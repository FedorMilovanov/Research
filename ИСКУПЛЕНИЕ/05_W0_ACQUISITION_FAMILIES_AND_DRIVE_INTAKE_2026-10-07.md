# W0 — Acquisition families и Drive intake

**Дата:** 2026-10-07
**Статус:** `CURRENT / REQUEST-READY / 0 VERIFIED FILE RECEIPTS / 0 QUOTE-READY FAMILIES`
**Drive root:** `07 — СЕРИЯ «ИСКУПЛЕНИЕ»` → folder id `1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV`
**Custody policy:** [`../data/artifact-custody-policy-v2.json`](../data/artifact-custody-policy-v2.json)

---

## 1. Что здесь владеет

Этот документ определяет, **как** корпус добывает книги и тексты, и что засчитывается как приёмка. Он не является реестром источников (реестр — `03_...`) и не является списком источников для статьи.

Принцип, перенесённый из Gill- и Baptist-lane этого репозитория:

```text
Request package READY  ≠  файлы получены
Файл в Drive            ≠  receipt
Receipt                 ≠  quote-ready
Quote-ready             ≠  publication approval
```

## 2. Соответствие слоёв реестра и папок Drive

| Drive-папка (имя / id) | Что в неё кладётся | Слой `03_...` |
|---|---|---|
| `00 — INDEX, AUTHORITY & SERIES MAP` / `1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL` | index-файлы корпуса, series map, статусная карточка | — |
| `01 — PUBLIC DOMAIN LIBRARY — Owen, Calvin, Goodwin, Confessions` / `1BuYqlnPM1pIw-pCIFZLOKgGLL3hR1F4t` | тексты, чей PD-статус проверен (оригинал **и** перевод/редакторский аппарат) | P, O, C(PD) |
| `02 — COPYRIGHT BIBLIOGRAPHY & ACQUISITION — Murray and moderns` / `1FdQlbxhVzhAdCPoS1lt2qEZMRPsaQNPI` | библиографические карточки + легальные каналы (издатель, библиотека, официальный open-access). **Пиратские копии сюда не загружаются** | M |
| `03 — SCRIPTURE, LEXICA & COMMENTARIES` / `17BZ9SUu5zp5VVFd5a0t8mFX8wEodHcIv` | инвентарь текстов, лексические карточки, комментарийные зависимости | L, C |
| `04 — CONFESSIONS & HISTORICAL THEOLOGY` / `1ZTD2idu9oFO9Et1MSgfgtKMZZg63yUTw` | первичные конфессиональные тексты и исторические документы | P, O |
| `05 — SOURCE LEDGERS & CLAIM MAPS` / `13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ` | реестры, claim-карты, зеркала machine-JSON | — |
| `06 — RIGHTS, HOLD & PROVENANCE` / `1edsBGRg0oQw_G-75QYdaNvde7KKiCFQy` | манифесты, SHA256SUMS, provenance-заметки, HOLD-реестр | — |

Правило: **файл без записи в реестре — не источник. Источник без прав — не цитата.**

## 3. Receipt-политика

```text
RECEIVED требует:      file name, byte size, sha256, received_at, путь durable storage
USABLE требует:       идентичность издания, сверка титульных данных, объём/оглавление, rights_state
QUOTE-READY требует:  страница/раздел проверены по объекту, quote-card, контекстное окно, rights_basis
```

`driveNameAloneIsReceipt = false`; `previewAloneIsFullText = false`; `bibliographyAloneSupportsClaim = false`.

## 4. Семьи acquisition

### `RED-FAM-DORT-ACTS` — Дорт: Rejection of Errors, акты, латынь
- **Claim-scopes:** что именно осуждено; отношения «canons vs acts»; латинский текст против перевода 1840.
- **Owner-документы:** `10_...` §5, §7; `03_...` `RED-SRC-0002/0004`.
- **Что искать:** издания канонов с разделами Errors/Rejections по каждой главе; латинский текст; аннотированные переводы (Gatiss, `RED-SRC-0407`); actes Synodi Nationalis (лат./нидерл.).
- **Критерий приёмки:** полный документ + страница + выходные данные; скриншот/поисковый сниппет — не приёмка.

