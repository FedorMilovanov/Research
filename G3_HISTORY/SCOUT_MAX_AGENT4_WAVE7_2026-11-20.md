# G3 MAX — Агент №4 (СКАУТ) — Волна 7

**Дата:** 2026-11-20 (продолжение, ночь)
**Агент:** №4
**Ветка:** `arena/963be9bc-research` — волны 1–6 `e9e09a1`, без правки чужих веток
**Статус:** `RESEARCH_DRAFT / PUBLICATION_HOLD`
**Вход:** wave6 (2017 delivered + GA HOLD + 59-title platform), `2021_MACARTHUR_LIVE_EPISODE.md` (ARCHIVE_HOLD), `OPEN_QUESTIONS` Q016/Q020, Wayback calendar `g3min.org/podcast` + `shop.g3min.org` + `lumenapress.com` p2/p3 live 20.11.2026

---

## 1. Две выбранные гипотезы волны 7

### Гипотеза M — P1-важная: Q016 January 2021 MacArthur `live` episode — продвинуть с `PARTIALLY_VERIFIED` к `ARCHIVE_PINNED`

**Вопрос:** Подтверждает ли независимый архив Wayback точную дату/длительность эпизода `Episode 31 — Interview with John MacArthur Jan 07 2021 50:43`, и сохраняет ли он хронологию `Oct 2020 recording → Jan 2021 premiere`, не полагаясь только на adversarial compilation Detwiler?
**Ожидаемый результат:** pinned Wayback локатор для даты/тайтла как primary-объект, хронология `a few weeks` остаётся спорной, `live` semantics остаётся `INTENT_UNPROVED`.
**STOP:** после двух podcast-каптов (20210121 + 202010 calendar) — STOP.

### Гипотеза N — P1-важная: Q020 title-by-title Press delta — точный snapshot `42 → 59`

**Вопрос:** Сколько титулов было в `shop.g3min.org/collections/g3-press-books` на последнем pre-wind-down snapshot (Dec 22 2024: 42 products) против `lumenapress.com/collections/lumena-press-books` now (59 products) — и что это доказывает о миграции, не о юридической передаче прав?
**Ожидаемый результат:** точный count delta + примеры удержанных/новых тайтлов + guardrail `STORE_COUNT ≠ RIGHTS_TRANSFER`.
**STOP:** после одного historical capture (20241222) + live p2/p3 — STOP.

---

## 2. Пакет открытий

### DISCOVERY-2026-11-20-M01 — Q016 MacArthur episode date pinned via Wayback

**DISCOVERY-ID:** `SCOUT-M01` (upgrade Q016 / `2021_MACARTHUR_LIVE_EPISODE.md`)
**Что найдено:**
- **Wayback `https://web.archive.org/web/20210121022916/https://g3min.org/podcast/` (36 captures 21 Jan 2021–21 Aug 2026, first 21 Jan 2021):**
  ```
  Episode 32 — Spurgeon, Susie, and Gospel Ministry  Jan 14, 2021  Duration: 39:58
  Episode 31 — Interview with John MacArthur          Jan 07, 2021  Duration: 50:43
    [macarthur-copy.jpg + josh-buice.jpg]
  Episode 30 — Season 2 Begins with Virgil Walker!    Dec 17, 2020  Duration: 36:07
  Episode 29 — Romans 13 and Civil Disobedience        Jul 31, 2020
  ```
  Плюс Jan 4 2021 homepage capture `20210104142628` показывает G3 2021 `Christ` + тренд `Do Black Lives Matter? Walker Dec 28 2020` + `Will You Read Bible With Me Buice Dec 29 2020` — контекст без MacArthur promotion text.

- **Calendar `https://web.archive.org/web/20201001000000*/https://g3min.org/podcast/` + Jan 2021 calendar:** 414 captures g3min.org 07 Dec 2020–12 Oct 2026, Jan 2021 has 21,04,01 captures — подтверждает, что `Jan 07` не поздняя правка, а contemporaneous podcast list.

