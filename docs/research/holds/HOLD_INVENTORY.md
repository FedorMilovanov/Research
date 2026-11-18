# HOLD inventory — сквозной инвентарь HOLD-ов Research

**Собрано:** 2026-11-18; **проверенный коммит:** `34b0332dfa9c5df35cc33f2fa9e344dac6781357`. **Роль:** производный read-only артефакт, не authority. Пересобрать: `python3 -B scripts/render_hold_inventory.py`.

Инвентарь отвечает на один вопрос: какие HOLD-и объявлены в репозитории, какого они типа и что нужно, чтобы закрыть каждый честно. Он **ничего не снимает**: по `data/repository-evidence-policy-v2.json` HOLD не снимается ни присутствием файла в Research/Drive, ни достижимостью URL, ни библиографической записью.

## 1. Сколько и каких

| Метрика | Значение |
|---|---|
| JSON-файлов с HOLD-ами | 35 |
| JSON-записей (объектов) с HOLD-ами | 2231 |
| Всего HOLD-вхождений в `holds`-массивах | 6012 |
| Markdown-файлов с типизированными токенами | 759 |
| Всего типизированных токенов в Markdown/YAML | 7145 |
| Нетипизированных строк `HOLD` | 0 |

По типам:

| Тип | В JSON-реестрах | В Markdown/YAML | Маршрут закрытия |
|---|---|---|---|
| `EVIDENCE_HOLD` | 1113 | 1082 | EXTERNAL_EVIDENCE |
| `LOCATOR_HOLD` | 236 | 1582 | EXTERNAL_LOCATOR |
| `ARCHIVE_HOLD` | 1344 | 1173 | EXTERNAL_OBJECT |
| `RIGHTS_HOLD` | 1355 | 1206 | EXTERNAL_RIGHTS |
| `PUBLICATION_HOLD` | 1964 | 2102 | TERMINAL_BY_DEFAULT |

Счётчики не суммировать: один и тот же HOLD описывается и в машинном реестре, и в досье, и в аудите.

## 2. Что означает каждый маршрут

- `EVIDENCE_HOLD` → **EXTERNAL_EVIDENCE**. Нужно прочитать сам источник (полный текст в нужной редакции) либо получить независимое свидетельство требуемой силы.
- `LOCATOR_HOLD` → **EXTERNAL_LOCATOR**. Нужен точный локатор в конкретном издании: страница, столбец, номер строки, лист, таймкод — сверенный с самим объектом.
- `ARCHIVE_HOLD` → **EXTERNAL_OBJECT**. Нужен сам архивный/печатный объект: страницы, листы, сканы, документ из закрытого собрания. Каталог и опись объект не заменяют.
- `RIGHTS_HOLD` → **EXTERNAL_RIGHTS**. Нужно установить права на объект (издатель, архив, лицензия). Чтение текста и достижимость URL права не устанавливают.
- `PUBLICATION_HOLD` → **TERMINAL_BY_DEFAULT**. Отдельное решение владельца о публикации. Исследовательский проход не снимает PUBLICATION_HOLD, даже если источник прочитан полностью.

## 3. По корпусам

