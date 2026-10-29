"""T3.7.4 - Firm - Summarize Each Firm.

GPU batch stage of the topic-relevance rebuild: one summary per firm for one input set, one
summary family, and one prompt version, built from the firm's yearly filing summaries (T3.7.3's
table) with the per-firm task of that family, as the reduce stage of T1 builds one hearing
summary from its segment summaries. One call per firm; the firm's yearly summaries always fit
one call. Prompts, budgets, and generation settings come from T3.7.1's settings file; the
firm-level prompt must carry the same prompt version as the filing summaries it reads. Every
call is logged. A summary still over the encoder limit after the re-asks is trimmed by dropping
trailing sentences until it fits, and the record says so. --seed changes only the sampling, so a firm
can be rerun with the same prompts until its summary fits on its own. Rerunnable: finished firms are read back and skipped.
Run only on a card the environment's torch build supports (A40, L40S, A100).

Usage   python "T3.7.4 - Firm - Summarize Each Firm.py" --set three_years --family summary_lines_of_business --version item1-mapreduce-1.2
Reads   output/T3.7.1/settings.json; <scratch>/T3.7 - Firm Summaries/Processed/filing_summaries.parquet; output/T3.4.1/filings.csv
Writes  <scratch>/T3.7 - Firm Summaries/Interim/firm_summaries/<set>/<family>/<version>/firms.jsonl        (one line per firm)
        <scratch>/T3.7 - Firm Summaries/Interim/firm_summaries/<set>/<family>/<version>/firms.calls.jsonl  (every model call)
        <scratch>/T3.7 - Firm Summaries/Interim/firm_summaries/<set>/<family>/<version>/firms.json        (run record)
"""
import argparse
import hashlib
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
SCRATCH_FOLDER = Path("/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3-TEMP")
SETTINGS_FILE = PROJECT_FOLDER / NOTEBOOK_SUBFOLDER / "output/T3.7.1/settings.json"
FILINGS_FILE = PROJECT_FOLDER / NOTEBOOK_SUBFOLDER / "output/T3.4.1/filings.csv"
TABLE_FILE = SCRATCH_FOLDER / "T3.7 - Firm Summaries" / "Processed" / "filing_summaries.parquet"
FIRM_FOLDER = SCRATCH_FOLDER / "T3.7 - Firm Summaries" / "Interim" / "firm_summaries"
BGE_MODEL_FOLDER = Path(
    "/scratch2/acroh/projects/llm_method/hf_cache/hub/models--BAAI--bge-large-en-v1.5"
    "/snapshots/d4aa6901d3a41ba39fb536a557fa166f842b0e09"
)

MAX_BATCH_TOKENS = 48_000  # total padded prompt tokens per forward pass
MAX_BATCH_PROMPTS = 16  # prompts per forward pass at most
SEED = 0
SHORTER_TARGET_WORDS = ["150 to 200", "120 to 150"]  # re-asks for a firm summary that exceeds the bge limit
PROGRESS_EVERY = 10

parser = argparse.ArgumentParser()
parser.add_argument("--set", required=True, choices=["three_years", "all_years"], help="three_years uses the three-year filings; all_years uses every filing of the firm")
parser.add_argument("--family", required=True, help="summary family from T3.7.1 settings")
parser.add_argument("--version", required=True, help="prompt version of the filing summaries to read; must equal the current settings version")
parser.add_argument("--limit", type=int, default=None, help="smoke test: only the first N firms")
parser.add_argument("--seed", type=int, default=SEED, help="sampling seed; change it to redraw a firm whose summary did not fit")
args = parser.parse_args()

# Step 1. Read the settings, the filing summaries of this family and version, and the sample flags.
settings = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
assert args.family in settings["families"], f"unknown family {args.family}"
assert args.version == settings["prompt_version"], f"settings are at {settings['prompt_version']}, requested {args.version}"
prompts = settings["prompts"]
table = pd.read_parquet(TABLE_FILE)
table = table.loc[table["family"].eq(args.family) & table["prompt_version"].eq(args.version)]
filings = pd.read_csv(FILINGS_FILE, dtype={"gvkey": str, "cik": str})
flag = "in_three_years" if args.set == "three_years" else "in_all_years"
wanted = filings.loc[filings[flag].eq(1), ["accessionNo", "gvkey", "conm", "fyear"]]
missing = set(wanted["accessionNo"]) - set(table["accessionNo"])
assert not missing, f"{len(missing)} filings of the {args.set} sample have no {args.family} summary at {args.version} yet"
yearly = wanted.merge(table[["accessionNo", "summary"]], on="accessionNo", how="left", validate="one_to_one")
firms = yearly.groupby("gvkey", sort=True).agg(conm=("conm", "first"), n_filings=("accessionNo", "size"), years=("fyear", lambda s: sorted(int(y) for y in s)))
if args.limit is not None:
    firms = firms.head(args.limit)
