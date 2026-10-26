"""Plan provenance and synthetic XML tests;not certification of future reader prose."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from audit_charnock_editorial_links import ROOT, check_review, extract


class EditorialRoutingTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT / self.plan['baselineRegistry']).read_text())
        self.review = self.plan['routingReview']

    def check(self):
        return check_review(self.plan, self.registry)

    def test_current_bounded_review(self):
        result = self.check()
        self.assertEqual(result['routedContextReceptionReferences'], 11)
        self.assertEqual(result['ownershipHandoffs'], 5)
        self.assertFalse(result['draftDeduplicationVerified'])

    def test_future_drafts_not_claimed_reviewed(self):
        self.review['draftDeduplicationVerified'] = True
        with self.assertRaisesRegex(ValueError, 'plan-level'):
            self.check()

    def test_foreign_quotes_not_claimed_reverified(self):
        self.review['foreignQuotationsReverified'] = True
        with self.assertRaisesRegex(ValueError, 'plan-level'):
            self.check()

    def test_hoek_positive_conclusion_required(self):
        self.review['contextReceptionDecisions'] = [c for c in self.review['contextReceptionDecisions'] if c['ref'] != 'REC-06']
        with self.assertRaisesRegex(ValueError, 'Every selected'):
            self.check()

    def test_hoek_pairing_not_optional(self):
        c = next(c for c in self.review['contextReceptionDecisions'] if c['ref'] == 'REC-05')
        c['requiredCompanionRefs'] = []
        with self.assertRaisesRegex(ValueError, 'must remain paired'):
            self.check()

    def test_context_holds_not_removed(self):
        self.review['contextReceptionDecisions'][0]['sourceStateSnapshot']['holds'] = []
        with self.assertRaisesRegex(ValueError, 'cannot promote evidence'):
            self.check()

    def test_two_full_analysis_owners_rejected(self):
        self.review['ownershipHandoffs'][0]['sharedRefOwners']['TXT-14'] = 'VI'
        with self.assertRaisesRegex(ValueError, 'one full-analysis owner'):
            self.check()

    def test_historical_contact_not_inferred_from_navigation(self):
        self.review['corpusBridges'][0]['relation'] = 'HISTORICAL_INFLUENCE'
        with self.assertRaisesRegex(ValueError, 'cannot assert historical contact'):
            self.check()

    def test_original_owner_excerpt_bytes_required(self):
        self.review['corpusBridges'][0]['ownerExcerpt']['text'] += ' fabricated'
        with self.assertRaisesRegex(ValueError, 'actual bytes'):
            self.check()

    def test_atlas_exclusion_cannot_be_silently_dropped(self):
        self.review['excludedLinksSnapshot'].pop()
        with self.assertRaisesRegex(ValueError, 'Atlas types/exclusions'):
            self.check()

    def test_transition_questions_not_silently_dropped(self):
        self.review['transitionQuestions'].pop()
        with self.assertRaisesRegex(ValueError, 'Nine adjacent'):
            self.check()

    def test_noncoercion_qualification_not_dropped(self):
        self.review['byteVerifiedContexts']['A41722']['paragraphs'].pop(1)
        with self.assertRaisesRegex(ValueError, 'all three constitutional'):
            self.check()

    def test_canonical_anchor_fingerprint_must_match(self):
        self.review['contextReceptionDecisions'][0]['canonicalAnchorSha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'cannot promote evidence'):
            self.check()


class NormExtractionTests(unittest.TestCase):
    def fixture(self, duplicate=False, missing=False):
        norms = ['<p>XXXV. Synthetic public profession.</p>', '<p>XXXVI. Synthetic noncoercion.</p>', '<p>XXXVII. Synthetic conditional protection.</p>']
        if duplicate:
            norms.append(norms[0])
        if missing:
            norms.pop(1)
        ad = '<p>THE Works of Mr. Stephen Charnock on Various Divine Subjects. In Folio. 2 Vol.</p>'
        raw = {identifier: ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div><pb n="17"/>' + text + '</div></body></text></TEI>').encode()
               for identifier, text in [('A41722', ''.join(norms)), ('B20167', ad)]}
        registry = dict(sources={key:dict(size=len(value), sha256=hashlib.sha256(value).hexdigest()) for key,value in raw.items()})
        return raw, registry

    def run_fixture(self, raw, registry):
        with tempfile.TemporaryDirectory() as directory:
            for key, value in raw.items():
                (Path(directory) / (key + '.xml')).write_bytes(value)
            return extract(Path(directory), registry)

    def test_three_norms_and_one_advertisement(self):
        result = self.run_fixture(*self.fixture())
        self.assertEqual(len(result['A41722']['paragraphs']), 3)
        self.assertEqual(len(result['B20167']['paragraphs']), 1)

    def test_source_bytes_required(self):
        raw, registry = self.fixture()
        raw['A41722'] += b' '
        with self.assertRaisesRegex(ValueError, 'byte pin mismatch'):
            self.run_fixture(raw, registry)

    def test_unique_norm_required(self):
        with self.assertRaisesRegex(ValueError, 'unique paragraph'):
            self.run_fixture(*self.fixture(duplicate=True))

    def test_noncoercion_norm_required(self):
        with self.assertRaisesRegex(ValueError, 'unique paragraph'):
            self.run_fixture(*self.fixture(missing=True))


if __name__ == '__main__':
    unittest.main()
