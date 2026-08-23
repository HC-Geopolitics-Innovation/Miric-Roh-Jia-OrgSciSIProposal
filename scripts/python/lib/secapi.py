"""A client for sec-api.io: the bulk 10-K dataset, and item extraction.

Two very different jobs, and the split between them is the design decision worth
recording.

**Enumeration comes from the bulk dataset, not the Query API.** The Query API
would need one paginated call per CIK — 25,207 of them for this project's sample
— and its `formType:"10-K"` clause is analysed rather than matched exactly, so a
query for Apple's 10-K filings returns 30 `10-K`, 2 `10-K/A` and 1 `NT 10-K`
together. The bulk dataset instead ships 394 monthly ZIP containers covering all
305,140 annual reports since 1993, and every filing arrives with a
`metadata.json` carrying `cik`, an exact `formType`, `periodOfReport`, `filedAt`
and `linkToFilingDetails`. That is the whole enumeration, in 394 requests, with
no fuzzy matching to undo afterwards.

**Item splitting still comes from the Extractor API.** The bulk records are the
original filing documents — HTML from about 2000 on, SGML-wrapped TXT before
that — and are not split by item. The Extractor takes a URL and fetches from
SEC.gov itself, so having the HTML locally does not reduce the number of
extraction calls; what it buys is a local archive the extraction can be checked
against, and re-run from, without re-enumerating.

Writing a local item splitter instead was considered and rejected: 10-K item
headings appear in the table of contents and in cross-references as well as at
the head of the section they name, and `10-K405` and pre-2001 SGML filings are
laid out differently again. That is a parser project, not a function.

Rate limits are per license tier and are not discoverable from the API. What is
documented is the failure mode: exceeding the per-second limit blocks the key
for the remainder of that second only, with no longer penalty, so a client that
paces itself and retries briefly is safe.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import requests

BASE_URL = "https://api.sec-api.io"

#: Index of every monthly container in the bulk 10-K dataset.
DATASET_INDEX = f"{BASE_URL}/datasets/form-10k-content.json"

#: Form variants the bulk dataset carries. Only the exact `10-K` is the annual
#: report this project wants; the rest are amendments, small-business and
#: transition-period variants, and are filtered out by an exact string match on
#: `formType` rather than by a query clause.
BULK_FORM_TYPES = (
    "10-K", "10-K/A", "10-K405", "10-K405/A", "10-KSB", "10-KSB/A", "10-KT", "10-KT/A",
)

TRANSIENT_STATUS = frozenset({408, 425, 500, 502, 503, 504})

#: Rate limiting is handled separately from other transient failures, because it
#: is not a failure — it is flow control, and it needs the opposite response.
#:
#: Measured against the live API: the ceiling is roughly 8-9 successful requests
#: per second ACCOUNT-WIDE, and exceeding it returns HTTP 429 with an 18-byte
#: body in about 0.07 s and no Retry-After header. The documented penalty lasts
#: only the remainder of the offending second.
#:
#: Treating that as a transient error and backing off exponentially — 1, 2, 4, 8,
#: 16 s — is what collapsed the first extraction run to about 1 request/second
#: per task, an eighth of what one thread can sustain. A 429 costs almost
#: nothing, so the right response is a short constant pause and another attempt.
#: These waits are counted separately and do not consume the retry budget that
#: exists for genuine failures.
RATE_LIMIT_STATUS = 429
RATE_LIMIT_PAUSE = 0.25
MAX_RATE_LIMIT_WAITS = 60


class SecApiError(RuntimeError):
    """A request failed permanently, or a download did not match its expected size."""


class UnsupportedFiling(SecApiError):
    """The Extractor has no item splitter for this filing.

    sec-api answers `HTTP 404 {"error":"filing type not supported"}` for filings it
    cannot split. This is a permanent property of the filing, not a transient
    failure, so it is raised as its own type: a caller that lumps it in with
    network errors will retry it on every resume and will never succeed.
    """


def load_api_key(env_file: Path | None = None, var: str = "SEC_API_KEY") -> str:
    """Return the sec-api key from the environment or a .env beside the caller."""
    key = os.environ.get(var)
    if key:
        return key
    if env_file is not None and Path(env_file).exists():
        for line in Path(env_file).read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            if name.strip() == var:
                return value.strip().strip('"').strip("'")
    raise SecApiError(f"{var} is not set and no .env supplied it.")


@dataclass
class SecApiClient:
    """Rate-limited, retrying client.

    The key travels in the ``Authorization`` header, never in the query string,
    so it cannot reach an exception message and from there a committed notebook.
    """

    api_key: str
    rate_per_sec: float = 4.0
    max_retries: int = 5
    timeout: float = 600.0
    session: requests.Session = field(default_factory=requests.Session, repr=False)
    _last: float = field(default=0.0, init=False, repr=False)

    n_requests: int = field(default=0, init=False)
    n_retries: int = field(default=0, init=False)
    n_rate_limited: int = field(default=0, init=False)

    def _throttle(self) -> None:
        wait = 1.0 / self.rate_per_sec - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def _get(self, url: str, params: dict[str, Any] | None = None, stream: bool = False):
        last = "no attempt made"
        attempt = 0
        waits = 0
        while attempt < self.max_retries:
            self._throttle()
            self.n_requests += 1
            try:
                r = self.session.get(
                    url,
                    params=params or {},
                    headers={"Authorization": self.api_key},
                    timeout=self.timeout,
                    stream=stream,
                )
            except requests.RequestException as exc:
                last = f"{type(exc).__name__}: {exc}"
            else:
                if r.status_code == 200:
                    return r
                if r.status_code == RATE_LIMIT_STATUS:
                    # Flow control, not failure: pause briefly and try again
                    # without spending an attempt. See RATE_LIMIT_PAUSE above.
                    waits += 1
                    self.n_rate_limited += 1
                    if waits > MAX_RATE_LIMIT_WAITS:
                        raise SecApiError(
                            f"still rate limited after {waits} pauses for {url} — "
                            "the aggregate request rate is set too high"
                        )
                    time.sleep(RATE_LIMIT_PAUSE)
                    continue
                if r.status_code == 404 and "not supported" in r.text:
                    raise UnsupportedFiling(f"HTTP 404 for {url}: {r.text[:200]}")
                if r.status_code not in TRANSIENT_STATUS:
                    raise SecApiError(f"HTTP {r.status_code} for {url}: {r.text[:200]}")
                last = f"HTTP {r.status_code}"
            self.n_retries += 1
            attempt += 1
            time.sleep(2.0**attempt)
        raise SecApiError(f"{self.max_retries} attempts failed for {url}: {last}")

    # ------------------------------------------------------------ bulk data --
    def dataset_index(self) -> dict[str, Any]:
        """The dataset manifest: every container with its key, size and record count.

        This is the completeness contract for the download. Each container
        entry states how many filings it holds, so a downloaded archive can be
        checked against what the index promised rather than against itself.
        """
        return self._get(DATASET_INDEX, {"token": self.api_key}).json()

    def download_container(self, key: str, target: Path, expected_size: int | None = None) -> int:
        """Download one monthly container to ``target``.

        Written to a temporary name and renamed on completion, so an interrupted
        download cannot leave a truncated ZIP that a resume would accept as done.
        Returns bytes written.
        """
        target = Path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        url = f"{BASE_URL}/datasets/form-10k-content/{key}"
        tmp = target.with_suffix(target.suffix + ".partial")

        with self._get(url, {"token": self.api_key}, stream=True) as r, tmp.open("wb") as fh:
            written = 0
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
                    written += len(chunk)

        if expected_size is not None and written != expected_size:
            tmp.unlink(missing_ok=True)
            raise SecApiError(
                f"{key}: expected {expected_size:,} bytes, got {written:,}. "
                "Refusing to keep a short container."
            )
        tmp.replace(target)
        return written

    # ------------------------------------------------------------- extractor --
    def get_section(self, filing_url: str, item: str, return_type: str = "text") -> str:
        """One 10-K item, as text or HTML.

        Item ids are the strings the Extractor uses: ``"1"`` for Business and
        ``"7"`` for Management's Discussion and Analysis.
        """
        r = self._get(
            f"{BASE_URL}/extractor",
            {"url": filing_url, "item": item, "type": return_type, "token": self.api_key},
        )
        return r.text
