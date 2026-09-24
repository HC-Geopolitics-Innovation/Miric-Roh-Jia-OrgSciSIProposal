# T3 worked example: the Zuckerberg hearing and firms' privacy relevance

This example continues the **April 10, 2018** hearing, *Facebook, Social Media Privacy, and the Use and Abuse of Data* (`CHRG-115shrg37801`). Its saved primary category is **topic 68, consumer data privacy legislation**. The count tie and proposed alternative tie-breaking rule remain documented in the [T2 example](<../../T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/README.md>) and manuscript.

The assessment covers **998 firms**, using each firm's latest usable Item 1 disclosure filed before the hearing. **Facebook and ResMed are two illustrations within that sample.** The run processes all 7,950 blocks and 298,651 retained sentences in those filings. It does not select firms or LLM input sentences by embedding similarity.

<!-- RUN_STATUS_START -->
The full run is complete: **998 firms, 7,950 blocks, and 8,789 verified calls**. It retains 1,044 privacy tags. See the [all-firm panel](<02 - Outputs/01 - Full Sample/hearing_firm_privacy_panel.csv>), [assessment](<02 - Outputs/03 - Evaluation and Figures/assessment.json>), and [two illustrations](<02 - Outputs/02 - Worked Cases/privacy_records.md>). Processing flags remain visible; independent human validation is not yet complete.
<!-- RUN_STATUS_END -->

## 1. What the files contain

| Folder | Contents |
|---|---|
| [01 - Inputs](<01 - Inputs/>) | Codebook and prompts; Facebook/ResMed filing metadata and numbered blocks. Original Item 1 texts for all five illustrated firms are grouped in [Source Filings](<01 - Inputs/Source Filings/>). |
| [02 - Outputs / 01 - Full Sample](<02 - Outputs/01 - Full Sample/>) | All-firm similarity scores, the original and similarity-weighted panels, directional rankings of unflagged filings, and all 1,044 weighted sentence records. |
| [02 - Outputs / 02 - Worked Cases](<02 - Outputs/02 - Worked Cases/>) | Facebook/ResMed similarity and classification records; the four leading directional examples; readable evidence and weighted-score tables with their structured data. |
| [02 - Outputs / 03 - Evaluation and Figures](<02 - Outputs/03 - Evaluation and Figures/>) | Run assessment, pending human-review candidates, agreement-figure groups, and the threat/opportunity display tables. Figure files remain in the shared results directory. |
| [03 - Logs and Verification](<03 - Logs and Verification/>) | Embedding, figure, and weighted-score checks; recorded model calls and verified prompts for the illustrations; full-run configuration; and explicit hearing-name and industry comparisons for the firms in the directional plots. |
| [04 - Scripts](<04 - Scripts/>) | Export/verification, GPU submission, dependent assembly, an aggregation check, and reproduction of the four corpus-similarity figures and two LLM directional figures and an evidence table. |

For a quick reading, start with the [four-firm evidence table](<02 - Outputs/02 - Worked Cases/privacy_evidence_table.md>) and [weighted-score examples](<02 - Outputs/02 - Worked Cases/privacy_weighted_firm_examples.md>). Use the [weighted all-firm panel](<02 - Outputs/01 - Full Sample/hearing_firm_privacy_weighted_panel.csv>) for analysis; it adds the combined measures to the original panel. The [original panel](<02 - Outputs/01 - Full Sample/hearing_firm_privacy_panel.csv>) preserves the results before this extension, and the [similarity-only table](<02 - Outputs/01 - Full Sample/privacy_firm_scores_before_hearing.csv>) documents Track 1 independently of the LLM assessment.

Readable Markdown tables and their JSON/CSV counterparts are kept together: the former support inspection, and the latter preserve fields for analysis. The two call logs cover Facebook/ResMed and the four directional examples respectively; their Facebook calls overlap because Facebook appears in both walkthroughs. Both retain the executed prompts and responses. The [human-review table](<02 - Outputs/03 - Evaluation and Figures/human_review_candidates.csv>) remains an unfinished evaluation asset, not a completed validation result. The input codebook is a frozen copy of T2's output.

The source files keep their SEC accession identifiers so they can be matched directly to sentence records:

