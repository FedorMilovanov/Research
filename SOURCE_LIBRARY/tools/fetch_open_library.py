#!/usr/bin/env python3
"""Download a rights-reviewed whitelist of open research assets.

This script is intentionally conservative:
- it downloads only items classified DOWNLOAD-OK in the source index;
- it never downloads IAA 4Q204 or Vatican P72 facsimiles;
- every downloaded file receives provenance metadata and SHA-256;
- failures are recorded instead of being silently ignored.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen

USER_AGENT = (
    "TheLegendaryPoet-ResearchSourceLibrary/1.0 "
    "(+https://github.com/FedorMilovanov/Research)"
)
TIMEOUT = 120
RETRIES = 3

COLLECTIONS: dict[str, list[dict[str, str]]] = {
    "esenin-letopis": [
        {
            "name": "letopis-tom-1.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/821-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-1",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "letopis-tom-2.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/822-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-2",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "letopis-tom-3-kniga-1.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/823-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-3",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "letopis-tom-3-kniga-2.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/824-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-3-kniga-2",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "letopis-tom-4.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/825-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-4",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "letopis-tom-5-kniga-1.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/component/abook/book/826-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-5?Itemid=0&catid=527%3Aesenin-s-a",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
    ],
    "esenin-pss": [
        {
            "name": "esenin-pss-tom-1.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/688-esenin-s-a-pss-v-7-tomakh-t-1-1995",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-2.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/689-esenin-s-a-pss-v-7-tomakh-t-2-1997",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-3.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/690-esenin-s-a-pss-v-7-tomakh-t-3-1998",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-4.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/691-esenin-s-a-pss-v-7-tomakh-t-4-2004",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-5.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/692-esenin-s-a-pss-v-7-tomakh-t-5-2005",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-6.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/693-esenin-s-a-pss-v-7-tomakh-t-6-2005",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-7-kniga-1.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/557-esenin-s-a-pss-v-7-tomakh-t-7-kn-1-1999",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-7-kniga-2.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/694-esenin-s-a-pss-v-7-tomakh-t-7-kn-2-2000",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
        {
            "name": "esenin-pss-tom-7-kniga-3.pdf",
            "type": "page_pdf",
            "url": "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/695-esenin-s-a-pss-v-7-tomakh-t-7-kn-3-2002",
            "rights": "Official IMLI open-access PDF; rights-holder consent stated by IMLI",
        },
    ],
    "duncan-public-domain": [
        {
            "name": "isadora-duncan-my-life.pdf",
            "type": "direct",
            "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/My_Life_(IA_mylife00dunc).pdf",
            "rights": "Public-domain book; verify the Commons item page and preserve attribution",
        },
        {
            "name": "loc-isadora-2018708185.jpg",
            "type": "loc_large_jpeg",
            "url": "https://www.loc.gov/pictures/item/2018708185/",
            "rights": "Library of Congress: no known restrictions on publication; Genthe credit required",
        },
        {
            "name": "loc-isadora-2018709542.jpg",
            "type": "loc_large_jpeg",
            "url": "https://www.loc.gov/pictures/item/2018709542/",
            "rights": "Library of Congress: no known restrictions on publication; Genthe credit required",
        },
        {
            "name": "loc-isadora-2018709521.jpg",
            "type": "loc_large_jpeg",
            "url": "https://www.loc.gov/pictures/item/2018709521/",
            "rights": "Library of Congress: no known restrictions on publication; Genthe credit required",
        },
        {
            "name": "loc-isadora-2018708261.jpg",
            "type": "loc_large_jpeg",
            "url": "https://www.loc.gov/pictures/item/2018708261/",
            "rights": "Library of Congress: no known restrictions on publication; Genthe credit required",
        },
        {
            "name": "loc-isadora-2018708251.jpg",
            "type": "loc_large_jpeg",
            "url": "https://www.loc.gov/pictures/item/2018708251/",
            "rights": "Library of Congress: no known restrictions on publication; Genthe credit required",
        },
        {
            "name": "loc-isadora-2018703975.jpg",
            "type": "loc_large_jpeg",
            "url": "https://www.loc.gov/pictures/item/2018703975/",
            "rights": "Library of Congress: no known restrictions on publication; Genthe credit required",
        },
        {
            "name": "loc-isadora-2018708189.jpg",
            "type": "loc_large_jpeg",
            "url": "https://www.loc.gov/pictures/item/2018708189/",
            "rights": "Library of Congress: no known restrictions on publication; Genthe credit required",
        },
    ],
    "manuscript-open-resources": [
        {
            "name": "sblgnt-master.zip",
            "type": "direct",
            "url": "https://github.com/Faithlife/SBLGNT/archive/refs/heads/master.zip",
            "rights": "SBLGNT source files, CC BY 4.0",
        },
        {
            "name": "4q204-qumran-digital-2026-02-11.html",
            "type": "direct",
            "url": "https://lexicon.qumran-digital.org/transcriptions/4Q204/2026-02-11/index.html?v=2026-02-11",
            "rights": "Qumran-Digital transcription, CC BY-SA 4.0; page snapshot is research evidence",
        },
        {
            "name": "drawnel-introductory-bibliography-1-enoch.pdf",
            "type": "direct",
            "url": "https://bibliotekanauki.pl/articles/1051067.pdf",
            "rights": "Open-access scholarly article; not the 2019 critical edition",
        },
        {
            "name": "drawnel-2019-book-review.pdf",
            "type": "direct",
            "url": "https://journals.us.edu.pl/index.php/ssht/article/view/11533/10227",
            "rights": "Open-access review; not the copyrighted book",
        },
    ],
}


def fetch_bytes(url: str) -> tuple[bytes, str, str | None]:
    last_error: Exception | None = None
    for attempt in range(1, RETRIES + 1):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=TIMEOUT) as response:
                data = response.read()
                final_url = response.geturl()
                content_type = response.headers.get("Content-Type")
                return data, final_url, content_type
        except Exception as exc:  # noqa: BLE001 - recorded in provenance
            last_error = exc
            if attempt < RETRIES:
                time.sleep(attempt * 3)
    assert last_error is not None
    raise last_error


def resolve_url(item: dict[str, str]) -> tuple[str, str | None]:
    source_type = item["type"]
    landing = item["url"]
    if source_type == "direct":
        return landing, None

    page_bytes, final_page, _ = fetch_bytes(landing)
    page = html.unescape(page_bytes.decode("utf-8", errors="replace"))

    if source_type == "page_pdf":
        patterns = [
            r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
            r'(https?://[^\s"\']+\.pdf(?:\?[^\s"\']*)?)',
        ]
        candidates: list[str] = []
        for pattern in patterns:
            candidates.extend(re.findall(pattern, page, flags=re.IGNORECASE))
        if not candidates:
            raise RuntimeError(f"No PDF link found on {landing}")
        return urljoin(final_page, candidates[0]), final_page

    if source_type == "loc_large_jpeg":
        candidates = re.findall(
            r'https://tile\.loc\.gov/[^\s"\']+v\.jpg', page, flags=re.IGNORECASE
        )
        if not candidates:
            raise RuntimeError(f"No LOC large JPEG found on {landing}")
        return candidates[0], final_page

    raise ValueError(f"Unsupported source type: {source_type}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_item(item: dict[str, str], output_dir: Path) -> dict[str, Any]:
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    record: dict[str, Any] = {
        "file_name": item["name"],
        "landing_page": item["url"],
        "source_type": item["type"],
        "rights_status": "DOWNLOAD-OK",
        "rights_note": item["rights"],
        "started_at": started,
    }
    try:
        resolved_url, resolved_landing = resolve_url(item)
        data, final_url, content_type = fetch_bytes(resolved_url)
        target = output_dir / item["name"]
        target.write_bytes(data)
        record.update(
            {
                "status": "downloaded",
                "resolved_landing_page": resolved_landing,
                "resolved_url": resolved_url,
                "final_url": final_url,
                "content_type": content_type,
                "bytes": target.stat().st_size,
                "sha256": sha256_file(target),
                "downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
        )
    except Exception as exc:  # noqa: BLE001 - preserve failure evidence
        record.update(
            {
                "status": "failed",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "failed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
        )
    return record


def write_readme(collection: str, output_dir: Path, records: list[dict[str, Any]]) -> None:
    downloaded = sum(record["status"] == "downloaded" for record in records)
    failed = len(records) - downloaded
    text = f"""OPEN SOURCE LIBRARY ARTIFACT

