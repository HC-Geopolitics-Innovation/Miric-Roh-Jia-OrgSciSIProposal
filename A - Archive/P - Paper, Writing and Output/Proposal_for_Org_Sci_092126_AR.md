# Proposal For Organization Science

# Data Bottlenecks and Enabling Research in New Domains by Engineering AI-Enabled Research Pipelines

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

To further concretely show exact step of process, we use *Facebook, Social Media Privacy, and the Use and Abuse of Data* (`CHRG-115shrg37801`), featuring Mark Zuckerberg's testimony on April 10, 2018, as a running example. This joint hearing of the Senate Judiciary and Commerce committees examined Facebook's handling of user data following the Cambridge Analytica revelations. Its stored text contains 243,434 words (385 page in PDF document), including written material appended to the hearing record. The linked [worked example](<../T1 - Text Summarization/T1.X - Worked Example/README.md>) provides the source, parsed records, exact model inputs, and recorded outputs. It illustrates the intermediate collapse stage and includes a matched C-SPAN abstract.

**1. Parse the transcript into speaker records.** We downloaded the hearing transcript and its accompanying MODS metadata through GovInfo's API, then extracted the fixed-width text from the transcript's HTML wrapper. Our goal is to capture the hearing's overall themes while identifying the regulatory concerns voiced by legislators to capture regulatory concerns in subsequent steps. This requires distinguishing legislators' contributions from witness testimony and retaining the exchanges that give those contributions context. We therefore treat the *speaker turn* as the basic unit to preserve.

