#!/usr/bin/env python3
"""Validate the final Heart X.3 conclusion-section owner overlay."""
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

# Historical overlay chain must remain immutable and monotonic.
require(base.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "base authority drift")
require(base.get("counts", {}).get("ownerRequired") == 4, "base gap count drift")
entries = base.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "base must contain eighteen entries")
base_x3 = next((row for row in entries if isinstance(row, dict) and row.get("id") == "HEART-BOOK-X3"), {})
require(base_x3.get("bookLabel") == "X.3 Заключительная надежда", "base X.3 label drift")
require(base_x3.get("primaryState") == "OWNER_REQUIRED", "base X.3 historical state drift")
require(base_x3.get("productOwner") is None and base_x3.get("researchOwners") == [], "base X.3 snapshot mutated")

require(vii.get("authorityId") == "HEART-VII-OWNER-CLOSURE-2026-08-04", "VII dependency drift")
require(vii.get("effectiveCounts", {}).get("ownerRequired") == 3, "VII gap count drift")
require(i4.get("authorityId") == "HEART-I4-OWNER-CLOSURE-2026-08-04", "I.4 dependency drift")
require(i4.get("effectiveCounts", {}).get("ownerRequired") == 2, "I.4 gap count drift")
require(x2.get("authorityId") == "HEART-X2-OWNER-CLOSURE-2026-08-04", "X.2 dependency drift")
require(x2.get("effectiveCounts", {}).get("productSourceOnly") == 8, "X.2 Product count drift")
require(x2.get("effectiveCounts", {}).get("ownerRequired") == 1, "X.2 gap count drift")
require(x2.get("remainingOwnerGaps") == ["HEART-BOOK-X3"], "X.2 remaining-gap snapshot drift")
require(x2.get("publicationBoundary", {}).get("x2SourceOwnerClosed") is True, "X.2 owner not closed")
require(x2.get("publicationBoundary", {}).get("x2UnifiedReaderAssembled") is False, "X.2 reader boundary drift")

# X.3 overlay contract.
require(x3.get("schemaVersion") == 1, "X.3 schema drift")
require(x3.get("authorityId") == "HEART-X3-OWNER-CLOSURE-2026-08-04", "X.3 authority drift")
require(x3.get("status") == "X3_PRODUCT_CONCLUSION_SECTION_ESTABLISHED_FINAL_BOOK_ASSEMBLY_AND_CITATION_PASS_OPEN", "X.3 status drift")
require(x3.get("generatedAt") == x3.get("lastVerifiedAt") == "2026-08-04", "X.3 date drift")
require(x3.get("baseAuthorityId") == base.get("authorityId"), "X.3 base authority mismatch")
require(x3.get("baseAuthority") == "data/heart-whole-book-integration-2026-08-04.json", "X.3 base path drift")
require(x3.get("dependsOnOverlays") == [
    "data/heart-vii-owner-closure-2026-08-04.json",
    "data/heart-i4-owner-closure-2026-08-04.json",
    "data/heart-x2-owner-closure-2026-08-04.json",
], "X.3 dependency order drift")
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
require(override.get("effectivePrimaryState") == "PRODUCT_SECTION_ONLY", "X.3 effective state drift")
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
require(override.get("excludedSiblingSections") == EXCLUDED_X2_SECTIONS, "X.3 excluded X.2 section set drift")
require(override.get("researchOwners") == [
    "СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md",
    "СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md",
    "СЕРИЯ СЕРДЦЕ/86_X2_GORIFIED_HEART_OWNER_CLOSURE_2026-08-04.md",
], "X.3 Research owner set drift")
require(override.get("effectiveCitationState") == "PRODUCT_SECTION_CITATION_PASS_REQUIRED", "X.3 citation state drift")
require(override.get("manuscriptState") == "CONCLUSION_SECTION_SELECTED_FINAL_BOOK_CONCLUSION_NOT_ASSEMBLED", "X.3 manuscript state drift")
require(len(str(override.get("dedupOwner", ""))) >= 380, "X.3 dedup boundary too weak")

