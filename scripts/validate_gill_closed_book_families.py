#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'data/gill-closed-book-families-2026-08-02.json'
DISC=ROOT/'data/gill-rippon-1838-open-access-verification-2026-08-04.json'
DOC=ROOT/'Джон Гилл/75_CLOSED_BOOK_FAMILY_ACQUISITION_AUTHORITY_2026-08-02.md'
DISC_DOC=ROOT/'Джон Гилл/76_RIPPON_1838_OPEN_ACCESS_VERIFICATION_2026-08-04.md'
EXPECTED_SHA='362019ee851280e14eb4c6cd8bca70a30df957af225ac56c7c6d95bbaf461792'
EXPECTED_SIZE=9297102
EXPECTED_DRIVE_ID='1q4IFETrDu9bH8mGMIPQO38qQTVwxjxMu'
EXPECTED_STORED_NAME='GILL-BIO-RIPPON-1838-IA__briefmemoiroflif00ripp__sha256-362019ee851280e1.pdf'
errors=[]

def req(condition,message):
    if not condition: errors.append(message)

def read_json(path):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception as error: errors.append(f'{path}: {error}'); return {}

def https_url(value,host=None):
    try:
        parsed=urlparse(str(value))
        return parsed.scheme=='https' and bool(parsed.netloc) and (host is None or parsed.netloc==host)
    except Exception: return False

def valid_timestamp(value):
    return isinstance(value,str) and bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z',value))

def validate_storage_receipt(storage,prefix,full=False):
    req(isinstance(storage,dict),f'{prefix}: storage receipt object required')
    if not isinstance(storage,dict): return
    req(storage.get('provider')=='Google Drive',f'{prefix}: storage provider drift')
    req(storage.get('file_id')==EXPECTED_DRIVE_ID,f'{prefix}: Drive file ID drift')
    req(storage.get('stored_name')==EXPECTED_STORED_NAME,f'{prefix}: stored name drift')
    req(storage.get('created_at')=='2026-08-03T23:49:15.863Z',f'{prefix}: created timestamp drift')
    req(storage.get('shared') is False,f'{prefix}: receipt must preserve private/not-shared state')
    if full:
        req(storage.get('mime_type')=='application/pdf',f'{prefix}: MIME drift')
        req(storage.get('byte_size')==EXPECTED_SIZE,f'{prefix}: stored size drift')
        req(storage.get('modified_at')=='2026-08-03T23:49:15.863Z',f'{prefix}: modified timestamp drift')
        req(storage.get('parent_id')=='0AL754uQ3lkWPUk9PVA',f'{prefix}: parent ID drift')
        req(storage.get('metadata_readback') is True,f'{prefix}: metadata readback required')

data=read_json(REG)
req(data.get('schemaVersion')==1,'schema drift')
req(data.get('authorityId')=='GILL-CLOSED-BOOK-FAMILIES-2026-08-02','authority drift')
req(data.get('status')=='CURRENT_REQUEST_READY_ONE_DURABLE_FILE_RECEIPT_NO_QUOTES','matrix status drift')
req(data.get('lastVerifiedAt')=='2026-08-04','matrix verification date drift')
req(data.get('directQuotesApproved') is False,'direct quotes forbidden')
policy=data.get('receiptPolicy',{})
req(policy.get('receivedRequires')==['file_name','byte_size','sha256','received_at','durable_storage_receipt'],'received policy drift')
req(policy.get('driveNameAloneIsReceipt') is False,'Drive-name-alone prohibition drift')
req(policy.get('previewAloneIsFullText') is False,'preview boundary drift')
req(policy.get('bibliographyAloneSupportsClaim') is False,'bibliography boundary drift')

