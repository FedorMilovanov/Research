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
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

import requests

ROOT = Path(os.environ.get("AUDIT_OUT", "total-audit-output"))
SRC = ROOT / "refined" / "refined_source_url_audit.csv"
OUT = ROOT / "dead-url-classification"
OUT.mkdir(parents=True, exist_ok=True)

UA = "TheLegendaryPoet-DeadSourceClassifier/2026-07-30"
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/148.0.0.0 Safari/537.36"
)
REPLACEMENT_REGISTRY = Path(
    os.environ.get(
        "SOURCE_URL_REPLACEMENT_REGISTRY",
        "data/source-url-replacements-2026-08-02.json",
    )
)

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
CSV_METADATA_SUFFIX_RE = re.compile(
    r",(?:Official|Contemporary|physical|reproduced|Complete|\d{1,5})$",
    re.I,
)
METADATA_DOMAINS = {
    "samizdat.library.utoronto.ca",
    "almanah.bogomysliye.com",
    "repository.up.ac.za",
}
LEGACY_PROJECT_DOMAINS = {"raw.githubusercontent.com", "github.com"}

BAPTIST_COLLECTIONS = (
    (
        re.compile(
            r"(?:utren(?:nyaya|niaia)[-_]?zvezda|(?:^|[/_-])uz(?:18|19|20)\d{2}(?:[_-]|\.))",
            re.I,
        ),
        "https://baptist.org.ru/izdaniya/utrennyaya-zvezda/",
    ),
    (
        re.compile(r"bratsk(?:iy|ii)[-_]?vestnik", re.I),
        "https://baptist.org.ru/izdaniya/bratskij-vestnik/",
    ),
    (
        re.compile(r"khristianin|hristianin", re.I),
        "https://baptist.org.ru/izdaniya/hristianin/",
    ),
    (
        re.compile(r"(?:^|[/_-])baptist[-_]?(?:18|19|20)\d{2}", re.I),
        "https://baptist.org.ru/izdaniya/baptist/",
    ),
)

_COLLECTION_CACHE: dict[str, dict] = {}


def read_rows() -> list[dict[str, str]]:
    with SRC.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r["status"] == "DEAD"]


