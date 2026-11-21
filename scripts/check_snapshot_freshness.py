#!/usr/bin/env python3
"""Check dated research snapshots against the branch tree they were built from.

The workflow checks pull requests in two trees with two different purposes:

* the synthetic merge tree is for integration checks;
* the pull-request head is for dated snapshots committed by that branch.

Checking a snapshot in the synthetic merge tree made every unrelated ``main`` change look
like a defect in the pull request.  This checker is therefore run in a detached worktree at
the PR head.  It is offline: the pinned GitHub report is checked for citation-site drift,
not downloaded again, and the Drive report is rebuilt from its dated committed snapshot.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import audit_document_twins as twins
import audit_drive_ledger as drive
import audit_relative_links as links
import audit_repository_holds as holds
import audit_state_stamps as stamps
import verify_pinned_github_locators as pinned

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SnapshotSpec:
    label: str
    relative_path: str
    build: Callable[[Path, dict], dict]


def _inventory(root: Path, _committed: dict) -> dict:
    return holds.scan(root)


def _links(root: Path, _committed: dict) -> dict:
    exceptions = links.load_exceptions(root / "data" / "relative-link-exceptions-v1.json")
    return links.scan(root, exceptions)


def _twins(root: Path, _committed: dict) -> dict:
    return twins.audit(root)


def _stamps(root: Path, committed: dict) -> dict:
    recorded = committed["scope"]["today"]
    return stamps.audit(root, today=dt.date.fromisoformat(recorded))


def _drive(root: Path, _committed: dict) -> dict:
    snapshot = json.loads((root / "data" / "drive-ledger-snapshot-2026-11-18.json").read_text(encoding="utf-8"))
    return drive.audit(root, snapshot)


SNAPSHOTS = (
    SnapshotSpec("holds inventory", "data/repository-holds-inventory-v1.json", _inventory),
    SnapshotSpec("relative links", "data/relative-links-audit-2026-11-18.json", _links),
    SnapshotSpec("document twins", "data/document-twins-2026-11-18.json", _twins),
    SnapshotSpec("state stamps", "data/state-stamps-2026-11-18.json", _stamps),
    SnapshotSpec("Drive ledger", "data/drive-ledger-audit-2026-11-18.json", _drive),
)


def first_difference(expected: object, actual: object, path: str = "$") -> str | None:
    """Return one stable JSON path explaining a mismatch."""
    if type(expected) is not type(actual):
        return f"{path}: {type(expected).__name__} != {type(actual).__name__}"
    if isinstance(expected, dict):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if missing:
            return f"{path}: missing key {missing[0]!r}"
        if extra:
            return f"{path}: extra key {extra[0]!r}"
        for key in expected:
            problem = first_difference(expected[key], actual[key], f"{path}.{key}")
            if problem:
                return problem
        return None
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return f"{path}: list length {len(expected)} != {len(actual)}"
        for index, (left, right) in enumerate(zip(expected, actual)):
            problem = first_difference(left, right, f"{path}[{index}]")
            if problem:
                return problem
        return None
    if expected != actual:
        return f"{path}: {expected!r} != {actual!r}"
    return None


def check(root: Path = ROOT, specs: tuple[SnapshotSpec, ...] = SNAPSHOTS) -> list[str]:
    problems: list[str] = []
    for spec in specs:
        path = root / spec.relative_path
        if not path.is_file():
            problems.append(f"{spec.label}: missing {spec.relative_path}")
            continue
        try:
            committed = json.loads(path.read_text(encoding="utf-8"))
            fresh = spec.build(root, committed)
            difference = first_difference(committed, fresh)
        except (KeyError, TypeError, ValueError, OSError) as exc:
            problems.append(f"{spec.label}: cannot reproduce: {exc}")
            continue
        if difference:
            problems.append(f"{spec.label}: stale ({difference})")

    pinned_path = root / "data" / "pinned-github-locators-verified-2026-11-18.json"
    try:
        committed_pinned = json.loads(pinned_path.read_text(encoding="utf-8"))
        for problem in pinned.structure_drift(committed_pinned, pinned.collect(root)):
            problems.append(f"pinned GitHub locators: {problem}")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        problems.append(f"pinned GitHub locators: cannot check: {exc}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--check", action="store_true", help="return 1 when a snapshot is stale")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args(argv)

    problems = check(Path(args.root).resolve())
    if problems:
        print("Snapshot freshness: FAIL", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
    else:
        print(f"Snapshot freshness: OK ({len(SNAPSHOTS) + 1} reports)")
    return 1 if args.check and problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
