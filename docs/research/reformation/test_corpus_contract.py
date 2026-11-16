#!/usr/bin/env python3
"""Regression checks for the Reformation evidence contract (read-only)."""
from __future__ import annotations

import copy
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_corpus as corpus


HERE = Path(__file__).resolve().parent


class ReformationContractTests(unittest.TestCase):
    def test_current_corpus_integrity(self):
        errors, stats = corpus.validate()
        self.assertEqual(errors, [])
        # The previous 147/226 thresholds were from an obsolete wave and
        # could allow accidental loss of 42 sources and 89 claim rows.
        # Pin the confirmed manuscript + epilogue candidate floor; any intentional retirement needs an
        # explicit reviewed baseline change rather than silent attrition.
        self.assertGreaterEqual(stats["sources"], 193)
        self.assertGreaterEqual(stats["claims"], 319)

    def test_original_ledger_lf_crlf_and_tampering(self):
        data = (HERE / "source-ledger-2026-11-03-original.md").read_bytes()
        normalized = data.replace(b"\r\n", b"\n")
        self.assertEqual(corpus.canonical_ledger_blob_sha(normalized),
                         corpus.EXPECTED_ORIGINAL_GIT_BLOB)
        self.assertEqual(corpus.canonical_ledger_blob_sha(
            normalized.replace(b"\n", b"\r\n")),
            corpus.EXPECTED_ORIGINAL_GIT_BLOB)
        self.assertNotEqual(corpus.canonical_ledger_blob_sha(
            normalized + b"\nUNAUDITED CHANGE\n"),
            corpus.EXPECTED_ORIGINAL_GIT_BLOB)

    def test_invalid_source_status_fails_closed(self):
        original = corpus.json_read

        def tampered(path):
            result = original(path)
            if path.name == "source-registry-v1.json":
                result = copy.deepcopy(result)
                result["sources"][0]["accessState"] = "UNVERIFIED_CUSTOM_ENUM"
            return result

        with patch.object(corpus, "json_read", side_effect=tampered):
            errors, _ = corpus.validate()
        self.assertTrue(any("invalid accessState" in e for e in errors), errors)

    def test_full_primary_archive_conflict_fails_closed(self):
        original = corpus.json_read

        def tampered(path):
            result = original(path)
            if path.name == "source-registry-v1.json":
                result = copy.deepcopy(result)
                source = next(x for x in result["sources"] if x["id"] == "REF-P62")
                source["holds"].append("ARCHIVE_HOLD")
            return result

        with patch.object(corpus, "json_read", side_effect=tampered):
            errors, _ = corpus.validate()
        self.assertTrue(any("REF-P62: full primary object with ARCHIVE_HOLD" in e
                            for e in errors), errors)

    def test_secondary_full_access_does_not_erase_primary_hold(self):
        rows = corpus.json_read(HERE / "source-registry-v1.json")["sources"]
        for source_id in ("REF-S18", "REF-S22", "REF-S29", "REF-S30"):
            row = next(x for x in rows if x["id"] == source_id)
            self.assertEqual(row["evidenceClass"], "B1")
            self.assertEqual(row["accessState"], "FULL_OBJECT_VERIFIED")
            self.assertIn("ARCHIVE_HOLD", row["holds"])
            self.assertIn("PUBLICATION_HOLD", row["holds"])


if __name__ == "__main__":
    unittest.main()
