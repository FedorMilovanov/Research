#!/usr/bin/env python3
"""Temporary read-only Part IV citation/link decomposition."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
SOURCE = ROOT / "СЕРИЯ СЕРДЦЕ/68_R7A_WORD_AND_HEART.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/129_READER_CHAPTER_IV_HEART_AND_WORD_2026-08-04.md"
ASSEMBLY = ROOT / "data/heart-part4-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v9-2026-08-04.json"
OUTPUT = ROOT / "part4-citation-diagnostic.json"
EXPECTED_BLOBS = {
    SOURCE: "ceff41072982c664606bc377ef8f1f0f241677da",
    READER: "55eda03de3cc29e7946a705fe0fffbd2acc4e36d",
    ASSEMBLY: "58f0922734601cf9cf16e448d50836b269b624e0",
    CURRENT: "d8a65b5233a471e024f5642e1dc3d1a50f13babf",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
HOLD_TERMS = [
    "НЕ ВЕРИФИЦИРОВАНО", "не верифицирован", "кандидат", "Открытые вопросы",
    "не использовать", "неточно", "не найден", "не подтверд", "сомнитель",
    "проверить", "HOLD", "NO-DIRECT-QUOTE", "BOOK-PAGE-HOLD",
    "DO-NOT-DIRECT-QUOTE", "перед публикацией", "контрольное сличение",
    "локатор", "не quote-ready", "ATTRIBUTED-ONLY",
]
VERIFIED_TERMS = [
    "ВЕРИФИЦИРОВАНО", "SAFE CLOSURE", "подтверждено", "точная фраза",
    "дословно", "проверен", "проверено", "VERIFIED",
]
ATTRIBUTED_TERMS = [
    "Цитатный банк", "Цитаты", "Свидетели", "Источник", "Источники",
    "Реформаторы", "Пуритане", "Баптисты", "Современные", "Отцы",
]
EDITORIAL_TERMS = [
    "Задача и место", "Выводы", "Тезисы", "структура", "Чего избегать",
    "Открытые вопросы", "Итог", "Коротко", "Статус", "Применение для статьи",
]


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def sha(value: Any, *, sort_keys: bool = False) -> str:
    if isinstance(value, str):
        payload = value
    else:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def qcount(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]


def headings(text: str) -> list[dict[str, Any]]:
    return [
        {"offset": match.start(), "level": len(match.group(1)), "title": match.group(2).strip()}
        for match in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text)
    ]


def heading_for(rows: list[dict[str, Any]], offset: int) -> str:
    current = "frontmatter-or-introduction"
    for row in rows:
        if row["offset"] > offset:
            break
        current = str(row["title"])
    return current


def role(section: str) -> str:
    if any(term.casefold() in section.casefold() for term in ATTRIBUTED_TERMS):
        return "ATTRIBUTED_WITNESS_OR_SOURCE_BANK_SURFACE"
    if any(term.casefold() in section.casefold() for term in EDITORIAL_TERMS):
        return "EDITORIAL_STRUCTURAL_OR_CAUTION_SURFACE"
    return "EXEGETICAL_SCRIPTURE_OR_DOCTRINAL_SURFACE"


def extract_surfaces(text: str, module: Any) -> list[dict[str, Any]]:
    heading_rows = headings(text)
    rows: list[dict[str, Any]] = []
    patterns = [
        ("RUSSIAN", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY", re.compile(r"“([^”\n]{8,})”")),
        ("MD_BLOCK", re.compile(r"(?m)^\s*>\s?(\S.*)$")),
        ("HTML_BLOCK", re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.S | re.I)),
    ]
    for surface_type, pattern in patterns:
        for match in pattern.finditer(text):
            value = normalize(match.group(1))
            section = heading_for(heading_rows, match.start())
            left = max(0, match.start() - 300)
            right = min(len(text), match.end() + 300)
            nearby = sorted(
                {module.normalize_ref(item.group(0)) for item in module.SCRIPTURE_RE.finditer(text[left:right])},
                key=str.casefold,
            )
            rows.append({
                "position": match.start(),
                "section": section,
                "type": surface_type,
                "sha256": sha(value),
                "chars": len(value),
                "nearbyScripture": nearby,
                "class": role(section),
            })
    rows.sort(key=lambda row: int(row["position"]))
    for index, row in enumerate(rows, start=1):
        row["surfaceIndex"] = index
        del row["position"]
    return rows


def contexts_for_url(text: str, url: str) -> list[dict[str, Any]]:
    heading_rows = headings(text)
    rows: list[dict[str, Any]] = []
    cursor = 0
    while True:
        offset = text.find(url, cursor)
        if offset < 0:
            break
        left = max(0, offset - 500)
        right = min(len(text), offset + len(url) + 500)
        context = normalize(text[left:right])
        rows.append({
            "section": heading_for(heading_rows, offset),
            "contextSha256": sha(context),
            "holdTerms": sorted({term for term in HOLD_TERMS if term.casefold() in context.casefold()}, key=str.casefold),
            "verifiedTerms": sorted({term for term in VERIFIED_TERMS if term.casefold() in context.casefold()}, key=str.casefold),
        })
        cursor = offset + 1
    return rows


def classify_url(contexts: list[dict[str, Any]]) -> str:
    if any(row["holdTerms"] for row in contexts) or any("Открытые вопросы" in row["section"] for row in contexts):
        return "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
    if any(row["verifiedTerms"] for row in contexts):
        return "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
    return "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER"


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

for path, expected in EXPECTED_BLOBS.items():
    assert path.is_file(), path
    assert blob(path) == expected, (path, blob(path), expected)

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

source_text = SOURCE.read_text(encoding="utf-8")
reader_text = READER.read_text(encoding="utf-8")
source_scan = module.scan_owner(module.r(str(SOURCE.relative_to(ROOT)), "Part IV R7a owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part IV reader"), product_root)
surfaces = extract_surfaces(source_text, module)
assert len(surfaces) == 225 and qcount(source_scan) == 225
base_manifest = [
    {key: row[key] for key in ("surfaceIndex", "section", "type", "sha256", "chars", "nearbyScripture")}
    for row in surfaces
]
classified_manifest = [{**base, "class": surface["class"]} for base, surface in zip(base_manifest, surfaces)]
role_counts = dict(sorted(Counter(row["class"] for row in classified_manifest).items()))
role_section_map: dict[str, set[str]] = {}
for row in classified_manifest:
    role_section_map.setdefault(row["class"], set()).add(row["section"])
role_section_map = {
    role_name: sorted(sections, key=str.casefold)
    for role_name, sections in sorted(role_section_map.items())
}
section_summary: dict[str, dict[str, Any]] = {}
for row in classified_manifest:
    bucket = section_summary.setdefault(row["section"], {"surfaces": 0, "classes": Counter(), "types": Counter()})
    bucket["surfaces"] += 1
    bucket["classes"][row["class"]] += 1
    bucket["types"][row["type"]] += 1
section_summary = {
    key: {
        "surfaces": value["surfaces"],
        "classes": dict(sorted(value["classes"].items())),
        "types": dict(sorted(value["types"].items())),
    }
    for key, value in sorted(section_summary.items())
}

urls = sorted(source_scan["externalLinks"], key=str.casefold)
url_registry: list[dict[str, Any]] = []
for url in urls:
    contexts = contexts_for_url(source_text, url)
    url_registry.append({
        "url": url,
        "status": classify_url(contexts),
        "occurrences": len(contexts),
        "sections": sorted({row["section"] for row in contexts}, key=str.casefold),
        "contexts": contexts,
        "readerTransfer": False,
        "directQuoteBulkApproval": False,
    })

internal_registry: list[dict[str, Any]] = []
for path in sorted(source_scan["internalArticleLinks"], key=str.casefold):
    containing_urls = sorted([url for url in urls if path in url], key=str.casefold)
    if containing_urls:
        internal_registry.append({
            "path": path,
            "status": "EXTERNAL_URL_PATH_FRAGMENT_FALSE_POSITIVE",
            "containingExternalUrls": containing_urls,
            "productTargetChecked": False,
            "readerTransfer": False,
        })
    else:
        slug = path.removeprefix("/articles/").removesuffix("/")
        target = Path("src/content/articles") / f"{slug}.mdx"
        target_path = product_root / target
        internal_registry.append({
            "path": path,
            "status": "PINNED_PRODUCT_TARGET_EXISTS" if target_path.is_file() else "UNRESOLVED_PRODUCT_TARGET",
            "target": str(target),
            "exists": target_path.is_file(),
            "targetBlob": subprocess.check_output(["git", "hash-object", str(target)], cwd=product_root, text=True).strip() if target_path.is_file() else None,
            "readerTransfer": False,
        })

refs = sorted(source_scan["scriptureReferences"], key=str.casefold)
payload = {
    "authorityId": "HEART-PART4-CITATION-DIAGNOSTIC-2026-08-04",
    "researchHead": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "sourceCounts": {
        "scriptureReferences": len(refs),
        "quotationSurfaces": len(surfaces),
        "externalLinks": len(urls),
        "internalArticleLinks": len(internal_registry),
    },
    "manifestHashes": {
        "scriptureReferenceSetSha256": sha(refs),
        "baseSurfaceManifestSha256": sha(base_manifest),
        "classifiedSurfaceManifestSha256": sha(classified_manifest),
        "roleSectionMapSha256": sha(role_section_map, sort_keys=True),
        "sectionSummarySha256": sha(section_summary, sort_keys=True),
        "externalLinkSetSha256": sha(urls),
        "internalLinkSetSha256": sha([row["path"] for row in internal_registry]),
    },
    "roleCounts": role_counts,
    "roleSectionMap": role_section_map,
    "sectionSummary": section_summary,
    "surfaceManifest": base_manifest,
    "classifiedSurfaceManifest": classified_manifest,
    "urlStatusCounts": dict(sorted(Counter(row["status"] for row in url_registry).items())),
    "urlRegistry": url_registry,
    "internalRegistry": internal_registry,
    "reader": {
        "words": len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b", reader_text)),
        "scriptureReferences": len(reader_scan["scriptureReferences"]),
        "quotationSurfaces": qcount(reader_scan),
        "externalLinks": len(reader_scan["externalLinks"]),
        "internalArticleLinks": len(reader_scan["internalArticleLinks"]),
        "footnoteDefinitions": reader_scan["footnoteDefinitions"],
        "sourceHeadings": reader_scan["sourceHeadings"],
        "gitBlob": blob(READER),
        "fullSha256": sha(reader_text),
    },
}
assert payload["sourceCounts"] == {
    "scriptureReferences": 65,
    "quotationSurfaces": 225,
    "externalLinks": 36,
    "internalArticleLinks": 2,
}
assert payload["reader"] == {
    "words": 1580,
    "scriptureReferences": 18,
    "quotationSurfaces": 0,
    "externalLinks": 0,
    "internalArticleLinks": 0,
    "footnoteDefinitions": 0,
    "sourceHeadings": [],
    "gitBlob": "55eda03de3cc29e7946a705fe0fffbd2acc4e36d",
    "fullSha256": "b3a103936c9495484a2a5478262ec4d4e47ab49f5192dd523add1deeb7d23d58",
}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "sourceCounts": payload["sourceCounts"],
    "manifestHashes": payload["manifestHashes"],
    "roleCounts": role_counts,
    "urlStatusCounts": payload["urlStatusCounts"],
    "internalRegistry": internal_registry,
    "reader": payload["reader"],
    "outputSha256": sha(OUTPUT.read_text(encoding="utf-8")),
}, ensure_ascii=False, indent=2))
