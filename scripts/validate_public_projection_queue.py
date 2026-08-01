#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE_JSON = ROOT / "data/public-projection-queue-2026-08-01.json"
QUEUE_CSV = ROOT / "data/public-projection-queue-2026-08-01.csv"
RIGHTS_JSON = ROOT / "data/physical-rights-ledger-2026-08-01.json"
RIGHTS_CSV = ROOT / "data/physical-rights-ledger-2026-08-01.csv"
DASHBOARD = ROOT / "PUBLIC_PROJECTION_CURRENT_AUTHORITY_2026-08-01.md"

ALLOWED_DISPOSITIONS = {"PROMOTE", "REFERENCE", "SUPERSEDED", "BLOCKED"}
ALLOWED_HOLDS = {
    "EVIDENCE_HOLD",
    "LOCATOR_HOLD",
    "ARCHIVE_HOLD",
    "RIGHTS_HOLD",
    "PUBLICATION_HOLD",
}
ALLOWED_PHYSICAL = {
    "VERIFIED_COMPLETE_PACKAGE",
    "VERIFIED_FILES_AND_CHECKSUMS_PARTIAL_VIEW",
    "VERIFIED_APPROVED_FOLDER",
    "VERIFIED_REGISTER_NOT_COMPLETE_RUN",
    "VERIFIED_REGISTERS_AND_FINDING_AIDS",
    "NOT_VERIFIED",
    "NOT_VERIFIED_CANONICAL_PACKAGE",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]+$")
DRIVE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,}$")

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}


def load_csv(path: Path):
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid CSV: {exc}")
        return []


queue = load_json(QUEUE_JSON)
rights = load_json(RIGHTS_JSON)
queue_csv = load_csv(QUEUE_CSV)
rights_csv = load_csv(RIGHTS_CSV)

if queue.get("schemaVersion") != 1:
    fail("queue schemaVersion must be 1")
if rights.get("schemaVersion") != 1:
    fail("rights schemaVersion must be 1")
if queue.get("allowedDispositions") != ["PROMOTE", "REFERENCE", "SUPERSEDED", "BLOCKED"]:
    fail("queue disposition vocabulary/order drift")
if set(queue.get("allowedHolds", [])) != ALLOWED_HOLDS:
    fail("queue hold vocabulary drift")

for repo, sha in queue.get("snapshots", {}).items():
    if not SHA_RE.fullmatch(str(sha)):
        fail(f"snapshot {repo} is not an exact 40-character SHA")

rights_records = rights.get("records", [])
rights_by_id = {}
for record in rights_records:
    rid = record.get("id")
    if not rid or rid in rights_by_id:
        fail(f"duplicate or missing rights id: {rid}")
        continue
    rights_by_id[rid] = record
    if record.get("physicalState") not in ALLOWED_PHYSICAL:
        fail(f"{rid}: unsupported physicalState {record.get('physicalState')}")
    objects = record.get("driveObjects")
    if not isinstance(objects, list):
        fail(f"{rid}: driveObjects must be a list")
        objects = []
    if str(record.get("physicalState", "")).startswith("VERIFIED") and not objects:
        fail(f"{rid}: verified physical state requires Drive objects")
    for obj in objects:
        if not DRIVE_ID_RE.fullmatch(str(obj.get("id", ""))):
            fail(f"{rid}: invalid Drive object id")
        if not str(obj.get("title", "")).strip():
            fail(f"{rid}: Drive object title missing")
    if record.get("publicationEligible") is True and record.get("rightsState") != "CLEARED":
        fail(f"{rid}: publicationEligible requires rightsState=CLEARED")
    if record.get("publicationEligible") is False and not record.get("requiredBeforeUse"):
        fail(f"{rid}: non-eligible record requires actionable requiredBeforeUse")