boundary = override.get("supportBoundary", {})
require(len(boundary.get("supports", [])) == 5, "X.3 support set drift")
require(len(boundary.get("doesNotSupport", [])) == 7, "X.3 non-support set drift")
require("the five positive-glorification sections already assigned to X.2 belong to X.3" in boundary.get("doesNotSupport", []), "X.2/X.3 section exclusion missing")
require("the final eighteen-entry manuscript bundle is complete" in boundary.get("doesNotSupport", []), "X.3 manuscript negative boundary missing")

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
}, "X.3 effective count drift")
require(x3.get("remainingOwnerGaps") == [], "X.3 remaining gap set must be empty")
require(x3.get("publicationBoundary") == {
    "allEighteenEntriesOwnerMapped": True,
    "x3ConclusionSectionSelected": True,
    "x3FinalBookConclusionAssembled": False,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "X.3 publication boundary drift")

# Exact Product section extraction and boundaries.
require(product_root.is_dir(), "Product checkout missing")
require(git(product_root, "rev-parse", "HEAD") == PRODUCT_COMMIT, "Product checkout head drift")
require(git(product_root, "hash-object", ARTICLE_PATH) == ARTICLE_BLOB, "Product article blob drift")
article = read(product_root / ARTICLE_PATH)
start_marker = '<h2 id="vyhod">Выход: сердце, наконец успокоенное</h2>'
end_marker = '<h2 id="istochniki">Источники и сверка</h2>'
require(start_marker in article, "X.3 section start missing")
require(end_marker in article, "X.3 section end missing")
if start_marker in article and end_marker in article:
    start = article.index(start_marker)
    end = article.index(end_marker)
    require(start < end, "X.3 section ordering drift")
    conclusion = article[start:end]
else:
    conclusion = ""
for marker in (
    "И вот последнее, к чему шла вся серия.",
    "Мы начали с сердца испорченного и лукавого",
    "прошли через новое рождение, войну двух природ, идолов, искушения, страхи, тьму",
    "увидели Христа, Который несёт немощных",
    "не к бесконечному самокопанию, а к лицу Божьему",
    "не к вечной тревоге, а к вечному насыщению",
    "Здесь — война. Там — Он. И этого довольно, чтобы держаться.",
):
    require(marker in conclusion, f"X.3 Product conclusion marker missing: {marker}")
for section in EXCLUDED_X2_SECTIONS:
    require(f'id="{section}"' not in conclusion, f"X.2 section leaked into X.3 conclusion: {section}")
require('id="istochniki"' not in conclusion, "sources section leaked into X.3 conclusion")

# Research authority chain.
book = read(BOOK)
r9 = read(R9)
x2_human = read(X2_HUMAN)
require("**Authority ID:** `HEART-READER-ASSEMBLY-2026-08-02`" in book, "book assembly authority marker missing")
require("18. X.3 — Заключительная надежда." in book, "X.3 final-order marker missing")
require("FINAL ORDER = CLOSED" in book, "final-order closure marker missing")
require("WHOLE-BOOK CITATION/REFERENCE PASS = OPEN" in book, "book citation boundary missing")
require("# R9 — Христос Откровения" in r9, "R9 authority title missing")
require("Тот же Христос" in r9, "R9 same-Christ boundary missing")
require("испытующий сердца" in r9, "R9 heart-testing Christ marker missing")
require("X.3 OWNER = OPEN" in x2_human, "X.2 historical X.3 gap marker missing")
require("The final `vyhod` section is not silently absorbed into X.2" in x2_human, "X.2/X.3 withholding marker missing")

# Human/current status must show complete mapping without claiming assembly/release.
human = read(HUMAN)
current = read(CURRENT)
for marker in (
    "HEART-X3-OWNER-CLOSURE-2026-08-04",
    "X.3 CONCLUSION SECTION OWNER = CLOSED",
    "PRODUCT SECTION = osvobozhdennoe-serdce#vyhod",
    "ALL 18 ENTRIES OWNER-MAPPED = TRUE",
    "STANDALONE OWNER GAPS = 0",
    "FINAL-BOOK X.3 MANUSCRIPT = NOT ASSEMBLED",
    ARTICLE_BLOB,
):
    require(marker in human, f"X.3 human authority marker missing: {marker}")
for marker in (
    "X.3 CONCLUSION SECTION OWNER = CLOSED",
    "PRODUCT SOURCE OWNERS = 8",
    "PRODUCT SECTION OWNERS = 1",
    "STANDALONE OWNER GAPS = 0",
    "ALL 18 ENTRIES OWNER-MAPPED = TRUE",
    "FINAL-BOOK X.3 MANUSCRIPT = NOT ASSEMBLED",
):
    require(marker in current, f"current authority X.3 marker missing: {marker}")
gap_section = current.split("### Manuscript owner gaps", 1)[-1].split("### Dossier-to-reader assembly", 1)[0]
require("NONE / CLOSED" in gap_section, "current zero-gap marker missing")
for entry in (
    "I.4 `Внутренний человек и телесная жизнь`",
    "VII `Сердце в страдании и унынии`",
    "X.2 `Освобождённое сердце`",
    "X.3 `Заключительная надежда`",
):
    require(entry not in gap_section, f"closed entry remains in current gap section: {entry}")

for text, name in ((human, "human"), (current, "current")):
    for forbidden in (
        "FINAL-BOOK X.3 MANUSCRIPT = ASSEMBLED",
        "WHOLE-BOOK CITATION PASS = CLOSED",
        "WHOLE-BOOK LINE EDIT = CLOSED",
        "MANUSCRIPT BUNDLE = COMPLETE",
        "PRODUCT RELEASE = COMPLETE",
        "NEW DIRECT QUOTES = 1",
        "TODO",
        "TBD",
    ):
        require(forbidden not in text, f"{name} authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.3 owner closure: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart X.3 owner closure: PASS — all 18 entries owner-mapped, 0 gaps, final-book assembly/citation/line-edit/Product release open")
