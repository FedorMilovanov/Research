#!/usr/bin/env python3
"""Scoped, read-only contract for RF-EDIT-07-09: narrative distinctions.

This guards the edited research texts; it does not verify historical truth,
critical original-print collation, use rights or editorial publication approval.
"""
from pathlib import Path
import json
import unittest

HERE = Path(__file__).resolve().parent
BOOKS = {
    7: HERE / "episode07_luther_peasants_war_1524_1525_manuscript.md",
    8: HERE / "episode08_justification_confessions_1530_1563_manuscript.md",
    9: HERE / "episode09_calvin_geneva_1535_1555_manuscript.md",
}


class ReformationAdversarialSevenNineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.books = {n: p.read_text(encoding="utf-8") for n, p in BOOKS.items()}

    def test_three_manuscripts_keep_reader_and_apparatus(self):
        for n, s in self.books.items():
            with self.subTest(chapter=n):
                self.assertTrue(s.startswith(f"# Эпизод {n:02}."))
                self.assertIn("## Источниковедческий аппарат", s)
                reader, apparatus = s.split("## Источниковедческий аппарат", 1)
                self.assertGreaterEqual(len(reader.split()), 1500)
                self.assertIn("adversarial-матрица", apparatus)
                for status in ("RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY",
                               "PUBLICATION_HOLD"):
                    self.assertIn(status, reader)
                for label in ("Допустим", "REF-P", "HOLD"):
                    self.assertIn(label.lower(), apparatus.lower())

    def test_peasants_prints_and_voice_limit(self):
        s = self.books[7]
        for marker in ("Двенадцать статей", "прежнее увещание",
                       "один авторский памфлет", "REF-P07-ZRH",
                       "REF-P07-WIT", "REF-P08", "REF-P08-ERF",
                       "не документирует судьбу каждой деревни",
                       "Полное дипломатическое сопоставление каждой строки"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), s.lower())
        self.assertIn("двух отдельных печатных экземплярах", s)

    def test_justification_different_definitions_and_confessions(self):
        s = self.books[8]
        for marker in ("статья IV", "статья VI", "статья XX",
                       "главе VII", "главе VIII", "канон IX",
                       "канон XI", "канон XXIV", "формальную",
                       "инструментальную", "REF-P14", "REF-P20",
                       "REF-P77", "1563"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), s.lower())
        self.assertIn("не", s.lower())

    def test_geneva_civil_verdict_vs_church_jurisdiction(self):
        s = self.books[9]
        for marker in ("21 мая 1536", "20 ноября 1541",
                       "30 ноября", "2 января 1542",
                       "16 февраля 1542", "десятое заседание",
                       "Малому совету", "27 октября 1553",
                       "не заменяет судебный протокол",
                       "REF-P21", "REF-P22", "REF-P38",
                       "REF-S82", "LEGAL_RECORD_HOLD"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), s.lower())

    def test_registry_count_and_single_active_plan(self):
        j = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(j["sourceCount"], len(j["sources"]))
        self.assertGreaterEqual(j["sourceCount"], 195)
        self.assertTrue(all(row["publicationState"] == "REFERENCE"
                            and "PUBLICATION_HOLD" in row["holds"]
                            for row in j["sources"]))
        lines = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8").splitlines()
        ids = [int(line.split(" |", 1)[0][3:])
               for line in lines if line.startswith("| C")
               and len(line) > 3 and line[3].isdigit()]
        self.assertEqual(ids, list(range(1, 320)))
        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("волна 385", plan)
        self.assertIn("RF-EDIT-10-12", plan)
        self.assertIn("STOP_DISCOVERY", plan)
        self.assertIn("PUBLICATION_HOLD", plan)


if __name__ == "__main__":
    unittest.main()
