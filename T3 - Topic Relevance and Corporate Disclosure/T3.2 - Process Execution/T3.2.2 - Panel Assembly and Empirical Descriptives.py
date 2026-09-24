"""Verify complete tagging shards, aggregate evidence, and link to the hearing.

Refuses to publish a panel until every scheduled block is present. A filing with
flagged/capped calls and no accepted tags has unknown relevance, not a false zero.
Audit tags remain separate from screened production tags.
"""

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "B - Backup of Original File Structure/scripts/python/lib"
sys.path.insert(0, str(LIB))
import tagging as T

DEFAULT_RUN = Path("/project2/njia_1089/acroh/data/output/topic68_relevance_20180410")


def agreement_quintiles(panel):
    """Summarize tag presence within five groups defined only by similarity."""
    usable = panel.loc[panel.flagged_blocks.eq(0)].copy()
    assert usable.standardized_score.notna().all()
    assert usable.llm_related.isin([0, 1]).all()
    usable["similarity_quintile"] = pd.qcut(usable.standardized_score, 5, labels=False) + 1
    summary = usable.groupby("similarity_quintile").agg(
        firms=("accessionNo", "size"), firms_with_tags=("llm_related", "sum"),
        similarity_min=("standardized_score", "min"), similarity_max=("standardized_score", "max"),
    ).reset_index()
    summary["firms_with_tags_percent"] = 100 * summary.firms_with_tags / summary.firms
    assert summary.firms.sum() == len(usable)
    assert summary.firms_with_tags.sum() == usable.llm_related.sum()
    return summary


