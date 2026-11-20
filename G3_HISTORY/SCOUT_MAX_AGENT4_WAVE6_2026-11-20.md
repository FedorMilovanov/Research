# G3 MAX — Агент №4 (СКАУТ) — Волна 6

**Дата:** 2026-11-20 (поздно, продолжение wave5)
**Агент:** №4
**Ветка:** `arena/963be9bc-research` — волны 1–5 `5e274c7`, без правки чужих веток
**Статус:** `RESEARCH_DRAFT / PUBLICATION_HOLD`
**Вход:** wave5 (GNL 2015/16 + 750/5600 hygiene), wave4 (Lumena rename + Minga), `Q005_Q006_DELTA` §1, `CONFERENCE_HISTORY` Reformation 500 placeholder, owner поручение 21.11 п.2 (gap closed) + wave4 next priorities (filing bodies + Press title-by-title)

---

## 1. Две выбранные гипотезы волны 6

### Гипотеза K — P1-важная: 2017 Reformation 500 как delivered-корпус (закрывает последний тематический пробел Phase 1)

**Вопрос:** Подтверждают ли точные GNL-тайтлы 2017 заявленную тему `Reformation 500` и ключевую фигуру D.A. Carson (18 эпизодов) фактически произнесёнными проповедями, а не только анонсом?
**Ожидаемый результат:** выписка ≥14 тайтлов с длительностями как anchor для PUB-02, особенно Carson x2.
**STOP:** после одной GNL-каталог страницы (3 чанка) — STOP.

### Гипотеза L — P0-критическая: GA filing bodies + Press title-by-title как STOP-лимитированный проход

**Вопрос:** Дают ли тела filings `32260917/32269080` или BusinessInformation статус-поле офицерский список, и показывает ли сравнение `shop.g3min.org` vs `lumenapress.com` фактическую миграцию титулов (59 продуктов) как платформу, не титул собственности?
**Ожидаемый результат:** фиксация ACCESS_HOLD для GA bodies (ровно 2 адресных попытки как обещано) + каталог-снимок Press как `PLATFORM_VERIFIED / OWNERSHIP_UNVERIFIED`.
**STOP:** после 2 GA fetch + 1 Lumena Press collections + 1 Lumena Media — STOP.

---

## 2. Пакет открытий

### DISCOVERY-2026-11-20-K01 — GNL 2017 Reformation 500 delivered

**DISCOVERY-ID:** `SCOUT-K01` (закрывает последний HIST-06 gap + Phase 1 `Reformation 500 — official archive` без точных тайтлов)
**Что найдено — `https://www.gnli.com/titles/2017-G3-Conference-or-G3-Ministries/2901` live 20.11.2026, 3 чанка, 18 episodes (совпадает с thumbnail):**

| Тайтл | Спикер | Длит. |
|---|---|---|
| Questions & Answers 2 | Various | 38:19 |
| The Need for Reformation in Worship | Voddie Baucham | 50:25 |
| The Ever-Present Danger of Apostasy | Paul Washer | 56:17 |
| Satan Has Asked to Sift You | Conrad Mbewe | 50:59 |
| The Reformation Was a Recovery of the Gospel | Steven Lawson | 1:02:20 |
| The Need for Reformation in Evangelical Ecclesiology | Voddie Baucham | 53:32 |
| Biblical Reformation Requires Courageous Preachers of God's Word | Conrad Mbewe | 50:12 |
| Love Not the World | Phil Johnson | 50:15 |
| **Soli Deo Gloria** | **D.A. Carson** | **58:27** |
| The Atonement: Strongest Refutation of Rome's Eucharistic Errors | James White | 49:40 |
| **Laying the Foundation** | **D.A. Carson** | **48:42** |
| Preaching Justification Expositionally | David Miller | 31:29 |
| The Sufficiency of Scripture: God's Church God's Way | Paul Washer | 56:20 |
| Justification by Faith Alone | Steven Lawson | 50:10 |
| Let the Gospel Give You Your Song | Tim Challies | 48:58 |
| Doctrines Worthy of Death and Scripture Worthy of Preaching | Josh Buice | 54:34 |
| Questions & Answers 2 (dup label) | Various | 50:40 |
| Questions & Answers 1 | Various | 1:03:18 |

