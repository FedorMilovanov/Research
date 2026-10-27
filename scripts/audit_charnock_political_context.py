#!/usr/bin/env python3
"""Pinned constitutional norms and biographical wording; not implementation proof."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_biographical_anchors import text_and_pages
from audit_charnock_handoff import canonical_bytes
ROOT = Path(__file__).resolve().parents[1]
PROBES = {
 'TITLE': ('A41722','As it was publickly declared at Westminster'),
 'XXXV': ('A41722','XXXV. That the Christian Religion'),
 'XXXVI': ('A41722','XXXVI. That to the publick Profession'),
 'XXXVII': ('A41722','XXXVII. That such as profess Faith'),
 'XXXVIII': ('A41722','XXXVIII. That all Laws'),
 'ADAMS_VEAL': ('A32726','the year after he had been Proctor'),
 'WOOD': ('A71277','that also he was good in the practice of physick'),
}
PAIRS = {
 'REASON': ('strong Reason, great Judgment','strong reason, great judgment'),
 'MEDICINE': ('a considerable measure of knowledge','a considerable measure of knowledge'),
 'ARTICLES': ('sound Doctrine laid down in the Articles of Religion','sound doctrine laid down in the articles of Religion'),
}

def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def extract(directory, registry):
    loaded={};result={}
    for key,(source_id,probe) in PROBES.items():
        pin=registry['sources'][source_id]
        if source_id not in loaded:
            raw=(directory/(source_id+'.xml')).read_bytes()
            if len(raw)!=pin['size'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']:
                raise ValueError('Political context byte pin mismatch: '+source_id)
            loaded[source_id]=(ET.fromstring(raw),text_and_pages(raw))
        root,(stream,pages)=loaded[source_id]
        nodes=root.findall('.//'+NS+'front/'+NS+'div[@type="title_page"]') if key=='TITLE' else root.iter(NS+'p')
        matches=[p for p in nodes if probe in plain(p)]
        if len(matches)!=1 or stream.count(probe)!=1:
            raise ValueError('Unique political context required: '+key)
        text=plain(matches[0]);start=stream.index(probe)
        context_at=stream.find(text)
        full_pages=list(dict.fromkeys(pages[context_at:context_at+len(text)])) if stream.count(text)==1 else None
        result[key]=dict(source=source_id,sourceSha256=pin['sha256'],sourceBytes=pin['size'],probe=probe,
                         probeTeiPages=list(dict.fromkeys(pages[start:start+len(probe)])),contextTeiPages=full_pages,text=text,textSha256=hashlib.sha256(text.encode()).hexdigest())
    return result


def check_review(plan,registry):
    review=plan['politicalContextReview'];contexts=review['byteVerifiedContexts']
    if (review['reviewState']!='BOUNDED_NORMS_AND_WORDING_NOT_IMPLEMENTATION'
        or review['implementationVerified'] is not False or review['independentWitnessesEstablished'] is not False
        or review['publicationApproval'] is not False):
        raise ValueError('Norms and verbal parallels cannot certify implementation or independence')
    if set(contexts)!=set(PROBES):
        raise ValueError('Seven full context units required')
    for key,(source_id,probe) in PROBES.items():
        c=contexts[key];pin=registry['sources'][source_id]
        if (c['source']!=source_id or c['sourceSha256']!=pin['sha256'] or c['sourceBytes']!=pin['size']
            or c['probe']!=probe or probe not in c['text'] or hashlib.sha256(c['text'].encode()).hexdigest()!=c['textSha256']):
            raise ValueError('Political context must remain source-bound')
    cards=review['normCards']
    if len(cards)!=5 or {c['contextId'] for c in cards}!={'TITLE','XXXV','XXXVI','XXXVII','XXXVIII'}:
        raise ValueError('Title plus four distinct normative readings required')
    for c in cards:
        if c['contextSha256']!=sha(contexts[c['contextId']]) or not c['allowedReading'] or not c['prohibitedInference'] or c['applicationState']!='NORM_NOT_PERSONAL_CASE':
            raise ValueError('Norm cannot be promoted to personal legal history')
    pairs=review['wordingComparisons']
    if len(pairs)!=3 or {p['id'] for p in pairs}!=set(PAIRS):
        raise ValueError('Three bounded verbal comparisons required')
    for p in pairs:
        left,right=PAIRS[p['id']]
        if (p['editorialProbe']!=left or p['woodProbe']!=right or left not in contexts['ADAMS_VEAL']['text']
            or right not in contexts['WOOD']['text'] or p['independenceState']!='NOT_ESTABLISHED'
            or p['dependencyDirectionProven'] is not False or not p['limit']):
            raise ValueError('Verbal similarity is not independent corroboration or a proven stemma')
    if review['woodMedicalVoice']!='WOOD_REPORTS_BRETHREN_ESTIMATION':
        raise ValueError('Preserve nested medical attribution')
    return dict(constitutionalContextUnits=5,biographicalWordingComparisons=3,legalImplementationVerified=False)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text());registry=json.loads((ROOT/plan['baselineRegistry']).read_text());result=extract(a.directory,registry)
        if a.check:
            check_review(plan,registry)
            if result!=plan['politicalContextReview']['byteVerifiedContexts']:
                raise ValueError('Stored political contexts differ from XML replay')
            print('Three pins/seven contexts: PASS;no implementation or independence certification')
        else:print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,ET.ParseError) as exc:p.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
