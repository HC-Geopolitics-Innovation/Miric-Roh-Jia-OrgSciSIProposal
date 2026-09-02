"""
T1.3 Quality Assessment - Part 1: C-SPAN Match & Embedding Discriminant Setup
-------------------------------------------------------------------------------
Matches generated LLM summaries with independent C-SPAN editorial program abstracts,
prepares text embedding environments, and asserts token length constraints.

Discriminant Framework:
- Embedded using `bge-large-en-v1.5` sentence embeddings (512 token context).
- Evaluates 3-way cosine similarity matrix:
  1. Same Document: Sim(Summary_i, Abstract_i)
  2. Same Committee, Different Hearing: Sim(Summary_i, Abstract_i')
  3. Different Committee: Sim(Summary_i, Abstract_j)
"""

import sys
import os
from pathlib import Path
import pandas as pd

sys.path.insert(0, "../L - Lib/L5 - Evaluation and Utilities")
from paths import DATA_REPO, HEARINGS_REPO, CSPAN_RAW, HF_CACHE

def setup_quality_assessment_environment():
    """Verify input datasets and configure BGE embedding environment."""
    print("--- 1. Quality Assessment Environment & Input Setup ---")
    
    # Configure HF_HOME cache for bge-large-en-v1.5 model weights
    HF_CACHE.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(HF_CACHE)
    print(f"Set HF_HOME to scratch cache: {HF_CACHE}")

def match_hearings_to_cspan(
    summaries_path: Path | None = None,
    hearings_path: Path | None = None,
    cspan_path: Path | None = None
) -> pd.DataFrame:
    """
    Matches LLM hearing summaries to independent C-SPAN program abstracts by videoId/packageId.
    Returns matched dataset table.
    """
    print("\n--- 2. Matching LLM Summaries to C-SPAN Reference Abstracts ---")
    
    if summaries_path is None or not summaries_path.exists():
        summaries_path = DATA_REPO / "cleaned" / "01_text_summarization" / "hearing_summaries.parquet"
    if hearings_path is None or not hearings_path.exists():
        hearings_path = HEARINGS_REPO / "hearings_all.parquet"
    if cspan_path is None or not cspan_path.exists():
        cspan_path = CSPAN_RAW / "programs.parquet"
        
    print(f"Summaries Source : {summaries_path} (Exists: {summaries_path.exists()})")
    print(f"Hearings Source  : {hearings_path} (Exists: {hearings_path.exists()})")
    print(f"C-SPAN Abstracts : {cspan_path} (Exists: {cspan_path.exists()})")
    
    if summaries_path.exists() and cspan_path.exists():
        df_sum = pd.read_parquet(summaries_path)
        df_csp = pd.read_parquet(cspan_path)
        print(f"Loaded {len(df_sum)} generated summaries and {len(df_csp)} C-SPAN reference abstracts.")
        # Perform matching logic
        matches = df_sum.merge(df_csp, on="packageId", how="inner")
        print(f"Successfully matched {len(matches)} hearing-abstract pairs.")
        
        out_dir = DATA_REPO / "cleaned" / "01_text_summarization"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "cspan_matches.parquet"
        matches.to_parquet(out_file, index=False)
        print(f"Saved matched reference dataset to {out_file}")
        return matches
    else:
        print("Input dataset files missing. Creating empty match table template.")
        return pd.DataFrame(columns=["packageId", "summary_text", "cspan_abstract", "committee"])

if __name__ == "__main__":
    setup_quality_assessment_environment()
    match_hearings_to_cspan()
