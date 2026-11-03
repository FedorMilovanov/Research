#!/usr/bin/env python3
"""Read-only custody gate for Wave 8 Cyril John 11:49-52 edition, apparatus, and medium controls.

Default: retained primary-scan / OCR-witness / web-observation controls and actual Git preimages.
--source-root: verify all 32 external Git-blob objects (including 8 printed JPEG scans of Pusey
1872 Vol. I and 24 OCR/hOCR/XML/JSON witnesses across Pusey Vol. II-III, Migne PG 74, and
open-greek) BEFORE checking literal structural/apparatus invariants. No network, file writes,
silent OCR repair, Greek quote-safe promotion for Vol. II/PG 74, doctrinal closure, or
publication approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from atonement_wave4_sources import git_blob

ROOT = Path(__file__).resolve().parents[1]
CONTROL = 'ИСКУПЛЕНИЕ/evidence/source_controls_wave8_2026-11-03.json'
REPORT = 'ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json'
BASELINE = '10f39af4ec2633f6304790cef346627a3fb5a62c'
REVIEW_KEY = 'greekEditionAndApparatusReviewWave8'
STATUS = 'PUSEY_VOL1_SCAN_VERIFIED_VOL2_AND_PG74_OCR_COLLATED_PRINT_SCAN_FOR_1152_OPEN'
O11 = 'EDITION_LOCATOR_APPARATUS_AND_MEDIUM_ESTABLISHED_1152_PRINT_IMAGE_OPEN'

OGL_V1 = 'OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev'
OGL_BOOK = '2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book'
LATIN_V2 = 'latin-ocr/operacyrilli04cyriuoft'
LATIN_V3 = 'latin-ocr/operacyrilli05cyriuoft'
FABIO = 'Fabio3rs/BibliothecaPatristica'
OPEN_GREEK = 'open-greek/open-greek-corpus'

PINS = {
    OGL_V1: '9f4df68bb5fdb07b996b36b1a4b532680eb6aec2',
    LATIN_V2: 'fc594d8f43ef141af4e93a0fcc424063a378eacf',
    LATIN_V3: '831c045235ad912f69ecf9f3bb4d164e43378560',
    FABIO: '84f81c0138bffe9e9a7a836b8e1551007ae946cf',
    OPEN_GREEK: 'a152e69ef26c1b9f9da2218d303f36f5ba4ab5b9',
}

FILE_PINS = {
    'PUSEY-V1-INVENTORY': ('63f167e228a57f8fcd42922720ebdd853533ebbaef57e5e2cc5ee223d4c4134e', 1541580, '511b56e96d02b279eb95e66804c6155070279caf'),
    'PUSEY-V1-COLOPHON-JPG': ('195d23bface7cb9fdeca06f175eabc61f0631f06691c49a0c3722b37e0b53a1a', 43885, '460d8ac9891edde954edeaefd6d86efe70413078'),
    'PUSEY-V1-TITLE-JPG': ('d8fda9072fe8c2eab5149391e93e7f4ca0dd6fd6bb91af4a007ef6a938c630a1', 85938, '39a50394d2ef8b446577b1d31956000524af5016'),
    'PUSEY-V1-PRAEF-VII-JPG': ('6e205561134e0c5275dbaa2da0d9a9f28d7eb758de1f28cbab5f6e1a1ceb1fec', 244120, 'bff8a198d0870c713ae71c3df725025129e05fcf'),
    'PUSEY-V1-PRAEF-VIII-JPG': ('e9d69e7c2dcc423696653007ceb829958914698c4be50a5486394f5c9c14c2c6', 280882, 'ec47247ac29f881526018271a3402fe6c75c4014'),
    'PUSEY-V1-PRAEF-IX-JPG': ('655fcbbff34dc4bc058c58a71be0a267987e5ac363c0fc63322bbe4fa3877367', 318334, '64af78b1aa8748c801f3eafb7a949bcd19a7ea14'),
    'PUSEY-V1-PRAEF-X-JPG': ('dc1a62ec8c32c7db0d1fdec14f97e8be0103c2e96de16bbd4f2cbfa9a4aa4580', 91280, '2c93fc8eefc33f586b536f39ef340e788a3addbf'),
    'PUSEY-V1-ERRATUM-JPG': ('8a1490eff04508e596b8bede263b0b0f06a3b6c978c401014c42b141d62f1cff', 175918, 'fe50ab267a90665b46c9990126956cbd03d2729d'),
    'PUSEY-V1-CAPITA-JPG': ('5c9a851c832372a690fbaff6b689786e977f601f0e021a65d3da90537decf24e', 341306, 'bc2a3316e7f95e332a3ca75520b3f094500b8758'),
    'PUSEY-V2-TITLE-TXT': ('e2ebba2ecbf03294af676628a009029c80cc83b47ed12965ba9276ded0e686c7', 545, 'bb0b8e9cc7a6d4b63558ad6dc9002dbf5f858c71'),
    'PUSEY-V2-LIB7-OPEN-TXT': ('993c59d3f64f59400b95bfce14d45f560cbe90e692003522924d3307e404879c', 2443, '7a40d7f9d7baedac24f86086abb660f3948c19ff'),
    'PUSEY-V2-P292-TXT': ('657d722a4ddb89a4fb268e7f184a0350b933a0bb9031afcf50859ec393020bbc', 4233, '7071f73758f88501c62dfaec507796a18ac5cbb0'),
    'PUSEY-V2-P293-TXT': ('de7edfc3de31c020a71aa6b6e1c38e41f5f356b10a1a19255a28cf96d6f49ce5', 3543, '6950f11b7c1070b79354da1e82c061be0bf7e0b7'),
    'PUSEY-V2-P294-TXT': ('f3ea76f41a28642e11e3e66a1584af3bbd00cdaab4b0e81cdd6985f52e0f4c11', 3614, 'a6e16d36973d29f9ef1763a7021e5eed0a1f0dbc'),
    'PUSEY-V2-P294-HOCR': ('bc1bc298aa85be1afeeded0c19c08fe2e53cff5ececd7ae460c5e423e157be56', 46037, '476a228b1e74199709a594288d7dcdd2bd8b19d1'),
    'PUSEY-V2-P295-TXT': ('004a7ef7181b01e19e83cf50403231f8ab72df72a36c1c72af79ed1daf7ae2ab', 4545, '7e5c63efb62479d9937ee09999eabbe8c69a6ad2'),
    'PUSEY-V2-P295-HOCR': ('93ba51c5f6bf5031f6ad822a6bb95d783092cf3f9ad511f0d26eaf8928a008c2', 59844, 'ff9597a84cf58facce5bf2702007dac11aba08c7'),
    'PUSEY-V2-P296-TXT': ('1c18e424a6febd92f20b9f790f1e9c8a338c408523e620fa10f2041521df39fb', 3905, '3fc58dc9d190656f67e7f74633c314874ad4f9f8'),
    'PUSEY-V2-P296-HOCR': ('78ebf5cffea3eb010c3a7f5e7a6241715aa9c4c36f6c96ad701a514afa63f310', 48156, 'f3369b6f2b11a1c64ec82c98c38a9cca89e69d94'),
    'PUSEY-V2-LIB7-END-TXT': ('cf3f74e9c8ece94db162f51e444932a9c56a65ed6795588c3073ffb28069c3e6', 775, '0b1be93beee342faa90d05669ee5c5ae95508c79'),
    'PUSEY-V2-LIB8-SYR-TXT': ('23db331e3c467ca54e9f1e276e25a986c6366162115afec38dde180877169fc2', 2600, 'f8f072c942c467bd9a7aa000582128849724268d'),
    'PUSEY-V3-CONSPECTUS-TXT': ('0d5d9f78f0886da93a7ec2994cd669bb2de53206fffaef59db97102d85133695', 1756, '66150a5f0fe34924c0482d2b8a1045868ebdf02d'),
    'PUSEY-V3-APPSYR-TITLE-TXT': ('75de9440e6f70d8f98f948bdb5ccf0043fc46d1b371b20e202780eb2cbcb38aa', 1523, 'c9f9484817f5cffd580e5b44358f2100726232fb'),
    'FABIO-LICENSE-NOTICE': ('b8c0989bf8c34d03113119bc66dd12b8ce53b32396f4e5cbb5414c8213de704a', 561, '654eb9cb9e3b512b213b757c52c5830febb9d4b8'),
    'FABIO-PG74-007': ('1b2935916cf962d0e54ae855696dc898a80be81f01d91dc9c9143ac816b56c50', 2863, '2a67647ee5ca47f96b7ab37930402a2fa42dce25'),
    'FABIO-PG74-038': ('81e7195de35132933659e7e822a6252e60d00bb2511dc2b52b871126be9605ed', 6985, 'cdc45dca087ea9575827c889a6fa0fa1863cce5f'),
    'FABIO-PG74-039': ('decf1cdeb0a8af4287222d435ca75c6edaabf1de6760a42f38b60b37c8d72339', 8875, 'acd883be8b5b885d0c6febd79e5c4a30f2c78448'),
    'FABIO-PG74-040': ('05be64e14b3f9b313329b346c68e39e93a6385b21e70676deb6899800b01551f', 8522, '7b0575f7980a3c5a12f723ef3d1a203748d5ed32'),
    'OG-COVERAGE-CHANGES': ('fe9d484c8189eda8f5c17035a1709c29402d13bc69caca58486235b3b2cd8e8f', 1384231, '57e3a5b1b543e8f7b581fb091f64ea0ebb809da3'),
    'OG-MISSING-PG74-REQ': ('d8fdf926338b676200402d896fed520f36b3036ef0fa7367c51edf6688f9087b', 1679, '37f6134979faa070bd602df905cb78e0f5f70317'),
    'OG-QWEN36-EVAL': ('ddfc4c33d5c53322190b39051b5c276b85027169de9ad5d8011f7f113ac0f077', 19552, 'a55ba44d9ef28bd0c47175d8a270bcd4f29950cd'),
    'OG-PG74-TITLE': ('da767053794b8afae25150a10ad8f2bab49248a0cbe4d2f0a0ee1731bb90c6e7', 1248, '121381fcd8fa0fcf1d8e7ca27fe22301c6c11233'),
}

A1_SCAN_IDS = {
    'PUSEY-V1-COLOPHON-JPG',
    'PUSEY-V1-TITLE-JPG',
    'PUSEY-V1-PRAEF-VII-JPG',
    'PUSEY-V1-PRAEF-VIII-JPG',
    'PUSEY-V1-PRAEF-IX-JPG',
    'PUSEY-V1-PRAEF-X-JPG',
    'PUSEY-V1-ERRATUM-JPG',
    'PUSEY-V1-CAPITA-JPG',
}

WEB_IDS = {
    'HT-RANDELL-V2-P133',
    'HT-RANDELL-V2-P134',
    'HT-RANDELL-V2-P164-SYR',
    'IA-PG74-1859-P41-KAIAFAS',
    'IA-PG74-1859-P41-FN1',
}

DISCREPANCY_IDS = {'DISC-1', 'DISC-2', 'DISC-3', 'DISC-4A', 'DISC-4B'}

STATISTICS = dict(
    gitObjects=32,
    visuallyInspectedA1PrintScans=8,
    classCOcrAndMetadataObjects=24,
    controlledArtifacts=32,
    discrepancyResolutions=5,
    renderedWebObservations=5,
    verifiedGreekOriginalPassagesFor1152=0,
)

FALSE_BOUNDARIES = (
    'fullWorksRead',
    'greekOriginalVerified',
    'puseyVol2PageImagesInspected',
    'mignePg74PageImagesInspected',
    'randellPageImagesInspected',
    'syriacInvolvedInJohn1149_52',
    'continuousGreekManuscriptForBook7Survives',
    'pusey691aDisclaimerTargetsJohn1149_52',
    'qwen36CorruptionsAreMigneReadings',
    'manuscriptsInspected',
    'rawHtmlAcquired',
    'publicationEligible',
    'mergePerformed',
    'doctrinalClosure',
    'englishCreationReadingErased',
    'humanReadingMeasured',
)

REQUIRED_REPAIRS = {
    'W8-' + s for s in (
        'NT15', 'F05', 'F10', 'C25', 'P13', 'N00', 'F00', 'ROOT00',
        'ROOT-DATA', 'NT-DATA', 'F-DATA', 'S-DATA',
    )
}

REGISTRIES = (
    'data/atonement-corpus-v1.json',
    'nt/data/nt-corpus-v1.json',
    'fathers/data/fathers-corpus-v1.json',
    'synthesis/data/synthesis-corpus-v1.json',
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_layout() -> dict[str, tuple[str, str, str]]:
    """Map artifact id -> (repo, upstream_path, external_relative_path)."""
    rows: dict[str, tuple[str, str, str]] = {}
    for aid, fname in (
        ('PUSEY-V1-INVENTORY', 'inventory.json'),
        ('PUSEY-V1-COLOPHON-JPG', 'i0008.jpg'),
        ('PUSEY-V1-TITLE-JPG', 'i0009.jpg'),
        ('PUSEY-V1-PRAEF-VII-JPG', 'i0013.jpg'),
        ('PUSEY-V1-PRAEF-VIII-JPG', 'i0014.jpg'),
        ('PUSEY-V1-PRAEF-IX-JPG', 'i0015.jpg'),
        ('PUSEY-V1-PRAEF-X-JPG', 'i0016.jpg'),
        ('PUSEY-V1-ERRATUM-JPG', 'i0021.jpg'),
        ('PUSEY-V1-CAPITA-JPG', 'i0028.jpg'),
    ):
        rows[aid] = (OGL_V1, f'{OGL_BOOK}/{fname}', f'OpenGreekAndLatin--operacyrilli03cyriuoft/{fname}')
    for aid, fname in (
        ('PUSEY-V2-TITLE-TXT', 'operacyrilli04cyriuoft_0007.txt'),
        ('PUSEY-V2-LIB7-OPEN-TXT', 'operacyrilli04cyriuoft_0255.txt'),
        ('PUSEY-V2-P292-TXT', 'operacyrilli04cyriuoft_0304.txt'),
        ('PUSEY-V2-P293-TXT', 'operacyrilli04cyriuoft_0305.txt'),
        ('PUSEY-V2-P294-TXT', 'operacyrilli04cyriuoft_0306.txt'),
        ('PUSEY-V2-P294-HOCR', 'operacyrilli04cyriuoft_0306.hocr'),
        ('PUSEY-V2-P295-TXT', 'operacyrilli04cyriuoft_0307.txt'),
        ('PUSEY-V2-P295-HOCR', 'operacyrilli04cyriuoft_0307.hocr'),
        ('PUSEY-V2-P296-TXT', 'operacyrilli04cyriuoft_0308.txt'),
        ('PUSEY-V2-P296-HOCR', 'operacyrilli04cyriuoft_0308.hocr'),
        ('PUSEY-V2-LIB7-END-TXT', 'operacyrilli04cyriuoft_0311.txt'),
        ('PUSEY-V2-LIB8-SYR-TXT', 'operacyrilli04cyriuoft_0344.txt'),
    ):
        rows[aid] = (LATIN_V2, fname, f'latin-ocr--operacyrilli04cyriuoft/{fname}')
    for aid, fname in (
        ('PUSEY-V3-CONSPECTUS-TXT', 'operacyrilli05cyriuoft_0009.txt'),
        ('PUSEY-V3-APPSYR-TITLE-TXT', 'operacyrilli05cyriuoft_0623.txt'),
    ):
        rows[aid] = (LATIN_V3, fname, f'latin-ocr--operacyrilli05cyriuoft/{fname}')
    rows['FABIO-LICENSE-NOTICE'] = (
        FABIO, 'LICENSE-NOTICE.md', 'Fabio3rs--BibliothecaPatristica/LICENSE-NOTICE.md'
    )
    for leaf in ('007', '038', '039', '040'):
        up = f'teste/PG074/text/b615395e-52c5-401c-849b-8287a03d8853-{leaf}.txt'
        rows[f'FABIO-PG74-{leaf}'] = (FABIO, up, f'Fabio3rs--BibliothecaPatristica/{up}')
    for aid, up in (
        ('OG-COVERAGE-CHANGES', 'data/corpus_changes/cyril-john-coverage/changes.json'),
        ('OG-MISSING-PG74-REQ', 'data/ocr_requests/cyril-john-missing-pg74.json'),
        ('OG-QWEN36-EVAL', 'data/evaluation/ocr-fresh/cyril-pg74-qwen36.jsonl'),
        ('OG-PG74-TITLE', 'data/paratext/cyril-pg74-title.jsonl'),
    ):
        rows[aid] = (OPEN_GREEK, up, f'open-greek--open-greek-corpus/{up}')
    return rows


def check_controls(root: Path, report: dict, control: dict) -> list[str]:
    errors: list[str] = []
    wave = report.get('wave8', {})
    if (wave.get('controls'), wave.get('baselineCommit'), wave.get('publicationEligible'), wave.get('mergePerformed')) != (
        CONTROL, BASELINE, False, False
    ):
        errors.append('wave8: journal identity/nonpublication boundary')
    if (control.get('baselineCommit'), control.get('status'), control.get('c25'), control.get('o11')) != (
        BASELINE, STATUS, 'OPEN', O11
    ):
        errors.append('wave8: edition/apparatus resolution cannot become C25/original closure')
    for key in FALSE_BOUNDARIES:
        if control.get(key) is not False:
            errors.append('wave8: missing/overclaimed boundary ' + key)
    if control.get('statistics') != STATISTICS:
        errors.append('wave8: artifact/scope statistics drift')

    policy = json.loads((root / 'data/repository-evidence-policy-v2.json').read_text(encoding='utf-8'))
    axes = {
        'evidenceClass': 'sourceClasses',
        'accessState': 'accessStates',
        'locatorState': 'locatorStates',
        'rightsState': 'rightsStates',
        'publicationState': 'publicationStates',
    }

    def states(row: dict, label: str) -> None:
        for key, vocabulary in axes.items():
            if row.get(key) not in policy[vocabulary]:
                errors.append(f'wave8: noncanonical axis {label}/{key}')
        for h in row.get('holds', []):
            if h not in policy['holds']:
                errors.append(f'wave8: noncanonical hold {label}/{h}')
        if row.get('publicationEligible') is not False or row.get('publicationState') != 'BLOCKED' or 'PUBLICATION_HOLD' not in row.get('holds', []):
            errors.append('wave8: publication promotion ' + label)

    files = control.get('files', [])
    if len(files) != len(FILE_PINS) or {f.get('id') for f in files} != set(FILE_PINS):
        errors.append('wave8: artifact inventory missing/duplicate')
    layout = file_layout()
    for f in files:
        ident = f.get('id', '')
        states(f, ident)
        if (f.get('sha256'), f.get('bytes'), f.get('gitBlob')) != FILE_PINS.get(ident):
            errors.append('wave8: artifact byte pin ' + ident)
        repo, upath, ext = layout.get(ident, ('', '', ''))
        if (f.get('kind'), f.get('repo'), f.get('commit'), f.get('path'), f.get('externalRelativePath')) != (
            'git_blob', repo, PINS.get(repo), upath, ext
        ):
            errors.append('wave8: artifact identity/path ' + ident)
        if f.get('originalLanguageVerifiedFor1152') is not False:
            errors.append('wave8: 11:52 Greek original cannot be marked verified ' + ident)
        if ident in A1_SCAN_IDS:
            if (
                f.get('evidenceClass') != 'A1'
                or f.get('visualScanInspected') is not True
                or f.get('quoteSafe') is not True
                or f.get('accessState') != 'FULL_OBJECT_VERIFIED'
                or f.get('locatorState') != 'EXACT_LOCATOR_VERIFIED'
                or not str(f.get('path', '')).endswith('.jpg')
            ):
                errors.append('wave8: A1 Vol. I scan contract ' + ident)
        else:
            if (
                f.get('evidenceClass') != 'C'
                or f.get('visualScanInspected') is not False
                or f.get('quoteSafe') is not False
                or f.get('accessState') != 'FULL_OBJECT_VERIFIED'
                or 'EVIDENCE_HOLD' not in f.get('holds', [])
            ):
                errors.append('wave8: class C OCR/metadata contract ' + ident)
        if (root / ext).exists():
            errors.append('wave8: external file leaked into repository ' + ident)

    web = control.get('webObservations', [])
    if len(web) != len(WEB_IDS) or {w.get('id') for w in web} != WEB_IDS:
        errors.append('wave8: web observation inventory')
    for w in web:
        ident = w.get('id', '')
        states(w, ident)
        if (
            w.get('evidenceClass') != 'C'
            or w.get('accessState') != 'PARTIAL_OBJECT'
            or w.get('locatorState') != 'EXACT_LOCATOR_VERIFIED'
            or w.get('rawHtmlAcquired') is not False
            or w.get('visualScanInspected') is not False
            or w.get('quoteSafe') is not False
            or 'EVIDENCE_HOLD' not in w.get('holds', [])
        ):
            errors.append('wave8: web observation partial-object contract ' + ident)

    phil = control.get('philologicalResolution', {})
    discs = phil.get('discrepancyClassification', [])
    if len(discs) != len(DISCREPANCY_IDS) or {d.get('id') for d in discs} != DISCREPANCY_IDS:
        errors.append('wave8: discrepancy classification inventory')
    med = phil.get('languageMediumVerdict', {})
    if med.get('john1149_52Medium') != 'GREEK_CATENA_FRAGMENT_ONLY' or med.get('syriacInvolvementOnJohn1149_52') is not False:
        errors.append('wave8: language medium verdict drift')
    ep = phil.get('epistemicStatusAfterWave8', {})
    if ep.get('verifiedGreekOriginalsFor1152') != 0 or ep.get('c25Status') != 'OPEN':
        errors.append('wave8: epistemic closure overclaim')

    repairs = {r['id']: r for r in report.get('repairs', []) if str(r.get('id', '')).startswith('W8-')}
    if set(repairs) != REQUIRED_REPAIRS or set(wave.get('repairIds', [])) != REQUIRED_REPAIRS:
        errors.append('wave8: repair coverage')
    snaps = wave.get('supersededSnapshots', [])
    if len({s['path'] for s in snaps}) != len(snaps) or not {r['file'] for r in repairs.values()} <= {s['path'] for s in snaps}:
        errors.append('wave8: actual preimage coverage')
    baseline_texts: dict[str, str] = {}
    for s in snaps:
        if s.get('commit') != BASELINE:
            errors.append('wave8: preimage baseline')
            continue
        p = subprocess.run(['git', 'show', f"{BASELINE}:{s['path']}"], cwd=root, capture_output=True)
        if p.returncode or (len(p.stdout), digest(p.stdout), git_blob(p.stdout)) != (
            s.get('bytes'), s.get('sha256'), s.get('blob')
        ):
            errors.append('wave8: actual Git preimage mismatch ' + s['path'])
        else:
            baseline_texts[s['path']] = p.stdout.decode('utf-8')

    for r in repairs.values():
        present = r['removed'] in baseline_texts.get(r['file'], '')
        kind = 'BASELINE_REMOVAL_OR_EXPLICIT_SUPERSESSION' if present else 'ADDITIVE_GUARD_NOT_A_HISTORICAL_QUOTE'
        if r.get('rejectedWordingPresentInBaseline') is not present or r.get('controlType') != kind:
            errors.append('wave8: invented historical error ' + r['id'])
        if r['required'] not in (root / r['file']).read_text(encoding='utf-8'):
            errors.append('wave8: owner update missing ' + r['id'])

    for path in REGISTRIES:
        review = json.loads((root / 'ИСКУПЛЕНИЕ' / path).read_text(encoding='utf-8')).get(REVIEW_KEY, {})
        if (
            review.get('controls'),
            review.get('status'),
            review.get('c25'),
            review.get('o11'),
            review.get('greekOriginalVerified'),
            review.get('publicationEligible'),
        ) != (CONTROL, STATUS, 'OPEN', O11, False, False):
            errors.append('wave8: registry review boundary ' + path)
        if (
            review.get('puseyVol1PraefatioEvidenceClass') != 'A1'
            or review.get('puseyVol2AndPg74OcrEvidenceClass') != 'C'
            or review.get('syriacInvolvementOnJohn1149_52') is not False
            or review.get('greekCandidatesQuoteSafe') is not False
        ):
            errors.append('wave8: registry class/medium boundary ' + path)

    ledger = (root / 'ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md').read_text(encoding='utf-8')
    c25 = re.search(r'(?ms)^## C-25\b.*?(?=^## |\Z)', ledger)
    if not c25 or not re.search(r'\*\*Статус:\*\*\s*`OPEN`', c25.group()):
        errors.append('wave8: C25 owner status is not OPEN')
    return errors


def verify_sources(source_root: Path, control: dict) -> list[str]:
    """Full byte & JPEG gate first; never parse text from an unverified external object set."""
    errors: list[str] = []
    raws: dict[str, bytes] = {}
    base = source_root.resolve()
    for f in control.get('files', []):
        ident = f['id']
        target = (base / f['externalRelativePath']).resolve()
        try:
            target.relative_to(base)
        except ValueError:
            errors.append('wave8 replay: path traversal ' + ident)
            continue
        if not target.is_file() or target.is_symlink():
            errors.append('wave8 replay: missing/symlink file ' + ident)
            continue
        raw = target.read_bytes()
        if (digest(raw), len(raw), git_blob(raw)) != (f['sha256'], f['bytes'], f['gitBlob']):
            errors.append('wave8 replay: artifact bytes changed ' + ident)
            continue
        if ident in A1_SCAN_IDS and not (raw.startswith(b'\xff\xd8\xff') and raw.endswith(b'\xff\xd9')):
            errors.append('wave8 replay: invalid JPEG markers ' + ident)
            continue
        raws[ident] = raw
    if errors:
        return errors

    try:
        p292 = raws['PUSEY-V2-P292-TXT'].decode('utf-8')
        p294 = raws['PUSEY-V2-P294-TXT'].decode('utf-8')
        p295 = raws['PUSEY-V2-P295-TXT'].decode('utf-8')
        p296 = raws['PUSEY-V2-P296-TXT'].decode('utf-8')
        p332 = raws['PUSEY-V2-LIB8-SYR-TXT'].decode('utf-8')
        pg39 = raws['FABIO-PG74-039'].decode('utf-8')
        changes = json.loads(raws['OG-COVERAGE-CHANGES'].decode('utf-8'))
        req = json.loads(raws['OG-MISSING-PG74-REQ'].decode('utf-8'))

        if '691Α. a Λάμβανε' not in p292:
            errors.append('wave8 replay: Pusey II 292 691A boundary missing')
        if '294 B. CYRILLI ALEXANDR.' not in p294 or 'S. Isidoro tribuunt recte a.k. Est lib. iii. Ep. 128.' not in p294:
            errors.append('wave8 replay: Pusey II 294 Isidore apparatus missing')
        for needle in (
            'ἅπαντες χρηματίζομεν',
            'τῆς θείας ὁμολογίας ἠξιωμένοι, καὶ τῆς ἐν',
            'παραδείσῳ διαίτης τε καὶ τρυφῆς ἀπολαύοντες',
            'συνεισήγαγε δὲ πάλιν καὶ συνεκόμισε',
            '16‚ 17. τῆς θείας-ἀπολαύοντες c. 1. Cord. εὐτόνως τὴν ἀρέτην ἐργαζόμενοι Nik. Ed.',
            'a 693 A.',
        ):
            if needle not in p295:
                errors.append('wave8 replay: Pusey II 295 expected reading missing: ' + needle)
        if 'Οὐχ ὡς κατὰ πνεῦμα προφητείας ὑπὸ Καϊάφα ἐρρέθη' not in p296 or 'quae sunt in Orig. ad loc. iv. 399 d e.' not in p296:
            errors.append('wave8 replay: Pusey II 296 Mai/Origen apparatus missing')
        if 'Sequuntur quatuor scholia Syriaca' not in p332:
            errors.append('wave8 replay: Pusey II 332 Book VIII Syriac notice missing')
        for needle in (
            '69 IN JOANNEM. — LIB. VII ET VIII FRAGMENTA. 70',
            'χρηματίζομεν',
            'εὐτόνως τὴν ἀρετὴν ἐργαζόμενοι',
            'συνεισήγαγε δὲ πάλιν',
            'καὶ συνεκόμισε πάντας',
            'Οὐχ ὡς (2) κατὰ πνεῦμα προφητείας ὑπὸ Καϊάφα',
            '693',
        ):
            if needle not in pg39:
                errors.append('wave8 replay: Fabio PG74-039 expected reading missing: ' + needle)
        pg74_src = req.get('sources', {}).get('pg74', {})
        if (
            'patrologiaecurs25hopfgoog' not in json.dumps(changes)
            or pg74_src.get('sha256') != '0150e7ffadcf5836ba6198cebdec113effe9e655b652a54388f1e8e8802b2005'
        ):
            errors.append('wave8 replay: open-greek PG74 scan provenance mismatch')
    except (ValueError, KeyError, UnicodeError) as exc:
        errors.append('wave8 replay: invalid source structure ' + str(exc))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--source-root', type=Path)
    args = ap.parse_args()
    try:
        control = json.loads((args.root / CONTROL).read_text(encoding='utf-8'))
        report = json.loads((args.root / REPORT).read_text(encoding='utf-8'))
        errors = check_controls(args.root, report, control)
        replay = verify_sources(args.source_root, control) if args.source_root else []
        errors += replay
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('WAVE8 SOURCES: FAIL —', exc)
        return 1
    print(json.dumps(dict(
        control['statistics'],
        sourceByteReplay=('FAIL' if replay else 'PASS') if args.source_root else 'NOT_RUN',
        rawHtmlReplay='NOT_AVAILABLE_RENDERED_OBSERVATIONS_ONLY',
        puseyVol1PraefatioVisualScanVerified=True,
        greekOriginalFor1152Verified=False,
        puseyVol2AndPg74PageImagesInspected=False,
        humanReadingMeasured=False,
        publicationApproved=False,
    )))
    for error in errors:
        print('FAIL:', error)
    print('WAVE8 SOURCES: ' + ('FAIL' if errors else 'PASS — Vol. I Praefatio A1; Vol. II & PG74 OCR C collated; 11:52 Greek unverified; C25 OPEN'))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
