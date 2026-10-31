# Data Bottlenecks and Enabling Research in New Domains by Engineering AI-Enabled Research Pipelines

**Proposal for Special Issue:** AI-Enabled Frontiers in Organizational Science (*Organization Science*)  
**CFP / URL:** https://orgsci.org  
**Repository:** https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis  
**Authors:** Jia, Miric, and Roh (in alphabetical order)  

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?](#2-why-an-ai-enabled-data-pipeline-vs-allowing-an-llm-to-handle-the-entire-task)
- [3. Step #1: Long-Document Text Summarization](#3-step-1-long-document-text-summarization)
  - [3.1. How Text Summarization Works: Data Preparation and Key Inputs](#31-how-text-summarization-works-data-preparation-and-key-inputs)
  - [3.2. Application: Congressional Hearing Transcripts](#32-application-congressional-hearing-transcripts)
  - [3.3. Research Outputs](#33-research-outputs)
- [4. Step #2: Extracting Relevant Information from Textual Documents](#4-step-2-extracting-relevant-information-from-textual-documents)
  - [4.1. Application: Topic Extraction and Stance Analysis in Congressional Hearings](#41-application-topic-extraction-and-stance-analysis-in-congressional-hearings)
- [5. Step #3: Identifying Topic Relevance and Corporate Disclosure](#5-step-3-identifying-topic-relevance-and-corporate-disclosure)
- [6. Research Outputs, Reproducibility, and Application to Future Research](#6-research-outputs-reproducibility-and-application-to-future-research)

---

## 1. Introduction

Textual data has provided a rich resource for researchers to answer a wide variety of questions that were otherwise difficult to measure. Prior to advances in textual analysis, researchers relied heavily on structured datasets such as the USPTO patent database, Compustat, or other structured financial datasets. However, the availability of large-scale textual data from documents such as 10-K financial statements, patent abstracts, or corporate websites (xxx; xxx) has opened new avenues for research. Data availability is an important enabler of research advancement (xxx; xxx), and empirical approaches that utilize textual data—such as topic modeling, text embeddings to compute textual distance, or text classification (xxx)—have enabled the investigation of new questions. 

One critical limitation, however, is that while textual data is abundant, much of it faces an important constraint: approaches such as topic modeling or embedding construction typically require text documents of comparable length (ideally relatively short) with a high share of informative content (meaningful statements) relative to noise (boilerplate or generic statements). This constraint limits researchers' ability to leverage many rich data sources and introduces noise into downstream empirical measures.

Large language models (LLMs) have emerged as extremely powerful tools capable of performing many tasks previously handled by earlier computational models. There are continuous attempts to use them for theorizing (xxx), testing assumptions (xxx), performing classification (xxx), and clustering data (xxx). Yet, while we have established research practices and validation standards for traditional methodologies, LLMs often operate as opaque black boxes that, while capable of producing useful outputs, can obscure how specific decisions are made. Fundamentally, these models possess two core strengths: 
1. **Synthesizing text** (generating readable, coherent text based on existing documents); and 
2. **Generating code** (producing machine-readable instructions that can be systematically executed and tested).

Rather than abandoning research practices for which we have established routines, validation standards, and verifiable properties in the hope that LLMs will outperform them end-to-end, we propose a methodology that combines the complementary strengths of existing research practices (interpretability, confidence in understanding their underlying properties, and grounding in established corpuses of knowledge) with the strengths of Large Language Models (distilling information and generating structured textual documents). 

The proposed project contains three core steps:

1. **Generative AI as a Tool for Information Extraction and Synthesis.** Many existing text analysis methodologies (e.g., topic modeling, text classification, semantic distance) break down when applied to raw documents that are long (or of differing lengths), contextually idiosyncratic, or dilute in signal. Examples include congressional testimony, earnings call transcripts, or corporate websites. In these settings, key information is embedded within generic, formulaic text. Traditional approaches have attempted to address this issue by upweighting informative words and downweighting generic words (e.g., TF-IDF weighting), but these methods do not fully resolve the underlying signal-to-noise problem. Similarly, text embeddings provide a representation of semantic similarity across words, overcoming limitations of word co-occurrence, but cannot readily distinguish informative content from formulaic boilerplate. This noise propagates into downstream measures such as topic models, language distance, or classifiers, obfuscating meaningful variation. We propose that using LLMs to take long, convoluted documents (e.g., 10-Ks, corporate websites, or congressional testimony) and convert them into concise, information-rich text summaries (analogous to patent abstracts) can substantially improve the performance of subsequent text analysis methods and enable structured information extraction.

2. **Demonstration of Information-Rich Textual Summaries on Substantive Research Questions.** Next, we demonstrate how using LLM-generated, information-rich summaries allows us to identify relationships in textual data that were previously difficult to capture. We demonstrate this in the context of studying the impact of privacy regulation on innovation. A fundamental policy issue for technology regulators, firm non-market strategy, and intellectual property scholars is the relationship between government regulation and innovation outcomes. An example is consumer privacy regulation, where policymakers increasingly scrutinize consumer data protection, but linking these debates to corporate innovation has remained challenging. Prior work has examined specific contexts such as mobile app markets following GDPR where direct impacts could be measured; however, scalable empirical methods to identify which firms across the broader economy are affected by evolving policy debates remain scarce. Using our proposed methodology, we establish an empirical relationship between these policy debates and the specific firms influenced by them, allowing us to investigate how firms adjust their innovation strategies in response.

3. **Reproducible AI-Driven Pipelines for Empirical Research.** The proposed methodology provides a systematic way to leverage the primary strength of LLMs—generating concise textual summaries from larger documents—to enhance empirical research methods. To make this methodology accessible, we intend to release both the summarized datasets and the complete processing pipeline to support future research projects. Historically, sharing empirical methodologies required scholars to use existing static code as a starting point or adopt a specialized software package. However, LLMs excel at reading, writing, and understanding code. Going forward, empirical researchers will increasingly use these tools to implement new methods and verify their code (and it will be standard practice for empirical work to utilize computational tools to validate code and methodology). Therefore, in addition to making code and data available, we provide an AI-agent-driven framework for researchers to implement these approaches within their own research projects. This project uses Generative AI to overcome a primary bottleneck in empirical research (extracting reliable textual signal) as well as a secondary bottleneck (the cost and learning curve of adopting advanced computational methods) by documenting a reproducible, AI-driven data pipeline.

---

## 2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?

One question that inevitably emerges is why researchers should develop a structured, LLM-enabled pipeline rather than simply prompting a commercial LLM to process entire context windows and execute the entire task end-to-end. Furthermore, while existing models encounter limitations, future frontier models will continue to advance.

There are two critical reasons for designing an explicit data pipeline:

* **Transparency and Control:** Concerns regarding LLM model transparency, reliability, and stability typically arise when researchers cede full autonomy to a model and ask it to arrive at an unassisted solution. By contrast, our approach uses the LLM in targeted roles: to write code, execute specific processing steps, or summarize discrete textual segments based on defined source documents. By developing an AI-enabled data pipeline, we overcome specific bottlenecks in existing research workflows rather than re-engineering parts of the research process where unconstrained LLM execution lacks control and statistical guarantees.

* **Auditability and Systematic Replication:** While LLMs can formulate reasoning internally, their outputs often depend heavily on subtle nuances in prompt formulation, model versioning, and temperature settings. By carefully engineering a structured research pipeline, researchers can leverage LLMs at discrete intermediate steps while fully documenting every phase of the process at scale. This modular approach provides a degree of oversight, reproducibility, and methodological transparency that would otherwise be impossible.

---

## 3. Step #1: Long-Document Text Summarization

Text summarization involves taking long, noisy, and complex textual data and using a large language model to create a concise, information-rich summary that can be utilized in subsequent research tasks. 

While off-the-shelf models can easily generate summaries of uploaded documents, systematically and reliably summarizing large corpora into consistent, representative summaries requires carefully engineering the summarization pipeline to overcome two technical challenges:

1. **Context Limits and Computational Efficiency:** Although modern models feature expanding context windows, these limits are still encountered with lengthy documents (which are precisely those requiring summarization), particularly when deploying economical, open-weight, or local models. To address this, the researcher must either implement a procedure for carefully partitioning and sequencing data through the model, or rely on opaque, automated chunking.
2. **Heterogeneous Topical Sections:** Within long textual documents, different sections address distinct topics. In order for the summarization procedure to be reliable, these textual components must be partitioned such that the input provided to the LLM is as coherent as possible. Even when a full document fits within a model's context window, pre-cleaning and structured partitioning yield significant improvements in summary fidelity and clarity.

Carefully designing and partitioning this process ensures that data extraction remains reliable, transparent, and reproducible regardless of underlying model advances.

### 3.1. How Text Summarization Works: Data Preparation and Key Inputs

The summarization of text by an LLM depends heavily on how the text is preprocessed and structured as input, particularly for long documents. Therefore, the core objective of text summarization is to create a data processing pipeline that takes raw documents, generates cleaned text inputs, systematically combines them, and produces clear, summary outputs.

The LLM-enabled data pipeline proceeds as follows:

* **Document Structure and Semantic Partitioning:** Researchers must first analyze the dataset structure to determine how documents should be split into smaller chunks for individual processing. For example, financial 10-K filings require firms to describe business operations, macroeconomic risks, and governance structures—often in separate sections. Because these sections serve distinct functions, they benefit from being processed individually. Even for models with large context windows, processing text in smaller, topically coherent chunks improves reliability and cost efficiency.
* **Map-Reduce Aggregation:** Researchers design a processing pipeline to create and aggregate individual summaries systematically. A standard approach is a Map-Reduce framework: individual text chunks are first summarized (Map), and these segment-level summaries are subsequently aggregated into a comprehensive document summary (Reduce).
* **Model Selection and Validation:** Outcomes depend on the choice of model, prompt design, and aggregation rules. Researchers must evaluate alternative models, preprocessing heuristics, and aggregation techniques during an initial prototyping and validation stage to ensure the pipeline yields consistent, high-fidelity results.
* **Corpus Deployment and Artifact Storage:** The finalized model pipeline is deployed across the entire dataset. Data from each intermediate stage—cleaned source segments, intermediate chunk summaries, and aggregated outputs—are documented and archived. This ensures full traceability, allowing researchers to inspect intermediate components or re-run specific transformations with alternative models.

### 3.2. Application: Congressional Hearing Transcripts

Congressional hearings provide an ideal application for text summarization. These transcripts document extensive deliberations among policymakers and invited witnesses (including scientists, corporate executives, and industry stakeholders).

These transcripts capture critical policy deliberations utilized across various research settings (xxx; xxx; xxx). However, they are typically long and saturated with procedural preamble and formulaic pleasantries that dilute the substantive debate. Extracting the core arguments into a usable dataset for variable construction requires a structured pipeline:

* **Preprocessing and Speaker-Turn Parsing:** Congressional hearings follow a structured format: an opening preamble outlining committee business, followed by allocated speaking turns for members and witnesses. While individual statements are manageable, full hearings span hundreds of pages. Furthermore, arbitrary text splitting risks cutting off active exchanges between speakers. The initial step is therefore to parse the raw transcript into discrete speaking turns and Q&A exchanges. For complete transparency, these partitioned sub-documents are preserved alongside the original source transcripts.
* **Hierarchical Summarization:** The model processes each isolated speaking session or dialogue block to construct a concise summary. Individual speech summaries can then be grouped chronologically or by witness exchange (e.g., back-and-forth dialogue between a committee member and a witness) and passed to the model for consolidated synthesis.
* **Validating the Summaries:** While intermediate steps are fully documented and reproducible, external validation ensures that the summaries accurately capture ground-truth information. In congressional hearings, human annotators write coarse official summaries that are published with the public record. We validate our LLM-generated summaries by computing cosine similarity against these human-coded summaries. To benchmark this measure, we compare within-hearing similarity against baseline similarity across hearings within the same committee (related topics) and across different committees (unrelated topics), verifying that our summaries capture specific hearing content rather than generic political discourse.

### 3.3. Research Outputs

The output of this process is a structured set of empirical assets: (1) cleaned and parsed text segments, (2) individual chunk-level summaries, and (3) final document-level summaries. This layered architecture ensures complete traceability and allows researchers to reproduce or extend any phase of the pipeline.

---

## 4. Step #2: Extracting Relevant Information from Textual Documents

The rapid growth of textual data provides substantial opportunities for computational text analysis in organizational research (xxx; xxx). These methods rely on clean, standardized textual data. The summarization procedures outlined in Step #1 standardize raw text to facilitate subsequent information extraction.

In addition to document-level summaries, LLMs can be utilized to extract specific thematic information from text documents. This shares conceptual similarities with unsupervised machine learning approaches where topics emerge from the data. However, traditional unsupervised methods often struggle when documents are lengthy, convoluted, and characterized by a low signal-to-noise ratio.

Because LLMs can ingest structured chunks and extract salient concepts, they can reliably identify key topics and terminology associated with specific substantive issues. The workflow operates as follows:

* **Data Preparation:** Text data is preprocessed and partitioned into coherent thematic chunks.
* **Topic Identification:** The model is prompted to extract the core topic or focus of a given text segment. Unlike traditional topic modeling (e.g., LDA), which relies solely on term co-occurrence frequencies across a bag-of-words representation, the LLM identifies semantic topics while filtering out boilerplate and procedural text.
* **Stance and Sentiment Classification:** Once topics are identified, the LLM is prompted to classify the speaker's stance toward that focal topic (e.g., whether an issue is framed as a strategic opportunity or an operational threat).
* **Validation:** Extracted topics and stances are validated against established benchmarks and domain-specific human-coded datasets.

### 4.1. Application: Topic Extraction and Stance Analysis in Congressional Hearings

We apply this methodology to congressional hearings on technology regulation, social media, and cybersecurity.

In this setting, the empirical task is twofold:
1. **Topic Identification:** Identify the specific issues being debated (e.g., consumer data privacy, algorithmic harm to children, platform liability, national security threats).
2. **Stance Identification:** Determine the stance expressed regarding each issue—for instance, whether regulatory compliance is framed as a competitive threat to business models or an opportunity for differentiation and consumer trust.

The extraction pipeline proceeds in four steps:

1. **Preprocessing:** Transcripts are parsed to isolate core dialogue between committee members and witnesses, removing procedural administrative business.
2. **Topic Extraction:** Text segments are passed to the model to extract the primary topic of discussion within each exchange, avoiding overly large context windows to maintain model focus.
3. **Stance Classification:** The model evaluates the identified topics within each exchange to categorize the speaker's stance (e.g., opportunity vs. threat; supportive vs. critical).
4. **Aggregation and Validation:** Extracted topics are aggregated and validated against benchmark human-coded data sources, such as the Comparative Agendas Project (CAP).

---

## 5. Step #3: Identifying Topic Relevance and Corporate Disclosure

A fundamental breakthrough of modern semantic models—such as embedding models and bidirectional encoders (e.g., BERT)—is their ability to capture semantic proximity in a continuous vector space. Concepts with related meanings are located close to one another, enabling researchers to measure semantic similarity across documents. This capability underpins recent applications of LLMs for identifying keywords, topics, and conceptual similarity in organizational research (Raj & Seamans, xxx; Rock, Mishkin, & Manning, xxx).

We propose extending these tools to measure proximity and relevance across distinct domains where raw-text similarity metrics often fail. For example, expert human coders can readily determine whether a pending policy debate is relevant to a specific firm or industry, but manually coding this across thousands of firms and legislative sessions is cost-prohibitive.

By combining topic extraction with corporate disclosures, we use LLMs to assess whether policy topics discussed in congressional committee hearings (from Step #2) are relevant to specific firms based on their 10-K disclosures. Once topic relevance is established, the pipeline classifies whether the firm frames the policy development as a strategic opportunity, a regulatory threat, or a neutral operational factor.

---

## 6. Research Outputs, Reproducibility, and Application to Future Research

The proposed research project will generate several core contributions and empirical outputs:

* **A Modular, Controlled AI Research Methodology:** The paper provides a formal methodology for integrating LLMs and generative AI into empirical research workflows without relinquishing researcher control. Instead of treating models as opaque end-to-end deciders, researchers design and engineer modular pipelines that optimize specific analytical steps for their distinct research objectives while ensuring transparent documentation and auditability of all key modeling choices. The LLM is deployed strategically at targeted bottlenecks where it delivers clear comparative advantages over traditional methods.

* **Novel Empirical Datasets on Congressional Deliberations and Corporate Exposure:** Applying this methodology to the complex textual corpus of congressional hearings yields several research datasets for organizational and policy scholars:
  1. **Entity-Attributed Summaries of Congressional Hearings:** A comprehensive database of concise, validated hearing summaries ($N = \text{XX}$ hearings).
  2. **Granular Topic and Stance Panel:** A structured database capturing the primary policy topics discussed in each hearing ($N = \text{XX}$ hearings; $N \text{ to } M$ topics per hearing), along with directional speaker stances identifying whether deliberations reflect support, concern, or neutrality toward each focal issue.
  3. **Firm-Level Policy Exposure and Framing Panels:** A longitudinal dataset linking hearing policy topics to publicly traded firms ($N = \text{XX}$ topics across $N = \text{XX}$ public firms), capturing both topic relevance and corporate sentiment (classifying whether firm disclosures frame the policy development as a strategic opportunity or a regulatory threat).
  
  In addition, by releasing all intermediate assets (cleaned speaker-turn transcripts, intermediate chunk-level summaries, and raw classification logs), we enable scholars to re-aggregate, validate, or adapt these datasets for distinct empirical inquiries.

* **A Reusable Template and Agent-Driven Framework for Custom Applications:** We provide a structured template and operational guidelines enabling researchers to adapt, extend, or customize these pipelines for their own projects. With recent advances in AI systems capable of interpreting, executing, and validating code, releasing an open, well-structured computational repository offers unprecedented utility. We will host all pipeline code in an open-access repository and demonstrate how scholars can deploy AI agents to inspect, replicate, and adapt our workflows.

  This approach fundamentally transforms traditional replication. Rather than manually parsing static scripts, researchers can task their own AI coding agents with analyzing our open-source codebase to understand its architecture, dependency graphs, and modular components. Grounded in this transparent codebase, agents can readily adapt the pipeline to new text corpora, adjusting prompts, chunking strategies, and classification schemas while automatically documenting their modeling decisions. By lowering technical barriers and establishing high standards for computational transparency, we hope this framework helps establish best practices for reproducible, AI-assisted empirical research in organization science.
