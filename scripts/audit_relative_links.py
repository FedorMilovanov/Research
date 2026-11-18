#!/usr/bin/env python3
"""Read-only audit of relative links in Markdown files.

A relative link is a locator: it either resolves to bytes in this checkout or
it does not. This script answers exactly that question and nothing more. It
never rewrites a link, never clears a ``LOCATOR_HOLD`` and never treats a
resolving link as evidence about the *object* the link talks about -- a path
that opens says "these bytes exist", not "this claim is verified".

Link states:

* ``resolves``   - the target exists inside the repository;
* ``missing``    - the target is absent (a dead locator);
* ``outside``    - the target escapes the repository root (absolute paths and
  ``../`` chains that leave the tree);
* ``unqualified``- a bare host (``www.example.org/x.pdf``) parsed by Markdown
  as a relative path; a scheme is missing;
* ``external``   - ``http(s)``, ``mailto``, ``tel`` and in-page ``#anchor``
  links; not a filesystem locator and therefore not judged here.

Code fences and inline code spans are skipped: a link written inside an example
block or inside backticks is quoted syntax, not a locator. Images are counted separately (``image``) because a missing image
is a rendering defect, not a citation one.

Usage::

    python3 scripts/audit_relative_links.py --summary
    python3 scripts/audit_relative_links.py -o data/relative-links-inventory-v1.json
    python3 scripts/audit_relative_links.py --only missing --only unqualified
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

SCHEMA_VERSION = 1
AUTHORITY_ID = "RESEARCH-RELATIVE-LINKS-INVENTORY-V1"

ROOT = Path(__file__).resolve().parents[1]

LINK_RE = re.compile(r"(!?)\[[^\]\n]*\]\(([^()\n]+)\)")
SCHEME_RE = re.compile(r"^(?:https?|mailto|tel|ftp):", re.IGNORECASE)
BARE_HOST_RE = re.compile(r"^(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+/", re.IGNORECASE)
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

SKIP_DIRS = {".git", "node_modules", ".arena", ".cache", ".local", "__pycache__",
             ".pytest_cache", ".ruff_cache", ".venv", "venv", ".mypy_cache"}
STATES = ("resolves", "missing", "outside", "unqualified", "external")


def iter_markdown(root: Path) -> list[Path]:
    out = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        out.append(path)
    return sorted(out)


def strip_fences(text: str) -> str:
    """Drop fenced code blocks, keeping line count (line numbers stay true)."""
    result: list[str] = []
    inside = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            inside = not inside
            result.append("")
            continue
        # inline code is quoted syntax (``[x](y)`` as an example), not a locator:
        # blank only the span so that line numbers and the rest of the line survive
        result.append("" if inside else INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(result)


def classify(raw: str, source: Path, root: Path) -> tuple[str, str]:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if target.startswith("#"):
        return "external", "in-page anchor"
    if SCHEME_RE.match(target):
        return "external", "scheme"
    path_part = unquote(target.split("#")[0].split("?")[0])
    if not path_part:
        return "external", "empty"
    if BARE_HOST_RE.match(path_part) and not (source.parent / path_part).exists():
        return "unqualified", "missing scheme"
    resolved = (source.parent / path_part).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return "outside", "escapes repository root"
    if resolved.exists():
        return "resolves", "ok"
    if (root / path_part).exists():
        # a copy of a root-level document (an archive snapshot) carries the original
        # document's relative paths; they resolve from the root, not from the copy
        return "missing", "absent here; resolves from repository root"
    return "missing", "no such path"


def load_exceptions(path: Path | None) -> dict[tuple[str, str], str]:
    """Justified exceptions: (file, target) -> reason.

    An exception is not a repair. It records that a dead locator is known and
    why it is deliberately not rewritten (a historical record, a lossless
    snapshot, a document whose objects never lived in this repository). New
    dead locators are never covered by it: the key is the exact pair.
    """
    if path is None or not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], str] = {}
    for item in data.get("exceptions", []):
        reason = str(item.get("reason", "")).strip()
        if not reason:
            raise ValueError(f"exception without reason: {item}")
        out[(item["file"], item["target"])] = reason
    return out


def scan(root: Path, exceptions: dict[tuple[str, str], str] | None = None) -> dict:
    files = iter_markdown(root)
    exceptions = exceptions or {}
    findings: list[dict] = []
    by_state: Counter = Counter()
    by_file: Counter = Counter()
    kinds: Counter = Counter()
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(strip_fences(text).splitlines(), 1):
            for match in LINK_RE.finditer(line):
                is_image = bool(match.group(1))
                state, reason = classify(match.group(2), path, root)
                kind = "image" if is_image else "link"
                by_state[state] += 1
                kinds[state if kind == "link" else f"image-{state}"] += 1
                if state in ("missing", "outside", "unqualified"):
                    by_file[rel] += 1
                if state in ("missing", "outside", "unqualified"):
                    target_text = match.group(2).strip()
                    justification = exceptions.get((rel, target_text))
                    findings.append({
                        "file": rel,
                        "line": lineno,
                        "kind": kind,
                        "state": state,
                        "target": target_text,
                        "reason": reason,
                        "explained": justification or "",
                    })
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "root": ".",
        "scope": {"markdownFiles": len(files)},
        "totals": {
            "byState": {state: by_state.get(state, 0) for state in STATES},
            "byKind": dict(sorted(kinds.items())),
            "defects": sum(by_state.get(s, 0) for s in ("missing", "outside", "unqualified")),
            "filesWithDefects": len(by_file),
            "explained": sum(1 for f in findings if f["explained"]),
            "unexplained": sum(1 for f in findings if not f["explained"]),
        },
        "defectsByFile": dict(sorted(by_file.items(), key=lambda kv: (-kv[1], kv[0]))),
        "findings": findings,
    }


def summary(report: dict) -> str:
    totals = report["totals"]
    states = totals["byState"]
    lines = [
        f"Markdown files scanned: {report['scope']['markdownFiles']}",
        "Links by state: " + ", ".join(f"{k}={v}" for k, v in states.items()),
        f"Defective locators: {totals['defects']} in {totals['filesWithDefects']} files "
        f"(explained {totals['explained']}, unexplained {totals['unexplained']})",
    ]
    for rel, count in list(report["defectsByFile"].items())[:15]:
        lines.append(f"  {count:3d}  {rel}")
    if len(report["defectsByFile"]) > 15:
        lines.append(f"  ... {len(report['defectsByFile']) - 15} more files")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only relative-link audit (never rewrites links)")
    parser.add_argument("-o", "--output", help="write the full inventory as JSON")
    parser.add_argument("--summary", action="store_true", help="print a human-readable summary")
    parser.add_argument("--only", action="append", choices=STATES,
                        help="restrict --summary output to these states (repeatable)")
    parser.add_argument("--root", default=str(ROOT), help="repository root (default: this checkout)")
    parser.add_argument("--exceptions", default=None,
                        help="justified exceptions JSON (default: data/relative-link-exceptions-v1.json)")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when at least one defect is not explained")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    exc_path = Path(args.exceptions) if args.exceptions else root / "data" / "relative-link-exceptions-v1.json"
    exceptions = load_exceptions(exc_path)
    report = scan(root, exceptions)
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                          encoding="utf-8")
        print(f"wrote {target}")
    if args.summary or not args.output:
        print(summary(report))
        if args.only:
            allowed = set(args.only)
            print("\nFindings:")
            for item in report["findings"]:
                if item["state"] in allowed:
                    print(f"  {item['state']:12s} {item['file']}:{item['line']} -> {item['target'][:80]}")
    if args.strict and report["totals"]["unexplained"]:
        print(f"strict: {report['totals']['unexplained']} unexplained dead locators", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