| Корпус | JSON-записей с HOLD | Markdown-токенов |
|---|---|---|
| `docs` | 219 | 2359 |
| `ИСКУПЛЕНИЕ` | 526 | 1976 |
| `БИОГРАФИИ` | 0 | 1323 |
| `data` | 1248 | 1 |
| `SUNO_HYMNS` | 223 | 618 |
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО` | 0 | 217 |
| `apostasy` | 0 | 183 |
| `G3_HISTORY` | 0 | 142 |
| `TEEN_DOUBLE_LIFE` | 0 | 58 |
| `LE_CANON_SUCRE` | 0 | 44 |
| `1_PETER_BOT` | 15 | 27 |
| `STEVE_LAWSON` | 0 | 33 |
| `ОТСТУПНИЧЕСТВО` | 0 | 31 |
| `1_КОРИНФЯНАМ_11` | 0 | 25 |
| `(root)` | 0 | 21 |
| `BIBLE_CORPUS` | 0 | 15 |
| `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ` | 0 | 15 |
| `СЕРИЯ ЖЕНЩИНЫ В СЛУЖЕНИИ` | 0 | 14 |
| `ТРУДНЫЕ ТЕКСТЫ` | 0 | 10 |
| `СЕРИЯ 1 КОРИНФЯНАМ 11` | 0 | 9 |
| `SOURCE_LIBRARY` | 0 | 8 |
| `APOSTASY` | 0 | 6 |
| `RUSSIAN_BAPTISTS_ARCHIVE` | 0 | 4 |
| `БАПТИСТЫ РОССИИ` | 0 | 4 |
| `СЕРИЯ СЕРДЦЕ` | 0 | 2 |

## 4. Внутренние проверки, выполненные в этом проходе

### 4.1 SUNO_HYMNS: машинный реестр против человекочитаемого зеркала

Проверено записей: 126. Вердикт: **PASS**.

Источники в JSON без отдельной секции в `SOURCE_REGISTER.md`: 20. Это не расхождение HOLD-ов (сравнивать не с чем), но зеркало покрывает не весь реестр.

### 4.2 SUNO_HYMNS: тезисы

Проверено тезисов с зеркалом: 51. Вердикт: **PASS**; тезисов в JSON без секции в `CLAIM_LEDGER.md`: 141.

### 4.3 1_PETER_BOT: действующий статус после цепочки override

Кандидатов: 144; override-записей: 7; действующих `HOLD`: **0**.

Замороженные исторические метки `HOLD`, перекрытые override-файлами (7): `w3q_013`, `w3q_031`, `w3q_036`, `w3q_038`, `w3q_050`, `w3q_051`, `w3q_075`.

### 4.4 «Реформация»: датированный аудит против выросшего реестра

В реестре 219 записей. Аудит 2026-11-11 объявляет охват 211 записей и содержит таблицу §4 ровно на 211 строк. Записей, отсутствующих в аудите целиком: **0**. Записей, описанных в прозе аудита, но не попавших в таблицу: **8**.

Только в прозе: `REF-P88`, `REF-P89`, `REF-P90`, `REF-P91`, `REF-P92`, `REF-P93`, `REF-P94`, `REF-S109`. Без типизированных HOLD-ов среди них: **0**. Это дельта формы подачи, а не пропуск аудита.

Действующие HOLD-и реестра: `ARCHIVE_HOLD`=164, `EVIDENCE_HOLD`=92, `LOCATOR_HOLD`=55, `PUBLICATION_HOLD`=219, `RIGHTS_HOLD`=198. Вердикт: **PASS**.

### 4.5 Формальные противоречия HOLD и его оси состояния

| Файл | id | Ось | Значение | HOLD |
|---|---|---|---|---|
| `ИСКУПЛЕНИЕ/nt/data/nt-corpus-v1.json` | `S15` | `rightsState` | `PUBLICATION_ELIGIBLE` | `RIGHTS_HOLD` |

Противоречие — сигнал перепроверить запись, а не основание снять HOLD: оси описывают разные предметы (например, права на конкретный фрагмент).

### 4.6 HOLD недозаявлен (fail-closed проверка)

Записей с `rightsState` = `RIGHTS_UNKNOWN`/`PERMISSION_REQUIRED` и без `RIGHTS_HOLD`: **5**, из них в датированных снимках **5**, а в недатированных (действующих) файлах **0**. Записей с `publicationState` = `BLOCKED` и без `PUBLICATION_HOLD`: **0**.

| Файл | id | rightsState | Фактические HOLD-и |
|---|---|---|---|
| `ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-05.json` | `dort` | `RIGHTS_UNKNOWN` | `PUBLICATION_HOLD` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-05.json` | `westminster` | `RIGHTS_UNKNOWN` | `PUBLICATION_HOLD` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-05.json` | `heidelberg` | `RIGHTS_UNKNOWN` | `PUBLICATION_HOLD` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-05.json` | `davenant2024` | `RIGHTS_UNKNOWN` | `PUBLICATION_HOLD` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-05.json` | `articles39` | `RIGHTS_UNKNOWN` | `PUBLICATION_HOLD` |

Это дыра в обратную сторону: запись выглядит права-разрешённой, хотя права не установлены. Правильная реакция — добавить типизированный `RIGHTS_HOLD` в актуальную запись, а не переписывать датированный снимок задним числом.

### 4.7 Что держат только права и публикация

Объектов, прочитанных полностью и с точным локатором, где все HOLD-и сводятся к `RIGHTS_HOLD`/`PUBLICATION_HOLD`: **417** в машинных реестрах. Здесь новый поиск ничего не изменит — нужен ответ по правам и решение о публикации.

| Реестр | Объектов | Примеры |
|---|---|---|
| `data/charnock-biographical-anchors-v1.json` | 146 | `A25478`, `A32722`, `A32723` |
| `data/charnock-series-editorial-plan-v1.json` | 110 | `(без id)`, `(без id)`, `(без id)` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-05.json` | 83 | `allargs-scan-cheek2025-p94`, `allargs-scan-cheek2025-p95`, `allargs-scan-cheek2025-p96` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_wave6_2026-11-03.json` | 24 | `F1K-LICENSE`, `F1K-README`, `JOHN` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_wave9_2026-11-03.json` | 24 | `CRAMER-V2-P318-JPG`, `CRAMER-V2-P319-JPG`, `CRAMER-V2-P320-JPG` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_wave8_2026-11-03.json` | 8 | `PUSEY-V1-CAPITA-JPG`, `PUSEY-V1-COLOPHON-JPG`, `PUSEY-V1-ERRATUM-JPG` |
| `SUNO_HYMNS/data/source-registry-v1.json` | 6 | `SRC-CONF-1689-LBCF`, `SRC-PHOS-CLEM-EB1911`, `SRC-PHOS-CLEM-MCCLINTOCK` |
| `ИСКУПЛЕНИЕ/nt/data/nt-corpus-v1.json` | 5 | `S1`, `S2`, `S3` |
| `data/bible-corpus-rights-provenance-2026-08-06.json` | 4 | `CROSSWIRE-RUSSYNODAL-COPYRIGHT`, `CROSSWIRE-RUSSYNODALLIO-1.0.3`, `ONLY-BIBLE-KASSIAN-PERMISSION-NOTICE` |
| `ИСКУПЛЕНИЕ/evidence/source_controls_wave4_2026-11-03.json` | 2 | `AUGUSTINE`, `CHRYSOSTOM` |
| `ИСКУПЛЕНИЕ/fathers/data/fathers-corpus-v1.json` | 2 | `(без id)`, `(без id)` |
| `data/charnock-handoff-receipt-v1.json` | 1 | `(без id)` |

Разрез по правам (как их называет сам реестр, не как их оценивает этот отчёт):

| `rightsState` | Объектов |
|---|---|
| `PUBLICATION_ELIGIBLE` | 281 |
| `PRIVATE_STUDY_ONLY` | 43 |
| `PUBLIC_DOMAIN` | 37 |
| `STORAGE_ONLY` | 34 |
| `RIGHTS_UNKNOWN` | 19 |
| `PERMISSION_REQUIRED` | 3 |

Из 417 объектов: **318** уже помечены как публикационно допустимые или общественное достояние — их держит только решение о публикации, а не права; **77** по политике владельца существуют только для внутренней работы; и лишь **22** требуют запроса о правах или разрешения.

Кто именно требует запроса о правах:

- `SUNO_HYMNS/data/source-registry-v1.json` (`RIGHTS_UNKNOWN`): `SRC-CONF-1689-LBCF`, `SRC-PHOS-CLEM-EB1911`, `SRC-PHOS-CLEM-MCCLINTOCK`, `SRC-PHOS-CLEM-TEXT`, `SRC-PHOS-EPIPHANIUS-COLLYRIDIANS-LOCATORS`, `SRC-PHOS-SHOEMAKER-LECTURE-2017`
- `data/bible-corpus-rights-provenance-2026-08-06.json` (`PERMISSION_REQUIRED`): `CROSSWIRE-RUSSYNODALLIO-1.0.3`, `ONLY-BIBLE-KASSIAN-PERMISSION-NOTICE`, `RBO-KASSIAN-CATALOG-2039`
- `ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-05.json` (`RIGHTS_UNKNOWN`): `articles39`, `davenant2024`, `dort`, `heidelberg`, `westminster`
- `ИСКУПЛЕНИЕ/evidence/source_controls_wave8_2026-11-03.json` (`RIGHTS_UNKNOWN`): `PUSEY-V1-CAPITA-JPG`, `PUSEY-V1-COLOPHON-JPG`, `PUSEY-V1-ERRATUM-JPG`, `PUSEY-V1-PRAEF-IX-JPG`, `PUSEY-V1-PRAEF-VII-JPG`, `PUSEY-V1-PRAEF-VIII-JPG` и ещё 2

Из них **1** уже несут записанный отрицательный вердикт в собственном поле `finding`: вопрос прав там отвечен «не использовать», и открытым остаётся только формальное снятие, а не запрос.

Оговорка: Один и тот же объект может учитываться в двух реестрах корпуса (например, карточка и её снимок в плане), поэтому сумма — верхняя граница.

### 4.8 Неканоническая лексика внутри `holds`

Записей в `holds`, которые не являются каноническим типом: **134**, вердикт **PASS**. Корпуса `ИСКУПЛЕНИЕ/{data,nt,synthesis,fathers}` объявляют свои `holds` как «маркеры состояния прозы файла (дубль для машинного учёта)», поэтому в одном массиве лежат три разных словаря: типизированные HOLD-и, HOLD-и в неканонической записи, значения осей состояния и вердикты. Массивы не переписываются: правка данных без правки прозы расщепила бы источник.

| Неканоническая запись | Канонический тип | Всего | Из них добавляют новый долг |
|---|---|---|---|
| `ORIGINAL_TEXT_HOLD` | `EVIDENCE_HOLD` | 25 | 13 |
| `ATTRIBUTION_HOLD` | `EVIDENCE_HOLD` | 5 | 2 |
| `EDITION_HOLD` | `EVIDENCE_HOLD` | 5 | 0 |
| `MT_HOLD` | `EVIDENCE_HOLD` | 5 | 0 |
| `LXX_HOLD` | `EVIDENCE_HOLD` | 4 | 0 |
| `EDITION_UNAVAILABLE` | `ARCHIVE_HOLD` | 2 | 1 |
| `RECONCILIATION_HOLD` | `EVIDENCE_HOLD` | 2 | 0 |
| `CONTEXT_HOLD` | `EVIDENCE_HOLD` | 1 | 0 |
| `DATE_HOLD` | `EVIDENCE_HOLD` | 1 | 0 |
| `FACSIMILE_HOLD` | `ARCHIVE_HOLD` | 1 | 1 |
| `LOCATOR_SINGLE_ATTESTATION` | `LOCATOR_HOLD` | 1 | 0 |
| `TEXT_ACCESS_HOLD` | `EVIDENCE_HOLD` | 1 | 0 |

Итого: **53** записей сводятся к каноническому типу, из них **35** лишь повторяют уже объявленный на том же узле тип. Новый долг добавляют только **18** записей (17 уникальных пар «узел + тип»):

- `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` → `ARCHIVE_HOLD`: `(без id)`
- `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` → `EVIDENCE_HOLD`: `07`
- `ИСКУПЛЕНИЕ/fathers/data/fathers-corpus-v1.json` → `EVIDENCE_HOLD`: `01`, `03`, `04`, `10`, `11`, `12`, `15`, `16`, `17`, `18`, `20`, `21`
- `ИСКУПЛЕНИЕ/synthesis/data/synthesis-corpus-v1.json` → `ARCHIVE_HOLD`: `06_MERGE_REA`
- `ИСКУПЛЕНИЕ/synthesis/data/synthesis-corpus-v1.json` → `EVIDENCE_HOLD`: `05_RIGHTS_AN`, `06_MERGE_REA`

Ещё **78** записей — это значения осей состояния и вердикты, а не HOLD-и (`PRIVATE_STUDY_ONLY`, `LOCATOR_PARTIAL`, `FALSE_FRIEND`, `QUOTE_RISK`, `FALSE_LOCATOR`, `PARTIAL_VERIFICATION`, `RIGHTS_UNKNOWN`, `ATTRIBUTION_SECONDARY`, `OPEN_TENSION`, `DRAFT` и др.). Они не требуют ни объекта, ни решения: это подписи к прозе.

Голый `HOLD` встречается 2 раза (`ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json`/15, `ИСКУПЛЕНИЕ/synthesis/data/synthesis-corpus-v1.json`/00_SYNTHESIS) и всегда рядом с типизированным HOLD на том же узле, то есть своего долга не несёт.

Правило зафиксировано в генераторе: незнакомое значение в `holds` переводит проверку в `REVIEW`, поэтому новый словарь не проскочит молча.

### 4.9 Книга «Баптисты России»: HOLD в прозе досье

В `БАПТИСТЫ РОССИИ` HOLD объявлен строкой `Status:` досье, а не реестром: таких строк **25** в **17** файлах (остальные упоминания — прозаические ссылки на те же метки).

| Маршрут закрытия | Меток |
|---|---|
| `EVIDENCE_HOLD` | 16 |
| `ARCHIVE_HOLD` | 6 |
| `LOCATOR_HOLD` | 2 |
| `RIGHTS_HOLD` | 1 |

Самые частые метки: `SECONDARY REPORTED / HOLD` ×2; `NARRATIVE RESOLVED / TECHNICAL TERMINOLOGY HOLD` ×1; `A2 RECEIVED / CORE FACT STRONGLY SUPPORTED / LOCATOR_HOLD` ×1; `FUNCTIONAL PROFILE STRONG / NUMERIC DETAIL HOLD` ×1; `CORE EVENT STRONGLY SUPPORTED / PRIMARY PAGE BINARY OPEN / MOTIVE HOLD` ×1; `OUTCOME STRONGLY SUPPORTED / LEGAL SEQUENCE HOLD` ×1; `DOCUMENT IDENTITY STRONG / BINARY OPEN / PAGE_VISUAL OPEN / MOTIVE HOLD` ×1; `LEGAL_TERMINOLOGY_HOLD` ×1.

Заявлений о снятии HOLD в корпусе: **0**. То есть ни одна метка не забыта и не отменена молча.

Медиа в каталоге: **26** файлов (PDF и снимки по другим объектам — Борноволоков, Белякова, Потапова, бюллетени Совета родственников), страничных образов, которых требуют метки `BINARY OPEN` / `HOLD FOR FACSIMILE`, среди них нет.

Вердикт: **NO_HOLD_CLOSABLE_FROM_REPO** — метки называют конкретный отсутствующий объект, поэтому закрываются только получением страничных образов, а не работой с текстом репозитория.

### 4.10 Зеркало реестра SUNO

Реестр: **146** источников, зеркало: **146** записей, отсутствующих в зеркале **0**, лишних **0**, расхождений по HOLD **0** — вердикт **PASS**.

Заголовков без id в зеркале: **6** — это групповые заголовки проходов («Third-pass additions» и т. п.), а не источники. Поздние греческие записи лежат на уровень ниже (`###`) и держат поля в одной строке через `·`, поэтому подсчёт только по `##` ошибочно показывает их отсутствующими.

