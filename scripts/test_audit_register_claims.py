#!/usr/bin/env python3
"""Tests for scripts/audit_register_claims.py (offline)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import audit_register_claims as claims


class Fixture:
    def __init__(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        self.write_json(claims.INVENTORY, {"totals": {"filesScanned": 10, "mentions": {"LOCATOR_HOLD": 4}},
                                           "byCorpus": {"docs": {"files": 3, "mentions": {"LOCATOR_HOLD": 4}}}})
        self.write_json(claims.DIGESTS, {"totals": {"byState": {"match": 58, "stale": 27},
                                                    "unclaimedByReason": {"bare-hash": 141}}})
        self.register = self.root / claims.REGISTER
        self.register.parent.mkdir(parents=True, exist_ok=True)

    def write_json(self, rel: str, payload: dict) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def write_register(self, text: str) -> None:
        self.register.write_text(text, encoding="utf-8")

    def close(self) -> None:
        self._dir.cleanup()


class ClaimTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def report(self) -> dict:
        return claims.audit(self.fx.root)

    def finding(self, report: dict, label: str) -> dict:
        return next(f for f in report["findings"] if f["label"] == label)

    def test_matching_counter(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 10 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "match")

    def test_stale_counter_reports_both_numbers(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 9 |\n")
        entry = self.finding(self.report(), "просканировано текстовых файлов")
        self.assertEqual(entry["state"], "stale")
        self.assertEqual((entry["claimed"], entry["actual"]), (9, 10))

    def test_missing_anchor_is_reported_not_skipped(self) -> None:
        self.fx.write_register("| что-то другое | 10 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "anchor-missing")

    def test_missing_artefact(self) -> None:
        (self.fx.root / claims.DIGESTS).unlink()
        self.fx.write_register("| просканировано текстовых файлов | 10 |\n")
        self.assertEqual(self.finding(self.report(), "`match`")["state"], "source-missing")

    def test_conflicting_numbers_for_one_label(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 10 |\n| просканировано текстовых файлов | 11 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "anchor-ambiguous")

    def test_thin_spaces_in_numbers_are_ignored(self) -> None:
        self.fx.write_json(claims.INVENTORY, {"totals": {"filesScanned": 3110}, "byCorpus": {}})
        self.fx.write_register("| просканировано текстовых файлов | 3\u2009110 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "match")

    def test_check_exits_non_zero_on_drift(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 9 |\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--check"]), 1)

    def test_corpus_table_drift_is_detected(self) -> None:
        self.fx.write_register(claims.CORPUS_BEGIN + "\n| stale |\n" + claims.CORPUS_END + "\n")
        self.assertEqual(self.report()["corpusTable"], "stale")

    def test_corpus_table_without_markers_is_reported(self) -> None:
        self.fx.write_register("## 2.1 без таблицы\n")
        self.assertEqual(self.report()["corpusTable"], "anchor-missing")

    def test_write_corpus_table_makes_the_block_match(self) -> None:
        self.fx.write_register("## 2.1\n" + claims.CORPUS_BEGIN + "\n" + claims.CORPUS_END + "\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--write-corpus-table"]), 0)
        text = self.fx.register.read_text(encoding="utf-8")
        self.assertIn("| `docs/` | 3 | 4 |", text)
        self.assertEqual(self.report()["corpusTable"], "match")


    def test_slice_table_is_generated_from_the_inventory(self) -> None:
        self.fx.write_register("## 2\n" + claims.SLICE_BEGIN + "\n" + claims.SLICE_END + "\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--write-slice-table"]), 0)
        text = self.fx.register.read_text(encoding="utf-8")
        self.assertIn("| просканировано текстовых файлов | 10 |", text)
        self.assertEqual(self.report()["sliceTable"], "match")

    def test_slice_drift_is_detected(self) -> None:
        self.fx.write_register(claims.SLICE_BEGIN + "\n| 3 110 |\n" + claims.SLICE_END + "\n")
        self.assertEqual(self.report()["sliceTable"], "stale")

    def test_thin_space_separator_does_not_touch_label_text(self) -> None:
        self.fx.write_json(claims.INVENTORY, {"totals": {"filesScanned": 3112}, "byCorpus": {}})
        block = claims.render_slice_table({"totals": {"filesScanned": 3112}})
        self.assertIn("3\u2009112", block)
        self.assertIn("| просканировано текстовых файлов |", block)

if __name__ == "__main__":
    unittest.main()
