#!/usr/bin/env python3
"""Offline negative tests for the official-core carrier receipts."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import check_official_core_reproducibility as core


class ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = json.loads(core.RECEIPT.read_text(encoding="utf-8"))
        cls.step_terms = json.loads(core.STEP_TERMS.read_text(encoding="utf-8"))

    def test_committed_receipt_passes(self) -> None:
        self.assertEqual(core.validate(self.receipt, self.step_terms), [])
        items, errors = core.receipt_items()
        self.assertEqual(errors, [])
        self.assertEqual(len(items), 3)

    def test_committed_markdown_is_exact_generated_view(self) -> None:
        self.assertEqual(core.markdown_errors(self.receipt), [])
        self.assertEqual(
            core.OUT.read_text(encoding="utf-8"),
            core.render_markdown(self.receipt),
        )
        rendered = core.render_markdown(self.receipt)
        self.assertIn("DERIVED_READ_ONLY_NOT_AUTHORITY", rendered)
        for boundary in self.receipt["boundaries"]:
            self.assertIn(boundary, rendered)
        self.assertIn("не является текущим сетевым ответом", rendered)
        self.assertIn("PROMOTE=0", rendered)

    def test_markdown_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "view.md"
            out.write_text("stale\n", encoding="utf-8")
            errors = core.markdown_errors(self.receipt, out)
        self.assertEqual(len(errors), 1)
        self.assertIn("разошёлся с JSON", errors[0])

    def test_result_totals_are_computed_not_trusted(self) -> None:
        changed = copy.deepcopy(self.receipt)
        changed["result"]["bytesTotal"] += 1
        self.assertTrue(any("result.bytesTotal" in error for error in core.validate(changed)))

    def test_source_date_and_boundaries_cannot_drift(self) -> None:
        changed = copy.deepcopy(self.receipt)
        changed["checkedAt"] = "2026-11-19"
        changed["boundaries"] = changed["boundaries"][1:]
        errors = core.validate(changed)
        self.assertTrue(any("исходную дату" in error for error in errors))
        self.assertTrue(any("не подтверждают права" in error for error in errors))

    def test_duplicate_repository_is_rejected(self) -> None:
        changed = copy.deepcopy(self.receipt)
        changed["items"][1]["repository"] = changed["items"][0]["repository"]
        errors = core.validate(changed)
        self.assertTrue(any("повторяется" in error for error in errors))
        self.assertTrue(any("bounded official-core" in error for error in errors))

    def test_unpinned_commit_and_short_digest_are_rejected(self) -> None:
        changed = copy.deepcopy(self.receipt)
        changed["items"][0]["commit"] = "b86d26cd"
        changed["items"][0]["sha256"] = "6845fa96"
        errors = core.validate(changed)
        self.assertTrue(any("полным lowercase Git SHA" in error for error in errors))
        self.assertTrue(any("полным lowercase SHA-256" in error for error in errors))

    def test_stepbible_receipts_must_agree(self) -> None:
        changed = copy.deepcopy(self.step_terms)
        changed["pin"]["bytes"] -= 1
        self.assertTrue(any("STEPBible bytes" in error for error in core.validate(self.receipt, changed)))

    def test_malformed_json_is_a_failure_not_a_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{", encoding="utf-8")
            value, errors = core.load_json(path)
        self.assertIsNone(value)
        self.assertEqual(len(errors), 1)
        self.assertIn("не разбирается", errors[0])

    def test_archive_bytes_and_hash_are_both_checked(self) -> None:
        payload = b"bounded carrier"
        item = {
            "repository": "Faithlife/SBLGNT",
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "carrier.zip"
            path.write_bytes(payload)
            self.assertEqual(core.verify_archive(item, path), [])
            path.write_bytes(payload + b"!")
            errors = core.verify_archive(item, path)
        self.assertTrue(any("размер" in error for error in errors))
        self.assertTrue(any("SHA-256" in error for error in errors))

    def test_archive_arguments_need_each_repository_once(self) -> None:
        parsed, errors = core.parse_archives(
            [
                "Faithlife/SBLGNT=/tmp/a.zip",
                "Faithlife/SBLGNT=/tmp/b.zip",
                "unknown/repo=/tmp/c.zip",
            ]
        )
        self.assertEqual(set(parsed), {"Faithlife/SBLGNT"})
        self.assertTrue(any("повторяет" in error for error in errors))
        self.assertTrue(any("неверный" in error for error in errors))

    def test_offline_main_rejects_receipt_drift(self) -> None:
        changed = copy.deepcopy(self.receipt)
        changed["role"] = "AUTHORITY"
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "receipt.json"
            receipt.write_text(json.dumps(changed, ensure_ascii=False), encoding="utf-8")
            with mock.patch.object(core, "RECEIPT", receipt):
                self.assertEqual(core.main(["--check"]), 1)

    def test_hcr39_pins_both_source_prose_blobs_and_generated_view(self) -> None:
        registry = json.loads(
            (core.ROOT / "data" / "hold-closure-registry-v1.json").read_text(encoding="utf-8")
        )
        closure = next(
            row for row in registry["closures"] if row["id"] == "HCR-2026-11-18-39"
        )
        obj = closure["objects"][0]
        self.assertEqual(
            {
                "sourcePrReproducibilityProseBlob": obj["sourcePrReproducibilityProseBlob"],
                "sourcePrMixedGapProseBlob": obj["sourcePrMixedGapProseBlob"],
            },
            {
                "sourcePrReproducibilityProseBlob": "7f6bc0a9d23189c9805676d0af1647eb201fc6fa",
                "sourcePrMixedGapProseBlob": "7145b0a8e5e462f6ae6713ce191d5c12930f063e",
            },
        )
        self.assertEqual(obj["sourcePathsImportedVerbatim"], 0)
        self.assertEqual(obj["repairedCarrierViewAdmitted"], 1)
        self.assertEqual(obj["mixedGapNoteAdmitted"], 0)
        self.assertEqual(
            obj["generatedMarkdownSha256"],
            hashlib.sha256(core.OUT.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            set(closure["residualHolds"]),
            {"ARCHIVE_HOLD", "EVIDENCE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"},
        )


if __name__ == "__main__":
    unittest.main()
