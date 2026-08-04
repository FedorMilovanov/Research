#!/usr/bin/env python3
"""Validate the self-contained X.2 entry citation pass."""
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
CURRENT = ROOT / "data/heart-entry-citation-pass-current-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/97_READER_CHAPTER_X2_GLORIFIED_HEART_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/99_X2_CITATION_REVIEW_2026-08-04.md"
PRODUCT_REL = Path("src/content/articles/osvobozhdennoe-serdce.mdx")

BLOBS = {
    READER: "72f6a9d70b32af65d7a44c297d467e9fabdc4a85",
    ASSEMBLY: "c6d80a65ad7b4d764252ad48169b1e33ad88d283",
    OWNER: "c1fdcfba816bdc6131d157760632d4899f89731c",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    CURRENT: "79cfd859180a95da76c8102bc4167f245487dd74",
}
PRODUCT_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
PRODUCT_SHA256 = "621c0ab9af7a417cf73d9012f7ed02be74d02223a24af65a836b875a06d32e9d"
SECTION_IDS = ["chetyre-sostoyaniya", "vopl-i-otvet", "ne-besplotnoe-parenie", "ne-sposobno-greshit", "pobeda-nad-vragom"]
READER_REFS = {"Рим.7", "Рим.8", "Флп.1:6", "1 Кор.15", "Флп.3:21", "1 Ин.3:2", "Мф.5:8", "Евр.12:23", "Откр.21–22"}
PRODUCT_REFS = {"Рим.7:24", "Рим.7:25", "Рим.8:23", "Флп.1:6", "1 Кор.15:42,44", "Флп.3:21", "1 Ин.3:2", "Евр.12:23", "Мф.5:8", "1 Кор.15:55,57"}
MANUAL_REFS = {"Отк.21:4", "Отк.22:3"}
PRODUCT_INLINE = [
    "Человеческая природа в её четверояком состоянии", "Крайне ли испорчено сердце",
    "Бедный я человек! кто избавит меня от сего тела смерти?", "Благодарю Бога моего Иисусом Христом",
    "искупление тела", "искупление", "освобождение через выкуп", "начавший в вас доброе дело",
    "даже до дня Иисуса Христа", "уничижённое тело наше преобразит так, что оно будет сообразно славному телу Его",
    "тело духовное", "бесплотное", "телу душевному", "нетление",
    "сделана совершенно и неизменно свободной только к добру", "Будем подобны Ему, потому что увидим Его, как Он есть",
    "Блаженны чистые сердцем, ибо они Бога узрят", "духов праведников, достигших совершенства",
    "стремящихся", "поглощается", "проглотить, поглотить без остатка",
    "отрёт Бог всякую слезу с очей их, и смерти не будет уже; ни плача, ни вопля, ни болезни уже не будет",
    "И ничего уже не будет проклятого",
]
PRODUCT_BLOCKS = [
    "Мы в себе стенаем, ожидая усыновления, искупления тела нашего (Рим. 8:23).",
    "Сеется в тлении, восстаёт в нетлении… сеется тело душевное, восстаёт тело духовное (1 Кор. 15:42, 44).",
    "Смерть! где твоё жало? ад! где твоя победа?.. Благодарение Богу, даровавшему нам победу Господом нашим Иисусом Христом (1 Кор. 15:55, 57).",
]
SCRIPTURE = [
    ["Бедный я человек! кто избавит меня от сего тела смерти?", "Рим.7:24", "inline"],
    ["Благодарю Бога моего Иисусом Христом", "Рим.7:25", "inline"],
    ["искупление тела", "Рим.8:23", "inline_fragment"],
    ["искупление", "Рим.8:23", "inline_term"],
    ["начавший в вас доброе дело", "Флп.1:6", "inline_fragment"],
    ["даже до дня Иисуса Христа", "Флп.1:6", "inline_fragment"],
    [PRODUCT_BLOCKS[0], "Рим.8:23", "markdown_blockquote"],
    ["уничижённое тело наше преобразит так, что оно будет сообразно славному телу Его", "Флп.3:21", "inline"],
    ["тело духовное", "1 Кор.15:44", "inline_fragment"],
    ["телу душевному", "1 Кор.15:44", "inline_fragment"],
    ["нетление", "1 Кор.15:42", "inline_term"],
    [PRODUCT_BLOCKS[1], "1 Кор.15:42,44", "markdown_blockquote"],
    ["Будем подобны Ему, потому что увидим Его, как Он есть", "1 Ин.3:2", "inline"],
    ["Блаженны чистые сердцем, ибо они Бога узрят", "Мф.5:8", "inline"],
    ["духов праведников, достигших совершенства", "Евр.12:23", "inline_fragment"],
    ["отрёт Бог всякую слезу с очей их, и смерти не будет уже; ни плача, ни вопля, ни болезни уже не будет", "Отк.21:4", "inline"],
    ["И ничего уже не будет проклятого", "Отк.22:3", "inline"],
    [PRODUCT_BLOCKS[2], "1 Кор.15:55,57", "markdown_blockquote"],
]
CONFESSIONAL = "сделана совершенно и неизменно свободной только к добру"
TITLES = {"Человеческая природа в её четверояком состоянии", "Крайне ли испорчено сердце"}
EDITORIAL = {"освобождение через выкуп", "бесплотное", "стремящихся", "поглощается", "проглотить, поглотить без остатка"}
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


