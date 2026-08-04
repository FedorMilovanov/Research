#!/usr/bin/env python3
"""Validate the paraphrase-only III.2 regeneration reader assembly."""
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
RECEIPT = ROOT / "data/heart-iii2-reader-assembly-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/121_READER_CHAPTER_III2_REGENERATION_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/122_III2_READER_ASSEMBLY_2026-08-04.md"
EXEGESIS = ROOT / "СЕРИЯ СЕРДЦЕ/62_R1_REGENERATION_EXEGESIS.md"
SYSTEMATICS = ROOT / "СЕРИЯ СЕРДЦЕ/63_R1_REGENERATION_SYSTEMATICS.md"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v7-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"

EXPECTED_BLOBS = {
    EXEGESIS: "d75117cf00cf0bb859fc40a67a26dca4c039ec57",
    SYSTEMATICS: "143b3477792f52a9fa5721431ff64e7ffb2a4d5a",
    CURRENT: "86c932764ca2eba3bec726876f2cb73a0c78e762",
    INTEGRATION: "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
    READER: "a3f66d265cd66eff7187dcd5c511faf645833988",
}
READER_SHA256 = "10cf0d7cc4ed548280ebd06c02b240f173fa06a3948b22616652e697c7626437"
REQUIRED_HEADINGS = [
    "Не исправление, а рождение",
    "Рождение свыше и начало жизни",
    "Мёртвые оживают по благодати",
    "Дух действует суверенно",
    "Слово как установленное средство",
    "Порядок без разрыва",
    "Вера как первый живой ответ",
    "Баня возрождения и крещальный вопрос",
    "Плоды новой жизни",
    "Пастырская проверка",
    "Границы III.2",
    "Переход",
]
EXPECTED_IMMUTABLE = {
    "currentV7": [str(CURRENT.relative_to(ROOT)), EXPECTED_BLOBS[CURRENT]],
    "wholeBookIntegration": [str(INTEGRATION.relative_to(ROOT)), EXPECTED_BLOBS[INTEGRATION]],
    "historicalTriage": [str(TRIAGE.relative_to(ROOT)), EXPECTED_BLOBS[TRIAGE]],
    "inventoryBuilder": [str(BUILDER.relative_to(ROOT)), EXPECTED_BLOBS[BUILDER]],
}
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "assembledReaders": 11,
    "missingStandaloneFinalReaders": 7,
    "entryCitationPassComplete": 10,
    "entryCitationPassOpen": 8,
    "assembledReaderCitationReviewsComplete": 10,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 15,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}
errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be an object")
    return value if isinstance(value, dict) else {}


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[.–—-][A-Za-zА-Яа-яЁё0-9]+)*", text))


