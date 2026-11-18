# Хранение артефактов CI: что живёт только в Actions (2026-11-18)

**Роль:** `DERIVED_READ_ONLY_NOT_AUTHORITY`. Снимок, не решение: ни один HOLD здесь не
снимается и не ставится.

**Метод:** `gh api repos/<repo>/actions/artifacts по всем страницам; gitleaks-отчёты исключены как шум сканера`.

## 1. Зачем это считать

Часть объектов репозиторий сам объявляет `EPHEMERAL_ACTION_ARTIFACT` с
`durableReceiptPresent: false`. Объявление честное, но проверять его было нечем: нигде не
видно, **сколько байт и до какой даты** существует только внутри Actions. Снимок это
показывает, и делит артефакты по воспроизводимости — потому что «эфемерный» не значит
«потерянный»: отчёт о ссылках пересобирается, а скачанный из внешнего источника PDF — нет.

## 2. Итог

Живых артефактов (без отчётов сканера): **168** в **27** семьях, суммарно **5.74 ГБ**.
Просроченных: **0**. Ноль здесь читается узко: GitHub держит
просроченные артефакты в списке ещё около 90 дней, поэтому «ноль» означает «ни один из
живых не истёк», а не «за всё время ничего не пропало».

| Класс | Артефактов | Байт | Что это значит |
|---|---:|---:|---|
| `DURABLE_ON_DRIVE_RECEIPTED` | 8 | 4.07 ГБ | байты на Drive есть, квитанция записана 2026-11-18 |
| `NO_DURABLE_DESTINATION` | 2 | 1.02 ГБ | на Drive только манифест, объекты живут лишь в артефакте |
| `REVIEW_MATERIAL_ONLY` | 22 | 0.60 ГБ | артефакт — расходный материал ревью, хранению не подлежит |
| `REGENERABLE_AUDIT` | 72 | 0.03 ГБ | пересобирается; потеря артефакта не теряет доказательство |
| `HAS_DURABLE_RECEIPT` | 6 | 0.01 ГБ | есть квитанция хранения с Drive ID и SHA-256 |
| `NON_DETERMINISTIC_ACQUISITION` | 38 | 0.00 ГБ | перепрогон даёт другое состояние источника — байты не воспроизводятся |
| `REGENERABLE_PACKAGE` | 10 | 0.00 ГБ | заявка/пакет, а не сам объект |
| `REGENERABLE_VIEW` | 10 | 0.00 ГБ | производная сборка из реестра репозитория |

## 3. Семьи

