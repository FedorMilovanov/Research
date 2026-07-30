#!/usr/bin/env python3
"""Build open-license review sheets for manuscripts, covers, places and history.

This is a candidate-review pass. It downloads 512px previews only, enforces small
per-topic caps, preserves item-level provenance, and builds contact sheets. Final
originals require a separate reviewed allowlist.
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
    "TheLegendaryPoet-EphemeraReview/1.0 "
    "(+https://github.com/FedorMilovanov/Research; contact: viktorcoy2012@gmail.com)"
)

OPEN_LICENSE_PATTERNS = (
    "public domain", "pd-", "cc0", "cc by ", "cc-by-", "cc by-sa", "cc-by-sa",
    "creative commons attribution",
)
EXCLUDED_LICENSE_PATTERNS = (
    "fair use", "copyrighted", "noncommercial", "no derivatives", "all rights reserved",
)
ALLOWED_MIME = {"image/jpeg", "image/png", "image/tiff", "image/webp"}
EXT_FIELDS = "|".join([
    "LicenseShortName", "UsageTerms", "AttributionRequired", "Artist", "Credit",
    "Source", "DateTimeOriginal", "DateTime", "ImageDescription", "Categories",
])


@dataclass(frozen=True)
class Topic:
    name: str
    queries: tuple[str, ...]
    include: str
    exclude: str = ""
    cap: int = 5


@dataclass
class Candidate:
    topic: str
    query: str
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


TOPICS: tuple[Topic, ...] = (
    Topic("manuscript-pushkin", ('"Alexander Pushkin" manuscript filetype:bitmap', '"Александр Пушкин" рукопись filetype:bitmap', '"Пушкин" автограф filetype:bitmap'), r"(?=.*(?:pushkin|пушкин))(?=.*(?:manuscript|рукопис|autograph|автограф|чернов))", cap=5),
    Topic("manuscript-lermontov", ('"Mikhail Lermontov" manuscript filetype:bitmap', '"Лермонтов" рукопись filetype:bitmap', '"Лермонтов" автограф filetype:bitmap'), r"(?=.*(?:lermontov|лермонтов))(?=.*(?:manuscript|рукопис|autograph|автограф|чернов))", cap=5),
    Topic("manuscript-yesenin", ('"Sergei Yesenin" manuscript filetype:bitmap', '"Есенин" рукопись filetype:bitmap', '"Есенин" автограф filetype:bitmap'), r"(?=.*(?:yesenin|esenin|есенин))(?=.*(?:manuscript|рукопис|autograph|автограф|стихотворен))", cap=5),
    Topic("manuscript-mayakovsky", ('"Vladimir Mayakovsky" manuscript filetype:bitmap', '"Маяковский" рукопись filetype:bitmap', '"Маяковский" автограф filetype:bitmap'), r"(?=.*(?:mayakov|маяков))(?=.*(?:manuscript|рукопис|autograph|автограф|чернов))", cap=5),
    Topic("manuscript-blok", ('"Alexander Blok" manuscript filetype:bitmap', '"Александр Блок" рукопись filetype:bitmap', '"Блок" автограф filetype:bitmap'), r"(?=.*(?:alexander blok|александр блок))(?=.*(?:manuscript|рукопис|autograph|автограф|чернов))", cap=5),
    Topic("manuscript-akhmatova", ('"Anna Akhmatova" manuscript filetype:bitmap', '"Ахматова" рукопись filetype:bitmap', '"Ахматова" автограф filetype:bitmap'), r"(?=.*(?:akhmatova|ахматова))(?=.*(?:manuscript|рукопис|autograph|автограф|чернов))", cap=5),
    Topic("manuscript-tsvetaeva", ('"Marina Tsvetaeva" manuscript filetype:bitmap', '"Цветаева" рукопись filetype:bitmap', '"Цветаева" автограф filetype:bitmap'), r"(?=.*(?:tsvetaeva|цветаева))(?=.*(?:manuscript|рукопис|autograph|автограф|чернов))", cap=5),
    Topic("manuscript-pasternak", ('"Boris Pasternak" manuscript filetype:bitmap', '"Пастернак" рукопись filetype:bitmap', '"Пастернак" автограф filetype:bitmap'), r"(?=.*(?:pasternak|пастернак))(?=.*(?:manuscript|рукопис|autograph|автограф|чернов|letter|письм))", cap=5),

    Topic("cover-russian-futurism", ('Russian futurist book cover filetype:bitmap', 'русский футуризм обложка filetype:bitmap'), r"(?=.*(?:futur|футур))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|exhibition|выстав", 6),
    Topic("cover-kruchenykh", ('Kruchenykh book cover filetype:bitmap', 'Крученых обложка filetype:bitmap'), r"(?=.*(?:kruchenykh|крученых))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|reconstruction|реконструк", 5),
    Topic("cover-khlebnikov", ('Khlebnikov book cover filetype:bitmap', 'Хлебников обложка filetype:bitmap'), r"(?=.*(?:khlebnikov|хлебников))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|exhibition", 5),
    Topic("cover-mayakovsky", ('Mayakovsky book cover filetype:bitmap', 'Маяковский обложка filetype:bitmap'), r"(?=.*(?:mayakov|маяков))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|exhibition", 5),
    Topic("cover-silver-age-journals", ('Мир искусства обложка filetype:bitmap', 'Аполлон журнал обложка filetype:bitmap', 'Весы журнал обложка filetype:bitmap', 'Золотое руно обложка filetype:bitmap'), r"(?=.*(?:мир искусства|аполлон|весы|золотое руно))(?=.*(?:облож|cover|журнал))", r"20(?:1|2)\d|exhibition", 6),

    Topic("place-yesenin", ('"Sergei Yesenin" house museum filetype:bitmap', '"Есенин" дом-музей filetype:bitmap'), r"(?=.*(?:yesenin|esenin|есенин))(?=.*(?:museum|музей|house|дом|estate|усадьб))", r"plaque|таблич|sign|grave|могил|monument|памятник|information", 3),
    Topic("place-blok", ('"Alexander Blok" house museum filetype:bitmap', '"Александр Блок" дом-музей filetype:bitmap'), r"(?=.*(?:alexander blok|александр блок))(?=.*(?:museum|музей|house|дом|apartment|квартир))", r"plaque|таблич|sign|grave|могил|monument|памятник|information", 3),
    Topic("place-mayakovsky", ('"Vladimir Mayakovsky" house museum filetype:bitmap', '"Маяковский" музей filetype:bitmap'), r"(?=.*(?:mayakov|маяков))(?=.*(?:museum|музей|house|дом|apartment|квартир))", r"plaque|таблич|sign|grave|могил|monument|памятник|information", 3),
    Topic("place-pasternak", ('"Boris Pasternak" house museum filetype:bitmap', '"Пастернак" дом-музей filetype:bitmap'), r"(?=.*(?:pasternak|пастернак))(?=.*(?:museum|музей|house|дом|dacha|дач))", r"guide|экскурсовод|plaque|таблич|sign|grave|могил|information", 3),
    Topic("place-pushkin", ('"Alexander Pushkin" house museum filetype:bitmap', '"Пушкин" дом-музей filetype:bitmap'), r"(?=.*(?:pushkin|пушкин))(?=.*(?:museum|музей|house|дом|estate|усадьб))", r"plaque|таблич|sign|grave|могил|monument|памятник|information", 3),
    Topic("place-lermontov", ('"Mikhail Lermontov" house museum filetype:bitmap', '"Лермонтов" дом-музей filetype:bitmap'), r"(?=.*(?:lermontov|лермонтов))(?=.*(?:museum|музей|house|дом|estate|усадьб))", r"plaque|таблич|sign|grave|могил|monument|памятник|information", 3),
    Topic("place-akhmatova", ('"Anna Akhmatova" house museum filetype:bitmap', '"Ахматова" музей filetype:bitmap'), r"(?=.*(?:akhmatova|ахматова))(?=.*(?:museum|музей|house|дом|apartment|квартир))", r"information|таблич|sign|grave|могил|monument|памятник", 3),
    Topic("place-tsvetaeva", ('"Marina Tsvetaeva" house museum filetype:bitmap', '"Цветаева" дом-музей filetype:bitmap'), r"(?=.*(?:tsvetaeva|цветаева))(?=.*(?:museum|музей|house|дом|estate|усадьб))", r"information|таблич|sign|grave|могил|monument|памятник", 3),

    Topic("manuscript-codex-sinaiticus", ('Codex Sinaiticus filetype:bitmap',), r"codex sinaiticus", r"book cover|museum display|modern replica|tourist|stone|relique", 4),
    Topic("manuscript-dead-sea-scrolls", ('Dead Sea Scroll manuscript filetype:bitmap', 'Qumran scroll fragment filetype:bitmap'), r"(?=.*(?:dead sea scroll|qumran))(?=.*(?:manuscript|scroll|fragment|plate|papyrus|parchment))", r"stone|relique|museum display|replica|book cover|tourist|jar\b|cave\b", 4),
    Topic("manuscript-bodmer-p72", ('Papyrus Bodmer manuscript filetype:bitmap', 'P72 manuscript filetype:bitmap', 'Papyrus Bodmer VIII filetype:bitmap'), r"papyrus bodmer|(?:^|\W)p72(?:\W|$)", r"book cover|museum display|modern replica|bodmer vi\b|bodmer xxiv", 4),
    Topic("manuscript-hebrew-bible", ('Hebrew Bible manuscript filetype:bitmap', 'Masoretic codex manuscript filetype:bitmap', 'Aleppo Codex filetype:bitmap', 'Leningrad Codex filetype:bitmap'), r"hebrew bible manuscript|masoretic codex|aleppo codex|leningrad codex", r"book cover|modern replica|museum display", 5),

    Topic("reformation-calvin", ('John Calvin portrait filetype:bitmap',), r"john calvin", r"sir john|reverse|flipped|mirror|statue|monument|modern|plaque", 3),
    Topic("reformation-luther", ('Martin Luther portrait filetype:bitmap',), r"martin luther", r"statue|monument|modern|plaque|king jr", 3),
    Topic("puritan-john-owen", ('"John Owen" puritan portrait filetype:bitmap', '"John Owen" theologian portrait filetype:bitmap'), r"john owen", r"sir john|admiral|judge|politician|welsh politician|statue|modern", 3),
    Topic("puritan-thomas-goodwin", ('"Thomas Goodwin" puritan portrait filetype:bitmap', '"Thomas Goodwin" theologian portrait filetype:bitmap'), r"thomas goodwin", r"actor|politician|architect|modern|statue", 3),
    Topic("westminster-assembly", ('Westminster Assembly engraving filetype:bitmap', 'Westminster divines engraving filetype:bitmap'), r"westminster assembly|westminster divines", r"modern|book cover|abbey", 4),
)

GENERAL_BAD = re.compile(
    r"football|airport|aircraft|ship\b|album cover|logo\b|currency|coin\b|"
    r"medical|chemistry|botany|zoology|modern advertisement|school yearbook",
    re.IGNORECASE,
)


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
    return not any(x in text for x in EXCLUDED_LICENSE_PATTERNS) and any(x in text for x in OPEN_LICENSE_PATTERNS)


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


def search_titles(session: requests.Session, query: str, limit: int) -> list[str]:
    rows: list[str] = []
    continuation: dict[str, Any] = {}
    while len(rows) < limit:
        params = {
            "action": "query", "format": "json", "formatversion": 2,
            "list": "search", "srsearch": query, "srnamespace": 6,
            "srlimit": min(50, limit - len(rows)), "srprop": "size|timestamp", **continuation,
        }
        response = get(session, API, params=params); response.raise_for_status()
        payload = response.json()
        rows.extend(str(r["title"]) for r in payload.get("query", {}).get("search", []) if r.get("title"))
        if "continue" not in payload: break
        continuation = payload["continue"]
    return rows[:limit]


def hydrate(session: requests.Session, topic: Topic, query: str, titles: list[str]) -> list[Candidate]:
    output: list[Candidate] = []
    for start in range(0, len(titles), 10):
        params = {
            "action": "query", "format": "json", "formatversion": 2,
            "titles": "|".join(titles[start:start + 10]), "prop": "imageinfo",
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
            elif GENERAL_BAD.search(combined): status, notes = "REJECTED_GENERAL", "general unrelated marker"
            elif not re.search(topic.include, combined, re.I): status, notes = "REJECTED_INCLUDE", "topic include missing"
            elif topic.exclude and re.search(topic.exclude, combined, re.I): status, notes = "REJECTED_EXCLUDE", "topic exclusion marker"
            output.append(Candidate(
                topic.name, query, int(page.get("pageid", 0)), title,
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
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._") or "item"


def download_review(session: requests.Session, candidates: list[Candidate], folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    seen_url: set[str] = set(); seen_sha: set[str] = set()
    for c in candidates:
        if c.status != "CANDIDATE": continue
        topic = next(t for t in TOPICS if t.name == c.topic)
        if counts.get(c.topic, 0) >= topic.cap:
            c.status = "REJECTED_TOPIC_CAP"; c.notes = f"cap={topic.cap}"; continue
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
            idx = counts.get(c.topic, 0) + 1
            filename = f"{safe(c.topic)}__{idx:02d}{ext}"
            path = folder / filename; path.write_bytes(payload)
            with Image.open(path) as image: image.verify()
            c.review_file = filename; c.review_sha256 = digest; c.status = "REVIEW_READY"
            counts[c.topic] = idx
        except Exception as exc:
            c.status = "REJECTED_THUMBNAIL"; c.notes = f"{type(exc).__name__}: {exc}"


def contact_sheets(candidates: list[Candidate], thumb_dir: Path, output_dir: Path, topics_per_sheet: int = 6) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h, cols = 280, 350, 4
    font = ImageFont.load_default(); sheets: list[str] = []
    topic_names = [t.name for t in TOPICS]
    for batch_start in range(0, len(topic_names), topics_per_sheet):
        batch = topic_names[batch_start:batch_start + topics_per_sheet]
        rows = sum(max(1, (len([c for c in candidates if c.topic == t and c.status == "REVIEW_READY"]) + cols - 1) // cols) for t in batch)
        canvas = Image.new("RGB", (cols * tile_w, max(1, rows) * tile_h), "white"); draw = ImageDraw.Draw(canvas)
        row = 0
        for topic in batch:
            items = [c for c in candidates if c.topic == topic and c.status == "REVIEW_READY"]
            topic_rows = max(1, (len(items) + cols - 1) // cols)
            for idx, c in enumerate(items):
                col, local_row = idx % cols, idx // cols; x, y = col * tile_w, (row + local_row) * tile_h
                with Image.open(thumb_dir / str(c.review_file)).convert("RGB") as image:
                    fitted = ImageOps.contain(image, (tile_w - 16, tile_h - 76)); canvas.paste(fitted, (x + (tile_w - fitted.width)//2, y + 8))
                label = f"{topic} #{idx+1}\n{c.file_title.removeprefix('File:')[:48]}"
                draw.multiline_text((x+8, y+tile_h-62), label, fill="black", font=font, spacing=2)
            row += topic_rows
        filename = f"ephemera-review-sheet-{batch_start // topics_per_sheet + 1:02d}.jpg"
        canvas.save(output_dir / filename, quality=88, optimize=True); sheets.append(filename)
    return sheets


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--per-query", type=int, default=60); parser.add_argument("--minimum-ready", type=int, default=65); parser.add_argument("--output", default="ephemera-review-output")
    args = parser.parse_args(); output = Path(args.output); thumb = output/"thumbnails"; sheets_dir = output/"contact-sheets"
    session = requests.Session(); session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json,text/html,*/*"})
    candidates: list[Candidate] = []; seen_title: set[str] = set()
    for topic in TOPICS:
        accepted_before = len(candidates)
        for query in topic.queries:
            titles = [t for t in search_titles(session, query, args.per_query) if t not in seen_title]
            seen_title.update(titles); candidates.extend(hydrate(session, topic, query, titles))
        print(f"[topic] {topic.name} records={len(candidates)-accepted_before}", flush=True)
    download_review(session, candidates, thumb); sheets = contact_sheets(candidates, thumb, sheets_dir)
    ready = [c for c in candidates if c.status == "REVIEW_READY"]
    report = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "review_ready": len(ready),
        "review_ready_by_topic": {t.name: sum(c.topic == t.name and c.status == "REVIEW_READY" for c in candidates) for t in TOPICS},
        "status_counts": {s: sum(c.status == s for c in candidates) for s in sorted({c.status for c in candidates})},
        "contact_sheets": sheets,
        "records": [asdict(c) for c in candidates],
    }
    output.mkdir(parents=True, exist_ok=True); (output/"ephemera-candidates.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(Candidate.__dataclass_fields__)
    with (output/"ephemera-candidates.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); [writer.writerow(asdict(c)) for c in candidates]
    (output/"README.md").write_text(f"# Ephemera review candidates\n\nReview-ready previews: **{len(ready)}**. These are not production-approved originals.\n", encoding="utf-8")
    print(json.dumps({"review_ready": len(ready), "minimum_ready": args.minimum_ready, "contact_sheets": sheets}))
    return 0 if len(ready) >= args.minimum_ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
