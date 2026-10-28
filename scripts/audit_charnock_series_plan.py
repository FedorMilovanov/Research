#!/usr/bin/env python3
"""Read-only editorial blueprint audit, not publication or renewed custody approval."""
import argparse
import hashlib
import json
from pathlib import Path

from audit_charnock_copyist_transmission import check_review as check_copyist_transmission
from audit_charnock_mercy_distinctions import check_review as check_mercy_distinctions
from audit_charnock_reception_locus import check_review as check_reception_locus
from audit_charnock_folio_apparatus import check_review as check_folio_apparatus
from audit_charnock_cartesian_definition import check_review as check_cartesian_definition
from audit_charnock_mourning import check_review as check_mourning_complete
from audit_charnock_childbearing import check_review as check_childbearing
from audit_charnock_handoff import canonical_bytes
from audit_charnock_thoughts import check_review as check_thoughts, check_complete as check_thoughts_complete
from audit_charnock_prayer import check_review as check_prayer
from audit_charnock_fifth_november import check_review as check_fifth_november
from audit_charnock_pastoral_contexts import check_doctrinal_review, check_regenerate_continuation, check_regenerate_opening, check_pardon_distinctions, check_mourning_distinctions, check_pardon_opening, check_pardon_complete, check_stability_opening, check_stability_complete
from audit_charnock_political_context import check_review as check_political_context
from audit_charnock_reference_material import check_review as check_reference_material
from audit_charnock_death_witnesses import check_review as check_death_witnesses
from audit_charnock_editorial_voice import check_review as check_editorial_voice
from audit_charnock_editorial_translations import check_review as check_editorial_translations, check_authorial_review, check_atheism_review, check_enmity_review
from audit_charnock_source_use import check_critical_review, check_acquisition_boundary, check_scripture_purpose
from audit_charnock_translation_contexts import check_review
from audit_charnock_editorial_links import check_review as check_routing_review

ROOT = Path(__file__).resolve().parents[1]
PLAN = Path('data/charnock-series-editorial-plan-v1.json')
IDS = ['INTRO', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'REFERENCE']
AXES = ['evidenceClass', 'accessState', 'locatorState', 'rightsState', 'publicationState', 'holds']


