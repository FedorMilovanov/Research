#!/usr/bin/env python3
"""Read-only replay of seven title-page transcription records,not page images.

Selects div@type=title_page,not the whole front or a half-title. No network/writes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from audit_charnock_book_route import NS, plain

ROOT = Path(__file__).resolve().parents[1]


def extract(directory, registry):
    records = {}
    for unit in registry['bibliographyUnits']:
        if unit['unitType'] != 'PRINTED_OBJECT':
            continue
        identifier = unit['source']
        source = registry['sources'][identifier]
        raw = (directory / (identifier + '.xml')).read_bytes()
        if len(raw) != source['size'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
            raise ValueError(identifier + ': byte pin mismatch')
        root = ET.fromstring(raw)
        front = root.find('.//' + NS + 'text/' + NS + 'front')
        if front is None:
            raise ValueError(identifier + ': missing front')
        titles = [n for n in front if n.tag == NS + 'div' and n.get('type') == 'title_page']
        if len(titles) != 1:
            raise ValueError(identifier + ': expected one explicit title_page,not a half-title')
        text = plain(titles[0])
        if not text:
            raise ValueError(identifier + ': empty title')
        records[unit['id']] = dict(source=identifier, sourceBytes=source['size'], sourceSha256=source['sha256'],
                                   titleText=text, titleTextSha256=hashlib.sha256(text.encode()).hexdigest(),
                                   selector='text/front/div[@type=title_page]',
                                   boundary='TCP title transcription only;no page image,authorial authorization or full edition collation')
    if len(records) != 7:
        raise ValueError('Seven printed objects required,not twelve acquired books')
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        registry = json.loads((ROOT / 'data/charnock-biographical-anchors-v1.json').read_text())
        result = extract(args.directory, registry)
        if args.check:
            plan = json.loads((ROOT / 'data/charnock-series-editorial-plan-v1.json').read_text())
            if result != plan['boundaryReview']['byteVerifiedTitles']:
                raise ValueError('Stored titles differ from pinned XML')
            print('Seven byte-pinned TCP titles: PASS;not image collation or acquisition of five families')
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
