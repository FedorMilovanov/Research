# HOLD в Research: машинный срез, закрытия 18.11.2026 и что осталось открытым

**Дата среза:** 18.11.2026 · **Статус:** навигационный/операционный реестр, **не** root authority и **не** новая evidence-policy.
**Политика:** [`data/repository-evidence-policy-v2.json`](../../data/repository-evidence-policy-v2.json) · [`AGENT_RULES.md`](../../AGENT_RULES.md) · [`data/artifact-custody-policy-v2.json`](../../data/artifact-custody-policy-v2.json)

> `HOLD` — не класс источника и не доказательство. Present на Drive, доступный URL, каталожная
> запись и совпавший хеш сами по себе не снимают `EVIDENCE_HOLD`, `LOCATOR_HOLD`, `RIGHTS_HOLD`
> или `PUBLICATION_HOLD`. Этот документ фиксирует, **где** маркеры стоят, **что** из них закрыто
> проверкой байтов и **что** осталось открытым по существу.

<!-- closures-summary:begin -->
## 0. Карта закрытий (генерируется; не редактировать руками)

Закрытий: **31**. Подтверждений без закрытия: **4**. Открытых пунктов по существу: **5**.

Типы HOLD: `ARCHIVE_HOLD` — 9, `EVIDENCE_HOLD` — 17, `LOCATOR_HOLD` — 4, `TEXT_INTEGRITY_HOLD` — 1 (ось реестра, не флаг политики).

| № | Ось | HOLD | Чем проверено | Где запись |
|---|---|---|---|---|
| 01 | Три исторические копии §2 / §6 — обратный SHA-256 readback выполнен | `ARCHIVE_HOLD` | скачивание и пересчёт байтов | `БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md §2, §2.2, §6 п.1`, `БИОГРАФИИ/Стивен Чарнок/07_REPO_CROSSLINKS_AND_DRIVE_MIRROR.md §6` |
| 02 | Зеркала отдела Чарнока, волна 22 (5 файлов) — обратная SHA-256 сверка | `ARCHIVE_HOLD` | серверная контрольная сумма | `БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md §7` |
| 03 | Зеркала отдела Чарнока, волна 23 (3 файла) — обратная SHA-256 сверка | `ARCHIVE_HOLD` | серверная контрольная сумма | `БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md, блок волны 23` |
| 04 | Зеркала отдела Чарнока, волна 24 (3 файла) — обратная SHA-256 сверка | `ARCHIVE_HOLD` | серверная контрольная сумма | `БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md, блок волны 24` |
| 05 | Зеркала отдела Чарнока, волна 25 (6 файлов) — обратный SHA-256 readback | `ARCHIVE_HOLD` | серверная контрольная сумма | `БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md, блок волны 25` |
| 06 | Искупление — четыре PD-копии: parity копия/источник по серверной SHA-256 | `ARCHIVE_HOLD` | серверная контрольная сумма | `ИСКУПЛЕНИЕ/07_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md §2` |
| 07 | Локаторная ось Markdown: 58 мёртвых относительных ссылок классифицированы, 3 дефекта починены, остальное объяснено точечно | `LOCATOR_HOLD` | read-only проверка ссылок | `scripts/audit_relative_links.py`, `scripts/test_audit_relative_links.py` и ещё 6 |
| 08 | Повреждённый текст: 95 склеек «слово+число+слово» восстановлены по истории самих файлов; 446 остаются под квитанциями | `TEXT_INTEGRITY_HOLD` | пробелы по истории файла | `data/text-integrity-repairs-2026-11-18.json`, `scripts/audit_text_integrity.py` и ещё 2 |
| 09 | Подписи SHA-256 в Markdown: 1 537 подписей разобраны, 58 совпали с байтами, 0 просроченных в живых документах | `EVIDENCE_HOLD` | пересчёт внутренних подписей | `data/internal-digests-verified-2026-11-18.json`, `scripts/verify_internal_digests.py` и ещё 2 |
| 10 | Короткие хеши: SHA-1 и MD5 рядом с именами файлов | `EVIDENCE_HOLD` | разметка коротких подписей | `data/internal-digests-verified-2026-11-18.json (schema internal-digests-verified/2, totals.byAlgorithm, состояния git-object-id и unlabelled-partial)` |
| 11 | Дубли-близнецы: один документ под двумя именами | `EVIDENCE_HOLD` | сравнение текстов | `data/document-twins-2026-11-18.json (schema document-twins/1)` |
| 12 | Самодатировка: дата в заголовке против истории Git | `EVIDENCE_HOLD` | дата в заголовке против Git | `data/state-stamps-2026-11-18.json (schema state-stamps/1)` |
| 13 | Строки Drive-реестра: ответ Drive против локального файла | `ARCHIVE_HOLD` | реестр против ответа Drive | `data/drive-ledger-audit-2026-11-18.json; data/drive-ledger-snapshot-2026-11-18.json (что именно ответил Drive)` |
| 14 | Хеши без имени файла: 514 строк разобраны по причине | `EVIDENCE_HOLD` | классификация строк | `data/internal-digests-verified-2026-11-18.json, totals.unclaimedByReason и unclaimedDigestClaimedElsewhere` |
| 15 | Drive-реестр: 92 из 92 id подтверждены; две собственные ошибки сняты в тот же день | `ARCHIVE_HOLD` | реестр против ответа Drive | `docs/research/HOLDS_REGISTER_2026-11-18.md §19`, `data/drive-ledger-audit-2026-11-18.json` и ещё 1 |
| 16 | Регистр проверен на собственные счётчики: 8 просроченных чисел и таблица по корпусам, ставшая генерируемой | `EVIDENCE_HOLD` | счётчики против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §20`, `scripts/audit_register_claims.py` и ещё 1 |
| 17 | Счётчики в прозе: «закрыта одна ось» — число убрано из фразы, а не обновлено | `EVIDENCE_HOLD` | счётчики против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §21`, `scripts/audit_register_claims.py` и ещё 1 |
| 18 | Ссылки: отчёт стал закоммиченным артефактом, таблица §8 генерируется, отчёт сверяется в CI | `LOCATOR_HOLD` | проверка относительных ссылок | `docs/research/HOLDS_REGISTER_2026-11-18.md §22`, `data/relative-links-audit-2026-11-18.json` и ещё 1 |
| 19 | Якоря: «36 ссылок с фрагментом» измерены — 18 внутристраничных и 18 межфайловых, все резолвятся | `LOCATOR_HOLD` | проверка относительных ссылок | `docs/research/HOLDS_REGISTER_2026-11-18.md §23`, `data/relative-links-audit-2026-11-18.json` и ещё 1 |
| 20 | Открытые пункты получили имя, а их числа — поле: карта закрытий больше не печатает непроверенный замер | `EVIDENCE_HOLD` | соответствие неканонических значений `holds` | `docs/research/HOLDS_REGISTER_2026-11-18.md §24`, `data/hold-value-mapping-proposal-v1.json` и ещё 1 |
| 21 | Список триггеров CI сверен с зависимостями: найдены дубли, асимметрия pr/push и пять невидимых входов гейта публикации | `LOCATOR_HOLD` | сверка триггеров CI с зависимостями гейтов | `docs/research/HOLDS_REGISTER_2026-11-18.md §25`, `scripts/audit_ci_triggers.py` и ещё 1 |
| 22 | Таблица §11 генерируется из отчёта, а отчёт перестал терять второе цитирование локатора | `EVIDENCE_HOLD` | перечитывание закреплённых локаторов | `docs/research/HOLDS_REGISTER_2026-11-18.md §26`, `data/pinned-github-locators-verified-2026-11-18.json` и ещё 1 |
| 23 | Снимок очереди читал сам себя: исключения индекса выводятся из композиции, ссылочное поле воспроизводимо | `EVIDENCE_HOLD` | регрессия на самоподтверждение | `docs/research/HOLDS_REGISTER_2026-11-18.md §27`, `data/publication-gate-queue-v1.json` и ещё 1 |
| 24 | Подтверждения: числа в заголовках заменены счётчиками из артефактов; три из четырёх заголовков были просрочены | `EVIDENCE_HOLD` | счётчики подтверждений против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §28`, `data/hold-closure-registry-v1.json` и ещё 1 |
| 25 | Таблицы §15 и §16 генерируются из отчётов; §16 печатает темы коммитов дословно, §15 называет пары поименно | `EVIDENCE_HOLD` | счётчики против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §29`, `data/document-twins-2026-11-18.json` и ещё 1 |
| 26 | §3 генерируется из реестра закрытий: третья копия перечня отставала на семь строк | `EVIDENCE_HOLD` | счётчики против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §30`, `data/hold-closure-registry-v1.json` и ещё 1 |
| 27 | Само-счётчики удалены из реестра и из прозы: два из пяти уже разошлись | `EVIDENCE_HOLD` | счётчики против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §31`, `data/hold-closure-registry-v1.json` и ещё 1 |
| 28 | Правило «число тестов — тоже счётчик» применялось к одному предложению; три из шести цитат разошлись | `EVIDENCE_HOLD` | счётчики против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §32`, `scripts/test_audit_register_claims.py` и ещё 1 |
| 29 | Аудит собственной работы: мутации нашли три проверки, которые ничего не проверяли | `EVIDENCE_HOLD` | счётчики против артефактов | `docs/research/HOLDS_REGISTER_2026-11-18.md §33`, `scripts/render_closures_summary.py` и ещё 3 |
| 30 | Неклассифицированные употребления `HOLD` и `FORBIDDEN` прочитаны по record key | `EVIDENCE_HOLD` | контекстная классификация по record key | `docs/research/HOLD_ACTIONABILITY_SWEEP_2026-11-18.md §2`, `data/hold-value-mapping-proposal-v1.json` и ещё 2 |
| 31 | Точный редакционный архив Чарнока получил durable Drive readback | `ARCHIVE_HOLD` | скачивание и пересчёт байтов | `data/charnock-editorial-book-receipt-v1-20261121.json`, `.github/workflows/charnock-editorial-book-custody.yml` и ещё 1 |

**Подтверждения (не закрытия):**
- `HCR-2026-11-18-C1` — Charnock custody v3 ZIP — независимое подтверждение квитанции
- `HCR-2026-11-18-C2` — Закреплённые GitHub-локаторы перепроверены независимо; заявленные SHA-256 совпали (локаторов: 20; совпавших SHA-256: 4; расхождений: 0)
- `HCR-2026-11-18-C3` — Якоря разделов разрешаются по заголовкам цели (ссылок с фрагментом: 48; резолвится: 48; не резолвится: 0)
- `HCR-2026-11-18-C4` — Объекты Drive перечитаны у сервера; размер и SHA-256 совпали с заявленными в реестре — значения пересняты в §19

**Осталось открытым по существу:**
- `OPEN-HOLDS-VOCABULARY` — Неканонические значения `holds` в machine-SSOT. Смешение осей в machine-SSOT сохраняется: часть значений — accessState/rightsState/publicationState, часть — статусы, часть — склейки двух флагов.
- `OPEN-PRIMARY-SOURCES` — Внешние первоисточники и точные страницы. Внешние архивы, сканы и печатные издания в этой волне не открывались; исходящая сеть ограничена, а каталог, аннотация и URL не считаются прочтением объекта.
- `OPEN-RIGHTS` — Права на хранение и публикацию. Требуют отдельного лицензионного решения по каждому объекту и не снимаются ни хешами, ни присутствием на Drive.
- `OPEN-MIRRORS-BEHIND-HEAD` — Зеркала, отставшие от HEAD. Текущие редакции томов 00/04/16 и досье новее последних проверенных зеркал; закрытие readback исторических снимков не делает их актуальными.
- `OPEN-INDEPENDENT-REVIEW` — Независимая научная приёмка. Независимый внешний рецензент не привлекался; агентская проверка не подменяет рецензию.

Строки этой карты не являются проверкой: они перечисляют, где проверка записана.
Перегенерация: `python3 -B scripts/render_closures_summary.py --write`;
расхождение с реестром ловит `--check` (шаг CI).
<!-- closures-summary:end -->

## 1. Что здесь сделано и чего здесь нет

Карта закрытий — в §0: она генерируется из `data/hold-closure-registry-v1.json`
(`scripts/render_closures_summary.py`) и проверяется шагом CI, чтобы перечень не разошёлся
с реестром. Ниже — подробности по каждой оси.

Сделано:

1. read-only инвентаризация всех маркеров `HOLD` в рабочем дереве (`scripts/audit_repository_holds.py`, снимок — `data/repository-holds-inventory-v1.json`);
2. закрытие осей — их перечень и счёт в §0, здесь числа нет — начиная с обратного SHA-256 readback Drive там, где `ARCHIVE_HOLD` был обоснован именно отсутствием этой сверки (`data/hold-closure-registry-v1.json`);
3. честный перечень того, что этими проверками не закрывается и почему.

Не сделано и не заявляется: ни один внешний архив, скан, рукопись или печатное издание в этой волне
не открывались; права не пересматривались; на Google Drive не записывался ни один объект;
независимая внешняя рецензия не привлекалась. Поэтому все `EVIDENCE_HOLD`/`LOCATOR_HOLD` по
внешним объектам, `RIGHTS_HOLD` и `PUBLICATION_HOLD` остаются в силе.

## 2. Машинный срез (18.11.2026)

<!-- inventory-slice:begin -->
| Показатель | Значение |
|---|---:|
| просканировано текстовых файлов | 3 135 |
| файлов хотя бы с одним маркером | 921 |
| канонические упоминания `PUBLICATION_HOLD` | 2 667 |
| канонические упоминания `LOCATOR_HOLD` | 1 986 |
| канонические упоминания `RIGHTS_HOLD` | 1 483 |
| канонические упоминания `ARCHIVE_HOLD` | 1 424 |
| канонические упоминания `EVIDENCE_HOLD` | 1 306 |
| строки, где флаг зафиксирован как действующий (`open`) | 2 365 |
| строки, где флаг зафиксирован как снятый (`closed`) | 824 |
| строки без явного состояния (`unmarked`) | 6 083 |
| строки, где одновременно записаны и снятие, и сохранение (`mixed`) | 406 |
| JSON-файлов с массивом `holds` | 42 |
<!-- inventory-slice:end -->

Замер снят с исключением артефактов, которые **сами описывают удержания** (`data/repository-holds-inventory-v1.json`, `data/hold-closure-registry-v1.json`, `data/hold-value-mapping-proposal-v1.json`, этот регистр): иначе пасс считал бы свои же классы и число зависело бы от того, сколько их перечислили. Поэтому цифры ниже отличаются от предыдущего снимка не только потому, что добавились файлы.

**Как читать числа.** Это счётчик текста, а не аудит источников: одна строка может называть
несколько флагов, `mixed`-строки попадают в оба состояния (поэтому `open + closed + unmarked + mixed`
не равна сумме упоминаний), исторические блоки учитываются наравне с текущими. Смысл среза — не
«8 698 проблем», а карта: где именно стоит маркер и записано ли рядом его состояние.

**Что не считается.** Собственные артефакты инвентаря исключены из сканирования, иначе снимок
учитывал бы сам себя: `data/repository-holds-inventory-v1.json`, этот документ,
`data/hold-closure-registry-v1.json` и `data/hold-value-mapping-proposal-v1.json` — последние два
называют классы удержаний, а не состояния объектов. Каталоги `.git`,
`google_drive`, `.cache`, `.scratch`, `node_modules` и аналогичные не сканируются.

### 2.1. Где стоят канонические флаги

<!-- corpus-table:begin -->
| Корпус | Файлов с маркерами | Канонических упоминаний |
|---|---:|---:|
| `docs/` | 99 | 2 914 |
| `ИСКУПЛЕНИЕ/` | 153 | 2 522 |
| `БИОГРАФИИ/` | 57 | 1 391 |
| `SUNO_HYMNS/` | 65 | 712 |
| `scripts/` | 48 | 317 |
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/` | 124 | 293 |
| `G3_HISTORY/` | 92 | 206 |
| `apostasy/` | 116 | 183 |
| `data/` | 24 | 93 |
| `ТРУДНЫЕ ТЕКСТЫ/` | 15 | 59 |
| `TEEN_DOUBLE_LIFE/` | 17 | 58 |
| `LE_CANON_SUCRE/` | 14 | 44 |
| `1_PETER_BOT/` | 5 | 44 |
| `СЕРИЯ СЕРДЦЕ/` | 9 | 36 |
| `STEVE_LAWSON/` | 14 | 34 |
| `ОТСТУПНИЧЕСТВО/` | 16 | 31 |
| `1_КОРИНФЯНАМ_11/` | 17 | 25 |
| корневые файлы | 6 | 21 |
| `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/` | 8 | 15 |
| `BIBLE_CORPUS/` | 1 | 15 |
| `СЕРИЯ ЖЕНЩИНЫ В СЛУЖЕНИИ/` | 5 | 14 |
| `СЕРИЯ 1 КОРИНФЯНАМ 11/` | 4 | 9 |
| `БАПТИСТЫ РОССИИ/` | 7 | 8 |
| `SOURCE_LIBRARY/` | 2 | 8 |
| `APOSTASY/` | 2 | 6 |
| `.github/` | 1 | 5 |
<!-- corpus-table:end -->
## 3. Что закрыто 18.11.2026 (и чем именно)

Первой закрытой осью был `ARCHIVE_HOLD`, который стоял потому, что обратная сверка байтов
Google Drive не выполнялась; перечень всех закрытых осей и их счёт — в §0, а не в этом абзаце. Методы: (а) независимое скачивание **обеих** сторон пары, локальный `sha256sum` и
`cmp`; (б) `get_file` → `sha256Checksum` со сверкой против SHA-256, записанного в репозитории при
загрузке. Контроль второго метода: скачанный в этой же волне `Westminster Confession (PD copy).pdf`
дал локальный SHA-256, идентичный серверному.