## 5. Проверенные кандидаты и вердикты

| Случай | Что проверялось | Вердикт | Почему |
|---|---|---|---|
| SUNO_HYMNS SRC-PHOS-PRAVENC | ARCHIVE_HOLD при accessState=FULL_OBJECT_VERIFIED | **ОСТАВЛЕН** | Полностью прочитана энциклопедическая статья, но печатный том Православной энциклопедии (т. 62, с. 54–55) не сверялся; ARCHIVE_HOLD относится к печатному объекту, а не к веб-тексту. |
| SUNO_HYMNS SRC-PHOS-VRG-B3 | LOCATOR_HOLD при locatorState=EXACT_LOCATOR_VERIFIED | **ОСТАВЛЕН** | Локатор л. 269r взят из каталога, факсимиле рукописи не открывалось (accessState=CATALOG_ONLY); каталог не подтверждает лист. |
| ИСКУПЛЕНИЕ/nt S15 (Каноны Дорта) | RIGHTS_HOLD при rightsState=PUBLICATION_ELIGIBLE | **ОСТАВЛЕН** | PUBLICATION_ELIGIBLE ограничен явно только английским фрагментом 1840 г. из локальной записи; RIGHTS_HOLD держит остальные издания (CRC 1986, OPC 1948). |
| 1_PETER_BOT w3q_013/031/036/038/050/051/075 | status=HOLD в базовых чанках кандидатов | **НЕ ДЕЙСТВУЕТ (снят цепочкой override)** | Все семь базовых меток перекрыты question-overrides-wave3g/k/l/n; действующий счёт HOLD = 0, что подтверждает пересчёт в этом отчёте. Исторические файлы не перезаписываются. |
| 1_PETER_BOT data/p0-claim-holds-wave3.json (1 Pet 5:2a/5:2b) | P0_HOLD после закрытия HOLD-TC-5-2A/5-2B | **ОСТАВЛЕН** | Другая ось: поле officialECMWitnessStatus означает прямой readback аппарата ECM, а волна 3n закрывала кандидата по маршруту peer-reviewed ECM-based treatment и прямо не заявляла прямого dECM readback. Файл при этом нигде в репозитории не цитируется. |
| G3 Q005 / Q006 | снять hold после переименования в Lumena Ministries | **ОСТАВЛЕН** | Переименование подтверждено на уровне индекса реестра, но не даёт ни текущего status field, ни документов о переходе; Q006 TRANSFEREE/CLOSING остаётся EXTERNAL_DOCUMENT_HOLD. |

