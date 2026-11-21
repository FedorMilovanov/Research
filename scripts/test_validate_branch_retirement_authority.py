#!/usr/bin/env python3
"""Offline CLI regressions for the retirement validator, with every Git call mocked.

The dated authority is a test input, never rewritten. These tests fix diagnosis,
not the authority's remote-ref policy or the live repository's retirement state.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
from pathlib import Path
import runpy
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_branch_retirement_authority.py"
AUTH_REL = Path("data/branch-retirement-authority-2026-08-02.json")
HUMAN_REL = Path("archive-ledgers/CURRENT_BRANCH_RETIREMENT_AUTHORITY_2026-08-02.md")
AUTHORITY = json.loads((ROOT / AUTH_REL).read_text(encoding="utf-8"))
ARCHIVE = AUTHORITY["forensicArchive"]
ARCHIVE_REF = "refs/remotes/origin/" + ARCHIVE["branch"]
TESTED_MAIN = AUTHORITY["testedMainBeforeReceipt"]
TESTED_OBJECT = TESTED_MAIN + "^{commit}"
LEDGERS = ARCHIVE["uniqueLedgerFiles"]
OBJECTS = [TESTED_OBJECT] + [ARCHIVE_REF + ":" + p for p in LEDGERS]


class RetirementValidatorTests(unittest.TestCase):
    def run_validator(
        self, *, extra_refs=(), archive_head=None, missing_objects=(),
        fail_command=None, merge_base=None, ahead="50", behind="138",
        authority=None, human=None,
    ):
        refs = {"main": TESTED_MAIN, ARCHIVE["branch"]: archive_head or ARCHIVE["headSha"]}
        refs.update({name: TESTED_MAIN for name in extra_refs})
        missing = set(missing_objects)
        calls = []
        stdout, stderr = io.StringIO(), io.StringIO()
        real_read_text = Path.read_text
        machine = copy.deepcopy(AUTHORITY if authority is None else authority)

        def read_text(path, *args, **kwargs):
            if path == ROOT / AUTH_REL:
                return json.dumps(machine)
            if path == ROOT / HUMAN_REL and human is not None:
                return human
            return real_read_text(path, *args, **kwargs)

        def run_git(argv, *args, **kwargs):
            self.assertFalse(args)
            self.assertEqual(argv[0], "git")
            self.assertEqual(Path(kwargs["cwd"]), ROOT)
            self.assertIs(kwargs["text"], True)
            self.assertEqual(kwargs["stdout"], subprocess.PIPE)
            self.assertEqual(kwargs["stderr"], subprocess.STDOUT)
            cmd = tuple(argv[1:])
            calls.append(cmd)
            rc = 0
            if fail_command is not None and cmd == fail_command:
                rc, output = 128, "fatal: simulated command failure\n"
            elif cmd == ("ls-remote", "--heads", "origin"):
                output = "".join(f"{sha}\trefs/heads/{ref}\n" for ref, sha in sorted(refs.items()))
            elif cmd == ("fetch", "origin", "+refs/heads/" + ARCHIVE["branch"] + ":" + ARCHIVE_REF):
                output = ""
            elif len(cmd) == 3 and cmd[:2] == ("cat-file", "-e"):
                self.assertIn(cmd[2], OBJECTS)
                rc = 128 if cmd[2] in missing else 0
                output = "fatal: simulated missing object\n" if rc else ""
            elif cmd == ("merge-base", TESTED_MAIN, ARCHIVE_REF):
                output = (ARCHIVE["mergeBaseWithMain"] if merge_base is None else merge_base) + "\n"
            elif cmd == ("rev-list", "--count", TESTED_MAIN + ".." + ARCHIVE_REF):
                output = ahead + "\n"
            elif cmd == ("rev-list", "--count", ARCHIVE_REF + ".." + TESTED_MAIN):
                output = behind + "\n"
            else:
                self.fail(f"Unexpected Git command (no remote writer is allowed): {cmd}")
            # Faithful for both subprocess.run and the old check_output wrapper:
            # check_output delegates to run(check=True), which must raise on error.
            if rc and kwargs.get("check"):
                raise subprocess.CalledProcessError(rc, argv, output=output)
            return subprocess.CompletedProcess(argv, rc, stdout=output)

        code = 0
        with patch.object(Path, "read_text", read_text), patch.object(subprocess, "run", run_git):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                try:
                    runpy.run_path(str(VALIDATOR), run_name="__main__")
                except SystemExit as exc:
                    code = exc.code
        return code, stdout.getvalue(), stderr.getvalue(), calls

    def assert_objects_checked(self, calls):
        self.assertEqual([c[2] for c in calls if c[:2] == ("cat-file", "-e")], OBJECTS)

    def assert_no_invented_missing_objects(self, stderr):
        self.assertNotIn("recorded tested main commit unavailable", stderr)
        self.assertNotIn("archive ledger missing:", stderr)

    def test_clean_receipt_accepts_empty_stdout_for_all_seven_objects(self):
        code, out, err, calls = self.run_validator()
        self.assertEqual(code, 0, err)
        self.assertIn("Branch retirement authority: PASS", out)
        self.assertEqual(err, "")
        self.assert_objects_checked(calls)

    def test_unrelated_live_branch_drift_does_not_invent_missing_objects(self):
        code, out, err, calls = self.run_validator(extra_refs=("test/unrelated-active",))
        self.assertEqual(code, 1)
        self.assertNotIn("PASS", out)
        self.assertIn("FAIL (1)", err)
        self.assertIn("remote branch set drift", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_forensic_head_drift_does_not_invent_missing_objects(self):
        code, _, err, calls = self.run_validator(archive_head=TESTED_MAIN)
        self.assertEqual(code, 1)
        self.assertIn("FAIL (1)", err)
        self.assertIn("remote forensic archive head drift", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_two_real_drifts_remain_two_not_nine(self):
        code, _, err, calls = self.run_validator(
            extra_refs=("test/unrelated-active",), archive_head=TESTED_MAIN,
        )
        self.assertEqual(code, 1)
        self.assertIn("FAIL (2)", err)
        self.assertIn("remote branch set drift", err)
        self.assertIn("remote forensic archive head drift", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_missing_tested_main_uses_exit_code_and_does_not_poison_ledger_checks(self):
        code, _, err, calls = self.run_validator(missing_objects=(TESTED_OBJECT,))
        self.assertEqual(code, 1)
        self.assertIn("recorded tested main commit unavailable", err)
        self.assertIn("git cat-file -e", err)
        self.assertNotIn("archive ledger missing:", err)
        self.assert_objects_checked(calls)

    def test_each_missing_ledger_is_reported_without_inventing_other_missing_files(self):
        for path in LEDGERS:
            with self.subTest(path=path):
                code, _, err, calls = self.run_validator(
                    extra_refs=("test/unrelated-active",),
                    missing_objects=(ARCHIVE_REF + ":" + path,),
                )
                self.assertEqual(code, 1)
                self.assertIn("archive ledger missing: " + path, err)
                self.assertNotIn("recorded tested main commit unavailable", err)
                for other in LEDGERS:
                    if other != path:
                        self.assertNotIn("archive ledger missing: " + other, err)
                self.assert_objects_checked(calls)

    def test_multiple_real_missing_objects_are_all_reported(self):
        absent = [TESTED_OBJECT, ARCHIVE_REF + ":" + LEDGERS[-1]]
        code, _, err, calls = self.run_validator(missing_objects=absent)
        self.assertEqual(code, 1)
        self.assertIn("recorded tested main commit unavailable", err)
        self.assertIn("archive ledger missing: " + LEDGERS[-1], err)
        self.assertEqual(err.count("archive ledger missing:"), 1)
        self.assert_objects_checked(calls)

    def test_ls_remote_failure_remains_fail_closed(self):
        code, _, err, calls = self.run_validator(fail_command=("ls-remote", "--heads", "origin"))
        self.assertEqual(code, 1)
        self.assertIn("git ls-remote --heads origin failed:", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_fetch_failure_is_not_hidden_but_existing_local_objects_stay_available(self):
        cmd = ("fetch", "origin", "+refs/heads/" + ARCHIVE["branch"] + ":" + ARCHIVE_REF)
        code, _, err, calls = self.run_validator(fail_command=cmd)
        self.assertEqual(code, 1)
        self.assertIn("FAIL (1)", err)
        self.assertIn("git fetch origin", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_reappearing_retired_ref_still_fails(self):
        retired = AUTHORITY["retiredRefs"][0]
        code, _, err, calls = self.run_validator(extra_refs=(retired,))
        self.assertEqual(code, 1)
        self.assertIn("one or more retired refs reappeared", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_merge_base_drift_still_fails(self):
        code, _, err, _ = self.run_validator(merge_base=TESTED_MAIN)
        self.assertEqual(code, 1)
        self.assertIn("recorded merge base no longer reproduces", err)

    def test_historical_unique_counts_still_fail_closed(self):
        for kwargs, expected in [
            ({"ahead": "49"}, "archive unique commits at receipt no longer reproduce"),
            ({"behind": "139"}, "main unique commits at receipt no longer reproduce"),
        ]:
            with self.subTest(kwargs=kwargs):
                code, _, err, _ = self.run_validator(**kwargs)
                self.assertEqual(code, 1)
                self.assertIn(expected, err)

    def test_machine_authority_checks_are_not_bypassed(self):
        authority = copy.deepcopy(AUTHORITY)
        authority["verification"]["allEightPassedPreDeleteRule"] = False
        code, _, err, calls = self.run_validator(authority=authority)
        self.assertEqual(code, 1)
        self.assertIn("ancestry proof marker lost", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_human_authority_checks_are_not_bypassed(self):
        code, _, err, calls = self.run_validator(human="not a valid authority receipt\n")
        self.assertEqual(code, 1)
        self.assertIn("human authority marker missing:", err)
        self.assert_no_invented_missing_objects(err)
        self.assert_objects_checked(calls)

    def test_git_commands_never_write_or_delete_remote_branches(self):
        _, _, _, calls = self.run_validator()
        allowed = {"ls-remote", "fetch", "cat-file", "merge-base", "rev-list"}
        self.assertTrue(all(c[0] in allowed for c in calls))
        self.assertEqual([c for c in calls if c[0] == "fetch"], [
            ("fetch", "origin", "+refs/heads/" + ARCHIVE["branch"] + ":" + ARCHIVE_REF),
        ])


if __name__ == "__main__":
    unittest.main()
