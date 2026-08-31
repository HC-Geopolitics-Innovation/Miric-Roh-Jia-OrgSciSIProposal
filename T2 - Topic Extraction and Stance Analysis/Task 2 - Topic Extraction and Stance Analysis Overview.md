# Task 2 (T2) — Topic Extraction and Stance Analysis: Pipeline & File Overview

This folder contains the complete workflow for member turn attribution, LLM prompt prototyping, constrained batch topic extraction, taxonomy alignment, codebook freezing, benchmark evaluation, and final panel construction.

---

## Task Stages & File Mapping

```
T2 - Topic Extraction and Stance Analysis/
├── Task 2 - Topic Extraction and Stance Analysis Overview.md
│
├── T2.01 - Pre-Processing - Member Turn Attribution.ipynb
│   └── Stage: Pre-Processing
│   └── Description: Links hearing transcript speaking turns to BioGuide congressional member IDs.
│
├── T2.02 - Model Prototyping - Promptbook & Few-Shot Design.ipynb
│   └── Stage: Model Testing & Prototyping
│   └── Description: Develops and tests prompt engineering strategies (few-shot, JSON schema constraints) for topic extraction.
│
├── T2.03 - Production Execution - Track 2 Batch Extraction.ipynb
│   └── Stage: Production Execution (Track 2)
│   └── Description: Runs unconstrained batch topic extraction over congressional member speaking turns.
│
├── T2.04 - Production Execution - Track 1 Constrained Extraction.ipynb
│   └── Stage: Production Execution (Track 1)
│   └── Description: Runs constrained topic extraction using JSON schema enforcement (via Jsonformer/vLLM).
│
├── T2.05 - Post-Processing - Stance Record Consolidation.ipynb
│   └── Stage: Post-Processing & Consolidation
│   └── Description: Assembles raw extraction output into clean member-topic-stance records.
│
├── T2.06 - Quality Assessment - Track 2 Production Check.ipynb
│   └── Stage: Quality Assessment
│   └── Description: Audits completion rates, error handling, and coverage for Track 2 extractions.
│
├── T2.07 - Taxonomy Alignment - Comparative Agenda Project Matching.ipynb
│   └── Stage: Taxonomy Alignment & Validation
│   └── Description: Maps extracted topics against standard Comparative Agendas Project (CAP) codebooks.
│
├── T2.08 - Taxonomy Alignment - LLM Consensus Clustering.ipynb
│   └── Stage: Taxonomy Alignment
│   └── Description: Clusters extracted topics into higher-level thematic taxonomies via LLM consensus.
│
├── T2.09 - Codebook Development - Topic Codebook Draft.ipynb
│   └── Stage: Codebook Development
│   └── Description: Drafts comprehensive policy topic codebooks from clustered extracted topics.
│
├── T2.10 - Codebook Development - Codebook Freeze & Mapping.ipynb
│   └── Stage: Codebook Development
│   └── Description: Freezes final topic definitions and assigns static topic IDs across the corpus.
│
├── T2.11 - Model Validation - CAP Codebook Benchmark Evaluation.ipynb
│   └── Stage: Model Validation & Benchmarking
│   └── Description: Benchmarks LLM topic extraction accuracy and alignment against human-coded CAP standards.
│
└── T2.12 - Empirical Analysis - Final Stance Panel Assembly.ipynb
    └── Stage: Empirical Panel Construction
    └── Description: Assembles final longitudinal firm-member stance dataset for econometric analysis.
```
