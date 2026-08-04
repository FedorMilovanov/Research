#!/usr/bin/env python3
"""Validate the bounded Part IV Heart-and-Word standalone reader assembly."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
SOURCE = ROOT / "СЕРИЯ СЕРДЦЕ/68_R7A_WORD_AND_HEART.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/129_READER_CHAPTER_IV_HEART_AND_WORD_2026-08-04.md"
RECEIPT = ROOT / "data/heart-part4-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v9-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/130_PART4_READER_ASSEMBLY_2026-08-04.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
EXPECTED_BLOBS = {
    SOURCE: "ceff41072982c664606bc377ef8f1f0f241677da",
    READER: "55eda03de3cc29e7946a705fe0fffbd2acc4e36d",
    CURRENT: "d8a65b5233a471e024f5642e1dc3d1a50f13babf",
    INTEGRATION: "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
EXPECTED_SOURCE_SHA = "420e5fd82739edcd77258440125fa65dd4a6c8cf36e5377e32a3c2e143285089"
EXPECTED_READER_SHA = "b3a103936c9495484a2a5478262ec4d4e47ab49f5192dd523add1deeb7d23d58"
EXPECTED_SOURCE_HASHES = {
    "scriptureReferenceSetSha256": "f7539fc92fd79dc29d4ba97bad1e43a173cf6d77a77006ea1a77a08059224b3a",
    "externalLinkSetSha256": "452a0db94764d231a3f8798368c71d624c98fae30825a94e68c98b4f168b4219",
    "internalArticleLinkSetSha256": "26f4a242663e5d878d4b09e33890abddf605a0cbcdda9c653c1e41cd6849c0d3",
    "headingManifestSha256": "a850b5b16e4c776d6991d93e4ab08cef46ee9c72cd5c52df85539997db77d5d1",
    "sectionSummarySha256": "2491e864a4d0eb19946dfe294b525644108448e39a96e2e49bd95aa49ffc2675",
}
EXPECTED_READER_REF_HASH = "56bbb6e030f13cd370efd794cc76f19c59a70d5fb76abbabd5a8167f989f8f75"
EXPECTED_READER_HEADINGS = [
    "IV. Сердце и Слово Божие",
    "Одно слышание и два исхода",
    "Принять насаждённое слово",
    "Зеркало, в котором нельзя задержаться на мгновение",
    "Пища для сердца",
    "Размышление не опустошает ум",
    "Не Слово вместо Духа и не Дух без Слова",
    "Освящение истиной",
    "Пребывание, которое ведёт к свободе",
    "Услышать, принять и жить",
]
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "assembledReaders": 13,
    "missingStandaloneFinalReaders": 5,
    "entryCitationPassComplete": 12,
    "entryCitationPassOpen": 6,
    "assembledReaderCitationReviewsComplete": 12,
    "assembledReadersAwaitingCitationReview": 1,
    "productSourceOnlyEntries": 2,
    "researchDossierOnlyEntries": 3,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 46,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
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
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be an object")
    return value if isinstance(value, dict) else {}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_sha(value: Any, *, sort_keys: bool = False) -> str:
    return text_sha(json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys))


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
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", source_clean)
        if len(sentence.strip()) >= 110 and sentence.strip() in reader_clean
    ]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")

receipt = read_json(RECEIPT)
current = read_json(CURRENT)
integration = read_json(INTEGRATION)
source_text = SOURCE.read_text(encoding="utf-8") if SOURCE.is_file() else ""
reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
require(text_sha(source_text) == EXPECTED_SOURCE_SHA, "Part IV source SHA drift")
require(text_sha(reader_text) == EXPECTED_READER_SHA, "Part IV reader SHA drift")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source_scan = module.scan_owner(module.r(str(SOURCE.relative_to(ROOT)), "Part IV R7a owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part IV reader"), product_root)
source_refs = sorted(source_scan["scriptureReferences"], key=str.casefold)
source_urls = sorted(source_scan["externalLinks"], key=str.casefold)
source_internal = sorted(source_scan["internalArticleLinks"], key=str.casefold)
source_headings = [{"level": row["level"], "title": row["title"]} for row in headings(source_text)]
source_sections = section_summary(source_text, module)
reader_refs = sorted(reader_scan["scriptureReferences"], key=str.casefold)
reader_words = len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b", reader_text))
reader_heading_titles = [row["title"] for row in headings(reader_text)]
transfers = long_exact_transfers(source_text, reader_text)

require(len(source_refs) == 65, "Part IV source Scripture count drift")
require(qcount(source_scan) == 225, "Part IV source quotation count drift")
require(len(source_urls) == 36, "Part IV source external-link count drift")
require(len(source_internal) == 2, "Part IV source internal-path count drift")
require(source_scan["footnoteDefinitions"] == 0, "Part IV source footnote count drift")
require(source_scan["sourceHeadings"] == [], "Part IV source heading classification drift")
require(json_sha(source_refs) == EXPECTED_SOURCE_HASHES["scriptureReferenceSetSha256"], "Part IV source Scripture set hash drift")
require(json_sha(source_urls) == EXPECTED_SOURCE_HASHES["externalLinkSetSha256"], "Part IV source URL set hash drift")
require(json_sha(source_internal) == EXPECTED_SOURCE_HASHES["internalArticleLinkSetSha256"], "Part IV source internal set hash drift")
require(json_sha(source_headings) == EXPECTED_SOURCE_HASHES["headingManifestSha256"], "Part IV source heading manifest drift")
require(json_sha(source_sections, sort_keys=True) == EXPECTED_SOURCE_HASHES["sectionSummarySha256"], "Part IV source section summary drift")

require(reader_words == 1580, "Part IV reader word count drift")
require(len(reader_refs) == 18, "Part IV reader Scripture count drift")
require(json_sha(reader_refs) == EXPECTED_READER_REF_HASH, "Part IV reader Scripture set hash drift")
require(qcount(reader_scan) == 0, "Part IV reader quotation surface drift")
require(len(reader_scan["externalLinks"]) == 0, "Part IV reader external-link drift")
require(len(reader_scan["internalArticleLinks"]) == 0, "Part IV reader internal-link drift")
require(reader_scan["footnoteDefinitions"] == 0, "Part IV reader footnote drift")
require(reader_scan["sourceHeadings"] == [], "Part IV reader source-heading drift")
require(reader_heading_titles == EXPECTED_READER_HEADINGS, "Part IV reader heading order drift")
require(transfers == [], "Part IV reader contains long exact source transfer")
for forbidden in (
    "Without the Holy Spirit we may as well burn our Bibles", "Менахема-Мендла", "Коцк",
    "Owen", "Оуэн", "семь шагов", "7 шагов",
):
    require(forbidden not in reader_text, f"Part IV reader contains forbidden transfer/attribution: {forbidden}")
for required in (
    "Евр. 4:2", "1 Фес. 2:13", "Иак. 1:21", "Иак. 1:22–25", "Ин. 17:17",
    "Пс. 1", "Пс. 118", "1 Пет. 2:2", "Кол. 3:16", "Еф. 5:18–20",
    "Лк. 24", "2 Тим. 3:16–17", "Ин. 8:31–32",
):
    require(required in reader_text, f"Part IV reader missing required canonical anchor: {required}")

entry = next((row for row in integration.get("entries", []) if row.get("id") == "HEART-BOOK-IV"), {})
require(entry.get("order") == 10, "Part IV integration order drift")
require(entry.get("bookLabel") == "IV Сердце и слово Божие", "Part IV integration label drift")
require(entry.get("primaryState") == "RESEARCH_DOSSIER_ONLY", "Part IV integration source state drift")
require(entry.get("productOwner") is None, "Part IV integration Product owner drift")
require(entry.get("researchOwners") == [str(SOURCE.relative_to(ROOT))], "Part IV integration owner drift")
require(entry.get("dedupOwner") == "Owns Scripture reception, illumination and the heart; forbidden Owen and Kotzker attributions remain excluded.", "Part IV integration dedup boundary drift")

require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V9-2026-08-04", "current V9 authority drift")
require(current.get("currentCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 12,
    "entryCitationPassOpen": 6,
    "assembledReaderEntries": 12,
    "assembledReaderCitationReviewsComplete": 12,
    "missingStandaloneFinalReaders": 6,
    "productSourceOnlyEntries": 2,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 46,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "current V9 count block drift")
require(current.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-IV", "V9 next-entry drift")

require(receipt.get("schemaVersion") == 1, "Part IV receipt schema drift")
require(receipt.get("authorityId") == "HEART-PART4-READER-ASSEMBLY-2026-08-04", "Part IV receipt authority drift")
require(receipt.get("status") == "PART4_STANDALONE_READER_ASSEMBLED_CITATION_PASS_OPEN", "Part IV receipt status drift")
require(receipt.get("entry") == {
    "order": 10,
    "id": "HEART-BOOK-IV",
    "label": "IV Сердце и слово Божие",
    "previousState": "RESEARCH_DOSSIER_ONLY",
    "currentState": "ASSEMBLED_READER_CITATION_OPEN",
    "dedupOwner": "Owns Scripture reception, illumination and the heart; forbidden Owen and Kotzker attributions remain excluded.",
}, "Part IV receipt entry block drift")
source_receipt = receipt.get("sourceOwner", {})
require(source_receipt.get("path") == str(SOURCE.relative_to(ROOT)), "Part IV receipt source path drift")
require(source_receipt.get("gitBlob") == EXPECTED_BLOBS[SOURCE], "Part IV receipt source blob drift")
require(source_receipt.get("fullSha256") == EXPECTED_SOURCE_SHA, "Part IV receipt source SHA drift")
require(source_receipt.get("historicalSurface") == {
    "scriptureReferences": 65,
    "quotationSurfaces": 225,
    "externalLinks": 36,
    "internalArticleLinks": 2,
    "footnoteDefinitions": 0,
    "sourceHeadings": 0,
}, "Part IV receipt source counts drift")
require(source_receipt.get("manifestHashes") == EXPECTED_SOURCE_HASHES, "Part IV receipt source hashes drift")
for key in (
    "allHistoricalQuotationSurfacesRemainOutsideReader", "allHistoricalLinksRemainOutsideReader",
    "hebrews4VariantNotUsedAsSoleDoctrinalBasis", "owenBurnBiblesAttributionExcluded",
    "kotzkerAttributionExcluded", "part8BeholdingGloryOwnershipRetained", "citationAndLinkDispositionDeferred",
):
    require(source_receipt.get("assemblyBoundary", {}).get(key) is True, f"Part IV source boundary drift: {key}")
require(receipt.get("reader") == {
    "path": str(READER.relative_to(ROOT)),
    "gitBlob": EXPECTED_BLOBS[READER],
    "fullSha256": EXPECTED_READER_SHA,
    "words": 1580,
    "scriptureReferences": 18,
    "scriptureReferenceSetSha256": EXPECTED_READER_REF_HASH,
    "quotationSurfaces": 0,
    "externalLinks": 0,
    "internalArticleLinks": 0,
    "footnoteDefinitions": 0,
    "sourceHeadings": 0,
    "longExactSentenceTransfers": 0,
    "sourceQuotationTransfer": 0,
    "sourceLinkTransfer": 0,
    "newDirectQuotesApproved": 0,
}, "Part IV receipt reader block drift")
require(receipt.get("effectiveCounts") == EXPECTED_COUNTS, "Part IV effective count block drift")
publication = receipt.get("publicationBoundary", {})
require(publication.get("part4ReaderAssemblyComplete") is True, "Part IV assembly not complete")
for key in (
    "part4EntryCitationPassComplete", "allCurrentlyAssembledReadersReviewed",
    "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete",
    "manuscriptBundleComplete", "productReleaseComplete", "productSourceRepairsComplete",
    "dossierUrlHoldsResolved", "dossierSourceUrlRepairsComplete", "unresolvedInternalPathsResolved",
):
    require(publication.get(key) is False, f"Part IV receipt falsely closes {key}")
require(receipt.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-IV", "Part IV next transaction drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-PART4-READER-ASSEMBLY-2026-08-04",
    "SOURCE SCRIPTURE REFERENCES = 65", "SOURCE QUOTATION SURFACES = 225",
    "SOURCE EXTERNAL LINKS = 36", "SOURCE INTERNAL PATH DETECTIONS = 2",
    "READER WORDS = 1580", "READER SCRIPTURE REFERENCES = 18",
    "READER QUOTATION SURFACES = 0", "READER LINKS = 0",
    "ASSEMBLED READERS = 13 / 18", "ENTRY CITATION PASSES COMPLETE = 12 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 12 / 13",
    "NEXT TRANSACTION = HEART-BOOK-IV ENTRY CITATION PASS",
    EXPECTED_BLOBS[SOURCE], EXPECTED_BLOBS[READER], EXPECTED_BLOBS[CURRENT],
):
    require(marker in human, f"Part IV human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 13 / 18", "ASSEMBLED READER CITATION REVIEWS = 13 / 13",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE", "WHOLE-BOOK CITATION PASS = COMPLETE",
    "PRODUCT RELEASE = COMPLETE", "TODO", "TBD",
):
    require(forbidden not in human, f"Part IV human authority contains forbidden marker: {forbidden}")
workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
require("validate_heart_part4_reader_assembly.py" in workflow, "Part IV permanent workflow gate missing")

if errors:
    print(f"Heart Part IV reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart Part IV reader assembly: PASS — source 65/225/36/2, reader 1580/18/0/0, readers 13/18, reviews 12/13, citation pass open")
