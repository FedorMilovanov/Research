#!/usr/bin/env python3
"""Check the non-canonical ``holds`` vocabulary against the mapping proposal.

``data/repository-holds-inventory-v1.json`` counts what the machine registries
actually say. 39 spellings inside ``holds`` arrays are not canonical flags of
``data/repository-evidence-policy-v2.json``: some are axis values of that same
policy, some are statuses, some glue two facts into one string, and three
cannot be resolved without reading the record.

``data/hold-value-mapping-proposal-v1.json`` proposes a home for each spelling.
It is a **proposal**, not a rewrite: no registry value is changed here or
anywhere else. This script is the guard rail around it:

* coverage - every non-canonical spelling in the inventory is mapped, and no
  mapping is stale;
* counts - proposed counts equal measured counts;
* vocabulary - every axis proposal names an existing axis and an existing value
  of that axis in policy v2;
* class - every entry is one of ``canonical`` | ``axis`` | ``split`` |
  ``status`` | ``manual``;
* rendering - ``--render`` prints the table used in the register, so the human
  document cannot drift from the machine file.

Usage::

    python3 scripts/check_hold_vocabulary.py --check
    python3 scripts/check_hold_vocabulary.py --render
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "repository-holds-inventory-v1.json"
POLICY = ROOT / "data" / "repository-evidence-policy-v2.json"
PROPOSAL = ROOT / "data" / "hold-value-mapping-proposal-v1.json"

CLASSES = ("canonical", "axis", "split", "status", "manual")
AXES = ("accessStates", "locatorStates", "rightsStates", "publicationStates")


class VocabularyError(Exception):
    pass


def canonical_flags(policy: dict) -> set[str]:
    return set(policy.get("holds", []))


def axis_values(policy: dict) -> dict[str, str]:
    """axisName -> singular key ("accessState"), plus name -> allowed values."""
    out: dict[str, str] = {}
    for axis in AXES:
        if axis in policy:
            out[axis] = axis[:-1] if axis.endswith("s") else axis
    return out


def measured_spellings(inventory: dict, canonical: set[str]) -> dict[str, dict]:
    acc: dict[str, dict] = {}
    for item in inventory.get("jsonHolds", []):
        for value in item.get("values", []):
            if value in canonical:
                continue
            slot = acc.setdefault(value, {"count": 0, "files": set()})
            slot["count"] += 1
            slot["files"].add(item.get("path", ""))
    return acc


def check(inventory: dict, policy: dict, proposal: dict) -> list[str]:
    problems: list[str] = []
    canonical = canonical_flags(policy)
    if not canonical:
        problems.append("policy has no canonical holds list")
    measured = measured_spellings(inventory, canonical)

    proposed = proposal.get("values", [])
    proposed_by_value = {v["value"]: v for v in proposed}
    if len(proposed_by_value) != len(proposed):
        problems.append("duplicate spellings in proposal")

    for spelling in sorted(set(measured) - set(proposed_by_value)):
        problems.append(f"unmapped spelling in inventory: {spelling!r} ({measured[spelling]['count']} values)")
    for spelling in sorted(set(proposed_by_value) - set(measured)):
        problems.append(f"stale mapping (spelling no longer in inventory): {spelling!r}")

    axis_singular = axis_values(policy)
    for entry in proposed:
        spelling = entry.get("value")
        cls = entry.get("class")
        if cls not in CLASSES:
            problems.append(f"{spelling!r}: unknown class {cls!r}")
            continue
        if not str(entry.get("justification", "")).strip():
            problems.append(f"{spelling!r}: missing justification")
        if spelling in measured and entry.get("count") != measured[spelling]["count"]:
            problems.append(f"{spelling!r}: count {entry.get('count')} != measured {measured[spelling]['count']}")
        if spelling in measured and sorted(entry.get("files", [])) != sorted(measured[spelling]["files"]):
            problems.append(f"{spelling!r}: file list drifted from inventory")
        target = str(entry.get("proposedRepresentation", ""))
        for axis, singular in axis_singular.items():
            for token in re.findall(rf"{singular}=([A-Z_]+)", target):
                if token not in policy.get(axis, []):
                    problems.append(f"{spelling!r}: {singular}={token} is not a value of {axis}")
        if cls == "canonical":
            named = re.findall(r"\b[A-Z]+_HOLD\b", target)
            if not named:
                problems.append(f"{spelling!r}: canonical class without a canonical flag")
            for flag in named:
                if flag not in canonical:
                    problems.append(f"{spelling!r}: {flag} is not a canonical flag")

    if proposal.get("status") != "PROPOSAL_ONLY":
        problems.append("proposal must stay PROPOSAL_ONLY: nothing here rewrites registries")
    if proposal.get("counts", {}).get("spellings") != len(measured):
        problems.append("counts.spellings does not match the inventory")
    return problems


def render(proposal: dict) -> str:
    lines = [
        "| Написание в `holds` | Значений | Класс | Предлагаемое место |",
        "|---|---:|---|---|",
    ]
    for entry in sorted(proposal.get("values", []), key=lambda v: (-v["count"], v["value"])):
        lines.append(
            f"| `{entry['value']}` | {entry['count']} | {entry['class']} | {entry['proposedRepresentation']} |"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check / render the non-canonical holds mapping proposal")
    parser.add_argument("--check", action="store_true", help="validate coverage, counts and vocabulary")
    parser.add_argument("--render", action="store_true", help="print the Markdown table")
    parser.add_argument("--inventory", default=str(INVENTORY))
    parser.add_argument("--policy", default=str(POLICY))
    parser.add_argument("--proposal", default=str(PROPOSAL))
    args = parser.parse_args(argv)

    try:
        inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
        policy = json.loads(Path(args.policy).read_text(encoding="utf-8"))
        proposal = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"hold vocabulary: cannot read inputs: {exc}", file=sys.stderr)
        return 2

    if args.render:
        print(render(proposal))
    problems = check(inventory, policy, proposal)
    if problems:
        for problem in problems:
            print(f"hold vocabulary: {problem}", file=sys.stderr)
        return 1
    if args.check or not args.render:
        canonical = canonical_flags(policy)
        measured = measured_spellings(inventory, canonical)
        total = sum(v["count"] for v in measured.values())
        print(f"hold vocabulary: PASS — {len(measured)} non-canonical spellings / {total} values, "
              f"all mapped; proposal stays PROPOSAL_ONLY (no registry rewritten)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
