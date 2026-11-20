#!/usr/bin/env python3
"""Offline tests for scripts/verify_pinned_github_locators.py.

Fixing the contract: claims are read from the same line only (no guessing), a
pinned URL without a commit is not a locator this tool judges, fetched bytes are
compared against both the digest and the byte count, and a mismatch is a failure
rather than a warning.
"""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

import verify_pinned_github_locators as vp

SHA = hashlib.sha256(b"<xml/>").hexdigest()


class Fixture:
    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def close(self) -> None:
        self._tmp.cleanup()


class CollectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def test_claim_read_from_same_line(self) -> None:
        self.fx.write("doc.md", f"| [A1](https://github.com/o/r/blob/{'a'*40}/A1.xml) | `{SHA}` | (12 bytes) |\n")
        entries = vp.collect(self.fx.root)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["claimedSha256"], SHA)
        self.assertEqual(entries[0]["claimedBytes"], 12)

    def test_claim_on_another_line_is_not_invented(self) -> None:
        self.fx.write("doc.md", f"https://github.com/o/r/blob/{'a'*40}/A1.xml\n\n`{SHA}`\n")
        entries = vp.collect(self.fx.root)
        self.assertIsNone(entries[0]["claimedSha256"])
        self.assertIsNone(entries[0]["claimedBytes"])

    def test_byte_count_with_thin_spaces(self) -> None:
        self.fx.write("doc.md", f"https://github.com/o/r/blob/{'a'*40}/big.xml (6\u00a0035\u00a0109 bytes)\n")
        self.assertEqual(vp.collect(self.fx.root)[0]["claimedBytes"], 6035109)

    def test_percent_encoded_path_is_decoded(self) -> None:
        self.fx.write("doc.md", f"https://github.com/o/r/blob/{'a'*40}/%D0%A2%D0%95%D0%9A%D0%A1%D0%A2.xml\n")
        self.assertEqual(vp.collect(self.fx.root)[0]["path"], "ТЕКСТ.xml")

    def test_duplicate_locator_is_counted_once(self) -> None:
        url = f"https://github.com/o/r/blob/{'a'*40}/A1.xml"
        self.fx.write("a.md", url + "\n")
        self.fx.write("b.md", url + "\n")
        self.assertEqual(len(vp.collect(self.fx.root)), 1)

    def test_duplicate_locator_keeps_every_citation_site(self) -> None:
        # One verified object, two documents: the first version recorded only the first
        # site, so the second citation could disappear without anything noticing.
        url = f"https://github.com/o/r/blob/{'a'*40}/A1.xml"
        self.fx.write("a.md", url + "\n")
        self.fx.write("b.md", "\n" + url + "\n")
        entry = vp.collect(self.fx.root)[0]
        self.assertEqual([(c["file"], c["line"]) for c in entry["citations"]], [("a.md", 1), ("b.md", 2)])


class VerifyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entries = [{
            "file": "doc.md", "line": 1, "repo": "o/r", "commit": "a" * 40, "path": "A1.xml",
            "url": "https://github.com/o/r/blob/" + "a" * 40 + "/A1.xml",
            "claimedSha256": SHA, "claimedBytes": 6,
        }]

    def tearDown(self) -> None:
        if hasattr(self, "_original"):
            vp.gh_raw = self._original

    def _patch(self, blob: bytes | None) -> None:
        self._original = vp.gh_raw
        vp.gh_raw = lambda repo, commit, path: blob

    def test_match(self) -> None:
        self._patch(b"<xml/>")
        self.assertEqual(vp.verify(self.entries)[0]["state"], "match")

    def test_digest_mismatch_is_not_a_match(self) -> None:
        self._patch(b"<other/>")
        self.assertEqual(vp.verify(self.entries)[0]["state"], "mismatch")

    def test_size_mismatch_is_not_a_match(self) -> None:
        entry = dict(self.entries[0])
        entry["claimedSha256"] = None
        entry["claimedBytes"] = 99
        self._patch(b"<xml/>")
        self.assertEqual(vp.verify([entry])[0]["state"], "mismatch")

    def test_unclaimed_but_measured(self) -> None:
        entry = dict(self.entries[0])
        entry["claimedSha256"] = None
        entry["claimedBytes"] = None
        self._patch(b"<xml/>")
        result = vp.verify([entry])[0]
        self.assertEqual(result["state"], "unclaimed")
        self.assertEqual(result["fetchedBytes"], 6)
        self.assertEqual(result["fetchedSha256"], SHA)

    def test_unavailable_object(self) -> None:
        self._patch(None)
        self.assertEqual(vp.verify(self.entries)[0]["state"], "unavailable")

    def test_offline_marks_not_checked(self) -> None:
        result = vp.verify(self.entries, offline=True)[0]
        self.assertEqual(result["state"], "not-checked")
        self.assertIsNone(result["fetchedSha256"])


class OutputTests(unittest.TestCase):
    def test_summary_counts_states(self) -> None:
        results = [
            {"state": "match", "repo": "o/r", "commit": "a" * 40, "path": "x", "file": "f.md", "line": 1},
            {"state": "mismatch", "repo": "o/r", "commit": "b" * 40, "path": "y", "file": "f.md", "line": 2},
        ]
        text = vp.summarise(results)
        self.assertIn("match=1", text)
        self.assertIn("mismatch=1", text)

    def test_main_returns_one_on_mismatch(self) -> None:
        fx = Fixture()
        try:
            fx.write("doc.md", f"https://github.com/o/r/blob/{'a'*40}/A1.xml (5 bytes)\n")
            original = vp.gh_raw
            vp.gh_raw = lambda repo, commit, path: b"<xml/>"
            try:
                code = vp.main(["--root", str(fx.root)])
            finally:
                vp.gh_raw = original
            self.assertEqual(code, 1)
        finally:
            fx.close()


if __name__ == "__main__":
    unittest.main()


class ReportDriftTests(unittest.TestCase):
    """The bytes need network; the shape of the report does not."""

    def setUp(self) -> None:
        self.fx = Fixture()
        self.url = f"https://github.com/o/r/blob/{'a' * 40}/A1.xml"
        self.fx.write("a.md", self.url + "\n")

    def tearDown(self) -> None:
        self.fx.close()

    def committed(self) -> dict:
        return {"locators": vp.collect(self.fx.root)}

    def test_unchanged_tree_passes(self) -> None:
        self.assertEqual(vp.structure_drift(self.committed(), vp.collect(self.fx.root)), [])

    def test_new_citation_is_reported(self) -> None:
        report = self.committed()
        self.fx.write("b.md", self.url + "\n")
        problems = vp.structure_drift(report, vp.collect(self.fx.root))
        self.assertTrue(any("citation sites changed" in p for p in problems), problems)

    def test_removed_locator_is_reported(self) -> None:
        report = self.committed()
        self.fx.write("a.md", "nothing here\n")
        problems = vp.structure_drift(report, vp.collect(self.fx.root))
        self.assertTrue(any("no longer cited" in p for p in problems), problems)

    def test_locator_outside_the_report_is_reported(self) -> None:
        report = self.committed()
        self.fx.write("c.md", f"https://github.com/o/r/blob/{'b' * 40}/B2.xml\n")
        problems = vp.structure_drift(report, vp.collect(self.fx.root))
        self.assertTrue(any("absent from the report" in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
