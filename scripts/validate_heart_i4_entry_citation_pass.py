#!/usr/bin/env python3
"""Validate the completed I.4 entry citation pass."""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
REVIEW = ROOT / "data/heart-i4-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-i4-reader-assembly-2026-08-04.json"
OWNER = ROOT / "data/heart-i4-owner-closure-2026-08-04.json"
CURRENT_V2 = ROOT / "data/heart-entry-citation-pass-current-v2-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/101_READER_CHAPTER_I4_INNER_PERSON_EMBODIED_LIFE_2026-08-04.md"
V81 = ROOT / "СЕРИЯ СЕРДЦЕ/60_V81_JAY_ADAMS_PRIMARY_SOURCE_DEEPENING.md"
V82 = ROOT / "СЕРИЯ СЕРДЦЕ/61_V82_PSYCHOTROPIC_MEDICATION_BODY_SOUL_BIBLICAL_COUNSELING.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/103_I4_CITATION_REVIEW_2026-08-04.md"
PRIMARY = Path("src/content/articles/serdce-i-telo.mdx")
SUPPORT = Path("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx")

RESEARCH_BLOBS = {
    READER: "d683ed3f1e8d699f0232f9ee7a30dc0fa2400d74",
    ASSEMBLY: "83c535047dbc8bb9f19676d539e04a5e700e43ab",
    OWNER: "5a7aa3ef29571255708c49692a6232177b7bcf14",
    CURRENT_V2: "66d2f46cf639d9825b5b09fc4e94111be3af2a11",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    V81: "f5b3491acad2e6a68197d6c1191ea3b9fb74aa75",
    V82: "d62d76abe607335861745cc732a9aad8edc3b743",
}
PRODUCT_BLOBS = {
    PRIMARY: "dca5863c614cf3a4f8503d52a79bb76e705c9d2c",
    SUPPORT: "acc12804f5b2450efebbb6e0b2cabd31066ef48c",
}
EXPECTED_DOMAINS_V82 = {
    "biblicalcounseling.com", "blog.tms.edu", "blogs.faithlafayette.org", "ibcd.org",
    "newgrowthpress.com", "store.faithlafayette.org", "tms.edu",
    "www.biblicalcounselingcoalition.org", "www.ccef.org", "www.faithlafayette.org",
    "www.fda.gov", "www.gov.uk", "www.gracechurch.org", "www.nice.org.uk", "www.rcpsych.ac.uk",
}
PRODUCT_CONTEXT_LINKS = {
    "/articles/serdce-i-iskushenie/",
    "/articles/serdce-i-yazyk/",
    "/articles/skrytye-idoly-serdca/",
    "/articles/starye-dorozhki-serdca/",
    "/articles/krajne-li-isporcheno-serdce/",
    "/articles/novoe-serdce/",
    "/articles/serdce-hrista-k-nemoshchnym/",
}
V82_FALSE_POSITIVE = "/articles/who-is-saying-medicine-is-unimportant/"
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


def git_blob(root: Path, path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
require(product_root.is_dir(), "exact Product checkout missing")

for path, expected_blob in RESEARCH_BLOBS.items():
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(ROOT, path.relative_to(ROOT)) == expected_blob, f"immutable Research blob drift: {path.relative_to(ROOT)}")
for path, expected_blob in PRODUCT_BLOBS.items():
    require((product_root / path).is_file(), f"immutable Product source missing: {path}")
    if (product_root / path).is_file():
        require(git_blob(product_root, path) == expected_blob, f"immutable Product blob drift: {path}")

builder = import_builder()
owner_specs = [
    builder.p(str(PRIMARY), "primary Product body-life source"),
    builder.p(str(SUPPORT), "supporting Product whole-person source"),
    builder.r(str(V81.relative_to(ROOT)), "V81 habit and inner-person boundary"),
    builder.r(str(V82.relative_to(ROOT)), "V82 body-soul and competence boundary"),
] if builder is not None else []
scans = [builder.scan_owner(owner, product_root) for owner in owner_specs] if builder is not None else []
reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "assembled I.4 reader"), product_root) if builder is not None else {}
scan_by_path = {scan.get("path"): scan for scan in scans}

