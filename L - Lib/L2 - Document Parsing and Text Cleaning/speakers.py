"""Attribute hearing paragraphs to the member who is speaking.

GPO writes a change of speaker as an honorific, a surname, a period, and then
the speech, at the start of an indented paragraph:

    Mr. Fazio. Thank you, Mr. Chairman.
    Senator Stevens. Let me ask about the budget request.
    The Chairman. Our House Oversight Committee will be in order.
    Mr. Ehlers [continuing]. On the point you raised a moment ago.

Paragraphs that do not open that way continue the previous speaker's turn. That
is the whole convention, and it is stable across the corpus: measured over
116,833 paragraphs from 65 transcripts spanning 1995-2000, 26.6 percent open a
turn and 69.6 percent continue one.

Why this module replaces the inherited rule
-------------------------------------------
The earlier pipeline asked whether ``f"{surname}."`` appeared anywhere in the
first five words of a paragraph, and took the first roster member that matched.
That rule and the anchored one below agree on **99.85 percent** of paragraphs,
so the change is small — but the 0.15 percent where they differ is not random,
and every case falls the same way:

===========================  =====  ==========================================
disagreement                 count  what the inherited rule does
===========================  =====  ==========================================
``Mr. Walsh. Mr. Serrano.``    119  chair yields the floor; the rule attributes
                                    the turn to whichever of the two the roster
                                    lists first, which is not the speaker
``Yes, Mr. Baker.``             36  a continuation that names a member becomes
                                    a new turn by that member
``Mr. Lancaster. No, Mr.        14  the speaker is not on the roster, so the
Rogers.``                           rule reaches past them to a member who was
                                    merely mentioned
``Present: Representatives       4  a roll-call line becomes a speaking turn
Gutknecht and Peterson.``
===========================  =====  ==========================================

There were zero paragraphs the inherited rule declined and the anchored rule
claimed. The anchored rule is not a different method; it is the same convention
read at the position where GPO actually writes it.

The bracketed-aside form is the one genuine gap in both. ``[continuing]`` and
``[presiding]`` sit between the surname and its period, so a pattern that
requires the period immediately after the surname misses them — 265 turns in the
same sample, 0.23 percent of paragraphs. `TURN_OPENING` allows the aside.

What this module does not decide
--------------------------------
Half of all turn openings belong to someone who is not on the committee roster:
13,538 of 27,216 in the sample are witnesses, agency officials, and non-member
legislators — Speaker Gingrich, Secretary Babbitt, General McCaffrey.
`attribute` returns those with a null ``bioGuideId`` and the surname as written
rather than dropping them, because whether a stage wants member speech only is
that stage's decision, and it cannot make it from a list the paragraphs have
already been removed from.

Called from `scripts/python/01_dataset_construction/04_build_hearing_corpus.ipynb`.
"""

from __future__ import annotations

import re
from typing import Any, Iterable

#: Honorifics GPO writes with a trailing period. Measured shares of turn
#: openings in the sample: Mr. 69.4%, Ms. 7.6%, Dr. 3.3%, Mrs. 3.1%.
_ABBREV = r"(?:Mr|Mrs|Ms|Dr|Hon|Rev|Prof)"

#: Honorifics written as whole words. Senator alone is 8.5% of openings;
#: Secretary, General, Chief, and Admiral together are a further 6.4%, and they
#: are almost always witnesses rather than members.
_TITLE = (
    r"(?:Miss|Senator|Representative|Congressman|Congresswoman|Chairman|"
    r"Chairwoman|Chairperson|Secretary|General|Admiral|Chief|Governor|Judge|"
    r"Justice|Commissioner|Director|Colonel|Captain|Major|Lieutenant|Sergeant|"
    r"Professor|Ambassador|Mayor|Sheriff|Reverend|Rabbi|Delegate|Speaker|"
    r"President)"
)

#: One or two capitalized words. Two allows "Diaz-Balart" style compounds and
#: the occasional "Van Hollen"; more than two starts matching sentence text.
_SURNAME = r"[A-Z][A-Za-z'’\-]+(?:\s+[A-Z][A-Za-z'’\-]+)?"

#: A paragraph opens a turn when it *begins* with this. The optional bracketed
#: aside covers "[continuing]" and "[presiding]"; the optional period after an
#: abbreviation and the doubled period both appear as typesetting slips.
TURN_OPENING = re.compile(
    rf"^(?:"
    rf"(?P<chair>The\s+Chair(?:man|woman|person)?)"
    rf"|(?:{_ABBREV}\.?\s+(?P<abbrev_name>{_SURNAME}))"
    rf"|(?:(?P<title>{_TITLE})\s+(?P<title_name>{_SURNAME}))"
    rf")"
    rf"(?:\s*\[[^\]]*\])?"
    rf"\.{{1,2}}(?:\s|$)"
)

