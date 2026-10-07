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

Канон остаётся Git-файлами в `ИСКУПЛЕНИЕ/`. Docs — зеркало для чтения на Drive.

**Волна 2026-10-07b:** зеркала `00`, `05`, `07`, `12`, `13`, `15` перезалиты byte-accurate (`upload_file` с `file_path`, без пересказа). Предыдущие ID (`1bI3GKw5…`, `1yRVrEg-…`, `1a1OFbfq…`, `1wz5vC0-…`, `1KGtaHM7…`, `1QCk0y3l…`) отправлены в корзину. Актуальные ID всех зеркал — в `driveMirrors` реестра [`data/atonement-corpus-v1.json`](data/atonement-corpus-v1.json).

**Волна 2026-10-07c:** после переноса английского текста Dort Head II / Rejectio I–VII (Scott 1841) в `15` §B.5 зеркала `00`, `05`, `07`, `13`, `15` перезалиты byte-accurate; реестр `atonement-corpus-v1.json` перезалит в папку `05`. Предыдущие ID (`1FSjtZ2…`, `1M1k9Es…`, `1eEz0Nq…`, `1XdjShz…`, `1aAKDv3…` и промежуточный `1Vys7bm…`) отправлены в корзину. `14`, `11`, `12` не менялись — их ID актуальны.

После волны HARD (2026-10-07) канон Git: `11_MURRAY_OTHER_WORKS_HARD_TEXTS.md`, `12_HARD_TEXTS_EXTENT_CARDS.md`, `13_DORT_II_CALVIN_OWEN_EXTENT.md`. Зеркала на Drive — в `05` (ledgers), не вместо Git.

## 6. Что владелец может сделать дальше

1. Бумажный Banner/Eerdmans Мюррея всё ещё полезен: точные страницы под локусы внутри I.4 и пагинация Banner reset. Что именно вписать — worksheet [`08` §7.1](08_MURRAY_RAA_SOURCE_CARD.md) (9 строк). IA-экземпляр `redemptionaccomp00murr` для этого закрыт («Item not available…»), не ретраить.
2. Купить *From Heaven He Came and Sought Her*.
3. Не выкладывать владельческий HTML в публичный Product.
