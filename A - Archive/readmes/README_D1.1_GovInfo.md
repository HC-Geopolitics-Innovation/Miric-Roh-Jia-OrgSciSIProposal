# GovInfo Congressional Hearings: Collection, Cleaning & Extraction

This folder contains the complete pipeline for identifying, downloading, parsing, cleaning, and assembling the U.S. Congressional Hearing corpus (`CHRG` collection from 1995 to 2025).

---

## Data Lifecycle & Notebook Pipeline

### 1. Identification & Enumeration (`01_enumerate_hearings.ipynb`)
- **API Endpoint**: `GET /published/{start}/{end}?collection=CHRG` via GovInfo API.
- **Logic**: Queries calendar years 1995–2025 using `offsetMark` pagination to prevent records from shifting mid-walk.
- **Output**: Year-by-year Parquet manifests (`packages_{year}.parquet`) and master list (`packages_all.parquet`).

### 2. Download & File Acquisition (`02_download_hearings.ipynb`)
- **Endpoints**:
  - `GET /packages/{packageId}/mods` (MODS XML metadata)
  - `GET /packages/{packageId}/htm` (Raw text HTML transcript)
- **Logic**: Downloads MODS and HTML files for each package in the manifest contract, logging missing renditions (e.g. stubs without full text).

### 3. Metadata Parsing & Roster Extraction (`03_parse_mods.ipynb`)
- **Logic**: Parses XML using `lib/mods.py` to extract:
  - Hearing metadata & committees (`congCommittee`, preserving joint hearing lists).
  - Member rosters (`congMember` BioGuide IDs & names) required for speaker attribution.
  - Witness names.
  - Digitization availability markers (`<TEXT NOT AVAILABLE>`).
- **Outputs**: `hearings.parquet`, `hearing_committees.parquet`, `hearing_members.parquet`.

### 4. Transcript Cleaning & Corpus Assembly (`04_build_hearing_corpus.ipynb`)
- **Logic**: Reads raw HTML transcripts:
  - Applies 4-space paragraph indent rule (with blank-line fallback) to identify speaking turn boundaries.
  - Groups paragraphs into speaking turns and attaches MODS participant metadata.
- **Output**: Master parsed hearing table `hearings_all.parquet`.
