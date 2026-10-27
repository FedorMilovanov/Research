#!/usr/bin/env python3
"""Read-only extraction of candidate-name notes from one SHA-pinned TCP witness.

This audits the Charnock side only. It does not resolve identities or certify the
books cited. Printed page labels are TEI transcriptions, not newly read images.
"""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from audit_charnock_cudworth_refs import SOURCES

PATTERNS = {
    'LING': re.compile(r'lingend', re.I),
    'RAY': re.compile(r'rayn(?:aud|ard)', re.I),
    'SANCT': re.compile(r'sanct\.\s*in\s+loc', re.I),
    'ZARN': re.compile(r'zarnovec', re.I),
    'MAG': re.compile(r'magalano', re.I),
    'PLACE': re.compile(r'placeus', re.I),
    # Lexical candidates, including damaged spelling; not resolved identities.
    'DAIL': re.compile(r'\bdai(?:ll?[eèéêá]|l(?=\s*[•.]))|\bdall(?:e|ae)', re.I),
}


def local(element):
    return element.tag.rsplit('}', 1)[-1].lower()


def plain(element):
    return ' '.join(''.join(element.itertext()).replace('ſ', 's').split())


def extract(path, identifier="A32723"):
    if identifier not in ("A32723", "A32724"):
        raise ValueError("Unsupported Charnock witness: " + identifier)
    raw = path.read_bytes()
    revision, expected = SOURCES[identifier]
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected:
        raise ValueError(identifier + ': SHA-256 mismatch; refusing unpinned input')
    root = ET.fromstring(raw)
    body = root.find('.//{http://www.tei-c.org/ns/1.0}text')
    if body is None:
        raise ValueError(identifier + ': no TEI text body')
    parents = {child: node for node in body.iter() for child in node}
    page = None
    notes = []
    entered_on_page = {}
    for node in body.iter():
        if local(node) == 'pb':
            page = node.get('n')
        entered_on_page[node] = page
        if local(node) == 'note':
            text = plain(node)
            matches = [key for key, pattern in PATTERNS.items() if pattern.search(text)]
            if matches:
                ancestor = node
                discourse = None
                while ancestor in parents:
                    ancestor = parents[ancestor]
                    if local(ancestor) == 'div' and ancestor.get('type') == 'discourse':
                        discourse = next((plain(child) for child in ancestor
                                          if local(child) == 'head'), None)
                        break
                notes.append({'groups': matches, 'printed_page_label': page,
                              'note': text, 'parent_start_page_label': entered_on_page[parents[node]],
                              'discourse_heading': discourse,
                              'parent_context': plain(parents[node])})
    discourse_rows = []
    for division in body.iter():
        if local(division) == 'div' and division.get('type') == 'discourse':
            heading = next((plain(child) for child in division
                            if local(child) == 'head'), None)
            discourse_rows.append({'heading': heading,
                                   'note_elements': sum(local(item) == 'note'
                                                        for item in division.iter())})
    # Count each note once even if discourse divisions are nested.
    discourse_notes = set()
    for division in body.iter():
        if local(division) == 'div' and division.get('type') == 'discourse':
            discourse_notes.update(item for item in division.iter() if local(item) == 'note')
    all_notes = sum(local(item) == 'note' for item in body.iter())
    inventory = {'scope': 'tei_structure_not_reading_or_verification_progress',
                 'text_note_elements': all_notes,
                 'discourse_note_elements': len(discourse_notes),
                 'outside_discourses_note_elements': all_notes - len(discourse_notes),
                 'discourse_divisions': len(discourse_rows),
                 'discourses': discourse_rows}
    return {'scope': 'named_notes_only_not_exhaustive_variants_or_influence',
            'witness_inventory': inventory,
            'tcp': identifier, 'revision': revision, 'sha256': digest,
            'counts': {key: sum(key in row['groups'] for row in notes) for key in PATTERNS},
            'notes': notes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml', type=Path)
    parser.add_argument('--tcp', choices=('A32723', 'A32724'), default='A32723')
    args = parser.parse_args()
    try:
        report = extract(args.xml, args.tcp)
    except (OSError, ValueError, ET.ParseError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
