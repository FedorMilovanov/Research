import hashlib
import tempfile
import unittest
from pathlib import Path

from audit_charnock_biographical_anchors import audit, text_and_pages, audit_publication_units, audit_edition_comparisons, audit_research_handoff


def tei(body):
    return ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><p>excluded</p></teiHeader><text>' + body + '</text></TEI>').encode()


class BiographyAnchorTests(unittest.TestCase):
    def registry(self, raw, probe, pages):
        return {'sources': {'X': {'sha256': hashlib.sha256(raw).hexdigest()}},
                'anchors': [{'id': 'one', 'source': 'X', 'probe': probe, 'teiPages': pages}]}

    def run_audit(self, raw, registry):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'X.xml').write_bytes(raw)
            return audit(registry, Path(tmp))

    def test_cross_page_nested_text_and_long_s(self):
        raw = tei('<p><pb n="33"/>Firſt <hi>word</hi> <pb n="34"/>next word</p>')
        self.assertEqual(self.run_audit(raw, self.registry(raw, 'First word next word', ['33', '34']))[0]['lexicalCheck'], 'PASS')

    def test_unnumbered_and_header_excluded(self):
        text, labels = text_and_pages(tei('<p>front text</p>'))
        self.assertNotIn('excluded', text)
        self.assertEqual(labels, [None] * len(text))

    def test_hash_mismatch_fails(self):
        raw = tei('<p>one</p>')
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            self.run_audit(tei('<p>two</p>'), self.registry(raw, 'one', [None]))

    def test_repeated_probe_fails(self):
        raw = tei('<p>one one</p>')
        with self.assertRaisesRegex(ValueError, 'one exact match'):
            self.run_audit(raw, self.registry(raw, 'one', [None]))

    def test_wrong_page_fails(self):
        raw = tei('<pb n="33"/><p>one</p>')
        with self.assertRaisesRegex(ValueError, 'page mismatch'):
            self.run_audit(raw, self.registry(raw, 'one', ['34']))

    def test_missing_probe_fails(self):
        raw = tei('<p>Josiah-like</p>')
        with self.assertRaisesRegex(ValueError, 'one exact match'):
            self.run_audit(raw, self.registry(raw, 'Jonah-like', [None]))


class PublicationUnitTests(unittest.TestCase):
    def registry(self):
        source = dict(evidenceClass='A1', accessState='FULL_OBJECT_VERIFIED',
                      locatorState='EXACT_LOCATOR_VERIFIED', rightsState='PUBLICATION_ELIGIBLE',
                      publicationState='REFERENCE', holds=['PUBLICATION_HOLD'])
        return dict(sources={'X': source}, anchors=[dict(id='one', source='X')],
                    bibliographyUnits=[dict(id='PUB', unitType='PRINTED_OBJECT', source='X',
                                            refs=['one'], owner='dossier.md', boundary='Only this object', **source)])

    def test_valid_object(self):
        self.assertEqual(audit_publication_units(self.registry()), 1)

    def test_wrong_source(self):
        r = self.registry(); r['bibliographyUnits'][0]['source'] = 'Y'
        with self.assertRaisesRegex(ValueError, 'Unknown printed object'):
            audit_publication_units(r)

    def test_duplicate_unit(self):
        r = self.registry(); r['bibliographyUnits'] *= 2
        with self.assertRaisesRegex(ValueError, 'Duplicate bibliography'):
            audit_publication_units(r)

    def test_unknown_ref(self):
        r = self.registry(); r['bibliographyUnits'][0]['refs'] = ['invented']
        with self.assertRaisesRegex(ValueError, 'Unknown bibliography anchor'):
            audit_publication_units(r)

    def test_source_state_cannot_be_promoted(self):
        r = self.registry(); r['bibliographyUnits'][0]['publicationState'] = 'PROMOTE'
        with self.assertRaisesRegex(ValueError, 'inherit source'):
            audit_publication_units(r)

    def test_family_cannot_be_claimed_as_full_object(self):
        r = self.registry(); r['bibliographyUnits'][0]['unitType'] = 'ACQUISITION_FAMILY'
        with self.assertRaisesRegex(ValueError, 'Unacquired family'):
            audit_publication_units(r)