#: Dot leaders mark a table of contents or an index row rather than speech.
#: 3.9 percent of paragraphs carry one.
DOT_LEADER = re.compile(r"\.{3,}")

#: The chair is identified by office, not name, so there is no bioGuideId to
#: give. The earlier pipeline used this sentinel and it is kept so the two
#: outputs can be compared row for row.
CHAIR_ID = "0000000"


def surname_of(authority_lnf: str) -> str:
    """Surname from a MODS ``authority-lnf`` name ("Bennett, Robert F." -> "Bennett")."""
    return authority_lnf.split(",")[0].strip()


def opening_of(paragraph: str) -> tuple[str | None, str | None]:
    """The honorific and surname a paragraph opens with, if it opens a turn.

    Returns
    -------
    tuple
        ``(honorific, surname)``, or ``(None, None)`` when the paragraph
        continues the previous turn. For the chair the surname is ``None`` and
        the honorific is the matched "The Chairman" form.
    """
    match = TURN_OPENING.match(paragraph)
    if not match:
        return None, None
    if match.group("chair"):
        return match.group("chair"), None
    name = match.group("abbrev_name") or match.group("title_name")
    honorific = match.group("title") or paragraph.split(None, 1)[0]
    return honorific, name.split()[-1] if name else None


def attribute(
    paragraphs: Iterable[str],
    members: list[dict[str, Any]],
    drop_front_matter: bool = True,
) -> list[dict[str, Any]]:
    """Group paragraphs into speaking turns.

    Parameters
    ----------
    paragraphs : iterable of str
        Output of `transcript.group_paragraphs`, in document order.
    members : list of dict
        Roster from `mods.parse_members`. Only ``bioGuideId`` and one of
        ``name_lnf`` / ``lastname`` are read.
    drop_front_matter : bool
        Skip paragraphs containing a dot leader. These are tables of contents
        and index rows; leaving them in makes the first turn of a hearing a
        page-number list.

    Returns
    -------
    list of dict
        One entry per turn: ``bioGuideId`` (None for a speaker who is not on the
        roster, `CHAIR_ID` for the chair), ``surname``, ``honorific``,
        ``is_member``, and ``paragraphs``. Paragraphs before the first
        recognized opening are returned as a single leading turn with
        ``surname`` None, so nothing is silently discarded.
    """
    by_surname: dict[str, str] = {}
    for member in members:
        name = member.get("name_lnf") or member.get("lastname")
        if name and member.get("bioGuideId"):
            by_surname.setdefault(surname_of(name), member["bioGuideId"])

    turns: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for paragraph in paragraphs:
        if drop_front_matter and DOT_LEADER.search(paragraph):
            continue

        honorific, surname = opening_of(paragraph)
        if honorific is None:
            if current is None:
                # Front matter before anyone speaks. Kept as its own turn rather
                # than dropped, so a transcript whose openings all fail to match
                # is visibly empty of turns instead of quietly short.
                current = {
                    "bioGuideId": None,
                    "surname": None,
                    "honorific": None,
                    "is_member": False,
                    "paragraphs": [],
                }
            current["paragraphs"].append(paragraph)
            continue

        if current is not None:
            turns.append(current)
        bio = CHAIR_ID if surname is None else by_surname.get(surname)
        current = {
            "bioGuideId": bio,
            "surname": surname,
            "honorific": honorific,
            "is_member": bio is not None and bio != CHAIR_ID,
            "paragraphs": [paragraph],
        }

    if current is not None:
        turns.append(current)
    return turns


def attribute_inherited(
    paragraphs: Iterable[str], members: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """The earlier pipeline's rule, kept so the difference can be measured.

    Reproduces `4a_paragraph_labeling.py`: a paragraph opens a turn when
    ``f"{surname}."`` appears anywhere in its first five words, and roster order
    breaks ties. Not used to build the dataset — it exists so the notebook can
    report how many paragraphs the two rules assign differently instead of
    asserting that the change is small.
    """
    roster = [
        {"bioGuideId": m["bioGuideId"], "lastname": surname_of(m.get("name_lnf") or "")}
        for m in members
        if m.get("bioGuideId") and m.get("name_lnf")
    ]

    turns: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for paragraph in paragraphs:
        if DOT_LEADER.search(paragraph):
            continue
        first_five = " ".join(paragraph.split()[:5])

        hit: dict[str, Any] | None = None
        if first_five.startswith("The Chairman."):
            hit = {"bioGuideId": CHAIR_ID, "surname": "The Chairman"}
        else:
            for member in roster:
                if f"{member['lastname']}." in first_five:
                    hit = {"bioGuideId": member["bioGuideId"], "surname": member["lastname"]}
                    break

        if hit is None:
            if current is not None:
                current["paragraphs"].append(paragraph)
            continue

        if current is not None:
            turns.append(current)
        current = {**hit, "paragraphs": [paragraph]}

    if current is not None:
        turns.append(current)
    return turns
