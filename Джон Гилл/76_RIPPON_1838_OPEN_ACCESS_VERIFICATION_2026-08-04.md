# Том 76. Rippon 1838 — durable byte receipt and edition verification

**Дата:** 2026-08-04  
**Authority ID:** `GILL-RIPPON-1838-OPEN-ACCESS-VERIFICATION-2026-08-04`  
**Family:** `GILL-FAM-BIOGRAPHICAL-PRIMARY`  
**Machine registry:** `data/gill-rippon-1838-open-access-verification-2026-08-04.json`

```text
REMOTE ITEM VERIFIED = 1
BYTE RECEIPT = 1
EDITION-USABLE ITEMS = 1
QUOTE READY = 0
DIRECT QUOTES APPROVED = 0
```

## 1. Edition identity

Для одного конкретного издания Риппона подтверждены:

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

Exact source PDF endpoint:

`https://archive.org/download/briefmemoiroflif00ripp/briefmemoiroflif00ripp.pdf`

OCR navigation endpoint:

`https://archive.org/stream/briefmemoiroflif00ripp/briefmemoiroflif00ripp_djvu.txt`

OCR остаётся только навигационным слоем и не заменяет page-image readback.

## 2. Exact-byte receipt

Файл был фактически загружен и измерен как полученный объект:

```text
file_name = briefmemoiroflif00ripp.pdf
byte_size = 9297102
sha256 = 362019ee851280e14eb4c6cd8bca70a30df957af225ac56c7c6d95bbaf461792
received_at = 2026-08-03T23:46:51.303Z
```

Durable raw-file storage установлен в Google Drive и подтверждён независимым metadata readback:

```text
provider = Google Drive
file_id = 1q4IFETrDu9bH8mGMIPQO38qQTVwxjxMu
stored_name = GILL-BIO-RIPPON-1838-IA__briefmemoiroflif00ripp__sha256-362019ee851280e1.pdf
mime_type = application/pdf
stored_size = 9297102
created_at = 2026-08-03T23:49:15.863Z
shared = false
metadata_readback = true
```

Drive-name сам по себе не использован как receipt: квитанция включает фактически загруженные bytes, полный SHA-256, measured size, time и устойчивый file ID. Файл хранится private/not-shared; Research фиксирует custody, но не превращает Drive в публичный источник.

## 3. PDF and page-image readback

Проверка полученного PDF установила:

- PDF object pages: `178`;
- catalog pages: `182`;
- repository page-number confidence: `96`;
- scan density: `400 ppi`;
- encrypted: `false`;
- JavaScript: `false`;
- attachments: `0`;
- PDF object page `6`: визуально проверенная title page;
- PDF object pages `8-9`: визуально проверенное publisher advertisement;
- PDF object page `10`: начало memoir body.

Title page визуально подтверждает Rippon, John Gill, John Bennett, лондонский адрес и 1838 год. Advertisement сообщает, что detached edition напечатано verbatim из memoir, ранее помещённого перед девятитомным exposition Gill.

Разница `178` PDF-object pages / `182` catalog pages сохранена как явная граница. Локаторы в registry относятся к PDF object index и не подменяются printed-page номерами.

## 4. Rights boundary

Работа опубликована в 1838 году; Rippon умер в 1836 году. Internet Archive предоставляет unrestricted PDF/OCR download для данного item. Registry сохраняет состояние `PUBLIC_DOMAIN_WORK_REMOTE_SCAN_DOWNLOADABLE` и отдельно указывает, что repository terms продолжают применяться.

Право хранить public-domain scan и право переносить конкретную цитату в Product не смешиваются.

## 5. Что закрыто

```text
REMOTE DISCOVERY = CLOSED
EDITION IDENTITY = CLOSED
EXACT FILE RECEIPT = CLOSED
DURABLE STORAGE RECEIPT = CLOSED
TITLE-PAGE IMAGE REVIEW = CLOSED
EDITION-LEVEL LOCATOR MAP = CLOSED
EDITION USABILITY = CLOSED
```

Family status:

`DURABLE_BYTE_RECEIPT_ESTABLISHED_EDITION_VERIFIED_CLAIM_FOLLOWUP_REQUIRED`

## 6. Что остаётся закрытым для promotion

```text
CLAIM-USABLE OWNER MAPPING = OPEN
QUOTE CARD = 0
CONTEXT WINDOW REVIEW = 0
QUOTE READY = 0
DIRECT QUOTES APPROVED = 0
PRODUCT PUBLICATION APPROVAL = 0
```

Наличие bytes и edition usability не разрешает автоматически цитировать любую страницу. Для каждого будущего тезиса требуется отдельный owner-scoped locator, контекстное окно, quote card и rights/publication decision.

## 7. Next valid action

Выбрать один конкретный claim из owner documents этой family, проверить его по page image и surrounding context, оформить одну quote card и только затем решать, может ли item стать claim usable для этого ограниченного scope. Массовая quote promotion всей книги запрещена.
