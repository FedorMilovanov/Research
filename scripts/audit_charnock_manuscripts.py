#!/usr/bin/env python3
"""Read-only structural guard for Charnock's ten draft manuscripts.

It does not verify historical claims, source bytes, translations or publication rights.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = Path('БИОГРАФИИ/Стивен Чарнок/manuscripts')
MANUSCRIPTS = (
    'INTRO_MIR_STEPHEN_CHARNOCK_WORKING_DRAFT.md',
    'I_CHELOVEK_KEMBRIDZH_DUBLIN_LONDON_WORKING_DRAFT.md',
    'II_UCHENYI_I_PROPOVEDNIK_WORKING_DRAFT.md',
    'III_CHARNOCK_AND_SCRIPTURE_FROM_TEXT_TO_SERMON_WORKING_DRAFT.md',
    'IV_BOGOSLOVSKII_PORTRET_WORKING_DRAFT.md',
    'V_KAK_PROPOVEDI_STALI_KNIGAMI_WORKING_DRAFT.md',
    'VI_GLAVNAYA_KNIGA_BYTIE_I_ATRIBUTY_WORKING_DRAFT.md',
    'VII_ZA_PREDELAMI_GLAVNOI_KNIGI_WORKING_DRAFT.md',
    'VIII_CHARNOCK_POSLE_CHARNOCKA_WORKING_DRAFT.md',
    'REFERENCE_KHRONOLOGIYA_TRUDY_ISTOCHNIKI_WORKING_DRAFT.md',
)
NOTE_DEF = re.compile(r'^\[\^([^\]]+)\]:', re.MULTILINE)
NOTE_REF = re.compile(r'\[\^([^\]]+)\](?!:)')
RELATIVE_LINK = re.compile(r'\]\((\.\./[^)]+)\)')
FLAGS = ('DRAFT', 'RESEARCH_ONLY', 'PUBLICATION_HOLD')
H2 = re.compile(r'^##[ \t]+(.+?)\s*$', re.MULTILINE)


def is_source_section(title):
    return title.startswith('Источниковые примечания') or title == 'Примечания к первичным и вторичным свидетелям'


def is_backstage_section(title):
    return title.startswith('Редакторская приёмка') or title.startswith('Редакторский контроль')



def audit(root=ROOT):
    root = Path(root).resolve()
    folder = root / MANUSCRIPT_DIR
    errors, targets = [], set()
    notes = 0
    for name in MANUSCRIPTS:
        path = folder / name
        if not path.is_file():
            errors.append(f'{name}: missing manuscript')
            continue
        body = path.read_text(encoding='utf-8')
        for flag in FLAGS:
            if flag not in body[:700]:
                errors.append(f'{name}: missing {flag} in front matter')
        headings = [(m.group(1).strip(), m.start()) for m in H2.finditer(body)]
        source = [offset for title, offset in headings if is_source_section(title)]
        backstage = [offset for title, offset in headings if is_backstage_section(title)]
        if len(source) != 1:
            errors.append(f'{name}: expected exactly one sources section (found {len(source)})')
        if len(backstage) != 1:
            errors.append(f'{name}: expected exactly one backstage section (found {len(backstage)})')
        if len(source) == len(backstage) == 1:
            if source[0] >= backstage[0]:
                errors.append(f'{name}: sources section must precede backstage')
            if not headings or headings[-1][1] != backstage[0]:
                errors.append(f'{name}: backstage must be the final H2 section')
            for note in NOTE_DEF.finditer(body):
                if not source[0] < note.start() < backstage[0]:
                    errors.append(f'{name}: footnote definition outside sources section [^{note.group(1)}]')
        definitions = NOTE_DEF.findall(body)
        references = NOTE_REF.findall(body)
        notes += len(definitions)
        defined, referenced = set(definitions), set(references)
        for key in sorted(defined):
            if definitions.count(key) > 1:
                errors.append(f'{name}: duplicate footnote [^{key}]')
        for key in sorted(referenced - defined):
            errors.append(f'{name}: undefined footnote [^{key}]')
        for key in sorted(defined - referenced):
            errors.append(f'{name}: unused footnote [^{key}]')
        # A reference in the sources/backstage section must not disguise a citation
        # lost from the reader-facing prose.
        if len(source) == 1:
            reader_references = set(NOTE_REF.findall(body[:source[0]]))
            for key in sorted(defined - reader_references):
                errors.append(f'{name}: footnote not cited by reader text [^{key}]')
        for link in RELATIVE_LINK.findall(body):
            resolved = (path.parent / unquote(link.split('#', 1)[0].strip())).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                errors.append(f'{name}: broken relative target {link}')
            else:
                targets.add(str(resolved.relative_to(root)))
    if errors:
        raise ValueError('\n'.join(errors))
    return {'manuscripts': len(MANUSCRIPTS), 'footnotes': notes,
            'internalTargets': len(targets),
            'limit': 'structure-only; not source review or approval'}


if __name__ == '__main__':
    try:
        print(audit())
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
