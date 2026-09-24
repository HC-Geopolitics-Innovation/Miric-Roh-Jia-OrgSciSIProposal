"""Render saved stance panels with corrected coverage captions, without models.

Usage: python render_stance_figures.py /path/to/llm_method/data
Reuses the original notebook's plotting cells; does not recompute panel data.
"""

import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("data_root", type=Path)
base = parser.parse_args().data_root / "interim/topics/taxonomy"
root = Path(__file__).resolve().parents[3]
FIGURES = root / "R - Results/figures/T2 - Topic Extraction and Stance Analysis"
rec = pd.read_parquet(base / "track2_assigned.parquet")
rec = rec[rec["topic_id"] >= 0]
tp = pd.read_parquet(base / "stance_panel_topic_congress.parquet")
notebook = json.loads((root / "B - Backup of Original File Structure/scripts/python/03_topic_extraction/12_stance_panel.ipynb").read_text())
# Preserve plotting logic and styles. The original cell imports an output
# directory from the old project; use this repository's directory instead.
exec("".join(notebook["cells"][4]["source"]).replace("from paths import FIGURES", ""))
NOTE = (f"Note: {len(rec):,} legislator stance records (prompt "
        "stance-extraction-0.3-dev) placed on the frozen Track-1 codebook "
        "v1.0; House Science and Senate Commerce hearings, "
        f"{tp['congress'].min()}th–{tp['congress'].max()}th Congress "
        f"({rec['year'].min()}–{rec['year'].max()}). A record is one member "
        "position: evidence sentences, a topic, and support or concern.")
for cell in (6, 8, 10):
    source = "".join(notebook["cells"][cell]["source"])
    source = source.replace("Congress (106th = 1999–2000 … 119th = 2025–26)",
                            "Congress (104th = 1995–96 … 119th = 2025–26)")
    exec(source)
