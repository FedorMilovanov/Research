#!/usr/bin/env python3
"""Validate the completed Part II entry citation pass."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
RECEIPT = ROOT / "data/heart-part2-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-part2-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v5-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
SOURCE_CLOSURE = ROOT / "СЕРИЯ СЕРДЦЕ/74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json"
R3 = ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md"
R4 = ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/113_READER_CHAPTER_II_FALLEN_HEART_DIAGNOSIS_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/115_PART2_CITATION_REVIEW_2026-08-04.md"

EXPECTED_BLOBS = {
    ASSEMBLY: "7fe129945caa023e796e592d0c8fc07a01a89f69",
    CURRENT: "2ba8c381e636a9f1148fa30e3f010d595feb42a6",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    SOURCE_CLOSURE: "c67243b7f180bd84c86a0a52b9134844fb221d90",
    R3: "ae55b1fad5cccbdb623c551a14222e0f51ec084a",
    R4: "f82780e13cb064aa89c06427d11a938662fc3ff8",
    READER: "4cca195d034c70a7d3d6c3dd8edc9a04fcffcc20",
}
EXPECTED_ROLE_COUNTS = {
    "EXEGETICAL_SCRIPTURE_OR_LEXICAL_SURFACE": 178,
    "ATTRIBUTED_WITNESS_OR_QUOTE_BANK_SURFACE": 194,
    "EDITORIAL_STRUCTURAL_OR_CAUTION_SURFACE": 65,
}
EXPECTED_URL_STATUS_COUNTS = {
    "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE": 34,
    "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER": 31,
    "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD": 15,
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


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def json_sha(value: Any, *, sort_keys: bool = False) -> str:
    return text_sha(json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys
    ))


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def qcount(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]


def extract_surfaces(text: str, owner: str) -> list[dict[str, Any]]:
    headings = [(m.start(), m.group(2).strip()) for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text)]

    def heading_for(offset: int) -> str:
        current = "frontmatter-or-introduction"
        for start, heading in headings:
            if start > offset:
                break
            current = heading
        return current

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
            rows.append({
                "owner": owner,
                "pos": match.start(),
                "section": heading_for(match.start()),
                "type": surface_type,
                "sha256": text_sha(value),
                "chars": len(value),
            })
    rows.sort(key=lambda row: row["pos"])
    return rows


def contexts_for_url(text: str, url: str) -> list[tuple[str, str]]:
    headings = [(m.start(), m.group(2).strip()) for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text)]

    def heading_for(offset: int) -> str:
        current = "frontmatter-or-introduction"
        for start, heading in headings:
            if start > offset:
                break
            current = heading
        return current

    rows: list[tuple[str, str]] = []
    cursor = 0
    while True:
        offset = text.find(url, cursor)
        if offset < 0:
            break
        left = max(0, offset - 500)
        right = min(len(text), offset + len(url) + 500)
        rows.append((heading_for(offset), normalize(text[left:right])))
        cursor = offset + 1
    return rows


def classify_url(text: str, url: str, method: dict[str, Any]) -> str:
    contexts = contexts_for_url(text, url)
    joined = " ".join(context for _, context in contexts).casefold()
    sections = {section for section, _ in contexts}
    if any(term.casefold() in joined for term in method["holdTerms"]) or any(
        "Открытые вопросы" in section for section in sections
    ):
        return "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
    if any(term.casefold() in joined for term in method["verifiedTerms"]):
        return "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
    return method["fallback"]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")

receipt = read_json(RECEIPT)
assembly = read_json(ASSEMBLY)
current = read_json(CURRENT)
triage = read_json(TRIAGE)
texts = {"R3": R3.read_text(encoding="utf-8"), "R4": R4.read_text(encoding="utf-8")}
reader_text = READER.read_text(encoding="utf-8")

require(text_sha(texts["R3"]) == "12c4344acfc96050eaae35d98ed666102e62c700ead9db34c24681a914102efb", "R3 SHA drift")
require(text_sha(texts["R4"]) == "1e5ff030fea335f64dda3a613898d1237d3a4e34d0c303d67f51a64af92e1964", "R4 SHA drift")
require(text_sha(reader_text) == "c7e37a30651bf96f77f2a2eba204251591edb2ab28aff1cc8332d6c72f99086d", "Part II reader SHA drift")

scans = {
    "R3": module.scan_owner(module.r(str(R3.relative_to(ROOT)), "Part II R3 owner"), product_root),
    "R4": module.scan_owner(module.r(str(R4.relative_to(ROOT)), "Part II R4 owner"), product_root),
}
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part II reader"), product_root)
union_refs = sorted(set(scans["R3"]["scriptureReferences"]) | set(scans["R4"]["scriptureReferences"]), key=str.casefold)
union_urls = {
    "R3": sorted(scans["R3"]["externalLinks"], key=str.casefold),
    "R4": sorted(scans["R4"]["externalLinks"], key=str.casefold),
}
union_internal = sorted(set(scans["R3"]["internalArticleLinks"]) | set(scans["R4"]["internalArticleLinks"]), key=str.casefold)
require(len(union_refs) == 118, "Part II Scripture union count drift")
require(json_sha(union_refs) == "5d78a0e23ed09e10f71dfcf9010269430c53faf2bd6ffe1225a3160ee9ffc4a6", "Part II Scripture set hash drift")
require(qcount(scans["R3"]) + qcount(scans["R4"]) == 437, "Part II quotation count drift")
require(len(union_urls["R3"]) + len(union_urls["R4"]) == 80, "Part II external-link count drift")
require(union_internal == ["/articles/opinion/"], "Part II internal-link set drift")

owner_review = receipt.get("fullOwnerReview", {})
role_map = owner_review.get("roleSectionMap", {})
surfaces = extract_surfaces(texts["R3"], "R3") + extract_surfaces(texts["R4"], "R4")
base_rows = [{key: row[key] for key in ("owner", "section", "type", "sha256", "chars")} for row in surfaces]
require(len(base_rows) == 437, "Part II source surface extraction drift")
require(json_sha(base_rows) == owner_review.get("sourceSurfaceBaseManifestSha256") == "d51a1de91ac865bf81c485797092637ff39d3b50ca59dbbaddec85e9cd2cb804", "Part II base manifest drift")

index_map: dict[str, list[int]] = defaultdict(list)
classified_rows: list[dict[str, Any]] = []
for index, row in enumerate(base_rows):
    owner_roles = role_map.get(row["owner"], {})
    role = "EDITORIAL_STRUCTURAL_OR_CAUTION_SURFACE"
    for candidate in (
        "EXEGETICAL_SCRIPTURE_OR_LEXICAL_SURFACE",
        "ATTRIBUTED_WITNESS_OR_QUOTE_BANK_SURFACE",
    ):
        if row["section"] in owner_roles.get(candidate, []):
            role = candidate
            break
    index_map[role].append(index)
    classified_rows.append({**row, "class": role})
index_map = dict(index_map)
require(Counter(row["class"] for row in classified_rows) == Counter(EXPECTED_ROLE_COUNTS), "Part II quotation role counts drift")
require(json_sha(classified_rows) == owner_review.get("classifiedSurfaceManifestSha256") == "f7cf291e9cecb4a3a9d5aa28ae0185982c54c477448ce3e1b3752501379538cc", "Part II classified manifest drift")
require(json_sha(index_map, sort_keys=True) == owner_review.get("roleMapSha256") == "be48bfb08f60853e858217c3df3a3456dc1b9a7d8235aed394ca5c39f3e65894", "Part II role-map hash drift")

section_summary: dict[str, dict[str, Any]] = {}
for row in classified_rows:
    key = f"{row['owner']}::{row['section']}"
    bucket = section_summary.setdefault(key, {"surfaces": 0, "classes": Counter()})
    bucket["surfaces"] += 1
    bucket["classes"][row["class"]] += 1
section_summary = {
    key: {"surfaces": value["surfaces"], "classes": dict(sorted(value["classes"].items()))}
    for key, value in section_summary.items()
}
require(json_sha(section_summary, sort_keys=True) == owner_review.get("sectionSummarySha256") == "b0932037fbc01a403aa22347d2c3065b6115a1513b3747a4b46fdeb926e6adf7", "Part II section-summary hash drift")
require(owner_review.get("allScriptureReferenceTokensGoverned") is True, "Part II Scripture governance flag drift")
require(owner_review.get("allQuotationSurfacesClassified") is True, "Part II quotation governance flag drift")
require(owner_review.get("bulkDirectQuotationApproval") is False, "Part II bulk quote approval must remain false")

link_review = receipt.get("externalLinkReview", {})
method = link_review.get("method", {})
registry: list[dict[str, Any]] = []
for owner in ("R3", "R4"):
    for url in union_urls[owner]:
        registry.append({
            "owner": owner,
            "url": url,
            "status": classify_url(texts[owner], url, method),
            "readerTransfer": False,
            "directQuoteBulkApproval": False,
        })
require(len(registry) == 80, "Part II URL disposition count drift")
require(Counter(row["status"] for row in registry) == Counter(EXPECTED_URL_STATUS_COUNTS), "Part II URL status counts drift")
require(json_sha(registry, sort_keys=True) == link_review.get("dispositionRegistrySha256") == "0811af3bd3865bc4dfd36f7d1f62048cdbd85f73c243512eb33410b07bbf8fe1", "Part II URL disposition registry drift")
require(all(row["readerTransfer"] is False and row["directQuoteBulkApproval"] is False for row in registry), "Part II URL transfer/approval drift")

internal = receipt.get("internalLinkReview", {})
require(internal.get("path") == "/articles/opinion/", "Part II internal path drift")
require(internal.get("status") == "UNRESOLVED_GENERIC_PATH_NO_PRODUCT_TARGET_NO_READER_TRANSFER", "Part II internal path status drift")
require(not (product_root / "src/content/articles/opinion.mdx").exists(), "Part II generic path unexpectedly resolves to Product article")
require(internal.get("readerTransfer") is False, "Part II internal path transferred to reader")

for marker in ("SAFE CLOSURE", "НЕ ВЕРИФИЦИРОВАНО", "Открытые вопросы", "NO-DIRECT-QUOTE"):
    require(marker in texts["R3"] or marker in texts["R4"], f"Part II dossier status marker missing: {marker}")
require("CLOSED-AS-NO-DIRECT-QUOTE" in texts["R4"], "R4 no-direct-quote closure marker missing")
require("[НЕ ВЕРИФИЦИРОВАНО — кандидат]" in texts["R4"], "R4 candidate marker missing")

require(len(reader_scan["scriptureReferences"]) == 20, "Part II reader locator count drift")
require(qcount(reader_scan) == 0, "Part II reader quotation surface detected")
require(len(reader_scan["externalLinks"]) == 0 and len(reader_scan["internalArticleLinks"]) == 0, "Part II reader link detected")
require(reader_scan["footnoteDefinitions"] == 0, "Part II reader footnote detected")

require(receipt.get("authorityId") == "HEART-PART2-CITATION-REVIEW-2026-08-04", "Part II receipt authority drift")
require(receipt.get("disposition", {}).get("entryCitationPassComplete") is True, "Part II citation pass incomplete")
require(receipt.get("disposition", {}).get("remainingEntryBlockers") == [], "Part II entry blockers remain")
require(receipt.get("disposition", {}).get("newDirectQuotesApproved") == 0, "Part II new quote boundary drift")
require(receipt.get("sourceStatusBoundary", {}).get("unresolvedSourceCandidatesPromoted") == 0, "Part II candidate promotion drift")
require(receipt.get("effectiveCounts") == {"finalBookEntries":18,"assembledReader":9,"missingStandaloneFinalReaders":9,"entryCitationPassComplete":9,"entryCitationPassOpen":9,"assembledReaderCitationReviewsComplete":9,"productSourceOnly":4,"researchDossierOnly":5,"productSourceLinkRepairsRequired":3,"newDirectQuotesApproved":0}, "Part II effective count block drift")
require(receipt.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(receipt.get("publicationBoundary", {}).get("productReleaseComplete") is False, "Product release falsely closed")
require(receipt.get("publicationBoundary", {}).get("productSourceLinkRepairsComplete") is False, "Product repairs falsely closed")

require(assembly.get("authorityId") == "HEART-PART2-READER-ASSEMBLY-2026-08-04", "Part II assembly authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 8, "preceding V5 count drift")
triage_entry = next((row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-II"), {})
require(triage_entry.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical Part II triage rewritten")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-PART2-CITATION-REVIEW-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 9 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 9 / 9",
    "SCRIPTURE LOCATORS GOVERNED = 118 / 118",
    "QUOTATION SURFACES CLASSIFIED = 437 / 437",
    "EXTERNAL LINKS DISPOSITIONED = 80 / 80",
    "URL HOLDS RETAINED = 15",
    "UNRESOLVED INTERNAL PATHS = 1",
    "PRODUCT SOURCE LINK REPAIRS REQUIRED = 3",
    "NEW DIRECT QUOTES APPROVED = 0",
):
    require(marker in human, f"Part II human authority marker missing: {marker}")
for forbidden in (
    "DIRECT QUOTES APPROVED = 437", "URL HOLDS RETAINED = 0",
    "UNRESOLVED INTERNAL PATHS = 0", "PRODUCT SOURCE LINK REPAIRS REQUIRED = 0",
    "WHOLE-BOOK CITATION PASS = COMPLETE", "PRODUCT RELEASE = COMPLETE", "TODO", "TBD",
):
    require(forbidden not in human, f"Part II human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart Part II entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart Part II entry citation pass: PASS — 118 Scripture locators, 437 role-classified surfaces, 80 URL dispositions, 15 holds, 1 unresolved path, reader 20/0/0, whole-book 9/18")
