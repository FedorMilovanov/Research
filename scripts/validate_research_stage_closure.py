#!/usr/bin/env python3
"""Validate the 2026-08-02 repository stage-based root authority."""
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
    "STAGE-OSK-WAVE12": "CLOSED_WITH_CI_AND_PRODUCTION_READBACK",
    "STAGE-HEART-P0": "RESEARCH_CLOSED_EDITORIAL_ASSEMBLY_OPEN",
    "STAGE-ATLAS-PIHAHIROTH": "RESEARCH_CLOSED_PRODUCT_IMPLEMENTATION_OPEN",
    "STAGE-BAPTIST-SCAN-LANE": "REQUEST_AND_RECEIPT_SYSTEM_CLOSED_EXTERNAL_DELIVERY_OPEN",
    "STAGE-GILL-CLOSED-BOOKS": "OWNERSHIP_AND_ACCEPTANCE_CLOSED_EXTERNAL_ACQUISITION_OPEN",
    "STAGE-SOURCE-URL-REPAIRS": "CONFIRMED_REPAIRS_CLOSED_REMAINING_QUEUE_OPEN",
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


def assert_path(raw: Any, context: str) -> Path | None:
    require(isinstance(raw, str) and bool(raw.strip()), f"{context}: path required")
    if not isinstance(raw, str) or not raw.strip():
        return None
    path = ROOT / raw
    require(path.is_file(), f"{context}: missing file {raw}")
    return path


def stage_receipt_success(path: Path, stage_id: str) -> None:
    value = load(path)
    text = json.dumps(value, ensure_ascii=False).upper()
    require("SUCCESS" in text, f"{stage_id}: receipt does not contain SUCCESS: {path.relative_to(ROOT)}")


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
    semantic = assert_path(stage.get("semanticAuthority"), f"{stage_id} semanticAuthority")
    machine = assert_path(stage.get("machineAuthority"), f"{stage_id} machineAuthority")
    require(bool(str(stage.get("nextLane", "")).strip()), f"{stage_id}: nextLane required")
    receipt_paths = stage.get("receipts", [])
    require(isinstance(receipt_paths, list) and bool(receipt_paths), f"{stage_id}: at least one receipt required")
    if isinstance(receipt_paths, list):
        for receipt_raw in receipt_paths:
            receipt = assert_path(receipt_raw, f"{stage_id} receipt")
            if receipt is not None:
                stage_receipt_success(receipt, stage_id)
    if semantic is not None:
        semantic_text = read(semantic)
        require("TODO" not in semantic_text and "TBD" not in semantic_text, f"{stage_id}: unresolved marker in semantic authority")
    if machine is not None:
        machine_data = load(machine)
        require(bool(machine_data), f"{stage_id}: machine authority empty or invalid")

require(set(ids) == set(EXPECTED_STATES), "root stage set drift")
require(len(ids) == len(set(ids)), "duplicate root stage IDs")

by_id = {str(stage.get("id")): stage for stage in stages if isinstance(stage, dict)}
osk = by_id.get("STAGE-OSK-WAVE12", {}).get("result", {})
require(osk == {
    "route": "/articles/diotrefy-nashego-vremeni/",
    "disposition": "PROMOTE",
    "holds": [],
    "authoritySources": 181,
    "readerLinks": 73,
    "newDirectQuotesApproved": 0,
    "productionReadback": True,
}, "OSK root result drift")
heart = by_id.get("STAGE-HEART-P0", {}).get("result", {})
require(heart == {"dossiers": 3, "sources": 17, "claims": 26, "newDirectQuotesApproved": 0}, "Heart root result drift")
atlas = by_id.get("STAGE-ATLAS-PIHAHIROTH", {}).get("result", {})
require(atlas.get("authoritativePoints") == 0 and atlas.get("exactCoordinate") == "UNRESOLVED" and atlas.get("singlePointAllowed") is False, "Atlas uncertainty boundary drift")
baptist = by_id.get("STAGE-BAPTIST-SCAN-LANE", {}).get("result", {})
require(baptist.get("verifiedFileReceipts") == 0 and baptist.get("ocrComplete") == 0 and baptist.get("quoteReady") == 0, "Baptist root receipt overclaim")
gill = by_id.get("STAGE-GILL-CLOSED-BOOKS", {}).get("result", {})
require(gill.get("verifiedPackageReceipts") == 0 and gill.get("quoteReadyFamilies") == 0 and gill.get("newDirectQuotesApproved") == 0, "Gill root receipt overclaim")
source = by_id.get("STAGE-SOURCE-URL-REPAIRS", {}).get("result", {})
require(source == {"confirmedReplacements": 7, "addedVersionHistory": 1, "rightsHoldsPreserved": 3, "versionPins": 1}, "Source URL root result drift")

counts = registry.get("counts")
require(counts == {
    "stages": 6,
    "fullyClosedWithExternalReadback": 1,
    "researchClosedNextLaneOpen": 2,
    "operationalSystemsClosedExternalDependencyOpen": 2,
    "boundedRepairSetClosedRemainingQueueOpen": 1,
}, "root count classification drift")

for marker in (
    "RESEARCH-CURRENT-AUTHORITY-2026-08-02",
    "OSK Wave 12",
    "Heart P0",
    "Atlas Pihahiroth",
    "Baptist scan acquisition",
    "Gill closed books",
    "Source URL repairs",
    "VERIFIED FILE RECEIPTS = 0",
    "VERIFIED PACKAGE RECEIPTS = 0",
    "SINGLE AUTHORITATIVE POINT = FORBIDDEN",
):
    require(marker in root_text, f"root authority missing marker: {marker}")
for forbidden in ("TODO", "TBD", "всё полностью закрыто", "все файлы получены"):
    require(forbidden not in root_text.lower(), f"root authority contains forbidden completion marker: {forbidden}")
require("RESEARCH-CONTROL-PLANE-2026-08-02" in control_text, "control-plane authority marker missing")

if errors:
    print(f"Research stage authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Research stage authority: PASS — six owned stages, receipts composed, external dependencies preserved")
