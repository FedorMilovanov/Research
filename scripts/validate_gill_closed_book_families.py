#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'data/gill-closed-book-families-2026-08-02.json'
DISC=ROOT/'data/gill-rippon-1838-open-access-verification-2026-08-04.json'
DOC=ROOT/'Джон Гилл/75_CLOSED_BOOK_FAMILY_ACQUISITION_AUTHORITY_2026-08-02.md'
DISC_DOC=ROOT/'Джон Гилл/76_RIPPON_1838_OPEN_ACCESS_VERIFICATION_2026-08-04.md'
errors=[]
def req(c,m):
    if not c: errors.append(m)
def read_json(path):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'{path}: {e}'); return {}
def https_url(value,host=None):
    try:
        parsed=urlparse(str(value))
        return parsed.scheme=='https' and bool(parsed.netloc) and (host is None or parsed.netloc==host)
    except Exception: return False

data=read_json(REG)
req(data.get('schemaVersion')==1,'schema drift')
req(data.get('authorityId')=='GILL-CLOSED-BOOK-FAMILIES-2026-08-02','authority drift')
req(data.get('status')=='CURRENT_REQUEST_READY_REMOTE_ITEM_VERIFIED_NO_BYTE_RECEIPT','matrix status drift')
req(data.get('directQuotesApproved') is False,'direct quotes forbidden')
fams=data.get('families',[])
req(isinstance(fams,list) and len(fams)==7,'exactly seven families required')
ids=[]
allowed_statuses={
    'EXTERNAL_ACQUISITION_REQUIRED',
    'PARTIAL_OPEN_ACCESS_ACQUISITION_REQUIRED',
    'OPEN_ACCESS_ITEM_VERIFIED_BYTE_RECEIPT_REQUIRED',
    'PACKAGE_IDENTITY_UNRESOLVED',
}
for row in fams if isinstance(fams,list) else []:
    req(isinstance(row,dict),'family object required')
    if not isinstance(row,dict): continue
    fid=str(row.get('id','')); ids.append(fid)
    req(fid.startswith('GILL-FAM-'),f'{fid}: bad id')
    req(row.get('status') in allowed_statuses,f'{fid}: bad status')
    req(isinstance(row.get('ownerDocuments'),list) and row['ownerDocuments'],f'{fid}: owners required')
    for p in row.get('ownerDocuments',[]): req((ROOT/p).is_file(),f'{fid}: owner missing {p}')
    req(isinstance(row.get('claimScopes'),list) and row['claimScopes'],f'{fid}: claim scopes required')
    req(isinstance(row.get('searchQueries'),list) and len(row['searchQueries'])>=2,f'{fid}: search queries required')
    req(len(str(row.get('acceptance','')))>=50,f'{fid}: acceptance too weak')
    if fid=='GILL-FAM-BIOGRAPHICAL-PRIMARY':
        req(row.get('status')=='OPEN_ACCESS_ITEM_VERIFIED_BYTE_RECEIPT_REQUIRED','biographical family must remain receipt-bounded')
        req(row.get('discoveryAuthority')=='data/gill-rippon-1838-open-access-verification-2026-08-04.json','biographical discovery authority drift')
    else:
        req('discoveryAuthority' not in row,f'{fid}: unexpected discovery authority')
req(len(ids)==len(set(ids)),'family IDs must be unique')
req(data.get('receipts')==[],'no unverified receipts may be declared')
counts=data.get('counts',{})
req(counts=={'families':7,'verifiedRemoteItems':1,'verifiedPackageReceipts':0,'quoteReadyFamilies':0,'directQuotesApproved':0},'count drift')

