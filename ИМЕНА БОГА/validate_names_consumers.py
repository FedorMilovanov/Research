#!/usr/bin/env python3
"""Independent NG-02 consumer witness checks; read-only Research contracts only.

This checks the 50 pinned inline locusIds in four existing source snapshots
and 22 general historical snapshots without locusId. It does NOT establish
that any remote Product deploy is compatible with a hypothetical V2 schema.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from validate_names_locus_compat import DATA, load_json, validate_locus_compat

ROOT = Path(__file__).resolve().parent
EXPECTED_CONTRACTS = (
    ("memorial", "data/memorial_attestation_contract_v1.json", "baselineId", 16, "P"),
    ("speech", "data/speech_intertext_contract_v1.json", "baselineId", 12, "P"),
    ("extension", "data/extension_attestation_contract_v1.json", "extensionId", 14, "P"),
    ("core", "data/core_name_lexeme_contract_v1.json", "baselineId", 8, "P"),
    ("general", "data/attestation_contract_v1.json", "baselineId", 22, "G"),
)
EXPECTED_PRODUCT_STATE = "BLOCKED_PENDING_EXTERNAL_CONSUMER_CONTRACT"
EXPECTED_STATUS = "INTERNAL_RESEARCH_CONTRACT_VERIFIED_EXTERNAL_CONSUMERS_NOT_ATTESTED"
CHECK_FIELDS = (
    "verse", "surface", "edition", "sourceUrl",
    "criticalEditionStatus", "rightsState", "publicationState",
)


def validate_consumer_contracts(
    baseline: dict[str, Any],
    extension: dict[str, Any],
    crosswalk: dict[str, Any],
    inventory: dict[str, Any],
    contracts: dict[str, Any],
) -> list[str]:
    errors = validate_locus_compat(baseline, extension, crosswalk)
    if not isinstance(inventory, dict):
        return errors + ["consumer: inventory is not a JSON object"]
    if (inventory.get("schemaVersion") != 1
            or inventory.get("id") != "NG02_CONSUMER_COMPATIBILITY_WITNESS_V1"
            or inventory.get("status") != EXPECTED_STATUS
            or inventory.get("authority") != "RESEARCH_ONLY_NONPRODUCT_NO_LICENSE_OR_MIGRATION_GRANT"
            or inventory.get("scope") != "SOURCE_CONTROL_INTERNAL_ONLY_NO_PRODUCTION_RUNTIME_WITNESS"):
        errors.append("consumer: internal-only evidence authority or status was promoted")
    gate = inventory.get("v2Gate")
    if not isinstance(gate, dict) or (
        gate.get("approval") != EXPECTED_PRODUCT_STATE
        or gate.get("automaticInlineBackfill") is not False
        or gate.get("deploymentEvidence") != "NONE"
        or gate.get("productApprovals") != 0
        or gate.get("criticalManuscriptCollations") != 0
        or gate.get("rightsGrant") != "NOT_ESTABLISHED"
        or gate.get("externalConsumerVerification") != "NOT_COMPLETED"
        or gate.get("compatibilityRule") != "V1_INLINE_50_AND_ABSENT_55_IMMUTABLE_V2_REQUIRES_EXPLICIT_DUAL_READ_VERSIONING"
    ):
        errors.append("consumer: external/V2/rights/critical manuscript gate not independently approved")
    ex = inventory.get("externalCandidates")
    repos = {"FedorMilovanov/gb-is-my-strength", "FedorMilovanov/TheLegendaryPoet", "FedorMilovanov/FedorMilovanov.github.io"}
    if (not isinstance(ex, list) or len(ex) != len(repos)
            or {r.get("repo") for r in ex if isinstance(r, dict)} != repos
            or any(not isinstance(r, dict)
                   or r.get("consumerContract") != "NOT_ATTESTED"
                   or r.get("evidenceLevel") != "READ_ONLY_INDEX_AND_TREE_SEARCH_NO_DIRECT_MATCH_NOT_RUNTIME_PROOF"
                   for r in ex)):
        errors.append("consumer: inspected external repository results are not runtime proofs")
    cfg = inventory.get("internalEvidence")
    expected_cfg = [
        {"id": name, "path": path, "parentKey": parent,
         "expectedWitnesses": count,
         "mode": "PINNED_INLINE_LOCUS" if mode == "P" else "NO_INLINE_LOCUS_GENERIC_WITNESS"}
        for name, path, parent, count, mode in EXPECTED_CONTRACTS
    ]
    if (not isinstance(cfg, dict)
            or cfg.get("internalContracts") != expected_cfg
            or cfg.get("originalAttestations") != 105
            or cfg.get("originalInlineLocusIds") != 50
            or cfg.get("originalMissingInlineLocusIds") != 55
            or cfg.get("internalLocusSnapshotsCovered") != 50
            or cfg.get("generalSnapshotsWithoutLocusId") != 22):
        errors.append("consumer: internal contract inventory/counters changed")
    if not isinstance(contracts, dict):
        return errors + ["consumer: contract docs not an object"]
    witnesses: dict[str, tuple[str, dict]] = {}
    inline: dict[str, tuple[str, dict]] = {}
    for name, doc in (("baseline", baseline), ("extension", extension)):
        rows = doc.get("records") if isinstance(doc, dict) else None
        if not isinstance(rows, list):
            errors.append("consumer: invalid ledger rows")
            continue
        for record in rows:
            if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                errors.append("consumer: invalid source record")
                continue
            observations = record.get("attestations")
            if not isinstance(observations, list):
                errors.append("consumer: invalid attestation list")
                continue
            for witness in observations:
                if not isinstance(witness, dict) or not isinstance(witness.get("attestationId"), str):
                    errors.append("consumer: invalid source witness")
                    continue
                att = witness["attestationId"]
                if att in witnesses:
                    errors.append("consumer: duplicate attestationId source")
                witnesses[att] = (record["id"], witness)
                if witness.get("locusId") is not None:
                    loc = witness.get("locusId")
                    if not isinstance(loc, str) or not loc or loc in inline:
                        errors.append("consumer: malformed/duplicate existing inline locus")
                    else:
                        inline[loc] = (record["id"], witness)
    mappings = crosswalk.get("mappings") if isinstance(crosswalk, dict) else None
    mapped = {}
    if not isinstance(mappings, list):
        return errors + ["consumer: invalid sidecar mappings"]
    for item in mappings:
        if isinstance(item, dict) and isinstance(item.get("attestationId"), str):
            mapped[item["attestationId"]] = item
    covered_inline: set[str] = set()
    covered_general: set[str] = set()
    for name, path, parent_field, count, mode in EXPECTED_CONTRACTS:
        doc = contracts.get(name)
        snapshots = doc.get("lockedAttestations") if isinstance(doc, dict) else None
        if not isinstance(snapshots, list) or len(snapshots) != count:
            errors.append(f"consumer: {name} expected {count} independent lock snapshots")
            continue
        seen_in_group: set[str] = set()
        for snapshot in snapshots:
            if not isinstance(snapshot, dict):
                errors.append(f"consumer: {name} malformed contract witness")
                continue
            rid = snapshot.get(parent_field)
            if not isinstance(rid, str) or not rid:
                errors.append(f"consumer: {name} missing original record link")
                continue
            if mode == "P":
                loc = snapshot.get("locusId")
                witness_pair = inline.get(loc) if isinstance(loc, str) else None
                if witness_pair is None:
                    errors.append(f"consumer: {name} pinned inline locusId lost")
                    continue
                record_id, witness = witness_pair
                aid = witness["attestationId"]
                if aid in seen_in_group or aid in covered_inline:
                    errors.append("consumer: duplicate internal contract witness identity")
                seen_in_group.add(aid)
                covered_inline.add(aid)
                mapping = mapped.get(aid)
                if (not isinstance(mapping, dict)
                    or mapping.get("mode") != "PRESERVE_INLINE_V1"
                    or mapping.get("resolvedLocusId") != loc
                    or mapping.get("recordId") != rid):
                    errors.append(f"consumer: {name} preserved V1 locus not bound to sidecar")
            else:
                if "locusId" in snapshot:
                    errors.append("consumer: generic 22-history contract must remain without locusId")
                candidates = [
                    w for key, (parent_id, w) in witnesses.items()
                    if parent_id == rid and w.get("verse") == snapshot.get("verse")
                    and w.get("surface") == snapshot.get("surface")
                    and w.get("edition") == snapshot.get("edition")
                ]
                if len(candidates) != 1:
                    errors.append("consumer: general contract source witness not unique")
                    continue
                witness = candidates[0]
                aid = witness["attestationId"]
                record_id = rid
                if aid in seen_in_group or aid in covered_general:
                    errors.append("consumer: generic snapshot duplicated")
                seen_in_group.add(aid)
                covered_general.add(aid)
                mapping = mapped.get(aid)
                if (not isinstance(mapping, dict)
                    or mapping.get("mode") != "SIDECAR_ALIAS_ONLY_V1"
                    or witness.get("locusId") is not None):
                    errors.append("consumer: general witness upgraded without V2 schema")
            if record_id != rid:
                errors.append(f"consumer: {name} witness moved to wrong original record")
            for field in CHECK_FIELDS:
                if snapshot.get(field) != witness.get(field):
                    errors.append(f"consumer: {name} exact snapshot field drift ({field})")
    inline_ids = {v["attestationId"] for _, v in inline.values()}
    if len(covered_inline) != 50 or covered_inline != inline_ids:
        errors.append("consumer: 50 pre-existing V1 inline witnesses not fully contract-pinned")
    if len(covered_general) != 22 or covered_general & covered_inline:
        errors.append("consumer: 22 general original snapshots no longer independently bound to sidecar-only witnesses")
    return errors


def main() -> int:
    try:
        b = load_json(DATA / "names_ledger_v1.json")
        e = load_json(DATA / "names_extension_ledger_v1.json")
        compat = load_json(DATA / "names_locus_compat_v1.json")
        inventory = load_json(DATA / "names_consumer_compat_v1.json")
        contracts = {
            name: load_json(ROOT / path)
            for name, path, _, _, _ in EXPECTED_CONTRACTS
        }
        errors = validate_consumer_contracts(b, e, compat, inventory, contracts)
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: consumer contract load/validation: {exc}")
        return 1
    if errors:
        for err in errors:
            print("FAIL: " + err)
        return 1
    print("PASS: consumer witness 50/50 original locus snapshots pinned by four "
          "Research contracts; 22/22 general no-locus snapshots map to sidecar-only "
          "witnesses; 55 inline gaps remain; external Product/Arena NOT ATTESTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
