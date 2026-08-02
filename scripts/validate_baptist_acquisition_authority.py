#!/usr/bin/env python3
"""Fail-closed validator for Baptist Drive acquisition and proof-stage authority."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/baptist-acquisition-proof-authority-2026-08-02.json"
CURRENT = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/00_CURRENT_AUTHORITY_2026-08-02.md"
RECEIPT = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/drive_acquisition_delta_2026-08-02.csv"
README = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/README.md"

errors: list[str] = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

for path in (AUTH, CURRENT, RECEIPT, README):
    require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

try:
    authority = json.loads(AUTH.read_text(encoding="utf-8"))
except Exception as exc:
    authority = {}
    errors.append(f"invalid authority JSON: {exc}")

expected = {
    "SINICHKIN-2018-FIRST-RUSSIAN-BAPTIST-BAPTISM": {
        "masterRow": 51,
        "canonicalDriveId": "1yH-oxjymaDJi4g5Els8xpRiqKFgWDD7V",
        "rawDuplicateDriveId": "1nPb63h0DLbhx582WFpVPeXS2fH5UFT8O",
        "bytes": 542143,
        "pages": 14,
        "sha256": "3d33eb3691dd18f0109028cf1c2c51bb71e21b882dfddfff4393438311498c1c",
    },
    "VORONIN-BIOGRAPHY-DOSSIER": {
        "masterRow": 52,
        "canonicalDriveId": "17O1csxPvxZO0T4Wq0TaRmT69yQ1dkEmT",
        "rawDuplicateDriveId": "1_PxsBG7YrO58B3yajjNt5MF08WlZDrbV",
        "bytes": 244468,
        "pages": 5,
        "sha256": "6d23e500ef19dc457d2f23c06b695ea95e2670759558e0419847022ccc969cc9",
    },
}

require(authority.get("schemaVersion") == 1, "schemaVersion drift")
require(authority.get("authorityId") == "BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02", "authorityId drift")
require(authority.get("status") == "CURRENT_FOR_ACQUISITION_AND_PROOF_STAGES_NOT_PUBLICATION", "status drift")
master = authority.get("operationalMaster", {})
require(master.get("driveId") == "1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM", "MASTER Drive ID drift")
require(master.get("sheet") == "12 Drive Acquisitions", "MASTER sheet drift")
require(master.get("mutationPolicy") == "APPEND_ONLY", "MASTER mutation policy drift")
split = authority.get("authoritySplit", {})
require(split.get("driveMasterRole") == "MUTABLE_OPERATIONAL_INVENTORY", "Drive role drift")
require(split.get("githubRole") == "IMMUTABLE_STATUS_SEMANTICS_AND_AUDIT_RECEIPTS", "GitHub role drift")
require(split.get("binaryIdentityRule") == "EXACT_DRIVE_ID_PLUS_SHA256", "binary identity rule drift")
require(split.get("conflictRule") == "FAIL_CLOSED_NO_SILENT_SUPERSESSION", "conflict rule drift")
require(authority.get("stateMachines", {}).get("acquisition") == [
    "LOCATOR_ONLY", "VIEWER_ACCESSIBLE", "BYTES_ACQUIRED", "CANONICAL_DRIVE_REGISTERED"
], "acquisition state machine drift")
require(authority.get("stateMachines", {}).get("proof") == [
    "NO_TEXT", "TEXT_LAYER_PRESENT", "VISUAL_PAGE_VERIFIED", "QUOTE_READY"
], "proof state machine drift")

receipts = authority.get("receipts", [])
require(isinstance(receipts, list) and len(receipts) == 2, "exactly two receipts required")
receipt_by_id = {item.get("id"): item for item in receipts if isinstance(item, dict)}
require(len(receipt_by_id) == 2, "receipt IDs must be unique")
canonical_ids: set[str] = set()
raw_ids: set[str] = set()
hashes: set[str] = set()
for item_id, spec in expected.items():
    item = receipt_by_id.get(item_id, {})
    for field, value in spec.items():
        require(item.get(field) == value, f"{item_id}: {field} drift")
    require(item.get("acquisitionState") == "CANONICAL_DRIVE_REGISTERED", f"{item_id}: acquisition state drift")
    require(item.get("proofState") == "TEXT_LAYER_PRESENT", f"{item_id}: proof state drift")
    require(item.get("visualState") == "PENDING", f"{item_id}: visual state must remain pending")
    require(item.get("quoteState") == "NOT_APPROVED", f"{item_id}: quote state must remain not approved")
    require(item.get("canonicalDriveId") != item.get("rawDuplicateDriveId"), f"{item_id}: canonical and raw IDs collide")
    canonical_ids.add(str(item.get("canonicalDriveId")))
    raw_ids.add(str(item.get("rawDuplicateDriveId")))
    hashes.add(str(item.get("sha256")))
require(len(canonical_ids) == 2, "canonical Drive IDs must be unique")
require(len(raw_ids) == 2, "raw duplicate Drive IDs must be unique")
require(len(hashes) == 2, "SHA-256 values must be unique")

counts = authority.get("counts", {})
require(counts == {
    "receipts": 2,
    "canonicalDriveRegistered": 2,
    "textLayerPresent": 2,
    "visualPageVerified": 0,
    "quoteReady": 0,
}, "authority counts drift")
boundaries = authority.get("boundaries", {})
for key in ("publicationClaimed", "visualVerificationClaimed", "quoteReadyClaimed", "rawDuplicatesMayBeDeleted", "paidOrdersAuthorized"):
    require(boundaries.get(key) is False, f"boundary must remain false: {key}")

try:
    with RECEIPT.open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
except Exception as exc:
    csv_rows = []
    errors.append(f"invalid receipt CSV: {exc}")
require(len(csv_rows) == 2, "receipt CSV must contain exactly two data rows")
for row in csv_rows:
    matching = next((item for item in receipts if str(item.get("masterRow")) == row.get("row")), None)
    require(matching is not None, f"CSV row {row.get('row')} absent from JSON authority")
    if matching:
        require(row.get("canonical_drive_id") == matching.get("canonicalDriveId"), f"CSV row {row.get('row')}: canonical Drive ID drift")
        require(row.get("raw_duplicate_id") == matching.get("rawDuplicateDriveId"), f"CSV row {row.get('row')}: raw duplicate ID drift")
        require(row.get("sha256") == matching.get("sha256"), f"CSV row {row.get('row')}: SHA drift")
        require(row.get("pages") == str(matching.get("pages")), f"CSV row {row.get('row')}: page count drift")
        require(row.get("bytes") == str(matching.get("bytes")), f"CSV row {row.get('row')}: byte count drift")
        require(row.get("acquisition_state") == "CANONICAL_DRIVE_REGISTERED", f"CSV row {row.get('row')}: acquisition state drift")
        require(row.get("text_state") == "TEXT_LAYER_PRESENT", f"CSV row {row.get('row')}: text state drift")
        require(row.get("visual_state") == "PENDING", f"CSV row {row.get('row')}: visual state drift")
        require(row.get("quote_state") == "NOT_APPROVED", f"CSV row {row.get('row')}: quote state drift")

current_text = CURRENT.read_text(encoding="utf-8") if CURRENT.exists() else ""
readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
for marker in (
    "BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02",
    "FAIL_CLOSED",
    "VISUAL PENDING",
    "PUBLICATION READINESS: NOT CLAIMED",
):
    require(marker in current_text.upper(), f"current authority marker missing: {marker}")
require("00_CURRENT_AUTHORITY_2026-08-02.md" in readme_text, "README does not point to current authority")
require("операционный каталог" in readme_text.lower(), "README does not define Drive operational role")
require("неизменяем" in readme_text.lower(), "README does not define immutable GitHub receipt role")
require("Живой Google Sheets MASTER является каноническим и редактируется append-only." not in readme_text, "obsolete universal MASTER authority statement remains")

if errors:
    print(f"Baptist acquisition authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Baptist acquisition authority: PASS — 2 canonical Drive receipts, 2 text layers, 0 visual, 0 quote-ready")
