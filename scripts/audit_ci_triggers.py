#!/usr/bin/env python3
"""Check the gate's trigger list against what the gate actually reads.

``.github/workflows/holds-inventory.yml`` runs the register's gates, but only when one
of the paths it lists changes. That list is hand-maintained, and §22.2 already recorded
the consequence: a divergence can sit unnoticed until something touches a trigger path.

The list is not a wish list - it is a statement about dependencies. So it can be checked
against the dependencies themselves:

* **cleanliness** - no path appears twice in one list;
* **symmetry** - ``pull_request`` and ``push`` list the same set. Two copies of one
  statement, kept by hand, is the drift this register documents everywhere else;
* **scripts** - every script the workflow executes is a trigger, or editing the gate
  would not run the gate;
* **inputs** - every file under ``data/``, ``docs/`` or ``.github/`` that a gated script
  names as a path constant is a trigger.

What this does **not** claim: that a trigger fires on the content a gate depends on in
general. Corpora markdown, for instance, is read by the text-integrity gate in bulk; no
path list can express "the whole tree" without firing on every commit. The boundary is
declared in ``NOT_TRIGGERABLE`` below rather than left implicit.

Usage::

    python3 -B scripts/audit_ci_triggers.py --check
    python3 -B scripts/audit_ci_triggers.py --summary
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "holds-inventory.yml"

EVENTS = ("pull_request", "push")
WATCHED_PREFIXES = ("data/", "docs/", ".github/")
SUFFIXES = (".json", ".md", ".yml", ".yaml", ".py")

# Inputs reached through another artefact's content. A general walk would "discover" the
# 2 416 corpus files the link audit merely observes - observations are not inputs - so
# transitive dependencies are declared here, with the reason, and checked like the rest.
DECLARED_INPUTS = {
    "data/publication-gate-queue-v1.json": [
        ("data/public-projection-queue-2026-08-01.json", "base queue named by the queue's own entries"),
        ("data/public-projection-osk-wave6-overlay-2026-08-01.json", "overlay named by the queue's entries"),
        ("data/bratsky-listok-publication-ledger.json", "publication ledger of a queued corpus"),
        ("data/genesis6-authority-manifest.json", "authority manifest of a queued corpus"),
        ("data/genesis6-enoch-extension-authority-manifest.json", "authority manifest of a queued corpus"),
    ],
}

# Gates that read whole corpora cannot be triggered by a path list without firing on
# every commit. Named here so the limit is a decision, not an oversight.
NOT_TRIGGERABLE = {
    "corpus markdown": "text integrity and link audits read the whole tree; the trigger is "
                       "the tool or the register, and §22.2 states the cost of that choice",
}

PATH_LIKE = re.compile(r"(?<![\w/.-])((?:data|docs|\.github|scripts)/[\w./§—-]+?\.(?:json|md|ya?ml|py))")


class WorkflowError(Exception):
    pass


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def trigger_lists(text: str) -> dict[str, list[str]]:
    """event -> path list, parsed by indentation so a wrong shape fails loudly."""
    lines = text.splitlines()
    out: dict[str, list[str]] = {}
    for event in EVENTS:
        start = None
        for i, line in enumerate(lines):
            if line.strip() == f"{event}:" and _indent(line) <= 2:
                start = i
                break
        if start is None:
            raise WorkflowError(f"workflow has no '{event}' event block")
        base = _indent(lines[start])
        paths_at = None
        for j in range(start + 1, len(lines)):
            line = lines[j]
            if line.strip() and _indent(line) <= base and not line.strip().startswith("paths:"):
                break
            if line.strip() == "paths:":
                paths_at = _indent(line)
                j0 = j
                break
        if paths_at is None:
            raise WorkflowError(f"event '{event}' has no paths: filter")
        entries: list[str] = []
        for line in lines[j0 + 1:]:
            if not line.strip():
                continue
            if _indent(line) <= paths_at:
                break
            item = line.strip()
            if not item.startswith("- "):
                raise WorkflowError(f"unexpected line under paths: {item!r}")
            entries.append(item[2:].strip().strip("'").strip('"'))
        if not entries:
            raise WorkflowError(f"event '{event}' has an empty paths: list")
        out[event] = entries
    return out


def workflow_body(text: str) -> str:
    marker = text.find("\njobs:")
    return text[marker:] if marker != -1 else ""


def scripts_run(body: str) -> set[str]:
    return {m.group(0) for m in PATH_LIKE.finditer(body) if m.group(0).startswith("scripts/")}


def files_named(body: str) -> set[str]:
    return {(ROOT / m.group(0)).relative_to(ROOT).as_posix()
            for m in PATH_LIKE.finditer(body)
            if not m.group(0).startswith("scripts/") and (ROOT / m.group(0)).is_file()}


def _string_parts(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {node.value}
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left, right = _string_parts(node.left), _string_parts(node.right)
        if left and right:
            return {f"{a}/{b.lstrip('/')}" for a in left for b in right}
        return left | right
    return set()


def literals_in(script: Path, root: Path = ROOT) -> set[str]:
    """Watched paths a script names as a bare string literal anywhere in its source."""
    try:
        tree = ast.parse(script.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        raise WorkflowError(f"cannot read {script}: {exc}") from exc
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value.lstrip("/")
            if value.startswith(WATCHED_PREFIXES) and value.endswith(SUFFIXES) and (root / value).is_file():
                out.add(value)
    return out


def constants_in(script: Path, root: Path = ROOT) -> set[str]:
    """Paths a script names, composed (``ROOT / "data" / "x.json"``) or literal."""
    try:
        tree = ast.parse(script.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        raise WorkflowError(f"cannot read {script}: {exc}") from exc
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            found |= _string_parts(getattr(node, "value", None) or ast.Constant(""))
    out: set[str] = set()
    for value in found:
        candidate = value.lstrip("/")
        if not candidate.startswith(WATCHED_PREFIXES) or not candidate.endswith(SUFFIXES):
            continue
        if "*" in candidate or "{" in candidate:
            continue
        if (root / candidate).is_file():
            out.add(candidate)
    return out | literals_in(script, root)


def check(text: str, root: Path = ROOT, declared: dict | None = None) -> list[str]:
    declared = DECLARED_INPUTS if declared is None else declared
    problems: list[str] = []
    lists = trigger_lists(text)

    for event, entries in lists.items():
        seen: set[str] = set()
        for entry in entries:
            if entry in seen:
                problems.append(f"duplicate trigger path in {event}: {entry}")
            seen.add(entry)
        for entry in entries:
            if not (root / entry).exists() and not any(ch in entry for ch in "*?["):
                problems.append(f"trigger path does not exist in {event}: {entry}")

    pr, push = set(lists["pull_request"]), set(lists["push"])
    for path in sorted(pr - push):
        problems.append(f"listed for pull_request but not for push: {path}")
    for path in sorted(push - pr):
        problems.append(f"listed for push but not for pull_request: {path}")

    body = workflow_body(text)
    if not body:
        raise WorkflowError("workflow has no jobs: block")
    for script in sorted(scripts_run(body)):
        if script not in pr:
            problems.append(f"script executed by the workflow is not a trigger path: {script}")
    for named in sorted(files_named(body)):
        if named not in pr:
            problems.append(f"file named by the workflow is not a trigger path: {named}")

    for script in sorted(scripts_run(body)):
        if not (root / script).is_file():
            problems.append(f"workflow runs a script that does not exist: {script}")
            continue
        for dependency in sorted(constants_in(root / script, root)):
            if dependency not in pr:
                problems.append(
                    f"read by {script} but not a trigger path: {dependency}")

    for artefact, inputs in sorted(declared.items()):
        if artefact not in pr:
            problems.append(f"declared input artefact is not a trigger path: {artefact}")
        for path, reason in inputs:
            if not (root / path).is_file():
                problems.append(f"declared input does not exist: {path} ({reason})")
            elif path not in pr:
                problems.append(f"input of {artefact} but not a trigger path: {path} ({reason})")
    return problems


def summary(text: str, root: Path = ROOT) -> dict:
    lists = trigger_lists(text)
    body = workflow_body(text)
    return {
        "workflow": WORKFLOW.relative_to(ROOT).as_posix(),
        "pullRequestPaths": len(set(lists["pull_request"])),
        "pushPaths": len(set(lists["push"])),
        "duplicates": len(lists["pull_request"]) - len(set(lists["pull_request"]))
                      + len(lists["push"]) - len(set(lists["push"])),
        "scripts": len(scripts_run(body)),
        "declaredNotTriggerable": NOT_TRIGGERABLE,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail on any problem")
    parser.add_argument("--summary", action="store_true", help="print the measured shape")
    parser.add_argument("--workflow", default=str(WORKFLOW))
    args = parser.parse_args(argv)

    try:
        text = Path(args.workflow).read_text(encoding="utf-8")
        problems = check(text)
        shape = summary(text)
    except WorkflowError as exc:
        print(f"ci triggers: {exc}", file=sys.stderr)
        return 2

    if args.summary:
        print(f"workflow: {shape['workflow']}")
        print(f"trigger paths: pull_request={shape['pullRequestPaths']}, push={shape['pushPaths']}, "
              f"duplicates={shape['duplicates']}")
        print(f"scripts executed: {shape['scripts']}")
    if problems:
        for problem in problems:
            print(f"ci triggers: {problem}", file=sys.stderr)
        return 1
    if args.check or not args.summary:
        print(f"ci triggers: PASS — {shape['pullRequestPaths']} paths cover {shape['scripts']} scripts "
              f"and the files they read; pull_request and push agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
