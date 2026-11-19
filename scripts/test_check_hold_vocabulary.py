#!/usr/bin/env python3
"""Offline tests for scripts/check_hold_vocabulary.py.

The checker guards a proposal, not a rewrite. Its contract: coverage is total
in both directions (no unmapped spelling, no stale mapping), counts equal the
inventory, axis proposals only name values that exist in policy v2, canonical
proposals only name canonical flags, and the proposal may never stop being
`PROPOSAL_ONLY`.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_hold_vocabulary as chv

POLICY = {
    "holds": ["EVIDENCE_HOLD", "LOCATOR_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"],
    "accessStates": ["FULL_OBJECT_VERIFIED", "PARTIAL_OBJECT", "NOT_ACQUIRED"],
    "locatorStates": ["EXACT_LOCATOR_VERIFIED", "COARSE_LOCATOR_ONLY"],
    "rightsStates": ["PRIVATE_STUDY_ONLY", "RIGHTS_UNKNOWN"],
    "publicationStates": ["PROMOTE", "REFERENCE", "BLOCKED"],
}


def inventory(*values: str) -> dict:
    return {"jsonHolds": [{"path": "corpus/data/x.json", "pointer": "/a/0/holds", "values": list(values)}]}


def entry(value: str, cls: str, target: str, count: int = 1) -> dict:
    return {
        "value": value,
        "count": count,
        "files": ["corpus/data/x.json"],
        "class": cls,
        "proposedRepresentation": target,
        "justification": "test",
    }


def proposal(*entries: dict, status: str = "PROPOSAL_ONLY") -> dict:
    return {
        "status": status,
        "counts": {"spellings": len(entries), "byClass": {}},
        "values": list(entries),
    }


class CoverageTests(unittest.TestCase):
    def test_complete_mapping_passes(self) -> None:
        inv = inventory("PRIVATE_STUDY_ONLY", "QUOTE_RISK")
        prop = proposal(
            entry("PRIVATE_STUDY_ONLY", "axis", "rightsState=PRIVATE_STUDY_ONLY"),
            entry("QUOTE_RISK", "canonical", "PUBLICATION_HOLD"),
        )
        self.assertEqual(chv.check(inv, POLICY, prop), [])

    def test_unmapped_spelling_fails(self) -> None:
        inv = inventory("PRIVATE_STUDY_ONLY", "MYSTERY_HOLD")
        prop = proposal(entry("PRIVATE_STUDY_ONLY", "axis", "rightsState=PRIVATE_STUDY_ONLY"))
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("unmapped spelling" in p for p in problems), problems)

    def test_stale_mapping_fails(self) -> None:
        inv = inventory("PRIVATE_STUDY_ONLY")
        prop = proposal(
            entry("PRIVATE_STUDY_ONLY", "axis", "rightsState=PRIVATE_STUDY_ONLY"),
            entry("GONE_HOLD", "canonical", "EVIDENCE_HOLD"),
        )
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("stale mapping" in p for p in problems), problems)

    def test_canonical_values_are_not_mapped(self) -> None:
        inv = inventory("EVIDENCE_HOLD")
        prop = proposal()
        self.assertEqual(chv.check(inv, POLICY, prop), [])


class VocabularyTests(unittest.TestCase):
    def test_unknown_axis_value_fails(self) -> None:
        inv = inventory("PRIVATE_STUDY_ONLY")
        prop = proposal(entry("PRIVATE_STUDY_ONLY", "axis", "rightsState=MADE_UP_STATE"))
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("is not a value of rightsStates" in p for p in problems), problems)

    def test_unknown_canonical_flag_fails(self) -> None:
        inv = inventory("SOME_HOLD")
        prop = proposal(entry("SOME_HOLD", "canonical", "PROOF_HOLD"))
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("not a canonical flag" in p for p in problems), problems)

    def test_unknown_class_fails(self) -> None:
        inv = inventory("SOME_HOLD")
        prop = proposal(entry("SOME_HOLD", "invented", "EVIDENCE_HOLD"))
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("unknown class" in p for p in problems), problems)

    def test_missing_justification_fails(self) -> None:
        inv = inventory("SOME_HOLD")
        bad = entry("SOME_HOLD", "canonical", "EVIDENCE_HOLD")
        bad["justification"] = "  "
        problems = chv.check(inv, POLICY, proposal(bad))
        self.assertTrue(any("missing justification" in p for p in problems), problems)


class CountTests(unittest.TestCase):
    def test_count_drift_fails(self) -> None:
        inv = inventory("QUOTE_RISK", "QUOTE_RISK")
        prop = proposal(entry("QUOTE_RISK", "canonical", "PUBLICATION_HOLD", count=1))
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("count" in p for p in problems), problems)

    def test_file_drift_fails(self) -> None:
        inv = inventory("QUOTE_RISK")
        bad = entry("QUOTE_RISK", "canonical", "PUBLICATION_HOLD")
        bad["files"] = ["somewhere/else.json"]
        problems = chv.check(inv, POLICY, proposal(bad))
        self.assertTrue(any("file list drifted" in p for p in problems), problems)

    def test_spelling_count_drift_fails(self) -> None:
        inv = inventory("QUOTE_RISK")
        prop = proposal(entry("QUOTE_RISK", "canonical", "PUBLICATION_HOLD"))
        prop["counts"]["spellings"] = 7
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("counts.spellings" in p for p in problems), problems)


class DisciplineTests(unittest.TestCase):
    def test_proposal_must_stay_proposal_only(self) -> None:
        inv = inventory("QUOTE_RISK")
        prop = proposal(entry("QUOTE_RISK", "canonical", "PUBLICATION_HOLD"), status="APPLIED")
        problems = chv.check(inv, POLICY, prop)
        self.assertTrue(any("PROPOSAL_ONLY" in p for p in problems), problems)

    def test_render_lists_every_spelling(self) -> None:
        inv = inventory("A_HOLD", "B_HOLD")
        prop = proposal(
            entry("A_HOLD", "canonical", "EVIDENCE_HOLD"),
            entry("B_HOLD", "status", "no hold"),
        )
        table = chv.render(prop)
        self.assertIn("`A_HOLD`", table)
        self.assertIn("`B_HOLD`", table)
        self.assertEqual(chv.check(inv, POLICY, prop), [])


class RegisterBlockTests(unittest.TestCase):
    """The register used to retype these two tables by hand; it may not any more."""

    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.register = Path(self._dir.name) / "register.md"
        self.prop = proposal(
            entry("QUOTE_RISK", "canonical", "PUBLICATION_HOLD"),
            entry("PRIVATE_STUDY_ONLY", "axis", "rightsState=PRIVATE_STUDY_ONLY"),
        )
        self.prop["counts"]["byClass"] = {"canonical": 1, "axis": 1}
        self.register.write_text(
            "# Реестр\n\n" + chv.CLASS_BEGIN + "\n" + chv.CLASS_END + "\n\n"
            + chv.VALUES_BEGIN + "\n" + chv.VALUES_END + "\n", encoding="utf-8")

    def tearDown(self) -> None:
        self._dir.cleanup()

    def test_empty_blocks_are_reported_as_drift_then_written(self) -> None:
        self.assertTrue(chv.register_problems(self.register, self.prop))
        self.assertTrue(chv.write_register(self.register, self.prop))
        self.assertEqual(chv.register_problems(self.register, self.prop), [])

    def test_write_is_idempotent(self) -> None:
        chv.write_register(self.register, self.prop)
        self.assertFalse(chv.write_register(self.register, self.prop))

    def test_hand_edited_count_is_a_drift(self) -> None:
        chv.write_register(self.register, self.prop)
        text = self.register.read_text(encoding="utf-8").replace("| `canonical` | 1 |", "| `canonical` | 2 |")
        self.register.write_text(text, encoding="utf-8")
        problems = chv.register_problems(self.register, self.prop)
        self.assertTrue(any("hold-classes" in p for p in problems), problems)

    def test_missing_markers_are_reported(self) -> None:
        self.register.write_text("# Реестр без таблиц\n", encoding="utf-8")
        problems = chv.register_problems(self.register, self.prop)
        self.assertEqual(len(problems), 2)


if __name__ == "__main__":
    unittest.main()
