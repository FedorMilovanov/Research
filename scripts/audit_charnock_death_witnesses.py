#!/usr/bin/env python3
"""Read-only death-witness replay and calendar arithmetic,not resolution of an event.

Three historical pinned sources plus two separately registered small supplements.
Julian/Gregorian arithmetic does not certify a document's calendar or independence.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_biographical_anchors import text_and_pages

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT_IDS = {'A52960','A39134'}


def jdn(year, month, day, calendar):
    if calendar not in {'JULIAN','GREGORIAN'}:
        raise ValueError('Explicit JULIAN/GREGORIAN calendar required')
    if not 1 <= year <= 9999 or not 1 <= month <= 12:
        raise ValueError('Invalid calendar date')
    leap = year % 4 == 0 and (calendar == 'JULIAN' or year % 100 != 0 or year % 400 == 0)
    lengths = [31,29 if leap else 28,31,30,31,30,31,31,30,31,30,31]
    if not 1 <= day <= lengths[month-1]:
        raise ValueError('Invalid calendar date')
    a = (14-month)//12
    y = year+4800-a
    m = month+12*a-3
    base = day+(153*m+2)//5+365*y+y//4
    if calendar == 'JULIAN':
        return base-32083
    if calendar == 'GREGORIAN':
        return base-y//100+y//400-32045
    raise ValueError('Explicit JULIAN/GREGORIAN calendar required')


def calendar_review():
    rows = []
    weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for day in [27,28,30]:
        julian = jdn(1680,7,day,'JULIAN')
        gregorian = jdn(1680,7,day,'GREGORIAN')
        equivalent = datetime.date.fromordinal(julian-jdn(1,1,1,'GREGORIAN')+1)
        rows.append(dict(nominalDate=f'1680-07-{day}',julianWeekday=weekday[julian%7],
                         prolepticGregorianWeekday=weekday[gregorian%7],
                         equivalentGregorianDate=equivalent.isoformat(),calendarOffsetDays=julian-gregorian))
    return dict(kind='ARITHMETIC_NOT_EVENT_EVIDENCE',rows=rows,deathConflictResolved=False,
                boundary='Weekday compatibility is internal consistency,not a parish record or proof of which death date is true')


def pinned_tree(path, source):
    raw = path.read_bytes()
    if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
        raise ValueError('Witness byte pin mismatch: '+str(path))
    return raw,ET.fromstring(raw)


def check_supplements(sources, root=ROOT):
    if set(sources) != SUPPLEMENT_IDS:
        raise ValueError('Two separately identified poetic supplements required')
    for identifier,source in sources.items():
        path = (root/source['localPath']).resolve()
        if not path.is_relative_to((root/'data/charnock-primary-supplement').resolve()):
            raise ValueError('Unsafe supplemental source path')
        raw,tree = pinned_tree(path,source)
        notices = tree.findall('.//'+NS+'availability')
        if len(notices) != 1:
            raise ValueError('Explicit TCP text licence required')
        notice = plain(notices[0])
        targets = [n.get('target') for n in notices[0].iter(NS+'ref')]
        if (notice != source['licenceText'] or 'https://creativecommons.org/publicdomain/zero/1.0/' not in targets
                or 'This Phase I text is available for reuse, according to the terms of Creative Commons 0 1.0 Universal.' not in notice
                or 'even for commercial purposes, all without asking permission' not in notice
                or source['evidenceClass'] != 'A1' or source['accessState'] != 'FULL_OBJECT_VERIFIED'
                or source['locatorState'] != 'EXACT_LOCATOR_VERIFIED' or source['rightsState'] != 'PUBLICATION_ELIGIBLE'
                or source['publicationState'] != 'BLOCKED' or 'PUBLICATION_HOLD' not in source['holds']
                or source['rightsScope'] != 'CC0_TCP_TEXT_ONLY_NOT_IMAGES' or source['inHistoricalHandoff'] is not False):
            raise ValueError('Supplement licence/access does not approve images or historical custody')


def extract(directory, registry, supplements, root=ROOT):
    check_supplements(supplements,root)
    trees,raws = {},{}
    for identifier in ['A71277','B02133','A46911','A52960','A39134']:
        source = supplements[identifier] if identifier in supplements else registry['sources'][identifier]
        path = root/source['localPath'] if identifier in supplements else directory/(identifier+'.xml')
        raws[identifier],trees[identifier] = pinned_tree(path,source)
    wood = trees['A71277']
    matches = [p for p in wood.iter(NS+'p') if 'on the 27 of July in sixteen hundred and eighty' in plain(p)]
    if len(matches) != 1:
        raise ValueError('Unique Wood death paragraph required')
    full = plain(matches[0])
    boundary = 'I must now, having a just opportunity laid before me, tell the Reader'
    if full.count(boundary) != 1 or 'This Rosacrucian Charnock paid his last debt to nature' not in full:
        raise ValueError('Wood person-switch boundary must be preserved')
    main,continuation = full.split(boundary,1)
    whole,pages = text_and_pages(raws['A71277'])
    probe = 'on the 27 of July in sixteen hundred and eighty'
    at = whole.index(probe)
    result = {'A71277':dict(stephenContext=main.strip(),fullParagraphSha256=hashlib.sha256(full.encode()).hexdigest(),
                           probeTeiPages=list(dict.fromkeys(pages[at:at+len(probe)])),
                           personSwitchMarker=boundary,continuationStartsWith=continuation[:240],
                           continuationBelongsToStephen=False)}
    for identifier in ['B02133','A52960','A39134']:
        text = trees[identifier].find(NS+'text')
        heads = list(text.iter(NS+'head'))
        if not heads:
            raise ValueError('Explicit memorial heading required')
        result[identifier] = dict(heading=plain(heads[0]),headingIndexZeroBased=0,
                                  text=plain(text),textSha256=hashlib.sha256(plain(text).encode()).hexdigest(),
                                  boundary='TCP main text,not page images;distinct object is not proof of independent reporting')
    front = trees['A46911'].find('.//'+NS+'text/'+NS+'front')
    units = {}
    for kind in ['title_page','to_the_reader']:
        selected = front.findall(NS+'div[@type="'+kind+'"]')
        if len(selected) != 1:
            raise ValueError('Selected Johnson prefatory unit missing')
        units[kind] = plain(selected[0])
    result['A46911'] = dict(units=units,boundary='Selected title and letter,not proof of a specific death or funeral day')
    return result


def check_review(plan, registry, root=ROOT):
    review = plan['deathWitnessReview']
    check_supplements(review['supplementalSources'],root)
    if (review['reviewState'] != 'FIVE_PRINTED_OBJECTS_CONFLICT_RETAINED' or review['deathConflictResolved'] is not False
            or review['independenceEstablished'] is not False or review['parishRegisterAcquired'] is not False
            or review['calendarArithmetic'] != calendar_review() or review['baselineSourceRegistryChanged'] is not False
            or review['sourceLedgerRole'] != 'SUPPLEMENTARY_RESEARCH_SOURCE_RECORD_NOT_ROOT_AUTHORITY'):
        raise ValueError('Death witness review must retain event conflict,independence and parish-register limits')
    data = review['byteVerifiedContexts']
    if set(data) != {'A71277','B02133','A46911','A52960','A39134'}:
        raise ValueError('Five printed witness contexts required')
    wood = data['A71277']
    if (wood['continuationBelongsToStephen'] is not False or 'on the 27 of July' not in wood['stephenContext']
            or 'Agnes Norden' in wood['stephenContext'] or '21. Apr. 1581' in wood['stephenContext']):
        raise ValueError('Wood continuation about Thomas cannot become Stephen biography')
    for identifier in ['A52960','A39134']:
        source = review['supplementalSources'][identifier]
        _,tree = pinned_tree(root/source['localPath'],source)
        actual = plain(tree.find(NS+'text'))
        if data[identifier]['text'] != actual or data[identifier]['textSha256'] != hashlib.sha256(actual.encode()).hexdigest():
            raise ValueError('Supplemental main text must match persisted XML')
        if 'July 27.' not in data[identifier]['heading']:
            raise ValueError('Poetic date heading must remain literal')
    if 'Wednesday the 28 of July, 1680' not in data['B02133']['heading']:
        raise ValueError('Sayings Wednesday/28 date cannot be silently corrected')
    decisions = review['witnessDecisions']
    if len(decisions) != 5 or {d['source'] for d in decisions} != set(data):
        raise ValueError('Five explicit witness dispositions required')
    for d in decisions:
        source = review['supplementalSources'].get(d['source'],registry['sources'].get(d['source']))
        axes = ['evidenceClass','accessState','locatorState','rightsState','publicationState','holds']
        if source is None or any(d['sourceStateSnapshot'][key] != source[key] for key in axes):
            raise ValueError('Witness decision cannot promote source axes')
        if d['independence'] != 'NOT_ESTABLISHED' or not d['allowedUse'] or not d['prohibitedInference']:
            raise ValueError('Distinct memorial objects cannot vote as independent witnesses')
    return dict(deathWitnessObjects=5,newPoeticXmlSupplements=2,deathConflictResolved=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path,help='Existing pinned A71277/B02133/A46911 XMLs')
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    try:
        plan = json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        registry = json.loads((ROOT/plan['baselineRegistry']).read_text())
        review = plan['deathWitnessReview']
        result = extract(args.directory,registry,review['supplementalSources'])
        if args.check:
            check_review(plan,registry)
            if result != review['byteVerifiedContexts']:
                raise ValueError('Stored death witness contexts differ from source bytes')
            print('Five printed objects/two supplemental XML pins/calendar arithmetic: PASS;death conflict NOT resolved')
        else:
            print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,ET.ParseError) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__ == '__main__':
    main()
