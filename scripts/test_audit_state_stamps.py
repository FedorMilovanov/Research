#!/usr/bin/env python3
"""Tests for scripts/audit_state_stamps.py (offline; Git history is injected)."""
from __future__ import annotations

import datetime
import json
import tempfile
import unittest
from pathlib import Path

import audit_state_stamps as stamps

TODAY = datetime.date(2026, 11, 18)


class Fixture:
    def __init__(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def close(self) -> None:
        self._dir.cleanup()


def history(last: str | None, subject: str = "edit", added: str | None = None):
    def lookup(path: Path, root: Path) -> dict:
        return {"lastCommit": last, "lastSubject": subject, "addedCommit": added or last}
    return lookup


class StampTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def audit(self, last: str | None, **kwargs) -> dict:
        return stamps.audit(self.fx.root, today=TODAY, history_lookup=history(last), **kwargs)

    def test_current_stamp(self) -> None:
        self.fx.write("a/doc.md", "**Обновлено: 2026-11-13**\n\nbody\n")
        report = self.audit("2026-11-13")
        self.assertEqual(report["findings"][0]["state"], "current")

    def test_edited_after_stamp(self) -> None:
        self.fx.write("a/doc.md", "> **Updated:** 2026-11-13\n\nbody\n")
        report = self.audit("2026-11-15")
        self.assertEqual(report["findings"][0]["state"], "edited-after-stamp")
        self.assertEqual(report["findings"][0]["stamp"], "2026-11-13")

    def test_stamp_ahead_of_history(self) -> None:
        self.fx.write("a/doc.md", "**Обновлено 03.11.2026**\n")
        report = self.audit("2026-11-02")
        self.assertEqual(report["findings"][0]["state"], "stamp-ahead-of-history")

    def test_stamp_in_future_is_impossible_and_fails_check(self) -> None:
        self.fx.write("a/doc.md", "**As of:** 2026-12-31\n")
        out = self.fx.root / "r.json"
        code = stamps.main(["--root", str(self.fx.root), "-o", str(out), "--check"])
        # --check uses the real clock; the stub history is only used inside audit()
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertIn(report["findings"][0]["state"], {"stamp-in-future"})
        self.assertEqual(code, 1)

    def test_table_rows_and_urls_are_not_self_stamps(self) -> None:
        self.fx.write("a/batch.md",
                      "| row | policy, last updated 2026-05-17 | FULL_OBJECT |\n"
                      "> see https://example.org docs, updated 2026-01-01\n"
                      "body\n")
        report = self.audit("2026-11-16")
        self.assertEqual(report["totals"]["stamped"], 0)

    def test_both_date_formats(self) -> None:
        self.fx.write("a/dots.md", "**Обновлено: 13.11.2026**\n")
        self.fx.write("b/dashes.md", "**Обновлено: 2026-11-13**\n")
        report = self.audit("2026-11-13")
        self.assertEqual(sorted(f["stamp"] for f in report["findings"]),
                         ["2026-11-13", "2026-11-13"])

    def test_stamp_only_inside_head(self) -> None:
        self.fx.write("a/late.md", "\n" * 20 + "**Обновлено: 2026-11-13**\n")
        report = self.audit("2026-11-13")
        self.assertEqual(report["totals"]["stamped"], 0)

    def test_report_schema_and_scope(self) -> None:
        self.fx.write("a/doc.md", "**Обновлено: 2026-11-13**\n")
        report = self.audit("2026-11-13")
        self.assertEqual(report["schemaVersion"], stamps.SCHEMA_VERSION)
        self.assertEqual(report["authorityId"], stamps.AUTHORITY_ID)
        self.assertEqual(report["scope"]["today"], TODAY.isoformat())
        self.assertIn("byState", report["totals"])


if __name__ == "__main__":
    unittest.main()
