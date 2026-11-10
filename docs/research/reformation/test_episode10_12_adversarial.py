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
                    self.assertIn(key, apparatus)
                self.assertIn("adversarial-матрица", apparatus)
                self.assertIn("Допустим", apparatus)
                self.assertIn("REF-P", apparatus)
                self.assertIn("HOLD", apparatus)

    def test_wave412_first_section_and_source_scope_retained(self):
        """No research-status prologue; full limits remain in each source apparatus."""
        cases = (
            (10, "Не одна Реформация на двух островных берегах",
             "Не объединять два самостоятельных королевства"),
            (11, "Когда веру стали защищать государственным мечом",
             "Полной колляции оригинальных латинских"),
            (12, "Открытая книга ещё не значит открытая школа",
             "фактическая степень его прочтения"),
        )
        for n, first_section, original_limit in cases:
            with self.subTest(chapter=n):
                text = self.books[n]
                reader, apparatus = text.split("## Источниковедческий аппарат", 1)
                self.assertTrue(reader.startswith(f"# Эпизод {n:02}."))
                self.assertIn("\n\n## " + first_section, reader)
                self.assertNotIn("**Статус:**", reader)
                self.assertIn("**Статус:** RESEARCH_MANUSCRIPT_DRAFT", apparatus)
                self.assertEqual(apparatus.count(original_limit), 1)
                for gate in ("NOT_EDITORIAL_READY", "PUBLICATION_HOLD", "RIGHTS_HOLD"):
                    self.assertIn(gate, apparatus)

    def test_reader_research_apparatus_separation_and_no_evidence_loss(self):
        """After editing, witness locators stay in apparatus, not the reader."""
        import re
        for number in (10, 11, 12):
            reader, apparatus = self.books[number].split("## Источниковедческий аппарат", 1)
            with self.subTest(chapter=number):
                self.assertGreaterEqual(len(reader.split()), 1700)
                self.assertIsNone(re.search(r"\\bREF-[SP]\\d+|CATALOG_ONLY|DDE\\s+L\\d{3}", reader))
                self.assertNotIn("COPY_DATE_CONFLICT_22_29_MAY_1599", reader)
                self.assertIn("PUBLICATION_HOLD", self.books[number])
                self.assertIn("REF-P", apparatus)
        nant_reader, nant_notes = self.books[11].split("## Источниковедческий аппарат", 1)
        self.assertIn("Перенесённые источниковедческие пояснения", nant_notes)
        self.assertEqual(nant_notes.count("**Перенесённое пояснение "), 8)
        for fact in ("13 апреля", "30 апреля", "статья XI", "93–95",
                     "25 февраля 1599", "22 мая 1599 года"):
            self.assertIn(fact.lower(), nant_reader.lower())
        self.assertNotIn("2026", nant_reader)
        self.assertNotIn("29 мая 1599 года", nant_reader)
        self.assertIn("29 мая", nant_notes)
        self.assertIn("CUSTODIAN_DATE_22_MAY_1599_CONFIRMED", nant_notes)
        scot_reader, scot_notes = self.books[10].split("## Источниковедческий аппарат", 1)
        self.assertIn("Первоначальная рукопись Шотландского исповедания", scot_reader)
        self.assertNotIn("Теперь доступны **две разные академические презентации", scot_reader)
        for evidence in ("A1560/8/3", "A1567/12/3", "Skene", "Lekpreuik"):
            self.assertIn(evidence, scot_notes)
        for proof in ("L198–231", "L423–463", "L926–935",
                      "ORIGINAL_GENEVAN_COLLATION_HOLD", "EARLY_XI_COLLATION_HOLD",
                      "COPY_DATE_CONFLICT_22_29_MAY_1599", "J//943/2"):
            self.assertIn(proof, nant_notes)
        lives_reader, lives_notes = self.books[12].split("## Источниковедческий аппарат", 1)
        self.assertIn("Перенесённые справочные локаторы", lives_notes)
        self.assertEqual(lives_notes.count("**Перенесённое пояснение "), 3)
        self.assertIn("1524 году", lives_reader)
        self.assertIn("1537 года", lives_reader)
        for proof in ("REF-P06: CATALOG_ONLY / LOCATOR_MISSING",
                      "StAZH B VI 249 fol.1r", "1883 года", "1542 года"):
            self.assertIn(proof, lives_notes)

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
        self.assertEqual(src["sourceCount"], 204)
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
