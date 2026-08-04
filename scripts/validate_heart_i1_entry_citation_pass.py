#!/usr/bin/env python3
"""Validate the completed I.1 entry citation pass."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
RECEIPT = ROOT / "data/heart-i1-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-i1-reader-assembly-2026-08-04.json"
CURRENT_V3 = ROOT / "data/heart-entry-citation-pass-current-v3-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/105_READER_CHAPTER_I1_WHAT_BIBLE_CALLS_HEART_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/107_I1_CITATION_REVIEW_2026-08-04.md"
PRODUCT_PATH = Path("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx")

BLOBS = {
    ASSEMBLY: "e4b805585fbe9606efb5ed4c59861d52ec08c699",
    CURRENT_V3: "407c8d78baa966a3336e7bd60edfa51178b74f32",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    READER: "a5d35df1a87ab39abc8a85b1d84f1b1ab03da105",
}
PRODUCT_BLOB = "acc12804f5b2450efebbb6e0b2cabd31066ef48c"
PRODUCT_SHA = "50657f3473c06e16d75ffe740828a9311f642562e824f148113ae28ff9b03c07"
REFERENCE_SET_SHA = "054912d08830664a4f898ea326b47dd421986fe4dc80cad80f9061342d1013d5"
READER_REFERENCE_SET_SHA = "8a14e3cb29cc087963479ac9ae2e4e65ac7414615cb691233299d2eb520aedf4"
MANIFEST_SHA = "422e855d715df99f5f4648f337366f94897eaa25413a165a7b11b71878d5f387"
CLASS_MAP_SHA = "093fc3619f9c36e55ed6ca6399affc88f4caa093720c2b892647997ae51d71d8"
SECTION_SUMMARY_SHA = "f5b48c44baddefc71a965a42c6365c301f5845e4b9b15f429a5f3efecc8c4590"
EXPECTED_COUNTS = {
    "EDITORIAL_OR_COLLOQUIAL": 18,
    "LEXICAL_OR_TRANSLATION": 5,
    "SCRIPTURE_DIRECT_RUSSIAN_SYNODAL": 69,
    "TITLE_OR_LINK_LABEL": 6,
}
EXPECTED_LINKS = [
    "/articles/krajne-li-isporcheno-serdce/",
    "/articles/novoe-serdce/",
    "/articles/serdce-hrista-k-nemoshchnym/",
    "/articles/skrytye-idoly-serdca/",
]
EXPECTED_TARGETS = [
    "src/content/articles/krajne-li-isporcheno-serdce.mdx",
    "src/content/articles/novoe-serdce.mdx",
    "src/content/articles/serdce-hrista-k-nemoshchnym.mdx",
    "src/content/articles/skrytye-idoly-serdca.mdx",
]
EXPECTED_DETECTED = {
    "ownerSurfaces": 1,
    "sourceHeadings": 0,
    "scriptureReferences": 142,
    "externalLinks": 0,
    "internalArticleLinks": 4,
    "quotationSurfaces": 98,
}
EXPECTED_EFFECTIVE = {
    "finalBookEntries": 18,
    "assembledReader": 7,
    "missingStandaloneFinalReaders": 11,
    "entryCitationPassComplete": 7,
    "entryCitationPassOpen": 11,
    "assembledReaderCitationReviewsComplete": 7,
    "productSourceOnly": 5,
    "researchDossierOnly": 6,
    "newDirectQuotesApproved": 0,
}
errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value if isinstance(value, dict) else {}


def blob(root: Path, path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_sha(value: Any) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def long_sentences(text: str, minimum: int = 120) -> set[str]:
    plain = normalize(text)
    return {segment.strip() for segment in re.split(r"(?<=[.!?])\s+", plain) if len(segment.strip()) >= minimum}


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_surface_manifest(product_text: str, builder: Any) -> tuple[list[dict[str, Any]], dict[str, dict[str, int]]]:
    section_starts = [(m.start(), m.group(1)) for m in re.finditer(r'<h2\s+id="([^"]+)"', product_text)]

    def section_for(offset: int) -> str:
        current = "frontmatter-or-introduction"
        for start, section_id in section_starts:
            if start > offset:
                break
            current = section_id
        return current

    def nearby_refs(start: int, end: int) -> list[str]:
        left = max(0, start - 220)
        right = min(len(product_text), end + 220)
        return sorted(
            {builder.normalize_ref(m.group(0)) for m in builder.SCRIPTURE_RE.finditer(product_text[left:right])},
            key=str.casefold,
        )

    surfaces: list[dict[str, Any]] = []
    for surface_type, pattern in (
        ("RUSSIAN_GUILLEMETS", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY_QUOTES", re.compile(r"“([^”\n]{8,})”")),
    ):
        for match in pattern.finditer(product_text):
            value = normalize(match.group(1))
            surfaces.append({
                "type": surface_type,
                "sectionId": section_for(match.start()),
                "sha256": sha(value),
                "characters": len(value),
                "nearbyScriptureReferences": nearby_refs(match.start(), match.end()),
            })
    for match in re.finditer(r"(?m)^\s*>\s?(\S.*)$", product_text):
        value = normalize(match.group(1))
        surfaces.append({
            "type": "MARKDOWN_BLOCKQUOTE",
            "sectionId": section_for(match.start()),
            "sha256": sha(value),
            "characters": len(value),
            "nearbyScriptureReferences": nearby_refs(match.start(), match.end()),
        })
    for match in re.finditer(r"<blockquote[^>]*>(.*?)</blockquote>", product_text, flags=re.S | re.I):
        value = normalize(match.group(1))
        surfaces.append({
            "type": "HTML_BLOCKQUOTE",
            "sectionId": section_for(match.start()),
            "sha256": sha(value),
            "characters": len(value),
            "nearbyScriptureReferences": nearby_refs(match.start(), match.end()),
        })
    surfaces.sort(key=lambda row: (row["sectionId"], row["type"], row["sha256"]))
    section_summary: dict[str, dict[str, int]] = {}
    for row in surfaces:
        bucket = section_summary.setdefault(row["sectionId"], {"surfaces": 0, "withNearbyScripture": 0})
        bucket["surfaces"] += 1
        bucket["withNearbyScripture"] += int(bool(row["nearbyScriptureReferences"]))
    return surfaces, section_summary


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
product_file = product_root / PRODUCT_PATH
require(product_root.is_dir(), "exact Product checkout missing")
for path, expected in BLOBS.items():
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(ROOT, path.relative_to(ROOT)) == expected, f"immutable Research blob drift: {path.relative_to(ROOT)}")
require(product_file.is_file(), "I.1 Product source missing")
if product_file.is_file():
    require(blob(product_root, PRODUCT_PATH) == PRODUCT_BLOB, "I.1 Product blob drift")

product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
require(sha(product_text) == PRODUCT_SHA, "I.1 Product SHA drift")
builder = import_builder()
full_scan = builder.scan_owner(builder.p(str(PRODUCT_PATH), "historical full I.1 owner"), product_root) if builder is not None else {}
reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "I.1 assembled reader"), product_root) if builder is not None else {}
require(len(full_scan.get("scriptureReferences", [])) == 142, "I.1 Product reference count drift")
require(full_scan.get("inlineQuotationSegments") == 98, "I.1 Product quotation count drift")
require(full_scan.get("markdownBlockquotes") == 0 and full_scan.get("htmlBlockquotes") == 0, "I.1 unexpected Product blockquote surfaces")
require(full_scan.get("externalLinks") == [], "I.1 Product external links introduced")
require(full_scan.get("internalArticleLinks") == EXPECTED_LINKS, "I.1 Product internal-link set drift")
require(canonical_sha(sorted(full_scan.get("scriptureReferences", []))) == REFERENCE_SET_SHA, "I.1 Product reference-set hash drift")

surfaces, section_summary = build_surface_manifest(product_text, builder)
require(len(surfaces) == 98, "I.1 quotation extraction drift")
require(canonical_sha(surfaces) == MANIFEST_SHA, "I.1 quotation manifest hash drift")
require(canonical_sha(section_summary) == SECTION_SUMMARY_SHA, "I.1 section/proximity summary drift")
all_hashes = [row["sha256"] for row in surfaces]
require(len(all_hashes) == 98 and len(set(all_hashes)) == 97, "I.1 expected one duplicate quotation occurrence")

receipt = read_json(RECEIPT)
full = receipt.get("fullOwnerReview", {})
class_sets = full.get("surfaceClassHashSets", {})
require(canonical_sha(class_sets) == CLASS_MAP_SHA, "I.1 semantic class-map hash drift")
flat_classes = [surface_hash for values in class_sets.values() for surface_hash in values]
require(len(flat_classes) == 97 and len(set(flat_classes)) == 97, "I.1 class taxonomy must contain 97 unique hashes")
require(set(flat_classes) == set(all_hashes), "I.1 class taxonomy does not cover all Product quotation hashes")
class_counts = {name: sum(1 for item in all_hashes if item in set(values)) for name, values in sorted(class_sets.items())}
require(class_counts == EXPECTED_COUNTS, "I.1 quotation class count drift")
require(full.get("quotationClassCounts") == EXPECTED_COUNTS, "I.1 receipt class counts drift")
require(full.get("duplicateSurfaceHashes") == {"902767037a7756eb98484200bafeacc72b34061008afe674b42c1fabae593b59": 2}, "I.1 duplicate-surface receipt drift")
require(full.get("sectionSummary") == section_summary, "I.1 receipt section summary drift")
require(full.get("scriptureReferenceSetSha256") == REFERENCE_SET_SHA, "I.1 receipt reference-set hash drift")
require(full.get("quotationSurfaceManifestSha256") == MANIFEST_SHA, "I.1 receipt manifest hash drift")
require(full.get("classificationMapSha256") == CLASS_MAP_SHA, "I.1 receipt class-map hash drift")
require(full.get("sectionSummarySha256") == SECTION_SUMMARY_SHA, "I.1 receipt section-summary hash drift")
require(full.get("internalArticleLinks") == EXPECTED_LINKS, "I.1 receipt internal-link set drift")
require(full.get("internalTargetFiles") == EXPECTED_TARGETS, "I.1 receipt target-file set drift")
require(full.get("sourceMarkers") == {"synodalDeclaration": True, "sourcesSection": True, "accuracyNotice": True}, "I.1 receipt source-marker drift")
for marker in (
    "Все библейские цитаты — по Синодальному переводу",
    '<h2 id="istochniki">',
    "Нашли неточность?",
):
    require(marker in product_text, f"I.1 Product source marker missing: {marker}")
for target in EXPECTED_TARGETS:
    require((product_root / target).is_file(), f"I.1 Product internal target missing: {target}")

require(len(reader_scan.get("scriptureReferences", [])) == 20, "I.1 reader reference count drift")
require(canonical_sha(sorted(reader_scan.get("scriptureReferences", []))) == READER_REFERENCE_SET_SHA, "I.1 reader reference-set hash drift")
for key in ("externalLinks", "internalArticleLinks"):
    require(reader_scan.get(key) == [], f"I.1 reader {key} must remain absent")
for key in ("footnoteDefinitions", "markdownBlockquotes", "htmlBlockquotes", "inlineQuotationSegments"):
    require(reader_scan.get(key) == 0, f"I.1 reader {key} must remain zero")
require(long_sentences(product_text).isdisjoint(long_sentences(reader_text)), "I.1 reader contains a long exact Product sentence")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-I1-READER-ASSEMBLY-2026-08-04", "I.1 assembly authority drift")
require(assembly.get("reader", {}).get("gitBlob") == BLOBS[READER], "I.1 assembly reader blob drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 6, "I.1 assembly citation baseline drift")
require(assembly.get("effectiveCounts", {}).get("assembledReader") == 7, "I.1 assembly reader count drift")
current = read_json(CURRENT_V3)
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V3-2026-08-04", "current V3 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 6, "current V3 citation count drift")
require("HEART-BOOK-I1" in current.get("openEntryIds", []), "I.1 absent from historical open set")
triage = read_json(TRIAGE)
rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-I1"]
require(len(rows) == 1, "historical I.1 triage row missing")
if rows:
    require(rows[0].get("detected") == EXPECTED_DETECTED, "historical I.1 row drift")
    require(rows[0].get("disposition", {}).get("entryCitationPassComplete") is False, "historical triage was rewritten")

require(receipt.get("authorityId") == "HEART-I1-CITATION-REVIEW-2026-08-04", "I.1 citation receipt authority drift")
require(receipt.get("status") == "I1_ENTRY_CITATION_PASS_COMPLETE_SEVEN_ASSEMBLED_READERS_REVIEWED_WHOLE_BOOK_OPEN", "I.1 citation receipt status drift")
require(receipt.get("fullOwnerReview", {}).get("detected") == EXPECTED_DETECTED, "I.1 receipt detected counts drift")
require(receipt.get("readerReview", {}).get("scriptureReferences") == 20, "I.1 receipt reader count drift")
require(receipt.get("readerReview", {}).get("quotationSurfaces") == 0, "I.1 receipt reader quotation drift")
require(receipt.get("disposition", {}).get("newDirectQuotesApproved") == 0, "I.1 receipt direct-quote boundary drift")
require(receipt.get("effectiveCounts") == EXPECTED_EFFECTIVE, "I.1 receipt effective-count drift")
boundary = receipt.get("publicationBoundary", {})
require(boundary.get("i1EntryCitationPassComplete") is True, "I.1 citation pass not complete")
require(boundary.get("allCurrentlyAssembledReadersCitationReviewed") is True, "I.1 assembled-reader reviews not complete")
for key in (
    "wholeBookReaderAssemblyComplete",
    "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete",
    "wholeBookLineEditComplete",
    "manuscriptBundleComplete",
    "productReleaseComplete",
):
    require(boundary.get(key) is False, f"I.1 falsely closes {key}")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-I1-CITATION-REVIEW-2026-08-04",
    "I.1 ENTRY CITATION PASS = COMPLETE",
    "ENTRY CITATION PASSES COMPLETE = 7 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 7 / 7",
    "PRODUCT SCRIPTURE REFERENCES GOVERNED = 142 / 142",
    "PRODUCT QUOTATION SURFACES CLASSIFIED = 98 / 98",
    "SCRIPTURE DIRECT / RUSSIAN SYNODAL = 69",
    "EDITORIAL / COLLOQUIAL = 18",
    "LEXICAL / TRANSLATION = 5",
    "TITLE / LINK LABEL = 6",
    "INTERNAL TARGETS RESOLVED = 4 / 4",
    "READER SCRIPTURE LOCATORS = 20",
    "READER QUOTATION / LINK SURFACES = 0",
    "NEW DIRECT QUOTES APPROVED = 0",
    "BULK DIRECT-QUOTE APPROVAL = FORBIDDEN",
    MANIFEST_SHA,
    BLOBS[READER],
    PRODUCT_BLOB,
):
    require(marker in human, f"I.1 human authority marker missing: {marker}")
for forbidden in (
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"I.1 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.1 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart I.1 entry citation pass: PASS — 142 references, 98 surfaces (69 Scripture / 18 editorial / 5 lexical / 6 titles), 4 internal targets, reader 20/0/0, whole-book 7/18")
