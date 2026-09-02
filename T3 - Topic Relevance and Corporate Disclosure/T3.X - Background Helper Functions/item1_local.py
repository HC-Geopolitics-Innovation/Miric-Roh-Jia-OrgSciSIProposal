"""A local Item 1 (Business) extractor, used where the sec-api Extractor returns nothing.

**Why this exists.** The Extractor returns an empty string for Item 1 on 432 of
the 22,299 S&P 500 annual reports — 1.94 percent. Item 1 is mandatory in a 10-K,
so an empty result is a failure by definition, and the text is present in the
filing: FactSet, Marathon Oil, Iron Mountain and E*TRADE all have full Business
sections the API declines to return. The failure is deterministic, not
transient — four URL shapes (as-shipped, `linkToTxt`, `linkToFilingDetails`, a
rebuilt accession directory) and both output modes (`text`, `html`) were tried on
eleven of them, and all twenty-two attempts returned zero characters. The text
therefore has to come from the archived document instead.

**What it does.** Picks the primary document out of an SGML submission, converts
markup to text, finds every `Item N` marker, discards the ones that are
table-of-contents rows or inline cross-references, chooses the Item 1 heading,
and cuts at the next real item heading — `Item 1A`, or `Item 2`/`Item 3` for
filings that predate Item 1A or combine items ("Items 1. and 2. Business and
Properties").

**Measured against the API on 5,314 filings where the API succeeded:** median
token Jaccard 0.9976, agreement at or above 0.95 for 95.6 percent, median length
ratio 1.003, disagreement below 0.5 for 1.3 percent. Agreement is stable across
eras, with medians of 0.997 to 1.000 from pre-1997 through 2023+.

**The known failure mode is overrun, and it is why the caller needs a guard.** Of
83 cases where this extractor returned more than 1.5x the API's length, 64 were
this extractor running past the end of Item 1, 13 were the API returning the
wrong section, and 6 were unclear. Disagreement therefore does not automatically
mean the API was right — but at roughly 1.2 percent of filings this module does
swallow the following section, so `10_assemble_sp500_item1.ipynb` re-truncates at
a line-initial item heading rather than trusting the boundary found here.

Not a general-purpose 10-K splitter: it finds one item, and its accuracy is
established only for Item 1.

Returns a dict::

    {"status": "ok" | "incorporated_by_reference" | "not_found" | "no_document",
     "text": str, "chars": int, "start_heading": str, "end_heading": str,
     "combined_items": str, "n_candidates": int, "note": str}
"""

from __future__ import annotations

import argparse
import html as _html
import os
import re
import zipfile

from paths import SEC_BULK

ARCHIVE_ROOT = str(SEC_BULK)
INDEX_PARQUET = "/scratch2/acroh/projects/llm_method/data/raw/sec/filings.parquet"

# --------------------------------------------------------------------------
# 1. Getting the primary document out of the archived submission
# --------------------------------------------------------------------------

_DOC_RE = re.compile(r"(?is)<DOCUMENT>(.*?)(?:</DOCUMENT>|\Z)")
_TYPE_RE = re.compile(r"(?i)<TYPE>\s*([^\s<]+)")
_TEXT_RE = re.compile(r"(?is)<TEXT>(.*?)(?:</TEXT>|\Z)")


def decode_bytes(b: bytes) -> str:
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("latin-1", "replace")


def select_primary_document(raw: str) -> str:
    """Old .txt archives hold the whole SGML submission (10-K + every exhibit).
    Return the <TEXT> body of the first <DOCUMENT> whose <TYPE> starts 10-K.
    HTML files from later years are returned unchanged."""
    if "<DOCUMENT>" not in raw[:400000]:
        return raw
    best = None
    for d in _DOC_RE.finditer(raw):
        body = d.group(1)
        m = _TYPE_RE.search(body[:2000])
        t = (m.group(1) if m else "").upper()
        if t.startswith("10-K") or t.startswith("10K"):
            tm = _TEXT_RE.search(body)
            return tm.group(1) if tm else body
        if best is None:
            tm = _TEXT_RE.search(body)
            best = tm.group(1) if tm else body
    return best if best is not None else raw


# --------------------------------------------------------------------------
# 2. Markup -> plain text, preserving line structure
# --------------------------------------------------------------------------

