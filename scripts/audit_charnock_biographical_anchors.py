#!/usr/bin/env python3
"""Read-only checks of selected biography anchors against byte-pinned TCP XML.

Exact lexical presence is not independent corroboration or publication approval.
Normalizes whitespace and long-s only; page labels are TEI, not image checks.
"""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize(text):
    return ' '.join(text.replace('ſ', 's').split())


def text_and_pages(raw):
    root = ET.fromstring(raw)
    text = root.find('.//{http://www.tei-c.org/ns/1.0}text')
    if text is None:
        raise ValueError('Missing TEI text')
    chunks, pages = [], []
    page = None

    def emit(value):
        if value:
            chunks.append(value.replace('ſ', 's'))
            pages.extend([page] * len(value))

    def visit(node):
        nonlocal page
        if node.tag.rsplit('}', 1)[-1] == 'pb':
            page = node.get('n')
        emit(node.text)
        for child in node:
            visit(child)
            emit(child.tail)
    visit(text)
    joined = ''.join(chunks)
    # Keep page provenance while collapsing whitespace, including inter-element spaces.
    out, labels, pending_space = [], [], False
    for char, label in zip(joined, pages):
        if char.isspace():
            pending_space = bool(out)
        else:
            if pending_space:
                out.append(' ')
                labels.append(label)
                pending_space = False
            out.append(char)
            labels.append(label)
    return ''.join(out), labels


def audit_publication_units(registry):
    """Check object/family identity and state inheritance; not historical completeness."""
    anchors = {a['id']: a for a in registry['anchors'] + registry.get('supportAnchors', [])}
    seen = set()
    axes = ('evidenceClass', 'accessState', 'locatorState', 'rightsState', 'publicationState', 'holds')
    for unit in registry.get('bibliographyUnits', []):
        if unit['id'] in seen:
            raise ValueError('Duplicate bibliography unit')
        seen.add(unit['id'])
        if not unit.get('boundary') or not unit.get('owner'):
            raise ValueError('Missing bibliography boundary/owner')
        if any(ref not in anchors for ref in unit['refs']):
            raise ValueError('Unknown bibliography anchor')
        if unit['unitType'] == 'PRINTED_OBJECT':
            if unit.get('source') not in registry['sources']:
                raise ValueError('Unknown printed object source')
            source = registry['sources'][unit['source']]
            if not unit['refs'] or any(anchors[ref]['source'] != unit['source'] for ref in unit['refs']):
                raise ValueError('Printed object refs must identify its own source')
            if any(unit.get(key) != source.get(key) for key in axes):
                raise ValueError('Printed object states must inherit source states')
        elif unit['unitType'] == 'ACQUISITION_FAMILY':
            if (unit.get('accessState') == 'FULL_OBJECT_VERIFIED'
                    or unit.get('publicationState') != 'BLOCKED'
                    or not {'ARCHIVE_HOLD', 'EVIDENCE_HOLD'} <= set(unit.get('holds', []))):
                raise ValueError('Unacquired family must remain blocked with archive/evidence holds')
        else:
            raise ValueError('Unknown bibliography unit type')
    return len(seen)


def audit_edition_comparisons(registry, texts):
    """Selected lexical matches are not whole-edition identity or authorization."""
    seen = set()
    for comparison in registry.get('editionComparisons', []):
        if comparison['id'] in seen:
            raise ValueError('Duplicate comparison ID')
        seen.add(comparison['id'])
        if (comparison['comparisonType'] != 'SELECTED_SHARED_READING'
                or len(comparison['objects']) != 2 or not comparison.get('boundary')):
            raise ValueError('Comparison must remain selected and bounded')
        if comparison['objects'][0]['source'] == comparison['objects'][1]['source']:
            raise ValueError('Comparison needs two distinct objects')
        needle = normalize(comparison['probe'])
        for obj in comparison['objects']:
            if obj['source'] not in texts:
                raise ValueError('Unknown comparison source')
            text, labels = texts[obj['source']]
            if not needle or text.count(needle) != 1:
                raise ValueError('Comparison requires one exact match per object')
            at = text.index(needle)
            if list(dict.fromkeys(labels[at:at + len(needle)])) != obj['teiPages']:
                raise ValueError('Comparison page mismatch')
    return len(seen)


