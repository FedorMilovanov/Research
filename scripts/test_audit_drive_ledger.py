#!/usr/bin/env python3
"""Tests for scripts/audit_drive_ledger.py (offline; Drive answers come from a snapshot)."""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

import audit_drive_ledger as ledger

DRIVE_ID = "1" + "a" * 32


class Fixture:
    def __init__(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)

    def write(self, rel: str, data: bytes | str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        path.write_bytes(data)
        return path

    def close(self) -> None:
        self._dir.cleanup()


def row(label: str, size: int, md5: str, drive_id: str = DRIVE_ID) -> str:
    return f"| {label} | `{drive_id}` | {size} | `{md5}` |\n"


class ChecksumColumnTests(unittest.TestCase):
    """The checksum cell is either MD5 (32 hex) or SHA-256 (64 hex).

    Reading the first 32 hex of a SHA-256 as an MD5 makes four wave40 rows look like
    byte mismatches when nothing is wrong with them. That happened once, during the
    92-of-92 sampling pass, and is what these tests hold shut.
    """

    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def finding(self, checksum: str, drive_size: int = 10) -> dict:
        self.fx.write("dept/ledger.md", row("`doc.md`", 10, checksum))
        snapshot = {"retrievedOn": "2026-11-18",
                    "objects": {DRIVE_ID: {"size": str(drive_size), "md5": "b" * 32, "name": "doc.md"}}}
        return ledger.audit(self.fx.root, snapshot)["findings"][0]

    def test_sha256_cell_is_not_read_as_md5(self) -> None:
        finding = self.finding("a" * 64)
        self.assertIsNone(finding["claimedMd5"])
        self.assertEqual(finding["claimedSha256"], "a" * 64)

    def test_sha256_row_is_never_called_a_mismatch(self) -> None:
        self.assertEqual(self.finding("a" * 64)["driveState"], "drive-size-only")

    def test_sha256_row_with_different_size_is_a_size_mismatch(self) -> None:
        self.assertEqual(self.finding("a" * 64, drive_size=11)["driveState"], "drive-size-mismatch")

    def test_md5_row_still_compares_bytes(self) -> None:
        finding = self.finding("b" * 32)
        self.assertEqual(finding["claimedMd5"], "b" * 32)
        self.assertEqual(finding["driveState"], "drive-verified")

    def test_md5_row_with_wrong_hash_is_a_mismatch(self) -> None:
        self.assertEqual(self.finding("c" * 32)["driveState"], "drive-mismatch")

    def test_mixed_lengths_in_one_file(self) -> None:
        self.fx.write("dept/ledger.md",
                      row("`a.md`", 10, "b" * 32) + row("`b.md`", 10, "a" * 64, drive_id="1" + "c" * 32))
        report = ledger.audit(self.fx.root, None)
        self.assertEqual([f["claimedMd5"] is None for f in report["findings"]], [False, True])


class LedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def audit(self, snapshot: dict | None) -> dict:
        return ledger.audit(self.fx.root, snapshot)

    def test_parses_a_row(self) -> None:
        self.fx.write("dept/ledger.md", row("`doc.md`", 10, "0" * 32))
        report = self.audit(None)
        self.assertEqual(report["scope"]["ledgerRows"], 1)
        self.assertEqual(report["findings"][0]["driveId"], DRIVE_ID)

    def test_drive_verified(self) -> None:
        self.fx.write("dept/ledger.md", row("`doc.md`", 10, "0" * 32))
        snapshot = {"retrievedOn": "2026-11-18",
                    "objects": {DRIVE_ID: {"size": "10", "md5": "0" * 32, "name": "doc.md"}}}
        self.assertEqual(self.audit(snapshot)["findings"][0]["driveState"], "drive-verified")

    def test_drive_mismatch(self) -> None:
        self.fx.write("dept/ledger.md", row("`doc.md`", 10, "0" * 32))
        snapshot = {"retrievedOn": "2026-11-18",
                    "objects": {DRIVE_ID: {"size": "11", "md5": "0" * 32, "name": "doc.md"}}}
        self.assertEqual(self.audit(snapshot)["findings"][0]["driveState"], "drive-mismatch")

    def test_drive_not_sampled(self) -> None:
        self.fx.write("dept/ledger.md", row("`doc.md`", 10, "0" * 32))
        self.assertEqual(self.audit(None)["findings"][0]["driveState"], "drive-not-sampled")

    def test_local_current_and_moved_on(self) -> None:
        body = b"hello"
        md5 = hashlib.md5(body).hexdigest()
        self.fx.write("dept/doc.md", body)
        self.fx.write("dept/ledger.md", row("`doc.md`", len(body), md5))
        self.assertEqual(self.audit(None)["findings"][0]["localState"], "local-current")
        self.fx.write("dept/doc.md", b"hello again")
        self.assertEqual(self.audit(None)["findings"][0]["localState"], "local-moved-on")

    def test_same_name_in_two_folders_is_ambiguous(self) -> None:
        self.fx.write("dept/a/doc.md", b"one")
        self.fx.write("dept/b/doc.md", b"two")
        self.fx.write("dept/ledger.md", row("`doc.md`", 3, hashlib.md5(b"one").hexdigest()))
        finding = self.audit(None)["findings"][0]
        self.assertEqual(finding["localState"], "local-ambiguous")
        self.assertEqual(finding["localMatches"], 2)

    def test_report_schema_and_scope(self) -> None:
        self.fx.write("dept/ledger.md", row("`doc.md`", 10, "0" * 32))
        report = self.audit({"retrievedOn": "2026-11-18", "objects": {}})
        self.assertEqual(report["schemaVersion"], ledger.SCHEMA_VERSION)
        self.assertEqual(report["authorityId"], ledger.AUTHORITY_ID)
        self.assertEqual(report["scope"]["snapshotDate"], "2026-11-18")
        self.assertIn("drive", report["totals"])


if __name__ == "__main__":
    unittest.main()
