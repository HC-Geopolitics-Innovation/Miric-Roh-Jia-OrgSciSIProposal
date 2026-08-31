"""Parse a GovInfo MODS record into one flat row per hearing package.

MODS is the only place the corpus states who a hearing belonged to and who spoke
at it, and both matter downstream: the committee is how the demonstration subset
is selected, and the list of members is what the topic-extraction stage matches
surnames against to attribute statements. A hearing whose MODS carries no
`congMember` produces no attributable statements and drops out of that stage
silently — which is why `n_members` is carried on every row rather than left
implicit.

Shape of the document, which is not obvious from the schema name:

    <mods>
      <titleInfo><title>…                     the hearing title
      <originInfo><dateIssued>…               publication date
      <extension>                             three of these, flat siblings
        <collectionCode>CHRG</…               (1) provenance
      <extension>
        <docClass>SHRG</…  <chamber>…         (2) package identity
        <congress>105</…   <session>2</…
        <heldDate>…  repeated, one per sitting day
      <extension>
        <granuleClass>…                       (3) content description
        <congCommittee authorityId=…>         committee, sometimes more than one
        <congMember bioGuideId=… role=…>      repeated, one per member
        <witness>Ashe, Dan, Assistant Dir…</…> repeated, free text
        <isNomination>false</…

The three `<extension>` blocks are siblings, not nested, and which one holds a
given field is a fact about GovInfo rather than about MODS. Everything here is
therefore read by searching the whole tree for the element rather than by
walking a fixed path, which also survives the packages that carry only two of
the three blocks.

Called from `scripts/python/01_dataset_construction/03_parse_mods.ipynb`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from lxml import etree

NS = {"m": "http://www.loc.gov/mods/v3"}

#: A hearing whose HTML rendition carries this marker was never digitized past
#: its cover page. GovInfo says so in the file, so the pipeline reads the marker
#: instead of guessing from a length threshold — the earlier pipeline dropped
#: these with a hand-tuned `char_count > 8650` rule whose provenance was a
#: comment saying the number had been checked by eye.
NO_TEXT_MARKER = b"<TEXT NOT AVAILABLE>"

#: Cover-page-only renditions are small. Reading the first chunk of a 6 MB
#: transcript to look for a marker that only appears in 2 KB stubs is wasteful,
#: so the marker check is gated on size.
STUB_MAX_BYTES = 20_000


def _text(el: etree._Element | None) -> str | None:
    """Stripped text of an element, or None. Empty strings become None."""
    if el is None or el.text is None:
        return None
    value = el.text.strip()
    return value or None


def _find_text(root: etree._Element, path: str) -> str | None:
    return _text(root.find(path, NS))


def _named(el: etree._Element, name_type: str) -> str | None:
    """The `<name type="...">` child of a congCommittee or congMember."""
    return _text(el.find(f'm:name[@type="{name_type}"]', NS))


def parse_committees(root: etree._Element) -> list[dict[str, Any]]:
    """Every `<congCommittee>` in the record, in document order.

    Most hearings have one. Joint hearings and packages that reprint a second
    committee's proceedings have more, so this returns all of them and leaves
    the choice of a primary to the caller. The collector this replaces took
    `.//congCommittee` — the first match anywhere — without recording that a
    choice had been made, so a joint hearing silently became a hearing of
    whichever committee happened to be listed first.
    """
    out = []
    for el in root.iterfind(".//m:congCommittee", NS):
        out.append(
            {
                "authorityId": el.get("authorityId"),
                "chamber": el.get("chamber"),
                "congress": el.get("congress"),
                "type": el.get("type"),
                "name_standard": _named(el, "authority-standard"),
                "name_short": _named(el, "authority-short"),
            }
        )
    return out


def parse_members(root: etree._Element) -> list[dict[str, Any]]:
    """Every `<congMember>` in the record.

    `bioGuideId` is the stable identifier and the key the topic-extraction stage
    joins on, but it is not always present — GovInfo omits it for some members,
    typically ones who left office around the time the package was catalogued.
    Those members are kept with a null id rather than dropped, so the count of
    unattributable speakers is visible in the data instead of being absorbed
    into a smaller list.
    """
    out = []
    for el in root.iterfind(".//m:congMember", NS):
        out.append(
            {
                "bioGuideId": el.get("bioGuideId"),
                "chamber": el.get("chamber"),
                "congress": el.get("congress"),
                "party": el.get("party"),
                "state": el.get("state"),
                "role": el.get("role"),
                "name_parsed": _named(el, "parsed"),
                "name_lnf": _named(el, "authority-lnf"),
                "name_fnf": _named(el, "authority-fnf"),
                "name_other": _named(el, "authority-other"),
            }
        )
    return out


def parse_witnesses(root: etree._Element) -> list[str]:
    """Witness lines, verbatim.

    `<witness>` is free text in "Surname, Given name, Title, Organization,
    Location" order with no internal markup, so it is stored as written. Parsing
    it into fields would be a guess, and the downstream stages only need the
    surnames — which they take from this string themselves, at the point where
    the rule for doing so can be stated and checked.
    """
    return [t for t in (_text(el) for el in root.iterfind(".//m:witness", NS)) if t]


def parse_mods(path: str | Path) -> dict[str, Any]:
    """One MODS file to one row.

    Parameters
    ----------
    path : str or Path
        A `.xml` MODS record written by `02_download_hearings.ipynb`.

    Returns
    -------
    dict
        Package identity, dates, committees, members, witnesses, and the counts
        derived from them. List-valued fields stay lists; the notebook explodes
        them into their own tables where a relational shape is wanted.
    """
    path = Path(path)
    root = etree.parse(str(path)).getroot()

    committees = parse_committees(root)
    members = parse_members(root)
    witnesses = parse_witnesses(root)

    held = [t for t in (_text(el) for el in root.iterfind(".//m:heldDate", NS)) if t]

    record: dict[str, Any] = {
        "packageId": _find_text(root, './/m:recordInfo/m:recordIdentifier')
        or _find_text(root, ".//m:accessId")
        or path.stem,
        "title": _find_text(root, "m:titleInfo/m:title"),
        "dateIssued": _find_text(root, "m:originInfo/m:dateIssued"),
        "docClass": _find_text(root, ".//m:docClass"),
        "chamber": _find_text(root, ".//m:chamber"),
        "congress": _find_text(root, ".//m:congress"),
        "session": _find_text(root, ".//m:session"),
        "number": _find_text(root, ".//m:number"),
        "granuleClass": _find_text(root, ".//m:granuleClass"),
        "preferredCitation": _find_text(root, ".//m:preferredCitation"),
        "sudoc": _find_text(root, 'm:classification[@authority="sudocs"]'),
        "branch": _find_text(root, ".//m:branch"),
        "dateIngested": _find_text(root, ".//m:dateIngested"),
        "isNomination": _find_text(root, ".//m:isNomination"),
        "isErrata": _find_text(root, ".//m:isErrata"),
        "heldDates": held,
        "heldDate_first": held[0] if held else None,
        "committees": committees,
        "members": members,
        "witnesses": witnesses,
    }

    # Derived, so that a downstream filter never has to re-walk the nested
    # columns to answer "can this hearing be used".
    primary = committees[0] if committees else {}
    record.update(
        {
            "committee_name": primary.get("name_standard"),
            "committee_id": primary.get("authorityId"),
            "n_committees": len(committees),
            "n_members": len(members),
            "n_members_with_bioguide": sum(1 for m in members if m["bioGuideId"]),
            "n_witnesses": len(witnesses),
            "n_held_dates": len(held),
        }
    )
    return record


def transcript_status(path: str | Path) -> dict[str, Any]:
    """Whether an HTML rendition actually contains a transcript.

    A download can succeed and still yield nothing usable: GovInfo serves a
    cover page carrying `<TEXT NOT AVAILABLE>` for hearings it never digitized
    past the front matter. Those are roughly 45 percent of 1995-96 and a few
    percent of later years, so the distinction has to be recorded rather than
    inferred from file size alone.

    Returns
    -------
    dict
        ``bytes``, ``has_text``, and ``exists``. A missing file is reported
        rather than raised: `02` already recorded why it is missing, and this
        function's job is to describe what is on disk.
    """
    path = Path(path)
    if not path.exists():
        return {"exists": False, "bytes": 0, "has_text": False}

    size = path.stat().st_size
    if size > STUB_MAX_BYTES:
        return {"exists": True, "bytes": size, "has_text": True}

    return {
        "exists": True,
        "bytes": size,
        "has_text": NO_TEXT_MARKER not in path.read_bytes(),
    }