def audit_research_handoff(registry):
    """Selection and unsent requests do not grant publication or acquisition status."""
    selection = registry.get('seriesSelection', [])
    anchors = {a['id']: a for a in registry['anchors'] + registry.get('supportAnchors', [])}
    if selection:
        expected = {'INTRO', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'REFERENCE'}
        if len(selection) != 10 or {s['id'] for s in selection} != expected:
            raise ValueError('Selection must cover ten distinct documents')
        for item in selection:
            refs = item['refs']
            if not 3 <= len(refs) <= 5 or len(refs) != len(set(refs)):
                raise ValueError('Selection needs three to five distinct references')
            if (item.get('selectionState') != 'SELECTION_ONLY'
                    or item.get('publicationState') != 'BLOCKED'
                    or 'PUBLICATION_HOLD' not in item.get('holds', []) or not item.get('boundary')):
                raise ValueError('Selection cannot grant publication or hide boundary')
            for ref in refs:
                if ref not in anchors:
                    raise ValueError('Unknown selection anchor')
                a = anchors[ref]
                if (a['evidenceClass'] in {'C', 'D'}
                        or a['locatorState'] != 'EXACT_LOCATOR_VERIFIED'):
                    raise ValueError('Selection requires identified checked loci')
    families = {u['id'] for u in registry.get('bibliographyUnits', [])
                if u['unitType'] == 'ACQUISITION_FAMILY'}
    seen = set()
    for request in registry.get('acquisitionRequests', []):
        if request['id'] in seen or request['family'] not in families:
            raise ValueError('Duplicate request or unknown family')
        seen.add(request['id'])
        if request.get('requestState') != 'DRAFT_NOT_SENT' or request.get('receipt') is not None:
            raise ValueError('Draft cannot claim dispatch or receipt')
        if (request.get('accessState') != 'NOT_ACQUIRED'
                or request.get('publicationState') != 'BLOCKED'
                or not {'ARCHIVE_HOLD', 'EVIDENCE_HOLD', 'PUBLICATION_HOLD'} <= set(request['holds'])):
            raise ValueError('Unsent request must remain unacquired and blocked')
        if (len(request.get('expectedPacket', [])) < 3 or len(request.get('acceptance', [])) < 3
                or not request.get('boundary') or not request['target'].startswith('https://')):
            raise ValueError('Request needs bounded delivery and acceptance criteria')
    return {'documents': len(selection), 'requests': len(seen)}


REQUIRED_BIOGRAPHICAL_TOPICS = frozenset('''BIRTH_PLACE BIRTH_YEAR FATHER MATRICULATION TUTOR
CONVERSION CONVERSION_NOTE SOUTHWARK OXFORD_MOVE FELLOWSHIP MA_INCORPORATION PROCTOR
IRELAND_ARRIVAL PATRON_TITLE IRELAND_LENGTH DUBLIN_BD DUBLIN_POSTS RESTORATION_RETURN
UNSETTLED_PERIOD CONTINENTAL_TRIPS FIRE CROMWELL1659 CONSPIRACY1663 LAST_MINISTRY
WATSON_RELATION FOWLER_IDENTITY PREACHING_NOTES HEALTH MEDICINE DOCTRINAL_AFFILIATION
POPISH_PLOT_NOTE WILL_FAMILY CELIBACY AUCTION_WEALTH FORESEEN_DEATH DEATH_PLACE
DEATH_DATE BURIAL LAST_TOPIC WORKS_PUBLICATION'''.split())


