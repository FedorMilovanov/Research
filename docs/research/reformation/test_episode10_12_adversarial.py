#!/usr/bin/env python3
"""Read-only source and reader regression guards for RF-EDIT-10-12.

Not a substitute for independent scholarly collation or rights clearance.
These tests protect specific limits on unsupported historical inferences.
"""
from pathlib import Path
import json
import unittest

HERE = Path(__file__).resolve().parent
BOOKS = {
    10: HERE / "episode10_england_scotland_1534_1581_manuscript.md",
    11: HERE / "episode11_france_catholic_reform_nantes_1545_1599_manuscript.md",
    12: HERE / "episode12_reformation_everyday_life_1520_1600_manuscript.md",
}


class ReformationAdversarialTenTwelve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.books = {n: p.read_text(encoding="utf-8") for n, p in BOOKS.items()}

    def test_reader_apparatus_and_not_publication(self):
        for n, s in self.books.items():
            with self.subTest(n=n):
                self.assertTrue(s.startswith(f"# Эпизод {n:02}."))
                self.assertIn("## Источниковедческий аппарат", s)
                reader, apparatus = s.split("## Источниковедческий аппарат", 1)
                self.assertGreaterEqual(len(reader.split()), 1700)
                for key in ("RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY", "PUBLICATION_HOLD"):
                    self.assertIn(key, reader)
                self.assertIn("adversarial-матрица", apparatus)
                self.assertIn("Допустим", apparatus)
                self.assertIn("REF-P", apparatus)
                self.assertIn("HOLD", apparatus)

    def test_scots_and_english_legislation_not_conflated(self):
        s = self.books[10]
        for term in ("Supreme Head", "Supreme Governor", "1549", "1552", "1559",
                     "1563", "1571", "номер **13 пропущен**",
                     "A1560/8/3", "A1567/12/3", "1581/10/20",
                     "REGNAL_ASSENT_HOLD", "NUMBERING_HOLD", "REF-P78"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), s.lower())
        self.assertIn("не доказывает", s)

    def test_nantes_document_layers_and_rights(self):
        s = self.books[11]
        for term in ("95", "92", "93", "56 особых", "два brevets",
                     "25 февраля 1599", "апреле 1598",
                     "J//943/2", "статья VI", "статья XIII",
                     "статья XIV", "REF-P27", "REF-S89",
                     "ARTICLE_COUNT_VARIANT_HOLD"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), s.lower())
        self.assertIn("не** следует без доказательств", s)

    def test_everyday_life_law_is_not_execution_or_19c_census(self):
        s = self.books[12]
        for term in ("1466", "1522", "1539", "1542", "1568",
                     "1570", "1573", "1871 года",
                     "Урсула", "Дентьер", "REF-P79", "REF-P80",
                     "REF-P81", "REF-S92", "CHRONOLOGICAL_EXTRAPOLATION_HOLD"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), s.lower())
        self.assertIn("не равна первичной переписи", s)

    def test_registry_claims_and_plan_fail_closed(self):
        src = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(src["sourceCount"], len(src["sources"]))
        self.assertEqual(src["sourceCount"], 195)
        self.assertTrue(all(row["publicationState"] == "REFERENCE"
                            and "PUBLICATION_HOLD" in row["holds"]
                            for row in src["sources"]))
        ledger = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        ids = [int(line.split(" |", 1)[0][3:]) for line in ledger.splitlines()
               if line.startswith("| C") and len(line) > 3 and line[3].isdigit()]
        self.assertEqual(ids, list(range(1, 320)))
        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("RF-EDIT-10-12", plan)
        self.assertIn("RF-BOOK-FINAL-REVIEW", plan)
        self.assertIn("PUBLICATION_HOLD", plan)


if __name__ == "__main__":
    unittest.main()
