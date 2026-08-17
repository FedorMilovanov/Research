#!/usr/bin/env python3
"""Classify refined DEAD URLs into actionable source failures vs parser/ledger noise."""
from __future__ import annotations

import csv
import html
import json
import os
import re
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import requests

ROOT = Path(os.environ.get("AUDIT_OUT", "total-audit-output"))
SRC = ROOT / "refined" / "refined_source_url_audit.csv"
OUT = ROOT / "dead-url-classification"
OUT.mkdir(parents=True, exist_ok=True)
UA = "TheLegendaryPoet-DeadSourceClassifier/2026-07-30"

TECH_PATH_RE = re.compile(
    r"(^|/)(scripts?|tests?|fixtures?|audit|incoming|archive|stale-incoming|_build-tools|docs/design-references)(/|$)",
    re.I,
)
SOURCE_PATH_RE = re.compile(
    r"source|sources|research|bibliograph|ledger|primary|manuscript|rights|"
    r"источник|литератур|библиограф|рукопис|архив",
    re.I,
)
TEMPLATE_RE = re.compile(r"\$\{?|\{\{|\{[A-Za-z_][A-Za-z0-9_]*|%[A-Z_]+%|<[^>]+>|\*\.")
CSV_METADATA_SUFFIX_RE = re.compile(r",(?:Official|Contemporary|physical|reproduced|\d{1,5})$", re.I)
METADATA_DOMAINS = {"samizdat.library.utoronto.ca", "almanah.bogomysliye.com", "repository.up.ac.za"}
LEGACY_PROJECT_DOMAINS = {"raw.githubusercontent.com", "github.com"}
BAPTIST_COLLECTIONS = (
    (re.compile(r"utren(?:nyaya|niaia)[-_]?zvezda", re.I), "https://baptist.org.ru/izdania/utrenniiazvezda"),
    (re.compile(r"bratsk(?:iy|ii)[-_]?vestnik", re.I), "https://baptist.org.ru/izdania/bratskiivestnik"),
    (re.compile(r"khristianin|hristianin", re.I), "https://baptist.org.ru/izdania/hristianin"),
    (re.compile(r"(?:^|[/_-])baptist[-_]?(?:18|19|20)\d{2}", re.I), "https://baptist.org.ru/izdania/baptist"),
)
_COLLECTION_CACHE: dict[str, dict] = {}


def read_rows() -> list[dict[str, str]]:
    with SRC.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r["status"] == "DEAD"]


def write_csv(name: str, rows: list[dict]) -> None:
    fields = [
        "classification", "original_url", "cleaned_url", "recheck_status", "recheck_code",
        "final_url", "domain", "priority", "occurrences", "repos", "example_paths", "reason", "error",
    ]
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def unbalanced(url: str) -> bool:
    return url.count("(") != url.count(")") or url.count("[") != url.count("]")


def clean_metadata_suffix(url: str, domain: str) -> tuple[str, str]:
    value = html.unescape(url).strip()
    metadata_match = CSV_METADATA_SUFFIX_RE.search(value)
    if metadata_match:
        return value[:metadata_match.start()], "comma-separated ledger metadata removed"
    if domain in METADATA_DOMAINS and "," in value:
        return value.split(",", 1)[0], "comma-separated ledger metadata removed"
    if ";Telegram" in value:
        return value.split(";", 1)[0], "semicolon label removed"
    return value, ""


def technical_only(paths: str) -> bool:
    items = [p.strip() for p in paths.split("|") if p.strip()]
    return bool(items) and all(TECH_PATH_RE.search(p) for p in items)


def root_only(url: str) -> bool:
    try:
        path = urlsplit(url).path
        return path in {"", "/"}
    except Exception:
        return False


def https_upgrade(url: str) -> str:
    try:
        parts = urlsplit(url)
        if parts.scheme == "http":
            return urlunsplit(("https", parts.netloc, parts.path, parts.query, parts.fragment))
    except Exception:
        pass
    return url


def check(url: str) -> dict:
    headers = {"User-Agent": UA}
    attempts = [url]
    upgraded = https_upgrade(url)
    if upgraded != url:
        attempts.append(upgraded)
    last = {"status": "REQUEST_ERROR", "code": 0, "final_url": "", "error": "not attempted"}
    for attempt in attempts:
        started = time.monotonic()
        try:
            r = requests.get(attempt, headers=headers, timeout=(7, 18), allow_redirects=True, stream=True)
            code = int(r.status_code)
            final = r.url
            r.close()
            if 200 <= code < 400:
                status = "OK"
            elif code in {401, 403, 429, 451}:
                status = "RESTRICTED"
            elif code in {404, 410}:
                status = "DEAD"
            elif 500 <= code < 600:
                status = "SERVER_ERROR"
            else:
                status = "HTTP_ERROR"
            last = {"status": status, "code": code, "final_url": final, "error": "", "seconds": round(time.monotonic()-started, 3)}
            if status in {"OK", "RESTRICTED"}:
                return last
        except Exception as exc:
            last = {"status": "REQUEST_ERROR", "code": 0, "final_url": "", "error": str(exc)[:300], "seconds": round(time.monotonic()-started, 3)}
    return last