<!-- closures-detail:begin -->
| Запись | Что закрыто | Метод | Где отражено |
|---|---|---|---|
| `HCR-2026-11-18-01` | Custody-ось трёх копий: байты копии совпадают с байтами исходного объекта Drive. `ACQUIRED_DURABLE` относительно пары копия/источник. | скачивание и пересчёт байтов | [`БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md`](../../БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md) §2, §2.2, §6 п.1, `БИОГРАФИИ/Стивен Чарнок/07_REPO_CROSSLINKS_AND_DRIVE_MIRROR.md §6` |
| `HCR-2026-11-18-02` | Серверные байты каждого объекта совпадают с SHA-256 локального снимка, зафиксированным при загрузке. | серверная контрольная сумма | [`БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md`](../../БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md) §7 |
| `HCR-2026-11-18-03` | Серверные байты трёх объектов совпадают с SHA-256 локального снимка. | серверная контрольная сумма | [`БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md`](../../БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md) , блок волны 23 |
| `HCR-2026-11-18-04` | Серверные байты трёх объектов совпадают с SHA-256 локального снимка. | серверная контрольная сумма | [`БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md`](../../БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md) , блок волны 24 |
| `HCR-2026-11-18-05` | Серверные байты шести объектов совпадают с SHA-256 локального снимка. | серверная контрольная сумма | [`БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md`](../../БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md) , блок волны 25 |
| `HCR-2026-11-18-06` | Байты каждой копии равны байтам её исходного объекта (серверные SHA-256 и размеры совпадают). | серверная контрольная сумма | [`ИСКУПЛЕНИЕ/07_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md`](../../ИСКУПЛЕНИЕ/07_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md) §2 |
| `HCR-2026-11-18-07` | Не «все LOCATOR_HOLD корпуса», а локаторная ось Markdown: 2 407 файлов, 8 712 ссылок измерены, 58 дефектов разобраны по классам; 3 дефекта исправлены проверяемым способом (указание на коммит вместо мёртвого пути; добавление схемы https://), остальные 55 записаны в data/relative-link-exceptions-v1.json парами (файл, ссылка) с причиной. Ни одна ссылка не переписана «на глаз». | read-only проверка ссылок | [`scripts/audit_relative_links.py`](../../scripts/audit_relative_links.py), [`scripts/test_audit_relative_links.py`](../../scripts/test_audit_relative_links.py), [`data/relative-link-exceptions-v1.json`](../../data/relative-link-exceptions-v1.json), [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §8, [`STEVE_LAWSON/README.md`](../../STEVE_LAWSON/README.md) п.4, п.6, [`history/README_CORPUS_INDEX_2026-08-17.md`](../../history/README_CORPUS_INDEX_2026-08-17.md) (шапка), `incoming/arena-auditor/2026-07-09/pr2-lossless-snapshots/README_SNAPSHOT_FIDELITY.md`, `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/29_EXTERNAL_LINKS_REGISTRY_30_PLUS.md (строка 1)` |
| `HCR-2026-11-18-08` | Не «весь текст корпуса», а измеримый класс: 541 склейка в 19 файлах. 95 починены там, где в истории того же файла уже существовало окно ±25 символов с теми же словами и пробелами (проверка нечувствительна к пробелам: «10будущих» = «10 будущих» ≠ «11 будущих»). 446 в 9 файлах не тронуты: их текущие байты названы SHA-256 внутри корпуса (квитанции, `dossierSha256`), и правка сломала бы квитанцию молча — такие файлы помечаются `receipt-blocked`, `--repair` их пропускает, `--check` падает только на чинимой склейке. Для всех изменённых файлов выполнено «текст без пробелов совпадает до и после», все изменённые .json остаются валидным JSON. Четыре склейки в «Искуплении» починены с последующим штатным пересъёмом байтовой описи лана (`atonement_reshoot_state.py --write` → `--check: PASS`); дальнейшие правки в этом лане инструмент помечает `lane-blocked` и не делает. | пробелы по истории файла | [`data/text-integrity-repairs-2026-11-18.json`](../../data/text-integrity-repairs-2026-11-18.json), [`scripts/audit_text_integrity.py`](../../scripts/audit_text_integrity.py), [`scripts/test_audit_text_integrity.py`](../../scripts/test_audit_text_integrity.py), [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §12 |
| `HCR-2026-11-18-09` | Не «все хеши в репозитории», а измеримая ось: 1 537 подписей в 2 416 Markdown-файлах разобраны по состояниям. 58 подписей впервые сверены с байтами рабочего дерева и совпали. Просроченных 27, и все они в документах, которые фиксируют момент: 21 в манифестах раундов V68–V70 (включая три самоподписи, которые не могут совпасть никогда) и 6 в хендофф-таблице, которая сама сообщает о расхождении квитанции с файлом. Просроченных подписей в живых документах — 0. | пересчёт внутренних подписей | [`data/internal-digests-verified-2026-11-18.json`](../../data/internal-digests-verified-2026-11-18.json), [`scripts/verify_internal_digests.py`](../../scripts/verify_internal_digests.py), [`scripts/test_verify_internal_digests.py`](../../scripts/test_verify_internal_digests.py), [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §14 |
| `HCR-2026-11-18-10` | Хеш считается подписью байтов только при словесной разметке (sha1, sha-1, md5, checksum, контрольная) и отсутствии commit/коммит/blob/main=/at/after. Размеченных коротких подписей 10 (sha1 3, md5 7), и все десять указывают на объекты вне рабочего дерева — локально сверять нечего. Совпадений с файлами дерева и просроченных среди них нет. | разметка коротких подписей | — |
| `HCR-2026-11-18-11` | Скрытого дублирования между корпусами на сходстве >= 0.5 нет: все 12 пар лежат в 1 Кор. 11, «Обратной стороне кафедры» и STEVE_LAWSON. Пары-надмножества (04⊂30, 10⊂29, v0_5⊂v0_6) объявлены как supplement или поколения. | сравнение текстов | — |
| `HCR-2026-11-18-12` | Перепись полная: каждая самодатировка в шапке документа найдена и сверена с датой последнего коммита. Даты не переписывались — инструмент печатает дату, коммит и его тему. | дата в заголовке против Git | — |
| `HCR-2026-11-18-13` | Перепись полная по строкам: 92 строки найдены, у каждой зафиксировано состояние обеих сторон. Drive-сторона проверена на выборке 7 объектов, локальная — целиком там, где имя разрешается однозначно. | реестр против ответа Drive | — |
| `HCR-2026-11-18-14` | Разобраны все 514. Проверена и отклонена гипотеза «взять путь из предыдущей строки»: подходящих строк 18, и выборка показала обрывки URL и ссылки на внешние файлы — правило дало бы подписи, которых документ не делал. | классификация строк | — |
| `HCR-2026-11-18-15` | Drive-сторона реестра: 92 из 92 объектов подтверждены — 88 по размеру и md5Checksum, 4 по размеру и sha256Checksum; расхождений 0. | реестр против ответа Drive | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §19, [`data/drive-ledger-audit-2026-11-18.json`](../../data/drive-ledger-audit-2026-11-18.json), [`data/drive-ledger-snapshot-2026-11-18.json`](../../data/drive-ledger-snapshot-2026-11-18.json) |
| `HCR-2026-11-18-16` | 32 объявленных счётчика сверяются с полями артефактов; таблица §2.1 генерируется из byCorpus; оба механизма под гейтом CI | счётчики против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §20, [`scripts/audit_register_claims.py`](../../scripts/audit_register_claims.py), [`scripts/test_audit_register_claims.py`](../../scripts/test_audit_register_claims.py) |
| `HCR-2026-11-18-17` | введены утверждения в прозе под проверкой; введено состояние superseded, требующее существующего раздела ниже по файлу; число закрытий в §1/§3 заменено ссылкой на генерируемый §0 | счётчики против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §21, [`scripts/audit_register_claims.py`](../../scripts/audit_register_claims.py), [`scripts/test_audit_register_claims.py`](../../scripts/test_audit_register_claims.py) |
| `HCR-2026-11-18-18` | Отчёт data/relative-links-audit-2026-11-18.json закоммичен, §8 генерируется из него, CI сверяет отчёт с новым прогоном: resolves 2 861, external 5 984, missing 58 | проверка относительных ссылок | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §22, [`data/relative-links-audit-2026-11-18.json`](../../data/relative-links-audit-2026-11-18.json), [`scripts/audit_register_claims.py`](../../scripts/audit_register_claims.py) |
| `HCR-2026-11-18-19` | Введены состояния fragment/missing-fragment и перепись totals.fragments (total 36 = 18 + 18, resolved 36, unresolved 0); таблица §8 генерируется, утверждение §11 под проверкой | проверка относительных ссылок | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §23, [`data/relative-links-audit-2026-11-18.json`](../../data/relative-links-audit-2026-11-18.json), [`scripts/audit_relative_links.py`](../../scripts/audit_relative_links.py) |
| `HCR-2026-11-18-20` | id + title без чисел (тест), §5 без дубля распределения, обе таблицы §9 генерируются из proposal (--write/--check), 5 новых утверждений и totals.jsonHoldsTotal в инвентаре | соответствие неканонических значений `holds` | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §24, [`data/hold-value-mapping-proposal-v1.json`](../../data/hold-value-mapping-proposal-v1.json), [`scripts/check_hold_vocabulary.py`](../../scripts/check_hold_vocabulary.py) |
| `HCR-2026-11-18-21` | scripts/audit_ci_triggers.py --check: дубли, симметрия pull_request/push, покрытие исполняемых скриптов, файлы из констант и литералов, объявленные транзитивные входы; списки приведены к одному набору из 49 путей, шаг добавлен в CI | сверка триггеров CI с зависимостями гейтов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §25, [`scripts/audit_ci_triggers.py`](../../scripts/audit_ci_triggers.py), `.github/workflows/holds-inventory.yml` |
| `HCR-2026-11-18-22` | Отчёт schema 2: citations по каждому локатору, totals.citations=19 и citationFiles=7; перезамер с сетью (байты всех 17 совпали); таблица §11 генерируется (--write-pinned-table); --check-report сверяет отчёт с деревом без сети и стоит в CI; гейт таблиц идёт по SLICES, а не по списку имён | перечитывание закреплённых локаторов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §26, [`data/pinned-github-locators-verified-2026-11-18.json`](../../data/pinned-github-locators-verified-2026-11-18.json), [`scripts/verify_pinned_github_locators.py`](../../scripts/verify_pinned_github_locators.py) |
| `HCR-2026-11-18-23` | pipeline_files() выводит исключения из overlaysApplied + снимок; indexExcluded в отчёте (schema 2); composedCounts с нулями по объявленным состояниям и total; регрессия на два построения и три контроля, проверенная в обе стороны; шесть чисел §10 подключены к снимку | регрессия на самоподтверждение | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §27, [`data/publication-gate-queue-v1.json`](../../data/publication-gate-queue-v1.json), [`scripts/publication_gate_status.py`](../../scripts/publication_gate_status.py) |
| `HCR-2026-11-18-24` | counters (label/artefact/field) у подтверждений, значения читаются из отчётов; неразрешимый счётчик валит --check кодом 2; title и verification.expect без измерений (тест различает идентификаторы и измерения); C4 помечен supersededBy §19 | счётчики подтверждений против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §28, [`data/hold-closure-registry-v1.json`](../../data/hold-closure-registry-v1.json), [`scripts/render_closures_summary.py`](../../scripts/render_closures_summary.py) |
| `HCR-2026-11-18-25` | Срезы twins и stamps в audit_register_claims.py (--write-twins-table/--write-stamps-table): таблица состояний, поименные пары с перекрытием, сумма «Пар выше порога» под утверждением, дословные темы коммитов и полный список документов | счётчики против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §29, [`data/document-twins-2026-11-18.json`](../../data/document-twins-2026-11-18.json), [`data/state-stamps-2026-11-18.json`](../../data/state-stamps-2026-11-18.json) |
| `HCR-2026-11-18-26` | render_detail() в render_closures_summary.py печатает closedScope/method/recordLocations из реестра в блок closures-detail; --write и --check отвечают за оба блока; отсутствие маркеров — падение; replace_block получает маркеры параметрами и режет по найденному индексу | счётчики против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §30, [`data/hold-closure-registry-v1.json`](../../data/hold-closure-registry-v1.json), [`scripts/render_closures_summary.py`](../../scripts/render_closures_summary.py) |
| `HCR-2026-11-18-27` | Само-счётчики (closures, confirmations, openItems, claims, triggerPaths) удалены из objects и заменены отсылкой к инструменту; число утверждений убрано из прозы §21.2, §24 и записи 17; добавлены два теста — на ключи в objects и на конструкцию «N утверждени…» в регистре | счётчики против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §31, [`data/hold-closure-registry-v1.json`](../../data/hold-closure-registry-v1.json), [`scripts/test_hold_closure_registry.py`](../../scripts/test_hold_closure_registry.py) |
| `HCR-2026-11-18-28` | Размер набора удалён, а не обновлён; в §8 осталось проверяемое имя CI-шага; добавлены четыре теста — на конструкцию «число + тест» в прозе, на существование цитируемого имени шага среди шагов workflow и на те же счётчики в полях записи (previousState исключён как пересказ прошлой формулировки); свежесть закоммиченного отчёта о ссылках переехала из шага workflow в тест — первый коммит главы упал в CI именно на ней | счётчики против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §32, [`scripts/test_audit_register_claims.py`](../../scripts/test_audit_register_claims.py), [`scripts/test_hold_closure_registry.py`](../../scripts/test_hold_closure_registry.py) |
| `HCR-2026-11-18-29` | Восемь дефектов исправлены: §3 печатает все локаторы, §0 — первые два и «и ещё N»; неканонический флаг объявлен в localAxes и помечен в §0; добавлены имена трёх методов, тест падает на методе без имени; словарь имён методов дедуплицирован; обрыв причины открытого пункта помечается «…»; правило двусмысленности приведено к одному (сравниваются значения, тесты в обе стороны); у самодатировки появился --today, и закоммиченный отчёт воспроизводится со своей датой. Сверх правок: тринадцать внесённых поломок — три не были пойманы до правок и ловятся после; инвентарь §2 цитировал артефакт, разошедшийся с деревом, потому что CI сравнивал два прогона между собой, — артефакт перегенерирован и получил тест свежести; после слияния с main пересняты отчёты, пересняты пять просроченных прозовых чисел, ручная копия таблицы в §23 заменена ссылкой на генерируемую | счётчики против артефактов | [`docs/research/HOLDS_REGISTER_2026-11-18.md`](../../docs/research/HOLDS_REGISTER_2026-11-18.md) §33, [`scripts/render_closures_summary.py`](../../scripts/render_closures_summary.py), [`scripts/audit_register_claims.py`](../../scripts/audit_register_claims.py), [`scripts/audit_state_stamps.py`](../../scripts/audit_state_stamps.py), [`scripts/test_render_closures_summary.py`](../../scripts/test_render_closures_summary.py) |
| `HCR-2026-11-18-30` | Все измеренные manual-употребления получили отдельное соответствие по path, JSON pointer и value: одно legacy-написание дублирует PUBLICATION_HOLD, второе является собирательным marker/status при уже типизированных флагах, FORBIDDEN является статусом отсечённой формулировки; checker требует полное покрытие и отклоняет пропавшие, лишние и дублированные разрешения | контекстная классификация по record key | [`docs/research/HOLD_ACTIONABILITY_SWEEP_2026-11-18.md`](../../docs/research/HOLD_ACTIONABILITY_SWEEP_2026-11-18.md) §2, [`data/hold-value-mapping-proposal-v1.json`](../../data/hold-value-mapping-proposal-v1.json), [`scripts/check_hold_vocabulary.py`](../../scripts/check_hold_vocabulary.py), [`scripts/test_check_hold_vocabulary.py`](../../scripts/test_check_hold_vocabulary.py) |
| `HCR-2026-11-18-31` | Для неизменяемого snapshot от source Git SHA 962010d55e38cabf3f0c04670ec16a9d5a80704e подтверждены исходные SHA-256, Git blob IDs, ZIP-member readback, SHA-256 архива и точное равенство сырого destination readback на Drive; закрытие относится только к перечисленным в квитанции исходным файлам | скачивание и пересчёт байтов | [`data/charnock-editorial-book-receipt-v1-20261121.json`](../../data/charnock-editorial-book-receipt-v1-20261121.json), `.github/workflows/charnock-editorial-book-custody.yml`, [`docs/research/HOLD_ACTIONABILITY_SWEEP_2026-11-18.md`](../../docs/research/HOLD_ACTIONABILITY_SWEEP_2026-11-18.md) §3 |
<!-- closures-detail:end -->
**Важная граница.** Readback говорит только «байты копии равны байтам источника / байты на Drive
равны записанному снимку». Он **не** говорит, что в PDF есть нужная печатная страница, что локатор
сверен, что права позволяют публикацию или что зеркало актуально. Зеркала волн 22–25 — исторические
снимки; сегодняшние `00`/`04`/`16` новее их, поэтому новая загрузка (ED-08 как upload-действие) и
новая квитанция не выполнялись и остаются открытыми.

## 4. Что осталось открытым и что требуется для снятия

| Класс | Где | Что нужно, чтобы закрыть (без подмены) |
|---|---|---|
| `IMAGE_CHECK_PENDING` (Чарнок) | CS-03 с. 264–265 и индекс 308–309; CS-06 35 листов, расхождение «медицина 64↔65» | просмотр изображений конкретных листов; хеши и OCR этого не заменяют |
| `EVIDENCE_HOLD`/`LOCATOR_HOLD` внешних оригиналов | «Реформация» (H-08 Нант, T-03 оправдание, T-08 эсхатология; 218 REF), Чарнок (Claude, Puente, Bolduc, Nichol 1864), Искупление (страницы WCF 8, Dort II), 1 Кор. 11, Сердце, «Трудные тексты» | точный экземпляр/издание, конкретная страница или лист, проверенный контекст; каталог, аннотация и URL — недостаточны |
| `RIGHTS_HOLD` | цифровые изображения BSB/Pitts/IA/Oxford, EEBO-TCP производные, сканы XIX в., Drive-объекты | отдельное лицензионное решение по каждому предмету; readback и присутствие на Drive прав не дают |
| `PUBLICATION_HOLD` | фактически весь исследовательский корпус (`PROMOTE` не заявлялся нигде) | редакционное принятие + отдельная Product-проверка на текущем source anchor; Research closure ≠ publication approval |
| Независимая научная приёмка | Чарнок ED-02/ED-06, «Реформация» (peer review open), Искупление (agent 7) | внешний рецензент/эксперт; агентская проверка его не заменяет |
| `ARCHIVE_HOLD` по актуальности зеркал | тома 00/04/16 и досье новее последних зеркал | новая загрузка + независимый destination readback + квитанция (в этой волне не выполнялись) |
| Гигиена машинных реестров | 42 файла с массивом `holds` | см. §5 |

## 5. Наблюдение по машинным реестрам (не исправлялось)

В массивах `holds` машинных реестров есть значения, которые не являются каноническими
HOLD-флагами: `ORIGINAL_TEXT_HOLD`, `PRIVATE_STUDY_ONLY`, `LOCATOR_PARTIAL`, `FALSE_FRIEND`,
`QUOTE_RISK`, `ATTRIBUTION_HOLD`, `EDITION_HOLD`, а также единичные `RESOLVED-BY-TEXT`,
`PARTIAL_OBJECT`, `RIGHTS_UNKNOWN`, `BLOCKED`, `MIRROR-LAG`, `PERMISSION_REQUIRED` и другие.
Часть из них — состояния доступа/прав или статусы проверки, а не блокировки.

Сколько их и как они распределены, здесь не повторяется: распределение измерено в §9, и там
числа стоят под проверкой. В первой редакции этого раздела они были продублированы — и одно из
них разошлось с инвентарём (в таблице §2 стояло «39 файлов», в инвентаре — 38). Дубль убран, а
не исправлен: число должно жить в одном месте.

Это смешение осей, которое evidence-policy запрещает концептуально (`HOLD` — не класс источника и
не `accessState`/`rightsState`). Автоматически переписывать такие поля нельзя: это machine-SSOT
корпусов, и правка без владельца корпуса изменила бы смысл записей. Требуется решение владельца
корпуса о переносе значений в отдельные поля; до этого они учитываются как есть.

## 6. Воспроизводимость

```bash
python3 scripts/audit_repository_holds.py --summary                  # человеческий срез
python3 scripts/audit_repository_holds.py -o /tmp/holds.json         # полный снимок
python3 -B -m unittest discover -s scripts -p 'test_audit_repository_holds.py' -v
python3 scripts/validate_research_root_authority.py                  # корневая authority не менялась
```

Скрипт read-only: он не пишет в рабочее дерево, не снимает ни одного HOLD и не считает свой вывод
доказательством. Снимок `data/repository-holds-inventory-v1.json` — датированный срез на 18.11.2026,
а не «текущая authority»; при следующем изменении текстов с маркерами его нужно перегенерировать.

## 7. Пересъём машинных счётчиков после правки леджера (18.11.2026)

Добавление раздела в `ИСКУПЛЕНИЕ/07_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md` — это новый `##`-заголовок,
то есть **новая строка реестра доводов** (`СР@07_DRIVE_LIBRARY_AND_RIGHTS_LEDGER~2`). Проверки
правил 27/28 в `validate_atonement_corpus_integrity.py` поэтому разошлись на единицу
(236→237 строк, 1392→1393 доводов, 1666→1669 маркеров, «с вердиктом» 407→408,
«удерживается» 370→371, `маркеровВПрозеНеОтражённыхВКарточке` 43→44).

Счётчики не правились руками — они пересняты инструментами самого корпуса:

```bash
python3 -B scripts/atonement_claim_register.py --write root   # блок claimRegister20261026
python3 -B scripts/atonement_claim_register.py --check root   # 237 строк / 1393 довода — сходится
python3 -B scripts/atonement_reshoot_state.py --write         # §9.1, driveMirrors, срез дерева
python3 -B scripts/atonement_reshoot_state.py --check         # 137 чисел в 11 группах — PASS
python3 -B scripts/validate_atonement_corpus_integrity.py     # PASS (24 root-файла, 4 под-корпуса)
```

Замечание по методу: локальная копия была shallow-клоном, и падало `commitTimeChecks`
(«ни одна из 16 записей не сверена»). После `git fetch --unshallow` та же проверка даёт PASS —
то есть это была среда, а не дефект корпуса. Снимок `data/repository-holds-inventory-v1.json`
после пересъёма побайтово тот же (`cmp` двух прогонов): значения `holds` не менялись, менялись
только агрегаты реестра доводов.

Дополнительно подтверждено: в корпусе 130 файлов прозы, у всех 130 есть машинная карточка,
висящих ссылок 0 — при 39 «машинно покрытых» строках по идентификатору (это разные оси учёта,
правила 27 и 28, и они не подменяют друг друга).

## 8. Локаторная ось Markdown (18.11.2026)

HOLD-флаги считались, а мёртвые относительные ссылки — нет. Это тот же дефект, только
механический: путь обещает объект, объекта нет. Добавлен read-only замер
`scripts/audit_relative_links.py` (CI-шаг «Reject unexplained dead locators»).

Замер на 18.11.2026 (таблица генерируется из отчёта, см. §22):

<!-- links-slice:begin -->
| Показатель ссылок | Значение |
|---|---:|
| Markdown-файлов | 2 425 |
| ссылок `resolves` | 3 206 |
| ссылок `external` | 6 581 |
| ссылок `missing` | 58 |
| ссылок `outside` | 0 |
| ссылок `unqualified` | 0 |
| ссылок `missing-anchor` | 0 |
| ссылок с фрагментом (`total`) | 48 |
| из них внутристраничных | 28 |
| из них на другой файл | 20 |
| фрагментов резолвится | 48 |
| дефектов разобрано (`explained`) | 58 |
| дефектов необъяснённых (`unexplained`) | 0 |
<!-- links-slice:end -->

Все 58 дефектов разобраны:

| Класс | Ссылок | Что сделано | Почему так |
|---|---|---|---|
| Мёртвый путь на удалённый файл | 2 | Ссылка заменена указанием на коммит и blob (`b8f15a6c`/`fcf649c9…`, `e3952667`/`3f91d6d0…`) | Файлы удалены в `dff6e36a`; объект существует и читается, но не по рабочему пути |
| URL без схемы | 1 | `www.…` → `https://www.…` | Markdown трактовал адрес как относительный путь |
| Архивная копия корневого README | 50 | В шапку добавлено правило чтения; текст не переписывался | Все 50 путей разрешаются **от корня** (проверено: 50/50) |
| `HISTORICAL` в самом корпусе | 4 | Ничего: корпус уже пометил и запретил переписывать | `AUDIT_gb-main_*` принадлежали параллельному checkout |
| Lossless-снимок `pr2-…` | 4 | Отдельная заметка `README_SNAPSHOT_FIDELITY.md`; снимки не тронуты | Пути принадлежат исходному расположению документа |

55 мёртвых локаторов остаются мёртвыми и **видны**: они записаны парами (файл, ссылка) с причиной
в `data/relative-link-exceptions-v1.json`. Исключение не покрывает новую битую ссылку в том же файле
и не считается починкой. `--strict` возвращает 1 при любом необъяснённом дефекте.

Границы этого замера: проверено существование байтов по пути, а не тождество объекта, на который
ссылка указывает; разрешающаяся ссылка не доказывает содержание. Внешние URL по сети не
проверялись — исходящая сеть ограничена.

```bash
python3 -B scripts/audit_relative_links.py --summary
python3 -B scripts/audit_relative_links.py --strict          # 0 необъяснённых
python3 -B scripts/audit_relative_links.py --only missing    # полный список с номерами строк
```

### 8.1. Якоря разделов (18.11.2026)

Ссылка `файл.md#раздел` проверялась только по файлу: якорь не читался. Заголовок в файле
переименовывается, файл остаётся, ссылка продолжает «разрешаться» — но ведёт в никуда.
Добавлена проверка якоря: для относительных ссылок на `.md` с `#fragment` считается набор
заголовков цели (slug по правилам GitHub) и фрагмент должен в нём быть; иначе состояние
`missing-anchor`, которое считается дефектом наравне с `missing` и валит `--strict`.

Ссылок с фрагментом в репозитории **48**; после правки резолвятся **48/48**. Найдено два
мёртвых якоря:

| Файл | Было | Стало | Почему |
|---|---|---|---|
| `docs/research/reformation/README.md:9` | `EDITORIAL_AUDIT_2026-11-11.md#…-после-пр-496499` | `…-после-pr-496499` | «пр» вместо «pr»: заголовок «…после PR #496–499» даёт slug с латиницей |
| `ИСКУПЛЕНИЕ/18_SERIES_AUDIT_AND_ARCS_2026-10-26.md:1405` | `36_hodge…md#9-доказательство-и-возражения--ходж-гл-vii-6-7` | без правки | Заголовок существует; тире `6–7` в slug исчезает, поэтому `6-7` и `67` — одно место |

Для второго случая правило сравнения нормализует дефисные формы (`–`, `—` удаляются, как при
рендере GitHub, повторные дефисы схлопываются), иначе каждая ссылка с числовым диапазоном
считалась бы мёртвой. Содержание раздела это не проверяет: существование заголовка не есть
прочитанный текст. Якоря `#L12` и фрагменты не-markdown целей не проверяются — у них нет
заголовков.

## 9. Неканонические значения `holds`: предложение соответствия (не правка)

В 42 JSON-файлах массивы `holds` содержат 6 160 значений, из них **134 (39 написаний)** — не
канонические флаги. Это смешение осей, которое policy v2 запрещает концептуально. Автоматически
переписать такие поля нельзя — это machine-SSOT чужих корпусов, — но и оставлять их без разбора
значит хранить неизмеримое.

Предложение вынесено в `data/hold-value-mapping-proposal-v1.json` со статусом **`PROPOSAL_ONLY`**:
ни одно значение в реестрах не перезаписано. Обе таблицы ниже **генерируются** из этого файла
(`check_hold_vocabulary.py --write`), а `--check` падает, если закоммиченный блок с ним разошёлся.
Классы:

<!-- hold-classes:begin -->
| Класс | Значений | Что означает |
|---|---:|---|
| `canonical` | 80 | по смыслу это канонический HOLD, записанный своим именем |
| `axis` | 24 | это значение оси policy v2 (`accessState` / `rightsState` / `publicationState` / `locatorState`), а не HOLD |
| `split` | 7 | в одной строке склеены две вещи (флаг + статус, два флага) |
| `status` | 20 | статус записи, а не удержание: `OPEN`, `RESOLVED-BY-TEXT`, `RESEARCH / NOT PRODUCT` |
| `manual` | 3 | из одной строки не выводится (`HOLD`, `FORBIDDEN`); каждое употребление требует чтения записи |
<!-- hold-classes:end -->
<!-- hold-values:begin -->
| Написание в `holds` | Значений | Класс | Предлагаемое место |
|---|---:|---|---|
| `ORIGINAL_TEXT_HOLD` | 25 | canonical | EVIDENCE_HOLD |
| `PRIVATE_STUDY_ONLY` | 13 | axis | rightsState=PRIVATE_STUDY_ONLY (+ RIGHTS_HOLD while publication is intended) |
| `LOCATOR_PARTIAL` | 12 | canonical | LOCATOR_HOLD (+ locatorState=COARSE_LOCATOR_ONLY) |
| `FALSE_FRIEND` | 11 | status | translationRisk note; no hold |
| `QUOTE_RISK` | 6 | canonical | PUBLICATION_HOLD |
| `ATTRIBUTION_HOLD` | 5 | canonical | EVIDENCE_HOLD |
| `EDITION_HOLD` | 5 | canonical | EVIDENCE_HOLD (+ PUBLICATION_HOLD when a quote depends on it) |
| `FALSE_LOCATOR` | 5 | canonical | LOCATOR_HOLD |
| `MT_HOLD` | 5 | canonical | EVIDENCE_HOLD (note: Masoretic tradition) |
| `LXX_HOLD` | 4 | canonical | EVIDENCE_HOLD (note: Septuagint tradition) |
| `PARTIAL_VERIFICATION` | 4 | axis | accessState=PARTIAL_OBJECT (+ EVIDENCE_HOLD if a claim depends on the missing part) |
| `ATTRIBUTION_SECONDARY` | 3 | canonical | EVIDENCE_HOLD |
| `RIGHTS_UNKNOWN` | 3 | axis | rightsState=RIGHTS_UNKNOWN (+ RIGHTS_HOLD) |
| `DRAFT / PUBLICATION_HOLD` | 2 | split | PUBLICATION_HOLD + status=DRAFT |
| `EDITION_UNAVAILABLE` | 2 | split | EVIDENCE_HOLD + accessState=NOT_ACQUIRED |
| `HOLD` | 2 | manual | requires per-record reading |
| `OPEN` | 2 | status | status=OPEN; no hold |
| `OPEN-LAYER` | 2 | status | status=OPEN (layer pending); no hold |
| `OPEN_TENSION` | 2 | status | conflict record (CONFLICT) with status OPEN |
| `RECONCILIATION_HOLD` | 2 | canonical | EVIDENCE_HOLD (+ pointer to the conflict record) |
| `APPARATUS_FALSE_FRIEND` | 1 | status | translationRisk note (apparatus); no hold |
| `BLOCKED` | 1 | axis | publicationState=BLOCKED (+ PUBLICATION_HOLD) |
| `CONFLICT / LOCATOR_HOLD` | 1 | split | LOCATOR_HOLD + conflict record |
| `CONTEXT_HOLD` | 1 | canonical | EVIDENCE_HOLD |
| `DATE_HOLD` | 1 | canonical | EVIDENCE_HOLD |
| `FACSIMILE_HOLD` | 1 | canonical | EVIDENCE_HOLD (+ accessState=PARTIAL_OBJECT) |
| `FORBIDDEN` | 1 | manual | requires per-record reading |
| `LOCATOR_SINGLE_ATTESTATION` | 1 | canonical | LOCATOR_HOLD |
| `MIRROR-LAG` | 1 | canonical | ARCHIVE_HOLD |
| `NO SETTLED VERDICT / EVIDENCE_HOLD` | 1 | split | EVIDENCE_HOLD + status=no settled verdict |
| `PARTIALLY_VERIFIED` | 1 | axis | accessState=PARTIAL_OBJECT |
| `PARTIAL_OBJECT` | 1 | axis | accessState=PARTIAL_OBJECT |
| `PERMISSION_REQUIRED` | 1 | axis | rightsState=PERMISSION_REQUIRED (+ RIGHTS_HOLD) |
| `RESEARCH / NOT PRODUCT` | 1 | status | publicationState=REFERENCE |
| `RESEARCH / NOT PUBLICATION-READY` | 1 | canonical | PUBLICATION_HOLD |
| `RESOLVED-BY-TEXT` | 1 | status | closed: record with pointer to the passage that resolved it |
| `RIGHTS_HOLD + PUBLICATION_HOLD` | 1 | split | RIGHTS_HOLD + PUBLICATION_HOLD |
| `RIGHTS_UNCLEAR` | 1 | canonical | RIGHTS_HOLD (+ rightsState=RIGHTS_UNKNOWN) |
| `TEXT_ACCESS_HOLD` | 1 | canonical | EVIDENCE_HOLD (+ accessState=LINK_ONLY|NOT_ACQUIRED) |
<!-- hold-values:end -->

Проверка не даёт таблице разойтись с инвентарём: `scripts/check_hold_vocabulary.py --check`
сверяет покрытие (каждое написание из инвентаря отображено, устаревших нет), счётчики и то, что
предложенная ось существует в policy v2 с таким значением. Смена статуса с `PROPOSAL_ONLY`
валит проверку — правка реестров возможна только решением владельца корпуса, а не скриптом.

```bash
python3 -B scripts/check_hold_vocabulary.py --check    # PASS: покрытие, счётчики, классы и обе таблицы §9
python3 -B scripts/check_hold_vocabulary.py --write    # перегенерация таблиц выше из машинного файла
```

## 10. Публикационный шлюз: очередь решений (18.11.2026)

Самый крупный открытый класс — права (1 453 упоминания `RIGHTS_HOLD`) и публикация
(2 582 упоминания `PUBLICATION_HOLD`). Закрыть его работой нельзя: нужны решения человека.
Поэтому он превращён из «много текста» в проверяемую очередь: `docs/research/PUBLICATION_GATE_QUEUE_2026-11-18.md`,
снимок `data/publication-gate-queue-v1.json`, инструмент `scripts/publication_gate_status.py`
(офлайн-тесты, шаг в CI).

Что даёт очередь:

- **Композиция по правилу, а не чтение базы.** База очереди сама запрещает читать себя без
  оверлеев; скрипт применяет оверлеи по `record id` и пересчитывает счётчики. Сейчас: 10 записей,
  `BLOCKED=6`, `REFERENCE=4`, `PROMOTE=0` — сходится с заявленным в current-authority.
- **Проверяемые факты вместо обещаний.** Все `sourceAuthorities` существуют в дереве (0
  отсутствующих), все `rightsLedgerIds` встречаются в репозитории **вне очереди** — и вне
  оверлеев, вне current-authority и вне самого снимка (0 потерянных; что именно не читалось,
  перечислено в `indexExcluded`). Но наличие файла — не права, и упоминание id — не разрешение:
  это записано в самом снимке. О том, почему «вне очереди» пришлось уточнить, — §27.
- **Находка.** Корпуса, у которых нет записи в очереди, повышены быть не могут вообще:
  `productWriteRequiresPromoteRecord`. Отсутствие записи — это не «почти готово», это отсутствие
  решения; первым шагом для Чарнока, «Искупления», «Баптистов» и других должен быть не поиск
  прав, а создание записи с ограниченным тезисом.
- **Дрейф ловится.** Новая/исчезнувшая запись, смена `disposition`/`effectiveHolds`/`nextAction`,
  новая суперсессия оверлеем или `PROMOTE` с непустыми `holds` — валят `--check`.

```bash
python3 -B scripts/publication_gate_status.py --summary
python3 -B scripts/publication_gate_status.py --check
```

Это по-прежнему **не** закрытие прав и не разрешение на публикацию: ни одно удержание не снято,
ни один `disposition` не изменён.

## 11. Закреплённые GitHub-локаторы: независимая перепроверка байтов (18.11.2026)

В корпусе есть локаторы вида `github.com/<owner>/<repo>/blob/<commit>/<path>` — в основном
EEBO-TCP XML по Чарноку. Такой локатор проверяем без доверия автору: объект на закреплённом
коммите можно скачать и пересчитать. Сколько их, в каких файлах и в каком они состоянии —
в таблице ниже; она генерируется из отчёта, а не переписывается из него.

Метод: `scripts/verify_pinned_github_locators.py` — `gh api contents?ref=<commit>` с raw-медиатипом,
локальный пересчёт размера и SHA-256, заявка читается **только с той же строки** (иначе «не заявлено»,
а не догадка). Отчёт: `data/pinned-github-locators-verified-2026-11-18.json`.

Итог — в таблице ниже, и он же пересчитан в §26: совпавшие заявки, отсутствие расхождений и
недоступных объектов, объекты без заявки. У последних байты и хеши измерены и записаны, чтобы
владелец корпуса мог их принять, а не пересказывать.

<!-- pinned-locators:begin -->
| Показатель | Значение |
|---|---:|
| локаторов | 20 |
| заявленных SHA-256 совпало | 4 |
| расхождений | 0 |
| без заявки | 16 |
| недоступных | 0 |
| цитирований (мест) | 23 |
| файлов с цитированием | 10 |

| Репозиторий | Коммит | Путь | Заявка | Байт (факт) | SHA-256 (факт) | Состояние |
|---|---|---|---|---:|---|---|
| `FedorMilovanov/Research` | `d3d07164` | `G3_HISTORY/SOURCE_LEDGER.md` | — | 44074 | `48887dab8d8d1131…` | unclaimed |
| `FedorMilovanov/Research` | `43f13a21` | `G3_HISTORY/drafts/B_CORRECTIONS_REVIEW.md` | — | 7151 | `96d3689a494b0dc0…` | unclaimed |
| `FedorMilovanov/gb-is-my-strength` | `e733dd29` | `src/components/journal/G3Dossier.astro` | — | 40757 | `61a19fcb0385cc47…` | unclaimed |
| `FedorMilovanov/gb-is-my-strength` | `bc8f63dd` | `docs/LAWSON-SOURCE-RECHECK-2026-11-15.md` | — | 18517 | `c51a1654dc04ef2a…` | unclaimed |
| `FedorMilovanov/Research` | `26c5531c` | `ИСКУПЛЕНИЕ/evidence/AGENT2_JOHANNINE_ATONEMENT_EXEGESIS_HANDOFF_2026-11-15.md` | — | 115085 | `0eaca9d9d1f49370…` | unclaimed |
| `textcreationpartnership/A46911` | `32dc300b` | `A46911.xml` | да | 163974 | `e2bea34fb919b90d…` | match |
| `textcreationpartnership/A71277` | `97f473a5` | `A71277.xml` | да | 6035109 | `beaa62b9b406cbc3…` | match |
| `textcreationpartnership/A32726` | `460e9c2a` | `A32726.xml` | да | 603576 | `1268a63fa8eebeac…` | match |
| `textcreationpartnership/A79420` | `492c6013` | `A79420.xml` | да | 598792 | `5f07206177dcffc8…` | match |
| `textcreationpartnership/A41722` | `7f99242e` | `A41722.xml` | — | 76048 | `ed2038ae64d1e5bb…` | unclaimed |
| `textcreationpartnership/B02133` | `41dc7ea9` | `B02133.xml` | — | 17702 | `505f653df483ce85…` | unclaimed |
| `textcreationpartnership/A32722` | `5c9d910f` | `A32722.xml` | — | 54754 | `b25bad732f769d06…` | unclaimed |
| `textcreationpartnership/B20167` | `11049eba` | `B20167.xml` | — | 538534 | `4708c9c4b5e3036c…` | unclaimed |
| `textcreationpartnership/A25478` | `ea0aef19` | `A25478.xml` | — | 3485491 | `dd3588d681fe1ff3…` | unclaimed |
| `textcreationpartnership/A32723` | `caa75dff` | `A32723.xml` | — | 4622240 | `d6205c4062867acf…` | unclaimed |
| `textcreationpartnership/A32724` | `aa978932` | `A32724.xml` | — | 1146488 | `efaf653b7c9d0589…` | unclaimed |
| `textcreationpartnership/A35345` | `81cb6888` | `A35345.xml` | — | 4535033 | `5ef15afca7c22866…` | unclaimed |
| `textcreationpartnership/B15418` | `44913a36` | `B15418.xml` | — | 1704145 | `1b0ec102e0e3ef82…` | unclaimed |
| `GITenberg/Selections-from-the-Principles-of-Philosophy_4391` | `fe5d9245` | `4391.txt` | — | 195080 | `be132739f8ca6689…` | unclaimed |
| `textcreationpartnership/A52424` | `7859df5a` | `A52424.xml` | — | 352981 | `3680ed708035808b…` | unclaimed |
<!-- pinned-locators:end -->

**Что это даёт.** Заявка «SHA-256 фактических байтов» в `БИОГРАФИИ/Стивен Чарнок/02_…` перестала
быть утверждением автора: она воспроизводится с закреплённого объекта. Это узкая, но настоящая
победа локаторной оси.

**Чего это не даёт.** Совпадение хеша удостоверяет байты, а не прочтение: что текст именно прочитан,
что издание то самое и что есть права на воспроизведение — из хеша не следует. `ARCHIVE_HOLD` на
сканы и `RIGHTS_HOLD`/`PUBLICATION_HOLD` этим не снимаются. Для объектов без заявки измерение
добавляет факт, но не закрывает удержание: закрывать нечего, пока корпус не заявил, что искал.

```bash
python3 -B scripts/verify_pinned_github_locators.py --summary       # нужна сеть (gh api)
python3 -B scripts/verify_pinned_github_locators.py --offline --summary   # только сбор заявок
python3 -B -m unittest discover -s scripts -p 'test_verify_pinned_github_locators.py'
```

## 12. Повреждённый текст: склейки чисел (18.11.2026)

Отдельный класс HOLD, который не виден ни счётчикам, ни проверке ссылок: проза записана без
пробелов вокруг чисел — `Архитектура10будущих документов`, `погребение30июля`, `Итого44строки`.
Путь на месте, файл открывается, строка не пустая, а цитата из неё уже не транскрипция.
Пометки `стр.697–786` или `§21.111–21.113` такой формы не дают, поэтому дефект и не замечался.

Замер `scripts/audit_text_integrity.py`: **541** склейка в **19** файлах.
Код и инлайн-код маскируются при сохранении смещений (там идентификаторы вроде `A32726`
законны), латиница не считается (`EEBO-TCP`, `B20167`), проверяется только форма
«кириллическое слово + цифры + кириллическое слово».

Починка не «на глаз». Для каждой склейки берётся окно ±25 символов и ищется в прежних blob'ах
**того же файла**: `10будущих` совпадает с `10 будущих` и не совпадает с `11 будущих`; вставка
делается только при найденном окне и повторяется до неподвижной точки (соседние склейки меняют
окно друг друга). Для всех изменённых файлов выполнено
`re.sub(r'\s+', '', before) == re.sub(r'\s+', '', after)` — ни один непробельный символ не
добавлен, не удалён и не переставлен; все изменённые `.json` остаются валидным JSON.

**Починено 95 склеек в 10 файлах.** Остальные **446 в 9 файлах не тронуты**: их текущие байты
названы SHA-256 внутри корпуса (квитанции и поля `dossierSha256`), и правка сломала бы квитанцию
молча. Это проверяется машинно: файл, чей хеш встречается в корпусе, помечается `receipt-blocked`
и `--repair` его пропускает; `--check` падает только на чинимой склейке, поэтому CI зелёный, а
долг виден в отчёте. Файл без читаемой истории (мелкий клон) получает `not-checked`, а не приговор:
в CI поэтому включён `fetch-depth: 0`, иначе проверка молчала бы обо всём.

Отдельный случай — «Искупление»: там проба держит байтовую опись лановых источников и корпуса
(`.github/workflows/atonement-corpus-integrity.yml`, `atonement_reshoot_state.py`), и один
вставленный пробел требует пересъёма всего снимка. Четыре склейки в `ИСКУПЛЕНИЕ/data/` и
`ИСКУПЛЕНИЕ/synthesis/` починены, после чего снимок переснят штатной командой
(`atonement_reshoot_state.py --write` → `--check: PASS`); новые правки в этом лане инструмент
пропускает как `lane-blocked` и оставляет его собственной круговой процедуре.

| Файл | Склеек | Состояние |
|---|---:|---|
| `БИОГРАФИИ/08_DRIVE_LIBRARY_AND_RIGHTS_LEDGER.md` | 52 | починено |
| `БИОГРАФИИ/Стивен Чарнок/02_LIFE_CHRONOLOGY_AND_DATE_CONFLICTS.md` | 24 | починено |
| `БИОГРАФИИ/Стивен Чарнок/06_CORPUS_ACCESS_MATRIX_AND_LOCATORS.md` | 7 | починено |
| `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` | 3 | починено |
| остальные 6 файлов | 9 | починено |
| `БИОГРАФИИ/Стивен Чарнок/16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN.md` | 277 | `receipt-blocked` |
| `data/charnock-series-editorial-plan-v1.json` | 96 | `receipt-blocked` |
| `БИОГРАФИИ/Стивен Чарнок/00_README_AND_NAVIGATION.md` | 29 | `receipt-blocked` |
| `data/charnock-biographical-anchors-v1.json` | 28 | `receipt-blocked` |
| остальные 5 файлов | 16 | `receipt-blocked` |

Происхождение: почти всё — один массовый проход `c6a6ea67` «organize biographies and preserve
audited Charnock research» (26.10.2026), где-то `7e622af2`, `9944ecd2`, `3a1a3fb8`, `f10f9268`.
История репозитория не переписывалась: коммит назван, но остаётся на месте.

Границы: чинится только форма «слово+число+слово». Число, замыкающее слово (`Кор80`), не
трогается — та же форма у законных цитат `Мф5`, `1Кор`. Возвращены пробелы, а не иное
повреждение того же прохода (кавычки, абзацы, маркеры сносок). Наличие окна в истории
доказывает раздельность слов, но не верность числа по существу; права, издания и факт чтения
текста не затрагивались.

```bash
python3 -B scripts/audit_text_integrity.py --summary   # 446, все receipt-blocked
python3 -B scripts/audit_text_integrity.py --check     # 0, если чинимых склеек нет
python3 -B scripts/audit_text_integrity.py --repair    # вставка только по доказательству из истории
```

## 13. Объекты Drive: перечитывание у сервера (18.11.2026)

Замыкания `HCR-2026-11-18-01` и `-02` ссылаются на объекты Google Drive по `driveFileId` и
заявляют их размер и SHA-256. Заявка проверяема: сервер сам отдаёт `sha256Checksum` в
метаданных файла. Перечитаны восемь объектов из 24 различных, упомянутых в реестре:

| Объект | Заявлено | Сервер сообщил | Итог |
|---|---|---|---|
| `1Vg9tA3uhECDf6uHLdv2_PArcgd7BL70x` (Works 3–5, фрагмент 1/16) | 2 965 B, `5ad0aa52…b0ea` | 2 965 B, `5ad0aa52…b0ea` | совпало |
| `14bfNjtyOgIh7MQV-7yK8I6K2p3AG6dNY` (Rippon 1838, PDF) | 9 297 102 B, `362019ee…1792` | то же | совпало |
| `1uXU3sR6yn8VEUhQWQ_z_ctwtD300-Pwi` (GILL mobile reference) | 40 563 B, `7472a79f…beee` | то же | совпало |
| `1sV3jfs0slLQh1lX6FawkL-It7tob2X10` (00 Navigation, волна 22) | 89 100 B, `c6ce878b…793e` | то же | совпало |
| `1JmhghsHYSS13PF_nVpn4b0jdEc7WrQkT` (01 Witnesses) | 67 556 B, `a74bed26…26fa` | то же | совпало |
| `12btSm2nqtKH7PaI0KbpVeSs2nalWvI5W` (03 Works and Catalogue) | 78 099 B, `7e92a299…8cec` | то же | совпало |
| `1liMd0gBB7tWsYQTqonR_QnglutSPnn1A` (04 Theology and Identity Audit) | 259 911 B, `0ca99267…3aca` | то же | совпало |
| `10q8rOMAWPxUqMRqoR9M-lEYWU8HHvewl` (16 Series and Persons) | 96 664 B, `fb81a207…5c59` | то же | совпало |

Итог: **8/8 совпали, 0 отсутствующих, 0 расхождений**. Байты при этом не скачивались — прочитаны
метаданные; независимый пересчёт содержимого сделан отдельно только для ZIP из `HCR-C1`.

Границы: `sha256Checksum` — заявление Drive, а не пересчёт байтов, поэтому подмена объекта с
обновлением метаданных так не ловится. Проверено 8 из 24 объектов, выборка не случайная (первые по
порядку объекты замыканий 01 и 02). Совпадение хеша не даёт прав на публикацию и не доказывает, что
текст прочитан: `RIGHTS_HOLD`/`PUBLICATION_HOLD` остаются в силе.

## 14. Подписи SHA-256 внутри репозитория (18.11.2026)

Квитанция вида «`00_README_AND_NAVIGATION.md` = `2a8d41c1…`» — это локатор плюс хеш: путь
говорит где, хеш говорит какие байты. Никто эти байты не перечитывал, поэтому хеш мог
описывать прошлую редакцию, другой файл или ничего, а документ продолжал выглядеть сверенным.

Замер `scripts/verify_internal_digests.py`: в **2 416** Markdown-файлах
**2 739** подписей. Состояния (таблица переснята 18.11.2026, см. §20: раньше здесь стояли
шесть состояний с суммой 1 537 — это было верно до разделения `git-object-id` и
`unlabelled-partial`):

| Состояние | Подписей | Что означает |
|---|---:|---|
| `match` | 58 | файл в рабочем дереве хешируется **ровно в заявленное** значение |
| `stale` | 27 | файл есть, но байты уже другие |
| `external` | 258 | назван файл, которого в дереве нет (скачанный PDF, скан) |
| `external-drive` | 920 | строка про объект Drive с репозиторным именем (в таблице есть Drive-ID) |
| `ambiguous` | 8 | хешей и путей в строке не поровну — утверждать нечего |
| `unclaimed` | 514 | хеш стоит один: строка не называет файла (§18 разбирает их по причине) |
| `git-object-id` | 789 | 40-значный хеш без метки SHA-1: это объект Git, а не файл |
| `unlabelled-partial` | 165 | подпись разобрана частично: ни пути, ни метки алгоритма |

Сопоставление хеша с путём — позиционное и только при равенстве счётчиков; строка, где
хешей больше, чем путей, не утверждает ничего (`ambiguous`), кроме одного частого случая: два
хеша и один путь — это квитанция «старый хеш / хеш на момент записи», и тогда проверяются оба.

Важное разделение: **ни одна просроченная подпись не находится в «живом» документе**. Все 27
распадаются на два типа документов, которые по своей природе фиксируют момент:

| Документ | Просрочено | Почему это не дефект документа |
|---|---:|---|
| `СЕРИЯ СЕРДЦЕ/V68…V70_SINGLE_ZIP_MANIFEST.md` | 21 | манифест описывает байты **своего** выпуска; три из них хешируют сами себя, что не может совпасть никогда |
| `БИОГРАФИИ/Стивен Чарнок/supplemental-audits/agent6/Чарнок_ED-08_handoff_preparation.md` | 6 | таблица прямо называется «Хеш в квитанции wave40 — текущий хеш»: она сама сообщает, что квитанция разошлась с файлом |

Поэтому `--check` падает только на просроченной подписи **живого** документа: манифест раунда
и хендофф-таблица обязаны устаревать, а живая квитанция — нет. Сейчас таких 0.

Границы: проверяется только целый файл по названному пути. Хеш фрагмента, страницы или
склеенного архива этим не проверяется; подпись, у которой в строке нет пути, остаётся
`unclaimed` и не считается ни подтверждённой, ни опровергнутой. Совпадение хеша удостоверяет
байты, а не факт чтения, не издание и не права.

```bash
python3 -B scripts/verify_internal_digests.py --summary
python3 -B scripts/verify_internal_digests.py --check      # 1 на просрочке в живом документе
python3 -B scripts/verify_internal_digests.py --only stale
```

### 14.1. Машинные реестры JSON (18.11.2026)

Тот же вопрос к JSON: запись вида `{"path": "data/x.json", "sha256": "…"}` утверждает байты
файла в дереве. Пара принимается только когда в объекте ровно один 64-хеш и ровно одна
строка-путь; иначе запись не утверждает ничего и не проверяется.

Итог: **2 329** таких записей. Из них 421 называет файл вне дерева (скачанный PDF, `_work/…`),
1 908 — файл в дереве. Из 1 908 **58** всё ещё совпадают с текущими байтами, **1 850** — нет.

Это не 1 850 дефектов: реестр хранения фиксирует байты на момент передачи, и файлы после этого
менялись (часть — моими же правками пробелов в §12, часть — содержательными правками других
ланов). Практический вывод обратный: **машинный реестр нельзя читать как «файл сейчас такой»** —
он описывает прошлое состояние. Поэтому JSON-проход в CI не гейтится; гейт стоит только на живых
Markdown-документах (§14).

### 14.2. Короткие хеши: SHA-1 и MD5 (18.11.2026)

Язык квитанций не заканчивается на SHA-256. В корпусе есть **789** значений из 40 hex-знаков
и **172** из 32, и их тоже никто не перечитывал. Но первая же проверка показала, что читать их
как подписи байтов нельзя: почти все 40-знаковые — это **идентификаторы объектов Git** (коммиты
и blob-ы снимков, часть из них в чужих репозиториях).

Проверка «хеш рядом с именем файла» на этом материале дала бы **12 ложных обвинений** именно
в живых документах: закрывающий отчёт `DEEP_PASS_XXV…CLOSEOUT.md` перечисляет в колонке «Коммит»
шесть коммитов рядом с именами файлов, `apostasy/README.md` пишет «Parts I/II/V at/after `<sha1>`»,
`docs/research/reformation/independent_review_packets.md` — «`main=<sha1>`», а `PORTFOLIO/AUDIT_RU.md`
приводит Git blob словаря из **другого** репозитория (`gb-vosk-tts`) рядом с упоминанием `AGENTS.md`.
Ни одно из этих значений не утверждает байты соседнего файла.

Поэтому правило обратное: короткое значение считается подписью байтов **только когда это
сказано словами** (`sha1`, `sha-1`, `md5`, `checksum`, `контрольная`) и в строке нет
`commit`/`коммит`/`blob`/`main=`/`at/after`. Остальные 40-знаковые помечены как `git-object-id`
и не обвиняются; 32-знаковые без разметки — `unlabelled-partial` (могут быть обрезанным sha256).

Итог: размеченных коротких подписей **10** (sha1 — 3, md5 — 7), и **все десять** указывают на
объекты вне рабочего дерева (PDF и djvu с Drive, чужие репозитории) — сверять локально нечего.
Совпадений с файлами дерева среди них нет, просроченных нет. Для 40-знаковых значение
сверяется и как обычный sha1, и как Git blob (`blob <len>\0` + байты), потому что оба —
определённые функции файла, а не догадка.

Ограничение то же, что в §14: совпадение подтверждает байты, но не прочтение, издание и права;
`external` означает «здесь нечего хешировать», а не «подпись неверна».

## 15. Дубли-близнецы: один документ под двумя именами (18.11.2026)

Вопрос, которого не задавал ни один приём: два файла в разных местах могут быть **одним
документом**. Оба выглядят целыми, оба цитируются, правка приходит в один из них — и второй
продолжает отвечать старыми словами. Ни одна квитанция при этом не просрочена: копии ничего
не утверждают друг о друге.

Сравнение шло по тексту, не по именам: 8-словные шинглы, кандидаты из фиксированной выборки
сигнатуры (детерминированно, порядок входа не влияет), затем точная мера Жаккара по полному
множеству. Сколько документов сравнено и сколько Markdown просканировано — в таблице ниже: эти два
числа печатаются из отчёта, а не переписываются в прозу (файлы короче 200 слов отсечены).

**Итог — в таблице ниже.** Порог 0.5; пары выше него перечислены по состояниям, а всё,
что не просто общий текст, названо поименно с измеренным перекрытием.

<!-- twins-states:begin -->
| Показатель | Значение |
|---|---:|
| сравнено документов | 2 394 |
| документов в корпусе | 2 418 |

| Состояние | Пар | Что это |
|---|---:|---|
| `identical-text` | 3 | дословно один текст (байты тоже совпадают) |
| `near-identical` | 1 | почти дословно: один текст вложен в другой |
| `superset` | 2 | надмножество: дополнение сохранило базу |
| `shared-text` | 6 | общие блоки и линии версий, не копии |

| Пара | Состояние | Перекрытие |
|---|---|---:|
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/08_LOGIC_AND_RHETORIC_OF_1COR11_2_16.md` ↔ `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/27_LOGIC_AND_RHETORIC_2026-08-09.md` | `identical-text` | 1.000 |
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/13_ADVERSARIAL_AND_LIBERAL_READINGS_DOSSIER.md` ↔ `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/24_ADVERSARIAL_AND_LIBERAL_READINGS_2026-08-09.md` | `identical-text` | 1.000 |
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/14_VERSE_BY_VERSE_SYNOPSIS_AND_STATUS.md` ↔ `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/28_VERSE_BY_VERSE_EXEGESIS_2026-08-09.md` | `identical-text` | 1.000 |
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/04_OT_AND_JEWISH_BACKGROUND_DOSSIER.md` ↔ `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/30_OT_AND_JEWISH_BACKGROUND_SUPPLEMENT_2026-08-09.md` | `near-identical` | 0.909 |
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/10_PRAYER_PROPHECY_AND_1COR14_34_RECONCILIATION.md` ↔ `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/29_WOMEN_PRAYING_VS_1COR14_34_2026-08-09.md` | `superset` | 0.739 |
| `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/osk_update_h/obratnaya_storona_kafedry_FINAL_PACKAGE/02_RESEARCH_BY_VERSION/v0_foundation_methodology/research_obratnaya_storona_kafedry_v0_5.md` ↔ `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/osk_update_h/obratnaya_storona_kafedry_FINAL_PACKAGE/02_RESEARCH_BY_VERSION/v0_foundation_methodology/research_obratnaya_storona_kafedry_v0_6.md` | `superset` | 0.706 |

Пар выше порога: **12**.
<!-- twins-states:end -->

Все пары, кроме одной, лежат **внутри одного корпуса** (1 Кор. 11, «Обратная сторона кафедры»,
STEVE_LAWSON). Скрытого дублирования между корпусами на этом уровне сходства нет — это
отрицательный результат, и он тоже результат.

**Что действительно нашлось.** Три пары дословно совпадают, и корпус это фиксирует строкой
мастер-индекса: `27` — «дубль файла 08», `28` — «дубль файла 14», `30` — «supplement к 04».
Но третья дословная пара — `13_ADVERSARIAL_AND_LIBERAL_READINGS_DOSSIER.md` и
`24_ADVERSARIAL_AND_LIBERAL_READINGS_2026-08-09.md` — в индексе стоит как самостоятельный
`PASS-1`-документ без пометки о дубле. Это **открытый пункт** для лана, владеющего индексом:
здесь нечего «исправлять» инструментом, потому что правка мастер-карты — решение владельца.

**Почему объявление проверяется узко.** Строка считается объявлением, только если она называет
один файл и указывает на другой — именем или собственным сокращением лана (`файла 08`, `к 04`).
Голые числа не принимаются: строка `Лк 24:13` содержит и «24», и «13» и не объявляет ничего —
первая версия инструмента на этом дала ложное объявление ровно для пары 13↔24. Версия в имени
(`v0_5`/`v0_6`, `V3`/`V4`) считается объявлением сама по себе: имена говорят, что это поколения
одного документа.

**Ограничения.** Сходство — мера перекрытия слов, а не смысла: пересказ того же материала
сюда не попадает, а общий блок цитат может сблизить разные документы. Порог 0.5 отсекает
пересказы осознанно. Байтовое совпадение подтверждает копию, но не говорит, какая из копий
каноническая. `--check` (падение на необъявленной дословной паре) **не подключён** в CI: сегодня
он падал бы на паре 13↔24, а это открытый пункт, а не повод править чужой индекс.

    python3 -B scripts/audit_document_twins.py --summary
    python3 -B scripts/audit_document_twins.py -o data/document-twins-2026-11-18.json
    python3 -B scripts/audit_document_twins.py --only identical-text

## 16. Самодатировка: дата в заголовке против истории Git (18.11.2026)

Заголовок «**Обновлено: 13.11.2026**» или «**As of 2026-10-26**» — утверждение о
собственной актуальности документа: читатель вправе принять всё ниже написанное за истину на
этот день. Ничто это не проверяло, поэтому файл может правиться неделями, а дата в нём
остаётся прежним вторником.

Сколько документов ставит дату себе в первых 15 строках и сколько их всего — в таблице ниже,
из отчёта.

<!-- stamps-states:begin -->
| Показатель | Значение |
|---|---:|
| документов со своей датой | 17 |
| документов в корпусе | 2 418 |

| Состояние | Документов |
|---|---:|
| `current` — последний коммит в тот же день | 9 |
| `edited-after-stamp` — файл менялся после своей даты | 6 |
| `stamp-ahead-of-history` — дата позже любого коммита | 2 |
| `stamp-in-future` — дата позже сегодняшней (невозможна) | 0 |

**Отредактированы после своей даты** (с темой последнего коммита как уликой):

| Документ | Дата в тексте | Последний коммит | Что пришло позже |
|---|---|---|---|
| `PORTFOLIO/PORTFOLIO_EN.md` | 2026-11-03 | 2026-11-05 | *docs(portfolio): align visual direction with published cases (EN)* |
| `STEVE_LAWSON/_START_HERE.md` | 2026-11-13 | 2026-11-15 | *research(lawson): reconcile November 2026 elders' letter evidence* |
| `БИОГРАФИИ/Джон Гилл/31_GILL_DEPT_MASTER_MAP.md` | 2026-07-07 | 2026-10-26 | *research: organize biographies and preserve audited Charnock research* |
| `ИСКУПЛЕНИЕ/fathers/00_FATHERS_AUTHORITY_2026-10-07.md` | 2026-10-08 | 2026-11-16 | *research(atonement): consolidate Agent 5 verified historical primary sources (#526)* |
| `ИСКУПЛЕНИЕ/fathers/10_ORIGINAL_LANGUAGE_VERIFICATION.md` | 2026-10-08 | 2026-11-16 | *research(atonement): consolidate Agent 5 verified historical primary sources (#526)* |
| `СЕРИЯ СЕРДЦЕ/61_BOOK_ARCHITECTURE_V2_CHAPTERS_AND_RESEARCH_TASKS.md` | 2026-07-31 | 2026-08-01 | *Close heart-series source verification gaps (#77)* |
<!-- stamps-states:end -->

Это **не приговор**: лан может законно дописать раздел с более поздней датой, а правка
нумерации или пробелов вообще не меняет существа. Инструмент поэтому печатает дату, день
последнего коммита и его тему — и на этом останавливается. Дату он **не переписывает**:
поставить «сегодня» значило бы изготовить ровно ту свежесть, которую проверка и ставит под вопрос.
Два файла `ИСКУПЛЕНИЕ/fathers/` при этом ещё и связаны квитанциями лана, так что руками в них
не лезем тем более.

**`stamp-ahead-of-history`** — два случая, где дата в тексте новее истории файла
(`SUNO_HYMNS/HANDOFF_FOR_NEXT_AGENT.md`: 2026-10-26 при последнем коммите 25.10;
`ИСКУПЛЕНИЕ/fathers/06_METAPHOR_AND_MODEL_MAP.md`: 2026-11-03 при 02.11). Обычно это дата,
поставленная перед коммитом самой правки; она не ложна, но и не подтверждена историей.

**Что исключено и почему.** Строки таблиц и строки со ссылкой не считаются самодатировкой:
`| Living Heritage Homeschool — current Terms of Use, last updated 2026-05-17 |` датирует **чужой**
документ, а не этот. Из 36 строк с датой в шапке так отсеялись 19.

**`--check`** падает только на невозможной дате (позже сегодняшней); сегодня таких 0, поэтому
шаг в CI **отчётный**, а не гейтовый.

    python3 -B scripts/audit_state_stamps.py --summary
    python3 -B scripts/audit_state_stamps.py -o data/state-stamps-2026-11-18.json
    python3 -B scripts/audit_state_stamps.py --only edited-after-stamp

## 17. Строки Drive-реестра: что сказал Drive и что лежит локально (18.11.2026)

> Счётчики этого раздела — на 7 опрошенных id из 92. Полный опрос 92/92 и найденный при нём
> дефект парсера — в §19; §17 не переписывается, разница показана рядом.

Строка реестра вида

    | `00_README_AND_NAVIGATION.md` | `1sV3…X10` | 89100 | `89ad08d7…` |

утверждает сразу три вещи: объект есть в Drive, его размер и MD5 — вот такие, и **локальный**
файл из той же строки имеет ровно эти байты. Ни одна из трёх не перечитывалась.

Проверка соединила три источника: строки реестра (92 строки, 92 разных id), ответ Drive по
семи id (снапшот [`data/drive-ledger-snapshot-2026-11-18.json`](../../data/drive-ledger-snapshot-2026-11-18.json))
и md5 локальных байтов.

| Сторона | Состояние | Строк |
|---|---|---:|
| Drive | `drive-verified` — размер и MD5 совпали с приложенным | **7** |
| Drive | `drive-not-sampled` — id в этом проходе не запрашивался | 85 |
| Локально | `local-moved-on` — файл есть, байты другие | **13** |
| Локально | `local-ambiguous` — имя встречается в 4 местах отдела, выбирать нельзя | 4 |
| Локально | `local-unresolved` — строка не называет локального файла | 75 |

**Что это значит.** Все семь перечитанных объектов совпали с реестром — Drive действительно
хранит те байты, о которых написано. И одновременно **все 13 однозначно разрешённых локальных
файлов выросли** с момента загрузки: `04_CHARACTER_MINISTRY_AND_THEOLOGY.md` 259 911 → 406 668,
`16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN.md` 96 664 → 887 094 (в девять раз),
`03_WORKS_EDITIONS…` 78 099 → 116 999. Ни один из них не равен своему реестровому md5.

Это не 13 ложных подписей. Реестр фиксирует **момент загрузки** (в подписях стоят `wave 22`,
`wave 28`, `rev 21`), и он верен: в момент волны локальные байты и байты Drive совпадали.
Неверно другое — читать реестр как «зеркало равно локальному файлу сейчас». Сегодня отдел
переписан, и последняя строка реестра описывает волну, а не текущее состояние.

**Открытый пункт (для владельца лана, не для инструмента):** чтобы закрыть вопрос зеркала,
нужно загрузить текущие файлы и снять новый ряд подписей; старые строки при этом остаются
историей и переписывать их нельзя — иначе исчезнет след того, что было проверено.

**Ограничения, честно.** Байты объектов не скачивались — сверялся `md5Checksum` из ответа
Drive, то есть утверждение сервера о хранимом объекте. Из 92 id перечитано 7 (по одному вызову
на объект; фильтр по `id` язык запросов Drive не принимает, а листинг папки вернул 0 файлов —
объекты лежат в разных папках). 4 имени из 17 неоднозначны внутри отдела: инструмент сообщает
об этом и **не выбирает** файл по имени, потому что выбор по имени — это уже догадка.

    python3 -B scripts/audit_drive_ledger.py --snapshot data/drive-ledger-snapshot-2026-11-18.json --summary

## 18. Хеши без имени файла: 514 «бесхозных» (18.11.2026)

Прибор разобрал 1 537 подписей; 514 из них стоят в строке, где нет ни одного имени файла.
Это не значит «не проверено» — это значит, что проверять нечего **до тех пор, пока не сказано,
что именно подписано**. Причина записана для каждой строки, и распределение оказалось
содержательным:

| Причина | Хешей | Что подписано |
|---|---:|---|
| `labelled-no-path` | 205 | объект назван словами, но это не файл дерева: `Feed SHA-256`, Vimeo `900633606`, ленты и фиды |
| `bare-hash` | 141 | хеш стоит один: объект назван другой колонкой (`202641339349303874_public.xml`, IRS) или строкой выше (`bytes/pages/SHA: 542143 / 14 / 3d33…`) |
| `short-digest-no-path` | 95 | SHA-1/MD5 с разметкой, но без имени файла |
| `artifact-not-in-tree` | 59 | ZIP, XML, PDF, скан, факсимиле — объектов нет в дереве |
| `media-segment` | 12 | отрезок записи: `16:30–19:35 SHA-256` |
| `corpus-digest` | 2 | дайджест состояния корпуса («effective authority digest»), не файла |

**11** из 514 имеют то же значение, что и подпись **с путём** в другом документе. Это
перекрёстная ссылка: сама строка объекта не называет, но значение в репозитории не безызвестно
и проверено там, где путь указан.

**Почему нельзя просто «дотянуть» путь из соседней строки.** Проверена и эта гипотеза: ровно
у 18 строк предыдущая непустая строка называет один файл и не содержит хеша. Выборка показала,
что это по большей части ссылки на **внешние** файлы, а часть «путей» — обрывки URL
(`…81.pdf`) и скобок (`(HOLD_SOURCE_SWEEP_2026-11-11.md`). Правило «возьми путь сверху» дало бы
подписи, которых документ не делал, поэтому оно отклонено — как и в случае с Drive, где имя
в отделе встречается четырежды.

**Итог.** 514 хешей нельзя проверить, потому что в этих строках не сказано, что подписано;
503 из них указывают на объекты вне дерева (фиды, медиа, артефакты, дайджесты состояния),
11 подтверждаются перекрёстно. Ни один из 514 не является подписью файла репозитория, и ни
один не был бы проверен даже при идеальном соединении с сетью — сверять пришлось бы фид и
медиа, а не файл.

**Ограничение.** Классификация — по словам строки, а не по смыслу документа; строка с
«архивом» в другом значении попадёт в `artifact-not-in-tree`. Поэтому классы — это карта
поверхности, а не приговор: `--check` на них не гейтится и не должен.

    python3 -B scripts/verify_internal_digests.py --only unclaimed
    python3 -B scripts/verify_internal_digests.py -o data/internal-digests-verified-2026-11-18.json

## 19. Drive-реестр: опрошены все 92 id, и один счётчик пришлось снять (18.11.2026)

В §17 было 7 подтверждённых id и 85 непрошеных; «не опрошено» — это не «не сходится», но
читать так приходилось. Здесь опрос доведён до конца: **92 из 92**.

Отдельные `get_file` на каждый id (фильтра по id в языке запросов Drive нет), снапшот
`data/drive-ledger-snapshot-2026-11-18.json` перезаписан ответами по всем объектам,
отчёт `data/drive-ledger-audit-2026-11-18.json` переснят.

| Что сверялось | Ответ |
|---|---|
| Размер и md5Checksum совпали с записью реестра | **88 из 88** строк, где записан MD5 |
| Размер и sha256Checksum совпали с записью реестра | **4** строки (wave40), где записан SHA-256 |
| Всего подтверждено объектных тождеств | **92 из 92** |
| Расхождений размера, MD5 или SHA-256 | **0** |

**Опрос сразу же поймал ошибку в моём собственном парсере.** Четыре строки wave40 несут в
колонке сверки 64-значный SHA-256; регулярное выражение брало первые 32 знака и называло это
MD5 — и первые четыре «расхождения» оказались не расхождениями, а половиной чужого хеша.
Ошибка была бы опубликована как обвинение четырём строкам реестра. Проверка: у всех четырёх
`modifiedTime` лежит в одной секунде `2026-10-25T22:07:36–37Z`, то есть объекты загружены
одной волной, а не перезаписаны позже.

Что исправлено: границы хеш-токена (`(?<![0-9a-fA-F])…(?![0-9a-fA-F])`), колонка
классифицируется по длине — 32 → MD5, 64 → SHA-256. Это закрыто тестами `ChecksumColumnTests`; сколько их —
печатает прогон, а не эта строка.

**Вторая ошибка того же прохода, исправленная в тот же день.** Первая редакция этого раздела
утверждала, что «Drive отдаёт только MD5», и потому четыре строки wave40 были записаны как
`drive-size-only` — размер подтверждён, байты нет. Это неверно: Drive возвращает и поле
`sha256Checksum`. Оно запрошено для всех четырёх объектов, и все четыре значения совпали с
записью реестра байт в байт:

| Объект wave40 | sha256Checksum Drive = запись реестра |
|---|---|
| `CHARNOCK_FULL_BOUNDED_RESEARCH_wave40_2026-10-26.zip` | `3bda1d76…c9bc41` |
| `00_README_AND_NAVIGATION_wave40_2026-10-26.md` | `21a2e1af…c2a863` |
| `16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN_wave40_2026-10-26.md` | `41d98132…16f313` |
| `charnock-biographical-anchors-v1_wave40_2026-10-26.json` | `f35b1fd7…28775784` |

Поэтому счётчик раздела — не «88 подтверждено, 4 только по размеру», а **92 из 92**. Утверждение
«только MD5» снято, а не переписано молча: оно стояло в этом же файле несколько часов и было
бы прочитано как граница возможного.

Границы этого раздела те же, что и в §17: **байты не скачивались** — сверялись серверные
checksum-поля (`md5Checksum`, `sha256Checksum`), а не содержимое; ничего не загружалось и не
менялось на Drive. Подтверждается тождество объекта, а не прочтение документа.

Локальная сторона от полного опроса не изменилась и не могла измениться: 17 строк называют
локальный файл, из них **13 `local-moved-on`** (файл вырос после волны), **4 `local-ambiguous`**
(имя встречается в отделе больше одного раза), **75 `local-unresolved`**. Строка реестра — это
момент загрузки; «сходится с Drive» и «равно сегодняшнему файлу» — разные утверждения, и
опрос закрывает только первое.

**Осталось открытым:** актуальность локального зеркала — её не снимает ни один опрос, только
новая загрузка текущих редакций с новыми подписями (действие владельца лана).

## 20. Регистр цитировал сам себя: восемь счётчиков были просрочены (18.11.2026)

Весь этот документ ищет один дефект: документ утверждает число, а файл, из которого число
взято, с тех пор изменился. Писали его так же, как всё остальное — руками. Поэтому здесь
то же самое и нашлось.

`scripts/audit_register_claims.py` объявляет 32 счётчика, у каждого — поле в артефакте,
которое он обязан повторять. Проверка идёт в обе стороны: счётчик сверяется с артефактом,
а если строки с таким ярлыком больше нет — это `anchor-missing`, а не тишина.

**Что нашлось при первом прогоне:**

| Раздел | Напечатано | В артефакте |
|---|---:|---:|
| §2, канонические упоминания `LOCATOR_HOLD` | 1 966 | 1 967 |
| §2, канонические упоминания `ARCHIVE_HOLD` | 1 408 | 1 410 |
| §2, канонические упоминания `EVIDENCE_HOLD` | 1 290 | 1 291 |
| §2, строки без явного состояния (`unmarked`) | 5 952 | 5 956 |
| §13, `external` | 248 | 258 |
| §13, `external-drive` | 778 | 920 |
| §13, `ambiguous` | 7 | 8 |
| §13, `unclaimed` | 419 | 514 |

Восемь чисел, и §13 просрочен не на единицы: `external-drive` вырос со 778 до 920, `unclaimed`
с 419 до 514 — это ровно та разница, которую внесло разделение состояний `git-object-id` и
`unlabelled-partial` и уточнение классов в §18. Сумма шести старых строк (1 537) была верна,
когда писалась, и перестала быть верной молча — потому что таблица в прозе не связана ни с
чем.

Таблица §13 теперь из восьми состояний с суммой **2 739**, и она же под проверкой.

### 20.1. Машинный срез §2 и таблица по корпусам больше не пишутся руками

Первый же прогон проверки после её добавления показал, почему это обязательно. Я дописал §20,
добавил два файла инструментов — и `файлов просканировано` стало 3 112 вместо 3 110,
`не могут` упоминания сдвинулись на единицы. Замер честно изменился, а таблица в тексте
осталась прежней: тот же дефект, но вызванный моей же правкой за десять минут.

Поэтому §2 **генерируется** из инвентаря (`--write-slice-table`), как и таблица по корпусам
(`--write-corpus-table`); в тексте остались только маркеры. `--check` падает, если блок
разошёлся с артефактом.



В §2.1 было 25 строк «корпус → файлы → упоминания», снятых однажды. При пересборке инвентаря
они разошлись: `docs/` 96 → **97**, `ИСКУПЧЕНИЕ/` 152 → **153**, `БИОГРАФИИ/` 48 → **55**,
`1КОРИНФЯНАМ_11_ПОКРЫВАЛО/` 217 → **293** упоминаний. Такая таблица всегда будет отставать
на одну пересборку, поэтому она генерируется из `byCorpus` (`--write-corpus-table`), а
`--check` падает, если закоммиченный блок расходится с инвентарём.

### 20.2. Что это не значит

Это не значит, что числа были выдуманы: каждое было верным в свой момент, и §19 показывает,
как тот же дефект ловится у других. Это значит, что **счётчик в прозе — утверждение без
срока годности**, и держать его можно только проверкой. Проверка стоит в CI
(`--check`), и её падение означает именно «регистр отстал от артефакта», а не «артефакт
испортился».

Границы: проверяются только объявленные 32 счётчика и таблица §2.1. Остальные числа в тексте
(например «58 мёртвых ссылок» в §8, «2 385 документов» в §15) — утверждения без машинного
поля, их проверка была бы подгонкой. Это ограничение записано, а не замазано.

## 21. Счётчики в прозе: два утверждения о масштабе были неверны по существу (18.11.2026)

§20 проверял таблицы. Но §1 и §3 начинались словами «одна ось» — и это тоже счётчик, только
записанный словами и потому не попавший ни в одну проверку. Когда закрытий стало 16, фраза
«закрыта одна ось» перестала быть верной, не изменив ни одной цифры.

Теперь проверяются и числа внутри предложений — утверждения с шаблоном, полем в артефакте и,
где нужно, ссылкой на раздел, который переснял значение. Сколько их, здесь не сказано: число
печатает сам инструмент (`--summary`), и всякое его повторение в тексте — тот же дефект.

**Что нашлось:** §1 («закрытие одной проверяемой оси») и §3 («Закрыта **одна ось**») описывали
масштаб работы, которого уже нет. Первым побуждением было подставить верное число — и проверка
сразу показала, почему это плохо: я исправил «одну ось» на **16**, дописал этот раздел, добавил
запись в реестр закрытий — и число стало **17** в ту же минуту. Две строки прозы снова разошлись
с артефактом, не успев прожить и получаса.

Поэтому число из этих фраз **убрано**, а не обновлено: §3 говорит, какой была **первая** ось, и
отсылает за перечнем и счётом в §0, который генерируется. Это и есть вывод: счётчик, который
обязан меняться при каждом закрытии, нельзя держать в прозе — только ссылкой на место, где он
считается. В таблице проверяемых утверждений остались прозовые, и ни одно не обязано меняться
от добавления записи.

### 21.1. Состояние `superseded`: история не переписывается

Два утверждения в тексте — «объекты Drive: 8 из 24 перечитаны» (§11 и подтверждение `C4`) —
были верны 18.11.2026 и перестали быть верными в §19, где опрошены 92 из 92. Стирать их нельзя:
это запись о том, что именно было проверено тогда, и она объясняет, почему §19 вообще
понадобился.

Поэтому у проверки есть третье состояние, кроме `match` и `stale`: **`superseded`**. Утверждение
объявляется переснятым, но только при двух условиях — указан раздел (`§19`), и этот раздел
**находится ниже** утверждения в файле. Если раздел удалён или стоит выше, состояние становится
`superseded-target-missing` и проверка падает. Ссылка «это устарело, см. §N» без §N — не
объяснение, а отговорка.

### 21.2. Границы

Проверяются объявленные утверждения — табличные и прозовые; их число печатает `--summary`, и в
тексте оно не повторяется. Остальные числа по-прежнему без машинного поля — их список не
изменился, и §20.2 остаётся в силе. Проверка не судит, **должно**
ли число быть таким; она ловит только расхождение с артефактом и отсутствие адреса, по которому
живёт актуальное значение.

## 22. Ссылки: отчёт стал артефактом, а не выводом в терминал (18.11.2026)

§8 начинался с замера: «**2 416** Markdown-файлов, **8 914** ссылок — `resolves` 2 856,
`external` 5 974…». У `audit_relative_links.py` давно был флаг `-o`, но его отчёт никуда не
коммитился: замер жил только в этой фразе. Проверить её было нечем — не потому, что число
неверное, а потому, что сверять было не с чем.

Теперь отчёт лежит в `data/relative-links-audit-2026-11-18.json`, таблица §8 **генерируется** из
него (`--write-links-table`), а шаг CI сверяет закоммиченный отчёт с новым прогоном (`cmp`), так
что таблица не может честно цитировать вчерашний запуск.

**Что показал первый честный замер:** `resolves` 2 861 (в тексте стояло 2 856), `external`
5 984 (стояло 5 974); `missing` 58 — совпало. Сдвиг не от правки ссылок, а от того, что файлов
в дереве стало больше: те же права, та же проверка, другой снимок.

### 22.1. Две ловушки, найденные при сборке

1. **Счётчик должен иметь владельца-артефакт.** Числа §8 нельзя было проверять, пока они жили
   в прозе: `--strict` знает про «нет необъяснённых», но не про «сколько всего». Отчёт - это и
   есть владелец.
2. **Ярлыки должны быть уникальны в документе.** Первая версия таблицы §8 назвала строки
   `external` и `missing` — и проверка тут же выдала `anchor-ambiguous`: в §13 уже есть
   `external` (248 → 258 подписей). Две строки с одним именем и разными значениями — это не
   утверждение, а двусмысленность; строки переименованы в «ссылок `external`».

### 22.2. Когда гейт срабатывает, а когда нет

Рабочий процесс запускается по изменению перечисленных путей — регистра, артефактов, самих
инструментов, — а не по любому изменению контента. Поэтому расхождение может накапливаться
между этими событиями, и первое же касание триггерного пути его обнажает: ровно так и вылезли
восемь чисел §20. Это ограничение честнее назвать, чем делать вид, что «проверено» означает
«проверяется на каждом коммите».

## 23. Якоря: «36 ссылок с фрагментом» оказались верны — но проверить это было нельзя (18.11.2026)

§11 утверждал, что ссылок с фрагментом в репозитории тридцать шесть и что после правки
резолвятся все. Проверить это было нечем по двум причинам сразу: инструмент ссылок относил любой `#anchor`
к `external` («внутристраничная ссылка») и не считал его вовсе, а ссылки вида `файл.md#раздел`
попадали в общий `resolves` без отдельного счёта. Число жило в прозе, подтверждённое только
самим собой.

Теперь инструмент различает два состояния и ведёт перепись:

Перепись ведётся в отчёте и печатается в §8; копии этой таблицы здесь больше нет — она
разошлась с отчётом сразу после первого же слияния (появились ссылки с фрагментом в чужих
документах), и разошлась молча. Итог на 18.11.2026: ссылок с фрагментом 36, из них 18
внутристраничных и 18 межфайловых, все резолвились. Это запись о моменте, а не счётчик.

Число совпало с тем, что стояло в тексте с самого начала — но это совпадение теперь
**измерено**, а не заявлено. Заодно счёт `external` уменьшился с 5 984 до 5 966: 18
внутристраничных ссылок перестали считаться внешними.

### 23.1. Почему мёртвый якорь — отчёт, а не дефект

`missing-fragment` не входит в `defects` и не валит `--strict`. Причина не в снисходительности:
слаги GitHub мы здесь воспроизводим приблизительно (регистр, пунктуация, дефисы, `?`/`#` в
заголовках). Гейт на собственной аппроксимации превращал бы догадку в приговор — ровно то,
чего этот регистр избегает везде, где сверка неточна. Поэтому якорь **считается и
показывается**, но вердикт по нему не выносится, а в отчёте это записано рядом с полем.

Граница честная: если внутристраничный якорь умрёт, `--strict` этого не заметит. Компенсация —
счётчик `фрагментов не резолвится` в таблице §8: он виден и генерируется, а не тонет в тексте.

## 24. Числа, спрятанные в именах: «134 значения / 39 написаний» были и в заголовке, и нигде не проверялись (18.11.2026)

У пункта «осталось открытым» не было имени. Его `class` был одновременно **названием** и
**измерением**: «Неканонические значения `holds` (134 значения / 39 написаний)». Строка §0
печаталась из этого поля, то есть генерируемая карта закрытий повторяла число, которое никто не
измерял, и выглядела при этом проверенной.

Дальше — хуже, и это нашлось при сверке: §2 в строке «Гигиена машинных реестров» говорил
**39** файлов с массивом `holds`, а инвентарь — **38**. Девять цифр в §5, шесть в таблице классов
§9, вся таблица распределения §9 и число в §2 — всё это были копии одного и того же замера,
сделанные руками, и одна копия уже была неверна.

### 24.1. Что сделано

1. **У открытых пунктов появилось имя.** `notClosed` теперь `id` + `title`, а числа из `title`
   запрещены тестом: число внутри имени — это счётчик без поля, он стареет молча. §0 печатает
   `OPEN-HOLDS-VOCABULARY` и название, а не предложение с измерениями внутри скобок.
2. **Числа переехали в одно место.** §5 больше не дублирует распределение — он отсылает в §9,
   где числа стоят под проверкой. Это убрано, а не исправлено: дубль, исправленный однажды,
   разойдётся снова.
3. **Обе таблицы §9 генерируются** из `hold-value-mapping-proposal-v1.json` (маркеры
   `hold-classes` / `hold-values`, `--write` / `--check`), а не переписываются из вывода
   инструмента в текст.
4. **Новые утверждения под проверкой:** число JSON-файлов, сумма значений `holds`, число
   неканонических значений, число написаний и строка §2. Плюс `totals.jsonHoldsTotal` в инвентаре,
   чтобы сумма имела поле, а не память.

Итог этого шага: число 38 в §2 совпало с инвентарём после исправления, 39 в той строке не
совпадало никогда. Сколько всего утверждений проверяется сейчас, печатает инструмент — в тексте
это число не повторяется (§31).

### 24.2. Почему это не закрывает сам пункт

`OPEN-HOLDS-VOCABULARY` остаётся открытым, и я не стал его закрывать. Закрыто **другое**:
неизмеримость этого пункта. До сих пор нельзя было сказать, изменился ли он; теперь можно —
и видно, что не изменился: переписывать `holds` в machine-SSOT 38 файлов без владельца корпуса
по-прежнему нельзя, а предложение соответствия остаётся `PROPOSAL_ONLY`.

Разница между «пункт открыт» и «пункт открыт, измерен и не двигается молча» — это и есть вся
работа этого раздела. Открытый пункт без имени неотличим от забытого.

## 25. Список триггеров — это утверждение о зависимостях, и его можно проверить (18.11.2026)

§22.2 честно записал: рабочий процесс запускается по изменению перечисленных путей, поэтому
расхождение может накапливаться между событиями, и первое касание триггерного пути его
обнажает. Это ограничение было названо — и оставлено как есть. Но список `paths:` не пожелание:
он говорит, **от чего зависят гейты**. Значит его можно сверить с самими зависимостями.

`scripts/audit_ci_triggers.py` проверяет четыре вещи, все выводимые из файлов:

| Что | Как выводится |
|---|---|
| нет ли дублей в одном списке | сам список |
| совпадают ли `pull_request` и `push` | два списка, которые обязаны быть одним |
| все ли исполняемые скрипты — триггеры | команды `run:` в задачах |
| все ли файлы, которые эти скрипты читают, — триггеры | константы и литералы в исходниках + объявленные транзитивные входы |

**Что нашлось при первом прогоне:**

- **5 дублей**: `hold-closure-registry-v1.json`, `HOLDS_REGISTER_2026-11-18.md` и
  `relative-links-audit-2026-11-18.json` внесены дважды — список правился руками не один раз.
- **Асимметрия**: закоммиченный отчёт ссылок (`data/relative-links-audit-2026-11-18.json`) был
  триггером для PR, но не для `push`. То есть на `main` правка файла, который §8 цитирует и
  сверяет через `cmp`, гейт не запускала.
- **Три файла, читаемые гейтом публикации**, не были триггерами: `physical-rights-ledger`,
  `public-projection-current` и `public-projection-queue`. Очередь публикации ссылается на них
  по содержимому, поэтому правка любого из них меняла вердикт `publication_gate_status.py`,
  не запуская его проверку.

### 25.1. Граница: транзитивные входы объявлены, а не выведены

Соблазн — обойти все артефакты и собрать все пути, на которые они ссылаются. Такой обход
«нашёл» бы 2 416 markdown-файлов, которые отчёт ссылок **наблюдает**, а не читает как вход.
Наблюдение — не зависимость. Поэтому транзитивные входы объявлены в самом инструменте
(`DECLARED_INPUTS`) с причиной и проверяются наравне с выведенными; а то, что принципиально
нельзя выразить списком путей (гейты, читающие весь корпус), названо в `NOT_TRIGGERABLE`.
Оба места — решение, записанное рядом с проверкой, а не умолчание.

### 25.2. Результат

Списки `pull_request` и `push` теперь **один и тот же** отсортированный набор из 49 путей без
дублей, и девять недостающих путей добавлены. Проверка стоит шагом в том же рабочем процессе,
поэтому список, разошедшийся с зависимостями, валит гейт — вместе с самим файлом workflow,
который тоже триггер.

Это не делает гейт всевидящим: правка корпуса, не задев ни одного триггерного пути, по-прежнему
не запустит проверку, и §22.2 остаётся в силе. Изменилось другое — список перестал быть
**надеждой**, что рука не ошиблась: теперь это проверяемое утверждение о том, что читают гейты.

## 26. Таблица §11 была копией отчёта, а отчёт терял половину цитирований (18.11.2026)

§11 — раздел о том, что закреплённый локатор проверяем без доверия автору. Внутри него стояла
таблица из семнадцати строк, **переписанная руками** из `data/pinned-github-locators-verified-2026-11-18.json`:
репозиторий, коммит, путь, размер, SHA-256. Отчёт существовал, а таблица была его копией — то же,
что §22 нашёл у ссылок и §24 у словаря `holds`, но здесь ещё и с числами в прозе поверх.

Две вещи, найденные при сверке:

1. **«в 7 файлах» не имело поля.** Отчёт хранил один адрес на локатор (`file`, `line` первого
   вхождения), поэтому файлов в нём было **6**, а в тексте — 7. Оба числа «верны» по-своему:
   локаторов 17, мест цитирования 19, файлов 7. Но отчёт не мог подтвердить ни одного из них,
   кроме первого.
2. **Второе цитирование было невидимым.** Один объект процитирован в двух документах; удали
   вторую цитату — отчёт не изменится, и никто не заметит.

### 26.1. Что сделано

- **Отчёт версии 2** хранит все места цитирования (`citations`) и считает `totals.citations = 19`
  и `totals.citationFiles = 7`. Перезамер выполнен заново, с сетью, по всем 17 объектам.
- **Таблица §11 генерируется** из отчёта (`--write-pinned-table`), вместе со строкой итогов;
  проза раздела больше не повторяет чисел, а отсылает к таблице.
- **Проверка без сети**: `--check-report` сверяет закоммиченный отчёт с деревом — набор
  локаторов и все места цитирования. Байты требуют сети, и это сказано в самом выводе проверки;
  шаг стоит в CI, поэтому новое или исчезнувшее цитирование не пройдёт молча.
- **Гейт таблиц стал общим.** Раньше `--check` знал ровно три таблицы по именам, и четвёртая
  («будущая») не проверялась бы вовсе: `SLICES` — единственный реестр, а проверка идёт по нему,
  а не по списку, который надо не забыть обновить. Это нашлось сразу: после добавления блока
  §11 в `SLICES` проверка честно выдала `anchor-missing`, потому что блока в тексте ещё не было.

### 26.2. Что подтвердил перезамер

Байты и хеши всех 17 объектов **совпали с прежним отчётом побайтово**: закреплённый коммит
неизменяем, поэтому проверка воспроизводима — и в этом весь смысл закрепления. Заявок по-прежнему
четыре, совпавших — четыре, расхождений и недоступных — ноль.

Это не снимает удержаний: совпадение хеша удостоверяет байты, а не прочтение, не выбор издания и
не права. `ARCHIVE_HOLD`, ось прав и `PUBLICATION_HOLD` остаются как были; §11.2 об этом
сказано раньше и в силе.

## 27. Снимок очереди читал сам себя: ссылочное поле было невоспроизводимо (18.11.2026)

Дефект найден не мной: он пришёл комментарием к PR и воспроизведён на `20a635e9`. Формулировка
была точной, и проверка заняла меньше времени, чем её пересказ.

`publication_gate_status.py` отвечает на вопрос «записан ли rights-id где-то в репозитории».
Индекс собран как один текстовый корпус, из которого исключены база очереди и current-authority —
иначе очередь «нашла» бы собственные id. **Оверлеи и собственный предыдущий отчёт в исключения
не входили.** Следствие ровно такое, как в комментарии: контрольный id без внешних упоминаний
даёт `recordedInRepository=false` при первом построении; если сохранить отчёт по стандартному
пути `data/publication-gate-queue-v1.json` и построить снова, с теми же входами, значение
становится `true` — потому что индекс прочитал предыдущий отчёт, где id присутствует даже при
`false`.

### 27.1. Почему это важнее, чем одно поле

Поле не влияет ни на права, ни на `PROMOTE`: допущенных записей нет ни одной, и это
видно в снимке счётчиком, а не отсутствием строки.
Но это **справочное поле, которое нельзя воспроизвести**: два прогона на одних данных дают
разные ответы, и второй «лучше» первого без всякой причины. Документ, который не воспроизводится,
не может быть проверкой — он может быть только мнением, оформленным как таблица.

Причина в смешении ролей файла: отчёт одновременно **вывод** и **вход** следующего прогона.
Пока он лежал в дереве и не был исключён, он был свидетелем сам себе.

### 27.2. Что сделано

- **Исключения выводятся из композиции**, а не помнятся: база, current-authority, **все оверлеи**
  из `overlaysApplied` и собственный снимок. Функция `pipeline_files()` перечисляет первые три,
  снимок добавляется рядом; принцип один — файл, существующий потому, что очередь назвала id,
  не может удостоверить, что id записан где-то ещё.
- **Что именно не читалось — видно в отчёте**: поле `indexExcluded` (schema 2) перечисляет
  четыре исключённых файла. Исключение, о котором надо помнить, — это не проверка.
- **Регрессия на два последовательных построения** и три контроля: id, названный только в
  оверлее, не свидетель; внешний документ — свидетель; сохранённый отчёт — не свидетель.
  Тесты проверены **в обе стороны**: на прежней версии кода четыре из них падают, на новой
  проходят.
- **Ноль стал счётчиком, а не отсутствием ключа.** `composedCounts` теперь содержит все
  состояния, объявленные властью, с нулями, и `total`. Отсутствующий ключ читается как согласие;
  ноль читается как ноль.
- **Шесть чисел §10 подключены к снимку** (`записей`, `BLOCKED`, `REFERENCE`, `PROMOTE`,
  `отсутствующих`, `потерянных`), а хвост с числом офлайн-тестов из прозы убран: число тестов —
  тоже счётчик, и он уже устарел.

### 27.3. Что это не меняет

Ни одного вердикта: `PROMOTE` по-прежнему ноль, потерянных id по-прежнему ноль, отсутствующих
authority-файлов ноль, записей без записи в реестре прав — три, ни одна не публикационно
допустима. Изменилось одно: теперь снимок **воспроизводится**, и это можно показать двумя
прогонами, а не обещанием.

## 28. Подтверждения носили числа в заголовке — и три из четырёх уже разошлись (18.11.2026)

В §24 я записал правило: число внутри имени — это счётчик без поля, он стареет молча. Правило
применил к открытым пунктам и **не применил к подтверждениям**, хотя они устроены так же:

- `C2` — «17 объектов перепроверены независимо, 4 из 4 заявленных SHA-256 совпали»;
- `C3` — «36 ссылок с #fragment, 36/36 …; 2 мёртвых якоря найдено, 1 исправлен»;
- `C4` — «8 из 24 перечитаны у сервера, 8/8 совпали».

Все эти числа печатались в §0 из самого реестра. Сверка показала, что **три из четырёх
заголовков просрочены** — не по факту, а по числам:

| Где | Что было написано | Что в артефакте сейчас |
|---|---|---|
| `C2`, `verification.expect` | `17 локаторов, match=4 …`, тесты «13 OK» | 17 и 4 верны, тестов **18** |
| `C3`, `verification.expect` | `resolves=2 856, external=5 974`, тесты «27 OK» | **2 861** и **5 966**, тестов **30** |
| `C4` | «8 из 24 … 8/8» | переснято в §19: опрошены все, `distinctDriveIds` = 92 |

Факты подтверждений остались верными; устарели **числа, которые их описывали**. Именно это и
происходит с любым счётчиком, у которого нет поля.

### 28.1. Что сделано

- **Заголовки без измерений.** Тест запрещает измерения в `title` подтверждений — тем же
  шаблоном, что и для открытых пунктов, с одной поправкой: идентификаторы (`v3`, `SHA-256`, `§19`)
  разрешены, а `17 объектов`, `36/36` и `8 из 24` — нет.
- **Числа читаются из артефактов.** У подтверждений появилось поле `counters`: `label` +
  `artefact` + `field`, и §0 печатает значения, прочитанные из отчётов, а не из памяти реестра.
  `C2` берёт три счётчика из отчёта локаторов, `C3` — три из отчёта ссылок.
- **Неразрешимый счётчик валит проверку.** Нет артефакта, нет поля или поле не число —
  `--check` возвращает 2 и печатает причину. Молчаливый пропуск превратил бы «не смог прочитать»
  в «всё в порядке».
- **`verification.expect` больше не повторяет числа**, а отсылает к counters; тот же тест
  требует, чтобы в них не было измерений. `C4` помечен `supersededBy: §19` — §0 печатает это
  явно, а не оставляет читателю догадываться, почему выборка из восьми стоит рядом с полным
  опросом.

Одна проверка при этом снялась сама: утверждение `drive-sample-in-confirmation` следило за
фразой «объекты Drive: 8 из 24 перечитаны», которая жила **только в заголовке `C4`**. Заголовка
больше нет — следить не за чем, и проверка удалена, а не перенацелена на похожую фразу. Её
соседка `drive-sample-in-section-11` осталась: там фраза на месте и по-прежнему `superseded`.

### 28.2. Что это доказывает про сам регистр

Три просрочки за один день — в разделе, который целиком про просроченные счётчики. Это не
повод переписать регистр заново, а довод в пользу единственного правила, которое здесь
работает: **число живёт там, где его считают, и печатается оттуда**. Всё остальное — копия,
и копия стареет без предупреждения.

Подтверждения от этого не стали закрытиями: ни `C1`, ни `C2`, ни `C3`, ни `C4` не снимают
удержаний. Изменилось то, что их числа теперь либо верны, либо проверка падает.

## 29. Таблицы §15 и §16 были копиями отчётов — и §16 потерял темы коммитов (18.11.2026)

Третий и четвёртый случай одного и того же: §15 (дубли-близнецы) и §16 (самодатировка) держали
таблицы состояний, переписанные из отчётов руками, — 3/1/6/2 и 9/6/2/0. В §16 к таблице
прилагался ещё и список шести документов с датой, последним коммитом и темой.

Копия успела разойтись: в §16 две строки `ИСКУПЛЕНИЕ/fathers/` были сокращены до «то же», а
темы коммитов в остальных четырёх — усечены до короткой формы без префикса. Читатель видел
пересказ улики вместо улики.

### 29.1. Что сделано

- **Оба блока генерируются** (`--write-twins-table`, `--write-stamps-table`) из
  `data/document-twins-2026-11-18.json` и `data/state-stamps-2026-11-18.json`.
- **§15 называет пары поименно.** Раньше в таблице стояло одно пояснение на состояние, и только
  у `near-identical` была названа пара (и её 0.909). Теперь все пары, которые не просто общий
  текст, перечислены с измеренным перекрытием: три дословных, вложенность 0.909, два
  надмножества 0.739 и 0.706. `shared-text` (6 пар) остаётся счётом: перечислять линии версий
  по именам — это уже не карта, а свалка.
- **Сумма пар печатается строкой** в генерируемом блоке и проверяется утверждением на
  `totals.pairs` — иначе после удаления ручной фразы с итогом число осталось бы вовсе без дома.
- **§16 печатает темы коммитов дословно** и повторяет строку `ИСКУПЛЕНИЕ/fathers/` для каждого
  файла: сокращение «то же» было решением переписчика, а не отчёта.

### 29.2. Что это меняет по существу

Ничего в вердиктах: дублей по-прежнему 12, дословных — три, и одна из них (`13`↔`24`) остаётся
**открытым пунктом для владельца индекса** (§15), потому что правка мастер-карты — решение
человека, а не инструмента. Дат, отставших от текста, по-прежнему шесть, и даты инструмент
не переписывает.

Изменилось другое: четыре раздела регистра из шести, где числа дублировали отчёт, теперь
печатаются из него (§8, §9, §11, §15, §16 — пять). Осталось проверить, сколько таких копий
ещё не найдено; это следующий честный вопрос, а не победа.

## 30. §3 отставал на семь закрытий: третья копия, которую никто не перегенерировал (18.11.2026)

В §29 я написал, что дальше честный вопрос — сколько копий ещё не найдено. Ответ пришёл сразу,
и он крупнее предыдущих: §3 «Что закрыто 18.11.2026 (и чем именно)» держал таблицу на
**18 строк**, тогда как в реестре закрытий было **25**. Семь последних закрытий в тексте
отсутствовали — не потому, что их забыли описать (описаны они в §20–§29), а потому, что
таблица §3 обновлялась руками и перестала.

Это третья копия одного и того же перечня: §0 (генерируется), реестр закрытий (источник) и §3
(руками). Первые две согласованы проверкой; третья не проверялась ничем и разошлась на семь
строк — то есть на всё, что случилось после того, как её в последний раз трогали.

### 30.1. Что сделано

- **§3 генерируется из реестра** (`render_detail` в `render_closures_summary.py`, маркеры
  `closures-detail`): `closedScope` → «что закрыто», `method` → «метод», `recordLocations` →
  ссылки. Теперь таблица не может быть короче реестра: она из него и состоит.
- **`--write` и `--check` отвечают за оба блока**; отсутствие любого из маркеров — падение, а
  не молчание.
- **Красная строка в этом же инструменте.** Первая версия `replace_block` читала маркеры из
  глобальных переменных, поэтому второй вызов записал блок §3 **поверх** блока §0. Это
  обнаружилось сразу (`--check` сказал «stale»), но важно, как: инструмент, который ловит
  подмену блока в документе, поймал собственную подмену блока. Маркеры теперь параметры, и
  срез собирается по найденному индексу, а не по строке маркера — вторая ошибка того же
  вызова съедала перевод строки.

### 30.2. Что это не решает

Тексты `closedScope` в реестре сами содержат измерения — «2 407 файлов, 8 712 ссылок» у
закрытия 07, «541 склейка в 19 файлах» у закрытия 08. Это **записи о том, что было измерено
тогда**, и в этом качестве они верны; текущие числа живут в §8 и §12 и проверяются там. Но
различить «историческое число» и «число, которое обязано совпадать с артефактом» пока может
только читатель, а не проверка. Это следующий открытый вопрос, и он честнее прежнего: не
«сколько копий», а «какие числа обязаны быть живыми».

## 31. Какие числа обязаны быть живыми (18.11.2026)

§30 закончился вопросом: отличить историческое число от того, которое обязано совпадать с
артефактом. Первый замер этого различия нашёлся там же, где и всё остальное: **в записях реестра
о самом реестре**.

Их было пять, и два уже разошлись:

| Где | Что стояло | Что на самом деле |
|---|---|---|
| запись 20, `objects` | `claims: 46` | на момент сверки инструмент печатал **52** |
| запись 21, `objects` | `triggerPaths: 49` | на момент сверки чекер печатал **50** |
| записи 20, 24, 26 | `openItems: 5`, `confirmations: 4`, `closures: 26` | меняются с каждой записью по построению |

Плюс три числа в прозе: «проверяются **38** утверждений: 32 табличных и 6 в прозе» (§21.2),
«Итог: **46** утверждений» (§24), «**6** утверждений в прозе» в записи 17. Все три — счёт
**собственного инструмента**, и все три устарели.

### 31.1. Правило, которое из этого следует

Число, считающее **сам регистр** (сколько закрытий, утверждений, открытых пунктов, триггеров),
нельзя хранить в регистре: к следующему коммиту оно неверно, а печатает его инструмент.
Такие числа **удалены, а не обновлены**, и вместо них стоит отсылка к инструменту.

Два числа в таблице выше — те самые, что я только что объявил недопустимыми, и они стоят здесь
как **запись о находке на 18.11.2026**, а не как живой счёт. Разница тонкая, и я не выдаю её за
проверку: тест ловит конструкцию «N утверждени…» в тексте, но датированную запись о прошлом
отличить от живого счётчика он не может. Поэтому дата стоит рядом с числом явно.

Число, измеряющее **внешний объект** (байты, хеши, число пар в отчёте на дату среза), —
законная запись о моменте: она не обязана быть живой, но обязана быть датированной. Дата среза
в реестре есть, и записи закреплены собственными `snapshotDate`.

### 31.2. Что теперь проверяется

- **В `objects` записей запрещены само-счётчики** (`closures`, `confirmations`, `openItems`,
  `claims`, `triggerPaths`) — тест падает, если такой ключ появится снова;
- **в тексте регистра запрещено число утверждений** — тест ловит конструкцию «N утверждени…» и
  баннер инструмента. Оба теста проверены на текущем файле: до правки они падали;
- **`closedScope` записи 17** больше не называет счёта прозовых утверждений — он тоже был
  само-счётчиком, просто записанным словами.

### 31.3. Граница, которая осталась

Записи о **внешних** объектах по-прежнему содержат числа, снятые при закрытии: «2 407 файлов,
8 712 ссылок» в записи 07, «541 склейка» в записи 08, «17 локаторов» в записи C2. Это не дефект,
пока читатель понимает, что это снимок. Механической разницы между «снимок» и «живое число» в
формате записи пока нет — есть только дата среза у всего файла.

Следующий шаг, если он понадобится, выглядит так: у каждой записи явное поле `measuredAt` и
проверка, что числа, помеченные живыми, совпадают с артефактом. Пока таких чисел в записях нет —
и это лучше, чем формат, который обещает больше, чем проверяет.

## 32. Правило «число тестов — тоже счётчик» было записано и применено к одному предложению (18.11.2026)

В §27.2 есть фраза: «а хвост с числом офлайн-тестов из прозы убран: число тестов — тоже счётчик,
и он уже устарел». Правило верное. Применено оно было к **одному** предложению — тому самому,
из которого число убрали. В том же файле оставалось ещё пять таких цитат, и шестая — в записи
реестра.

### 32.1. Что нашлось

| Где стоит число | Записано | На деле при сверке |
|---|---|---|
| §8, офлайн-прогон замера относительных ссылок | 27 | 30 |
| §10, `ChecksumColumnTests` в замере библиотеки Drive | 6 | 9 |
| §10, «всего по оси» того же замера (с `LedgerTests`) | 13 | 16 |
| §19, офлайн-прогон замера целостности текста | 22 | 22 |
| §20, офлайн-прогон замера дайджестов | 30 | 30 |
| запись 24, `previousState` (пересказ прежней формулировки) | 27 и 13 | 30 и 16 |

Три из шести разошлись за часы. Остальные три верны не потому, что их кто-то поддерживал: они
верны потому, что с момента, когда их набрали, в этих файлах не появлялось нового теста. Разница
между «27» и «30» возникла не из ошибки, а из работы — я добавлял тесты в тот же день, к той же
оси, и не возвращался к цитате.

Отдельно стоит отметить соседство: **запись 24 уже описывала этот самый дрейф** — в ней так и
записано — прежнее число и рядом верное, «27 (их 30)». То есть реестр в одном месте знал
правильное число, а файл в
другом месте продолжал утверждать прежнее, и ничто не замечало противоречия внутри одного
документа.

### 32.2. Что сделано

Числа **удалены, а не обновлены** — по тому же правилу, что и само-счётчики в §31. Если число
нужно, его печатает прогон; документ, который его копирует, ошибается к следующему тесту и при
этом не может сказать, о каком прогоне речь (в файле живут прогоны девяти разных наборов).

Вместо чисел в тексте осталось то, что проверяемо:

- §8 сохранил имя шага — `CI-шаг «Reject unexplained dead locators»`; это утверждение о
  workflow, и оно теперь сверяется с именами шагов в `.github/workflows/*.yml`;
- §10 вместо счёта говорит, какой набор закрывает вопрос, и что число печатает прогон;
- в §19 и §20 названия замеров остались, счёт ушёл.

Гейты (все — тесты, новых проверяющих скриптов нет):

| Проверка | Что запрещает |
|---|---|
| `RegisterSuiteSizeTests.test_prose_does_not_quote_the_suite_size` | конструкцию «число + тест» в тексте регистра |
| `RegisterSuiteSizeTests.test_quoted_ci_step_names_are_step_names` | имя шага CI, которого нет среди имён шагов ни в одном workflow |
| `ClosureTests.test_records_do_not_quote_the_suite_size` | тот же счёт в полях записи: `title`, `closedScope`, `method`, `objects` |
| `CommittedReportTests.test_committed_report_matches_a_fresh_run` | закоммиченный отчёт о ссылках, разошедшийся с текущим деревом |

`previousState` из третьей проверки исключён намеренно: это пересказ прежней формулировки, и
запись 24 приводит «27 (их 30)» как доказательство дрейфа, который она закрывала. Запретить там
числа — значит потребовать, чтобы доказательство не содержало предмета.

Все четыре проверки я прогнал **в обратную сторону**: подложил в копии по одному нарушению
каждого вида. Покраснели все четыре.

### 32.3. Граница, которая осталась

- Проверка ловит **цифры**. «Тесты проверены в обе стороны: на прежней версии кода четыре из них
  падают» (§26) — тот же счёт словами, и он пройдёт мимо. Такой формулировке цена та же; правило
  о ней не знает.
- Имя шага сверяется с **существующим** именем. Переименование шага сделает цитату ложной, и
  проверка это поймает; но проверка не знает, что шаг делает то, что о нём написано.
- Сегодня у второй проверки ровно один предмет — единственная цитата имени шага в файле. Это не
  сила проверки, а состояние текста.

### 32.4. Что это не меняет

Ни одного вердикта. Ни одна зацепка не закрыта: приводы, права, шесть документов, отредактированных
после штампа, неканонические `holds` и независимая научная приёмка остаются как были. Изменилось
одно: число, которое раньше могло тихо устареть в прозе, теперь не может там находиться.

### 32.5. Почему не `measuredAt`

§31.3 назвал следующим шагом поле `measuredAt` у записей. Я его не сделал, и вот причина: в этом
файле все внешние измерения сняты в один день, поэтому поле, добавленное сегодня, дало бы
двадцать одинаковых дат — формально больше информации, фактически ноль. Проверяемое правило,
которое уже было записано и не исполнялось, нашло шесть мест, три из которых успели разойтись за
часы. Это больше, чем дало бы поле, и это было честнее начать с него.

### 32.6. Ошибку поймал CI, а не мой прогон

Первый коммит этой главы (`7ce07407`) упал в CI на шаге «Scan (must not touch the working tree)».
Причина: таблица §3 генерируется из реестра и ставит ссылки, а две новые ссылки записи 28
(`docs/research/HOLDS_REGISTER_2026-11-18.md` и `scripts/test_audit_register_claims.py`) добавили
два разрешаемых локатора. Закоммиченный отчёт о ссылках продолжал говорить 2 885, шаг `cmp`
сравнил свежий прогон с отчётом и покраснел.

Главное здесь не цифра, а то, **где** стояла проверка. Свежесть отчёта сверялась только в
workflow: `cmp /tmp/links-a.json data/relative-links-audit-2026-11-18.json`. Локально ни один тест
этого не делал, поэтому мой полный прогон был зелёным — и я в предыдущем отчёте написал, что гейты
прошли. Прошли не все: один жил в CI и мой прогон его не включал.

Исправление: тот же `cmp` переехал в тест — `CommittedReportTests.test_committed_report_matches_a_fresh_run`
сравнивает закоммиченный отчёт со свежим `scan()` и стоит в общем наборе. Проверка в workflow
осталась: дублирование здесь не вредно, потому что обе стороны читают один артефакт.
Обратная сторона проверена: со старым отчётом тест падает, со свежим проходит.

Вывод, который я записываю, потому что он дороже этой главы: **проверка, живущая только в
workflow, — это проверка, которую автор не запускает.** Пока она там, «все гейты зелёные» в
отчёте значит «все гейты, которые я вспомнил».

## 33. Аудит собственной работы: тринадцать дефектов, шесть из них — в проверках

Владелец корпуса попросил проверить всё, что сделано в этом регистре, прежде чем это мержить.
Проверка шла не «перечитал и вроде нормально», а двумя способами, которые оставляют след.

**Первый — инварианты.** Все гейты заново, все отчёты воспроизведены из дерева, реестр проверен
на форму (уникальность id, отсутствие пропусков, канонические типы, существование каждого
локатора), §3 сверен с реестром построчно, утверждения — с артефактами.

**Второй — мутации.** В код по одной вносились заведомые поломки, и смотрелось, покраснеет ли
набор. Это единственный способ узнать, что тест проверяет, а не просто существует. Внесено
тринадцать поломок; сначала поймано десять. Три непойманных — это дыры в проверках, а не в
работающем коде: они означали, что такой дефект мог бы пройти незамеченным.

Пять дефектов нашлись позже, уже после первого круга, — и все пять не в тексте, а в том, как
он проверяется: пять прозовых счётчиков, которые приходилось перепечатывать после слияния
(§33.5, §33.6); пропущенный отчёт о пинованных локаторах (§33.7); отчёт о дублях, который
сверялся только с самим собой (§33.8); тестовые классы ниже раннего `unittest.main()` (§33.8);
и, наконец, проверка снимка не в дереве ветки, а в синтетическом дереве слияния (§33.9).
Итог — тринадцать.

### 33.1. Исправлено

| Дефект | Что было не так | Чем закрыт |
|---|---|---|
| §3 показывал не все локаторы | в таблице стояли первые два, остальные исчезали молча | §3 печатает все; §0 — первые два и «и ещё N» |
| Флаг, которого нет в политике | `TEXT_INTEGRITY_HOLD` (запись 08) не объявлен ни одним файлом корпуса, но печатался в §0 среди флагов | объявлен в `localAxes` с причиной, §0 помечает его как ось реестра |
| Три метода без русского имени | в русской строке §0 и §3 стояли сырые слаги трёх подтверждений | добавлены имена, тест падает на любом методе без имени |
| Шесть повторяющихся ключей в `METHOD_NAMES` | мусор от правки: один и тот же метод был объявлен дважды | словарь дедуплицирован |
| Обрыв причины открытого пункта | текст резался по 180 знакам без многоточия — короткое не отличить от обрезанного | обрыв помечается «…» |
| Два правила двусмысленности | таблица считала двусмысленностью только разные числа, проза — любое второе вхождение | одно правило: сравниваются значения; тесты в обе стороны |
| Машинный срез §2 цитировал устаревший артефакт | инвентарь не сверялся с деревом: CI гонял инструмент дважды и сравнивал прогоны между собой, а не с закоммиченным файлом; упоминания флагов, появившиеся в скриптах позже, в артефакт не попали | артефакт перегенерирован; теперь его сверяет единый гейт `check_snapshot_freshness.py` |
| Отчёт самодатировки не воспроизводился | инструмент писал в отчёт сегодняшнюю дату, поэтому на следующий день отчёт отличался одной строкой | флаг `--today`; закоммиченный отчёт воспроизводится со своей датой побайтово |
| Отчёт о дублях никем не сверялся с деревом | §15 генерируется из `data/document-twins-2026-11-18.json`, а утверждения сравнивают текст с артефактом: отчёт, описывающий вчерашний корпус, соглашался с таблицей, сгенерированной из него же | единый гейт воспроизводит отчёт; проверено мутацией (`documentsCompared +1` → красный результат) |
| Тестовые классы после `__main__` | проблема была не в одном файле: ранний `unittest.main()` скрывал нижние классы при прямом запуске в семи тестовых модулях | заглушки перенесены в конец; `TestModuleLayoutTests` запрещает раннюю или повторную заглушку |
| Свежесть проверялась в синтетическом merge-дереве | новый файл из `main`, которого ветка не меняла, делал красным PR и заставлял переснимать все отчёты снова | блокирующий гейт запускается в отдельном worktree на PR head; merge-дерево получает интеграционные проверки, а после merge дрейф только печатается |

**Самый дорогой из восьми — первый в этом списке, и он же последний, который я нашёл.**
Машинный срез §2 и таблица по корпусам построены на `data/repository-holds-inventory-v1.json`.
Шаг CI запускал инвентаризацию дважды и сравнивал два прогона — это доказывало
детерминированность, а не актуальность. Артефакт отставал от дерева на несколько упоминаний
флагов, и все утверждения §2 «совпадали» — с устаревшим файлом. Проверка, которая сравнивает
инструмент с самим собой, не видит, что он описывает прошлое дерево.

Про отчёт о самодатировке: его **нельзя было сверить** — его собственное
поле `scope.today` делало его другим назавтра, даже если в дереве не изменился ни один байт. Шаг CI
для него потому и был отчётным, а не гейтовым. Теперь его можно воспроизвести — и тогда гейт
становится возможным; включать его или нет, решает владелец, потому что он покраснеет на любой
правке в любом документе корпуса, а не только в этом.

### 33.2. Что не нашлось

Это тоже результат, и его стоит записать:

- ни одного расхождения в утверждениях — все совпали, кроме одного, перекрытого более поздним
  разделом, — и ни одного в генерируемых таблицах; число утверждений здесь не приводится: оно
  считается инструментом, а не переписывается (§31);
- ни одной пропущенной строки: §3 совпадает с реестром построчно, id идут без пропусков;
- **ни одного удалённого утверждения за всю работу**: таблица утверждений не менялась, а из
  прозовых исчезло одно — то, чьё число убрали из заголовка подтверждения в §28;
- исторические числа, выборочно сверенные по истории Git, верны: «18 строк против 25 записей» в
  §30 и «46 против 52, 49 против 50» в §31 воспроизводятся из коммитов, на которые ссылаются;
- слияние с `main` проходит без конфликтов; разрозненные проверки свежести сведены в один
  блокирующий `check_snapshot_freshness.py`, а не удалены: он проверяет и прежние случаи, и Drive;
- ни одной зависимости от времени или случайности, кроме найденной в самодатировке;
- ни одного артефакта-сироты: у каждого файла в `data/`, добавленного этой работой, есть
  потребитель — инструмент, запись реестра или тест.

### 33.3. Что осталось и почему

- **Утверждения проверяют текст против артефакта, а свежесть — артефакт против дерева ветки.**
  Это две разные проверки. `check_snapshot_freshness.py --check` воспроизводит инвентарь,
  ссылки, дубли, даты и Drive-отчёт, а у пинованных локаторов без сети сверяет места цитирования.
- **Три результата остаются отчётными** (найденные дубли, смысл самодатировки, сверка Drive).
  «Отчётный» значит: результат печатается, но сам по себе не запрещает merge, потому что требует
  человеческого решения. **Свежесть этих отчётов — гейт**, то есть несовпадение с PR head
  блокирует merge. Так ошибка в измерении не смешивается с содержательным вердиктом.
- **Сеть не перечитывается в CI.** Пинованные байты подтверждены датированным сетевым прогоном;
  сейчас автоматически проверяются только состав локаторов и места их цитирования. Снимок Drive
  остаётся ответом Drive на свою дату и не выдаётся за сегодняшний ответ сервиса.
- **`previousState` цитирует исторические числа** и из запрета на числа в записях исключён
  намеренно: запись 24 приводит «27 (их 30)» как доказательство того дрейфа, который закрывала.
- **Проверки ловят цифры, не слова.** «Четыре из них падают» пройдёт мимо запрета.
- **Открытые зацепки не изменились**: независимая научная приёмка, приводы Drive, права, шесть
  документов, изменённых после своего штампа, неканонические `holds`.

### 33.4. Правило, которое я забираю из этой проверки

Аудит, который только перечитывает, находит опечатки. Аудит, который **ломает код и смотрит, кто
закричит**, находит тесты, которые ничего не проверяют. Три дыры из тринадцати — это не мало: если
бы я не внёс поломки, «все гейты зелёные» звучало бы так же уверенно, как звучало до §32.6.

### 33.5. Что показало слияние с `main`

Первый прогон этой главы упал в CI — и не на моей правке, а на **актуальности отчётов**. GitHub
для pull request собирает дерево `main` + ветка; в `main` за это время пришли три коммита с
новыми документами, и три проверки свежести («отчёт описывает это дерево») покраснели. Они были
правы: отчёты описывали дерево до слияния.

Так был устроен первый вариант гейта: **проверка свежести делала красным любой PR, база которого
уехала вперёд**, пока артефакты не пересняты. Ровно та же цена была у шага `cmp` в workflow.
После нескольких бессодержательных пересъёмов владелец выбрал «не гоняться за `main`»; эта
политика заменена в §33.9. Исторический диагноз здесь оставлен, но правило уже не действует.

Пересъём вскрыл ещё одно расхождение, которого никто не видел: **§8, §15 и §16 держали числа в
прозе**, и эти числа уехали вместе с корпусом — ссылок с фрагментом стало больше, документов
стало больше. Пять прозовых утверждений были просрочены, и это поймал тот самый аудит
утверждений, который до сих пор ловил их только при правке реестра. Числа пересняты из отчётов.

И третье: **§23 держал ручную копию таблицы переписи фрагментов** — с другими подписями, поэтому
аудит утверждений её не видел. Она разошлась с отчётом молча. Копия убрана: вместо неё ссылка на
генерируемую таблицу §8 и датированная запись «на 18.11.2026 было 36, из них 18 и 18».

### 33.6. Числа, которые приходилось перепечатывать на каждом слиянии

Пересъём после слияния дважды подряд показал одно и то же: три числа в прозе §15 и §16 —
сколько документов сравнено, сколько Markdown просканировано, сколько документов ставит себе
дату — уезжают при каждом слиянии с `main`, потому что в `main` приходят новые документы. Их
приходилось перепечатывать руками. Это ровно тот дефект, из-за которого §27.2 убрал число из
прозы, а §29 и §30 сделали таблицы генерируемыми: **число, которое надо править после каждого
слияния, — это число без поля.**

Теперь эти три показателя стоят строками в генерируемых таблицах §15 и §16 и проверяются как
обычные табличные утверждения. Из прозы они убраны вместе с тремя прозовыми утверждениями,
которые на них опирались, — иначе утверждение осталось бы без якоря. Одно прозовое утверждение
(«проверено N документов») ушло по той же причине: его число теперь строка «документов со своей
датой».

### 33.7. Красный CI: я ошибался в том, какой шаг падает

Два раза подряд я записывал, что job `inventory` падает на шаге «Test classification and
read-only behaviour», — и оба раза это было неверно. Правильный ответ даёт не лог (его
скачать из песочницы нельзя: журнал отдаётся с `blob.core.windows.net`, а туда выхода нет),
а перечисление шагов job:

```
gh api repos/FedorMilovanov/Research/actions/runs/44839225121/jobs \
  --jq '.jobs[] | select(.conclusion=="failure") | [.steps[] | select(.conclusion=="failure").name]'
→ ["Check the pinned-locator report still describes the tree"]
```

**Десятый дефект, и снова в моей процедуре пересъёма.** Отчёт
`data/pinned-github-locators-verified-2026-11-18.json` тоже описывает дерево и тоже уезжает при
слиянии: в `main` пришёл новый файл ридера Чарнока, в нём оказалась ещё одна цитата того же
пинованного локатора, и отчёт остался с числами «19 цитат в 7 файлах». Мой цикл пересъёма знал
пять артефактов (инвентарь, ссылки, дубли, даты, утверждения) и не знал шестого. Ошибка не в
инструменте — он как раз поймал расхождение, — а в списке того, что я переснимаю после
`merge main`. Список задан не мной, а шагами workflow: каждый шаг `--check-report` — это
артефакт, который обязан пересниматься вместе с остальными.

Пересъём: 19 → 20 цитат, 7 → 8 файлов; подтверждение локаторов не изменилось. Проверка
`--check-report` теперь 0, таблица §11 перегенерирована.

Промежуточное правило было таким: **после `merge main` переснимать всё, что имеет шаг
`--check` в CI, а не то, что я помню.** Оно устранило неполный ручной список, но породило другой
дефект — бесконечное догоняние чужих изменений. Окончательная граница проверки — §33.9.

### 33.8. Два дефекта, которые видны только при попытке их покраснеть

**Отчёт о дублях не был гейтован ничем.** §15 строится из отчёта, утверждения сравнивают текст
с отчётом — и оба согласны, даже если отчёт описывает прошлое дерево. Теперь его воспроизводит
единый гейт. Мутация `documentsCompared +1` краснит результат: проверка смотрит на дерево, а не
на файл, который только что прочитала.

**Ранний `unittest.main()` оказался не единичной ошибкой.** После первого исправленного файла
поиск по всем `scripts/test_*.py` нашёл тот же дефект ещё в шести модулях; в трёх заглушка была
даже записана дважды. `unittest discover` импортировал модули целиком и всё видел, а прямой
`python3 scripts/test_…py` завершался до нижних классов. Все заглушки перенесены в конец;
AST-тест запрещает повторение.

Оба дефекта — про то, что «зелёный набор» и «работающая проверка» не одно и то же.

### 33.9. Граница гейта: свежесть ветки отдельно от догоняния `main`

Три последовательных прогона показали анти-паттерн: GitHub строит `pull_request` как
синтетическое дерево «текущий `main` + ветка», новый документ в `main` меняет глобальные
счётчики, и PR приходится догонять снова, хотя ни отчёт, ни его исходники в ветке не менялись.
В тот момент владелец выбрал это прекратить; последующее прямое указание изменило
операционную политику (§33.10), но не должно снова смешивать два разных вопроса в одном гейте.

Теперь CI намеренно использует **два дерева для двух разных вопросов**:

1. В отдельном worktree на `github.event.pull_request.head.sha` команда
   `python3 -B scripts/check_snapshot_freshness.py --check` блокирует PR, если датированные
   отчёты не воспроизводятся из дерева самой ветки. Там же проверяются карта закрытий и все
   счётчики регистра.
2. В синтетическом merge-дереве идут тесты алгоритмов и интеграционные гейты: необъяснённые
   ссылки, словарь HOLD, триггеры CI, целостность текста, внутренние дайджесты и очередь
   публикации. Глобальные датированные снимки там заново не объявляются «просроченными» только
   потому, что `main` получил чужой файл.
3. На `push` в `main` дрейф снимков всё равно печатается, но не делает уже состоявшееся слияние
   красным. Это наблюдение, а не запоздалый запрет, который можно закрыть только ещё одним PR.

Гейт свежести объединяет инвентарь, ссылки, дубли, самодатировки, датированный Drive-отчёт и
структуру пинованных локаторов. Drive и GitHub в сеть не перечитываются: проверяется локальная
воспроизводимость датированного свидетельства. Содержательные находки в дублях, датах и Drive
остаются отчётными, потому что автоматический код не вправе решать, какой чужой документ
объявлять главным или было ли позднее редактирование существенным.

Цена этой границы названа прямо: проверка PR head отвечает за то, что закоммитила ветка, а
догоняние `main` — отдельное действие по прямой политике владельца. Их разделение не запрещает
держать ветку вровень; оно запрещает выдавать технический сдвиг базы за дефект алгоритма.

### 33.10. Новая команда владельца: не оставлять ветку позади

После зелёного прогона владелец дал новое прямое указание: «ИСПРАВЛЯЙ до конца всё, не отставай».
Оно отменяет операционное решение не догонять `main`. Техническая граница §33.9 остаётся: CI
по-прежнему отличает снимок ветки от синтетического merge-дерева, но перед завершением работы
ветка должна включать актуальный `origin/main`, а все снимки — воспроизводиться уже после этого
слияния.

На момент команды ветка отставала на три коммита. `origin/main` до
`d4d3e43bd1c8459ef37a35c49f691fb63863a1c2` слит без конфликтов. Изменения `main` сдвинули
инвентарь и аудит ссылок: упоминаний `LOCATOR_HOLD` стало на три больше, внешних ссылок — на
пять. Пересъём выполнен до неподвижной точки двумя последовательными прогонами; единый гейт
свежести, таблицы и карта закрытий после пересъёма возвращают 0.

Эта запись не превращает каждый сдвиг `main` в четырнадцатый дефект: дефект был в смешении
деревьев, он исправлен. Здесь зафиксирована новая политика сопровождения — **перед итоговым
ответом снова проверить `origin/main`, при отставании слить его без force-push и переснять все
зависимые артефакты.**

### 33.11. Комментарий владельца о #621: карта вместо слепого merge

Комментарий владельца `#7062248521` назначил #584 интегратором read-only слоя #621, но прямо
запретил целиком сливать 50 путей. Выполнен отдельный документ
[`PR621_SELECTIVE_INTEGRATION_CROSSWALK_2026-11-18.md`](PR621_SELECTIVE_INTEGRATION_CROSSWALK_2026-11-18.md):
в нём все 32 новых и 18 изменённых путей сведены в пакеты, названы зависимости, владелец и
решение `ADMIT/HOLD`; два пересечения с #584 и пять с #585 разобраны по ключам записей, а не
выбором целого файла.

Scratch-дерево на актуальном #584 показало три красных гейта у добавленного слоя и ровно два
текстовых конфликта полного объединения — оба в производных JSON «Искупления». После сохранения
актуальных JSON и штатного пересъёма целевой `scripts/test_atonement_sync.py` проходит, но это не исправляет
устаревший HOLD inventory и расходящиеся пары Drive-зеркал. Поэтому из #621 ничего не перенесено.
Единственный пакет `ADMIT` — два read-only файла STEPBible: закреплённый ZIP перечитан, размер и
SHA-256 совпали, новый прогон построил тот же JSON. `ADMIT` здесь означает «готов к отдельной
приёмке», а не разрешение на публикацию или уже совершённый перенос.

