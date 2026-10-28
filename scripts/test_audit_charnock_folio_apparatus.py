"""Scope, attribution and note anchoring regressions, not historical witnesses."""
import json
import unittest
import xml.etree.ElementTree as ET
from audit_charnock_folio_apparatus import ROOT, KEY, FALSE_FLAGS, check_review, anchor_before, NS


class FolioApparatusTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan[KEY]
        self.data=self.review['byteVerifiedReading']

    def check(self):
        return check_review(self.plan,self.registry)

    def rejects(self):
        with self.assertRaises(ValueError):self.check()

    def test_exact_scope_reconciliation(self):
        self.assertEqual(self.check()['folioTextMarginalNotes'],2343)
        self.assertEqual(self.check()['folioDiscourseMarginalNotes'],2337)

    def test_counts_are_not_interchangeable(self):
        for key in ['allXmlNoteElements','metadataNoteElements','textNoteElements','textMarginalNotes','discourseNoteElements','discourseCount']:
            with self.subTest(key=key):
                self.data[key]+=1
                self.rejects()
                self.data[key]-=1

    def test_all_inferences_remain_unproved(self):
        for key in FALSE_FLAGS:
            with self.subTest(key=key):
                self.review[key]=True;self.rejects();self.review[key]=False

    def test_source_pin(self):
        self.data['sourceSha256']='0'*64;self.rejects()

    def test_no_missing_front_note(self):
        self.data['editorialFrontMarginalNotes'].pop();self.rejects()

    def test_editorial_voice_not_charnock_body(self):
        self.data['editorialFrontMarginalNotes'][0]['divisionType']='discourse';self.rejects()

    def test_no_guessed_name_expansion(self):
        self.data['editorialFrontMarginalNotes'][0]['noteText']='John Wichens and William Ashton';self.rejects()

    def test_no_invented_printed_page(self):
        self.data['editorialFrontMarginalNotes'][0]['teiPage']='1';self.rejects()

    def test_note_anchored_to_transcription_not_generic_praise(self):
        self.data['editorialFrontMarginalNotes'][0]['precedingBodyText']='our Authour';self.rejects()

    def test_parent_full_context_hash(self):
        self.data['editorialFrontMarginalNotes'][0]['paragraphSha256']='0'*64;self.rejects()

    def test_not_quote_safe_by_counting(self):
        self.review['evidenceClass']='A1';self.rejects()

    def test_printed_transmission_integration(self):
        self.plan['documents'][5]['supplementaryContextReadings'].remove(KEY);self.rejects()

    def test_anchor_excludes_note_bodies_but_retains_tails(self):
        p=ET.fromstring(f'<p xmlns="{NS[1:-1]}">Before <note>not body</note>copyists<note place="margin">Names</note> after</p>')
        notes=p.findall(NS+'note')
        self.assertEqual(anchor_before(p,notes[1]),'Before copyists')
        other=ET.Element(NS+'note')
        with self.assertRaises(ValueError):anchor_before(p,other)


if __name__=='__main__':unittest.main()
