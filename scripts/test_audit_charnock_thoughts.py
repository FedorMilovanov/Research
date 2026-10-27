"""Fail closed on bounded reading, involuntary motions and unverified counterparts."""
import json
import unittest

from audit_charnock_thoughts import ROOT, FALSE_FLAGS, check_review, digest


class ThoughtsOpeningTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT / self.plan['baselineRegistry']).read_text())
        self.review = self.plan['thoughtsOpeningReview']
        self.data = self.review['byteVerifiedReading']

    def check(self):
        return check_review(self.plan, self.registry)

    def test_bounded38_not_whole(self):
        self.assertEqual(self.check(), dict(
            thoughtsOpeningParagraphs=38, thoughtsOpeningMarginalNotes=34,
            thoughtsOpeningObservations=21, thoughtsWholeDiscourseRead=False,
            thoughtsCureSectionRead=False, cartesianCounterpartVerified=False))

    def test_all_false_flags(self):
        for key in FALSE_FLAGS:
            with self.subTest(key=key):
                self.review[key] = True
                with self.assertRaises(ValueError):
                    self.check()
                self.review[key] = False

    def test_no_paragraph_gap(self):
        self.data['contextWindow'].pop(4)
        with self.assertRaises(ValueError):
            self.check()

    def test_proposition_is_paragraph_not_extra_quote(self):
        self.data['standaloneQuotes'] = ['A purported foreign proposition']
        with self.assertRaises(ValueError):
            self.check()

    def test_source_pin(self):
        self.data['sourceSha256'] = '0' * 64
        with self.assertRaises(ValueError):
            self.check()

    def test_same_discourse_continues(self):
        self.data['nextParagraph']['boundary'] = 'FINIS'
        with self.assertRaises(ValueError):
            self.check()

    def test_nonconsent_clause_not_sanitized(self):
        row = self.data['contextWindow'][18 - 3]
        row['text'] = row['text'].replace(
            'These are sins, though we consent not to them',
            'These are innocent unless we consent')
        row['textSha256'] = digest(row['text'])
        with self.assertRaises(ValueError):
            self.check()

    def test_bare_apprehension_not_made_criminal(self):
        row = self.data['contextWindow'][16 - 3]
        row['text'] = row['text'].replace(
            'A simple apprehension of sin is not sinful',
            'A simple apprehension of sin is always sinful')
        row['textSha256'] = digest(row['text'])
        with self.assertRaises(ValueError):
            self.check()

    def test_mixed_targum_note_not_a_new_original(self):
        self.review['marginalNoteDecisions'][33]['kind'] = 'SOURCE_POINTER'
        with self.assertRaises(ValueError):
            self.check()

    def test_cross_page_note(self):
        self.data['marginalNotes'][-1]['teiPage'] = '5'
        with self.assertRaises(ValueError):
            self.check()

    def test_no_counterpart_acquisition(self):
        self.review['cartesianCounterpartSearch']['originalRawAcquired'] = True
        with self.assertRaises(ValueError):
            self.check()

    def test_search_not_global_absence(self):
        self.review['cartesianCounterpartSearch']['claimOfGlobalAbsence'] = True
        with self.assertRaises(ValueError):
            self.check()

    def test_candidate_metadata_not_full_object(self):
        self.review['cartesianCounterpartSearch']['accessState'] = 'FULL_OBJECT_VERIFIED'
        with self.assertRaises(ValueError):
            self.check()

    def test_part_vii_opening_link(self):
        next(d for d in self.plan['documents'] if d['id'] == 'VII')[
            'supplementaryOpeningReadings'].remove('thoughtsOpeningReview')
        with self.assertRaises(ValueError):
            self.check()

    def test_no_release(self):
        self.review['observations'][0]['holds'] = []
        with self.assertRaises(ValueError):
            self.check()



class ThoughtsCompleteTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT / self.plan['baselineRegistry']).read_text())
        self.review = self.plan['thoughtsCompleteReview']
        self.data = self.review['byteVerifiedReading']

    def check(self):
        from audit_charnock_thoughts import check_complete
        return check_complete(self.plan, self.registry)

    def test_complete89_and_eight_routes(self):
        self.assertEqual(self.check(), dict(
            thoughtsMainTextParagraphs=89, thoughtsAdditionalParagraphs=51,
            thoughtsMarginalNotes=139, thoughtsContinuationObservations=32,
            thoughtsWholeDiscourseRead=True, thoughtsCureSectionRead=True,
            oneTcpVolumeMainTextRoutes=8, allCharnockWorksRead=False))

    def test_continuation_gap(self):
        self.data['continuationContextWindow'].pop()
        with self.assertRaises(ValueError):
            self.check()

    def test_manifest_gap(self):
        self.data['mainTextManifest'].pop()
        with self.assertRaises(ValueError):
            self.check()

    def test_old34_notes_preserved(self):
        self.data['marginalNotes'][0]['text'] = 'Changed opening note'
        with self.assertRaises(ValueError):
            self.check()

    def test_no_additional_authorial_q(self):
        self.data['directTags'].append('q')
        with self.assertRaises(ValueError):
            self.check()

    def test_stability_is_boundary(self):
        self.data['nextParagraph']['paragraphIndexZeroBased'] = 91
        with self.assertRaises(ValueError):
            self.check()

    def test_source_pin(self):
        self.data['sourceSha256'] = '0' * 64
        with self.assertRaises(ValueError):
            self.check()

    def test_no_edition_therapy_or_impression_promotion(self):
        from audit_charnock_thoughts import COMPLETE_FALSE_FLAGS
        for key in COMPLETE_FALSE_FLAGS:
            with self.subTest(key=key):
                self.review[key] = True
                with self.assertRaises(ValueError):
                    self.check()
                self.review[key] = False

    def test_full_read_includes_cure(self):
        for key in ['wholeDiscourseRead', 'cureSectionRead']:
            with self.subTest(key=key):
                self.review[key] = False
                with self.assertRaises(ValueError):
                    self.check()
                self.review[key] = True

    def test_no_external_original_acquisition(self):
        self.review['additionalMarginalNoteDecisions'][0]['counterpartRawAcquired'] = True
        with self.assertRaises(ValueError):
            self.check()

    def test_catechism_note_not_identified_book(self):
        self.review['additionalMarginalNoteDecisions'][87 - 34]['kind'] = 'SOURCE_POINTER'
        with self.assertRaises(ValueError):
            self.check()

    def test_haunt_lodge_distinction_not_removed(self):
        row = self.data['continuationContextWindow'][82 - 41]
        row['text'] = row['text'].replace('Though we cannot hinder them from haunting us',
                                         'If they return you necessarily consented')
        row['textSha256'] = digest(row['text'])
        with self.assertRaises(ValueError):
            self.check()

    def test_heavenward_refusal_not_removed(self):
        row = self.data['continuationContextWindow'][85 - 41]
        row['text'] = row['text'].replace('is a refusal of the thought that presseth upon you',
                                         'is never counted as a refusal')
        row['textSha256'] = digest(row['text'])
        with self.assertRaises(ValueError):
            self.check()

    def test_volume_map_not_truncated_at_direct_pardon_paragraph(self):
        self.data['volumeMainTextRanges'][-1]['end'] = 620
        with self.assertRaises(ValueError):
            self.check()

    def test_extract_volume_ranges_include_nested_div_descendants(self):
        import hashlib
        import tempfile
        import xml.etree.ElementTree as ET
        from pathlib import Path
        from audit_charnock_thoughts import extract_complete, VOLUME_RANGES, HEADING
        from audit_charnock_book_route import NS
        root = ET.Element(NS + 'TEI')
        front = ET.SubElement(root, NS + 'front')
        for i in range(3):
            ET.SubElement(front, NS + 'p').text = 'Front ' + str(i)
        body = ET.SubElement(root, NS + 'body')
        for index, (start, end) in enumerate(VOLUME_RANGES):
            div = ET.SubElement(body, NS + 'div')
            ET.SubElement(div, NS + 'pb', {'n': str(index + 1)})
            ET.SubElement(div, NS + 'head').text = HEADING if index == 0 else 'Fixture discourse'
            epigraph = ET.SubElement(div, NS + 'epigraph')
            ET.SubElement(epigraph, NS + 'p').text = 'Epigraph ' + str(start)
            nested = None
            for number in range(start + 1, end + 1):
                if index == 7 and number == 621:
                    nested = ET.SubElement(div, NS + 'div')
                parent = nested if nested is not None else div
                ET.SubElement(parent, NS + 'p').text = 'Body ' + str(number)
        raw = ET.tostring(root)
        registry = {'sources': {'A32724': {'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}}}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / 'A32724.xml').write_bytes(raw)
            reading = extract_complete(directory, registry)
        self.assertEqual([(r['start'], r['end']) for r in reading['volumeMainTextRanges']], VOLUME_RANGES)
        self.assertEqual(reading['volumeMainTextRanges'][-1]['end'], 691)


if __name__ == '__main__':
    unittest.main()
