# Task 3 (T3) — Topic Relevance and Corporate Disclosure: Pipeline & File Overview

This folder contains the complete workflow for segmenting corporate 10-K disclosures, scoring embedding topic centroids, prototyping LLM relevance tagging prompts, auditing gold-standard samples, batch tagging production execution, and constructing empirical relevance panels.

---

## Task Stages & File Mapping

```
T3 - Topic Relevance and Corporate Disclosure/
├── Task 3 - Topic Relevance Overview.md
│
├── T3.1 - Pre-Processing - 10-K Item 1 Sentence Segmentation.ipynb
│   └── Stage: Pre-Processing
│   └── Description: Cleans and segmentates 10-K Item 1 text into sentences and paragraph blocks.
│
├── T3.2 - Model Prototyping - Embedding Centroid Scoring.ipynb
│   └── Stage: Model Testing & Prototyping
│   └── Description: Computes sentence embedding distance scores against policy topic centroids.
│
├── T3.3 - Production Execution - Text Block Partitioning.ipynb
│   └── Stage: Pre-Processing & Execution Setup
│   └── Description: Partitions 10-K text disclosures into optimal blocks for LLM tagging tasks.
│
├── T3.4 - Model Prototyping - LLM Tagging Promptbook & Few-Shot.ipynb
│   └── Stage: Model Testing & Prototyping
│   └── Description: Designs and tests prompt structures and few-shot examples for topic relevance tagging.
│
├── T3.5 - Model Validation - Gold Standard Gate Audit.ipynb
│   └── Stage: Model Validation & Audit
│   └── Description: Audits LLM relevance tagging predictions against hand-annotated gold-standard ground truth.
│
├── T3.6 - Production Execution - Batch Tagging Pipeline.ipynb
│   └── Stage: Production Execution
│   └── Description: Runs batch LLM inference to tag topic relevance across firm disclosures.
│
└── T3.7 - Empirical Analysis - Topic Relevance Descriptives & Panel.ipynb
    └── Stage: Empirical Panel Construction & Analysis
    └── Description: Assembles final firm-year topic relevance panel and computes descriptive statistics.
```
