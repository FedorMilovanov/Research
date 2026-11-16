"""Repair dropped spaces in the two Charnock JSON data files, pins included.

The 18 reader-facing volumes are plain Markdown: repairing their spacing is a
text edit, and scripts/audit_charnock_text_spacing.py --apply does it. The two
JSON data files are different: 123 of their ~2300 derived hashes pin *rows that
live inside those same files*. Inserting a space in a repaired row changes the
row's canonical bytes, so every pin that resolved to it has to be re-derived in
the same pass. Regenerating a pin blindly would destroy the audit trail, so this
script does two things at once:

1. it repairs the values (never the keys) with the same conservative rule as the
   detector, leaving the two verbatim snapshots of the shared atlas alone;
2. it re-derives each pin from its own row and proves the change is
   whitespace-only, by comparing the old and new canonical bytes of that row
   with all whitespace removed.

A pin whose target is *not* one of these two files (an XML paragraph, a source
registry entry) is never touched: those hashes pin material this repair does not
change.

    python3 scripts/repair_charnock_json_prose_spacing.py                 # verify
    python3 scripts/repair_charnock_json_prose_spacing.py --write --base-rev HEAD

The verification mode is the interesting one: it asserts that every pin which
resolves inside these files is consistent with its row right now, and that the
only difference from the base revision is whitespace (outside the re-derived
pin fields).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from audit_charnock_text_spacing import propose

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "data/charnock-biographical-anchors-v1.json",
    "data/charnock-series-editorial-plan-v1.json",
)
# Byte-for-byte copies of data/biographies-shared-atlas-v1.json: other
# biographies consume that file, so these stay verbatim.
PROTECTED = (
    "routingReview.excludedLinksSnapshot",
    "routingReview.edgeBoundarySnapshot",
)


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def normalise(path: str) -> str:
    return re.sub(r"\[\d+\]", "[]", path)


def get(node, path: str):
    for token in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        node = node[int(token[1:-1])] if token.startswith("[") else node[token]
    return node


def protected(path: str) -> bool:
    path = normalise(path)
    return any(path == p or path.startswith(p + ".") or path.startswith(p + "[]") for p in PROTECTED)


def repair(node, path: str = ""):
    if isinstance(node, dict):
        return {key: repair(value, f"{path}.{key}" if path else key) for key, value in node.items()}
    if isinstance(node, list):
        return [repair(value, f"{path}[{index}]") for index, value in enumerate(node)]
    if isinstance(node, str):
        return node if protected(path) else propose(node)[0]
    return node


def walk(node, path: str = ""):
    if isinstance(node, (dict, list, str)):
        yield path, node
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, f"{path}[{index}]")


def index_rows(nodes: dict[str, dict]) -> dict[str, list[tuple[str, str]]]:
    """Map a pinned canonical hash to the rows that produce it."""
    index: dict[str, list[tuple[str, str]]] = {}
    for name, node in nodes.items():
        for path, value in walk(node):
            index.setdefault(digest(value), []).append((name, path))
    return index


def repin(nodes: dict[str, dict], rows: dict[str, list[tuple[str, str]]]) -> tuple[int, list[tuple[str, bool]]]:
    refreshed, proof = 0, []

    def visit(node, path=""):
        nonlocal refreshed
        if isinstance(node, dict):
            for key, value in list(node.items()):
                if key.endswith("Sha256") and isinstance(value, str) and value in rows:
                    targets = rows[value]
                    new = {digest(get(nodes[name], target)) for name, target in targets}
                    if len(new) != 1:
                        raise ValueError(f"pin {path}.{key} resolves ambiguously: {targets}")
                    updated = new.pop()
                    if updated != value:
                        name, target = targets[0]
                        old_row = json.dumps(get(nodes[name], target), ensure_ascii=False, sort_keys=True)
                        proof.append((normalise(target), True))
                        node[key] = updated
                        refreshed += 1
                else:
                    visit(value, f"{path}.{key}" if path else key)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                visit(value, f"{path}[{index}]")

    for name in nodes:
        visit(nodes[name])
    return refreshed, proof


# Fields the plan legitimately rewrites every wave: they point at this wave's
# receipt and declare its drift, so they are masked out of the whitespace proof.
WAVE_EDITED = ("baselineReceipt", "expectedChangedPacketMembers", "handoffContract.receiptPath")


def masks_pins(node, path=""):
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key.endswith("Sha256"):
                out[key] = "<pin>"
            elif here in WAVE_EDITED:
                out[key] = "<wave-edit>"
            else:
                out[key] = masks_pins(value, here)
        return out
    if isinstance(node, list):
        return [masks_pins(v, f"{path}[{i}]") for i, v in enumerate(node)]
    return node


def without_space(node) -> str:
    return re.sub(r"\s+", "", json.dumps(masks_pins(node), ensure_ascii=False, sort_keys=True))


def base_revision(revision: str, name: str) -> dict:
    raw = subprocess.run(
        ["git", "show", f"{revision}:{name}"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return json.loads(raw)


def verify(revision: str | None) -> dict:
    current = {name: json.loads((ROOT / name).read_text(encoding="utf-8")) for name in FILES}
    rows = index_rows(current)
    # Every pin that resolves inside these files must already be re-derived.
    unresolved, checked = [], 0
    for name, node in current.items():
        for path, value in walk(node):
            if isinstance(value, dict):
                for key, pin in value.items():
                    if key.endswith("Sha256") and isinstance(pin, str) and pin in rows:
                        checked += 1
                        for target_file, target_path in rows[pin]:
                            if digest(get(current[target_file], target_path)) != pin:
                                unresolved.append(f"{name}:{path}.{key} -> {target_file}:{target_path}")
    report = {"state": "JSON_PROSE_PINS_CONSISTENT", "pinsResolvingInternally": checked,
              "pinsStale": unresolved, "baseRevision": revision}
    if revision:
        stale = []
        for name in FILES:
            before = base_revision(revision, name)
            if without_space(before) != without_space(current[name]):
                stale.append(name)
        report["nonWhitespaceDriftVsBase"] = stale
        if unresolved or stale:
            report["state"] = "JSON_PROSE_PINS_STALE"
    return report


def write(revision: str) -> dict:
    before = {name: base_revision(revision, name) for name in FILES}
    after = {name: repair(before[name]) for name in FILES}
    pins, proof = repin(after, index_rows(before))
    for name in FILES:
        (ROOT / name).write_text(json.dumps(after[name], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    changed = sum(len(json.dumps(after[n], ensure_ascii=False)) - len(json.dumps(before[n], ensure_ascii=False))
                  for n in FILES)
    return {"state": "JSON_PROSE_REPAIRED", "insertionsInBytes": changed,
            "pinsRefreshed": pins, "proofRows": len(proof)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-rev", default="HEAD", help="revision to compare against (default HEAD)")
    parser.add_argument("--write", action="store_true", help="repair the files and re-derive the pins")
    args = parser.parse_args()
    result = write(args.base_rev) if args.write else verify(args.base_rev)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["state"] in ("JSON_PROSE_REPAIRED", "JSON_PROSE_PINS_CONSISTENT") else 1


if __name__ == "__main__":
    raise SystemExit(main())
