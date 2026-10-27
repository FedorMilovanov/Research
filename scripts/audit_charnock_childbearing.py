#!/usr/bin/env python3
"""One named TCP discourse:conditional pastoral claims,not medical guarantees."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS,plain
from audit_charnock_pastoral_contexts import source_structure,extract as extract_context

ROOT=Path(__file__).resolve().parents[1]
HEADING='A DISCOURSE FOR The Comfort of Child-bearing Women.'
PROBES={
 'NESTED_POLEMIC':(407,'Becanus only is the man that Rivet mentions','NESTED_REPORTED_POLEMIC'),
 'TACIT_RESERVE':(411,'there being in all such promises a tacit reserve','AUTHOR_QUALIFICATION'),
 'STATE_NOT_CAUSE':(412,'not the cause of the salvation of the Woman, but the state','AUTHOR_DISTINCTION'),
 'COLLECTIVE_SUBJECT':(413,'The name Woman is taken collectively for all Women','AUTHOR_DISTINCTION'),
 'PAIN_NOT_BIRTH':(431,'Child-bearing it self is not the punishment, but the pain in it.','AUTHOR_DISTINCTION'),
 'ADAM_COMPARISON':(434,"the sin was greater on Adam 's part",'AUTHOR_QUALIFIED_COMPARISON'),
 'NOT_SATISFACTION':(442,"not continued as a part of Satisfaction to the justice of God.",'AUTHOR_DISTINCTION'),
 'NO_PRESENT_REMOVAL':(449,'God never promised the total removal of them in this life to any Saint','AUTHOR_QUALIFICATION'),
 'MATERIAL_FORMAL':(451,'though the curse remains materially, yet it doth not formally','AUTHOR_DISTINCTION'),
 'PRESENTED_OBJECTION':(458,'What is the reason these punishments are continued','AUTHOR_PRESENTED_OBJECTION'),
 'NOT_AUTOMATIC_GRACE':(470,'Punishments of themselves have no power to set any grace on work','AUTHOR_QUALIFICATION'),
 'FAITH_REPROACH':(480,'not for want of faithfulness in God, but for want of Faith in us','AUTHOR_PASTORAL_REPROACH'),
 'NONABSOLUTE':(480,'not an absolute, infallible assurance','AUTHOR_QUALIFICATION'),
 'RHETORICAL_HANDS':(488,'Unbelief binds Gods hands','AUTHOR_RHETORICAL_APPLICATION'),
 'SAME_MATERIAL_OUTCOME':(490,'In the material part of the punishment there is no difference between a believer and an unbeliever','AUTHOR_DISTINCTION'),
}


def text_hash(text):return hashlib.sha256(text.encode()).hexdigest()


def extract(directory,registry):
    contexts=extract_context(directory,registry,('TXT-20',),paragraph_ranges={'TXT-20':(403,490)})
    raw,root,parents,pages,paragraphs=source_structure(directory,registry,'A32724')
    matches=[d for d in root.iter(NS+'div') if d.find(NS+'head') is not None and plain(d.find(NS+'head'))==HEADING]
    if len(matches)!=1:raise ValueError('Unique childbearing discourse required')
    d=matches[0];members=set(d.iter());epigraph=d.find(NS+'epigraph');epi=set(epigraph.iter())
    indexes={p:i for i,p in enumerate(paragraphs)}
    manifest=[dict(paragraphIndexZeroBased=indexes[p],zone='EPIGRAPH' if p in epi else 'BODY',textSha256=text_hash(plain(p))) for p in paragraphs if p in members]
    standalone=[];children=list(d)
    for i,c in enumerate(children):
        if c.tag not in {NS+'head',NS+'pb',NS+'epigraph',NS+'p',NS+'q'}:
            raise ValueError('Unaccounted childbearing main-text element')
        if c.tag==NS+'q':
            if list(c.iter(NS+'p')):raise ValueError('Standalone doctrine cannot double-count nested paragraphs')
            before=[indexes[n] for b in children[:i] for n in b.iter(NS+'p') if n in indexes]
            after=[indexes[n] for b in children[i+1:] for n in b.iter(NS+'p') if n in indexes]
            text=plain(c)
            standalone.append(dict(directChildIndexZeroBased=i,elementTag='q',afterParagraphIndexZeroBased=before[-1],beforeParagraphIndexZeroBased=after[0],
                                   startTeiPage=pages[c],text=text,textSha256=text_hash(text),role='DISPLAYED_AUTHOR_DOCTRINE'))
    notes=[]
    for i,n in enumerate(d.iter(NS+'note')):
        p=n
        while p in parents and p not in indexes:p=parents[p]
        if p not in indexes:raise ValueError('Marginal note needs an identified paragraph parent')
        text=plain(n);notes.append(dict(localNoteIndexZeroBased=i,parentParagraphIndexZeroBased=indexes[p],startTeiPage=pages[n],text=text,textSha256=text_hash(text)))
    successor=parents[paragraphs[491]]
    while successor in parents and successor.tag!=NS+'div':successor=parents[successor]
    return dict(contexts=contexts,layout=dict(sectionHeading=HEADING,epigraph=plain(epigraph),directBodyParagraphs=len(d.findall(NS+'p')),
                paragraphManifest=manifest,standaloneDoctrineBlocks=standalone,nextDiscourseHeading=plain(successor.find(NS+'head')),
                normalization='Main text includes epigraph and standalone q;note/fw bodies omitted from paragraph text;no images or modernized lacunae'),
                marginalNotes=notes,successorScopeParagraph=dict(paragraphIndexZeroBased=517,text=plain(paragraphs[517]),textSha256=text_hash(plain(paragraphs[517]))))


def check_review(plan,registry):
    review=plan['childbearingReview'];c=review['byteVerifiedContexts']['TXT-20'];layout=review['layout'];pin=registry['sources']['A32724']
    if (review['reviewState']!='ONE_TCP_DISCOURSE_MAIN_TEXT_WITH_CONDITIONAL_PASTORAL_CLAIMS'
        or review['clinicalOutcomeGuaranteed'] is not False or review['individualBlameInferenceApproved'] is not False
        or review['criticalEditionVerified'] is not False or review['publicationApproval'] is not False):
        raise ValueError('Historical pastoral claims cannot certify medical outcomes,individual blame or publication')
    anchor=next(a for a in registry['anchors'] if a['id']=='TXT-20')
    if (c['source']!='A32724' or c['sourceSha256']!=pin['sha256'] or c['sourceBytes']!=pin['size']
        or c['probe']!=anchor['probe'] or c['probeTeiPages']!=anchor['teiPages']
        or c['rangeOverrideStartEndInclusive']!=[403,490]
        or [p['paragraphIndexZeroBased'] for p in c['contextWindow']]!=list(range(403,491))):
        raise ValueError('Childbearing main-text paragraph coverage must remain source-bound')
    paragraphs={p['paragraphIndexZeroBased']:p for p in c['contextWindow']}
    for p in paragraphs.values():
        if text_hash(p['text'])!=p['textSha256']:raise ValueError('Childbearing paragraph hash mismatch')
    if (layout['sectionHeading']!=HEADING or layout['directBodyParagraphs']!=87
        or layout['nextDiscourseHeading']!='A DISCOURSE OF THE Sins of the Regenerate.'
        or [p['paragraphIndexZeroBased'] for p in layout['paragraphManifest']]!=list(range(403,491))):
        raise ValueError('One epigraph and 87 body paragraphs belong to this discourse only')
    for p in layout['paragraphManifest']:
        i=p['paragraphIndexZeroBased']
        if p['textSha256']!=paragraphs[i]['textSha256'] or p['zone']!=('EPIGRAPH' if i==403 else 'BODY'):
            raise ValueError('Childbearing manifest must match every paragraph and epigraph')
    standalone=layout['standaloneDoctrineBlocks']
    if len(standalone)!=1:
        raise ValueError('Displayed doctrine outside paragraphs must not be omitted')
    q=standalone[0]
    if (q['elementTag']!='q' or q['afterParagraphIndexZeroBased']!=429 or q['beforeParagraphIndexZeroBased']!=430
        or not q['text'].startswith('Doct. The continuance of the punishment') or text_hash(q['text'])!=q['textSha256']
        or q['role']!='DISPLAYED_AUTHOR_DOCTRINE'):
        raise ValueError('Standalone doctrine must retain its authorial frame and position')
    prior=plan['freshStudyReview']['byteVerifiedContexts']['TXT-20']['contextWindow']
    old_final=plan['regenerateOpeningReview']['byteVerifiedContexts']['TXT-07']['contextWindow'][0]
    for p in prior+[old_final]:
        if paragraphs[p['paragraphIndexZeroBased']]!=p:raise ValueError('Previously read childbearing paragraphs must match exactly')
    if review['priorParagraphIndexes']!=[412,413,414,490] or review['newParagraphCount']!=84:
        raise ValueError('Old windows and conclusion cannot be counted as 88 new paragraphs')
    observations=review['observations']
    if len(observations)!=15 or {o['id'] for o in observations}!=set(PROBES):
        raise ValueError('Fifteen bounded childbearing observations required')
    for o in observations:
        i,probe,role=PROBES[o['id']]
        if (o['paragraphIndexZeroBased']!=i or o['probe']!=probe or probe not in paragraphs[i]['text']
            or o['probeRole']!=role or not o['limitedReading'] or not o['prohibitedInference'] or o['translationState']!='NOT_PREPARED'):
            raise ValueError('Preserve nested attribution,reproach and qualifications together')
    notes=review['byteVerifiedMarginalNotes'];decisions=review['marginalNoteDecisions']
    if len(notes)!=7 or len(decisions)!=7:raise ValueError('Seven marginal citations,not seven acquired books,required')
    note_coordinates=[(406,'76'),(407,'76'),(409,'77'),(432,'78'),(434,'78'),(468,'82'),(480,'85')]
    probes=['Hierom.','Isagog. ad Script.','Aristot. Hist. Animal.','Mariana in loc.','Estius in senten.','Kellet Miscel.','Tho. Goodwin.']
    for i,(n,d,probe) in enumerate(zip(notes,decisions,probes)):
        if (n['localNoteIndexZeroBased']!=i or probe not in n['text']
            or (n['parentParagraphIndexZeroBased'],n['startTeiPage'])!=note_coordinates[i] or text_hash(n['text'])!=n['textSha256']
            or n['parentParagraphIndexZeroBased'] not in paragraphs
            or d['localNoteIndexZeroBased']!=i or d['noteSha256']!=n['textSha256']
            or d['reviewState']!='TCP_CITATION_LOCATED_NOT_CITED_WORK_REPLAY'
            or d['citedWorkIndependentlyReplayed'] is not False or not d['limit']):
            raise ValueError('A marginal source pointer does not identify or replay its edition')
    successor=review['successorScopeParagraph'];old=next(p for p in plan['regenerateOpeningReview']['byteVerifiedContexts']['TXT-07']['contextWindow'] if p['paragraphIndexZeroBased']==517)
    if (successor['paragraphIndexZeroBased']!=517 or successor['text']!=old['text'] or successor['textSha256']!=old['textSha256']):
        raise ValueError('Printed successor relation needs its exact scope paragraph,not a reconstructed preaching chronology')
    relations=review['limitedRelations']
    if len(relations)!=2 or {r['id'] for r in relations}!={'ATTRIBUTES_IN_PASTORAL_USE','PRINTED_COMFORT_AND_PRESUMPTION'}:
        raise ValueError('Two limited internal relations required,not a whole-corpus reception verdict')
    if any(not r['limitedRelation'] or not r['prohibitedInference'] for r in relations):
        raise ValueError('Internal relations need both a positive reading and a limit')
    card=next(c for c in plan['studyCards'] if c['ref']=='TXT-20')
    doc=next(d for d in plan['documents'] if d['id']=='VII')
    if card.get('additionalMainTextReview')!='childbearingReview' or not {'regenerateOpeningReview','childbearingReview'} <= set(doc.get('supplementaryMainTextReadings',[])):
        raise ValueError('Prior study card and selected-work passport need explicit supplemental reading links')
    if review['printedPairChronologyEstablished'] is not False:raise ValueError('Printed adjacency is not a dated preaching sequence')
    return dict(childbearingParagraphsCovered=88,childbearingStandaloneDoctrineBlocks=1,newChildbearingParagraphs=84,childbearingObservations=15,childbearingMarginalCitations=7)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text());registry=json.loads((ROOT/plan['baselineRegistry']).read_text());result=extract(a.directory,registry)
        if a.check:
            check_review(plan,registry);review=plan['childbearingReview']
            if result!=dict(contexts=review['byteVerifiedContexts'],layout=review['layout'],marginalNotes=review['byteVerifiedMarginalNotes'],successorScopeParagraph=review['successorScopeParagraph']):
                raise ValueError('Stored childbearing text/layout differs from pinned XML')
            print('88 paragraphs+standalone doctrine/7 marginal citations: PASS;not medical guarantee or publication approval')
        else:print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,ET.ParseError) as exc:p.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
