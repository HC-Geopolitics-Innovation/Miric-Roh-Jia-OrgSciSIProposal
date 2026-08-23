"""Stance-record extraction from legislator turns (Stage 3, Track 2).

The atomic unit of the stage is the **stance record**:

    (speaker [turn metadata]) x (evidence sentences [selected by index])
        x (topic [neutral noun phrase]) x (stance in {support, concern})

Design rules carried from the Stage-3 plan
(`quality_reports/plans/20260820_ plan/20260820_topic_extraction_plan.tex`):

* **Selection over generation.** Sentences are segmented deterministically and
  numbered BEFORE the model sees them; the model returns sentence numbers, so
  evidence cannot be hallucinated. The topic phrase is the single
  free-generation field, and it is validated downstream (clustering,
  convergence with Track 1, external gold).
* **Binary directional stance.** `support` and `concern` (concern-or-
  opposition merged as one negative pole). No neutral category: stance-free
  attention is covered by Track 1, and the crisp boundary is what a small
  model classifies reliably.
* **Neutral-noun-phrase topics.** The topic names the policy object itself,
  never a direction toward it; `lint_topic` flags directional wording so a
  violation is caught by code, not by hope.
* **Default to exclude.** A turn with no directional position returns an
  empty list, which is a valid, expected output.
"""

from __future__ import annotations

import json
import re
from typing import Any

import pysbd

#: Bumped on any change to the prompt strings below. "-dev" marks wording that
#: is still being iterated on the development split; the freeze before
#: validation renames it to "stance-extraction-1.0" (rule V1).
PROMPT_VERSION = "stance-extraction-0.3-dev"

#: Turns longer than this many sentences are extracted in windows of this
#: size, with global sentence numbering preserved across windows. Two reasons,
#: both measured in the 0.1-dev run: a long opening statement can carry more
#: records than one bounded completion holds, and the corpus has turns up to
#: 2,967 sentences that no single call should carry. ~5% of turns exceed it.
WINDOW_SENTENCES = 40

#: pysbd release this stage was built against. Segmentation defines the
#: sentence indices every record points at, so a silent version change would
#: silently re-index the evidence; better to fail loudly.
PYSBD_VERSION = "0.3.4"
if pysbd.__version__ != PYSBD_VERSION:
    raise ImportError(
        f"pysbd {pysbd.__version__} found, {PYSBD_VERSION} required — "
        "sentence indices are only comparable within one segmenter version"
    )

_SEGMENTER = pysbd.Segmenter(language="en", clean=False)

#: Sentences shorter than this many characters are kept in the numbering (so
#: indices match the visible text) but a record citing only such fragments is
#: suspect; the parse report counts them.
MIN_SENTENCE_CHARS = 15

STANCES = ("support", "concern")

#: Directional words that must not appear inside a topic phrase — direction
#: belongs in the stance field. Word-boundary match, case-insensitive. The
#: lint flags for re-prompting or review; it does not silently rewrite.
DIRECTIONAL_LINT = re.compile(
    r"\b(?:ban(?:ning)?|block(?:ing)?|stop(?:ping)?|halt(?:ing)?|"
    r"oppos(?:e|ing|ition)|support(?:ing)?|defend(?:ing)?|protect(?:ing|ion)?|"
    r"against|anti|pro|promot(?:e|ing|ion)|expand(?:ing)?|restrict(?:ing|ion)?|"
    r"repeal(?:ing)?|eliminat(?:e|ing|ion))\b",
    re.IGNORECASE,
)

SYSTEM = (
    "You are an expert reader of United States congressional hearing "
    "transcripts. You report only what the text states."
)

