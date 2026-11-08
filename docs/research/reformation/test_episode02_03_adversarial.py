#!/usr/bin/env python3
"""Wave 382: source-critical and reader-flow checks for Reformation chapters 02-03."""
from pathlib import Path
import json
import unittest

D = Path(__file__).resolve().parent
CH02 = D / "episode02_indulgences_1517_manuscript.md"
CH03 = D / "episode03_luther_worms_1520_1521_manuscript.md"

class Luther1517WormsEditorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.two = CH02.read_text(encoding="utf-8")
        cls.three = CH03.read_text(encoding="utf-8")

    def test_ch02_instruction_does_not_erase_papal_intercession_or_thesis35(self):
        s = self.two
        reader, apparatus = s.split("## Источниковедческий аппарат", 1)
        for marker in ("первой", "тезис 35", "тезисе 26", "тезис 28",
                       "тезис 71", "тезис 72", "не", "сокрушени",
                       "Kidd", "REF-P01"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), s.lower())
        self.assertIn("тезис 35", reader.lower())
        self.assertIn("Adversarial-проверка", apparatus)
        self.assertIn("Оксфордское издание", reader)
        self.assertIn("PUBLICATION_HOLD", s)
        self.assertIn("NOT_EDITORIAL_READY", s)

    def test_wave399_reader_apparatus_boundary_and_verbatim_evidence_retention(self):
        """Keep original witness qualifications without interrupting reader prose."""
        import re
        for chapter, expected in ((self.two, 5), (self.three, 10)):
            reader, apparatus = chapter.split("## Источниковедческий аппарат", 1)
            with self.subTest(original_explanations=expected):
                self.assertGreater(len(reader.split()), 2000)
                self.assertEqual(apparatus.count("**Первоначальное пояснение "), expected)
                self.assertNotRegex(reader, r"\bREF-[PS]\d+|\bVD16\b|CATALOG_ONLY|ORIGINAL_PRINT_COLLATION_HOLD")
                self.assertIn("PUBLICATION_HOLD", chapter)
                self.assertIn("ORIGINAL_PRINT_COLLATION_HOLD", apparatus)
                self.assertIn("RIGHTS_HOLD", apparatus)
        reader2, apparatus2 = self.two.split("## Источниковедческий аппарат", 1)
        for marker in ("Оксфордское издание", "тезисом 35", "31 октября 1517 года",
                       "лейпцигской печати последний номер оказался 87",
                       "тезисе 71", "тезис 72"):
            self.assertIn(marker.lower(), reader2.lower())
        for preserved in ("Jnstructiones Confessorum", "Instructio summaria",
                          "**Тезис 71** сформулирован", "Нюрнбергский и базельский",
                          "Для научной ссылки нужно различать"):
            self.assertIn(preserved, apparatus2)
        reader3, apparatus3 = self.three.split("## Источниковедческий аппарат", 1)
        for marker in ("1.18", "9.3", "видимого знака", "Reg. E 81",
                       "зависим", "8 мая", "12 мая", "25 мая", "26 мая"):
            self.assertIn(marker.lower(), reader3.lower())
        for witness in ("VD16 L3759", "VD16 L4189", "VD16 L3653",
                        "VD16 A3024", "REF-P64", "Taylor Institution Library"):
            self.assertIn(witness, apparatus3)
        self.assertIn("https://editions.mml.ox.ac.uk/editions/freiheit-1520/", apparatus3)
        self.assertIn("https://tueditions.ulb.tu-darmstadt.de/v/pa000008-0107", apparatus3)

    def test_ch02_1517_prints_and_letter_details_stay_in_backstage(self):
        s = self.two
        reader, apparatus = s.split("## Источниковедческий аппарат", 1)
        self.assertLess(len(reader.split()), 2600)
        self.assertIn("Письмо 31 октября — полный предшествующий разбор", apparatus)
        self.assertIn("Ранние печати 1517 года — полный предшествующий", apparatus)
        for term in ("автограф", "Дрездене", "Базел", "Нюрнберг"):
            self.assertIn(term.lower(), apparatus.lower())
        self.assertIn("episode03_luther_worms_1520_1521_manuscript.md", reader)
        self.assertNotIn("См. будущий ненаписанный эпизод", reader)

    def test_ch03_sacramental_sources_and_opposing_argument(self):
        s = self.three
        reader, apparatus = s.split("## Источниковедческий аппарат", 1)
        for marker in ("1.18", "9.3", "три", "два", "видимого знака",
                       "Каэтаном", "28 июня 1519", "Карла V", "императорской стороны"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), reader.lower())
        self.assertIn("Adversarial-проверка", apparatus)
        self.assertIn("REF-P64", apparatus)
        self.assertIn("NOT_EDITORIAL_READY", s)
        self.assertIn("PUBLICATION_HOLD", s)

    def test_worms_edit_rejects_false_stenography_and_may8_signature(self):
        s = self.three
        reader, apparatus = s.split("## Источниковедческий аппарат", 1)
        for marker in ("8 мая", "12 мая", "25 мая", "26 мая",
                       "не на пленарном", "Reg. E 81", "зависим",
                       "разных", "подписал"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), reader.lower())
        for marker in ("REF-S72", "C233", "C234", "C235", "P44", "P46",
                       "C229", "26.05", "8.05"):
            self.assertIn(marker, apparatus)
        self.assertIn("episode04_zurich_zwingli_1523_1525_manuscript.md", s)

    def test_scope_preserves_193_source_319_claim_base(self):
        reg = json.loads((D / "source-registry-v1.json").read_text(encoding="utf-8"))
        # Preserve the 193-source historical floor; later editorial waves may add
        # genuine, separately registered evidence without breaking chapter tests.
        self.assertGreaterEqual(reg["sourceCount"], 193)
        self.assertEqual(len(reg["sources"]), reg["sourceCount"])
        self.assertTrue(all("PUBLICATION_HOLD" in x["holds"] for x in reg["sources"]))
        claim = (D / "03_claim_verification_register.md").read_text(encoding="utf-8")
        import re
        ids = [int(x) for x in re.findall(r"^\|\s*C(\d+)\s*\|", claim, re.M)]
        self.assertEqual(ids, list(range(1, 320)))

if __name__ == "__main__":
    unittest.main()
