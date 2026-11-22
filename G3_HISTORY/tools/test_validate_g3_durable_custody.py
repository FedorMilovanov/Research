#!/usr/bin/env python3
"""Negative tests for the bounded G3 Actions custody/assessment partition."""
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

import validate_g3_durable_custody as validator


class ActionsAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = validator.EXPIRY_COHORT_ASSESSMENT.read_text(encoding="utf-8")
        cls.receipt = json.loads(validator.PRESERVATION_RECEIPT.read_text(encoding="utf-8"))
        cls.receipt_ids = {
            row["githubActionsArtifactId"] for row in cls.receipt["artifacts"]
        }

    def validate(self, text: str) -> tuple[int, list[str]]:
        errors: list[str] = []
        count = validator.validate_actions_assessment_text(text, self.receipt_ids, errors)
        return count, errors

    def test_current_assessment_partitions_receipt_and_unpreserved_rows(self) -> None:
        count, errors = self.validate(self.text)
        self.assertEqual(errors, [])
        self.assertEqual(count, 30)
        self.assertEqual(len(self.receipt_ids), 8)

    def test_missing_unpreserved_row_is_rejected(self) -> None:
        rows = [
            line for line in self.text.splitlines()
            if re.match(r"^\|\s*[^|]+\|\s*`\d+`\s*\|\s*`g3-", line)
        ]
        self.assertEqual(len(rows), 30)
        count, errors = self.validate(self.text.replace(rows[-1] + "\n", "", 1))
        self.assertEqual(count, 29)
        self.assertTrue(any("exactly 30 unique" in error for error in errors))
        self.assertTrue(any("exact 38-item" in error for error in errors))

    def test_receipt_id_cannot_be_reclassified_as_unpreserved(self) -> None:
        first_unpreserved = re.search(
            r"(^\|\s*[^|]+\|\s*`)(\d+)(`\s*\|\s*`g3-)", self.text, flags=re.M
        )
        self.assertIsNotNone(first_unpreserved)
        covered_id = min(self.receipt_ids)
        mutated = (
            self.text[: first_unpreserved.start(2)]
            + str(covered_id)
            + self.text[first_unpreserved.end(2) :]
        )
        _, errors = self.validate(mutated)
        self.assertTrue(any("marks receipt-covered IDs unpreserved" in error for error in errors))

    def test_mandatory_boundary_hold_cannot_disappear(self) -> None:
        boundary = self.text.index("## Boundary retained")
        mutated = self.text[:boundary] + self.text[boundary:].replace("`PUBLICATION_HOLD`, ", "", 1)
        _, errors = self.validate(mutated)
        self.assertIn("G3 Actions expiry assessment boundary lost PUBLICATION_HOLD", errors)

    def test_hcr36_counts_and_digest_are_derived_from_canonical_evidence(self) -> None:
        registry = json.loads(
            (validator.REPO / "data" / "hold-closure-registry-v1.json").read_text(encoding="utf-8")
        )
        closure = next(
            row for row in registry["closures"] if row["id"] == "HCR-2026-11-18-36"
        )
        obj = closure["objects"][0]
        source_digest = hashlib.sha256(validator.PRESERVATION_SOURCE_MANIFEST.read_bytes()).hexdigest()
        unpreserved_count, errors = self.validate(self.text)

        self.assertEqual(errors, [])
        self.assertEqual(obj["sourcePathsImported"], 0)
        self.assertEqual(obj["boundedCohortArtifacts"], len(self.receipt_ids) + unpreserved_count)
        self.assertEqual(obj["durablyPreservedOriginalZips"], len(self.receipt_ids))
        self.assertEqual(obj["explicitlyUnpreservedArtifacts"], unpreserved_count)
        self.assertEqual(
            obj["preservedDestinationBytes"],
            sum(row["destinationBytes"] for row in self.receipt["artifacts"]),
        )
        self.assertEqual(obj["sourceManifestSha256"], source_digest)
        self.assertEqual(
            set(closure["residualHolds"]),
            {"ARCHIVE_HOLD", "EVIDENCE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"},
        )


if __name__ == "__main__":
    unittest.main()
