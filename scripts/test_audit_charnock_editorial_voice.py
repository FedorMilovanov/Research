"""Synthetic extraction and bounded editorial-voice contract tests."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from audit_charnock_editorial_voice import ROOT, PROBES, extract, check_review


class EditorialVoiceExtractionTests(unittest.TestCase):
    def fixture(self, signature=True, duplicate=False, missing=False):
        pref = '<div type="to_the_reader"><head>TO THE READER.</head>' + ''.join('<p>Fixture paragraph ' + str(i) + '.</p>' for i in range(5))
        pref += '<closer><signed>' + ('EDW. VEEL. RI. ADAMS.' if signature else 'Unknown') + '</signed></closer></div>'
        bodies = []
        for i,(key,probe) in enumerate(PROBES.items()):
            value = 'Missing' if missing and i == 1 else probe
            bodies.append('<div type="discourse"><head>Fixture discourse</head><pb n="' + str(260+i) + '"/><p>Before.</p><div type="section"><p>' + value + '</p></div></div>')
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><front>' + pref + (pref if duplicate else '') + '</front><body>' + ''.join(bodies) + '</body></text></TEI>').encode()
        return raw, dict(sources={'A32723':dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())})

    def run_fixture(self, raw, registry):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.xml'
            path.write_bytes(raw)
            return extract(path,registry)

    def test_five_preface_paragraphs_and_two_body_tests(self):
        data = self.run_fixture(*self.fixture())
        self.assertEqual(len(data['prefaceParagraphs']),5)
        self.assertEqual(set(data['authorContexts']),set(PROBES))

    def test_joint_signature_required(self):
        with self.assertRaisesRegex(ValueError,'joint signature'):
            self.run_fixture(*self.fixture(signature=False))

    def test_source_pin_required(self):
        raw,registry = self.fixture()
        with self.assertRaisesRegex(ValueError,'byte pin'):
            self.run_fixture(raw+b' ',registry)

    def test_duplicate_preface_rejected(self):
        with self.assertRaisesRegex(ValueError,'One explicit'):
            self.run_fixture(*self.fixture(duplicate=True))

    def test_missing_body_probe_rejected(self):
        with self.assertRaisesRegex(ValueError,'One authorial'):
            self.run_fixture(*self.fixture(missing=True))

    def test_nested_section_not_lost(self):
        data = self.run_fixture(*self.fixture())
        self.assertEqual(data['authorContexts']['VOICE-PATIENCE']['localDiscourseParagraphIndexZeroBased'],1)


class EditorialVoiceContractTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review = self.plan['editorialVoiceReview']

    def test_two_examples_do_not_measure_frequency(self):
        self.review['objectionFrequencyMeasured'] = True
        with self.assertRaisesRegex(ValueError,'objection frequency'):
            check_review(self.plan,self.registry)

    def test_reported_speech_not_autograph(self):
        self.review['reportedSpeech']['independentVerbatimWitness'] = True
        with self.assertRaisesRegex(ValueError,'Reported speech'):
            check_review(self.plan,self.registry)

    def test_fresh_english_not_publication_release(self):
        self.review['quotationFollowUps'][0]['publicationApproval'] = True
        with self.assertRaisesRegex(ValueError,'Fresh English context'):
            check_review(self.plan,self.registry)

    def test_editors_not_authorial_self_description(self):
        self.review['readingCards'][0]['voice'] = 'CHARNOCK_BODY'
        with self.assertRaisesRegex(ValueError,'self-description'):
            check_review(self.plan,self.registry)

    def test_translation_not_silently_prepared(self):
        self.review['quotationFollowUps'][0]['translationState'] = 'APPROVED'
        with self.assertRaisesRegex(ValueError,'Fresh English context'):
            check_review(self.plan,self.registry)

    def test_superseded_queue_not_erased(self):
        self.plan['documents'][2]['remainingWorkHistory'] = []
        with self.assertRaisesRegex(ValueError,'explicit history'):
            check_review(self.plan,self.registry)


if __name__ == '__main__':
    unittest.main()
