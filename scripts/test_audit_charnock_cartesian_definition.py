"""Regression guards: a translation and a later Latin quote are not the original."""
import hashlib
import json
import unittest
from unittest.mock import patch
from audit_charnock_cartesian_definition import ROOT, KEY, PINS, FALSE_FLAGS, check_review, verified_bytes


class CartesianDefinitionTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan[KEY]
        self.data=self.review['byteVerifiedReading']

    def check(self):
        return check_review(self.plan,self.registry)

    def rejects(self):
        with self.assertRaises(ValueError):
            self.check()

    def test_bounded_comparison(self):
        self.assertEqual(self.check()['cartesianComparativeObservations'],12)
        self.assertFalse(self.check()['descartesLatinOriginalVerified'])

    def test_no_original_dependence_or_publication_inference(self):
        for key in FALSE_FLAGS:
            with self.subTest(key=key):
                self.review[key]=True
                self.rejects()
                self.review[key]=False

    def test_no_pin_marker_without_actual_match(self):
        self.review['sources']['PG4391']['sha256']='0'*64
        self.rejects()

    def test_separate_source_rights(self):
        self.review['sources']['A52424']['rightsState']='PUBLICATION_ELIGIBLE'
        self.rejects()

    def test_context_is_not_quote_safe(self):
        self.review['evidenceClass']='A1'
        self.rejects()
        self.review['evidenceClass']='C'
        self.review['rejectedLatinCandidates'][0]['evidenceClass']='A1'
        self.rejects()

    def test_charnock_text_matches_historical_reading(self):
        self.data['charnockParagraphs'][0]['text']='Charnock simply accepts Descartes'
        self.rejects()

    def test_damaged_note_not_silently_repaired(self):
        self.data['charnockMarginalNote'][0]='Cartes. Princip. Philos. Part 1. Sect. 9.'
        self.rejects()

    def test_norris_not_astell_speaker(self):
        self.data['norrisLetterVI']['signed']=['Mary Astell']
        self.rejects()

    def test_no_calendar_normalization(self):
        self.data['norrisLetterVI']['dateline']=['11 January 1694']
        self.rejects()

    def test_complete_letter_not_complete_book(self):
        self.data['norrisLetterVI']['paragraphs'].pop()
        self.rejects()

    def test_text_license_not_metadata_guess(self):
        self.data['norrisLetterVI']['textLicenseVerified']=False
        self.rejects()

    def test_pg_text_hash(self):
        self.data['veitchSectionsVIIItoX']['text']+=' invented'
        self.rejects()

    def test_actual_span_not_paraphrase(self):
        self.review['observations'][0]['spans'][0]['text']='invented quote'
        self.rejects()

    def test_twelve_distinct_observations(self):
        self.review['observations'].pop()
        self.rejects()

    def test_search_history_not_retroactively_promoted(self):
        self.plan['thoughtsOpeningReview']['cartesianCounterpartSearch']['accessState']='FULL_OBJECT_VERIFIED'
        self.rejects()

    def test_part_vii_integration(self):
        self.plan['documents'][7]['supplementaryContextReadings'].remove(KEY)
        self.rejects()

    def test_byte_and_git_blob_guard_independent_of_sha256(self):
        raw=b'fixture'
        fake=dict(PINS['PG4391'],size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),blob='0'*40)
        with patch.dict(PINS,PG4391=fake), patch('pathlib.Path.read_bytes',return_value=raw):
            with self.assertRaisesRegex(ValueError,'blob pin'):
                verified_bytes(ROOT,'PG4391')


if __name__=='__main__':
    unittest.main()
