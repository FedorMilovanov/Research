#!/usr/bin/env python3
"""Selected Mercy opening and complete final caution; not full-treatise or publication approval."""
import argparse
import json
from pathlib import Path
from audit_charnock_book_route import NS, plain
from audit_charnock_pastoral_contexts import ROOT, source_structure
from audit_charnock_thoughts import digest, HOLDS

KEY='mercyDoctrineFollowUp'
POSITIONS=list(range(683,712))+list(range(960,976))
FALSE_FLAGS=('wholeTreatiseRead','lostFirstDoctrineRecovered','allSinnersAutomaticallyPardoned',
             'sinNecessitatesGrace','originalForeignSourcesVerified','modernGroupBlameApproved',
             'completeOrdoSalutisEstablished','publicationApproval')


def extract(directory,registry):
    _,root,parents,pages,paragraphs=source_structure(directory,registry,'B20167')
    division=next(d for d in root.iter(NS+'div') if d.find(NS+'head') is not None and plain(d.find(NS+'head'))=='Chiefest Sinners Objects of Choicest Mercy.')
    def row(i):
        p=paragraphs[i];text=plain(p)
        return dict(paragraphIndexZeroBased=i,startTeiPage=pages[p],text=text,textSha256=digest(text))
    for i in POSITIONS:
        node=paragraphs[i]
        while node in parents and node is not division:node=parents[node]
        if node is not division:raise ValueError('Selected paragraph outside Mercy sermon')
    caution=next(d for d in division.iter(NS+'div') if d.find(NS+'head') is not None and plain(d.find(NS+'head'))=='ƲSE 4. Caution.')
    source=registry['sources']['B20167']
    return dict(source='B20167',sourceSha256=source['sha256'],sourceBytes=source['size'],
                heading=plain(division.find(NS+'head')),epigraph=plain(division.find(NS+'epigraph')),
                cautionHeading=plain(caution.find(NS+'head')),
                cautionParagraphIndices=[paragraphs.index(p) for p in caution.iter(NS+'p')],
                paragraphs=[row(i) for i in POSITIONS],
                marginalNotes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split())) for i in POSITIONS for n in paragraphs[i].iter(NS+'note')],
                contextBeforeCaution=row(959),nextOpeningParagraph=row(712),nextPublisherParagraph=row(976))


def extract_election_context(directory,registry):
    _,_,_,pages,paragraphs=source_structure(directory,registry,'A32723')
    rows=[]
    for i in [2751,2752,2753,2755,2756]:
        text=plain(paragraphs[i]);rows.append(dict(paragraphIndexZeroBased=i,startTeiPage=pages[paragraphs[i]],text=text,textSha256=digest(text)))
    return dict(source='A32723',sourceSha256=registry['sources']['A32723']['sha256'],paragraphs=rows,
                existingDailleParagraph=dict(paragraphIndexZeroBased=2754,textSha256=digest(plain(paragraphs[2754]))),
                marginalNotes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split())) for i in range(2751,2757) for n in paragraphs[i].iter(NS+'note')])


def check_election_context(plan,registry):
    c=plan[KEY]['electionApplicationCrossCheck'];reading=c['byteVerifiedContext']
    if (c['reviewState']!='AUTHOR_DISTINGUISHES_ELECTION_AND_FINAL_JUDGMENT_NOT_COMPLETE_ORDO'
            or any(c[k] is not False for k in ['wholeDiscourseRead','completeOrdoSalutisEstablished',
                 'repentanceMeritsElection','humanArbitraryRuleApproved','dailleOriginalReacquired',
                 'foreignCaseClosed','independentReview','publicationApproval'])):
        raise ValueError('Cross-check is not full system, acquired foreign counterpart or publication approval')
    if reading['source']!='A32723' or reading['sourceSha256']!=registry['sources']['A32723']['sha256']:
        raise ValueError('Election source pin changed')
    rows=reading['paragraphs']
    if [p['paragraphIndexZeroBased'] for p in rows]!=[2751,2752,2753,2755,2756]:
        raise ValueError('Keep the expanded immediate context and the referenced central paragraph')
    inherited=next(c for c in plan['sourceUseCases'] if c['id']=='CASE-DAILLE')['charnockSide']['byteVerifiedContext']
    if reading['existingDailleParagraph']!=dict(paragraphIndexZeroBased=2754,textSha256=inherited['bodyParagraphSha256']):
        raise ValueError('Historical Daillé source-side paragraph remains unchanged')
    if any(digest(p['text'])!=p['textSha256'] for p in rows):raise ValueError('Election context hash mismatch')
    if reading['marginalNotes']!=[dict(parentParagraphIndexZeroBased=2752,teiPage='728',text='Amyrald. dissert. p. 101, 102.'),dict(parentParagraphIndexZeroBased=2754,teiPage='729',text='Dalle in loc.')]:
        raise ValueError('Preserve separate Amyrald and Dalle note placement')
    if KEY not in plan['documents'][4]['supplementaryContextReadings']:raise ValueError('PartIV cross-reference missing')
    texts={'E'+str(p['paragraphIndexZeroBased']):p['text'] for p in rows}
    texts['E2754']=inherited['bodyParagraph']
    texts.update({'M'+str(p['paragraphIndexZeroBased']):p['text'] for p in plan[KEY]['byteVerifiedReading']['paragraphs']})
    if [o['id'] for o in c['observations']]!=[f'EA{i:02}' for i in range(1,8)]:
        raise ValueError('Seven source-grounded cross-context decisions required')
    for o in c['observations']:
        if not o['finding'] or not o['limit'] or not o['spans']:
            raise ValueError('Cross-context observation needs limits')
        for span in o['spans']:
            if not span['text'] or span['text'] not in texts[span['source']] or digest(span['text'])!=span['sha256']:
                raise ValueError('Cross-context claim must cite actual authorial words')
    search=c['counterpartSearchFollowUp']
    if search['targetForeignOriginalAcquired'] is not False or search['globalAbsenceProven'] is not False or not search['queries']:
        raise ValueError('Negative bounded searches do not close foreign cases')
    if not c['limitedConclusion'] or not c['scope']:raise ValueError('Local distinctions are not full doctrinal harmonisation')
    return dict(electionAndFinalJudgmentDistinguished=True,electionApplicationCrossObservations=7,completeOrdoSalutisEstablished=False)


