# Research control-plane authority — 2026-08-02

**Authority ID:** `RESEARCH-CONTROL-PLANE-2026-08-02`  
**Status:** `CURRENT / FAIL-CLOSED`  
**Scope:** repository governance, evidence semantics, validator behavior, transitive dependencies, byte pins, public projection, custody and branch state.

This file does not replace corpus-specific research conclusions. It governs how those conclusions are selected, validated and transferred.

## Current contracts

1. [`data/repository-evidence-policy-v2.json`](data/repository-evidence-policy-v2.json) — single global evidence and HOLD vocabulary.
2. [`data/artifact-custody-policy-v2.json`](data/artifact-custody-policy-v2.json) — temporary artifact versus durable acquisition boundary.
3. [`data/public-projection-current-2026-08-02.json`](data/public-projection-current-2026-08-02.json) — canonical composed public projection.
4. [`scripts/validate_repository_authority_integrity.py`](scripts/validate_repository_authority_integrity.py) — repository-wide fail-closed validator.
5. [`.github/workflows/repository-authority-integrity.yml`](.github/workflows/repository-authority-integrity.yml) — full deterministic gate on every PR and `main` push.
6. [`archive-ledgers/README.md`](archive-ledgers/README.md) — permanent forensic archive and neutralized-ref record.

## Snapshot semantics

A corpus authority may intentionally pin an older Research commit as the exact evidence snapshot it examined. Such a pin does **not** claim that the pinned commit is the current repository HEAD.

Fields must therefore be read as:

- `researchSnapshot`, `authorityBaseCommit`, `productSnapshot` — evidence/input snapshots;
- current Git `main` HEAD — control-plane implementation state;
- `authorityId` plus `status=CURRENT` — semantic selection state.

A validator must never compare these fields as though they represented the same concept.

## Enforced corrections

- Legacy `A/B/C/HOLD` and conflicting local `A1–X` semantics are superseded or namespaced.
- OSK Waves 9–10 validate transitive parent registries.
- Wave 7 and Gill verify Product commits in `gb-is-my-strength`, not by literal strings in Research.
- Bratsky stages verify `commit:path`, Git blob and current bytes.
- Genesis active documents verify current bytes against `authorityBaseCommit`.
- Heart trust classes are validator-owned and quote-safe claims require explicit locator/version/context contracts.
- Public projection is `base + required overlay`; the base queue alone is historical.
- Total/source audits execute committed code, are read-only and use real baseline gates.
- Source Library artifacts declare `EPHEMERAL_ACTION_ARTIFACT` until a durable readback receipt exists.
- Baptist proof ledger has a deterministic V2 canonical view; legacy CSV remains append-only input.
- Obsolete working refs were neutralized to exact `main`; only the forensic archive intentionally diverges.

## Publication boundary

No Research closure, green structural validator, downloaded artifact or Drive object independently authorizes publication. Publication requires the corpus authority, exact target snapshot/route, evidence and locator closure, item-level rights/credit decisions, and an explicit Product release witness.