class EditionComparisonTests(unittest.TestCase):
    def registry(self):
        return {'editionComparisons': [dict(id='CMP', comparisonType='SELECTED_SHARED_READING',
                probe='one', boundary='Not full collation',
                objects=[dict(source='X', teiPages=['1']), dict(source='Y', teiPages=['9'])])]}

    def texts(self):
        return {'X': ('one', ['1'] * 3), 'Y': ('one', ['9'] * 3)}

    def test_two_page_systems(self):
        self.assertEqual(audit_edition_comparisons(self.registry(), self.texts()), 1)

    def test_missing_match_fails(self):
        t = self.texts(); t['Y'] = ('two', ['9'] * 3)
        with self.assertRaisesRegex(ValueError, 'one exact match'):
            audit_edition_comparisons(self.registry(), t)

    def test_wrong_comparison_page_fails(self):
        r = self.registry(); r['editionComparisons'][0]['objects'][1]['teiPages'] = ['1']
        with self.assertRaisesRegex(ValueError, 'page mismatch'):
            audit_edition_comparisons(r, self.texts())


class ResearchHandoffTests(unittest.TestCase):
    def registry(self):
        refs = ['one', 'two', 'three']
        return {'anchors': [dict(id=x, evidenceClass='A1', locatorState='EXACT_LOCATOR_VERIFIED') for x in refs],
                'seriesSelection': [dict(id=x, refs=refs[:], boundary='Limited reading',
                  selectionState='SELECTION_ONLY', publicationState='BLOCKED', holds=['PUBLICATION_HOLD'])
                  for x in ['INTRO', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'REFERENCE']],
                'bibliographyUnits': [dict(id='FAM', unitType='ACQUISITION_FAMILY')],
                'acquisitionRequests': [dict(id='REQ', family='FAM', requestState='DRAFT_NOT_SENT',
                    receipt=None, accessState='NOT_ACQUIRED', publicationState='BLOCKED',
                    holds=['ARCHIVE_HOLD', 'EVIDENCE_HOLD', 'PUBLICATION_HOLD'],
                    expectedPacket=['title','contents','preface'], acceptance=['bytes','edition','rights'],
                    boundary='Not yet acquired', target='https://example.com')]}

    def test_valid_handoff(self):
        self.assertEqual(audit_research_handoff(self.registry()), {'documents': 10, 'requests': 1})

    def test_missing_document_fails(self):
        r = self.registry(); r['seriesSelection'].pop()
        with self.assertRaisesRegex(ValueError, 'ten distinct'):
            audit_research_handoff(r)

    def test_repeated_refs_fail(self):
        r = self.registry(); r['seriesSelection'][0]['refs'] = ['one'] * 3
        with self.assertRaisesRegex(ValueError, 'distinct references'):
            audit_research_handoff(r)

    def test_unknown_ref_fails(self):
        r = self.registry(); r['seriesSelection'][0]['refs'][0] = 'invented'
        with self.assertRaisesRegex(ValueError, 'Unknown selection'):
            audit_research_handoff(r)

    def test_no_publication_promotion(self):
        r = self.registry(); r['seriesSelection'][0]['publicationState'] = 'PROMOTE'
        with self.assertRaisesRegex(ValueError, 'cannot grant publication'):
            audit_research_handoff(r)

    def test_no_fake_receipt(self):
        r = self.registry(); r['acquisitionRequests'][0]['receipt'] = {'claimed': 'received'}
        with self.assertRaisesRegex(ValueError, 'cannot claim dispatch or receipt'):
            audit_research_handoff(r)

    def test_no_fake_full_object(self):
        r = self.registry(); r['acquisitionRequests'][0]['accessState'] = 'FULL_OBJECT_VERIFIED'
        with self.assertRaisesRegex(ValueError, 'unacquired and blocked'):
            audit_research_handoff(r)