expected_owner_counts = {
    str(PRIMARY): (17, 0, 4, 64, 0),
    str(SUPPORT): (142, 0, 4, 98, 0),
    str(V81.relative_to(ROOT)): (12, 31, 0, 23, 1),
    str(V82.relative_to(ROOT)): (1, 66, 1, 31, 2),
}
for path, (refs, external, internal, quotes, headings) in expected_owner_counts.items():
    scan = scan_by_path.get(path, {})
    require(len(scan.get("scriptureReferences", [])) == refs, f"I.4 owner Scripture count drift: {path}")
    require(len(scan.get("externalLinks", [])) == external, f"I.4 owner external-link count drift: {path}")
    require(len(scan.get("internalArticleLinks", [])) == internal, f"I.4 owner internal-link count drift: {path}")
    require(scan.get("inlineQuotationSegments", 0) + scan.get("markdownBlockquotes", 0) + scan.get("htmlBlockquotes", 0) == quotes, f"I.4 owner quotation count drift: {path}")
    require(len(scan.get("sourceHeadings", [])) == headings, f"I.4 owner source-heading count drift: {path}")

all_refs = {ref for scan in scans for ref in scan.get("scriptureReferences", [])}
all_external = {url for scan in scans for url in scan.get("externalLinks", [])}
all_internal = {url for scan in scans for url in scan.get("internalArticleLinks", [])}
all_quotes = sum(scan.get("inlineQuotationSegments", 0) + scan.get("markdownBlockquotes", 0) + scan.get("htmlBlockquotes", 0) for scan in scans)
all_headings = sum(len(scan.get("sourceHeadings", [])) for scan in scans)
require(len(scans) == 4, "I.4 historical owner-surface count drift")
require(len(all_refs) == 171, "I.4 historical aggregate Scripture count drift")
require(len(all_external) == 97, "I.4 historical aggregate external-link count drift")
require(len(all_internal) == 8, "I.4 historical aggregate internal-link count drift")
require(all_quotes == 216, "I.4 historical aggregate quotation count drift")
require(all_headings == 3, "I.4 historical aggregate source-heading count drift")

require(len(reader_scan.get("scriptureReferences", [])) == 9, "I.4 reader Scripture count drift")
require(set(reader_scan.get("scriptureReferences", [])).issubset(all_refs), "I.4 reader references are not a subset of governed evidence")
require(reader_scan.get("externalLinks") == [], "I.4 reader external links must remain absent")
require(reader_scan.get("internalArticleLinks") == [], "I.4 reader internal links must remain absent")
require(reader_scan.get("inlineQuotationSegments") == 0, "I.4 reader inline quotations must remain absent")
require(reader_scan.get("markdownBlockquotes") == 0, "I.4 reader Markdown blockquotes must remain absent")
require(reader_scan.get("htmlBlockquotes") == 0, "I.4 reader HTML blockquotes must remain absent")
require(reader_scan.get("footnoteDefinitions") == 0, "I.4 reader footnotes must remain absent")

primary_text = (product_root / PRIMARY).read_text(encoding="utf-8")
support_text = (product_root / SUPPORT).read_text(encoding="utf-8")
v81_text = V81.read_text(encoding="utf-8")
v82_text = V82.read_text(encoding="utf-8")
for text, label in ((primary_text, "primary Product"), (support_text, "support Product")):
    require("Все библейские цитаты — по Синодальному переводу" in text, f"{label} Synodal declaration missing")
for marker in (
    "P1 — VERIFIED PRIMARY TEXT",
    "P1-C — VERIFIED, CAUTION",
    "P2 — OFFICIAL BOOK PAGE",
    "PAGE-IMAGE HOLD",
    "Политика цитат",
):
    require(marker in v81_text, f"V81 source-governance marker missing: {marker}")
for marker in (
    "### GREEN — можно внедрять",
    "### YELLOW — только с оговоркой и современной проверкой",
    "### RED — не внедрять",
    "# 10. КОНСЕРВАТИВНЫЙ ХРИСТИАНСКИЙ SOURCE LEDGER — 56 РЕСУРСОВ",
    "## 12. Source hierarchy for publication",
    "`C1-PDF`",
    "`C2`",
    "`C3`",
    "`CAUTION`",
):
    require(marker in v82_text, f"V82 source-governance marker missing: {marker}")