Collection: {collection}
Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}
Downloaded: {downloaded}
Failed: {failed}

This artifact was produced from the rights-reviewed whitelist in:
https://github.com/FedorMilovanov/Research/blob/main/SOURCE_LIBRARY/MASTER_OPEN_ACCESS_SOURCE_INDEX_2026-07-30.md

Important:
- IAA 4Q204 and Vatican P72 facsimiles are intentionally excluded.
- Review provenance.json before any publication.
- Preserve credit lines and licence notices.
- A successful download is not by itself a licence; the recorded rights note controls use.
"""
    (output_dir / "README.txt").write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("collection", choices=sorted(COLLECTIONS))
    parser.add_argument("--output", type=Path, default=Path("source-library-output"))
    args = parser.parse_args()

    output_dir = args.output / args.collection
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    records: list[dict[str, Any]] = []
    for item in COLLECTIONS[args.collection]:
        print(f"Fetching {item['name']} from {item['url']}", flush=True)
        record = download_item(item, output_dir)
        records.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)

    manifest = {
        "schema": "thelegendarypoet.source-library.provenance.v1",
        "collection": args.collection,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "records": records,
    }
    (output_dir / "provenance.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_readme(args.collection, output_dir, records)

    downloaded = sum(record["status"] == "downloaded" for record in records)
    print(f"Downloaded {downloaded}/{len(records)} items", flush=True)
    return 0 if downloaded else 1


if __name__ == "__main__":
    sys.exit(main())
