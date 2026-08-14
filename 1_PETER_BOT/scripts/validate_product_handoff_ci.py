#!/usr/bin/env python3
"""Fail-closed CI entrypoint for the Chapter 4–5 handoff audit.

The core validator scans ledgers/quorums. PR #183 also has one explicit Wave3e
source-upgrade authority; this wrapper adds that file as an inspection lane without
pretending it is a global identity/depth ledger. It also separates access state from
claim-evidence status and proves that older HOLD files remain historical.
"""
import sys

import validate_product_handoff as core

ORIGINAL_READ_SOURCES = core.read_sources


def read_sources_with_explicit_upgrades():
    identity_lanes, inspection_lanes = ORIGINAL_READ_SOURCES()
    upgrade_files = [core.DATA / "source-upgrade-wave3e.json"]
    for path in upgrade_files:
        core.fail(not path.exists(), f"missing explicit source-upgrade authority {path.name}")
        obj = core.load(path)
        rows = obj.get("sources")
        core.fail(not isinstance(rows, list), f"{path.name}: sources is not a list")
        for row in rows:
            sid = core.source_id(row)
            core.fail(not sid, f"{path.name}: source without id")
            lane = {
                "path": str(path.relative_to(core.ROOT)),
                "layer": core.layer_of(path),
                "record": row,
            }
            # Deliberately inspection-only. SOURCE_IDENTITY_PACKAGE != CLAIM_INSPECTION_LEDGER.
            inspection_lanes[sid].append(lane)
    return identity_lanes, inspection_lanes


def inspection_for_exact_status(rec, identity_lanes, inspection_lanes):
    rows = []
    for sid in rec.get("source_minimum") or []:
        owner, why = core.choose_owner(rec, sid, identity_lanes, inspection_lanes)
        source = owner["record"]
        rows.append({
            "source_id": sid,
            "evidence_status": source.get("evidence_status") or source.get("evidenceStatus") or "NOT_EXPLICITLY_LABELED",
            "access_state": core.norm_access(source),
            "inspection_scope": core.norm_scope(source),
            "owning_lane": owner["path"],
            "claim_limit": core.norm_limit(source),
            "owner_resolution": why,
        })
    core.fail(not rows, f"{core.cid(rec)}: no source_minimum")
    return rows


def exact_claim_ready_with_access(rows):
    bad_scope = ("catalog", "metadata", "abstract", "page_inspected", "unspecified", "link_only")
    for row in rows:
        scope = row["inspection_scope"].lower()
        access = row.get("access_state", "UNSPECIFIED").lower()
        if any(marker in scope for marker in bad_scope):
            return False
        if "catalog" in access or "link" in access or "unspecified" in access:
            return False
        if not any(marker in scope for marker in ("exact_", "full_", "relevant_", "partial_text_inspected", "author_uploaded_published_text")):
            return False
    return True


def source_identity_package_bibliographic_only(identity_lanes, inspection_lanes):
    rows = []
    for sid in sorted(inspection_lanes):
        lane = identity_lanes.get(sid, [inspection_lanes[sid][0]])[0]
        source = lane["record"]
        title = source.get("title")
        rows.append({
            "source_id": sid,
            "title": title,
            "author": source.get("author") or core.author_from_title(title),
            "year": source.get("year") or core.year_from_title(title),
            "type": core.norm_role(source),
            "stable_locator": source.get("url"),
            "identity_verification_status": "BIBLIOGRAPHIC_IDENTITY_RECORDED_FROM_RESEARCH_AUTHORITY",
        })
    return rows


def validate_hold_history():
    old = core.load(core.DATA / "remaining-holds-wave3l.json")
    current = core.load(core.DATA / "remaining-holds-wave3n.json")
    p0 = core.load(core.DATA / "p0-claim-holds-wave3.json")

    old_ids = {row.get("candidate_id") for row in old.get("remaining_holds", [])}
    closed_ids = {row.get("candidate_id") for row in current.get("closed_in_wave3n", [])}
    current_ids = {row.get("candidate_id") for row in current.get("remaining_holds", [])}

    core.fail(None in old_ids or None in closed_ids, "historical/current HOLD record missing candidate_id")
    core.fail(old_ids != closed_ids,
              f"Wave3l historical HOLDs do not match Wave3n closure set: old={sorted(old_ids)} closed={sorted(closed_ids)}")
    core.fail(bool(current_ids), f"Wave3n still has current HOLD IDs: {sorted(current_ids)}")
    core.fail((current.get("candidate_corpus_after_overrides") or {}).get("hold") != 0,
              "Wave3n declares nonzero current HOLD count")
    core.fail(not isinstance(p0.get("targets"), list) or not p0.get("methodRules"),
              "P0 HOLD history malformed")
    # P0 and Wave3l are historical evidence only. They must never be unioned into current HOLDs.


if __name__ == "__main__":
    try:
        validate_hold_history()
        core.read_sources = read_sources_with_explicit_upgrades
        core.inspection_for = inspection_for_exact_status
        core.exact_claim_ready = exact_claim_ready_with_access
        core.source_identity_package = source_identity_package_bibliographic_only
        core.main()
    except core.AuditError as exc:
        print(f"HANDOFF_AUDIT_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
