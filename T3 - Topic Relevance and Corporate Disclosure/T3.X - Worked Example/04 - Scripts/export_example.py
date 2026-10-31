"""Export and verify the Zuckerberg relevance example from saved data.

Prepare exports source text and checks existing embeddings. Export reads the
completed all-firm topic run, including two illustrations and all-firm results.
No language-model generation occurs in this script.
"""

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
LIB = ROOT / "B - Backup of Original File Structure/scripts/python/lib"
sys.path.insert(0, str(LIB))
import tagging as T

PACKAGE = "CHRG-115shrg37801"
HEARING_DATE = "2018-04-10"
TOPIC = 68
INPUTS = OUT / "01 - Inputs"
SOURCES = INPUTS / "Source Filings"
OUTPUTS = OUT / "02 - Outputs"
FULL_SAMPLE = OUTPUTS / "01 - Full Sample"
CASES = OUTPUTS / "02 - Worked Cases"
EVALUATION = OUTPUTS / "03 - Evaluation and Figures"
LOGS = OUT / "03 - Logs and Verification"


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=str) + "\n")


def load(path):
    return json.loads(path.read_text())


def prepare(base):
    for p in (INPUTS, SOURCES, FULL_SAMPLE, CASES, EVALUATION, LOGS):
        p.mkdir(parents=True, exist_ok=True)
    interim = base / "interim"
    rel = interim / "relevance"
    raw_path = interim / "repo_data/raw/03_sp500_10k_item1/sp500_10k_item1.parquet"
    columns = ["accessionNo", "cik", "gvkey", "companyName", "conm", "fyear", "filedAt", "usable", "filingUrl"]
    meta = pd.read_parquet(raw_path, columns=columns)
    prior = meta[meta.usable & meta.filedAt.lt(pd.Timestamp(HEARING_DATE, tz="UTC"))]
    latest = prior.sort_values(["filedAt", "accessionNo"]).groupby("cik").tail(1)
    firms = latest[latest.cik.isin(["1326801", "943819"])].sort_values("cik")
    assert len(firms) == 2
    accs = firms.accessionNo.tolist()
    raw = pd.read_parquet(raw_path, filters=[("accessionNo", "in", accs)])
    sentences = pd.read_parquet(rel / "item1/sentences.parquet", filters=[("accessionNo", "in", accs)])
    blocks = pd.read_parquet(rel / "tagging/blocks.parquet", filters=[("accessionNo", "in", accs)])
    cb_path = interim / "topics/taxonomy/codebook_v1.parquet"
    codebook = pd.read_parquet(cb_path)
    dump(INPUTS / "codebook.json", codebook.to_dict("records"))
    dump(INPUTS / "filings.json", firms.to_dict("records"))
    records, numbered = [], ["# Numbered filing sentences", "", "Display numbers are the saved, filtered sent_idx + 1. Blocks retain document order.", ""]
    for firm in firms.itertuples():
        acc = firm.accessionNo
        text = raw.loc[raw.accessionNo.eq(acc), "item1"].iloc[0]
        (SOURCES / f"{acc}_source.txt").write_text(text)
        grp = sentences[sentences.accessionNo.eq(acc)].sort_values("sent_idx")
        assert grp.sent_idx.tolist() == list(range(len(grp)))
        numbered += [f"## {firm.companyName} — fiscal year {firm.fyear}", "", f"Accession: `{acc}`. Filed: {firm.filedAt}.", ""]
        for b in blocks[blocks.accessionNo.eq(acc)].sort_values("block_idx").itertuples():
            sents = grp[grp.sent_idx.between(b.sent_lo, b.sent_hi)].sentence.tolist()
            assert len(sents) == b.n_sentences and len(sents) <= T.BLOCK_SENTENCES
            records.append({"accessionNo": acc, "block_idx": b.block_idx, "start": b.sent_lo + 1, "sentences": sents})
            numbered += [f'<a id="{acc}-block-{b.block_idx}"></a>', f"### Block {b.block_idx}: sentences {b.sent_lo + 1}–{b.sent_hi + 1}", "", "```text", T.format_numbered(sents, b.sent_lo + 1), "```", ""]
    dump(INPUTS / "blocks.json", records)
    (INPUTS / "numbered_sentences.md").write_text("\n".join(numbered))

    scores = pd.read_parquet(rel / "scores/firm_topic_scores.parquet")
    scores["score"] = scores.score.astype("float64")
    lengths = scores.drop_duplicates("accessionNo")[["accessionNo", "n_sentences"]].copy()
    lengths["length_decile"] = pd.qcut(lengths.n_sentences, 10, labels=False, duplicates="drop")
    scores = scores.merge(lengths[["accessionNo", "length_decile"]], on="accessionNo", validate="m:1")
    scores = scores[scores.topic_id.eq(TOPIC)].copy()
    g = scores.groupby("length_decile").score
    scores["standardized_score"] = (scores.score - g.transform("mean")) / g.transform("std")
    snapshot = latest.merge(scores, on=["accessionNo", "cik", "gvkey", "fyear"], validate="1:1").sort_values("score", ascending=False)
    snapshot.to_csv(FULL_SAMPLE / "privacy_firm_scores_before_hearing.csv", index=False)
    example = firms.merge(scores, on=["accessionNo", "cik", "gvkey", "fyear"], validate="1:1")
    evidence = pd.read_parquet(rel / "scores/evidence_sentences.parquet", filters=[("accessionNo", "in", accs), ("topic_id", "==", TOPIC)])
    evidence = evidence.merge(sentences, on=["accessionNo", "sent_idx"], validate="m:1").sort_values(["accessionNo", "rank"])
    evidence["sentence_number"] = evidence.sent_idx + 1
    dump(CASES / "embedding_scores.json", example.to_dict("records"))
    dump(CASES / "embedding_evidence.json", evidence.to_dict("records"))

    # Recompute the example scores from the existing row-aligned vectors.
    acc_index = pd.read_parquet(rel / "item1/sentences.parquet", columns=["accessionNo"])
    embeddings = np.load(rel / "item1/emb_bge-large-en-v1.5.npy", mmap_mode="r")
    topic_index = pd.read_parquet(rel / "scores/topic_index.parquet")
    centers = np.load(rel / "scores/topic_centroids_bge-large-en-v1.5.npy")
    ti = topic_index.index[topic_index.topic_id.eq(TOPIC)].item()
    center = centers[ti].astype(np.float32)
    checks = []
    for row in example.itertuples():
        idx = np.flatnonzero(acc_index.accessionNo.eq(row.accessionNo).to_numpy())
        sims = embeddings[idx].astype(np.float32) @ center
        best = np.argsort(-sims)[:5]
        ev = evidence[evidence.accessionNo.eq(row.accessionNo)].sort_values("rank")
        assert best.tolist() == ev.sent_idx.tolist()
        assert np.allclose(sims[best], ev.cosine.to_numpy(), atol=2e-6, rtol=0)
        assert np.isclose(sims[best].mean(), row.score, atol=2e-6, rtol=0)
        checks.append({"accessionNo": row.accessionNo, "saved_score": row.score, "recomputed_score": float(sims[best].mean()), "top_five_indices_match": True})
    dump(LOGS / "embedding_verification.json", {"packageId": PACKAGE, "hearing_date": HEARING_DATE, "topic_id": TOPIC, "topic_evidence_sentences": int(topic_index.loc[ti, "n_evidence"]), "preceding_filings": len(snapshot), "codebook_sha256": hashlib.sha256(cb_path.read_bytes()).hexdigest(), "checks": checks})
    (INPUTS / "prompts.md").write_text(f"# Relevance prompts\n\nVersion: `{T.PROMPT_VERSION}`. Templates are imported from the original tagging helper. Each executed call stores its full rendered prompt in the call log.\n\n## System\n\n```text\n{T.SYSTEM}\n```\n\n## Pass A: topic screen\n\n```text\n{T.GATE_USER}\n```\n\n## Pass B: confirmation and direction\n\n```text\n{T.CONFIRM_USER}\n```\n")
    print(f"Prepared {len(records)} blocks, {len(sentences)} sentences, {len(snapshot)} preceding-filing privacy scores.", flush=True)



