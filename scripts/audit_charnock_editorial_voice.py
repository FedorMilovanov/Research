#!/usr/bin/env python3
"""Replay the five-paragraph 1682 preface and two selected authorial arguments.

TCP text only,not autograph verification,objection frequency or translation approval.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_handoff import canonical_bytes

ROOT = Path(__file__).resolve().parents[1]
PROBES = {
    'VOICE-OMNIPRESENCE': "But as to this Case; since tho' God be present in every thing",
    'VOICE-PATIENCE': 'It seems thus, that slowness to Anger is brought in as an objection against the revenge proclaimed.',
}


def extract(path, registry):
    source = registry['sources']['A32723']
    raw = path.read_bytes()
    if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
        raise ValueError('A32723 source byte pin mismatch')
    root = ET.fromstring(raw)
    matches = root.findall('.//' + NS + 'text/' + NS + 'front/' + NS + 'div[@type="to_the_reader"]')
    if len(matches) != 1:
        raise ValueError('One explicit front/to_the_reader required')
    preface = matches[0]
    head = preface.find(NS + 'head')
    signatures = [plain(n) for n in preface.iter(NS + 'signed')]
    if head is None or plain(head) != 'TO THE READER.' or not any('EDW. VEEL.' in s and 'RI. ADAMS.' in s for s in signatures):
        raise ValueError('Preface heading and joint signature required')
    paragraphs = preface.findall(NS + 'p')
    if len(paragraphs) != 5:
        raise ValueError('Five direct preface paragraphs required')
    page, at = None, {}
    for n in root.iter():
        if n.tag == NS + 'pb':
            page = n.get('n')
        at[n] = page
    def record(p):
        text = plain(p)
        return dict(text=text, textSha256=hashlib.sha256(text.encode()).hexdigest(), startTeiPage=at[p],
                    numberedBreaks=[n.get('n') for n in p.iter(NS + 'pb') if n.get('n')])
    parents = {c:p for p in root.iter() for c in p}
    tests = {}
    for key, probe in PROBES.items():
        found = []
        for d in root.findall('.//' + NS + 'body//' + NS + 'div[@type="discourse"]'):
            local = []
            for p in d.iter(NS + 'p'):
                a, excluded = p, False
                while a in parents and a is not d:
                    a = parents[a]
                    if a.tag in {NS + 'p', NS + 'note', NS + 'fw'}:
                        excluded = True
                if not excluded:
                    local.append(p)
            for i, p in enumerate(local):
                if probe in plain(p):
                    found.append((d, i, p))
        if len(found) != 1:
            raise ValueError('One authorial paragraph required for ' + key)
        d, index, p = found[0]
        tests[key] = dict(sectionHeading=plain(d.find(NS + 'head')), localDiscourseParagraphIndexZeroBased=index,
                          probe=probe, paragraph=record(p), voice='CHARNOCK_BODY')
    return dict(source='A32723', sourceSha256=source['sha256'], sourceBytes=source['size'],
                prefaceHeading=plain(head), signatures=signatures,
                normalization='Whitespace/long-s;note/fw bodies omitted,tails retained',
                prefaceParagraphs=[dict(localDirectParagraphIndexZeroBased=i, **record(p)) for i,p in enumerate(paragraphs)],
                authorContexts=tests, locatorBoundary='Preface:direct p index;body:non-nested p within discourse,note/fw excluded;front unnumbered')


def check_review(plan, registry):
    review = plan['editorialVoiceReview']
    data = review['byteVerifiedExtraction']
    source = registry['sources']['A32723']
    if (review['reviewState'] != 'FIVE_EDITORIAL_PARAGRAPHS_TWO_AUTHORIAL_TESTS'
            or review['objectionFrequencyMeasured'] is not False or review['autographsVerified'] is not False
            or data['sourceSha256'] != source['sha256'] or data['sourceBytes'] != source['size']
            or len(data['prefaceParagraphs']) != 5 or [p['localDirectParagraphIndexZeroBased'] for p in data['prefaceParagraphs']] != list(range(5)) or set(data['authorContexts']) != set(PROBES)
            or not any('EDW. VEEL.' in s and 'RI. ADAMS.' in s for s in data['signatures'])):
        raise ValueError('Editorial voice review cannot certify autographs or objection frequency')
    for para in data['prefaceParagraphs'] + [c['paragraph'] for c in data['authorContexts'].values()]:
        if hashlib.sha256(para['text'].encode()).hexdigest() != para['textSha256']:
            raise ValueError('Editorial/authorial paragraph hash differs')
    cards = review['readingCards']
    if len(cards) != 5 or [c['paragraphIndex'] for c in cards] != list(range(5)):
        raise ValueError('Five editorial reading cards required')
    for c in cards:
        if c['voice'] != 'VEEL_ADAMS_EDITORIAL' or not c['limitedConclusion'] or not c['readingToAvoid']:
            raise ValueError('Editorial judgments cannot become Charnock self-description')
    tests = review['authorTests']
    if len(tests) != 2 or {t['id'] for t in tests} != set(PROBES):
        raise ValueError('Two authorial argument tests required')
    for t in tests:
        c = data['authorContexts'][t['id']]
        if (t['voice'] != 'CHARNOCK_BODY' or PROBES[t['id']] not in c['paragraph']['text']
                or not t['rejectedInference'] or t['rejectedInference'] not in c['paragraph']['text']
                or not t['authorAnswer'] or t['authorAnswer'] not in c['paragraph']['text'] or not t['boundary']
                or t['provesPrefaceFrequency'] is not False):
            raise ValueError('Authorial argument test must distinguish objection,answer and frequency limit')
    speech = review['reportedSpeech']
    if (speech['paragraphIndex'] != 1 or not speech['span'] or speech['span'] not in data['prefaceParagraphs'][1]['text']
            or 'but said,' not in speech['span'] or speech['state'] != 'EDITORIALLY_REPORTED_NOT_AUTOGRAPH'
            or speech['independentVerbatimWitness'] is not False):
        raise ValueError('Reported speech must remain an editorial report,not an independent autograph quotation')
    history = plan['documents'][2].get('remainingWorkHistory', [])
    if not history or history[0]['state'] != 'HISTORICAL_SUPERSEDED_AFTER_PAIR_PACKETS' or not history[0]['items']:
        raise ValueError('Superseded partII queue must remain in explicit history')
    quotations = {q['id']:q for q in registry['researchPreparationReview']['quotationPlan']}
    followups = review['quotationFollowUps']
    if len(followups) != 3 or {q['id'] for q in followups} != {'Q-04','Q-05','Q-10'}:
        raise ValueError('Three bounded quotation follow-ups required')
    for q in followups:
        old = quotations[q['id']]
        if (q['canonicalRowSha256'] != hashlib.sha256(canonical_bytes(old)).hexdigest()
                or old['quoteText'] not in data['prefaceParagraphs'][q['paragraphIndex']]['text']
                or q['voice'] != 'VEEL_ADAMS_EDITORIAL' or q['translationState'] != 'NOT_PREPARED'
                or q['publicationApproval'] is not False):
            raise ValueError('Fresh English context cannot approve translation/publication or change editorial voice')
    return dict(freshPrefaceParagraphs=5, authorialMethodTests=2, freshEditorialQuotationContexts=3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml',type=Path)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    try:
        registry = json.loads((ROOT / 'data/charnock-biographical-anchors-v1.json').read_text())
        data = extract(args.xml,registry)
        if args.check:
            plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
            check_review(plan,registry)
            if data != plan['editorialVoiceReview']['byteVerifiedExtraction']:
                raise ValueError('Stored preface/authorial contexts differ from pinned XML')
            print('Five preface paragraphs/two authorial tests: PASS;not autograph,frequency or translation approval')
        else:
            print(json.dumps(data,ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,ET.ParseError) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__ == '__main__':
    main()