### `RED-FAM-REMONSTRANCE` — Remonstrance 1610 и remonstrantская ортодоксия
- **Claim-scopes:** что арминиане утверждали своими словами; отличие Arminius / Remonstrants / Episcopius / Limborch.
- **Что искать:** латинский текст Exhibitio articulorum + переводы; Works Arminius (пер. Nichols? — уточнить издание); Episcopius; Limborch.
- **Критерий:** цитируемый пункт обязан быть сверен с нумерацией статей в издании.

### `RED-FAM-OWEN`
- **Claim-scopes:** аргументация кн. I; разбор «всеобщих текстов» в кн. IV; «Of the Death of Christ» против Baxter; intercession; «duty-faith».
- **Owner:** тексты Оуэна — наши; цитатные карточки — с томом/страницей конкретного издания (издание Works фиксируется явно (перепечатка Banner vs цифровой текст — это разные локаторы)).
- **Что искать:** полный том 10 Works (PDF в open law? — нет; искать на электронных библиотеках с проверкой PD-статуса перевода/аппарата), плюс Packer introduction (copyrighted — отдельная запись).
- **Критерий:** том + страница + издание; пересказ у вторичных авторов — `C`.

### `RED-FAM-MURRAY` — центральный учебник серии
- **Claim-scopes:** необходимость / природа / совершенство / **простирание**; соотношение accomplished ↔ applied.
- **Состояние:** библиография подтверждена (Eerdmans 1955; оглавление; в издании Banner 2014 — 200 стр., гл. IV на стр. 51). Права: COPYRIGHT — `RIGHTS_HOLD`.
- **Легальные каналы:** издатель (Eerdmans), Banner of Truth eBook, библиотечные программы, официальные sample/preview. **Не загружать в Drive неавторизованные копии.**
- **Критерий приёмки:** читаемая полная копия, принадлежащая владельцу/библиотеке, с фиксацией постраничной нумерации конкретного использованного издания.

### `RED-FAM-GIBSON-ANTHOLOGY`
- **Claim-scopes:** 23 главы как систематическая защита; отдельные эссе (Schreiner, Williams, Blocher, Gatiss, Djaballah, Trueman, Harmon, Motyer, Strange, Ferguson, Piper).
- **Что искать:** P&R 2013, 704 pp; страницы начал глав подтверждены из оглавления (см. `03_...` `RED-SRC-0402`).
- **Критерий:** по каждой цитируемой главе — страница; «per chapter» недостаточно.

### `RED-FAM-DAVENANT`
- **Claim-scopes:** `sufficienter/efficaciter`, acceptatio, «public worth» vs payment; роль в Westminster? (отдельный claim — только по актам).
- **Что искать:** лат. *De Morte Christi Dissertatio Dubia* (1650?) и ранние англ. переводы;Works-издание (Vol. 3? — уточнить по каталогу).
- **Риск:** цитировать Davenant по вторичному пересказу о «Davenantism» — самая частая ошибка в этой теме.

### `RED-FAM-AMYRAUT` (Saumur)
- **Claim-scopes:** двухуровневый decree; отношение к Дорту; соборные решения по его учению; отличие от Arminius.
- **Что искать:** *Brief Tretté* / *Traicté de la prédestination et de ses dépendances* (1658) — фр./лат.; исследования: Djaballah; Crisp; исторические монографии (точные названия — только после подтверждения в каталоге).
- **HOLD:** вся первичная формулировка — `EVIDENCE_HOLD`, пока не получена.

### `RED-FAM-BAXTER-MANTON`
- **Claim-scopes:** «disputation of universal redemption» (уточнить точное название трактата), ответы Owen/Manton; последствия для free offer.
- **Критерий:** страницы по изданию Works/периодическим изданиям XVII в.

### `RED-FAM-LEX` — лексикография `ἱλασ*`, `λυτρ*`, `ἀγορα*`, `καταλλαγή`, `πᾶς`/`κόσμος`
- **Что искать:** BDAG (3rd ed.) статьи; HALOT; TDNT/NIDNTTE; Trench (PD); Girdlestone (PD); конкордансные подсчёты; статья Wallace (только подтверждённая публикация — `RED-SRC-0209`).
- **Критерий:** статья словаря = название статьи + страница; «BDAG говорит» недостаточно.