output_folder = FIRM_FOLDER / args.set / args.family / args.version
output_folder.mkdir(parents=True, exist_ok=True)
output_file = output_folder / "firms.jsonl"
calls_file = output_folder / "firms.calls.jsonl"
done = set()
if output_file.exists():
    done = {json.loads(line)["gvkey"] for line in output_file.read_text(encoding="utf-8").splitlines()}
firms = firms.loc[~firms.index.isin(done)]
print(f"Set {args.set}, family {args.family}, version {args.version}: {len(firms):,} firms to do ({len(done):,} already done), {int(firms['n_filings'].sum()):,} yearly summaries", flush=True)

# Step 2. Load the language model on the GPU and the encoder's tokenizer for the length check.
assert torch.cuda.is_available(), "run this stage on a GPU node"
torch.manual_seed(args.seed)
model_folder = Path(settings["model_folder"])
tokenizer = AutoTokenizer.from_pretrained(model_folder, local_files_only=True)
tokenizer.padding_side = "left"
pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id
model = AutoModelForCausalLM.from_pretrained(model_folder, dtype=torch.bfloat16, device_map="cuda", local_files_only=True).eval()
bge_tokenizer = AutoTokenizer.from_pretrained(BGE_MODEL_FOLDER, local_files_only=True)
gpu_name = torch.cuda.get_device_name(0)
run_started = datetime.now(timezone.utc).isoformat(timespec="seconds")
calls_handle = calls_file.open("a", encoding="utf-8")
n_calls = 0
print(f"Model {model_folder.parent.parent.name} on {gpu_name}, {next(model.parameters()).dtype}; prompt version {settings['prompt_version']}", flush=True)


def render(user_prompt):
    messages = [{"role": "system", "content": prompts["system"]["reduce"]}, {"role": "user", "content": user_prompt}]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=settings["enable_thinking"])


def model_tokens(text):
    return len(tokenizer(text, add_special_tokens=False)["input_ids"])


def trim_to_sentence(text):
    text = text.rstrip()
    if not text or text.endswith((".", "!", "?", '."', ".'", ".)")):
        return text
    cut = max(text.rfind(mark) for mark in ".!?")
    if cut <= 0:
        return text
    end = cut + 1
    while end < len(text) and text[end] in "\"')]":
        end += 1
    return text[:end].rstrip()


def clean(text):
    return re.sub(r"^<think>.*?</think>\s*", "", text.strip(), flags=re.DOTALL).strip()