def audit_biographical_core(registry):
    """Validate a bounded wording apparatus, never historical truth or publication."""
    if 'biographicalCoreReview' not in registry:
        if any(a['id'].startswith('CORE-') for a in registry['anchors']):
            raise ValueError('Missing biographical core review')
        return 0  # Legacy/synthetic registries have no core layer.
    review = registry['biographicalCoreReview']
    if (not isinstance(review, dict) or review.get('reviewState') != 'BOUNDED_WORDING_REVIEW'
            or not review.get('scope')):
        raise ValueError('Core review must remain bounded')
    rows = review.get('items', [])
    if (len(rows) != len(REQUIRED_BIOGRAPHICAL_TOPICS)
            or {x['topic'] for x in rows} != REQUIRED_BIOGRAPHICAL_TOPICS
            or len({x['id'] for x in rows}) != len(rows)):
        raise ValueError('Core topics or IDs missing/duplicated')
    anchors = {a['id']: a for a in registry['anchors'] + registry.get('supportAnchors', [])}
    policy = json.loads((Path(__file__).resolve().parents[1] / 'data/repository-evidence-policy-v2.json').read_text())
    axes = {'evidenceClass': 'sourceClasses', 'accessState': 'accessStates',
            'locatorState': 'locatorStates', 'rightsState': 'rightsStates',
            'publicationState': 'publicationStates'}
    for row in rows:
        if any(row.get(k) not in policy[v] for k, v in axes.items()):
            raise ValueError('Invalid core evidence/state axis')
        holds = row.get('holds', [])
        if (row['publicationState'] != 'BLOCKED' or 'PUBLICATION_HOLD' not in holds
                or not set(holds) <= set(policy['holds']) or not row.get('boundary')):
            raise ValueError('Core cannot grant publication or hide boundary')
        refs = row.get('refs', [])
        if len(refs) != len(set(refs)) or any(ref not in anchors for ref in refs):
            raise ValueError('Unknown or duplicated core reference')
        disposition = row.get('disposition')
        if disposition == 'EXCLUDE':
            if row.get('safeFormulation') is not None or not row.get('excludedClaim') or 'EVIDENCE_HOLD' not in holds:
                raise ValueError('Excluded claim cannot have an approved formulation')
        elif disposition in {'ATTRIBUTED', 'APPROXIMATE', 'CONFLICT'}:
            if not row.get('safeFormulation') or row.get('excludedClaim') is not None or not refs:
                raise ValueError('Positive wording needs a formulation and references')
            for ref in refs:
                a = anchors[ref]
                if (a['evidenceClass'] not in {'A1', 'A2', 'A3'}
                        or a['accessState'] != 'FULL_OBJECT_VERIFIED'
                        or a['locatorState'] != 'EXACT_LOCATOR_VERIFIED'):
                    raise ValueError('Positive wording needs checked primary loci')
            if any(row[k] != anchors[refs[0]][k] for k in ('evidenceClass', 'accessState', 'locatorState', 'rightsState')):
                raise ValueError('Core axes must inherit the cited support, not invent verification')
            if disposition == 'CONFLICT' and len({anchors[ref].get('source') for ref in refs}) < 2:
                raise ValueError('Conflict needs both distinct source objects; independence is not implied')
        else:
            raise ValueError('Invalid core disposition')
        if row['topic'] == 'DEATH_DATE' and disposition != 'CONFLICT':
            raise ValueError('Death-date conflict must remain explicit until a new reviewed resolution')
    return len(rows)


