#!/usr/bin/env python3
"""Validate the paraphrase-only III.1 final-book reader assembly."""
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
RECEIPT_PATH = ROOT / "data/heart-iii1-reader-assembly-2026-08-04.json"
READER_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/117_READER_CHAPTER_III1_NEW_HEART_PROMISE_2026-08-04.md"
HUMAN_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/118_III1_READER_ASSEMBLY_2026-08-04.md"
PRODUCT_REL = Path("src/content/articles/novoe-serdce.mdx")
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
PRODUCT_BLOB = "8d4936d6b58b380215b259a5511a8c2bfad33a46"
READER_BLOB = "f0355d4a9a451ecbe6a2256a36876839a0c4889e"
READER_SHA256 = "fd4fe3aa36e46554d105fa7277fe812337d1852ca7a475f2b91b779238fdf93f"

EXPECTED_RESEARCH_BLOBS = {
    ROOT / "data/heart-entry-citation-pass-current-v6-2026-08-04.json": "fd46d6f99a735301f2966b0e2912eb68805bdff9",
    ROOT / "data/heart-whole-book-integration-2026-08-04.json": "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json": "de4d49cada15b231dfc31058aced4ec7a25928a2",
}
EXPECTED_SECTION_ORDER = [
    "ne-radi-vas",
    "obrezanie-serdca",
    "dam-serdce-novoe",
    "ne-remont-a-rozhdenie",
    "zavet-na-serdce",
    "chto-novo-chto-net",
    "lidiya",
    "fundament",
    "tverdo-ne-dubinkoy",
    "kak-uznat",
    "vyhod",
    "istochniki",
]
PROMISE_CORE = ["ne-radi-vas", "obrezanie-serdca", "dam-serdce-novoe", "zavet-na-serdce", "vyhod"]
BOUNDED_SUPPORT = ["chto-novo-chto-net"]
RETAINED = ["ne-remont-a-rozhdenie", "lidiya", "fundament", "tverdo-ne-dubinkoy", "kak-uznat", "istochniki"]
EXPECTED_HEADINGS = [
    "Обетование звучит после суда",
    "Обещание старше Иезекииля",
    "Один заветный замысел, а не набор образов",
    "Очищение, замена и новое направление",
    "Закон, написанный внутри",
    "Послушание как плод, а не цена",
    "Не ремонт прежнего центра",
    "Обещание не становится человеческой техникой",
    "Заветная надежда для слабого сердца",
    "Место III.1 в книге",
]
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value if isinstance(value, dict) else {}


def git_blob(path: Path, repo_root: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(repo_root))],
        cwd=repo_root,
        text=True,
    ).strip()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def word_count(value: str) -> int:
    return len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[.–—-][A-Za-zА-Яа-яЁё0-9]+)*", value))


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
product_path = product_root / PRODUCT_REL

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