class BiographicalCoreTests(unittest.TestCase):
    def setUp(self):
        import json
        from audit_charnock_biographical_anchors import audit_biographical_core
        self.check = audit_biographical_core
        self.r = json.loads((Path(__file__).resolve().parents[1] / 'data/charnock-biographical-anchors-v1.json').read_text())
        self.rows = self.r['biographicalCoreReview']['items']

    def test_current_bounded_core(self):
        self.assertEqual(self.check(self.r), 40)

    def test_missing_topic(self):
        self.rows.pop()
        with self.assertRaisesRegex(ValueError, 'topics'):
            self.check(self.r)

    def test_unknown_reference(self):
        self.rows[0]['refs'] = ['invented']
        with self.assertRaisesRegex(ValueError, 'reference'):
            self.check(self.r)

    def test_excluded_claim_cannot_be_printed(self):
        row = next(x for x in self.rows if x['disposition'] == 'EXCLUDE')
        row['safeFormulation'] = 'Unsupported assertion'
        with self.assertRaisesRegex(ValueError, 'Excluded claim'):
            self.check(self.r)

    def test_no_publication_promotion(self):
        self.rows[0]['publicationState'] = 'PROMOTE'
        with self.assertRaisesRegex(ValueError, 'cannot grant publication'):
            self.check(self.r)

    def test_secondary_cannot_replace_primary(self):
        self.r['anchors'][0]['evidenceClass'] = 'B1'
        with self.assertRaisesRegex(ValueError, 'checked primary'):
            self.check(self.r)

    def test_death_conflict_cannot_be_silently_collapsed(self):
        row = next(x for x in self.rows if x['topic'] == 'DEATH_DATE')
        row['disposition'] = 'ATTRIBUTED'
        with self.assertRaisesRegex(ValueError, 'conflict must remain explicit'):
            self.check(self.r)

    def test_invalid_operational_axis(self):
        self.rows[0]['rightsState'] = 'HOLD'
        with self.assertRaisesRegex(ValueError, 'state axis'):
            self.check(self.r)

    def test_core_layer_cannot_disappear(self):
        del self.r['biographicalCoreReview']
        with self.assertRaisesRegex(ValueError, 'Missing biographical'):
            self.check(self.r)


class ReceptionReviewTests(unittest.TestCase):
    def setUp(self):
        import json
        from audit_charnock_biographical_anchors import audit_reception_review
        self.check = audit_reception_review
        self.r = json.loads((Path(__file__).resolve().parents[1] / 'data/charnock-biographical-anchors-v1.json').read_text())
        self.review = self.r['receptionReview']

    def test_current_five_cases(self):
        self.assertEqual(self.check(self.r), 5)

    def test_missing_reception_type(self):
        self.review['items'].pop()
        with self.assertRaisesRegex(ValueError, 'five distinct'):
            self.check(self.r)

    def test_unknown_reference(self):
        self.review['items'][0]['witnessRefs'] = ['invented']
        with self.assertRaisesRegex(ValueError, 'reception reference'):
            self.check(self.r)

    def test_no_publication_promotion(self):
        self.review['items'][0]['publicationState'] = 'PROMOTE'
        with self.assertRaisesRegex(ValueError, 'cannot grant publication'):
            self.check(self.r)

    def test_no_automatic_influence(self):
        self.review['items'][0]['influenceState'] = 'PROVEN'
        with self.assertRaisesRegex(ValueError, 'infer influence'):
            self.check(self.r)

    def test_no_fake_raw_web_pin(self):
        self.review['extractArchive']['rawObjectSha256'] = 'a' * 64
        with self.assertRaisesRegex(ValueError, 'raw-object pin'):
            self.check(self.r)

    def test_primary_cannot_be_secondary(self):
        next(a for a in self.r['anchors'] if a['id'] == 'RCX-02')['evidenceClass'] = 'B1'
        with self.assertRaisesRegex(ValueError, 'primary locus'):
            self.check(self.r)

    def test_extract_must_match_anchor(self):
        next(a for a in self.r['supportAnchors'] if a['id'] == 'REC-05')['observedText'] = 'not observed'
        with self.assertRaisesRegex(ValueError, 'extract/anchor mismatch'):
            self.check(self.r)

    def test_extract_hash_must_match_bytes(self):
        self.review['extractArchive']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'extract SHA mismatch'):
            self.check(self.r)


