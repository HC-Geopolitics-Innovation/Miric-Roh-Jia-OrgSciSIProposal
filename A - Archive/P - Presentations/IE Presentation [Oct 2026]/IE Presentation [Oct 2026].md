# How LLMs and Agents Change Research Pipelines and the Classroom

**Event:** IE University  
**Date:** October 8, 2026  
**Speaker:** Milan Miric (University of Southern California, Marshall School of Business)

---

## Slide 1: Title Slide
- **Title:** How LLMs and Agents Change Research Pipelines and the Classroom
- **Event & Date:** IE University — October 8, 2026
- **Presenter:** Milan Miric (USC Marshall School of Business)

---

## Section: Motivation

### Slide 2: Motivation
- **Textual Data in Research:** Text (10-Ks, hearings, transcripts) provides rich empirical signal for research questions that were previously difficult to measure.
- **The Data Bottleneck:** Existing methods (topic models, embeddings) require short documents and break down with long, noisy, boilerplate-heavy text.
- **Need for Control:** Unassisted, end-to-end LLM processing lacks auditability, transparency, and verifiable statistical guarantees.
- **Our Approach:** Build structured, modular AI pipelines. Use LLM to solve key bottlenecks (LLM text distillation) while using established econometric and empirical standards.

### Slide 3: What LLMs Do
- **Two Core Strengths of LLMs:**
  - *Synthesizing text:* Converting long, unstructured text into concise, informative summaries.
  - *Generating code:* Writing structured instructions that can be systematically tested and audited.
- **Complementary Deployment:** Use LLMs at discrete bottlenecks where they excel, while retaining explicit control over data structures and validation.
- **Transparency & Replication:** Preserving intermediate chunks, prompts, and verification logs enables systematic replication. You can look and audit the code yourselves.

### Slide 4: An Example: Privacy Regulation and Firm Innovation
- **Substantive Question:** How do government debates on consumer privacy regulation influence corporate strategy and innovation?
- **The Empirical Challenge:** Policy deliberations are diffuse across hundreds of hearing pages, while corporate responses are embedded in 10-K filings. Information is there, but Noise > Signal.
- **Three-Stage Solution:**
  - *Step 1:* Summarize multi-hour Congressional hearings into dense policy summaries.
  - *Step 2:* Extract debated topics and directional member/witness stances.
  - *Step 3:* Connect hearing topics to S&P 500 10-K Item 1 business disclosures.

---

## Section: Part A — Engineering the AI-Enabled Research Pipeline

### Slide 5: Part A Separator Slide
# Part A
### Engineering the AI-Enabled Research Pipeline

---

### Subsection: Step 1 — Long-Document Text Summarization

#### Slide 6: Step 1: Document Characteristics and Noise
- **Corpus Scale:** 2,352 Congressional hearings (1996–2025; House Science, Space, & Tech; Senate Commerce, Science, & Transportation).
- **Extreme Length:** Median transcript contains 36,505 words.
- **Running Example:** *Facebook, Social Media Privacy, and Data Abuse* (April 10, 2018): 243,434 words (385 PDF pages).
- **The Noise Problem:** Saturated with opening procedural preamble, committee pleasantries, and index dot leaders.

```text
Unidentified speaker: - FACEBOOK, SOCIAL MEDIA PRIVACY, AND THE USE AND ABUSE OF DATA [Senate Hearing 115-683]
[From the U.S. Government Publishing Office]
S. Hrg. 115-683
FACEBOOK, SOCIAL MEDIA PRIVACY, AND THE USE AND ABUSE OF DATA
=======================================================================
JOINT HEARING BEFORE THE COMMITTEE ON COMMERCE, SCIENCE, AND TRANSPORTATION
UNITED STATES SENATE AND THE COMMITTEE ON THE JUDICIARY UNITED STATES SENATE
ONE HUNDRED FIFTEENTH CONGRESS SECOND SESSION
APRIL 10, 2018
Serial No. J-115-40
Printed for the use of the Committee on Commerce, Science, and Transportation
[GRAPHIC NOT AVAILABLE IN TIFF FORMAT] Available online: http://www.govinfo.gov
U.S. GOVERNMENT PUBLISHING OFFICE 37-801 PDF WASHINGTON : 2019
SENATE COMMITTEE ON COMMERCE, SCIENCE, AND TRANSPORTATION
JOHN THUNE, South Dakota, Chairman
ROGER F. WICKER, Mississippi, ROY BLUNT, Missouri, MARCO RUBIO, Florida...
BILL NELSON, Florida, Ranking, MARIA CANTWELL, Washington, AMY KLOBUCHAR, Minnesota...
```

