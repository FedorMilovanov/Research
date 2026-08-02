# CURRENT AUTHORITY — RUSSIAN BAPTISTS ARCHIVE

**Дата:** 2026-08-02  
**Authority ID:** `BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02`  
**Статус:** текущая authority для acquisition, source-class и proof stages; **не** утверждает публикационную готовность корпуса.

## 1. Как устроена authority

У проекта два согласованных, но не взаимозаменяемых слоя:

1. **Google Sheets MASTER** (`1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM`) — живой операционный каталог файлов, ссылок, приобретений, dossier-state и заявок. Inventory rows добавляются append-only; явно названные dossier/library cells могут обновляться idempotent targeted update.
2. **GitHub current authority + immutable receipts** — точные значения статусов, правила повышения evidence и неизменяемая фиксация Drive ID, страниц, байтов, SHA-256, source class и visual witnesses.

Физический объект определяется парой **exact Drive ID + SHA-256**. Visual closure дополнительно требует source SHA-256, точный page locator и visual-card Drive ID + SHA-256. Source class определяется отдельно от исторического содержания: существование старого текста не превращает современную транскрипцию в archival facsimile.

При расхождении действует `FAIL_CLOSED`: статус не повышается и конфликт не разрешается молча.

Машинная authority: [`../data/baptist-acquisition-proof-authority-2026-08-02.json`](../data/baptist-acquisition-proof-authority-2026-08-02.json).

Immutable receipts:

- [`drive_acquisition_delta_2026-08-02.csv`](drive_acquisition_delta_2026-08-02.csv) — rows 51–52;
- [`drive_acquisition_delta_2026-08-02-b.csv`](drive_acquisition_delta_2026-08-02-b.csv) — row 53;
- [`BAPTIST_1909_NO11_MAZAEV_VISUAL_CLOSURE_2026-08-02.md`](BAPTIST_1909_NO11_MAZAEV_VISUAL_CLOSURE_2026-08-02.md);
- [`SHILOV_LENIN_1919_DERIVATIVE_CLASSIFICATION_2026-08-02.md`](SHILOV_LENIN_1919_DERIVATIVE_CLASSIFICATION_2026-08-02.md).

## 2. Закрытые acquisition-записи

### Синичкин — «К вопросу о крещении первого русского баптиста»

- canonical Drive ID: `1yH-oxjymaDJi4g5Els8xpRiqKFgWDD7V`;
- raw provenance duplicate: `1nPb63h0DLbhx582WFpVPeXS2fH5UFT8O`;
- bytes/pages/SHA-256: `542143` / `14` / `3d33eb3691dd18f0109028cf1c2c51bb71e21b882dfddfff4393438311498c1c`;
- MASTER: `12 Drive Acquisitions!51`;
- acquisition: `CANONICAL_DRIVE_REGISTERED`;
- proof: `TEXT_LAYER_PRESENT`;
- source class: `MODERN_SCHOLARLY_ARTICLE`;
- visual: `PENDING`;
- quote-ready: `NOT_APPROVED`.

### «Никита Исаевич Воронин» — biography dossier

- canonical Drive ID: `17O1csxPvxZO0T4Wq0TaRmT69yQ1dkEmT`;
- raw provenance duplicate: `1_PxsBG7YrO58B3yajjNt5MF08WlZDrbV`;
- bytes/pages/SHA-256: `244468` / `5` / `6d23e500ef19dc457d2f23c06b695ea95e2670759558e0419847022ccc969cc9`;
- MASTER: `12 Drive Acquisitions!52`;
- acquisition: `CANONICAL_DRIVE_REGISTERED`;
- proof: `TEXT_LAYER_PRESENT`;
- source class: `DERIVATIVE_BIOGRAPHY_DOSSIER`;
- source-chain visual pass: `PENDING`;
- quote-ready: `NOT_APPROVED`.

## 3. Source-class closure — письмо Шилова Ленину

**Classification ID:** `SHILOV-LENIN-1919-DERIVATIVE-2026-08-02`.

Exact file:

- canonical Drive ID: `12PD_RzFXLcKrIYy9ubfskvRKVPj7FlOc`;
- raw provenance duplicate: `1iJhvJ7UjlyhNZAXk586sZzRTa37mKLmf`;
- canonical folder: `02 — LETTERS, PETITIONS & STATE DOCUMENTS` (`1-vmWwdvYcF8RqFdPr4aWO5REp_mic9Aq`);
- bytes/pages/SHA-256: `79460` / `3` / `7c9674b65e15bf76c1833ba0b99b4d735e2c9f3f268351af17f8206516003327`;
- MASTER acquisition: `12 Drive Acquisitions!53`;
- MASTER library class: `01 PDF Library!100`.

Technical/visual facts:

- PDF Author: `Алексей Синичкин`;
- Creator: `Microsoft Word`;
- CreationDate: `2024-04-18`;
- modern A4 typeset pages and clean text layer;
- contains a typed 1919 letter text and a typed 1920 response/result section;
- contains no photographed archival page, original signature, stamp, folio or repository shelfmark.

Decision:

