"""Guard the explicit backreference, qualified collation and unresolved identities."""
import json
import unittest
from audit_charnock_copyist_transmission import ROOT,KEY,FALSE_FLAGS,check_review


class CopyistTransmissionTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan[KEY];self.data=self.review['byteVerifiedReading']

    def check(self):return check_review(self.plan,self.registry)
    def rejects(self):
        with self.assertRaises(ValueError):self.check()

    def test_two_accounts_not_independent_proof(self):
        self.assertEqual(self.check()['copyistEditorialAccountsCompared'],2)
        self.assertFalse(self.check()['copyistAutographsVerified'])

    def test_no_unproved_upgrades(self):
        for key in FALSE_FLAGS:
            with self.subTest(key=key):
                self.review[key]=True;self.rejects();self.review[key]=False

    def test_first_volume_pin(self):
        self.data['firstVolume']['sourceSha256']='0'*64;self.rejects()

    def test_later_volume_pin(self):
        self.data['laterVolume']['sourceSha256']='0'*64;self.rejects()

    def test_no_expanded_initials(self):
        self.data['firstVolume']['copyistMargin']['noteText']='John Wichens and William Ashton';self.rejects()

    def test_date_is_editorial_not_sermon(self):
        self.data['laterVolume']['datelines']=['1680'];self.rejects()

    def test_veel_not_charnock_signature(self):
        self.data['laterVolume']['signatures']=['Stephen Charnock'];self.rejects()

    def test_complete_editorial_context(self):
        self.data['laterVolume']['paragraphs'].pop();self.rejects()

    def test_printed_for_not_printer(self):
        self.data['laterVolume']['titlePage']=self.data['laterVolume']['titlePage'].replace('Printed for','Printed by');self.rejects()

    def test_exact_spans_not_paraphrases(self):
        self.review['observations'][0]['spans'][0]['text']='Ashton independently identified';self.rejects()

    def test_nine_distinct_decisions(self):
        self.review['observations'].pop();self.rejects()

    def test_context_is_not_publication_approval(self):
        self.review['evidenceClass']='A1';self.rejects()

    def test_transmission_chapter_ownership(self):
        self.plan['documents'][5]['supplementaryContextReadings'].remove(KEY);self.rejects()

    def test_explicit_backreference_not_surname_alone(self):
        self.review['explicitFirstVolumeBackreferenceLocated']=False;self.rejects()


if __name__=='__main__':unittest.main()
