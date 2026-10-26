#!/usr/bin/env python3
"""Replay four bounded quotation contexts and TCP licence statements from pinned XML.

No network or writes. Does not certify Russian translation quality or publication.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_biographical_anchors import text_and_pages, normalize

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    'TR-TXT03': ('A32724', 'TXT-03', 'Whether the Holy Ghost alludes to a particular number of Nations'),
    'TR-TXT08': ('A32726', 'TXT-08', "'Tis not a bare sight of things that is here meant by Gods eye"),
    'TR-VEEL': ('B20167', 'BIB-06', 'The Papers I have seen'),
    'TR-MERCY': ('B20167', 'BIB-06', 'God doth often make the chiefest Sinners Objects of his choicest Mercy.'),
}


def has_explicit_tcp_text_waiver(statement):
    """Recognize the two encountered TCP notices,not a generic CC0 substring."""
    modern = all(part in statement for part in (
        'the Text Creation Partnership has waived all copyright and related or neighboring rights to this keyboarded and encoded edition',
        'according to the terms of the CC0 1.0 Public Domain Dedication',
        'This waiver does not extend to any page images or other supplementary files'))
    legacy = all(part in statement for part in (
        'This keyboarded and encoded edition of the work described above is co-owned',
        'This text is available for reuse, according to the terms of Creative Commons 0 1.0 Universal licence.',
        'The text can be copied, modified, distributed and performed, even for commercial purposes, all without asking permission.'))
    return modern or legacy


def extract(directory, registry):
    cache, records = {}, {}
    for key, (identifier, ref, probe) in TARGETS.items():
        source = registry['sources'][identifier]
        if identifier not in cache:
            raw = (directory / (identifier + '.xml')).read_bytes()
            if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
                raise ValueError(identifier + ': source byte pin mismatch')
            root = ET.fromstring(raw)
            parents = {c: p for p in root.iter() for c in p}
            pages, page = {}, None
            for n in root.iter():
                if n.tag == NS + 'pb':
                    page = n.get('n')
                pages[n] = page
            paragraphs = []
            for p in root.iter(NS + 'p'):
                a, excluded = p, False
                while a in parents:
                    a = parents[a]
                    if a.tag in {NS + 'p', NS + 'note', NS + 'fw', NS + 'teiHeader', NS + 'epigraph'}:
                        excluded = True
                if not excluded:
                    paragraphs.append(p)
            availability = root.findall('.//' + NS + 'teiHeader//' + NS + 'availability')
            if len(availability) != 1:
                raise ValueError(identifier + ': one explicit licence statement required')
            licence = availability[0]
            statement = plain(licence)
            if not has_explicit_tcp_text_waiver(statement):
                raise ValueError(identifier + ': TCP text licence not recognized;fail closed')
            cache[identifier] = (parents, pages, paragraphs, text_and_pages(raw),
                                 dict(statement=statement, statementSha256=hashlib.sha256(statement.encode()).hexdigest(),
                                      refTargets=[n.get('target') for n in licence.iter(NS + 'ref')],
                                      scope='TCP encoded text only;not page images,autographs or external editions'))
        parents, pages, paragraphs, (whole, labels), licence = cache[identifier]
        matches = [p for p in paragraphs if normalize(probe) in plain(p)]
        if len(matches) != 1 or whole.count(normalize(probe)) != 1:
            raise ValueError(key + ': probe must be unique')
        p = matches[0]
        def division(n):
            while n in parents and n.tag != NS + 'div':
                n = parents[n]
            return n
        d = division(p)
        head = d.find(NS + 'head')
        local = [n for n in paragraphs if division(n) is d]
        index = local.index(p)
        ancestors, a = [], p
        while a in parents:
            a = parents[a]
            ancestors.append(a.tag)
        zone = 'FRONT' if NS + 'front' in ancestors else 'BODY' if NS + 'body' in ancestors else None
        signatures = [plain(n) for n in d.iter(NS + 'signed')]
        voice = 'VEEL_EDITORIAL' if key == 'TR-VEEL' else 'CHARNOCK_BODY'
        if ((voice == 'VEEL_EDITORIAL' and (zone != 'FRONT' or not any('Veel' in s for s in signatures)))
                or (voice == 'CHARNOCK_BODY' and zone != 'BODY')
                or (key == 'TR-MERCY' and (head is None or plain(head) != 'Chiefest Sinners Objects of Choicest Mercy.'))):
            raise ValueError(key + ': voice/section mismatch')
        at = whole.index(normalize(probe))
        probe_pages = list(dict.fromkeys(labels[at:at + len(normalize(probe))]))
        anchor = next(a for a in registry['anchors'] if a['id'] == ref)
        if key in {'TR-TXT03', 'TR-TXT08', 'TR-VEEL'} and probe_pages != anchor['teiPages']:
            raise ValueError(key + ': printed probe locator changed')
        records[key] = dict(source=identifier, sourceBytes=source['size'], sourceSha256=source['sha256'],
                            relatedRef=ref, probe=probe, probeTeiPages=probe_pages, zone=zone, voice=voice,
                            sectionHeading=plain(head) if head is not None else None, signatures=signatures,
                            localParagraphIndexZeroBased=index, paragraphStartTeiPage=pages[p],
                            paragraphIndexScheme='Non-nested p in nearest div;epigraph,note,fw,header excluded',
                            selectedParagraph=plain(p), selectedParagraphSha256=hashlib.sha256(plain(p).encode()).hexdigest(),
                            contextWindow=[dict(localParagraphIndexZeroBased=i, startTeiPage=pages[n], text=plain(n),
                                                textSha256=hashlib.sha256(plain(n).encode()).hexdigest())
                                           for i, n in enumerate(local) if abs(i - index) <= 1],
                            licence=licence, boundary='Heading plus paragraph index;no image collation or publication approval')
    return records


def check_review(plan, registry):
    """Check provenance/holds,not the correctness of Russian semantics."""
    from audit_charnock_handoff import canonical_bytes
    review = plan['translationReview']
    if (review['reviewState'] != 'FOUR_WORKING_TRANSLATIONS_NOT_PUBLICATION_APPROVAL'
            or review['independentReviewState'] != 'NOT_PERFORMED' or review['publicationApproval'] is not False):
        raise ValueError('Working translation cannot claim independent review or publication approval')
    contexts, items = review['byteVerifiedContexts'], review['items']
    if set(contexts) != set(TARGETS) or len(items) != 4 or {q['id'] for q in items} != set(TARGETS):
        raise ValueError('Exactly four selected translation contexts/drafts required')
    axes = ['evidenceClass', 'accessState', 'locatorState', 'rightsState', 'publicationState', 'holds']
    for q in items:
        c = contexts[q['id']]
        identifier, ref, probe = TARGETS[q['id']]
        source = registry['sources'][identifier]
        voice = 'VEEL_EDITORIAL' if q['id'] == 'TR-VEEL' else 'CHARNOCK_BODY'
        if (c['source'] != identifier or c['sourceSha256'] != source['sha256'] or c['sourceBytes'] != source['size']
                or c['relatedRef'] != ref or c['probe'] != probe or probe not in c['selectedParagraph']
                or hashlib.sha256(c['selectedParagraph'].encode()).hexdigest() != c['selectedParagraphSha256']
                or c['voice'] != voice or c['zone'] != ('FRONT' if voice == 'VEEL_EDITORIAL' else 'BODY')):
            raise ValueError('Translation context source,paragraph or voice changed')
        if voice == 'VEEL_EDITORIAL' and not any('Veel' in s for s in c['signatures']):
            raise ValueError('Editorial first person must retain Veel signature')
        if q['id'] == 'TR-TXT03' and not c['selectedParagraph'].endswith('is uncertain.'):
            raise ValueError('Full TXT03 paragraph must preserve actual uncertainty ending')
        if q['id'] == 'TR-MERCY' and c['sectionHeading'] != 'Chiefest Sinners Objects of Choicest Mercy.':
            raise ValueError('Repeated pagination requires specific mercy heading')
        window = c['contextWindow']
        if (not 2 <= len(window) <= 3
                or not any(w['text'] == c['selectedParagraph'] and w['localParagraphIndexZeroBased'] == c['localParagraphIndexZeroBased'] for w in window)
                or any(hashlib.sha256(w['text'].encode()).hexdigest() != w['textSha256'] for w in window)):
            raise ValueError('Full same-section quotation context window required')
        licence = c['licence']
        if (hashlib.sha256(licence['statement'].encode()).hexdigest() != licence['statementSha256']
                or not has_explicit_tcp_text_waiver(licence['statement'])
                or licence['scope'] != 'TCP encoded text only;not page images,autographs or external editions'):
            raise ValueError('TCP licence does not approve page images or translations')
        if (q['source'] != identifier or q['relatedRef'] != ref or q['voice'] != voice
                or not q['quoteText'] or c['selectedParagraph'].count(q['quoteText']) != 1
                or hashlib.sha256(q['quoteText'].encode()).hexdigest() != q['quoteTextSha256']
                or q['quoteTeiPages'] != c['probeTeiPages']
                or any(q['sourceStateSnapshot'][k] != source[k] for k in axes)):
            raise ValueError('Selected quote must be a literal span of its own voice/edition')
        if (not q['russianDraft'] or not any('А' <= ch <= 'я' for ch in q['russianDraft'])
                or hashlib.sha256(q['russianDraft'].encode()).hexdigest() != q['russianDraftSha256']
                or q['translationMethod'] != 'AI_ASSISTED_RESEARCH_DRAFT'
                or q['translationState'] != 'WORKING_DRAFT_NOT_INDEPENDENTLY_REVIEWED'
                or q['independentReview'] != dict(state='NOT_PERFORMED', reviewer=None, reviewedTranslationSha256=None)
                or q['sourceTextRights'] != 'CC0_TCP_ENCODED_TEXT_ONLY' or q['imageRights'] != 'NOT_REVIEWED_NOT_INCLUDED'
                or len(q['notes']) < 2 or not q['boundary']):
            raise ValueError('Russian draft requires unresolved independent review and explicit translation boundaries')
    original = {q['id']: q for q in registry['researchPreparationReview']['quotationPlan']}
    decisions = review['baselineCandidateDispositions']
    if len(decisions) != 23 or {q['id'] for q in decisions} != set(original):
        raise ValueError('All23original quotation dispositions must be retained')
    for q in decisions:
        old = original[q['id']]
        expected = 'KEEP_RESEARCH_ONLY' if old['decision'] == 'RESEARCH_ONLY' else 'KEEP_CANDIDATE_WITHOUT_PUBLICATION_APPROVAL'
        if (q['originalDecision'] != old['decision'] or q['decision'] != expected
                or q['canonicalRowSha256'] != hashlib.sha256(canonical_bytes(old)).hexdigest()
                or any(q['sourceStateSnapshot'][k] != old[k] for k in axes)
                or q['relatedExcerptFollowUp'] != ('TR-TXT08' if q['id'] == 'Q-11' else None)):
            raise ValueError('Quotation candidate decision cannot remove inherited holds or promote research-only text')
    return len(items)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        registry = json.loads((ROOT / 'data/charnock-biographical-anchors-v1.json').read_text())
        records = extract(args.directory, registry)
        if args.check:
            plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
            if records != plan['translationReview']['byteVerifiedContexts']:
                raise ValueError('Stored translation contexts/licences differ from source XML')
            print('Four quotation contexts/three byte pins/TCP text licences: PASS;not independent translation review')
        else:
            print(json.dumps(records, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
