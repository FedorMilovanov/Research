#!/usr/bin/env python3
"""Fail-closed source-critical regression guards for Reformation episode 03."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_SOURCES = ("REF-P63", "REF-P64", "REF-P65", "REF-P66", "REF-S70", "REF-S71", "REF-S72")


class Episode03HistoricalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        cls.rows = {r["id"]: r for r in cls.registry["sources"]}
        cls.claims = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        cls.manuscript = (HERE / "episode03_luther_worms_1520_1521_manuscript.md").read_text(encoding="utf-8")

    def test_exact_new_source_set_and_no_publication_release(self):
        for id_ in EXPECTED_SOURCES:
            with self.subTest(source=id_):
                self.assertIn(id_, self.rows)
                row = self.rows[id_]
                self.assertEqual(row["publicationState"], "REFERENCE")
                self.assertIn("PUBLICATION_HOLD", row["holds"])
                self.assertIn("RIGHTS_HOLD", row["holds"])
                self.assertTrue(row["verificationNote"])
        self.assertEqual(self.registry["sourceCount"], len(self.registry["sources"]))

    def test_1520_prints_are_not_misrepresented_as_fully_collated(self):
        for id_ in ("REF-P63", "REF-P64", "REF-P66"):
            with self.subTest(source=id_):
                self.assertEqual(self.rows[id_]["accessState"], "CATALOG_ONLY")
                self.assertIn("ARCHIVE_HOLD", self.rows[id_]["holds"])
        self.assertEqual(self.rows["REF-P65"]["accessState"], "PARTIAL_OBJECT")
        self.assertIn("ARCHIVE_HOLD", self.rows["REF-P65"]["holds"])
        self.assertIn("final leaf", self.rows["REF-P63"]["verificationNote"])
        self.assertIn("FOURTH printing", self.rows["REF-P66"]["verificationNote"])

    def test_nine_following_claims_are_present_and_evidenced(self):
        for number in range(227, 236):
            matches = re.findall(r"^\| C" + str(number) + r" \|(.+)$",
                                 self.claims, re.MULTILINE)
            with self.subTest(claim=number):
                self.assertEqual(len(matches), 1)
                self.assertIn("REF-", matches[0])
                self.assertIn("PUBLICATION_HOLD", matches[0])
        self.assertIn("REF-S72", self.claims)

    def test_publication_hold_and_precise_edict_dates(self):
        text = self.manuscript
        self.assertTrue(text.startswith("# Эпизод 03."))
        self.assertIn("RESEARCH_MANUSCRIPT_DRAFT / PUBLICATION_HOLD", text)
        for expected in ("8 мая", "12 мая", "25 мая", "26 мая",
                         "15 июня", "3 января", "VD16 L3759", "VD16 L4189",
                         "REG. E 81", "REF-P63", "REF-S72"):
            if expected == "REG. E 81":
                self.assertIn("Reg. E 81", text)
            else:
                self.assertIn(expected, text)
        self.assertGreaterEqual(len(text.split()), 2500)


if __name__ == "__main__":
    unittest.main()