#### Slide 7: Step 1: Approach — Semantic Partitioning & Map-Reduce
- **Context Limits & Partitioning:** Long transcripts exceed token limits and span diverse topics, requiring structure-aware chunking.
- **Speaker-Turn Parsing:** Rule-based parser separates 903 speaker turns without LLM calls, preserving dialogue context.
- **Hierarchical Map-Reduce:**
  - *Map:* 55 chunks $\to$ 55 segment summaries ($\approx 150$ words each).
  - *Collapse:* 55 segment summaries $\to$ 3 condensed accounts ($\approx 200$ words each).
  - *Reduce:* 3 condensed accounts $\to$ 1 hearing summary (264 words, 359 tokens).
- **Total Calls:** 59 model calls for 243k words (evaluated on Qwen 3.5-4B).

#### Slide 8: Architecture: Map-Reduce Summarization Pipeline (Figure Slide)
- **Main Element:** `fig_summarization_mapreduce.pdf`
- **Location:** `R - Results/figures/T1 - Text Summarization/fig_summarization_mapreduce.pdf`
- *(Full-slide architectural schematic illustrating the 3-stage Map $\to$ Collapse $\to$ Reduce summarization pipeline)*

#### Slide 9: Step 1: Validation Against Independent Human Abstracts
- **Ground-Truth Benchmark:** Evaluated against 3,812 human-written C-SPAN editorial abstracts using `bge-large-en-v1.5` embeddings.
- **Discriminant Validity Test:** Cosine similarity compared across three mutually exclusive tiers:

| Comparison | Assessment Objective | Pairs | Median Sim. |
|:---|:---|---:|---:|
| **Same hearing** | Correspondence to independent human account | 351 | **0.798** |
| **Diff. hearing, shared comm.** | Baseline for recurring committee subject matter | 94,304 | **0.576** |
| **Hearings, no shared comm.** | Broad cross-congressional baseline similarity | 1,243,357 | **0.533** |

- **Top-1 Retrieval:** Correct human abstract ranked #1 among all 3,812 candidates for **61.3%** of hearings.

#### Slide 10: Step 1: Similarity Distribution (Figure Slide)
- **Main Element:** `cosine_similarity_averages.pdf`
- **Location:** `R - Results/figures/T1 - Text Summarization/cosine_similarity_averages.pdf`
- *(Figure 1: Boxplots showing cosine similarity for Same Hearing [0.798] vs. Same Committee [0.576] vs. Different Committee [0.533])*

#### Slide 11: Step 1: Three-Tier Research Outputs
- **Traceable Asset Generation:** Releasing all intermediate stages for auditability:

| Output Tier | Content | Research Utility |
|:---|:---|:---|
| **Parsed Records** | Cleaned turns, speaker labels, and chunk bounds | Trace raw text; inspect turn boundaries |
| **Segment Summaries** | Intermediate outputs before final synthesis | Identify if details were lost in mapping |
| **Hearing Summary Table** | 2,352 hearing rows with metadata and runtime | Extract topics; compare accounts at scale |

---

### Subsection: Step 2 — Topic Extraction and Stance Analysis

#### Slide 12: Step 2: Two-Track Topic and Stance Extraction
- **Beyond Bag-of-Words:** LLMs identify semantic concepts directly from dialogue without LDA topic mixing or vocabulary thresholds.

- **Track 1 (Hearing Subjects):** Model extracts up to 5 neutral policy phrases per summary (*"Facebook data privacy"*, *"Honest Ads Act"*, *"GDPR-style controls"*).

- **Track 2 (Legislator Stances):** Cleans 507 legislator speaking turns (1,696 sentences); extracts neutral topic, stance (`support` vs. `concern`), and sentence citations.

- **Evidence Linking:** Links statements directly to numbered sentence citations for transparent human review.

#### Slide 13: Pipeline: Member Turn Topic & Stance Extraction (Figure Slide)
- **Main Element:** `fig_topic_extraction.pdf`
- **Location:** `R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_topic_extraction.pdf`
- *(Full-slide schematic of member-turn parsing, promptbook extraction, stance parsing, and codebook freezing)*

