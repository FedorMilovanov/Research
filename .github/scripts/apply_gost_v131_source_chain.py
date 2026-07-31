from pathlib import Path
import csv

ROOT = Path('БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED')
LEDGER = ROOT / 'groups/06_DATA_AND_PROOF_LEDGERS.md'
DATA = ROOT / 'data'
SOURCES = DATA / 'SOURCE_ANCHORS.csv'
PROOF = DATA / 'PROOF_STATUS_LEDGER.csv'
MICRO = DATA / 'NEXT_MICROBATCH.csv'

for path in (LEDGER, SOURCES, PROOF, MICRO):
    if not path.exists():
        raise SystemExit(f'missing required file: {path}')

MARKER = '## v131 — `Воскресная школа`: source-chain correction and exact recovery target'
BLOCK = r'''
## v131 — `Воскресная школа`: source-chain correction and exact recovery target

### Derivative claims collapse to one citation

The repeated attribution of `Воскресная школа` to V. I. Gusaruk in Mochola-derived press lists and later biographical profiles is not a set of independent confirmations. The biographical profile exposes the underlying locator: **`Сеятель Истины`, 1926, №2, p.15**. That issue and page have not been inspected, so the editor attribution and the competing `1923–1936` / `1933–1936` chronologies remain `HOLD`.

### Publisher route and holding exclusion

The official RUEBU / Slavic Missionary Publications archive is the correct publisher route, but the public archive is being updated and does not expose the target early issue. The Mennonite Heritage Centre serial inventory lists its 1926 `Seiatel Istinj` holdings as №1, №5 and №8–12; therefore №2 is not a viable MHC request target. This is a routing exclusion, not evidence that the issue is lost.

### Aggregate-catalog caution

The `Эмигрантика` aggregate entry ends the early sequence in 1922 and resumes it in 1956, while the MHC inventory physically records issues from 1925–1927. Catalog silence must not be used as negative evidence for the interwar run or for №2/1926.

### Single next proof step

Request only four elements from the publisher archive: the cover, contents, page 15 and final colophon of `Сеятель Истины` 1926 №2. Until those are seen, do not promote Gusaruk's role, the appendix start year, office, binding relation or issue count to primary-verified status. The institutional request is prepared but not sent.

**Routes retained:**
- official publisher archive: https://ruebu.net/ru/publications/sower-of-truth-archive
- exact-citation profile: https://zarubezhje.narod.ru/gi/g_046.htm
- MHC holding inventory: https://www.mharchives.ca/holdings/serials/r.htm
- aggregate catalog with coverage gap: https://emigrantika.imli.ru/cat2010/715-bookiv
'''

text = LEDGER.read_text(encoding='utf-8')
if MARKER not in text:
    LEDGER.write_text(text.rstrip() + '\n\n' + BLOCK.strip() + '\n', encoding='utf-8')


