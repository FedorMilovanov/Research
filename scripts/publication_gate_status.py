#!/usr/bin/env python3
"""Compose the publication gate queue and check that it has not silently moved.

``data/public-projection-queue-2026-08-01.json`` is a **base** queue: its own
composition rule says consumers must load it by record id, replace every record
named by an overlay's ``supersedes_queue_record_id`` with the overlay's
``effective_record``, and only then recompute counts. Reading the base file
alone is reading history.

This script does exactly that composition, adds what can be *checked* rather
than asserted -- whether each record's ``sourceAuthorities`` path exists in this
checkout, and whether each ``rightsLedgerIds`` identifier occurs anywhere in the
repository -- and fails when the composed queue differs from the committed
snapshot. It never promotes a record, never lifts a hold and never invents a
missing decision: ``nextAction`` is carried through verbatim from the queue.

Usage::

    python3 scripts/publication_gate_status.py --summary
    python3 scripts/publication_gate_status.py -o data/publication-gate-queue-v1.json
    python3 scripts/publication_gate_status.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data" / "public-projection-current-2026-08-02.json"
RIGHTS_LEDGER = ROOT / "data" / "physical-rights-ledger-2026-08-01.json"
SNAPSHOT = ROOT / "data" / "publication-gate-queue-v1.json"
SCHEMA_VERSION = 1
AUTHORITY_ID = "RESEARCH-PUBLICATION-GATE-QUEUE-V1"

SCAN_SUFFIXES = {".md", ".json", ".txt", ".yaml", ".yml"}
SKIP_DIRS = {".git", "node_modules", ".arena", ".cache", ".local", "__pycache__",
             ".pytest_cache", ".ruff_cache", ".venv", "venv", ".mypy_cache", "google_drive"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_composed(root: Path = ROOT) -> dict:
    """Base queue + overlays, composed by record id as the rule requires."""
    current = read_json(root / "data" / "public-projection-current-2026-08-02.json")
    base = read_json(root / current["baseQueue"])
    records = {rec["id"]: dict(rec) for rec in base["records"]}

    application = []
    for overlay_rel in current.get("overlays", []):
        overlay = read_json(root / overlay_rel)
        target = overlay.get("supersedes_queue_record_id")
        effective = overlay.get("effective_record")
        if not target or not effective:
            raise ValueError(f"overlay without supersession payload: {overlay_rel}")
        before = records.get(target)
        if before is None:
            raise ValueError(f"overlay names an unknown record: {target}")
        merged = dict(effective)
        merged["_supersededBy"] = overlay.get("authority_id")
        merged["_previousDisposition"] = before.get("disposition")
        merged["_previousHolds"] = before.get("holds", [])
        records[target] = merged
        application.append({
            "overlay": overlay_rel,
            "authorityId": overlay.get("authority_id"),
            "record": target,
            "previousDisposition": before.get("disposition"),
            "effectiveDisposition": effective.get("disposition"),
        })

    counts = {}
    for rec in records.values():
        counts[rec.get("disposition", "UNKNOWN")] = counts.get(rec.get("disposition", "UNKNOWN"), 0) + 1
    return {
        "currentAuthority": current["authorityId"],
        "baseQueue": current["baseQueue"],
        "baseAuthority": base.get("authorityId"),
        "compositionRule": current.get("compositionRule"),
        "policy": current.get("policy", {}),
        "declaredCounts": current.get("effectiveCounts"),
        "composedCounts": dict(sorted(counts.items())),
        "overlaysApplied": application,
        "records": [records[rid] for rid in sorted(records)],
    }


def iter_text(root: Path, exclude: set[str] | None = None):
    exclude = exclude or set()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.as_posix() in exclude:
            continue
        yield path


def identifier_index(root: Path, exclude: set[str] | None = None) -> str:
    """Blunt but honest: one concatenated corpus for substring lookups.

    A rights-ledger id is a pointer, not a proof. Finding it says the identifier
    is recorded somewhere in this checkout; it says nothing about the rights.
    """
    chunks = []
    for path in iter_text(root, exclude):
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(chunks)


def rights_ledger_index(root: Path) -> dict[str, dict]:
    """Rights-ledger entries by corpus id, with the fields a decision needs.

    The ledger's own rule is blunt: "Drive presence proves custody only." So the
    index carries ``rightsState`` and ``publicationEligible`` verbatim and adds
    only what is countable -- how many Drive objects the entry names.
    """
    path = root / "data" / "physical-rights-ledger-2026-08-01.json"
    if not path.is_file():
        return {}
    ledger = read_json(path)
    out: dict[str, dict] = {}
    for rec in ledger.get("records", []):
        corpus = rec.get("corpusId")
        if not corpus:
            continue
        out[corpus] = {
            "rightsLedgerId": rec.get("id"),
            "rightsState": rec.get("rightsState"),
            "publicationEligible": rec.get("publicationEligible"),
            "driveObjects": len(rec.get("driveObjects") or []),
            "driveCheckedAt": ledger.get("driveCheckedAt"),
            "rule": ledger.get("rule"),
        }
    return out


def augment(composed: dict, root: Path = ROOT) -> dict:
    # The queue files name the ids they carry, so scanning them would "find" any
    # id the queue mentions. A rights id must be recorded somewhere *other* than
    # the queue that lists it.
    exclude = {composed["baseQueue"], "data/public-projection-current-2026-08-02.json"}
    index = identifier_index(root, exclude)
    ledger = rights_ledger_index(root)
    records = []
    for rec in composed["records"]:
        authorities = []
        for rel in rec.get("sourceAuthorities", []):
            authorities.append({
                "path": rel,
                "exists": (root / rel).exists(),
            })
        rights_ids = []
        for ident in rec.get("rightsLedgerIds", []) or []:
            rights_ids.append({
                "id": ident,
                "recordedInRepository": ident in index,
            })
        records.append({
            "id": rec["id"],
            "corpus": rec.get("corpus"),
            "disposition": rec.get("disposition"),
            "effectiveHolds": rec.get("holds", []),
            "researchStatus": rec.get("researchStatus"),
            "targetRouteState": rec.get("targetRouteState"),
            "alreadyPublic": rec.get("alreadyPublic"),
            "nextAction": rec.get("nextAction"),
            "forbiddenPromotion": rec.get("forbiddenPromotion"),
            "sourceAuthorities": authorities,
            "rightsLedgerIds": rights_ids,
            "rightsLedger": ledger.get(rec["id"]),
            "supersededBy": rec.get("_supersededBy"),
            "previousDisposition": rec.get("_previousDisposition"),
            "previousHolds": rec.get("_previousHolds"),
        })
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "snapshotDate": "2026-11-18",
        "currentAuthority": composed["currentAuthority"],
        "baseQueue": composed["baseQueue"],
        "compositionRule": composed["compositionRule"],
        "policy": composed["policy"],
        "declaredCounts": composed["declaredCounts"],
        "composedCounts": composed["composedCounts"],
        "overlaysApplied": composed["overlaysApplied"],
        "records": records,
        "checks": {
            "recordsWithMissingAuthorityFile": sum(
                1 for r in records for a in r["sourceAuthorities"] if not a["exists"]),
            "rightsIdsNotRecorded": sum(
                1 for r in records for i in r["rightsLedgerIds"] if not i["recordedInRepository"]),
            "recordsWithoutRightsLedgerEntry": sum(1 for r in records if not r["rightsLedger"]),
            "rightsLedgerEntriesPublicationEligible": sum(
                1 for r in records
                if r["rightsLedger"] and r["rightsLedger"].get("publicationEligible") is True),
        },
        "note": ("Снимок собран по правилу композиции из current-authority: база + оверлеи, "
                 "пересчёт счётчиков. Наличие файла authority и упоминание rights-id в репозитории — "
                 "проверяемые факты; они не являются ни правами, ни разрешением на публикацию."),
    }


def summary(snapshot: dict) -> str:
    lines = [
        f"Publication gate: {len(snapshot['records'])} records, PROMOTE {snapshot['composedCounts'].get('PROMOTE', 0)}",
        "composed: " + ", ".join(f"{k}={v}" for k, v in snapshot["composedCounts"].items()),
        "declared: " + ", ".join(f"{k}={v}" for k, v in (snapshot["declaredCounts"] or {}).items()),
        f"missing authority files: {snapshot['checks']['recordsWithMissingAuthorityFile']}, "
        f"rights ids not recorded: {snapshot['checks']['rightsIdsNotRecorded']}",
    ]
    for rec in snapshot["records"]:
        holds = ", ".join(rec["effectiveHolds"]) or "-"
        rights = (rec.get("rightsLedger") or {}).get("rightsState", "no rights entry")
        lines.append(f"  {rec['disposition']:9s} {rec['id']:34s} holds: {holds:52s} rights: {rights}")
    return "\n".join(lines)


def check(snapshot: dict, committed: dict) -> list[str]:
    problems = []
    if snapshot["composedCounts"] != committed.get("composedCounts"):
        problems.append(f"composed counts drifted: {committed.get('composedCounts')} -> {snapshot['composedCounts']}")
    if snapshot["declaredCounts"] != committed.get("declaredCounts"):
        problems.append("declared effectiveCounts drifted from the current authority")
    old = {r["id"]: r for r in committed.get("records", [])}
    new = {r["id"]: r for r in snapshot["records"]}
    for rid in sorted(set(new) - set(old)):
        problems.append(f"record appeared without notice: {rid}")
    for rid in sorted(set(old) - set(new)):
        problems.append(f"record vanished: {rid}")
    for rid in sorted(set(old) & set(new)):
        a, b = old[rid], new[rid]
        for field in ("disposition", "effectiveHolds", "nextAction"):
            if a.get(field) != b.get(field):
                problems.append(f"{rid}: {field} changed ({a.get(field)!r} -> {b.get(field)!r})")
        if a.get("supersededBy") != b.get("supersededBy"):
            problems.append(f"{rid}: overlay supersession changed")
    for rid, rec in new.items():
        if rec["disposition"] == "PROMOTE" and rec["effectiveHolds"]:
            problems.append(f"{rid}: PROMOTE declared with holds {rec['effectiveHolds']} (policy forbids)")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compose and check the publication gate queue (read-only)")
    parser.add_argument("-o", "--output", help="write the composed snapshot as JSON")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--check", action="store_true", help="compare with the committed snapshot")
    parser.add_argument("--snapshot", default=str(SNAPSHOT))
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    try:
        snapshot = augment(load_composed(root), root)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"publication gate: cannot compose queue: {exc}", file=sys.stderr)
        return 2

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}")

    if args.check:
        path = Path(args.snapshot)
        if not path.is_file():
            print(f"publication gate: no committed snapshot at {path}", file=sys.stderr)
            return 2
        problems = check(snapshot, json.loads(path.read_text(encoding="utf-8")))
        if problems:
            for problem in problems:
                print(f"publication gate: {problem}", file=sys.stderr)
            return 1
        print("publication gate: PASS — composed queue matches the committed snapshot, "
              f"PROMOTE {snapshot['composedCounts'].get('PROMOTE', 0)}")

    if args.summary or (not args.output and not args.check):
        print(summary(snapshot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