def normalize(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


def qcount(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable witness missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable witness blob drift: {path.relative_to(ROOT)}")

texts = {
    EXEGESIS: EXEGESIS.read_text(encoding="utf-8"),
    SYSTEMATICS: SYSTEMATICS.read_text(encoding="utf-8"),
    READER: READER.read_text(encoding="utf-8"),
}
require(sha256(texts[READER]) == READER_SHA256, "III.2 reader SHA-256 drift")

receipt = read_json(RECEIPT)
current = read_json(CURRENT)
integration = read_json(INTEGRATION)
triage = read_json(TRIAGE)

exe_scan = module.scan_owner(module.r(str(EXEGESIS.relative_to(ROOT)), "III.2 R1 exegesis owner"), product_root)
sys_scan = module.scan_owner(module.r(str(SYSTEMATICS.relative_to(ROOT)), "III.2 R1 systematics owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "III.2 assembled reader"), product_root)

require(exe_scan["sourceHeadings"] == [], "III.2 exegesis source-heading drift")
require(sys_scan["sourceHeadings"] == [], "III.2 systematics source-heading drift")
union_refs = sorted(set(exe_scan["scriptureReferences"]) | set(sys_scan["scriptureReferences"]), key=str.casefold)
union_external = sorted(set(exe_scan["externalLinks"]) | set(sys_scan["externalLinks"]), key=str.casefold)
union_internal = sorted(set(exe_scan["internalArticleLinks"]) | set(sys_scan["internalArticleLinks"]), key=str.casefold)
require(len(union_refs) == 115, "III.2 historical Scripture union drift")
require(qcount(exe_scan) + qcount(sys_scan) == 609, "III.2 historical quotation total drift")
require(len(union_external) == 67, "III.2 historical external-link union drift")
require(len(union_internal) == 1, "III.2 historical internal-link union drift")

reader_text = texts[READER]
require(word_count(reader_text) == 1718, "III.2 reader word count drift")
require(1600 <= word_count(reader_text) <= 2200, "III.2 reader outside accepted word boundary")
require(len(reader_scan["scriptureReferences"]) == 25, "III.2 reader Scripture locator count drift")
require(qcount(reader_scan) == 0, "III.2 reader quotation surface detected")
require(len(reader_scan["externalLinks"]) == 0, "III.2 reader external link detected")
require(len(reader_scan["internalArticleLinks"]) == 0, "III.2 reader internal article link detected")
require(reader_scan["sourceHeadings"] == [], "III.2 reader source heading detected")
require(reader_scan["footnoteDefinitions"] == 0, "III.2 reader footnote detected")
for heading in REQUIRED_HEADINGS:
    require(f"## {heading}" in reader_text, f"III.2 reader heading missing: {heading}")
for marker in (
    "PARAPHRASE-ONLY",
    "ENTRY CITATION PASS OPEN",
    "Новые прямые цитаты:** `0`",
    "III.1 остановилась на Божьем обещании",
    "III.3 сохранит покаяние, сокрушение и плод обращения",
    "III.4 — жизнь, усыновление и пребывание Духа",
    "Слово не заменяет Духа, а Дух не делает Слово ненужным",
):
    require(marker in reader_text, f"III.2 reader boundary marker missing: {marker}")

reader_norm = normalize(reader_text)
for source_path in (EXEGESIS, SYSTEMATICS):
    for sentence in re.split(r"(?<=[.!?])\s+", normalize(texts[source_path])):
        sentence = sentence.strip(" -*")
        if len(sentence) >= 150:
            require(sentence not in reader_norm, f"III.2 reader copies a long sentence from {source_path.name}")

require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V7-2026-08-04", "current V7 authority drift")
require(current.get("currentCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 10,
    "entryCitationPassOpen": 8,
    "assembledReaderEntries": 10,
    "assembledReaderCitationReviewsComplete": 10,
    "missingStandaloneFinalReaders": 8,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 5,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 15,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "current V7 count block drift")
require("HEART-BOOK-III2" in current.get("openEntryIds", []), "current V7 does not retain III.2 open")
require(current.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-III2", "current V7 next-entry drift")

integration_entry = next((row for row in integration.get("entries", []) if row.get("id") == "HEART-BOOK-III2"), {})
require(integration_entry.get("order") == 7, "III.2 integration order drift")
require(integration_entry.get("primaryState") == "RESEARCH_DOSSIER_ONLY", "III.2 integration primary state drift")
require(integration_entry.get("productOwner") is None, "III.2 unexpectedly has Product owner")
require(integration_entry.get("researchOwners") == [
    str(EXEGESIS.relative_to(ROOT)),
    str(SYSTEMATICS.relative_to(ROOT)),
], "III.2 integration owner set drift")
require(
    integration_entry.get("dedupOwner") == "Owns divine causation, new birth, monergistic renewal and means; III.3 owns repentance response and fruit.",
    "III.2 integration ownership boundary drift",
)

triage_entry = next((row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-III2"), {})
require(triage_entry.get("inventoryEntrySha256") == "f5308c0ccf13e992ac19ea78801a2d5253940c89e41d73ef6b4e9c280797fb0c", "III.2 triage inventory row drift")
require(triage_entry.get("detected") == {
    "ownerSurfaces": 2,
    "sourceHeadings": 0,
    "scriptureReferences": 115,
    "externalLinks": 67,
    "internalArticleLinks": 1,
    "quotationSurfaces": 609,
}, "III.2 historical triage surface counts drift")
require(triage_entry.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "III.2 historical triage rewritten")
require(triage_entry.get("disposition", {}).get("entryCitationPassComplete") is False, "III.2 historical citation pass unexpectedly complete")

require(receipt.get("authorityId") == "HEART-III2-READER-ASSEMBLY-2026-08-04", "III.2 receipt authority drift")
require(receipt.get("status") == "III2_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_ENTRY_CITATION_PASS_OPEN", "III.2 receipt status drift")
require(receipt.get("immutableAuthorities") == EXPECTED_IMMUTABLE, "III.2 immutable authority chain drift")
require(receipt.get("entry") == {"order": 7, "id": "HEART-BOOK-III2", "label": "III.2 Рождение свыше и обновление"}, "III.2 receipt entry drift")
require(receipt.get("reader") == {
    "path": str(READER.relative_to(ROOT)),
    "gitBlob": EXPECTED_BLOBS[READER],
    "fullSha256": READER_SHA256,
    "wordCount": 1718,
    "scriptureReferences": 25,
    "quotationSurfaces": 0,
    "externalLinks": 0,
    "internalArticleLinks": 0,
    "footnoteDefinitions": 0,
    "sourceHeadings": 0,
    "newDirectQuotesApproved": 0,
}, "III.2 receipt reader block drift")
require(receipt.get("exactResearchSources") == [
    {"role": "R1_REGENERATION_EXEGESIS", "path": str(EXEGESIS.relative_to(ROOT)), "gitBlob": EXPECTED_BLOBS[EXEGESIS]},
    {"role": "R1_REGENERATION_SYSTEMATICS", "path": str(SYSTEMATICS.relative_to(ROOT)), "gitBlob": EXPECTED_BLOBS[SYSTEMATICS]},
], "III.2 receipt source witness drift")
require(receipt.get("historicalUnion") == {
    "ownerSurfaces": 2,
    "sourceHeadings": 0,
    "scriptureReferences": 115,
    "quotationSurfaces": 609,
    "externalLinks": 67,
    "internalArticleLinks": 1,
    "inventoryEntrySha256": "f5308c0ccf13e992ac19ea78801a2d5253940c89e41d73ef6b4e9c280797fb0c",
}, "III.2 receipt historical union drift")
require(receipt.get("composition") == {
    "mode": "PARAPHRASE_ONLY",
    "researchDossiersChanged": False,
    "historicalAuthoritiesChanged": False,
    "dossierQuotationSurfacesCopiedToReader": 0,
    "dossierLinksCopiedToReader": 0,
    "longExactDossierSentencesCopied": 0,
    "newHistoricalClaims": 0,
    "newDirectQuotesApproved": 0,
}, "III.2 composition boundary drift")
require(receipt.get("effectiveState") == {
    "entryId": "HEART-BOOK-III2",
    "previous": "RESEARCH_DOSSIER_ONLY",
    "current": "ASSEMBLED_READER_CITATION_OPEN",
}, "III.2 effective state drift")
require(receipt.get("effectiveCounts") == EXPECTED_COUNTS, "III.2 effective count block drift")

boundary = receipt.get("publicationBoundary", {})
require(boundary.get("iii2ReaderAssembled") is True, "III.2 reader not marked assembled")
for key in (
    "iii2EntryCitationPassComplete",
    "allCurrentlyAssembledReadersCitationReviewed",
    "wholeBookReaderAssemblyComplete",
    "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete",
    "wholeBookLineEditComplete",
    "manuscriptBundleComplete",
    "productReleaseComplete",
    "productSourceRepairsComplete",
    "dossierUrlHoldsResolved",
    "unresolvedInternalPathsResolved",
):
    require(boundary.get(key) is False, f"III.2 publication boundary weakened: {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "III.2 publication boundary quote drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-III2-READER-ASSEMBLY-2026-08-04",
    "HISTORICAL DOSSIER SURFACES = 115 / 609 / 67 / 1",
    "READER SURFACES = 25 / 0 / 0 / 0",
    "ASSEMBLED READERS = 11 / 18",
    "MISSING STANDALONE FINAL READERS = 7",
    "ENTRY CITATION PASSES COMPLETE = 10 / 18",
    "Research-dossier-only lanes: `5 → 4`",
    "III.2 ENTRY CITATION PASS = OPEN",
    "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in human, f"III.2 human authority marker missing: {marker}")
for forbidden in (
    "III.2 ENTRY CITATION PASS = COMPLETE",
    "ENTRY CITATION PASSES COMPLETE = 11 / 18",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"III.2 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart III.2 reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart III.2 reader assembly: PASS")
print("- reader: 1718 words / 25 Scripture / 0 quote-link-footnote-source surfaces")
print("- historical union: 115 Scripture / 609 quotation / 67 external / 1 internal")
print("- effective state: 11 readers assembled; III.2 citation pass remains open")