def render_agreement(panel, out):
    """Rebuild the agreement figure and its grouped data from the saved panel."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import findfont

    findfont("Times New Roman", fallback_to_default=False)
    usable = panel.loc[panel.flagged_blocks.eq(0)]
    summary = agreement_quintiles(panel)
    summary.to_csv(out / "privacy_agreement_quintiles.csv", index=False)
    with plt.rc_context({"font.family": "Times New Roman", "font.size": 11,
                         "svg.fonttype": "none", "pdf.fonttype": 42}):
        fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.3))
        groups = [usable.loc[usable.llm_related.eq(i), "standardized_score"].to_numpy() for i in (0, 1)]
        axes[0].boxplot(
            groups, tick_labels=[f"No privacy tags\n(n = {len(groups[0])})", f"Privacy tags\n(n = {len(groups[1])})"],
            showfliers=False, patch_artist=True, widths=.5,
            boxprops={"facecolor": "#E5E9EC", "edgecolor": "#003049"},
            medianprops={"color": "#003049", "linewidth": 1.4},
            whiskerprops={"color": "#003049"}, capprops={"color": "#003049"},
        )
        axes[0].set_ylabel("Privacy similarity (standardized)")
        axes[1].bar(summary.similarity_quintile, summary.firms_with_tags_percent, color="#003049", width=.6)
        axes[1].set_xticks([1, 2, 3, 4, 5], ["Lowest", "2", "3", "4", "Highest"])
        axes[1].set_xlabel("Privacy similarity quintile")
        axes[1].set_ylabel("Firms with privacy tags (%)")
        axes[1].set_ylim(0, 100)
        axes[1].set_yticks([0, 25, 50, 75, 100])
        for ax in axes:
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(axis="y", color="#D0D0D0", linewidth=.5)
            ax.set_axisbelow(True)
        fig.tight_layout(pad=.4, w_pad=1.6)
        for ext in ["svg", "pdf", "png"]:
            fig.savefig(out / f"privacy_measure_agreement.{ext}", dpi=180,
                        bbox_inches="tight", pad_inches=.03, facecolor="white")
        plt.close(fig)


def assemble(run_root, figures=True):
    cfg = json.loads((run_root / "config.json").read_text())
    for name, digest in cfg["input_hashes"].items():
        assert hashlib.sha256((run_root / name).read_bytes()).hexdigest() == digest, name
    for name, digest in cfg["helper_hashes"].items():
        assert hashlib.sha256((LIB / name).read_bytes()).hexdigest() == digest, name
    blocks = pd.read_parquet(run_root / "blocks.parquet").set_index("block_id")
    events = []
    for shard in range(cfg["n_shards"]):
        path = run_root / f"events_{shard}.jsonl"
        if path.exists():
            subset = [json.loads(l) for l in path.read_text().splitlines()]
            assert all(e["block_id"] % cfg["n_shards"] == shard for e in subset)
            events.extend(subset)
    event_ids = [e["block_id"] for e in events]
    assert len(event_ids) == len(set(event_ids)), "Duplicated block results."
    assert set(event_ids) == set(blocks.index), f"Incomplete run: {len(event_ids)}/{len(blocks)} blocks. No final panel written."
    sentences = pd.read_parquet(run_root / "sentences.parquet").set_index(["accessionNo", "sent_idx"])
    codebook = pd.read_parquet(run_root / "codebook.parquet")
    labels, valid_ids = T.format_topic_labels(codebook)
    entries, target_ids = T.format_topic_entries(codebook, [cfg["topic_id"]])
    records, audit_records, block_records = [], [], []
    calls, caps, all_errors = 0, 0, Counter()
    audit_checked, audit_invalid, audit_positive, audit_missed = 0, 0, 0, 0
    for e in sorted(events, key=lambda x: x["block_id"]):
        row = blocks.loc[e["block_id"]]
        assert e["accessionNo"] == row.accessionNo and e["block_idx"] == row.block_idx
        assert e["audit"] == bool(row.audit)
        texts = sentences.loc[row.accessionNo].loc[row.sent_lo:row.sent_hi, "sentence"].tolist()
        start = int(row.sent_lo) + 1
        gate, *rest = e["calls"]
        assert gate["stage"] == "gate"
        candidates, errors = T.parse_gate_topics(gate["output"], valid_ids)
        assert candidates == e["candidates"]
        gated = cfg["topic_id"] in candidates
        assert gated == e["target_gated"]
        tags, aud_tags, confirm_errors = [], [], []
        assert len(rest) == int(gated or row.audit)
        if rest:
            confirmation = rest[0]
            assert confirmation["stage"] == ("confirm" if gated else "audit")
            parsed, confirm_errors = T.parse_topic_tags(confirmation["output"], target_ids, start, len(texts))
            if gated:
                tags = parsed
                errors.extend(confirm_errors)
            if row.audit:
                aud_tags = parsed
        assert tags == e["tags"] and errors == e["errors"] and aud_tags == e["audit_tags"]
        assert e["audit_errors"] == (confirm_errors if row.audit else [])
        for c in e["calls"]:
            user = T.render_gate_user(texts, start, labels) if c["stage"] == "gate" else T.render_confirm_user(texts, start, entries)
            assert c["user"] == user and c["system"] == T.SYSTEM
            assert c["input_sha256"] == hashlib.sha256(user.encode()).hexdigest()
            assert c["prompt_version"] == cfg["prompt_version"]
            calls += 1
            caps += int(c["hit_cap"])
        flagged = bool(errors or gate["hit_cap"] or (gated and rest[0]["hit_cap"]))
        all_errors.update(errors)
        block_records.append({"accessionNo": row.accessionNo, "block_idx": int(row.block_idx), "target_gated": gated, "n_tags": len(tags), "flagged": flagged})
        for parsed, destination in [(tags, records), (aud_tags, audit_records)]:
            for tag in parsed:
                destination.append({"accessionNo": row.accessionNo, "block_idx": int(row.block_idx), "sent_idx": tag["sentence"] - 1, "sentence_number": tag["sentence"], "topic_id": tag["topic"], "direction": tag["direction"], "sentence": texts[tag["sentence"] - start]})
        if row.audit:
            audit_checked += 1
            bad = bool(confirm_errors or rest[0]["hit_cap"] or gate["hit_cap"] or T.parse_gate_topics(gate["output"], valid_ids)[1])
            audit_invalid += int(bad)
            if not bad and aud_tags:
                audit_positive += 1
                audit_missed += int(not gated)
    columns = ["accessionNo", "block_idx", "sent_idx", "sentence_number", "topic_id", "direction", "sentence"]
    tags = pd.DataFrame(records, columns=columns)
    assert not tags.duplicated(["accessionNo", "sent_idx", "topic_id"]).any()
    aud = pd.DataFrame(audit_records, columns=columns)
    reports = pd.DataFrame(block_records)
    filings = pd.read_parquet(run_root / "filings.parquet")
    counts = pd.crosstab(tags.accessionNo, tags.direction).reindex(columns=T.DIRECTIONS, fill_value=0)
    panel = filings.merge(counts, left_on="accessionNo", right_index=True, how="left", validate="1:1")
    for d in T.DIRECTIONS:
        panel[d] = panel[d].fillna(0).astype(int)
    qa = reports.groupby("accessionNo").agg(processed_blocks=("block_idx", "size"), flagged_blocks=("flagged", "sum"), gated_blocks=("target_gated", "sum"))
    panel = panel.merge(qa, on="accessionNo", validate="1:1")
    panel["relevant_sentences"] = panel[list(T.DIRECTIONS)].sum(axis=1)
    panel["llm_related"] = panel.relevant_sentences.gt(0).astype("Int64")
    panel.loc[panel.flagged_blocks.gt(0) & panel.relevant_sentences.eq(0), "llm_related"] = pd.NA
    for d in T.DIRECTIONS:
        panel[d + "_share"] = panel[d] / panel.relevant_sentences.replace(0, float("nan"))
    panel["relevant_sentence_share"] = panel.relevant_sentences / panel.n_sentences
    panel["packageId"] = cfg["packageId"]
    panel["hearing_date"] = cfg["hearing_date"]
    panel["filing_age_days"] = (pd.Timestamp(cfg["hearing_date"], tz="UTC") - panel.filedAt).dt.days
    assert panel.filing_age_days.ge(0).all()
    assert len(panel) == cfg["n_filings"] and panel.gvkey.is_unique
    assert panel.relevant_sentences.le(panel.n_sentences).all()
    usable = panel[panel.flagged_blocks.eq(0)]
    rho = usable.standardized_score.corr(usable.relevant_sentence_share, method="spearman") if len(usable) > 1 else float("nan")
    assessment = {"status": "complete", "firms": len(panel), "blocks_verified": len(events), "calls_verified": calls, "cap_hits": caps, "parser_flags": dict(all_errors), "firms_with_flagged_calls": int(panel.flagged_blocks.gt(0).sum()), "firms_related": int(panel.llm_related.eq(1).sum()), "firms_without_confirmed_relevance": int(panel.llm_related.eq(0).sum()), "firms_unknown": int(panel.llm_related.isna().sum()), "privacy_sentence_tags": len(tags), "directions": tags.direction.value_counts().to_dict(), "audit_blocks": audit_checked, "audit_invalid_blocks": audit_invalid, "audit_confirmed_blocks": audit_positive, "audit_missed_blocks": audit_missed, "audit_miss_rate": audit_missed / audit_positive if audit_positive else None, "spearman_standardized_similarity_vs_sentence_share": None if pd.isna(rho) else float(rho), "agreement_firms_without_flagged_calls": len(usable), "filings_older_than_two_years": int(panel.filing_age_days.gt(730).sum()), "human_validation": "not completed"}
    out = run_root / "outputs"; out.mkdir(exist_ok=True)
    tags.to_parquet(out / "privacy_tags.parquet", index=False)
    aud.to_parquet(out / "audit_tags.parquet", index=False)
    reports.to_parquet(out / "block_results.parquet", index=False)
    panel.to_parquet(out / "hearing_firm_privacy_panel.parquet", index=False)
    panel.to_csv(out / "hearing_firm_privacy_panel.csv", index=False)
    (out / "assessment.json").write_text(json.dumps(assessment, indent=2) + "\n")
    # Blank fields are for independent human review, never filled by this code.
    gold = tags.sample(min(100, len(tags)), random_state=1089).copy()
    gold["kind"] = "confirmed_tag"
    neg = reports[reports.target_gated & reports.n_tags.eq(0) & ~reports.flagged].sample(n=min(50, int((reports.target_gated & reports.n_tags.eq(0) & ~reports.flagged).sum())), random_state=1089)
    probes = []
    for r in neg.itertuples():
        b = blocks[(blocks.accessionNo == r.accessionNo) & (blocks.block_idx == r.block_idx)].iloc[0]
        idx = (int(b.sent_lo) + int(b.sent_hi)) // 2
        probes.append({"accessionNo": r.accessionNo, "block_idx": r.block_idx, "sent_idx": idx, "sentence_number": idx + 1, "topic_id": cfg["topic_id"], "direction": "", "sentence": sentences.loc[(r.accessionNo, idx), "sentence"], "kind": "unconfirmed_probe"})
    gold = pd.concat([gold, pd.DataFrame(probes)], ignore_index=True)
    review_meta = [c for c in ["accessionNo", "companyName", "gvkey", "fyear", "filedAt", "filingUrl"] if c in filings.columns]
    gold = gold.merge(filings[review_meta], on="accessionNo", how="left", validate="m:1")
    gold["topic_definition"] = codebook.set_index("topic_id").loc[cfg["topic_id"], "definition"]
    contexts = []
    for r in gold.itertuples():
        b = blocks[(blocks.accessionNo == r.accessionNo) & (blocks.block_idx == r.block_idx)].iloc[0]
        texts = sentences.loc[r.accessionNo].loc[b.sent_lo:b.sent_hi, "sentence"].tolist()
        contexts.append(T.format_numbered(texts, int(b.sent_lo) + 1))
    gold["numbered_block_context"] = contexts
    gold["verified_relevance"] = ""; gold["verified_direction"] = ""
    gold.to_csv(out / "human_review_candidates.csv", index=False)
    if figures:
        render_agreement(panel, out)
    print(json.dumps(assessment, indent=2), flush=True)
    return assessment


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-root", type=Path, default=DEFAULT_RUN)
    p.add_argument("--no-figures", action="store_true")
    p.add_argument("--agreement-only", action="store_true", help="Rebuild agreement assets from the existing panel without reassembling model results.")
    a = p.parse_args()
    if a.agreement_only:
        render_agreement(pd.read_parquet(a.run_root / "outputs/hearing_firm_privacy_panel.parquet"), a.run_root / "outputs")
        sys.exit(0)
    assemble(a.run_root, not a.no_figures)
    # This application's completed batch publishes the reviewable worked example
    # and replaces only the manuscript's marked result passage.
    if not a.no_figures:
        import subprocess
        cfg = json.loads((a.run_root / "config.json").read_text())
        if cfg["packageId"] == "CHRG-115shrg37801" and cfg["topic_id"] == 68:
            exporter = ROOT / "T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/export_example.py"
            subprocess.run([sys.executable, str(exporter), "export", "--run-root", str(a.run_root)], check=True)
