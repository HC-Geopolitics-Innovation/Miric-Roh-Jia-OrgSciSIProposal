"""Combine sentence cosine similarity with recorded LLM direction after extraction.

New measurement extension: not part of the original two-instrument design.
For direction d, score = 100/N * sum(max(0, cosine) for accepted d tags).
No new model calls, topic assignments, or directional labels are generated.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example"
VERSION = "sentence-cosine-direction-1.0"
EXAMPLES = {"010631": "Total System Services", "170617": "Facebook",
            "020116": "Paycom Software", "165993": "Fidelity National (FIS)"}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def cosine_weights(vectors, center):
    """Re-normalize the stored, quantized vectors to calculate actual cosines."""
    vectors, center = vectors.astype(np.float64), center.astype(np.float64)
    norms = np.linalg.norm(vectors, axis=1) * np.linalg.norm(center)
    assert np.isfinite(vectors).all() and np.isfinite(center).all()
    assert (norms > 0).all()
    cosines = np.clip(vectors @ center / norms, -1, 1)
    return cosines, np.maximum(0, cosines)


def aggregate(panel, tags):
    """Keep observed sums; make final scores missing for any flagged filing."""
    out = panel.copy()
    assert out.accessionNo.is_unique and out.n_sentences.gt(0).all()
    assert not tags.duplicated(["accessionNo", "sent_idx", "topic_id"]).any()
    assert set(tags.accessionNo) <= set(out.accessionNo)
    assert tags.direction.isin(["threat", "opportunity", "neutral"]).all()
    assert tags.weight.between(0, 1).all()
    out["eligible_directional_scores"] = out.flagged_blocks.eq(0)
    for d in ["threat", "opportunity", "neutral"]:
        rows = tags.loc[tags.direction.eq(d)]
        counts = out.accessionNo.map(rows.groupby("accessionNo").size()).fillna(0)
        assert counts.eq(out[d]).all(), f"{d} tags do not match the existing panel"
        if d == "neutral":
            continue
        sums = out.accessionNo.map(rows.groupby("accessionNo").weight.sum()).fillna(0)
        out[f"observed_{d}_weight_sum"] = sums
        out[f"mean_{d}_weight"] = sums / out[d].replace(0, np.nan)
        out[f"unweighted_{d}_score"] = (100 * out[d] / out.n_sentences).where(out.eligible_directional_scores)
        out[f"weighted_{d}_score"] = (100 * sums / out.n_sentences).where(out.eligible_directional_scores)
        out[f"weighted_{d}_rank"] = out[f"weighted_{d}_score"].rank(method="min", ascending=False).astype("Int64")
        assert sums.le(out[d] + 1e-10).all()
        valid = out.eligible_directional_scores
        assert out.loc[valid, f"weighted_{d}_score"].between(0, 100).all()
        assert out.loc[valid, f"weighted_{d}_score"].le(out.loc[valid, f"unweighted_{d}_score"] + 1e-10).all()
    return out


def self_check():
    # Known angles, a negative cosine, a neutral tag, an untagged sentence,
    # a flagged positive filing, and a clean filing with no tags.
    cos, weights = cosine_weights(np.array([[2., 0], [.6, .8], [-1, 0], [0, 3], [.8, .6]]), np.array([4., 0]))
    assert np.allclose(cos, [1, .6, -1, 0, .8])
    assert np.allclose(weights, [1, .6, 0, 0, .8])
    panel = pd.DataFrame({"accessionNo": ["A", "B", "C"], "n_sentences": [5, 2, 3],
                          "flagged_blocks": [0, 1, 0], "threat": [2, 1, 0],
                          "opportunity": [1, 0, 0], "neutral": [1, 0, 0]})
    tags = pd.DataFrame({"accessionNo": ["A"] * 4 + ["B"], "sent_idx": [0, 1, 2, 3, 0],
                         "topic_id": [68] * 5, "direction": ["threat", "opportunity", "threat", "neutral", "threat"],
                         "weight": weights})
    out = aggregate(panel, tags).set_index("accessionNo")
    assert out.loc["A", "weighted_threat_score"] == 20
    assert np.isclose(out.loc["A", "weighted_opportunity_score"], 12)
    assert out.loc["A", "unweighted_threat_score"] == 40
    assert np.isclose(out.loc["B", "observed_threat_weight_sum"], .8)
    assert pd.isna(out.loc["B", "weighted_threat_score"])
    assert pd.isna(out.loc["B", "weighted_opportunity_score"])
    assert out.loc["C", "weighted_threat_score"] == out.loc["C", "weighted_opportunity_score"] == 0
    assert pd.isna(out.loc["C", "mean_threat_weight"])


def main(run_root):
    self_check()
    cfg = json.loads((run_root / "config.json").read_text())
    assessment = json.loads((run_root / "outputs/assessment.json").read_text())
    assert assessment["status"] == "complete" and cfg["topic_id"] == 68
    panel_path = run_root / "outputs/hearing_firm_privacy_panel.parquet"
    tags_path = run_root / "outputs/privacy_tags.parquet"
    panel = pd.read_parquet(panel_path)
    tags = pd.read_parquet(tags_path)
    assert len(panel) == cfg["n_filings"] and len(tags) == assessment["privacy_sentence_tags"]
    assert tags.topic_id.eq(68).all() and tags.sentence_number.eq(tags.sent_idx + 1).all()
    rel = Path(cfg["source_data"]) / "interim/relevance"
    sentence_path = rel / "item1/sentences.parquet"
    embedding_path = rel / "item1/emb_bge-large-en-v1.5.npy"
    center_path = rel / "scores/topic_centroids_bge-large-en-v1.5.npy"
    index_path = rel / "scores/topic_index.parquet"
    topic_index = pd.read_parquet(index_path)
    centers = np.load(center_path)
    assert len(centers) == len(topic_index)
    topic_row = topic_index.index[topic_index.topic_id.eq(68)].item()
    center = centers[topic_row]

    # The full key table establishes global row positions in the saved .npy.
    # Sentence text is read only for tagged filings, keeping memory modest.
    keys = pd.read_parquet(sentence_path, columns=["accessionNo", "sent_idx"])
    embeddings = np.load(embedding_path, mmap_mode="r")
    assert len(keys) == len(embeddings)
    chosen_keys = keys.loc[keys.accessionNo.isin(tags.accessionNo)].copy()
    chosen_keys["embedding_row"] = chosen_keys.index
    tags = tags.merge(chosen_keys, on=["accessionNo", "sent_idx"], how="left", validate="1:1")
    assert tags.embedding_row.notna().all()
    source_text = pd.read_parquet(sentence_path, filters=[("accessionNo", "in", tags.accessionNo.unique().tolist())],
                                  columns=["accessionNo", "sent_idx", "sentence"])
    tags = tags.merge(source_text.rename(columns={"sentence": "source_sentence"}),
                      on=["accessionNo", "sent_idx"], how="left", validate="1:1")
    assert tags.sentence.eq(tags.source_sentence).all()
    tags = tags.drop(columns="source_sentence")
    vectors = embeddings[tags.embedding_row.to_numpy(dtype=int)]
    tags["cosine"], tags["weight"] = cosine_weights(vectors, center)
    result = aggregate(panel, tags)
    tags = tags.merge(panel[["accessionNo", "gvkey", "companyName", "n_sentences", "flagged_blocks", "filedAt"]],
                      on="accessionNo", validate="m:1")
    for d in ["threat", "opportunity"]:
        tags[f"observed_{d}_contribution"] = np.where(tags.direction.eq(d), 100 * tags.weight / tags.n_sentences, 0.)
        # A second, direct sum of per-sentence contributions must reproduce
        # the published scores for eligible filings.
        direct = result.accessionNo.map(tags.groupby("accessionNo")[f"observed_{d}_contribution"].sum()).fillna(0)
        eligible = result.eligible_directional_scores
        assert np.allclose(result.loc[eligible, f"weighted_{d}_score"], direct.loc[eligible], atol=1e-12, rtol=0)
    tags = tags.sort_values(["accessionNo", "sent_idx"])
    result["weighted_score_version"] = VERSION
    examples = pd.concat([result.loc[result.gvkey.eq(gv)] for gv in EXAMPLES]).copy()
    examples.insert(0, "display_name", examples.gvkey.map(EXAMPLES))
    keep = ["display_name", "gvkey", "accessionNo", "filedAt", "n_sentences", "threat", "opportunity", "neutral",
            "unweighted_threat_score", "mean_threat_weight", "weighted_threat_score", "weighted_threat_rank",
            "unweighted_opportunity_score", "mean_opportunity_weight", "weighted_opportunity_score", "weighted_opportunity_rank"]
    examples = examples[keep]
    # Illustrations include an explicit counterexample to semantic correction.
    selected = {"010631": [48, 62], "170617": [55, 56], "020116": [263, 268], "165993": [217, 233]}
    illustration = pd.concat([tags.loc[tags.gvkey.eq(gv) & tags.sentence_number.isin(numbers)]
                              for gv, numbers in selected.items()])
    assert len(illustration) == sum(map(len, selected.values()))
    illustration = illustration.copy()
    illustration.insert(0, "display_name", illustration.gvkey.map(EXAMPLES))

    full_sample = EXAMPLE / "02 - Outputs/01 - Full Sample"
    cases = EXAMPLE / "02 - Outputs/02 - Worked Cases"
    for panel_dir, case_dir in [(run_root / "outputs", run_root / "outputs"), (full_sample, cases)]:
        for directory in (panel_dir, case_dir):
            directory.mkdir(parents=True, exist_ok=True)
        result.to_csv(panel_dir / "hearing_firm_privacy_weighted_panel.csv", index=False)
        tags.to_csv(panel_dir / "privacy_weighted_sentence_records.csv", index=False)
        examples.to_csv(case_dir / "privacy_weighted_firm_examples.csv", index=False)
        illustration.to_csv(case_dir / "privacy_weighted_sentence_examples.csv", index=False)
    # Keep the numeric example tables generated from the same verified values.
    rows = ["| Firm | Threat sentences | Mean threat weight | Unweighted threat | Weighted threat | Opportunity sentences | Mean opportunity weight | Unweighted opportunity | Weighted opportunity |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in examples.itertuples():
        ow = "—" if pd.isna(r.mean_opportunity_weight) else f"{r.mean_opportunity_weight:.3f}"
        rows.append(f"| {r.display_name} | {r.threat}/{r.n_sentences} | {r.mean_threat_weight:.3f} | "
                    f"{r.unweighted_threat_score:.2f} | {r.weighted_threat_score:.2f} | {r.opportunity}/{r.n_sentences} | "
                    f"{ow} | {r.unweighted_opportunity_score:.2f} | {r.weighted_opportunity_score:.2f} |")
    (cases / "privacy_weighted_firm_examples.md").write_text("\n".join(rows) + "\n")
    rows = ["| Firm | Sentence | Recorded label | Cosine weight | Contribution to directional score | Original sentence |",
            "|---|---:|---|---:|---:|---|"]
    for r in illustration.itertuples():
        contribution = getattr(r, f"observed_{r.direction}_contribution")
        rows.append(f"| {r.display_name} | {r.sentence_number} | {r.direction.title()} | {r.weight:.3f} | "
                    f"{contribution:.3f} | {r.sentence.replace('|', '&#124;')} |")
    (cases / "privacy_weighted_sentence_examples.md").write_text("\n".join(rows) + "\n")
    report = {"version": VERSION, "status": "computed; not independently validated",
              "formula": "100 / n_sentences * sum(max(0, sentence_cosine) for accepted tags of each direction)",
              "cosine": "L2-normalize stored sentence and topic vectors again after loading; float64 calculation",
              "topic_id": 68, "filings": len(result), "sentence_records": len(tags),
              "eligible_filings": int(result.eligible_directional_scores.sum()),
              "flagged_filings_with_missing_scores": int((~result.eligible_directional_scores).sum()),
              "nonpositive_cosines": int(tags.cosine.le(0).sum()),
              "cosine_min": float(tags.cosine.min()), "cosine_max": float(tags.cosine.max()),
              "checks": ["known-angle and missing-versus-zero self-check", "unique sentence-topic keys",
                         "all tag counts match original panel", "source sentence text matches embedding row",
                         "sentence contributions sum to filing scores", "0 <= weighted <= unweighted <= 100"],
              "input_sha256": {str(p): sha(p) for p in [panel_path, tags_path, center_path, index_path, run_root / "config.json"]},
              "embedding_source": {"path": str(embedding_path), "shape": list(embeddings.shape),
                                   "dtype": str(embeddings.dtype), "file_size": embedding_path.stat().st_size,
                                   "selected_rows_sha256": hashlib.sha256(vectors.tobytes()).hexdigest()},
              "sentence_index_source": str(sentence_path),
              "interpretation": "A weighted disclosure-intensity index; neither a percentage of sentences nor an economic-effect estimate. "
                                "Positive weights do not prove relevance; direction labels remain the original LLM outputs."}
    for output in [run_root / "outputs/weighted_score_verification.json",
                   EXAMPLE / "03 - Logs and Verification/weighted_score_verification.json"]:
        output.write_text(json.dumps(report, indent=2) + "\n")
    print(examples.to_string(index=False))
    print(f"Verified {len(tags)} sentence records; scores available for {result.eligible_directional_scores.sum()} of {len(result)} filings.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-root", type=Path, default=Path("/project2/njia_1089/acroh/data/output/topic68_relevance_20180410"))
    p.add_argument("--check", action="store_true", help="Run the small numerical check without reading research data.")
    args = p.parse_args()
    if args.check:
        self_check()
        print("Numerical and missing-data checks passed.")
    else:
        main(args.run_root)
