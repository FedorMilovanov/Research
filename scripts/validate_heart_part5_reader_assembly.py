#!/usr/bin/env python3
"""Validate the bounded Part V Heart-in-war reader assembly."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v10-2026-08-09.json"
RECEIPT = ROOT / "data/heart-part5-reader-assembly-2026-08-09.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/133_READER_CHAPTER_V_HEART_IN_WAR_2026-08-09.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/134_PART5_READER_ASSEMBLY_2026-08-09.md"
R3 = ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md"
R4 = ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md"
R5 = ROOT / "СЕРИЯ СЕРДЦЕ/67_R5_TWO_STRUGGLES.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
PRODUCT_REL = Path("src/components/article-pilots/rimlyanam7/Rimlyanam7Body.astro")

EXPECTED_RESEARCH_BLOBS = {
    CURRENT: "2a34228ecb29d3181c6e23f0f761a48c3af0ebd5",
    R3: "ae55b1fad5cccbdb623c551a14222e0f51ec084a",
    R4: "f82780e13cb064aa89c06427d11a938662fc3ff8",
    R5: "846277b099e58bf36b88c2ae0dfe4e24e6bec53b",
    READER: "183819bf469d7e28f270fa6891b8ae1534e2f6ef",
}
EXPECTED_PRODUCT_BLOB = "35ed2f340ae725485533e322b3e1db0a68e01747"
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "assembledReaders": 14,
    "missingStandaloneFinalReaders": 4,
    "entryCitationPassComplete": 13,
    "entryCitationPassOpen": 5,
    "assembledReaderCitationReviewsComplete": 13,
    "assembledReadersAwaitingCitationReview": 1,
    "productSourceOnlyEntries": 1,
    "researchDossierOnlyEntries": 3,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}
EXPECTED_HEADINGS = [
    "V. Сердце в борьбе с грехом",
    "Господство сломлено, присутствие греха осталось",
    "Почему Римлянам 7 нельзя использовать как алиби",
    "Борьба совести может быть очень серьёзной",
    "Где проходит потолок борьбы без Духа",
    "Два воина могут выглядеть наоборот",
    "Оружие показывает, на кого надеется сердце",
    "Поражение раскрывает не меньше, чем победа",
    "Победа тоже является испытанием",
    "Не всякий быстрый рост имеет корень",
    "Шесть вопросов вместо одного теста",
    "Война должна вести дальше себя",
    "Итог",
]

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


def blob(root: Path, rel: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(rel)], cwd=root, text=True).strip()


def words(text: str) -> list[str]:
    return re.findall(r"[0-9A-Za-zА-Яа-яЁё]+(?:[-–][0-9A-Za-zА-Яа-яЁё]+)*", text)


def normalized_sentences(text: str) -> set[str]:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text)
    out: set[str] = set()
    for chunk in chunks:
        normalized = " ".join(w.lower() for w in words(chunk))
        if len(normalized.split()) >= 16:
            out.add(normalized)
    return out


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", required=True)
args = parser.parse_args()
product_root = Path(args.product_root).resolve()
product_source = product_root / PRODUCT_REL

for path, expected in EXPECTED_RESEARCH_BLOBS.items():
    require(path.is_file(), f"missing pinned Research file: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(ROOT, path.relative_to(ROOT)) == expected, f"Research blob drift: {path.relative_to(ROOT)}")
require(product_source.is_file(), f"missing pinned Product source: {PRODUCT_REL}")
if product_source.is_file():
    require(blob(product_root, PRODUCT_REL) == EXPECTED_PRODUCT_BLOB, "pinned Product Romans 7 owner blob drift")

current = read_json(CURRENT)
receipt = read_json(RECEIPT)
reader = READER.read_text(encoding="utf-8") if READER.is_file() else ""

# V10 remains the citation authority while this transaction only assembles Part V.
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V10-2026-08-09", "current V10 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 13, "V10 citation-complete count drift")
require(current.get("currentCounts", {}).get("assembledReaderEntries") == 13, "V10 pre-assembly reader count drift")
require(current.get("currentCounts", {}).get("dossierUrlHoldsRetained") == 55, "V10 retained HOLD count drift")
require(current.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-V", "V10 no longer assigns Part V next")

require(receipt.get("authorityId") == "HEART-PART5-READER-ASSEMBLY-2026-08-09", "Part V receipt authority drift")
require(receipt.get("status") == "PART5_STANDALONE_READER_ASSEMBLED_CITATION_PASS_OPEN", "Part V receipt status drift")
entry = receipt.get("entry", {})
require(entry.get("id") == "HEART-BOOK-V" and entry.get("order") == 11, "Part V entry identity/order drift")
require(entry.get("previousState") == "PRODUCT_SOURCE_ONLY", "Part V previous state drift")
require(entry.get("currentState") == "ASSEMBLED_READER_CITATION_OPEN", "Part V current state drift")

primary = receipt.get("sourceOwners", {}).get("primaryProduct", {})
require(primary.get("path") == str(PRODUCT_REL), "Part V primary Product path drift")
require(primary.get("gitBlob") == EXPECTED_PRODUCT_BLOB, "Part V primary Product blob drift")
support = receipt.get("sourceOwners", {}).get("boundedResearchSupport", [])
support_pairs = {(item.get("path"), item.get("gitBlob")) for item in support if isinstance(item, dict)}
require(support_pairs == {
    (str(R3.relative_to(ROOT)), EXPECTED_RESEARCH_BLOBS[R3]),
    (str(R4.relative_to(ROOT)), EXPECTED_RESEARCH_BLOBS[R4]),
    (str(R5.relative_to(ROOT)), EXPECTED_RESEARCH_BLOBS[R5]),
}, "Part V bounded Research support set drift")

reader_meta = receipt.get("reader", {})
require(reader_meta.get("path") == str(READER.relative_to(ROOT)), "Part V reader path drift")
require(reader_meta.get("gitBlob") == EXPECTED_RESEARCH_BLOBS[READER], "Part V reader blob drift")
require(reader_meta.get("minimumWords") == 1800, "Part V minimum word boundary drift")
for key in ("quotationSurfaces", "externalLinks", "internalArticleLinks", "footnoteDefinitions", "sourceQuotationTransfer", "sourceLinkTransfer", "newDirectQuotesApproved"):
    require(reader_meta.get(key) == 0, f"Part V reader must keep {key}=0")

# Reader must be a real standalone chapter, not a short bridge or source dump.
word_count = len(words(reader))
require(word_count >= 1800, f"Part V reader too short: {word_count} words < 1800")
require(word_count <= 4200, f"Part V reader unexpectedly expanded beyond bounded assembly: {word_count} words")
headings = [m.group(1).strip() for m in re.finditer(r"^#{1,2}\s+(.+?)\s*$", reader, re.MULTILINE)]
require(headings == EXPECTED_HEADINGS, "Part V reader heading/order drift")

# Assembly is paraphrase-only. Historical citation/link surfaces stay in source owners for the next pass.
require(not re.search(r"https?://|www\.", reader, re.IGNORECASE), "Part V reader contains an external URL")
require(not re.search(r"\[[^\]]+\]\([^\)]+\)", reader), "Part V reader contains a Markdown link")
require(not re.search(r"^\s*>\s", reader, re.MULTILINE), "Part V reader contains a block quotation")
require(not re.search(r"\[\^[^\]]+\]", reader), "Part V reader contains a footnote marker")
require(not re.search(r"^\[\^[^\]]+\]:", reader, re.MULTILINE), "Part V reader contains a footnote definition")
require(not re.search(r"[«»“”]", reader), "Part V reader contains direct-quotation typography")
require("<" not in reader and ">" not in reader, "Part V reader must not transfer Product HTML")

# Secondary named-source material is deliberately deferred with its citation surfaces.
for forbidden in ("Августин", "Ллойд-Джонс", "Schreiner", "Шрайнер", "Moo", "Street", "Оуэн", "Эдвардс", "Мид", "Шепард", "Аллейн", "Буньян"):
    require(forbidden not in reader, f"Part V reader transferred named secondary-source material: {forbidden}")

# Fail if a long sentence was copied verbatim from any owner. This is stronger than punctuation-only checks.
reader_sentences = normalized_sentences(reader)
source_texts = [
    product_source.read_text(encoding="utf-8"),
    R3.read_text(encoding="utf-8"),
    R4.read_text(encoding="utf-8"),
    R5.read_text(encoding="utf-8"),
]
source_sentences: set[str] = set()
for text in source_texts:
    source_sentences |= normalized_sentences(text)
long_transfers = sorted(reader_sentences & source_sentences)
require(not long_transfers, f"Part V reader contains long exact sentence transfer(s): {long_transfers[:3]}")

boundary = receipt.get("assemblyBoundary", {})
for key in (
    "romans7InterpretiveDisputeNotFlattenedToOneUnqualifiedProofText",
    "moralRestraintWithoutRegenerationNotDenied",
    "visiblePerformanceNotUsedAsStandaloneSalvationTest",
    "allHistoricalQuotationSurfacesRemainOutsideReader",
    "allHistoricalExternalLinksRemainOutsideReader",
    "allSourceFootnotesRemainOutsideReader",
    "part6PhariseeExegesisNotAbsorbed",
    "citationAndLinkDispositionDeferred",
):
    require(boundary.get(key) is True, f"Part V assembly boundary missing: {key}")

require(receipt.get("effectiveCounts") == EXPECTED_COUNTS, "Part V effective-count block drift")
require(receipt.get("retainedRepairAndHoldBacklog") == {
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "part5RepairsClosedByAssembly": 0,
    "part5HoldsPromotedByAssembly": 0,
}, "Part V silently changes repair/HOLD backlog")

publication = receipt.get("publicationBoundary", {})
require(publication.get("part5ReaderAssemblyComplete") is True, "Part V reader assembly not marked complete")
require(publication.get("part5EntryCitationPassComplete") is False, "Part V assembly falsely claims citation completion")
require(publication.get("allCurrentlyAssembledReadersReviewed") is False, "Part V assembly falsely claims all readers reviewed")
for key in (
    "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete", "wholeBookTransitionDedupPassComplete",
    "wholeBookLineEditComplete", "manuscriptBundleComplete", "productReleaseComplete", "productSourceRepairsComplete",
    "dossierUrlHoldsResolved", "dossierSourceUrlRepairsComplete", "unresolvedInternalPathsResolved",
):
    require(publication.get(key) is False, f"Part V assembly falsely closes publication boundary: {key}")
require(publication.get("newDirectQuotesApproved") == 0, "Part V assembly approves new direct quotes")
require(receipt.get("nextTransaction", {}).get("type") == "ENTRY_CITATION_PASS", "Part V next transaction type drift")
require(receipt.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-V", "Part V next transaction entry drift")

require(HUMAN.is_file(), "Part V human assembly record missing")
if HUMAN.is_file():
    human = HUMAN.read_text(encoding="utf-8")
    for marker in (
        "ASSEMBLED READERS = 14 / 18",
        "ENTRY CITATION PASSES COMPLETE = 13 / 18",
        "DOSSIER URL HOLDS RETAINED = 55",
        "PART V ENTRY CITATION PASS = OPEN",
        "NEXT = HEART-BOOK-V ENTRY CITATION PASS",
        "PRODUCT RELEASE = NOT CLAIMED",
    ):
        require(marker in human, f"Part V human record missing marker: {marker}")

require(WORKFLOW.is_file(), "Heart workflow missing")
if WORKFLOW.is_file():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    require("scripts/validate_heart_part5_reader_assembly.py" in workflow, "workflow does not compile/run Part V assembly validator")
    require("Validate Part V reader assembly" in workflow, "workflow missing Part V assembly validation step")

if errors:
    print("Heart Part V reader assembly: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Heart Part V reader assembly: PASS — {word_count} words, 14/18 assembled, citation pass remains 13/18")