verification=read_json(DISC)
req(verification.get('schemaVersion')==1,'Rippon schema drift')
req(verification.get('authorityId')=='GILL-RIPPON-1838-OPEN-ACCESS-VERIFICATION-2026-08-04','Rippon authority drift')
req(verification.get('familyId')=='GILL-FAM-BIOGRAPHICAL-PRIMARY','Rippon family drift')
req(verification.get('status')=='REMOTE_ITEM_VERIFIED_AWAITING_BYTE_RECEIPT','Rippon status must remain receipt-bounded')
req(verification.get('directQuotesApproved') is False,'Rippon direct quotes forbidden')
req(verification.get('quoteReady') is False,'Rippon quote-ready promotion forbidden')
req(verification.get('byteReceiptEstablished') is False,'Rippon byte receipt must remain false')
items=verification.get('items',[])
req(isinstance(items,list) and len(items)==1,'exactly one remote Rippon item required')
if isinstance(items,list) and len(items)==1 and isinstance(items[0],dict):
    item=items[0]
    req(item.get('id')=='GILL-BIO-RIPPON-1838-IA','Rippon item ID drift')
    req(item.get('itemIdentifier')=='briefmemoiroflif00ripp','Rippon IA identifier drift')
    req(https_url(item.get('itemUrl'),'archive.org'),'Rippon item URL invalid')
    edition=item.get('editionIdentity',{})
    req(edition.get('publicationYear')==1838,'Rippon publication year drift')
    req('John Bennett' in str(edition.get('publisher','')),'Rippon publisher identity missing')
    req(edition.get('lccn')=='36019852','Rippon LCCN drift')
    req(edition.get('oclc')=='10750526','Rippon OCLC drift')
    remote=item.get('remoteFiles',{})
    pdf=remote.get('pdf',{}) if isinstance(remote,dict) else {}
    ocr=remote.get('ocrText',{}) if isinstance(remote,dict) else {}
    req(pdf.get('candidateFileName')=='briefmemoiroflif00ripp.pdf','Rippon PDF filename drift')
    req(https_url(pdf.get('url'),'archive.org'),'Rippon PDF URL invalid')
    req(pdf.get('availabilityObserved') is True,'Rippon PDF availability not observed')
    req(pdf.get('pdfObjectPages')==178,'Rippon PDF page count drift')
    req(ocr.get('candidateFileName')=='briefmemoiroflif00ripp_djvu.txt','Rippon OCR filename drift')
    req(https_url(ocr.get('url'),'archive.org'),'Rippon OCR URL invalid')
    req(ocr.get('availabilityObserved') is True,'Rippon OCR availability not observed')
    req(ocr.get('role')=='navigation_only','Rippon OCR must remain navigation only')
    observed=item.get('remoteVerification',{})
    req(observed.get('itemMetadataReviewed') is True,'Rippon metadata review missing')
    req(observed.get('catalogPages')==182,'Rippon catalog page count drift')
    req(observed.get('titlePageTextReviewed') is True,'Rippon title-page text review missing')
    req(observed.get('titlePageImageReviewed') is False,'Rippon title-page image must not be claimed')
    req(observed.get('advertisementConfirmsVerbatimReprint') is True,'Rippon advertisement evidence missing')
    req(observed.get('pageCountDifferenceDocumented') is True,'Rippon page-count boundary missing')
    rights=item.get('rights',{})
    req(rights.get('state')=='PUBLIC_DOMAIN_WORK_REMOTE_SCAN_DOWNLOADABLE','Rippon rights state drift')
    req(rights.get('repositoryTermsStillApply') is True,'repository terms boundary missing')
    receipt=item.get('receipt',{})
    req(receipt.get('state')=='NOT_RECEIVED','Rippon receipt state drift')
    for field in ['file_name','byte_size','sha256','received_at','durable_storage_receipt']:
        req(receipt.get(field) is None,f'Rippon {field} must remain null before receipt')
    req(item.get('receiptGaps')==['file_name','byte_size','sha256','received_at','durable_storage_receipt'],'Rippon receipt gap set drift')
else:
    req(False,'Rippon item object required')
req(verification.get('counts')=={'remoteItemsVerified':1,'byteReceipts':0,'editionUsableItems':0,'quoteReadyItems':0,'directQuotesApproved':0},'Rippon count drift')

text=DOC.read_text(encoding='utf-8') if DOC.exists() else ''
for marker in ['FAMILY OWNERSHIP CLOSED','BYTE RECEIPTS = 0','QUOTE-READY FAMILIES = 0','data/gill-closed-book-families-2026-08-02.json']:
    req(marker in text,f'document marker missing: {marker}')
disc_text=DISC_DOC.read_text(encoding='utf-8') if DISC_DOC.exists() else ''
for marker in ['REMOTE ITEM VERIFIED = 1','BYTE RECEIPT = 0','EDITION-USABLE ITEMS = 0','QUOTE READY = 0','DIRECT QUOTES APPROVED = 0','data/gill-rippon-1838-open-access-verification-2026-08-04.json','OPEN_ACCESS_ITEM_VERIFIED_BYTE_RECEIPT_REQUIRED']:
    req(marker in disc_text,f'Rippon document marker missing: {marker}')
for bad in ['TODO','TBD','PUBLICATION_HOLD']:
    req(bad not in text,f'unresolved marker in family authority: {bad}')
    req(bad not in disc_text,f'unresolved marker in Rippon authority: {bad}')
if errors:
    print(f'Gill closed-book families: FAIL ({len(errors)})',file=sys.stderr)
    for e in errors: print(f'- {e}',file=sys.stderr)
    raise SystemExit(1)
print('Gill closed-book families: PASS — 7 families, 1 remote item, 0 byte receipts, 0 quote-ready items')
