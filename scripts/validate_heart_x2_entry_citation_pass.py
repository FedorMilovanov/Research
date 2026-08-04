#!/usr/bin/env python3
"""Validate the completed X.2 entry citation pass across reader and evidence surfaces."""
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
REVIEW = ROOT / "data/heart-x2-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-x2-reader-assembly-2026-08-04.json"
OWNER = ROOT / "data/heart-x2-owner-closure-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
CURRENT_PASS = ROOT / "data/heart-entry-citation-pass-current-2026-08-04.json"
X1_REVIEW = ROOT / "data/heart-x1-citation-review-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/97_READER_CHAPTER_X2_GLORIFIED_HEART_2026-08-04.md"
DOSSIER = ROOT / "СЕРИЯ СЕРДЦЕ/77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md"
X1_READER = ROOT / "СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/99_X2_CITATION_REVIEW_2026-08-04.md"
PRODUCT_PATH = Path("src/content/articles/osvobozhdennoe-serdce.mdx")

BLOBS = {
    READER: "72f6a9d70b32af65d7a44c297d467e9fabdc4a85",
    ASSEMBLY: "c6d80a65ad7b4d764252ad48169b1e33ad88d283",
    OWNER: "c1fdcfba816bdc6131d157760632d4899f89731c",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    CURRENT_PASS: "79cfd859180a95da76c8102bc4167f245487dd74",
    X1_REVIEW: "81c4f9f0354ed3e156a4f84f223035801795046e",
    DOSSIER: "ae5c16ef129892e169596fbd90490b5d4f64aa43",
    X1_READER: "0fe2b234c1249d1dc6f1e37103f63c850fb41b83",
}
PRODUCT_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
PRODUCT_FULL_SHA = "621c0ab9af7a417cf73d9012f7ed02be74d02223a24af65a836b875a06d32e9d"
SECTION_IDS = [
    "chetyre-sostoyaniya",
    "vopl-i-otvet",
    "ne-besplotnoe-parenie",
    "ne-sposobno-greshit",
    "pobeda-nad-vragom",
]
EXPECTED_PRODUCT_INLINE = [
    "Человеческая природа в её четверояком состоянии",
    "Крайне ли испорчено сердце",
    "Бедный я человек! кто избавит меня от сего тела смерти?",
    "Благодарю Бога моего Иисусом Христом",
    "искупление тела",
    "искупление",
    "освобождение через выкуп",
    "начавший в вас доброе дело",
    "даже до дня Иисуса Христа",
    "уничижённое тело наше преобразит так, что оно будет сообразно славному телу Его",
    "тело духовное",
    "бесплотное",
    "телу душевному",
    "нетление",
    "сделана совершенно и неизменно свободной только к добру",
    "Будем подобны Ему, потому что увидим Его, как Он есть",
    "Блаженны чистые сердцем, ибо они Бога узрят",
    "духов праведников, достигших совершенства",
    "стремящихся",
    "поглощается",
    "проглотить, поглотить без остатка",
    "отрёт Бог всякую слезу с очей их, и смерти не будет уже; ни плача, ни вопля, ни болезни уже не будет",
    "И ничего уже не будет проклятого",
]
EXPECTED_PRODUCT_BLOCKS = [
    "Мы в себе стенаем, ожидая усыновления, искупления тела нашего (Рим. 8:23).",
    "Сеется в тлении, восстаёт в нетлении… сеется тело душевное, восстаёт тело духовное (1 Кор. 15:42, 44).",
    "Смерть! где твоё жало? ад! где твоя победа?.. Благодарение Богу, даровавшему нам победу Господом нашим Иисусом Христом (1 Кор. 15:55, 57).",
]
EXPECTED_SCRIPTURE_QUOTES = [
    ("Бедный я человек! кто избавит меня от сего тела смерти?", "Рим. 7:24", "inline"),
    ("Благодарю Бога моего Иисусом Христом", "Рим. 7:25", "inline"),
    ("искупление тела", "Рим. 8:23", "inline_fragment"),
    ("начавший в вас доброе дело", "Флп. 1:6", "inline_fragment"),
    ("даже до дня Иисуса Христа", "Флп. 1:6", "inline_fragment"),
    ("Мы в себе стенаем, ожидая усыновления, искупления тела нашего", "Рим. 8:23", "markdown_blockquote"),
    ("уничижённое тело наше преобразит так, что оно будет сообразно славному телу Его", "Флп. 3:21", "inline"),
    ("тело духовное", "1 Кор. 15:44", "inline_fragment"),
    ("телу душевному", "1 Кор. 15:44", "inline_fragment"),
    ("Сеется в тлении, восстаёт в нетлении… сеется тело душевное, восстаёт тело духовное", "1 Кор. 15:42, 44", "markdown_blockquote"),
    ("Будем подобны Ему, потому что увидим Его, как Он есть", "1 Ин. 3:2", "inline"),
    ("Блаженны чистые сердцем, ибо они Бога узрят", "Мф. 5:8", "inline"),
    ("духов праведников, достигших совершенства", "Евр. 12:23", "inline_fragment"),
    ("отрёт Бог всякую слезу с очей их, и смерти не будет уже; ни плача, ни вопля, ни болезни уже не будет", "Откр. 21:4", "inline"),
    ("И ничего уже не будет проклятого", "Откр. 22:3", "inline"),
    ("Смерть! где твоё жало? ад! где твоя победа?.. Благодарение Богу, даровавшему нам победу Господом нашим Иисусом Христом", "1 Кор. 15:55, 57", "markdown_blockquote"),
]
EXPECTED_HISTORICAL = {
    "ownerSurfaces": 3,
    "sourceHeadings": 1,
    "scriptureReferences": 50,
    "externalLinks": 0,
    "internalArticleLinks": 1,
    "quotationSurfaces": 59,
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


def git_blob(root: Path, path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()


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


def quotes(text: str) -> list[str]:
    return re.findall(r"«([^»\n]{8,})»", text) + re.findall(r"“([^”\n]{8,})”", text)


def blocks(text: str) -> list[str]:
    return [line.lstrip()[1:].strip() for line in text.splitlines() if re.match(r"^\s*>\s?\S", line)]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
product_file = product_root / PRODUCT_PATH
require(product_root.is_dir(), "exact Product checkout missing")
require(product_file.is_file(), "exact X.2 Product source missing")

for path, expected in BLOBS.items():
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(ROOT, path.relative_to(ROOT)) == expected, f"immutable Research blob drift: {path.relative_to(ROOT)}")
if product_file.is_file():
    require(git_blob(product_root, PRODUCT_PATH) == PRODUCT_BLOB, "immutable Product blob drift")

builder = import_builder()
reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
require(sha256_text(product_text) == PRODUCT_FULL_SHA, "Product full SHA drift")

reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "X.2 reader"), product_root) if builder else {}
dossier_scan = builder.scan_owner(builder.r(str(DOSSIER.relative_to(ROOT)), "judgment dossier"), product_root) if builder else {}
x1_scan = builder.scan_owner(builder.r(str(X1_READER.relative_to(ROOT)), "X.1 reader"), product_root) if builder else {}
product_scoped = "\n".join(builder.extract_sections(product_text, [section_id]) for section_id in SECTION_IDS) if builder else ""
product_refs = sorted({builder.normalize_ref(match.group(0)) for match in builder.SCRIPTURE_RE.finditer(product_scoped)}, key=str.casefold) if builder else []
product_urls = sorted({builder.trim_url(match.group(0)) for match in builder.URL_RE.finditer(product_scoped)}, key=str.casefold) if builder else []
product_internal = sorted(set(builder.ARTICLE_LINK_RE.findall(product_scoped))) if builder else []
product_inline = quotes(product_scoped)
product_blocks = blocks(product_scoped)

