"""Turn a GovInfo hearing HTML rendition into a list of paragraphs.

GPO serves congressional hearings as a single `<pre>` block of fixed-width text
inside a minimal HTML wrapper. There is no paragraph markup; the structure is
carried entirely by indentation, and the convention is that a paragraph begins
with four spaces and continues on unindented lines until the next four-space
line. That is the whole rule, and `group_paragraphs` implements exactly it.

**The paragraph rule is preserved from the earlier pipeline deliberately.** It
determines what the summarization stage sees as a unit and what the attribution
step matches speaker names against, so changing it would change the model's
input while leaving the prompts untouched — a silent change to the method
dressed up as a refactor. What has changed is that the rule is now stated, its
edge cases are named below, and the notebook that calls it reports how many
paragraphs each decision produces.

Two edge cases are inherited rather than fixed, and both are worth knowing:

* **Blank lines do not separate paragraphs.** Only the four-space indent does.
  A paragraph broken across a page boundary rejoins as one paragraph, which is
  usually right, and a heading sitting alone between blank lines attaches to
  whichever paragraph precedes it, which is usually wrong.
* **Front matter is not removed here.** The tables of contents, witness lists,
  and page-number rows in the first several hundred lines all become
  paragraphs. Downstream steps drop them — the attribution step skips anything
  containing `...`, which is what a table-of-contents dot leader looks like —
  but this function returns everything so that the drop happens where it can be
  counted.

Called from `scripts/python/01_dataset_construction/04_build_hearing_corpus.ipynb`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from speakers import TURN_OPENING

#: A paragraph begins at a line indented by at least this many spaces. GPO's
#: fixed-width layout uses exactly four; the earlier pipeline tested for the
#: literal four-space prefix and this keeps that behaviour.
INDENT = "    "

#: Share of non-blank lines that must carry the indent for the convention to be
#: considered present. A handful of packages — 5 in a 2,856-hearing sample, four
#: of them from 2006 — are printed with no indentation at all and separate
#: paragraphs with blank lines instead. On those the indent rule collapses the
#: whole document into a few enormous paragraphs (CHRG-109hhrg30382: 190,695
#: characters in 4 paragraphs) and no speaking turn can be found, because a turn
#: is recognised at the start of a paragraph. Measured across the corpus, real
#: hearings sit at 17 percent indented lines and the failures at 0.1-1.0 percent,
#: so the two populations are far apart and this threshold is not delicate.
INDENT_MIN_SHARE = 0.05

#: Dot leaders in a table of contents. A paragraph carrying one is front matter
#: rather than speech, and the attribution step drops it. Recorded here so the
#: notebook can count how much of a transcript is front matter before anything
#: is discarded.
DOT_LEADER = re.compile(r"\.{3,}")

#: GPO stamps the printed page number into the text stream at column zero, so it
#: lands inside whatever paragraph is being spoken when the page turns:
#: "The Chairman. Thank you. [[Page 6]]". It is 0.10 percent of non-blank lines
#: — 384 of 400,608 measured — and carries nothing a summarizer or a topic
#: extractor can use, so it is removed and counted rather than passed through.
PAGE_MARKER = re.compile(r"\[\[Page[^\]]*\]\]")

#: GovInfo writes this where a hearing's body would be when the document was
#: never digitized past its cover page. Reading the marker beats guessing from
#: a length threshold — but it only covers a third of the text-less files, so
#: see `has_usable_text` for the rest.
NO_TEXT_MARKER = b"<TEXT NOT AVAILABLE>"

#: Opens a block of written questions answered for the record. GPO announces
#: these in a bracketed aside, and the transcript states outright that the
#: exchange did not happen at the hearing:
#:
#:     [The following questions were not asked at the hearing, but were
#:      submitted to the Department for response subsequent to the hearing:]
#:     [Questions from Mr. Hoyer and responses follow:]
#:     Questions Submitted by Senator Herb Kohl
#:
#: The vocabulary here is the one the corpus actually uses, taken from every
#: bracketed aside in 154 sampled transcripts rather than from the first example
#: that turned up. `[The information follows:]` and `[The statement follows:]`
#: are deliberately excluded: they are exhibits inserted into a speaker's turn,
#: not a question-and-answer exchange, and they are far more common (583 and 177
#: against 44 for the clearest QFR phrasing).
QFR_OPENING = re.compile(
    r"^\[?\s*(?:"
    r"the following questions? (?:were|was) (?:not asked at the hearing|submitted)"
    r"|(?:a\s+)?questions?\s+from\b.{0,90}?(?:responses?|answers?)\s+follows?"
    r"|questions?\s+submitted\s+(?:by|to|for the record)"
    r"|the response to the aforementioned question follows"
    r")",
    re.I,
)

#: Inside a written block the exchange alternates on these openers.
QA_OPENING = re.compile(r"^(?:Question|Answer|Response)\.\s")


def extract_text(html: bytes | str) -> str:
    """Plain text of a GovInfo hearing rendition.

    BeautifulSoup rather than a regex strip: the older renditions carry stray
    unclosed tags inside the `<pre>` block, and a regex either eats the text
    around them or leaves the markup in the transcript.
    """
    return BeautifulSoup(html, "html.parser").get_text()


def _uses_indent_convention(text: str) -> tuple[bool, float]:
    """Does this document mark paragraphs with the four-space indent at all?"""
    lines = [line for line in text.split("\n") if line.strip()]
    if not lines:
        return True, 0.0
    share = sum(1 for line in lines if line.startswith(INDENT)) / len(lines)
    return share >= INDENT_MIN_SHARE, share


def group_paragraphs_by_blank_line(
    text: str, strip_page_markers: bool = True, collapse_spaces: bool = True
) -> list[str]:
    """Split on blank lines instead of the indent. Used only where the indent is absent.

    Recovers both structure and attribution on the affected packages. On
    CHRG-109hhrg30382 it takes 4 paragraphs to 614 and 0 recognised speakers to
    104; on CHRG-109hhrg30793, 48 to 334 and 0 to 46. Where a document has no
    dialogue at all the speaker count stays at zero, but the paragraphs are still
    recovered, which is the point: a summarizer can work with paragraphs.

    Checked against 150 hearings drawn at random: 149 carry the indent so this
    never runs on them, and on the one that did not it was strictly better.
    Nothing was made worse.
    """
    paragraphs: list[str] = []
    current: list[str] = []

    for line in text.split("\n"):
        if strip_page_markers:
            line = PAGE_MARKER.sub("", line)
        stripped = line.strip()
        if stripped:
            current.append(stripped)
        elif current:
            paragraphs.append(" ".join(current))
            current = []

    if current:
        paragraphs.append(" ".join(current))

    if collapse_spaces:
        return [re.sub(r"\s+", " ", p).strip() for p in paragraphs if p.strip()]
    return [re.sub(r"^\s+", "", p) for p in paragraphs if p.strip()]


def group_paragraphs(
    text: str, strip_page_markers: bool = True, collapse_spaces: bool = True
) -> list[str]:
    """Split hearing text into paragraphs on the four-space indent convention.

    Empty lines are dropped, lines inside a paragraph are joined with a single
    space, and leading whitespace is stripped from the result.

    The indent rule is the inherited one and it holds: over 400,608 non-blank
    lines sampled across six years, 17.1 percent sit at exactly four spaces and
    93.6 percent of lines that open a speaking turn are among them. The 6
    percent of turn-looking lines at column zero are almost entirely false
    positives — mid-sentence continuations such as "Congress. We have to find a
    middle ground." — 1,785 of them against 20 genuine turns.

    Note that `startswith(INDENT)` is true of any indent of four or more, so
    deeper indents (block quotes at eight, centered headings at twenty or more)
    also break a paragraph, while one to three spaces continue it. That is the
    inherited behaviour and it is correct for this text: everything indented
    further than a paragraph is a separate block.

    Parameters
    ----------
    text : str
        Output of `extract_text`.
    strip_page_markers : bool
        Remove `[[Page N]]` stamps, which GPO writes at column zero and which
        therefore land inside the surrounding paragraph. Changes 0.52 percent of
        paragraphs and no paragraph boundaries.
    collapse_spaces : bool
        Collapse runs of whitespace inside a paragraph to one space. Needed
        because removing a mid-line page marker leaves a gap, and useful because
        GPO's fixed-width layout puts column padding inside the roster and
        contents lines. Changes 4.27 percent of paragraphs, all of them front
        matter — committee rosters, tables of contents, title pages — and no
        paragraph boundaries.

    Both default to on. Setting both to False reproduces the earlier pipeline's
    output exactly, which is what the notebook uses to report the difference.

    Returns
    -------
    list of str
        Paragraphs in document order, including front matter.
    """
    # Where the convention is absent the indent rule cannot work at all, so fall
    # back rather than return a document in four paragraphs. See INDENT_MIN_SHARE.
    if not _uses_indent_convention(text)[0]:
        return group_paragraphs_by_blank_line(text, strip_page_markers, collapse_spaces)

    paragraphs: list[str] = []
    current: list[str] = []

    for line in text.split("\n"):
        if strip_page_markers:
            line = PAGE_MARKER.sub("", line)
        stripped = line.strip()
        if not stripped:
            continue
        if line.startswith(INDENT) and current:
            paragraphs.append(" ".join(current))
            current = []
        current.append(stripped)

    if current:
        paragraphs.append(" ".join(current))

    if collapse_spaces:
        return [re.sub(r"\s+", " ", p).strip() for p in paragraphs]
    return [re.sub(r"^\s+", "", p) for p in paragraphs]


#: A cover page runs to a couple of thousand bytes; a hearing with any real
#: proceedings in it runs to a hundred thousand or more. The 25th percentile of
#: HTML size across the corpus is 104 KB and the 5th is 1.5 KB, so anything
#: under this is on the cover-page side of a gap, not near a boundary.
COVER_PAGE_MAX_BYTES = 20_000


def has_usable_text(path: str | Path) -> dict[str, Any]:
    """Does this HTML rendition contain a hearing, or only its cover page?

    Three different things produce a file with no proceedings in it, and only
    one of them announces itself:

    * **The marker.** GovInfo writes `<TEXT NOT AVAILABLE>` where the body would
      be. Measured on the downloaded corpus this catches 334 files — about a
      third of the cases.
    * **Silent truncation.** The rendition simply stops after the front matter,
      with no marker at all: 780 files under 2 KB and 1,127 under 20 KB. This is
      why the earlier pipeline used a hand-tuned `char_count > 8650` threshold
      instead of the marker — the marker alone misses most of them.
    * **Written-submission volumes.** Large files with real text but no spoken
      dialogue, typically appropriations "nondepartmental witnesses" volumes
      that print statements submitted for the record. These have text and must
      **not** be treated as missing.

    The test is therefore two-part: the marker, or *both* cover-page size and no
    spoken turn. Requiring both keeps the third category out — a 1.5 MB volume
    of written testimony has no turns but is not a cover page.

    Returns
    -------
    dict
        ``exists``, ``bytes``, ``n_turns``, ``has_marker``, and ``has_text``.
    """
    path = Path(path)
    if not path.exists():
        return {"exists": False, "bytes": 0, "n_turns": 0,
                "has_marker": False, "has_text": False}

    raw = path.read_bytes()
    size = len(raw)
    has_marker = NO_TEXT_MARKER in raw

    if has_marker:
        return {"exists": True, "bytes": size, "n_turns": 0,
                "has_marker": True, "has_text": False}

    if size > COVER_PAGE_MAX_BYTES:
        # Too big to be a cover page. Turn counting is the expensive part and
        # nothing above this size is classified on it, so skip it.
        return {"exists": True, "bytes": size, "n_turns": -1,
                "has_marker": False, "has_text": True}

    paragraphs = group_paragraphs(extract_text(raw))
    n_turns = sum(1 for p in paragraphs if TURN_OPENING.match(p))
    return {"exists": True, "bytes": size, "n_turns": n_turns,
            "has_marker": False, "has_text": n_turns > 0}


def label_sections(paragraphs: list[str]) -> list[str]:
    """Mark each paragraph ``"spoken"`` or ``"qfr"``.

    Questions for the record are **embedded blocks, not a document tail.** That
    was worth measuring rather than assuming: of 26 transcripts carrying a QFR
    marker, spoken dialogue resumes after the first marker in 20 of them, and
    one appropriations hearing carries 22 separate blocks interleaved through
    the proceedings. Treating everything after the first marker as appendix —
    the obvious first guess — would have discarded most of the hearing.

    A block therefore opens at a `QFR_OPENING` marker and closes at the next
    paragraph that opens a spoken turn. Measured block spans run from 3 to 77
    paragraphs. The closing rule is what makes this safe: the worst case for a
    marker the pattern does not recognize is that its block stays labelled
    spoken, and the worst case for a false marker is that one speaker turn's
    worth of text is labelled qfr — neither loses a paragraph, because nothing
    is dropped here.

    Parameters
    ----------
    paragraphs : list of str
        Output of `group_paragraphs`, in document order.

    Returns
    -------
    list of str
        One label per paragraph, same length and order as the input.
    """
    labels: list[str] = []
    in_block = False
    for paragraph in paragraphs:
        if QFR_OPENING.match(paragraph):
            in_block = True
        elif in_block and TURN_OPENING.match(paragraph):
            in_block = False
        labels.append("qfr" if in_block else "spoken")
    return labels


def parse_transcript(path: str | Path) -> dict[str, Any]:
    """One HTML rendition to its paragraphs plus the counts describing them.

    Parameters
    ----------
    path : str or Path
        A `.htm` file written by `02_download_hearings.ipynb`.

    Returns
    -------
    dict
        ``paragraphs`` and ``sections`` — parallel lists — plus the counts that
        describe them: ``n_paragraphs``, ``n_chars``, ``n_front_matter``
        (paragraphs carrying a dot leader), ``n_page_markers`` (`[[Page N]]`
        stamps removed), ``n_qfr_blocks``, ``n_qfr_paragraphs``, and
        ``n_spoken_chars``.

        Spoken and written material are separated but both are returned. Which
        one a stage wants is that stage's decision: summarizing what was said at
        a hearing wants the spoken text, and what a member asked the agency in
        writing is still evidence of what that member cared about. Cutting here
        would take that choice away from every stage downstream.
    """
    path = Path(path)
    text = extract_text(path.read_bytes())
    indented, indent_share = _uses_indent_convention(text)
    paragraphs = group_paragraphs(text)
    sections = label_sections(paragraphs)

    n_blocks = sum(
        1
        for i, label in enumerate(sections)
        if label == "qfr" and (i == 0 or sections[i - 1] == "spoken")
    )
    return {
        "paragraphs": paragraphs,
        "sections": sections,
        # Which rule produced these paragraphs, so a reader can tell without
        # re-deriving it. "blank_line" means the four-space convention was absent.
        "paragraph_rule": "indent" if indented else "blank_line",
        "indent_share": indent_share,
        "n_paragraphs": len(paragraphs),
        "n_chars": sum(len(p) for p in paragraphs),
        "n_front_matter": sum(1 for p in paragraphs if DOT_LEADER.search(p)),
        "n_page_markers": len(PAGE_MARKER.findall(text)),
        "n_qfr_blocks": n_blocks,
        "n_qfr_paragraphs": sections.count("qfr"),
        "n_spoken_chars": sum(
            len(p) for p, s in zip(paragraphs, sections) if s == "spoken"
        ),
    }
