## *Accompanying GitHub Page for Organization Science Paper Submission*

# Opening the Black Box of Large Language Models in Text-based Measurement: Staged Pipelines with Verifiable Checkpoints

**Milan Miric, Albert Roh, Nan Jia**  
*University of Southern California, Marshall School of Business*  
**Proposal for Special Issue:** AI-Enabled Frontiers in Organizational Science (*Organization Science*)  
**Repository:** [https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis](https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis)

Below we provide an overview of the repository structure, the main files in the paper, and the empirical demonstration.

---

## A. Abstract

Researchers increasingly use large language models (LLMs) to construct variables from long, noisy documents that were previously impractical to study at scale. When an LLM is used end to end, however, the final output is the only observable checkpoint. This opacity makes measures hard to validate and reproduce, and it conceals heterogeneity within documents, so systematic measurement error can bias subsequent analyses. More capable models will not resolve these concerns, because they stem from opacity and lack of control over design choices rather than limited capability. We propose decomposing LLM-based measurement into a pipeline of discrete stages, each producing an inspectable intermediate output. This design allows researchers to validate each stage against its own benchmark, locate where errors arise, revise one stage while reusing the others, and trace aggregate measures back to their components. We demonstrate the approach by processing 2,352 congressional hearings and firms’ 10-K filings to summarize hearings, extract policymakers’ stances, and measure firms’ exposure to the debate over consumer data privacy. Across 1,058 publicly traded firms, we demonstrate how the most exposed firms as reflected in our index experience a shift in their innovation trajectory towards both data anonymization and user-activity tracking. We aim to release the modular code and intermediate datasets, enabling researchers to adapt the pipeline with coding agents and to replicate it stage by stage.

---

## B. Main Proposal Documents

In this section we list and provide links to the proposal documents we submitted as part of this paper.

| Document | Description |
| :--- | :--- |
| **[P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md)** | Markdown (Github readable) version of main proposal document + technical appendix. |
| **[P2. Org Sci Proposal [Miric, Roh and Jia][PDF].pdf](P%20-%20Paper,%20Writing%20and%20Output/P2.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BPDF%5D.pdf)** | PDF version of main proposal document + technical appendix. |
| **[P3. Org Sci Proposal - Full Methodology [Miric, Roh and Jia].md](P%20-%20Paper,%20Writing%20and%20Output/P3.%20Org%20Sci%20Proposal%20-%20Full%20Methodology%20%5BMiric,%20Roh%20and%20Jia%5D.md)** | Extended methodological details. |

---

## C. Three-Step Text Analysis Pipeline Overview

The main pipeline steps are reported in the folder `T - Three Step Text Analysis Pipeline/`. For each of these there is a README providing an explanation of the methodology. Each example has a README walkthrough, a step-by-step notebook, and numbered folders for inputs, outputs, and logs. These are listed here for reference:

- **[T1 - Text Summarization](<T - Three Step Text Analysis Pipeline/T1 - Text Summarization/README.md>)**: Long-document turn-aware chunking and Map-Reduce summarization ([Facebook Hearing Walkthrough](<T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>)).
- **[T2 - Topic Extraction and Stance Analysis](<T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/README.md>)**: 111-topic policy taxonomy codebook and legislator stance panel ([Facebook Hearing Walkthrough](<T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>)).
- **[T3 - Topic Relevance and Corporate Disclosure](<T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/README.md>)**: Firm 10-K topic relevance to the consumer data privacy debate ([Facebook Hearing Walkthrough](<T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>)).

Each pipeline step opens with a workflow overview notebook and ends with a running example that follows the same hearing, the April 10, 2018 Facebook hearing with Mark Zuckerberg.

---

## D. Repository Structure

```
.
├── D - Data Collection and Processing/                      # Example of Text Inputs  (GovInfo, C-SPAN, 10-K)
│   ├── Data Collection Workflow Overview.ipynb
│   ├── D1 - GovInfo Congressional Hearings/
│   ├── D2 - C-SPAN Reference Abstracts/
│   ├── D3 - SEC Form 10-K Corporate Filings/
│   └── D4 - SST Sample Construction/
|
├── T - Three Step Text Analysis Pipeline/                     # Code for Pipeline Steps
│   ├── T1 - Text Summarization/                                # Long-document summarization
│   ├── T2 - Topic Extraction and Stance Analysis/              # Coonstruct topic stance measure
│   └── T3 - Topic Relevance and Corporate Disclosure/          # Firm 10-K exposure to privacy debate
|
├── X1 - Example of Research Enabled by LLM Pipeline/           # Empirical application and patent shifts
│   ├── X1.1 - Data for Matching and Patent Analysis/
│   ├── X1.2 - Notebooks for Matching and Aggregating Patent Data/
│   └── X1.3 - Notebooks for Analysis/
|
├── X2 - Example of Reproducing and Adapting the Research Pipeline/ # Coding agent adaptation guide
|
├── P - Paper, Writing and Output/                     # Main proposal documents and PDFs
│   ├── P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md
│   ├── P2. Org Sci Proposal [Miric, Roh and Jia][PDF].pdf
│   ├── P2. Org Sci Proposal [Miric, Roh and Jia][PDF].tex
│   ├── P3. Org Sci Proposal - Full Methodology [Miric, Roh and Jia].md
│   ├── P1.1 - PDFs for Submission/                    # Component and submission PDFs
│   ├── P1.2 - Latex style files/                      # Supporting style files and compilation script
│   └── figures/                                       # Rendered proposal figures
|
└── R - Results/                                       # Figures and tables matching D, T, X1
    ├── R1.1 - Figures/                                # High-resolution numbered figures (.png, .pdf, .svg)
    └── R1.2 - Tables/                                 # Summary tables and point estimates
```

