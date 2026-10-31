"""Small synthetic check: aggregation, missed-screen audit, and incomplete runs.

All synthetic data stays in a temporary directory; no model results are invented
in the project outputs. Run with the project Python environment.
"""

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
path = ROOT / "T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.2 - Panel Assembly and Empirical Descriptives.py"
spec = importlib.util.spec_from_file_location("assembly", path)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
T = M.T


def check():
    comparison = pd.DataFrame({"accessionNo": [f"q-{i}" for i in range(11)],
                               "standardized_score": list(range(11)),
                               "flagged_blocks": [0] * 10 + [1],
                               "llm_related": [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1]})
    quintiles = M.agreement_quintiles(comparison)
    assert quintiles.firms.tolist() == [2, 2, 2, 2, 2]
    assert quintiles.firms_with_tags.tolist() == [0, 1, 1, 2, 1]
    assert quintiles.firms_with_tags_percent.tolist() == [0, 50, 50, 100, 50]
    assert quintiles.similarity_max.max() == 9  # Flagged high-similarity firm is excluded.
    print("PASS: agreement bins use similarity, exclude flagged filings, and divide tagged firms by all firms in each bin.")
    with tempfile.TemporaryDirectory() as d:
        run = Path(d)
        cb = pd.DataFrame([{"topic_id": 68, "label": "privacy", "definition": "Consumer personal information."}])
        cb.to_parquet(run / "codebook.parquet", index=False)
        firms, blocks, sents, events = [], [], [], []
        labels, _ = T.format_topic_labels(cb)
        definitions, _ = T.format_topic_entries(cb, [68])
        for i, gate_output in enumerate(["[68]", "[]", "not JSON", "[]"]):
            acc = f"test-{i}"
            text = ["This company collects consumer information.", "Privacy compliance increases our costs."]
            firms.append({"accessionNo": acc, "gvkey": acc, "filedAt": pd.Timestamp("2017-01-01", tz="UTC"), "n_sentences": 2, "standardized_score": float(i)})
            blocks.append({"block_id": i, "accessionNo": acc, "block_idx": 0, "sent_lo": 0, "sent_hi": 1, "n_sentences": 2, "audit": i == 3})
            sents.extend({"accessionNo": acc, "sent_idx": j, "sentence": s} for j, s in enumerate(text))
            candidates, errors = T.parse_gate_topics(gate_output, {68})
            def call(stage, output):
                user = T.render_gate_user(text, 1, labels) if stage == "gate" else T.render_confirm_user(text, 1, definitions)
                return {"stage": stage, "output": output, "user": user, "system": T.SYSTEM, "input_sha256": hashlib.sha256(user.encode()).hexdigest(), "prompt_version": T.PROMPT_VERSION, "hit_cap": False}
            calls = [call("gate", gate_output)]
            tags, audit_tags = [], []
            if i == 0:
                output = '[[1,68,"N"],[2,68,"T"]]'
                calls.append(call("confirm", output))
                tags, _ = T.parse_topic_tags(output, {68}, 1, 2)
            if i == 3:
                output = '[[1,68,"N"]]'
                calls.append(call("audit", output))
                audit_tags, _ = T.parse_topic_tags(output, {68}, 1, 2)
            events.append({"block_id": i, "accessionNo": acc, "block_idx": 0, "candidates": candidates, "target_gated": bool(candidates), "tags": tags, "errors": errors, "audit": i == 3, "audit_tags": audit_tags, "audit_errors": [], "calls": calls})
        for name, rows in [("filings", firms), ("blocks", blocks), ("sentences", sents)]:
            pd.DataFrame(rows).to_parquet(run / f"{name}.parquet", index=False)
        cfg = {"packageId": "TEST", "hearing_date": "2018-04-10", "topic_id": 68, "n_shards": 1, "n_filings": 4, "prompt_version": T.PROMPT_VERSION, "input_hashes": {}, "helper_hashes": {}}
        (run / "config.json").write_text(json.dumps(cfg))
        (run / "events_0.jsonl").write_text("\n".join(json.dumps(e) for e in events[:-1]) + "\n")
        try:
            M.assemble(run, figures=False)
        except AssertionError as e:
            assert "Incomplete run" in str(e)
        else:
            raise AssertionError("Incomplete run was accepted.")
        assert not (run / "outputs/hearing_firm_privacy_panel.csv").exists()
        (run / "events_0.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n")
        result = M.assemble(run, figures=False)
        panel = pd.read_parquet(run / "outputs/hearing_firm_privacy_panel.parquet").set_index("accessionNo")
        assert panel.loc["test-0", "relevant_sentences"] == 2
        assert panel.loc["test-0", "threat_share"] == .5
        assert panel.loc["test-1", "llm_related"] == 0
        assert pd.isna(panel.loc["test-1", "neutral_share"])
        assert pd.isna(panel.loc["test-2", "llm_related"])
        assert panel.loc["test-3", "relevant_sentences"] == 0
        assert result["audit_miss_rate"] == 1 and result["privacy_sentence_tags"] == 2
        print("PASS: incomplete runs refused; counts/shares correct; failures stay unknown; audit tags stay separate.")
        # Exercise the unattended publication step only in the temporary tree.
        exporter_path = Path(__file__).with_name("export_example.py")
        spec = importlib.util.spec_from_file_location("exporter_check", exporter_path)
        exporter = importlib.util.module_from_spec(spec); spec.loader.exec_module(exporter)
        exporter.ROOT = run / "publication_check"
        exporter.OUT = exporter.ROOT / "worked_example"
        manuscript = exporter.ROOT / "W - Writing and Drafts/Proposal_for_Org_Sci_092126_AR.md"
        manuscript.parent.mkdir(parents=True)
        exporter.OUT.mkdir()
        manuscript.write_text("before\n<!-- TOPIC68_RUN_STATUS_START -->\npending\n<!-- TOPIC68_RUN_STATUS_END -->"
                              "\nEvaluation methods stay here.\n<!-- TOPIC68_EVALUATION_START -->\npending\n<!-- TOPIC68_EVALUATION_END -->\nafter")
        (exporter.OUT / "README.md").write_text("before\n<!-- RUN_STATUS_START -->\npending\n<!-- RUN_STATUS_END -->\nafter")
        sample = panel.reset_index().iloc[:2].copy()
        sample["companyName"] = ["Example A", "Example B"]
        tag_frame = pd.read_parquet(run / "outputs/privacy_tags.parquet")
        quintiles = M.agreement_quintiles(panel.reset_index())
        exporter.publish_results(result, sample, tag_frame, quintiles)
        generated = manuscript.read_text()
        assert generated.startswith("before\n") and generated.endswith("\nafter")
        assert "Example A | 2 | 0 | 1 | 1 | 0" in generated
        assert "screen missed 1" in generated and "human validation remains incomplete" in generated
        assert "percentage uses firms as its denominator" in generated
        run_text = generated.split("<!-- TOPIC68_RUN_STATUS_START -->")[1].split("<!-- TOPIC68_RUN_STATUS_END -->")[0]
        evaluation_text = generated.split("<!-- TOPIC68_EVALUATION_START -->")[1].split("<!-- TOPIC68_EVALUATION_END -->")[0]
        assert "Example A | 2 | 0 | 1 | 1 | 0" in run_text and "screen missed" not in run_text
        assert "screen missed 1" in evaluation_text and "Example A |" not in evaluation_text
        assert generated.index("Evaluation methods stay here.") < generated.index("screen missed 1")
        exporter.publish_results(result, sample, tag_frame, quintiles)
        assert manuscript.read_text() == generated
        print("PASS: publication separates run and evaluation results, preserves methods and other prose, and is idempotent.")


if __name__ == "__main__":
    check()
