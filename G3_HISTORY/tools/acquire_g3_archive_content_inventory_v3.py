#!/usr/bin/env python3
"""Acquire metadata-only Wayback CDX URL inventory for historical G3 domains.

V3 uses one bounded era query per explicit host and CDX resume-key pagination.
No archived HTML bodies are fetched or stored.

Exit contract:
- 0: every planned era scan reached terminal CDX exhaustion;
- 2: parse/schema/invariant/non-transport defect (fail closed);
- 3: bounded retryable transport failures were exhausted;
- 4: resume-page safety bound reached before exhaustion.

Even a successful inventory remains discovery evidence. Domain-era attribution,
article/page adjudication, topic coding, and quantitative publication language
remain separate gates.
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

UA = "FedorMilovanov-Research-G3-Archive-Census/3.0 (metadata-only; no body fetch)"
CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
RETRY_DELAYS = (2, 6)
DEFAULT_LIMIT = 1000
DEFAULT_MAX_PAGES = 30

FAMILIES = (
    {
        "family": "g3conference.com",
        "hosts": ("g3conference.com", "www.g3conference.com"),
        "from": "20110101",
        "to": "20201231",
    },
    {
        "family": "g3min.org",
        "hosts": ("g3min.org", "www.g3min.org"),
        "from": "20200101",
        "to": "20261231",
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
    pass


class PageLimitHold(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def fetch(url: str, *, timeout: int = 60, attempts: int = 3) -> tuple[bytes, dict]:
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,*/*"})
        started = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                return data, {
                    "requested_url": url,
                    "final_url": response.geturl(),
                    "status": getattr(response, "status", None),
                    "content_type": response.headers.get("Content-Type"),
                    "bytes": len(data),
                    "sha256": sha256_bytes(data),
                    "elapsed_seconds": round(time.time() - started, 3),
                    "attempt": attempt,
                    "max_attempts": attempts,
                }
        except urllib.error.HTTPError as exc:
            body = exc.read()
            msg = (
                f"HTTP {exc.code} {exc.reason} url={url} body_sha256={sha256_bytes(body)} "
                f"bytes={len(body)} attempt={attempt}/{attempts}"
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
        print("TRANSIENT_RETRY", f"attempt={attempt}/{attempts}", f"sleep={delay}s", url, file=sys.stderr)
        time.sleep(delay)
    raise RuntimeError(f"fetch exhausted unexpectedly url={url}")


def parse_page(data: bytes) -> tuple[list[dict], str | None, str]:
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

    resume_key = None
    body = rows[1:]
    if len(body) >= 2 and body[-2] == []:
        marker = body[-1]
        if not isinstance(marker, list) or len(marker) != 1 or not isinstance(marker[0], str) or not marker[0]:
            raise RuntimeError(f"invalid CDX resume marker: {marker!r}")
        resume_key = marker[0]
        body = body[:-2]

    captures = []
    for idx, row in enumerate(body, start=1):
        if not isinstance(row, list) or len(row) != len(header):
            raise RuntimeError(f"CDX row {idx} shape mismatch")
        captures.append(dict(zip(header, row)))
    if resume_key and not captures:
        raise RuntimeError("resume key returned with zero data rows")
    state = "CAPTURES_PRESENT_MORE" if resume_key else ("CAPTURES_PRESENT_TERMINAL" if captures else "VALID_HEADER_ZERO_ROWS")
    return captures, resume_key, state


def build_url(host: str, start: str, end: str, limit: int, resume_key: str | None) -> str:
    params = [
        ("url", f"{host}/*"),
        ("from", start),
        ("to", end),
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


def scan_era(*, family: str, host: str, start: str, end: str, limit: int, max_pages: int, sleep_ms: int, receipt: dict) -> list[dict]:
    resume_key = None
    seen_keys: set[str] = set()
    collected: list[dict] = []
    for page_index in range(1, max_pages + 1):
        raw, fetch_meta = fetch(build_url(host, start, end, limit, resume_key))
        captures, next_key, state = parse_page(raw)
        receipt["pages"].append({
            "family": family,
            "host": host,
            "from": start,
            "to": end,
            "page_index": page_index,
            "query_state": state,
            "row_count": len(captures),
            "limit": limit,
            "resume_key_in": resume_key,
            "resume_key_out": next_key,
            "fetch": fetch_meta,
        })
        for item in captures:
            item["_family"] = family
            item["_host_query"] = host
            item["_era_from"] = start
            item["_era_to"] = end
            item["_page_index"] = page_index
        collected.extend(captures)
        if not next_key:
            return collected
        if next_key in seen_keys:
            raise RuntimeError(f"CDX resume-key cycle family={family} host={host}")
        seen_keys.add(next_key)
        resume_key = next_key
        time.sleep(max(sleep_ms, 0) / 1000)
    raise PageLimitHold(f"{family} host={host} exceeded max_pages={max_pages} before terminal exhaustion")


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
    return f"https://{family}{path}", {
        "path": path,
        "query_present": bool(parsed.query),
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
    if "/conference/" in lower or "/conferences/" in lower or "/national-conference/" in lower:
        return "conference_page_candidate"
    if "/event/" in lower or "/events/" in lower:
        return "event_page_candidate"
    if DATED_POST_RE.match(lower):
        return "dated_article_candidate"
    return "article_or_page_candidate"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="g3-archive-content-inventory")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--sleep-ms", type=int, default=75)
    args = parser.parse_args()
    if not 100 <= args.limit <= 5000:
        print("ERROR --limit must be between 100 and 5000", file=sys.stderr)
        return 2
    if not 1 <= args.max_pages <= 500:
        print("ERROR --max-pages must be between 1 and 500", file=sys.stderr)
        return 2

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "g3-archive-content-inventory-v3",
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "metadata_only": True,
        "archived_html_bodies_fetched": False,
        "publication_authorized": False,
        "domain_era_attribution_closed": False,
        "article_denominator_closed": False,
        "topic_coding_authorized": False,
        "quantitative_language_authorized": False,
        "negative_result_boundary": "Missing captures, transport failure, archive gaps, classification, or domain-era uncertainty are not evidence that historical content did not exist.",
        "method": {
            "endpoint": CDX_ENDPOINT,
            "filters": ["statuscode:200", "mimetype:text/html"],
            "collapse": "urlkey",
            "pagination": "showResumeKey=true + resumeKey until terminal exhaustion",
            "query_frame": "four explicit host-era scans: root/www for g3conference.com and g3min.org",
            "families": FAMILIES,
            "row_limit": args.limit,
            "max_pages_per_host_era": args.max_pages,
        },
        "pages": [],
        "transport_holds": [],
        "overflow_holds": [],
        "errors": [],
    }

    planned = sum(len(cfg["hosts"]) for cfg in FAMILIES)
    completed = 0
    captures: list[dict] = []
    for cfg in FAMILIES:
        for host in cfg["hosts"]:
            try:
                captures.extend(scan_era(
                    family=cfg["family"], host=host, start=cfg["from"], end=cfg["to"],
                    limit=args.limit, max_pages=args.max_pages, sleep_ms=args.sleep_ms, receipt=receipt,
                ))
                completed += 1
            except PageLimitHold as exc:
                receipt["overflow_holds"].append(str(exc))
            except TransportHold as exc:
                receipt["transport_holds"].append(str(exc))
            except Exception as exc:
                receipt["errors"].append(f"{cfg['family']} host={host}: {exc}")
            time.sleep(max(args.sleep_ms, 0) / 1000)

    with (out / "cdx_capture_witnesses.csv").open("w", encoding="utf-8", newline="") as fh:
        fields = ["family", "host_query", "era_from", "era_to", "page_index", "timestamp", "original", "statuscode", "mimetype", "digest", "length"]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for item in sorted(captures, key=lambda x: (x.get("_family", ""), x.get("timestamp", ""), x.get("original", ""))):
            writer.writerow({
                "family": item.get("_family"), "host_query": item.get("_host_query"),
                "era_from": item.get("_era_from"), "era_to": item.get("_era_to"),
                "page_index": item.get("_page_index"), "timestamp": item.get("timestamp"),
                "original": item.get("original"), "statuscode": item.get("statuscode"),
                "mimetype": item.get("mimetype"), "digest": item.get("digest"), "length": item.get("length"),
            })

    by_url: dict[str, dict] = {}
    rejected: Counter[str] = Counter()
    for item in captures:
        canonical, meta = normalize_url(item.get("original", ""), item["_family"])
        if canonical is None:
            rejected[meta.get("reason", "unknown")] += 1
            continue
        ts = item.get("timestamp", "")
        row = by_url.get(canonical)
        if row is None:
            by_url[canonical] = {
                "family": item["_family"], "canonical_url": canonical, "path": meta["path"],
                "route_class": classify_route(meta["path"]), "first_capture_witness": ts,
                "last_capture_witness": ts, "capture_witness_count": 1,
                "query_present_observed": meta["query_present"],
                "source_original_examples": [item.get("original", "")],
                "digests": [item.get("digest")] if item.get("digest") else [],
            }
        else:
            row["first_capture_witness"] = min(row["first_capture_witness"], ts)
            row["last_capture_witness"] = max(row["last_capture_witness"], ts)
            row["capture_witness_count"] += 1
            row["query_present_observed"] = row["query_present_observed"] or meta["query_present"]
            original = item.get("original", "")
            if original and original not in row["source_original_examples"] and len(row["source_original_examples"]) < 3:
                row["source_original_examples"].append(original)
            digest = item.get("digest")
            if digest and digest not in row["digests"] and len(row["digests"]) < 10:
                row["digests"].append(digest)

    with (out / "normalized_url_inventory.csv").open("w", encoding="utf-8", newline="") as fh:
        fields = ["family", "canonical_url", "path", "route_class", "first_capture_witness", "last_capture_witness", "capture_witness_count", "query_present_observed", "distinct_digest_examples", "source_original_examples"]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in sorted(by_url.values(), key=lambda x: (x["family"], x["canonical_url"])):
            writer.writerow({
                **{k: row[k] for k in fields[:7]},
                "query_present_observed": str(bool(row["query_present_observed"])).lower(),
                "distinct_digest_examples": "|".join(row["digests"]),
                "source_original_examples": "|".join(row["source_original_examples"]),
            })

    family_counts = Counter(row["family"] for row in by_url.values())
    route_counts = Counter(row["route_class"] for row in by_url.values())
    first_year_counts = Counter(
        row["first_capture_witness"][:4] for row in by_url.values()
        if len(row["first_capture_witness"]) >= 4 and row["first_capture_witness"][:4].isdigit()
    )
    frame_complete = completed == planned and not receipt["errors"] and not receipt["transport_holds"] and not receipt["overflow_holds"]
    receipt["summary"] = {
        "planned_host_era_scans": planned,
        "completed_host_era_scans": completed,
        "cdx_pages_fetched": len(receipt["pages"]),
        "cdx_capture_witness_rows": len(captures),
        "normalized_unique_urls": len(by_url),
        "unique_urls_by_family": dict(sorted(family_counts.items())),
        "unique_urls_by_route_class": dict(sorted(route_counts.items())),
        "unique_urls_by_first_capture_year": dict(sorted(first_year_counts.items())),
        "rejected_normalization_reasons": dict(sorted(rejected.items())),
        "denominator_complete_for_planned_cdx_frame": frame_complete,
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
    print(json.dumps(receipt["summary"] | {"acquisition_result": receipt["acquisition_result"]}, indent=2, sort_keys=True))

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
