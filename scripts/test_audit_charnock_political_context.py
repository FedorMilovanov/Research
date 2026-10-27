"""Political norm/biography separation and source-byte replay tests."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from audit_charnock_political_context import ROOT, PROBES, PAIRS, extract, check_review
from audit_charnock_series_plan import check

class PoliticalContextTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['politicalContextReview']

    def rejects(self):
        with self.assertRaises(ValueError):check_review(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_review(self.plan,self.registry)['biographicalWordingComparisons'],3)

    def test_no_implementation_claim(self):
        self.review['implementationVerified']=True;self.rejects()

    def test_no_independent_witness_claim(self):
        self.review['independentWitnessesEstablished']=True;self.rejects()

    def test_no_publication_approval(self):
        self.review['publicationApproval']=True;self.rejects()

    def test_no_proven_dependency_direction(self):
        self.review['wordingComparisons'][0]['dependencyDirectionProven']=True;self.rejects()

    def test_norm_not_personal_case(self):
        self.review['normCards'][0]['applicationState']='CHARNOCK_PAID';self.rejects()

    def test_full_context_integrity(self):
        self.review['byteVerifiedContexts']['XXXVII']['text']+=' all religions';self.rejects()

    def test_nested_voice(self):
        self.review['woodMedicalVoice']='WOOD_PERSONAL_ATTESTATION';self.rejects()

    def test_exact_wording_required(self):
        self.review['wordingComparisons'][1]['woodProbe']='medical graduate';self.rejects()

    def test_root_checks_axes(self):
        self.review['normCards'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)

class PoliticalExtractionTests(unittest.TestCase):
    def fixture(self):
        sources={}
        for source in {s for s,_ in PROBES.values()}:
            title='';paragraphs=[]
            for key,(s,probe) in PROBES.items():
                if s!=source:continue
                if key=='TITLE':title='<div type="title_page">'+probe+'</div>'
                else:
                    extra=' '.join(pair[0 if key=='ADAMS_VEAL' else 1] for pair in PAIRS.values()) if key in {'ADAMS_VEAL','WOOD'} else ''
                    paragraphs.append('<p>'+probe+' '+extra+'</p>')
            sources[source]=('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><front>'+title+'</front><body><pb n="17"/>'+''.join(paragraphs)+'</body></text></TEI>').encode()
        return sources,{'sources':{s:dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for s,raw in sources.items()}}

    def replay(self,sources,registry):
        with tempfile.TemporaryDirectory() as directory:
            for s,raw in sources.items():(Path(directory)/(s+'.xml')).write_bytes(raw)
            return extract(Path(directory),registry)

    def test_seven_contexts(self):
        result=self.replay(*self.fixture());self.assertEqual(len(result),7)
        self.assertEqual(result['XXXVIII']['probeTeiPages'],['17'])

    def test_byte_pin(self):
        sources,registry=self.fixture();sources['A41722']+=b' '
        with self.assertRaisesRegex(ValueError,'byte pin'):self.replay(sources,registry)

    def test_duplicate_norm(self):
        sources,registry=self.fixture();sources['A41722']=sources['A41722'].replace(b'</body>',('<p>'+PROBES['XXXVIII'][1]+'</p></body>').encode());raw=sources['A41722'];registry['sources']['A41722']=dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        with self.assertRaisesRegex(ValueError,'Unique political'):self.replay(sources,registry)

if __name__=='__main__':unittest.main()
