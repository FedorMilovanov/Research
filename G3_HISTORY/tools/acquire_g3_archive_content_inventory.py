#!/usr/bin/env python3
"""Acquire a metadata-only Wayback CDX URL inventory for historical G3 domains.

This v2 lane uses the Internet Archive CDX resumption-key protocol so large
queries are consumed in bounded pages instead of relying on a single large
response or heuristic month splitting.

No archived HTML bodies are fetched or stored.

Exit contract:
- 0: every planned host/year query reached terminal CDX exhaustion;
- 2: parse/schema/invariant/non-transport defect (fail closed);
- 3: bounded retryable transport failures were exhausted;
- 4: a query exceeded the configured resume-page safety bound.

A successful URL inventory is discovery evidence only. It does not close the
article denominator, domain-era attribution, topic coding, or quantitative
language gates.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

UA = "FedorMilovanov-Research-G3-Archive-Census/2.0 (metadata-only; no body fetch)"
CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
RETRY_DELAYS = (2, 6)
DEFAULT_LIMIT = 750
DEFAULT_MAX_PAGES = 40

FAMILIES = (
    {
        "family": "g3conference.com",
        "hosts": ("g3conference.com", "www.g3conference.com"),
        "start_year": 2011,
        "end_year": 2020,
    },
    {
        "family": "g3min.org",
        "hosts": ("g3min.org", "www.g3min.org"),
        "start_year": 2020,
        "end_year": 2026,
    },
)

ASSET_EXTENSIONS = {
    ".7z", ".avi", ".bmp", ".css", ".csv", ".doc", ".docx", ".eot", ".epub",
    ".gif", ".gz", ".ico", ".jpeg", ".jpg", ".js", ".json", ".m4a", ".m4v",
    ".map", ".mov", ".mp3", ".mp4", ".mpeg", ".ogg", ".otf", ".pdf", ".png",
    ".ppt", ".pptx", ".rar", ".rss", ".svg", ".tar", ".tgz", ".tif", ".tiff",
    ".ttf", ".txt", ".wav", ".webm", ".webp", ".woff", ".woff2", ".xls", ".xlsx",
    ".xml", ".zip",
}
NAV_PREFIXES = (
    "/wp-admin", "/wp-content", "/wp-includes", "/wp-json", "/feed", "/comments",
    "/category/", "/tag/", "/author/", "/search", "/sitemap", "/robots",
    "/cart", "/checkout", "/account", "/my-account", "/login", "/register",
)
GENERIC_PAGES = {
    "/", "/about/", "/contact/", "/events/", "/event/", "/donate/", "/giving/",
    "/resources/", "/articles/", "/blog/", "/podcast/", "/podcasts/",
    "/conference/", "/conferences/", "/national-conference/", "/speakers/",
}
DATED_POST_RE = re.compile(r"^/(?:19|20)\d{2}/\d{1,2}/(?:\d{1,2}/)?[^/]+/?$")
YEAR_PAGE_RE = re.compile(r"^/(?:19|20)\d{2}/?$")
PAGE_PAGINATION_RE = re.compile(r"^/page/\d+/?$")


class TransportHold(RuntimeError):
    """Bounded retryable external transport failure."""


class PageLimitHold(RuntimeError):
    """Resume pagination safety bound reached before CDX exhaustion."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def fetch(url: str, *, timeout: int = 45, attempts: int = 3) -> tuple[bytes, dict]:
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": UA, "Accept": "application/json,*/*"},
        )
        started = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                return data, {
                    "requested_url": url,
                    "final_url": response.geturl(),
                    "status": getattr(response, "status", None),
                    "content_type": response.headers.get("Content-Type"),
                    "content_encoding": response.headers.get("Content-Encoding"),
                    "bytes": len(data),
                    "sha256": sha256_bytes(data),
                    "elapsed_seconds": round(time.time() - started, 3),
                    "attempt": attempt,
                    "max_attempts": attempts,
                }
        except urllib.error.HTTPError as exc:
            body = exc.read()
            msg = (
                f"HTTP {exc.code} {exc.reason} url={url} "
                f"body_sha256={sha256_bytes(body)} bytes={len(body)} "
                f"attempt={attempt}/{attempts}"
            )
            if exc.code not in RETRYABLE_HTTP:
                raise RuntimeError(msg) from exc
            if attempt >= attempts:
                raise TransportHold(msg) from exc
        except urllib.error.URLError as exc:
            msg = f"URL error {exc.reason} url={url} attempt={attempt}/{attempts}"
            if attempt >= attempts:
                raise TransportHold(msg) from exc
        except TimeoutError as exc:
            msg = f"Timeout url={url} attempt={attempt}/{attempts}"
            if attempt >= attempts:
                raise TransportHold(msg) from exc

        delay = RETRY_DELAYS[min(attempt - 1, len(RETRY_DELAYS) - 1)]
        print(
            "TRANSIENT_RETRY",
            f"attempt={attempt}/{attempts}",
            f"sleep={delay}s",
            url,
            file=sys.stderr,
        )
        time.sleep(delay)

    raise RuntimeError(f"fetch exhausted unexpectedly url={url}")


def parse_cdx_page(data: bytes) -> tuple[list[dict], str | None, str]:
    try:
        rows = json.loads(data.decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"CDX response is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(rows, list):
        raise RuntimeError("CDX JSON root is not a list")
    if not rows:
        return [], None, "VALID_EMPTY_CDX"

    header = rows[0]
    required = {"timestamp", "original", "statuscode", "mimetype", "digest"}
    if not isinstance(header, list) or not required.issubset(set(header)):
        raise RuntimeError(f"CDX response has invalid header: {header!r}")

    resume_key: str | None = None
    data_rows = rows[1:]
    if len(data_rows) >= 2 and data_rows[-2] == []:
        resume_row = data_rows[-1]
        if not isinstance(resume_row, list) or len(resume_row) != 1:
            raise RuntimeError(f"CDX resume row has invalid shape: {resume_row!r}")
        resume_key = resume_row[0]
        if not isinstance(resume_key, str) or not resume_key:
            raise RuntimeError("CDX resume key is empty/non-string")
        data_rows = data_rows[:-2]

    captures: list[dict] = []
    for idx, row in enumerate(data_rows, start=1):
        if not isinstance(row, list) or len(row) != len(header):
            raise RuntimeError(f"CDX row {idx} shape mismatch")
        captures.append(dict(zip(header, row)))

    if captures:
        state = "CAPTURES_PRESENT_MORE" if resume_key else "CAPTURES_PRESENT_TERMINAL"
    else:
        state = "VALID_HEADER_ZERO_ROWS"
        if resume_key:
            raise RuntimeError("CDX returned resume key with zero data rows")
    return captures, resume_key, state


def cdx_url(
    host: str,
    from_value: str,
    to_value: str,
    limit: int,
    resume_key: str | None,
) -> str:
    params = [
        ("url", f"{host}/*"),
        ("from", from_value),
        ("to", to_value),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length"),
        ("filter", "statuscode:200"),
        ("filter", "mimetype:text/html"),
        ("collapse", "urlkey"),
        ("limit", str(limit)),
        ("showResumeKey", "true"),
    ]
    if resume_key:
        params.append(("resumeKey", resume_key))
    return CDX_ENDPOINT + "?" + urllib.parse.urlencode(params)


def normalize_url(original: str, family: str) -> tuple[str | None, dict]:
    raw = original.strip()
    if not raw:
        return None, {"reason": "empty_original"}
    candidate = raw if "://" in raw else "http://" + raw
    try:
        parsed = urllib.parse.urlsplit(candidate)
    except Exception as exc:
        return None, {"reason": "urlsplit_error", "error": repr(exc)}

    host = (parsed.hostname or "").casefold().rstrip(".")
    normalized_host = host[4:] if host.startswith("www.") else host
    if normalized_host != family:
        return None, {"reason": "host_outside_family", "host": host}

    path = urllib.parse.unquote(parsed.path or "/", errors="replace")
    path = re.sub(r"/{2,}", "/", path)
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not path.endswith("/"):
        leaf = path.rsplit("/", 1)[-1]
        if "." not in leaf:
            path += "/"

    canonical = f"https://{family}{path}"
    return canonical, {
        "host": host,
        "path": path,
        "query_present": bool(parsed.query),
        "fragment_present": bool(parsed.fragment),
    }


def classify_route(path: str) -> str:
    lower = path.casefold()
    leaf = lower.rstrip("/").rsplit("/", 1)[-1] if lower != "/" else ""
    suffix = "." + leaf.rsplit(".", 1)[-1] if "." in leaf else ""
    if suffix in ASSET_EXTENSIONS:
        return "asset_or_nonhtml_extension"
    if PAGE_PAGINATION_RE.match(lower) or YEAR_PAGE_RE.match(lower):
        return "navigation_or_archive"
    if any(lower.startswith(prefix) for prefix in NAV_PREFIXES):
        return "navigation_or_taxonomy"
    if lower in GENERIC_PAGES:
        return "navigation_or_landing"
    if "/podcast/" in lower or "/podcasts/" in lower:
        return "podcast_candidate"
    if (
        "/conference/" in lower
        or "/conferences/" in lower
        or "/national-conference/" in lower
    ):
        return "conference_page_candidate"
    if "/event/" in lower or "/events/" in lower:
        return "event_page_candidate"
    if DATED_POST_RE.match(lower):
        return "dated_article_candidate"
    return "article_or_page_candidate"


def query_year(
    *,
    family: str,
    host: str,
    year: int,
    limit: int,
    max_pages: int,
    sleep_ms: int,
    receipt: dict,
) -> list[dict]:
    from_value = f"{year}0101"
    to_value = f"{year}1231"
    resume_key: str | None = None
    seen_resume_keys: set[str] = set()
    rows: list[dict] = []

    for page_index in range(1, max_pages + 1):
        url = cdx_url(host, from_value, to_value, limit, resume_key)
        raw, fetch_meta = fetch(url)
        captures, next_resume, state = parse_cdx_page(raw)
        receipt["pages"].append({
            "family": family,
            "host": host,
            "year": year,
            "page_index": page_index,
            "query_state": state,
            "row_count": len(captures),
            "limit": limit,
            "resume_key_in": resume_key,
            "resume_key_out": next_resume,
            "fetch": fetch_meta,
        })

        for item in captures:
            item["_family"] = family
            item["_host_query"] = host
            item["_year_query"] = str(year)
            item["_page_index"] = page_index
        rows.extend(captures)

        if not next_resume:
            return rows
        if next_resume in seen_resume_keys:
            raise RuntimeError(
                f"CDX resume-key cycle family={family} host={host} year={year}"
            )
        seen_resume_keys.add(next_resume)
        resume_key = next_resume
        time.sleep(max(sleep_ms, 0) / 1000)

    raise PageLimitHold(
        f"{family} host={host} year={year} exceeded max_pages={max_pages} "
        f"with resume_key still present"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="g3-archive-content-inventory")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--sleep-ms", type=int, default=75)
    args = parser.parse_args()

    if args.limit < 100 or args.limit > 5000:
        print("ERROR --limit must be between 100 and 5000", file=sys.stderr)
        return 2
    if args.max_pages < 1 or args.max_pages > 500:
        print("ERROR --max-pages must be between 1 and 500", file=sys.stderr)
        return 2

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "g3-archive-content-inventory-v2",
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "metadata_only": True,
        "archived_html_bodies_fetched": False,
        "publication_authorized": False,
        "domain_era_attribution_closed": False,
        "article_denominator_closed": False,
        "topic_coding_authorized": False,
        "quantitative_language_authorized": False,
        "negative_result_boundary": (
            "Missing captures, transport failures, archive gaps, URL classification, "
            "or domain-era uncertainty must not be converted into evidence that "
            "historical content did not exist."
        ),
        "method": {
            "endpoint": CDX_ENDPOINT,
            "filters": ["statuscode:200", "mimetype:text/html"],
            "collapse": "urlkey",
            "pagination": "showResumeKey=true + resumeKey until terminal exhaustion",
            "families": FAMILIES,
            "row_limit": args.limit,
            "max_pages_per_host_year": args.max_pages,
        },
        "pages": [],
        "transport_holds": [],
        "page_limit_holds": [],
        "errors": [],
    }

    all_captures: list[dict] = []
    completed_host_years = 0
    planned_host_years = sum(
        len(cfg["hosts"]) * (cfg["end_year"] - cfg["start_year"] + 1)
        for cfg in FAMILIES
    )

    for cfg in FAMILIES:
        family = cfg["family"]
        for host in cfg["hosts"]:
            for year in range(cfg["start_year"], cfg["end_year"] + 1):
                try:
                    year_rows = query_year(
                        family=family,
                        host=host,
                        year=year,
                        limit=args.limit,
                        max_pages=args.max_pages,
                        sleep_ms=args.sleep_ms,
                        receipt=receipt,
                    )
                    all_captures.extend(year_rows)
                    completed_host_years += 1
                except PageLimitHold as exc:
                    receipt["page_limit_holds"].append(str(exc))
                except TransportHold as exc:
                    receipt["transport_holds"].append(str(exc))
                except Exception as exc:
                    receipt["errors"].append(
                        f"{family} host={host} year={year}: {exc}"
                    )
                time.sleep(max(args.sleep_ms, 0) / 1000)

    raw_fields = [
        "family", "host_query", "year_query", "page_index", "timestamp",
        "original", "statuscode", "mimetype", "digest", "length",
    ]
    with (out / "cdx_capture_witnesses.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        writer = csv.DictWriter(fh, fieldnames=raw_fields)
        writer.writeheader()
        for item in sorted(
            all_captures,
            key=lambda x: (
                x.get("_family", ""),
                x.get("timestamp", ""),
                x.get("original", ""),
            ),
        ):
            writer.writerow({
                "family": item.get("_family"),
                "host_query": item.get("_host_query"),
                "year_query": item.get("_year_query"),
                "page_index": item.get("_page_index"),
                "timestamp": item.get("timestamp"),
                "original": item.get("original"),
                "statuscode": item.get("statuscode"),
                "mimetype": item.get("mimetype"),
                "digest": item.get("digest"),
                "length": item.get("length"),
            })

    by_canonical: dict[str, dict] = {}
    rejected_reasons: Counter[str] = Counter()
    for item in all_captures:
        family = item["_family"]
        canonical, meta = normalize_url(item.get("original", ""), family)
        if canonical is None:
            rejected_reasons[meta.get("reason", "unknown")] += 1
            continue
        route_class = classify_route(meta["path"])
        timestamp = item.get("timestamp", "")
        existing = by_canonical.get(canonical)
        if existing is None:
            by_canonical[canonical] = {
                "family": family,
                "canonical_url": canonical,
                "path": meta["path"],
                "route_class": route_class,
                "first_capture_witness": timestamp,
                "last_capture_witness": timestamp,
                "capture_witness_count": 1,
                "query_present_observed": meta["query_present"],
                "source_original_examples": [item.get("original", "")],
                "digests": [item.get("digest")] if item.get("digest") else [],
            }
        else:
            existing["first_capture_witness"] = min(
                existing["first_capture_witness"], timestamp
            )
            existing["last_capture_witness"] = max(
                existing["last_capture_witness"], timestamp
            )
            existing["capture_witness_count"] += 1
            existing["query_present_observed"] = (
                existing["query_present_observed"] or meta["query_present"]
            )
            original = item.get("original", "")
            if (
                original
                and original not in existing["source_original_examples"]
                and len(existing["source_original_examples"]) < 3
            ):
                existing["source_original_examples"].append(original)
            digest = item.get("digest")
            if (
                digest
                and digest not in existing["digests"]
                and len(existing["digests"]) < 10
            ):
                existing["digests"].append(digest)

    family_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    first_capture_year_counts: Counter[str] = Counter()
    for row in by_canonical.values():
        family_counts[row["family"]] += 1
        route_counts[row["route_class"]] += 1
        first_year = row["first_capture_witness"][:4]
        if len(first_year) == 4 and first_year.isdigit():
            first_capture_year_counts[first_year] += 1

    inventory_fields = [
        "family", "canonical_url", "path", "route_class",
        "first_capture_witness", "last_capture_witness",
        "capture_witness_count", "query_present_observed",
        "distinct_digest_examples", "source_original_examples",
    ]
    with (out / "normalized_url_inventory.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        writer = csv.DictWriter(fh, fieldnames=inventory_fields)
        writer.writeheader()
        for row in sorted(
            by_canonical.values(), key=lambda x: (x["family"], x["canonical_url"])
        ):
            writer.writerow({
                "family": row["family"],
                "canonical_url": row["canonical_url"],
                "path": row["path"],
                "route_class": row["route_class"],
                "first_capture_witness": row["first_capture_witness"],
                "last_capture_witness": row["last_capture_witness"],
                "capture_witness_count": row["capture_witness_count"],
                "query_present_observed": str(
                    bool(row["query_present_observed"])
                ).lower(),
                "distinct_digest_examples": "|".join(row["digests"]),
                "source_original_examples": "|".join(
                    row["source_original_examples"]
                ),
            })

    planned_frame_complete = (
        completed_host_years == planned_host_years
        and not receipt["errors"]
        and not receipt["transport_holds"]
        and not receipt["page_limit_holds"]
    )
    receipt["summary"] = {
        "planned_host_years": planned_host_years,
        "completed_host_years": completed_host_years,
        "cdx_pages_fetched": len(receipt["pages"]),
        "cdx_capture_witness_rows": len(all_captures),
        "normalized_unique_urls": len(by_canonical),
        "unique_urls_by_family": dict(sorted(family_counts.items())),
        "unique_urls_by_route_class": dict(sorted(route_counts.items())),
        "unique_urls_by_first_capture_year": dict(
            sorted(first_capture_year_counts.items())
        ),
        "rejected_normalization_reasons": dict(
            sorted(rejected_reasons.items())
        ),
        "planned_cdx_frame_complete": planned_frame_complete,
        "domain_era_attribution_closed": False,
        "article_denominator_closed": False,
        "topic_coding_authorized": False,
        "quantitative_language_authorized": False,
    }

    if receipt["errors"]:
        receipt["acquisition_result"] = "ERROR"
    elif receipt["transport_holds"]:
        receipt["acquisition_result"] = "TRANSPORT_HOLD"
    elif receipt["page_limit_holds"]:
        receipt["acquisition_result"] = "PAGE_LIMIT_HOLD"
    else:
        receipt["acquisition_result"] = "ARCHIVE_URL_INVENTORY_ACQUIRED"

    write_json(out / "ACQUISITION_RECEIPT.json", receipt)
    print(json.dumps(
        receipt["summary"]
        | {"acquisition_result": receipt["acquisition_result"]},
        indent=2,
        sort_keys=True,
    ))

    if receipt["errors"]:
        for error in receipt["errors"]:
            print("ERROR", error, file=sys.stderr)
        return 2
    if receipt["transport_holds"]:
        for hold in receipt["transport_holds"]:
            print("TRANSPORT_HOLD", hold, file=sys.stderr)
        return 3
    if receipt["page_limit_holds"]:
        for hold in receipt["page_limit_holds"]:
            print("PAGE_LIMIT_HOLD", hold, file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
