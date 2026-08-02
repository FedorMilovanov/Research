# CURRENT AUTHORITY — RUSSIAN BAPTISTS ARCHIVE

**Дата:** 2026-08-02  
**Base authority:** `BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02`  
**Source-class overlay:** `BAPTIST-DERIVATIVE-TRANSCRIPTIONS-2026-08-02`  
**Статус:** current authority для acquisition, source class и proof stages; publication readiness не заявляется.

## 1. Authority composition

1. [`../data/baptist-acquisition-proof-authority-2026-08-02.json`](../data/baptist-acquisition-proof-authority-2026-08-02.json) управляет exact binary identity, acquisition receipts и локальным visual closure «Баптиста» 1909 №11.
2. [`../data/baptist-derivative-transcription-authority-2026-08-02.json`](../data/baptist-derivative-transcription-authority-2026-08-02.json) управляет source class современных Word-транскрипций Шилова и Московской общины.
3. Google Sheets MASTER `1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM` остаётся живым operational inventory. GitHub receipts остаются immutable proof/status authority.

Binary identity = exact Drive ID + SHA-256. Visual identity = source SHA-256 + page locator + visual-card Drive ID + visual-card SHA-256. Source class определяется отдельно от исторического содержания файла.

При конфликте действует `FAIL_CLOSED`: никакого молчаливого повышения статуса.

## 2. Acquisition receipts

### Синичкин — статья о крещении Воронина

- canonical Drive: `1yH-oxjymaDJi4g5Els8xpRiqKFgWDD7V`;
- raw duplicate: `1nPb63h0DLbhx582WFpVPeXS2fH5UFT8O`;
- bytes/pages/SHA: `542143` / `14` / `3d33eb3691dd18f0109028cf1c2c51bb71e21b882dfddfff4393438311498c1c`;
- MASTER: `12 Drive Acquisitions!51`;
- `CANONICAL_DRIVE_REGISTERED / TEXT_LAYER_PRESENT / VISUAL_PENDING / NOT_QUOTE_READY`.

### Biography dossier «Никита Исаевич Воронин»

- canonical Drive: `17O1csxPvxZO0T4Wq0TaRmT69yQ1dkEmT`;
- raw duplicate: `1_PxsBG7YrO58B3yajjNt5MF08WlZDrbV`;
- bytes/pages/SHA: `244468` / `5` / `6d23e500ef19dc457d2f23c06b695ea95e2670759558e0419847022ccc969cc9`;
- MASTER: `12 Drive Acquisitions!52`;
- `CANONICAL_DRIVE_REGISTERED / TEXT_LAYER_PRESENT / VISUAL_PENDING / NOT_QUOTE_READY`.

### Шилов — typed compilation

- canonical Drive: `12PD_RzFXLcKrIYy9ubfskvRKVPj7FlOc`;
- raw duplicate: `1iJhvJ7UjlyhNZAXk586sZzRTa37mKLmf`;
- bytes/pages/SHA: `79460` / `3` / `7c9674b65e15bf76c1833ba0b99b4d735e2c9f3f268351af17f8206516003327`;
- MASTER: `12 Drive Acquisitions!53`, `01 PDF Library!100`;
- acquisition/text: closed;
- source class controlled by derivative overlay.

### Московская община 1923 — typed compilation

- canonical Drive: `1xBpAmUxoERAZJULqnmevSr5zjgReWAGi`;
- raw duplicate: `1ag6DMRa4UO3Pz3SbKRue6LpTR4gL6a1E`;
- bytes/pages/SHA: `119979` / `8` / `c6ef11f8b2fef460bcc083709e0a74fcc6c29a70c353ac73fbff0907126cb8a0`;
- MASTER: `12 Drive Acquisitions!54`, `01 PDF Library!92`;
- acquisition/text: closed;
- source class controlled by derivative overlay.

## 3. Derivative transcription overlay

### SHILOV-LENIN-1919-DERIVATIVE-2026-08-02

Technical/visual result:

- PDF Author: Алексей Синичкин;
- Creator: Microsoft Word;
- CreationDate: 2024-04-18;
- modern A4 typeset text, not a photographed document;
- combines a typed 1919 letter and typed 1920 response/result section;
- no archival folio, signature, stamp or repository shelfmark.

Decision: `DERIVATIVE_TRANSCRIPTION / NOT_ARCHIVAL_FACSIMILE / ARCHIVAL_ORIGINAL_NOT_IDENTIFIED / PRIMARY_QUOTE_NOT_APPROVED`.

### MOSCOW-COMMUNITY-1923-DERIVATIVE-2026-08-02

Technical/visual result:

