#!/usr/bin/env python3
"""Book bridge and document-voice boundaries for Reformation episode 05."""
from pathlib import Path
import json
import unittest

D = Path(__file__).resolve().parent
EP05 = D / "episode05_marburg_colloquy_1529_manuscript.md"

class MarburgEpisodeTests(unittest.TestCase):
    def test_manuscript_exists_with_narrative_and_hold(self):
        s = EP05.read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# Эпизод 05."))
        self.assertGreater(len(s.split()), 1500)
        self.assertIn("RESEARCH_MANUSCRIPT_DRAFT", s)
        self.assertIn("PUBLICATION_HOLD", s)
        self.assertIn("Источниковедческий аппарат", s)
        for marker in ("статья 14", "Пятнадцатая статья", "Иоахиму Вадиану",
                       "Андреас Осиандер", "статьям **7, 13 и 15**"):
            self.assertIn(marker.lower(), s.lower())

    def test_undistorted_source_provenance_and_versions(self):
        j = json.loads((D/"source-registry-v1.json").read_text(encoding="utf-8"))
        src = {v["id"]:v for v in j["sources"]}
        for id_ in ("REF-P13", "REF-P13-ARCHIVE", "REF-P73", "REF-P74"):
            self.assertIn(id_, src)
            self.assertIn("PUBLICATION_HOLD", src[id_]["holds"])
        for id_ in ("REF-P73","REF-P74"):
            self.assertEqual(src[id_]["evidenceClass"], "A1")
            self.assertEqual(src[id_]["accessState"], "PARTIAL_OBJECT")
            self.assertIn("ARCHIVE_HOLD", src[id_]["holds"])
            self.assertEqual(src[id_]["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertEqual(src["REF-P13-ARCHIVE"]["accessState"],"CATALOG_ONLY")
        self.assertIn("article 9",src["REF-P13"]["verificationNote"].lower())

    def test_book_navigation_and_evidence_limits(self):
        for f in ("README.md","04_series_blueprint.md",
                  "episode03_luther_worms_1520_1521_manuscript.md",
                  "episode04_zurich_zwingli_1523_1525_manuscript.md","SELF_PLAN.md"):
            self.assertIn(EP05.name,(D/f).read_text(encoding="utf-8"))
        chapter = EP05.read_text(encoding="utf-8")
        self.assertIn("не просмотрен построчно", chapter)
        ledger = (D/"03_claim_verification_register.md").read_text(encoding="utf-8")
        for n in range(248,254):
            self.assertIn("| C%d |" % n, ledger)
        self.assertIn("NOT_EDITORIAL_READY", (D/"SELF_PLAN.md").read_text(encoding="utf-8"))
        self.assertIn("REF-P13-ARCHIVE", chapter)

if __name__ == "__main__":
    unittest.main()
