#!/usr/bin/env python3
"""Collect 120+ openly licensed project materials from Wikimedia Commons.

Three independent 40+ gates are enforced:

1. Additional research PDFs (periodicals, memoirs, criticism, theology/history).
2. Portrait/reference images for The Legendary Poet.
3. Ephemera and mixed media (manuscripts, letters, posters, covers, places,
   sheet music, audio and video).

Only structured Public Domain, CC0, CC BY, or CC BY-SA records are accepted.
Every downloaded original is preserved unchanged and receives provenance,
license metadata, SHA-256, byte size and format-specific validation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import mimetypes
import re
import shutil
import subprocess
import time
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests
from PIL import Image
from pypdf import PdfReader

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "TheLegendaryPoet-OpenProjectMaterials/1.0 "
    "(+https://github.com/FedorMilovanov/Research; contact: viktorcoy2012@gmail.com)"
)
COLLECTION = "commons-project-materials-120plus"

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

EXT_FIELDS = "|".join(
    [
        "LicenseShortName",
        "UsageTerms",
        "AttributionRequired",
        "Artist",
        "Credit",
        "Source",
        "DateTimeOriginal",
        "DateTime",
        "ImageDescription",
        "Categories",
    ]
)

ALLOWED_BY_BUCKET = {
    "pdf": {"application/pdf"},
    "portrait": {
        "image/jpeg",
        "image/png",
        "image/tiff",
        "image/webp",
    },
    "ephemera": {
        "image/jpeg",
        "image/png",
        "image/tiff",
        "image/webp",
        "image/svg+xml",
        "audio/ogg",
        "audio/mpeg",
        "audio/wav",
        "audio/flac",
        "video/webm",
        "video/ogg",
        "application/ogg",
        "image/vnd.djvu",
    },
}

EXTENSION_BY_MIME = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/tiff": ".tif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "audio/ogg": ".ogg",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/flac": ".flac",
    "video/webm": ".webm",
    "video/ogg": ".ogv",
    "application/ogg": ".ogg",
    "image/vnd.djvu": ".djvu",
}


@dataclass(frozen=True)
class Topic:
    bucket: str
    name: str
    queries: tuple[str, ...]
    include: str
    exclude: str = ""
    cap: int = 8


@dataclass
class Candidate:
    bucket: str
    topic: str
    query: str
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
    description: str
    categories: str


@dataclass
class Record:
    bucket: str
    topic: str
    archive_number: int | None
    file_title: str
    local_file_name: str | None
    description_url: str
    original_url: str
    discovery_query: str
    mime: str
    license_short_name: str
    usage_terms: str
    attribution_required: str
    artist: str
    credit: str
    source: str
    date: str
    advertised_bytes: int | None
    downloaded_bytes: int | None
    sha256: str | None
    width: int | None
    height: int | None
    pages: int | None
    duration_seconds: float | None
    status: str
    http_status: int | None
    content_type: str | None
    checked_at_utc: str
    notes: str


TOPICS: tuple[Topic, ...] = (
    Topic("pdf", "russian-periodicals", (
        'intitle:"Русский архив" filemime:pdf',
        'intitle:"Исторический вестник" filemime:pdf',
        'intitle:"Вестник Европы" filemime:pdf',
        'intitle:"Русская мысль" filemime:pdf',
        'intitle:"Русское богатство" filemime:pdf',
        'intitle:"Нива" filemime:pdf',
    ), r"русский архив|исторический вестник|вестник европы|русская мысль|русское богатство|(?:^|\W)нива(?:\W|$)", cap=18),
    Topic("pdf", "silver-age-periodicals", (
        'intitle:"Мир искусства" filemime:pdf',
        'intitle:"Золотое руно" filemime:pdf',
        'intitle:"Аполлон" filemime:pdf',
        'intitle:"Весы" filemime:pdf',
        'intitle:"Перевал" журнал filemime:pdf',
        'intitle:"Северные цветы" filemime:pdf',
    ), r"мир искусства|золотое руно|аполлон|(?:^|\W)весы(?:\W|$)|перевал|северные цветы", cap=16),
    Topic("pdf", "memoirs-letters", (
        'Russian literary memoirs filemime:pdf',
        'русские писатели воспоминания filemime:pdf',
        'intitle:"Письма русских писателей" filemime:pdf',
        'intitle:"Литературные воспоминания" filemime:pdf',
        'intitle:"Переписка" русская литература filemime:pdf',
    ), r"memoir|воспоминан|письм|переписк|литературн", cap=14),
    Topic("pdf", "avant-garde-imagism", (
        'Russian futurism filemime:pdf',
        'Русский футуризм filemime:pdf',
        'Russian avant-garde literature filemime:pdf',
        'Имажинизм filemime:pdf',
        'Imagism Russian poetry filemime:pdf',
    ), r"futuris|футур|avant.?garde|авангард|имажиниз|imagis", cap=12),
    Topic("pdf", "protestant-history", (
        'Russian Baptists history filemime:pdf',
        'русские баптисты filemime:pdf',
        'Protestantism Russia history filemime:pdf',
        'евангельские христиане Россия filemime:pdf',
        'intitle:"Westminster Confession" filemime:pdf',
    ), r"baptist|баптист|protestant|протестант|евангельск|westminster", cap=14),
    Topic("pdf", "puritan-reformed", (
        'John Owen theology filemime:pdf',
        'Thomas Goodwin theology filemime:pdf',
        'John Calvin Institutes filemime:pdf',
        'Puritan theology filemime:pdf',
        'Reformed theology history filemime:pdf',
    ), r"john owen|thomas goodwin|calvin|puritan|reformed|theolog", cap=14),
    Topic("pdf", "biblical-manuscripts", (
        'Codex Sinaiticus filemime:pdf',
        'First Peter commentary filemime:pdf',
        'Book of Enoch study filemime:pdf',
        'Dead Sea Scrolls filemime:pdf',
        'Qumran manuscripts filemime:pdf',
    ), r"sinaitic|first peter|1 peter|enoch|dead sea scroll|qumran|рукопис", cap=12),

    Topic("portrait", "esenin", ('"Sergei Yesenin" filetype:bitmap', '"Сергей Есенин" filetype:bitmap'), r"serge[yi].*yesenin|sergey.*esenin|сергей.*есенин", cap=8),
    Topic("portrait", "bunin", ('"Ivan Bunin" filetype:bitmap', '"Иван Бунин" filetype:bitmap'), r"ivan.*bunin|иван.*бунин", cap=8),
    Topic("portrait", "severyanin", ('"Igor Severyanin" filetype:bitmap', '"Игорь Северянин" filetype:bitmap'), r"igor.*severyanin|игорь.*северянин", cap=8),
    Topic("portrait", "balmont", ('"Konstantin Balmont" filetype:bitmap', '"Константин Бальмонт" filetype:bitmap'), r"konstantin.*balmont|константин.*бальмонт", cap=8),
    Topic("portrait", "tyutchev", ('"Fyodor Tyutchev" filetype:bitmap', '"Фёдор Тютчев" filetype:bitmap'), r"fyodor.*tyutchev|ф[её]дор.*тютчев", cap=8),
    Topic("portrait", "maykov", ('"Apollon Maykov" filetype:bitmap', '"Аполлон Майков" filetype:bitmap'), r"apollon.*maykov|аполлон.*майков", cap=8),
    Topic("portrait", "bryusov", ('"Valery Bryusov" filetype:bitmap', '"Валерий Брюсов" filetype:bitmap'), r"valer.*bryusov|валер.*брюсов", cap=8),
    Topic("portrait", "blok", ('"Alexander Blok" filetype:bitmap', '"Александр Блок" filetype:bitmap'), r"alexander.*blok|александр.*блок", cap=8),
    Topic("portrait", "fet", ('"Afanasy Fet" filetype:bitmap', '"Афанасий Фет" filetype:bitmap'), r"afanasy.*fet|афанасий.*фет|шеншин", cap=8),
    Topic("portrait", "mayakovsky", ('"Vladimir Mayakovsky" filetype:bitmap', '"Владимир Маяковский" filetype:bitmap'), r"vladimir.*maya?kov|владимир.*маяков", cap=8),
    Topic("portrait", "akhmatova", ('"Anna Akhmatova" filetype:bitmap', '"Анна Ахматова" filetype:bitmap'), r"anna.*akhmatova|анна.*ахматова", cap=8),
    Topic("portrait", "gumilev", ('"Nikolay Gumilev" filetype:bitmap', '"Николай Гумилёв" filetype:bitmap'), r"nikolay.*gumilev|николай.*гумил", cap=8),
    Topic("portrait", "pasternak", ('"Boris Pasternak" filetype:bitmap', '"Борис Пастернак" filetype:bitmap'), r"boris.*pasternak|борис.*пастернак", cap=8),
    Topic("portrait", "pushkin-lermontov", (
        '"Alexander Pushkin" portrait filetype:bitmap',
        '"Mikhail Lermontov" portrait filetype:bitmap',
        '"Александр Пушкин" портрет filetype:bitmap',
        '"Михаил Лермонтов" портрет filetype:bitmap',
    ), r"pushkin|пушкин|lermontov|лермонтов", cap=10),

    Topic("ephemera", "manuscripts-letters", (
        'Russian poet manuscript filetype:bitmap',
        'рукопись поэта filetype:bitmap',
        'автограф писателя filetype:bitmap',
        'Russian writer letter filetype:bitmap',
        'письмо писателя filetype:bitmap',
    ), r"manuscript|рукопис|автограф|letter|письм", cap=14),
    Topic("ephemera", "posters-covers", (
        'Russian poetry poster filetype:bitmap',
        'Russian avant-garde poster filetype:bitmap',
        'русская поэзия афиша filetype:bitmap',
        'обложка поэтического сборника filetype:bitmap',
        'Russian book cover poetry filetype:bitmap',
    ), r"poster|афиш|обложк|cover|плакат|book", cap=14),
    Topic("ephemera", "literary-places", (
        'Sergei Yesenin museum filetype:bitmap',
        'Alexander Blok house filetype:bitmap',
        'Mayakovsky museum filetype:bitmap',
        'Pushkin house museum filetype:bitmap',
        'Russian literary museum filetype:bitmap',
    ), r"museum|музей|house|дом|estate|усадьб|memorial", cap=12),
    Topic("ephemera", "theology-manuscripts", (
        'Codex Sinaiticus filetype:bitmap',
        'Dead Sea Scrolls filetype:bitmap',
        'Qumran manuscript filetype:bitmap',
        'Greek New Testament manuscript filetype:bitmap',
        'Hebrew Bible manuscript filetype:bitmap',
    ), r"sinaitic|dead sea scroll|qumran|manuscript|рукопис|codex", cap=14),
    Topic("ephemera", "reformation-puritan", (
        'John Calvin portrait filetype:bitmap',
        'John Owen portrait filetype:bitmap',
        'Puritan portrait filetype:bitmap',
        'Reformation engraving filetype:bitmap',
        'Westminster Assembly filetype:bitmap',
    ), r"calvin|john owen|puritan|reformation|westminster", cap=12),
    Topic("ephemera", "audio-poetry-hymns", (
        'Russian poetry filetype:audio',
        'Russian poem filetype:audio',
        'poetry reading Russian filetype:audio',
        'Russian hymn filetype:audio',
        'Protestant hymn filetype:audio',
    ), r"poem|poetry|стих|поэз|hymn|гимн|reading|чтени", cap=12),
    Topic("ephemera", "historic-film", (
        'Russian writers filetype:video',
        'Russian poetry filetype:video',
        'Isadora Duncan dance filetype:video',
        'Russian literary history filetype:video',
    ), r"writer|poet|poetry|писател|поэт|duncan|литератур", cap=8),
)

GLOBAL_EXCLUDE = re.compile(
    r"football|soccer|baseball|basketball|hockey|airport|aircraft|ship\b|"
    r"album cover|modern advertisement|logo\b|coat of arms|currency|coin\b|"
    r"school yearbook|medical|chemistry|botany|zoology",
    re.IGNORECASE,
)


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


def license_allowed(short_name: str, usage_terms: str) -> bool:
    combined = f"{short_name} {usage_terms}".lower()
    if any(marker in combined for marker in EXCLUDED_LICENSE_PATTERNS):
        return False
    return any(marker in combined for marker in OPEN_LICENSE_PATTERNS)


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


def search_titles(session: requests.Session, query: str, limit: int) -> list[str]:
    rows: list[str] = []
    continuation: dict[str, Any] = {}
    while len(rows) < limit:
        params: dict[str, Any] = {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": min(50, limit - len(rows)),
            "srprop": "size|wordcount|timestamp",
            **continuation,
        }
        response = request(session, API, params=params)
        response.raise_for_status()
        payload = response.json()
        rows.extend(str(row.get("title", "")) for row in payload.get("query", {}).get("search", []) if row.get("title"))
        if "continue" not in payload:
            break
        continuation = payload["continue"]
    return rows[:limit]


def hydrate_batch(
    session: requests.Session,
    titles: list[str],
    topic: Topic,
    query: str,
) -> list[Candidate]:
    params: dict[str, Any] = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "titles": "|".join(titles),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiextmetadatafilter": EXT_FIELDS,
        "iiextmetadatalanguage": "en",
        "iimetadataversion": "latest",
    }
    response = request(session, API, params=params)
    response.raise_for_status()
    payload = response.json()
    output: list[Candidate] = []
    for page in payload.get("query", {}).get("pages", []):
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        title = str(page.get("title", ""))
        mime = str(info.get("mime", "")).lower()
        if mime not in ALLOWED_BY_BUCKET[topic.bucket]:
            continue
        if GLOBAL_EXCLUDE.search(title):
            continue
        if not re.search(topic.include, title, flags=re.IGNORECASE):
            continue
        if topic.exclude and re.search(topic.exclude, title, flags=re.IGNORECASE):
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

        output.append(
            Candidate(
                bucket=topic.bucket,
                topic=topic.name,
                query=query,
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
                description=metadata_value(ext, "ImageDescription"),
                categories=metadata_value(ext, "Categories"),
            )
        )
    return output


def semantic_key(title: str) -> str:
    value = title.removeprefix("File:")
    value = re.sub(r"\.(pdf|jpe?g|png|tiff?|webp|svg|ogg|oga|mp3|wav|flac|webm|ogv|djvu)$", "", value, flags=re.I)
    value = unicodedata.normalize("NFKD", value).lower()
    value = re.sub(r"\b(scan|scanned|copy|version|page|pages|vol|volume|том|выпуск|issue)\b", " ", value)
    value = re.sub(r"\b\d{3,4}\b", " ", value)
    value = re.sub(r"[^a-zа-яё0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def discover(session: requests.Session, per_query: int) -> tuple[dict[str, list[Candidate]], list[dict[str, str]]]:
    buckets: dict[str, list[Candidate]] = defaultdict(list)
    failures: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_semantic: dict[str, set[str]] = defaultdict(set)

    for topic in TOPICS:
        topic_count = 0
        for query in topic.queries:
            print(f"[query] bucket={topic.bucket} topic={topic.name} query={query}", flush=True)
            try:
                titles = search_titles(session, query, per_query)
                hydrated: list[Candidate] = []
                for start in range(0, len(titles), 10):
                    hydrated.extend(hydrate_batch(session, titles[start:start + 10], topic, query))
            except Exception as exc:
                failures.append({
                    "bucket": topic.bucket,
                    "topic": topic.name,
                    "query": query,
                    "error": f"{type(exc).__name__}: {exc}",
                })
                continue

            for candidate in hydrated:
                key = semantic_key(candidate.file_title)
                if candidate.original_url in seen_urls or not key or key in seen_semantic[topic.bucket]:
                    continue
                seen_urls.add(candidate.original_url)
                seen_semantic[topic.bucket].add(key)
                buckets[topic.bucket].append(candidate)
                topic_count += 1
                if topic_count >= topic.cap:
                    break
            if topic_count >= topic.cap:
                break
        print(f"[topic-result] bucket={topic.bucket} topic={topic.name} accepted={topic_count}", flush=True)

    return buckets, failures


def slugify(value: str, mime: str, limit: int = 120) -> str:
    value = value.removeprefix("File:")
    value = re.sub(r"\.[A-Za-z0-9]{2,5}$", "", value)
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("—", "-").replace("–", "-")
    value = re.sub(r'[\\/:*?"<>|]+', "_", value)
    value = re.sub(r"\s+", " ", value).strip(" ._")
    ext = EXTENSION_BY_MIME.get(mime) or mimetypes.guess_extension(mime) or ".bin"
    return f"{(value[:limit].rstrip(' ._') or 'commons-material')}{ext}"


def validate_pdf(path: Path) -> tuple[int | None, int | None, int | None, float | None, str]:
    with path.open("rb") as handle:
        if handle.read(5) != b"%PDF-":
            raise ValueError("missing %PDF signature")
    pages = len(PdfReader(str(path), strict=False).pages)
    return None, None, pages, None, "valid PDF"


def validate_image(path: Path) -> tuple[int | None, int | None, int | None, float | None, str]:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        width, height = image.size
        fmt = image.format or "image"
    if width < 300 or height < 300:
        raise ValueError(f"image too small: {width}x{height}")
    return width, height, None, None, f"valid {fmt} image"


def validate_svg(path: Path) -> tuple[int | None, int | None, int | None, float | None, str]:
    root = ET.parse(path).getroot()
    if not root.tag.lower().endswith("svg"):
        raise ValueError("root is not svg")
    return None, None, None, None, "valid SVG"


def validate_djvu(path: Path) -> tuple[int | None, int | None, int | None, float | None, str]:
    with path.open("rb") as handle:
        signature = handle.read(12)
    if not signature.startswith(b"AT&TFORM"):
        raise ValueError("missing DjVu signature")
    return None, None, None, None, "valid DjVu"


def validate_av(path: Path) -> tuple[int | None, int | None, int | None, float | None, str]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe is unavailable")
    completed = subprocess.run(
        [
            ffprobe,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    duration = float(completed.stdout.strip() or "0")
    if duration <= 0:
        raise ValueError("duration is zero")
    return None, None, None, duration, "valid audio/video"


def validate(path: Path, mime: str) -> tuple[int | None, int | None, int | None, float | None, str]:
    if mime == "application/pdf":
        return validate_pdf(path)
    if mime in {"image/jpeg", "image/png", "image/tiff", "image/webp"}:
        return validate_image(path)
    if mime == "image/svg+xml":
        return validate_svg(path)
    if mime == "image/vnd.djvu":
        return validate_djvu(path)
    if mime.startswith("audio/") or mime.startswith("video/") or mime == "application/ogg":
        return validate_av(path)
    raise ValueError(f"unsupported mime: {mime}")


def download_candidate(
    session: requests.Session,
    candidate: Candidate,
    archive_number: int,
    output_dir: Path,
    max_bytes: int,
) -> Record:
    checked = now_utc()
    base_args = dict(
        bucket=candidate.bucket,
        topic=candidate.topic,
        archive_number=None,
        file_title=candidate.file_title,
        local_file_name=None,
        description_url=candidate.description_url,
        original_url=candidate.original_url,
        discovery_query=candidate.query,
        mime=candidate.mime,
        license_short_name=candidate.license_short_name,
        usage_terms=candidate.usage_terms,
        attribution_required=candidate.attribution_required,
        artist=candidate.artist,
        credit=candidate.credit,
        source=candidate.source,
        date=candidate.date,
        advertised_bytes=candidate.advertised_bytes,
        downloaded_bytes=None,
        sha256=None,
        width=candidate.width,
        height=candidate.height,
        pages=None,
        duration_seconds=None,
        status="",
        http_status=None,
        content_type=None,
        checked_at_utc=checked,
        notes="",
    )
    if candidate.advertised_bytes and candidate.advertised_bytes > max_bytes:
        return Record(**{**base_args, "status": "SKIPPED_TOO_LARGE", "notes": f"advertised size exceeds {max_bytes} bytes"})

    try:
        response = request(session, candidate.original_url, stream=True)
    except Exception as exc:
        return Record(**{**base_args, "status": "REQUEST_FAILED", "notes": f"{type(exc).__name__}: {exc}"})

    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip() or None
    if response.status_code != 200:
        status = response.status_code
        response.close()
        return Record(**{**base_args, "status": "HTTP_ERROR", "http_status": status, "content_type": content_type, "notes": "original request was not HTTP 200"})

    local_name = f"{archive_number:03d}__{slugify(candidate.file_title, candidate.mime)}"
    path = output_dir / local_name
    digest = hashlib.sha256()
    size = 0
    try:
        with path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError(f"stream exceeded {max_bytes} bytes")
                digest.update(chunk)
                handle.write(chunk)
        response.close()
        width, height, pages, duration, note = validate(path, candidate.mime)
    except Exception as exc:
        response.close()
        path.unlink(missing_ok=True)
        return Record(**{
            **base_args,
            "status": "VALIDATION_FAILED",
            "http_status": response.status_code,
            "content_type": content_type,
            "downloaded_bytes": size or None,
            "notes": f"{type(exc).__name__}: {exc}",
        })

    return Record(**{
        **base_args,
        "archive_number": archive_number,
        "local_file_name": local_name,
        "status": "DOWNLOADED",
        "http_status": response.status_code,
        "content_type": content_type,
        "downloaded_bytes": size,
        "sha256": digest.hexdigest(),
        "width": width or candidate.width,
        "height": height or candidate.height,
        "pages": pages,
        "duration_seconds": duration,
        "notes": note,
    })


def round_robin(candidates: list[Candidate]) -> list[Candidate]:
    by_topic: dict[str, deque[Candidate]] = defaultdict(deque)
    for candidate in candidates:
        by_topic[candidate.topic].append(candidate)
    ordered: list[Candidate] = []
    active = deque(sorted(by_topic))
    while active:
        topic = active.popleft()
        queue = by_topic[topic]
        if queue:
            ordered.append(queue.popleft())
        if queue:
            active.append(topic)
    return ordered


def write_outputs(
    root: Path,
    records: list[Record],
    candidates_by_bucket: dict[str, list[Candidate]],
    failures: list[dict[str, str]],
    targets: dict[str, int],
) -> None:
    downloaded = [record for record in records if record.status == "DOWNLOADED"]
    manifest = {
        "collection": COLLECTION,
        "generated_at_utc": now_utc(),
        "targets": targets,
        "eligible_candidates_discovered": {bucket: len(items) for bucket, items in candidates_by_bucket.items()},
        "downloaded_counts": {
            bucket: sum(1 for record in downloaded if record.bucket == bucket)
            for bucket in targets
        },
        "total_downloaded": len(downloaded),
        "total_bytes": sum(record.downloaded_bytes or 0 for record in downloaded),
        "license_counts": {
            license_name: sum(1 for record in downloaded if record.license_short_name == license_name)
            for license_name in sorted({record.license_short_name for record in downloaded})
        },
        "mime_counts": {
            mime: sum(1 for record in downloaded if record.mime == mime)
            for mime in sorted({record.mime for record in downloaded})
        },
        "discovery_failures": failures,
        "records": [asdict(record) for record in records],
    }
    (root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    fields = list(asdict(records[0]).keys()) if records else list(Record.__dataclass_fields__)
    with (root / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))

    with (root / "SHA256SUMS.txt").open("w", encoding="utf-8") as handle:
        for record in downloaded:
            handle.write(f"{record.sha256}  {record.bucket}/{record.local_file_name}\n")

    readme = f"""# Commons project materials — 120+ open originals

