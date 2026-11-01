# Prompts of the topic relevance pipeline

## Policy summary prompts

Used by T3.2.3 with `Qwen/Qwen3.5-4B`: one map call per hearing year, then one reduce call.

### System prompt

You are a policy analyst with a working knowledge of United States congressional hearings. You report only what the statements say.

### Map prompt template

```
Below are {n_statements} statements that members of the House Science and Senate Commerce committees made in hearings held in {year} on the topic "{topic_label}". Each statement is numbered and marked with the legislator's stance toward the topic, support or concern.

--- STATEMENTS ---
{statements_block}
--- END OF STATEMENTS ---

Summarize, in {target_words} words, what the legislation discussed in these statements asks of companies and other organizations and what it tries to regulate: which data practices, which kinds of data, and which actors. Write continuous prose. If the statements say little, write only a sentence or two. Do not list or count the statements, do not name legislators, and do not add knowledge beyond the statements.
```

### Reduce prompt template

```
Below are {n_years} summaries, one per year, of statements that members of the House Science and Senate Commerce committees made in hearings held between {year_min} and {year_max} on the topic "{topic_label}". Each summary is marked with its year.

--- YEARLY SUMMARIES ---
{summaries_block}
--- END OF YEARLY SUMMARIES ---

Combine them into one summary of the legislation, in {target_words} words, for a reader who has not seen the statements. Cover two things:
1. What the legislation asks of companies and other organizations: the obligations it imposes on them and the rights it gives consumers.
2. What it tries to regulate: which data practices, which kinds of data, and which actors.

Write continuous prose in one or two paragraphs. Name the specific requirements, data practices, and actors; do not say that the topic is about laws, bills, or privacy in general. Do not add knowledge beyond the yearly summaries.
```

## Firm summary prompts

Used by T3.3.2 (map, collapse, reduce) and T3.3.4 (per firm) with `Qwen/Qwen3.5-4B`, family `summary_lines_of_business`, prompt version `item1-mapreduce-1.3`.

### System prompt, map

You are an expert reader of corporate 10-K filings. You report only what the text states.

### System prompt, collapse

You are an expert reader of corporate 10-K filings. You condense summaries without adding to them.

### System prompt, reduce

You are an expert reader of corporate 10-K filings. You write from the summaries given and add nothing that is not in them.

### Map (one segment)

```
Below is one consecutive segment of the Item 1 (Business) section of the 10-K that {company} filed for fiscal year {fyear}. The segments are read in order.

--- SEGMENT {segment} OF {n_segments} ---
{text}
--- END OF SEGMENT ---
Summarize in {target_words} words of continuous prose what this segment says the company's business is: the products, services, or segments it sells or operates, and who its customers are. Do not describe internal activities such as labor relations, fuel purchasing, insurance, financing, or regulatory compliance. If the segment describes no business, say so in one sentence.

Write only the summary of the segment above.
```

### Collapse (a run of segment summaries)

```
Below are summaries of consecutive segments of the Item 1 (Business) section of the 10-K that {company} filed for fiscal year {fyear}, in the order they occur. They are already summaries, not the filing text.

--- SEGMENT SUMMARIES ---
{text}
--- END ---
Condense them into one paragraph of {target_words} words that keeps every distinct product, service, or segment named, removing repetition. This is a portion of the section, so do not write an overall conclusion about the company.

Write only the condensed paragraph.
```

### Reduce (all segment summaries of a filing)

```
Below are summaries of every segment of the Item 1 (Business) section of the 10-K that {company} filed for fiscal year {fyear}, in order. They are already summaries, not the filing text.

--- SEGMENT SUMMARIES ---
{text}
--- END ---
Write one paragraph of {target_words} words of continuous prose describing the company's business as a whole: the products, services, or segments it sells or operates, and who its customers are, with no list, no headings, and no repetition. Include only what the summaries state. Ignore any segment summary that says the segment describes no business. Write about the company only; do not refer to the summaries or to what they do not say. Do not add a closing or general statement.

Write only the paragraph.
```

### Per firm (the firm's yearly summaries)

```
Below are summaries of the Item 1 (Business) sections of the 10-Ks that {company} filed for fiscal years {years}, one per year and marked with its year. They are already summaries, not the filing text.

--- YEARLY SUMMARIES ---
{text}
--- END ---
Write one paragraph of {target_words} words of continuous prose describing the company's business across these years, noting changes where the summaries show them, with no list and no repetition. Include only what the summaries state. Write about the company only; do not refer to the summaries or to what they do not say. Do not add a closing or general statement.

Write only the paragraph.
```
