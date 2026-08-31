"""Sentence-block topic tagging: the Layer-2 instrument of Stage 4.

Layer 2 re-measures firm-topic relevance with a small LLM, independently of
the embedding rail (Layer 1). The model reads Item 1 sentences in
document-order blocks, numbered exactly as the Track-2 stance extraction
numbered hearing sentences, and cites sentence indices for every tag. No
cosine score, ranking, centroid, or top-k selection — no Layer-1 output of
any kind — enters a prompt, so agreement between the two layers downstream
is evidence about the measurement, not a construction of the sampling.

Two passes per block, both index-cited:

* **Pass A, the gate** (`render_gate_user`): all 111 topic *labels* ->
  which sentences match which topics. Labels, not the Stage-3 themes: the
  0.1-dev round showed the theme layer is a hearing-map grouping, not a
  retrieval index — "EPA air and water regulations" sat invisible inside a
  theme labeled "Telecommunications and Trade Policy", and a Clean Air Act
  compliance block gated to nothing. Generous by instruction; the gate's
  miss rate is *measured* by a no-gate audit on a random block sample.
* **Pass B, the confirmation** (`render_confirm_user`): the gate's
  candidate topics with their frozen definitions -> (sentence index,
  topic_id, direction) records, direction in {opportunity, threat,
  neutral}.

Index citation replaces quote matching: a cited index either resolves to a
sentence in the block or the record is rejected — there is no quote to
paraphrase. Aggregation to (firm, fyear, topic) cells happens downstream by
counting tagged sentences, so intensity is a measured quantity, never a
scalar asked of the model.
"""

from __future__ import annotations

import json
import re
from typing import Any

#: Frozen release marker stamped on every logged call. Bump on any change to
#: the prompt strings, generation caps, or parser behavior; freeze (drop
#: -dev) before the production run.
#: 0.1-dev: theme-gated variant — retired after the dev read (see above).
#: 0.2-dev: label gate; its dev round hit the confirm cap on a dense block
#:   (39 cited sentences > 512 tokens of JSON) and lost the whole call.
#: 0.3-dev: confirm cap 1024 + truncated-array salvage in the parsers.
#: 1.0: frozen 2026-08-22, identical strings to 0.3-dev, after the
#:   three-round dev read in 04 (researcher-approved: EPA/threat block
#:   recovered in full, gate-then-confirm division of labor verified).
#: 1.1: gate output is a bare list of topic ids. The 1.0 production run
#:   (aborted at ~150 blocks) showed the gate enumerating whole sentence
#:   ranges per topic — 268 output tokens on average, frequent 512-token
#:   caps that silently truncated the topic list, and 12s/call of decode
#:   for citations nothing downstream reads (Pass B re-derives sentence
#:   citations from scratch). Grounding stays in the instruction; the
#:   citations leave the output.
#: 1.2: confirm records become compact triples [sentence, topic, "O|T|N"]
#:   with a one-letter direction legend and shorter, plainer instructions.
#:   The 1.1 design rule applied to Pass B as well: a small model keeps
#:   JSON syntax but not verbosity restraint, so the output space itself
#:   is made minimal — repeated object keys were most of confirm decoding
#:   (~237 output tokens/call measured on the 150-block benchmark).
#: 1.2 is the production instrument (decision 2026-08-23): 3.3 s/block
#:   and one parse error on 30 random blocks; a constrained-decoding
#:   alternative (jsonformer) was evaluated the same day and set aside —
#:   see lib/constrained.py for the record.
PROMPT_VERSION = "item1-topic-tagging-1.2"

#: Sentences per tagging call. Track 2's window size (`stance.py`), so both
#: instruments read the record in units of the same measured size.
BLOCK_SENTENCES = 40

DIRECTIONS = ("opportunity", "threat", "neutral")

#: A bare id list: 111 ids would be ~350 tokens, a typical block emits a
#: handful. The 1.0 cap of 512 was reached by sentence-range enumeration
#: and truncated topic lists — the format change removes the failure mode.
GATE_MAX_NEW_TOKENS = 160
#: A dense block is ~40 confirmable sentences; as 1.2 triples that is
#: ~9 tokens each (~360 for the worst block), so 512 leaves headroom the
#: 1.0 object format needed 1024 for.
CONFIRM_MAX_NEW_TOKENS = 512

SYSTEM = (
    "You are an expert reader of corporate 10-K filings with a working "
    "knowledge of United States science and technology policy. You report "
    "only what the text states."
)

GATE_USER = """Below are numbered consecutive sentences from the Business section (Item 1) of one company's 10-K annual report, followed by a list of policy topics drawn from congressional science-committee hearings.

--- SENTENCES ---
{numbered}
--- END OF SENTENCES ---

--- TOPICS ---
{topics}
--- END OF TOPICS ---

A topic matches when at least one specific sentence describes a part of this company's business that falls in the topic's subject area — its products, services, technologies, inputs, customers, or the regulations it operates under. The sentence does not need to mention any law, agency, or hearing. Be generous: include plausible matches. Do not include a topic on the strength of generic statements that are not about this company's business.

Answer with only a JSON list of the matching topic ids:
[<topic id>, <topic id>]

If no topic matches, answer []."""

CONFIRM_USER = """Below are numbered sentences from the Business section (Item 1) of one company's 10-K annual report, and a list of policy topics with definitions.

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

If nothing matches, answer []."""


