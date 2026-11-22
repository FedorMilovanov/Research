# #621 → #584: карта выборочной интеграции, без wholesale merge

**Дата проверки:** 2026-11-18  
**Целевое дерево:** `main @ 8d2bc9709531743be905aaabbb70b3ead54dc683` после слияния `#584`
**Источник:** `#621 @ 1bb893a95b499237afe5e086c016e3ef9da64b8d`  
**Редакционный владелец пересечений SUNO:** `#585 @ 35260487d767c38c9709656d343ccf474713128a`  
**Роль документа:** интеграционная карта. Она не создаёт второй HOLD-реестр, не снимает HOLD, не разрешает публикацию и не разрешает целиком сливать #621.

## 1. Короткий вывод

GitHub API для точного head #621 перечисляет 50 путей: 32 новых и 18 изменённых. Все 32 новых пути отсутствуют в целевом дереве. В scratch-дереве «актуальный `main` после #584 + только 32 новых пути» все девять новых Python-скриптов компилируются, но общий раннер проходит лишь четыре гейта из семи. Падают:

1. `render_hold_inventory.py --check`: оба производных файла инвентаря уже не описывают текущее дерево;
2. `check_hold_doc_numbers.py`: 13 из 54 утверждений не воспроизводятся (часть чисел устарела, часть источников существует только вместе с изменёнными файлами #621);
3. `check_drive_mirror_pairs.py --cross`: 12 из 13 пар расходятся с актуальными корпусом или индексом.

Полное scratch-слияние #621 в актуальный `main` после #584 не является даже текстово бесконфликтным: ровно два конфликта — `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` и `ИСКУПЛЕНИЕ/nt/data/nt-corpus-v1.json`. После сохранения актуальных версий этих двух производных JSON и пересъёма командой `atonement_reshoot_state.py --write` проверка `--check` и 230 тестов `test_atonement_sync.py` проходят. Это доказывает способ механического разрешения, но не принимает спорную исходную прозу #621.

**Актуальное решение:** три узких среза приняты отдельными closures: STEPBible subdataset terms (`HCR-2026-11-18-32`), точная official-core квитанция вместе с независимо написанным полным гейтом (`HCR-2026-11-18-33`) и исправленный shallow-clone runbook с fresh-clone fixture (`HCR-2026-11-18-34`). Actions-custody пакет получил окончательный disposition `REJECTED / SUPERSEDED` в `HCR-2026-11-18-36`: ни один из трёх путей не импортирован. Два исходных official-core prose-файла #621 не приняты; шесть прочих пакетов остаются `HOLD`. Wholesale merge #621 по-прежнему запрещён.

## 2. Пакеты 32 новых путей

| Пакет | Путей | Зависимости и проверка на актуальном дереве | Владелец | Решение |
|---|---:|---|---|---|
| STEPBible subdataset terms | 2 | Только stdlib и закреплённый ZIP. `--check` = 0; ZIP заново скачан по pinned commit, размер и SHA-256 совпали; генерация дала JSON, структурно равный закоммиченному | #584, read-only rights evidence | **ADMIT выполнен в HCR-32**; rights/publication HOLD сохранены |
| Actions artifact custody | 3 | Снимок #621 устарел и не подтверждает байтовый readback. Актуальный main уже содержит bounded assessment 38 G3 items, отдельную квитанцию private readback 8/8 и канонический durable manifest; `validate_g3_durable_custody.py` = PASS | G3 custody owner | **REJECTED / SUPERSEDED в HCR-36**; 0 путей импортировано, полный archive остаётся HOLD |
| Corpus/Drive custody и пары зеркал | 8 | Датированный Drive-снимок, текущие corpus/index JSON и изменённые валидаторы #621. `--cross` на актуальном дереве: 12/13 расходятся | custody owner + владельцы корпусов | **HOLD** |
| Official-core reproducibility | 3 | Точная data-квитанция принята; независимо добавлен полный offline/`--archive`/`--fetch` гейт. Все три ZIP повторно скачаны по полным commit SHA, размеры и SHA-256 совпали. Два prose-файла #621 не переносились | #584, read-only evidence | **PARTIAL ADMIT выполнен в HCR-33:** data receipt + новый локальный gate; исходная проза остаётся **HOLD** |
| Rights proposal | 3 | `render_rights_matrix.py --check` проходит, но импортирует не принятый `render_hold_inventory.py`; это предложение, а не authority | #584 | **HOLD** до отделения от непринятого inventory-слоя |
| HOLD inventory / triage / orchestration | 9 | Производные снимки и документы уже stale; общий раннер падает на inventory, numbers и mirror cross | #584 | **HOLD** |
| Russian Baptists Drive custody note | 1 | Зависит от четырёх изменённых RBA-файлов и датированных Drive identifiers/readback | RBA custody owner | **HOLD** |
| SUNO DBNL slug map | 1 | Сам по себе не обновляет реестр; требуются пять пересекающихся путей, принадлежащих #585, и разрешение по record IDs | #585 | **HOLD** |
| Shallow-clone recovery note | 1 | Ошибочная связка заменена явным `refs/heads/$branch:refs/remotes/origin/$branch`; добавлены безопасные backup/precondition границы. Offline fixture воспроизводит fresh depth-1 single-branch clone и сохранение локальной правки после `reset --mixed` | #584 tooling | **ADMIT выполнен в HCR-34** |
| Pusey II locator note | 1 | Независимая перепроверка подтвердила OCR, но нашла неверную пару p.295 ↔ leaf 306, пропущенный аппарат и границу фрагмента; визуальный C-25 остаётся OPEN | atonement source owner | **HOLD** |

### 2.1. Принятые узкие срезы

```text
scripts/stepbible_subdataset_terms.py
  git blob ba56572a98a3f96b159392b5c91ff492dff26617
data/stepbible-subdataset-terms-2026-11-18.json
  git blob 038b2cca840d71fc525c9414550611c50658364a
```

Проверенный вход:

```text
repository  STEPBible/STEPBible-Data
commit      b86d26cdb1f51729e73b5b4eb7f7ccadc5dfba39
bytes       100920275
sha256      6845fa9660c62301a0eec38c009ca34ef82647a9737529d8c56ac45d35182df0
```

Проверка:

```bash
curl -L --fail -o /tmp/stepbible.zip \
  https://codeload.github.com/STEPBible/STEPBible-Data/zip/b86d26cdb1f51729e73b5b4eb7f7ccadc5dfba39
python3 -B scripts/stepbible_subdataset_terms.py --zip /tmp/stepbible.zip > /tmp/built.json
python3 -B scripts/stepbible_subdataset_terms.py --check
```

`/tmp/built.json` после JSON-разбора равен source JSON. Скрипт ничего не меняет в HOLD/rights state и прямо ограничивает вывод: лицензия в имени файла — утверждение распространителя, а не разрешение на публикацию.

Official-core срез закрыт отдельно как HCR-33. Из #621 принят только точный data blob; checker и негативные тесты написаны независимо в текущей ветке:

```text
data/official-core-datasets-reproducibility-2026-11-18.json
  source git blob 2c1bdecf91f6c05f5cf7ec3187eb86e19bbc905c
scripts/check_official_core_reproducibility.py
scripts/test_check_official_core_reproducibility.py
```

Проверка `--fetch` повторно получила все три ZIP и сверила суммарно `123205547` байт; offline-check и девять негативных тестов включены в CI. Это закрывает только зависимость от истекающего Actions artifact. Независимая Drive-custody, чтение содержимого, научная приёмка, права, публикация и `PROMOTE=0` не изменены.

Shallow-clone note принят после исправления, а не как исходный blob. Канонический документ называет source blob, использует явный refspec и не объявляет runbook authority над корпусом:

```text
docs/research/arena/SANDBOX_SHALLOW_CLONE_RECOVERY_2026-11-18.md
  source git blob aaef9274f73c258d22bad189d23eacc0b460b411
scripts/test_sandbox_shallow_clone_recovery.py
```

Fresh local fixture не использует сеть и не меняет рабочий repository; он проверяется в holds CI. Закрыта ошибка инструкции, а не какой-либо corpus/evidence/rights HOLD.

### 2.2. Точные пути остальных пакетов

**Actions artifact custody (3):**

- `scripts/audit_artifact_custody.py`
- `data/artifact-custody-snapshot-2026-11-18.json`
- `docs/research/holds/ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md`

**Окончательный disposition (HCR-36): `REJECTED / SUPERSEDED`; `sourcePathsImported=0`.** Быстро меняющиеся totals и expiry старого snapshot не принимаются как current authority и параллельный SSOT не создаётся. Актуальная замена в main разделяет exact bounded cohort: `G3_HISTORY/G3_ACTIONS_2026-11-24_EXPIRY_COHORT_ASSESSMENT_2026-11-21.md` отмечает 8 сохранённых объектов и 30 объектов, не сохранённых этой квитанцией. Только 8 перечисленных original ZIP (`2 807 235` bytes) покрыты canonical source manifest, private Drive raw-readback receipt и `DURABLE_CUSTODY_MANIFEST.json`; `G3_ACTIONS_PRESERVATION_CUSTODY_RECEIPT_2026-11-21.json` имеет статус `ACQUIRED_DURABLE_8_OF_8_PRIVATE_DRIVE_READBACK_VERIFIED`.

`validate_g3_durable_custody.py` офлайн проверяет exact IDs, source/destination bytes и SHA-256, original-ZIP/no-repack boundary, canonical links и обязательные `PUBLICATION_HOLD`, `RIGHTS_HOLD`, `EVIDENCE_HOLD`. Это не свежий сетевой readback и не доказательство для остальных 30 объектов, полного Actions archive, title, rights или publication authority; `PROMOTE=0` не меняется.

**Corpus/Drive custody и пары зеркал (8):**

- `data/corpus-custody-receipts-2026-11-18.json`
- `docs/research/data/drive-mirror-pairs.json`
- `docs/research/holds/CORPUS_CUSTODY_RECEIPTS_2026-11-18.md`
- `docs/research/holds/DRIVE_SHA256_READBACK_CROSSCHECK_2026-11-18.md`
- `scripts/check_drive_mirror_pairs.py`
- `ИСКУПЛЕНИЕ/evidence/DOC_MIRRORS_EXPORT_TAILS_2026-11-18.md`
- `ИСКУПЛЕНИЕ/evidence/DRIVE_INDEX_BYTES_FIELD_2026-11-18.md`
- `ИСКУПЛЕНИЕ/evidence/RIGHTS_MIRROR_07_STOP_POINT_2026-11-18.md`

**Official-core source paths (1 data receipt принят в HCR-33; 2 prose-файла остаются HOLD):**

- `data/official-core-datasets-reproducibility-2026-11-18.json` — принят точный blob;
- `docs/research/holds/OFFICIAL_CORE_DATASETS_REPRODUCIBILITY_2026-11-18.md` — не переносился;
- `docs/research/holds/OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md` — не переносился.

**Rights proposal (3):**

- `data/rights-determination-matrix-2026-11-18.json`
- `docs/research/holds/RIGHTS_DETERMINATION_MATRIX_2026-11-18.md`
- `scripts/render_rights_matrix.py`

**HOLD inventory / triage / orchestration (9):**

- `docs/research/holds/HOLD_INVENTORY.json`
- `docs/research/holds/HOLD_INVENTORY.md`
- `docs/research/holds/README.md`
- `docs/research/holds/UNDER_ACQUIRED_WITHOUT_HOLD_TRIAGE_2026-11-18.md`
- `scripts/audit_hold_coverage_gaps.py`
- `scripts/audit_prose_holds.py`
- `scripts/check_hold_doc_numbers.py`
- `scripts/render_hold_inventory.py`
- `scripts/run_research_gates.py`

**Оставшиеся одиночные пакеты (по одному):**

- RBA: `RUSSIAN_BAPTISTS_ARCHIVE/DRIVE_CUSTODY_VS_LEDGER_2026-11-18.md`
- SUNO: `SUNO_HYMNS/data/dbnl-slug-map-1676.json`
- Pusey: `ИСКУПЛЕНИЕ/evidence/PUSEY_II_294_296_OCR_LOCATOR_2026-11-18.md`

## 3. Все 18 изменённых путей: владелец и disposition

| Путь | Семантическая дельта #621 | Текущий владелец / способ сведения | Решение |
|---|---|---|---|
| `00_RUSSIAN_BAPTISTS_ARCHIVE.md` | ссылка на новую custody note | RBA owner; только после принятия самого evidence-пакета | HOLD |
| `1_PETER_BOT/data/source-ledger-v1.json` | четыре замены в датированном ledger | 1_PETER_BOT owner; по record ID, не whole file | HOLD |
| `README.md` | ссылки/числа нового HOLD-кластера | root owner; производные числа уже stale | HOLD |
| `RUSSIAN_BAPTISTS_ARCHIVE/DRIVE_SNAPSHOT_MANIFEST_2026-07-31.md` | custody/readback дополнение | RBA custody owner | HOLD |
| `RUSSIAN_BAPTISTS_ARCHIVE/NEXT_ACTIONS.md` | новые действия по custody | RBA owner | HOLD |
| `RUSSIAN_BAPTISTS_ARCHIVE/README.md` | ссылка на новый документ | RBA owner | HOLD |
| `SUNO_HYMNS/RESEARCH/CLAIM_LEDGER.md` | секция `CLM-DBNL-SLUG-TRAP` | #585; merge секции по claim ID | HOLD |
| `SUNO_HYMNS/RESEARCH/OPEN_HOLDS.md` | только новый generated snapshot/date | #585; не переносить, пересобрать renderer после решения | HOLD |
| `SUNO_HYMNS/RESEARCH/SOURCE_REGISTER.md` | секция `SRC-L-1676` | #585; зеркало сводить после JSON record | HOLD |
| `SUNO_HYMNS/data/source-registry-v1.json` | `sources[id=SRC-L-1676].limits` | #585; добавить только один limits-item после source review | HOLD |
| `SUNO_HYMNS/scripts/render_hold_ledger.py` | изменение renderer | SUNO owner; отдельный code review, не часть data merge | HOLD |
| `scripts/run_atonement_mutation_battery.py` | новые mutation cases | atonement gate owner; актуальная main-версия новее | HOLD |
| `scripts/validate_atonement_corpus_integrity.py` | новые custody/corpus проверки | atonement gate owner; нужен scoped перенос с тестами | HOLD |
| `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` | производные totals для нового NT-раздела | main/#584; значения не переносить, переснять генератором | HOLD |
| `ИСКУПЛЕНИЕ/data/atonement-library-index.json` | Drive mirror/index measurements | atonement owner; файл пересобирается round-close tooling | HOLD |
| `ИСКУПЛЕНИЕ/evidence/AGENT7_DRIVE_LIBRARY_RIGHTS_LOCATORS_AND_ACQUISITION_AUDIT_2026-11-16.md` | новая custody-проза | atonement custody owner | HOLD |
| `ИСКУПЛЕНИЕ/nt/15_JOHN_11_52_SCATTERED_CHILDREN_EXEGESIS_2026-10-23.md` | новый §11 про Pusey/archive.org | atonement source owner; зависит от исправления Pusey review | HOLD |
| `ИСКУПЛЕНИЕ/nt/data/nt-corpus-v1.json` | производный `claimRegister20261026`, новая строка `11@…` | main/#584; переснять после принятия первичной прозы | HOLD |

## 4. Разрешение двух пересечений #584 × #621 по полям

### 4.1. `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json`

#621 меняет только производный блок `integrityGate.scopeOfMeasurementRules.claimsPerRegistry`: счёт NT, общие totals, классы и timestamp. Это следствие нового §11 в NT-прозе, не самостоятельное evidence. Текущая ветка одновременно имеет более поздние изменения других ланов, поэтому ни `ours`, ни `theirs` целиком не является разрешением.

**Правило сведения:** сначала принять или отклонить исправленную первичную NT-прозу; затем выполнить `python3 -B scripts/atonement_reshoot_state.py --write` на combined tree и проверить `--check`. Ручные числа из #621 не переносить.

### 4.2. `ИСКУПЛЕНИЕ/nt/data/nt-corpus-v1.json`

#621 добавляет в `claimRegister20261026` производную строку `11@15_JOHN_11_52_SCATTERED_CHILDREN_EXEGESIS_2026-10-23`, три новых токена и пересчитанные totals. В source review остаются замечания к связанному Pusey-пакету, поэтому generated row нельзя принять раньше текста.

**Правило сведения:** после source-owner review переснять `claimRegister20261026`; не копировать объект и counters вручную. Scratch-проверка этого способа: два конфликтных JSON оставлены из актуального #584, затем `atonement_reshoot_state.py --write`, `--check` и `scripts/test_atonement_sync.py` — 230 тестов OK.

## 5. Разрешение пяти пересечений #585 × #621

| Путь | Ключ сведения | Решение |
|---|---|---|
| `SUNO_HYMNS/data/source-registry-v1.json` | `sources[id=SRC-L-1676].limits` | #585 сохраняется целиком; отдельно рассмотреть добавление одного limits-item #621 |
| `SUNO_HYMNS/RESEARCH/SOURCE_REGISTER.md` | секция `SRC-L-1676` | обновлять после JSON; не выбирать whole-file #621 |
| `SUNO_HYMNS/RESEARCH/CLAIM_LEDGER.md` | `CLM-DBNL-SLUG-TRAP` | перенести только список Source IDs и две оговорки после проверки DBNL map |
| `SUNO_HYMNS/RESEARCH/OPEN_HOLDS.md` | generated output | не переносить; пересобрать из принятого #585 registry |
| `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` | `claimsPerRegistry` | не переносить из обеих веток; переснять после окончательного текстового дерева |

#585 содержит больше поздних source/claim records, поэтому wholesale-версия #621 потеряла бы редакционную работу. В обратную сторону wholesale-версия #585 потеряла бы узкую DBNL находку. Единственная безопасная операция — field/section merge после проверки `dbnl-slug-map-1676.json` владельцем #585.

## 6. Scratch-протокол и воспроизводимость

```bash
# source refs
git fetch origin refs/pull/621/head:refs/remotes/origin/pr-621
git fetch origin refs/pull/585/head:refs/remotes/origin/pr-585

# added-only combined tree
git worktree add --detach /tmp/pr621-combined 8d2bc9709531743be905aaabbb70b3ead54dc683
cd /tmp/pr621-combined
base=$(git merge-base HEAD refs/remotes/origin/pr-621)
git diff --name-only --diff-filter=A -z "$base" refs/remotes/origin/pr-621 \
  | xargs -0 git checkout refs/remotes/origin/pr-621 --
python3 -B scripts/run_research_gates.py --verbose

# full scratch merge: не коммитить и не переносить как merge
git worktree add --detach /tmp/pr621-full-combined 8d2bc9709531743be905aaabbb70b3ead54dc683
git -C /tmp/pr621-full-combined merge --no-commit --no-ff refs/remotes/origin/pr-621
```

Фактический full scratch merge остановился ровно на двух JSON из §4. После разрешения их через актуальное дерево и пересъём:

```bash
python3 -B scripts/atonement_reshoot_state.py --write
python3 -B scripts/atonement_reshoot_state.py --check
python3 -B scripts/test_atonement_sync.py -q
# Ran 230 tests ... OK
```

Оставшиеся три красных research gate — не конфликты Git и не основание ослаблять тесты. Они доказывают, что HOLD inventory, numbers и mirror-pairs нельзя переносить как законченный слой.

## 7. Что остаётся непроверенным

- Текущие байты private/expiring Actions artifacts не скачивались и не выдаются за сохранённые.
- Drive snapshot #621 не перечитывался как сегодняшний ответ Drive; наличие ID не равно destination readback.
- Pusey II page images не открывались визуально; OCR и page-number index не закрывают C-25.
- DBNL slug map не принят редакционным владельцем #585.
- HCR-32, HCR-33 и HCR-34 уже выполняют три выборочных переноса. Первые два не являются решением о правах, независимой custody, научной приёмке или публикации; HCR-34 закрывает только дефект tooling-документа.
