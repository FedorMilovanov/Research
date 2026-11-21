"""Offline tests for the read-only HOLD inventory.

Fixtures are synthetic: they test classification of marker text, not the
evidentiary state of any real source.
"""
import tempfile
import unittest
from pathlib import Path

from audit_repository_holds import (
    CANONICAL_FLAGS,
    classification,
    corpus_of,
    main,
    scan,
)


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class ClassificationTests(unittest.TestCase):
    def test_closure_is_closed(self):
        self.assertEqual(classification("- **HOLD:** `ARCHIVE_HOLD` **снят**"), {"closed"})

    def test_surviving_flag_is_open(self):
        self.assertEqual(
            classification("`RIGHTS_HOLD` сохраняется до проверки лицензии."), {"open"}
        )

    def test_negated_closure_is_open(self):
        self.assertEqual(classification("`LOCATOR_HOLD` не снят."), {"open"})

    def test_bare_marker_is_unmarked(self):
        self.assertEqual(classification("| 12 | `EVIDENCE_HOLD` |"), {"unmarked"})

    def test_line_with_two_states_is_mixed(self):
        states = classification("ARCHIVE_HOLD снят, но PUBLICATION_HOLD сохраняется")
        self.assertIn("closed", states)
        self.assertIn("open", states)
        self.assertIn("mixed", states)


class CorpusTests(unittest.TestCase):
    def test_top_level_file_is_root(self):
        self.assertEqual(corpus_of("README.md"), "_root")

    def test_nested_file_takes_top_segment(self):
        self.assertEqual(corpus_of("ИСКУПЛЕНИЕ/07_LEDGER.md"), "ИСКУПЛЕНИЕ")


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_counts_canonical_flags_and_status(self):
        write(
            self.root,
            "corpus/a.md",
            "`ARCHIVE_HOLD` сhanged nothing\n"
            "`ARCHIVE_HOLD` **снят**\n"
            "`PUBLICATION_HOLD` открыт\n",
        )
        inventory = scan(self.root)
        self.assertEqual(inventory["totals"]["mentions"]["ARCHIVE_HOLD"], 2)
        self.assertEqual(inventory["totals"]["mentions"]["PUBLICATION_HOLD"], 1)
        self.assertEqual(inventory["totals"]["mentionsByStatus"]["closed"], 1)
        self.assertEqual(inventory["totals"]["mentionsByStatus"]["open"], 1)
        self.assertEqual(inventory["byCorpus"]["corpus"]["files"], 1)

    def test_json_holds_arrays_are_counted_separately(self):
        write(
            self.root,
            "data/registry.json",
            '{\n  "entry": {\n    "holds": [\n      "RIGHTS_HOLD",\n      "PUBLICATION_HOLD"\n    ]\n  }\n}\n',
        )
        inventory = scan(self.root)
        self.assertEqual(inventory["totals"]["filesWithJsonHolds"], 1)
        self.assertEqual(inventory["totals"]["jsonHoldsValues"]["RIGHTS_HOLD"], 1)
        self.assertEqual(inventory["totals"]["jsonHoldsValues"]["PUBLICATION_HOLD"], 1)
        # structured array items must not be double-counted as prose mentions
        self.assertEqual(inventory["totals"]["mentions"], {})

    def test_extended_flags_are_reported(self):
        write(self.root, "corpus/b.md", "`VERSION-HOLD` сохранён; `BLOCKING-HOLD` remains.\n")
        inventory = scan(self.root)
        self.assertEqual(inventory["totals"]["mentions"]["VERSION-HOLD"], 1)
        self.assertEqual(inventory["totals"]["mentions"]["BLOCKING-HOLD"], 1)
        self.assertEqual(inventory["totals"]["mentionsByStatus"], {})

    def test_scan_is_deterministic(self):
        write(self.root, "a.md", "`EVIDENCE_HOLD` остаётся\n")
        write(self.root, "b/x.md", "`LOCATOR_HOLD` снят\n")
        self.assertEqual(scan(self.root), scan(self.root))

    def test_scan_is_read_only(self):
        target = write(self.root, "a.md", "`ARCHIVE_HOLD` сохраняется\n")
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        scan(self.root)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(target.read_text(encoding="utf-8"), "`ARCHIVE_HOLD` сохраняется\n")

    def test_skipped_directories_are_not_scanned(self):
        write(self.root, "google_drive/mirror.md", "`ARCHIVE_HOLD` сохраняется\n")
        inventory = scan(self.root)
        self.assertEqual(inventory["totals"]["mentions"], {})

    def test_output_file_matches_scan(self):
        write(self.root, "a.md", "`RIGHTS_HOLD` открыт\n")
        out = self.root / "out.json"
        self.assertEqual(main(["--root", str(self.root), "-o", str(out)]), 0)
        self.assertIn("RIGHTS_HOLD", out.read_text(encoding="utf-8"))


class PolicyTests(unittest.TestCase):
    def test_canonical_flag_set_is_exactly_evidence_policy_v2(self):
        self.assertEqual(
            CANONICAL_FLAGS,
            (
                "EVIDENCE_HOLD",
                "LOCATOR_HOLD",
                "ARCHIVE_HOLD",
                "RIGHTS_HOLD",
                "PUBLICATION_HOLD",
            ),
        )


if __name__ == "__main__":
    unittest.main()
