# Том 76. Rippon 1838 — open-access item verification

**Дата:** 2026-08-04  
**Authority ID:** `GILL-RIPPON-1838-OPEN-ACCESS-VERIFICATION-2026-08-04`  
**Family:** `GILL-FAM-BIOGRAPHICAL-PRIMARY`  
**Machine registry:** `data/gill-rippon-1838-open-access-verification-2026-08-04.json`

```text
REMOTE ITEM VERIFIED = 1
BYTE RECEIPT = 0
EDITION-USABLE ITEMS = 0
QUOTE READY = 0
DIRECT QUOTES APPROVED = 0
```

## 1. Что закрыто этой волной

Для одного конкретного издания Риппона закрыты discovery и edition identity:

- John Rippon, *A Brief Memoir of the Life and Writings of the Late Rev. John Gill, D.D.*;
- London: John Bennett, 4 Three Tun Passage, Newgate Street;
- printer: E. Spettigue, 67 Chancery Lane;
- 1838;
- добавлен текст Benjamin Francis об обстоятельствах смерти Гилла;
- item ID `briefmemoiroflif00ripp`;
- holding institution: Princeton Theological Seminary Library;
- ARK `ark:/13960/t3223d09c`;
- LCCN `36019852`;
- OCLC `10750526`;
- Open Library edition `OL6341134M`.

Canonical item page:

`https://archive.org/details/briefmemoiroflif00ripp`

Remote PDF candidate:

`https://archive.org/download/briefmemoiroflif00ripp/briefmemoiroflif00ripp.pdf`

OCR navigation candidate:

`https://archive.org/stream/briefmemoiroflif00ripp/briefmemoiroflif00ripp_djvu.txt`

## 2. Title-page and pagination review

Remote PDF parsing records:

- PDF object pages: `178`;
- catalog pages: `182`;
- repository page-number confidence: `96`;
- scan density: `400 ppi`;
- PDF object page `6`: title page;
- PDF object page `8`: publisher advertisement;
- PDF object page `10`: memoir body begins.

The title-page text identifies Rippon, John Gill, John Bennett, the London address and the year 1838. The advertisement states that the detached edition was printed verbatim from the memoir prefixed to Gill's nine-volume exposition. This establishes remote edition identity, not local custody.

The `178` PDF-object / `182` catalog-page difference is preserved as a documented boundary and must not be silently normalized into a quotation locator.

## 3. Rights boundary

The work was published in 1838. Rippon died in 1836. Internet Archive presents unrestricted PDF and OCR download options for this item. The registry therefore records the work as a public-domain remote scan while preserving repository terms.

This rights review does not itself prove that a particular local file was received unchanged.

## 4. What remains open

A valid byte receipt still requires all five fields:

1. actual received file name;
2. byte size measured from the received file;
3. SHA-256 computed from the received bytes;
4. received-at timestamp;
5. durable storage receipt.

None of these fields is inferred from a browser preview, OCR endpoint, item metadata, generated Gill PDF, or a filename in Drive/Library.

The runtime used for this wave could verify the remote item and parse the PDF endpoint, but could not materialize the external bytes into durable storage. Therefore the family is advanced only to:

`OPEN_ACCESS_ITEM_VERIFIED_BYTE_RECEIPT_REQUIRED`

It is not advanced to `received`, `edition usable`, `claim usable` or `quote ready`.

## 5. Claim boundary

Until a byte receipt and page-image readback exist:

- OCR remains navigation only;
- no new direct quotation is approved;
- no quote card is created;
- no claim in the Gill corpus may cite this new authority as locally verified page evidence;
- the existing owner documents remain unchanged.

## 6. Next valid action

Materialize the exact PDF or original scan, calculate SHA-256 and byte size, store it durably, review the page image at the intended locator, then update the same family registry. Creating a second receipt ledger or treating the remote URL as custody is forbidden.
