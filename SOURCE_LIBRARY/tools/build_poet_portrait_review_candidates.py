#!/usr/bin/env python3
"""Build review sheets for historical poet portrait candidates from Commons.

Unlike broad text search, this pass starts from exact person categories. It
collects open-license image records, rejects obvious non-person objects, downloads
512px review thumbnails, and builds contact sheets. Originals are not treated as
approved: a separate human selection file must choose the final reference set.
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
from PIL import Image, ImageDraw, ImageFont, ImageOps

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "TheLegendaryPoet-PortraitReview/1.0 "
    "(+https://github.com/FedorMilovanov/Research; contact: viktorcoy2012@gmail.com)"
)

PEOPLE: tuple[tuple[str, str], ...] = (
    ("Sergei Yesenin", "Sergei Yesenin"),
    ("Ivan Bunin", "Ivan Bunin"),
    ("Igor Severyanin", "Igor Severyanin"),
    ("Konstantin Balmont", "Konstantin Balmont"),
    ("Fyodor Tyutchev", "Fyodor Tyutchev"),
    ("Apollon Maykov", "Apollon Maykov"),
    ("Valery Bryusov", "Valery Bryusov"),
    ("Alexander Blok", "Alexander Blok"),
    ("Afanasy Fet", "Afanasy Fet"),
    ("Vladimir Mayakovsky", "Vladimir Mayakovsky"),
    ("Anna Akhmatova", "Anna Akhmatova"),
    ("Nikolay Gumilev", "Nikolay Gumilev"),
    ("Boris Pasternak", "Boris Pasternak"),
    ("Alexander Pushkin", "Alexander Pushkin"),
    ("Mikhail Lermontov", "Mikhail Lermontov"),
    ("Marina Tsvetaeva", "Marina Tsvetaeva"),
    ("Osip Mandelstam", "Osip Mandelstam"),
    ("Velimir Khlebnikov", "Velimir Khlebnikov"),
    ("Zinaida Gippius", "Zinaida Gippius"),
)

OPEN_LICENSE_PATTERNS = (
    "public domain", "pd-", "cc0", "cc by ", "cc-by-", "cc by-sa", "cc-by-sa",
    "creative commons attribution",
)
EXCLUDED_LICENSE_PATTERNS = (
    "fair use", "copyrighted", "noncommercial", "no derivatives", "all rights reserved",
)
ALLOWED_MIME = {"image/jpeg", "image/png", "image/tiff", "image/webp"}

BAD_OBJECT = re.compile(
    r"museum|house|grave|burial|tomb|plaque|monument|statue|bust|estate|street|"
    r"school|library|book|cover|works|autograph|signature|memorial|collection|"
    r"stamp|coin|banknote|quote|family|group|cemetery|river|reservoir|port\b|"
    r"ship\b|cruise|boat\b|vessel|letter|drawing from manuscript|manuscript|"
    r"literary prize|award|concert hall|envelope|garden|villa|room|apartment|"
    r"exhibition|poster|graffiti|mural|performance|guide\b|information|wall\b|"
    r"дом-музей|музей|дом\b|могил|захорон|таблич|памятник|стату|бюст|усадьб|"
    r"улиц|школ|библиотек|книг|облож|собрани|автограф|подпис|мемориал|"
    r"кладбищ|цитат|семь|групп|барельеф|порт\b|теплоход|корабл|судно|речн|"
    r"письм|рукопис|преми|концертн|конверт|сад\b|комнат|квартир|выстав|"
    r"плакат|граффити|исполнени|экскурсовод|информац",
    re.IGNORECASE,
)

EXT_FIELDS = "|".join([
    "LicenseShortName", "UsageTerms", "AttributionRequired", "Artist", "Credit",
    "Source", "DateTimeOriginal", "DateTime", "ImageDescription", "Categories",
])


@dataclass
class Candidate:
    person: str
    category: str
    page_id: int
    file_title: str
    description_url: str
    original_url: str
    thumb_url: str
    mime: str
    width: int | None
    height: int | None
    advertised_bytes: int | None
    license_short_name: str
    usage_terms: str
    attribution_required: str
    artist: str
    credit: str
    source: str
    date: str
    description: str
    categories: str
    review_file: str | None
    review_sha256: str | None
    status: str
    notes: str


def clean_html(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", html.unescape(value))
    return re.sub(r"\s+", " ", value).strip()


def meta(ext: dict[str, Any], key: str) -> str:
    raw = ext.get(key, {})
    if isinstance(raw, dict):
        return clean_html(str(raw.get("value", "")))
    return clean_html(str(raw))


def license_allowed(short: str, terms: str) -> bool:
    text = f"{short} {terms}".lower()
    return not any(x in text for x in EXCLUDED_LICENSE_PATTERNS) and any(
        x in text for x in OPEN_LICENSE_PATTERNS
    )


def get(session: requests.Session, url: str, *, params: dict[str, Any] | None = None, stream: bool = False) -> requests.Response:
    last: Exception | None = None
    for attempt in range(1, 5):
        try:
            response = session.get(url, params=params, stream=stream, timeout=(25, 180), allow_redirects=True)
            if response.status_code in {429, 500, 502, 503, 504} and attempt < 4:
                response.close()
                time.sleep(attempt * 3)
                continue
            return response
        except requests.RequestException as exc:
            last = exc
            if attempt < 4:
                time.sleep(attempt * 3)
                continue
    raise RuntimeError(f"request failed: {last}")


def category_titles(session: requests.Session, category: str, limit: int) -> list[str]:
    titles: list[str] = []
    continuation: dict[str, Any] = {}
    while len(titles) < limit:
        params = {
            "action": "query", "format": "json", "formatversion": 2,
            "list": "categorymembers", "cmtitle": f"Category:{category}",
            "cmnamespace": 6, "cmlimit": min(500, limit - len(titles)),
            "cmtype": "file", **continuation,
        }
        response = get(session, API, params=params)
        response.raise_for_status()
        payload = response.json()
        titles.extend(str(row["title"]) for row in payload.get("query", {}).get("categorymembers", []) if row.get("title"))
        if "continue" not in payload:
            break
        continuation = payload["continue"]
    return titles[:limit]


def search_titles(session: requests.Session, person: str, limit: int) -> list[str]:
    params = {
        "action": "query", "format": "json", "formatversion": 2,
        "list": "search", "srsearch": f'intitle:"{person}" filetype:bitmap',
        "srnamespace": 6, "srlimit": min(50, limit), "srprop": "size|timestamp",
    }
    response = get(session, API, params=params)
    response.raise_for_status()
    return [str(row["title"]) for row in response.json().get("query", {}).get("search", []) if row.get("title")]


def hydrate(session: requests.Session, person: str, category: str, titles: list[str]) -> list[Candidate]:
    output: list[Candidate] = []
    for start in range(0, len(titles), 10):
        params = {
            "action": "query", "format": "json", "formatversion": 2,
            "titles": "|".join(titles[start:start + 10]), "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 512,
            "iiextmetadatafilter": EXT_FIELDS, "iiextmetadatalanguage": "en",
            "iimetadataversion": "latest",
        }
        response = get(session, API, params=params)
        response.raise_for_status()
        for page in response.json().get("query", {}).get("pages", []):
            infos = page.get("imageinfo") or []
            if not infos:
                continue
            info = infos[0]
            ext = info.get("extmetadata") or {}
            title = str(page.get("title", ""))
            mime = str(info.get("mime", "")).lower()
            short = meta(ext, "LicenseShortName")
            terms = meta(ext, "UsageTerms")
            description = meta(ext, "ImageDescription")
            categories = meta(ext, "Categories")
            combined = f"{title} {description} {categories}"
            status, notes = "CANDIDATE", ""
            if mime not in ALLOWED_MIME:
                status, notes = "REJECTED_FORMAT", mime
            elif not license_allowed(short, terms):
                status, notes = "REJECTED_LICENSE", f"{short} / {terms}"
            elif BAD_OBJECT.search(combined):
                status, notes = "REJECTED_OBJECT_TYPE", "non-person object marker"
            elif person.lower() not in combined.lower():
                status, notes = "REJECTED_IDENTITY_TEXT", "person name absent from title/metadata"
            output.append(Candidate(
                person=person, category=category, page_id=int(page.get("pageid", 0)),
                file_title=title, description_url=str(info.get("descriptionurl", "")),
                original_url=str(info.get("url", "")), thumb_url=str(info.get("thumburl", "")),
                mime=mime, width=int(info["width"]) if info.get("width") is not None else None,
                height=int(info["height"]) if info.get("height") is not None else None,
                advertised_bytes=int(info["size"]) if info.get("size") is not None else None,
                license_short_name=short, usage_terms=terms,
                attribution_required=meta(ext, "AttributionRequired"), artist=meta(ext, "Artist"),
                credit=meta(ext, "Credit"), source=meta(ext, "Source"),
                date=meta(ext, "DateTimeOriginal") or meta(ext, "DateTime"),
                description=description, categories=categories, review_file=None,
                review_sha256=None, status=status, notes=notes,
            ))
    return output


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return value.strip("._") or "portrait"


def download_thumbnails(session: requests.Session, candidates: list[Candidate], folder: Path, per_person: int) -> None:
    accepted_by_person: dict[str, int] = {}
    seen_original: set[str] = set()
    folder.mkdir(parents=True, exist_ok=True)
    for candidate in candidates:
        if candidate.status != "CANDIDATE":
            continue
        if accepted_by_person.get(candidate.person, 0) >= per_person:
            candidate.status = "REJECTED_PERSON_CAP"
            candidate.notes = f"cap={per_person}"
            continue
        if candidate.original_url in seen_original:
            candidate.status = "REJECTED_DUPLICATE_URL"
            continue
        seen_original.add(candidate.original_url)
        try:
            response = get(session, candidate.thumb_url, stream=True)
            response.raise_for_status()
            data = response.content
            response.close()
            digest = hashlib.sha256(data).hexdigest()
            extension = ".png" if "png" in response.headers.get("content-type", "") else ".jpg"
            index = accepted_by_person.get(candidate.person, 0) + 1
            filename = f"{safe_name(candidate.person)}__{index:02d}{extension}"
            path = folder / filename
            path.write_bytes(data)
            with Image.open(path) as image:
                image.verify()
            candidate.review_file = filename
            candidate.review_sha256 = digest
            candidate.status = "REVIEW_READY"
            accepted_by_person[candidate.person] = index
        except Exception as exc:
            candidate.status = "REJECTED_THUMBNAIL"
            candidate.notes = f"{type(exc).__name__}: {exc}"


def make_contact_sheets(candidates: list[Candidate], thumb_dir: Path, output_dir: Path, people_per_sheet: int = 5) -> list[str]:
    people = [person for person, _ in PEOPLE]
    output_dir.mkdir(parents=True, exist_ok=True)
    sheets: list[str] = []
    tile_w, tile_h = 280, 350
    cols = 4
    font = ImageFont.load_default()
    for batch_start in range(0, len(people), people_per_sheet):
        batch = people[batch_start:batch_start + people_per_sheet]
        rows = sum(max(1, (len([c for c in candidates if c.person == p and c.status == "REVIEW_READY"]) + cols - 1) // cols) for p in batch)
        canvas = Image.new("RGB", (cols * tile_w, max(1, rows) * tile_h), "white")
        draw = ImageDraw.Draw(canvas)
        row = 0
        for person in batch:
            items = [c for c in candidates if c.person == person and c.status == "REVIEW_READY"]
            person_rows = max(1, (len(items) + cols - 1) // cols)
            for idx, candidate in enumerate(items):
                col = idx % cols
                local_row = idx // cols
                x, y = col * tile_w, (row + local_row) * tile_h
                with Image.open(thumb_dir / str(candidate.review_file)).convert("RGB") as image:
                    fitted = ImageOps.contain(image, (tile_w - 16, tile_h - 76))
                    px = x + (tile_w - fitted.width) // 2
                    py = y + 8
                    canvas.paste(fitted, (px, py))
                label = f"{person} #{idx + 1}\n{candidate.file_title.removeprefix('File:')[:48]}"
                draw.multiline_text((x + 8, y + tile_h - 62), label, fill="black", font=font, spacing=2)
            row += person_rows
        filename = f"portrait-review-sheet-{batch_start // people_per_sheet + 1:02d}.jpg"
        canvas.save(output_dir / filename, quality=88, optimize=True)
        sheets.append(filename)
    return sheets


def write_manifest(candidates: list[Candidate], output_dir: Path, sheets: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    records = [asdict(c) for c in candidates]
    ready = [c for c in candidates if c.status == "REVIEW_READY"]
    report = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "people": [p for p, _ in PEOPLE],
        "total_records": len(records),
        "review_ready": len(ready),
        "review_ready_by_person": {p: sum(c.person == p and c.status == "REVIEW_READY" for c in candidates) for p, _ in PEOPLE},
        "status_counts": {s: sum(c.status == s for c in candidates) for s in sorted({c.status for c in candidates})},
        "contact_sheets": sheets,
        "records": records,
    }
    (output_dir / "portrait-candidates.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(Candidate.__dataclass_fields__)
    with (output_dir / "portrait-candidates.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(asdict(candidate))
    (output_dir / "README.md").write_text(
        "# Poet portrait review candidates\n\n"
        f"Review-ready thumbnails: **{len(ready)}** across **{len(PEOPLE)}** people.\n\n"
        "These are review previews, not approved originals. Select final items by description page, then download original bytes with item-level license and attribution metadata.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--category-limit", type=int, default=120)
    parser.add_argument("--search-limit", type=int, default=40)
    parser.add_argument("--per-person", type=int, default=8)
    parser.add_argument("--minimum-ready", type=int, default=70)
    parser.add_argument("--output", default="portrait-review-output")
    args = parser.parse_args()

    output = Path(args.output)
    thumb_dir = output / "thumbnails"
    sheet_dir = output / "contact-sheets"
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json,text/html,*/*"})
    candidates: list[Candidate] = []
    seen_titles: set[str] = set()

    for person, category in PEOPLE:
        print(f"[person] {person} / Category:{category}", flush=True)
        titles = category_titles(session, category, args.category_limit)
        if len(titles) < args.per_person:
            titles.extend(search_titles(session, person, args.search_limit))
        unique = []
        for title in titles:
            if title in seen_titles:
                continue
            seen_titles.add(title)
            unique.append(title)
        hydrated = hydrate(session, person, category, unique)
        candidates.extend(hydrated)
        print(f"  titles={len(unique)} candidates={sum(c.status == 'CANDIDATE' for c in hydrated)}", flush=True)

    download_thumbnails(session, candidates, thumb_dir, args.per_person)
    sheets = make_contact_sheets(candidates, thumb_dir, sheet_dir)
    write_manifest(candidates, output, sheets)
    ready = sum(c.status == "REVIEW_READY" for c in candidates)
    print(json.dumps({"review_ready": ready, "minimum_ready": args.minimum_ready, "contact_sheets": sheets}))
    return 0 if ready >= args.minimum_ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