---

## E. Key Empirical Results from Empirical Demonstration in Proposal

All figures below are displayed side by side as presented in the proposal. Click on any figure or heading to jump directly to its discussion and complete econometric notes in [`P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md`](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md).

### E1. Analysis of Congressional Debate Stance on Key Topics

As an example of the output of our stance measurement approach, below we provide a summary of the results of our analysis. Panel A reports the distribution of topics and balance of stances, highlighting consumer privacy as a dominant topic with emerging regulatory support, while Panel C tracks the structural surge in legislative support for privacy regulation following 2016.

#### [Figure 2. Topics and Overview of Stance (Panels A & C)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md#a22-application-extracting-stances-and-arguments-around-focal-topics)


| [Panel A: Distribution of Member Net Stances](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel C: Subtopic Polarization](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 2 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig2_panel_a.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 2 Panel C](P%20-%20Paper,%20Writing%20and%20Output/figures/fig2_panel_c.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

### E2. Relevance of Topics in Debate on Publicly Listed Firms


As an example of measuring the relevance of topics in the leglisative debate to the to individual firms, we provide a summary of the relevance scores aggregated at different levels. We compute semantic cosine similarity between synthesized congressional privacy debate statements and Form 10-K Item 1 business descriptions across public firms. In Panel A, we report the relevance to various sectors at the NAICS two digite level. In Panel B, we provide an example of the companies that are subject to (or exposed to) this congressional debate issue. 

#### [Figure 3. Topic Relevance Scores for Publicly Listed Firms](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md#a32-application-connecting-focal-concerns-and-opportunities-of-policymakers-to-business-areas-of-publicly-listed-firms)


| [Panel A: NAICS-2 Sector Cosine Relative to Mean](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Selected High and Low Relevance Firms](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 3 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig3_panel_a_naics_relevance.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 3 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig3_panel_b_top_firms.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

### E3. Example of Applying Scores to Debate Around Privacy Legislation

As an example of the application of our topic relevance scores, we demonstrate the application on the debate around privacy legislation. WUsing our policy exposure index, we examine corporate patenting responses before and after the 2016 privacy debate shock across relevance quartiles. Panel A shows that high-relevance firms account for the vast share of privacy patents, Panel B documents an increase patenting following 2016 concentrated heavily in Quartile 4, and Panel C decomposes this growth across specific privacy technology subclasses.

#### [Figure 4. Firm Topic Relevance and Privacy Patenting Pre- and Post-2016](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md#appendix-c-example-of-research-enabled-by-llm-data-pipeline)


| [Panel A: Distribution & Patent Intensity](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Pre/Post 2016 by Quartile](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel C: Pre/Post 2016 by Subclass](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: | :---: |
| [![Figure 4 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_panel_a_topic_relevance.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 4 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_panel_b_quartiles.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 4 Panel C](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_panel_c_subclasses.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

Here we continue this analysis, by providing a raw summary of the long-term technological trajectories from 1999 to 2021 across five distinct privacy classes (those related to tracking user data). Panel A plots annual patent counts across regulatory milestones, highlighting the surge in data anonymization and behavioral tracking, while Panel B reveals how much the top twenty firms that patented in technology related to consumer privacy, engaged with the different technologies (e.g. consumer tracking versus annonymization technologies). 

#### [Figure 5. Long-Term Trends and Firm Concentration in Privacy Patenting (1999–2021)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md#appendix-c-example-of-research-enabled-by-llm-data-pipeline)


| [Panel A: Annual Patents by Topic Group](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Top 20 Privacy Patenting Firms](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 5 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig8a_raw_counts.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 5 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig9_top_firms.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |

As a way of directly understanding how much the firm level trajectory of innovation shifted following these policies, we estimate dynamic event-study regressions relative to 2015. We report the results for two sub-classes of privacy patents which saw a drastic divergence in patenting behaviour coinciding with this shift in policy debate, across subslasses with different levels of topic-policy relevance. 

#### [Figure 6. Annual Event-Study Estimates of Patenting Probability by Topic Relevance Quartile](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md#appendix-c-example-of-research-enabled-by-llm-data-pipeline)


| [Panel A: Anonymizing / Decorrelating Data](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [Panel B: Tracking User Activity](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
| :---: | :---: |
| [![Figure 6 Panel A](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig6_panel_a_anonymizing.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) | [![Figure 6 Panel B](P%20-%20Paper,%20Writing%20and%20Output/figures/fig_app_c_fig6_panel_b_tracking.png)](P%20-%20Paper,%20Writing%20and%20Output/P1.%20Org%20Sci%20Proposal%20%5BMiric,%20Roh%20and%20Jia%5D%5BGithub%20Version%5D.md) |
