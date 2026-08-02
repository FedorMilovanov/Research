# CURRENT AUTHORITY — RUSSIAN BAPTISTS ARCHIVE

**Дата:** 2026-08-02  
**Authority ID:** `BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02`  
**Статус:** текущая authority для acquisition/proof stages; **не** утверждает публикационную готовность корпуса.

## 1. Как устроена authority

У проекта два согласованных, но не взаимозаменяемых слоя:

1. **Google Sheets MASTER** (`1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM`) — живой операционный каталог файлов, ссылок, приобретений, dossier-state и заявок. Новые inventory rows добавляются append-only; явно названные dossier cells могут обновляться idempotent targeted update.
2. **GitHub current authority + immutable receipts** — точные значения статусов, правила повышения evidence и неизменяемая фиксация Drive ID, страниц, байтов, SHA-256 и visual-card witnesses.

Физический объект определяется парой **exact Drive ID + SHA-256**. Visual closure дополнительно требует source SHA-256, точный page locator и visual-card Drive ID + SHA-256. При расхождении действует `FAIL_CLOSED`: статус не повышается и конфликт не разрешается молча.

Машинная authority: [`../data/baptist-acquisition-proof-authority-2026-08-02.json`](../data/baptist-acquisition-proof-authority-2026-08-02.json).  
Acquisition receipt: [`drive_acquisition_delta_2026-08-02.csv`](drive_acquisition_delta_2026-08-02.csv).  
Visual receipt: [`BAPTIST_1909_NO11_MAZAEV_VISUAL_CLOSURE_2026-08-02.md`](BAPTIST_1909_NO11_MAZAEV_VISUAL_CLOSURE_2026-08-02.md).

## 2. Закрытые acquisition-записи

### Синичкин — «К вопросу о крещении первого русского баптиста»

- canonical Drive ID: `1yH-oxjymaDJi4g5Els8xpRiqKFgWDD7V`;
- raw provenance duplicate: `1nPb63h0DLbhx582WFpVPeXS2fH5UFT8O`;
- canonical folder: `02 — ORIGINS, STUNDISM & IMPERIAL PERIOD`;
- bytes: `542143`;
- pages: `14`;
- SHA-256: `3d33eb3691dd18f0109028cf1c2c51bb71e21b882dfddfff4393438311498c1c`;
- MASTER row: `12 Drive Acquisitions!51`;
- acquisition: `CANONICAL_DRIVE_REGISTERED`;
- proof: `TEXT_LAYER_PRESENT`;
- visual page cards: `PENDING`;
- quote-ready: `NOT_APPROVED`.

Этим сняты только старые формулировки, будто bytes или text layer отсутствуют. Полный visual page-card pass и production quote cards не выполнены.

### «Никита Исаевич Воронин» — biography dossier

- canonical Drive ID: `17O1csxPvxZO0T4Wq0TaRmT69yQ1dkEmT`;
- raw provenance duplicate: `1_PxsBG7YrO58B3yajjNt5MF08WlZDrbV`;
- canonical folder: `03 — BIOGRAPHIES, MEMOIRS & PEOPLE`;
- bytes: `244468`;
- pages: `5`;
- SHA-256: `6d23e500ef19dc457d2f23c06b695ea95e2670759558e0419847022ccc969cc9`;
- MASTER row: `12 Drive Acquisitions!52`;
- acquisition: `CANONICAL_DRIVE_REGISTERED`;
- proof: `TEXT_LAYER_PRESENT`;
- source-chain visual pass: `PENDING`;
- quote-ready: `NOT_APPROVED`.

Атрибуции внутри dossier не становятся автоматически первичными доказательствами: каждое утверждение должно возвращаться к письму, журналу, архивному делу или facsimile.

## 3. Локальный visual closure — «Баптист» 1909 №11

**Closure ID:** `BAPTIST-1909-NO11-MAZAEV-VISUAL-2026-08-02`.

Физический источник:

- Drive ID: `1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU`;
- bytes: `9842696`;
- PDF pages: `22`;
- SHA-256: `0d54f0c2157e76f621bf2fd65137386ae538a792516c473703179bc3127fba73`;
- text layer: `ABSENT_SCAN_ONLY`.

