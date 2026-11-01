# Running Example: Topics and Stances in the Facebook Hearing

This folder is the T2 part of the running example: the hearing *Facebook, Social Media Privacy, and the Use and Abuse of Data* of April 10, 2018. Its GovInfo package is `CHRG-115shrg37801`. The summary of this hearing comes from the [T1 part](<../../T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>). Its relevance to firms is scored in the [T3 part](<../../T3 - Topic Relevance and Corporate Disclosure/T3.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>).

The notebook [T2.5.1 - Example - Topics and Stances in the Facebook Hearing Step by Step](<T2.5.1 - Example - Topics and Stances in the Facebook Hearing Step by Step.ipynb>) replays the saved production run. It rebuilds the Track 1 prompt from the summary and the 507 Track 2 prompts from the cleaned legislator turns. It checks all 508 against the hashes the run logged. It parses the logged outputs again, checks the topic assignment and the placement under the codebook, and writes the files below. No model is called.

| Folder | Files |
|---|---|
| [01 - Inputs](<01 - Inputs>) | [numbered_turns.md](<01 - Inputs/numbered_turns.md>), the 507 cleaned legislator turns with numbered sentences. [prompts.md](<01 - Inputs/prompts.md>), the system prompt, the Track 1 prompt, and one Track 2 prompt. |
| [02 - Outputs](<02 - Outputs>) | [topics.json](<02 - Outputs/topics.json>), the five hearing topics and their codebook assignment. [stance_records.md](<02 - Outputs/stance_records.md>), the 49 stance records with their cited sentences; [stance_records.json](<02 - Outputs/stance_records.json>) holds the same records as data. [codebook.json](<02 - Outputs/codebook.json>), the frozen codebook. |
| [03 - Logs and Verification](<03 - Logs and Verification>) | [call_log.jsonl](<03 - Logs and Verification/call_log.jsonl>), the hearing's 508 logged calls, and [verification.json](<03 - Logs and Verification/verification.json>), the counts and checks. |

## What happened to this hearing

| Step | What to read | Result |
|---|---|---|
| Track 1 topics | [topics.json](<02 - Outputs/topics.json>) | Five phrases from the summary: Facebook data privacy, content moderation, election integrity, Honest Ads Act, GDPR-style controls. |
| Legislator turns | [numbered_turns.md](<01 - Inputs/numbered_turns.md>) | 507 of the 903 parsed records are legislator turns; the cleaning rules leave 1,696 sentences. |
| Track 2 records | [stance_records.md](<02 - Outputs/stance_records.md>) | 49 records from 27 turns, each with its cited sentences, topic phrase, and stance. |
| Codebook assignment | [topics.json](<02 - Outputs/topics.json>) | Topics 68 and 93 tie at two phrases each; the primary topic is 68, consumer data privacy legislation. |
| Placement | [stance_records.md](<02 - Outputs/stance_records.md>) | 41 records placed at cosine 0.68 or above, 8 left in the other pool. |
| Panel | [verification.json](<03 - Logs and Verification/verification.json>) | The hearing adds 7 support and 6 concern records on topic 68 to the 115th Congress. |

## How to read it

Start with [Senator Hassan's turn 772](<01 - Inputs/numbered_turns.md#turn-772>) and its [record](<02 - Outputs/stance_records.md#turn-772-record-0>): sentences 6 and 7, support, "Honest Ads Act", placed under topic 93 at cosine 0.733. Then read a placement that went wrong, [Senator Tillis's record on a business code of conduct](<02 - Outputs/stance_records.md#turn-656-record-1>), which the floor let through. The records are the model's outputs without correction; the cited sentences and the original phrase stay with each record so a reader can judge it.

## Where the files come from

The model is `Qwen/Qwen3.5-4B` with prompt versions `summary-topics-0.2-dev` and `stance-extraction-0.3-dev`, the recorded names of the production wording. The saved inputs sit under the scratch root and are listed in the notebook's Step 2. The codebook file has SHA-256 `fd81e7814be416617cb52ac4bfaee3eec8086192aa51fda171342b9bb1919abc`. The hearing has no match in the CAP table, so it is not part of the validation in T2.3. Last replayed on 2026-10-31.