- acquisition: `CANONICAL_DRIVE_REGISTERED`;
- proof: `TEXT_LAYER_PRESENT`;
- source class: `DERIVATIVE_TRANSCRIPTION`;
- facsimile: `NOT_ARCHIVAL_FACSIMILE`;
- archival provenance/original: `NOT_IDENTIFIED`;
- navigation/paraphrase with explicit derivative disclosure: `ALLOWED`;
- primary quotation: `NOT_APPROVED`.

The former `PRIMARY_SOURCE` label for this exact 2024 PDF has been removed. This does not declare the underlying 1919 letter false; it prevents the derivative file from impersonating an archival witness.

## 4. Локальный visual closure — «Баптист» 1909 №11

**Closure ID:** `BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02`.

Source identity:

- Drive ID: `1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU`;
- bytes/pages/SHA-256: `9842696` / `22` / `0d54f0c2157e76f621bf2fd65137386ae538a792516c473703179bc3127fba73`;
- text layer: `ABSENT_SCAN_ONLY`.

Visual witnesses:

- printed p.14: Drive `1yOm3KBJ9ujtETUG7u-0hl5ijrGiKuXYG`, SHA-256 `ed381e3ee5764483098fbdda76986953d8d5c7e2ab170e453d38d1a2fd6c23e5`;
- printed p.15: Drive `1v-7bxYeZ6bMsaiVoFgqz5nWUctOtEwA8`, SHA-256 `bb3e78a0deb06b437cbf647c09fada131343eb48174d2fa0630809aca639b2ea`;
- combined Google Doc: `1zCwFFMTaOcI476aOP_cXSzgdViWNk4VEySJ2G88W6bY`.

Закрыто:

1. p.14 начинает материал **«О Петербургской „свободе“»**;
2. pp.14–15 содержат критику/обсуждение евангельского союза;
3. p.15 завершает материал подписью **«Ваш меньший брат А. М. Мазаев»**;
4. title, continuity, author attribution и existence-level critique claim имеют статус `VISUAL_PAGE_VERIFIED`.

Не закрыто: full OCR, `BOUNDED_TRANSCRIPTION_PENDING`, general quote-ready, документы соглашения 1912 года и обобщение позиции статьи на всё движение.

## 5. Обязательные модели стадий

### Acquisition

`LOCATOR_ONLY → VIEWER_ACCESSIBLE → BYTES_ACQUIRED → CANONICAL_DRIVE_REGISTERED`

### Proof

`NO_TEXT → TEXT_LAYER_PRESENT → VISUAL_PAGE_VERIFIED → BOUNDED_TRANSCRIPTION_VERIFIED → QUOTE_READY`

### Source class

`UNCLASSIFIED → DERIVATIVE_TRANSCRIPTION | PUBLISHED_PRIMARY_TEXT_EDITION | ARCHIVAL_FACSIMILE`

Переходы не подразумеваются:

- link ≠ viewer;
- viewer ≠ bytes;
- bytes ≠ canonical registration;
- text layer ≠ visual verification;
- visual page ≠ bounded transcription;
- old wording inside a modern file ≠ archival facsimile;
- bounded transcription ≠ unlimited quotation right.

## 6. Что остаётся открытым

Эта authority **не** закрывает:

- visual page-card set для всех 14 страниц Синичкина;
- source-chain pass для dossier Воронина;
- archival original/provenance письма Шилова и ответа 1920 года;
- bounded transcription для «Баптиста» 1909 №11 pp.14–15;
- OCR 46 сканов «Баптиста» 1909–1911;
- OCR 16 выпусков «Утренней звезды» 1915;
- первые пять физических единиц «Слова истины» 1918;
- отсутствующие/неизвлечённые выпуски «Братского листка»;
- платные институциональные заказы;
- publication readiness книги или отдельных глав.

## 7. Supersession

Исторические отчёты сохраняются. Эта authority supersede’ит только:

- отсутствие exact bytes/text layer для acquisitions rows 51–53;
- старое неразличение operational MASTER и proof authority;
- blocker, будто primary pages «Баптиста» 1909 №11 не открыты;
- ошибочный `PRIMARY_SOURCE` label для exact Word-PDF Шилова.

Запрещены более широкие выводы: «архив полностью закрыт», «весь №11 quote-ready», «письмо Шилова проверено по архивному оригиналу», «все unity documents получены».

## 8. Текущий итог

```text
LIVE MASTER: OPERATIONAL INVENTORY
GITHUB AUTHORITY: STATUS SEMANTICS + IMMUTABLE RECEIPTS
SINICHKIN PDF: CANONICAL / TEXT PRESENT / VISUAL PENDING / NOT QUOTE-READY
VORONIN DOSSIER: CANONICAL / TEXT PRESENT / VISUAL PENDING / NOT QUOTE-READY
SHILOV PDF: DERIVATIVE TRANSCRIPTION / NOT ARCHIVAL FACSIMILE / PRIMARY QUOTE NOT APPROVED
BAPTIST 1909 NO.11 P14–15: VISUAL PAGE VERIFIED / TRANSCRIPTION PENDING / NOT GENERAL QUOTE-READY
CORPUS-WIDE VISUAL VERIFICATION: NOT CLAIMED
PAID ORDERS: NOT AUTHORIZED
PUBLICATION READINESS: NOT CLAIMED
```
