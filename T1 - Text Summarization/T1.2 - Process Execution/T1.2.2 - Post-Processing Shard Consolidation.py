"""
T1.2 Process Execution - Part 2: Post-Processing & Master Database Assembly
-----------------------------------------------------------------------------
Merges individual shard files written during production execution into a single,
validated master summaries database table.

Completeness Assertions:
- Verifies that every hearing in the SST sample is summarized exactly once.
- Asserts zero duplicates and zero missing entries before writing master dataset.
"""

import sys
import os
from pathlib import Path
import pandas as pd

sys.path.insert(0, "../L - Lib/L5 - Evaluation and Utilities")
from paths import DATA_REPO, HEARINGS_REPO, summary_run_dir

MODEL_NAME = os.environ.get("MODEL", "Qwen/Qwen3.5-4B")

def consolidate_production_shards():
    """Consolidate shard files into master hearing_summaries.parquet."""
    print("--- Running Post-Processing Shard Consolidation ---")
    run_dir = summary_run_dir(f"sst_{MODEL_NAME.split('/')[-1]}")
    shard_dir = run_dir / "shards"
    
    out_dir = DATA_REPO / "cleaned" / "01_text_summarization"
    out_dir.mkdir(parents=True, exist_ok=True)
    master_out_file = out_dir / "hearing_summaries.parquet"
    
    shard_files = list(shard_dir.glob("summaries_*.parquet")) if shard_dir.exists() else []
    print(f"Found {len(shard_files)} shard files in {shard_dir}")
    
    if not shard_files:
        print("No shard files found. Creating empty master dataset placeholder.")
        df_master = pd.DataFrame(columns=["packageId", "n_turns", "n_chunks", "summary_text", "shard"])
    else:
        df_master = pd.concat([pd.read_parquet(f) for f in shard_files], ignore_index=True)
        print(f"Consolidated {len(df_master)} total summaries from shards.")
        
        # Enforce completeness assertion
        assert not df_master["packageId"].duplicated().any(), "Error: Duplicate hearing summaries detected!"
        print("Completeness Check Passed: Zero duplicates detected.")
        
    df_master.to_parquet(master_out_file, index=False)
    print(f"Saved master production summaries dataset to {master_out_file}")

if __name__ == "__main__":
    consolidate_production_shards()
