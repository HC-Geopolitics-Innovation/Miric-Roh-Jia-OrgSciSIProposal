# External Data Collection & Download Summary

This document highlights all external data collection and download activities identified across the scripts in [`scripts/python/01_dataset_construction`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/01_dataset_construction).

---

## 1. Overview Table of External Data Collection

| Data Source / Provider | Script Name(s) | API / Endpoint / Method | Credentials Required | Data / Files Collected | Purpose in Pipeline |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GovInfo API** (U.S. GPO) | [`01_enumerate_hearings.ipynb`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/01_dataset_construction/01_enumerate_hearings.ipynb) | `GET https://api.govinfo.gov/published/{start}/{end}?collection=CHRG` (Paginated via `offsetMark`) | `GOVINFO_API_KEY` | Metadata manifest for CHRG packages (1995–2025): `packageId`, `dateIssued`, `lastModified`, `congress`, `docClass`, `title`. | Enumerates the full universe of congressional hearings to construct the baseline manifest. |
| **GovInfo API** (U.S. GPO) | [`02_download_hearings.ipynb`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/01_dataset_construction/02_download_hearings.ipynb) | `GET https://api.govinfo.gov/packages/{packageId}/mods`<br>`GET https://api.govinfo.gov/packages/{packageId}/htm` | `GOVINFO_API_KEY` | MODS XML metadata records & HTML transcript files for each CHRG package. | Retrieves raw text transcripts and structured metadata (roster, committees, witnesses). |
| **C-SPAN Archives API** | [`06_collect_cspan.ipynb`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/06_collect_cspan.ipynb) | `GET https://api.c-spanarchives.org/2.0/programs/search`<br>`GET https://api.c-spanarchives.org/2.0/programs/{id}` (Optional detail call) | `CSPAN_API_KEY` | Program abstracts, program titles, dates, video links, `videoId`, and category information. | Provides independent human-written abstracts as reference summaries. |
| **SEC-API.io** (Bulk Dataset) | [`07_download_10k_bulk.ipynb`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/07_download_10k_bulk.ipynb) | `GET https://api.sec-api.io/datasets/form-10k-content.json`<br>`GET https://api.sec-api.io/datasets/form-10k-content/{year}/{month}.zip` | `SEC_API_KEY` | 394 monthly ZIP archives (34 GB total, ~305,140 annual reports from Oct 1993 to present) containing raw filing documents & `metadata.json`. | Primary bulk repository for SEC Form 10-K filings and firm filing index. |
| **SEC-API.io** (Extractor API) | [`09_extract_10k_items.ipynb`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/09_extract_10k_items.ipynb) | Extractor API endpoint via `sec-api` library / REST endpoint taking SEC filing URLs. | `SEC_API_KEY` | Individual text sections/items from 10-K filings (e.g., Item 1, Item 1A, Item 7). | Extracts parsed, structured item text (e.g., Business description, Risk Factors, MD&A). |

---

## 2. Detailed Breakdown by Collection Source

### A. Congressional Hearing Transcripts & Metadata (GovInfo API)
- **Primary Helper Module**: [`lib/govinfo.py`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/lib/govinfo.py)
- **Authentication**: Key passed via `X-Api-Key` HTTP header (configured via `GOVINFO_API_KEY` in `.env`).
- **Pacing & Constraints**: Default rate limit of ~10 requests/sec. Handles pagination strictly via `offsetMark` cursors to avoid missing modified entries.
- **Downloaded Content**:
  - Package listings (`CHRG` collection between 1995 and 2025).
  - MODS metadata records (used by notebook `03` for participant roster, committee, and witness extraction).
  - Raw HTML transcripts.

### B. Reference Summaries (C-SPAN Archives API)
- **Primary Helper Module**: [`lib/cspan.py`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/lib/cspan.py)
- **Authentication**: Key passed via `CSPAN_API_KEY` in `.env`.
- **Pacing & Constraints**: Default rate limit of 2 requests/sec.
- **Downloaded Content**:
  - Editorial abstracts for congressional committee hearings across three main categories (`House Committee`, `Senate Committee`, `Joint Committee`).
  - Search metadata (`id`, `title`, `description`, `date`, `videoLink`).

### C. Corporate SEC Form 10-K Filings (SEC-API.io)
- **Primary Helper Module**: [`lib/secapi.py`](file:///Users/milanmiric/Documents/Research/Active%20Papers/LLM%20Text%20Sumarization%20and%20Data%20Extraction/scripts/python/lib/secapi.py)
- **Authentication**: Key passed via `SEC_API_KEY` in `.env`.
- **Pacing & Constraints**: Target aggregate rate of 7.0 requests/sec. Account-wide rate limiting ceiling around 8.8 req/sec (HTTP 429 retried with 0.25s constant pause).
- **Downloaded Content**:
  - Bulk monthly 10-K containers from 1993 to present (~34 GB).
  - Specific extracted items (Item 1: Business Description, Item 1A: Risk Factors, Item 7: MD&A, etc.).

---

## 3. Storage & Environment Configuration

- **Environment File**: `.env` (gitignored, initialized from `.env.example`).
- **Data Destination**: Bulk data files, raw HTML, ZIPs, and Parquet manifests land outside git (e.g. `/scratch2/$USER/projects/llm_method/data/raw/...` or gitignored `./data/` & `./interim/` directories).
