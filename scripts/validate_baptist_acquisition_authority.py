#!/usr/bin/env python3
"""Fail-closed validator for Baptist acquisition, source-class and visual authority."""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/baptist-acquisition-proof-authority-2026-08-02.json"
CURRENT = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/00_CURRENT_AUTHORITY_2026-08-02.md"
README = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/README.md"
ACQ_A = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/drive_acquisition_delta_2026-08-02.csv"
ACQ_B = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/drive_acquisition_delta_2026-08-02-b.csv"
VISUAL_MD = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/BAPTIST_1909_NO11_MAZAEV_VISUAL_CLOSURE_2026-08-02.md"
SHILOV_MD = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/SHILOV_LENIN_1919_DERIVATIVE_CLASSIFICATION_2026-08-02.md"

errors: list[str] = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""

def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except Exception as exc:
        errors.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return []

for path in (AUTH, CURRENT, README, ACQ_A, ACQ_B, VISUAL_MD, SHILOV_MD):
    require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

try:
    authority: dict[str, Any] = json.loads(read(AUTH))
except Exception as exc:
    authority = {}
    errors.append(f"invalid authority JSON: {exc}")

require(authority.get("schemaVersion") == 3, "schemaVersion must be 3")
require(authority.get("authorityId") == "BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02", "authorityId drift")
require(authority.get("status") == "CURRENT_FOR_ACQUISITION_AND_PROOF_STAGES_NOT_PUBLICATION", "authority status drift")

master = authority.get("operationalMaster", {})
require(master.get("driveId") == "1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM", "MASTER Drive ID drift")
require(master.get("acquisitionSheet") == "12 Drive Acquisitions", "acquisition sheet drift")
require(master.get("dossierSheet") == "08 Article Dossiers", "dossier sheet drift")
require(master.get("librarySheet") == "01 PDF Library", "library sheet drift")
require(master.get("mutationPolicy") == "APPEND_ONLY_OR_IDEMPOTENT_TARGETED_UPDATE", "MASTER mutation policy drift")

split = authority.get("authoritySplit", {})
expected_split = {
    "driveMasterRole": "MUTABLE_OPERATIONAL_INVENTORY",
    "githubRole": "IMMUTABLE_STATUS_SEMANTICS_AND_AUDIT_RECEIPTS",
    "binaryIdentityRule": "EXACT_DRIVE_ID_PLUS_SHA256",
    "visualIdentityRule": "EXACT_SOURCE_SHA256_PLUS_PAGE_LOCATOR_PLUS_VISUAL_CARD_DRIVE_ID_AND_SHA256",
    "sourceClassRule": "FILE_FORM_AND_PROVENANCE_MUST_BE_CLASSIFIED_SEPARATELY_FROM_UNDERLYING_HISTORICAL_TEXT",
    "conflictRule": "FAIL_CLOSED_NO_SILENT_SUPERSESSION",
}
for key, value in expected_split.items():
    require(split.get(key) == value, f"authoritySplit drift: {key}")

machines = authority.get("stateMachines", {})
require(machines.get("acquisition") == [
    "LOCATOR_ONLY", "VIEWER_ACCESSIBLE", "BYTES_ACQUIRED", "CANONICAL_DRIVE_REGISTERED"
], "acquisition state machine drift")
require(machines.get("proof") == [
    "NO_TEXT", "TEXT_LAYER_PRESENT", "VISUAL_PAGE_VERIFIED", "BOUNDED_TRANSCRIPTION_VERIFIED", "QUOTE_READY"
], "proof state machine drift")
require(machines.get("sourceClass") == [
    "UNCLASSIFIED", "DERIVATIVE_TRANSCRIPTION", "PUBLISHED_PRIMARY_TEXT_EDITION", "ARCHIVAL_FACSIMILE"
], "source-class state machine drift")

receipts = authority.get("receipts", [])
require(isinstance(receipts, list) and len(receipts) == 3, "exactly three acquisition receipts required")
by_id = {item.get("id"): item for item in receipts if isinstance(item, dict)}
require(len(by_id) == 3, "receipt IDs must be unique")

