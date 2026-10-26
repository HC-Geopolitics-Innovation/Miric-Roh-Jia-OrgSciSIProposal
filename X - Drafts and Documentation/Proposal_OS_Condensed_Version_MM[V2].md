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
- [3. Three instances of Large Language Model Enabled Research Pipelines leveraging US Congressional Hearings as a motivating context](#3-three-instances-of-large-language-model-enabled-research-pipelines-leveraging-us-congressional-hearings-as-a-motivating-context)
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
- [4. Empirical Application Enabled by AI Data Pipeline: Evaluating the Impact of Privacy Policy on Innovation Regulation](#4-empirical-application-enabled-by-ai-data-pipeline-evaluating-the-impact-of-privacy-policy-on-innovation-regulation)
- [5. Reproducible and Adaptable Data Pipelines with Coding Agents](#5-reproducible-and-adaptable-data-pipelines-with-coding-agents)

---

## 1. Introduction

Textual data has provided a rich resource for researchers to answer a wide variety of questions that were otherwise difficult to measure. Prior to the advances that have been enabled through rich textual data and text analysis methods (e.g. topic modeling, keyword extraction), researchers relied heavily on structured datasets such as the USPTO patent database, Compustat, or other structured financial datasets. However, the availability of large-scale textual data from documents such as 10-K financial statements, patent abstracts or claims, or corporate websites (xxx; xxx) has opened new avenues for research. This has not replaced the earlier structured datasets, but provided new inputs which could augment these tools. Data availability is an important enabler of research advancement (xxx; xxx), and empirical approaches that utilize textual data—such as topic modeling, text embeddings to compute textual distance, or text classification (xxx)—have enabled the investigation of new questions.

One critical limitation, however, is that while textual data is abundant, much of it faces an important constraint: approaches such as topic modeling or embedding construction typically require text documents of comparable length (ideally relatively short) with a high share of informative content (meaningful statements) relative to noise (boilerplate or generic statements). This often hidden constraint has impacted research in two ways. First, researchers are avoiding contexts where they cannot have clean standardized textual data. Second, when they are using these tools they may be often introducing considerable noise into the process, as the long textual documents may have an overemphasis of noise relative to the signal latent in the data. 

Large language models (LLMs) have emerged as a powerful research tool that has the potential to transform research and provide valuable new inputs and methodologies. There has been a surge of attempts to use these large language models to fundamentally automate and replicate parts of the research process, which are laboriously being performed by researchers. These include attempts to use LLMs for theorizing (xxx), testing assumptions (xxx), performing classification (xxx), and clustering data (xxx).  However, any attempts to use such tools should be met with caution, as their internal processes are fundamentally opaque and devolving control, decision making and outputs to such a model should be met with skepticism, or at least require transparency by documenting choices and outputs in each step of the process such that they could be replicated. 

In the proposed research project, we are advocating that large language models should be used tactically as part of a transparent and clear research pipeline which does not devolve full control to a large language model, and when it does, does so in a way that allows for inspection of inputs and outputs as well as clear potential validation points. We argue that LLMs can be a critical enabling input for research, but that they should be part of a documented research pipeline, that leverages two domains where LLMs are particularly good. 

1. **Synthesizing text** (generating readable, coherent text based on existing documents); and
2. **Generating code** (producing machine-readable instructions that can be systematically executed and tested).

We argue that established text analysis methods, for which we have established routines, validation standards, and verifiable properties can be augmented by these large language models using these two critical features of this technology. We believe that this is a much more sound, verifiable and transparent approach to using these tools, and can overcome the hesitation and skepticism around using this technology for research. 

While we believe these arguments can apply broadly to a wide range of research applications, we have identified a particularly salient use case for organizational researchers that can be leveraged and applied. 

Long textual documents such as congressional testimony of firm 10K statements are valuable artefacts about the direction of government debate and legislation, as well as information about the strategies and business areas of firms themselves. However, they suffer from the constraint that they are long and contain a lot of generic boilerplate language that obscures the latent nuance (the signal) within the long and formulaic text (noise). Our proposal demonstrates how the use of large language models, as a critical but narrow part of a data processing pipeline can create reliable and useful textual data, which can enable further research that was previously not possible (or which in previous cases relied on measurement in the coarsest possible forms).

Using these long textual documents, we develop several LLM enabled research pipelines which allow us to generate new data and insights, which translate into future research. We then demonstrate how this can be used to answer informative research questions and how this can be replicated or adapted by other scholars. In summary, within the proposed project we contribute the following elements. 


1. **Generative AI enabled Pipelines for Information Extraction and Synthesis.** We show how an example of long information rich, but noisy textual documents from the US Congressional record—specifically, hearing transcripts can be transformed into actionable data inputs through the use of LLM enabled research pipelines. We develop and demonstrate LLM enabled data pipelines for three types of information extraction tasks, that can enable different subsequent research outputs. 

a.  ***Textual Summarization.*** Taking large, complex textual documents, splitting them into chunks, using LLMs to generate textual summaries of chunks, and then synthesizing these summaries into final, actionable inputs. This provides the equivalent of reliable, structured "abstract" for documents where such summaries do not exist. This subsequently enables tasks such as text classification, topic modeling or language distance from embeddings in more reliable ways. 

b.  ***Stance Extraction.*** Using LLMs to identify the positions of different actors (e.g. Congress members, firms, government agencies) on specific topics, allowing researchers to distill the nuances of an academic debate and identify the positions that each individual takes on an issue, formulating a rich description of the debate, with data in a tabular format that can be utilized in subsequent research. 

c.  ***Debate Relevance to Firm Business Area.*** Using fine-grained information on the topical debate as well as on the understanding of the business of firms based on their 10K statements, we develop an LLM enabled pipeline to establish the extent to which firms have the potential to be impacted by the policy debates. 

These data pipelines are the foundation of our proposal, and the contribution that enables further research. However, we also demonstrate the impact of this with two additional elements. 

2. **Demonstration of Empirical Research Question Enabled by LLM Created Variables** While the ability to identify and understand these LLM enabled pipelines is critical for researchers, we further illustrate how the variables that result from this exercise can allow us to construct an empirical research paper that would otherwise not be possible for us to investigate. We document the increasing scrutiny of privacy regulation within US congressional debates and use the proposed methodology to identify which firms are subject to these policy changes, and which can provide a reasonable counterfactual because they are unaffected by these policies. We utilize this framework to identify the firms which are influenced (treated) by this policy, and which remain unaffected (control) and demonstrate the response of firms following these policy debates. 

3. **Reproducing these AI-Driven Pipelines for Alternative Research Questions.** 

Our methodology thus far leverages AI models as a tool which summarizes and extracts information from other sources. We demonstrate the benefit of this research tool in our particular context. However, we expect that methodology can be applicable in the long term to other settings, documents and research questions. For this reason we also demonstrate how our research can be reproduced, but leveraging another powerful functionality of Large Language Models: AI Coding Agents. We demonstrate how researchers can apply our methodology to a different research context, but directing their own AI coding agents to understand the code from our public repository, develop an implementation plan for the researcher to review, and implement it within their own research projects. We hope that this can set a precedent for how research can be shared in manner that is transparent, reproducible and extensible.

This proposal proceeds as follows. We first outline the rationale for why one might use such specific pipelines, rather than simply relying on an LLM to provide answers end-to-end. We next describe the three distinct data pipelines we develop for text summarization, stance extraction, and topic relevance identification, using US Congressional hearings as a motivating context. These are summaries for the sake of brevity, which we then elaborate on in the accompanying GitHub repo. In section 4 we demonstrate an application of the variables constructed from this in a novel research context. Finally, in section 5 we then provide a framework for researchers to apply these frameworks to a different methodology / approach. 

## 2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?

One question that inevitably emerges is why researchers should develop a structured, LLM-enabled pipeline rather than simply prompting a commercial LLM to process entire context windows and execute the entire task end-to-end. Furthermore, while existing models encounter limitations, future frontier models will continue to advance.

There are two critical reasons for designing an explicit data pipeline:

- **Transparency and Control:** Concerns regarding LLM model transparency, reliability, and stability typically arise when researchers cede full autonomy to a model and ask it to arrive at an unassisted solution. By contrast, our approach uses the LLM in targeted roles: to write code, execute specific processing steps, or summarize discrete textual segments based on defined source documents. By developing an AI-enabled data pipeline, we overcome specific bottlenecks in existing research workflows rather than re-engineering parts of the research process where unconstrained LLM execution lacks control and statistical guarantees.

- **Auditability and Systematic Replication:** While LLMs can formulate reasoning internally, their outputs often depend heavily on subtle nuances in prompt formulation, model versioning, and temperature settings. By carefully engineering a structured research pipeline, researchers can leverage LLMs at discrete intermediate steps while fully documenting every phase of the process at scale. This modular approach provides a degree of oversight, reproducibility, and methodological transparency that would otherwise be impossible.

## 3. Three instances of Large Language Model Enabled Research Pipelines leveraging US Congressional Hearings as a motivating context

### 3.1. Long-Document Text Summarization

Many textual documents contain important information, but also contain noisy, and complex textual data. Large language models can provide a concise, information-rich summary that can be utilized in subsequent research tasks. 

Even though frontier language models have large context windows (they can process long text documents), they still do so in an opaque way and may miss part of the documents, or present them in an inconsistent manner, especially when summarizing corpora of documents. Carefully designing and partitioning this process ensures that data extraction remains reliable, transparent, and reproducible regardless of underlying model advances.

#### 3.1.1. Overview of Processing Pipeline

A pipeline to manage this process is as follows (summarized at length in xxx):

a. **Understand Document Structure and Define Semantic Partitioning.** Long textual documents often have a particular structure, and therefore may be split into meaningful chunks. *context-aware chunking* uses meaningful units of text in the document, such as a document section or a speaker's uninterrupted contribution to split this into chunks which can be processed by the LLM. The document is partitioned into these chunks and processed further. 

b. **Summarize and Combine the Inputs.** Each chunk of text is provided to an LLM with instruction which outlines the desired format of the summary, and the key information which should be extracted. The outputs of this can be combined in a variety of ways, such as recursively summarizing chunks or using a dedicated "reduce" stage to combine the summaries. This is referred to as a "map-reduce" approach. 

c. **Model Selection, Validation and Deployment.** This is inherently an iterative process, where the researcher must test different approaches for partitioning, prompts for summarization, models for summarization, and finally combination strategy. All of these tests can be validated by testing the intermediate outputs (partitions, summaries, outcomes for different models), and validated against ground truth where such data exists. Once the optimal set of choices is identified, the pipeline is deployed on the entire corpus of documents. 

#### 3.1.2. Application: Summarizing Long Text Congressional Hearings

We apply this pipeline to a corpus of US Congressional hearing testimonies. The corpus consists of hearing transcripts spanning from 1995 to 2022, with multiple sessions per year. Hearings are typically long, often exceeding 100 pages, and feature multiple witnesses and committee members presenting testimony and engaging in Q&A discussions.

To apply the pipeline, we first partition each hearing into individual witness testimonies. Within each testimony, we use sentence-level splitting to ensure granular coverage. These segments are then processed using the Map-Reduce summarization approach, with a "reduce" stage to consolidate summaries from multiple witnesses into a single comprehensive hearing summary.

These summaries are tested with different prompts, models and splitting strategies and validated against human-made summaries for the hearings where they are available. The detailed output, prompts, splitting strategies, collapsing choices, validation tables and code for each stage are detailed in the Appendix.

#### 3.1.3. Research Outputs

The summarization pipeline yields a transparent pipeline of code and prompts, as well as intermediate outputs at each stage of the process which can be deployed (utilized) further. 

1. **Partitioned Textual Documents:** A cleaned and partitioned version of each hearing which can be uploaded to an LLM without exceeding the context windows. 

2. **Summarized Partitions:** A summary of each partition, generated by feeding the partitions into an LLM. 

3. **Committee Hearing Summaries:** Aggregated summaries from individual partitions into an overall high-level summaries of the overall hearing proceedings, capturing the main themes, discussions, and conclusions. An output of the map-reduce process. 

### 3.2. Extracting Topics, Positions and Arguments from Long-Form Documents

In addition to summarizing text, researchers may apply large language models to extract subtle but important information from a textual document, specifically related to a topic of interest. In this step, we provide a method for extracting topics, positions and arguments from long-form documents. 

#### 3.2.1. Overview of Processing Pipeline

A pipeline to manage this process is as follows (summarized at length in xxx):

a. **Extract Topics from Textual Summaries.** From the long-form textual summaries, researchers can identify the major topics being discussed within each textual summary. Because there are now, condensed, information rich summaries, traditional topic models may work well. In addition however, researchers could leverage large language models to extract topics.   

b. **Filter Textual Summaries by Topic Relevance.** The partitioned text chunks contain subtle and nuanced arguments. However, as described in section 3.1.x, many of these chunks contain noise, such as generic statements, statements made by other entities or other irrelevant information. Large language models can be used to filter out these chunks which are not relevant. Using a large-language model, we can select a focal topic and then filter out only the chunks which are relevant to this focal topic.  

c. **Extract Arguments and Stances from Relevant Textual Summaries.** Within the filtered chunks, researchers can use an LLM to extract arguments and stances related to the focal topic. We can implement this by using an LLM to extract the key position related to each topic. For instance, the argument for or against a particular topic (or the stance of an individual on a topic). 

d. **Aggregate and Summarize.** The output of the earlier section provides a set of concise and information rich arguments about the arguments or stance on the focal topic. However, there is a choice of how these arguments can be aggregated or summarized. One approach is to count the number of times a particular stance is mentioned, or otherwise numerically aggregate the frequency of a particular stance. Otherwise, researchers can use an LLM to further aggregate or summarize these arguments and stances, into a summary of the key debates. 

e. **Prototyping and Validation.** The goal of this exercise is to extract information which is otherwise difficult to capture and contextualize at scale. While this is challenging to validate precisely (i.e. quantitatively), it is possible to compare against other baselines where there exists some external validation. For instance to compare against other document categories or summaries.

#### 3.2.2. Application: Extracting Stances and Arguments around Focal Topics 

We apply this methodology to extract stances and arguments from US Congressional hearings. First, we use an LLM to extract key topics from the hearing summaries produced in the previous step. Then, we filter out summaries which are not relevant to the topic of interest. Finally, we extract the arguments and stances related to the topic of interest from the filtered summaries. 

This yields a set of statements which provides information about the key arguments related to each topic. For instance, within congressional debate on a particular topic (for example security and privacy of consumers), it becomes possible to capture both the arguments related to the risks that a policy topic presents (e.g. potential misuse of data, impact on free speech, etc.), as well as the potential opportunities (e.g. economic growth, innovation, etc.). 

Using these individual summaries, we are able to provide aggregation in different ways. First, we are able to aggregate the count of times a particular stance is made, or stance is taken on a particular topic (e.g. the number of times that the risks of a policy are mentioned, as opposed to the number of times the opportunities are mentioned).
Alternatively, we are able to identify the major threats and opportunities being mentioned, and in doing so, and create a textual summary of the threats and opportunities. In doing so, we are able to capture the predominant stance and arguments being made by policy makers. 

#### 3.2.3. Research Outputs

The outputs of this pipeline are: 
1. **Topics of Debate within Congressional Hearings.** A list of topics which are discussed within the textual documents, standardized and assigned to each hearing document. 
2. **Filtered Arguments and Examples on Each Topic.** A set of statements filtered from each congressional debate that captures the main arguments related to each specific topic, classified as as whether they are examples of the policy being discussed within the congressional debate as an opportunity or a threat. 
3. **Predominant Stances on Each Topic.** An index for each topic which indicates the extent to which it is perceived as an opportunity or a threat by policy makers in each hearing, also aggregated at the year and the committee levels providing an overall description of the main stances on each topic. 

### 3.3. Policy Relevance for Publicly Listed Firms

The earlier analysis provides detailed information extraction from congressional debate about economically important policies that will directly shape the external environment of publicly listed firms. However, a fundamental challenge of applying this to research is that it is challenging to link policy debates to the firms that are being affected. 

To identify the relevance of policy debate to publicly listed firms, fundamentally involves computing the semantic similarity or relatedness between policy documents and corporate disclosures. This can fundamentally be done by computing the textual distance between the documents that convey the policy relevance, and documents that convey about the business of the firm. LLMs can be used to either filter or summarize the text, as described above, in order to improve the accuracy of this distance measure. 

First, LLMs could be used to filter and identify the statements which capture the position of a policy debate (as described above), and identify the distance between those statements and the 10K statements of a firm. Second, LLMs could be used to summarize the documents which capture a particular stance of policy makers on this topic. Once these summaries have been created, which contain the key policy elements, computing the distance between these policy summaries and the 10K statements of a firm provides a measure of the relevance of the policy debate to the business of the firm. 

#### 3.3.1. Overview of Processing Pipeline

A pipeline to manage this process is as follows (summarized at length in xxx):

a. **Identify & Pre-Process Focal Documents.** In the earlier process, we filtered out the text chunks that reflected a position or a stance of individuals or organizations on a particular topic. These chunks could be used further. However, as an optional step, they could also be further processed and summarized using a large language model to summarize and synthesize the main insights based on these filtered chunks of text. Similarly, an optional step could be to summarize or synthesize textual documents from companies (for example 10-Ks) in order to succinctly describe the characteristics of the focal firm. 

b. **Compute Semantic Distance and Topical Relevance.** Using either the raw textual documents, or summaries of the documents created in the earlier step, we can compute the semantic relatedness of these documents to the 10k statements of firms. This can be done using textual distance measures between document embeddings (e.g. cosine similarity using transformer-based embedding), or by using large language models to compute semantic similarity. The robustness or sensitivity to different measures of similarity can be tested or validated. 

c. **Aggregate Distance and Relevance Measures.** Depending on the exact research question, and the unit at which the distance computation is calculated, the measures may be aggregated up to the level of theoretical interest. For instance, it may be of interest to aggregate the overall impact of policies on the business of a specific firm, but it might also be relevant to have a finer-grained measure the impact of a policy on the changing business of companies. To compute and test the robustness and sensitivity of this, the ability of researchers to provide fine-grained data outputs of each stage of the process, it allows for the understanding and evaluation of this process. 

#### 3.3.2. Application: Connecting Focal Concerns and Opportunities of Policy Makers to Business Areas of Publicly Listed Firms

We apply this phenomenon to understand how the congressional policy debate around a particular policy topic, on the business of firms. We focus one of the most important topics which emerged from the policy debate on the privacy and security of consumers (summarized below in xxx).

We utilize the filtered text from section 3.2.3. to first create a summary of the Congressional debate on the topic of Privacy and Security, and the primary concerns and opportunities. We then compute the semantic distance between these summaries and the 10-K statements of publicly listed firms. We then aggregate these measures to identify which are the firms for whom these policies have the potential to impact their business. We report both the raw data that can be leveraged for subsequent research, as well as an aggregate measure that is relevant for us. 

#### 3.3.3. Research Outputs

The outputs of this pipeline are: 

1. **Summary of Policy Opportunities and Concerns for each Congressional Session.** A textual summary of the key concerns and opportunities related to a particular policy that policy makers discuss during a particular session. 
2. **Aggregated Summary of Opportunities and Concerns for each Major Policy Issue.** A synthesized summary of the primary opportunities and concerns related to each policy for policy makers. 
3. **Scores for Policy Relevance to Publicly Listed Firms.** A score (distance-based measure) of how much a particular policy (either opportunity or threat) related to the specific business activities of a publicly listed firm.

## 4. Empirical Application Enabled by AI Data Pipeline: Evaluating the Impact of Privacy Policy on Innovation Regulation 

To demonstrate the impact of technology policy on the innovation trajectory of firms, we focus on a specific research question which would have otherwise been difficult to study without the specific research outputs of this data pipeline. In addition, the AI-enabled nature of the pipeline with intermediate outputs allows a careful scrutiny and assessment of such approaches, far more than what would have otherwise been possible in other research applications. 

We focus on a specific empirical research question, how the increasing intensity of Congressional attention to consumer privacy after 2016 (the Cambridge Analytica scandal) and calls for regulation and legislation was associated with the innovation trajectories of companies which were affected. We utilize the relevance measures computed in section 3.3.3. to identify the specific firms most affected by the privacy policy debates. We then proceed to match these scores to the innovation portfolios of publicly listed firms. 

We can observe from the data how, following the Cambridge Analytica scandal, firms which were impacted by the legislation being discussed by policy makers (excluding Facebook, Google, and other technology companies which were likely impacted), increased their innovative activity in domains related to data privacy and security. While the unaffected firms, which were not likely to be subject to this legislation remained unaffected. 

These are descriptive findings that point to the potential to use the methodology presented, in a transparent, replicable and scalable way to investigate research questions which would otherwise not have been possible. 

## 5. Reproducible and Adaptable Data Pipelines with Coding Agents

While this data pipeline can leverage AI tools to perform important analysis tasks, there is an additional important benefit which is emerging in empirical research. Research papers, made available through platforms such as GitHub in easy machine-readable formats (markdown, python code, stata and R), can be deployed easily through code agents, in order to build entire data pipelines in an instant. In addition to providing a methodology which we believe can advance research with text data, we also want to advocate for, and provide a framework for using the online repository of these papers as a medium where researchers can share their tools and have their tools be easily deployable and adaptable for other researchers. To demonstrate this in Appendix XX, we demonstrate a sample agent prompt and a sample implementation plan generated by an LLM. Researchers could do the same with their own AI tools, augment the implementation plan and deploy it further. 