receipt = read_json(RECEIPT_PATH)
current_v6 = read_json(ROOT / "data/heart-entry-citation-pass-current-v6-2026-08-04.json")
integration = read_json(ROOT / "data/heart-whole-book-integration-2026-08-04.json")
triage = read_json(ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json")
reader_text = READER_PATH.read_text(encoding="utf-8")
human_text = HUMAN_PATH.read_text(encoding="utf-8")
product_text = product_path.read_text(encoding="utf-8")

for path, expected_blob in EXPECTED_RESEARCH_BLOBS.items():
    require(path.is_file(), f"immutable Research witness missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(path) == expected_blob, f"immutable Research witness blob drift: {path.relative_to(ROOT)}")

require(
    subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip() == PRODUCT_COMMIT,
    "Product checkout is not the pinned Heart snapshot",
)
require(git_blob(product_path, product_root) == PRODUCT_BLOB, "III.1 Product blob drift")
require(git_blob(READER_PATH) == READER_BLOB, "III.1 reader blob drift")
require(sha256_text(reader_text) == READER_SHA256, "III.1 reader SHA-256 drift")

full_scan = module.scan_owner(module.p(str(PRODUCT_REL), "historical full III.1 owner"), product_root)
reader_scan = module.scan_owner(
    module.r(str(READER_PATH.relative_to(ROOT)), "assembled III.1 reader"),
    product_root,
)

require(len(full_scan["scriptureReferences"]) == 30, "III.1 historical Product Scripture count drift")
require(
    full_scan["inlineQuotationSegments"] + full_scan["markdownBlockquotes"] + full_scan["htmlBlockquotes"] == 67,
    "III.1 historical Product quotation count drift",
)
require(len(full_scan["externalLinks"]) == 0, "III.1 historical Product external-link count drift")
require(len(full_scan["internalArticleLinks"]) == 4, "III.1 historical Product internal-link count drift")
require(len(full_scan["sourceHeadings"]) == 0, "III.1 historical Product source-heading count drift")

section_matches = list(re.finditer(r'<h2\s+id="([^"]+)"[^>]*>', product_text, flags=re.I))
section_order = [match.group(1) for match in section_matches]
require(section_order == EXPECTED_SECTION_ORDER, "III.1 Product H2 section order drift")
section_blocks: dict[str, str] = {}
for index, match in enumerate(section_matches):
    end = section_matches[index + 1].start() if index + 1 < len(section_matches) else len(product_text)
    section_blocks[match.group(1)] = product_text[match.start():end]

source = receipt.get("exactProductSource", {})
ownership = source.get("assemblyOwnership", {})
require(source.get("repository") == "FedorMilovanov/gb-is-my-strength", "III.1 receipt Product repository drift")
require(source.get("commit") == PRODUCT_COMMIT, "III.1 receipt Product commit drift")
require(source.get("path") == str(PRODUCT_REL), "III.1 receipt Product path drift")
require(source.get("gitBlob") == PRODUCT_BLOB, "III.1 receipt Product blob drift")
require(source.get("exactSectionOrder") == EXPECTED_SECTION_ORDER, "III.1 receipt section order drift")
require(ownership.get("promiseCore") == PROMISE_CORE, "III.1 promise-core ownership drift")
require(ownership.get("boundedSupport") == BOUNDED_SUPPORT, "III.1 bounded-support ownership drift")
require(ownership.get("retainedForAdjacentEntriesOrCitationReview") == RETAINED, "III.1 retained section boundary drift")
require(set(PROMISE_CORE + BOUNDED_SUPPORT + RETAINED) == set(EXPECTED_SECTION_ORDER), "III.1 section partition is not exhaustive")
require(not (set(PROMISE_CORE) & set(RETAINED)), "III.1 promise and retained section sets overlap")

require(word_count(reader_text) == 1791, "III.1 reader word count drift")
require(1600 <= word_count(reader_text) <= 2200, "III.1 reader outside accepted word boundary")
require(len(reader_scan["scriptureReferences"]) == 18, "III.1 reader Scripture locator count drift")
require(
    reader_scan["inlineQuotationSegments"] + reader_scan["markdownBlockquotes"] + reader_scan["htmlBlockquotes"] == 0,
    "III.1 reader quotation surface detected",
)
require(len(reader_scan["externalLinks"]) == 0, "III.1 reader external link detected")
require(len(reader_scan["internalArticleLinks"]) == 0, "III.1 reader internal article link detected")
require(reader_scan["footnoteDefinitions"] == 0, "III.1 reader footnote definition detected")
require(reader_scan["sourceHeadings"] == [], "III.1 reader source heading detected")
for heading in EXPECTED_HEADINGS:
    require(f"## {heading}" in reader_text, f"III.1 reader heading missing: {heading}")
for marker in (
    "PARAPHRASE-ONLY",
    "ENTRY CITATION PASS OPEN",
    "Новые прямые цитаты:** `0`",
    "Следующая глава отдельно разберёт причинную сторону нового рождения и обновления.",
    "Глава III.3 сохранит покаяние как ответ и плод",
    "III.4 будет говорить о жизни и усыновлении Духом",
):
    require(marker in reader_text, f"III.1 reader boundary marker missing: {marker}")

reader_normalized = normalized(reader_text).casefold()
for section_id in PROMISE_CORE + BOUNDED_SUPPORT:
    source_normalized = normalized(section_blocks[section_id]).casefold()
    for sentence in re.split(r"(?<=[.!?])\s+", source_normalized):
        sentence = sentence.strip(" -*")
        if len(sentence) >= 140:
            require(sentence not in reader_normalized, f"III.1 reader copies a long Product sentence from {section_id}")

require(receipt.get("authorityId") == "HEART-III1-READER-ASSEMBLY-2026-08-04", "III.1 receipt authority drift")
require(receipt.get("status") == "III1_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_ENTRY_CITATION_PASS_OPEN", "III.1 receipt status drift")
require(receipt.get("entry") == {"order": 6, "id": "HEART-BOOK-III1", "label": "III.1 Обещание нового сердца"}, "III.1 receipt entry drift")
require(receipt.get("reader", {}).get("path") == str(READER_PATH.relative_to(ROOT)), "III.1 receipt reader path drift")
require(receipt.get("reader", {}).get("gitBlob") == READER_BLOB, "III.1 receipt reader blob drift")
require(receipt.get("reader", {}).get("fullSha256") == READER_SHA256, "III.1 receipt reader SHA drift")
require(receipt.get("reader", {}).get("wordCount") == 1791, "III.1 receipt reader word count drift")
require(receipt.get("reader", {}).get("scriptureReferences") == 18, "III.1 receipt reader Scripture count drift")
for key in ("quotationSurfaces", "externalLinks", "internalArticleLinks", "footnoteDefinitions", "sourceHeadings", "newDirectQuotesApproved"):
    require(receipt.get("reader", {}).get(key) == 0, f"III.1 receipt reader {key} drift")
require(receipt.get("composition") == {
    "mode": "PARAPHRASE_ONLY",
    "productSourceChanged": False,
    "historicalAuthoritiesChanged": False,
    "productQuotationSurfacesCopiedToReader": 0,
    "productLinksCopiedToReader": 0,
    "longExactProductSentencesCopied": 0,
    "newHistoricalClaims": 0,
    "newDirectQuotesApproved": 0,
}, "III.1 composition boundary drift")

require(current_v6.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V6-2026-08-04", "current V6 authority drift")
v6_counts = current_v6.get("currentCounts", {})
require(v6_counts.get("entryCitationPassComplete") == 9, "current V6 completed count drift")
require(v6_counts.get("assembledReaderEntries") == 9, "current V6 reader count drift")
require(v6_counts.get("missingStandaloneFinalReaders") == 9, "current V6 backlog count drift")
require(v6_counts.get("productSourceOnlyEntries") == 4, "current V6 Product lane drift")
require(v6_counts.get("researchDossierOnlyEntries") == 5, "current V6 dossier lane drift")
require("HEART-BOOK-III1" in current_v6.get("openEntryIds", []), "current V6 does not retain III.1 as open")
require(current_v6.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-III1", "current V6 next-entry drift")

integration_entry = next((row for row in integration.get("entries", []) if row.get("id") == "HEART-BOOK-III1"), {})
require(integration_entry.get("order") == 6, "III.1 integration order drift")
require(integration_entry.get("productOwner") == {"id": "novoe", "slug": "novoe-serdce"}, "III.1 Product owner drift")
require(
    integration_entry.get("dedupOwner") == "Owns the Ezekiel 36 promise and covenant replacement motif; III.2 owns the causal new-birth exposition.",
    "III.1 integration ownership boundary drift",
)

triage_entry = next((row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-III1"), {})
require(triage_entry.get("inventoryEntrySha256") == "2c7ff62520fb4ad6844cce55a87acc53d4c41fe5bf6e75435eb2e8651cf785db", "III.1 triage inventory row drift")
require(triage_entry.get("detected") == {
    "ownerSurfaces": 1,
    "sourceHeadings": 0,
    "scriptureReferences": 30,
    "externalLinks": 0,
    "internalArticleLinks": 4,
    "quotationSurfaces": 67,
}, "III.1 triage surface counts drift")
require(triage_entry.get("disposition", {}).get("entryCitationPassComplete") is False, "historical III.1 triage unexpectedly complete")

require(receipt.get("effectiveState") == {
    "entryId": "HEART-BOOK-III1",
    "previous": "PRODUCT_SOURCE_ONLY",
    "current": "ASSEMBLED_READER_CITATION_OPEN",
}, "III.1 effective state drift")
require(receipt.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 10,
    "missingStandaloneFinalReaders": 8,
    "entryCitationPassComplete": 9,
    "entryCitationPassOpen": 9,
    "assembledReaderCitationReviewsComplete": 9,
    "productSourceOnly": 3,
    "researchDossierOnly": 5,
    "productSourceLinkRepairsRequired": 3,
    "dossierUrlHoldsRetained": 15,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "III.1 effective count drift")

boundary = receipt.get("publicationBoundary", {})
require(boundary.get("iii1ReaderAssembled") is True, "III.1 reader not marked assembled")
for key in (
    "iii1EntryCitationPassComplete",
    "allCurrentlyAssembledReadersCitationReviewed",
    "wholeBookReaderAssemblyComplete",
    "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete",
    "wholeBookLineEditComplete",
    "manuscriptBundleComplete",
    "productReleaseComplete",
    "productSourceLinkRepairsComplete",
    "dossierUrlHoldsResolved",
    "unresolvedInternalPathsResolved",
):
    require(boundary.get(key) is False, f"III.1 publication boundary weakened: {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "III.1 publication boundary direct quote drift")

for marker in (
    "HEART-III1-READER-ASSEMBLY-2026-08-04",
    "PARAPHRASE_ONLY",
    "III.1 ENTRY CITATION PASS COMPLETE = FALSE",
    "ALL CURRENT READERS REVIEWED = FALSE",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "PRODUCT RELEASE = NOT CLAIMED",
    "30 / 67 / 0 / 4",
):
    require(marker in human_text, f"III.1 human authority marker missing: {marker}")

if errors:
    print("III.1 reader assembly validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    sys.exit(1)

print("III.1 reader assembly validated")
print("- reader: 1791 words / 18 Scripture locators / 0 quote-link-footnote surfaces")
print("- Product owner: 30 Scripture / 67 quotation / 0 external / 4 internal")
print("- state: 10 readers assembled; III.1 citation pass remains open")
