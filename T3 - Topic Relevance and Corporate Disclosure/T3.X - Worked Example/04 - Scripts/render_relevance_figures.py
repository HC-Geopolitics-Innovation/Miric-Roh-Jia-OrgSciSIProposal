"""Rebuild the original four relevance figures, correcting caption metadata.

Uses the original notebook calculations; changes only the year-range notes and
the incorrectly named zero reference. Does not run either language model.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[3]


def main(data_root):
    notebook = ROOT / "B - Backup of Original File Structure/scripts/python/04_topic_relevance/07_layer1_descriptives.ipynb"
    cells = json.loads(notebook.read_text())["cells"]
    figures = ROOT / "R - Results/figures/T3 - Topic Relevance and Corporate Disclosure"
    scope = {"DATA_REPO": data_root / "interim/repo_data", "FIGURES": figures,
             "relevance_run_dir": lambda name: data_root / "interim/relevance" / name}
    for i in [2, 4, 6, 8, 10, 12, 14]:
        source = "".join(cells[i]["source"])
        source = source.replace("from paths import DATA_REPO, FIGURES, relevance_run_dir", "")
        source = source.replace("plt.show()", "plt.close('all')")
        if i in [6, 8, 10]:
            s = scope["scores"]
            source = source.replace("1993–2025", f"{s.fyear.min()}–{s.fyear.max()}")
        if i == 12:
            source = source.replace('label="All-industry mean"', 'label="Pooled standardization reference"')
            source = source.replace("all-industry mean for the same topic by construction.", "pooled topic-and-length standardization reference, not a yearly industry mean.")
            source = source.replace("whole period (Figure 3).", "whole period.")
        exec(compile(source, f"{notebook.name}:cell{i}", "exec"), scope)
    report = {"fyear_min": int(scope["scores"].fyear.min()), "fyear_max": int(scope["scores"].fyear.max()), "top_pairs": scope["firm_topic"].nlargest(15, "z").to_dict("records"), "industries": scope["ind"].to_dict("records"), "industry_topics": scope["ind_topic"].to_dict("records")}
    out = Path(__file__).resolve().parents[1] / "03 - Logs and Verification/descriptive_figure_values.json"
    out.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("data_root", type=Path)
    main(p.parse_args().data_root)