**Почему важно:** Впервые Q016 получает **независимый primary архив** для центрального факта, который ранее был только в Detwiler compilation:
- Дата `Jan 07, 2021` + `50:43` + тайтл `Interview with John MacArthur` теперь **primary-pinned** без ссылки на adversarial source.
- Хронология `Dec 17 2020 Ep30 → Jan 07 2021 Ep31 → Jan 14 2021 Ep32` доказывает, что `Jan 07` был реальным релизом, не поздней переэтикеткой.
- Не доказывает: текст email `will be sitting down / live edition / refresh for live event` и точные `a few weeks ago / early October` replies — они остаются в Detwiler reproduction без независимого archive-pin. `live` defence (platform premiere) и `few weeks` inaccuracy остаются как в `2021_MACARTHUR_LIVE_EPISODE.md`: `PROMOTIONAL_CLARITY_CONCERN / INTENT_UNPROVED`.

**Источник:** Wayback podcast page 20210121022916 + g3min.org homepage 20210104142628 + calendar 202010/202101.
**Фактически изучено:** `FULL_OBJECT_VERIFIED` для podcast list (3 episodes + dates/durations), `PARTIAL_OBJECT` для homepage context.
**Результат:** **PARTIALLY_VERIFIED → ARCHIVE_PINNED for date/title/duration; REMAINS ARCHIVE_HOLD for promotion wording/chronology wording.** Не меняет финальный вердикт `INTENT_UNPROVED`, но даёт точный локатор для цитирования.
**Новизна:** `OPEN_QUESTIONS Q016` требовал `original G3 email, archived FB/X posts, Buice Oct post, Jan 07 replies, podcast metadata`. Теперь 1 из 8 (podcast metadata) закрыт primary-архивом; остальные 7 остаются HOLD.
**Кому:** Agent №1 (идеология/хронология) + Agent №2 (MEDIA_LEDGER Q016) — для upgrade Q016 source list.
**Ограничения:** `A2` (official G3 site via Wayback), `FULL_OBJECT_VERIFIED` для date/duration, `PARTIAL_OBJECT` для promotion text, `PUBLICATION_HOLD` для intent.

### DISCOVERY-2026-11-20-N01 — Press delta 42 → 59, storefront continuity

**DISCOVERY-ID:** `SCOUT-N01` (уточнение Q020 / `ASSET_TRANSFER_AND_RIGHTS.md` §4)
**Что найдено:**

- **Historical G3 snapshot `https://web.archive.org/web/20241222011715/https://shop.g3min.org/collections/g3-press-books` (23 captures 22 Dec 2024–19 May 2026):**
  - Menu: `G3 Press Books / Living Heritage Books / Downloads / DVDs / Christian Living ...` + `G3 Ministries / Blog / Events / Plus`
  - Banner: `15% discount for 25+ / Read all G3 Press Books on G3 Plus! → plus.g3min.org`
  - **Filter: `42 products`** — first page выписка:
    `“Is That You, Lord?” Gilley $18`, `40 Days in Philippians Cole $19`, `A Biblical Case for Cessationism Pennington $24`, `A Biblical Theology of Climate Change Harrison/Walker $18→$13.50 sale`, `A Conservative Christian Declaration Aniol $10`, `As Far As the Curse Is Found Attebury $15`, `Cessationist Study Series G3 Ministries $14`, `Citizens & Exiles Aniol $21`, `Dividing the Faithful Schrock $21`, `Galatians Thornton $13`, `Gloria Deo Journal Vol 3 2024 $10`, `How We May Read Scriptures Watson $10`, `Hymns & Carols Advent $11`, `Hymns for Troubled Times Anderson $17`, `Let Men Be Free Crawford $22`, `Marriage to Difficult Man Dodd $25`, `Measuring the Music Makujina $34` … (42 total, sale on Climate Change)
  - Identical on `20250118173410` — pre-wind-down stability.

