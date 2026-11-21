#!/usr/bin/env python3
"""Read-only NG-02 attestationId -> locusId compatibility registry.

Research-only opt-in sidecar: preserves the historical V1 JSON byte-for-byte.
The registry is NOT manuscript evidence, permission to publish, or a Product
migration. No automatic inline locusId writes or guessed biblical labels.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CORPUS = "NAMES_OF_GOD_LOCUS_COMPATIBILITY_V1"
STATUS = "RESEARCH_HOLD_NO_AUTOMATIC_LEDGER_OR_PRODUCT_MUTATION"
COUNT = 105


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _witnesses(baseline: dict, extension: dict) -> tuple[dict[str, tuple[dict, str, str]], list[str]]:
    errors: list[str] = []
    result: dict[str, tuple[dict, str, str]] = {}
    for ledger_name, doc, expected_records in (
        ("baseline", baseline, 29), ("extension", extension, 13)
    ):
        records = doc.get("records") if isinstance(doc, dict) else None
        if not isinstance(records, list) or len(records) != expected_records:
            errors.append(f"compat: {ledger_name} record count/schema changed")
            continue
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                errors.append(f"compat: invalid {ledger_name} record")
                continue
            att = record.get("attestations")
            if not isinstance(att, list):
                errors.append(f"compat: invalid {ledger_name} attestations")
                continue
            for item in att:
                if not isinstance(item, dict):
                    errors.append("compat: invalid witness object")
                    continue
                aid = item.get("attestationId")
                if not isinstance(aid, str) or not aid or aid in result:
                    errors.append("compat: missing/duplicate attestationId")
                    continue
                result[aid] = (item, ledger_name, record["id"])
    if len(result) != COUNT:
        errors.append(f"compat: expected exactly {COUNT} source attestations, got {len(result)}")
    return result, errors


def resolve_locus_id(witness: dict, mapping: dict) -> str:
    """Resolve an explicitly authorized mapping; never synthesize at runtime.

    Raises ValueError on stale source/edition/verse or V1-inline mismatch.
    Consumers must explicitly opt in and keep attestationId as primary key.
    """
    if not isinstance(witness, dict) or not isinstance(mapping, dict):
        raise ValueError("compat: resolver needs witness and mapping objects")
    for key in ("attestationId", "sourceId", "editionId", "verse"):
        if (not isinstance(witness.get(key), str)
                or not witness.get(key) or witness[key] != mapping.get(key)):
            raise ValueError(f"compat: resolver witness binding mismatch ({key})")
    inline = witness.get("locusId")
    mode = mapping.get("mode")
    if mode == "PRESERVE_INLINE_V1":
        if (not isinstance(inline, str) or not inline
                or inline != mapping.get("inlineLocusId")
                or inline != mapping.get("resolvedLocusId")):
            raise ValueError("compat: existing inline locusId changed")
    elif mode == "SIDECAR_ALIAS_ONLY_V1":
        if inline is not None or mapping.get("inlineLocusId") is not None:
            raise ValueError("compat: alias-only witness silently changed inline V1")
        expected = "legacy-" + witness["attestationId"].lower()
        if mapping.get("resolvedLocusId") != expected:
            raise ValueError("compat: historical alias is not stable attestation-derived ID")
    else:
        raise ValueError("compat: unsupported migration mode")
    locus_id = mapping.get("resolvedLocusId")
    if not isinstance(locus_id, str) or not locus_id:
        raise ValueError("compat: missing resolved locusId")
    return locus_id


def validate_locus_compat(baseline: dict, extension: dict, compat: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(compat, dict):
        return ["compat: registry must be an object"]
    if compat.get("schemaVersion") != 1 or compat.get("corpusId") != CORPUS:
        errors.append("compat: wrong schema version or corpus")
    if compat.get("status") != STATUS or compat.get("authority") != "RESEARCH_ONLY_OPT_IN_CROSSWALK_NOT_CANONICAL_MANUSCRIPT_OR_PRODUCT_IDENTITY":
        errors.append("compat: source authority or publication HOLD promoted")
    lifecycle = compat.get("lifecycle")
    if not isinstance(lifecycle, dict) or lifecycle.get("consumers") != "MUST_OPT_IN_TO_RESOLVER_AND_TEST_BEFORE_INLINE_V2_BACKFILL" or lifecycle.get("publication") != "BLOCKED_ZERO_PRODUCT_APPROVALS" or lifecycle.get("currentLedgers") != "PRESERVE_V1_EXACT_BYTES_OF_ALL_105_ATTESTATION_OBSERVATIONS":
        errors.append("compat: unsafe automatic consumer migration or Product promotion")
    original, origin_errors = _witnesses(baseline, extension)
    errors.extend(origin_errors)
    mappings = compat.get("mappings")
    if not isinstance(mappings, list):
        return errors + ["compat: mappings must be a list"]
    by_id: dict[str, dict] = {}
    resolved: set[str] = set()
    inline_count = alias_count = 0
    for row in mappings:
        if not isinstance(row, dict):
            errors.append("compat: non-object mapping")
            continue
        aid = row.get("attestationId")
        if not isinstance(aid, str) or not aid or aid in by_id:
            errors.append("compat: duplicate/invalid mapped attestation ID")
            continue
        by_id[aid] = row
        original_row = original.get(aid)
        if original_row is None:
            errors.append(f"compat: orphan mapped attestation {aid}")
            continue
        witness, ledger_name, record_id = original_row
        if row.get("ledger") != ledger_name or row.get("recordId") != record_id:
            errors.append(f"compat: {aid} original parent ownership changed")
        try:
            loc = resolve_locus_id(witness, row)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if loc in resolved:
            errors.append("compat: duplicate resolved locusId across 105 witnesses")
        resolved.add(loc)
        if row.get("mode") == "PRESERVE_INLINE_V1":
            inline_count += 1
        else:
            alias_count += 1
    if set(by_id) != set(original):
        errors.append("compat: missing or extra 105 witness mappings")
    if len(resolved) != COUNT or inline_count != 50 or alias_count != 55:
        errors.append("compat: 105 unique resolved IDs, 50 inline and 55 aliases required")
    counts = compat.get("counts")
    expected_counts = {
        "baselineRecords": 29, "extensionRecords": 13,
        "totalAttestations": 105, "existingInlineLocusIds": 50,
        "missingInlineLocusIds": 55, "sidecarAliasEntries": 55,
        "resolvedLocusIds": 105, "productApprovals": 0,
    }
    if not isinstance(counts, dict) or counts != expected_counts:
        errors.append("compat: registry counts or Product approvals drifted")
    return errors


def main() -> int:
    try:
        baseline = load_json(DATA / "names_ledger_v1.json")
        extension = load_json(DATA / "names_extension_ledger_v1.json")
        compat = load_json(DATA / "names_locus_compat_v1.json")
        errors = validate_locus_compat(baseline, extension, compat)
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: locus compatibility loading/validation: {exc}")
        return 1
    if errors:
        for item in errors:
            print("FAIL: " + item)
        return 1
    print("PASS: locus compatibility 105/105 unique resolved identifiers, "
          "50 V1 inline preserved, 55 sidecar-only historical aliases; "
          "legacy JSON untouched, Product publication BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
