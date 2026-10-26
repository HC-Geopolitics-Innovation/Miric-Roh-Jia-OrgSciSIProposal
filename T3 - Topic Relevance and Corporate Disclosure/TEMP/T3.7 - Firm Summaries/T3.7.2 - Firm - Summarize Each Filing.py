"""T3.7.2 - Firm - Summarize Each Filing.

GPU batch stage of the topic-relevance rebuild: one summary per filing for one summary family,
by the map-collapse-reduce of the hearing summaries (T1): every segment of a filing is summarized
(map); when the segment summaries together exceed the aggregation budget they are condensed in
groups (collapse) until they fit; one call writes the filing's summary (reduce). Prompts, budgets,
and generation settings come from T3.7.1's settings file. Prompts of one stage are batched by
length across filings so similar-sized prompts share a forward pass. Every call is logged with
the stage, level, index, an input hash, token counts, time, and the full output, as T1 logs.
A task that is interrupted can be rerun: finished filings are read back and skipped.
Run only on a card the environment's torch build supports (A40, L40S, A100).

Usage   python "T3.7.2 - Firm - Summarize Each Filing.py" --set three_years --family summary_lines_of_business --shard 3
Reads   output/T3.7.1/settings.json; <scratch>/T3.7 - Firm Summaries/Interim/filing_inputs/<set>/shard_<k>.parquet
Writes  <scratch>/T3.7 - Firm Summaries/Interim/filing_summaries/<set>/<family>/<prompt version>/shard_<k>.jsonl       (one line per filing)
        <scratch>/T3.7 - Firm Summaries/Interim/filing_summaries/<set>/<family>/<prompt version>/shard_<k>.calls.jsonl (every model call)
        <scratch>/T3.7 - Firm Summaries/Interim/filing_summaries/<set>/<family>/<prompt version>/shard_<k>.json        (run record)
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
INPUTS_FOLDER = SCRATCH_FOLDER / "T3.7 - Firm Summaries" / "Interim" / "filing_inputs"
SUMMARIES_FOLDER = SCRATCH_FOLDER / "T3.7 - Firm Summaries" / "Interim" / "filing_summaries"
BGE_MODEL_FOLDER = Path(
    "/scratch2/acroh/projects/llm_method/hf_cache/hub/models--BAAI--bge-large-en-v1.5"
    "/snapshots/d4aa6901d3a41ba39fb536a557fa166f842b0e09"
)

MAX_BATCH_TOKENS = 48_000  # total padded prompt tokens per forward pass; measured at about 23 GB on an A40 for 55,000
MAX_BATCH_PROMPTS = 16  # prompts per forward pass at most
MAX_COLLAPSE_LEVELS = 8  # runaway guard on collapse rounds, as in T1
SEED = 0  # sampling at temperature 0.1 is near-greedy; the seed makes a rerun of the same shard repeat on the same card
SHORTER_TARGET_WORDS = ["100 to 150", "80 to 100"]  # re-asks for a final summary that exceeds the bge limit
PROGRESS_EVERY = 10  # batches between progress lines

parser = argparse.ArgumentParser()
parser.add_argument("--set", required=True, choices=["three_years", "remaining"], help="input set from T3.7.1")
parser.add_argument("--family", required=True, help="summary family from T3.7.1 settings")
parser.add_argument("--shard", type=int, required=True, help="shard id within the set")
parser.add_argument("--limit", type=int, default=None, help="smoke test: only the first N filings of the shard")
args = parser.parse_args()

# Step 1. Read the settings and the shard; read back finished filings.
settings = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
assert args.family in settings["families"], f"unknown family {args.family}"
prompts = settings["prompts"]
shard = pd.read_parquet(INPUTS_FOLDER / args.set / f"shard_{args.shard}.parquet")
if args.limit is not None:
    shard = shard.loc[shard["accessionNo"].isin(shard["accessionNo"].drop_duplicates().head(args.limit))].copy()
assert shard["n_model_tokens"].le(settings["segment_tokens"]).all()
output_folder = SUMMARIES_FOLDER / args.set / args.family / settings["prompt_version"]
output_folder.mkdir(parents=True, exist_ok=True)
output_file = output_folder / f"shard_{args.shard}.jsonl"
calls_file = output_folder / f"shard_{args.shard}.calls.jsonl"
done = set()
if output_file.exists():
    done = {json.loads(line)["accessionNo"] for line in output_file.read_text(encoding="utf-8").splitlines()}
shard = shard.loc[~shard["accessionNo"].isin(done)].copy()
filings = shard.groupby("accessionNo", sort=False).first()[["gvkey", "conm", "fyear", "n_segments"]]
print(f"Set {args.set}, family {args.family}, shard {args.shard}: {len(filings):,} filings to do ({len(done):,} already done), {len(shard):,} segments", flush=True)

# Step 2. Load the language model on the GPU and the encoder's tokenizer for the length check.
assert torch.cuda.is_available(), "run this stage on a GPU node"
torch.manual_seed(SEED + args.shard)
model_folder = Path(settings["model_folder"])
tokenizer = AutoTokenizer.from_pretrained(model_folder, local_files_only=True)
tokenizer.padding_side = "left"
pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id
model = AutoModelForCausalLM.from_pretrained(
    model_folder, dtype=torch.bfloat16, device_map="cuda", local_files_only=True
).eval()
bge_tokenizer = AutoTokenizer.from_pretrained(BGE_MODEL_FOLDER, local_files_only=True)
gpu_name = torch.cuda.get_device_name(0)
run_started = datetime.now(timezone.utc).isoformat(timespec="seconds")
calls_handle = calls_file.open("a", encoding="utf-8")
n_calls = 0
print(f"Model {model_folder.parent.parent.name} on {gpu_name}, {next(model.parameters()).dtype}; prompt version {settings['prompt_version']}", flush=True)


def render(stage, user_prompt):
    """Chat template with the stage's system prompt and reasoning traces off."""
    messages = [{"role": "system", "content": prompts["system"][stage]}, {"role": "user", "content": user_prompt}]
    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=settings["enable_thinking"]
    )


