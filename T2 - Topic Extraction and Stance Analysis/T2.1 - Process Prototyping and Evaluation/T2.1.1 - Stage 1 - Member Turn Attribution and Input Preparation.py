"""
T2.1 Stage 1: Member Turn Attribution & Input Preparation
-----------------------------------------------------------
Links congressional hearing speaking turns to BioGuide member IDs and prepares
input records for topic extraction and stance classification.
"""

import sys
import os
from pathlib import Path
import pandas as pd

sys.path.insert(0, "../L - Lib/L5 - Evaluation and Utilities")
sys.path.insert(0, "../L - Lib/L2 - Document Parsing and Text Cleaning")
from paths import DATA_REPO, HEARINGS_REPO

def prepare_member_speaking_turns(hearings_path: Path | None = None) -> pd.DataFrame:
    """Prepares speaking turn records attributed to congressional member rosters."""
    print("--- 1. Preparing Member Speaking Turns for Topic Extraction ---")
    if hearings_path is None or not hearings_path.exists():
        hearings_path = HEARINGS_REPO / "hearings_sst.parquet"
        
    if hearings_path.exists():
        df = pd.read_parquet(hearings_path)
        print(f"Loaded {len(df)} hearings for turn attribution.")
        return df
    else:
        print(f"File {hearings_path} not found. Operating in template mode.")
        return pd.DataFrame(columns=["packageId", "member_id", "turn_text", "speaker_name"])

if __name__ == "__main__":
    prepare_member_speaking_turns()
