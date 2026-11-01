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
├── D - Data Collection and Processing/               # Data ingestion, metadata parsing, and sample construction
│   ├── Data Collection Workflow Overview.ipynb
│   ├── D1 - GovInfo Congressional Hearings/        # Enumerate, download, parse MODS XML & build hearing corpus
│   ├── D2 - C-SPAN Reference Abstracts/            # Query C-SPAN Archives for human editorial abstracts
│   ├── D3 - SEC Form 10-K Corporate Filings/       # Bulk 10-K downloads, indexing & item extraction
│   └── D4 - SST Sample Construction/               # Space, Science & Technology benchmark sample build
│
├── T - Three Step Text Analysis Pipeline/             # The three pipeline steps, one folder per step; results and scratch mirror this tree
│   │
│   ├── T1 - Text Summarization/                          # Task 1: long-document map-reduce summarization
│   │   ├── Text Summarization Workflow Overview.ipynb    # Markdown guide: flowchart, the four parts, where the data live
│   │   ├── T1.1 - Process Prototyping and Evaluation/    # Draft on two hearings; four models compared on five hearings
│   │   ├── T1.2 - Process Entire Sample Congressional Hearings/  # Sharded production run and assembly of the 2,352 summaries
│   │   ├── T1.3 - Validation of Summaries/               # C-SPAN matching and the summary-abstract similarity test
│   │   └── T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/  # One hearing step by step: inputs, outputs, log
│   │
│   ├── T2 - Topic Extraction and Stance Analysis/        # Task 2: topic codebook, legislator stances, stance by topic over time
│   │   ├── Topic Extraction Workflow Overview.ipynb      # Markdown guide: flowchart, the five parts, where the data live
│   │   ├── T2.1 - Track 1 - Topic Extraction based on Hearing Summaries/  # Topics from the summaries, clustering, the frozen codebook, the 26 groups
│   │   ├── T2.2 - Track 2 - Legislator Stance Extraction/  # Numbered turns, prompt development, sharded production, placement under topics
│   │   ├── T2.3 - Validation of Topics/                  # CAP matching and the comparison with CAP's human codes
│   │   ├── T2.4 - Stance by Topic over Time/             # Support and concern by topic group and Congress; the privacy group
│   │   └── T2.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/  # One hearing through both tracks: inputs, outputs, log
│   │
│   └── T3 - Topic Relevance and Corporate Disclosure/    # Task 3: topic relevance of each S&P 500 firm's 10-K Item 1 to consumer data privacy legislation
│       ├── Topic Relevance Workflow Overview.ipynb       # Markdown guide: flowchart, the main chain, where the data live
│       ├── T3.1 - Sample - Firms and 10-K Item 1 Filings/  # 1,058 firms, 18,779 filings, two samples
│       ├── T3.2 - Topic Side - Policy Summary of the Legislator Statements/  # 374 statements, the prompts, the model run, its check, the vector
│       ├── T3.3 - Firm Side - Summaries of the 10-K Item 1 Filings/  # segments and prompts, filing and firm summaries, their vectors
│       ├── T3.4 - Topic Relevance - Score and Figures/   # the cosine score, its distribution, sector means, selected firms
│       └── T3.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/  # the hearing's topic followed to the firms, Figure 3 in one figure
│
├── X1 - Example of Research Enabled by LLM Pipeline/   # Empirical application: topic relevance and privacy patents around 2016
│   ├── Data/                                         # The two data files of X1.2 and the three privacy code lists
│   ├── X1.1 - Patent Data - Sample Firm Patents and Privacy Codes/  # Sample firms to KPSS patents, then the CPC code match
│   └── X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM/  # Descriptive figures, topic groups, pre- and post-2016 by relevance quartile
│
├── X2 - Example of Reproducing and Adapting the Research Pipeline/  # Agent prompt and implementation plan for adapting the pipeline
│
├── J - Jobs/                                         # SLURM scripts and logs of the GPU runs
└── R - Results/                                      # Evaluation results and categorized figure outputs
    ├── figures/                                      # Subdivided by D, T1, T2, T3, X1; one folder per notebook
    └── tables/                                       # Readable tables, one folder per notebook
```

Follow the running example, the April 10, 2018 Facebook hearing with Mark Zuckerberg, through the [T1 summarization example](<T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>), [T2 topic and stance example](<T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>), and [T3 firm-relevance example](<T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>). Each example has a README walkthrough, a step-by-step notebook, and numbered folders for inputs, outputs, and logs. T3 follows the hearing's topic, consumer data privacy legislation, to the 1,058 S&P 500 firms it concerns, with the two panels of Figure 3 as one figure.

---

## 2. Summary of What Was Done in Each Process Stage

### A. Data Collection & Processing (`D`)
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