<!--
#### Slide 14: Step 2: Codebook Construction (111 Topics under 14 Themes) [COMMENTED OUT]
- **Taxonomy Construction:** Embedded 8,736 distinct Track 1 phrases with bge-large-en-v1.5; clustered using average-linkage + weighted k-means across 15–150 clusters.
- **Diagnostic Criteria:** Selected 15 broad clusters and 111 frozen topics based on stability, silhouette, and cohesion.
- **Frozen Schema:** Saved as fixed JSON codebook to prevent category drift.

#### Slide 15: Figure: Clustering Diagnostics across Topic Counts [COMMENTED OUT]
- **Main Element:** fig_taxonomy_criteria.pdf
- **Location:** R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_taxonomy_criteria.pdf
-->

#### Slide 14: Step 2: Validation Against Comparative Agendas Project (CAP)
- **Benchmark Sample:** 1,697 matched hearings with official human-assigned CAP codes.

- **Phrase Correspondence:** Human-assigned CAP subtopic ranks #1 for **27.0%** of hearings.

- **Domain Alignment:** Cross-tabulation shows strong correspondence (e.g., 88.6% of NASA theme hearings align with CAP Technology domain).

#### Slide 15: Figure: CAP Category Crosswalk Heatmap (Figure Slide)
- **Main Element:** `fig_cap_crosswalk.pdf`
- **Location:** `R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_cap_crosswalk.pdf`
- *(Heatmap cross-tabulating 14 codebook themes against CAP human-coded major policy domains)*

#### Slide 16: Step 2: Longitudinal Stance Panels & Polarization
- **Corpus Totals:** 32,385 stance records across 2,352 hearings.
- **Topic-by-Congress Aggregation:** Panel measuring volume and net stance:
  $$\text{Net Stance} = \frac{\text{Support Records} - \text{Concern Records}}{\text{Support Records} + \text{Concern Records}} \in [-1, +1]$$
- **Example (Consumer Privacy in 115th Congress):** 17 hearings, 34 support, 21 concern records $\to \text{Net Stance} = +0.236$.

#### Slide 17: Figure: Congressional Attention Heatmap (Figure Slide)
- **Main Element:** `fig_stance_attention.pdf`
- **Location:** `R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_stance_attention.pdf`
- *(Longitudinal heatmap showing Congressional attention volume across the 104th–119th Congresses)*

#### Slide 18: Figure: Net Stance Polarization Heatmap (Figure Slide)
- **Main Element:** `fig_stance_net.pdf`
- **Location:** `R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_stance_net.pdf`
- *(Longitudinal heatmap showing net stance polarization across the 104th–119th Congresses)*

---

### Subsection: Step 3 — Identifying Topic Relevance and Corporate Disclosure

#### Slide 19: Step 3: Measuring Cross-Domain Topic Relevance
- **The Empirical Goal:** Connect Congressional policy topics to publicly traded firms via SEC 10-K Item 1 (Business Description) disclosures.
- **Corpus Scale:** 21,966 filings for 1,061 S&P 500 firms (6,306,793 retained sentences after boilerplate removal).
- **Two-Layer Architecture:**
  - *Layer 1 (Deterministic Embedding Rail):* Sentence-level cosine similarity to fixed topic centroids (top 5 sentences averaged).
  - *Layer 2 (LLM Sentence Tagging):* Qwen two-pass screening and confirmation of directional framing (`Opportunity`, `Threat`, `Neutral`).

#### Slide 20: Step 3: Similarity-Weighted Directional Scores
- **Mathematical Formulation:**
  - Let $w_{sk} = \max(0, \cos(\mathbf{e}_s, \mathbf{v}_k))$ be the topic similarity weight of sentence $s$.
  - Separate threat and opportunity indices (per 100 retained sentences):
    $$\operatorname{Threat}_{fkt} = \frac{100}{N_{ft}}\sum_{s\in S_{ft}}w_{sk}\,\mathbf{1}\{D_{sk}=T\}$$
    $$\operatorname{Opportunity}_{fkt} = \frac{100}{N_{ft}}\sum_{s\in S_{ft}}w_{sk}\,\mathbf{1}\{D_{sk}=O\}$$
- **Advantage:** Combines the volume of discussion with its semantic proximity to the policy topic without letting threats and opportunities cancel.

