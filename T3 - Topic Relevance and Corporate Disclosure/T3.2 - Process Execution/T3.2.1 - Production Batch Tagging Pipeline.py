"""Prepare/run a hearing-linked, all-firm relevance assessment for one topic.

The screen uses all 111 labels; confirmation uses the selected definition only.
A seeded 60-block audit also checks the target topic without screening.
"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "B - Backup of Original File Structure/scripts/python/lib"
sys.path.insert(0, str(LIB))
import tagging as T

DEFAULT_DATA = Path("/project2/mmiric_1435/acroh/llm_method/data")
DEFAULT_RUN = Path("/project2/njia_1089/acroh/data/output/topic68_relevance_20180410")
DEFAULT_MODEL = Path("/scratch2/acroh/projects/llm_method/hf_cache/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
MODEL = "Qwen/Qwen3.5-4B"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=str) + "\n")


def prepare(data_root, run_root, package, topic, n_shards):
    assert n_shards > 0
    config_path = run_root / "config.json"
    if config_path.exists():
        cfg = json.loads(config_path.read_text())
        assert (cfg["packageId"], cfg["topic_id"], cfg["n_shards"]) == (package, topic, n_shards)
        for name, digest in cfg["input_hashes"].items():
            assert sha(run_root / name) == digest, name
        for name, digest in cfg["helper_hashes"].items():
            assert sha(LIB / name) == digest, name
        print(f"Verified existing run: {cfg['n_filings']} filings / {cfg['n_blocks']} blocks.")
        return
    assert not run_root.exists() or not any(run_root.glob("events_*.jsonl"))
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "logs").mkdir(exist_ok=True)
    base = data_root / "interim"
    summaries = pd.read_parquet(base / "repo_data/cleaned/01_text_summarization/hearing_summaries.parquet", filters=[("packageId", "==", package)])
    assert len(summaries) == 1
    hearing_date = pd.Timestamp(summaries.heldDate_first.iloc[0]).date().isoformat()
    primary = pd.read_parquet(base / "topics/taxonomy/hearing_topics_v1.parquet", filters=[("packageId", "==", package)])
    assert len(primary) == 1 and int(primary.topic_id.iloc[0]) == topic, "Topic differs from the saved primary classification."
    cb_path = base / "topics/taxonomy/codebook_v1.parquet"
    cb = pd.read_parquet(cb_path)
    assert len(cb) == 111 and topic in set(cb.topic_id)
    cb.to_parquet(run_root / "codebook.parquet", index=False)
    scores = pd.read_parquet(base / "relevance/scores/firm_topic_scores.parquet")
    scores["score"] = scores.score.astype("float64")
    lengths = scores.drop_duplicates("accessionNo")[["accessionNo", "n_sentences"]].copy()
    lengths["length_decile"] = pd.qcut(lengths.n_sentences, 10, labels=False, duplicates="drop")
    selected_scores = scores[scores.topic_id.eq(topic)].merge(lengths[["accessionNo", "length_decile"]], on="accessionNo", validate="1:1")
    g = selected_scores.groupby("length_decile").score
    selected_scores["standardized_score"] = (selected_scores.score - g.transform("mean")) / g.transform("std")
    meta = pd.read_parquet(base / "repo_data/raw/03_sp500_10k_item1/sp500_10k_item1.parquet", columns=["accessionNo", "companyName", "conm", "filedAt", "filingUrl", "usable"])
    candidates = selected_scores.merge(meta, on="accessionNo", validate="1:1")
    cutoff = pd.Timestamp(hearing_date, tz="UTC")
    candidates = candidates[candidates.usable & candidates.filedAt.lt(cutoff)]
    filings = candidates.sort_values(["filedAt", "accessionNo"]).groupby("gvkey").tail(1).sort_values("gvkey").reset_index(drop=True)
    assert filings.gvkey.is_unique and filings.accessionNo.is_unique
    filings.to_parquet(run_root / "filings.parquet", index=False)
    filings.to_csv(run_root / "embedding_panel.csv", index=False)
    accs = filings.accessionNo.tolist()
    sents = pd.read_parquet(base / "relevance/item1/sentences.parquet", filters=[("accessionNo", "in", accs)])
    blocks = pd.read_parquet(base / "relevance/tagging/blocks.parquet", filters=[("accessionNo", "in", accs)]).sort_values(["accessionNo", "block_idx"]).reset_index(drop=True)
    blocks.insert(0, "block_id", np.arange(len(blocks)))
    blocks["audit"] = blocks.block_id.isin(blocks.sample(min(60, len(blocks)), random_state=1089).block_id)
    assert blocks.n_sentences.sum() == len(sents) == filings.n_sentences.sum()
    for acc, grp in sents.groupby("accessionNo", sort=False):
        assert sorted(grp.sent_idx.tolist()) == list(range(len(grp)))
    sents.to_parquet(run_root / "sentences.parquet", index=False)
    blocks.to_parquet(run_root / "blocks.parquet", index=False)
    inputs = ["codebook.parquet", "filings.parquet", "sentences.parquet", "blocks.parquet"]
    cfg = {"packageId": package, "hearing_title": summaries.title.iloc[0], "hearing_date": hearing_date, "topic_id": topic, "topic_label": cb.set_index("topic_id").loc[topic, "label"], "n_shards": n_shards, "n_filings": len(filings), "n_blocks": len(blocks), "n_sentences": len(sents), "audit_blocks": int(blocks.audit.sum()), "prompt_version": T.PROMPT_VERSION, "design": "all-111-label screen; target-topic-only confirmation; 60 random blocks checked without screening", "source_data": str(data_root), "source_codebook_sha256": sha(cb_path), "input_hashes": {name: sha(run_root / name) for name in inputs}, "helper_hashes": {name: sha(LIB / name) for name in ["tagging.py", "summarize.py"]}}
    write_json(config_path, cfg)
    print(json.dumps(cfg, indent=2), flush=True)


def run_shard(run_root, shard, model_path):
    import fcntl
    import torch
    import transformers
    import summarize as S
    from transformers import AutoModelForCausalLM, AutoTokenizer

    cfg = json.loads((run_root / "config.json").read_text())
    assert 0 <= shard < cfg["n_shards"]
    assert torch.cuda.is_available(), "This run requires the submitted GPU allocation."
    for name, digest in cfg["input_hashes"].items():
        assert sha(run_root / name) == digest, name
    for name, digest in cfg["helper_hashes"].items():
        assert sha(LIB / name) == digest, name
    lock = (run_root / f"shard_{shard}.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    path = run_root / f"events_{shard}.jsonl"
    events = [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []
    done = {e["block_id"]: e for e in events}
    assert len(done) == len(events)
    os.environ["HF_HUB_OFFLINE"] = "1"
    torch.set_num_threads(8)
    manifest = {"config_sha256": sha(run_root / "config.json"), "model": MODEL, "snapshot": str(model_path), "dtype": "bfloat16", "torch": torch.__version__, "transformers": transformers.__version__, "gpu": torch.cuda.get_device_name(), "generation": S.GENERATION, "prompt_version": T.PROMPT_VERSION, "slurm_job_id": os.environ.get("SLURM_JOB_ID"), "shard": shard}
    mp = run_root / f"runtime_{shard}.json"
    if mp.exists():
        old = json.loads(mp.read_text())
        assert all(old[k] == manifest[k] for k in ["config_sha256", "model", "snapshot", "dtype", "generation", "prompt_version", "torch", "transformers"])
    else:
        write_json(mp, manifest)
    codebook = pd.read_parquet(run_root / "codebook.parquet")
    labels, valid_ids = T.format_topic_labels(codebook)
    target_entries, target_ids = T.format_topic_entries(codebook, [cfg["topic_id"]])
    blocks = pd.read_parquet(run_root / "blocks.parquet")
    work = blocks[blocks.block_id.mod(cfg["n_shards"]).eq(shard)]
    sents = pd.read_parquet(run_root / "sentences.parquet", filters=[("accessionNo", "in", work.accessionNo.unique().tolist())])
    by_acc = {a: g.set_index("sent_idx").sentence.sort_index() for a, g in sents.groupby("accessionNo")}
    if set(work.block_id) == set(done):
        print(f"Shard {shard} already complete.", flush=True)
        return
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, dtype=torch.bfloat16, device_map="cuda", local_files_only=True).eval()

    def call(row, stage, user, cap):
        doc = f"{row.accessionNo}:{row.block_idx}"
        seed = int.from_bytes(hashlib.sha256(f"{doc}:{stage}".encode()).digest()[:8], "little")
        torch.manual_seed(seed)
        start = time.time()
        output, hit_cap = S._generate(model, tokenizer, T.SYSTEM, user, cap)
        log = S.CallLog(None, doc, MODEL, prompt_version=T.PROMPT_VERSION)
        log.write(stage, 0, int(row.block_idx), int(row.n_sentences), user, output, tokenizer, time.time() - start)
        return log.records[-1] | {"system": T.SYSTEM, "user": user, "seed": seed, "hit_cap": hit_cap}

    for row in work.itertuples(index=False):
        if row.block_id in done:
            continue
        texts = by_acc[row.accessionNo].loc[row.sent_lo:row.sent_hi].tolist()
        start = int(row.sent_lo) + 1
        gate = call(row, "gate", T.render_gate_user(texts, start, labels), T.GATE_MAX_NEW_TOKENS)
        candidates, gate_errors = T.parse_gate_topics(gate["output"], valid_ids)
        calls, tags, errors, audit_tags = [gate], [], list(gate_errors), []
        gated = cfg["topic_id"] in candidates
        if gated or row.audit:
            stage = "confirm" if gated else "audit"
            confirmation = call(row, stage, T.render_confirm_user(texts, start, target_entries), T.CONFIRM_MAX_NEW_TOKENS)
            calls.append(confirmation)
            parsed, confirm_errors = T.parse_topic_tags(confirmation["output"], target_ids, start, len(texts))
            if gated:
                tags = parsed
                errors.extend(confirm_errors)
            if row.audit:
                audit_tags = parsed
        else:
            confirm_errors = []
        event = {"block_id": int(row.block_id), "accessionNo": row.accessionNo, "block_idx": int(row.block_idx), "candidates": candidates, "target_gated": gated, "tags": tags, "errors": errors, "audit": bool(row.audit), "audit_tags": audit_tags, "audit_errors": confirm_errors if row.audit else [], "calls": calls}
        with path.open("a") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            stream.flush()
        done[row.block_id] = event
        if len(done) % 25 == 0 or len(done) == len(work):
            print(f"shard {shard}: {len(done)}/{len(work)} blocks; last target tags {len(tags)}", flush=True)
    assert set(work.block_id) == set(done)
    print(f"COMPLETE shard {shard}: {len(done)} blocks", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("stage", choices=["prepare", "run"])
    p.add_argument("--data-root", type=Path, default=DEFAULT_DATA)
    p.add_argument("--run-root", type=Path, default=DEFAULT_RUN)
    p.add_argument("--package", default="CHRG-115shrg37801")
    p.add_argument("--topic", type=int, default=68)
    p.add_argument("--n-shards", type=int, default=4)
    p.add_argument("--shard", type=int, default=int(os.environ.get("SLURM_ARRAY_TASK_ID", "0")))
    p.add_argument("--model-path", type=Path, default=DEFAULT_MODEL)
    a = p.parse_args()
    if a.stage == "prepare": prepare(a.data_root, a.run_root, a.package, a.topic, a.n_shards)
    else: run_shard(a.run_root, a.shard, a.model_path)