def generate_batched(items, max_new_tokens):
    """Generate completions for (gvkey, user_prompt) items; returns {gvkey: text}. Logs every call."""
    global n_calls
    rendered = {key: render(user_prompt) for key, user_prompt in items}
    lengths = {key: model_tokens(text) for key, text in rendered.items()}
    order = sorted(rendered, key=lambda key: lengths[key])
    batches, current = [], []
    for key in order:
        longest = max([lengths[k] for k in current] + [lengths[key]])
        if current and (len(current) + 1 > MAX_BATCH_PROMPTS or longest * (len(current) + 1) > MAX_BATCH_TOKENS):
            batches.append(current)
            current = []
        current.append(key)
    if current:
        batches.append(current)
    results, user_prompts = {}, dict(items)
    for batch_number, batch in enumerate(batches, start=1):
        encoded = tokenizer([rendered[key] for key in batch], return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
        started = time.time()
        with torch.no_grad():
            output_ids = model.generate(**encoded, max_new_tokens=max_new_tokens, pad_token_id=pad_token_id, **settings["generation"])
        generated = output_ids[:, encoded["input_ids"].shape[1]:].cpu()
        del output_ids, encoded
        torch.cuda.empty_cache()
        seconds = time.time() - started
        for row, key in enumerate(batch):
            ids = generated[row]
            ids = ids[ids != pad_token_id]
            text = clean(tokenizer.decode(ids, skip_special_tokens=True))
            hit_cap = int(len(ids)) >= max_new_tokens
            if hit_cap:
                text = trim_to_sentence(text)
            results[key] = text
            calls_handle.write(json.dumps({
                "gvkey": key, "family": args.family, "stage": "firm", "prompt_version": settings["prompt_version"],
                "model": settings["model_folder"], "input_sha256": hashlib.sha256(user_prompts[key].encode("utf-8")).hexdigest(),
                "input_tokens": lengths[key], "output_tokens": int(len(ids)), "hit_cap": hit_cap, "seconds_batch": round(seconds, 1),
                "batch_size": len(batch), "output": text, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }, ensure_ascii=False) + "\n")
            n_calls += 1
        calls_handle.flush()
        if batch_number % PROGRESS_EVERY == 0 or batch_number == len(batches):
            print(f"  firm: batch {batch_number}/{len(batches)}, {len(batch)} prompts, longest {max(lengths[k] for k in batch):,} tokens, {seconds:.0f}s", flush=True)
    return results


def firm_prompt(gvkey, target_words):
    firm = firms.loc[gvkey]
    rows = yearly.loc[yearly["gvkey"].eq(gvkey)].sort_values("fyear")
    text = "\n\n".join(f"[fiscal {int(row.fyear)}] {row.summary}" for row in rows.itertuples(index=False))
    years = ", ".join(str(year) for year in firm["years"])
    return prompts["firm_opening"].format(company=firm["conm"], years=years, text=text) \
        + prompts["firm_tasks"][args.family].format(target_words=target_words)


# Step 3. One call per firm, then the length rule with re-asks, then write.
stage_started = time.time()
items = [(gvkey, firm_prompt(gvkey, settings["target_words"]["firm"])) for gvkey in firms.index]
print(f"Firm calls: {len(items):,}", flush=True)
final = generate_batched(items, settings["max_new_tokens"]["reduce"]) if items else {}
rounds = {gvkey: 1 for gvkey in firms.index}
for target_words in SHORTER_TARGET_WORDS:
    too_long = [gvkey for gvkey in firms.index if len(bge_tokenizer(final[gvkey])["input_ids"]) > settings["max_bge_tokens"]]
    if not too_long:
        break
    print(f"Re-asking {len(too_long):,} firms at {target_words} words", flush=True)
    redo = generate_batched([(gvkey, firm_prompt(gvkey, target_words)) for gvkey in too_long], settings["max_new_tokens"]["reduce"])
    for gvkey in too_long:
        final[gvkey] = redo[gvkey]
        rounds[gvkey] += 1

# Step 4. Last resort for a summary still over the encoder limit after the re-asks: drop trailing sentences until it fits.
trimmed = {gvkey: False for gvkey in firms.index}
for gvkey in firms.index:
    while len(bge_tokenizer(final[gvkey])["input_ids"]) > settings["max_bge_tokens"]:
        sentences = re.split(r"(?<=[.!?])\s+", final[gvkey].strip())
        assert len(sentences) > 1, f"{gvkey}: cannot trim a one-sentence summary under the limit"
        final[gvkey] = " ".join(sentences[:-1])
        trimmed[gvkey] = True
n_trimmed = sum(trimmed.values())
if n_trimmed:
    print(f"Trimmed {n_trimmed} firm summaries to the encoder limit by dropping trailing sentences", flush=True)

records_written = 0
with output_file.open("a", encoding="utf-8") as handle:
    for gvkey, firm in firms.iterrows():
        text = final[gvkey]
        n_bge_tokens = len(bge_tokenizer(text)["input_ids"])
        handle.write(json.dumps({
            "gvkey": gvkey, "conm": firm["conm"], "set": args.set, "family": args.family, "prompt_version": settings["prompt_version"],
            "n_filings": int(firm["n_filings"]), "years": firm["years"], "summary": text, "n_words": len(text.split()),
            "n_bge_tokens": n_bge_tokens, "within_bge_limit": n_bge_tokens <= settings["max_bge_tokens"], "reduce_rounds": rounds[gvkey], "trimmed": trimmed[gvkey],
            "run_started": run_started,
        }, ensure_ascii=False) + "\n")
        records_written += 1
calls_handle.close()
seconds = time.time() - stage_started
(output_folder / "firms.json").write_text(json.dumps({
    "set": args.set, "family": args.family, "prompt_version": settings["prompt_version"], "firms_done_this_run": records_written,
    "firms_skipped_as_done": len(done), "firms_trimmed": n_trimmed, "model_calls": n_calls, "model": settings["model_folder"], "gpu": gpu_name,
    "generation": settings["generation"], "enable_thinking": settings["enable_thinking"], "max_new_tokens": settings["max_new_tokens"]["reduce"],
    "seed": args.seed, "torch": torch.__version__, "seconds": round(seconds, 1), "run_started": run_started,
    "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}, indent=2), encoding="utf-8")
print(f"Wrote {records_written:,} firm summaries ({n_calls:,} model calls) to {output_file} in {seconds / 60:.1f} minutes", flush=True)