def check_review(plan,registry):
    review=plan[KEY];data=review['byteVerifiedReading'];source=registry['sources']['B20167']
    if (review['reviewState']!='AUTHOR_SECOND_OBSERVATION_AND_FINAL_CAUTION_SELECTED_NOT_WHOLE'
            or any(review[f] is not False for f in FALSE_FLAGS)):
        raise ValueError('Selected authorial corroboration is not lost-text recovery or an unconditional promise')
    if (data['source']!='B20167' or data['sourceSha256']!=source['sha256'] or data['sourceBytes']!=source['size']
            or data['heading']!='Chiefest Sinners Objects of Choicest Mercy.'
            or data['cautionHeading']!='ƲSE 4. Caution.' or data['cautionParagraphIndices']!=list(range(960,976))):
        raise ValueError('Preserve sermon identity, source pin and complete final caution scope')
    rows=data['paragraphs']
    if [r['paragraphIndexZeroBased'] for r in rows]!=POSITIONS:
        raise ValueError('Two discontinuous ranges:29 opening and16 final paragraphs')
    for key,index in [('contextBeforeCaution',959),('nextOpeningParagraph',712),('nextPublisherParagraph',976)]:
        if data[key]['paragraphIndexZeroBased']!=index:raise ValueError('Keep the gap and publisher boundary explicit')
    if any(digest(r['text'])!=r['textSha256'] for r in rows+[data[k] for k in ['contextBeforeCaution','nextOpeningParagraph','nextPublisherParagraph']]):
        raise ValueError('Mercy paragraph text hash mismatch')
    old=plan['pastoralReview']['mercyOpeningReview']['byteVerifiedOpening']['paragraphs']
    if len(old)!=7 or any(r['text']!=o['text'] or r['textSha256']!=o['textSha256'] for r,o in zip(rows[:7],old)):
        raise ValueError('The seven-paragraph historical opening remains unchanged')
    if (rows[1]['text']!='2. God doth often make the chiefest Sinners Objects of his choicest Mercy.'
            or rows[2]['text']!='For the last, That God doth so.'
            or data['marginalNotes']!=[dict(parentParagraphIndexZeroBased=961,teiPage='143',text='Hierony in Vol. 1. p. 114. e.')]):
        raise ValueError('Keep often/latter transition and the unverified Jerome pointer')
    texts={str(r['paragraphIndexZeroBased']):r['text'] for r in rows+[data['contextBeforeCaution']]}
    observations=review['observations']
    if [o['id'] for o in observations]!=[f'MD{i:02}' for i in range(1,15)]:raise ValueError('Fourteen bounded authorial decisions required')
    for o in observations:
        if (not o['finding'] or not o['prohibitedInference'] or not o['spans']
                or any(not s['text'] or s['text'] not in texts[s['paragraph']] or digest(s['text'])!=s['sha256'] for s in o['spans'])):
            raise ValueError('Exact authorial spans, not editorial paraphrases, required')
    if (review['evidenceClass']!='C' or review['accessState']!='FULL_OBJECT_VERIFIED'
            or review['locatorState']!='EXACT_LOCATOR_VERIFIED' or review['rightsState']!='RIGHTS_UNKNOWN'
            or review['publicationState']!='BLOCKED' or set(review['holds'])!=HOLDS
            or KEY not in plan['documents'][7]['supplementaryContextReadings']):
        raise ValueError('Preserve evidence axes, HOLD and partVII ownership')
    return dict(mercySelectedParagraphs=45,mercyAdditionalSelectedParagraphs=38,
                mercyFinalCautionParagraphs=16,mercyAuthorialObservations=14,mercyWholeTreatiseRead=False,**check_election_context(plan,registry))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text());registry=json.loads((ROOT/plan['baselineRegistry']).read_text());reading=extract(args.directory,registry)
        if args.check:
            check_review(plan,registry)
            if reading!=plan[KEY]['byteVerifiedReading']:raise ValueError('Mercy selection differs from pinned XML')
            if extract_election_context(args.directory,registry)!=plan[KEY]['electionApplicationCrossCheck']['byteVerifiedContext']:raise ValueError('Election context differs from pinned XML')
            print('Mercy45paragraphs+Dominion election context:PASS;not complete ordo or foreign-case closure')
        else:print(json.dumps(reading,ensure_ascii=False,indent=2))
    except (OSError,KeyError,ValueError,TypeError,StopIteration) as exc:parser.exit(1,str(exc)+'\n')


if __name__=='__main__':main()