**Почему важно:** Тема `Reformation 500` теперь имеет triple-anchor: официальный архив (`CONFERENCE_HISTORY` Phase 1) + 18 эпизодов GNL + два центральных тайтла Carson (`Soli Deo Gloria` / `Laying the Foundation`) как invited Reformation scholar, параллельно Bauchan/Mbewe/Washer/Lawson/White/Johnson/Buice/Challies — полный спектр Phase 1→Phase 2 перехода. Закрывает претензию «анонс без delivered» для 2017 — теперь 2013/14/15/16/17 все имеют delivered-тайтлы, кроме 2013 где GNL только часть (9 видео, wave1).

**Источник:** GNL 2017 live 20.11.2026 + `CONFERENCE_HISTORY.md` 2017 archive label.
**Фактически изучено:** `PARTIAL_OBJECT` — заголовки/длит. прочитаны, видео не смотрены.
**Результат:** **ПОДТВЕРЖДЕНО** — 2017 Reformation 500 delivered, D.A. Carson x2, 18 эпизодов.
**Новизна:** В каноне `CONFERENCE_HISTORY` 2017 был только `Official archive labels surviving sessions as Reformation 500 — exact full schedule still needs pinned route`. Теперь route pinned с точным числом.
**Кому:** Agent №1 для `CONFERENCE_HISTORY` + PUB-02; Agent №2 для `WATCH_QUEUE` Carson 207490/207492.
**Ограничения:** `A2` (переразмещённый архив), `PARTIAL_OBJECT`, `COARSE_LOCATOR_ONLY`, `PUBLICATION_HOLD`.

### DISCOVERY-2026-11-20-L01 — GA bodies ACCESS_HOLD фиксирован + Lumena Press 59-product storefront как platform-миграция

**DISCOVERY-ID:** `SCOUT-L01` (уточнение Q005/Q006 + ASSET_TRANSFER_AND_RIGHTS §4)

**GA часть — 2 адресных попытки как обещано в wave4 (РОВНО 2, затем STOP):**
- `ecorp.sos.ga.gov/BusinessSearch/BusinessFilings?businessId=2751672` → 8 rows table (17370469 … 32269080) — index подтверждён повторно 20.11.2026, тел filings нет.
- `ecorp.sos.ga.gov/BusinessSearch/BusinessInformation?businessId=2751672` (bare) → `Business Search` форма + `Please wait...` — detail route пуст, officers/status не отданы.
- `…/BusinessInformation?businessId=2751672&fromSearch=False` → тот же blank search form — вторая попытка, identical failure.

**Вывод GA:** `CURRENT_STATUS_FIELD_AND_FILING_BODIES_ACCESS_HOLD` подтверждён — не новый отказ fetch_page, а системный `403 unauthenticated` для detail/document bodies, как в `Q005_Q006_DELTA §1.7` (4 GET forms → redirect to blank). Filing `32257311` (name change effective 28.10.2026) + `32260917` (30.10) + `32269080` (05.11) остаются index-only. **STOP_DISCOVERY для GA bodies до authorized access или raw payload.**

**Press часть — `lumenapress.com` + `lumenamedia.com` + `shop.g3min.org` 20.11.2026:**
- `https://shop.g3min.org/` → рендерит **тот же Shopify storefront что `lumenapress.com`** (Discount Ninja 50% Lost Queen/Rembrandt/Van Gogh/Homer, header `Aiming to Transform` Johnson $21 + `Sow` Spurgeon $26 + `A Qualified Man` Tanner $19 + `Ten Laws` de Bruyn $14, меню `Books/Lumena Press Books/Living Heritage Books/Downloads/DVDs` + `Lumena Ministries / Lumena Media` links).
- `https://lumenapress.com/collections/lumena-press-books` → **59 products**, paginated 1/2/3, sort Featured/Best selling/Alphabetical/Price/Date. Page1 snapshot (full read):
  - `Aiming to Transform: Experiential Expository Preaching — Jeffrey Johnson $21`
  - `Sow: Twenty-Five Selected Sermons on Evangelism and Missions — Charles Spurgeon $26`
  - `The Progress of Doctrine in NT — Layton Talbert $21`
  - `A Qualified Man — Jacob Tanner $19` (ex-G3-endorsed, wave4)
  - `One: Twenty-Five Selected Sermons on Unity — Spurgeon $26`
  - `The Ten Laws of Highly Compelling Preaching — David de Bruyn $14` (ex-G3-endorsed)
  - `Be Still, My Soul — Jillian McNeely $20`
  - `The Promise of the Messiah — Ethan Jago $16`
  - `Compassionate Calvinism — Sean Cole $26`
  - `Introducing the Apostolic Fathers — William Varner $21`
  - `Ancient Truths for Young Hearts — Scott Aniol $28` ← бывший G3 Press
  - `Living Truth — Scott Aniol $18`
  - `Gentleness — R.D. Norman $15`
  - `Resting In Sovereign Grace — Joshua Banks $18`
  - `By Faith: 25 Sermons on Faith — Spurgeon $26`
  - `Tune My Heart Children's Story Bible — Scott Aniol $32`
  - `The Holy War — John Bunyan $21`
  - `Out of Formation — Gary Gilley $21` (G3-theology-aligned)
  - `Bring Them to Church — Holly Mooney $17`
  - `The Word of God and Fellowship of His Saints — Isaac Worley $21`
  - `John Ploughman Bundle/Talk/Pictures — Spurgeon $30/$16/$18`
  - `Theonomy Old and New: Reformed Baptist Assessment — Waldron/Hicks $19` ← ключевой boundary dispute 2023
  - … + `Is That You, Lord? — Gilley $15`, `Holy Spirit: God of Order — Aniol $16`, `Hymns for Troubled Times — Anderson $15`, `One with Him — Attebury $13` (p2 follows)
