"""Export the recorded Zuckerberg example and verify it without model generation.

Run with the existing project environment and the saved data root as the sole
argument. See README.md for sources and the limits of this verification.
"""

import argparse
import ast
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions"))
import stance

PACKAGE = "CHRG-115shrg37801"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_root", type=Path)
    base = parser.parse_args().data_root
    topics = base / "interim/topics"
    tax = topics / "taxonomy"

    def hearing_rows(path):
        return pq.read_table(path, filters=[("packageId", "==", PACKAGE)]).to_pylist()

    raw = json.loads((ROOT / "T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/parsed_turns.json").read_text())["turns"]
    turns = sorted(hearing_rows(topics / "track2/member_turns.parquet"), key=lambda r: r["turn_idx"])
    status = {r["turn_idx"]: r for r in hearing_rows(topics / "track2/stance_turns.parquet")}
    records = sorted(hearing_rows(tax / "track2_assigned.parquet"), key=lambda r: (r["turn_idx"], r["record_idx"]))
    original_records = sorted(hearing_rows(topics / "track2/stance_records.parquet"), key=lambda r: (r["turn_idx"], r["record_idx"]))
    assert len(records) == len(original_records)
    for assigned, original in zip(records, original_records):
        assert all(assigned[k] == v for k, v in original.items())

    # Select the original log lines, including every window of long turns.
    log_lines = []
    for path in [topics / "track1/status/extract.jsonl", *sorted((topics / "track2/status").glob("extract_*.jsonl"))]:
        with path.open() as stream:
            for line in stream:
                if PACKAGE in line:
                    row = json.loads(line)
                    if row["document_id"].split(":")[0] == PACKAGE:
                        log_lines.append(line)
    calls = [json.loads(line) for line in log_lines]
    by_turn = defaultdict(list)
    for call in calls:
        if call["stage"] == "extract":
            by_turn[int(call["document_id"].split(":")[1])].append(call)
    t1_call, = [c for c in calls if c["stage"] == "track1"]
    summary, = hearing_rows(base / "interim/repo_data/cleaned/01_text_summarization/hearing_summaries.parquet")
    t1_saved, = hearing_rows(topics / "track1/topics.parquet")
    t1_prompt = stance.render_track1(summary["summary"])
    assert hashlib.sha256(t1_prompt.encode()).hexdigest() == t1_call["input_sha256"]
    assert t1_call["prompt_version"] == stance.TRACK1_PROMPT_VERSION
    parsed_topics, errors = stance.parse_topics(t1_call["output"])
    assert parsed_topics == json.loads(t1_saved["topics_json"])
    assert ";".join(errors) == t1_saved["errors"]

    selected = [i for i, r in enumerate(raw) if r.get("section") == "spoken" and
                (r.get("is_member") or r.get("bioGuideId") == "0000000")]
    assert selected == [r["turn_idx"] for r in turns]
    removal_totals = Counter()
    by_record = defaultdict(list)
    for row in records:
        by_record[row["turn_idx"]].append({k: row[k] for k in ("sentences", "topic", "stance", "topic_lint")})
    n_calls = 0
    for row in turns:
        idx = row["turn_idx"]
        segmented = stance.segment_turn(raw[idx]["text"])
        cleaned, removed = stance.clean_turn_sentences(segmented, row["surname"], row["honorific"])
        assert cleaned == row["sentences"] and len(cleaned) == row["n_sentences"]
        removal_totals.update(removed)
        speaker = f"{row['honorific'] or ''} {row['surname'] or ''}".strip() or "Unidentified"
        windows = list(stance.windows(cleaned))
        saved_calls = sorted(by_turn[idx], key=lambda c: c["index"])
        assert len(windows) == len(saved_calls)
        extracted, errors = [], []
        for i, ((start, sentences), call) in enumerate(zip(windows, saved_calls)):
            prompt = stance.render_user(sentences, speaker, start=start)
            assert call["index"] == i and call["prompt_version"] == stance.PROMPT_VERSION
            assert hashlib.sha256(prompt.encode()).hexdigest() == call["input_sha256"]
            parsed, flags = stance.parse_records(call["output"], len(sentences), start=start)
            extracted.extend(parsed)
            errors.extend(flags)
        merged, n_merged = stance.merge_adjacent_records(extracted)
        assert merged == by_record[idx]
        assert len(merged) == status[idx]["n_records"]
        assert n_merged == status[idx]["n_merged"]
        assert ";".join(errors) == status[idx]["errors"]
        n_calls += len(saved_calls)
    assert n_calls + 1 == len(calls)
    print(f"Verified {len(turns)} cleaned turns, {len(calls)} user-prompt hashes, and {len(records)} stance records.", flush=True)

    # Reconstruct Track-1 category membership from saved clusters and the exact
    # DROP/MERGE decisions, without executing notebook model-loading cells.
    notebook = json.loads((ROOT / "B - Backup of Original File Structure/scripts/python/03_topic_extraction/10_codebook_freeze_assign.ipynb").read_text())
    decisions = {}
    for node in ast.parse("".join(notebook["cells"][2]["source"])).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in {"DROP", "MERGE", "RELABEL"}:
            decisions[node.targets[0].id] = ast.literal_eval(node.value)
    phrases = {r["key"]: r for r in pq.read_table(tax / "phrases.parquet").to_pylist()}
    cuts = {r["family_id"]: r for r in pq.read_table(tax / "cut_labels.parquet").to_pylist()}
    codebook = pq.read_table(tax / "codebook_v1.parquet").to_pylist()
    labels = {r["topic_id"]: r["label"] for r in codebook}
    t1_assigned = sorted(hearing_rows(tax / "track1_assigned.parquet"), key=lambda r: r["rank"])
    for row in t1_assigned:
        phrase = phrases[row["phrase"].casefold().strip()]
        cluster = cuts[phrase["family_id"]]["K150"]
        tid = -1 if cluster in decisions["DROP"] else decisions["MERGE"].get(cluster, [cluster])[0]
        assert tid == row["topic_id"] and labels[tid] == row["topic_label"]
    primary, = hearing_rows(tax / "hearing_topics_v1.parquet")
    counts = Counter(r["topic_id"] for r in t1_assigned if r["topic_id"] >= 0)
    assert primary["n"] == counts[primary["topic_id"]] == max(counts.values())
    for row in records:
        assert (row["sim"] >= 0.68) == (row["topic_id"] >= 0)
        assert row["topic_label"] == labels.get(row["topic_id"], "other")
    assert not hearing_rows(topics / "taxonomy_v0/cap_match.parquet")

    out = Path(__file__).resolve().parents[1]
    inputs = out / "01 - Inputs"
    outputs = out / "02 - Outputs"
    logs = out / "03 - Logs and Verification"
    for directory in (inputs, outputs, logs):
        directory.mkdir(parents=True, exist_ok=True)
    def write_json(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_json(outputs / "topics.json", {"packageId": PACKAGE, "extracted": parsed_topics, "assigned": t1_assigned, "primary": primary})
    write_json(outputs / "stance_records.json", records)
    write_json(outputs / "codebook.json", codebook)
    (logs / "call_log.jsonl").write_text("".join(log_lines), encoding="utf-8")
    text = ["# Numbered legislator turns\n\nSaved cleaned inputs for `CHRG-115shrg37801`. "
            "Turn IDs are zero-based indices in the [original parsed records](<../../../T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/parsed_turns.json>); "
            "sentence numbers start at one within each cleaned turn. Turns longer than 40 sentences are sent in consecutive windows.\n"]
    for row in turns:
        idx = row["turn_idx"]
        text.append(f"\n## Turn {idx}\n\n{row['honorific']} {row['surname']}; "
                    f"speaker ID `{row['bioGuideId']}`; {row['n_sentences']} sentences; "
                    f"{status[idx]['n_records']} saved stance records. "
                    f"Parser errors: `{status[idx]['errors'] or 'none'}`.\n\n"
                    f"```text\n{stance.format_numbered(row['sentences'])}\n```\n")
    (inputs / "numbered_turns.md").write_text("".join(text), encoding="utf-8")
    numbered = {r["turn_idx"]: r["sentences"] for r in turns}
    text = ["# Recorded stance outputs and supporting sentences\n\n"
            "All 49 accepted records, including the eight assigned to `other`. "
            "Topic wording, stance, evidence indices, similarity, and category come from the saved production tables; "
            "the cited sentences are retrieved from the saved cleaned inputs. "
            "These records include model and category-assignment errors; they have not been editorially corrected.\n"]
    for row in records:
        idx, ri = row["turn_idx"], row["record_idx"]
        text.append(f"\n## Turn {idx}, record {ri}\n\n{row['honorific']} {row['surname']}: "
                    f"**{row['stance']}** toward **{row['topic']}**. "
                    f"Category `{row['topic_id']}`: {row['topic_label']}; "
                    f"cosine similarity {row['sim']:.6f}; wording flag: `{row['topic_lint'] or 'none'}`. "
                    f"[Full turn](<../01 - Inputs/numbered_turns.md#turn-{idx}>).\n\n```text\n")
        text.extend(f"[{i}] {numbered[idx][i-1]}\n" for i in row["sentences"])
        text.append("```\n")
    (outputs / "stance_records.md").write_text("".join(text), encoding="utf-8")
    example = next(r for r in turns if r["turn_idx"] == 772)
    user = stance.render_user(example["sentences"], "Senator Hassan")
    (inputs / "prompts.md").write_text(
        "# Verified example prompts\n\nThe user prompts below reproduce the hashes in "
        "[the saved call log](<../03 - Logs and Verification/call_log.jsonl>). The shared system prompt is copied from the production helper.\n\n"
        f"## System prompt\n\n```text\n{stance.SYSTEM}\n```\n\n"
        f"## Track 1: hearing summary\n\nVersion `{stance.TRACK1_PROMPT_VERSION}`.\n\n```text\n{t1_prompt}\n```\n\n"
        f"## Track 2: Senator Hassan, turn 772\n\nVersion `{stance.PROMPT_VERSION}`.\n\n```text\n{user}\n```\n",
        encoding="utf-8")
    panel = Counter((r["topic_id"], r["topic_label"], r["stance"]) for r in records if r["topic_id"] >= 0)
    write_json(logs / "verification.json", {
        "packageId": PACKAGE, "data_root": str(base), "model": t1_call["model"],
        "selected_turns": len(turns), "cleaned_sentences": sum(r["n_sentences"] for r in turns),
        "removed_sentences_by_rule": dict(removal_totals), "verified_user_prompt_hashes": len(calls),
        "track2_calls": n_calls, "stance_records": len(records),
        "turns_with_stances": len({r["turn_idx"] for r in records}),
        "parser_errors": dict(Counter(e for r in status.values() for e in r["errors"].split(";") if e)),
        "merged_records": sum(r["n_merged"] for r in status.values()),
        "assigned_stance_records": sum(r["topic_id"] >= 0 for r in records),
        "codebook_topics": len(codebook), "codebook_themes": len({r["theme_id"] for r in codebook}),
        "codebook_parquet_sha256": hashlib.sha256((tax / "codebook_v1.parquet").read_bytes()).hexdigest(),
        "codebook_dropped_clusters": len(decisions["DROP"]), "codebook_merged_clusters": len(decisions["MERGE"]),
        "hearing_contributions_to_115th_congress": [
            {"topic_id": k[0], "topic_label": k[1], "stance": k[2], "n": v} for k, v in sorted(panel.items())],
        "cap_match": None,
        "verification_scope": "Reproduced turn selection, sentence cleaning, all extraction user prompts, parsing and merging, and Track-1 cluster membership. Checked saved Track-2 labels and the 0.68 threshold; did not rerun embeddings or LLMs."
    })
    print(f"Exported verified example to {out}")


if __name__ == "__main__":
    main()