Visual witnesses:

- printed p.14 / visual-card Drive ID `1yOm3KBJ9ujtETUG7u-0hl5ijrGiKuXYG` / SHA-256 `ed381e3ee5764483098fbdda76986953d8d5c7e2ab170e453d38d1a2fd6c23e5`;
- printed p.15 / visual-card Drive ID `1v-7bxYeZ6bMsaiVoFgqz5nWUctOtEwA8` / SHA-256 `bb3e78a0deb06b437cbf647c09fada131343eb48174d2fa0630809aca639b2ea`;
- combined Google Doc: `1zCwFFMTaOcI476aOP_cXSzgdViWNk4VEySJ2G88W6bY`.

Закрыто:

1. p.14 начинает материал **«О Петербургской „свободе“»**;
2. pp.14–15 содержат критику/обсуждение евангельского союза;
3. p.15 завершает материал подписью **«Ваш меньший брат А. М. Мазаев»**;
4. title, article continuity, author attribution и existence-level critique claim имеют статус `VISUAL_PAGE_VERIFIED`.

Не закрыто:

- full-issue OCR;
- bounded transcription точного фрагмента;
- general quote-ready;
- документы и содержание соглашения 1912 года;
- обобщение позиции статьи на всё баптистское движение.

MASTER dossier `08 Article Dossiers!S03` синхронизирован. Это **локальный** visual closure; corpus-wide visual verification не заявляется.

## 4. Обязательная модель стадий

### Acquisition

`LOCATOR_ONLY → VIEWER_ACCESSIBLE → BYTES_ACQUIRED → CANONICAL_DRIVE_REGISTERED`

### Proof

`NO_TEXT → TEXT_LAYER_PRESENT → VISUAL_PAGE_VERIFIED → BOUNDED_TRANSCRIPTION_VERIFIED → QUOTE_READY`

Переходы не подразумеваются:

- ссылка ≠ viewer;
- viewer ≠ bytes;
- bytes ≠ canonical Drive registration;
- OCR/text layer ≠ визуально проверенная страница;
- visual page ≠ точная транскрипция;
- bounded transcription ≠ неограниченное право цитирования без контекста и редакционного решения.

## 5. Что остаётся открытым

Эта authority **не** закрывает:

- visual page-card set для всех 14 страниц Синичкина;
- source-chain/quote-card pass для 5-страничного dossier Воронина;
- bounded transcription для «Баптиста» 1909 №11 pp.14–15;
- OCR 46 сканов «Баптиста» 1909–1911;
- OCR 16 выпусков «Утренней звезды» 1915;
- первые пять физических единиц «Слова истины» 1918;
- отсутствующие/неизвлечённые выпуски «Братского листка»;
- институциональные заказы, требующие согласования стоимости;
- publication readiness книги или отдельных глав.

## 6. Supersession

Исторические отчёты 2026-07-31 сохраняются. Эта authority supersede’ит только:

- утверждения об отсутствии exact bytes/text layer для Синичкина и dossier Воронина;
- старое неразличение операционного MASTER и доказательной authority;
- blocker, будто primary pages «Баптиста» 1909 №11 с author line и критикой союза не открыты.

Любая более широкая формулировка — «архив полностью закрыт», «весь №11 quote-ready», «все unity documents получены» — запрещена.

## 7. Текущий итог

```text
LIVE MASTER: OPERATIONAL INVENTORY
GITHUB AUTHORITY: STATUS SEMANTICS + IMMUTABLE RECEIPTS
SINICHKIN PDF: CANONICAL DRIVE REGISTERED / TEXT PRESENT / VISUAL PENDING / NOT QUOTE-READY
VORONIN DOSSIER: CANONICAL DRIVE REGISTERED / TEXT PRESENT / VISUAL PENDING / NOT QUOTE-READY
BAPTIST 1909 NO.11 P14–15: VISUAL PAGE VERIFIED / TRANSCRIPTION PENDING / NOT GENERAL QUOTE-READY
CORPUS-WIDE VISUAL VERIFICATION: NOT CLAIMED
PAID ORDERS: NOT AUTHORIZED
PUBLICATION READINESS: NOT CLAIMED
```
