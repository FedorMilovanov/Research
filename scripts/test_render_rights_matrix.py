#!/usr/bin/env python3
"""Offline and negative tests for the proposal-only rights matrix."""
from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

import render_rights_matrix as matrix


class RightsMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = matrix.load()

    def problems(self, mutate) -> list[str]:
        payload = copy.deepcopy(self.current)
        mutate(payload)
        return matrix.validate(payload)

    def test_current_matrix_matches_current_registry_selection(self) -> None:
        self.assertEqual(matrix.validate(copy.deepcopy(self.current)), [])
        self.assertEqual(matrix.expected_ids(), {row["id"] for row in self.current["entries"]})

    def test_markdown_is_generated_exactly_from_json(self) -> None:
        self.assertEqual(
            matrix.OUT.read_text(encoding="utf-8"),
            matrix.render(self.current),
        )

    def test_authority_role_cannot_be_promoted(self) -> None:
        problems = self.problems(lambda payload: payload.__setitem__("role", "AUTHORITY"))
        self.assertTrue(any("PROPOSAL_NOT_AUTHORITY" in problem for problem in problems))

    def test_entry_cannot_disappear_from_the_exact_current_set(self) -> None:
        problems = self.problems(lambda payload: payload["entries"].pop())
        self.assertTrue(any("набор id разошёлся" in problem for problem in problems))

    def test_entry_cannot_acquire_a_rights_decision(self) -> None:
        def mutate(payload: dict) -> None:
            payload["entries"][0]["rightsBasis"] = "invented"

        problems = self.problems(mutate)
        self.assertTrue(any("объявляют правовой эффект" in problem for problem in problems))

    def test_dated_observation_cannot_be_presented_as_current(self) -> None:
        def mutate(payload: dict) -> None:
            payload["boundaries"] = [
                value for value in payload["boundaries"]
                if "не являются текущим сетевым ответом" not in value
            ]

        problems = self.problems(mutate)
        self.assertTrue(any("текущим сетевым ответом" in problem for problem in problems))

    def test_external_observation_date_cannot_drift(self) -> None:
        def mutate(payload: dict) -> None:
            payload["digitizerCheck"]["upstream"]["checkedAt"] = "2026-11-19"

        problems = self.problems(mutate)
        self.assertTrue(any("исходную дату" in problem for problem in problems))

    def test_recorded_state_is_checked_against_source_registry(self) -> None:
        def mutate(payload: dict) -> None:
            payload["entries"][0]["recordedRightsState"] = "PUBLIC_DOMAIN"

        problems = self.problems(mutate)
        self.assertTrue(any("не совпадает с реестром" in problem for problem in problems))

    def test_rejected_inventory_is_not_a_runtime_dependency(self) -> None:
        source = Path(matrix.__file__).read_text(encoding="utf-8")
        self.assertNotIn("render_hold_inventory", source)
        self.assertNotIn("docs/research/holds/HOLD_INVENTORY", source)

    def test_hcr38_is_derived_from_the_proposal_artifact(self) -> None:
        registry = json.loads(
            (matrix.ROOT / "data" / "hold-closure-registry-v1.json").read_text(encoding="utf-8")
        )
        closure = next(
            row for row in registry["closures"] if row["id"] == "HCR-2026-11-18-38"
        )
        obj = closure["objects"][0]
        self.assertEqual(obj["currentSelectionEntries"], len(self.current["entries"]))
        self.assertEqual(
            obj["currentDataSha256"],
            hashlib.sha256(matrix.DATA.read_bytes()).hexdigest(),
        )
        self.assertEqual(obj["role"], self.current["role"])
        self.assertFalse(obj["sourceScriptImportedVerbatim"])
        self.assertEqual(
            set(closure["residualHolds"]),
            {"RIGHTS_HOLD", "PUBLICATION_HOLD"},
        )


if __name__ == "__main__":
    unittest.main()