- PDF Author: Алексей Синичкин;
- Creator: Microsoft Word;
- CreationDate: 2023-01-05;
- eight modern A4 typeset pages;
- no archival page image, signatures, stamp, folio or shelfmark;
- archival original or published primary edition is not identified in the PDF.

Decision: `DERIVATIVE_TRANSCRIPTION / NOT_ARCHIVAL_FACSIMILE / ARCHIVAL_ORIGINAL_NOT_IDENTIFIED / PRIMARY_QUOTE_NOT_APPROVED`.

Allowed for both: navigation, search-target discovery and working paraphrase with explicit derivative disclosure. Forbidden: primary quotation, facsimile claim, original-orthography/signature claim and completeness claim until the original or a verified primary edition is opened.

## 4. Local visual closure — «Баптист» 1909 №11

**Closure ID:** `BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02`.

Source:

- Drive `1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU`;
- bytes/pages/SHA: `9842696` / `22` / `0d54f0c2157e76f621bf2fd65137386ae538a792516c473703179bc3127fba73`;
- scan-only, no text layer.

Visual witnesses:

- printed p.14: Drive `1yOm3KBJ9ujtETUG7u-0hl5ijrGiKuXYG`, SHA `ed381e3ee5764483098fbdda76986953d8d5c7e2ab170e453d38d1a2fd6c23e5`;
- printed p.15: Drive `1v-7bxYeZ6bMsaiVoFgqz5nWUctOtEwA8`, SHA `bb3e78a0deb06b437cbf647c09fada131343eb48174d2fa0630809aca639b2ea`;
- evidence Doc `1zCwFFMTaOcI476aOP_cXSzgdViWNk4VEySJ2G88W6bY`.

Verified:

1. p.14 begins «О Петербургской „свободе“»;
2. pp.14–15 discuss/criticize the evangelical union;
3. p.15 ends with «Ваш меньший брат А. М. Мазаев»;
4. title, continuity, attribution and existence-level critique claim are `VISUAL_PAGE_VERIFIED`.

Still open: full OCR, `BOUNDED_TRANSCRIPTION_PENDING`, general quote-ready, 1912 agreement documents and movement-wide generalization.

## 5. Stage models

### Acquisition

`LOCATOR_ONLY → VIEWER_ACCESSIBLE → BYTES_ACQUIRED → CANONICAL_DRIVE_REGISTERED`

### Proof

`NO_TEXT → TEXT_LAYER_PRESENT → VISUAL_PAGE_VERIFIED → BOUNDED_TRANSCRIPTION_VERIFIED → QUOTE_READY`

### Source class

`UNCLASSIFIED → DERIVATIVE_TRANSCRIPTION | PUBLISHED_PRIMARY_TEXT_EDITION | ARCHIVAL_FACSIMILE`

Old words inside a modern PDF do not make the PDF a primary facsimile.

## 6. Current open gates

- visual page-card set for all 14 pages of the Sinichkin article;
- source-chain pass for the Voronin dossier;
- archival original/edition for the Shilov letter and 1920 response;
- archival original/edition for the Moscow 1923 statement;
- bounded transcription for «Баптист» 1909 №11 pp.14–15;
- OCR for 46 «Баптист» scans and 16 «Утренняя звезда» scans;
- missing physical issues of «Слова истины» and «Братский листок»;
- paid institutional requests;
- book/site publication readiness.

## 7. Supersession boundary

Closed only:

- acquisition/text-layer absence claims for rows 51–54;
- primary-page-unopened blocker for «Баптист» 1909 №11 pp.14–15;
- false `PRIMARY_SOURCE` labels for the exact Shilov and Moscow Word-PDFs.

Not closed: archival provenance, diplomatic transcription, primary-quotation permission or entire corpus completion.

## 8. Machine summary

```text
BASE AUTHORITY: BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02
SOURCE-CLASS OVERLAY: BAPTIST-DERIVATIVE-TRANSCRIPTIONS-2026-08-02
DERIVATIVE TRANSCRIPTIONS: 2
ARCHIVAL FACSIMILES AMONG THEM: 0
PRIMARY QUOTE-READY AMONG THEM: 0
SHILOV PDF: DERIVATIVE TRANSCRIPTION / NOT ARCHIVAL FACSIMILE / PRIMARY QUOTE NOT APPROVED
MOSCOW 1923 PDF: DERIVATIVE TRANSCRIPTION / NOT ARCHIVAL FACSIMILE / PRIMARY QUOTE NOT APPROVED
BAPTIST 1909 NO.11: LOCALIZED VISUAL PAGE VERIFIED
CORPUS-WIDE VISUAL VERIFICATION: NOT CLAIMED
PAID ORDERS: NOT AUTHORIZED
PUBLICATION READINESS: NOT CLAIMED
```
