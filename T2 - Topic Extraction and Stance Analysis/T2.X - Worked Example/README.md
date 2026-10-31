# Worked example: topics and stances in the Zuckerberg hearing

This continues the [Section 3 example](<../../T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>): **Facebook, Social Media Privacy, and the Use and Abuse of Data**, April 10, 2018, `CHRG-115shrg37801`. These files export the saved production results. No new LLM calls were made, and neither topic wording nor category assignments were corrected for presentation.

Use this README as the walkthrough. The supporting files use the same layout as the T1 example:

| Folder | Contents |
|---|---|
| [01 - Inputs](<01 - Inputs>) | Cleaned, numbered legislator turns and the exact example prompts. |
| [02 - Outputs](<02 - Outputs>) | Extracted hearing topics, stance records with supporting sentences, and the shared codebook. |
| [03 - Logs and Verification](<03 - Logs and Verification>) | Saved model calls and the verification counts and provenance. |
| [04 - Scripts](<04 - Scripts>) | Scripts to verify and export this example and render the stance figures. |

For a quick reading, open the [hearing topics](<02 - Outputs/topics.json>) and [readable stance records](<02 - Outputs/stance_records.md>), then follow their references to the [numbered turns](<01 - Inputs/numbered_turns.md>) and [prompts](<01 - Inputs/prompts.md>). The stance JSON preserves structured fields for reuse; the Markdown presents the same records with source links. The [call log](<03 - Logs and Verification/call_log.jsonl>) also retains responses that produced no accepted records, while [verification.json](<03 - Logs and Verification/verification.json>) reports the checks and provenance. These files serve different purposes and are all retained.

The [codebook](<02 - Outputs/codebook.json>) is an output of topic extraction. T3 keeps an identical copy among its inputs to document the categories supplied to the relevance assessment.

## 1. Start with the summary for hearing topics

