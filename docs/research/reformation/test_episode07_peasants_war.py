#!/usr/bin/env python3
"""Reformation episode 07: source witnesses, chronology and publication holds."""
from pathlib import Path
import json
import unittest

D=Path(__file__).resolve().parent
CH=D/"episode07_luther_peasants_war_1524_1525_manuscript.md"

class PeasantsWarBookTests(unittest.TestCase):
    def test_written_chapter_with_two_distinct_luther_works(self):
        chapter=CH.read_text(encoding="utf-8")
        self.assertTrue(chapter.startswith("# Эпизод 07."))
        self.assertGreaterEqual(len(chapter.split()),2000)
        for phrase in ("RESEARCH_MANUSCRIPT_DRAFT","PUBLICATION_HOLD",
                       "Двенадцать статей", "Лотцер", "Шаппелер",
                       "Первое слово Лютера", "Второе слово Лютера",
                       "Вайнсберг",
                       "Вайнгартен", "Мюнцер", "Источниковедческий аппарат"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(),chapter.lower())
        self.assertIn("не проверены",chapter.lower())

    def test_unmerged_print_objects_and_primary_provenance(self):
        j=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(j["sourceCount"],len(j["sources"]))
        records={s["id"]:s for s in j["sources"]}
        for key in ("REF-P07-ZRH","REF-P07-WIT","REF-P08","REF-P08-ERF",
                    "REF-P76","REF-S78","REF-S79"):
            with self.subTest(key=key):
                self.assertIn(key,records)
                self.assertIn("PUBLICATION_HOLD",records[key]["holds"])
        self.assertNotEqual(records["REF-P07-ZRH"]["url"], records["REF-P07-WIT"]["url"])
        self.assertNotEqual(records["REF-P08"]["url"], records["REF-P08-ERF"]["url"])
        self.assertEqual(records["REF-P07-WIT"]["accessState"],"CATALOG_ONLY")
        self.assertEqual(records["REF-P76"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(records["REF-P76"]["evidenceClass"],"A1")
        self.assertEqual(records["REF-S78"]["evidenceClass"],"B1")
        self.assertEqual(records["REF-S79"]["evidenceClass"],"B1")
        self.assertIn("ARCHIVE_HOLD",records["REF-P76"]["holds"])

    def test_reader_navigation_and_overclaim_guards(self):
        for name in ("README.md", "04_series_blueprint.md", "SELF_PLAN.md",
                     "episode06_schleitheim_1527_1529_manuscript.md"):
            with self.subTest(name=name):
                self.assertIn(CH.name,(D/name).read_text(encoding="utf-8"))
        ledger=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for i in range(262,268):
            self.assertIn("| C%d |" % i,ledger)
        self.assertIn("NOT_EDITORIAL_READY",(D/"SELF_PLAN.md").read_text(encoding="utf-8"))

    def test_no_publication_and_no_undocumented_literal_quote(self):
        s=CH.read_text(encoding="utf-8")
        self.assertIn("не завершена полная строковая колляция",s)
        self.assertIn("не выдана за прочитанную полная критическая",s)
        self.assertIn("призыв",s)
        self.assertIn("не документирует судьбу каждой деревни",s)
        self.assertIn("PUBLICATION_HOLD",s)

if __name__=="__main__":
    unittest.main()
