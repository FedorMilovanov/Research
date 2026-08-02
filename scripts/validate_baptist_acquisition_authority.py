#!/usr/bin/env python3
"""Fail-closed validator for Baptist Drive acquisition and proof-stage authority."""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/baptist-acquisition-proof-authority-2026-08-02.json"
CURRENT = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/00_CURRENT_AUTHORITY_2026-08-02.md"
ACQUISITION_RECEIPT = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/drive_acquisition_delta_2026-08-02.csv"
VISUAL_RECEIPT = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/BAPTIST_1909_NO11_MAZAEV_VISUAL_CLOSURE_2026-08-02.md"
README = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/README.md"

errors: list[str] = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

for path in (AUTH, CURRENT, ACQUISITION_RECEIPT, VISUAL_RECEIPT, README):
    require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

try:
    authority = json.loads(AUTH.read_text(encoding="utf-8"))
except Exception as exc:
    authority = {}
    errors.append(f"invalid authority JSON: {exc}")

expected_receipts = {
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

require(authority.get("schemaVersion") == 2, "schemaVersion drift")
require(authority.get("authorityId") == "BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02", "authorityId drift")
require(authority.get("status") == "CURRENT_FOR_ACQUISITION_AND_PROOF_STAGES_NOT_PUBLICATION", "status drift")
master = authority.get("operationalMaster", {})
require(master.get("driveId") == "1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM", "MASTER Drive ID drift")
require(master.get("acquisitionSheet") == "12 Drive Acquisitions", "acquisition sheet drift")
require(master.get("dossierSheet") == "08 Article Dossiers", "dossier sheet drift")
require(master.get("mutationPolicy") == "APPEND_ONLY_OR_IDEMPOTENT_TARGETED_UPDATE", "MASTER mutation policy drift")
split = authority.get("authoritySplit", {})
require(split.get("driveMasterRole") == "MUTABLE_OPERATIONAL_INVENTORY", "Drive role drift")
require(split.get("githubRole") == "IMMUTABLE_STATUS_SEMANTICS_AND_AUDIT_RECEIPTS", "GitHub role drift")
require(split.get("binaryIdentityRule") == "EXACT_DRIVE_ID_PLUS_SHA256", "binary identity rule drift")
require(split.get("visualIdentityRule") == "EXACT_SOURCE_SHA256_PLUS_PAGE_LOCATOR_PLUS_VISUAL_CARD_DRIVE_ID_AND_SHA256", "visual identity rule drift")
require(split.get("conflictRule") == "FAIL_CLOSED_NO_SILENT_SUPERSESSION", "conflict rule drift")
require(authority.get("stateMachines", {}).get("acquisition") == [
    "LOCATOR_ONLY", "VIEWER_ACCESSIBLE", "BYTES_ACQUIRED", "CANONICAL_DRIVE_REGISTERED"
], "acquisition state machine drift")
require(authority.get("stateMachines", {}).get("proof") == [
    "NO_TEXT", "TEXT_LAYER_PRESENT", "VISUAL_PAGE_VERIFIED", "BOUNDED_TRANSCRIPTION_VERIFIED", "QUOTE_READY"
], "proof state machine drift")

receipts = authority.get("receipts", [])
require(isinstance(receipts, list) and len(receipts) == 2, "exactly two acquisition receipts required")
receipt_by_id = {item.get("id"): item for item in receipts if isinstance(item, dict)}
require(len(receipt_by_id) == 2, "acquisition receipt IDs must be unique")
canonical_ids: set[str] = set()
raw_ids: set[str] = set()
hashes: set[str] = set()
for item_id, spec in expected_receipts.items():
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
require(len(hashes) == 2, "acquisition SHA-256 values must be unique")

visuals = authority.get("visualClosures", [])
require(isinstance(visuals, list) and len(visuals) == 1, "exactly one localized visual closure required")
visual = visuals[0] if visuals and isinstance(visuals[0], dict) else {}
require(visual.get("id") == "BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02", "visual closure ID drift")
source = visual.get("source", {})
require(source == {
    "title": "Баптист 1909 №11.pdf",
    "canonicalDriveId": "1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU",
    "bytes": 9842696,
    "pdfPages": 22,
    "sha256": "0d54f0c2157e76f621bf2fd65137386ae538a792516c473703179bc3127fba73",
    "textLayer": "ABSENT_SCAN_ONLY",
}, "visual closure source identity drift")
locators = visual.get("locators", [])
require(isinstance(locators, list) and len(locators) == 2, "visual closure requires exactly two page locators")
locator_by_page = {item.get("printedPage"): item for item in locators if isinstance(item, dict)}
expected_locators = {
    14: {
        "pdfPage": 14,
        "visualCardDriveId": "1yOm3KBJ9ujtETUG7u-0hl5ijrGiKuXYG",
        "visualCardSha256": "ed381e3ee5764483098fbdda76986953d8d5c7e2ab170e453d38d1a2fd6c23e5",
        "requiredClaims": {"ARTICLE_TITLE_O_PETERBURGSKOI_SVOBODE", "EVANGELICAL_UNION_CRITIQUE_EXISTS", "ARTICLE_CONTINUES_TO_NEXT_PAGE"},
    },
    15: {
        "pdfPage": 15,
        "visualCardDriveId": "1v-7bxYeZ6bMsaiVoFgqz5nWUctOtEwA8",
        "visualCardSha256": "bb3e78a0deb06b437cbf647c09fada131343eb48174d2fa0630809aca639b2ea",
        "requiredClaims": {"ARTICLE_ENDING", "AUTHOR_SIGNATURE_A_M_MAZAEV"},
    },
}
for page, spec in expected_locators.items():
    item = locator_by_page.get(page, {})
    require(item.get("pdfPage") == spec["pdfPage"], f"visual p.{page}: PDF page drift")
    require(item.get("visualCardDriveId") == spec["visualCardDriveId"], f"visual p.{page}: Drive ID drift")
    require(item.get("visualCardSha256") == spec["visualCardSha256"], f"visual p.{page}: SHA drift")
    require(set(item.get("verifies", [])) == spec["requiredClaims"], f"visual p.{page}: claim set drift")
require(visual.get("combinedEvidenceDocumentDriveId") == "1zCwFFMTaOcI476aOP_cXSzgdViWNk4VEySJ2G88W6bY", "combined evidence Doc ID drift")
require(visual.get("canonicalFolderDriveId") == "19AluFtMQ_uV3YTAZMA3U0Raostby779c", "visual canonical folder drift")
require(visual.get("masterDossier") == "08 Article Dossiers!S03", "visual MASTER dossier drift")
require(visual.get("proofState") == "VISUAL_PAGE_VERIFIED", "visual proof state drift")
require(visual.get("transcriptionState") == "BOUNDED_TRANSCRIPTION_PENDING", "transcription must remain pending")
require(visual.get("quoteState") == "NOT_GENERAL_QUOTE_READY", "general quote-ready must remain false")
require(visual.get("receipt") == "RUSSIAN_BAPTISTS_ARCHIVE/BAPTIST_1909_NO11_MAZAEV_VISUAL_CLOSURE_2026-08-02.md", "visual receipt path drift")

counts = authority.get("counts", {})
require(counts == {
    "acquisitionReceipts": 2,
    "canonicalDriveRegistered": 2,
    "textLayerPresent": 2,
    "visualClosures": 1,
    "visualPageVerified": 1,
    "boundedTranscriptionVerified": 0,
    "quoteReady": 0,
}, "authority counts drift")
boundaries = authority.get("boundaries", {})
for key in ("publicationClaimed", "corpusWideVisualVerificationClaimed", "boundedTranscriptionClaimed", "quoteReadyClaimed", "rawDuplicatesMayBeDeleted", "paidOrdersAuthorized"):
    require(boundaries.get(key) is False, f"boundary must remain false: {key}")
require(boundaries.get("localizedVisualClosureClaimed") is True, "localized visual closure must be true")

try:
    with ACQUISITION_RECEIPT.open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
except Exception as exc:
    csv_rows = []
    errors.append(f"invalid acquisition receipt CSV: {exc}")
require(len(csv_rows) == 2, "acquisition receipt CSV must contain exactly two data rows")
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

visual_text = VISUAL_RECEIPT.read_text(encoding="utf-8") if VISUAL_RECEIPT.exists() else ""
for marker in (
    "BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02",
    "1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU",
    "0d54f0c2157e76f621bf2fd65137386ae538a792516c473703179bc3127fba73",
    "1yOm3KBJ9ujtETUG7u-0hl5ijrGiKuXYG",
    "ed381e3ee5764483098fbdda76986953d8d5c7e2ab170e453d38d1a2fd6c23e5",
    "1v-7bxYeZ6bMsaiVoFgqz5nWUctOtEwA8",
    "bb3e78a0deb06b437cbf647c09fada131343eb48174d2fa0630809aca639b2ea",
    "BOUNDED_TRANSCRIPTION_PENDING",
    "GENERAL QUOTE-READY: NO",
):
    require(marker in visual_text, f"visual receipt marker missing: {marker}")
require(len(re.findall(r"[0-9a-f]{64}", visual_text)) >= 3, "visual receipt lacks cryptographic identities")

current_text = CURRENT.read_text(encoding="utf-8") if CURRENT.exists() else ""
readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
for marker in (
    "BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02",
    "FAIL_CLOSED",
    "BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02",
    "BOUNDED_TRANSCRIPTION_PENDING",
    "CORPUS-WIDE VISUAL VERIFICATION: NOT CLAIMED",
    "PUBLICATION READINESS: NOT CLAIMED",
):
    require(marker in current_text.upper(), f"current authority marker missing: {marker}")
readme_lower = readme_text.lower()
require("00_CURRENT_AUTHORITY_2026-08-02.md" in readme_text, "README does not point to current authority")
require("операционный" in readme_lower and "каталог" in readme_lower, "README does not define Drive operational catalog role")
require("неизменяем" in readme_lower, "README does not define immutable GitHub receipt role")
require("Живой Google Sheets MASTER является каноническим и редактируется append-only." not in readme_text, "obsolete universal MASTER authority statement remains")

if errors:
    print(f"Baptist acquisition authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Baptist acquisition authority: PASS — 2 acquisitions, 1 localized visual closure, 0 transcription, 0 quote-ready")
