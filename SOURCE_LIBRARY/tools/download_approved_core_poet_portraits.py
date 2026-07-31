#!/usr/bin/env python3
"""Download 45 manually approved Commons portrait originals, five per poet.

Selection is metadata-grounded from Commons person categories and contact-sheet
review of object type. The script does not infer identity from facial appearance.
It re-fetches current item-level rights, downloads original bytes unchanged,
validates raster images, rejects byte-identical duplicates, and enforces exactly
five successful files for each of nine core poets.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "TheLegendaryPoet-ApprovedCorePortraits/1.0 "
    "(+https://github.com/FedorMilovanov/Research; contact: viktorcoy2012@gmail.com)"
)
OPEN_LICENSE_PATTERNS = (
    "public domain", "pd-", "cc0", "cc by ", "cc-by-", "cc by-sa", "cc-by-sa",
    "creative commons attribution",
)
EXCLUDED_LICENSE_PATTERNS = (
    "fair use", "copyrighted", "noncommercial", "no derivatives", "all rights reserved",
)
EXT_FIELDS = "|".join([
    "LicenseShortName", "UsageTerms", "AttributionRequired", "Artist", "Credit",
    "Source", "DateTimeOriginal", "DateTime", "ImageDescription", "Categories",
])

SELECTED: tuple[tuple[str, str, str], ...] = (
    ("01_esenin", "Сергей Есенин", "File:Esenin1914.jpg"),
    ("01_esenin", "Сергей Есенин", "File:Esenin1925.jpg"),
    ("01_esenin", "Сергей Есенин", "File:1916. Сергей Есенин и Сергей Городецкий.jpg"),
    ("01_esenin", "Сергей Есенин", "File:Chagin and Esenin 1924.jpg"),
    ("01_esenin", "Сергей Есенин", "File:Eseninnikolaiklyeuv.jpg"),

    ("02_bunin", "Иван Бунин", "File:Ivan Bunin (sepia).jpg"),
    ("02_bunin", "Иван Бунин", "File:Ivan Bunin 1891.jpg"),
    ("02_bunin", "Иван Бунин", "File:Ivan Bunin 1933.jpg"),
    ("02_bunin", "Иван Бунин", "File:Ivan Bunin-1901.jpg"),
    ("02_bunin", "Иван Бунин", "File:Иван Бунин (1928).jpg"),

    ("03_severyanin", "Игорь Северянин", "File:Igor Severyanin 1915.jpg"),
    ("03_severyanin", "Игорь Северянин", "File:Igor Severyanin by Leonidov.jpg"),
    ("03_severyanin", "Игорь Северянин", "File:Igor Severyanin by Lev Leonidov.JPG"),
    ("03_severyanin", "Игорь Северянин", "File:Igor Severyanin.jpg"),
    ("03_severyanin", "Игорь Северянин", "File:Igor Severyanin by Viktor Deni.jpg"),

    ("04_balmont", "Константин Бальмонт", "File:Balm1892.jpg"),
    ("04_balmont", "Константин Бальмонт", "File:Balmont 1880s.jpg"),
    ("04_balmont", "Константин Бальмонт", "File:Balmont by Voloshin.JPG"),
    ("04_balmont", "Константин Бальмонт", "File:Balmont KD.jpg"),
    ("04_balmont", "Константин Бальмонт", "File:Konstantin Balmont 1928.jpg"),

    ("05_tyutchev", "Фёдор Тютчев", "File:1864. Тютчев.jpg"),
    ("05_tyutchev", "Фёдор Тютчев", "File:1865. Тютчев в Париже.jpg"),
    ("05_tyutchev", "Фёдор Тютчев", "File:1867. Тютчев.jpg"),
    ("05_tyutchev", "Фёдор Тютчев", "File:Fyodor Tyutchev.jpg"),
    ("05_tyutchev", "Фёдор Тютчев", "File:Tiutchev.jpg"),

    ("06_maykov", "Аполлон Майков", "File:Apollon Maykov.jpg"),
    ("06_maykov", "Аполлон Майков", "File:Perov-Maikov.jpg"),
    ("06_maykov", "Аполлон Майков", "File:Apollon Maikov.jpg"),
    ("06_maykov", "Аполлон Майков", "File:Maikov AN.jpg"),
    ("06_maykov", "Аполлон Майков", "File:Портрет А.Н.Майкова.jpg"),

    ("07_bryusov", "Валерий Брюсов", "File:Brusov1920-2.jpg"),
    ("07_bryusov", "Валерий Брюсов", "File:Brusov.jpg"),
    ("07_bryusov", "Валерий Брюсов", "File:Brusov1890.PNG"),
    ("07_bryusov", "Валерий Брюсов", "File:Brjussow, Waleri (Moskauer Almanach, 1914).jpeg"),
    ("07_bryusov", "Валерий Брюсов", "File:1903. Портрет В.Я. Брюсова.jpg"),

    ("08_blok", "Александр Блок", "File:A. A. Blok.jpg"),
    ("08_blok", "Александр Блок", "File:Alexander Blok by Ivan Parkhomenko 1910.jpg"),
    ("08_blok", "Александр Блок", "File:Alexander Blok.jpeg"),
    ("08_blok", "Александр Блок", "File:Blok AA.jpg"),
    ("08_blok", "Александр Блок", "File:Александр Блок. 1898 год.jpg"),

    ("09_fet", "Афанасий Фет", "File:Afanasy Fet 7.jpg"),
    ("09_fet", "Афанасий Фет", "File:Afanasy Fet.jpg"),
    ("09_fet", "Афанасий Фет", "File:Fet A A.jpg"),
    ("09_fet", "Афанасий Фет", "File:Fet as officer (ca. 1850) 2.jpg"),
    ("09_fet", "Афанасий Фет", "File:Fet by Repin.jpg"),
)


@dataclass
class Record:
    number: int
    poet_key: str
    poet_name: str
    file_title: str
    local_file_name: str | None
    description_url: str
    original_url: str
    mime: str
    width: int | None
    height: int | None
    advertised_bytes: int | None
    downloaded_bytes: int | None
    sha256: str | None
    license_short_name: str
    usage_terms: str
    attribution_required: str
    artist: str
    credit: str
    source: str
    date: str
    image_description: str
    categories: str
    status: str
    notes: str
    checked_at_utc: str


def clean_html(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(value))).strip()


def meta(ext: dict[str, Any], key: str) -> str:
    raw = ext.get(key, {})
    return clean_html(str(raw.get("value", ""))) if isinstance(raw, dict) else clean_html(str(raw))


def license_allowed(short: str, terms: str) -> bool:
    text = f"{short} {terms}".lower()
    return not any(x in text for x in EXCLUDED_LICENSE_PATTERNS) and any(
        x in text for x in OPEN_LICENSE_PATTERNS
    )


def request(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    stream: bool = False,
) -> requests.Response:
    last: Exception | None = None
    for attempt in range(1, 7):
        time.sleep(0.35 if not stream else 0.10)
        try:
            response = session.get(
                url,
                params=params,
                stream=stream,
                allow_redirects=True,
                timeout=(30, 360),
            )
            if response.status_code == 429:
                raw = response.headers.get("Retry-After", "")
                try:
                    wait = float(raw)
                except ValueError:
                    wait = attempt * 8.0
                response.close()
                if attempt < 6:
                    time.sleep(min(max(wait, 5.0), 90.0))
                    continue
            if response.status_code in {500, 502, 503, 504} and attempt < 6:
                response.close()
                time.sleep(min(attempt * 5.0, 45.0))
                continue
            return response
        except requests.RequestException as exc:
            last = exc
            if attempt < 6:
                time.sleep(min(attempt * 5.0, 45.0))
                continue
            raise
    raise RuntimeError(f"request failed: {last}")


def hydrate(session: requests.Session, titles: list[str]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for start in range(0, len(titles), 10):
        params = {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "titles": "|".join(titles[start : start + 10]),
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiextmetadatafilter": EXT_FIELDS,
            "iiextmetadatalanguage": "en",
            "iimetadataversion": "latest",
        }
        response = request(session, API, params=params)
        response.raise_for_status()
        for page in response.json().get("query", {}).get("pages", []):
            title = str(page.get("title", ""))
            infos = page.get("imageinfo") or []
            if infos:
                output[title] = infos[0]
    return output


def safe_stem(title: str, limit: int = 92) -> str:
    stem = title.removeprefix("File:")
    stem = re.sub(r"\.[A-Za-z0-9]{2,5}$", "", stem)
    stem = re.sub(r'[\\/:*?"<>|]+', "_", stem)
    return re.sub(r"\s+", " ", stem).strip(" ._")[:limit] or "portrait"


def extension_for(mime: str, original_url: str) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/tiff": ".tif",
        "image/webp": ".webp",
    }
    return mapping.get(mime) or Path(original_url.split("?", 1)[0]).suffix or ".bin"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="approved-core-poet-portraits-45")
    parser.add_argument("--max-file-mb", type=int, default=100)
    parser.add_argument("--pause", type=float, default=0.25)
    args = parser.parse_args()

    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=True)
    max_bytes = args.max_file_mb * 1024 * 1024
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Api-User-Agent": USER_AGENT,
        "Accept": "application/json,image/*,*/*;q=0.8",
        "Referer": "https://commons.wikimedia.org/",
    })
    current = hydrate(session, [title for _, _, title in SELECTED])
    records: list[Record] = []
    seen_sha: set[str] = set()
    per_poet_index: dict[str, int] = {}

    for number, (poet_key, poet_name, title) in enumerate(SELECTED, start=1):
        checked = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        info = current.get(title)
        blank = dict(
            number=number,
            poet_key=poet_key,
            poet_name=poet_name,
            file_title=title,
            local_file_name=None,
            description_url="",
            original_url="",
            mime="",
            width=None,
            height=None,
            advertised_bytes=None,
            downloaded_bytes=None,
            sha256=None,
            license_short_name="",
            usage_terms="",
            attribution_required="",
            artist="",
            credit="",
            source="",
            date="",
            image_description="",
            categories="",
            status="",
            notes="",
            checked_at_utc=checked,
        )
        if not info:
            records.append(Record(**{**blank, "status": "MISSING", "notes": "Commons item not returned"}))
            continue

        ext = info.get("extmetadata") or {}
        short = meta(ext, "LicenseShortName")
        terms = meta(ext, "UsageTerms")
        original = str(info.get("url", ""))
        description_url = str(info.get("descriptionurl", ""))
        mime = str(info.get("mime", "")).lower()
        advertised = int(info["size"]) if info.get("size") is not None else None
        base = {
            **blank,
            "description_url": description_url,
            "original_url": original,
            "mime": mime,
            "width": int(info["width"]) if info.get("width") is not None else None,
            "height": int(info["height"]) if info.get("height") is not None else None,
            "advertised_bytes": advertised,
            "license_short_name": short,
            "usage_terms": terms,
            "attribution_required": meta(ext, "AttributionRequired"),
            "artist": meta(ext, "Artist"),
            "credit": meta(ext, "Credit"),
            "source": meta(ext, "Source"),
            "date": meta(ext, "DateTimeOriginal") or meta(ext, "DateTime"),
            "image_description": meta(ext, "ImageDescription"),
            "categories": meta(ext, "Categories"),
        }

        if mime not in {"image/jpeg", "image/png", "image/tiff", "image/webp"}:
            records.append(Record(**{**base, "status": "REJECTED_FORMAT", "notes": mime}))
            continue
        if not license_allowed(short, terms):
            records.append(Record(**{**base, "status": "REJECTED_LICENSE", "notes": f"{short}/{terms}"}))
            continue
        if advertised and advertised > max_bytes:
            records.append(Record(**{**base, "status": "REJECTED_SIZE", "notes": f"> {max_bytes}"}))
            continue

        response: requests.Response | None = None
        destination: Path | None = None
        try:
            response = request(session, original, stream=True)
            response.raise_for_status()
            poet_dir = root / poet_key
            poet_dir.mkdir(parents=True, exist_ok=True)
            index = per_poet_index.get(poet_key, 0) + 1
            local_name = f"{index:02d}__{safe_stem(title)}{extension_for(mime, original)}"
            destination = poet_dir / local_name
            digest = hashlib.sha256()
            size = 0
            with destination.open("wb") as handle:
                for chunk in response.iter_content(1024 * 1024):
                    if not chunk:
                        continue
                    size += len(chunk)
                    if size > max_bytes:
                        raise ValueError("stream exceeds file limit")
                    digest.update(chunk)
                    handle.write(chunk)
            response.close()
            response = None
            with Image.open(destination) as image:
                image.verify()
            sha = digest.hexdigest()
            if sha in seen_sha:
                destination.unlink(missing_ok=True)
                records.append(Record(**{
                    **base,
                    "downloaded_bytes": size,
                    "sha256": sha,
                    "status": "DUPLICATE_SHA256",
                    "notes": "byte-identical duplicate rejected",
                }))
                continue
            seen_sha.add(sha)
            per_poet_index[poet_key] = index
            records.append(Record(**{
                **base,
                "local_file_name": f"{poet_key}/{local_name}",
                "downloaded_bytes": size,
                "sha256": sha,
                "status": "DOWNLOADED",
                "notes": "manual portrait-type allowlist; identity grounded in Commons metadata",
            }))
            print(f"[saved] {number}/{len(SELECTED)} {poet_name} — {local_name}", flush=True)
        except Exception as exc:
            if response is not None:
                response.close()
            if destination is not None:
                destination.unlink(missing_ok=True)
            records.append(Record(**{
                **base,
                "status": "DOWNLOAD_FAILED",
                "notes": f"{type(exc).__name__}: {exc}",
            }))
        time.sleep(args.pause)

    downloaded = [r for r in records if r.status == "DOWNLOADED"]
    counts_by_poet = {
        poet_name: sum(r.poet_name == poet_name and r.status == "DOWNLOADED" for r in records)
        for _, poet_name, _ in SELECTED
    }
    counts_by_poet = dict.fromkeys(counts_by_poet, 0) | counts_by_poet
    report = {
        "collection": "approved-core-poet-portraits-45",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "selected": len(SELECTED),
        "downloaded": len(downloaded),
        "total_bytes": sum(r.downloaded_bytes or 0 for r in downloaded),
        "counts_by_poet": counts_by_poet,
        "license_counts": {
            license_name: sum(r.license_short_name == license_name for r in downloaded)
            for license_name in sorted({r.license_short_name for r in downloaded})
        },
        "status_counts": {
            status: sum(r.status == status for r in records)
            for status in sorted({r.status for r in records})
        },
        "records": [asdict(r) for r in records],
    }
    (root / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(Record.__dataclass_fields__)
    with (root / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))
    with (root / "SHA256SUMS.txt").open("w", encoding="utf-8") as handle:
        for record in downloaded:
            handle.write(f"{record.sha256}  {record.local_file_name}\n")
    (root / "README.md").write_text(
        "# Approved core poet portrait references\n\n"
        f"Selected: **{len(SELECTED)}**  \n"
        f"Downloaded: **{len(downloaded)}**  \n"
        f"Total bytes: **{report['total_bytes']}**  \n"
        f"Counts: `{counts_by_poet}`\n\n"
        "Files were selected as portrait-type references from metadata-grounded Commons candidates. "
        "Identity and production use remain tied to each item page and credit line.\n",
        encoding="utf-8",
    )

    failures = {name: count for name, count in counts_by_poet.items() if count != 5}
    print(json.dumps({
        "selected": report["selected"],
        "downloaded": report["downloaded"],
        "total_bytes": report["total_bytes"],
        "counts_by_poet": counts_by_poet,
        "license_counts": report["license_counts"],
        "status_counts": report["status_counts"],
        "failures": failures,
    }, ensure_ascii=False))
    return 0 if len(downloaded) == 45 and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
