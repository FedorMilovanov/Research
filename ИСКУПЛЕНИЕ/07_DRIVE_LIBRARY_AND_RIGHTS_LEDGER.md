# Искупление — Google Drive library и права

**Дата:** 2026-10-07  
**Родитель:** [07 — СЕРИЯ «ИСКУПЛЕНИЕ»](https://drive.google.com/drive/folders/1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV) (`1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV`)  
**Политика:** [`data/artifact-custody-policy-v2.json`](../data/artifact-custody-policy-v2.json)  
**Правило:** Drive presence ≠ quote-safe ≠ publication approval ≠ снятие HOLD.

## 1. Дерево

| Папка | ID | Ссылка |
|---|---|---|
| 00 — INDEX, AUTHORITY & SERIES MAP | `1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL` | [открыть](https://drive.google.com/drive/folders/1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL) |
| 01 — PUBLIC DOMAIN LIBRARY | `1BuYqlnPM1pIw-pCIFZLOKgGLL3hR1F4t` | [открыть](https://drive.google.com/drive/folders/1BuYqlnPM1pIw-pCIFZLOKgGLL3hR1F4t) |
| 02 — COPYRIGHT BIBLIOGRAPHY & ACQUISITION | `1FdQlbxhVzhAdCPoS1lt2qEZMRPsaQNPI` | [открыть](https://drive.google.com/drive/folders/1FdQlbxhVzhAdCPoS1lt2qEZMRPsaQNPI) |
| 03 — SCRIPTURE, LEXICA & COMMENTARIES | `17BZ9SUu5zp5VVFd5a0t8mFX8wEodHcIv` | [открыть](https://drive.google.com/drive/folders/17BZ9SUu5zp5VVFd5a0t8mFX8wEodHcIv) |
| 04 — CONFESSIONS & HISTORICAL THEOLOGY | `1ZTD2idu9oFO9Et1MSgfgtKMZZg63yUTw` | [открыть](https://drive.google.com/drive/folders/1ZTD2idu9oFO9Et1MSgfgtKMZZg63yUTw) |
| 05 — SOURCE LEDGERS & CLAIM MAPS | `13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ` | [открыть](https://drive.google.com/drive/folders/13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ) |
| 06 — RIGHTS, HOLD & PROVENANCE | `1edsBGRg0oQw_G-75QYdaNvde7KKiCFQy` | [открыть](https://drive.google.com/drive/folders/1edsBGRg0oQw_G-75QYdaNvde7KKiCFQy) |
| 08 — PARALLEL AGENT BRIEFS | `1LkzUHWOLH1M04si64c5iQCNmHpqOBU4n` | [открыть](https://drive.google.com/drive/folders/1LkzUHWOLH1M04si64c5iQCNmHpqOBU4n) |
| 09 — SYNTHESIS (agent 4) | `18U6dslSsNJ20CwlAHTYRrO318mGohtI2` | [открыть](https://drive.google.com/drive/folders/18U6dslSsNJ20CwlAHTYRrO318mGohtI2) |
| 99 — HOLD — SUPERSEDED MIRRORS | `1FK7_q8431ys6MAv_0zFsXfht1Dnl5wmd` | [открыть](https://drive.google.com/drive/folders/1FK7_q8431ys6MAv_0zFsXfht1Dnl5wmd) |

Родитель висит в Research backend: `03 — Research — ИССЛЕДОВАТЕЛЬСКИЙ БЭКЕНД` (`1Eb8qglwGIqeJY-02J8eXNpDaQfdkmozs`). Копии PD-книг **не удаляют** оригиналы из общей PDF-библиотеки.

## 2. Уже положенные объекты (копии существующих PD)

| Объект | Drive ID | Источник копии | Rights | locatorState | publicationState |
|---|---|---|---|---|---|
| Owen, *Works* | `1gfKY8eXGhV-HL5O4u1tVVcCRYNKx-dQY` | `1e1rTdQH8bBrDh8NeEufhtVcBhbzWqyFK` | PD | unchecked | HOLD |
| Calvin, *Institutes* | `1DLcwFWyRXtTDBzdS_tHptGkoItoumVWZ` | `1Pj5iUMrf8OlRuTowMVt7tRoHejpHY1_6` | PD | unchecked | HOLD |
| Goodwin, *Works* | `1o9T7mIQxIH3ZB2EVc2hQsKdjEQM3SW-M` | `1q_D74eAj1x1J_rgE9qL1Y_N3kRPpMrSL` | PD | unchecked | HOLD |
| Westminster Confession | `1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4` | `1zbqz-EaFN5Fwnqo3a8ynVG4B1MpqVVVX` | PD | **unchecked / скан без текстового слоя** (см. §2.1) | HOLD |

Это `ACQUIRED_DURABLE` относительно байтов копии только после независимого SHA-readback. На старте фиксируем: **копия создана через Drive copy_file; SHA-256 readback не выполнялся.** Custody ближе к `TRANSFER_PENDING_VERIFICATION` по строгой политике. Не заявлять forensic acquisition.

### 2.1 Проверка извлечения текста (2026-10-07)

| Объект | Байты | Порог | Результат `read_file_text` | Вывод |
|---|---|---|---|---|
| Westminster Confession | **16 179 601** | ниже cap 25 MB — cap не помеха | `extraction_status: empty`: текстового слоя нет, OCR в коннекторе недоступен | страница WCF 8 в **этом** файле извлечением не проверяема. **Не ретраить, не угадывать** |
| Calvin, *Institutes* | 45 351 929 | выше cap | отказ по cap (`15` §A.1) | то же |
| Owen, *Works* | 42 084 171 | выше cap | отказ по cap (`14`) | то же |

Чем закрыт текст вместо страницы: WCF 8 = Schaff/CCEL `creeds3.txt` **chunks 182–183** (глава VIII, EN+LA) — [`15` §D](15_CALVIN_III24_AND_DORT_II_LOCATORS.md). Оси «печатная страница тома Шаффа» и «страница нашего Drive PDF» остаются `unchecked`.

По Dort Head II английская ось закрыта **не извлечением из Drive PDF, а транскрипцией PD-скана** Scott 1841 (`articlesofsynodo1841syno`, archive.org): Artt. I–IX с. 282–286 и Rejectio I–VII с. 287–292 перенесены в [`15` §B.5](15_CALVIN_III24_AND_DORT_II_LOCATORS.md) вручную, с сохранением OCR-артефактов.

**Вторая волна 2026-10-07 (сличение и перенос):** текст §B.5 сличён со второй OCR-выдачей того же скана (`…_djvu.xml`, чанки 43–45), с латынью (Schaff/CCEL `creeds3.txt` чанк 165) и со вторым английским переводом — 1840 г. (`16`, перенесён в Git из W0-пака на Drive `01`). `accessState = transcribed-from-OCR + collated`; расхождения, прочтения артефактов и найденное сокращение Rejectio IV — [`15` §B.6](15_CALVIN_III24_AND_DORT_II_LOCATORS.md). Сличение с изображениями страниц из этой среды невозможно — открытый локатор, а не снятое ограничение.

Мюррей RAA (in copyright) остаётся вне этой схемы: английских страниц в руках нет, есть только **вторичная** постраничная привязка (I.4 = с. 57–74 по Eerdmans 1955/2015) — [`08` §7](08_MURRAY_RAA_SOURCE_CARD.md). Полные PDF книги со сторонних сайтов сознательно не открывались.

## 3. Мюррей — владельческий RU HTML (не английский PDF)

Владелец загрузил `s3516.htm.zip`. Это полный русский HTML 1955, не Banner PDF.

| Объект | ID | Права | Замечание |
|---|---|---|---|
| ZIP (переименован, папка 02) | `174vd9LfrbuLiamdRHlK9nBasgqAMn7dl` | copyright / PRIVATE_STUDY | SHA-256 `e2adc9d8…` |
| UTF-8 HTML копия | `1SKSoLDuwzSpn8GmPCAseu3swJqSGmxvC` | то же | для чтения |

Тело полное. В Git не кладётся. Цитаты на сайт — нет.

Остальные авторские XX–XXI вв. по-прежнему без полного файла: Packer 1959 intro; Gibson & Gibson 2013; Morris; Stott; Letham; Macleod; Berkhof ST; Bavinck English; Grudem; Frame. Агент не добывает пиратские PDF.

## 4. Как класть новые книги

1. Проверить PD / rights.
2. PD → `01` или `04`, provenance card в `06`.
3. Copyright → только карточка в `02`, либо легальный экземпляр владельца.
4. Не двигать чужие оригиналы; только copy.
5. После copy — записать ID в этот ledger, не плодить мелкие отчёты.

## 5. Загруженные Google Docs (навигация, не первоисточники)

### 5.0 Актуальные зеркала — проверено 2026-10-09

Таблица ниже собрана запросом к Drive и сверена с `driveMirrors` реестра. **SSOT по ID — `driveMirrors` в [`data/atonement-corpus-v1.json`](data/atonement-corpus-v1.json)**; эта таблица — для человека.

| Объект | ID | Папка |
|---|---|---|
| 00 — AUTHORITY — MIRROR (актуальное) | `driveMirrors.file00` | 00 |
| 00 — README AND NAVIGATION — ИСКУПЛЕНИЕ | `1V6j8nzmOr4zJ44kTka9ZSsiX5YYh3ip84nwOKKrJlOs` | 00 |
| 01 — MASTER RESEARCH MAP AND SERIES ARCHITECTURE | `1_0I6d9OiRapJWQ9RzsgIAu73dxeArTJSI7ViRBMPlNw` | 00 |
| 02 — TERMS, DEFINITIONS AND WHAT IS ATONEMENT | `14EwvFHHCY3OlaMJ_tKQH7mGbr3Z3Fc5CqBNGrQNZO7A` | 00 |
| 06 — PUBLICATION ARCHITECTURE FOR GOSPOD-BOG — DO NOT IMPLEMENT YET | `1mxYsP0RPDM8yNq_XCEJQXpDit96QP2z2KKww7psPcKs` | 00 |
| 03 — BIBLICAL CORPUS AND REDEMPTION VOCAB — MIRROR | `1Bu5d-44UP1XEz7gvcXuazUjfP4HyDJtOCA39iQmg64w` | 03 |
| 04 — LIMITED VS UNIVERSAL QUESTION MAP — NO VERDICT — MIRROR | `1GFVUswVklNLz5VCtZRclMFj9b06nA4WUj1pjbIrtNaA` | 05 |
| 05 — SOURCE REGISTRY AND ACQUISITION QUEUE — MIRROR | `15i2GEHWfM-zxqFmDNyiQaSEGMBWd10hPxg4IdJEMOEg` | 05 |
| 12 — HARD TEXTS EXTENT CARDS — MIRROR (актуальное) | `driveMirrors.file12` | 05 |
| atonement-corpus-v1.json — SSOT (актуальный) | свой ID не хранит (самоссылка) — последний объект в папке `05` | 05 |
| 07 — RIGHTS LEDGER — MIRROR (актуальное, этот файл) | не фиксируется здесь — см. `driveMirrors.file07` в реестре | 06 |
| 10 — PRIMARY TEXT — DORT HEAD II AND CALVIN — MIRROR | `1hPs1aEWtwv1GHGHtZVtpWd8c91bQgAgo` | 01 |
| 14 — OWEN BOOK IV LOCATORS — MIRROR (актуальное) | `driveMirrors.file14` | 01 |
| Owen, *Works* (PD PDF) | `1gfKY8eXGhV-HL5O4u1tVVcCRYNKx-dQY` | 01 |
| Calvin, *Institutes* (PD PDF) | `1DLcwFWyRXtTDBzdS_tHptGkoItoumVWZ` | 01 |
| Goodwin, *Works* (PD PDF) | `1o9T7mIQxIH3ZB2EVc2hQsKdjEQM3SW-M` | 01 |
| 13 — DORT II, CALVIN, OWEN EXTENT — MIRROR | `1jMpfpjP-ThrWCXLx13wb-d4aOBH9PH39` | 04 |
| 15 — CALVIN III.24 AND DORT II LOCATORS — MIRROR | `11OYvutqx9z-V5Vcesp3_NUw8Hgccgl47FQ43UkOUMoI` | 04 |
| 16 — DORT HEAD II ENGLISH 1840 — PRIMARY TEXT (независимый свидетель) | `1iBuWNf57KGtSGrUdt1Sou4cmYTY2Aeb0` | 04 |
| Westminster Confession of Faith (PD PDF) | `1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4` | 04 |

**Почему у части строк вместо ID ключ реестра.** Зеркала `.md`-файлов перезаливаются каждый раз, когда меняется Git-канон, — то есть ID у них «летучий». Чтобы таблица не устаревала в тот же день, в ней стоит ключ `driveMirrors.fileNN` из реестра, а не сам ID. Жёстко прописаны только ID PD-книг (они не меняются) и тех доков, которые с 2026-10-09 не перезаливались. **Если файл менялся после 2026-10-09 — берите ID из реестра.**

**Почему у этого файла нет собственного ID в таблице.** Строка о зеркале `07` лежит внутри самого `07`, поэтому любой перезалив делает её устаревшей в момент публикации — самоссылка. ID живого зеркала `07` — только в `driveMirrors.file07` реестра, и это единственный случай такого рода в таблице.

**Таблица ниже — исторический журнал, не навигация.** Часть ID в ней уже **в корзине** (вытеснены волнами 2026-10-07b–e, до изменения правила) и открывать их не надо. Проверка 2026-10-09: в папках `00`/`01`/`03`/`04`/`05`/`06` лежат 20 живых объектов и **46 объектов в корзине** — корзина видна только через фильтр `trashed = true`, в самой папке она не мешает. Ничего из корзины не удалялось: по правилу владельца удаления без прямой команды не делаются.

| Doc | ID |
|---|---|
| README | `1qXjocuWb3xm747BLhtmDBNY4Pd_EhbgZbAlFVgZDqSk` |
| Current authority | `1C0cPyukrgA9xykYXj2D9tLq5zOqm9sU8AOjhMsxK0cw` |
| Master map | `1_0I6d9OiRapJWQ9RzsgIAu73dxeArTJSI7ViRBMPlNw` |
| Terms | `14EwvFHHCY3OlaMJ_tKQH7mGbr3Z3Fc5CqBNGrQNZO7A` |
| Biblical corpus | `1xMwEx6UA2W4N8sE3b9DKRifRnko8T4-RNZfO0_IB-Cs` |
| Question map | `1GFVUswVklNLz5VCtZRclMFj9b06nA4WUj1pjbIrtNaA` |
| Source registry | `1Kd_IB7OVxjaX3zKpFbwDre_XaKA0ACprEHz9Oe77Ksw` |
| Rights ledger (этот файл) | зеркало — Google Doc `07 DRIVE LIBRARY AND RIGHTS LEDGER` в папке `06`; ID — в `driveMirrors.file07` реестра [`data/atonement-corpus-v1.json`](data/atonement-corpus-v1.json) |
| `atonement-corpus-v1.json` (папка `05`) | зеркало реестра; актуальный ID — смотреть в папке `05` (`13cx8Y86…`): каждая перезаливка даёт новый ID, канон — Git-файл |
| Murray card | `1k2iVUPhMXwtV9hrAaZwlOM0YPW-V4JPCf8q4eR43zsA` |
| 11 Murray other works (md, папка 02) | `1YjRSRZtvlYwHME_kUgis5qeSJQ-z5qZd` |
| 12 HARD cards (md, папка 05) | `1PRePtwasQqHSX0C1j5hwD4WM-lG3vflz` |
| 13 Dort/Calvin/Owen (md, папка 04) | `1pKGCNBahIt9ITsHGo5jpeDY2nZQuQWfk` |
| 14 Owen Book IV locators (md, папка 01) | `1cNXU1YIefmgKKU_4uC41dBRP5paP4VVw` |
| 15 Calvin III.24 + Dort II (md, папка 04) | `1qLSeqSU8KE-8NXfO6p3Lwe0Y5vdCib2X` |
| 16 Dort II EN 1840 (md, папка 04) | ID — в `driveMirrors.file16` реестра [`data/atonement-corpus-v1.json`](data/atonement-corpus-v1.json) |
| Брифы параллельных агентов (5 Google Docs, папка `08`) | папка `1LkzUHWOLH1M04si64c5iQCNmHpqOBU4n`; ID отдельных доков при перезаливке меняются — канон в Git: `ИСКУПЛЕНИЕ/agents/` |

Канон остаётся Git-файлами в `ИСКУПЛЕНИЕ/`. Docs — зеркало для чтения на Drive.

**Волна 2026-10-07b:** зеркала `00`, `05`, `07`, `12`, `13`, `15` перезалиты byte-accurate (`upload_file` с `file_path`, без пересказа). Предыдущие ID (`1bI3GKw5…`, `1yRVrEg-…`, `1a1OFbfq…`, `1wz5vC0-…`, `1KGtaHM7…`, `1QCk0y3l…`) отправлены в корзину. Актуальные ID всех зеркал — в `driveMirrors` реестра [`data/atonement-corpus-v1.json`](data/atonement-corpus-v1.json).

**Волна 2026-10-07c:** после переноса английского текста Dort Head II / Rejectio I–VII (Scott 1841) в `15` §B.5 зеркала `00`, `05`, `07`, `13`, `15` перезалиты byte-accurate; реестр `atonement-corpus-v1.json` перезалит в папку `05`. Предыдущие ID (`1FSjtZ2…`, `1M1k9Es…`, `1eEz0Nq…`, `1XdjShz…`, `1aAKDv3…` и промежуточный `1Vys7bm…`) отправлены в корзину. `14`, `11`, `12` не менялись — их ID актуальны.

**Волна 2026-10-07d:** страницы печатных изданий (Шафф vol. III, Оуэн Goold vol. X, Кальвин Beveridge vol. II) + брифы параллельных агентов. Создана папка `08 — PARALLEL AGENT BRIEFS` (`1LkzUHWOLH1M04si64c5iQCNmHpqOBU4n`) с пятью доками (README + 4 брифа). Зеркала `00`, `00_README`, `07`, `14`, `15` перезалиты byte-accurate; реестр перезалит в папку `05`. Предыдущие ID (`1g14vi4…`, `1mLLQ_X…`, `11F4fNT…`, `1cNXU1Y…`, `1yx_gig…` и промежуточный `13t1sEg…`) отправлены в корзину. ID отдельных доков в папке `08` не фиксируются: канон — Git-каталог `ИСКУПЛЕНИЕ/agents/`.

**Волна 2026-10-07e:** страницы абзаца для Оуэна (Goold vol. X, 1850, IA `worksofjohnowe185010owen`), постатейные страницы WCF гл. VIII в Schaff vol. III (1919), отождествление `Rejectio Errorum` с. 577 как Rejectio главы II Дорта, приведение ссылок на Мюррея в `12` к форме из `08` §7. Зеркала `00`, `07`, `12`, `14`, `15` перезалиты byte-accurate; реестр перезалит в папку `05`. Предыдущие ID (`1wVDEcD…`, `1SJ4NR9…`, `1PRePtw…`, `1-B5i3t…`, `1RrX7Wg…` и промежуточный `19FcQjv…`) отправлены в корзину.

После волны HARD (2026-10-07) канон Git: `11_MURRAY_OTHER_WORKS_HARD_TEXTS.md`, `12_HARD_TEXTS_EXTENT_CARDS.md`, `13_DORT_II_CALVIN_OWEN_EXTENT.md`. Зеркала на Drive — в `05` (ledgers), не вместо Git.

**Волна 2026-10-08a — реорганизация Drive без потери ссылок.** Правило волны: **только операции, сохраняющие ID** (перемещение = `add_parents` + `remove_parents`, переименование). Ни одного `delete_file`; ни один файл, на который есть ссылка из репозитория, не перезаливался (перезалив меняет ID и рвёт ссылки других репозиториев).

- Создана папка `99 — HOLD — SUPERSEDED MIRRORS (не удалять: старые копии, ID живы)` — `1FK7_q8431ys6MAv_0zFsXfht1Dnl5wmd` (внутри `07`). **Правило изменено:** вытесненные зеркала теперь не уходят в корзину, а переносятся в `99` — ID остаётся живым.
- В `99` перенесены 11 объектов, которых **нет ни в одной ссылке репозитория** (проверено grep по всем `.md/.json/.py/.yml` и по URL-формам): `1IzZxjB…` (00_CURRENT_AUTHORITY .md), `1ozlnTT…` (00_MASTER_RESEARCH_MAP .md), `10go1Wo…` (01_W0_INTRODUCTION), `1dAMRTc…` (02_W0_SCRIPTURE), `1is-gox…` (03_W0_SOURCE_REGISTRY), `1eZKED3…` (04_W0_COMPETING_MODELS), `1aigyR9…` (05_W0_ACQUISITION), `1_eb42t…` (06_PUBLICATION_ARCHITECTURE .md), `1r4UNql…` (07_W0_DRIVE_MIRROR_RECEIPT), `1tTA18H…` (README.md), `1VVOS5a…` (redemption-corpus-authority json).
- `10 Murray RAA argument map` (`10_c-neE…`) перемещён из `05` (ledgers) в `02` (copyright/acquisition) — к остальным материалам Мюррея.
- Переименованы 5 объектов (ID сохранены): `09 Murray RAA intake and completeness — s3516.htm.zip` → `09_MURRAY_RAA_INTAKE_AND_COMPLETENESS.md`; `10 Murray RAA argument map — PRIVATE STUDY not for publication` → `10_MURRAY_RAA_ARGUMENT_MAP_PRIVATE_STUDY.md`; `08 Murray RAA source card — RIGHTS HOLD — no full text` → `08 MURRAY RAA SOURCE CARD — RIGHTS HOLD, NO FULL TEXT`; `04 LIMITED VS UNIVERSAL QUESTION MAP — no verdict` → `04 LIMITED VS UNIVERSAL QUESTION MAP — NO VERDICT`; `06 PUBLICATION ARCHITECTURE FOR GOSPOD-BOG — do not implement yet` → `06 PUBLICATION ARCHITECTURE FOR GOSPOD-BOG — DO NOT IMPLEMENT YET`. Имена `.md`-зеркал приведены к именам Git-канона.
- Корень «Мой диск»: три исследовательских объекта переехали в хаб `1Eb8qgl…` — Gill PDF `1q4IFET…` → `12k0Om0…` («01 — PDF LIBRARY» корпуса русских баптистов); «1 Peter Bot — Source Materials» `10kZrOw…` → `10WLnp…` («02 — ТРУДНЫЕ ТЕКСТЫ», папка была пуста); «РУССКИЕ БАПТИСТЫ — EMERGENCY HANDOFF» `1G-9jYT…` → `1W8egf…` («99 — EMERGENCY SNAPSHOT»). Личные файлы корня (торты, Маяковский, скриншоты, `1.CSV`, два «Untitled spreadsheet», `00 — GITHUB PROJECTS`) **не тронуты** — ждут решения владельца.

**Волна 2026-10-08b — приём под-корпуса синтеза (агент №4).** Агент синтеза не смог работать в своей песочнице (E2B не инициализировалась ~40 минут, 16+ попыток) и сложил материалы в Drive: `09 — SYNTHESIS (agent 4) — FALLBACK 2026-10-07 (E2B sandbox down)` = `18U6dsl…`. Перенесено в канонический дом Git `ИСКУПЛЕНИЕ/synthesis/` (7 файлов, byte-accurate; у `synthesis-corpus-v1.json` снят BOM, поставленный коннектором):

| Файл Git | Drive ID |
|---|---|
| `synthesis/00_SYNTHESIS_AUTHORITY_2026-10-07.md` | `1AnV1Q137HnN8zNqyn9xJOeo6wzuTe4ws` |
| `synthesis/01_SERIES_PLAN_AND_ARTICLE_COUNT.md` | `11lznQuu7weVv99mt-DW_0o_DEv2FDzo_` |
| `synthesis/02_CONFLICT_LEDGER.md` | `151yu6HTO2j6RSkwNCk5YnbQY2XuO7g8H` |
| `synthesis/03_PRACTICAL_AND_PASTORAL_NOTES.md` | `1YDkHr38ddVGimxxppFQB0Pa7woMGYEFf` |
| `synthesis/drafts/01_what-is-atonement.md` | `1zlK97uW5wEByt_3HUEYBE5NCdLr-wPQ1` |
| `synthesis/data/synthesis-corpus-v1.json` | `1yMiPi3vv-3TjapCeMKNn5JleHgyAv9-_` |
| `synthesis/00_README_FALLBACK_2026-10-07.md` | `1lPGvBuvCEI-D3AYxtsR379BZGO3_I5Ko` |

Папка переименована в `09 — SYNTHESIS (agent 4) — INGESTED INTO GIT 2026-10-08`. Исправленный канон перезалит byte-accurate поверх папки (`upload_file` из рабочей копии Git), прежние файлы агента перенесены в `99 — HOLD` — **ничего не удалено**, старые ID живы.

**Волна 2026-10-08c — зеркала по канону и новая политика вытесненных копий.** Зеркала `00`, `00_README`, `07`, семь файлов под-корпуса `synthesis/` и реестр `atonement-corpus-v1.json` перезалиты byte-accurate из рабочей копии Git (`upload_file` с `file_path`). Прежние ID **не удалены и не отправлены в корзину** — они перенесены в `99 — HOLD` (`1FK7_q…`): ссылка, опубликованная раньше из любого места (включая другие репозитории), продолжает открываться. Папка агента переименована в `09 — SYNTHESIS (agent 4) — INGESTED INTO GIT 2026-10-08`. Актуальные ID — в `driveMirrors` реестра [`data/atonement-corpus-v1.json`](data/atonement-corpus-v1.json); вытесненные — в `driveMirrors.supersededIds2026-10-08` там же.

**2026-10-08d:** после волны локаторов Кальвина (`13`, `15`, `05`, `12`, `00`) зеркала перезалиты по канону; прежние ID — туда же, в `99 — HOLD`.

**Волна 2026-10-08g — отцы у Оуэна + пересчёт страниц WCF VIII.** Два закрытия и одно исправление. (1) *Testimonies of the Ancients* у Оуэна: Амвросий **423**, Августин **424**, Проспер **424** — verbatim на латыни и в переводе Оуэна; колонтитулы раздела подтвердили смещение −16 уже внутри раздела. (2) **Проспер, *Resp. ad Capit. Gall.* cap. 9** — место, которого в каноне не было: «pro totius mundi redemptione crucifixus … propter veram humanae naturae susceptionem … pro his tantum … quibus mors ipsius profuit». (3) **Исправление масштаба**: записанные в волнах 2026-10-07 страницы WCF VIII (633–636) оказались номерами **листов**; печатные — **619–622**, смещение −14. Ошибку выдало то, что в той же строке число 600 было настоящей страницей из оглавления. Зеркала перезалиты по канону; прежние ID — в `99 — HOLD`.

**Волна 2026-10-08f — Оуэн по Тит. 2:11 и 1 Тим. 2:6 (Goold vol. X, 1850).** Четвёртая волна локаторов: `14` §2.4 даёт страницы абзаца для двух локусов, которых в каноне не было, — **Тит. 2:11 — с. 336 и 395** и **1 Тим. 2:6 — с. 307 и 371**. Смещение лист − 16 подтверждено уже не тремя, а десятком колонтитулов подряд (306/314/320/336/350 … = листы 322/330/336/352/366 без разрывов). Карточка **H10** (Тит. 2:11) из состояния «один первоисточник» перешла в состояние «два независимых свидетеля с PD-страницами»: Кальвин CTS 1856 + Оуэн Goold 1850. Зеркала перезалиты по канону; прежние ID — в `99 — HOLD`.

**Волна 2026-10-08e — Кальвин, комментарий на Пастырские послания (CTS 1856).** В канон вошёл второй том CTS-комментариев: IA `commentariesonep00calvuoft`, 1856, `NOT_IN_COPYRIGHT`. Локаторы — 1 Тим. 2:4 (с. 54–55), 2:5 (с. 56), 2:6 (с. 61), Тит. 2:11 (с. 316–318). Затронуло `15` (новый §A.4), `12` (новые чтения H2-e / H2-f и **новая карточка H10 по Тит. 2:11** — раньше локус значился обязательным в `03`, но своей карточки не имел), `03`, `05` (строка `R02b`), `00` и реестр; в слое синтеза — уточнение `C-03` и новый конфликт `C-16` (Кальвин против Кальвина: «сословия» на 2:4 vs «плод жертвы простирается на всех» на 2:5). Зеркала перезалиты по канону; прежние ID — в `99 — HOLD`. Ветка агента `arena/5fe5b33f-research` на GitHub отсутствует (404) — перенос сделан в ветке координатора `arena/dddc1326-research`. Правки при приёмке: снято приписанное Мюррею «закрытие» 2 Кор. 5:14 и Евр. 2:9 (материнский `10` §3 это запрещает), счёт расхождений 12 → 15 по факту реестра, цитата Мф. 11:28 приведена к Синодальному, реплика «нельзя молиться за каждого (1 Ин. 5:16)» атрибутирована как чтение Оуэна. Ни один HOLD не снят; вердикта по объёму нет.

**Волна 2026-10-09a — порядок в именах + обновление отставших зеркал.** Две части, обе без потери ID.

(1) **Переименованы 69 объектов**: 55 в `99 — HOLD` и 14 в рабочих папках `00`/`01`/`03`/`04`/`05`/`06`, по правилу §5.1. Было: 8 файлов `atonement-corpus-v1.json`, 6 — `07 DRIVE LIBRARY AND RIGHTS LEDGER`, 5 — `00 CURRENT AUTHORITY…`, 4 — `12 HARD TEXTS EXTENT CARDS`, 4 — `05 SOURCE REGISTRY…`, 3 — `15 CALVIN…`, 2 — `14 OWEN…`, 2 — `02_CONFLICT_LEDGER.md`, 2 — `synthesis-corpus-v1.json`; остальные имена не повторялись, но не показывали ни состояния, ни того, копией чего файл является. Стало: у каждого объекта в имени есть номер канона, состояние (`MIRROR` / `HOLD` / `PRIMARY TEXT`) и, в `99`, хвост ID. Правилась только запись `name` — **ID всех 69 объектов сохранены**, все ранее опубликованные ссылки продолжают открываться.

(2) **Перезалиты три зеркала, отставшие от Git**: `00`, `12`, `14`. Они изменились в коммитах `52ace08` (свидетельства отцов у Оуэна переведены в `PRECEDENT_OF_READING` + `ORIGINAL_TEXT_HOLD`; страницы Оуэна по Тит. 2:11 и 1 Тим. 2:6) и `7895287` (разделение слоёв), то есть **после** волны 2026-10-08g, которой датировались прежние ID. Новые объекты получили новые ID; прежние `1IeTc1…` (`00`), `1wrBw5…` (`12`), `1en18-…` (`14`) перенесены в `99 — HOLD`, не в корзину.

За пределами темы «Искупление» Drive **не тронут**: личные и посторонние файлы в корне «Мой диск», папки `01`/`02`/`03`/`04`/`90` бэкенда Research и файлы других проектов не переименовывались и не перемещались. Папка `09 — SYNTHESIS` (слой агента синтеза) оставлена как есть — её файлы уникальны и повторяют имена Git-канона.

**Волна 2026-10-09b — Оуэн по 2 Пет. 2:1 и 3:9: verbatim Goold и машинная карта страниц.** Обе оси уже имели страницы Goold vol. X (348; 362–363) с волны 2026-10-08, но текст был пересказан по CCEL TXT — **другому** изданию, а смещение лист→страница проверялось колонтитулами «на глаз». Теперь: (1) verbatim взят из самого скана Goold 1850; (2) смещение −16 проверено по машинной карте IA `worksofjohnowe185010owen_page_numbers.json` (автоопределение печатных номеров по hOCR) на девяти опорах — 352→336, 359→343, **364→348**, **378→362**, **379→363**, 387→371, 411→395, 417→401, **559→543**. Четыре из них (336, 371, 395, 401) были найдены раньше независимым поиском по OCR, и карта их воспроизводит — значит 348 и 362–363 держатся с той же силой. Побочно найден **второй** локус Оуэна по 2 Пет. 3:9 — с. 543, трактат *A Dissertation on Divine Justice*, не *Death of Death*. Подробно — [`14` §2.6](14_OWEN_DEATH_OF_DEATH_BOOK_IV_LOCATORS.md), карточки **H3** и **H9** в [`12`](12_HARD_TEXTS_EXTENT_CARDS.md). Перезалиты зеркала `12`, `14` и реестр; прежние ID — в `99 — HOLD`.


### 5.1 Правила именования (волна 2026-10-09a)

Каша была в именах: `atonement-corpus-v1.json` назывались восемь разных объектов, и по имени нельзя было сказать, какой из них актуальный. Правило: **имя кодирует состояние, ID остаётся единственным ключом.**

| Шаблон | Где лежит | Пример |
|---|---|---|
| `NN — НАЗВАНИЕ — MIRROR (актуальное, git ИСКУПЛЕНИЕ/NN_…md)` | рабочая папка (`00`–`06`) | `12 — HARD TEXTS EXTENT CARDS — MIRROR (актуальное, git 12_HARD_TEXTS_EXTENT_CARDS.md)` |
| `NN — НАЗВАНИЕ — HOLD · <волна> · id <хвост ID>` | `99 — HOLD` | `12 — HARD TEXTS EXTENT CARDS — HOLD · волна g · id DUf4QCEs` |
| `NN — НАЗВАНИЕ — PRIMARY TEXT (…)` | первоисточник, а не копия Git-файла | `16 — DORT HEAD II ENGLISH 1840 — PRIMARY TEXT (независимый свидетель)` |

- **`NN` в начале** — номер файла-канона в `ИСКУПЛЕНИЕ/`. Даёт сортировку по смыслу, а не по алфавиту, и сразу показывает, к какому разделу корпуса объект относится.
- **`MIRROR`** — копия Git-файла, канон в Git. **`PRIMARY TEXT`** — того, чего в Git нет: PD-книга, перевод, verbatim-выписка.
- **Суффикс `· id <хвост>`** в `99` — последние 6–8 символов Drive ID. Делает каждую копию уникальной и позволяет найти объект по имени, не открывая его.
- **Имя никогда не бывает ключом.** Ключ — ID; переименование его не меняет, поэтому операция безопасна для ссылок из других репозиториев.
- Актуальные ID — `driveMirrors` реестра [`data/atonement-corpus-v1.json`](data/atonement-corpus-v1.json). Это SSOT; имена на Drive существуют для человека.

## 6. Что владелец может сделать дальше

1. Бумажный Banner/Eerdmans Мюррея всё ещё полезен: точные страницы под локусы внутри I.4 и пагинация Banner reset. Что именно вписать — worksheet [`08` §7.1](08_MURRAY_RAA_SOURCE_CARD.md) (9 строк). IA-экземпляр `redemptionaccomp00murr` для этого закрыт («Item not available…»), не ретраить.
2. Купить *From Heaven He Came and Sought Her*.
3. Не выкладывать владельческий HTML в публичный Product.

---

## Erratum 2026-10-15 (три строки этого ledger были верны до 2026-10-12)

1. **Erratum к «канон в Git: `ИСКУПЛЕНИЕ/agents/`»** (строки 126, 128, 134). Каталога больше нет ни в main, ни в
   одной из 27 веток: координационный слой был выведен из активного дерева (см. `00_README_AND_NAVIGATION.md` §«Что
   не входит»). Единственный живой экземпляр README и четырёх брифов — Google Docs в папке `08 — PARALLEL AGENT
   BRIEFS` (`1LkzUHWOLH1M04si64c5iQCNmHpqOBU4n`), а её file id по правилу «при перезаливке меняются» не
   фиксируются. То есть зеркало осталось единственным оригиналом. Решение (вернуть в git или удалить `parallelAgents`
   из реестра) — за владельцем; реестр помечен `parallelAgents.gitPathState`, чтобы проверка не молчала.
2. **Erratum к формулировке о wave 0.** В `99` перенесены 11 объектов волны 0 по формальному критерию «нет ни в
   одной ссылке репозитория» — содержательных претензий к ней этот ledger не содержит и не является снятием
   `RIGHTS_HOLD`/`PUBLICATION_HOLD` для её материалов.
3. **Состояние зеркал, зафиксированное измерением:** запрос к Drive `modifiedTime > '2026-10-13'` = 0 объектов,
   при этом в git `02_TERMS`, `synthesis/00_SYNTHESIS_AUTHORITY`, `synthesis/02_CONFLICT_LEDGER` правились
   14–15 октября. `driveMirrors` отстаёт от канона; при следующей перезаливке — обновлять в том же коммите.

4. **Остаточные ссылки на wave-0 в `main` (найдено сканом 2026-10-16; не «починено» молча).** Шесть мест корпуса
   цитируют `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md` — файл, которого в `main` не было никогда,
   потому что он относился к осиротевшей ветке и 2026-10-15 снят с её верхушки: `05_SOURCE_REGISTRY` (стр. 79 и 190),
   `13_DORT_II_CALVIN_OWEN_EXTENT` (стр. 26), `15_CALVIN_III24_AND_DORT_II_LOCATORS` (стр. 245),
   `16_DORT_HEAD_II_ENGLISH_1840_PRIMARY_TEXT` (стр. 4) и машинная запись
   `data/atonement-corpus-v1.json → pdLocators.dortEnglishAlternateW0Pack.name`. Смысл всех шести — провенанс по
   Drive-объекту, а не git-путь; сам текст первоисточника в каноне есть (`16_…`), потерь нет. Машинный слой помечен
   `gitStatus` с erratum (на него опираются инструменты), правки в четырёх прозаических файлах сознательно отложены
   как шум: граница периметра гейта описана в его docstring.

5. **Побочная находка того же скана, к wave-0 не относится:** строка 158 этого файла ссылается на
   `synthesis/00_README_FALLBACK_2026-10-07.md`, которого в `main` нет. Дефект существовал до PR #216; фиксирую, а не
   чиню — «вернуть файл» или «убрать ссылку» решает владелец под-корпуса synthesis.

## 7. Drive-фронт 2026-10-16: идентичность PD-копий и полный состав хаба

**Метод, а не удача.** Коннектор `download_file` выкладывает объект в `google_drive/` (каталог игнорируется
`.gitignore:1`, в git не попадает), файл разбирается локально: `PdfReader` → число страниц, метаданные, пословная
полнота текстового слоя, считанный титул. Так обходится лимит коннекторной экстракции 25 МБ, из-за которого три копии
из четырёх «не читались» и `05_SOURCE_REGISTRY` (R01) записал это как `Drive 45 MB extract fail`. Хэши больших PDF не
считывались, `99 — HOLD` не тронут, объекты удалены сразу после разбора.

| Копия | Байт | PDF-стр. | Страниц с текстом | Считанный титул / метаданные |
|---|---|---|---|---|
| Owen, *Works* `1gfKY8eX…` | 42 084 171 | 624 | 614 (98 %) | «The Works of John Owen, D.D., edited by the Rev. W. H. Goold, D.D., with Life by Rev. A. Thomson, D.D., **Vol. I**. Edinburgh: **T. & T. Clark**, 38, George Street; London: Hamilton, Adams and Co.; Dublin: John Robertson. **MDCCCLXII**»; IA `worksofjohnowen01owen` |
| Calvin, *Institutes* `1DLcwFWy…` | 45 351 929 | 696 | 688 (98 %) | «translated from the original Latin, and collated with the author's last edition in French, by **John Allen**. **Fifth American edition, revised and corrected. In two volumes. Vol. I**. Philadelphia: Presbyterian Board of Publication»; IA `institutesofchri01calv` |
| Goodwin, *Works* `1o9T7mIQ…` | 27 215 853 | 578 | **0** | скан Google Books `worksthomasgood06goodgoog` = **том VI из VI**, ни текстового слоя, ни пагинации |
| WCF `1VSp4vU5…` | 16 179 601 | 25 | **0** | «The Confession of Faith of the Assembly of Divines at Westminster», author «Presbyterian Church of England», keywords «**1946 Tercentenary Edition**» |

**Четыре следствия, каждое поперёк прежней формулировке.**

1. Копия Оуэна в Drive — **том I, а не том X**. Страниц *Goold vol. X* она подтвердить не может ни при каком лимите
   экстракции: препятствие не в размере файла, а в составе holdings. Строка 20 файла `14_OWEN_DEATH_OF_DEATH_BOOK_IV_LOCATORS.md`
   («extraction cap 25 MB → страница Goold в этом PDF по-прежнему unchecked») описывает не то препятствие.
2. При этом **привязка по номеру тома подтверждена самим нашим объектом**: «CONTENTS OF THE TWENTY-FOUR VOLUMES»
   (PDF-стр. 2) читается как «DIVISION III: CONTROVERSIAL. Vol. X. 1. A Display of Arminianism. 2. The Death of Death in
   the Death of Christ. 3. On the Death of Christ. 4. A Dissertation on Divine Justice. Vol. XI. The Doctrine of the
   Saints' Perseverance…». Печатные страницы остаются на basis скана *Johnstone & Hunter, 1850* (IA
   `worksofjohnowe185010owen`, смещение лист → страница −16); копия в Drive — перепечаток **Clark 1862**, и две эти
   пагинации не смешиваются.
3. Копия Кальвина — **перевод Аллена, том I из двух** (Книги I–II), тогда как локаторная база корпуса — **Beveridge, CTS
   1845, vol. II**. Значит «он только дубль текста» (`13_DORT_II_CALVIN_OWEN_EXTENT.md`, §2.1) неверно: дубля нет, есть
   другой перевод и неполный набор томов. Сверить wording II.12 / II.16 / II.17 можно, страницы Beveridge — нет.
4. Про совпадение числа **624**: в `14_OWEN_DEATH_OF_DEATH_BOOK_IV_LOCATORS.md` (строка 21) «624 с.» — это **печатные** страницы
   тома X в перепечатке Banner of Truth; в нашем Drive-объекте 624 — это **PDF-страницы тома I**. Совпадение чисел ничего не
   подтверждает: сопоставимы объёмы, но не нумерации. Ссылка «страница 624 нашего PDF» про том X не говорит ни слова, и
   использовать её как подтверждение пагинации Goold нельзя.

**Состав хаба `07` снят целиком, включая вложенное.** `00` = 5 (зеркала `00`, `00_README`, `01`, `02`, `06`), `01` = 5
(3 PDF + 2 зеркала), `02` = 6 (4 карточки Мюррея + RU HTML 566 938 B + ZIP 113 293 B), `03` = **1** (зеркало; ни
лексиконов, ни комментариев, ни Синодального ⇒ пункты «BDAG/HALOT/TDNT со страницами» и «Синодальный как цитатный
источник» из Drive не закрываются), `04` = 4 (WCF + 3 зеркала; ни канонов Дорта, ни PRRDT vol. III ⇒ `Rejectio`
остаётся на Wikisource-1840 без пагинации), `05` = 4 (зеркала `04`, `05`, `12` + JSON SSOT 53 098 B), `06` = 1 (Docs-
зеркало этого файла), `08` = 5 (README + 4 брифа), `09` = 7 + `drafts` 1 + `data` 1. **Английского печатного RAA в хабе
нет** ⇒ локатор Мюррея остаётся «глава RU HTML, не страница Banner».

**`99 — HOLD` = 65 объектов** (полный листинг при `page_size` 1000; «60» было бы артефактом страницы ровно на 60).
Состав посчитан по массиву имён скриптом, а не «на глаз»: **10** копий прав ли́дера (этого файла), **9** копий
`atonement-corpus-v1.json` (размером 27 097 → 49 824 B — копии различаются и по размеру, и по содержимому), **7** копий
`00_CURRENT_AUTHORITY` в трёх исторических вариантах имени, **6** — `12_`, по **4** — `05_` и `14_`, **3** — `15_`,
по **2** —
`02_` и `synthesis-corpus-v1.json`, и по **1** — `13_`, `06_`, план серии `01_` и черновик статьи `01_`, `00
SYNTHESIS AUTHORITY`,
`00 README FALLBACK`, `00 — README AND NAVIGATION`, `00 MASTER RESEARCH MAP`, `README.md`, `redemption-corpus-authority-2026-10-07.json`.
Сумма по семьям = 65, то есть ни один объект не остался неучтённым.

**«Перенесены 11 объектов» теперь не оговорка, а сверенное число.** Читать его надо не как ёмкость папки (там 65), а как
состав зеркал снятой wave-0. `git -c core.quotepath=off show --name-only c54cf68` даёт 13 снятых путей: 10 документов
(девять нумерованных и `README.md`) плюс `data/redemption-corpus-authority-2026-10-07.json` — вместе **11**; erratum: этот
JSON-путь удалён тем же снятием wave-0, в HEAD его нет и быть не должно. По именам 10 из 11 лежат в `99`; зеркало
десятого документа wave-0 — в папке `01`. Двух последних снятых путей —
`.github/workflows/redemption-corpus-integrity.yml`
и `scripts/validate_redemption_corpus.py` — в хабе нет ни под каким именем, машинная часть wave-0 в Drive не переносилась.
Значит противоречия между 11 и 65 нет и 65 не читается как «11 + мусор»: 11 — набор переноса, 65 — всё, что накопилось в `99`
после. (Снятие цифр по `git show` требует `core.quotepath=off`: без него кириллические пути печатаются в
octal-экранировке, и
проверка «сколько тут `.md`» молча даёт ноль.)

*Erratum к этому самому пункту:* первая редакция строки (записана этим же днём раньше) давала 7 и 6 копий вместо 9 и 10 —
«зрительная оценка» половины листинга. Ошибка была в моём счёте, не в Drive. Это ровно тот сорт дефекта, который два дня подряд
находился у чужих записей, поэтому он зафиксирован в тексте, а не молча перезаписан.

**Целостность ссылок реестра на Drive:** из 121 идентификатора в `data/atonement-corpus-v1.json` **115 резолвятся** в
списках снятых папок (включая `09/drafts`, `09/data` и 65 объектов `99`); **6 не резолвятся и не должны** — это
`drive.reorg2026-10-08.rootCleanup[0…2].id/.to`, записи о переезде объектов в другие хабы (Gill PDF и др.), вне темы.

**Побочное, закрывающее пункт 5 Erratum предметно:** файл, на который в строке 158 ссылается этот ли́дер, **живёт в
Drive**: `09 — SYNTHESIS (agent 4) → 00_README_FALLBACK_2026-10-07.md`, id `1lPGvBuvCEI-D3AYxtsR379BZGO3_I5Ko`,
6 303 B (мод. 2026-10-08T08:52Z). Значит выбор «внести из Drive» против «убрать ссылку» теперь обеспечен материалом, а
не догадкой; решает владелец под-корпуса synthesis.

**Зеркала отстают — измерено:** git-реестр 78 830 B против Drive-SSOT 53 098 B (мод. 2026-10-09T00:09Z); git-лидер
38 208 B против Docs-зеркала 22 691 B (там же). Перезаливку делает владелец: в моём периметре только git.