v81_scan = scan_by_path.get(str(V81.relative_to(ROOT)), {})
v82_scan = scan_by_path.get(str(V82.relative_to(ROOT)), {})
require({urlparse(url).netloc for url in v81_scan.get("externalLinks", [])} == {"nouthetic.org"}, "V81 domain set drift")
require({urlparse(url).netloc for url in v82_scan.get("externalLinks", [])} == EXPECTED_DOMAINS_V82, "V82 domain set drift")
product_internal = set(scan_by_path.get(str(PRIMARY), {}).get("internalArticleLinks", [])) | set(scan_by_path.get(str(SUPPORT), {}).get("internalArticleLinks", []))
require(product_internal == PRODUCT_CONTEXT_LINKS, "I.4 Product context-link set drift")
require(set(v82_scan.get("internalArticleLinks", [])) == {V82_FALSE_POSITIVE}, "I.4 V82 path-token set drift")
require(any(url.endswith(V82_FALSE_POSITIVE) for url in v82_scan.get("externalLinks", [])), "I.4 V82 false-positive token is not part of an external URL")
for link in PRODUCT_CONTEXT_LINKS:
    slug = link.removeprefix("/articles/").removesuffix("/")
    require((product_root / "src/content/articles" / f"{slug}.mdx").is_file(), f"I.4 Product context target missing: {link}")

triage = read_json(TRIAGE)
triage_rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-I4"]
require(len(triage_rows) == 1, "historical I.4 triage row missing")
if triage_rows:
    row = triage_rows[0]
    require(row.get("inventoryEntrySha256") == "96cf828429bc60fd1ba4cec313182f629f17131d2004017e7ff3c88df4a741e0", "I.4 inventory-entry SHA drift")
    require(row.get("detected") == {"ownerSurfaces":4,"sourceHeadings":3,"scriptureReferences":171,"externalLinks":97,"internalArticleLinks":8,"quotationSurfaces":216}, "I.4 historical detected counts drift")
    require(row.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical I.4 triage state rewritten")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-I4-READER-ASSEMBLY-2026-08-04", "I.4 assembly authority drift")
require(assembly.get("status") == "I4_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_ENTRY_CITATION_PASS_OPEN", "I.4 assembly status drift")
require(assembly.get("effectiveState", {}).get("entryCitationPassComplete") is False, "historical I.4 assembly receipt rewritten")
require(assembly.get("publicationBoundary", {}).get("i4EntryCitationPassComplete") is False, "historical I.4 assembly publication state rewritten")

current = read_json(CURRENT_V2)
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V2-2026-08-04", "preceding current V2 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 5, "preceding completion count drift")
require("HEART-BOOK-I4" in current.get("openEntryIds", []), "I.4 missing from preceding open-entry set")

