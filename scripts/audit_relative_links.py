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
* ``missing-anchor`` - the file exists, but the ``#fragment`` names no heading
  in it (a dead section locator);
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
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
SLUG_DROP_RE = re.compile(r"[^\w\- \u0400-\u04ff]")
SCHEME_RE = re.compile(r"^(?:https?|mailto|tel|ftp):", re.IGNORECASE)
BARE_HOST_RE = re.compile(r"^(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+/", re.IGNORECASE)
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

SKIP_DIRS = {".git", "node_modules", ".arena", ".cache", ".local", "__pycache__",
             ".pytest_cache", ".ruff_cache", ".venv", "venv", ".mypy_cache"}
STATES = ("resolves", "missing", "outside", "unqualified", "external", "missing-anchor",
          "fragment", "missing-fragment")


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


def slugify(text: str) -> str:
    """GitHub-flavoured anchor slug, close enough for checking our own headings.

    Links and inline code are removed first so that a heading like
    ``## См. [`X`](x.md)`` slugs by its visible words, not by the markup.
    """
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)
    text = text.replace("`", "")
    text = re.sub(r"[*_]{1,3}", "", text)
    text = text.strip().lower()
    text = SLUG_DROP_RE.sub("", text)
    return text.replace(" ", "-")


def normalise_anchor(anchor: str) -> str:
    """Fold cosmetic differences that do not change which heading is meant.

    En/em dashes render as nothing on GitHub, so ``6–7`` and ``6-7`` are the same
    place; repeated hyphens come from the spaces around a dropped dash.
    """
    anchor = anchor.replace("\u2013", "-").replace("\u2014", "-")
    anchor = re.sub(r"(?<=\d)-(?=\d)", "", anchor)
    return re.sub(r"-{2,}", "-", anchor.lower())


def anchors_of(path: Path) -> set[str]:
    out: set[str] = set()
    seen: dict[str, int] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return out
    for line in lines:
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify(match.group(1))
        count = seen.get(base, 0)
        seen[base] = count + 1
        out.add(base if count == 0 else f"{base}-{count}")
    return out


def classify(raw: str, source: Path, root: Path, anchor_cache: dict[Path, set[str]] | None = None) -> tuple[str, str]:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if target.startswith("#"):
        # An in-page anchor is checkable against the source file's own headings. It is
        # reported, but not counted as a defect: the slug rules are approximated here, and
        # gating on our own approximation would turn a guess into a verdict.
        cache = anchor_cache if anchor_cache is not None else {}
        anchors = cache.get(source)
        if anchors is None:
            anchors = anchors_of(source)
            cache[source] = anchors
        wanted = normalise_anchor(unquote(target[1:]))
        known = {normalise_anchor(a) for a in anchors}
        return ("fragment", "in-page anchor resolves") if wanted in known or wanted == "" \
            else ("missing-fragment", "no such heading in this file")
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
        fragment = unquote(target.split("#", 1)[1]) if "#" in target else ""
        if fragment and resolved.suffix.lower() == ".md":
            cache = anchor_cache if anchor_cache is not None else {}
            anchors = cache.get(resolved)
            if anchors is None:
                anchors = anchors_of(resolved)
                cache[resolved] = anchors
            wanted = normalise_anchor(fragment)
            known = {normalise_anchor(a) for a in anchors}
            if wanted not in known and not fragment.startswith("L"):
                return "missing-anchor", "no such heading in target"
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
    anchor_cache: dict[Path, set[str]] = {}
    # "Links carrying a #fragment" is a claim the register makes about itself, so it has to
    # be counted here: in-page anchors and file-relative targets of the form doc.md#heading
    # are different states but the same kind of locator.
    fragments: Counter = Counter()
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(strip_fences(text).splitlines(), 1):
            for match in LINK_RE.finditer(line):
                is_image = bool(match.group(1))
                state, reason = classify(match.group(2), path, root, anchor_cache)
                kind = "image" if is_image else "link"
                by_state[state] += 1
                kinds[state if kind == "link" else f"image-{state}"] += 1
                target = match.group(2).strip()
                if "#" in target and not SCHEME_RE.match(target):
                    fragments["total"] += 1
                    fragments["in-page" if target.startswith("#") else "cross-file"] += 1
                    fragments["resolved" if state in ("fragment", "resolves") else "unresolved"] += 1
                if state in ("missing", "outside", "unqualified", "missing-anchor"):
                    by_file[rel] += 1
                if state in ("missing", "outside", "unqualified", "missing-anchor"):
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
            "defects": sum(by_state.get(s, 0) for s in ("missing", "outside", "unqualified", "missing-anchor")),
            "fragments": {
                "total": fragments.get("total", 0),
                "inPage": fragments.get("in-page", 0),
                "crossFile": fragments.get("cross-file", 0),
                "resolved": fragments.get("resolved", 0),
                "unresolved": fragments.get("unresolved", 0),
                "note": "Links whose target carries a #fragment; in-page anchors are reported, not counted as defects.",
            },
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
