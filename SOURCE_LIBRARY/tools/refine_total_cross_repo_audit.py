#!/usr/bin/env python3
"""Refine the raw four-repository audit into actionable, low-noise queues."""
from __future__ import annotations

import csv
import html
import json
import os
import re
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit

import requests

RAW = Path(os.environ.get("AUDIT_OUT", "total-audit-output"))
OUT = RAW / "refined"
OUT.mkdir(parents=True, exist_ok=True)

NOISE_DOMAINS = {
    "127.0.0.1", "localhost", "0.0.0.0", "schema.org", "www.schema.org",
    "w3.org", "www.w3.org", "registry.npmjs.org", "npmjs.com",
    "opencollective.com", "cdn.jsdelivr.net", "fonts.googleapis.com",
    "fonts.gstatic.com", "mc.yandex.ru", "mc.yandex.com",
}
OWN_DOMAINS = {"gospod-bog.ru", "www.gospod-bog.ru", "thelegendarypoet.ru", "www.thelegendarypoet.ru"}
SOURCE_PATH_RE = re.compile(
    r"source|research|bibliograph|rights|provenance|manuscript|archive|audit|"
    r"источник|литератур|библиограф|прав|лиценз|рукопис|архив",
    re.I,
)
CONTENT_PATH_RE = re.compile(
    r"(^|/)(articles?|biografii|hard-texts|baptisty-rossii|content|docs|src/data)(/|$)",
    re.I,
)
ARCHIVE_PATH_RE = re.compile(r"(^|/)(archive|incoming|stale-incoming|_build-tools)(/|$)", re.I)
PROCESS_DOC_RE = re.compile(r"migration|session.crash|constraints|priority|changelog|readme", re.I)
STATUS_SUFFIX_RE = re.compile(r",(?=[A-Z][A-Z0-9_ -]{2,}(?:,|$))")
TEMPLATE_RE = re.compile(r"\$\{|\{\{|%BASE_URL%|<[^>]+>|\[\*\]|\*\.")
LOCAL_RE = re.compile(r"^https?://(?:127\.0\.0\.1|localhost|0\.0\.0\.0)(?::\d+)?", re.I)
DOC_EXAMPLE_RE = re.compile(r"(?:^|/)(docs?|examples?|fixtures?|tests?|qa|scripts?)(?:/|$)", re.I)
PUBLISH_ASSET_RE = re.compile(r"^public/images/", re.I)


