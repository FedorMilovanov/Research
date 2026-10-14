#!/usr/bin/env python3
"""Sequential fixed-tree NT audit; no implicit fetch, no ignored Genesis FAIL.

Raw logs can contain study-only text: keep them outside Git, never upload
as public CI artifacts. Existing CI coverage is separate from this receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
from nt_sources import ROOT

TOOLS = ROOT / "ИСКУПЛЕНИЕ/nt/tools"
UPPER = ":".join("ИСКУПЛЕНИЕ/" + x for x in ["04_LIMITED_VS_UNIVERSAL_QUESTION_MAP.md",
                 "12_HARD_TEXTS_EXTENT_CARDS.md", "00_README_AND_NAVIGATION.md",
                 "05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md"])


def tree_fingerprint() -> str:
    listing = subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT)
    digest = hashlib.sha256()
    for name in sorted(set(x for x in listing.split(b"\0") if x)):
        path = ROOT / os.fsdecode(name)
        digest.update(name + b"\0")
        if path.is_file():
            digest.update(path.read_bytes())
        else:
            digest.update(b"MISSING")
        digest.update(b"\0")
    return digest.hexdigest()


def commands(nt_only: bool = False, fetch: bool = False) -> list[tuple[str, list[str]]]:
    def tool(name, *args):
        return [sys.executable, str(TOOLS / name), *args]
    checks = []
    if fetch:
        checks.append(("Explicit outside-Git acquisition", tool("nt_sources.py", "--fetch")))
    checks += [("Exact source bytes/names", tool("nt_sources.py")),
               ("Regression tests", [sys.executable, "-m", "unittest", "discover", "-s", str(TOOLS / "tests"), "-p", "test_nt*.py", "-v"]),
               ("Greek citations plus required upper files", tool("verify_nt_citations.py")),
               ("Card inventory and method floor", tool("check_nt_card_discipline.py")),
               ("Derived Greek/MT/LXX facts and states", tool("verify_nt_facts.py")),
               ("S1/TR/S7/S8 variant controls", tool("verify_nt_variants.py")),
               ("MT parsed inventory", tool("mt_lookup.py")),
               ("MT/LXX positive and registered negative pairs", tool("mt_lxx_collation.py")),
               ("Edition apparatus census", tool("sbl_apparatus.py")),
               ("Selected card-heading apparatus sweep", tool("pericope_apparatus_sweep.py", "--check")),
               ("Manuscript census/book/probe controls", tool("manuscript_collation.py", "--check", "--stats"))]
    if not nt_only:
        checks += [(name, [sys.executable, str(ROOT / "scripts" / f"validate_{name}.py")])
                   for name in ("research_root_authority", "repository_authority_integrity", "genesis6_authority_manifest")]
    return checks


def run_checks(checks: list[tuple[str, list[str]]], logs: Path, env: dict,
               immutable: bool = True) -> list[dict]:
    baseline = tree_fingerprint() if immutable else None
    records = []
    for index, (name, argv) in enumerate(checks, 1):
        started = time.monotonic()
        try:
            proc = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True, timeout=180)
            code, output = proc.returncode, proc.stdout + proc.stderr
        except subprocess.TimeoutExpired as exc:
            code = 124
            output = f"FAIL: timeout: {exc}\n"
        except OSError as exc:
            code, output = 1, f"FAIL: process unavailable: {exc}\n"
        changed = immutable and tree_fingerprint() != baseline
        if changed:
            code = 1
            output += "\nFAIL: checked tree mutated during audit; receipt is invalid\n"
        log = logs / f"{index:02d}.log"
        log.write_text(output, encoding="utf-8")
        record = {"name":name, "argv":argv, "rc":code, "seconds":round(time.monotonic()-started,3),
                  "log":str(log), "logSha256":hashlib.sha256(log.read_bytes()).hexdigest()}
        records.append(record)
        print(f"{'PASS' if code == 0 else 'FAIL'} {index:02d} {name} (rc={code})", flush=True)
        if code != 0:
            print(output, flush=True)  # no head/tail/grep masking of failure diagnostics
        (logs / "results.json").write_text(json.dumps(records, ensure_ascii=False, indent=2)+"\n")
        if changed:
            break
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nt-only", action="store_true", help="explicitly omit the three root checks")
    parser.add_argument("--fetch", action="store_true", help="explicit acquisition outside Git before validation")
    parser.add_argument("--logs", type=Path, help="private log directory outside the checkout")
    args = parser.parse_args()
    if args.logs:
        logs = args.logs.resolve()
        if logs == ROOT or ROOT in logs.parents:
            raise ValueError("raw audit logs must stay outside the Research checkout")
        logs.mkdir(parents=True, exist_ok=True)
    else:
        home = Path.home() / ".cache/research-audit"
        home.mkdir(parents=True, exist_ok=True)
        logs = Path(tempfile.mkdtemp(prefix="nt-audit-", dir=home))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", NT_EXTRA_CARDS=UPPER)
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    fingerprint = tree_fingerprint()
    print(f"Audit scope: {'NT only' if args.nt_only else 'NT + three root checks'}; branch={branch}; HEAD={head}")
    print(f"Fixed-tree sha256: {fingerprint}; private raw logs: {logs}")
    checks = commands(args.nt_only, args.fetch)
    records = run_checks(checks, logs, env)
    failures = [x for x in records if x["rc"] != 0]
    receipt = {"scope":"NT" if args.nt_only else "NT + three root checks", "branch":branch, "head":head,
               "checkedTreeSha256":fingerprint, "treeUnchanged":tree_fingerprint()==fingerprint,
               "planned":len(checks), "completed":len(records), "pass":len(records)-len(failures),
               "fail":len(failures), "publicationState":"BLOCKED", "checks":records}
    (logs / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+"\n")
    ok = not failures and len(records)==len(checks) and receipt["treeUnchanged"]
    print(f"{'PASS' if ok else 'FAIL'}: {receipt['pass']}/{len(checks)} checks; tree unchanged={receipt['treeUnchanged']}; publication BLOCKED")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