def inline_quotes(text: str) -> list[str]:
    return re.findall(r"«([^»\n]{8,})»", text) + re.findall(r"“([^”\n]{8,})”", text)


def blockquotes(text: str) -> list[str]:
    return [line.lstrip()[1:].strip() for line in text.splitlines() if re.match(r"^\s*>\s?\S", line)]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
product_file = product_root / PRODUCT_REL
require(product_root.is_dir(), "exact Product checkout missing")
require(product_file.is_file(), "exact Product source missing")
for path, expected in BLOBS.items():
    require(path.is_file(), f"immutable source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(ROOT, path.relative_to(ROOT)) == expected, f"immutable blob drift: {path.relative_to(ROOT)}")
if product_file.is_file():
    require(git_blob(product_root, PRODUCT_REL) == PRODUCT_BLOB, "Product blob drift")

builder = import_builder()
reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
require(hashlib.sha256(product_text.encode("utf-8")).hexdigest() == PRODUCT_SHA256, "Product SHA-256 drift")
reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "X.2 reader"), product_root) if builder else {}
product_scoped = "\n".join(builder.extract_sections(product_text, [section_id]) for section_id in SECTION_IDS) if builder else ""
product_refs = {builder.normalize_ref(match.group(0)) for match in builder.SCRIPTURE_RE.finditer(product_scoped)} if builder else set()
product_urls = {builder.trim_url(match.group(0)) for match in builder.URL_RE.finditer(product_scoped)} if builder else set()
product_internal = set(builder.ARTICLE_LINK_RE.findall(product_scoped)) if builder else set()
actual_inline = inline_quotes(product_scoped)
actual_blocks = blockquotes(product_scoped)

require(set(reader_scan.get("scriptureReferences", [])) == READER_REFS, "reader Scripture set drift")
require(reader_scan.get("inlineQuotationSegments") == 0 and reader_scan.get("markdownBlockquotes") == 0, "reader quotation boundary drift")
require(reader_scan.get("externalLinks") == [] and reader_scan.get("internalArticleLinks") == [], "reader link boundary drift")
require("**Новые прямые цитаты:** `0`" in reader_text, "reader zero-direct-quote marker missing")
require("X.2 ENTRY CITATION PASS = OPEN" in reader_text, "historical reader citation-open marker missing")
require(product_refs == PRODUCT_REFS, "Product scanner Scripture set drift")
require("Отк. 21:4" in product_scoped and "Отк. 22:3" in product_scoped, "manual Revelation locator gap drift")
require(len(READER_REFS | PRODUCT_REFS | MANUAL_REFS) == 16, "aggregate governed locator count drift")
require(product_urls == set(), "Product external link drift")
require(product_internal == {"/articles/krajne-li-isporcheno-serdce/"}, "Product internal link drift")
require(actual_inline == PRODUCT_INLINE, "Product inline quotation order/text drift")
require(actual_blocks == PRODUCT_BLOCKS, "Product blockquote order/text drift")
require(len(actual_inline) == 23 and len(actual_blocks) == 3, "Product quotation count drift")

review = read_json(REVIEW)
require(review.get("authorityId") == "HEART-X2-CITATION-REVIEW-2026-08-04", "review authority drift")
require(review.get("status") == "X2_ENTRY_CITATION_PASS_COMPLETE_ASSEMBLED_READER_REVIEWS_FIVE_OF_FIVE_WHOLE_BOOK_OPEN", "review status drift")
require(review.get("entry", {}).get("inventoryEntrySha256") == "9754ba5e5545d57d56d56ee9f23f3204c7e40e424cc4ed7956db8e83707347a6", "inventory row SHA drift")
require(review.get("entry", {}).get("triageStateBefore") == "TRIAGED_OPEN", "historical triage state drift")
immutable = review.get("immutableSources", {})
for key, path in (("reader", READER), ("readerAssembly", ASSEMBLY), ("ownerClosure", OWNER), ("precedingCurrentCitationAuthority", CURRENT), ("historicalTriage", TRIAGE)):
    require(immutable.get(key) == [str(path.relative_to(ROOT)), BLOBS[path]], f"review immutable source drift: {key}")