Track 1 supplies the [final hearing summary](<../../T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/02 - Outputs/outputs.md#final-summary>) to Qwen/Qwen3.5-4B. The [exact prompt](<01 - Inputs/prompts.md#track-1-hearing-summary>) asks for up to five neutral topic phrases, ordered by centrality. The recorded response is:

```json
["Facebook data privacy", "content moderation", "election integrity", "Honest Ads Act", "GDPR-style controls"]
```

The code parses this list and adds ranks. [topics.json](<02 - Outputs/topics.json>) preserves these phrases, their later codebook assignments, and the hearing's primary classification. The [production notebook](<../../B - Backup of Original File Structure/scripts/python/03_topic_extraction/04_track1_production.ipynb>) describes the corpus run; the [helper](<../T2.X - Background Helper Functions/stance.py>) contains the prompt and parser.

## 2. Return to the source turns for legislators' positions

Track 2 begins with the [903 parsed records](<../../T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/01 - Inputs/parsed_turns.json>), selecting records labeled `spoken` and attributed either to a member or to the unnamed-chair identifier `0000000`. This hearing has **507 selected turns**. Witness testimony does not enter this extraction track.

The [preparation notebook](<../../B - Backup of Original File Structure/scripts/python/03_topic_extraction/01_member_turns.ipynb>) segments each paragraph with `pysbd==0.3.4`, then applies the helper's cleaning rules. They truncate a turn at the first recognized adjournment or inserted-document marker, remove the initial speaker-label echo, and drop bracketed stage directions and mostly capitalized headers. For this hearing, the rules remove 13,380 sentences by truncation, 501 label echoes, 15 stage directions, and 44 headers, leaving **1,696 sentences**. All 507 turns remain nonempty.

This cleaning differs from the summarization input. The written-response appendix retained in Grassley's final parsed record is removed here; [cleaned turn 902](<01 - Inputs/numbered_turns.md#turn-902>) contains only three closing sentences. Truncation discards the entire remainder of a matched turn; it does not identify and resume oral speech after an inserted document.

The [numbered inputs](<01 - Inputs/numbered_turns.md>) contain every cleaned turn. Turn IDs are zero-based positions in the original parsed array; sentence references start at one within the cleaned turn. The production code uses windows of 40 sentences. All turns in this hearing fit in a single window.

## 3. Extract a topic, stance, and evidence references

In [Senator Hassan's turn 772](<01 - Inputs/numbered_turns.md#turn-772>), the input includes:

```text
[6] You have supported targeted regulations such as the Honest Ads Act, and that is an important step for election integrity.
[7] I am proud to be a cosponsor of that bill.
```

The saved model response to the [full prompt and turn](<01 - Inputs/prompts.md#track-2-senator-hassan-turn-772>) is:

```json
[{"sentences": [6, 7], "topic": "Honest Ads Act", "stance": "support"}]
```

The [production notebook](<../../B - Backup of Original File Structure/scripts/python/03_topic_extraction/03_track2_production.ipynb>) invokes the parser and merges nearby records with identical topic wording and stance. The parser requires valid sentence indices, at most three consecutive references per generated record, and a stance of `support` or `concern`. Wording flags are retained for review. A merged record can cite more than three sentences.

For this hearing, eight candidate records fail the consecutive-reference check across seven turns. One merge reduces duplicate records. The result is **49 accepted records from 27 turns**. [stance_records.md](<02 - Outputs/stance_records.md>) displays all accepted records and their supporting sentences; [stance_records.json](<02 - Outputs/stance_records.json>) preserves the saved fields. The [call log](<03 - Logs and Verification/call_log.jsonl>) also contains rejected candidates and empty responses. Structural acceptance does not establish that a stance interpretation is substantively correct.

## 4. Build the shared codebook across hearings

The codebook is built from **Track 1 phrases across the corpus**, not from this hearing alone and not from pooled topic and stance phrases. The [clustering notebook](<../../B - Backup of Original File Structure/scripts/python/03_topic_extraction/08_taxonomy_consensus.ipynb>) starts with 11,592 mentions and 9,095 distinct phrases. It removes years, bill numbers, and selected trailing terms for clustering; for example, `Honest Ads Act` becomes `Honest Ads`. After excluding 79 phrases whose normalized strings are shorter than three characters, it embeds 8,736 distinct normalized strings with `BAAI/bge-large-en-v1.5` and forms 7,712 groups of similar expressions.

For each of nine candidate cluster counts (15, 20, 25, 40, 60, 80, 100, 120, 150), the code repeats weighted k-means clustering on 80-percent subsamples 30 times, predicts memberships for all groups, and combines the results using the frequency of co-membership. The saved operating choice is 150 topic clusters and 15 broad clusters. Stability and cohesion are diagnostics, not minimum acceptance thresholds.

The [drafting notebook](<../../B - Backup of Original File Structure/scripts/python/03_topic_extraction/09_codebook_draft.ipynb>) prompts Qwen with member phrases and two neighboring clusters to draft labels, definitions, exclusions, and verbatim examples. The [freeze and assignment notebook](<../../B - Backup of Original File Structure/scripts/python/03_topic_extraction/10_codebook_freeze_assign.ipynb>) records explicit decisions: 30 topic clusters are dropped, nine are merged into others, and eight retained labels are revised. The saved [codebook](<02 - Outputs/codebook.json>) has **111 topics under 14 themes**. Topic IDs retain their original cluster numbers and are not consecutive.

## 5. Assign both tracks to the codebook

Track 1 uses cluster membership and the recorded merge/drop decisions:

| Rank | Extracted phrase | Topic ID | Saved category |
|---:|---|---:|---|
| 1 | Facebook data privacy | 68 | consumer data privacy legislation |
| 2 | content moderation | 93 | Online advertising and consumer choice policies |
| 3 | election integrity | 100 | Voting systems standards and integrity |
| 4 | Honest Ads Act | 93 | Online advertising and consumer choice policies |
| 5 | GDPR-style controls | 68 | consumer data privacy legislation |

The primary-topic rule counts assigned phrases and retains the category with the largest count. Here topics 68 and 93 tie at two phrases. The saved result retains 68. The code does not use the original phrase ranks to resolve the tie; it retains the first row after sorting by hearing and descending count.

For Track 2, the code embeds each distinct stance topic and compares it with the normalized, frequency-weighted mean embedding of each category's Track 1 members. The nearest category is accepted when cosine similarity is at least **0.68**; otherwise the record is `other` (ID −1). The comparison uses member embeddings, not the codebook's written definition. Hassan's `Honest Ads Act` receives category 93 at **0.732774**. Overall, **41 records are assigned and eight remain in other**.

The threshold does not prevent all unsuitable assignments. For example, Tillis's [turn 656, record 1](<02 - Outputs/stance_records.md#turn-656-record-1>) concerns `business code of conduct` but receives `hours-of-service regulations` at 0.694650. This saved mismatch illustrates why sentence references and original topic wording must remain available for review.

## 6. Aggregate the assigned records

The [panel notebook](<../../B - Backup of Original File Structure/scripts/python/03_topic_extraction/12_stance_panel.ipynb>) counts assigned support and concern records by topic and Congress, and separately by speaker identifier, surname, topic, Congress, and stance. This hearing contributes to the 115th Congress. For topic 68, it contributes seven support and six concern records. These 13 records are this hearing's contribution, not the complete topic-by-Congress cell. Counts measure extracted statements, and multiple records can come from one speaker.

[verification.json](<03 - Logs and Verification/verification.json>) records all of this hearing's contributions. The hearing has **no match in the saved CAP matching table**. The manuscript's CAP comparisons therefore refer to other hearings in the corpus, not a human-coded label for this example.

The original stance figure captions stated 1999–2025, although the saved panel includes eight records from 1996. [render_stance_figures.py](<04 - Scripts/render_stance_figures.py>) reuses the original plotting cells and saved panel to render the three stance figures in the repository's [results directory](<../../R - Results/figures/T2 - Topic Extraction and Stance Analysis>) with corrected coverage captions: 104th–119th Congress, observations from 1996–2025. To regenerate their SVG and PDF files, run `python` on this script with the same data-root argument. This changes the captions, not the panel values.

## Provenance and verification

Source directory supplied by the researcher: `/project2/mmiric_1435/acroh/llm_method/data`. The export reads `interim/topics/track1/`, `interim/topics/track2/`, and `interim/topics/taxonomy/`. The similarly named `taxonomy_v1/` contains an older, 37-topic result and is not the source of the 111-topic codebook. The saved codebook parquet has SHA-256 `fd81e7814be416617cb52ac4bfaee3eec8086192aa51fda171342b9bb1919abc`.

The extraction logs identify model `Qwen/Qwen3.5-4B` and prompt versions `summary-topics-0.2-dev` and `stance-extraction-0.3-dev`; these are the recorded versions, including their `-dev` suffixes. The original notebooks linked above preserve the full processing logic and recorded outputs used for this account.

To re-export with the existing project environment:

```bash
/project2/njia_1089/acroh/envs/llm_method/bin/python \
  "T2 - Topic Extraction and Stance Analysis/T2.X - Worked Example/04 - Scripts/export_example.py" \
  /project2/mmiric_1435/acroh/llm_method/data
```

Run from the repository root. [export_example.py](<04 - Scripts/export_example.py>) reproduces all 507 turn selections and cleaned sentence lists, verifies **all 508 user-prompt hashes** (one topic call and 507 stance calls), and reproduces the saved parsing and merging results. It also reconstructs the five Track 1 assignments from the saved clusters and review decisions, and checks the stored Track 2 labels and threshold outcomes. It does not rerun embedding models, generation, or the corpus-wide CAP evaluation. These checks establish correspondence with the saved run; they do not certify the substantive accuracy of its interpretations.
