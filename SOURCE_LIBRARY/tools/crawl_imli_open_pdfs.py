#!/usr/bin/env python3
"""Download open-access PDFs from the official IMLI RAN digital library.

The IMLI landing page states that its PDFs are made openly available with
rights-holder consent. This tool deliberately crawls only biblio.imli.ru and
stores provenance, landing pages, hashes, sizes and page counts beside every
successful download. It does not crawl Academia, ResearchGate, mirrors, cloud
shares, or facsimile repositories with publication restrictions.
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
from typing import Iterable
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

BASE = "https://biblio.imli.ru"
USER_AGENT = (
    "TheLegendaryPoet-ResearchArchive/1.0 "
    "(+https://github.com/FedorMilovanov/Research)"
)

COLLECTIONS = {
    "esenin": {
        "title": "Сергей Есенин — ИМЛИ РАН",
        "category_url": f"{BASE}/index.php/ruslit/527-esenin-s-a",
        "expected_items": 19,
        "extra_items": [],
    },
    "blok": {
        "title": "Александр Блок — ИМЛИ РАН",
        "category_url": f"{BASE}/index.php/ruslit/514-blok-a-a",
        "expected_items": 13,
        "extra_items": [],
    },
    "khlebnikov": {
        "title": "Велимир Хлебников — ИМЛИ РАН",
        "category_url": f"{BASE}/index.php/ruslit/525-velimir-khlebnikov",
        "expected_items": 7,
        "extra_items": [],
    },
    "silver-age-general": {
        "title": "Серебряный век — общие академические труды ИМЛИ РАН",
        "category_url": None,
        "expected_items": 4,
        "extra_items": [
            f"{BASE}/index.php/ruslit/412-poetika-russkoj-literatury-kontca-xix-nachala-xx",
            f"{BASE}/index.php/ruslit/237-russkaya-literatura-rubezha-vekov-1890-e-nachalo-1920",
            f"{BASE}/index.php/ruslit/162-istoriya-russkoj-literatury-xx-veka-1920-1930-e-gg",
            f"{BASE}/index.php/ruslit/707-keldysh-v-a-o-serebryanom-veke-russkoj-literatury-obshchie-zakonomernosti-problemy-prozy-2010",
        ],
    },
}


@dataclass
class Record:
    collection: str
    title: str
    landing_page: str
    pdf_url: str | None
    file_name: str | None
    status: str
    http_status: int | None
    content_type: str | None
    bytes: int | None
    pages: int | None
    sha256: str | None
    downloaded_at_utc: str
    rights_status: str
    source_authority: str
    notes: str


def now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str, max_length: int = 150) -> str:
    value = unicodedata.normalize("NFKC", unquote(value))
    value = value.replace("—", "-").replace("–", "-")
    value = re.sub(r"[\\/:*?\"<>|]+", "_", value)
    value = re.sub(r"\s+", " ", value).strip(" ._")
    return (value[:max_length].rstrip(" ._") or "document")


def request(session: requests.Session, url: str, *, stream: bool = False) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, 5):
        try:
            response = session.get(
                url,
                timeout=(20, 180),
                allow_redirects=True,
                stream=stream,
            )
            if response.status_code in {429, 500, 502, 503, 504} and attempt < 4:
                response.close()
                time.sleep(attempt * 4)
                continue
            return response
        except requests.RequestException as exc:
            last_error = exc
            if attempt < 4:
                time.sleep(attempt * 4)
                continue
            raise
    raise RuntimeError(f"request failed: {url}: {last_error}")


def category_item_links(session: requests.Session, category_url: str) -> list[str]:
    response = request(session, category_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    category_path = urlparse(category_url).path.rstrip("/") + "/"
    links: list[str] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        absolute = urljoin(category_url, anchor["href"])
        parsed = urlparse(absolute)
        if parsed.netloc != urlparse(BASE).netloc:
            continue
        if not parsed.path.startswith(category_path):
            continue
        if parsed.path.rstrip("/") == category_path.rstrip("/"):
            continue
        # Item pages use one slug beneath the category; exclude assets and feeds.
        tail = parsed.path[len(category_path):].strip("/")
        if not tail or "/" in tail or tail.endswith((".jpg", ".png", ".webp", ".xml")):
            continue
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if normalized not in seen:
            seen.add(normalized)
            links.append(normalized)
    return links


def extract_item(session: requests.Session, landing_page: str) -> tuple[str, str]:
    response = request(session, landing_page)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title_node = soup.find("h1")
    title = clean_text(title_node.get_text(" ", strip=True)) if title_node else landing_page
    candidates: list[str] = []
    for anchor in soup.find_all("a", href=True):
        absolute = urljoin(landing_page, anchor["href"])
        parsed = urlparse(absolute)
        if parsed.netloc != urlparse(BASE).netloc:
            continue
        if ".pdf" in parsed.path.lower():
            candidates.append(absolute)
    if not candidates:
        raise LookupError("official item page contains no PDF link")
    # Prefer the direct IMLI storage path over any incidental link.
    candidates.sort(key=lambda url: ("/images/abook/" not in url, len(url)))
    return title, candidates[0]


def count_pages(path: Path) -> int | None:
    try:
        return len(PdfReader(str(path)).pages)
    except Exception:
        return None


def download_pdf(
    session: requests.Session,
    collection: str,
    index: int,
    title: str,
    landing_page: str,
    pdf_url: str,
    output_dir: Path,
) -> Record:
    response = request(session, pdf_url, stream=True)
    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip()
    if response.status_code != 200:
        response.close()
        return Record(
            collection, title, landing_page, pdf_url, None, "HTTP_ERROR",
            response.status_code, content_type or None, None, None, None,
            now_utc(), "DOWNLOAD-OK", "IMLI RAN official digital library",
            "PDF request did not return HTTP 200",
        )

    url_name = Path(unquote(urlparse(response.url).path)).name
    stem = slugify(Path(url_name).stem if url_name.lower().endswith(".pdf") else title)
    filename = f"{index:02d}__{stem}.pdf"
    destination = output_dir / filename
    digest = hashlib.sha256()
    total = 0
    first = b""
    with destination.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if not chunk:
                continue
            if not first:
                first = chunk[:8]
            handle.write(chunk)
            digest.update(chunk)
            total += len(chunk)
    response.close()

    if not first.startswith(b"%PDF"):
        destination.unlink(missing_ok=True)
        return Record(
            collection, title, landing_page, pdf_url, None, "NOT_A_PDF",
            response.status_code, content_type or None, total, None, None,
            now_utc(), "DOWNLOAD-OK", "IMLI RAN official digital library",
            "Downloaded response did not begin with the PDF signature",
        )

    return Record(
        collection, title, landing_page, pdf_url, filename, "DOWNLOADED",
        response.status_code, content_type or "application/pdf", total,
        count_pages(destination), digest.hexdigest(), now_utc(), "DOWNLOAD-OK",
        "IMLI RAN official digital library",
        "Official open-access PDF; preserve this manifest with the file",
    )


def write_reports(collection: str, output_dir: Path, records: list[Record], expected: int) -> None:
    payload = {
        "collection": collection,
        "generated_at_utc": now_utc(),
        "source_policy": (
            "Only official biblio.imli.ru item pages and their direct PDF links. "
            "IMLI states that PDFs are openly published with rights-holder consent."
        ),
        "expected_item_pages": expected,
        "discovered_item_pages": len(records),
        "downloaded": sum(record.status == "DOWNLOADED" for record in records),
        "failed": sum(record.status != "DOWNLOADED" for record in records),
        "total_bytes": sum(record.bytes or 0 for record in records if record.status == "DOWNLOADED"),
        "records": [asdict(record) for record in records],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (output_dir / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        fields = list(asdict(records[0]).keys()) if records else list(Record.__annotations__)
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))

    lines = [
        f"# {COLLECTIONS[collection]['title']}",
        "",
        f"- Generated: `{payload['generated_at_utc']}`",
        f"- Expected item pages: `{expected}`",
        f"- Discovered/processed: `{len(records)}`",
        f"- Downloaded PDFs: `{payload['downloaded']}`",
        f"- Failed/HOLD: `{payload['failed']}`",
        f"- Total bytes: `{payload['total_bytes']}`",
        "",
        "## Rights and provenance",
        "",
        "All downloads originate from the official IMLI RAN digital library. "
        "Its public landing page states that PDFs are offered in open access with "
        "rights-holder consent. The archive is for private research and controlled "
        "editorial use; every future publication must still retain attribution and "
        "check the exact item page.",
        "",
        "## Files",
        "",
    ]
    for record in records:
        lines.append(
            f"- `{record.status}` — {record.title} — "
            f"{record.file_name or 'no file'} — `{record.sha256 or 'no hash'}` — "
            f"{record.landing_page}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", choices=sorted(COLLECTIONS), required=True)
    parser.add_argument("--output-root", type=Path, default=Path("open-access-pdf-archive"))
    parser.add_argument("--pause", type=float, default=0.8)
    args = parser.parse_args()

    config = COLLECTIONS[args.collection]
    output_dir = args.output_root / args.collection
    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.5"})

    item_pages: list[str] = []
    if config["category_url"]:
        item_pages.extend(category_item_links(session, str(config["category_url"])))
    item_pages.extend(str(url) for url in config["extra_items"])
    item_pages = list(dict.fromkeys(item_pages))

    records: list[Record] = []
    for index, landing_page in enumerate(item_pages, start=1):
        print(f"[{args.collection} {index}/{len(item_pages)}] {landing_page}", flush=True)
        try:
            title, pdf_url = extract_item(session, landing_page)
            record = download_pdf(
                session, args.collection, index, title, landing_page, pdf_url, output_dir
            )
        except Exception as exc:
            record = Record(
                args.collection,
                landing_page,
                landing_page,
                None,
                None,
                "FAILED",
                None,
                None,
                None,
                None,
                None,
                now_utc(),
                "HOLD",
                "IMLI RAN item page expected",
                f"{type(exc).__name__}: {exc}",
            )
        records.append(record)
        write_reports(args.collection, output_dir, records, int(config["expected_items"]))
        time.sleep(args.pause)

    downloaded = sum(record.status == "DOWNLOADED" for record in records)
    print(
        json.dumps(
            {
                "collection": args.collection,
                "discovered": len(records),
                "downloaded": downloaded,
                "expected": config["expected_items"],
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    # A transient failure must not suppress manifests/artifacts. The report carries
    # exact status; the workflow summary enforces the global 40+ review threshold.
    return 0


if __name__ == "__main__":
    sys.exit(main())
