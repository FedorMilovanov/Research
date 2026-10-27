#!/usr/bin/env python3
"""Pinned opening or complete single-TCP Thoughts; neither a critical nor clinical edition."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from audit_charnock_book_route import NS, plain
from audit_charnock_pastoral_contexts import ROOT, source_structure

HEADING = 'A DISCOURSE OF THE Sinfulness and Cure OF THOUGHTS.'
POSITIONS = [4, 6, 7, 8, 10, 13, 14, 16, 18, 23, 24, 25, 26, 31, 32,
             33, 34, 36, 37, 38, 40]
SOURCE_POINTERS = {2, 3, 4, 6, 7, 25, 29}
NOTE_PARENTS = [4, 4, 4, 6, 6, 9, 10, 13, 18, 24, 24, 25, 25, 25,
                26, 28, 28, 29, 30, 31, 31, 33, 33, 33, 34, 37, 37,
                37, 37, 38, 40, 40, 40, 40]
FALSE_FLAGS = ('wholeDiscourseRead', 'cureSectionRead', 'criticalEditionVerified',
               'directCartesianDependenceVerified', 'counterpartOriginalVerified',
               'clinicalThoughtDiagnosisApproved', 'modernCollectiveBlameApproved',
               'originalLanguageGapsReconstructed', 'publicationApproval')
HOLDS = {'EVIDENCE_HOLD', 'ARCHIVE_HOLD', 'RIGHTS_HOLD', 'PUBLICATION_HOLD'}


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def note_kind(index):
    if index in SOURCE_POINTERS:
        return 'SOURCE_POINTER'
    return 'BIBLICAL_LEXICAL_WITH_TARGUM' if index == 33 else 'BIBLICAL_OR_LEXICAL_NOTE'


def extract_opening(directory, registry):
    _, _, parents, pages, paragraphs = source_structure(directory, registry, 'A32724')
    div = paragraphs[3]
    while div in parents and div.tag != NS + 'div':
        div = parents[div]
    last = None
    standalone = []
    for node in div:
        if node.tag == NS + 'p':
            last = paragraphs.index(node)
        elif node.tag == NS + 'q' and last is not None and 3 <= last <= 40:
            standalone.append(plain(node))
    source = registry['sources']['A32724']
    return dict(
        source='A32724', sourceSha256=source['sha256'], sourceBytes=source['size'],
        sectionHeading=plain(div.find(NS + 'head')),
        rangeStartEndInclusive=[3, 40], epigraph=plain(div.find(NS + 'epigraph')),
        contextWindow=[dict(paragraphIndexZeroBased=i, startTeiPage=pages[paragraphs[i]],
                            text=plain(paragraphs[i]), textSha256=digest(plain(paragraphs[i])))
                       for i in range(3, 41)],
        authorialPropositionParagraphIndex=12, standaloneQuotes=standalone,
        marginalNotes=[dict(parentParagraphIndexZeroBased=i, teiPage=pages[n],
                            text=' '.join(''.join(n.itertext()).replace('ſ', 's').split()))
                       for i in range(3, 41) for n in paragraphs[i].iter(NS + 'note')],
        nextParagraph=dict(paragraphIndexZeroBased=41, startTeiPage=pages[paragraphs[41]],
                           text=plain(paragraphs[41]), boundary='SAME_DISCOURSE_CONTINUES'))


def check_review(plan, registry):
    review = plan['thoughtsOpeningReview']
    data = review['byteVerifiedReading']
    source = registry['sources']['A32724']
    if (review['reviewState'] != 'BOUNDED_TCP_THOUGHTS_OPENING_DEFINITIONS_NOT_CURE'
            or any(review[k] is not False for k in FALSE_FLAGS)
            or data['source'] != 'A32724' or data['sourceSha256'] != source['sha256']
            or data['sourceBytes'] != source['size'] or data['sectionHeading'] != HEADING
            or data['rangeStartEndInclusive'] != [3, 40]
            or review['coverageNotClaimedHere'] != [41, 91]):
        raise ValueError('Bounded Thoughts opening cannot certify whole discourse, cure or diagnosis')
    rows = data['contextWindow']
    if ([r['paragraphIndexZeroBased'] for r in rows] != list(range(3, 41))
            or any(digest(r['text']) != r['textSha256'] for r in rows)
            or data['epigraph'] != 'Gen. 6.5. ' + rows[0]['text']
            or data['standaloneQuotes'] != [] or data['authorialPropositionParagraphIndex'] != 12
            or rows[12 - 3]['text'] != ('That the thoughts, and inward operations of the souls of men, '
                                      'are naturally universally evil, and highly provoking.')
            or data['nextParagraph'] != dict(
                paragraphIndexZeroBased=41, startTeiPage='6',
                text='There are three Reasons for the proof of this, that they are Sins.',
                boundary='SAME_DISCOURSE_CONTINUES')):
        raise ValueError('38paragraphs, authorial proposition12 and continuation41 required')
    notes = data['marginalNotes']
    decisions = review['marginalNoteDecisions']
    if ([n['parentParagraphIndexZeroBased'] for n in notes] != NOTE_PARENTS
            or len(decisions) != 34 or notes[-1]['teiPage'] != '6'):
        raise ValueError('34notes required, with cross-page note40 retained')
    for i, decision in enumerate(decisions):
        if (decision['localNoteIndex'] != i or decision['kind'] != note_kind(i)
                or decision['noteSha256'] != digest(notes[i]['text'])
                or decision['counterpartRawAcquired'] is not False or not decision['limit']):
            raise ValueError('Printed pointers and mixed notes are not acquired originals')
    observations = review['observations']
    if [o['paragraphIndexZeroBased'] for o in observations] != POSITIONS:
        raise ValueError('21 bounded Thoughts observations required')
    paragraphs = {r['paragraphIndexZeroBased']: r for r in rows}
    for observation in observations:
        span = observation['englishSpan']
        if (not span or span not in paragraphs[observation['paragraphIndexZeroBased']]['text']
                or digest(span) != observation['englishSpanSha256']
                or not observation['observation'] or not observation['prohibitedInference']):
            raise ValueError('Observation requires actual span and inference limit')
    for row in [review] + observations + decisions:
        if (row['evidenceClass'] != 'C' or row['accessState'] != 'FULL_OBJECT_VERIFIED'
                or row['locatorState'] != 'EXACT_LOCATOR_VERIFIED'
                or row['rightsState'] != 'RIGHTS_UNKNOWN' or row['publicationState'] != 'BLOCKED'
                or set(row['holds']) != HOLDS):
            raise ValueError('Keep evidence class, access, locator, rights and publication separate')
    search = review['cartesianCounterpartSearch']
    if (search['state'] != 'BOUNDED_DISCOVERY_NO_VERIFIED_COUNTERPART'
            or search['originalLatinCompared'] is not False
            or search['originalRawAcquired'] is not False
            or search['resultsExhausted'] is not False
            or search['claimOfGlobalAbsence'] is not False
            or not search['queries'] or not search['limits']
            or search['evidenceClass'] != 'C' or search['accessState'] != 'CATALOG_ONLY'
            or search['locatorState'] != 'COARSE_LOCATOR_ONLY'
            or search['rightsState'] != 'RIGHTS_UNKNOWN' or search['publicationState'] != 'BLOCKED'
            or set(search['holds']) != HOLDS | {'LOCATOR_HOLD'}):
        raise ValueError('Search hits are not an original counterpart, global absence or dependence proof')
    if 'thoughtsOpeningReview' not in next(
            d for d in plan['documents'] if d['id'] == 'VII').get('supplementaryOpeningReadings', []):
        raise ValueError('Bounded opening must be integrated without claiming completion')
    return dict(thoughtsOpeningParagraphs=38, thoughtsOpeningMarginalNotes=34,
                thoughtsOpeningObservations=21, thoughtsWholeDiscourseRead=False,
                thoughtsCureSectionRead=False, cartesianCounterpartVerified=False)



CONTINUATION_POSITIONS = [42, 43, 44, 45, 47, 51, 53, 55, 57, 60, 63, 64,
                          65, 66, 67, 68, 69, 72, 73, 75, 77, 79, 81, 82,
                          83, 84, 85, 87, 88, 89, 90, 91]
CONTINUATION_POINTERS = {40, 45, 56, 58, 62, 63, 64, 65, 66, 74, 79, 80,
                         94, 105, 107, 109, 114, 122, 131}
COMPLETE_FALSE_FLAGS = tuple(k for k in FALSE_FLAGS if k not in
                             {'wholeDiscourseRead', 'cureSectionRead'}) + (
                                 'allWorksRead', 'privateImpressionAuthorityApproved',
                                 'therapeuticEfficacyEstablished', 'preachingYearEstablished')
VOLUME_RANGES = [(3, 91), (92, 184), (185, 255), (256, 331), (332, 402),
                 (403, 490), (491, 560), (561, 691)]
VOLUME_REVIEWS = ['thoughtsCompleteReview', 'stabilityCompleteReview',
                  'fifthNovemberCompleteReview', 'prayerCompleteReview',
                  'mourningCompleteReview', 'childbearingReview',
                  'regenerateOpeningReview', 'pardonCompleteReview']


def complete_note_kind(index):
    if index < 34:
        return note_kind(index)
    if index in CONTINUATION_POINTERS:
        return 'SOURCE_POINTER'
    return {84: 'BIBLICAL_WITH_UNATTRIBUTED_LATIN',
            87: 'AUTHORIAL_METHOD_NOTE',
            112: 'UNATTRIBUTED_LATIN_ANNOTATION'}.get(index, 'BIBLICAL_OR_LEXICAL_NOTE')


def extract_complete(directory, registry):
    _, root, parents, pages, paragraphs = source_structure(directory, registry, 'A32724')

    def containing_div(node):
        while node in parents and node.tag != NS + 'div':
            node = parents[node]
        return node

    div = containing_div(paragraphs[3])
    indices = [i for i, p in enumerate(paragraphs) if containing_div(p) is div]
    if indices != list(range(3, 92)):
        raise ValueError('Thoughts full main-text boundary differs')
    tags = [n.tag.removeprefix(NS) for n in div]
    if any(t not in {'p', 'pb', 'head', 'epigraph'} for t in tags):
        raise ValueError('Unexpected standalone Thoughts unit')
    def within(node, ancestor):
        while node in parents:
            node = parents[node]
            if node is ancestor:
                return True
        return False

    volume_ranges = []
    for body_div in root.findall('.//' + NS + 'body/' + NS + 'div'):
        numbers = [i for i, p in enumerate(paragraphs) if within(p, body_div)]
        volume_ranges.append(dict(start=numbers[0], end=numbers[-1],
                                  heading=plain(body_div.find(NS + 'head'))))
    source = registry['sources']['A32724']
    return dict(
        source='A32724', sourceSha256=source['sha256'], sourceBytes=source['size'],
        sectionHeading=plain(div.find(NS + 'head')), directTags=tags,
        epigraph=plain(div.find(NS + 'epigraph')),
        mainTextManifest=[dict(paragraphIndexZeroBased=i, startTeiPage=pages[paragraphs[i]],
                               textSha256=digest(plain(paragraphs[i]))) for i in indices],
        continuationContextWindow=[dict(paragraphIndexZeroBased=i,
                                         startTeiPage=pages[paragraphs[i]],
                                         text=plain(paragraphs[i]),
                                         textSha256=digest(plain(paragraphs[i])))
                                    for i in range(41, 92)],
        marginalNotes=[dict(parentParagraphIndexZeroBased=i, teiPage=pages[n],
                            text=' '.join(''.join(n.itertext()).replace('ſ', 's').split()))
                       for i in indices for n in paragraphs[i].iter(NS + 'note')],
        nextParagraph=dict(paragraphIndexZeroBased=92, startTeiPage=pages[paragraphs[92]],
                           sectionHeading=plain(containing_div(paragraphs[92]).find(NS + 'head')),
                           text=plain(paragraphs[92])), volumeMainTextRanges=volume_ranges)


def check_complete(plan, registry):
    review = plan['thoughtsCompleteReview']
    data = review['byteVerifiedReading']
    opening = plan['thoughtsOpeningReview']['byteVerifiedReading']
    source = registry['sources']['A32724']
    if (review['reviewState'] != 'COMPLETE_SINGLE_TCP_THOUGHTS_MAIN_TEXT_AND_CURE'
            or review['wholeDiscourseRead'] is not True or review['cureSectionRead'] is not True
            or any(review[k] is not False for k in COMPLETE_FALSE_FLAGS)
            or review['priorParagraphCount'] != 38 or review['additionalParagraphCount'] != 51
            or data['source'] != 'A32724' or data['sourceSha256'] != source['sha256']
            or data['sourceBytes'] != source['size'] or data['sectionHeading'] != HEADING):
        raise ValueError('Complete one-TCP Thoughts is not all works, clinical efficacy or authority for impressions')
    tail = data['continuationContextWindow']
    if [r['paragraphIndexZeroBased'] for r in tail] != list(range(41, 92)):
        raise ValueError('51 continuation paragraphs required')
    rows = opening['contextWindow'] + tail
    if (len(rows) != 89 or any(digest(r['text']) != r['textSha256'] for r in rows)
            or data['mainTextManifest'] != [dict(paragraphIndexZeroBased=r['paragraphIndexZeroBased'],
                                                startTeiPage=r['startTeiPage'], textSha256=r['textSha256'])
                                           for r in rows]):
        raise ValueError('89 Thoughts paragraphs must remain tied to actual contexts')
    tags = data['directTags']
    if (tags.count('p') != 88 or tags.count('epigraph') != 1 or tags.count('head') != 1
            or any(t not in {'p', 'pb', 'head', 'epigraph'} for t in tags)
            or data['epigraph'] != opening['epigraph']):
        raise ValueError('Thoughts proposition12 is included, not an additional q')
    start = plan['stabilityOpeningReview']['byteVerifiedReading']['context']['contextWindow'][0]
    if data['nextParagraph'] != dict(paragraphIndexZeroBased=92,
                                     startTeiPage=start['startTeiPage'], text=start['text'],
                                     sectionHeading='A DISCOURSE OF THE CHURCHES STABILITY.'):
        raise ValueError('Stability92 is a boundary, not the end of Thoughts')
    notes = data['marginalNotes']
    decisions = review['additionalMarginalNoteDecisions']
    if (len(notes) != 139 or notes[:34] != opening['marginalNotes']
            or len(decisions) != 105
            or any(not 41 <= n['parentParagraphIndexZeroBased'] <= 91 for n in notes[34:])
            or notes[-1]['teiPage'] != '19'):
        raise ValueError('139notes=34historical+105continuation, including terminal page19')
    for i, decision in enumerate(decisions, 34):
        if (decision['localNoteIndex'] != i or decision['kind'] != complete_note_kind(i)
                or decision['noteSha256'] != digest(notes[i]['text'])
                or decision['counterpartRawAcquired'] is not False or not decision['limit']):
            raise ValueError('Additional pointers, Latin and method notes do not certify originals')
    paragraphs = {r['paragraphIndexZeroBased']: r for r in rows}
    observations = review['observations']
    if [o['paragraphIndexZeroBased'] for o in observations] != CONTINUATION_POSITIONS:
        raise ValueError('32 bounded continuation observations required')
    for observation in observations:
        span = observation['englishSpan']
        if (not span or span not in paragraphs[observation['paragraphIndexZeroBased']]['text']
                or digest(span) != observation['englishSpanSha256']
                or not observation['observation'] or not observation['prohibitedInference']):
            raise ValueError('Continuation observation requires actual English span and limit')
    for row in [review] + observations + decisions:
        if (row['evidenceClass'] != 'C' or row['accessState'] != 'FULL_OBJECT_VERIFIED'
                or row['locatorState'] != 'EXACT_LOCATOR_VERIFIED'
                or row['rightsState'] != 'RIGHTS_UNKNOWN' or row['publicationState'] != 'BLOCKED'
                or set(row['holds']) != HOLDS):
            raise ValueError('Full reading does not remove evidence, archive, rights or publication HOLD')
    ranges = data['volumeMainTextRanges']
    if ([(r['start'], r['end']) for r in ranges] != VOLUME_RANGES
            or [r['heading'] for r in ranges[:1]] != [HEADING]
            or review['volumeMainTextReviewLinks'] != VOLUME_REVIEWS
            or any(key not in plan for key in VOLUME_REVIEWS)):
        raise ValueError('Eight main-text routes of this TCP volume only, not eight publication-ready chapters')
    if 'thoughtsCompleteReview' not in next(
            d for d in plan['documents'] if d['id'] == 'VII')['supplementaryMainTextReadings']:
        raise ValueError('Full Thoughts must be integrated while preserving the opening history')
    return dict(thoughtsMainTextParagraphs=89, thoughtsAdditionalParagraphs=51,
                thoughtsMarginalNotes=139, thoughtsContinuationObservations=32,
                thoughtsWholeDiscourseRead=True, thoughtsCureSectionRead=True,
                oneTcpVolumeMainTextRoutes=8, allCharnockWorksRead=False)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--complete', action='store_true', help='Replay full Thoughts, retaining historical opening scope')
    args = parser.parse_args()
    try:
        plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        registry = json.loads((ROOT / plan['baselineRegistry']).read_text())
        if args.complete:
            reading = extract_complete(args.directory, registry)
            if args.check:
                check_review(plan, registry)
                check_complete(plan, registry)
                if reading != plan['thoughtsCompleteReview']['byteVerifiedReading']:
                    raise ValueError('Complete Thoughts differs from pinned XML')
                if extract_opening(args.directory, registry) != plan['thoughtsOpeningReview']['byteVerifiedReading']:
                    raise ValueError('Historical Thoughts opening differs from XML')
                print('89paragraphs/139notes/cure/end+8volume routes: PASS;not critical edition or all works')
            else:
                print(json.dumps(reading, ensure_ascii=False, indent=2))
            return
        reading = extract_opening(args.directory, registry)
        if args.check:
            check_review(plan, registry)
            if reading != plan['thoughtsOpeningReview']['byteVerifiedReading']:
                raise ValueError('Thoughts opening differs from pinned XML')
            print('38paragraphs/34notes/proposition12/continuation41: PASS;not whole discourse or cure')
        else:
            print(json.dumps(reading, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
