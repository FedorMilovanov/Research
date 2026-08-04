#!/usr/bin/env python3
"""Validate the Heart chapter VII source-owner closure overlay."""
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
OVERLAY = ROOT / "data/heart-vii-owner-closure-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/84_VII_SUFFERING_AND_DESPAIR_OWNER_CLOSURE_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"
V84B = ROOT / "СЕРИЯ СЕРДЦЕ/65_V84B_DEPRESSION_THEOLOGICAL_PRIMACY_AND_AXIS_CORRECTION.md"
V84D = ROOT / "СЕРИЯ СЕРДЦЕ/67_V84D_SOURCE_LOCATOR_AND_EVIDENCE_STATUS_CLOSURE.md"
V84I = ROOT / "СЕРИЯ СЕРДЦЕ/72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md"

PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
CORE_PATH = "src/components/article-pilots/_shared/heartSeriesData.ts"
CORE_BLOB = "553adbd67a459fa9e022f00b924e8c20201bf400"
SATELLITE_PATH = "src/components/article-pilots/_shared/series/hardTextsSeriesConfig.ts"
SATELLITE_BLOB = "152c90b2dcee67d1683289445d0d2239905ed41c"
EXPECTED_SATELLITES = {
    ("tma", "tma-na-serdce"),
    ("skorb", "serdce-pod-skorbyu"),
}
EXPECTED_RESEARCH_OWNERS = [
    "СЕРИЯ СЕРДЦЕ/65_V84B_DEPRESSION_THEOLOGICAL_PRIMACY_AND_AXIS_CORRECTION.md",
    "СЕРИЯ СЕРДЦЕ/67_V84D_SOURCE_LOCATOR_AND_EVIDENCE_STATUS_CLOSURE.md",
    "СЕРИЯ СЕРДЦЕ/72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md",
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
overlay = load(OVERLAY)

require(base.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "base integration authority drift")
require(base.get("counts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 5,
    "researchDossierOnly": 6,
    "ownerRequired": 4,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "newDirectQuotesApproved": 0,
}, "base integration counts drift")
entries = base.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "base integration must contain eighteen entries")
base_vii = next((row for row in entries if isinstance(row, dict) and row.get("id") == "HEART-BOOK-VII"), None)
require(isinstance(base_vii, dict), "base chapter VII entry missing")
if isinstance(base_vii, dict):
    require(base_vii.get("bookLabel") == "VII Сердце в страдании и унынии", "base chapter VII label drift")
    require(base_vii.get("primaryState") == "OWNER_REQUIRED", "base chapter VII historical state drift")
    require(base_vii.get("productOwner") is None, "base chapter VII must remain the pre-overlay snapshot")
    require(base_vii.get("researchOwners") == [], "base chapter VII historical owner set drift")

require(overlay.get("schemaVersion") == 1, "VII overlay schema drift")
require(overlay.get("authorityId") == "HEART-VII-OWNER-CLOSURE-2026-08-04", "VII overlay authority drift")
require(overlay.get("status") == "VII_PRODUCT_SOURCE_CLUSTER_ESTABLISHED_UNIFIED_READER_AND_BOOK_CITATION_PASS_OPEN", "VII overlay status drift")
require(overlay.get("generatedAt") == "2026-08-04", "VII overlay generated date drift")
require(overlay.get("lastVerifiedAt") == "2026-08-04", "VII overlay verification date drift")
require(overlay.get("baseAuthorityId") == base.get("authorityId"), "VII overlay base authority mismatch")
require(overlay.get("baseAuthority") == "data/heart-whole-book-integration-2026-08-04.json", "VII overlay base path drift")
require(overlay.get("researchSnapshot") == "3000ce2b90a61cfc0fc0a24c2292ab5bf931ffb7", "VII overlay Research snapshot drift")

snapshot = overlay.get("productSnapshot", {})
require(snapshot.get("repository") == "FedorMilovanov/gb-is-my-strength", "VII Product repository drift")
require(snapshot.get("commit") == PRODUCT_COMMIT, "VII Product commit drift")
require(snapshot.get("coreRegistry") == {"path": CORE_PATH, "blobSha": CORE_BLOB}, "VII core registry drift")
require(snapshot.get("satelliteRegistry") == {"path": SATELLITE_PATH, "blobSha": SATELLITE_BLOB}, "VII satellite registry drift")

override = overlay.get("entryOverride", {})
require(override.get("id") == "HEART-BOOK-VII", "VII override ID drift")
require(override.get("bookLabel") == "VII Сердце в страдании и унынии", "VII override label drift")
require(override.get("previousPrimaryState") == "OWNER_REQUIRED", "VII previous state drift")
require(override.get("effectivePrimaryState") == "PRODUCT_SOURCE_ONLY", "VII effective state drift")
require(override.get("primaryProductOwner") == {
    "id": "tma",
    "slug": "tma-na-serdce",
    "minutes": 34,
    "role": "depression-darkness-body-soul-guilt-safety primary source",
}, "VII primary Product owner drift")
require(override.get("supportingProductOwners") == [{
    "id": "skorb",
    "slug": "serdce-pod-skorbyu",
    "minutes": 28,
    "role": "suffering-providence-lament companion source",
}], "VII supporting Product owner drift")
require(override.get("researchOwners") == EXPECTED_RESEARCH_OWNERS, "VII Research owner set drift")
for owner in EXPECTED_RESEARCH_OWNERS:
    require((ROOT / owner).is_file(), f"VII Research owner missing: {owner}")
