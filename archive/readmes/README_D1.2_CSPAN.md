# C-SPAN Reference Abstracts: Collection & Processing

This folder contains the pipeline for querying C-SPAN Archives to collect human-written editorial abstracts of congressional committee hearings.

---

## Data Lifecycle & Notebook Pipeline

### 1. Identification & Retrieval (`06_collect_cspan.ipynb`)
- **API Endpoint**: `GET /2.0/programs/search` via C-SPAN Archives API (`api.c-spanarchives.org`).
- **Logic**:
  - Queries Lucene ISO date ranges for three specific committee categories (`House Committee`, `Senate Committee`, `Joint Committee`).
  - Follows cursor pagination to pull program titles, program IDs (`videoId`), dates, and human-written abstracts (~48 words median length).
- **Outputs**: Category-year JSONL files (`{category}_{year}.jsonl`) and merged `programs.parquet` reference summary table.
