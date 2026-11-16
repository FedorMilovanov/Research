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

    def test_epilogue_starts_with_theology_and_keeps_reader_limits_in_apparatus(self):
        """Theological alternatives and evidence restrictions are kept, not hidden."""
        content = EPI.read_text(encoding="utf-8")
        reader, apparatus = content.split(
            "## Источниковедческий и богословский аппарат", 1
        )
        self.assertIn("## Чего не смогла завершить Реформация", reader)
        self.assertNotIn("**Статус:**", reader)
        self.assertIn("**Статус:** RESEARCH_MANUSCRIPT_DRAFT", apparatus)
        self.assertIn("Это отдельный **богословский эпилог**", apparatus)
        self.assertIn("премилленаристском прочтении", apparatus)
        for status in ("NOT_EDITORIAL_READY", "PUBLICATION_HOLD",
                       "EXEGESIS_HOLD", "ORIGINAL_GREEK_HOLD", "RIGHTS_HOLD"):
            self.assertIn(status, apparatus)

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

    def test_wave443_greek_edition_does_not_become_manuscript_or_review(self):
        """Modern Greek critical edition establishes precise lemmas, but
        cannot itself establish a millennium chronology or manuscript history."""
        content = EPI.read_text(encoding="utf-8")
        reader, apparatus = content.split(
            "## Источниковедческий и богословский аппарат", 1
        )
        self.assertNotIn("небесное оправдание", reader.lower())
        self.assertIn("небесная жизнь и царствование душ мучеников", reader.lower())
        self.assertIn("принято премилленаристское прочтение", reader)
        for phrase in (
            "REF-P88", "SBLGNT", "MODERN_EDITED_GREEK_TEXT_CHECKED",
        ):
            if phrase == "MODERN_EDITED_GREEK_TEXT_CHECKED":
                self.assertIn(phrase, LEDGER.read_text(encoding="utf-8"))
            else:
                self.assertIn(phrase, apparatus)
        for word in (
            "καὶ ἔζησαν καὶ ἐβασίλευσαν",
            "οἱ λοιποὶ τῶν νεκρῶν οὐκ ἔζησαν",
            "τὰς ψυχὰς τῶν πεπελεκισμένων",
            "ἔπειτα", "εἶτα τὸ τέλος",
            "не сверены", "ARCHIVE_HOLD", "EVIDENCE_HOLD",
            "RIGHTS_HOLD", "PUBLICATION_HOLD",
        ):
            with self.subTest(word=word):
                self.assertIn(word, apparatus)
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        src = {x["id"]: x for x in registry["sources"]}["REF-P88"]
        self.assertEqual(src["accessState"], "PARTIAL_OBJECT")
        self.assertEqual(src["locatorState"], "EXACT_LOCATOR_VERIFIED")
        self.assertEqual(src["rightsState"], "RIGHTS_UNKNOWN")
        self.assertTrue(set(("EVIDENCE_HOLD", "ARCHIVE_HOLD",
                             "RIGHTS_HOLD", "PUBLICATION_HOLD")).issubset(src["holds"]))
        self.assertIn("NOT ANCIENT MANUSCRIPT", src["verificationNote"])
        c316 = next(x for x in LEDGER.read_text(encoding="utf-8").splitlines()
                    if x.startswith("| C316 |"))
        self.assertIn("REF-P88", c316)
        self.assertIn("ANCIENT_GREEK_WITNESS_HOLD", c316)

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
        # Plans advance; the editorial evidence and successor remain traceable.
        self.assertIn("RF-THEO-EPI", plan)
        self.assertIn("RF-EDIT-04-06", plan)
        self.assertIn("PUBLICATION_HOLD", plan)


if __name__ == "__main__":
    unittest.main()
