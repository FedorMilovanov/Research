#!/usr/bin/env python3
"""Strict recursive-category portrait candidate builder.

The first category-first pass still admitted documents and related objects from
root person categories. This v2 traverses only portrait-oriented subcategories,
uses strict exact-name fallback searches, excludes work/place/object categories,
and builds a second human-review package. It does not identify people by model;
identity remains grounded in the Commons category/file metadata and requires
manual review before original download.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "TheLegendaryPoet-PortraitReviewV2/1.0 "
    "(+https://github.com/FedorMilovanov/Research; contact: viktorcoy2012@gmail.com)"
)

PEOPLE: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("Sergei Yesenin", "Sergei Yesenin", ("Sergey Esenin", "Сергей Есенин")),
    ("Ivan Bunin", "Ivan Bunin", ("Иван Бунин",)),
    ("Igor Severyanin", "Igor Severyanin", ("Игорь Северянин",)),
    ("Konstantin Balmont", "Konstantin Balmont", ("Константин Бальмонт",)),
    ("Fyodor Tyutchev", "Fyodor Tyutchev", ("Fedor Tyutchev", "Фёдор Тютчев", "Федор Тютчев")),
    ("Apollon Maykov", "Apollon Maykov", ("Apollon Maikov", "Аполлон Майков")),
    ("Valery Bryusov", "Valery Bryusov", ("Valeriy Bryusov", "Валерий Брюсов")),
    ("Alexander Blok", "Alexander Blok", ("Александр Блок",)),
    ("Afanasy Fet", "Afanasy Fet", ("Afanasy Shenshin", "Афанасий Фет", "Афанасий Шеншин")),
    ("Vladimir Mayakovsky", "Vladimir Mayakovsky", ("Владимир Маяковский",)),
    ("Anna Akhmatova", "Anna Akhmatova", ("Анна Ахматова",)),
    ("Nikolay Gumilev", "Nikolay Gumilev", ("Nikolai Gumilev", "Николай Гумилёв", "Николай Гумилев")),
    ("Boris Pasternak", "Boris Pasternak", ("Борис Пастернак",)),
    ("Alexander Pushkin", "Alexander Pushkin", ("Александр Пушкин",)),
    ("Mikhail Lermontov", "Mikhail Lermontov", ("Михаил Лермонтов",)),
    ("Marina Tsvetaeva", "Marina Tsvetaeva", ("Марина Цветаева",)),
    ("Osip Mandelstam", "Osip Mandelstam", ("Осип Мандельштам",)),
    ("Velimir Khlebnikov", "Velimir Khlebnikov", ("Velemir Khlebnikov", "Велимир Хлебников")),
    ("Zinaida Gippius", "Zinaida Gippius", ("Zinaida Hippius", "Зинаида Гиппиус")),
)

OPEN_LICENSE_PATTERNS = (
    "public domain", "pd-", "cc0", "cc by ", "cc-by-", "cc by-sa", "cc-by-sa",
    "creative commons attribution",
)
EXCLUDED_LICENSE_PATTERNS = (
    "fair use", "copyrighted", "noncommercial", "no derivatives", "all rights reserved",
)
ALLOWED_MIME = {"image/jpeg", "image/png", "image/tiff", "image/webp"}

GOOD_CATEGORY = re.compile(
    r"portrait|photograph|photo\b|paintings? of|drawings? of|caricatures? of|"
    r"portraits? de|portraits? von|retratos|портрет|фотограф|карикатур|изображени",
    re.IGNORECASE,
)
BAD_CATEGORY = re.compile(
    r"museum|house|home|grave|burial|tomb|monument|statue|bust|memorial|"
    r"street|place|estate|school|library|books?|works?|poems?|manuscripts?|"
    r"letters?|autographs?|awards?|prizes?|stamps?|coins?|ships?|vehicles?|"
    r"family|relatives|descendants|namesakes|events?|anniversar|funeral|death|"
    r"музей|дом|могил|захорон|памятник|стату|бюст|мемориал|улиц|места|усадьб|"
    r"школ|библиотек|книг|произвед|стих|рукопис|письм|автограф|преми|награ|"
    r"марок|монет|корабл|теплоход|семь|родствен|юбиле|похорон|смерт",
    re.IGNORECASE,
)
BAD_OBJECT = re.compile(
    r"museum|house|grave|burial|tomb|plaque|monument|statue|bust|estate|street|"
    r"school|library|book|cover|works|autograph|signature|memorial|collection|"
    r"stamp|coin|banknote|quote|family|group|cemetery|river|reservoir|port\b|"
    r"ship\b|cruise|boat\b|vessel|letter|manuscript|literary prize|award|"
    r"concert hall|envelope|garden|villa|room|apartment|exhibition|poster|"
    r"graffiti|mural|performance|information|wall\b|funeral|coffin|deathbed|"
    r"дом-музей|музей|дом\b|могил|захорон|таблич|памятник|стату|бюст|усадьб|"
    r"улиц|школ|библиотек|книг|облож|собрани|автограф|подпис|мемориал|"
    r"кладбищ|цитат|семь|групп|барельеф|порт\b|теплоход|корабл|судно|речн|"
    r"письм|рукопис|преми|награ|концертн|конверт|сад\b|комнат|квартир|"
    r"выстав|плакат|граффити|исполнени|информац|похорон|гроб|смертн",
    re.IGNORECASE,
)
EXT_FIELDS = "|".join([
    "LicenseShortName", "UsageTerms", "AttributionRequired", "Artist", "Credit",
    "Source", "DateTimeOriginal", "DateTime", "ImageDescription", "Categories",
])


@dataclass
class Candidate:
    person: str
    source_category: str
    source_mode: str
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
                response.close(); time.sleep(attempt * 3); continue
            return response
        except requests.RequestException as exc:
            last = exc
            if attempt < 4:
                time.sleep(attempt * 3); continue
    raise RuntimeError(f"request failed: {last}")


def category_members(session: requests.Session, category: str, namespace: int, limit: int) -> list[str]:
    output: list[str] = []
    continuation: dict[str, Any] = {}
    while len(output) < limit:
        params = {
            "action": "query", "format": "json", "formatversion": 2,
            "list": "categorymembers", "cmtitle": f"Category:{category}",
            "cmnamespace": namespace, "cmlimit": min(500, limit - len(output)),
            **continuation,
        }
        response = get(session, API, params=params); response.raise_for_status()
        payload = response.json()
        output.extend(str(row["title"]) for row in payload.get("query", {}).get("categorymembers", []) if row.get("title"))
        if "continue" not in payload: break
        continuation = payload["continue"]
    return output[:limit]


def portrait_categories(session: requests.Session, root: str, depth: int, limit_per_category: int) -> list[str]:
    accepted: list[str] = []
    seen: set[str] = {root}
    queue: deque[tuple[str, int]] = deque([(root, 0)])
    while queue:
        current, level = queue.popleft()
        if level >= depth: continue
        for raw in category_members(session, current, 14, limit_per_category):
            name = raw.removeprefix("Category:")
            if name in seen: continue
            seen.add(name)
            if BAD_CATEGORY.search(name):
                continue
            if GOOD_CATEGORY.search(name):
                accepted.append(name)
            queue.append((name, level + 1))
    return accepted


def search_exact_titles(session: requests.Session, names: tuple[str, ...], limit: int) -> list[str]:
    titles: list[str] = []
    seen: set[str] = set()
    for name in names:
        params = {
            "action": "query", "format": "json", "formatversion": 2,
            "list": "search", "srsearch": f'intitle:"{name}" filetype:bitmap',
            "srnamespace": 6, "srlimit": min(50, limit), "srprop": "size|timestamp",
        }
        response = get(session, API, params=params); response.raise_for_status()
        for row in response.json().get("query", {}).get("search", []):
            title = str(row.get("title", ""))
            if title and title not in seen:
                seen.add(title); titles.append(title)
    return titles


def exact_name_in_title(title: str, names: tuple[str, ...]) -> bool:
    normalized = re.sub(r"[_-]+", " ", title.removeprefix("File:"), flags=re.I)
    return any(re.search(rf"(?<!\w){re.escape(name)}(?!\w)", normalized, re.I) for name in names)


def hydrate(session: requests.Session, person: str, names: tuple[str, ...], source_category: str, source_mode: str, titles: list[str]) -> list[Candidate]:
    output: list[Candidate] = []
    for start in range(0, len(titles), 10):
        params = {
            "action": "query", "format": "json", "formatversion": 2,
            "titles": "|".join(titles[start:start+10]), "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 512,
            "iiextmetadatafilter": EXT_FIELDS, "iiextmetadatalanguage": "en",
            "iimetadataversion": "latest",
        }
        response = get(session, API, params=params); response.raise_for_status()
        for page in response.json().get("query", {}).get("pages", []):
            infos = page.get("imageinfo") or []
            if not infos: continue
            info = infos[0]; ext = info.get("extmetadata") or {}
            title = str(page.get("title", "")); mime = str(info.get("mime", "")).lower()
            description = meta(ext, "ImageDescription"); categories = meta(ext, "Categories")
            combined = f"{title} {description} {categories}"
            short = meta(ext, "LicenseShortName"); terms = meta(ext, "UsageTerms")
            status, notes = "CANDIDATE", ""
            if mime not in ALLOWED_MIME: status, notes = "REJECTED_FORMAT", mime
            elif not license_allowed(short, terms): status, notes = "REJECTED_LICENSE", f"{short}/{terms}"
            elif BAD_OBJECT.search(combined): status, notes = "REJECTED_OBJECT_TYPE", "non-portrait object marker"
            elif source_mode == "exact-title" and not exact_name_in_title(title, names):
                status, notes = "REJECTED_EXACT_NAME", "exact person name absent from file title"
            output.append(Candidate(
                person, source_category, source_mode, int(page.get("pageid", 0)), title,
                str(info.get("descriptionurl", "")), str(info.get("url", "")), str(info.get("thumburl", "")), mime,
                int(info["width"]) if info.get("width") is not None else None,
                int(info["height"]) if info.get("height") is not None else None,
                int(info["size"]) if info.get("size") is not None else None,
                short, terms, meta(ext, "AttributionRequired"), meta(ext, "Artist"), meta(ext, "Credit"), meta(ext, "Source"),
                meta(ext, "DateTimeOriginal") or meta(ext, "DateTime"), description, categories,
                None, None, status, notes,
            ))
    return output


def safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._") or "portrait"


def download_review(session: requests.Session, candidates: list[Candidate], folder: Path, per_person: int) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}; seen_url: set[str] = set(); seen_sha: set[str] = set()
    # Prefer true portrait-oriented categories before exact-title fallback.
    candidates.sort(key=lambda c: (c.person, 0 if c.source_mode == "portrait-category" else 1, c.file_title))
    for c in candidates:
        if c.status != "CANDIDATE": continue
        if counts.get(c.person, 0) >= per_person:
            c.status = "REJECTED_PERSON_CAP"; c.notes = f"cap={per_person}"; continue
        if c.original_url in seen_url:
            c.status = "REJECTED_DUPLICATE_URL"; continue
        seen_url.add(c.original_url)
        try:
            response = get(session, c.thumb_url, stream=True); response.raise_for_status()
            payload = response.content; response.close()
            digest = hashlib.sha256(payload).hexdigest()
            if digest in seen_sha:
                c.status = "REJECTED_DUPLICATE_SHA"; continue
            seen_sha.add(digest)
            ext = ".png" if c.mime == "image/png" else ".jpg"
            idx = counts.get(c.person, 0) + 1
            filename = f"{safe(c.person)}__{idx:02d}{ext}"
            path = folder / filename; path.write_bytes(payload)
            with Image.open(path) as image:
                image.verify()
            c.review_file = filename; c.review_sha256 = digest; c.status = "REVIEW_READY"
            counts[c.person] = idx
        except Exception as exc:
            c.status = "REJECTED_THUMBNAIL"; c.notes = f"{type(exc).__name__}: {exc}"


def contact_sheets(candidates: list[Candidate], thumb_dir: Path, output_dir: Path, people_per_sheet: int = 4) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    people = [p for p, _, _ in PEOPLE]; tile_w, tile_h, cols = 300, 370, 4
    font = ImageFont.load_default(); sheets: list[str] = []
    for batch_start in range(0, len(people), people_per_sheet):
        batch = people[batch_start:batch_start+people_per_sheet]
        rows = sum(max(1, (len([c for c in candidates if c.person == p and c.status == "REVIEW_READY"])+cols-1)//cols) for p in batch)
        canvas = Image.new("RGB", (cols*tile_w, max(1, rows)*tile_h), "white"); draw = ImageDraw.Draw(canvas); row = 0
        for person in batch:
            items = [c for c in candidates if c.person == person and c.status == "REVIEW_READY"]
            person_rows = max(1, (len(items)+cols-1)//cols)
            for idx, c in enumerate(items):
                col, local = idx%cols, idx//cols; x, y = col*tile_w, (row+local)*tile_h
                with Image.open(thumb_dir/str(c.review_file)).convert("RGB") as image:
                    fitted = ImageOps.contain(image, (tile_w-16, tile_h-90)); canvas.paste(fitted, (x+(tile_w-fitted.width)//2, y+8))
                label = f"{person} #{idx+1}\n{c.source_mode}\n{c.file_title.removeprefix('File:')[:44]}"
                draw.multiline_text((x+8, y+tile_h-78), label, fill="black", font=font, spacing=2)
            row += person_rows
        filename = f"portrait-review-v2-sheet-{batch_start//people_per_sheet+1:02d}.jpg"
        canvas.save(output_dir/filename, quality=90, optimize=True); sheets.append(filename)
    return sheets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--category-limit", type=int, default=250)
    parser.add_argument("--exact-search-limit", type=int, default=50)
    parser.add_argument("--per-person", type=int, default=10)
    parser.add_argument("--minimum-ready", type=int, default=70)
    parser.add_argument("--minimum-core", type=int, default=3)
    parser.add_argument("--output", default="portrait-review-v2-output")
    args = parser.parse_args()

    output = Path(args.output); thumb = output/"thumbnails"; sheets_dir = output/"contact-sheets"
    session = requests.Session(); session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json,text/html,*/*"})
    candidates: list[Candidate] = []; global_seen_titles: set[str] = set()

    for person, root_category, aliases in PEOPLE:
        names = (person, *aliases)
        categories = portrait_categories(session, root_category, args.depth, 300)
        print(f"[person] {person} portrait-subcategories={categories}", flush=True)
        for category in categories:
            titles = category_members(session, category, 6, args.category_limit)
            unique = [t for t in titles if t not in global_seen_titles]
            global_seen_titles.update(unique)
            candidates.extend(hydrate(session, person, names, category, "portrait-category", unique))
        exact = [t for t in search_exact_titles(session, names, args.exact_search_limit) if t not in global_seen_titles]
        global_seen_titles.update(exact)
        candidates.extend(hydrate(session, person, names, root_category, "exact-title", exact))

    download_review(session, candidates, thumb, args.per_person)
    sheets = contact_sheets(candidates, thumb, sheets_dir)
    ready = [c for c in candidates if c.status == "REVIEW_READY"]
    by_person = {p: sum(c.person == p and c.status == "REVIEW_READY" for c in candidates) for p, _, _ in PEOPLE}
    report = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "review_ready": len(ready), "review_ready_by_person": by_person,
        "status_counts": {s: sum(c.status == s for c in candidates) for s in sorted({c.status for c in candidates})},
        "contact_sheets": sheets, "records": [asdict(c) for c in candidates],
    }
    output.mkdir(parents=True, exist_ok=True)
    (output/"portrait-v2-candidates.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(Candidate.__dataclass_fields__)
    with (output/"portrait-v2-candidates.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); [writer.writerow(asdict(c)) for c in candidates]
    (output/"README.md").write_text(
        f"# Strict recursive-category portrait review v2\n\nReview-ready: **{len(ready)}**. Identity is not approved automatically; contact sheets require human review.\n",
        encoding="utf-8",
    )
    core = {"Sergei Yesenin", "Ivan Bunin", "Igor Severyanin", "Konstantin Balmont", "Fyodor Tyutchev", "Apollon Maykov", "Valery Bryusov", "Alexander Blok", "Afanasy Fet"}
    core_fail = {p: by_person[p] for p in core if by_person[p] < args.minimum_core}
    print(json.dumps({"review_ready": len(ready), "by_person": by_person, "core_fail": core_fail, "sheets": sheets}, ensure_ascii=False))
    return 0 if len(ready) >= args.minimum_ready and not core_fail else 2


if __name__ == "__main__":
    raise SystemExit(main())
