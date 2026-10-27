#!/usr/bin/env python3
"""Reference-material provenance and contextual gloss replay,not a reader chapter.

Word senses are working contextual glosses,not dictionary/translation certification.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_biographical_anchors import text_and_pages
from audit_charnock_handoff import canonical_bytes

ROOT = Path(__file__).resolve().parents[1]
TERMS = {
    'DIVINE': ('A46911','TITLE',None,'that Reverend and Excellent Divine, Mr. STEPHEN CHARNOCK'),
    'NERVOUS': ('A32723','PREFACE',2,'nothing is more nervous than his Reasonings'),
    'CONVERSATION': ('A41722','NORM',None,'the Example of a good Conversation.'),
    'PHYSICK': ('A71277','LIFE',None,'that also he was good in the practice of physick'),
    'INCORPORATED': ('A71277','LIFE',None,'In 1652 he was incorporated Master of Arts as he had stood in Cambridge'),
    'CHARITY': ('A32723','PREFACE',1,'without breach of Charity differ in among themselves'),
    'VULGAR': ('A32723','PREFACE',2,'and so makes them intelligible to Vulgar Capacities'),
    'SENSE_SOUND': ('A32723','PREFACE',1,'was more for sense than sound'),
    'NICETIES': ('A32723','PREFACE',4,'Solidity dwindles into Niceties'),
    'PORTION': ('A32723','PREFACE',0,'not as their Soveraign only, but their Portion?'),
}


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def extract(directory, registry):
    cache, contexts, usages = {}, {}, {}
    for identifier,(source_id,kind,index,probe) in TERMS.items():
        source = registry['sources'][source_id]
        if source_id not in cache:
            raw = (directory/(source_id+'.xml')).read_bytes()
            if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
                raise ValueError('Gloss source byte pin mismatch: '+source_id)
            cache[source_id] = (ET.fromstring(raw),text_and_pages(raw))
        tree,(whole,pages) = cache[source_id]
        if kind == 'PREFACE':
            candidates = tree.findall('.//'+NS+'front/'+NS+'div[@type="to_the_reader"]/'+NS+'p')
            if len(candidates) != 5:
                raise ValueError('Five direct editorial paragraphs required')
            node = candidates[index]
        elif kind == 'TITLE':
            candidates = tree.findall('.//'+NS+'front/'+NS+'div[@type="title_page"]')
            if len(candidates) != 1:
                raise ValueError('Unique Johnson title page required')
            node = candidates[0]
        else:
            candidates = [p for p in tree.iter(NS+'p') if probe in plain(p)]
            if len(candidates) != 1:
                raise ValueError('Unique life/norm paragraph required')
            node = candidates[0]
        text = plain(node)
        if probe not in text or whole.count(probe) != 1:
            raise ValueError('Gloss probe must be literal and unique: '+identifier)
        key = source_id+'-'+kind+('-'+str(index) if index is not None else '')
        contexts[key] = dict(source=source_id,sourceSha256=source['sha256'],sourceBytes=source['size'],
                             selectorKind=kind,localPrefaceParagraphIndexZeroBased=index,text=text,
                             textSha256=hashlib.sha256(text.encode()).hexdigest())
        at = whole.index(probe)
        usages[identifier] = dict(contextId=key,probe=probe,probeTeiPages=list(dict.fromkeys(pages[at:at+len(probe)])))
    return dict(contexts=contexts,usages=usages,
                normalization='Whitespace/long-s;note/fw bodies omitted in selected context,tails retained;probe pages read from full TEI stream')


def check_review(plan, registry):
    review = plan['referenceMaterialReview']
    if (review['reviewState'] != 'REFERENCE_SOURCE_SELECTION_NOT_AUTHORED_REFERENCE_CHAPTER'
            or review['readerChapterWritten'] is not False or review['dictionaryVerificationClaimed'] is not False
            or review['publicationApproval'] is not False):
        raise ValueError('Reference source selection cannot certify a chapter,dictionary or publication')
    core = {c['id']:c for c in registry['biographicalCoreReview']['items']}
    rows = review['chronologySelection']
    required = {'BCD-02','BCD-06','BCD-09','BCD-10','BCD-11','BCD-12','BCD-13','BCD-15','BCD-18','BCD-24','BCD-31','BCD-37','BCD-38','BCD-39'}
    if len(rows) != 14 or {c['coreId'] for c in rows} != required:
        raise ValueError('Fourteen bounded chronology selections required')
    for c in rows:
        old = core[c['coreId']]
        if (c['canonicalRowSha256'] != digest(old) or c['safeFormulation'] != old['safeFormulation']
                or c['refs'] != old['refs'] or c['originalDisposition'] != old['disposition']
                or not c['dateLabel'] or not c['readerCaution']):
            raise ValueError('Reference chronology cannot erase attribution,approximation or conflict')
    if next(c for c in rows if c['coreId']=='BCD-06')['dateMeaning'] != 'ACQUAINTANCE_RECOLLECTION_NOT_CONVERSION_DAY':
        raise ValueError('Calculated acquaintance year cannot become an exact conversion date')
    units = {u['id']:u for u in registry['bibliographyUnits']}
    bibliography = review['bibliographicSelection']
    if len(bibliography) != 12 or {b['unitId'] for b in bibliography} != set(units):
        raise ValueError('Seven objects/five families must remain distinct')
    for b in bibliography:
        u = units[b['unitId']]
        expected = 'TCP_TRANSCRIPTION_NOT_IMAGES' if u['unitType']=='PRINTED_OBJECT' else 'FAMILY_NOT_ACQUIRED_AS_WHOLE'
        if b['canonicalUnitSha256'] != digest(u) or b['label'] != u['label'] or b['unitType'] != u['unitType'] or b['readerAccessLabel'] != expected or not b['caution']:
            raise ValueError('Bibliographic reference cannot promote an acquisition family')
    extraction = review['byteVerifiedGlossContexts']
    glosses = review['contextualGlosses']
    if len(glosses) != 10 or {g['id'] for g in glosses} != set(TERMS) or set(extraction['usages']) != set(TERMS):
        raise ValueError('Ten contextual glosses,not a certified dictionary,required')
    for g in glosses:
        source_id,kind,index,probe = TERMS[g['id']]
        usage = extraction['usages'][g['id']]
        ctx = extraction['contexts'][usage['contextId']]
        source = registry['sources'][source_id]
        if (ctx['source'] != source_id or ctx['sourceSha256'] != source['sha256'] or ctx['sourceBytes'] != source['size']
                or ctx['selectorKind'] != kind or ctx['localPrefaceParagraphIndexZeroBased'] != index
                or hashlib.sha256(ctx['text'].encode()).hexdigest() != ctx['textSha256']
                or usage['probe'] != probe or probe not in ctx['text']
                or g['glossState'] != 'WORKING_CONTEXTUAL_GLOSS_NOT_INDEPENDENTLY_REVIEWED'
                or not g['workingMeaning'] or not g['misreadingToAvoid'] or not g['scopeLimit']):
            raise ValueError('Gloss must remain bound to a specific source context and review limit')
    physick = next(g for g in glosses if g['id']=='PHYSICK')
    if physick['sourceRole'] != 'WOOD_REPORTS_BRETHREN_ESTIMATION':
        raise ValueError('Wood reports Brethren estimation,not a medical qualification')
    if len(extraction['contexts']) != 7:
        raise ValueError('Seven unique contexts,not ten independent witnesses,required')
    doc = next(d for d in plan['documents'] if d['id']=='REFERENCE')
    if not any(h['state']=='HISTORICAL_SUPERSEDED_REFERENCE_SELECTION_PREPARED' and h['items'] for h in doc.get('remainingWorkHistory',[])):
        raise ValueError('Reference selection setup history must be preserved')
    return dict(referenceChronologySelections=14,referenceBibliographicUnits=12,contextualGlosses=10,referenceChapterWritten=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    try:
        plan = json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        registry = json.loads((ROOT/plan['baselineRegistry']).read_text())
        result = extract(args.directory,registry)
        if args.check:
            check_review(plan,registry)
            if result != plan['referenceMaterialReview']['byteVerifiedGlossContexts']:
                raise ValueError('Stored contextual gloss evidence differs from XML')
            print('Four source byte pins/ten contextual usages: PASS;not dictionary or translation certification')
        else:
            print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,ET.ParseError) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__ == '__main__':
    main()