USER = """Below is one speaking turn by a member of Congress, split into numbered sentences.

Task: find every sentence in which the member takes a directional position on a policy object, and return one record per position.

A record has three fields:
- "sentences": the sentence number(s) expressing the position (1-3 consecutive numbers);
- "topic": the policy object, as a short and specific neutral noun phrase (the policy, program, regulation, technology, practice, or budget item itself; never directional wording; name the specific object, not the agency or field around it);
- "stance": "support" if the member endorses, advocates, or urges adoption, funding, or expansion of the topic; "concern" if the member expresses worry, criticism, or objection toward the topic, or urges its restriction, delay, or scrutiny.

The stance is toward the topic exactly as you phrase it. Before returning a record, check that it reads sensibly as "the member supports [topic]" or "the member is concerned about [topic]". If the topic is a problem or harm, the stance toward it is "concern", never "support".

The topic must be the object the member takes a position ON. Entities mentioned only as examples, comparisons, or asides are not topics, and a bare number or amount is never a topic. If several consecutive sentences express the same position on the same topic, return one record covering them, not one record per sentence.

Example: "Youth vaping is an epidemic we cannot ignore." -> {{"sentences": [n], "topic": "youth e-cigarette use", "stance": "concern"}}
Example: "This bill funds the research our labs badly need." -> {{"sentences": [n], "topic": "research funding bill", "stance": "support"}}

Do not return records for: procedure (recognitions, time, the record), courtesies, introductions, logistics, questions asked without an expressed position, or factual statements without evaluation. If no sentence takes a directional position, return an empty list. When in doubt, do not extract.

--- TURN (Speaker: {speaker}) ---
{numbered}
--- END OF TURN ---

Return only a JSON list of records. Your very first output character must be [."""


#: Truncation markers: everything from the first match onward is written
#: material, not speech. Two families, both measured on the SST corpus before
#: being written down here:
#: * adjournment — the post-adjournment appendix (submitted statements,
#:   post-hearing Q&A) rides on the last speaker's turn: 748,830 sentences,
#:   35.4% of the raw legislator-sentence corpus;
#: * inserted documents — "[The prepared statement of X follows:]" blocks
#:   appear inside mid-hearing turns, and were the direct cause of every
#:   json_parse failure in the first extraction dev run.
_TRUNCATE_AT = re.compile(
    r"\[\s*Whereupon|hearing (?:was |is )?adjourned"
    r"|\[The [^\]]{0,80}follows[:.\]]",
    re.IGNORECASE,
)

#: A sentence that is only a bracketed stage direction ("[Laughter.]",
#: "[Applause.]", "[Pause.]").
_STAGE_DIRECTION = re.compile(r"\[[^\]]{2,60}\]\.?")


def _is_header(sentence: str) -> bool:
    """An inline all-caps heading ("STATEMENT OF MR. DAVID KEATING, ...")."""
    letters = [c for c in sentence if c.isalpha()]
    return len(sentence) >= 20 and len(letters) >= 10 and \
        sum(c.isupper() for c in letters) / len(letters) >= 0.8


def clean_turn_sentences(sentences: list[str], surname: str | None,
                         honorific: str | None) -> tuple[list[str], dict[str, int]]:
    """Deterministic cleanup of one turn's sentence list, with counts.

    Applied between segmentation and everything downstream, in this order:

    1. truncate at the first adjournment / inserted-document marker
       (the marker sentence and all that follows are written material);
    2. drop the leading speaker-label echo ("Senator Dorgan.") — GPO repeats
       the turn opening inside the text, so 99% of turns start with it;
    3. drop bracketed stage directions and all-caps inline headers.

    Returns the kept sentences and a per-rule removal count, so the notebook
    can report exactly what each rule cost — a filter whose removals are not
    reported is a silent sample choice.
    """
    removed = {"truncated": 0, "label_echo": 0, "stage_direction": 0, "header": 0}

    for i, sentence in enumerate(sentences):
        if _TRUNCATE_AT.search(sentence):
            removed["truncated"] = len(sentences) - i
            sentences = sentences[:i]
            break

    if sentences:
        first = sentences[0].rstrip(".")
        if len(sentences[0]) <= 40 and (
            (surname and first.endswith(surname))
            or (honorific and first == honorific)
        ):
            removed["label_echo"] = 1
            sentences = sentences[1:]

    kept: list[str] = []
    for sentence in sentences:
        if _STAGE_DIRECTION.fullmatch(sentence.strip()):
            removed["stage_direction"] += 1
        elif _is_header(sentence):
            removed["header"] += 1
        else:
            kept.append(sentence)
    return kept, removed


def segment_sentences(text: str) -> list[str]:
    """Deterministic sentence segmentation of one block of text.

    Whitespace inside the block is flattened first: GPO hard-wraps lines and
    pysbd treats stray newlines as boundaries, which would fragment the
    numbering the records point at.
    """
    flat = re.sub(r"\s+", " ", text).strip()
    if not flat:
        return []
    return [s.strip() for s in _SEGMENTER.segment(flat) if s.strip()]


