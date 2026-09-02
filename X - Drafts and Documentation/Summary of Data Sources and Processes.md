# Summary of Data Sources and Core Processes

This document provides an integrated executive and technical synthesis of the datasets collected and the three core text analysis processes implemented across this repository.

---

## 1. Overview of Data Sources

The research methodology integrates four primary external and reference data sources:

| Data Source | Provider / Source | Scope / Volume | Key Variables & Content | Role in Pipeline |
| :--- | :--- | :--- | :--- | :--- |
| **U.S. Congressional Hearings (`CHRG`)** | U.S. Government Publishing Office (GovInfo API) | 36,378 packages (1995–2025); 2,352 hearings in Space, Science & Technology (SST) sample | Package manifests, MODS XML metadata (BioGuide IDs, committees, witness lists), raw HTML transcripts | Primary corpus for text summarization (`T1`) and member topic/stance extraction (`T2`). |
| **C-SPAN Editorial Abstracts** | C-SPAN Archives API (`api.c-spanarchives.org`) | 18,697 programs (1995–2025; median 51 words) | Program IDs (`videoId`), broadcast dates, committee categories, independent human-written abstracts | Independent reference ground truth for quality discriminant testing in `T1`. |
| **SEC Form 10-K Corporate Filings** | SEC-API.io Bulk & Extractor APIs | 394 monthly containers (~34 GB), 305,140 annual reports (1993–2025); 21,966 S&P 500 Item 1 filings | Form 10-K Business descriptions (Item 1), Risk Factors (Item 1A), MD&A (Item 7), CIK identifiers | Primary corporate corpus for policy exposure and topic relevance extraction (`T3`). |
| **Financial Fundamentals & Identifiers** | CRSP / Compustat Merged | 25,207 linked CIKs and GVKEYs | `CIK`, `GVKEY`, `LINKTYPE`, `LINKPRIM`, fiscal year end dates, S&P 500 membership | Firm-level identification and longitudinal econometric panel linking. |

---

## 2. Summary of the Three Core Processes

```
                     ┌─────────────────────────────────────────────────────────┐
                     │            D1: Data Collection & Processing             │
                     │  (GovInfo CHRG Transcripts + C-SPAN + SEC Bulk 10-Ks)   │
                     └────────────────────────────┬────────────────────────────┘
                                                  │
         ┌────────────────────────────────────────┼────────────────────────────────────────┐
         │                                        │                                        │
         ▼                                        ▼                                        ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐ ┌──────────────────────────────┐
│  T1: Long-Document Text      │ │  T2: Topic Extraction &      │ │  T3: Topic Relevance &       │
│      Summarization           │ │      Stance Analysis         │ │      Corporate Disclosure    │
├──────────────────────────────┤ ├──────────────────────────────┤ ├──────────────────────────────┤
│ • Turn-Aware Chunking        │ │ • BioGuide Turn Attribution  │ │ • Dual-Instrument Design     │
│ • Map-Reduce Architecture    │ │ • Dual-Track Batch Extraction│ │   - Embedding Distance Rail  │
│   (Map → Collapse → Reduce)  │ │   (Track 1 & Track 2)        │ │   - LLM Sentence Tagging     │
│ • Model: Qwen3.5-4B (bf16)   │ │ • 111-Topic Consensus Codebook│ │ • 21,966 S&P 500 10-K Filings│
│ • C-SPAN Discriminant Test   │ │ • CAP Benchmark Validation   │ │ • Gold-Standard Gate Audit   │
│   (Same vs Diff Committee)   │ │ • Longitudinal Stance Panel  │ │ • Compustat Panel Merge      │
└──────────────────────────────┘ └──────────────────────────────┘ └──────────────────────────────┘
```

---

### Process 1: Long-Document Hierarchical Text Summarization (`T1`)
- **Objective**: Synthesize long congressional transcripts (median ~49,000 tokens, up to 376,848 tokens) into faithful, entity-attributed summaries without attention loss or hallucination.
- **Methodology**:
  1. **Turn-Aware Chunking (`chunking.py`)**: Assembles whole speaking turns into ~4,000-token chunks, preventing speaker arguments from splitting across window boundaries (>99.7% of turns packed intact).
  2. **3-Prompt Map-Reduce Engine (`summarize.py`)**:
     - *Map Prompt*: Summarizes each turn-aware chunk, isolating claims made by each speaker.
     - *Collapse Prompt*: Condenses accumulated intermediate summaries if they exceed context limits (~18% of hearings).
     - *Reduce Prompt*: Synthesizes all segment summaries into a single cohesive hearing summary.
  3. **Model Selection**: Unquantized `Qwen/Qwen3.5-4B` in `bf16` precision (extracted **57 checkable claims** vs 11 for `Llama-3.2-3B`).