require(len(reader_scan.get("scriptureReferences", [])) == 9, "X.2 reader Scripture count drift")
require(reader_scan.get("inlineQuotationSegments") == 0 and reader_scan.get("markdownBlockquotes") == 0, "X.2 reader quotation boundary drift")
require(reader_scan.get("externalLinks") == [] and reader_scan.get("internalArticleLinks") == [], "X.2 reader link boundary drift")
require("**Новые прямые цитаты:** `0`" in reader_text, "X.2 reader zero-direct-quote declaration missing")
require("X.2 ENTRY CITATION PASS = OPEN" in reader_text, "historical X.2 reader citation-open marker missing")

require(len(product_refs) == 10, "X.2 Product Scripture count drift")
require(product_urls == [], "X.2 Product external links must remain absent")
require(product_internal == ["/articles/krajne-li-isporcheno-serdce/"], "X.2 Product internal-link set drift")
require(product_inline == EXPECTED_PRODUCT_INLINE, "X.2 Product inline quotation surface drift")
require(product_blocks == EXPECTED_PRODUCT_BLOCKS, "X.2 Product blockquote surface drift")
require(len(product_inline) == 23 and len(product_blocks) == 3, "X.2 Product quotation count drift")

support_refs = set(dossier_scan.get("scriptureReferences", [])) | set(x1_scan.get("scriptureReferences", []))
historical_refs = support_refs | set(product_refs)
current_refs = historical_refs | set(reader_scan.get("scriptureReferences", []))
require(len(dossier_scan.get("scriptureReferences", [])) == 37, "X.2 support dossier Scripture count drift")
require(len(x1_scan.get("scriptureReferences", [])) == 3, "X.2 support X.1 Scripture count drift")
require(len(support_refs) == 40, "X.2 support Scripture union drift")
require(len(historical_refs) == 50, "X.2 historical evidence Scripture union drift")
require(len(current_refs) == 50, "X.2 current reader-plus-evidence Scripture union drift")
require(set(reader_scan.get("scriptureReferences", [])).issubset(historical_refs), "X.2 reader Scripture references exceed governed evidence")

