# Running Example: From the Facebook Hearing Transcript to Its Summary

One hearing is followed through the whole repository: *Facebook, Social Media Privacy, and the Use and Abuse of Data*, held on April 10, 2018. It was a joint hearing of the Senate Committees on the Judiciary and on Commerce, Science, and Transportation, with Mark Zuckerberg as the witness. Its GovInfo package is `CHRG-115shrg37801`. This folder is the T1 part: the transcript becomes one summary. The same hearing continues in [T2](<../../T2 - Topic Extraction and Stance Analysis/T2.5 - Running Example [Facebook-Cambridge Analytica Scandal Hearing]/README.md>), where its topics and stances are extracted, and in [T3](<../../T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/README.md>), where its relevance to firms is scored.

The notebook [T1.4.1 - Example - The Facebook Hearing Step by Step](<T1.4.1 - Example - The Facebook Hearing Step by Step.ipynb>) replays the saved production run. It reads the transcript as speaking turns and rebuilds the model inputs with the production tokenizer. Then it checks each of the 59 logged calls against the hash the run stored. No model is called. It then writes the files below, so every step can be read on GitHub.

| Folder | Files |
|---|---|
| [01 - Inputs](<01 - Inputs>) | [source.txt](<01 - Inputs/source.txt>), the transcript text. [parsed_turns.json](<01 - Inputs/parsed_turns.json>), the 903 speaking turns. [prompts.md](<01 - Inputs/prompts.md>), the map, collapse, and reduce prompts. [chunks.md](<01 - Inputs/Chunks/chunks.md>), the 55 model inputs in six pages. |
| [02 - Outputs](<02 - Outputs>) | [outputs.md](<02 - Outputs/outputs.md>): the 55 segment summaries, the 3 condensed accounts, the final summary, and the C-SPAN abstract. |
| [03 - Logs and Verification](<03 - Logs and Verification>) | [call_log.jsonl](<03 - Logs and Verification/call_log.jsonl>), a byte-for-byte copy of the production log. |

## What happened to this hearing

| Step | What to read | Result |
|---|---|---|
| Source | [Text extracted from the saved HTML](<01 - Inputs/source.txt>) | Front matter, testimony, exchanges, and inserted material in document order. |
| Parsing | [Turn records](<01 - Inputs/parsed_turns.json>) | 8,192 paragraphs; 40 dot-leader paragraphs removed; 903 records, including introductory and appended material. |
| Packing | [55 model-input chunks](<01 - Inputs/Chunks/chunks.md>) | Consecutive turns packed within a 6,144-token budget; oversized records divided. |
| Map | [55 segment summaries](<02 - Outputs/outputs.md#map-01>) | One model call per chunk. |
| Collapse | [First](<02 - Outputs/outputs.md#collapse-01>), [second](<02 - Outputs/outputs.md#collapse-02>), and [third](<02 - Outputs/outputs.md#collapse-03>) condensed accounts | Three batches: segment summaries 1 to 23, 24 to 45, and 46 to 55. |
| Reduce | [Final summary](<02 - Outputs/outputs.md#final-summary>) | One 264-word, 359-token summary. |
| Reference | [Matched C-SPAN abstract](<02 - Outputs/outputs.md#c-span-reference>) | The independently written program abstract used in T1.3. |

## How to read it

Start with the [final summary](<02 - Outputs/outputs.md#final-summary>) and set it beside the [C-SPAN abstract](<02 - Outputs/outputs.md#c-span-reference>). Then open one [chunk](<01 - Inputs/Chunks/chunks_01-10.md#chunk-02>) and its [segment summary](<02 - Outputs/outputs.md#map-02>). The outputs are the strings stored in the production log, with no correction or new generation. Similarity to the abstract shows that the summary is about this hearing. It does not check each attribution, number, or omission.

## Where the files come from

The model is `Qwen/Qwen3.5-4B` and the prompt version is `hearing-mapreduce-1.0`. The chunks are rebuilt with the cached tokenizer snapshot `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. All 59 user-prompt hashes in the log must match before the notebook writes a file; the hashes cover the user prompt, not the system message. The saved inputs sit under the scratch root and are listed in the notebook's Step 2. Last replayed on 2026-10-31; the files equal the August export.
