#!/usr/bin/env python3
"""Check the date a document puts on itself against when Git last changed it.

A header like ``**Обновлено: 2026-11-13**`` or ``**As of 2026-10-26**`` is a claim
about the document's own currency: a reader is meant to take everything below it as
true on that day. Nothing checks it, so a file can be edited for weeks while its
stamp keeps pointing at an earlier Tuesday.

For every Markdown file whose first lines carry such a stamp, this tool reports:

* ``current``               - the last commit that touched the file is the stamp day;
* ``edited-after-stamp``    - the file changed after the date it declares: the reader
  is being handed later edits as if they were as old as the stamp;
* ``stamp-ahead-of-history`` - the stamp is later than any commit: the document claims
  a state it never had in Git (often a stamp added before the change it describes);
* ``stamp-in-future``       - the stamp is later than today, which cannot be true.

``edited-after-stamp`` is not automatically a lie: a lane may legitimately add a
section dated later, or a numbering-only edit may land afterwards. The tool reports
the stamp, the last commit day and that commit's subject, and stops there - it never
rewrites the stamp, because moving a date to "now" would manufacture exactly the
freshness the check exists to question.

Scope is deliberately narrow: only the first ``--head`` lines, only a stamp phrase
(``по состоянию на``, ``обновлено``, ``last updated``, ``as of``, ``актуально на``)
that is followed by a date on the same line, and never a table row or a line with a
URL - those cite somebody else's date, not this document's.

    python3 -B scripts/audit_state_stamps.py --summary
    python3 -B scripts/audit_state_stamps.py -o data/state-stamps-2026-11-18.json
    python3 -B scripts/audit_state_stamps.py --check      # 1 on an impossible stamp
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA_VERSION = "state-stamps/1"
AUTHORITY_ID = "STATE-STAMPS-2026-11-18"

SKIP_DIRS = {".git", "node_modules", "incoming", ".venv", "__pycache__"}
STAMP_RE = re.compile(
    r"(?:\u043f\u043e\s+\u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044e\s+\u043d\u0430"
    r"|\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u043e|last\s+updated|updated\s*:"
    r"|as\s+of|\u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d[а-яё]*\s+\u043d\u0430)",
    re.I,
)
DATE_RE = re.compile(r"\b(\d{2})\.(\d{2})\.(\d{4})\b|\b(\d{4})-(\d{2})-(\d{2})\b")


def parse_date(match: re.Match) -> datetime.date | None:
    try:
        if match.group(1):
            return datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
        return datetime.date(int(match.group(4)), int(match.group(5)), int(match.group(6)))
    except ValueError:
        return None


def iter_markdown(root: Path) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if set(rel.parts) & SKIP_DIRS:
            continue
        if rel.parts[:1] == ("data",):
            continue
        out.append(path)
    return out


def stamp_of(text: str, head: int) -> tuple[int, datetime.date, str] | None:
    for lineno, line in enumerate(text.splitlines()[:head], 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("|") or "http" in stripped:
            continue
        match = STAMP_RE.search(stripped)
        if not match:
            continue
        date_match = DATE_RE.search(stripped[match.end():])
        if not date_match:
            continue
        parsed = parse_date(date_match)
        if parsed is None:
            continue
        return lineno, parsed, stripped[:300]
    return None


def git_history(path: Path, root: Path) -> dict:
    def run(*args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
        )
        return completed.stdout.strip()

    last = run("log", "-1", "--format=%cs%x00%s", "--", str(path))
    first = run("log", "--diff-filter=A", "--format=%cs", "--", str(path)).splitlines()
    last_day, _, subject = last.partition("\x00")
    return {
        "lastCommit": last_day or None,
        "lastSubject": subject or None,
        "addedCommit": first[-1] if first else None,
    }


def state_of(stamp: datetime.date, history: dict, today: datetime.date) -> str:
    if stamp > today:
        return "stamp-in-future"
    last = history["lastCommit"]
    if last is None:
        return "unknown"
    if last == stamp.isoformat():
        return "current"
    if last > stamp.isoformat():
        return "edited-after-stamp"
    return "stamp-ahead-of-history"


def audit(root: Path, head: int = 15, today: datetime.date | None = None,
          history_lookup=git_history) -> dict:
    today = today or datetime.date.today()
    findings = []
    by_state: dict[str, int] = {}
    for path in iter_markdown(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        found = stamp_of(text, head)
        if not found:
            continue
        lineno, stamp, line = found
        history = history_lookup(path, root)
        state = state_of(stamp, history, today)
        by_state[state] = by_state.get(state, 0) + 1
        findings.append({
            "file": rel, "line": lineno, "stamp": stamp.isoformat(),
            "state": state, "text": line,
            "lastCommit": history["lastCommit"], "lastSubject": history["lastSubject"],
            "addedCommit": history["addedCommit"],
        })
    findings.sort(key=lambda f: (f["state"], f["file"]))
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "root": ".",
        "scope": {"markdownFiles": len(iter_markdown(root)), "headLines": head,
                  "today": today.isoformat()},
        "totals": {
            "stamped": len(findings),
            "byState": by_state,
            "impossible": by_state.get("stamp-in-future", 0),
        },
        "findings": findings,
    }


def summary(report: dict) -> str:
    scope, totals = report["scope"], report["totals"]
    lines = [
        f"Documents with a self-dating stamp in the first {scope['headLines']} lines:"
        f" {totals['stamped']} of {scope['markdownFiles']} Markdown files",
        "States: " + (", ".join(f"{k}={v}" for k, v in sorted(totals["byState"].items())) or "none"),
    ]
    for finding in report["findings"]:
        lines.append(
            f"  {finding['state']:22s} stamp={finding['stamp']} last={finding['lastCommit']}"
            f"  {finding['file']}:{finding['line']}"
        )
        if finding["state"] in ("edited-after-stamp", "stamp-in-future"):
            lines.append(f"      last commit: {finding['lastSubject']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("-o", "--output")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--check", action="store_true", help="fail on an impossible stamp")
    parser.add_argument("--head", type=int, default=15)
    # The report records the date it was taken as scope.today, so it can only be reproduced
    # with that date given: without this flag the committed artefact stops matching on the
    # next calendar day, and a report nobody can regenerate is not evidence.
    parser.add_argument("--today", default=None, help="the date to judge against (default: today)")
    parser.add_argument("--only", choices=("current", "edited-after-stamp", "stamp-ahead-of-history",
                                           "stamp-in-future"))
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    report = audit(root, head=args.head,
                   today=datetime.date.fromisoformat(args.today) if args.today else None)
    if args.only:
        report["findings"] = [f for f in report["findings"] if f["state"] == args.only]
    if args.output:
        Path(args.output).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"wrote {args.output}", file=sys.stderr)
    if args.summary or not args.output:
        print(summary(report))
    if args.check and report["totals"]["impossible"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
