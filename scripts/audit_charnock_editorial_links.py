#!/usr/bin/env python3
"""Read-only plan-level routing audit;not a future chapter or foreign-quote review."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain
from audit_charnock_biographical_anchors import text_and_pages, normalize
from audit_charnock_handoff import canonical_bytes
from build_biographies_shared_atlas import validate as validate_atlas

ROOT = Path(__file__).resolve().parents[1]
AXES = ['evidenceClass', 'accessState', 'locatorState', 'rightsState', 'publicationState', 'holds']


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def extract(directory, registry):
    result = {}
    for identifier, probes in [('A41722', ['XXXV.', 'XXXVI.', 'XXXVII.']),
                               ('B20167', ['THE Works of Mr. Stephen Charnock on Various Divine Subjects. In Folio. 2 Vol.'])]:
        source = registry['sources'][identifier]
        raw = (directory / (identifier + '.xml')).read_bytes()
        if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
            raise ValueError(identifier + ': byte pin mismatch')
        root = ET.fromstring(raw)
        whole, pages = text_and_pages(raw)
        paragraphs = []
        for probe in probes:
            matches = [p for p in root.iter(NS + 'p') if plain(p).startswith(probe)]
            if len(matches) != 1 or whole.count(normalize(probe)) != 1:
                raise ValueError(identifier + ': unique paragraph probe required')
            text = plain(matches[0])
            at = whole.index(normalize(probe))
            span = list(dict.fromkeys(pages[at:at + len(normalize(probe))]))
            paragraphs.append(dict(probe=probe, probeTeiPages=span, text=text,
                                   textSha256=hashlib.sha256(text.encode()).hexdigest()))
        result[identifier] = dict(sourceSha256=source['sha256'], sourceBytes=source['size'], paragraphs=paragraphs,
                                  boundary='Selected norm/advertisement paragraphs;not enforcement,personal conduct or sales')
    return result


def check_review(plan, registry, root=ROOT):
    review = plan['routingReview']
    if (review['reviewState'] != 'BOUNDED_PLAN_ROUTING_NOT_DRAFT_REVIEW'
            or review['draftDeduplicationVerified'] is not False or review['foreignQuotationsReverified'] is not False):
        raise ValueError('Routing is plan-level,not a completed draft/foreign quotation audit')
    anchors = {a['id']: a for a in registry['anchors'] + registry['supportAnchors']}
    documents = plan['documents']
    used = {ref for d in documents for ref in d['primaryRefs'] + d['crossRefs']}
    required = {r for r in used if r.startswith(('CTX-', 'GOV-', 'REC-'))} | {'BIB-08'}
    claims = review['contextReceptionDecisions']
    if len(claims) != len(required) or {c['ref'] for c in claims} != required:
        raise ValueError('Every selected context/reception reference requires a wording decision')
    for c in claims:
        a = anchors[c['ref']]
        if (c['canonicalAnchorSha256'] != digest(a) or c['source'] != a['source']
                or any(c['sourceStateSnapshot'][k] != a[k] for k in AXES)
                or not c['allowedParaphrase'] or not c['prohibitedInference']
                or c['basis'] != 'PRESERVED_REGISTRY_WITH_EXPLICIT_FRESH_SUBSET'
                or c['publicationUse'] != 'NOT_APPROVED'):
            raise ValueError('Context/reception decision cannot promote evidence or erase its boundary')
        companion = ['REC-06'] if c['ref'] == 'REC-05' else ['REC-05'] if c['ref'] == 'REC-06' else []
        if c['requiredCompanionRefs'] != companion:
            raise ValueError('Hoek criticism and positive conclusion must remain paired')
    rules = {tuple(r['pair']): r for r in plan['duplicationRules']}
    handoffs = review['ownershipHandoffs']
    if len(handoffs) != len(rules) or {tuple(h['pair']) for h in handoffs} != set(rules):
        raise ValueError('Five existing duplication boundary rules must be explicitly routed')
    by_doc = {d['id']: d for d in documents}
    owners = {ref: d['id'] for d in documents for ref in d['primaryRefs']}
    for h in handoffs:
        left, right = h['pair']
        d1, d2 = by_doc[left], by_doc[right]
        shared = set(d1['primaryRefs'] + d1['crossRefs']) & set(d2['primaryRefs'] + d2['crossRefs'])
        if (h['ruleSha256'] != digest(rules[tuple(h['pair'])]) or set(h['sharedRefOwners']) != shared
                or any(h['sharedRefOwners'][r] != owners[r] for r in shared)
                or h['transferMode'] != 'CROSS_REFERENCE_NOT_SECOND_FULL_EXPOSITION' or not h['handoffQuestion']):
            raise ValueError('Shared reference must retain one full-analysis owner')
    transitions = review['transitionQuestions']
    expected_pairs = list(zip([d['id'] for d in documents][:-1], [d['id'] for d in documents][1:]))
    if [tuple(t['pair']) for t in transitions] != expected_pairs:
        raise ValueError('Nine adjacent transitions required,not reader chapter prose')
    for t in transitions:
        refs = {r for doc in t['pair'] for r in by_doc[doc]['primaryRefs'] + by_doc[doc]['crossRefs']}
        if not t['question'] or not t['refs'] or not set(t['refs']) <= refs:
            raise ValueError('Transition question requires references from its adjacent documents')
    graph_path = root / 'data/biographies-shared-atlas-v1.json'
    graph = json.loads(graph_path.read_text())
    validate_atlas(graph, registry, root)
    if (review['atlasCanonicalSha256'] != digest(graph)
            or review['excludedLinksSnapshot'] != graph['excludedLinks']
            or review['edgeBoundarySnapshot'] != graph['edges']):
        raise ValueError('Atlas types/exclusions cannot be promoted to personal influence')
    bridges = review['corpusBridges']
    if len(bridges) != 3 or {b['edgeId'] for b in bridges} != {'shared-reception-nav', 'heart-nav', 'apostasy-nav'}:
        raise ValueError('Three bounded cross-corpus navigation bridges required')
    nodes = {n['id']: n for n in graph['nodes']}
    edges = {e['id']: e for e in graph['edges']}
    for b in bridges:
        edge = edges[b['edgeId']]
        snapshot = b['ownerExcerpt']
        path = (root / snapshot['path']).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError('Bridge owner must remain inside Research')
        raw = path.read_bytes()
        if (snapshot['sha256'] != hashlib.sha256(raw).hexdigest() or snapshot['size'] != len(raw)
                or not snapshot['text'] or snapshot['text'] not in raw.decode()
                or snapshot['textSha256'] != hashlib.sha256(snapshot['text'].encode()).hexdigest()):
            raise ValueError('Owner excerpt snapshot differs from actual bytes')
        if (edge['type'] != 'NAVIGATION' or edge['refs'] or b['authorityPath'] != nodes[edge['to']]['owner']
                or not (root / b['authorityPath']).is_file() or not b['relatedRefs'] or not set(b['relatedRefs']) <= used
                or b['relation'] != 'RESEARCH_NAVIGATION_NOT_HISTORICAL_INFLUENCE'
                or not b['reuseBoundary']):
            raise ValueError('Navigation bridge cannot assert historical contact or quote approval')
    fresh = review['byteVerifiedContexts']
    if set(fresh) != {'A41722', 'B20167'}:
        raise ValueError('Two fresh norm/advertisement source contexts required')
    for identifier, entry in fresh.items():
        source = registry['sources'][identifier]
        if entry['sourceSha256'] != source['sha256'] or entry['sourceBytes'] != source['size']:
            raise ValueError('Fresh norm source pin differs')
        expected_probes = ['XXXV.', 'XXXVI.', 'XXXVII.'] if identifier == 'A41722' else ['THE Works of Mr. Stephen Charnock on Various Divine Subjects. In Folio. 2 Vol.']
        if [p['probe'] for p in entry['paragraphs']] != expected_probes:
            raise ValueError('Preserve all three constitutional qualifications and advertisement')
        for paragraph in entry['paragraphs']:
            if hashlib.sha256(paragraph['text'].encode()).hexdigest() != paragraph['textSha256']:
                raise ValueError('Fresh norm paragraph hash differs')
    return dict(routedContextReceptionReferences=len(claims), ownershipHandoffs=len(handoffs),
                transitionQuestions=len(transitions), crossCorpusBridges=len(bridges),
                draftDeduplicationVerified=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xml-dir', type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
        registry = json.loads((ROOT / plan['baselineRegistry']).read_text())
        report = check_review(plan, registry)
        if args.xml_dir and extract(args.xml_dir, registry) != plan['routingReview']['byteVerifiedContexts']:
            raise ValueError('Fresh norm/advertisement replay differs from stored context')
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
