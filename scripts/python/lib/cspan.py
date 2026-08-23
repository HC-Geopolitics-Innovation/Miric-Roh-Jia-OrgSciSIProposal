"""A client for the C-SPAN Archives API, used to collect reference summaries.

C-SPAN writes a short editorial abstract for every program in its Video Library.
For a congressional hearing that abstract is an independent, human-written
account of what the hearing was about, produced without reference to anything
this project does — which is what makes it usable as a reference against which
to check a generated summary.

Know what it is before using it. Measured over 16,853 abstracts, the median is
**48 words** against 388 for a summary this pipeline generates: an eight-fold
difference, and a difference in kind. C-SPAN writes *what the hearing was about*;
the pipeline writes *what was said*. That supports a discriminant test — does the
generated summary of hearing X sit closer to C-SPAN's abstract of X than to any
other hearing's — and it does not support n-gram overlap scoring, where the
length and genre mismatch would dominate whatever signal there is.

**Why the API rather than the website.** The obvious route is to scrape
c-span.org search pages, and it does not work: the site sits behind an AWS WAF
that answers a plain HTTP client with `202` and an empty body after a handful of
requests, and robots.txt disallows the `/ajax` paths the site's own search uses.
The Archives API at `api.c-spanarchives.org` is the supported route, needs a key
from api@c-spanarchives.org, and returns the abstract in full.

API shape, from https://www.c-span.org/api/c-span/ :

    GET /2.0/programs/search   query (Lucene), cursor, sort
    GET /2.0/programs/{id}     one program, with publicId and duration

The searchable fields are abstract, category, date, format, isbn, location,
person, personid, series, sponsor, subject, tag and text. Two syntax details
cost an afternoon to find and are not in the documentation:

* **Dates need full ISO timestamps.** ``date:[2024-01-01T00:00:00Z TO
  2024-12-31T23:59:59Z]`` works; ``date:2024*``, ``date:[2024 TO 2025]`` and
  ``date:>2024-01-01`` all return 500.
* **Committee categories are three separate values** — ``House Committee``,
  ``Senate Committee``, ``Joint Committee``. There is no combined
  "Congressional Committee" value.

Called from `scripts/python/01_dataset_construction/06_collect_cspan.ipynb`.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import requests

BASE_URL = "https://api.c-spanarchives.org/2.0"

#: The API returns twenty programs per page and offers no page-size parameter.
PAGE_SIZE = 20

#: The three category values that hold congressional hearings. Verified against
#: the API: "Congressional Committee", "House Session" and "Senate Session"
#: return nothing.
COMMITTEE_CATEGORIES = ("House Committee", "Senate Committee", "Joint Committee")

#: No published rate limit. Two per second is slow enough not to matter to
#: C-SPAN and fast enough that the whole archive is under an hour.
DEFAULT_RATE_PER_SEC = 2.0

TRANSIENT_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})


class CSpanError(RuntimeError):
    """A request failed permanently, or a cursor walk did not behave."""


def load_api_key(env_file: Path | None = None) -> str:
    """Return `CSPAN_API_KEY` from the environment or from a .env beside the caller."""
    key = os.environ.get("CSPAN_API_KEY")
    if key:
        return key
    if env_file is not None and Path(env_file).exists():
        for line in Path(env_file).read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            if name.strip() == "CSPAN_API_KEY":
                return value.strip().strip('"').strip("'")
    raise CSpanError(
        "CSPAN_API_KEY is not set and no .env supplied one. Request a key from "
        "api@c-spanarchives.org and put it in a .env next to the notebook."
    )


def year_range(year: int) -> str:
    """The Lucene date clause for one calendar year.

    Full timestamps on both ends: the shorter forms the field seems to invite
    all return 500.
    """
    return f"date:[{year}-01-01T00:00:00Z TO {year}-12-31T23:59:59Z]"


@dataclass
class CSpanClient:
    """Rate-limited, retrying client for the two endpoints this project uses.

    The key travels as an ``x-api-key`` header — never in the query string,
    where it would end up in an exception message and from there in a committed
    notebook.
    """

    api_key: str
    rate_per_sec: float = DEFAULT_RATE_PER_SEC
    max_retries: int = 5
    timeout: float = 60.0
    session: requests.Session = field(default_factory=requests.Session, repr=False)
    _last_request: float = field(default=0.0, init=False, repr=False)

    n_requests: int = field(default=0, init=False)
    n_retries: int = field(default=0, init=False)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{BASE_URL}{path}"
        last_error = "no attempt made"
        for attempt in range(self.max_retries):
            gap = 1.0 / self.rate_per_sec
            wait = gap - (time.monotonic() - self._last_request)
            if wait > 0:
                time.sleep(wait)
            self._last_request = time.monotonic()
            self.n_requests += 1
            try:
                response = self.session.get(
                    url,
                    params=params or {},
                    headers={"x-api-key": self.api_key, "Accept": "application/json"},
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                if response.status_code == 200:
                    return response.json()
                if response.status_code not in TRANSIENT_STATUS:
                    raise CSpanError(
                        f"HTTP {response.status_code} for {url}: {response.text[:200]}"
                    )
                last_error = f"HTTP {response.status_code}"
            self.n_retries += 1
            time.sleep(2.0**attempt)
        raise CSpanError(f"{self.max_retries} attempts failed for {url}: {last_error}")

    def search(self, query: str, sort: str = "date asc") -> Iterator[dict[str, Any]]:
        """Every program matching a Lucene query, following the cursor to the end.

        Yields one dict per program: ``id``, ``title``, ``description``,
        ``date``, ``videoLink``, ``imagePath``, ``jwplayerId``.

        The API reports no total, so there is no count to check the walk
        against the way `govinfo.list_published` can. What it does instead is
        refuse to loop: a cursor that returns programs already seen, or that
        stops advancing, raises rather than silently spinning or silently
        stopping short.
        """
        cursor: str | None = None
        seen: set[int] = set()
        while True:
            params = {"query": query, "sort": sort}
            if cursor:
                params["cursor"] = cursor
            payload = self._get("/programs/search", params)

            programs = payload.get("programs") or []
            if not programs:
                return

            fresh = [p for p in programs if p.get("id") not in seen]
            if not fresh:
                raise CSpanError(
                    f"cursor returned only programs already seen for query {query!r}; "
                    "the walk is looping rather than advancing"
                )
            for program in fresh:
                seen.add(program["id"])
                yield program

            next_cursor = payload.get("cursor")
            if not next_cursor or next_cursor == cursor:
                return
            cursor = next_cursor

    def search_year(
        self, year: int, category: str, sort: str = "date asc"
    ) -> list[dict[str, Any]]:
        """Every program in one category and one calendar year.

        Slicing by year keeps each cursor walk short and gives the notebook a
        natural unit to report and to re-collect.
        """
        query = f'category:"{category}" AND {year_range(year)}'
        return list(self.search(query, sort=sort))

    def program(self, video_id: int | str) -> dict[str, Any]:
        """One program's full record.

        Adds ``publicId``, ``eventid``, ``videoDuration`` and ``time`` to what
        the search already returns. Only needed when those fields matter — the
        abstract, title and date all come back from the search itself, so the
        matching work does not need a request per program.
        """
        return self._get(f"/programs/{video_id}")