class ResearchPreparationTests(unittest.TestCase):
    def setUp(self):
        import json
        from audit_charnock_biographical_anchors import audit_research_preparation
        self.check = audit_research_preparation
        self.r = json.loads((Path(__file__).resolve().parents[1] / 'data/charnock-biographical-anchors-v1.json').read_text())
        self.review = self.r['researchPreparationReview']

    def test_current_bounded_preparation(self):
        self.assertEqual(self.check(self.r), {'areas': 3, 'candidates': 16, 'researchOnly': 7, 'illustrations': 1})

    def test_content_area_cannot_disappear(self):
        self.review['contentAreas'].pop()
        with self.assertRaisesRegex(ValueError, 'three distinct'):
            self.check(self.r)

    def test_content_exclusions_required(self):
        self.review['contentAreas'][0]['exclusions'] = []
        with self.assertRaisesRegex(ValueError, 'exclusions/HOLD'):
            self.check(self.r)

    def test_unselected_quote_rejected(self):
        self.review['quotationPlan'][0]['documents'] = ['VIII']
        with self.assertRaisesRegex(ValueError, 'selected document'):
            self.check(self.r)

    def test_no_quote_publication_promotion(self):
        self.review['quotationPlan'][0]['publicationState'] = 'PROMOTE'
        with self.assertRaisesRegex(ValueError, 'overstate'):
            self.check(self.r)

    def test_quote_voice_cannot_disappear(self):
        self.review['quotationPlan'][0]['attribution'] = ''
        with self.assertRaisesRegex(ValueError, 'attributed voice'):
            self.check(self.r)

    def test_candidate_words_must_match(self):
        self.review['quotationPlan'][0]['quoteText'] = 'invented quotation'
        with self.assertRaisesRegex(ValueError, 'checked primary text'):
            self.check(self.r)

    def test_candidate_cannot_claim_final_public_text(self):
        self.review['quotationPlan'][0]['textKind'] = 'FINAL_PUBLIC_QUOTE'
        with self.assertRaisesRegex(ValueError, 'checked primary text'):
            self.check(self.r)

    def test_candidate_archive_pin_must_match(self):
        self.review['quotationPlan'][0]['archive']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'archive pin'):
            self.check(self.r)

    def test_research_only_is_not_cleared_quotation(self):
        q = next(q for q in self.review['quotationPlan'] if q['decision'] == 'RESEARCH_ONLY')
        q['quoteText'] = 'Not an approved direct quotation'
        with self.assertRaisesRegex(ValueError, 'Research-only'):
            self.check(self.r)

    def test_death_date_pair_not_silently_split(self):
        next(q for q in self.review['quotationPlan'] if q['ref'] == 'CORE-06')['conflictGroup'] = None
        with self.assertRaisesRegex(ValueError, 'both conflict witnesses'):
            self.check(self.r)

    def test_illustration_cannot_be_swapped_for_portrait(self):
        self.review['illustrations'][0]['path'] = 'portrait.png'
        with self.assertRaisesRegex(ValueError, 'not historical evidence'):
            self.check(self.r)

    def test_illustration_operational_axes_are_not_source_class(self):
        self.review['illustrations'][0]['accessState'] = 'A1'
        with self.assertRaisesRegex(ValueError, 'not historical evidence'):
            self.check(self.r)

    def test_illustration_checksum_must_match(self):
        self.review['illustrations'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SHA/path'):
            self.check(self.r)

    def test_external_images_not_silently_added(self):
        self.review['externalImagesDecision'] = 'PORTRAIT_CLEARED'
        with self.assertRaisesRegex(ValueError, 'External image'):
            self.check(self.r)


if __name__ == '__main__':
    unittest.main()
