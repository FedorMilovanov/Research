#!/usr/bin/env python3
"""Read-only, bounded MT/LXX gathering intertexts for John 11:52.

Default: retained controls, scopes, source axes, repairs and actual Git preimages.
--source-root: additionally check 21 external objects BEFORE re-extraction. No
network, writes, inferred manuscript agreement, printed collation, automated
human-reading measure, theological closure or publication approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from atonement_wave3_sources import TEI, OSIS, normalized, osis_words, morphgnt_words, tei_body_text, unique
from atonement_wave4_sources import git_blob

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "ИСКУПЛЕНИЕ/evidence/source_controls_wave6_2026-11-03.json"
REPORT = "ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json"
BASELINE = "75c9cb64d2c75805ca7fa05dca7f6c5f626c386f"
REVIEW_KEY = "otGatheringReviewWave6"
PINS = {
    "OpenGreekAndLatin/First1KGreek": "ed91552c52530c8f5a3ddf2dd767e899372a804c",
    "openscriptures/morphhb": "3d15126fb1ef74867fc1434be1942e837932691f",
    "morphgnt/py-sblgnt": "904fed08a14bffea6e1776d8c4c3eeb7c6092688",
}
BOOKS = {"Deut": "005", "Isa": "048", "Jer": "049", "Ezek": "053", "Zech": "046"}
OT_RANGES = (
    ("DEUT30", "Deut", (30, 1, 10), (30, 1, 10)),
    ("ISA11", "Isa", (11, 10, 16), (11, 10, 16)),
    ("ISA43", "Isa", (43, 1, 7), (43, 1, 7)),
    ("ISA56", "Isa", (56, 1, 8), (56, 1, 8)),
    ("JER31", "Jer", (31, 1, 14), (38, 1, 14)),
    ("EZ34", "Ezek", (34, 1, 31), (34, 1, 31)),
    ("EZ37", "Ezek", (37, 15, 28), (37, 15, 28)),
    ("ZECH2", "Zech", (2, 5, 17), (2, 1, 13)),
)
NT_RANGES = (("JN1", 1, 9, 18), ("JN7", 7, 30, 39), ("JN10", 10, 1, 18), ("JN11", 11, 45, 57))
REQUIRED_REPAIRS = {"W6-" + s for s in (
    "NT15", "OT14", "C25", "H11", "P13", "NT09", "QMAP", "P04", "P06", "P18", "S04",
    "N00", "O00", "ROOT00", "NT-DATA", "OT-DATA", "ROOT-DATA", "S-DATA")}
FALSE_BOUNDARIES = (
    "fullBooksRead", "printedCollationClaimed", "criticalOriginalTextSettled", "cyrilGreekRead",
    "oldPackagesReplayed", "publicationEligible", "interpretationProvedByCode",
    "quotationInJohn1152Established", "agentImportedIntoJn1152", "everyNationMeansEveryIndividual",
    "covenantalMeansExclusiveDeath", "creationMeansAllHumans", "allMtLxxPairsVerbatimEquivalent",
    "creationAlternativeErased", "humanReadingMeasured",
)
# Verbatim digital signals, not claims that their presence proves an allusion.
SIGNALS = {
    "DEUT-DIASPORA": ("LXX-DEUT30", "Deut.30.4", "ἡ διασπορά σου"),
    "DEUT-DIVINE-AGENT": ("LXX-DEUT30", "Deut.30.1", "σε διασκορπίσῃ Κύριος"),
    "ISA-NATIONS": ("LXX-ISA11", "Isa.11.10", "ἐπʼ αὐτῷ ἔθνη ἐλπιοῦσιν"),
    "ISA-SCATTERED": ("LXX-ISA11", "Isa.11.12", "τοὺς διεσπαρμένους Ἰούδα"),
    "CREATED-JACOB": ("LXX-ISA43", "Isa.43.1", "ὁ ποιήσας σε Ἰακώβ"),
    "SONS-DAUGHTERS": ("LXX-ISA43", "Isa.43.6", "τοὺς υἱούς μου"),
    "NAMED": ("LXX-ISA43", "Isa.43.7", "πάντας ὅσοι ἐπικέκληνται τῷ ὀνόματί μου"),
    "FOREIGNER": ("LXX-ISA56", "Isa.56.3", "ὁ ἀλλογενὴς ὁ προσκείμενος"),
    "COVENANT": ("LXX-ISA56", "Isa.56.6", "ἀντεχομένους τῆς διαθήκης μου"),
    "ADDED-GATHERING": ("LXX-ISA56", "Isa.56.8", "συνάξω ἐπʼ αὐτὸν συναγωγήν"),
    "FATHER-ISRAEL": ("LXX-JER31", "Jer.38.9", "τῷ Ἰσραὴλ εἰς πατέρα"),
    "FIRSTBORN": ("LXX-JER31", "Jer.38.9", "Ἐφράιμ πρωτότοκός μού ἐστιν"),
    "WINNOWING-NOT-DIASKORPIZO": ("LXX-JER31", "Jer.38.10", "Ὁ λικμήσας τὸν Ἰσραὴλ συνάξει αὐτόν"),
    "REDEEMED-JACOB": ("LXX-JER31", "Jer.38.11", "ἐλυτρώσατο Κύριος τὸν Ἰακώβ"),
    "NEGLECT": ("LXX-EZ34", "Ezek.34.5", "διὰ τὸ μὴ εἶναι ποιμένας"),
    "GATHER-COUNTRIES": ("LXX-EZ34", "Ezek.34.13", "συνάξω αὐτοὺς ἀπὸ τῶν χωρῶν"),
    "INTERNAL-JUDGMENT": ("LXX-EZ34", "Ezek.34.17", "διακρινῶ ἀνὰ μέσον προβάτου καὶ προβάτου"),
    "ONE-SHEPHERD-34": ("LXX-EZ34", "Ezek.34.23", "ποιμένα ἕνα"),
    "ISRAEL-PEOPLE": ("LXX-EZ34", "Ezek.34.30", "οἶκος Ἰσραήλ"),
    "TWO-NATIONS": ("LXX-EZ37", "Ezek.37.22", "οὐκ ἔσονται ἔτι εἰς δύο ἔθνη"),
    "ONE-SHEPHERD-37": ("LXX-EZ37", "Ezek.37.24", "ποιμὴν εἷς πάντων"),
    "ZECH-GATHER-NOT-SPREAD": ("LXX-ZECH2", "Zech.2.6", "συνάξω ὑμᾶς"),
    "MANY-NATIONS": ("LXX-ZECH2", "Zech.2.11", "ἔθνη πολλὰ"),
    "PEOPLE": ("LXX-ZECH2", "Zech.2.11", "ἔσονται αὐτῷ εἰς λαόν"),
    "JOHN-FAITH-CHILDREN": ("JN1", "040112", "τέκνα θεοῦ γενέσθαι, τοῖς πιστεύουσιν"),
    "JOHN-INTERLOCUTORS": ("JN7", "040735", "εἶπον οὖν οἱ Ἰουδαῖοι πρὸς ἑαυτούς"),
    "JOHN-DIASPORA": ("JN7", "040735", "τὴν διασπορὰν τῶν Ἑλλήνων"),
    "JOHN-WOLF": ("JN10", "041012", "ὁ λύκος ἁρπάζει αὐτὰ καὶ ⸀σκορπίζει"),
    "JOHN-ONE-FLOCK": ("JN10", "041016", "μία ποίμνη, εἷς ποιμήν"),
    "JOHN-GATHERING": ("JN11", "041152", "συναγάγῃ εἰς ἕν"),
}
# Visible defects/suspect fragments and a verse marker; NO conjectural correction.
ANOMALIES = {
    "DEUT30-3": ("LXX-DEUT30", "Deut.30.3", "καὶ σε"),
    "DEUT30-5": ("LXX-DEUT30", "Deut.30.5", "πλεοναστόν σε"),
    "DEUT30-6": ("LXX-DEUT30", "Deut.30.6", "τὴν σου κοὶ"),
    "DEUT30-10": ("LXX-DEUT30", "Deut.30.10", "ἐὰν ἐπιστραφῇς τὸν θεόν σου"),
    "ISA11-16": ("LXX-ISA11", "Isa.11.16", "§ ¹6"),
    "EZ34-1": ("LXX-EZ34", "Ezek.34.1", "πρὸς μ λέγων"),
    "EZ34-4": ("LXX-EZ34", "Ezek.34.4", "ἐσαωματοποιήσατε"),
    "EZ34-12": ("LXX-EZ34", "Ezek.34.12", "διεσ πάρησαν"),
    "EZ37-25": ("LXX-EZ37", "Ezek.37.25", "ἄθρχων"),
    "EZ37-26": ("LXX-EZ37", "Ezek.37.26", "διαθήσομαι ὐτοῖς"),
    "ZECH2-4": ("LXX-ZECH2", "Zech.2.4", "Κατακάρπαως"),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def context_digest(verses: list[dict]) -> str:
    # Deliberately NOT NFC: OSHB README warns against Hebrew normalization.
    return digest("\n".join(v["ref"] + " " + v["text"] for v in verses).encode())


def file_layout() -> dict:
    result = {}
    for book, work in BOOKS.items():
        stem = f"data/tlg0527/tlg{work}/"
        result["LXX-" + book] = ("OpenGreekAndLatin/First1KGreek", stem + f"tlg0527.tlg{work}.1st1K-grc1.xml", "PRIMARY_TEXT")
        result["LXX-" + book + "-META"] = ("OpenGreekAndLatin/First1KGreek", stem + "__cts__.xml", "EDITION_METADATA")
        result["MT-" + book] = ("openscriptures/morphhb", f"wlc/{book}.xml", "PRIMARY_TEXT")
    for ident, repo, path in (
        ("F1K-README", "OpenGreekAndLatin/First1KGreek", "README.md"),
        ("F1K-LICENSE", "OpenGreekAndLatin/First1KGreek", "license.md"),
        ("MT-README", "openscriptures/morphhb", "README.md"),
        ("MT-LICENSE", "openscriptures/morphhb", "LICENSE.md"),
        ("NT-README", "morphgnt/py-sblgnt", "README.md"),
    ):
        result[ident] = (repo, path, "RIGHTS_OR_PROVENANCE_METADATA")
    result["NT-JOHN"] = ("morphgnt/py-sblgnt", "pysblgnt/sblgnt/64-Jn-morphgnt.txt", "PRIMARY_TEXT")
    return result


def definitions() -> list[dict]:
    rows = []
    for ident, book, mt, lxx in OT_RANGES:
        for prefix, kind, bounds in (("MT", "osis-ketiv", mt), ("LXX", "tei-body", lxx)):
            rows.append(dict(id=prefix + "-" + ident, sourceFile=prefix + "-" + book, kind=kind,
                             book=book, chapter=bounds[0], firstVerse=bounds[1], lastVerse=bounds[2]))
    rows += [dict(id=i, sourceFile="NT-JOHN", kind="morphgnt-8", book="John", chapter=c,
                  firstVerse=a, lastVerse=b) for i, c, a, b in NT_RANGES]
    return rows


def expected_refs(row: dict) -> list[str]:
    return [f"04{row['chapter']:02}{v:02}" if row['kind'] == "morphgnt-8" else
            f"{row['book']}.{row['chapter']}.{v}" for v in range(row['firstVerse'], row['lastVerse'] + 1)]


def extract_context(raw: bytes, row: dict, cache: dict | None = None) -> list[dict]:
    cache = {} if cache is None else cache
    key = (row['sourceFile'], row['kind'])
    if key not in cache:
        cache[key] = (osis_words(raw) if row['kind'] == 'osis-ketiv' else
                      morphgnt_words(raw, 8) if row['kind'] == 'morphgnt-8' else ET.fromstring(raw))
    parsed = cache[key]
    if row['kind'] == 'tei-body':
        body = unique(parsed.findall('.//' + TEI + 'body'), 'TEI body')
        chapter = unique([e for e in body.iter(TEI + 'div') if e.get('subtype') == 'chapter'
                          and e.get('n') == str(row['chapter'])], 'TEI chapter')
    result = []
    for v, ref in zip(range(row['firstVerse'], row['lastVerse'] + 1), expected_refs(row)):
        if row['kind'] == 'tei-body':
            element = unique([e for e in chapter.iter(TEI + 'div') if e.get('subtype') == 'verse'
                              and e.get('n') == str(v)], 'TEI verse')
            text = normalized(tei_body_text(element))
        else:
            text = ' '.join(' '.join(w['text'] for w in parsed[ref]).split())
            if row['kind'] == 'morphgnt-8':
                text = normalized(text)
        result.append({'ref': ref, 'text': text})
    return result


def pairings() -> list[dict]:
    return [dict(id=i, mtContext='MT-' + i, lxxContext='LXX-' + i,
                 verseMap=[{'mt': f'{b}.{m[0]}.{mv}', 'lxx': f'{b}.{g[0]}.{gv}'}
                           for mv, gv in zip(range(m[1], m[2]+1), range(g[1], g[2]+1))])
            for i, b, m, g in OT_RANGES]


def excluded_notes(raw: bytes, row: dict) -> list[dict]:
    refs = set(expected_refs(row))
    return [{'ref': v.get('osisID'), 'xml': ET.tostring(n, encoding='unicode')}
            for v in ET.fromstring(raw).iter(OSIS + 'verse') if v.get('osisID') in refs
            for n in v.findall(OSIS + 'note')]


def edition_control(raw: bytes, metadata: bytes, book: str) -> dict:
    root, cts = ET.fromstring(raw), ET.fromstring(metadata)
    urn = f'urn:cts:greekLit:tlg0527.tlg{BOOKS[book]}.1st1K-grc1'
    unique([e for e in root.iter(TEI+'div') if e.get('type') == 'edition' and e.get('n') == urn], 'edition URN')
    desc = unique(root.findall('.//' + TEI + 'sourceDesc'), 'source description')
    edition = unique([e for e in cts.iter('{http://chs.harvard.edu/xmlns/cts}edition')
                      if e.get('urn') == urn], 'matching CTS edition, not another Isaiah edition')
    return dict(book=book, sourceFile='LXX-'+book, metadataFile='LXX-'+book+'-META', editionUrn=urn,
                sourceDescription=normalized(''.join(desc.itertext())),
                matchingCtsDescription=normalized(''.join(edition.itertext())),
                printYear='1901' if book == 'Deut' else '1905', printedCollationClaimed=False)


def check_controls(root: Path, report: dict, control: dict) -> list[str]:
    errors = []
    wave = report.get('wave6', {})
    if (wave.get('controls'), wave.get('baselineCommit'), wave.get('publicationEligible'), wave.get('mergePerformed')) != (CONTROL, BASELINE, False, False):
        errors.append('wave6: journal/control/merge boundary')
    for key in FALSE_BOUNDARIES:
        if control.get(key) is not False:
            errors.append('wave6: missing/overclaimed boundary ' + key)
    if (control.get('c25'), control.get('o09'), control.get('interpretationStatus')) != (
            'OPEN', 'BOUNDED_COMPARISON_DONE_CRITICAL_FOLLOWUP_OPEN', 'ARGUED_PROVISIONAL_NOT_MACHINE_PROOF'):
        errors.append('wave6: C25/O09/preference closure drift')
    if control.get('pairings') != pairings():
        errors.append('wave6: explicit MT/LXX verse map drift')
    if control.get('hebrewNormalization') != 'WHITESPACE_ONLY_NO_NFC_KETIV_NOT_QERE':
        errors.append('wave6: Hebrew extraction semantics drift')
    expected = {d['id']: d for d in definitions()}
    rows = control.get('contexts', [])
    contexts = {x['id']: x for x in rows}
    if len(rows) != len(expected) or set(contexts) != set(expected):
        errors.append('wave6: context coverage missing/duplicate')
    lookup = {}
    for ident, row in contexts.items():
        definition = expected.get(ident, {})
        if not definition or any(row.get(k) != v for k, v in definition.items()):
            errors.append('wave6: context bounds/source drift ' + ident)
            continue
        verses = row.get('verses', [])
        if ([v.get('ref') for v in verses] != expected_refs(definition) or
                row.get('textSha256') != context_digest(verses) or not all(v.get('text') for v in verses)):
            errors.append('wave6: context refs/text hash drift ' + ident)
        lookup.update({(ident, v['ref']): v['text'] for v in verses})
        if row.get('contextVerified') is not True or row.get('readingScope') != 'SELECTED_DIGITAL_CONTEXT_NOT_WHOLE_BOOK_OR_PRINT':
            errors.append('wave6: context scope drift ' + ident)
    for field, anchors in (('signals', SIGNALS), ('digitalAnomalies', ANOMALIES)):
        entries = control.get(field, [])
        if len(entries) != len(anchors) or {e['id'] for e in entries} != set(anchors):
            errors.append('wave6: missing/duplicate ' + field)
        for entry in entries:
            wanted = anchors.get(entry['id'])
            if wanted != (entry.get('context'), entry.get('ref'), entry.get('verbatim')) or not wanted or wanted[2] not in lookup.get(wanted[:2], ''):
                errors.append('wave6: changed digital signal/anomaly ' + entry['id'])
            if field == 'digitalAnomalies' and (entry.get('silentlyEmended') is not False or entry.get('printedCauseVerified') is not False):
                errors.append('wave6: conjectural repair/printed cause promoted ' + entry['id'])
    if control.get('statistics') != dict(filePins=21, primaryTextFiles=11, metadataFiles=10,
                                         otContexts=16, otPairs=104, ntContexts=4, ntVerses=51, verseInstances=259):
        errors.append('wave6: coverage statistics drift')
    files = control.get('files', [])
    layout = file_layout()
    if len(files) != len(layout) or {f['id'] for f in files} != set(layout):
        errors.append('wave6: file inventory missing/duplicate')
    policy = json.loads((root / 'data/repository-evidence-policy-v2.json').read_text())
    axes = {'evidenceClass':'sourceClasses', 'accessState':'accessStates', 'locatorState':'locatorStates',
            'rightsState':'rightsStates', 'publicationState':'publicationStates'}
    for f in files:
        if (f.get('repo'), f.get('path'), f.get('role')) != layout.get(f['id']) or f.get('commit') != PINS.get(f.get('repo')):
            errors.append('wave6: wrong source identity/pin ' + f['id'])
        if (f.get('externalRelativePath') != f.get('repo', '').replace('/', '--') + '/' + f.get('path', '') or
                not re.fullmatch(r'[0-9a-f]{40}', f.get('gitBlob', '')) or not re.fullmatch(r'[0-9a-f]{64}', f.get('sha256', '')) or
                not isinstance(f.get('bytes'), int) or f.get('bytes', 0) <= 0):
            errors.append('wave6: malformed file pin/path ' + f['id'])
        for axis, vocabulary in axes.items():
            if f.get(axis) not in policy[vocabulary]:
                errors.append('wave6: invalid file axis ' + f['id'] + '/' + axis)
        if f.get('publicationState') != 'BLOCKED' or 'PUBLICATION_HOLD' not in f.get('holds', []):
            errors.append('wave6: publication boundary ' + f['id'])
        if f.get('evidenceClass') != ('A1' if f.get('role') == 'PRIMARY_TEXT' else 'C') or f.get('quoteSafe') is not False:
            errors.append('wave6: file role is not a blanket quote-safe biblical witness ' + f['id'])
    profiles = control.get('sources', [])
    if len(profiles) != 3 or {s['id'] for s in profiles} != {'MT', 'LXX', 'JOHN'}:
        errors.append('wave6: primary profiles missing/duplicate')
    for s in profiles:
        prefix = {'MT': 'MT-', 'LXX': 'LXX-', 'JOHN': 'JN'}.get(s['id'], '?')
        scoped = [d for d in definitions() if d['id'].startswith(prefix)]
        if s.get('contextIds') != [d['id'] for d in scoped] or s.get('sourceFileIds') != sorted({d['sourceFile'] for d in scoped}):
            errors.append('wave6: primary profile context/file binding ' + s['id'])
        version_terms = {'MT': ('Westminster Leningrad Codex', PINS['openscriptures/morphhb']),
                         'LXX': ('Swete', '.1st1K-grc1', PINS['OpenGreekAndLatin/First1KGreek']),
                         'JOHN': ('SBLGNT', 'eight-column', PINS['morphgnt/py-sblgnt'])}.get(s['id'], ())
        if not all(term in s.get('version', '') for term in version_terms):
            errors.append('wave6: primary profile edition identity ' + s['id'])
        for axis, vocabulary in axes.items():
            if s.get(axis) not in policy[vocabulary]:
                errors.append('wave6: invalid primary axis ' + s['id'] + '/' + axis)
        if (s.get('evidenceClass') != 'A1' or s.get('accessState') != 'FULL_OBJECT_VERIFIED' or
                s.get('locatorState') != 'EXACT_LOCATOR_VERIFIED' or s.get('rightsState') != 'STORAGE_ONLY' or
                s.get('publicationState') != 'BLOCKED' or 'PUBLICATION_HOLD' not in s.get('holds', []) or
                s.get('contextVerified') is not True or not s.get('quoteSafeScope') or not s.get('readingScope') or not s.get('version')):
            errors.append('wave6: primary profile scope/axes ' + s['id'])
    eds = control.get('editions', [])
    if len(eds) != 5 or {e['book'] for e in eds} != set(BOOKS):
        errors.append('wave6: edition coverage')
    for e in eds:
        book = e['book']
        if (book not in BOOKS or e.get('sourceFile') != 'LXX-' + book or e.get('metadataFile') != 'LXX-' + book + '-META' or
                e.get('editionUrn') != f'urn:cts:greekLit:tlg0527.tlg{BOOKS.get(book)}.1st1K-grc1' or
                e.get('printYear') != ('1901' if book == 'Deut' else '1905') or e.get('printedCollationClaimed') is not False or
                not all('Swete' in e.get(k, '') and e.get('printYear', '?') in e.get(k, '') for k in ('sourceDescription','matchingCtsDescription'))):
            errors.append('wave6: edition identity/year/printed overclaim')
    if control.get('speakerControl', {}).get('speaker') != 'INTERLOCUTORS_QUESTION_NOT_NARRATOR_ENDORSEMENT' or control.get('speakerControl', {}).get('ref') != '040735':
        errors.append('wave6: John7:35 speaker is not narrator endorsement')
    differences = control.get('nonEquivalences', [])
    if (len(differences) != 3 or {(x.get('mt'), x.get('lxx')) for x in differences} != {
            ('Jer.31.8', 'Jer.38.8'), ('Zech.2.10', 'Zech.2.6'), ('Ezek.34.16', 'Ezek.34.16')} or
            any(not x.get('observation') for x in differences)):
        errors.append('wave6: MT/LXX differences cannot be silently harmonized')
    alternatives = control.get('alternatives', [])
    if ({a['id'] for a in alternatives} != {'DIASPORA_ONLY', 'GATHERED_MULTIETHNIC_COMMUNITY', 'ALL_HUMAN_CREATION'} or
            len(alternatives) != 3 or any(not a.get('grounds') or not a.get('limits') for a in alternatives) or
            control.get('preferredReading') != 'GATHERED_MULTIETHNIC_COMMUNITY'):
        errors.append('wave6: alternatives/argued preference drift')
    assessments = control.get('intertextAssessments', [])
    if len(assessments) != 8 or {x['id'] for x in assessments} != {x[0] for x in OT_RANGES}:
        errors.append('wave6: intertext assessment coverage')
    for a in assessments:
        if a.get('explicitQuotationEstablished') is not False or not a.get('grounds') or not a.get('limits'):
            errors.append('wave6: intertext promoted to quotation ' + a['id'])
    repairs = {r['id']: r for r in report['repairs'] if r['id'].startswith('W6-')}
    if set(repairs) != REQUIRED_REPAIRS or set(wave.get('repairIds', [])) != REQUIRED_REPAIRS:
        errors.append('wave6: repairs missing/extra')
    snapshots = wave.get('supersededSnapshots', [])
    baseline = {}
    if len({s['path'] for s in snapshots}) != len(snapshots) or not {r['file'] for r in repairs.values()} <= {s['path'] for s in snapshots}:
        errors.append('wave6: preimage coverage/duplicate')
    for s in snapshots:
        if s.get('commit') != BASELINE:
            errors.append('wave6: wrong preimage baseline')
            continue
        p = subprocess.run(['git', 'show', f"{BASELINE}:{s['path']}"], cwd=root, capture_output=True)
        if p.returncode or (len(p.stdout), digest(p.stdout), git_blob(p.stdout)) != (s.get('bytes'), s.get('sha256'), s.get('blob')):
            errors.append('wave6: actual preimage bytes differ ' + s['path'])
        else:
            baseline[s['path']] = p.stdout.decode()
    for r in repairs.values():
        present = r['removed'] in baseline.get(r['file'], '')
        kind = 'BASELINE_REMOVAL_OR_EXPLICIT_SUPERSESSION' if present else 'ADDITIVE_GUARD_NOT_A_HISTORICAL_QUOTE'
        if r.get('rejectedWordingPresentInBaseline') is not present or r.get('controlType') != kind:
            errors.append('wave6: invented historical error ' + r['id'])
        if r['required'] not in (root / r['file']).read_text():
            errors.append('wave6: integrated repair missing ' + r['id'])
    for lane, name in (('', 'atonement'), ('nt/', 'nt'), ('ot/', 'ot'), ('synthesis/', 'synthesis')):
        d = json.loads((root / f'ИСКУПЛЕНИЕ/{lane}data/{name}-corpus-v1.json').read_text())
        review = d.get(REVIEW_KEY, {})
        if (review.get('controls'), review.get('c25'), review.get('o09'), review.get('publicationEligible')) != (
                CONTROL, 'OPEN', 'BOUNDED_COMPARISON_DONE_CRITICAL_FOLLOWUP_OPEN', False):
            errors.append('wave6: registry review drift ' + name)
        if name == 'ot':
            card = next((c for c in d['cards'] if c['id'] == 14), {}).get('gatheringReviewWave6', {})
            mt_profile = next((s for s in profiles if s['id'] == 'MT'), {})
            if (card.get('sourceControl') != CONTROL or card.get('historicalCardFieldsNotRecertified') is not True or
                    card.get('sourceProfileIds') != ['MT', 'LXX'] or card.get('contextVerified') is not True or
                    not card.get('readingScope') or not card.get('quoteSafeScope') or
                    any(card.get(k) != mt_profile.get(k) for k in axes)):
                errors.append('wave6: card14 bounded review promoted to whole-card closure')
    ledger = (root / 'ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md').read_text()
    c25 = re.search(r'(?ms)^## C-25\b.*?(?=^## |\Z)', ledger)
    if not c25 or not re.search(r'\*\*Статус:\*\*\s*`OPEN`', c25.group()):
        errors.append('wave6: C25 cannot silently close')
    return errors


def verify_sources(source_root: Path, control: dict) -> list[str]:
    errors, raws, cache = [], {}, {}
    base = source_root.resolve()
    for f in control['files']:
        path = (base / f['externalRelativePath']).resolve()
        if not path.is_relative_to(base):
            errors.append('wave6 replay: unsafe source path ' + f['id'])
            continue
        try:
            raw = path.read_bytes()
        except OSError as exc:
            errors.append(f"wave6 replay: missing object {f['id']}: {exc}")
            continue
        if (len(raw), digest(raw), git_blob(raw)) != (f['bytes'], f['sha256'], f['gitBlob']):
            errors.append('wave6 replay: file bytes changed ' + f['id'])
            continue
        raws[f['id']] = raw
    for row in control.get('contexts', []):
        try:
            raw = raws[row['sourceFile']]
            verses = extract_context(raw, row, cache)
            if verses != row['verses'] or context_digest(verses) != row['textSha256']:
                errors.append('wave6 replay: context differs ' + row['id'])
            if row['kind'] == 'osis-ketiv' and excluded_notes(raw, row) != row.get('excludedNotes'):
                errors.append('wave6 replay: ketiv/qere/editorial separation differs ' + row['id'])
        except (ValueError, KeyError, UnicodeError, ET.ParseError) as exc:
            errors.append(f"wave6 replay: unavailable/invalid context {row['id']}: {exc}")
    for e in control.get('editions', []):
        try:
            if edition_control(raws[e['sourceFile']], raws[e['metadataFile']], e['book']) != e:
                errors.append('wave6 replay: edition differs ' + e['book'])
        except (ValueError, KeyError, UnicodeError, ET.ParseError) as exc:
            errors.append('wave6 replay: unavailable edition ' + e['book'] + ': ' + str(exc))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--source-root', type=Path)
    args = ap.parse_args()
    try:
        control = json.loads((args.root / CONTROL).read_text())
        report = json.loads((args.root / REPORT).read_text())
        errors = check_controls(args.root, report, control)
        replay = verify_sources(args.source_root, control) if args.source_root else []
        errors += replay
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('WAVE6 SOURCES: FAIL —', exc)
        return 1
    print(json.dumps(dict(control['statistics'], sourceByteReplay=('FAIL' if replay else 'PASS') if args.source_root else 'NOT_RUN',
                          humanReadingMeasured=False, printedCollationClaimed=False, publicationApproved=False)))
    for e in errors:
        print('FAIL:', e)
    print('WAVE6 SOURCES: ' + ('FAIL' if errors else 'PASS — bounded intertexts; C25 OPEN'))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
