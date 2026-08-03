#!/usr/bin/env python3
"""Fail-closed validation of the current OSK Wave 12 source-acceptance boundary.

A Product source merge and green exact-head checks are not a production/live
receipt. This validator therefore requires REFERENCE + PUBLICATION_HOLD until a
separate same-release live witness exists and a later authority explicitly
changes the disposition.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "data/public-projection-osk-wave6-overlay-2026-08-01.json"
CURRENT = ROOT / "data/public-projection-current-2026-08-02.json"
AUTHORITY = ROOT / "PUBLIC_PROJECTION_CURRENT_AUTHORITY_2026-08-01.md"
ROOT_AUTHORITY = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"
OSK_ID = "osk-power-dark-side-standalone"
EXPECTED_HEAD = "f39589d8920ae828c13ee5fd804a79433be7bd82"
EXPECTED_MERGE = "e604b97dbbe45cf9ba9e2a84551b799f0dac1a0e"
EXPECTED_ROUTE = "/articles/diotrefy-nashego-vremeni/"
EXPECTED_COUNTS = {"PROMOTE": 0, "REFERENCE": 4, "SUPERSEDED": 0, "BLOCKED": 6, "total": 10}
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


overlay = load(OVERLAY)
current = load(CURRENT)
authority_text = read(AUTHORITY)
root_text = read(ROOT_AUTHORITY)

require(overlay.get("schema_version") == 2, "Wave 12 overlay schema must be 2")
require(overlay.get("authority_id") == "A06-OSK-CURRENT-PROJECTION-2026-08-02", "Wave 12 overlay authority drift")
require(overlay.get("supersedes_queue_record_id") == OSK_ID, "Wave 12 overlay target drift")
require(overlay.get("product_snapshot") == EXPECTED_MERGE, "Wave 12 Product source snapshot drift")
require(overlay.get("effective_projection_counts") == EXPECTED_COUNTS, "Wave 12 effective counts drift")

effective = overlay.get("effective_record")
require(isinstance(effective, dict), "Wave 12 effective record missing")
effective = effective if isinstance(effective, dict) else {}
require(effective.get("id") == OSK_ID, "Wave 12 effective record ID drift")
require(effective.get("disposition") == "REFERENCE", "Wave 12 must remain REFERENCE before live verification")
require(effective.get("holds") == ["PUBLICATION_HOLD"], "Wave 12 must retain PUBLICATION_HOLD")
require(effective.get("targetRouteState") == "WAVE12_SOURCE_ROUTE_MERGED_LIVE_WITNESS_NOT_CLAIMED", "Wave 12 route-state boundary drift")
require(EXPECTED_ROUTE in effective.get("targetPublicRoutes", []), "Wave 12 source route missing")
require(effective.get("separateMediaLaneRequired") is True, "media rights lane must remain separate")
require("same-release production/live witness" in effective.get("nextAction", ""), "Wave 12 next action must require a live witness")

acceptance = effective.get("wave12SourceAcceptance")
require(isinstance(acceptance, dict), "Wave 12 source acceptance missing")
acceptance = acceptance if isinstance(acceptance, dict) else {}
require(acceptance.get("productPullRequest") == 810, "Wave 12 Product PR drift")
require(acceptance.get("exactVerifiedHead") == EXPECTED_HEAD, "Wave 12 exact Product head drift")
require(acceptance.get("sourceMerge") == EXPECTED_MERGE, "Wave 12 Product merge drift")
require(acceptance.get("route") == EXPECTED_ROUTE, "Wave 12 route drift")
require(acceptance.get("exactHeadChecksGreen") is True, "Wave 12 exact-head checks not recorded")
require(acceptance.get("productionVerified") is False, "Wave 12 must not claim production verification")

require(current.get("schemaVersion") == 2, "current projection schema drift")
require(current.get("authorityId") == "RESEARCH-PUBLIC-PROJECTION-CURRENT-2026-08-02", "current projection authority drift")
require(current.get("status") == "CURRENT", "current projection status drift")
require(current.get("overlays") == ["data/public-projection-osk-wave6-overlay-2026-08-01.json"], "current projection overlay composition drift")
require(current.get("productSnapshot") == EXPECTED_MERGE, "current projection Product snapshot drift")
require(current.get("effectiveCounts") == EXPECTED_COUNTS, "current projection counts drift")
require(current.get("policy", {}).get("researchClosureIsNotPublication") is True, "research/publication boundary missing")
require(current.get("policy", {}).get("promoteRequiresNoHolds") is True, "PROMOTE hold policy missing")

for marker in (
    "RESEARCH-PUBLIC-PROJECTION-CURRENT-2026-08-02",
    EXPECTED_MERGE,
    EXPECTED_ROUTE,
    "Production verification:** `NOT CLAIMED`",
    "PUBLICATION_HOLD",
):
    require(marker in authority_text, f"projection authority missing marker: {marker}")
for marker in ("Wave 12 source acceptance", EXPECTED_MERGE, "production/live verification is not claimed"):
    require(marker in root_text, f"root authority missing Wave 12 boundary: {marker}")

if errors:
    print(f"Wave 12 source projection: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Wave 12 source projection: PASS — REFERENCE/PUBLICATION_HOLD; exact source merge green; production unverified")
