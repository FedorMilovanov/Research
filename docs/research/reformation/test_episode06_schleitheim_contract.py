#!/usr/bin/env python3
"""Episode 06 manuscript, primary/secondary print and legal status regression checks."""
from pathlib import Path
import json
import unittest

D = Path(__file__).resolve().parent
CH = D / "episode06_schleitheim_1527_1529_manuscript.md"

class SchleitheimEpisodeTests(unittest.TestCase):
    def test_narrative_and_seven_articles(self):
        s=CH.read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# Эпизод 06."))
        self.assertGreaterEqual(len(s.split()), 1600)
        for part in ("Первое решение", "Вторая статья", "Третья статья", "Четвёртая статья",
                     "Пятая статья", "шестой статьёй", "Седьмая статья", "RESEARCH_MANUSCRIPT_DRAFT",
                     "PUBLICATION_HOLD", "Источниковедческий аппарат"):
            with self.subTest(part=part):
                self.assertIn(part.lower(),s.lower())
        self.assertIn("не проверены по оригинальным протоколам",s)

    def test_originals_separate_and_publication_hold(self):
        j=json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        by={x["id"]:x for x in j["sources"]}
        for id_ in ("REF-P10","REF-P11","REF-P12","REF-P24","REF-P24-BSB1",
                    "REF-P24-BSB2","REF-P57","REF-P59","REF-P61","REF-P13"):
            with self.subTest(id=id_):
                self.assertIn(id_,by)
                self.assertIn("PUBLICATION_HOLD",by[id_]["holds"])
        self.assertNotEqual(by["REF-P24-BSB1"]["url"],by["REF-P24-BSB2"]["url"])
        manuscript=CH.read_text(encoding="utf-8")
        for s in ("REF-P24-BSB1","REF-P24-BSB2","REF-P12","930–934","940–946"):
            self.assertIn(s,manuscript)

    def test_speyer_collective_consent_and_execution_boundary(self):
        chapter = CH.read_text(encoding="utf-8")
        reader, apparatus = chapter.split("## Источниковедческий аппарат", 1)
        ledger = (D / "03_claim_verification_register.md").read_text(encoding="utf-8")
        row = next(line for line in ledger.splitlines() if line.startswith("| C12 |"))
        packet = (D / "independent_review_packets.md").read_text(encoding="utf-8")
        for marker in ("Протестации 20 апреля", "против повторного крещения",
                       "не доказывает личного голосования", "конкретных казнях"):
            with self.subTest(reader=marker):
                self.assertIn(marker.lower(), reader.lower())
        for marker in ("REF-P11", "583–587", "widertauff", "ainig sein",
                       "PARTIAL_OBJECT"):
            with self.subTest(apparatus=marker):
                self.assertIn(marker, apparatus)
        for marker in ("COLLECTIVE_PROTESTATION_ANTI_REBAPTISM_CONSENT_TEXT_CHECKED",
                       "INDIVIDUAL_VOTE_NOT_PROVEN", "LOCAL_EXECUTION_HOLD",
                       "EVIDENCE_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(marker, row)
        self.assertIn("Bv 583–587", packet)
        self.assertIn("f.28r/f.28v", packet)

    def test_navigation_and_five_overclaims(self):
        for name in ("README.md","04_series_blueprint.md","SELF_PLAN.md",
                     "episode05_marburg_colloquy_1529_manuscript.md"):
            self.assertIn(CH.name,(D/name).read_text(encoding="utf-8"))
        ledger=(D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for i in range(257,262):
            self.assertIn("| C%d |" % i,ledger)
        self.assertIn("NOT_EDITORIAL_READY",(D/"SELF_PLAN.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
