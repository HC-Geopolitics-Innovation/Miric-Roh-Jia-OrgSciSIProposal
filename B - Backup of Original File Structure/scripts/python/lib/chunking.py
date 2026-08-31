"""Pack a hearing's speaking turns into chunks a model can read in one call.

The unit is the **speaking turn**, not the paragraph. A turn is one person's
uninterrupted contribution, and splitting it puts half an argument in one call
and half in another, with neither call able to see who was speaking or what they
were answering. So turns are packed whole, greedily, until the next one would
overflow the budget.

A turn longer than the whole budget has to be divided, and there the split falls
on a paragraph boundary rather than mid-sentence. `n_turns_split` counts how
often that happens so the cost is visible rather than assumed to be zero.

Token counts come from the model's own tokenizer. A character heuristic is off by
enough on transcript text — heavy punctuation, names, dollar figures — to either
overflow the context or waste a third of it.
"""

from __future__ import annotations

from typing import Any, Iterable

#: Room left inside the model's context for the instructions and the generated
#: summary. The chunk budget is the context minus this.
DEFAULT_RESERVE_TOKENS = 2_048


def format_turn(turn: dict[str, Any]) -> str:
    """One turn as the model sees it: a speaker label, then what they said.

    The label matters. Without it the reduce step cannot attribute a position to
    anyone, and attribution is most of what a hearing summary is for.

    Senate transcripts record the presiding officer's turns as "The Chairman"
    with no surname. The honorific alone is the label then: appending
    "Unidentified speaker" would tag the hearing's most frequent speaker as
    unknown and push the model to guess who is presiding.
    """
    name = turn.get("surname") or ""
    honorific = turn.get("honorific") or ""
    who = f"{honorific} {name}".strip() or "Unidentified speaker"
    if turn.get("section") == "qfr":
        who = f"{who} (submitted for the record)"
    return f"{who}: {turn['text']}"


def _encoded_length(tokenizer, text: str) -> int:
    return len(tokenizer.encode(text, add_special_tokens=False))


def _token_slice(text: str, tokenizer, max_tokens: int) -> list[str]:
    """Cut text into pieces that each re-encode within budget.

    `decode(ids[:n])` followed by `encode` is **not** the identity: BPE re-merges
    across the cut, so a slice of exactly `max_tokens` ids can come back longer
    than `max_tokens`. Taking the slice at face value is what puts an over-budget
    chunk into the output. Each piece is therefore re-encoded and shortened until
    it actually fits.
    """
    ids = tokenizer.encode(text, add_special_tokens=False)
    pieces: list[str] = []
    start = 0
    while start < len(ids):
        take = min(max_tokens, len(ids) - start)
        piece = tokenizer.decode(ids[start:start + take])
        while take > 64 and _encoded_length(tokenizer, piece) > max_tokens:
            take = int(take * 0.9)
            piece = tokenizer.decode(ids[start:start + take])
        pieces.append(piece)
        start += take
    return pieces


