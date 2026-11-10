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
import subprocess
import sys
import unittest
from collections import Counter
from unittest.mock import patch
import unicodedata

import atonement_reshoot_state as reshoot
import atonement_wave3_sources as wave3
import atonement_wave4_sources as wave4
import atonement_wave5_sources as wave5
import atonement_wave6_sources as wave6
import atonement_wave7_sources as wave7
import atonement_wave8_sources as wave8
import atonement_wave9_sources as wave9
from atonement_source_metrics import source_label_prefix, legacy_carrier_code

from atonement_claim_register import classify_token
from atonement_crossref_audit import FILE_REF, main as crossref_main
from atonement_draft_citation_audit import audit_quotes, check_quote, load_bible, parse_ref
from atonement_sync_check import (ROOT, REPORT, CONTROL, DRAFTS, SYNTHESIS_REPAIR_IDS,
                                  check, check_greek, check_repairs, check_wave2,
                                  verify_pdf_bytes, verify_pdf_page_controls, witnesses)
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

    def test_section_inside_second_markdown_link_belongs_to_second_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drafts = root / "drafts"
            drafts.mkdir()
            (root / "01_hard.md").write_text("## 3. H3 context\n", encoding="utf-8")
            (root / "02_nt.md").write_text("## 08.20 Correct NT section\n", encoding="utf-8")
            (drafts / "01_draft.md").write_text(
                "[H3](../01_hard.md), [NT 08 §08.20](../02_nt.md)\n",
                encoding="utf-8",
            )
            with redirect_stdout(io.StringIO()):
                status = crossref_main(["--drafts", str(drafts), "--check"])
            self.assertEqual(status, 0)

    def test_wrong_section_inside_second_link_cannot_borrow_first_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drafts = root / "drafts"
            drafts.mkdir()
            (root / "01_hard.md").write_text("## 08.20 Only in first\n", encoding="utf-8")
            (root / "02_nt.md").write_text("## 08.19 Not the cited section\n", encoding="utf-8")
            (drafts / "01_draft.md").write_text(
                "[H3](../01_hard.md), [NT 08 §08.20](../02_nt.md)\n",
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                status = crossref_main(["--drafts", str(drafts), "--check"])
            self.assertEqual(status, 1)
            self.assertIn("SECTION_NOT_FOUND", output.getvalue())
            self.assertIn("02_nt.md", output.getvalue())

    def test_real_research_draft_sections_resolve(self):
        output = io.StringIO()
        with redirect_stdout(output):
            status = crossref_main(["--check"])
        self.assertEqual(status, 0, output.getvalue())


class ActualSynchronizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text(encoding="utf-8"))
        cls.control = json.loads((ROOT / CONTROL).read_text(encoding="utf-8"))

    def test_colossians_1_22_both_edition_readings_are_named(self):
        card = (ROOT / "ИСКУПЛЕНИЕ/nt/07_NT_PERICOPE_CARDS_ACTS_AND_PAUL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("ἀποκατηλλάγητε", card)
        self.assertIn("ἀποκατήλλαξεν", card)
        self.assertIn("SBLGNT", card)
        self.assertIn("NA28", card)

    def test_article13_separates_critical_source_holds(self):
        p = ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md"
        text = p.read_text(encoding="utf-8")
        for marker in (
            "DABNEY_FULL_BOOK_COLLATION_HOLD",
            "DABNEY_520_523_FACSIMILE_VERIFIED",
            "DABNEY_648_FACSIMILE_VERIFIED",
            "DAVENANT_1650_THREE_PRINT_LOCI_VERIFIED",
            "DAVENANT_LATIN_DIPLOMATIC_COLLATION_HOLD",
            "AI_TRANSLATION_HOLD",
            "OWEN_WCF_TIMING_HOLD",
            "NO PUBLICATION AUTHORIZATION",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_article13_payment_and_application_distinction_not_erased(self):
        p = ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md"
        text = p.read_text(encoding="utf-8")
        for marker in (
            "solutio ejusdem",
            "solutio tantidem",
            "actual right",
            "actual possession",
            "Дорт II.8",
            "WCF XI.4",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        self.assertIn("A1 в узком месте", text)
        self.assertIn("COARSE_LOCATOR_ONLY", text)
        self.assertIn("UNVERIFIED_TRANSCRIPTION", text)
        self.assertNotIn("**B1**", text)
        self.assertIn("**A1 scoped**", text)
        self.assertIn("DAVENANT_1650_THREE_PRINT_LOCI_VERIFIED", text)
        self.assertIn("DABNEY_FULL_BOOK_COLLATION_HOLD", text)

    def test_article02_sacrifice_covenant_distinguishes_rituals_and_has_semantic_claim_map(self):
        rel = "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md"
        p = ROOT / rel
        article = p.read_text(encoding="utf-8")
        plan = (ROOT / "ИСКУПЛЕНИЕ/synthesis/01_SERIES_PLAN_AND_ARTICLE_COUNT.md").read_text(encoding="utf-8")
        for marker in (
            "ARTICLE 02 / 18", "Исх. 12:13", "Исх. 24:8",
            "Лев. 5:11–13", "Лев. 16:21–22", "Лев. 17:11",
            "Ис. 52:15", "Ис. 53:4", "Евр. 9:12", "Евр. 9:22",
            "святилище", "живым", "почти", "Евр. 10:1–4",
            "AT-010", "LOCATOR_HOLD", "RIGHTS_HOLD",
            "PUBLICATION_HOLD", "не", "Göttingen",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, article)
        for i in range(1, 22):
            with self.subTest(claim=i):
                self.assertEqual(article.count("| F02-%02d |" % i), 1)
        self.assertEqual(article.count("| F02-"), 21)
        self.assertIn("article02_sacrifice_covenant_passover_day_of_atonement.md", plan)
        self.assertIn("исторического черновика", plan)
        for source in (
            "../../ot/06_PESAH_EXOD12.md",
            "../../ot/10_EXOD24_GEN22.md",
            "../../ot/07_LEV1_7_SISTEMA_ZHERTV.md",
            "../../ot/08_LEV16_KAPPORET_AZAZEL.md",
            "../../ot/11_ISA52_53_SERVANT.md",
            "../../nt/08_NT_PERICOPE_CARDS_HEBREWS_CATHOLICS_APOCALYPSE.md",
        ):
            with self.subTest(source=source):
                self.assertTrue((p.parent / source).resolve().is_file())
        controls = json.loads((ROOT / "ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json").read_text(encoding="utf-8"))
        matching = [m for m in controls.get("postReviewDrafts", []) if m.get("path") == rel]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["sha256"], hashlib.sha256(p.read_bytes()).hexdigest())
        self.assertFalse(matching[0]["publicationEligible"])

    def test_article02_semantic_review_keeps_eight_counterreadings_and_text_boundaries(self):
        article_path = ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md"
        memo_path = ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md"
        article = article_path.read_text(encoding="utf-8")
        memo = memo_path.read_text(encoding="utf-8")
        for i in (1, 3, 6, 9, 13, 16, 17, 20):
            with self.subTest(claim=i):
                self.assertEqual(memo.count("### F02-%02d —" % i), 1)
        self.assertEqual(memo.count("**Сильнейшее возражение:**"), 8)
        self.assertEqual(memo.count("**Итог:**"), 8)
        self.assertIn("../../evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md", article)
        for marker in (
            "Исх. 13:13–15", "Числ. 3", "Евр. 9:19",
            "σχεδόν", "χωρὶς αἱματεκχυσίας", "не повторяет слова «почти»",
            "τῷ ἀποπομπαίῳ", "εἰς τὴν ἀποπομπήν",
            "τὸν διεσταλμένον εἰς ἄφεσιν", "θαυμάσονται",
            "τοῖς αὐτὸν ἀπεκδεχομένοις", "не** две «предложные группы»",
            "article01_what_is_atonement_biblical_language_and_work.md", "02_why-the-cross-necessity.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, article if marker != "не** две «предложные группы»" else memo)
        for source in (
            "../ot/06_PESAH_EXOD12.md",
            "../ot/02_GAL_PADAH_PIDYON.md",
            "../ot/08_LEV16_KAPPORET_AZAZEL.md",
            "../nt/08_NT_PERICOPE_CARDS_HEBREWS_CATHOLICS_APOCALYPSE.md",
        ):
            with self.subTest(source=source):
                self.assertTrue((memo_path.parent / source).resolve().is_file())
        self.assertIn("не внешнее рецензирование", memo)
        self.assertTrue((article_path.parent / "01_what-is-atonement.md").is_file(), "historic article01 remains intact")
        self.assertIn("PUBLICATION_HOLD", memo)
        self.assertIn("publicationEligible=false", memo)

    def test_article02_external_primary_and_competing_scholarly_readings_are_guarded(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        for marker in (
            "без масла и ладана", "приношением **за грех**",
            "σχεδόν", "синтаксически", "риторическое",
            "Элликотт", "τοῦ ἀποπομπαίου",
            "εἰς τὴν ἀποπομπήν",
            "τὸν διεσταλμένον εἰς ἄφεσιν",
            "RHETORICAL_SCOPE_OPEN", "ETYMOLOGY_HOLD",
        ):
            with self.subTest(article_marker=marker):
                self.assertIn(marker, article)
        for marker in (
            "## AT-010-R2", "R2-09", "R2-13",
            "https://www.saet.ac.uk/Christianity/SacrificeandtheOldTestament",
            "https://www.die-bibel.de/en/bible/LXX/LEV.16",
            "https://www.kingjamesbibleonline.org/Hebrews-9_Commentary-Ellicott/",
            "https://www.bsw.org/biblica/",
            "De Roo", "NET Bible", "печaт",
            "RHETORICAL_SCOPE_OPEN", "ETYMOLOGY_HOLD",
            "Публикационный статус", "STOP_DISCOVERY",
        ):
            with self.subTest(memo_marker=marker):
                if marker != "печaт":
                    self.assertIn(marker, memo)
        self.assertIn("AT-010-R2", board)
        self.assertIn("PUBLICATION_HOLD", memo)

    def test_article02_isaiah_r3_publisher_text_syntax_and_reception_remain_separate(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        source = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        for marker in (
            "גּוֹיִם רַבִּים", "без обычного", "θαυμάσονται",
            "חֳלָיֵנוּ", "מַכְאֹבֵינוּ",
            "οὗτος τὰς ἁμαρτίας ἡμῶν φέρει",
            "ἀσθενείας", "νόσους", "δῶτε", "ὑμῶν",
            "2-е лицо множ.", "3-е лицо жен. ед.",
            "SYNTAX_LEXEME_OPEN", "RECEPTION_SCOPE_OPEN",
        ):
            with self.subTest(article=marker):
                self.assertIn(marker, article)
        for marker in (
            "## AT-010-R3", "R3-17", "R3-16", "R3-10",
            "https://www.die-bibel.de/en/bible/LXX/ISA.52",
            "https://www.die-bibel.de/en/bible/LXX/ISA.53",
            "https://biblia.com/bible/sblgnt/matthew/8/16-18",
            "Rahlfs", "Hanhart", "2006",
            "NET Bible", "παιδία", "παιδεία",
            "EDITION_WITNESS_HOLD", "EDITORIAL_TRANSCRIPTION_HOLD",
            "ARCHIVE_HOLD", "RIGHTS_HOLD",
            "publicationEligible=false", "STOP_DISCOVERY",
        ):
            with self.subTest(memo=marker):
                self.assertIn(marker, memo)
        for marker in ("## 11. R3", "53:5", "παιδία", "παιδεία", "53:10",
                       "SYNTAX_LEXEME_OPEN", "EDITION_WITNESS_HOLD", "PUBLICATION_HOLD"):
            with self.subTest(source=marker):
                self.assertIn(marker, source)
        self.assertIn("## 13. AT-010-R3", board)
        self.assertIn("201/201", board)
        self.assertIn("NO MERGE / NO PUBLICATION", board)

    def test_article02_r4_swete_print_pages_and_editorial_variants_are_separate_from_manuscripts(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        owner = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        for marker in ("Фотография печатной страницы Суита", "1905",
                       "παιδία εἰρήνης ἡμῶν", "παιδεία εἰρήνης ἡμῶν",
                       "ἡ ψυχὴ ἡμῶν", "ἡ ψυχὴ ὑμῶν",
                       "подтверждённое различие опубликованных редакций",
                       "F02-16 |", "F02-17 |"):
            with self.subTest(article_marker=marker):
                self.assertIn(marker, article)
        for marker in ("## AT-010-R4", "с. 199", "с. 200", "с. 201",
                       "https://ccel.org/ccel/swete/lxx3/lxx3/Page_199.html",
                       "https://ccel.org/ccel/swete/lxx3/lxx3/Page_200.html",
                       "https://ccel.org/ccel/swete/lxx3/lxx3/Page_201.html",
                       "https://www.die-bibel.de/en/bible/LXX/ISA.53",
                       "SWETE_III_PRINT_FACSIMILE_VERIFIED",
                       "EDITION_VARIANT_LOCATED",
                       "GOTTINGEN_APPARATUS_HOLD", "OTTLEY_1906_PRINT_HOLD",
                       "CODEX_WITNESS_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD",
                       "publicationEligible=false", "STOP_DISCOVERY"):
            with self.subTest(memo_marker=marker):
                self.assertIn(marker, memo)
        self.assertIn("## 12. R4", owner)
        self.assertIn("SWETE_III_PRINT_FACSIMILE_VERIFIED", owner)
        self.assertIn("## 14. AT-010-R4", board)
        self.assertIn("NO MERGE / NO PUBLICATION", board)

    def test_article02_r5_ottley_1906_print_and_reported_witnesses_are_scoped(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        source = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        for marker in ("Оттли (1906)", "παιδία εἰρήνης ἡμῶν", "παιδεία",
                       "ἡ ψυχὴ ὑμῶν", "ἡ ψυχὴ ἡμῶν", "ψυχή",
                       "ἐμαλακίσθη", "μεμαλάκισται",
                       "Göttingen"):
            with self.subTest(article_marker=marker):
                self.assertIn(marker, article)
        for marker in ("## AT-010-R5", "PDF стр. 351", "PDF 466", "PDF 467",
                       "PDF 726", "PDF 727", "PDF 730", "PDF 775",
                       "https://abramkj.com/wp-content/uploads/2012/12/ottley_isaiah-according-to-the-lxx.pdf",
                       "4b5ef257c0b9744d813ff98aa54f320fbce00b28705f0ee524d58edd437dd3be",
                       "OTTLEY_II_1906_PRINT_FACSIMILE_VERIFIED",
                       "EDITION_VARIANT_LOCATED", "ἐμαλακίσθη", "μεμαλάκισται",
                       "συνάξουσιν", "συνέξουσιν",
                       "ῥαντισεῖ", "CODEX_WITNESS_HOLD",
                       "GOTTINGEN_APPARATUS_HOLD", "RIGHTS_HOLD",
                       "PUBLICATION_HOLD", "publicationEligible=false", "STOP_DISCOVERY"):
            with self.subTest(memo_marker=marker):
                self.assertIn(marker, memo)
        self.assertIn("## 13. AT-010-R5", source)
        self.assertIn("OTTLEY_II_1906_PRINT_FACSIMILE_VERIFIED", source)
        self.assertIn("## 15. AT-010-R5", board)
        self.assertIn("NO MERGE / NO PUBLICATION", board)

    def test_article02_r6_coptic_sahidic_critical_edition_not_greek_manuscript(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        source = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        for marker in ("Бонка (2023", "sa 52", "sa 48", "ⲛϣⲏⲣⲉ",
                       "παιδεία", "παιδία", "53:10",
                       "коптскую", "не доказана"):
            with self.subTest(article_marker=marker):
                self.assertIn(marker, article)
        for marker in ("## AT-010-R6", "41/4 (2023)", "печат. с. 861",
                       "с. 868", "с. 875", "DOI",
                       "10.31743/vv.16174",
                       "https://czasopisma.kul.pl/index.php/vv/article/download/16174/14711/75589",
                       "https://www.themorgan.org/collection/isaiah/77430/115",
                       "https://www.themorgan.org/collection/isaiah/77430/116",
                       "https://bodmerlab.unige.ch/fr/constellations/papyri/barcode/1072205362",
                       "page=034", "sa 48", "n+yHre", "n+te(n)irHnH",
                       "tetn+TuCH", "tepn+TuCH",
                       "PUBLISHED_SAHIDIC_CRITICAL_EDITION_VERIFIED",
                       "COPTIC_CHILDREN_READING_LOCATED",
                       "GREEK_VORLAGE_AMBIGUOUS",
                       "GREEK_BACKTRANSLATION_HOLD",
                       "GOTTINGEN_APPARATUS_HOLD",
                       "CODEX_WITNESS_HOLD", "RIGHTS_HOLD",
                       "PUBLICATION_HOLD", "publicationEligible=false",
                       "STOP_DISCOVERY"):
            with self.subTest(memo_marker=marker):
                self.assertIn(marker, memo)
        self.assertIn("## 14. AT-010-R6", source)
        self.assertIn("GREEK_VORLAGE_AMBIGUOUS", source)
        self.assertIn("## 16. AT-010-R6", board)
        self.assertIn("NO MERGE / NO PUBLICATION", board)

    def test_article02_r7_bodmer_photo_frame_locator_corrects_034_without_greek_promotion(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        owner = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        for marker in ("проверка первичных фотографий", "кадр 034",
                       "кадр 041", "кадр 042", "53:5", "53:10",
                       "непосредственно просмотрены", "не удостоверено",
                       "παιδία / παιδεία"):
            with self.subTest(article_marker=marker):
                self.assertIn(marker.lower(), article.lower())
        for marker in ("## AT-010-R7", "95 canvases", "6132 × 8176",
                       "034", "50, 11–51, 4", "041", "53, 3–8",
                       "042", "53, 8–12", "039", "040", "043",
                       "https://bodmerlab.unige.ch/fr/constellations/papyri/manifest/1072205362?page=041",
                       "https://bodmerlab.unige.ch/fr/constellations/papyri/mirador/1072205362?page=041",
                       "https://bodmerlab.unige.ch/fr/constellations/papyri/mirador/1072205362?page=042",
                       "fc1dc1759f728e49401c521964be370e3165e2039cded04220728f8d5a0bcc3f",
                       "eb17fcf65a96c9da0d43ca5712a64dd15c3175e371edde5a9da9e9f56cb556d4",
                       "BODMER23_FRAME_VERIFIED", "SA48_GLYPH_READ_HOLD",
                       "MORGAN_M568_IMAGE_ACCESS_HOLD",
                       "GREEK_VORLAGE_AMBIGUOUS",
                       "GOTTINGEN_APPARATUS_HOLD", "CODEX_WITNESS_HOLD",
                       "RIGHTS_HOLD", "PUBLICATION_HOLD",
                       "publicationEligible=false", "STOP_DISCOVERY"):
            with self.subTest(memo_marker=marker):
                self.assertIn(marker, memo)
        self.assertIn("## 15. AT-010-R7", owner)
        self.assertIn("## 17. AT-010-R7", board)
        self.assertIn("SUPERSEDED", owner)
        self.assertIn("NO MERGE / NO PUBLICATION", board)
        self.assertIn("Bąk", memo)
        self.assertIn("не установлена", memo)

    def test_article02_r8_decot_original_glyphs_and_editor_conflict_are_scoped(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        owner = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        for marker in ("Прямая сверка коптских рукописей (R8)", "M.568", "ⲛ︦ϣⲏⲣⲉ",
                       "ⲧⲉⲧⲛ︦ⲯⲩⲭⲏ", "ⲛ̄ϣⲏⲣⲉ", "ⲧⲉⲧ̣ⲛ̄",
                       "спор об одной повреждённой букве", "παιδία/παιδεία"):
            with self.subTest(article_marker=marker):
                self.assertIn(marker, article)
        for marker in ("## AT-010-R8", "pageID 1140", "pageID 260", "pageID 270",
                       "NML_M568.f.054v_lib.jpg",
                       "CFB_PBodmerXXIII.f.013v_bscan.jpg",
                       "CFB_PBodmerXXIII.f.014r_bscan.jpg",
                       "6f551d9971f0840284ade1a0fdf4b9b96f45692859aa1cd5dfb7dd9e3b2afacc",
                       "88f40df3d06c6bf7ef47a057d7d10e130ec7f776ff1aac08f141dc566feb0207",
                       "50c7d0437d7902b146fdc1bbbb7f62f3901de893c7f0ce46060fbd485f241537",
                       "ⲛ︦", "ϣⲏⲣⲉ", "ⲛⲧⲛ︦ⲉⲓⲣⲏⲛⲏ", "ⲛ̄ϣⲏⲣⲉ",
                       "ⲧⲉⲧⲛ︦ⲯⲩ", "ⲧⲉⲧ̣ⲛ̄", "ⲯⲩⲭⲏ",
                       "MORGAN_M568_FOLIO_AND_TARGET_GLYPHS_VERIFIED",
                       "DECOT_BAK_ONE_GLYPH_DISAGREEMENT_LOCATED",
                       "SA48_53_10_GLYPH_ADJUDICATION_HOLD",
                       "GREEK_VORLAGE_AMBIGUOUS", "GREEK_BACKTRANSLATION_HOLD",
                       "GOTTINGEN_APPARATUS_HOLD", "CODEX_WITNESS_HOLD",
                       "RIGHTS_HOLD", "PUBLICATION_HOLD",
                       "publicationEligible=false", "STOP_DISCOVERY"):
            with self.subTest(memo_marker=marker):
                self.assertIn(marker, memo)
        self.assertIn("## 16. AT-010-R8", owner)
        self.assertIn("## 18. AT-010-R8", board)
        self.assertIn("SUPERSEDED", owner)
        self.assertIn("NO MERGE / NO PUBLICATION", board)

    def test_article02_r9_coptic_witnesses_have_no_false_collation(self):
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        registry = (ROOT / "ИСКУПЛЕНИЕ/05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md").read_text(encoding="utf-8")
        self.assertIn("## AT-010-R9", memo)
        r9 = memo.split("## AT-010-R9",1)[-1]
        for doc,page in (("622148","2250"),("620292","3090"),("622028","350"),("620016","2575")):
            locator="docid="+doc+"&pageID="+page+"&format=xhtml"
            self.assertIn(locator, r9)
            self.assertIn(locator, registry)
        for marker in ("ⲉⲧⲉⲧⲛ", "ⲧⲉⲧ︤ⲛ︥ⲯⲩⲭⲏ", "TARGET_CLAUSE_NOT_PRESENT", "PHOTO_NOT_COLLATED", "PROTECTED_IMAGE_ACCESS_HOLD", "CLM3469_EDITORIAL_READ_CONFLICT_HOLD", "SA48_53_10_GLYPH_ADJUDICATION_HOLD", "GREEK_BACKTRANSLATION_HOLD", "GOTTINGEN_APPARATUS_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD", "publicationEligible=false"):
            self.assertIn(marker, r9)
        self.assertIn("## 19. AT-010-R9", board)
        self.assertIn("NO MERGE / NO PUBLICATION", board)

    def test_active_reader_sources_match_root_evidence_policy(self):
        import re
        import json
        import hashlib
        policy = json.loads((ROOT / "data/repository-evidence-policy-v2.json").read_text(encoding="utf-8"))
        self.assertEqual(set(policy["sourceClasses"]), {"A1", "A2", "A3", "B1", "C", "D"})
        files = (
            "article08_particular_redemption_positive_case.md",
            "article09_world_and_propitiation_johannine_case.md",
            "article10_ransom_for_all_two_adams_paul_hebrews.md",
            "article11_bought_apostates_covenant_blood_and_weak_brother.md",
            "article12_cosmic_reconciliation_heaven_earth_new_creation.md",
            "article13_double_payment_unbelief_and_acquired_faith.md",
        )
        expected_a1 = (0, 2, 3, 6, 4, 5)
        expected_a3 = (2, 1, 0, 0, 0, 2)
        manifest = {x["path"]: x for x in self.report["postReviewDrafts"]}
        for name, e1, e3 in zip(files, expected_a1, expected_a3):
            path = ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts" / name
            text = path.read_text(encoding="utf-8")
            rows = [line for line in text.splitlines() if line.startswith("| ") and line.count("|") >= 4]
            evidence_cells = [line.split("|")[2] for line in rows if len(line.split("|")) >= 5]
            with self.subTest(draft=name):
                self.assertGreaterEqual(sum(bool(re.search(r"\bA1\b", x)) for x in evidence_cells), e1, "primary author slots remain A1")
                self.assertGreaterEqual(sum(bool(re.search(r"\bA3\b", x)) for x in evidence_cells), e3)
                self.assertFalse(any(re.search(r"\bA2\b", x) for x in evidence_cells), "A2 is not the author/official-confession class")
                self.assertFalse(any(re.match(r"\s*C(?:[,:]|\s)", x) for x in evidence_cells), "C-class sources belong outside the primary evidence table")
                self.assertIn("PUBLICATION_HOLD", text)
                rel = "ИСКУПЛЕНИЕ/synthesis/drafts/" + name
                self.assertIn(rel, manifest)
                self.assertFalse(manifest[rel]["publicationEligible"])
                self.assertEqual(manifest[rel]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        # OPC 1948 remains an A2 institutional report; official confessions are A3.
        historic = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/09_free-offer-of-the-gospel.md").read_text(encoding="utf-8")
        self.assertIn("A2 (публичный церковный отчёт", historic)
        section13 = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md").read_text(encoding="utf-8")
        self.assertIn("UNVERIFIED_TRANSCRIPTION", section13)
        self.assertNotIn("**B1** — остальная цифровая транскрипция", section13)

    def test_reader_05_06_canonical_accomplishment_application_boundary(self):
        import hashlib
        import re
        base = ROOT / "ИСКУПЛЕНИЕ/synthesis"
        plan = (base / "01_SERIES_PLAN_AND_ARTICLE_COUNT.md").read_text(encoding="utf-8")
        board = (base / "07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        one = "article05_once_for_all_sacrifice_living_high_priest.md"
        two = "article06_accomplishment_union_faith_justification.md"
        ch4 = (base / "drafts/article04_substitution_victory_reconciliation_how_cross_saves.md").read_text(encoding="utf-8")
        self.assertIn("## 28. READER-W3", board)
        self.assertIn("](" + one + ")", ch4)
        manifest = {item["path"]: item for item in self.report["postReviewDrafts"]}
        for number, name, historic in (
            (5, one, "04_perfection-of-atonement.md"),
            (6, two, "11_order-of-salvation.md"),
        ):
            path = base / "drafts" / name
            reader = path.read_text(encoding="utf-8")
            rel = "ИСКУПЛЕНИЕ/synthesis/drafts/" + name
            with self.subTest(chapter=number):
                self.assertGreater(len(reader), 17000)
                self.assertIn("ARTICLE %02d / 18" % number, reader)
                self.assertIn("drafts/" + name, plan)
                self.assertEqual(len(set(re.findall(r"F%02d-\d{2}" % number, reader))), 12)
                self.assertTrue((base / "drafts" / historic).is_file())
                self.assertIn(historic, reader)
                for boundary in ("EVIDENCE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD", "publicationEligible=false"):
                    self.assertIn(boundary, reader)
                self.assertNotIn("publicationEligible=true", reader)
                self.assertIn(rel, manifest)
                self.assertFalse(manifest[rel]["publicationEligible"])
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), manifest[rel]["sha256"])
        ch5 = (base / "drafts" / one).read_text(encoding="utf-8")
        ch6 = (base / "drafts" / two).read_text(encoding="utf-8")
        self.assertIn("](" + two + ")", ch5)
        self.assertIn("Евр. 10:29", ch5)
        self.assertIn("Евр. 7:25", ch5)
        self.assertIn("Евр. 10:14", ch5)
        self.assertIn("Пс. 39", ch5)
        self.assertIn("Дорт", ch5)
        for marker in ("Еф. 2:8", "Флп. 1:29", "Дорт", "Рим. 8:29–30", "оправдание", "во времени", "проповед"):
            with self.subTest(ch6_marker=marker):
                self.assertIn(marker, ch6)
        self.assertIn("CONFESSIONAL_HOLD", ch6)
        self.assertIn("LEXICAL_SCOPE_HOLD", ch6)

    def test_reader_03_04_new_canonical_route_keeps_primary_boundaries(self):
        import re
        import hashlib
        base = ROOT / "ИСКУПЛЕНИЕ/synthesis"
        plan = (base / "01_SERIES_PLAN_AND_ARTICLE_COUNT.md").read_text(encoding="utf-8")
        board = (base / "07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        ch2 = (base / "drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        names = (
            ("article03_why_cross_love_holiness_justice.md", "02_why-the-cross-necessity.md", "F03"),
            ("article04_substitution_victory_reconciliation_how_cross_saves.md", "03_nature-of-atonement.md", "F04"),
        )
        self.assertIn("## 27. READER-W2", board)
        manifest = {x["path"]: x for x in self.report["postReviewDrafts"]}
        for name, historic, marker in names:
            path = base / "drafts" / name
            txt = path.read_text(encoding="utf-8")
            rel = "ИСКУПЛЕНИЕ/synthesis/drafts/" + name
            with self.subTest(chapter=name):
                self.assertGreater(len(txt), 17500)
                self.assertIn("ARTICLE " + marker[1:] + " / 18", txt)
                self.assertIn("drafts/" + name, plan)
                self.assertEqual(len(set(re.findall(marker + r"-\d{2}", txt))), 12)
                self.assertIn(historic, txt)
                self.assertTrue((base / "drafts" / historic).is_file())
                for hold in ("EVIDENCE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD", "publicationEligible=false"):
                    self.assertIn(hold, txt)
                self.assertNotIn("publicationEligible=true", txt)
                self.assertIn(rel, manifest)
                self.assertFalse(manifest[rel]["publicationEligible"])
                self.assertEqual(manifest[rel]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertIn("article03_why_cross_love_holiness_justice.md", ch2)
        reader3 = (base / "drafts" / names[0][0]).read_text(encoding="utf-8")
        reader4 = (base / "drafts" / names[1][0]).read_text(encoding="utf-8")
        self.assertIn(names[1][0], reader3)
        for marker in ("Лев. 5:11–13", "Евр. 9:22", "Ансельм", "Дорт", "Гроци", "гипотетичес", "последовательн"):
            with self.subTest(reader3_marker=marker):
                self.assertIn(marker, reader3)
        for marker in ("Ис. 53", "Гал. 3:13", "2 Кор. 5", "Christus Victor", "невиновн", "примирен", "ETHICAL_OBJECTION_OPEN"):
            with self.subTest(reader4_marker=marker):
                self.assertIn(marker, reader4)

    def test_reader_01_02_canonical_recast_keeps_textual_claims(self):
        import hashlib
        import re
        base = ROOT / "ИСКУПЛЕНИЕ/synthesis"
        plan = (base / "01_SERIES_PLAN_AND_ARTICLE_COUNT.md").read_text(encoding="utf-8")
        board = (base / "07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        one = "article01_what_is_atonement_biblical_language_and_work.md"
        two = "article02_sacrifice_covenant_passover_day_of_atonement.md"
        f1 = base / "drafts" / one
        f2 = base / "drafts" / two
        a = f1.read_text(encoding="utf-8")
        b = f2.read_text(encoding="utf-8")
        self.assertGreater(len(a), 16000)
        self.assertGreater(len(b), 35000)
        self.assertIn("ARTICLE 01 / 18", a)
        self.assertIn("ARTICLE 02 / 18", b)
        self.assertIn("drafts/" + one, plan)
        self.assertIn("drafts/" + two, plan)
        self.assertIn("## 26. READER-W1", board)
        self.assertIn("article01_what_is_atonement_biblical_language_and_work.md", b)
        self.assertTrue((base / "drafts/01_what-is-atonement.md").is_file(), "historic first chapter is retained")
        self.assertEqual(len(set(re.findall(r"F01-\d{2}", a))), 12)
        self.assertEqual(len(set(re.findall(r"F02-\d{2}", b))), 21)
        self.assertIn("## Текстологическое приложение: Ис. 52–53 (R3–R18)", b)
        self.assertLess(b.index("## 7. Послание к Евреям"), b.index("## Текстологическое приложение"))
        self.assertLess(b.index("## Приложение для научной редакции"), b.index("## Текстологическое приложение"))
        for marker in ("Swete", "Оттли", "Bodmer XXIII", "Codex Marchalianus Q", "4Q58", "1Q8", "Göttingen"):
            with self.subTest(textual_witness=marker):
                self.assertIn(marker, b)
        manifest = {entry["path"]: entry for entry in self.report["postReviewDrafts"]}
        for name, file, content in ((one, f1, a), (two, f2, b)):
            rel = "ИСКУПЛЕНИЕ/synthesis/drafts/" + name
            with self.subTest(draft=name):
                self.assertIn(rel, manifest)
                self.assertFalse(manifest[rel]["publicationEligible"])
                self.assertEqual(manifest[rel]["sha256"], hashlib.sha256(file.read_bytes()).hexdigest())
                self.assertIn("PUBLICATION_HOLD", content)
                self.assertIn("RIGHTS_HOLD", content)
                self.assertNotIn("publicationEligible=true", content)

    def test_reader_15_and_16_confessional_sources_not_publication(self):
        base = ROOT / "ИСКУПЛЕНИЕ/synthesis"
        plan = (base / "01_SERIES_PLAN_AND_ARTICLE_COUNT.md").read_text(encoding="utf-8")
        board = (base / "07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        registry = (ROOT / "ИСКУПЛЕНИЕ/05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md").read_text(encoding="utf-8")
        manifest = self.report["postReviewDrafts"]
        paths = {entry["path"] for entry in manifest}
        for name, chapter, last, hold in (
            ("article15_dort_westminster_saumur_english_hu.md", "ARTICLE 15 / 18", "F15-07", "ATTRIBUTION_HOLD"),
            ("article16_boundaries_calvinism_reformed_family.md", "ARTICLE 16 / 18", "F16-07", "CONFESSIONAL_REVIEW_HOLD"),
        ):
            rel = "ИСКУПЛЕНИЕ/synthesis/drafts/" + name
            data = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(chapter=name):
                self.assertGreater(len(data), 16000)
                self.assertIn(chapter, data)
                self.assertIn(last, data)
                self.assertIn(hold, data)
                self.assertIn("RIGHTS_HOLD", data)
                self.assertIn("PUBLICATION_HOLD", data)
                self.assertIn("publicationEligible=false", data)
                self.assertNotIn("publicationEligible=true", data)
                self.assertIn(rel, paths, "every new reader chapter requires a pinned manifest entry")
                self.assertIn("drafts/" + name, plan)
        self.assertIn("## 24. READER-15", board)
        self.assertIn("## 25. READER-16", board)
        for marker in ("H15-DORT-II", "H15-WCF-1689", "H15-DEVENANT-AMYRAUT", "H16-MODEL-AXES"):
            self.assertIn(marker, registry)

    def test_reader_14_and_18_new_standalone_drafts_not_publication(self):
        base = ROOT / "ИСКУПЛЕНИЕ/synthesis"
        plan = (base / "01_SERIES_PLAN_AND_ARTICLE_COUNT.md").read_text(encoding="utf-8")
        board = (base / "07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        registry = (ROOT / "ИСКУПЛЕНИЕ/05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md").read_text(encoding="utf-8")
        for name, label, last in (
            ("article14_early_church_to_reformation_history.md", "ARTICLE 14 / 18", "F14-07"),
            ("article18_living_atonement_holiness_church_mission_suffering.md", "ARTICLE 18 / 18", "F18-07"),
        ):
            content = (base / "drafts" / name).read_text(encoding="utf-8")
            with self.subTest(chapter=name):
                self.assertGreater(len(content),12000)
                self.assertIn(label,content)
                self.assertIn(last,content)
                self.assertIn("PUBLICATION_HOLD",content)
                self.assertIn("publicationEligible=false",content)
                self.assertNotIn("publicationEligible=true",content)
                self.assertIn("drafts/"+name,plan)
        self.assertIn("## 22. READER-14",board)
        self.assertIn("## 23. READER-18",board)
        for label in ("H14-ANSELM-CDH","H14-AQUINAS-ST48-49","H14-LUTHER-GAL313"):
            self.assertIn(label,registry)
    def test_article02_r18_vatican_codex_q_photo_not_full_apparatus(self):
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        ot = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        registry = (ROOT / "ИСКУПЛЕНИЕ/05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md").read_text(encoding="utf-8")
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        self.assertIn("## AT-010-R18",memo)
        r18 = memo.split("## AT-010-R18",1)[1]
        for marker in ("Codex Marchalianus", "canvas 0620", "canvas 0621–0622",
                       "ΠΑΙΔΕΙΑ ΕΙΡΗΝΗΣ ΗΜΩΝ", "ἡ ψυχὴ ὑμῶν", "LOCATOR_CORRECTED",
                       "GOTTINGEN_APPARATUS_HOLD", "GREEK_BACKTRANSLATION_HOLD",
                       "RIGHTS_HOLD", "PUBLICATION_HOLD", "publicationEligible=false"):
            with self.subTest(marker=marker): self.assertIn(marker,r18)
        self.assertIn("## 19. AT-010-R18",ot)
        self.assertIn("## 21. AT-010-R18",board)
        self.assertIn("VAT-Q-IS53-05",registry)
        self.assertIn("VAT-Q-IS53-10",registry)
        self.assertIn("Дополнительная первичная греческая сверка (R18)",article)
        self.assertNotIn("GOTTINGEN_APPARATUS_VERIFIED",r18)

    def test_article02_r17_qumran_digital_versioned_transcripts_not_photos(self):
        memo = (ROOT / "ИСКУПЛЕНИЕ/evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md").read_text(encoding="utf-8")
        ot = (ROOT / "ИСКУПЛЕНИЕ/ot/11_ISA52_53_SERVANT.md").read_text(encoding="utf-8")
        board = (ROOT / "ИСКУПЛЕНИЕ/synthesis/07_LIVING_EXECUTION_BOARD_2026-11-07.md").read_text(encoding="utf-8")
        registry = (ROOT / "ИСКУПЛЕНИЕ/05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md").read_text(encoding="utf-8")
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md").read_text(encoding="utf-8")
        self.assertIn("## AT-010-R17", memo)
        r17 = memo.split("## AT-010-R17", 1)[1]
        for marker in ("2026-05-21", "2025-08-25", "או֯[ר]", "חטאי",
                       "1Q8", "4Q58", "4Q56", "R16 SUPERSEDED",
                       "GLYPH_PHOTO_HOLD", "GOTTINGEN_APPARATUS_HOLD",
                       "RIGHTS_HOLD", "PUBLICATION_HOLD", "publicationEligible=false"):
            with self.subTest(marker=marker):
                self.assertIn(marker, r17)
        self.assertIn("## 18. AT-010-R17", ot)
        self.assertIn("## 20. AT-010-R17", board)
        self.assertIn("QD-4Q58-20260521", registry)
        self.assertIn("QD-1Q8-20250825", registry)
        self.assertIn("Текстологическое уточнение (R17", article)

    def test_noncanonical_source_classes_are_outside_support_tables(self):
        targets = (
            "article09_world_and_propitiation_johannine_case.md",
            "article10_ransom_for_all_two_adams_paul_hebrews.md",
            "article11_bought_apostates_covenant_blood_and_weak_brother.md",
            "article13_double_payment_unbelief_and_acquired_faith.md",
        )
        for name in targets:
            content = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts" / name).read_text(encoding="utf-8")
            with self.subTest(article=name):
                self.assertNotIn("B1/B2", content)
                self.assertIn("Справочные материалы (evidenceClass C, вне доказательных опор)", content)
                table = content.split("| Опора | Класс", 1)[1].split("\n\n", 1)[0]
                self.assertNotIn("| C:", table)
                self.assertNotIn("| C —", table)

    def test_article11_named_judas_primary_witnesses_and_hebrews_hold(self):
        text = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article11_bought_apostates_covenant_blood_and_weak_brother.md").read_text(encoding="utf-8")
        cards = (ROOT / "ИСКУПЛЕНИЕ/12_HARD_TEXTS_EXTENT_CARDS.md").read_text(encoding="utf-8")
        p17 = (ROOT / "docs/research/atonement/17_quote_mining_and_theological_equivocation.md").read_text(encoding="utf-8")
        for marker in (
            "14.1. Иуда Искариот", "14.2. Сильнейшее широкое возражение",
            "14.3. Граница свидетельства о Прокопенко",
            "A Display of Arminianism", "Стэнли Гауэр",
            "redemptus erat", "Сперджен", "Девенант",
            "392–398", "1855", "543–548",
            "JUDAS_NAMED_REDEMPTION_QUOTE_HOLD",
            "2026_ORAL_RESPONSE_HOLD",
            "OWEN_OTHER_LOCATORS_HOLD",
            "HEBREWS_EXEGESIS_HOLD", "PUBLICATION_HOLD",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        self.assertIn("543–548", cards)
        self.assertIn("§11", p17)
        self.assertIn("Иуда", text)

    def test_article13_time_decree_application_and_gill_countercase(self):
        text = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md").read_text(encoding="utf-8")
        for marker in (
            "Вечный замысел не означает вечного личного оправдания",
            "Серьёзное историческое возражение: Джон Гилл",
            "Турретин", "XVI.9", "600–602",
            "Гилл", "вечное активное оправдание",
            "Вестминстерское исповедание XI.4",
            "Божья вневременность — не скрытая посылка о круге искупления",
            "DABNEY_FULL_BOOK_COLLATION_HOLD",
            "DAVENANT_LATIN_DIPLOMATIC_COLLATION_HOLD",
            "AI_TRANSLATION_HOLD", "OWEN_WCF_TIMING_HOLD",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        self.assertIn("P05 §§19–31", text)
        self.assertIn("R. T. Mullins (2023)", text)
        self.assertIn("не цитируются как прочитанные", text)

    def test_wave1_primary_dabney_context_and_print_hold_stay_distinct(self):
        text = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md").read_text(encoding="utf-8")
        dossier = (ROOT / "ИСКУПЛЕНИЕ/evidence/WAVE1_DABNEY_DAVENANT_OWEN_PRIMARY_WITNESSES_2026-11-07.md").read_text(encoding="utf-8")
        for marker in ("DABNEY_520_523_FACSIMILE_VERIFIED", "DABNEY_648_FACSIMILE_VERIFIED", "DABNEY_FULL_BOOK_COLLATION_HOLD", "sermonindex.net/books/writings-of-robert-l-dabney/57"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
                self.assertIn(marker, dossier)
        for token in ("Inconclusive Proofs", "Real Proofs", "strict Calvinistic", "QUOTE_SAFE=NO"):
            self.assertIn(token.lower(), dossier.lower())

    def test_wave1_dabney_648_is_justification_not_extent(self):
        article = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md").read_text(encoding="utf-8")
        dossier = (ROOT / "ИСКУПЛЕНИЕ/evidence/WAVE1_DABNEY_DAVENANT_OWEN_PRIMARY_WITNESSES_2026-11-07.md").read_text(encoding="utf-8")
        self.assertIn("archive.org/details/syllabusnotesofc00dabn/page/648", dossier)
        self.assertIn("archive.org/details/syllabusnotesofc00dabn/page/521", dossier)
        self.assertIn("антиномист", dossier.lower())
        self.assertIn("DABNEY_FULL_BOOK_COLLATION_HOLD", article)
        self.assertIn("/page/520/mode/1up", dossier)
        self.assertIn("/page/522/mode/1up", dossier)
        self.assertIn("/page/523/mode/1up", dossier)
        self.assertIn("нравственную обязанность", article.lower())

    def test_wave1_davenant_latin_web_segments_are_not_print_pages(self):
        text = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md").read_text(encoding="utf-8")
        dossier = (ROOT / "ИСКУПЛЕНИЕ/evidence/WAVE1_DABNEY_DAVENANT_OWEN_PRIMARY_WITNESSES_2026-11-07.md").read_text(encoding="utf-8")
        for marker in ("DAVENANT_1650_THREE_PRINT_LOCI_VERIFIED", "AI_TRANSLATION_HOLD", "§75", "foedus Evangelicum"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
                self.assertIn(marker, dossier)
        self.assertIn("веб-локатор", dossier)
        for leaf in ("n10", "n41", "n78"):
            with self.subTest(leaf=leaf):
                self.assertIn(f"/page/{leaf}/mode/1up", text)
                self.assertIn(f"/page/{leaf}/mode/1up", dossier)
        self.assertIn("Именно **69**, а не 70", text)
        self.assertIn("буквальная", dossier)
        self.assertIn("PUBLICATION_HOLD", dossier)

    def test_wave0_hodge_source_target_and_owen_distinction(self):
        text = (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md").read_text(encoding="utf-8")
        self.assertIn("https://ccel.org/ccel/hodge/theology2.iv.viii.ii.html", text)
        self.assertNotIn("theology2.iv.vii.iii.html", text)
        self.assertIn("не то же самое", text)
        self.assertIn("actual right", text)
        self.assertIn("actual possession", text)

    def test_wave0_conflict_cards_are_current_without_false_closure(self):
        text = (ROOT / "ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md").read_text(encoding="utf-8")
        def section(name, following):
            begin = text.index("## " + name + ".")
            end = text.index("## " + following + ".", begin)
            return text[begin:end]
        calvin = section("C-06", "C-07")
        fathers = section("C-07", "C-08")
        confessions = section("C-14", "C-15")
        complex_case = section("C-16", "C-17")
        self.assertIn("1855", calvin)
        self.assertIn("172–173", calvin)
        self.assertNotIn("страница не в руках", calvin)
        self.assertIn("GAP-B1", calvin)
        self.assertIn("12 действующих Markdown-досье", fathers)
        self.assertNotIn("слой `fathers/` ещё не создан", fathers)
        self.assertIn("`OPEN`", fathers)
        self.assertIn("obtained eternal redemption", confessions)
        self.assertIn("purchased redemption", confessions)
        self.assertNotIn("1689 не прочитан постатейно", confessions)
        for atom in ("C16-LEX", "C16-HIST", "C16-INTENT", "C16-APPLICATION"):
            self.assertIn(atom, complex_case)
        self.assertIn("`OPEN`", complex_case)
        self.assertIn("EVIDENCE_HOLD", complex_case)

    def test_current_corpus_and_coverage(self):
        errors, summary = check(ROOT, self.report, self.control)
        self.assertEqual(errors, [])
        self.assertEqual(summary["markedCitations"], self.report["markedCitationCount"])
        # The 2026-11-02 evidence still records its historical 13-draft scope.
        # New drafts require a separately declared, byte-pinned addition.
        self.assertEqual(self.report["draftCount"], 13)
        additions = self.report.get("postReviewDrafts", [])
        self.assertEqual(summary["drafts"], self.report["draftCount"] + len(additions))
        declared_paths = {r["path"] for r in additions}
        self.assertEqual(len(declared_paths), len(additions), "duplicate post-review draft declaration")
        actual_added = {
            p.relative_to(ROOT).as_posix()
            for p in (ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts").glob("article*.md")
        }
        self.assertEqual(declared_paths, actual_added, "drafts must be fully declared in the byte-pinned manifest")
        self.assertTrue(
            {
                "ИСКУПЛЕНИЕ/synthesis/drafts/article02_sacrifice_covenant_passover_day_of_atonement.md",
                "ИСКУПЛЕНИЕ/synthesis/drafts/article08_particular_redemption_positive_case.md",
                "ИСКУПЛЕНИЕ/synthesis/drafts/article09_world_and_propitiation_johannine_case.md",
                "ИСКУПЛЕНИЕ/synthesis/drafts/article10_ransom_for_all_two_adams_paul_hebrews.md",
                "ИСКУПЛЕНИЕ/synthesis/drafts/article11_bought_apostates_covenant_blood_and_weak_brother.md",
                "ИСКУПЛЕНИЕ/synthesis/drafts/article12_cosmic_reconciliation_heaven_earth_new_creation.md",
                "ИСКУПЛЕНИЕ/synthesis/drafts/article13_double_payment_unbelief_and_acquired_faith.md",
            }.issubset(declared_paths),
            "historic seven post-review drafts must not disappear",
        )

    def test_post_review_draft_manifest_fails_closed(self):
        additions = self.report.get("postReviewDrafts", [])
        self.assertGreaterEqual(len(additions), 7)
        self.assertEqual(
            len(additions),
            len(list((ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts").glob("article*.md"))),
            "all post-review drafts must be explicitly registered",
        )
        cases = [
            (f"missing-declaration-{i}", additions[:i] + additions[i + 1 :])
            for i in range(len(additions))
        ]
        for i in range(len(additions)):
            altered_sha = list(additions)
            altered_sha[i] = {**additions[i], "sha256": "0" * 64}
            cases.append((f"incorrect-sha256-{i}", altered_sha))
            altered_publication = list(additions)
            altered_publication[i] = {**additions[i], "publicationEligible": True}
            cases.append((f"publication-authorized-{i}", altered_publication))
        for case, replacement in cases:
            with self.subTest(case=case):
                bad_report = {**self.report, "postReviewDrafts": replacement}
                errors, _ = check(ROOT, bad_report, self.control)
                self.assertTrue(errors, f"{case} unexpectedly passed")
                self.assertTrue(
                    any(
                        "draft inventory differs" in e
                        or "post-review draft bytes differ" in e
                        or "post-review draft must remain unpublished" in e
                        for e in errors
                    ),
                    errors,
                )

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


class SynthesisEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text(encoding="utf-8"))
        cls.source = cls.report["wave2"]["primaryArticle"]

    def test_canonical_permission_requirement_is_not_an_unknown_or_closed_marker(self):
        self.assertEqual(classify_token("PERMISSION_REQUIRED"), "УДЕРЖИВАЕТСЯ")

    def test_wave2_scope_and_original_git_bytes(self):
        self.assertEqual(check_wave2(ROOT, self.report), [])
        self.assertEqual(len(self.source["readPages"]), 22)
        self.assertEqual(self.source["pageCount"], 40)
        self.assertEqual(len(self.source["controls"]), 14)
        self.assertEqual(len(self.report["wave2"]["supersededSnapshots"]), 15)

    def test_missing_wave2_is_not_zero_work_success(self):
        broken = deepcopy(self.report)
        del broken["wave2"]
        self.assertTrue(check_wave2(ROOT, broken))

    def test_pdf_source_axes_cannot_be_interchanged_or_promoted(self):
        for field, value in (("evidenceClass", "OCR"), ("accessState", "A1"),
                             ("locatorState", "FULL_OBJECT_VERIFIED"), ("rightsState", "A1"),
                             ("publicationState", "PROMOTE")):
            with self.subTest(axis=field):
                broken = deepcopy(self.report)
                broken["wave2"]["primaryArticle"][field] = value
                self.assertTrue(check_wave2(ROOT, broken))

    def test_full_object_is_not_a_full_reading_claim(self):
        broken = deepcopy(self.report)
        broken["wave2"]["primaryArticle"]["fullReadingClaimed"] = True
        self.assertTrue(any("full reading" in e for e in check_wave2(ROOT, broken)))

    def test_losing_a_pdf_control_is_detected(self):
        broken = deepcopy(self.report)
        broken["wave2"]["primaryArticle"]["controls"] = [
            r for r in broken["wave2"]["primaryArticle"]["controls"] if r["id"] != "P31b"]
        self.assertTrue(check_wave2(ROOT, broken))

    def test_duplicate_pdf_control_is_detected(self):
        broken = deepcopy(self.report)
        broken["wave2"]["primaryArticle"]["controls"].append(deepcopy(self.source["controls"][0]))
        self.assertTrue(check_wave2(ROOT, broken))

    def test_unread_page_cannot_be_claimed_as_reviewed_control(self):
        broken = deepcopy(self.report)
        broken["wave2"]["primaryArticle"]["controls"][0]["pdfPage"] = 12
        self.assertTrue(any("out-of-scope" in e for e in check_wave2(ROOT, broken)))

    def test_pdf_pin_change_is_detected_offline(self):
        broken = deepcopy(self.report)
        broken["wave2"]["primaryArticle"]["sha256"] = "0" * 64
        self.assertTrue(any("byte pin" in e for e in check_wave2(ROOT, broken)))

    def test_superseded_snapshot_hash_is_checked_on_actual_bytes(self):
        for field, value in (("sha256", "0" * 64), ("blob", "0" * 40), ("bytes", 0)):
            with self.subTest(field=field):
                broken = deepcopy(self.report)
                broken["wave2"]["supersededSnapshots"][0][field] = value
                self.assertTrue(any("snapshot bytes/hash" in e for e in check_wave2(ROOT, broken)))

    def test_lost_superseded_snapshot_is_detected(self):
        broken = deepcopy(self.report)
        broken["wave2"]["supersededSnapshots"].pop()
        self.assertTrue(any("missing/duplicate superseded" in e for e in check_wave2(ROOT, broken)))

    def test_each_synthesis_repair_cannot_be_silently_reverted(self):
        tested = set()
        for row in self.report["repairs"]:
            if row["id"] not in SYNTHESIS_REPAIR_IDS:
                continue
            with self.subTest(repair=row["id"]):
                original = (ROOT / row["file"]).read_text(encoding="utf-8")
                broken = original.replace(row["required"], row["removed"], 1)
                self.assertNotEqual(original, broken)
                self.assertTrue(any(row["id"] in e for e in check_repairs(ROOT, self.report, {row["file"]: broken})))
                tested.add(row["id"])
        self.assertEqual(tested, SYNTHESIS_REPAIR_IDS)

    def test_page_control_matcher_with_synthetic_fixture(self):
        # A unit fixture made only of retained short snippets is NOT a source
        # acquisition or reading. Actual PDF replay remains an optional CLI step.
        pages = [""] * self.source["pageCount"]
        for row in self.source["controls"]:
            pages[row["pdfPage"] - 1] += "\n" + row["text"]
        self.assertEqual(verify_pdf_page_controls(pages, self.source), [])

    def test_correct_words_on_the_wrong_page_are_not_verified(self):
        pages = [""] * self.source["pageCount"]
        for row in self.source["controls"]:
            pages[row["pdfPage"] - 1] += "\n" + row["text"]
        broken = deepcopy(self.source)
        next(row for row in broken["controls"] if row["id"] == "P31b")["pdfPage"] = 30
        self.assertTrue(any("P31b" in e for e in verify_pdf_page_controls(pages, broken)))

    def test_different_pdf_bytes_are_rejected_before_extraction(self):
        errors = verify_pdf_bytes(b"not the recorded PDF", self.source)
        self.assertTrue(any("SHA-256" in e for e in errors))
        self.assertTrue(any("MD5" in e for e in errors))
        self.assertTrue(any("size" in e for e in errors))

    def test_retained_history_requires_the_supersession_notice_first(self):
        row = next(r for r in self.report["repairs"] if r.get("historicalRetained"))
        original = (ROOT / row["file"]).read_text(encoding="utf-8")
        broken = original.replace(row["required"], "", 1) + "\n" + row["required"]
        errors = check_repairs(ROOT, self.report, {row["file"]: broken})
        self.assertTrue(any(row["id"] in e and "must precede" in e for e in errors))


class Wave3ParserTests(unittest.TestCase):
    def test_eli_uses_ids_not_zero_based_list_slices(self):
        verses = b"10\tIsa.1:1\n12\tIsa.1:2\n"
        words = "10\tἸδοὺ\n11\tλέγει\n12\tθεός\n".encode()
        self.assertEqual(wave3.eli_verses(verses, words),
                         {"Isa.1:1": "Ἰδοὺ λέγει", "Isa.1:2": "θεός"})

    def test_eli_duplicate_or_missing_tokens_fail_closed(self):
        for words in [b"10\tx\n10\ty\n12\tz\n", b"10\tx\n12\tz\n"]:
            with self.subTest(words=words), self.assertRaises(ValueError):
                wave3.eli_verses(b"10\tIsa.1:1\n12\tIsa.1:2\n", words)

    def test_tei_excludes_editorial_text_but_keeps_tail(self):
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader>λύτρον</teiHeader>'
               '<text><body><div subtype="chapter" n="20"><head>λύτρον</head>'
               '<p>ἔδωκεν <note>λύτρον</note>λύτρον αὐτόν</p></div></body></text></TEI>').encode()
        text = wave3.tei_segment(raw, {"chapter": 20})
        self.assertEqual(text, "ἔδωκεν λύτρον αὐτόν")
        self.assertEqual(wave3.tokens(text).count("λυτρον"), 1)

    def test_tei_missing_and_ambiguous_locators_are_errors(self):
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'
               '<div subtype="chapter" n="20">α</div><div subtype="chapter" n="20">β</div>'
               '</body></text></TEI>').encode()
        for chapter in (20, 21):
            with self.subTest(chapter=chapter), self.assertRaises(ValueError):
                wave3.tei_segment(raw, {"chapter": chapter})

    def test_normalization_is_not_a_lemma_family_search(self):
        decomposed = unicodedata.normalize("NFD", "λύτρον")
        self.assertEqual(wave3.tokens(decomposed), ["λυτρον"])
        self.assertNotEqual(wave3.tokens("αἵματος"), wave3.tokens("αἷμα"))

    def test_osis_counts_direct_ketiv_words_not_qere_notes(self):
        raw = ('<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace">'
               '<verse osisID="Amos.7.2"><w lemma="c/5545" morph="HVq">ו/סלח</w>'
               '<note><w lemma="5545">סלח</w></note><w lemma="5545">סלח</w>'
               '</verse></osis>').encode()
        words = wave3.osis_words(raw)
        self.assertEqual(len(words), 1)
        self.assertEqual(len(words["Amos.7.2"]), 2)
        self.assertEqual(words["Amos.7.2"][0]["lemma"], ["5545"])
        self.assertNotIn("/", words["Amos.7.2"][0]["text"])

    def test_morphgnt_seven_and_eight_column_schemas_are_explicit(self):
        old = "040101 P- -------- PREP Ἐν Ἐν ἐν ἐν\n".encode()
        modern = "040101 P- -------- Ἐν Ἐν ἐν ἐν\n".encode()
        self.assertEqual(wave3.morphgnt_words(old)["040101"][0]["text"], "Ἐν")
        self.assertEqual(wave3.morphgnt_words(modern, columns=7)["040101"][0]["lemma"], "ἐν")
        with self.assertRaises(ValueError):
            wave3.morphgnt_words(old, columns=7)
        with self.assertRaises(ValueError):
            wave3.morphgnt_words(modern)

    def test_empty_or_unsupported_nt_schema_rejected(self):
        for raw, columns in [(b"", 8), (b"x", 6)]:
            with self.subTest(columns=columns), self.assertRaises(ValueError):
                wave3.morphgnt_words(raw, columns)

    def test_s23_token_per_line_is_grouped_by_verse(self):
        raw = "48.1.0 προφήτης\n48.1.1 Ἰδοὺ\n48.1.1 λέγει\n48.1.2 θεός\n".encode()
        self.assertEqual(wave3.s23_verses(raw)["48.1.1"], "Ἰδοὺ λέγει")

    def test_s23_noncontiguous_verse_and_bad_format_rejected(self):
        for raw in [b"48.1.1 a\n48.1.2 b\n48.1.1 c\n", b"48.1 a\n", b""]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                wave3.s23_verses(raw)

    def test_source_bytes_and_absence_are_checked_before_parsing(self):
        raw = b"verified original"
        pin = dict(localRelativePath="source.txt", bytes=len(raw), blob=wave3.blob_hash(raw),
                   sha256=hashlib.sha256(raw).hexdigest())
        control = {"files": {"sample": pin}}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertTrue(any("missing" in e for e in wave3.verify_external(control, root)))
            (root / "source.txt").write_bytes(b"changed")
            self.assertTrue(any("bytes/hash mismatch" in e for e in wave3.verify_external(control, root)))

    def test_source_path_cannot_escape_external_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = wave3.verify_external({"files": {"bad": {"localRelativePath": "../escape"}}}, Path(tmp))
            self.assertEqual(errors, ["unsafe source path: bad"])


class LabelMetricTests(unittest.TestCase):
    def test_reshooter_importlib_mode_finds_its_helper_without_pythonpath(self):
        code = ("import importlib.util; "
                f"s=importlib.util.spec_from_file_location('proof_reshoot', {str(ROOT / 'scripts/atonement_reshoot_state.py')!r}); "
                "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
                "assert m.source_label_prefix('D') == 'D'")
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, "-I", "-B", "-c", code], cwd=tmp, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_canonical_prefix_recognition_is_not_legacy_vocabulary(self):
        for label in ("A1", "A2", "A3", "B1", "C", "D"):
            self.assertEqual(source_label_prefix(f"`{label}` (context)"), label)
        for label in ("B2", "READABLE", "not A1", "A10", "A1suffix"):
            self.assertIsNone(source_label_prefix(label))

    def test_legacy_label_can_follow_different_column_layouts(self):
        self.assertEqual(legacy_carrier_code("| FP-001 | author | claim | `A1` | page |"), "A1")
        self.assertEqual(legacy_carrier_code("| FP-137 | author | work | claim | `B2` (qualifier) | page |"), "B2")

    def test_a_quoted_grade_inside_a_claim_is_not_the_row_grade(self):
        self.assertEqual(legacy_carrier_code("| FP-001 | author | disputed `A1` attribution | `C` | queue |"), "C")
        self.assertIsNone(legacy_carrier_code("| FP-001 | author | disputed `A1` attribution | queue |"))

    def test_ambiguous_and_unmarked_legacy_cells_fail_closed(self):
        self.assertIsNone(legacy_carrier_code("| FP-001 | `A1` | `B1` | page |"))
        self.assertIsNone(legacy_carrier_code("| FP-001 | A1 | page |"))
        self.assertIsNone(legacy_carrier_code("| FP-001 | `A3` | page |"))

    def test_actual_209_rows_are_legacy_labels_not_reading(self):
        file = ROOT / "docs/research/atonement/35_four_point_authors_mass_registry.md"
        codes = [legacy_carrier_code(line) for line in file.read_text().splitlines() if line.startswith("| FP-")]
        self.assertEqual(len(codes), 209)
        self.assertEqual(Counter(codes), {"A1": 53, "A2": 30, "B1": 34, "B2": 6, "C": 86})
        corpus = json.loads((ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json").read_text())
        block = corpus["fourPointMassRegistry20261023"]
        self.assertEqual(block["perLegacyCode"], dict(Counter(codes)))
        self.assertIs(block["readingMeasured"], False)
        self.assertIs(block["sourceClassesMeasured"], False)
        self.assertFalse({"perClass", "shareA1Percent", "classesVocabulary"} & set(block))

    def test_matrix_counts_labels_without_certifying_reading_and_blocks_c_and_d(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / "ledger.md"
            ledger.write_text("# empty conflict fixture\n")
            (root / "draft.md").write_text(
                "| Опора | Класс | Локатор | HOLD |\n|---|---|---|---|\n"
                + "".join(f"| source | `{label}` | section 1 | x |\n" for label in ["A1", "A2", "C", "D", "B2"]))
            with patch.multiple(reshoot, ROOT=root, LEDGER=ledger, SUBLANES=(),
                                draft_paths=lambda: ["draft.md"], DONOT_SIGNS={}, DONOT_COMPOUND={}):
                matrix = reshoot.exhaust_matrix_scan({})
        self.assertEqual(matrix["итог"]["сРаспознаннойМеткой"], 4)
        self.assertEqual(matrix["итог"]["безРаспознаннойМетки"], 1)
        self.assertIs(matrix["readingMeasured"], False)
        self.assertIs(matrix["exhaustivenessMeasured"], False)
        self.assertEqual(matrix["приёмка"]["статейСКлассомC"], 1)
        self.assertEqual(matrix["приёмка"]["статейСКлассомD"], 1)
        self.assertNotIn("читаемых", matrix["итог"])


class ActualWave3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text())
        cls.control = json.loads((ROOT / wave3.CONTROL).read_text())

    def test_current_offline_controls_and_historical_bytes(self):
        self.assertEqual(wave3.check_controls(ROOT, self.report, self.control), [])

    def test_missing_source_cannot_pass(self):
        broken = deepcopy(self.control)
        del broken["files"]["swete/utils/convert-swete.py"]
        self.assertTrue(any("inventory" in e for e in wave3.check_controls(ROOT, self.report, broken)))

    def test_lost_extract_cannot_pass(self):
        broken = deepcopy(self.control)
        broken["extracts"] = [r for r in broken["extracts"] if r["id"] != "gregory30-20"]
        self.assertTrue(any("extract" in e for e in wave3.check_controls(ROOT, self.report, broken)))

    def test_source_class_is_not_a_language_or_readability_state(self):
        broken = deepcopy(self.control)
        broken["files"]["gregory30"]["evidenceClass"] = "A1-original"
        self.assertTrue(any("source axis" in e for e in wave3.check_controls(ROOT, self.report, broken)))

    def test_reading_and_apparatus_cannot_be_promoted(self):
        for key in ["fullCorpusReadingClaimed", "printedCollationClaimed"]:
            broken = deepcopy(self.report)
            broken["wave3"]["readingScope"][key] = True
            self.assertTrue(any("reading scope promoted" in e for e in wave3.check_controls(ROOT, broken, self.control)))

    def test_derivative_source_cannot_be_called_independent(self):
        broken = deepcopy(self.control)
        broken["sourceRelationships"][0]["relation"] = "INDEPENDENT"
        self.assertTrue(any("independence" in e for e in wave3.check_controls(ROOT, self.report, broken)))

    def test_rendered_web_excerpt_is_not_a_hashed_raw_archive(self):
        broken = deepcopy(self.control)
        broken["webExcerpts"][0]["rawObjectSha256"] = "a" * 64
        self.assertTrue(any("unobserved archive" in e for e in wave3.check_controls(ROOT, self.report, broken)))

    def test_missing_or_wrong_baseline_snapshot_cannot_pass(self):
        for field in ("missing", "sha256"):
            broken = deepcopy(self.report)
            if field == "missing":
                broken["wave3"]["supersededSnapshots"].pop()
            else:
                broken["wave3"]["supersededSnapshots"][0]["sha256"] = "0" * 64
            self.assertTrue(wave3.check_controls(ROOT, broken, self.control))

    def test_every_wave3_text_or_data_repair_is_guarded(self):
        tested = set()
        for row in self.report["repairs"]:
            if not row["id"].startswith("W3-"):
                continue
            with self.subTest(repair=row["id"]):
                original = (ROOT / row["file"]).read_text()
                broken = original.replace(row["required"], row["removed"], 1)
                self.assertNotEqual(original, broken)
                self.assertTrue(any(row["id"] in e for e in check_repairs(ROOT, self.report, {row["file"]: broken})))
                tested.add(row["id"])
        self.assertTrue(wave3.REQUIRED_REPAIRS <= tested)


class ActualWave4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text())
        cls.control = json.loads((ROOT / wave4.CONTROL).read_text())

    def errors(self, control=None, report=None):
        return wave4.check_controls(ROOT, self.report if report is None else report,
                                    self.control if control is None else control)

    @staticmethod
    def web(control, ident):
        return next(x for x in control["webObservations"] if x["id"] == ident)

    def replace_web_phrase(self, row, old, new):
        before = wave4.web_text(row)
        self.assertIn(old, before)
        for selection in row["selections"]:
            selection["text"] = selection["text"].replace(old, new)
        after = wave4.web_text(row)
        self.assertNotEqual(before, after)
        row["textSha256"] = wave4.text_hash(after)

    def test_current_bounded_controls_and_actual_baseline_bytes(self):
        self.assertEqual(self.errors(), [])

    def test_missing_file_pin_cannot_become_empty_success(self):
        broken = deepcopy(self.control)
        broken["files"].pop()
        self.assertTrue(any("file pins" in x for x in self.errors(broken)))

    def test_lost_excerpt_and_changed_text_hash_refused(self):
        broken = deepcopy(self.control)
        broken["extracts"].pop()
        self.assertTrue(any("file extract" in x for x in self.errors(broken)))
        broken = deepcopy(self.control)
        broken["extracts"][0]["text"] += " changed"
        self.assertTrue(any("extract identity/hash" in x for x in self.errors(broken)))

    def test_missing_web_observation_refused(self):
        broken = deepcopy(self.control)
        broken["webObservations"].pop()
        self.assertTrue(any("rendered web observation" in x for x in self.errors(broken)))

    def test_rendered_capture_is_not_a_raw_http_hash(self):
        for key, value in (("rawHtmlReceived", True), ("rawObjectSha256", "a" * 64),
                           ("hashScope", "RAW_HTTP_BYTES"), ("fetchTimestampUtc", "2026-11-03T00:00:00Z")):
            with self.subTest(field=key):
                broken = deepcopy(self.control)
                broken["webObservations"][0][key] = value
                self.assertTrue(any("promoted to HTTP bytes" in x for x in self.errors(broken)))

    def test_cyril_all_mankind_and_creation_cannot_be_replaced_by_election(self):
        broken = deepcopy(self.control)
        row = self.web(broken, "CYRIL-7-WEB")
        self.replace_web_phrase(row, "for all mankind", "for the elect")
        self.replace_web_phrase(row, "by way of creation", "by election")
        self.assertTrue(any("critical web text missing" in x for x in self.errors(broken)))

    def test_cyril_faith_boundary_cannot_be_dropped_even_with_a_new_hash(self):
        broken = deepcopy(self.control)
        row = self.web(broken, "CYRIL-7-WEB")
        self.replace_web_phrase(row, "through faith into one fold, the Church", "automatically into final salvation")
        self.assertTrue(any("critical web text missing" in x for x in self.errors(broken)))

    def test_cyril_fragment_not_promoted_to_authentic_complete_greek(self):
        for key, value in (("attribution", "INDEPENDENTLY_AUTHENTICATED"), ("textCompleteness", "FULL_BOOK"),
                           ("originalGreekRead", True), ("universalFinalSalvationProved", True),
                           ("targetPageMarkers", "133-135")):
            with self.subTest(field=key):
                broken = deepcopy(self.control)
                next(s for s in broken["sources"] if s["id"] == "CYRIL-FRAGMENT")[key] = value
                self.assertTrue(any("Cyril fragment" in x for x in self.errors(broken)))

    def test_alford_displayed_greek_not_silently_replaced_from_acts(self):
        broken = deepcopy(self.control)
        row = self.web(broken, "ALFORD-11-WEB")
        self.replace_web_phrase(row, "τασσόμενοι", "τεταγμένοι")
        self.assertTrue(any("critical web text missing" in x for x in self.errors(broken)))

    def test_calvin_suspect_sentence_is_not_silently_emended(self):
        broken = deepcopy(self.control)
        row = self.web(broken, "CALVIN-1-WEB")
        self.replace_web_phrase(row, "is occupied by the Jews", "is occupied by the Gentiles")
        self.assertTrue(any("critical web text missing" in x for x in self.errors(broken)))

    def test_shared_calvin_defect_not_assigned_to_ai_without_evidence(self):
        broken = deepcopy(self.control)
        broken["calvinDigitalDefect"]["originAssignedToAIConversion"] = True
        self.assertTrue(any("AI-conversion error" in x for x in self.errors(broken)))

    def test_translated_latin_not_a_greek_original(self):
        broken = deepcopy(self.control)
        next(s for s in broken["sources"] if s["id"] == "CHRYSOSTOM")["originalGreekRead"] = True
        self.assertTrue(any("Latin translation" in x for x in self.errors(broken)))

    def test_calvin_mirrors_not_independent_or_original_language(self):
        for field in ("independentMirrorsClaimed", "originalLanguageRead"):
            broken = deepcopy(self.control)
            next(s for s in broken["sources"] if s["id"] == "CALVIN")[field] = True
            self.assertTrue(any("Calvin original-language" in x for x in self.errors(broken)))

    def test_scope_rights_and_publication_are_not_one_axis(self):
        for field in ("fullCorpusReadingClaimed", "wholeWorksRead", "printedCollationClaimed",
                      "allAuthorConsensusClaimed", "publicationEligible"):
            broken = deepcopy(self.control)
            broken[field] = True
            self.assertTrue(any("overclaim" in x for x in self.errors(broken)))
        broken = deepcopy(self.control)
        broken["sources"][0]["evidenceClass"] = "A1-translation"
        self.assertTrue(any("independent axis" in x for x in self.errors(broken)))
        broken = deepcopy(self.control)
        broken["sources"][0]["publicationState"] = "PROMOTE"
        self.assertTrue(any("publication boundary" in x for x in self.errors(broken)))

    def test_metadata_cannot_replace_the_actual_primary_refs(self):
        broken = deepcopy(self.control)
        next(s for s in broken["sources"] if s["id"] == "CALVIN")["evidenceRefs"] = ["CALVIN-README"]
        self.assertTrue(any("missing primary evidence" in x for x in self.errors(broken)))

    def test_new_patristic_card_must_match_its_scoped_source(self):
        broken = deepcopy(self.control)
        next(s for s in broken["sources"] if s["id"] == "AUGUSTINE")["readingScope"] = "entire Augustine corpus"
        self.assertTrue(any("AUG-2 card/source scope mismatch" in x for x in self.errors(broken)))

    def test_malformed_whole_xml_not_called_repaired_or_valid(self):
        broken = deepcopy(self.control)
        broken["pl35WholeDocumentParse"]["status"] = "PASS"
        broken["pl35WholeDocumentParse"]["sourceRepaired"] = True
        self.assertTrue(any("malformed whole XML" in x for x in self.errors(broken)))

    def test_historical_timezone_correction_cannot_be_reversed(self):
        for field in ("moscowJustificationWithdrawn", "historicalUtcInstantsRetained"):
            broken = deepcopy(self.control)
            broken["timeProvenance"][field] = False
            self.assertTrue(any("timezone provenance" in x for x in self.errors(broken)))

    def test_missing_baseline_and_false_removal_history_refused(self):
        broken = deepcopy(self.report)
        broken["wave4"]["supersededSnapshots"][0]["sha256"] = "0" * 64
        self.assertTrue(any("Git preimage byte mismatch" in x for x in self.errors(report=broken)))
        broken = deepcopy(self.report)
        row = next(r for r in broken["repairs"] if r.get("controlType") == "ADDITIVE_GUARD_NOT_A_HISTORICAL_QUOTE")
        row["rejectedWordingPresentInBaseline"] = True
        self.assertTrue(any("invented historical-removal" in x for x in self.errors(report=broken)))

    def test_deleting_both_record_and_declaration_cannot_hollow_the_gate(self):
        broken = deepcopy(self.report)
        broken["repairs"] = [r for r in broken["repairs"] if r["id"] != "W4-NT15"]
        broken["wave4"]["repairIds"].remove("W4-NT15")
        self.assertTrue(any("repair coverage mismatch" in x for x in self.errors(report=broken)))

    def test_all_22_wave4_reversion_controls_execute_in_memory(self):
        tested = set()
        for row in self.report["repairs"]:
            if not row["id"].startswith("W4-"):
                continue
            with self.subTest(repair=row["id"]):
                original = (ROOT / row["file"]).read_text()
                broken = original.replace(row["required"], row["removed"], 1)
                self.assertNotEqual(original, broken)
                self.assertTrue(any(row["id"] in e for e in check_repairs(ROOT, self.report, {row["file"]: broken})))
                tested.add(row["id"])
        self.assertEqual(tested, wave4.REQUIRED_REPAIRS)

    def test_missing_external_files_are_failure_not_skipped_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = wave4.verify_sources(Path(tmp), self.control)
        self.assertTrue(any("unavailable verified source" in e for e in errors))

    def test_actual_byte_identity_is_checked_before_extracting(self):
        raw = b"first\nsecond\n"
        fixture = {"files": [{"id": "fixture", "externalRelativePath": "file.txt", "bytes": len(raw),
                               "gitBlob": wave4.git_blob(raw), "sha256": wave4.sha256(raw)}],
                   "extracts": [{"id": "fixture-lines", "sourceFile": "fixture", "selector": {"kind": "lines", "firstLine": 1, "lastLine": 2},
                                  "text": "first second", "textSha256": wave4.text_hash("first second")}]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "file.txt")
            path.write_bytes(raw)
            self.assertEqual(wave4.verify_sources(Path(tmp), fixture), [])
            path.write_bytes(raw + b"changed")
            self.assertTrue(any("file bytes changed" in e for e in wave4.verify_sources(Path(tmp), fixture)))

    def test_source_path_escape_refused(self):
        broken = deepcopy(self.control)
        broken["files"][0]["externalRelativePath"] = "../outside.xml"
        self.assertTrue(any("unsafe external source path" in e for e in self.errors(broken)))
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(any("unsafe source path" in e for e in wave4.verify_sources(Path(tmp), broken)))

    def test_augustine_fragment_parser_preserves_ocr_and_uses_incipit(self):
        raw = (b'<root>invalid & outside fragment<ab><title type="sub">TRACTATUS XLIX.</title></ab>'
               b'<p>25. Dicit ei Martha: wrong OCR number, do not select me.</p>'
               b'<p>25. Multi ergo ex Judaeis: selected.</p><p>26. Context.</p>'
               b'<p>27. Joan. x, 46. Do not repair me.</p><p>28. End.</p>'
               b'<ab><title type="sub">TRACTATUS L.</title></ab></root>')
        before = raw
        result = wave4.extract(raw, {"kind": "augustine-49-fragment"})
        self.assertNotIn("Martha", result)
        self.assertIn("Joan. x, 46", result)
        self.assertEqual(raw, before)
        duplicate = raw.replace(b'<p>26.', b'<p>25. Multi ergo ex Judaeis: duplicate.</p><p>26.')
        with self.assertRaises(ValueError):
            wave4.extract(duplicate, {"kind": "augustine-49-fragment"})

    def test_source_helpers_are_in_the_native_byte_inventory(self):
        required = {"scripts/atonement_wave3_sources.py", "scripts/atonement_wave4_sources.py", "scripts/atonement_source_metrics.py"}
        self.assertTrue(required <= set(reshoot.PIPELINE_FILES))
        inventory = reshoot.pipeline_inventory()
        self.assertTrue(required <= set(inventory["файлы"]))
        self.assertTrue(all(isinstance(inventory["файлы"][p], dict) for p in required))

    def test_new_card_ids_are_visible_to_the_native_claim_register(self):
        from atonement_claim_register import CODE_RE, machine_ids
        wanted = {"CHR-2", "AUG-2", "CYRA-2"}
        self.assertTrue(wanted <= machine_ids("fathers"))
        data = json.loads((ROOT / "ИСКУПЛЕНИЕ/fathers/data/fathers-corpus-v1.json").read_text())
        for card in data["cards"]:
            if card["cardId"] not in wanted:
                continue
            text = (ROOT / "ИСКУПЛЕНИЕ/fathers" / card["file"]).read_text()
            titles = [line[3:] for line in text.splitlines() if line.startswith("## " + card["cardId"] + ".")]
            self.assertEqual(len(titles), 1)
            self.assertEqual(CODE_RE.match(titles[0]).group(1), card["cardId"])

    def test_calvin_extractor_distinguishes_verse_from_italic_comment(self):
        raw = b'**16.** Verse text.\n\n**16.** *Lemma.* Comment.\n\n**17.** *Next.* Other.\n'
        result = wave4.extract(raw, {"kind": "calvin-comments", "firstVerse": 16, "lastVerse": 16})
        self.assertEqual(result, "16. Lemma. Comment.")
        with self.assertRaises(ValueError):
            wave4.extract(raw + b'\n**16.** *Duplicate.*\n', {"kind": "calvin-comments", "firstVerse": 16, "lastVerse": 16})


class ActualWave5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text())
        cls.control = json.loads((ROOT / wave5.CONTROL).read_text())

    def errors(self, control=None, report=None):
        return wave5.check_controls(ROOT, self.report if report is None else report,
                                    self.control if control is None else control)

    web = staticmethod(ActualWave4Tests.web)
    replace_web_phrase = ActualWave4Tests.replace_web_phrase

    def test_current_controls_and_actual_git_preimages(self):
        self.assertEqual(self.errors(), [])

    def test_all_nonclosure_boundaries_are_effective(self):
        for key in wave5.FALSE_BOUNDARIES:
            with self.subTest(field=key):
                c = deepcopy(self.control)
                c[key] = True
                self.assertTrue(any(key in e for e in self.errors(c)))

    def test_objection_and_author_reply_cannot_exchange_voices(self):
        c = deepcopy(self.control)
        row = self.web(c, 'CYRIL-JN10')
        s = next(s for s in row['selections'] if s['id'] == 'WHO-OUTSIDE-OBJECTION')
        s['voice'] = 'AUTHOR_REPLY'
        self.assertTrue(any('objection' in e for e in self.errors(c)))

    def test_cyril_creation_faith_and_differentiated_reply_survive_rehash(self):
        for ident, phrase in [('CYRIL-JN1', 'baptized into nought originate'),
                              ('CYRIL-JN8', 'it will not harmonize so to understand it here'),
                              ('CYRIL-JN10', 'yet is not the same thing to all'),
                              ('CYRIL-JN11-52', 'for all mankind'),
                              ('CYRIL-JN11-52', 'by way of creation'),
                              ('CYRIL-JN11-52', 'through faith into one fold, the Church')]:
            with self.subTest(phrase=phrase):
                c = deepcopy(self.control)
                self.replace_web_phrase(self.web(c, ident), phrase, 'removed by regression fixture')
                self.assertTrue(any('critical selection' in e for e in self.errors(c)))

    def test_broad_resurrection_language_cannot_be_hidden(self):
        c = deepcopy(self.control)
        self.replace_web_phrase(self.web(c, 'CYRIL-JN11-44'), 'every one will be set free', 'some are set free')
        self.assertTrue(any('critical selection' in e for e in self.errors(c)))

    def test_punishment_language_cannot_be_hidden_either(self):
        c = deepcopy(self.control)
        self.replace_web_phrase(self.web(c, 'CYRIL-JN10'), 'they will go down into Hades', 'they will receive identical bliss')
        self.assertTrue(any('critical selection' in e for e in self.errors(c)))

    def test_partial_context_not_promoted_to_raw_http(self):
        c = deepcopy(self.control)
        c['webObservations'][0]['rawObjectSha256'] = 'a' * 64
        self.assertTrue(any('raw HTTP' in e for e in self.errors(c)))

    def test_missing_web_and_file_controls_cannot_pass(self):
        for key, message in [('files', 'file pins'), ('webObservations', 'rendered observation'),
                             ('greekContexts', 'Greek context')]:
            with self.subTest(key=key):
                c = deepcopy(self.control)
                c[key].pop()
                self.assertTrue(any(message in e for e in self.errors(c)))

    def test_greek_missing_verse_caught_even_after_rehash(self):
        c = deepcopy(self.control)
        x = c['greekContexts'][0]
        x['verses'].pop()
        x['textSha256'] = wave5.text_hash(wave5.context_text(x['verses']))
        self.assertTrue(any('verse coverage' in e for e in self.errors(c)))

    def test_present_participle_not_changed_into_future_proof(self):
        c = deepcopy(self.control)
        x = next(x for x in c['greekContexts'] if x['id'] == 'JN17')
        v = next(v for v in x['verses'] if v['ref'] == '041720')
        self.assertIn('πιστευόντων', v['text'])
        v['text'] = v['text'].replace('πιστευόντων', 'πιστευσόντων')
        x['textSha256'] = wave5.text_hash(wave5.context_text(x['verses']))
        self.assertTrue(any('critical Greek control' in e for e in self.errors(c)))

    def test_broad_john12_not_erased_to_protect_preference(self):
        c = deepcopy(self.control)
        x = next(x for x in c['greekContexts'] if x['id'] == 'JN12')
        v = next(v for v in x['verses'] if v['ref'] == '041232')
        self.assertIn('πάντας', v['text'])
        v['text'] = v['text'].replace('πάντας', 'τινάς')
        x['textSha256'] = wave5.text_hash(wave5.context_text(x['verses']))
        self.assertTrue(any('critical Greek control' in e for e in self.errors(c)))

    def test_lemma_query_does_not_include_diminutives_abraham_or_devil(self):
        def vs(*lemmas):
            return [{'lemma': l} for l in lemmas]
        words = {'040101': vs('τέκνον', 'θεός'), '040102': vs('τέκνον', 'ὁ', 'θεός'),
                 '040103': vs('τεκνίον', 'θεός'), '040104': vs('τέκνον', 'ὁ', 'διάβολος'),
                 '040105': vs('τέκνον', 'Ἀβραάμ'), '040106': vs('τέκνον', 'ὁ', 'ὁ', 'θεός'),
                 '040107': vs('τέκνον'), '040108': vs('θεός')}
        got = wave5.lexical_query(words)
        self.assertEqual(got['childrenOfGodOccurrences'], ['040101', '040102'])
        self.assertEqual(len(got['teknonOccurrences']), 6)
        self.assertEqual(got['parsedVerses'], 8)

    def test_counts_and_source_search_are_not_reading(self):
        for key, value in [('queryIsReading', True), ('lexicalResults', {})]:
            c = deepcopy(self.control)
            c[key] = value
            self.assertTrue(any('lexical scope' in e for e in self.errors(c)))

    def test_prophets_metadata_is_not_greek_john_or_global_absence(self):
        for key, value in [('metadataWork', 'In Ioannem'), ('globalAbsenceClaimed', True),
                           ('johnGreekAcquired', True), ('scope', 'ALL_GREEK_EDITIONS')]:
            c = deepcopy(self.control)
            c['greekCyrilDiscovery'][key] = value
            self.assertTrue(any('Prophets metadata' in e for e in self.errors(c)))

    def test_source_class_and_publication_are_independent(self):
        for key, value in [('evidenceClass', 'C'), ('publicationState', 'PROMOTE'),
                           ('holds', []), ('readingScope', '')]:
            c = deepcopy(self.control)
            c['sources'][0][key] = value
            self.assertTrue(any('scope/version/quote/publication' in e for e in self.errors(c)))

    def test_original_language_and_fragment_boundaries(self):
        for key, value in [('originalGreekRead', True), ('textCompleteness', 'EXTANT_FRAGMENT')]:
            c = deepcopy(self.control)
            c['sources'][0][key] = value
            self.assertTrue(any('English Cyril' in e or 'Book VII fragment status' in e for e in self.errors(c)))
        c = deepcopy(self.control)
        c['sources'][1]['attribution'] = 'INDEPENDENTLY_AUTHENTICATED'
        self.assertTrue(any('fragment/attribution' in e for e in self.errors(c)))

    def test_readme_does_not_clear_eula(self):
        c = deepcopy(self.control)
        c['sources'][2]['eulaNewlyRead'] = True
        self.assertTrue(any('README license' in e for e in self.errors(c)))

    def test_real_baseline_snapshots_and_additive_guard_semantics(self):
        r = deepcopy(self.report)
        r['wave5']['supersededSnapshots'][0]['sha256'] = '0' * 64
        self.assertTrue(any('preimage byte mismatch' in e for e in self.errors(report=r)))
        r = deepcopy(self.report)
        row = next(x for x in r['repairs'] if x['id'] == 'W5-H11')
        row['rejectedWordingPresentInBaseline'] = True
        self.assertTrue(any('invented historical error' in e for e in self.errors(report=r)))

    def test_all_wave5_reversions_execute_in_memory(self):
        tested = set()
        for row in self.report['repairs']:
            if row['id'] not in wave5.REQUIRED_REPAIRS:
                continue
            text = (ROOT / row['file']).read_text()
            self.assertIn(row['required'], text)
            broken = text.replace(row['required'], row['removed'])
            self.assertNotEqual(text, broken)
            errors = check_repairs(ROOT, self.report, {row['file']: broken})
            self.assertTrue(any(e.startswith(row['id'] + ':') for e in errors), row['id'])
            tested.add(row['id'])
        self.assertEqual(tested, wave5.REQUIRED_REPAIRS)

    def test_missing_sources_fail_replay_not_empty_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(wave5.verify_sources(Path(tmp), self.control))

    def test_actual_fixture_bytes_and_path_escape(self):
        raw = '040112 N- ----APN- N-APN τέκνα τέκνα τέκνα τέκνον\n040112 N- ----GSM- N-GSM θεοῦ θεοῦ θεοῦ θεός\n'.encode()
        words = wave3.morphgnt_words(raw, 8)
        verses = wave5.context(words, 1, 12, 12)
        fixture = {'files': [{'id': 'NT-JOHN', 'externalRelativePath': 'book.txt', 'bytes': len(raw),
                             'sha256': wave5.sha256(raw), 'gitBlob': wave5.git_blob(raw)}],
                   'lexicalResults': {'NT-JOHN': wave5.lexical_query(words)},
                   'greekContexts': [{'id': 'fixture', 'sourceFile': 'NT-JOHN', 'chapter': 1, 'firstVerse': 12,
                                      'lastVerse': 12, 'verses': verses, 'textSha256': wave5.text_hash(wave5.context_text(verses))}]}
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'book.txt'
            p.write_bytes(raw)
            self.assertEqual(wave5.verify_sources(Path(tmp), fixture), [])
            p.write_bytes(raw + b'\n')
            self.assertTrue(any('file bytes changed' in e for e in wave5.verify_sources(Path(tmp), fixture)))
            fixture['files'][0]['externalRelativePath'] = '../outside.txt'
            self.assertTrue(any('unsafe source path' in e for e in wave5.verify_sources(Path(tmp), fixture)))

    def test_new_helper_and_card_participate_in_native_inventory(self):
        from atonement_claim_register import machine_ids
        self.assertIn('scripts/atonement_wave5_sources.py', reshoot.PIPELINE_FILES)
        self.assertIn('CYRA-3', machine_ids('fathers'))
        p = ROOT / 'ИСКУПЛЕНИЕ/fathers/05_FIFTH_CENTURY_AND_BOUNDARY_CARDS.md'
        self.assertEqual(len([s for s in p.read_text().splitlines() if s.startswith('## CYRA-3.')]), 1)


class ActualWave6Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text())
        cls.control = json.loads((ROOT / wave6.CONTROL).read_text())

    def errors(self, control=None, report=None):
        return wave6.check_controls(ROOT, self.report if report is None else report,
                                    self.control if control is None else control)

    def test_actual_controls_and_git_preimages(self):
        self.assertEqual(self.errors(), [])

    def test_each_nonclosure_boundary_is_enforced(self):
        for key in wave6.FALSE_BOUNDARIES:
            with self.subTest(field=key):
                c = deepcopy(self.control)
                c[key] = True
                self.assertTrue(any(key in e for e in self.errors(c)))

    def test_file_context_and_count_coverage(self):
        for key, message in [('files', 'file inventory'), ('contexts', 'context coverage')]:
            for action in ('remove', 'duplicate'):
                with self.subTest(key=key, action=action):
                    c = deepcopy(self.control)
                    c[key].pop() if action == 'remove' else c[key].append(deepcopy(c[key][0]))
                    self.assertTrue(any(message in e for e in self.errors(c)))
        c = deepcopy(self.control)
        c['statistics']['verseInstances'] = 208
        self.assertTrue(any('coverage statistics' in e for e in self.errors(c)))

    def test_jeremiah_and_zechariah_maps_are_not_identity_or_global_offsets(self):
        p = {r['id']: r for r in self.control['pairings']}
        self.assertEqual(p['JER31']['verseMap'][0], {'mt': 'Jer.31.1', 'lxx': 'Jer.38.1'})
        self.assertEqual(p['ZECH2']['verseMap'][-1], {'mt': 'Zech.2.17', 'lxx': 'Zech.2.13'})
        for ident in ('JER31', 'ZECH2'):
            c = deepcopy(self.control)
            row = next(r for r in c['pairings'] if r['id'] == ident)
            row['verseMap'][0]['lxx'] = row['verseMap'][0]['mt']
            self.assertTrue(any('verse map' in e for e in self.errors(c)))

    def test_missing_verse_caught_after_rehash(self):
        c = deepcopy(self.control)
        row = c['contexts'][0]
        row['verses'].pop()
        row['textSha256'] = wave6.context_digest(row['verses'])
        self.assertTrue(any('context refs/text hash' in e for e in self.errors(c)))

    def test_profile_axes_scope_and_file_bindings_are_distinct(self):
        for key, value in [('evidenceClass', 'C'), ('publicationState', 'PROMOTE'), ('holds', []),
                           ('rightsState', 'PUBLICATION_ELIGIBLE'), ('contextIds', []), ('sourceFileIds', [])]:
            c = deepcopy(self.control)
            c['sources'][0][key] = value
            self.assertTrue(any('primary profile' in e for e in self.errors(c)))

    def test_metadata_file_is_not_an_extra_quote_safe_biblical_witness(self):
        c = deepcopy(self.control)
        row = next(f for f in c['files'] if f['id'] == 'LXX-Isa-META')
        row['evidenceClass'] = 'A1'
        row['quoteSafe'] = True
        self.assertTrue(any('file role' in e for e in self.errors(c)))

    def test_isaiah_grc1_cannot_become_ottley_grc2_or_wrong_print_year(self):
        for key, value in [('editionUrn', 'urn:cts:greekLit:tlg0527.tlg048.1st1K-grc2'),
                           ('printYear', '1904'), ('printedCollationClaimed', True)]:
            c = deepcopy(self.control)
            row = next(e for e in c['editions'] if e['book'] == 'Isa')
            row[key] = value
            self.assertTrue(any('edition identity' in e for e in self.errors(c)))

    def test_key_signals_survive_self_rehash(self):
        for ident in ('CREATED-JACOB', 'FIRSTBORN', 'WINNOWING-NOT-DIASKORPIZO', 'ONE-SHEPHERD-37',
                      'ZECH-GATHER-NOT-SPREAD', 'JOHN-WOLF', 'JOHN-FAITH-CHILDREN'):
            c = deepcopy(self.control)
            ctx, ref, phrase = wave6.SIGNALS[ident]
            row = next(x for x in c['contexts'] if x['id'] == ctx)
            verse = next(v for v in row['verses'] if v['ref'] == ref)
            verse['text'] = verse['text'].replace(phrase, 'synthetic altered reading')
            row['textSha256'] = wave6.context_digest(row['verses'])
            self.assertTrue(any('changed digital signal' in e for e in self.errors(c)), ident)

    def test_proposed_allusion_not_promoted_to_quotation(self):
        c = deepcopy(self.control)
        next(x for x in c['intertextAssessments'] if x['id'] == 'EZ37')['explicitQuotationEstablished'] = True
        self.assertTrue(any('promoted to quotation' in e for e in self.errors(c)))

    def test_digital_irregularity_not_silently_repaired_or_called_print_collation(self):
        c = deepcopy(self.control)
        c['digitalAnomalies'][0]['silentlyEmended'] = True
        self.assertTrue(any('conjectural repair' in e for e in self.errors(c)))
        c = deepcopy(self.control)
        ctx, ref, phrase = wave6.ANOMALIES['EZ34-12']
        row = next(x for x in c['contexts'] if x['id'] == ctx)
        verse = next(v for v in row['verses'] if v['ref'] == ref)
        verse['text'] = verse['text'].replace(phrase, 'διεσπάρησαν')
        row['textSha256'] = wave6.context_digest(row['verses'])
        self.assertTrue(any('changed digital signal/anomaly EZ34-12' in e for e in self.errors(c)))

    def test_three_interpretations_are_retained_without_changing_c25(self):
        c = deepcopy(self.control)
        c['alternatives'] = [a for a in c['alternatives'] if a['id'] != 'ALL_HUMAN_CREATION']
        self.assertTrue(any('alternatives' in e for e in self.errors(c)))
        c = deepcopy(self.control)
        c['c25'] = 'CLOSED'
        self.assertTrue(any('closure drift' in e for e in self.errors(c)))

    def test_john735_question_is_not_narrator_endorsement(self):
        c = deepcopy(self.control)
        c['speakerControl']['speaker'] = 'NARRATOR_ENDORSEMENT'
        self.assertTrue(any('speaker' in e for e in self.errors(c)))

    def test_non_equivalence_not_erased_by_harmonization(self):
        c = deepcopy(self.control)
        c['nonEquivalences'].pop()
        self.assertTrue(any('silently harmonized' in e for e in self.errors(c)))

    def test_hebrew_ketiv_excludes_qere_and_does_not_normalize_nfc(self):
        # Intentionally noncanonical combining-mark order, per OSHB warning.
        word = '\u05e9\u05c1\u05b8'
        self.assertNotEqual(word, unicodedata.normalize('NFC', word))
        raw = (f'<osis xmlns="{wave3.OSIS[1:-1]}"><verse osisID="Zech.2.10">'
               f'<w>{word}</w><note type="variant"><w>qere</w></note><w>ב/ד</w></verse></osis>').encode()
        row = dict(id='fixture', sourceFile='mt', kind='osis-ketiv', book='Zech', chapter=2, firstVerse=10, lastVerse=10)
        got = wave6.extract_context(raw, row)
        self.assertEqual(got, [{'ref': 'Zech.2.10', 'text': word + ' בד'}])
        self.assertIn('qere', wave6.excluded_notes(raw, row)[0]['xml'])
        self.assertNotEqual(wave6.context_digest(got), wave6.context_digest([
            {'ref': 'Zech.2.10', 'text': unicodedata.normalize('NFC', word + ' בד')}]))

    def test_tei_notes_excluded_but_tail_and_digital_artifact_preserved(self):
        raw = (f'<TEI xmlns="{wave3.TEI[1:-1]}"><text><body><div subtype="chapter" n="34">'
               '<div subtype="verse" n="12"><p>α <note>NOT BIBLE</note> διεσ πάρησαν'
               '<pb n="2"/> τέλος</p></div></div></body></text></TEI>').encode()
        row = dict(id='fixture', sourceFile='lxx', kind='tei-body', book='Ezek', chapter=34, firstVerse=12, lastVerse=12)
        self.assertEqual(wave6.extract_context(raw, row), [{'ref': 'Ezek.34.12', 'text': 'α διεσ πάρησαν τέλος'}])
        with self.assertRaises(ValueError):
            wave6.extract_context(raw, dict(row, firstVerse=13, lastVerse=13))

    def test_byte_replay_precedes_extraction_and_detects_changed_file(self):
        raw = '040112 N- ----APN- N-APN τέκνα τέκνα τέκνα τέκνον\n'.encode()
        row = dict(id='fixture', sourceFile='NT-JOHN', kind='morphgnt-8', book='John', chapter=1, firstVerse=12, lastVerse=12)
        verses = wave6.extract_context(raw, row)
        row.update(verses=verses, textSha256=wave6.context_digest(verses))
        fixture = {'files': [{'id': 'NT-JOHN', 'externalRelativePath': 'book.txt', 'bytes': len(raw),
                             'sha256': wave6.digest(raw), 'gitBlob': wave6.git_blob(raw)}], 'contexts': [row]}
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp, 'book.txt')
            p.write_bytes(raw)
            self.assertEqual(wave6.verify_sources(Path(tmp), fixture), [])
            p.write_bytes(raw + b'\n')
            with patch.object(wave6, 'extract_context', side_effect=AssertionError('Must not parse unverified bytes')):
                self.assertTrue(any('file bytes changed' in e for e in wave6.verify_sources(Path(tmp), fixture)))

    def test_replay_refuses_source_path_escape(self):
        c = {'files': [deepcopy(self.control['files'][0])]}
        c['files'][0]['externalRelativePath'] = '../outside.xml'
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(any('unsafe source path' in e for e in wave6.verify_sources(Path(tmp), c)))

    def test_unavailable_source_package_is_not_empty_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            errs = wave6.verify_sources(Path(tmp), self.control)
            self.assertEqual(sum('missing object' in e for e in errs), 21)
            self.assertTrue(any('unavailable/invalid context' in e for e in errs))

    def test_preimages_and_synthetic_guard_are_checked_against_actual_git(self):
        r = deepcopy(self.report)
        r['wave6']['supersededSnapshots'][0]['sha256'] = '0' * 64
        self.assertTrue(any('actual preimage bytes differ' in e for e in self.errors(report=r)))
        r = deepcopy(self.report)
        next(x for x in r['repairs'] if x['id'] == 'W6-H11')['rejectedWordingPresentInBaseline'] = True
        self.assertTrue(any('invented historical error' in e for e in self.errors(report=r)))

    def test_all_wave6_owner_reversions_in_memory(self):
        tested = set()
        for row in self.report['repairs']:
            if row['id'] not in wave6.REQUIRED_REPAIRS:
                continue
            text = (ROOT / row['file']).read_text()
            self.assertIn(row['required'], text)
            broken = text.replace(row['required'], row['removed'])
            errors = check_repairs(ROOT, self.report, {row['file']: broken})
            self.assertTrue(any(e.startswith(row['id'] + ':') for e in errors), row['id'])
            tested.add(row['id'])
        self.assertEqual(tested, wave6.REQUIRED_REPAIRS)

    def test_native_inventory_and_bounded_existing_card_integration(self):
        self.assertIn('scripts/atonement_wave6_sources.py', reshoot.PIPELINE_FILES)
        self.assertIn('check_wave6(root, report, wave6_control)', (ROOT / 'scripts/atonement_sync_check.py').read_text())
        self.assertIn('"atonement_wave6_sources.py"', (ROOT / '.github/workflows/atonement-corpus-integrity.yml').read_text())
        ot = json.loads((ROOT / 'ИСКУПЛЕНИЕ/ot/data/ot-corpus-v1.json').read_text())
        card = next(c for c in ot['cards'] if c['id'] == 14)['gatheringReviewWave6']
        self.assertTrue(card['historicalCardFieldsNotRecertified'])
        self.assertEqual(card['sourceControl'], wave6.CONTROL)
        self.assertEqual(card['publicationState'], 'BLOCKED')


class ActualWave7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text())
        cls.control = json.loads((ROOT / wave7.CONTROL).read_text())

    def errors(self, control=None, report=None):
        return wave7.check_controls(ROOT, self.report if report is None else report,
                                    self.control if control is None else control)

    def test_actual_candidate_controls_and_git_preimages(self):
        self.assertEqual(self.errors(), [])

    def test_each_nonclosure_boundary_is_enforced(self):
        for key in wave7.FALSE_BOUNDARIES:
            with self.subTest(field=key):
                c = deepcopy(self.control); c[key] = True
                self.assertTrue(any(key in e for e in self.errors(c)))

    def test_candidates_cannot_be_promoted_to_primary_greek(self):
        for key,value in [('evidenceClass','A1'), ('quoteSafe',True), ('originalLanguageVerified',True),
                          ('authorialContextVerified',True), ('printedCollationClaimed',True), ('fullWorkRead',True)]:
            with self.subTest(field=key):
                c = deepcopy(self.control); c['candidates'][0][key] = value
                self.assertTrue(any('VERIFIED_ORIGINAL' in e for e in self.errors(c)))

    def test_candidate_axes_and_rights_are_not_class(self):
        for key,value in [('accessState','NOT_ACQUIRED'), ('locatorState','COARSE_LOCATOR_ONLY'),
                          ('rightsState','PUBLICATION_ELIGIBLE'), ('holds',['PUBLICATION_HOLD'])]:
            c = deepcopy(self.control); c['candidates'][1][key] = value
            self.assertTrue(any('digital-only axes' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['files'][0]['evidenceClass'] = 'A1'
        self.assertTrue(any('artifact class/access' in e for e in self.errors(c)))

    def test_artifact_inventory_and_frozen_byte_pin(self):
        c = deepcopy(self.control); c['files'].pop()
        self.assertTrue(any('artifact inventory' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['files'].append(deepcopy(c['files'][0]))
        self.assertTrue(any('artifact inventory' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['files'][0]['sha256'] = '0'*64
        self.assertTrue(any('byte pin' in e for e in self.errors(c)))

    def test_zip_members_are_not_claimed_as_git_blobs(self):
        c = deepcopy(self.control)
        member = next(f for f in c['files'] if f['kind']=='zip_member')
        member['gitBlob'] = '0'*40
        self.assertTrue(any('separate Git blob' in e for e in self.errors(c)))
        c = deepcopy(self.control)
        next(f for f in c['files'] if f['kind']=='zip_member')['containerId'] = 'OG-JOHN'
        self.assertTrue(any('separate Git blob' in e for e in self.errors(c)))

    def test_literal_candidate_and_selector_are_bound_after_rehash(self):
        c = deepcopy(self.control); row = c['candidates'][1]
        row['text'] = row['text'].replace('τροπωι δημιουργικωι', 'τρόπῳ δημιουργικῷ')
        row['textSha256'] = wave7.digest(row['text'].encode())
        self.assertTrue(any('literal candidate' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['candidates'][1]['selector']['first'] += 1
        self.assertTrue(any('selector pin' in e for e in self.errors(c)))

    def test_ocr_row_edition_is_not_the_corpus_default(self):
        c = deepcopy(self.control)
        c['candidates'][0]['rows'][2]['edition'] = 'calfa-pg73-5895ab908dd4'
        self.assertTrue(any('not default Calfa/Pusey' in e for e in self.errors(c)))

    def test_digital_difference_is_not_an_ancient_variant_or_proven_ocr_error(self):
        for key in ('authorialVariantEstablished','ocrCauseEstablished','silentlyEmended'):
            c = deepcopy(self.control); c['digitalComparisons'][0][key] = True
            self.assertTrue(any('cause/emendation' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['digitalComparisons'][1]['left'] = 'τροπωι δημιουργικωι'
        self.assertTrue(any('comparison' in e for e in self.errors(c)))

    def test_rendered_excerpts_are_not_html_bytes(self):
        for key,value in [('rawHtmlAcquired',True), ('rawHtmlSha256','0'*64),
                          ('accessState','FULL_OBJECT_VERIFIED')]:
            c = deepcopy(self.control); c['webObservations'][0][key] = value
            self.assertTrue(any('not raw HTML' in e for e in self.errors(c)))

    def test_pearse_is_not_direct_pusey_or_a_primary_greek_witness(self):
        for key,value in [('evidenceClass','A1'), ('quoteSafe',True)]:
            c = deepcopy(self.control)
            next(w for w in c['webObservations'] if w['id']=='PEARSE-EDITORIAL')[key] = value
            self.assertTrue(any('excerpt/class' in e or 'editor/translation' in e for e in self.errors(c)))
        c = deepcopy(self.control); row = c['webObservations'][0]
        row['passages'][0] = row['passages'][0].replace('and partly Syriac', 'only')
        row['selectedExcerptSha256'] = wave7.digest('\n'.join(row['passages']).encode())
        self.assertTrue(any('web excerpt/class pin' in e for e in self.errors(c)))

    def test_catalogue_is_not_received_edition_or_borrowed_verification(self):
        c = deepcopy(self.control); c['catalogue']['puseyReference']['servable'] = True
        self.assertTrue(any('not acquired Pusey' in e for e in self.errors(c)))
        for key in ('upstreamPdfChecksumsVerifiedHere','upstreamCalfaChecksumVerifiedHere','catalogueIsAcquiredPuseyText'):
            c = deepcopy(self.control); c['catalogue'][key] = True
            self.assertTrue(any('borrowed upstream' in e for e in self.errors(c)))

    def test_composition_and_statistics_are_not_verified_greek_counts(self):
        c = deepcopy(self.control); c['corpusComposition']['rows'] = 3109
        self.assertTrue(any('mixed OCR composition' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['statistics']['verifiedGreekOriginalPassages'] = 2
        self.assertTrue(any('scope statistics' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['interpretationStatus'] = 'PROVED_BY_OCR'
        self.assertTrue(any('not a machine proof' in e for e in self.errors(c)))

    def test_english_basis_and_owned_acquisition_queue_remain(self):
        c = deepcopy(self.control); c['substantiveBasis']['observationId'] = 'OG-JN11'
        self.assertTrue(any('English primary basis' in e for e in self.errors(c)))
        c = deepcopy(self.control); c['nextAcquisition'].pop()
        self.assertTrue(any('acquisition/acceptance' in e for e in self.errors(c)))

    def test_actual_preimage_bytes_not_just_hex_markers(self):
        r = deepcopy(self.report); r['wave7']['supersededSnapshots'][0]['sha256'] = '0'*64
        self.assertTrue(any('actual Git preimage mismatch' in e for e in self.errors(report=r)))
        r = deepcopy(self.report); row = next(x for x in r['repairs'] if x['id']=='W7-F10')
        row['rejectedWordingPresentInBaseline'] = not row['rejectedWordingPresentInBaseline']
        self.assertTrue(any('invented historical error' in e for e in self.errors(report=r)))

    def test_missing_sources_fail_before_context_parsing(self):
        with tempfile.TemporaryDirectory() as d, patch.object(wave7,'extract_candidate') as extract:
            errors = wave7.verify_sources(Path(d), self.control)
            self.assertEqual(len(errors), 13)
            self.assertTrue(all('missing object' in e for e in errors))
            extract.assert_not_called()

    def test_external_path_escape_rejected_before_reading(self):
        c = deepcopy(self.control); c['files'][0]['externalRelativePath'] = '../outside-source'
        with tempfile.TemporaryDirectory() as d, patch.object(wave7,'extract_candidate') as extract:
            self.assertTrue(any('unsafe path' in e for e in wave7.verify_sources(Path(d),c)))
            extract.assert_not_called()

    def test_literal_extract_preserves_accents_linebreaks_and_footer(self):
        literal = unicodedata.normalize('NFD','τρόπῳ')+' δημιουργικωι\nἐσκορ\nπισεν\nfooter'
        result = wave7.extract_candidate(literal.encode(), {'kind':'text_lines','first':1,'last':4})
        self.assertEqual(result['text'],literal)
        with self.assertRaises(ValueError):
            wave7.extract_candidate(literal.encode(),{'kind':'text_lines','first':0,'last':4})

    def test_jsonl_duplicate_or_missing_locus_rejected(self):
        one = dict(locus='x',text='unchanged',source='ocr',edition='test')
        raw = (json.dumps(one)+'\n'+json.dumps(one)+'\n').encode()
        with self.assertRaises(ValueError):
            wave7.extract_candidate(raw,{'kind':'jsonl_loci','loci':['x']})
        with self.assertRaises(ValueError):
            wave7.extract_candidate(raw,{'kind':'jsonl_loci','loci':['y']})
        got = wave7.extract_candidate((json.dumps(one)+'\n').encode(),{'kind':'jsonl_loci','loci':['x']})
        self.assertEqual(got['text'],'unchanged')
        self.assertEqual(got['rows'][0]['line'],1)

    def test_all_four_reviews_and_native_entrypoints_are_wired(self):
        for p in wave7.REGISTRIES:
            review = json.loads((ROOT/'ИСКУПЛЕНИЕ'/p).read_text())[wave7.REVIEW_KEY]
            self.assertEqual(review['candidateEvidenceClass'],'C')
            self.assertFalse(review['greekOriginalVerified'])
            self.assertFalse(review['publicationEligible'])
        self.assertIn('scripts/atonement_wave7_sources.py',reshoot.PIPELINE_FILES)
        self.assertIn('check_wave7(root, report, wave7_control)',(ROOT/'scripts/atonement_sync_check.py').read_text())
        self.assertIn('"atonement_wave7_sources.py"',(ROOT/'.github/workflows/atonement-corpus-integrity.yml').read_text())


class Wave8SourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text(encoding='utf-8'))
        cls.control = json.loads((ROOT / wave8.CONTROL).read_text(encoding='utf-8'))

    def errors(self, control=None, report=None):
        return wave8.check_controls(ROOT, self.report if report is None else report,
                                    self.control if control is None else control)

    def test_wave8_controls_pass_cleanly(self):
        self.assertEqual(self.errors(), [])

    def test_a1_vol1_scans_cannot_be_faked_on_ocr_or_without_visual_flag(self):
        c = deepcopy(self.control)
        scan = next(f for f in c['files'] if f['id'] == 'PUSEY-V1-PRAEF-IX-JPG')
        scan['visualScanInspected'] = False
        self.assertTrue(any('A1 Vol. I scan contract' in e for e in self.errors(c)))
        c2 = deepcopy(self.control)
        ocr = next(f for f in c2['files'] if f['id'] == 'PUSEY-V2-P295-TXT')
        ocr['evidenceClass'] = 'A1'
        self.assertTrue(any('class C OCR/metadata contract' in e for e in self.errors(c2)))
        c3 = deepcopy(self.control)
        ocr3 = next(f for f in c3['files'] if f['id'] == 'FABIO-PG74-039')
        ocr3['quoteSafe'] = True
        self.assertTrue(any('class C OCR/metadata contract' in e for e in self.errors(c3)))

    def test_1152_greek_original_and_c25_closure_are_rejected(self):
        c = deepcopy(self.control)
        c['greekOriginalVerified'] = True
        self.assertTrue(any('overclaimed boundary greekOriginalVerified' in e for e in self.errors(c)))
        c2 = deepcopy(self.control)
        c2['c25'] = 'RESOLVED'
        self.assertTrue(any('cannot become C25/original closure' in e for e in self.errors(c2)))
        c3 = deepcopy(self.control)
        c3['philologicalResolution']['epistemicStatusAfterWave8']['verifiedGreekOriginalsFor1152'] = 1
        self.assertTrue(any('epistemic closure overclaim' in e for e in self.errors(c3)))

    def test_syriac_medium_and_discrepancy_inventory_are_guarded(self):
        c = deepcopy(self.control)
        c['philologicalResolution']['languageMediumVerdict']['syriacInvolvementOnJohn1149_52'] = True
        self.assertTrue(any('language medium verdict drift' in e for e in self.errors(c)))
        c2 = deepcopy(self.control)
        c2['philologicalResolution']['discrepancyClassification'].pop()
        self.assertTrue(any('discrepancy classification inventory' in e for e in self.errors(c2)))

    def test_web_observations_must_remain_partial_non_raw_html(self):
        c = deepcopy(self.control)
        c['webObservations'][0]['rawHtmlAcquired'] = True
        self.assertTrue(any('web observation partial-object contract' in e for e in self.errors(c)))
        c2 = deepcopy(self.control)
        c2['webObservations'][0]['accessState'] = 'FULL_OBJECT_VERIFIED'
        self.assertTrue(any('web observation partial-object contract' in e for e in self.errors(c2)))

    def test_actual_git_preimage_bytes_and_repair_honesty_enforced(self):
        r = deepcopy(self.report)
        r['wave8']['supersededSnapshots'][0]['sha256'] = '0' * 64
        self.assertTrue(any('actual Git preimage mismatch' in e for e in self.errors(report=r)))
        r2 = deepcopy(self.report)
        row = next(x for x in r2['repairs'] if x['id'] == 'W8-F10')
        row['rejectedWordingPresentInBaseline'] = not row['rejectedWordingPresentInBaseline']
        self.assertTrue(any('invented historical error' in e for e in self.errors(report=r2)))

    def test_missing_or_escaped_external_sources_fail_before_parsing(self):
        with tempfile.TemporaryDirectory() as d:
            errors = wave8.verify_sources(Path(d), self.control)
            self.assertEqual(len(errors), 32)
            self.assertTrue(all('missing/symlink file' in e for e in errors))
        c = deepcopy(self.control)
        c['files'][0]['externalRelativePath'] = '../escape'
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(any('path traversal' in e for e in wave8.verify_sources(Path(d), c)))

    def test_jpeg_marker_gate_rejects_corrupted_scan_even_with_matching_pin(self):
        bad_bytes = b'NOT_A_JPEG_SCAN'
        c = deepcopy(self.control)
        for f in c['files']:
            f['bytes'] = len(bad_bytes)
            f['sha256'] = wave8.digest(bad_bytes)
            f['gitBlob'] = wave8.git_blob(bad_bytes)
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            for f in c['files']:
                p = base / f['externalRelativePath']
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(bad_bytes)
            errors = wave8.verify_sources(base, c)
            self.assertEqual(len(errors), 8)
            self.assertTrue(all('invalid JPEG markers' in e for e in errors))

    def test_all_four_wave8_reviews_and_pipeline_entrypoints_are_wired(self):
        for p in wave8.REGISTRIES:
            review = json.loads((ROOT / 'ИСКУПЛЕНИЕ' / p).read_text(encoding='utf-8'))[wave8.REVIEW_KEY]
            self.assertEqual(review['puseyVol1PraefatioEvidenceClass'], 'A1')
            self.assertEqual(review['puseyVol2AndPg74OcrEvidenceClass'], 'C')
            self.assertFalse(review['syriacInvolvementOnJohn1149_52'])
            self.assertFalse(review['greekOriginalVerified'])
            self.assertFalse(review['publicationEligible'])
        self.assertIn('scripts/atonement_wave8_sources.py', reshoot.PIPELINE_FILES)
        self.assertIn('check_wave8(root, report, wave8_control)', (ROOT / 'scripts/atonement_sync_check.py').read_text(encoding='utf-8'))
        self.assertIn('"atonement_wave8_sources.py"', (ROOT / '.github/workflows/atonement-corpus-integrity.yml').read_text(encoding='utf-8'))


class Wave9SourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / REPORT).read_text(encoding='utf-8'))
        cls.control = json.loads((ROOT / wave9.CONTROL).read_text(encoding='utf-8'))

    def errors(self, control=None, report=None):
        return wave9.check_controls(ROOT, self.report if report is None else report,
                                    self.control if control is None else control)

    def test_wave9_controls_pass_cleanly(self):
        self.assertEqual(self.errors(), [])

    def test_scan_tei_and_ocr_tier_contracts_are_enforced(self):
        c = deepcopy(self.control)
        scan = next(f for f in c['files'] if f['id'] == 'CRAMER-V2-P322-JPG')
        scan['visualScanInspected'] = False
        self.assertTrue(any('A1 visual scan contract' in e for e in self.errors(c)))
        c2 = deepcopy(self.control)
        tei = next(f for f in c2['files'] if f['id'] == 'PL75-TEI-XML')
        tei['visualScanInspected'] = True
        self.assertTrue(any('A1 TEI contract' in e for e in self.errors(c2)))
        c3 = deepcopy(self.control)
        ocr = next(f for f in c3['files'] if f['id'] == 'OG-NAZ-OR45-JSONL')
        ocr['quoteSafe'] = True
        self.assertTrue(any('class C OCR contract' in e for e in self.errors(c3)))

    def test_pusey_vol2_scan_and_c25_closure_remain_blocked(self):
        c = deepcopy(self.control)
        c['puseyVol2PageImagesInspected'] = True
        self.assertTrue(any('overclaimed boundary puseyVol2PageImagesInspected' in e for e in self.errors(c)))
        c2 = deepcopy(self.control)
        c2['fullCyril1152FragmentGreekOriginalVerified'] = True
        self.assertTrue(any('overclaimed boundary fullCyril1152FragmentGreekOriginalVerified' in e for e in self.errors(c2)))
        c3 = deepcopy(self.control)
        c3['c25'] = 'RESOLVED'
        self.assertTrue(any('status/C25/O10/O11 boundary drift' in e for e in self.errors(c3)))

    def test_cyril_five_locus_and_patristic_card_inventories_are_guarded(self):
        c = deepcopy(self.control)
        c['cyrilFiveLocusSynthesis'].pop('book7FragJohn11_44')
        self.assertTrue(any('Cyril five-locus synthesis inventory drift' in e for e in self.errors(c)))
        c2 = deepcopy(self.control)
        c2['patristicOriginalVerifications'].pop('GRG-1')
        self.assertTrue(any('patristic original verification inventory drift' in e for e in self.errors(c2)))

    def test_actual_git_preimage_and_grg1_baseline_removal_enforced(self):
        r = deepcopy(self.report)
        r['wave9']['supersededSnapshots'][0]['sha256'] = '0' * 64
        self.assertTrue(any('actual Git preimage mismatch' in e for e in self.errors(report=r)))
        r2 = deepcopy(self.report)
        row = next(x for x in r2['repairs'] if x['id'] == 'W9-F11')
        self.assertTrue(row['rejectedWordingPresentInBaseline'])
        row['rejectedWordingPresentInBaseline'] = False
        self.assertTrue(any('invented historical error W9-F11' in e for e in self.errors(report=r2)))

    def test_missing_escaped_and_corrupted_jpeg_replay_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            errors = wave9.verify_sources(Path(d), self.control)
            self.assertEqual(len(errors), 51)
            self.assertTrue(all('missing/symlink file' in e for e in errors))
        c = deepcopy(self.control)
        c['files'][0]['externalRelativePath'] = '../escape'
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(any('path traversal' in e for e in wave9.verify_sources(Path(d), c)))
        bad_bytes = b'NOT_A_JPEG_SCAN'
        c2 = deepcopy(self.control)
        for f in c2['files']:
            f['bytes'] = len(bad_bytes)
            f['sha256'] = wave9.digest(bad_bytes)
            f['gitBlob'] = wave9.git_blob(bad_bytes)
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            for f in c2['files']:
                p = base / f['externalRelativePath']
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(bad_bytes)
            errors = wave9.verify_sources(base, c2)
            self.assertEqual(len(errors), 21)
            self.assertTrue(all('invalid JPEG markers' in e for e in errors))

    def test_all_four_wave9_reviews_and_pipeline_entrypoints_are_wired(self):
        for p in wave9.REGISTRIES:
            review = json.loads((ROOT / 'ИСКУПЛЕНИЕ' / p).read_text(encoding='utf-8'))[wave9.REVIEW_KEY]
            self.assertEqual(review['cramerCoislin23CatenaScanEvidenceClass'], 'A1')
            self.assertTrue(review['coislin23AnonymousFor1152'])
            self.assertEqual(review['puseyVol2DualOcrEvidenceClass'], 'C')
            self.assertFalse(review['oratio4522GreekOcrQuoteSafe'])
            self.assertFalse(review['puseyVol2PageImagesInspected'])
            self.assertFalse(review['fullCyril1152FragmentGreekOriginalVerified'])
            self.assertFalse(review['publicationEligible'])
        self.assertIn('scripts/atonement_wave9_sources.py', reshoot.PIPELINE_FILES)
        self.assertIn('check_wave9(root, report, wave9_control)', (ROOT / 'scripts/atonement_sync_check.py').read_text(encoding='utf-8'))
        self.assertIn('"atonement_wave9_sources.py"', (ROOT / '.github/workflows/atonement-corpus-integrity.yml').read_text(encoding='utf-8'))


if __name__ == "__main__":
    unittest.main(verbosity=2)