def audit_reception_review(registry, root=None):
    """Check typed cases and selected-extract integrity, not remote text or influence."""
    if 'receptionReview' not in registry:
        if any(a.get('extractId') for a in registry.get('supportAnchors', [])):
            raise ValueError('Missing reception review')
        return 0
    root = root or Path(__file__).resolve().parents[1]
    review = registry['receptionReview']
    if (not isinstance(review, dict) or review.get('reviewState') != 'BOUNDED_RECEPTION_SAMPLE'
            or not review.get('scope')):
        raise ValueError('Reception review must remain bounded')
    archive = review['extractArchive']
    path = (root / archive['path']).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Unsafe reception archive path')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != archive['sha256']:
        raise ValueError('Reception extract SHA mismatch')
    if (archive.get('rawObjectSha256') is not None
            or archive.get('kind') != 'MANUAL_SELECTED_FETCH_EXTRACTS_NOT_RAW_OBJECTS'):
        raise ValueError('Selected extracts cannot claim a raw-object pin')
    extracted = json.loads(raw)['items']
    if len({x['id'] for x in extracted}) != len(extracted):
        raise ValueError('Duplicate reception extract')
    anchors = {a['id']: a for a in registry['anchors'] + registry.get('supportAnchors', [])}
    for item in extracted:
        a = anchors.get(item['id'], {})
        if a.get('extractId') != item['id'] or a.get('observedText') != item['text']:
            raise ValueError('Reception extract/anchor mismatch')
    cases = review.get('items', [])
    types = {'POLITICAL_FRAMING', 'ANTHOLOGY_USE', 'EDITORIAL_PROMOTION',
             'COMMENDATION', 'SCHOLARLY_CRITIQUE'}
    if (len(cases) != 5 or {c['receptionType'] for c in cases} != types
            or len({c['id'] for c in cases}) != len(cases)):
        raise ValueError('Reception needs five distinct typed cases')
    for case in cases:
        if (case.get('publicationState') != 'BLOCKED'
                or 'PUBLICATION_HOLD' not in case.get('holds', []) or not case.get('boundary')):
            raise ValueError('Reception cannot grant publication or hide boundary')
        if (case.get('influenceState') != 'NOT_INFERRED'
                or case.get('independenceState') != 'NOT_ESTABLISHED'):
            raise ValueError('Reception cannot infer influence or independence')
        refs = case.get('witnessRefs', [])
        primary = case.get('counterpartRefs', [])
        if not refs or len(set(refs + primary)) != len(refs + primary) or any(x not in anchors for x in refs + primary):
            raise ValueError('Unknown, missing or duplicate reception reference')
        for key in ('evidenceClass', 'accessState', 'locatorState', 'rightsState'):
            if case.get(key) != anchors[refs[0]][key]:
                raise ValueError('Reception axes cannot overstate witness support')
        if case['receptionType'] == 'SCHOLARLY_CRITIQUE' and not primary:
            raise ValueError('Scholarly critique needs primary-text counterparts')
        for ref in primary:
            a = anchors[ref]
            if (a['evidenceClass'] not in {'A1', 'A2', 'A3'}
                    or a['accessState'] != 'FULL_OBJECT_VERIFIED'
                    or a['locatorState'] != 'EXACT_LOCATOR_VERIFIED'):
                raise ValueError('Counterpart needs checked primary locus')
    return len(cases)


