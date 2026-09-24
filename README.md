# LLM Text Analysis and Synthesis

This repository provides an end-to-end framework for extracting low-dimensional, validated econometric measures from high-dimensional text using open-weights language models.

The methodology is demonstrated on:
1. **U.S. Congressional Science-Committee Hearings**: House Science and Senate Commerce committees (2,352 hearings, 1995–2025; 93.6 million words).
2. **S&P 500 Form 10-K Filings**: Business descriptions (Item 1) spanning 21,966 filings (1993–2025) across 25,207 CIKs.

---

## 1. Standardized Directory & Task Architecture

The codebase is organized into intuitive, self-contained sections:

```
.
├── D1 - Data Collection and Processing/               # Data ingestion, metadata parsing, and sample construction
│   ├── Data Collection Overview.md
│   ├── D1.1 - GovInfo Congressional Hearings/        # Enumerate, download, parse MODS XML & build hearing corpus
│   ├── D1.2 - C-SPAN Reference Abstracts/            # Query C-SPAN Archives for human editorial abstracts
│   ├── D1.3 - SEC Form 10-K Corporate Filings/       # Bulk 10-K downloads, indexing & item extraction
│   └── D1.4 - SST Sample Construction/               # Space, Science & Technology benchmark sample build
│
├── T1 - Text Summarization/                          # Task 1: Long-document hierarchical Map-Reduce summarization
│   ├── Text Summarization Workflow Overview.ipynb    # Comprehensive technical and workflow overview
│   ├── T1.1 - Process Prototyping and Evaluation/    # Model setup, token chunking & draft execution (Python)
│   ├── T1.2 - Process Execution/                     # 10-shard batch execution & master parquet consolidation (Python)
│   ├── T1.3 - Quality Assessment/                    # C-SPAN embedding discriminant evaluation (Python)
│   ├── T1.X - Background Helper Functions/           # chunking.py, summarize.py
│   └── T1.X - Worked Example/                       # Zuckerberg hearing: inputs, summaries, logs, and scripts
│
├── T2 - Topic Extraction and Stance Analysis/        # Task 2: Congressional topic extraction & stance panel
│   ├── Topic Extraction Workflow Overview.ipynb      # Comprehensive technical and workflow overview
│   ├── T2.1 - Process Prototyping and Evaluation/    # Turn attribution & few-shot promptbook testing (Python)
│   ├── T2.2 - Process Execution/                     # Track 1/Track 2 batch extraction & codebook freeze (Python)
│   ├── T2.3 - Quality Assessment/                    # CAP codebook crosswalk alignment & audit (Python)
│   ├── T2.X - Background Helper Functions/           # stance.py, constrained.py, speakers.py
│   └── T2.X - Worked Example/                       # Same hearing: topics, stances, codebook, logs, and scripts
│
├── T3 - Topic Relevance and Corporate Disclosure/    # Task 3: Dual-instrument corporate disclosure topic relevance
│   ├── Topic Relevance Workflow Overview.ipynb       # Comprehensive technical and workflow overview
│   ├── T3.1 - Process Prototyping and Evaluation/    # Sentence segmentation & centroid scoring prototyping (Python)
│   ├── T3.2 - Process Execution/                     # Dual-instrument batch tagging & Compustat panel (Python)
│   ├── T3.3 - Quality Assessment/                    # Gold-standard gate audit & agreement analysis (Python)
│   ├── T3.X - Background Helper Functions/           # tagging.py, relevance.py, item1_local.py
│   └── T3.X - Worked Example/                       # Same hearing: privacy relevance across eligible firms
│
├── L - Lib/                                          # Centralized core Python software library (L1 to L5)
├── R - Results/                                      # Evaluation results and categorized figure outputs
│   └── figures/                                      # Subdivided by D1, T1, T2, T3
└── B - Backup of Original File Structure/            # Complete preserved backup of initial scripts
```

Follow the April 10, 2018 Zuckerberg hearing through the [T1 summarization example](<T1 - Text Summarization/T1.X - Worked Example/README.md>), [T2 topic and stance example](<T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/README.md>), and [T3 firm-relevance example](<T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/README.md>). Each example has a README walkthrough and numbered folders for inputs, outputs, logs and verification, and scripts. T3 follows the hearing's privacy topic across all 998 eligible preceding firm disclosures, with Facebook and ResMed as two illustrations.

---

