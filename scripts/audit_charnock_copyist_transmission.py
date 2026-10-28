#!/usr/bin/env python3
"""Compare two editorial accounts of transcription; not autograph or identity certification."""
import argparse
import json
from pathlib import Path
from audit_charnock_book_route import NS, plain
from audit_charnock_pastoral_contexts import ROOT, source_structure
from audit_charnock_folio_apparatus import extract as extract_apparatus
from audit_charnock_thoughts import digest, HOLDS

KEY='copyistTransmissionReview'
FALSE_FLAGS=('autographsAcquired','fullNamesVerified','independentIdentityProof',
             'allPrintedWordsCollated','lostSermonsRecoveredAsTheseTwoTreatises',
             'twinsAreTheTwoPublishedTreatises','literalFireRecoveryVerified',
             'preachingDateEstablished','publicationApproval')


def extract(directory,registry):
    apparatus=extract_apparatus(directory,registry)
    _,root,_,pages,paragraphs=source_structure(directory,registry,'B20167')
    front=root.find(NS+'text/'+NS+'front')
    div=front.find(NS+'div[@type="to_the_reader"]')
    title=front.find(NS+'div[@type="title_page"]')
    return dict(firstVolume=dict(source='A32723',sourceSha256=registry['sources']['A32723']['sha256'],
                                 copyistMargin=apparatus['editorialFrontMarginalNotes'][0]),
                laterVolume=dict(source='B20167',sourceSha256=registry['sources']['B20167']['sha256'],
                                 sourceBytes=registry['sources']['B20167']['size'],
                                 titlePage=plain(title),editorialHeading=plain(div.find(NS+'head')),
                                 signatures=[plain(n) for n in div.iter(NS+'signed')],
                                 datelines=[plain(n) for n in div.iter(NS+'dateline')],
                                 paragraphs=[dict(paragraphIndexZeroBased=paragraphs.index(p),startTeiPage=pages[p],
                                                  text=plain(p),textSha256=digest(plain(p))) for p in div.findall(NS+'p')]))


def check_review(plan,registry):
    review=plan[KEY];reading=review['byteVerifiedReading'];first=reading['firstVolume'];later=reading['laterVolume']
    if (review['reviewState']!='TWO_EDITORIAL_ACCOUNTS_EXPLICIT_ASHTON_BACKREFERENCE'
            or review['explicitFirstVolumeBackreferenceLocated'] is not True
            or any(review[f] is not False for f in FALSE_FLAGS)):
        raise ValueError('Explicit editorial continuity is not independent identity or manuscript proof')
    if (first['source']!='A32723' or first['sourceSha256']!=registry['sources']['A32723']['sha256']
            or first['copyistMargin']!=plan['folioApparatusReview']['byteVerifiedReading']['editorialFrontMarginalNotes'][0]):
        raise ValueError('Retain first-volume printed initials and actual note placement')
    baseline=plan['enmityReview']['byteVerifiedReading']
    if (later['source']!='B20167' or later['sourceSha256']!=registry['sources']['B20167']['sha256']
            or later['sourceBytes']!=registry['sources']['B20167']['size']
            or later['editorialHeading']!=baseline['editorialHeading'] or later['signatures']!=baseline['signatures']
            or later['datelines']!=['Septemb. 20. 1699.'] or later['paragraphs']!=baseline['editorialParagraphs']):
        raise ValueError('Keep full four-paragraph editorial context, signature and printed date')
    if 'Printed for Tho. Cockerill' not in later['titlePage'] or 'Publish\'d from his Original Manuscripts by Mr. Edward Veel.' not in later['titlePage']:
        raise ValueError('Title-page editorial credit and Printed for are not a named printer')
    texts={str(p['paragraphIndexZeroBased']):p['text'] for p in later['paragraphs']}
    observations=review['observations']
    if [o['id'] for o in observations]!=[f'CT{i:02}' for i in range(1,10)]:
        raise ValueError('Nine bounded transmission decisions required')
    for observation in observations:
        if (not observation['finding'] or not observation['prohibitedInference'] or not observation['spans']
                or any(not s['text'] or s['text'] not in texts[s['paragraph']] or digest(s['text'])!=s['sha256'] for s in observation['spans'])):
            raise ValueError('Transmission decisions require exact spans and a prohibited inference')
    if (review['evidenceClass']!='C' or review['accessState']!='FULL_OBJECT_VERIFIED'
            or review['locatorState']!='EXACT_LOCATOR_VERIFIED' or review['rightsState']!='RIGHTS_UNKNOWN'
            or review['publicationState']!='BLOCKED' or set(review['holds'])!=HOLDS
            or KEY not in plan['documents'][5]['supplementaryContextReadings']):
        raise ValueError('Preserve evidence states, HOLD and printed-transmission ownership')
    return dict(copyistEditorialAccountsCompared=2,copyistTransmissionObservations=9,
                ashtonFirstVolumeBackreferenceLocated=True,copyistAutographsVerified=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text());registry=json.loads((ROOT/plan['baselineRegistry']).read_text())
        reading=extract(args.directory,registry)
        if args.check:
            check_review(plan,registry)
            if reading!=plan[KEY]['byteVerifiedReading']:raise ValueError('Two-volume reading differs from pinned XML')
            print('1682copyist note/1699explicit backreference+4paragraphs/title/signature/date: PASS;not autographs or full-name proof')
        else:print(json.dumps(reading,ensure_ascii=False,indent=2))
    except (OSError,KeyError,ValueError,TypeError) as exc:parser.exit(1,str(exc)+'\n')


if __name__=='__main__':main()
