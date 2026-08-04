#!/usr/bin/env python3
"""Validate the completed X.3 entry citation pass across all three owner surfaces."""
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
REVIEW = ROOT / "data/heart-x3-citation-review-2026-08-04.json"
X1_REVIEW = ROOT / "data/heart-x1-citation-review-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/88_READER_CHAPTER_X3_CONCLUDING_HOPE_2026-08-04.md"
R9 = ROOT / "СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md"
OWNER_CLOSURE = ROOT / "data/heart-x3-owner-closure-2026-08-04.json"
READER_ASSEMBLY = ROOT / "data/heart-x3-reader-assembly-2026-08-04.json"
SOURCE_REGISTRY = ROOT / "СЕРИЯ СЕРДЦЕ/74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/95_X3_CITATION_REVIEW_2026-08-04.md"
PRODUCT_PATH = Path("src/content/articles/osvobozhdennoe-serdce.mdx")

RESEARCH_BLOBS = {
    READER: "22a8d83700498e6229c5dbbe04366d23cf8859ec",
    R9: "c58d253324e1b4adba19fb7958ccd18a6862452c",
    OWNER_CLOSURE: "c6972b6dab85591d8a4b9ac5a5705ee6b1520513",
    READER_ASSEMBLY: "b8426888b2053ab5be1f18ccd1532513a8fe6cca",
    SOURCE_REGISTRY: "c67243b7f180bd84c86a0a52b9134844fb221d90",
}
PRODUCT_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
EXPECTED_EXTERNAL_LINKS = {
    "https://www.crossway.org/articles/qa-dane-ortlund-answers-your-questions-about-the-heart-of-christ-for-sinners/",
    "https://www.crossway.org/articles/what-it-means-that-god-is-rich-in-mercy/",
    "https://www.gty.org/sermons/66-71/the-glorious-return-of-jesus-christ-part-2",
    "https://www.gty.org/sermons/90-475/the-lords-word-to-his-church-thyatira",
    "https://www.ligonier.org/posts/great-quotes-holiness-god",
    "https://www.spurgeon.org/sermons/among-lions",
    "https://www.spurgeon.org/sermons/an-earnest-warning-against-lukewarmness",
}
EXPECTED_INTERNAL_TOKENS = {
    "/articles/qa-dane-ortlund-answers-your-questions-about-the-heart-of-christ-for-sinners/",
    "/articles/what-it-means-that-god-is-rich-in-mercy/",
}
EXPECTED_PRODUCT_QUOTES = [
    "А я в правде буду взирать на лице Твоё; пробудившись, буду насыщаться образом Твоим",
    "как Он есть",
]
EXPECTED_TRIAGE = {
    "ownerSurfaces": 3,
    "sourceHeadings": 2,
    "scriptureReferences": 115,
    "externalLinks": 7,
    "internalArticleLinks": 2,
    "quotationSurfaces": 209,
}
R9_REQUIRED_STATUS_MARKERS = (
    "ВЕРИФИЦИРОВАНО",
    "ВЕРИФИЦИРОВАНО ЧАСТИЧНО",
    "[НЕ ВЕРИФИЦИРОВАНО — кандидат]",
    "DO-NOT-DIRECT-QUOTE",
    "BOOK-PAGE-HOLD",
    "SAFE CLOSURE",
    "Цитатный банк (сводная таблица источников)",
    "Открытые вопросы",
)
R9_LINK_STATUS_MARKERS = (
    "OFFICIAL-CROSSWAY-ARTICLE/Q&A-VERIFIED / NO-BOOK-PAGE-CLAIM",
    "OFFICIAL-GTY-TRANSCRIPT-VERIFIED",
    "OFFICIAL-LIGONIER-QUOTE-PAGE-VERIFIED / NO-BOOK-PAGE-CLAIM",
    "OFFICIAL-PAGE-READ / CLAIM-NOT-FOUND / DO-NOT-DIRECT-QUOTE",
    "OFFICIAL-SPURGEON-LIBRARY-VERIFIED / SERMON-LOCATOR-LOCKED",
)
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
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        cwd=root,
        text=True,
    ).strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def russian_quote_segments(text: str) -> list[str]:
    return re.findall(r"«([^»\n]{8,})»", text)


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
require(product_root.is_dir(), "exact Product checkout missing")

