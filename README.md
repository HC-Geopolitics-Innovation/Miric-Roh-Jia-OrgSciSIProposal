
## *Accompanying Github Page for Organization Science Paper Submsision* ##


# Opening the Black Box of Large Language Models in Text-based Measurement: Staged Pipelines with Verifiable Checkpoints



**Milan Miric, Albert Roh, Nan Jia**  
*University of Southern California, Marshall School of Business*  
**Proposal for Special Issue:** AI-Enabled Frontiers in Organizational Science (*Organization Science*)  


---
---

## Main PProposal Documents

| Document | Format | Description |
| :--- | :--- | :--- |
| **[P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)** | Markdown (`.md`) | Core proposal text, interactive figure links, and online appendices |
| **[P2. Org Sci Proposal [Miric, Roh and Jia][PDF].pdf](P%20-%20Paper,%20Writing%20and%20Output/P2.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BPDF%5D.pdf)** | PDF (16 pages) | Camera-ready proposal + appendices compiled via LaTeX |
| **[P3. Org Sci Proposal - Full Methodology [Miric, Roh and Jia].md](P%20-%20Paper,%20Writing%20and%20Output/P3.%20Org%20Sci%20Proposal%20-%20Full%20Methodology%20%5BMiric,%20Roh%20and%20Jia%5D.md)** | Markdown (`.md`) | Comprehensive methodological architecture and technical extensions |

---

## Abstract

Researchers increasingly use large language models (LLMs) to construct variables from long, noisy documents that were previously impractical to study at scale. When an LLM is used end to end, however, the final output is the only observable checkpoint. This opacity makes measures hard to validate and reproduce, and it conceals heterogeneity within documents, so systematic measurement error can bias subsequent analyses. More capable models will not resolve these concerns, because they stem from opacity and lack of control over design choices rather than limited capability. We propose decomposing LLM-based measurement into a pipeline of discrete stages, each producing an inspectable intermediate output. This design allows researchers to validate each stage against its own benchmark, locate where errors arise, revise one stage while reusing the others, and trace aggregate measures back to their components. We demonstrate the approach by processing 2,352 congressional hearings and firms’ 10-K filings to summarize hearings, extract policymakers’ stances, and measure firms’ exposure to the debate over consumer data privacy. Across 1,058 publicly traded firms, we demonstrate how the most exposed firms as reflected in our index experience a shift in their innovation trajectory towards both data anonymization and user-activity tracking. We aim to release the modular code and intermediate datasets, enabling researchers to adapt the pipeline with coding agents and to replicate it stage by stage.

---

## Repository Structure

```
.
├── D - Data Collection and Processing/                # Raw corpus ingestion (GovInfo hearings, C-SPAN abstracts, SEC 10-K, SST)
│   ├── Data Collection Workflow Overview.ipynb
│   ├── D1 - GovInfo Congressional Hearings/
│   ├── D2 - C-SPAN Reference Abstracts/
│   ├── D3 - SEC Form 10-K Corporate Filings/
│   └── D4 - SST Sample Construction/
├── T - Three Step Text Analysis Pipeline/             # The three pipeline steps, one folder per step; results mirror this tree
│   ├── T1 - Text Summarization/                       # Task 1: Long-document turn-aware chunking and Map-Reduce summarization
│   ├── T2 - Topic Extraction and Stance Analysis/     # Task 2: 111-topic policy taxonomy codebook and legislator stance panel
│   └── T3 - Topic Relevance and Corporate Disclosure/ # Task 3: Firm 10-K topic relevance to the consumer data privacy debate
├── X1 - Example of Research Enabled by LLM Pipeline/  # Empirical application: topic relevance and privacy patents around 2016
│   ├── Data/                                          # The privacy patent file, the firm relevance file, and the privacy code lists
│   ├── X1.1 - Patent Data - Sample Firm Patents and Privacy Codes/
│   └── X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM/
├── X2 - Example of Reproducing and Adapting the Research Pipeline/ # Autonomous coding agent prompt and implementation plan
├── P - Paper, Writing and Output/                     # Main proposal documents, compiled PDFs, and methodology drafts
│   ├── P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md
│   ├── P2. Org Sci Proposal [Miric, Roh and Jia][PDF].pdf
│   ├── P2. Org Sci Proposal [Miric, Roh and Jia][PDF].tex
│   ├── P3. Org Sci Proposal - Full Methodology [Miric, Roh and Jia].md
│   ├── Proposal_for_Org_Sci_101126_AR.md
│   ├── [TEMP_for_Review]_Proposal_for_Org_Sci_103026_AR.md
│   ├── figures/                                       # Rendered figures for proposal and appendices
│   └── pdfs/                                          # Component PDFs (main.pdf, appendix.pdf)
├── R - Results/                                       # Figures and tables, one folder per notebook, in a tree that mirrors D, T, and X1
│   ├── figures/
│   └── tables/
└── J - Jobs/                                          # SLURM scripts of the GPU runs
```

Each pipeline step opens with a workflow overview notebook and ends with a running example that follows the same hearing, the April 10, 2018 Facebook hearing with Mark Zuckerberg: the [T1 summarization example](<T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>), the [T2 topic and stance example](<T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>), and the [T3 firm-relevance example](<T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>). Each example has a README walkthrough, a step-by-step notebook, and numbered folders for inputs, outputs, and logs.

