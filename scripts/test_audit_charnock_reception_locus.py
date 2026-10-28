import copy
import json
import unittest
from audit_charnock_reception_locus import ROOT,KEY,FLAGS,check_review,Paragraphs,words
from audit_charnock_thoughts import digest

class ReceptionLocusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        cls.registry=json.loads((ROOT/cls.plan['baselineRegistry']).read_text())
    def setUp(self):
        self.p=copy.deepcopy(self.plan);self.r=self.p[KEY]
    def fails(self):
        with self.assertRaises(ValueError):check_review(self.p,self.registry)
    def test_baseline(self):
        self.assertTrue(check_review(self.p,self.registry)['receptionREC01SourceLocated'])
    def test_flags(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):
                self.r[flag]=True;self.fails();self.r[flag]=False
    def test_wrong_source_pin(self):
        self.r['byteVerifiedSource']['sourceSha256']='0'*64;self.fails()
    def test_wrong_page(self):
        self.r['byteVerifiedSource']['paragraphs'][8]['startTeiPage']='400';self.fails()
    def test_context_not_omitted(self):
        self.r['byteVerifiedSource']['paragraphs'].pop();self.fails()
    def test_quote_not_paraphrase(self):
        self.r['comparison']['mirrorSentence']='Sin may be charged again';self.fails()
    def test_no_punctuation_identity_claim(self):
        self.r['comparison']['relation']='VERBATIM_IDENTICAL';self.fails()
    def test_mirror_pin(self):
        self.r['derivedWitness']['reading']['sha256']='0'*64;self.fails()
    def test_selected_mirror_not_empty(self):
        self.r['derivedWitness']['reading']['paragraphs']=[];self.fails()
    def test_text_hash(self):
        self.r['derivedWitness']['reading']['paragraphs'][0]['text']+=' changed';self.fails()
    def test_historical_row_retained(self):
        self.r['historicalUnlocatedRowRetained']=False;self.fails()
    def test_no_rights_promotion(self):
        self.r['rightsState']='CC0';self.fails()
    def test_holds(self):
        self.r['holds']=[];self.fails()
    def test_navigation(self):
        self.p['documents'][8]['supplementaryContextReadings'].remove(KEY);self.fails()
    def test_html_not_markdown_parser(self):
        p=Paragraphs();p.feed('<p><a href="x">Psa 103:12</a></p><p>East&nbsp;<i>and</i> West.</p>')
        self.assertEqual(p.rows,['Psa 103:12','East and West.'])
    def test_words_ignore_case_not_negation(self):
        self.assertEqual(words('East, West;'),words('east west'))
        self.assertNotEqual(words('never charged'),words('charged'))

class CondensedDominionTests(unittest.TestCase):
    setUpClass=classmethod(ReceptionLocusTests.setUpClass.__func__)
    setUp=ReceptionLocusTests.setUp
    fails=ReceptionLocusTests.fails

    def condensed(self):return self.r['condensedPassage']
    def test_all_six(self):
        self.assertEqual(check_review(self.p,self.registry)['receptionCondensedPointsLocated'],6)
    def test_no_verbatim_whole_claim(self):
        self.condensed()['verbatimWholePassage']=True;self.fails()
    def test_no_extra_reader(self):
        self.condensed()['newIndependentReader']=True;self.fails()
    def test_no_modern_astronomy_verification(self):
        self.condensed()['modernAstronomyVerified']=True;self.fails()
    def test_all_six_comparisons_required(self):
        self.condensed()['pointComparisons'].pop();self.fails()
    def test_correspondence_not_reordered(self):
        self.condensed()['pointComparisons'][0]['mirrorParagraph']=327;self.fails()
    def test_adams_not_charnock(self):
        self.condensed()['byteVerifiedReading']['followingMirrorAuthor']='Stephen Charnock.';self.fails()
    def test_no_silent_lie_repair(self):
        row=self.condensed()['byteVerifiedReading']['mirrorParagraphs'][3]
        row['text']=row['text'].replace('dominion lie rules','dominion He rules');row['textSha256']=digest(row['text']);self.fails()
    def test_condensed_attribution_retained(self):
        row=self.condensed()['byteVerifiedReading']['mirrorParagraphs'][-1]
        row['text']=row['text'].replace('Condensed from Charnock','Stephen Charnock');row['textSha256']=digest(row['text']);self.fails()
    def test_omission_must_be_absent(self):
        pair=self.condensed()['pointComparisons'][0]
        pair['omittedSourceSpan']=copy.deepcopy(pair['retainedSourceSpan']);self.fails()
    def test_retention_must_be_present(self):
        span=self.condensed()['pointComparisons'][4]['retainedMirrorSpan']
        span['text']='God is confined to heaven';span['sha256']=digest(span['text']);self.fails()
    def test_no_printed_collation_promotion(self):
        self.condensed()['printedEditionCollated']=True;self.fails()