support_surfaces = sum(int(scan.get("inlineQuotationSegments", 0)) + int(scan.get("markdownBlockquotes", 0)) for scan in (dossier_scan, x1_scan))
require(support_surfaces == 33, "X.2 support quotation-surface count drift")
require(len(product_inline) + len(product_blocks) + support_surfaces == 59, "X.2 historical quotation-surface total drift")
require(len(product_inline) + len(product_blocks) + support_surfaces + int(reader_scan.get("inlineQuotationSegments", 0)) + int(reader_scan.get("markdownBlockquotes", 0)) == 59, "X.2 current quotation-surface total drift")

triage = read_json(TRIAGE)
rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-X2"]
require(len(rows) == 1, "historical X.2 triage row missing")
if rows:
    row = rows[0]
    require(row.get("inventoryEntrySha256") == "9754ba5e5545d57d56d56ee9f23f3204c7e40e424cc4ed7956db8e83707347a6", "X.2 inventory-entry SHA drift")
    require(row.get("detected") == EXPECTED_HISTORICAL, "X.2 historical detected counts drift")
    require(row.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical X.2 triage state rewritten")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-X2-READER-ASSEMBLY-2026-08-04", "X.2 assembly authority drift")
require(assembly.get("publicationBoundary", {}).get("x2UnifiedReaderAssembled") is True, "X.2 assembly not complete")
require(assembly.get("publicationBoundary", {}).get("x2EntryCitationPassComplete") is False, "historical X.2 assembly receipt rewritten")
require(assembly.get("reader", {}).get("gitBlob") == BLOBS[READER], "X.2 assembly reader blob drift")
require(assembly.get("exactProductSource", {}).get("gitBlob") == PRODUCT_BLOB, "X.2 assembly Product blob drift")

