#!/usr/bin/env python3
"""Extract/check a bounded reading route from the registered A32723 XML bytes.

Not a full-book reading claim or image/pagination certification. No network or writes.
Paragraph ordinals include epigraph paragraphs, exclude note/fw paragraphs and
nested paragraphs. Long-s and whitespace normalized; note/fw bodies omitted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.tei-c.org/ns/1.0}'
TARGETS = [(2, 'Men may have Atheistical hearts'), (3, 'THE words are part'),
           (6, 'The Creation was a real change'), (14, 'THE Subject of this')]


def plain(node):
    def walk(n):
        result = [n.text or '']
        for child in n:
            if child.tag not in {NS + 'note', NS + 'fw'}:
                result += walk(child)
            result += [child.tail or '']
        return result
    return ' '.join(''.join(walk(node)).replace('ſ', 's').split())


def extract(path, registry):
    source = registry['sources']['A32723']
    raw = path.read_bytes()
    if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
        raise ValueError('A32723 byte size/SHA mismatch')
    tree = ET.fromstring(raw)
    text = tree.find('.//' + NS + 'text')
    if text is None:
        raise ValueError('Missing text body')
    parents = {c: n for n in text.iter() for c in n}
    page, page_at = None, {}
    for node in text.iter():
        if node.tag == NS + 'pb':
            page = node.get('n')
        page_at[node] = page
    divisions = text.findall('.//' + NS + 'div[@type="discourse"]')
    if len(divisions) != 14:
        raise ValueError('Expected fourteen discourse divisions')
    route, cards = [], []
    for ordinal, discourse in enumerate(divisions, 1):
        breaks = [n.get('n') for n in discourse.iter(NS + 'pb')]
        numbered = [p for p in breaks if p is not None]
        head = discourse.find(NS + 'head')
        epi = discourse.find(NS + 'epigraph')
        paragraphs = []
        for p in discourse.iter(NS + 'p'):
            ancestor, excluded = p, False
            while ancestor in parents and ancestor is not discourse:
                ancestor = parents[ancestor]
                if ancestor.tag in {NS + 'p', NS + 'note', NS + 'fw'}:
                    excluded = True
            if not excluded:
                paragraphs.append(p)
        route.append(dict(ordinal=ordinal, heading=plain(head),
                          epigraph=plain(epi) if epi is not None else None,
                          firstNumberedPage=numbered[0], lastNumberedPage=numbered[-1],
                          unnumberedBreaks=sum(p is None for p in breaks),
                          noteElements=len(list(discourse.iter(NS + 'note'))),
                          firstBodyParagraph=next(plain(p) for p in paragraphs if parents[p] is discourse)))
        for target, probe in TARGETS:
            if ordinal != target:
                continue
            matches = [(i, p) for i, p in enumerate(paragraphs) if probe.lower() in plain(p).lower()]
            if len(matches) != 1:
                raise ValueError('Context probe must locate exactly one paragraph')
            index, selected = matches[0]
            window = []
            for i in range(max(0, index - 1), min(len(paragraphs), index + 3)):
                paragraph = paragraphs[i]
                value = plain(paragraph)
                window.append(dict(paragraphIndexZeroBased=i, startTeiPage=page_at[paragraph],
                                   text=value, textSha256=hashlib.sha256(value.encode()).hexdigest()))
            cards.append(dict(id='BOOK-' + str(ordinal).zfill(2), discourse=ordinal,
                              selectedParagraphIndexZeroBased=index,
                              selectedStartTeiPage=page_at[selected], contextWindow=window))
    return dict(source='A32723', sourceSha256=source['sha256'], sourceBytes=source['size'],
                route=route, contexts=cards,
                paginationBoundary='First/last numbered TEI labels only;not continuous page coverage or image verification',
                normalization='long-s and whitespace;note/fw bodies excluded,tails retained')


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
            if plan['principalBookReading']['byteVerifiedExtraction'] != result:
                raise ValueError('Stored reading route/context differs from pinned XML')
            print('Fourteen discourse routes/four context windows: PASS;not full-book certification')
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
