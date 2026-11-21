#!/usr/bin/env python3
"""Offline checks for the bounded STEPBible terms snapshot."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import stepbible_subdataset_terms as step


class SnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.snapshot = json.loads(step.OUT_JSON.read_text(encoding="utf-8"))

    def run_check(self, snapshot: dict, repro: dict | None = None) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "snapshot.json"
            out.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
            repro_path = root / "repro.json"
            if repro is not None:
                repro_path.write_text(json.dumps(repro, ensure_ascii=False), encoding="utf-8")
            stderr = io.StringIO()
            with (
                mock.patch.object(step, "OUT_JSON", out),
                mock.patch.object(step, "REPRO_JSON", repro_path),
                contextlib.redirect_stderr(stderr),
            ):
                return step.check(), stderr.getvalue()

    def test_committed_snapshot_passes(self) -> None:
        self.assertEqual(step.check(), 0)

    def test_snapshot_names_every_measured_dataset(self) -> None:
        self.assertEqual(self.snapshot["role"], "DERIVED_READ_ONLY_NOT_AUTHORITY")
        self.assertEqual(
            [entry["path"] for entry in self.snapshot["subdatasets"]],
            [
                "Lexicons",
                "Morphology codes",
                "Older Formats",
                "Proper Nouns",
                "Tagged-Bibles",
                "Translators Amalgamated OT+NT",
                "Versification",
            ],
        )
        self.assertEqual(
            [entry["path"] for entry in self.snapshot["nestedSubdatasets"]],
            ["Tagged-Bibles/Arabic Bibles"],
        )
        self.assertIn("Ни один HOLD этим не снимается", self.snapshot["limits"][-1])

    def test_wrong_pin_fails(self) -> None:
        changed = copy.deepcopy(self.snapshot)
        changed["pin"]["sha256"] = "0" * 64
        status, error = self.run_check(changed)
        self.assertEqual(status, 1)
        self.assertIn("закрепление", error)

    def test_aggregate_drift_fails(self) -> None:
        changed = copy.deepcopy(self.snapshot)
        changed["subdatasets"][0]["bytes"] += 1
        status, error = self.run_check(changed)
        self.assertEqual(status, 1)
        self.assertIn("сумма подкаталогов", error)

    def test_empty_dataset_entry_fails(self) -> None:
        changed = copy.deepcopy(self.snapshot)
        changed["subdatasets"][0]["declaredTerms"] = []
        changed["subdatasets"][0]["filesWithoutTokenInName"] = []
        status, error = self.run_check(changed)
        self.assertEqual(status, 1)
        self.assertIn("ни токенов", error)

    def test_official_core_size_disagreement_fails(self) -> None:
        repro = {"datasets": [{"name": "STEPBible", "bytes": step.PIN["bytes"] - 1}]}
        status, error = self.run_check(self.snapshot, repro)
        self.assertEqual(status, 1)
        self.assertIn("official-core", error)

    def test_malformed_json_is_reported_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "bad.json"
            out.write_text("{", encoding="utf-8")
            stderr = io.StringIO()
            with mock.patch.object(step, "OUT_JSON", out), contextlib.redirect_stderr(stderr):
                self.assertEqual(step.check(), 1)
            self.assertIn("не разбирается", stderr.getvalue())

    def test_unpinned_archive_is_rejected_before_reading_zip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "not-the-pinned-archive.zip"
            bad.write_bytes(b"not the pinned archive")
            with self.assertRaisesRegex(SystemExit, "архив не совпал с закреплением"):
                step.build(bad)


if __name__ == "__main__":
    unittest.main()
