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

    def test_wave426_augsburg_V_and_IX_are_distinct_confessional_charges(self):
        """Chapter 08 must tell the reader what the 1530 text says without
        claiming its polemical portrait was proved for all Anabaptists.
        """
        content = E8.read_text(encoding="utf-8")
        reader, apparatus = content.split(
            "## Источниковедческий аппарат — вне основного повествования", 1
        )
        for token in (
            "**статья V**", "**статье IX**", "внешнего Слова",
            "собственным приготовлениям и делам",
            "крестить младенцев",
            "каждый анабаптист",
            "по их собственным исповеданиям",
        ):
            with self.subTest(reader_token=token):
                self.assertIn(token, reader)
        self.assertLess(reader.index("**статья V**"), reader.index("**статье IX**"))
        self.assertNotIn("REF-P14", reader)
        self.assertNotIn("RESEARCH_MANUSCRIPT_DRAFT", reader)
        for token in (
            "REF-P14", "статьи V и IX",
            "ORIGINAL_LANGUAGE_HOLD", "INDEPENDENT_EXTERNAL_REVIEW_OPEN",
            "THEOLOGICAL_PEER_REVIEW_OPEN", "RIGHTS_HOLD",
            "PUBLICATION_HOLD",
        ):
            with self.subTest(apparatus_token=token):
                self.assertIn(token, apparatus)

        sources = json.loads(
            (D / "source-registry-v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(sources["sourceCount"], 204)
        rows = {row["id"]: row for row in sources["sources"]}
        self.assertEqual(rows["REF-P14"]["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(rows["REF-P20"]["accessState"], "PARTIAL_OBJECT")
        for source_id, marker in (
            ("REF-P14", "2026-11-11 WAVE426"),
            ("REF-P20", "2026-11-11 WAVE426"),
        ):
            with self.subTest(source=source_id):
                row = rows[source_id]
                self.assertIn(marker, row["verificationNote"])
                self.assertIn("NOT", row["verificationNote"])
                self.assertIn("RIGHTS_HOLD", row["holds"])
                self.assertIn("PUBLICATION_HOLD", row["holds"])
        ledger = (D / "03_claim_verification_register.md").read_text(
            encoding="utf-8"
        )
        c273 = next(line for line in ledger.splitlines()
                    if line.startswith("| C273 |"))
        for token in ("ст. V и IX", "полемические формулировки",
                      "ORIGINAL_LANGUAGE_HOLD", "REJECTED_FORMULATION"):
            with self.subTest(claim_token=token):
                self.assertIn(token, c273)
        reviewer = (D / "independent_review_packets.md").read_text(
            encoding="utf-8"
        )
        t02 = next(line for line in reviewer.splitlines()
                   if line.startswith("| T-02 /"))
        self.assertIn("Аугсбургское исповедание **V/IX**", t02)
        self.assertIn("REVIEW_PACKETS_PREPARED / NOT_SENT", reviewer)
        plan = (D / "SELF_PLAN.md").read_text(encoding="utf-8")
        active_plan = plan.split("---", 1)[0]
        self.assertIn("волна 426", active_plan)
        self.assertIn("INDEPENDENT_EXTERNAL_REVIEW_OPEN", active_plan)
        self.assertIn("THEOLOGICAL_PEER_REVIEW_OPEN", active_plan)
        self.assertIn("PUBLICATION_HOLD", active_plan)

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
