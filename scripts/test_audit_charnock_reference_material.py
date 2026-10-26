"""Fail-closed reference selection and synthetic XML replay tests."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from audit_charnock_reference_material import ROOT, TERMS, check_review, extract
from audit_charnock_series_plan import check


class ReferenceMaterialTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry = json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review = self.plan['referenceMaterialReview']

    def test_current_contract(self):
        self.assertEqual(check_review(self.plan,self.registry)['contextualGlosses'],10)

    def rejected(self):
        with self.assertRaises(ValueError):
            check_review(self.plan,self.registry)

    def test_no_chapter_claim(self):
        self.review['readerChapterWritten'] = True
        self.rejected()

    def test_no_dictionary_certification(self):
        self.review['dictionaryVerificationClaimed'] = True
        self.rejected()

    def test_no_publication_approval(self):
        self.review['publicationApproval'] = True
        self.rejected()

    def test_approximate_chronology_retained(self):
        self.review['chronologySelection'][0]['safeFormulation'] = 'Born exactly in 1628.'
        self.rejected()

    def test_acquaintance_not_conversion_day(self):
        next(c for c in self.review['chronologySelection'] if c['coreId']=='BCD-06')['dateMeaning']='EXACT_CONVERSION_DATE'
        self.rejected()

    def test_family_not_acquired(self):
        next(b for b in self.review['bibliographicSelection'] if b['unitType']!='PRINTED_OBJECT')['readerAccessLabel']='TCP_TRANSCRIPTION_NOT_IMAGES'
        self.rejected()

    def test_gloss_context_hash(self):
        next(iter(self.review['byteVerifiedGlossContexts']['contexts'].values()))['text']+=' fabricated'
        self.rejected()

    def test_medical_attribution(self):
        next(g for g in self.review['contextualGlosses'] if g['id']=='PHYSICK')['sourceRole']='WOOD_MEDICAL_CERTIFICATION'
        self.rejected()

    def test_gloss_review_not_independent(self):
        self.review['contextualGlosses'][0]['glossState']='INDEPENDENTLY_REVIEWED'
        self.rejected()

    def test_root_checks_new_axes(self):
        self.review['contextualGlosses'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):
            check(self.plan)

    def test_history_required(self):
        next(d for d in self.plan['documents'] if d['id']=='REFERENCE')['remainingWorkHistory']=[]
        self.rejected()


class ReferenceExtractionTests(unittest.TestCase):
    def fixture(self):
        sources={}
        for source_id in {t[0] for t in TERMS.values()}:
            front=[];body=[]
            if source_id=='A32723':
                front=['<div type="to_the_reader">'+''.join('<p>'+ ' '.join(t[3] for t in TERMS.values() if t[0]==source_id and t[2]==i)+'</p>' for i in range(5))+'</div>']
            elif source_id=='A46911':
                front=['<div type="title_page">'+TERMS['DIVINE'][3]+'</div>']
            else:
                body=['<pb n="17"/><p>'+ ' '.join(t[3] for t in TERMS.values() if t[0]==source_id)+'</p>']
            sources[source_id]=('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><front>'+''.join(front)+'</front><body>'+''.join(body)+'</body></text></TEI>').encode()
        registry={'sources':{k:dict(size=len(v),sha256=hashlib.sha256(v).hexdigest()) for k,v in sources.items()}}
        return sources,registry

    def replay(self,sources,registry):
        with tempfile.TemporaryDirectory() as directory:
            for k,v in sources.items():
                (Path(directory)/(k+'.xml')).write_bytes(v)
            return extract(Path(directory),registry)

    def test_deduplicated_contexts(self):
        evidence=self.replay(*self.fixture())
        self.assertEqual(len(evidence['contexts']),7)
        self.assertEqual(len(evidence['usages']),10)
        self.assertEqual(evidence['usages']['CONVERSATION']['probeTeiPages'],['17'])

    def test_source_pin_mismatch(self):
        sources,registry=self.fixture();sources['A46911']+=b' '
        with self.assertRaisesRegex(ValueError,'byte pin'):
            self.replay(sources,registry)

    def test_duplicate_title_probe(self):
        sources,registry=self.fixture();sources['A46911']=sources['A46911'].replace(b'</body>',('<p>'+TERMS['DIVINE'][3]+'</p></body>').encode())
        registry['sources']['A46911']=dict(size=len(sources['A46911']),sha256=hashlib.sha256(sources['A46911']).hexdigest())
        with self.assertRaisesRegex(ValueError,'literal and unique'):
            self.replay(sources,registry)


if __name__=='__main__':
    unittest.main()
