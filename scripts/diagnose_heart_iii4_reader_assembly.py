#!/usr/bin/env python3
"""Temporary read-only diagnostic for III.4 Heart-and-Spirit reader assembly."""
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
R2 = ROOT / "СЕРИЯ СЕРДЦЕ/64_R2_OT_REGENERATION_INDWELLING.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/125_READER_CHAPTER_III4_HEART_AND_SPIRIT_2026-08-04.md"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v8-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
PRODUCT_REL = Path("src/content/articles/serdce-i-duh.mdx")
OUTPUT = ROOT / "iii4-reader-diagnostic.json"
EXPECTED_RESEARCH_BLOBS = {
    R2: "0bc0cde5a85fe015ca8f394c3fda28074ce19577",
    CURRENT: "6736f90211e34c5dbb7d9943e617102b660bb5be",
    INTEGRATION: "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
EXPECTED_PRODUCT_BLOB = "1f8ede3dd03a2129bbf7d91d49689d25f0f72571"


def blob(root: Path, path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()


def sha(value: Any, *, sort_keys: bool = False) -> str:
    if isinstance(value, str):
        payload = value
    else:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[`*_#|>\[\](){}]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def qcount(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]


def headings(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for match in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text):
        rows.append({"offset": match.start(), "level": len(match.group(1)), "title": match.group(2).strip()})
    for match in re.finditer(r'<h([1-4])\s+[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', text, re.S | re.I):
        rows.append({"offset": match.start(), "level": int(match.group(1)), "title": normalize(match.group(3)), "id": match.group(2)})
    rows.sort(key=lambda row: row["offset"])
    return rows


def heading_for(rows: list[dict[str, Any]], offset: int) -> str:
    current = "frontmatter-or-introduction"
    for row in rows:
        if row["offset"] > offset:
            break
        current = str(row["title"])
    return current


def section_summary(text: str, module: Any) -> dict[str, Any]:
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
            left = max(0, match.start() - 300)
            right = min(len(text), match.end() + 300)
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


def long_exact_transfers(sources: dict[str, str], reader: str) -> list[dict[str, str]]:
    reader_clean = normalize(reader)
    rows: list[dict[str, str]] = []
    for owner, text in sources.items():
        for sentence in re.split(r"(?<=[.!?])\s+", normalize(text)):
            sentence = sentence.strip()
            if len(sentence) >= 110 and sentence in reader_clean:
                rows.append({"owner": owner, "sentenceSha256": sha(sentence)})
    return rows


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
product_path = product_root / PRODUCT_REL

for path, expected in EXPECTED_RESEARCH_BLOBS.items():
    assert path.is_file(), path
    assert blob(ROOT, path.relative_to(ROOT)) == expected, (path, blob(ROOT, path.relative_to(ROOT)), expected)
assert product_path.is_file(), product_path
assert blob(product_root, PRODUCT_REL) == EXPECTED_PRODUCT_BLOB, (blob(product_root, PRODUCT_REL), EXPECTED_PRODUCT_BLOB)
assert READER.is_file(), READER

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

texts = {
    "PRODUCT": product_path.read_text(encoding="utf-8"),
    "R2": R2.read_text(encoding="utf-8"),
}
scans = {
    "PRODUCT": module.scan_owner(module.p(str(PRODUCT_REL), "III.4 Product owner"), product_root),
    "R2": module.scan_owner(module.r(str(R2.relative_to(ROOT)), "III.4 R2 continuity dossier"), product_root),
}
reader_text = READER.read_text(encoding="utf-8")
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "III.4 assembled reader"), product_root)

union_refs = sorted(set(scans["PRODUCT"]["scriptureReferences"]) | set(scans["R2"]["scriptureReferences"]), key=str.casefold)
union_urls = sorted(set(scans["PRODUCT"]["externalLinks"]) | set(scans["R2"]["externalLinks"]), key=str.casefold)
union_internal = sorted(set(scans["PRODUCT"]["internalArticleLinks"]) | set(scans["R2"]["internalArticleLinks"]), key=str.casefold)
owner_url_records = sum(len(scans[owner]["externalLinks"]) for owner in scans)
reader_words = len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b", reader_text))
transfers = long_exact_transfers(texts, reader_text)

owners = []
for owner in ("PRODUCT", "R2"):
    text = texts[owner]
    scan = scans[owner]
    owner_headings = [{k: row[k] for k in row if k != "offset"} for row in headings(text)]
    owners.append({
        "id": owner,
        "path": str(PRODUCT_REL if owner == "PRODUCT" else R2.relative_to(ROOT)),
        "gitBlob": EXPECTED_PRODUCT_BLOB if owner == "PRODUCT" else EXPECTED_RESEARCH_BLOBS[R2],
        "fullSha256": sha(text),
        "scan": {
            "scriptureReferences": len(scan["scriptureReferences"]),
            "quotationSurfaces": qcount(scan),
            "externalLinks": len(scan["externalLinks"]),
            "internalArticleLinks": len(scan["internalArticleLinks"]),
            "footnoteDefinitions": scan["footnoteDefinitions"],
            "sourceHeadings": scan["sourceHeadings"],
        },
        "scriptureReferenceSet": sorted(scan["scriptureReferences"], key=str.casefold),
        "externalLinkSet": sorted(scan["externalLinks"], key=str.casefold),
        "internalArticleLinkSet": sorted(scan["internalArticleLinks"], key=str.casefold),
        "headingManifest": owner_headings,
        "sectionSummary": section_summary(text, module),
    })

payload = {
    "authorityId": "HEART-III4-READER-DIAGNOSTIC-2026-08-04",
    "researchHead": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "productCommit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip(),
    "owners": owners,
    "historicalUnion": {
        "ownerSurfaces": 2,
        "scriptureReferences": len(union_refs),
        "quotationSurfaces": qcount(scans["PRODUCT"]) + qcount(scans["R2"]),
        "uniqueExternalLinks": len(union_urls),
        "ownerUrlRecords": owner_url_records,
        "internalArticleLinks": len(union_internal),
        "scriptureReferenceSet": union_refs,
        "externalLinkSet": union_urls,
        "internalArticleLinkSet": union_internal,
    },
    "reader": {
        "path": str(READER.relative_to(ROOT)),
        "gitBlob": blob(ROOT, READER.relative_to(ROOT)),
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
assert 1500 <= reader_words <= 1900, reader_words
assert payload["reader"]["quotationSurfaces"] == 0
assert payload["reader"]["externalLinks"] == 0
assert payload["reader"]["internalArticleLinks"] == 0
assert payload["reader"]["footnoteDefinitions"] == 0
assert payload["reader"]["sourceHeadings"] == []
assert transfers == []
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "owners": [{"id": row["id"], "scan": row["scan"], "fullSha256": row["fullSha256"]} for row in owners],
    "historicalUnion": {k: v for k, v in payload["historicalUnion"].items() if not k.endswith("Set")},
    "reader": payload["reader"],
    "outputSha256": sha(OUTPUT.read_text(encoding="utf-8")),
}, ensure_ascii=False, indent=2))
