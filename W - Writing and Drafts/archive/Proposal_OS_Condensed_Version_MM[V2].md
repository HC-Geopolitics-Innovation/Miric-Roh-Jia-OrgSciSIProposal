# Proposal for Organization Science

# Overcoming Data Bottlenecks and Enabling Research in New Domains by Leveraging AI-Enabled Research Pipelines

**Proposal for Special Issue:** AI-Enabled Frontiers in Organizational Science (*Organization Science*)

**CFP / URL:** [https://orgsci.org](https://orgsci.org/)

**Repository:** [https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis](https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis)

**Authors:** Jia, Miric, and Roh (in alphabetical order)

---

## Table of Contents

- [1. Introduction](#1-introduction)
    - [1.1. Generative AI-Enabled Pipelines for Information Extraction and Synthesis](#11-generative-ai-enabled-pipelines-for-information-extraction-and-synthesis)
- [2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?](#2-why-an-ai-enabled-data-pipeline-vs-allowing-an-llm-to-handle-the-entire-task)
- [3. A Large Language Model Enabled Research Pipeline: Leveraging US Congressional Hearings](#3-a-large-language-model-enabled-research-pipeline-leveraging-us-congressional-hearings)
    - [3.1. Long-Document Text Summarization](#31-long-document-text-summarization)
        - [3.1.1. Overview of Processing Pipeline](#311-overview-of-processing-pipeline)
        - [3.1.2. Application: Summarizing Long Text Congressional Hearings](#312-application-summarizing-long-text-congressional-hearings)
        - [3.1.3. Research Outputs](#313-research-outputs)
    - [3.2. Extracting Topics, Positions and Arguments from Long-Form Documents](#32-extracting-topics-positions-and-arguments-from-long-form-documents)
        - [3.2.1. Overview of Processing Pipeline](#321-overview-of-processing-pipeline)
        - [3.2.2. Application: Extracting Stances and Arguments around Focal Topics](#322-application-extracting-stances-and-arguments-around-focal-topics)
        - [3.2.3. Research Outputs](#323-research-outputs)
    - [3.3. Policy Relevance for Publicly Listed Firms](#33-policy-relevance-for-publicly-listed-firms)
        - [3.3.1. Overview of Processing Pipeline](#331-overview-of-processing-pipeline)
        - [3.3.2. Application: Connecting Focal Concerns and Opportunities of Policy Makers to Business Areas of Publicly Listed Firms](#332-application-connecting-focal-concerns-and-opportunities-of-policy-makers-to-business-areas-of-publicly-listed-firms)
        - [3.3.3. Research Outputs](#333-research-outputs)
- [4. Research Design Enabled by LLM Data Pipeline: Evaluating the Impact of Privacy Policy Debate Following the Cambridge Analytica Scandal on the Trajectory of Firm Corporate Research on Privacy Technology](#4-research-design-enabled-by-llm-data-pipeline-evaluating-the-impact-of-privacy-policy-debate-following-the-cambridge-analytica-scandal-on-the-trajectory-of-firm-corporate-research-on-privacy-technology)
- [5. Reproducible and Adaptable Data Pipelines with Coding Agents](#5-reproducible-and-adaptable-data-pipelines-with-coding-agents)

---

## 1. Introduction

Textual data has provided a rich resource for researchers to answer a wide variety of questions that were otherwise difficult to measure. Prior to the advances that have been enabled through rich textual data and text analysis methods (e.g., topic modeling, keyword extraction), researchers relied heavily on structured datasets such as the USPTO patent database, Compustat, or other structured financial datasets. However, the availability of large-scale textual data from documents such as 10-K financial statements, patent abstracts or claims, or corporate websites (xxx; xxx) has opened new avenues for research. This has not replaced the earlier structured datasets, but provided new inputs which could augment these tools. Data availability is an important enabler of research advancement (xxx; xxx), and empirical approaches that utilize textual data—such as topic modeling, text embeddings to compute textual distance, or text classification (xxx)—have enabled the investigation of new questions.

One critical limitation, however, is that while textual data is abundant, much of it faces an important constraint: approaches such as topic modeling or embedding construction typically require text documents of comparable length (ideally relatively short) with a high share of informative content (meaningful statements) relative to noise (boilerplate or generic statements). This often hidden constraint has impacted research in two ways. First, researchers are avoiding contexts where they cannot have clean standardized textual data. Second, when they are using these tools they may be often introducing considerable noise into the process, as the long textual documents may have an overemphasis of noise relative to the signal latent in the data.

Large language models (LLMs) have emerged as a powerful research tool that has the potential to transform research and provide valuable new inputs and methodologies. There has been a surge of attempts to use these large language models to fundamentally automate and replicate parts of the research process, which are laboriously being performed by researchers. These include attempts to use LLMs for theorizing (xxx), testing assumptions (xxx), performing classification (xxx), and clustering data (xxx). However, any attempts to use such tools should be met with caution, as their internal processes are fundamentally opaque and devolving control, decision making and outputs to such a model should be met with skepticism, or at least require transparency by documenting choices and outputs in each step of the process such that they could be replicated.

In the proposed research project, we are advocating that large language models are powerful tools which should be widely used, but this should be done tactically as part of a transparent and clear research pipeline which does not devolve full control to a large language model, and where control is devolved, it is done so in a way that allows for inspection of inputs and outputs as well as clear potential validation points. We argue that LLMs can be a critical enabler for research, but that they should be part of a documented research pipeline.

We argue that large language models excel at two types of critical research tasks and therefore any type of data pipeline should leverage large language models at these two specific tasks, while allowing user evaluation and interpretability at other stages. The two areas where large language models are exceptionally effective are:

1. **Synthesizing text** (generating readable, coherent text based on existing documents); and
2. **Generating code** (producing machine-readable instructions that can be systematically executed and tested).

Established text analysis methods, for which we have established routines, validation standards, and verifiable properties are still relevant and can be augmented by these large language models focusing on these two strengths of this technology while avoiding potential pitfalls.

We develop a data pipeline and apply our proposed methodology on a context relevant for organization researchers: studying how changes in government debate around regulating a technology, associated with changes in the innovation trajectory of firms within that industry. We specifically focus on understanding how the policy debate around regulating technology firms following the Cambridge Analytica scandal. The fundamental challenge in studying this type of question is identifying which firms were likely impacted by this policy, so that we could compare this to a counterfactual of firms which were credibly not impacted. This information is embedded within textual data, but it requires developing a careful, verifiable and transparent data pipeline to construct and identify this data.

### 1.1. Generative AI-Enabled Pipelines for Information Extraction and Synthesis

We develop a framework which provides an example of a data pipeline which involves three data processing tasks, which leverage LLMs but do not devolve full control. These are tasks which provide verifiable, reproducible and adaptable pipelines. Researchers can tweak these methods to extract different insights, or apply this to data of their choice.

#### 1.1.1. Overview of Data Pipeline and Processing Tasks

a. ***Textual Summarization.*** Taking large, complex textual documents, which contain considerable noise but embedded data, splitting this into chunks and using LLMs to generate textual summaries, synthesizing and aggregating. We demonstrate this approach on congressional testimony on (ALBERT confirm -- make an appendix about data sources, and processing), summarizing long and convoluted documents into abstracts that can be subsequently used as "abstracts" for where research using text classification, topic modeling or language distance from embeddings in more reliable ways.

b. ***Stance Extraction.*** Using LLMs to identify the positions of different actors (e.g., Congress members, firms, government agencies) on specific topics, allowing researchers to distill the nuances of arguments, positions that each individual takes on an issue. We apply this to congressional testimony to identify the stances of individuals on the issues which emerge in this debate, within a format that can be utilized in subsequent research.

c. ***Debate Relevance to Firm Business Area.*** Using the distilled stances of individuals within the debate we create a synthesis of the debate. This can then be compared to the business descriptions of firms to identify which firms are subject to this debate. In our empirical context, this means a framing of what the key issue that the policy makers are debating and attempting to regulate. We then compare this to the 10-K financial statements of firms which describe their business operations. This allows us to study and identify the firms which are subject to these policies and those which are not.

#### 1.1.2. Reproducing these AI-Driven Pipelines for Alternative Research Questions

Our methodology thus far leverages the power of large language models for text extraction, synthesis and data cleaning. However, these models also excel at writing code, which is automatically tested, verified and validated. By providing our pipeline's code and methodologies in a GitHub repository where the codebase is available, researchers can use their own coding agents to either improve upon our methodology, or apply this methodology on their own setting and data.

We believe this is a framework that can guide how large language models can be used to adapt or deploy research models in the future.

## 2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?

One question that inevitably emerges is why researchers should develop a structured, LLM-enabled pipeline rather than simply prompting a frontier LLM to process entire context windows and execute the entire task end-to-end. Even if current models have limitations, one might worry that future frontier models will continue to advance.

We argue that there are three critical reasons for using LLMs as part of a carefully crafted research pipeline rather than fully devolving control:

- **Transparency and Control:** Concerns regarding LLM model transparency, reliability, and stability typically arise when researchers cede full autonomy to a model and ask it to arrive at an unassisted solution. The internal choices, decisions and intermediate outputs are not visible and verifiable. By using an LLM to execute a specific step (where it is superior to alternatives) within a larger research design (e.g., topic modeling of synthesized summaries), researchers can ensure their designs are reproducible, clear and verifiable.

- **Auditability and Systematic Replication:** While LLMs can formulate reasoning internally, their outputs often depend heavily on subtle nuances in prompt formulation, model versioning, and temperature settings. By carefully engineering a structured research pipeline, researchers can leverage LLMs at discrete intermediate steps while fully documenting every phase of the process at scale. This modular approach provides more consistent outputs.

- **Model Context Windows:** Even though frontier language models have large context windows (they can process long text documents), they still do so in an opaque way and may miss part of the documents, or present them in an inconsistent manner, especially when summarizing corpora of documents. Carefully designing and partitioning this process ensures that data extraction remains reliable, transparent, and reproducible regardless of underlying model advances.

## 3. A Large Language Model Enabled Research Pipeline: Leveraging US Congressional Hearings

Here we summarize and outline the described pipeline split across three related tasks (or problems) solved by LLMs.

### 3.1. Long-Document Text Summarization

Many textual documents contain important information, but also contain noisy and complex textual data. Large language models can provide a concise, information-rich summary that can be utilized in subsequent research tasks.

#### 3.1.1. Overview of Processing Pipeline

A pipeline to manage this process is as follows (summarized at length in xxx):

a. **Understand Document Structure and Define Semantic Partitioning.** Long textual documents often have a particular structure, and therefore may be split into meaningful chunks. *Context-aware chunking* uses meaningful units of text in the document, such as a document section or a speaker's uninterrupted contribution to split this into chunks which can be processed by the LLM. The document is partitioned into these chunks and processed further.

b. **Summarize and Combine the Inputs.** Each chunk of text is provided to an LLM with instructions outlining the desired format of the summary, and the key information which should be extracted. The outputs of this can be combined in a variety of ways, such as recursively summarizing chunks or using a dedicated "reduce" stage to combine the summaries. This is referred to as a "map-reduce" approach.

c. **Model Selection, Validation and Deployment.** This is inherently an iterative process, where the researcher must test different approaches for partitioning, prompts for summarization, models for summarization, and finally combination strategy. All of these tests can be validated by testing the intermediate outputs (partitions, summaries, outcomes for different models), and validated against ground truth where such data exists. Once the optimal set of choices is identified, the pipeline is deployed on the entire corpus of documents.

#### 3.1.2. Application: Summarizing Long Text Congressional Hearings

We apply this pipeline to a corpus of US Congressional hearing testimonies. The corpus consists of hearing transcripts spanning from 1995 to 2022, with multiple sessions per year. Hearings are typically long, often exceeding 100 pages, and feature multiple witnesses and committee members presenting testimony and engaging in Q&A discussions.

To apply the pipeline, we first partition each hearing into individual witness testimonies. Within each testimony, we use sentence-level splitting to ensure granular coverage. These segments are then processed using the Map-Reduce summarization approach, with a "reduce" stage to consolidate summaries from multiple witnesses into a single comprehensive hearing summary.

These summaries are tested with different prompts, models and splitting strategies and validated against human-made summaries for the hearings where they are available.

[FIGURES ABOUT HERE]

#### 3.1.3. Research Outputs

The summarization pipeline yields a transparent pipeline of code and prompts, as well as intermediate outputs at each stage of the process which can be deployed (utilized) further.

1. **Partitioned Textual Documents:** A cleaned and partitioned version of each hearing which can be uploaded to an LLM without exceeding the context windows.

2. **Summarized Partitions:** A summary of each partition, generated by feeding the partitions into an LLM.

3. **Committee Hearing Summaries:** Aggregated summaries from individual partitions into high-level summaries of the overall hearing proceedings, capturing the main themes, discussions, and conclusions. An output of the map-reduce process.

### 3.2. Extracting Topics, Positions and Arguments from Long-Form Documents

Large language models can also extract subtle but important nuance from a textual document, specifically related to a topic of interest. In this step, we provide a method for extracting topics, positions and arguments from long-form documents.

#### 3.2.1. Overview of Processing Pipeline

A pipeline to manage this process is as follows (summarized at length in xxx):

a. **Extract Topics from Textual Summaries.** From the long-form textual summaries, researchers can identify the major topics being discussed within each textual summary. Because there are now condensed, information-rich summaries, a variety of existing models may be effective for this task.

b. **Filter Textual Summaries by Topic Relevance.** The partitioned text chunks contain subtle and nuanced arguments. However, as described in Section 3.1, many of these chunks contain noise, such as generic statements, statements made by other entities or other irrelevant information. Large language models can be used to filter out the chunks which are relevant to having a stance on the focal topic.

c. **Extract Arguments and Stances from Relevant Textual Summaries.** Within the filtered chunks, the LLM is tasked with extracting key positions related to the focal topic. This might include identifying whether the statement is for or against the topic, or the specific nuance related to the statement, as well as contextualizing the statement with information from the document.

d. **Aggregate and Summarize.** The output of the earlier section provides a set of concise data about the stances of individuals on a focal topic. These can be aggregated or summarized in different ways and at different levels of granularity.

e. **Prototyping and Validation.** The goal of this exercise is to extract information which is otherwise difficult to capture and contextualize at scale. While this is challenging to validate precisely (i.e., quantitatively because that data does not currently exist), it is possible to compare against other baselines and identify whether these are somewhat comparable. We provide an example by validating our summaries against human-generated ones.

#### 3.2.2. Application: Extracting Stances and Arguments around Focal Topics

We apply this methodology to extract stances and arguments from US Congressional hearings. First, we filter out summaries which are not relevant to the topic of interest and extract the arguments and stances related to the topic of interest. For instance, within congressional debate on a particular topic (for example security and privacy of consumers), it becomes possible to capture both the arguments related to the risks that a policy topic presents (e.g., potential misuse of data, impact on free speech, etc.), as well as the potential opportunities (e.g., economic growth, innovation, etc.).

We aggregate these summaries in different ways, but ultimately arrive at a numerical measure that captures the overall tenor of the discussion within the congressional debate. In doing so, we are able to capture the predominant stance and arguments being made by policy makers.

[FIGURES ABOUT HERE]

#### 3.2.3. Research Outputs

The outputs of this pipeline are:

1. **Topics of Debate within Congressional Hearings.** A list of topics which are discussed within the textual documents, standardized and assigned to each hearing document.
2. **Filtered Arguments and Examples on Each Topic.** A set of statements filtered from each congressional debate that captures the main arguments related to each specific topic, classified as to whether they are examples of the policy being discussed within the congressional debate as an opportunity or a threat.
3. **Predominant Stances on Each Topic.** An index for each topic which indicates the extent to which it is perceived as an opportunity or a threat by policy makers in each hearing, also aggregated at the year and the committee levels providing an overall description of the main stances on each topic.

### 3.3. Policy Relevance for Publicly Listed Firms

The earlier analysis provides detailed information extraction from congressional debate about economically important policies that will directly shape the external environment of publicly listed firms. While there are anecdotal examples of firms being influenced by these policies, it is difficult to quantify this at scale and conclude to what extent firms are being impacted by these policies.

To quantitatively measure the relevance of policy debate to publicly listed firms requires computing the relatedness between policy documents and corporate disclosures which reflect the business of the firm. This can fundamentally be done by computing the textual distance between the documents that convey the policy relevance, and documents that describe the business of the firm. LLMs can be used to either filter or summarize the text, as described above, in order to improve the accuracy of this distance measure.

#### 3.3.1. Overview of Processing Pipeline

A pipeline to manage this process is as follows (summarized at length in xxx):

a. **Identify & Pre-Process Focal Documents.** In the earlier process, we filtered out the text chunks that reflected a position or a stance of individuals or organizations on a particular topic. As an optional step, they could also be further summarized into a summary of the stance on each issue. Similarly, an optional step is to summarize textual documents from companies (for example, 10-Ks).

b. **Compute Semantic Distance and Topical Relevance.** Using either the raw textual documents, or summaries of the documents created in the earlier step, we can compute the semantic relatedness of these documents to the 10-K statements of firms. This can be done using textual distance measures between document embeddings (e.g., cosine similarity using transformer-based embeddings), or by using large language models to compute semantic similarity. The robustness or sensitivity to different measures of similarity can be tested or validated.

c. **Aggregate Distance and Relevance Measures.** The outputs from the earlier phase can then be further aggregated up to the level appropriate for a specific analysis.
For instance, it may be relevant to compute the impact of a policy debate on a specific firm over time, a specific firm in aggregate or across an entire industry. Using fine-grained outputs in each stage of the process allows for validation, verification, and evaluation of each stage of the process.

#### 3.3.2. Application: Connecting Focal Concerns and Opportunities of Policy Makers to Business Areas of Publicly Listed Firms

We apply this phenomenon to understand how the congressional policy debate around a particular policy topic impacts the business of firms. We focus on a particularly transformational shift in the debate of regulators, a shift about regulating technology companies in relation to consumer privacy following the Cambridge Analytica scandal which affected Facebook / Meta.

We utilize the filtered text from Section 3.2.3 to first create a summary of the Congressional debate on the topic of Privacy and Security, and the primary concerns and opportunities. We then compute the semantic distance between these summaries and the 10-K statements of publicly listed firms. We then aggregate these measures to identify which are the firms for whom these policies have the potential to impact their business. We report both the raw data that can be leveraged for subsequent research, as well as an aggregate measure that is relevant for us.

#### 3.3.3. Research Outputs

The outputs of this pipeline are:

1. **Summary of Policy Opportunities and Concerns for each Congressional Session.** A textual summary of the key concerns and opportunities related to a particular policy that policy makers discuss during a particular session.

2. **Aggregated Summary of Opportunities and Concerns for each Major Policy Issue.** A synthesized summary of the primary opportunities and concerns related to each policy for policy makers.

3. **Scores for Policy Relevance to Publicly Listed Firms.** A score (distance-based measure) of how much a particular policy (either opportunity or threat) relates to the specific business activities of a publicly listed firm.

## 4. Research Design Enabled by LLM Data Pipeline: Evaluating the Impact of Privacy Policy Debate Following the Cambridge Analytica Scandal on the Trajectory of Firm Corporate Research on Privacy Technology

As described above, we demonstrate how the application of our data pipeline to congressional testimony and company 10-K filings allows us to quantify which firms were impacted by this policy and study this question in a way which was not previously possible. We focus on a specific empirical research question: how the increasing intensity of Congressional attention to consumer privacy after 2016 (the Cambridge Analytica scandal) and calls for regulation and legislation was associated with the innovation trajectories of companies which were affected. In addition, the AI-enabled nature of the pipeline with intermediate outputs allows a careful scrutiny and assessment of such approaches, far more than what would have otherwise been possible in other research applications. We utilize the relevance measures computed in Section 3.3.3 to identify the specific firms most affected by the privacy policy debates. We then proceed to match these scores to the innovation portfolios of publicly listed firms.

We can observe from the data how, following the Cambridge Analytica scandal, firms which were impacted by the legislation being discussed by policy makers (excluding Facebook, Google, and other technology companies which were likely impacted) increased their innovative activity in domains related to data privacy and security, while the unaffected firms, which were not likely to be subject to this legislation, remained unaffected.

## 5. Reproducible and Adaptable Data Pipelines with Coding Agents

While this data pipeline can leverage AI tools to perform important analysis tasks, there is an additional important benefit which is emerging in empirical research. Research papers, made available through platforms such as GitHub in easy machine-readable formats (Markdown, Python code, Stata, and R), can be deployed easily through coding agents, in order to build entire data pipelines in an instant. In addition to providing a methodology which we believe can advance research with text data, we also want to advocate for, and provide a framework for using the online repository of these papers as a medium where researchers can share their tools and have their tools be easily deployable and adaptable for other researchers. To demonstrate this in Appendix XX, we provide a sample agent prompt and a sample implementation plan generated by an LLM. Researchers could do the same with their own AI tools, augment the implementation plan and deploy it further.