def segment_turn(text: str) -> list[str]:
    """One turn to sentences, segmented paragraph block by paragraph block.

    Segmenting per block is the guard against runaway "sentences": GPO's
    nested quote marks and punctuation-free stretches can blind pysbd, and on
    flattened text that produced 2,400-word "sentences" spanning hundreds of
    paragraphs. A sentence can now never cross a paragraph boundary, which
    caps the damage of any missegmentation at one paragraph. (Measured on the
    worst SST case: 2,421-word blob -> 602 sentences, max 64 words.)
    """
    sentences: list[str] = []
    for block in re.split(r"\n\s*\n", text or ""):
        sentences.extend(segment_sentences(block))
    return sentences


def format_numbered(sentences: list[str], start: int = 1) -> str:
    """Sentences as the model sees them: one per line, globally numbered.

    `start` carries the turn-global index of the first sentence, so a windowed
    long turn shows [41]..[80] and its records point at the same indices every
    other window and the stored table use.
    """
    return "\n".join(f"[{i}] {s}" for i, s in enumerate(sentences, start))


def render_user(sentences: list[str], speaker: str, start: int = 1) -> str:
    """The extraction prompt for one turn (or one window of a long turn)."""
    return USER.format(speaker=speaker,
                       numbered=format_numbered(sentences, start=start))


def windows(sentences: list[str], size: int = WINDOW_SENTENCES):
    """Yield (start_index, window) pairs covering the turn, 1-indexed.

    A turn at or under `size` yields itself once; longer turns are cut into
    consecutive fixed-size windows. Numbering is turn-global, so records
    point at the same indices whichever window produced them. A position
    (1-3 consecutive sentences) can in principle straddle a boundary; the
    boundary falls inside a turn in ~5% of turns, and the dev read is where
    that cost is checked rather than assumed.
    """
    for offset in range(0, max(len(sentences), 1), size):
        yield offset + 1, sentences[offset:offset + size]


def merge_adjacent_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    """Deterministic insurance against per-sentence splitting of one position.

    Records carrying the same (topic, stance) — topic compared
    case-insensitively — whose sentence ranges touch or sit within two
    sentences of each other are merged into one record. The prompt asks the
    model to group these itself; when it does not, this rule keeps the
    intensity counts (records per topic) from inflating with verbosity.
    Returns the merged list and the number of merges, which the caller
    reports rather than hides.
    """
    if not records:
        return records, 0
    ordered = sorted(records, key=lambda r: (r["topic"].strip().lower(),
                                             r["stance"], r["sentences"][0]))
    merged: list[dict[str, Any]] = []
    n_merged = 0
    for record in ordered:
        if merged:
            prev = merged[-1]
            if (prev["topic"].strip().lower() == record["topic"].strip().lower()
                    and prev["stance"] == record["stance"]
                    and record["sentences"][0] - prev["sentences"][-1] <= 2):
                prev["sentences"] = sorted(set(prev["sentences"] + record["sentences"]))
                n_merged += 1
                continue
        merged.append(dict(record))
    merged.sort(key=lambda r: r["sentences"][0])
    return merged, n_merged


def lint_topic(phrase: str) -> str | None:
    """The directional word a topic phrase contains, or None if clean."""
    match = DIRECTIONAL_LINT.search(phrase or "")
    return match.group(0) if match else None


# --------------------------------------------------------------- Track 1 ----
# Summary-side topics: each Stage-2 final summary maps to a ranked list of at
# most TRACK1_MAX_TOPICS neutral noun phrases, one call per hearing. No stance
# field — Track 1 exists to cover stance-free attention (plan §Track 1), to
# feed the pooled phrase set for taxonomy induction, and to anchor the
# Track-1 vs. Track-2 convergence check. The topic-phrase rules are carried
# verbatim from the Track-2 prompt so the two phrase pools obey one grammar.

#: Versioned separately from the Track-2 prompt: the two iterate on different
#: evidence and freeze at different times.
TRACK1_PROMPT_VERSION = "summary-topics-0.2-dev"

TRACK1_MAX_TOPICS = 5

