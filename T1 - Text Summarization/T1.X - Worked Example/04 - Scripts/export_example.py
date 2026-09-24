"""Export one recorded production hearing; verify inputs without running an LLM.

Run with the project's existing Python environment. Both arguments name local
directories: the saved data tree and a cached Qwen3.5-4B tokenizer snapshot.
See README.md for the command and the provenance of the exported files.
"""

import argparse
import hashlib
import json
import sys
from functools import partial
from pathlib import Path
from unittest.mock import patch

import pyarrow.parquet as pq
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "T1 - Text Summarization/T1.X - Background Helper Functions"))
sys.path.insert(0, str(ROOT / "L - Lib/L2 - Document Parsing and Text Cleaning"))

from chunking import chunk_turns
from speakers import attribute
from transcript import extract_text, parse_transcript
import summarize as S

PACKAGE = "CHRG-115shrg37801"
BUDGET = 6144


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_root", type=Path)
    parser.add_argument("tokenizer_dir", type=Path)
    args = parser.parse_args()
    base = args.data_root
    repo_data = base / "interim/repo_data"

    def rows(path):
        return pq.read_table(path, filters=[("packageId", "==", PACKAGE)]).to_pylist()

    hearing, = rows(repo_data / "raw/02_hearings/hearings_sst.parquet")
    summary, = rows(repo_data / "cleaned/01_text_summarization/hearing_summaries.parquet")
    reference, = rows(repo_data / "cleaned/01_text_summarization/cspan_matches.parquet")
    raw_path = base / f"raw/govinfo/{hearing['year']}/html/{PACKAGE}.htm"
    log_path = base / f"interim/summaries/sst_Qwen3.5-4B/status/{PACKAGE}.jsonl"
    calls = [json.loads(line) for line in log_path.read_text().splitlines() if line.strip()]

    # Reproduce parsing and attribution before reconstructing model inputs.
    parsed = parse_transcript(raw_path)
    members = rows(base / "interim/govinfo/hearing_members.parquet")
    turns = attribute(parsed["paragraphs"], members, drop_front_matter=True)
    saved_turns = hearing["turns"]
    assert len(turns) == len(saved_turns) == 903
    # The saved parser missed the written-response appendix in this hearing.
    # Reproduce that recorded input rather than silently changing the sample.
    assert set(parsed["sections"]) == {"spoken"}, "Expected the saved all-spoken labeling."
    assert all(t["section"] == "spoken" for t in saved_turns)
    for rebuilt, saved in zip(turns, saved_turns):
        assert "\n\n".join(rebuilt["paragraphs"]) == saved["text"]
        assert all(rebuilt[k] == saved[k] for k in
                   ("honorific", "surname", "bioGuideId", "is_member"))

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_dir, local_files_only=True)
    chunks = chunk_turns(saved_turns, tokenizer, BUDGET, spoken_only=True)
    assert len(chunks) == summary["n_chunks"] == 55
    assert all(c["n_tokens"] <= BUDGET for c in chunks)
    assert all(c["model"] == summary["model"] and
               c["prompt_version"] == S.PROMPT_VERSION for c in calls)

    # Replay the existing orchestration with recorded outputs. Each attempted
    # model call must receive exactly the user prompt hashed in the saved log.
    pending = iter(calls)
    templates = {"map": S.MAP_USER, "collapse": S.COLLAPSE_USER, "reduce": S.REDUCE_USER}

    def replay(stage, text, *unused_args, **unused_kwargs):
        record = next(pending)
        prompt = templates[stage].format(text=text, target_words=S.REDUCE_TARGET_WORDS)
        assert record["stage"] == stage
        assert hashlib.sha256(prompt.encode()).hexdigest() == record["input_sha256"]
        return record["output"]

    with patch.object(S, "summarize_chunk", side_effect=partial(replay, "map")), \
         patch.object(S, "collapse_summaries", side_effect=partial(replay, "collapse")), \
         patch.object(S, "reduce_summaries", side_effect=partial(replay, "reduce")):
        result = S.map_reduce([c["text"] for c in chunks], None, tokenizer, BUDGET,
                              document_id=PACKAGE, model_name=summary["model"])
    assert next(pending, None) is None
    assert result["final_summary"] == summary["summary"]
    assert result["final_tokens"] == summary["summary_tokens"] == 359
    assert result["n_collapse_rounds"] == summary["n_collapse_rounds"] == 1
    assert result["n_calls"] == summary["n_calls"] == len(calls) == 59
    for rebuilt, saved in zip(result["log"].records, calls):
        assert all(rebuilt[k] == saved[k] for k in
                   ("stage", "level", "index", "n_inputs", "input_sha256",
                    "input_tokens", "output_tokens", "output"))

    # Write only after the full chain has passed verification.
    out = Path(__file__).resolve().parents[1]
    inputs = out / "01 - Inputs"
    chunk_inputs = inputs / "Chunks"
    outputs = out / "02 - Outputs"
    logs = out / "03 - Logs and Verification"
    for directory in (inputs, chunk_inputs, outputs, logs):
        directory.mkdir(parents=True, exist_ok=True)
    (inputs / "source.txt").write_text(extract_text(raw_path.read_bytes()), encoding="utf-8")
    (inputs / "parsed_turns.json").write_text(json.dumps({
        "packageId": PACKAGE, "title": hearing["title"],
        "n_paragraphs": hearing["n_paragraphs"],
        "n_paragraphs_dropped": hearing["n_paragraphs_dropped"],
        "paragraph_rule": hearing["paragraph_rule"], "turns": saved_turns,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (logs / "call_log.jsonl").write_bytes(log_path.read_bytes())

    def chunk_page(index):
        first = (index - 1) // 10 * 10 + 1
        return f"chunks_{first:02d}-{min(first + 9, len(chunks)):02d}.md"

    text = [f"# Model-input chunks: {PACKAGE}\n\n",
            "Reconstructed with the production tokenizer and 6,144-token budget. "
            f"All {len(chunks)} map user-prompt hashes match the saved run. "
            "The full inputs are divided into pages of up to ten chunks for reading. "
            "Text inside each fence is the exact chunk; headings and metadata "
            "are display labels.\n\n",
            "| Chunk | Tokens | Turn records represented | Split-turn flag |\n"
            "|---|---:|---:|---|\n"]
    for i, c in enumerate(chunks, 1):
        text.append(f"| [{i:02d}]({chunk_page(i)}#chunk-{i:02d}) | {c['n_tokens']:,} | "
                    f"{c['n_turns']} | {c['split_turn']} |\n")
    (chunk_inputs / "chunks.md").write_text("".join(text), encoding="utf-8")
    for start in range(0, len(chunks), 10):
        page = [f"# Model-input chunks {start + 1:02d}–{min(start + 10, len(chunks)):02d}: {PACKAGE}\n\n",
                "[All chunks and token counts](chunks.md). Text inside each fence "
                "is the verified model input; speaker metadata is a display label.\n"]
        for i, c in enumerate(chunks[start:start + 10], start + 1):
            page.append(f"\n## Chunk {i:02d}\n\n"
                        f"Tokens: {c['n_tokens']:,}. Speaker metadata: "
                        f"{', '.join(c['speakers'])}. Split-turn flag: {c['split_turn']}.\n\n"
                        f"```text\n{c['text']}\n```\n")
        (chunk_inputs / chunk_page(start + 1)).write_text("".join(page), encoding="utf-8")

    text = [f"# Recorded outputs: {PACKAGE}\n\n"
            "These are the output strings stored in the production log, without "
            "editorial corrections or new model generation. They include any "
            "sentence trimming performed by the original pipeline.\n\n"]
    for c in calls:
        name = "Final summary" if c["stage"] == "reduce" else f"{c['stage'].title()} {c['index'] + 1:02d}"
        text.append(f"## {name}\n\n"
                    f"Stage `{c['stage']}`, level {c['level']}, "
                    f"{c['n_inputs']} input(s), {c['output_tokens']} output tokens.\n\n"
                    f"```text\n{c['output']}\n```\n\n")
    text.append("## C-SPAN reference\n\n"
                f"Saved program ID: `{reference['cspan_id']}`. "
                f"Title: **{reference['cspan_title']}**.\n\n"
                f"```text\n{reference['abstract']}\n```\n")
    (outputs / "outputs.md").write_text("".join(text), encoding="utf-8")
    print(f"Verified {len(turns)} parsed records, {len(chunks)} chunks, "
          f"all {len(calls)} user-prompt hashes, and the stored final summary.")
    print(f"Exported example to {out}")


if __name__ == "__main__":
    main()