product = immutable.get("product", {})
require(product.get("gitBlob") == PRODUCT_BLOB and product.get("fullFileSha256") == PRODUCT_SHA256, "review Product witness drift")
require(product.get("sectionIds") == SECTION_IDS, "review Product section order drift")
historical = review.get("historicalInventoryWitness", {})
require(historical.get("detectedScriptureReferences") == 50 and historical.get("detectedQuotationSurfaces") == 59, "historical inventory witness drift")
require(historical.get("includesX1JudgmentSupportChain") is True and historical.get("reapprovedInThisTransaction") is False, "historical support boundary drift")
scripture = review.get("scriptureReview", {})
require(set(scripture.get("readerDetectedReferences", [])) == READER_REFS, "receipt reader Scripture set drift")
require(set(scripture.get("productScannerDetectedReferences", [])) == PRODUCT_REFS, "receipt Product Scripture set drift")
require(set(scripture.get("productManualScannerGapReferences", [])) == MANUAL_REFS, "receipt manual locator set drift")
require(scripture.get("readerDetectedReferenceCount") == 9, "receipt reader reference count drift")
require(scripture.get("productScannerDetectedReferenceCount") == 10, "receipt Product scanner count drift")
require(scripture.get("productManualScannerGapReferenceCount") == 2, "receipt manual gap count drift")
require(scripture.get("productGovernedLocatorCount") == 12 and scripture.get("aggregateUniqueGovernedLocatorCount") == 16, "receipt governed locator counts drift")
require(scripture.get("productScriptureTranslation") == "RUSSIAN_SYNODAL" and scripture.get("productScriptureQuotationSurfaces") == 18, "Scripture version/surface drift")
require(scripture.get("translationVersionResolved") is True and scripture.get("reviewComplete") is True, "Scripture review incomplete")
require(set(scripture.get("verificationSources", [])) == {"https://bible.by/syn/", "https://www.bible.com/ru/bible/400/PHP.1.6.SYNO", "https://www.bible.com/ru/bible/400/PHP.3.21.SYNO"}, "Scripture verification-source drift")

quotation = review.get("quotationReview", {})
require(quotation.get("reader") == {"inlineQuotationSegments": 0, "markdownBlockquotes": 0, "directQuotes": 0, "paraphraseOnlyBoundaryPreserved": True}, "reader quotation receipt drift")
product_q = quotation.get("product", {})
require(product_q.get("inlineQuotationSegments") == 23 and product_q.get("markdownBlockquotes") == 3 and product_q.get("quotationSurfaces") == 26, "Product quotation totals drift")
require(product_q.get("categoryCounts") == {"RUSSIAN_SYNODAL_SCRIPTURE": 18, "CONFESSIONAL_SUBSTANCE": 1, "BIBLIOGRAPHIC_OR_ARTICLE_TITLE": 2, "EDITORIAL_OR_LEXICAL_GLOSS": 5}, "quotation category counts drift")
require(quotation.get("russianSynodalScripture") == SCRIPTURE, "Scripture quotation classification drift")
conf = quotation.get("confessionalSubstance", [])
require(len(conf) == 1 and conf[0].get("text") == CONFESSIONAL, "confessional surface drift")
require(conf[0].get("locators") == ["Westminster Confession of Faith 9.5", "Second London Baptist Confession 1689 9.5"], "confessional locator drift")
require(conf[0].get("sourceUrls") == ["https://www.wts.edu/wcf/chapter-9-of-free-will", "https://www.the1689confession.com/1689/chapter-9"], "confessional source URL drift")
require({row[0] for row in quotation.get("bibliographicOrArticleTitles", [])} == TITLES, "title surface classification drift")
require({row[0] for row in quotation.get("editorialOrLexicalGlosses", [])} == EDITORIAL, "editorial surface classification drift")
classified = {row[0] for row in SCRIPTURE} | {CONFESSIONAL} | TITLES | EDITORIAL
require(classified == set(PRODUCT_INLINE + PRODUCT_BLOCKS), "not all Product surfaces are classified exactly once")
require(sum((len(SCRIPTURE), len(conf), len(TITLES), len(EDITORIAL))) == 26, "classified surface count drift")
require(quotation.get("allProductSurfacesDispositioned") == "26 / 26", "surface disposition completion drift")
require(quotation.get("approvedDirectQuoteTransferToReader") == 0 and quotation.get("newDirectQuotesApproved") == 0, "direct quote boundary drift")
require(quotation.get("reviewComplete") is True, "quotation review incomplete")

