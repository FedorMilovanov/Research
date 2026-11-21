#!/usr/bin/env python3
"""Offline regression tests for the shallow-clone recovery note."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "research" / "arena" / "SANDBOX_SHALLOW_CLONE_RECOVERY_2026-11-18.md"
BRANCH = "arena/recovery-fixture"


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "Recovery Fixture",
            "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Recovery Fixture",
            "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            "GIT_CONFIG_NOSYSTEM": "1",
        }
    )
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


class RecoveryNoteContractTests(unittest.TestCase):
    def test_note_uses_an_explicit_remote_tracking_refspec(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn(
            '"refs/heads/$branch:refs/remotes/origin/$branch"',
            text,
        )
        self.assertIn('git reset --mixed "$target"', text)
        self.assertIn("git diff --binary HEAD", text)

    def test_executable_section_contains_no_destructive_checkout(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        procedure = text.split("## 3. Безопасная процедура", 1)[1].split(
            "## 4. Проверка результата", 1
        )[0]
        for forbidden in ("reset --hard", "checkout -f", "git clean", "git switch"):
            self.assertNotIn(forbidden, procedure)


class FreshShallowCloneFixtureTests(unittest.TestCase):
    def test_explicit_fetch_and_mixed_reset_preserve_only_real_local_edit(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw)
            source = temp / "source"
            remote = temp / "remote.git"
            work = temp / "work"

            source.mkdir()
            git(source, "init", "--initial-branch=main")
            git(source, "config", "user.name", "Recovery Fixture")
            git(source, "config", "user.email", "fixture@example.invalid")
            (source / "base.txt").write_text("base\n", encoding="utf-8")
            git(source, "add", "base.txt")
            git(source, "commit", "-m", "base")

            git(temp, "init", "--bare", str(remote))
            git(source, "remote", "add", "origin", remote.as_uri())
            git(source, "push", "-u", "origin", "main")

            git(source, "switch", "-c", BRANCH)
            (source / "base.txt").write_text("branch version\n", encoding="utf-8")
            (source / "branch.txt").write_text("remote branch file\n", encoding="utf-8")
            git(source, "add", "base.txt", "branch.txt")
            git(source, "commit", "-m", "remote branch tip")
            remote_tip = git(source, "rev-parse", "HEAD").stdout.strip()
            git(source, "push", "-u", "origin", BRANCH)

            git(
                temp,
                "clone",
                "--depth",
                "1",
                "--single-branch",
                "--branch",
                "main",
                remote.as_uri(),
                str(work),
            )
            self.assertEqual(
                git(work, "rev-parse", "--is-shallow-repository").stdout.strip(),
                "true",
            )

            # Reproduce the observed split state: the branch-tip bytes are in the
            # working tree while .git still points at a depth-1 base checkout.
            git(work, "branch", "-m", BRANCH)
            (work / "base.txt").write_text("branch version\n", encoding="utf-8")
            (work / "branch.txt").write_text(
                "remote branch file\nlocal edit\n", encoding="utf-8"
            )

            git(work, "fetch", "--unshallow", "origin")
            git(
                work,
                "fetch",
                "origin",
                f"refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}",
            )
            target = git(
                work,
                "rev-parse",
                "--verify",
                f"refs/remotes/origin/{BRANCH}^{{commit}}",
            ).stdout.strip()
            git(work, "reset", "--mixed", target)

            self.assertEqual(target, remote_tip)
            self.assertEqual(git(work, "rev-parse", "HEAD").stdout.strip(), remote_tip)
            self.assertEqual(
                git(work, "rev-parse", "--is-shallow-repository").stdout.strip(),
                "false",
            )
            self.assertEqual(git(work, "status", "--porcelain=v1").stdout, " M branch.txt\n")
            self.assertEqual(
                (work / "branch.txt").read_text(encoding="utf-8"),
                "remote branch file\nlocal edit\n",
            )
            git(work, "diff", "--cached", "--exit-code")


if __name__ == "__main__":
    unittest.main()
