# Library Architecture Overview

This directory (`L - Lib`) contains the core Python backend library modules that power all data collection, transcript parsing, LLM orchestration, topic extraction, and evaluation workflows.

The original flat `lib/` directory has been categorized into intuitive subfolders below.

---

## Folder Categorization & Module Map

### `L1 - Data Collection and Network Clients`
Handles external API connections, request pacing, retries, exponential backoff, and pagination cursors.
- **`govinfo.py`**: API client for GovInfo `CHRG` hearing collection (`offsetMark` pagination cursor walk, retry budget).
- **`cspan.py`**: API client for C-SPAN Archives to query committee program reference abstracts.
- **`secapi.py`**: API client for SEC-API.io (bulk 10-K ZIP index downloads & Extractor REST API).

### `L2 - Document Parsing and Text Cleaning`
Extracts structured elements from XML/HTML documents and attributes text.
- **`mods.py`**: Parses GovInfo MODS XML records into hearing metadata, joint committees, BioGuide member rosters, and witnesses.
- **`transcript.py`**: Processes HTML transcripts using 4-space paragraph indent rules and identifies `<TEXT NOT AVAILABLE>` stubs.
- **`speakers.py`**: Attributes transcript speaking turns to specific BioGuide members using anchored surname rules.
- **`item1_local.py`**: Sentence segmentation and text block partitioning for SEC 10-K filings.

### `L3 - LLM Orchestration and Summarization`
Manages token chunking and map-reduce LLM prompt execution.
- **`summarize.py`**: Implements map-reduce summarization prompts, hierarchical reduction, and LLM call execution.
- **`chunking.py`**: Token-budgeted text chunking without splitting speaking turns across window boundaries.

### `L4 - Topic Extraction and Relevance`
Handles schema-constrained sampling, promptbook building, and topic relevance tagging.
- **`stance.py`**: Formats prompts and parses LLM outputs for member topic extraction and stance classification.
- **`tagging.py`**: Orchestrates LLM prompt execution for corporate disclosure topic relevance tagging.
- **`relevance.py`**: Calculates sentence embedding distance scores against policy topic centroids.
- **`constrained.py`**: Enables schema-constrained JSON sampling for local LLMs.
- **`jsonformer_vendor.py`**: Embedded vendor code for Jsonformer schema-constrained generation.

### `L5 - Evaluation and Utilities`
Provides evaluation metrics and path resolution across the repository.
- **`evalmetrics.py`**: Computes evaluation metrics (C-SPAN discriminant scores, CAP topic codebook accuracy).
- **`paths.py`**: Centralized single source of truth for directory paths and scratch storage locations.
