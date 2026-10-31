"""Synthetic negative regressions: never fetch or rewrite research documents."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
from pathlib import Path
import sys
import tarfile
import tempfile
import unicodedata
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import nt_sources as sources
import nt_refs as refs
import verify_nt_citations as citations
import check_nt_card_discipline as discipline
import mt_lookup
import manuscript_collation as manuscripts
import run_audit
from verify_nt_variants import greek_words, parse_tr


class GreekBoundaryTests(unittest.TestCase):
    def test_nfc_equivalence(self):
        q = "ἱλαστήριον"
        self.assertEqual(citations.norm(q), citations.norm(unicodedata.normalize("NFD", q)))

    def test_word_spaces_survive(self):
        # Контракт: границы слов и наличие/позиция ударения сохраняются;
        # нормализуется только позиционная мена острого и тяжёлого (см. ниже).
        self.assertEqual(citations.norm("λύτρον ἀντὶ πολλῶν"), "λύτρον ἀντί πολλῶν")
        self.assertNotEqual(citations.norm("λύτρονἀντὶπολλῶν"), citations.norm("λύτρον ἀντὶ πολλῶν"))

    def test_final_grave_equals_final_acute(self):
        self.assertEqual(citations.norm("παντός"), citations.norm("παντὸς"))

    def test_accent_presence_and_position_still_matter(self):
        self.assertNotEqual(citations.norm("τίς"), citations.norm("τις"))
        self.assertNotEqual(citations.norm("ἀλλά"), citations.norm("ἄλλα"))
        self.assertNotEqual(citations.norm("παντός"), citations.norm("πάντος"))

    def test_substring_is_not_quote(self):
        self.assertFalse(citations.occurs("λυτρ", " ἀπολύτρωσις λύτρον "))
        self.assertFalse(citations.occurs("τρον", " λύτρον "))

    def test_quote_cannot_cross_verses(self):
        self.assertFalse(citations.occurs("λύτρον πολλῶν", " λύτρον \n πολλῶν "))

    def test_whole_phrase(self):
        self.assertTrue(citations.occurs("λύτρον ἀντὶ πολλῶν", " δώσει λύτρον ἀντὶ πολλῶν "))

    def test_case_only_first_character(self):
        self.assertTrue(citations.occurs("Ἰησοῦς", " Ἰησοῦς "))
        self.assertFalse(citations.occurs("θεὸς ἸΗΣΟῦς", " θεὸς Ἰησοῦς "))

    def test_lemma_is_whole_single_word_only(self):
        self.assertTrue(citations.occurs("ἀντί", "", {"ἀντί": 22}))
        self.assertFalse(citations.occurs("ντί", "", {"ἀντί": 22}))
        self.assertFalse(citations.occurs("ἀντί λύτρον", "", {"ἀντί": 22, "λύτρον": 2}))

    def test_ellipsis_keeps_segments_separate(self):
        self.assertEqual(citations.segments("λύτρον … πολλῶν"), ["λύτρον", "πολλῶν"])

    def test_fenced_commands_are_not_inline_quotes(self):
        self.assertNotIn("python", citations.strip_fences("```bash\npython hello\n```\n`λύτρον`"))

    def test_no_text_corpus_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                citations.load_corpus(Path(d))
            with self.assertRaises(ValueError):
                citations.load_lxx(Path(d))

    def test_malformed_row_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "61-Matthew-morphgnt.txt").write_text("010101 N- too short\n")
            with self.assertRaises(ValueError):
                citations.load_corpus(root)

    def test_two_verses_stay_separate_in_loader(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "61-Matthew-morphgnt.txt").write_text(
                "010101 N- ----ASN- N-ASN λύτρον λύτρον λύτρον λύτρον\n"
                "010102 A- ----GPM- A-GPM πολλῶν πολλῶν πολλῶν πολύς\n")
            _, blob = citations.load_corpus(root)
            self.assertFalse(citations.occurs("λύτρον πολλῶν", blob))


class ReferenceTests(unittest.TestCase):
    def test_comma_not_range(self):
        self.assertEqual(refs.expand("Ин 10:11, 15, 26"), {"Ин 10:11", "Ин 10:15", "Ин 10:26"})

    def test_en_dash_range(self):
        self.assertEqual(refs.expand("Ин 6:37–40"), {f"Ин 6:{n}" for n in range(37, 41)})

    def test_em_dash_range(self):
        self.assertEqual(len(refs.expand("Евр 9:26—28")), 3)

    def test_inherited_chapter_book(self):
        self.assertEqual(refs.expand("Мф 23:37; 11:28–30"), {"Мф 23:37", "Мф 11:28", "Мф 11:29", "Мф 11:30"})

    def test_two_books(self):
        self.assertEqual(refs.expand("Мф 23:37 / Лк 13:34"), {"Мф 23:37", "Лк 13:34"})

    def test_single_chapter_comma_and_conjunction(self):
        self.assertEqual(refs.expand("Иуд 4 и 21"), {"Иуд 1:4", "Иуд 1:21"})
        self.assertEqual(refs.expand("Иуд 4, 21"), {"Иуд 1:4", "Иуд 1:21"})

    def test_single_chapter_explicit_not_double(self):
        self.assertEqual(refs.expand("Иуд 1:4"), {"Иуд 1:4"})

    def test_reversed_range_fails(self):
        with self.assertRaises(ValueError):
            refs.expand("Ин 6:40–37")

    def test_zero_fails(self):
        with self.assertRaises(ValueError):
            refs.expand("Ин 0:1")

    def test_bare_numbers_not_a_book(self):
        self.assertEqual(refs.expand("метрика 1:4"), set())


class SourceTests(unittest.TestCase):
    def fixture(self, root):
        (root / "a.txt").write_bytes(b"alpha")
        (root / "b.txt").write_bytes(b"beta")
        digest, count, size = sources.dataset_stats(root)
        return {"sha256OfSet": digest, "files": count, "bytes": size,
                "sha256OfSortedRelativePaths": sources.path_digest(root)}

    def test_good_bytes_and_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            row = self.fixture(root)
            self.assertEqual(sources.verify_dataset("fixture", row, root)[1:], (2, 9))

    def test_corrupt_content_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); row = self.fixture(root)
            (root / "a.txt").write_bytes(b"ALPHA")
            with self.assertRaises(ValueError): sources.verify_dataset("fixture", row, root)

    def test_renamed_file_fails_even_with_same_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); row = self.fixture(root)
            (root / "a.txt").rename(root / "aa.txt")
            self.assertEqual(sources.dataset_stats(root)[0], row["sha256OfSet"])
            with self.assertRaises(ValueError): sources.verify_dataset("fixture", row, root)

    def test_empty_dataset_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): sources.dataset_stats(Path(d))

    def test_count_and_size_not_advisory(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); row = self.fixture(root)
            for key in ("files", "bytes"):
                wrong = dict(row); wrong[key] += 1
                with self.assertRaises(ValueError): sources.verify_dataset("fixture", wrong, root)

    def test_symlink_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.fixture(root)
            (root / "link").symlink_to(root / "a.txt")
            with self.assertRaises(ValueError): sources.dataset_stats(root)

    def test_missing_dataset_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): sources.dataset_stats(Path(d) / "missing")

    def test_in_repo_acquisition_rejected(self):
        with patch.dict(os.environ, {"NT_CORPUS_HOME": str(sources.ROOT)}):
            with self.assertRaises(ValueError): sources.corpus_home()
        with self.assertRaises(ValueError):
            sources.fetch_witness("S7", {"repository":"test/repo", "commit":"a"*40}, sources.ROOT)

    def test_registry_duplicate_fails(self):
        data = sources.registry(); data["textWitnesses"].append(data["textWitnesses"][0])
        with patch.object(sources, "registry", return_value=data):
            with self.assertRaises(ValueError): sources.witnesses()

    def test_registry_moving_ref_fails(self):
        data = sources.registry(); data["textWitnesses"][0]["commit"] = "master"
        with patch.object(sources, "registry", return_value=data):
            with self.assertRaises(ValueError): sources.witnesses()

    def archive(self, name, kind=tarfile.REGTYPE):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w") as tar:
            item = tarfile.TarInfo(name); item.type = kind
            if kind == tarfile.REGTYPE: item.size = 1
            tar.addfile(item, io.BytesIO(b"x") if item.isfile() else None)
        stream.seek(0)
        return stream

    def test_archive_regular_file_python311(self):
        with tempfile.TemporaryDirectory() as d, tarfile.open(fileobj=self.archive("repo/xml/a.xml")) as tar:
            sources.safe_extract(tar, Path(d))
            self.assertEqual((Path(d)/"repo/xml/a.xml").read_bytes(), b"x")

    def test_archive_traversal_and_absolute_rejected(self):
        for name in ("../escape", "/absolute", "repo/../escape"):
            with tempfile.TemporaryDirectory() as d, tarfile.open(fileobj=self.archive(name)) as tar:
                with self.assertRaises(ValueError): sources.safe_extract(tar, Path(d))

    def test_archive_links_and_devices_rejected(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.CHRTYPE):
            with tempfile.TemporaryDirectory() as d, tarfile.open(fileobj=self.archive("repo/link", kind)) as tar:
                with self.assertRaises(ValueError): sources.safe_extract(tar, Path(d))


class MethodTests(unittest.TestCase):
    CARD = """## 06.1 Мф 1:1