class BiographicalPraiseTests(unittest.TestCase):
    setUpClass=classmethod(ReceptionLocusTests.setUpClass.__func__)
    setUp=ReceptionLocusTests.setUp
    fails=ReceptionLocusTests.fails
    def praise(self):return self.r['biographicalPraiseReview']
    def test_four_paragraphs_six_observations(self):
        self.assertEqual(check_review(self.p,self.registry)['biographicalPraiseObservations'],6)
    def test_no_print_verification(self):
        self.praise()['printedBiographyVerified']=True;self.fails()
    def test_no_metadata_authorship(self):
        self.praise()['mirrorMetadataAuthorshipAccepted']=True;self.fails()
    def test_no_independent_eyewitness(self):
        self.praise()['independentEyewitnessAdded']=True;self.fails()
    def test_nested_voices_preserved(self):
        self.praise()['allPraiseIsBiographerOwnVoice']=True;self.fails()
    def test_no_sales_from_recommendation(self):
        self.praise()['salesEstablished']=True;self.fails()
    def test_toplady_not_erased(self):
        self.praise()['byteVerifiedReading']['topLadyFootnote']=None;self.fails()
    def test_dateline_not_1682(self):
        self.praise()['byteVerifiedReading']['dateline']='1682';self.fails()
    def test_metadata_conflict_not_silently_fixed(self):
        self.praise()['byteVerifiedReading']['mirrorFrontmatter']='author: William Symington';self.fails()
    def test_context_hash(self):
        self.praise()['byteVerifiedReading']['editorialContext']['text']+=' changed';self.fails()
    def test_printed_locator_not_invented(self):
        self.praise()['byteVerifiedReading']['editorialContext']['startTeiPage']='1';self.fails()
    def test_adversative_not_erased(self):
        row=self.praise()['byteVerifiedReading']['paragraphs'][2]
        row['text']=row['text'].split('but he is not less')[0];row['textSha256']=digest(row['text']);self.fails()


class DigitalCollectionTests(unittest.TestCase):
    setUpClass=classmethod(ReceptionLocusTests.setUpClass.__func__)
    setUp=ReceptionLocusTests.setUp
    fails=ReceptionLocusTests.fails
    def collection(self):return self.r['digitalCollectionReview']
    def test_seven_navigation_segments(self):
        self.assertEqual(check_review(self.p,self.registry)['digitalCollectionContentLinks'],7)
    def test_no_edition_or_complete_works_promotion(self):
        for key in ['parsonsPhysicalEditionVerified','bestEditionRankingVerified','webCollectionIdentifiedAsParsons1815','completeWorksVerified','sevenLinksAreSevenTreatises','birthYearConflictResolved','linkedBodiesRead','publicationApproval']:
            self.collection()[key]=True;self.fails();self.collection()[key]=False
    def test_no_missing_link(self):
        self.collection()['byteVerifiedReading']['INDEX']['contentLinks'].pop();self.fails()
    def test_no_parts_merged_silently(self):
        self.collection()['byteVerifiedReading']['INDEX']['contentLinks'][5]['title']='A new independent treatise';self.fails()
    def test_literal_title_not_corrected(self):
        self.collection()['byteVerifiedReading']['INDEX']['contentLinks'][0]['title']='Discourse of the Nature of Regeneration';self.fails()
    def test_birth_conflict_not_normalised(self):
        self.collection()['byteVerifiedReading']['TITLE']['headings']=['[1628-1680]'];self.fails()
    def test_edition_claim_hash(self):
        self.collection()['byteVerifiedReading']['biographicalEditionClaim']['text']+=' changed';self.fails()
    def test_no_royal_format_replaced(self):
        claim=self.collection()['byteVerifiedReading']['biographicalEditionClaim'];claim['text']=claim['text'].replace('royal 8vo','folio');claim['textSha256']=digest(claim['text']);self.fails()
    def test_raw_pin(self):
        self.collection()['sourcePins']['TITLE']['sha256']='0'*64;self.fails()
    def test_scope_required(self):
        self.collection()['scope']='';self.fails()


if __name__=='__main__':unittest.main()
