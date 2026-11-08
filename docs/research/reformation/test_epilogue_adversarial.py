#!/usr/bin/env python3
"""Regression checks for the scoped RF-THEO-EPI editorial pass.

These are structural controls; they cannot establish theological truth,
a Greek critical-text collation, or publication and reuse permissions.
"""
from pathlib import Path
import json
import re
import unittest

HERE = Path(__file__).resolve().parent
EPI = HERE / "epilogue_reformation_last_restoration_manuscript.md"
LEDGER = HERE / "03_claim_verification_register.md"
REGISTRY = HERE / "source-registry-v1.json"
PLAN = HERE / "SELF_PLAN.md"


class ReformationEpilogueAdversarialTests(unittest.TestCase):
    def test_premillennial_voice_retained_and_opposition_not_erased(self):
        text = EPI.read_text(encoding="utf-8")
        for fragment in (
            "принято премилленаристское прочтение",
            "ἔζησαν", "20:4–5", "1 Кор. 15:23–28",
            "рекапитуляц", "душ мучеников",
            "Постмилленаристское прочтение",
            "связывание сатаны",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment.lower(), text.lower())
        self.assertIn("## Источниковедческий и богословский аппарат", text)
        self.assertIn("adversarial-матрица", text)

    def test_epilogue_remains_research_only(self):
        text = EPI.read_text(encoding="utf-8")
        for marker in ("RESEARCH_MANUSCRIPT_DRAFT", "NOT_EDITORIAL_READY",
                       "PUBLICATION_HOLD", "EXEGESIS_HOLD",
                       "ORIGINAL_GREEK_HOLD", "RIGHTS_HOLD"):
            self.assertIn(marker, text)
        self.assertIn("не сопоставлены", text)
        self.assertIn("не приравниваются", text)

    def test_opposing_secondary_sources_are_registered_fail_closed(self):
        sources = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(sources["sourceCount"], len(sources["sources"]))
        mapped = {row["id"]: row for row in sources["sources"]}
        for source_id in ("REF-S94", "REF-S95"):
            with self.subTest(source_id=source_id):
                row = mapped[source_id]
                self.assertEqual(row["evidenceClass"], "B1")
                self.assertEqual(row["accessState"], "PARTIAL_OBJECT")
                self.assertEqual(row["publicationState"], "REFERENCE")
                self.assertIn("PUBLICATION_HOLD", row["holds"])
                self.assertIn("RIGHTS_HOLD", row["holds"])
                self.assertIn("ARCHIVE_HOLD", row["holds"])
                self.assertIn(source_id, EPI.read_text(encoding="utf-8"))

    def test_existing_claim_ids_and_single_plan_preserved(self):
        ledger = LEDGER.read_text(encoding="utf-8")
        claim_lines = [line for line in ledger.splitlines()
                       if line.startswith("| C")
                       and line.split(" |", 1)[0][3:].isdigit()]
        ids = [int(line.split(" |", 1)[0][3:]) for line in claim_lines]
        self.assertEqual(ids, list(range(1, 320)))
        c316 = next(s for s in claim_lines if s.startswith("| C316 |"))
        for mark in ("REF-P82", "REF-S94", "REF-S95",
                     "REJECTED_FORMULATION", "PUBLICATION_HOLD"):
            self.assertIn(mark, c316)
        plan = PLAN.read_text(encoding="utf-8")
        self.assertIn("волна 383", plan)
        self.assertIn("RF-EDIT-04-06", plan)
        self.assertIn("PUBLICATION_HOLD", plan)


if __name__ == "__main__":
    unittest.main()
