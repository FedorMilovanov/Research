#!/usr/bin/env python3
"""Validate the Heart chapter I.4 source-owner closure overlay."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
VII = ROOT / "data/heart-vii-owner-closure-2026-08-04.json"
I4 = ROOT / "data/heart-i4-owner-closure-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/85_I4_INNER_PERSON_AND_EMBODIED_LIFE_OWNER_CLOSURE_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"
V81 = ROOT / "СЕРИЯ СЕРДЦЕ/60_V81_JAY_ADAMS_PRIMARY_SOURCE_DEEPENING.md"
V82 = ROOT / "СЕРИЯ СЕРДЦЕ/61_V82_PSYCHOTROPIC_MEDICATION_BODY_SOUL_BIBLICAL_COUNSELING.md"

PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
CORE_PATH = "src/components/article-pilots/_shared/heartSeriesData.ts"
CORE_BLOB = "553adbd67a459fa9e022f00b924e8c20201bf400"
SATELLITE_PATH = "src/components/article-pilots/_shared/series/hardTextsSeriesConfig.ts"
SATELLITE_BLOB = "152c90b2dcee67d1683289445d0d2239905ed41c"
EXPECTED_RESEARCH_OWNERS = [
    "СЕРИЯ СЕРДЦЕ/60_V81_JAY_ADAMS_PRIMARY_SOURCE_DEEPENING.md",
    "СЕРИЯ СЕРДЦЕ/61_V82_PSYCHOTROPIC_MEDICATION_BODY_SOUL_BIBLICAL_COUNSELING.md",
]

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: root object required")
        return {}
    return value


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return ""


def run_git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"git -C {repo} {' '.join(args)} failed: {exc}")
        return ""
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-root", type=Path, required=True)
    return parser.parse_args()


args = parse_args()
product_root = args.product_root.resolve()
base = load(BASE)
vii = load(VII)
i4 = load(I4)

require(base.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "base authority drift")
require(base.get("counts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 5,
    "researchDossierOnly": 6,
    "ownerRequired": 4,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "newDirectQuotesApproved": 0,
}, "base count snapshot drift")
entries = base.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "base must contain eighteen entries")
base_i4 = next((row for row in entries if isinstance(row, dict) and row.get("id") == "HEART-BOOK-I4"), None)
require(isinstance(base_i4, dict), "base I.4 entry missing")
if isinstance(base_i4, dict):
    require(base_i4.get("bookLabel") == "I.4 Внутренний человек и телесная жизнь", "base I.4 label drift")
    require(base_i4.get("primaryState") == "OWNER_REQUIRED", "base I.4 historical state drift")
    require(base_i4.get("productOwner") is None, "base I.4 must remain pre-overlay snapshot")
    require(base_i4.get("supportingProductOwner") == {
        "id": "prolog",
        "slug": "chto-bibliya-nazyvaet-serdcem",
    }, "base I.4 supporting owner drift")
    require(base_i4.get("researchOwners") == [], "base I.4 historical Research owner set drift")

require(vii.get("authorityId") == "HEART-VII-OWNER-CLOSURE-2026-08-04", "VII dependency authority drift")
require(vii.get("effectiveCounts", {}).get("productSourceOnly") == 6, "VII dependency Product count drift")
require(vii.get("effectiveCounts", {}).get("ownerRequired") == 3, "VII dependency owner-gap count drift")
require(vii.get("remainingOwnerGaps") == ["HEART-BOOK-I4", "HEART-BOOK-X2", "HEART-BOOK-X3"], "VII dependency gap set drift")
require(vii.get("publicationBoundary", {}).get("viiSourceOwnerClusterClosed") is True, "VII dependency not closed")
require(vii.get("publicationBoundary", {}).get("viiUnifiedReaderAssembled") is False, "VII dependency reader boundary drift")

require(i4.get("schemaVersion") == 1, "I.4 overlay schema drift")
require(i4.get("authorityId") == "HEART-I4-OWNER-CLOSURE-2026-08-04", "I.4 authority drift")
require(i4.get("status") == "I4_PRODUCT_SOURCE_CLUSTER_ESTABLISHED_UNIFIED_READER_AND_BOOK_CITATION_PASS_OPEN", "I.4 status drift")
require(i4.get("generatedAt") == "2026-08-04", "I.4 generated date drift")
require(i4.get("lastVerifiedAt") == "2026-08-04", "I.4 verification date drift")
require(i4.get("baseAuthorityId") == base.get("authorityId"), "I.4 base authority mismatch")
require(i4.get("baseAuthority") == "data/heart-whole-book-integration-2026-08-04.json", "I.4 base path drift")
require(i4.get("dependsOnOverlays") == ["data/heart-vii-owner-closure-2026-08-04.json"], "I.4 overlay dependency drift")
require(i4.get("researchSnapshot") == "6f73c5f0e32565e5df668f840a4eb513fdd50f83", "I.4 Research snapshot drift")

snapshot = i4.get("productSnapshot", {})
require(snapshot.get("repository") == "FedorMilovanov/gb-is-my-strength", "I.4 Product repository drift")
require(snapshot.get("commit") == PRODUCT_COMMIT, "I.4 Product commit drift")
require(snapshot.get("coreRegistry") == {"path": CORE_PATH, "blobSha": CORE_BLOB}, "I.4 core registry drift")
require(snapshot.get("satelliteRegistry") == {"path": SATELLITE_PATH, "blobSha": SATELLITE_BLOB}, "I.4 satellite registry drift")

override = i4.get("entryOverride", {})
require(override.get("id") == "HEART-BOOK-I4", "I.4 override ID drift")
require(override.get("bookLabel") == "I.4 Внутренний человек и телесная жизнь", "I.4 override label drift")
require(override.get("previousPrimaryState") == "OWNER_REQUIRED", "I.4 previous state drift")
require(override.get("effectivePrimaryState") == "PRODUCT_SOURCE_ONLY", "I.4 effective state drift")
require(override.get("primaryProductOwner") == {
    "id": "telo",
    "slug": "serdce-i-telo",
    "minutes": 23,
    "role": "heart-body-members-habits-appetites primary source",
}, "I.4 primary Product owner drift")
require(override.get("supportingProductOwners") == [{
    "id": "prolog",
    "slug": "chto-bibliya-nazyvaet-serdcem",
    "minutes": 39,
    "role": "whole-person biblical-heart definition support",
}], "I.4 supporting Product owner drift")
require(override.get("researchOwners") == EXPECTED_RESEARCH_OWNERS, "I.4 Research owner set drift")
for owner in EXPECTED_RESEARCH_OWNERS:
    require((ROOT / owner).is_file(), f"I.4 Research owner missing: {owner}")
require(override.get("effectiveCitationState") == "PRODUCT_SOURCE_CITATION_PASS_REQUIRED", "I.4 citation state drift")
require(override.get("manuscriptState") == "SOURCE_CLUSTER_SELECTED_UNIFIED_READER_NOT_ASSEMBLED", "I.4 manuscript state drift")
require(len(str(override.get("dedupOwner", ""))) >= 200, "I.4 dedup owner too weak")

support = override.get("supportBoundary", {})
require(isinstance(support.get("supports"), list) and len(support["supports"]) == 3, "I.4 support set drift")
require(isinstance(support.get("doesNotSupport"), list) and len(support["doesNotSupport"]) == 5, "I.4 non-support set drift")
require("historical medical claims from Adams are current clinical guidance" in support.get("doesNotSupport", []), "I.4 Adams clinical negative boundary missing")
require("a unified chapter I.4 reader manuscript is assembled" in support.get("doesNotSupport", []), "I.4 unified-reader negative boundary missing")

require(i4.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 7,
    "researchDossierOnly": 6,
    "ownerRequired": 2,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "selectedProductSatelliteItems": 3,
    "newDirectQuotesApproved": 0,
}, "I.4 effective counts drift")
require(i4.get("remainingOwnerGaps") == ["HEART-BOOK-X2", "HEART-BOOK-X3"], "I.4 remaining gap set drift")
require(i4.get("publicationBoundary") == {
    "i4SourceOwnerClusterClosed": True,
    "i4UnifiedReaderAssembled": False,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "I.4 publication boundary drift")
require("supersedes" in str(i4.get("supersessionRule", "")), "I.4 supersession rule missing")

require(product_root.is_dir(), f"Product checkout missing: {product_root}")
require(run_git(product_root, "rev-parse", "HEAD") == PRODUCT_COMMIT, "I.4 Product checkout head drift")
require(run_git(product_root, "hash-object", CORE_PATH) == CORE_BLOB, "I.4 core registry blob drift")
require(run_git(product_root, "hash-object", SATELLITE_PATH) == SATELLITE_BLOB, "I.4 satellite registry blob drift")
core_file = product_root / CORE_PATH
satellite_file = product_root / SATELLITE_PATH
require(core_file.is_file(), "I.4 core registry file missing")
require(satellite_file.is_file(), "I.4 satellite registry file missing")
core_text = core_file.read_text(encoding="utf-8") if core_file.is_file() else ""
satellite_text = satellite_file.read_text(encoding="utf-8") if satellite_file.is_file() else ""
core_pairs = set(re.findall(r"id:\s*'([^']+)'[\s\S]{0,120}?slug:\s*'([^']+)'", core_text))
satellite_pairs = set(re.findall(r"\{\s*id:\s*'([^']+)',\s*slug:\s*'([^']+)'", satellite_text))
require(("prolog", "chto-bibliya-nazyvaet-serdcem") in core_pairs, "I.4 Product prolog pair missing")
require(("telo", "serdce-i-telo") in satellite_pairs, "I.4 Product telo pair missing")
require(re.search(r"id:\s*'prolog'[\s\S]{0,220}?minutes:\s*39", core_text) is not None, "I.4 prolog minutes drift")
require(re.search(r"id:\s*'telo'[\s\S]{0,120}?minutes:\s*23", satellite_text) is not None, "I.4 telo minutes drift")

v81 = read(V81)
v82 = read(V82)
require("V81 — ДЖЕЙ АДАМС: СЕРДЦЕ, ПРИВЫЧКИ, ПОКАЯНИЕ И БИБЛЕЙСКАЯ ПЕРЕМЕНА" in v81, "V81 owner marker missing")
require("Сердце — внутренний человек, а не эмоциональная половина личности" in v81, "V81 inner-person boundary missing")
require("Ряд медицинских и психиатрических утверждений Адамса должен остаться" in v81, "V81 historical-medical boundary missing")
require("V82 — ПСИХОТРОПНЫЕ ПРЕПАРАТЫ, ТЕЛО И ДУША" in v82, "V82 owner marker missing")
require("человек создан как телесно-духовное единство" in v82, "V82 whole-person boundary missing")
require("пастор или душепопечитель без медицинской квалификации не назначает" in v82, "V82 medical-competence boundary missing")

human = read(HUMAN)
for marker in (
    "HEART-I4-OWNER-CLOSURE-2026-08-04",
    "I.4 SOURCE OWNER CLUSTER = CLOSED",
    "UNIFIED I.4 READER = NOT ASSEMBLED",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "OWNER GAPS REMAINING = 2",
    PRODUCT_COMMIT,
    CORE_BLOB,
    SATELLITE_BLOB,
    "serdce-i-telo",
    "chto-bibliya-nazyvaet-serdcem",
):
    require(marker in human, f"I.4 human authority marker missing: {marker}")

current = read(CURRENT)
for marker in (
    "HEART-CURRENT-AUTHORITY-2026-08-04",
    "I.4 SOURCE OWNER CLUSTER = CLOSED",
    "UNIFIED I.4 READER = NOT ASSEMBLED",
    "PRODUCT SOURCE OWNERS = 7",
    "STANDALONE OWNER GAPS = 2",
    "X.2 `Освобождённое сердце`",
    "X.3 `Заключительная надежда`",
):
    require(marker in current, f"current authority I.4 marker missing: {marker}")
owner_gap_section = current.split("### Manuscript owner gaps", 1)[-1].split("### Dossier-to-reader assembly", 1)[0]
require("I.4 `Внутренний человек и телесная жизнь`" not in owner_gap_section, "I.4 remains in current owner-gap list")
require("VII `Сердце в страдании и унынии`" not in owner_gap_section, "VII returned to current owner-gap list")

for path, text in ((HUMAN, human), (CURRENT, current)):
    for forbidden in (
        "I.4 SOURCE OWNER CLUSTER = OPEN",
        "UNIFIED I.4 READER = ASSEMBLED",
        "WHOLE-BOOK CITATION PASS = CLOSED",
        "PRODUCT RELEASE = COMPLETE",
        "NEW DIRECT QUOTES = 1",
        "TODO",
        "TBD",
    ):
        require(forbidden not in text, f"{path.relative_to(ROOT)} contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.4 owner closure: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart I.4 owner closure: PASS — Product source cluster selected, 2 owner gaps remain, unified reader/citation/Product release open")
