#!/usr/bin/env python3
"""Build a 40+ PDF research archive from the current official IMLI publisher.

The script crawls only the Russian Literature catalogue on ed-imli.ru. It
accepts records whose catalogue block explicitly states Creative Commons
Attribution-NoDerivatives 4.0, downloads the linked PDF unchanged, validates
its PDF signature, calculates SHA-256, and records provenance. A failed item is
kept in the manifest and the crawler continues to later candidates.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from pypdf import PdfReader

BASE = "https://ed-imli.ru"
CATALOGUE = f"{BASE}/index.php/en/russian-literature"
CATALOGUE_PAGES = [CATALOGUE] + [f"{CATALOGUE}?start={offset}" for offset in range(20, 121, 20)]
USER_AGENT = "TheLegendaryPoet-ResearchArchive/2.0 (+https://github.com/FedorMilovanov/Research)"
COLLECTION = "ed-imli-russian-literature-40plus"
RIGHTS_MARKERS = ("Creative Commons Attribution-NoDerivatives 4.0", "CC BY-ND", "СС BY-ND")


@dataclass
class Candidate:
    title: str
    item_page: str
    listing_page: str
    pdf_url: str
    doi: str | None
    isbn: str | None
    year: int | None
    rights: str


@dataclass
class Record:
    candidate_number: int
    archive_number: int | None
    title: str
    item_page: str
    listing_page: str
    pdf_url: str
    doi: str | None
    isbn: str | None
    year: int | None
    rights: str
    file_name: str | None
    status: str
    http_status: int | None
    content_type: str | None
    bytes: int | None
    pages: int | None
    sha256: str | None
    checked_at_utc: str
    notes: str


def now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str, limit: int = 145) -> str:
    value = unicodedata.normalize("NFKC", unquote(value))
    value = value.replace("—", "-").replace("–", "-")
    value = re.sub(r"[\\/:*?\"<>|]+", "_", value)
    value = re.sub(r"\s+", " ", value).strip(" ._")
    return (value[:limit].rstrip(" ._") or "imli-book")


def get(session: requests.Session, url: str, *, stream: bool = False) -> requests.Response:
    error: Exception | None = None
    for attempt in range(1, 6):
        try:
            response = session.get(
                url,
                timeout=(35, 360),
                allow_redirects=True,
                stream=stream,
            )
            if response.status_code in {429, 500, 502, 503, 504} and attempt < 5:
                response.close()
                time.sleep(attempt * 5)
                continue
            return response
        except requests.RequestException as exc:
            error = exc
            if attempt < 5:
                time.sleep(attempt * 5)
                continue
            raise
    raise RuntimeError(f"request failed for {url}: {error}")


def record_block(anchor: Tag) -> Tag | None:
    """Find the smallest ancestor that contains title and explicit CC rights."""
    for parent in anchor.parents:
        if not isinstance(parent, Tag):
            continue
        if parent.name not in {"li", "article", "div"}:
            continue
        title_node = parent.find(["h2", "h3", "h4"])
        if title_node is None:
            continue
        text = clean_text(parent.get_text(" ", strip=True))
        if any(marker in text for marker in RIGHTS_MARKERS):
            return parent
    return None


def first_match(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return clean_text(match.group(1)) if match else None


def discover(session: requests.Session) -> tuple[list[Candidate], list[dict[str, str]]]:
    candidates: list[Candidate] = []
    page_failures: list[dict[str, str]] = []
    seen: set[str] = set()

    for page_url in CATALOGUE_PAGES:
        print(f"[catalogue] {page_url}", flush=True)
        try:
            response = get(session, page_url)
            response.raise_for_status()
        except Exception as exc:  # recorded, never hidden
            page_failures.append({"url": page_url, "error": f"{type(exc).__name__}: {exc}"})
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for anchor in soup.find_all("a", href=True):
            absolute = urljoin(response.url, anchor["href"])
            parsed = urlparse(absolute)
            if parsed.netloc != urlparse(BASE).netloc or not parsed.path.lower().endswith(".pdf"):
                continue
            canonical_pdf = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if canonical_pdf in seen:
                continue
            block = record_block(anchor)
            if block is None:
                continue
            block_text = clean_text(block.get_text(" ", strip=True))
            title_node = block.find(["h2", "h3", "h4"])
            if title_node is None:
                continue
            title = clean_text(title_node.get_text(" ", strip=True))
            title_anchor = title_node.find("a", href=True)
            item_page = urljoin(response.url, title_anchor["href"]) if title_anchor else response.url
            doi_anchor = block.find("a", href=re.compile(r"doi\.org/", re.I))
            doi = clean_text(doi_anchor.get_text(" ", strip=True)) if doi_anchor else None
            if doi and "doi.org" not in doi:
                doi = urljoin("https://doi.org/", doi)
            isbn = first_match(r"ISBN(?:\s*\([^)]*\))?\s*:\s*([0-9Xx-]{10,20})", block_text)
            year_text = first_match(r"Year of publication\s*:\s*(\d{4})", block_text)
            rights = next((marker for marker in RIGHTS_MARKERS if marker in block_text), "CC BY-ND 4.0")
            seen.add(canonical_pdf)
            candidates.append(
                Candidate(
                    title=title,
                    item_page=item_page,
                    listing_page=response.url,
                    pdf_url=absolute,
                    doi=doi,
                    isbn=isbn,
                    year=int(year_text) if year_text else None,
                    rights=rights,
                )
            )

    return candidates, page_failures


def page_count(path: Path) -> int | None:
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
    try:
        response = get(session, candidate.pdf_url, stream=True)
    except Exception as exc:
        return Record(
            candidate_number, None, candidate.title, candidate.item_page,
            candidate.listing_page, candidate.pdf_url, candidate.doi, candidate.isbn,
            candidate.year, candidate.rights, None, "REQUEST_FAILED", None, None,
            None, None, None, checked, f"{type(exc).__name__}: {exc}",
        )

    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip() or None
    content_length = response.headers.get("content-length")
    announced = int(content_length) if content_length and content_length.isdigit() else None
    if response.status_code != 200:
        status = response.status_code
        response.close()
        return Record(
            candidate_number, None, candidate.title, candidate.item_page,
            candidate.listing_page, candidate.pdf_url, candidate.doi, candidate.isbn,
            candidate.year, candidate.rights, None, "HTTP_ERROR", status, content_type,
            announced, None, None, checked, "PDF request did not return HTTP 200",
        )
    if announced and announced > max_bytes:
        response.close()
        return Record(
            candidate_number, None, candidate.title, candidate.item_page,
            candidate.listing_page, candidate.pdf_url, candidate.doi, candidate.isbn,
            candidate.year, candidate.rights, None, "SKIPPED_TOO_LARGE", 200,
            content_type, announced, None, None, checked,
            f"Content-Length exceeds configured limit of {max_bytes} bytes",
        )

    filename = f"{archive_number:02d}__{slugify(candidate.title)}.pdf"
    destination = output_dir / filename
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
            candidate_number, None, candidate.title, candidate.item_page,
            candidate.listing_page, candidate.pdf_url, candidate.doi, candidate.isbn,
            candidate.year, candidate.rights, None, "DOWNLOAD_FAILED", 200,
            content_type, total, None, None, checked, f"{type(exc).__name__}: {exc}",
        )
    response.close()

    if not first.startswith(b"%PDF"):
        destination.unlink(missing_ok=True)
        return Record(
            candidate_number, None, candidate.title, candidate.item_page,
            candidate.listing_page, candidate.pdf_url, candidate.doi, candidate.isbn,
            candidate.year, candidate.rights, None, "NOT_A_PDF", 200, content_type,
            total, None, None, checked, "Response lacked the %PDF signature",
        )

    return Record(
        candidate_number, archive_number, candidate.title, candidate.item_page,
        candidate.listing_page, candidate.pdf_url, candidate.doi, candidate.isbn,
        candidate.year, candidate.rights, filename, "DOWNLOADED", 200,
        content_type or "application/pdf", total, page_count(destination),
        digest.hexdigest(), checked,
        "Official IMLI publisher PDF; keep unchanged under CC BY-ND 4.0 with attribution",
    )


def write_reports(
    output_dir: Path,
    candidates: list[Candidate],
    records: list[Record],
    page_failures: list[dict[str, str]],
    target: int,
) -> dict[str, object]:
    downloaded = [record for record in records if record.status == "DOWNLOADED"]
    report: dict[str, object] = {
        "collection": COLLECTION,
        "generated_at_utc": now_utc(),
        "catalogue": CATALOGUE,
        "catalogue_pages_attempted": len(CATALOGUE_PAGES),
        "catalogue_page_failures": page_failures,
        "eligible_cc_by_nd_candidates_discovered": len(candidates),
        "candidates_processed": len(records),
        "target_downloads": target,
        "downloaded_pdfs": len(downloaded),
        "failed_or_skipped": len(records) - len(downloaded),
        "total_bytes": sum(record.bytes or 0 for record in downloaded),
        "rights_policy": (
            "Only PDF links in official ed-imli.ru Russian Literature catalogue "
            "blocks explicitly marked Creative Commons Attribution-NoDerivatives 4.0."
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
            handle.write(f"{record.sha256}  {record.file_name}\n")

    lines = [
        "# ИМЛИ РАН: 40+ PDF по русской литературе",
        "",
        f"- Создано: `{report['generated_at_utc']}`",
        f"- Найдено CC BY-ND кандидатов: `{len(candidates)}`",
        f"- Обработано кандидатов: `{len(records)}`",
        f"- Загружено действительных PDF: `{len(downloaded)}` / `{target}`",
        f"- Ошибок/пропусков: `{len(records) - len(downloaded)}`",
        f"- Общий размер: `{report['total_bytes']}` байт",
        "",
        "Каждый файл получен с официального издательского портала ИМЛИ РАН, "
        "оставлен без изменений и сопровождается карточкой, DOI/ISBN, лицензией, "
        "размером, числом страниц и SHA-256. CC BY-ND запрещает создание производных "
        "версий; извлечение иллюстраций для сайта требует отдельного решения.",
        "",
        "## Состав",
        "",
    ]
    for record in records:
        lines.append(
            f"- `{record.status}` — {record.title} — {record.file_name or 'без файла'} — "
            f"`{record.sha256 or 'без SHA-256'}` — {record.item_page}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=40)
    parser.add_argument("--max-candidates", type=int, default=100)
    parser.add_argument("--max-file-mb", type=int, default=350)
    parser.add_argument("--pause", type=float, default=1.0)
    parser.add_argument("--output-root", type=Path, default=Path("open-access-pdf-archive"))
    args = parser.parse_args()

    output_dir = args.output_root / COLLECTION
    output_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.5",
        "Accept-Language": "ru,en;q=0.8",
    })

    candidates, page_failures = discover(session)
    records: list[Record] = []
    successful = 0
    max_bytes = args.max_file_mb * 1024 * 1024
    for candidate_number, candidate in enumerate(candidates[: args.max_candidates], start=1):
        if successful >= args.target:
            break
        print(
            f"[candidate {candidate_number}/{min(len(candidates), args.max_candidates)}; "
            f"saved {successful}/{args.target}] {candidate.title}",
            flush=True,
        )
        record = download(
            session, candidate, candidate_number, successful + 1, output_dir, max_bytes
        )
        records.append(record)
        if record.status == "DOWNLOADED":
            successful += 1
        write_reports(output_dir, candidates, records, page_failures, args.target)
        time.sleep(args.pause)

    report = write_reports(output_dir, candidates, records, page_failures, args.target)
    print(json.dumps({
        "discovered": len(candidates),
        "processed": len(records),
        "downloaded": report["downloaded_pdfs"],
        "target": args.target,
        "page_failures": len(page_failures),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
