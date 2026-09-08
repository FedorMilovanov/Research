#!/usr/bin/env python3
"""Validate durable cryptographic receipts for the G3 research corpus."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
G3 = REPO / "G3_HISTORY"
MANIFEST = G3 / "DURABLE_CUSTODY_MANIFEST.json"
SOURCE_LEDGER = G3 / "SOURCE_LEDGER.md"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_ID_RE = re.compile(r"^G3-S\d{3}$")

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


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: unreadable custody manifest: {exc}", file=sys.stderr)
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

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        print(f"G3_DURABLE_CUSTODY=FAIL errors={len(errors)}", file=sys.stderr)
        return 2

    print(f"G3_DURABLE_CUSTODY=PASS receipts={len(receipts)} sources={len(source_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