**Ось:** `extent`
**Текст S1:** `λύτρον`
**Синтаксис:** Конкретный синтаксический факт с ограниченным объектом.
**Контекст:** Конкретная перикопа и её аргумент, не пустой маркер.
**Чтения:** `A` particular / `B` universal, обе с текстовым основанием.
**Что не доказывает:** Не определяет численный объём искупления.
**Связь с ВЗ:** Прямой цитаты в этом локусе не заявляется.
"""
    def check(self, text, fn):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"06_test.md"; p.write_text(text)
            return fn([p])[1]

    def test_method_complete(self): self.assertEqual(self.check(self.CARD, discipline.check_method), [])
    def test_deleted_primary_not_service_section(self):
        self.assertTrue(self.check(self.CARD.replace("**Текст S1:** `λύτρον`\n", ""), discipline.check_method))
    def test_empty_context_rejected(self):
        self.assertTrue(self.check(self.CARD.replace("Конкретная перикопа и её аргумент, не пустой маркер.", ""), discipline.check_method))
    def test_body_mentions_not_readings(self):
        self.assertTrue(self.check(self.CARD.replace("**Чтения:**", "**Другие данные:**"), discipline.check_readings))
    def test_dash_axis_rejected(self):
        self.assertTrue(self.check(self.CARD.replace("`extent`", "—"), discipline.check_axis))
    def test_valid_axis_cannot_hide_invalid_extra(self):
        self.assertTrue(self.check(self.CARD.replace("`extent`", "`extent` + `whatever`"), discipline.check_axis))


class ForbiddenPhraseTests(unittest.TestCase):
    """Списки запрета не должны читаться как утверждения, и наоборот."""

    def probe(self, line):
        return discipline._norm(discipline._mask_prohibitions(discipline._mask_mentions(line)))

    def test_prohibition_list_masks_phrase(self):
        line = "**Нельзя:** объявлять стих решённым; приписывать Кальвину сноску редактора."
        self.assertIsNone(re.search(r"стих\s+реш[ёе]н", self.probe(line)))

    def test_prohibition_scope_stops_at_semicolon(self):
        line = "Здесь текст закрыт; нельзя медлить с проверкой."
        self.assertIsNotNone(re.search(r"текст\s+закрыт", self.probe(line)))

    def test_prohibition_without_negation_still_flags(self):
        line = "Можно объявлять стих решённым и идти дальше."
        self.assertIsNotNone(re.search(r"стих\s+реш[ёе]н", self.probe(line)))

    def test_negated_assertion_masked_but_quoted_mention_kept(self):
        line = "Нельзя утверждать, что тексты закрыты; в 5:18 `πάντες` — все без изъятия."
        probe = self.probe(line)
        self.assertIsNone(re.search(r"текст\w*\s+закрыт", probe))
        self.assertIn("5:18", probe)


class ParserAndExitTests(unittest.TestCase):
    def test_tf_empty_feature_slots_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/"word.tf").write_text("@node\n@valueType=str\n\nfirst\n\nthird\n")
            mt = object.__new__(mt_lookup.MT); mt.root = root
            self.assertEqual(mt._node_feature("word.tf"), {1:"first", 2:"", 3:"third"})

    def test_tf_sparse_node_indices(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/"word.tf").write_text("@node\n\n5\tvalue\n\n")
            mt = object.__new__(mt_lookup.MT); mt.root = root
            self.assertEqual(mt._node_feature("word.tf"), {5:"value", 6:""})

    def test_tr_title_and_continued_verse(self):
        self.assertEqual(parse_tr("1:1 [TITLE]\n logos\n yeov\n1:2 kai\n"), {(1,1):["logos","yeos"], (1,2):["kai"]})

    def test_tr_duplicate_verse_fails(self):
        with self.assertRaises(ValueError): parse_tr("1:1 logos\n1:1 logos\n")

    def test_greek_to_robinson_ascii(self):
        self.assertEqual(greek_words("χάριτι θεοῦ"), ["cariti","yeou"])

    def test_manuscript_word_not_substring(self):
        u = manuscripts.Unit("test", "Мк", 1, 1, "1", "λυσαντι", [("a","λυσαντι",[])])
        self.assertFalse(manuscripts.unit_matches(u, "word", ["αντι"]))
        self.assertTrue(manuscripts.unit_matches(u, "stem", ["λυσ"]))

    def test_manuscript_unknown_argument_fails(self):
        with self.assertRaises(ValueError): manuscripts.main(["--verfiy"])


class UniquePathsTests(unittest.TestCase):
    """Один файл обязан проверяться один раз, как бы его ни назвали."""

    def test_same_file_absolute_and_relative_is_one(self):
        import os
        base = Path(citations.CARD_DIR)
        abs_path = base / "09_NT_EXTENT_THREE_COLUMN_TABLE.md"
        rel_path = Path(os.path.relpath(abs_path, Path.cwd()))
        self.assertNotEqual(str(abs_path), str(rel_path))
        self.assertEqual(len(citations.unique_paths([abs_path, rel_path])), 1)

    def test_distinct_files_both_kept_in_order(self):
        base = Path(citations.CARD_DIR)
        a = base / "09_NT_EXTENT_THREE_COLUMN_TABLE.md"
        b = base / "11_NT_LXX_COLLATION.md"
        self.assertEqual(citations.unique_paths([a, b, a]), [a, b])


class RunnerTests(unittest.TestCase):
    def test_default_no_implicit_fetch_and_genesis_in_scope(self):
        names = [name for name, argv in run_audit.commands()]
        self.assertNotIn("Explicit outside-Git acquisition", names)
        self.assertIn("genesis6_authority_manifest", names)

    def test_failure_not_masked_by_tail_or_name(self):
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()):
            records = run_audit.run_checks([
                ("genesis6_authority_manifest", [sys.executable,"-c","import sys; print('FAIL early'); print('nice final line'); sys.exit(1)"]),
                ("following check", [sys.executable,"-c","print('PASS')"])], Path(d), dict(os.environ), immutable=False)
            self.assertEqual([r["rc"] for r in records], [1,0])
            self.assertIn("FAIL early", (Path(d)/"01.log").read_text())

    def test_tree_mutation_invalidates_receipt(self):
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()), \
             patch.object(run_audit,"tree_fingerprint",side_effect=["before","after"]):
            records = run_audit.run_checks([("check",[sys.executable,"-c","print('PASS')"])],Path(d),dict(os.environ))
            self.assertEqual(records[0]["rc"],1)
            self.assertIn("tree mutated",(Path(d)/"01.log").read_text())


class SignTests(unittest.TestCase):
    """Знаки SBLGNT живут в поле 4 MorphGNT; §9.122 утверждал обратное."""

    def test_inventory_is_pinned(self):
        self.assertEqual(refs.s1_sign_inventory(),
                         {"⸀": 5114, "⸁": 46, "⸂": 1764, "⸃": 1765, "⸄": 6, "⸅": 5})

    def test_clean_field_has_no_signs(self):
        for row in refs.s1_verses().values():
            for token in row:
                self.assertFalse(any(m in token[5] for m in refs.SIGN_MARKS), token)

    def test_spans_per_verse(self):
        verses = refs.s1_verses()
        self.assertEqual(refs.s1_sign_spans(verses["Мф 20:28"]), 0)
        self.assertEqual(refs.s1_sign_spans(verses["Мк 10:45"]), 0)
        self.assertEqual(refs.s1_sign_spans(verses["Евр 2:9"]), 1)
        self.assertEqual(refs.s1_sign_spans(verses["Мк 14:24"]), 2)
        self.assertEqual(refs.s1_sign_spans(verses["Деян 20:28"]), 3)

    def test_marked_token_locators(self):
        self.assertIn("⸀τῆς", refs.s1_sign_tokens("Мк 14:24"))
        self.assertIn("⸂ἐκχυννόμενον", refs.s1_sign_tokens("Мк 14:24"))
        self.assertIn("⸀θεοῦ,", refs.s1_sign_tokens("Деян 20:28"))
        self.assertEqual(refs.s1_sign_tokens("Мф 20:28"), [])

    def test_total_positions_pinned(self):
        by_ref = refs.s1_sign_spans_by_ref()
        self.assertEqual(sum(by_ref.values()), 6930)
        self.assertEqual(len(by_ref), 4472)


if __name__ == "__main__":
    unittest.main()
