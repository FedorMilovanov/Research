"""Conditional pastoral claims and standalone doctrine coverage,not medical tests."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from audit_charnock_childbearing import ROOT,HEADING,extract,check_review
from audit_charnock_series_plan import check

class ChildbearingContractTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['childbearingReview']

    def rejected(self):
        with self.assertRaises(ValueError):check_review(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_review(self.plan,self.registry)['newChildbearingParagraphs'],84)

    def test_not_clinical_guarantee(self):
        self.review['clinicalOutcomeGuaranteed']=True;self.rejected()

    def test_not_individual_blame_approval(self):
        self.review['individualBlameInferenceApproved']=True;self.rejected()

    def test_not_critical_edition(self):
        self.review['criticalEditionVerified']=True;self.rejected()

    def test_not_publication_approval(self):
        self.review['publicationApproval']=True;self.rejected()

    def test_standalone_doctrine_cannot_disappear(self):
        self.review['layout']['standaloneDoctrineBlocks']=[];self.rejected()

    def test_standalone_authorial_role_not_foreign_quote(self):
        self.review['layout']['standaloneDoctrineBlocks'][0]['role']='FOREIGN_QUOTATION';self.rejected()

    def test_old_paragraphs_not_counted_as_new(self):
        self.review['newParagraphCount']=88;self.rejected()

    def test_nested_polemic_not_unqualified_fact(self):
        next(o for o in self.review['observations'] if o['id']=='NESTED_POLEMIC')['probeRole']='AUTHOR_THESIS';self.rejected()

    def test_nonabsolute_qualification_not_removed(self):
        self.review['observations']=[o for o in self.review['observations'] if o['id']!='NONABSOLUTE'];self.rejected()

    def test_strong_reproach_not_sanitized_away(self):
        self.review['observations']=[o for o in self.review['observations'] if o['id']!='FAITH_REPROACH'];self.rejected()

    def test_citation_not_independent_replay(self):
        self.review['marginalNoteDecisions'][2]['citedWorkIndependentlyReplayed']=True;self.rejected()

    def test_marginal_note_page_is_not_parent_start_page(self):
        self.review['byteVerifiedMarginalNotes'][2]['startTeiPage']='76';self.rejected()

    def test_printed_pair_not_preaching_chronology(self):
        self.review['printedPairChronologyEstablished']=True;self.rejected()

    def test_prior_conclusion_exact_overlap(self):
        p=self.review['byteVerifiedContexts']['TXT-20']['contextWindow'][-1]
        p['text']+=' altered';p['textSha256']=hashlib.sha256(p['text'].encode()).hexdigest()
        self.review['layout']['paragraphManifest'][-1]['textSha256']=p['textSha256'];self.rejected()

    def test_root_checks_supplemental_axes(self):
        self.review['limitedRelations'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)


class ChildbearingExtractionTests(unittest.TestCase):
    def fixture(self,unknown=False):
        before='<div><head>Earlier discourse</head>'+''.join('<p>Before '+str(i)+'</p>' for i in range(403))+'</div>'
        body=[]
        for i in range(404,491):
            text='Unique childbearing anchor' if i==413 else 'Body '+str(i)
            note='<note place="margin">Fixture citation</note>' if i==409 else ''
            body.append('<p>'+text+note+'</p>')
            if i==429:body.append('<q>Doct. The continuance of the punishment:fixture.</q>')
        discourse='<div><head>'+HEADING+'</head><epigraph><p>Fixture epigraph</p></epigraph>'+''.join(body)+('<argument>Unsupported main text</argument>' if unknown else '')+'</div>'
        after='<div><head>A DISCOURSE OF THE Sins of the Regenerate.</head>'+''.join('<p>Successor '+str(i)+'</p>' for i in range(491,518))+'</div>'
        raw=('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><pb n="77"/>'+before+discourse+after+'</body></text></TEI>').encode()
        return raw,dict(anchors=[dict(id='TXT-20',source='A32724',probe='Unique childbearing anchor',teiPages=['77'])],sources={'A32724':dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())})

    def replay(self,raw,registry):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'A32724.xml').write_bytes(raw)
            return extract(root,registry)

    def test_paragraphs_and_standalone_doctrine_are_separate(self):
        x=self.replay(*self.fixture())
        self.assertEqual(len(x['layout']['paragraphManifest']),88)
        self.assertEqual(x['layout']['directBodyParagraphs'],87)
        q=x['layout']['standaloneDoctrineBlocks'][0]
        self.assertEqual((q['afterParagraphIndexZeroBased'],q['beforeParagraphIndexZeroBased']),(429,430))
        self.assertEqual(x['marginalNotes'][0]['parentParagraphIndexZeroBased'],409)
        self.assertEqual(x['layout']['nextDiscourseHeading'],'A DISCOURSE OF THE Sins of the Regenerate.')

    def test_pin_required(self):
        raw,registry=self.fixture()
        with self.assertRaisesRegex(ValueError,'byte pin'):self.replay(raw+b' ',registry)

    def test_unknown_main_text_not_silently_dropped(self):
        with self.assertRaisesRegex(ValueError,'Unaccounted'):self.replay(*self.fixture(unknown=True))


if __name__=='__main__':unittest.main()
