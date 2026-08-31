"""
GovInfo Data Collection Script
------------------------------
Enumerates and downloads U.S. Congressional Hearing (CHRG) packages and metadata
from the GovInfo API.
"""

import os
import time
from pathlib import Path
import requests

BASE_URL = "https://api.govinfo.gov"

def load_api_key(env_file: Path | None = None) -> str:
    key = os.environ.get("GOVINFO_API_KEY")
    if key:
        return key
    if env_file and env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GOVINFO_API_KEY="):
                return line.split("=", 1)[1].strip('"\'')
    raise RuntimeError("GOVINFO_API_KEY not found in environment or .env file.")

def enumerate_hearings(start_year: int, end_year: int, api_key: str, output_dir: Path):
    """Enumerate hearing packages year by year using offsetMark pagination."""
    output_dir.mkdir(parents=True, exist_ok=True)
    headers = {"X-Api-Key": api_key}
    
    for year in range(start_year, end_year + 1):
        print(f"Enumerating CHRG packages for year {year}...")
        start_date = f"{year}-01-01T00:00:00Z"
        end_date = f"{year}-12-31T23:59:59Z"
        offset_mark = "*"
        
        while offset_mark:
            url = f"{BASE_URL}/published/{start_date}/{end_date}"
            params = {
                "collection": "CHRG",
                "offsetMark": offset_mark,
                "pageSize": 1000
            }
            res = requests.get(url, headers=headers, params=params)
            if res.status_code != 200:
                print(f"Error fetching page: {res.status_code}")
                break
            
            data = res.json()
            packages = data.get("packages", [])
            print(f"Retrieved {len(packages)} packages for year {year}")
            
            offset_mark = data.get("nextPage")
            time.sleep(0.1) # Rate limit padding

def download_hearing_package(package_id: str, api_key: str, output_dir: Path):
    """Download MODS metadata XML and raw HTML transcript for a package."""
    headers = {"X-Api-Key": api_key}
    pkg_dir = output_dir / package_id
    pkg_dir.mkdir(parents=True, exist_ok=True)
    
    # Download MODS XML
    mods_url = f"{BASE_URL}/packages/{package_id}/mods"
    res_mods = requests.get(mods_url, headers=headers)
    if res_mods.status_code == 200:
        (pkg_dir / "mods.xml").write_bytes(res_mods.content)
        
    # Download HTM Transcript
    htm_url = f"{BASE_URL}/packages/{package_id}/htm"
    res_htm = requests.get(htm_url, headers=headers)
    if res_htm.status_code == 200:
        (pkg_dir / "transcript.htm").write_bytes(res_htm.content)

if __name__ == "__main__":
    print("GovInfo Collection Script Template")
