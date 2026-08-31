"""A GovInfo API client that cannot lose records without saying so.

The collection this replaces lost about 12 percent of the CHRG corpus and did
not report it. Two collections run eight months apart disagreed in *both*
directions — 3,602 packages the first pull never saw, and 363 the second pull
lost — which is the signature of a collector whose failures are invisible. Three
specific defects produced that:

1. **A network error inside the pagination loop ended the loop.** The old client
   caught ``RequestException``, logged it, and ``break``-ed, returning the
   partial page list to a caller that treated it as the complete answer. It
   happened 18 times, silently truncating whole quarters.
2. **A failed metadata request skipped the package.** ``except Exception:
   continue`` dropped 73 packages, and because the downstream combine step
   globbed the filesystem for whatever had been written, those packages simply
   did not exist as far as the pipeline was concerned.
3. **Pagination used ``offset`` with no sort order.** GovInfo orders
   ``/published`` by ``lastModified`` and re-issues packages continuously, so
   the result set shifts underneath an offset-based traversal. Records get
   skipped or repeated depending on what was re-published mid-walk. GovInfo's
   own documentation directs callers to ``offsetMark``, which is a cursor rather
   than a position.

This module inverts all three. Transient failures are retried with backoff and
then **raised**; a partial result is never returned as a whole one. Pagination
uses ``offsetMark``, following the ``nextPage`` cursor the API returns. And
``list_published`` checks its own work against the ``count`` the API reports,
raising when they disagree, so a short read is an error at the point it happens
rather than a discovery eight months later.

The API key is read from the environment. It is never a literal in this file,
which is how the four keys in the previous collector ended up in the source.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, Literal

import requests

BASE_URL = "https://api.govinfo.gov"

#: GovInfo caps a page at 1000 records. Fewer pages means fewer chances for a
#: cursor walk to be interrupted, so the collector always asks for the maximum.
MAX_PAGE_SIZE = 1000

#: Published rate limits for a registered key are 40 requests/second and 1,200
#: per minute. The collector runs well under that: the whole corpus is roughly
#: 68,000 file requests, and at 10/s that is under two hours, which is not worth
#: crowding a shared public API for.
DEFAULT_RATE_PER_SEC = 10.0

#: Retried. Anything else is treated as permanent and recorded rather than retried.
TRANSIENT_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})

#: GovInfo answers a request for a rendition a package does not have with
#: **400 and a body saying so**, not 404. Discovered the hard way: a GOVPUB
#: package with no HTML rendition returned
#: ``{"message":"The requested resource does not exist."}`` under a 400, which
#: fell through to `raise_for_status` and ended a 36,000-package run at the
#: 4,203rd. Both codes now mean the same thing, and the body is checked so a
#: genuine malformed-request 400 is not silently recorded as a missing file.
MISSING_STATUS = frozenset({400, 404})
MISSING_BODY = "does not exist"

FileKind = Literal["mods", "htm"]


class GovInfoError(RuntimeError):
    """A request failed permanently, or a page walk did not return what it promised.

    Raised rather than logged. The whole point of this module is that a caller
    cannot mistake an incomplete answer for a complete one.
    """


class MissingFile(GovInfoError):
    """GovInfo returned 404 for a file that its own package listing advertised.

    Distinct from `GovInfoError` because it is a fact about the collection —
    some packages genuinely have no HTML rendition — and belongs in the status
    log as an observation, not in a retry loop.
    """


def load_api_key(env_file: Path | None = None, var: str = "GOVINFO_API_KEY") -> str:
    """Return a GovInfo API key from the environment, or from a .env beside the caller.

    Parameters
    ----------
    env_file : Path or None
        Optional ``.env`` to read when ``var`` is not already set in the
        environment. Parsed with a deliberately small reader rather than a
        dependency; the file holds one ``KEY=value`` per line.
    var : str
        Which variable to read. Rate limits are per key, and this project runs
        two collections against GovInfo at once — the hearing corpus and the
        Congressional Record — so each takes its own key rather than sharing
        one and slowing both. `05_collect_daily_digest` passes
        ``GOVINFO_API_KEY_CREC``.

    Raises
    ------
    GovInfoError
        If no key can be found. Failing here is better than falling back to
        ``DEMO_KEY`` and silently collecting against a shared rate limit.
    """
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

    raise GovInfoError(
        f"{var} is not set and no .env supplied it. "
        "Register a key at https://api.data.gov/signup/ and export it, or put it "
        "in a .env next to the notebook (the .gitignore already excludes .env)."
    )


@dataclass
class GovInfoClient:
    """A rate-limited, retrying client for the endpoints this project uses.

    Parameters
    ----------
    api_key : str
        From `load_api_key`. Sent as a query parameter, which is what GovInfo
        accepts; it is kept out of every log line this module writes.
    rate_per_sec : float
        Requests per second, enforced by spacing rather than by a bucket. The
        default is a quarter of the published ceiling.
    max_retries : int
        Attempts per request before raising. Backoff is exponential from one
        second, and a ``Retry-After`` header overrides it when present.
    timeout : float
        Per-request timeout in seconds. Transcript HTML runs to several MB, so
        this is generous.
    """

    api_key: str
    rate_per_sec: float = DEFAULT_RATE_PER_SEC
    max_retries: int = 5
    timeout: float = 120.0
    session: requests.Session = field(default_factory=requests.Session, repr=False)
    _last_request: float = field(default=0.0, init=False, repr=False)

    #: Incremented as the client works, so a notebook can report what it cost.
    n_requests: int = field(default=0, init=False)
    n_retries: int = field(default=0, init=False)

    # ------------------------------------------------------------------ core --
    def _throttle(self) -> None:
        gap = 1.0 / self.rate_per_sec
        wait = gap - (time.monotonic() - self._last_request)
        if wait > 0:
            time.sleep(wait)
        self._last_request = time.monotonic()

    def _request(self, url: str, params: dict[str, Any] | None = None) -> requests.Response:
        """One GET, retried on transient failure, raised on permanent failure.

        Returns the `requests.Response` so callers can decide between ``.json()``
        and ``.content``. Never returns a failed response, and never raises
        anything but `GovInfoError` or `MissingFile` — a bare
        `requests.HTTPError` carries the full request URL in its message, and
        with the key in the query string that message puts a live credential
        into a traceback and from there into a committed notebook.

        The key travels as an ``X-Api-Key`` header for the same reason. GovInfo
        accepts either form; only one of them keeps the credential out of
        anything that gets printed.
        """
        params = dict(params or {})
        safe_url = _redact(url, self.api_key)
        last_error: str = "no attempt made"

        for attempt in range(self.max_retries):
            self._throttle()
            self.n_requests += 1
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers={"X-Api-Key": self.api_key},
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                # Connection reset, DNS failure, timeout, and the "Network is
                # unreachable" that took out 73 packages in the old collection.
                # All transient by assumption; if they are not, the retry budget
                # runs out and this raises rather than skipping the record.
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                code = response.status_code
                if code in MISSING_STATUS and MISSING_BODY in response.text.lower():
                    raise MissingFile(f"HTTP {code}, no such rendition: {safe_url}")
                if code < 400:
                    return response
                if code not in TRANSIENT_STATUS:
                    # A permanent error that is not "absent": bad key, revoked
                    # key, malformed request. Retrying cannot help and the
                    # caller must see it rather than record a missing file.
                    raise GovInfoError(
                        f"HTTP {code} for {safe_url}: {response.text[:200]}"
                    )
                last_error = f"HTTP {code}"
                retry_after = response.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    time.sleep(int(retry_after))
                    self.n_retries += 1
                    continue

            self.n_retries += 1
            time.sleep(2.0**attempt)

        raise GovInfoError(f"{self.max_retries} attempts failed for {safe_url}: {last_error}")

    # ------------------------------------------------------------ enumeration --
    def list_published(
        self,
        start_date: str,
        end_date: str,
        collection: str = "CHRG",
        page_size: int = MAX_PAGE_SIZE,
    ) -> list[dict[str, Any]]:
        """Every package issued in ``[start_date, end_date]``, as a complete list.

        Walks the ``offsetMark`` cursor from ``*`` until the API stops handing
        back a ``nextPage``, then checks the number of records against the
        ``count`` the API reported on the first page. That check is the whole
        reason this function exists: it converts "the walk ended early" from a
        silent data loss into an exception.

        Parameters
        ----------
        start_date, end_date : str
            ``YYYY-MM-DD``, inclusive, matched against ``dateIssued``.
        collection : str
            GovInfo collection code. ``CHRG`` is congressional hearings.
        page_size : int
            Records per request, capped at `MAX_PAGE_SIZE`.

        Returns
        -------
        list of dict
            One record per package, carrying ``packageId``, ``dateIssued``,
            ``lastModified``, ``congress``, ``docClass``, and ``title``.

        Raises
        ------
        GovInfoError
            If the walk returns a different number of records than ``count``,
            or if a page fails after the retry budget is spent.
        """
        url = f"{BASE_URL}/published/{start_date}/{end_date}"
        params = {
            "collection": collection,
            "pageSize": min(page_size, MAX_PAGE_SIZE),
            "offsetMark": "*",
        }

        records: list[dict[str, Any]] = []
        reported_count: int | None = None
        pages = 0

        while True:
            payload = self._request(url, params).json()
            pages += 1
            if reported_count is None:
                reported_count = int(payload.get("count", 0))

            records.extend(payload.get("packages") or [])

            next_page = payload.get("nextPage")
            if not next_page:
                break
            # nextPage is a full URL carrying the cursor. Take the cursor rather
            # than the URL so the api_key stays under this client's control.
            params["offsetMark"] = _offset_mark_of(next_page)

        if reported_count is not None and len(records) != reported_count:
            raise GovInfoError(
                f"incomplete walk for {collection} {start_date}..{end_date}: "
                f"API reported count={reported_count} but {len(records)} records "
                f"came back over {pages} page(s). Refusing to return a partial list."
            )

        return records

    def iter_published_years(
        self, first_year: int, last_year: int, collection: str = "CHRG"
    ) -> Iterator[tuple[int, list[dict[str, Any]]]]:
        """`list_published` for one calendar year at a time, oldest first.

        Yearly slices keep each cursor walk short and make the manifest
        partition on the same key the raw tree does.
        """
        for year in range(first_year, last_year + 1):
            yield year, self.list_published(f"{year}-01-01", f"{year}-12-31", collection)

    # -------------------------------------------------------------- retrieval --
    def list_granules(
        self, package_id: str, granule_class: str | None = None
    ) -> list[dict[str, Any]]:
        """Every granule in a package, following the cursor to the end.

        A CHRG package is one document, but a Congressional Record issue is a
        few hundred separately addressable pieces, and the piece this project
        wants — the Daily Digest's committee-meeting summaries — is one of them.
        The walk checks itself against the reported ``count`` for the same
        reason `list_published` does.

        Parameters
        ----------
        package_id : str
            e.g. ``CREC-2024-03-05``.
        granule_class : str or None
            Filter applied after the walk, not by the API. ``DAILYDIGEST`` is
            the class the Daily Digest granules carry.

        Raises
        ------
        GovInfoError
            If the walk returns a different number of granules than ``count``.
            Note that some packages answer this endpoint with a persistent 500
            — ``CREC-2024-09-17`` does while ``CREC-2024-09-18`` does not — so a
            caller working through many packages should catch this and record
            the failure rather than stopping.
        """
        url = f"{BASE_URL}/packages/{package_id}/granules"
        params: dict[str, Any] = {"offsetMark": "*", "pageSize": MAX_PAGE_SIZE}
        granules: list[dict[str, Any]] = []
        reported: int | None = None

        while True:
            payload = self._request(url, params).json()
            if reported is None:
                reported = int(payload.get("count", 0))
            granules.extend(payload.get("granules") or [])
            next_page = payload.get("nextPage")
            if not next_page or len(granules) >= reported:
                break
            params["offsetMark"] = _offset_mark_of(next_page)

        if reported is not None and len(granules) != reported:
            raise GovInfoError(
                f"incomplete granule walk for {package_id}: API reported "
                f"count={reported} but {len(granules)} came back"
            )

        if granule_class is not None:
            granules = [g for g in granules if g.get("granuleClass") == granule_class]
        return granules

    def fetch_granule_file(
        self, package_id: str, granule_id: str, kind: str = "htm"
    ) -> bytes:
        """One rendition of one granule."""
        return self._request(
            f"{BASE_URL}/packages/{package_id}/granules/{granule_id}/{kind}"
        ).content

    def fetch_file(self, package_id: str, kind: FileKind) -> bytes:
        """Download one package rendition.

        ``/packages/{id}/mods`` and ``/packages/{id}/htm`` serve the MODS record
        and the transcript directly. The previous collector first requested
        ``/packages/{id}/summary`` to read a download link out of it, which cost
        an extra request per package — about 34,000 of them — and added a second
        place the walk could fail.

        Raises
        ------
        MissingFile
            The package has no rendition of this kind. A real property of some
            packages; the caller records it and moves on.
        GovInfoError
            Transient failure that outlived the retry budget.
        """
        return self._request(f"{BASE_URL}/packages/{package_id}/{kind}").content


def _offset_mark_of(next_page_url: str) -> str:
    """Pull the ``offsetMark`` cursor out of the ``nextPage`` URL."""
    from urllib.parse import parse_qs, urlparse

    marks = parse_qs(urlparse(next_page_url).query).get("offsetMark")
    if not marks:
        raise GovInfoError(f"nextPage carried no offsetMark: {next_page_url[:120]}")
    return marks[0]


def _redact(url: str, api_key: str) -> str:
    """URL safe to put in an exception message or a log line."""
    return url.replace(api_key, "<API_KEY>") if api_key else url