fams=data.get('families',[])
req(isinstance(fams,list) and len(fams)==7,'exactly seven families required')
ids=[]
allowed_statuses={
    'EXTERNAL_ACQUISITION_REQUIRED',
    'PARTIAL_OPEN_ACCESS_ACQUISITION_REQUIRED',
    'DURABLE_BYTE_RECEIPT_ESTABLISHED_EDITION_VERIFIED_CLAIM_FOLLOWUP_REQUIRED',
    'PACKAGE_IDENTITY_UNRESOLVED',
}
for row in fams if isinstance(fams,list) else []:
    req(isinstance(row,dict),'family object required')
    if not isinstance(row,dict): continue
    fid=str(row.get('id','')); ids.append(fid)
    req(fid.startswith('GILL-FAM-'),f'{fid}: bad id')
    req(row.get('status') in allowed_statuses,f'{fid}: bad status')
    req(isinstance(row.get('ownerDocuments'),list) and row['ownerDocuments'],f'{fid}: owners required')
    for owner in row.get('ownerDocuments',[]): req((ROOT/owner).is_file(),f'{fid}: owner missing {owner}')
    req(isinstance(row.get('claimScopes'),list) and row['claimScopes'],f'{fid}: claim scopes required')
    req(isinstance(row.get('searchQueries'),list) and len(row['searchQueries'])>=2,f'{fid}: search queries required')
    req(len(str(row.get('acceptance','')))>=50,f'{fid}: acceptance too weak')
    if fid=='GILL-FAM-BIOGRAPHICAL-PRIMARY':
        req(row.get('status')=='DURABLE_BYTE_RECEIPT_ESTABLISHED_EDITION_VERIFIED_CLAIM_FOLLOWUP_REQUIRED','biographical family receipt status drift')
        req(row.get('discoveryAuthority')=='data/gill-rippon-1838-open-access-verification-2026-08-04.json','biographical discovery authority drift')
    else:
        req('discoveryAuthority' not in row,f'{fid}: unexpected discovery authority')
req(len(ids)==len(set(ids)),'family IDs must be unique')

receipts=data.get('receipts',[])
req(isinstance(receipts,list) and len(receipts)==1,'exactly one verified file receipt required')
if isinstance(receipts,list) and len(receipts)==1 and isinstance(receipts[0],dict):
    receipt=receipts[0]
    req(receipt.get('receiptId')=='GILL-RECEIPT-RIPPON-1838-IA-20260804','receipt ID drift')
    req(receipt.get('familyId')=='GILL-FAM-BIOGRAPHICAL-PRIMARY','receipt family drift')
    req(receipt.get('itemId')=='GILL-BIO-RIPPON-1838-IA','receipt item drift')
    req(receipt.get('authority')=='data/gill-rippon-1838-open-access-verification-2026-08-04.json','receipt authority drift')
    req(receipt.get('file_name')=='briefmemoiroflif00ripp.pdf','receipt filename drift')
    req(receipt.get('byte_size')==EXPECTED_SIZE,'receipt byte size drift')
    req(receipt.get('sha256')==EXPECTED_SHA,'receipt SHA-256 drift')
    req(valid_timestamp(receipt.get('received_at')),'receipt received timestamp invalid')
    validate_storage_receipt(receipt.get('durable_storage_receipt'),'family receipt')
    req(receipt.get('editionUsable') is True,'edition usability required')
    req(receipt.get('quoteReady') is False,'quote-ready promotion forbidden')
else:
    req(False,'receipt object required')
req(data.get('counts')=={
    'families':7,
    'verifiedRemoteItems':1,
    'verifiedFileReceipts':1,
    'verifiedPackageReceipts':0,
    'quoteReadyFamilies':0,
    'directQuotesApproved':0,
},'family count drift')

