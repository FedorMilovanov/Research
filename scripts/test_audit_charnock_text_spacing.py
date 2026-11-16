import unittest

from audit_charnock_text_spacing import findings, propose, scan


class SpacingDetectorTests(unittest.TestCase):
    def test_dropped_space_between_number_and_word(self):
        kinds = [hit["kind"] for hit in findings("Погребение30июля1680")]
        self.assertEqual(kinds, ["digit_then_word", "word_then_digit"])

    def test_dropped_space_after_punctuation_is_detected(self):
        self.assertEqual([h["match"] for h in findings("справочник;главы")], [";г"])

    def test_dropped_space_after_em_dash(self):
        self.assertEqual([h["kind"] for h in findings("итог —16§21.109")], ["dash_then_token"])

    def test_ranges_keep_their_dashes(self):
        for text in ("27–28 июля", "1660—1680", "§§21.138–21.139"):
            self.assertEqual(findings(text), [], text)
            fixed, changes = propose(text)
            self.assertEqual((fixed, changes), (text, []))

    def test_scripture_references_and_times_are_not_flagged(self):
        for text in ("Рим3:9–12", "1Тим2:15", "09:51:57Z", "p.265", "vol.16", "§§21.138", "A71277"):
            self.assertEqual(findings(text), [], text)

    def test_repair_only_inserts_spaces(self):
        fixed, changes = propose("около1644 и 5шиллингов")
        self.assertEqual(fixed, "около 1644 и 5 шиллингов")
        self.assertEqual(len(changes), 2)

    def test_repair_leaves_references_untouched(self):
        fixed, changes = propose("Пс32; p.265; Hoek1:532")
        self.assertEqual(fixed, "Пс32; p.265; Hoek1:532")
        self.assertEqual(changes, [])

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


if __name__ == "__main__":
    unittest.main()
