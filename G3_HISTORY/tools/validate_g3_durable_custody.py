#!/usr/bin/env python3
"""Validate durable cryptographic receipts for the G3 research corpus."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
G3 = REPO / "G3_HISTORY"
MANIFEST = G3 / "DURABLE_CUSTODY_MANIFEST.json"
SOURCE_LEDGER = G3 / "SOURCE_LEDGER.md"
CUSTODY_POLICY = REPO / "data" / "artifact-custody-policy-v2.json"
PRESERVATION_SOURCE_MANIFEST = G3 / "G3_ACTIONS_PRESERVATION_SOURCE_MANIFEST_2026-11-21.json"
PRESERVATION_RECEIPT = G3 / "G3_ACTIONS_PRESERVATION_CUSTODY_RECEIPT_2026-11-21.json"
EXPIRY_COHORT_ASSESSMENT = G3 / "G3_ACTIONS_2026-11-24_EXPIRY_COHORT_ASSESSMENT_2026-11-21.md"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_ID_RE = re.compile(r"^G3-S\d{3}$")

# Exact authorized scope. This validator deliberately does not treat these eight
# as a receipt for the whole G3 corpus or for any adjacent Actions artifact.
REQUIRED_ACTION_ARTIFACT_IDS = {
    14304253824,
    14305050966,
    14304413494,
    14304577164,
    14304975723,
    14305250133,
    14304199942,
    14305021388,
}

REQUIRED_RECEIPTS = {
    "IRS-FY2022-AMENDED",
    "IRS-FY2023",
    "IRS-FY2024",
    "IRS-FY2025",
    "WAYBACK-LATE-BOARD-20260721102641-RAW",
    "WAYBACK-LATE-BOARD-20260721102641-DECODED",
    "BUCK-TITUS2-SEGMENT-003230-003630",
    "FBC-LINDALE-RSS-CENSUS",
}


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def load_json(path: Path, label: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"unreadable {label}: {exc}")
        return None


def validate_actions_assessment_text(text: str, receipt_ids: set[int], errors: list[str]) -> int:
    """Validate the bounded 38-item assessment against the exact receipt scope.

    The Markdown is a dated metadata record, not a live API response. This gate
    protects its internal boundary: exactly eight IDs are covered by the byte
    receipt and exactly thirty separately enumerated IDs remain unpreserved.
    """
    result_match = re.search(r"^## Result\s*$([\s\S]*?)^## Separate disposition", text, flags=re.M)
    table_match = re.search(
        r"^## Unpreserved G3 entries in the bounded cohort\s*$([\s\S]*?)^## Boundary retained",
        text,
        flags=re.M,
    )
    boundary_match = re.search(r"^## Boundary retained\s*$([\s\S]*)", text, flags=re.M)
    if not result_match or not table_match or not boundary_match:
        errors.append("G3 Actions expiry assessment lost a required bounded-assessment section")
        return 0

    result = result_match.group(1)
    covered_match = re.search(r"covers exactly `8`[\s\S]*?IDs `([0-9, ]+)`", result)
    if not covered_match:
        errors.append("G3 Actions expiry assessment does not enumerate the eight receipt-covered IDs")
        covered_ids: set[int] = set()
    else:
        covered_ids = {int(value.strip()) for value in covered_match.group(1).split(",")}
    if covered_ids != receipt_ids:
        errors.append("G3 Actions expiry assessment covered IDs differ from the exact custody receipt")

    row_re = re.compile(
        r"^\|\s*([^|]+?)\s*\|\s*`(\d+)`\s*\|\s*`(g3-[^`]+)`\s*\|",
        flags=re.M,
    )
    rows = row_re.findall(table_match.group(1))
    unpreserved_ids = [int(artifact_id) for _, artifact_id, _ in rows]
    unique_unpreserved_ids = set(unpreserved_ids)
    if len(rows) != 30 or len(unique_unpreserved_ids) != 30:
        errors.append("G3 Actions expiry assessment must enumerate exactly 30 unique unpreserved artifacts")
    overlap = receipt_ids & unique_unpreserved_ids
    if overlap:
        errors.append(
            "G3 Actions expiry assessment marks receipt-covered IDs unpreserved: "
            + ", ".join(str(value) for value in sorted(overlap))
        )
    if len(receipt_ids | unique_unpreserved_ids) != 38:
        errors.append("G3 Actions expiry assessment no longer partitions the exact 38-item bounded cohort")

    expected_categories = {
        "IRS raw-acquisition output": 8,
        "Wayback board output": 4,
        "Buck supporting-media output": 4,
        "Buck individual-media output": 14,
    }
    categories = Counter(category.strip() for category, _, _ in rows)
    if categories != expected_categories:
        errors.append(f"G3 Actions unpreserved category counts drift: {dict(categories)!r}")

    if "remaining `30`" not in result or "not thereby preserved" not in result:
        errors.append("G3 Actions expiry assessment lost its explicit 30-item non-preservation statement")
    if "NOT_PRESERVED_BY_8_OF_8_RECEIPT" not in text:
        errors.append("G3 Actions expiry assessment lost its non-preservation status")
    boundary = boundary_match.group(1)
    for required in ("PUBLICATION_HOLD", "RIGHTS_HOLD", "EVIDENCE_HOLD", "CATALOG_ONLY"):
        if required not in boundary:
            errors.append(f"G3 Actions expiry assessment boundary lost {required}")
    return len(unique_unpreserved_ids)


def validate_actions_assessment(receipt_ids: set[int], errors: list[str]) -> int:
    try:
        text = EXPIRY_COHORT_ASSESSMENT.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"unreadable G3 Actions expiry assessment: {exc}")
        return 0
    return validate_actions_assessment_text(text, receipt_ids, errors)


def validate_actions_preservation(data: dict, receipts: list[object], errors: list[str]) -> int:
    """Validate the bounded 8/8 private-Drive receipt without contacting Drive.

    This validates the repository's immutable statement of the observed remote
    readback. It intentionally cannot claim that a live Drive object still
    exists at CI time; a fresh connected-app readback is a separate operation.
    """
    source = load_json(PRESERVATION_SOURCE_MANIFEST, "G3 Actions source manifest", errors)
    receipt = load_json(PRESERVATION_RECEIPT, "G3 Actions custody receipt", errors)
    policy = load_json(CUSTODY_POLICY, "artifact custody policy", errors)
    if not isinstance(source, dict) or not isinstance(receipt, dict) or not isinstance(policy, dict):
        return 0

    source_raw = PRESERVATION_SOURCE_MANIFEST.read_bytes()
    source_digest = hashlib.sha256(source_raw).hexdigest()
    if source_raw != canonical_bytes(source):
        errors.append("G3 Actions source manifest is not in its declared canonical JSON form")
    if source.get("schema") != "g3-actions-preservation-source-manifest-v1":
        errors.append("G3 Actions source manifest has an unexpected schema")
    if source.get("manifestId") != "G3-ACTIONS-PRESERVATION-SOURCE-MANIFEST-2026-11-21":
        errors.append("G3 Actions source manifest has an unexpected manifestId")
    source_scope = source.get("scope")
    if not isinstance(source_scope, dict) or source_scope.get("authorizedArtifactCount") != 8:
        errors.append("G3 Actions source manifest lost its exact eight-artifact scope")
    if not isinstance(source_scope, dict) or source_scope.get("unpackOrRepackAuthorized") is not False:
        errors.append("G3 Actions source manifest must keep unpack/repack unauthorized")

    source_rows = source.get("artifacts")
    if not isinstance(source_rows, list):
        errors.append("G3 Actions source manifest artifacts must be a list")
        source_rows = []
    source_by_id: dict[int, dict] = {}
    for index, row in enumerate(source_rows):
        if not isinstance(row, dict):
            errors.append(f"G3 Actions source manifest artifact[{index}] is not an object")
            continue
        aid = row.get("githubActionsArtifactId")
        if not isinstance(aid, int):
            errors.append(f"G3 Actions source manifest artifact[{index}] lacks integer GitHub artifact ID")
            continue
        if aid in source_by_id:
            errors.append(f"G3 Actions source manifest has duplicate artifact ID {aid}")
        source_by_id[aid] = row
        for field in ("sourceArtifactName", "sourceRepository", "sourceWorkflowDefinition", "sourceArtifactApiLocator"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"G3 Actions source {aid}: missing {field}")
        if not isinstance(row.get("sourceWorkflowRun"), int) or row["sourceWorkflowRun"] <= 0:
            errors.append(f"G3 Actions source {aid}: invalid sourceWorkflowRun")
        if not isinstance(row.get("sourceArchiveBytes"), int) or row["sourceArchiveBytes"] <= 0:
            errors.append(f"G3 Actions source {aid}: invalid sourceArchiveBytes")
        sha = row.get("sourceArchiveSha256")
        if not isinstance(sha, str) or not SHA256_RE.fullmatch(sha):
            errors.append(f"G3 Actions source {aid}: invalid sourceArchiveSha256")
        elif row.get("sourceArtifactApiDigest") != f"sha256:{sha}":
            errors.append(f"G3 Actions source {aid}: provider digest does not pin sourceArchiveSha256")
    if set(source_by_id) != REQUIRED_ACTION_ARTIFACT_IDS:
        errors.append(
            "G3 Actions source manifest scope differs from the exact authorized artifact IDs: "
            + ", ".join(str(aid) for aid in sorted(set(source_by_id) ^ REQUIRED_ACTION_ARTIFACT_IDS))
        )

    if receipt.get("schema") != "g3-actions-preservation-custody-receipt-v1":
        errors.append("G3 Actions custody receipt has an unexpected schema")
    if receipt.get("receiptId") != "G3-ACTIONS-PRESERVATION-CUSTODY-RECEIPT-2026-11-21":
        errors.append("G3 Actions custody receipt has an unexpected receiptId")
    if receipt.get("status") != "ACQUIRED_DURABLE_8_OF_8_PRIVATE_DRIVE_READBACK_VERIFIED":
        errors.append("G3 Actions custody receipt lost its exact bounded verification state")
    if receipt.get("custodyState") != "ACQUIRED_DURABLE":
        errors.append("G3 Actions custody receipt must remain ACQUIRED_DURABLE")
    if receipt.get("policyAuthority") != policy.get("authorityId"):
        errors.append("G3 Actions custody receipt has the wrong custody-policy authority")
    if receipt.get("sourceManifestSha256") != source_digest:
        errors.append("G3 Actions custody receipt sourceManifestSha256 does not match source manifest bytes")
    receipt_source = receipt.get("sourceManifest")
    if not isinstance(receipt_source, dict) or receipt_source.get("sha256") != source_digest:
        errors.append("G3 Actions custody receipt lacks the matching source-manifest receipt")
    if not isinstance(receipt_source, dict) or receipt_source.get("driveRawReadbackVerified") is not True:
        errors.append("G3 Actions source-manifest Drive readback is not explicitly verified")

    scope = receipt.get("scope")
    if not isinstance(scope, dict) or scope.get("artifactCountAuthorized") != 8 or scope.get("artifactCountPresentAndVerified") != 8:
        errors.append("G3 Actions custody receipt lost its 8/8 scope count")
    if not isinstance(scope, dict) or scope.get("sourceZipHandling") != "Original ZIP custody only; no unpacking to a destination, modification, replacement, or repacking.":
        errors.append("G3 Actions custody receipt lost its original-ZIP handling boundary")
    legal = receipt.get("publicationAndLegalBoundary")
    if not isinstance(legal, dict) or legal.get("publicationState") != "BLOCKED" or legal.get("rightsState") != "PRIVATE_STUDY_ONLY":
        errors.append("G3 Actions custody receipt lost publication/rights boundary")
    if not isinstance(legal, dict) or set(legal.get("holds", [])) != {"PUBLICATION_HOLD", "RIGHTS_HOLD", "EVIDENCE_HOLD"}:
        errors.append("G3 Actions custody receipt lost mandatory holds")

    required_fields = policy.get("durableReceiptRequiredFields")
    if not isinstance(required_fields, list) or not all(isinstance(field, str) for field in required_fields):
        errors.append("custody policy lacks a usable durableReceiptRequiredFields list")
        required_fields = []
    artifact_rows = receipt.get("artifacts")
    if not isinstance(artifact_rows, list):
        errors.append("G3 Actions custody receipt artifacts must be a list")
        artifact_rows = []
    receipt_by_id: dict[int, dict] = {}
    for index, row in enumerate(artifact_rows):
        if not isinstance(row, dict):
            errors.append(f"G3 Actions custody artifact[{index}] is not an object")
            continue
        aid = row.get("githubActionsArtifactId")
        if not isinstance(aid, int):
            errors.append(f"G3 Actions custody artifact[{index}] lacks integer GitHub artifact ID")
            continue
        if aid in receipt_by_id:
            errors.append(f"G3 Actions custody receipt has duplicate artifact ID {aid}")
        receipt_by_id[aid] = row
        missing_fields = [field for field in required_fields if field not in row]
        if missing_fields:
            errors.append(f"G3 Actions custody artifact {aid}: missing policy fields {', '.join(missing_fields)}")
            continue
        source_row = source_by_id.get(aid)
        if source_row is None:
            errors.append(f"G3 Actions custody artifact {aid}: absent from source manifest")
            continue
        if row.get("sourceArtifactName") != source_row.get("sourceArtifactName"):
            errors.append(f"G3 Actions custody artifact {aid}: source artifact name drift")
        if row.get("sourceWorkflowRun") != source_row.get("sourceWorkflowRun"):
            errors.append(f"G3 Actions custody artifact {aid}: source workflow run drift")
        if row.get("sourceManifestSha256") != source_digest:
            errors.append(f"G3 Actions custody artifact {aid}: source manifest digest drift")
        destination_digest = row.get("destinationSha256Readback")
        if not isinstance(destination_digest, str) or not SHA256_RE.fullmatch(destination_digest):
            errors.append(f"G3 Actions custody artifact {aid}: invalid destination SHA-256 readback")
        elif destination_digest != source_row.get("sourceArchiveSha256"):
            errors.append(f"G3 Actions custody artifact {aid}: source provider digest/readback mismatch")
        if row.get("destinationSha256DriveMetadata") != destination_digest:
            errors.append(f"G3 Actions custody artifact {aid}: Drive SHA-256 metadata/readback mismatch")
        if row.get("sourceArtifactApiDigest") != source_row.get("sourceArtifactApiDigest"):
            errors.append(f"G3 Actions custody artifact {aid}: GitHub API digest drift")
        if row.get("destinationBytes") != source_row.get("sourceArchiveBytes") or row.get("sourceArchiveBytes") != source_row.get("sourceArchiveBytes"):
            errors.append(f"G3 Actions custody artifact {aid}: source/destination byte count mismatch")
        if row.get("destinationProvider") != "Google Drive" or not isinstance(row.get("destinationObjectId"), str):
            errors.append(f"G3 Actions custody artifact {aid}: destination provider/object ID invalid")
        if row.get("sourceProviderDigestEqualsDestinationReadback") is not True or row.get("driveMetadataSha256EqualsDestinationReadback") is not True:
            errors.append(f"G3 Actions custody artifact {aid}: digest equivalence flags are incomplete")
        zip_integrity = row.get("zipIntegrity")
        if not isinstance(zip_integrity, dict) or zip_integrity.get("passed") is not True or zip_integrity.get("extractedToFilesystem") is not False or zip_integrity.get("repacked") is not False:
            errors.append(f"G3 Actions custody artifact {aid}: ZIP integrity/no-repack boundary is incomplete")
        permissions = row.get("directPermissionCheck")
        if not isinstance(permissions, dict) or permissions.get("activePermissionCount") != 1 or permissions.get("publicOrDomainPermissionObserved") is not False:
            errors.append(f"G3 Actions custody artifact {aid}: private direct-permission check is incomplete")
    if set(receipt_by_id) != REQUIRED_ACTION_ARTIFACT_IDS:
        errors.append(
            "G3 Actions custody receipt scope differs from exact authorized artifact IDs: "
            + ", ".join(str(aid) for aid in sorted(set(receipt_by_id) ^ REQUIRED_ACTION_ARTIFACT_IDS))
        )
    if isinstance(scope, dict) and isinstance(artifact_rows, list):
        total = sum(row.get("destinationBytes", 0) for row in artifact_rows if isinstance(row, dict) and isinstance(row.get("destinationBytes"), int))
        if scope.get("totalDestinationBytes") != total or total != 2807235:
            errors.append("G3 Actions custody receipt total byte count drift")

    register_by_id = {row.get("id"): row for row in receipts if isinstance(row, dict)}
    for aid, artifact in receipt_by_id.items():
        rid = f"G3-ACTIONS-ARTIFACT-{aid}"
        register = register_by_id.get(rid)
        if not isinstance(register, dict):
            errors.append(f"durable custody register missing {rid}")
            continue
        if (register.get("sourceArtifactId") != aid or register.get("objectId") != artifact.get("destinationObjectId")
                or register.get("sha256") != artifact.get("destinationSha256Readback")
                or register.get("custodyState") != "ACQUIRED_DURABLE"
                or register.get("publicationState") != "BLOCKED"
                or register.get("rawBytesInGit") is not False):
            errors.append(f"durable custody register drift for {rid}")

    receipt_sets = data.get("supplementalCustodyReceiptSets")
    matching_sets = [
        row for row in receipt_sets if isinstance(row, dict)
        and row.get("id") == receipt.get("receiptId")
    ] if isinstance(receipt_sets, list) else []
    if len(matching_sets) != 1:
        errors.append("durable custody register must contain exactly one matching supplemental G3 Actions receipt set")
    else:
        receipt_set = matching_sets[0]
        if (receipt_set.get("artifactCount") != 8
                or receipt_set.get("totalDestinationBytes") != 2807235
                or receipt_set.get("sourceManifestSha256") != source_digest
                or receipt_set.get("receiptRepositoryPath") != str(PRESERVATION_RECEIPT.relative_to(REPO))):
            errors.append("supplemental G3 Actions receipt-set register fields drift")

    validate_actions_assessment(set(receipt_by_id), errors)
    return len(receipt_by_id)


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: unreadable custody manifest: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("ERROR: durable custody manifest root is not an object", file=sys.stderr)
        return 2

    if data.get("schema") != "g3-durable-custody-receipts-v1":
        errors.append(f"unexpected schema: {data.get('schema')!r}")
    if "PUBLICATION_HOLD" not in str(data.get("status", "")):
        errors.append("manifest status lost PUBLICATION_HOLD")

    source_ids = set(re.findall(r"^\|\s*(G3-S\d{3})\s*\|", SOURCE_LEDGER.read_text(encoding="utf-8"), flags=re.M))
    receipts = data.get("receipts")
    if not isinstance(receipts, list) or not receipts:
        errors.append("receipts must be a non-empty list")
        receipts = []

    seen: set[str] = set()
    for index, receipt in enumerate(receipts):
        if not isinstance(receipt, dict):
            errors.append(f"receipt[{index}] is not an object")
            continue
        rid = receipt.get("id")
        if not isinstance(rid, str) or not rid:
            errors.append(f"receipt[{index}] has invalid id")
            continue
        if rid in seen:
            errors.append(f"duplicate receipt id: {rid}")
        seen.add(rid)

        digest = receipt.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"{rid}: sha256 is not exact 64-char lowercase hex")
        if receipt.get("durableReceipt") is not True:
            errors.append(f"{rid}: durableReceipt must be true")
        if receipt.get("rawBytesInGit") is not False:
            errors.append(f"{rid}: rawBytesInGit must remain false unless policy is explicitly redesigned")
        obj = receipt.get("objectId")
        if not isinstance(obj, str) or not obj.strip():
            errors.append(f"{rid}: missing objectId/locator")

        sid = receipt.get("sourceId")
        if sid is not None:
            if not isinstance(sid, str) or not SOURCE_ID_RE.fullmatch(sid):
                errors.append(f"{rid}: invalid sourceId {sid!r}")
            elif sid not in source_ids:
                errors.append(f"{rid}: sourceId {sid} is absent from SOURCE_LEDGER")

    missing = sorted(REQUIRED_RECEIPTS - seen)
    if missing:
        errors.append("missing required durable receipts: " + ", ".join(missing))

    g3_actions_artifacts = validate_actions_preservation(data, receipts, errors)

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        print(f"G3_DURABLE_CUSTODY=FAIL errors={len(errors)}", file=sys.stderr)
        return 2

    print(
        f"G3_DURABLE_CUSTODY=PASS receipts={len(receipts)} sources={len(source_ids)} "
        f"g3_actions_artifacts={g3_actions_artifacts}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