require(override.get("effectiveCitationState") == "PRODUCT_SOURCE_CITATION_PASS_REQUIRED", "VII citation state drift")
require(override.get("manuscriptState") == "SOURCE_CLUSTER_SELECTED_UNIFIED_READER_NOT_ASSEMBLED", "VII manuscript boundary drift")
require(len(str(override.get("dedupOwner", ""))) >= 180, "VII dedup owner too weak")

support = override.get("supportBoundary", {})
require(isinstance(support.get("supports"), list) and len(support["supports"]) == 3, "VII support set drift")
require(isinstance(support.get("doesNotSupport"), list) and len(support["doesNotSupport"]) == 4, "VII non-support set drift")
require("a unified chapter VII reader manuscript is assembled" in support.get("doesNotSupport", []), "VII unified-reader negative boundary missing")
require("new direct quotations are approved" in support.get("doesNotSupport", []), "VII direct-quote negative boundary missing")

require(overlay.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 6,
    "researchDossierOnly": 6,
    "ownerRequired": 3,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "selectedProductSatelliteItems": 2,
    "newDirectQuotesApproved": 0,
}, "VII effective counts drift")
require(overlay.get("remainingOwnerGaps") == ["HEART-BOOK-I4", "HEART-BOOK-X2", "HEART-BOOK-X3"], "VII remaining gap set drift")
require(overlay.get("publicationBoundary") == {
    "viiSourceOwnerClusterClosed": True,
    "viiUnifiedReaderAssembled": False,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "VII publication boundary drift")
require("supersedes" in str(overlay.get("supersessionRule", "")), "VII supersession rule missing")

require(product_root.is_dir(), f"Product checkout missing: {product_root}")
require(run_git(product_root, "rev-parse", "HEAD") == PRODUCT_COMMIT, "VII Product checkout head drift")
require(run_git(product_root, "hash-object", CORE_PATH) == CORE_BLOB, "VII core registry blob drift")
require(run_git(product_root, "hash-object", SATELLITE_PATH) == SATELLITE_BLOB, "VII satellite registry blob drift")
satellite_file = product_root / SATELLITE_PATH
require(satellite_file.is_file(), "VII satellite registry file missing")
satellite_text = satellite_file.read_text(encoding="utf-8") if satellite_file.is_file() else ""
parsed_satellites = set(re.findall(r"\{\s*id:\s*'([^']+)',\s*slug:\s*'([^']+)'", satellite_text))
require(EXPECTED_SATELLITES.issubset(parsed_satellites), f"VII Product satellite pair missing: {EXPECTED_SATELLITES - parsed_satellites}")
require("minutes: 34" in satellite_text and "minutes: 28" in satellite_text, "VII Product satellite reading times missing")

v84b = read(V84B)
v84d = read(V84D)
v84i = read(V84I)
require("V84B — ДЕПРЕССИЯ: БОГОСЛОВСКОЕ ПЕРВЕНСТВО И ИСПРАВЛЕНИЕ ОСЕЙ" in v84b, "V84B theological owner marker missing")
require("corrective authority / supersession overlay" in v84b, "V84B authority marker missing")
require("V84D — SOURCE LOCATOR AND EVIDENCE-STATUS CLOSURE" in v84d, "V84D source-integrity owner marker missing")
require("source-integrity authority" in v84d, "V84D authority marker missing")
require("The material text base is complete for the present publication stage." in v84i, "V84I material-completeness marker missing")
require("THEOLOGICAL AND SAFETY BOUNDARIES COMPLETE FOR CURRENT PUBLICATION" in v84i, "V84I safety-boundary marker missing")

human = read(HUMAN)
for marker in (
    "HEART-VII-OWNER-CLOSURE-2026-08-04",
    "VII SOURCE OWNER CLUSTER = CLOSED",
    "UNIFIED VII READER = NOT ASSEMBLED",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "OWNER GAPS REMAINING = 3",
    PRODUCT_COMMIT,
    CORE_BLOB,
    SATELLITE_BLOB,
    "tma-na-serdce",
    "serdce-pod-skorbyu",
):
    require(marker in human, f"VII human authority marker missing: {marker}")

current = read(CURRENT)
for marker in (
    "HEART-CURRENT-AUTHORITY-2026-08-04",
    "VII SOURCE OWNER CLUSTER = CLOSED",
    "UNIFIED VII READER = NOT ASSEMBLED",
    "PRODUCT SOURCE OWNERS = 6",
    "STANDALONE OWNER GAPS = 3",
    "I.4 `Внутренний человек и телесная жизнь`",
    "X.2 `Освобождённое сердце`",
    "X.3 `Заключительная надежда`",
):
    require(marker in current, f"current authority VII marker missing: {marker}")
require("VII `Сердце в страдании и унынии`" not in current.split("### Manuscript owner gaps", 1)[-1].split("### Dossier-to-reader assembly", 1)[0], "VII remains in current owner-gap list")

for path, text in ((HUMAN, human), (CURRENT, current)):
    for forbidden in (
        "VII SOURCE OWNER CLUSTER = OPEN",
        "UNIFIED VII READER = ASSEMBLED",
        "WHOLE-BOOK CITATION PASS = CLOSED",
        "PRODUCT RELEASE = COMPLETE",
        "NEW DIRECT QUOTES = 1",
        "TODO",
        "TBD",
    ):
        require(forbidden not in text, f"{path.relative_to(ROOT)} contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart VII owner closure: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart VII owner closure: PASS — Product source cluster selected, 3 owner gaps remain, unified reader/citation/Product release open")
