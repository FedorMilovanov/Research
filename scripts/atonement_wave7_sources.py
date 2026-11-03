#!/usr/bin/env python3
"""Read-only custody gate for Cyril John11:52 transmission DISCOVERY, not verification.

Default: retained digital-candidate/web-observation controls and actual Git preimages.
--source-root: verify all 11 Git objects and two ZIP members BEFORE parsing selected
contexts. No network, extraction to disk, source repair, print/manuscript collation,
Greek quote-safe promotion, doctrinal closure, or publication approval.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

from atonement_wave4_sources import git_blob

ROOT = Path(__file__).resolve().parents[1]
CONTROL = 'ИСКУПЛЕНИЕ/evidence/source_controls_wave7_2026-11-03.json'
REPORT = 'ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json'
BASELINE = '27eeb240196805f9ca08d3553a22b849560ba6a5'
REVIEW_KEY = 'greekTransmissionReviewWave7'
STATUS = 'CANDIDATE_GREEK_IDENTIFIED_PRINT_AND_ATTRIBUTION_OPEN'
O11 = 'DISCOVERY_AND_EDITORIAL_REVIEW_DONE_ORIGINAL_VERIFICATION_OPEN'
PINS = {
    'open-greek/open-greek-corpus': 'a152e69ef26c1b9f9da2218d303f36f5ba4ab5b9',
    'OpenGreekAndLatin/greek-dev': '0264701dbef6e02a49048c04109512c43f4eba5f',
    'JLCPutmans/Patrologia-Graeca-PG-txt-files': '16cafa1381e9fac54a54df2d8910fe75adfebdff',
}
FILE_PINS = {
    'OG-README': ('1a3b65cdd707d4b5cd09406ddefafa3e6a488b5e3ec94ffccf7986b99d21f9ff', 3162, '2ee93af722fcbd23c9ae20e2e94f5b6f27560a03'),
    'OG-LICENSE': ('a22ef97184528a0a113b5d21b478af69d32b75daf70885acc02e63bf806e4141', 1277, '8259e21ad92848217dcdfd4067d8a919765eb4a7'),
    'OG-JOHN': ('2b5ae4204ca5cb142375465ce41357719aad44bdb315fd08a12da4d208870613', 5420775, 'fb08ee551b2b44b58814f8a26b65f45b73159593'),
    'OG-CALFA-NOTE': ('7efd309e98bc2f416516bc1580241d6ab3447490625bfed0853d48587284b3c3', 888, 'a42634b4b924664b227e0d7af50a4f043352b196'),
    'OG-REOCR-META': ('5742bb15a1ed9ebeb22939dec614309e2529d9323d8caf68856a476a65eac674', 30885, '522a461209fa5761b3152d75bafbe93ccca34705'),
    'OG-GAP-REQUEST': ('d8fdf926338b676200402d896fed520f36b3036ef0fa7367c51edf6688f9087b', 1679, '37f6134979faa070bd602df905cb78e0f5f70317'),
    'OGL-README': ('fdb31ce7bc02bbc1fa22d5859e17f58d83e65305de0112b02c03e5df9e2ae2f9', 13372, 'f08793a54b04ec49c545c046f9deb04a52b1d612'),
    'OGL-INVENTORY': ('605be863adb6a2a70c4315fed65c24969fb6dbc64f4ded136f346be23b9e4e8a', 21470, 'b0c45cf8afa89ab48467255940419ae95691be09'),
    'OGL-SUBMODULES': ('9b96fab62be7cee1a3666917da915d7297c00f8f5842a0fe6b2ae59dc13d0ded', 17173, '1f2ec3e71149623193f3e3eb278ee337abb312f0'),
    'OG-REGISTRY': ('1f560628bafae42af6fa2b3a1b220d879db87b1078148090c6f73e2fe3b0d0e7', 9266800, '1bbe5bedb39dc508e3fe73aa844e844dfdd58ccf'),
    'PG-C-ZIP': ('79d98f70b6fe7d8dd1dee1221a08be5d3a9b1a8152ccb4b96493839e7a7d9a9c', 23866213, '5d77269c5cf1f2cb1510a935a7915dc60ba5cccc'),
    'AEGEAN-JOHN': ('d967a3e4f407c93360f58dcbfcc7c943a651a4550978a2bbc3795b1f7b293bc8', 4906768, None),
    'AEGEAN-ADDENDA': ('c4fe54eb3bd416cc8ddfd55ad1e2259332fe998931fb9cd5a5480e1ba205265a', 22197, None),
}
LOCUS_IDS = ['pg074_0038.5', 'pg074_0038.6', 'pg074_0039.1', 'pg074_0039.2', 'pg074_0039.3', 'pg074_0039.4']
CANDIDATES = {
    'OG-JN11': ('OG-JOHN', {'kind': 'jsonl_loci', 'loci': LOCUS_IDS}, '38db038e09966b56a442999f84f9c9afa0799508e1fa711f0eaa988a5f356811'),
    'AEGEAN-JN11': ('AEGEAN-JOHN', {'kind': 'text_lines', 'first': 24340, 'last': 24408}, '5c56545037b37f4d9f07dc7101d0d911898d8ad85ec10a63b0bfa06d2c700d2c'),
}
WEB = {
    'LIDDON-PREFACE': ('A1', 'cyril_on_john_00_intro2.htm', '35bba36dd9821d391deafee54cb50a9656d40a51373451c724fb7b60c78e5eb4'),
    'PEARSE-EDITORIAL': ('B1', 'cyril_on_john_00_eintro.htm', '0019af4f9008a72aeb4e1a4eda8d34a1b32406a6968bbaaaab2552df80b962e5'),
    'RANDELL-JN11': ('A1', 'cyril_on_john_07_book7.htm', '9e2175edbdac213b3c69420cc16f68b09367de9107355df8a6068729014ffa8c'),
}
COMPARISONS = {
    'NAMING': ('ὁνοματίζομεν', 'χρηματιζομεν'),
    'CREATION': ('τρώφῃ δημιουργικῇ', 'τροπωι δημιουργικωι'),
    'COVENANT-PARADISE': ('καὶ εὐτόνως τὴν ἀρετὴν ἐργάζομενοι', 'και της θειας ομολογιας\nηξιωμενοι, και της εν παραδεισωι διαιτης τε και τρυφης απολαυοντες'),
    'GATHERING': ('συνεισάγαγε δὲ πάλιν καὶ συνεκάθιμε', 'συνεισηγαγε δε παλιν και συνεκομισε'),
}
STATISTICS = dict(gitObjects=11, zipMembers=2, controlledArtifacts=13, greekCandidateContexts=2,
                  digitalComparisonPoints=4, renderedWebObservations=3, verifiedGreekOriginalPassages=0)
EDITION_COUNTS = {'calfa-pg73-5895ab908dd4': 520, 'migne-ocr-qwen36': 2578,
                  'migne-pg74-gap-consensus-2026-10': 3, 'reviewed-duplicate-block-consensus-2026-10': 4}
FALSE_BOUNDARIES = ('fullWorksRead', 'greekOriginalVerified', 'printedCollationClaimed', 'criticalAttributionSettled',
    'syriacTextRead', 'latinPraefatioDirectlyRead', 'quastenDirectlyRead', 'manuscriptsInspected',
    'digitalDiscrepanciesAreAncientVariants', 'twoDigitalFilesAreIndependentWitnesses', 'zeroSearchProvesAbsence',
    'corpusDefaultEditionAppliesToEveryRow', 'rawHtmlAcquired', 'publicationEligible', 'mergePerformed',
    'doctrinalClosure', 'englishCreationReadingErased', 'oldMissingPackagesReplayed', 'humanReadingMeasured')
REQUIRED_REPAIRS = {'W7-'+s for s in ('NT15','F05','F10','C25','P13','N00','F00','ROOT00',
                                    'ROOT-DATA','NT-DATA','F-DATA','S-DATA')}
REGISTRIES = ('data/atonement-corpus-v1.json', 'nt/data/nt-corpus-v1.json',
              'fathers/data/fathers-corpus-v1.json', 'synthesis/data/synthesis-corpus-v1.json')


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_layout() -> dict:
    og, ogl, pg = PINS
    rows = {i: (og, p) for i, p in (
        ('OG-README','README.md'), ('OG-LICENSE','LICENSE'),
        ('OG-JOHN','data/corpus/cyrillus-theology.commentarii-in-joannem.jsonl'),
        ('OG-CALFA-NOTE','data/reference/calfa-pg73/README.md'),
        ('OG-REOCR-META','data/inventory/reocr_provenance.json'),
        ('OG-GAP-REQUEST','data/ocr_requests/cyril-john-missing-pg74.json'),
        ('OG-REGISTRY','data/source_registry.json'))}
    rows.update({i: (ogl,p) for i,p in (('OGL-README','README.md'), ('OGL-INVENTORY','inventory.json'), ('OGL-SUBMODULES','.gitmodules'))})
    rows['PG-C-ZIP'] = (pg, 'PG-C.zip')
    return rows


def member_layout() -> dict:
    return {'AEGEAN-JOHN': 'CYRIL-ALEXANDRIEN/Commentarii in Joannem.pdf.txt',
            'AEGEAN-ADDENDA': 'CYRIL-ALEXANDRIEN/Commentarii in Joannem Additamenta.pdf.txt'}


def extract_candidate(raw: bytes, selector: dict) -> dict:
    """Literal digital extraction. No accent restoration, emendation or OCR repair."""
    if selector['kind'] == 'text_lines':
        lines = raw.decode().splitlines()
        if not 1 <= selector['first'] <= selector['last'] <= len(lines):
            raise ValueError('candidate line bounds')
        return {'text': '\n'.join(lines[selector['first']-1:selector['last']])}
    if selector['kind'] != 'jsonl_loci':
        raise ValueError('unknown candidate selector')
    rows = [json.loads(line) for line in raw.decode().splitlines()]
    selected = []
    for loc in selector['loci']:
        matches = [(i+1, r) for i,r in enumerate(rows) if r.get('locus') == loc]
        if len(matches) != 1:
            raise ValueError('missing/duplicate digital locus ' + loc)
        line, row = matches[0]
        selected.append(dict(line=line, **row))
    return dict(rows=selected, text='\n'.join(r['text'] for r in selected))


def check_controls(root: Path, report: dict, control: dict) -> list[str]:
    errors = []
    wave = report.get('wave7', {})
    if (wave.get('controls'), wave.get('baselineCommit'), wave.get('publicationEligible'), wave.get('mergePerformed')) != (CONTROL, BASELINE, False, False):
        errors.append('wave7: journal identity/nonpublication boundary')
    if (control.get('baselineCommit'), control.get('status'), control.get('c25'), control.get('o11')) != (BASELINE, STATUS, 'OPEN', O11):
        errors.append('wave7: discovery cannot become original-language/claim closure')
    for key in FALSE_BOUNDARIES:
        if control.get(key) is not False:
            errors.append('wave7: missing/overclaimed boundary ' + key)
    if control.get('interpretationStatus') != 'ARGUED_PROVISIONAL_NOT_MACHINE_PROOF':
        errors.append('wave7: interpretation is not a machine proof')
    if control.get('statistics') != STATISTICS:
        errors.append('wave7: artifact/scope statistics drift')
    policy = json.loads((root/'data/repository-evidence-policy-v2.json').read_text())
    axes = {'evidenceClass':'sourceClasses', 'accessState':'accessStates', 'locatorState':'locatorStates',
            'rightsState':'rightsStates', 'publicationState':'publicationStates'}
    def states(row, label):
        for key, vocabulary in axes.items():
            if row.get(key) not in policy[vocabulary]:
                errors.append('wave7: noncanonical axis '+label+'/'+key)
        if row.get('publicationEligible') is not False or row.get('publicationState') != 'BLOCKED' or 'PUBLICATION_HOLD' not in row.get('holds', []):
            errors.append('wave7: publication promotion '+label)
    files = control.get('files', [])
    if len(files) != len(FILE_PINS) or {f['id'] for f in files} != set(FILE_PINS):
        errors.append('wave7: artifact inventory missing/duplicate')
    layout, members = file_layout(), member_layout()
    for f in files:
        ident = f['id']; states(f, ident)
        if (f.get('sha256'), f.get('bytes'), f.get('gitBlob')) != FILE_PINS.get(ident):
            errors.append('wave7: artifact byte pin '+ident)
        if f.get('evidenceClass') != 'C' or f.get('quoteSafe') is not False or f.get('accessState') != 'FULL_OBJECT_VERIFIED' or f.get('locatorState') != 'EXACT_LOCATOR_VERIFIED' or not f.get('classScope') or not f.get('locatorScope'):
            errors.append('wave7: discovery artifact class/access/quote scope '+ident)
        if ident in layout:
            repo, path = layout[ident]
            if (f.get('kind'), f.get('repo'), f.get('commit'), f.get('path'), f.get('externalRelativePath')) != (
                    'git_blob', repo, PINS[repo], path, repo.replace('/','--')+'/'+path):
                errors.append('wave7: artifact identity/path '+ident)
        elif ident in members:
            relative = 'JLCPutmans--Patrologia-Graeca-PG-txt-files/extracted/'+members[ident]
            if (f.get('kind'), f.get('containerId'), f.get('member'), f.get('externalRelativePath')) != ('zip_member','PG-C-ZIP',members[ident],relative) or 'gitBlob' in f:
                errors.append('wave7: ZIP member is not a separate Git blob '+ident)
        wanted_rights = 'RIGHTS_UNKNOWN' if ident in members or ident == 'PG-C-ZIP' else 'STORAGE_ONLY'
        if f.get('rightsState') != wanted_rights:
            errors.append('wave7: artifact rights scope '+ident)
    candidates = control.get('candidates', [])
    texts = {c['id']: c.get('text','') for c in candidates}
    if len(candidates) != 2 or set(texts) != set(CANDIDATES):
        errors.append('wave7: candidate inventory missing/duplicate')
    for c in candidates:
        ident = c['id']; states(c, ident)
        if (c.get('sourceFile'), c.get('selector'), c.get('textSha256')) != CANDIDATES.get(ident) or digest(c.get('text','').encode()) != c.get('textSha256'):
            errors.append('wave7: literal candidate text/selector pin '+ident)
        if (c.get('evidenceClass'), c.get('quoteSafe'), c.get('selectedDigitalContextRead'), c.get('authorialContextVerified'), c.get('originalLanguageVerified'), c.get('printedCollationClaimed'), c.get('fullWorkRead')) != ('C', False, True, False, False, False, False):
            errors.append('wave7: candidate cannot be VERIFIED_ORIGINAL '+ident)
        if (c.get('accessState'), c.get('locatorState'), c.get('rightsState')) != ('FULL_OBJECT_VERIFIED', 'EXACT_LOCATOR_VERIFIED', 'RIGHTS_UNKNOWN' if ident=='AEGEAN-JN11' else 'STORAGE_ONLY') or 'EVIDENCE_HOLD' not in c.get('holds', []):
            errors.append('wave7: candidate digital-only axes/holds '+ident)
        if not c.get('version') or not c.get('provenance') or not c.get('locator'):
            errors.append('wave7: candidate provenance/scope missing '+ident)
        if ident == 'OG-JN11':
            rows = c.get('rows', [])
            if ([r.get('line') for r in rows] != list(range(673,679)) or [r.get('locus') for r in rows] != LOCUS_IDS or
                    any(r.get('edition') != 'migne-ocr-qwen36' or r.get('source') != 'ocr' for r in rows) or
                    '\n'.join(r.get('text','') for r in rows) != c.get('text')):
                errors.append('wave7: selected OCR rows are not default Calfa/Pusey text')
    comparisons = control.get('digitalComparisons', [])
    if len(comparisons) != 4 or {p['id'] for p in comparisons} != set(COMPARISONS):
        errors.append('wave7: digital comparison inventory')
    for p in comparisons:
        if (p.get('left'), p.get('right')) != COMPARISONS.get(p['id']) or (p.get('leftCandidate'), p.get('rightCandidate')) != ('OG-JN11','AEGEAN-JN11') or not p.get('purpose'):
            errors.append('wave7: literal comparison binding '+p['id'])
        for side in ('left','right'):
            if not p.get(side) or p.get(side) not in texts.get(p.get(side+'Candidate'), ''):
                errors.append('wave7: comparison not in candidate '+p['id'])
        for key in ('authorialVariantEstablished','ocrCauseEstablished','silentlyEmended'):
            if p.get(key) is not False:
                errors.append('wave7: comparison cause/emendation overclaim '+p['id']+'/'+key)
    web = control.get('webObservations', [])
    if len(web) != 3 or {w['id'] for w in web} != set(WEB):
        errors.append('wave7: web observation inventory')
    for w in web:
        ident = w['id']; states(w, ident)
        expected = WEB.get(ident)
        if not expected or (w.get('evidenceClass'), w.get('url'), w.get('selectedExcerptSha256')) != (expected[0], 'https://www.ccel.org/ccel/pearse/morefathers/files/'+expected[1], expected[2]) or digest('\n'.join(w.get('passages',[])).encode()) != w.get('selectedExcerptSha256'):
            errors.append('wave7: selected web excerpt/class pin '+ident)
        if (w.get('accessState'), w.get('rawHtmlAcquired'), w.get('rawHtmlSha256'), w.get('acquisitionKind')) != ('PARTIAL_OBJECT', False, None, 'RENDERED_WEB_OBSERVATION_NOT_RAW_HTML'):
            errors.append('wave7: rendered observation is not raw HTML '+ident)
        if w.get('quoteSafe') is not (ident != 'PEARSE-EDITORIAL') or w.get('rightsState') != 'STORAGE_ONLY' or w.get('contextVerified') is not True or w.get('printedCollationClaimed') is not False or not w.get('evidenceScope') or not w.get('locator') or not w.get('version'):
            errors.append('wave7: editor/translation/primary scope '+ident)
    cat = control.get('catalogue', {})
    if (cat.get('sourceFile'), cat.get('ctsAlias'), cat.get('defaultEdition'), cat.get('puseyReference',{}).get('servable'), cat.get('puseyReference',{}).get('provider')) != (
            'OG-REGISTRY','urn:cts:greekLit:tlg4090.tlg002','cyrillus-theology.commentarii-in-joannem.calfa-pg73-5895ab908dd4',False,'tlg-e-reference'):
        errors.append('wave7: catalogue metadata is not acquired Pusey text')
    for key in ('upstreamPdfChecksumsVerifiedHere','upstreamCalfaChecksumVerifiedHere','catalogueIsAcquiredPuseyText'):
        if cat.get(key) is not False:
            errors.append('wave7: borrowed upstream verification '+key)
    composition = control.get('corpusComposition', {})
    if composition.get('rows') != 3105 or composition.get('editionCounts') != EDITION_COUNTS:
        errors.append('wave7: mixed OCR composition is not independent witness count')
    basis = control.get('substantiveBasis', {})
    if (basis.get('control'), basis.get('observationId'), basis.get('freshEnglishObservation')) != (
            'ИСКУПЛЕНИЕ/evidence/source_controls_wave5_2026-11-03.json','CYRIL-JN11-52','RANDELL-JN11'):
        errors.append('wave7: retained English primary basis missing')
    requests = control.get('nextAcquisition', [])
    if len(requests) != 4 or {r['id'] for r in requests} != {'PRINT-EN','PRINT-PUSEY','PRINT-MIGNE','TRANSMISSION'} or any(not r.get('target') or not r.get('acceptance') for r in requests):
        errors.append('wave7: owned acquisition/acceptance queue missing')
    repairs = {r['id']:r for r in report['repairs'] if r['id'].startswith('W7-')}
    if set(repairs) != REQUIRED_REPAIRS or set(wave.get('repairIds', [])) != REQUIRED_REPAIRS:
        errors.append('wave7: repair coverage')
    snaps = wave.get('supersededSnapshots', [])
    if len({s['path'] for s in snaps}) != len(snaps) or not {r['file'] for r in repairs.values()} <= {s['path'] for s in snaps}:
        errors.append('wave7: actual preimage coverage')
    baseline = {}
    for s in snaps:
        if s.get('commit') != BASELINE:
            errors.append('wave7: preimage baseline'); continue
        p = subprocess.run(['git','show',f"{BASELINE}:{s['path']}"],cwd=root,capture_output=True)
        if p.returncode or (len(p.stdout), digest(p.stdout), git_blob(p.stdout)) != (s.get('bytes'), s.get('sha256'), s.get('blob')):
            errors.append('wave7: actual Git preimage mismatch '+s['path'])
        else:
            baseline[s['path']] = p.stdout.decode()
    for r in repairs.values():
        present = r['removed'] in baseline.get(r['file'], '')
        kind = 'BASELINE_REMOVAL_OR_EXPLICIT_SUPERSESSION' if present else 'ADDITIVE_GUARD_NOT_A_HISTORICAL_QUOTE'
        if r.get('rejectedWordingPresentInBaseline') is not present or r.get('controlType') != kind:
            errors.append('wave7: invented historical error '+r['id'])
        if r['required'] not in (root/r['file']).read_text():
            errors.append('wave7: owner update missing '+r['id'])
    for path in REGISTRIES:
        review = json.loads((root/'ИСКУПЛЕНИЕ'/path).read_text()).get(REVIEW_KEY, {})
        if (review.get('controls'), review.get('status'), review.get('c25'), review.get('o11'), review.get('greekOriginalVerified'), review.get('publicationEligible')) != (CONTROL, STATUS, 'OPEN', O11, False, False):
            errors.append('wave7: registry discovery/closure boundary '+path)
        if review.get('candidateIds') != list(CANDIDATES) or review.get('candidateEvidenceClass') != 'C' or review.get('greekCandidatesQuoteSafe') is not False:
            errors.append('wave7: registry candidate promotion '+path)
    ledger = (root/'ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md').read_text()
    c25 = re.search(r'(?ms)^## C-25\b.*?(?=^## |\Z)', ledger)
    if not c25 or not re.search(r'\*\*Статус:\*\*\s*`OPEN`', c25.group()):
        errors.append('wave7: C25 owner status is not OPEN')
    return errors


def verify_sources(source_root: Path, control: dict) -> list[str]:
    """Full byte gate first; never parse any context from a failed object set."""
    errors, raws = [], {}
    base = source_root.resolve()
    for f in control['files']:
        path = (base/f['externalRelativePath']).resolve()
        if not path.is_relative_to(base):
            errors.append('wave7 replay: unsafe path '+f['id']); continue
        try:
            raw = path.read_bytes()
        except OSError as exc:
            errors.append('wave7 replay: missing object '+f['id']+': '+str(exc)); continue
        expected = FILE_PINS.get(f['id'])
        actual = (digest(raw), len(raw), git_blob(raw) if f['kind']=='git_blob' else None)
        if actual != expected or actual != (f.get('sha256'),f.get('bytes'),f.get('gitBlob')):
            errors.append('wave7 replay: artifact bytes changed '+f['id']); continue
        raws[f['id']] = raw
    if errors:
        return errors
    try:
        with zipfile.ZipFile(io.BytesIO(raws['PG-C-ZIP'])) as z:
            for ident, member in member_layout().items():
                if z.namelist().count(member) != 1 or z.read(member) != raws[ident]:
                    errors.append('wave7 replay: ZIP/member provenance '+ident)
        for c in control['candidates']:
            extracted = extract_candidate(raws[c['sourceFile']], c['selector'])
            if any(c.get(k) != v for k,v in extracted.items()) or digest(extracted['text'].encode()) != c['textSha256']:
                errors.append('wave7 replay: candidate extraction differs '+c['id'])
        rows = [json.loads(l) for l in raws['OG-JOHN'].decode().splitlines()]
        if len(rows) != 3105 or dict(Counter(r['edition'] for r in rows)) != EDITION_COUNTS:
            errors.append('wave7 replay: corpus composition')
        work = json.loads(raws['OG-REGISTRY'])['works']['cyrillus-theology.commentarii-in-joannem']
        cat = control['catalogue']
        for key, actual in {'ctsAlias':work['aliases']['cts'], 'defaultEdition':work['default_edition'],
                'puseyReference':work['editions']['cyrillus-theology.commentarii-in-joannem.pusey-1872'],
                'sourceEditionClaims':work['coverage_composition']['source_editions'],
                'qualification':work['coverage_composition']['qualification']}.items():
            if cat.get(key) != actual:
                errors.append('wave7 replay: catalogue differs '+key)
    except (ValueError, KeyError, UnicodeError, zipfile.BadZipFile) as exc:
        errors.append('wave7 replay: invalid source structure '+str(exc))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--source-root', type=Path)
    args = ap.parse_args()
    try:
        control = json.loads((args.root/CONTROL).read_text())
        report = json.loads((args.root/REPORT).read_text())
        errors = check_controls(args.root, report, control)
        replay = verify_sources(args.source_root, control) if args.source_root else []
        errors += replay
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('WAVE7 SOURCES: FAIL —', exc)
        return 1
    print(json.dumps(dict(control['statistics'], sourceByteReplay=('FAIL' if replay else 'PASS') if args.source_root else 'NOT_RUN',
        rawHtmlReplay='NOT_AVAILABLE_RENDERED_OBSERVATIONS_ONLY', greekOriginalVerified=False,
        printedCollationClaimed=False, humanReadingMeasured=False, publicationApproved=False)))
    for error in errors:
        print('FAIL:', error)
    print('WAVE7 SOURCES: '+('FAIL' if errors else 'PASS — discovery only; Greek original unverified; C25 OPEN'))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
