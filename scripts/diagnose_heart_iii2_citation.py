#!/usr/bin/env python3
"""Temporary read-only III.2 dossier citation and link decomposition."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
EXEGESIS = ROOT / "СЕРИЯ СЕРДЦЕ/62_R1_REGENERATION_EXEGESIS.md"
SYSTEMATICS = ROOT / "СЕРИЯ СЕРДЦЕ/63_R1_REGENERATION_SYSTEMATICS.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/121_READER_CHAPTER_III2_REGENERATION_2026-08-04.md"
ASSEMBLY = ROOT / "data/heart-iii2-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v7-2026-08-04.json"
OUTPUT = ROOT / "iii2-citation-diagnostic.json"
EXPECTED_BLOBS = {
    EXEGESIS: "d75117cf00cf0bb859fc40a67a26dca4c039ec57",
    SYSTEMATICS: "143b3477792f52a9fa5721431ff64e7ffb2a4d5a",
    READER: "a3f66d265cd66eff7187dcd5c511faf645833988",
    ASSEMBLY: "82e2a70977d67591c3a290248f102601c7c4d5dc",
    CURRENT: "86c932764ca2eba3bec726876f2cb73a0c78e762",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
HOLD_TERMS = [
    "НЕ ВЕРИФИЦИРОВАНО", "не верифицирован", "кандидат", "Открытые вопросы",
    "выходные данные установить", "не использовать", "опасност", "неточно",
    "не найден", "не подтверд", "сомнитель", "проверить атрибуцию", "HOLD",
    "NO-DIRECT-QUOTE", "перед публикацией", "желательно контрольное сличение",
]
VERIFIED_TERMS = [
    "ВЕРИФИЦИРОВАНО", "SAFE CLOSURE", "подтверждено", "точная фраза",
    "дословно", "проверен", "проверено",
]


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def sha(value: Any, *, sort_keys: bool = False) -> str:
    if isinstance(value, str):
        payload = value
    else:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


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


def extract_surfaces(text: str, owner: str, module: Any) -> list[dict[str, Any]]:
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
            left = max(0, match.start() - 300)
            right = min(len(text), match.end() + 300)
            nearby = sorted(
                {module.normalize_ref(item.group(0)) for item in module.SCRIPTURE_RE.finditer(text[left:right])},
                key=str.casefold,
            )
            rows.append({
                "owner": owner,
                "position": match.start(),
                "section": heading_for(heading_rows, match.start()),
                "type": surface_type,
                "sha256": sha(value),
                "chars": len(value),
                "nearbyScripture": nearby,
            })
    rows.sort(key=lambda row: int(row["position"]))
    for index, row in enumerate(rows, start=1):
        row["ownerIndex"] = index
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


def qcount(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

for path, expected in EXPECTED_BLOBS.items():
    assert path.is_file(), path
    assert git_blob(path) == expected, (path, git_blob(path), expected)

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

texts = {
    "R1_EXEGESIS": EXEGESIS.read_text(encoding="utf-8"),
    "R1_SYSTEMATICS": SYSTEMATICS.read_text(encoding="utf-8"),
}
scans = {
    "R1_EXEGESIS": module.scan_owner(module.r(str(EXEGESIS.relative_to(ROOT)), "III.2 R1 exegesis owner"), product_root),
    "R1_SYSTEMATICS": module.scan_owner(module.r(str(SYSTEMATICS.relative_to(ROOT)), "III.2 R1 systematics owner"), product_root),
}
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "III.2 assembled reader"), product_root)

surfaces_by_owner = {
    owner: extract_surfaces(text, owner, module) for owner, text in texts.items()
}
all_surfaces = surfaces_by_owner["R1_EXEGESIS"] + surfaces_by_owner["R1_SYSTEMATICS"]
base_manifest = [
    {key: row[key] for key in ("owner", "ownerIndex", "section", "type", "sha256", "chars", "nearbyScripture")}
    for row in all_surfaces
]
section_summary: dict[str, dict[str, Any]] = {}
for row in all_surfaces:
    key = f"{row['owner']}::{row['section']}"
    bucket = section_summary.setdefault(key, {"surfaces": 0, "types": Counter(), "withNearbyScripture": 0})
    bucket["surfaces"] += 1
    bucket["types"][row["type"]] += 1
    bucket["withNearbyScripture"] += int(bool(row["nearbyScripture"]))
section_summary = {
    key: {
        "surfaces": value["surfaces"],
        "types": dict(sorted(value["types"].items())),
        "withNearbyScripture": value["withNearbyScripture"],
    }
    for key, value in sorted(section_summary.items())
}

url_registry: list[dict[str, Any]] = []
for owner, text in texts.items():
    for url in sorted(scans[owner]["externalLinks"], key=str.casefold):
        contexts = contexts_for_url(text, url)
        url_registry.append({
            "owner": owner,
            "url": url,
            "status": classify_url(contexts),
            "occurrences": len(contexts),
            "sections": sorted({row["section"] for row in contexts}, key=str.casefold),
            "contexts": contexts,
            "readerTransfer": False,
            "directQuoteBulkApproval": False,
        })

union_refs = sorted(
    set(scans["R1_EXEGESIS"]["scriptureReferences"]) | set(scans["R1_SYSTEMATICS"]["scriptureReferences"]),
    key=str.casefold,
)
union_internal = sorted(
    set(scans["R1_EXEGESIS"]["internalArticleLinks"]) | set(scans["R1_SYSTEMATICS"]["internalArticleLinks"]),
    key=str.casefold,
)
status_counts = dict(sorted(Counter(row["status"] for row in url_registry).items()))

payload = {
    "authorityId": "HEART-III2-CITATION-DIAGNOSTIC-2026-08-04",
    "researchHead": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "immutableBlobs": {str(path.relative_to(ROOT)): expected for path, expected in EXPECTED_BLOBS.items()},
    "owners": [
        {
            "id": owner,
            "path": str((EXEGESIS if owner == "R1_EXEGESIS" else SYSTEMATICS).relative_to(ROOT)),
            "fullSha256": sha(text),
            "headings": [{key: row[key] for key in ("level", "title")} for row in headings(text)],
            "scan": {
                "scriptureReferences": len(scans[owner]["scriptureReferences"]),
                "quotationSurfaces": qcount(scans[owner]),
                "externalLinks": len(scans[owner]["externalLinks"]),
                "internalArticleLinks": len(scans[owner]["internalArticleLinks"]),
                "sourceHeadings": scans[owner]["sourceHeadings"],
            },
        }
        for owner, text in texts.items()
    ],
    "historicalUnion": {
        "ownerSurfaces": 2,
        "scriptureReferences": len(union_refs),
        "quotationSurfaces": len(all_surfaces),
        "externalLinks": len(url_registry),
        "internalArticleLinks": len(union_internal),
        "scriptureReferenceSetSha256": sha(union_refs),
        "baseSurfaceManifestSha256": sha(base_manifest),
        "sectionSummarySha256": sha(section_summary, sort_keys=True),
        "externalLinkSetSha256": sha([{key: row[key] for key in ("owner", "url")} for row in url_registry]),
    },
    "scriptureReferences": union_refs,
    "surfaceManifest": base_manifest,
    "sectionSummary": section_summary,
    "urlStatusCounts": status_counts,
    "urlRegistry": url_registry,
    "internalLinks": union_internal,
    "readerReview": {
        "scriptureReferences": len(reader_scan["scriptureReferences"]),
        "quotationSurfaces": qcount(reader_scan),
        "externalLinks": len(reader_scan["externalLinks"]),
        "internalArticleLinks": len(reader_scan["internalArticleLinks"]),
        "footnoteDefinitions": reader_scan["footnoteDefinitions"],
        "sourceHeadings": reader_scan["sourceHeadings"],
    },
}
assert payload["historicalUnion"]["scriptureReferences"] == 115
assert payload["historicalUnion"]["quotationSurfaces"] == 609
assert payload["historicalUnion"]["externalLinks"] == 67
assert payload["historicalUnion"]["internalArticleLinks"] == 1
assert payload["readerReview"] == {
    "scriptureReferences": 25,
    "quotationSurfaces": 0,
    "externalLinks": 0,
    "internalArticleLinks": 0,
    "footnoteDefinitions": 0,
    "sourceHeadings": [],
}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "historicalUnion": payload["historicalUnion"],
    "urlStatusCounts": status_counts,
    "readerReview": payload["readerReview"],
    "outputSha256": sha(OUTPUT.read_text(encoding="utf-8")),
}, ensure_ascii=False, indent=2))