records = queue.get("records", [])
seen = set()
for record in records:
    rid = record.get("id")
    if not ID_RE.fullmatch(str(rid or "")):
        fail(f"invalid queue id: {rid}")
    if rid in seen:
        fail(f"duplicate queue id: {rid}")
    seen.add(rid)

    disposition = record.get("disposition")
    if disposition not in ALLOWED_DISPOSITIONS:
        fail(f"{rid}: unsupported disposition {disposition}")
    holds = record.get("holds")
    if not isinstance(holds, list):
        fail(f"{rid}: holds must be a list")
        holds = []
    for hold in holds:
        if hold not in ALLOWED_HOLDS:
            fail(f"{rid}: vague/unsupported hold {hold}")
    if disposition == "BLOCKED" and not holds:
        fail(f"{rid}: BLOCKED requires at least one typed hold")
    if disposition == "PROMOTE":
        if holds:
            fail(f"{rid}: PROMOTE cannot retain holds")
        if record.get("publicWordingFidelity") != "VERIFIED_FAITHFUL":
            fail(f"{rid}: PROMOTE requires VERIFIED_FAITHFUL wording")
        for rights_id in record.get("rightsLedgerIds", []):
            if not rights_by_id.get(rights_id, {}).get("publicationEligible"):
                fail(f"{rid}: PROMOTE references non-cleared rights record {rights_id}")

    for required in (
        "corpus",
        "researchStatus",
        "sourceAuthorities",
        "targetRepository",
        "targetRouteState",
        "targetPageType",
        "targetClaimIds",
        "publicWordingFidelity",
        "nextAction",
        "forbiddenPromotion",
    ):
        if not record.get(required):
            fail(f"{rid}: missing {required}")

    for authority in record.get("sourceAuthorities", []):
        source = ROOT / authority
        if not source.exists():
            fail(f"{rid}: source authority does not exist: {authority}")

    for route in record.get("targetPublicRoutes", []):
        if not isinstance(route, str) or not route.startswith("/") or not route.endswith("/"):
            fail(f"{rid}: invalid public route {route}")
    if not record.get("targetPublicRoutes") and "NO_" not in record.get("targetRouteState", "") and "RESEARCH_" not in record.get("targetRouteState", ""):
        fail(f"{rid}: empty target routes require an explicit no-route state")

    for rights_id in record.get("rightsLedgerIds", []):
        if rights_id not in rights_by_id:
            fail(f"{rid}: unknown rights ledger id {rights_id}")

expected_counts = {key: 0 for key in ALLOWED_DISPOSITIONS}
for record in records:
    if record.get("disposition") in expected_counts:
        expected_counts[record["disposition"]] += 1
reported = queue.get("counts", {})
for key, value in expected_counts.items():
    if reported.get(key) != value:
        fail(f"queue count drift for {key}: {reported.get(key)} != {value}")
if reported.get("total") != len(records):
    fail("queue total count drift")
if reported.get("alreadyPublic") != sum(bool(r.get("alreadyPublic")) for r in records):
    fail("queue alreadyPublic count drift")
if reported.get("withPhysicalRightsRecords") != sum(bool(r.get("rightsLedgerIds")) for r in records):
    fail("queue physical-rights count drift")

if len(queue_csv) != len(records):
    fail("queue CSV row count differs from JSON")
else:
    csv_by_id = {row.get("id"): row for row in queue_csv}
    if set(csv_by_id) != seen:
        fail("queue CSV ids differ from JSON")
    for record in records:
        row = csv_by_id.get(record["id"], {})
        if row.get("disposition") != record.get("disposition"):
            fail(f"{record['id']}: queue CSV disposition drift")
        if row.get("researchStatus") != record.get("researchStatus"):
            fail(f"{record['id']}: queue CSV researchStatus drift")

if len(rights_csv) != len(rights_records):
    fail("rights CSV row count differs from JSON")
else:
    csv_by_id = {row.get("id"): row for row in rights_csv}
    if set(csv_by_id) != set(rights_by_id):
        fail("rights CSV ids differ from JSON")
    for rid, record in rights_by_id.items():
        row = csv_by_id.get(rid, {})
        if row.get("physicalState") != record.get("physicalState"):
            fail(f"{rid}: rights CSV physicalState drift")
        if row.get("rightsState") != record.get("rightsState"):
            fail(f"{rid}: rights CSV rightsState drift")

try:
    dashboard = DASHBOARD.read_text(encoding="utf-8")
except Exception as exc:
    fail(f"dashboard unreadable: {exc}")
    dashboard = ""
for marker in (
    queue.get("authorityId", ""),
    queue.get("snapshots", {}).get("research", ""),
    f"| `PROMOTE` | **{reported.get('PROMOTE')}** |",
    f"| `REFERENCE` | **{reported.get('REFERENCE')}** |",
    f"| `BLOCKED` | **{reported.get('BLOCKED')}** |",
    "NO AUTOMATIC PROMOTION",
):
    if marker and marker not in dashboard:
        fail(f"dashboard missing marker: {marker}")

if queue.get("policy", {}).get("automaticPromotionForbidden") is not True:
    fail("automatic promotion policy must be true")
if reported.get("PROMOTE") != 0:
    fail("current Agent 06 snapshot must not contain an unreviewed PROMOTE record")

if errors:
    print(f"❌ Agent 06 public projection validation failed ({len(errors)}):", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "✅ Agent 06 projection authority passed: "
    f"{len(records)} records, "
    f"{reported.get('REFERENCE')} reference, "
    f"{reported.get('BLOCKED')} blocked, "
    f"{len(rights_records)} rights records, "
    "0 automatic promotions"
)