| Firm | Saved Item 1 text | Role in the example |
|---|---|---|
| Facebook | [0001326801-18-000009](<01 - Inputs/Source Filings/0001326801-18-000009_source.txt>) | Similarity/LLM comparison and threat example. |
| ResMed | [0001193125-17-248016](<01 - Inputs/Source Filings/0001193125-17-248016_source.txt>) | Similarity/LLM comparison. |
| Total System Services | [0001558370-18-001043](<01 - Inputs/Source Filings/0001558370-18-001043_source.txt>) | Threat example. |
| Paycom Software | [0001564590-18-002088](<01 - Inputs/Source Filings/0001564590-18-002088_source.txt>) | Recorded opportunity example; interpretation requires review. |
| Fidelity National Information Services | [0001136893-18-000011](<01 - Inputs/Source Filings/0001136893-18-000011_source.txt>) | Recorded opportunity example; interpretation requires review. |

Large run inputs and logs are stored outside the repository at `/project2/njia_1089/acroh/data/output/topic68_relevance_20180410`. They contain the frozen selection and codebook, selected sentences, blocks, per-shard events with complete prompts and responses, GPU runtime information, and the final all-firm outputs. The original saved data under `/project2/mmiric_1435/acroh/llm_method/data` are read without modification.

## 2. Select the disclosure available before the hearing

Selection uses **filing date**, not fiscal year. It takes the most recent available filing before April 10, 2018 for each GVKEY in the historical sample.

| Firm | Fiscal year | Filing date | Accession | Sentences | Blocks |
|---|---:|---|---|---:|---:|
| Facebook | 2017 | February 1, 2018 | `0001326801-18-000009` | 78 | 2 |
| ResMed | 2017 | August 4, 2017 | `0001193125-17-248016` | 484 | 13 |

The sample includes firms ever classified as S&P 500 constituents in the source project; it is not the contemporaneous April 2018 index. The latest-available rule imposes no freshness cutoff: 289 selected filings are more than two years old. Filing age is retained. This selection and its limitations are explicit in the manuscript.

The saved hearing text does not name ResMed. That makes the medical-device firm a useful illustration of a connection through a shared subject, beyond directly matching firm names in the hearing.

## 3. Construct and verify the similarity score

The privacy representation averages **475 embeddings**: the codebook definition and **474 distinct hearing evidence sentences** assigned to topic 68. It is normalized and fixed across filings. This uses the full hearing corpus, including later hearings; it is a retrospective topic representation.

The encoder is `BAAI/bge-large-en-v1.5`. Each filing's score averages its five closest sentence embeddings to the privacy vector. These scores already existed in the saved corpus. The exporter recomputes both illustrations from the stored vectors and checks all five sentence selections and cosines, with a numerical tolerance of `2e-6`.

| Firm | Top-five mean cosine | Within-topic, within-length-decile z-score |
|---|---:|---:|
| Facebook | 0.759330 | 4.879 |
| ResMed | 0.769908 | 2.443 |

See [embedding evidence](<02 - Outputs/02 - Worked Cases/embedding_evidence.json>), [verification](<03 - Logs and Verification/embedding_verification.json>), and [all 998 preceding-filing scores](<02 - Outputs/01 - Full Sample/privacy_firm_scores_before_hearing.csv>). Sentence numbers displayed to the model are the saved `sent_idx + 1`. The standardization reference uses all filings in the original corpus for this topic and length decile.

## 4. Run the LLM assessment for all firms

The [production script](<../T3.2 - Process Execution/T3.2.1 - Production Batch Tagging Pipeline.py>) reuses the original [tagging helper](<../../B - Backup of Original File Structure/scripts/python/lib/tagging.py>) and its `item1-topic-tagging-1.2` prompts:

1. Pass A reads each consecutive block alongside **all 111 labels** and identifies plausible topics.
2. When privacy is among the candidates, Pass B reads the same block alongside **topic 68's definition only**. It returns `[sentence number, topic ID, "O"|"T"|"N"]` records.
3. The existing parser checks sentence indices, topic IDs, and directions and deduplicates sentence–topic pairs. It records rejected or salvaged outputs and generation-cap hits.
4. A seeded **60-block audit** also obtains privacy confirmation without screening. These audit tags remain separate from production tags.

The all-label screen preserves the original candidate-selection procedure. Confirmation is intentionally restricted to the topic requested for this run. This differs from the original general-purpose notebook, which confirms all candidate topics together. The run does not classify the other 110 topics.

The model is `Qwen/Qwen3.5-4B`, using the cached snapshot `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`, bfloat16 on GPU, and the original temperature-0.1 sampling settings and content-based seeds. The limits remain 160 generated tokens for screening and 512 for confirmation. Runtime manifests record library versions, GPU type, and input/helper hashes; they do not promise identical generations across different hardware or software.

