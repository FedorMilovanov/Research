#!/usr/bin/env python3
"""Evidence, historical chronology and publication guards for episode 08."""
from pathlib import Path
import json
import unittest

D = Path(__file__).resolve().parent
E8 = D / "episode08_justification_confessions_1530_1563_manuscript.md"

class JustificationBookTests(unittest.TestCase):
    def test_coherent_chapter_and_distinct_dates(self):
        content=E8.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("# Эпизод 08."))
        self.assertGreaterEqual(len(content.split()), 1700)
        for marker in ("1530", "1547", "1563", "Меланхтон", "Аугсбург",
                       "Тридент", "Гейдельберг", "Источниковедческий аппарат",
                       "RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY", "PUBLICATION_HOLD"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), content.lower())
        self.assertIn("следующей главе", content.lower())

    def test_arguments_not_flattened_and_primary_status_honest(self):
        content=E8.read_text(encoding="utf-8")
        for marker in ("статья IV", "статья VI", "статья XX",
                       "канон IX", "канон XI", "канон XXIV",
                       "вопросе 60", "вопрос 64", "первопечат",
                       "баптист", "не", "благодат"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), content.lower())
        r=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        s={x["id"]: x for x in r["sources"]}
        self.assertEqual(r["sourceCount"],len(r["sources"]))
        self.assertEqual(s["REF-P17"]["accessState"],"CATALOG_ONLY")
        self.assertEqual(s["REF-P77"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P77"]["locatorState"],"EXACT_LOCATOR_VERIFIED")
        self.assertEqual(s["REF-P14"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P20"]["accessState"],"PARTIAL_OBJECT")
        for id in ("REF-P14","REF-P17","REF-P20","REF-P77"):
            self.assertIn("PUBLICATION_HOLD",s[id]["holds"])

    def test_registry_and_book_navigation(self):
        ledger=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for i in range(268,274):
            self.assertIn("| C%d |"%i,ledger)
        for filename in ("README.md","SELF_PLAN.md","04_series_blueprint.md"):
            self.assertIn(E8.name, (D/filename).read_text(encoding="utf-8"))
        readme=(D/"README.md").read_text(encoding="utf-8")
        self.assertLess(readme.find("episode07_luther_peasants_war"),readme.find(E8.name))
        self.assertIn("NOT_EDITORIAL_READY",(D/"SELF_PLAN.md").read_text(encoding="utf-8"))
        self.assertIn("немецкой транскрипции GHDI",(D/"episode07_luther_peasants_war_1524_1525_manuscript.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
