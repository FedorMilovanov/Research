#!/usr/bin/env python3
"""Validate X.3 owner closure and its later paraphrase-only reader composition."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
VII = ROOT / "data/heart-vii-owner-closure-2026-08-04.json"
I4 = ROOT / "data/heart-i4-owner-closure-2026-08-04.json"
X2 = ROOT / "data/heart-x2-owner-closure-2026-08-04.json"
X3 = ROOT / "data/heart-x3-owner-closure-2026-08-04.json"
X3_READER = ROOT / "data/heart-x3-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/87_X3_CONCLUDING_HOPE_OWNER_CLOSURE_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"
BOOK = ROOT / "СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md"
R9 = ROOT / "СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md"
X2_HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/86_X2_GORIFIED_HEART_OWNER_CLOSURE_2026-08-04.md"

PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
ARTICLE_PATH = "src/content/articles/osvobozhdennoe-serdce.mdx"
ARTICLE_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
EXCLUDED_X2_SECTIONS = [
    "chetyre-sostoyaniya",
    "vopl-i-otvet",
    "ne-besplotnoe-parenie",
    "ne-sposobno-greshit",
    "pobeda-nad-vragom",
]

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)}: object required")
    return value if isinstance(value, dict) else {}


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return ""


def git(repo: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"git {' '.join(args)} failed: {exc}")
        return ""


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()

base = load(BASE)
vii = load(VII)
i4 = load(I4)
x2 = load(X2)
x3 = load(X3)
reader = load(X3_READER)

# Immutable owner-discovery chain.
require(base.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "base authority drift")
require(base.get("counts", {}).get("ownerRequired") == 4, "base gap count drift")
entries = base.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "base must contain eighteen entries")
base_x3 = next((row for row in entries if isinstance(row, dict) and row.get("id") == "HEART-BOOK-X3"), {})
require(base_x3.get("bookLabel") == "X.3 Заключительная надежда", "base X.3 label drift")
require(base_x3.get("primaryState") == "OWNER_REQUIRED", "base X.3 state drift")
require(base_x3.get("productOwner") is None and base_x3.get("researchOwners") == [], "base X.3 snapshot mutated")

require(vii.get("authorityId") == "HEART-VII-OWNER-CLOSURE-2026-08-04", "VII dependency drift")
require(vii.get("effectiveCounts", {}).get("ownerRequired") == 3, "VII gap count drift")
require(i4.get("authorityId") == "HEART-I4-OWNER-CLOSURE-2026-08-04", "I.4 dependency drift")
require(i4.get("effectiveCounts", {}).get("ownerRequired") == 2, "I.4 gap count drift")
require(x2.get("authorityId") == "HEART-X2-OWNER-CLOSURE-2026-08-04", "X.2 dependency drift")
require(x2.get("effectiveCounts", {}).get("productSourceOnly") == 8, "X.2 Product count drift")
require(x2.get("effectiveCounts", {}).get("ownerRequired") == 1, "X.2 gap count drift")
require(x2.get("remainingOwnerGaps") == ["HEART-BOOK-X3"], "X.2 gap snapshot drift")

# X.3 owner snapshot stays pre-reader-assembly.
require(x3.get("schemaVersion") == 1, "X.3 schema drift")
require(x3.get("authorityId") == "HEART-X3-OWNER-CLOSURE-2026-08-04", "X.3 authority drift")
require(x3.get("status") == "X3_PRODUCT_CONCLUSION_SECTION_ESTABLISHED_FINAL_BOOK_ASSEMBLY_AND_CITATION_PASS_OPEN", "X.3 status drift")
require(x3.get("generatedAt") == x3.get("lastVerifiedAt") == "2026-08-04", "X.3 date drift")
require(x3.get("researchSnapshot") == "17a573f1791e7bcdf314be0f40593c13ef60b8d4", "X.3 Research snapshot drift")
require(x3.get("productSnapshot") == {
    "repository": "FedorMilovanov/gb-is-my-strength",
    "commit": PRODUCT_COMMIT,
    "articleOwner": {"path": ARTICLE_PATH, "blobSha": ARTICLE_BLOB},
}, "X.3 Product snapshot drift")

override = x3.get("entryOverride", {})
require(override.get("id") == "HEART-BOOK-X3", "X.3 ID drift")
require(override.get("bookLabel") == "X.3 Заключительная надежда", "X.3 label drift")
require(override.get("previousPrimaryState") == "OWNER_REQUIRED", "X.3 previous state drift")
require(override.get("effectivePrimaryState") == "PRODUCT_SECTION_ONLY", "X.3 owner state drift")
require(override.get("primaryProductOwner") == {
    "id": "osvobozhdennoe",
    "slug": "osvobozhdennoe-serdce",
    "minutes": 27,
    "sourcePath": ARTICLE_PATH,
    "sourceBlobSha": ARTICLE_BLOB,
    "sectionId": "vyhod",
    "sectionTitle": "Выход: сердце, наконец успокоенное",
    "role": "book-level conclusion from the whole journey of the heart to the face of God and final hope",
}, "X.3 Product section owner drift")
require(override.get("excludedSiblingSections") == EXCLUDED_X2_SECTIONS, "X.3 X.2 exclusion drift")
require(override.get("researchOwners") == [
    "СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md",
    "СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md",
    "СЕРИЯ СЕРДЦЕ/86_X2_GORIFIED_HEART_OWNER_CLOSURE_2026-08-04.md",
], "X.3 Research owner drift")
require(override.get("effectiveCitationState") == "PRODUCT_SECTION_CITATION_PASS_REQUIRED", "X.3 citation state drift")
require(override.get("manuscriptState") == "CONCLUSION_SECTION_SELECTED_FINAL_BOOK_CONCLUSION_NOT_ASSEMBLED", "X.3 historical manuscript state drift")
require(len(str(override.get("dedupOwner", ""))) >= 380, "X.3 dedup boundary too weak")
require(len(override.get("supportBoundary", {}).get("supports", [])) == 5, "X.3 support set drift")
require(len(override.get("supportBoundary", {}).get("doesNotSupport", [])) == 7, "X.3 non-support set drift")
require(x3.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 8,
    "productSectionOnly": 1,
    "researchDossierOnly": 6,
    "ownerRequired": 0,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "selectedProductSatelliteItems": 4,
    "selectedProductSectionOwners": 1,
    "uniqueProductPagesMapped": 9,
    "newDirectQuotesApproved": 0,
}, "X.3 owner count drift")
require(x3.get("remainingOwnerGaps") == [], "X.3 owner gaps must remain empty")
require(x3.get("publicationBoundary") == {
    "allEighteenEntriesOwnerMapped": True,
    "x3ConclusionSectionSelected": True,
    "x3FinalBookConclusionAssembled": False,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "X.3 owner publication boundary drift")

# Later reader transaction advances current state without mutating owner history.
require(reader.get("authorityId") == "HEART-X3-READER-ASSEMBLY-2026-08-04", "X.3 reader composition authority missing")
require(reader.get("ownerAuthorityId") == x3.get("authorityId"), "X.3 reader/owner mismatch")
require(reader.get("effectivePrimaryState") == {
    "entryId": "HEART-BOOK-X3",
    "previous": "PRODUCT_SECTION_ONLY",
    "current": "ASSEMBLED_READER",
    "sourceBackedByProductSection": True,
}, "X.3 reader state composition drift")
require(reader.get("effectiveCounts", {}).get("assembledReader") == 4, "X.3 current assembled-reader count drift")
require(reader.get("effectiveCounts", {}).get("productSourceOnly") == 8, "X.3 current Product-source count drift")
require(reader.get("effectiveCounts", {}).get("productSectionOnly") == 0, "X.3 current Product-section primary count drift")
require(reader.get("effectiveCounts", {}).get("researchDossierOnly") == 6, "X.3 current dossier count drift")
require(reader.get("effectiveCounts", {}).get("ownerRequired") == 0, "X.3 current owner-gap drift")
require(reader.get("effectiveCounts", {}).get("sourceBackedByProductSection") == 1, "X.3 source-backed reader count drift")
require(reader.get("publicationBoundary", {}).get("x3FinalBookConclusionAssembled") is True, "X.3 reader assembly not closed")
require(reader.get("publicationBoundary", {}).get("wholeBookReaderAssemblyComplete") is False, "whole-book reader boundary drift")
require(reader.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book citation boundary drift")
require(reader.get("publicationBoundary", {}).get("productReleaseComplete") is False, "Product release boundary drift")

# Exact Product section still controls the reader source.
require(product_root.is_dir(), "Product checkout missing")
require(git(product_root, "rev-parse", "HEAD") == PRODUCT_COMMIT, "Product checkout head drift")
require(git(product_root, "hash-object", ARTICLE_PATH) == ARTICLE_BLOB, "Product article blob drift")
article = read(product_root / ARTICLE_PATH)
start_marker = '<h2 id="vyhod">Выход: сердце, наконец успокоенное</h2>'
end_marker = '<h2 id="istochniki">Источники и сверка</h2>'
require(start_marker in article and end_marker in article, "X.3 Product section boundary missing")
if start_marker in article and end_marker in article:
    conclusion = article[article.index(start_marker):article.index(end_marker)]
else:
    conclusion = ""
for marker in (
    "И вот последнее, к чему шла вся серия.",
    "Мы начали с сердца испорченного и лукавого",
    "увидели Христа, Который несёт немощных",
    "не к бесконечному самокопанию, а к лицу Божьему",
    "Здесь — война. Там — Он. И этого довольно, чтобы держаться.",
):
    require(marker in conclusion, f"X.3 Product conclusion marker missing: {marker}")
for section in EXCLUDED_X2_SECTIONS:
    require(f'id="{section}"' not in conclusion, f"X.2 section leaked into X.3: {section}")

# Human owner snapshot and source authorities remain intact.
book = read(BOOK)
r9 = read(R9)
x2_human = read(X2_HUMAN)
human = read(HUMAN)
require("18. X.3 — Заключительная надежда." in book, "X.3 final order missing")
require("FINAL ORDER = CLOSED" in book, "final-order closure missing")
require("WHOLE-BOOK CITATION/REFERENCE PASS = OPEN" in book, "citation boundary missing")
require("# R9 — Христос Откровения" in r9 and "испытующий сердца" in r9, "R9 boundary missing")
require("X.3 OWNER = OPEN" in x2_human, "X.2 historical gap marker missing")
require("The final `vyhod` section is not silently absorbed into X.2" in x2_human, "X.2 withholding marker missing")
for marker in (
    "HEART-X3-OWNER-CLOSURE-2026-08-04",
    "X.3 CONCLUSION SECTION OWNER = CLOSED",
    "PRODUCT SECTION = osvobozhdennoe-serdce#vyhod",
    "ALL 18 ENTRIES OWNER-MAPPED = TRUE",
    "STANDALONE OWNER GAPS = 0",
    "FINAL-BOOK X.3 MANUSCRIPT = NOT ASSEMBLED",
    ARTICLE_BLOB,
):
    require(marker in human, f"X.3 owner human marker missing: {marker}")

# Current authority records both transaction history and current reader state.
current = read(CURRENT)
for marker in (
    "X.3 CONCLUSION SECTION OWNER = CLOSED",
    "ALL 18 ENTRIES OWNER-MAPPED = TRUE",
    "ASSEMBLED READER OWNERS = 4",
    "PRODUCT SOURCE OWNERS = 8",
    "CURRENT PRIMARY PRODUCT SECTION OWNERS = 0",
    "SOURCE-BACKED PRODUCT SECTION READERS = 1",
    "STANDALONE OWNER GAPS = 0",
    "FINAL-BOOK X.3 MANUSCRIPT = ASSEMBLED",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
):
    require(marker in current, f"current X.3 composition marker missing: {marker}")
require("AFTER X.3 OWNER OVERLAY:" in current, "X.3 owner ledger heading missing")
require("PRODUCT SECTION OWNERS = 1" in current, "X.3 historical section count missing")
require("FINAL-BOOK X.3 MANUSCRIPT = NOT ASSEMBLED" in current, "X.3 historical manuscript marker missing")
require("AFTER X.3 READER ASSEMBLY / CURRENT:" in current, "X.3 reader ledger heading missing")

gap_section = current.split("### Manuscript owner gaps", 1)[-1].split("### Dossier-to-reader assembly", 1)[0]
require("NONE / CLOSED" in gap_section, "current zero-gap marker missing")
for entry in (
    "I.4 `Внутренний человек и телесная жизнь`",
    "VII `Сердце в страдании и унынии`",
    "X.2 `Освобождённое сердце`",
    "X.3 `Заключительная надежда`",
):
    require(entry not in gap_section, f"closed entry remains in gap section: {entry}")
for forbidden in (
    "WHOLE-BOOK CITATION PASS = CLOSED",
    "WHOLE-BOOK LINE EDIT = CLOSED",
    "MANUSCRIPT BUNDLE = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "NEW DIRECT QUOTES = 1",
    "TODO",
    "TBD",
):
    require(forbidden not in current, f"current authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.3 owner closure: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart X.3 owner closure: PASS — owner snapshot preserved; paraphrase-only reader advances current state to 4 assembled readers")