Four resumable shards divide blocks by their saved index modulo four, with at most two GPU tasks running concurrently. Completed blocks are retained, and a shard lock prevents two processes from writing the same result stream. Input and helper hashes must match before a task resumes.

## 5. Assemble, evaluate, and link the outputs

The [assembly script](<../T3.2 - Process Execution/T3.2.2 - Panel Assembly and Empirical Descriptives.py>) refuses to publish a final panel until every scheduled block is present. It reconstructs prompts, verifies their hashes, and reparses the recorded responses. The final table has one row per selected firm and includes:

- Hearing, topic, firm, and filing identifiers; fiscal year, filing date, and filing age.
- Raw and standardized similarity and the number of retained filing sentences.
- Accepted privacy-sentence counts, separate opportunity/threat/neutral counts, directional shares, and the share of retained sentences tagged.
- A relevance indicator and processing-quality information.

An unflagged filing with no accepted tags receives zero. A filing with flagged or capped calls and no accepted tags receives a missing indicator, preserving the difference between a negative result and uncertain processing. Positive records remain available alongside their flags. Zero accepted tags is a model outcome, not proof that the firm is unaffected by privacy policy.

The audit estimates screening omissions among structurally usable, directly confirmed audit blocks. The output also prepares up to 100 confirmed sentences and 50 unconfirmed probes for human review; their verification fields stay blank. The agreement figure uses 894 unflagged filings. Its left panel compares similarity distributions for 782 firms without privacy tags and 112 with tags. Its right panel divides firms into five approximately equal groups by standardized similarity and plots the percentage of firms in each group with at least one accepted tag: 0.0%, 2.8%, 4.5%, 6.7%, and 48.6%, from lowest to highest similarity. Each bar's denominator is all firms in its quintile, rather than filing sentences. The [group counts and score ranges](<02 - Outputs/03 - Evaluation and Figures/privacy_agreement_quintiles.csv>) reproduce the plot. This replaces a scatter in which the 782 zero-tag observations overlapped on the horizontal axis. The figure uses Times New Roman, with explanation in the manuscript caption.

The agreement comparison includes tags of any direction and does not establish classification accuracy. The separate threat and opportunity figures below show the directional information supplied by the LLM. The original sentence-share Spearman correlation (0.461) remains in [assessment.json](<02 - Outputs/03 - Evaluation and Figures/assessment.json>) as an additional diagnostic; it is no longer used as the right-panel display.

The assembly/export step saves the all-firm panel and assessment here, exports the Facebook and ResMed source-linked classifications, and updates the manuscript's marked execution-status passage with the measured results. Corpus-wide LLM tagging of all 111 topics and independent human validation are outside this one-topic run.

## 6. Visualize threat and opportunity separately

The [threat figure](<../../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_llm_threat.svg>) ranks firms by threat-tagged privacy sentences divided by all retained filing sentences. The [opportunity figure](<../../R - Results/figures/T3 - Topic Relevance and Corporate Disclosure/fig_privacy_llm_opportunity.svg>) ranks opportunity-tagged sentences using the same denominator. Neutral tags do not enter either numerator. The plots contain only bars, firm labels, axes, and light grid lines; explanation and qualifications belong in the manuscript captions.

Both rankings use **894 filings without processing flags**; the 104 flagged filings remain in the original panel. There are 101 firms with threat tags and seven with opportunity tags. The threat plot shows the highest 15 values; the opportunity plot shows all seven positive values. Equal shares receive equal ranks. The [full directional measures](<02 - Outputs/01 - Full Sample/privacy_llm_ranking.csv>) retain all eligible filings, including zero values, while the [threat display table](<02 - Outputs/03 - Evaluation and Figures/privacy_llm_threat_top.csv>) and [opportunity display table](<02 - Outputs/03 - Evaluation and Figures/privacy_llm_opportunity_top.csv>) reproduce the figures.

The date restriction applies to **filings**, not firms: each selected disclosure was available before April 10, 2018. This keeps later disclosures out of the hearing-linked comparison. It does not establish contemporaneous index membership or turn the retrospective topic representation into a measure constructed entirely from information available before the hearing.

For the displayed firms, two simple baselines check whether a listed name or alias occurs in the full saved hearing and whether the firm shares Facebook's modal NAICS3 industry (519). Nine of the 15 threat firms and six of the seven opportunity firms match neither rule. The [verification record](<03 - Logs and Verification/llm_figure_verification.json>) retains the aliases and match counts. Searches ignore case and repeated whitespace and use word boundaries. This is not exhaustive entity resolution or a benchmark against all industry methods.

