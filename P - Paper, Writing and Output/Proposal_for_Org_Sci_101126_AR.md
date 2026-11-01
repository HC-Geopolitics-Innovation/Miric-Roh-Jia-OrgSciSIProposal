# Opening the Black Box of Large Language Models in Text-based Measurement: Staged Pipelines with Verifiable Checkpoints

## Detailed Overview of Proposal and Methodology

**Milan Miric, Albert Roh, Nan Jia**  
*University of Southern California, Marshall School of Business*  

**Proposal for Special Issue:** AI-Enabled Frontiers in Organizational Science (*Organization Science*)  

**Repository:** [https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis](https://github.com/HC-Geopolitics-Innovation/LLM-Text-Analysis-and-Synthesis)  

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?](#2-why-an-ai-enabled-data-pipeline-vs-allowing-an-llm-to-handle-the-entire-task)
- [3. Step #1: Long-Document Text Summarization](#3-step-1-long-document-text-summarization)
    - [3.1. How Text Summarization Works: Data Preparation and Key Inputs](#31-how-text-summarization-works-data-preparation-and-key-inputs)
    - [3.2. Application: Congressional Hearing Transcripts](#32-application-congressional-hearing-transcripts)
    - [3.3. Research Outputs](#33-research-outputs)
- [4. Step #2: Extracting Relevant Information from Textual Documents](#4-step-2-extracting-relevant-information-from-textual-documents)
    - [4.1. How Topic Extraction Works](#41-how-topic-extraction-works)
    - [4.2. Application: Topic Extraction and Stance Analysis in Congressional Hearings](#42-application-topic-extraction-and-stance-analysis-in-congressional-hearings)
    - [4.3. Research Outputs](#43-research-outputs)
- [5. Step #3: Identifying Topic Relevance and Corporate Disclosure](#5-step-3-identifying-topic-relevance-and-corporate-disclosure)
    - [5.1. How Topic Relevance Works](#51-how-topic-relevance-works)
    - [5.2. Application: Hearing Topics and S&P 500 10-K Item 1 Disclosures](#52-application-hearing-topics-and-sp-500-10-k-item-1-disclosures)
    - [5.3. Research Outputs](#53-research-outputs)
- [6. Toy Example: Empirical Strategy and Analyses](#6-toy-example-empirical-strategy-and-analyses)
    - [6.1. Unit of Analysis and Variables](#61-unit-of-analysis-and-variables)
    - [6.2. Specification](#62-specification)
    - [6.3. Why the Firm-Year and Not the Firm-Hearing](#63-why-the-firm-year-and-not-the-firm-hearing)
    - [6.4. Conditions for Interpretation](#64-conditions-for-interpretation)
- [7. Research Outputs, Reproducibility, and Application to Future Research](#7-research-outputs-reproducibility-and-application-to-future-research)

- [Appendix A. Prompts](#appendix-a-prompts)
    - [Appendix A.1. Text Summarization Prompts](#appendix-a1-text-summarization-prompts)
    - [Appendix A.2. Topic Extraction Prompts](#appendix-a2-topic-extraction-prompts)
    - [Appendix A.3. Codebook Drafting Prompt](#appendix-a3-codebook-drafting-prompt)
    - [Appendix A.4. Topic Relevance Prompts](#appendix-a4-topic-relevance-prompts)
- [Appendix B. Primary-Topic Tie Breaking](#appendix-b-primary-topic-tie-breaking)

---

## 1. Introduction

Textual data has provided a rich resource for researchers to answer a wide variety of questions that were otherwise difficult to measure. Prior to advances in textual analysis, researchers relied heavily on structured datasets such as the USPTO patent database, Compustat, or other structured financial datasets. However, the availability of large-scale textual data from documents such as 10-K financial statements, patent abstracts, or corporate websites (xxx; xxx) has opened new avenues for research. Data availability is an important enabler of research advancement (xxx; xxx), and empirical approaches that utilize textual data—such as topic modeling, text embeddings to compute textual distance, or text classification (xxx)—have enabled the investigation of new questions.

One critical limitation, however, is that while textual data is abundant, much of it faces an important constraint: approaches such as topic modeling or embedding construction typically require text documents of comparable length (ideally relatively short) with a high share of informative content (meaningful statements) relative to noise (boilerplate or generic statements). This constraint limits researchers’ ability to leverage many rich data sources and introduces noise into downstream empirical measures.

Large language models (LLMs) have emerged as extremely powerful tools capable of performing many tasks previously handled by earlier computational models. There are continuous attempts to use them for theorizing (xxx), testing assumptions (xxx), performing classification (xxx), and clustering data (xxx). Yet, while we have established research practices and validation standards for traditional methodologies, LLMs often operate as opaque black boxes that, while capable of producing useful outputs, can obscure how specific decisions are made. Fundamentally, these models possess two core strengths:

1. **Synthesizing text** (generating readable, coherent text based on existing documents); and
2. **Generating code** (producing machine-readable instructions that can be systematically executed and tested).

Rather than abandoning research practices for which we have established routines, validation standards, and verifiable properties in the hope that LLMs will outperform them end-to-end, we propose a methodology that combines the complementary strengths of existing research practices (interpretability, confidence in understanding their underlying properties, and grounding in established corpuses of knowledge) with the strengths of Large Language Models (distilling information and generating structured textual documents).

The proposed project makes three contributions:

1. **Generative AI as a Tool for Information Extraction and Synthesis.** Many existing text analysis methodologies (e.g., topic modeling, text classification, semantic distance) break down when applied to raw documents that are long (or of differing lengths), contextually idiosyncratic, or dilute in signal. Examples include congressional testimony, earnings call transcripts, or corporate websites. In these settings, key information is embedded within generic, formulaic text. Traditional approaches have attempted to address this issue by upweighting informative words and downweighting generic words (e.g., TF-IDF weighting), but these methods do not fully resolve the underlying signal-to-noise problem. Similarly, text embeddings provide a representation of semantic similarity across words, overcoming limitations of word co-occurrence, but cannot readily distinguish informative content from formulaic boilerplate. This noise propagates into downstream measures such as topic models, language distance, or classifiers, obfuscating meaningful variation. We propose that using LLMs to take long, convoluted documents (e.g., 10-Ks, corporate websites, or congressional testimony) and convert them into concise, information-rich text summaries (analogous to patent abstracts) can substantially improve the performance of subsequent text analysis methods and enable structured information extraction.
2. **Demonstration of Information-Rich Textual Summaries on Substantive Research Questions.** Next, we demonstrate how using LLM-generated, information-rich summaries allows us to identify relationships in textual data that were previously difficult to capture. We use consumer data privacy as a running application for linking policy discussions to firms’ disclosed activities. A fundamental policy issue for technology regulators, firm non-market strategy, and intellectual property scholars is the relationship between government regulation and innovation outcomes. An example is consumer privacy regulation, where policymakers increasingly scrutinize consumer data protection, but linking these debates to corporate innovation has remained challenging. Prior work has examined specific contexts such as mobile app markets following GDPR where direct impacts could be measured; however, scalable empirical methods to identify which firms across the broader economy are affected by evolving policy debates remain scarce. The present application constructs topic-based links and disclosure measures. Studying whether firms adjust their innovation strategies in response would require additional outcome data and a research design identifying those responses.
3. **Reproducible AI-Driven Pipelines for Empirical Research.** We document the code, prompts, source evidence, and intermediate outputs needed to inspect and adapt the procedure. This addresses both the difficulty of extracting reliable information from text and the cost and learning curve of adopting computational methods. Section 6 explains the available research assets, their reuse, and the work that remains.

The empirical workflow has three steps: summarizing long documents (Section 3), extracting topics and attributed positions (Section 4), and connecting those topics to firm disclosures (Section 5). Each section distinguishes the general method, its implementation in the running application, and the resulting research outputs.

---

## 2. Why an AI-Enabled Data Pipeline vs. Allowing an LLM to Handle the Entire Task?

One question that inevitably emerges is why researchers should develop a structured, LLM-enabled pipeline rather than simply prompting a commercial LLM to process entire context windows and execute the entire task end-to-end. Furthermore, while existing models encounter limitations, future frontier models will continue to advance.

There are two critical reasons for designing an explicit data pipeline:

- **Transparency and Control:** Concerns regarding LLM model transparency, reliability, and stability typically arise when researchers cede full autonomy to a model and ask it to arrive at an unassisted solution. By contrast, our approach uses the LLM in targeted roles: to write code, execute specific processing steps, or summarize discrete textual segments based on defined source documents. By developing an AI-enabled data pipeline, we overcome specific bottlenecks in existing research workflows rather than re-engineering parts of the research process where unconstrained LLM execution lacks control and statistical guarantees.
- **Auditability and Systematic Replication:** While LLMs can formulate reasoning internally, their outputs often depend heavily on subtle nuances in prompt formulation, model versioning, and temperature settings. By carefully engineering a structured research pipeline, researchers can leverage LLMs at discrete intermediate steps while fully documenting every phase of the process at scale. This modular approach provides a degree of oversight, reproducibility, and methodological transparency that would otherwise be impossible.

---

## 3. Step #1: Long-Document Text Summarization

Text summarization involves taking long, noisy, and complex textual data and using a large language model to create a concise, information-rich summary that can be utilized in subsequent research tasks. 

While off-the-shelf models can easily generate summaries of uploaded documents, systematically and reliably summarizing large corpora into consistent, representative summaries requires carefully engineering the summarization pipeline to overcome two technical challenges:

1. **Context Limits and Computational Efficiency**: Although modern models feature expanding context windows, these limits are still encountered with lengthy documents (which are precisely those requiring summarization), particularly when deploying economical, open-weight, or local models. To address this, the researcher must either implement a procedure for carefully partitioning and sequencing data through the model, or rely on opaque, automated chunking.
2. **Heterogeneous Topical Sections**: Within long textual documents, different sections address distinct topics. In order for the summarization procedure to be reliable, these textual components must be partitioned such that the input provided to the LLM is as coherent as possible. Even when a full document fits within a model's context window, pre-cleaning and structured partitioning yield significant improvements in summary fidelity and clarity.

Carefully designing and partitioning this process ensures that data extraction remains reliable, transparent, and reproducible regardless of underlying model advances.

### 3.1. How Text Summarization Works: Data Preparation and Key Inputs

The pipeline involves four decisions:

1. **Document Structure and Semantic Partitioning.** Researchers must first analyze the dataset structure to determine how documents should be split into smaller chunks for individual processing. The research question determines whether the final summary to capture broad document themes, particular arguments, or statements attributed to individual actors. Next step is to decide chunking strategy. First, *context-aware chunking* uses meaningful units already present in the source, such as a document section or a speaker's uninterrupted contribution. When these units cannot be identified, *recursive structure-aware splitting* can use structure of the text such as paragraphs and sentences. If none of above are available, the last option is chunking based on a fixed-size (character) sliding window that provides a simpler fallback but can divide an argument or separate it from its speaker. Units are then grouped into model inputs within a chosen context window, leaving room for instructions and generated text. 
2. **Choose how to summarize and combine the inputs.** There are two standard ways to summarize long text documents: 
    
    a. In *Map-Reduce* method, individual text chunks are first summarized in *map* stage, and these segment-level summaries are subsequently aggregated into a comprehensive document summary at *reduce* stage. If independent segment summaries are too long to combine in one call at *reduce* stage, intermediate *collapse* steps shorten groups of outputs from *map* stage first. Separate prompts distinguish reading source text from combining existing summaries. This method can be parallely processed at scale, but can loose context across chunks.

    b. In *Refine* method, the model updates a running summary as successive chunks arrive. This can maintain continuity, but requires sequential processing and can carry earlier errors into later updates. 

    The suitability of both approaches depends on the document and the intended output.

3. **Model Selection and Validation.** Outcomes depend on the choice of model, prompt design, and aggregation rules. Researchers must evaluate alternative models, preprocessing heuristics, and aggregation techniques during an initial prototyping and validation stage to ensure the pipeline yields consistent, high-fidelity results.
4. **Corpus Deployment and Artifact Storage.** The finalized model pipeline is deployed across the entire dataset. Data from each intermediate stage—cleaned source segments, intermediate chunk summaries, and aggregated outputs—are documented and archived. This ensures full traceability, allowing researchers to inspect intermediate components or re-run specific transformations with alternative models.

### 3.2. Application: Congressional Hearing Transcripts

Our goal of demonstration is to show how regulatory concerns affects firms' XXX(Financial Performance). Congressional hearings provide an ideal application for capturing regulatory concerns and at the same time to demonstrate text summarization. These transcripts document extensive deliberations among policymakers and invited witnesses (including scientists, corporate executives, and industry stakeholders).

These transcripts capture critical policy deliberations utilized across various research settings (xxx; xxx; xxx). However, they are typically long and saturated with procedural preamble and formulaic pleasantries that dilute the substantive debate. Extracting the core arguments into a usable dataset for variable construction requires a structured pipeline:

In this section, we apply text summarization procedure to 2,352 hearings from the House Committee on Science, Space, and Technology and the Senate Committee on Commerce, Science, and Transportation with usable digitized transcripts on GovInfo, covering 1996–2025. The median transcript contains 36,505 words. The documents contain introductory material and participant lists, followed by opening statements, witness testimony, exchanges between legislators and witnesses, and material inserted into the record.

These hearings provide records of policy discussions involving legislators, scientists, corporate executives, and other witnesses. Our research question needs the particular practices and proposals discussed, together with who expressed a position on them, so we can capture legislators' regulatory concerns alongside the hearing's overall themes. A title or opening statement can identify the announced subject but cannot supply those details from later exchanges. Procedural recognitions and repeated courtesies also occupy space without contributing equivalent substantive information. We therefore process the retained hearing record in sequence and ask the model to distinguish substantive discussion from procedural segments.

To further concretely show exact step of process, we use *Facebook, Social Media Privacy, and the Use and Abuse of Data* (`CHRG-115shrg37801`), featuring Mark Zuckerberg's testimony on April 10, 2018, as a running example. This joint hearing of the Senate Judiciary and Commerce committees examined Facebook's handling of user data following the Cambridge Analytica revelations. Its stored text contains 243,434 words (385 page in PDF document), including written material appended to the hearing record. The linked [worked example](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/README.md>) provides the source, parsed records, exact model inputs, and recorded outputs. It illustrates the intermediate collapse stage and includes a matched C-SPAN abstract.

**1. Parse the transcript into speaker records.** We downloaded the hearing transcript and its accompanying MODS metadata through GovInfo's API, then extracted the fixed-width text from the transcript's HTML wrapper. Our goal is to capture the hearing's overall themes while identifying the regulatory concerns voiced by legislators to capture regulatory concerns in subsequent steps. This requires distinguishing legislators' contributions from witness testimony and retaining the exchanges that give those contributions context. We therefore treat the *speaker turn* as the basic unit to preserve.

The downloaded text does not provide separate, labeled records for each turn. We recover this structure from a recurring formatting pattern: paragraphs begin with at least four spaces, and speaking turns open with a title and surname, such as `Chairman Grassley.` or `Mr. Zuckerberg.` in this hearing. Python reconstructs paragraphs from the indentation and starts a new speaker record at each recognized opening; subsequent paragraphs remain in that record until another opening appears. The MODS metadata supplies participants list, allowing us to match detected surnames to legislators and attach their Bioguide identifiers where available. Thus, Grassley's record receives a legislator identifier, while Zuckerberg's retains his transcript label without a legislator identifier. The [parsed examples](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/README.md#1-from-source-text-to-turn-records>) show these fields and link the text-processing rules, which require no LLM calls.

To focus the summarization input on discussion, we remove paragraphs containing dot leaders, which generally mark contents or index entries, and exclude records that the parser flags as written questions for the record (`qfr`). We also remove page markers and standardize whitespace. Text before the first recognized speaker remains in an unattributed record. For transcripts without consistent indentation, the parser uses blank lines to reconstruct paragraphs; the linked worked example documents this fallback.

For the Facebook hearing, the [source text](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/source.txt>) yields 8,192 paragraphs. Removing 40 dot-leader paragraphs and grouping the remainder produces [903 speaker records](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/parsed_turns.json>), containing the attributed speaker, member identifier where available, section label, and text in transcript order. These are the records passed to the next step. The output also reveals a limitation: the parser flags none as `qfr`, although the appendix contains written responses. Those responses remain attached to Grassley's final record and enter summarization. Consequently, the example summarizes the retained hearing record, including appended material; those appended responses cannot be treated as Grassley's own statements.

> **Coauthor note — appendix material in the last speaker's record.** Including the closing appendix in the last speaker's record is a parser error, not an intended feature. Submitted statements and written answers are not speech and should have been removed at parsing, before summarization; the question-for-the-record flag did not detect them. The summaries were produced with the appendix still attached to the last record, so the parser needs a fix that detects the appendix, and the affected hearings need to be identified and their summaries re-run before the results are final. The cleaning rule in Section 4 removes the appendix before stance extraction, so Track 2 is unaffected.

**2. Group consecutive speaking turns into model inputs.** Preserving speaker turns prevents a contribution from being divided arbitrarily, but summarizing at the level of speaker turn separately would introduce another problem from map-reduce approach: a answer could be detached from the question that explains it. Because the map stage summarizes each input independently, later aggregation cannot reliably restore context omitted from those summaries. We therefore group neighboring turns into larger inputs, keeping turns intact wherever possible and retaining their order, so the model can interpret several contributions as part of the same discussion.

We select a 6,144-token input window for transcript text, leaving additional space for instructions and generated text and at the same time can be applied to the four models we selected (`Qwen/Qwen3.5-4B`, `meta-llama/Llama-3.2-3B-Instruct`, `google/gemma-4-E4B-it`, and `meta-llama/Llama-3.1-8B-Instruct`) without exceeding the context window of the models. This choice lets each call process several neighboring contributions while keeping input length manageable and reducing the number of calls relative to summarizing each turn separately. Python adds the speaker labels and combines as many complete, consecutive turns as fit, measuring length with the summarization model's tokenizer. When the next turn would exceed the window, it starts a new chunk. The [chunking function](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Background Helper Functions/chunking.py>) records the resulting lengths and any split turns.

The running example produces [55 chunks](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/Chunks/chunks.md>). The first contains nine records and 5,881 tokens, including introductory text and opening remarks. The [second chunk](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/Chunks/chunks_01-10.md#chunk-02>) contains nine records and 5,898 tokens, including Zuckerberg's opening statement and exchanges with Grassley. For example, Grassley asks whether Facebook has required audits to confirm deletion of improperly transferred data; Zuckerberg responds that it has, but he does not have the exact count. Keeping these turns together gives the model both the action being questioned and the context needed to interpret the reply.

This grouping preserves local discussion context where exchanges fit together, but boundaries are determined by length, so a question and answer can still fall in different chunks. A turn that exceeds the window on its own must also be divided: the code first uses paragraph boundaries, then token boundaries if a single paragraph is too long. In this example, chunks 8–14 divide a long record labeled Grassley that contains submitted letters and statements. The saved inputs make these exceptions visible; preserving the speaking turn is the guiding rule, with splitting used when necessary to fit the selected input window.

**3. Summarize each chunk.** We used `Qwen/Qwen3.5-4B` in bfloat16 precision as a primary model for production. Before deployment, the [model-comparison notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/02_model_comparison.ipynb>) ran four models on the same five hearings, selected near the 10th, 30th, 50th, 70th, and 90th percentiles of transcript length. It recorded processing time, call counts, summary lengths, and speaker-name retention. These measurements made the resource requirements of short and long hearings observable before scaling to the corpus. The notebook profiles feasibility and output characteristics; it does not establish which model produces the most accurate summaries. By manually checking small set of summaries, researchers can manually choose the best performing model.

After the LLM is chosen, each chunk enters a separate model call. In our example, the [map prompt](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/README.md#map-prompt>) requests about 150 words describing the subjects discussed, positions attributed to named speakers, and numbers and legislation copied from the input. These fields carry information needed to distinguish particular policies and speakers in later analysis. For a purely procedural or ceremonial segment, the prompt requests one sentence, reducing its representation without requiring the model to invent a substantive account. These are instructions to the model, not checks that every requested detail survives. In the example, 55 calls produce [55 segment summaries](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#map-01>).

**4. Condense the segment summaries when necessary.** Our next goal is to bring the segment summaries together so the model can produce one account of the hearing as a whole. For long hearings, however, even these shorter summaries can collectively exceed the selected 6,144-token input window. We therefore introduce an intermediate condensation step that produces a shorter account of each successive portion of the hearing. Hearings whose segment summaries already fit proceed directly to the final synthesis.

Python checks the combined length of the summaries in transcript order. When they are too long, it groups consecutive summaries by token count and asks the model to condense each group. The [collapse prompt](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/README.md#collapse-prompt>) identifies the input as existing summaries and requests an account of about 200 words retaining named speakers, their positions, numbers, and legislation. Because each group covers only part of the hearing, the prompt explicitly instructs the model not to draw a conclusion about the hearing as a whole. Python then checks the combined length of the condensed accounts and repeats the process if needed, allowing up to eight condensation rounds.

In the Facebook example, the 55 segment summaries are too long to enter the final synthesis together. The procedure groups summaries 1–23, 24–45, and 46–55 and produces [three condensed accounts](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#collapse-01>). These fit together within the selected input window, so one condensation round is sufficient. The final call can then consider the three accounts together to synthesize the hearing. Each additional condensation can omit details; we therefore retain both the original segment summaries and the intermediate accounts so readers can inspect what information survives.

**5. Produce the hearing-level summary.** In the reduce stage, the model receives the segment summaries, or their condensed versions, in transcript order in a single call. The [reduce prompt](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/README.md#reduce-prompt>) requests a 200–250-word account covering the hearing's purpose, main subjects, speakers' positions, disagreements, and key numbers and legislation. It instructs the model to omit details that the supplied summaries do not establish.

The word range is a prompt target. In our example, the generation is capped at 512 tokens, measured with the summarization model's tokenizer. This keeps the output short for downstream text analysis and compatible with BERT-based models (i.e., BERTopic). Since token counts differ across models, compatibility is checked separately using the downstream model's tokenizer in the evaluation below. When generation reaches the cap, the pipeline attempts to remove an incomplete final sentence.

For the Facebook hearing, the [final summary](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#final-summary>) contains 264 words and 359 tokens. The complete sequence is **55 transcript chunks → 55 segment summaries → three condensed accounts → one hearing summary**, requiring 59 model calls. The example export reconstructs the inputs and verifies all 59 user-prompt hashes against the production log. The displayed summaries are the saved outputs from that run.

**6. Apply the procedure to the corpus.** Once a few examples have been reviewed and the resulting summaries meet the study's needs for content and quality, the next step is to scale the procedure to the full corpus. In our application, the [production notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/03_summarize_sst.ipynb>) divides the sample into ten disjoint batches and saves results after each hearing. The [assembly notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/04_assemble_summaries.ipynb>) combines the results and checks coverage, duplicates, failures, and summary lengths.

The completed run produced 2,352 successful hearing summaries from 26,722 chunks and 29,264 model calls. The median hearing required 11 chunks. Most hearings—2,259—proceeded directly from map to reduce; 93 required one collapse round. Final summaries had a median length of 396 tokens. Recorded per-hearing processing time summed to 112.7 hours across the ten batches.

**7. Validate the summaries against independent human-written abstracts.** Once summaries have been produced at scale, we need to assess whether they capture the hearings' substantive content. Fluent text alone is insufficient: a generated summary can omit central points or introduce claims unsupported by the transcript. Traditional measures such as ROUGE compare overlapping words or sequences with human reference summaries. Such overlap provides useful information, but does not by itself establish whether a summary preserves meaning or is faithful to its source. We therefore use independent human-written accounts as references and assess correspondence in meaning, allowing for differences in wording.

Comprehensive human-written summaries are not available for every hearing in our corpus. C-SPAN's editorial abstracts provide an available reference for hearings it broadcasts, but they are typically much shorter than our generated summaries and cover only the subject and selected points. This difference in scope limits what a direct comparison can establish: a detail absent from the abstract may still be supported by the transcript. An isolated similarity score also cannot show whether the resemblance reflects the particular hearing or vocabulary common to many policy discussions. We therefore ask whether a generated summary resembles the human-written abstract of its own hearing more closely than abstracts of other hearings, including those addressing related committee concerns.

We matched hearings to C-SPAN programs using date and chamber, title similarity, and witness names. This matching does not use the generated summaries' semantic similarity to the abstracts. Of the 2,352 hearings, 351 had a matched abstract. In the running example, the [generated summary and C-SPAN abstract](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#final-summary>) both identify Zuckerberg, Facebook's handling of user data, and Cambridge Analytica; the generated account includes additional subjects and details that the short abstract cannot independently verify.

We embedded the 351 generated summaries and a broader reference pool of 3,812 matched C-SPAN abstracts using `BAAI/bge-large-en-v1.5`, then calculated cosine similarity for every summary–abstract pair. Higher scores indicate closer representations of meaning in the embedding space. The [evaluation notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/05_evaluate_quality.ipynb>) checks lengths using the encoder's tokenizer and reports no truncation in either set. We divide the pairs into three mutually exclusive groups to assess what the similarity captures:

| Comparison | What the comparison helps assess | Pairs | Median similarity |
|---|---|---:|---:|
| Same hearing | Correspondence between the generated summary and an independent human account of the same event. | 351 | 0.798 |
| Different hearing, at least one shared committee identifier | A comparison for recurring committee subject matter: a generic account of a committee's concerns could resemble many of its hearings. | 94,304 | 0.576 |
| Hearings with no shared committee identifier | A broader comparison across congressional subjects, showing how much similarity remains outside shared committee membership. | 1,243,357 | 0.533 |

Figure 1 shows the distributions and their overlap. The higher median for the correct hearing, including relative to other hearings sharing a committee, supports the interpretation that the summaries retain information specific to the event beyond recurring committee subject matter. The comparison across committees provides a broader reference, although hearings from different committees can still discuss related topics. This design gives the same-hearing similarity a basis for interpretation without requiring the generated summary and editorial abstract to cover identical details.

Group medians can conceal weak matches for individual hearings. We therefore also ask whether each generated summary identifies its own abstract as the closest among all 3,812 candidates. The correct abstract ranked first for 215 of the 351 hearings (61.3 percent). Together, these checks provide evidence of hearing-specific content in the evaluated summaries. They do not establish the absence of hallucinations, the accuracy of every attribution or number, or complete coverage of the hearing. Those aspects require direct review against the source transcript; the paired texts and intermediate outputs make such review possible.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T1%20-%20Text%20Summarization/cosine_similarity_averages.png" alt="Figure 1. Similarity between generated hearing summaries and C-SPAN abstracts"></p>

*Figure 1. Cosine similarity for the same hearing, different hearings sharing a committee, and hearings sharing no committee identifier. The vertical axis measures similarity; each observation is one summary–abstract pair. Boxes contain the middle 50 percent of scores, and the line within each box marks the median. Whiskers extend to the most extreme scores no more than 1.5 times that range beyond the box; more distant observations are hidden. The comparison uses 351 generated summaries and 3,812 C-SPAN abstracts.*

### 3.3. Research Outputs

The outputs support both subsequent text analysis and inspection of how the final accounts were produced. They retain three levels of information:

| Output | What it contains | Research use |
|---|---|---|
| Parsed source records and reconstructed inputs | Speaker labels and retained text, plus the rules and tokenizer needed to reproduce each input chunk. | Retrieve the language underlying a summary and inspect attribution, exclusions, or chunk boundaries. |
| Segment and collapse summaries | The recorded outputs before final synthesis, identified by their stage and order. | Locate whether a detail disappeared when source text was first summarized or during later condensation. |
| Hearing-level summary table | One row for each of the 2,352 hearings, containing the final summary and identifying and run metadata. | Extract hearing subjects as in Section 4 and compare short accounts across hearings. |

For the running example, the [input chunks](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/Chunks/chunks.md>) and [recorded summaries](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md>) let a reader follow a passage through these levels. The hearing-level table includes model and prompt versions, chunk and call counts, collapse rounds, processing time, and summary length, so the amount of processing is visible alongside the resulting text.

Separate call logs retain the stage, position, user-prompt hash, token counts, timing, and output text for all 29,264 model calls. The corpus input chunks can be reconstructed from the retained parsed records using the tokenizer, packing rules, and selected input window, then checked against the logged hashes. The [worked example](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/README.md>) provides those inputs as readable files and includes the verification code. This record supports checking a specific transformation or revisiting it with different settings, while preserving the distinction between reproducing the saved computation and establishing the factual accuracy of its output.

---

## 4. Step #2: Extracting Relevant Information from Textual Documents

In Step #1, text summarization reduced long documents to standardized summaries. In the topic extraction step, we further reduce these high-dimensional summaries to a lower-dimensional set of topic categories. While the standardized summaries could be supplied directly to established topic modeling tools such as LDA, LLMs offer additional features that are valuable for topic extraction. Topic extraction with an LLM differs in four ways:

1. **Targeted extraction defined by the researcher**: This step shares conceptual similarities with unsupervised approaches such as LDA, where topics emerge from the data rather than from a predefined list. The difference is that the extraction is instructed. Working on the standardized summaries from Step #1, the model is told what counts as a topic for the research question and what does not, such as an organization named in passing or an entity mentioned, and it returns the central subjects of each document in order of centrality. A topic model cannot be given such instructions. Its topics are whatever word co-occurrence yields, and an incidental mention weighs the same as the central subject.

2. **Fine-grained categories within a specialized domain**: A topic model's level of detail is set by the number of topics chosen before fitting and by where the vocabulary varies most. In a general collection of documents that variation separates broad subjects, such as sports from politics; finer distinctions, such as baseball from football, require many more topics, and in a collection confined to one domain the finer topics are dominated by vocabulary that all documents share and become hard to interpret. Because the LLM names the specific subject each document discusses, the finest level of detail is the subject itself, and the named phrases can be grouped into broader categories at whatever level the research question requires while remaining readable at each level.

3. **Topics and categories defined by meaning**: In a topic model, meaning enters only when the researcher reads the output; the model itself works on word counts. With an LLM, meaning enters at two points:

    a. *What a topic is.* A topic model represents each topic as a ranked list of words that the researcher must interpret and label afterwards. The LLM returns a short phrase that actually has coherent meaning. In this case, each topic is an easily understandable unit that can be compared directly across documents.

    b. *How topics are grouped.* A topic model relates documents through word co-occurrence, so differently worded discussions of one subject are separated while generic words pull unrelated documents together. LLM-based topic extraction instead embeds the extracted phrases and clusters them on their meaning, so that two differently worded phrases about one subject enter the same category even though they share no word.

4. **Capturing within Topic Variation**: The clustered categories applied to all summaries are short labels, and a label alone cannot show how a topic is discussed. When the research question requires that variation, researchers can return to the raw text, extract the specific statements made about a topic, and attach them to the fixed categories. With the topic held fixed, the attached statements capture how its treatment varies over time and across documents.

### 4.1. How Topic Extraction Works

The pipeline runs in two tracks. Track 1 (high level) turns each document's summary into a small set of named subjects and builds the codebook of topics that all later work uses. Track 2 (granular level) returns to the raw text and attaches to those topics the specific statements made about them. Throughout, a *subject* is a phrase extracted from a document's summary, an *issue* is what a statement in the raw text is about, and a *topic* is a codebook category into which both are placed. The research question determines which tracks are needed. A document's overall subject requires only Track 1, at one call per document. If a research question requires granular details such as how a topic is treated inside documents and by whom, Track 2 is needed as well, at one call per passage of raw text. Note that Track 2 is to add resolution to Track 1 rather than replacing it, so a reader who needs only document-level subjects can stop after part a.

***a. Procedures for Track 1***

1. **Source Text.** Track 1 works on the standardized summaries from Step #1 Text Summarization, which present each document's main subjects in a short and uniform form. One call per document is enough.

2. **Extraction Design.** Based on the research question, researchers define what counts as a subject and what is excluded, and they do so *prior to* extraction. This is what separates LLM-based extraction from traditional topic modeling. Traditional topic modeling groups words by co-occurrence first and leaves the researcher to select, label, and discard topics afterwards. LLM-based extraction applies the researcher's rule to each document as a pre-filter, so only subjects that meet the rule are returned. The rule can therefore ask for narrow subjects directly, at a depth that a topic model reaches only with many topics and much post-selection. The rule is applied through the prompt, which sets a clear boundary. It can state what a subject is, such as the specific matter a document discusses rather than the field or the actor around it. It states what does not qualify, such as an actor named in passing or an item mentioned only as an example or comparison. The model then returns a short list of subjects that can be checked against the summary. Prompts are refined on a small sample before the full run.

3. **Document-level Subject Extraction.** One call per summary returns the document's central subjects as short, specific phrases. Researchers set the form of each subject, such as a phrase of a few words, and the maximum number of subjects per document, such as five. They can also ask for the subjects in order from most to least central, which later serves as a rank.

4. **Organizing Extracted Subjects into Common Categories.** Different documents name related subjects in different wording. The document-level subjects are embedded and clustered on meaning into candidate groups, and the clustering is repeated at several levels of detail so that the researcher can choose the number of groups according to the research question. These candidate groups are the input to review, not yet the codebook.

> **Coauthor note — clustering on subject wording, not on what subjects refer to.**
> - Problem: the clustering embeds each subject's wording alone. That captures paraphrase, but for a bare name such as a bill or program it rests mostly on the words in the name. The review had to drop 30 groups held together by a shared word rather than by meaning, such as the "program", "initiative", and named-Act families.
> - To do: either keep the design and state this limitation in the text, or re-cluster each subject together with context, such as the summary sentence it came from or a one-line description drafted by the model.

5. **Codebook Review and Document Classification.** An LLM can draft a label, a definition, and example phrases for each candidate group. Researchers review the groups and record decisions to keep, merge, or drop them. The result is fixed as the codebook. The document-level subjects were the input to the clustering, so each subject already belongs to one candidate group and needs no new assignment. If its group was kept, that group is the subject's category. If its group was merged, the subject moves to the merged category. If its group was dropped, the subject is left unassigned. Each document is then classified by the category that holds the most of its subjects.

6. **Validation.** Format checks establish that records are well formed, not that they are correct. Samples of records are read against their source sentences. An independent classification of the documents, where one exists, benchmarks the categories.

***b. (Optional) Procedures for Track 2***

Track 2 is needed when the research question asks how a topic is treated inside documents and by whom. It reuses Track 1's codebook and adds five procedures.

7. **Source Passages.** The raw text is prepared as passages that preserve attribution, such as a speaker's turn or a document section. Each passage is segmented into numbered sentences so that later records can cite evidence by number.

8. **Statement Extraction Design.** Researchers define what a statement record carries and which statements are excluded. For example, a record can carry the issue, the stance taken toward it, and the sentences that support it. In this procedure, the extraction does not see Track 1's subjects, so that a broad subject cannot make every sentence count as relevant. Prompts are refined on a small sample before the full run. The design fixes three judgments that the model makes in order within each passage.

    a. *Selection.* Which sentences express a statement that qualifies under the rule. All other sentences return nothing.

    b. *Issue.* What the statement is about, named as a short neutral phrase that carries no direction.

    c. *Attribute.* The additional field the record carries, such as the stance toward the issue, chosen from a closed set of labels.

    Each of these judgments is an *inference* by the model, but a narrow one. The model does not produce an issue from nothing. It selects sentences that are in front of it, names an issue those sentences contain, and chooses a label from a closed set, so each judgment is tightly anchored in the passage. Even so, a small open-weight model can misjudge any of the three, so the records must be checked by hand. This is why each record cites sentence numbers, so that any record can be traced to its source and reviewed by the researcher.

9. **Statement Extraction.** The extraction is applied to every passage and returns the specific statements made about an issue, with their supporting sentences, so that each issue carries attributed evidence.

10. **Placement into the Fixed Categories.** Within-topic statements took no part in the clustering. They are placed into the fixed categories by similarity, with a threshold below which they remain unassigned. Whether a document's statements fall in the categories Track 1 assigned to that document is then a cross-check on both tracks.

11. **Aggregation into Measures.** Aggregation turns the placed records into measures and requires three choices. The first is the counting unit. The second is the comparison period, such as a year. The third applies when records carry a direction and is a balance measure that summarizes the direction within a category, reported together with the underlying counts. The counting unit is decided by the research question, because the same records yield different measures depending on what is counted. A statement as the unit measures the volume of discussion, which suits a question about what was discussed and in what ways. An actor as the unit measures how many hold a view and who they are, which suits a question about the spread or the weight of a view. The two can differ sharply, because one actor can contribute many statements.

For both tracks, inputs, prompts, and intermediate outputs at each procedure are archived so that any measure can be traced to its source and re-run with alternative settings.

### 4.2. Application: Topic Extraction and Stance Analysis in Congressional Hearings

In our toy example, our research question is to study how regulatory concerns affect exposed firms' performance. For this, we need to capture two kinds of information: the regulatory subjects each hearing focused, which later connect hearings to firms, and the stances legislators took on particular issues of main subjects, which measure regulatory concern. We follow the eleven procedures illustrated in Section 4.1 in two tracks. *Track 1* extracts hearing-level subjects from the summaries and builds the codebook. *Track 2* then returns to the transcripts and places legislators' stances into that codebook.

We continue use the senate hearing on Facebook-Cambridge Analytica scandal as running example for demonstration of topic extraction process. The linked [topic extraction example](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/README.md>) contains the numbered inputs, exact prompts, recorded responses, category assignments, and verification code.

**Track 1. Hearing-level subjects**

**1. Select the source text.** The subject of each hearing connects hearings to understand what a given hearing was about. Using final summaries from Step #1 will be enough to identify broad subject. *Track 1* therefore takes each hearing's final summary as its input.

**2. Design the extraction and develop the prompt.** This is the procedure in which the LLM performs inference. We therefore state what the model is given and what it decides.

For *Track 1*, we extract each hearing's subjects from its summary. The LLM is given one hearing's final summary from Step #1 together with the [Track 1 prompt](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/stance.py>). It decides which subjects the summary gives substantial attention to and names each as a short neutral phrase. Without a rule, the first development rounds returned names such as an agency or a bill number as subjects. Such a name says who or which bill was discussed but not what the hearing was about, and it cannot be compared across hearings. The prompt therefore sets a screening rule for what counts as a subject. A subject is a specific policy or program, a regulation or technology, or a practice or budget item. An agency, company, or country named by itself does not count. Neither does a bare bill number or an entity mentioned only as an example or comparison. The [Track 1 parser](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/stance.py>) then checks that the output is a list of strings. It drops case-insensitive duplicates and any phrase beyond the fifth, flags directional wording, and counts each dropped item. Two judgments are left to the model. The first is whether a phrase is central to the hearing. The second is whether it names the right subject. Both are low-risk here because the input is already a standardized summary.

The prompt was fixed after two development rounds on 28 seeded summaries, which produced the screening rule above. The recorded version is `summary-topics-0.2-dev`.

**3. Extract hearing-level subjects.** We use `Qwen/Qwen3.5-4B` under the same model settings as Step #1. We send each final summary to the model once with the Track 1 prompt from step 2 ([production notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/04_track1_production.ipynb>)). For the Facebook hearing, the [saved response](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/topics.json>) is the following.

```json
["Facebook data privacy", "content moderation", "election integrity", "Honest Ads Act", "GDPR-style controls"]
```

The prompt asks for up to five phrases ordered from most to least central, and the parser keeps them with their ranks. Across all 2,352 hearings, the extraction yields 11,592 mentions and 9,095 distinct subjects after standardizing capitalization and whitespace. Hearings received 4.93 phrases on average with a standard deviation of 0.28.

**4. Cluster the subjects into candidate groups.** We group the extracted subjects into candidate groups in the following way. Procedure 3 returned 9,095 distinct subjects, and hearings on the same matter rarely yield the same wording. "Facebook data privacy" and "GDPR-style controls" both concern data privacy, yet they share no word. Comparing hearings therefore requires that subjects with similar meanings be grouped before any category is defined. Clustering performs this grouping, and each cluster becomes a candidate group for the codebook review in the next procedure. 

The [clustering notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/08_taxonomy_consensus.ipynb>) first strips years and bill numbers and trailing words such as "Act" from each phrase. "Honest Ads Act" and "Honest Ads" then become one string. It embeds the 8,736 resulting strings with `BAAI/bge-large-en-v1.5` and groups near-duplicates into 7,712 families. It then partitions the families at nine candidate counts from 15 to 150. Each partition is repeated 30 times on subsamples to see whether the groupings persist when the fitting sample changes.

We examine three properties of each partition. Stability measures how consistently members are assigned together across repetitions. Silhouette measures how well clusters are separated from their neighbors. Cohesion measures how closely member meanings align within a cluster. A reproducible group need not be well separated or coherent, so the three are reported separately and none is used as a gate. The 15-cluster partition has the highest stability and silhouette of all counts. Among the finer partitions, the 150-cluster partition has the highest stability and the fewest low-cohesion groups. We therefore keep 15 broad clusters and 150 candidate topics. These are chosen levels of detail and not optimal counts. We keep both levels because the research question uses both. The fine topics link hearings to specific firm disclosures, and the broad themes summarize the hearing agenda.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_taxonomy_criteria.svg" alt="Clustering diagnostics across candidate category counts"></p>

*Choosing the codebook's level of detail. The horizontal axis gives the number of clusters. The navy line reports weighted mean coassignment as a percentage. The green line reports the share of phrase weight in clusters with coassignment of at least 0.50. The red line reports sampled silhouette multiplied by 100. Higher values indicate greater stability or separation and not classification accuracy.*

**5. Review the codebook and classify each hearing.** We review the 150 candidate groups before any assignment, because a plausible label alone cannot establish a coherent group. The [drafting notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/09_codebook_draft.ipynb>) shows the model each group's member subjects and the leading subjects of its two nearest groups. The model drafts a label and a one-sentence definition. It adds a note on how the group differs from its neighbors and five example phrases copied from the members (prompt in Appendix A.3). A parser removes any invented example. We then review every draft. The review keeps 111 groups, merges nine into kept groups, and drops 30. Dropped groups are held together by a shared word rather than by meaning, such as "program" or "initiative", or mix unrelated subjects. Merged groups join a kept group on the same matter, as the Clean Air and Clean Water Act subjects join EPA regulation. Each kept topic is placed under the broad cluster holding most of its subjects, which leaves 14 themes. The [codebook of 111 topics under 14 themes](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/codebook.json>) is then frozen with a version hash, so that every later assignment refers to the same topics.

We assign the hearing-level subjects by membership. Each subject keeps its group and follows any merge or drop, and 83.2 percent of the 11,592 mentions receive a codebook topic. The Facebook hearing's subjects are assigned as follows.

| Rank | Subject | Topic ID | Topic label |
|---:|---|---:|---|
| 1 | Facebook data privacy | 68 | consumer data privacy legislation |
| 2 | content moderation | 93 | Online advertising and consumer choice policies |
| 3 | election integrity | 100 | Voting systems standards and integrity |
| 4 | Honest Ads Act | 93 | Online advertising and consumer choice policies |
| 5 | GDPR-style controls | 68 | consumer data privacy legislation |

The hearing's primary topic is the topic with the most assigned subjects ([primary-topic rule](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/10_codebook_freeze_assign.ipynb>)). Here topics 68 and 93 tie at two subjects each. The code keeps the first row after sorting by hearing and count, which is topic 68 because it has the lower identifier as the earlier subject ranked, it is considered more important by LLM. The original subject ranks play no part. Across the entire hearing sample, 2,342 hearings receive a primary topic.

> **Coauthor note — primary-topic ties.** The implemented rule does not use the LLM's ranking, although the ranking is the natural tie-breaker.
>
> - Problem: Track 1 asks for subjects ordered from most to least central and the parser saves that order as the rank. The [primary-topic code](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/10_codebook_freeze_assign.ipynb>) then counts subjects per hearing and topic with a groupby call that sorts its keys by default. That sort discards the order in which subjects appeared and arranges the tied topics by identifier. The later sort by count is stable, so the lowest identifier wins every tie. In the Facebook hearing the lower identifier and the rank-1 subject point to the same topic, so the example hides the defect. Appendix B finds ties in 976 of the 2,342 classified hearings, and a rank-based rule would change 655 primary topics.
> - What should have been done: among tied topics, keep the one holding the highest-ranked subject. The simplest implementation is `groupby(..., sort=False)`, which keeps first-appearance order, or an explicit sort by the minimum rank within each topic. A tie indicator and the competing topics should be saved so that the ambiguity stays visible.
> - To do: decide the rule, apply it, rerun the primary assignment, and regenerate the CAP analyses and figures that depend on the primary topic. Until then the text describes the identifier rule. [Appendix B](#appendix-b-primary-topic-tie-breaking) holds the proposed alternatives and the comparison across tied hearings.

**6. Validate against an independent classification.** We check the hearing-level subjects and the topics built from them against an independent human classification. Format checks and single examples leave two questions open. One is whether an extracted phrase captures a hearing's substantive subject. The other is whether grouping the phrases brings hearings on related subjects together. The Comparative Agendas Project (CAP) codes congressional hearings into human-assigned *major topics* and *subtopics*. Our codebook uses its own categories, so we examine correspondence between the two systems rather than requiring identical labels.

The [matching notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/07_cap_matching.ipynb>) links hearings to CAP rows by Congress and committee and then by date and title. CAP's topic codes are not read at this stage, and the codebook was frozen before any evaluation contact. CAP ends with the 117th Congress, so 143 later hearings cannot be matched. Of the 2,209 hearings in the CAP window, 1,796 are matched. The [evaluation notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/11_cap_evaluation.ipynb>) keeps the 1,763 matches with the strongest evidence and requires usable codes in both systems, which leaves **1,697 hearings**. The Facebook hearing has no CAP match and does not enter these comparisons. Five assessments use this sample, and each addresses a different remaining uncertainty.

**(a) Does the extracted phrase identify the hearing's human-coded subject?** We embed each hearing's first-ranked Track 1 phrase and the descriptions of all 213 CAP subtopics with `BAAI/bge-large-en-v1.5`. We rank the CAP descriptions by similarity to the phrase and record the rank of the human-assigned subtopic. That subtopic ranks first for 27.0 percent of hearings and within the top 11 for 63.1 percent. The median rank is fifth. The histogram converts the ranks into percentiles, where 100 is first place. The first-ranked subject therefore carries enough of the hearing's substance to put the human code within the top 5 percent of 213 candidates for most hearings, where a random ranking would do so for 1 hearing in 20.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_cap_rank_percentile.svg" alt="CAP subtopic ranks for first-ranked extracted phrases"></p>

*Overall phrase correspondence. Each bar reports the share of hearings in a five-point percentile interval. The dashed line marks approximately 5 percent per interval under uniform random ranking.*

**(b) Does the phrase add information beyond the frequency of policy subjects?** Science and Technology hearings concentrate on particular subjects, so favoring common CAP codes alone would beat random ranking. We therefore compare the phrase-based ranking with a frequency rule that gives every hearing the same list of the most common subtopics. With one candidate, the phrase finds the human code for 27.0 percent of hearings and the frequency rule for 9.4 percent. With 11 candidates the shares are 63.1 and 52.9 percent. The gap is the correspondence that hearing-specific phrases add beyond the subject distribution. This means the correspondence in (a) comes from what each summary says about its own hearing rather than from knowing which subjects these committees usually take up.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_cap_retrieval.svg" alt="CAP retrieval compared with frequency and random baselines"></p>

*Retrieval against baselines. The horizontal axis gives the number of candidate CAP subtopics retained. The vertical axis gives the share of hearings whose human-assigned subtopic is among them. The frequency rule uses the same candidates for every hearing.*

**(c) Does the overall result conceal weak correspondence in particular policy areas?** We group the same percentile ranks by each hearing's codebook theme. Median correspondence is lowest for manufacturing competitiveness and highest for railroad safety, with theme sizes from 16 to 245 hearings. The grouping only organizes the diagnostic. The quantities evaluated are still the first-ranked phrases. This means the correspondence does not rest on a few well-defined policy areas, since the median in every theme lies above 90 and no box reaches the random line at 50.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_cap_subtopic_boxes.svg" alt="CAP phrase correspondence separated by codebook theme"></p>

*Variation across themes. Values nearer 100 indicate better phrase-level correspondence with the human-assigned subtopic. Whiskers extend to the most extreme observations within 1.5 interquartile ranges and outliers are hidden. The dashed line marks the median under random ranking.*

**(d) Do the broad codebook themes bring together hearings in similar human-coded policy domains?** We cross-tabulate each hearing's theme with its CAP major topic. Each row of the heatmap gives one theme's distribution across CAP domains and sums to 100 percent. In the NASA theme, 217 of 245 hearings (88.6 percent) receive CAP's Technology code. In Aviation and Transportation Security, 74 of 93 (79.6 percent) receive Transportation. A concentrated row shows correspondence with one CAP domain. A dispersed row marks a theme that spans CAP boundaries and warrants inspection. This means that for 7 of the 14 themes more than half of the hearings share one human-coded domain, so the themes largely reproduce boundaries a human coder drew, and the dispersed rows mark where the two systems divide the same hearings differently.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_cap_crosswalk.svg" alt="Codebook themes cross-tabulated with CAP major topics"></p>

*Broad category correspondence. Cells show percentages within each codebook theme. Numerical labels appear for shares of at least 10 percent.*

**(e) Do the detailed codebook topics retain distinctions within those broad domains?** We take the 25 most frequent primary topics and find the most common CAP subtopic within each. All 31 hearings under Federal agency and board nominations receive CAP's Appointments code. For Mars and lunar exploration missions, 39 of 43 (90.7 percent) receive Space. Shorter bars mark topics whose hearings CAP spreads across several subtopics. These bars describe concentration within a topic and are not accuracy estimates. This means the fine topics are at least as specific as CAP's subtopics, since several of them pair with the same CAP code and so separate hearings that the human coding merges, while the short bars are topics defined around a matter such as funding that CAP divides by field.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_cap_subtopic_pairs.svg" alt="Detailed codebook topics and their most common CAP subtopics"></p>

*Detailed category correspondence. Bar length is the share of a codebook topic's hearings receiving its most common CAP subtopic. The right-hand label names that subtopic. Counts alongside the topic labels show the available evidence.*

> **Coauthor note — the CAP validation is centered on the original subjects, and CAP was not a clean holdout.** The headline checks validate a unit that no later analysis uses, and the text does not say that CAP agreement shaped two design choices.
>
> - Done correctly: the final codebook was frozen before the evaluation notebook ran. Hearings were matched to CAP by Congress and committee and then by date and title without reading CAP codes. The comparison uses an independent human classification with frequency and random baselines. Agreement at the codebook level was also computed, with 25.8 percent of hearings ranked first and a median rank of ninth when the topic label replaces the subject, and a normalized mutual information of 0.557 between primary topics and CAP subtopics.
> - Done wrong: assessments (a) to (c) evaluate each hearing's rank-1 subject, but every later measure uses the codebook topic. The headline validation should therefore have been run on the primary topic, with the raw-subject result kept as a secondary diagnostic. The codebook-level results exist but were left to one closing sentence. In addition, CAP agreement informed two design choices in the [clustering notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/08_taxonomy_consensus.ipynb>). The 150-topic operating point was chosen partly for its closeness to the earlier superseded taxonomy that set the CAP-agreement bar, and the rule not to gate clusters on stability was adopted because gating lowered agreement on 1,236 CAP-matched hearings. The sentence above that the codebook was frozen before any evaluation contact is true of the final labels only. The checks also say nothing about Track 2.
> - To do: report the codebook-level versions of (a) to (c) as the headline and the raw-subject versions as a secondary check. State in the text that CAP agreement shaped the operating point and the gating rule, or hold out CAP hearings that were not used in those decisions. Track 2 validation stays in its own note under procedure 8.

**Track 2. Legislators' stances within topics**

Regulatory concern is expressed in what legislators say about a topic, which a summary may compress, attribute to no one, or even drop. Capturing it requires revisiting the original transcripts. Track 2 therefore adds to each hearing-level topic the stances legislators expressed about it. It supplies the within-topic variation described in the overview: how stances on a topic divide and change across Congresses and legislators, together with the attributed sentences that later procedures draw on. Track 2 reuses the model, the sentence numbering, and the screening discipline of Track 1. During extraction it does not reference Track 1, for the reason given in procedure 8. The placement in procedure 10 then serves as a cross-check between the tracks.

**7. Prepare the speaker turns.** *Track 2* takes each legislator's own speaker turn as its input. Witness turns are excluded because Track 2 measures legislators' stances that can directly affect firms through regulations. We prepare the inputs for *Track 2* in the following ways. The turns come from the speaker turns of Step #1 pre-processing. The [attribution rules](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/speakers.py>) that produced them read the honorific and surname opening a paragraph, attach a Bioguide identifier when the surname appears on the committee roster, and carry the presiding chair, written as "The Chairman" without a surname, under the placeholder identifier `0000000`. The [preparation notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/01_member_turns.ipynb>) selects turns labeled as spoken and attributed either to a committee member or to the chair. Across the entire hearing sample, 221,311 of 399,029 spoken turns (55 percent) are legislator turns, and 2,343 of the 2,352 hearings contribute at least one.

To find direct evidence of stance at a sentence-level of which researchers can revisit and check, we split each speaker turn into sentences with `pysbd==0.3.4` paragraph by paragraph. Then we apply four cleaning rules: truncate the turn at the first adjournment or inserted-document marker; drop the leading speaker-label echo ("Senator Dorgan."); drop bracketed stage directions; and drop mostly capitalized inline headers. The four rules are implemented in the [stance helper](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/stance.py>) and applied to the entire hearing sample by the [member-turn notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/01_member_turns.ipynb>), which reports each rule's removals. In our sample congressional hearings, this process yields 2,490,103 raw sentences. Truncation removes 1,249,776 (50.2 percent), label echoes 219,650, headers 28,666, and stage directions 6,350, leaving *985,661 sentences in 220,160 nonempty turns*. 

From the hearing on Facebook-Cambridge Analytica scandal 903 speaker turns, this procedure selects **507 legislator turns containing 1,696 cleaned sentences**. Sentence numbering starts at one within each cleaned turn, allowing the model to point to existing evidence without generating a quotation. Turns longer than 40 sentences are sent in consecutive windows that keep the turn-wide numbering; none in this hearing requires it.

> **Coauthor note — truncation in the example.** In the current run, truncation removed 13,380 sentences from the Facebook hearing, almost all from Grassley's final record, which carried the written-response appendix and keeps only [three closing sentences](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/01 - Inputs/numbered_turns.md#turn-902>); label echoes, stage directions, and headers removed 501, 15, and 44 more. Once the parser excludes the appendix (see the note in Section 3), these counts should be regenerated.

**8. Design the extraction and develop the prompt.** For *Track 2*, we extract each legislator's stances from the speaker turn prepared in procedure 7. The LLM is given one speaker turn with its numbered sentences and the speaker's name, together with the [Track 2 prompt](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/stance.py>). It sees nothing else. It does not see the witness's answer or the neighboring turns. It does not see the hearing's subject or the codebook. This is to capture different levels of granularity. Track 1's subject is general and Track 2's issues are granular under the document-level subject by design. If Track 2 selected sentences by Track 1's subject, most sentences in the hearing would count as relevant and the extraction of stance would lose its discrimination. Within the turn the model makes three judgments in order.

The first judgment is the *selection* of sentences that express a stance. The model decides which sentences express a stance toward a policy issue. Most sentences in a turn express no stance. Questions asked without a stance, procedure, and courtesies return nothing. So are introductions and factual statements without evaluation. The prompt closes with "when in doubt, do not extract." The rule favors precision, because an invented stance enters the counts while a missed one only lowers them. 

The second judgment is the *issue*. The model names what the stance is about as a short neutral noun phrase. The phrase must name the issue and never the direction toward it, and a bare amount is never an issue. This rule keeps the issue apart from the direction. Support for an issue and concern about the same issue can then enter one category later.

The third judgment is the *direction*. The model labels the stance `support` if the legislator endorses or urges adoption, funding, or expansion of the issue. It labels the stance `concern` if the legislator expresses worry or objection toward the issue. Urging restriction or delay or scrutiny of the issue also counts as concern. The record must read sensibly as "the member supports [topic]" or "the member is concerned about [topic]". A harm is recorded as concern and never as support. The direction has only two values. Stance-free attention is already covered by Track 1, and a two-way boundary is what a small model labels reliably. The output is a list of records. Each record holds one to three consecutive sentence numbers, the issue, and the direction.

Each record the model returns is screened by rule-based code against the speaker turn it came from before it enters the data. To keep invalid records out of the data, the [Track 2 parser](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/stance.py>) rejects any output that is not well-formed JSON or that uses a stance label other than support or concern. It rejects any record whose cited sentence numbers do not exist in the turn, exceed three, or are not consecutive. Every rejection is recorded with its reason and counted. The parser also checks the issue against a fixed dictionary of directional words, and this check marks records without removing any. The dictionary is a list of sixteen word stems written into the parser before the full run. It covers words of opposition such as ban or repeal and words of endorsement such as support or expand. A stem is matched at word boundaries regardless of case. A matching issue receives a flag that stays attached to the record for later review, and the record enters the data and every later measure like any other. The parser then merges records that share an issue and a direction when their cited sentences overlap or lie within two sentences of each other. This merge prevents a stance stated three times in one turn from counting three times.

> **Coauthor note — screening counts.** The dictionary removed nothing, its review step was never run, and the sentence-citation rule is the only screening step that discarded model output.
>
> - The dictionary worked as a detector for later check and removed nothing. It flagged 838 of the 32,385 kept records (2.59 percent), and all of them remain in the data and the figures. The flag marks an issue phrase that carries a direction, such as "effort to reduce or eliminate federal incentives" labeled concern, where the legislator in fact supports the incentives and the record would enter the panel with an inverted sign.
> - Not followed through: the flagged records were meant to be reviewed and repaired before aggregation, and that review never ran beyond a five-record check that the flag works. 326 of the 838 flags come from "protection" and its forms in neutral names such as consumer protection and are harmless. The remaining flags include genuine leaks like the example above, so an unknown share of at most 838 records may carry an inverted sign in the panels.
> - The sentence-citation rule discarded 4,680 records, against 32,385 kept. The rule works as follows. The prompt numbers the sentences of each speaker turn and asks the model to cite, for every record, the one to three consecutive sentence numbers that express the stance. The parser drops any record whose cited numbers do not exist in the turn, exceed three, or are not consecutive, so a stance the model grounded in four sentences or in sentences 2 and 9 is thrown away rather than trimmed. To do: sample the 4,680 dropped records and estimate that share, and if it is high keep the longest consecutive run of cited sentences or split a record into runs and rerun the assembly. For the flags, review the non-"protection" subset and repair the sign where the issue phrase carries the direction.

This extraction procedure, the prompt together with the parser, was fixed only after development on a small sample before the full run. The [stance promptbook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/02_extraction_promptbook.ipynb>) iterated the Track 2 prompt on 30 seeded turns of varied length from both chambers. Short procedural turns were included on purpose, because the correct output for most of them is an empty list. Every round was read turn by turn beside the extracted records rather than judged from error rates. Three rounds removed the observed failure classes. These included appended written material, truncation of long opening statements, and a harm recorded as the supported issue. The recorded version is `stance-extraction-0.3-dev`. The planned `1.0` relabeling was never applied, so the logs carry the `-dev` label and the wording did not change after the full run began.

> **Coauthor note — stance judgments not yet validated.**
> - Problem: no error rate exists for the three Track 2 judgments. The development outputs include indirect stances that returned nothing ("you have to register me as one of the skeptics about the consolidation proposal") and a 45-sentence opening statement that produced 26 records, including a concern for every adverse issue it mentioned. 
> - To do: benchmark the three judgments against human coding or a commercial LLM's classification.

**9. Extract legislators' stances.** We send each cleaned speaker turn to the model with the Track 2 prompt from procedure 8 ([production notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/03_track2_production.ipynb>)). Senator Hassan's [turn](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/01 - Inputs/numbered_turns.md#turn-772>) includes the following sentences.

```text
[6] You have supported targeted regulations such as the Honest Ads Act, and that is an important step for election integrity.
[7] I am proud to be a cosponsor of that bill.
```

The [recorded response](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/stance_records.md#turn-772-record-0>) is the following.

```json
[{"sentences": [6, 7], "topic": "Honest Ads Act", "stance": "support"}]
```

The record identifies Hassan's support for the Honest Ads Act and nothing more, and the cited sentences make that reading checkable in the source. For the Facebook hearing, eight candidate records fail the consecutive-reference check and one merge combines duplicates. That leaves 49 stance records from 27 turns. The example's [verification script](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/04 - Scripts/export_example.py>) reproduces the parsing and merging and matches every prompt to the saved logs.

Across all hearings, the [assembly notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/05_assemble_stance_records.ipynb>) combines the results and checks that every nonempty turn appears exactly once. The extraction yields **32,385 records**, 16,149 support and 16,236 concern. Only 6 percent of turns return a record, and 1.87 percent of turns have a structural error. The records contain 24,798 distinct issues. A [production check](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/06_track2_production_check.ipynb>) read a sample of 45 records beside their cited sentences. About 85 to 90 percent read correctly on all three fields. The defects were a harm recorded as the supported issue, vague issues such as "agencies", and issues grounded in adjacent uncited sentences.

**10. Place the stance records into the codebook.** We place each Track 2 record under a codebook topic in the following way. The issues in Track 2 took no part in the earlier clustering, so they need an assignment rule of their own. An earlier run that pooled the subjects and the issues before clustering found only 4.6 percent of distinct phrases shared between the two, because hearing subjects and the issues of single statements sit at different levels of detail. The [assignment notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/10_codebook_freeze_assign.ipynb>) represents each topic by the average embedding of its Track 1 member subjects, weighted by how often each subject was extracted. It embeds each of the 24,798 distinct issues with the same encoder and places the issue in the topic whose embedding is closest, provided the cosine similarity is at least 0.68. An issue below that floor stays in "other" rather than being forced into a topic. The floor was carried over from the trial run, where a sample of placements just above it had been read and judged acceptable. Each record keeps its stance label, cited sentences, and original wording. It gains a topic and a similarity value. Across the entire hearing sample, 92.6 percent of records are placed and the median similarity among them is 0.78, which leaves 29,979 placed records and 2,406 in other. Hassan's "Honest Ads Act" from the running example is mapped to "Online advertising and consumer choice policies (topic 93)" at similarity 0.733. Of the Facebook hearing's 49 records, 41 are placed and eight stay in other.

This mapping procedure can also serves as the cross-check between the tracks. Of the Facebook hearing's 41 placed records, 24 fall in the two topics holding that hearing's top-ranked subjects, 13 in consumer data privacy legislation and 11 in online advertising and consumer choice policies. The two tracks reached those topics from different inputs and different prompts.

> **Coauthor note — Need to Revisit the threshold floor decision.**
> - The floor controls whether an issue is placed and not whether the topic fits. Tillis's [“business code of conduct” record](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/stance_records.md#turn-656-record-1>) is placed in “hours-of-service regulations” at similarity 0.695. Because every record keeps its sentence references and original wording, such cases can be found and reviewed.
> - Of course, there will be no perfect threshold at this scale, but for better results at least in the running example.

**11. Aggregate records into topic–Congress and legislator panels.** Finally, we count assigned stance records by topic and by Congress. In this research question, we count statements rather than legislators, because the question is what was mainly discussed and in what ways. The legislator-level table below serves the other reading, how many legislators hold a view. The research question compares stances across subjects and periods, and the Congress gives a common two-year period. The [panel notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/12_stance_panel.ipynb>) builds two tables. The Facebook hearing falls in the 115th Congress, which covers 2017–2018.

The topic-by-Congress table holds one row per topic and Congress. Each row counts the assigned records, the support and concern records separately, and the distinct hearings and speakers contributing them. The table has 1,453 rows.

A separate measure summarizes the balance of stances within a topic and period.

$$
\text{Net stance} = \frac{\text{Support records} - \text{Concern records}}{\text{Support records} + \text{Concern records}}
$$

The measure ranges from −1 when all records express concern to +1 when all express support. Zero means equal counts. It is defined when at least one record is present, and a minimum-record rule can keep sparse cells out of displays. The underlying counts should be kept, because similar balances can arise from very different volumes of discussion.

The privacy category shows how one hearing contributes to a period total.

| Records for “consumer data privacy legislation” | Hearings contributing records | Support | Concern | Total records |
|---|---:|---:|---:|---:|
| Zuckerberg hearing alone | 1 | 7 | 6 | 13 |
| All contributing hearings in the 115th Congress | 17 | 34 | 21 | 55 |

The 13 records from the Facebook hearing are part of the period's 55. The other 42 come from 16 further hearings. Each assigned record counts once whatever the length of its supporting passage, and one legislator can contribute several records. The net stance for privacy in the 115th Congress is therefore (34 − 21) / 55 = 0.236.

The legislator-level table splits the same records by speaker. Each row gives the number of records one speaker contributed to one topic in one Congress with one stance. For Hassan, category 93 in the 115th Congress has one support record and four concern records. The support record is the Honest Ads Act and the concern records are other issues such as ad targeting. The table therefore keeps distinct stances within a shared category without assuming that every statement concerns the same proposal.

> **Coauthor note — what support and concern measure.** The direction is judged toward the issue the model named, so after placement one topic mixes opposite policy stances.
>
> - Problem: concern about a harm such as "Facebook data policy" and concern about a rule such as "Facebook regulation" both enter a topic as concern, although the first is a pro-regulation stance and the second an anti-regulation one. In the Facebook hearing's consumer data privacy legislation topic, Kennedy's concern about "Facebook regulation" and Nelson's concern about "privacy" are both counted as concern. In its online advertising topic, the four support records all endorse the Honest Ads Act and the seven concern records object to platform practices such as ad targeting, so the net stance of −0.27 misreads a set of records that all favor rules. The net stance in procedure 11 is therefore not a measure of stance toward regulation.
> - To do: maybe narrow the scope instead of general support or concern. For example, "stricter rule" or "less strict rule" might work. 

The legislator table has 15,173 rows covering 27,679 records. It omits 2,300 records spoken by an unnamed chair, because the grouping drops records without a surname. Those records remain in the topic-by-Congress totals under a shared placeholder identifier. The two tables therefore cover different sets of records, and the topic table's speaker count is not a count of identified individuals.

We archive every stage's inputs and outputs for both tracks. The call logs keep one line per model call with its prompt version and input hash and full output. The intermediate tables keep the cleaned turns and the records before and after merging. They also keep the clusters at every tested count, the frozen codebook, and both assignment tables and panels. For the Facebook hearing, the [verification script](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/04 - Scripts/export_example.py>) re-derives every procedure from the cleaning to the assignments without any model call. A reader can therefore confirm what the saved computation did before judging what it got right.

### 4.3. Research Outputs

The pipeline produces data at three levels: the subjects of individual hearings, the stances expressed in individual statements, and counts of those stances across legislators and time. These outputs allow researchers to identify hearings on a common subject, retrieve the statements underlying a measured stance, and examine how the volume and balance of expressed views vary across topics and Congresses. The panel-construction rules and worked aggregation appear in Section 4.2. The outputs retain the following levels of information:

| Output | What it contains | Research use |
|---|---|---|
| Numbered legislator turns | 220,160 cleaned turns with speaker identifiers and sentence lists, plus the per-rule removal counts. | Resolve any cited sentence number to its text and inspect what the cleaning rules removed. |
| Hearing subject lists | Up to five ranked phrases for each of the 2,352 hearings (11,592 mentions), their codebook assignments, and a primary topic for 2,342 hearings. | Select hearings by subject and inspect the phrases behind a classification. |
| Stance records | 32,385 records with speaker, hearing and turn identifiers, cited sentence numbers, issue phrase, stance, wording flag, assigned category, and similarity. | Retrieve the statements underlying a measured stance. |
| Frozen codebook | 111 topics under 14 themes with definitions, exclusion notes, example phrases, and stability and cohesion diagnostics, identified by hash. | Common categories for Sections 4 and 5. |
| Topic-by-Congress and legislator tables | 1,453 topic–Congress rows and 15,173 legislator rows of support and concern counts. | Compare the volume and balance of stances across subjects, periods, and speakers. |
| Call logs | One line per model call for both tracks and for codebook drafting, with prompt version, input hash, token counts, timing, and full output. | Reproduce any prompt and distinguish a model decision from a parsing failure. |

Here we describe the available records and the patterns their aggregated counts make observable.

**1. Hearing topics and statements that can be traced to their source.** The codebook provides a common set of 111 topics under 14 broad themes, including definitions and example phrases. The hearing-level output retains the ranked phrases extracted from each of the 2,352 summaries and their assigned categories; 2,342 hearings also receive a primary-topic classification. A researcher can therefore select hearings classified under a subject and inspect the original phrases that led to that classification. For the Zuckerberg hearing, the [saved topic output](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/topics.json>) retains both “Facebook data privacy” and “GDPR-style controls,” even though both enter the standardized category “consumer data privacy legislation.” This preserves more detail than a single hearing label would convey.

The stance output contains 32,385 records. Each records an issue phrase, a support-or-concern label, the speaker, the hearing and turn identifiers, and references to the sentences supporting the extraction. For example, [Hassan's record](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/stance_records.md#turn-772-record-0>) links her support for the Honest Ads Act to sentences 6 and 7 of turn 772, and also records its assignment to category 93, “Online advertising and consumer choice policies.” Researchers can move from the standardized category back to the specific issue and source language. The saved dataset retains the 2,406 records assigned to “other”; the aggregated topic measures below use the remaining 29,979 records with codebook assignments.

The two aggregated outputs summarize these records by topic and Congress, and by legislator, topic, Congress, and stance. The former supports comparisons of discussion across subjects and periods; the latter identifies the speakers contributing those expressions. Their coverage differs because unnamed-chair records enter the topic totals but are excluded from the legislator table, as documented in Section 4.2.

**2. Which topics generate the most expressions of support and concern?** The first figure uses the topic-by-Congress table to compare the overall volume and balance of stances across subjects. The code sums support and concern records over all Congresses, selects the 25 topics with the largest combined counts, and draws one row for each. Concern records extend left from zero and support records extend right. The combined length of the two bars gives the total number of records for that topic; comparing the two sides reveals which stance is more frequent.

For example, “Science and research funding” contains 1,372 records: 716 support and 656 concern. Its two long bars indicate many extracted stances on both sides. Other topics can have similar totals with a more uneven balance. These comparisons identify subjects that generated substantial directional discussion in the sampled hearings. They measure expressions retained by the extraction procedure, so factual discussion and questions without an extracted stance do not add to the bars. Counts also give more weight to speakers who contribute more records.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_stance_topics.svg" alt="Support and concern by topic"></p>

*Support and concern across topics. Each row is one of the 25 topics with the most assigned stance records over the full sample. Bar lengths are record counts; left and right indicate concern and support, respectively.*

**3. When do those topics receive attention through expressed stances?** Totals over the full sample cannot show whether a topic generated stances throughout the period or mainly during a few Congresses. The second figure separates the same 25 topics by Congress. Each row is a topic, each column is a two-year congressional period, and each cell contains the combined number of support and concern records for that topic and period. Darker blue indicates more records. Reading across a row reveals the timing of activity on one subject; reading down a column compares the subjects discussed during the same Congress.

For example, science and research funding has 146 records in the 109th Congress and 129 in the 115th. These counts describe the volume of extracted stances without distinguishing their direction. Differences can reflect the number and subjects of hearings, the participating speakers, and their frequency of expressing stances. The figure reports raw counts rather than rates adjusted for those opportunities to speak; its darkest shade is capped at the 98th percentile of displayed cell counts. It can locate periods for closer investigation, but a darker cell alone does not establish a change in policy priorities.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_stance_attention.svg" alt="Stance record counts by topic and Congress"></p>

*Timing of expressed stances. Cells show support and concern records combined. The 25 topics are ordered by their total record counts over the sample, and columns run from the 104th through the 119th Congress. Combinations with no assigned records are displayed as zero.*

**4. How does the balance of support and concern change within a topic?** The attention figure treats support and concern alike: two equally dark cells can contain very different mixtures of stances. The third figure applies the net-stance measure defined in Section 4.2 to the counts assembled there. Values near −1 indicate predominantly concern records, values near +1 predominantly support, and zero equal counts.

Within the plotted topics, science and research funding changes from 59 support and 87 concern records in the 109th Congress, giving −0.192, to 74 support and 55 concern records in the 115th, giving +0.147. Thus, similar volumes of records can accompany a change in the balance of expressed views.

In the figure, red indicates more concern, navy indicates more support, and pale shading indicates a balance near zero. Cells with fewer than five records are blank to avoid displaying a strong-looking balance based on very little evidence; a blank cell can therefore contain a few records and does not imply an absence of discussion. Because the measure weights records rather than individuals, a change can reflect different speakers or proposals as well as changing stances. The original issue wording and sentence references allow researchers to inspect those possibilities. The extraction and assignment errors illustrated in Section 4.2 also carry into these descriptive measures until the underlying records are reviewed and corrected.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T2%20-%20Topic%20Extraction%20and%20Stance%20Analysis/fig_stance_net.svg" alt="Net stance by topic and Congress"></p>

*Balance of expressed stances. Color represents net stance for the same topic–Congress combinations as the attention figure. Cells with fewer than five records are masked; a colored value describes the balance among extracted records, rather than a legislative vote or consensus on a single proposal.*

---

## 5. Step #3: Identifying Topic Relevance and Corporate Disclosure

Topic relevance is the bridge between two independent sets of documents. Step #1 Text Summarization and Step #2 Topic Extraction describe what the first set of documents is about, as topics. Step #3 Topic Relevance takes a second set of documents and links each of them to those topics. Calculating topic-to-document relevance can serve social science research in two ways.

1. **Capturing the broader affected group.** It captures links that are not easily observable, and so it captures a broader scope of exposure. For example, in management research, most links between a policy event and the entities it affects rest on explicit evidence. An entity is in the treated group, if it was explicitly named in the document, or it belongs to the industry the policy addresses. But in many cases, a general subject such as "consumer data privacy" reaches every entity whose business handles consumer data, in health care and finance as much as in social media. Our topic relevance links through the "topic" so it rather asks whether the firm is relevant to consumer data privacy directly.
2. **Capturing heterogeneity in exposure.** Linking directly to the documents allows to capture heterogeneity in exposure. If exposure is defined by a high-level boundary, the variation within the group can be lost. For example, whether an entity is mentioned or which industry it belongs to. Measuring relevance from the text directly can gives each entity a degree and a direction of exposure.

### 5.1. How Topic Relevance Works

Topic relevance can be calculated in two ways. First, the similarity-based measure computes how closely a document's sentences resemble each topic. Second, the LLM-based measure reads the document and tags the sentences that make the entity relevant to a topic, each with a direction of exposure. The two measures are independent and complementary. They target the same theoretical construct but capture different parts of it. The table states the details of each measure. 

<table style="border-collapse: collapse;">
<thead>
<tr style="border-top: 1.5px solid; border-bottom: 1px solid;"><th></th><th>Similarity-based measure</th><th>LLM-based measure</th></tr>
</thead>
<tbody>
<tr><td>Theoretical construct</td><td colspan="2">Exposure. The degree to which an entity is affected by a topic, and whether as a threat or an opportunity.</td></tr>
<tr><td>What the measure captures</td><td>Textual closeness. How closely the document's sentences resemble the topic's definition and evidence sentences, regardless of what the sentences say about the entity.</td><td>Stated exposure. Whether the document says that the entity's activities fall within the topic, in which sentences, and whether each sentence presents the topic as an opportunity, a threat, or neither.</td></tr>
<tr><td>Unit of analysis</td><td>Topic–sentence cosine similarity, computed for every retained sentence and aggregated to one score per document and topic from the closest sentences.</td><td>Topic–sentence tags, assigned by the model while reading blocks of consecutive sentences and aggregated to one count and direction shares per document and topic.</td></tr>
<tr style="border-bottom: 1.5px solid;"><td>Form of the output</td><td>One continuous value per document and topic, with the contributing sentences kept</td><td>One record per tagged sentence, and per document and topic a related indicator, a count, and direction shares.</td></tr>

</tbody>
</table>

Because the two measures are complementary, they can be combined once each has been calculated on its own. The similarity-based measure gives every sentence a degree of closeness to the topic but no direction, and the LLM-based measure gives selected sentences a direction but treats every tagged sentence alike. Weighting each tagged sentence by its closeness yields one index per direction that captures how much of an entity's text concerns the topic as a threat and how much as an opportunity, and how closely that text sits to the topic. 

Detailed procedures of topic relevance calculation are as follows.

***a. Procedures for the common input from Topic Extraction***

Both similarity-based and LLM-based measures take the topic side as fixed. However, each measure can take different from of input. In this procedure, we prepare inputs for the two approaches.

1. **Prepare input #1 Topic label and definition.** Each topic has its label and the one-sentence definition in the codebook from Step #2. The label names the topic in a few words, and the definition states the subject area the topic covers and what falls outside it. Label and definition are used in both similarity-based and LLM-based measures. 

    However, the forms each measure takes differ because each needs a form it can use. The LLM-based measure judges from a readable boundary, so the raw text label and the definition are enough for it to decide whether a sentence of the second set is relevant, and it takes no other input. In contrast, the similarity-based measure needs a reference vector in the same space as the sentences it scores, and a single definition sentence embeds to one thin and abstract point. It therefore turns the definition into an embedding and adds the evidence sentences prepared in the next two procedures, with the definition as one vote among several hundred to draw concrete boundary for relevance calculation.

***b. Procedures for the similarity-based measure***

2. **Prepare input #2 selected evidence sentences for similarity-based measure.** A definition is one sentence, so on its own it anchors a topic thinly in sentence space. The reference needs a set of sentences from the first dataset that anchor the topic's label and definition for similarity-based measure. The first dataset may hold many sentences that touch a topic, most of them incidentally, and using them all would blur the reference. Therefore, a selection rule is needed that keeps the sentences carrying the topic's core frame. For example, sentences in which legislators take a stance on the topic lay out a concrete frame of how the topic is discussed in the hearings.

3. **Build each topic's vector for similarity-based measure.** The similarity-based measure needs one fixed reference per topic, so that documents can be compared with one another and over time. Topic $k$ is represented by its definition and its $M_k$ evidence sentences. Each is embedded, the unit vectors are averaged with equal weight, and the average is normalized:

    $$
    \mathbf{v}_k=\frac{\mathbf{u}_k}{\lVert \mathbf{u}_k\rVert},
    \qquad
    \mathbf{u}_k=\frac{1}{1+M_k}\Big(\mathbf{e}(\text{definition}_k)+\sum_{m=1}^{M_k}\mathbf{e}(\text{sentence}_{k,m})\Big).
    $$

    In words, the definition and every evidence sentence are embedded, the vectors are averaged, and the average is scaled back to unit length so that it can be compared with sentence vectors by cosine.

4. **Prepare input #3 sentences of the second dataset.** The similarity-based measure compares a topic with a document one sentence at a time. A relevant passage can be a few sentences in a long document, so one embedding of the whole document would dilute it, and letting a model pick the key sentences would put *inference* into a measure meant to be free of it. Each document is therefore split into sentences with the same segmenter used for the first dataset, so that the two sides are compared like with like. Sentences below a minimum length are dropped, and sentences repeated across many entities are removed as boilerplate. Each remaining sentence keeps its document date, entity identifier, and position, and is embedded once as a unit vector $\mathbf{e}_s$. The same retained sentences are read by the LLM-based measure in part c.

5. **Calculate similarity scores and standardize.** Each document receives one score per topic. The topic enters as its vector $\mathbf{v}_k$ from procedure 3, and the document enters as its sentence vectors $\mathbf{e}_s$ from procedure 4. The cosine similarity between sentence $s$ and topic $k$ is

    $$
    c_{sk}=\frac{\mathbf{e}_s^{\top}\mathbf{v}_k}{\lVert\mathbf{e}_s\rVert\,\lVert\mathbf{v}_k\rVert},
    $$

    which ranges from $-1$ to $1$ and is simply the dot product $\mathbf{e}_s^{\top}\mathbf{v}_k$ because both vectors have unit length. Stacking a document's $N_d$ sentences as the rows of $\mathbf{E}_d$ and the topic vectors as the columns of $\mathbf{V}$ gives every cosine at once, $\mathbf{C}_d=\mathbf{E}_d\mathbf{V}$. The document's raw score on a topic is the mean of its $K$ largest cosines, with $K$ small and fixed, such as five, and $c_{(j)k}$ the $j$-th largest cosine in column $k$:

    $$
    r_{dk}=\frac{1}{K}\sum_{j=1}^{K}c_{(j)k}.
    $$

    The maximum would let one sentence decide and the full mean would dilute, so the mean of the few closest sentences is taken, and those $K$ sentences are kept as the score's evidence. Raw scores rise with document length and differ across topics, so each score is standardized within topic and length decile. With $\ell(d)$ the length decile of document $d$ and $\mu_{k\ell}$ and $\sigma_{k\ell}$ the mean and standard deviation of raw scores in that topic and decile,

    $$
    z_{dk}=\frac{r_{dk}-\mu_{k\,\ell(d)}}{\sigma_{k\,\ell(d)}}.
    $$

    In words, the document's raw score is compared with the raw scores of all documents of similar length on the same topic, and $z$ counts how many standard deviations it sits above or below their mean. The value compares documents within a topic and says nothing across topics.

***c. Procedures for the LLM-based measure***

6. **Prepare the documents as numbered blocks.** The model needs surrounding sentences to judge one, but a whole document exceeds what a small model reads reliably. Each document is cut into blocks of consecutive sentences of a fixed size, numbered document-wide. Document order decides which sentences are read together. No similarity output touches this step, which is what keeps the two measures independent.

7. **Design the judgments.** The model makes the following three judgments.

    a. *Screening.* Which topics a block plausibly touches, chosen from the full list of topic labels. The screen is told to be generous, because its only purpose is to spare the next judgment definitions a block plainly never touches.

    b. *Selection.* Which sentences describe the entity's own activities within a candidate topic, given that topic's definition. The model cites sentence numbers and skips generic statements that are not about the entity. A sentence does not need to name a law or an event.

    c. *Direction.* Whether the sentence presents the connection as an opportunity, a threat, or neither, from its wording alone.

    Screening and selection are separate calls because reading every block against every definition is costly. The cost of the screen is missed topics, which is measured rather than assumed. Each returned record is checked by code against the block it came from. Prompts are refined on a small sample with every output read before the full run.

8. **Read and tag.** One screening call per block returns candidate topics. One confirmation call per block, with the candidates' definitions, returns tags of the form sentence, topic, direction. Every call is logged with its prompt and its complete output.

9. **Aggregate the tags.** For document $d$ and topic $k$, $n_{dk}$ counts the distinct sentences that carry a tag, and $n^{\text{threat}}_{dk}$, $n^{\text{opportunity}}_{dk}$, and $n^{\text{neutral}}_{dk}$ count them by direction. The document is related to the topic when $n_{dk}\ge 1$, and its intensity is $n_{dk}$. The direction shares divide each direction's count by $n_{dk}$, so that for threat the share is $n^{\text{threat}}_{dk}/n_{dk}$, and they are undefined when the document has no tag. A share per 100 sentences, such as $100\,n^{\text{threat}}_{dk}/N_d$, uses all $N_d$ retained sentences of the document as the denominator and so makes the document's length explicit. A document whose calls were flagged and that has no tag is recorded as unknown, not as zero. Documents of the second set are then linked to documents of the first through the shared topic and a date rule, such as the latest document available before the event.

***d. Procedures using both measures***

The two measures are complementary. Each is strong where the other is weak, and the table states only that. The procedures that use both follow.

| | Similarity-based measure | LLM-based measure |
|---|---|---|
| Strength | Gives every sentence a continuous degree of closeness to the topic, for every document and topic, at low cost and reproducibly. | Reads what a sentence says. It finds exposure stated in the entity's own words, and it supplies the direction and the intensity that closeness cannot. |
| Weakness | Blind to direction and to meaning. It cannot tell whether closeness comes from the entity's activities or from shared wording, and it rewards language about neighboring subjects. | Blind to degree. Every tag counts the same whether the sentence sits at the heart of the topic or at its edge, and it sees only the sentences it selected. Coverage is bounded by cost, and the labels follow the model's reading of the wording. |

10. **Combine similarity and direction into an index.** As the table above shows, both measure has strength and weakness speaks to different points. A score from similarity-based measure has no direction, and a count from llm-based measure gives every tag equal weight. The index weights each tagged sentence by its own cosine to the topic and keeps threat and opportunity apart so that they cannot cancel. Each sentence's weight is its cosine, or zero when the cosine is negative:

    $$
    w_{sk}=\max(0,\,c_{sk}).
    $$

    The threat index of document $d$ on topic $k$ adds the weights of the sentences tagged as threats on that topic, divides by all $N_d$ retained sentences of the document, and multiplies by 100. The opportunity index does the same for the sentences tagged as opportunities:

    $$
    \operatorname{Threat}_{dk}=\frac{100}{N_d}\sum_{s\,\in\,\text{threat tags on }k} w_{sk},
    \qquad
    \operatorname{Opportunity}_{dk}=\frac{100}{N_d}\sum_{s\,\in\,\text{opportunity tags on }k} w_{sk}.
    $$

    In words, go through the document's sentences, add up the cosines of those tagged as threats, and express the sum per 100 sentences. Neutral and untagged sentences add nothing but stay in the denominator. When a document has at least one tag in a direction, the index equals the share per 100 sentences from procedure 9 multiplied by the mean weight of those tagged sentences, so a document scores high when it has many directional sentences that are also close to the topic. The units are similarity-weighted sentence equivalents per 100 sentences, not a percentage and not an estimate of gain or loss. The index inherits the weaknesses of both measures, so it is reported beside them and not in their place.

    The index is the step's final outcome, and what it captures is intensity with direction. For each document and topic it gives two numbers, one for threat and one for opportunity. Each rises with the share of the document's sentences that present the topic in that direction and with how closely those sentences sit to the topic. In terms of the construct, it is the degree of disclosed exposure in each direction. The LLM-based measure supplies which sentences count and in which direction, and the similarity-based measure supplies how much each counts. It is therefore the operationalization that comes closest to the theoretical construct in the first table, exposure as a degree and a direction.

11. **[TO BE UPDATED] Validate the measures and check their agreement.** Validation relies on two ways. First, agreement between the measures compares scores for documents with and without tags and the share of documents with a tag across score quantiles. Because neither measure enters the other, agreement is evidence of convergent validity, and the documents on which they disagree are the ones to read. Second, human review of a sample of tags then tests whether each tagged sentence concerns the entity under the definition and whether its direction follows from the wording.

### 5.2. Application: Hearing Topics and S&P 500 10-K Item 1 Disclosures

We connect the 111 hearing topics of Section 4 to firms' descriptions of their businesses in 10-K Item 1. A filing is relevant to a topic when a passage describes the firm's products, services, technologies, inputs, customers, or operating conditions within the topic's subject area. The passage need not name a hearing, a law, or an agency, so the link can cross industries while still requiring evidence about the firm's own activities.

We follow the procedures of Section 5.1 in the same order and at two scales. The similarity-based measure is computed for every filing and every topic. The LLM-based measure is run for one topic and one firm-year, with each firm's latest filing before the hearings of 2018. [THIS WILL BE UPDATED TO ALL TOPICS IN FINAL VERSION ONCE ALL METHODS ARE AGREED] The running example continues the April 10, 2018 Zuckerberg hearing, `CHRG-115shrg37801`, whose primary topic is topic 68, consumer data privacy legislation. The [worked example](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/README.md>) follows this topic from the codebook to firm disclosures, scores, tags, and the hearing–firm table. Facebook anchors the example, ResMed supplies a comparison for the similarity calculation, and Total System Services, Paycom Software, and Fidelity National Information Services supply sentence-level illustrations of threat and opportunity.

***a. Common input from Topic Extraction***

**1. Prepare input #1 topic label and definition.** We take the topic side from the frozen [codebook](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/codebook.json>) of Section 4, which gives each of the 111 topics a label and a one-sentence definition. For example, the entry for consumer data privacy legislation topic is the following.

```json
{
  "topic_id": 68,
  "label": "consumer data privacy legislation",
  "definition": "This topic encompasses federal and state laws, proposed bills, and regulatory frameworks specifically addressing the collection, use, and protection of consumer personal information."
}
```

The saved entry also carries the theme, the exclusion notes drafted against the two nearest groups, and five example phrases copied from the group's subjects, none of which Step #3 reads. The similarity-based measure embeds the definition as one input to the topic vector. The LLM-based measure reads all 111 labels in its screening call and the definition of topic 68 in its confirmation call. Nothing in this section changes the codebook.

***b. Similarity-based measure***

**2. Prepare input #2 evidence sentences for the similarity-based measure.** We anchor each topic with the hearing sentences in which legislators took a stance on it. The [topic-vector notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/02_topic_centroids_scores.ipynb>) takes the 29,979 Track 2 records that Section 4 placed under a topic at the 0.68 floor, resolves the one to three sentence numbers each record cites to their texts in the speaker turn, and drops duplicate sentences within a topic. This gives **37,104 topic–sentence pairs** across the 111 topics, with a median of 263 sentences per topic and a minimum of 27. Only the text of each sentence is kept, and its support or concern label is left behind.

The selection is made entirely by the stance extraction and the placement of Section 4. For the Facebook hearing, legislators spoke 1,696 sentences. Stance records cite 70 of them. Thirteen of those records were placed under topic 68, and the 19 distinct sentences they cite are the hearing's contribution to the privacy topic. Pooled across all hearings in the sample, including hearings after April 2018, topic 68 has **474 distinct evidence sentences**. The pool is therefore a retrospective representation of how legislators talk when they take a stance on privacy, not a representation of the Zuckerberg hearing alone.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_topic_vector_schematic.svg" alt="Hypothetical embedding space showing how a topic vector is built"></p>

*How the privacy topic is anchored. Left panel: of all legislator sentences in the hearings, only those cited by a Track 2 stance record whose issue was placed under consumer data privacy legislation qualify as evidence. The choice is made by the stance extraction and the placement of Step #2, not by similarity. Right panel: the evidence sentences and the codebook definition are embedded and averaged into the topic vector. The space is a hypothetical two-dimensional embedding space, and the positions are drawn for illustration.*

**3. Build each topic's vector for the similarity-based measure.** We embed the definition and the 474 evidence sentences of topic 68 with `BAAI/bge-large-en-v1.5`, average the 475 unit vectors with equal weight, and normalize the result. The definition is one vote among 475. The same notebook does this for every topic, so each has one fixed vector. This vector is built from sentences and is not the Section 4 centroid, which was built from Track 1 subjects and served only to place records. It is fixed across firms and years.

**4. Prepare input #3 sentences of the 10-K Item 1.** We prepare the firm side from the 21,966 usable Item 1 disclosures of the 1,061 firms ever in the project's S&P 500 sample. The [sentence-preparation notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/01_item1_sentences.ipynb>) applies the [relevance helper](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Background Helper Functions/relevance.py>), which segments each Item 1 with the same pinned segmenter as the hearings, `pysbd==0.3.4`, and drops sentences shorter than 30 characters. It then removes boilerplate. Each sentence is lowercased, digit runs are replaced by a marker, and punctuation and whitespace are removed, and a form that appears in 20 or more distinct firms is excluded. The most widespread forms are headings such as "Executive Officers of the Registrant," rows of table figures, and the standard sentence directing readers to the SEC's Public Reference Room.

Segmentation yields 7,848,199 sentences. The length filter keeps 6,331,719, and the boilerplate filter removes a further 24,926, leaving **6,306,793 retained sentences** with a median of 239 per filing. The filter removes 0.39 percent of sentences at this threshold, and it would remove 0.56 percent at 10 firms and 0.21 percent at 50, so the result does not depend on the choice. Each retained sentence keeps its filing identifier, firm identifiers, fiscal year, and index, and is embedded once with `BAAI/bge-large-en-v1.5` as a unit vector. The vectors are stored in one matrix whose rows match the sentence table, so a sentence's index also locates its vector.

The LLM-based measure is run on one firm-year. For each of the 998 firms, the [production script](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.1 - Production Batch Tagging Pipeline.py>) takes the most recent usable 10-K filing dated before the privacy hearings of 2018, which is the latest 10-Kfiling before April 10, 2018, selected by filing date rather than fiscal year. This gives **998 filings with 298,651 retained sentences**. Facebook's fiscal 2017 report, filed February 1, 2018, contributes 78, and ResMed's fiscal 2017 report, filed August 4, 2017, contributes 484. ResMed is not named in the hearing, which is what makes it a useful case of a link through the topic. The displayed sentence number is the stored index plus one, so a citation resolves to one stored row.

> **Coauthor note — sample timing.** The selection rule takes the latest available filing in the historical sample and imposes no freshness cutoff.
>
> - Problem: 289 of the 998 selected filings are more than two years old at the hearing date, and the rule does not establish that the 998 firms were S&P 500 constituents in April 2018. Filing dates and ages are retained in the output.
> - To do: before estimating contemporaneous exposure, decide whether to require active firms, contemporaneous index membership, or a maximum filing age.

**5. Calculate similarity scores and standardize.** We score every filing on every topic with the [topic-vector notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/02_topic_centroids_scores.ipynb>). Each retained sentence's cosine to each topic vector is a dot product of unit vectors. For each filing and topic the code averages the **five highest cosines**, or all sentences when fewer remain, and keeps those five sentences as evidence. The saved table holds **2,438,226 filing–topic scores** and **12,190,686 evidence rows**. Raw scores rise with filing length, from a mean of 0.620 in the shortest length decile to 0.681 in the longest, so the [descriptive-analysis notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/07_layer1_descriptives.ipynb>) standardizes each score within its topic and length decile. The deciles and their means and standard deviations use all 21,966 filings pooled across years, not only the 998 selected ones.

The two illustrations show the calculation. Facebook's filing has 78 sentences, so it has 78 cosines to the privacy vector. The five largest are the sentences in the table below, and their mean is 0.7593. With 78 sentences the filing falls in the shortest decile, 1 to 96 sentences, where privacy scores have a mean of 0.6147 and a standard deviation of 0.0296, so its standardized score is $(0.7593-0.6147)/0.0296=4.879$. ResMed's 484 sentences place it in the decile of 406 to 530 sentences, with mean 0.6875 and standard deviation 0.0338.

| Firm | Sentence | Cosine | Retained Item 1 sentence |
|---|---:|---:|---|
| Facebook | 48 | 0.8049 | In particular, we are subject to federal, state, and foreign laws regarding privacy and protection of people's data. |
| Facebook | 47 | 0.7607 | These may involve user privacy, data protection and personal information, rights of publicity, content, intellectual property, advertising, marketing, distribution, data security, data retention and deletion, electronic contracts and other communications, competition, protection of minors, consumer protection, telecommunications, product liability, taxation, economic or other trade prohibitions or sanctions, securities law compliance, and online payment services. |
| Facebook | 57 | 0.7544 | In addition, some countries are considering or have passed legislation implementing data protection requirements or requiring local storage and processing of data or similar requirements that could increase the cost and complexity of delivering our services. |
| Facebook | 56 | 0.7407 | Similarly, there are a number of legislative proposals in the United States, at both the federal and state level, that could impose new obligations in areas affecting our business, such as liability for copyright infringement by third parties. |
| Facebook | 45 | 0.7359 | We are subject to a number of U.S. federal and state and foreign laws and regulations that affect companies conducting business on the Internet. |
| ResMed | 459 | 0.8131 | New laws governing privacy may be adopted in the future as well. |
| ResMed | 468 | 0.7685 | In addition, Congress and some states are considering new laws and regulations that further protect the privacy and security of medical records or medical information. |
| ResMed | 473 | 0.7656 | In addition to data breach notification laws, some states have enacted statutes and rules requiring businesses to reasonably protect certain types of personal information they hold or to otherwise comply with certain specified data security requirements for personal information. |
| ResMed | 469 | 0.7527 | With the recent increase in publicity regarding data breaches resulting in improper dissemination of consumer information, many states have passed laws regulating the actions that a business must take if it experiences a data breach, such as prompt disclosure to affected customers. |
| ResMed | 471 | 0.7497 | Congress has also been considering similar federal legislation relating to data breaches. |

*The five sentences behind each raw score, ordered by cosine to the privacy vector. Facebook's five average to 0.7593 and ResMed's to 0.7699. Against their length deciles, 1 to 96 sentences with mean 0.6147 and standard deviation 0.0296 for Facebook, and 406 to 530 sentences with mean 0.6875 and standard deviation 0.0338 for ResMed, the standardized scores are 4.879 and 2.443.*

The [example verification](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/03 - Logs and Verification/embedding_verification.json>) recomputes both scores from the saved embeddings. Facebook's five sentences include one on copyright liability and one on Internet regulation in general, which shows that closeness in wording is not the same as being about privacy. ResMed has the higher raw score, and Facebook is the more unusual filing relative to filings of its length. Neither value says anything about direction or about economic exposure. The [all-firm score table](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/privacy_firm_scores_before_hearing.csv>) gives the same calculation for all 998 filings.

***c. LLM-based measure***

**6. Prepare the documents as numbered blocks.** We cut each filing's retained sentences into blocks of at most 40 consecutive sentences with the [block-construction notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/03_tagging_blocks.ipynb>), keeping the filing-wide numbering. Document order decides which sentences the model reads together. Across all filings this makes 168,333 blocks. The 998 selected filings make **7,950 blocks**, two for Facebook and 13 for ResMed. No similarity output enters this step or any later one in part c.

**7. Design the judgments.** We use `Qwen/Qwen3.5-4B` with the [tagging helper](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Background Helper Functions/tagging.py>), prompt version `item1-topic-tagging-1.2`, whose [templates](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/01 - Inputs/prompts.md>) are reproduced in Appendix A.4. The three judgments of Section 5.1 are implemented as two calls per block.

a. *Screening.* Pass A shows the block beside all 111 topic labels and asks for the labels that plausibly match, with the instruction to be generous.

b. *Selection.* Pass B shows the same block beside the definition of each candidate topic and asks for every sentence that describes the company's own business in that subject area, citing its number. Generic statements that are not about the company are to be skipped.

c. *Direction.* For each selected sentence Pass B returns one letter. Opportunity when the sentence presents the topic as growth, demand, funding, or an advantage. Threat when it presents a risk, cost, restriction, or competitive pressure. Neutral when the connection is stated without either.

Each record returned is checked by code against its block. The sentence number must be one shown, the topic must be one supplied, and the direction must be one of the three. Duplicate sentence–topic pairs are dropped, and output that hits the generation cap or fails to parse is flagged rather than discarded, so that a missing tag can be told from a failed call. The generation caps are 160 tokens for screening and 512 for confirmation.

The [prompt-development notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/04_tagging_promptbook.ipynb>) refined the design on eight seeded blocks from three filing eras, with every output read before any larger run. Two earlier designs were retired on that reading, a screen over the 14 themes that hid detailed topics inside broad labels, and a screen that cited sentence ranges per topic and truncated its own output at the cap.

**8. Read and tag.** We run the two calls over the 7,950 blocks with the [production script](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.1 - Production Batch Tagging Pipeline.py>). This run focuses on **one topic**. The screen keeps all 111 labels, and the confirmation call is made for topic 68 only when the screen includes it, so no other topic is classified. Every call is logged with its prompt hash and complete output.

<!-- TOPIC68_RUN_STATUS_START -->
The completed run makes **8,789 model calls**, each verified against its recorded prompt, and retains **1,044 privacy tags**. Of these, 682 are threat, 336 neutral, and 26 opportunity. The run records 31 generation-cap hits, and 104 filings have at least one flagged call. For the two illustrations, Facebook receives 15 tags and ResMed 20, all threat, with no flagged blocks. For Facebook the model tags [sentence 52](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_records.md#0001326801-18-000009-sentence-52>) as threat, "Proposed or new legislation and regulations could also significantly affect our business." For ResMed it tags [sentence 471](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_records.md#0001193125-17-248016-sentence-471>) as threat, "Congress has also been considering similar federal legislation relating to data breaches." The [sentence-level records](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_records.md>) keep the original text of every tag.
<!-- TOPIC68_RUN_STATUS_END -->

The leading firms in each direction show what a tag looks like beside its sentence. Total System Services and Facebook rank first and second on threat, and Paycom Software and Fidelity National Information Services rank first and second on opportunity, in the rankings of Section 5.3.

| Firm | Filed | Sentence | Recorded label | Original disclosure sentence |
|---|---|---:|---|---|
| [Total System Services](https://www.sec.gov/Archives/edgar/data/721683/000155837018001043/tss-20171231x10k.htm) | 2018-02-23 | 48 | Threat | In many jurisdictions consumers must be notified in the event of a data breach, and such notification requirements continue to increase in scope and cost. |
| [Facebook](https://www.sec.gov/Archives/edgar/data/1326801/000132680118000009/fb-12312017x10k.htm) | 2018-02-01 | 55 | Threat | The GDPR will include operational requirements for companies that receive or process personal data of residents of the European Union that are different than those currently in place in the European Union, and will include significant penalties for non- compliance. |
| [Paycom Software](https://www.sec.gov/Archives/edgar/data/1590955/000156459018002088/payc-10k_20171231.htm) | 2018-02-14 | 263 | Opportunity | We voluntarily obtain third-party security examinations relating to security and data privacy in accordance with Statement on Standards for Attestation Engagements ("SSAE"), No. 16, Reporting on Controls at a Service Organization. |
| [Fidelity National Information Services (FIS)](https://www.sec.gov/Archives/edgar/data/1136893/000113689318000011/a10-k2017.htm) | 2018-02-22 | 217 | Opportunity | The Company has adopted a comprehensive global privacy program to assess and manage these evolving risks, including contract terms to comply with this new law. |

*Evidence behind the leading directional ranks. Company links lead to the original filings, and sentence numbers refer to the retained, numbered Item 1 text. The [table data](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_evidence_table.csv>) and the [complete examples](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_directional_examples.md>) keep all accepted tags, numbered input blocks, and recorded responses for the four firms.*

The two threat sentences state a cost or a penalty, so the label is observable in the wording. The two opportunity sentences describe a security examination and a compliance program. They establish a privacy-related response, not a stated gain. Three of the four firms are not named in the hearing and sit in industries other than Facebook's, so the shared topic finds links that name matching and industry codes would miss.

> **Coauthor note — direction labels.** Opportunity is rare and its leading cases do not meet the prompt's own definition.
>
> - Problem: of 1,044 tags, 26 are opportunity, and the top-ranked opportunity sentences describe compliance programs and security audits, which the prompt defines as neither growth nor demand nor advantage. Some threat tags also sit on neighboring subjects, such as Total System Services' debit interchange fees. No tag has been checked by a human.
> - To do: complete the human review of procedure 11 with direction as one of its fields, and decide whether compliance responses are to count as opportunity, as neutral, or as a fourth category.

**9. Aggregate the tags and attach the hearing.** We aggregate with the [assembly script](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.2 - Panel Assembly and Empirical Descriptives.py>), which refuses to publish until every scheduled block has a result, reconstructs each prompt and its hash, and parses the saved responses again. For each firm it counts distinct privacy-tagged sentences and their split into opportunity, threat, and neutral. The related indicator is one when at least one tag is retained. A filing with clean calls and no tag receives zero, and a filing with flagged calls and no tag is recorded as unknown, since its count may be incomplete. Direction shares divide each direction's count by the tagged total and are undefined at zero. A further share divides tagged sentences by all retained sentences of the filing, which is the per-100 form used for the rankings in Section 5.3.

Across the 998 firms, **129 are related**, 782 receive zero, and 87 are unknown. The final row of the [hearing–firm table](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/hearing_firm_privacy_panel.csv>) joins these counts and shares to the firm's standardized similarity, its selected filing and filing date, topic 68, and the April 10 hearing identifier.

***d. Both measures***

**10. Combine similarity and direction into an index.** We compute the index of Section 5.1 with the [combined-score script](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.3 - Similarity-Weighted Directional Scores.py>). It joins each accepted tag to its saved sentence embedding, checks the wording, recomputes the cosine to the privacy vector in full precision, and sums the weights by direction over all retained sentences of the filing. No new model call is made. The index was added after both measures had run and was not part of the original design. It is available for the **894 filings without flagged calls**, and the 104 flagged filings receive missing values because their counts may be incomplete. All 1,044 weights are positive, so the zero bound binds nowhere in this run.

For Facebook, the 15 threat sentences among 78 have a mean weight of 0.7096, so the threat index is $(100\times15/78)\times0.7096=13.65$. Paycom's eight opportunity sentences among 300 have a mean weight of 0.5485, giving $(100\times8/300)\times0.5485=1.46$. The four leading firms keep their ranks under weighting.

| Firm | Unweighted threat | Threat index | Unweighted opportunity | Opportunity index |
|---|---:|---:|---:|---:|
| Total System Services | 24.14 | 16.03 | 0.00 | 0.00 |
| Facebook | 19.23 | 13.65 | 0.00 | 0.00 |
| Paycom Software | 1.67 | 1.25 | 2.67 | 1.46 |
| Fidelity National Information Services (FIS) | 9.27 | 6.16 | 1.16 | 0.81 |

*Unweighted values are directional tags per 100 retained sentences. Index values weight each tag by its cosine with the same denominator. The [four-firm table](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_weighted_firm_examples.csv>) carries counts and mean weights, and the [weighted panel](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/hearing_firm_privacy_weighted_panel.csv>) carries all 998 firms.*

[THIS PART SHOULD BE UPDATED AFTER MEETING]

Sentence pairs within one firm show what the weight does and where it fails. For Total System Services, the breach-notification sentence carries 0.740 and a neighboring sentence on debit interchange fees 0.591, so the weight favors the privacy cost over the neighboring subject. For Facebook, the GDPR sentence carries 0.686 and a sentence on copyright obligations 0.740, so an off-topic tag keeps the larger weight. For Paycom and FIS, weighting does not turn a compliance program into a business gain. The [sentence table](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_weighted_sentence_examples.md>) keeps the wording, labels, and contributions.

> **Coauthor note — the weight is unchecked.** The index assumes that a tag's cosine tracks how central its sentence is to the topic, and the Facebook copyright case shows the assumption can fail.
>
> - Problem: no human has rated the tagged sentences, so there is no evidence that the weighting improves on the unweighted share.
> - To do: in the human review, rate each tagged sentence as central, peripheral, or off-topic and compare the ratings with the cosines. Rank firms by the unweighted share and by the index and read the firms that move most. Report the index beside the unweighted share and not in its place until the first test passes.

**11. Validate the measures and check their agreement.** We check agreement between the two measures on the 894 filings without flagged calls. The left panel of the figure compares standardized similarity between the 782 filings without a privacy tag and the 112 with one. The right panel orders firms by standardized similarity, divides them into five groups of equal size, and shows the share of firms in each group with at least one tag.

<!-- TOPIC68_EVALUATION_START -->
From the lowest similarity group to the highest, the shares are 0.0, 2.8, 4.5, 6.7, and 48.6 percent. In the lowest group 0 of 179 firms carry a tag, and in the highest group 87 of 179 do. The rank correlation between standardized similarity and the share of retained sentences tagged is 0.461. Because neither measure enters the other, the rise across the groups is evidence that the two measures converge on the same firms, and the half of the top group without a tag is where similarity finds closeness that the model does not read as the firm's own business.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_privacy_measure_agreement.svg" alt="Privacy similarity and LLM evidence across firms"></p>

*Privacy-measure agreement. Each observation is one firm's latest available filing before April 10, 2018. Left: boxes show the middle 50 percent and median of standardized similarity, with whiskers to observations within 1.5 interquartile ranges and more distant points hidden. Right: bars show the percentage of firms with any accepted privacy tag within each similarity quintile, with all firms in the quintile as the denominator. The [group counts and score ranges](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/03 - Evaluation and Figures/privacy_agreement_quintiles.csv>) reproduce the bars. Filings with flagged calls are excluded. Absence of a tag is a model outcome, not proof of irrelevance.*
<!-- TOPIC68_EVALUATION_END -->

The assembly script also exports 100 confirmed sentences and 50 unconfirmed probes for human review, with the relevance and direction fields left blank.

> **Coauthor note — human review and the screening audit.** Neither check has produced a result.
>
> - Problem: the review sheet has not been coded, so no tag has been checked by a human for relevance or direction, and the agreement above is the only validation of the LLM-based measure. A no-screen audit was run on 60 sampled blocks, but only two of them held a privacy tag and the screen missed one, which is too few blocks to estimate what the screen misses.
> - To do: code the review sheet, report agreement with the model as kappa for relevance and for direction, and rerun the no-screen audit on enough blocks to hold at least 30 confirmed privacy tags.

### 5.3. Research Outputs

The outputs let a researcher move from a hearing–firm connection to the specific text and computation supporting it. They distinguish similarity results for all filings, the privacy-specific LLM assessment, and the new combined indices:

| Output | What a row or file represents | Research use |
|---|---|---|
| Prepared sentence table and aligned embeddings | One retained Item 1 sentence with its filing, firm, fiscal year, and index; one matching vector per row. | Retrieve evidence, recompute similarity, and examine preprocessing choices. |
| Topic index and fixed vectors | One definition-and-evidence representation per topic, with its supporting sentence count. | Identify the common reference used across firms and years. |
| Full-sample similarity and evidence tables | One score per filing and topic, plus up to five contributing sentence references. | Compare semantic relatedness and inspect what produces a high score. |
| Privacy classification records and call logs | Accepted sentence-level tags, screening results, raw responses, prompts, hashes, and processing flags for the selected filings. | Inspect relevance and direction and distinguish a model decision from a failed call. |
| Hearing–firm privacy table | One row per selected firm, connecting its preceding filing to the April hearing through topic 68. | Compare similarity, presence of tagged evidence, sentence counts, direction, and disclosure age within the same sample. |
| Audit and human-review files | Direct privacy confirmations on the sampled blocks and sentences prepared for independent review. | Examine screening omissions and evaluate substantive judgments separately. |
| LLM ranking and cross-industry examples | Separate firm rankings by threat and opportunity sentences as shares of the disclosure, with a source-evidence table and explicit name and industry comparisons. | Locate connections that simple matching rules omit and inspect both supporting passages and questionable model tags. |
| Similarity-weighted directional panel and sentence contributions | Separate threat and opportunity indices for each eligible filing, plus every accepted sentence's cosine, label, and contribution. | Compare the combined measure with unweighted counts and trace a score to its evidence; retain missing scores for flagged filings. |

The first four descriptive exhibits use the similarity results for all filings to examine firm, industry, and time patterns. They use the [saved score calculations](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/07_layer1_descriptives.ipynb>). Two further figures use the completed LLM privacy assessment to rank threat and opportunity discussion separately. The sentence tables and worked calculations in Section 5.2 trace the evidence behind these directional measures and the combined indices. Three-digit NAICS classifications are available for 1,060 of the 1,061 firms, covering 84 industries. Each firm's industry is fixed at its most frequent NAICS3 code in the linked reference data. The first three figures use the full table, whose fiscal-year metadata span 1992–2026; the time-series figure explicitly restricts its display to 1995–2025. The LLM exhibits use the selected filings preceding the April 2018 hearing.

***Outputs from Similarity-based measure***

**1. Which firms are exposed to which topics?** The first figure displays the 15 firm–topic pairs with the highest mean standardized similarity, requiring at least three filings per pair. Each row names a firm and a topic, and it is plotted at the mean of that firm's standardized filing scores for that topic. Averaging several filings reduces reliance on a single disclosure.

Embarq's connection to the Universal Service Fund has a mean of 5.612, and T-Mobile's connection to spectrum policy has a mean of 5.058. United Airlines and Essential Air Service score 4.481, and Norfolk Southern and Positive Train Control and Rail Safety Legislation score 4.333. Every one of the 15 pairs is a connection a reader could have named in advance. Telephone and wireless carriers sit with the Universal Service Fund, spectrum policy, and broadband deployment, railroads and a rail equipment maker with Amtrak funding, passenger rail, and train control, and airlines with the Essential Air Service and the next-generation air traffic system. 

This means the similarity-based score finds meaningful exposure without seeing an industry classification or any other pre-existing link.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_relevance_top_pairs.svg" alt="Firm–topic pairs with the highest average standardized similarity"></p>

*Highest-scoring firm–topic pairs. Points show mean standardized similarity across a firm's filings for one topic, with at least three filings required. Standardization uses the topic and filing-length decile. The figure covers all 111 topics and does not use the LLM privacy classifications.*

**2. Which industries are most exposed to the hearing topics overall?** A few high-scoring firms cannot establish whether the collection of topics systematically relates to different industries. The second figure first averages each firm's standardized scores across filings and all 111 topics, then averages those firm values within industries. Each firm contributes equally. The display includes the eight highest and eight lowest industry means among industries containing at least eight firms.

Telecommunications has a mean of 0.670, with an approximate 95-percent interval of [0.401, 0.938], and Transportation Equipment has a mean of 0.424, with an interval of [0.224, 0.624]. Bars locate these industry averages, and whiskers show uncertainty calculated across firms. Positive values indicate greater average similarity to this collection of hearing topics. Negative values indicate lower average similarity, not an absence of relevant subjects. The ordering follows the committees that held the hearings. Our sample is the House Science and Senate Commerce committees, whose agenda is primarily around science, technology, transportation, and communications. The figure shows the most exposed industries are telecommunications, transportation equipment, mining support, information services, and computer and electronic products. The least exposed are clothing retail, apparel manufacturing, food services, insurance, and securities, whose business descriptions have little to say about that agenda. 

This means the score, averaged over all topics, captures the nature of the hearing sample rather than a general tendency of some industries to use regulatory language.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_relevance_industry_exposure.svg" alt="Average standardized similarity across industries"></p>

*Industry-wide relatedness. Bars show the mean of firm-level averages across filings and all topics; whiskers are approximate 95-percent intervals across firms. Parentheses give firm counts. The comparison weights firms equally and requires at least eight per industry.*

**3. Which topics are closest within each industry?** An industry-wide average can conceal a strong connection to a small number of subjects. The third figure separates eight industries and displays the three topics with the highest mean standardized filing scores within each. The notebook specifies the industries, while the calculated scores determine their leading topics. Each point locates an industry–topic mean.

Telecommunications scores highest on the Universal Service Fund (3.432), spectrum policy (3.093), and broadband deployment and infrastructure (2.902). Utilities scores highest on Smart Grid and Grid Modernization (1.642), the Clean Power Plan (1.538), and Renewable Energy Technologies and Storage (1.284). Air Transportation's leading matches include Essential Air Service (4.173), the Next Generation Air Transportation System (3.858), and aviation safety and certification policy (3.611).

These patterns permit inspection of whether the measure distinguishes recognizable subjects within industries. Here the averages are taken directly across filings, so a firm with more filings receives more weight than one with fewer. This differs from the preceding industry-wide comparison and should be considered when interpreting the values.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_relevance_industry_topics.svg" alt="Highest-scoring topics within selected industries"></p>

*Industry-specific subjects. Each industry block lists its three topics with the highest standardized similarity, averaging across filings. Industry selection is fixed in the notebook; topic selection follows the scores. Firms with more filings contribute more observations.*

**4. How does industry–topic relatedness change over time?** A pooled average does not reveal whether a connection is persistent or concentrated in particular years. The fourth figure follows six industry–topic pairs, selecting each industry's highest-scoring topic from the preceding calculation. Each panel plots fiscal year horizontally and the mean standardized score of that industry's filings in the year vertically.

Telecommunications' similarity to the Universal Service Fund increases from 2.556 in 1995 to 3.727 in 2025, reaching 4.203 in 2009. Utilities' similarity to Smart Grid and Grid Modernization rises from 1.107 to 2.240 over the displayed period. These movements describe changes in disclosed content and filing composition relative to the common reference. They do not establish a change in congressional attention or a policy's causal effect.

The dashed zero line is the pooled standardization reference, not a separately computed all-industry average for each year. Topic representations stay fixed, and labels referring to particular legislation function as retrospective categories when applied to earlier filings. The [figure export script](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/render_relevance_figures.py>) reproduces the notebook's calculations while correcting the earlier captions' date range and zero-line description.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_relevance_industry_trends.svg" alt="Industry–topic similarity over fiscal years"></p>

*Changes within industry–topic pairs. Lines show annual means for six pairs over fiscal years 1995–2025. The dashed line is the fixed zero reference from pooled topic-and-length standardization. Both changing disclosures and the composition of filing firms can change the observed series.*

***Outputs from LLM-based measure***

**5. Which firms describe privacy as a threat or an opportunity?** The following figures rank firms using the unweighted directional shares defined in Section 5.1 and calculated in Section 5.2. They show the extent of threat and opportunity discussion separately.

Both rankings use the **894 filings without processing flags**. The 104 filings with flagged calls remain in the full output but are excluded from these figures because their counts may be incomplete. The filing selected for each firm is its latest available disclosure filed before April 10, 2018. This date restriction keeps post-hearing disclosures out of the comparison; it does not establish that the firm was a contemporaneous S&P 500 constituent. The topic representation remains the retrospective category described in Section 5.2.

The threat figure displays the highest 15 values among the 101 firms with at least one threat tag. Total System Services ranks first, with 21 of 87 sentences tagged as threats (24.1 percent); Facebook follows with 15 of 78 (19.2 percent); Fidelity National Information Services ranks third with 24 of 259 (9.3 percent). ResMed ranks eleventh at 4.1 percent, and AmerisourceBergen ranks fourteenth at 3.8 percent.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_privacy_llm_threat.svg" alt="Firms ranked by privacy threat discussion"></p>

*Privacy threat discussion. Bars show threat-tagged sentences as a percentage of all retained sentences in the selected filing, ordered from highest to lowest. The figure displays the top 15 among 894 filings without processing flags. Neutral and opportunity tags do not contribute to the numerator. Counts are recorded model outputs, not validated measures of economic harm.*

Opportunity tags are much less frequent: **16 sentences across seven firms** in the same sample. The second figure displays all seven firms with positive values. Paycom Software ranks first with eight of 300 sentences tagged as opportunities (2.7 percent), followed by Fidelity National Information Services with three of 259 (1.2 percent). Each remaining firm has one accepted opportunity tag. The figure uses its own horizontal scale because the opportunity shares are considerably smaller; their precision and meaning should be assessed from the underlying passages.

<p align="center"><img src="../R%20-%20Results/R1.1%20-%20Figures/R1.1.2%20-%20T%20-%20Three%20Step%20Text%20Analysis%20Pipeline/T3%20-%20Topic%20Relevance%20and%20Corporate%20Disclosure/fig_privacy_llm_opportunity.svg" alt="Firms ranked by privacy opportunity discussion"></p>

*Privacy opportunity discussion. Bars show opportunity-tagged sentences as a percentage of all retained filing sentences, ordered from highest to lowest. All seven firms with positive counts are displayed; the other 887 filings without processing flags have zero accepted opportunity tags. The denominator and eligibility rules match the threat figure, while the horizontal scale differs. Neutral and threat tags do not contribute to the numerator.*

Applying the name and industry comparisons described in Section 5.2, nine of the 15 displayed threat firms and six of the seven opportunity firms satisfy neither rule. The [saved checks](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/03 - Logs and Verification/llm_figure_verification.json>) and [directional ranking tables](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/privacy_llm_ranking.csv>) record the comparisons. These are additional candidate connections and not independently validated omissions, since the name search is limited to documented aliases and matching Facebook's industry is one specific industry rule. This means the LLM-based measure finds topic (privacy) related exposure well beyond the firm that testified at the hearing and the industry it belongs to, in payment processors, payroll software, financial technology, and medical devices, which is the broader affected group the Section 5 overview describes.

---

## 6. [TO BE UPDATED] Toy Example: Empirical Strategy and Analyses

This section shows how the outputs of the three steps enter one empirical design. It is a toy example. It fixes one topic, takes the firm-year as the unit of analysis, and asks whether the stock market's reaction to congressional hearings on that topic depends on how exposed a firm is to the topic and on the direction legislators took. The purpose is to show which variable comes from which step, at which unit, and in which order in time.

### 6.1. Unit of Analysis and Variables

The unit is a firm $f$ in year $t$ for one fixed topic $k$. Three variables are needed. Two come from the pipeline, one from each side of the bridge built in Section 5, and one comes from market data.

**Topic relevance from Step #3, $E_{fk,t^-}$.** This is the firm's relevance to topic $k$, measured on the latest 10-K filed before the hearings on topic $k$ held in year $t$. It is one value per firm-year. In its simplest form it is the standardized similarity score of Section 5.1, which exists for every filing and every topic. Where the LLM-based measure has been run, it can instead be the related indicator, the count of tagged sentences, or the threat and opportunity indices. Because the topic vector is fixed, relevance is never recomputed for a hearing. The hearing dates only decide which filing is read, and one filing serves every hearing that falls before the next filing.

**Legislators' direction from Step #2, $S_{kt}$.** This is the direction legislators took on topic $k$ across the hearings held in year $t$. The stance records of Section 4 carry hearing dates, so the topic by Congress panel aggregates to the year by assigning each record to the year of its hearing. $S_{kt}$ can be the support count, the concern count, their shares, or the net stance. It is one value per topic and year, and therefore the same for every firm in that year. The variation in how each hearing discussed the topic lives here, summed into the year, and never touches the firm side.

**Cumulative abnormal return from market data, $CAR_{ft}$.** This is the firm's abnormal return accumulated over the event windows around the hearings on topic $k$ held in year $t$, summed across those hearings. The event window and the expected-return model are the researcher's choices and not the pipeline's.

The running example gives one row's pipeline inputs. For Facebook and consumer data privacy, the filing before the April 2018 hearing has a standardized similarity of 4.879, and the LLM-based measure finds 15 threat-tagged sentences among its 78, a threat share of 1.0. On the topic side, the 115th Congress holds 55 stance records on consumer data privacy legislation from 17 hearings, 34 support and 21 concern. Assigning those records to calendar years by hearing date gives the two annual values of $S_{kt}$ that the row would use.

### 6.2. Specification

With firm and year fixed effects, the design is

$$
CAR_{ft}=\alpha_f+\gamma_t+\beta_1\,E_{fk,t^-}+\beta_3\,\big(E_{fk,t^-}\times S_{kt}\big)+\varepsilon_{ft}.
$$

The firm effect $\alpha_f$ absorbs the firm's average return response, and the year effect $\gamma_t$ absorbs everything that happened to all firms in that year, including the average market reaction to that year's hearings. $\beta_1$ is the return response to being exposed to the topic when hearings on it occur, averaged over the directions they carried. It is identified because exposure moves within a firm across years as its filings change.

$S_{kt}$ does not appear on its own. With one topic it takes one value per year, so the year effect absorbs it completely. The legislators' direction therefore enters only as the slope on relevance. $\beta_3$ answers whether the return response of exposed firms depends on the direction legislators took, and it is identified from the comparison across years with different directions, within firms, among firms with different exposure. If $S_{kt}$ is the share of concern, a negative $\beta_3$ means that exposed firms lost more when Congress leaned toward concern and nothing when it leaned toward support.

Two refinements use what the pipeline already separates. First, $S_{kt}$ can be split into its support and concern counts, so that $\beta_3$ becomes one coefficient for each and no sign is imposed by a net formula. Second, once the LLM-based measure has been run on every filing, $E_{fk,t^-}$ can be split into its threat and opportunity parts. The product of threat exposure and congressional concern is the case where both sides point the same way, and it is where the largest negative return response should sit.

---

## 7. Research Outputs, Reproducibility, and Application to Future Research

The project contributes a documented procedure for turning unstructured text into inspectable research measures. Sections 3–5 connect each transformation to its inputs, code, intermediate records, and outputs. This allows researchers to examine a particular decision or adapt one stage while retaining the evidence needed to assess its consequences.

The completed assets have different scopes:

| Asset | Completed coverage | Interpretation and current limits |
|---|---|---|
| Hearing summaries | 2,352 hearings, with intermediate summaries and logs for 29,264 model calls. | Independent C-SPAN abstracts supply comparisons for 351 hearings; these comparisons do not establish complete factual accuracy. |
| Topic and stance datasets | A codebook of 111 topics under 14 themes; extracted topics for 2,352 hearings; primary classifications for 2,342; and 32,385 stance records. | Legislator stances are support or concern. The saved records include 2,406 assignments to “other,” and substantive extraction and assignment errors remain inspectable. |
| Similarity across annual firm disclosures | 21,966 usable filings for 1,061 firms, compared with all 111 topics. | The fixed topic representations support retrospective comparisons across firms and years. These scores describe semantic relatedness. |
| Privacy-specific directional assessment and combined scores | One pre-hearing filing for each of 998 firms; final combined scores for 894 unflagged filings. | Firm sentences can be classified as opportunity, threat, or neutral. The present run is a snapshot for topic 68; longitudinal directional scores and independent human validation remain unfinished. |

**Reproduction and reuse.** The repository links the manuscript to parsing and aggregation code, prompt templates, worked inputs, saved responses, and verification scripts. Source identifiers and intermediate records let researchers locate an attribution, category assignment, or score contribution. Model and prompt versions, generation settings, and input hashes document the computation. Reproducing a saved transformation and establishing the substantive accuracy of its output remain separate tasks.

Researchers adapting the workflow to a new corpus would specify the relevant document structure, actors, fields, and units of analysis; inspect the resulting inputs and extractions; and establish suitable evaluation references before deployment. Coding agents can help inspect and adapt these explicit components. Their changes can be reviewed against the source evidence and recorded checks rather than treated as validation by themselves. This supports the project's aim of lowering the technical burden of adopting and extending the method.

**Remaining work and research applications.** Extending the firm analysis over time requires applying the directional extraction to successive annual filings using a consistent topic reference and measurement procedure. Extending it beyond privacy requires classifying the other topics. Independent human review must assess relevance and direction, including screening omissions and ambiguous compliance statements. The primary-topic tie-breaking alternatives remain proposals pending the decision documented in Appendix B.

The resulting panels could support research on how firms' disclosed threats and opportunities change as policy attention evolves. Studying effects on innovation or other firm outcomes would additionally require outcome data, explicit sample and timing rules, and an appropriate research design. Those analyses are prospective applications of the measurements, not results established by the current worked example.

---

# Appendix

## Appendix A. Prompts

The full templates are available with the worked inputs for each stage: [T1 summarization](<../T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.X - Worked Example/README.md#map-prompt>), [T2 topic and stance extraction](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/01 - Inputs/prompts.md>), and [T3 relevance and direction](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/01 - Inputs/prompts.md>). The prompts for all three stages and for codebook drafting are reproduced below as they appear in the code; curly braces mark the substituted inputs.

### Appendix A.1. Text Summarization Prompts

#### 1. Prompt for Map Stage

```python
# MAP SYSTEM PROMPT
"""
You are an expert in text summarization with a working knowledge of United States congressional hearings. You report only what the transcript states.
"""

# MAP PROMPT
"""
Below is one consecutive segment of a congressional hearing transcript. Each speaking turn is labelled with the speaker.

Summarize this segment in about 150 words. Cover:
- the subjects raised, and what was said about them;
- the position each named speaker takes, attributed to that speaker;
- any numbers, dollar amounts, dates, and bill or act names, copied exactly as they appear.

If the segment is procedural or ceremonial and contains none of these, say so in one sentence.

--- SEGMENT ---
{text}
--- END OF SEGMENT ---

Write only the summary of the segment above.
"""
```

#### 2. Prompt for Collapse Stage

```python
# COLLAPSE SYSTEM PROMPT
"""
You are an expert in text summarization with a working knowledge of United States congressional hearings. You condense summaries without adding to them.
"""

# COLLAPSE PROMPT
"""
Below are summaries of consecutive segments of one congressional hearing, in the order they occurred. They are already summaries, not transcript.

Condense them into one account of about 200 words that keeps the named speakers, their positions, and the numbers and legislation. This is a middle portion of the hearing, so do not write an overall conclusion about the hearing.

--- SEGMENT SUMMARIES ---
{text}
--- END ---

Write only the condensed account.
"""
```

#### 3. Prompt for Reduce Stage

```python
# REDUCE SYSTEM PROMPT
"""
You are an expert in text summarization with a working knowledge of United States congressional hearings. You write from the summaries given and add nothing that is not in them.
"""

# REDUCE PROMPT
"""
Below are summaries of every segment of one congressional hearing, in order. They are already summaries, not transcript.

Write a single summary of the hearing as a whole, in about 200 to 250 words. Cover:
- what the hearing was about;
- the main subjects, the most heavily discussed first;
- the position each named speaker took;
- any point where speakers took opposing positions, naming both sides;
- the key numbers and the legislation referred to, exactly as given.

Where the segment summaries do not establish one of these, leave it out rather than inferring it.

--- SEGMENT SUMMARIES ---
{text}
--- END ---

Write only the summary of the hearing, in about 200 to 250 words, as continuous prose.
"""
```

### Appendix A.2. Topic Extraction Prompts

Both tracks share one system prompt and are rendered by the [stance helper](<../T - Three Step Text Analysis Pipeline/T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/stance.py>). The recorded versions are `summary-topics-0.2-dev` for Track 1 and `stance-extraction-0.3-dev` for Track 2.

#### 1. Shared System Prompt

```python
# SYSTEM PROMPT (Track 1 and Track 2)
"""
You are an expert reader of United States congressional hearing transcripts. You report only what the text states.
"""
```

#### 2. Track 1 Prompt for Hearing Summaries

```python
# TRACK 1 PROMPT ({max_topics} is 5; {summary} is the final hearing summary)
"""
Below is a summary of one United States congressional hearing.

Task: list the main topics the hearing covered, ordered from most to least central.

A topic is a short and specific neutral noun phrase: the policy, program, regulation, technology, practice, or budget item itself; never directional wording; name the specific object, not the agency or field around it. An agency, company, or country is never a topic by itself; name the policy object involving it. A bill counts as a topic by its subject or name, never as a bare bill number such as "H.R. 1". A bare number or amount is never a topic. Entities mentioned only as examples, comparisons, or asides are not topics.

List at most {max_topics} topics. Include a topic only if the hearing gave it substantial attention — most summaries support 2 to 4 topics, and padding to {max_topics} is worse than stopping early. Every major subject of the hearing should appear.

--- SUMMARY ---
{summary}
--- END OF SUMMARY ---

Return only a JSON list of topic strings, most central first. Your very first output character must be [.
"""
```

#### 3. Track 2 Prompt for Legislator Turns

```python
# TRACK 2 PROMPT ({speaker} is the honorific and surname; {numbered} is the numbered turn or window)
"""
Below is one speaking turn by a member of Congress, split into numbered sentences.

Task: find every sentence in which the member takes a directional position on a policy object, and return one record per position.

A record has three fields:
- "sentences": the sentence number(s) expressing the position (1-3 consecutive numbers);
- "topic": the policy object, as a short and specific neutral noun phrase (the policy, program, regulation, technology, practice, or budget item itself; never directional wording; name the specific object, not the agency or field around it);
- "stance": "support" if the member endorses, advocates, or urges adoption, funding, or expansion of the topic; "concern" if the member expresses worry, criticism, or objection toward the topic, or urges its restriction, delay, or scrutiny.

The stance is toward the topic exactly as you phrase it. Before returning a record, check that it reads sensibly as "the member supports [topic]" or "the member is concerned about [topic]". If the topic is a problem or harm, the stance toward it is "concern", never "support".

The topic must be the object the member takes a position ON. Entities mentioned only as examples, comparisons, or asides are not topics, and a bare number or amount is never a topic. If several consecutive sentences express the same position on the same topic, return one record covering them, not one record per sentence.

Example: "Youth vaping is an epidemic we cannot ignore." -> {"sentences": [n], "topic": "youth e-cigarette use", "stance": "concern"}
Example: "This bill funds the research our labs badly need." -> {"sentences": [n], "topic": "research funding bill", "stance": "support"}

Do not return records for: procedure (recognitions, time, the record), courtesies, introductions, logistics, questions asked without an expressed position, or factual statements without evaluation. If no sentence takes a directional position, return an empty list. When in doubt, do not extract.

--- TURN (Speaker: {speaker}) ---
{numbered}
--- END OF TURN ---

Return only a JSON list of records. Your very first output character must be [.
"""
```

### Appendix A.3. Codebook Drafting Prompt

Version `codebook-draft-0.1`, from the [drafting notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/09_codebook_draft.ipynb>). `{members}` lists the cluster's phrases with their mention counts; `{n1}` and `{n2}` list the leading phrases of the two nearest clusters.

```python
# CODEBOOK SYSTEM PROMPT
"""
You are helping construct a topic codebook for the analysis of United States congressional hearings. You use only the phrases provided; you never invent content.
"""

# CODEBOOK PROMPT
"""
Below are the member phrases of one topic cluster (most frequent first), followed by the top phrases of its nearest neighboring clusters.

CLUSTER MEMBERS (phrase — mentions):
{members}

NEIGHBOR 1 (a different topic): {n1}
NEIGHBOR 2 (a different topic): {n2}

Task: draft the codebook entry for this cluster.
- "label": a short, specific, neutral noun phrase naming the topic. Never directional wording (no ban/support/expand/protect); name the policy object, not a stance toward it.
- "definition": one sentence stating what belongs in this topic.
- "exclusion_notes": one or two short notes on how this topic differs from the two neighbors shown.
- "exemplars": exactly 5 phrases copied VERBATIM from the CLUSTER MEMBERS list above (or all of them, if fewer than 5 are listed).

Return only a JSON object with exactly those four fields. Your very first output character must be {.
"""
```

### Appendix A.4. Topic Relevance Prompts

Version `item1-topic-tagging-1.2`, rendered by the [tagging helper](<../T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.X - Background Helper Functions/tagging.py>). `{numbered}` is one block of up to 40 filing sentences with their filing-wide numbers. `{topics}` lists all 111 topics as `[id] label` lines in Pass A, and the candidate topics as `[id] label — definition` lines in Pass B.

```python
# RELEVANCE SYSTEM PROMPT (Pass A and Pass B)
"""
You are an expert reader of corporate 10-K filings with a working knowledge of United States science and technology policy. You report only what the text states.
"""

# PASS A PROMPT (topic screen)
"""
Below are numbered consecutive sentences from the Business section (Item 1) of one company's 10-K annual report, followed by a list of policy topics drawn from congressional science-committee hearings.

--- SENTENCES ---
{numbered}
--- END OF SENTENCES ---

--- TOPICS ---
{topics}
--- END OF TOPICS ---

A topic matches when at least one specific sentence describes a part of this company's business that falls in the topic's subject area — its products, services, technologies, inputs, customers, or the regulations it operates under. The sentence does not need to mention any law, agency, or hearing. Be generous: include plausible matches. Do not include a topic on the strength of generic statements that are not about this company's business.

Answer with only a JSON list of the matching topic ids:
[<topic id>, <topic id>]

If no topic matches, answer [].
"""

# PASS B PROMPT (confirmation and direction)
"""
Below are numbered sentences from the Business section (Item 1) of one company's 10-K annual report, and a list of policy topics with definitions.

--- SENTENCES ---
{numbered}
--- END OF SENTENCES ---

--- TOPICS ---
{topics}
--- END OF TOPICS ---

Find every sentence that describes this company's business in a topic's subject area. The sentence does not need to mention a law, an agency, or a hearing. Skip generic statements that are not about this company. A sentence may match several topics.

For each match, output one record: [sentence number, topic id, direction]. The direction is one letter:
- "O" — the sentence presents it as growth, demand, funding, or an advantage for the company
- "T" — the sentence presents it as a risk, cost, restriction, or competitive pressure
- "N" — neither: the connection is stated without either

Use only sentence numbers shown above and topic ids from the list.

Answer with only a JSON list of records:
[[<sentence number>, <topic id>, "O"]]

If nothing matches, answer [].
"""
```

## Appendix B. Primary-Topic Tie Breaking

> **Coauthor note — proposed primary-topic tie-breaking rule and sensitivity check; not yet implemented.** The current code resolves equal maximum counts through table ordering. A comparison using the saved assignments identifies ties in 976 of the 2,342 classified hearings.
>
> **Recommended rule:** retain the category with the largest Track 1 phrase count; when counts tie, choose the tied category containing the highest-ranked original phrase. Retain a tie indicator and the competing categories so that the ambiguity remains visible. Track 1's prompt orders phrases by their centrality to the hearing, so this criterion is consistent with identifying the hearing's principal subject. This rank is the model's ordering, not the order in which subjects first appear in the transcript. For the Zuckerberg hearing, category 68 would win because it contains rank 1, while category 93's best rank is 2.
>
> **Role of Track 2:** use its record counts as a sensitivity check. An alternative rule would select the tied category with the most assigned support and concern records combined, falling back to Track 1 rank if those counts also tie. Track 2 captures legislators' expressed positions, excludes witness testimony and statements without an extracted stance, and allows one legislator to contribute several records. Using it to select the primary topic would therefore emphasize evaluative activity by legislators and would introduce stance extraction and assignment errors into the hearing classification. That emphasis may suit a question about legislators' positions, but it differs from identifying the hearing's overall subject.
>
> **Comparison using saved outputs:** Track 2 counts give a unique winner in 675 of the 976 tied hearings; 409 of those winners differ from the highest-ranked Track 1 choice. The remaining 301 hearings would require the fallback. For the Zuckerberg hearing, Track 2 gives privacy 13 records and online advertising 11, so both approaches select privacy. Agreement in this example does not establish which rule is more accurate across the corpus.
>
> **Action after agreement:** implement the chosen rule and retain the tie information, then regenerate the primary labels and the CAP analyses and figures that depend on them. The recommended Track 1 rank rule would change 655 current primary classifications. The manuscript's reported results still describe the existing implementation; neither the proposed selection rule nor the sensitivity procedure has been incorporated into the production pipeline.
