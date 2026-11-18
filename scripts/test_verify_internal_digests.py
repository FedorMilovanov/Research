#!/usr/bin/env python3
"""Offline tests for scripts/verify_internal_digests.py.

The tool decides whether a document's SHA-256 still describes the file it names.
Its contract therefore fixes three things: which hash belongs to which path, when
a row says nothing at all, and which documents are allowed to be out of date.
"""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

import verify_internal_digests as vid


class Fixture:
    """A throwaway checkout with a few hashed files."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def digest(self, rel: str) -> str:
        return hashlib.sha256((self.root / rel).read_bytes()).hexdigest()

    def scan(self) -> dict:
        return vid.verify(self.root)

    def states(self) -> dict[tuple[str, int], str]:
        return {(f["file"], f["line"]): f["state"] for f in self.scan()["findings"]}

    def close(self) -> None:
        self._tmp.cleanup()


class PairingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("docs/target.md", "# target\n")
        self.digest = self.fx.digest("docs/target.md")

    def tearDown(self) -> None:
        self.fx.close()

    def _line(self, text: str) -> dict:
        self.fx.write("docs/page.md", text + "\n")
        return self.fx.scan()

    def test_one_hash_one_path_matches(self) -> None:
        report = self._line(f"- `target.md` — sha256 `{self.digest}`")
        self.assertEqual(report["findings"][0]["state"], "match")

    def test_changed_file_is_stale(self) -> None:
        report = self._line(f"- `target.md` — sha256 `{'0' * 64}`")
        self.assertEqual(report["findings"][0]["state"], "stale")

    def test_hash_without_path_is_unclaimed(self) -> None:
        report = self._line(f"цитата `{self.digest}` без файла")
        self.assertEqual(report["findings"][0]["state"], "unclaimed")

    def test_two_hashes_two_paths_pair_in_order(self) -> None:
        other = self.fx.write("docs/other.md", "# other\n")
        report = self._line(
            f"| `target.md` | `{self.digest}` | `other.md` | `{hashlib.sha256(other.read_bytes()).hexdigest()}` |"
        )
        self.assertEqual({f["sha256"]: f["state"] for f in report["findings"]},
                         {self.digest: "match",
                          hashlib.sha256(other.read_bytes()).hexdigest(): "match"})

    def test_unequal_counts_are_ambiguous(self) -> None:
        report = self._line(f"| `target.md` | `{self.digest}` | `{'1' * 64}` |")
        self.assertEqual({f["state"] for f in report["findings"]}, {"ambiguous"})

    def test_missing_file_is_external(self) -> None:
        report = self._line(f"- `gone.pdf` — sha256 `{self.digest}`")
        self.assertEqual(report["findings"][0]["state"], "external")

    def test_drive_row_is_not_hashed_against_the_repository(self) -> None:
        line = f"| `target.md` | `1sV3jfs0slLQh1lX6FawkL-It7tob2X10` | 89100 | `{self.digest}` |"
        report = self._line(line)
        self.assertEqual(report["findings"][0]["state"], "external-drive")

    def test_path_resolves_from_the_repository_root_too(self) -> None:
        self.fx.write("docs/deep/page.md", f"- `docs/target.md` — `{self.digest}`\n")
        states = [f["state"] for f in self.fx.scan()["findings"]]
        self.assertEqual(states, ["match"])


class SourceKindTests(unittest.TestCase):
    def test_round_manifest(self) -> None:
        self.assertEqual(vid.source_kind("СЕРИЯ СЕРДЦЕ/V70_SINGLE_ZIP_MANIFEST.md"), "round-manifest")

    def test_handoff(self) -> None:
        self.assertEqual(vid.source_kind("БИОГРАФИИ/Стивен Чарнок/supplemental-audits/agent6/x_handoff.md"),
                         "handoff")

    def test_live_document(self) -> None:
        self.assertEqual(vid.source_kind("docs/research/HOLDS_REGISTER_2026-11-18.md"), "live-document")


class CheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def test_stale_claim_in_a_live_document_fails_check(self) -> None:
        self.fx.write("docs/target.md", "# target\n")
        self.fx.write("docs/page.md", f"- `target.md` — `{'0' * 64}`\n")
        self.assertEqual(vid.main(["--root", str(self.fx.root), "--check"]), 1)

    def test_stale_claim_in_a_round_manifest_does_not_fail_check(self) -> None:
        self.fx.write("docs/target.md", "# target\n")
        self.fx.write("docs/V70_SINGLE_ZIP_MANIFEST.md", f"- `target.md` — `{'0' * 64}`\n")
        self.assertEqual(vid.main(["--root", str(self.fx.root), "--check"]), 0)

    def test_report_shape_is_stable(self) -> None:
        self.fx.write("docs/target.md", "# target\n")
        self.fx.write("docs/page.md", f"- `target.md` — `{self.fx.digest('docs/target.md')}`\n")
        report = self.fx.scan()
        self.assertEqual(report["schemaVersion"], vid.SCHEMA_VERSION)
        self.assertEqual(report["authorityId"], vid.AUTHORITY_ID)
        self.assertIn("staleBySourceKind", report["totals"])


if __name__ == "__main__":
    unittest.main()
