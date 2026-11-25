#!/usr/bin/env python3
"""Offline negative tests for the ED-09 editorial archive receipt gate."""

from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

import check_charnock_editorial_receipt as receipt


class ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(receipt.RECEIPT.read_text(encoding="utf-8"))

    def test_committed_receipt_passes_offline(self) -> None:
        self.assertEqual(receipt.validate_receipt(self.data), [])

    def test_bounded_source_paths_are_unique_and_globally_sorted(self) -> None:
        names = [path.as_posix() for path in receipt.SOURCE_PATHS]
        self.assertEqual(len(names), 17)
        self.assertEqual(len(set(names)), 17)
        self.assertEqual(names, sorted(names))
        self.assertEqual(sum("/manuscripts/" in name for name in names), 10)

    def test_destination_must_equal_the_reconstructed_carrier(self) -> None:
        drift = copy.deepcopy(self.data)
        drift["destinationBytesReadback"] += 1
        drift["destinationSha256Readback"] = "0" * 64
        errors = receipt.validate_receipt(drift)
        self.assertTrue(any("destinationBytesReadback" in error for error in errors))
        self.assertTrue(any("destinationSha256Readback расходится" in error for error in errors))

    def test_rights_publication_and_review_boundaries_are_gated(self) -> None:
        drift = copy.deepcopy(self.data)
        drift["rightsState"] = "CLEARED"
        drift["publicationState"] = "PROMOTE"
        drift["independentTranslationReview"] = "12/12"
        errors = receipt.validate_receipt(drift)
        self.assertTrue(any("rightsState" in error for error in errors))
        self.assertTrue(any("publicationState" in error for error in errors))
        self.assertTrue(any("independentTranslationReview" in error for error in errors))

    def test_malformed_json_is_reported_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "receipt.json"
            path.write_text("{broken", encoding="utf-8")
            data, errors = receipt.load_receipt(path)
        self.assertIsNone(data)
        self.assertTrue(errors)
        self.assertIn("не читается", errors[0])

    def test_archive_builder_is_deterministic_and_self_describing(self) -> None:
        rows = {"a.txt": b"alpha\n", "b.txt": b"beta\n"}
        manifest = receipt.build_manifest("a" * 40, rows)
        first = receipt.build_archive(manifest, rows)
        second = receipt.build_archive(manifest, rows)
        self.assertEqual(first, second)
        with zipfile.ZipFile(io.BytesIO(first)) as archive:
            self.assertEqual(archive.namelist(), ["a.txt", "b.txt", "SOURCE_MANIFEST.json"])
            self.assertEqual(json.loads(archive.read("SOURCE_MANIFEST.json")), manifest)
            self.assertEqual(archive.read("a.txt"), rows["a.txt"])
        self.assertEqual(
            manifest["files"]["a.txt"]["sha256"],
            hashlib.sha256(rows["a.txt"]).hexdigest(),
        )

    def test_missing_source_commit_fails_closed(self) -> None:
        drift = copy.deepcopy(self.data)
        drift["sourceGitSha"] = "0" * 40
        errors = receipt.validate_git_source(drift)
        self.assertTrue(errors)
        self.assertTrue(any("не читается" in error for error in errors))

    def test_exact_source_commit_reconstructs_when_object_is_available(self) -> None:
        commit = self.data["sourceGitSha"]
        probe = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=receipt.ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if probe.returncode:
            self.skipTest("source PR commit is not in this offline checkout")
        self.assertEqual(receipt.validate_git_source(self.data), [])


if __name__ == "__main__":
    unittest.main()
