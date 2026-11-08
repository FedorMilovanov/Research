#!/usr/bin/env python3
"""Scoped literary/evidence regressions for RF-EDIT-04-06.

These tests are read-only, and make no claim of original-archive or full-book
scholarly verification. They protect distinctions against editorial regression.
"""
from pathlib import Path
import json
import re
import unittest

HERE = Path(__file__).resolve().parent
FILES = {
    "zurich": HERE / "episode04_zurich_zwingli_1523_1525_manuscript.md",
    "marburg": HERE / "episode05_marburg_colloquy_1529_manuscript.md",
    "schleitheim": HERE / "episode06_schleitheim_1527_1529_manuscript.md",
}


class ReformationAdversarialFourSixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {key: path.read_text(encoding="utf-8")
                     for key, path in FILES.items()}

    def test_main_reader_keeps_evidence_and_apparatus_separate(self):
        for chapter, content in self.texts.items():
            with self.subTest(chapter=chapter):
                self.assertIn("## Источниковедческий аппарат", content)
                reader, apparatus = content.split("## Источниковедческий аппарат", 1)
                self.assertGreater(len(reader.split()), 1200)
                self.assertIn("adversarial-проверка", apparatus)
                self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", reader)
                self.assertIn("NOT_EDITORIAL_READY", reader)
                self.assertIn("PUBLICATION_HOLD", reader)

    def test_zurich_order_vs_execution_not_conflated(self):
        text = self.texts["zurich"]
        reader = text.split("## Источниковедческий аппарат", 1)[0]
        for fragment in (
            "12 января", "18 января", "21 января",
            "восьмидневный", "не «запрет детокрещения»",
            "приказ", "исполнены",
        ):
            self.assertIn(fragment.lower(), reader.lower())
        apparatus = text.split("## Источниковедческий аппарат", 1)[1]
        for fragment in ("B VI 248", "A 42.1.12", "№621", "№622", "№624", "REF-P72"):
            self.assertIn(fragment, apparatus)

    def test_marburg_difference_and_witnesses_not_erased(self):
        text = self.texts["marburg"]
        for fragment in ("четырнадцат", "стать", "пятнадцат", "телесном присутствии",
                         "десяти богословов", "7, 13 и 15",
                         "REF-P13-ARCHIVE", "REF-P75", "REF-P73", "REF-P74"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment.lower(), text.lower())
        self.assertIn("архив", text.lower())
        self.assertIn("Шляйтхайм", text)

    def test_schleitheim_variants_dates_and_civic_magistrate(self):
        text = self.texts["schleitheim"]
        for fragment in ("Матфея 28", "Матфея 27", "около 1550",
                         "около 1570", "zeugen", "schwören",
                         "не равен", "REF-P24-BSB1", "REF-P57",
                         "REF-P11", "REF-P12"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment.lower(), text.lower())
        self.assertIn("DATE_AND_IMPRINT_ATTRIBUTION_CONFLICT", text)
        self.assertIn("LOCAL_ARCHIVE_HOLD", text)

    def test_source_and_claim_registry_still_fail_closed(self):
        registry = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["sourceCount"], len(registry["sources"]))
        self.assertGreaterEqual(registry["sourceCount"], 195)
        self.assertTrue(all(row["publicationState"] == "REFERENCE"
                            and "PUBLICATION_HOLD" in row["holds"]
                            for row in registry["sources"]))
        ledger = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        lines = [line for line in ledger.splitlines() if line.startswith("| C")]
        ids = [int(line.split(" |", 1)[0][3:]) for line in lines]
        self.assertEqual(ids, list(range(1, 320)))
        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("волна 384", plan)
        self.assertIn("RF-EDIT-07-09", plan)
        self.assertIn("PUBLICATION_HOLD", plan)


if __name__ == "__main__":
    unittest.main()
