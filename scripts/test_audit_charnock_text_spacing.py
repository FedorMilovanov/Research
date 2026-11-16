import json
import unittest

from audit_charnock_text_spacing import findings, propose, scan


class SpacingDetectorTests(unittest.TestCase):
    def test_dropped_space_between_number_and_word(self):
        kinds = [hit["kind"] for hit in findings("Погребение30июля1680")]
        self.assertEqual(kinds, ["digit_then_word", "word_then_digit"])

    def test_dropped_space_after_punctuation_is_detected(self):
        self.assertEqual([h["match"] for h in findings("справочник;главы")], [";г"])

    def test_dropped_space_after_em_dash(self):
        self.assertEqual([h["kind"] for h in findings("итог —16§21.109")], ["digit_then_section", "dash_then_token"])

    def test_ranges_keep_their_dashes(self):
        for text in ("27–28 июля", "1660—1680", "§§21.138–21.139"):
            self.assertEqual(findings(text), [], text)
            fixed, changes = propose(text)
            self.assertEqual((fixed, changes), (text, []))

    def test_number_glued_to_latin_abbreviation(self):
        self.assertEqual(propose("79TCP/11XML")[0], "79 TCP/11 XML")

    def test_section_ids_and_urls_are_not_split(self):
        for text in ("04 §0AB.3", "§0AA", "LtbD-4FWpPcC", "%5BCG%20v2", "CLOSURE_60PLUS_2026"):
            self.assertEqual(propose(text), (text, []), text)

    def test_source_ids_are_never_split(self):
        for text in ("A71277", "B02133", "A32726.0001.001", "wave40"):
            self.assertEqual(propose(text), (text, []))

    def test_number_glued_to_section_sign(self):
        self.assertEqual(propose("16§§21.10–21.11")[0], "16 §§21.10–21.11")
        self.assertEqual(propose("§21.8")[0], "§21.8")

    def test_scripture_references_and_times_are_not_flagged(self):
        for text in ("Рим3:9–12", "1Тим2:15", "09:51:57Z", "p.265", "vol.16", "§§21.138", "A71277"):
            self.assertEqual(findings(text), [], text)

    def test_repair_only_inserts_spaces(self):
        fixed, changes = propose("около1644 и 5шиллингов")
        self.assertEqual(fixed, "около 1644 и 5 шиллингов")
        self.assertEqual(len(changes), 2)

    def test_repair_leaves_references_untouched(self):
        for text in ("Пс32; p.265; Hoek1:532", "1Тим2:15", "1Тим1:15 и 2Тим3:16", "Рим3:9–12"):
            fixed, changes = propose(text)
            self.assertEqual((fixed, changes), (text, []), text)

    def test_repairer_and_detector_share_one_predicate(self):
        # wave46: the repairer used to insert spaces the detector never flagged,
        # turning the author's `1Тим2:15` into `1Тим 2:15` in 18 places.
        for text in ("1Тим2:15", "Пс32", "Год1628 приблизителен", "Том03 §14", "Все6 пунктов"):
            fixed, _ = propose(text)
            self.assertEqual(findings(fixed), [], fixed)
        self.assertEqual(propose("Год1628 приблизителен")[0], "Год 1628 приблизителен")
        self.assertEqual(propose("Все6 пунктов")[0], "Все 6 пунктов")

    def test_reader_facing_documents_are_clean(self):
        report = scan(scope="documents")
        self.assertEqual(report["totalFindings"], 0, report["files"])
        self.assertEqual(report["state"], "TEXT_SPACING_CLEAN")

    def test_live_corpus_report_shape(self):
        report = scan()
        self.assertIn(report["state"], {"TEXT_SPACING_DEFECT_OPEN", "TEXT_SPACING_CLEAN"})
        self.assertEqual(report["totalFindings"], sum(v["count"] for v in report["files"].values()))
        self.assertEqual(
            report["totalFindings"],
            sum(report["byKind"].values()),
        )
        for entry in report["files"].values():
            self.assertEqual(len(entry["samples"]), min(5, entry["count"]))


class VerbatimSnapshotTests(unittest.TestCase):
    """The plan keeps two byte-exact copies of the shared atlas: exempt but checked."""

    def test_shared_atlas_snapshots_are_exempt_but_verified(self):
        report = scan("all")
        self.assertEqual(report["totalFindings"], 0, report["files"])
        self.assertEqual(report["verbatimSnapshotsVerified"], 2)

    def test_snapshot_that_drifted_from_the_atlas_is_not_exempted(self):
        from audit_charnock_text_spacing import ATLAS, ROOT, text_for_scan
        atlas = json.loads(ATLAS.read_text(encoding="utf-8"))
        atlas["edges"] = []
        with self.assertRaisesRegex(ValueError, "verbatim snapshot drifted"):
            text_for_scan(ROOT / "data/charnock-series-editorial-plan-v1.json", {}, atlas)


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
