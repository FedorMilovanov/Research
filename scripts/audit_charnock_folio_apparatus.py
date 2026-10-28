#!/usr/bin/env python3
"""Read-only apparatus scopes: metadata, editorial front matter, fourteen discourses."""
import argparse
import hashlib
import json
from pathlib import Path

from audit_charnock_book_route import NS, plain, extract as book_extract
from audit_charnock_pastoral_contexts import ROOT, source_structure
from audit_charnock_thoughts import digest, HOLDS

KEY = 'folioApparatusReview'
EXPECTED_NOTES = ['Mr. J. Wichens. Mr. Ashton.', 'Acts 17.23.', '2 Cor. 3.10.',
                  'Treatise of Providence and of Thoughts.', 'Psal. 146.2', 'Psal. 109.1.']
PARENTS = [3, 3, 3, 4, 6, 7]
FALSE_FLAGS = ['printedImagesVerified', 'allNotesAreForeignSources', 'wholeBookNewlyRead',
               'copyistsFullNamesVerified', 'copyistsAreEditors', 'independentWitnessVerified',
               'publicationApproval']


def anchor_before(paragraph, target):
    chunks = []
    found = False
    def visit(node):
        nonlocal found
        if node is target:
            found = True
            return
        chunks.append(node.text or '')
        for child in node:
            if found:
                return
            if child is target:
                found = True
                return
            if child.tag not in {NS+'note', NS+'fw'}:
                visit(child)
            if found:
                return
            chunks.append(child.tail or '')
    visit(paragraph)
    if not found:
        raise ValueError('Marginal note not inside its claimed paragraph')
    return ' '.join(''.join(chunks).replace('ſ', 's').split())[-160:]


def extract(directory, registry):
    raw, root, parents, pages, paragraphs = source_structure(directory, registry, 'A32723')
    route = book_extract(directory/'A32723.xml', registry)['route']
    text = root.find(NS+'text')
    header = root.find(NS+'teiHeader')
    all_notes = list(root.iter(NS+'note'))
    margins = [n for n in text.iter(NS+'note') if n.get('place') == 'margin']
    front_rows = []
    for note in margins:
        ancestors = []
        current = note
        while current in parents:
            current = parents[current]
            ancestors.append(current)
        if any(a.tag == NS+'div' and a.get('type') == 'discourse' for a in ancestors):
            continue
        paragraph = next(a for a in ancestors if a.tag == NS+'p')
        division = next(a for a in ancestors if a.tag == NS+'div')
        value = ' '.join(''.join(note.itertext()).replace('ſ', 's').split())
        front_rows.append(dict(noteText=value, noteTextSha256=digest(value),
                               paragraphIndexZeroBased=paragraphs.index(paragraph),
                               paragraphSha256=digest(plain(paragraph)),
                               precedingBodyText=anchor_before(paragraph,note),
                               divisionType=division.get('type'),
                               divisionHeading=plain(division.find(NS+'head')),
                               teiPage=pages[note]))
    return dict(source='A32723', sourceSha256=hashlib.sha256(raw).hexdigest(),
                sourceBytes=len(raw), allXmlNoteElements=len(all_notes),
                metadataNoteElements=len(list(header.iter(NS+'note'))),
                textNoteElements=len(list(text.iter(NS+'note'))),
                textMarginalNotes=len(margins), discourseNoteElements=sum(r['noteElements'] for r in route),
                discourseCount=len(route), editorialFrontMarginalNotes=front_rows,
                discourseCounts=[dict(ordinal=r['ordinal'],noteElements=r['noteElements']) for r in route])


def check_review(plan, registry):
    review = plan[KEY]
    data = review['byteVerifiedReading']
    if review['reviewState'] != 'XML_NOTE_SCOPES_RECONCILED_EDITORIAL_COPYIST_NOTE_LOCATED':
        raise ValueError('Apparatus-scope reconciliation only')
    if any(review[k] is not False for k in FALSE_FLAGS):
        raise ValueError('Scope count is not reading, identity resolution, image proof or publication')
    source = registry['sources']['A32723']
    if data['source'] != 'A32723' or data['sourceSha256'] != source['sha256'] or data['sourceBytes'] != source['size']:
        raise ValueError('Apparatus must bind immutable A32723 source bytes')
    if (data['allXmlNoteElements'],data['metadataNoteElements'],data['textNoteElements'],
            data['textMarginalNotes'],data['discourseNoteElements'],data['discourseCount']) != (2348,5,2343,2343,2337,14):
        raise ValueError('Distinguish 2348 XML notes, 5 metadata, 2343 text margins, 2337 discourse margins')
    rows = data['editorialFrontMarginalNotes']
    if ([r['noteText'] for r in rows] != EXPECTED_NOTES
            or [r['paragraphIndexZeroBased'] for r in rows] != PARENTS
            or any(r['divisionType'] != 'to_the_reader' or r['divisionHeading'] != 'TO THE READER.'
                   or r['teiPage'] is not None or not r['precedingBodyText']
                   or digest(r['noteText']) != r['noteTextSha256'] for r in rows)):
        raise ValueError('Six unnumbered editorial notes, not six missing discourse references')
    route = plan['principalBookReading']['byteVerifiedExtraction']['route']
    if data['discourseCounts'] != [dict(ordinal=r['ordinal'],noteElements=r['noteElements']) for r in route]:
        raise ValueError('Retain existing fourteen-discourse route counts')
    # Reuse the previously verified five preface paragraphs, not a new paraphrase.
    original = plan['editorialVoiceReview']['byteVerifiedExtraction']
    def dictionaries(value):
        if isinstance(value,dict):
            yield value
            for v in value.values():
                yield from dictionaries(v)
        elif isinstance(value,list):
            for v in value:
                yield from dictionaries(v)
    hashes = {v.get('textSha256') for v in dictionaries(original) if 'textSha256' in v}
    if any(r['paragraphSha256'] not in hashes for r in rows):
        raise ValueError('Editorial note parents must match preserved full preface contexts')
    if not rows[0]['precedingBodyText'].endswith('those worthy Persons that undertook it,'):
        raise ValueError('Copyist names must remain attached to the transcription clause')
    if (review['evidenceClass'] != 'C' or review['accessState'] != 'FULL_OBJECT_VERIFIED'
            or review['locatorState'] != 'EXACT_LOCATOR_VERIFIED' or review['rightsState'] != 'RIGHTS_UNKNOWN'
            or review['publicationState'] != 'BLOCKED' or set(review['holds']) != HOLDS
            or plan['principalBookReading']['apparatusScopeReview'] != KEY
            or KEY not in plan['documents'][5]['supplementaryContextReadings']):
        raise ValueError('Keep scope, evidence axes, HOLD and printed-transmission integration')
    return dict(folioTextMarginalNotes=2343, folioDiscourseMarginalNotes=2337,
                folioEditorialMarginalNotes=6, folioMetadataNotesExcluded=5,
                folioCopyistPrintedNamesLocated=True, folioCopyistFullNamesVerified=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text())
        registry=json.loads((ROOT/plan['baselineRegistry']).read_text())
        reading=extract(args.directory,registry)
        if args.check:
            check_review(plan,registry)
            if reading != plan[KEY]['byteVerifiedReading']:
                raise ValueError('Apparatus reconciliation differs from pinned XML')
            print('2348XML=5metadata+2343margins;2343=2337discourse+6editorial: PASS;not images or full-name identification')
        else:
            print(json.dumps(reading,ensure_ascii=False,indent=2))
    except (OSError,KeyError,ValueError,TypeError,StopIteration) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__=='__main__':
    main()