- **Live Lumena now `https://lumenapress.com/collections/lumena-press-books` 20.11.2026:**
  - Menu: `Lumena Press Books / Living Heritage Books / Downloads / DVDs ...` + `Lumena Ministries / Lumena Media`
  - Banner: `15% discount 25+ / Read all Lumena Press Books on Lumena Media! → lumenamedia.com` + Discount Ninja 50% Lost Queen/Rembrandt/Van Gogh/Homer
  - **Filter: `59 products`** — paginated 1/2/3:
    - p1 (20 titles): `Aiming to Transform Johnson $21` (new), `Sow Spurgeon $26`, `Progress of Doctrine Talbert $21`, `A Qualified Man Tanner $19`, `One Spurgeon $26`, `Ten Laws de Bruyn $14`, `Be Still My Soul McNeely $20`, `Promise of Messiah Jago $16`, `Compassionate Calvinism Cole $26`, `Introducing Apostolic Fathers Varner $21`, `Ancient Truths Aniol $28`, `Living Truth Aniol $18`, `Gentleness Norman $15`, `Resting in Sovereign Grace Banks $18`, `By Faith Spurgeon $26`, `Tune My Heart Aniol $32`, `Holy War Bunyan $21`, `Out of Formation Gilley $21`, `Bring Them to Church Mooney $17`, `Word of God & Fellowship Worley $21` …
    - p2 (20 titles): `Why Do Bad Things Happen Potter $13`, `Unhinged No More Skepple $19`, `Three Forms Unity Baptists $29`, `Strange Lyre de Bruyn $13`, `Psalms and Hymns Pew $25 / Spiral $24 / Limited $19`, `Daily Worship Book Howard $16`, `As Far As the Curse Is Found Attebury $15` (retained), `Theonomy Waldron/Hicks $19` (retained), `Is That You Lord Gilley $15` (retained, price $18→$15), `Holy Spirit God of Order Aniol $16`, `Hymns for Troubled Times Anderson $17` (retained, $17→$15), etc.
    - p3 (19 titles): `Measuring the Music Makujina $25` (retained, $34→$25), `Sound Worship Aniol $13`, `Hymns to Living God Spiral $21`
  - Product footer: `Lumena Press socials → instagram g3conference / facebook G3Conference / youtube / X g3conference` — handles не сменены.
  - `lumenamedia.com` Treefort `a963f031…` + Shop→`g3min.org/shop` (wave6), `lumenapress.com/products/aiming-to-transform…` vendor `Jeffrey Johnson`.

**Почему важно для Q020/Q006:**
- **Число:** `42 (Dec 2024 G3) → 59 (Nov 2026 Lumena)` = **+17 net** — рост за счёт Spurgeon reprints (`Sow/One/By Faith/John Ploughman`), Talbert/Varner/Jago, new Lumena imprint (`Aiming to Transform`), при удержании ядра Aniol (`Conservative Declaration → Ancient Truths/Living Truth/Citizens & Exiles`), Waldron `Theonomy`, Anderson `Hymns`, Attebury `Curse`, Makujina `Measuring Music`, Gilley `Is That You Lord`.
- **Доказывает:** operational continuity — Shopify коллекция переехала с `shop.g3min.org` на `lumenapress.com` с тем же шаблоном меню, скидкой 15% 25+, тем же набором Living Heritage/Discounted/Downloads.
- **Не доказывает:** кто владеет правами/инвентарём/роялти. Рост 42→59 может быть как transfer + new acquisitions, так и selective re-listing. Нельзя писать `Lumena acquired entire G3 Press catalog` — title-level rights остаются `TITLE-BY-TITLE PARTIAL CLOSURE` per `OPEN_QUESTIONS Q020`. Пример: `A Biblical Theology of Climate Change` Harrison/Walker $13.50 sale в Dec 2024 — отсутствует в Lumena p1/p2 (проверено) → rights possibly returned to authors, не transferred.
- Исправляет `ASSET_TRANSFER_AND_RIGHTS.md` draft фразу `G3 Press had expanded to more than 50 titles` — точнее `42 G3 Press Books in Shopify taxonomy Dec 2024; Lumena Press Books 59 Nov 2026 (taxonomy may differ from print claims)`.

**Источник:** Wayback shop.g3min.org/collections/g3-press-books 20241222 (42) + live lumenapress.com/collections/lumena-press-books p1/p2/p3 20.11.2026 (59) + product pages.
**Фактически изучено:** `FULL_OBJECT_VERIFIED` для counts (42/59) и p1/p2/p3 product names/prices, `PARTIAL_OBJECT` для cross-price delta.
**Результат:** **STORE_COUNT_VERIFIED / RIGHTS_HOLD_RETAINED** — точный дельта-число зафиксировано, юридическая передача не установлена.
**Новизна:** Ранее был только snapshot `shop.g3min.org` reachability (Sep 08) без count; теперь — exact pre/post count + title examples для forensics.
**Кому:** Agent №3 (финансы/активы/Q020) — для `ASSET_TRANSFER_FORENSICS.md` + `FINANCES.md` title-level appendix.
**Ограничения:** `A2` (shop via Wayback) / `A3` (Lumena official) + `C` (Shopify platform state), `FULL_OBJECT_VERIFIED` для counts, `COARSE_LOCATOR_ONLY` для full-title rights, `PUBLICATION_HOLD` для ownership.

---

## 3. Отчёт по волне 7

