"""T3.5.5 - Topic - Summarize the Statements.

Batch stage of the topic-relevance rebuild: one map call per hearing year over that year's
Topic 68 statements, then one reduce call that combines the per-year summaries into the policy
summary. Everything the calls depend on comes from the T3.5.4 input file; nothing is retyped
here. Run on a GPU node whose card the environment's torch build supports (A40, L40S, A100).

Reads   output/T3.5.4/policy_summary_input.json
Writes  output/T3.5.5/yearly_summaries.csv, policy_summary.md, policy_summary_meta.json
        <scratch>/T3.5 - Topic Representations/Interim/policy_summary_calls.jsonl (every call)
"""
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

PROJECT_FOLDER = Path("/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis")
NOTEBOOK_SUBFOLDER = Path("T3 - Topic Relevance and Corporate Disclosure/TEMP")
STAGE_NAME = "T3.5.5"  # the identifier names this stage's output folder
INPUT_FILE = PROJECT_FOLDER / NOTEBOOK_SUBFOLDER / "output/T3.5.4/policy_summary_input.json"
OUTPUT_FOLDER = PROJECT_FOLDER / NOTEBOOK_SUBFOLDER / "output" / STAGE_NAME
SCRATCH_FOLDER = Path("/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3-TEMP")
LOG_FILE = SCRATCH_FOLDER / "T3.5 - Topic Representations" / "Interim" / "policy_summary_calls.jsonl"
BGE_MODEL_FOLDER = Path(
    "/scratch2/acroh/projects/llm_method/hf_cache/hub/models--BAAI--bge-large-en-v1.5"
    "/snapshots/d4aa6901d3a41ba39fb536a557fa166f842b0e09"
)

SEED = 0  # sampling at temperature 0.1 is near-greedy; the seed makes a rerun repeat on the same card
SHORTER_TARGET_WORDS = ["150 to 200", "120 to 150", "100 to 120"]  # re-asks if the final summary exceeds the bge limit

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Step 1. Read the input file written by T3.5.4.
policy_input = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
settings = policy_input["settings"]
prompts = policy_input["prompts"]
chunks = policy_input["chunks"]
statement_lines = policy_input["statement_lines"]
assert policy_input["mode"] == "map_by_year_then_reduce"
assert sum(chunk["n_statements"] for chunk in chunks) == len(statement_lines)
print(f"Input: {INPUT_FILE}")
print(f"Statements: {len(statement_lines):,}; map calls: {len(chunks)}; settings: {settings}")

# Step 2. Load the language model on the GPU and the encoder's tokenizer for the length check.
assert torch.cuda.is_available(), "run this stage on a GPU node"
torch.manual_seed(SEED)
model_folder = Path(settings["model_folder"])
tokenizer = AutoTokenizer.from_pretrained(model_folder, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    model_folder, dtype=torch.bfloat16, device_map="cuda", local_files_only=True
).eval()
bge_tokenizer = AutoTokenizer.from_pretrained(BGE_MODEL_FOLDER, local_files_only=True)
gpu_name = torch.cuda.get_device_name(0)
print(f"Model: {model_folder.parent.parent.name} on {gpu_name}, {next(model.parameters()).dtype}")

run_started = datetime.now(timezone.utc).isoformat(timespec="seconds")
log_handle = LOG_FILE.open("a", encoding="utf-8")