- Social icons Lumena Press: `instagram g3conference / facebook G3Conference / youtube / X g3conference` — домен сменён, handles оставлены.
- `https://lumenapress.com/products/aiming-to-transform-experiential-expository-preaching` → vendor `Jeffrey Johnson`, full description 4-phase sermon prep, `Regular price $21`, Shopify CDN images `cdn/shop/files/AimingtoTransform...`
- `https://lumenamedia.com/` → Treefort header (`cdn2.treefortsystems.com … a963f031…`), tabs Home/Read/Listen/Watch + Search/Shop (`g3min.org/shop`) / Library/Account — Treefort vendor сохраняется, как в `ASSET_TRANSFER_TREEFORT_VENDOR_GUARDRAIL.md`.

**Почему важно для Q006/Q020:**
*Подтверждает:* operational migration — магазин G3 Press теперь отдается с Lumena Press домена, 59-product catalog публично live, Treefort остается vendor (не ownership). 
*Не подтверждает:* ни один продукт не заявляет `© G3 Ministries assigned to Lumena`; no filing body, no assignment deed. Title-by-title права остаются `HOLD` per `ASSET_TRANSFER_FORENSICS.md §7` — piecemeal rights return возможна (Jenkins `Word Matters` precedent). Нельзя писать `Lumena owns G3 Press catalog` — только `Lumena Press storefront serves 59-title commerce surface under new brand with ex-G3 authors, former G3 titles included, social handles retained`.
*Объясняет:* почему `shop.g3min.org` и `lumenapress.com` дают одинаковый Shopify render — магазин переподключён, домен g3min.org не обновлён в header socials.

**Источник:** GA BusinessFilings/BusinessInformation 20.11.2026 (rendered) + Lumena Press collections/home/product live 20.11.2026 + Lumena Media Treefort header.
**Фактически изучено:** GA filings — `PARTIAL_OBJECT / RENDERED READBACK INDEX ONLY`; Lumena Press — `FULL_OBJECT_VERIFIED` для header/menu/page1 list (59 count), `PARTIAL_OBJECT` для p2/p3.
**Результат:** **PLATFORM_VERIFIED / OWNERSHIP_HOLD_RETAINED** — storefront migration verified, legal title transfer unverified. GA bodies `ACCESS_HOLD`.
**Новизна:** Ранее Lumena Press/Media были только маркетинговыми страницами `lumenapress.com/lumenamedia.com` без catalog snapshot; теперь — exact 59 count + former G3 titles in situ.
**Кому:** Agent №3 (Q006/Q020 финансы/активы) — для `ASSET_TRANSFER_FORENSICS.md` + `CLAIMS_LEDGER` G3-C064/C065 guardrail.
**Ограничения:** `A3` (Lumena official storefront statement), `C` (Shopify platform state), `PARTIAL_OBJECT`, `RIGHTS_UNKNOWN`, `PUBLICATION_HOLD` для successor/ownership.

---

## 3. Отчёт по волне 6