expected_common = {
    "SINICHKIN-2018-FIRST-RUSSIAN-BAPTIST-BAPTISM": {
        "masterRow": 51, "canonicalDriveId": "1yH-oxjymaDJi4g5Els8xpRiqKFgWDD7V",
        "rawDuplicateDriveId": "1nPb63h0DLbhx582WFpVPeXS2fH5UFT8O", "bytes": 542143, "pages": 14,
        "sha256": "3d33eb3691dd18f0109028cf1c2c51bb71e21b882dfddfff4393438311498c1c",
        "sourceClass": "MODERN_SCHOLARLY_ARTICLE",
    },
    "VORONIN-BIOGRAPHY-DOSSIER": {
        "masterRow": 52, "canonicalDriveId": "17O1csxPvxZO0T4Wq0TaRmT69yQ1dkEmT",
        "rawDuplicateDriveId": "1_PxsBG7YrO58B3yajjNt5MF08WlZDrbV", "bytes": 244468, "pages": 5,
        "sha256": "6d23e500ef19dc457d2f23c06b695ea95e2670759558e0419847022ccc969cc9",
        "sourceClass": "DERIVATIVE_BIOGRAPHY_DOSSIER",
    },
}
seen_canonical: set[str] = set()
seen_raw: set[str] = set()
seen_hashes: set[str] = set()
for item_id, spec in expected_common.items():
    item = by_id.get(item_id, {})
    for key, value in spec.items():
        require(item.get(key) == value, f"{item_id}: {key} drift")
    require(item.get("acquisitionState") == "CANONICAL_DRIVE_REGISTERED", f"{item_id}: acquisition state drift")
    require(item.get("proofState") == "TEXT_LAYER_PRESENT", f"{item_id}: proof state drift")
    require(item.get("visualState") == "PENDING", f"{item_id}: visual state must remain pending")
    require(item.get("quoteState") == "NOT_APPROVED", f"{item_id}: quote state must remain not approved")
    seen_canonical.add(str(item.get("canonicalDriveId")))
    seen_raw.add(str(item.get("rawDuplicateDriveId")))
    seen_hashes.add(str(item.get("sha256")))

shilov = by_id.get("SHILOV-LENIN-1919-DERIVATIVE-2026-08-02", {})
expected_shilov = {
    "masterRow": 53,
    "libraryRow": 100,
    "fileName": "Письмо Шилова Ленину (1).pdf",
    "canonicalDriveId": "12PD_RzFXLcKrIYy9ubfskvRKVPj7FlOc",
    "rawDuplicateDriveId": "1iJhvJ7UjlyhNZAXk586sZzRTa37mKLmf",
    "canonicalFolderDriveId": "1-vmWwdvYcF8RqFdPr4aWO5REp_mic9Aq",
    "bytes": 79460,
    "pages": 3,
    "sha256": "7c9674b65e15bf76c1833ba0b99b4d735e2c9f3f268351af17f8206516003327",
    "acquisitionState": "CANONICAL_DRIVE_REGISTERED",
    "proofState": "TEXT_LAYER_PRESENT",
    "sourceClass": "DERIVATIVE_TRANSCRIPTION",
    "facsimileState": "NOT_ARCHIVAL_FACSIMILE",
    "provenanceState": "ARCHIVAL_ORIGINAL_AND_EDITION_NOT_IDENTIFIED",
    "primaryQuoteState": "NOT_APPROVED",
    "navigationUse": "ALLOWED_WITH_DERIVATIVE_DISCLOSURE",
    "receipt": "RUSSIAN_BAPTISTS_ARCHIVE/SHILOV_LENIN_1919_DERIVATIVE_CLASSIFICATION_2026-08-02.md",
}
for key, value in expected_shilov.items():
    require(shilov.get(key) == value, f"Shilov: {key} drift")
require(shilov.get("metadata") == {
    "author": "Алексей Синичкин", "creator": "Microsoft Word", "creationDate": "2024-04-18"
}, "Shilov PDF metadata drift")
require(shilov.get("underlyingHistoricalTexts") == [
    "SHILOV_LETTER_DATED_1919-12-11", "PETROGRAD_COMPLAINT_BUREAU_RESPONSE_1920"
], "Shilov underlying-text list drift")
seen_canonical.add(str(shilov.get("canonicalDriveId")))
seen_raw.add(str(shilov.get("rawDuplicateDriveId")))
seen_hashes.add(str(shilov.get("sha256")))
require(len(seen_canonical) == 3, "canonical Drive IDs must be unique")
require(len(seen_raw) == 3, "raw duplicate Drive IDs must be unique")
require(len(seen_hashes) == 3, "acquisition SHA-256 values must be unique")
require(not (seen_canonical & seen_raw), "canonical and raw Drive-ID sets must not overlap")

