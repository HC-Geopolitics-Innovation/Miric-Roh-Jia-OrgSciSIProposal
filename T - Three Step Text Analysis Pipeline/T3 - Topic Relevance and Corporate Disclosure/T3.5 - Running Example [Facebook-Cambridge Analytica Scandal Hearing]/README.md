# Running Example: From the Facebook Hearing's Topic to the Firms It Concerns

This folder is the T3 part of the running example: the hearing *Facebook, Social Media Privacy, and the Use and Abuse of Data* of April 10, 2018, GovInfo package `CHRG-115shrg37801`. The [T1 part](<../../T1 - Text Summarization/T1.4 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>) summarized the hearing and the [T2 part](<../../T2 - Topic Extraction and Stance Analysis/T2.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>) placed 13 of its stance records under its primary topic, consumer data privacy legislation. This part follows that topic to the firms: which S&P 500 businesses the legislation concerns, and how much.

The notebook [T3.5.1 - Example - From the Facebook Hearing's Topic to the Firms It Concerns](<T3.5.1 - Example - From the Facebook Hearing's Topic to the Firms It Concerns.ipynb>) reads the stored runs of T3.2 to T3.4 and calls no model. It shows the hearing's 13 statements among the 374 the topic holds, the policy summary the model wrote from all 374, the firm summaries of 22 well-known firms, and the two panels of Figure 3 of the proposal as one figure.

| Folder | Files |
|---|---|
| [01 - Inputs](<01 - Inputs>) | [hearing_statements.md](<01 - Inputs/hearing_statements.md>), the hearing's 13 statements on the topic. [prompts.md](<01 - Inputs/prompts.md>), the policy-summary prompts of T3.2.2 and the firm-summary prompts of T3.3.1. |
| [02 - Outputs](<02 - Outputs>) | [policy_summary.md](<02 - Outputs/policy_summary.md>), the 221-word summary of what the legislation asks and regulates. [selected_firm_summaries.md](<02 - Outputs/selected_firm_summaries.md>), the 22 firms with their scores, ranks, and firm-level summaries. [sector_means.csv](<02 - Outputs/sector_means.csv>) and [selected_firms.csv](<02 - Outputs/selected_firms.csv>), the data behind the two panels. |
| [03 - Logs and Verification](<03 - Logs and Verification>) | [policy_summary_calls.jsonl](<03 - Logs and Verification/policy_summary_calls.jsonl>), the 27 model calls that wrote the policy summary, and [verification.json](<03 - Logs and Verification/verification.json>), the counts and checks. |

## What happened to the topic

| Step | What to read | Result |
|---|---|---|
| Statements | [hearing_statements.md](<01 - Inputs/hearing_statements.md>) | 13 of the topic's 374 statements come from this hearing (7 support, 6 concern), 3.5 percent of the topic. |
| Policy summary | [policy_summary.md](<02 - Outputs/policy_summary.md>) | One call per hearing year, then one call over the 26 yearly summaries: 221 words on the obligations, rights, data practices, and actors the legislation names. |
| Firm summaries | [selected_firm_summaries.md](<02 - Outputs/selected_firm_summaries.md>) | One paragraph per firm, written from the firm's yearly summaries of its 10-K Item 1 sections. |
| Score | [selected_firms.csv](<02 - Outputs/selected_firms.csv>) | The cosine of the two summaries; Visa, Nielsen, Alphabet, and Motorola Mobility are highest among the selected firms, Pep Boys lowest. Meta Platforms scores 0.546, rank 186 of 1,058. |
| Figure | [fig_running_example_topic_relevance.png](<../../../R - Results/figures/T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/T3.5.1 - Example - From the Facebook Hearing's Topic to the Firms It Concerns/fig_running_example_topic_relevance.png>) | Left, the sector means relative to the sample mean; right, the selected firms. The information sector sits highest and mining lowest. |

## How to read it

Start with the [2018 yearly summary and the policy summary](<T3.5.1 - Example - From the Facebook Hearing's Topic to the Firms It Concerns.ipynb>) in Step 6 of the notebook, which show what the model kept from the hearing's year. Then read [Alphabet's and Pepsi Bottling Group's firm summaries](<02 - Outputs/selected_firm_summaries.md>) side by side: the score is high where the business description speaks of the data practices and actors the policy summary names, and low where it does not. The firm summaries are the model's outputs without correction.

## Where the files come from

The model is `Qwen/Qwen3.5-4B` for the summaries and `BAAI/bge-large-en-v1.5` for the embeddings. The policy summary run is dated 2026-10-25 and the firm summary runs 2026-10-25 and 2026-10-26; the scores and figures were rebuilt on 2026-10-31. Last executed on 2026-10-31.
