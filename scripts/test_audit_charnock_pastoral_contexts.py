"""Synthetic fixtures exercise locators,not historical or theological assertions."""
import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from audit_charnock_pastoral_contexts import check_pardon_distinctions, check_mourning_distinctions
from audit_charnock_pastoral_contexts import ROOT, THEOLOGY_REFS, THEOLOGY_AFTER, REGENERATE_HEADING, extract_regenerate_opening, check_regenerate_opening, check_regenerate_continuation, check_doctrinal_review, REFS, STUDY_REFS, extract, extract_mercy_opening


class PastoralContextTests(unittest.TestCase):
    def fixture(self, wrong_heading=False, wrong_transition=False, refs=REFS):
        divisions, anchors = [], []
        for index, ref in enumerate(refs):
            probe = 'Unique marker ' + ref
            number = None if ref == 'BIB-06' else str(index + 1)
            pb = '<pb/>' if number is None else f'<pb n="{number}"/>'
            signed = '<signed>Edw. Veel.</signed>' if ref == 'BIB-06' else ''
            divisions.append('<div>' + pb + '<head>Fixture section</head><p>Before</p><p>'
                             + probe + '</p>' + ''.join(f'<p>After {i}</p>' for i in range(10))
                             + signed + '</div>')
            anchors.append(dict(id=ref, source='B20167', probe=probe, teiPages=[number]))
        heading = 'Wrong heading' if wrong_heading else 'Chiefest Sinners Objects of Choicest Mercy.'
        transition = 'No switch' if wrong_transition else 'For the last'
        # A separate pagination sequence also starts at1;heading disambiguates it.
        divisions.append('<div><pb n="1"/><head>' + heading + '</head><epigraph>Fixture epigraph</epigraph>'
                         + '<p>First observation</p><p>Second observation</p><p>' + transition + '</p>'
                         + ''.join(f'<p>Opening argument {i}</p>' for i in range(4)) + '</div>')
        raw = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>' + ''.join(divisions)
               + '</body></text></TEI>').encode()
        registry = dict(anchors=anchors, sources={'B20167': dict(size=len(raw), sha256=hashlib.sha256(raw).hexdigest())})
        return raw, registry

    def run_fixture(self, raw, registry, opening=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'B20167.xml').write_bytes(raw)
            return (extract_mercy_opening if opening else extract)(root, registry)

    def test_explicit_study_ref_set_does_not_expand_to_pastoral_set(self):
        raw, registry = self.fixture(refs=STUDY_REFS)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'B20167.xml').write_bytes(raw)
            result = extract(root, registry, refs=STUDY_REFS)
            self.assertEqual(set(result), set(STUDY_REFS))
            self.assertTrue(all(len(c['contextWindow']) == 3 for c in result.values()))

    def test_expanded_doctrinal_windows(self):
        raw, registry = self.fixture(refs=THEOLOGY_REFS)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'B20167.xml').write_bytes(raw)
            result = extract(root, registry, refs=THEOLOGY_REFS, window_after=THEOLOGY_AFTER)
            self.assertEqual(len(result['TXT-06']['contextWindow']),7)
            self.assertEqual(len(result['TXT-07']['contextWindow']),10)

    def test_negative_window_rejected(self):
        raw, registry = self.fixture(refs=THEOLOGY_REFS)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'B20167.xml').write_bytes(raw)
            with self.assertRaisesRegex(ValueError,'nonnegative integer'):
                extract(root, registry, refs=THEOLOGY_REFS, window_after={'TXT-06':-1})

    def test_explicit_continuation_may_exclude_anchor(self):
        raw, registry = self.fixture(refs=('TXT-07',))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'B20167.xml').write_bytes(raw)
            c=extract(root,registry,refs=('TXT-07',),paragraph_ranges={'TXT-07':(4,7)})['TXT-07']
            self.assertEqual([p['paragraphIndexZeroBased'] for p in c['contextWindow']],[4,5,6,7])
            self.assertFalse(c['anchorProbeInsideWindow'])
            self.assertEqual(c['nextParagraphSectionHeading'],'Fixture section')

    def test_explicit_range_cannot_silently_truncate(self):
        raw, registry = self.fixture(refs=('TXT-07',))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'B20167.xml').write_bytes(raw)
            with self.assertRaisesRegex(ValueError,'within the source'):
                extract(root,registry,refs=('TXT-07',),paragraph_ranges={'TXT-07':(4,999)})

    def test_explicit_range_cannot_reverse(self):
        raw, registry = self.fixture(refs=('TXT-07',))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'B20167.xml').write_bytes(raw)
            with self.assertRaisesRegex(ValueError,'ordered'):
                extract(root,registry,refs=('TXT-07',),paragraph_ranges={'TXT-07':(7,4)})

    def test_seven_contexts(self):
        self.assertEqual(set(self.run_fixture(*self.fixture())), set(REFS))

    def test_lexical_scheme_retained(self):
        result = self.run_fixture(*self.fixture())
        self.assertEqual(len(result['TXT-04']['contextWindow']), 11)

    def test_editor_signature_and_unnumbered_locator(self):
        result = self.run_fixture(*self.fixture())['BIB-06']
        self.assertEqual(result['sectionSignatures'], ['Edw. Veel.'])
        self.assertEqual(result['probeTeiPages'], [None])

    def test_source_bytes_not_trusted_by_filename(self):
        raw, registry = self.fixture()
        with self.assertRaisesRegex(ValueError, 'byte pin'):
            self.run_fixture(raw + b' ', registry)

    def test_mercy_opening_by_heading_not_page_one(self):
        result = self.run_fixture(*self.fixture(), opening=True)
        self.assertEqual(len(result['paragraphs']), 7)
        self.assertEqual(result['paragraphs'][0]['text'], 'First observation')
        self.assertEqual(result['paragraphs'][0]['startTeiPage'], '1')

    def test_wrong_heading_rejected(self):
        with self.assertRaisesRegex(ValueError, 'heading'):
            self.run_fixture(*self.fixture(wrong_heading=True), opening=True)

    def test_missing_second_observation_transition_rejected(self):
        with self.assertRaisesRegex(ValueError, 'transition'):
            self.run_fixture(*self.fixture(wrong_transition=True), opening=True)

    def test_read_only_deterministic(self):
        data = self.fixture()
        self.assertEqual(self.run_fixture(*data), self.run_fixture(*data))


class DoctrinalDistinctionContractTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['doctrinalDistinctionReview']

    def rejected(self):
        with self.assertRaises(ValueError):check_doctrinal_review(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_doctrinal_review(self.plan,self.registry)['doctrinalObservations'],11)

    def test_no_full_system_claim(self):
        self.review['completeSystemClaimed']=True;self.rejected()

    def test_no_publication_approval(self):
        self.review['publicationApproval']=True;self.rejected()

    def test_retains_extended_followup(self):
        self.review['byteVerifiedContexts']['TXT-07']['contextWindow'].pop();self.rejected()

    def test_paragraph_hash(self):
        self.review['byteVerifiedContexts']['TXT-06']['contextWindow'][0]['text']+=' new';self.rejected()

    def test_peter_conjecture_not_historical_fact(self):
        next(o for o in self.review['observations'] if o['id']=='PETER')['probeRole']='ESTABLISHED_HISTORY';self.rejected()

    def test_relation_qualification_not_removed(self):
        self.review['observations']=[o for o in self.review['observations'] if o['id']!='RELATION'];self.rejected()

    def test_not_an_approved_translation(self):
        self.review['observations'][0]['translationState']='APPROVED';self.rejected()

    def test_old_matrix_history_retained(self):
        next(r for r in self.plan['theologyMatrix'] if r['ref']=='TXT-06')['reviewHistory']=[];self.rejected()

    def test_root_checks_axes(self):
        from audit_charnock_series_plan import check
        self.review['observations'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)


class RegenerateContinuationContractTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['regenerateContinuationReview']

    def rejected(self):
        with self.assertRaises(ValueError):check_regenerate_continuation(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_regenerate_continuation(self.plan,self.registry)['newRegenerateParagraphs'],33)

    def test_no_fixed_duration(self):
        self.review['durationDetermined']=True;self.rejected()

    def test_no_comfort_guarantee(self):
        self.review['comfortRestorationGuaranteed']=True;self.rejected()

    def test_no_full_treatise_claim(self):
        self.review['completeTreatiseClaimed']=True;self.rejected()

    def test_not_independent_witness(self):
        self.review['sourceDependencyState']='INDEPENDENT_WITNESS';self.rejected()

    def test_bridge_not_counted_twice(self):
        self.review['newParagraphCount']=34;self.rejected()

    def test_next_discourse_not_absorbed(self):
        self.review['byteVerifiedContexts']['TXT-07']['nextParagraphSectionHeading']='A DISCOURSE OF THE Sins of the Regenerate.';self.rejected()

    def test_hypothetical_not_unqualified_fact(self):
        next(o for o in self.review['observations'] if o['id']=='SUPPOSE_ACTUAL_CONSENT')['probeRole']='ESTABLISHED_HISTORY';self.rejected()

    def test_followup_remains_linked(self):
        next(o for o in self.plan['doctrinalDistinctionReview']['observations'] if o['id']=='DAVID').pop('followUpReview');self.rejected()

    def test_paragraph_hash(self):
        self.review['byteVerifiedContexts']['TXT-07']['contextWindow'][4]['text']+=' extra';self.rejected()

    def test_root_checks_new_axes(self):
        from audit_charnock_series_plan import check
        self.review['observations'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)


class RegenerateOpeningContractTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['regenerateOpeningReview']

    def rejected(self):
        with self.assertRaises(ValueError):check_regenerate_opening(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_regenerate_opening(self.plan,self.registry)['regenerateMainTextParagraphsCovered'],70)

    def test_not_critical_edition(self):
        self.review['criticalEditionVerified']=True;self.rejected()

    def test_not_complete_exegesis(self):
        self.review['completeExegesisClaimed']=True;self.rejected()

    def test_not_publication_approval(self):
        self.review['publicationApproval']=True;self.rejected()

    def test_coverage_must_not_skip(self):
        self.review['discourseLayout']['blocks'].pop(4);self.rejected()

    def test_overlap_must_match_even_if_rehashed(self):
        p=self.review['byteVerifiedContexts']['TXT-07']['contextWindow'][-1]
        p['text']+=' new';p['textSha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.rejected()

    def test_rejected_grace_loss_not_endorsed(self):
        next(o for o in self.review['observations'] if o['id']=='GRACE_LOST')['probeRole']='AUTHOR_THESIS';self.rejected()

    def test_marginal_citation_not_source_replay(self):
        self.review['marginalNoteDecisions'][0]['citedWorkIndependentlyReplayed']=True;self.rejected()

    def test_no_silent_name_repair(self):
        n=self.review['byteVerifiedMarginalNotes'][2];n['text']=n['text'].replace('Amyrant.','Amyraut.')
        n['textSha256']=hashlib.sha256(n['text'].encode()).hexdigest()
        self.review['marginalNoteDecisions'][2]['noteSha256']=n['textSha256'];self.rejected()

    def test_note_parent_required(self):
        self.review['byteVerifiedMarginalNotes'][0]['parentParagraphIndexZeroBased']=527;self.rejected()

    def test_preceding_discourse_not_absorbed(self):
        self.review['discourseLayout']['precedingPrintedDiscourseHeading']=REGENERATE_HEADING;self.rejected()

    def test_new_count_excludes_context_and_bridge(self):
        self.review['newDiscourseParagraphs']=29;self.rejected()

    def test_root_checks_axes(self):
        from audit_charnock_series_plan import check
        self.review['marginalNoteDecisions'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)


class RegenerateLayoutExtractionTests(unittest.TestCase):
    def fixture(self):
        # 491 preceding paragraphs,one epigraph,and 69 body paragraphs fix
        # the synthetic global coordinate system without using historical text.
        before='<div><head>A DISCOURSE FOR The Comfort of Child-bearing Women.</head>'+''.join('<p>Before '+str(i)+'</p>' for i in range(491))+'</div>'
        body=[]
        for i in range(492,561):
            text='Unique anchor' if i==519 else 'Body '+str(i)
            note='<note place="margin">Fixture citation</note>' if i==526 else ''
            body.append('<p>'+text+note+'</p>')
        discourse='<div type="discourse"><head>'+REGENERATE_HEADING+'</head><epigraph><p>Fixture epigraph</p></epigraph>'+''.join(body)+'</div>'
        following='<div><head>A DISCOURSE OF The Pardon of Sin.</head><p>Next discourse</p></div>'
        raw=('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><pb n="89"/>'+before+discourse+following+'</body></text></TEI>').encode()
        return raw,dict(anchors=[dict(id='TXT-07',source='A32724',probe='Unique anchor',teiPages=['89'])],sources={'A32724':dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())})

    def replay(self,raw,registry):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'A32724.xml').write_bytes(raw)
            return extract_regenerate_opening(root,registry)

    def test_separate_epigraph_body_and_marginal_note(self):
        result=self.replay(*self.fixture());layout=result['discourseLayout']
        self.assertEqual(len(layout['blocks']),70)
        self.assertEqual(layout['blocks'][0]['zone'],'EPIGRAPH')
        self.assertEqual(layout['directBodyParagraphs'],69)
        self.assertEqual(result['marginalNotes'][0]['parentParagraphIndexZeroBased'],526)
        self.assertEqual(layout['excludedNoteCount'],1)

    def test_layout_requires_actual_pin(self):
        raw,registry=self.fixture()
        with self.assertRaisesRegex(ValueError,'byte pin'):self.replay(raw+b' ',registry)


class PardonDistinctionContractTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['pardonDistinctionReview']

    def rejected(self):
        with self.assertRaises(ValueError):check_pardon_distinctions(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_pardon_distinctions(self.plan,self.registry)['pardonDistinctionParagraphs'],12)

    def test_not_complete_treatise(self):
        self.review['completeTreatiseClaimed']=True;self.rejected()

    def test_not_publication_approval(self):
        self.review['publicationApproval']=True;self.rejected()

    def test_following_qualifications_cannot_disappear(self):
        self.review['byteVerifiedContexts']['TXT-04']['contextWindow'].pop(8);self.rejected()

    def test_qualification_not_unqualified_thesis(self):
        next(o for o in self.review['observations'] if o['id']=='SATISFACTION')['probeRole']='AUTHOR_THESIS';self.rejected()

    def test_not_independent_witnesses(self):
        self.review['independenceState']='INDEPENDENT_WITNESSES';self.rejected()

    def test_replayed_paragraphs_not_new(self):
        self.review['newParagraphCount']=14;self.rejected()

    def test_concordance_must_match_prior_even_if_rehashed(self):
        p=self.review['byteVerifiedContexts']['TXT-20']['contextWindow'][0]
        p['text']+=' invented';p['textSha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.rejected()

    def test_root_checks_new_axes(self):
        from audit_charnock_series_plan import check
        self.review['observations'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)


class MourningDistinctionContractTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/self.plan['baselineRegistry']).read_text())
        self.review=self.plan['mourningDistinctionReview']

    def rejected(self):
        with self.assertRaises(ValueError):check_mourning_distinctions(self.plan,self.registry)

    def test_current_contract(self):
        self.assertEqual(check_mourning_distinctions(self.plan,self.registry)['mourningObservations'],10)

    def test_no_full_treatise_claim(self):
        self.review['completeTreatiseClaimed']=True;self.rejected()

    def test_no_collective_blame_approval(self):
        self.review['modernCollectiveBlameApproved']=True;self.rejected()

    def test_no_outward_guarantee(self):
        self.review['guaranteedOutwardProtection']=True;self.rejected()

    def test_preservation_qualification_retained(self):
        self.review['observations']=[o for o in self.review['observations'] if o['id']!='INWARD_OUTWARD'];self.rejected()

    def test_strong_claim_not_sanitized(self):
        self.review['observations']=[o for o in self.review['observations'] if o['id']!='NATIONAL_GUILT'];self.rejected()

    def test_compassion_rule_not_removed(self):
        self.review['observations']=[o for o in self.review['observations'] if o['id']!='PERSON'];self.rejected()

    def test_old_opening_not_new(self):
        self.review['newPastoralParagraphs']=17;self.rejected()

    def test_prior_opening_exact_even_if_rehashed(self):
        p=self.review['byteVerifiedContexts']['opening']['contextWindow'][0]
        p['text']+=' invented';p['textSha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.rejected()

    def test_root_checks_new_axes(self):
        from audit_charnock_series_plan import check
        self.review['observations'][0]['publicationState']='READY'
        with self.assertRaises(ValueError):check(self.plan)



class PardonOpeningTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/'data/charnock-biographical-anchors-v1.json').read_text())
        self.r=self.plan['pardonOpeningReview']

    def check(self):
        from audit_charnock_pastoral_contexts import check_pardon_opening
        return check_pardon_opening(self.plan,self.registry)

    def test_sixty_paragraphs_thirty_seven_new(self):
        self.assertEqual(self.check(),dict(pardonOpeningParagraphs=60,newPardonOpeningParagraphs=37,pardonOpeningObservations=13,pardonWholeDiscourseRead=False))

    def test_not_whole_pardon(self):
        self.r['wholeDiscourseRead']=True
        with self.assertRaises(ValueError):self.check()

    def test_prior_coverage_preserved(self):
        self.r['previouslyReadParagraphIndices']=[]
        with self.assertRaises(ValueError):self.check()

    def test_no_new_foreign_originals(self):
        self.r['foreignOriginalsVerified']=True
        with self.assertRaises(ValueError):self.check()

    def test_standalone_unknown_unit(self):
        self.r['byteVerifiedReading']['openingDirectTags'].append('q')
        with self.assertRaises(ValueError):self.check()

    def test_epigraph_required(self):
        self.r['byteVerifiedReading']['openingDirectTags'].remove('epigraph')
        with self.assertRaises(ValueError):self.check()

    def test_boundary_not_covered(self):
        self.r['byteVerifiedReading']['nextParagraph']['paragraphIndexZeroBased']=620
        with self.assertRaises(ValueError):self.check()

    def test_note_coordinates(self):
        self.r['byteVerifiedReading']['marginalNotes'][0]['parentParagraphIndexZeroBased']=593
        with self.assertRaises(ValueError):self.check()

    def test_actual_span_required(self):
        self.r['observations'][5]['englishSpan']='repentance merits pardon'
        with self.assertRaises(ValueError):self.check()

    def test_hold_not_cleared(self):
        self.r['observations'][0]['holds']=[]
        with self.assertRaises(ValueError):self.check()



class PardonCompleteTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/'data/charnock-biographical-anchors-v1.json').read_text())
        self.r=self.plan['pardonCompleteReview'];self.data=self.r['byteVerifiedReading']

    def check(self):
        from audit_charnock_pastoral_contexts import check_pardon_complete
        return check_pardon_complete(self.plan,self.registry)

    def test_complete131_not_critical(self):
        self.assertEqual(self.check(),dict(pardonMainTextParagraphs=131,pardonAdditionalCoverageParagraphs=71,pardonContinuationObservations=20,pardonMarginalNotes=2,pardonWholeDiscourseRead=True))

    def test_manifest_gap(self):
        self.data['mainTextManifest'].pop()
        with self.assertRaises(ValueError):self.check()

    def test_continuation_hash(self):
        self.data['continuationContext']['contextWindow'][0]['text']+=' foreign interpretation'
        with self.assertRaises(ValueError):self.check()

    def test_five_application_sections(self):
        self.data['layout'].pop()
        with self.assertRaises(ValueError):self.check()

    def test_printed_heading_not_silently_renumbered(self):
        self.data['layout'][-1]['heading']='5. Exhortation to those that are pardoned.'
        with self.assertRaises(ValueError):self.check()

    def test_back_not_next_sermon(self):
        self.data['nextParagraph']['zone']='BODY'
        with self.assertRaises(ValueError):self.check()

    def test_burges_note_required(self):
        self.data['marginalNotes'].pop()
        with self.assertRaises(ValueError):self.check()

    def test_actual_counterfactual_span_required(self):
        self.r['observations'][3]['englishSpan']='Devils will be saved'
        with self.assertRaises(ValueError):self.check()

    def test_no_clinical_guarantee(self):
        self.r['modernClinicalGuaranteeApproved']=True
        with self.assertRaises(ValueError):self.check()

    def test_not_critical_edition(self):
        self.r['criticalEditionVerified']=True
        with self.assertRaises(ValueError):self.check()

    def test_source_pin(self):
        self.data['continuationContext']['sourceSha256']='0'*64
        with self.assertRaises(ValueError):self.check()

    def test_prior_opening_not_removed(self):
        self.plan['pardonOpeningReview']['byteVerifiedReading']['context']['contextWindow'].pop()
        with self.assertRaises(ValueError):self.check()

    def test_hold_not_removed(self):
        self.r['observations'][0]['holds']=[]
        with self.assertRaises(ValueError):self.check()

    def test_part_vii_link(self):
        next(d for d in self.plan['documents'] if d['id']=='VII')['supplementaryMainTextReadings'].remove('pardonCompleteReview')
        with self.assertRaises(ValueError):self.check()



class StabilityOpeningTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/'data/charnock-biographical-anchors-v1.json').read_text())
        self.r=self.plan['stabilityOpeningReview'];self.data=self.r['byteVerifiedReading']

    def check(self):
        from audit_charnock_pastoral_contexts import check_stability_opening
        return check_stability_opening(self.plan,self.registry)

    def test_saved_window_and_doctrine(self):
        self.assertEqual(self.check(),dict(stabilityOpeningParagraphs=36,stabilityStandaloneDoctrine=1,stabilityNewCoverageParagraphs=33,stabilityMarginalNotes=20,stabilityOpeningObservations=16))

    def test_not_whole_or_dated(self):
        for k in ['wholeDiscourseRead','datedOccasionEstablished','modernCollectiveBlameApproved']:
            with self.subTest(key=k):
                self.r[k]=True
                with self.assertRaises(ValueError):self.check()
                self.r[k]=False

    def test_doctrine_not_foreign_quotation(self):
        self.data['standaloneDoctrine'][0]['voice']='FOREIGN_QUOTATION'
        with self.assertRaises(ValueError):self.check()

    def test_standalone_doctrine_not_omitted(self):
        self.data['standaloneDoctrine']=[]
        with self.assertRaises(ValueError):self.check()

    def test_note_cannot_be_raw_acquisition(self):
        self.r['marginalNoteDecisions'][0]['counterpartRawAcquired']=True
        with self.assertRaises(ValueError):self.check()

    def test_note_coordinates(self):
        self.data['marginalNotes'][0]['parentParagraphIndexZeroBased']=96
        with self.assertRaises(ValueError):self.check()

    def test_no_sanitized_source_bytes(self):
        self.data['context']['contextWindow'][103-92]['text']='Only inclusive language'
        with self.assertRaises(ValueError):self.check()

    def test_actual_particular_church_limit(self):
        self.r['observations'][10]['englishSpan']='Every particular church will last forever'
        with self.assertRaises(ValueError):self.check()

    def test_no_hold_release(self):
        self.r['observations'][0]['holds']=[]
        with self.assertRaises(ValueError):self.check()

    def test_prior_window_unchanged(self):
        self.data['context']['contextWindow'][0]['text']='Changed epigraph'
        with self.assertRaises(ValueError):self.check()



class StabilityCompleteTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        self.registry=json.loads((ROOT/'data/charnock-biographical-anchors-v1.json').read_text())
        self.r=self.plan['stabilityCompleteReview'];self.data=self.r['byteVerifiedReading']

    def check(self):
        from audit_charnock_pastoral_contexts import check_stability_complete
        return check_stability_complete(self.plan,self.registry)

    def test_complete93_paragraphs94_units(self):
        self.assertEqual(self.check(),dict(stabilityMainTextParagraphs=93,stabilityMainTextUnits=94,stabilityAdditionalCoverageParagraphs=57,stabilityMarginalNotes=48,stabilityContinuationObservations=26,stabilityWholeDiscourseRead=True))

    def test_manifest_gap(self):
        self.data['mainTextManifest'].pop()
        with self.assertRaises(ValueError):self.check()

    def test_doctrine_not_omitted(self):
        self.data['standaloneDoctrine']=[]
        with self.assertRaises(ValueError):self.check()

    def test_source_pin(self):
        self.data['continuationContext']['sourceSha256']='0'*64
        with self.assertRaises(ValueError):self.check()

    def test_next_discourse_not_included(self):
        self.data['nextParagraph']['paragraphIndexZeroBased']=184
        with self.assertRaises(ValueError):self.check()

    def test_prior_notes_retained(self):
        self.data['marginalNotes'].pop(0)
        with self.assertRaises(ValueError):self.check()

    def test_no_foreign_raw_promotion(self):
        self.r['additionalMarginalNoteDecisions'][0]['counterpartRawAcquired']=True
        with self.assertRaises(ValueError):self.check()

    def test_damaged_name_not_reconstructed(self):
        self.data['marginalNotes'][23]['text']='Charron verified original'
        with self.assertRaises(ValueError):self.check()

    def test_no_racial_or_violence_approval(self):
        for k in ['modernRacialHierarchyApproved','modernViolenceMandateApproved']:
            with self.subTest(key=k):
                self.r[k]=True
                with self.assertRaises(ValueError):self.check()
                self.r[k]=False

    def test_no_date_claim(self):
        self.r['datedOccasionEstablished']=True
        with self.assertRaises(ValueError):self.check()

    def test_actual_span_required(self):
        self.r['observations'][17]['englishSpan']='Every private prayer is guaranteed'
        with self.assertRaises(ValueError):self.check()

    def test_part_vii_link(self):
        next(d for d in self.plan['documents'] if d['id']=='VII')['supplementaryMainTextReadings'].remove('stabilityCompleteReview')
        with self.assertRaises(ValueError):self.check()

    def test_not_critical_edition(self):
        self.r['criticalEditionVerified']=True
        with self.assertRaises(ValueError):self.check()

    def test_holds_preserved(self):
        self.r['observations'][0]['holds']=[]
        with self.assertRaises(ValueError):self.check()


if __name__ == '__main__':
    unittest.main()
