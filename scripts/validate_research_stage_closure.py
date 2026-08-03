#!/usr/bin/env python3
"""Validate the current six-stage Research root authority without false receipts."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/research-stage-closure-2026-08-02.json"
AUTHORITY = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md"
CONTROL = ROOT / "00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md"
EXPECTED_STATES = {
    "STAGE-OSK-WAVE12": "SOURCE_ACCEPTED_LIVE_VERIFICATION_OPEN",
    "STAGE-HEART-P0": "RESEARCH_AND_THREE_READER_CHAPTERS_CLOSED_BOOK_QA_OPEN",
    "STAGE-ATLAS-PIHAHIROTH": "RESEARCH_CLOSED_PRODUCT_IMPLEMENTATION_OPEN",
    "STAGE-BAPTIST-SCAN-LANE": "REQUEST_AND_RECEIPT_SYSTEM_CLOSED_EXTERNAL_DELIVERY_OPEN",
    "STAGE-GILL-CLOSED-BOOKS": "OWNERSHIP_AND_ACCEPTANCE_CLOSED_EXTERNAL_ACQUISITION_OPEN",
    "STAGE-SOURCE-URL-REPAIRS": "CONFIRMED_REPAIRS_CLOSED_REMAINING_QUEUE_OPEN",
}
EXPECTED_COUNTS = {
    "stages": 6,
    "sourceAcceptedLiveVerificationOpen": 1,
    "researchAndReaderAssemblyClosedBookQaOpen": 1,
    "researchClosedProductImplementationOpen": 1,
    "operationalSystemsClosedExternalDependencyOpen": 2,
    "boundedRepairSetClosedRemainingQueueOpen": 1,
}
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
        errors.append(f"{path.relative_to(ROOT)}: JSON object required")
        return {}
    return value


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return ""


def require_file(raw: Any, context: str) -> Path | None:
    require(isinstance(raw, str) and bool(raw.strip()), f"{context}: path required")
    if not isinstance(raw, str) or not raw.strip():
        return None
    path = ROOT / raw
    require(path.is_file(), f"{context}: missing file {raw}")
    return path


registry = load(REGISTRY)
root_text = read(AUTHORITY)
control_text = read(CONTROL)
require(registry.get("schemaVersion") == 1, "stage registry schemaVersion drift")
require(registry.get("authorityId") == "RESEARCH-STAGE-CLOSURE-2026-08-02", "stage registry authorityId drift")
require(registry.get("status") == "CURRENT_FAIL_CLOSED", "stage registry status drift")
require(registry.get("currentAuthority") == "00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md", "root authority pointer drift")
require(registry.get("controlPlaneAuthority") == "00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md", "control-plane pointer drift")

stages = registry.get("stages")
require(isinstance(stages, list) and len(stages) == 6, "exactly six root stages required")
stages = stages if isinstance(stages, list) else []
ids: list[str] = []
for stage in stages:
    require(isinstance(stage, dict), "stage object required")
    if not isinstance(stage, dict):
        continue
    stage_id = str(stage.get("id", "")).strip()
    ids.append(stage_id)
    require(stage_id in EXPECTED_STATES, f"unexpected stage ID: {stage_id}")
    if stage_id not in EXPECTED_STATES:
        continue
    require(stage.get("state") == EXPECTED_STATES[stage_id], f"{stage_id}: state drift")
    semantic = require_file(stage.get("semanticAuthority"), f"{stage_id} semanticAuthority")
    machine = require_file(stage.get("machineAuthority"), f"{stage_id} machineAuthority")
    require(bool(str(stage.get("nextLane", "")).strip()), f"{stage_id}: nextLane required")
    receipts = stage.get("receipts")
    require(receipts == [], f"{stage_id}: no receipt path may be declared without an actual receipt")
    if semantic is not None:
        semantic_text = read(semantic)
        require("TODO" not in semantic_text and "TBD" not in semantic_text, f"{stage_id}: unresolved marker in semantic authority")
    if machine is not None:
        require(bool(load(machine)), f"{stage_id}: machine authority empty or invalid")

require(set(ids) == set(EXPECTED_STATES), "root stage set drift")
require(len(ids) == len(set(ids)), "duplicate root stage IDs")
by_id = {str(stage.get("id")): stage for stage in stages if isinstance(stage, dict)}

osk = by_id.get("STAGE-OSK-WAVE12", {})
require(osk.get("semanticAuthority") == "PUBLIC_PROJECTION_CURRENT_AUTHORITY_2026-08-01.md", "OSK semantic authority drift")
require(osk.get("machineAuthority") == "data/public-projection-current-2026-08-02.json", "OSK machine authority drift")
require(osk.get("result") == {
    "route": "/articles/diotrefy-nashego-vremeni/",
    "disposition": "REFERENCE",
    "holds": ["PUBLICATION_HOLD"],
    "authoritySources": 181,
    "readerLinks": 73,
    "newDirectQuotesApproved": 0,
    "productPullRequest": 810,
    "exactVerifiedHead": "f39589d8920ae828c13ee5fd804a79433be7bd82",
    "sourceMerge": "e604b97dbbe45cf9ba9e2a84551b799f0dac1a0e",
    "exactHeadChecksGreen": True,
    "productionReadback": False,
}, "OSK root source-acceptance result drift")

heart = by_id.get("STAGE-HEART-P0", {})
require(heart.get("semanticAuthority") == "СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md", "Heart semantic authority drift")
require(heart.get("machineAuthority") == "data/heart-reader-assembly-2026-08-02.json", "Heart machine authority drift")
require(heart.get("result") == {
    "dossiers": 3,
    "sources": 17,
    "claims": 26,
    "readerChapters": 3,
    "finalBookEntries": 18,
    "newDirectQuotesApproved": 0,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "productReleaseComplete": False,
}, "Heart root result drift")

atlas = by_id.get("STAGE-ATLAS-PIHAHIROTH", {}).get("result", {})
require(atlas.get("authoritativePoints") == 0, "Atlas authoritative-point drift")
require(atlas.get("exactCoordinate") == "UNRESOLVED", "Atlas exact-coordinate drift")
require(atlas.get("singlePointAllowed") is False, "Atlas single-point boundary drift")

baptist_stage = by_id.get("STAGE-BAPTIST-SCAN-LANE", {})
baptist = baptist_stage.get("result", {})
require(baptist_stage.get("receiptLedger") == "data/baptist-scan-receipts-v1.json", "Baptist receipt ledger pointer drift")
require_file(baptist_stage.get("receiptLedger"), "Baptist receiptLedger")
require(baptist.get("verifiedFileReceipts") == 0, "Baptist verified receipt overclaim")
require(baptist.get("ocrComplete") == 0 and baptist.get("quoteReady") == 0, "Baptist OCR/quote overclaim")

gill = by_id.get("STAGE-GILL-CLOSED-BOOKS", {}).get("result", {})
require(gill.get("verifiedPackageReceipts") == 0, "Gill verified package overclaim")
require(gill.get("quoteReadyFamilies") == 0 and gill.get("newDirectQuotesApproved") == 0, "Gill quote overclaim")

source = by_id.get("STAGE-SOURCE-URL-REPAIRS", {}).get("result", {})
require(source == {"confirmedReplacements": 7, "addedVersionHistory": 1, "rightsHoldsPreserved": 3, "versionPins": 1}, "Source URL root result drift")
require(registry.get("counts") == EXPECTED_COUNTS, "root count classification drift")

for marker in (
    "RESEARCH-CURRENT-AUTHORITY-2026-08-02",
    "SOURCE ACCEPTED / LIVE VERIFICATION OPEN",
    "DISPOSITION = REFERENCE",
    "HOLDS = [PUBLICATION_HOLD]",
    "PRODUCTION READBACK = NOT VERIFIED",
    "THREE READER CHAPTERS CLOSED",
    "VERIFIED FILE RECEIPTS = 0",
    "VERIFIED PACKAGE RECEIPTS = 0",
    "SINGLE AUTHORITATIVE POINT = FORBIDDEN",
):
    require(marker in root_text, f"root authority missing marker: {marker}")
for forbidden in (
    "CLOSED WITH CI + PRODUCTION READBACK",
    "DISPOSITION = PROMOTE",
    "PRODUCTION READBACK = VERIFIED",
    "data/osk-wave12-product-release-receipt-2026-08-02.json",
):
    require(forbidden not in root_text, f"root authority retains unsupported marker: {forbidden}")
require("RESEARCH-CONTROL-PLANE-2026-08-02" in control_text, "control-plane authority marker missing")

if errors:
    print(f"Research stage authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Research stage authority: PASS — six owned stages; source/live, reader/book and external receipt boundaries preserved")
