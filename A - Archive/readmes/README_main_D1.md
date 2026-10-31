# 01 — Dataset construction

Collecting the corpus this project's method operates on, and the reference data
it is checked against. Nothing here runs a language model; that starts in the
next stage. What this stage produces is a corpus whose gaps are *measured*
rather than discovered later.

Run the notebooks in order. Each is resumable: state lives in status logs on
scratch, not in the notebook, so an interrupted run is re-entered by executing
the notebook again.

| Notebook | Does | Status |
|---|---|---|
| `01_enumerate_hearings` | Lists every CHRG package 1995–2025 from the GovInfo API | done — 36,378 packages, 53 requests |
| `02_download_hearings` | Fetches the MODS record and HTML transcript for each | done |
| `03_parse_mods` | MODS → one row per hearing: committee, members, witnesses, dates | written, not yet run |
| `04_collect_cspan` | C-SPAN abstracts, the summarization reference | done — 18,697 programs |

Two further notebooks were written, run, and set aside — PDF collection for the
scanned hearings, and the Congressional Record Daily Digest. Both are in
`../99_archived_scripts/`, which is gitignored, with the measurements that ruled
them out. The decisions below explain why.

`lib/` holds the logic; the notebooks orchestrate and report. Paths resolve
through `lib/paths.py`, so nothing carries a project root as a literal. Bulk data
goes to `/scratch2/$USER/projects/llm_method/data`, which is not backed up and is
reproducible from these notebooks plus the API keys.

## Credentials

`.env` in this directory, gitignored; `.env.example` lists the variables.

| Variable | For |
|---|---|
| `GOVINFO_API_KEY` | the hearing corpus (`01`, `02`, `02b`) |
| `GOVINFO_API_KEY_CREC` | the Congressional Record (`07`) — a second key so the two collections do not spend each other's rate limit |
| `CSPAN_API_KEY` | the C-SPAN Archives API (`06`), from api@c-spanarchives.org |

The collector this replaces carried four GovInfo keys as string literals in
tracked source. No key appears in code here, and `lib/govinfo.py` sends it as a
header rather than a query parameter so it cannot reach an exception message and
from there a committed notebook.

## Decisions

**OCR is not part of the pipeline.** 12 percent of downloaded transcripts hold
only a cover page — 99 percent of 1995 and 1996, 3 to 10 percent from 2003 —
because GovInfo never digitized them. `baidu/Unlimited-OCR` was tested on an A40
against a real scanned hearing and rejected on two measurements: **23 seconds per
page** (100 GPU-days for the corpus) and **20 percent of surnames misread** —
`BUYER` as `BUTYER`, `STEARNS` as `STEAMANS`, `GIBBONS` as `GIBSON`. Speaker
attribution and topic extraction both key on surnames, so that error rate breaks
the pipeline's central operation.

With OCR ruled out the PDFs have no consumer, so `02b` was stopped too, at 495
files. The notebook and its status log are kept: if a usable OCR model appears,
re-running it resumes rather than restarts.

**Analysis runs from 2000 onward.** Collection covers 1995–2025 in full and the
earlier years are kept, but they are dropped at analysis time because GovInfo has
no text for them. That is a coverage fact, not a collection failure — the same
packages are absent from an independent November 2024 re-pull.

**C-SPAN abstracts are the only summarization reference.** The Congressional
Record Daily Digest was collected as a candidate second reference and does not
work as one: strip the committee clause, the action verb and the witness list
from a Digest entry and what remains is **14 to 19 words in every year from 1994
to 2026**, mostly the title restated. It is procedural record, not summary.

Recent entries are the thinnest, not the richest — the House has settled on
`held a hearing entitled "<exact title>". Testimony was heard from public
witnesses.`, which names no witness and adds nothing to the title. Collection
was stopped at 4,696 issues and nothing downstream reads it. The data on disk is
left in place, and the notebook resumes rather than restarts if the structured
date/committee/witness fields ever turn out to be worth having for matching.

Even C-SPAN is a limited reference: median 51 words against 388 for a generated
summary, and it describes *what a hearing was about* rather than *what was said*.
It supports a discriminant test — does a summary sit closest to its own hearing's
abstract — and not n-gram overlap scoring. Any number computed from it carries
that caveat.

**The C-SPAN per-program detail call is off.** It adds `publicId`, `eventid`,
`videoDuration` and `time` for one request per program. `publicId` was supposed
to be needed to reconcile against an earlier collection and is not — that
collection also carries `videoId`, which is the search's `id`, and 4,708 of a
5,130 sample join on it. `eventid` was supposed to group the parts of a
multi-day hearing and does not: of 60 multi-part groups, 21 share an id and 39
do not. Turn it back on with `FETCH_DETAIL = True` if re-air detection is ever
wanted, which is the one thing the field is good for.

