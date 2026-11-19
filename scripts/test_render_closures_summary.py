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
    "notClosed": [{"class": "Права", "reason": "Требуют лицензионного решения. Далее подробности."}],
}


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        self.registry = self.root / "registry.json"
        self.registry.write_text(json.dumps(REGISTRY, ensure_ascii=False), encoding="utf-8")
        self.register = self.root / "register.md"
        self.register.write_text(
            "# Реестр\n\n" + summary.BEGIN + "\n" + summary.END + "\n\n## 1. Дальше\n",
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

    def test_open_items_are_listed(self) -> None:
        block = summary.render(REGISTRY)
        self.assertIn("Осталось открытым по существу", block)
        self.assertIn("Права — Требуют лицензионного решения.", block)

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