for path, expected_blob in RESEARCH_BLOBS.items():
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(
            git_blob(ROOT, path.relative_to(ROOT)) == expected_blob,
            f"immutable Research blob drift: {path.relative_to(ROOT)}",
        )
product_file = product_root / PRODUCT_PATH
require(product_file.is_file(), "exact X.3 Product source missing")
if product_file.is_file():
    require(git_blob(product_root, PRODUCT_PATH) == PRODUCT_BLOB, "immutable Product blob drift")

reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
r9_text = R9.read_text(encoding="utf-8") if R9.is_file() else ""
product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
require("**Новые прямые цитаты:** `0`" in reader_text, "X.3 reader zero-direct-quote declaration missing")
require("**Статус:** `ASSEMBLED / PARAPHRASE-ONLY / WHOLE-BOOK LINE EDIT OPEN`" in reader_text, "X.3 reader paraphrase-only boundary drift")
require("NEW DIRECT QUOTES = 0" in reader_text, "X.3 reader final direct-quote boundary missing")
require("WHOLE-BOOK CITATION PASS = OPEN" in reader_text, "X.3 reader whole-book boundary missing")
for marker in R9_REQUIRED_STATUS_MARKERS + R9_LINK_STATUS_MARKERS:
    require(marker in r9_text, f"R9 governance marker missing: {marker}")
for url in EXPECTED_EXTERNAL_LINKS:
    require(url in r9_text, f"R9 expected external URL missing: {url}")

builder = import_builder()
if builder is not None:
    reader_scan = builder.scan_owner(
        builder.r(str(READER.relative_to(ROOT)), "assembled paraphrase-only reader"),
        product_root,
    )
    product_scan = builder.scan_owner(
        builder.p(str(PRODUCT_PATH), "exact Product conclusion source", ["vyhod"]),
        product_root,
    )
    r9_scan = builder.scan_owner(
        builder.r(str(R9.relative_to(ROOT)), "risen-Christ boundary"),
        product_root,
    )
else:
    reader_scan = {}
    product_scan = {}
    r9_scan = {}

require(len(reader_scan.get("scriptureReferences", [])) == 3, "X.3 reader Scripture count drift")
require(len(product_scan.get("scriptureReferences", [])) == 1, "X.3 Product Scripture count drift")
require(len(r9_scan.get("scriptureReferences", [])) == 111, "X.3 R9 Scripture count drift")
all_refs = {
    ref
    for scan in (reader_scan, product_scan, r9_scan)
    for ref in scan.get("scriptureReferences", [])
}
require(len(all_refs) == 115, "X.3 aggregate Scripture count drift")
require(reader_scan.get("externalLinks") == [], "X.3 reader external links must remain absent")
require(product_scan.get("externalLinks") == [], "X.3 Product section external links must remain absent")
require(set(r9_scan.get("externalLinks", [])) == EXPECTED_EXTERNAL_LINKS, "X.3 R9 external-link set drift")
require(reader_scan.get("internalArticleLinks") == [], "X.3 reader internal links must remain absent")
require(product_scan.get("internalArticleLinks") == [], "X.3 Product internal links must remain absent")
require(set(r9_scan.get("internalArticleLinks", [])) == EXPECTED_INTERNAL_TOKENS, "X.3 R9 internal-token set drift")
for scan, name in ((reader_scan, "reader"), (product_scan, "Product"), (r9_scan, "R9")):
    require(scan.get("footnoteDefinitions") == 0, f"X.3 {name} footnotes must remain absent")
    require(scan.get("htmlBlockquotes") == 0, f"X.3 {name} HTML blockquotes must remain absent")
