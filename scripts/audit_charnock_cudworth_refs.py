#!/usr/bin/env python3
"""Read-only, bounded lexical audit; pass a directory containing the pinned TCP XMLs.

No negative result from this script proves absence of reading, borrowing or influence.
The XML bodies (including apparatus) are searched; TEI metadata are excluded.
"""
import argparse
import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCES = {
    'A32723': ('caa75dffdc96aa353a6424679877f41e15b8c73e', 'd6205c4062867acf7f01c963ca06395ed07bb4f00774a071fcc8f903d22e6376'),
    'A32724': ('aa97893297d0bd0db63318afd4957ac38d53dd05', 'efaf653b7c9d058927dc546382d3a9771fbffdc6e15b50d08a7941bd0aafa007'),
    'A35345': ('81cb68885c517252d3f7acccf5c1d52ab77c1e6c', '5ef15afca7c22866b6f1ce5a4c1286e88b898b1ab9ebd9ec0fb628043ac159c8'),
}
PATTERNS = {
    'cudworth': r'c[uv]d[\s-]*worth',
    'cudw_prefix': r'c[uv]d[\s-]*w',
    'intellectual_system': r'intellectual[\s-]+syst',
    'charnock': r'charnock',
}

def normalize(text):
    text = unicodedata.normalize('NFKC', text).replace('ſ', 's')
    return ' '.join(text.casefold().replace('ʋ', 'u').split())


def audit(directory):
    results = []
    for identifier, (revision, expected) in SOURCES.items():
        path = directory / (identifier + '-pinned.xml')
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected:
            raise ValueError(f'{identifier}: SHA-256 mismatch; refusing unpinned input')
        root = ET.fromstring(raw)
        body = root.find('.//{http://www.tei-c.org/ns/1.0}text')
        if body is None:
            raise ValueError(f'{identifier}: no TEI text body')
        text = normalize(''.join(body.itertext()))
        counts = {name: len(re.findall(pattern, text)) for name, pattern in PATTERNS.items()}
        results.append({'tcp': identifier, 'revision': revision, 'sha256': digest,
                        'normalized_characters': len(text), 'counts': counts})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.directory)
    except (OSError, ValueError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')
    control = result[-1]['counts']
    if not control['cudworth'] or not control['intellectual_system']:
        parser.exit(1, 'Positive control failed\n')
    print(json.dumps({'scope': 'lexical_only_not_reading_or_influence', 'sources': result},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