def audit_research_preparation(registry, root=None):
    """Validate recorded research dispositions, not the scholarly adequacy judgement."""
    if 'researchPreparationReview' not in registry:
        return None  # Legacy and isolated lexical fixtures.
    root = root or Path(__file__).resolve().parents[1]
    review = registry['researchPreparationReview']
    if (review.get('reviewState') != 'BOUNDED_MATERIAL_PREPARATION'
            or review.get('contentDecision') != 'SATISFIED_WITH_LIMITS'
            or review.get('quotationDecision') != 'DISPOSITIONS_RECORDED_NOT_PUBLICATION_APPROVAL'
            or review.get('nextGate') != 'FINAL_CONSISTENCY_AND_VERIFIED_HANDOFF'
            or 'PUBLICATION_HOLD' not in review.get('holds', []) or not review.get('scope')):
        raise ValueError('Preparation must remain bounded and publication-held')
    anchors = {a['id']: a for a in registry['anchors'] + registry.get('supportAnchors', [])}
    selected = {s['id']: s['refs'] for s in registry['seriesSelection']}
    areas = review.get('contentAreas', [])
    if len(areas) != 3 or {a['document'] for a in areas} != {'INTRO', 'VII', 'VIII'}:
        raise ValueError('Preparation needs three distinct content areas')
    for area in areas:
        if (area['refs'] != selected[area['document']] or area.get('decision') != 'ACCEPTED_BOUNDED'
                or not area.get('boundary') or len(area.get('exclusions', [])) < 3
                or area.get('publicationState') != 'BLOCKED'
                or 'PUBLICATION_HOLD' not in area.get('holds', [])):
            raise ValueError('Content acceptance must match selection and retain exclusions/HOLD')
        covered = set()
        for claim in area.get('coveredClaims', []):
            if not claim.get('safeUse') or not claim.get('refs') or not set(claim['refs']) <= set(area['refs']):
                raise ValueError('Coverage needs a bounded use of selected references')
            covered.update(claim['refs'])
        if covered != set(area['refs']):
            raise ValueError('Every selected content reference needs a stated use')
    quotes = review.get('quotationPlan', [])
    if not quotes or len({q['id'] for q in quotes}) != len(quotes) or len({q['ref'] for q in quotes}) != len(quotes):
        raise ValueError('Quote IDs and references must be nonempty and unique')
    candidates = research_only = 0
    documents = set()
    for quote in quotes:
        ref = quote['ref']
        if ref not in anchors:
            raise ValueError('Unknown quote reference')
        a = anchors[ref]
        docs = quote.get('documents', [])
        if not docs or len(set(docs)) != len(docs) or any(d not in selected or ref not in selected[d] for d in docs):
            raise ValueError('Quote must belong to its selected document slots')
        documents.update(docs)
        if (quote.get('publicationState') != 'BLOCKED'
                or quote.get('holds') != a['holds'] or 'PUBLICATION_HOLD' not in quote['holds']
                or quote.get('boundary') != a['claimBoundary']
                or any(quote.get(k) != a[k] for k in ('evidenceClass', 'accessState', 'locatorState', 'rightsState'))):
            raise ValueError('Quote cannot overstate source axes, boundary or publication')
        if not quote.get('attribution') or quote.get('translationState') != 'NOT_PREPARED':
            raise ValueError('Quote needs an attributed voice;translation is not prepared')
        archive = quote['archive']
        if quote['decision'] == 'TEXT_CANDIDATE':
            candidates += 1
            if (ref not in {x['id'] for x in registry['anchors']}
                    or a['evidenceClass'] not in {'A1', 'A2', 'A3'}
                    or a['accessState'] != 'FULL_OBJECT_VERIFIED'
                    or a['locatorState'] != 'EXACT_LOCATOR_VERIFIED'
                    or a['rightsState'] != 'PUBLICATION_ELIGIBLE'
                    or set(a['holds']) != {'PUBLICATION_HOLD'}
                    or quote.get('textKind') != 'LEXICAL_FRAGMENT_NOT_FINAL_QUOTATION'
                    or quote.get('quoteText') != a['probe']
                    or quote['locator'].get('teiPages') != a['teiPages']):
                raise ValueError('Text candidate requires checked primary text and eligible text rights')
            source = registry['sources'][a['source']]
            if (archive.get('kind') != 'PINNED_TCP_XML' or archive.get('source') != a['source']
                    or archive.get('commit') != source['commit'] or archive.get('sha256') != source['sha256']
                    or archive.get('member') != 'xml/' + a['source'] + '.xml' or not archive.get('driveBaseId')):
                raise ValueError('Candidate archive pin must match its source')
        elif quote['decision'] == 'RESEARCH_ONLY':
            research_only += 1
            if (quote.get('textKind') != 'NO_DIRECT_QUOTATION_SELECTED'
                    or quote.get('quoteText') is not None or archive.get('rawObjectSha256') is not None
                    or archive.get('kind') not in {'REGISTRY_OBSERVATION_ONLY', 'SELECTED_EXTRACT_ONLY'}):
                raise ValueError('Research-only entry cannot supply a cleared quote or raw pin')
            if archive.get('kind') == 'SELECTED_EXTRACT_ONLY':
                extracted = registry['receptionReview']['extractArchive']
                if archive.get('sha256') != extracted['sha256'] or archive.get('path') != extracted['path']:
                    raise ValueError('Research quote extract pin mismatch')
        else:
            raise ValueError('Unknown quote disposition')
    if documents != set(selected):
        raise ValueError('Quote dispositions must cover ten documents')
    group = {q['ref'] for q in quotes if q.get('conflictGroup') == 'DEATH-DATE-1680'}
    if group != {'BIO-17', 'CORE-06'}:
        raise ValueError('Death-date quote candidates must retain both conflict witnesses')
    if (review.get('externalImagesDecision') != 'NONE_SELECTED'
            or not review.get('externalImagesBoundary') or not review.get('normalization')):
        raise ValueError('External image and transcription boundaries required')
    figures = review.get('illustrations', [])
    if len(figures) != 1:
        raise ValueError('Only the shared research SVG is selected in this review')
    figure = figures[0]
    if (figure.get('path') != 'БИОГРАФИИ/atlas/biographies-shared.svg'
            or figure.get('graphPath') != 'data/biographies-shared-atlas-v1.json'
            or figure.get('accessState') != 'FULL_OBJECT_VERIFIED'
            or figure.get('locatorState') != 'EXACT_LOCATOR_VERIFIED'
            or figure.get('decision') != 'RESEARCH_ONLY' or figure.get('publicationState') != 'BLOCKED'
            or figure.get('evidenceClass') != 'C' or figure.get('rightsState') != 'RIGHTS_UNKNOWN'
            or not {'EVIDENCE_HOLD', 'RIGHTS_HOLD', 'PUBLICATION_HOLD'} <= set(figure.get('holds', []))
            or not figure.get('caption') or not figure.get('boundary')):
        raise ValueError('Shared illustration is not historical evidence or cleared publication')
    for pathkey, shakey in [('path', 'sha256'), ('graphPath', 'graphSha256')]:
        path = (root / figure[pathkey]).resolve()
        if not path.is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != figure[shakey]:
            raise ValueError('Illustration or graph SHA/path mismatch')
    return {'areas': len(areas), 'candidates': candidates, 'researchOnly': research_only, 'illustrations': len(figures)}