Generated: {manifest['generated_at_utc']}

## Gates

- additional PDFs: {manifest['downloaded_counts'].get('pdf', 0)} / {targets['pdf']}
- portrait references: {manifest['downloaded_counts'].get('portrait', 0)} / {targets['portrait']}
- ephemera and mixed media: {manifest['downloaded_counts'].get('ephemera', 0)} / {targets['ephemera']}
- total downloaded: {manifest['total_downloaded']}
- total bytes: {manifest['total_bytes']}

Only structured Public Domain, CC0, CC BY and CC BY-SA items are accepted.
The original bytes are retained unchanged. A Commons license card is a strong
discovery signal, but every production image or excerpt still requires an
item-level provenance and attribution review.
"""
    (root / "README.md").write_text(readme, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-pdf", type=int, default=40)
    parser.add_argument("--target-portrait", type=int, default=40)
    parser.add_argument("--target-ephemera", type=int, default=40)
    parser.add_argument("--per-query", type=int, default=40)
    parser.add_argument("--max-pdf-mb", type=int, default=100)
    parser.add_argument("--max-portrait-mb", type=int, default=25)
    parser.add_argument("--max-ephemera-mb", type=int, default=40)
    parser.add_argument("--output-root", default="open-project-materials")
    parser.add_argument("--pause", type=float, default=0.35)
    args = parser.parse_args()

    targets = {
        "pdf": args.target_pdf,
        "portrait": args.target_portrait,
        "ephemera": args.target_ephemera,
    }
    max_bytes = {
        "pdf": args.max_pdf_mb * 1024 * 1024,
        "portrait": args.max_portrait_mb * 1024 * 1024,
        "ephemera": args.max_ephemera_mb * 1024 * 1024,
    }

    root = Path(args.output_root) / COLLECTION
    for bucket in targets:
        (root / bucket).mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json,text/html,*/*"})

    candidates_by_bucket, failures = discover(session, args.per_query)
    records: list[Record] = []

    for bucket, target in targets.items():
        ordered = round_robin(candidates_by_bucket.get(bucket, []))
        archive_number = 1
        for candidate in ordered:
            if archive_number > target:
                break
            record = download_candidate(
                session,
                candidate,
                archive_number,
                root / bucket,
                max_bytes[bucket],
            )
            records.append(record)
            if record.status == "DOWNLOADED":
                print(f"[saved] bucket={bucket} {archive_number}/{target} {record.local_file_name}", flush=True)
                archive_number += 1
            else:
                print(f"[skip] bucket={bucket} status={record.status} title={record.file_title}", flush=True)
            time.sleep(args.pause)

    write_outputs(root, records, candidates_by_bucket, failures, targets)

    downloaded_counts = {
        bucket: sum(1 for record in records if record.bucket == bucket and record.status == "DOWNLOADED")
        for bucket in targets
    }
    print(json.dumps({"downloaded_counts": downloaded_counts, "targets": targets}, ensure_ascii=False))
    failed = {bucket: count for bucket, count in downloaded_counts.items() if count < targets[bucket]}
    if failed:
        print(f"gate failed: {failed}", flush=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
