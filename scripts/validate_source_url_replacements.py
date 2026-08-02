#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'data/source-url-replacements-2026-08-02.json'
DOC=ROOT/'SOURCE_LIBRARY/CURRENT_SOURCE_URL_AUTHORITY_2026-08-02.md'
errors=[]
def req(c,m):
    if not c: errors.append(m)
try: data=json.loads(REG.read_text(encoding='utf-8'))
except Exception as e: data={}; errors.append(str(e))
req(data.get('schemaVersion')==1,'schema drift')
req(data.get('authorityId')=='SOURCE-URL-REPLACEMENTS-2026-08-02','authority drift')
rows=data.get('records',[])
req(isinstance(rows,list) and len(rows)==8,'exactly eight records required')
ids=[]; old=[]; new=[]
for row in rows if isinstance(rows,list) else []:
    req(isinstance(row,dict),'record object required')
    if not isinstance(row,dict): continue
    rid=str(row.get('id','')); ids.append(rid)
    req(rid.startswith('URLR-'),f'{rid}: bad id')
    status=row.get('status')
    req(status in {'REPLACE','REPLACE_WITH_RIGHTS_HOLD','REPLACE_WITH_VERSION_PIN','ADD_VERSION_HISTORY'},f'{rid}: bad status')
    old_url=str(row.get('oldUrl','')); new_url=str(row.get('newUrl',''))
    if old_url: old.append(old_url)
    new.append(new_url)
    p=urlparse(new_url); req(p.scheme=='https' and bool(p.netloc),f'{rid}: HTTPS replacement required')
    req(row.get('sourceClass') in {'A1','A2'},f'{rid}: source class drift')
    req(row.get('rightsEffect') is not None,f'{rid}: rights effect required')
    req(len(str(row.get('note','')))>=35,f'{rid}: note too weak')
req(len(ids)==len(set(ids)),'duplicate IDs')
req(len(old)==len(set(old)),'duplicate old URLs')
req(len(new)==len(set(new)),'duplicate new URLs')
rights=data.get('rightsBoundaries',{})
for key in ['duncan','qumran','feb','ccel']: req(bool(str(rights.get(key,''))),f'rights boundary missing: {key}')
req(data.get('counts')=={'confirmedReplacements':7,'addedVersionHistory':1,'rightsHoldsPreserved':3,'versionPins':1},'count drift')
text=DOC.read_text(encoding='utf-8') if DOC.exists() else ''
for marker in ['SOURCE-URL-REPLACEMENTS-2026-08-02','RIGHTS UNCHANGED','ITEM_LEVEL_RIGHTS_REVIEW_REQUIRED','НЕ ФАКСИМИЛЕ','REMAINING TRUE-DEAD QUEUE = ACTIVE ITEM-BY-ITEM RESEARCH']:
    req(marker in text,f'document marker missing: {marker}')
for bad in ['TODO','TBD','PUBLICATION_HOLD']:
    req(bad not in text,f'unresolved marker: {bad}')
if errors:
    print(f'Source URL replacements: FAIL ({len(errors)})',file=sys.stderr)
    for e in errors: print(f'- {e}',file=sys.stderr)
    raise SystemExit(1)
print('Source URL replacements: PASS — 7 replacements, 1 version-history endpoint, rights preserved')