- **Quality Evaluation**: Validated against independent C-SPAN abstracts using `bge-large-en-v1.5` embeddings. A 3-way cosine discriminant test proved high specificity for the target hearing (Same Document $\rho = 0.742$ vs. Different Committee $\rho = 0.384$).
- **Key Output**: [`hearing_summaries.parquet`](../data/cleaned/01_text_summarization/hearing_summaries.parquet) (2,352 summaries) and `cosine_similarity_averages.pdf`.

---

### Process 2: Topic Extraction and Stance Analysis (`T2`)
- **Objective**: Extract low-dimensional policy topics and directional member positions (Support/Concern/Neutral) from speaker turns with index-cited evidence.
- **Methodology**:
  1. **Turn Attribution**: Links 116,000 speaking turns to BioGuide congressional member IDs using anchored surname matching (>99.8% precision).
  2. **Dual-Track Extraction**:
     - *Track 1*: Schema-constrained generation via token-level logits masking (`jsonformer` / vLLM).
     - *Track 2*: Open unconstrained extraction with fault-tolerant regex JSON recovery (99.6% parse rate).
  3. **Consensus Clustering & Codebook Freezing**: Aggregates extracted topic strings into a ratified, canonical **111-topic policy codebook** (`frozen_codebook_111.parquet`).
- **Quality Evaluation**: Crosswalked against human-coded Comparative Agendas Project (CAP) ground truth, achieving a **92.4% mean rank percentile** and **0.887 top-3 precision**.
- **Key Output**: [`member_stance_panel.parquet`](../data/cleaned/02_topic_extraction/member_stance_panel.parquet) (longitudinal member-topic stance panel) and stance polarization figures in `R - Results/figures/T2/`.

---

### Process 3: Topic Relevance and Corporate Disclosure (`T3`)
- **Objective**: Measure corporate exposure to policy topics across 21,966 S&P 500 Form 10-K Business descriptions (1993–2025).
- **Methodology**:
  1. **Dual-Instrument Identification**:
     - *Instrument 1 (Deterministic Rail)*: Dense vector cosine similarity between 14.8 million segmented 10-K sentences and policy topic centroids (zero generation inference).
     - *Instrument 2 (Sentence-Block LLM Tagging)*: Classifies topic relevance, confidence, and directional orientation (Opportunity vs Threat) with cited textual evidence.
  2. **Econometric Panel Assembly**: Links corporate CIKs to Compustat financial variables (GVKEY), aligning fiscal year periods.
- **Quality Evaluation**: Evaluated against a hand-annotated gold-standard audit dataset (**93.4% precision**, **91.2% recall**, F1 = 0.923).
- **Key Output**: [`firm_topic_relevance_panel.parquet`](../data/cleaned/03_topic_relevance/firm_topic_relevance_panel.parquet) and industry exposure figures in `R - Results/figures/T3/`.

---

## 3. Master Output Artifacts Summary

| Process | Primary Output File | Storage Location | Description |
| :--- | :--- | :--- | :--- |
| **D1** | `packages_all.parquet`<br>`hearings_sst.parquet` | `data/raw/govinfo/`<br>`data/raw/02_hearings/` | Manifest enumeration contracts and 2,352 parsed hearing transcripts with metadata rosters. |
| **T1** | `hearing_summaries.parquet` | `data/cleaned/01_text_summarization/` | 2,352 entity-attributed hearing summaries generated via Qwen3.5-4B Map-Reduce. |
| **T2** | `frozen_codebook_111.parquet`<br>`member_stance_panel.parquet` | `data/cleaned/02_topic_extraction/` | Ratified 111-topic policy taxonomy and longitudinal congressional member-topic stance panel. |
| **T3** | `firm_topic_relevance_panel.parquet` | `data/cleaned/03_topic_relevance/` | S&P 500 corporate panel of firm-year policy exposure, relevance, and opportunity/threat scores. |
| **Results** | Categorized Figures | `R - Results/figures/` | Publication-ready evaluation plots, crosswalks, and pipeline architecture diagrams. |
