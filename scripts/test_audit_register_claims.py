#!/usr/bin/env python3
"""Tests for scripts/audit_register_claims.py (offline)."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

import audit_register_claims as claims


class Fixture:
    def __init__(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        self.write_json(claims.INVENTORY, {"totals": {"filesScanned": 10, "mentions": {"LOCATOR_HOLD": 4}},
                                           "byCorpus": {"docs": {"files": 3, "mentions": {"LOCATOR_HOLD": 4}}}})
        self.write_json(claims.DIGESTS, {"totals": {"byState": {"match": 58, "stale": 27},
                                                    "unclaimedByReason": {"bare-hash": 141}}})
        self.register = self.root / claims.REGISTER
        self.register.parent.mkdir(parents=True, exist_ok=True)

    def write_json(self, rel: str, payload: dict) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def write_register(self, text: str) -> None:
        self.register.write_text(text, encoding="utf-8")

    def close(self) -> None:
        self._dir.cleanup()


class ClaimTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def report(self) -> dict:
        return claims.audit(self.fx.root)

    def finding(self, report: dict, label: str) -> dict:
        return next(f for f in report["findings"] if f["label"] == label)

    def test_matching_counter(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 10 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "match")

    def test_stale_counter_reports_both_numbers(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 9 |\n")
        entry = self.finding(self.report(), "просканировано текстовых файлов")
        self.assertEqual(entry["state"], "stale")
        self.assertEqual((entry["claimed"], entry["actual"]), (9, 10))

    def test_missing_anchor_is_reported_not_skipped(self) -> None:
        self.fx.write_register("| что-то другое | 10 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "anchor-missing")

    def test_missing_artefact(self) -> None:
        (self.fx.root / claims.DIGESTS).unlink()
        self.fx.write_register("| просканировано текстовых файлов | 10 |\n")
        self.assertEqual(self.finding(self.report(), "`match`")["state"], "source-missing")

    def test_conflicting_numbers_for_one_label(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 10 |\n| просканировано текстовых файлов | 11 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "anchor-ambiguous")

    def test_thin_spaces_in_numbers_are_ignored(self) -> None:
        self.fx.write_json(claims.INVENTORY, {"totals": {"filesScanned": 3110}, "byCorpus": {}})
        self.fx.write_register("| просканировано текстовых файлов | 3\u2009110 |\n")
        self.assertEqual(self.finding(self.report(), "просканировано текстовых файлов")["state"], "match")

    def test_check_exits_non_zero_on_drift(self) -> None:
        self.fx.write_register("| просканировано текстовых файлов | 9 |\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--check"]), 1)

    def test_corpus_table_drift_is_detected(self) -> None:
        self.fx.write_register(claims.CORPUS_BEGIN + "\n| stale |\n" + claims.CORPUS_END + "\n")
        self.assertEqual(self.report()["sliceStates"]["corpus"], "stale")

    def test_corpus_table_without_markers_is_reported(self) -> None:
        self.fx.write_register("## 2.1 без таблицы\n")
        self.assertEqual(self.report()["sliceStates"]["corpus"], "anchor-missing")

    def test_write_corpus_table_makes_the_block_match(self) -> None:
        self.fx.write_register("## 2.1\n" + claims.CORPUS_BEGIN + "\n" + claims.CORPUS_END + "\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--write-corpus-table"]), 0)
        text = self.fx.register.read_text(encoding="utf-8")
        self.assertIn("| `docs/` | 3 | 4 |", text)
        self.assertEqual(self.report()["sliceStates"]["corpus"], "match")


    def test_slice_table_is_generated_from_the_inventory(self) -> None:
        self.fx.write_register("## 2\n" + claims.SLICE_BEGIN + "\n" + claims.SLICE_END + "\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--write-slice-table"]), 0)
        text = self.fx.register.read_text(encoding="utf-8")
        self.assertIn("| просканировано текстовых файлов | 10 |", text)
        self.assertEqual(self.report()["sliceStates"]["inventory"], "match")

    def test_slice_drift_is_detected(self) -> None:
        self.fx.write_register(claims.SLICE_BEGIN + "\n| 3 110 |\n" + claims.SLICE_END + "\n")
        self.assertEqual(self.report()["sliceStates"]["inventory"], "stale")

    def test_thin_space_separator_does_not_touch_label_text(self) -> None:
        self.fx.write_json(claims.INVENTORY, {"totals": {"filesScanned": 3112}, "byCorpus": {}})
        block = claims.render_slice_table({"totals": {"filesScanned": 3112}})
        self.assertIn("3\u2009112", block)
        self.assertIn("| просканировано текстовых файлов |", block)

class ProseClaimTests(unittest.TestCase):
    """Numbers inside sentences, and the superseded state that keeps history honest."""

    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write_json(claims.REGISTRY, {"closures": [{"id": f"c{i}"} for i in range(3)],
                                             "confirmations": [], "notClosed": []})
        self.fx.write_json(claims.TWINS, {"scope": {"documentsCompared": 3, "markdownFiles": 4},
                                          "totals": {"pairs": 1, "byState": {}}})
        self.fx.write_json(claims.LEDGER, {"scope": {"distinctDriveIds": 92}, "totals": {}})

    def tearDown(self) -> None:
        self.fx.close()

    def prose(self, text: str) -> dict:
        self.fx.write_register(text)
        return {f["id"]: f for f in self.report()["findings"] if "id" in f}

    def report(self) -> dict:
        return claims.audit(self.fx.root)

    def test_matching_prose_claim(self) -> None:
        text = "Сравнено **3** документов (из 4 Markdown; отсечены файлы короче 200 слов)."
        self.assertEqual(self.prose(text)["twins-documents-compared"]["state"], "match")

    def test_stale_prose_claim(self) -> None:
        text = "Сравнено **9** документов (из 4 Markdown; отсечены файлы короче 200 слов)."
        entry = self.prose(text)["twins-documents-compared"]
        self.assertEqual((entry["state"], entry["claimed"], entry["actual"]), ("stale", 9, 3))

    def test_superseded_claim_points_forward(self) -> None:
        text = ("Проверено 8 из 24 объектов.\n\n"
                "## 19. Опрос доведён до конца\n")
        self.assertEqual(self.prose(text)["drive-sample-in-section-11"]["state"], "superseded")

    def test_superseded_needs_its_target_section(self) -> None:
        text = "Проверено 8 из 24 объектов.\n"
        self.assertEqual(self.prose(text)["drive-sample-in-section-11"]["state"],
                         "superseded-target-missing")

    def test_superseded_target_must_come_after_the_claim(self) -> None:
        text = "## 19. Опрос доведён до конца\n\nПроверено 8 из 24 объектов.\n"
        self.assertEqual(self.prose(text)["drive-sample-in-section-11"]["state"],
                         "superseded-target-missing")

    def test_matching_claim_is_not_downgraded_to_superseded(self) -> None:
        text = "Проверено 92 из 92 объектов.\n"
        self.assertEqual(self.prose(text)["drive-sample-in-section-11"]["state"], "match")

    def test_check_fails_on_unsuperseded_drift(self) -> None:
        self.fx.write_register("Сравнено **9** документов (из 4 Markdown).\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--check"]), 1)

class SliceRegistryTests(unittest.TestCase):
    """Every generated block is declared once, and an unknown name is not silently skipped."""

    def setUp(self) -> None:
        self.fx = Fixture()
        self.fx.write_json(claims.LINKS, {"scope": {"markdownFiles": 7},
                                          "totals": {"byState": {"resolves": 5, "external": 2, "missing": 1},
                                                     "explained": 1, "unexplained": 0}})
        self.fx.write_json(claims.TWINS, {"scope": {"documentsCompared": 3, "markdownFiles": 4},
                                          "totals": {"pairs": 0, "byState": {}}, "findings": []})
        self.fx.write_json(claims.STAMPS, {"scope": {"stamped": 0}, "totals": {"byState": {}},
                                           "findings": []})
        self.fx.write_json(claims.PINNED, {"totals": {"locators": 1, "match": 1, "mismatch": 0,
                                                      "unclaimed": 0, "unavailable": 0,
                                                      "citations": 1, "citationFiles": 1},
                                           "locators": [{"repo": "o/r", "commit": "a" * 40, "path": "A.xml",
                                                         "claimedSha256": "b" * 64, "claimedBytes": 10,
                                                         "fetchedBytes": 10, "fetchedSha256": "b" * 64,
                                                         "state": "match", "citations": [{"file": "a.md", "line": 1}]}]})

    def tearDown(self) -> None:
        self.fx.close()

    def test_links_slice_renders_from_the_committed_report(self) -> None:
        block = claims.render_links_table(json.loads((self.fx.root / claims.LINKS).read_text(encoding="utf-8")))
        self.assertIn("| ссылок `resolves` | 5 |", block)
        self.assertIn("| Markdown-файлов | 7 |", block)

    def test_links_slice_drift_is_detected(self) -> None:
        self.fx.write_register(claims.LINKS_BEGIN + "\n| ссылок `resolves` | 99 |\n" + claims.LINKS_END + "\n")
        self.assertEqual(self.report()["sliceStates"]["links"], "stale")

    def test_write_all_fills_every_declared_slice(self) -> None:
        # Built from SLICES, not from a hand-written list: a new block must not be able to
        # be declared and then forgotten by the test that is supposed to cover it.
        markers = "\n".join(line for (begin, end), _a, _r in claims.SLICES.values()
                            for line in (begin, end))
        self.fx.write_register(markers + "\n")
        self.assertEqual(claims.main(["--root", str(self.fx.root), "--write-all"]), 0)
        states = self.report()["sliceStates"]
        self.assertEqual(sorted(states), sorted(claims.SLICES))
        self.assertEqual({name: state for name, state in states.items() if state != "match"}, {})

    def test_twins_slice_renders_states_and_named_pairs(self) -> None:
        payload = {"totals": {"pairs": 2, "byState": {"identical-text": 1, "shared-text": 1}},
                   "findings": [
                       {"a": "x/a.md", "b": "x/b.md", "overlap": 1.0, "state": "identical-text"},
                       {"a": "y/c.md", "b": "y/d.md", "overlap": 0.6, "state": "shared-text"}]}
        block = claims.render_twins_table(payload)
        self.assertIn("| `identical-text` | 1 |", block)
        self.assertIn("Пар выше порога: **2**", block)
        self.assertIn("`x/a.md` ↔ `x/b.md`", block)
        self.assertNotIn("y/c.md", block, "shared text is counted, not enumerated")

    def test_stamps_slice_renders_states_and_the_edited_documents(self) -> None:
        payload = {"totals": {"byState": {"current": 1, "edited-after-stamp": 1}},
                   "findings": [
                       {"file": "a.md", "stamp": "2026-01-01", "state": "current"},
                       {"file": "b.md", "stamp": "2026-02-02", "state": "edited-after-stamp",
                        "lastCommit": "2026-03-03", "lastSubject": "fix: something"}]}
        block = claims.render_stamps_table(payload)
        self.assertIn("`current` — последний коммит в тот же день | 1 |", block)
        self.assertIn("| `b.md` | 2026-02-02 | 2026-03-03 | *fix: something* |", block)
        self.assertNotIn("`a.md`", block)

    def test_pinned_slice_renders_the_report(self) -> None:
        block = claims.render_pinned_table(json.loads((self.fx.root / claims.PINNED).read_text(encoding="utf-8")))
        self.assertIn("| локаторов | 1 |", block)
        self.assertIn("| `o/r` | `aaaaaaaa` | `A.xml` | да | 10 |", block)

    def test_missing_artefact_makes_the_slice_source_missing(self) -> None:
        (self.fx.root / claims.LINKS).unlink()
        self.fx.write_register(claims.LINKS_BEGIN + "\n" + claims.LINKS_END + "\n")
        self.assertEqual(self.report()["sliceStates"]["links"], "source-missing")

    def report(self) -> dict:
        return claims.audit(self.fx.root)

if __name__ == "__main__":
    unittest.main()


class RegisterSelfCountTests(unittest.TestCase):
    """The register may not quote the claims tool's own tally.

    Two copies of it (38 claims, then 46) sat in the prose while the tool reported 52. The number
    is printed by --summary; anything typed here is wrong by the next closure.
    """

    def setUp(self) -> None:
        self.text = (Path(__file__).resolve().parents[1] / claims.REGISTER).read_text(encoding="utf-8")

    def test_register_does_not_quote_the_number_of_claims(self) -> None:
        self.assertIsNone(re.search(r"\d+\s+утверждени", self.text),
                          "the claim count belongs to --summary, not to the document")

    def test_register_does_not_quote_the_tool_banner(self) -> None:
        self.assertNotIn("Заявленных счётчиков: ", self.text)
