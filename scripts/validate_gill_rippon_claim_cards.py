#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'data/gill-rippon-1838-claim-cards-2026-08-04.json'
RECEIPT = ROOT / 'data/gill-rippon-1838-open-access-verification-2026-08-04.json'
OWNER = ROOT / 'Джон Гилл/17_BIOGRAPHICAL_PRIMARY_SOURCES_AND_VERIFICATION.md'
DOC = ROOT / 'Джон Гилл/77_RIPPON_1838_BIRTH_AND_PARENTS_CLAIM_CARD_2026-08-04.md'

PDF_SHA = '362019ee851280e14eb4c6cd8bca70a30df957af225ac56c7c6d95bbaf461792'
QUOTE_SHA = 'ba341d1321897649e616f94a1693d21ab5fc632010bc4f839b8c49aa823e2587'
PRIMARY_IMAGE_SHA = '0a7fa164c13ae653ee9d6ab754057224cf266674536070a49e78a48d31eb9b86'
CONTEXT_IMAGE_SHA = '98f923d831023617ee3d8c99c6663c34edfcc44470dc7a08e6270fae64583590'
DRIVE_ID = '1q4IFETrDu9bH8mGMIPQO38qQTVwxjxMu'
EXPECTED_QUOTE = (
    'The subject of this Memoir was born at Kettering, in Northamptonshire, '
    'Nov. 23, o. s. 1697, of amiable and serious parents, Edward Gill, and '
    'Elizabeth his wife, whose maiden name was Walker.'
)
EXPECTED_PARAPHRASE = (
    'Джон Гилл родился в Кеттеринге, Нортгемптоншир, 23 ноября 1697 года по '
    'старому стилю; его родителями были Эдвард Гилл и Элизабет, урождённая Уолкер.'
)

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except Exception as error:
        errors.append(f'{path.relative_to(ROOT)}: {error}')
        return {}
    if not isinstance(value, dict):
        errors.append(f'{path.relative_to(ROOT)}: root object required')
        return {}
    return value


def is_https(value: object, host: str | None = None) -> bool:
    try:
        parsed = urlparse(str(value))
    except Exception:
        return False
    return parsed.scheme == 'https' and bool(parsed.netloc) and (host is None or parsed.netloc == host)


registry = read_json(REGISTRY)
receipt = read_json(RECEIPT)

require(registry.get('schemaVersion') == 1, 'claim-card schema drift')
require(registry.get('authorityId') == 'GILL-RIPPON-1838-CLAIM-CARDS-2026-08-04', 'claim-card authority drift')
require(registry.get('status') == 'ONE_PAGE_IMAGE_REVIEWED_CLAIM_USABLE_PARAPHRASE_ONLY', 'claim-card status drift')
require(registry.get('generatedAt') == '2026-08-04', 'claim-card generated date drift')
require(registry.get('lastVerifiedAt') == '2026-08-04', 'claim-card verification date drift')
require(registry.get('sourceItemId') == 'GILL-BIO-RIPPON-1838-IA', 'source item drift')
require(registry.get('receiptAuthority') == 'data/gill-rippon-1838-open-access-verification-2026-08-04.json', 'receipt authority drift')
require(registry.get('ownerDocument') == 'Джон Гилл/17_BIOGRAPHICAL_PRIMARY_SOURCES_AND_VERIFICATION.md', 'owner document drift')
require(registry.get('directQuoteApproved') is False, 'registry direct quotation must remain unapproved')
require(registry.get('productPublicationApproved') is False, 'registry Product publication must remain unapproved')
require(OWNER.is_file(), 'biographical owner document missing')
require(DOC.is_file(), 'claim-card document missing')

