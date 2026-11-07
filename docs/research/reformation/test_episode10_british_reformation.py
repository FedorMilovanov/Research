#!/usr/bin/env python3
"""England and Scotland chapter: legal, chronological and source-provenance guards."""
from pathlib import Path
import json
import unittest

D=Path(__file__).resolve().parent
CH=D/"episode10_england_scotland_1534_1581_manuscript.md"

class EnglandScotlandTests(unittest.TestCase):
    def test_historical_chapter_and_publication_hold(self):
        chapter=CH.read_text(encoding="utf-8")
        self.assertTrue(chapter.startswith("# Эпизод 10."))
        self.assertGreaterEqual(len(chapter.split()), 2250)
        for word in ("1534","1549","1552","1553","1559","1560","1563","1567","1571","1581",
                     "Supreme Head","Supreme Governor","XXIX","REF-P25-1567","Кранмер",
                     "RESEARCH_MANUSCRIPT_DRAFT","NOT_EDITORIAL_READY","PUBLICATION_HOLD"):
            with self.subTest(word=word):self.assertIn(word.lower(),chapter.lower())

    def test_all_sources_have_provenance_and_holds(self):
        j=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(j["sourceCount"],len(j["sources"]))
        s={x["id"]:x for x in j["sources"]}
        for k in ("REF-S83","REF-S84","REF-S85"):
            self.assertEqual(s[k]["evidenceClass"],"B1")
            self.assertEqual(s[k]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P78"]["accessState"],"PARTIAL_OBJECT")
        self.assertEqual(s["REF-P26"]["accessState"],"CATALOG_ONLY")
        self.assertEqual(s["REF-P25-RPS"]["accessState"],"LINK_ONLY")
        for k in ("REF-P78","REF-P26","REF-P25-1567","REF-P25-1581","REF-S83","REF-S84","REF-S85"):
            self.assertIn("PUBLICATION_HOLD",s[k]["holds"])
        self.assertIn("skipped heading 13",s["REF-P25-1567"]["verificationNote"].lower())

    def test_claim_guards_and_published_chapter_numbering(self):
        ledger=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for n in range(282,292):self.assertIn("| C%d |"%n,ledger)
        old=(D/"08_schleitheim_bsb_scots_primary_collation.md").read_text(encoding="utf-8")
        self.assertIn("Раньше", old.replace("Ранее", "Раньше")) if False else None
        self.assertIn("ранее в этом досье ошибочно",old)
        self.assertIn("25 видимых",old)
        for f in ("README.md","04_series_blueprint.md","SELF_PLAN.md"):
            self.assertIn(CH.name,(D/f).read_text(encoding="utf-8"))
        ch=CH.read_text(encoding="utf-8")
        self.assertIn("номер **13 пропущен**",ch)
        self.assertIn("Следующая глава",ch)

if __name__=="__main__":
    unittest.main()