## 2. Summary of What Was Done in Each Process Stage

### A. Data Collection & Processing (`D1`)
- **GovInfo Hearing Corpus**: Built an enumeration contract via `offsetMark` pagination to avoid shifting drops across 36,378 packages (1995–2025). Parsed MODS XML metadata to extract BioGuide member rosters and applied a 4-space indent paragraph rule to attribute speaker turns.
- **C-SPAN Reference Summaries**: Queried C-SPAN Archives API across three committee categories (`House Committee`, `Senate Committee`, `Joint Committee`) to acquire 18,697 human-written editorial abstracts.
- **SEC Form 10-K Filings**: Acquired 394 monthly bulk ZIP archives (~34 GB) containing 305,140 filings. Linked CIKs to Compustat GVKEYs and extracted Item 1 (Business), Item 1A (Risk Factors), and Item 7 (MD&A).

### B. Task 1: Long-Document Text Summarization (`T1`)
- **Problem**: Congressional transcripts average ~49,000 tokens (up to 376,848 tokens), exceeding standard context windows.
- **Methodology**: Implemented **turn-aware chunking** (packing whole turns without mid-speech splits) paired with a 3-prompt Map-Reduce architecture (`Map` $\to$ `Collapse` $\to$ `Reduce`).
- **Model Choice**: Selected unquantized **`Qwen/Qwen3.5-4B`** in 16-bit `bf16` precision (identified **57 checkable claims** vs. 11 generic claims for `Llama-3.2-3B`).
- **Execution & Output**: Executed 10 parallel disjoint shards over 2,352 SST hearings (~121 GPU hours) and consolidated outputs into master **`hearing_summaries.parquet`**.
- **Quality Evaluation**: Validated summaries against independent C-SPAN abstracts using `bge-large-en-v1.5` sentence embeddings. The 3-way discriminant test confirmed high specificity for target hearings (Same Document $\rho = 0.742$ vs. Different Committee $\rho = 0.384$), generating `cosine_similarity_averages.pdf`.

### C. Task 2: Topic Extraction & Stance Analysis (`T2`)
- **Methodology**: Evaluated congressional member speaking turns through dual tracks: Track 1 (schema-constrained token masking via `jsonformer`) and Track 2 (open extraction with robust regex parsing).
- **Execution & Output**: Consensus clustered extracted topic strings into a **111-topic ratified policy codebook** (`frozen_codebook_111.parquet`) and assembled the longitudinal dataset **`member_stance_panel.parquet`**.
- **Quality Evaluation**: Crosswalked extracted topics against the Comparative Agendas Project (CAP) ground truth, achieving a **92.4% mean rank percentile** and **0.887 top-3 precision**. Generated polarization network and attention figures in `R - Results/figures/T2/`.

### D. Task 3: Topic Relevance & Corporate Disclosure (`T3`)
- **Methodology**: Constructed two independent instruments to identify corporate exposure to policy topics:
  1. *Deterministic Embedding Rail*: Cosine similarity between 10-K sentence embeddings and policy centroids (no generation inference).
  2. *Sentence-Block LLM Tagging*: Classifies relevance, confidence, and opportunity/threat direction with index-cited quotes.
- **Execution & Output**: Processed 21,966 S&P 500 Form 10-K Business sections and merged with Compustat fundamentals to build **`firm_topic_relevance_panel.parquet`**.
- **Quality Evaluation**: Audited against hand-verified gold annotations (**93.4% precision**, **91.2% recall**). Exported industry exposure and longitudinal trend figures to `R - Results/figures/T3/`.

---

## 3. Core Output Artifacts

| Output Table / Asset | Directory Location | Description |
| :--- | :--- | :--- |
| `hearing_summaries.parquet` | `data/cleaned/01_text_summarization/` | Master table of 2,352 entity-attributed hearing summaries |
| `frozen_codebook_111.parquet` | `data/cleaned/02_topic_extraction/` | 111-topic ratified policy codebook definitions |
| `member_stance_panel.parquet` | `data/cleaned/02_topic_extraction/` | Longitudinal congressional member-topic stance panel |
| `firm_topic_relevance_panel.parquet` | `data/cleaned/03_topic_relevance/` | S&P 500 firm-year policy exposure and opportunity/threat scores |
| Evaluation Figures | `R - Results/figures/` | PDF, SVG, and PNG evaluation figures categorized by task |