def chunk_turns(
    turns: Iterable[dict[str, Any]],
    tokenizer,
    max_tokens: int,
    spoken_only: bool = True,
) -> list[dict[str, Any]]:
    """Group consecutive turns into chunks of at most `max_tokens` tokens.

    Parameters
    ----------
    turns : iterable of dict
        The `turns` column of one hearing, in document order.
    tokenizer : PreTrainedTokenizerBase
        The tokenizer of the model that will read the chunks.
    max_tokens : int
        Budget per chunk, already net of instructions and generation.
    spoken_only : bool
        Drop turns marked `qfr`. Questions for the record were not spoken at the
        hearing, and mixing them into the spoken record silently changes what the
        summary is a summary of.

    Returns
    -------
    list of dict
        One entry per chunk: ``text``, ``n_turns``, ``n_tokens``, ``speakers``,
        and ``split_turn`` — true when the chunk is part of a turn too long to
        fit on its own.
    """
    selected = [t for t in turns if not (spoken_only and t.get("section") == "qfr")]

    # Turns are joined with a blank line, and those separators are tokens too.
    # Summing the turns alone under-counts the text the model actually receives,
    # which is the second way an over-budget chunk gets emitted.
    join_cost = _encoded_length(tokenizer, "\n\n")

    chunks: list[dict[str, Any]] = []
    current: list[str] = []
    current_tokens = 0
    current_speakers: list[str] = []

    def flush(split: bool = False) -> None:
        nonlocal current, current_tokens, current_speakers
        if not current:
            return
        text = "\n\n".join(current)
        speakers = sorted(set(current_speakers))
        # Packing predicts a length by summing parts; the emitted text is what
        # the model reads. Where the two disagree, divide rather than ship an
        # over-budget chunk, and mark it so the cost stays visible.
        if _encoded_length(tokenizer, text) > max_tokens:
            for piece in _split_long_turn(text, tokenizer, max_tokens):
                chunks.append({
                    "text": piece,
                    "n_turns": len(current),
                    "n_tokens": _encoded_length(tokenizer, piece),
                    "speakers": speakers,
                    "split_turn": True,
                })
        else:
            chunks.append({
                "text": text,
                "n_turns": len(current),
                # Measured on the emitted text, not summed from its parts.
                "n_tokens": _encoded_length(tokenizer, text),
                "speakers": speakers,
                "split_turn": split,
            })
        current, current_tokens, current_speakers = [], 0, []

    for turn in selected:
        rendered = format_turn(turn)
        n = len(tokenizer.encode(rendered, add_special_tokens=False))

        if n > max_tokens:
            # One turn that cannot fit. Emit what is pending, then divide this
            # turn on paragraph boundaries — never mid-sentence.
            flush()
            for piece in _split_long_turn(rendered, tokenizer, max_tokens):
                chunks.append({
                    "text": piece,
                    "n_turns": 1,
                    "n_tokens": _encoded_length(tokenizer, piece),
                    "speakers": [turn.get("surname") or "Unidentified speaker"],
                    "split_turn": True,
                })
            continue

        cost = n + (join_cost if current else 0)
        if current_tokens + cost > max_tokens:
            flush()
            cost = n

        current.append(rendered)
        current_tokens += cost
        current_speakers.append(turn.get("surname") or "Unidentified speaker")

    flush()
    return chunks


def _split_long_turn(text: str, tokenizer, max_tokens: int) -> list[str]:
    """Divide one over-long turn at paragraph boundaries."""
    join_cost = _encoded_length(tokenizer, "\n\n")
    paragraphs = text.split("\n\n")
    out: list[str] = []
    buffer: list[str] = []
    buffer_tokens = 0

    for paragraph in paragraphs:
        n = _encoded_length(tokenizer, paragraph)
        if n > max_tokens:
            # A single paragraph over budget. Nothing left but a token cut.
            if buffer:
                out.append("\n\n".join(buffer))
                buffer, buffer_tokens = [], 0
            out.extend(_token_slice(paragraph, tokenizer, max_tokens))
            continue
        cost = n + (join_cost if buffer else 0)
        if buffer_tokens + cost > max_tokens:
            out.append("\n\n".join(buffer))
            buffer, buffer_tokens = [], 0
            cost = n
        buffer.append(paragraph)
        buffer_tokens += cost

    if buffer:
        out.append("\n\n".join(buffer))

    # Final guarantee. Everything above predicts a length by summing parts, and a
    # prediction is not the emitted text — separators cost tokens and BPE
    # re-merges across a cut. Re-encode every piece and divide any that is still
    # over, so the budget is an invariant rather than an aim.
    verified: list[str] = []
    for piece in out:
        if _encoded_length(tokenizer, piece) <= max_tokens:
            verified.append(piece)
        else:
            verified.extend(_token_slice(piece, tokenizer, max_tokens))
    return verified
