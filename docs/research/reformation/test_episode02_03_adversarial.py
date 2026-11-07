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
        self.assertEqual(reg["sourceCount"], 193)
        self.assertEqual(len(reg["sources"]), 193)
        self.assertTrue(all("PUBLICATION_HOLD" in x["holds"] for x in reg["sources"]))
        claim = (D / "03_claim_verification_register.md").read_text(encoding="utf-8")
        import re
        ids = [int(x) for x in re.findall(r"^\|\s*C(\d+)\s*\|", claim, re.M)]
        self.assertEqual(ids, list(range(1, 320)))

if __name__ == "__main__":
    unittest.main()