### `RED-FAM-NT-COMM` — комментарийный слой по 12 locus
- **Что искать:** конкретные серии и тома (Hebrews, Catholic Epistles, 2 Peter, Pastoral epistles) подбираются по автору и году — **никакой комментарий не вносится в реестр без подтверждённых автора, года и издателя**.
- **PD-кандидаты первой очереди:** Delitzsch on Hebrews (англ. пер. XIX в. — проверить статус перевода), Alford (уже использован в `../SOURCE_LIBRARY/processed/1COR11_PRIMARY/` как проверенный sample), Calvin (есть), Lange (есть русский перевод — права перевода проверить).

### `RED-FAM-RUSSIAN` — русско-язычный пласт
- **Что искать:** Толковая Библия (Лопухин), протестантская энциклопедия нач. XX в., Макарий (Булгаков), русские переводы Кальвина/Оуэна/Бавинка, дореволюционные баптистские катехизисы и периодика (пересечение с `../RUSSIAN_BAPTISTS_ARCHIVE/` — там же права и скан-политика).
- **Критерий:** для русского перевода — библиографические данные перевода + права; для PD-сканов — страница с титулом.
- **Особая ценность:** это тот слой, который отличает отдел от перевода англо-спора.

### `RED-FAM-GILL` — заказ владельцу, а не дублирование
- **Claim-scopes:** offer, duty-faith, external call; Gill на Isa 53, 1 Ин. 2:2, 2 Пет. 2:1.
- **Правило:** наш корпус **не** заводит собственных Gill-цитат. Мы отправляем claim-запрос в `../Джон Гилл/` (см. `data/gill-closed-book-families-2026-08-02.json`, семья `GILL-FAM-ASCOL`) и получаем ответ как input.

### `RED-FAM-RECEIPT-AUDIT`
- Каждое закрытое семейство получает receipt-запись в machine JSON (`acquisitionFamilies[].receipts`), с sha256 и правами; без записи семейство остаётся `EXTERNAL_ACQUISITION_REQUIRED`.

## 5. Права — жёсткие границы (в частности для «книги в Drive»)

1. **Можно:** размещать тексты, чей public-domain статус подтверждён для конкретной редакции/перевода; собственные research-документы; манифесты; карточки библиографии; ссылки на легальные open-access.
2. **Нельзя:** загружать в Drive PDF современных книг (Мюррей, Packer, Gibson, Schreiner, Stott, Morris, Amyx, Pinnock, Bavinck, Carson, …), даже «для внутреннего пользования», если права не установлены. Это не пуританство, а репутационная и юридическая гигиена проекта, и она записана в `AGENT_RULES` как `RIGHTS_HOLD`.
3. **Серая зона, требующая решения владельца:** сканы PD-оригиналов, отсканированные библиотекой с утверждением о праве на репринт-аппарат; переводы, изданные после 1930 г. с PD-оригиналов. Правило корпуса: пока вопрос не решён, файл может лежать в `06 — RIGHTS, HOLD & PROVENANCE` как `EPHEMERAL_ACTION_ARTIFACT`, но не в `01 — PUBLIC DOMAIN LIBRARY`, и не даёт права на цитату.
4. **Открытые репозитории и официальные архивы** — предпочтительный канал; ссылка + дата доступа + снимок метаданных (см. `../SOURCE_LIBRARY/CURRENT_SOURCE_URL_AUTHORITY_2026-08-02.md`).

## 6. Текущее состояние

```text
FAMILIES = 13
VERIFIED FILE RECEIPTS = 1   (Dort Head II, Arts I–IX — verified text, см. 10_...)
QUOTE-READY FAMILIES = 1     (RED-FAM-DORT-ACTS — частично: Arts I–IX)
NEW DIRECT QUOTES FROM COPYRIGHT BOOKS = 0
USER-PLACED FILES IN Drive = 0 (папки созданы, пустые на момент открытия волны)
```

Внешние зависимости (библиотеки, издатели, платные доступы) не являются «ничьим» вопросом: у каждой есть family-owner, request-запрос и критерий приёмки (§4). Но Research не может сфабриковать отсутствующие байты — и не будет.

## 7. Следующее проверяемое действие

1. Отправить запросы по `RED-FAM-DORT-ACTS`, `RED-FAM-REMONSTRANCE`, `RED-FAM-LEX` — они не требуют платного доступа.
2. Для `RED-FAM-MURRAY` и `RED-FAM-GIBSON-ANTHOLOGY` — зафиксировать легальный канал чтения (электронная библиотека владельца), потому что без них серия не имеет учебникового каркаса.
3. Не начинать: загрузку «всех найденных PDF», расширение реестра ради числа, написание reader-draft.