def format_numbered(sentences: list[str], start: int) -> str:
    """Sentences as the model sees them, numbered filing-globally.

    `start` is the display number of the block's first sentence (its filing
    sent_idx + 1), so cited numbers resolve to table rows by subtraction and
    are unique within the filing — the Track-2 convention.
    """
    return "\n".join(f"[{i}] {s}" for i, s in enumerate(sentences, start))


def format_topic_labels(codebook) -> tuple[str, set[int]]:
    """The Pass-A gate list: every frozen topic as `[id] label`, no
    definitions — 111 short lines the model can actually scan per block."""
    lines = [f"[{t.topic_id}] {t.label}" for t in codebook.itertuples()]
    return "\n".join(lines), set(int(t) for t in codebook["topic_id"])


def format_topic_entries(codebook, topic_ids) -> tuple[str, set[int]]:
    """The Pass-B list for one block's candidates: id, label, frozen
    definition."""
    grp = codebook.loc[codebook["topic_id"].isin(set(topic_ids))]
    lines = [f"[{t.topic_id}] {t.label} — {t.definition}"
             for t in grp.itertuples()]
    return "\n".join(lines), set(int(t) for t in grp["topic_id"])


def render_gate_user(sentences: list[str], start: int, topics: str) -> str:
    return GATE_USER.format(numbered=format_numbered(sentences, start),
                            topics=topics)


def render_confirm_user(sentences: list[str], start: int, topics: str) -> str:
    return CONFIRM_USER.format(numbered=format_numbered(sentences, start),
                               topics=topics)


def _load_json_list(text: str, errors: list[str]):
    """Shared JSON envelope handling, the stance-parser conventions.

    A completion cut off at the generation cap ends mid-array; every
    complete `{...}` object before the cut is still valid data, so on a
    parse failure the salvage path recovers those objects individually and
    records the truncation instead of discarding the call. Our records
    never nest braces, which is what makes the flat regex sound.
    """
    text = text.strip()
    if text.startswith("```"):
        errors.append("markdown_fence")
        text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text).strip()
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        # complete inner records — {...} objects or [..] triples — survive
        # a truncated outer array; the outer "[" never matches the inner-
        # array pattern because its body contains brackets
        salvaged = []
        for m in re.finditer(r"\{[^{}]*\}|\[[^\[\]{}]*\]", text):
            try:
                salvaged.append(json.loads(m.group()))
            except json.JSONDecodeError:
                continue
        if salvaged:
            errors.append("json_truncated_salvaged")
            return salvaged
        errors.append("json_parse")
        return None
    if not isinstance(raw, list):
        errors.append("not_a_list")
        return None
    return raw


def parse_gate_topics(output: str,
                      valid_topics: set[int]) -> tuple[list[int], list[str]]:
    """Pass-A output -> validated, deduplicated topic ids.

    Accepts bare ids, numeric strings, or leftover 1.0-style
    ``{"topic": id}`` objects; anything not resolving to a codebook id is
    counted and dropped.
    """
    errors: list[str] = []
    raw = _load_json_list(output, errors)
    if raw is None:
        return [], errors

    topics: list[int] = []
    seen: set[int] = set()
    for item in raw:
        if isinstance(item, dict):
            item = item.get("topic")
        if isinstance(item, str) and item.strip().isdigit():
            item = int(item.strip())
        if not (isinstance(item, int) and item in valid_topics):
            errors.append("unknown_topic")
            continue
        if item in seen:
            errors.append("duplicate_topic")
            continue
        seen.add(item)
        topics.append(item)
    return topics, errors


#: 1.2 letters and the pre-1.2 full words both resolve; anything else is
#: a rejected direction.
_DIRECTION_MAP = {"O": "opportunity", "T": "threat", "N": "neutral",
                  "opportunity": "opportunity", "threat": "threat",
                  "neutral": "neutral"}


def parse_topic_tags(output: str, valid_topics: set[int], start: int,
                     n_sentences: int) -> tuple[list[dict[str, Any]], list[str]]:
    """Pass-B output -> validated {sentence, topic, direction} records.

    The 1.2 record is a ``[sentence, topic, "O"|"T"|"N"]`` triple; earlier
    dict records and full-word directions still parse, so a mixed or
    old-style completion degrades to counted errors, never to a crash.
    Each record must cite a shown sentence, a topic from the offered
    candidates, and a direction from the closed vocabulary; (sentence,
    topic) pairs are deduplicated keeping the first, so a rambling
    completion cannot double-count intensity. Directions are always
    returned as full words.
    """
    errors: list[str] = []
    raw = _load_json_list(output, errors)
    if raw is None:
        return [], errors

    records: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for item in raw:
        if isinstance(item, dict):
            sent, topic, direction = (item.get("sentence"), item.get("topic"),
                                      item.get("direction"))
        elif isinstance(item, list) and len(item) == 3:
            sent, topic, direction = item
        else:
            errors.append("bad_record")
            continue
        if isinstance(sent, str) and sent.strip().isdigit():
            sent = int(sent.strip())
        if isinstance(topic, str) and topic.strip().isdigit():
            topic = int(topic.strip())
        direction = _DIRECTION_MAP.get(
            direction.strip() if isinstance(direction, str) else direction)
        if not (isinstance(sent, int) and start <= sent <= start + n_sentences - 1):
            errors.append("index_out_of_range")
            continue
        if not (isinstance(topic, int) and topic in valid_topics):
            errors.append("unknown_topic")
            continue
        if direction is None:
            errors.append("bad_direction")
            continue
        if (sent, topic) in seen:
            errors.append("duplicate_pair")
            continue
        seen.add((sent, topic))
        records.append({"sentence": sent, "topic": topic, "direction": direction})
    return records, errors
