#!/usr/bin/env python3
"""Tests for scripts/render_closures_summary.py (offline)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import render_closures_summary as summary

REGISTRY = {
    "closures": [
        {"id": "HCR-2026-11-18-01", "title": "Ось один", "holdType": "ARCHIVE_HOLD",
         "method": "raw-download-compare", "recordLocations": ["data/a.json"]},
        {"id": "HCR-2026-11-18-02", "title": "Ось два", "holdType": "EVIDENCE_HOLD",
         "method": "internal-digest-rehash", "evidence": "data/b.json"},
    ],
    "confirmations": [{"id": "HCR-2026-11-18-C1", "title": "Подтверждение"}],
    "notClosed": [{"id": "OPEN-RIGHTS", "title": "Права",
                   "reason": "Требуют лицензионного решения. Далее подробности."}],
}


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        self.registry = self.root / "registry.json"
        self.registry.write_text(json.dumps(REGISTRY, ensure_ascii=False), encoding="utf-8")
        self.register = self.root / "register.md"
        self.register.write_text(
            "# Реестр\n\n" + summary.BEGIN + "\n" + summary.END + "\n\n"
            + summary.DETAIL_BEGIN + "\n" + summary.DETAIL_END + "\n\n## 1. Дальше\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._dir.cleanup()

    def run_tool(self, *args: str) -> int:
        return summary.main(["--registry", str(self.registry), "--register", str(self.register), *args])

    def test_block_counts_and_rows(self) -> None:
        block = summary.render(REGISTRY)
        self.assertIn("Закрытий: **2**", block)
        self.assertIn("Подтверждений без закрытия: **1**", block)
        self.assertIn("| 01 | Ось один | `ARCHIVE_HOLD`", block)
        self.assertIn("скачивание и пересчёт байтов", block)

    def test_detail_block_lists_every_closure(self) -> None:
        detail = summary.render_detail(REGISTRY)
        self.assertIn("| `HCR-2026-11-18-01` |", detail)
        self.assertIn("| `HCR-2026-11-18-02` |", detail)

    def test_missing_detail_markers_fail_loudly(self) -> None:
        self.register.write_text("# Реестр\n\n" + summary.BEGIN + "\n" + summary.END + "\n",
                                 encoding="utf-8")
        self.assertEqual(self.run_tool("--check"), 1)

    def test_open_items_are_listed(self) -> None:
        block = summary.render(REGISTRY)
        self.assertIn("Осталось открытым по существу", block)
        self.assertIn("`OPEN-RIGHTS` — Права. Требуют лицензионного решения.", block)

    def test_open_item_is_rendered_by_id_not_by_sentence(self) -> None:
        # The old renderer printed the item's class text as its identity; that text carried
        # two measurements which then travelled unchecked into the generated map.
        registry = {"closures": [], "confirmations": [], "notClosed": [
            {"id": "OPEN-X", "title": "Ось без чисел", "class": "Ось (134 значения)",
             "reason": "Причина."}]}
        block = summary.render(registry)
        self.assertIn("`OPEN-X` — Ось без чисел.", block)
        self.assertNotIn("134", block)

    def test_write_then_check_passes(self) -> None:
        self.assertEqual(self.run_tool("--write"), 0)
        self.assertEqual(self.run_tool("--check"), 0)

    def test_check_fails_when_register_drifts(self) -> None:
        self.assertEqual(self.run_tool("--write"), 0)
        text = self.register.read_text(encoding="utf-8").replace("Закрытий: **2**", "Закрытий: **3**")
        self.register.write_text(text, encoding="utf-8")
        self.assertEqual(self.run_tool("--check"), 1)

    def test_missing_markers_fail(self) -> None:
        self.register.write_text("# Реестр без маркеров\n", encoding="utf-8")
        self.assertEqual(self.run_tool("--write"), 1)

    def test_markers_survive_the_rewrite(self) -> None:
        self.run_tool("--write")
        text = self.register.read_text(encoding="utf-8")
        self.assertEqual(text.count(summary.BEGIN), 1)
        self.assertEqual(text.count(summary.END), 1)
        self.assertIn("## 1. Дальше", text)


if __name__ == "__main__":
    unittest.main()


class ConfirmationCounterTests(unittest.TestCase):
    """A confirmation's numbers must come from an artefact, not from its own title."""

    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        (self.root / "data").mkdir()
        (self.root / "data" / "report.json").write_text(
            json.dumps({"totals": {"locators": 1234, "match": 4}}), encoding="utf-8")
        self.registry = self.root / "registry.json"
        self.register = self.root / "register.md"
        self.register.write_text("# Реестр\n\n" + summary.BEGIN + "\n" + summary.END + "\n"
                                 + summary.DETAIL_BEGIN + "\n" + summary.DETAIL_END + "\n",
                                 encoding="utf-8")

    def tearDown(self) -> None:
        self._dir.cleanup()

    def registry_with(self, counters: list[dict]) -> dict:
        return {"closures": [], "notClosed": [], "confirmations": [
            {"id": "HCR-C9", "title": "Подтверждение без чисел", "counters": counters}]}

    def run_tool(self, *args: str) -> int:
        return summary.main(["--registry", str(self.registry), "--register", str(self.register),
                             "--root", str(self.root), *args])

    def test_counter_is_read_from_the_artefact(self) -> None:
        registry = self.registry_with([{"label": "локаторов", "artefact": "data/report.json",
                                        "field": "totals.locators"}])
        block = summary.render(registry, self.root)
        self.assertIn("(локаторов: 1\u2009234)", block)

    def test_write_and_check_agree_with_counters(self) -> None:
        self.registry.write_text(json.dumps(self.registry_with([
            {"label": "локаторов", "artefact": "data/report.json", "field": "totals.locators"}])),
            encoding="utf-8")
        self.assertEqual(self.run_tool("--write"), 0)
        self.assertEqual(self.run_tool("--check"), 0)

    def test_artifact_change_makes_the_block_stale(self) -> None:
        self.registry.write_text(json.dumps(self.registry_with([
            {"label": "локаторов", "artefact": "data/report.json", "field": "totals.locators"}])),
            encoding="utf-8")
        self.assertEqual(self.run_tool("--write"), 0)
        (self.root / "data" / "report.json").write_text(
            json.dumps({"totals": {"locators": 9, "match": 4}}), encoding="utf-8")
        self.assertEqual(self.run_tool("--check"), 1)

    def test_missing_artefact_fails_loudly(self) -> None:
        self.registry.write_text(json.dumps(self.registry_with([
            {"label": "локаторов", "artefact": "data/absent.json", "field": "totals.locators"}])),
            encoding="utf-8")
        self.assertEqual(self.run_tool("--check"), 2)

    def test_counter_without_a_field_fails_loudly(self) -> None:
        self.registry.write_text(json.dumps(self.registry_with([{"label": "локаторов"}])), encoding="utf-8")
        self.assertEqual(self.run_tool("--check"), 2)

    def test_non_numeric_field_fails_loudly(self) -> None:
        (self.root / "data" / "report.json").write_text(
            json.dumps({"totals": {"locators": "много"}}), encoding="utf-8")
        self.registry.write_text(json.dumps(self.registry_with([
            {"label": "локаторов", "artefact": "data/report.json", "field": "totals.locators"}])),
            encoding="utf-8")
        self.assertEqual(self.run_tool("--check"), 2)


if __name__ == "__main__":
    unittest.main()
