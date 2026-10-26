# Firm summary prompts and settings (item1-mapreduce-1.3)

18,779 filings cut into 57,754 segments of at most 4,000 model tokens; aggregation budget 6,144 tokens; per-filing summaries of 150 to 200 words, per-firm summaries of 200 to 250 words.

## Settings

```json
{
  "prompt_version": "item1-mapreduce-1.3",
  "model_folder": "/scratch2/acroh/projects/llm_method/hf_cache/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
  "families": [
    "summary_without_focus",
    "summary_lines_of_business",
    "summary_privacy"
  ],
  "generation": {
    "do_sample": true,
    "temperature": 0.1
  },
  "enable_thinking": false,
  "segment_tokens": 4000,
  "aggregation_budget": 6144,
  "max_new_tokens": {
    "map": 320,
    "collapse": 384,
    "reduce": 512
  },
  "target_words": {
    "map": "about 150",
    "collapse": "about 200",
    "reduce": "150 to 200",
    "firm": "200 to 250"
  },
  "max_bge_tokens": 512,
  "inputs_folder": "/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3-TEMP/T3.7 - Firm Summaries/Interim/filing_inputs"
}
```

## System prompt, map## 

You are an expert reader of corporate 10-K filings. You report only what the text states.

## System prompt, collapse## 

You are an expert reader of corporate 10-K filings. You condense summaries without adding to them.

## System prompt, reduce## 

You are an expert reader of corporate 10-K filings. You write from the summaries given and add nothing that is not in them.

## Map (one segment), opening## 

```
Below is one consecutive segment of the Item 1 (Business) section of the 10-K that {company} filed for fiscal year {fyear}. The segments are read in order.

--- SEGMENT {segment} OF {n_segments} ---
{text}
--- END OF SEGMENT ---
```

## Map (one segment), task `summary_without_focus`## 

```
Summarize this segment in {target_words} words: what the company does, its products and services, its customers and markets, how it operates, and the regulations it says it is subject to, as this segment states them. Keep the company's own terms. If the segment contains none of these, for example only headings or boilerplate, say so in one sentence.

Write only the summary of the segment above.
```

## Map (one segment), task `summary_lines_of_business`## 

```
Summarize in {target_words} words of continuous prose what this segment says the company's business is: the products, services, or segments it sells or operates, and who its customers are. Do not describe internal activities such as labor relations, fuel purchasing, insurance, financing, or regulatory compliance. If the segment describes no business, say so in one sentence.

Write only the summary of the segment above.
```

## Map (one segment), task `summary_privacy`## 

```
Report in {target_words} words what this segment says about consumer personal data: which activities collect, store, use, share, or sell personal data; whose data it is; and which privacy or data protection laws and regulators it names. If the segment says nothing about personal data or privacy, say so in one sentence.

Write only the report for the segment above.
```

## Collapse (a run of segment summaries), opening## 

```
Below are summaries of consecutive segments of the Item 1 (Business) section of the 10-K that {company} filed for fiscal year {fyear}, in the order they occur. They are already summaries, not the filing text.

--- SEGMENT SUMMARIES ---
{text}
--- END ---
```

## Collapse (a run of segment summaries), task `summary_without_focus`## 

```
Condense them into one account of {target_words} words that keeps what the company does, its products and services, customers and markets, operations, and the regulations named. This is a portion of the section, so do not write an overall conclusion about the company.

Write only the condensed account.
```

## Collapse (a run of segment summaries), task `summary_lines_of_business`## 

```
Condense them into one paragraph of {target_words} words that keeps every distinct product, service, or segment named, removing repetition. This is a portion of the section, so do not write an overall conclusion about the company.

Write only the condensed paragraph.
```

## Collapse (a run of segment summaries), task `summary_privacy`## 

```
Condense them into one account of {target_words} words that keeps every activity involving personal data, whose data it is, and every privacy law and regulator named, removing repetition. This is a portion of the section, so do not write an overall conclusion about the company.

Write only the condensed account.
```

## Reduce (all segment summaries of a filing), opening## 

```
Below are summaries of every segment of the Item 1 (Business) section of the 10-K that {company} filed for fiscal year {fyear}, in order. They are already summaries, not the filing text.

--- SEGMENT SUMMARIES ---
{text}
--- END ---
```

## Reduce (all segment summaries of a filing), task `summary_without_focus`## 

```
Write a single summary of the whole section in {target_words} words of continuous prose: what the company does, its products and services, its customers and markets, how it operates, and the regulations it says it is subject to. Keep the company's own terms. Where the segment summaries do not establish one of these, leave it out rather than inferring it.

Write only the summary.
```

## Reduce (all segment summaries of a filing), task `summary_lines_of_business`## 

```
Write one paragraph of {target_words} words of continuous prose describing the company's business as a whole: the products, services, or segments it sells or operates, and who its customers are, with no list, no headings, and no repetition. Include only what the summaries state. Ignore any segment summary that says the segment describes no business. Write about the company only; do not refer to the summaries or to what they do not say. Do not add a closing or general statement.

Write only the paragraph.
```

## Reduce (all segment summaries of a filing), task `summary_privacy`## 

```
Write a single account of the whole section in {target_words} words of continuous prose: how the company's business involves consumer personal data, which activities collect, store, use, share, or sell personal data, whose data it is, and which privacy or data protection laws and regulators are named. If the segment summaries say the section does not mention personal data or privacy, write exactly one sentence saying so and nothing else. Where the segment summaries do not establish something, leave it out rather than inferring it.

Write only the account.
```

## Per firm (the firm's yearly summaries), opening## 

```
Below are summaries of the Item 1 (Business) sections of the 10-Ks that {company} filed for fiscal years {years}, one per year and marked with its year. They are already summaries, not the filing text.

--- YEARLY SUMMARIES ---
{text}
--- END ---
```

## Per firm (the firm's yearly summaries), task `summary_without_focus`## 

```
Write a single description of the company's business over these years in {target_words} words of continuous prose: what the company does, its products and services, its customers and markets, how it operates, and the regulations it says it is subject to, noting changes across the years where the summaries show them. Add nothing that is not in the summaries.

Write only the description.
```

## Per firm (the firm's yearly summaries), task `summary_lines_of_business`## 

```
Write one paragraph of {target_words} words of continuous prose describing the company's business across these years, noting changes where the summaries show them, with no list and no repetition. Include only what the summaries state. Write about the company only; do not refer to the summaries or to what they do not say. Do not add a closing or general statement.

Write only the paragraph.
```

## Per firm (the firm's yearly summaries), task `summary_privacy`## 

```
Write a single account in {target_words} words of continuous prose of how the company's business involves consumer personal data across these years: which activities collect, store, use, share, or sell personal data, whose data it is, and which privacy or data protection laws and regulators are named. If the summaries say the filings do not mention personal data or privacy, write exactly one sentence saying so and nothing else. Add nothing that is not in the summaries.

Write only the account.
```


