#!/usr/bin/env python3
"""Tests for the branch-head snapshot freshness gate."""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import check_snapshot_freshness as freshness


class DifferenceTests(unittest.TestCase):
    def test_equal_structures_have_no_difference(self) -> None:
        self.assertIsNone(freshness.first_difference({"a": [1, 2]}, {"a": [1, 2]}))

    def test_value_difference_names_its_json_path(self) -> None:
        self.assertEqual(freshness.first_difference({"a": [1, 2]}, {"a": [1, 3]}),
                         "$.a[1]: 2 != 3")

    def test_missing_key_is_not_smoothed_over(self) -> None:
        self.assertEqual(freshness.first_difference({"a": 1}, {}), "$: missing key 'a'")


class CheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "data").mkdir()
        # The pinned-locator half of check() is deliberately independent of SnapshotSpec.
        # Make it an empty, internally consistent report for these offline unit tests.
        self.pinned_path = self.root / "data" / "pinned-github-locators-verified-2026-11-18.json"
        self.pinned_path.write_text(json.dumps({"locators": []}), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def spec(self, build):
        path = self.root / "data" / "report.json"
        path.write_text(json.dumps({"count": 2}), encoding="utf-8")
        return (freshness.SnapshotSpec("probe", "data/report.json", build),)

    def test_current_snapshot_passes(self) -> None:
        problems = freshness.check(self.root, self.spec(lambda _root, committed: committed))
        self.assertEqual(problems, [])

    def test_stale_snapshot_fails_with_a_field(self) -> None:
        problems = freshness.check(self.root, self.spec(lambda _root, _committed: {"count": 3}))
        self.assertEqual(problems, ["probe: stale ($.count: 2 != 3)"])

    def test_missing_snapshot_fails(self) -> None:
        spec = (freshness.SnapshotSpec("probe", "data/absent.json", lambda _r, _c: {}),)
        self.assertEqual(freshness.check(self.root, spec), ["probe: missing data/absent.json"])

    def test_cli_check_returns_one_for_stale_tree(self) -> None:
        # A bare fixture has none of the six reports; --check must therefore be a gate,
        # while the default command is allowed to be report-only for local inspection.
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(freshness.main(["--root", str(self.root), "--check"]), 1)
            self.assertEqual(freshness.main(["--root", str(self.root)]), 0)


if __name__ == "__main__":
    unittest.main()