**Prompts are fixed; infrastructure is not.** The map-reduce summarization,
topic-extraction and topic-relevance prompts are the method this repository
documents and are carried over unchanged. Library versions, paths, error
handling and storage format are implementation and were all rewritten.

**Parquet, not pickle.** The earlier pipeline stored intermediates as pickle. A
cluster filesystem failure zeroed 512 KiB blocks inside 76 of 2,088 files, and a
pickle with a hole in it is unreadable end to end.

## What the collection cost, and what it found

The earlier collector lost about 10 percent of the corpus without reporting it,
through three defects this one inverts:

| Earlier | Here |
|---|---|
| a network error inside the pagination loop `break`s, returning a partial list as complete — 18 times | retried, then **raised**; a partial list is never returned |
| `offset` paging with no sort, against a result set ordered by `lastModified` and continuously re-published | `offsetMark` cursor, following `nextPage` |
| no completeness check | every walk checks itself against the `count` the API reports |
| a failed metadata request `continue`s past the package — 73 times | recorded as a status row; the verification cell refuses to pass while any remain |

Two bugs in *this* collector were found the same way and fixed: GovInfo answers a
request for a rendition a package does not have with **400, not 404** (which
ended a run at the 4,203rd package), and `raise_for_status` puts the full request
URL — key included — into its message.

Findings worth carrying forward:

- **36,378 packages** 1995–2025, against 30,032 in the corpus the earlier
  pipeline ran on: 3,386 missing in the overlapping window, plus 2,960 after it.
- `docClass` is not just `HHRG`/`SHRG`/`JHRG`. Legacy SuDoc classes — `Y4_J89_1`,
  `Y4_F49`, `Y4_AG8_1` — carry several hundred real hearings, and a
  chamber-based filter drops them silently.
- Roughly 875 packages have **no HTML rendition at all**, all `GOVPUB-` prefixed.
  They have MODS, so they keep their committee and roster and drop out at
  summarization rather than at selection.

## Parsing rules, and how they were checked

`lib/transcript.py` and `lib/speakers.py` implement the rules the earlier
pipeline used. Both were verified against the corpus rather than inherited on
trust, and one was changed.

**Paragraphs break on a four-space indent.** Confirmed: over 400,608 non-blank
lines, 17 percent sit at exactly four spaces and **93.6 percent of lines opening
a speaking turn** are among them. The 6 percent at column zero are almost all
false positives — 1,785 mid-sentence continuations against 20 genuine turns. The
distribution is the same in 2005–2025 as in 1995–2000.

**Speaker attribution is anchored, not searched.** The earlier rule asked whether
`"{Surname}."` appeared anywhere in a paragraph's first five words. That and an
anchored rule agree on **99.85 percent** of 116,833 paragraphs, and every one of
the 173 disagreements falls the same way:

| case | n | what the earlier rule does |
|---|---|---|
| `Mr. Walsh. Mr. Serrano.` | 119 | the chair yields; the turn is attributed to whichever the roster lists first, not to the speaker |
| `Yes, Mr. Baker.` | 36 | a continuation naming a member becomes a new turn by that member |
| `Mr. Lancaster. No, Mr. Rogers.` | 14 | the speaker is not on the roster, so it reaches past them to a member merely mentioned |
| `Present: Representatives Gutknecht and Peterson.` | 4 | a roll-call line becomes a speaking turn |

Zero paragraphs went the other way. Both rules also missed the bracketed-aside
form — `Mr. Ehlers [continuing]. …` — which is 265 further turns;
`speakers.TURN_OPENING` allows it. `speakers.attribute_inherited` keeps the old
rule so a notebook can report the difference rather than assert it is small.

**Questions for the record are separated, not dropped.** Some hearings carry
blocks of written Q&A the transcript itself says were *not* spoken —
`[The following questions were not asked at the hearing…]`. They are **embedded,
not a document tail**: of 26 transcripts carrying a marker, dialogue resumes
after it in 20, and one appropriations hearing has 22 separate blocks. Each is
labelled `qfr` from its marker to the next spoken turn; nothing is discarded, and
which section a stage reads is that stage's decision.

## Known open items

- **`03_parse_mods` has not been run.** It was written against the partial
  corpus and should be executed now that `02` has finished.
- **`lib/crec.py` and `07` still describe the Daily Digest as a second
  summarization reference.** That framing is wrong per the measurement above and
  the prose needs correcting, even though the notebook is no longer run.
- **73 transcripts do not use the four-space convention at all** — nearly all
  from 2006, indent-4 lines under 2 percent — so the paragraph rule collapses
  them into a few giant blocks. Splitting on blank lines recovers turns in some.
  Unresolved.
- **859 C-SPAN programs have no abstract**, concentrated in 2015 (483) and 2014
  (127). Cause not investigated.
- **2015-era `eventid` re-air duplicates** are not deduplicated.
- All rules above were verified on the corpus as downloaded at the time. They
  should be re-run over the complete corpus before the numbers here are quoted
  anywhere else.
