#!/usr/bin/env python3
"""Read-only inventory of HOLD markers across the repository.

HOLD is not an evidence class (see ``data/repository-evidence-policy-v2.json``).
Canonical flags are ``EVIDENCE_HOLD``, ``LOCATOR_HOLD``, ``ARCHIVE_HOLD``,
``RIGHTS_HOLD`` and ``PUBLICATION_HOLD``; corpora also use historical and
domain-specific markers (``VERSION-HOLD``, ``BLOCKING-HOLD``,
``PAGE-IMAGE-HOLD`` ...). This script only counts and classifies what the
checked-out bytes say. It never clears a HOLD, never writes into the working
tree and never treats its own output as evidence.

A mention is classified from its own line:

* ``closed``   - the line records that the flag was taken down
  ("снят", "CLOSED", "resolved"), unless negated;
* ``open``     - the line records that the flag survives
  ("сохраняется", "остаётся", "открыт", "не снят", "OPEN", "pending");
* ``unmarked`` - the line names the flag without recording either state.

Lines that both record a closure and a surviving flag are counted in both
buckets and reported as ``mixed``: such lines are usually summaries.

Usage::

    python3 scripts/audit_repository_holds.py --summary
    python3 scripts/audit_repository_holds.py -o data/repository-holds-inventory-v1.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCHEMA_VERSION = 1
AUTHORITY_ID = "RESEARCH-HOLDS-INVENTORY-V1"

CANONICAL_FLAGS = (
    "EVIDENCE_HOLD",
    "LOCATOR_HOLD",
    "ARCHIVE_HOLD",
    "RIGHTS_HOLD",
    "PUBLICATION_HOLD",
)

# Historical / corpus-specific markers that are not part of evidence-policy v2.
EXTENDED_FLAGS = (
    "VERSION-HOLD",
    "BLOCKING-HOLD",
    "PAGE-IMAGE-HOLD",
    "BOOK-FULLTEXT-HOLD",
    "LIVE-READBACK-HOLD",
    "HOLD-RETAINED",
    "HOLD_RETAINED",
    "HOLD-SOURCE",
    "HOLD-QUOTE",
    "HOLD-STUB",
    "HOLD-RIGHTS",
    "HOLD-VERSION",
    "HOLD_MAJOR",
    "HOLD_FULLTEXT",
    "HOLD_DETAIL",
    "HOLD-AS",
    "HOLD-GLOSS",
    "HOLD-APPARATUS",
    "HOLD-SEARCHCLOSED",
)

SKIP_DIRS = {
    ".git",
    ".arena",
    ".cache",
    ".local",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".scratch",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "google_drive",
    "node_modules",
    "out",
    "target",
}

# Artifacts that describe the inventory itself. Counting them would make the
# snapshot depend on its own output.
SELF_REFERENTIAL = {
    "data/repository-holds-inventory-v1.json",
    "docs/research/HOLDS_REGISTER_2026-11-18.md",
    # The closure registry and the vocabulary proposal are bookkeeping *about*
    # holds: their `holds` fields name the classes they discuss, not the state
    # of an object. Counting them would let this pass inflate the very numbers
    # it is supposed to measure -- and would make the snapshot depend on how
    # many classes the register happens to list.
    "data/hold-closure-registry-v1.json",
    "data/hold-value-mapping-proposal-v1.json",
}

TEXT_SUFFIXES = {
    ".csv",
    ".json",
    ".jsonl",
    ".js",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}

CLOSED_RE = re.compile(
    r"(?<!не\s)(?<!не)(?:снят(?:а|о|ы)?|закрыт(?:а|о|ы)?|CLOSED|closed|resolved|RESOLVED)",
    re.IGNORECASE,
)
JSON_ARRAY_ITEM_RE = re.compile(r'^\s*"(?:EVIDENCE|LOCATOR|ARCHIVE|RIGHTS|PUBLICATION)_HOLD"\s*,?\s*$')

OPEN_RE = re.compile(
    r"(?:не\s+снят\w*|сохраня\w+|оста[её]тся|остают\w+|открыт\w*|не\s+закрыт\w+|"
    r"не\s+выполнен\w*|OPEN|open|pending|PENDING|unresolved)",
)


def flag_pattern() -> re.Pattern[str]:
    canonical = "|".join(re.escape(flag) for flag in CANONICAL_FLAGS)
    extended = "|".join(re.escape(flag) for flag in sorted(set(EXTENDED_FLAGS), key=len, reverse=True))
    return re.compile(rf"(?<![A-Z0-9_])(?:{canonical})(?![A-Z0-9_])|(?:{extended})")


def classification(line: str) -> set[str]:
    states: set[str] = set()
    if CLOSED_RE.search(line):
        states.add("closed")
    if OPEN_RE.search(line):
        states.add("open")
    if not states:
        states.add("unmarked")
    if len(states) > 1:
        states.add("mixed")
    return states


def corpus_of(rel: str) -> str:
    parts = Path(rel).parts
    return parts[0] if len(parts) > 1 else "_root"


def iter_text_files(root: Path) -> list[Path]:
    found: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.relative_to(root).as_posix() in SELF_REFERENTIAL:
            continue
        found.append(path)
    return sorted(found, key=lambda p: p.relative_to(root).as_posix())


def json_holds(path: Path) -> list[tuple[str, list[str]]]:
    """Return ``(pointer, values)`` for every ``holds`` array in a JSON file."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return []

    results: list[tuple[str, list[str]]] = []

    def walk(node: object, pointer: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                child = f"{pointer}/{key}"
                if key == "holds" and isinstance(value, list):
                    values = [str(item) for item in value]
                    results.append((child, values))
                else:
                    walk(value, child)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{pointer}/{index}")

    walk(payload, "")
    return results


def scan(root: Path) -> dict:
    pattern = flag_pattern()
    flag_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    per_corpus: dict[str, dict] = {}
    per_file: list[dict] = []
    json_files: list[dict] = []
    both_states = 0
    scanned = 0

    for path in iter_text_files(root):
        scanned += 1
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        file_flags: Counter[str] = Counter()
        file_status: Counter[str] = Counter()
        is_json = path.suffix.lower() == ".json"
        for line in text.splitlines():
            if is_json and JSON_ARRAY_ITEM_RE.match(line):
                # structured ``holds`` values are counted by ``json_holds``
                continue
            matches = pattern.findall(line)
            if not matches:
                continue
            states = classification(line)
            for flag in matches:
                canonical = flag in CANONICAL_FLAGS
                flag_counts[flag] += 1
                file_flags[flag] += 1
                if canonical:
                    status_counts.update(states - {"mixed"})
                    file_status.update(states - {"mixed"})
                    if "mixed" in states:
                        both_states += 1
        if file_flags:
            corpus = corpus_of(rel)
            bucket = per_corpus.setdefault(
                corpus,
                {"files": 0, "mentions": Counter(), "status": Counter()},
            )
            bucket["files"] += 1
            bucket["mentions"].update(file_flags)
            bucket["status"].update(file_status)
            per_file.append(
                {
                    "path": rel,
                    "corpus": corpus,
                    "mentions": dict(sorted(file_flags.items())),
                    "status": dict(sorted(file_status.items())),
                }
            )

        if path.suffix.lower() == ".json":
            holds = json_holds(path)
            if holds:
                for pointer, values in holds:
                    json_files.append(
                        {
                            "path": rel,
                            "pointer": pointer or "/",
                            "values": values,
                        }
                    )

    json_values: Counter[str] = Counter()
    for entry in json_files:
        json_values.update(entry["values"])

    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "snapshotDate": "2026-11-18",
        "policy": "data/repository-evidence-policy-v2.json",
        "policyNote": (
            "HOLD is not an evidence class. Counts here describe marker text in the "
            "checked-out bytes, not the evidentiary state of any source."
        ),
        "scope": {
            "root": ".",
            "textSuffixes": sorted(TEXT_SUFFIXES),
            "skippedDirectories": sorted(SKIP_DIRS),
            "selfReferentialArtifacts": sorted(SELF_REFERENTIAL),
            "canonicalFlags": list(CANONICAL_FLAGS),
            "extendedFlags": sorted(set(EXTENDED_FLAGS)),
        },
        "totals": {
            "filesScanned": scanned,
            "filesWithMentions": len(per_file),
            "mentions": dict(sorted(flag_counts.items())),
            "mentionsByStatus": dict(sorted(status_counts.items())),
            "canonicalFlagLineStatesRecordedAsBothOpenAndClosed": both_states,
            "filesWithJsonHolds": len({entry["path"] for entry in json_files}),
            "jsonHoldsValues": dict(sorted(json_values.items())),
            # the sum is what the register quotes; keeping it here means the sentence can be
            # checked instead of remembered
            "jsonHoldsTotal": sum(json_values.values()),
        },
        "byCorpus": {
            corpus: {
                "files": bucket["files"],
                "mentions": dict(sorted(bucket["mentions"].items())),
                "status": dict(sorted(bucket["status"].items())),
            }
            for corpus, bucket in sorted(per_corpus.items())
        },
        "jsonHolds": sorted(json_files, key=lambda e: (e["path"], e["pointer"])),
        "files": per_file,
    }