_RE_COMMENT = re.compile(r"(?is)<!--.*?-->")
_RE_SCRIPT = re.compile(r"(?is)<(script|style)\b[^>]*>.*?</\1\s*>")
_RE_IXHIDE = re.compile(r"(?is)<(ix:header|ix:hidden)\b[^>]*>.*?</\1\s*>")
_RE_XMLDECL = re.compile(r"(?is)<\?xml.*?\?>")
# block-ish elements -> newline
_RE_BLOCK = re.compile(
    r"(?is)<\s*/?\s*(br|p|div|tr|table|thead|tbody|h[1-6]|li|ul|ol|center|hr|"
    r"caption|blockquote|dt|dd|article|section|body)\b[^>]*>"
)
# table cells -> tab (keeps 'Item 1.' and 'Business' and a page number on one line)
_RE_CELL = re.compile(r"(?is)<\s*/?\s*(td|th)\b[^>]*>")
_RE_TAG = re.compile(r"(?s)<[^>\n]{0,2000}>")
_RE_PAGE = re.compile(r"(?i)<PAGE[^>]*>")
_RE_UNISPACE = re.compile("[\u00a0\u1680\u2000-\u200a\u202f\u205f\u3000]")
_RE_ZEROWIDTH = re.compile("[\u200b\u200c\u200d\u2060\ufeff\u00ad]")


_RE_HTMLISH = re.compile(r"(?i)<\s*(!doctype\s+html|html\b|body\b|/?div\b|/?font\b|/?span\b|/?td\b|br\s*/?>)")
_RE_CLOSERS = re.compile(r"(?i)</\s*(td|tr|div|font|span|p)\s*>")


def is_html(doc: str) -> bool:
    """Old EDGAR .txt bodies are fixed-width ASCII where newlines carry meaning.
    HTML bodies wrap source lines arbitrarily, so their newlines must be killed
    BEFORE tag-derived line breaks are inserted -- otherwise 'ITEM\n1. BUSINESS'
    never matches a line-anchored heading regex."""
    if _RE_HTMLISH.search(doc[:300000]):
        return True
    return len(_RE_CLOSERS.findall(doc[:500000])) >= 5