def export_run(run_root):
    import shutil
    for p in (FULL_SAMPLE, CASES, EVALUATION, LOGS):
        p.mkdir(parents=True, exist_ok=True)
    assessment = load(run_root / "outputs/assessment.json")
    assert assessment["status"] == "complete"
    panel = pd.read_parquet(run_root / "outputs/hearing_firm_privacy_panel.parquet")
    assert len(panel) == assessment["firms"] == 998
    tags = pd.read_parquet(run_root / "outputs/privacy_tags.parquet")
    firms = load(INPUTS / "filings.json")
    accs = {r["accessionNo"] for r in firms}
    subset = tags[tags.accessionNo.isin(accs)].copy()
    sample_panel = panel[panel.accessionNo.isin(accs)]
    clean_panel = sample_panel.astype(object).where(pd.notna(sample_panel), None)
    dump(CASES / "privacy_aggregates.json", clean_panel.to_dict("records"))
    dump(CASES / "privacy_tags.json", subset.to_dict("records"))
    calls = []
    events = []
    for p in sorted(run_root.glob("events_*.jsonl")):
        with p.open() as stream:
            for line in stream:
                e = json.loads(line)
                if e["accessionNo"] in accs:
                    events.append(e)
                    calls.extend(e["calls"])
    cb = pd.DataFrame(load(INPUTS / "codebook.json"))
    labels, ids = T.format_topic_labels(cb)
    entries, topic_ids = T.format_topic_entries(cb, [TOPIC])
    blocks = {(b["accessionNo"], b["block_idx"]): b for b in load(INPUTS / "blocks.json")}
    assert len(events) == len(blocks) == 15
    for e in events:
        b = blocks[(e["accessionNo"], e["block_idx"])]
        for c in e["calls"]:
            prompt = T.render_gate_user(b["sentences"], b["start"], labels) if c["stage"] == "gate" else T.render_confirm_user(b["sentences"], b["start"], entries)
            assert c["user"] == prompt
            assert c["input_sha256"] == hashlib.sha256(prompt.encode()).hexdigest()
    (LOGS / "call_log.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in calls))
    dump(LOGS / "verification.json", {"source_run": str(run_root), "all_firm_assessment": assessment, "example_blocks": len(events), "example_calls_verified": len(calls)})
    dump(LOGS / "full_run_config.json", load(run_root / "config.json"))
    shutil.copy2(run_root / "outputs/hearing_firm_privacy_panel.csv", FULL_SAMPLE / "hearing_firm_privacy_panel.csv")
    shutil.copy2(run_root / "outputs/assessment.json", EVALUATION / "assessment.json")
    shutil.copy2(run_root / "outputs/human_review_candidates.csv", EVALUATION / "human_review_candidates.csv")
    shutil.copy2(run_root / "outputs/privacy_agreement_quintiles.csv", EVALUATION / "privacy_agreement_quintiles.csv")
    quintiles = pd.read_csv(EVALUATION / "privacy_agreement_quintiles.csv")
    fig_dir = ROOT / "R - Results/figures/T3 - Topic Relevance and Corporate Disclosure"
    for ext in ["svg", "pdf", "png"]:
        shutil.copy2(run_root / f"outputs/privacy_measure_agreement.{ext}", fig_dir / f"fig_privacy_measure_agreement.{ext}")
    lines = ["# Privacy relevance records", "", "New Qwen classifications from the all-firm topic run. Human validation remains separate.", ""]
    for firm in sample_panel.to_dict("records"):
        acc = firm["accessionNo"]
        lines += [f"## {firm['companyName']}", "", f"Accession `{acc}`; {firm['relevant_sentences']} accepted sentences: {firm['opportunity']} opportunity, {firm['threat']} threat, {firm['neutral']} neutral. Flagged blocks: {firm['flagged_blocks']}.", ""]
        for t in subset[subset.accessionNo.eq(acc)].sort_values("sent_idx").to_dict("records"):
            lines += [f'<a id="{acc}-sentence-{t["sentence_number"]}"></a>', f"### Sentence {t['sentence_number']} — {t['direction']}", "", t["sentence"], ""]
    (CASES / "privacy_records.md").write_text("\n".join(lines))
    publish_results(assessment, sample_panel, subset, quintiles)
    print(f"Exported {len(panel)} firms; verified {len(calls)} calls in the two illustrations.")


def replace_marked(path, start, end, text):
    """Only replace the explicitly marked generated passage; preserve other edits."""
    original = path.read_text()
    assert original.count(start) == original.count(end) == 1, f"Missing/duplicate markers in {path}"
    left = original.index(start) + len(start)
    right = original.index(end, left)
    path.write_text(original[:left] + "\n" + text.rstrip() + "\n" + original[right:])


def publish_results(a, sample, tags, quintiles):
    prefix = "../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/"
    text = [
        f"The completed privacy run covers **{a['firms']:,} firms and {a['blocks_verified']:,} blocks**, with {a['calls_verified']:,} model calls verified against their recorded prompts. It retains **{a['privacy_sentence_tags']:,} privacy sentence–topic records**. At least one record is retained for **{a['firms_related']:,} firms**; {a['firms_without_confirmed_relevance']:,} receive a zero indicator and {a['firms_unknown']:,} remain unknown under the processing-quality rule. The run records {a['cap_hits']:,} generation-cap hits; {a['firms_with_flagged_calls']:,} filings have flagged calls and remain identifiable for review.",
        "", "The two illustrations contribute the following model classifications:", "",
        "| Firm | Accepted privacy sentences | Opportunity | Threat | Neutral | Flagged blocks |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in sample.itertuples():
        text.append(f"| {r.companyName} | {r.relevant_sentences} | {r.opportunity} | {r.threat} | {r.neutral} | {r.flagged_blocks} |")
    text += ["", f"The [sentence-level classifications](<{prefix}02 - Outputs/02 - Worked Cases/privacy_records.md>) retain the original text, and the [full firm table](<{prefix}02 - Outputs/01 - Full Sample/hearing_firm_privacy_panel.csv>) supplies the corresponding measures for every selected firm. Directional shares divide each direction's count by the accepted total; counts from flagged filings require review before being treated as complete."]
    for acc, name in [("0001326801-18-000009", "Facebook"), ("0001193125-17-248016", "ResMed")]:
        subset = tags[tags.accessionNo.eq(acc)]
        if len(subset):
            chosen = subset.loc[subset.sentence.str.len().idxmin()]
            anchor = f"{prefix}02 - Outputs/02 - Worked Cases/privacy_records.md#{acc}-sentence-{chosen.sentence_number}"
            text += ["", f"For {name}, the model classifies [sentence {chosen.sentence_number}](<{anchor}>) as **{chosen.direction}**: “{chosen.sentence}” This is a recorded model judgment whose interpretation can be checked against the surrounding input block."]
    run_text = "\n".join(text)
    text = []
    if a["audit_miss_rate"] is None:
        audit = "No usable audit block contained a directly confirmed privacy tag, so the screening miss rate is undefined."
    else:
        audit = f"Privacy is directly confirmed in {a['audit_confirmed_blocks']} usable audit blocks; the screen missed {a['audit_missed_blocks']} of these, a miss rate of {a['audit_miss_rate']:.1%}."
    text += [f"In the {a['audit_blocks']}-block screening audit, {a['audit_invalid_blocks']} blocks have structural or cap problems. {audit} These are comparisons between model procedures, not human accuracy estimates."]
    assert quintiles.firms.sum() == a["agreement_firms_without_flagged_calls"]
    low, high = quintiles.iloc[0], quintiles.iloc[-1]
    text += ["", f"The agreement figure asks whether higher embedding similarity is accompanied by privacy evidence from the separate LLM procedure. It uses {a['agreement_firms_without_flagged_calls']:,} filings without flagged calls. The left panel compares similarity between filings with and without accepted tags. The right panel orders firms by standardized similarity, divides them into five approximately equal groups, and shows the percentage in each group with at least one accepted privacy tag. This percentage uses firms as its denominator, not sentences. In the lowest-similarity group, {int(low.firms_with_tags)} of {int(low.firms)} firms have tags ({low.firms_with_tags_percent:.1f}%); in the highest group, {int(high.firms_with_tags)} of {int(high.firms)} do ({high.firms_with_tags_percent:.1f}%). These bars show how often similarity is accompanied by a model-retained passage. Similarity remains a continuous score; the LLM supplies specific sentences and their directional labels. A tag can indicate threat, opportunity, or neutral relevance. The figure assesses correspondence, while the directional figures in Section 5.3 examine what the LLM adds about implications. Independent human validation remains incomplete.", "",
             "![Privacy similarity and LLM evidence across firms](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_measure_agreement.svg>)", "",
             f"*Privacy-measure agreement. Each observation is one firm's latest available filing before April 10, 2018. Left: boxes show the middle 50 percent and median of standardized similarity, with whiskers extending to observations within 1.5 interquartile ranges and more distant points hidden. Similarity is standardized within topic and filing-length decile. Right: bars show the fraction of firms with any accepted privacy tag within each similarity quintile, expressed as a percentage; the denominator is all firms in that quintile. Quintiles are defined using similarity alone. The [group counts and score ranges](<{prefix}02 - Outputs/03 - Evaluation and Figures/privacy_agreement_quintiles.csv>) reproduce the bars. Filings with flagged calls are excluded. Absence of a tag is a model outcome, not proof of irrelevance; neither panel establishes classification accuracy or economic effects.*"]
    manuscript = ROOT / "W - Writing and Drafts/Proposal_for_Org_Sci_092126_AR.md"
    replace_marked(manuscript, "<!-- TOPIC68_RUN_STATUS_START -->", "<!-- TOPIC68_RUN_STATUS_END -->", run_text)
    replace_marked(manuscript, "<!-- TOPIC68_EVALUATION_START -->", "<!-- TOPIC68_EVALUATION_END -->", "\n".join(text))
    status = f"The full run is complete: **{a['firms']:,} firms, {a['blocks_verified']:,} blocks, and {a['calls_verified']:,} verified calls**. It retains {a['privacy_sentence_tags']:,} privacy tags. See the [all-firm panel](<02 - Outputs/01 - Full Sample/hearing_firm_privacy_panel.csv>), [assessment](<02 - Outputs/03 - Evaluation and Figures/assessment.json>), and [two illustrations](<02 - Outputs/02 - Worked Cases/privacy_records.md>). Processing flags remain visible; independent human validation is not yet complete."
    replace_marked(OUT / "README.md", "<!-- RUN_STATUS_START -->", "<!-- RUN_STATUS_END -->", status)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["prepare", "export"])
    parser.add_argument("--data-root", type=Path, default=Path("/project2/mmiric_1435/acroh/llm_method/data"))
    parser.add_argument("--run-root", type=Path, default=Path("/project2/njia_1089/acroh/data/output/topic68_relevance_20180410"))
    args = parser.parse_args()
    if args.stage == "prepare": prepare(args.data_root)
    else: export_run(args.run_root)
