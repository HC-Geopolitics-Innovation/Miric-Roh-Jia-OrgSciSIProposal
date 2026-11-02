# Data files of the X1 section

The five files the X1.2 notebooks read. The two CSV files are written by [X1.1.2](<../X1.1 - Patent Data - Sample Firm Patents and Privacy Codes/X1.1.2 - Patents - Match the Privacy CPC Codes and Build the Data Files.ipynb>) from the X1.1.1 patent table and the T3.4.1 score table; the three code lists are authored inputs. No file here is licensed data: the patents come from the public KPSS release, the firm identifiers and names are those of the T3 sample, and the Compustat extract and the CRSP-Compustat link that X1.1 uses stay on the cluster.

## sample_firm_privacy_patents.csv

One row per sample-firm patent and listed privacy code it carries, filing years 1999 to 2021; a patent with two listed codes has two rows. 47,225 rows, 37,289 patents, 69 of the 72 codes (three never occur), 1,058 sample firms of which the patenting ones appear. Written by X1.1.2, Step 5.

| Column | Meaning |
|---|---|
| `patent_num` | USPTO patent number, as in the KPSS table |
| `gvkey` | Compustat firm identifier of the assignee, six characters, through the CRSP-Compustat link in force on the filing date |
| `conm` | Company name from the T3 sample |
| `filing_date` | Filing date, `YYYY-MM-DD` |
| `cpc_all` | Every CPC code of the patent, sorted, separated by semicolons, in the KPSS spelling without a space (`G06F21/6254`) |
| `privacy_cpc` | The listed privacy code this row stands for, same spelling |

## firm_topic_relevance.csv

One row per firm of the all-years T3 sample, 1,058 rows: the main topic relevance score of T3.4.1, the cosine between the firm-level summary of the firm's 10-K Item 1 sections and the policy summary of the legislator statements on consumer data privacy legislation. Written by X1.1.2, Step 7, from `table_firm_relevance_scores.csv`.

| Column | Meaning |
|---|---|
| `gvkey` | Compustat firm identifier, six characters |
| `conm` | Company name |
| `n_filings` | Number of 10-K filings of the firm in the sample |
| `cosine_policy_summary_firm_summary` | The T3.4.1 score (`score` in the T3.4.1 table) |

## privacy_cpc_codes.xlsx

The 72-code privacy list, one row per code: `CPC` (with a space between class and group, `G06F 21/6245`) and `Definition` (the CPC scheme text). The codes fall in the classes G06F, H04L, H04W, and G06Q. X1.1.2 matches them exactly, so a listed parent code does not pull in unlisted child codes.

## privacy_cpc_codes_MM_102926.xlsx

The five focal codes of the X1.2 figures, selected by hand on 2026-10-29, same two columns: G06Q 30/0269 and G06Q 30/0255 (advertising targeted by user profile and by user history), G06F 21/6254 (anonymisation of personal data), H04L 67/535 (tracking of user activity in network services), and G06F 11/3438 (monitoring of user actions on computers). The X1.2 notebooks define their topic groups in code; this file documents the selection. All five are among the 72.

## privacy_cpc_codes_clustered.csv

The 72 codes in four cluster groups: `cpc_display`, `cpc_class`, `definition`, `n_privacy_patents` and `n_firms_filing` (counts from the October 2026 pass, informational), and `group` (A. privacy protection; B. use of personal data; C. interception by authorities; D. security). The grouping was proposed by a language model and reviewed by the authors.
