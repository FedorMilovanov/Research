"""Integrity and fail-closed tests;not independent linguistic review."""
import copy
import json
from pathlib import Path
import unittest
from audit_charnock_editorial_translations import check_review

ROOT = Path(__file__).resolve().parents[1]


class EditorialTranslationTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT / 'data/charnock-biographical-anchors-v1.json').read_text())
        self.review = self.plan['editorialTranslationReview']
        self.row = self.review['items'][0]

    def check(self):
        return check_review(self.plan,self.registry)

    def test_saved_three_drafts_nine_terms(self):
        self.assertEqual(self.check(),dict(editorialWorkingTranslationDrafts=3,editorialTranslationTermDecisions=9))

    def test_source_pin(self):
        self.review['sourceReplay']['sourceSha256']='0'*64
        with self.assertRaises(ValueError): self.check()

    def test_context_not_truncated(self):
        self.row['quoteText'] = self.row['quoteText'][:80]
        with self.assertRaises(ValueError): self.check()

    def test_not_authorial_voice(self):
        self.row['voice']='CHARNOCK_BODY'
        with self.assertRaises(ValueError): self.check()

    def test_historical_row_bound(self):
        self.row['canonicalRowSha256']='0'*64
        with self.assertRaises(ValueError): self.check()

    def test_translation_hash(self):
        self.row['russianDraft']+=' Другой текст.'
        with self.assertRaises(ValueError): self.check()

    def test_no_invented_reviewer(self):
        self.row['independentReview']['reviewer']='AI self-review'
        with self.assertRaises(ValueError): self.check()

    def test_no_approval(self):
        self.row['publicationApproval']=True
        with self.assertRaises(ValueError): self.check()

    def test_no_image_waiver(self):
        self.review['licence']['scope']='ALL_IMAGES'
        with self.assertRaises(ValueError): self.check()

    def test_no_printed_page_invention(self):
        self.row['quoteTeiPages']=['3']
        with self.assertRaises(ValueError): self.check()

    def test_term_must_match_actual_text(self):
        self.row['termDecisions'][0]['russianRendering']='несуществующее соответствие'
        with self.assertRaises(ValueError): self.check()

    def test_no_hold_clearance(self):
        self.row['holds']=[]
        with self.assertRaises(ValueError): self.check()

    def test_no_ed06_closure(self):
        next(t for t in self.plan['tasks'] if t['id']=='ED-06')['status']='DONE'
        with self.assertRaises(ValueError): self.check()

    def test_read_only(self):
        before=copy.deepcopy((self.plan,self.registry))
        self.check()
        self.assertEqual(before,(self.plan,self.registry))



class AuthorialTranslationTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/'data/charnock-biographical-anchors-v1.json').read_text())
        self.review=self.plan['authorialTranslationReview']
        self.row=self.review['items'][0]

    def check(self):
        from audit_charnock_editorial_translations import check_authorial_review
        return check_authorial_review(self.plan,self.registry)

    def test_two_saved_authorial_drafts(self):
        self.assertEqual(self.check(),dict(authorialWorkingTranslationDrafts=2,authorialTranslationTermDecisions=6))

    def test_opening_not_whole_paragraph(self):
        self.row['fullParagraphTranslated']=True
        with self.assertRaises(ValueError):self.check()

    def test_no_sanitized_context_claim(self):
        self.review['omittedPolemicRetainedInContext']=False
        with self.assertRaises(ValueError):self.check()

    def test_full_creation_paragraph_required(self):
        self.review['items'][1]['quoteText']='The Creation was a real change'
        with self.assertRaises(ValueError):self.check()

    def test_no_editorial_voice(self):
        self.row['voice']='VEEL_ADAMS_EDITORIAL'
        with self.assertRaises(ValueError):self.check()

    def test_source_context_pin(self):
        self.row['contextSha256']='0'*64
        with self.assertRaises(ValueError):self.check()

    def test_translation_integrity(self):
        self.row['russianDraft']+=' Новый смысл.'
        with self.assertRaises(ValueError):self.check()

    def test_no_independent_review_invented(self):
        self.row['independentReview']['state']='VERIFIED'
        with self.assertRaises(ValueError):self.check()

    def test_no_rights_promotion(self):
        self.row['rightsState']='PUBLICATION_ELIGIBLE'
        with self.assertRaises(ValueError):self.check()

    def test_no_licence_scope_expansion(self):
        self.review['licences']['A32724']['scope']='IMAGES_TOO'
        with self.assertRaises(ValueError):self.check()

    def test_term_must_match(self):
        self.row['termDecisions'][0]['englishSpan']='all Scripture is uncertain'
        with self.assertRaises(ValueError):self.check()

    def test_read_only(self):
        before=copy.deepcopy((self.plan,self.registry))
        self.check()
        self.assertEqual(before,(self.plan,self.registry))



class AtheismTranslationTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/'data/charnock-biographical-anchors-v1.json').read_text())
        self.r=self.plan['atheismReview']

    def check(self):
        from audit_charnock_editorial_translations import check_atheism_review
        return check_atheism_review(self.plan,self.registry)

    def test_bounded_seven_paragraphs_one_translation(self):
        self.assertEqual(self.check(),dict(atheismContextParagraphs=7,atheismWorkingTranslationDrafts=1,atheismObservations=7))

    def test_not_whole_discourse(self):
        self.r['wholeDiscourseRead']=True
        with self.assertRaises(ValueError):self.check()

    def test_no_modern_verdict(self):
        self.r['modernCollectiveVerdictApproved']=True
        with self.assertRaises(ValueError):self.check()

    def test_full_selected_paragraph(self):
        self.r['translation']['quoteText']='Men may have Atheistical hearts without Atheistical heads.'
        with self.assertRaises(ValueError):self.check()

    def test_job_note_not_replaced(self):
        self.r['marginalNotes'][0]['text']='Job. 2.5.'
        with self.assertRaises(ValueError):self.check()

    def test_script_gap_not_reconstructed(self):
        self.r['marginalNotes'][1]['text']='reconstructed Hebrew'
        with self.assertRaises(ValueError):self.check()

    def test_no_automatic_review(self):
        self.r['translation']['independentReview']['state']='REVIEWED'
        with self.assertRaises(ValueError):self.check()

    def test_no_hold_clearance(self):
        self.r['translation']['holds']=[]
        with self.assertRaises(ValueError):self.check()

    def test_no_ungrounded_observation(self):
        self.r['observations'][1]['englishSpan']='No one ever doubts'
        with self.assertRaises(ValueError):self.check()

    def test_translation_integrity(self):
        self.r['translation']['russianDraft']+=' Все люди таковы.'
        with self.assertRaises(ValueError):self.check()

    def test_read_only(self):
        before=copy.deepcopy((self.plan,self.registry))
        self.check()
        self.assertEqual(before,(self.plan,self.registry))



class EnmityTranslationTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/'data/charnock-biographical-anchors-v1.json').read_text())
        self.r=self.plan['enmityReview']

    def check(self):
        from audit_charnock_editorial_translations import check_enmity_review
        return check_enmity_review(self.plan,self.registry)

    def test_saved_reading(self):
        self.assertEqual(self.check(),dict(enmityBodyParagraphs=34,enmityEditorialParagraphs=4,enmityObservations=10,enmityWorkingTranslationDrafts=2))

    def test_no_date_or_autograph_promotion(self):
        for key in ['preachingDateEstablished','autographsVerified','wholeDiscourseRead']:
            with self.subTest(key=key):
                self.r[key]=True
                with self.assertRaises(ValueError):self.check()
                self.r[key]=False

    def test_editor_not_charnock(self):
        self.r['translations'][1]['voice']='CHARNOCK_BODY'
        with self.assertRaises(ValueError):self.check()

    def test_not_all_editorial_paragraph_translated(self):
        self.r['translations'][1]['fullParagraphTranslated']=True
        with self.assertRaises(ValueError):self.check()

    def test_body_complete_not_short_candidate(self):
        self.r['translations'][0]['quoteText']='not created, but corrupted Nature'
        with self.assertRaises(ValueError):self.check()

    def test_no_false_independent_review(self):
        self.r['translations'][0]['independentReview']['reviewer']='imagined reviewer'
        with self.assertRaises(ValueError):self.check()

    def test_translation_hash(self):
        self.r['translations'][1]['russianDraft']+=' Точная дата установлена.'
        with self.assertRaises(ValueError):self.check()

    def test_no_hold_clearance(self):
        self.r['observations'][0]['holds']=[]
        with self.assertRaises(ValueError):self.check()

    def test_observation_requires_actual_span(self):
        self.r['observations'][2]['englishSpan']='God created sin'
        with self.assertRaises(ValueError):self.check()

    def test_read_only(self):
        before=copy.deepcopy((self.plan,self.registry))
        self.check()
        self.assertEqual(before,(self.plan,self.registry))


if __name__=='__main__':
    unittest.main()
