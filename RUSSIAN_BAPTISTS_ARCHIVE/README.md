# RUSSIAN BAPTISTS ARCHIVE

Текстовая долговременная копия проекта **«РУССКИЕ БАПТИСТЫ»**. Большие факсимиле и исходные пакеты находятся в Google Drive; этот каталог обеспечивает восстановление структуры, библиографии и исследовательских решений без зависимости от истории чата.

## Канонические ресурсы

| Ресурс | Ссылка / ID |
|---|---|
| Живой MASTER ARCHIVE CATALOG | [Google Sheets](https://docs.google.com/spreadsheets/d/1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM/edit) |
| Drive ID MASTER | `1y9d_7bWAEsz8iYdMuRrtb6onDYEXLQx5PgT95oYNsSM` |
| Детальный аудит «Братского листка» | [Google Sheets](https://docs.google.com/spreadsheets/d/15L76H5bufK9Pr8EelwO-KZTYXuKX-weKnOh7qV_ze6k/edit) |
| Drive ID аудита «Братского листка» | `15L76H5bufK9Pr8EelwO-KZTYXuKX-weKnOh7qV_ze6k` |
| Emergency snapshot folder | [Google Drive](https://drive.google.com/drive/folders/1W8egf7QYGqBxKee_YgvGldxhcNyfTJRa) |
| Drive ID snapshot folder | `1W8egf7QYGqBxKee_YgvGldxhcNyfTJRa` |
| Live emergency handoff | [Google Doc](https://docs.google.com/document/d/1G-9jYTIURIC3-YA-6YdP67JejkBxZDPhj1b0yi3gm0o/edit) |

## Файлы этого каталога

- [`MASTER_STATUS_2026-07-31.md`](MASTER_STATUS_2026-07-31.md) — проверенные контрольные цифры и главные выводы.
- [`DRIVE_SNAPSHOT_MANIFEST_2026-07-31.md`](DRIVE_SNAPSHOT_MANIFEST_2026-07-31.md) — Drive ID всех аварийных копий.
- [`drive_acquisitions_manifest_2026-07-31.csv`](drive_acquisitions_manifest_2026-07-31.csv) — все 47 объектов из `12 Drive Acquisitions`: файлы, Drive ID, байты, страницы и SHA-256.
- [`snapshot_manifest_2026-07-31.json`](snapshot_manifest_2026-07-31.json) — машинный снимок контрольных цифр, конфликтов и точек восстановления.
- [`NEXT_ACTIONS.md`](NEXT_ACTIONS.md) — приоритеты получения PDF/DJVU и правила продолжения.
- [`INSTITUTIONAL_RESPONSES_2026-07-31.md`](INSTITUTIONAL_RESPONSES_2026-07-31.md) — ответы РГБ/РНБ, шифры и ограничения.
- [`BOOK_CONVERSION_AND_SITE_REMEDIATION_2026-07-31.md`](BOOK_CONVERSION_AND_SITE_REMEDIATION_2026-07-31.md) — решение о переходе от ограниченной серии к книге из 17 глав с сохранением URL.
- [`OFFICIAL_PDF_SOURCE_LEDGER_73_2026-07-31.md`](OFFICIAL_PDF_SOURCE_LEDGER_73_2026-07-31.md) — независимая копия 73 прямых официальных PDF-ссылок и незакрытых слотов.
- [`OFFICIAL_HOLE_CLOSURES_2026-07-31.md`](OFFICIAL_HOLE_CLOSURES_2026-07-31.md) — прямой официальный маршрут «Баптиста» 1909 №20, проверенные PDF «Братского вестника» 1945 №1/№3 и оставшиеся доказательные пробелы.
- [`SECOND_PDF_DJVU_ACQUISITION_LEDGER_61_2026-07-31.md`](SECOND_PDF_DJVU_ACQUISITION_LEDGER_61_2026-07-31.md) — второй пакет из 61 прямого PDF/DJVU-маршрута; суммарно зафиксировано 135 прямых URL.
- [`BRATSKY_LISTOK_1906_1910_RESEARCH_LEDGER_2026-07-31.md`](BRATSKY_LISTOK_1906_1910_RESEARCH_LEDGER_2026-07-31.md) — каноническая консолидация пономерных и постраничных находок по «Братскому листку» без дублирования этапных отчётов и ZIP-пакетов.
- [`BOOK_ENGINE_MIGRATION_INVENTORY_2026-07-31.md`](BOOK_ENGINE_MIGRATION_INVENTORY_2026-07-31.md) — аудит всех десяти HTML-глав, жёстко зашитой навигации и найденного бага прогресс-индикатора.
- [`INITIAL_CLAIM_TO_SOURCE_MATRIX_10_CHAPTERS_2026-07-31.md`](INITIAL_CLAIM_TO_SOURCE_MATRIX_10_CHAPTERS_2026-07-31.md) — приоритеты и статусы ключевых тезисов всех десяти опубликованных глав.

## Актуальная редакционная интеграция

В `FedorMilovanov/gb-is-my-strength` создан lane `lane/baptists-book-research-integration-2026-07-31`. В нём находятся:

- `baptisty-rossii/research/79-book-conversion-and-editorial-audit-2026-07-31.md`;
- `baptisty-rossii/research/80-official-periodicals-pdf-ledger-73-links-2026-07-31.md`;
- `baptisty-rossii/research/81-official-hole-closures-2026-07-31.md`;
- `baptisty-rossii/research/82-book-engine-migration-inventory-2026-07-31.md`;
- `baptisty-rossii/research/83-initial-claim-to-source-matrix-10-chapters-2026-07-31.md`;
- `baptisty-rossii/research/84-second-pdf-djvu-acquisition-ledger-61-links-2026-07-31.md`.

Решение: развивать проект как книгу с отдельными URL глав. Текущие десять опубликованных маршрутов не объединяются в один монолит и не переименовываются без отдельного SYSTEM PR.

## Высшие правила

1. Живой Google Sheets MASTER является каноническим и редактируется append-only.
2. Аварийные snapshot-копии не используются вместо живого MASTER.
3. Найденная ссылка, проверенный viewer, скачанный файл и файл в Drive — четыре разные стадии.
4. Raw Telegram export и canonical thematic copy могут составлять provenance pair и не являются мусорным дублем.
5. Сдвоенный выпуск хранится одним физическим объектом.
6. Для загрузки фиксируются Drive ID, имя, MIME, байты, страницы, SHA-256, источник, дата и папка.
7. Платные работы не начинать без отдельного согласования.
8. Этапные отчёты и подготовительные ZIP-пакеты не переносятся в канонические хранилища отдельными дублями: в MASTER и GitHub вливается только проверенная содержательная дельта.
9. Параллельные журнальные агенты работают через отдельные маркеры; общие README/status/grouped-файлы перечитываются перед записью и обновляются только idempotent append/upsert.

Последняя синхронизация: **2026-07-31, 20:21+03:00 — evidence-layer «Братского листка», единый маршрут БАН для 8 content-unknown выпусков, 49 институциональных записей и параллельная grouped-интеграция без потери дельт других журналов**.