def read_csv(name: str) -> list[dict[str, str]]:
    with (RAW / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    path = OUT / name
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def clean_url(raw: str) -> tuple[str, str]:
    value = html.unescape((raw or "").strip())
    reason = ""
    match = STATUS_SUFFIX_RE.search(value)
    if match:
        value = value[: match.start()]
        reason = "cut_csv_status_suffix"
    # Common unquoted source ledgers append a semicolon + human label.
    if ";" in value:
        left, right = value.split(";", 1)
        if re.search(r"[А-Яа-я ]", right) and not re.search(r"[?&][^=]+=", value):
            value = left
            reason = reason or "cut_semicolon_label"
    value = value.rstrip(".,;:!?\")'»”]")
    return value, reason


def parse_domain(url: str) -> tuple[str, str]:
    try:
        parts = urlsplit(url)
        if parts.scheme not in {"http", "https"} or not parts.netloc:
            return "", "invalid_scheme_or_host"
        return parts.netloc.lower().removeprefix("www."), ""
    except ValueError as exc:
        return "", f"parse_error:{exc}"


def occurrence_priority(repo: str, path: str, domain: str) -> int:
    score = 0
    if SOURCE_PATH_RE.search(path):
        score += 6
    if CONTENT_PATH_RE.search(path):
        score += 3
    if repo == "Research":
        score += 2
    if domain.endswith((".edu", ".ac.uk", ".gov", ".gov.uk")):
        score += 4
    if any(token in domain for token in (
        "ran.ru", "imli.ru", "pushkinskijdom.ru", "rusneb.ru", "rsl.ru", "nlr.ru",
        "prlib.ru", "loc.gov", "nypl.org", "archive.org", "wikimedia.org", "commons.ptsem.edu",
        "prdl.org", "ccel.org", "manuscriptroom.com", "csntm.org", "vatlib.it",
        "deadseascrolls.org.il", "qumran-digital.org", "github.com", "rvb.ru", "feb-web.ru",
    )):
        score += 5
    if ARCHIVE_PATH_RE.search(path):
        score -= 5
    if DOC_EXAMPLE_RE.search(path):
        score -= 2
    return score


def audit_url(url: str) -> dict:
    headers = {"User-Agent": "TheLegendaryPoet-RefinedSourceAudit/2026-07-30"}
    started = time.monotonic()
    try:
        response = requests.get(url, headers=headers, timeout=(5, 10), allow_redirects=True, stream=True)
        code = int(response.status_code)
        final_url = response.url
        ctype = response.headers.get("content-type", "")[:180]
        response.close()
        if 200 <= code < 400:
            status = "OK"
        elif code in {401, 403, 429, 451}:
            status = "RESTRICTED_OR_RATE_LIMITED"
        elif code in {404, 410}:
            status = "DEAD"
        elif 500 <= code < 600:
            status = "SERVER_ERROR"
        else:
            status = "HTTP_ERROR"
        return {
            "url": url, "status": status, "code": code, "final_url": final_url,
            "content_type": ctype, "seconds": round(time.monotonic() - started, 3), "error": "",
        }
    except Exception as exc:
        return {
            "url": url, "status": "REQUEST_ERROR", "code": 0, "final_url": "",
            "content_type": "", "seconds": round(time.monotonic() - started, 3),
            "error": str(exc)[:320],
        }


def classify_missing(row: dict) -> str:
    repo = row["repo"]
    path = row["source_path"]
    target = row["target"]
    if TEMPLATE_RE.search(target):
        return "TEMPLATE_OR_PATTERN_FALSE_POSITIVE"
    if repo == "AuditRepo" and ARCHIVE_PATH_RE.search(path):
        return "ARCHIVED_EVIDENCE_NO_FIX"
    if DOC_EXAMPLE_RE.search(path) and re.search(r"foo|example|sample", target, re.I):
        return "DOCUMENTATION_EXAMPLE_NO_FIX"
    if target.startswith("/"):
        return "DYNAMIC_SITE_ROUTE_REVIEW"
    if path.endswith((".astro", ".tsx", ".ts", ".js", ".mjs")) and target.startswith(("../", "./")):
        return "SOURCE_RELATIVE_ASSET_OR_IMPORT_REVIEW"
    if target.lower().endswith((".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".pdf", ".zip", ".html")):
        return "LIKELY_MISSING_FILE_REFERENCE"
    return "MANUAL_REVIEW"


def classify_editorial(row: dict) -> str:
    path = row["path"]
    if path.endswith(".astro"):
        return "TECHNICAL_WRAPPER_FALSE_POSITIVE"
    if PROCESS_DOC_RE.search(path):
        return "PROCESS_DOCUMENT_NO_BIBLIOGRAPHY_REQUIRED"
    if "baptisty-rossii/research/75-orthodoxy-baptists" in path:
        return "GENUINE_RESEARCH_SOURCE_GAP"
    return "MANUAL_REVIEW"


def classify_asset(row: dict) -> str:
    repo, path = row["repo"], row["path"]
    if repo == "TheLegendaryPoet" and PUBLISH_ASSET_RE.search(path):
        return "PUBLICATION_ASSET_ADD_PROVENANCE_LEDGER"
    if repo == "AuditRepo" and "/evidence/" in path:
        return "AUDIT_EVIDENCE_ADD_CAPTURE_METADATA"
    if repo == "Research" and path.endswith(".zip"):
        return "RESEARCH_PACKAGE_ADD_PACKAGE_PROVENANCE"
    return "MANUAL_REVIEW"


def main() -> int:
    occurrences = read_csv("url_occurrences.csv")
    missing = read_csv("missing_local_links.csv")
    editorial = read_csv("editorial_content_without_sources.csv")
    assets = read_csv("assets_without_provenance.csv")
    duplicates = read_csv("duplicate_files.csv")

    grouped: dict[str, dict] = {}
    malformed: list[dict] = []
    for row in occurrences:
        clean, clean_note = clean_url(row["url"])
        domain, parse_error = parse_domain(clean)
        if parse_error or TEMPLATE_RE.search(clean) or LOCAL_RE.search(clean):
            malformed.append({**row, "clean_url": clean, "classification": parse_error or "template_or_local", "clean_note": clean_note})
            continue
        if domain in NOISE_DOMAINS or domain in OWN_DOMAINS:
            continue
        if domain.endswith("yandex.ru") or domain.endswith("yandex.com"):
            continue
        key = clean
        entry = grouped.setdefault(key, {
            "url": clean, "domain": domain, "occurrences": 0, "repos": set(),
            "paths": [], "priority": -999,
        })
        entry["occurrences"] += 1
        entry["repos"].add(row["repo"])
        if row["path"] not in entry["paths"] and len(entry["paths"]) < 8:
            entry["paths"].append(row["path"])
        entry["priority"] = max(entry["priority"], occurrence_priority(row["repo"], row["path"], domain))

    candidates = []
    for entry in grouped.values():
        candidates.append({
            "url": entry["url"], "domain": entry["domain"],
            "occurrences": entry["occurrences"], "repos": ",".join(sorted(entry["repos"])),
            "example_paths": " | ".join(entry["paths"]), "priority": entry["priority"],
        })
    candidates.sort(key=lambda r: (-int(r["priority"]), -int(r["occurrences"]), r["url"]))

    cap = int(os.environ.get("REFINED_URL_AUDIT_CAP", "2500"))
    selected = candidates[:cap]
    selected_urls = [r["url"] for r in selected]
    results: list[dict] = []
    workers = int(os.environ.get("REFINED_URL_AUDIT_WORKERS", "36"))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(audit_url, url): url for url in selected_urls}
        for index, future in enumerate(as_completed(futures), 1):
            results.append(future.result())
            if index % 100 == 0:
                print(f"refined URL audit: {index}/{len(selected_urls)}", flush=True)
    result_by_url = {r["url"]: r for r in results}
    url_rows = []
    for item in selected:
        url_rows.append({**item, **result_by_url[item["url"]]})
    url_rows.sort(key=lambda r: (r["status"] != "DEAD", r["status"], -int(r["priority"]), -int(r["occurrences"]), r["url"]))

    missing_rows = [{**row, "classification": classify_missing(row)} for row in missing]
    editorial_rows = [{**row, "classification": classify_editorial(row)} for row in editorial]
    asset_rows = [{**row, "classification": classify_asset(row)} for row in assets]

    # Duplicate classification is conservative: only flag same-repository live-path groups for cleanup.
    dup_groups: dict[str, list[dict]] = defaultdict(list)
    for row in duplicates:
        dup_groups[row["sha256"]].append(row)
    duplicate_summary = []
    for sha, items in dup_groups.items():
        repos = {i["repo"] for i in items}
        archived = all(ARCHIVE_PATH_RE.search(i["path"]) for i in items)
        if archived:
            classification = "ARCHIVED_EVIDENCE_DUPLICATION_NO_URGENT_FIX"
        elif len(repos) > 1:
            classification = "CROSS_REPO_COPY_REVIEW"
        else:
            classification = "SAME_REPO_DUPLICATE_REVIEW"
        duplicate_summary.append({
            "sha256": sha, "copies": len(items), "repos": ",".join(sorted(repos)),
            "size_each": items[0].get("size", ""), "classification": classification,
            "paths": " | ".join(f"{i['repo']}:{i['path']}" for i in items),
        })

    write_csv("refined_source_url_audit.csv", url_rows, [
        "url", "domain", "status", "code", "final_url", "content_type", "seconds", "error",
        "priority", "occurrences", "repos", "example_paths",
    ])
    write_csv("excluded_or_malformed_url_occurrences.csv", malformed, [
        "repo", "path", "url", "clean_url", "classification", "clean_note",
    ])
    write_csv("classified_missing_local_links.csv", missing_rows, [
        "repo", "source_path", "target", "resolved_candidate", "classification",
    ])
    write_csv("classified_editorial_source_gaps.csv", editorial_rows, [
        "repo", "path", "size_bytes", "reason", "classification",
    ])
    write_csv("classified_asset_provenance_gaps.csv", asset_rows, [
        "repo", "path", "size_bytes", "kind", "reason", "classification",
    ])
    write_csv("classified_duplicate_groups.csv", duplicate_summary, [
        "sha256", "copies", "repos", "size_each", "classification", "paths",
    ])

    url_status = Counter(r["status"] for r in url_rows)
    missing_status = Counter(r["classification"] for r in missing_rows)
    editorial_status = Counter(r["classification"] for r in editorial_rows)
    asset_status = Counter(r["classification"] for r in asset_rows)
    duplicate_status = Counter(r["classification"] for r in duplicate_summary)

    genuine_dead = [r for r in url_rows if r["status"] == "DEAD" and int(r["priority"]) >= 3]
    genuine_restricted = [r for r in url_rows if r["status"] == "RESTRICTED_OR_RATE_LIMITED" and int(r["priority"]) >= 3]
    report = [
        "# Refined total source/archive audit",
        "",
        "This layer removes localhost, templates, analytics/dependency URLs, own-site links, malformed CSV suffixes and obvious archived-evidence noise from the raw scan.",
        "",
        "## Actionable totals",
        "",
        f"- curated external source URL candidates: **{len(candidates):,}**",
        f"- live-checked in this run: **{len(url_rows):,}**",
        f"- high-priority dead source URLs: **{len(genuine_dead):,}**",
        f"- high-priority restricted/rate-limited source URLs: **{len(genuine_restricted):,}**",
        f"- genuine research files requiring bibliography: **{editorial_status['GENUINE_RESEARCH_SOURCE_GAP']:,}**",
        f"- publication assets requiring provenance ledger: **{asset_status['PUBLICATION_ASSET_ADD_PROVENANCE_LEDGER']:,}**",
        f"- research packages requiring package provenance: **{asset_status['RESEARCH_PACKAGE_ADD_PACKAGE_PROVENANCE']:,}**",
        f"- audit evidence files requiring capture metadata: **{asset_status['AUDIT_EVIDENCE_ADD_CAPTURE_METADATA']:,}**",
        f"- likely missing file references: **{missing_status['LIKELY_MISSING_FILE_REFERENCE']:,}**",
        "",
        "## URL health",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for key, value in url_status.most_common():
        report.append(f"| `{key}` | {value:,} |")
    report += ["", "## Local-reference classification", "", "| Class | Count |", "|---|---:|"]
    for key, value in missing_status.most_common():
        report.append(f"| `{key}` | {value:,} |")
    report += ["", "## Editorial-source classification", "", "| Class | Count |", "|---|---:|"]
    for key, value in editorial_status.most_common():
        report.append(f"| `{key}` | {value:,} |")
    report += ["", "## Asset-provenance classification", "", "| Class | Count |", "|---|---:|"]
    for key, value in asset_status.most_common():
        report.append(f"| `{key}` | {value:,} |")
    report += ["", "## Duplicate classification", "", "| Class | Count |", "|---|---:|"]
    for key, value in duplicate_status.most_common():
        report.append(f"| `{key}` | {value:,} |")

    report += [
        "",
        "## Immediate repair order",
        "",
        "1. Add a project-owned/archive-derived provenance ledger for the 13 production images in `TheLegendaryPoet/public/images`.",
        "2. Add citations to `baptisty-rossii/research/75-orthodoxy-baptists-and-why-the-sect-label-stuck-2026-06-21.md`.",
        "3. Review only `LIKELY_MISSING_FILE_REFERENCE` rows; do not treat Astro routes or archived evidence as broken files.",
        "4. Replace or archive high-priority `DEAD` source URLs using institutional catalogs, web archives or newer official landing pages.",
        "5. Add package/capture provenance to the one Research ZIP and three AuditRepo evidence images.",
        "6. Keep duplicate cleanup conservative: deployment copies and audit evidence may be intentional.",
        "",
        "## Outputs",
        "",
        "- `refined_source_url_audit.csv`",
        "- `excluded_or_malformed_url_occurrences.csv`",
        "- `classified_missing_local_links.csv`",
        "- `classified_editorial_source_gaps.csv`",
        "- `classified_asset_provenance_gaps.csv`",
        "- `classified_duplicate_groups.csv`",
    ]
    (OUT / "REFINED_TOTAL_SOURCE_AUDIT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (OUT / "refined_summary.json").write_text(json.dumps({
        "curated_candidates": len(candidates), "audited": len(url_rows),
        "url_status": dict(url_status), "missing_classification": dict(missing_status),
        "editorial_classification": dict(editorial_status), "asset_classification": dict(asset_status),
        "duplicate_classification": dict(duplicate_status),
        "high_priority_dead": len(genuine_dead), "high_priority_restricted": len(genuine_restricted),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REFINED_AUDIT_COMPLETE", json.dumps({
        "audited": len(url_rows), "high_priority_dead": len(genuine_dead),
        "genuine_research_source_gaps": editorial_status["GENUINE_RESEARCH_SOURCE_GAP"],
        "publication_provenance_gaps": asset_status["PUBLICATION_ASSET_ADD_PROVENANCE_LEDGER"],
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
