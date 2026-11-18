#!/usr/bin/env python3
"""Offline tests for scripts/audit_text_integrity.py.

The tool changes prose, so its contract has to be narrow: it may only insert
spaces, only where the file's own history already contains the spaced words, and
never inside code. These tests fix each of those limits.
"""
from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

import audit_text_integrity as ati


class FakeHistory:
    """Stand-in for git: returns whatever blob the test declares."""

    def __init__(self, blobs: dict[str, str]) -> None:
        self.blobs = blobs

    def __call__(self, path: Path, root: Path, limit: int = 0) -> str:
        return self.blobs.get(path.relative_to(root).as_posix(), "")


class Fixture:
    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def audit(self, blobs: dict[str, str] | None = None) -> dict:
        return ati.audit(self.root, FakeHistory(blobs or {}))

    def repair(self, blobs: dict[str, str] | None = None, **kwargs) -> dict:
        return ati.repair(self.root, FakeHistory(blobs or {}), **kwargs)

    def close(self) -> None:
        self._tmp.cleanup()


class TokenTests(unittest.TestCase):
    def test_glued_token_is_found(self) -> None:
        self.assertEqual([t for _, t in ati.find_tokens("Архитектура10будущих")], ["Архитектура10будущих"])

    def test_spaced_text_is_not_a_token(self) -> None:
        self.assertEqual(ati.find_tokens("Архитектура 10 будущих"), [])

    def test_identifiers_are_not_tokens(self) -> None:
        # Latin identifiers such as A32726 or EEBO-TCP are not damaged prose.
        self.assertEqual(ati.find_tokens("EEBO-TCP A32726 B20167"), [])

    def test_inline_code_is_masked(self) -> None:
        self.assertEqual(ati.find_tokens("см. `1глава2` тут"), [])

    def test_fenced_block_is_masked(self) -> None:
        self.assertEqual(ati.find_tokens("```\n1глава2\n```\n"), [])

    def test_masking_keeps_offsets(self) -> None:
        text = "a `x` b10c"
        masked = ati.mask_code(text)
        self.assertEqual(len(masked), len(text))
        self.assertEqual(masked.index("b10c"), text.index("b10c"))

    def test_spaced_splits_both_boundaries(self) -> None:
        self.assertEqual(ati.spaced("и28июля"), "и 28 июля")

    def test_spaced_leaves_other_text_alone(self) -> None:
        self.assertEqual(ati.spaced("обычный"), "обычный")


class EvidenceTests(unittest.TestCase):
    def test_window_matches_across_whitespace(self) -> None:
        window = "Архитектура10будущих документов"
        self.assertTrue(ati.has_evidence(window, "… Архитектура 10 будущих документов …"))

    def test_missing_history_is_no_evidence(self) -> None:
        self.assertFalse(ati.has_evidence("Архитектура10будущих", ""))

    def test_different_words_are_no_evidence(self) -> None:
        self.assertFalse(ati.has_evidence("Архитектура10будущих", "Архитектура 11 будущих"))


class RepairTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def test_repair_inserts_spaces_when_history_agrees(self) -> None:
        path = self.fx.write("docs/a.md", "Итого44строки текста.\n")
        result = self.fx.repair({"docs/a.md": "Итого 44 строки текста.\n"})
        self.assertEqual(result["repairedTokens"], 1)
        self.assertEqual(path.read_text(encoding="utf-8"), "Итого 44 строки текста.\n")

    def test_repair_leaves_unproven_tokens_alone(self) -> None:
        path = self.fx.write("docs/a.md", "Итого44строки текста.\n")
        self.fx.repair({})
        self.assertEqual(path.read_text(encoding="utf-8"), "Итого44строки текста.\n")

    def test_repair_changes_only_whitespace(self) -> None:
        path = self.fx.write("docs/a.md", "Итого44строки и18нельзя.\n")
        self.fx.repair({"docs/a.md": "Итого 44 строки и 18 нельзя.\n"})
        after = path.read_text(encoding="utf-8")
        self.assertEqual(re.sub(r"\s+", "", after), re.sub(r"\s+", "", "Итого44строки и18нельзя.\n"))

    def test_repair_reaches_fixpoint_in_one_run(self) -> None:
        self.fx.write("docs/a.md", "и28июля\n")
        history = "и 28 июля\n"
        self.fx.repair({"docs/a.md": history})
        self.assertEqual(self.fx.audit({"docs/a.md": history})["totals"]["gluedTokens"], 0)

    def test_repair_does_not_touch_json_syntax(self) -> None:
        path = self.fx.write("docs/a.json", '{"k": "по2Кор80"}\n')
        self.fx.repair({"docs/a.json": '{"k": "по 2 Кор 80"}\n'})
        import json
        # The tool repairs the word-number-word boundaries it can see; a number
        # merely trailing a word ("Кор80") is left alone, because citations such
        # as "Мф5" and "1Кор" use the same shape legitimately.
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["k"], "по 2 Кор80")


class AuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def test_report_counts_states(self) -> None:
        self.fx.write("docs/a.md", "Итого44строки.\n")
        self.fx.write("docs/b.md", "Ничего.\n")
        report = self.fx.audit({"docs/a.md": "Итого 44 строки.\n"})
        self.assertEqual(report["totals"]["gluedTokens"], 1)
        self.assertEqual(report["totals"]["filesWithTokens"], 1)
        self.assertEqual(report["totals"]["byState"], {"evidence": 1})

    def test_token_without_history_is_not_checked(self) -> None:
        # Outside a git repository the tool cannot tell damage from prose that was
        # always written this way, so it must not claim either: no failure.
        self.fx.write("docs/a.md", "Итого44строки.\n")
        report = self.fx.audit({})
        self.assertEqual(report["totals"]["byState"], {"not-checked": 1})
        self.assertEqual(ati.main(["--root", str(self.fx.root), "--check"]), 0)

    def test_check_fails_on_a_repairable_token(self) -> None:
        self.fx.write("docs/a.md", "Итого44строки.\n")
        original = ati.file_history_text
        ati.file_history_text = lambda path, root, limit=0: "Итого 44 строки.\n"
        try:
            self.assertEqual(ati.main(["--root", str(self.fx.root), "--check"]), 1)
        finally:
            ati.file_history_text = original

    def test_receipt_blocked_file_is_not_repaired_and_does_not_fail_check(self) -> None:
        import hashlib
        text = "Итого44строки.\n"
        self.fx.write("docs/a.md", text)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        self.fx.write("data/receipts.json", '{"a": "%s"}\n' % digest)
        report = ati.audit(self.fx.root, FakeHistory({"docs/a.md": "Итого 44 строки.\n"}))
        self.assertEqual(report["totals"]["byState"], {"receipt-blocked": 1})
        self.assertEqual(ati.main(["--root", str(self.fx.root), "--check"]), 0)
        self.fx.repair({"docs/a.md": "Итого 44 строки.\n"})
        self.assertEqual((self.fx.root / "docs/a.md").read_text(encoding="utf-8"), text)

    def test_receipt_override_repairs_anyway(self) -> None:
        import hashlib
        text = "Итого44строки.\n"
        self.fx.write("docs/a.md", text)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        self.fx.write("data/receipts.json", '{"a": "%s"}\n' % digest)
        self.fx.repair({"docs/a.md": "Итого 44 строки.\n"}, ignore_receipts=True)
        self.assertEqual((self.fx.root / "docs/a.md").read_text(encoding="utf-8"), "Итого 44 строки.\n")

    def test_report_shape(self) -> None:
        self.fx.write("docs/a.md", "Итого44строки.\n")
        report = self.fx.audit({"docs/a.md": "Итого 44 строки.\n"})
        self.assertEqual(report["schemaVersion"], ati.SCHEMA_VERSION)
        self.assertEqual(report["authorityId"], ati.AUTHORITY_ID)


if __name__ == "__main__":
    unittest.main()