def generate_once(stage, label, user_prompt):
    """One prompt, one completion, fresh context; the call is logged before returning.

    Returns the completion text, whether it hit the new-token cap, and the token counts.
    """
    messages = [{"role": "system", "content": prompts["system"]}, {"role": "user", "content": user_prompt}]
    rendered = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=settings["enable_thinking"]
    )
    encoded = tokenizer(rendered, return_tensors="pt").to(model.device)
    n_input_tokens = int(encoded["input_ids"].shape[-1])
    assert n_input_tokens <= settings["input_token_budget"], f"{label}: prompt exceeds the budget"
    started = time.time()
    with torch.no_grad():
        output_ids = model.generate(
            **encoded,
            max_new_tokens=settings["max_new_tokens"],
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            **settings["generation"],
        )
    generated_ids = output_ids[0][n_input_tokens:]
    n_output_tokens = int(len(generated_ids))
    hit_cap = n_output_tokens >= settings["max_new_tokens"]
    text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    text = re.sub(r"^<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()  # defensive: no reasoning trace kept
    seconds = time.time() - started
    log_handle.write(json.dumps({
        "run_started": run_started, "stage": stage, "label": label, "model": settings["model_folder"],
        "gpu": gpu_name, "generation": settings["generation"], "enable_thinking": settings["enable_thinking"],
        "max_new_tokens": settings["max_new_tokens"], "seed": SEED, "n_input_tokens": n_input_tokens,
        "n_output_tokens": n_output_tokens, "hit_cap": hit_cap, "seconds": round(seconds, 1),
        "user_prompt": user_prompt, "output": text,
    }, ensure_ascii=False) + "\n")
    log_handle.flush()
    print(f"  {stage} {label}: {n_input_tokens:,} in, {n_output_tokens} out, {seconds:.0f}s{', HIT CAP' if hit_cap else ''}", flush=True)
    return text, hit_cap, n_input_tokens, n_output_tokens


def trim_to_sentence(text):
    """Cut a capped completion back to its last complete sentence."""
    ends = [text.rfind(mark) for mark in (". ", "! ", "? ")] + [len(text) if text.endswith((".", "!", "?")) else -1]
    cut = max(ends)
    return text[:cut + 1].strip() if cut > 0 else text


# Step 3. Map: one call per hearing year.
print("Map step")
yearly_rows = []
for chunk in chunks:
    statements_block = "\n".join(statement_lines[number - 1] for number in chunk["statement_numbers"])
    user_prompt = prompts["map_template"].format(
        n_statements=chunk["n_statements"], year=chunk["hearing_year"], topic_label=policy_input["topic_label"],
        statements_block=statements_block, target_words=settings["map_target_words"],
    )
    summary, hit_cap, n_in, n_out = generate_once("map", str(chunk["hearing_year"]), user_prompt)
    if hit_cap:
        summary = trim_to_sentence(summary)
    yearly_rows.append({
        "chunk_id": chunk["chunk_id"], "hearing_year": chunk["hearing_year"], "n_statements": chunk["n_statements"],
        "summary": summary, "n_words": len(summary.split()),
        "n_bge_tokens": len(bge_tokenizer(summary)["input_ids"]), "hit_cap": hit_cap,
        "n_input_tokens": n_in, "n_output_tokens": n_out,
    })
yearly_summaries = pd.DataFrame(yearly_rows)
assert yearly_summaries["summary"].str.strip().ne("").all()
yearly_file = OUTPUT_FOLDER / "yearly_summaries.csv"
yearly_summaries.to_csv(yearly_file, index=False)
print(f"Saved: {yearly_file}")

# Step 4. Reduce: one call over the per-year summaries, re-asked shorter if it exceeds the bge limit.
print("Reduce step")
summaries_block = "\n".join(f"[{row.hearing_year}] {row.summary}" for row in yearly_summaries.itertuples(index=False))
reduce_rounds = []
for round_number, target_words in enumerate([settings["reduce_target_words"]] + SHORTER_TARGET_WORDS, start=1):
    user_prompt = prompts["reduce_template"].format(
        n_years=len(yearly_summaries), year_min=policy_input["year_min"], year_max=policy_input["year_max"],
        topic_label=policy_input["topic_label"], summaries_block=summaries_block, target_words=target_words,
    )
    summary, hit_cap, n_in, n_out = generate_once("reduce", f"round {round_number} ({target_words} words)", user_prompt)
    if hit_cap:
        summary = trim_to_sentence(summary)
    n_bge_tokens = len(bge_tokenizer(summary)["input_ids"])
    reduce_rounds.append({"round": round_number, "target_words": target_words, "n_words": len(summary.split()),
                          "n_bge_tokens": n_bge_tokens, "hit_cap": hit_cap})
    if n_bge_tokens <= settings["max_bge_tokens"]:
        break
else:
    raise RuntimeError(f"final summary still exceeds {settings['max_bge_tokens']} bge tokens after {len(reduce_rounds)} rounds")
log_handle.close()

# Step 5. Save the policy summary and its metadata.
summary_file = OUTPUT_FOLDER / "policy_summary.md"
meta_file = OUTPUT_FOLDER / "policy_summary_meta.json"
summary_file.write_text(summary + "\n", encoding="utf-8")
meta_file.write_text(json.dumps({
    "topic_id": policy_input["topic_id"], "topic_label": policy_input["topic_label"],
    "n_statements": len(statement_lines), "n_map_calls": len(chunks), "reduce_rounds": reduce_rounds,
    "final_n_words": len(summary.split()), "final_n_bge_tokens": n_bge_tokens,
    "model": settings["model_folder"], "gpu": gpu_name, "generation": settings["generation"],
    "enable_thinking": settings["enable_thinking"], "max_new_tokens": settings["max_new_tokens"], "seed": SEED,
    "run_started": run_started, "run_finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "call_log": str(LOG_FILE),
}, indent=2), encoding="utf-8")
print(f"Saved: {summary_file}")
print(f"Saved: {meta_file}")
print(f"Final summary: {len(summary.split())} words, {n_bge_tokens} bge tokens, after {len(reduce_rounds)} reduce round(s)")
print(f"Call log: {LOG_FILE}")