TRACK1_USER = """Below is a summary of one United States congressional hearing.

Task: list the main topics the hearing covered, ordered from most to least central.

A topic is a short and specific neutral noun phrase: the policy, program, regulation, technology, practice, or budget item itself; never directional wording; name the specific object, not the agency or field around it. An agency, company, or country is never a topic by itself; name the policy object involving it. A bill counts as a topic by its subject or name, never as a bare bill number such as "H.R. 1". A bare number or amount is never a topic. Entities mentioned only as examples, comparisons, or asides are not topics.

List at most {max_topics} topics. Include a topic only if the hearing gave it substantial attention — most summaries support 2 to 4 topics, and padding to {max_topics} is worse than stopping early. Every major subject of the hearing should appear.

--- SUMMARY ---
{summary}
--- END OF SUMMARY ---

Return only a JSON list of topic strings, most central first. Your very first output character must be [."""


def render_track1(summary: str) -> str:
    """The topic-listing prompt for one hearing summary."""
    return TRACK1_USER.format(max_topics=TRACK1_MAX_TOPICS, summary=summary)


def parse_topics(output: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Validate one Track-1 output into ranked topics plus named errors.

    Same philosophy as `parse_records`: every code-checkable property is
    checked and counted. Structural failures drop the item; a directionality
    lint keeps it but carries the flag. Case-insensitive duplicates are
    dropped (the first, higher-ranked occurrence wins) and counted; topics
    beyond TRACK1_MAX_TOPICS are dropped and counted, so a model that pads
    is visible in the error rates rather than in the phrase pool.
    """
    errors: list[str] = []
    text = output.strip()
    if text.startswith("```"):
        errors.append("markdown_fence")
        text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text).strip()

    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return [], errors + ["json_parse"]
    if not isinstance(raw, list):
        return [], errors + ["not_a_list"]

    topics: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in raw:
        if not (isinstance(item, str) and item.strip()):
            errors.append("topic_not_string")
            continue
        phrase = item.strip()
        if phrase.lower() in seen:
            errors.append("duplicate_topic")
            continue
        if len(topics) >= TRACK1_MAX_TOPICS:
            errors.append("too_many_topics")
            continue
        seen.add(phrase.lower())
        topics.append({
            "rank": len(topics) + 1,
            "topic": phrase,
            "topic_lint": lint_topic(phrase),
        })
    return topics, errors


def parse_records(output: str, n_sentences: int,
                  start: int = 1) -> tuple[list[dict[str, Any]], list[str]]:
    """Validate one model output into records plus a list of named errors.

    Every check that can be made by code is made here, so a bad output is a
    counted event rather than a silent row: JSON shape, field presence,
    stance vocabulary, index validity (1..n, at most 3, consecutive), and the
    topic directionality lint. Records that fail a structural check are
    dropped and counted; a lint hit keeps the record but carries the flag,
    because the phrase may still be usable after review.
    """
    errors: list[str] = []
    text = output.strip()
    # Tolerate a markdown fence; its presence is still recorded as an error
    # so the rate is visible.
    if text.startswith("```"):
        errors.append("markdown_fence")
        text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text).strip()

    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return [], errors + ["json_parse"]
    if not isinstance(raw, list):
        return [], errors + ["not_a_list"]

    records: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            errors.append("record_not_object")
            continue
        topic = item.get("topic")
        stance = item.get("stance")
        sent = item.get("sentences")
        if isinstance(sent, int):
            sent = [sent]
        if not (isinstance(topic, str) and topic.strip()):
            errors.append("missing_topic")
            continue
        if stance not in STANCES:
            errors.append("bad_stance")
            continue
        if not (isinstance(sent, list) and sent
                and all(isinstance(i, int) for i in sent)):
            errors.append("bad_sentences_field")
            continue
        sent = sorted(set(sent))
        if sent[0] < start or sent[-1] > start + n_sentences - 1:
            errors.append("index_out_of_range")
            continue
        if len(sent) > 3 or sent[-1] - sent[0] != len(sent) - 1:
            errors.append("indices_not_consecutive")
            continue
        records.append({
            "sentences": sent,
            "topic": topic.strip(),
            "stance": stance,
            "topic_lint": lint_topic(topic),
        })
    return records, errors
