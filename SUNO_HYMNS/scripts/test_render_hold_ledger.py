"""Black-box regressions: --check must never create, fix or restamp a HOLD view.

Only temporary project fixtures are executed, including in the old-renderer control.
Neither the real registries nor RESEARCH/OPEN_HOLDS.md are written by these tests.
"""

import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("render_hold_ledger.py")


class HoldLedgerCheckTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for directory in ("scripts", "data", "RESEARCH"):
            (self.root / directory).mkdir()
        self.script = self.root / "scripts" / SCRIPT.name
        self.script.write_bytes(SCRIPT.read_bytes())
        self.src = self.root / "data" / "source-registry-v1.json"
        self.clm = self.root / "data" / "claim-ledger-v1.json"
        self.out = self.root / "RESEARCH" / "OPEN_HOLDS.md"
        self.src.write_text(json.dumps({"sources": [
            {"id": "SRC-Z", "title": "Зет", "accessState": "PARTIAL_OBJECT",
             "locatorState": "COARSE_LOCATOR_ONLY", "rightsState": "PERMISSION_REQUIRED",
             "holds": ["ARCHIVE_HOLD", "LOCATOR_HOLD", "RIGHTS_HOLD"]},
            {"id": "SRC-A", "title": "Альфа", "accessState": "NOT_ACQUIRED",
             "locatorState": "LOCATOR_MISSING", "rightsState": "RIGHTS_UNKNOWN",
             "holds": ["EVIDENCE_HOLD", "RIGHTS_HOLD"]},
        ]}, ensure_ascii=False), encoding="utf-8")
        self.clm.write_text(json.dumps({"claims": [
            {"id": "CLM-Z", "topic": "Зет", "claimStatus": "RESEARCH_OPEN",
             "holds": ["ARCHIVE_HOLD", "RIGHTS_HOLD"]},
            {"id": "CLM-A", "topic": "Альфа", "claimStatus": "EVIDENCE_HOLD",
             "holds": ["LOCATOR_HOLD", "EVIDENCE_HOLD", "RIGHTS_HOLD"]},
        ]}, ensure_ascii=False), encoding="utf-8")
        result = self.run_cli()
        self.assertEqual(0, result.returncode, result.stderr)
        # Seed an old leap-day snapshot without a clock mock. A later --check must
        # use its recorded date, not rewrite it to the date of the test run.
        text, substitutions = re.subn(r"; сборка от \d{4}-\d{2}-\d{2}\.",
                                     "; сборка от 2000-02-29.",
                                     self.out.read_text(encoding="utf-8"))
        self.assertEqual(1, substitutions)
        self.out.write_bytes(text.encode("utf-8"))
        for path in self.root.rglob("*"):
            if path.is_file():
                os.utime(path, ns=(946684800000000000, 946684800000000000))

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(self.script), *args],
                              cwd=self.root, capture_output=True, text=True,
                              encoding="utf-8", timeout=10, check=False)

    def snapshot(self):
        return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns,
                                                p.stat().st_mode)
                for p in self.root.rglob("*") if p.is_file()}

    def assert_check(self, expected):
        before = self.snapshot()
        result = self.run_cli("--check")
        self.assertEqual(before, self.snapshot(), "--check wrote to the fixture")
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS" if expected == 0 else "FAIL", result.stdout + result.stderr)
        return result

    def change_record(self, path, kind, field, value):
        data = json.loads(path.read_text(encoding="utf-8"))
        data[kind][0][field] = value
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_check_preserves_matching_snapshot_bytes_mtimes_and_recorded_date(self):
        result = self.assert_check(0)
        self.assertIn("2000-02-29", result.stdout)
        self.assertIn("это не новая сборка", result.stdout)

    def test_missing_snapshot_fails_without_creating_it(self):
        self.out.unlink()
        self.assert_check(1)
        self.assertFalse(self.out.exists())

    def test_source_hold_drift_fails_without_repair(self):
        self.change_record(self.src, "sources", "holds", ["RIGHTS_HOLD"])
        self.assert_check(1)

    def test_claim_hold_drift_fails_without_repair(self):
        self.change_record(self.clm, "claims", "holds", [])
        self.assert_check(1)

    def test_source_title_drift_fails_without_repair(self):
        self.change_record(self.src, "sources", "title", "Новый заголовок")
        self.assert_check(1)

    def test_source_operational_field_drift_fails_without_repair(self):
        original = self.src.read_bytes()
        for field, value in (("accessState", "FULL_OBJECT_VERIFIED"),
                             ("locatorState", "EXACT_LOCATOR_VERIFIED"),
                             ("rightsState", "STORAGE_ONLY")):
            with self.subTest(field=field):
                self.src.write_bytes(original)
                self.change_record(self.src, "sources", field, value)
                self.assert_check(1)

    def test_claim_topic_and_status_drift_fail_without_repair(self):
        original = self.clm.read_bytes()
        for field, value in (("topic", "Новая тема"), ("claimStatus", "SUPPORTED_WITH_SCOPE_LIMITS")):
            with self.subTest(field=field):
                self.clm.write_bytes(original)
                self.change_record(self.clm, "claims", field, value)
                self.assert_check(1)

    def test_rights_count_only_drift_is_detected(self):
        # Neither record loses an actionable HOLD here: this changes only the
        # aggregate RIGHTS_HOLD count, not its separate permission-required list.
        self.change_record(self.src, "sources", "holds", ["ARCHIVE_HOLD", "LOCATOR_HOLD"])
        self.assert_check(1)

    def test_unrendered_notes_and_source_links_do_not_force_a_rebuild(self):
        self.change_record(self.src, "sources", "limits", ["No new primary reading."])
        self.change_record(self.clm, "claims", "sourceIds", ["SRC-A"])
        self.assert_check(0)

    def test_registry_order_does_not_change_the_sorted_view(self):
        for path, key in ((self.src, "sources"), (self.clm, "claims")):
            data = json.loads(path.read_text(encoding="utf-8"))
            data[key].reverse()
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assert_check(0)

    def test_bad_or_missing_header_and_impossible_date_fail_without_repair(self):
        original = self.out.read_bytes()
        for bad in (original.replace(b"2000-02-29", b"2026-02-30"),
                    original.replace(b"2000-02-29", b"not-a-date"),
                    b"# Not a generated header\n\n" + original,
                    b"# No header\n\n" + original.split(b"\n", 3)[3]):
            with self.subTest(header=bad[:240]):
                self.out.write_bytes(bad)
                self.assert_check(1)

    def test_valid_header_does_not_mask_truncated_or_edited_body(self):
        original = self.out.read_bytes()
        for bad in (b"\n".join(original.split(b"\n")[:3]) + b"\n",
                    original + b"Extra content\n", original[:-1]):
            with self.subTest(length=len(bad)):
                self.out.write_bytes(bad)
                self.assert_check(1)

    def test_crlf_is_not_silently_normalized_or_rewritten(self):
        self.out.write_bytes(self.out.read_bytes().replace(b"\n", b"\r\n"))
        self.assert_check(1)

    def test_invalid_registry_json_and_utf8_fail_without_writes(self):
        for path in (self.src, self.clm):
            original = path.read_bytes()
            for bad in (b"{broken", b"\xff"):
                with self.subTest(path=path.name, data=bad):
                    path.write_bytes(bad)
                    self.assert_check(1)
            path.write_bytes(original)

    def test_typo_and_unknown_flags_fail_before_io_without_writes(self):
        self.src.unlink()
        self.clm.unlink()
        self.out.unlink()
        for args in (("--chek",), ("--check", "--unknown")):
            with self.subTest(args=args):
                before = self.snapshot()
                result = self.run_cli(*args)
                self.assertEqual(before, self.snapshot())
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn("unrecognized arguments", result.stderr)

    def test_help_neither_reads_registries_nor_writes_snapshot(self):
        self.src.unlink()
        self.clm.unlink()
        self.out.unlink()
        before = self.snapshot()
        result = self.run_cli("--help")
        self.assertEqual(before, self.snapshot())
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--check", result.stdout)

    def test_default_mode_still_writes_with_today_but_does_not_change_registries(self):
        self.out.write_bytes(b"stale snapshot\n")
        before = self.snapshot()
        first_day = datetime.date.today().isoformat()
        result = self.run_cli()
        last_day = datetime.date.today().isoformat()
        after = self.snapshot()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({key: value for key, value in before.items()
                          if key != "RESEARCH/OPEN_HOLDS.md"},
                         {key: value for key, value in after.items()
                          if key != "RESEARCH/OPEN_HOLDS.md"})
        text = self.out.read_text(encoding="utf-8")
        self.assertTrue(any(f"сборка от {day}." in text for day in (first_day, last_day)))
        self.assertIn("ARCHIVE=1/1 LOCATOR=1/1 EVIDENCE=1/1 RIGHTS=2/2", result.stdout)
        for name in ("ARCHIVE_HOLD", "LOCATOR_HOLD", "EVIDENCE_HOLD"):
            self.assertIn(f"| `{name}` | 1 | 1 |", text)
        self.assertIn("| `RIGHTS_HOLD` | 2 | 2 |", text)
        self.assert_check(0)


if __name__ == "__main__":
    unittest.main()