def summary(inventory: dict) -> str:
    totals = inventory["totals"]
    lines = [
        f"HOLD inventory: {totals['filesWithMentions']} files of "
        f"{totals['filesScanned']} carry a HOLD marker",
        "",
        "canonical flags (mentions):",
    ]
    for flag in CANONICAL_FLAGS:
        lines.append(f"  {flag:<18} {totals['mentions'].get(flag, 0)}")
    lines.append("")
    lines.append("line status for canonical flags:")
    for state in ("open", "closed", "unmarked"):
        lines.append(f"  {state:<10} {totals['mentionsByStatus'].get(state, 0)}")
    lines.append("")
    lines.append("corpora carrying canonical flags:")
    for corpus, bucket in inventory["byCorpus"].items():
        canonical = sum(
            count for flag, count in bucket["mentions"].items() if flag in CANONICAL_FLAGS
        )
        if canonical:
            lines.append(
                f"  {corpus:<40} files={bucket['files']:<4} mentions={canonical}"
            )
    lines.append("")
    lines.append(
        f"JSON `holds` arrays: {totals['filesWithJsonHolds']} files, "
        f"{sum(totals['jsonHoldsValues'].values())} values"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("-o", "--output", help="write JSON here instead of stdout")
    parser.add_argument("--summary", action="store_true", help="print a human-readable summary")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    inventory = scan(root)

    if args.summary:
        print(summary(inventory))
        return 0

    text = json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
