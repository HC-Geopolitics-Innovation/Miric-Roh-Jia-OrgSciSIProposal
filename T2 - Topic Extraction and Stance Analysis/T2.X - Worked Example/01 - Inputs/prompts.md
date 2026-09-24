# Verified example prompts

The user prompts below reproduce the hashes in [the saved call log](<../03 - Logs and Verification/call_log.jsonl>). The shared system prompt is copied from the production helper.

## System prompt

```text
You are an expert reader of United States congressional hearing transcripts. You report only what the text states.
```

## Track 1: hearing summary

Version `summary-topics-0.2-dev`.

```text
Below is a summary of one United States congressional hearing.

Task: list the main topics the hearing covered, ordered from most to least central.

A topic is a short and specific neutral noun phrase: the policy, program, regulation, technology, practice, or budget item itself; never directional wording; name the specific object, not the agency or field around it. An agency, company, or country is never a topic by itself; name the policy object involving it. A bill counts as a topic by its subject or name, never as a bare bill number such as "H.R. 1". A bare number or amount is never a topic. Entities mentioned only as examples, comparisons, or asides are not topics.

List at most 5 topics. Include a topic only if the hearing gave it substantial attention — most summaries support 2 to 4 topics, and padding to 5 is worse than stopping early. Every major subject of the hearing should appear.

--- SUMMARY ---
On April 10, 2018, a joint Senate hearing addressed Facebook's data privacy, centering on the Cambridge Analytica scandal where approximately 87 million users' data was scraped. Mark Zuckerberg testified, apologizing for the failure to notify victims and acknowledging that while changes were made in 2014, he failed to prevent harm from fake news and foreign interference. He confirmed the Internet Research Agency spent $100,000 on ads seen by 11 million people and that around 200 apps were suspended pending audit. Zuckerberg stated Facebook serves over 2 billion users with $40 billion in 2017 revenue, emphasizing community protection over profits. He denied selling data to advertisers but acknowledged allowing targeted placement.

The hearing also covered content moderation and political neutrality. Zuckerberg detailed data collection practices and explained that content visibility adheres to Community Standards focused on Safety, Voice, and Equity, explicitly excluding political party affiliation from hate speech definitions. Regarding bias, Facebook reported that an investigation into the "Trending Topics" feature found no systematic bias, with approval rates for conservative and liberal topics being "virtually identical." On election integrity, Zuckerberg noted tracking 40+ elections, removing 70 Facebook and 65 Instagram accounts controlled by the Russia-based Internet Research Agency, and finding no evidence of Russian involvement in the "Release the Nunes Memo" campaign as of February 7, 2018.

Senators questioned the need for federal standards, including the Honest Ads Act and GDPR-style controls, while Zuckerberg supported a 72-hour breach notification rule but refused to disclose his hotel name or messenger contacts. The hearing concluded with a recess, leaving the committee to consider stronger legislation versus self-regulation.
--- END OF SUMMARY ---

Return only a JSON list of topic strings, most central first. Your very first output character must be [.
```

## Track 2: Senator Hassan, turn 772

Version `stance-extraction-0.3-dev`.

```text
Below is one speaking turn by a member of Congress, split into numbered sentences.

Task: find every sentence in which the member takes a directional position on a policy object, and return one record per position.

A record has three fields:
- "sentences": the sentence number(s) expressing the position (1-3 consecutive numbers);
- "topic": the policy object, as a short and specific neutral noun phrase (the policy, program, regulation, technology, practice, or budget item itself; never directional wording; name the specific object, not the agency or field around it);
- "stance": "support" if the member endorses, advocates, or urges adoption, funding, or expansion of the topic; "concern" if the member expresses worry, criticism, or objection toward the topic, or urges its restriction, delay, or scrutiny.

The stance is toward the topic exactly as you phrase it. Before returning a record, check that it reads sensibly as "the member supports [topic]" or "the member is concerned about [topic]". If the topic is a problem or harm, the stance toward it is "concern", never "support".

The topic must be the object the member takes a position ON. Entities mentioned only as examples, comparisons, or asides are not topics, and a bare number or amount is never a topic. If several consecutive sentences express the same position on the same topic, return one record covering them, not one record per sentence.

Example: "Youth vaping is an epidemic we cannot ignore." -> {"sentences": [n], "topic": "youth e-cigarette use", "stance": "concern"}
Example: "This bill funds the research our labs badly need." -> {"sentences": [n], "topic": "research funding bill", "stance": "support"}

Do not return records for: procedure (recognitions, time, the record), courtesies, introductions, logistics, questions asked without an expressed position, or factual statements without evaluation. If no sentence takes a directional position, return an empty list. When in doubt, do not extract.

--- TURN (Speaker: Senator Hassan) ---
[1] OK.
[2] And I understand the point that you are trying to make here, but here is what I am concerned about.
[3] We have heard this point from you over the last decade-plus since you founded Facebook, and I understand that you founded it pretty much as a solo entrepreneur with your roommate, but now, you know, you are sitting here, the head of a bazillion-dollar company.
[4] And we have heard you apologize numerous times and promise to change, but here we are again, right?
[5] So I really firmly believe in free enterprise, but when private companies are unwilling or unable to do what is necessary, public officials have historically in every industry stepped up to protect our constituents and consumers.
[6] You have supported targeted regulations such as the Honest Ads Act, and that is an important step for election integrity.
[7] I am proud to be a cosponsor of that bill.
[8] But we need to address other broader issues as well.
[9] And today, you have said you would be open to some regulation, but this has been a pretty general conversation.
[10] So will you commit to working with Congress to develop ways of protecting constituent privacy and well-being, even if it means that that results in some laws that will require you to adjust your business model?
--- END OF TURN ---

Return only a JSON list of records. Your very first output character must be [.
```
