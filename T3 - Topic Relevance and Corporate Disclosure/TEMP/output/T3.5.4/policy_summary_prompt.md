# Policy summary prompts and settings

Topic 68, consumer data privacy legislation; 374 statements, hearings 1999–2025; map by year (26 calls), then one reduce call.

## Settings

```json
{
  "model_folder": "/scratch2/acroh/projects/llm_method/hf_cache/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
  "generation": {
    "do_sample": true,
    "temperature": 0.1
  },
  "enable_thinking": false,
  "max_new_tokens": 512,
  "map_target_words": "at most 150",
  "reduce_target_words": "200 to 250",
  "max_bge_tokens": 512,
  "input_token_budget": 32000
}
```

## System prompt

You are a policy analyst with a working knowledge of United States congressional hearings. You report only what the statements say.

## Map prompt template, one call per year

```
Below are {n_statements} statements that members of the House Science and Senate Commerce committees made in hearings held in {year} on the topic "{topic_label}". Each statement is numbered and marked with the legislator's stance toward the topic, support or concern.

--- STATEMENTS ---
{statements_block}
--- END OF STATEMENTS ---

Summarize, in {target_words} words, what the legislation discussed in these statements asks of companies and other organizations and what it tries to regulate: which data practices, which kinds of data, and which actors. Write continuous prose. If the statements say little, write only a sentence or two. Do not list or count the statements, do not name legislators, and do not add knowledge beyond the statements.
```

## Reduce prompt template, one call

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