x1_review = read_json(X1_REVIEW)
require(x1_review.get("authorityId") == "HEART-X1-CITATION-REVIEW-2026-08-04", "X.1 support authority drift")
require(x1_review.get("disposition", {}).get("entryCitationPassComplete") is True, "X.1 support citation pass incomplete")
require(x1_review.get("wholeBookBoundary", {}).get("entryCitationPassComplete") == "3 / 18", "X.1 historical composed count drift")
require(x1_review.get("scriptureReview", {}).get("aggregateUniqueReferences") == 40, "X.1 support Scripture governance drift")
require(x1_review.get("quotationReview", {}).get("aggregateQuotationSurfaces") == 33, "X.1 support quotation governance drift")

preceding = read_json(CURRENT_PASS)
require(preceding.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-2026-08-04", "preceding current authority drift")
require(preceding.get("currentCounts", {}).get("entryCitationPassComplete") == 4, "preceding current citation count drift")
require(preceding.get("currentCounts", {}).get("assembledReaderEntries") == 4, "preceding historical reader count drift")

review = read_json(REVIEW)
require(review.get("authorityId") == "HEART-X2-CITATION-REVIEW-2026-08-04", "X.2 review authority drift")
require(review.get("status") == "X2_ENTRY_CITATION_PASS_COMPLETE_ASSEMBLED_READER_REVIEWS_FIVE_OF_FIVE_WHOLE_BOOK_OPEN", "X.2 review status drift")
require(review.get("entry", {}).get("inventoryEntrySha256") == "9754ba5e5545d57d56d56ee9f23f3204c7e40e424cc4ed7956db8e83707347a6", "X.2 receipt inventory SHA drift")
scripture = review.get("scriptureReview", {})
require(scripture.get("readerDetectedReferences") == 9, "X.2 receipt reader Scripture count drift")
require(scripture.get("productSectionUniqueReferences") == 10, "X.2 receipt Product Scripture count drift")
require(scripture.get("x1SupportUniqueReferences") == 40, "X.2 receipt support Scripture count drift")
require(scripture.get("historicalThreeOwnerUniqueReferences") == 50, "X.2 receipt historical Scripture count drift")
require(scripture.get("currentReaderPlusEvidenceUniqueReferences") == 50, "X.2 receipt current Scripture count drift")
require(scripture.get("readerReferencesSubsetOfGovernedEvidence") is True, "X.2 reader evidence-subset boundary drift")
require(scripture.get("productDirectScriptureQuotationSurfaces") == 16, "X.2 direct Scripture surface count drift")
require(scripture.get("productDirectScriptureQuotationVersion") == "RUSSIAN_SYNODAL", "X.2 Product Scripture version drift")
expected_quote_rows = [{"text": text, "locator": locator, "version": "RUSSIAN_SYNODAL", "surface": surface, "transferToReader": False} for text, locator, surface in EXPECTED_SCRIPTURE_QUOTES]
require(scripture.get("productDirectScriptureQuotations") == expected_quote_rows, "X.2 direct Scripture quotation registry drift")
require(scripture.get("translationVersionResolved") is True, "X.2 translation-version blocker unresolved")
require(scripture.get("reviewComplete") is True, "X.2 Scripture review incomplete")
quotation = review.get("quotationReview", {})
product_review = quotation.get("productSections", {})
require(product_review == {
    "inlineQuotationSegments": 23,
    "markdownBlockquotes": 3,
    "quotationSurfaces": 26,
    "scriptureDirectQuotationSurfaces": 16,
    "confessionalDirectQuotationSurfaces": 1,
    "titleSurfaces": 2,
    "technicalLexicalOrAuthorialSurfaces": 7,
    "approvedDirectQuoteTransferToReader": 0,
}, "X.2 Product quotation classification drift")
confession = quotation.get("confessionalQuotation", {})
require(confession.get("text") == "сделана совершенно и неизменно свободной только к добру", "X.2 confessional quotation text drift")
require(confession.get("locators") == ["Westminster Confession of Faith 9.5", "Second London Baptist Confession 1689 9.5"], "X.2 confessional locator drift")
require(confession.get("sourceUrls") == ["https://www.opc.org/wcf.html", "https://baptistconfession.org/"], "X.2 confessional source URL drift")
require(confession.get("transferToReader") is False, "X.2 confessional quote transfer falsely approved")
require(quotation.get("historicalThreeOwnerQuotationSurfaces") == 59, "X.2 receipt historical quotation total drift")
require(quotation.get("currentReaderPlusEvidenceQuotationSurfaces") == 59, "X.2 receipt current quotation total drift")
require(quotation.get("newDirectQuotesApproved") == 0, "X.2 new direct quote drift")
require(quotation.get("reviewComplete") is True, "X.2 quotation review incomplete")
link_review = review.get("linkReview", {})
require(link_review.get("externalLinks") == 0, "X.2 receipt external link drift")
require(link_review.get("productInternalArticleLinks") == ["/articles/krajne-li-isporcheno-serdce/"], "X.2 receipt internal link drift")
require(link_review.get("readerInternalArticleLinks") == 0, "X.2 reader internal link drift")
require(link_review.get("linkBlockerResolved") is True, "X.2 link blocker unresolved")
require(review.get("supportGovernance", {}).get("x1CitationPassRequiredAndComplete") is True, "X.2 X.1 support boundary unresolved")
disposition = review.get("disposition", {})
require(disposition.get("remainingEntryBlockers") == [], "X.2 blockers remain")
require(disposition.get("readerManuscriptChanged") is False, "X.2 reader mutation falsely claimed")
require(disposition.get("productSourceChanged") is False, "X.2 Product mutation falsely claimed")
require(disposition.get("researchSupportChanged") is False, "X.2 support mutation falsely claimed")
require(disposition.get("newHistoricalClaims") == 0, "X.2 historical claim drift")
require(disposition.get("newDirectQuotesApproved") == 0, "X.2 direct quote approval drift")
require(disposition.get("entryCitationPassComplete") is True, "X.2 entry citation pass incomplete")
boundary = review.get("wholeBookBoundary", {})
require(boundary.get("assembledReaderEntries") == "5 / 18", "X.2 assembled-reader count drift")
require(boundary.get("assembledReaderCitationReviewsComplete") == "5 / 5", "X.2 assembled-reader review count drift")
require(boundary.get("missingStandaloneFinalReaders") == 13, "X.2 missing-reader count drift")
require(boundary.get("entryCitationPassComplete") == "5 / 18", "X.2 whole-book citation completion count drift")
require(boundary.get("entryCitationPassOpen") == "13 / 18", "X.2 open citation count drift")
require(boundary.get("wholeBookReaderAssemblyComplete") is False, "whole-book reader assembly falsely closed")
require(boundary.get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(boundary.get("productReleaseComplete") is False, "Product release falsely closed")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-X2-CITATION-REVIEW-2026-08-04",
    "X.2 ENTRY CITATION PASS = COMPLETE",
    "ENTRY CITATION PASSES COMPLETE = 5 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 5 / 5",
    "SCRIPTURE REFERENCES GOVERNED = 50 / 50",
    "PRODUCT QUOTATION SURFACES CLASSIFIED = 26 / 26",
    "HISTORICAL THREE-OWNER QUOTATION SURFACES = 59 / 59",
    "PRODUCT SCRIPTURE QUOTATION VERSION = RUSSIAN SYNODAL",
    "NEW DIRECT QUOTES APPROVED = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
    BLOBS[READER],
    PRODUCT_BLOB,
):
    require(marker in human, f"X.2 human citation authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "NEW DIRECT QUOTES APPROVED = 1",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"X.2 human citation authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.2 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart X.2 entry citation pass: PASS — "
    "50/50 governed Scripture refs; 59/59 evidence quotation surfaces; "
    "26 Product surfaces classified, 16 Synodal + 1 confessional direct surfaces; "
    "reader 0 direct quotes; assembled-reader reviews 5/5; whole-book 5/18"
)
