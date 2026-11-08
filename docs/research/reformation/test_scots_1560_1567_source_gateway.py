#!/usr/bin/env python3
"""Read-only Scottish RPS 1560/1567 textual-history and archive boundary checks.

Access to a modern edited English text never asserts that the lost 1560
original manuscript or early Scottish printed leaves have been collated.
"""
from pathlib import Path
import json
import unittest

HERE = Path(__file__).resolve().parent


class ScottishSourceGatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ch = (HERE / "episode10_england_scotland_1534_1581_manuscript.md").read_text(encoding="utf-8")
        cls.dossier = (HERE / "08_schleitheim_bsb_scots_primary_collation.md").read_text(encoding="utf-8")
        cls.sources = {
            row["id"]: row for row in json.loads(
                (HERE / "source-registry-v1.json").read_text(encoding="utf-8")
            )["sources"]
        }

    def test_recovered_research_edition_is_not_autograph(self):
        r = self.sources["REF-P25-RPS"]
        self.assertEqual(r["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(r["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertIn("maryi_trans", r["url"])
        self.assertIn("ORIGINAL CONFESSION MANUSCRIPT IS LOST", r["verificationNote"])
        for hold in ("ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"):
            self.assertIn(hold, r["holds"])
        self.assertEqual(r["publicationState"], "REFERENCE")

    def test_1560_witnesses_and_17_august_approval_separated(self):
        for marker in ("17.08.1560", "Skene 1597", "ff.3r–9v",
                       "PRO SP52/05", "Lekpreuik 1568",
                       "не содержит всех", "рукопись"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.ch.lower())
        self.assertIn("королевской санкции", self.ch)
        self.assertIn("утрачена", self.ch)

    def test_1567_is_another_editorial_source_and_numbering(self):
        other = self.sources["REF-P25-1567"]
        self.assertEqual(other["accessState"], "PARTIAL_OBJECT")
        self.assertIn("Lekpreuik 1568", other["verificationNote"])
        self.assertIn("skipped numeral 13", other["verificationNote"].lower())
        for marker in ("13 пропущен", "25 заголовков", "Sic.", "A1567/12/3"):
            self.assertIn(marker.lower(), self.ch.lower())
        self.assertIn("непосредственное чтение", self.dossier.lower())

    def test_original_language_and_rights_hold_remain(self):
        self.assertIn("PARTIAL_OBJECT / EXACT_LOCATOR_VERIFIED", self.dossier)
        self.assertIn("ORIGINAL_MANUSCRIPT_LOST", self.dossier)
        self.assertIn("ARCHIVE_HOLD", self.dossier)
        self.assertIn("RIGHTS_HOLD", self.dossier)
        self.assertIn("PUBLICATION_HOLD", self.dossier)
        ledger = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        self.assertIn("| C288 |", ledger)
        self.assertIn("ORIGINAL_MANUSCRIPT_LOST", ledger)


if __name__ == "__main__":
    unittest.main()
