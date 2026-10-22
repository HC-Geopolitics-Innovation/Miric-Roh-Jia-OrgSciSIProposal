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
- [3. Step #1: Long-Document Text Summarization](#3-step-1-long-document-text-summarization)
    - [3.1. How Text Summarization Works: Data Preparation and Key Inputs](#31-how-text-summarization-works-data-preparation-and-key-inputs)
    - [3.2. Application: Congressional Hearing Transcripts](#32-application-congressional-hearing-transcripts)
    - [3.3. Research Outputs](#33-research-outputs)
- [4. Step #2: Extracting Relevant Information from Textual Documents](#4-step-2-extracting-relevant-information-from-textual-documents)
    - [4.1. How Topic Extraction Works: Topic and Stance Identification](#41-how-topic-extraction-works-topic-and-stance-identification)
    - [4.2. Application: Topic Extraction and Stance Analysis in Congressional Hearings](#42-application-topic-extraction-and-stance-analysis-in-congressional-hearings)
    - [4.3. Research Outputs](#43-research-outputs)
- [5. Step #3: Identifying Topic Relevance and Corporate Disclosure](#5-step-3-identifying-topic-relevance-and-corporate-disclosure)
    - [5.1. How Topic Relevance Works: Similarity and Sentence-Level Assessment](#51-how-topic-relevance-works-similarity-and-sentence-level-assessment)
    - [5.2. Application: Hearing Topics and S&P 500 10-K Item 1 Disclosures](#52-application-hearing-topics-and-sp-500-10-k-item-1-disclosures)
    - [5.3. Research Outputs](#53-research-outputs)
- [6. Research Outputs, Reproducibility, and Application to Future Research](#6-research-outputs-reproducibility-and-application-to-future-research)

- [Appendix A. Prompts](#appendix-a-prompts)
- [Appendix B. Primary-Topic Tie Breaking](#appendix-b-primary-topic-tie-breaking)

---

## 1. Introduction

Textual data has provided a rich resource for researchers to answer a wide variety of questions that were otherwise difficult to measure. Prior to the advances that have been enabled through rich textual data and text analysis methods (e.g. topic modeling, keyword extraction), researchers relied heavily on structured datasets such as the USPTO patent database, Compustat, or other structured financial datasets. However, the availability of large-scale textual data from documents such as 10-K financial statements, patent abstracts or claims, or corporate websites (xxx; xxx) has opened new avenues for research. This has not replaced the earlier structured datasets, but provided new inputs which could augment these tools. Data availability is an important enabler of research advancement (xxx; xxx), and empirical approaches that utilize textual data—such as topic modeling, text embeddings to compute textual distance, or text classification (xxx)—have enabled the investigation of new questions.

One critical limitation, however, is that while textual data is abundant, much of it faces an important constraint: approaches such as topic modeling or embedding construction typically require text documents of comparable length (ideally relatively short) with a high share of informative content (meaningful statements) relative to noise (boilerplate or generic statements). This often hidden constraint has impacted research in two ways. First, researchers are avoiding contexts where they cannot have clean standardized textual data. Second, when they are using these tools they may be often introducing considerable noise into the process, as the long textual documents may have an overemphasis of noise relative to the signal latent in the data. 

Large language models (LLMs) have emerged as a piowerful research tool that has the potential to transform research and provide valuable new inputs and methodologies. There has been a surge of attempts to use these large language models to funamentally automate and replicate part5s of the research process, which are laboriously being performed researchers. These include attemnpts to use LLMs for theorizing (xxx), testing assumptions (xxx), performing classification (xxx), and clustering data (xxx).  However, any attempts to use such tools should be met with caution, as their internal processes are fundametnally opaque and devolving control, decision making and outputs to such a model should be met with skepticism, or at least require trasparecny by documenting choices and outputs in each step of the process such that they could be replicated. 

In the proposed research project, we are are advocating that large language models should be used tactically as part of a transparent and clear research pipeline which does not devolve frull control to a large langauge model, and when it does, does so in a way that allows for instpection of inputs and outputs as well as clear potential validation points. We argue that LLMs can be a critical enabling input for research, but that they should be part of a documented research pipeline, that leverages two domains where LLMs are particularly good. 

1. **Synthesizing text** (generating readable, coherent text based on existing documents); and
2. **Generating code** (producing machine-readable instructions that can be systematically executed and tested).

We argue that established text analysis methods, for which we have established routines, validation standards, and verifiable properties can be augemented by these large language mdoels using these two critical features of this technology. We believe that this is a much more sound, verifiable and transperent approach to using these tools, and can overcome the hesitation and skepticisim around using this technology for research. 

While we believe these arguments can apply broadly to a wide range of research applications, we have identified a particularly salient use case for organizatioanl researchers that can be leveraged and applied. 

Long textual documents such as congressional testimony of firm 10K statements are valuable artefacts about the direction of government debate and legislation, as well as information about the strategies and busienss areas of firms themselves. However, they suffer from the constraint that they are long and contain a lot of generic boilerplate language that obscures the latent nuance (the signal) within the long and formulatic text (noise). Our proposal demonstrates how the use of large language models, as a critical but narrow part of a data processing pipeline can create reliable and useful textual data, which can enable further research that was previoulsy not possible (or which in previous cases relied on measurement in the coarsest possible forms).

Using these long textual documents, we develop several LLM enabled research pipelines which allow us to generate new data and isnights, whcih translate int ofutrue research. We then demosntrate how this can be used to answer informative research questions and how this can be replciated or adapted by other scholars. In summary, within the proposed project we contribute the following elements. 


1. **Generative AI enabled Pipelines for Information Extraction and Synthesis.**

We show how an example of long information rich, but noisy textual documents from the US Congressional record—specifically, hearing transcripts can be transformed into actionable data inputs through the use of LLM enabled reacsearch pipelines. We develop and demonstrate LLM enabled data pipelines for three types of information extraction tasks, that can enable different subsequent research outputs. 

- Texual Summarization. Taking large, complex textual documents, splitting them into chunks, using LLMs to generate texutl summaries of chunks, and then synthesizing these summaries into final, actionable inputs. This provides the equivlient of reliable, structured "abstract" for documents where such summaries do not exist. This subsequently enables tasks such as text classification, topic modeling or language distance from embeddings in more reibale ways. 

- Stance Extraction. Using LLMs to identify the positions of different actors (e.g. Congress members, firms, government agencies) on specific topics, allowing researchers to distill the nuances of an academic debate and identify the positions that each individulal takes on an issue, formulating a rich description of the debate, with data in a tabular format that can be utilized in subsequent resarch. 

- Debate Relevance to Firm Business Area. Usiing fine grained information on the topical debate as well as on the understanding of the busienss of firms based on their 10K statements, we develop an LLM enabled pipeline to establish the extent to which firms have the potential to be impacted by the policy debates. 

These data pipelines are the foundation of our proposal, and the contribution that enales further research. However, we also demonstrate the impact of this with two additional elements. 

2. **Demonstraton of Empirical Research Question Enabled by LLM Created Varaibles** 

While the ability to identify and understand these LLM enabled pipelines is critical for researchers, we further illustratye how the variables that result from this exercise can allow us to construct an empirical research paper that would otherwise not be possible for us to investigate. We document the increasing scrutiny of privacy regulation within US congressional debates and document the construction of outcomes within this 




Demonstration of Information-Rich Textual Summaries on Substantive Research Questions.** Next, we demonstrate how using LLM-generated, information-rich summaries allows us to identify relationships in textual data that were previously difficult to capture. We use consumer data privacy as a running application for linking policy discussions to firms’ disclosed activities. A fundamental policy issue for technology regulators, firm non-market strategy, and intellectual property scholars is the relationship between government regulation and innovation outcomes. An example is consumer privacy regulation, where policymakers increasingly scrutinize consumer data protection, but linking these debates to corporate innovation has remained challenging. Prior work has examined specific contexts such as mobile app markets following GDPR where direct impacts could be measured; however, scalable empirical methods to identify which firms across the broader economy are affected by evolving policy debates remain scarce. The present application constructs topic-based links and disclosure measures. Studying whether firms adjust their innovation strategies in response would require additional outcome data and a research design identifying those responses.

3. **Reproducible AI-Driven Pipelines for Empirical Research.** We document the code, prompts, source evidence, and intermediate outputs needed to inspect and adapt the procedure. This addresses both the difficulty of extracting reliable information from text and the cost and learning curve of adopting computational methods. Section 6 explains the available research assets, their reuse, and the work that remains.

The empirical workflow has three steps: summarizing long documents (Section 3), extracting topics and attributed positions (Section 4), and connecting those topics to firm disclosures (Section 5). Each section distinguishes the general method, its implementation in the running application, and the resulting research outputs.

---≠≠≠