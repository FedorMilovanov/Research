import copy
import json
import unittest
from audit_charnock_series_plan import ROOT, PLAN, check


class EditorialPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / PLAN).read_text())

    def test_current_blueprint(self):
        report = check(self.plan)
        self.assertEqual((report['documents'], report['mainParts']), (10, 8))
        self.assertEqual(len(report['openPackages']), 3)
        self.assertEqual(report['publicationState'], 'BLOCKED')
        self.assertEqual(report['currentRevisionCustody'], 'NOT_REVERIFIED')
        self.assertFalse(report['historicalReceiptMatchesCurrentTree'])

    def test_working_title_must_be_listed(self):
        self.plan['documents'][3]['title'] = 'Как Чарнок читает Писание'
        with self.assertRaisesRegex(ValueError, 'Title selection'):
            check(self.plan)

    def test_no_eighteen_reader_chapters(self):
        self.plan['documents'] += copy.deepcopy(self.plan['documents'][:8])
        with self.assertRaisesRegex(ValueError, 'ten ordered'):
            check(self.plan)

    def test_no_silent_loss_of_legacy_chapter(self):
        self.plan['documents'].pop(8)
        with self.assertRaises(ValueError):
            check(self.plan)

    def test_no_double_full_exposition(self):
        self.plan['documents'][6]['crossRefs'].remove('TXT-14')
        self.plan['documents'][6]['primaryRefs'].append('TXT-14')
        with self.assertRaisesRegex(ValueError, 'multiple primary owners'):
            check(self.plan)

    def test_unknown_anchor_rejected(self):
        self.plan['documents'][2]['primaryRefs'].append('UNVERIFIED-NEW-SOURCE')
        with self.assertRaisesRegex(ValueError, 'Unknown anchor'):
            check(self.plan)

    def test_source_class_not_promoted(self):
        ref = next(iter(self.plan['referenceSnapshot']))
        self.plan['referenceSnapshot'][ref]['evidenceClass'] = 'A3'
        with self.assertRaisesRegex(ValueError, 'Source axes'):
            check(self.plan)

    def test_source_hold_not_dropped(self):
        ref = next(iter(self.plan['referenceSnapshot']))
        self.plan['referenceSnapshot'][ref]['holds'] = []
        with self.assertRaisesRegex(ValueError, 'Source axes'):
            check(self.plan)

    def test_plan_not_publication_approval(self):
        self.plan['documents'][3]['publicationState'] = 'PROMOTE'
        with self.assertRaises(ValueError):
            check(self.plan)

    def test_no_claim_that_research_tasks_are_done(self):
        self.plan['tasks'][2]['status'] = 'DONE'
        with self.assertRaisesRegex(ValueError, 'silently claim'):
            check(self.plan)

    def test_no_new_authored_chapters(self):
        self.plan['authoredChapters'] = 10
        with self.assertRaises(ValueError):
            check(self.plan)

    def test_case_must_have_existing_locator(self):
        self.plan['documents'][2]['dossierCases'][0]['section'] = 'INVENTED'
        with self.assertRaisesRegex(ValueError, 'source section'):
            check(self.plan)

    def test_case_path_cannot_escape(self):
        self.plan['documents'][2]['dossierCases'][0]['dossier'] = '../../../AGENT_RULES.md'
        with self.assertRaisesRegex(ValueError, 'Unsafe dossier'):
            check(self.plan)

    def test_unchanged_packet_members_not_exempted(self):
        self.plan['expectedChangedPacketMembers'].append('data/charnock-biographical-anchors-v1.json')
        with self.assertRaisesRegex(ValueError, 'Unexpected changes'):
            check(self.plan)

    def test_all_boundary_rules_required(self):
        self.plan['duplicationRules'].pop()
        with self.assertRaisesRegex(ValueError, 'boundary rule'):
            check(self.plan)

    def test_rejected_reading_cannot_become_authorial_claim(self):
        self.plan['studyCards'][-1]['positionRole'] = 'AUTHORIAL_ARGUMENT'
        with self.assertRaisesRegex(ValueError, 'position role'):
            check(self.plan)

    def test_preserved_context_not_rewritten(self):
        self.plan['studyCards'][0]['preservedContext'] += 'invented continuation'
        with self.assertRaisesRegex(ValueError, 'source context'):
            check(self.plan)

    def test_unlinked_fresh_xml_replay_claim_rejected(self):
        self.plan['studyCards'][0]['reviewBasis'] = 'FRESH_XML_REPLAY'
        with self.assertRaisesRegex(ValueError, 'context limits'):
            check(self.plan)

    def test_no_prepared_translation_claim(self):
        self.plan['studyCards'][0]['translationState'] = 'PREPARED'
        with self.assertRaises(ValueError):
            check(self.plan)

    def test_case_candidate_cannot_disappear(self):
        self.plan['documents'][2]['dossierCases'].pop()
        with self.assertRaisesRegex(ValueError, 'Three explicit'):
            check(self.plan)

    def test_no_complete_system_claim(self):
        self.plan['theologyMatrix'][0]['synthesisState'] = 'COMPLETE'
        with self.assertRaisesRegex(ValueError, 'complete synthesis'):
            check(self.plan)

    def test_title_approval_not_silently_removed(self):
        self.plan['titleDecision']['approved'] = False
        with self.assertRaisesRegex(ValueError, 'Title selection'):
            check(self.plan)

    def test_book_context_checksum(self):
        self.plan['principalBookReading']['byteVerifiedExtraction']['contexts'][0]['contextWindow'][0]['text'] += 'invented'
        with self.assertRaisesRegex(ValueError, 'paragraph checksum'):
            check(self.plan)

    def test_book_review_not_prepared_translation(self):
        self.plan['principalBookReading']['manualReviewCards'][0]['translationState'] = 'PREPARED'
        with self.assertRaises(ValueError):
            check(self.plan)

    def test_pair_counterpart_not_freshly_acquired(self):
        self.plan['sourceUseCases'][0]['counterpartSide']['accessState'] = 'FULL_OBJECT_VERIFIED'
        with self.assertRaisesRegex(ValueError, 'Counterpart evidence'):
            check(self.plan)

    def test_pair_counterpart_rights_not_assumed(self):
        self.plan['sourceUseCases'][2]['counterpartSide']['rightsState'] = 'PUBLICATION_ELIGIBLE'
        with self.assertRaisesRegex(ValueError, 'Counterpart evidence'):
            check(self.plan)

    def test_pair_context_not_rewritten(self):
        self.plan['sourceUseCases'][0]['charnockSide']['byteVerifiedContext']['bodyParagraph'] += 'invented'
        with self.assertRaisesRegex(ValueError, 'pair source/context'):
            check(self.plan)

    def test_pair_requires_publication_hold(self):
        self.plan['sourceUseCases'][0]['holds'] = []
        with self.assertRaises(ValueError):
            check(self.plan)

    def test_pastoral_editor_not_charnock(self):
        c = next(c for c in self.plan['pastoralReview']['readingCards'] if c['ref'] == 'BIB-06')
        c['authorVoice'] = 'CHARNOCK_BODY'
        with self.assertRaisesRegex(ValueError, 'Pastoral voice'):
            check(self.plan)

    def test_pastoral_context_not_truncated(self):
        self.plan['pastoralReview']['byteVerifiedContexts']['TXT-04']['contextWindow'].pop()
        with self.assertRaisesRegex(ValueError, 'lexical scheme'):
            check(self.plan)

    def test_lost_first_discourse_not_recovered(self):
        self.plan['pastoralReview']['mercyOpeningReview']['firstDoctrineRecovered'] = True
        with self.assertRaisesRegex(ValueError, 'lost first discourse'):
            check(self.plan)

    def test_work_profiles_not_full_work(self):
        self.plan['pastoralReview']['workProfiles'][0]['profileState'] = 'FULL_WORK_READ'
        with self.assertRaisesRegex(ValueError, 'whole-work'):
            check(self.plan)

    def test_anniversary_does_not_date_delivery(self):
        self.plan['pastoralReview']['workProfiles'][-1]['eventDateEstablished'] = True
        with self.assertRaisesRegex(ValueError, 'delivery date'):
            check(self.plan)

    def test_no_authorial_system_inferred(self):
        self.plan['pastoralReview']['synthesisRelations'][0]['kind'] = 'AUTHORIAL_SYSTEM'
        with self.assertRaisesRegex(ValueError, 'authorial system'):
            check(self.plan)

    def test_no_first_edition_acquisition_by_decision(self):
        d = next(d for d in self.plan['boundaryReview']['unitDecisions'] if d['id'] == 'FAM-01')
        d['decision'] = 'ACQUIRED'
        with self.assertRaisesRegex(ValueError, 'Unit decision'):
            check(self.plan)

    def test_biographical_conflict_not_resolved(self):
        d = next(d for d in self.plan['boundaryReview']['claimDecisions'] if d['id'] == 'BCD-37')
        d['action'] = 'USE_EXACT_DATE'
        with self.assertRaisesRegex(ValueError, 'Biographical decision'):
            check(self.plan)

    def test_excluded_family_claim_not_revived(self):
        d = next(d for d in self.plan['boundaryReview']['claimDecisions'] if d['id'] == 'BCD-33')
        d['safeFormulation'] = 'No wife or children'
        with self.assertRaisesRegex(ValueError, 'Biographical decision'):
            check(self.plan)

    def test_draft_not_dispatched(self):
        self.plan['boundaryReview']['requestDecisions'][0]['requestState'] = 'SENT'
        with self.assertRaisesRegex(ValueError, 'Draft request'):
            check(self.plan)

    def test_title_not_rewritten(self):
        self.plan['boundaryReview']['byteVerifiedTitles']['PUB-04']['titleText'] += 'Entire VolII'
        with self.assertRaisesRegex(ValueError, 'Title source'):
            check(self.plan)

    def test_working_translation_not_publication_approval(self):
        self.plan['translationReview']['publicationApproval'] = True
        with self.assertRaisesRegex(ValueError, 'Working translation'):
            check(self.plan)

    def test_no_fictional_independent_reviewer(self):
        self.plan['translationReview']['items'][0]['independentReview']['reviewer'] = 'Self-check'
        with self.assertRaisesRegex(ValueError, 'Russian draft'):
            check(self.plan)

    def test_russian_draft_hash_not_stale(self):
        self.plan['translationReview']['items'][0]['russianDraft'] += ' Added text'
        with self.assertRaisesRegex(ValueError, 'Russian draft'):
            check(self.plan)

    def test_editorial_quote_not_authorial(self):
        self.plan['translationReview']['items'][2]['voice'] = 'CHARNOCK_BODY'
        with self.assertRaisesRegex(ValueError, 'Selected quote'):
            check(self.plan)

    def test_quote_must_remain_literal_span(self):
        self.plan['translationReview']['items'][2]['quoteText'] = 'I collated all manuscripts completely'
        with self.assertRaisesRegex(ValueError, 'Selected quote'):
            check(self.plan)

    def test_no_page_image_permission_from_tcp_cc0(self):
        self.plan['translationReview']['items'][0]['imageRights'] = 'APPROVED'
        with self.assertRaisesRegex(ValueError, 'Russian draft'):
            check(self.plan)

    def test_research_only_candidate_not_promoted(self):
        d = next(q for q in self.plan['translationReview']['baselineCandidateDispositions'] if q['originalDecision'] == 'RESEARCH_ONLY')
        d['decision'] = 'KEEP_CANDIDATE_WITHOUT_PUBLICATION_APPROVAL'
        with self.assertRaisesRegex(ValueError, 'Quotation candidate'):
            check(self.plan)

    def test_full_uncertainty_ending_required(self):
        import hashlib
        c = self.plan['translationReview']['byteVerifiedContexts']['TR-TXT03']
        c['selectedParagraph'] = c['selectedParagraph'].removesuffix('uncertain.')
        c['selectedParagraphSha256'] = hashlib.sha256(c['selectedParagraph'].encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'uncertainty ending'):
            check(self.plan)

    def test_translation_snapshot_cannot_remove_source_hold(self):
        self.plan['translationReview']['items'][0]['sourceStateSnapshot']['holds'] = []
        with self.assertRaisesRegex(ValueError, 'Selected quote'):
            check(self.plan)

    def test_rejected_consequence_not_turned_into_doctrine(self):
        row = self.plan['sourceUseCases'][2]['criticalReview']['microReadings'][1]
        row['positionRole'] = 'AUTHORIAL_ASSERTION'
        with self.assertRaisesRegex(ValueError, 'Micro-reading'):
            check(self.plan)

    def test_conditional_antecedent_not_stripped(self):
        import hashlib
        row = self.plan['sourceUseCases'][2]['criticalReview']['microReadings'][1]
        row['charnockSpan'] = "they are not so much God's Elect, as God their Elect;"
        row['charnockSpanSha256'] = hashlib.sha256(row['charnockSpan'].encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'conditional antecedent'):
            check(self.plan)

    def test_old_ocr_not_new_raw_acquisition(self):
        self.plan['sourceUseCases'][0]['criticalReview']['counterpartRawReacquired'] = True
        with self.assertRaisesRegex(ValueError, 'not claim fresh counterpart'):
            check(self.plan)

    def test_inherited_gloss_not_independently_approved(self):
        self.plan['sourceUseCases'][0]['criticalReview']['workingGlosses'][0]['independentReview'] = True
        with self.assertRaisesRegex(ValueError, 'Foreign gloss'):
            check(self.plan)

    def test_foreign_words_must_exist_in_preserved_dossier(self):
        import hashlib
        g = self.plan['sourceUseCases'][0]['criticalReview']['workingGlosses'][0]
        g['foreignSpan'] = 'invented Latin quotation'
        g['foreignSpanSha256'] = hashlib.sha256(g['foreignSpan'].encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'Foreign gloss'):
            check(self.plan)

    def test_french_conditional_link_must_retain_rejected_context(self):
        g = self.plan['sourceUseCases'][2]['criticalReview']['workingGlosses'][1]
        g['microReading'] = 'D3'
        with self.assertRaisesRegex(ValueError, 'Conditional French gloss'):
            check(self.plan)

    def test_filename_search_not_exhaustive_archive_audit(self):
        self.plan['counterpartSearchReview']['searchKind'] = 'EXHAUSTIVE_DRIVE_AUDIT'
        with self.assertRaisesRegex(ValueError, 'Filename search'):
            check(self.plan)

    def test_deeper_reading_does_not_close_counterpart_gate(self):
        self.plan['tasks'][1]['status'] = 'DONE_BOUNDED'
        with self.assertRaisesRegex(ValueError, 'silently claim'):
            check(self.plan)

    def test_fresh_scripture_does_not_reconstruct_greek(self):
        self.plan['freshStudyReview']['greekReconstructed'] = True
        with self.assertRaisesRegex(ValueError, 'Greek reconstruction'):
            check(self.plan)

    def test_selected_exegesis_not_whole_corpus_method(self):
        self.plan['freshStudyReview']['wholeCorpusMethodVerified'] = True
        with self.assertRaisesRegex(ValueError, 'whole-corpus method'):
            check(self.plan)

    def test_txt20_probe_role_not_changed_by_full_paragraph(self):
        c = next(c for c in self.plan['freshStudyReview']['readingCards'] if c['ref'] == 'TXT-20')
        c['probeRole'] = 'AUTHORIAL_ARGUMENT'
        with self.assertRaisesRegex(ValueError, 'probe polarity'):
            check(self.plan)

    def test_txt20_whole_paragraph_not_only_rejected_position(self):
        c = next(c for c in self.plan['freshStudyReview']['readingCards'] if c['ref'] == 'TXT-20')
        c['paragraphRole'] = 'REJECTED_POSITION'
        with self.assertRaisesRegex(ValueError, 'entire paragraph'):
            check(self.plan)

    def test_fresh_scripture_paragraph_hash_not_stale(self):
        c = self.plan['freshStudyReview']['byteVerifiedContexts']['TXT-01']
        c['contextWindow'][1]['text'] += ' invented continuation'
        with self.assertRaisesRegex(ValueError, 'paragraph hash'):
            check(self.plan)

    def test_selected_study_freshness_requires_followup(self):
        self.plan['studyCards'][0]['followUpReview'] = 'UNKNOWN'
        with self.assertRaisesRegex(ValueError, 'probe polarity'):
            check(self.plan)

    def test_q06_context_not_translation_approval(self):
        self.plan['freshStudyReview']['quotationFollowUp']['translationState'] = 'APPROVED'
        with self.assertRaisesRegex(ValueError, 'Q06 fresh English'):
            check(self.plan)

    def test_q06_context_not_publication_approval(self):
        self.plan['freshStudyReview']['quotationFollowUp']['publicationApproval'] = True
        with self.assertRaisesRegex(ValueError, 'Q06 fresh English'):
            check(self.plan)

    def test_completed_setup_history_not_erased(self):
        self.plan['documents'][3]['remainingWorkHistory'] = []
        with self.assertRaisesRegex(ValueError, 'explicit history'):
            check(self.plan)

    def test_read_only_input(self):
        original = copy.deepcopy(self.plan)
        self.assertEqual(check(self.plan), check(self.plan))
        self.assertEqual(original, self.plan)


if __name__ == '__main__':
    unittest.main()