#### Slide 21: Step 3: Firm Evidence and Score Comparisons
- **Embedding Similarity (Snapshot preceding April 2018 hearing):**
  - *Facebook (78 sentences):* Raw similarity = 0.759, Standardized = 4.879 (Sentence 48: subject to privacy & data protection laws).
  - *ResMed (484 sentences):* Raw similarity = 0.770, Standardized = 2.443 (Sentence 459: laws governing privacy & medical data).
- **Unweighted vs. Similarity-Weighted Scores:**

| Firm | Unweighted Threat (%) | Weighted Threat | Unweighted Opp (%) | Weighted Opp |
|:---|---:|---:|---:|---:|
| Total System Services | 24.14% | **16.03** | 0.00% | **0.00** |
| Facebook | 19.23% | **13.65** | 0.00% | **0.00** |
| Paycom Software | 1.67% | **1.25** | 2.67% | **1.46** |
| Fidelity National Info (FIS) | 9.27% | **6.16** | 1.16% | **0.81** |

#### Slide 22: Step 3: Sentence Evidence for Directional Labels
- **Sentence-Level Audit:** Retaining original disclosure sentences behind model classifications:

| Firm | Sent. | Label | Original 10-K Disclosure Sentence |
|:---|:---|:---|:---|
| **Total System Services** | 48 | **Threat** | In many jurisdictions consumers must be notified in the event of a data breach, and such notification requirements continue to increase in scope and cost. |
| **Facebook** | 55 | **Threat** | The GDPR will include operational requirements... and will include significant penalties for non-compliance. |
| **Paycom Software** | 263 | **Opportunity** | We voluntarily obtain third-party security examinations relating to security and data privacy in accordance with SSAE No. 16... |
| **FIS** | 217 | **Opportunity** | The Company has adopted a comprehensive global privacy program to assess and manage these evolving risks... |

#### Slide 23: Figure: Privacy Measure Agreement Across Quintiles (Figure Slide)
- **Main Element:** `fig_privacy_measure_agreement.pdf`
- **Location:** `R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_measure_agreement.pdf`
- *(Agreement plot: Share of firms with LLM privacy tags rises monotonically from 0.0% in Q1 similarity to 48.6% in Q5 similarity)*

#### Slide 24: Figure: Industry-Wide Policy Exposure (Figure Slide)
- **Main Element:** `fig_relevance_industry_exposure.pdf`
- **Location:** `R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_relevance_industry_exposure.pdf`
- *(Bar chart showing average standardized topic similarity across 2-digit SIC / NAICS industry sectors)*

#### Slide 25: Figure: Longitudinal Industry Disclosure Trends (Figure Slide)
- **Main Element:** `fig_relevance_industry_trends.pdf`
- **Location:** `R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_relevance_industry_trends.pdf`
- *(Time-series plot of industry-topic disclosure relevance from 1995 to 2025)*

#### Slide 26: Figure: Leading Privacy Threat and Opportunity Ranks (Figure Slide)
- **Main Element:** `fig_privacy_llm_threat.pdf`
- **Location:** `R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_llm_threat.pdf`
- *(Bar charts displaying the top 15 firms ranked by privacy threat discussion share)*

#### Slide 27: Step 3: Empirical Assets of Topic Relevance
- **Multi-Level Panel Assets:**

| Output Tier | Content | Research Utility |
|:---|:---|:---|
| **Prepared Sentences** | 6.3M 10-K sentences with metadata | Retrieve raw text; test preprocessing |
| **Topic Vectors** | 111 representations combining text + evidence | Fixed anchor representation across years |
| **Corpus Similarity** | 2.4M filing–topic pairs with top-5 citations | Measure proximity across S&P 500 firms |
| **Weighted Panel** | Threat & Opportunity indices (894 clean filings) | Econometric panel on corporate policy exposure |

---

## Section: Part B — LLM Coding Agents for Research and PhD Teaching

### Slide 28: Part B Separator Slide
# Part B
### LLM Coding Agents for Research & PhD Teaching

---

### Slide 29: Evaluating Current Discourses on LLMs in Research
- **Can AI generate novel theory or formulate and test hypotheses?**
  - Currently, no. But this is not what we should want.
- **Can LLMs effectively synthesize literature and map a field?**
  - Valuable for orienting new entrants, but often superficial for established scholars.
- **Can AI assist in data cleaning, structuring, and synthesis?**
  - Yes, [as shown in Part A].
