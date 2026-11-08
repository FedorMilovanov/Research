#!/usr/bin/env python3
"""Archive boundary and legal-reading regression for Nantes 1599, wave 391.

Registered Paris print XI and I–II are directly readable; changes against the
lost 1598 original remain SECONDARY. No claim of early autograph collation.
"""
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class NantesWorshipAndAmnestyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (HERE / "episode11_france_catholic_reform_nantes_1545_1599_manuscript.md").read_text(encoding="utf-8")
        cls.dossier = (HERE / "09_france_confession_nantes_source_study.md").read_text(encoding="utf-8")
        cls.claims = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        cls.plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        registry = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        cls.registry = registry
        cls.refs = {v["id"]: v for v in registry["sources"]}

    def test_source_provenance_is_conservative(self):
        self.assertEqual(self.registry["sourceCount"], 202)
        self.assertEqual(len(self.refs), 202)
        for k in ("REF-P27", "REF-P29", "REF-P86", "REF-S99", "REF-S100"):
            self.assertIn(k, self.refs)
        self.assertEqual(self.refs["REF-P27"]["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(self.refs["REF-P29"]["accessState"], "CATALOG_ONLY")
        self.assertEqual(self.refs["REF-P86"]["accessState"], "CATALOG_ONLY")
        for k in ("REF-S99", "REF-S100"):
            with self.subTest(source=k):
                v = self.refs[k]
                self.assertEqual(v["evidenceClass"], "B1")
                self.assertEqual(v["accessState"], "PARTIAL_OBJECT")
                self.assertIn("ARCHIVE_HOLD", v["holds"])
                self.assertIn("RIGHTS_HOLD", v["holds"])
                self.assertIn("PUBLICATION_HOLD", v["holds"])

    def test_bailiwick_exception_is_limited_and_early_comparison_held(self):
        for key in ("Статья XI", "L423–463", "011v–012r",
                    "епископские", "владения духовенства",
                    "Денис Рамеле", "Бернара Котре",
                    "EARLY_XI_COLLATION_HOLD", "уже ранее"):
            with self.subTest(key=key):
                self.assertIn(key.lower(), self.chapter.lower())
        for key in ("REF-S99", "Bernard Cottret", "L423–463",
                    "не**", "EARLY_XI_COLLATION_HOLD"):
            with self.subTest(key=key):
                self.assertIn(key.lower(), self.dossier.lower())
        self.assertIn("L441–455", self.refs["REF-S99"]["verificationNote"])

    def test_legal_amnesty_is_not_forgetting_history(self):
        for key in ("Статьи I–II", "L198–231", "006r–007r",
                    "юридического забвения", "исследовать прошлое",
                    "судебным делам"):
            with self.subTest(key=key):
                self.assertIn(key.lower(), self.chapter.lower())
        self.assertIn("REF-P27", self.dossier)
        self.assertIn("амнистия", self.dossier.lower())

    def test_legal_peace_does_not_erase_redress_problem(self):
        for name, doc in (("chapter", self.chapter), ("dossier", self.dossier)):
            with self.subTest(name=name):
                self.assertIn("Депре" if name == "chapter" else "Desprez", doc)
                self.assertIn("потерпевш", doc.lower())
                self.assertIn("L198–231", doc)
                self.assertIn("судебн", doc.lower())
                self.assertIn("не" if name == "chapter" else "Недоказанное", doc)
        self.assertIn("DESPREZ_CHRONOLOGY_CONFLICT", self.dossier)
        self.assertIn("DESPREZ_CHRONOLOGY_CONFLICT", self.plan)
        self.assertIn("LOCAL_EXECUTION_HOLD", self.plan)
        row = next(l for l in self.claims.splitlines() if l.startswith("| C301 |"))
        self.assertIn("DESPREZ_CHRONOLOGY_CONFLICT", row)
        self.assertIn("REF-P27", row)
        self.assertIn("B1 интерпретацию", row)
        self.assertEqual(self.registry["sourceCount"], 202)
        self.assertEqual(len(self.refs), 202)
        self.assertIn("PUBLICATION_HOLD", self.refs["REF-P27"]["holds"])

    def test_engraving_is_not_primary_1599_witness(self):
        for marker in ("REF-S100", "Jan Luyken", "Élie Benoist",
                       "1693", "нельзя принимать за репортаж", "RIGHTS_HOLD"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.dossier.lower())

    def test_claim_and_handoff_keep_distinct_literature_levels(self):
        row = next(l for l in self.claims.splitlines() if l.startswith("| C301 |"))
        for marker in ("REF-P27", "REF-S99", "L423–463",
                       "EARLY_XI_COLLATION_HOLD", "LOCAL_EXECUTION_HOLD"):
            self.assertIn(marker, row)
        for marker in ("волна 391", "INDEPENDENT_EXTERNAL_REVIEW_OPEN",
                       "THEOLOGICAL_PEER_REVIEW_OPEN", "EARLY_XI_COLLATION_HOLD",
                       "RIGHTS_HOLD", "EDITORIAL_HANDOFF_HOLD",
                       "PUBLICATION_HOLD", "STOP_DISCOVERY"):
            self.assertIn(marker, self.plan)


if __name__ == "__main__":
    unittest.main()
