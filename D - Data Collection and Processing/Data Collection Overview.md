# Data Collection and Processing Overview

This document provides a comprehensive overview of the datasets collected, the data pipeline methodology, and the folder structure within `D - Data Collection and Processing`.

---

## 1. Overview of Datasets Collected

| Data Source | Primary Content | Provider / API | Collection Window | Primary Identifiers | Key Outputs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GovInfo Congressional Hearings** | U.S. Congressional Hearing Package Manifests, MODS XML Roster Metadata, and HTML Transcripts | U.S. Government Publishing Office (GovInfo API) | 1995 – 2025 | `packageId` (e.g. `CHRG-109hhrg...`), `congress`, BioGuide IDs | `packages_all.parquet`, `hearings.parquet`, `hearing_members.parquet`, `hearings_all.parquet` |
| **C-SPAN Reference Abstracts** | Editorial Summaries for House, Senate, and Joint Committee Programs | C-SPAN Archives API (`api.c-spanarchives.org`) | 1995 – 2025 | `videoId`, `program_id`, Category | `programs.parquet` (Reference abstracts for LLM summary evaluation) |
| **SEC Form 10-K Corporate Filings** | Bulk 10-K Annual Report Containers & Extracted Section Items (Item 1, 1A Risk Factors, Item 7 MD&A) | SEC-API.io (Bulk & Extractor APIs) | 1993 – Present | `cik`, `accessionNo`, `gvkey`, `fyear` | `form10k_index.json`, `filings.parquet`, `sample_firms.parquet`, Extracted item text files |
| **SST Demonstration Sample** | Filtered sample of hearings & filings for benchmark evaluation | Internal Processing | Pipeline subsets | `packageId`, `cik` | Demonstration benchmark sample tables |

---

## 2. Complete File & Directory Structure

```
D - Data Collection and Processing/
├── Data Collection Overview.md                     # Overview of collected datasets and structure
├── .env.example                                    # Template for API credentials (GOVINFO_API_KEY, CSPAN_API_KEY, SEC_API_KEY)
│
├── D1 - GovInfo Congressional Hearings/
│   ├── D1.1 - GovInfo - Enumerate Hearings.ipynb    # Identification: Cursor pagination walk via offsetMark to enumerate 36k+ packages
│   ├── D1.2 - GovInfo - Download Hearings.ipynb     # Acquisition: Fetching MODS XML metadata records & HTML transcripts
│   ├── D1.3 - GovInfo - Parse MODS Metadata.ipynb   # Metadata Parsing: Extracting committee rosters, BioGuide member IDs & witnesses
│   └── D1.4 - GovInfo - Build Hearing Corpus.ipynb  # Cleaning & Assembly: 4-space paragraph turn attribution and corpus table build
│
├── D2 - C-SPAN Reference Abstracts/
│   └── D2.1 - C-SPAN - Collect Reference Abstracts.ipynb # Retrieval: Searching committee categories & compiling evaluation reference abstracts
│
├── D3 - SEC Form 10-K Corporate Filings/
│   ├── D3.1 - SEC 10-K - Download Bulk Containers.ipynb # Acquisition: Downloading 394 monthly bulk ZIP archives (~34 GB)
│   ├── D3.2 - SEC 10-K - Build Filing Index & Linkage.ipynb # Indexing & Linkage: Parsing metadata.json & merging CIK/GVKEY with Compustat
│   ├── D3.3 - SEC 10-K - Extract 10-K Items.ipynb  # Extraction: Extracting Item 1, Item 1A (Risk Factors), Item 7 (MD&A) text
│   └── D3.4 - SEC 10-K - Assemble SP500 Item 1 Panel.ipynb # Assembly: Constructing S&P 500 firm annual panel
│
└── D4 - SST Sample Construction/
    └── D4.1 - SST - Build SST Sample.ipynb          # Sample Assembly: Filtering benchmark evaluation sample
```

---

## 3. Data Lifecycle & Processing Steps

1. **Identification & Enumeration**: Generating complete, non-shifting manifest contracts using cursor-based pagination.
2. **Acquisition & Bulk Storage**: Downloading raw structured XML, HTML, and ZIP containers with verification against API metadata count totals.
3. **Parsing & Cleaning**: Attributing speaker turns (using 4-space indent rules) and extracting structured entity rosters (members, witnesses, committees).
4. **Extraction & Panel Linking**: Isolating specific text sections (e.g. 10-K Item 1A Risk Factors) and linking corporate CIKs with CRSP-Compustat GVKEY identifiers.
