#!/usr/bin/env python3
"""Fail-closed CI entrypoint for the Chapter 4–5 handoff audit.

The core validator intentionally scans ledgers/quorums. PR #183 also has one explicit
Wave3e source-upgrade authority; this wrapper adds that file as an inspection lane
without pretending it is a global identity/depth ledger. It also proves that the
Wave3l HOLD list is historical by matching those four IDs to Wave3n closures.
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
        core.main()
    except core.AuditError as exc:
        print(f"HANDOFF_AUDIT_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