| Семья | n | ГБ | Класс | Создано | Истекает | retention | Объявлено |
|---|---:|---:|---|---|---|---:|---|
| `ephemeral-second-editorial-40-pdf` | 2 | 2.54 | `DURABLE_ON_DRIVE_RECEIPTED` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | квитанция есть |
| `ephemeral-commons-strict-literary-pdf-40plus` | 2 | 1.25 | `DURABLE_ON_DRIVE_RECEIPTED` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | квитанция есть |
| `ephemeral-official-core-acquisition-59-v2` | 2 | 1.02 | `NO_DURABLE_DESTINATION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `ephemeral-poet-portrait-review-v4` | 11 | 0.32 | `REVIEW_MATERIAL_ONLY` | 2026-11-01…2026-11-17 | 2026-12-01 | 30 | расходный материал |
| `ephemeral-ephemera-review-candidates` | 11 | 0.28 | `REVIEW_MATERIAL_ONLY` | 2026-11-01…2026-11-17 | 2026-12-01 | 30 | расходный материал |
| `ephemeral-approved-ephemera-originals` | 2 | 0.21 | `DURABLE_ON_DRIVE_RECEIPTED` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | квитанция есть |
| `ephemeral-approved-core-poet-portraits` | 2 | 0.06 | `DURABLE_ON_DRIVE_RECEIPTED` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | квитанция есть |
| `total-cross-repo-source-audit` | 16 | 0.03 | `REGENERABLE_AUDIT` | 2026-10-26…2026-11-17 | 2026-11-25 | 30 | не объявлено |
| `charnock-custody-v3-research-only` | 6 | 0.01 | `HAS_DURABLE_RECEIPT` | 2026-11-17…2026-11-17 | 2026-12-17 | 30 | квитанция есть |
| `1peter-product-handoff` | 25 | 0.00 | `REGENERABLE_AUDIT` | 2026-11-01…2026-11-17 | 2026-12-01 | 30 | не объявлено |
| `g3-archive-content-inventory` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | не объявлено |
| `g3-douglas-property` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | не объявлено |
| `baptist-scan-request-package` | 10 | 0.00 | `REGENERABLE_PACKAGE` | 2026-11-01…2026-11-17 | 2026-12-01 | 30 | не объявлено |
| `g3-irs-FY2025` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `g3-irs-FY2024` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `g3-buck-media` | 14 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | не объявлено |
| `g3-irs-FY2023` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `g3-wayback-late-board` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `g3-irs-FY2022_LATER` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `baptist-proof-ledger-v2-canonical-view` | 10 | 0.00 | `REGENERABLE_VIEW` | 2026-11-01…2026-11-17 | 2026-12-01 | 30 | не объявлено |
| `official-digital-collections-link-audit` | 15 | 0.00 | `REGENERABLE_AUDIT` | 2026-10-21…2026-11-18 | 2026-11-20 | 30 | не объявлено |
| `g3-georgia-entity` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `google-drive-upload-46-link-audit` | 16 | 0.00 | `REGENERABLE_AUDIT` | 2026-10-20…2026-11-17 | 2026-11-19 | 30 | не объявлено |
| `g3-buck-titus-media-evidence` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | не объявлено |
| `g3-wayback-2025-board` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | эфемерно, квитанции нет |
| `g3-buck-rss-media-inventory` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | не объявлено |
| `g3-content-inventory` | 2 | 0.00 | `NON_DETERMINISTIC_ACQUISITION` | 2026-11-17…2026-11-17 | 2026-11-24 | 7 | не объявлено |

## 4. Ближайший обрыв

- **2026-11-19**: 0.00 ГБ — `google-drive-upload-46-link-audit`
- **2026-11-20**: 0.00 ГБ — `official-digital-collections-link-audit`
- **2026-11-24**: 5.10 ГБ — `ephemeral-approved-core-poet-portraits`, `ephemeral-approved-ephemera-originals`, `ephemeral-commons-strict-literary-pdf-40plus`, `ephemeral-official-core-acquisition-59-v2`, `ephemeral-second-editorial-40-pdf`, `g3-archive-content-inventory`, `g3-buck-media`, `g3-buck-rss-media-inventory`, `g3-buck-titus-media-evidence`, `g3-content-inventory`, `g3-douglas-property`, `g3-georgia-entity`, `g3-irs-FY2022_LATER`, `g3-irs-FY2023`, `g3-irs-FY2024`, `g3-irs-FY2025`, `g3-wayback-2025-board`, `g3-wayback-late-board`
- **2026-11-25**: 0.03 ГБ — `total-cross-repo-source-audit`
- **2026-12-01**: 0.60 ГБ — `1peter-product-handoff`, `baptist-proof-ledger-v2-canonical-view`, `baptist-scan-request-package`, `ephemeral-ephemera-review-candidates`, `ephemeral-poet-portrait-review-v4`
- **2026-12-17**: 0.01 ГБ — `charnock-custody-v3-research-only`

Ближайшая дата — через несколько дней. Это не значит, что доказательства исчезнут: у
большинства семей перепрогон даёт сопоставимый объект. Но у класса
`NON_DETERMINISTIC_ACQUISITION` перепрогон даёт **другое состояние источника**, и если
владелец считает прежние байты доказательством, их нужно забрать до этой даты.

## 5. Проверка на Drive: у двух семей байты уже сохранены

Срок артефакта сам по себе не означает потери. Проверка на Drive 2026-11-18 разделила
эти гигабайты на две несопоставимые части: у двух семей байты сохранены, у одной — нет.

| Семья | Что найдено на Drive | Объектов | Байт | SHA-256 |
|---|---|---:|---:|---|
| `ephemeral-second-editorial-40-pdf` | папка «02 — SECOND EDITORIAL 40» | 40 | — | есть |
| `ephemeral-commons-strict-literary-pdf-40plus` | папка «01 — COMMONS STRICT 40» | 9 | 610 192 501 | есть |
| `ephemeral-approved-core-poet-portraits` | папка «01 — APPROVED CORE POET PORTRAITS 45» | 3 | 15 606 930 | есть |
| `ephemeral-approved-ephemera-originals` | папка «02 — APPROVED EPHEMERA 63» | 5 | 133 208 395 | есть |
| `ephemeral-poet-portrait-review-v4` | папка «01 — PEOPLE & PORTRAITS» | 0 | — | нет |
| `ephemeral-ephemera-review-candidates` | папка «01 — PEOPLE & PORTRAITS» | 0 | — | нет |
| `ephemeral-official-core-acquisition-59-v2` | папки нет | 0 | — | нет |

**`ephemeral-second-editorial-40-pdf`** — 40 PDF в четырёх шардах 01-10 / 11-20 / 21-30 / 31-40, у каждого серверный sha256Checksum; рядом ZIP с манифестом прав и SHA-256.

Чего не хватает: Квитанция теперь есть: docs/research/holds/CORPUS_CUSTODY_RECEIPTS_2026-11-18.md (снята 2026-11-18). Остаётся не сверенным содержимое шардов.

**`ephemeral-commons-strict-literary-pdf-40plus`** — Девять ZIP-шардов (01-10 / 11-20 / 21-30 / 31-40, по частям A/B/C), сумма размеров 610 192 501 Б против 610 183 443 Б заявленных для 40 PDF; файл проверки перечисляет 40 из 40 «OK».

Чего не хватает: В репозитории нет квитанции, связывающей ID папки и суммы шардов с манифестом.

**`ephemeral-approved-core-poet-portraits`** — Три ZIP-шарда с серверными суммами и манифест прав. В самом allowlist-файле статус записан как CURRENT LICENSE RECHECK REQUIRED.

Чего не хватает: Квитанция есть: docs/research/holds/CORPUS_CUSTODY_RECEIPTS_2026-11-18.md §3. Объём артефакта больше суммы шардов, причина расхождения не установлена.

**`ephemeral-approved-ephemera-originals`** — Четыре шарда оригиналов (01-16, 17-32, 33-48, 49-63) плюс контрольный лист и кандидаты; у каждого серверная сумма.

Чего не хватает: Квитанция есть: CORPUS_CUSTODY_RECEIPTS_2026-11-18.md §3. Артефакт больше суммы шардов — расхождение не объяснено.

**`ephemeral-poet-portrait-review-v4`** — На Drive — итог ревью: контрольные листы и списки кандидатов. Скачанные изображения кандидатов на Drive не переносились и доказательством не являются.

Чего не хватает: Ничего: расходный материал ревью не подлежит хранению как доказательство.

**`ephemeral-ephemera-review-candidates`** — На Drive — контрольные листы, ephemera-candidates.csv (1,2 МБ) и ephemera-candidates.json (1,7 МБ): то, по чему принималось решение.

Чего не хватает: Ничего по хранению; сами кандидаты — расходный материал.

**`ephemeral-official-core-acquisition-59-v2`** — На Drive только манифест 19 137 Б и документ статуса; STEPBible, morphhb и SBLGNT поиском не обнаружены — это же записано в самом документе статуса от 2026-07-30.

Чего не хватает: На Drive наборов нет, но байты воспроизводимы по зафиксированным коммитам (размеры совпали байт в байт, 2026-11-18): см. docs/research/holds/OFFICIAL_CORE_DATASETS_REPRODUCIBILITY_2026-11-18.md. Артефакт 2026-11-24 — дедлайн удобства, не хранения.

Отсюда поправка к первой редакции снимка: прежний вывод «квитанции нет» был верен
только про репозиторий. Для second-editorial и commons strict байты на Drive есть, и
потеря артефакта их не уничтожит. Настоящий риск — только у `official-core`: там на Drive
лежит манифест на 19 КБ, а объекты на 123 МБ истекают 24 ноября.

## 6. Что здесь не так, помимо срока

Артефакты сборки PDF висят на прогонах **dependabot-ветвей**: обновление версии
`upload-artifact` меняет сам workflow-файл, а path-фильтр включает этот файл, поэтому
каждый dependabot-PR пересобирает архив в гигабайт. Побочный эффект: живой артефакт
последней сборки может оказаться копией с ветки, которая вот-вот закроется.

## 6. Границы

- Снимок описывает только артефакты Actions. Объекты в Drive и в репозитории он не проверяет.
- Класс воспроизводимости назначен по тому, что workflow делает с внешним объектом, а не
  по проверке совпадения байтов двух прогонов: такой проверки не делалось.
- `HAS_DURABLE_RECEIPT` присвоен только семье Charnock V3, и только потому, что суммы
  сверены с Drive 2026-11-18 в `docs/research/holds/DRIVE_SHA256_READBACK_CROSSCHECK_2026-11-18.md`.
- Раздел 5 опирается на `list_files` по ID папок и `get_file` по объектам. Содержимое
  архивов не распаковывалось: совпадение объёма и наличие sums — не проверка содержимого.
- Снимок датирован. Retention и состав семей меняются каждым прогоном, поэтому файл
  пересобирается, а не правится.

Воспроизводимость: `python3 scripts/audit_artifact_custody.py`.
