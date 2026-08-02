# Baptist scan acquisition — current authority

**Дата:** 2026-08-02  
**Authority ID:** `BAPTIST-SCAN-ACQUISITION-AUTHORITY-2026-08-02`  
**Статус:** `REQUEST LANE READY / NO VERIFIED FILE RECEIPTS / NO FALSE ACQUISITION CLAIMS`

## 1. Current inputs

- queue: `БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED/data/NEXT_MICROBATCH.csv`;
- append-only evidence history: `.../data/PROOF_STATUS_LEDGER.csv`;
- policy: `data/baptist-scan-acquisition-policy-v2.json`;
- receipts: `data/baptist-scan-receipts-v1.json`;
- builder/validator: `scripts/build_baptist_scan_request_package.py`.

## 2. Status distinction

```text
CATALOG / HOLDING VERIFIED
≠ FILE RECEIVED
≠ FILE VERIFIED
≠ OCR COMPLETE
≠ QUOTE READY
≠ RIGHTS CLEARED
```

The current receipt ledger contains no established byte-level scan receipts. This statement does not claim that no copy exists in an institution, private Drive or external archive. It means Research has not yet recorded a reproducible receipt satisfying the current policy.

## 3. What is operationally closed

Every row of current `NEXT_MICROBATCH` is machine-converted into a request-ready record with:

- stable record ID;
- exact issue/item designation;
- holding/provider pointer;
- catalog/source URL when available;
- page/copy-variant note;
- next action;
- standardized request wording;
- queue SHA-256;
- package SHA-256 list.

The generated artifact is explicitly `EPHEMERAL_ACTION_ARTIFACT`. It is a request package, not a scan archive.

## 4. Promotion gates

### Received

Required:

- exact file name;
- positive byte size;
- SHA-256;
- received timestamp;
- durable storage receipt.

### File verified

Required:

- format;
- page count;
- visual title-page check;
- issue identity check;
- duplicate/service-manifest rejection.

### OCR complete

Required:

- engine and version;
- OCR text SHA-256;
- OCR page range;
- explicit list of visually unreviewed pages.

### Quote ready

Required:

- page-image visual review;
- stable locator system;
- quote cards;
- rights state and basis.

## 5. Explicit rejections

The following never count as acquired source files:

- a viewer bootstrap `/manifest.json`;
- identical service JSON returned for multiple catalog records;
- a thumbnail without the complete issue;
- a catalog page saved as HTML;
- a Drive filename without hash/readback;
- OCR text without page images;
- a page count without a file.

## 6. External dependency

The remaining work depends on actual delivery or reproducible download from archives/providers. CI can prepare requests and validate receipts; it cannot fabricate institutional scans.

Therefore the honest status is:

```text
REQUEST PREPARATION = CLOSED
RECEIPT SCHEMA = CLOSED
FALSE-POSITIVE GATE = CLOSED
INSTITUTIONAL FILE DELIVERY = EXTERNAL
OCR / VISUAL REVIEW = BLOCKED UNTIL FILE RECEIPT
QUOTE READINESS = BLOCKED UNTIL OCR + VISUAL + RIGHTS
```

## 7. Next valid action

Run the workflow, send the generated exact requests, and append a receipt record only after a real file is received. Any future claim `DOWNLOADED`, `OCR_COMPLETE` or `QUOTE_READY` must pass the same validator.
