#!/usr/bin/env python3
"""Find text that lost the spaces around numbers, and repair what git can prove.

Some bulk passes over this repository have written prose without spaces where
the numbers were: ``Архитектура10будущих документов`` instead of ``Архитектура 10
будущих документов``. The words are still there, so no HOLD fires and no link is
dead, but the sentences are damaged and quotes inside them cannot be trusted as
transcribed text.

The repair is not a guess. For every glued token the file's own git history is
searched for the same words with the spaces present; the repair is applied only
when that evidence is found, and the whole window around the token - not just
the token - has to match. Tokens without evidence are reported and left alone.

A file with no readable history (a shallow clone, or a file added in the very
commit being checked) is marked ``not-checked``: the tool does not claim either
way, and ``--check`` does not fail on it.

A file whose current bytes are named by a SHA-256 somewhere in the corpus is
never rewritten: that hash is a receipt, and editing the file would quietly
break it. Such files are reported with state ``receipt-blocked`` and need their
owning lane to re-issue the receipt after repair.

Known limit: only word-number-word boundaries are seen. A number that merely
trails a word (``Кор80``) is not repaired, because citation shapes such as
``Мф5`` and ``1Кор`` look identical and are legitimate.

    python3 -B scripts/audit_text_integrity.py --summary      # count only
    python3 -B scripts/audit_text_integrity.py -o report.json # full report
    python3 -B scripts/audit_text_integrity.py --repair       # rewrite backed tokens
    python3 -B scripts/audit_text_integrity.py --check        # 1 if any remain
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA_VERSION = "text-integrity-audit/1"
AUTHORITY_ID = "TEXT-INTEGRITY-GLUED-TOKENS-2026-11-18"

# A word, a number and another word with nothing between them. Latin is left out
# on purpose: ``A32726`` and ``EEBO-TCP`` are identifiers, not damaged prose.
TOKEN_RE = re.compile(r"([\u0410-\u044f\u0401\u0451]+)(\d+)([\u0410-\u044f\u0401\u0451]+)")
SUFFIXES = {".md", ".json", ".txt"}
CONTEXT = 25
SKIP_DIRS = {".git", "node_modules", "incoming/archive"}
# ИСКУПЛЕНИЕ keeps a byte-for-byte inventory of its lane sources and data corpus
# (.github/workflows/atonement-corpus-integrity.yml, atonement_reshoot_state).
# One inserted space re-issues a whole lane snapshot that other agents are
# editing, so repairs there belong to that lane's own round, not to this tool.
WITNESSED_PREFIXES = (
    "ИСКУПЛЕНИЕ/ot/",
    "ИСКУПЛЕНИЕ/nt/",
    "ИСКУПЛЕНИЕ/fathers/",
    "ИСКУПЛЕНИЕ/synthesis/",
    "ИСКУПЛЕНИЕ/data/",
)
# The tool's own report quotes glued forms on purpose; scanning it would make the
# count depend on the previous run.
SELF_REFERENTIAL = {"data/text-integrity-repairs-2026-11-18.json"}
HISTORY_LIMIT = 150


def iter_text_files(root: Path) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        if any(part in rel.split("/")[0] for part in SKIP_DIRS if "/" not in part):
            continue
        if rel in SELF_REFERENTIAL:
            continue
        out.append(path)
    return out


def mask_code(text: str) -> str:
    """Blank out code spans while keeping every offset where it was.

    Identifiers live in code legitimately, so they must not be scanned; but the
    caller writes the repaired text back at these offsets, so a mask may only
    replace characters with spaces - never remove them.
    """
    def blank(match: re.Match[str]) -> str:
        return "".join(ch if ch == "\n" else " " for ch in match.group(0))

    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    return re.sub(r"`[^`\n]*`", blank, text)


def find_tokens(text: str) -> list[tuple[int, str]]:
    return [(m.start(), m.group(0)) for m in TOKEN_RE.finditer(mask_code(text))]


def spaced(token: str) -> str:
    match = TOKEN_RE.fullmatch(token)
    if not match:
        return token
    return f"{match.group(1)} {match.group(2)} {match.group(3)}"


def flexible_pattern(window: str) -> str:
    """The window, with every whitespace choice allowed to differ."""
    parts = re.split(r"(\d+)", window)
    return r"\s*".join(re.escape(p.strip()) for p in parts if p.strip())


def window_of(text: str, start: int, token: str) -> str:
    return text[max(0, start - CONTEXT):start + len(token) + CONTEXT]


def file_history_text(path: Path, root: Path, limit: int = HISTORY_LIMIT) -> str:
    """Every previous version of the file, concatenated; empty outside a repo."""
    rel = path.relative_to(root).as_posix()
    try:
        shas = subprocess.run(
            ["git", "-C", str(root), "log", "--format=%H", "--", rel],
            capture_output=True, text=True, check=False,
        ).stdout.split()
    except OSError:
        return ""
    chunks = []
    for sha in shas[:limit]:
        blob = subprocess.run(
            ["git", "-C", str(root), "show", f"{sha}:{rel}"],
            capture_output=True, text=True, check=False,
        )
        if blob.returncode == 0:
            chunks.append(blob.stdout)
    return "\n".join(chunks)


def has_evidence(window: str, history: str) -> bool:
    if not history:
        return False
    return re.search(flexible_pattern(window), history) is not None


HEX64_RE = re.compile(r"\b[0-9a-f]{64}\b")


def recorded_hashes(root: Path) -> set[str]:
    """Every 64-hex string written anywhere in the corpus, i.e. every receipt."""
    seen: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        if ".git" in path.parts:
            continue
        try:
            seen.update(HEX64_RE.findall(path.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    return seen


def lane_witnessed(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    return rel.startswith(WITNESSED_PREFIXES)


def receipt_blocked(path: Path, receipts: set[str]) -> bool:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest() in receipts


def audit(root: Path, history_provider=None, ignore_receipts: bool = False) -> dict:
    history_provider = history_provider or file_history_text
    receipts = set() if ignore_receipts else recorded_hashes(root)
    findings = []
    per_file: dict[str, dict] = {}
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        tokens = find_tokens(text)
        if not tokens:
            continue
        history = history_provider(path, root)
        if lane_witnessed(path, root):
            state_for_all = "lane-blocked"
        elif not ignore_receipts and receipt_blocked(path, receipts):
            state_for_all = "receipt-blocked"
        else:
            state_for_all = ""
        blocked = bool(state_for_all)
        for start, token in tokens:
            window = window_of(text, start, token)
            if blocked:
                state = state_for_all
            elif not history:
                state = "not-checked"
            elif has_evidence(window, history):
                state = "evidence"
            else:
                state = "no-evidence"
            findings.append({
                "file": path.relative_to(root).as_posix(),
                "token": token,
                "repaired": spaced(token),
                "state": state,
            })
            bucket = per_file.setdefault(path.relative_to(root).as_posix(), {"tokens": 0, "withEvidence": 0})
            bucket["tokens"] += 1
            if state == "evidence":
                bucket["withEvidence"] += 1
    by_state: dict[str, int] = {}
    for item in findings:
        by_state[item["state"]] = by_state.get(item["state"], 0) + 1
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "root": ".",
        "scope": {"textFiles": len(iter_text_files(root))},
        "totals": {
            "gluedTokens": len(findings),
            "byState": by_state,
            "filesWithTokens": len(per_file),
        },
        "files": dict(sorted(per_file.items(), key=lambda kv: (-kv[1]["tokens"], kv[0]))),
        "findings": findings,
    }


def repair(root: Path, history_provider=None, passes: int = 5,
           ignore_receipts: bool = False) -> dict:
    """Insert the missing spaces where the file's history shows them.

    One pass is not enough when two tokens touched each other: the first
    insertion changes the window the second one is judged by. The loop repeats
    until nothing changes, so a single --repair always reaches the fixpoint.
    """
    history_provider = history_provider or file_history_text
    totals: dict[str, int] = {}
    skipped: list[str] = []
    receipts = set() if ignore_receipts else recorded_hashes(root)
    for attempt in range(passes):
        changed = False
        for path in iter_text_files(root):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            tokens = find_tokens(text)
            if not tokens:
                continue
            if lane_witnessed(path, root) or (not ignore_receipts and receipt_blocked(path, receipts)):
                rel = path.relative_to(root).as_posix()
                if rel not in skipped:
                    skipped.append(rel)
                continue
            history = history_provider(path, root)
            new_text = text
            applied = 0
            for start, token in reversed(tokens):
                window = window_of(text, start, token)
                if not has_evidence(window, history):
                    continue
                end = start + len(token)
                new_text = new_text[:start] + spaced(token) + new_text[end:]
                applied += 1
            if applied and new_text != text:
                path.write_text(new_text, encoding="utf-8")
                changed = True
                rel = path.relative_to(root).as_posix()
                totals[rel] = totals.get(rel, 0) + applied
        if not changed:
            break
    files = [{"file": name, "repaired": count} for name, count in sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))]
    return {
        "repairedFiles": len(files),
        "repairedTokens": sum(totals.values()),
        "files": files,
        "skippedReceipts": sorted(skipped),
    }


def summary(report: dict) -> str:
    totals = report["totals"]
    states = totals["byState"]
    lines = [
        f"Text files scanned: {report['scope']['textFiles']}",
        f"Glued tokens: {totals['gluedTokens']} in {totals['filesWithTokens']} files "
        f"(evidence={states.get('evidence', 0)}, no-evidence={states.get('no-evidence', 0)})",
        "Nothing is repaired by --summary; --repair rewrites only tokens the history proves.",
    ]
    for name, data in list(report["files"].items())[:10]:
        lines.append(f"  {data['tokens']:5d} tokens ({data['withEvidence']} with evidence)  {name}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("-o", "--output")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--check", action="store_true", help="exit 1 if any repairable glued token remains")
    parser.add_argument("--ignore-receipts", action="store_true",
                        help="repair even where the corpus records the file's current sha256")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if args.repair:
        result = repair(root, ignore_receipts=args.ignore_receipts)
        print(f"repaired {result['repairedTokens']} tokens in {result['repairedFiles']} files")
        for item in result["files"]:
            print(f"  {item['repaired']:5d}  {item['file']}")
        for name in result["skippedReceipts"]:
            print(f"  skipped (sha256 on record): {name}")
        return 0

    report = audit(root, ignore_receipts=args.ignore_receipts)
    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    if args.summary or not args.output:
        print(summary(report))
    if args.check and (report["totals"]["byState"].get("evidence")
                       or report["totals"]["byState"].get("no-evidence")):
        # A token whose repair is blocked by a recorded hash is not this tool's
        # to fix; it must fail only when a repairable token is still there.
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
