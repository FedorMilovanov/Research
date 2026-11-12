#!/usr/bin/env python3
"""Episode 12 everyday-life checks: source limits, social history and book completion."""
from pathlib import Path
import json
import unittest

D=Path(__file__).resolve().parent
CH=D/"episode12_reformation_everyday_life_1520_1600_manuscript.md"

class EverydayLifeBookTests(unittest.TestCase):
    def test_final_historical_chapter_complete_but_not_editorially_ready(self):
        text=CH.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Эпизод 12."))
        self.assertGreaterEqual(len(text.split()),3000)
        for part in ("1466","1522","1524","1526","1537","1539","1541","1542",
                     "1568","1570","1573","1871","Дентьер","Урсула","Страсбург",
                     "печат","школ","бедн","миграц","монахин","Варшав",
                     "RESEARCH_MANUSCRIPT_DRAFT","NOT_EDITORIAL_READY","PUBLICATION_HOLD"):
            with self.subTest(part=part):self.assertIn(part.lower(),text.lower())
        self.assertIn("книжный эпилог",text.lower())

    def test_source_states_are_honest_and_originals_not_misdeclared(self):
        r=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(r["sourceCount"],len(r["sources"]))
        by={x["id"]:x for x in r["sources"]}
        for id in ("REF-P79","REF-P80","REF-P81","REF-S91","REF-S92"):
            self.assertIn(id,by)
            self.assertIn("PUBLICATION_HOLD",by[id]["holds"])
        self.assertEqual(by["REF-P79"]["accessState"],"CATALOG_ONLY")
        self.assertEqual(by["REF-P79"]["evidenceClass"],"A1")
        self.assertEqual(by["REF-P80"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(by["REF-P81"]["accessState"],"PARTIAL_OBJECT")
        self.assertTrue(all(by[x]["evidenceClass"]=="B1" for x in ("REF-S91","REF-S92")))
        for id in ("REF-P05","REF-P32","REF-P33","REF-P52"):
            self.assertEqual(by[id]["accessState"],"CATALOG_ONLY")
        # Evidence-based 1524 update: verified Oxford diplomatic folios, NOT Pitts first-print autopsy.
        self.assertEqual(by["REF-P06"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(by["REF-P06"]["locatorState"],"EXACT_LOCATOR_VERIFIED")
        self.assertIn("ARCHIVE_HOLD",by["REF-P06"]["holds"])
        self.assertIn("RIGHTS_HOLD",by["REF-P06"]["holds"])
        self.assertIn("PUBLICATION_HOLD",by["REF-P06"]["holds"])
        self.assertNotIn("LOCATOR_HOLD",by["REF-P06"]["holds"])
        for folio in ("d2r","d3v","e1r"):
            self.assertIn(folio,by["REF-P06"]["verificationNote"])
        # Edwards official publisher text was read selectively; empirical claims still require checking.
        self.assertEqual(by["REF-S03"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(by["REF-S03"]["locatorState"],"EXACT_LOCATOR_VERIFIED")
        self.assertIn("EVIDENCE_HOLD",by["REF-S03"]["holds"])
        self.assertEqual(by["REF-P34"]["accessState"],"PARTIAL_OBJECT")

    def test_wave451_1871_anachronism_caveat_is_concise_and_source_preserved(self):
        """A single readable chronological caveat, not two repeated conclusions."""
        manuscript = CH.read_text(encoding="utf-8")
        reader, apparatus = manuscript.split(
            "## Источниковедческий аппарат", 1
        )
        section = reader.split(
            "## Школы и богатство: ловушка поздней статистики", 1
        )[1].split("## Были изменения — не было одного общего результата", 1)[0]
        for anchor in (
            "Беккера и Людгера Вёссмана",
            "Quarterly Journal of Economics",
            "перепись Пруссии 1871 года",
            "Саксонии в 1524 году",
            "Для такого вывода потребовались бы собственные ранние измерения",
            "гипотезой о долгосрочном наследии",
            "экономическом чуде протестантизма",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, section)
        self.assertEqual(section.count("1871 года"), 1,
                         "Do not reintroduce the redundant chronological paragraph")
        self.assertNotIn("Но статистика **1871 года**", section)
        for note in ("REF-S92", "531–596",
                     "CHRONOLOGICAL_EXTRAPOLATION_HOLD"):
            self.assertIn(note, apparatus)
        claims = (D / "03_claim_verification_register.md").read_text(
            encoding="utf-8"
        )
        for claim_id in ("C21", "C57", "C313"):
            self.assertIn("| " + claim_id + " |", claims)
        self.assertIn("TEMPORAL_EXTRAPOLATION_HOLD", claims)
        self.assertIn("PUBLICATION_HOLD", manuscript)

    def test_book_navigation_false_claims_and_scots_legacy_fix(self):
        for path in ("README.md","SELF_PLAN.md","04_series_blueprint.md"):
            self.assertIn(CH.name,(D/path).read_text(encoding="utf-8"))
        s=(D/"04_series_blueprint.md").read_text(encoding="utf-8")
        self.assertNotIn("RPS 24 главы",s)
        self.assertIn("богословский эпилог",s.lower())
        text=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for num in range(304,316):
            self.assertIn("| C%d |"%num,text)
        chapter=CH.read_text(encoding="utf-8").lower()
        self.assertIn("не",chapter)
        self.assertIn("1871 года",chapter)
        self.assertIn("не были",chapter)

if __name__=="__main__":
    unittest.main()
