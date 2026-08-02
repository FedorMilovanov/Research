#!/usr/bin/env python3
"""Fail-closed validation of the Wave 12 public-projection composition.

The effective projection is never trusted as an independently edited snapshot.
It must equal the historical base queue with exactly one OSK record replaced by
an overlay backed by Product CI and production-readback receipts.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/public-projection-queue-2026-08-01.json"
OVERLAY = ROOT / "data/public-projection-osk-wave12-overlay-2026-08-02.json"
RECEIPT = ROOT / "data/osk-wave12-product-release-receipt-2026-08-02.json"
CI_RECEIPTS = ROOT / "data/stage-ci-receipts-2026-08-02.json"
CURRENT = ROOT / "data/public-projection-current-2026-08-02-v2.json"
AUTHORITY = ROOT / "PUBLIC_PROJECTION_CURRENT_AUTHORITY_2026-08-02_V2.md"
RELEASE = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/45_WAVE12_PRODUCT_PUBLICATION_RELEASE_2026-08-02.md"
OSK_ID = "osk-power-dark-side-standalone"
EXPECTED_COUNTS = {"PROMOTE": 1, "REFERENCE": 3, "SUPERSEDED": 0, "BLOCKED": 6, "total": 10}
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


def first(obj: dict[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in obj:
            return obj[name]
    return default


def records(obj: dict[str, Any]) -> list[dict[str, Any]]:
    value = first(obj, "records", "queue", "items", default=[])
    if isinstance(value, dict):
        value = value.get("records", [])
    if not isinstance(value, list):
        errors.append("projection records must be a list")
        return []
    bad = [index for index, row in enumerate(value) if not isinstance(row, dict)]
    require(not bad, f"projection contains non-object records at {bad}")
    return [row for row in value if isinstance(row, dict)]


def record_id(row: dict[str, Any]) -> str:
    value = first(row, "id", "recordId", "record_id", default="")
    return value.strip() if isinstance(value, str) else ""


def disposition(row: dict[str, Any]) -> str:
    value = first(row, "disposition", "publicationDisposition", default="")
    return value.strip() if isinstance(value, str) else ""


def normalized(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalized(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalized(item) for item in value]
    return value


def count_records(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(disposition(row) for row in rows)
    return {
        "PROMOTE": counts["PROMOTE"],
        "REFERENCE": counts["REFERENCE"],
        "SUPERSEDED": counts["SUPERSEDED"],
        "BLOCKED": counts["BLOCKED"],
        "total": len(rows),
    }


def receipt_success(receipt: dict[str, Any]) -> bool:
    status_values = {
        str(first(receipt, "status", "conclusion", "state", default="")).upper(),
        str(first(receipt, "ciConclusion", "ci_conclusion", default="")).upper(),
        str(first(receipt, "productionConclusion", "production_conclusion", default="")).upper(),
    }
    explicit = [
        first(receipt, "ciPassed", "ci_passed"),
        first(receipt, "productionReadbackPassed", "production_readback_passed"),
        first(receipt, "liveReadbackPassed", "live_readback_passed"),
    ]
    return (
        any(value in {"SUCCESS", "PASSED", "PASS", "PUBLIC_ROUTE_LIVE_VERIFIED"} for value in status_values)
        or any(value is True for value in explicit)
    )


base = load(BASE)
overlay = load(OVERLAY)
receipt = load(RECEIPT)
ci_receipts = load(CI_RECEIPTS)
current = load(CURRENT)

base_rows = records(base)
current_rows = records(current)
require(len(base_rows) == 10, f"historical base must contain 10 records, found {len(base_rows)}")
require(len(current_rows) == 10, f"effective projection must contain 10 records, found {len(current_rows)}")
require(len({record_id(row) for row in base_rows}) == len(base_rows), "base record IDs must be unique")
require(len({record_id(row) for row in current_rows}) == len(current_rows), "current record IDs must be unique")

base_osk = [row for row in base_rows if record_id(row) == OSK_ID]
current_osk = [row for row in current_rows if record_id(row) == OSK_ID]
require(len(base_osk) == 1, "base queue must contain exactly one OSK record")
require(len(current_osk) == 1, "current projection must contain exactly one OSK record")

effective = first(overlay, "effective_record", "effectiveRecord", default={})
require(isinstance(effective, dict), "Wave 12 overlay effective record must be an object")
effective = effective if isinstance(effective, dict) else {}
require(record_id(effective) == OSK_ID, "Wave 12 overlay replaces the wrong record")
require(disposition(effective) == "PROMOTE", "Wave 12 OSK disposition must be PROMOTE")
require(first(effective, "holds", default=None) == [], "Wave 12 OSK record must have no remaining holds")
require(first(effective, "alreadyPublic", "already_public") is True, "Wave 12 OSK route must be marked public")
require("/articles/diotrefy-nashego-vremeni/" in first(effective, "targetPublicRoutes", "target_public_routes", default=[]), "Wave 12 public route missing")
require(first(effective, "separateMediaLaneRequired", "separate_media_lane_required") is False, "Wave 12 article must not retain an artificial media-lane hold")

composed: list[dict[str, Any]] = []
for row in base_rows:
    composed.append(effective if record_id(row) == OSK_ID else row)
require(normalized(composed) == normalized(current_rows), "current v2 projection is not exactly base + Wave 12 overlay")

actual_counts = count_records(current_rows)
require(actual_counts == EXPECTED_COUNTS, f"effective projection counts drift: {actual_counts} != {EXPECTED_COUNTS}")
for declared in (
    first(overlay, "effective_projection_counts", "effectiveProjectionCounts", default={}),
    first(current, "effective_projection_counts", "effectiveProjectionCounts", "counts", default={}),
):
    if declared:
        require(declared == EXPECTED_COUNTS, f"declared projection counts drift: {declared}")

require(first(overlay, "authority_id", "authorityId") == "A06-OSK-WAVE12-PROJECTION-2026-08-02", "Wave 12 overlay authority ID drift")
require(first(overlay, "supersedes_authority_id", "supersedesAuthorityId") in {"A06-OSK-WAVE6-PROJECTION-2026-08-01", None}, "unexpected overlay supersession")
require(first(current, "authority_id", "authorityId") == "A06-RESEARCH-PUBLIC-PROJECTION-2026-08-02-V2", "current projection authority ID drift")
required_overlay = first(current, "required_overlay_authority_id", "requiredOverlayAuthorityId", default="")
if required_overlay:
    require(required_overlay == "A06-OSK-WAVE12-PROJECTION-2026-08-02", "current authority points to wrong overlay")

require(receipt_success(receipt), "Product release receipt does not prove successful CI/live readback")
receipt_route = first(receipt, "route", "publicRoute", "public_route", default="")
require(receipt_route == "/articles/diotrefy-nashego-vremeni/", "Product receipt route drift")
require(first(receipt, "newDirectQuotesApproved", "new_direct_quotes_approved", default=0) in {0, False}, "Product receipt must preserve zero new direct quotes")
product_authority = first(receipt, "authorityId", "authority_id", default="")
require(product_authority == "RESEARCH-OSK-WAVE12-PRODUCT-RELEASE-RECEIPT-2026-08-02", "Research release receipt authority drift")

ci_text = json.dumps(ci_receipts, ensure_ascii=False).upper()
for marker in ("DIOTROPHES", "WAVE12", "SUCCESS"):
    require(marker in ci_text, f"stage CI receipt missing marker: {marker}")

for path, markers in (
    (AUTHORITY, ("A06-RESEARCH-PUBLIC-PROJECTION-2026-08-02-V2", "PROMOTE", "Wave 12")),
    (RELEASE, ("RESEARCH-OSK-WAVE12-PRODUCT-RELEASE-RECEIPT-2026-08-02", "PUBLIC", "0")),
):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        continue
    for marker in markers:
        require(marker in text, f"{path.relative_to(ROOT)} missing marker: {marker}")
    for forbidden in ("TODO", "TBD", "PUBLICATION_HOLD"):
        require(forbidden not in text, f"{path.relative_to(ROOT)} contains unresolved marker: {forbidden}")

if errors:
    print(f"Wave 12 public projection: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Wave 12 public projection: PASS — base + required overlay, PROMOTE=1, holds=0, live receipt verified")
