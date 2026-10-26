#!/usr/bin/env python3
"""Read-only translated counterpart/late Latin quotation audit; not Descartes-original proof."""
import argparse
import hashlib
import json
from pathlib import Path

from audit_charnock_book_route import NS, plain
from audit_charnock_pastoral_contexts import ROOT, source_structure
from audit_charnock_thoughts import digest, HOLDS

KEY = 'cartesianDefinitionComparison'
PINS = {
    'PG4391': dict(repository='GITenberg/Selections-from-the-Principles-of-Philosophy_4391',
                   commit='fe5d92458506b5cb4db135aced80046deeaf8ca2', path='4391.txt',
                   blob='3d81fb5c145695cd2b522896a4d220f8cd23c934', size=195080,
                   sha256='be132739f8ca66897dbe1c19a5d6e5db1c15ae1fd447b84613b43ab541150475'),
    'A52424': dict(repository='textcreationpartnership/A52424',
                   commit='7859df5a4fdc4a339e62c7fcb8d5d066dc17551b', path='A52424.xml',
                   blob='1e2195feb67e592a64345e21d0e111d6b6dab02a', size=352981,
                   sha256='3680ed708035808b41fd88a7da7367369a2d1c54cd0de4dd118f0c5657226066'),
}
FALSE_FLAGS = ('descartesLatinOriginalAcquired', 'descartesOriginalEditionVerified',
               'directCartesianDependenceVerified', 'charnockOwnedEditionVerified',
               'norrisWasCharnockSource', 'wholeNorrisBookRead', 'clinicalApproval',
               'publicationApproval', 'driveWritesPerformed', 'historicalReceiptReverified')


def verified_bytes(directory, source):
    pin = PINS[source]
    raw = (directory / pin['path']).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if len(raw) != pin['size'] or hashlib.sha256(raw).hexdigest() != pin['sha256'] or blob != pin['blob']:
        raise ValueError(source + ': byte or Git blob pin mismatch')
    return raw


def row(index, paragraph, pages):
    text = plain(paragraph)
    return dict(paragraphIndexZeroBased=index, startTeiPage=pages[paragraph], text=text,
                textSha256=digest(text), internalTeiPages=[p.get('n') for p in paragraph.iter(NS+'pb')])


def extract(directory, charnock_directory, registry):
    text = verified_bytes(directory, 'PG4391').decode('utf-8').replace('\r\n', '\n')
    # Structural headings, not any occurrence of cogitatio in metadata or another work.
    start = text.index('VIII. That we hence discover')
    end = text.index('XI.', start)
    window = text[start:end].strip()
    if window.count('IX. What thought (COGITATIO) is.') != 1:
        raise ValueError('A genuine Principles I.IX section is required')
    verified_bytes(directory, 'A52424')
    _, root, _, pages, paragraphs = source_structure(directory, {'sources':{'A52424':PINS['A52424']}}, 'A52424')
    letter = next(d for d in root.iter(NS+'div') if d.get('type')=='letter' and d.get('n')=='6')
    nodes = letter.findall(NS+'p')
    norris = dict(heading=plain(letter.find(NS+'head')),
                  signed=[plain(n) for n in letter.iter(NS+'signed')],
                  dateline=[plain(n) for n in letter.iter(NS+'dateline')],
                  paragraphs=[row(paragraphs.index(p),p,pages) for p in nodes],
                  textLicenseVerified='Creative Commons 0 1.0 Universal' in ' '.join(' '.join(root.find(NS+'teiHeader').itertext()).split()))
    _, _, _, pages, paragraphs = source_structure(charnock_directory, registry, 'A32724')
    return dict(veitchSectionsVIIItoX=dict(text=window, textSha256=digest(window)),
                norrisLetterVI=norris,
                charnockParagraphs=[row(i,paragraphs[i],pages) for i in [13,14,16,18]],
                charnockMarginalNote=[' '.join(''.join(n.itertext()).replace('ſ', 's').split()) for n in paragraphs[13].iter(NS+'note')])


