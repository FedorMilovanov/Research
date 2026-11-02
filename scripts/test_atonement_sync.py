#!/usr/bin/env python3
"""Offline regression tests. No source downloads and no writes to repository files."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import io
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from atonement_crossref_audit import FILE_REF, main as crossref_main
from atonement_draft_citation_audit import audit_quotes, check_quote, load_bible, parse_ref
from atonement_sync_check import ROOT, REPORT, CONTROL, DRAFTS, check, check_greek, check_repairs, witnesses
from atonement_sync_sources import parse_rst_book, USFM, RSB_STEMS, SOURCES


class CitationTests(unittest.TestCase):
    def test_exact_with_typographic_normalization(self):
        self.assertEqual(check_quote("**Он** понёс грех", "Он понес грех.")[0], "EXACT")

    def test_not_a_substring_of_a_word(self):
        self.assertEqual(check_quote("Бог", "богатство")[0], "MISMATCH")

    def test_ordered_ellipsis(self):
        self.assertEqual(check_quote("Бог… через веру", "Бог предложил через веру")[0], "SEGMENTS")
        self.assertEqual(check_quote("через веру… Бог", "Бог предложил через веру")[0], "MISMATCH")

    def test_segment_cannot_reuse_same_occurrence(self):
        self.assertEqual(check_quote("слово… слово", "одно слово")[0], "MISMATCH")

    def test_empty_ellipsis_is_not_proof(self):
        self.assertEqual(check_quote("…", "любой текст")[0], "PARSE_FAIL")

    def test_reversed_range_refused(self):
        self.assertIsNone(parse_ref("Рим 3:26–24"))
        self.assertIsNone(parse_ref("Рим 0:1"))
        self.assertIsNone(parse_ref("Рим 3:0"))

    def test_reference_alias_and_range(self):
        self.assertEqual(parse_ref("1 Ин. 2:1–2, Синодальный"), ("1Ин", 2, 1, 2))

    def test_empty_bible_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "empty.tsv"
            p.write_text("not a Bible\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_bible(p)

    def test_duplicate_tsv_verse_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "duplicate.tsv"
            p.write_text("Рим\t3\t25\tone\nРим\t3\t25\ttwo\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_bible(p)

    def test_zero_quotations_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                audit_quotes(Path(tmp), [("w", {("Рим", 3, 25): "text"})])

    def test_duplicate_witness_names_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                audit_quotes(Path(tmp), [("same", {1: "x"}), ("same", {1: "x"})])

    def test_unresolved_reference_is_not_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "01.md").write_text("«достоверная цитата» (Синодальный).\n", encoding="utf-8")
            rows = audit_quotes(Path(tmp), [("w", {("Рим", 3, 25): "достоверная цитата"})])
            self.assertEqual(rows[0]["status"], "NO_REF")

    def test_source_conflict_is_not_a_unanimous_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "01.md").write_text("«показания правды» (Рим 3:25, Синодальный).\n", encoding="utf-8")
            rows = audit_quotes(Path(tmp), [("a", {("Рим", 3, 25): "показания правды"}),
                                           ("b", {("Рим", 3, 25): "другой текст"})])
            self.assertEqual(rows[0]["status"], "SOURCE_CONFLICT")

    def test_incomplete_source_is_not_proof_of_wrong_quotation(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "01.md").write_text("«показания правды» (Рим 3:25, Синодальный).\n", encoding="utf-8")
            rows = audit_quotes(Path(tmp), [("a", {("Рим", 3, 25): "показания правды"}),
                                           ("b", {("Рим", 3, 24): "другой стих"})])
            self.assertEqual(rows[0]["status"], "VERSE_MISSING")


class SourceExtractionTests(unittest.TestCase):
    def test_rst_paragraph_split_is_joined_not_overwritten(self):
        rows = parse_rst_book("#3:13#Первая часть.\n#p#\n#3:13#Вторая <i>часть</i>.\n", "Быт", "book.dat")
        self.assertEqual(rows[("Быт", 3, 13)], ("Первая часть. Вторая часть.", "book.dat"))

    def test_nonconsecutive_repeated_verse_refused(self):
        with self.assertRaises(ValueError):
            parse_rst_book("#1:1#A\n#1:2#B\n#1:1#C\n", "Быт", "book.dat")

    def test_entities_and_markup_preserve_text(self):
        rows = parse_rst_book("#1:1#&laquo;Я&raquo; <i>сказал</i>.\n", "Быт", "book.dat")
        self.assertEqual(rows[("Быт", 1, 1)][0], "«Я» сказал.")

    def test_identifiers_not_file_order_define_books(self):
        self.assertEqual(USFM["rom"], "Рим")
        self.assertEqual(RSB_STEMS["rim"], "Рим")
        self.assertEqual(USFM["jas"], "Иак")
        self.assertEqual(len(USFM), 66)
        self.assertEqual(len(set(USFM.values())), 66)
        self.assertEqual(set(USFM.values()), set(RSB_STEMS.values()))


class CrossReferenceTests(unittest.TestCase):
    def test_multilevel_path_is_not_truncated(self):
        path = "../../../docs/research/atonement/34_example.md"
        match = FILE_REF.search(f"`{path}` §4.110")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), path)

    def test_wrong_base_is_not_silently_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drafts = root / "drafts"
            drafts.mkdir()
            (root / "01_source.md").write_text("## 1. Exists at the wrong base\n", encoding="utf-8")
            (drafts / "01_draft.md").write_text("`01_source.md` §1.\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                status = crossref_main(["--drafts", str(drafts), "--docs", str(root), "--check"])
            self.assertEqual(status, 1)

    def test_correct_relative_path_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drafts = root / "drafts"
            drafts.mkdir()
            (root / "01_source.md").write_text("## 4.110. Correct section\n", encoding="utf-8")
            (drafts / "01_draft.md").write_text("`../01_source.md` §4.110.\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                status = crossref_main(["--drafts", str(drafts), "--check"])
            self.assertEqual(status, 0)


class ActualSynchronizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text(encoding="utf-8"))
        cls.control = json.loads((ROOT / CONTROL).read_text(encoding="utf-8"))

    def test_current_corpus_and_coverage(self):
        errors, summary = check(ROOT, self.report, self.control)
        self.assertEqual(errors, [])
        self.assertEqual(summary["markedCitations"], self.report["markedCitationCount"])
        self.assertEqual(summary["drafts"], 13)

    def test_each_refuted_greek_claim_cannot_be_restored(self):
        for row in self.report["repairs"]:
            if row["id"] not in {f"G{i:02}" for i in range(1, 6)}:
                continue
            with self.subTest(repair=row["id"]):
                original = (ROOT / row["file"]).read_text(encoding="utf-8")
                broken = original.replace(row["required"], row["removed"], 1)
                errors = check_repairs(ROOT, self.report, {row["file"]: broken})
                self.assertTrue(any(row["id"] in error for error in errors), errors)

    def test_each_old_synodal_mismatch_still_fails_both_sources(self):
        old = json.loads((ROOT / "ИСКУПЛЕНИЕ/evidence/synodal_citation_audit_2026-10-30.json").read_text(encoding="utf-8"))
        corpora = witnesses(self.control)
        checked = 0
        for row in old["findings"]:
            if row["status"] != "MISMATCH":
                continue
            ref = parse_ref(row["ref"])
            self.assertIsNotNone(ref)
            book, chapter, first, last = ref
            for name, verses in corpora:
                text = " ".join(verses[(book, chapter, v)] for v in range(first, last + 1))
                with self.subTest(file=row["file"], line=row["line"], witness=name):
                    self.assertEqual(check_quote(row["quote_in_draft"], text)[0], "MISMATCH")
            checked += 1
        self.assertEqual(checked, 22)

    def test_deleting_a_quote_cannot_make_the_audit_green(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            for path in (ROOT / DRAFTS).glob("*.md"):
                (target / path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            path = target / "01_what-is-atonement.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("(1 Ин. 2:2, Синодальный)", "(примечание)", 1), encoding="utf-8")
            rows = audit_quotes(target, witnesses(self.control))
            self.assertNotEqual(len(rows), self.report["markedCitationCount"])

    def test_lost_repair_record_is_detected(self):
        broken = deepcopy(self.report)
        broken["repairs"] = [r for r in broken["repairs"] if r["id"] != "Q01"]
        self.assertTrue(any("Q01" in error for error in check_repairs(ROOT, broken)))

    def test_empty_witness_is_refused(self):
        broken = deepcopy(self.control)
        broken["sources"]["rst"]["verses"] = []
        with self.assertRaises(ValueError):
            witnesses(broken)

    def test_evidence_class_access_locator_rights_and_publication_stay_separate(self):
        for field, invalid in (("evidenceClass", "PUBLICATION_HOLD"), ("accessState", "A1"),
                               ("locatorState", "FULL_OBJECT_VERIFIED"), ("rightsState", "A1"),
                               ("publicationState", "PROMOTE")):
            with self.subTest(axis=field):
                broken = deepcopy(self.control)
                broken["sources"]["rst"][field] = invalid
                with self.assertRaises(ValueError):
                    witnesses(broken)

    def test_pin_change_is_detected(self):
        broken = deepcopy(self.control)
        broken["sources"]["rst"]["commit"] = SOURCES["rsb"][1]
        with self.assertRaises(ValueError):
            witnesses(broken)

    def test_fabricated_greek_control_is_detected(self):
        broken = deepcopy(self.control)
        for row in broken["sources"]["py-sblgnt"]["verses"]:
            if (row["book"], row["chapter"], row["verse"]) == ("Евр", 2, 9):
                row["text"] += " μάλιστα"
        self.assertTrue(check_greek(broken, self.report["greekChecks"]))

    def test_titus_verse_19_is_detected(self):
        broken = deepcopy(self.control)
        broken["sources"]["py-sblgnt"]["chapterVerseNumbers"]["Тит|2"].append(19)
        self.assertTrue(check_greek(broken, self.report["greekChecks"]))

    def test_gate_does_not_write_repository_files(self):
        paths = {ROOT / r["file"] for r in self.report["repairs"]} | {ROOT / REPORT, ROOT / CONTROL}
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        check(ROOT, self.report, self.control)
        after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
