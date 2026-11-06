#!/usr/bin/env python3
"""Read-only, fail-closed structural checks for Names of God RESEARCH ledger.

This checks data contracts, NOT the accuracy of Hebrew/Greek, critical editions,
external URLs, licenses or publication approval. It must never modify files.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parent / "data" / "names_ledger_v1.json"
ALLOWED_CLASSES = {"A1", "A2", "A3", "B1", "C", "D"}
ALLOWED_ACCESS = {"FULL_OBJECT_VERIFIED", "PARTIAL_OBJECT", "CATALOG_ONLY", "LINK_ONLY", "NOT_ACQUIRED"}
ALLOWED_LOCATOR = {"EXACT_LOCATOR_VERIFIED", "COARSE_LOCATOR_ONLY", "LOCATOR_MISSING"}
ALLOWED_RIGHTS = {"PUBLICATION_ELIGIBLE", "STORAGE_ONLY", "PRIVATE_STUDY_ONLY", "PERMISSION_REQUIRED", "RIGHTS_UNKNOWN"}
ALLOWED_PUBLICATION = {"PROMOTE", "REFERENCE", "SUPERSEDED", "BLOCKED"}
ALLOWED_HOLDS = {"EVIDENCE_HOLD", "LOCATOR_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
ALLOWED_LANGUAGES = {"hebrew", "greek", "aramaic", "aramaic_transliterated_in_greek", "hebrew_and_greek"}
EXPECTED_TYPES = {
    "yhwh": "personal_divine_name",
    "yireh": "place_name",
    "nissi": "altar_name",
    "shalom": "altar_name",
    "shammah": "city_name",
    "el-bethel": "place_name",
    "rapha": "predication_about_yhwh",
    "ro-i": "predication_about_yhwh",
    "mekoddishkem": "predication_about_yhwh",
    "tsidkenu": "symbolic_royal_and_city_name",
}
HEBREW = re.compile(r"[\u0590-\u05ff]")
GREEK = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
URL = re.compile(r"^https://[^\s]+$")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Ledger must be a JSON object"]
    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if data.get("corpusId") != "NAMES_OF_GOD":
        errors.append("unexpected corpusId")
    rows = data.get("records")
    if not isinstance(rows, list):
        return errors + ["records must be a list"]
    if len(rows) != 29:
        errors.append(f"Arena baseline must keep 29 rows, got {len(rows)}; new discoveries belong in a separate extension ledger")
    ids: set[str] = set()
    for i, row in enumerate(rows, start=1):
        prefix = f"records[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: expected object")
            continue
        rid = row.get("id")
        if not isinstance(rid, str) or not rid:
            errors.append(f"{prefix}: missing id")
            continue
        prefix = rid
        if rid in ids:
            errors.append(f"{prefix}: duplicate id")
        ids.add(rid)
        if row.get("arenaOrder") != i:
            errors.append(f"{prefix}: arenaOrder must remain {i}")
        for field in ("arenaLabel", "language", "verifiedForm", "verseLocator", "category", "sourceEdition", "sourceUrl"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{prefix}: {field} must be nonblank")
        form = row.get("verifiedForm", "")
        lang = row.get("language")
        if lang not in ALLOWED_LANGUAGES:
            errors.append(f"{prefix}: unknown language {lang!r}")
        if isinstance(form, str):
            if lang in {"hebrew", "aramaic"} and not HEBREW.search(form):
                errors.append(f"{prefix}: Hebrew/Aramaic text missing Hebrew-script letters")
            if lang in {"greek", "aramaic_transliterated_in_greek"} and not GREEK.search(form):
                errors.append(f"{prefix}: Greek-script form missing Greek letters")
            if lang == "hebrew_and_greek" and not (HEBREW.search(form) and GREEK.search(form)):
                errors.append(f"{prefix}: mixed-script witness must have both Hebrew and Greek")
        if row.get("category") == "personal_divine_name" and rid != "yhwh":
            errors.append(f"{prefix}: cannot silently promote to personal_divine_name")
        expected = EXPECTED_TYPES.get(rid)
        if expected and row.get("category") != expected:
            errors.append(f"{prefix}: referent/syntax regression; expected category {expected}")
        for field, allowed in (
            ("evidenceClass", ALLOWED_CLASSES), ("accessState", ALLOWED_ACCESS),
            ("locatorState", ALLOWED_LOCATOR), ("rightsState", ALLOWED_RIGHTS),
            ("publicationState", ALLOWED_PUBLICATION),
        ):
            if row.get(field) not in allowed:
                errors.append(f"{prefix}: invalid {field}")
        holds = row.get("holds")
        if not isinstance(holds, list) or any(h not in ALLOWED_HOLDS for h in holds):
            errors.append(f"{prefix}: invalid holds")
            holds = []
        if row.get("publicationState") != "BLOCKED" or "PUBLICATION_HOLD" not in holds:
            errors.append(f"{prefix}: publication unblocked without separate approval")
        if row.get("criticalEditionStatus") != "NOT_COLLATED":
            errors.append(f"{prefix}: critical collation state changed; research review required")
        if row.get("claimScope") != "VERIFIED_DIGITAL_SURFACE_ONLY":
            errors.append(f"{prefix}: claim scope must not be inflated")
        if not URL.match(str(row.get("sourceUrl", ""))):
            errors.append(f"{prefix}: sourceUrl must be explicit https URL")
        if "SEPTUAGINTA_SBL.pdf" in str(row.get("sourceUrl", "")):
            errors.append(f"{prefix}: obsolete unverified LXX PDF locator")
        witnesses = row.get("witnesses", [])
        if not isinstance(witnesses, list):
            errors.append(f"{prefix}: witnesses must be a list")
        else:
            for index, witness in enumerate(witnesses):
                if not isinstance(witness, dict):
                    errors.append(f"{prefix}: witnesses[{index}] must be an object")
                elif not URL.match(str(witness.get("sourceUrl", ""))):
                    errors.append(f"{prefix}: witnesses[{index}] has no explicit https source URL")
        if rid == "tsidkenu" and (not isinstance(witnesses, list) or len(witnesses) < 3):
            errors.append(f"{prefix}: must retain both MT referents and Old Greek absence marker")
        if rid == "immanuel" and (not isinstance(witnesses, list) or len(witnesses) < 2):
            errors.append(f"{prefix}: must retain both Isaiah Hebrew and Matthew Greek witnesses")

    counts = data.get("counts", {})
    if not isinstance(counts, dict):
        errors.append("counts must be object")
    else:
        count = sum(r.get("textCheck") == "EXACT_VERSE_CHECKED_IN_NAMED_DIGITAL_EDITION" for r in rows if isinstance(r, dict))
        if counts.get("arenaCandidateCount") != len(rows) or counts.get("exactDigitalVerseChecks") != count:
            errors.append("counts: machine status totals do not match records")
        if counts.get("criticalEditionCollationsCompleted") != 0 or counts.get("publicationEligible") != 0:
            errors.append("counts: critical/publication status must remain zero absent evidence")
    if "derived_from_yhwh" in json.dumps(data, ensure_ascii=False):
        errors.append("derived_from_yhwh forbidden in data model without review")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    args = parser.parse_args()
    try:
        with args.ledger.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read ledger: {exc}", file=sys.stderr)
        return 1
    issues = validate(data)
    if issues:
        for issue in issues:
            print("FAIL:", issue, file=sys.stderr)
        return 1
    print(f"PASS: {len(data['records'])} Arena baseline rows; publication blocked. "
          "This is a STRUCTURAL test, not an external text/rights check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