def check_review(plan, registry):
    review = plan[KEY]
    if (review['reviewState'] != 'TRANSLATED_COUNTERPART_AND_POSTHUMOUS_LATIN_WITNESS_NOT_ORIGINAL'
            or any(review[k] is not False for k in FALSE_FLAGS)
            or review['wholeNorrisLetterVIRead'] is not True
            or review['translatedPrinciplesI9Compared'] is not True):
        raise ValueError('A translated counterpart and later witness cannot certify an original or dependence')
    if (review['evidenceClass'] != 'C' or review['accessState'] != 'FULL_OBJECT_VERIFIED'
            or review['locatorState'] != 'EXACT_LOCATOR_VERIFIED' or review['rightsState'] != 'RIGHTS_UNKNOWN'
            or review['publicationState'] != 'BLOCKED' or set(review['holds']) != HOLDS):
        raise ValueError('Comparison remains contextual, bounded and blocked')
    for key, pin in PINS.items():
        source = review['sources'][key]
        if (any(source[k] != v for k,v in pin.items()) or not source['rightsNote']
                or source['evidenceClass'] != 'C' or source['accessState'] != 'FULL_OBJECT_VERIFIED'
                or source['locatorState'] != 'EXACT_LOCATOR_VERIFIED' or source['publicationState'] != 'BLOCKED'
                or source['rightsState'] != ('STORAGE_ONLY' if key=='A52424' else 'RIGHTS_UNKNOWN')
                or set(source['holds']) != (HOLDS-{'RIGHTS_HOLD'} if key=='A52424' else HOLDS)):
            raise ValueError('Separate immutable object pins, contextual class and rights scope required')
    data = review['byteVerifiedReading']
    charnock = data['charnockParagraphs']
    opening = {r['paragraphIndexZeroBased']:r for r in plan['thoughtsOpeningReview']['byteVerifiedReading']['contextWindow']}
    if ([r['paragraphIndexZeroBased'] for r in charnock] != [13,14,16,18]
            or any(r['text'] != opening[r['paragraphIndexZeroBased']]['text'] for r in charnock)
            or data['charnockMarginalNote'] != ['Cartes. Princip. P • ilos. Part 1. Sect. 9.']
            or registry['sources']['A32724']['sha256'] != plan['thoughtsOpeningReview']['byteVerifiedReading']['sourceSha256']):
        raise ValueError('Keep Charnock definition, note and morally mixed paragraphs intact')
    norris = data['norrisLetterVI']
    if (norris['heading'] != "LETTER VI. Mr. Norris's Answer."
            or norris['signed'] != ['Your most humble Servant J. NORRIS.']
            or norris['dateline'] != ['Bemerton, Jan. 11. 1693.'] or norris['textLicenseVerified'] is not True
            or [r['paragraphIndexZeroBased'] for r in norris['paragraphs']] != list(range(86,93))
            or norris['paragraphs'][4]['startTeiPage'] != '117'
            or norris['paragraphs'][4]['internalTeiPages'] != ['118','119']):
        raise ValueError('Norris attribution, printed date and full seven-paragraph letter scope required')
    text_rows = charnock + norris['paragraphs'] + [data['veitchSectionsVIIItoX']]
    if any(digest(r['text']) != r['textSha256'] for r in text_rows):
        raise ValueError('Reading text hash mismatch')
    texts = {'CH13':charnock[0]['text'], 'CH14':charnock[1]['text'],
             'CH16':charnock[2]['text'], 'CH18':charnock[3]['text'],
             'VEITCH':data['veitchSectionsVIIItoX']['text'],
             'N86':norris['paragraphs'][0]['text'], 'N90':norris['paragraphs'][4]['text']}
    observations = review['observations']
    if [o['id'] for o in observations] != [f'CD{i:02}' for i in range(1,13)]:
        raise ValueError('Twelve distinct comparative decisions required')
    for o in observations:
        if (not o['finding'] or not o['prohibitedInference'] or not o['spans']
                or any(not s['text'] or s['text'] not in texts[s['source']] or digest(s['text']) != s['sha256'] for s in o['spans'])):
            raise ValueError('Comparison needs exact source spans and explicit limits')
    for candidate in review['rejectedLatinCandidates']:
        if (candidate['decision'] != 'REJECTED_AS_TARGET_ORIGINAL_NOT_GLOBAL_ABSENCE'
                or candidate['evidenceClass'] != 'D' or candidate['accessState'] != 'PARTIAL_OBJECT'
                or candidate['locatorState'] != 'COARSE_LOCATOR_ONLY'
                or candidate['rightsState'] != 'RIGHTS_UNKNOWN' or candidate['publicationState'] != 'BLOCKED'
                or set(candidate['holds']) != HOLDS | {'LOCATOR_HOLD'}
                or not candidate['path'] or not candidate['url'] or not candidate['reason']):
            raise ValueError('Wrong-work candidates remain excluded, partial and rights-unverified')
    discovery = review['additionalDiscovery']
    if discovery['resultsExhausted'] is not False or discovery['globalAbsenceClaimed'] is not False:
        raise ValueError('A bounded code search cannot establish global absence')
    if (review['historicalSearchSha256'] != digest(json.dumps(plan['thoughtsOpeningReview']['cartesianCounterpartSearch'],ensure_ascii=False,sort_keys=True))
            or KEY not in plan['documents'][7]['supplementaryContextReadings']
            or len(review['rejectedLatinCandidates']) != 2):
        raise ValueError('Preserve earlier discovery state and integrate the new comparison separately')
    return dict(cartesianTranslatedDefinitionCompared=True, cartesianLaterLatinWitnessCompared=True,
                cartesianComparativeObservations=12, norrisLetterVIParagraphs=7,
                descartesLatinOriginalVerified=False, directCartesianDependenceVerified=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path,help='Pinned 4391.txt and A52424.xml')
    parser.add_argument('--charnock-directory',type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        registry=json.loads((ROOT/plan['baselineRegistry']).read_text())
        reading=extract(args.directory,args.charnock_directory,registry)
        if args.check:
            check_review(plan,registry)
            if reading != plan[KEY]['byteVerifiedReading']:
                raise ValueError('Comparison differs from pinned source bytes')
            print('Principles VIII–X/Charnock13+14+16+18/NorrisVI7paragraphs: PASS;not Latin original')
        else:
            print(json.dumps(reading,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,TypeError,StopIteration) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__=='__main__':
    main()