require(reader_scan.get("inlineQuotationSegments") == 0, "X.3 reader inline quotation drift")
require(reader_scan.get("markdownBlockquotes") == 0, "X.3 reader blockquote drift")
require(product_scan.get("inlineQuotationSegments") == 2, "X.3 Product inline quotation drift")
require(product_scan.get("markdownBlockquotes") == 0, "X.3 Product blockquote drift")
require(r9_scan.get("inlineQuotationSegments") == 204, "X.3 R9 inline quotation drift")
require(r9_scan.get("markdownBlockquotes") == 3, "X.3 R9 blockquote drift")
require(
    sum(
        int(scan.get("inlineQuotationSegments", 0))
        + int(scan.get("markdownBlockquotes", 0))
        for scan in (reader_scan, product_scan, r9_scan)
    )
    == 209,
    "X.3 aggregate quotation-surface drift",
)
require(len(reader_scan.get("sourceHeadings", [])) == 1, "X.3 reader source-heading drift")
require(len(product_scan.get("sourceHeadings", [])) == 0, "X.3 Product source-heading drift")
require(len(r9_scan.get("sourceHeadings", [])) == 1, "X.3 R9 source-heading drift")
require(reader_scan.get("fullFileSha256") == "44e79c9497b582802aed7cf7eefbc16db4cd9e1b2b3c6b493a4dde823fa57852", "X.3 reader SHA drift")
require(product_scan.get("fullFileSha256") == "621c0ab9af7a417cf73d9012f7ed02be74d02223a24af65a836b875a06d32e9d", "X.3 Product full SHA drift")
require(product_scan.get("scopedSha256") == "556f29a8402172abaf76dd62480398a8e3a73d0154341b745bc85bc0fb7caa5f", "X.3 Product scoped SHA drift")
require(r9_scan.get("fullFileSha256") == "533159ae410d10945ab851cd4d344d374ecb616dfadf947438a554001090f567", "X.3 R9 SHA drift")

product_scoped = builder.extract_sections(product_text, ["vyhod"]) if builder is not None else ""
require(russian_quote_segments(product_scoped) == EXPECTED_PRODUCT_QUOTES, "X.3 Product Scripture quote surface drift")
require("(Пс. 16:15)" in product_scoped, "X.3 Product Psalm locator missing")
require("как Он есть" in product_scoped, "X.3 Product 1 John fragment missing")

owner = read_json(OWNER_CLOSURE)
require(owner.get("authorityId") == "HEART-X3-OWNER-CLOSURE-2026-08-04", "X.3 owner authority drift")
require(owner.get("productSnapshot", {}).get("commit") == "0fbe7d1ead9ebd1bea867418e254da438ec63329", "X.3 owner Product commit drift")
require(owner.get("entryOverride", {}).get("primaryProductOwner", {}).get("sourceBlobSha") == PRODUCT_BLOB, "X.3 owner Product blob drift")
require(owner.get("entryOverride", {}).get("primaryProductOwner", {}).get("sectionId") == "vyhod", "X.3 owner section drift")
require(owner.get("entryOverride", {}).get("effectiveCitationState") == "PRODUCT_SECTION_CITATION_PASS_REQUIRED", "X.3 historical citation state drift")
require(owner.get("publicationBoundary", {}).get("newDirectQuotesApproved") == 0, "X.3 owner direct quote boundary drift")

assembly = read_json(READER_ASSEMBLY)
require(assembly.get("authorityId") == "HEART-X3-READER-ASSEMBLY-2026-08-04", "X.3 reader assembly authority drift")
require(assembly.get("reader", {}).get("state") == "ASSEMBLED_READER_PARAPHRASE_ONLY", "X.3 reader assembly mode drift")
require(assembly.get("exactSource", {}).get("blobSha") == PRODUCT_BLOB, "X.3 assembly Product blob drift")
require(assembly.get("exactSource", {}).get("sectionId") == "vyhod", "X.3 assembly section drift")
composition = assembly.get("composition", {})
require(composition.get("mode") == "PARAPHRASE_ONLY", "X.3 composition mode drift")
require(composition.get("newHistoricalClaims") == 0, "X.3 composition historical claim drift")
require(composition.get("newDirectQuotesApproved") == 0, "X.3 composition direct quote drift")
require(composition.get("exactProductProseQuotesCopied") == 0, "X.3 Product quote transfer drift")
require(assembly.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "X.3 assembly falsely closes whole-book citation pass")