def markup_to_text(s: str) -> str:
    if is_html(s):
        s = s.replace("\r", " ").replace("\n", " ")
    s = _RE_XMLDECL.sub(" ", s)
    s = _RE_COMMENT.sub(" ", s)
    s = _RE_SCRIPT.sub(" ", s)
    s = _RE_IXHIDE.sub(" ", s)
    s = _RE_PAGE.sub("\n", s)
    s = _RE_BLOCK.sub("\n", s)
    s = _RE_CELL.sub("\t", s)
    s = _RE_TAG.sub("", s)
    s = _html.unescape(s)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    # Filers separate "Item" from "1" with thin/hair/figure spaces far more often
    # than you would guess; a plain [ \t] heading regex silently misses those.
    s = _RE_UNISPACE.sub(" ", s)
    s = _RE_ZEROWIDTH.sub("", s)
    s = s.replace("\u2028", "\n").replace("\u2029", "\n")
    # collapse horizontal whitespace, drop trailing spaces
    s = re.sub(r"[ \t\f\v]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# --------------------------------------------------------------------------
# 3. Item-heading markers
# --------------------------------------------------------------------------

# "Item 1.", "ITEM 1:", "Item 1 -", "Items 1 and 2.", "ITEM 1. AND 2.",
# "Item 1 & 2", optionally preceded by "PART I".
_ITEM_RE = re.compile(
    r"""(?imx)
    ^[ \t]*
    (?:PART\s+[IVX]+[ \t]*[.,:\-]?[ \t]*)?
    I[ \t]?T[ \t]?E[ \t]?M[ \t]?S?
    [ \t]*[\.\:\-‐-―]?[ \t]*
    (\d{1,2})[ \t]*([A-Ca-c])?
    (?![\w])
    (?:
        [ \t]*[\.\:\-‐-―]?[ \t]*
        (?:AND|&|,|THROUGH|TO)
        [ \t]*(?:ITEMS?[ \t]*)?
        (\d{1,2})[ \t]*([A-Ca-c])?
        (?![\w])
    )?
    """
)

_ITEM_TITLES = (
    "business", "properties", "propertie", "legal proceedings", "risk factors",
    "unresolved staff comments", "mine safety disclosures",
    "submission of matters to a vote of security holders",
)
# "1. Business." / "1A. Risk Factors" used as headings with the word ITEM omitted
# (J.C. Penney files this way).  Anchored to end of line so that financial
# statement note titles such as "1. Business and Summary of Significant
# Accounting Policies" cannot match.
_BARE_ITEM_RE = re.compile(
    r"(?im)^[ \t]*(\d{1,2})[ \t]*([A-Ca-c])?[\.\:][ \t]*("
    + "|".join(t.replace(" ", r"\s+") for t in _ITEM_TITLES)
    + r")s?[ \t]*\.?[ \t]*$")

_RANK = {}
for _n in range(0, 20):
    _RANK[(str(_n), "")] = _n * 10
    for _i, _s in enumerate("abc", start=1):
        _RANK[(str(_n), _s)] = _n * 10 + _i


def _rank(num: str, suf: str) -> int:
    return _RANK.get((num, (suf or "").lower()), int(num) * 10)


TITLE_WORDS = (
    "business", "propert", "risk factor", "unresolved", "legal proceeding",
    "mine safety", "submission of matters", "market for", "selected financial",
    "management's discussion", "quantitative and qualitative", "financial statements",
    "changes in and disagreements", "controls and procedures", "description of business",
    "general", "executive officers",
)


class Marker:
    __slots__ = ("pos", "line_start", "line_end", "line", "num", "suf",
                 "num2", "suf2", "rank_lo", "rank_hi", "text")

    def __repr__(self):
        return f"<Marker {self.text!r} @{self.pos}>"


def _mk(text, pos, num, suf, matched):
    mk = Marker()
    ls = text.rfind("\n", 0, pos) + 1
    le = text.find("\n", pos)
    le = len(text) if le < 0 else le
    mk.pos, mk.line_start, mk.line_end = pos, ls, le
    mk.line = text[ls:le]
    mk.num, mk.suf, mk.num2, mk.suf2 = num, suf, None, ""
    mk.rank_lo = mk.rank_hi = _rank(num, suf)
    mk.text = matched.strip()
    return mk


def augment_lenient(text: str, markers: list) -> list:
    """Filers really do type 'Item l. Business' (lower-case L) and 'ITEM I.
    BUSINESS' (roman numeral).  Add those as extra Item-1 candidates when the
    strict digit regex did not already fire on that line."""
    have = {m.line_start for m in markers}
    extra = []
    for m in _ITEM1_LENIENT.finditer(text):
        ls = text.rfind("\n", 0, m.start()) + 1
        if ls in have:
            continue
        extra.append(_mk(text, m.start(), "1", "", m.group(0)))
        have.add(ls)
    for m in _BARE_ITEM_RE.finditer(text):
        ls = text.rfind("\n", 0, m.start()) + 1
        if ls in have:
            continue
        extra.append(_mk(text, m.start(), m.group(1), (m.group(2) or ""), m.group(0)))
        have.add(ls)
    if not extra:
        return markers
    return sorted(markers + extra, key=lambda x: x.pos)


def find_markers(text: str) -> list:
    out = []
    for m in _ITEM_RE.finditer(text):
        mk = Marker()
        mk.pos = m.start()
        ls = text.rfind("\n", 0, m.start()) + 1
        le = text.find("\n", m.start())
        le = len(text) if le < 0 else le
        mk.line_start, mk.line_end = ls, le
        mk.line = text[ls:le]
        mk.num, mk.suf = m.group(1), (m.group(2) or "")
        mk.num2, mk.suf2 = m.group(3), (m.group(4) or "")
        mk.rank_lo = _rank(mk.num, mk.suf)
        mk.rank_hi = _rank(mk.num2, mk.suf2) if mk.num2 else mk.rank_lo
        if mk.rank_hi < mk.rank_lo:          # "Item 5 to 1" nonsense
            mk.rank_hi = mk.rank_lo
        mk.text = m.group(0).strip()
        out.append(mk)
    return out


_SENTENCE_LEAD = re.compile(r"^[a-z]")


def _looks_like_heading(text: str, mk: Marker) -> bool:
    """Distinguish a real section heading from an in-sentence cross reference
    ('...described in Item 1A. Risk Factors of this report...').  A heading is:
    a short line, whose remainder after the item number is empty or begins with
    a capital / a known item title -- never a lower-case continuation."""
    line = mk.line.strip()
    if len(line) > 160:
        return False
    rest = text[mk.pos + len(mk.text): mk.line_end].strip(" \t.:;,-–—()\u2010\u2011\u2012\u2013\u2014")
    if rest == "":
        nxt = text[mk.line_end: mk.line_end + 120].strip()
        nxt = nxt.split("\n")[0].strip() if nxt else ""
        rest = nxt
        if rest == "":
            return True
    low = rest.lower()
    if any(low.startswith(w) for w in TITLE_WORDS):
        return len(line) <= 160
    if _SENTENCE_LEAD.match(rest):
        return False
    return len(rest) <= 70


def _toc_line(text: str, mk: Marker) -> bool:
    """Dot leaders, or a trailing page number, on the heading's own line."""
    line = mk.line
    if re.search(r"\.{4,}", line):
        return True
    if re.search(r"[\s\t]\d{1,3}\s*$", line) and len(line) <= 120:
        return True
    return False


# --------------------------------------------------------------------------
# 4. Selecting the real Item 1
# --------------------------------------------------------------------------

_REF_RE = re.compile(
    r"(?is)(incorporated\s+(?:herein\s+)?by\s+reference|"
    r"is\s+incorporated\s+herein|see\s+pages?\s+\d|"
    r"pages?\s+\d[\d\s,\-and]*of\s+(?:the\s+)?(?:registrant|company)?)"
)

_XREF_RE = re.compile(
    r"(?is)(cross[\s\-]?reference|incorporated\s+(?:herein\s+)?by\s+reference|"
    r"annual\s+report\s+to\s+(?:share|stock)holders)")

MIN_SECTION_CHARS = 1000

_ITEM1_LENIENT = re.compile(
    r"(?im)^[ \t]*(?:PART\s+[IVX]+[ \t]*[.,:\-]?[ \t]*)?ITEMS?[ \t]*[\.\:\-]?[ \t]*"
    r"(?:1|I|l)[ \t]*[\.\:\-]?[ \t]*(?:BUSINESS|DESCRIPTION OF (?:THE )?BUSINESS)")


def _toc_blocks(markers: list, text: str) -> list:
    """A table of contents is a dense, STRICTLY ASCENDING run of >=4 item
    markers separated by small gaps.  The ascending requirement matters: without
    it the run walks straight past the end of the TOC ('...Item 14 ... 35' then
    'PART I / ITEM 1. BUSINESS' a few characters later) and masks the real
    heading, which is exactly how a naive TOC filter loses the section."""
    blocks = []
    i = 0
    n = len(markers)
    while i < n:
        j = i
        seen = {markers[i].rank_lo}
        while (j + 1 < n
               and (markers[j + 1].pos - markers[j].line_end) < 400
               and markers[j + 1].rank_lo > markers[j].rank_lo):
            j += 1
            seen.add(markers[j].rank_lo)
        if len(seen) >= 4 and j > i:
            blocks.append((markers[i].line_start, markers[j].line_end))
        i = j + 1
    return blocks


def _section_for(text: str, markers: list, k: int, pos: int = None,
                 covered: int = None) -> tuple:
    """End of Item 1 = the next *adjacent* item heading.  Two passes: first only
    accept a near successor (1A/1B/1C/2 after Item 1; 3/4 after a combined
    'Items 1 and 2'), because ASCII line wrapping regularly puts an in-text
    cross reference such as 'Item 8. "Financial Statements..."' at the start of
    a line and it would otherwise truncate the section.  Only if no near
    successor exists do we accept any higher-numbered heading."""
    if pos is None:
        start = markers[k]
        covered = start.rank_hi
        pos = start.line_start
    body_start = pos
    for window in (20, 10000):
        for j in range(len(markers)):
            e = markers[j]
            if e.line_start <= body_start:
                continue
            if e.rank_lo <= covered or e.rank_lo > covered + window:
                continue
            if not _looks_like_heading(text, e):
                continue
            return body_start, e.line_start, e
    return body_start, len(text), None


def _row_title(text: str, mk) -> str:
    """Title that goes with an item marker: rest of its line, else the next
    non-empty line (HTML puts 'Item 1.' and 'Business' in sibling cells)."""
    rest = text[mk.pos + len(mk.text): mk.line_end].strip(" \t.:;,-\u2010-\u2015()")
    if not rest:
        nxt = text[mk.line_end: mk.line_end + 200].strip("\n")
        rest = nxt.split("\n")[0].strip() if nxt else ""
    rest = re.sub(r"[\s.]*\d[\d\s,\-\u2013]*$", "", rest).strip(" \t.:;,-")
    return rest


def _standalone_line(text: str, title: str, after: int):
    if not title or len(title) < 4 or len(title) > 60:
        return None
    rx = re.compile(r"(?im)^[ \t]*" + re.escape(title) + r"[ \t]*\.?[ \t]*$")
    m = rx.search(text, after)
    return m.start() if m else None


def _toc_title_fallback(text: str, markers: list, best: dict):
    """Integrated annual-report 10-Ks (Weyerhaeuser, Molina, Align, ...) carry
    the item numbers ONLY in a cross-reference table; the body headings are the
    bare titles ('OUR BUSINESS' ... 'RISK FACTORS').  When the only Item 1 we
    can find is such a table row, follow its title into the body instead."""
    mk, endmk = best["marker"], best["endmk"]
    t1 = _row_title(text, mk)
    if not t1 or "business" not in t1.lower():
        return None
    after = mk.line_end + 200
    s1 = _standalone_line(text, t1, after)
    while s1 is not None and endmk is not None and s1 < endmk.line_end:
        s1 = _standalone_line(text, t1, s1 + 1)
    if s1 is None:
        return None
    t2 = _row_title(text, endmk) if endmk is not None else ""
    e1 = _standalone_line(text, t2, s1 + 1000) if t2 else None
    if e1 is None:
        nxt = [m for m in markers
               if m.line_start > s1 + 1000 and m.rank_lo > mk.rank_hi
               and _looks_like_heading(text, m)]
        e1 = nxt[0].line_start if nxt else None
    if e1 is None:
        return None
    body = text[s1:e1].strip()
    if len(body) < MIN_SECTION_CHARS or len(body) > 0.6 * len(text):
        return None
    return {"start": s1, "end": e1, "body": body, "title": t1, "end_title": t2}


def choose_item1(text: str, markers: list) -> dict:
    cands = [k for k, m in enumerate(markers) if m.num == "1" and m.suf == ""]
    if not cands:
        return {"status": "not_found", "text": "", "n_candidates": 0,
                "note": "no 'Item 1' marker in document"}

    toc = _toc_blocks(markers, text)

    # Some archived "10-K" submissions actually hold a 10-Q document, whose
    # Item 1 is FINANCIAL STATEMENTS, not Business.  Never return that.
    def _is_10q_item1(mk):
        tail = text[mk.pos: mk.line_end + 40].lower()
        return "financial statements" in tail[:80] and "business" not in tail[:80]

    q_dropped = [k for k in cands if _is_10q_item1(markers[k])]
    cands = [k for k in cands if k not in set(q_dropped)]
    if not cands:
        return {"status": "not_found", "text": "", "n_candidates": 0,
                "note": "only 10-Q style 'Item 1. Financial Statements' headings "
                        "found - archived document is not a 10-K body"}

    scored = []
    for k in cands:
        mk = markers[k]
        s, e, endmk = _section_for(text, markers, k)
        body = text[s:e].strip()
        in_toc = any(a <= mk.pos <= b for a, b in toc) or _toc_line(text, mk)
        scored.append({
            "k": k, "start": s, "end": e, "body": body, "len": len(body),
            "in_toc": in_toc, "marker": mk, "endmk": endmk,
        })

    # TOC rows produce very short sections (bounded by the next TOC row), so the
    # longest section is essentially always the real one.  Among sections at
    # least half that long, take the EARLIEST -- later ones are cross references
    # from MD&A back into Item 1.  Pools are tried strictest first and we fall
    # back whenever the strict pool yields nothing of plausible length.
    pools = [
        [c for c in scored if not c["in_toc"] and _looks_like_heading(text, c["marker"])],
        [c for c in scored if not c["in_toc"]],
        [c for c in scored if _looks_like_heading(text, c["marker"])],
        scored,
    ]
    best = None
    for pool in pools:
        if not pool:
            continue
        lmax = max(c["len"] for c in pool)
        cand = min([c for c in pool if c["len"] >= 0.5 * lmax],
                   key=lambda c: c["marker"].pos)
        if best is None or cand["len"] > best["len"]:
            if best is None or best["len"] < MIN_SECTION_CHARS:
                best = cand
        if best["len"] >= MIN_SECTION_CHARS:
            break

    body = best["body"]
    note = ""
    status = "ok"
    if len(body) < MIN_SECTION_CHARS:
        alt = _toc_title_fallback(text, markers, best)
        if alt is not None:
            return {
                "status": "ok", "text": alt["body"], "n_candidates": len(cands),
                "start_heading": alt["title"][:120],
                "end_heading": (alt["end_title"] or "<next item heading>")[:120],
                "combined_items": "1",
                "note": "cross-reference-table 10-K: located section by its title, "
                        "not by an item number",
            }
        window = text[max(0, best["start"] - 1500): best["start"] + 2500]
        if _REF_RE.search(body[:2500]) or _XREF_RE.search(window):
            status = "incorporated_by_reference"
            note = ("short Item 1 that points elsewhere (cross-reference index / "
                    "incorporation by reference); %d chars" % len(body))
        else:
            status = "not_found"
            note = f"best candidate only {len(body)} chars"
    return {
        "status": status,
        "text": body,
        "n_candidates": len(cands),
        "start_heading": best["marker"].line.strip()[:120],
        "end_heading": (best["endmk"].line.strip()[:120] if best["endmk"] else "<end of document>"),
        "combined_items": (f"{best['marker'].num}{best['marker'].suf}"
                           + (f"-{best['marker'].num2}{best['marker'].suf2}"
                              if best["marker"].num2 else "")),
        "note": note,
    }


def extract_item1_from_text(raw: str) -> dict:
    doc = select_primary_document(raw)
    text = markup_to_text(doc)
    markers = augment_lenient(text, find_markers(text))
    res = choose_item1(text, markers)
    res["chars"] = len(res["text"])
    res["doc_chars"] = len(text)
    return res


# --------------------------------------------------------------------------
# 5. Archive access
# --------------------------------------------------------------------------

_ZIP_CACHE = {}


def _open_zip(container: str) -> zipfile.ZipFile:
    path = container if os.path.isabs(container) else os.path.join(ARCHIVE_ROOT, container)
    z = _ZIP_CACHE.get(path)
    if z is None:
        z = zipfile.ZipFile(path)
        _ZIP_CACHE[path] = z
        z._member_index = {}
        for n in z.namelist():
            parts = n.split("/")
            if len(parts) >= 2:
                z._member_index.setdefault(parts[-2], []).append(n)
    return z


def read_archived_document(accession_no: str, container: str) -> str:
    z = _open_zip(container)
    key = accession_no.replace("-", "")
    members = z._member_index.get(key, [])
    docs = [m for m in members if not m.endswith("metadata.json")]
    if not docs:
        return ""
    docs.sort(key=lambda m: (0 if m.lower().endswith((".htm", ".html")) else 1, len(m)))
    return decode_bytes(z.read(docs[0]))


_INDEX = None


def _index_lookup(accession_no: str) -> str:
    global _INDEX
    if _INDEX is None:
        import pandas as pd
        d = pd.read_parquet(INDEX_PARQUET, columns=["accessionNo", "container"])
        _INDEX = dict(zip(d.accessionNo, d.container))
    return _INDEX.get(accession_no, "")


def extract_item1(accession_no: str, container: str = None) -> dict:
    container = container or _index_lookup(accession_no)
    if not container:
        return {"status": "no_document", "text": "", "chars": 0,
                "note": "accession not in filing index"}
    raw = read_archived_document(accession_no, container)
    if not raw:
        return {"status": "no_document", "text": "", "chars": 0,
                "note": "no document member in archive"}
    res = extract_item1_from_text(raw)
    res["accessionNo"] = accession_no
    res["container"] = container
    return res


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accession", nargs="+")
    ap.add_argument("--container", default=None)
    ap.add_argument("--head", type=int, default=400)
    a = ap.parse_args()
    for acc in a.accession:
        r = extract_item1(acc, a.container)
        print("=" * 70)
        print(acc, r["status"], r.get("chars"), "|", r.get("start_heading"),
              "->", r.get("end_heading"), "|", r.get("note", ""))
        print(r["text"][:a.head])


if __name__ == "__main__":
    main()