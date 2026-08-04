#!/usr/bin/env python3
"""Temporary read-only diagnostic for the Part IV Heart-and-Word reader assembly."""
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
READER = ROOT / "СЕРИЯ СЕРДЦЕ/125_READER_CHAPTER_IV_HEART_AND_WORD_2026-08-04.md"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v8-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
OUTPUT = ROOT / "part4-reader-diagnostic.json"
EXPECTED_BLOBS = {
    SOURCE: "ceff41072982c664606bc377ef8f1f0f241677da",
    CURRENT: "6736f90211e34c5dbb7d9943e617102b660bb5be",
    INTEGRATION: "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[`*_#|>\[\](){}]", " ", value)
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


def source_section_summary(text: str, module: Any) -> dict[str, Any]:
    heading_rows = headings(text)
    patterns = [
        ("RUSSIAN", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY", re.compile(r"“([^”\n]{8,})”")),
        ("STRAIGHT", re.compile(r'"([^"\n]{8,})"')),
        ("MD_BLOCK", re.compile(r"(?m)^\s*>\s?(\S.*)$")),
        ("HTML_BLOCK", re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.S | re.I)),
    ]
    buckets: dict[str, dict[str, Any]] = {}
    for surface_type, pattern in patterns:
        for match in pattern.finditer(text):
            section = heading_for(heading_rows, match.start())
            bucket = buckets.setdefault(section, {"quotationSurfaces": 0, "types": Counter(), "scriptureNearby": set()})
            bucket["quotationSurfaces"] += 1
            bucket["types"][surface_type] += 1
            left = max(0, match.start() - 250)
            right = min(len(text), match.end() + 250)
            for item in module.SCRIPTURE_RE.finditer(text[left:right]):
                bucket["scriptureNearby"].add(module.normalize_ref(item.group(0)))
    return {
        key: {
            "quotationSurfaces": value["quotationSurfaces"],
            "types": dict(sorted(value["types"].items())),
            "scriptureNearby": sorted(value["scriptureNearby"], key=str.casefold),
        }
        for key, value in sorted(buckets.items())
    }


def long_exact_transfers(source: str, reader: str) -> list[str]:
    source_clean = normalize(source)
    reader_clean = normalize(reader)
    candidates = []
    for sentence in re.split(r"(?<=[.!?])\s+", source_clean):
        sentence = sentence.strip()
        if len(sentence) >= 110 and sentence in reader_clean:
            candidates.append(sentence)
    return candidates


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

for path, expected in EXPECTED_BLOBS.items():
    assert path.is_file(), path
    actual = blob(path)
    assert actual == expected, (path, actual, expected)
assert READER.is_file(), READER

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

source_text = SOURCE.read_text(encoding="utf-8")
reader_text = READER.read_text(encoding="utf-8")
source_scan = module.scan_owner(module.r(str(SOURCE.relative_to(ROOT)), "Part IV R7a owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part IV reader"), product_root)
reader_words = len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b", reader_text))
transfers = long_exact_transfers(source_text, reader_text)

payload = {
    "authorityId": "HEART-PART4-READER-DIAGNOSTIC-2026-08-04",
    "researchHead": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "immutableBlobs": {str(path.relative_to(ROOT)): expected for path, expected in EXPECTED_BLOBS.items()},
    "source": {
        "path": str(SOURCE.relative_to(ROOT)),
        "gitBlob": blob(SOURCE),
        "fullSha256": sha(source_text),
        "headings": [{"level": row["level"], "title": row["title"]} for row in headings(source_text)],
        "scan": {
            "scriptureReferences": len(source_scan["scriptureReferences"]),
            "quotationSurfaces": qcount(source_scan),
            "externalLinks": len(source_scan["externalLinks"]),
            "internalArticleLinks": len(source_scan["internalArticleLinks"]),
            "footnoteDefinitions": source_scan["footnoteDefinitions"],
            "sourceHeadings": source_scan["sourceHeadings"],
        },
        "scriptureReferenceSet": sorted(source_scan["scriptureReferences"], key=str.casefold),
        "externalLinkSet": sorted(source_scan["externalLinks"], key=str.casefold),
        "internalArticleLinkSet": sorted(source_scan["internalArticleLinks"], key=str.casefold),
        "sectionSummary": source_section_summary(source_text, module),
    },
    "reader": {
        "path": str(READER.relative_to(ROOT)),
        "gitBlob": blob(READER),
        "fullSha256": sha(reader_text),
        "words": reader_words,
        "scriptureReferences": len(reader_scan["scriptureReferences"]),
        "scriptureReferenceSet": sorted(reader_scan["scriptureReferences"], key=str.casefold),
        "quotationSurfaces": qcount(reader_scan),
        "externalLinks": len(reader_scan["externalLinks"]),
        "internalArticleLinks": len(reader_scan["internalArticleLinks"]),
        "footnoteDefinitions": reader_scan["footnoteDefinitions"],
        "sourceHeadings": reader_scan["sourceHeadings"],
        "longExactSentenceTransfers": transfers,
    },
}
assert 1450 <= reader_words <= 1900, reader_words
assert payload["reader"]["quotationSurfaces"] == 0
assert payload["reader"]["externalLinks"] == 0
assert payload["reader"]["internalArticleLinks"] == 0
assert payload["reader"]["footnoteDefinitions"] == 0
assert payload["reader"]["sourceHeadings"] == []
assert transfers == []

OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "sourceScan": payload["source"]["scan"],
    "sourceSha256": payload["source"]["fullSha256"],
    "reader": payload["reader"],
    "outputSha256": sha(OUTPUT.read_text(encoding="utf-8")),
}, ensure_ascii=False, indent=2))
