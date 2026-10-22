# Proposal For Organization Science

# Overcoming Data Bottlenecks and Enabling Research in New Domains by Leveraging AI-Enabled Research Pipelines

**Proposal for Special Issue:** AI-Enabled Frontiers in Organizational Science (*Organization Science*)

**CFP / URL:** [https://orgsci.org](https://orgsci.org/)

**Repository:** [https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis](https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis)

**Authors:** Jia, Miric, and Roh (in alphabetical order)

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?](#2-why-an-ai-enabled-data-pipeline-vs-allowing-an-llm-to-handle-the-entire-task)
- [3. Three Instances of Large Language Model-Enabled Research Pipelines Leveraging US Congressional Hearings as a Motivating Context](#3-three-instances-of-large-language-model-enabled-research-pipelines-leveraging-us-congressional-hearings-as-a-motivating-context)
    - [3.1. Long-Document Text Summarization](#31-long-document-text-summarization)
        - [3.1.1. Overview of Processing Pipeline](#311-overview-of-processing-pipeline)
        - [3.1.2. Application: Summarizing Long-Text Congressional Hearings](#312-application-summarizing-long-text-congressional-hearings)
        - [3.1.3. Research Outputs](#313-research-outputs)
    - [3.2. Extracting Topics, Positions, and Arguments from Long-Form Documents](#32-extracting-topics-positions-and-arguments-from-long-form-documents)
        - [3.2.1. Overview of Processing Pipeline](#321-overview-of-processing-pipeline)
        - [3.2.2. Application: Extracting Stances and Arguments around Focal Topics](#322-application-extracting-stances-and-arguments-around-focal-topics)
        - [3.2.3. Research Outputs](#323-research-outputs)
    - [3.3. Policy Relevance for Publicly Listed Firms](#33-policy-relevance-for-publicly-listed-firms)
        - [3.3.1. Overview of Processing Pipeline](#331-overview-of-processing-pipeline)
        - [3.3.2. Application: Linking Hearing Topics to S&P 500 10-K Disclosures](#332-application-linking-hearing-topics-to-sp-500-10-k-disclosures)
        - [3.3.3. Research Outputs](#333-research-outputs)
- [4. Demonstrating Empirical Research Questions Enabled by LLM-Created Variables](#4-demonstrating-empirical-research-questions-enabled-by-llm-created-variables)
- [5. Reproducing AI-Driven Pipelines for Alternative Research Questions](#5-reproducing-ai-driven-pipelines-for-alternative-research-questions)

---

## 1. Introduction

Textual data has provided a rich resource for researchers to answer a wide variety of questions that were otherwise difficult to measure. Prior to the advances enabled by rich textual data and modern text analysis methods (e.g., topic modeling, keyword extraction), researchers relied heavily on structured datasets such as the USPTO patent database, Compustat, or other traditional financial databases. However, the availability of large-scale textual data from corporate documents such as 10-K financial statements, patent abstracts or claims, and corporate websites (xxx; xxx) has opened new avenues for inquiry. This textual data has not replaced earlier structured datasets, but rather provided complementary inputs to augment existing empirical tools. Data availability is a primary catalyst of scholarly progress (xxx; xxx), and empirical approaches leveraging textual data—such as topic modeling, text embeddings to compute linguistic distance, and supervised text classification (xxx)—have expanded the frontier of researchable questions.

One critical limitation, however, is that while textual data is abundant, much of it faces a severe structural constraint: methods such as topic modeling or embedding construction typically require text documents of comparable length (ideally relatively short) with a high share of informative content (meaningful domain statements) relative to noise (boilerplate or generic language). This often-hidden constraint has impacted empirical research in two major ways. First, researchers frequently avoid settings where they cannot readily obtain clean, standardized, and concise textual data. Second, when applying existing tools to uncurated corpora, scholars often introduce substantial measurement error and noise into downstream analyses, because long textual documents tend to bury latent signals beneath a disproportionate volume of boilerplate.

Large language models (LLMs) have emerged as a powerful tool with the potential to transform organizational research and yield valuable new data inputs and methodologies. There has been a surge of recent attempts to leverage LLMs to automate and replicate core elements of the research workflow that are traditionally performed laboriously by human researchers. These include using LLMs for theorizing (xxx), testing assumptions (xxx), performing classification (xxx), and clustering data (xxx). However, uncritical adoption of these tools warrants caution: internal LLM processes are fundamentally opaque, and devolving full analytical discretion, decision-making, and measurement to a closed model introduces severe risks regarding validity and replicability. Responsible adoption requires methodological transparency, where researcher choices, prompt specifications, and intermediate outputs at each stage are systematically documented and verifiable.

In this proposal, we advocate that large language models should be deployed tactically as modular components of a transparent, auditable research pipeline—one that avoids ceding autonomous control to an LLM, and instead provides clear inspection points and empirical validation gates at every stage. We argue that LLMs serve as an indispensable enabling input when targeted specifically toward two domains where they excel:

1. **Synthesizing text** (generating readable, coherent, and condensed summaries grounded directly in source documents); and
2. **Generating code** (producing machine-readable, testable instructions that can be executed deterministically at scale).

By augmenting established text analysis methods—which possess known statistical properties, verifiable routines, and standard validation benchmarks—with LLMs across these two capabilities, scholars can overcome the skepticism and opacity surrounding generative AI in empirical science.

While these principles apply broadly across organizational research, we ground our framework in a particularly salient and challenging use case: analyzing public policy debates and connecting them to firm strategy. Long-form textual documents, such as US Congressional hearing transcripts and corporate 10-K filings, contain valuable evidence regarding the direction of government debate and legislation, as well as the strategic positioning of firms. However, both corpora are long and saturated with procedural boilerplate, obscuring the nuanced substantive positions within. Our proposal demonstrates how using LLMs as targeted components within an auditable data processing pipeline extracts reliable, structured data from long-form text, enabling empirical research designs that were previously intractable.

Specifically, we develop several LLM-enabled research pipelines that transform raw, unstructured text into research-ready datasets, and demonstrate how these pipelines contribute three core methodological and substantive elements:

1. **Generative AI-Enabled Pipelines for Information Extraction and Synthesis.** We demonstrate how long, information-rich, but noisy documents from the US Congressional Record—specifically, hearing transcripts—can be transformed into structured data inputs via modular LLM pipelines across three core extraction tasks:
    - a. ***Textual Summarization:*** Segmenting complex documents into semantic partitions, using LLMs to generate structured summaries for each partition, and synthesizing these summaries into concise document-level abstracts. This produces reliable, information-dense summaries for texts where no abstracts exist, substantially improving downstream tasks such as topic modeling, classification, and text embeddings.
    - b. ***Stance Extraction:*** Deploying LLMs to identify specific actor positions (e.g., members of Congress, corporate executives, agency officials) on focal policy topics, distilling the nuances of legislative debate into structured tabular data suitable for econometric analysis.
    - c. ***Debate Relevance to Corporate Disclosures:*** Combining fine-grained policy debate data with corporate 10-K business descriptions (Item 1) to establish the degree and direction of firm-level exposure to emerging regulatory developments.

2. **Demonstration of Empirical Research Questions Enabled by LLM-Created Variables.** Beyond developing methodological pipelines, we illustrate how the resulting measures enable empirical research that would otherwise be infeasible. We examine the escalating scrutiny of consumer data privacy within congressional hearings, applying our pipeline to identify which firms are directly exposed to privacy policy debates (treated) versus those that remain unexposed (control). This framework enables causal investigation of firm strategic and innovative responses following major policy shocks.

3. **Reproducing These AI-Driven Pipelines for Alternative Research Questions.** While our motivating application centers on regulatory policy and corporate disclosure, the underlying architecture is generalizable across textual corpora and research domains. To facilitate adaptation, we demonstrate an emerging paradigm of reproducibility: using autonomous AI Coding Agents. We provide fully documented repository assets and instructions allowing researchers to direct their own coding agents to parse our code, generate custom implementation plans, and execute these pipelines within their own empirical projects—establishing a transparent standard for computational reproducibility in organizational research.

The remainder of this proposal proceeds as follows. Section 2 outlines the methodological rationale for structured pipelines over unassisted end-to-end prompting. Section 3 details the three core data pipelines (summarization, stance extraction, and corporate relevance) within the context of US Congressional hearings. Section 4 demonstrates the empirical application to consumer data privacy and firm responses. Finally, Section 5 outlines the protocol for replicating and adapting these pipelines using AI coding agents.

---

## 2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?

A natural question is why researchers should engineer a multi-stage, modular pipeline rather than simply supplying raw documents to a commercial frontier LLM with a long context window and asking it to perform the entire analysis end-to-end.

We highlight two fundamental methodological reasons for designing an explicit, modular pipeline:

- **Transparency and Control:** Concerns regarding LLM reliability, model drift, and unobserved hallucinations become acute when an unconstrained model is granted full analytical autonomy. In contrast, our approach restricts LLMs to discrete, highly bounded tasks: parsing semantic units, executing targeted summarization prompts, or classifying specific sentences against predefined criteria. By isolating LLM operations within an auditable pipeline, researchers retain control over data transformations and can implement objective quality checks, preserving the statistical rigor expected in organizational scholarship.

- **Auditability and Systematic Replication:** Frontier model outputs are sensitive to variations in prompt wording, temperature parameters, and proprietary model updates. A modular architecture logs intermediate inputs and outputs at every step (e.g., raw partitions, intermediate chunk summaries, and extracted stance vectors). This granular audit trail allows scholars to inspect intermediate failure modes, validate intermediate outputs against ground-truth human annotations, and ensure computational replication across model generations.

---

## 3. Three Instances of Large Language Model-Enabled Research Pipelines Leveraging US Congressional Hearings as a Motivating Context

### 3.1. Long-Document Text Summarization

Many textual corpora contain vital empirical information embedded within extensive boilerplate. LLMs can distill these long texts into concise, information-dense representations suitable for downstream analysis. Although contemporary frontier models feature large context windows, processing an entire multi-hundred-page transcript in a single prompt remains opaque, risks omitting critical details in the middle of long contexts, and produces inconsistent outputs across large corpora. A structured map-reduce architecture ensures systematic and reproducible extraction.

#### 3.1.1. Overview of Processing Pipeline

The summarization pipeline consists of three sequential stages:

a. **Document Structure and Semantic Partitioning.** Long documents are parsed into meaningful semantic units rather than arbitrary token blocks. Using *context-aware chunking*, transcripts are split along natural institutional boundaries, such as individual witness opening statements, committee member remarks, and dedicated question-and-answer exchanges.

b. **Partition Summarization and Hierarchical Synthesis (Map-Reduce).** Each partition is passed to an LLM with standardized prompt instructions detailing the required summary schema and extraction targets. These partition summaries are subsequently combined through a structured "reduce" stage, synthesizing individual testimony summaries into a coherent, high-level hearing summary without exceeding context constraints or losing local nuance.

c. **Model Selection, Validation, and Deployment.** Prompt templates, partitioning chunk sizes, and combination strategies are iteratively refined. Intermediate outputs are evaluated against human-curated benchmarks (e.g., official committee press summaries and CRS reports) where available. Once validated, the pipeline is executed deterministically across the full corpus.

#### 3.1.2. Application: Summarizing Long-Text Congressional Hearings

We apply this pipeline to a comprehensive corpus of US Congressional hearing transcripts spanning from 1995 to 2022. Hearings routinely exceed 100 pages, involving dozens of witnesses and legislators. We segment each hearing by witness testimony and Q&A block, generate granular partition summaries, and synthesize them into comprehensive hearing-level abstracts. Validation against official committee summaries confirms high factual recall and thematic consistency.

#### 3.1.3. Research Outputs

This pipeline generates three durable research assets:
1. **Partitioned Textual Documents:** Cleaned, structured JSON/tabular transcript segments partitioned along institutional boundaries.
2. **Granular Partition Summaries:** Verified summaries for each testimony and exchange.
3. **Committee Hearing Abstracts:** Unified, high-level summaries capturing overall hearing themes, legislative intent, and policy conclusions.

---

### 3.2. Extracting Topics, Positions, and Arguments from Long-Form Documents

Beyond general summarization, researchers often require granular extraction of substantive positions and arguments concerning specific policy topics.

#### 3.2.1. Overview of Processing Pipeline

a. **Topic Identification from Summaries.** Leveraging the concise, information-rich summaries produced in Section 3.1, researchers can employ standard topic models or zero-shot LLM categorization to identify recurring policy topics across the corpus.

b. **Topic-Relevance Filtering.** Because full hearing transcripts contain extensive peripheral discussion, an LLM screening step evaluates partition chunks against target topic definitions, filtering out irrelevant dialogue and isolating topical discussions.

c. **Stance and Argument Extraction.** For all relevant chunks, an LLM extracts specific arguments, policy rationales, and the explicit stances (e.g., support, opposition, concern) taken by each identified speaker.

d. **Aggregation and Stance Indexing.** Extracted arguments are aggregated either quantitatively (by calculating actor stance frequencies and directional sentiment shares) or qualitatively (by synthesizing the dominant threats and opportunities identified by participants).

e. **Validation.** Extracted topic labels and stances are validated through cross-coder reliability checks against human-annotated sample hearings and external policy issue classifications.

#### 3.2.2. Application: Extracting Stances and Arguments around Focal Topics

Applying this methodology to hearings addressing consumer privacy and cybersecurity, the pipeline identifies specific risk frames (e.g., unauthorized data monetization, algorithmic bias, foreign surveillance) and opportunity frames (e.g., AI innovation, digital trade competitiveness). Aggregating these extractions by committee and year reveals temporal shifts in legislative scrutiny and bipartisanship.

#### 3.2.3. Research Outputs

1. **Standardized Hearing Topic Taxonomy:** A verified codebook of 111 policy topics mapped across congressional sessions.
2. **Actor-Attributed Argument Database:** A tabular dataset of extracted statements recording the topic, speaker, institutional affiliation, and policy argument.
3. **Annual and Committee Stance Indices:** Quantitative metrics capturing the intensity of perceived threats versus opportunities for each policy topic over time.

---

### 3.3. Policy Relevance for Publicly Listed Firms

Connecting macro-policy debates to firm behavior requires measuring the semantic relatedness between congressional discussions and corporate disclosures.

#### 3.3.1. Overview of Processing Pipeline

We calculate firm-level exposure to policy topics through two complementary approaches:
- **Similarity-Based Exposure:** Measuring the semantic closeness between a firm's Form 10-K business description (Item 1) and topic reference vectors built from topic definitions and evidence sentences.
- **LLM-Based Directional Exposure:** Prompting an LLM to read 10-K passages and tag whether the firm explicitly describes operations or technologies intersecting the policy topic, classifying whether the firm frames the issue as an operational threat, strategic opportunity, or neutral factor.
- **Integrated Exposure Index:** Weighting directional LLM tags by sentence-level cosine similarity to produce continuous, directional exposure scores.

#### 3.3.2. Application: Linking Hearing Topics to S&P 500 10-K Disclosures

We map the 111 congressional hearing topics into the annual 10-K filings of S&P 500 firms over a multi-decade panel. For consumer data privacy, this approach isolates firms with direct operational exposure (e.g., advertising platforms, financial processors, healthcare informatics) from unexposed firms within the same broad industry classifications.

#### 3.3.3. Research Outputs

1. **Firm–Topic Exposure Panel:** An annual panel dataset containing continuous similarity scores, discrete sentence tags, and directional exposure measures for each firm-topic pair.
2. **Sentence-Level Exposure Concordance:** An auditable database linking individual 10-K disclosure sentences to specific policy topics with assigned threat/opportunity indicators.

---

## 4. Demonstrating Empirical Research Questions Enabled by LLM-Created Variables

To demonstrate the empirical utility of these pipelines, we construct a quasi-experimental study examining firm strategic responses to the emergence of federal consumer privacy scrutiny. Leveraging our topic relevance indices, we identify firms with significant operational exposure to consumer privacy legislation (treated) alongside unaffected firms operating within comparable economic sectors (control). By linking these exposure metrics to firm-level patenting filings, R&D investments, and lobbying expenditures, we illustrate how researchers can test substantive theories regarding non-market strategy, compliance costs, and technological redirection following regulatory debate.

---

## 5. Reproducing AI-Driven Pipelines for Alternative Research Questions

To ensure our contribution extends beyond the immediate empirical setting, we provide a complete, open-source computational infrastructure designed for adaptation by other scholars.

Rather than expecting researchers to manually re-engineer code or execute scripts in isolation, we demonstrate how researchers can deploy autonomous **AI Coding Agents** to adapt our methodology:
- **Open Codebook and Modular Prompts:** All prompt templates, schema definitions, and chunking parameters are documented in our public repository.
- **Agentic Implementation Protocol:** We provide structured workflow instructions that allow a researcher to task an AI coding agent with ingesting our repository, tailoring the prompts and chunking logic to an alternative textual corpus (e.g., regulatory rulemaking, CEO earnings calls, patent re-examinations), and producing an executable execution plan for the researcher to review.
- **Verification Benchmarks:** Reusable evaluation scripts allow researchers to inspect intermediate failure rates and validate accuracy before full deployment.

By coupling modular LLM pipelines with agentic reproducibility, this project provides a robust, extensible foundation for text-as-data methodology in organizational science.