def model_tokens(text):
    return len(tokenizer(text, add_special_tokens=False)["input_ids"])


def trim_to_sentence(text):
    """Cut a capped completion back to its last complete sentence."""
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


def generate_batched(stage, items, max_new_tokens):
    """Generate completions for (key, user_prompt) items of one stage; returns {key: text}.

    Prompts are sorted by length and grouped so a batch holds at most MAX_BATCH_PROMPTS prompts and
    MAX_BATCH_TOKENS padded tokens. A completion that hits the cap is trimmed to its last sentence.
    Every completion is written to the call log with its stage, the item's level and index, and an
    input hash, as T1's CallLog does.
    """
    global n_calls
    rendered = {key: render(stage, user_prompt) for key, user_prompt in items}
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
    results = {}
    user_prompts = dict(items)
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
            accessionNo, level, index = key[0], key[1], key[2]
            calls_handle.write(json.dumps({
                "accessionNo": accessionNo, "family": args.family, "stage": stage, "level": level, "index": index,
                "prompt_version": settings["prompt_version"], "model": settings["model_folder"],
                "input_sha256": hashlib.sha256(user_prompts[key].encode("utf-8")).hexdigest(),
                "input_tokens": lengths[key], "output_tokens": int(len(ids)), "hit_cap": hit_cap,
                "seconds_batch": round(seconds, 1), "batch_size": len(batch), "output": text,
                "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }, ensure_ascii=False) + "\n")
            n_calls += 1
        calls_handle.flush()
        if batch_number % PROGRESS_EVERY == 0 or batch_number == len(batches):
            print(f"  {stage}: batch {batch_number}/{len(batches)}, {len(batch)} prompts, longest {max(lengths[k] for k in batch):,} tokens, {seconds:.0f}s", flush=True)
    return results


stage_started = time.time()

# Step 3. Map: one call per segment.
map_items = []
for segment in shard.itertuples(index=False):
    user_prompt = prompts["map_opening"].format(
        company=segment.conm, fyear=segment.fyear, segment=segment.segment_id, n_segments=segment.n_segments, text=segment.text
    ) + prompts["map_tasks"][args.family].format(target_words=settings["target_words"]["map"])
    map_items.append(((segment.accessionNo, 0, int(segment.segment_id)), user_prompt))
print(f"Map: {len(map_items):,} segment calls", flush=True)
map_results = generate_batched("map", map_items, settings["max_new_tokens"]["map"]) if map_items else {}
summaries = {
    accessionNo: [map_results[(accessionNo, 0, segment_id)] for segment_id in range(1, int(n_segments) + 1)]
    for accessionNo, n_segments in filings["n_segments"].items()
}
levels_reached = {accessionNo: 0 for accessionNo in summaries}

# Step 4. Collapse: while a filing's segment summaries exceed the aggregation budget, condense them in groups.
join = "\n\n"
for level in range(1, MAX_COLLAPSE_LEVELS + 1):
    collapse_items, groups_of = [], {}
    for accessionNo, parts in summaries.items():
        if model_tokens(join.join(parts)) <= settings["aggregation_budget"]:
            continue
        groups, current, current_tokens = [], [], 0
        for part in parts:
            n_tokens = model_tokens(part) + (model_tokens(join) if current else 0)
            if current and current_tokens + n_tokens > settings["aggregation_budget"]:
                groups.append(current)
                current, current_tokens = [], 0
                n_tokens = model_tokens(part)
            current.append(part)
            current_tokens += n_tokens
        groups.append(current)
        groups_of[accessionNo] = len(groups)
        for index, group in enumerate(groups, start=1):
            filing = filings.loc[accessionNo]
            user_prompt = prompts["collapse_opening"].format(company=filing["conm"], fyear=filing["fyear"], text=join.join(group)) \
                + prompts["collapse_tasks"][args.family].format(target_words=settings["target_words"]["collapse"])
            collapse_items.append(((accessionNo, level, index), user_prompt))
    if not collapse_items:
        break
    print(f"Collapse level {level}: {len(groups_of):,} filings, {len(collapse_items):,} group calls", flush=True)
    collapse_results = generate_batched("collapse", collapse_items, settings["max_new_tokens"]["collapse"])
    for accessionNo, n_groups in groups_of.items():
        summaries[accessionNo] = [collapse_results[(accessionNo, level, index)] for index in range(1, n_groups + 1)]
        levels_reached[accessionNo] = level
else:
    raise RuntimeError(f"segment summaries still over the aggregation budget after {MAX_COLLAPSE_LEVELS} collapse levels")

# Step 5. Reduce: one call per filing, then the length rule with re-asks, then write.
def reduce_prompt(accessionNo, target_words):
    filing = filings.loc[accessionNo]
    return prompts["reduce_opening"].format(company=filing["conm"], fyear=filing["fyear"], text=join.join(summaries[accessionNo])) \
        + prompts["reduce_tasks"][args.family].format(target_words=target_words)


reduce_items = [((accessionNo, 99, 1), reduce_prompt(accessionNo, settings["target_words"]["reduce"])) for accessionNo in summaries]
print(f"Reduce: {len(reduce_items):,} filing calls", flush=True)
final = generate_batched("reduce", reduce_items, settings["max_new_tokens"]["reduce"]) if reduce_items else {}
rounds = {accessionNo: 1 for accessionNo in summaries}
for target_words in SHORTER_TARGET_WORDS:
    too_long = [accessionNo for accessionNo in summaries if len(bge_tokenizer(final[(accessionNo, 99, 1)])["input_ids"]) > settings["max_bge_tokens"]]
    if not too_long:
        break
    print(f"Re-asking {len(too_long):,} filings at {target_words} words", flush=True)
    redo = generate_batched("reduce", [((accessionNo, 99, 1), reduce_prompt(accessionNo, target_words)) for accessionNo in too_long], settings["max_new_tokens"]["reduce"])
    for accessionNo in too_long:
        final[(accessionNo, 99, 1)] = redo[(accessionNo, 99, 1)]
        rounds[accessionNo] += 1

records_written = 0
with output_file.open("a", encoding="utf-8") as handle:
    for accessionNo, filing in filings.iterrows():
        text = final[(accessionNo, 99, 1)]
        n_bge_tokens = len(bge_tokenizer(text)["input_ids"])
        handle.write(json.dumps({
            "accessionNo": accessionNo, "gvkey": filing["gvkey"], "conm": filing["conm"], "fyear": int(filing["fyear"]),
            "family": args.family, "prompt_version": settings["prompt_version"], "summary": text,
            "n_words": len(text.split()), "n_bge_tokens": n_bge_tokens, "within_bge_limit": n_bge_tokens <= settings["max_bge_tokens"],
            "n_segments": int(filing["n_segments"]), "collapse_levels": levels_reached[accessionNo], "reduce_rounds": rounds[accessionNo],
            "run_started": run_started,
        }, ensure_ascii=False) + "\n")
        records_written += 1
calls_handle.close()
seconds = time.time() - stage_started

# Step 6. Run record.
(output_folder / f"shard_{args.shard}.json").write_text(json.dumps({
    "set": args.set, "family": args.family, "shard_id": args.shard, "filings_done_this_run": records_written,
    "filings_skipped_as_done": len(done), "segments": int(len(shard)), "model_calls": n_calls,
    "prompt_version": settings["prompt_version"], "model": settings["model_folder"], "gpu": gpu_name,
    "generation": settings["generation"], "enable_thinking": settings["enable_thinking"], "max_new_tokens": settings["max_new_tokens"],
    "seed": SEED + args.shard, "max_batch_tokens": MAX_BATCH_TOKENS, "max_batch_prompts": MAX_BATCH_PROMPTS,
    "torch": torch.__version__, "seconds": round(seconds, 1), "run_started": run_started,
    "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}, indent=2), encoding="utf-8")
print(f"Wrote {records_written:,} filing summaries ({n_calls:,} model calls) to {output_file} in {seconds / 60:.1f} minutes", flush=True)
