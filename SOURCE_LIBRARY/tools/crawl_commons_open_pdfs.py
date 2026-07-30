#!/usr/bin/env python3
"""Collect 40+ openly licensed Russian-literature PDFs from Wikimedia Commons.

The collector uses the Wikimedia Commons API, accepts only application/pdf
files whose structured extmetadata declares Public Domain, CC0, CC BY, or
CC BY-SA, then downloads the original unchanged file. Every object receives a
source page, original URL, license metadata, query provenance, SHA-256, byte
size, and page count. Commons metadata is a discovery/rights signal, not a
blanket production approval: individual images extracted from a book still
require a separate provenance review.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import time
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests
from pypdf import PdfReader

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "TheLegendaryPoet-OpenResearchArchive/1.0 "
    "(+https://github.com/FedorMilovanov/Research; contact: viktorcoy2012@gmail.com)"
)
COLLECTION = "commons-russian-literature-open-pdf-40plus"

SEARCH_QUERIES = [
    '"Сергей Есенин" filetype:pdf',
    '"Sergei Yesenin" filetype:pdf',
    '"Александр Пушкин" filetype:pdf',
    '"Alexander Pushkin" filetype:pdf',
    '"Михаил Лермонтов" filetype:pdf',
    '"Mikhail Lermontov" filetype:pdf',
    '"Александр Блок" filetype:pdf',
    '"Alexander Blok" filetype:pdf',
    '"Владимир Маяковский" filetype:pdf',
    '"Vladimir Mayakovsky" filetype:pdf',
    '"Иван Бунин" filetype:pdf',
    '"Ivan Bunin" filetype:pdf',
    '"Афанасий Фет" filetype:pdf',
    '"Afanasy Fet" filetype:pdf',
    '"Фёдор Тютчев" filetype:pdf',
    '"Fyodor Tyutchev" filetype:pdf',
    '"Николай Гумилёв" filetype:pdf',
    '"Nikolay Gumilev" filetype:pdf',
    '"Анна Ахматова" filetype:pdf',
    '"Anna Akhmatova" filetype:pdf',
    '"Велимир Хлебников" filetype:pdf',
    '"Velimir Khlebnikov" filetype:pdf',
    '"Валерий Брюсов" filetype:pdf',
    '"Valery Bryusov" filetype:pdf',
    '"Константин Бальмонт" filetype:pdf',
    '"Konstantin Balmont" filetype:pdf',
    '"Игорь Северянин" filetype:pdf',
    '"Igor Severyanin" filetype:pdf',
    '"русская поэзия" filetype:pdf',
    '"Russian poetry" filetype:pdf',
    '"русская литература" filetype:pdf',
    '"Russian literature" filetype:pdf',
    '"Серебряный век" filetype:pdf',
    '"Silver Age" "Russian" filetype:pdf',
    '"Айседора Дункан" filetype:pdf',
    '"Isadora Duncan" filetype:pdf',
]

OPEN_LICENSE_PATTERNS = (
    "public domain",
    "pd-",
    "cc0",
    "cc by ",
    "cc-by-",
    "cc by-sa",
    "cc-by-sa",
    "creative commons attribution",
)
EXCLUDED_LICENSE_PATTERNS = (
    "fair use",
    "copyrighted",
    "noncommercial",
    "no derivatives",
    "all rights reserved",
)


@dataclass
class Candidate:
    page_id: int
    file_title: str
    description_url: str
    original_url: str
    mime: str
    advertised_bytes: int | None
    width: int | None
    height: int | None
    license_short_name: str
    usage_terms: str
    attribution_required: str
    artist: str
    credit: str
    source: str
    date: str
    query: str


@dataclass
class Record:
    candidate_number: int
    archive_number: int | None
    file_title: str
    local_file_name: str | None
    description_url: str
    original_url: str
    discovery_query: str
    license_short_name: str
    usage_terms: str
    attribution_required: str
    artist: str
    credit: str
    source: str
    date: str
    advertised_bytes: int | None
    status: str
    http_status: int | None
    content_type: str | None
    downloaded_bytes: int | None
    pages: int | None
    sha256: str | None
    checked_at_utc: str
    notes: str


def now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def clean_html(value: str | None) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", html.unescape(value))
    return re.sub(r"\s+", " ", text).strip()


def metadata_value(ext: dict[str, Any], key: str) -> str:
    raw = ext.get(key, {})
    if isinstance(raw, dict):
        return clean_html(str(raw.get("value", "")))
    return clean_html(str(raw))


def slugify(value: str, limit: int = 150) -> str:
    value = value.removeprefix("File:")
    value = re.sub(r"\.pdf$", "", value, flags=re.IGNORECASE)
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("—", "-").replace("–", "-")
    value = re.sub(r"[\\/:*?\"<>|]+", "_", value)
    value = re.sub(r"\s+", " ", value).strip(" ._")
    return (value[:limit].rstrip(" ._") or "commons-document")


def request(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    stream: bool = False,
) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, 6):
        try:
            response = session.get(
                url,
                params=params,
                stream=stream,
                allow_redirects=True,
                timeout=(30, 360),
            )
            if response.status_code in {429, 500, 502, 503, 504} and attempt < 5:
                response.close()
                time.sleep(attempt * 4)
                continue
            return response
        except requests.RequestException as exc:
            last_error = exc
            if attempt < 5:
                time.sleep(attempt * 4)
                continue
            raise
    raise RuntimeError(f"request failed: {url}: {last_error}")


def license_allowed(short_name: str, usage_terms: str) -> bool:
    combined = f"{short_name} {usage_terms}".lower()
    if any(marker in combined for marker in EXCLUDED_LICENSE_PATTERNS):
        return False
    return any(marker in combined for marker in OPEN_LICENSE_PATTERNS)


def discover_query(
    session: requests.Session,
    query: str,
    limit: int,
) -> list[Candidate]:
    params: dict[str, Any] = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": min(limit, 50),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 0,
        "origin": "*",
    }
    results: list[Candidate] = []
    continuation: dict[str, Any] = {}

    while len(results) < limit:
        response = request(session, API, params={**params, **continuation})
        response.raise_for_status()
        payload = response.json()
        pages = payload.get("query", {}).get("pages", [])
        for page in pages:
            infos = page.get("imageinfo") or []
            if not infos:
                continue
            info = infos[0]
            mime = str(info.get("mime", ""))
            title = str(page.get("title", ""))
            if mime != "application/pdf" and not title.lower().endswith(".pdf"):
                continue
            ext = info.get("extmetadata") or {}
            short_name = metadata_value(ext, "LicenseShortName")
            usage_terms = metadata_value(ext, "UsageTerms")
            if not license_allowed(short_name, usage_terms):
                continue
            original_url = str(info.get("url", ""))
            description_url = str(info.get("descriptionurl", ""))
            if not original_url.startswith("https://upload.wikimedia.org/"):
                continue
            results.append(
                Candidate(
                    page_id=int(page.get("pageid", 0)),
                    file_title=title,
                    description_url=description_url,
                    original_url=original_url,
                    mime=mime,
                    advertised_bytes=int(info["size"]) if info.get("size") is not None else None,
                    width=int(info["width"]) if info.get("width") is not None else None,
                    height=int(info["height"]) if info.get("height") is not None else None,
                    license_short_name=short_name,
                    usage_terms=usage_terms,
                    attribution_required=metadata_value(ext, "AttributionRequired"),
                    artist=metadata_value(ext, "Artist"),
                    credit=metadata_value(ext, "Credit"),
                    source=metadata_value(ext, "Source"),
                    date=metadata_value(ext, "DateTimeOriginal") or metadata_value(ext, "DateTime"),
                    query=query,
                )
            )
            if len(results) >= limit:
                break
        if len(results) >= limit or "continue" not in payload:
            break
        continuation = payload["continue"]
    return results


def discover(session: requests.Session, per_query: int) -> tuple[list[Candidate], list[dict[str, str]]]:
    candidates: list[Candidate] = []
    failures: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for index, query in enumerate(SEARCH_QUERIES, start=1):
        print(f"[query {index}/{len(SEARCH_QUERIES)}] {query}", flush=True)
        try:
            found = discover_query(session, query, per_query)
        except Exception as exc:
            failures.append({"query": query, "error": f"{type(exc).__name__}: {exc}"})
            continue
        for candidate in found:
            if candidate.original_url in seen_urls:
                continue
            seen_urls.add(candidate.original_url)
            candidates.append(candidate)
    return candidates, failures


def count_pages(path: Path) -> int | None:
    try:
        return len(PdfReader(str(path), strict=False).pages)
    except Exception:
        return None


def download(
    session: requests.Session,
    candidate: Candidate,
    candidate_number: int,
    archive_number: int,
    output_dir: Path,
    max_bytes: int,
) -> Record:
    checked = now_utc()
    if candidate.advertised_bytes and candidate.advertised_bytes > max_bytes:
        return Record(
            candidate_number, None, candidate.file_title, None,
            candidate.description_url, candidate.original_url, candidate.query,
            candidate.license_short_name, candidate.usage_terms,
            candidate.attribution_required, candidate.artist, candidate.credit,
            candidate.source, candidate.date, candidate.advertised_bytes,
            "SKIPPED_TOO_LARGE", None, None, None, None, None, checked,
            f"Advertised size exceeds {max_bytes} bytes",
        )

    try:
        response = request(session, candidate.original_url, stream=True)
    except Exception as exc:
        return Record(
            candidate_number, None, candidate.file_title, None,
            candidate.description_url, candidate.original_url, candidate.query,
            candidate.license_short_name, candidate.usage_terms,
            candidate.attribution_required, candidate.artist, candidate.credit,
            candidate.source, candidate.date, candidate.advertised_bytes,
            "REQUEST_FAILED", None, None, None, None, None, checked,
            f"{type(exc).__name__}: {exc}",
        )

    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip() or None
    if response.status_code != 200:
        status = response.status_code
        response.close()
        return Record(
            candidate_number, None, candidate.file_title, None,
            candidate.description_url, candidate.original_url, candidate.query,
            candidate.license_short_name, candidate.usage_terms,
            candidate.attribution_required, candidate.artist, candidate.credit,
            candidate.source, candidate.date, candidate.advertised_bytes,
            "HTTP_ERROR", status, content_type, None, None, None, checked,
            "Original file request did not return HTTP 200",
        )

    local_name = f"{archive_number:02d}__{slugify(candidate.file_title)}.pdf"
    destination = output_dir / local_name
    digest = hashlib.sha256()
    total = 0
    first = b""
    try:
        with destination.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                if not first:
                    first = chunk[:8]
                total += len(chunk)
                if total > max_bytes:
                    raise RuntimeError(f"stream exceeded {max_bytes} bytes")
                handle.write(chunk)
                digest.update(chunk)
    except Exception as exc:
        response.close()
        destination.unlink(missing_ok=True)
        return Record(
            candidate_number, None, candidate.file_title, None,
            candidate.description_url, candidate.original_url, candidate.query,
            candidate.license_short_name, candidate.usage_terms,
            candidate.attribution_required, candidate.artist, candidate.credit,
            candidate.source, candidate.date, candidate.advertised_bytes,
            "DOWNLOAD_FAILED", 200, content_type, total, None, None, checked,
            f"{type(exc).__name__}: {exc}",
        )
    response.close()

    if not first.startswith(b"%PDF"):
        destination.unlink(missing_ok=True)
        return Record(
            candidate_number, None, candidate.file_title, None,
            candidate.description_url, candidate.original_url, candidate.query,
            candidate.license_short_name, candidate.usage_terms,
            candidate.attribution_required, candidate.artist, candidate.credit,
            candidate.source, candidate.date, candidate.advertised_bytes,
            "NOT_A_PDF", 200, content_type, total, None, None, checked,
            "Response did not begin with the %PDF signature",
        )

    return Record(
        candidate_number, archive_number, candidate.file_title, local_name,
        candidate.description_url, candidate.original_url, candidate.query,
        candidate.license_short_name, candidate.usage_terms,
        candidate.attribution_required, candidate.artist, candidate.credit,
        candidate.source, candidate.date, candidate.advertised_bytes,
        "DOWNLOADED", 200, content_type or "application/pdf", total,
        count_pages(destination), digest.hexdigest(), checked,
        "Original Commons PDF stored unchanged; production use requires per-item review",
    )


def write_reports(
    output_dir: Path,
    candidates: list[Candidate],
    records: list[Record],
    discovery_failures: list[dict[str, str]],
    target: int,
) -> dict[str, Any]:
    downloaded = [record for record in records if record.status == "DOWNLOADED"]
    license_counts: dict[str, int] = {}
    for record in downloaded:
        key = record.license_short_name or record.usage_terms or "unspecified-open"
        license_counts[key] = license_counts.get(key, 0) + 1
    report: dict[str, Any] = {
        "collection": COLLECTION,
        "generated_at_utc": now_utc(),
        "api": API,
        "search_queries": SEARCH_QUERIES,
        "discovery_failures": discovery_failures,
        "eligible_open_pdf_candidates_discovered": len(candidates),
        "candidates_processed": len(records),
        "target_downloads": target,
        "downloaded_pdfs": len(downloaded),
        "failed_or_skipped": len(records) - len(downloaded),
        "total_bytes": sum(record.downloaded_bytes or 0 for record in downloaded),
        "license_counts": license_counts,
        "rights_policy": (
            "Only Commons application/pdf originals with structured extmetadata "
            "matching Public Domain, CC0, CC BY, or CC BY-SA; exclusions include "
            "fair use, noncommercial, no-derivatives, copyrighted/all-rights-reserved."
        ),
        "records": [asdict(record) for record in records],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    fields = list(Record.__annotations__)
    with (output_dir / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))
    with (output_dir / "SHA256SUMS.txt").open("w", encoding="utf-8") as handle:
        for record in downloaded:
            handle.write(f"{record.sha256}  {record.local_file_name}\n")

    lines = [
        "# Wikimedia Commons: открытые PDF по русской литературе",
        "",
        f"- Создано: `{report['generated_at_utc']}`",
        f"- Найдено открытых PDF-кандидатов: `{len(candidates)}`",
        f"- Обработано: `{len(records)}`",
        f"- Загружено: `{len(downloaded)}` / `{target}`",
        f"- Ошибок/пропусков: `{len(records) - len(downloaded)}`",
        f"- Размер: `{report['total_bytes']}` байт",
        "",
        "Файлы сохранены без изменений. Структурированная лицензия Commons является "
        "основанием для архивного включения, но перед использованием конкретной страницы "
        "или иллюстрации на публичном сайте требуется ручная проверка описания, автора, "
        "источника, credit line и применимости лицензии.",
        "",
        "## Файлы",
        "",
    ]
    for record in records:
        lines.append(
            f"- `{record.status}` — {record.file_title} — "
            f"{record.local_file_name or 'без файла'} — "
            f"{record.license_short_name or record.usage_terms} — "
            f"`{record.sha256 or 'без SHA-256'}` — {record.description_url}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=40)
    parser.add_argument("--per-query", type=int, default=20)
    parser.add_argument("--max-candidates", type=int, default=250)
    parser.add_argument("--max-file-mb", type=int, default=120)
    parser.add_argument("--pause", type=float, default=0.7)
    parser.add_argument("--output-root", type=Path, default=Path("open-access-pdf-archive"))
    args = parser.parse_args()

    output_dir = args.output_root / COLLECTION
    output_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Api-User-Agent": USER_AGENT,
            "Accept": "application/json,application/pdf;q=0.9,*/*;q=0.5",
            "Referer": "https://commons.wikimedia.org/",
        }
    )

    candidates, discovery_failures = discover(session, args.per_query)
    records: list[Record] = []
    successful = 0
    max_bytes = args.max_file_mb * 1024 * 1024
    for candidate_number, candidate in enumerate(candidates[: args.max_candidates], start=1):
        if successful >= args.target:
            break
        print(
            f"[candidate {candidate_number}/{min(len(candidates), args.max_candidates)}; "
            f"saved {successful}/{args.target}] {candidate.file_title}",
            flush=True,
        )
        record = download(
            session, candidate, candidate_number, successful + 1, output_dir, max_bytes
        )
        records.append(record)
        if record.status == "DOWNLOADED":
            successful += 1
        write_reports(output_dir, candidates, records, discovery_failures, args.target)
        time.sleep(args.pause)

    report = write_reports(output_dir, candidates, records, discovery_failures, args.target)
    print(
        json.dumps(
            {
                "discovered": len(candidates),
                "processed": len(records),
                "downloaded": report["downloaded_pdfs"],
                "target": args.target,
                "discovery_failures": len(discovery_failures),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