The [sentence evidence table](<02 - Outputs/02 - Worked Cases/privacy_evidence_table.md>) focuses on the first two firms in each directional ranking: **Total System Services and Facebook for threat; Paycom Software and Fidelity National Information Services for opportunity**. The [table data](<02 - Outputs/02 - Worked Cases/privacy_evidence_table.csv>) retain each original sentence, recorded label, filing identifier, filing date, and sentence number. Their [complete examples](<02 - Outputs/02 - Worked Cases/privacy_directional_examples.md>), [structured records](<02 - Outputs/02 - Worked Cases/privacy_directional_examples.json>), and [29 verified calls](<03 - Logs and Verification/directional_example_calls.jsonl>) preserve all accepted tags and full input context for the four firms.

Total System Services' sentence 48 describes increasing breach-notification costs; Facebook's sentence 55 describes GDPR requirements and penalties. Paycom's sentence 263 describes security examinations, while FIS's sentence 217 describes a privacy compliance program. The latter two have recorded opportunity labels but do not explicitly state a business gain. Their interpretation requires review. The full records also retain questionable assignments to neighboring regulations or certification statements; no model labels or ranking counts are manually corrected. All four selected filings were available 45–67 days before the hearing. Name checks find Facebook; the checked aliases for the other three return zero matches, and their NAICS3 codes differ from Facebook's.

## 7. Combine sentence similarity and direction

The [new scoring script](<../T3.2 - Process Execution/T3.2.3 - Similarity-Weighted Directional Scores.py>) adds an extension to the original two-instrument design. Similarity helps assess what a sentence concerns; interpretation must establish which direction its implications support. The script combines **each accepted sentence's own cosine** with its recorded direction after extraction. It leaves the original classifications and top-five filing similarity scores available separately.

For direction $d$ (threat or opportunity), firm $f$, topic $k$, and filing $t$:

$$
\operatorname{Score}^{d}_{fkt}=\frac{100}{N_{ft}}\sum_{s\in S_{ft}}\max(0,\cos(\mathbf{e}_s,\mathbf{v}_k))\,\mathbf{1}\{D_{sk}=d\}.
$$

$S_{ft}$ contains all retained filing sentences and $N_{ft}$ is its size. The vectors are the saved sentence embeddings and the fixed privacy centroid. Neutral and untagged sentences contribute zero to both numerators but remain in the denominator. The two indices stay separate so opportunity and threat do not cancel. For a nonzero tag count, each equals the unweighted directional share per 100 sentences multiplied by the mean cosine weight of those tags.

The core calculation for one eligible filing is:

```python
# vectors and direction contain this filing's accepted sentence tags.
# n_sentences counts ALL retained filing sentences, including untagged ones.
cosine = (vectors @ topic_vector) / (
    np.linalg.norm(vectors, axis=1) * np.linalg.norm(topic_vector)
)
weight = np.maximum(0, np.clip(cosine, -1, 1))
threat_score = 100 * weight[direction == "threat"].sum() / n_sentences
opportunity_score = 100 * weight[direction == "opportunity"].sum() / n_sentences
```

The production script calculates in float64 after loading the saved embeddings, correcting for small norm deviations from float16 storage. It checks that each sentence's filing identifier, position, and wording match the saved embedding index. It then verifies all 1,044 tag counts against the completed panel and checks that sentence contributions reproduce the final scores. No new LLM calls or GPU run is required.

| Firm | Illustrated direction | Tags / retained sentences | Mean weight | Unweighted score | Weighted score |
|---|---|---:|---:|---:|---:|
| Total System Services | Threat | 21 / 87 | 0.664 | 24.14 | 16.03 |
| Facebook | Threat | 15 / 78 | 0.710 | 19.23 | 13.65 |
| Paycom Software | Opportunity | 8 / 300 | 0.549 | 2.67 | 1.46 |
| Fidelity National Information Services (FIS) | Opportunity | 3 / 259 | 0.701 | 1.16 | 0.81 |

Final scores are available for **894 unflagged filings**; all **104 flagged filings** have missing final scores. Their accepted tags and observed weight sums remain available, but may be incomplete. A clean filing with no tags for a direction receives zero and has an undefined mean tag weight. All observed cosines are positive; the zero bound prevents negative contributions but does not constitute a validated relevance cutoff.

The output files are:

