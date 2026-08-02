#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'data/gill-closed-book-families-2026-08-02.json'
DOC=ROOT/'Джон Гилл/75_CLOSED_BOOK_FAMILY_ACQUISITION_AUTHORITY_2026-08-02.md'
errors=[]
def req(c,m):
    if not c: errors.append(m)
try: data=json.loads(REG.read_text(encoding='utf-8'))
except Exception as e: data={}; errors.append(str(e))
req(data.get('schemaVersion')==1,'schema drift')
req(data.get('authorityId')=='GILL-CLOSED-BOOK-FAMILIES-2026-08-02','authority drift')
req(data.get('directQuotesApproved') is False,'direct quotes forbidden')
fams=data.get('families',[])
req(isinstance(fams,list) and len(fams)==7,'exactly seven families required')
ids=[]
for row in fams if isinstance(fams,list) else []:
    req(isinstance(row,dict),'family object required')
    if not isinstance(row,dict): continue
    fid=str(row.get('id','')); ids.append(fid)
    req(fid.startswith('GILL-FAM-'),f'{fid}: bad id')
    req(row.get('status') in {'EXTERNAL_ACQUISITION_REQUIRED','PARTIAL_OPEN_ACCESS_ACQUISITION_REQUIRED','PACKAGE_IDENTITY_UNRESOLVED'},f'{fid}: bad status')
    req(isinstance(row.get('ownerDocuments'),list) and row['ownerDocuments'],f'{fid}: owners required')
    for p in row.get('ownerDocuments',[]): req((ROOT/p).is_file(),f'{fid}: owner missing {p}')
    req(isinstance(row.get('claimScopes'),list) and row['claimScopes'],f'{fid}: claim scopes required')
    req(isinstance(row.get('searchQueries'),list) and len(row['searchQueries'])>=2,f'{fid}: search queries required')
    req(len(str(row.get('acceptance','')))>=50,f'{fid}: acceptance too weak')
req(len(ids)==len(set(ids)),'family IDs must be unique')
req(data.get('receipts')==[],'no unverified receipts may be declared')
counts=data.get('counts',{})
req(counts=={'families':7,'verifiedPackageReceipts':0,'quoteReadyFamilies':0,'directQuotesApproved':0},'count drift')
text=DOC.read_text(encoding='utf-8') if DOC.exists() else ''
for marker in ['FAMILY OWNERSHIP CLOSED','BYTE RECEIPTS = 0','QUOTE-READY FAMILIES = 0','data/gill-closed-book-families-2026-08-02.json']:
    req(marker in text,f'document marker missing: {marker}')
for bad in ['TODO','TBD','PUBLICATION_HOLD']:
    req(bad not in text,f'unresolved marker: {bad}')
if errors:
    print(f'Gill closed-book families: FAIL ({len(errors)})',file=sys.stderr)
    for e in errors: print(f'- {e}',file=sys.stderr)
    raise SystemExit(1)
print('Gill closed-book families: PASS — 7 owned families, 0 unverified receipts')
