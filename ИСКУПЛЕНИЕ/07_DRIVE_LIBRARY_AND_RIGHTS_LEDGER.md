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

**Волна 2026-10-08f — Оуэн по Тит. 2:11 и 1 Тим. 2:6 (Goold vol. X, 1850).** Четвёртая волна локаторов: `14` §2.4 даёт страницы абзаца для двух локусов, которых в каноне не было, — **Тит. 2:11 — с. 336 и 395** и **1 Тим. 2:6 — с. 307 и 371**. Смещение лист − 16 подтверждено уже не тремя, а десятком колонтитулов подряд (306/314/320/336/350 … = листы 322/330/336/352/366 без разрывов). Карточка **H10** (Тит. 2:11) из состояния «один первоисточник» перешла в состояние «два независимых свидетеля с PD-страницами»: Кальвин CTS 1856 + Оуэн Goold 1850. Зеркала перезалиты по канону; прежние ID — в `99 — HOLD`.

**Волна 2026-10-08e — Кальвин, комментарий на Пастырские послания (CTS 1856).** В канон вошёл второй том CTS-комментариев: IA `commentariesonep00calvuoft`, 1856, `NOT_IN_COPYRIGHT`. Локаторы — 1 Тим. 2:4 (с. 54–55), 2:5 (с. 56), 2:6 (с. 61), Тит. 2:11 (с. 316–318). Затронуло `15` (новый §A.4), `12` (новые чтения H2-e / H2-f и **новая карточка H10 по Тит. 2:11** — раньше локус значился обязательным в `03`, но своей карточки не имел), `03`, `05` (строка `R02b`), `00` и реестр; в слое синтеза — уточнение `C-03` и новый конфликт `C-16` (Кальвин против Кальвина: «сословия» на 2:4 vs «плод жертвы простирается на всех» на 2:5). Зеркала перезалиты по канону; прежние ID — в `99 — HOLD`. Ветка агента `arena/5fe5b33f-research` на GitHub отсутствует (404) — перенос сделан в ветке координатора `arena/dddc1326-research`. Правки при приёмке: снято приписанное Мюррею «закрытие» 2 Кор. 5:14 и Евр. 2:9 (материнский `10` §3 это запрещает), счёт расхождений 12 → 15 по факту реестра, цитата Мф. 11:28 приведена к Синодальному, реплика «нельзя молиться за каждого (1 Ин. 5:16)» атрибутирована как чтение Оуэна. Ни один HOLD не снят; вердикта по объёму нет.

## 6. Что владелец может сделать дальше

1. Бумажный Banner/Eerdmans Мюррея всё ещё полезен: точные страницы под локусы внутри I.4 и пагинация Banner reset. Что именно вписать — worksheet [`08` §7.1](08_MURRAY_RAA_SOURCE_CARD.md) (9 строк). IA-экземпляр `redemptionaccomp00murr` для этого закрыт («Item not available…»), не ретраить.
2. Купить *From Heaven He Came and Sought Her*.
3. Не выкладывать владельческий HTML в публичный Product.
