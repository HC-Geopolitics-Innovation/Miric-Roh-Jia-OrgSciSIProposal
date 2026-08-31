"""Constrained-decoding wrappers for the Layer-2 tagging passes.

STATUS: explored and SET ASIDE (researcher decision, 2026-08-23). The
production instrument is the free-form 1.2 path in `tagging.py`, whose
minimal output formats plus validating parsers already deliver what
constrained decoding promises (measured on 30 random blocks: 3.3 s/block,
1 parse error, quality verified in four dev rounds). This path, after
seven vendor patches, still mis-generated topic ids (the number-
termination problem in `jsonformer_vendor.generate_number`, patch 11
unverified) and re-encodes the full ~3k-token prompt for every generated
value. Kept for the methods appendix as a documented negative result.

Both passes run as two Jsonformer calls: a boolean probe (one forward pass
answering "does anything here match?") and, only if true, the value list.
The split exists because the vendored jsonformer always emits at least one
array element — about half of all blocks legitimately match nothing, and
the boolean makes that outcome a single constrained token comparison
instead of a forced false positive.

The model generates only values; every bracket, key, and quote is emitted
by the harness (`jsonformer_vendor`). Validation still runs through the
`tagging` parsers — constrained generation guarantees syntax, while range,
membership, and vocabulary checks stay where they always were.

Generation here is greedy and prompt-deterministic (vendor PATCH 5), so no
per-call seeding is needed on this path.
"""

from __future__ import annotations

import json
from typing import Any

from jsonformer_vendor import Jsonformer
import summarize as S
import tagging as T

#: Version stamped on constrained-path calls. -dev until the researcher
#: reads a dev round and the head-to-head against the 1.2 free-form path.
JF_PROMPT_VERSION = "item1-topic-tagging-2.0-dev"

GATE_USER_JF = """Below are numbered sentences from the Business section (Item 1) of one company's 10-K annual report, and a list of policy topics drawn from congressional science-committee hearings.

--- SENTENCES ---
{numbered}
--- END OF SENTENCES ---

--- TOPICS ---
{topics}
--- END OF TOPICS ---

A topic matches when at least one specific sentence describes a part of this company's business in the topic's subject area — its products, services, technologies, inputs, customers, or the regulations it operates under. The sentence does not need to mention a law, an agency, or a hearing. Be generous: include plausible matches. Do not count generic statements that are not about this company.

First report whether any topic matches (any_match). If true, list the matching topic ids."""

CONFIRM_USER_JF = """Below are numbered sentences from the Business section (Item 1) of one company's 10-K annual report, and a list of policy topics with definitions.

--- SENTENCES ---
{numbered}
--- END OF SENTENCES ---

--- TOPICS ---
{topics}
--- END OF TOPICS ---

Find every sentence that describes this company's business in a topic's subject area. The sentence does not need to mention a law, an agency, or a hearing. Skip generic statements that are not about this company. A sentence may match several topics.

Each match is one record: sentence number "s", topic id "t", and direction "d" as one letter — "O" if the sentence presents it as growth, demand, funding, or an advantage for the company; "T" if a risk, cost, restriction, or competitive pressure; "N" if neither.

First report whether any sentence matches (any_match). If true, list the records."""

_BOOL_SCHEMA = {"type": "object",
                "properties": {"any_match": {"type": "boolean"}}}
_GATE_SCHEMA = {"type": "object",
                "properties": {"topics": {"type": "array",
                                          "items": {"type": "number"}}}}
_CONFIRM_SCHEMA = {"type": "object", "properties": {
    "tags": {"type": "array", "items": {"type": "object", "properties": {
        "s": {"type": "number"}, "t": {"type": "number"},
        "d": {"type": "string"}}}}}}


def _as_int(v) -> Any:
    """generate_number returns floats; ids and indices must be integers."""
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def run_gate(model, tokenizer, sentences: list[str], start: int,
             labels_text: str):
    """Constrained Pass A. Returns (topic ids, canonical output text,
    parse-style errors) — the text is what CallLog stores, and the ids are
    validated by the same parser as the free-form path."""
    user = GATE_USER_JF.format(numbered=T.format_numbered(sentences, start),
                               topics=labels_text)
    prompt = S._render(tokenizer, T.SYSTEM, user)

    probe = Jsonformer(model, tokenizer, _BOOL_SCHEMA, prompt)()
    if not probe["any_match"]:
        return [], "[]", []

    raw = Jsonformer(model, tokenizer, _GATE_SCHEMA, prompt,
                     max_array_length=30, max_number_tokens=4)()
    out_text = json.dumps([_as_int(v) for v in raw["topics"]])
    topics, errors = T.parse_gate_topics(out_text, T_VALID_CACHE["topics"])
    return topics, out_text, errors


def run_confirm(model, tokenizer, sentences: list[str], start: int,
                entries_text: str, cand_ids: set[int]):
    """Constrained Pass B. Returns (records, canonical output text,
    parse-style errors); records carry full-word directions, as always."""
    user = CONFIRM_USER_JF.format(
        numbered=T.format_numbered(sentences, start), topics=entries_text)
    prompt = S._render(tokenizer, T.SYSTEM, user)

    probe = Jsonformer(model, tokenizer, _BOOL_SCHEMA, prompt)()
    if not probe["any_match"]:
        return [], "[]", []

    raw = Jsonformer(model, tokenizer, _CONFIRM_SCHEMA, prompt,
                     max_array_length=45, max_number_tokens=5,
                     max_string_token_length=3)()
    triples = [[_as_int(r.get("s")), _as_int(r.get("t")), r.get("d")]
               for r in raw["tags"]]
    out_text = json.dumps(triples)
    records, errors = T.parse_topic_tags(out_text, cand_ids, start,
                                         len(sentences))
    return records, out_text, errors


#: The gate parser needs the valid-topic set; callers register it once so
#: run_gate's signature stays parallel to the free-form path.
T_VALID_CACHE: dict = {"topics": set()}


def register_topics(topic_ids: set[int]) -> None:
    T_VALID_CACHE["topics"] = set(topic_ids)
