"""Single source of path truth for the llm_method notebooks.

Usage from any notebook::

    import sys; sys.path.insert(0, "../lib")   # notebooks run with cwd = their folder
    from paths import RAW, INTERIM, PROCESSED, GOVINFO_RAW, output_dir

No notebook carries a project root or a data location as a literal. `ROOT` is
derived from this file's own position and `SCRATCH` from `$USER`, so a clone
runs from wherever it is placed and writes its own intermediates.
"""

import os
from pathlib import Path

# scripts/python/lib/paths.py -> project root is three levels up
ROOT = Path(__file__).resolve().parents[3]

# ---------------------------------------------------------------- repository --
# Only small, public, paper-facing material lives in the repository itself:
# reference tables, the demonstration subset, and the figures.
DATA_REPO = ROOT / "data"
FIGURES = ROOT / "paper" / "figures"

# Assembled corpora, one file per stage. These are the tables the LLM stages read
# from, so they live with the paper rather than on scratch — but they carry full
# document text and are large, and `*.parquet` is gitignored for that reason.
#   02_hearings/hearings_all.parquet      every CHRG package, metadata + turns
#   03_sp500_10k_item1/…parquet           the S&P 500 Item 1 table, from stage 01
HEARINGS_REPO = DATA_REPO / "raw" / "02_hearings"

# ------------------------------------------------------------------- scratch --
# Everything bulk lives on scratch. /scratch2 is not backed up and is not
# quota-enforced; nothing here is archival, and all of it is reproducible from
# the GovInfo API plus the notebooks.
SCRATCH = Path("/scratch2") / os.environ.get("USER", "acroh") / "projects" / "llm_method"
DATA = SCRATCH / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"

# Stage 0 — the GovInfo CHRG collection.
#   manifest/packages_{year}.json  one record per package, from /published
#   {year}/mods/{packageId}.xml    MODS metadata (committee, members, witnesses)
#   {year}/html/{packageId}.htm    the hearing transcript
#   status/fetch_{year}.jsonl      one line per package: what was written, or why not
GOVINFO_RAW = RAW / "govinfo"
GOVINFO_MANIFEST = GOVINFO_RAW / "manifest"
GOVINFO_STATUS = GOVINFO_RAW / "status"

# C-SPAN Archives API results. The abstracts here are the independent reference
# against which generated summaries are checked, so they are collected and kept
# separately from anything the pipeline produces.
#   search/{category}_{year}.jsonl   one line per program, from /programs/search
#   detail/{videoId}.json            one file per program, from /programs/{id}
#   programs.parquet                 search and detail merged
CSPAN_RAW = RAW / "cspan"
CSPAN_SEARCH = CSPAN_RAW / "search"
CSPAN_DETAIL = CSPAN_RAW / "detail"

# Congressional Record Daily Digest: Congress's own one-paragraph account of
# each committee meeting, the second reference summaries are checked against.
#   {packageId}/{chamber}__{granuleId}.txt   granule text, verbatim
#   packages.parquet                         one row per issue of the Record
#   committee_meetings.parquet               one row per meeting
CREC_RAW = RAW / "crec"

# SEC 10-K corpus. The bulk dataset ships 305,140 annual reports as monthly ZIP
# containers, each filing a directory holding the primary document plus a
# metadata.json with cik, exact formType, periodOfReport and the SEC.gov URL the
# Extractor API takes.
#   form10k_index.json        the dataset manifest: every container, size, record count
#   form10k/{yyyy}/{yyyy-mm}.zip  the containers
#   filings.parquet           one row per filing, joined to GVKEY
#   {run}/item{X}/{cik}/{accessionNo}.txt  extracted item text, one run per tree
#   {run}/status/extract_{shard}.jsonl     one line per filing-item attempted
SEC_RAW = RAW / "sec"
SEC_BULK = SEC_RAW / "form10k"
SEC_INTERIM = INTERIM / "sec"

# Extraction runs are kept in separate trees, one per run, named by what the run
# is for. `sp500_item1` is the S&P 500 Item 1 pass; `items` is the full six-item
# pass over the whole sample. Keeping them apart means the two never share a
# status log or an output directory, so they can run independently and one
# cannot be mistaken for the other on disk.
SEC_ITEMS = SEC_INTERIM / "items"
SEC_STATUS = SEC_ITEMS / "status"


def sec_run_dir(name: str) -> Path:
    """Root of one extraction run: items under `item{X}/`, logs under `status/`."""
    d = SEC_INTERIM / name
    (d / "status").mkdir(parents=True, exist_ok=True)
    return d

# Hugging Face weights, kept off /home1 — a single 8B model in bf16 is 16 GB and
# /home1 is a 100 GB quota shared with everything else the user owns.
HF_CACHE = SCRATCH / "hf_cache"

# Stage 2, text summarization. One tree per run, named for the model and scope,
# so two models' outputs are never mixed and neither has to be regenerated to
# compare them.
#   {run}/summaries.parquet          one row per hearing
#   {run}/status/*.jsonl             one line per hearing attempted
SUMMARY_INTERIM = INTERIM / "summaries"


def summary_run_dir(name: str) -> Path:
    """Root of one summarization run: outputs plus its own status log."""
    d = SUMMARY_INTERIM / name
    (d / "status").mkdir(parents=True, exist_ok=True)
    return d


# Stage 3, topic extraction. Same layout discipline as summaries: one tree per
# run under interim, holding parquet outputs plus per-call status logs.
TOPICS_INTERIM = INTERIM / "topics"


def topics_run_dir(name: str) -> Path:
    """Root of one topic-extraction run: outputs plus its own status log."""
    d = TOPICS_INTERIM / name
    (d / "status").mkdir(parents=True, exist_ok=True)
    return d


# Stage 4, topic relevance. Sentence tables and embedding matrices for the
# deterministic rail, judgment logs for the classification layer.
RELEVANCE_INTERIM = INTERIM / "relevance"


def relevance_run_dir(name: str) -> Path:
    """Root of one relevance-stage run: outputs plus its own status log."""
    d = RELEVANCE_INTERIM / name
    (d / "status").mkdir(parents=True, exist_ok=True)
    return d


def output_dir(stem: str) -> Path:
    """By-notebook output folder beside the running notebook: output/<stem>/.

    Assumes cwd is the notebook's own folder, which is what both Jupyter and
    `nbconvert --execute` give.
    """
    out = Path.cwd() / "output" / stem
    out.mkdir(parents=True, exist_ok=True)
    return out


#: Subdirectories under a collection year. `pdf` holds the scanned-only
#: packages: a few hundred older GOVPUB records exist on GovInfo as PDF and
#: nothing else — no HTML, no text rendition — so the PDF is the only copy of
#: their content there is.
GOVINFO_KINDS = {"mods", "html", "pdf"}


def govinfo_year_dir(year: int, kind: str) -> Path:
    """Directory holding one file type for one collection year.

    Parameters
    ----------
    year : int
        Calendar year of `dateIssued`, which is how GovInfo partitions
        `/published` queries and therefore how the raw tree is laid out.
    kind : str
        One of `GOVINFO_KINDS`.
    """
    if kind not in GOVINFO_KINDS:
        raise ValueError(f"kind must be one of {sorted(GOVINFO_KINDS)}, got {kind!r}")
    d = GOVINFO_RAW / str(year) / kind
    d.mkdir(parents=True, exist_ok=True)
    return d
