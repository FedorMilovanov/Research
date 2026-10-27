#!/usr/bin/env python3
"""Replay one complete, pinned TCP Fifth of November main text, not an edition."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from audit_charnock_book_route import NS, plain
from audit_charnock_handoff import canonical_bytes
from audit_charnock_pastoral_contexts import ROOT, extract, source_structure

HEADING = 'A DISCOURSE UPON THE Fifth of November.'
POSITIONS = [186, 188, 189, 194, 197, 200, 203, 205, 206, 208, 213,
             218, 220, 221, 222, 223, 229, 230, 233, 239, 241, 244,
             246, 248, 249, 250, 251, 252, 253, 254, 255]
HOLDS = {'EVIDENCE_HOLD', 'ARCHIVE_HOLD', 'RIGHTS_HOLD', 'PUBLICATION_HOLD'}
FALSE_FLAGS = ('criticalEditionVerified', 'preachingYearEstablished',
               'preachingPlaceEstablished', 'foreignOriginalsVerified',
               'paginationCorrected', 'apocalypticNumberCorrected',
               'modernCollectiveBlameApproved', 'modernViolenceMandateApproved',
               'clinicalFaithDiagnosisApproved', 'publicationApproval')


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def extract_complete(directory, registry):
    context = extract(directory, registry, ('TXT-19',),
                      paragraph_ranges={'TXT-19': (185, 255)})['TXT-19']
    _, _, parents, pages, paragraphs = source_structure(directory, registry, 'A32724')

    def containing_div(node):
        while node in parents and node.tag != NS + 'div':
            node = parents[node]
        return node

    div = containing_div(paragraphs[185])
    indices = [i for i, p in enumerate(paragraphs) if containing_div(p) is div]
    if indices != list(range(185, 256)):
        raise ValueError('Fifth of November main-text boundary changed')
    tags = [n.tag.removeprefix(NS) for n in div]
    if tags.count('p') != 70 or tags.count('epigraph') != 1 or any(
            t not in {'p', 'head', 'epigraph', 'pb'} for t in tags):
        raise ValueError('Unexpected standalone main-text unit')
    next_div = containing_div(paragraphs[256])
    return dict(
        context=context, directTags=tags,
        epigraph=plain(div.find(NS + 'epigraph')),
        marginalNotes=[dict(parentParagraphIndexZeroBased=i, teiPage=pages[n],
                            text=' '.join(''.join(n.itertext()).replace('ſ', 's').split()))
                       for i in indices for n in paragraphs[i].iter(NS + 'note')],
        nextParagraph=dict(paragraphIndexZeroBased=256,
                           startTeiPage=pages[paragraphs[256]],
                           sectionHeading=plain(next_div.find(NS + 'head')),
                           text=plain(paragraphs[256])),
        nextOpeningPageBreaks=[dict(n=n.get('n'), facs=n.get('facs'))
                              for n in list(next_div)[:3] if n.tag == NS + 'pb'])


def check_review(plan, registry):
    review = plan['fifthNovemberCompleteReview']
    data = review['byteVerifiedReading']
    context = data['context']
    source = registry['sources']['A32724']
    if (review['reviewState'] != 'COMPLETE_SINGLE_TCP_FIFTH_NOVEMBER_MAIN_TEXT'
            or any(review[k] is not False for k in FALSE_FLAGS)
            or review['priorParagraphCount'] != 3
            or review['additionalCoverageParagraphCount'] != 68
            or context['source'] != 'A32724'
            or context['sourceSha256'] != source['sha256']
            or context['sourceBytes'] != source['size']
            or context['sectionHeading'] != HEADING
            or context['rangeOverrideStartEndInclusive'] != [185, 255]
            or context['anchorProbeInsideWindow'] is not True):
        raise ValueError('Single TCP coverage is not a dated, located, corrected edition')
    rows = context['contextWindow']
    if ([r['paragraphIndexZeroBased'] for r in rows] != list(range(185, 256))
            or any(digest(r['text']) != r['textSha256'] for r in rows)):
        raise ValueError('71 full paragraphs required')
    prior = plan['pastoralReview']['byteVerifiedContexts']['TXT-19']
    if (rows[:3] != prior['contextWindow']
            or review['priorContextSha256'] != hashlib.sha256(canonical_bytes(prior)).hexdigest()):
        raise ValueError('Historical three-paragraph TXT-19 reading must remain unchanged')
    tags = data['directTags']
    if (tags.count('p') != 70 or tags.count('epigraph') != 1
            or tags.count('head') != 1
            or any(t not in {'p', 'head', 'epigraph', 'pb'} for t in tags)
            or data['epigraph'] != 'Exod. 15.9, 10. ' + rows[0]['text']
            or data['nextParagraph'] != dict(
                paragraphIndexZeroBased=256, startTeiPage='53',
                sectionHeading='A DISCOURSE OF Delight in Prayer.',
                text='Delight thy self also in the Lord, and he shall give thee the desires of thy heart.')
            or rows[-1]['startTeiPage'] != '55'
            or data['nextOpeningPageBreaks'] != [dict(n='53', facs='tcp:41445:30')]):
        raise ValueError('Epigraph, body or uncorrected55-to53 boundary differs')
    notes = data['marginalNotes']
    decisions = review['marginalNoteDecisions']
    if ([n['parentParagraphIndexZeroBased'] for n in notes] != [198, 203, 218, 218, 219, 239, 248]
            or len(decisions) != 7):
        raise ValueError('Seven marginal notes, not seven independent authors')
    kinds = ['LEXICAL_NOTE', 'SOURCE_POINTER', 'BIBLICAL_AND_POLEMICAL_COMMENT',
             'SOURCE_POINTER', 'BIBLICAL_NOTE', 'BIBLICAL_NOTE', 'SOURCE_POINTER']
    for i, decision in enumerate(decisions):
        if (decision['localNoteIndex'] != i or decision['kind'] != kinds[i]
                or decision['noteSha256'] != digest(notes[i]['text'])
                or decision['counterpartRawAcquired'] is not False or not decision['limit']):
            raise ValueError('Marginal attribution is not foreign-original verification')
    observations = review['observations']
    if [o['paragraphIndexZeroBased'] for o in observations] != POSITIONS:
        raise ValueError('31 source-bounded observations required')
    paragraphs = {r['paragraphIndexZeroBased']: r for r in rows}
    for observation in observations:
        span = observation['englishSpan']
        if (not span or span not in paragraphs[observation['paragraphIndexZeroBased']]['text']
                or digest(span) != observation['englishSpanSha256']
                or not observation['observation'] or not observation['prohibitedInference']):
            raise ValueError('Observation needs an actual English span and explicit limit')
    for row in [review] + observations + decisions:
        if (row['evidenceClass'] != 'C' or row['accessState'] != 'FULL_OBJECT_VERIFIED'
                or row['locatorState'] != 'EXACT_LOCATOR_VERIFIED'
                or row['rightsState'] != 'RIGHTS_UNKNOWN'
                or row['publicationState'] != 'BLOCKED' or set(row['holds']) != HOLDS):
            raise ValueError('Coverage does not release the independent axes or HOLDs')
    if 'One thousand six hundred and twenty years' not in paragraphs[250]['text']:
        raise ValueError('Do not silently substitute1260 or infer a preaching year')
    if 'fifthNovemberCompleteReview' not in next(
            d for d in plan['documents'] if d['id'] == 'VII')['supplementaryMainTextReadings']:
        raise ValueError('Complete reading must be integrated into PartVII')
    if review['politicalContextLink'] != 'politicalContextReview; norms and wording, not personal implementation':
        raise ValueError('Political comparison is not legal implementation proof')
    return dict(fifthNovemberMainTextParagraphs=71, fifthNovemberAdditionalParagraphs=68,
                fifthNovemberMarginalNotes=7, fifthNovemberObservations=31,
                fifthNovemberWholeMainTextRead=True, fifthNovemberPreachingYearVerified=False)


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
            if reading != plan['fifthNovemberCompleteReview']['byteVerifiedReading']:
                raise ValueError('Complete Fifth of November differs from pinned XML')
            print('71paragraphs/7notes/55-to53 boundary: PASS;not a dated or corrected edition')
        else:
            print(json.dumps(reading, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