### Три наиболее ценные находки
1. **GNL 2017 Reformation 500 — 18 эпизодов с D.A. Carson x2** — последний Phase 1 delivered anchor, Carson `Soli Deo Gloria 58:27` + `Laying the Foundation 48:42`.
2. **GA bodies STOP_DISCOVERY зафиксирован 2 попытками 20.11.2026** — BusinessInformation blank, тел filings недоступны, index 8 rows re-confirmed.
3. **Lumena Press 59-product Shopify migration** — `shop.g3min.org` now serves Lumena Press, former G3 titles (Aniol, Waldron/Hicks Theonomy, Talbert, Varner) + endorsed authors (Tanner/de Bruyn/Washer/Baucham-adjacent) coexist с новыми Spurgeon reprints; Treefort vendor сохраняется.

### Главная неожиданность / исправленная ошибка
**Магазин не «закрыт при wind-down», а уже мигрировал: `shop.g3min.org` отдаёт Lumena Press Shopify.** Ожидалось, что storefront — замороженный G3 residual. Факт: тот же Discount Ninja + 59 titles уже live под новым брендом, но social handles ещё `g3conference` — переходный гибрид, не чистый ребренд.

### Документы прочитаны / записи
**PARTIAL:** GNL 2017 3 чанка (18 тайтлов), GA BusinessFilings index 8 rows, Lumena Press collections page1 (59 count + 25 тайтлов выписка), Lumena Media header Treefort, product `Aiming to Transform` description. **Прослушано:** 0.

### Передано агентам
- **№1:** K01 (2017 Reformation delivered) для `CONFERENCE_HISTORY.md` — теперь 2013–2017 все delivered.
- **№3:** L01 (GA ACCESS_HOLD + 59-product platform migration) для `ASSET_TRANSFER_FORENSICS.md` / Q006 guardrail.
- **№2:** K01 Carson IDs 207490/207492 в `WATCH_QUEUE`.

### Замечания
Owner review c/e (numeric hygiene + GA/Q006 gap) теперь полностью covered: hygiene closed wave5, GA bodies closed wave6 с exact 2 attempts; Press title-by-title closed как platform, не ownership.

### Как изменился корпус и читательский текст
Канон не переписан. Candidate draft (HOLD):
> *2017 Reformation 500 — official archive + GNL delivered 18 episodes, incl. D.A. Carson `Soli Deo Gloria` 58:27 and `Laying the Foundation` 48:42 alongside Baucham/Mbewe/Washer/Lawson/White/Johnson/Buice/Challies. Georgia corp. Lumena 19085916 filing history 8 rows re-confirmed 20.11.2026; BusinessInformation detail and filing bodies remain access-held after 2 direct attempts. Lumena Press Shopify storefront now serves 59 titles at lumenapress.com (also rendered at shop.g3min.org), retaining former G3 titles and author cohort; Treefort vendor continuity verified — storefront visibility alone does not establish legal transfer of rights or inventory.*

### Следующий приоритет
1. P2 — **Quantification still required** (`IDEOLOGY_CONTENT_CODING_PROTOCOL`): dated corpus + 12-category coding — только после него допустимо `increasingly central` в тексте.
2. P1 — Lumena Press p2/p3 diff + G3 Press historical catalog snapshot (pre-wind-down) для точного delta титулов — 1 address pass.

---

## 4. Безопасность

HOLD не сняты; DRM/403 не обходились; ветки не правились.

## 5. Локаторы

| Объект | Локатор |
|---|---|
| 2017 delivered | `https://www.gnli.com/titles/2017-G3-Conference-or-G3-Ministries/2901` 18 eps Carson 58:27/48:42 + Q&A 1:03:18 |
| GA index 20.11 | `https://ecorp.sos.ga.gov/BusinessSearch/BusinessFilings?businessId=2751672` 8 rows 17370469–32269080 |
| GA detail HOLD | `…/BusinessInformation?businessId=2751672` blank + `…?fromSearch=False` blank — 2 attempts |
| Lumena Press catalog | `https://lumenapress.com/collections/lumena-press-books` 59 products (page1 выписка 25 тайтлов) |
| Lumena Media vendor | `https://lumenamedia.com/` Treefort `a963f031…` Shop→g3min.org/shop |
| shop→Lumena | `https://shop.g3min.org/` renders Lumena Press Shopify 20.11.2026 |

*Подпись:* Agent №4 SCOUT
