"""
SEC Data Processing Script
--------------------------
Builds filing indices, processes extracted items (Item 1, 1A, 7), and merges firm mappings.
Replicates logic from scripts/python/01_dataset_construction/08_build_filing_index.ipynb, 09_extract_10k_items.ipynb, & lib/secapi.py.
"""

import json
import zipfile
from pathlib import Path
from typing import Any

# Form types considered valid annual reports
ANNUAL_REPORT_FORMS = {"10-K", "10-K405", "10KSB", "10KSB40", "10-KT"}

def build_filing_index_from_zip(zip_path: Path) -> list[dict[str, Any]]:
    """Inspect metadata.json inside bulk monthly ZIP containers without unzipping full contents."""
    if not zip_path.exists():
        return []
        
    filings = []
    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if name.endswith("metadata.json"):
                data = json.loads(z.read(name).decode("utf-8"))
                form_type = data.get("formType", "")
                
                # Filter for annual report form variants
                if form_type in ANNUAL_REPORT_FORMS:
                    filings.append({
                        "cik": data.get("cik"),
                        "form_type": form_type,
                        "period_of_report": data.get("periodOfReport"),
                        "filed_at": data.get("filedAt"),
                        "company_name": data.get("companyName"),
                        "ticker": data.get("ticker"),
                        "sec_url": data.get("linkToFilingDetails")
                    })
                    
    return filings

def process_extracted_item_file(item_file: Path) -> dict[str, Any]:
    """Process an extracted Item text file (e.g. Item 1A Risk Factors)."""
    if not item_file.exists():
        return {"text": "", "char_count": 0, "is_empty": True}
        
    text = item_file.read_text(encoding="utf-8", errors="ignore").strip()
    return {
        "accession_no": item_file.stem,
        "text": text,
        "char_count": len(text),
        "is_empty": len(text) == 0
    }

if __name__ == "__main__":
    print("SEC Data Processing Script")
