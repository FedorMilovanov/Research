#!/usr/bin/env python3
"""Validate the composed public-projection authority (base queue + overlays)."""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_JSON = ROOT / "data/public-projection-queue-2026-08-01.json"
BASE_CSV = ROOT / "data/public-projection-queue-2026-08-01.csv"
RIGHTS_JSON = ROOT / "data/physical-rights-ledger-2026-08-01.json"
OVERLAY_JSON = ROOT / "data/public-projection-osk-wave6-overlay-2026-08-01.json"
CURRENT_JSON = ROOT / "data/public-projection-current-2026-08-02.json"
DASHBOARD = ROOT / "PUBLIC_PROJECTION_CURRENT_AUTHORITY_2026-08-01.md"
ROOT_AUTHORITY = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"

ALLOWED_DISPOSITIONS = {"PROMOTE", "REFERENCE", "SUPERSEDED", "BLOCKED"}
ALLOWED_HOLDS = {"EVIDENCE_HOLD", "LOCATOR_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def counts_for(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(record.get("disposition")) for record in records)
    return {
        "PROMOTE": counts["PROMOTE"],
        "REFERENCE": counts["REFERENCE"],
        "SUPERSEDED": counts["SUPERSEDED"],
        "BLOCKED": counts["BLOCKED"],
        "total": len(records),
    }


def apply_osk_overlay(base: dict[str, Any], overlay: dict[str, Any]) -> list[dict[str, Any]]:
    records = base.get("records", [])
    require(isinstance(records, list), "base records must be a list")
    if not isinstance(records, list):
        return []
    target = overlay.get("supersedes_queue_record_id")
    replacement = overlay.get("effective_record")
    require(isinstance(target, str) and bool(target), "overlay target record id missing")
    require(isinstance(replacement, dict), "overlay effective_record must be an object")
    result: list[dict[str, Any]] = []
    matches = 0
    for record in records:
        if not isinstance(record, dict):
            errors.append("base queue contains non-object record")
            continue
        if record.get("id") == target:
            matches += 1
            result.append(dict(replacement) if isinstance(replacement, dict) else record)
        else:
            result.append(record)
    require(matches == 1, f"overlay must replace exactly one base record, found {matches}")
    return result


def validate_record(record: dict[str, Any], rights_ids: set[str]) -> None:
    rid = record.get("id")
    require(isinstance(rid, str) and bool(rid), "projection record missing id")
    disposition = record.get("disposition")
    require(disposition in ALLOWED_DISPOSITIONS, f"{rid}: invalid disposition {disposition!r}")
    holds = record.get("holds", [])
    require(isinstance(holds, list), f"{rid}: holds must be a list")
    if not isinstance(holds, list):
        holds = []
    unknown_holds = sorted(set(holds) - ALLOWED_HOLDS)
    require(not unknown_holds, f"{rid}: unknown holds {unknown_holds}")
    authorities = record.get("sourceAuthorities", [])
    require(isinstance(authorities, list) and authorities, f"{rid}: sourceAuthorities required")
    if isinstance(authorities, list):
        for rel in authorities:
            require(isinstance(rel, str) and (ROOT / rel).is_file(), f"{rid}: missing source authority {rel}")
    record_rights = record.get("rightsLedgerIds", [])
    require(isinstance(record_rights, list), f"{rid}: rightsLedgerIds must be a list")
    if isinstance(record_rights, list):
        missing_rights = sorted(set(record_rights) - rights_ids)
        require(not missing_rights, f"{rid}: missing rights records {missing_rights}")
    if disposition == "PROMOTE":
        require(not holds, f"{rid}: PROMOTE cannot retain holds")
        require(record.get("publicWordingFidelity") == "VERIFIED_FAITHFUL", f"{rid}: PROMOTE requires VERIFIED_FAITHFUL wording")
        require(record.get("alreadyPublic") is True, f"{rid}: PROMOTE requires an existing verified target")


def validate_base_csv(base: dict[str, Any]) -> None:
    try:
        with BASE_CSV.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as exc:
        errors.append(f"cannot read base CSV: {exc}")
        return
    records = base.get("records", [])
    if not isinstance(records, list):
        return
    json_ids = [record.get("id") for record in records if isinstance(record, dict)]
    csv_ids = [row.get("id") for row in rows]
    require(csv_ids == json_ids, "base CSV record order/IDs drift from base JSON")
    for row, record in zip(rows, records):
        require(row.get("disposition") == record.get("disposition"), f"base CSV disposition drift: {record.get('id')}")
        csv_holds = [item for item in (row.get("holds") or "").split("|") if item]
        require(csv_holds == record.get("holds", []), f"base CSV hold drift: {record.get('id')}")


def main() -> int:
    base = load(BASE_JSON)
    rights = load(RIGHTS_JSON)
    overlay = load(OVERLAY_JSON)
    current = load(CURRENT_JSON)
    try:
        dashboard = DASHBOARD.read_text(encoding="utf-8")
        root_authority = ROOT_AUTHORITY.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"authority text read failed: {exc}")
        dashboard = ""
        root_authority = ""

    require(base.get("schemaVersion") == 1, "base queue schemaVersion drift")
    require(base.get("authorityId") == "A06-RESEARCH-PUBLIC-PROJECTION-2026-08-01", "base authorityId drift")
    validate_base_csv(base)

    rights_records = rights.get("records", rights.get("items", []))
    if not isinstance(rights_records, list):
        rights_records = []
        errors.append("rights ledger records/items must be a list")
    rights_ids = {
        str(item.get("id")) for item in rights_records
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    effective = apply_osk_overlay(base, overlay)
    ids = [record.get("id") for record in effective]
    require(len(ids) == len(set(ids)) == 10, "effective queue must contain 10 unique record IDs")
    for record in effective:
        if isinstance(record, dict):
            validate_record(record, rights_ids)

    effective_counts = counts_for(effective)
    require(overlay.get("schema_version") == 2, "OSK overlay schema_version must be 2")
    require(overlay.get("authority_id") == "A06-OSK-CURRENT-PROJECTION-2026-08-02", "OSK overlay authority drift")
    require(overlay.get("effective_projection_counts") == effective_counts, "overlay effective counts drift")
    require(current.get("schemaVersion") == 2 and current.get("status") == "CURRENT", "current projection descriptor drift")
    require(current.get("baseQueue") == BASE_JSON.relative_to(ROOT).as_posix(), "current descriptor baseQueue drift")
    require(current.get("overlays") == [OVERLAY_JSON.relative_to(ROOT).as_posix()], "current descriptor overlay list drift")
    require(current.get("effectiveCounts") == effective_counts, "current descriptor effective counts drift")
    require(current.get("policy", {}).get("baseQueueAloneIsHistorical") is True, "base queue must be explicitly historical alone")

    osk = next((record for record in effective if record.get("id") == "osk-power-dark-side-standalone"), None)
    require(isinstance(osk, dict), "effective OSK record missing")
    if isinstance(osk, dict):
        require(osk.get("disposition") == "REFERENCE", "effective OSK disposition must be REFERENCE")
        require(osk.get("researchStatus") == "WAVES_1_TO_11_RESEARCH_CLOSED_PRODUCT_PUBLICATION_HOLD", "WAVES_1_TO_11 OSK state missing")
        require(osk.get("holds") == ["PUBLICATION_HOLD"], "effective OSK must retain only PUBLICATION_HOLD")
        require("wave11-product-integration-closeout" in osk.get("targetClaimIds", []), "OSK Wave 11 claim marker missing")
        require("Wave 12" in osk.get("nextAction", ""), "OSK next action must name Wave 12")

    require("44_WAVE11_PRODUCT_INTEGRATION_CLOSEOUT_2026-08-01.md" in root_authority, "root authority missing Wave 11 closeout")
    require("Wave 12" in root_authority, "root authority missing Wave 12 route-release stage")
    for marker in (
        "RESEARCH-PUBLIC-PROJECTION-CURRENT-2026-08-02",
        "base + overlay",
        "REFERENCE: 4",
        "BLOCKED: 6",
        "WAVES_1_TO_11_RESEARCH_CLOSED_PRODUCT_PUBLICATION_HOLD",
    ):
        require(marker in dashboard, f"dashboard missing current marker: {marker}")

    if errors:
        print(f"Public projection authority: FAIL ({len(errors)})", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Public projection authority: PASS — base + overlay composed; "
        f"counts={effective_counts}; OSK Waves 1-11 REFERENCE/PUBLICATION_HOLD"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