- **Can LLMs facilitate the execution of technical research tasks?**
  - Yes, particularly in writing and optimizing code.
  - The critical challenge shifts from syntax generation to formulating research designs and processes.

---

### Slide 30: Evolving the Data Pipeline: An Agent-Centric Approach
- **Transitioning to "Agent-First" Workflows:** Moving beyond simple chat interfaces to deploying autonomous agents to do the analytical tasks.
- **Understanding of the context:** While AI generates code, the researcher must possess a deep understanding of the codebase architecture and the overall data stack.
- **Navigating the Computational Environment:** Need to understand the packages, functionality and what the technology is doing.
- **Shifting Cognitive Load:** The responsibility of the researcher evolves from knowing syntax to architecting the analytical structure.

---

### Slide 31: Implications for Doctoral Education
- **Enhanced Reproducibility:** LLMs enable the generation of cleaner, more robust code, which the LLM can audit.
- **Rethinking Doctoral Training:**
  - Historically, methodological training emphasized the mechanics of coding.
  - Shifting focus to teaching students how to develop analytical workflows.
- **The Limitations of Traditional Replication:** While replicating prior studies remains valuable, existing approaches focus on reproducibility.
  - LLMs allow for better documentation, in-process validation, human-readable documents, and clarification of the logic.

---

### Slide 32: The Future of Research Outputs
Current fear of LLMs being able to "do research" better than people $\rightarrow$ It's already there.

- **Elevating Research Questions:** The premium shifts away from "shock arbitrage" toward important research questions.
  - Because LLMs can evaluate alternatives, the value is not the empirical contingencies. The value is the question and the data.
- **Transforming the Manuscript Format:** If empirical execution becomes easy, why retain dense, convoluted methods sections?
  - We may transition toward methods sections functioning as high-level executive summaries, with the granular methodology dynamically documented and accessible in public repositories.

---

### Slide 33: Concluding Thoughts on Research Pipelines
- **LLMs as Implementation Engines:** They are exceptionally powerful tools for executing complex research designs.
- **The Era of Agents:** The debate has moved past simple chatbots; autonomous agents are already transforming commercial software development and will similarly impact academic research.
- **Iterative Refinement:** The value lies in using LLMs to continuously check, refine, and adapt code across diverse empirical scenarios.

---

### Slide 34: Concluding Thoughts on Institutional Shifts
**The Real Existential Question:**  
While many worry that AI will devalue traditional research skills, the more profound disruption is institutional:
- These technologies challenge the primacy of the static, "PDF-centric" publication model.
- The critical question is determining how to attribute intellectual credit, manage the peer review process, and document scientific knowledge in a dynamic landscape.

---

## Section: Part C — LLM Coding Agents for Teaching

### Slide 35: Part C Separator Slide
# Part C
### LLM Coding Agents for Teaching

---

### Slide 36: LLM Coding Agents and the Future of Teaching
- **Productivity & Adoption:** This is an undeniably positive shift that increases productivity; everyone should learn and adopt these tools.
- **The Wrong Focus:** The discourse is often fixated on the wrong things (theorizing, long-form writing, etc. were just testing proxies).
- **Two Core University Functions:** Universities perform two intertwined roles: **Teaching/Knowledge** and **Evaluation**.
  - We were never exceptionally good at evaluation, but knowledge and evaluation were historically highly correlated.
  - Difficult exams with trick questions or elaborate essays meant students had to master knowledge to succeed.
- **Diminishing Correlation:** LLMs make learning easier, but make evaluating learning with traditional methods far harder.
- **The Real Disruption:** Don't worry about direct teaching decline undermining universities; worry about employers and companies performing evaluation directly.

---

### Slide 37: Potential Solutions: Real Problem-Solving
- **Evaluation Through Building:** Test by building and solving real problems rather than evaluation through repetition or trick questions. Building with LLMs enables students to accomplish far more than ever before.
- **Current Misalignment:** Those who could benefit most from AI often avoid it, while others overuse tokens prognosticating hype.
- **A Practical Experiment:** Rather than managing central token licenses, give staff and students \$20/month for their own agent models to use across personal and professional tasks to gain genuine proficiency.
- **Focus on Immediate Problems:** Those who solve immediate, concrete problems with these tools consistently outperform those chasing grandiose theoretical claims.

---

## Slide 38: Closing Slide
# Thank You!
