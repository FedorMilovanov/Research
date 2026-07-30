#!/usr/bin/env python3
"""Audit HTTP reachability for URLs in the official digital collections index.

This is a navigation audit, not a rights or content-verification pass. It follows
redirects, records status/content type/final URL, and treats 401/403/429 as
reachable-but-restricted rather than dead. Results are written as JSON, CSV and
Markdown so link maintenance does not rely on memory or browser spot checks.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import requests

URL_RE = re.compile(r"https?://[^\s)\]>]+")
USER_AGENT = (
    "TheLegendaryPoet-SourceLinkAudit/1.0 "
    "(+https://github.com/FedorMilovanov/Research; contact: viktorcoy2012@gmail.com)"
)


@dataclass
class LinkRecord:
    number: int
    source_url: str
    final_url: str | None
    status_code: int | None
    classification: str
    content_type: str | None
    elapsed_seconds: float | None
    redirects: int
    method: str
    error: str
    checked_at_utc: str


def now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for raw in URL_RE.findall(text):
        url = raw.rstrip(".,;:`'")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def classify(status: int | None, error: str) -> str:
    if error:
        lowered = error.lower()
        if "timeout" in lowered:
            return "TIMEOUT"
        if "ssl" in lowered or "certificate" in lowered:
            return "TLS_ERROR"
        if "name or service" in lowered or "resolve" in lowered or "dns" in lowered:
            return "DNS_ERROR"
        return "NETWORK_ERROR"
    if status is None:
        return "UNKNOWN"
    if 200 <= status < 300:
        return "OK"
    if 300 <= status < 400:
        return "REDIRECT_RESPONSE"
    if status in {401, 403}:
        return "REACHABLE_RESTRICTED"
    if status == 429:
        return "REACHABLE_RATE_LIMITED"
    if status in {404, 410}:
        return "DEAD"
    if 400 <= status < 500:
        return "CLIENT_ERROR"
    if 500 <= status < 600:
        return "SERVER_ERROR"
    return "OTHER"


def fetch_one(session: requests.Session, number: int, url: str, timeout: float) -> LinkRecord:
    checked = now_utc()
    started = time.monotonic()
    last_error = ""
    response: requests.Response | None = None
    method = "GET"

    for attempt in range(1, 4):
        try:
            response = session.get(
                url,
                allow_redirects=True,
                timeout=(20, timeout),
                stream=True,
                headers={"Range": "bytes=0-4095"},
            )
            if response.status_code in {429, 500, 502, 503, 504} and attempt < 3:
                response.close()
                time.sleep(attempt * 2)
                continue
            break
        except requests.RequestException as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < 3:
                time.sleep(attempt * 2)
                continue

    elapsed = round(time.monotonic() - started, 3)
    if response is None:
        return LinkRecord(
            number=number,
            source_url=url,
            final_url=None,
            status_code=None,
            classification=classify(None, last_error),
            content_type=None,
            elapsed_seconds=elapsed,
            redirects=0,
            method=method,
            error=last_error,
            checked_at_utc=checked,
        )

    status = response.status_code
    final_url = response.url
    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip() or None
    redirects = len(response.history)
    response.close()
    return LinkRecord(
        number=number,
        source_url=url,
        final_url=final_url,
        status_code=status,
        classification=classify(status, ""),
        content_type=content_type,
        elapsed_seconds=elapsed,
        redirects=redirects,
        method=method,
        error="",
        checked_at_utc=checked,
    )


def write_outputs(records: list[LinkRecord], output_dir: Path, source_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = {
        name: sum(record.classification == name for record in records)
        for name in sorted({record.classification for record in records})
    }
    report = {
        "source_file": str(source_path),
        "checked_at_utc": now_utc(),
        "total_unique_urls": len(records),
        "classification_counts": counts,
        "records": [asdict(record) for record in records],
    }
    (output_dir / "official-collections-link-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fields = list(LinkRecord.__dataclass_fields__)
    with (output_dir / "official-collections-link-audit.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))

    lines = [
        "# Official digital collections — HTTP link audit",
        "",
        f"- Source: `{source_path}`",
        f"- Checked: `{report['checked_at_utc']}`",
        f"- Unique URLs: **{len(records)}**",
        f"- Classifications: `{counts}`",
        "",
        "## Non-OK and redirected/restricted results",
        "",
        "| # | Class | HTTP | Source | Final / error |",
        "|---:|---|---:|---|---|",
    ]
    for record in records:
        if record.classification == "OK" and record.redirects == 0:
            continue
        detail = record.error or record.final_url or ""
        detail = detail.replace("|", "%7C")
        source = record.source_url.replace("|", "%7C")
        lines.append(
            f"| {record.number} | `{record.classification}` | "
            f"{record.status_code or ''} | {source} | {detail} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `OK` means the endpoint responded; it does not establish item rights.",
            "- `REACHABLE_RESTRICTED` and `REACHABLE_RATE_LIMITED` are not dead links.",
            "- `DEAD`, DNS/TLS/network errors and persistent 5xx require manual follow-up.",
            "- Redirects should be normalized in the source index when the final URL is stable.",
        ]
    )
    (output_dir / "OFFICIAL_COLLECTIONS_LINK_AUDIT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default="SOURCE_LIBRARY/OFFICIAL_DIGITAL_COLLECTIONS_70PLUS_INDEX_2026-07-30.md",
    )
    parser.add_argument("--output", default="link-audit-output")
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--pause", type=float, default=0.25)
    args = parser.parse_args()

    source_path = Path(args.source)
    urls = extract_urls(source_path.read_text(encoding="utf-8"))
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/json,application/pdf,*/*;q=0.8",
    })

    records: list[LinkRecord] = []
    for index, url in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] {url}", flush=True)
        record = fetch_one(session, index, url, args.timeout)
        records.append(record)
        print(
            f"  -> {record.classification} http={record.status_code} final={record.final_url}",
            flush=True,
        )
        time.sleep(args.pause)

    write_outputs(records, Path(args.output), source_path)

    dead = sum(record.classification == "DEAD" for record in records)
    severe = sum(
        record.classification in {"DNS_ERROR", "TLS_ERROR", "NETWORK_ERROR"}
        for record in records
    )
    print(json.dumps({
        "total": len(records),
        "dead": dead,
        "severe_network_errors": severe,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
