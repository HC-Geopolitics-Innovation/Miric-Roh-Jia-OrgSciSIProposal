"""Map-reduce summarization of congressional hearings with a local model.

**The three prompts are different jobs and are written separately.**

| Stage | Input | Task |
|---|---|---|
| `map` | raw transcript turns, one segment | read speech, report what was said |
| `collapse` | segment summaries, a group of them | shorten a run of summaries, keep detail |
| `reduce` | segment summaries, all of them | write the hearing's single summary |

Using one prompt for all three is the obvious shortcut and it produces the
characteristic failure: the reduce step summarizes the *summaries* as if they
were speech, re-attributing positions to whoever a segment happened to mention
last. The map step therefore asks what a speaker said; the reduce step asks what
the hearing was about, and is told explicitly that its input is already summary.

Recursion: if the segment summaries do not fit in one call, they are grouped and
run through `collapse`, and that repeats until they do. `collapse` differs from
`reduce` in that it must NOT produce a whole-hearing summary — it is a partial
view and writing a conclusion from it would invent one.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch

#: Frozen release marker for the three prompts below. Every logged call carries
#: it, so any summary can be traced to the exact wording that produced it. Bump
#: it whenever a prompt string changes — a run whose outputs mix two wordings
#: under one label cannot be reasoned about afterwards.
PROMPT_VERSION = "hearing-mapreduce-1.0"

#: Hard ceiling on the final summary, in tokens.
#:
#: This is a downstream requirement, not a style preference. The summaries are
#: the documents BERTopic embeds, and a sentence-transformer truncates its input
#: at the encoder's window — anything past it is silently dropped, so a summary
#: that overruns is not a longer document, it is a truncated one whose tail never
#: reaches the topic model. Generation is capped here so the limit holds by
#: construction, and the reduce prompt asks for a length that lands inside it
#: rather than relying on the cap, because a cap reached mid-sentence truncates.
REDUCE_MAX_TOKENS = 512

#: Words requested of the reduce step, as a range rather than a ceiling.
#:
#: Measured on this text the model produces about 1.55 tokens per word, so a
#: 300-word request lands at 465-470 tokens — inside the 512 cap, but close
#: enough that a summary carrying a few extra names or dollar figures runs into
#: it, and a completion stopped at the cap ends mid-clause. Asking for 200-250
#: words puts the median near 390 and leaves roughly 120 tokens of headroom, so
#: the model reaches its own ending instead of being cut off at ours.
#:
#: A range works better here than "at most N": a ceiling invites the model to
#: write up to it, while a range gives it a length to land inside.
REDUCE_TARGET_WORDS = "200 to 250"

#: Sampling, carried over unchanged from the pipeline this replaces
#: (`scaleup_original/2a_summarization.py`, which set `do_sample=True` and
#: `temperature=0.1` and passed no `top_p` or `top_k`).
#:
#: Kept because it is model-agnostic. A temperature this low is close to greedy
#: decoding on any causal LM, which is what a measurement task wants — the
#: annotation literature recommends the lowest available temperature for exactly
#: this reason. Model cards recommend their own values (Qwen suggests a much
#: warmer setting for open-ended chat), but those are tuned for generation
#: quality in conversation, not for making a corpus reproducible.
#:
#: `top_p` is deliberately absent. An earlier draft of this file added
#: `top_p=0.9`, which appears in no source: not in the inherited code, not in a
#: model card, not in the literature. At temperature 0.1 it changes almost
#: nothing, and an unsourced parameter is one more thing to defend, so it is
#: gone. Everything sent is in this dict and this dict is logged with every run.
GENERATION = {
    "do_sample": True,
    "temperature": 0.1,
}

MAP_SYSTEM = (
    "You are an expert in text summarization with a working knowledge of United "
    "States congressional hearings. You report only what the transcript states."
)

MAP_USER = """Below is one consecutive segment of a congressional hearing transcript. Each speaking turn is labelled with the speaker.

Summarize this segment in about 150 words. Cover:
- the subjects raised, and what was said about them;
- the position each named speaker takes, attributed to that speaker;
- any numbers, dollar amounts, dates, and bill or act names, copied exactly as they appear.

If the segment is procedural or ceremonial and contains none of these, say so in one sentence.

--- SEGMENT ---
{text}
--- END OF SEGMENT ---

Write only the summary of the segment above."""

COLLAPSE_SYSTEM = (
    "You are an expert in text summarization with a working knowledge of United "
    "States congressional hearings. You condense summaries without adding to them."
)

COLLAPSE_USER = """Below are summaries of consecutive segments of one congressional hearing, in the order they occurred. They are already summaries, not transcript.

