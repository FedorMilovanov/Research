#!/usr/bin/env python3
"""Tests for scripts/audit_document_twins.py (offline, no network)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import audit_document_twins as twins

BODY = "one two three four five six seven eight nine ten " * 6
OTHER = "alpha beta gamma delta epsilon zeta eta theta iota kappa " * 6


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


class TwinTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def audit(self, **kwargs) -> dict:
        return twins.audit(self.fx.root, min_words=5, **kwargs)

    def test_identical_text_is_found(self) -> None:
        self.fx.write("a/08_doc.md", BODY)
        self.fx.write("a/27_doc_2026-08-09.md", BODY)
        report = self.audit()
        self.assertEqual(report["totals"]["byState"].get("identical-text"), 1)
        self.assertTrue(report["findings"][0]["sameBytes"])

    def test_unrelated_documents_are_not_paired(self) -> None:
        self.fx.write("a/one.md", BODY)
        self.fx.write("b/two.md", OTHER)
        self.assertEqual(self.audit()["totals"]["pairs"], 0)

    def test_supplement_that_kept_its_base_is_a_superset(self) -> None:
        self.fx.write("a/04_dossier.md", BODY)
        self.fx.write("a/30_dossier_supplement.md", BODY + "\n\nappendix: extra words here\n")
        report = self.audit()
        self.assertEqual(report["findings"][0]["state"], "superset")

    def test_index_line_declares_duplication(self) -> None:
        self.fx.write("a/08_doc.md", BODY)
        self.fx.write("a/27_doc_2026-08-09.md", BODY)
        self.fx.write(
            "a/INDEX.md",
            "| 27 | `27_doc_2026-08-09.md` | Логика (дубль файла 08) | SUPPLEMENT |\n",
        )
        report = self.audit()
        self.assertTrue(report["findings"][0]["declared"])
        self.assertEqual(report["findings"][0]["declaration"]["kind"], "index-line")
        self.assertEqual(report["totals"]["identicalTextUndeclared"], 0)

    def test_bare_numbers_declare_nothing(self) -> None:
        # "Лк 24:13" carries both numbers and means nothing about duplication.
        self.fx.write("a/13_doc.md", BODY)
        self.fx.write("a/24_doc_2026-08-09.md", BODY)
        self.fx.write("b/atlas.md", "Лк 24:13: селение в шестидесяти стадиях; версия текста иная.\n")
        report = self.audit()
        self.assertFalse(report["findings"][0]["declared"])
        self.assertEqual(report["totals"]["identicalTextUndeclared"], 1)

    def test_version_names_declare_generations(self) -> None:
        self.fx.write("a/research_v0_5.md", BODY)
        self.fx.write("a/research_v0_6.md", BODY + "\n\n")
        report = self.audit()
        self.assertTrue(report["findings"][0]["declared"])
        self.assertEqual(report["findings"][0]["declaration"]["kind"], "version-name")

    def test_check_fails_only_on_undeclared_identical_pair(self) -> None:
        self.fx.write("a/13_doc.md", BODY)
        self.fx.write("a/24_doc.md", BODY)
        out = self.fx.root / "report.json"
        self.assertEqual(twins.main(["--root", str(self.fx.root), "--min-words", "5",
                                     "-o", str(out), "--check"]), 1)
        self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["totals"]
                         ["identicalTextUndeclared"], 1)

    def test_report_schema_and_scope(self) -> None:
        self.fx.write("a/one.md", BODY)
        self.fx.write("b/two.md", OTHER)
        report = self.audit()
        self.assertEqual(report["schemaVersion"], twins.SCHEMA_VERSION)
        self.assertEqual(report["authorityId"], twins.AUTHORITY_ID)
        self.assertEqual(report["scope"]["documentsCompared"], 2)
        self.assertIn("byState", report["totals"])


class CommittedTwinReportTests(unittest.TestCase):
    """The committed report has to describe the tree it is committed with.

    Without this the twins artefact was the only one in the register with no gate of its own:
    §15 is generated from it and the claims audit compares text against the artefact, so a
    report describing yesterday's corpus would agree with a table generated from itself.
    The merge that brought a new Charnock document proved it - the numbers moved and nothing
    said so.
    """

    def test_committed_report_reappears(self) -> None:
        root = Path(__file__).resolve().parents[1]
        committed = json.loads((root / "data" / "document-twins-2026-11-18.json").read_text(encoding="utf-8"))
        self.assertEqual(twins.audit(root), committed,
                         "regenerate data/document-twins-2026-11-18.json (если дерево уехало — merge main и переснимите; см. §33.5)")


if __name__ == "__main__":
    unittest.main()
