# CURRENT AUTHORITY — RUSSIAN BAPTISTS ARCHIVE

**Дата:** 2026-08-02  
**Authority ID:** `BAPTIST-ACQUISITION-PROOF-AUTHORITY-2026-08-02`  
**Статус:** текущая authority для acquisition/proof stages; **не** утверждает публикационную готовность корпуса.

## 1. Как теперь устроена authority

У проекта два согласованных, но не взаимозаменяемых слоя:

1. **Google Sheets MASTER** (`1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM`) — живой append-only операционный каталог файлов, ссылок, приобретений и заявок.
2. **GitHub current authority + immutable receipts** — точные значения статусов, правила повышения evidence и неизменяемая фиксация конкретных Drive ID, страниц, байтов и SHA-256.

Физический объект считается определённым только парой **exact Drive ID + SHA-256**. Если Sheet, GitHub receipt и фактический файл расходятся, действует `FAIL_CLOSED`: статус не повышается и конфликт не разрешается молча.

Машинная authority: [`../data/baptist-acquisition-proof-authority-2026-08-02.json`](../data/baptist-acquisition-proof-authority-2026-08-02.json).  
Неизменяемая дельта MASTER: [`drive_acquisition_delta_2026-08-02.csv`](drive_acquisition_delta_2026-08-02.csv).

## 2. Две закрытые acquisition-записи

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

Этим снимаются только старые формулировки, будто байты или текстовый слой отсутствуют. Полный visual page-card pass и production quote cards по-прежнему не выполнены.

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

Этим снимаются только старые acquisition/text-layer blocker’ы для exact file. Атрибуции внутри dossier не становятся автоматически первичными доказательствами: каждое утверждение должно возвращаться к указанному письму, журналу, архивному делу или facsimile.

## 3. Обязательная модель стадий

### Acquisition

`LOCATOR_ONLY → VIEWER_ACCESSIBLE → BYTES_ACQUIRED → CANONICAL_DRIVE_REGISTERED`

### Proof

`NO_TEXT → TEXT_LAYER_PRESENT → VISUAL_PAGE_VERIFIED → QUOTE_READY`

Переходы между стадиями не подразумеваются. В частности:

- найденная ссылка не означает доступный viewer;
- viewer не означает полученные bytes;
- bytes не означают canonical Drive registration;
- OCR/text layer не означает визуально проверенную страницу;
- визуально проверенная страница не означает право на длинную цитату без контекста и locator card.

## 4. Что остаётся открытым

Эта authority **не** закрывает:

- visual page-card set для 14 страниц Синичкина;
- source-chain/quote-card pass для 5-страничного dossier Воронина;
- OCR 46 сканов «Баптиста» 1909–1911;
- OCR 16 выпусков «Утренней звезды» 1915;
- первые пять физических единиц «Слова истины» 1918;
- отсутствующие/неизвлечённые выпуски «Братского листка»;
- институциональные заказы, для которых требуется согласование стоимости;
- publication readiness книги или отдельных глав.

## 5. Supersession

Исторические отчёты 2026-07-31 сохраняются. Эта authority supersede’ит только изменяемые утверждения о наличии exact bytes/text layer для двух перечисленных файлов и старое неразличение операционного MASTER и доказательной authority.

Любая более широкая формулировка — например «архив полностью закрыт», «Воронин quote-ready», «все источники получены» — запрещена.

## 6. Текущий итог

```text
LIVE MASTER: OPERATIONAL APPEND-ONLY INVENTORY
GITHUB AUTHORITY: STATUS SEMANTICS + IMMUTABLE RECEIPTS
SINICHKIN PDF: CANONICAL DRIVE REGISTERED / TEXT PRESENT / VISUAL PENDING / NOT QUOTE-READY
VORONIN DOSSIER: CANONICAL DRIVE REGISTERED / TEXT PRESENT / VISUAL PENDING / NOT QUOTE-READY
PAID ORDERS: NOT AUTHORIZED
PUBLICATION READINESS: NOT CLAIMED
```