def load_csv(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames or []
        rows = list(reader)
    if not fields:
        raise SystemExit(f'missing CSV header: {path}')
    return fields, rows


def save_csv(path: Path, fields, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator='\r\n')
        writer.writeheader()
        writer.writerows(rows)


def upsert(path: Path, key_fields, record):
    fields, rows = load_csv(path)
    keys = [(k, record.get(k, '')) for k in key_fields if record.get(k, '')]
    if not keys:
        raise SystemExit(f'no key supplied for {path}')
    matches = [row for row in rows if any(row.get(k, '') == value for k, value in keys)]
    if len(matches) > 1:
        raise SystemExit(f'duplicate key in {path}: {keys}')
    clean = {key: value for key, value in record.items() if key in fields}
    if matches:
        matches[0].update(clean)
    else:
        row = {field: '' for field in fields}
        row.update(clean)
        rows.append(row)
    save_csv(path, fields, rows)


upsert(SOURCES, ['source_id', 'id'], {
    'source_id': 'GOST-131-SRC-SEIATEL1926-02',
    'url': 'https://ruebu.net/ru/publications/sower-of-truth-archive',
    'confirms': 'Official publisher/archive route for exact cited target Seiatel Istiny 1926 no.2 p.15; public early issue not exposed.',
    'id': '',
    'source': 'RUEBU / Slavic Missionary Publications archive; exact locator disclosed by Gusaruk profile',
    'authority_level': 'A-route / primary page unseen',
    'used_for': 'Gusaruk and Voskresnaia Shkola source-chain verification',
    'version': 'v131',
    'source_key': 'GOST-131-SRC-SEIATEL1926-02',
    'use': 'targeted cover-contents-p15-colophon request',
    'label': 'Seiatel Istiny 1926 no.2 p.15 target',
    'type': 'official publisher archive route plus exact primary citation',
    'trust_note': 'Citation is exact but wording/page not inspected; derivative profiles are not independent confirmations.',
    'source_type': 'official publisher route / primary target',
    'note': 'Profile exposing locator: https://zarubezhje.narod.ru/gi/g_046.htm ; keep Gusaruk role and appendix chronology HOLD.'
})

upsert(SOURCES, ['source_id', 'id'], {
    'source_id': 'GOST-131-SRC-MHC-EXCLUSION',
    'url': 'https://www.mharchives.ca/holdings/serials/r.htm',
    'confirms': 'MHC 1926 Seiatel Istinj holdings are no.1, no.5 and no.8-12; target no.2 is not held there.',
    'id': '',
    'source': 'Mennonite Heritage Centre serial inventory',
    'authority_level': 'A-metadata',
    'used_for': 'holding exclusion and request routing',
    'version': 'v131',
    'source_key': 'GOST-131-SRC-MHC-EXCLUSION',
    'use': 'do not request no.2 from MHC',
    'label': 'MHC holding exclusion — Seiatel Istiny 1926 no.2',
    'type': 'institutional holdings inventory',
    'trust_note': 'Excludes only this holding route; does not prove universal absence or loss.',
    'source_type': 'institutional holding metadata',
    'note': 'Preserve as negative routing evidence, not a missing-publication claim.'
})

upsert(SOURCES, ['source_id', 'id'], {
    'source_id': 'GOST-131-SRC-EMIGRANTIKA-GAP',
    'url': 'https://emigrantika.imli.ru/cat2010/715-bookiv',
    'confirms': 'Aggregate catalog omits 1925-1927 issues physically listed by MHC, so its silence cannot establish absence.',
    'id': '',
    'source': 'Emigrantika aggregate serial record compared with MHC inventory',
    'authority_level': 'B-catalog control',
    'used_for': 'negative-evidence caution',
    'version': 'v131',
    'source_key': 'GOST-131-SRC-EMIGRANTIKA-GAP',
    'use': 'catalog coverage-gap control',
    'label': 'Emigrantika chronology coverage gap',
    'type': 'aggregate bibliography conflict',
    'trust_note': 'Useful as a lead, not as a complete holdings or publication chronology.',
    'source_type': 'aggregate catalog comparison',
    'note': 'MHC independently lists physical 1925-1927 holdings.'
})

upsert(PROOF, ['item_id', 'id'], {
    'item_id': 'GOST-130-004',
    'corpus': 'Воскресная школа',
    'issue': 'Gusaruk source chain / Seiatel Istiny 1926 no.2 p.15',
    'status': 'exact_primary_citation_located_issue_unseen',
    'pages': 'p.15 target; cover/contents/colophon required',
    'holding': 'RUEBU publisher archive route; MHC inventory excludes no.2',
    'source': 'Gusaruk profile -> Seiatel Istiny 1926 no.2 p.15; MHC inventory; Emigrantika comparison',
    'next_action': 'Obtain cover, contents, p.15 and final colophon from RUEBU; do not request no.2 from MHC',
    'id': '',
    'year': '1926 / appendix chronology 1923-1936 vs 1933-1936',
    'source_url': 'https://ruebu.net/ru/publications/sower-of-truth-archive',
    'verification_note': 'Derivative claims collapse to one exact citation; page unseen; Gusaruk editorship and start year remain HOLD; Emigrantika has a demonstrated coverage gap.',
    'version': 'v131'
})

fields, rows = load_csv(MICRO)
old_item = 'Locate official Voskresnaia Shkola holding'
new_item = 'Obtain Seiatel Istiny 1926 no.2 p.15'
old_matches = [row for row in rows if row.get('item', '') == old_item]
new_matches = [row for row in rows if row.get('item', '') == new_item]
if len(old_matches) > 1 or len(new_matches) > 1 or (old_matches and new_matches):
    raise SystemExit('unsafe duplicate generic/exact Voskresnaia microbatch rows')
target = new_matches[0] if new_matches else old_matches[0] if old_matches else None
if target is None:
    target = {field: '' for field in fields}
    rows.append(target)
target.update({
    'priority': 'P0',
    'item': new_item,
    'goal': 'Acquire only cover, contents, p.15 and final colophon; verify exact wording naming Gusaruk and relation to Voskresnaia Shkola/Gost',
    'blocker': 'RUEBU early archive is not publicly exposed; MHC lacks no.2; request is READY TO REQUEST — NOT SENT'
})
save_csv(MICRO, fields, rows)

# Exact uniqueness and marker gates.
if LEDGER.read_text(encoding='utf-8').count(MARKER) != 1:
    raise SystemExit('v131 ledger marker count is not one')
for path, key, value in [
    (SOURCES, 'source_id', 'GOST-131-SRC-SEIATEL1926-02'),
    (SOURCES, 'source_id', 'GOST-131-SRC-MHC-EXCLUSION'),
    (SOURCES, 'source_id', 'GOST-131-SRC-EMIGRANTIKA-GAP'),
    (PROOF, 'item_id', 'GOST-130-004'),
    (MICRO, 'item', new_item),
]:
    _, check_rows = load_csv(path)
    count = sum(1 for row in check_rows if row.get(key, '') == value)
    if count != 1:
        raise SystemExit(f'expected one {value} in {path}; found {count}')

print('Gost v131 source-chain integration prepared successfully')
