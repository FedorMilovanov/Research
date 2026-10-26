#!/usr/bin/env python3
"""Recheck the Charnock side of three source-use cases,not their foreign counterparts.

No network/writes. Counterpart OCR excerpts remain inherited dossier evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import plain, NS
from audit_charnock_biographical_anchors import text_and_pages, normalize

ROOT = Path(__file__).resolve().parents[1]
PROBES = {'CASE-LINGENDES': 'But since he could not be united to any but to an intellectual Creature',
          'CASE-RAYNAUD': 'which flows from the excellency and fulness of his Essence',
          'CASE-DAILLE': 'Election is the cause of Faith, and not Faith the cause of Election'}


def extract(path, registry):
    raw = path.read_bytes()
    source = registry['sources']['A32723']
    if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
        raise ValueError('A32723 source byte pin mismatch')
    root = ET.fromstring(raw)
    parents = {c: n for n in root.iter() for c in n}
    page, pages = None, {}
    for n in root.iter():
        if n.tag == NS + 'pb':
            page = n.get('n')
        pages[n] = page
    alltext, labels = text_and_pages(raw)
    result = {}
    for identifier, probe in PROBES.items():
        candidates = [p for p in root.iter(NS + 'p') if probe.lower() in plain(p).lower()]
        if not candidates:
            raise ValueError('Source-use probe not found')
        paragraph = min(candidates, key=lambda p: len(plain(p)))
        text = plain(paragraph)
        needle = normalize(probe)
        if alltext.count(needle) != 1:
            raise ValueError('Source-use probe not unique')
        index = alltext.index(needle)
        locus = list(dict.fromkeys(labels[index:index + len(needle)]))
        ancestor = paragraph
        while ancestor in parents and not (ancestor.tag == NS + 'div' and ancestor.get('type') == 'discourse'):
            ancestor = parents[ancestor]
        head = ancestor.find(NS + 'head')
        notes = [{'teiPage': pages[n], 'text': ' '.join(''.join(n.itertext()).replace('ſ', 's').split())}
                 for n in paragraph.iter(NS + 'note')]
        result[identifier] = dict(source='A32723', sourceSha256=source['sha256'], sourceBytes=source['size'],
                                  discourseHeading=plain(head), paragraphStartTeiPage=pages[paragraph],
                                  probe=probe, probeTeiPages=locus,
                                  paragraphNumberedBreaks=[n.get('n') for n in paragraph.iter(NS + 'pb') if n.get('n')],
                                  bodyParagraph=text, bodyParagraphSha256=hashlib.sha256(text.encode()).hexdigest(),
                                  marginalNotes=notes, normalization='Whitespace/long-s;note/fw bodies omitted,tails retained')
    return result


def body_text_and_pages(raw):
    """Derived locator view:omit marginal note/fw bodies,retain their tails."""
    root = ET.fromstring(raw)
    text = root.find('.//' + NS + 'text')
    if text is None:
        raise ValueError('Missing TEI text')
    chars, labels, page = [], [], None
    def emit(value):
        if value:
            value = value.replace('ſ', 's')
            chars.extend(value)
            labels.extend([page] * len(value))
    def visit(node):
        nonlocal page
        if node.tag == NS + 'pb':
            page = node.get('n')
        emit(node.text)
        for child in node:
            if child.tag not in {NS + 'note', NS + 'fw'}:
                visit(child)
            emit(child.tail)
    visit(text)
    out, pages, pending = [], [], False
    for ch, label in zip(chars, labels):
        if ch.isspace():
            pending = bool(out)
        else:
            if pending:
                out.append(' ')
                pages.append(label)
                pending = False
            out.append(ch)
            pages.append(label)
    return ''.join(out), pages


def check_critical_review(case, dossier_text):
    """Validate bounded micro-readings,not correctness of inherited foreign OCR."""
    review = case['criticalReview']
    excerpt = review['dossierExcerpt']
    if (review['reviewState'] != 'TWELVE_MICRO_READINGS_FIVE_INHERITED_GLOSSES'
            or review['counterpartRawReacquired'] is not False or not excerpt or excerpt not in dossier_text
            or hashlib.sha256(excerpt.encode()).hexdigest() != review['dossierExcerptSha256']):
        raise ValueError('Critical pair review must retain inherited dossier,not claim fresh counterpart acquisition')
    prefix = {'CASE-LINGENDES': 'L', 'CASE-RAYNAUD': 'R', 'CASE-DAILLE': 'D'}[case['id']]
    rows = review['microReadings']
    body = case['charnockSide']['byteVerifiedContext']['bodyParagraph']
    if len(rows) != 4 or {r['id'] for r in rows} != {prefix + str(i) for i in range(1,5)}:
        raise ValueError('Four distinct micro-readings required per pair')
    for row in rows:
        role = 'REJECTED_CONSEQUENCE' if row['id'] == 'D2' else 'RHETORICAL_SEEMING' if row['id'] == 'L3' else 'AUTHORIAL_ASSERTION'
        if (not row['charnockSpan'] or body.count(row['charnockSpan']) != 1
                or hashlib.sha256(row['charnockSpan'].encode()).hexdigest() != row['charnockSpanSha256']
                or not row['spanTeiPages'] or any(page not in {case['charnockSide']['byteVerifiedContext']['paragraphStartTeiPage'], *case['charnockSide']['byteVerifiedContext']['paragraphNumberedBreaks']} for page in row['spanTeiPages'])
                or row['positionRole'] != role or row['counterpartBasis'] != 'INHERITED_DOSSIER_ONLY'
                or not row['observation'] or not row['alternativeOrLimit']):
            raise ValueError('Micro-reading must preserve literal English span,role and comparison boundary')
        if row['id'] == 'D2' and not row['charnockSpan'].startswith('If men be chosen by God upon the foresight of Faith'):
            raise ValueError('Rejected consequence must retain its conditional antecedent')
        if row['id'] == 'L3' and 'seem' not in row['charnockSpan']:
            raise ValueError('Rhetorical seeming cannot become an ontological assertion')
    glosses = review['workingGlosses']
    expected = {'L': {'G-L1','G-L2'}, 'R': {'G-R1'}, 'D': {'G-D1','G-D2'}}[prefix]
    if len(glosses) != len(expected) or {g['id'] for g in glosses} != expected:
        raise ValueError('Five total inherited foreign glosses required')
    for g in glosses:
        if (not g['foreignSpan'] or g['foreignSpan'] not in ' '.join(excerpt.split())
                or hashlib.sha256(g['foreignSpan'].encode()).hexdigest() != g['foreignSpanSha256']
                or not g['russianDraft'] or hashlib.sha256(g['russianDraft'].encode()).hexdigest() != g['russianDraftSha256']
                or g['microReading'] not in {r['id'] for r in rows}
                or g['basis'] != 'INHERITED_NORMALIZED_OCR_EXCERPT_NOT_RAW_SOURCE'
                or g['translationState'] != 'AI_WORKING_GLOSS_NOT_INDEPENDENTLY_REVIEWED'
                or g['independentReview'] is not False or len(g['notes']) < 2):
            raise ValueError('Foreign gloss must remain inherited,working and independently unreviewed')
        if g['id'] == 'G-D2' and g['microReading'] != 'D2':
            raise ValueError('Conditional French gloss must link rejected-consequence context')
    return len(rows), len(glosses)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        registry = json.loads((ROOT / 'data/charnock-biographical-anchors-v1.json').read_text())
        result = extract(args.xml, registry)
        if args.check:
            plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
            saved = {c['id']: c['charnockSide']['byteVerifiedContext'] for c in plan['sourceUseCases']}
            if result != saved:
                raise ValueError('Stored Charnock contexts differ from actual pinned XML')
            body, labels = body_text_and_pages(args.xml.read_bytes())
            for case in plan['sourceUseCases']:
                for row in case['criticalReview']['microReadings']:
                    span = normalize(row['charnockSpan'])
                    if body.count(span) != 1:
                        raise ValueError('Micro-reading span must be unique in note-free body view')
                    at = body.index(span)
                    if list(dict.fromkeys(labels[at:at + len(span)])) != row['spanTeiPages']:
                        raise ValueError('Micro-reading page span differs from source bytes')
            print('Three Charnock contexts/notes plus12micro-span locators: PASS. Counterpart OCR NOT independently replayed.')
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


def check_acquisition_boundary(plan):
    """Search-record consistency only;never verifies remote absence or foreign bytes."""
    review = plan['counterpartAcquisitionReview']
    if (review['reviewState'] != 'BOUNDED_DRIVE_SEARCH_NO_TARGET_ACQUISITION'
            or any(review[k] is not False for k in ('independentCounterpartRawLocated',
                'downloadPerformed', 'driveWritesPerformed', 'allDriveAbsenceProven'))
            or not review['searchBoundary']):
        raise ValueError('Search must not certify foreign acquisition or global absence')
    for record in [review] + [c['acquisitionBoundaryReview'] for c in plan['sourceUseCases']]:
        if (record['evidenceClass'] != 'C' or record['accessState'] != 'PARTIAL_OBJECT'
                or record['locatorState'] != 'COARSE_LOCATOR_ONLY'
                or record['rightsState'] != 'RIGHTS_UNKNOWN' or record['publicationState'] != 'BLOCKED'
                or set(record['holds']) != {'EVIDENCE_HOLD','ARCHIVE_HOLD','LOCATOR_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Acquisition boundary axes must remain partial and held')
    folder = review['folderMetadata']
    queries = review['completedQueries']
    if (folder['mimeType'] != 'application/vnd.google-apps.folder' or folder['trashed'] is not False
            or len(queries) != 3 or folder['id'] not in queries[0]['query']
            or queries[0]['returnedFiles']
            or any(q['nextPageToken'] is not None or q['incompleteSearch'] is not False for q in queries)
            or [len(q['returnedFiles']) for q in queries] != [0, 2, 1]
            or any(f['classification'] != 'NON_TARGET_TITLE_ONLY_NOT_DOWNLOADED' for f in queries[1]['returnedFiles'])
            or queries[2]['returnedFiles'][0]['classification'] != 'DERIVED_DOSSIER_NOT_COUNTERPART_RAW'):
        raise ValueError('Bounded metadata query provenance changed')
    partial = review['partialQuery']
    if (partial['responseTruncated'] is not True or partial['hasNextPage'] is not True
            or partial['usedForExhaustiveConclusion'] is not False):
        raise ValueError('Truncated paginated search cannot become an exhaustive inventory')
    cases = plan['sourceUseCases']
    if {c['id'] for c in cases} != set(PROBES) or len(cases) != 3:
        raise ValueError('Three source-side boundaries required')
    for case in cases:
        boundary = case['acquisitionBoundaryReview']
        if (boundary['decision'] != 'SOURCE_SIDE_ONLY_PENDING_COUNTERPART'
                or boundary['sourceContextSha256'] != case['charnockSide']['byteVerifiedContext']['bodyParagraphSha256']
                or set(boundary['excludedUntilAcquired']) != {'VERIFIED_FOREIGN_WORDING',
                    'DIRECT_BORROWING_PROVEN','OWNED_EDITION_IDENTIFIED','COUNTERPART_QUOTE_SAFE'}
                or not boundary['usableResearchQuestion'] or not boundary['counterpartGate']
                or boundary['historicalComparisonPreserved'] is not True
                or boundary['publicationState'] != 'BLOCKED' or boundary['evidenceClass'] != 'C'
                or set(boundary['holds']) != {'EVIDENCE_HOLD','ARCHIVE_HOLD','LOCATOR_HOLD','RIGHTS_HOLD','PUBLICATION_HOLD'}):
            raise ValueError('Source-side reading cannot clear counterpart claims or HOLDs')
    task = next(t for t in plan['tasks'] if t['id'] == 'ED-02')
    if task['status'] != 'OPEN':
        raise ValueError('ED-02 cannot silently claim closure through negative metadata search')
    return len(cases)


if __name__ == '__main__':
    main()
