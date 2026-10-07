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
| Westminster Confession | `1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4` | `1zbqz-EaFN5Fwnqo3a8ynVG4B1MpqVVVX` | PD | unchecked | HOLD |

Это `ACQUIRED_DURABLE` относительно байтов копии только после независимого SHA-readback. На старте фиксируем: **копия создана через Drive copy_file; SHA-256 readback не выполнялся.** Custody ближе к `TRANSFER_PENDING_VERIFICATION` по строгой политике. Не заявлять forensic acquisition.

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
| Current authority | `1bI3GKw5tpAV3uDHUxGwz42WmAa2i2giGkpT49USkMVM` |
| Master map | `1_0I6d9OiRapJWQ9RzsgIAu73dxeArTJSI7ViRBMPlNw` |
| Terms | `14EwvFHHCY3OlaMJ_tKQH7mGbr3Z3Fc5CqBNGrQNZO7A` |
| Biblical corpus | `1xMwEx6UA2W4N8sE3b9DKRifRnko8T4-RNZfO0_IB-Cs` |
| Question map | `1GFVUswVklNLz5VCtZRclMFj9b06nA4WUj1pjbIrtNaA` |
| Source registry | `1yRVrEg-BglE8442TvZ5iIvr3WGGmEe5TOXADRtlmE4c` |
| Rights ledger | `1a1OFbfqzHEQfGS-WBPBRRfJR-a8hu6IMfRJwx9C5-UY` |
| Murray card | `1k2iVUPhMXwtV9hrAaZwlOM0YPW-V4JPCf8q4eR43zsA` |
| 11 Murray other works (md, папка 02) | `1YjRSRZtvlYwHME_kUgis5qeSJQ-z5qZd` |
| 12 HARD cards (md, папка 05) | `1wz5vC0-0EroWw7i5mAAVY4jtMtlWzpzf` |
| 13 Dort/Calvin/Owen (md, папка 04) | `1KGtaHM7POs0aTZ8PgPPymhDxllvMB6qV` |
| 14 Owen Book IV locators (md, папка 01) | `1R7LhytnAXbTjp6iOARBkdMLFXzZ7bU25` |
| 15 Calvin III.24 + Dort II (md, папка 04) | `1Au1ykvia5zWdHxt0OxbQaCRFPb0B9KH2` |

Канон остаётся Git-файлами в `ИСКУПЛЕНИЕ/`. Docs — зеркало для чтения на Drive.

После волны HARD (2026-10-07) канон Git: `11_MURRAY_OTHER_WORKS_HARD_TEXTS.md`, `12_HARD_TEXTS_EXTENT_CARDS.md`, `13_DORT_II_CALVIN_OWEN_EXTENT.md`. Зеркала на Drive — в `05` (ledgers), не вместо Git.

## 6. Что владелец может сделать дальше

1. Бумажный Banner/Eerdmans Мюррея всё ещё полезен: английские страницы как locator.
2. Купить *From Heaven He Came and Sought Her*.
3. Не выкладывать владельческий HTML в публичный Product.
