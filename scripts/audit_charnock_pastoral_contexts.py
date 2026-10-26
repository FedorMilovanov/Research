#!/usr/bin/env python3
"""Byte-pinned pastoral,Scripture and doctrinal reading contexts.

Default:seven selected contexts and mercy opening. Optional modes replay
extended windows or main-text coverage of one named discourse,not page images.
No network/writes. TXT-04 retains nine following lexical-scheme paragraphs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_biographical_anchors import text_and_pages, normalize

ROOT = Path(__file__).resolve().parents[1]
THEOLOGY_REFS = ('TXT-06', 'TXT-07')
THEOLOGY_AFTER = {'TXT-06': 5, 'TXT-07': 8}
STUDY_REFS = ('TXT-01', 'TXT-02', 'TXT-18', 'TXT-20')
REFS = ('TXT-07', 'TXT-08', 'TXT-17', 'TXT-04', 'BIB-07', 'BIB-06', 'TXT-19')


def source_structure(directory, registry, identifier):
    """Pinned raw TEI and one shared non-nested paragraph coordinate system."""
    source=registry['sources'][identifier]
    raw=(directory/(identifier+'.xml')).read_bytes()
    if len(raw)!=source['size'] or hashlib.sha256(raw).hexdigest()!=source['sha256']:
        raise ValueError(identifier+': source byte pin mismatch')
    root=ET.fromstring(raw);parents={c:p for p in root.iter() for c in p}
    page=None;page_at={};paragraphs=[]
    for n in root.iter():
        if n.tag==NS+'pb':page=n.get('n')
        page_at[n]=page
    for p in root.iter(NS+'p'):
        ancestor=p;excluded=False
        while ancestor in parents:
            ancestor=parents[ancestor]
            if ancestor.tag in {NS+'p',NS+'note',NS+'fw',NS+'teiHeader'}:excluded=True
        if not excluded:paragraphs.append(p)
    return raw,root,parents,page_at,paragraphs


def extract(directory, registry, refs=REFS, window_after=None, paragraph_ranges=None):
    anchors = {a['id']: a for a in registry['anchors']}
    cache, result = {}, {}
    for ref in refs:
        anchor = anchors[ref]
        identifier = anchor['source']
        source = registry['sources'][identifier]
        if identifier not in cache:
            raw, root, parents, page_at, paragraphs = source_structure(directory, registry, identifier)
            cache[identifier] = (root, parents, page_at, paragraphs, text_and_pages(raw))
        root, parents, page_at, paragraphs, (whole, labels) = cache[identifier]
        probe = normalize(anchor['probe'])
        matches = [(i, p) for i, p in enumerate(paragraphs) if probe in plain(p)]
        if len(matches) != 1 or whole.count(probe) != 1:
            raise ValueError(ref + ': context probe must be unique')
        index, paragraph = matches[0]
        at = whole.index(probe)
        span = list(dict.fromkeys(labels[at:at + len(probe)]))
        if span != anchor['teiPages']:
            raise ValueError(ref + ': registered probe page mismatch')
        ancestor = paragraph
        while ancestor in parents and ancestor.tag != NS + 'div':
            ancestor = parents[ancestor]
        head = ancestor.find(NS + 'head')
        signatures = [plain(n) for n in ancestor.iter(NS + 'signed')]
        windows = []
        after = (window_after or {}).get(ref, 9 if ref == 'TXT-04' else 1)
        if not isinstance(after, int) or isinstance(after, bool) or after < 0:
            raise ValueError('Context window length must be a nonnegative integer')
        lower, upper = max(0, index - 1), min(len(paragraphs), index + after + 1)
        bounds = (paragraph_ranges or {}).get(ref)
        if bounds is not None:
            if (len(bounds) != 2 or any(not isinstance(n,int) or isinstance(n,bool) for n in bounds)
                    or bounds[0] < 0 or bounds[1] < bounds[0] or bounds[1] >= len(paragraphs)):
                raise ValueError('Explicit paragraph range must be ordered and within the source')
            lower, upper = bounds[0], bounds[1]+1
        for i in range(lower, upper):
            p = paragraphs[i]
            value = plain(p)
            windows.append(dict(paragraphIndexZeroBased=i, startTeiPage=page_at[p], text=value,
                                textSha256=hashlib.sha256(value.encode()).hexdigest()))
        result[ref] = dict(source=identifier, sourceSha256=source['sha256'], sourceBytes=source['size'],
                           probe=anchor['probe'], probeTeiPages=span, selectedParagraphIndexZeroBased=index,
                           paragraphStartTeiPage=page_at[paragraph], sectionHeading=plain(head) if head is not None else None,
                           sectionSignatures=signatures, contextWindow=windows,
                           normalization='Whitespace/long-s;note/fw bodies excluded,tails retained',
                           boundary='Selected paragraph windows only;not full work or page-image verification')
        if bounds is not None:
            next_node = paragraphs[upper] if upper < len(paragraphs) else None
            while next_node is not None and next_node in parents and next_node.tag != NS+'div':
                next_node = parents[next_node]
            next_head = next_node.find(NS+'head') if next_node is not None else None
            result[ref].update(rangeOverrideStartEndInclusive=list(bounds),
                               anchorProbeInsideWindow=lower <= index < upper,
                               nextParagraphSectionHeading=plain(next_head) if next_head is not None else None,
                               boundary='Explicit paragraph continuation;anchor is replayed separately and may lie outside window;not full work')
    return result


# Exact authorial probes label only the selected span,not the whole paragraph.
DOCTRINAL_PROBES = {
 'ACTIVE_PASSIVE': ('TXT-06',1041,'Creation is considered as active or passive','AUTHOR_DISTINCTION'),
 'ETERNAL_DECREE': ('TXT-06',1042,'The Work was new, but the Decree','AUTHOR_DISTINCTION'),
 'POWER': ('TXT-06',1043,'There can be no more new Power in God','AUTHOR_DISTINCTION'),
 'RELATION': ('TXT-06',1044,'But howsoever, if there were any such change of relation','AUTHOR_QUALIFICATION'),
 'INCARNATION': ('TXT-06',1045,'but he did not cease to be God','AUTHOR_DISTINCTION'),
 'POSSIBILITY': ('TXT-07',518,'a May of possibility, not a May of lawfulness','AUTHOR_DISTINCTION'),
 'EXTERNAL_SERVICE': ('TXT-07',521,'Not that this attendance on God in his Ordinances doth of it self argue a man to be a good man','AUTHOR_QUALIFICATION'),
 'KNOWN_SIN': ('TXT-07',522,'Not one Example of the gross fall of a good man in Scripture will countenance any pretence for a course in sin','AUTHOR_DISTINCTION'),
 'PETER': ('TXT-07',525,"'Tis probable Peter's Faith",'AUTHOR_CONJECTURE'),
 'CORINTHIANS': ('TXT-07',526,'yet it seems to be out of a corrupt Judgment','AUTHOR_CONJECTURE'),
 'DAVID': ('TXT-07',527,'but of that after','DEFERRED_ARGUMENT'),
}


def check_doctrinal_review(plan,registry):
    review=plan['doctrinalDistinctionReview']
    if (review['reviewState']!='TWO_EXTENDED_DISTINCTIONS_NOT_COMPLETE_SYSTEM'
        or review['completeSystemClaimed'] is not False or review['publicationApproval'] is not False):
        raise ValueError('Selected doctrinal distinctions are not a complete system or publication approval')
    contexts=review['byteVerifiedContexts'];anchors={a['id']:a for a in registry['anchors']}
    if set(contexts)!=set(THEOLOGY_REFS):
        raise ValueError('Two extended doctrine windows required')
    for ref in THEOLOGY_REFS:
        ctx=contexts[ref];a=anchors[ref];pin=registry['sources'][a['source']]
        expected=list(range(ctx['selectedParagraphIndexZeroBased']-1,ctx['selectedParagraphIndexZeroBased']+THEOLOGY_AFTER[ref]+1))
        if (ctx['source']!=a['source'] or ctx['sourceSha256']!=pin['sha256'] or ctx['sourceBytes']!=pin['size']
            or ctx['probe']!=a['probe'] or ctx['probeTeiPages']!=a['teiPages']
            or [w['paragraphIndexZeroBased'] for w in ctx['contextWindow']]!=expected):
            raise ValueError('Doctrine context must retain source pins and extended paragraph sequence')
        for w in ctx['contextWindow']:
            if hashlib.sha256(w['text'].encode()).hexdigest()!=w['textSha256']:
                raise ValueError('Doctrinal paragraph hash mismatch')
    observations=review['observations']
    if len(observations)!=11 or {o['id'] for o in observations}!=set(DOCTRINAL_PROBES):
        raise ValueError('Eleven bounded doctrinal observations required')
    for o in observations:
        ref,index,probe,role=DOCTRINAL_PROBES[o['id']]
        paragraph=next(p for p in contexts[ref]['contextWindow'] if p['paragraphIndexZeroBased']==index)
        if (o['ref']!=ref or o['paragraphIndexZeroBased']!=index or o['probe']!=probe
            or probe not in paragraph['text'] or o['probeRole']!=role
            or not o['limitedReading'] or not o['prohibitedInference']
            or o['translationState']!='NOT_PREPARED'):
            raise ValueError('Authorial distinction,qualification or conjecture must remain context-bound')
    rows={r['ref']:r for r in plan['theologyMatrix']}
    for ref in THEOLOGY_REFS:
        if rows[ref].get('contextReviewState')!='EXTENDED_SELECTED_CONTEXT_VERIFIED' or not rows[ref].get('reviewHistory'):
            raise ValueError('Old matrix checkpoint must remain historical after extended reading')
    return dict(extendedDoctrinalWindows=2,doctrinalObservations=11,completeTheologicalSystemClaimed=False)


CONTINUATION_PROBES = {
 'NO_DISPENSATION': (529,'Regeneration gives not a man a dispensation from the Law of God.','AUTHOR_THESIS'),
 'OUTWARD_RESTRAINT': (538,"Such a man is not oblig'd to his will for his abstinence from sin, but to the outward hindrances",'AUTHOR_DISTINCTION'),
 'MODERATE_CENSURE': (547,'to moderate your Censures of others','PASTORAL_APPLICATION'),
 'PARTIAL_CONSENT': (548,'Some consent of the will I do acknowledg','AUTHOR_QUALIFICATION'),
 'SUPPOSE_ACTUAL_CONSENT': (551,'Suppose he may have by the suspension of grace, a whole actual consent of will to one particular sin','HYPOTHETICAL_CONCESSION'),
 'NO_FIXED_DURATION': (554,'But how long he may lie in a sin, without acting consideration about it, I cannot determine.','AUTHOR_LIMIT'),
 'COUNTERFACTUAL_NATHAN': (557,'If God had sent Nathan with a message to David','AUTHOR_COUNTERFACTUAL'),
 'RECOVERY_NOT_COMFORT': (558,'for the most part returns to his former holiness, and an increase of it, though not always to his former comforts','AUTHOR_QUALIFICATION'),
 'EXAMINATION': (560,'a circle of sinning and repenting without abhorrence of sin','PASTORAL_APPLICATION'),
}


def check_regenerate_continuation(plan,registry):
    review=plan['regenerateContinuationReview']
    if (review['reviewState']!='LATER_ARGUMENT_AND_ENDING_NOT_FULL_TREATISE'
        or review['durationDetermined'] is not False or review['comfortRestorationGuaranteed'] is not False
        or review['completeTreatiseClaimed'] is not False or review['publicationApproval'] is not False
        or review['sourceDependencyState']!='SAME_WORK_NOT_INDEPENDENT_WITNESS'):
        raise ValueError('Continuation cannot certify a duration,comfort guarantee,full treatise or independent witness')
    if set(review['byteVerifiedContexts'])!={'TXT-07'}:
        raise ValueError('Only the selected regenerate continuation is replayed')
    c=review['byteVerifiedContexts']['TXT-07'];a=next(a for a in registry['anchors'] if a['id']=='TXT-07');pin=registry['sources'][a['source']]
    if (c['source']!=a['source'] or c['sourceSha256']!=pin['sha256'] or c['sourceBytes']!=pin['size']
        or c['probe']!=a['probe'] or c['probeTeiPages']!=a['teiPages']
        or c['rangeOverrideStartEndInclusive']!=[527,560] or c['anchorProbeInsideWindow'] is not False
        or c['nextParagraphSectionHeading']!='A DISCOURSE OF The Pardon of Sin.'
        or [p['paragraphIndexZeroBased'] for p in c['contextWindow']]!=list(range(527,561))):
        raise ValueError('Continuation range,anchor location and next-discourse boundary must remain explicit')
    paragraphs={p['paragraphIndexZeroBased']:p for p in c['contextWindow']}
    for p in paragraphs.values():
        if hashlib.sha256(p['text'].encode()).hexdigest()!=p['textSha256']:
            raise ValueError('Continuation paragraph hash mismatch')
    prior=plan['doctrinalDistinctionReview']['byteVerifiedContexts']['TXT-07']['contextWindow']
    prior_indexes={p['paragraphIndexZeroBased'] for p in prior}
    if (review['bridgeParagraphIndexes']!=[527] or paragraphs[527]!=next(p for p in prior if p['paragraphIndexZeroBased']==527)
        or review['newParagraphCount']!=33 or len(set(paragraphs)-prior_indexes)!=33
        or review['priorWindowRange']!=[518,527]):
        raise ValueError('Bridge paragraph cannot be counted as new evidence')
    observations=review['observations']
    if len(observations)!=9 or {o['id'] for o in observations}!=set(CONTINUATION_PROBES):
        raise ValueError('Nine bounded continuation observations required')
    for o in observations:
        index,probe,role=CONTINUATION_PROBES[o['id']]
        if (o['paragraphIndexZeroBased']!=index or o['probe']!=probe or probe not in paragraphs[index]['text']
            or o['probeRole']!=role or o['translationState']!='NOT_PREPARED'
            or not o['limitedReading'] or not o['prohibitedInference']):
            raise ValueError('Continuation must preserve qualification,conditional voice and source context')
    row=next(r for r in plan['theologyMatrix'] if r['ref']=='TXT-07')
    old=next(o for o in plan['doctrinalDistinctionReview']['observations'] if o['id']=='DAVID')
    if (row.get('continuationReviewState')!='LATER_ARGUMENT_AND_ENDING_VERIFIED_NOT_FULL_TREATISE'
        or not any(h['state']=='HISTORICAL_PRIOR_EXTENDED_WINDOW_CHECKPOINT' for h in row['reviewHistory'])
        or old.get('followUpReview')!='regenerateContinuationReview'):
        raise ValueError('Prior deferred topic needs an explicit historical checkpoint and current follow-up')
    return dict(regenerateContinuationParagraphs=34,newRegenerateParagraphs=33,regenerateContinuationObservations=9)


REGENERATE_HEADING = 'A DISCOURSE OF THE Sins of the Regenerate.'
OPENING_PROBES = {
 'OBLIGATION': (499,'But this is not the meaning of cannot here, ought not.','INSUFFICIENT_READING'),
 'DIFFICULTY': (500,'Not a simple impossibility, but secundum quid','REVIEWED_QUALIFICATION'),
 'FORMAL': (502,'Sin in a regenerate man proceeds not from his grace, but from his corruption.','AUTHOR_DISTINCTION'),
 'GRACE_LOST': (503,'This is founded upon a false Hypothesis, viz. That Grace may be lost:','REJECTED_HYPOTHESIS'),
 'UNBELIEF_ONLY': (504,'Though this be true, yet it is not the full meaning and sense of it.','INSUFFICIENT_READING'),
 'ANTITHESIS': (505,'which is clear by the Antithesis','PREFERRED_READING'),
 'ACT_HABIT': (507,'The Habit of sin, or custom in it.','AUTHOR_DISTINCTION'),
 'SEED': (508,"God's Seed efficiently, man's Seed subjectively.",'AUTHOR_DISTINCTION'),
 'LIMITED_PURPOSE': (517,'I intend not to run thorow all the parts of this Text','AUTHOR_SCOPE_LIMIT'),
}


def extract_regenerate_opening(directory,registry):
    contexts=extract(directory,registry,('TXT-07',),paragraph_ranges={'TXT-07':(490,518)})
    raw,root,parents,page_at,paragraphs=source_structure(directory,registry,'A32724')
    divisions=[d for d in root.iter(NS+'div') if d.find(NS+'head') is not None and plain(d.find(NS+'head'))==REGENERATE_HEADING]
    if len(divisions)!=1:raise ValueError('Unique regenerate discourse heading required')
    d=divisions[0];members=set(d.iter());epigraph=d.find(NS+'epigraph');epi_members=set(epigraph.iter()) if epigraph is not None else set()
    blocks=[dict(paragraphIndexZeroBased=i,zone='EPIGRAPH' if p in epi_members else 'BODY',textSha256=hashlib.sha256(plain(p).encode()).hexdigest()) for i,p in enumerate(paragraphs) if p in members]
    previous=parents[paragraphs[490]]
    while previous in parents and previous.tag!=NS+'div':previous=parents[previous]
    following=parents[paragraphs[561]]
    while following in parents and following.tag!=NS+'div':following=parents[following]
    layout=dict(sectionHeading=REGENERATE_HEADING,epigraph=plain(epigraph),blocks=blocks,
                directBodyParagraphs=len(d.findall(NS+'p')),epigraphParagraphs=len(epi_members.intersection(set(paragraphs))),
                excludedNoteCount=sum(1 for n in d.iter(NS+'note')),excludedRunningMatterCount=sum(1 for n in d.iter(NS+'fw')),
                precedingPrintedDiscourseHeading=plain(previous.find(NS+'head')),
                nextDiscourseHeading=plain(following.find(NS+'head')),
                normalization='TCP main text and epigraph;note/fw bodies excluded,tails retained;not image collation or critical apparatus')
    page=None;page_at={}
    for n in root.iter():
        if n.tag==NS+'pb':page=n.get('n')
        page_at[n]=page
    marginal=[]
    for i,n in enumerate(d.iter(NS+'note')):
        parent=n
        while parent in parents and parent not in paragraphs:parent=parents[parent]
        if parent not in paragraphs:raise ValueError('Marginal note needs an identified main-text parent')
        text=plain(n)
        marginal.append(dict(localNoteIndexZeroBased=i,parentParagraphIndexZeroBased=paragraphs.index(parent),
                             startTeiPage=page_at[n],text=text,textSha256=hashlib.sha256(text.encode()).hexdigest()))
    return dict(contexts=contexts,discourseLayout=layout,marginalNotes=marginal)


def check_regenerate_opening(plan,registry):
    review=plan['regenerateOpeningReview'];layout=review['discourseLayout']
    if (review['reviewState']!='ONE_TCP_DISCOURSE_MAIN_TEXT_COVERED_NOT_CRITICAL_EDITION'
        or review['completeExegesisClaimed'] is not False or review['criticalEditionVerified'] is not False
        or review['publicationApproval'] is not False):
        raise ValueError('Main-text coverage is not complete exegesis,critical collation or publication approval')
    context=review['byteVerifiedContexts']['TXT-07'];pin=registry['sources']['A32724']
    anchor=next(a for a in registry['anchors'] if a['id']=='TXT-07')
    if (context['source']!='A32724' or context['sourceSha256']!=pin['sha256'] or context['sourceBytes']!=pin['size']
        or context['probe']!=anchor['probe'] or context['probeTeiPages']!=anchor['teiPages']
        or context['anchorProbeInsideWindow'] is not False
        or context['rangeOverrideStartEndInclusive']!=[490,518]
        or [p['paragraphIndexZeroBased'] for p in context['contextWindow']]!=list(range(490,519))):
        raise ValueError('Opening includes one preceding-context paragraph and one old bridge,not 29 new discourse paragraphs')
    if (layout['sectionHeading']!=REGENERATE_HEADING or layout['directBodyParagraphs']!=69 or layout['epigraphParagraphs']!=1
        or layout['precedingPrintedDiscourseHeading']!='A DISCOURSE FOR The Comfort of Child-bearing Women.'
        or layout['nextDiscourseHeading']!='A DISCOURSE OF The Pardon of Sin.'
        or [b['paragraphIndexZeroBased'] for b in layout['blocks']]!=list(range(491,561))):
        raise ValueError('Regenerate discourse structural boundary must remain distinct from adjacent texts')
    all_rows=(context['contextWindow'] + plan['doctrinalDistinctionReview']['byteVerifiedContexts']['TXT-07']['contextWindow']
              +plan['regenerateContinuationReview']['byteVerifiedContexts']['TXT-07']['contextWindow'])
    covered={}
    for row in all_rows:
        i=row['paragraphIndexZeroBased']
        if hashlib.sha256(row['text'].encode()).hexdigest()!=row['textSha256'] or (i in covered and covered[i]!=row):
            raise ValueError('Main-text coverage needs exact matching overlap and paragraph hashes')
        covered[i]=row
    for b in layout['blocks']:
        i=b['paragraphIndexZeroBased']
        if covered[i]['textSha256']!=b['textSha256'] or b['zone']!=('EPIGRAPH' if i==491 else 'BODY'):
            raise ValueError('Each of 70 discourse paragraphs must be covered once by source-bound reading windows')
    if review['newDiscourseParagraphs']!=27 or review['priorContextParagraphIndexes']!=[490] or review['oldBridgeParagraphIndexes']!=[518]:
        raise ValueError('Adjacent text and old bridge cannot count as new discourse coverage')
    observations=review['observations']
    if len(observations)!=9 or {o['id'] for o in observations}!=set(OPENING_PROBES):
        raise ValueError('Nine opening distinctions required')
    for o in observations:
        index,probe,role=OPENING_PROBES[o['id']]
        if (o['paragraphIndexZeroBased']!=index or o['probe']!=probe or probe not in covered[index]['text']
            or o['probeRole']!=role or o['translationState']!='NOT_PREPARED'
            or not o['limitedReading'] or not o['prohibitedInference']):
            raise ValueError('Opening alternatives must retain acceptance,rejection and scope limits')
    notes=review['byteVerifiedMarginalNotes'];decisions=review['marginalNoteDecisions']
    expected_notes=[(526,'90','Baronias'),(532,'91','Taylor of repentance.'),(533,'92','Amyrant.'),
                    (553,'97','Smith o • the Creed.'),(557,'99','Greenham.'),(558,'99','Suarez: de Gratia.')]
    if len(notes)!=6 or len(decisions)!=6 or layout['excludedNoteCount']!=6:
        raise ValueError('Six marginal TCP citations required,separate from cited-work acquisition')
    for i,(note,decision,(parent,page,probe)) in enumerate(zip(notes,decisions,expected_notes)):
        if (note['localNoteIndexZeroBased']!=i or note['parentParagraphIndexZeroBased']!=parent
            or note['startTeiPage']!=page or probe not in note['text']
            or hashlib.sha256(note['text'].encode()).hexdigest()!=note['textSha256']
            or decision['localNoteIndexZeroBased']!=i or decision['noteSha256']!=note['textSha256']
            or decision['reviewState']!='TCP_CITATION_LOCATED_NOT_CITED_WORK_REPLAY'
            or decision['citedWorkIndependentlyReplayed'] is not False or not decision['limit']):
            raise ValueError('Marginal citation cannot certify spelling repair,identity or cited-work replay')
    slices=review['coverageSlices']
    if [(s['indexes'],s['paragraphs']) for s in slices]!=[([491,517],27),([518,527],10),([528,560],33)]:
        raise ValueError('Coverage slices must count 70 unique discourse paragraphs,not their overlapping bridges')
    row=next(r for r in plan['theologyMatrix'] if r['ref']=='TXT-07')
    if row.get('mainTextReadingState')!='ONE_TCP_DISCOURSE_MAIN_TEXT_COVERED_NOT_CRITICAL_EDITION':
        raise ValueError('Current matrix must distinguish complete main text from earlier partial windows')
    return dict(regenerateMainTextParagraphsCovered=70,newOpeningDiscourseParagraphs=27,regenerateOpeningObservations=9,marginalCitationNotes=6,criticalEditionVerified=False)


PARDON_RANGES={'TXT-04':(586,597),'TXT-20':(442,442),'TXT-07':(529,529)}
PARDON_PROBES={
 'KNOWLEDGE':(586,'not out of the memory of his knowledge','AUTHOR_DISTINCTION'),
 'SANCTIFICATION':(589,'yet they are distinct acts','AUTHOR_DISTINCTION'),
 'PERSON_NOT_ACT':(590,'this pardon did not make David a righteous person in those acts','AUTHOR_DISTINCTION'),
 'DEMERIT':(591,'Pardon frees us from actual condemnation','AUTHOR_DISTINCTION'),
 'OBLIGATION':(592,'The guilt of sin, or obligation to punishment is taken away by pardon.','AUTHOR_THESIS_WITH_FOLLOWING_QUALIFICATIONS'),
 'SATISFACTION':(593,"not a punishment in order to Satisfaction.",'AUTHOR_QUALIFICATION'),
 'MEDICINAL':(594,"not so much poenal as medicinal.",'AUTHOR_QUALIFICATION'),
 'NOT_ETERNAL':(595,"not the eternal punishment due to sin.",'AUTHOR_QUALIFICATION'),
 'SHIMEI':(596,'It was not in Davids power absolutely to forget it','AUTHOR_SCRIPTURAL_ANALOGY'),
}


def check_pardon_distinctions(plan,registry):
    review=plan['pardonDistinctionReview'];contexts=review['byteVerifiedContexts']
    if (review['reviewState']!='BOUNDED_PARDON_DISTINCTIONS_NOT_COMPLETE_TREATISE'
        or review['completeTreatiseClaimed'] is not False or review['publicationApproval'] is not False):
        raise ValueError('Pardon selection cannot certify a complete treatise or publication')
    if set(contexts)!=set(PARDON_RANGES):raise ValueError('Pardon window and two same-work concordances required')
    anchors={a['id']:a for a in registry['anchors']}
    for ref,(lo,hi) in PARDON_RANGES.items():
        c=contexts[ref];a=anchors[ref];pin=registry['sources'][a['source']]
        if (c['source']!=a['source'] or c['sourceSha256']!=pin['sha256'] or c['sourceBytes']!=pin['size']
            or c['probe']!=a['probe'] or c['probeTeiPages']!=a['teiPages']
            or c['rangeOverrideStartEndInclusive']!=[lo,hi]
            or [p['paragraphIndexZeroBased'] for p in c['contextWindow']]!=list(range(lo,hi+1))):
            raise ValueError('Pardon source pins and selected ranges must remain explicit')
        for p in c['contextWindow']:
            if hashlib.sha256(p['text'].encode()).hexdigest()!=p['textSha256']:raise ValueError('Pardon paragraph hash mismatch')
    paragraphs={p['paragraphIndexZeroBased']:p for p in contexts['TXT-04']['contextWindow']}
    obs=review['observations']
    if len(obs)!=9 or {o['id'] for o in obs}!=set(PARDON_PROBES):raise ValueError('Nine pardon distinctions required')
    for o in obs:
        i,probe,role=PARDON_PROBES[o['id']]
        if (o['paragraphIndexZeroBased']!=i or o['probe']!=probe or probe not in paragraphs[i]['text']
            or o['probeRole']!=role or not o['limitedReading'] or not o['prohibitedInference']
            or o['translationState']!='NOT_PREPARED'):raise ValueError('Pardon distinctions must retain context and qualifications')
    old_w=next(p for p in plan['childbearingReview']['byteVerifiedContexts']['TXT-20']['contextWindow'] if p['paragraphIndexZeroBased']==442)
    old_s=next(p for p in plan['regenerateContinuationReview']['byteVerifiedContexts']['TXT-07']['contextWindow'] if p['paragraphIndexZeroBased']==529)
    if contexts['TXT-20']['contextWindow']!=[old_w] or contexts['TXT-07']['contextWindow']!=[old_s]:
        raise ValueError('Concordance paragraphs must match prior readings,not independent witnesses')
    if review['newParagraphCount']!=12 or review['replayedConcordanceParagraphs']!=2 or review['independenceState']!='SAME_AUTHOR_INTERNAL_CONCORDANCE':
        raise ValueError('Internal concordance cannot inflate new reading or independence counts')
    profile=next(p for p in plan['pastoralReview']['workProfiles'] if p['id']=='OTHER-PARDON')
    if profile.get('additionalReadingReview')!='pardonDistinctionReview' or profile['coverage']!='SELECTED_AUTHORIAL_PARAGRAPHS':
        raise ValueError('Pardon profile needs a bounded supplemental link,not a whole-work promotion')
    return dict(pardonDistinctionParagraphs=12,pardonDistinctionObservations=9,replayedPardonConcordances=2)


MOURNING_PROBES={
 'SELF_INTEREST':(374,'mask our displeasure against some mens offences with a care of Gods honour','AUTHOR_MOTIVE_EXAMINATION'),
 'GRIEF_ANGER':(375,'Anger for sin may have something of revenge in it','AUTHOR_DISTINCTION'),
 'INWARD_OUTWARD':(380,'they shall have a blessed inward security, though they may not always have an outward','AUTHOR_QUALIFICATION'),
 'STRONG_SINCERITY':(380,'but never an Ahab, or Judas, or any other ungodly person in Scripture, lamented the sins of others','AUTHOR_STRONG_SCRIPTURAL_GENERALIZATION'),
 'SILENT_CONSENT':(381,'on the side of sin by a silent consent','AUTHOR_COLLECTIVE_RESPONSIBILITY_CLAIM'),
 'CAPACITY':(381,'When we cannot be Reformers','AUTHOR_QUALIFICATION'),
 'NATIONAL_GUILT':(381,'When any sin becomes national, it is imputed to the body of the Nation','AUTHOR_COLLECTIVE_RESPONSIBILITY_CLAIM'),
 'SELF_APPLICATION':(385,'both you and I may bring a charge against our selves','AUTHOR_SELF_APPLICATION'),
 'PERSON':(387,'We must never love the wickedness, nor hate the person.','AUTHOR_PASTORAL_RULE'),
 'TONGUE':(387,'There ought to be more grief in our hearts, than fire in our tongues.','AUTHOR_PASTORAL_RULE'),
}


def extract_mourning(directory,registry):
    return dict(pastoral=extract(directory,registry,('TXT-03',),paragraph_ranges={'TXT-03':(374,387)})['TXT-03'],
                opening=extract(directory,registry,('TXT-03',))['TXT-03'])


def check_mourning_distinctions(plan,registry):
    review=plan['mourningDistinctionReview'];contexts=review['byteVerifiedContexts']
    if (review['reviewState']!='SELECTED_MOURNING_ARGUMENT_NOT_COMPLETE_TREATISE'
        or review['completeTreatiseClaimed'] is not False or review['modernCollectiveBlameApproved'] is not False
        or review['guaranteedOutwardProtection'] is not False or review['publicationApproval'] is not False):
        raise ValueError('Mourning selection cannot certify a whole treatise,collective blame or guaranteed physical protection')
    pin=registry['sources']['A32724'];anchor=next(a for a in registry['anchors'] if a['id']=='TXT-03')
    for key,indices in [('pastoral',list(range(374,388))),('opening',[333,334,335])]:
        c=contexts[key]
        if (c['source']!='A32724' or c['sourceSha256']!=pin['sha256'] or c['sourceBytes']!=pin['size']
            or c['probe']!=anchor['probe'] or c['probeTeiPages']!=anchor['teiPages']
            or [p['paragraphIndexZeroBased'] for p in c['contextWindow']]!=indices):
            raise ValueError('Mourning source and paragraph windows must remain bounded')
        for p in c['contextWindow']:
            if hashlib.sha256(p['text'].encode()).hexdigest()!=p['textSha256']:raise ValueError('Mourning paragraph hash mismatch')
    old=plan['translationReview']['byteVerifiedContexts']['TR-TXT03']['contextWindow']
    if [(p['text'],p['textSha256']) for p in contexts['opening']['contextWindow']]!=[(p['text'],p['textSha256']) for p in old]:
        raise ValueError('Uncertain opening is a replayed prior reading,not a new translation')
    paragraphs={p['paragraphIndexZeroBased']:p for p in contexts['pastoral']['contextWindow']}
    obs=review['observations']
    if len(obs)!=10 or {o['id'] for o in obs}!=set(MOURNING_PROBES):raise ValueError('Ten bounded mourning observations required')
    for o in obs:
        i,probe,role=MOURNING_PROBES[o['id']]
        if (o['paragraphIndexZeroBased']!=i or o['probe']!=probe or probe not in paragraphs[i]['text']
            or o['probeRole']!=role or not o['limitedReading'] or not o['prohibitedInference']
            or o['translationState']!='NOT_PREPARED'):raise ValueError('Preserve compassion,strong claims and qualifications together')
    if review['newPastoralParagraphs']!=14 or review['replayedOpeningParagraphs']!=3:
        raise ValueError('Prior opening cannot inflate new pastoral reading counts')
    card=next(c for c in plan['studyCards'] if c['ref']=='TXT-03')
    if card.get('additionalPastoralReadingReview')!='mourningDistinctionReview':
        raise ValueError('Prior Scripture card must retain an explicit supplemental pastoral link')
    return dict(mourningPastoralParagraphs=14,mourningObservations=10,replayedMourningOpeningParagraphs=3)


def extract_mercy_opening(directory, registry):
    source = registry['sources']['B20167']
    raw = (directory / 'B20167.xml').read_bytes()
    if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
        raise ValueError('B20167 source byte pin mismatch')
    root = ET.fromstring(raw)
    page, pages = None, {}
    for n in root.iter():
        if n.tag == NS + 'pb':
            page = n.get('n')
        pages[n] = page
    matches = []
    for d in root.iter(NS + 'div'):
        head = d.find(NS + 'head')
        if head is not None and plain(head) == 'Chiefest Sinners Objects of Choicest Mercy.':
            matches.append(d)
    if len(matches) != 1:
        raise ValueError('Mercy sermon must be identified by heading,not page1 alone')
    division = matches[0]
    paragraphs = division.findall(NS + 'p')[:7]
    if len(paragraphs) != 7 or 'For the last' not in plain(paragraphs[2]):
        raise ValueError('Preserve the two observations and transition to the latter')
    epigraph = division.find(NS + 'epigraph')
    return dict(source='B20167', sourceSha256=source['sha256'], sourceBytes=source['size'],
                sectionHeading=plain(division.find(NS + 'head')), epigraph=plain(epigraph),
                paragraphs=[dict(localParagraphIndexZeroBased=i, startTeiPage=pages[p], text=plain(p),
                                 numberedBreaks=[n.get('n') for n in p.iter(NS + 'pb') if n.get('n')],
                                 textSha256=hashlib.sha256(plain(p).encode()).hexdigest())
                            for i, p in enumerate(paragraphs)],
                locatorBoundary='Heading plus local paragraph index mandatory;B20167 has separate pagination sequences.',
                scope='Seven opening paragraphs,not the full treatise or recovered lost first discourse')



PARDON_OPENING_RANGE=(561,620)


def extract_pardon_opening(directory,registry):
    context=extract(directory,registry,('TXT-04',),paragraph_ranges={'TXT-04':PARDON_OPENING_RANGE})['TXT-04']
    _,root,parents,pages,paras=source_structure(directory,registry,'A32724')
    div=paras[620]
    while div in parents and div.tag!=NS+'div':div=parents[div]
    if plain(div.find(NS+'head'))!='A DISCOURSE OF The Pardon of Sin.':
        raise ValueError('Pardon opening discourse heading changed')
    prefix=[]
    for child in div:
        tag=child.tag.removeprefix(NS)
        if tag not in {'pb','head','epigraph','p'}:
            raise ValueError('Unknown standalone text unit in Pardon opening')
        prefix.append(tag)
        if child is paras[620]:break
    else:raise ValueError('Opening endpoint must be direct paragraph')
    notes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split()))
           for i in range(561,621) for n in paras[i].iter(NS+'note')]
    from audit_charnock_editorial_translations import licence_from_xml
    return dict(context=context,openingDirectTags=prefix,marginalNotes=notes,
                nextParagraph=dict(paragraphIndexZeroBased=621,startTeiPage=pages[paras[621]],text=plain(paras[621])),
                licence=licence_from_xml(directory/'A32724.xml'))


def check_pardon_opening(plan,registry):
    import hashlib
    from audit_charnock_translation_contexts import has_explicit_tcp_text_waiver
    r=plan['pardonOpeningReview'];data=r['byteVerifiedReading'];ctx=data['context'];source=registry['sources']['A32724']
    if (r['reviewState']!='CONTINUOUS_PARDON_OPENING_NOT_WHOLE_DISCOURSE'
            or r['wholeDiscourseRead'] is not False or r['publicationApproval'] is not False
            or r['foreignOriginalsVerified'] is not False or r['newParagraphIndices']!=list(range(572,586))+list(range(598,621))
            or r['previouslyReadParagraphIndices']!=list(range(561,572))+list(range(586,598))
            or r['remainingMainTextRange']!=[621,691]
            or ctx['source']!='A32724' or ctx['sourceSha256']!=source['sha256'] or ctx['sourceBytes']!=source['size']
            or ctx['rangeOverrideStartEndInclusive']!=[561,620] or ctx['selectedParagraphIndexZeroBased']!=562
            or ctx['sectionHeading']!='A DISCOURSE OF The Pardon of Sin.'
            or [p['paragraphIndexZeroBased'] for p in ctx['contextWindow']]!=list(range(561,621))):
        raise ValueError('Pardon opening must remain partial,with historical coverage retained')
    paras={p['paragraphIndexZeroBased']:p for p in ctx['contextWindow']}
    if any(hashlib.sha256(p['text'].encode()).hexdigest()!=p['textSha256'] for p in paras.values()):
        raise ValueError('Pardon opening paragraph hash differs')
    tags=data['openingDirectTags']
    if (tags.count('p')!=59 or tags.count('epigraph')!=1 or tags.count('head')!=1
            or any(t not in {'p','pb','head','epigraph'} for t in tags)
            or data['nextParagraph']['paragraphIndexZeroBased']!=621 or data['nextParagraph']['startTeiPage']!='107'
            or not data['nextParagraph']['text'].startswith('(3.) The extent of it.')
            or len(data['marginalNotes'])!=1 or data['marginalNotes'][0]['parentParagraphIndexZeroBased']!=592
            or data['marginalNotes'][0]['teiPage']!='103' or 'Durand.' not in data['marginalNotes'][0]['text']):
        raise ValueError('Pardon opening epigraph,body,notes or next boundary changed')
    licence=data['licence']
    if (hashlib.sha256(licence['statement'].encode()).hexdigest()!=licence['statementSha256']
            or not has_explicit_tcp_text_waiver(licence['statement'])
            or licence['scope']!='TCP encoded text only;not page images,autographs or external editions'):
        raise ValueError('Pardon opening text waiver only')
    obs=r['observations']
    expected=[562,575,578,598,599,603,604,610,611,617,618,619,620]
    if len(obs)!=13 or [o['paragraphIndexZeroBased'] for o in obs]!=expected:
        raise ValueError('Thirteen bounded Pardon opening observations required')
    for o in [r]+obs:
        if (o['evidenceClass']!='C' or o['accessState']!='FULL_OBJECT_VERIFIED'
                or o['locatorState']!='EXACT_LOCATOR_VERIFIED' or o['rightsState']!='RIGHTS_UNKNOWN'
                or o['publicationState']!='BLOCKED'
                or set(o['holds'])!={'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Pardon decisions must retain independent axes/HOLDs')
    for o in obs:
        if (not o['englishSpan'] or o['englishSpan'] not in paras[o['paragraphIndexZeroBased']]['text']
                or hashlib.sha256(o['englishSpan'].encode()).hexdigest()!=o['englishSpanSha256']
                or not o['observation'] or not o['prohibitedInference']):
            raise ValueError('Pardon observation needs actual span and limit')
    if not paras[592]['text'].endswith('But') or 'medicinal' not in paras[594]['text'] or 'not the eternal punishment' not in paras[595]['text']:
        raise ValueError('Retain prior But/medicinal/eternal qualification chain')
    return dict(pardonOpeningParagraphs=60,newPardonOpeningParagraphs=37,pardonOpeningObservations=13,pardonWholeDiscourseRead=False)


PARDON_USE_HEADINGS=['USE.','2. Use. Of comfort.','3 Use Of Examination.',
                     '4 Use of Exhortation.','3. Exhortation to those that are pardoned.']


def extract_pardon_complete(directory,registry):
    ctx=extract(directory,registry,('TXT-04',),paragraph_ranges={'TXT-04':(621,691)})['TXT-04']
    _,root,parents,pages,paras=source_structure(directory,registry,'A32724')
    div=paras[620]
    while div in parents and div.tag!=NS+'div':div=parents[div]
    def within(node,parent):
        while node in parents:
            node=parents[node]
            if node is parent:return True
        return False
    indices=[i for i,p in enumerate(paras) if within(p,div)]
    if indices!=list(range(561,692)):raise ValueError('Full Pardon main-text paragraph range changed')
    structural=[]
    for d in [div]+div.findall('.//'+NS+'div'):
        tags=[n.tag.removeprefix(NS) for n in d]
        if any(t not in {'p','div','pb','head','epigraph','trailer'} for t in tags):
            raise ValueError('Unknown standalone Pardon text unit')
        local=[i for i,p in enumerate(paras) if parents.get(p) is d]
        structural.append(dict(heading=plain(d.find(NS+'head')),directTags=tags,directParagraphIndices=local))
    manifest=[dict(paragraphIndexZeroBased=i,startTeiPage=pages[paras[i]],textSha256=hashlib.sha256(plain(paras[i]).encode()).hexdigest()) for i in indices]
    notes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split()))
           for i in indices for n in paras[i].iter(NS+'note')]
    trailers=[dict(teiPage=pages[n],text=plain(n)) for n in div.iter(NS+'trailer')]
    return dict(continuationContext=ctx,layout=structural,mainTextManifest=manifest,marginalNotes=notes,trailers=trailers,
                nextParagraph=dict(paragraphIndexZeroBased=692,zone='BACK' if within(paras[692],root.find('.//'+NS+'back')) else 'UNKNOWN',text=plain(paras[692])))


def check_pardon_complete(plan,registry):
    r=plan['pardonCompleteReview'];data=r['byteVerifiedReading'];ctx=data['continuationContext']
    source=registry['sources']['A32724']
    if (r['reviewState']!='COMPLETE_TCP_PARDON_MAIN_TEXT'
            or r['criticalEditionVerified'] is not False or r['foreignOriginalsVerified'] is not False
            or r['publicationApproval'] is not False or r['modernClinicalGuaranteeApproved'] is not False
            or r['priorParagraphCount']!=60 or r['additionalCoverageParagraphCount']!=71
            or ctx['sourceSha256']!=source['sha256'] or ctx['sourceBytes']!=source['size']
            or ctx['rangeOverrideStartEndInclusive']!=[621,691] or ctx['anchorProbeInsideWindow'] is not False
            or [p['paragraphIndexZeroBased'] for p in ctx['contextWindow']]!=list(range(621,692))):
        raise ValueError('Complete Pardon review is single TCP main text,not critical edition or foreign acquisition')
    opening=plan['pardonOpeningReview']['byteVerifiedReading']['context']['contextWindow']
    allp=opening+ctx['contextWindow'];paras={p['paragraphIndexZeroBased']:p for p in allp}
    if len(paras)!=131 or any(hashlib.sha256(p['text'].encode()).hexdigest()!=p['textSha256'] for p in allp):
        raise ValueError('Complete Pardon paragraph coverage/hash differs')
    if data['mainTextManifest']!=[dict(paragraphIndexZeroBased=i,startTeiPage=paras[i]['startTeiPage'],textSha256=paras[i]['textSha256']) for i in range(561,692)]:
        raise ValueError('Pardon manifest must tie all131 paragraphs to actual contexts')
    layout=data['layout'];ranges=[list(range(562,641)),list(range(641,646)),list(range(646,651)),list(range(651,678)),list(range(678,688)),list(range(688,692))]
    if (len(layout)!=6 or [x['heading'] for x in layout]!=['A DISCOURSE OF The Pardon of Sin.']+PARDON_USE_HEADINGS
            or [x['directParagraphIndices'] for x in layout]!=ranges
            or layout[0]['directTags'].count('epigraph')!=1 or layout[0]['directTags'].count('div')!=5
            or any(any(t not in {'p','div','pb','head','epigraph','trailer'} for t in x['directTags']) for x in layout)
            or data['trailers']!=[dict(teiPage='118',text='FINIS.')]
            or data['nextParagraph']['paragraphIndexZeroBased']!=692 or data['nextParagraph']['zone']!='BACK'
            or not data['nextParagraph']['text'].startswith('The Reader may observe,')):
        raise ValueError('Pardon application headings,FINIS or back-matter boundary changed')
    notes=data['marginalNotes']
    if (len(notes)!=2 or notes[0]!=plan['pardonOpeningReview']['byteVerifiedReading']['marginalNotes'][0]
            or notes[1]!=dict(parentParagraphIndexZeroBased=657,teiPage='114',text='Burges.')):
        raise ValueError('Keep both Pardon marginal notes,not two acquired originals')
    obs=r['observations'];positions=[621,622,625,628,630,632,636,638,650,659,667,668,672,673,676,677,682,685,686,691]
    if len(obs)!=20 or [o['paragraphIndexZeroBased'] for o in obs]!=positions:
        raise ValueError('Twenty bounded Pardon continuation observations required')
    for o in [r]+obs:
        if (o['evidenceClass']!='C' or o['accessState']!='FULL_OBJECT_VERIFIED'
                or o['locatorState']!='EXACT_LOCATOR_VERIFIED' or o['rightsState']!='RIGHTS_UNKNOWN'
                or o['publicationState']!='BLOCKED'
                or set(o['holds'])!={'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Complete Pardon analytical decisions retain axes/HOLDs')
    for o in obs:
        if (not o['englishSpan'] or o['englishSpan'] not in paras[o['paragraphIndexZeroBased']]['text']
                or hashlib.sha256(o['englishSpan'].encode()).hexdigest()!=o['englishSpanSha256']
                or not o['observation'] or not o['prohibitedInference']):
            raise ValueError('Pardon continuation observation needs actual span and inference limit')
    if 'pardonCompleteReview' not in next(d for d in plan['documents'] if d['id']=='VII')['supplementaryMainTextReadings']:
        raise ValueError('PartVII must link completed Pardon main text')
    return dict(pardonMainTextParagraphs=131,pardonAdditionalCoverageParagraphs=71,pardonContinuationObservations=20,pardonMarginalNotes=2,pardonWholeDiscourseRead=True)


def extract_stability_opening(directory,registry):
    ctx=extract(directory,registry,('TXT-18',),paragraph_ranges={'TXT-18':(92,127)})['TXT-18']
    _,root,parents,pages,paras=source_structure(directory,registry,'A32724')
    div=paras[127]
    while div in parents and div.tag!=NS+'div':div=parents[div]
    prefix=[];standalone=[];last=None
    for node in div:
        tag=node.tag.removeprefix(NS)
        if tag not in {'head','pb','epigraph','p','q'}:raise ValueError('Unknown standalone Stability opening unit')
        prefix.append(tag)
        if tag=='p':last=paras.index(node)
        if tag=='q':
            text=plain(node)
            standalone.append(dict(afterParagraphIndexZeroBased=last,beforeParagraphIndexZeroBased=last+1,teiPage=pages[node],text=text,textSha256=hashlib.sha256(text.encode()).hexdigest(),voice='CHARNOCK_DOCTRINAL_PROPOSITION'))
        if node is paras[127]:break
    else:raise ValueError('Stability endpoint must be direct paragraph')
    notes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split()))
           for i in range(92,128) for n in paras[i].iter(NS+'note')]
    from audit_charnock_editorial_translations import licence_from_xml
    return dict(context=ctx,prefixTags=prefix,standaloneDoctrine=standalone,marginalNotes=notes,
                nextParagraph=dict(paragraphIndexZeroBased=128,startTeiPage=pages[paras[128]],probe=plain(paras[128])[:120]),
                licence=licence_from_xml(directory/'A32724.xml'))


def check_stability_opening(plan,registry):
    from audit_charnock_translation_contexts import has_explicit_tcp_text_waiver
    r=plan['stabilityOpeningReview'];data=r['byteVerifiedReading'];ctx=data['context'];source=registry['sources']['A32724']
    if (r['reviewState']!='BOUNDED_STABILITY_OPENING_WITH_STANDALONE_DOCTRINE'
            or any(r[k] is not False for k in ('wholeDiscourseRead','datedOccasionEstablished','foreignOriginalsVerified','modernCollectiveBlameApproved','publicationApproval'))
            or ctx['source']!='A32724' or ctx['sourceSha256']!=source['sha256'] or ctx['sourceBytes']!=source['size']
            or ctx['rangeOverrideStartEndInclusive']!=[92,127] or ctx['selectedParagraphIndexZeroBased']!=93
            or ctx['sectionHeading']!='A DISCOURSE OF THE CHURCHES STABILITY.'
            or [x['paragraphIndexZeroBased'] for x in ctx['contextWindow']]!=list(range(92,128))
            or r['additionalCoverageParagraphCount']!=33 or r['priorParagraphCount']!=3):
        raise ValueError('Stability opening must stay bounded,undated and without modern collective verdict')
    rows=ctx['contextWindow'];paras={p['paragraphIndexZeroBased']:p for p in rows}
    if any(hashlib.sha256(p['text'].encode()).hexdigest()!=p['textSha256'] for p in rows):
        raise ValueError('Stability paragraph hash differs')
    if rows[:3]!=plan['freshStudyReview']['byteVerifiedContexts']['TXT-18']['contextWindow']:
        raise ValueError('Prior Scripture window must replay unchanged')
    tags=data['prefixTags'];qs=data['standaloneDoctrine']
    if (tags.count('p')!=35 or tags.count('epigraph')!=1 or tags.count('q')!=1
            or any(t not in {'head','pb','epigraph','p','q'} for t in tags) or len(qs)!=1
            or qs[0]['afterParagraphIndexZeroBased']!=112 or qs[0]['beforeParagraphIndexZeroBased']!=113
            or qs[0]['teiPage']!='23' or qs[0]['voice']!='CHARNOCK_DOCTRINAL_PROPOSITION'
            or qs[0]['text']!='Doct. The Gospel-Church is a perpetual Society establisht by the highest Power in Heaven or Earth.'
            or hashlib.sha256(qs[0]['text'].encode()).hexdigest()!=qs[0]['textSha256']
            or data['nextParagraph']['paragraphIndexZeroBased']!=128 or data['nextParagraph']['startTeiPage']!='26'):
        raise ValueError('Stability epigraph/standalone doctrine/next boundary changed')
    notes=data['marginalNotes'];decisions=r['marginalNoteDecisions']
    positions=[95,97,97,99,100,102,102,103,103,103,109,110,112,113,113,113,114,120,120,120]
    source_indices={0,1,5,10,11,14,15,16,19}
    if len(notes)!=20 or [n['parentParagraphIndexZeroBased'] for n in notes]!=positions or len(decisions)!=20:
        raise ValueError('Twenty local marginal notes required')
    for i,d in enumerate(decisions):
        if (d['localNoteIndex']!=i or d['noteSha256']!=hashlib.sha256(notes[i]['text'].encode()).hexdigest()
                or d['kind']!=('SOURCE_POINTER' if i in source_indices else 'BIBLICAL_OR_LEXICAL_NOTE')
                or d['counterpartRawAcquired'] is not False or not d['limit']):
            raise ValueError('Marginal pointer cannot certify foreign acquisition')
    obs=r['observations'];expected=[95,98,101,103,105,110,111,113,114,115,120,121,122,123,126,127]
    if len(obs)!=16 or [o['paragraphIndexZeroBased'] for o in obs]!=expected:
        raise ValueError('Sixteen bounded Stability observations required')
    for row in [r]+obs+decisions:
        if (row['evidenceClass']!='C' or row['accessState']!='FULL_OBJECT_VERIFIED'
                or row['locatorState']!='EXACT_LOCATOR_VERIFIED' or row['rightsState']!='RIGHTS_UNKNOWN'
                or row['publicationState']!='BLOCKED'
                or set(row['holds'])!={'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Stability decisions must retain separate axes/HOLDs')
    for o in obs:
        if (not o['englishSpan'] or o['englishSpan'] not in paras[o['paragraphIndexZeroBased']]['text']
                or hashlib.sha256(o['englishSpan'].encode()).hexdigest()!=o['englishSpanSha256']
                or not o['observation'] or not o['prohibitedInference']):
            raise ValueError('Stability observation needs actual span and inference limit')
    licence=data['licence']
    if (hashlib.sha256(licence['statement'].encode()).hexdigest()!=licence['statementSha256']
            or not has_explicit_tcp_text_waiver(licence['statement'])
            or licence['scope']!='TCP encoded text only;not page images,autographs or external editions'):
        raise ValueError('Stability text waiver only')
    return dict(stabilityOpeningParagraphs=36,stabilityStandaloneDoctrine=1,stabilityNewCoverageParagraphs=33,stabilityMarginalNotes=20,stabilityOpeningObservations=16)


def extract_stability_complete(directory,registry):
    ctx=extract(directory,registry,('TXT-18',),paragraph_ranges={'TXT-18':(128,184)})['TXT-18']
    _,root,parents,pages,paras=source_structure(directory,registry,'A32724')
    div=paras[184]
    while div in parents and div.tag!=NS+'div':div=parents[div]
    def within(node,parent):
        while node in parents:
            node=parents[node]
            if node is parent:return True
        return False
    indices=[i for i,p in enumerate(paras) if within(p,div)]
    if indices!=list(range(92,185)):raise ValueError('Stability complete paragraph range changed')
    tags=[n.tag.removeprefix(NS) for n in div]
    if any(t not in {'head','pb','epigraph','p','q'} for t in tags):
        raise ValueError('Unknown standalone Stability main-text unit')
    qrows=[];last=None
    for n in div:
        if n.tag==NS+'p':last=paras.index(n)
        if n.tag==NS+'q':
            text=plain(n)
            qrows.append(dict(afterParagraphIndexZeroBased=last,beforeParagraphIndexZeroBased=last+1,teiPage=pages[n],text=text,textSha256=hashlib.sha256(text.encode()).hexdigest(),voice='CHARNOCK_DOCTRINAL_PROPOSITION'))
    nextdiv=paras[185]
    while nextdiv in parents and nextdiv.tag!=NS+'div':nextdiv=parents[nextdiv]
    return dict(continuationContext=ctx,mainTextManifest=[dict(paragraphIndexZeroBased=i,startTeiPage=pages[paras[i]],textSha256=hashlib.sha256(plain(paras[i]).encode()).hexdigest()) for i in indices],
                directTags=tags,standaloneDoctrine=qrows,
                marginalNotes=[dict(parentParagraphIndexZeroBased=i,teiPage=pages[n],text=' '.join(''.join(n.itertext()).replace('ſ','s').split())) for i in indices for n in paras[i].iter(NS+'note')],
                nextParagraph=dict(paragraphIndexZeroBased=185,startTeiPage=pages[paras[185]],discourseHeading=plain(nextdiv.find(NS+'head')),text=plain(paras[185])))


def check_stability_complete(plan,registry):
    r=plan['stabilityCompleteReview'];data=r['byteVerifiedReading'];ctx=data['continuationContext'];source=registry['sources']['A32724']
    if (r['reviewState']!='COMPLETE_TCP_STABILITY_MAIN_TEXT'
            or any(r[k] is not False for k in ('criticalEditionVerified','datedOccasionEstablished','foreignOriginalsVerified','modernRacialHierarchyApproved','modernViolenceMandateApproved','publicationApproval'))
            or r['priorParagraphCount']!=36 or r['additionalCoverageParagraphCount']!=57
            or ctx['source']!='A32724' or ctx['sourceSha256']!=source['sha256'] or ctx['sourceBytes']!=source['size']
            or ctx['rangeOverrideStartEndInclusive']!=[128,184] or ctx['anchorProbeInsideWindow'] is not False
            or [p['paragraphIndexZeroBased'] for p in ctx['contextWindow']]!=list(range(128,185))):
        raise ValueError('Complete Stability is one TCP main text,not dated occasion,critical edition or foreign collation')
    opening=plan['stabilityOpeningReview']['byteVerifiedReading'];allp=opening['context']['contextWindow']+ctx['contextWindow']
    paras={p['paragraphIndexZeroBased']:p for p in allp}
    if len(paras)!=93 or any(hashlib.sha256(p['text'].encode()).hexdigest()!=p['textSha256'] for p in allp):
        raise ValueError('Complete Stability coverage/hash differs')
    if data['mainTextManifest']!=[dict(paragraphIndexZeroBased=i,startTeiPage=paras[i]['startTeiPage'],textSha256=paras[i]['textSha256']) for i in range(92,185)]:
        raise ValueError('All93 Stability paragraph coordinates must tie to contexts')
    tags=data['directTags']
    if (tags.count('p')!=92 or tags.count('epigraph')!=1 or tags.count('q')!=1 or tags.count('head')!=1
            or any(t not in {'p','epigraph','q','head','pb'} for t in tags)
            or data['standaloneDoctrine']!=opening['standaloneDoctrine']
            or data['nextParagraph']['paragraphIndexZeroBased']!=185 or data['nextParagraph']['startTeiPage']!='42'
            or data['nextParagraph']['discourseHeading']!='A DISCOURSE UPON THE Fifth of November.'
            or not data['nextParagraph']['text'].startswith('The Enemy said,')):
        raise ValueError('Stability body,standalone doctrine or next discourse changed')
    notes=data['marginalNotes'];decisions=r['additionalMarginalNoteDecisions']
    positions=[129,131,136,136,137,137,137,137,137,138,138,146,146,147,147,148,149,150,152,155,155,157,159,161,161,161,162,171]
    if len(notes)!=48 or notes[:20]!=opening['marginalNotes'] or [n['parentParagraphIndexZeroBased'] for n in notes[20:]]!=positions or len(decisions)!=28:
        raise ValueError('48 Stability notes required,20 prior+28 additional')
    for i,d in enumerate(decisions,20):
        if (d['localNoteIndex']!=i or d['noteSha256']!=hashlib.sha256(notes[i]['text'].encode()).hexdigest()
                or d['kind']!=('SOURCE_POINTER' if i in {20,23,34,42} else 'BIBLICAL_OR_LEXICAL_NOTE')
                or d['counterpartRawAcquired'] is not False or not d['limit']):
            raise ValueError('Additional Stability notes cannot certify foreign originals')
    obs=r['observations'];positions=[129,131,133,136,137,146,147,148,149,150,152,154,155,156,158,161,162,164,166,169,170,172,177,180,183,184]
    if len(obs)!=26 or [o['paragraphIndexZeroBased'] for o in obs]!=positions:
        raise ValueError('26 bounded Stability continuation observations required')
    for o in [r]+obs+decisions:
        if (o['evidenceClass']!='C' or o['accessState']!='FULL_OBJECT_VERIFIED'
                or o['locatorState']!='EXACT_LOCATOR_VERIFIED' or o['rightsState']!='RIGHTS_UNKNOWN'
                or o['publicationState']!='BLOCKED'
                or set(o['holds'])!={'EVIDENCE_HOLD','ARCHIVE_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Stability complete decisions retain axes/HOLDs')
    for o in obs:
        if (not o['englishSpan'] or o['englishSpan'] not in paras[o['paragraphIndexZeroBased']]['text']
                or hashlib.sha256(o['englishSpan'].encode()).hexdigest()!=o['englishSpanSha256']
                or not o['observation'] or not o['prohibitedInference']):
            raise ValueError('Stability continuation needs actual spans and limits')
    if 'stabilityCompleteReview' not in next(d for d in plan['documents'] if d['id']=='VII')['supplementaryMainTextReadings']:
        raise ValueError('PartVII must link complete Stability main-text reading')
    return dict(stabilityMainTextParagraphs=93,stabilityMainTextUnits=94,stabilityAdditionalCoverageParagraphs=57,stabilityMarginalNotes=48,stabilityContinuationObservations=26,stabilityWholeDiscourseRead=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--check', action='store_true')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--stability-complete',action='store_true',help='Replay complete TCP Stability main-text coverage')
    modes.add_argument('--stability-opening',action='store_true',help='Replay bounded Church Stability opening and standalone doctrine')
    modes.add_argument('--pardon-complete',action='store_true',help='Replay complete single TCP Pardon main-text coverage')
    modes.add_argument('--pardon-opening',action='store_true',help='Replay continuous opening561–620,not the full discourse')
    modes.add_argument('--mourning-distinctions',action='store_true',help='Replay mourning,motives and responsibility,not the full treatise')
    modes.add_argument('--pardon-distinctions',action='store_true',help='Replay pardon and consequence distinctions,not a full treatise')
    modes.add_argument('--regenerate-opening', action='store_true', help='Replay opening and source layout of one regenerate discourse')
    modes.add_argument('--regenerate-continuation', action='store_true', help='Replay the later argument and ending of Sins of the Regenerate')
    modes.add_argument('--theology', action='store_true', help='Replay two extended doctrinal distinctions')
    modes.add_argument('--study', action='store_true', help='Replay four Scripture contexts,not the pastoral/mercy set')
    args = parser.parse_args()
    try:
        registry = json.loads((ROOT / 'data/charnock-biographical-anchors-v1.json').read_text())
        if args.stability_complete:
            result=extract_stability_complete(args.directory,registry)
            if args.check:
                plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
                check_stability_opening(plan,registry)
                check_stability_complete(plan,registry)
                if result!=plan['stabilityCompleteReview']['byteVerifiedReading']:raise ValueError('Complete Stability differs from actual pinned XML')
                if extract_stability_opening(args.directory,registry)!=plan['stabilityOpeningReview']['byteVerifiedReading']:raise ValueError('Stability opening differs from XML')
                print('93 Stability paragraphs+standalone doctrine/48notes/next-discourse boundary: PASS;not critical edition or dated occasion')
            else:print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if args.stability_opening:
            result=extract_stability_opening(args.directory,registry)
            if args.check:
                plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
                check_stability_opening(plan,registry)
                if result!=plan['stabilityOpeningReview']['byteVerifiedReading']:raise ValueError('Stability opening differs from actual pinned XML')
                print('36 Stability paragraphs+standalone doctrine/20notes: PASS;not full discourse,dated occasion or foreign collation')
            else:print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if args.pardon_complete:
            result=extract_pardon_complete(args.directory,registry)
            if args.check:
                plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
                check_pardon_opening(plan,registry)
                check_pardon_complete(plan,registry)
                if result!=plan['pardonCompleteReview']['byteVerifiedReading']:raise ValueError('Complete Pardon layout/continuation differs from XML')
                if extract_pardon_opening(args.directory,registry)!=plan['pardonOpeningReview']['byteVerifiedReading']:raise ValueError('Prior Pardon opening differs from XML')
                print('131 Pardon main-text paragraphs/5application sections/2notes/FINIS+back boundary: PASS;not critical edition')
            else:print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if args.pardon_opening:
            result=extract_pardon_opening(args.directory,registry)
            if args.check:
                plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
                check_pardon_opening(plan,registry)
                if result!=plan['pardonOpeningReview']['byteVerifiedReading']:raise ValueError('Pardon opening differs from actual XML')
                print('60 continuous Pardon paragraphs/one note: PASS;not full discourse or independent foreign replay')
            else:print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if args.mourning_distinctions:
            result=extract_mourning(args.directory,registry)
            if args.check:
                plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
                check_mourning_distinctions(plan,registry)
                if result!=plan['mourningDistinctionReview']['byteVerifiedContexts']:raise ValueError('Stored mourning distinctions differ from XML')
                print('14 pastoral paragraphs+3 prior opening paragraphs: PASS;not full treatise or outward-protection guarantee')
            else:print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if args.pardon_distinctions:
            result=extract(args.directory,registry,tuple(PARDON_RANGES),paragraph_ranges=PARDON_RANGES)
            if args.check:
                plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
                check_pardon_distinctions(plan,registry)
                if result!=plan['pardonDistinctionReview']['byteVerifiedContexts']:raise ValueError('Stored pardon distinctions differ from XML')
                print('12 pardon paragraphs+2 prior concordances: PASS;not full treatise or independent witnesses')
            else:print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if args.regenerate_opening:
            result=extract_regenerate_opening(args.directory,registry)
            if args.check:
                plan=json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
                check_regenerate_opening(plan,registry)
                review=plan['regenerateOpeningReview']
                if result != dict(contexts=review['byteVerifiedContexts'],discourseLayout=review['discourseLayout'],marginalNotes=review['byteVerifiedMarginalNotes']):
                    raise ValueError('Opening or complete main-text layout differs from XML')
                print('Pinned opening/70 paragraph coverage layout: PASS;not critical edition or complete exegesis')
            else:print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if args.regenerate_continuation:
            result = extract(args.directory, registry, ('TXT-07',), paragraph_ranges={'TXT-07': (527,560)})
            if args.check:
                plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
                check_regenerate_continuation(plan, registry)
                if result != plan['regenerateContinuationReview']['byteVerifiedContexts']:
                    raise ValueError('Stored regenerate continuation differs from XML')
                print('One pinned source/34 paragraphs,33 beyond prior window: PASS;not full treatise or translation approval')
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        result = extract(args.directory, registry, THEOLOGY_REFS if args.theology else STUDY_REFS if args.study else REFS, THEOLOGY_AFTER if args.theology else None)
        if args.theology:
            if args.check:
                plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
                if result != plan['doctrinalDistinctionReview']['byteVerifiedContexts']:
                    raise ValueError('Stored doctrinal distinctions differ from actual XML')
                print('Two extended doctrinal contexts/two XML byte pins: PASS;not complete system or translation approval')
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        if args.study:
            if args.check:
                plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
                if result != plan['freshStudyReview']['byteVerifiedContexts']:
                    raise ValueError('Stored Scripture contexts differ from actual source bytes')
                print('Four Scripture context windows/two XML byte pins: PASS;not whole-corpus exegesis or translation approval')
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        opening = extract_mercy_opening(args.directory, registry)
        if args.check:
            plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
            if (result != plan['pastoralReview']['byteVerifiedContexts']
                    or opening != plan['pastoralReview']['mercyOpeningReview']['byteVerifiedOpening']):
                raise ValueError('Stored pastoral contexts differ from actual source bytes')
            print('Seven contexts plus authorial mercy opening/three XML byte pins: PASS;not full-work reading or publication approval')
        else:
            print(json.dumps(dict(contexts=result, mercyOpening=opening), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
