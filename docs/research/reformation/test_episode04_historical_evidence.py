#!/usr/bin/env python3
"""Regression guards for Zurich 1523/1525 evidence limits and actual manuscript."""
from pathlib import Path
import json
import re
import unittest

HERE = Path(__file__).resolve().parent
CH = HERE / "episode04_zurich_zwingli_1523_1525_manuscript.md"

class Episode04HistoricalEvidenceTests(unittest.TestCase):
    def test_chapter04_full_reader_and_17_january_disputation_sequence(self):
        """The chapter retains the council-vs-conscience narrative and evidence limits."""
        content = CH.read_text(encoding="utf-8")
        reader, apparatus = content.split("## Источниковедческий аппарат", 1)
        self.assertEqual(reader.count("## "), 9)
        self.assertNotRegex(reader, r"https?://")
        for phrase in ("3 января 1523 года", "29 января 1523 года",
                       "Иоганна Фабера", "евхаристической жертвы",
                       "июне 1524 года", "апреле 1525-го",
                       "12 января", "17 января", "18 января",
                       "21 января", "в течение восьми дней",
                       "не «запрет детокрещения»",
                       "приказе о высылке", "исполнены"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, reader)
        january = reader.split(
            "## Январь 1525-го: вопрос о крещении становится вопросом закона", 1
        )[1].split("## Два притязания на верность Писанию", 1)[0]
        self.assertLess(january.index("12 января"), january.index("17 января"))
        self.assertLess(january.index("17 января"), january.index("18 января"))
        self.assertLess(january.index("18 января"), january.index("21 января"))
        self.assertIn("Исторические", reader)
        self.assertIn("www.befg.de/", apparatus)
        self.assertIn("uecf.net/books/zwingli-potter/chapter7.html", apparatus)
        self.assertIn("непосредственно новое чтение листов", apparatus)
        for gate in ("RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY",
                     "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(gate, apparatus)
        self.assertIn("episode05_marburg_colloquy_1529_manuscript.md", reader)

    def test_navigation_and_publication_hold(self):
        self.assertTrue(CH.is_file())
        s = CH.read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# Эпизод 04."))
        self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", s)
        self.assertIn("PUBLICATION_HOLD", s)
        self.assertIn("не выполнена", s)
        self.assertGreaterEqual(len(s.split()), 1800)
        for f in ("README.md", "SELF_PLAN.md", "04_series_blueprint.md", "episode03_luther_worms_1520_1521_manuscript.md"):
            with self.subTest(file=f):
                self.assertIn(CH.name, (HERE / f).read_text(encoding="utf-8"))

    def test_four_archival_objects_are_distinct_and_not_falsely_read(self):
        j = json.loads((HERE/"source-registry-v1.json").read_text(encoding="utf-8"))
        src = {x["id"]: x for x in j["sources"]}
        for id_,exact_url in {
            "REF-P67": "ID=4652025",
            "REF-P68": "ID=4652027",
            "REF-P69": "ID=1158607",
            "REF-P70": "ID=4652028",
        }.items():
            with self.subTest(id=id_):
                o=src[id_]
                self.assertEqual(o["accessState"],"CATALOG_ONLY")
                self.assertEqual(o["locatorState"],"COARSE_LOCATOR_ONLY")
                self.assertIn("ARCHIVE_HOLD",o["holds"])
                self.assertIn("PUBLICATION_HOLD",o["holds"])
                self.assertIn(exact_url,o["url"])
        self.assertNotEqual(src["REF-P68"]["url"],src["REF-P69"]["url"])
        self.assertEqual(src["REF-P71"]["documentYear"],1524)
        self.assertIn("ARCHIVE_HOLD",src["REF-P71"]["holds"])
        self.assertEqual(src["REF-S73"]["evidenceClass"],"B1")

    def test_egli_1879_original_print_selected_not_council_autograph(self):
        j = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        x = {v["id"]:v for v in j["sources"]}
        self.assertEqual(x["REF-P72"]["documentYear"],1879)
        self.assertEqual(x["REF-P72"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(x["REF-P72"]["locatorState"],"EXACT_LOCATOR_VERIFIED")
        self.assertIn("ARCHIVE_HOLD",x["REF-P72"]["holds"])
        self.assertIn("PUBLICATION_HOLD",x["REF-P72"]["holds"])
        for token in ("p275", "p276", "p278", "canvas289", "canvas290", "canvas292", "SHA256"):
            self.assertIn(token,x["REF-P72"]["verificationNote"])
        for ref in ("REF-P68", "REF-P69", "REF-P70"):
            self.assertEqual(x[ref]["accessState"],"CATALOG_ONLY")
        chapter = CH.read_text(encoding="utf-8")
        for phrase in ("№621", "№622", "№624", "Рёубли", "Хетцеру", "рукописный"):
            self.assertIn(phrase,chapter)
        ledger = (HERE/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for n in (243,244,245):
            self.assertIn("| C%d |" % n,ledger)
        self.assertIn("REF-P72",ledger)

    def test_editorial_voice_chronology_and_institutional_source(self):
        source = json.loads((HERE/"source-registry-v1.json").read_text(encoding="utf-8"))
        records = {v["id"]:v for v in source["sources"]}
        self.assertEqual(records["REF-S74"]["evidenceClass"], "B1")
        self.assertIn("ARCHIVE_HOLD", records["REF-S74"]["holds"])
        chapter = CH.read_text(encoding="utf-8")
        main_text = chapter.split("## Источниковедческий аппарат")[0]
        self.assertIn("июне 1524", main_text)
        self.assertIn("апреле 1525", main_text)
        self.assertIn("без требования сознательной веры", main_text)
        self.assertIn("приказе о высылке", main_text)
        self.assertNotIn("нами непосредственно прочитаны", main_text)
        self.assertNotIn("в прежнем исследовании", main_text)
        self.assertIn("REF-P71", chapter)
        self.assertIn("REF-S74", chapter)
        self.assertIn("PUBLICATION_HOLD", chapter)
        self.assertIn("EXTERNAL_REVIEW_OPEN", (HERE/"SELF_PLAN.md").read_text(encoding="utf-8"))

    def test_faber_and_grebel_critical_counterposition(self):
        source = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        s = {v["id"]: v for v in source["sources"]}
        self.assertEqual(s["REF-S75"]["evidenceClass"], "B1")
        self.assertEqual(s["REF-S75"]["accessState"], "PARTIAL_OBJECT")
        self.assertIn("ARCHIVE_HOLD", s["REF-S75"]["holds"])
        self.assertIn("FULL ARTICLE BODY NOT READ", s["REF-S75"]["verificationNote"])
        chapter = CH.read_text(encoding="utf-8")
        before_apparatus = chapter.split("## Источниковедческий аппарат")[0]
        for phrase in ("Иоганна Фабера", "евхаристической жертвы", "церковного пения на немецком языке", "Еф. 5", "Кол. 3", "общая чаша"):
            self.assertIn(phrase, before_apparatus)
        self.assertIn("REF-S75", chapter)
        self.assertIn("INDEPENDENT_EXTERNAL_REVIEW_OPEN", (HERE/"SELF_PLAN.md").read_text(encoding="utf-8"))
        ledger = (HERE/"03_claim_verification_register.md").read_text(encoding="utf-8")
        self.assertIn("| C246 |", ledger)
        self.assertIn("| C247 |", ledger)

    def test_incompatible_conclusions_remain_rejected(self):
        s = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        rows = {}
        for line in s.splitlines():
            cols = [part.strip() for part in line.split("|")]
            if len(cols) > 2 and cols[1].startswith("C") and cols[1][1:].isdigit():
                rows[int(cols[1][1:])] = line
        for n in range(236,243):
            with self.subTest(n=n):
                self.assertIn(n,rows)
                self.assertIn("REJECTED_FORMULATION",rows[n])
                self.assertIn("PUBLICATION_HOLD",rows[n])
        self.assertIn("REF-P68",rows[239])
        self.assertIn("REF-P69",rows[239])
        self.assertIn("REF-S73",rows[239])
        chapter = CH.read_text(encoding="utf-8")
        for token in ("3 января", "29 января", "12 января", "18 января", "21 января", "5 сентября 1524", "в течение восьми дней"):
            with self.subTest(token=token):
                self.assertIn(token,chapter)

if __name__ == "__main__":
    unittest.main()