def audit(registry, directory):
    audit_publication_units(registry)
    audit_research_handoff(registry)
    audit_biographical_core(registry)
    audit_reception_review(registry)
    audit_research_preparation(registry)
    texts = {}
    for key, source in registry['sources'].items():
        raw = (directory / (key + '.xml')).read_bytes()
        if hashlib.sha256(raw).hexdigest() != source['sha256']:
            raise ValueError(key + ': SHA-256 mismatch')
        texts[key] = text_and_pages(raw)
    audit_edition_comparisons(registry, texts)
    results = []
    ids = set()
    for anchor in registry['anchors']:
        if anchor['id'] in ids:
            raise ValueError('Duplicate anchor ID')
        ids.add(anchor['id'])
        text, labels = texts[anchor['source']]
        needle = normalize(anchor['probe'])
        if not needle or text.count(needle) != 1:
            raise ValueError(anchor['id'] + ': expected one exact match')
        at = text.index(needle)
        span = list(dict.fromkeys(labels[at:at + len(needle)]))
        if span != anchor['teiPages']:
            raise ValueError(anchor['id'] + ': page mismatch ' + repr(span))
        results.append({'id': anchor['id'], 'teiPages': span, 'lexicalCheck': 'PASS'})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml_directory', type=Path)
    parser.add_argument('--registry', type=Path, default=Path(__file__).resolve().parents[1] / 'data/charnock-biographical-anchors-v1.json')
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(args.registry.read_text()), args.xml_directory), ensure_ascii=False, indent=2))