cards = registry.get('cards')
require(isinstance(cards, list) and len(cards) == 1, 'exactly one claim card required')
if isinstance(cards, list) and len(cards) == 1 and isinstance(cards[0], dict):
    card = cards[0]
    require(card.get('id') == 'GILL-RIPPON-1838-CLAIM-BIRTH-PARENTS-001', 'claim-card ID drift')
    require(card.get('claimState') == 'CLAIM_USABLE_PARAPHRASE_ONLY', 'claim state drift')
    require(card.get('approvedParaphraseRu') == EXPECTED_PARAPHRASE, 'approved paraphrase drift')

    source = card.get('source', {})
    require(source.get('pdfFileName') == 'briefmemoiroflif00ripp.pdf', 'PDF filename drift')
    require(source.get('pdfByteSize') == 9297102, 'PDF byte size drift')
    require(source.get('pdfSha256') == PDF_SHA, 'PDF SHA-256 drift')
    require(source.get('driveFileId') == DRIVE_ID, 'Drive file ID drift')
    require(is_https(source.get('itemUrl'), 'archive.org'), 'Archive item URL invalid')

    locator = card.get('locator', {})
    require(locator.get('pdfObjectIndexZeroBased') == 10, 'zero-based PDF locator drift')
    require(locator.get('pdfHumanPageOneBased') == 11, 'human PDF locator drift')
    require(locator.get('printedPage') == '1', 'printed-page locator drift')
    require(locator.get('contextPdfObjectIndexesZeroBased') == [10, 11], 'context PDF locator drift')
    require(locator.get('contextPrintedPages') == ['1', '2'], 'context printed-page locator drift')

    image = card.get('pageImageReview', {})
    require(image.get('reviewed') is True, 'page-image review required')
    require(image.get('renderDpi') == 220, 'render DPI drift')
    require(image.get('primaryImageSha256') == PRIMARY_IMAGE_SHA, 'primary page-image SHA drift')
    require(image.get('contextImageSha256') == CONTEXT_IMAGE_SHA, 'context page-image SHA drift')
    require(len(str(image.get('primaryImageFinding', ''))) >= 80, 'primary image finding too weak')
    require(len(str(image.get('contextImageFinding', ''))) >= 80, 'context image finding too weak')

    transcription = card.get('transcription', {})
    text = transcription.get('text')
    require(text == EXPECTED_QUOTE, 'transcription text drift')
    if isinstance(text, str):
        require(hashlib.sha256(text.encode('utf-8')).hexdigest() == QUOTE_SHA, 'computed transcription SHA drift')
        require(len(text.split()) == 32, 'computed transcription word count drift')
    require(transcription.get('sha256') == QUOTE_SHA, 'stored transcription SHA drift')
    require(transcription.get('wordCount') == 32, 'stored transcription word count drift')
    require(transcription.get('role') == 'research_evidence_not_product_quote', 'transcription role drift')
    require(transcription.get('normalizedLongS') is False, 'unexpected long-s normalization claim')

    context = card.get('contextWindow', {})
    require(context.get('reviewed') is True, 'context-window review required')
    require(len(str(context.get('before', ''))) >= 80, 'before-context summary too weak')
    require(len(str(context.get('after', ''))) >= 80, 'after-context summary too weak')

    boundary = card.get('supportBoundary', {})
    supports = boundary.get('supports', [])
    excludes = boundary.get('doesNotSupport', [])
    require(isinstance(supports, list) and len(supports) == 4, 'exact support set required')
    require(isinstance(excludes, list) and len(excludes) >= 4, 'explicit exclusion set required')
    require('any Product publication or direct quotation' in excludes, 'Product/direct-quote exclusion missing')

    rights = card.get('rights', {})
    require(rights.get('state') == 'PUBLIC_DOMAIN_WORK_REMOTE_SCAN_DOWNLOADABLE', 'rights state drift')
    require(rights.get('repositoryTermsStillApply') is True, 'repository terms boundary missing')

    approval = card.get('approval', {})
    require(approval == {
        'claimUsable': True,
        'paraphraseApproved': True,
        'directQuoteApproved': False,
        'productPublicationApproved': False,
    }, 'approval boundary drift')
else:
    require(False, 'claim-card object required')

require(registry.get('counts') == {
    'cards': 1,
    'pageImageReviewed': 1,
    'claimUsableScopes': 1,
    'paraphraseApproved': 1,
    'directQuoteApproved': 0,
    'productPublicationApproved': 0,
}, 'claim-card count drift')
require('paraphrase' in str(registry.get('boundary', '')).lower(), 'registry paraphrase boundary missing')

require(receipt.get('authorityId') == 'GILL-RIPPON-1838-OPEN-ACCESS-VERIFICATION-2026-08-04', 'receipt authority missing')
require(receipt.get('byteReceiptEstablished') is True, 'byte receipt must remain established')
require(receipt.get('quoteReady') is False, 'item-wide quote readiness must remain false')
require(receipt.get('directQuotesApproved') is False, 'receipt-wide direct quote approval must remain false')
items = receipt.get('items', [])
require(isinstance(items, list) and len(items) == 1, 'one receipt item required')
if isinstance(items, list) and len(items) == 1 and isinstance(items[0], dict):
    item = items[0]
    require(item.get('id') == registry.get('sourceItemId'), 'claim-card/receipt item mismatch')
    received = item.get('receipt', {})
    require(received.get('sha256') == PDF_SHA, 'claim-card/receipt PDF SHA mismatch')
    durable = received.get('durable_storage_receipt', {})
    require(durable.get('file_id') == DRIVE_ID, 'claim-card/receipt Drive ID mismatch')

text = DOC.read_text(encoding='utf-8') if DOC.exists() else ''
for marker in [
    'CLAIM USABLE = PARAPHRASE ONLY',
    'DIRECT QUOTE APPROVED = 0',
    'PRODUCT PUBLICATION APPROVED = 0',
    'GILL-RIPPON-1838-CLAIM-BIRTH-PARENTS-001',
    PDF_SHA,
    QUOTE_SHA,
    DRIVE_ID,
    'printed page 1',
    'PDF object index 10',
    EXPECTED_PARAPHRASE,
]:
    require(marker in text, f'claim-card document marker missing: {marker}')
for forbidden in ['QUOTE READY = 1', 'DIRECT QUOTE APPROVED = 1', 'PRODUCT PUBLICATION APPROVED = 1', 'TODO', 'TBD']:
    require(forbidden not in text, f'forbidden claim-card marker: {forbidden}')

owner_text = OWNER.read_text(encoding='utf-8') if OWNER.exists() else ''
require('N1' in owner_text and 'маiden' not in owner_text, 'owner document N1 marker missing or corrupted')
require('Мать Гилла — Элизабет, урождённая Уолкер' in owner_text, 'owner claim text missing')

if errors:
    print(f'Gill Rippon claim cards: FAIL ({len(errors)})')
    for error in errors:
        print(f'- {error}')
    raise SystemExit(1)

print('Gill Rippon claim cards: PASS — 1 page-image-reviewed paraphrase-only claim, 0 direct quotes, 0 Product approvals')
