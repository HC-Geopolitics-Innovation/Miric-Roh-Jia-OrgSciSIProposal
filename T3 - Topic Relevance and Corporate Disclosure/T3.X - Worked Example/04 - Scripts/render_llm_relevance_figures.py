"""Visualize the completed privacy run, preserving model outputs and source evidence.

Separate ranks describe threat and opportunity sentences as shares of each filing. Name matching
uses the explicit aliases below; the industry baseline is Facebook's modal NAICS3.
No model generation or correction of saved tags occurs here.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "R - Results/figures/T3 - Topic Relevance and Corporate Disclosure"
sys.path.insert(0, str(ROOT / "B - Backup of Original File Structure/scripts/python/lib"))
import tagging as T

# These are documented literal-name checks, not exhaustive entity resolution.
ALIASES = {
    "010631": ["Total System Services", "TSYS"],
    "170617": ["Facebook"],
    "027885": ["Trade Desk"],
    "001468": ["American Greetings", "AmericanGreetings", "AG Interactive",
               "Blue Mountain", "BlueMountain", "justwink", "Cardstore", "Carlton Cards"],
    "031673": ["AmerisourceBergen", "Amerisource"],
    "165993": ["Fidelity National Information Services", "FIS"],
    "199356": ["TripAdvisor", "Trip Advisor"],
    "002269": ["H&R Block", "H & R Block", "H and R Block"],
    "007647": ["Bank of America", "BofA"],
    "184700": ["Fleetcor", "Fleet cor"],
    "007228": ["Medtronic"],
    "001447": ["American Express", "Amex"],
    "143974": ["Alliance Data", "AllianceData"],
    "018043": ["News Corp", "News Corporation"],
    "018872": ["Twitter"],
}
DISPLAY = dict(zip(ALIASES, [
    "Total System Services", "Facebook", "The Trade Desk", "American Greetings",
    "AmerisourceBergen", "Fidelity National Information Services", "TripAdvisor",
    "H&R Block", "Bank of America", "Fleetcor", "Medtronic", "American Express",
    "Alliance Data Systems", "News Corp", "Twitter",
]))
ALIASES.update({
    "002751": ["Cardinal Health"], "031887": ["ResMed"],
    "025056": ["Time Warner", "TimeWarner"], "003226": ["Comcast"],
    "005543": ["Welltower", "Health Care REIT"], "020116": ["Paycom"],
    "141384": ["Align Technology", "Invisalign"],
    "020430": ["SLM", "Sallie Mae"], "028191": ["Royal Caribbean"],
})
DISPLAY.update({
    "165993": "Fidelity National (FIS)",
    "002751": "Cardinal Health", "031887": "ResMed", "025056": "Time Warner",
    "003226": "Comcast", "005543": "Welltower", "020116": "Paycom Software",
    "141384": "Align Technology", "020430": "SLM", "028191": "Royal Caribbean",
})
CASES = {
    "010631": {"context": 42, "sentence": 48, "direction": "threat",
               "interpretation": "The sentence explicitly links breach notification to increasing scope and cost."},
    "170617": {"context": 54, "sentence": 55, "direction": "threat",
               "interpretation": "The sentence identifies operational requirements and penalties for noncompliance."},
    "020116": {"context": 259, "sentence": 263, "direction": "opportunity",
               "interpretation": "Security assurance is explicit; growth, demand, or competitive advantage is not. The opportunity label requires review."},
    "165993": {"context": 215, "sentence": 217, "direction": "opportunity",
               "interpretation": "The program manages privacy risks and compliance. A business gain is not explicitly stated, so the opportunity label requires review."},
}

COLORS = {"threat": "#AB4A3A", "neutral": "#477A94", "opportunity": "#28765D"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n")


def save(fig, name):
    for ext in ["svg", "pdf", "png"]:
        fig.savefig(FIGURES / f"{name}.{ext}", dpi=180, bbox_inches="tight", pad_inches=.03, facecolor="white")
    plt.close(fig)


def ranking_figure(top, direction):
    fig, ax = plt.subplots(figsize=(7.4, max(2.6, .28 * len(top) + .7)))
    values = 100 * top[f"{direction}_filing_share"].to_numpy()
    y = np.arange(len(top))
    ax.barh(y, values, color="#003049", height=.58)
    ax.set_yticks(y, [DISPLAY[r.gvkey] for r in top.itertuples()])
    ax.invert_yaxis()
    ax.set_xlim(left=0)
    ax.set_xlabel(f"Privacy {direction} sentences (% of disclosure)")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#D0D0D0", linewidth=.5)
    ax.set_axisbelow(True)
    ax.margins(y=.025)
    fig.tight_layout(pad=.35)
    save(fig, f"fig_privacy_llm_{direction}")


def evidence_table(clean, tags, output):
    selected = [(gv, spec["sentence"], spec["direction"]) for gv, spec in CASES.items()]
    records = []
    lines = ["| Firm | Filed | Sentence | Recorded LLM label | Original disclosure sentence |",
             "|---|---|---:|---|---|"]
    for gv, number, direction in selected:
        firm = clean.loc[clean.gvkey.eq(gv)].iloc[0]
        tag = tags.loc[tags.accessionNo.eq(firm.accessionNo) & tags.sentence_number.eq(number)]
        assert len(tag) == 1 and tag.direction.item() == direction
        sentence = tag.sentence.item()
        date = str(firm.filedAt)[:10]
        name = "Fidelity National Information Services (FIS)" if gv == "165993" else DISPLAY[gv]
        records.append({"gvkey": gv, "company": name, "accessionNo": firm.accessionNo,
                        "filedAt": date, "sentence_number": number, "direction": direction,
                        "sentence": sentence, "filingUrl": firm.filingUrl})
        lines.append(f"| [{name}]({firm.filingUrl}) | {date} | {number} | {direction.title()} | "
                     f"{sentence.replace('|', '&#124;')} |")
    pd.DataFrame(records).to_csv(output / "privacy_evidence_table.csv", index=False)
    (output / "privacy_evidence_table.md").write_text("\n".join(lines) + "\n")


def main(run_root):
    cfg = json.loads((run_root / "config.json").read_text())
    assessment = json.loads((run_root / "outputs/assessment.json").read_text())
    assert assessment["status"] == "complete" and cfg["topic_id"] == 68
    panel_path = run_root / "outputs/hearing_firm_privacy_panel.parquet"
    tags_path = run_root / "outputs/privacy_tags.parquet"
    panel = pd.read_parquet(panel_path)
    tags = pd.read_parquet(tags_path)
    assert panel.accessionNo.is_unique and not tags.duplicated(["accessionNo", "sent_idx", "topic_id"]).any()
    counts = tags.groupby(["accessionNo", "direction"]).size().unstack(fill_value=0)
    for direction in COLORS:
        assert np.array_equal(panel[direction], panel.accessionNo.map(counts[direction]).fillna(0))
    assert panel.relevant_sentences.eq(panel[list(COLORS)].sum(axis=1)).all()
    assert np.allclose(panel.relevant_sentence_share, panel.relevant_sentences / panel.n_sentences)
    source_root = Path(cfg["source_data"]) / "interim/repo_data"
    industry_path = source_root / "raw/01_firm_id/crsp_compustat_link.dta"
    link = pd.read_stata(industry_path, columns=["GVKEY", "naics"])
    link["naics"] = link.naics.astype(str).str.strip()
    link = link[link.naics.str.len().ge(3)].copy()
    link["naics3"] = link.naics.str[:3]
    mapping = link.groupby("GVKEY").naics3.agg(lambda s: s.mode().iloc[0])
    panel["naics3"] = panel.gvkey.map(mapping)
    facebook_industry = panel.loc[panel.gvkey.eq("170617"), "naics3"].item()
    assert facebook_industry == "519"
    clean = panel[panel.flagged_blocks.eq(0)].copy()
    for direction in ["threat", "opportunity"]:
        clean[f"{direction}_filing_share"] = clean[direction] / clean.n_sentences
        clean[f"{direction}_rank"] = clean[f"{direction}_filing_share"].rank(method="min", ascending=False).astype(int)
    clean["similarity_rank"] = clean.standardized_score.rank(method="min", ascending=False).astype(int)
    clean["same_facebook_naics3"] = clean.naics3.eq(facebook_industry).astype("boolean").where(clean.naics3.notna())
    tops = {d: clean.loc[clean[d].gt(0)].sort_values(
        [f"{d}_filing_share", "gvkey"], ascending=[False, True]).head(15).copy()
        for d in ["threat", "opportunity"]}
    assert all(set(top.gvkey) <= set(ALIASES) for top in tops.values()), "Add documented aliases for new displayed firms."
    hearing_path = ROOT / "T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/source.txt"
    hearing = " ".join(hearing_path.read_text().casefold().split())
    checks = []
    for gv, aliases in ALIASES.items():
        hits = {a: len(re.findall(r"(?<!\w)" + re.escape(a.casefold()) + r"(?!\w)", hearing))
                for a in aliases}
        checks.append({"gvkey": gv, "display_name": DISPLAY[gv], "aliases": aliases,
                       "alias_hit_counts": hits, "name_found": any(hits.values())})
    output = EXAMPLE / "02 - Outputs"
    full_sample = output / "01 - Full Sample"
    cases_output = output / "02 - Worked Cases"
    evaluation = output / "03 - Evaluation and Figures"
    sources = EXAMPLE / "01 - Inputs/Source Filings"
    logs = EXAMPLE / "03 - Logs and Verification"
    for directory in (full_sample, cases_output, evaluation, sources, logs):
        directory.mkdir(parents=True, exist_ok=True)
    clean.sort_values("gvkey").to_csv(full_sample / "privacy_llm_ranking.csv", index=False)
    for direction, top in tops.items():
        top = top.merge(pd.DataFrame(checks)[["gvkey", "name_found"]], on="gvkey", validate="1:1")
        assert top.same_facebook_naics3.notna().all()
        assert top[f"{direction}_filing_share"].is_monotonic_decreasing
        assert (~top.name_found & ~top.same_facebook_naics3).sum() == sum(
            not n and not i for n, i in zip(top.name_found, top.same_facebook_naics3))
        tops[direction] = top
        top.to_csv(evaluation / f"privacy_llm_{direction}_top.csv", index=False)
    sentences = pd.read_parquet(run_root / "sentences.parquet")
    accs = clean.loc[clean.gvkey.isin(CASES), "accessionNo"].tolist()
    raw = pd.read_parquet(source_root / "raw/03_sp500_10k_item1/sp500_10k_item1.parquet",
                          filters=[("accessionNo", "in", accs)], columns=["accessionNo", "item1"])
    blocks = pd.read_parquet(run_root / "blocks.parquet")
    cb = pd.read_parquet(run_root / "codebook.parquet")
    labels, valid_ids = T.format_topic_labels(cb)
    entries, target_ids = T.format_topic_entries(cb, [68])
    events = []
    for path in sorted(run_root.glob("events_*.jsonl")):
        with path.open() as stream:
            events.extend(e for line in stream if (e := json.loads(line))["accessionNo"] in accs)
    cases, calls = [], []
    lines = ["# Threat and opportunity examples", "",
             "These four cases are the two highest-ranked firms for threat and the two highest-ranked for opportunity. "
             "They illustrate traceable connections, not an independent validation sample. "
             "Ranks include all 894 filings without processing flags and use minimum ranks for ties.", "",
             "Hearing-name checks use documented aliases in the full saved hearing, including appendices. "
             "Matching ignores case and repeated whitespace and requires word boundaries. "
             "It is not exhaustive entity resolution. The industry baseline requires Facebook's modal NAICS3 (519), "
             "using the same historical reference mapping as the original figures.", "",
             "Raw model labels are preserved, including questionable tags. Inspection here is not independent human validation.", ""]
    for gv, spec in CASES.items():
        row = clean[clean.gvkey.eq(gv)].iloc[0]
        acc = row.accessionNo
        ss = sentences[sentences.accessionNo.eq(acc)].set_index("sent_idx").sentence.sort_index()
        tt = tags[tags.accessionNo.eq(acc)].set_index("sentence_number").sort_index()
        source = raw.loc[raw.accessionNo.eq(acc), "item1"].item()
        (sources / f"{acc}_source.txt").write_text(source)
        case = json.loads(row.to_json())
        case.update({"display_name": DISPLAY[gv], "filedAt": str(row.filedAt),
                     "name_check": next(c for c in checks if c["gvkey"] == gv),
                     "context_sentence": ss.loc[spec["context"]-1],
                     "selected_sentence_number": spec["sentence"], "selected_direction": spec["direction"],
                     "selected_sentence": ss.loc[spec["sentence"]-1], "interpretation": spec["interpretation"]})
        assert tt.loc[spec["sentence"], "direction"] == spec["direction"]
        assert tt.loc[spec["sentence"], "sentence"] == case["selected_sentence"]
        assert row[f"{spec['direction']}_rank"] in [1, 2]
        cases.append(case)
        direction = spec["direction"]
        lines += [f'<a id="{acc}"></a>', f"## {DISPLAY[gv]}", "",
                  f"{direction.title()} rank {row[f'{direction}_rank']}/{len(clean)}; "
                  f"{row[direction]}/{row.n_sentences} {direction} sentences "
                  f"({100*row[f'{direction}_filing_share']:.2f}%); "
                  f"all recorded counts: threat {row.threat}, neutral {row.neutral}, opportunity {row.opportunity}.", "",
                  f"NAICS {row.naics3}. Filed {str(row.filedAt)[:10]}; {row.filing_age_days} days before hearing. "
                  f"[SEC filing]({row.filingUrl}); [saved Item 1](<../../01 - Inputs/Source Filings/{acc}_source.txt>).", "",
                  f"Aliases searched and match counts: {case['name_check']['alias_hit_counts']}.", "",
                  f"Context, sentence {spec['context']}: {case['context_sentence']}", "",
                  f"**Selected sentence {spec['sentence']} / recorded label {direction}:** {case['selected_sentence']}", "",
                  f"Interpretation: {spec['interpretation']}", "",
                  "All model tags are retained below, including statements that may concern neighboring subjects "
                  "or support a different directional interpretation. No counts or ranks are manually corrected.", "",
                  "### All retained tags", "", "| Sentence | Recorded label | Original text |", "|---:|---|---|"]
        for n, t in tt.iterrows():
            lines.append(f"| {n} | {t.direction} | {t.sentence.replace('|', '&#124;')} |")
        lines += ["", "### Complete input blocks and recorded responses", ""]
        for e in sorted((e for e in events if e['accessionNo'] == acc), key=lambda e: e['block_idx']):
            b = blocks.loc[blocks.accessionNo.eq(acc) & blocks.block_idx.eq(e['block_idx'])].iloc[0]
            texts = ss.loc[b.sent_lo:b.sent_hi].tolist()
            start = int(b.sent_lo)+1
            lines += [f"#### Block {e['block_idx']}: sentences {start}–{int(b.sent_hi)+1}", "", "```text",
                      T.format_numbered(texts, start), "```", ""]
            for c in e['calls']:
                prompt = T.render_gate_user(texts, start, labels) if c['stage'] == 'gate' else T.render_confirm_user(texts, start, entries)
                assert prompt == c['user'] and hashlib.sha256(prompt.encode()).hexdigest() == c['input_sha256']
                if c['stage'] == 'confirm':
                    parsed, errors = T.parse_topic_tags(c['output'], target_ids, start, len(texts))
                    assert not errors and parsed == e['tags']
                calls.append(c)
                lines += [f"{c['stage'].title()} response:", "", "```text", c['output'], "```", ""]
    (cases_output / "privacy_directional_examples.md").write_text("\n".join(lines))
    dump(cases_output / "privacy_directional_examples.json", cases)
    evidence_table(clean, tags, cases_output)
    (logs / "directional_example_calls.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False)+'\n' for c in calls))
    report = {"run_root": str(run_root), "topic_id": 68, "hearing_id": cfg['packageId'],
              "ranking": "Separate threat / n_sentences and opportunity / n_sentences; flagged_blocks == 0; minimum ranks for ties; plots omit zeros",
              "clean_filings": len(clean), "excluded_flagged_filings": len(panel)-len(clean),
              "clean_positive_filings": int(clean.relevant_sentences.gt(0).sum()),
              "clean_positive_industries": int(clean.loc[clean.relevant_sentences.gt(0), 'naics3'].nunique()),
              "directional_figures": {d: {"displayed_firms": len(top),
                  "firms_with_tags": int(clean[d].gt(0).sum()),
                  "neither_baseline": int((~top.name_found & ~top.same_facebook_naics3).sum())}
                  for d, top in tops.items()},
              "industry_rule": "Same modal NAICS3 as Facebook (519); not a test of all industry-based methods",
              "name_rule": "Literal listed aliases; casefold; whitespace collapsed; word boundaries; full hearing including appendices",
              "name_checks": checks, "case_calls_verified": len(calls),
              "selection": "The two highest-ranked firms for threat and the two highest-ranked for opportunity; sentences selected for interpretation",
              "human_validation": "not completed; raw tags retained; selected opportunity passages describe assurance or compliance without an explicit gain",
              "input_sha256": {str(p): digest(p) for p in [panel_path, tags_path, hearing_path, industry_path]}}
    dump(logs / "llm_figure_verification.json", report)
    plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10,
                         "axes.labelsize": 10.5, "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
                         "svg.fonttype": "none", "pdf.fonttype": 42})
    for direction, top in tops.items():
        ranking_figure(top, direction)
    print(f"Rendered two directional figures; checked all {len(tags)} tag counts and {len(calls)} case calls.")
    print(json.dumps(report["directional_figures"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path,
                        nargs="?", default=Path("/project2/njia_1089/acroh/data/output/topic68_relevance_20180410"))
    main(parser.parse_args().run_root)
