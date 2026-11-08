#!/usr/bin/env python3
"""Read-only targeted source-provenance regression: Marburg 1529 and Luther 1525.

Verifies registry provenance, manuscript-level historical distinctions, and
publication holds; never claims facsimile or independent peer review approval.
"""
from pathlib import Path
import json
import unittest

HERE = Path(__file__).resolve().parent


class MarburgLutherSourceGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.marburg = (HERE / "episode05_marburg_colloquy_1529_manuscript.md").read_text(encoding="utf-8")
        cls.luther = (HERE / "episode07_luther_peasants_war_1524_1525_manuscript.md").read_text(encoding="utf-8")
        registry = json.loads((HERE / "source-registry-v1.json").read_text(encoding="utf-8"))
        cls.n = registry["sourceCount"]
        cls.sources = {entry["id"]: entry for entry in registry["sources"]}
        cls.all_sources = registry["sources"]

    def test_exact_new_evidence_count_and_ids(self):
        self.assertEqual(self.n, 197)
        self.assertEqual(len(self.all_sources), self.n)
        self.assertEqual(len(self.sources), self.n)
        for key in ("REF-P13", "REF-P13-ARCHIVE", "REF-P75",
                    "REF-P85", "REF-S96", "REF-P07-WIT"):
            self.assertIn(key, self.sources)

    def test_original_manuscripts_and_print_remain_closed(self):
        for key in ("REF-P13-ARCHIVE", "REF-P75", "REF-P07-WIT"):
            with self.subTest(key=key):
                row = self.sources[key]
                self.assertEqual(row["accessState"], "CATALOG_ONLY")
                self.assertIn("ARCHIVE_HOLD", row["holds"])
                self.assertIn("PUBLICATION_HOLD", row["holds"])
        for key in ("REF-P85", "REF-S96"):
            with self.subTest(key=key):
                row = self.sources[key]
                self.assertEqual(row["accessState"], "PARTIAL_OBJECT")
                self.assertIn("RIGHTS_HOLD", row["holds"])
                self.assertIn("PUBLICATION_HOLD", row["holds"])
        self.assertEqual(self.sources["REF-P85"]["evidenceClass"], "A1")
        self.assertEqual(self.sources["REF-S96"]["evidenceClass"], "B1")

    def test_marburg_confessional_content_and_limits(self):
        for marker in ("REF-P85", "HAPuls", "Oberman", "28:19",
                       "§14", "§15", "7, 13 и 15", "60r–64v",
                       "ORIGINAL_GERMAN_HOLD", "ARCHIVE_HOLD"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.marburg.lower())
        self.assertIn("не были получены и визуально прочитаны", self.marburg)

    def test_luther_composition_vs_first_paired_impression(self):
        for marker in ("REF-S96", "Томас Кауфман", "16 апреля",
                       "составной", "VD16 L4692", "VD16 L4690",
                       "VD16 L4693", "CATALOG_ONLY", "RIGHTS_HOLD"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.luther.lower())
        self.assertIn("гипотезу", self.luther.lower())
        self.assertIn("Два авторских текста", self.luther)

    def test_existing_claims_and_plan_unapproved(self):
        ledger = (HERE / "03_claim_verification_register.md").read_text(encoding="utf-8")
        for ident in ("C10", "C60"):
            self.assertIn("| " + ident + " |", ledger)
        self.assertIn("ORIGINAL_ZK_COLLATION_HOLD", ledger)
        self.assertIn("COMPOSITION_DATING_CONTESTED", ledger)
        plan = (HERE / "SELF_PLAN.md").read_text(encoding="utf-8")
        for key in ("волна 388", "RF-EXTERNAL-REVIEW-GATES",
                    "INDEPENDENT_EXTERNAL_REVIEW_OPEN", "THEOLOGICAL_PEER_REVIEW_OPEN",
                    "PUBLICATION_HOLD", "STOP_DISCOVERY"):
            self.assertIn(key, plan)


if __name__ == "__main__":
    unittest.main()