The downloaded text does not provide separate, labeled records for each turn. We recover this structure from a recurring formatting pattern: paragraphs begin with at least four spaces, and speaking turns open with a title and surname, such as `Chairman Grassley.` or `Mr. Zuckerberg.` in this hearing. Python reconstructs paragraphs from the indentation and starts a new speaker record at each recognized opening; subsequent paragraphs remain in that record until another opening appears. The MODS metadata supplies participants list, allowing us to match detected surnames to legislators and attach their Bioguide identifiers where available. Thus, Grassley's record receives a legislator identifier, while Zuckerberg's retains his transcript label without a legislator identifier. The [parsed examples](<../T1 - Text Summarization/T1.X - Worked Example/README.md#1-from-source-text-to-turn-records>) show these fields and link the text-processing rules, which require no LLM calls.

To focus the summarization input on discussion, we remove paragraphs containing dot leaders, which generally mark contents or index entries, and exclude records that the parser flags as written questions for the record (`qfr`). We also remove page markers and standardize whitespace. Text before the first recognized speaker remains in an unattributed record. For transcripts without consistent indentation, the parser uses blank lines to reconstruct paragraphs; the linked worked example documents this fallback.

For the Facebook hearing, the [source text](<../T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/source.txt>) yields 8,192 paragraphs. Removing 40 dot-leader paragraphs and grouping the remainder produces [903 speaker records](<../T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/parsed_turns.json>), containing the attributed speaker, member identifier where available, section label, and text in transcript order. These are the records passed to the next step. The output also reveals a limitation: the parser flags none as `qfr`, although the appendix contains written responses. Those responses remain attached to Grassley's final record and enter summarization. Consequently, the example summarizes the retained hearing record, including appended material; those appended responses cannot be treated as Grassley's own statements.

**2. Group consecutive speaking turns into model inputs.** Preserving speaker turns prevents a contribution from being divided arbitrarily, but summarizing at the level of speaker turn separately would introduce another problem from map-reduce approach: a answer could be detached from the question that explains it. Because the map stage summarizes each input independently, later aggregation cannot reliably restore context omitted from those summaries. We therefore group neighboring turns into larger inputs, keeping turns intact wherever possible and retaining their order, so the model can interpret several contributions as part of the same discussion.

We select a 6,144-token input window for transcript text, leaving additional space for instructions and generated text and at the same time can be applied to the four models we selected (`Qwen/Qwen3.5-4B`, `meta-llama/Llama-3.2-3B-Instruct`, `google/gemma-4-E4B-it`, and `meta-llama/Llama-3.1-8B-Instruct`) without exceeding the context window of the models. This choice lets each call process several neighboring contributions while keeping input length manageable and reducing the number of calls relative to summarizing each turn separately. Python adds the speaker labels and combines as many complete, consecutive turns as fit, measuring length with the summarization model's tokenizer. When the next turn would exceed the window, it starts a new chunk. The [chunking function](<../T1 - Text Summarization/T1.X - Background Helper Functions/chunking.py>) records the resulting lengths and any split turns.

The running example produces [55 chunks](<../T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/Chunks/chunks.md>). The first contains nine records and 5,881 tokens, including introductory text and opening remarks. The [second chunk](<../T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/Chunks/chunks_01-10.md#chunk-02>) contains nine records and 5,898 tokens, including Zuckerberg's opening statement and exchanges with Grassley. For example, Grassley asks whether Facebook has required audits to confirm deletion of improperly transferred data; Zuckerberg responds that it has, but he does not have the exact count. Keeping these turns together gives the model both the action being questioned and the context needed to interpret the reply.

This grouping preserves local discussion context where exchanges fit together, but boundaries are determined by length, so a question and answer can still fall in different chunks. A turn that exceeds the window on its own must also be divided: the code first uses paragraph boundaries, then token boundaries if a single paragraph is too long. In this example, chunks 8–14 divide a long record labeled Grassley that contains submitted letters and statements. The saved inputs make these exceptions visible; preserving the speaking turn is the guiding rule, with splitting used when necessary to fit the selected input window.

**3. Summarize each chunk.** We used `Qwen/Qwen3.5-4B` in bfloat16 precision as a primary model for production. Before deployment, the [model-comparison notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/02_model_comparison.ipynb>) ran four models on the same five hearings, selected near the 10th, 30th, 50th, 70th, and 90th percentiles of transcript length. It recorded processing time, call counts, summary lengths, and speaker-name retention. These measurements made the resource requirements of short and long hearings observable before scaling to the corpus. The notebook profiles feasibility and output characteristics; it does not establish which model produces the most accurate summaries. By manually checking small set of summaries, researchers can manually choose the best performing model.

After the LLM is chosen, each chunk enters a separate model call. In our example, the [map prompt](<../T1 - Text Summarization/T1.X - Worked Example/README.md#map-prompt>) requests about 150 words describing the subjects discussed, positions attributed to named speakers, and numbers and legislation copied from the input. These fields carry information needed to distinguish particular policies and speakers in later analysis. For a purely procedural or ceremonial segment, the prompt requests one sentence, reducing its representation without requiring the model to invent a substantive account. These are instructions to the model, not checks that every requested detail survives. In the example, 55 calls produce [55 segment summaries](<../T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#map-01>).

**4. Condense the segment summaries when necessary.** Our next goal is to bring the segment summaries together so the model can produce one account of the hearing as a whole. For long hearings, however, even these shorter summaries can collectively exceed the selected 6,144-token input window. We therefore introduce an intermediate condensation step that produces a shorter account of each successive portion of the hearing. Hearings whose segment summaries already fit proceed directly to the final synthesis.

Python checks the combined length of the summaries in transcript order. When they are too long, it groups consecutive summaries by token count and asks the model to condense each group. The [collapse prompt](<../T1 - Text Summarization/T1.X - Worked Example/README.md#collapse-prompt>) identifies the input as existing summaries and requests an account of about 200 words retaining named speakers, their positions, numbers, and legislation. Because each group covers only part of the hearing, the prompt explicitly instructs the model not to draw a conclusion about the hearing as a whole. Python then checks the combined length of the condensed accounts and repeats the process if needed, allowing up to eight condensation rounds.

In the Facebook example, the 55 segment summaries are too long to enter the final synthesis together. The procedure groups summaries 1–23, 24–45, and 46–55 and produces [three condensed accounts](<../T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#collapse-01>). These fit together within the selected input window, so one condensation round is sufficient. The final call can then consider the three accounts together to synthesize the hearing. Each additional condensation can omit details; we therefore retain both the original segment summaries and the intermediate accounts so readers can inspect what information survives.

**5. Produce the hearing-level summary.** In the reduce stage, the model receives the segment summaries, or their condensed versions, in transcript order in a single call. The [reduce prompt](<../T1 - Text Summarization/T1.X - Worked Example/README.md#reduce-prompt>) requests a 200–250-word account covering the hearing's purpose, main subjects, speakers' positions, disagreements, and key numbers and legislation. It instructs the model to omit details that the supplied summaries do not establish.

The word range is a prompt target. In our example, the generation is capped at 512 tokens, measured with the summarization model's tokenizer. This keeps the output short for downstream text analysis and compatible with BERT-based models (i.e., BERTopic). Since token counts differ across models, compatibility is checked separately using the downstream model's tokenizer in the evaluation below. When generation reaches the cap, the pipeline attempts to remove an incomplete final sentence.

For the Facebook hearing, the [final summary](<../T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#final-summary>) contains 264 words and 359 tokens. The complete sequence is **55 transcript chunks → 55 segment summaries → three condensed accounts → one hearing summary**, requiring 59 model calls. The example export reconstructs the inputs and verifies all 59 user-prompt hashes against the production log. The displayed summaries are the saved outputs from that run.

**6. Apply the procedure to the corpus.** Once a few examples have been reviewed and the resulting summaries meet the study's needs for content and quality, the next step is to scale the procedure to the full corpus. In our application, the [production notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/03_summarize_sst.ipynb>) divides the sample into ten disjoint batches and saves results after each hearing. The [assembly notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/04_assemble_summaries.ipynb>) combines the results and checks coverage, duplicates, failures, and summary lengths.

The completed run produced 2,352 successful hearing summaries from 26,722 chunks and 29,264 model calls. The median hearing required 11 chunks. Most hearings—2,259—proceeded directly from map to reduce; 93 required one collapse round. Final summaries had a median length of 396 tokens. Recorded per-hearing processing time summed to 112.7 hours across the ten batches.

**7. Validate the summaries against independent human-written abstracts.** Once summaries have been produced at scale, we need to assess whether they capture the hearings' substantive content. Fluent text alone is insufficient: a generated summary can omit central points or introduce claims unsupported by the transcript. Traditional measures such as ROUGE compare overlapping words or sequences with human reference summaries. Such overlap provides useful information, but does not by itself establish whether a summary preserves meaning or is faithful to its source. We therefore use independent human-written accounts as references and assess correspondence in meaning, allowing for differences in wording.

Comprehensive human-written summaries are not available for every hearing in our corpus. C-SPAN's editorial abstracts provide an available reference for hearings it broadcasts, but they are typically much shorter than our generated summaries and cover only the subject and selected points. This difference in scope limits what a direct comparison can establish: a detail absent from the abstract may still be supported by the transcript. An isolated similarity score also cannot show whether the resemblance reflects the particular hearing or vocabulary common to many policy discussions. We therefore ask whether a generated summary resembles the human-written abstract of its own hearing more closely than abstracts of other hearings, including those addressing related committee concerns.

We matched hearings to C-SPAN programs using date and chamber, title similarity, and witness names. This matching does not use the generated summaries' semantic similarity to the abstracts. Of the 2,352 hearings, 351 had a matched abstract. In the running example, the [generated summary and C-SPAN abstract](<../T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md#final-summary>) both identify Zuckerberg, Facebook's handling of user data, and Cambridge Analytica; the generated account includes additional subjects and details that the short abstract cannot independently verify.

We embedded the 351 generated summaries and a broader reference pool of 3,812 matched C-SPAN abstracts using `BAAI/bge-large-en-v1.5`, then calculated cosine similarity for every summary–abstract pair. Higher scores indicate closer representations of meaning in the embedding space. The [evaluation notebook](<../B - Backup of Original File Structure/scripts/python/02_text_summarization/05_evaluate_quality.ipynb>) checks lengths using the encoder's tokenizer and reports no truncation in either set. We divide the pairs into three mutually exclusive groups to assess what the similarity captures:

| Comparison | What the comparison helps assess | Pairs | Median similarity |
|---|---|---:|---:|
| Same hearing | Correspondence between the generated summary and an independent human account of the same event. | 351 | 0.798 |
| Different hearing, at least one shared committee identifier | A comparison for recurring committee subject matter: a generic account of a committee's concerns could resemble many of its hearings. | 94,304 | 0.576 |
| Hearings with no shared committee identifier | A broader comparison across congressional subjects, showing how much similarity remains outside shared committee membership. | 1,243,357 | 0.533 |

Figure 1 shows the distributions and their overlap. The higher median for the correct hearing, including relative to other hearings sharing a committee, supports the interpretation that the summaries retain information specific to the event beyond recurring committee subject matter. The comparison across committees provides a broader reference, although hearings from different committees can still discuss related topics. This design gives the same-hearing similarity a basis for interpretation without requiring the generated summary and editorial abstract to cover identical details.

Group medians can conceal weak matches for individual hearings. We therefore also ask whether each generated summary identifies its own abstract as the closest among all 3,812 candidates. The correct abstract ranked first for 215 of the 351 hearings (61.3 percent). Together, these checks provide evidence of hearing-specific content in the evaluated summaries. They do not establish the absence of hallucinations, the accuracy of every attribution or number, or complete coverage of the hearing. Those aspects require direct review against the source transcript; the paired texts and intermediate outputs make such review possible.

![Figure 1. Similarity between generated hearing summaries and C-SPAN abstracts](<../R - Results/figures/T1 - Text Summarization/cosine_similarity_averages.png>)

*Figure 1. Cosine similarity for the same hearing, different hearings sharing a committee, and hearings sharing no committee identifier. The vertical axis measures similarity; each observation is one summary–abstract pair. Boxes contain the middle 50 percent of scores, and the line within each box marks the median. Whiskers extend to the most extreme scores no more than 1.5 times that range beyond the box; more distant observations are hidden. The comparison uses 351 generated summaries and 3,812 C-SPAN abstracts.*

### 3.3. Research Outputs

The outputs support both subsequent text analysis and inspection of how the final accounts were produced. They retain three levels of information:

| Output | What it contains | Research use |
|---|---|---|
| Parsed source records and reconstructed inputs | Speaker labels and retained text, plus the rules and tokenizer needed to reproduce each input chunk. | Retrieve the language underlying a summary and inspect attribution, exclusions, or chunk boundaries. |
| Segment and collapse summaries | The recorded outputs before final synthesis, identified by their stage and order. | Locate whether a detail disappeared when source text was first summarized or during later condensation. |
| Hearing-level summary table | One row for each of the 2,352 hearings, containing the final summary and identifying and run metadata. | Extract hearing subjects as in Section 4 and compare short accounts across hearings. |

For the running example, the [input chunks](<../T1 - Text Summarization/T1.X - Worked Example/01 - Inputs/Chunks/chunks.md>) and [recorded summaries](<../T1 - Text Summarization/T1.X - Worked Example/02 - Outputs/outputs.md>) let a reader follow a passage through these levels. The hearing-level table includes model and prompt versions, chunk and call counts, collapse rounds, processing time, and summary length, so the amount of processing is visible alongside the resulting text.

Separate call logs retain the stage, position, user-prompt hash, token counts, timing, and output text for all 29,264 model calls. The corpus input chunks can be reconstructed from the retained parsed records using the tokenizer, packing rules, and selected input window, then checked against the logged hashes. The [worked example](<../T1 - Text Summarization/T1.X - Worked Example/README.md>) provides those inputs as readable files and includes the verification code. This record supports checking a specific transformation or revisiting it with different settings, while preserving the distinction between reproducing the saved computation and establishing the factual accuracy of its output.

---

## 4. Step #2: Extracting Relevant Information from Textual Documents

Summaries make a corpus easier to read, but they remain prose rather than comparable observations of subjects and positions. This step converts hearing text into two linked datasets: the subjects discussed in each hearing and legislators' expressed positions on those subjects. The first uses the summaries produced in Section 3; the second returns to the source text to preserve individual speakers' statements. A common topic codebook allows differently worded expressions about related subjects to be compared across hearings, while retaining the original wording and evidence.

### 4.1. How Topic Extraction Works: Topic and Stance Identification

Document subjects and actor-level positions answer different research questions. A document can discuss a subject without expressing support or concern, while a summary can omit an individual's position or combine several speakers' contributions. Summary-based topic extraction and extraction from source passages can therefore provide complementary information.

The procedure involves four decisions:

1. **Choose the source text and the information to extract.** Document summaries can supply broad subjects. Actor-level positions require passages that preserve who said what; for example, studying managers' concerns requires distinguishing their statements from analysts' questions. These sources can be used separately or together, according to the required detail. Specify the requested fields, such as topic, stance, and supporting sentence references, and define which statements qualify.
2. **Organize topic phrases into common categories.** Different documents can describe related subjects in different words. Embedding and clustering those phrases creates candidate groups. Researchers must choose the source phrases and the level of detail appropriate for the research question; broad document subjects and narrow objects of individual statements need not define the same categories.
3. **Review the codebook and specify assignment rules.** An LLM can draft category labels, definitions, and examples from cluster members. Reviewing those groups can reveal overlapping categories or clusters held together by generic wording. Record decisions to retain, merge, or remove groups, then specify how extracted phrases enter the resulting categories and when they remain unassigned.
4. **Check the outputs and construct measures.** Format checks can verify required fields and source references. Substantive review must separately assess whether the evidence supports the interpretation and category. External classifications can benchmark document topics. Retaining the original wording and evidence allows researchers to inspect the records underlying aggregated measures.

Aggregation requires an explicit counting unit and comparison period. Counts of extracted statements measure the volume of expressed positions; they need not equal the number of actors holding a view. A separate measure summarizes their balance:

$$
\text{Net stance} = \frac{\text{Support records} - \text{Concern records}}{\text{Support records} + \text{Concern records}}
$$

The measure ranges from −1, when all records express concern, to +1, when all express support; zero means equal counts. It is defined when at least one record is present. A minimum-record rule can limit displays based on sparse evidence. Researchers should preserve the underlying counts because similar balances can arise from very different volumes of discussion.

### 4.2. Application: Topic Extraction and Stance Analysis in Congressional Hearings

We process the same 2,352 hearings used in Section 3. Track 1 extracts subjects from each hearing summary; Track 2 extracts positions from legislators' speaking turns. We continue the April 10, 2018 Zuckerberg hearing as a running example. The linked [topic and stance example](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/README.md>) contains the numbered inputs, exact prompts, recorded responses, category assignments, and verification code.

**1. Extract the hearing's principal topics from its summary.** The [Track 1 production notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/04_track1_production.ipynb>) supplies each final summary to `Qwen/Qwen3.5-4B`. The prompt requests up to five neutral phrases, ordered from most to least central. The limit allows several subjects while focusing the output on the hearing's main concerns. It asks for specific policies, programs, regulations, technologies, practices, or budget items, excluding bare agency names and incidental examples. Naming a policy or practice distinguishes the object of discussion more clearly than naming only an organization. For the Zuckerberg hearing, the [saved response](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/topics.json>) is:

```json
["Facebook data privacy", "content moderation", "election integrity", "Honest Ads Act", "GDPR-style controls"]
```

Python parses the list, removes duplicate phrases, and stores their ranks. Across the corpus, this produces 11,592 mentions and 9,095 distinct phrases after standardizing capitalization and surrounding whitespace.

**2. Prepare legislators' turns for stance extraction.** The [preparation notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/01_member_turns.ipynb>) returns to the parsed transcripts and selects records labeled as spoken and attributed to a committee member or the unnamed-chair identifier. Witness records are excluded because this track measures legislators' expressed positions rather than pooling those views with the testimony they receive. It splits each paragraph into sentences using `pysbd==0.3.4`, preserving paragraph boundaries to prevent malformed sentences from spanning large stretches of text. It then removes repeated speaker labels, bracketed stage directions, and mostly capitalized headers, and truncates each turn at the first recognized adjournment or inserted-document marker.

These additional rules address written material that the earlier parser retained. A written response appended to the chair's final record should not become evidence of the chair's own position. In the example, Grassley's final record loses its written-response appendix and becomes [three closing sentences](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/01 - Inputs/numbered_turns.md#turn-902>). The rules discard everything after a matched marker within that turn; they do not recover speech that might resume later in the same record. From the hearing's 903 parsed records, this stage selects **507 legislator turns containing 1,696 cleaned sentences**. Across the corpus, 221,311 selected turns become 220,160 nonempty turns containing 985,661 sentences. Sentence numbering starts at one within each cleaned turn, allowing the model to point to existing evidence without generating a quotation.

**3. Extract each position with its supporting sentences.** The [Track 2 production notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/03_track2_production.ipynb>) supplies each numbered turn to the same model, dividing turns longer than 40 sentences into consecutive windows while preserving the numbering. The prompt requests a neutral topic phrase, `support` or `concern`, and one to three consecutive sentence references. Support includes endorsement or advocacy for adoption, funding, or expansion; concern includes criticism, worry, objection, or calls for restriction or scrutiny. Procedural remarks and questions without an expressed position should return no record.

For example, [Senator Hassan's input](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/01 - Inputs/numbered_turns.md#turn-772>) includes:

```text
[6] You have supported targeted regulations such as the Honest Ads Act, and that is an important step for election integrity.
[7] I am proud to be a cosponsor of that bill.
```

The [recorded response](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/stance_records.md#turn-772-record-0>) is:

```json
[{"sentences": [6, 7], "topic": "Honest Ads Act", "stance": "support"}]
```

Separating the neutral topic from the stance allows support and concern about the same object to enter a common category. Here the record identifies Hassan's endorsement of the Honest Ads Act; it does not label her as supporting Facebook or every policy discussed in the hearing. Keeping the sentence references makes this interpretation inspectable in the source.

The [parser](<../T2 - Topic Extraction and Stance Analysis/T2.X - Background Helper Functions/stance.py>) checks the fields, stance vocabulary, and sentence indices. Invalid records are discarded with an error flag. Potentially directional topic wording is retained with a review flag. To reduce repeated counting of one local expression, records with the same topic wording and stance are merged when their evidence overlaps or the next evidence range begins within two sentence positions of the previous range's end. For this hearing, eight candidate records fail the consecutive-reference check and one merge combines duplicate records, leaving **49 stance records from 27 turns**. The full corpus contains **32,385 records**. The example's verification script reproduces the cleaning, parsing, and merging results and matches all 508 extraction user-prompt hashes to the saved logs.

**4. Construct and review the topic codebook.** The extracted phrases retain useful detail, but differences in wording make direct comparison difficult: “Facebook data privacy” and “GDPR-style controls,” for example, name different aspects of privacy policy. We build common categories from Track 1's phrases across all hearings, giving the codebook a hearing-level scope. Track 2's narrower objects are assigned afterward so that individual statements do not independently determine the categories used to compare hearings.

The [clustering notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/08_taxonomy_consensus.ipynb>) removes years, bill numbers, and selected trailing terms for clustering; for example, “Honest Ads Act” becomes “Honest Ads.” This reduces distinctions based on naming conventions before comparing substantive wording; the original phrases remain available in the outputs. It embeds the resulting 8,736 distinct usable strings with `BAAI/bge-large-en-v1.5`, then groups closely related expressions using average-linkage clustering at cosine distance 0.100, producing 7,712 preliminary groups.

The number of categories determines which substantive differences remain visible: broad categories combine related policy areas, while more detailed categories distinguish objects within them. The code examines nine cluster counts from 15 to 150. For each count, it fits weighted k-means on 80-percent subsamples drawn without replacement 30 times, assigns all preliminary groups in each repetition, and combines the results according to how often groups share a cluster. Repeating the calculation tests whether groupings persist when the fitting sample changes.

We examine three properties. **Stability** measures how consistently members are assigned together across repetitions. **Silhouette** compares proximity within a cluster with proximity to neighboring clusters, assessing separation. **Cohesion** assesses how closely member embeddings align within each cluster, flagging groups with dispersed meanings for review. These diagnostics address different concerns: a reproducible group need not be well separated or substantively coherent. The 15-group solution has the highest weighted stability and silhouette among the tested counts. Among the finer partitions from 40 to 150, the 150-group solution has the highest weighted stability and fewest low-cohesion groups. The saved choices are 15 broad clusters and 150 candidate topics. The drafting notebook also identifies comparability with the earlier codebook's level of detail as a reason for choosing 150. These are selected levels of detail, not uniquely optimal counts or minimum quality thresholds that every topic passes.

![Clustering diagnostics across candidate category counts](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_taxonomy_criteria.svg>)

*Choosing the codebook's level of detail. The horizontal axis gives the number of clusters. The navy line reports weighted mean coassignment as a percentage; the green line reports the share of phrase weight in clusters with coassignment of at least 0.50; the red line reports sampled silhouette multiplied by 100. Higher values indicate greater stability or separation under the corresponding measure, rather than classification accuracy. The linked notebook reports the additional cohesion flags used in review.*

The [drafting notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/09_codebook_draft.ipynb>) supplies each cluster's member phrases and two neighboring clusters to Qwen to draft its label, definition, exclusions, and examples. Neighboring phrases help specify the boundary between similar categories, while checks against the supplied members remove invented example phrases. A plausible label alone cannot establish a coherent group. The [review decisions encoded in the next notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/10_codebook_freeze_assign.ipynb>) drop 30 topic clusters, merge nine into retained clusters, and revise eight labels. For example, one dropped cluster groups unrelated named Acts; a merged cluster places Clean Air and Clean Water Act phrases with EPA regulation.

Each retained topic is placed under the broad cluster receiving the greatest frequency-weighted share of its member phrases after merges. Only 14 broad clusters remain represented. The resulting [codebook of 111 topics under 14 themes](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/codebook.json>) is saved with a hash identifying its fixed version, so later assignments refer to the same set of categories.

**5. Assign both sets of extracted phrases to the codebook.** Track 1 uses the phrases' cluster membership and the recorded merge/drop decisions. Because these phrases formed the codebook, they do not need a new similarity-based assignment. Phrases from dropped clusters or without usable clustering input remain in “other.” The example yields:

| Rank | Extracted phrase | Topic ID | Saved category |
|---:|---|---:|---|
| 1 | Facebook data privacy | 68 | consumer data privacy legislation |
| 2 | content moderation | 93 | Online advertising and consumer choice policies |
| 3 | election integrity | 100 | Voting systems standards and integrity |
| 4 | Honest Ads Act | 93 | Online advertising and consumer choice policies |
| 5 | GDPR-style controls | 68 | consumer data privacy legislation |

The [implemented primary-topic rule](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/10_codebook_freeze_assign.ipynb>) counts assigned phrases and retains the category with the largest count. Here categories 68 and 93 tie at two phrases. The grouping operation orders categories by topic identifier, and the subsequent sort by hearing and descending count retains the first row for each hearing. Category 68 therefore precedes 93 and is saved as the primary topic. This tie is resolved by table ordering; the original phrase ranks do not enter the selection. Across the corpus, 2,342 hearings receive a primary classification.

> **Coauthor note — primary-topic ties.** The implemented table-order rule remains in use. [Appendix B](#appendix-b-primary-topic-tie-breaking) preserves the proposed alternatives, the comparison across tied hearings, and the changes requiring a coauthor decision.

Track 2 requires a rule for assigning phrases that did not define the codebook. The code first constructs one vector for each of the 111 categories by averaging the embeddings of its normalized Track 1 member phrases, giving greater weight to phrases extracted more frequently across hearings, and normalizing the resulting vector. Thus, a category is represented by its constituent phrases rather than by embedding its drafted label and definition. For example, category 93 includes the member phrases “content moderation” and “Honest Ads Act” shown above.

Each distinct stance topic phrase is embedded with the same encoder and compared with all 111 category vectors. The code assigns the closest category when cosine similarity is at least 0.68; otherwise it records “other,” preserving phrases without a sufficiently close match instead of forcing every record into the codebook. The assignment uses the topic phrase and leaves its support-or-concern label unchanged. Hassan's “Honest Ads Act” is assigned to category 93 with similarity 0.733. Of the example's 49 records, **41 receive categories and eight remain in other**; the corresponding corpus totals are 29,979 and 2,406. The threshold controls whether an assignment is made; it does not by itself establish that the category is appropriate.

**6. Inspect assignments and benchmark hearing topics.** The retained text makes errors visible. For example, Tillis's [“business code of conduct” record](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/stance_records.md#turn-656-record-1>) is assigned to “hours-of-service regulations” at similarity 0.695. Passing the threshold does not establish an appropriate substantive match. Sentence references, original topic wording, and assigned labels are therefore retained together for review.

We use the Comparative Agendas Project (CAP) to assess two uncertainties that format checks and individual examples leave unresolved: whether extracted phrases capture a hearing's substantive subject, and whether grouping those phrases produces categories that bring together hearings on related subjects. CAP supplies human-coded major topics and subtopics for comparison. Since our codebook uses its own categories, we examine correspondence between the two systems rather than requiring identical labels.

The [CAP evaluation notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/11_cap_evaluation.ipynb>) starts with 1,796 hearing matches, of which 1,763 meet the two stronger matching tiers based on dates and titles within the matching procedure's Congress, chamber, and committee restrictions. Requiring usable CAP codes and classifications in both the current and earlier codebooks leaves **1,697 hearings**. The Zuckerberg hearing has no saved CAP match and does not enter these comparisons. The following assessments use this common sample, addressing a different remaining uncertainty at each stage.

**(a) Does the extracted phrase identify the hearing's human-coded subject?** A plausible, well-formed topic phrase can still miss the principal subject of a hearing. To evaluate its substantive correspondence, the code embeds each hearing's first-ranked Track 1 phrase and the descriptions of all 213 CAP subtopics using `BAAI/bge-large-en-v1.5`. It ranks the CAP descriptions by cosine similarity to the phrase and records the position of the human-assigned subtopic. The histogram below converts those positions into percentiles: 100 corresponds to first place and zero to last place.

The human-assigned subtopic ranks first for **27.0 percent** of hearings, within the top 11 for **63.1 percent**, and fifth at the median. This measures whether the extracted phrase points toward the human-coded subject. It does not establish how much of that performance could be obtained by guessing frequently occurring subjects, which motivates the next comparison.

![CAP subtopic ranks for first-ranked extracted phrases](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_cap_rank_percentile.svg>)

*Overall phrase correspondence. Each bar reports the share of hearings in a five-point percentile interval. The dashed line marks approximately 5 percent per interval under uniform random ranking.*

**(b) Does the phrase add information beyond the frequency of policy subjects?** Science and Commerce hearings concentrate on particular subjects, so a method can outperform random ranking simply by favoring common CAP codes. The code therefore compares the phrase-based ranking with a frequency rule that gives every hearing the same list of the sample's most common CAP subtopics. For each list length from one to 20, it calculates the share of hearings whose human-assigned code appears in the list. A uniform-random reference is also shown.

With one candidate, phrase-based retrieval finds the human code for **27.0 percent** of hearings, compared with **9.4 percent** for the frequency rule. With 11 candidates, the shares are **63.1 and 52.9 percent**. This comparison establishes the additional correspondence associated with hearing-specific phrases beyond the sample's subject distribution. The frequency ranking is calculated from the evaluation sample itself, so it is a descriptive benchmark. Neither overall comparison reveals whether the result holds equally across policy areas.

![CAP retrieval compared with frequency and random baselines](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_cap_retrieval.svg>)

*Retrieval against baselines. The horizontal axis gives the number of candidate CAP subtopics retained; the vertical axis gives the share of hearings whose human-assigned subtopic is among them. The frequency rule uses the same candidates for every hearing.*

**(c) Does the overall result conceal weak correspondence in particular policy areas?** A strong aggregate result can be driven by the largest or most easily identified subjects. The code therefore takes the same phrase-level percentile ranks from assessment (a) and groups them by each hearing's assigned codebook theme. The boxes show the median and middle half of the rankings within each theme, with sample sizes alongside the labels.

This breakdown locates areas where extracted phrases correspond less closely to CAP or where correspondence varies widely across hearings. The saved plot places manufacturing competitiveness at the low end of median correspondence and railroad safety at the high end; theme sample sizes range from 16 to 245 hearings. The groups organize the diagnostic, but the quantities being evaluated remain the original first-ranked phrases. Whether the codebook itself groups hearings consistently with human classifications requires a further check.

![CAP phrase correspondence separated by codebook theme](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_cap_subtopic_boxes.svg>)

*Variation across themes. Values nearer 100 indicate better phrase-level correspondence with the human-assigned subtopic. Whiskers extend to the most extreme observations within 1.5 interquartile ranges; outliers are hidden. The dashed line marks the median under random ranking.*

**(d) Do the broad codebook themes bring together hearings in similar human-coded policy domains?** The preceding assessments concern phrase meanings. Clustering and consolidation can still combine hearings that CAP places in different domains. To examine those groupings directly, the code takes each hearing's assigned primary topic and its parent theme, then cross-tabulates that theme with the hearing's human-assigned CAP major topic. Each row in the heatmap reports the distribution of one theme's hearings across CAP domains and sums to 100 percent. This comparison uses category assignments rather than distances between category descriptions.

For example, **217 of 245 hearings (88.6 percent)** in the NASA theme receive CAP's Technology code; **74 of 93 (79.6 percent)** in Aviation and Transportation Security receive Transportation. A concentrated row indicates correspondence with a particular CAP domain. A dispersed row identifies a theme that spans CAP boundaries and warrants inspection: the dispersion can reflect different organizing principles or an overly broad grouping. Even close correspondence at this level can conceal mixtures of distinct subjects within a detailed topic.

![Codebook themes cross-tabulated with CAP major topics](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_cap_crosswalk.svg>)

*Broad category correspondence. Cells show percentages within each codebook theme; numerical labels appear for shares of at least 10 percent. This is a comparison of the hearings assigned to categories.*

**(e) Do the detailed codebook topics retain distinctions within those broad domains?** A theme can align with CAP's Technology domain while combining separate subjects such as space research and telecommunications. To inspect the finer categories used in subsequent research measures, the code selects the 25 most frequent primary topics, finds the most common human-assigned CAP subtopic within each, and reports the share of that topic's hearings receiving that code.

All **31 hearings** classified under Federal agency and board nominations receive CAP's Appointments code. For Mars and lunar exploration missions, **39 of 43 (90.7 percent)** receive Space. Shorter bars identify categories whose hearings CAP distributes across several subtopics. The CAP counterpart is selected as the most frequent code in the same sample, so these bars describe within-topic concentration; they are not accuracy estimates for a separately trained classifier. They also cover only the 25 most frequent primary topics.

![Detailed codebook topics and their most common CAP subtopics](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_cap_subtopic_pairs.svg>)

*Detailed category correspondence. Bar length is the share of a codebook topic's hearings receiving its most common CAP subtopic; the right-hand label names that subtopic. Counts alongside the topic labels show the available evidence.*

The notebook also repeats the semantic retrieval calculation using each hearing's final theme and topic labels together. The human-assigned CAP subtopic then ranks first for **25.8 percent** of hearings, within the top 11 for **54.9 percent**, and ninth at the median. This provides a complementary check on the standardized labels: their wording retrieves CAP subjects less closely than the original phrases under this measure, even where the groupings show correspondence. The earlier codebook comparison is retained in the linked notebook.

These assessments document phrase-level correspondence, performance beyond subject frequency, variation across policy areas, and agreement of broad and detailed groupings with CAP. They do not verify every extracted topic, the accuracy of individual support/concern labels, or the assignment of stance records to the codebook. The mismatched stance assignment illustrated above therefore remains a separate issue. Because CAP agreement also informed codebook development, these results are external benchmarks rather than an untouched holdout test.

**7. Aggregate records into topic–Congress and legislator panels.** The [panel notebook](<../B - Backup of Original File Structure/scripts/python/03_topic_extraction/12_stance_panel.ipynb>) groups records by Congress, which supplies a common two-year period for comparison. The Zuckerberg hearing falls in the 115th Congress, covering 2017–2018. The code creates two tables, each answering a different research question.

The **topic-by-Congress table** asks how many expressions of support and concern a subject receives during that period. Each row represents one topic in one Congress and contains the total number of assigned records, separate support and concern counts, and the numbers of distinct hearings and speaker identifiers contributing them. The saved table contains 1,453 such rows. It includes topic–Congress combinations with records; the attention figure in Section 4.3 fills absent combinations with zeros.

The privacy category illustrates how one hearing contributes to a period total:

| Records for “consumer data privacy legislation” | Hearings contributing records | Support | Concern | Total records |
|---|---:|---:|---:|---:|
| Zuckerberg hearing alone | 1 | 7 | 6 | 13 |
| All contributing hearings in the 115th Congress | 17 | 34 | 21 | 55 |

The 13 records from the running example are included in the period's 55 records; the other 42 come from 16 additional hearings. This calculation counts each assigned stance record once, whether its supporting passage contains one sentence or several. A legislator can contribute multiple records, so these totals do not represent the number of legislators holding a view. Applying the net-stance definition in Section 4.1 gives `(34 − 21) / 55 = 0.236` for privacy in the 115th Congress. This category remains in the full panel but falls outside the 25 topics displayed in Section 4.3.

The **legislator-level table** asks which speakers contribute those expressions. Each row contains one speaker identifier and surname, one topic, one Congress, one stance, and the number of records with that combination. Support and concern occupy separate rows when both occur. For Hassan, category 93 in the 115th Congress has one support record and four concern records. The support record concerns the Honest Ads Act; the concern records include other objects, such as ad targeting. The counts therefore retain positions within a shared category without assuming that every statement concerns the same proposal.

The saved legislator table has 15,173 rows representing 27,679 records. It excludes 2,300 unnamed-chair records because the grouping operation drops records with missing surnames. Those records remain in the topic-by-Congress totals, where they carry a shared placeholder speaker identifier. Consequently, the two tables cover different sets of records, and the topic table's count of speaker identifiers cannot be interpreted as a count of fully identified individuals.

### 4.3. Research Outputs

The pipeline produces data at three levels: the subjects of individual hearings, the positions expressed in individual statements, and counts of those positions across legislators and time. These outputs allow researchers to identify hearings on a common subject, retrieve the statements underlying a measured position, and examine how the volume and balance of expressed views vary across topics and Congresses. The panel-construction rules and worked aggregation appear in Section 4.2. Here we describe the available records and the patterns their aggregated counts make observable.

**1. Hearing topics and statements that can be traced to their source.** The codebook provides a common set of 111 topics under 14 themes, including definitions and example phrases. The hearing-level output retains the ranked phrases extracted from each of the 2,352 summaries and their assigned categories; 2,342 hearings also receive a primary-topic classification. A researcher can therefore select hearings classified under a subject and inspect the original phrases that led to that classification. For the Zuckerberg hearing, the [saved topic output](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/topics.json>) retains both “Facebook data privacy” and “GDPR-style controls,” even though both enter the standardized category “consumer data privacy legislation.” This preserves more detail than a single hearing label would convey.

The stance output contains 32,385 records. Each records a topic phrase, a support-or-concern label, the speaker, the hearing and turn identifiers, and references to the sentences supporting the extraction. For example, [Hassan's record](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/02 - Outputs/stance_records.md#turn-772-record-0>) links her support for the Honest Ads Act to sentences 6 and 7 of turn 772, and also records its assignment to category 93, “Online advertising and consumer choice policies.” Researchers can move from the standardized category back to the specific object and source language. The saved dataset retains the 2,406 records assigned to “other”; the aggregated topic measures below use the remaining 29,979 records with codebook assignments.

The two aggregated outputs summarize these records by topic and Congress, and by legislator, topic, Congress, and stance. The former supports comparisons of discussion across subjects and periods; the latter identifies the speakers contributing those expressions. Their coverage differs because unnamed-chair records enter the topic totals but are excluded from the legislator table, as documented in Section 4.2.

**2. Which topics generate the most expressions of support and concern?** The first figure uses the topic-by-Congress table to compare the overall volume and balance of positions across subjects. The code sums support and concern records over all Congresses, selects the 25 topics with the largest combined counts, and draws one row for each. Concern records extend left from zero and support records extend right. The combined length of the two bars gives the total number of records for that topic; comparing the two sides reveals which stance is more frequent.

For example, “Science and research funding” contains 1,372 records: 716 support and 656 concern. Its two long bars indicate many extracted positions on both sides. Other topics can have similar totals with a more uneven balance. These comparisons identify subjects that generated substantial directional discussion in the sampled hearings. They measure expressions retained by the extraction procedure, so factual discussion and questions without an extracted position do not add to the bars. Counts also give more weight to speakers who contribute more records.

![Support and concern by topic](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_stance_topics.svg>)

*Support and concern across topics. Each row is one of the 25 topics with the most assigned stance records over the full sample. Bar lengths are record counts; left and right indicate concern and support, respectively.*

**3. When do those topics receive attention through expressed positions?** Totals over the full sample cannot show whether a topic generated positions throughout the period or mainly during a few Congresses. The second figure separates the same 25 topics by Congress. Each row is a topic, each column is a two-year congressional period, and each cell contains the combined number of support and concern records for that topic and period. Darker blue indicates more records. Reading across a row reveals the timing of activity on one subject; reading down a column compares the subjects discussed during the same Congress.

For example, science and research funding has 146 records in the 109th Congress and 129 in the 115th. These counts describe the volume of extracted positions without distinguishing their direction. Differences can reflect the number and subjects of hearings, the participating speakers, and their frequency of expressing positions. The figure reports raw counts rather than rates adjusted for those opportunities to speak; its darkest shade is capped at the 98th percentile of displayed cell counts. It can locate periods for closer investigation, but a darker cell alone does not establish a change in policy priorities.

![Stance record counts by topic and Congress](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_stance_attention.svg>)

*Timing of expressed positions. Cells show support and concern records combined. The 25 topics are ordered by their total record counts over the sample, and columns run from the 104th through the 119th Congress. Combinations with no assigned records are displayed as zero.*

**4. How does the balance of support and concern change within a topic?** The attention figure treats support and concern alike: two equally dark cells can contain very different mixtures of positions. The third figure applies the net-stance measure defined in Section 4.1 to the counts assembled in Section 4.2. Values near −1 indicate predominantly concern records, values near +1 predominantly support, and zero equal counts.

Within the plotted topics, science and research funding changes from 59 support and 87 concern records in the 109th Congress, giving −0.192, to 74 support and 55 concern records in the 115th, giving +0.147. Thus, similar volumes of records can accompany a change in the balance of expressed views.

In the figure, red indicates more concern, navy indicates more support, and pale shading indicates a balance near zero. Cells with fewer than five records are blank to avoid displaying a strong-looking balance based on very little evidence; a blank cell can therefore contain a few records and does not imply an absence of discussion. Because the measure weights records rather than individuals, a change can reflect different speakers or proposals as well as changing positions. The original topic wording and sentence references allow researchers to inspect those possibilities. The extraction and assignment errors illustrated in Section 4.2 also carry into these descriptive measures until the underlying records are reviewed and corrected.

![Net stance by topic and Congress](<../R - Results/figures/T2 - Topic Extraction and Stance Analysis/fig_stance_net.svg>)

*Balance of expressed positions. Color represents net stance for the same topic–Congress combinations as the attention figure. Cells with fewer than five records are masked; a colored value describes the balance among extracted records, rather than a legislative vote or consensus on a single proposal.*

---

## 5. Step #3: Identifying Topic Relevance and Corporate Disclosure

Topic extraction identifies the subjects discussed in hearings and the positions expressed about them. Topic relevance connects those subjects to firms whose disclosed activities fall within their scope. This connection can extend beyond organizations named in a hearing or represented by a witness. A discussion of consumer data privacy, for example, can concern both a social media company handling user information and a medical-device company handling patient information. Industry classifications and firm-name matching alone would not establish that shared connection.

The measurement must distinguish three questions: whether the disclosure concerns the topic, how much of the disclosure discusses it, and whether the text presents the connection as an opportunity, a threat, or neither. Semantic similarity supplies a continuous measure of relatedness, but similar passages can describe very different implications. Conversely, an LLM can identify and classify particular statements, but its judgments require evidence and evaluation. We construct the two measures separately and retain their supporting sentences. We then add a combined measure: each directionally classified sentence contributes in proportion to its similarity to the topic. The motivation is that similarity can help assess **what a sentence concerns**, while substantive interpretation must assess **which direction its implications support**. Accumulating those contributions relative to disclosure length measures the intensity of the firm's discussion. Neither textual similarity nor the firm's framing of a connection establishes the economic effect of a hearing or policy.

### 5.1. How Topic Relevance Works: Similarity and Sentence-Level Assessment

The procedure involves five decisions:

1. **Define the connection and select the evidence.** Specify what would make a topic relevant to the entities being studied, such as a relationship to their products, services, customers, or operating conditions. A general reference to an industry may be insufficient. Divide the source documents into identifiable passages and retain document dates, entity identifiers, and sentence references. Sentence-level comparisons can preserve a relevant business segment that would contribute little to an embedding of the whole document.
2. **Represent the topics and calculate semantic similarity.** Topic definitions and supporting passages can be embedded and combined into a numerical representation. A fixed representation permits comparisons against a common reference; a changing representation may be appropriate when the question concerns changes in the topic itself. Record the period supplying the reference evidence. Comparing document sentences with these representations and averaging several of the closest matches focuses the measure on relevant passages without letting one sentence determine the entire score. Check whether the scores vary with document length or differ systematically across topics.
3. **Identify and classify connections in the source text.** An LLM can read consecutive sentence blocks, identify relevant topics, and return sentence references with directional labels. An initial screen using short topic labels can reduce the definitions supplied during detailed confirmation, but it can also miss relevant subjects. Keep the evidence used for this assessment separate from the similarity ranking when the purpose is to compare the two methods. Similarity-selected inputs would make that comparison partly a consequence of the selection rule.
4. **Aggregate statements and link observations.** Count distinct qualifying sentences within each document and topic, preserving their directional classifications. A combined measure can weight each classified sentence by its topic similarity and divide by all retained document sentences, producing separate opportunity and threat indices. This captures the extent and semantic closeness of directional discussion; it does not measure economic severity. Link documents through common topic identifiers and explicit date rules, and distinguish an observed absence of qualifying tags from incomplete or failed processing.
5. **Evaluate each source of uncertainty.** Source inspection tests whether the passages support the interpretation. A comparison without preliminary screening tests what the screen excludes. Independent human review tests substantive relevance and direction. Comparing similarity scores with LLM classifications assesses agreement between the methods, while retaining the possibility that both share errors in source material or topic definitions. Store the inputs and intermediate responses needed to locate those errors.

**Define separate measures of threat and opportunity.** A similarity score does not identify direction, while a directional count gives every accepted tag equal weight. After constructing the similarity and classification measures separately, we can combine their sentence-level evidence. The following definition preserves both the extent of discussion and its direction without letting opportunities and threats cancel.

For firm $f$, topic $k$, and filing $t$, let $S_{ft}$ be the retained sentences and $N_{ft}=|S_{ft}|$. Let $\mathbf{e}_s$ denote a sentence embedding and $\mathbf{v}_k$ the fixed representation of topic $k$. The sentence's weight is its cosine similarity, bounded below by zero:

$$
c_{sk}=\frac{\mathbf{e}_s^\top\mathbf{v}_k}{\|\mathbf{e}_s\|\,\|\mathbf{v}_k\|},
\qquad w_{sk}=\max(0,c_{sk}).
$$

Let $D_{sk}$ be the recorded LLM classification: threat ($T$), opportunity ($O$), neutral, or no accepted tag. The unweighted directional share is $100n^d_{fkt}/N_{ft}$, where $n^d_{fkt}$ counts accepted sentences in direction $d$. To also account for their semantic closeness to the topic, we calculate two weighted indices:

$$
\operatorname{Threat}_{fkt}=\frac{100}{N_{ft}}\sum_{s\in S_{ft}}w_{sk}\,\mathbf{1}\{D_{sk}=T\},
\qquad
\operatorname{Opportunity}_{fkt}=\frac{100}{N_{ft}}\sum_{s\in S_{ft}}w_{sk}\,\mathbf{1}\{D_{sk}=O\}.
$$

Here, $\mathbf{1}\{\cdot\}$ equals one when the condition holds and zero otherwise. Neutral and untagged sentences contribute zero to both numerators; all retained sentences remain in the denominator. Keeping the two indices separate preserves simultaneous threats and opportunities within a firm. For either direction $d$ with $n^d_{fkt}>0$ tagged sentences, the index also equals

$$
\operatorname{Score}^{d}_{fkt}
=\left(100\frac{n^d_{fkt}}{N_{ft}}\right)\overline{w}^{d}_{fkt},
$$

where $\overline{w}^{d}_{fkt}$ is the mean weight of those sentences. Thus, the score combines the extent of directional discussion with its semantic closeness to the topic. Its units are similarity-weighted sentence equivalents per 100 retained sentences, rather than a literal percentage, probability, or estimate of economic loss or gain. Bounding weights below by zero prevents a negative similarity from reversing a sentence's direction; zero is not a validated relevance threshold.

**Compare a firm over time against a fixed topic.** Applying the same calculation to successive annual disclosures yields separate firm–topic trajectories for threat and opportunity discussion. Holding the topic vector fixed provides a common reference; changing filing text and directional classifications can change the scores. Comparable trajectories require consistent embedding, preprocessing, and labeling procedures, with changes in those choices documented. The indices describe disclosed content and implications. Estimating a policy's or hearing's economic effect requires an additional research design.

### 5.2. Application: Hearing Topics and S&P 500 10-K Item 1 Disclosures

We connect the 111 hearing-derived topics to firms' descriptions of their businesses in 10-K Item 1. Relevance means that a passage describes the firm's products, services, technologies, inputs, customers, or operating conditions within the topic's subject area. The passage need not name a hearing, law, or agency. This permits connections across industries while requiring evidence about the firm's own activities.

We continue the April 10, 2018 Zuckerberg hearing, `CHRG-115shrg37801`. Its saved primary category is topic 68, **consumer data privacy legislation**, under the implemented selection rule and tie described in Section 4. The [worked example](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/README.md>) follows this topic from the codebook to firm disclosures, scores, sentence classifications, and the hearing–firm table. Facebook anchors the example throughout; ResMed supplies a comparison for the embedding calculation. Total System Services, Paycom Software, and Fidelity National Information Services supply further sentence-level illustrations of threat and opportunity. All are drawn from the completed assessment of every eligible firm.

**1. Select the firms' disclosures and preserve their dates.** The source corpus contains 21,966 usable Item 1 disclosures for 1,061 firms ever included in the project's S&P 500 sample. For the running hearing, the [preparation script](<../T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.1 - Production Batch Tagging Pipeline.py>) selects each firm's most recent available, usable filing dated before April 10, 2018. This yields **998 filings for 998 firms**. It uses the filing date, which establishes when the disclosure became available, rather than selecting by fiscal year alone. Selecting a filing available before the hearing keeps later changes in the firm’s business description out of this hearing-linked comparison.

Facebook's selected report covers fiscal year 2017 and was filed on February 1, 2018. ResMed's fiscal-year 2017 report was filed on August 4, 2017. Both therefore precede the same April hearing. ResMed does not appear by name in the saved hearing text; its inclusion allows us to examine a connection that direct firm-name matching would miss.

The full corpus supplies repeated annual filings, but this hearing-linked LLM run uses one selected filing per firm. It therefore produces a snapshot of directional discussion; constructing annual threat and opportunity trajectories requires tagging the additional filings.

The selection rule concerns availability within this historical sample. It does not restrict the firms to contemporaneous S&P 500 membership or impose an expiration date on their last filing. **289 of the 998 selected disclosures are more than two years old** at the hearing date. The output retains filing dates and filing age so those observations remain identifiable.

> **Coauthor note — sample timing.** Before using these links to estimate contemporaneous firm exposure, decide whether to require active firms, contemporaneous index membership, or a maximum filing age. The current example follows the latest-available-filing rule across the project's historical firm sample. It does not establish that all 998 firms were active S&P 500 constituents in April 2018.

**2. Prepare the business descriptions as numbered sentences.** The [sentence-preparation notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/01_item1_sentences.ipynb>) segments paragraph blocks with `pysbd==0.3.4` and removes sentences shorter than 30 characters. This filters many headings and fragments before computing relevance. It then identifies repeated forms across firms: text is lowercased, digit sequences are replaced by a common marker, and punctuation and whitespace are removed for comparison. A normalized form occurring in at least 20 distinct firms is excluded as potential boilerplate. The original wording of retained sentences is preserved.

Across the full corpus, segmentation produces 7,848,199 sentences. The length filter retains 6,331,719, and the cross-firm filter removes a further 24,926, leaving **6,306,793 sentences**, with a median of 239 per filing. These rules reduce repeated or fragmentary text; they do not establish that every retained sentence describes a substantive business activity. The notebook reports removal-rate comparisons for alternative boilerplate thresholds, making the effect of that choice observable.

The 998 selected filings contain **298,651 retained sentences**. Facebook contributes 78 and ResMed 484. Each sentence carries its filing identifier, firm identifiers, fiscal year, and position after filtering. The [numbered example inputs](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/01 - Inputs/numbered_sentences.md>) use that position plus one as the displayed sentence number. Thus, an LLM citation can be resolved to a specific stored row.

**3. Construct the common privacy-topic representation.** The [topic-vector notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/02_topic_centroids_scores.ipynb>) starts with the frozen codebook definition and the hearing sentences cited by stance records assigned to each topic in Section 4. It retains records meeting the 0.68 assignment threshold, retrieves their cited sentences, and removes duplicate sentence texts within each topic. Across all 111 topics, this produces **37,104 topic–sentence pairs**. The median topic has 263 distinct evidence sentences and the smallest has 27.

Topic 68's definition concerns federal and state laws, proposed bills, and regulatory frameworks addressing the collection, use, and protection of consumer personal information. Its numerical representation combines that definition with **474 distinct hearing sentences**. Each text is embedded with `BAAI/bge-large-en-v1.5`; the code averages the 475 embeddings with equal weight and normalizes the resulting vector. The definition therefore contributes one input alongside the evidence sentences, not half of the combined weight.

This representation differs from the phrase-based category vectors used to assign stances in Section 4. There, the inputs were Track 1 topic phrases. Here, the inputs are the definition and the actual hearing sentences supporting assigned stances. The latter supply examples of how the subject is discussed in the hearings, although errors in the upstream stance or topic assignments can enter the representation.

The topic vector is fixed across firms and years. It pools evidence from the full hearing corpus, including hearings after April 2018, rather than representing only Zuckerberg's testimony. The resulting score is a retrospective measure of relatedness to the common privacy category. Selecting an earlier firm filing establishes the disclosure's timing; it does not make the full measurement procedure an information set available before the hearing.

**4. Compare each disclosure with the privacy topic.** The code embeds every retained Item 1 sentence with the same encoder and computes its cosine similarity to each topic vector. The encoder processes at most 512 tokens per input, truncating longer sentence inputs. For each filing–topic combination, the code averages the **five highest sentence similarities**, or all available sentences when fewer than five remain. This concentrates the score on the closest passages while reducing reliance on a single match and avoiding dilution by the rest of a long business description.

The saved corpus contains **2,438,226 filing–topic scores** and **12,190,686 supporting sentence references**. The [example verification](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/03 - Logs and Verification/embedding_verification.json>) recomputes the two illustrations directly from the saved sentence embeddings and topic vector, checking both the selected sentences and their scores.

| Firm and selected filing | Retained sentences | Display numbers of the five selected sentences, ordered by similarity | Mean similarity | Standardized similarity |
|---|---:|---|---:|---:|
| Facebook, fiscal 2017; filed February 1, 2018 | 78 | 48, 47, 57, 56, 45 | 0.759 | 4.879 |
| ResMed, fiscal 2017; filed August 4, 2017 | 484 | 459, 468, 473, 469, 471 | 0.770 | 2.443 |

The [underlying sentences and individual scores](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/embedding_evidence.json>) show what drives these values. Facebook's closest sentence states: “In particular, we are subject to federal, state, and foreign laws regarding privacy and protection of people's data.” ResMed's closest sentence states: “New laws governing privacy may be adopted in the future as well.” Other selected ResMed passages concern medical-information privacy, breach notification, and protection of personal information. Some describe laws broadly, so high similarity alone does not establish the firm's particular obligation or its direction. The subsequent LLM assessment considers those passages within their original context.

The two score columns answer different questions. Raw similarity describes closeness to the fixed topic vector. Longer filings have more opportunities to supply high-scoring sentences: in the full corpus, average similarity rises from 0.620 in the shortest filing-length decile to 0.681 in the longest. The [descriptive-analysis notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/07_layer1_descriptives.ipynb>) therefore standardizes scores within each topic and filing-length decile, subtracting that group's mean and dividing by its standard deviation. The reference groups use the full filing corpus, not just the 998 preceding filings.

ResMed has the higher raw score, whereas Facebook is more unusual relative to filings of similar length. Neither comparison ranks the firms' economic exposure to the hearing. The [all-firm score table](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/privacy_firm_scores_before_hearing.csv>) supplies the same calculation for the full selected sample.

**5. Screen and classify the filing sentences with Qwen.** The separate LLM procedure reads the retained sentences in document order. The [block-construction notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/03_tagging_blocks.ipynb>) groups at most 40 consecutive sentences per input, retaining filing-wide numbering. It prepares 168,333 blocks across the full corpus. The privacy application uses **7,950 blocks** for the 998 preceding filings; Facebook contributes two and ResMed 13. Neither sentence similarity nor the top-five selection determines these inputs.

We use `Qwen/Qwen3.5-4B` and the existing [tagging helper](<../B - Backup of Original File Structure/scripts/python/lib/tagging.py>), prompt version `item1-topic-tagging-1.2`. Pass A presents all 111 topic labels and requests a list of plausible matches. Pass B presents the same sentence block with the definition of the topic being assessed. It returns records of the form `[sentence number, topic identifier, direction]`, where `O`, `T`, and `N` denote opportunity, threat, and neutral. Opportunity covers growth, demand, funding, or an advantage; threat covers a risk, cost, restriction, or competitive pressure; neutral indicates a connection without either implication. The [exact templates](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/01 - Inputs/prompts.md>) specify the firm's own business as the required connection.

This full-firm run focuses on **one topic**. It preserves the all-label screen, then confirms topic 68 only when the screen includes it. The original general-purpose notebook confirms all candidate topics together; restricting confirmation to the privacy definition makes the present run a targeted application of that procedure. It does not produce classifications for the other 110 topics. The code also confirms privacy without screening on a separate random sample described below.

The [prompt-development notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/04_tagging_promptbook.ipynb>) records why the two-pass design and compact responses were adopted. Screening on broad themes could hide a detailed topic under an uninformative theme label. Requesting sentence citations during screening also consumed output tokens for work repeated during confirmation, and an earlier production attempt was stopped after output truncation. The current screen returns only identifiers; confirmation returns compact triples with citations. The generation caps are 160 tokens for screening and 512 for confirmation. These changes address observed failure modes; cap hits and parsing flags remain recorded rather than assumed away.

**Sentence evidence for the running example.** From the completed run, we inspect the two highest-ranked firms in each directional figure shown in Section 5.3: Total System Services and Facebook for threat, and Paycom Software and Fidelity National Information Services (FIS) for opportunity. These cases illustrate how the recorded classifications relate to their underlying sentences; their selection follows the all-firm run and does not restrict its inputs. The table retains the model's recorded label and the original wording so readers can assess the privacy connection and the directional interpretation separately.

For Total System Services, the surrounding disclosure identifies privacy obligations applying to the firm and its financial-institution clients. The selected sentence describes increasing breach-notification scope and cost, providing a concrete basis for its threat label. Facebook's selected sentence identifies GDPR operational requirements and significant penalties for noncompliance. These passages make the threat interpretation observable as a stated cost or penalty rather than merely the presence of privacy-related language.

Paycom's selected sentence describes voluntary third-party examinations of security and privacy practices. FIS describes a global privacy program for managing risks and complying with new requirements. The model labels both passages as opportunities. Their wording establishes a privacy-related organizational response, but it does not explicitly state increased demand, revenue, growth, or competitive advantage. These examples therefore permit inspection of where the model places the boundary between compliance, risk mitigation, and opportunity.

| Firm | Filed | Sentence | Recorded LLM label | Original disclosure sentence |
|---|---|---:|---|---|
| [Total System Services](https://www.sec.gov/Archives/edgar/data/721683/000155837018001043/tss-20171231x10k.htm) | 2018-02-23 | 48 | Threat | In many jurisdictions consumers must be notified in the event of a data breach, and such notification requirements continue to increase in scope and cost. |
| [Facebook](https://www.sec.gov/Archives/edgar/data/1326801/000132680118000009/fb-12312017x10k.htm) | 2018-02-01 | 55 | Threat | The GDPR will include operational requirements for companies that receive or process personal data of residents of the European Union that are different than those currently in place in the European Union, and will include significant penalties for non- compliance. |
| [Paycom Software](https://www.sec.gov/Archives/edgar/data/1590955/000156459018002088/payc-10k_20171231.htm) | 2018-02-14 | 263 | Opportunity | We voluntarily obtain third-party security examinations relating to security and data privacy in accordance with Statement on Standards for Attestation Engagements (“SSAE”), No. 16, Reporting on Controls at a Service Organization. |
| [Fidelity National Information Services (FIS)](https://www.sec.gov/Archives/edgar/data/1136893/000113689318000011/a10-k2017.htm) | 2018-02-22 | 217 | Opportunity | The Company has adopted a comprehensive global privacy program to assess and manage these evolving risks, including contract terms to comply with this new law. |

*Evidence behind the leading directional ranks. Total System Services and Facebook rank first and second on threat; Paycom and FIS rank first and second on opportunity. Company links lead to the original filings. Sentence numbers refer to the retained, numbered Item 1 text. The [table data](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_evidence_table.csv>) preserve filing identifiers, and the [complete examples](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_directional_examples.md>) provide all accepted tags, numbered input blocks, and recorded responses for these four firms. The selected sentences illustrate model outputs; they do not independently validate the labels or ranks.*

The same examples show the value of linking firms through the shared topic. Total System Services is assigned to NAICS 522, while Paycom and FIS are assigned to NAICS 518; Facebook is in NAICS 519. The checked names and aliases for the other three firms do not appear in the saved hearing. Their privacy passages identify connections that the specified name-matching and same-industry rules would omit. The four selected filings were available 45–67 days before the hearing, keeping the disclosure evidence close to the running example's date.

Source inspection also identifies limits to these classifications and the rankings constructed from them. Total System Services' accepted tags include neighboring subjects such as debit interchange fees and wage-payment rules. Paycom's opportunity tags include quality-management certification and certification-expiration statements, and FIS's opportunity passages emphasize safeguards and compliance. Such assignments can inflate topic counts or treat a protective response as a business opportunity. We preserve these recorded outputs and identify the interpretive issue explicitly: the selected threat passages state adverse implications, while the selected opportunity labels require further substantive review before being interpreted as evidence of a business benefit. The [figure and table script](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/render_llm_relevance_figures.py>) reproduces the rankings and examples and verifies their recorded prompts without making new model calls.

**6. Aggregate the classifications and attach the hearing.** The [assembly script](<../T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.2 - Panel Assembly and Empirical Descriptives.py>) checks that every scheduled block has a result, reconstructs each prompt and its hash, and parses the saved responses again. The parser accepts only sentence numbers shown in the input, topic identifiers supplied to the call, and permitted directions. It removes duplicate sentence–topic pairs. These checks establish structural consistency, not substantive accuracy.

For each firm, the script counts distinct privacy-tagged sentences and their division into opportunity, threat, and neutral. Their sum is the total extent of tagged discussion. A relevance indicator equals one when at least one qualifying tag is retained. A zero means that the completed, structurally clean screened procedure found no tag; it does not prove that the topic is irrelevant. If a filing has flagged or capped calls and no accepted tags, the indicator remains missing. When positive tags coexist with flagged calls, the output retains those tags and identifies the filing for review, since its sentence count may be incomplete.

Directional shares divide each direction's count by the total tagged sentences and remain undefined when the total is zero. A further descriptive share divides tagged sentences by all retained filing sentences, making the denominator explicit when comparing disclosures of different lengths. These are counts and shares of model-classified text, not measures of regulatory severity. A neutral tag still contributes to the relevance indicator and to the total discussion count.

For directional comparisons, we construct separate rankings for threat and opportunity. The threat measure divides sentences tagged as privacy-related threats by all retained sentences in that firm's disclosure; the opportunity measure uses opportunity-tagged sentences with the same denominator. Neutral tags enter neither numerator and cannot raise a firm's rank. These measures describe how much of a disclosure the model assigns to each direction, rather than the severity of a threat or the value of an opportunity. Dividing by all filing sentences also distinguishes a filing with one threat sentence from a filing with extensive threat discussion, even when all privacy tags in both filings are threats.

The final row joins these measures to the saved embedding score, firm identifiers, selected filing and its date, topic 68, and the April 10 hearing identifier. The shared topic establishes the connection: the LLM is judging a filing's relationship to the codebook definition, not directly judging whether Zuckerberg's testimony affected that firm. All sentence references remain available for inspection.

<!-- TOPIC68_RUN_STATUS_START -->
The completed privacy run covers **998 firms and 7,950 blocks**, with 8,789 model calls verified against their recorded prompts. It retains **1,044 privacy sentence–topic records**. At least one record is retained for **129 firms**; 782 receive a zero indicator and 87 remain unknown under the processing-quality rule. The run records 31 generation-cap hits; 104 filings have flagged calls and remain identifiable for review.

The two illustrations contribute the following model classifications:

| Firm | Accepted privacy sentences | Opportunity | Threat | Neutral | Flagged blocks |
|---|---:|---:|---:|---:|---:|
| RESMED INC | 20 | 0 | 20 | 0 | 0 |
| Facebook Inc | 15 | 0 | 15 | 0 | 0 |

The [sentence-level classifications](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_records.md>) retain the original text, and the [full firm table](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/hearing_firm_privacy_panel.csv>) supplies the corresponding measures for every selected firm. Directional shares divide each direction's count by the accepted total; counts from flagged filings require review before being treated as complete.

For Facebook, the model classifies [sentence 52](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_records.md#0001326801-18-000009-sentence-52>) as **threat**: “Proposed or new legislation and regulations could also significantly affect our business.” This is a recorded model judgment whose interpretation can be checked against the surrounding input block.

For ResMed, the model classifies [sentence 471](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_records.md#0001193125-17-248016-sentence-471>) as **threat**: “Congress has also been considering similar federal legislation relating to data breaches.” This is a recorded model judgment whose interpretation can be checked against the surrounding input block.
<!-- TOPIC68_RUN_STATUS_END -->

**7. Calculate the combined privacy indices.** We implement the measure defined in Section 5.1 as a new extension after the two original procedures have run independently. It combines sentence similarity with the recorded LLM direction without changing the model's inputs or labels. This extension was calculated for the present privacy application and was not part of the original implemented design.

The [combined-score script](<../T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.3 - Similarity-Weighted Directional Scores.py>) joins each accepted tag to its saved embedding using the filing identifier and sentence position, checks the original wording, and computes cosine after re-normalizing the stored vectors. It uses each tagged sentence's own similarity, rather than multiplying the entire filing by its top-five average or standardized score. No additional model calls are needed. The original similarity and classification measures remain available for the independent agreement comparison in step 8.

The new panel retains all **998 firms** and supplies final scores for **894 filings without processing flags**. A clean filing with no tags for a direction receives zero; all 104 flagged filings receive missing final scores because their counts may be incomplete. Accepted records and their observed weighted sums remain available for those filings. Numerical checks verify all 1,044 tags against the original counts and confirm that sentence contributions reproduce each published score. These checks establish computational consistency; independent review of relevance and direction is still needed before claiming improved measurement accuracy.

All observed tag weights in this run are positive, so the weighting reduces contributions without discarding tags.

**Worked calculation and sentence comparisons.** The new calculation assigns less weight to a tagged sentence when its embedding is less closely related to the privacy topic. The table compares the unweighted directional shares underlying the figures in Section 5.3 with the combined indices for the same four firms. The original LLM labels are retained in both calculations.

| Firm | Unweighted threat (%) | Weighted threat | Unweighted opportunity (%) | Weighted opportunity |
|---|---:|---:|---:|---:|
| Total System Services | 24.14 | 16.03 | 0.00 | 0.00 |
| Facebook | 19.23 | 13.65 | 0.00 | 0.00 |
| Paycom Software | 1.67 | 1.25 | 2.67 | 1.46 |
| Fidelity National Information Services (FIS) | 9.27 | 6.16 | 1.16 | 0.81 |

*Calculated privacy indices. Unweighted values are directional tag counts per 100 retained filing sentences. Weighted values sum sentence similarities within each direction using the same denominator. The [four-firm calculation table](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_weighted_firm_examples.csv>) includes counts, mean weights, filing identifiers, and ranks; the [complete panel](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/hearing_firm_privacy_weighted_panel.csv>) retains all 998 firms and flags unavailable scores.*

For Facebook, the 15 threat sentences among 78 retained sentences have a mean weight of 0.709621. Its combined threat score is therefore $(100\times15/78)\times0.709621=13.65$. Paycom's eight opportunity sentences among 300 have a mean weight of 0.548507, giving $(100\times8/300)\times0.548507=1.46$. Total System Services and Facebook remain first and second on weighted threat; Paycom and FIS remain first and second on weighted opportunity among the 894 eligible filings. Lower numerical values follow from weights bounded by one and do not, by themselves, demonstrate better accuracy.

The sentence comparisons below show both the motivation for weighting and its limits. Descriptions abbreviate the source text; the [full sentence table](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/02 - Worked Cases/privacy_weighted_sentence_examples.md>) preserves the original wording, labels, weights, and individual score contributions.

| Firm | Recorded direction | First sentence and weight | Comparison sentence and weight | What the comparison shows |
|---|---|---|---|---|
| Total System Services | Threat | Sentence 48: increasing breach-notification costs; **0.740** | Sentence 62: regulation of debit interchange fees; **0.591** | The explicit privacy cost receives greater weight than a neighboring regulatory subject. |
| Facebook | Threat | Sentence 55: GDPR requirements and penalties; **0.686** | Sentence 56: obligations concerning third-party copyright infringement; **0.740** | The copyright passage receives greater weight despite its weaker fit to the privacy definition. |
| Paycom Software | Opportunity | Sentence 263: examinations of security and data privacy; **0.634** | Sentence 268: quality-management certification; **0.510** | Weighting reduces the certification passage's contribution, but does not establish a business benefit in either sentence. |
| Fidelity National Information Services (FIS) | Opportunity | Sentence 217: a privacy compliance program; **0.653** | Sentence 233: safeguards for consumers' personal information; **0.743** | Both passages concern privacy; their opportunity labels still require substantive justification. |

Weighting therefore supplies a continuous topic-relatedness component, not an automatic correction of relevance or direction. The Facebook comparison shows that an off-topic assignment can retain substantial weight. The Paycom and FIS comparisons show why privacy safeguards or compliance cannot be interpreted as a business opportunity solely because they concern the topic. A useful evaluation must compare weighted and unweighted measures against independently reviewed relevance and direction, including doubtful and untagged passages; agreement between the two components cannot establish that the combination is more accurate.

**8. Assess screening, interpretation, and agreement separately.** The run includes a seeded sample of **60 blocks** from the 7,950-block application. On those blocks, privacy confirmation is obtained even when the screen omits the topic. A block counts as a screening miss when this direct confirmation retains privacy evidence but Pass A did not select privacy. The script reports the fraction of confirmed audit blocks missed, together with the number of usable audit observations and any parsing or cap problems. This targets a gap that reviewing retained tags cannot address: relevant passages excluded before confirmation. The audit outputs remain separate from the production counts.

The assembly also exports up to 100 confirmed sentences and 50 unconfirmed probes for human review, with relevance and direction fields left blank. That review addresses whether a sentence actually concerns the firm's business under the definition and whether the assigned direction follows from its wording. It is distinct from the screening audit, whose alternative confirmations still come from the same model. The earlier [general audit notebook](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/05_gate_audit_gold.ipynb>) specifies a broader all-topic comparison; the present audit assesses privacy within this hearing-linked sample.

Finally, the code compares standardized similarity across firms with and without accepted privacy tags, then reports the percentage of firms with tags within each similarity quintile. These comparisons make the correspondence across the sample observable beyond a few selected examples. The [saved assessment](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/03 - Evaluation and Figures/assessment.json>) also retains the Spearman correlation between similarity and the share of retained sentences tagged, which is 0.461 among the 894 unflagged filings. This statistic concerns tagged discussion, not its direction. Flagged filings are excluded from the agreement calculations and counted separately. Agreement remains a measurement diagnostic: both methods depend on the codebook and source text, and neither substitutes for independent human validation.

For the directional rankings, we also compare topic-based connections with two simpler rules: whether a listed firm name or documented alias occurs in the saved full hearing, including appendices, and whether the firm shares Facebook's modal three-digit industry code, NAICS 519. These checks identify connections those specified rules omit; they do not provide an independent relevance gold standard.

<!-- TOPIC68_EVALUATION_START -->
In the 60-block screening audit, 0 blocks have structural or cap problems. Privacy is directly confirmed in 2 usable audit blocks; the screen missed 1 of these, a miss rate of 50.0%. These are comparisons between model procedures, not human accuracy estimates.

The agreement figure asks whether higher embedding similarity is accompanied by privacy evidence from the separate LLM procedure. It uses 894 filings without flagged calls. The left panel compares similarity between filings with and without accepted tags. The right panel orders firms by standardized similarity, divides them into five approximately equal groups, and shows the percentage in each group with at least one accepted privacy tag. This percentage uses firms as its denominator, not sentences. In the lowest-similarity group, 0 of 179 firms have tags (0.0%); in the highest group, 87 of 179 do (48.6%). These bars show how often similarity is accompanied by a model-retained passage. Similarity remains a continuous score; the LLM supplies specific sentences and their directional labels. A tag can indicate threat, opportunity, or neutral relevance. The figure assesses correspondence, while the directional figures in Section 5.3 examine what the LLM adds about implications. Independent human validation remains incomplete.

![Privacy similarity and LLM evidence across firms](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_measure_agreement.svg>)

*Privacy-measure agreement. Each observation is one firm's latest available filing before April 10, 2018. Left: boxes show the middle 50 percent and median of standardized similarity, with whiskers extending to observations within 1.5 interquartile ranges and more distant points hidden. Similarity is standardized within topic and filing-length decile. Right: bars show the fraction of firms with any accepted privacy tag within each similarity quintile, expressed as a percentage; the denominator is all firms in that quintile. Quintiles are defined using similarity alone. The [group counts and score ranges](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/03 - Evaluation and Figures/privacy_agreement_quintiles.csv>) reproduce the bars. Filings with flagged calls are excluded. Absence of a tag is a model outcome, not proof of irrelevance; neither panel establishes classification accuracy or economic effects.*
<!-- TOPIC68_EVALUATION_END -->

### 5.3. Research Outputs

The outputs let a researcher move from a hearing–firm connection to the specific text and computation supporting it. They distinguish corpus-wide similarity results, the privacy-specific LLM assessment, and the new combined indices:

| Output | What a row or file represents | Research use |
|---|---|---|
| Prepared sentence table and aligned embeddings | One retained Item 1 sentence with its filing, firm, fiscal year, and position; one matching vector per row. | Retrieve evidence, recompute similarity, and examine preprocessing choices. |
| Topic index and fixed vectors | One definition-and-evidence representation per topic, with its supporting sentence count. | Identify the common reference used across firms and years. |
| Corpus similarity and evidence tables | One score per filing and topic, plus up to five contributing sentence references. | Compare semantic relatedness and inspect what produces a high score. |
| Privacy classification records and call logs | Accepted sentence-level tags, screening results, raw responses, prompts, hashes, and processing flags for the selected filings. | Inspect relevance and direction and distinguish a model decision from a failed call. |
| Hearing–firm privacy table | One row per selected firm, connecting its preceding filing to the April hearing through topic 68. | Compare similarity, presence of tagged evidence, sentence counts, direction, and disclosure age within the same sample. |
| Audit and human-review files | Direct privacy confirmations on the sampled blocks and sentences prepared for independent review. | Examine screening omissions and evaluate substantive judgments separately. |
| LLM ranking and cross-industry examples | Separate firm rankings by threat and opportunity sentences as shares of the disclosure, with a source-evidence table and explicit name and industry comparisons. | Locate connections that simple matching rules omit and inspect both supporting passages and questionable model tags. |
| Similarity-weighted directional panel and sentence contributions | Separate threat and opportunity indices for each eligible filing, plus every accepted sentence's cosine, label, and contribution. | Compare the combined measure with unweighted counts and trace a score to its evidence; retain missing scores for flagged filings. |

The first four descriptive exhibits use the full corpus similarity results to examine firm, industry, and time patterns. They use the [saved score calculations](<../B - Backup of Original File Structure/scripts/python/04_topic_relevance/07_layer1_descriptives.ipynb>). Two further figures use the completed LLM privacy assessment to rank threat and opportunity discussion separately. The sentence tables and worked calculations in Section 5.2 trace the evidence behind these directional measures and the combined indices. Three-digit NAICS classifications are available for 1,060 of the 1,061 firms, covering 84 industries. Each firm's industry is fixed at its most frequent NAICS3 code in the linked reference data. The first three figures use the full table, whose fiscal-year metadata span 1992–2026; the time-series figure explicitly restricts its display to 1995–2025. The LLM exhibits use the selected filings preceding the April 2018 hearing.

**1. Which firm–topic connections receive the highest scores?** The first figure displays the 15 firm–topic pairs with the highest mean standardized relevance, requiring at least three filings per pair. Each row names a firm and a topic, and its horizontal position is the mean of that firm's standardized filing scores for that topic. Averaging several filings reduces reliance on a single disclosure.

Embarq's connection to the Universal Service Fund has a mean of 5.612, and T-Mobile's connection to spectrum policy has a mean of 5.058. United Airlines and Essential Air Service score 4.481; Norfolk Southern and Positive Train Control and Rail Safety Legislation score 4.333. These are unusually close textual matches relative to filings of comparable length. They identify cases whose contributing sentences can be inspected; they are neither probabilities nor estimates of policy effects.

![Firm–topic pairs with the highest average standardized similarity](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_relevance_top_pairs.svg>)

*Highest-scoring firm–topic pairs. Points show mean standardized similarity across a firm's filings for one topic, with at least three filings required. Standardization uses the topic and filing-length decile. The figure covers all 111 topics and does not use the LLM privacy classifications.*

**2. Which industries are closest to the hearing topics overall?** A few high-scoring firms cannot establish whether the collection of topics systematically relates to different industries. The second figure first averages each firm's standardized scores across filings and all 111 topics, then averages those firm values within industries. Each firm contributes equally. The display includes the eight highest and eight lowest industry means among industries containing at least eight firms.

Telecommunications has a mean of 0.670, with an approximate 95-percent interval of [0.401, 0.938], and Transportation Equipment has a mean of 0.424, with an interval of [0.224, 0.624]. Bars locate these industry averages, and whiskers show uncertainty calculated across firms. Positive values indicate greater average similarity to this collection of hearing topics. Negative values indicate lower average similarity, not an absence of relevant subjects. Because the topics enter equally, this measure does not weight an industry by how often Congress discussed its concerns.

![Average standardized similarity across industries](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_relevance_industry_exposure.svg>)

*Industry-wide relatedness. Bars show the mean of firm-level averages across filings and all topics; whiskers are approximate 95-percent intervals across firms. Parentheses give firm counts. The comparison weights firms equally and requires at least eight per industry.*

**3. Which topics are closest within each industry?** An industry-wide average can conceal a strong connection to a small number of subjects. The third figure separates eight industries and displays the three topics with the highest mean standardized filing scores within each. The notebook specifies the industries, while the calculated scores determine their leading topics. Each point locates an industry–topic mean.

Telecommunications scores highest on the Universal Service Fund (3.432), spectrum policy (3.093), and broadband deployment and infrastructure (2.902). Utilities scores highest on Smart Grid and Grid Modernization (1.642), the Clean Power Plan (1.538), and Renewable Energy Technologies and Storage (1.284). Air Transportation's leading matches include Essential Air Service (4.173), the Next Generation Air Transportation System (3.858), and aviation safety and certification policy (3.611).

These patterns permit inspection of whether the measure distinguishes recognizable subjects within industries. Here the averages are taken directly across filings, so a firm with more filings receives more weight than one with fewer. This differs from the preceding industry-wide comparison and should be considered when interpreting the values.

![Highest-scoring topics within selected industries](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_relevance_industry_topics.svg>)

*Industry-specific subjects. Each industry block lists its three topics with the highest standardized similarity, averaging across filings. Industry selection is fixed in the notebook; topic selection follows the scores. Firms with more filings contribute more observations.*

**4. How does industry–topic relatedness change over time?** A pooled average does not reveal whether a connection is persistent or concentrated in particular years. The fourth figure follows six industry–topic pairs, selecting each industry's highest-scoring topic from the preceding calculation. Each panel plots fiscal year horizontally and the mean standardized score of that industry's filings in the year vertically.

Telecommunications' similarity to the Universal Service Fund increases from 2.556 in 1995 to 3.727 in 2025, reaching 4.203 in 2009. Utilities' similarity to Smart Grid and Grid Modernization rises from 1.107 to 2.240 over the displayed period. These movements describe changes in disclosed content and filing composition relative to the common reference. They do not establish a change in congressional attention or a policy's causal effect.

The dashed zero line is the pooled standardization reference, not a separately computed all-industry average for each year. Topic representations stay fixed, and labels referring to particular legislation function as retrospective categories when applied to earlier filings. The [figure export script](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/render_relevance_figures.py>) reproduces the notebook's calculations while correcting the earlier captions' date range and zero-line description.

![Industry–topic similarity over fiscal years](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_relevance_industry_trends.svg>)

*Changes within industry–topic pairs. Lines show annual means for six pairs over fiscal years 1995–2025. The dashed line is the fixed zero reference from pooled topic-and-length standardization. Both changing disclosures and the composition of filing firms can change the observed series.*

**5. Which firms describe privacy as a threat or an opportunity?** The following figures rank firms using the unweighted directional shares defined in Section 5.1 and calculated in Section 5.2. They show the extent of threat and opportunity discussion separately.

Both rankings use the **894 filings without processing flags**. The 104 filings with flagged calls remain in the full output but are excluded from these figures because their counts may be incomplete. The filing selected for each firm is its latest available disclosure filed before April 10, 2018. This date restriction keeps post-hearing disclosures out of the comparison; it does not establish that the firm was a contemporaneous S&P 500 constituent. The topic representation remains the retrospective category described in Section 5.2.

The threat figure displays the highest 15 values among the 101 firms with at least one threat tag. Total System Services ranks first, with 21 of 87 sentences tagged as threats (24.1 percent); Facebook follows with 15 of 78 (19.2 percent); Fidelity National Information Services ranks third with 24 of 259 (9.3 percent). ResMed ranks eleventh at 4.1 percent, and AmerisourceBergen ranks fourteenth at 3.8 percent.

![Firms ranked by privacy threat discussion](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_llm_threat.svg>)

*Privacy threat discussion. Bars show threat-tagged sentences as a percentage of all retained sentences in the selected filing, ordered from highest to lowest. The figure displays the top 15 among 894 filings without processing flags. Neutral and opportunity tags do not contribute to the numerator. Counts are recorded model outputs, not validated measures of economic harm.*

Opportunity tags are much less frequent: **16 sentences across seven firms** in the same sample. The second figure displays all seven firms with positive values. Paycom Software ranks first with eight of 300 sentences tagged as opportunities (2.7 percent), followed by Fidelity National Information Services with three of 259 (1.2 percent). Each remaining firm has one accepted opportunity tag. The figure uses its own horizontal scale because the opportunity shares are considerably smaller; their precision and meaning should be assessed from the underlying passages.

![Firms ranked by privacy opportunity discussion](<../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_llm_opportunity.svg>)

*Privacy opportunity discussion. Bars show opportunity-tagged sentences as a percentage of all retained filing sentences, ordered from highest to lowest. All seven firms with positive counts are displayed; the other 887 filings without processing flags have zero accepted opportunity tags. The denominator and eligibility rules match the threat figure, while the horizontal scale differs. Neutral and threat tags do not contribute to the numerator.*

Applying the name and industry comparisons described in Section 5.2, nine of the 15 displayed threat firms and six of the seven opportunity firms satisfy neither rule. The [saved checks](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/03 - Logs and Verification/llm_figure_verification.json>) and [directional ranking tables](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/02 - Outputs/01 - Full Sample/privacy_llm_ranking.csv>) record the comparisons. These are additional candidate connections, not independently validated omissions: the name search is limited to documented aliases, and matching Facebook's industry is one specific industry rule.

---

## 6. Research Outputs, Reproducibility, and Application to Future Research

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

The full templates are available with the worked inputs for each stage: [T1 summarization](<../T1 - Text Summarization/T1.X - Worked Example/README.md#map-prompt>), [T2 topic and stance extraction](<../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/01 - Inputs/prompts.md>), and [T3 relevance and direction](<../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/01 - Inputs/prompts.md>). The summarization prompts are reproduced below; the linked files retain the templates and substitutions used in the other stages.

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
