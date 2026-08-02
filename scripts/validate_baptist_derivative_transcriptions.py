#!/usr/bin/env python3
"""Fail-closed validator for modern derivative transcriptions in the Baptist corpus."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/baptist-derivative-transcription-authority-2026-08-02.json"
CURRENT = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/00_CURRENT_AUTHORITY_2026-08-02.md"

errors: list[str] = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""

def csv_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except Exception as exc:
        errors.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return []

require(REGISTRY.is_file(), "derivative registry missing")
try:
    registry: dict[str, Any] = json.loads(text(REGISTRY))
except Exception as exc:
    registry = {}
    errors.append(f"invalid derivative registry JSON: {exc}")

require(registry.get("schemaVersion") == 1, "schemaVersion drift")
require(registry.get("authorityId") == "BAPTIST-DERIVATIVE-TRANSCRIPTIONS-2026-08-02", "authorityId drift")
require(registry.get("status") == "CURRENT_SOURCE_CLASS_OVERLAY_NOT_PRIMARY_QUOTE_AUTHORITY", "status drift")
require(registry.get("composes") == "BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02", "composition target drift")
require(registry.get("classificationRule") == "MODERN_TYPED_TEXT_WITHOUT_ARCHIVAL_PAGE_IMAGE_OR_EDITION_PROVENANCE_IS_DERIVATIVE_TRANSCRIPTION", "classification rule drift")
require(set(registry.get("permittedUse", [])) == {
    "NAVIGATION", "SEARCH_TARGET_DISCOVERY", "WORKING_PARAPHRASE_WITH_DERIVATIVE_DISCLOSURE"
}, "permitted-use set drift")
require(set(registry.get("forbiddenUse", [])) == {
    "PRIMARY_QUOTATION_WITHOUT_ORIGINAL_OR_EDITION_CHECK",
    "ARCHIVAL_FACSIMILE_CLAIM",
    "ORIGINAL_ORTHOGRAPHY_OR_SIGNATURE_CLAIM",
    "COMPLETENESS_CLAIM",
}, "forbidden-use set drift")

expected = {
    "SHILOV-LENIN-1919-DERIVATIVE-2026-08-02": {
        "historicalTarget": "LETTER_DATED_1919-12-11_PLUS_1920_RESPONSE",
        "fileName": "Письмо Шилова Ленину (1).pdf",
        "canonicalDriveId": "12PD_RzFXLcKrIYy9ubfskvRKVPj7FlOc",
        "rawDuplicateDriveId": "1iJhvJ7UjlyhNZAXk586sZzRTa37mKLmf",
        "bytes": 79460,
        "pages": 3,
        "sha256": "7c9674b65e15bf76c1833ba0b99b4d735e2c9f3f268351af17f8206516003327",
        "creationDate": "2024-04-18",
        "masterAcquisitionRow": 53,
        "masterLibraryRow": 100,
        "receipt": "RUSSIAN_BAPTISTS_ARCHIVE/SHILOV_LENIN_1919_DERIVATIVE_CLASSIFICATION_2026-08-02.md",
        "acquisitionReceipt": "RUSSIAN_BAPTISTS_ARCHIVE/drive_acquisition_delta_2026-08-02-b.csv",
    },
    "MOSCOW-COMMUNITY-1923-DERIVATIVE-2026-08-02": {
        "historicalTarget": "MOSCOW_EVANGELICAL_CHRISTIAN_COMMUNITY_STATEMENT_1923",
        "fileName": "Заявление Московской Общины  1923.pdf",
        "canonicalDriveId": "1xBpAmUxoERAZJULqnmevSr5zjgReWAGi",
        "rawDuplicateDriveId": "1ag6DMRa4UO3Pz3SbKRue6LpTR4gL6a1E",
        "bytes": 119979,
        "pages": 8,
        "sha256": "c6ef11f8b2fef460bcc083709e0a74fcc6c29a70c353ac73fbff0907126cb8a0",
        "creationDate": "2023-01-05",
        "masterAcquisitionRow": 54,
        "masterLibraryRow": 92,
        "receipt": "RUSSIAN_BAPTISTS_ARCHIVE/MOSCOW_COMMUNITY_1923_DERIVATIVE_CLASSIFICATION_2026-08-02.md",
        "acquisitionReceipt": "RUSSIAN_BAPTISTS_ARCHIVE/drive_acquisition_delta_2026-08-02-c.csv",
    },
}

records = registry.get("records", [])
require(isinstance(records, list) and len(records) == 2, "exactly two derivative records required")
by_id = {item.get("id"): item for item in records if isinstance(item, dict)}
require(set(by_id) == set(expected), "derivative record ID set drift")
canonical_ids: set[str] = set()
raw_ids: set[str] = set()
digests: set[str] = set()

for record_id, spec in expected.items():
    item = by_id.get(record_id, {})
    for field in (
        "historicalTarget", "fileName", "canonicalDriveId", "rawDuplicateDriveId",
        "bytes", "pages", "sha256", "masterAcquisitionRow", "masterLibraryRow",
        "receipt", "acquisitionReceipt"
    ):
        require(item.get(field) == spec[field], f"{record_id}: {field} drift")
    require(item.get("canonicalFolderDriveId") == "1-vmWwdvYcF8RqFdPr4aWO5REp_mic9Aq", f"{record_id}: folder drift")
    require(item.get("sourceClass") == "DERIVATIVE_TRANSCRIPTION", f"{record_id}: source class drift")
    require(item.get("facsimileState") == "NOT_ARCHIVAL_FACSIMILE", f"{record_id}: facsimile state drift")
    require(item.get("provenanceState") == "ARCHIVAL_ORIGINAL_AND_EDITION_NOT_IDENTIFIED", f"{record_id}: provenance state drift")
    require(item.get("primaryQuoteState") == "NOT_APPROVED", f"{record_id}: primary quote state drift")
    metadata = item.get("pdfMetadata", {})
    require(metadata.get("author") == "Алексей Синичкин", f"{record_id}: PDF author drift")
    require(metadata.get("creator") == "Microsoft Word", f"{record_id}: PDF creator drift")
    require(metadata.get("creationDate") == spec["creationDate"], f"{record_id}: creation date drift")
    canonical_ids.add(str(item.get("canonicalDriveId")))
    raw_ids.add(str(item.get("rawDuplicateDriveId")))
    digests.add(str(item.get("sha256")))

    receipt_path = ROOT / str(item.get("receipt"))
    acquisition_path = ROOT / str(item.get("acquisitionReceipt"))
    require(receipt_path.is_file(), f"{record_id}: classification receipt missing")
    require(acquisition_path.is_file(), f"{record_id}: acquisition receipt missing")
    receipt_text = text(receipt_path)
    for marker in (
        record_id,
        spec["canonicalDriveId"],
        spec["sha256"],
        "DERIVATIVE_TRANSCRIPTION",
        "NOT ARCHIVAL FACSIMILE",
        "PRIMARY QUOTATION: NOT APPROVED",
        "Microsoft Word",
        "Алексей Синичкин",
    ):
        require(marker in receipt_text, f"{record_id}: receipt marker missing: {marker}")
    rows = csv_rows(acquisition_path)
    require(len(rows) == 1, f"{record_id}: acquisition receipt must contain one row")
    if rows:
        row = rows[0]
        require(row.get("row") == str(spec["masterAcquisitionRow"]), f"{record_id}: CSV MASTER row drift")
        require(row.get("canonical_drive_id") == spec["canonicalDriveId"], f"{record_id}: CSV canonical ID drift")
        require(row.get("raw_duplicate_id") == spec["rawDuplicateDriveId"], f"{record_id}: CSV raw ID drift")
        require(row.get("sha256") == spec["sha256"], f"{record_id}: CSV SHA drift")
        require(row.get("source_class") == "DERIVATIVE_TRANSCRIPTION", f"{record_id}: CSV class drift")
        require(row.get("facsimile_state") == "NOT_ARCHIVAL_FACSIMILE", f"{record_id}: CSV facsimile drift")
        require(row.get("primary_quote_state") == "NOT_APPROVED", f"{record_id}: CSV quote drift")

require(len(canonical_ids) == 2, "canonical Drive IDs must be unique")
require(len(raw_ids) == 2, "raw duplicate Drive IDs must be unique")
require(len(digests) == 2, "SHA-256 values must be unique")
require(not (canonical_ids & raw_ids), "canonical and raw Drive IDs overlap")

require(registry.get("counts") == {
    "records": 2,
    "canonicalDriveRegistered": 2,
    "textLayerPresent": 2,
    "derivativeTranscriptions": 2,
    "archivalFacsimiles": 0,
    "primaryQuoteReady": 0,
    "provenanceRestored": 0,
}, "derivative counts drift")
require(registry.get("boundaries") == {
    "underlyingHistoricalTextsDenied": False,
    "facsimileAuthorityClaimed": False,
    "primaryQuoteAuthorityClaimed": False,
    "navigationUseAllowed": True,
}, "derivative boundary drift")

current_text = text(CURRENT).upper()
for marker in (
    "BAPTIST-DERIVATIVE-TRANSCRIPTIONS-2026-08-02",
    "SHILOV-LENIN-1919-DERIVATIVE-2026-08-02",
    "MOSCOW-COMMUNITY-1923-DERIVATIVE-2026-08-02",
    "DERIVATIVE TRANSCRIPTIONS: 2",
    "ARCHIVAL FACSIMILES AMONG THEM: 0",
    "PRIMARY QUOTE-READY AMONG THEM: 0",
):
    require(marker in current_text, f"current authority composition marker missing: {marker}")

if errors:
    print(f"Baptist derivative transcription authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Baptist derivative transcription authority: PASS — 2 derivatives, 0 facsimiles, 0 primary quote-ready")
