"""Coverage and non-promotion guards, not medical or theological adjudication."""
import json
import unittest

from audit_charnock_prayer import ROOT, FALSE_FLAGS, check_review, digest


class PrayerTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT / self.plan['baselineRegistry']).read_text())
        self.review = self.plan['prayerCompleteReview']
        self.data = self.review['byteVerifiedReading']

    def check(self):
        return check_review(self.plan, self.registry)

    def test_76_paragraphs_plus_authorial_doctrine(self):
        self.assertEqual(self.check(), dict(
            prayerMainTextParagraphs=76, prayerMainTextUnits=77,
            prayerAdditionalMainBodyParagraphs=75, prayerMarginalNotes=2,
            prayerObservations=28, prayerWholeMainTextRead=True))

    def test_no_paragraph_gap(self):
        self.data['contextWindow'].pop(27)
        with self.assertRaises(ValueError):
            self.check()

    def test_doctrine_required(self):
        self.data['standaloneDoctrine'] = []
        with self.assertRaises(ValueError):
            self.check()

    def test_doctrine_not_foreign_quote(self):
        self.data['standaloneDoctrine'][0]['voice'] = 'REYNOLDS_QUOTATION'
        with self.assertRaises(ValueError):
            self.check()

    def test_pagination_not_silently_corrected(self):
        self.data['openingPageBreaks'][0]['n'] = '56'
        with self.assertRaises(ValueError):
            self.check()

    def test_source_pin(self):
        self.data['sourceSha256'] = '0' * 64
        with self.assertRaises(ValueError):
            self.check()

    def test_next_discourse_excluded(self):
        self.data['nextParagraph']['paragraphIndexZeroBased'] = 331
        with self.assertRaises(ValueError):
            self.check()

    def test_previous_boundary_retained(self):
        self.plan['fifthNovemberCompleteReview']['byteVerifiedReading'][
            'nextParagraph']['text'] = 'Altered old boundary'
        with self.assertRaises(ValueError):
            self.check()

    def test_all_non_promotion_flags(self):
        for key in FALSE_FLAGS:
            with self.subTest(key=key):
                self.review[key] = True
                with self.assertRaises(ValueError):
                    self.check()
                self.review[key] = False

    def test_actual_span(self):
        observation = self.review['observations'][0]
        observation['englishSpan'] = 'Every wish is immediately fulfilled'
        observation['englishSpanSha256'] = digest(observation['englishSpan'])
        with self.assertRaises(ValueError):
            self.check()

    def test_common_providence_not_deleted(self):
        paragraph = self.data['contextWindow'][326 - 256]
        paragraph['text'] = paragraph['text'].replace('common providence', 'guaranteed regeneration')
        paragraph['textSha256'] = digest(paragraph['text'])
        with self.assertRaises(ValueError):
            self.check()

    def test_no_reynolds_acquisition_claim(self):
        self.review['marginalNoteDecisions'][1]['counterpartRawAcquired'] = True
        with self.assertRaises(ValueError):
            self.check()

    def test_part_vii_link(self):
        next(d for d in self.plan['documents'] if d['id'] == 'VII')[
            'supplementaryMainTextReadings'].remove('prayerCompleteReview')
        with self.assertRaises(ValueError):
            self.check()

    def test_holds_not_released(self):
        self.review['observations'][0]['holds'] = []
        with self.assertRaises(ValueError):
            self.check()


if __name__ == '__main__':
    unittest.main()