### Detailed Paths for Proposal Documents (`P - Paper, Writing and Output/`):
- **Core Markdown Proposal**: [`P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md`](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)
- **Combined PDF (Proposal + Appendices)**: [`P2. Org Sci Proposal [Miric, Roh and Jia][PDF].pdf`](P%20-%20Paper,%20Writing%20and%20Output/P2.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BPDF%5D.pdf) (Source: [`P2. Org Sci Proposal [Miric, Roh and Jia][PDF].tex`](P%20-%20Paper,%20Writing%20and%20Output/P2.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BPDF%5D.tex))
- **Full Methodology Document**: [`P3. Org Sci Proposal - Full Methodology [Miric, Roh and Jia].md`](P%20-%20Paper,%20Writing%20and%20Output/P3.%20Org%20Sci%20Proposal%20-%20Full%20Methodology%20%5BMiric,%20Roh%20and%20Jia%5D.md)
  - *Methodology Integration Sources*: [`Proposal_for_Org_Sci_101126_AR.md`](P%20-%20Paper,%20Writing%20and%20Output/Proposal_for_Org_Sci_101126_AR.md) and [`[TEMP_for_Review]_Proposal_for_Org_Sci_103026_AR.md`](P%20-%20Paper,%20Writing%20and%20Output/%5BTEMP_for_Review%5D_Proposal_for_Org_Sci_103026_AR.md)
- **Figures Directory**: [`P - Paper, Writing and Output/figures/`](P%20-%20Paper,%20Writing%20and%20Output/figures/)
- **Individual Component PDFs**: [`P - Paper, Writing and Output/pdfs/`](P%20-%20Paper,%20Writing%20and%20Output/pdfs/) ([`main.pdf`](P%20-%20Paper,%20Writing%20and%20Output/pdfs/main.pdf), [`appendix.pdf`](P%20-%20Paper,%20Writing%20and%20Output/pdfs/appendix.pdf))

---

## Key Empirical Figures

All figures below are displayed side by side as presented in the proposal. Click on any figure or heading to jump directly to its discussion and complete econometric notes in [`P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md`](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md).

### [Figure 2. Topics and Overview of Stance (Panels A & C)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)

| [Panel A: Distribution of Member Net Stances](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel C: Subtopic Polarization](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 2 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig2_panel_a.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 2 Panel C](P%20-%20Paper,%20Writing%20and%20Output/figures/fig2_panel_c.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

### [Figure 3. Topic Relevance Scores for Publicly Listed Firms](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)

| [Panel A: NAICS-2 Sector Cosine Relative to Mean](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Selected High and Low Relevance Firms](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 3 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig3_panel_a_naics_relevance.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 3 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig3_panel_b_top_firms.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

### [Figure 4. Firm Topic Relevance and Privacy Patenting Pre- and Post-2016](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)

| [Panel A: Distribution & Patent Intensity](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Pre/Post 2016 by Quartile](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel C: Pre/Post 2016 by Subclass](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: | :---: |
| [![Figure 4 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_panel_a_topic_relevance.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 4 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_panel_b_quartiles.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 4 Panel C](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_panel_c_subclasses.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

### [Figure 5. Long-Term Trends and Firm Concentration in Privacy Patenting (1999–2021)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)

| [Panel A: Annual Patents by Topic Group](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Top 20 Privacy Patenting Firms](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 5 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig8a_raw_counts.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 5 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig9_top_firms.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

### [Figure 6. Annual Event-Study Estimates of Patenting Probability by Topic Relevance Quartile](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)

| [Panel A: Anonymizing / Decorrelating Data](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Tracking User Activity](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 6 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig6_panel_a_anonymizing.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 6 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig6_panel_b_tracking.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

---

## Summary of Processing Stages

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
- **Quality Evaluation**: Crosswalked extracted topics against the Comparative Agendas Project (CAP) ground truth, achieving a **92.4% mean rank percentile** and **0.887 top-3 precision**. Generated polarization network and attention figures in `R - Results/figures/`.

### D. Task 3: Topic Relevance & Corporate Disclosure (`T3`)
- **Methodology**: Constructed two independent instruments to identify corporate exposure to policy topics:
  1. *Deterministic Embedding Rail*: Cosine similarity between 10-K sentence embeddings and policy centroids (no generation inference).
  2. *Sentence-Block LLM Tagging*: Classifies relevance, confidence, and opportunity/threat direction with index-cited quotes.
- **Execution & Output**: Processed 21,966 S&P 500 Form 10-K Business sections and merged with Compustat fundamentals to build **`firm_topic_relevance_panel.parquet`**.
- **Quality Evaluation**: Audited against hand-verified gold annotations (**93.4% precision**, **91.2% recall**). Exported industry exposure and longitudinal trend figures to `R - Results/figures/`.

---

## Core Output Artifacts

| Output Table / Asset | Directory Location | Description |
| :--- | :--- | :--- |
| `hearing_summaries.parquet` | `data/cleaned/01_text_summarization/` | Master table of 2,352 entity-attributed hearing summaries |
| `frozen_codebook_111.parquet` | `data/cleaned/02_topic_extraction/` | 111-topic ratified policy codebook definitions |
| `member_stance_panel.parquet` | `data/cleaned/02_topic_extraction/` | Longitudinal congressional member-topic stance panel |
| `firm_topic_relevance_panel.parquet` | `data/cleaned/03_topic_relevance/` | S&P 500 firm-year policy exposure and opportunity/threat scores |
| Evaluation Figures | `R - Results/figures/` | PDF, SVG, and PNG evaluation figures categorized by task |
