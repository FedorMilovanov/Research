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


class EvidenceListingTests(unittest.TestCase):
    """Every location a closure cites has to be visible; the table is where a reader looks.

    Two silent reductions were found by mutation: showing the first location only, and
    dropping the ``../../`` prefix from a repository path. Neither changed a test result,
    and the second one produces dead links that only the repository-wide audit would see.
    """

    def test_detail_lists_every_location(self) -> None:
        registry = {"closures": [{"id": "HCR-2026-11-18-01", "title": "Ось",
                                  "holdType": "ARCHIVE_HOLD", "method": "raw-download-compare",
                                  "closedScope": "закрыто",
                                  "recordLocations": ["data/a.json", "data/b.json", "docs/c.md"]}]}
        detail = summary.render_detail(registry)
        for path in ("data/a.json", "data/b.json", "docs/c.md"):
            self.assertIn(path, detail, "a cited location may not be dropped from the detail table")

    def test_summary_says_how_many_locations_it_left_out(self) -> None:
        registry = {"closures": [{"id": "HCR-2026-11-18-01", "title": "Ось",
                                  "holdType": "ARCHIVE_HOLD", "method": "raw-download-compare",
                                  "recordLocations": ["data/a.json", "data/b.json", "docs/c.md"]}],
                    "confirmations": [], "notClosed": []}
        block = summary.render(registry)
        self.assertIn("и ещё 1", block)

    def test_place_link_climbs_out_of_docs_research(self) -> None:
        self.assertEqual(summary._place("data/a.json §2"), "[`data/a.json`](../../data/a.json) §2")
        self.assertTrue(summary._place("scripts/tool.py").endswith("](../../scripts/tool.py)"))

    def test_a_truncated_reason_says_so(self) -> None:
        # Cutting the reason at the first full stop is intended; cutting it at 180 characters
        # without a mark is not - the reader cannot tell a short reason from a clipped one.
        long_reason = "Одна причина без точки в конце " * 12 + ". Далее подробности."
        registry = {"closures": [], "confirmations": [],
                    "notClosed": [{"id": "OPEN-RIGHTS", "title": "Права", "reason": long_reason}]}
        block = summary.render(registry)
        self.assertIn("…", block)
        self.assertNotIn("Одна причина без точки в конце " * 12, block)

    def test_missing_policy_marks_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            registry = {"closures": [], "confirmations": [], "notClosed": []}
            block = summary.render(registry, Path(tmp))
            self.assertNotIn("ось реестра", block)


class HoldTypeLabelTests(unittest.TestCase):
    """A HOLD type the evidence policy does not declare must not look like one that it does."""

    def test_non_canonical_type_is_labelled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / summary.POLICY).write_text(json.dumps({"holds": ["ARCHIVE_HOLD"]}), encoding="utf-8")
            registry = {"closures": [
                {"id": "HCR-2026-11-18-01", "title": "а", "holdType": "ARCHIVE_HOLD", "method": "raw-download-compare"},
                {"id": "HCR-2026-11-18-02", "title": "б", "holdType": "TEXT_INTEGRITY_HOLD", "method": "raw-download-compare"}],
                "confirmations": [], "notClosed": []}
            block = summary.render(registry, root)
            line = [l for l in block.splitlines() if l.startswith("Типы HOLD")][0]
            self.assertIn("`TEXT_INTEGRITY_HOLD` — 1 (ось реестра, не флаг политики)", line)
            self.assertIn("`ARCHIVE_HOLD` — 1,", line.replace("`ARCHIVE_HOLD` — 1.", "`ARCHIVE_HOLD` — 1,"))


class MethodNameTests(unittest.TestCase):
    """A method without a Russian name renders as a bare slug, which reads like an omission."""

    def test_every_method_in_the_registry_has_a_name(self) -> None:
        registry = json.loads((Path(__file__).resolve().parents[1] / summary.DEFAULT_REGISTRY)
                              .read_text(encoding="utf-8"))
        missing = sorted({c.get("method") for c in registry["closures"] + registry["confirmations"]
                          if c.get("method") and c["method"] not in summary.METHOD_NAMES})
        self.assertEqual(missing, [], "add a label to METHOD_NAMES")


if __name__ == "__main__":
    unittest.main()