source_registry = read_json(SOURCE_REGISTRY)
require(source_registry.get("schema_version") == 1, "source closure registry schema drift")
require(source_registry.get("scope") == "СЕРИЯ СЕРДЦЕ R1–R9 and V84 evidence boundaries", "source closure registry scope drift")
require(source_registry.get("counts") == {
    "unique_sources": 85,
    "trusted_sources": 81,
    "claims": 18,
    "quote_safe_claims": 9,
    "non_quote_claims": 9,
}, "source closure registry count drift")

triage = read_json(TRIAGE)
triage_rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-X3"]
require(len(triage_rows) == 1, "historical X.3 triage row missing")
if triage_rows:
    row = triage_rows[0]
    require(row.get("inventoryEntrySha256") == "4b4c812566e075fcb94612ed94f7fd16d4ec7c43185cd2516f6386298180fc74", "X.3 inventory-entry SHA drift")
    require(row.get("detected") == EXPECTED_TRIAGE, "X.3 aggregate inventory counts drift")
    require(row.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical X.3 triage state drift")

review = read_json(REVIEW)
require(review.get("authorityId") == "HEART-X3-CITATION-REVIEW-2026-08-04", "X.3 review authority drift")
require(review.get("status") == "X3_ENTRY_CITATION_PASS_COMPLETE_ALL_ASSEMBLED_READERS_REVIEWED_WHOLE_BOOK_OPEN", "X.3 review status drift")
immutable = review.get("immutableSources", {})
require(immutable.get("reader", {}).get("gitBlob") == RESEARCH_BLOBS[READER], "X.3 receipt reader blob drift")
require(immutable.get("productConclusion", {}).get("gitBlob") == PRODUCT_BLOB, "X.3 receipt Product blob drift")
require(immutable.get("r9Dossier", {}).get("gitBlob") == RESEARCH_BLOBS[R9], "X.3 receipt R9 blob drift")
require(immutable.get("ownerClosure", {}).get("gitBlob") == RESEARCH_BLOBS[OWNER_CLOSURE], "X.3 receipt owner closure blob drift")
require(immutable.get("readerAssembly", {}).get("gitBlob") == RESEARCH_BLOBS[READER_ASSEMBLY], "X.3 receipt assembly blob drift")
require(immutable.get("sourceClosureRegistry", {}).get("gitBlob") == RESEARCH_BLOBS[SOURCE_REGISTRY], "X.3 receipt source registry blob drift")
scripture = review.get("scriptureReview", {})
require(scripture.get("readerDetectedReferences") == 3, "X.3 receipt reader Scripture drift")
require(scripture.get("productSectionDetectedReferences") == 1, "X.3 receipt Product Scripture drift")
require(scripture.get("r9DetectedReferences") == 111, "X.3 receipt R9 Scripture drift")
require(scripture.get("aggregateUniqueReferences") == 115, "X.3 receipt aggregate Scripture drift")
require(scripture.get("translationVersionResolvedInReceipt") is True, "X.3 Product translation version unresolved")
product_quotes = scripture.get("productDirectScriptureQuotes", [])
require([row.get("text") for row in product_quotes] == EXPECTED_PRODUCT_QUOTES, "X.3 receipt Product quote text drift")
require([row.get("locator") for row in product_quotes] == ["Пс. 16:15", "1 Ин. 3:2"], "X.3 receipt Product quote locator drift")
require(all(row.get("version") == "RUSSIAN_SYNODAL" for row in product_quotes), "X.3 Product quote version drift")
require(all(row.get("transferToReader") is False for row in product_quotes), "X.3 Product quote transfer falsely approved")
require(scripture.get("reviewComplete") is True, "X.3 Scripture review incomplete")
quotation = review.get("quotationReview", {})
require(quotation.get("aggregateQuotationSurfaces") == 209, "X.3 receipt quotation total drift")
require(quotation.get("reader", {}).get("inlineQuotationSegments") == 0, "X.3 receipt reader quote drift")
require(quotation.get("productConclusion", {}).get("inlineQuotationSegments") == 2, "X.3 receipt Product quote drift")
require(quotation.get("r9Dossier", {}).get("inlineQuotationSegments") == 204, "X.3 receipt R9 inline drift")
require(quotation.get("r9Dossier", {}).get("markdownBlockquotes") == 3, "X.3 receipt R9 blockquote drift")
require(quotation.get("r9Dossier", {}).get("supportDossierPublicationAsDirectQuoteArticleApproved") is False, "X.3 R9 publication falsely approved")
require(quotation.get("r9Dossier", {}).get("approvedDirectQuoteTransferToReader") == 0, "X.3 R9 quote transfer drift")
require(quotation.get("newDirectQuotesApproved") == 0, "X.3 new direct quote drift")
require(quotation.get("reviewComplete") is True, "X.3 quotation review incomplete")
external = review.get("externalLinkReview", {})
require(external.get("aggregateExternalLinks") == 7, "X.3 receipt external-link count drift")
require({row.get("url") for row in external.get("links", [])} == EXPECTED_EXTERNAL_LINKS, "X.3 receipt external-link set drift")
require(set(external.get("internalArticleLinkTokens", [])) == EXPECTED_INTERNAL_TOKENS, "X.3 receipt internal-token set drift")
require(external.get("externalLinkBlockerResolved") is True, "X.3 external-link blocker unresolved")
require(external.get("reviewComplete") is True, "X.3 external-link review incomplete")
require(review.get("sourceGovernance", {}).get("mixedStatusQuoteBankNotBulkApproved") is True, "X.3 R9 bulk-approval boundary missing")
require(review.get("sourceGovernance", {}).get("reviewComplete") is True, "X.3 source governance incomplete")
disposition = review.get("disposition", {})
require(disposition.get("remainingEntryBlockers") == [], "X.3 blockers remain")
require(disposition.get("readerManuscriptChanged") is False, "X.3 reader mutation falsely claimed")
require(disposition.get("productSourceChanged") is False, "X.3 Product mutation falsely claimed")
require(disposition.get("r9DossierChanged") is False, "X.3 R9 mutation falsely claimed")
require(disposition.get("newHistoricalClaims") == 0, "X.3 historical claim drift")
require(disposition.get("newDirectQuotesApproved") == 0, "X.3 direct quote drift")
require(disposition.get("entryCitationPassComplete") is True, "X.3 entry pass not complete")
boundary = review.get("wholeBookBoundary", {})
require(boundary.get("entryCitationPassComplete") == "4 / 18", "whole-book completion count drift")
require(boundary.get("entryCitationPassOpen") == "14 / 18", "whole-book open count drift")
require(boundary.get("assembledReaderCitationReviewsComplete") == "4 / 4", "assembled-reader review count drift")
require(boundary.get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(boundary.get("productReleaseComplete") is False, "Product release falsely closed")

x1_review = read_json(X1_REVIEW)
require(x1_review.get("disposition", {}).get("entryCitationPassComplete") is True, "X.1 preceding pass missing")
require(x1_review.get("wholeBookBoundary", {}).get("entryCitationPassComplete") == "3 / 18", "X.1 historical count drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-X3-CITATION-REVIEW-2026-08-04",
    "X.3 ENTRY CITATION PASS = COMPLETE",
    "WHOLE-BOOK ENTRY CITATION PASSES = 4 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 4 / 4",
    "SCRIPTURE REFERENCES GOVERNED = 115 / 115",
    "QUOTATION SURFACES CLASSIFIED = 209 / 209",
    "EXTERNAL LINKS DISPOSITIONED = 7 / 7",
    "READER DIRECT QUOTES = 0",
    "NEW DIRECT QUOTES APPROVED = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
    RESEARCH_BLOBS[READER],
    PRODUCT_BLOB,
    RESEARCH_BLOBS[R9],
):
    require(marker in human, f"X.3 human authority marker missing: {marker}")
for forbidden in (
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "NEW DIRECT QUOTES APPROVED = 1",
    "R9 QUOTE BANK = BULK APPROVED",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"X.3 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.3 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart X.3 entry citation pass: PASS — "
    "115 Scripture refs; 209 quotation surfaces; 7 external links dispositioned; "
    "reader remains paraphrase-only with 0 direct quotes; all assembled readers 4/4; "
    "whole-book 4/18"
)