link = review.get("linkReview", {})
require(link.get("externalLinks") == 0 and link.get("readerInternalArticleLinks") == 0, "link count drift")
require(link.get("productInternalArticleLinks") == [{"path": "/articles/krajne-li-isporcheno-serdce/", "section": "chetyre-sostoyaniya", "disposition": "EXISTING_PRODUCT_CONTEXT_LINK_SOURCE_ONLY_NOT_COPIED_TO_READER"}], "internal link disposition drift")
require(link.get("linkBlockerResolved") is True and link.get("reviewComplete") is True, "link review incomplete")
require(review.get("supportBoundary") == {"x1SupportReapprovedInThisTransaction": False, "x1OwnsJudicialFork": True, "x2OwnsPositiveGlorification": True, "x3OwnsBookConclusion": True}, "support ownership boundary drift")
disposition = review.get("disposition", {})
require(disposition.get("remainingEntryBlockers") == [], "entry blockers remain")
require(disposition.get("readerManuscriptChanged") is False and disposition.get("productSourceChanged") is False and disposition.get("researchSupportChanged") is False, "source mutation falsely claimed")
require(disposition.get("newHistoricalClaims") == 0 and disposition.get("newDirectQuotesApproved") == 0 and disposition.get("entryCitationPassComplete") is True, "entry disposition drift")
boundary = review.get("wholeBookBoundary", {})
require(boundary.get("assembledReaderEntries") == "5 / 18" and boundary.get("assembledReaderCitationReviewsComplete") == "5 / 5", "assembled-reader state drift")
require(boundary.get("entryCitationPassComplete") == "5 / 18" and boundary.get("entryCitationPassOpen") == "13 / 18", "entry citation count drift")
require(boundary.get("missingStandaloneFinalReaders") == 13, "missing-reader count drift")
for field in ("wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete", "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete", "manuscriptBundleComplete", "productReleaseComplete"):
    require(boundary.get(field) is False, f"publication boundary falsely closed: {field}")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-X2-READER-ASSEMBLY-2026-08-04", "assembly authority drift")
require(assembly.get("effectivePrimaryState", {}).get("entryCitationPassComplete") is False, "historical assembly receipt rewritten")
require(assembly.get("publicationBoundary", {}).get("x2EntryCitationPassComplete") is False, "assembly citation-open boundary rewritten")
current = read_json(CURRENT)
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 4, "preceding current count drift")
require("HEART-BOOK-X2" in current.get("openEntryIds", []), "X.2 absent from preceding open set")
triage = read_json(TRIAGE)
rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-X2"]
require(len(rows) == 1, "historical X.2 triage row missing")
if rows:
    require(rows[0].get("inventoryEntrySha256") == "9754ba5e5545d57d56d56ee9f23f3204c7e40e424cc4ed7956db8e83707347a6", "historical inventory-row SHA drift")
    require(rows[0].get("detected") == {"ownerSurfaces": 3, "sourceHeadings": 1, "scriptureReferences": 50, "externalLinks": 0, "internalArticleLinks": 1, "quotationSurfaces": 59}, "historical X.2 detected counts drift")
    require(rows[0].get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical triage state rewritten")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-X2-CITATION-REVIEW-2026-08-04", "X.2 ENTRY CITATION PASS = COMPLETE",
    "ENTRY CITATION PASSES COMPLETE = 5 / 18", "ASSEMBLED READER CITATION REVIEWS = 5 / 5",
    "X.2 GOVERNED SCRIPTURE LOCATORS = 16", "PRODUCT QUOTATION SURFACES CLASSIFIED = 26 / 26",
    "RUSSIAN SYNODAL SCRIPTURE SURFACES = 18", "CONFESSIONAL SURFACES = 1",
    "TITLE SURFACES = 2", "EDITORIAL / LEXICAL SURFACES = 5",
    "X.1 SUPPORT REAPPROVED = FALSE", "NEW DIRECT QUOTES APPROVED = 0",
    "WHOLE-BOOK CITATION PASS = OPEN", BLOBS[READER], BLOBS[ASSEMBLY], PRODUCT_BLOB,
):
    require(marker in human, f"human authority marker missing: {marker}")
for forbidden in ("ENTRY CITATION PASSES COMPLETE = 18 / 18", "WHOLE-BOOK CITATION PASS = COMPLETE", "PRODUCT RELEASE = COMPLETE", "TODO", "TBD"):
    require(forbidden not in human, f"human authority forbidden marker present: {forbidden}")

if errors:
    print(f"Heart X.2 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart X.2 entry citation pass: PASS — 16 governed Scripture locators; 26/26 Product quotation surfaces (18 Scripture, 1 confessional, 2 titles, 5 editorial/lexical); reader remains paraphrase-only; whole-book 5/18")