Condense them into one account of about 200 words that keeps the named speakers, their positions, and the numbers and legislation. This is a middle portion of the hearing, so do not write an overall conclusion about the hearing.

--- SEGMENT SUMMARIES ---
{text}
--- END ---

Write only the condensed account."""

REDUCE_SYSTEM = (
    "You are an expert in text summarization with a working knowledge of United "
    "States congressional hearings. You write from the summaries given and add "
    "nothing that is not in them."
)

REDUCE_USER = """Below are summaries of every segment of one congressional hearing, in order. They are already summaries, not transcript.

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

Write only the summary of the hearing, in about {target_words} words, as continuous prose."""


def _render(tokenizer, system: str, user: str) -> str:
    """Apply the model's chat template, with reasoning traces off where offered.

    Qwen3 and Qwen3.5 default their template to a thinking mode that emits a
    `<think>` block before the answer. That block is drawn from the same output
    budget as the summary, so leaving it on either truncates the summary or has
    to be paid for twice. Templates that do not take the argument raise, and are
    rendered plainly.
    """
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": user}]
    try:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
        )


def _generate(model, tokenizer, system: str, user: str,
              max_new_tokens: int) -> tuple[str, bool]:
    """One prompt, one completion, fresh context.

    Returns the text and whether generation stopped because it ran out of budget
    rather than because the model finished. The caller needs to know: a
    completion cut off at the cap ends mid-sentence.
    """
    prompt = _render(tokenizer, system, user)
    ids = tokenizer(prompt, return_tensors="pt").to(model.device)
    n_in = ids["input_ids"].shape[-1]
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=max_new_tokens,
                             pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                             **GENERATION)
    generated = out[0][n_in:]
    hit_cap = len(generated) >= max_new_tokens
    return tokenizer.decode(generated, skip_special_tokens=True).strip(), hit_cap


#: Sentence terminators used when a completion has to be trimmed back to a whole
#: sentence. The closing-quote and bracket variants matter here because hearing
#: summaries quote titles and statute names.
_SENTENCE_END = tuple('.!?') + tuple(f'{p}{q}' for p in '.!?' for q in '"\')]')


def trim_to_sentence(text: str) -> str:
    """Cut back to the last complete sentence.

    Used only when generation hit its token cap. A summary that stops mid-clause
    is worse than a shorter one that ends: downstream this text is embedded and
    read, and a dangling fragment misrepresents the hearing rather than merely
    shortening it.
    """
    text = text.rstrip()
    if not text or text.endswith(_SENTENCE_END):
        return text
    cut = max(text.rfind(mark) for mark in '.!?')
    if cut <= 0:
        return text
    # Keep any closing quote or bracket that belongs to the sentence.
    end = cut + 1
    while end < len(text) and text[end] in '"\')]':
        end += 1
    return text[:end].rstrip()


def summarize_chunk(chunk_text: str, model, tokenizer, max_new_tokens: int = 320) -> str:
    """Map: one transcript segment to a summary of what was said in it."""
    text, hit_cap = _generate(model, tokenizer, MAP_SYSTEM,
                              MAP_USER.format(text=chunk_text), max_new_tokens)
    return trim_to_sentence(text) if hit_cap else text


def collapse_summaries(joined: str, model, tokenizer, max_new_tokens: int = 384) -> str:
    """Intermediate: a run of segment summaries to one shorter account."""
    text, hit_cap = _generate(model, tokenizer, COLLAPSE_SYSTEM,
                              COLLAPSE_USER.format(text=joined), max_new_tokens)
    return trim_to_sentence(text) if hit_cap else text


def reduce_summaries(joined: str, model, tokenizer,
                     max_new_tokens: int = REDUCE_MAX_TOKENS) -> str:
    """Reduce: all segment summaries to the hearing's single summary.

    Capped at `REDUCE_MAX_TOKENS` so the output is embeddable by the topic model
    downstream without truncation.
    """
    text, hit_cap = _generate(model, tokenizer, REDUCE_SYSTEM,
                              REDUCE_USER.format(text=joined,
                                                 target_words=REDUCE_TARGET_WORDS),
                              max_new_tokens)
    # The cap exists so the summary is embeddable downstream. Reaching it means
    # the model was still writing, so the text is cut back to its last whole
    # sentence rather than shipped ending in half a clause.
    return trim_to_sentence(text) if hit_cap else text


class CallLog:
    """A JSONL record of every model call made for one document.

    One line per call, written and flushed as it happens. The line carries the
    stage, the level and position within that level, a SHA-256 of the exact input
    string, the token counts, the elapsed time, and **the complete output text**.

    Two reasons this exists rather than a summary count.

    *Provenance.* The final summary is one of many model outputs and the only one
    normally kept. Logging every intermediate makes the chain from transcript to
    summary inspectable end to end, which is what lets someone check that no
    output was edited by hand between stages. The input hash pins what was fed in
    without duplicating the corpus; the output is stored in full because the
    output is the thing that would have been altered.

    *Diagnosis.* When a summary comes out wrong the question is always which call
    went wrong. With per-call records the answer is a lookup — the level, the
    position, the input hash — instead of a re-run that may not reproduce.
    """

    def __init__(self, path: Path | str | None, document_id: str, model_name: str,
                 prompt_version: str | None = None):
        self.path = Path(path) if path else None
        self.document_id = document_id
        self.model_name = model_name
        # Stage 3 reuses this logger for its own prompts; the version stamped on
        # each line must name the prompt actually sent, not this module's.
        self.prompt_version = prompt_version or PROMPT_VERSION
        self.records: list[dict[str, Any]] = []
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, stage: str, level: int, index: int, n_inputs: int,
              prompt_text: str, output: str, tokenizer, seconds: float) -> None:
        record = {
            "document_id": self.document_id,
            "model": self.model_name,
            "prompt_version": self.prompt_version,
            "stage": stage,
            "level": level,
            "index": index,
            "n_inputs": n_inputs,
            "input_sha256": hashlib.sha256(prompt_text.encode("utf-8")).hexdigest(),
            "input_chars": len(prompt_text),
            "input_tokens": len(tokenizer.encode(prompt_text, add_special_tokens=False)),
            "output_tokens": len(tokenizer.encode(output, add_special_tokens=False)),
            "output_chars": len(output),
            "seconds": round(seconds, 2),
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "output": output,
        }
        self.records.append(record)
        if self.path:
            with self.path.open("a") as fh:
                fh.write(json.dumps(record) + "\n")
                fh.flush()


def map_reduce(chunks: list[str], model, tokenizer, budget_tokens: int,
               max_levels: int = 8, log: "CallLog | None" = None,
               document_id: str = "", model_name: str = "") -> dict[str, Any]:
    """Map every chunk, collapse until the summaries fit, then reduce once.

    **The number of collapse rounds is not fixed.** A short hearing produces
    segment summaries that already fit and goes straight to reduce; a long one
    may need several rounds. `max_levels` is a runaway guard, not a target, and
    the level actually reached is reported per document.

    Every call is written to `log` as it completes, so the intermediate summaries
    survive the run rather than existing only inside it.
    """
    if log is None:
        log = CallLog(None, document_id, model_name)

    level_summaries: list[str] = []
    for i, chunk in enumerate(chunks):
        t0 = time.time()
        out = summarize_chunk(chunk, model, tokenizer)
        log.write("map", 0, i, 1,
                  MAP_USER.format(text=chunk), out, tokenizer, time.time() - t0)
        level_summaries.append(out)
    levels = [list(level_summaries)]

    level = 0
    for _ in range(max_levels):
        joined = "\n\n".join(level_summaries)
        if len(tokenizer.encode(joined, add_special_tokens=False)) <= budget_tokens:
            break
        level += 1
        # Regroup into batches that fit, then condense each.
        groups, current, current_tokens = [], [], 0
        for summary in level_summaries:
            n = len(tokenizer.encode(summary, add_special_tokens=False))
            if current and current_tokens + n > budget_tokens:
                groups.append(current)
                current, current_tokens = [], 0
            current.append(summary)
            current_tokens += n
        if current:
            groups.append(current)

        collapsed = []
        for i, group in enumerate(groups):
            text = "\n\n".join(group)
            t0 = time.time()
            out = collapse_summaries(text, model, tokenizer)
            log.write("collapse", level, i, len(group),
                      COLLAPSE_USER.format(text=text), out, tokenizer,
                      time.time() - t0)
            collapsed.append(out)
        level_summaries = collapsed
        levels.append(list(level_summaries))

    joined = "\n\n".join(level_summaries)
    t0 = time.time()
    final = reduce_summaries(joined, model, tokenizer)
    log.write("reduce", level + 1, 0, len(level_summaries),
              REDUCE_USER.format(text=joined, target_words=REDUCE_TARGET_WORDS),
              final, tokenizer, time.time() - t0)

    return {
        "final_summary": final,
        "final_tokens": len(tokenizer.encode(final, add_special_tokens=False)),
        "levels": levels,
        "n_levels": len(levels),
        "n_collapse_rounds": level,
        "n_calls": len(log.records),
        "n_chunks": len(chunks),
        "log": log,
    }
