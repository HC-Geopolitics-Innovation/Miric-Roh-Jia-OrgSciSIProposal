# Relevance prompts

Version: `item1-topic-tagging-1.2`. Templates are imported from the original tagging helper. Each executed call stores its full rendered prompt in the call log.

## System

```text
You are an expert reader of corporate 10-K filings with a working knowledge of United States science and technology policy. You report only what the text states.
```

## Pass A: topic screen

```text
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
```

## Pass B: confirmation and direction

```text
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
```
