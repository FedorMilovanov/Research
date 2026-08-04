#!/usr/bin/env python3
"""Temporary exact I.1 citation-surface decomposition."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
PRODUCT_PATH = Path("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx")
READER_PATH = Path("СЕРИЯ СЕРДЦЕ/105_READER_CHAPTER_I1_WHAT_BIBLE_CALLS_HEART_2026-08-04.md")

parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

product_text = (product_root / PRODUCT_PATH).read_text(encoding="utf-8")
reader_text = (ROOT / READER_PATH).read_text(encoding="utf-8")
product_scan = module.scan_owner(module.p(str(PRODUCT_PATH), "historical full I.1 owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER_PATH), "assembled I.1 reader"), product_root)

section_starts = [(m.start(), m.group(1)) for m in re.finditer(r'<h2\s+id="([^"]+)"', product_text)]

def section_for(offset: int) -> str:
    current = "frontmatter-or-introduction"
    for start, section_id in section_starts:
        if start > offset:
            break
        current = section_id
    return current


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def nearby_refs(start: int, end: int) -> list[str]:
    left = max(0, start - 220)
    right = min(len(product_text), end + 220)
    return sorted({module.normalize_ref(m.group(0)) for m in module.SCRIPTURE_RE.finditer(product_text[left:right])}, key=str.casefold)

surfaces: list[dict[str, Any]] = []
patterns = [
    ("RUSSIAN_GUILLEMETS", re.compile(r"«([^»\n]{8,})»")),
    ("CURLY_QUOTES", re.compile(r"“([^”\n]{8,})”")),
]
for surface_type, pattern in patterns:
    for match in pattern.finditer(product_text):
        value = normalize(match.group(1))
        surfaces.append({
            "type": surface_type,
            "sectionId": section_for(match.start()),
            "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
            "characters": len(value),
            "nearbyScriptureReferences": nearby_refs(match.start(), match.end()),
            "text": value,
        })

for match in re.finditer(r"(?m)^\s*>\s?(\S.*)$", product_text):
    value = normalize(match.group(1))
    surfaces.append({
        "type": "MARKDOWN_BLOCKQUOTE",
        "sectionId": section_for(match.start()),
        "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
        "characters": len(value),
        "nearbyScriptureReferences": nearby_refs(match.start(), match.end()),
        "text": value,
    })

for match in re.finditer(r"<blockquote[^>]*>(.*?)</blockquote>", product_text, flags=re.S | re.I):
    value = normalize(match.group(1))
    surfaces.append({
        "type": "HTML_BLOCKQUOTE",
        "sectionId": section_for(match.start()),
        "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
        "characters": len(value),
        "nearbyScriptureReferences": nearby_refs(match.start(), match.end()),
        "text": value,
    })

surfaces.sort(key=lambda row: (row["sectionId"], row["type"], row["sha256"]))
section_summary: dict[str, dict[str, int]] = {}
for row in surfaces:
    summary = section_summary.setdefault(row["sectionId"], {"surfaces": 0, "withNearbyScripture": 0})
    summary["surfaces"] += 1
    summary["withNearbyScripture"] += int(bool(row["nearbyScriptureReferences"]))

payload = {
    "product": {
        "repository": "FedorMilovanov/gb-is-my-strength",
        "commit": "0fbe7d1ead9ebd1bea867418e254da438ec63329",
        "path": str(PRODUCT_PATH),
        "gitBlob": "acc12804f5b2450efebbb6e0b2cabd31066ef48c",
        "fullSha256": hashlib.sha256(product_text.encode("utf-8")).hexdigest(),
        "scan": product_scan,
        "quotationSurfaceCount": len(surfaces),
        "surfaceTypeCounts": {kind: sum(1 for row in surfaces if row["type"] == kind) for kind in sorted({row["type"] for row in surfaces})},
        "sectionSummary": section_summary,
        "surfaces": surfaces,
        "internalArticleLinks": product_scan["internalArticleLinks"],
        "sourceMarkers": {
            "synodalDeclaration": "Все библейские цитаты — по Синодальному переводу" in product_text,
            "sourcesSection": '<h2 id="istochniki">' in product_text,
            "accuracyNotice": "Нашли неточность?" in product_text,
        },
    },
    "reader": {
        "path": str(READER_PATH),
        "gitBlob": "a5d35df1a87ab39abc8a85b1d84f1b1ab03da105",
        "fullSha256": hashlib.sha256(reader_text.encode("utf-8")).hexdigest(),
        "scan": reader_scan,
    },
    "assembly": json.loads((ROOT / "data/heart-i1-reader-assembly-2026-08-04.json").read_text(encoding="utf-8")),
    "currentV3": json.loads((ROOT / "data/heart-entry-citation-pass-current-v3-2026-08-04.json").read_text(encoding="utf-8")),
    "triage": json.loads((ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json").read_text(encoding="utf-8")),
}
args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "productRefs": len(product_scan["scriptureReferences"]),
    "productQuotationSurfaces": len(surfaces),
    "surfaceTypeCounts": payload["product"]["surfaceTypeCounts"],
    "sectionsWithSurfaces": section_summary,
    "internalArticleLinks": product_scan["internalArticleLinks"],
    "sourceMarkers": payload["product"]["sourceMarkers"],
    "readerRefs": len(reader_scan["scriptureReferences"]),
    "readerQuotationSurfaces": reader_scan["inlineQuotationSegments"] + reader_scan["markdownBlockquotes"] + reader_scan["htmlBlockquotes"],
    "readerLinks": len(reader_scan["externalLinks"]) + len(reader_scan["internalArticleLinks"]),
}, ensure_ascii=False))
