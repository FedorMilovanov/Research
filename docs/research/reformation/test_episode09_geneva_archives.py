#!/usr/bin/env python3
"""Geneva 1535–1555 chapter / archival limits and civil competence regression."""
from pathlib import Path
import json
import unittest

D=Path(__file__).resolve().parent
CH=D/"episode09_calvin_geneva_1535_1555_manuscript.md"

class GenevaChapterTests(unittest.TestCase):
    def test_narrative_history_and_holds(self):
        s=CH.read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# Эпизод 09."))
        self.assertGreaterEqual(len(s.split()),1900)
        for word in ("1535","1536","1538","1541","1542","1551","1553","Фарель",
                     "Малому совету","Консистория","Сервет","Больсек",
                     "RESEARCH_MANUSCRIPT_DRAFT","NOT_EDITORIAL_READY","PUBLICATION_HOLD"):
            with self.subTest(word=word):self.assertIn(word.lower(),s.lower())
        self.assertIn("следующей главе",s.lower())

    def test_archival_claims_and_unread_primary_holds(self):
        sources=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        by={s["id"]:s for s in sources["sources"]}
        self.assertEqual(sources["sourceCount"],len(sources["sources"]))
        for x in ("REF-P21","REF-P22","REF-P22-TRANSLATION","REF-P38","REF-S10","REF-S80","REF-S81","REF-S82"):
            with self.subTest(x=x): self.assertIn(x,by);self.assertIn("PUBLICATION_HOLD",by[x]["holds"])
        for x in ("REF-S80","REF-S81","REF-S82"):
            self.assertEqual(by[x]["evidenceClass"],"B1")
            self.assertEqual(by[x]["accessState"],"PARTIAL_OBJECT")
        self.assertIn("ARCHIVE_HOLD",by["REF-P22"]["holds"])
        self.assertEqual(by["REF-P38"]["accessState"],"PARTIAL_OBJECT")

    def test_navigation_and_evidence_guard_claims(self):
        for file in ("README.md","SELF_PLAN.md","04_series_blueprint.md"):
            self.assertIn(CH.name,(D/file).read_text(encoding="utf-8"))
        l=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for i in range(274,282):self.assertIn("| C%d |"%i,l)
        s=CH.read_text(encoding="utf-8")
        for term in ("20 ноября 1541", "30 ноября", "2 января 1542",
                     "21 мая 1536", "10 августа 1535", "23 апреля 1538",
                     "гражданская власть","не", "первичных"):
            self.assertIn(term.lower(),s.lower())

if __name__=="__main__":
    unittest.main()
