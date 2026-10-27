#!/usr/bin/env python3
"""Audit working editorial/authorial translations;not linguistic or publication approval."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_editorial_voice import extract
from audit_charnock_handoff import canonical_bytes
from audit_charnock_translation_contexts import has_explicit_tcp_text_waiver

ROOT = Path(__file__).resolve().parents[1]
INDICES = {'Q-04': 2, 'Q-05': 0, 'Q-10': 2}


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def selected_span(qid, body):
    if qid == 'Q-04':
        return body[body.index('Though he make'):]
    if qid == 'Q-05':
        return body[:body.index(' In the Epistle')]
    return body[:body.index(' Though he make')]


def licence_from_xml(path):
    root = ET.fromstring(path.read_bytes())
    found = root.findall('.//' + NS + 'teiHeader//' + NS + 'availability')
    if len(found) != 1:
        raise ValueError('One explicit TCP availability statement required')
    statement = plain(found[0])
    if not has_explicit_tcp_text_waiver(statement):
        raise ValueError('TCP text waiver required;not image or translation approval')
    return dict(statement=statement, statementSha256=digest(statement),
                refTargets=[n.get('target') for n in found[0].iter(NS + 'ref')],
                scope='TCP encoded text only;not page images,autographs or external editions')


def check_review(plan, registry):
    review = plan['editorialTranslationReview']
    data = plan['editorialVoiceReview']['byteVerifiedExtraction']
    source = registry['sources']['A32723']
    if (review['reviewState'] != 'THREE_EDITORIAL_WORKING_TRANSLATIONS'
            or review['sourceReplay'] != dict(source='A32723', sourceSha256=source['sha256'], sourceBytes=source['size'])
            or review['independentReviewState'] != 'NOT_PERFORMED' or review['publicationApproval'] is not False
            or 'HISTORICAL_ENGLISH_CONTEXT_REVIEW_BEFORE_TRANSLATION' not in plan['editorialVoiceReview']['quotationFollowUpsScope']):
        raise ValueError('Editorial drafts cannot approve independent review or rewrite earlier states')
    licence = review['licence']
    if (digest(licence['statement']) != licence['statementSha256']
            or not has_explicit_tcp_text_waiver(licence['statement'])
            or licence['scope'] != 'TCP encoded text only;not page images,autographs or external editions'):
        raise ValueError('Text licence must not become image or translation approval')
    items = review['items']
    if len(items) != 3 or {r['quotationId'] for r in items} != set(INDICES):
        raise ValueError('Three distinct editorial quotation drafts required')
    old = {q['id']: q for q in registry['researchPreparationReview']['quotationPlan']}
    for row in [review] + items:
        if (row['evidenceClass'] != 'C' or row['accessState'] != 'FULL_OBJECT_VERIFIED'
                or row['locatorState'] != 'EXACT_LOCATOR_VERIFIED' or row['rightsState'] != 'RIGHTS_UNKNOWN'
                or row['publicationState'] != 'BLOCKED'
                or set(row['holds']) != {'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Working decisions must retain their own axes and HOLDs')
    terms = 0
    for row in items:
        qid = row['quotationId']
        para = data['prefaceParagraphs'][INDICES[qid]]
        if (row['id'] != 'TR-' + qid or row['source'] != 'A32723' or row['sourceSha256'] != source['sha256']
                or row['canonicalRowSha256'] != hashlib.sha256(canonical_bytes(old[qid])).hexdigest()
                or row['paragraphIndex'] != INDICES[qid] or row['contextSha256'] != para['textSha256']
                or digest(para['text']) != para['textSha256']
                or row['quoteText'] != selected_span(qid, para['text'])
                or old[qid]['quoteText'] not in row['quoteText'] or digest(row['quoteText']) != row['quoteTextSha256']
                or row['quoteTeiPages'] != [None] or row['locator'] != dict(section=data['prefaceHeading'],
                    localDirectParagraphIndexZeroBased=INDICES[qid],
                    scheme='Direct p in front preface;zero-based;unnumbered;not a printed page number')
                or row['voice'] != 'VEEL_ADAMS_EDITORIAL'):
            raise ValueError('Editorial span,voice,canonical row or unnumbered locator changed')
        if (not row['russianDraft'] or digest(row['russianDraft']) != row['russianDraftSha256']
                or row['translationState'] != 'WORKING_DRAFT_NOT_INDEPENDENTLY_REVIEWED'
                or row['translationMethod'] != 'AI_ASSISTED_RESEARCH_DRAFT'
                or row['independentReview'] != dict(state='NOT_PERFORMED',reviewer=None,reviewedTranslationSha256=None)
                or row['sourceTextRights'] != 'CC0_TCP_ENCODED_TEXT_ONLY'
                or row['imageRights'] != 'NOT_REVIEWED_NOT_INCLUDED' or row['publicationApproval'] is not False
                or not row['boundary']):
            raise ValueError('Working translation integrity,review and rights boundary required')
        if len(row['termDecisions']) != {'Q-04':3,'Q-05':2,'Q-10':4}[qid]:
            raise ValueError('Nine bounded term decisions required')
        for term in row['termDecisions']:
            if (not term['englishSpan'] or term['englishSpan'] not in row['quoteText']
                    or not term['russianRendering'] or term['russianRendering'] not in row['russianDraft']
                    or not term['reason']):
                raise ValueError('Term decision must link actual English and Russian spans')
            terms += 1
    if next(t for t in plan['tasks'] if t['id'] == 'ED-06')['status'] != 'OPEN':
        raise ValueError('Unreviewed translations cannot close ED-06')
    return dict(editorialWorkingTranslationDrafts=3, editorialTranslationTermDecisions=terms)



AUTHORIAL = {'Q-06': ('freshStudyReview','TXT-18'),
             'Q-07': ('doctrinalDistinctionReview','TXT-06')}


def check_authorial_review(plan, registry):
    """Integrity of two working translations;does not certify Russian semantics."""
    review = plan['authorialTranslationReview']
    if (review['reviewState'] != 'TWO_AUTHORIAL_WORKING_TRANSLATIONS'
            or review['independentReviewState'] != 'NOT_PERFORMED'
            or review['publicationApproval'] is not False
            or review['omittedPolemicRetainedInContext'] is not True
            or 'HISTORICAL_ENGLISH_CONTEXT_REVIEW_BEFORE_TRANSLATION' not in plan['freshStudyReview']['quotationFollowUpScope']):
        raise ValueError('Authorial drafts cannot approve release or erase omitted polemic')
    if set(review['licences']) != {'A32723','A32724'}:
        raise ValueError('Two TCP text licences required')
    for licence in review['licences'].values():
        if (digest(licence['statement']) != licence['statementSha256']
                or not has_explicit_tcp_text_waiver(licence['statement'])
                or licence['scope'] != 'TCP encoded text only;not page images,autographs or external editions'):
            raise ValueError('Authorial text waiver cannot approve images or translations')
    items = review['items']
    if len(items) != 2 or {r['quotationId'] for r in items} != set(AUTHORIAL):
        raise ValueError('Two distinct authorial drafts required')
    for row in [review] + items:
        if (row['evidenceClass'] != 'C' or row['accessState'] != 'FULL_OBJECT_VERIFIED'
                or row['locatorState'] != 'EXACT_LOCATOR_VERIFIED' or row['rightsState'] != 'RIGHTS_UNKNOWN'
                or row['publicationState'] != 'BLOCKED'
                or set(row['holds']) != {'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Authorial translation decision axes/HOLDs must remain distinct from source')
    old = {q['id']:q for q in registry['researchPreparationReview']['quotationPlan']}
    for row in items:
        qid = row['quotationId'];owner,ref = AUTHORIAL[qid]
        ctx = plan[owner]['byteVerifiedContexts'][ref]
        para = next(x for x in ctx['contextWindow'] if x['paragraphIndexZeroBased'] == ctx['selectedParagraphIndexZeroBased'])
        expected = para['text'].split(' The Jews ridiculously interpret',1)[0] if qid == 'Q-06' else para['text']
        source = registry['sources'][ctx['source']]
        if (row['id'] != 'TR-'+qid or row['relatedRef'] != ref or row['contextOwner'] != owner
                or row['source'] != ctx['source'] or row['sourceSha256'] != source['sha256']
                or ctx['sourceSha256'] != source['sha256'] or ctx['sourceBytes'] != source['size']
                or row['contextSha256'] != para['textSha256'] or digest(para['text']) != para['textSha256']
                or row['canonicalRowSha256'] != hashlib.sha256(canonical_bytes(old[qid])).hexdigest()
                or row['quoteText'] != expected or digest(expected) != row['quoteTextSha256']
                or old[qid]['quoteText'] not in expected or row['quoteTeiPages'] != ctx['probeTeiPages']
                or row['locator'] != dict(section=ctx['sectionHeading'],globalNonNestedParagraphIndexZeroBased=ctx['selectedParagraphIndexZeroBased'],paragraphStartTeiPage=ctx['paragraphStartTeiPage'])
                or row['voice'] != 'CHARNOCK_BODY' or row['fullParagraphTranslated'] is not (qid == 'Q-07')
                or not row['omittedContextBoundary']):
            raise ValueError('Authorial context,selection,voice or locator changed')
        if qid == 'Q-06' and ('The Jews ridiculously interpret' not in para['text'] or 'Stable for Mahomet' not in para['text']):
            raise ValueError('Omitted polemic must remain in full context')
        if (not row['russianDraft'] or digest(row['russianDraft']) != row['russianDraftSha256']
                or row['translationState'] != 'WORKING_DRAFT_NOT_INDEPENDENTLY_REVIEWED'
                or row['translationMethod'] != 'AI_ASSISTED_RESEARCH_DRAFT'
                or row['independentReview'] != dict(state='NOT_PERFORMED',reviewer=None,reviewedTranslationSha256=None)
                or row['publicationApproval'] is not False or row['sourceTextRights'] != 'CC0_TCP_ENCODED_TEXT_ONLY'
                or row['imageRights'] != 'NOT_REVIEWED_NOT_INCLUDED'):
            raise ValueError('Authorial draft integrity and unreviewed state required')
        if len(row['termDecisions']) != 3 or any(not t['englishSpan'] or t['englishSpan'] not in expected
                or not t['russianRendering'] or t['russianRendering'] not in row['russianDraft'] or not t['reason'] for t in row['termDecisions']):
            raise ValueError('Six actual English/Russian term links required')
    if next(t for t in plan['tasks'] if t['id'] == 'ED-06')['status'] != 'OPEN':
        raise ValueError('Authorial working drafts cannot close ED-06')
    return dict(authorialWorkingTranslationDrafts=2,authorialTranslationTermDecisions=6)


def replay_authorial(directory,plan,registry):
    from audit_charnock_pastoral_contexts import extract as extract_contexts, THEOLOGY_AFTER
    for owner,ref in AUTHORIAL.values():
        actual = extract_contexts(directory,registry,refs=(ref,),window_after=THEOLOGY_AFTER)[ref]
        if actual != plan[owner]['byteVerifiedContexts'][ref]:
            raise ValueError('Authorial context differs from pinned XML')
    for source,licence in plan['authorialTranslationReview']['licences'].items():
        if licence_from_xml(directory/(source+'.xml')) != licence:
            raise ValueError('Authorial licence differs from pinned XML')


def check_atheism_review(plan,registry):
    """Seven historical paragraphs,not a diagnostic classification of modern people."""
    r=plan['atheismReview'];ctx=r['byteVerifiedContext'];tr=r['translation']
    src=registry['sources']['A32723']
    if (r['reviewState']!='SEVEN_PRACTICAL_ATHEISM_PARAGRAPHS_ONE_WORKING_TRANSLATION'
            or any(r[k] is not False for k in ('wholeDiscourseRead','modernCollectiveVerdictApproved','publicationApproval'))
            or r['independentReviewState']!='NOT_PERFORMED'
            or ctx['source']!='A32723' or ctx['sourceSha256']!=src['sha256'] or ctx['sourceBytes']!=src['size']
            or ctx['selectedParagraphIndexZeroBased']!=244 or ctx['probeTeiPages']!=['47']
            or ctx['rangeOverrideStartEndInclusive']!=[242,248] or ctx['anchorProbeInsideWindow'] is not True
            or [x['paragraphIndexZeroBased'] for x in ctx['contextWindow']]!=list(range(242,249))):
        raise ValueError('Seven bounded atheism paragraphs required;not whole discourse or modern verdict')
    paras={x['paragraphIndexZeroBased']:x for x in ctx['contextWindow']}
    if any(digest(x['text'])!=x['textSha256'] or x['startTeiPage']!='47' for x in paras.values()):
        raise ValueError('Atheism context hash/page differs')
    notes=r['marginalNotes']
    if (len(notes)!=2 or [n['parentParagraphIndexZeroBased'] for n in notes]!=[244,246]
            or notes[0]['text']!='Job. 1.5.' or 'in non-Latin alphabet' not in notes[1]['text']
            or any(n['teiPage']!='47' for n in notes)):
        raise ValueError('Keep Job note and unreconstructed Chaldean-script gap')
    licence=r['licence']
    if (digest(licence['statement'])!=licence['statementSha256']
            or not has_explicit_tcp_text_waiver(licence['statement'])
            or licence['scope']!='TCP encoded text only;not page images,autographs or external editions'):
        raise ValueError('Atheism text waiver is not image or translation approval')
    obs=r['observations']
    if len(obs)!=7 or [x['paragraphIndexZeroBased'] for x in obs]!=list(range(242,249)):
        raise ValueError('Seven bounded observations required')
    for row in [r,tr]+obs:
        if (row['evidenceClass']!='C' or row['accessState']!='FULL_OBJECT_VERIFIED'
                or row['locatorState']!='EXACT_LOCATOR_VERIFIED' or row['rightsState']!='RIGHTS_UNKNOWN'
                or row['publicationState']!='BLOCKED'
                or set(row['holds'])!={'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Atheism research decisions must retain independent axes/HOLDs')
    for row in obs:
        if (not row['englishSpan'] or row['englishSpan'] not in paras[row['paragraphIndexZeroBased']]['text']
                or digest(row['englishSpan'])!=row['englishSpanSha256']
                or not row['observation'] or not row['prohibitedInference']):
            raise ValueError('Atheism observation needs actual span and inference limit')
    if ('in some sence all unbelievers may be termed Atheists' not in paras[247]['text']
            or 'But this is beyond the intended scope' not in paras[248]['text']
            or 'Yet this is deducible from it.' not in paras[248]['text']):
        raise ValueError('Retain both broad historical usage and scope qualification')
    q=next(x for x in registry['researchPreparationReview']['quotationPlan'] if x['id']=='Q-08')
    if (tr['id']!='TR-Q-08' or tr['quotationId']!='Q-08' or tr['voice']!='CHARNOCK_BODY'
            or tr['canonicalRowSha256']!=hashlib.sha256(canonical_bytes(q)).hexdigest()
            or tr['quoteText']!=paras[244]['text'] or q['quoteText'] not in tr['quoteText']
            or digest(tr['quoteText'])!=tr['quoteTextSha256'] or tr['contextSha256']!=paras[244]['textSha256']
            or tr['locator']!=dict(section=ctx['sectionHeading'],teiPages=['47'],globalNonNestedParagraphIndexZeroBased=244)
            or not tr['russianDraft'] or digest(tr['russianDraft'])!=tr['russianDraftSha256']
            or tr['translationState']!='WORKING_DRAFT_NOT_INDEPENDENTLY_REVIEWED'
            or tr['translationMethod']!='AI_ASSISTED_RESEARCH_DRAFT'
            or tr['independentReview']!=dict(state='NOT_PERFORMED',reviewer=None,reviewedTranslationSha256=None)
            or tr['publicationApproval'] is not False or tr['sourceTextRights']!='CC0_TCP_ENCODED_TEXT_ONLY'
            or tr['imageRights']!='NOT_REVIEWED_NOT_INCLUDED'):
        raise ValueError('Atheism full-paragraph working translation integrity/voice/limits required')
    if len(tr['termDecisions'])!=3 or any(not t['englishSpan'] or t['englishSpan'] not in tr['quoteText']
            or not t['russianRendering'] or t['russianRendering'] not in tr['russianDraft'] or not t['reason'] for t in tr['termDecisions']):
        raise ValueError('Three linked atheism term decisions required')
    if next(t for t in plan['tasks'] if t['id']=='ED-06')['status']!='OPEN':
        raise ValueError('Atheism draft cannot close ED-06')
    return dict(atheismContextParagraphs=7,atheismWorkingTranslationDrafts=1,atheismObservations=7)


def replay_atheism(directory,plan,registry):
    from audit_charnock_pastoral_contexts import extract as extract_contexts,source_structure
    r=plan['atheismReview']
    actual=extract_contexts(directory,registry,refs=('TXT-05',),paragraph_ranges={'TXT-05':(242,248)})['TXT-05']
    if actual!=r['byteVerifiedContext']:
        raise ValueError('Atheism context differs from actual pinned XML')
    _,_,_,pages,paras=source_structure(directory,registry,'A32723')
    notes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split()))
           for i in range(242,249) for n in paras[i].iter(NS+'note')]
    if notes!=r['marginalNotes'] or licence_from_xml(directory/'A32723.xml')!=r['licence']:
        raise ValueError('Atheism note or licence differs from actual XML')


def extract_enmity(directory,registry):
    """Pinned 1699 editorial preface and one bounded body window;not autographs."""
    from audit_charnock_pastoral_contexts import source_structure
    _,root,parents,pages,paras=source_structure(directory,registry,'B20167')
    src=registry['sources']['B20167']
    def record(i):
        node=paras[i];text=plain(node)
        return dict(paragraphIndexZeroBased=i,startTeiPage=pages[node],text=text,textSha256=digest(text))
    div=paras[9]
    while div in parents and div.tag!=NS+'div':div=parents[div]
    return dict(source='B20167',sourceBytes=src['size'],sourceSha256=src['sha256'],
                editorialHeading=plain(div.find(NS+'head')),
                signatures=[plain(n) for n in div.iter(NS+'signed')],
                editorialParagraphs=[record(i) for i in range(6,10)],
                bodyParagraphs=[record(i) for i in range(40,74)],
                marginalNotes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split()))
                    for i in list(range(6,10))+list(range(40,74)) for n in paras[i].iter(NS+'note')],
                licence=licence_from_xml(directory/'B20167.xml'),
                normalization='Whitespace/long-s;note/fw bodies omitted,tails retained')


def check_enmity_review(plan,registry):
    r=plan['enmityReview'];reading=r['byteVerifiedReading'];src=registry['sources']['B20167']
    if (r['reviewState']!='BOUNDED_NATURE_AND_EDITORIAL_PROVENANCE'
            or any(r[k] is not False for k in ('wholeDiscourseRead','autographsVerified','preachingDateEstablished','publicationApproval'))
            or r['independentReviewState']!='NOT_PERFORMED'
            or reading['source']!='B20167' or reading['sourceSha256']!=src['sha256'] or reading['sourceBytes']!=src['size']
            or [x['paragraphIndexZeroBased'] for x in reading['editorialParagraphs']]!=list(range(6,10))
            or [x['paragraphIndexZeroBased'] for x in reading['bodyParagraphs']]!=list(range(40,74))
            or not any('Edw. Veel.' in t for t in reading['signatures'])):
        raise ValueError('Bounded Enmity reading cannot verify autographs,date or whole discourse')
    paras={x['paragraphIndexZeroBased']:x for x in reading['editorialParagraphs']+reading['bodyParagraphs']}
    if any(digest(p['text'])!=p['textSha256'] for p in paras.values()):
        raise ValueError('Enmity paragraph hash differs')
    licence=reading['licence']
    if (digest(licence['statement'])!=licence['statementSha256'] or not has_explicit_tcp_text_waiver(licence['statement'])
            or licence['scope']!='TCP encoded text only;not page images,autographs or external editions'):
        raise ValueError('Enmity encoded-text licence only')
    obs=r['observations'];trs=r['translations']
    if (len(obs)!=10 or [o['paragraphIndexZeroBased'] for o in obs]!=[43,48,49,53,57,62,68,71,72,9]
            or len(trs)!=2 or {t['quotationId'] for t in trs}!={'Q-12','Q-16'}):
        raise ValueError('Ten observations and two Enmity translations required')
    for row in [r]+obs+trs:
        if (row['evidenceClass']!='C' or row['accessState']!='FULL_OBJECT_VERIFIED'
                or row['locatorState']!='EXACT_LOCATOR_VERIFIED' or row['rightsState']!='RIGHTS_UNKNOWN'
                or row['publicationState']!='BLOCKED'
                or set(row['holds'])!={'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Enmity decisions need independent axes and HOLDs')
    for o in obs:
        if (not o['englishSpan'] or o['englishSpan'] not in paras[o['paragraphIndexZeroBased']]['text']
                or digest(o['englishSpan'])!=o['englishSpanSha256'] or not o['observation'] or not o['prohibitedInference']
                or o['voice']!=('VEEL_EDITORIAL' if o['paragraphIndexZeroBased']==9 else 'CHARNOCK_BODY')):
            raise ValueError('Enmity observation needs actual span,voice and inference limit')
    for t in trs:
        qid=t['quotationId'];i=53 if qid=='Q-12' else 9;p=paras[i]
        expected=p['text'] if i==53 else p['text'].split(' And in it, if the Reader',1)[0]
        old=next(q for q in registry['researchPreparationReview']['quotationPlan'] if q['id']==qid)
        if (t['id']!='TR-'+qid or t['source']!='B20167' or t['sourceSha256']!=src['sha256']
                or t['canonicalRowSha256']!=hashlib.sha256(canonical_bytes(old)).hexdigest()
                or t['contextSha256']!=p['textSha256'] or t['quoteText']!=expected or old['quoteText'] not in expected
                or digest(expected)!=t['quoteTextSha256'] or t['voice']!=('CHARNOCK_BODY' if i==53 else 'VEEL_EDITORIAL')
                or t['locator']!=dict(globalNonNestedParagraphIndexZeroBased=i,teiPages=[p['startTeiPage']])
                or t['fullParagraphTranslated'] is not (i==53)
                or not t['russianDraft'] or digest(t['russianDraft'])!=t['russianDraftSha256']
                or t['translationState']!='WORKING_DRAFT_NOT_INDEPENDENTLY_REVIEWED'
                or t['translationMethod']!='AI_ASSISTED_RESEARCH_DRAFT'
                or t['independentReview']!=dict(state='NOT_PERFORMED',reviewer=None,reviewedTranslationSha256=None)
                or t['publicationApproval'] is not False or t['sourceTextRights']!='CC0_TCP_ENCODED_TEXT_ONLY'
                or t['imageRights']!='NOT_REVIEWED_NOT_INCLUDED'):
            raise ValueError('Enmity source,span,translation integrity or editorial voice differs')
        if len(t['termDecisions'])!=(2 if i==53 else 3) or any(not x['englishSpan'] or x['englishSpan'] not in expected
                or not x['russianRendering'] or x['russianRendering'] not in t['russianDraft'] or not x['reason'] for x in t['termDecisions']):
            raise ValueError('Five actual Enmity term links required')
    if next(t for t in plan['tasks'] if t['id']=='ED-06')['status']!='OPEN':
        raise ValueError('Enmity drafts cannot close ED-06')
    return dict(enmityBodyParagraphs=34,enmityEditorialParagraphs=4,enmityObservations=10,enmityWorkingTranslationDrafts=2)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml',type=Path,help='XML file,or pinned XML directory with --authorial/--atheism/--enmity')
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--authorial',action='store_true')
    modes.add_argument('--atheism',action='store_true')
    modes.add_argument('--enmity',action='store_true')
    args = parser.parse_args()
    try:
        plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        registry = json.loads((ROOT / 'data/charnock-biographical-anchors-v1.json').read_text())
        if args.enmity:
            report=check_enmity_review(plan,registry)
            if extract_enmity(args.xml,registry)!=plan['enmityReview']['byteVerifiedReading']:
                raise ValueError('Enmity reading differs from actual pinned XML')
            print(json.dumps(report))
            print('Enmity text/licence replay: PASS;not autographs,preaching date or translation approval')
            return
        if args.atheism:
            report=check_atheism_review(plan,registry)
            replay_atheism(args.xml,plan,registry)
            print(json.dumps(report))
            print('Atheism context/notes/licence: PASS;not independent translation review or modern verdict')
            return
        if args.authorial:
            report = check_authorial_review(plan,registry)
            replay_authorial(args.xml,plan,registry)
            print(json.dumps(report))
            print('Authorial context/licence replay: PASS;not independent translation review or release')
            return
        report = check_review(plan,registry)
        if extract(args.xml,registry) != plan['editorialVoiceReview']['byteVerifiedExtraction']:
            raise ValueError('Stored editorial context differs from pinned XML')
        if licence_from_xml(args.xml) != plan['editorialTranslationReview']['licence']:
            raise ValueError('Stored text licence differs from pinned XML')
        print(json.dumps(report))
        print('Pinned context/licence replay: PASS;not independent translation review or publication approval')
    except (ValueError,KeyError,OSError,ET.ParseError) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__ == '__main__':
    main()