visuals = authority.get("visualClosures", [])
require(isinstance(visuals, list) and len(visuals) == 1, "exactly one localized visual closure required")
visual = visuals[0] if visuals and isinstance(visuals[0], dict) else {}
require(visual.get("id") == "BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02", "visual closure ID drift")
require(visual.get("source") == {
    "title": "Баптист 1909 №11.pdf",
    "canonicalDriveId": "1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU",
    "bytes": 9842696,
    "pdfPages": 22,
    "sha256": "0d54f0c2157e76f621bf2fd65137386ae538a792516c473703179bc3127fba73",
    "textLayer": "ABSENT_SCAN_ONLY",
}, "Mazaev source identity drift")
locators = visual.get("locators", [])
require(isinstance(locators, list) and len(locators) == 2, "Mazaev closure requires two locators")
locator_by_page = {item.get("printedPage"): item for item in locators if isinstance(item, dict)}
expected_locators = {
    14: (14, "1yOm3KBJ9ujtETUG7u-0hl5ijrGiKuXYG", "ed381e3ee5764483098fbdda76986953d8d5c7e2ab170e453d38d1a2fd6c23e5", {
        "ARTICLE_TITLE_O_PETERBURGSKOI_SVOBODE", "EVANGELICAL_UNION_CRITIQUE_EXISTS", "ARTICLE_CONTINUES_TO_NEXT_PAGE"
    }),
    15: (15, "1v-7bxYeZ6bMsaiVoFgqz5nWUctOtEwA8", "bb3e78a0deb06b437cbf647c09fada131343eb48174d2fa0630809aca639b2ea", {
        "ARTICLE_ENDING", "AUTHOR_SIGNATURE_A_M_MAZAEV"
    }),
}
for page, (pdf_page, drive_id, digest, claims) in expected_locators.items():
    item = locator_by_page.get(page, {})
    require(item.get("pdfPage") == pdf_page, f"Mazaev p.{page}: PDF locator drift")
    require(item.get("visualCardDriveId") == drive_id, f"Mazaev p.{page}: visual Drive ID drift")
    require(item.get("visualCardSha256") == digest, f"Mazaev p.{page}: visual SHA drift")
    require(set(item.get("verifies", [])) == claims, f"Mazaev p.{page}: claim set drift")
require(visual.get("combinedEvidenceDocumentDriveId") == "1zCwFFMTaOcI476aOP_cXSzgdViWNk4VEySJ2G88W6bY", "combined evidence Doc ID drift")
require(visual.get("canonicalFolderDriveId") == "19AluFtMQ_uV3YTAZMA3U0Raostby779c", "visual folder drift")
require(visual.get("masterDossier") == "08 Article Dossiers!S03", "visual MASTER dossier drift")
require(visual.get("proofState") == "VISUAL_PAGE_VERIFIED", "visual proof state drift")
require(visual.get("transcriptionState") == "BOUNDED_TRANSCRIPTION_PENDING", "bounded transcription must remain pending")
require(visual.get("quoteState") == "NOT_GENERAL_QUOTE_READY", "general quote-ready must remain false")

counts = authority.get("counts", {})
require(counts == {
    "acquisitionReceipts": 3,
    "canonicalDriveRegistered": 3,
    "textLayerPresent": 3,
    "derivativeTranscriptions": 1,
    "archivalFacsimilesAmongReceipts": 0,
    "visualClosures": 1,
    "visualPageVerified": 1,
    "boundedTranscriptionVerified": 0,
    "quoteReady": 0,
}, "authority counts drift")

boundaries = authority.get("boundaries", {})
for key in (
    "publicationClaimed", "corpusWideVisualVerificationClaimed", "boundedTranscriptionClaimed",
    "quoteReadyClaimed", "shilovPrimaryFacsimileClaimed", "rawDuplicatesMayBeDeleted", "paidOrdersAuthorized"
):
    require(boundaries.get(key) is False, f"boundary must remain false: {key}")
require(boundaries.get("localizedVisualClosureClaimed") is True, "localized visual closure must remain true")