## 6. Что действительно закрыто в этом проходе

- **SUNO_HYMNS/RESEARCH/OPEN_HOLDS.md** — Пересобрано генератором scripts/render_hold_ledger.py. Состав HOLD-ов не изменился (реестры те же); обновлена только дата сборки, то есть устранено расхождение «сводка от 2026-11-15 при реестрах без изменений».

## 7. Нетипизированные `HOLD`

Не найдено.

Нетипизированные элементы внутри `holds`-массивов JSON (57 записей) — отдельный технический долг; они перечислены в JSON-версии отчёта.

## 8. Границы отчёта

- Инвентарь не перечитывает внешние источники и не проверяет их содержание.
- HOLD-и в Markdown посчитаны как токены; один и тот же HOLD может упоминаться в досье, реестре и аудите несколько раз.
- Счётчики по корпусам не складывать между собой: наборы пересекаются.

Главный вывод честного прохода: подавляющая часть HOLD-ов в этом репозитории — не забытые задачи, а сознательные запреты на утверждения без объекта (архив, права, точный локатор, независимое свидетельство). Их нельзя закрыть изнутри репозитория, не выдумывая доказательство. Закрываемыми изнутри оказываются только административные расхождения: устаревшие зеркала и замороженные метки, перекрытые более поздними файлами.

