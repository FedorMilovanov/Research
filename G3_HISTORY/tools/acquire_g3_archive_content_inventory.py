#!/usr/bin/env python3
"""Acquire a metadata-only archive URL inventory for historical G3 web properties.

No archived HTML bodies are fetched or stored. The tool queries the Internet Archive
CDX index for text/html captures, preserves capture provenance, normalizes canonical
URLs, and emits route-classification candidates for later denominator adjudication.

Exit contract:
- 0: all planned segments completed with no overflow or transport hold;
- 2: parse/schema/invariant/non-transport defect (fail closed);
- 3: bounded retryable transport failures were exhausted;
- 4: one or more CDX segments reached the configured row cap, so completeness is held.

Important: a successful URL inventory is not yet an article denominator and does not
authorize percentages or topic-prevalence claims.
"""
from __future__ import annotations

import argparse
import calendar
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

UA = "FedorMilovanov-Research-G3-Archive-Census/1.0 (metadata-only; no body fetch)"
CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
RETRY_DELAYS = (2, 6)
DEFAULT_LIMIT = 5000

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


class OverflowHold(RuntimeError):
    """CDX row cap reached; segment completeness cannot be asserted."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def fetch(url: str, *, timeout: int = 60, attempts: int = 3) -> tuple[bytes, dict]:
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


def parse_cdx(data: bytes) -> tuple[list[dict], str]:
    try:
        rows = json.loads(data.decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"CDX response is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(rows, list):
        raise RuntimeError("CDX JSON root is not a list")
    if not rows:
        return [], "VALID_EMPTY_CDX"
    header = rows[0]
    required = {"timestamp", "original", "statuscode", "mimetype", "digest"}
    if not isinstance(header, list) or not required.issubset(set(header)):
        raise RuntimeError(f"CDX response has invalid header: {header!r}")
    captures: list[dict] = []
    for idx, row in enumerate(rows[1:], start=1):
        if not isinstance(row, list) or len(row) != len(header):
            raise RuntimeError(f"CDX row {idx} shape mismatch")
        captures.append(dict(zip(header, row)))
    return captures, "CAPTURES_PRESENT" if captures else "VALID_HEADER_ZERO_ROWS"


def cdx_url(host: str, from_value: str, to_value: str, limit: int) -> str:
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
    ]
    return CDX_ENDPOINT + "?" + urllib.parse.urlencode(params)


def normalize_url(original: str, family: str) -> tuple[str | None, dict]:
    raw = original.strip()
    if not raw:
        return None, {"reason": "empty_original"}
    candidate = raw
    if "://" not in candidate:
        candidate = "http://" + candidate
    try:
        parsed = urllib.parse.urlsplit(candidate)
    except Exception as exc:
        return None, {"reason": "urlsplit_error", "error": repr(exc)}

    host = (parsed.hostname or "").casefold().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    if host != family:
        return None, {"reason": "host_outside_family", "host": host}

    path = parsed.path or "/"
    path = re.sub(r"/{2,}", "/", path)
    path = urllib.parse.unquote(path, errors="replace")
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
    suffix = ""
    leaf = lower.rstrip("/").rsplit("/", 1)[-1] if lower != "/" else ""
    if "." in leaf:
        suffix = "." + leaf.rsplit(".", 1)[-1]
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
    if "/conference/" in lower or "/conferences/" in lower or "/national-conference/" in lower:
        return "conference_page_candidate"
    if "/event/" in lower or "/events/" in lower:
        return "event_page_candidate"
    if DATED_POST_RE.match(lower):
        return "dated_article_candidate"
    if lower == "/":
        return "navigation_or_landing"
    return "article_or_page_candidate"


def query_segment(
    *,
    family: str,
    host: str,
    year: int,
    month: int | None,
    limit: int,
    receipt: dict,
) -> list[dict]:
    if month is None:
        from_value = f"{year}0101"
        to_value = f"{year}1231"
        segment = f"{year}"
    else:
        last_day = calendar.monthrange(year, month)[1]
        from_value = f"{year}{month:02d}01"
        to_value = f"{year}{month:02d}{last_day:02d}"
        segment = f"{year}-{month:02d}"

    url = cdx_url(host, from_value, to_value, limit)
    raw, fetch_meta = fetch(url)
    captures, state = parse_cdx(raw)
    rec = {
        "family": family,
        "host": host,
        "segment": segment,
        "from": from_value,
        "to": to_value,
        "query_state": state,
        "row_count": len(captures),
        "limit": limit,
        "fetch": fetch_meta,
    }
    receipt["segments"].append(rec)
    if len(captures) >= limit:
        raise OverflowHold(
            f"{family} host={host} segment={segment} row_count={len(captures)} limit={limit}"
        )
    for item in captures:
        item["_family"] = family
        item["_host_query"] = host
        item["_segment"] = segment
    return captures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="g3-archive-content-inventory")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument(
        "--sleep-ms",
        type=int,
        default=75,
        help="polite delay between successful CDX queries",
    )
    args = parser.parse_args()

    if args.limit < 100:
        print("ERROR --limit must be >=100", file=sys.stderr)
        return 2
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    receipt = {
        "schema": "g3-archive-content-inventory-v1",
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "metadata_only": True,
        "archived_html_bodies_fetched": False,
        "publication_authorized": False,
        "quantitative_language_authorized": False,
        "negative_result_boundary": (
            "Missing captures, transport failures, archive gaps, or URL classification "
            "must not be converted into evidence that historical content did not exist."
        ),
        "method": {
            "endpoint": CDX_ENDPOINT,
            "filters": ["statuscode:200", "mimetype:text/html"],
            "collapse": "urlkey",
            "adaptive_segmentation": (
                "query each host/year first; if row cap is reached, replace that year "
                "with month-level queries; any month at cap creates OVERFLOW_HOLD"
            ),
            "families": FAMILIES,
            "row_limit": args.limit,
        },
        "segments": [],
        "transport_holds": [],
        "overflow_holds": [],
        "errors": [],
    }

    all_captures: list[dict] = []
    for cfg in FAMILIES:
        family = cfg["family"]
        for host in cfg["hosts"]:
            for year in range(cfg["start_year"], cfg["end_year"] + 1):
                try:
                    year_rows = query_segment(
                        family=family,
                        host=host,
                        year=year,
                        month=None,
                        limit=args.limit,
                        receipt=receipt,
                    )
                    all_captures.extend(year_rows)
                except OverflowHold as year_overflow:
                    print("YEAR_SPLIT", str(year_overflow), file=sys.stderr)
                    for month in range(1, 13):
                        try:
                            month_rows = query_segment(
                                family=family,
                                host=host,
                                year=year,
                                month=month,
                                limit=args.limit,
                                receipt=receipt,
                            )
                            all_captures.extend(month_rows)
                        except OverflowHold as exc:
                            receipt["overflow_holds"].append(str(exc))
                        except TransportHold as exc:
                            receipt["transport_holds"].append(str(exc))
                        except Exception as exc:
                            receipt["errors"].append(
                                f"{family} host={host} {year}-{month:02d}: {exc}"
                            )
                        time.sleep(max(args.sleep_ms, 0) / 1000)
                except TransportHold as exc:
                    receipt["transport_holds"].append(str(exc))
                except Exception as exc:
                    receipt["errors"].append(f"{family} host={host} year={year}: {exc}")
                time.sleep(max(args.sleep_ms, 0) / 1000)

    raw_fields = [
        "family", "host_query", "segment", "timestamp", "original",
        "statuscode", "mimetype", "digest", "length",
    ]
    with (out / "cdx_capture_witnesses.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=raw_fields)
        writer.writeheader()
        for item in sorted(
            all_captures,
            key=lambda x: (x.get("_family", ""), x.get("timestamp", ""), x.get("original", "")),
        ):
            writer.writerow({
                "family": item.get("_family"),
                "host_query": item.get("_host_query"),
                "segment": item.get("_segment"),
                "timestamp": item.get("timestamp"),
                "original": item.get("original"),
                "statuscode": item.get("statuscode"),
                "mimetype": item.get("mimetype"),
                "digest": item.get("digest"),
                "length": item.get("length"),
            })

    by_canonical: dict[str, dict] = {}
    family_counts: Counter[str] = Counter()
    rejected_reasons: Counter[str] = Counter()

    for item in all_captures:
        family = item["_family"]
        canonical, meta = normalize_url(item.get("original", ""), family)
        if canonical is None:
            rejected_reasons[meta.get("reason", "unknown")] += 1
            continue
        route_class = classify_route(meta["path"])

        existing = by_canonical.get(canonical)
        timestamp = item.get("timestamp", "")
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
            if original and original not in existing["source_original_examples"] and len(existing["source_original_examples"]) < 3:
                existing["source_original_examples"].append(original)
            digest = item.get("digest")
            if digest and digest not in existing["digests"] and len(existing["digests"]) < 10:
                existing["digests"].append(digest)

    unique_class_counts: Counter[str] = Counter()
    for row in by_canonical.values():
        unique_class_counts[row["route_class"]] += 1
        family_counts[row["family"]] += 1

    inventory_fields = [
        "family", "canonical_url", "path", "route_class",
        "first_capture_witness", "last_capture_witness",
        "capture_witness_count", "query_present_observed",
        "distinct_digest_examples", "source_original_examples",
    ]
    with (out / "normalized_url_inventory.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=inventory_fields)
        writer.writeheader()
        for row in sorted(by_canonical.values(), key=lambda x: (x["family"], x["canonical_url"])):
            writer.writerow({
                "family": row["family"],
                "canonical_url": row["canonical_url"],
                "path": row["path"],
                "route_class": row["route_class"],
                "first_capture_witness": row["first_capture_witness"],
                "last_capture_witness": row["last_capture_witness"],
                "capture_witness_count": row["capture_witness_count"],
                "query_present_observed": str(bool(row["query_present_observed"])).lower(),
                "distinct_digest_examples": "|".join(row["digests"]),
                "source_original_examples": "|".join(row["source_original_examples"]),
            })

    denominator_complete = not (
        receipt["errors"] or receipt["transport_holds"] or receipt["overflow_holds"]
    )
    receipt["summary"] = {
        "cdx_capture_witness_rows": len(all_captures),
        "normalized_unique_urls": len(by_canonical),
        "unique_urls_by_family": dict(sorted(family_counts.items())),
        "unique_urls_by_route_class": dict(sorted(unique_class_counts.items())),
        "rejected_normalization_reasons": dict(sorted(rejected_reasons.items())),
        "denominator_complete_for_planned_cdx_frame": denominator_complete,
        "article_denominator_closed": False,
        "topic_coding_authorized": False,
        "quantitative_language_authorized": False,
    }
    if receipt["errors"]:
        receipt["acquisition_result"] = "ERROR"
    elif receipt["transport_holds"]:
        receipt["acquisition_result"] = "TRANSPORT_HOLD"
    elif receipt["overflow_holds"]:
        receipt["acquisition_result"] = "OVERFLOW_HOLD"
    else:
        receipt["acquisition_result"] = "ARCHIVE_URL_INVENTORY_ACQUIRED"

    write_json(out / "ACQUISITION_RECEIPT.json", receipt)

    print(json.dumps(receipt["summary"] | {
        "acquisition_result": receipt["acquisition_result"]
    }, indent=2, sort_keys=True))

    if receipt["errors"]:
        for error in receipt["errors"]:
            print("ERROR", error, file=sys.stderr)
        return 2
    if receipt["transport_holds"]:
        for hold in receipt["transport_holds"]:
            print("TRANSPORT_HOLD", hold, file=sys.stderr)
        return 3
    if receipt["overflow_holds"]:
        for hold in receipt["overflow_holds"]:
            print("OVERFLOW_HOLD", hold, file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
