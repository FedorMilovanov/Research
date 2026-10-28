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


LATIN_OCR_PINS = {'LAT1722': {'repository': 'jedipunkz/philosophy', 'path': 'inbox/デカルト/2026-10-14-René Descartes-Renati desCartes Principia philosophiae.md', 'commit': '95b16856e35f754ce67c22c6457232264a4fbbc2', 'blob': '17ab8f4fe6e8f8be29480cb5ac64de2c204eb68d', 'size': 302304, 'sha256': '3b3bfc5a790c58301942086cfaf76de7a9bb600e9f41fca477b64960b5ab039e', 'cacheName': 'principia-latin80.md', 'url': 'https://github.com/jedipunkz/philosophy/blob/95b16856e35f754ce67c22c6457232264a4fbbc2/inbox/%E3%83%87%E3%82%AB%E3%83%AB%E3%83%88/2026-10-14-Ren%C3%A9%20Descartes-Renati%20desCartes%20Principia%20philosophiae.md'}, 'LAT1672': {'repository': 'jedipunkz/philosophy', 'path': 'inbox/デカルト/2026-10-21-René Descartes-Renati DesCartes Opera philosophica Renati DesCartes Principia p.md', 'commit': '11d6066a17a8bc03eaf98be73c1dfe30d9489444', 'blob': '88d447743fce0e9b3f47bb815431f1f238918962', 'size': 302887, 'sha256': 'ab5ac74066bbde5fb3574fac4bdb64af641eb9f6d280267fab6938e86dda3588', 'cacheName': 'principia-opera80.md', 'url': 'https://github.com/jedipunkz/philosophy/blob/11d6066a17a8bc03eaf98be73c1dfe30d9489444/inbox/%E3%83%87%E3%82%AB%E3%83%AB%E3%83%88/2026-10-21-Ren%C3%A9%20Descartes-Renati%20DesCartes%20Opera%20philosophica%20Renati%20DesCartes%20Principia%20p.md'}}


def extract_latin_ocr(directory):
    result={}
    for key,pin in LATIN_OCR_PINS.items():
        raw=(directory/pin['cacheName']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if len(raw)!=pin['size'] or hashlib.sha256(raw).hexdigest()!=pin['sha256'] or blob!=pin['blob']:
            raise ValueError('Latin OCR byte/blob mismatch:'+key)
        text=raw.decode('utf-8')
        if 'book_text_truncated: true' not in text or 'public_domain: true' not in text:
            raise ValueError('Keep capture truncation and metadata-only rights statement visible')
        if key=='LAT1722':
            start=text.index('Haecque  optima  via')
            target=text.index('Cogitationis  nomine,',start)
            stop=text.index('\nX.  Non  hic',target)
            end=text.index('Jam  vero  ut',stop)
        else:
            start=text.index('Haecqucoptimaviacft')
            target=text.index('CoatacioDisiiomioe',start)
            stop=text.index('\nNon ii^c explico',target)
            end=text.index('Jamverouifciatur',stop)
        def window(a,b):
            value=text[a:b]
            return dict(startCharacterZeroBased=a,endCharacterExclusive=b,text=value,textSha256=digest(value))
        result[key]=dict(sourceSha256=pin['sha256'],sourceBytes=pin['size'],
                         captureMarkedTruncated=True,metadataClaimsPublicDomain=True,
                         contextVIIItoX=window(start,end),targetIX=window(target,stop))
    return result


def check_latin_ocr(review):
    r=review['latinTargetOcrFollowUp'];reading=r['byteVerifiedReading']
    if (r['reviewState']!='PRINCIPLES_I9_LATIN_OCR_TARGET_LOCATED_NOT_IMAGE_OR_FIRST_EDITION'
            or r['targetLatinOcrLocated'] is not True
            or any(r[k] is not False for k in ['firstEditionVerified','pageImagesAcquired',
                'normalisedLatinPrepared','directDependenceVerified','charnockOwnedEditionVerified',
                'wholeBooksAcquired','wholeBooksRead','independentReview','publicationApproval'])):
        raise ValueError('Latin target OCR is progress, not image/first-edition/dependence verification')
    if set(reading)!=set(LATIN_OCR_PINS):raise ValueError('Two bounded Latin OCR witnesses required')
    for key,pin in LATIN_OCR_PINS.items():
        row=reading[key]
        if (r['sources'][key]!=pin or row['sourceSha256']!=pin['sha256'] or row['sourceBytes']!=pin['size']
                or row['captureMarkedTruncated'] is not True or row['metadataClaimsPublicDomain'] is not True):
            raise ValueError('Do not promote a truncated OCR capture to a full original book')
        for name in ['contextVIIItoX','targetIX']:
            w=row[name]
            if digest(w['text'])!=w['textSha256'] or len(w['text'])!=w['endCharacterExclusive']-w['startCharacterZeroBased']:
                raise ValueError('Raw uncorrected Latin OCR text/character-range mismatch')
        outer=row['contextVIIItoX'];inner=row['targetIX'];offset=inner['startCharacterZeroBased']-outer['startCharacterZeroBased']
        if offset<0 or outer['text'][offset:offset+len(inner['text'])]!=inner['text']:
            raise ValueError('Target must be embedded in the actual VIII–X context')
    if ('inrclligo' not in reading['LAT1722']['targetIX']['text']
            or 'CoatacioDisiiomioe' not in reading['LAT1672']['targetIX']['text']):
        raise ValueError('Preserve OCR corruption, not a silently reconstructed Latin edition')
    if not r['scope'] or not r['rightsLimits'] or not r['historicalBaselineMeaning']:
        raise ValueError('Separate old acquisition baseline, new OCR target and rights')
    texts={key:row['targetIX']['text'] for key,row in reading.items()}
    texts['CH13']=review['byteVerifiedReading']['charnockParagraphs'][0]['text']
    if [o['id'] for o in r['observations']]!=[f'LO{i:02}' for i in range(1,6)]:
        raise ValueError('Five bounded OCR comparison observations required')
    for o in r['observations']:
        if not o['finding'] or not o['limit'] or not o['spans']:
            raise ValueError('Observation without an explicit OCR limit')
        for span in o['spans']:
            if not span['text'] or span['text'] not in texts[span['source']] or digest(span['text'])!=span['sha256']:
                raise ValueError('Observation must cite actual uncorrected OCR/Charnock spans')
    return dict(cartesianLatinTargetOcrWitnesses=2,cartesianLatinTargetOcrLocated=True,cartesianLatinPageImagesVerified=False)


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
                descartesLatinOriginalVerified=False, directCartesianDependenceVerified=False, **check_latin_ocr(review))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path,help='Pinned 4391.txt and A52424.xml')
    parser.add_argument('--charnock-directory',type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--latin-ocr-directory',type=Path,help='Optional replay of new bounded Latin OCR captures')
    args=parser.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        registry=json.loads((ROOT/plan['baselineRegistry']).read_text())
        reading=extract(args.directory,args.charnock_directory,registry)
        if args.check:
            check_review(plan,registry)
            if reading != plan[KEY]['byteVerifiedReading']:
                raise ValueError('Comparison differs from pinned source bytes')
            if args.latin_ocr_directory and extract_latin_ocr(args.latin_ocr_directory)!=plan[KEY]['latinTargetOcrFollowUp']['byteVerifiedReading']:
                raise ValueError('Latin target OCR differs from pinned raw captures')
            print('Principles VIII–X/Charnock/NorrisVI:PASS;Latin OCR follow-up checked if supplied;not original-edition verification')
        else:
            print(json.dumps(reading,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,TypeError,StopIteration) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__=='__main__':
    main()
