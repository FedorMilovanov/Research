"""Full main-text layout and limits for one mourning discourse."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from audit_charnock_mourning import ROOT,HEADING,extract,check_review
from audit_charnock_series_plan import check

class MourningCompleteTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['mourningCompleteReview']

    def rejected(self):
        with self.assertRaises(ValueError):check_review(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_review(self.plan,self.registry)['mourningMainTextParagraphsCovered'],71)

    def test_no_dated_occasion(self):
        self.review['datedOccasionEstablished']=True;self.rejected()

    def test_not_critical_edition(self):
        self.review['criticalEditionVerified']=True;self.rejected()

    def test_no_collective_blame_approval(self):
        self.review['modernCollectiveBlameApproved']=True;self.rejected()

    def test_no_publication_approval(self):
        self.review['publicationApproval']=True;self.rejected()

    def test_old_paragraphs_not_new(self):
        self.review['newParagraphCount']=71;self.rejected()

    def test_coverage_cannot_skip(self):
        self.review['byteVerifiedContexts']['closing']['contextWindow'].pop();self.rejected()

    def test_standalone_doctrine_not_omitted(self):
        self.review['layout']['standaloneBlocks'].pop(0);self.rejected()

    def test_standalone_outline_not_omitted(self):
        self.review['layout']['standaloneBlocks'].pop();self.rejected()

    def test_no_forged_extra_branch(self):
        e=self.review['layout']['standaloneBlocks'][1]
        e['text']=e['text'].replace('2. A Duty acceptable to God.','Removed branch')
        e['textSha256']=hashlib.sha256(e['text'].encode()).hexdigest();self.rejected()

    def test_explanatory_note_not_independent_author(self):
        self.review['marginalNoteDecisions'][6]['noteKind']='SOURCE_POINTER';self.rejected()

    def test_note_not_foreign_work_replay(self):
        self.review['marginalNoteDecisions'][4]['citedWorkIndependentlyReplayed']=True;self.rejected()

    def test_probable_not_established_history(self):
        next(o for o in self.review['observations'] if o['id']=='BAPTIST')['probeRole']='AUTHOR_FACT';self.rejected()

    def test_prior_checkpoint_link_preserved(self):
        self.plan['mourningDistinctionReview'].pop('mainTextCoverageFollowUp');self.rejected()

    def test_next_discourse_boundary(self):
        self.review['layout']['nextDiscourseHeading']=HEADING;self.rejected()

    def test_root_checks_new_axes(self):
        self.review['observations'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)

class MourningLayoutTests(unittest.TestCase):
    def fixture(self,unknown=False):
        before='<div><head>Earlier</head>'+''.join('<p>Before '+str(i)+'</p>' for i in range(332))+'</div>'
        body=[]
        for i in range(333,403):
            text='Unique mourning anchor' if i==334 else 'Body '+str(i)
            note='<note>Fixture source</note>' if i==345 else ''
            body.append('<p>'+text+note+'</p>')
            if i==357:body.append('<q>Doct. Lamenting the sins:fixture</q>')
            if i==358:body.append('<list><item>1. First</item><item>2. Second</item><item>3. Third</item></list>')
        main='<div><head>'+HEADING+'</head><epigraph><p>Epigraph</p></epigraph>'+''.join(body)+('<argument>Unknown</argument>' if unknown else '')+'</div>'
        next_text='<div><head>A DISCOURSE FOR The Comfort of Child-bearing Women.</head><p>Next</p></div>'
        raw=('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><pb n="64"/>'+before+main+next_text+'</body></text></TEI>').encode()
        return raw,dict(anchors=[dict(id='TXT-03',source='A32724',probe='Unique mourning anchor',teiPages=['64'])],sources={'A32724':dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())})

    def replay(self,raw,registry):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'A32724.xml').write_bytes(raw)
            return extract(root,registry)

    def test_full_layout_includes_q_and_list(self):
        x=self.replay(*self.fixture());layout=x['layout']
        self.assertEqual(len(layout['paragraphManifest']),71)
        self.assertEqual(layout['directBodyParagraphs'],70)
        self.assertEqual([e['elementTag'] for e in layout['standaloneBlocks']],['q','list'])
        self.assertEqual(layout['nextDiscourseParagraphIndex'],403)
        self.assertEqual(x['marginalNotes'][0]['parentParagraphIndexZeroBased'],345)

    def test_pin_required(self):
        raw,registry=self.fixture()
        with self.assertRaisesRegex(ValueError,'byte pin'):self.replay(raw+b' ',registry)

    def test_unknown_main_text_not_dropped(self):
        with self.assertRaisesRegex(ValueError,'Unaccounted'):self.replay(*self.fixture(unknown=True))

if __name__=='__main__':unittest.main()