### Три наиболее ценные находки
1. **Wayback podcast Jan 07 2021 50:43 pinned** — первый независимый primary-объект для Q016, закрывает 1 из 8 required acquisitions.
2. **G3 Press 42 → Lumena Press 59 delta** — точный pre/post count с ценой и retention list (Atebury/Theonomy/Makujina/Anderson/Gilley retained, Harrison/Walker sale gone).
3. **Homepage Jan 04 2021 context** — `Do Black Lives Matter? Dec 28 2020` + `Will You Read Bible With Me Dec 29 2020` показывают, что G3 уже в Dec 2020 публиковал social-justice-adjacent + Bible-reading promo рядом с podcast, не только `Worship/Christ` conference.

### Главная неожиданность
**Podcast list хранит MacArthur как рядовой Episode 31 между Virgil Walker S2 premiere (Dec 17) и Spurgeon Susie (Jan 14) — без отдельного `live event` баннера в archive capture Jan 21.** Ожидался promo текст `live edition / refresh for live event` в том же snapshot; факт: Wayback Jan 21 показывает только list с 50:43, не email/FB promo. Promotion wording остаётся только в Detwiler reproduction — archive_gap подтверждён.

### Документы прочитаны / записи
**FULL:** Wayback podcast 20210121 (Ep31/32/30 list + durations), shop.g3min.org 20241222 (42 products header), lumenapress p1/p2/p3 20.11.2026 (59 products). **PARTIAL:** g3min homepage 20210104 (event list + trending). **Прослушано:** 0.

### Передано агентам
- **№3:** N01 (42→59 Press delta) для `ASSET_TRANSFER_FORENSICS` Q020 — exact counts + retained/new examples.
- **№2 / Media:** M01 (MacArthur date pinned) для `MEDIA_LEDGER` Q016 — upgrade source to A2 via Wayback.
- **№1:** M01 context для `IDEOLOGY_AND_COALITION` Dec 2020 social-justice proximity.

### Замечания
Q013 quantification остаётся `DATASET_REQUIRED` — wave7 не пытается проценты; даёт только platform-count как пример будущей census методики (content universe D).

### Как изменился корпус и читательский текст
Канон не переписан. Candidate draft (HOLD):
> *G3 Podcast Episode 31 — Interview with John MacArthur — published Jan 07, 2021 (50:43) per contemporaneous Wayback capture of g3min.org/podcast Jan 21 2021; list position between Dec 17 2020 Virgil Walker and Jan 14 2021 Spurgeon. Promotional `live edition` wording remains attested only via secondary reproduction, not via independent archive — intent unverified. G3 Press Shopify taxonomy held 42 G3 Press Books in Dec 2024 capture; Lumena Press Books lists 59 products Nov 2026 under same Shopify template (15% 25+), retaining titles such as Aniol Ancient Truths/Living Truth, Waldron Theonomy, Anderson Hymns, Attebury Curse and Makujina Measuring Music while adding new Spurgeon reprints — storefront counts document platform migration, not legal assignment of rights.*

### Следующий приоритет
1. P0 — GA BusinessInformation/officers — остаётся `ACCESS_HOLD` до authorized filing body; no new GA attempt until route changes.
2. P1 — Lumena Press p2/p3 price diffs vs G3 Dec 2024 exact cross-walk for individual rights-return candidates (Harrison/Walker Climate Change sale as test case) — 1 address pass.

---

## 4. Безопасность

HOLD не сняты; DRM/403 не обходились; ветки не правились.

## 5. Локаторы

| Объект | Локатор |
|---|---|
| MacArthur ep date | `https://web.archive.org/web/20210121022916/https://g3min.org/podcast/` Ep31 Jan 07 2021 50:43 |
| g3min Jan 04 2021 | `https://web.archive.org/web/20210104142628/https://g3min.org/` G3 2021 Christ + Trending Walker Dec 28 |
| G3 Press 42 | `https://web.archive.org/web/20241222011715/https://shop.g3min.org/collections/g3-press-books` 42 products |
| Lumena 59 | `https://lumenapress.com/collections/lumena-press-books` 59 products p1/p2/p3 20.11.2026 |
| Lumena vendor | `https://lumenapress.com/products/aiming-to-transform-experiential-expository-preaching` Johnson |
| shop→Lumena | `https://shop.g3min.org/` renders Lumena Press Shopify 20.11.2026 |

*Подпись:* Agent №4 SCOUT
