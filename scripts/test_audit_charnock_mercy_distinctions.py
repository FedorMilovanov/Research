import copy
import json
import unittest
from audit_charnock_mercy_distinctions import ROOT, KEY, FALSE_FLAGS, check_review
from audit_charnock_thoughts import digest


class MercyDistinctionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        cls.registry=json.loads((ROOT/cls.plan['baselineRegistry']).read_text())

    def setUp(self):
        self.p=copy.deepcopy(self.plan);self.r=self.p[KEY];self.d=self.r['byteVerifiedReading']

    def fails(self):
        with self.assertRaises(ValueError):check_review(self.p,self.registry)

    def test_baseline(self):
        result=check_review(self.p,self.registry)
        self.assertEqual(result['mercyAdditionalSelectedParagraphs'],38)
        self.assertEqual(result['mercyFinalCautionParagraphs'],16)

    def test_false_claim_flags(self):
        for flag in FALSE_FLAGS:
            with self.subTest(flag=flag):
                self.r[flag]=True;self.fails();self.r[flag]=False

    def test_wrong_source_pin(self):
        self.d['sourceSha256']='0'*64;self.fails()

    def test_wrong_sermon(self):
        self.d['heading']='Discourse of Enmity';self.fails()

    def test_caution_not_complete(self):
        self.d['cautionParagraphIndices'].pop();self.fails()

    def test_not_continuous_reading(self):
        self.d['paragraphs'][29]['paragraphIndexZeroBased']=712;self.fails()

    def test_historical_seven_not_newly_rewritten(self):
        row=self.d['paragraphs'][3];row['text']+=' changed';row['textSha256']=digest(row['text']);self.fails()

    def test_text_hash(self):
        self.d['paragraphs'][12]['text']+=' changed';self.fails()

    def test_often_not_always(self):
        row=self.d['paragraphs'][1];row['text']=row['text'].replace('often','always');row['textSha256']=digest(row['text']);self.fails()

    def test_not_first_doctrine_transition(self):
        row=self.d['paragraphs'][2];row['text']=row['text'].replace('last','first');row['textSha256']=digest(row['text']);self.fails()

    def test_no_silent_saith_emendation(self):
        row=next(r for r in self.d['paragraphs'] if r['paragraphIndexZeroBased']==964)
        row['text']=row['text'].replace('saith in Christ','faith in Christ');row['textSha256']=digest(row['text']);self.fails()

    def test_unverified_jerome_note_retained(self):
        self.d['marginalNotes']=[];self.fails()

    def test_boundary_not_authorial_continuation(self):
        self.d['nextPublisherParagraph']['paragraphIndexZeroBased']=975;self.fails()

    def test_exact_observation_span(self):
        s=self.r['observations'][-2]['spans'][0];s['text']='Sin necessitates Grace';s['sha256']=digest(s['text']);self.fails()

    def test_all_observations(self):
        self.r['observations'].pop();self.fails()

    def test_no_publication_release(self):
        self.r['publicationState']='APPROVED';self.fails()

    def test_part_vii_navigation(self):
        self.p['documents'][7]['supplementaryContextReadings'].remove(KEY);self.fails()

    def test_typed_holds_preserved(self):
        self.r['holds']=[];self.fails()


class ElectionApplicationTests(unittest.TestCase):
    setUpClass=classmethod(MercyDistinctionTests.setUpClass.__func__)
    setUp=MercyDistinctionTests.setUp
    fails=MercyDistinctionTests.fails
    def cross(self):return self.r['electionApplicationCrossCheck']
    def test_bounded_distinction(self):
        self.assertEqual(check_review(self.p,self.registry)['electionApplicationCrossObservations'],7)
    def test_no_foreign_case_closure(self):
        self.cross()['foreignCaseClosed']=True;self.fails()
    def test_no_full_ordo(self):
        self.cross()['completeOrdoSalutisEstablished']=True;self.fails()
    def test_no_merit_before_election(self):
        self.cross()['repentanceMeritsElection']=True;self.fails()
    def test_no_human_arbitrary_rule(self):
        self.cross()['humanArbitraryRuleApproved']=True;self.fails()
    def test_preserve_inherited_daille(self):
        self.cross()['byteVerifiedContext']['existingDailleParagraph']['textSha256']='0'*64;self.fails()
    def test_source_pin(self):
        self.cross()['byteVerifiedContext']['sourceSha256']='0'*64;self.fails()
    def test_distinct_margin_notes(self):
        self.cross()['byteVerifiedContext']['marginalNotes'][0]['text']='Dalle in loc.';self.fails()
    def test_no_global_absence(self):
        self.cross()['counterpartSearchFollowUp']['globalAbsenceProven']=True;self.fails()
    def test_context_hash(self):
        self.cross()['byteVerifiedContext']['paragraphs'][1]['text']+=' changed';self.fails()
    def test_exact_qualified_claim(self):
        span=self.cross()['observations'][0]['spans'][0]
        span['text']='Faith causes eternal election';span['sha256']=digest(span['text']);self.fails()
    def test_part_iv_cross_reference(self):
        self.p['documents'][4]['supplementaryContextReadings'].remove(KEY);self.fails()


if __name__=='__main__':unittest.main()
