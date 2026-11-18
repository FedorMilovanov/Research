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
        self.assertEqual({f["digest"]: f["state"] for f in report["findings"]},
                         {self.digest: "match",
                          hashlib.sha256(other.read_bytes()).hexdigest(): "match"})

    def test_two_hashes_for_one_path_are_both_checked(self) -> None:
        # The handoff table lists the hash from the old receipt and the hash of the
        # bytes at handoff: both name the same file, so both are claims.
        line = f"| `target.md` | `{'0' * 64}` | `{self.digest}` |"
        report = self._line(line)
        states = {f["digest"]: f["state"] for f in report["findings"]}
        self.assertEqual(states[("0" * 64)], "stale")
        self.assertEqual(states[self.digest], "match")

    def test_unequal_counts_are_ambiguous(self) -> None:
        report = self._line(f"| `target.md` | `{self.digest}` | `{'1' * 64}` | `{'2' * 64}` |")
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


class ShortDigestTests(unittest.TestCase):
    """A 40-hex value is a Git object id unless the line says it is a file digest."""

    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("target.md", "one\ntwo\n")
        data = (self.fx.root / "target.md").read_bytes()
        self.plain = hashlib.sha1(data).hexdigest()
        blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        self.blob = blob

    def tearDown(self) -> None:
        self.fx.close()

    def _states(self, line: str) -> dict:
        self.fx.write("doc.md", line + "\n")
        report = vid.verify(self.fx.root)
        return {f["digest"][:8]: f["state"] for f in report["findings"]}

    def test_labelled_sha1_is_verified(self) -> None:
        self.assertEqual(self._states(f"- `target.md` — sha1 `{self.plain}`"), {self.plain[:8]: "match"})

    def test_labelled_sha1_of_earlier_bytes_is_stale(self) -> None:
        self.assertEqual(self._states(f"- `target.md` — sha1 `{'0' * 40}`"), {"00000000": "stale"})

    def test_git_blob_spelling_also_matches(self) -> None:
        self.assertEqual(self._states(f"- `target.md` — Git blob sha1 `{self.blob}`"), {self.blob[:8]: "match"})

    def test_unlabelled_commit_id_is_not_a_claim(self) -> None:
        # A closeout table lists a commit next to a file name; that is not a claim
        # about the bytes of the file, and proximity must not convict it.
        line = f"| 2 | `target.md` | `{'a' * 40}` |"
        self.assertEqual(self._states(line), {"aaaaaaaa": "git-object-id"})

    def test_unlabelled_md5_is_not_a_claim(self) -> None:
        self.assertEqual(self._states(f"- `target.md` — {'b' * 32}"), {"bbbbbbbb": "unlabelled-partial"})


class JsonRecordTests(unittest.TestCase):
    """Machine registries pair one digest with one path; looser shapes claim nothing."""

    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write("data/target.json", '{"a": 1}\n')
        self.digest = self.fx.digest("data/target.json")

    def tearDown(self) -> None:
        self.fx.close()

    def _states(self, payload: dict) -> list[str]:
        self.fx.write("data/registry.json", __import__("json").dumps(payload))
        return [f["state"] for f in vid.verify_json(self.fx.root)["findings"]]

    def test_matching_record(self) -> None:
        self.assertEqual(self._states({"path": "data/target.json", "sha256": self.digest}), ["match"])

    def test_record_of_earlier_bytes(self) -> None:
        self.assertEqual(self._states({"path": "data/target.json", "sha256": "0" * 64}), ["stale"])

    def test_path_outside_the_checkout(self) -> None:
        self.assertEqual(self._states({"path": "gone/file.pdf", "sha256": self.digest}), ["external"])

    def test_two_digests_are_not_paired(self) -> None:
        self.assertEqual(self._states({"path": "data/target.json", "sha256": self.digest, "other": "1" * 64}), [])


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
