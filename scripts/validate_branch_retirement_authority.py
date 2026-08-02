#!/usr/bin/env python3
"""Fail-closed remote-branch and forensic-archive authority validator."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/branch-retirement-authority-2026-08-02.json"
HUMAN = ROOT / "archive-ledgers/CURRENT_BRANCH_RETIREMENT_AUTHORITY_2026-08-02.md"
RETIRED = {
    "agent/osk-source-authority-20260801",
    "agent/osk-wave2-money-power-20260801",
    "agent/osk-wave5-adelaja-20260801",
    "archive/poet-portrait-review-refresh-20260731",
    "archive/second-editorial-40-pdf-refresh-20260731",
    "arena/019fb9cf-research",
    "docs/source-library-94-collections-navigation-2026-07-30",
    "tmp-do-not-use",
}
EXPECTED_VISIBLE = {"main", "archive/legacy-diverged-heads-20260801"}
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as exc:
        errors.append(f"git {' '.join(args)} failed: {exc.output.strip()}")
        return ""


require(AUTH.is_file(), "machine authority missing")
require(HUMAN.is_file(), "human authority missing")
try:
    authority = json.loads(AUTH.read_text(encoding="utf-8"))
except Exception as exc:
    authority = {}
    errors.append(f"invalid authority JSON: {exc}")

require(authority.get("schemaVersion") == 1, "schemaVersion drift")
require(authority.get("authorityId") == "RESEARCH-BRANCH-RETIREMENT-AUTHORITY-2026-08-02", "authorityId drift")
require(authority.get("status") == "ABSORBED_REFS_RETIRED_FORENSIC_ARCHIVE_RETAINED", "status drift")
require(set(authority.get("retiredRefs", [])) == RETIRED, "retired ref set drift")
require(authority.get("retiredCount") == 8, "retiredCount drift")
require(set(authority.get("postRetirementVisibleRefs", [])) == EXPECTED_VISIBLE, "expected visible ref set drift")
verification = authority.get("verification", {})
require(verification.get("preDeleteRule") == "DELETE_ONLY_AFTER_HEAD_IS_ANCESTOR_OF_FRESH_ORIGIN_MAIN_AND_AHEAD_COUNT_EQUALS_ZERO", "pre-delete rule drift")
require(verification.get("allEightPassedPreDeleteRule") is True, "ancestry proof marker lost")
require(verification.get("postDeleteRefSearchConfirmedAbsent") is True, "post-delete confirmation marker lost")
require(verification.get("deletedHeadShasPersisted") is False, "receipt must not invent deleted head SHAs")
require(verification.get("workflowRemovedAfterOneTimeUse") is True, "one-time writer removal marker lost")
require("not reconstructed" in str(verification.get("deletedHeadShaLimitation", "")), "deleted-head limitation missing")

archive = authority.get("forensicArchive", {})
require(archive.get("branch") == "archive/legacy-diverged-heads-20260801", "archive branch drift")
require(archive.get("headSha") == "979fdc748c5f7097618c126eb75176152ac98d69", "archive head drift")
require(archive.get("mergeBaseWithMain") == "f50b21ad6af5dd7aaa53c5be381929b353b26d58", "archive merge-base drift")
require(archive.get("aheadOfMainAtReceipt") == 50, "recorded archive unique-count drift")
require(archive.get("behindMainAtReceipt") == 138, "recorded main unique-count drift")
require(archive.get("status") == "RETAIN_FORENSIC_HISTORY_NOT_CURRENT_AUTHORITY", "archive status drift")
require(archive.get("currentAuthority") is False, "archive must not become current authority")
require(archive.get("mayBeDeleted") is False, "archive deletion must remain forbidden")
require(len(archive.get("uniqueLedgerFiles", [])) == 6, "archive ledger inventory drift")
require(not (ROOT / ".github/workflows/retire-absorbed-branches.yml").exists(), "one-time branch writer still exists")

remote_lines = git("ls-remote", "--heads", "origin").splitlines()
remote_refs: dict[str, str] = {}
for line in remote_lines:
    if not line.strip():
        continue
    sha, ref = line.split("\t", 1)
    if ref.startswith("refs/heads/"):
        remote_refs[ref.removeprefix("refs/heads/")] = sha
require(set(remote_refs) == EXPECTED_VISIBLE, f"remote branch set drift: {sorted(remote_refs)}")
require(RETIRED.isdisjoint(remote_refs), "one or more retired refs reappeared")
require(remote_refs.get(archive.get("branch")) == archive.get("headSha"), "remote forensic archive head drift")

archive_ref = "refs/remotes/origin/archive/legacy-diverged-heads-20260801"
git("fetch", "origin", "+refs/heads/archive/legacy-diverged-heads-20260801:" + archive_ref)
tested_main = authority.get("testedMainBeforeReceipt", "")
require(bool(git("cat-file", "-e", f"{tested_main}^{{commit}}")) or not errors, "recorded tested main commit unavailable")
require(git("merge-base", tested_main, archive_ref) == archive.get("mergeBaseWithMain"), "recorded merge base no longer reproduces")
require(git("rev-list", "--count", f"{tested_main}..{archive_ref}") == "50", "archive unique commits at receipt no longer reproduce")
require(git("rev-list", "--count", f"{archive_ref}..{tested_main}") == "138", "main unique commits at receipt no longer reproduce")
for relative in archive.get("uniqueLedgerFiles", []):
    require(bool(git("cat-file", "-e", f"{archive_ref}:{relative}")) or not errors, f"archive ledger missing: {relative}")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.exists() else ""
for marker in (
    "RESEARCH-BRANCH-RETIREMENT-AUTHORITY-2026-08-02",
    "ABSORBED REFS RETIRED: 8",
    "FORENSIC ARCHIVE IS CURRENT AUTHORITY: NO",
    "DELETED HEAD SHAS PERSISTED: NO",
    "ONE-TIME BRANCH WRITER: REMOVED",
):
    require(marker in human, f"human authority marker missing: {marker}")

if errors:
    print(f"Branch retirement authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Branch retirement authority: PASS — 8 absorbed refs absent, main + forensic archive only, 50 unique archive commits retained")
