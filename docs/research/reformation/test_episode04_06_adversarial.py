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
                self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", apparatus)
                self.assertIn("NOT_EDITORIAL_READY", apparatus)
                self.assertIn("PUBLICATION_HOLD", apparatus)

    def test_wave410_reader_starts_with_history_not_operational_status(self):
        """Exact metadata moves into the existing apparatus, not out of the book."""
        cases = (
            ("zurich", "Два города — не один путь", "Полная колляция всех оригинальных протоколов"),
            ("marburg", "Когда союзники спорят друг с другом", "Подписанный немецкий автограф"),
            ("schleitheim", "Почему после Марбурга мы возвращаемся назад", "Ранние печатные экземпляры Шляйтхайма"),
        )
        for key, title, unique_provenance in cases:
            with self.subTest(chapter=key):
                chapter = self.texts[key]
                reader, apparatus = chapter.split("## Источниковедческий аппарат", 1)
                self.assertRegex(reader, r"\A# Эпизод 0[456]\.[^\n]*\n\n## ")
                self.assertIn("## " + title, reader)
                self.assertNotIn("**Статус:**", reader)
                self.assertIn("**Статус:** RESEARCH_MANUSCRIPT_DRAFT", apparatus)
                self.assertEqual(apparatus.count(unique_provenance), 1)
                self.assertIn("NOT_EDITORIAL_READY", apparatus)
                self.assertIn("RIGHTS_HOLD", apparatus)
                self.assertIn("PUBLICATION_HOLD", apparatus)

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

    def test_chapter05_full_reader_preserves_articles_nine_fourteen_fifteen(self):
        """Keep the actual 1529 signed agreement distinct from party reports."""
        chapter = self.texts["marburg"]
        reader, apparatus = chapter.split("## Источниковедческий аппарат", 1)
        self.assertGreater(len(reader.split()), 1750)
        self.assertEqual(reader.count("## "), 8)
        for marker in ("Статья 9", "не пустым знаком", "Статья 10",
                       "статья 11", "статья 14", "под обоими видами",
                       "духовное вкушение", "телесном присутствии",
                       "десять богословов", "7, 13 и 15",
                       "3 октября"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), reader.lower())
        self.assertNotRegex(reader, r"https?://|\\bREF-[PS]\\d+|\\bVD16\\b")
        self.assertIn("Цвингли", reader)
        self.assertIn("Осиандер", reader)
        self.assertIn("Шляйтхайм", reader)
        self.assertIn("эпизод", reader.lower())
        for marker in ("REF-P13-ARCHIVE", "REF-P75",
                       "REF-P73", "REF-P74", "ARCHIVE_HOLD",
                       "RIGHTS_HOLD", "PUBLICATION_HOLD",
                       "NOT_EDITORIAL_READY", "Матфея"):
            with self.subTest(archive_marker=marker):
                self.assertIn(marker, apparatus)
        self.assertIn("episode06_schleitheim_1527_1529_manuscript.md", reader)

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

    def test_wave400_witness_provenance_kept_outside_reader(self):
        """Full original excerpts survive in the apparatus, not editorial memory."""
        for chapter, expected in (("zurich", 2), ("marburg", 1), ("schleitheim", 2)):
            reader, notes = self.texts[chapter].split("## Источниковедческий аппарат", 1)
            with self.subTest(chapter=chapter):
                self.assertGreater(len(reader.split()), 1700)
                self.assertEqual(notes.count("**Перенесённое пояснение "), expected)
                self.assertIn("Сохранённые исходные источниковедческие разборы", notes)
                for forbidden in ("VD16", "CATALOG_ONLY", "REF-P", "REF-S"):
                    self.assertNotIn(forbidden, reader)
                for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
                    self.assertIn(hold, notes)
                self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", notes)
                self.assertIn("NOT_EDITORIAL_READY", notes)

        zurich_reader, zurich_notes = self.texts["zurich"].split("## Источниковедческий аппарат", 1)
        for fact in ("29 января 1523", "статью 38", "статьи 42", "Цвингли"):
            self.assertIn(fact, zurich_reader)
        for locator in ("VD16 Z821", "XIX", "XXIX"):
            self.assertIn(locator, zurich_notes)

        marburg_reader, marburg_notes = self.texts["marburg"].split("## Источниковедческий аппарат", 1)
        for fact in ("десять богословов", "7, 13 и 15", "телесном присутствии"):
            self.assertIn(fact, marburg_reader)
        for proof in ("гессенский", "Цюрихский государственный архив", "живым или умершим"):
            self.assertIn(proof.lower(), marburg_notes.lower())

        sch_reader, sch_notes = self.texts["schleitheim"].split("## Источниковедческий аппарат", 1)
        for fact in ("Матфея 28", "Матфея 27", "около 1550 года", "около 1570 года"):
            self.assertIn(fact, sch_reader)
        for witness in ("VD16 ZV30530", "e-rara", "музейная транскрипция"):
            self.assertIn(witness.lower(), sch_notes.lower())
        self.assertIn("DATE_AND_IMPRINT_ATTRIBUTION_CONFLICT", sch_notes)

    def test_source_and_claim_registry_still_fail_closed(self):
        registry = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["sourceCount"], len(registry["sources"]))
        self.assertGreaterEqual(registry["sourceCount"], 195)
        self.assertTrue(all(row["publicationState"] == "REFERENCE"
                            and "PUBLICATION_HOLD" in row["holds"]
                            for row in registry["sources"]))
        ledger = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        lines = [line for line in ledger.splitlines() if line.startswith("| C") and len(line) > 3 and line[3].isdigit()]
        ids = [int(line.split(" |", 1)[0][3:]) for line in lines]
        self.assertEqual(ids, list(range(1, 320)))
        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        # Previous editorial wave must remain in history when active plan advances.
        self.assertIn("ИСТОРИЧЕСКИЙ СРЕЗ ВОЛНЫ 384", plan)
        self.assertIn("RF-EDIT-07-09", plan)
        self.assertIn("PUBLICATION_HOLD", plan)


if __name__ == "__main__":
    unittest.main()