def write_csv(name: str, rows: list[dict]) -> None:
    fields = [
        "classification",
        "original_url",
        "cleaned_url",
        "recheck_status",
        "recheck_code",
        "final_url",
        "domain",
        "priority",
        "occurrences",
        "repos",
        "example_paths",
        "reason",
        "error",
    ]
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_replacements() -> dict[str, dict]:
    if not REPLACEMENT_REGISTRY.is_file():
        return {}
    try:
        payload = json.loads(REPLACEMENT_REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    replacements: dict[str, dict] = {}
    for record in payload.get("records", []):
        old = str(record.get("oldUrl") or "").strip()
        new = str(record.get("newUrl") or "").strip()
        if old and new:
            replacements[old] = record
    return replacements


def unbalanced(url: str) -> bool:
    return url.count("(") != url.count(")") or url.count("[") != url.count("]")


def clean_metadata_suffix(url: str, domain: str) -> tuple[str, str]:
    value = html.unescape(url).strip()
    metadata_match = CSV_METADATA_SUFFIX_RE.search(value)
    if metadata_match:
        return value[: metadata_match.start()], "comma-separated ledger metadata removed"
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


def known_non_item_endpoint(url: str, domain: str) -> bool:
    try:
        path = urlsplit(url).path.rstrip("/") or "/"
    except Exception:
        return False
    return (domain, path.lower()) in {
        ("upload.wikimedia.org", "/wikipedia/commons"),
    }


def known_linewrap_fragment(url: str, domain: str) -> bool:
    try:
        path = urlsplit(url).path.rstrip("/") or "/"
    except Exception:
        return False
    return (domain, path.lower()) in {
        ("dhi.ac.uk", "/protestantizm/section/do"),
        ("dhi.ac.uk", "/protestantizm/section/doc"),
        ("pravenc.ru", "/text"),
    }


def https_upgrade(url: str) -> str:
    try:
        parts = urlsplit(url)
        if parts.scheme == "http":
            return urlunsplit(("https", parts.netloc, parts.path, parts.query, parts.fragment))
    except Exception:
        pass
    return url


def classify_http(code: int) -> str:
    if 200 <= code < 400:
        return "OK"
    if code in {401, 403, 429, 451}:
        return "RESTRICTED"
    if code in {404, 410}:
        return "DEAD"
    if 500 <= code < 600:
        return "SERVER_ERROR"
    return "HTTP_ERROR"


def check(url: str, *, browser_fallback: bool = False) -> dict:
    attempts = [url]
    upgraded = https_upgrade(url)
    if upgraded != url:
        attempts.append(upgraded)

    user_agents = [UA]
    if browser_fallback:
        user_agents.append(BROWSER_UA)

    last = {
        "status": "REQUEST_ERROR",
        "code": 0,
        "final_url": "",
        "error": "not attempted",
    }
    for attempt in attempts:
        for user_agent in user_agents:
            started = time.monotonic()
            try:
                response = requests.get(
                    attempt,
                    headers={
                        "User-Agent": user_agent,
                        "Accept": "text/html,application/pdf,*/*;q=0.8",
                    },
                    timeout=(7, 18),
                    allow_redirects=True,
                    stream=True,
                )
                code = int(response.status_code)
                final = response.url
                response.close()
                status = classify_http(code)
                last = {
                    "status": status,
                    "code": code,
                    "final_url": final,
                    "error": "",
                    "seconds": round(time.monotonic() - started, 3),
                }
                if status in {"OK", "RESTRICTED"}:
                    return last
            except requests.RequestException as exc:
                last = {
                    "status": "REQUEST_ERROR",
                    "code": 0,
                    "final_url": "",
                    "error": f"{type(exc).__name__}: {exc}"[:300],
                    "seconds": round(time.monotonic() - started, 3),
                }
    return last


def baptist_issue_identity(path: str) -> tuple[str, str] | None:
    filename = path.rsplit("/", 1)[-1]
    match = re.search(r"(?P<year>(?:18|19|20)\d{2})[_-](?P<issue>\d{1,2}(?:-\d{1,2})?)", filename)
    if match:
        return match.group("year"), str(int(match.group("issue").split("-", 1)[0]))
    match = re.search(r"(?P<issue>\d{1,2}(?:-\d{1,2})?)[_-](?P<year>(?:18|19|20)\d{2})", filename)
    if match:
        return match.group("year"), str(int(match.group("issue").split("-", 1)[0]))
    return None


def fetch_collection_page(collection_url: str) -> dict:
    cached = _COLLECTION_CACHE.get(collection_url)
    if cached is not None:
        return cached

    started = time.monotonic()
    try:
        response = requests.get(
            collection_url,
            headers={
                "User-Agent": BROWSER_UA,
                "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            },
            timeout=(7, 20),
            allow_redirects=True,
        )
        code = int(response.status_code)
        final = response.url
        body = response.text if 200 <= code < 400 else ""
        response.close()
        result = {
            "status": classify_http(code),
            "code": code,
            "final_url": final,
            "error": "",
            "seconds": round(time.monotonic() - started, 3),
            "body": body,
        }
    except requests.RequestException as exc:
        result = {
            "status": "REQUEST_ERROR",
            "code": 0,
            "final_url": "",
            "error": f"{type(exc).__name__}: {exc}"[:300],
            "seconds": round(time.monotonic() - started, 3),
            "body": "",
        }
    _COLLECTION_CACHE[collection_url] = result
    return result


def collection_confirms_issue(body: str, page_url: str, target_url: str, identity: tuple[str, str] | None) -> bool:
    if not body:
        return False

    try:
        target_path = unquote(urlsplit(target_url).path)
    except Exception:
        target_path = ""

    for raw_href in re.findall(r'''href\s*=\s*["']([^"']+)["']''', body, flags=re.I):
        absolute = urljoin(page_url, html.unescape(raw_href))
        try:
            href_path = unquote(urlsplit(absolute).path)
        except Exception:
            continue
        if target_path and href_path == target_path:
            return True

    if identity:
        year, issue = identity
        plain = html.unescape(re.sub(r"<[^>]+>", " ", body))
        plain = re.sub(r"\s+", " ", plain)
        issue_patterns = (
            rf"{re.escape(year)}\s*(?:№|N[oº]?\.?)\s*0*{re.escape(issue)}(?:\D|$)",
            rf"{re.escape(year)}[^0-9]{{0,20}}0*{re.escape(issue)}(?:\D|$)",
        )
        if any(re.search(pattern, plain, re.I) for pattern in issue_patterns):
            return True
    return False


def recover_baptist_collection(url: str, domain: str) -> tuple[str, dict | None, bool]:
    if domain != "baptist.org.ru":
        return "", None, False
    try:
        path = unquote(urlsplit(url).path)
    except Exception:
        return "", None, False
    if "/_service/" not in path.lower():
        return "", None, False

    for pattern, collection_url in BAPTIST_COLLECTIONS:
        if not pattern.search(path):
            continue
        result = fetch_collection_page(collection_url)
        confirmed = False
        if result["status"] in {"OK", "RESTRICTED"}:
            confirmed = collection_confirms_issue(
                result.get("body", ""),
                result.get("final_url") or collection_url,
                url,
                baptist_issue_identity(path),
            )
        return collection_url, result, confirmed
    return "", None, False


def main() -> int:
    replacements = load_replacements()
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
            classified.append(
                {
                    **base,
                    "classification": "TEMPLATE_FALSE_POSITIVE",
                    "reason": "template/variable URL",
                }
            )
            continue
        if unbalanced(original):
            classified.append(
                {
                    **base,
                    "classification": "TRUNCATED_URL_FALSE_POSITIVE",
                    "reason": "unbalanced brackets/parentheses from Markdown or CSV extraction",
                }
            )
            continue
        if known_linewrap_fragment(original, domain):
            classified.append(
                {
                    **base,
                    "classification": "TRUNCATED_URL_FALSE_POSITIVE",
                    "reason": "known line-wrapped source extraction fragment; the URL continues on the following source-text line",
                }
            )
            continue
        if technical_only(row["example_paths"]):
            classified.append(
                {
                    **base,
                    "classification": "TECHNICAL_OR_ARCHIVED_REFERENCE",
                    "reason": "all occurrences are scripts/audit/incoming/archive/design references",
                }
            )
            continue
        if root_only(original) or known_non_item_endpoint(original, domain):
            classified.append(
                {
                    **base,
                    "classification": "ROOT_OR_SERVICE_ENDPOINT_NOT_SOURCE_ITEM",
                    "reason": "domain root/service endpoint is not an item citation",
                }
            )
            continue
        if domain in LEGACY_PROJECT_DOMAINS and "FedorMilovanov/gospod-bog" in original:
            classified.append(
                {
                    **base,
                    "classification": "LEGACY_PROJECT_REFERENCE",
                    "reason": "old project/repository architecture reference, not external research source",
                }
            )
            continue

        cleaned, clean_reason = clean_metadata_suffix(original, domain)

        replacement = replacements.get(cleaned) or replacements.get(original)
        if replacement:
            classified.append(
                {
                    **base,
                    "classification": "SUPERSEDED_BY_CURRENT_URL_AUTHORITY",
                    "cleaned_url": cleaned,
                    "recheck_status": "AUTHORITY_REPLACEMENT",
                    "final_url": str(replacement.get("newUrl") or ""),
                    "reason": (
                        f"{replacement.get('id', 'replacement')}: "
                        f"{replacement.get('status', 'REPLACE')}; "
                        "historical URL preserved as evidence, active consumers use current replacement authority"
                    ),
                }
            )
            continue

        result = check(cleaned)
        if result["status"] == "OK":
            classification = "RECOVERED_AFTER_CLEAN_OR_HTTPS"
        elif result["status"] == "RESTRICTED":
            classification = "LIVE_BUT_RESTRICTED"
        elif result["status"] in {"SERVER_ERROR", "REQUEST_ERROR"}:
            classification = "TEMPORARY_OR_NETWORK_RETRY"
        elif result["status"] == "DEAD":
            collection_url, collection_result, confirmed = recover_baptist_collection(cleaned, domain)
            if collection_result and collection_result["status"] in {"OK", "RESTRICTED"} and confirmed:
                classification = "RECOVERABLE_OFFICIAL_COLLECTION_MIGRATION"
                clean_reason = (
                    "direct PDF transport returned DEAD to the runner, but the live official Union "
                    f"collection confirms this issue: {collection_result.get('final_url') or collection_url}"
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

        classified.append(
            {
                **base,
                "classification": classification,
                "cleaned_url": cleaned,
                "recheck_status": result["status"],
                "recheck_code": result["code"],
                "final_url": result["final_url"],
                "reason": clean_reason or "rechecked after noise classification",
                "error": result["error"],
            }
        )
        time.sleep(0.15)

    classified.sort(
        key=lambda row: (
            row["classification"],
            -int(row["priority"]),
            row["domain"],
            row["original_url"],
        )
    )
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
        f"- superseded URLs preserved by current authority: **{counts['SUPERSEDED_BY_CURRENT_URL_AUTHORITY']}**",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    for key, value in counts.most_common():
        report.append(f"| `{key}` | {value} |")
    report += [
        "",
        "`TRUE_DEAD_SOURCE_REPAIR` is still a repair queue, not proof that the cited claim is false. "
        "Replace with a current institutional landing page, archived copy, DOI, catalog record or a "
        "different primary witness; do not silently delete evidence.",
        "",
        "`RECOVERABLE_OFFICIAL_COLLECTION_MIGRATION` means the runner could not retrieve the old deep "
        "PDF endpoint but a live official institutional issue index confirmed that exact issue during "
        "this run. The old URL remains recorded for eventual deep-link normalization.",
        "",
        "`SUPERSEDED_BY_CURRENT_URL_AUTHORITY` means a committed current replacement registry explicitly "
        "supersedes the historical transport while preserving the old URL as audit evidence.",
    ]
    (OUT / "DEAD_URL_CLASSIFICATION.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    (OUT / "summary.json").write_text(
        json.dumps(
            {"total": len(classified), "counts": dict(counts)},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        "DEAD_URL_CLASSIFICATION_COMPLETE",
        json.dumps(dict(counts), ensure_ascii=False),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
