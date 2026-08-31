"""
C-SPAN Data Collection Script
------------------------------
Collects congressional committee program abstracts from the C-SPAN Archives API
to serve as reference summaries.
"""

import os
import time
from pathlib import Path
import requests

BASE_URL = "https://api.c-spanarchives.org/2.0"
CATEGORIES = ["House Committee", "Senate Committee", "Joint Committee"]

def load_api_key(env_file: Path | None = None) -> str:
    key = os.environ.get("CSPAN_API_KEY")
    if key:
        return key
    if env_file and env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("CSPAN_API_KEY="):
                return line.split("=", 1)[1].strip('"\'')
    raise RuntimeError("CSPAN_API_KEY not found in environment or .env file.")

def collect_cspan_programs(year: int, category: str, api_key: str, output_dir: Path):
    """Query C-SPAN Archives API for committee programs in a given year."""
    output_dir.mkdir(parents=True, exist_ok=True)
    query = f'category:"{category}" AND date:[{year}-01-01T00:00:00Z TO {year}-12-31T23:59:59Z]'
    
    url = f"{BASE_URL}/programs/search"
    params = {
        "q": query,
        "key": api_key
    }
    
    print(f"Querying C-SPAN for {category} ({year})...")
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        programs = data.get("programs", [])
        print(f"Retrieved {len(programs)} programs for {category} ({year}).")
        # Save output JSONL or JSON
        output_file = output_dir / f"{category.lower().replace(' ', '_')}_{year}.json"
        import json
        output_file.write_text(json.dumps(data, indent=2))
    else:
        print(f"Failed C-SPAN request: {res.status_code}")

if __name__ == "__main__":
    print("C-SPAN Collection Script Template")
