#!/usr/bin/env python3
"""Verify pinned GitHub locators cited in Markdown, byte for byte.

Many research claims in this repository point at a GitHub object *pinned to a
commit* and carry a SHA-256 and a byte count ("Commit полученных XML",
"SHA-256 фактических байтов"). Such a claim is checkable without trusting the
author: fetch the object at that exact commit and recompute.

This script:

1. scans Markdown for ``https://github.com/<owner>/<repo>/(blob|raw)/<sha>/<path>``;
2. reads the claim written on the same line, if any -- a 64-hex digest and
   ``(NNN bytes)`` -- without guessing: no digest on the line means "не заявлен";
3. fetches the object at that commit (``gh api`` with the raw media type) and
   recomputes size and SHA-256;
4. reports ``match`` / ``mismatch`` / ``unclaimed`` / ``unavailable``.

It never edits a document and never clears a hold. A match proves that the bytes
at that commit are the bytes the author measured; it does **not** prove that the
author read them, nor that the edition is the right one, nor anything about
rights.

Usage::

    python3 scripts/verify_pinned_github_locators.py --summary
    python3 scripts/verify_pinned_github_locators.py -o data/pinned-github-locators-verified-2026-11-18.json
    python3 scripts/verify_pinned_github_locators.py --offline --summary   # no network: claims only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
AUTHORITY_ID = "RESEARCH-PINNED-GITHUB-LOCATORS-VERIFICATION-V1"
SNAPSHOT_DATE = "2026-11-18"

URL_RE = re.compile(
    r"https://github\.com/([\w.\-]+)/([\w.\-]+)/(?:blob|raw)/([0-9a-f]{7,40})/([^\s)\"'><`]+)")
SHA_RE = re.compile(r"\b([0-9a-f]{64})\b")
SIZE_RE = re.compile(r"\(?(\d{1,3}(?:[ \u00a0]\d{3})+|\d+)\s*(?:bytes|байт)\b\)?")
SKIP_DIRS = {".git", "node_modules", ".arena", ".cache", ".local", "__pycache__",
             ".pytest_cache", ".ruff_cache", ".venv", "venv", ".mypy_cache", "google_drive"}


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield path


def claims_on_line(line: str) -> tuple[str | None, int | None]:
    sha = SHA_RE.search(line)
    size = SIZE_RE.search(line)
    size_value = None
    if size:
        size_value = int(re.sub(r"[ \u00a0]", "", size.group(1)))
    return (sha.group(1) if sha else None), size_value


def collect(root: Path) -> list[dict]:
    found: list[dict] = []
    seen: set[tuple[str, str, str, str]] = set()
    for path in iter_markdown(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(lines, 1):
            for match in URL_RE.finditer(line):
                owner, repo, sha, target = match.group(1), match.group(2), match.group(3), match.group(4)
                target = unquote(target)
                key = (owner, repo, sha, target)
                if key in seen:
                    continue
                seen.add(key)
                claimed_sha, claimed_size = claims_on_line(line)
                found.append({
                    "file": rel,
                    "line": lineno,
                    "repo": f"{owner}/{repo}",
                    "commit": sha,
                    "path": target,
                    "url": match.group(0),
                    "claimedSha256": claimed_sha,
                    "claimedBytes": claimed_size,
                })
    return found


def gh_raw(repo: str, commit: str, path: str) -> bytes | None:
    """Fetch one object at one commit through the authenticated GitHub CLI."""
    api_path = f"repos/{repo}/contents/{path}?ref={commit}"
    proc = subprocess.run(
        ["gh", "api", api_path, "-H", "Accept: application/vnd.github.raw"],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def verify(entries: list[dict], offline: bool = False) -> list[dict]:
    results = []
    for entry in entries:
        item = dict(entry)
        item["state"] = "not-checked" if offline else "unclaimed"
        item["fetchedBytes"] = None
        item["fetchedSha256"] = None
        if offline:
            results.append(item)
            continue
        blob = gh_raw(entry["repo"], entry["commit"], entry["path"])
        if blob is None:
            item["state"] = "unavailable"
            results.append(item)
            continue
        digest = hashlib.sha256(blob).hexdigest()
        item["fetchedBytes"] = len(blob)
        item["fetchedSha256"] = digest
        claimed_sha, claimed_size = entry.get("claimedSha256"), entry.get("claimedBytes")
        if claimed_sha is None and claimed_size is None:
            item["state"] = "unclaimed"
        elif claimed_sha and claimed_sha != digest:
            item["state"] = "mismatch"
        elif claimed_size is not None and claimed_size != len(blob):
            item["state"] = "mismatch"
        else:
            item["state"] = "match"
        results.append(item)
    return results


def summarise(results: list[dict]) -> str:
    counts: dict[str, int] = {}
    for item in results:
        counts[item["state"]] = counts.get(item["state"], 0) + 1
    lines = [
        f"Pinned GitHub locators: {len(results)} "
        + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())),
    ]
    for item in results:
        lines.append(
            f"  {item['state']:12s} {item['repo']}@{item['commit'][:8]} "
            f"{item['path'][:40]} ({item['file']}:{item['line']})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify pinned GitHub locators cited in Markdown")
    parser.add_argument("-o", "--output", help="write the verification report as JSON")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--offline", action="store_true", help="collect claims without fetching")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    entries = collect(root)
    results = verify(entries, offline=args.offline)
    report = {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "snapshotDate": SNAPSHOT_DATE,
        "method": ("gh api contents?ref=<commit> with raw media type; size and SHA-256 recomputed locally; "
                   "claims read from the same line only"),
        "offline": args.offline,
        "totals": {
            "locators": len(results),
            "match": sum(1 for r in results if r["state"] == "match"),
            "mismatch": sum(1 for r in results if r["state"] == "mismatch"),
            "unclaimed": sum(1 for r in results if r["state"] == "unclaimed"),
            "unavailable": sum(1 for r in results if r["state"] == "unavailable"),
            "notChecked": sum(1 for r in results if r["state"] == "not-checked"),
        },
        "limits": [
            "Совпадение хеша доказывает байты объекта на закреплённом коммите, а не прочтение содержания.",
            "Оно не подтверждает, что издание то самое, не даёт прав и не снимает ARCHIVE/LOCATOR_HOLD само по себе.",
            "URL без закреплённого коммита этим инструментом не проверяются: у них нет версии.",
        ],
        "locators": results,
    }
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}")
    if args.summary or not args.output:
        print(summarise(results))
    return 1 if report["totals"]["mismatch"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
