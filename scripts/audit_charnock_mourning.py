#!/usr/bin/env python3
"""Full main-text coverage of one TCP mourning discourse,not dated occasion proof."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS,plain
from audit_charnock_pastoral_contexts import source_structure,extract as extract_context
ROOT=Path(__file__).resolve().parents[1]
HEADING='A DISCOURSE OF Mourning for other Mens Sins.'
RANGES={'opening':(332,373),'closing':(388,402)}
PROBES={
 'UNCERTAIN_ALTAR':(338,"'Tis uncertain whether this respects",'AUTHOR_EXEGETICAL_UNCERTAINTY'),
 'SIX_TO_ONE':(341,'intimating that there were six bad to one good in the City','AUTHOR_HOMILETIC_INFERENCE'),
 'MARK_LIMIT':(350,'But this mark is not properly meant here','AUTHOR_APPLICATION_LIMIT'),
 'BAPTIST':(365,"'Tis probable John Baptist",'AUTHOR_CONJECTURE'),
 'NESTED_BOOK':(368,'in an Ancient Mahumetan Book','NESTED_UNIDENTIFIED_BOOK_REPORT'),
 'IMPASSIBILITY':(372,'God indeed is uncapable of suffering','AUTHOR_QUALIFICATION'),
 'SELF_FIRST':(392,'unless we mourn for our own','AUTHOR_SELF_EXAMINATION'),
 'DEATH':(393,'or take away in them, to a place of happiness','AUTHOR_QUALIFICATION'),
 'AUSTIN':(397,'This was Austins opinion','ATTRIBUTED_AUTHORITY_REPORT'),
 'FALSE_FAST':(401,'to palliate a murther with the cloak of religion','AUTHOR_COUNTEREXAMPLE'),
 'UNDATED_WARNING':(402,'We know not whence they will come','AUTHOR_CONTEMPORARY_WARNING'),
 'SPIRIT_GRIEF':(402,'Grieve not the Holy Spirit of God','AUTHOR_SCRIPTURAL_AFFECTION_LANGUAGE'),
 'ZEAL':(402,'that sorrow is crude which is not accompanied with a godly Zeal','AUTHOR_PASTORAL_RULE'),
}

def digest(text):return hashlib.sha256(text.encode()).hexdigest()

def extract(directory,registry):
    contexts={k:extract_context(directory,registry,('TXT-03',),paragraph_ranges={'TXT-03':bounds})['TXT-03'] for k,bounds in RANGES.items()}
    raw,root,parents,pages,ps=source_structure(directory,registry,'A32724');ix={p:i for i,p in enumerate(ps)}
    ds=[d for d in root.iter(NS+'div') if d.find(NS+'head') is not None and plain(d.find(NS+'head'))==HEADING]
    if len(ds)!=1:raise ValueError('Unique mourning discourse required')
    d=ds[0];members=set(d.iter());epi=set(d.find(NS+'epigraph').iter());children=list(d)
    blocks=[dict(paragraphIndexZeroBased=ix[p],zone='EPIGRAPH' if p in epi else 'BODY',textSha256=digest(plain(p))) for p in ps if p in members]
    extra=[]
    for j,c in enumerate(children):
        if c.tag not in {NS+'head',NS+'pb',NS+'epigraph',NS+'p',NS+'q',NS+'list'}:raise ValueError('Unaccounted mourning main-text element')
        if c.tag in {NS+'q',NS+'list'}:
            if list(c.iter(NS+'p')):raise ValueError('Standalone mourning blocks cannot double-count paragraphs')
            before=[ix[p] for n in children[:j] for p in n.iter(NS+'p') if p in ix];after=[ix[p] for n in children[j+1:] for p in n.iter(NS+'p') if p in ix]
            text=plain(c);extra.append(dict(elementTag=c.tag[len(NS):],afterParagraphIndexZeroBased=before[-1],beforeParagraphIndexZeroBased=after[0],startTeiPage=pages[c],text=text,textSha256=digest(text)))
    notes=[]
    for j,n in enumerate(d.iter(NS+'note')):
        p=n
        while p in parents and p not in ix:p=parents[p]
        if p not in ix:raise ValueError('Mourning margin needs a main-text parent')
        text=plain(n);notes.append(dict(localNoteIndexZeroBased=j,parentParagraphIndexZeroBased=ix[p],startTeiPage=pages[n],text=text,textSha256=digest(text)))
    next_index=blocks[-1]['paragraphIndexZeroBased']+1
    next_node=ps[next_index]
    while next_node in parents and next_node.tag!=NS+'div':next_node=parents[next_node]
    next_heading=plain(next_node.find(NS+'head'))
    return dict(contexts=contexts,layout=dict(sectionHeading=HEADING,directBodyParagraphs=len(d.findall(NS+'p')),paragraphManifest=blocks,standaloneBlocks=extra,
                nextDiscourseParagraphIndex=next_index,nextDiscourseHeading=next_heading,normalization='TCP main text and epigraph,including standalone q/list;notes inventoried separately;no image collation'),marginalNotes=notes)

def check_review(plan,registry):
    review=plan['mourningCompleteReview'];contexts=review['byteVerifiedContexts'];layout=review['layout'];pin=registry['sources']['A32724']
    if (review['reviewState']!='ONE_TCP_MOURNING_MAIN_TEXT_COVERED_NOT_CRITICAL_EDITION'
        or review['datedOccasionEstablished'] is not False or review['modernCollectiveBlameApproved'] is not False
        or review['criticalEditionVerified'] is not False or review['publicationApproval'] is not False):
        raise ValueError('Mourning main-text coverage is not dated-occasion,critical-edition or collective-blame approval')
    if set(contexts)!=set(RANGES):raise ValueError('Two remaining discourse windows required')
    all_rows=[]
    anchor=next(a for a in registry['anchors'] if a['id']=='TXT-03')
    for key,(lo,hi) in RANGES.items():
        c=contexts[key]
        if (c['source']!='A32724' or c['sourceSha256']!=pin['sha256'] or c['sourceBytes']!=pin['size']
            or c['probe']!=anchor['probe'] or c['probeTeiPages']!=anchor['teiPages']
            or c['rangeOverrideStartEndInclusive']!=[lo,hi] or [p['paragraphIndexZeroBased'] for p in c['contextWindow']]!=list(range(lo,hi+1))):
            raise ValueError('Remaining mourning ranges need exact source pins')
        all_rows+=c['contextWindow']
    prior=plan['mourningDistinctionReview']['byteVerifiedContexts'];all_rows+=prior['pastoral']['contextWindow']
    paragraphs={p['paragraphIndexZeroBased']:p for p in all_rows}
    if sorted(paragraphs)!=list(range(332,403)):raise ValueError('All 71 discourse paragraphs need coverage')
    for p in paragraphs.values():
        if digest(p['text'])!=p['textSha256']:raise ValueError('Mourning main-text paragraph hash mismatch')
    for old in prior['opening']['contextWindow']:
        if paragraphs[old['paragraphIndexZeroBased']]!=old:raise ValueError('Old opening must match exactly')
    if (layout['sectionHeading']!=HEADING or layout['directBodyParagraphs']!=70 or layout['nextDiscourseParagraphIndex']!=403 or layout['nextDiscourseHeading']!='A DISCOURSE FOR The Comfort of Child-bearing Women.'
        or [p['paragraphIndexZeroBased'] for p in layout['paragraphManifest']]!=list(range(332,403))):
        raise ValueError('Mourning layout must exclude the next discourse')
    for p in layout['paragraphManifest']:
        i=p['paragraphIndexZeroBased']
        if p['textSha256']!=paragraphs[i]['textSha256'] or p['zone']!=('EPIGRAPH' if i==332 else 'BODY'):raise ValueError('Mourning layout differs from reading windows')
    extras=layout['standaloneBlocks']
    if len(extras)!=2 or [(e['elementTag'],e['afterParagraphIndexZeroBased'],e['beforeParagraphIndexZeroBased']) for e in extras]!=[('q',357,358),('list',358,359)]:
        raise ValueError('Both standalone doctrine and three-branch outline must remain visible')
    if 'Doct. Lamenting the sins' not in extras[0]['text'] or any(v not in extras[1]['text'] for v in ["1. 'Tis a Duty.",'2. A Duty acceptable to God.',"3. 'Tis a means of preservation"]):
        raise ValueError('Do not lose the doctrine or one of its three branches')
    for e in extras:
        if digest(e['text'])!=e['textSha256']:raise ValueError('Standalone mourning block hash mismatch')
    obs=review['observations']
    if len(obs)!=13 or {o['id'] for o in obs}!=set(PROBES):raise ValueError('Thirteen new bounded mourning observations required')
    for o in obs:
        i,probe,role=PROBES[o['id']]
        if (o['paragraphIndexZeroBased']!=i or o['probe']!=probe or probe not in paragraphs[i]['text'] or o['probeRole']!=role
            or not o['limitedReading'] or not o['prohibitedInference'] or o['translationState']!='NOT_PREPARED'):
            raise ValueError('Keep conjectures,authority reports and qualifications distinct')
    notes=review['byteVerifiedMarginalNotes'];decisions=review['marginalNoteDecisions']
    if len(notes)!=11 or len(decisions)!=11:raise ValueError('Eleven notes,not eleven independently read authors,required')
    note_coordinates=[(345,'65'),(345,'65'),(345,'65'),(361,'66'),(368,'67'),(371,'68'),(377,'69'),(379,'69'),(381,'70'),(387,'72'),(397,'74')]
    for i,(n,d) in enumerate(zip(notes,decisions)):
        expected='EXPLANATORY_COMMENT' if i in {6,7} else 'SOURCE_POINTER'
        if (n['localNoteIndexZeroBased']!=i or digest(n['text'])!=n['textSha256'] or n['parentParagraphIndexZeroBased'] not in paragraphs or (n['parentParagraphIndexZeroBased'],n['startTeiPage'])!=note_coordinates[i]
            or d['localNoteIndexZeroBased']!=i or d['noteSha256']!=n['textSha256'] or d['noteKind']!=expected
            or d['citedWorkIndependentlyReplayed'] is not False or not d['limit']):raise ValueError('Do not promote a marginal note into a verified foreign source')
    if review['newParagraphCount']!=54 or review['priorParagraphCount']!=17:raise ValueError('Previous 17 paragraphs cannot be counted again as new')
    if plan['mourningDistinctionReview'].get('mainTextCoverageFollowUp')!='mourningCompleteReview':raise ValueError('Earlier partial checkpoint needs an explicit complete-coverage follow-up')
    card=next(c for c in plan['studyCards'] if c['ref']=='TXT-03');doc=next(d for d in plan['documents'] if d['id']=='VII')
    if card.get('additionalMainTextReview')!='mourningCompleteReview' or 'mourningCompleteReview' not in doc.get('supplementaryMainTextReadings',[]):
        raise ValueError('Full main-text coverage needs explicit study/passport follow-up links')
    return dict(mourningMainTextParagraphsCovered=71,mourningStandaloneBlocks=2,newRemainingMourningParagraphs=54,mourningNewObservations=13,mourningMarginalNotes=11)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text());registry=json.loads((ROOT/plan['baselineRegistry']).read_text());result=extract(a.directory,registry)
        if a.check:
            check_review(plan,registry);r=plan['mourningCompleteReview']
            if result!=dict(contexts=r['byteVerifiedContexts'],layout=r['layout'],marginalNotes=r['byteVerifiedMarginalNotes']):raise ValueError('Stored complete mourning layout differs from XML')
            print('71 paragraphs+q/list+11 marginal notes: PASS;not a critical edition or dated-occasion proof')
        else:print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,ET.ParseError) as exc:p.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