def check(plan, root=ROOT):
    if (plan.get('id') != 'CHARNOCK-EDITORIAL-PLAN-V1'
            or plan.get('authorityRole') != 'corpus-specific-editorial-proposal-only'
            or plan.get('stage') != 'BLUEPRINT_WITH_OPEN_WORK_NOT_AUTHORING'
            or plan.get('authoredChapters') != 0):
        raise ValueError('Editorial plan must not claim authoring or root authority')
    documents = plan['documents']
    if [d['id'] for d in documents] != IDS:
        raise ValueError('Exactly ten ordered documents,eight main parts,are required')
    decision = plan['titleDecision']
    if (decision['document'] != 'III' or decision['approved'] is not True
            or len(set(decision['alternatives'])) < 3
            or documents[3]['title'] not in decision['alternatives']
            or decision['recommended'] != documents[3]['title']
            or documents[3]['titleState'] != 'USER_APPROVED'
            or decision.get('approvedTitle') != 'Чарнок и Писание: от текста к проповеди'
            or documents[3]['title'] != decision.get('approvedTitle')
            or not decision.get('approvalBasis')):
        raise ValueError('Title selection must preserve the explicit user-approved title')
    registry = json.loads((root / plan['baselineRegistry']).read_text())
    anchors = {a['id']: a for a in registry['anchors'] + registry['supportAnchors']}
    policy = json.loads((root / 'data/repository-evidence-policy-v2.json').read_text())
    used, owners = set(), {}
    for document in plan['mourningCompleteReview']['observations'] + plan['mourningCompleteReview']['marginalNoteDecisions'] + plan['mourningDistinctionReview']['observations'] + plan['pardonDistinctionReview']['observations'] + plan['childbearingReview']['observations'] + plan['childbearingReview']['marginalNoteDecisions'] + plan['childbearingReview']['limitedRelations'] + plan['regenerateOpeningReview']['observations'] + plan['regenerateOpeningReview']['marginalNoteDecisions'] + plan['regenerateContinuationReview']['observations'] + plan['doctrinalDistinctionReview']['observations'] + plan['politicalContextReview']['normCards'] + plan['politicalContextReview']['wordingComparisons'] + plan['referenceMaterialReview']['chronologySelection'] + plan['referenceMaterialReview']['bibliographicSelection'] + plan['referenceMaterialReview']['contextualGlosses'] + [plan] + documents + plan['studyCards'] + plan['theologyMatrix'] + plan['principalBookReading']['manualReviewCards'] + plan['sourceUseCases'] + plan['pastoralReview']['readingCards'] + plan['pastoralReview']['workProfiles'] + [plan['pastoralReview']['mercyOpeningReview']] + plan['pastoralReview']['synthesisRelations'] + plan['boundaryReview']['unitDecisions'] + plan['boundaryReview']['claimDecisions'] + plan['boundaryReview']['requestDecisions'] + plan['boundaryReview']['archiveDebts'] + plan['translationReview']['items'] + plan['translationReview']['baselineCandidateDispositions'] + plan['routingReview']['contextReceptionDecisions'] + plan['routingReview']['ownershipHandoffs'] + plan['routingReview']['transitionQuestions'] + plan['routingReview']['corpusBridges'] + plan['editorialVoiceReview']['readingCards'] + plan['editorialVoiceReview']['authorTests'] + plan['editorialVoiceReview']['quotationFollowUps'] + plan['freshStudyReview']['readingCards'] + plan['freshStudyReview']['limitedRelations'] + [plan['freshStudyReview']['quotationFollowUp']] + plan['deathWitnessReview']['witnessDecisions'] + [plan['counterpartSearchReview']] + [row for case in plan['sourceUseCases'] for row in case['criticalReview']['microReadings'] + case['criticalReview']['workingGlosses']]:
        if (document.get('evidenceClass') != 'C' or document.get('publicationState') != 'BLOCKED'
                or document.get('rightsState') != 'RIGHTS_UNKNOWN'
                or document.get('accessState') != 'FULL_OBJECT_VERIFIED'
                or document.get('locatorState') != 'EXACT_LOCATOR_VERIFIED'
                or not {'EVIDENCE_HOLD', 'ARCHIVE_HOLD', 'RIGHTS_HOLD', 'PUBLICATION_HOLD'} <= set(document.get('holds', []))):
            raise ValueError('Editorial proposals need independent axes and explicit holds')
    for d in documents:
        if (not d.get('question') or not d.get('workingThesis') or len(d.get('outline', [])) < 5
                or len(d.get('excludedClaims', [])) < 3 or not d.get('remainingWork')
                or not 1000 <= d['targetWords'][0] <= d['targetWords'][1] <= 5000):
            raise ValueError('Incomplete document passport')
        if not d['primaryRefs'] or set(d['primaryRefs']) & set(d['crossRefs']):
            raise ValueError('Primary and cross-reference roles must be distinct')
        for ref in d['primaryRefs']:
            if ref in owners:
                raise ValueError('Full exposition has multiple primary owners: ' + ref)
            owners[ref] = d['id']
        for ref in d['primaryRefs'] + d['crossRefs']:
            if ref not in anchors:
                raise ValueError('Unknown anchor: ' + ref)
            used.add(ref)
        for case in d['dossierCases']:
            source = root / 'БИОГРАФИИ/Стивен Чарнок' / case['dossier']
            if not source.resolve().is_relative_to((root / 'БИОГРАФИИ/Стивен Чарнок').resolve()):
                raise ValueError('Unsafe dossier case path')
            text = source.read_text()
            if not case.get('boundary') or ('## ' + case['section'] + '.') not in text:
                raise ValueError('Case lacks source section or limits')
            if not case.get('legacyIds') or any(identifier not in text for identifier in case['legacyIds']):
                raise ValueError('Unknown legacy case;not a newly verified quote')
    if set(plan['referenceSnapshot']) != used:
        raise ValueError('Snapshot must cover precisely the referenced anchors')
    for ref, snap in plan['referenceSnapshot'].items():
        a = anchors[ref]
        locator = a.get('locator', {'teiPages': a.get('teiPages')})
        if (any(snap.get(k) != a[k] for k in AXES) or snap['source'] != a['source']
                or snap['locator'] != locator or snap['boundary'] != a['claimBoundary']):
            raise ValueError('Source axes,locator or boundary changed in editorial snapshot')
        if (a['evidenceClass'] not in policy['sourceClasses'] or a['accessState'] not in policy['accessStates']
                or a['locatorState'] not in policy['locatorStates'] or a['rightsState'] not in policy['rightsStates']
                or a['publicationState'] not in policy['publicationStates']
                or not set(a['holds']) <= set(policy['holds'])):
            raise ValueError('Unknown source axis')
    cases = documents[2]['dossierCases']
    if {c['id'] for c in cases} != {'CASE-LINGENDES', 'CASE-RAYNAUD', 'CASE-DAILLE'} or len(cases) != 3:
        raise ValueError('Three explicit source-use case candidates required')
    operations = {'TXT-01': 'SCRIPTURE_INTERPRETS_SCRIPTURE', 'TXT-02': 'SCENE_TO_DOCTRINAL_APPLICATION',
                  'TXT-03': 'ALTERNATIVES_LEFT_OPEN', 'TXT-18': 'UNCERTAIN_HISTORICAL_SETTING',
                  'TXT-20': 'REJECTED_READING_AND_GRAMMAR'}
    cards = plan['studyCards']
    if len(cards) != 5 or {c['ref'] for c in cards} != set(operations):
        raise ValueError('Five distinct study cards required')
    for c in cards:
        a = anchors[c['ref']]
        expected_role = ('REJECTED_POSITION' if c['ref'] == 'TXT-20' else
                         'AUTHORIAL_QUESTION' if c['ref'] == 'TXT-03' else 'AUTHORIAL_ARGUMENT')
        if (c['operation'] != operations[c['ref']] or c['positionRole'] != expected_role
                or c['source'] != a['source'] or c['teiPages'] != a['teiPages']
                or c['preservedProbe'] != a['probe'] or c['preservedContext'] != a['contextExcerpt']
                or c['preservedContextSha256'] != hashlib.sha256(a['contextExcerpt'].encode()).hexdigest()):
            raise ValueError('Study card cannot alter source context or position role')
        fresh = c['ref'] == 'TXT-03'
        expected_basis = 'FRESH_XML_PARAGRAPH_IN_TRANSLATION_REVIEW' if fresh else 'FRESH_XML_CONTEXT_IN_SCRIPTURE_REVIEW'
        expected_translation = 'SELECTED_EXCERPT_WORKING_DRAFT_NOT_INDEPENDENTLY_REVIEWED' if fresh else 'NOT_PREPARED'
        if (c['reviewBasis'] != expected_basis or c['fullContextRecheckRequired'] is not False
                or c['canGeneralizeToWholeCorpus'] is not False or c['translationState'] != expected_translation
                or len(c['argumentSteps']) < 3 or not c['limitedConclusion'] or not c['readingToAvoid']):
            raise ValueError('Study card must preserve context limits and unprepared translation outside selected excerpt')
        if fresh and (c.get('followUpReview') != 'TR-TXT03' or c.get('preservedExcerptState') != 'HISTORICAL_TRUNCATED_RETAINED'):
            raise ValueError('Fresh TXT03 context must link follow-up without rewriting historical excerpt')
    study = plan['freshStudyReview']
    if (study['reviewState'] != 'FOUR_FRESH_WINDOWS_PLUS_PRIOR_TXT03_NOT_CORPUS_CLOSURE'
            or study['greekReconstructed'] is not False or study['wholeCorpusMethodVerified'] is not False
            or set(study['byteVerifiedContexts']) != {'TXT-01', 'TXT-02', 'TXT-18', 'TXT-20'}
            or len(study['readingCards']) != 4
            or {c['ref'] for c in study['readingCards']} != set(study['byteVerifiedContexts'])):
        raise ValueError('Four fresh Scripture windows cannot certify Greek reconstruction or whole-corpus method')
    for c in study['readingCards']:
        ctx = study['byteVerifiedContexts'][c['ref']]
        a = anchors[c['ref']]
        old = next(k for k in cards if k['ref'] == c['ref'])
        source = registry['sources'][a['source']]
        if (ctx['source'] != a['source'] or ctx['sourceSha256'] != source['sha256'] or ctx['sourceBytes'] != source['size']
                or ctx['probe'] != a['probe'] or ctx['probeTeiPages'] != a['teiPages'] or len(ctx['contextWindow']) != 3):
            raise ValueError('Fresh Scripture context must bind original source and probe locator')
        for w in ctx['contextWindow']:
            if hashlib.sha256(w['text'].encode()).hexdigest() != w['textSha256']:
                raise ValueError('Fresh Scripture paragraph hash differs')
        selected = [w for w in ctx['contextWindow'] if w['paragraphIndexZeroBased'] == ctx['selectedParagraphIndexZeroBased']]
        if (len(selected) != 1 or c['literalAnchor'] not in selected[0]['text'] or ctx['probe'] not in selected[0]['text']
                or c['probeRole'] != old['positionRole'] or c['translationState'] != 'NOT_PREPARED'
                or old.get('followUpReview') != c['id'] or not old.get('reviewHistory')
                or old['reviewHistory'][0]['state'] != 'HISTORICAL_REGISTRY_EXCERPT_CHECKPOINT'
                or not c['rejectedReading'] or not c['authorAffirmation'] or not c['boundary']):
            raise ValueError('Fresh study must retain probe polarity,history and translation boundary')
        if c['ref'] == 'TXT-20' and c['paragraphRole'] != 'MIXED_REJECTED_READING_AND_AUTHORIAL_REPLY':
            raise ValueError('TXT20 rejected probe is not the role of the entire paragraph')
    relations = study['limitedRelations']
    if (len(relations) != 2 or {r['id'] for r in relations} != {'ANTIQUITY_AND_OLD_DIVINITY','UNCERTAINTY_AND_POSITIVE_EXEGESIS'}
            or any(not r['relation'] or not r['limit'] or not set(r['refs']) <= set(operations) for r in relations)):
        raise ValueError('Two explicitly limited Scripture/editorial relations required')
    followup = study['quotationFollowUp']
    q = next(q for q in registry['researchPreparationReview']['quotationPlan'] if q['id'] == 'Q-06')
    selected = study['byteVerifiedContexts']['TXT-18']
    if (followup['id'] != 'Q-06' or followup['ref'] != 'TXT-18'
            or followup['canonicalRowSha256'] != hashlib.sha256(canonical_bytes(q)).hexdigest()
            or not any(q['quoteText'] in w['text'] for w in selected['contextWindow'])
            or followup['translationState'] != 'NOT_PREPARED' or followup['publicationApproval'] is not False):
        raise ValueError('Q06 fresh English context cannot approve translation or publication')
    for doc in documents:
        if doc['id'] in {'III','IV','V','VI','VII'}:
            if not any(h['state'] == 'HISTORICAL_SUPERSEDED_COMPLETED_BOUNDED_SETUP' and h['items'] for h in doc.get('remainingWorkHistory', [])):
                raise ValueError('Completed setup queue must be retained as explicit history')
    translation_drafts = check_review(plan, registry)
    routing_report = check_routing_review(plan, registry, root)
    editorial_voice_report = check_editorial_voice(plan, registry)
    editorial_translation_report = check_editorial_translations(plan, registry)
    authorial_translation_report = check_authorial_review(plan, registry)
    atheism_report = check_atheism_review(plan, registry)
    enmity_report = check_enmity_review(plan, registry)
    death_witness_report = check_death_witnesses(plan, registry, root)
    mourning_complete_report = check_mourning_complete(plan, registry)
    mourning_report = check_mourning_distinctions(plan, registry)
    pardon_report = check_pardon_distinctions(plan, registry)
    pardon_opening_report = check_pardon_opening(plan, registry)
    pardon_opening_report['pardonOpeningWholeDiscourseRead'] = pardon_opening_report.pop('pardonWholeDiscourseRead')
    pardon_complete_report = check_pardon_complete(plan, registry)
    stability_report = check_stability_opening(plan, registry)
    stability_report['stabilityOpeningMarginalNotes'] = stability_report.pop('stabilityMarginalNotes')
    stability_complete_report = check_stability_complete(plan, registry)
    fifth_november_report = check_fifth_november(plan, registry)
    prayer_report = check_prayer(plan, registry)
    thoughts_report = check_thoughts(plan, registry)
    thoughts_report['thoughtsOpeningWholeDiscourseRead'] = thoughts_report.pop('thoughtsWholeDiscourseRead')
    thoughts_report['thoughtsOpeningCureSectionRead'] = thoughts_report.pop('thoughtsCureSectionRead')
    thoughts_complete_report = check_thoughts_complete(plan, registry)
    cartesian_report = check_cartesian_definition(plan, registry)
    folio_apparatus_report = check_folio_apparatus(plan, registry)
    copyist_transmission_report = check_copyist_transmission(plan, registry)
    mercy_distinctions_report = check_mercy_distinctions(plan, registry)
    reception_locus_report = check_reception_locus(plan, registry)
    scripture_purpose_report = check_scripture_purpose(plan, registry)
    childbearing_report = check_childbearing(plan, registry)
    opening_report = check_regenerate_opening(plan, registry)
    continuation_report = check_regenerate_continuation(plan, registry)
    doctrinal_report = check_doctrinal_review(plan, registry)
    political_report = check_political_context(plan, registry)
    reference_report = check_reference_material(plan, registry)
    matrix = plan['theologyMatrix']
    if len(matrix) != 4 or {m['ref'] for m in matrix} != {'TXT-05', 'TXT-06', 'TXT-07', 'TXT-08'}:
        raise ValueError('Four bounded theological rows required')
    for m in matrix:
        a = anchors[m['ref']]
        if (m['synthesisState'] != 'WORKING_MATRIX_NOT_COMPLETE_SYSTEM' or m['source'] != a['source']
                or m['teiPages'] != a['teiPages'] or not m['limitedRelation']
                or not m['applicationTask'] or not m['limit']):
            raise ValueError('Theological matrix cannot claim complete synthesis')
    source_cases = plan['sourceUseCases']
    if len(source_cases) != 3 or {c['id'] for c in source_cases} != {'CASE-LINGENDES', 'CASE-RAYNAUD', 'CASE-DAILLE'}:
        raise ValueError('Three derived source-use pairs required')
    micro_readings, inherited_glosses = 0, 0
    for case in source_cases:
        dossier = (root / case['dossierPath']).resolve()
        if not dossier.is_relative_to((root / 'БИОГРАФИИ/Стивен Чарнок').resolve()):
            raise ValueError('Unsafe pair dossier')
        text = dossier.read_text()
        if (hashlib.sha256(dossier.read_bytes()).hexdigest() != case['dossierSha256']
                or case['dossierSection'] not in text or any(k not in text for k in case['legacyIds'])):
            raise ValueError('Pair dossier provenance differs')
        side = case['charnockSide']
        ctx = side['byteVerifiedContext']
        source = registry['sources']['A32723']
        if (ctx['sourceSha256'] != source['sha256'] or ctx['sourceBytes'] != source['size']
                or hashlib.sha256(ctx['bodyParagraph'].encode()).hexdigest() != ctx['bodyParagraphSha256']
                or ctx['probe'] not in ctx['bodyParagraph'] or not ctx['marginalNotes']
                or side['evidenceClass'] != 'A1' or side['accessState'] != 'FULL_OBJECT_VERIFIED'
                or side['locatorState'] != 'EXACT_LOCATOR_VERIFIED'
                or side['rightsState'] != 'PUBLICATION_ELIGIBLE' or side['publicationState'] != 'BLOCKED'
                or not {'ARCHIVE_HOLD', 'PUBLICATION_HOLD'} <= set(side['holds'])):
            raise ValueError('Charnock pair source/context changed or promoted')
        counterpart = case['counterpartSide']
        if (case['reviewState'] != 'DERIVED_PAIR_PACKET_COUNTERPART_RECHECK_OPEN'
                or counterpart['reviewBasis'] != 'PRESERVED_DOSSIER_OCR_NOT_FRESH_REMOTE_RETRIEVAL'
                or counterpart['evidenceClass'] != 'A1' or counterpart['accessState'] != 'PARTIAL_OBJECT'
                or counterpart['locatorState'] != 'COARSE_LOCATOR_ONLY'
                or counterpart['rightsState'] != 'RIGHTS_UNKNOWN' or counterpart['publicationState'] != 'BLOCKED'
                or not {'ARCHIVE_HOLD', 'LOCATOR_HOLD', 'RIGHTS_HOLD', 'PUBLICATION_HOLD'} <= set(counterpart['holds'])):
            raise ValueError('Counterpart evidence must remain partial,inherited and held')
        if (len(case['comparisonSteps']) < 3 or any(not all(step.get(k) for k in ('counterpart', 'charnock', 'assessment')) for step in case['comparisonSteps'])
                or len(case['unprovedClaims']) < 3 or not case['nextCheck'] or not case['functionInCharnock']
                or not case['limitedConclusion'] or case['translationState'] != 'NOT_PREPARED'):
            raise ValueError('Pair needs argument,function,bounds and unprepared translation')
        micro_count, gloss_count = check_critical_review(case, text)
        micro_readings += micro_count
        inherited_glosses += gloss_count
    search = plan['counterpartSearchReview']
    if (search['searchKind'] != 'DRIVE_FILENAME_QUERIES_ONLY' or search['independentCounterpartRawLocated'] is not False
            or len(search['queries']) != 2 or not search['searchBoundary']
            or any(q['nextPageToken'] is not None or q['incompleteSearch'] is not False for q in search['queries'])
            or len(search['queries'][0]['returnedFiles']) != 1 or search['queries'][1]['returnedFiles']
            or search['queries'][0]['returnedFiles'][0]['classification'] != 'DERIVED_DOSSIER_NOT_COUNTERPART_RAW'):
        raise ValueError('Filename search cannot certify counterpart acquisition or exhaustive archive absence')
    check_acquisition_boundary(plan)
    pastoral = plan['pastoralReview']
    refs = {'TXT-07', 'TXT-08', 'TXT-17', 'TXT-04', 'BIB-07', 'BIB-06', 'TXT-19'}
    if (pastoral['reviewState'] != 'BOUNDED_SEVEN_CONTEXTS_FIVE_TEXT_PROFILES'
            or set(pastoral['byteVerifiedContexts']) != refs
            or len(pastoral['readingCards']) != 7 or {c['ref'] for c in pastoral['readingCards']} != refs):
        raise ValueError('Seven bounded pastoral contexts/cards required')
    for ref, ctx in pastoral['byteVerifiedContexts'].items():
        a = anchors[ref]
        source = registry['sources'][a['source']]
        if (ctx['source'] != a['source'] or ctx['sourceSha256'] != source['sha256']
                or ctx['sourceBytes'] != source['size'] or ctx['probe'] != a['probe']
                or ctx['probeTeiPages'] != a['teiPages']):
            raise ValueError('Pastoral source pin/probe/pages changed')
        window = ctx['contextWindow']
        selected = [p for p in window if p['paragraphIndexZeroBased'] == ctx['selectedParagraphIndexZeroBased']]
        if (len(selected) != 1 or a['probe'] not in selected[0]['text']
                or len(window) < (11 if ref == 'TXT-04' else 3)):
            raise ValueError('Pastoral context or lexical scheme truncated')
        for paragraph in window:
            if hashlib.sha256(paragraph['text'].encode()).hexdigest() != paragraph['textSha256']:
                raise ValueError('Pastoral paragraph checksum mismatch')
        if ref == 'BIB-06' and not any('Edw. Veel.' in text for text in ctx['sectionSignatures']):
            raise ValueError('Editorial signature must be preserved')
    for c in pastoral['readingCards']:
        voice = 'VEEL_EDITORIAL_PREFACE' if c['ref'] == 'BIB-06' else 'CHARNOCK_BODY'
        if (c['authorVoice'] != voice or c['translationState'] != 'NOT_PREPARED'
                or c['reviewBasis'] != 'FRESH_BYTE_PINNED_PARAGRAPH_WINDOW'
                or len(c['argumentSteps']) < 3 or not c['limitedConclusion'] or not c['boundary']):
            raise ValueError('Pastoral voice,scope or translation cannot be promoted')
    profiles = pastoral['workProfiles']
    expected_profiles = {'OTHER-PROVIDENCE', 'OTHER-PARDON', 'OTHER-ENMITY', 'OTHER-MERCY', 'OTHER-ANNIVERSARY'}
    if len(profiles) != 5 or {p['id'] for p in profiles} != expected_profiles:
        raise ValueError('Five selected-text profiles required,not five new books')
    for profile in profiles:
        coverage = 'SELECTED_AUTHORIAL_OPENING_AND_EDITORIAL_TRANSMISSION' if profile['id'] == 'OTHER-MERCY' else 'SELECTED_AUTHORIAL_PARAGRAPHS'
        if (profile['profileState'] != 'ACCEPTED_BOUNDED_SELECTED_TEXT_NOT_WHOLE_WORK'
                or profile['coverage'] != coverage or profile['primaryChapter'] != 'VII'
                or not set(profile['refs']) <= refs or not profile['refs']
                or len(profile['notCovered']) < 3 or not profile['contribution']):
            raise ValueError('Work profile cannot claim a whole-work or missing authorial reading')
        if profile['id'] == 'OTHER-ANNIVERSARY' and profile['eventDateEstablished'] is not False:
            raise ValueError('Anniversary heading cannot establish delivery date')
    mercy = pastoral['mercyOpeningReview']
    opening = mercy['byteVerifiedOpening']
    source = registry['sources']['B20167']
    if (opening['sourceSha256'] != source['sha256'] or opening['sourceBytes'] != source['size']
            or opening['sectionHeading'] != 'Chiefest Sinners Objects of Choicest Mercy.'
            or mercy['authorVoice'] != 'CHARNOCK_BODY' or mercy['translationState'] != 'NOT_PREPARED'
            or mercy['firstDoctrineRecovered'] is not False or len(mercy['argumentSteps']) < 3
            or not mercy['limitedConclusion'] or not mercy['boundary']):
        raise ValueError('Mercy opening cannot recover the lost first discourse or mix voices')
    paragraphs = opening['paragraphs']
    if len(paragraphs) != 7 or [p['localParagraphIndexZeroBased'] for p in paragraphs] != list(range(7)):
        raise ValueError('Seven bounded opening paragraphs required')
    for paragraph in paragraphs:
        if hashlib.sha256(paragraph['text'].encode()).hexdigest() != paragraph['textSha256']:
            raise ValueError('Mercy opening paragraph checksum mismatch')
    if 'For the last' not in paragraphs[2]['text']:
        raise ValueError('Preserve the transition to the second observation')
    relations = pastoral['synthesisRelations']
    if len(relations) != 4 or {r['id'] for r in relations} != {'SYN-01', 'SYN-02', 'SYN-03', 'SYN-04'}:
        raise ValueError('Four bounded editorial connections required')
    for relation in relations:
        if (relation['kind'] != 'EDITORIAL_CONNECTION_NOT_AUTHORIAL_SYSTEM_OUTLINE'
                or len(relation['refs']) != 2 or not set(relation['refs']) <= set(anchors)
                or not relation['connection'] or not relation['boundary']):
            raise ValueError('Editorial connections cannot claim an authorial system outline')
    boundary_review = plan['boundaryReview']
    if boundary_review['reviewState'] != 'BOUNDED_BIBLIOGRAPHIC_AND_BIOGRAPHICAL_WORDING_DECISIONS':
        raise ValueError('Boundary review must remain a bounded wording decision')
    units = {u['id']: u for u in registry['bibliographyUnits']}
    decisions = boundary_review['unitDecisions']
    if len(decisions) != 12 or {d['id'] for d in decisions} != set(units):
        raise ValueError('Twelve unit decisions,not twelve acquired books,required')
    titles = boundary_review['byteVerifiedTitles']
    printed = {u['id'] for u in units.values() if u['unitType'] == 'PRINTED_OBJECT'}
    if len(titles) != 7 or set(titles) != printed:
        raise ValueError('Exactly seven title transcription records required')
    for d in decisions:
        u = units[d['id']]
        expected_decision = ('USE_IDENTIFIED_OBJECT_WITH_LIMITS' if u['unitType'] == 'PRINTED_OBJECT'
                             else 'DEFER_ACQUISITION_EXCLUDE_UNVERIFIED_EDITION_CLAIMS')
        if (d['unitType'] != u['unitType'] or d['decision'] != expected_decision
                or any(d['sourceStateSnapshot'][k] != u[k] for k in AXES) or not d['readerBoundary']):
            raise ValueError('Unit decision cannot promote source access or rights')
        if u['unitType'] == 'PRINTED_OBJECT':
            t = titles[u['id']]
            source = registry['sources'][u['source']]
            if (t['source'] != u['source'] or t['sourceBytes'] != source['size'] or t['sourceSha256'] != source['sha256']
                    or hashlib.sha256(t['titleText'].encode()).hexdigest() != t['titleTextSha256']
                    or t['selector'] != 'text/front/div[@type=title_page]' or not d['roles'] or not d['dateReading']):
                raise ValueError('Title source pin,selector or imprint reading changed')
    core = {c['id']: c for c in registry['biographicalCoreReview']['items']}
    actions = {'ATTRIBUTED': 'USE_WITH_NAMED_ATTRIBUTION', 'APPROXIMATE': 'KEEP_APPROXIMATION',
               'CONFLICT': 'SHOW_CONFLICT', 'EXCLUDE': 'EXCLUDE_WITHOUT_NEW_EVIDENCE'}
    claims = boundary_review['claimDecisions']
    if len(claims) != 40 or {c['id'] for c in claims} != set(core):
        raise ValueError('All forty canonical wording decisions required')
    for c in claims:
        original = core[c['id']]
        if (c['canonicalRowSha256'] != hashlib.sha256(canonical_bytes(original)).hexdigest()
                or c['originalDisposition'] != original['disposition'] or c['action'] != actions[original['disposition']]
                or any(c[k] != original[k] for k in ('topic', 'safeFormulation', 'excludedClaim', 'boundary', 'refs'))
                or any(c['sourceStateSnapshot'][k] != original[k] for k in AXES)):
            raise ValueError('Biographical decision cannot erase attribution,exclusion or conflict')
    requests = {q['id']: q for q in registry['acquisitionRequests']}
    dispatch = boundary_review['requestDecisions']
    if len(dispatch) != 2 or {q['id'] for q in dispatch} != set(requests):
        raise ValueError('Two request dispositions required')
    for q in dispatch:
        if (q['decision'] != 'KEEP_DRAFT_EXCLUDE_UNACQUIRED_CLAIMS' or q['requestState'] != 'DRAFT_NOT_SENT'
                or q['receipt'] is not None or not q['reason']
                or any(q['sourceStateSnapshot'][k] != requests[q['id']][k] for k in AXES)):
            raise ValueError('Draft request cannot claim dispatch,receipt or source promotion')
    debts = boundary_review['archiveDebts']
    if len(debts) != 7 or {d['id'] for d in debts} != {'WILL', 'FAMILY', 'AUCTION', 'REGISTERS', 'IRELAND', 'POLITICS', 'DEATH'}:
        raise ValueError('Seven explicit archive-boundary decisions required')
    for d in debts:
        if (d['archiveState'] != 'NOT_NEWLY_ACQUIRED' or not d['readerBoundary']
                or not d['claimIds'] or not set(d['claimIds']) <= set(core)):
            raise ValueError('Excluded archive-dependent detail cannot become acquired evidence')
    pairs = {tuple(rule['pair']) for rule in plan['duplicationRules'] if rule.get('rule')}
    if pairs != {('II', 'VI'), ('IV', 'VI'), ('IV', 'VII'), ('III', 'VII'), ('V', 'VIII')}:
        raise ValueError('Missing chapter boundary rule')
    tasks = plan['tasks']
    if [t['id'] for t in tasks] != ['ED-' + str(i).zfill(2) for i in range(1, 9)]:
        raise ValueError('Eight finite work packages required')
    for t in tasks:
        if (t['status'] != ('DONE' if t['id'] == 'ED-01' else 'DONE_BOUNDED' if t['id'] in {'ED-03', 'ED-04', 'ED-05', 'ED-07'} else 'OPEN')
                or not t.get('acceptance') or not t.get('documents') or not set(t['documents']) <= set(IDS)):
            raise ValueError('Task cannot silently claim research/publication work complete')
    reading = plan['principalBookReading']
    extraction = reading['byteVerifiedExtraction']
    source = registry['sources']['A32723']
    if (reading['reviewState'] != 'BOUNDED_ROUTE_AND_FOUR_CONTEXT_REVIEWS'
            or extraction['sourceSha256'] != source['sha256'] or extraction['sourceBytes'] != source['size']
            or any(reading['sourceStateSnapshot'][k] != source[k] for k in AXES)):
        raise ValueError('Book reading cannot change source pins or source axes')
    route = extraction['route']
    if ([d['ordinal'] for d in route] != list(range(1, 15))
            or sum(d['noteElements'] for d in route) != 2337
            or any(not d['heading'] or not d['firstNumberedPage'] or not d['lastNumberedPage'] for d in route)):
        raise ValueError('Fourteen structural discourse rows required,not a full-book read claim')
    expected_cards = {'BOOK-02', 'BOOK-03', 'BOOK-06', 'BOOK-14'}
    contexts = extraction['contexts']
    reviews = reading['manualReviewCards']
    if (len(contexts) != 4 or {c['id'] for c in contexts} != expected_cards
            or len(reviews) != 4 or {c['id'] for c in reviews} != expected_cards):
        raise ValueError('Four explicit book contexts and limited reviews required')
    for context in contexts:
        if len(context['contextWindow']) < 3:
            raise ValueError('Context window too small')
        for paragraph in context['contextWindow']:
            if hashlib.sha256(paragraph['text'].encode()).hexdigest() != paragraph['textSha256']:
                raise ValueError('Stored book paragraph checksum mismatch')
    for review in reviews:
        if (review['authorVoice'] != 'CHARNOCK_BODY' or review['translationState'] != 'NOT_PREPARED'
                or len(review['argumentSteps']) < 3 or not review['limitedConclusion'] or not review['boundary']):
            raise ValueError('Book review cannot hide attribution,bounds or translation status')
    receipt = json.loads((root / plan['baselineReceipt']).read_text())
    manifest = receipt['sourceManifest']
    if hashlib.sha256(canonical_bytes(manifest)).hexdigest() != receipt['sourceManifestSha256']:
        raise ValueError('Historical receipt source manifest modified')
    if receipt['sourceArchiveSha256'] != receipt['destinationSha256Readback']:
        raise ValueError('Historical receipt archive checksum mismatch')
    changed = []
    for name, meta in manifest['files'].items():
        if name.startswith('xml/'):
            source = registry['sources'][Path(name).stem]
            if meta['sha256'] != source['sha256'] or meta['bytes'] != source['size']:
                raise ValueError('Baseline source pin changed')
            continue  # XML bytes remain external;this audit is not an XML replay.
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('Unsafe baseline manifest path')
        raw = path.read_bytes()
        if len(raw) != meta['bytes'] or hashlib.sha256(raw).hexdigest() != meta['sha256']:
            changed.append(name)
    expected = ['БИОГРАФИИ/Стивен Чарнок/00_README_AND_NAVIGATION.md',
                'БИОГРАФИИ/Стивен Чарнок/16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN.md']
    if sorted(plan['expectedChangedPacketMembers']) != sorted(expected) or sorted(changed) != sorted(expected):
        raise ValueError('Unexpected changes to the preserved source packet')
    architecture = (root / expected[1]).read_text()
    if '## 21.' not in architecture or any(d['title'] not in architecture for d in documents):
        raise ValueError('Human architecture does not contain the ten current passports')
    return dict(state='EDITORIAL_BLUEPRINT_WITH_OPEN_WORK', documents=10, mainParts=8,
                registeredReferences=len(used), dossierCaseCandidates=len(cases),
                studyCards=len(cards), freshlyReplayedScriptureWindows=4, selectedScriptureContextsVerified=5, theologicalRows=len(matrix),
                bookRoutes=len(route), bookContextReviews=len(reviews),
                **mourning_complete_report, **mourning_report, **pardon_report, **pardon_opening_report, **pardon_complete_report, **stability_report, **stability_complete_report, **fifth_november_report, **prayer_report, **thoughts_report, **thoughts_complete_report, **cartesian_report, **folio_apparatus_report, **copyist_transmission_report, **mercy_distinctions_report, **reception_locus_report, **scripture_purpose_report, **childbearing_report, **opening_report, **continuation_report, **doctrinal_report, **political_report, **reference_report, **routing_report, **editorial_voice_report, **editorial_translation_report, **authorial_translation_report, **atheism_report, **enmity_report, **death_witness_report, earlierWorkingTranslationDrafts=translation_drafts, workingTranslationDrafts=translation_drafts + editorial_translation_report['editorialWorkingTranslationDrafts'] + authorial_translation_report['authorialWorkingTranslationDrafts'] + atheism_report['atheismWorkingTranslationDrafts'] + enmity_report['enmityWorkingTranslationDrafts'], independentlyReviewedTranslations=0,
                titleTranscriptions=len(titles), unitDecisions=len(decisions), biographicalWordingDecisions=len(claims),
                sourceUseMicroReadings=micro_readings, inheritedCounterpartGlosses=inherited_glosses,
                sourceUsePairs=len(source_cases), pastoralContexts=7, selectedWorkProfiles=5, mercyOpeningParagraphs=7, synthesisConnections=4, titleState=documents[3]["titleState"],
                completedPackages=[t['id'] for t in tasks if t['status'].startswith('DONE')], openPackages=[t['id'] for t in tasks if t['status'] == 'OPEN'],
                targetWords=[sum(d['targetWords'][i] for d in documents) for i in (0, 1)],
                publicationState='BLOCKED', historicalReceiptMatchesCurrentTree=False,
                changedPacketMembers=sorted(changed), currentRevisionCustody='NOT_REVERIFIED',
                boundary='Saved receipt metadata/source pins checked;not remote authentication or fresh XML-byte replay')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=ROOT / PLAN)
    args = parser.parse_args()
    try:
        report = check(json.loads(args.plan.read_text()))
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
