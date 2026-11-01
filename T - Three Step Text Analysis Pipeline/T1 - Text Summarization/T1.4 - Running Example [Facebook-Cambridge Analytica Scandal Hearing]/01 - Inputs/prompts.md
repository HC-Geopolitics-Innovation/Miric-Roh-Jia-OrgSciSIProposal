# Prompts of the production run: hearing-mapreduce-1.0

The three prompts below carry the version `hearing-mapreduce-1.0` stamped on every logged call. Each call sends the system message and then the user message, with `{text}` or the list of summaries filled in. Generation settings: {'do_sample': True, 'temperature': 0.1}; the reduce call is capped at 512 tokens and asks for 200 to 250 words.

## Map prompt

System message:

```text
You are an expert in text summarization with a working knowledge of United States congressional hearings. You report only what the transcript states.
```

User message:

```text
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
```

## Collapse prompt

System message:

```text
You are an expert in text summarization with a working knowledge of United States congressional hearings. You condense summaries without adding to them.
```

User message:

```text
Below are summaries of consecutive segments of one congressional hearing, in the order they occurred. They are already summaries, not transcript.

Condense them into one account of about 200 words that keeps the named speakers, their positions, and the numbers and legislation. This is a middle portion of the hearing, so do not write an overall conclusion about the hearing.

--- SEGMENT SUMMARIES ---
{text}
--- END ---

Write only the condensed account.
```

## Reduce prompt

System message:

```text
You are an expert in text summarization with a working knowledge of United States congressional hearings. You write from the summaries given and add nothing that is not in them.
```

User message:

```text
Below are summaries of every segment of one congressional hearing, in order. They are already summaries, not transcript.

Write a single summary of the hearing as a whole, in about {target_words} words. Cover:
- what the hearing was about;
- the main subjects, the most heavily discussed first;
- the position each named speaker took;
- any point where speakers took opposing positions, naming both sides;
- the key numbers and the legislation referred to, exactly as given.

Where the segment summaries do not establish one of these, leave it out rather than inferring it.

--- SEGMENT SUMMARIES ---
{text}
--- END ---

Write only the summary of the hearing, in about {target_words} words, as continuous prose.
```

