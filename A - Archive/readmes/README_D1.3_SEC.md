# SEC Form 10-K Filings: Collection, Indexing & Item Extraction

This folder contains the complete pipeline for acquiring corporate Form 10-K filings from SEC-API.io, indexing firm identifiers against CRSP-Compustat, and extracting specific text sections.

---

## Data Lifecycle & Notebook Pipeline

### 1. Bulk Download (`07_download_10k_bulk.ipynb`)
- **API Endpoint**: `GET /datasets/form-10k-content.json` & `GET /datasets/form-10k-content/{year}/{month}.zip`
- **Logic**: Fetches 394 monthly ZIP archives containing ~305,140 annual reports from 1993 to present (~34 GB). Verification against byte sizes in manifest ensures complete downloads.

### 2. Indexing & Firm Linkage (`08_build_filing_index.ipynb`)
- **Logic**: Inspects `metadata.json` inside bulk ZIPs (without extracting full text files) to build a master index of CIK, accession numbers, filing dates, and SEC URLs.
- **Linkage**: Merges CIKs with CRSP-Compustat link tables (`crsp_compustat_link.dta`) to establish GVKEY mapping and fiscal year alignment.
- **Outputs**: `filings.parquet` and `sample_firms.parquet`.

### 3. Item Extraction (`09_extract_10k_items.ipynb`)
- **API Endpoint**: SEC-API Extractor REST API.
- **Logic**: Sends SEC filing URLs to extract specific numbered items: Item 1 (Business), Item 1A (Risk Factors), Item 1B, Item 1C, Item 7 (MD&A), Item 7A.
- **Outputs**: Individual text files per filing-item (`item1/{cik}/{accessionNo}.txt`) and extraction status parquet tables.

### 4. Sample Assembly (`10_assemble_sp500_item1.ipynb`)
- **Logic**: Filters extracted items for target firm panels (e.g. S&P 500 constituents across fiscal years) and prepares clean text inputs for downstream LLM evaluation.
