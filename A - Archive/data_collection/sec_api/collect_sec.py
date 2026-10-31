"""
SEC-API Data Collection & Item Extraction Script
------------------------------------------------
Downloads bulk 10-K datasets and extracts structured item text (Item 1, 1A, 7) via sec-api.io.
"""

import os
import time
from pathlib import Path
import requests

BASE_URL = "https://api.sec-api.io"
DATASET_INDEX = f"{BASE_URL}/datasets/form-10k-content.json"

def load_api_key(env_file: Path | None = None) -> str:
    key = os.environ.get("SEC_API_KEY")
    if key:
        return key
    if env_file and env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("SEC_API_KEY="):
                return line.split("=", 1)[1].strip('"\'')
    raise RuntimeError("SEC_API_KEY not found in environment or .env file.")

def fetch_bulk_dataset_index(api_key: str, output_dir: Path):
    """Download manifest index of bulk Form 10-K monthly ZIP files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    url = f"{DATASET_INDEX}?token={api_key}"
    res = requests.get(url)
    if res.status_code == 200:
        index_file = output_dir / "form10k_index.json"
        index_file.write_bytes(res.content)
        print("Bulk 10-K dataset index downloaded successfully.")
    else:
        print(f"Failed to download dataset index: {res.status_code}")

def download_monthly_bulk_container(year: int, month: int, api_key: str, output_dir: Path):
    """Download a single monthly bulk ZIP container."""
    output_dir.mkdir(parents=True, exist_ok=True)
    month_str = f"{month:02d}"
    url = f"{BASE_URL}/datasets/form-10k-content/{year}/{year}-{month_str}.zip?token={api_key}"
    
    dest_path = output_dir / f"{year}-{month_str}.zip"
    print(f"Downloading SEC bulk container for {year}-{month_str}...")
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved {dest_path}")
    else:
        print(f"Failed container download: {res.status_code}")

if __name__ == "__main__":
    print("SEC-API Collection Script Template")