def recover_baptist_collection(url: str, domain: str) -> tuple[str, dict | None]:
    if domain != "baptist.org.ru":
        return "", None
    try:
        path = urlsplit(url).path
    except Exception:
        return "", None
    # The old `_service` PDF endpoints were retired, while the official Union
    # still exposes issue indexes for these historical periodicals. Treat a
    # live collection index as recoverable institutional custody, not as a
    # vanished source. Exact dead deep links remain visible in the full CSV.
    if "/_service/" not in path.lower():
        return "", None
    for pattern, collection_url in BAPTIST_COLLECTIONS:
        if pattern.search(path):
            result = _COLLECTION_CACHE.get(collection_url)
            if result is None:
                result = check(collection_url)
                _COLLECTION_CACHE[collection_url] = result
            return collection_url, result
    return "", None


def main() -> int:
    classified: list[dict] = []
    for row in read_rows():
        original = row["url"]
        domain = row["domain"]
        base = {
            "original_url": original,
            "cleaned_url": original,
            "domain": domain,
            "priority": row["priority"],
            "occurrences": row["occurrences"],
            "repos": row["repos"],
            "example_paths": row["example_paths"],
            "recheck_status": "NOT_RECHECKED",
            "recheck_code": 0,
            "final_url": "",
            "error": "",
        }

        if TEMPLATE_RE.search(original):
            classified.append({**base, "classification": "TEMPLATE_FALSE_POSITIVE", "reason": "template/variable URL"})
            continue
        if unbalanced(original):
            classified.append({**base, "classification": "TRUNCATED_URL_FALSE_POSITIVE", "reason": "unbalanced brackets/parentheses from Markdown or CSV extraction"})
            continue
        if technical_only(row["example_paths"]):
            classified.append({**base, "classification": "TECHNICAL_OR_ARCHIVED_REFERENCE", "reason": "all occurrences are scripts/audit/incoming/archive/design references"})
            continue
        if root_only(original):
            classified.append({**base, "classification": "ROOT_OR_SERVICE_ENDPOINT_NOT_SOURCE_ITEM", "reason": "domain root/service endpoint is not an item citation"})
            continue
        if domain in LEGACY_PROJECT_DOMAINS and "FedorMilovanov/gospod-bog" in original:
            classified.append({**base, "classification": "LEGACY_PROJECT_REFERENCE", "reason": "old project/repository architecture reference, not external research source"})
            continue

        cleaned, clean_reason = clean_metadata_suffix(original, domain)
        result = check(cleaned)
        if result["status"] == "OK":
            classification = "RECOVERED_AFTER_CLEAN_OR_HTTPS"
        elif result["status"] == "RESTRICTED":
            classification = "LIVE_BUT_RESTRICTED"
        elif result["status"] in {"SERVER_ERROR", "REQUEST_ERROR"}:
            classification = "TEMPORARY_OR_NETWORK_RETRY"
        elif result["status"] == "DEAD":
            collection_url, collection_result = recover_baptist_collection(cleaned, domain)
            if collection_result and collection_result["status"] in {"OK", "RESTRICTED"}:
                classification = "RECOVERABLE_OFFICIAL_COLLECTION_MIGRATION"
                clean_reason = (
                    f"retired deep PDF endpoint; official collection index is {collection_result['status']}: {collection_url}"
                )
                result = {
                    **result,
                    "final_url": collection_result.get("final_url") or collection_url,
                }
            elif SOURCE_PATH_RE.search(row["example_paths"]):
                classification = "TRUE_DEAD_SOURCE_REPAIR"
            else:
                classification = "DEAD_NON_SOURCE_REFERENCE_REVIEW"
        else:
            classification = "OTHER_HTTP_REVIEW"
        classified.append({
            **base,
            "classification": classification,
            "cleaned_url": cleaned,
            "recheck_status": result["status"],
            "recheck_code": result["code"],
            "final_url": result["final_url"],
            "reason": clean_reason or "rechecked after noise classification",
            "error": result["error"],
        })
        time.sleep(0.15)

    classified.sort(key=lambda r: (r["classification"], -int(r["priority"]), r["domain"], r["original_url"]))
    write_csv("dead_url_classification.csv", classified)
    true_dead = [r for r in classified if r["classification"] == "TRUE_DEAD_SOURCE_REPAIR"]
    write_csv("true_dead_source_repair_queue.csv", true_dead)
    counts = Counter(r["classification"] for r in classified)
    report = [
        "# DEAD URL classification",
        "",
        f"- raw refined-DEAD rows: **{len(classified)}**",
        f"- true dead source repair candidates after recheck: **{len(true_dead)}**",
        f"- recoverable official collection migrations: **{counts['RECOVERABLE_OFFICIAL_COLLECTION_MIGRATION']}**",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    for key, value in counts.most_common():
        report.append(f"| `{key}` | {value} |")
    report += [
        "",
        "`TRUE_DEAD_SOURCE_REPAIR` is still a repair queue, not proof that the cited claim is false. Replace with a current institutional landing page, archived copy, DOI, catalog record or a different primary witness; do not silently delete evidence.",
        "",
        "`RECOVERABLE_OFFICIAL_COLLECTION_MIGRATION` means the old deep item endpoint is retired but a live official institutional issue index was verified during this run. The old URL remains recorded in the full classification CSV for eventual deep-link normalization.",
    ]
    (OUT / "DEAD_URL_CLASSIFICATION.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (OUT / "summary.json").write_text(json.dumps({"total": len(classified), "counts": dict(counts)}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("DEAD_URL_CLASSIFICATION_COMPLETE", json.dumps(dict(counts), ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