review = read_json(REVIEW)
require(review.get("authorityId") == "HEART-I4-CITATION-REVIEW-2026-08-04", "I.4 review authority drift")
require(review.get("status") == "I4_ENTRY_CITATION_PASS_COMPLETE_SIX_ASSEMBLED_READERS_REVIEWED_WHOLE_BOOK_OPEN", "I.4 review status drift")
require(review.get("entry", {}).get("stateAfter") == "ENTRY_CITATION_PASS_COMPLETE", "I.4 review state transition drift")
immutable = review.get("immutableSources", {})
require(immutable.get("reader", [None, None])[1] == RESEARCH_BLOBS[READER], "I.4 review reader blob drift")
require(immutable.get("readerAssembly", [None, None])[1] == RESEARCH_BLOBS[ASSEMBLY], "I.4 review assembly blob drift")
require(immutable.get("ownerClosure", [None, None])[1] == RESEARCH_BLOBS[OWNER], "I.4 review owner blob drift")
require(immutable.get("precedingCurrentV2", [None, None])[1] == RESEARCH_BLOBS[CURRENT_V2], "I.4 review current V2 blob drift")
require(immutable.get("historicalTriage", [None, None])[1] == RESEARCH_BLOBS[TRIAGE], "I.4 review triage blob drift")
require(immutable.get("primaryProduct", [None, None])[1] == PRODUCT_BLOBS[PRIMARY], "I.4 review primary Product blob drift")
require(immutable.get("supportProduct", [None, None])[1] == PRODUCT_BLOBS[SUPPORT], "I.4 review support Product blob drift")
require(immutable.get("v81", [None, None])[1] == RESEARCH_BLOBS[V81], "I.4 review V81 blob drift")
require(immutable.get("v82", [None, None])[1] == RESEARCH_BLOBS[V82], "I.4 review V82 blob drift")
require(review.get("readerReview") == {
    "detectedScriptureReferences":9,
    "quotationSurfaces":0,
    "externalLinks":0,
    "internalArticleLinks":0,
    "footnoteDefinitions":0,
    "scriptureClassification":"LOCATOR_ONLY_AND_CANONICAL_PARAPHRASE_NO_VERBATIM_TRANSLATION",
    "translationVersionIdentifierRequired":False,
    "historicalOrSourceDirectQuotes":0,
    "newDirectQuotesApproved":0,
    "reviewComplete":True,
}, "I.4 reader review block drift")
historical = review.get("historicalOwnerSurfaceReview", {})
require({key: historical.get(key) for key in ("ownerSurfaces","sourceHeadings","uniqueScriptureReferences","externalLinks","internalArticleLinks","quotationSurfaces")} == {
    "ownerSurfaces":4,"sourceHeadings":3,"uniqueScriptureReferences":171,"externalLinks":97,"internalArticleLinks":8,"quotationSurfaces":216,
}, "I.4 historical review totals drift")
require(review.get("scriptureReview", {}).get("readerReferencesSubsetOfGovernedOwnerReferences") is True, "I.4 reader Scripture subset boundary missing")
require(review.get("quotationReview", {}).get("historicalOwnerQuotationSurfaces") == 216, "I.4 quotation review total drift")
require(review.get("quotationReview", {}).get("reader") == 0, "I.4 reader quotation review drift")
require(review.get("quotationReview", {}).get("newDirectQuotesApproved") == 0, "I.4 direct quote review drift")
require(review.get("quotationReview", {}).get("bulkApprovalOfResearchDossierSurfaces") is False, "I.4 research quote bank falsely bulk-approved")
external_review = review.get("externalLinkReview", {})
require(external_review.get("historicalExternalLinks") == 97, "I.4 external-link review total drift")
require(external_review.get("readerExternalLinks") == 0, "I.4 reader external-link review drift")
require(external_review.get("blockerResolvedForEntryUse") is True, "I.4 external-link blocker unresolved")
internal_review = review.get("internalLinkReview", {})
require(set(internal_review.get("productContextTargets", [])) == PRODUCT_CONTEXT_LINKS, "I.4 receipt Product target set drift")
require(internal_review.get("v82FalsePositiveExternalPathToken") == V82_FALSE_POSITIVE, "I.4 receipt false-positive token drift")
require(internal_review.get("transferredToReader") is False, "I.4 internal links falsely transferred")
disposition = review.get("disposition", {})
require(disposition.get("remainingEntryBlockers") == [], "I.4 citation blockers remain")
require(disposition.get("readerManuscriptChanged") is False, "I.4 reader mutation falsely claimed")
require(disposition.get("productSourcesChanged") is False, "I.4 Product mutation falsely claimed")
require(disposition.get("v81Changed") is False and disposition.get("v82Changed") is False, "I.4 Research boundary mutation falsely claimed")
require(disposition.get("newHistoricalClaims") == 0, "I.4 new historical claim drift")
require(disposition.get("newDirectQuotesApproved") == 0, "I.4 new direct quote drift")
require(disposition.get("entryCitationPassComplete") is True, "I.4 entry citation pass incomplete")
boundary = review.get("wholeBookBoundary", {})
require(boundary.get("entryCitationPassComplete") == "6 / 18", "I.4 whole-book completion count drift")
require(boundary.get("entryCitationPassOpen") == "12 / 18", "I.4 whole-book open count drift")
require(boundary.get("assembledReaderEntries") == "6 / 18", "I.4 assembled-reader count drift")
require(boundary.get("assembledReaderCitationReviewsComplete") == "6 / 6", "I.4 assembled-reader review count drift")
require(boundary.get("missingStandaloneFinalReaders") == 12, "I.4 missing-reader count drift")
require(boundary.get("wholeBookCitationPassComplete") is False, "I.4 falsely closes whole-book citation pass")
require(boundary.get("productReleaseComplete") is False, "I.4 falsely closes Product release")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-I4-CITATION-REVIEW-2026-08-04",
    "I.4 ENTRY CITATION PASS = COMPLETE",
    "ENTRY CITATION PASSES COMPLETE = 6 / 18",
    "ENTRY CITATION PASSES OPEN = 12 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 6 / 6",
    "SCRIPTURE REFERENCES GOVERNED = 171 / 171",
    "QUOTATION SURFACES CLASSIFIED = 216 / 216",
    "EXTERNAL LINKS DISPOSITIONED = 97 / 97",
    "READER DIRECT QUOTES = 0",
    "NEW DIRECT QUOTES APPROVED = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
    RESEARCH_BLOBS[READER],
    RESEARCH_BLOBS[ASSEMBLY],
):
    require(marker in human, f"I.4 human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "RESEARCH DOSSIER SURFACES = BULK APPROVED",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"I.4 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.4 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart I.4 entry citation pass: PASS — "
    "171 Scripture refs, 216 quotation surfaces, 97 support links, "
    "reader 9 locators and 0 quote/link surfaces, whole-book 6/18"
)
