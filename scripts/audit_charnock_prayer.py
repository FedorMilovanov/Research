#!/usr/bin/env python3
"""Complete single-TCP Delight in Prayer coverage; not a clinical or textual edition."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from audit_charnock_book_route import NS, plain
from audit_charnock_pastoral_contexts import ROOT, source_structure

HEADING = 'A DISCOURSE OF Delight in Prayer.'
DOCTRINE = ('Doctrine. Delight in God, in seeking him only, procures gracious answers; '
            'or, without chearful prayers, we cannot have gracious answers.')
POSITIONS = [257, 261, 267, 269, 276, 280, 283, 286, 288, 289, 290, 291,
             293, 295, 296, 297, 299, 301, 302, 315, 316, 321, 322, 323,
             325, 326, 329, 331]
FALSE_FLAGS = ('criticalEditionVerified', 'preachingYearEstablished',
               'preachingPlaceEstablished', 'foreignOriginalsVerified',
               'paginationCorrected', 'clinicalMoodDiagnosisApproved',
               'instantAnswerGuaranteeApproved', 'everyDesireApproved',
               'publicationApproval')
HOLDS = {'EVIDENCE_HOLD', 'ARCHIVE_HOLD', 'RIGHTS_HOLD', 'PUBLICATION_HOLD'}


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def extract_complete(directory, registry):
    _, _, parents, pages, paragraphs = source_structure(directory, registry, 'A32724')

    def containing_div(node):
        while node in parents and node.tag != NS + 'div':
            node = parents[node]
        return node

    div = containing_div(paragraphs[256])
    indices = [i for i, p in enumerate(paragraphs) if containing_div(p) is div]
    if indices != list(range(256, 332)):
        raise ValueError('Prayer division coverage changed')
    tags = [n.tag.removeprefix(NS) for n in div]
    if any(t not in {'p', 'pb', 'head', 'epigraph', 'q'} for t in tags):
        raise ValueError('Unknown standalone Prayer unit')
    doctrines = []
    last = None
    for node in div:
        if node.tag == NS + 'p':
            last = paragraphs.index(node)
        elif node.tag == NS + 'q':
            text = plain(node)
            doctrines.append(dict(afterParagraphIndexZeroBased=last,
                                  beforeParagraphIndexZeroBased=last + 1,
                                  teiPage=pages[node], text=text,
                                  textSha256=digest(text),
                                  voice='CHARNOCK_DOCTRINAL_PROPOSITION'))
    source = registry['sources']['A32724']
    next_div = containing_div(paragraphs[332])
    return dict(
        source='A32724', sourceSha256=source['sha256'], sourceBytes=source['size'],
        sectionHeading=plain(div.find(NS + 'head')), directTags=tags,
        epigraph=plain(div.find(NS + 'epigraph')),
        contextWindow=[dict(paragraphIndexZeroBased=i, startTeiPage=pages[paragraphs[i]],
                            text=plain(paragraphs[i]), textSha256=digest(plain(paragraphs[i])))
                       for i in indices],
        standaloneDoctrine=doctrines,
        marginalNotes=[dict(parentParagraphIndexZeroBased=i, teiPage=pages[n],
                            text=' '.join(''.join(n.itertext()).replace('ſ', 's').split()))
                       for i in indices for n in paragraphs[i].iter(NS + 'note')],
        openingPageBreaks=[dict(n=n.get('n'), facs=n.get('facs'))
                           for n in list(div)[:3] if n.tag == NS + 'pb'],
        nextParagraph=dict(paragraphIndexZeroBased=332, startTeiPage=pages[paragraphs[332]],
                           sectionHeading=plain(next_div.find(NS + 'head')),
                           text=plain(paragraphs[332])))


def check_review(plan, registry):
    review = plan['prayerCompleteReview']
    data = review['byteVerifiedReading']
    source = registry['sources']['A32724']
    if (review['reviewState'] != 'COMPLETE_SINGLE_TCP_DELIGHT_IN_PRAYER_MAIN_TEXT'
            or any(review[k] is not False for k in FALSE_FLAGS)
            or data['source'] != 'A32724' or data['sourceSha256'] != source['sha256']
            or data['sourceBytes'] != source['size'] or data['sectionHeading'] != HEADING
            or review['priorBoundaryOnlyParagraphCount'] != 1
            or review['additionalMainBodyParagraphs'] != 75):
        raise ValueError('Complete Prayer coverage is not a clinical guarantee or corrected edition')
    rows = data['contextWindow']
    if ([r['paragraphIndexZeroBased'] for r in rows] != list(range(256, 332))
            or any(digest(r['text']) != r['textSha256'] for r in rows)):
        raise ValueError('All76 Prayer paragraphs required')
    tags = data['directTags']
    if (tags.count('p') != 75 or tags.count('epigraph') != 1
            or tags.count('q') != 1 or tags.count('head') != 1
            or any(t not in {'p', 'pb', 'head', 'epigraph', 'q'} for t in tags)
            or data['epigraph'] != 'Psal. 37.4. ' + rows[0]['text']
            or rows[0]['startTeiPage'] != '53' or rows[-1]['startTeiPage'] != '63'
            or data['openingPageBreaks'] != [dict(n='53', facs='tcp:41445:30')]
            or data['standaloneDoctrine'] != [dict(
                afterParagraphIndexZeroBased=269, beforeParagraphIndexZeroBased=270,
                teiPage='57', text=DOCTRINE, textSha256=digest(DOCTRINE),
                voice='CHARNOCK_DOCTRINAL_PROPOSITION')]):
        raise ValueError('Epigraph, standalone authorial q or pagination changed')
    previous = plan['fifthNovemberCompleteReview']['byteVerifiedReading']['nextParagraph']
    if previous != dict(paragraphIndexZeroBased=256, startTeiPage=rows[0]['startTeiPage'],
                        sectionHeading=HEADING, text=rows[0]['text']):
        raise ValueError('Prayer opening must match the previously saved boundary')
    following = data['nextParagraph']
    if (following['paragraphIndexZeroBased'] != 332 or following['startTeiPage'] != '64'
            or following['sectionHeading'] != 'A DISCOURSE OF Mourning for other Mens Sins.'
            or not following['text'].startswith('And the Lord said unto him, Go thorow')):
        raise ValueError('Mourning epigraph is a boundary, not part of Prayer')
    notes = data['marginalNotes']
    if notes != [dict(parentParagraphIndexZeroBased=273, teiPage='57', text='Judg. 13.20.'),
                 dict(parentParagraphIndexZeroBased=296, teiPage='60', text='Reynolds.')]:
        raise ValueError('Two notes only; Reynolds is not an acquired original')
    decisions = review['marginalNoteDecisions']
    if len(decisions) != 2:
        raise ValueError('Two note decisions required')
    for i, decision in enumerate(decisions):
        if (decision['localNoteIndex'] != i
                or decision['kind'] != ('BIBLICAL_NOTE' if i == 0 else 'SOURCE_POINTER')
                or decision['noteSha256'] != digest(notes[i]['text'])
                or decision['counterpartRawAcquired'] is not False or not decision['limit']):
            raise ValueError('Do not promote a note to foreign-original verification')
    observations = review['observations']
    if [o['paragraphIndexZeroBased'] for o in observations] != POSITIONS:
        raise ValueError('28 source-bounded Prayer observations required')
    paragraphs = {r['paragraphIndexZeroBased']: r for r in rows}
    for observation in observations:
        span = observation['englishSpan']
        if (not span or span not in paragraphs[observation['paragraphIndexZeroBased']]['text']
                or digest(span) != observation['englishSpanSha256']
                or not observation['observation'] or not observation['prohibitedInference']):
            raise ValueError('Observation needs an actual span and limit')
    for row in [review] + observations + decisions:
        if (row['evidenceClass'] != 'C' or row['accessState'] != 'FULL_OBJECT_VERIFIED'
                or row['locatorState'] != 'EXACT_LOCATOR_VERIFIED'
                or row['rightsState'] != 'RIGHTS_UNKNOWN'
                or row['publicationState'] != 'BLOCKED' or set(row['holds']) != HOLDS):
            raise ValueError('Coverage cannot release the independent evidence axes or HOLDs')
    if 'prayerCompleteReview' not in next(
            d for d in plan['documents'] if d['id'] == 'VII')['supplementaryMainTextReadings']:
        raise ValueError('PartVII must link the complete Prayer reading')
    return dict(prayerMainTextParagraphs=76, prayerMainTextUnits=77,
                prayerAdditionalMainBodyParagraphs=75, prayerMarginalNotes=2,
                prayerObservations=28, prayerWholeMainTextRead=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        registry = json.loads((ROOT / plan['baselineRegistry']).read_text())
        reading = extract_complete(args.directory, registry)
        if args.check:
            check_review(plan, registry)
            if reading != plan['prayerCompleteReview']['byteVerifiedReading']:
                raise ValueError('Prayer reading differs from pinned XML')
            print('76paragraphs+authorial doctrine/2notes/boundaries: PASS;not a clinical or corrected edition')
        else:
            print(json.dumps(reading, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
