"""
C-SPAN Data Processing Script
-----------------------------
Processes collected C-SPAN program abstracts into standardized reference datasets.
Replicates logic from scripts/python/01_dataset_construction/06_collect_cspan.ipynb & lib/cspan.py.
"""

import json
from pathlib import Path
from typing import Any

def process_cspan_file(json_file: Path) -> list[dict[str, Any]]:
    """Process raw C-SPAN search JSON or JSONL file into clean program rows."""
    if not json_file.exists():
        return []
        
    records = []
    content = json_file.read_text(encoding="utf-8")
    
    if json_file.suffix == ".jsonl":
        for line in content.splitlines():
            if line.strip():
                records.append(json.loads(line))
    else:
        data = json.loads(content)
        records = data.get("programs", [])
        
    processed = []
    for r in records:
        abstract = r.get("description") or r.get("abstract") or ""
        words = abstract.split()
        
        processed.append({
            "program_id": r.get("id"),
            "title": r.get("title"),
            "abstract": abstract,
            "word_count": len(words),
            "date": r.get("date"),
            "category": r.get("category"),
            "video_link": r.get("videoLink")
        })
        
    return processed

def merge_cspan_datasets(input_dir: Path, output_file: Path):
    """Consolidate per-category C-SPAN files into a single merged collection."""
    all_programs = []
    for f in input_dir.glob("*.json*"):
        all_programs.extend(process_cspan_file(f))
        
    print(f"Total C-SPAN reference program abstracts processed: {len(all_programs)}")
    
    # Save as JSON / Parquet
    if output_file.suffix == ".parquet":
        try:
            import pandas as pd
            df = pd.DataFrame(all_programs)
            df.to_parquet(output_file, index=False)
            print(f"Saved merged Parquet dataset to {output_file}")
        except ImportError:
            print("Pandas/pyarrow not installed. Saving fallback JSON.")
            output_file.with_suffix(".json").write_text(json.dumps(all_programs, indent=2))
    else:
        output_file.write_text(json.dumps(all_programs, indent=2))

if __name__ == "__main__":
    print("C-SPAN Data Processing Script")
