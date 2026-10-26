"""Guard coverage, historical scopes and non-promotion, not theological truth."""
import json
import unittest

from audit_charnock_fifth_november import ROOT, FALSE_FLAGS, check_review, digest


class FifthNovemberTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT / self.plan['baselineRegistry']).read_text())
        self.review = self.plan['fifthNovemberCompleteReview']
        self.data = self.review['byteVerifiedReading']

    def check(self):
        return check_review(self.plan, self.registry)

    def test_71_paragraphs_68_additional(self):
        self.assertEqual(self.check(), dict(
            fifthNovemberMainTextParagraphs=71, fifthNovemberAdditionalParagraphs=68,
            fifthNovemberMarginalNotes=7, fifthNovemberObservations=31,
            fifthNovemberWholeMainTextRead=True, fifthNovemberPreachingYearVerified=False))

    def test_no_body_gap(self):
        self.data['context']['contextWindow'].pop(30)
        with self.assertRaises(ValueError):
            self.check()

    def test_pagination_not_corrected(self):
        self.data['nextParagraph']['startTeiPage'] = '56'
        with self.assertRaises(ValueError):
            self.check()

    def test_number_not_corrected_even_with_rehashed_text(self):
        paragraph = self.data['context']['contextWindow'][250 - 185]
        paragraph['text'] = paragraph['text'].replace(
            'One thousand six hundred and twenty years', 'One thousand two hundred and sixty years')
        paragraph['textSha256'] = digest(paragraph['text'])
        with self.assertRaises(ValueError):
            self.check()

    def test_epigraph_retained(self):
        self.data['epigraph'] = ''
        with self.assertRaises(ValueError):
            self.check()

    def test_source_pin(self):
        self.data['context']['sourceSha256'] = '0' * 64
        with self.assertRaises(ValueError):
            self.check()

    def test_historical_three_paragraphs_not_replaced(self):
        self.plan['pastoralReview']['byteVerifiedContexts']['TXT-19']['contextWindow'].pop()
        with self.assertRaises(ValueError):
            self.check()

    def test_actual_english_span(self):
        observation = self.review['observations'][0]
        observation['englishSpan'] = 'Delivered in Dublin in a certain year'
        observation['englishSpanSha256'] = digest(observation['englishSpan'])
        with self.assertRaises(ValueError):
            self.check()

    def test_no_foreign_original_promotion(self):
        self.review['marginalNoteDecisions'][1]['counterpartRawAcquired'] = True
        with self.assertRaises(ValueError):
            self.check()

    def test_no_release(self):
        self.review['observations'][0]['publicationState'] = 'READY'
        with self.assertRaises(ValueError):
            self.check()

    def test_all_false_flags_guarded(self):
        for key in FALSE_FLAGS:
            with self.subTest(key=key):
                self.review[key] = True
                with self.assertRaises(ValueError):
                    self.check()
                self.review[key] = False

    def test_no_invented_standalone_doctrine(self):
        self.data['directTags'].append('q')
        with self.assertRaises(ValueError):
            self.check()

    def test_series_integration_required(self):
        next(d for d in self.plan['documents'] if d['id'] == 'VII')[
            'supplementaryMainTextReadings'].remove('fifthNovemberCompleteReview')
        with self.assertRaises(ValueError):
            self.check()

    def test_lexical_note_not_another_author(self):
        self.review['marginalNoteDecisions'][0]['kind'] = 'SOURCE_POINTER'
        with self.assertRaises(ValueError):
            self.check()


if __name__ == '__main__':
    unittest.main()
