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
        self.assertIn("не выдана за прочитанную",chapter.lower())

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

    def test_wave453_weinsberg_civic_penalty_not_individual_guilt(self):
        """Municipal B1 summary warrants a dated civic consequence, not
        direct-reading or individualized criminal liability."""
        chapter = CH.read_text(encoding="utf-8")
        reader, apparatus = chapter.split("## Источниковедческий аппарат", 1)
        for fact in (
            "21 мая 1525 года",
            "войска Швабского союза сожгли Вайнсберг",
            "1553 году",
            "коллективного наказания",
            "не доказательство личной виновности каждого жителя",
            "непосредственному воздействию памфлета Лютера",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact.lower(), reader.lower())
        self.assertNotIn("каждый житель участвовал", reader.lower())
        registry = json.loads((D / "source-registry-v1.json").read_text(
            encoding="utf-8"
        ))
        self.assertEqual(registry["sourceCount"], len(registry["sources"]))
        self.assertGreaterEqual(registry["sourceCount"], 217)
        source = next(s for s in registry["sources"] if s["id"] == "REF-S109")
        self.assertEqual(source["evidenceClass"], "B1")
        self.assertEqual(source["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(source["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertIsNone(source["documentYear"],
                          "Undated modern webpage must not acquire a made-up year")
        for hold in ("EVIDENCE_HOLD", "ARCHIVE_HOLD",
                     "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, source["holds"])
        for marker in ("REF-S109", "ORIGINAL_PUNITIVE_ORDER_UNREAD",
                       "21 мая 1525", "1553"):
            self.assertIn(marker, apparatus)
        claim = next(
            row for row in (D / "03_claim_verification_register.md").read_text(
                encoding="utf-8"
            ).splitlines() if row.startswith("| C266 |")
        )
        for marker in ("REF-S109", "INDIVIDUAL", "REJECTED_FORMULATION"):
            self.assertIn(marker.lower(), claim.lower())
        sweep = (D / "HOLD_SOURCE_SWEEP_2026-11-11.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Волна 453 — Вайнсберг 1525", sweep)
        self.assertIn("217 PUBLICATION_HOLD", sweep)
        self.assertIn("ORIGINAL_PUNITIVE_ORDER_UNREAD", sweep)
        self.assertEqual(
            len([s for s in registry["sources"]
                 if "PUBLICATION_HOLD" in s["holds"]]),
            registry["sourceCount"],
        )

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
        self.assertIn("Полное дипломатическое сопоставление каждой строки двух факсимиле в данной волне не выполнено",s)
        self.assertIn("не выдана за прочитанную полная критическая",s)
        self.assertIn("призыв",s)
        self.assertIn("не документирует судьбу каждой деревни",s)
        self.assertIn("PUBLICATION_HOLD",s)

if __name__=="__main__":
    unittest.main()