rows_a = read_csv(ACQ_A)
rows_b = read_csv(ACQ_B)
require(len(rows_a) == 2, "acquisition delta A must contain two rows")
require(len(rows_b) == 1, "acquisition delta B must contain one row")
all_rows = rows_a + rows_b
require({row.get("row") for row in all_rows} == {"51", "52", "53"}, "acquisition receipt row set drift")
for row in all_rows:
    item = next((entry for entry in receipts if str(entry.get("masterRow")) == row.get("row")), None)
    require(item is not None, f"CSV row {row.get('row')} absent from JSON authority")
    if not item:
        continue
    require(row.get("canonical_drive_id") == item.get("canonicalDriveId"), f"CSV row {row.get('row')}: canonical Drive ID drift")
    require(row.get("raw_duplicate_id") == item.get("rawDuplicateDriveId"), f"CSV row {row.get('row')}: raw duplicate ID drift")
    require(row.get("sha256") == item.get("sha256"), f"CSV row {row.get('row')}: SHA drift")
    require(row.get("pages") == str(item.get("pages")), f"CSV row {row.get('row')}: page-count drift")
    require(row.get("bytes") == str(item.get("bytes")), f"CSV row {row.get('row')}: byte-count drift")
    require(row.get("acquisition_state") == "CANONICAL_DRIVE_REGISTERED", f"CSV row {row.get('row')}: acquisition state drift")
    require(row.get("text_state") == "TEXT_LAYER_PRESENT", f"CSV row {row.get('row')}: text state drift")
if rows_b:
    row = rows_b[0]
    require(row.get("source_class") == "DERIVATIVE_TRANSCRIPTION", "Shilov CSV source class drift")
    require(row.get("facsimile_state") == "NOT_ARCHIVAL_FACSIMILE", "Shilov CSV facsimile state drift")
    require(row.get("primary_quote_state") == "NOT_APPROVED", "Shilov CSV quote state drift")

visual_text = read(VISUAL_MD)
for marker in (
    "BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02",
    "1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU",
    "ed381e3ee5764483098fbdda76986953d8d5c7e2ab170e453d38d1a2fd6c23e5",
    "bb3e78a0deb06b437cbf647c09fada131343eb48174d2fa0630809aca639b2ea",
    "BOUNDED_TRANSCRIPTION_PENDING",
    "GENERAL QUOTE-READY: NO",
):
    require(marker in visual_text, f"visual receipt marker missing: {marker}")
require(len(re.findall(r"[0-9a-f]{64}", visual_text)) >= 3, "visual receipt lacks cryptographic identities")

shilov_text = read(SHILOV_MD)
for marker in (
    "SHILOV-LENIN-1919-DERIVATIVE-2026-08-02",
    "12PD_RzFXLcKrIYy9ubfskvRKVPj7FlOc",
    "7c9674b65e15bf76c1833ba0b99b4d735e2c9f3f268351af17f8206516003327",
    "DERIVATIVE_TRANSCRIPTION",
    "NOT ARCHIVAL FACSIMILE",
    "PRIMARY QUOTATION: NOT APPROVED",
    "Microsoft Word",
    "Алексей Синичкин",
):
    require(marker in shilov_text, f"Shilov receipt marker missing: {marker}")
require("архивное факсимиле" not in shilov_text.lower().replace("не архивное факсимиле", ""), "Shilov receipt contains an unqualified facsimile claim")

current_text = read(CURRENT)
for marker in (
    "BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02",
    "FAIL_CLOSED",
    "BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02",
    "BOUNDED_TRANSCRIPTION_PENDING",
    "CORPUS-WIDE VISUAL VERIFICATION: NOT CLAIMED",
    "SHILOV-LENIN-1919-DERIVATIVE-2026-08-02",
    "SHILOV PDF: DERIVATIVE TRANSCRIPTION / NOT ARCHIVAL FACSIMILE / PRIMARY QUOTE NOT APPROVED",
    "PUBLICATION READINESS: NOT CLAIMED",
):
    require(marker in current_text.upper(), f"current authority marker missing: {marker}")

readme_text = read(README)
readme_lower = readme_text.lower()
require("00_CURRENT_AUTHORITY_2026-08-02.md" in readme_text, "README does not point to current authority")
require("операционный" in readme_lower and "каталог" in readme_lower, "README does not define operational catalog role")
require("неизменяем" in readme_lower, "README does not define immutable receipt role")
require("Живой Google Sheets MASTER является каноническим и редактируется append-only." not in readme_text, "obsolete universal MASTER authority statement remains")

if errors:
    print(f"Baptist acquisition authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Baptist acquisition authority: PASS — 3 acquisitions, 1 derivative classification, 1 localized visual closure, 0 quote-ready")