verification=read_json(DISC)
req(verification.get('schemaVersion')==1,'Rippon schema drift')
req(verification.get('authorityId')=='GILL-RIPPON-1838-OPEN-ACCESS-VERIFICATION-2026-08-04','Rippon authority drift')
req(verification.get('familyId')=='GILL-FAM-BIOGRAPHICAL-PRIMARY','Rippon family drift')
req(verification.get('status')=='BYTE_RECEIPT_ESTABLISHED_EDITION_VERIFIED_CLAIM_FOLLOWUP_REQUIRED','Rippon receipt status drift')
req(verification.get('lastVerifiedAt')=='2026-08-04','Rippon verification date drift')
req(verification.get('directQuotesApproved') is False,'Rippon direct quotes forbidden')
req(verification.get('quoteReady') is False,'Rippon quote-ready promotion forbidden')
req(verification.get('byteReceiptEstablished') is True,'Rippon byte receipt must be established')
items=verification.get('items',[])
req(isinstance(items,list) and len(items)==1,'exactly one Rippon item required')
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
    req(observed.get('pdfInspectionReviewed') is True,'Rippon PDF inspection missing')
    req(observed.get('pdfEncrypted') is False,'Rippon PDF encryption drift')
    req(observed.get('pdfJavaScript') is False,'Rippon PDF JavaScript drift')
    req(observed.get('pdfAttachments')==0,'Rippon PDF attachment drift')
    req(observed.get('titlePageTextReviewed') is True,'Rippon title-page text review missing')
    req(observed.get('titlePagePdfIndex')==6,'Rippon title-page locator drift')
    req(observed.get('titlePageImageReviewed') is True,'Rippon title-page image review required')
    req(observed.get('advertisementPdfIndex')==8,'Rippon advertisement locator drift')
    req(observed.get('advertisementImageReviewed') is True,'Rippon advertisement image review required')
    req(observed.get('advertisementConfirmsVerbatimReprint') is True,'Rippon advertisement evidence missing')
    req(observed.get('pageCountDifferenceDocumented') is True,'Rippon page-count boundary missing')
    req(observed.get('locatorMapReviewed') is True,'Rippon edition locator map required')
    req(observed.get('stableLocatorExamples')==[
        'PDF object page 6: title page',
        'PDF object pages 8-9: publisher advertisement',
        'PDF object page 10: memoir text begins',
    ],'Rippon locator map drift')
    rights=item.get('rights',{})
    req(rights.get('state')=='PUBLIC_DOMAIN_WORK_REMOTE_SCAN_DOWNLOADABLE','Rippon rights state drift')
    req(rights.get('repositoryTermsStillApply') is True,'repository terms boundary missing')
    receipt=item.get('receipt',{})
    req(receipt.get('state')=='RECEIVED_DURABLE_DRIVE','Rippon receipt state drift')
    req(receipt.get('file_name')=='briefmemoiroflif00ripp.pdf','Rippon received filename drift')
    req(receipt.get('byte_size')==EXPECTED_SIZE,'Rippon received byte size drift')
    req(receipt.get('sha256')==EXPECTED_SHA,'Rippon received SHA-256 drift')
    req(receipt.get('received_at')=='2026-08-03T23:46:51.303Z','Rippon received timestamp drift')
    validate_storage_receipt(receipt.get('durable_storage_receipt'),'Rippon receipt',full=True)
    req(item.get('receiptGaps')==[],'Rippon receipt gap set must be empty')
else:
    req(False,'Rippon item object required')
req(verification.get('counts')=={
    'remoteItemsVerified':1,
    'byteReceipts':1,
    'editionUsableItems':1,
    'quoteReadyItems':0,
    'directQuotesApproved':0,
},'Rippon count drift')

text=DOC.read_text(encoding='utf-8') if DOC.exists() else ''
for marker in [
    'FAMILY OWNERSHIP CLOSED',
    'DURABLE FILE RECEIPTS = 1',
    'VERIFIED PACKAGE RECEIPTS = 0',
    'QUOTE-READY FAMILIES = 0',
    'data/gill-closed-book-families-2026-08-02.json',
]: req(marker in text,f'document marker missing: {marker}')
disc_text=DISC_DOC.read_text(encoding='utf-8') if DISC_DOC.exists() else ''
for marker in [
    'REMOTE ITEM VERIFIED = 1',
    'BYTE RECEIPT = 1',
    'EDITION-USABLE ITEMS = 1',
    'QUOTE READY = 0',
    'DIRECT QUOTES APPROVED = 0',
    EXPECTED_SHA,
    EXPECTED_DRIVE_ID,
    'data/gill-rippon-1838-open-access-verification-2026-08-04.json',
    'DURABLE_BYTE_RECEIPT_ESTABLISHED_EDITION_VERIFIED_CLAIM_FOLLOWUP_REQUIRED',
]: req(marker in disc_text,f'Rippon document marker missing: {marker}')
for bad in ['TODO','TBD','PUBLICATION_HOLD']:
    req(bad not in text,f'unresolved marker in family authority: {bad}')
    req(bad not in disc_text,f'unresolved marker in Rippon authority: {bad}')
if errors:
    print(f'Gill closed-book families: FAIL ({len(errors)})',file=sys.stderr)
    for error in errors: print(f'- {error}',file=sys.stderr)
    raise SystemExit(1)
print('Gill closed-book families: PASS — 7 families, 1 durable file receipt, 1 edition-usable item, 0 quote-ready items')