- [Weighted panel](<02 - Outputs/01 - Full Sample/hearing_firm_privacy_weighted_panel.csv>): all 998 original rows and columns, plus eligibility, observed directional weight sums, mean weights, unweighted and weighted scores, ranks, and a scoring-version identifier. `unweighted_threat_score` and `unweighted_opportunity_score` divide by **all retained filing sentences**; the original `threat_share` and `opportunity_share` instead describe composition among tagged sentences.
- [All sentence contributions](<02 - Outputs/01 - Full Sample/privacy_weighted_sentence_records.csv>): 1,044 recorded tags, including neutral and flagged-filing records, with text, embedding row, cosine, weight, and contribution to each directional numerator after scaling by 100 / filing length. Only unflagged filings have final published indices.
- [Four-firm calculations](<02 - Outputs/02 - Worked Cases/privacy_weighted_firm_examples.md>) and [CSV](<02 - Outputs/02 - Worked Cases/privacy_weighted_firm_examples.csv>): both directional scores, underlying counts and weights, with identifiers and ranks in the CSV.
- [Eight sentence examples](<02 - Outputs/02 - Worked Cases/privacy_weighted_sentence_examples.md>) and [CSV](<02 - Outputs/02 - Worked Cases/privacy_weighted_sentence_examples.csv>): paired illustrations of privacy costs, neighboring regulatory subjects, and ambiguous opportunity labels.
- [Verification](<03 - Logs and Verification/weighted_score_verification.json>): formulas, checks, coverage, source hashes, and embedding provenance. Copies of the four CSV files and verification are also saved in the run's `outputs/` directory.

The indices measure similarity-weighted disclosure intensity, not economic severity, probability, or literal sentence percentages. The sentence examples deliberately include a failure: Facebook's copyright sentence has weight 0.740, exceeding the 0.686 assigned to its GDPR sentence. Paycom's privacy-examination sentence receives more weight than its quality-certification sentence, but neither weighting nor the recorded opportunity label establishes a business gain. FIS's privacy compliance and safeguard statements pose the same directional interpretation issue. Independent substantive review remains necessary before claiming an improvement over unweighted counts.

Repeated filings could support trajectories using a consistent encoder, topic reference, preprocessing, and tagging procedure. The present run includes only one filing per firm. Its privacy centroid pools the full hearing corpus, including later hearings, so the resulting indices are retrospective. They do not estimate the effect of the April 2018 hearing.

## 8. Commands

Submit once from a terminal that can connect to Slurm:

```bash
bash 'T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/submit_topic_run.sh'
```

The script prints the GPU array and dependent assembly job IDs. The run root contains `gpu_job_id.txt`, `assembly_job_id.txt`, and `logs/`. Resubmitting starts resumable tasks; avoid submitting duplicates while an existing array is still active.

Re-export source text and verify the existing embeddings, without generation:

```bash
python 'T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/export_example.py' prepare
```

Run the aggregation check, which uses only temporary synthetic records:

```bash
python 'T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/check_panel_assembly.py'
```

After the full run has completed, its saved results can be re-exported without generation:

```bash
python 'T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/export_example.py' export
```

To update only the agreement figure from the saved panel, then refresh its exported assets and manuscript passage:

```bash
python 'T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.2 - Panel Assembly and Empirical Descriptives.py' --agreement-only
python 'T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/export_example.py' export
```

This uses the existing scores and tags without reassembling or generating model results. The assembly script also regenerates the figure and quintile table during a normal full assembly.

Rebuild the original four corpus-similarity figures, using the original notebook calculations with corrected caption metadata:

```bash
python 'T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/render_relevance_figures.py' /project2/mmiric_1435/acroh/llm_method/data
```

Rebuild the threat and opportunity rankings, sentence evidence table, comparisons, and case exports from the completed run, without new model calls:

```bash
python 'T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/render_llm_relevance_figures.py'
```

An optional positional argument selects a different run directory. The script checks all tag aggregates against the panel and reconstructs the case prompts before exporting SVG, PDF, and PNG figures to `R - Results/figures/T3 - Topic Relevance and Corporate Disclosure`.

Rebuild the new weighted panel and example tables from saved embeddings and tags (CPU only):

```bash
python 'T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.3 - Similarity-Weighted Directional Scores.py'
```

Use `--run-root PATH` to select the completed privacy run, or `--check` to run the numerical and missing-data checks without loading research data. The checks cover known cosine values, negative-weight clipping, neutral and untagged sentences, and the difference between a flagged filing and a clean zero. The dependent assembly job now runs this scoring step after exporting the original panel.
