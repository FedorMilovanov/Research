# G3 MAX — Агент №4 (СКАУТ) — Волна 8

**Дата:** 2026-11-20 (финал ночи)
**Агент:** №4
**Ветка:** `arena/963be9bc-research` — волны 1–7 `ab38bff`, без правки чужих веток
**Статус:** `RESEARCH_DRAFT / PUBLICATION_HOLD`
**Вход:** wave7 (MacArthur 07.01.2021 pinned + 42→59 Press delta), `Q005_Q006_DELTA` §1.7-1.8, OpenCorporates renderer, Wayback `shop.g3min.org` Climate Change product + Lumena search 0 results, Lumena Press p3 + Treefort vendor (wave6/7)

---

## 1. Две выбранные гипотезы волны 8

### Гипотеза O — P0-дополнение: подтверждает ли вторичный рендерер смену агента и исчезновение титула как кейс title-by-title

**Вопрос:** Совпадает ли OpenCorporates для 19085916 с GA-индексом по `Active/Compliance + Laramie Minga 502 Ramah Dr Palmetto` против `Scott Aniol` на 08.09, и отсутствует ли `A Biblical Theology of Climate Change Harrison/Walker` на Lumena (0 results) при наличии на G3 23.02.2025 как пример не-мигрированного титула?
**Ожидаемый результат:** discovery-only corroboration агента + точный кейс disappearance, не upgrade ownership.
**STOP:** после 1 OpenCorporates + 1 historical product + 1 Lumena search — STOP.

### Гипотеза P — P1-важная: Lumena Press p3 + Treefort vendor как финальный platform snapshot

**Вопрос:** Что на p3 Lumena Press (последние 3 тайтла: Makujina $25, Aniol $13, Hymns $21) завершает инвентаризацию 59, и подтверждает ли Treefort header постоянство vendor-слоя?
**Ожидаемый результат:** полный 59-closed list + FINAL_PLATFORM_HOLD формулировка для editor.
**STOP:** после p3 chunk — STOP.

---

## 2. Пакет открытий

### DISCOVERY-2026-11-20-O01 — GA agent change (renderer) + Climate Change disappearance

**DISCOVERY-ID:** `SCOUT-O01` (уточнение Q005 G3-S144 / Q020 title-by-title)

**OpenCorporates `https://opencorporates.com/companies/us_ga/19085916` (renderer, не primary):**
```
Lumena Ministries, Inc. [nonprofit]
Company Number 19085916
Status Active/Compliance
Company Type Domestic Nonprofit Corporation
Jurisdiction Georgia (US)
Registered Address 502 Ramah Dr, Palmetto, 30268, GA
Agent Name Laramie Minga
Agent Address 502 Ramah Dr, Palmetto, GA 30268
Recent filings: 5 Nov 2026 Amended Annual Registration / 30 Oct 2026 Amended Annual / 28 Oct 2026 Business Amendment Name Change / 14 May 2025 Annual Registration / 10 Jan 2022 Annual / 30 Mar 2020 / 16 Jul 2019 / 6 Jun 2019 Formation
```
Сравнимо с: `G3-S001` official Sep 08 2026 `Active/Compliance` с агентом `Scott Aniol`, и `G3-S144` index 15 Nov 2026 (тот же 8-row history) без статус-поля. OpenCorporates повторяет GA history точно, но добавляет **адрес + статус-поле после Oct 30** — lead что статус остался `Active/Compliance` и агент сменился на Minga (совпадает с Lumena About `President Laramie Minga ex-Director Operations G3` wave4). **Нельзя публиковать как primary:** renderer disclaimer `not primary source, company registry should be referred`. Publication wording: `secondary renderer shows Active/Compliance and agent Laramie Minga at Winston/Palmetto address; official BusinessInformation detail still not re-read`.

**Climate Change кейс:**
- **G3 historical:** `https://web.archive.org/web/20250223092134/https://shop.g3min.org/collections/g3-press-books/products/a-biblical-theology-of-climate-change` (1 capture Feb 23 2025, plus Dec 22 2024 collection 42):
  - Title `A Biblical Theology of Climate Change — Darrell Harrison, Virgil Walker $18.00` (sale $13.50 Dec 2024)
  - 139 pages, 9781959908333, `G3 Press`
  - Bio: *Virgil Walker is Vice President of Ministry Relations for G3 Ministries ... co-host Just Thinking Podcast*
  - Description: climate justice as false gospel, stewardship vs neo-paganism
- **Lumena now:** `https://lumenapress.com/search?q=climate+change` → `Search: 0 results found for "climate change"` (live 20.11.2026, same Shopify template, Discount Ninja)
- **Context:** Harrison/Walker — core G3-aligned authors (Walker VP Ministry Relations, Harrison pastor Redeemer Bible Gilbert), title directly from G3 Press taxonomy, not third-party distributor.

**Почему важно:** Это первый **чистый disappearance** между последним G3 snapshot (Feb 2025) и живым Lumena (Nov 2026) для тайтла из того же идеологического кластера (culture-war), что и wave7 retained `Strange Lyre de Bruyn $13`, `Theonomy Waldron $19`, `Let Men Be Free Crawford $22`. Доказывает, что **миграция 42→59 не была bulk transfer** — selective rights return / inventory split. Нельзя экстраполировать на весь каталог, но нельзя и писать `all G3 Press titles now at Lumena`.

**Источник:** OpenCorporates 19085916 + Wayback Climate Change product Feb 23 2025 + Lumena search 0 results 20.11.2026.
**Фактически изучено:** `PARTIAL_OBJECT` — renderer readback + single product + search result; GA detail body still `ACCESS_HOLD`.
**Результат:** **AGENT_CHANGE_LEAD_VERIFIED via renderer (not primary) / SINGLE_TITLE_DISAPPEARANCE_VERIFIED** — reinforces `TITLE-BY-TITLE PARTIAL CLOSURE`.
**Новизна:** Ранее Q020 кейс был Jenkins `Word Matters` (external republication); теперь — Harrison/Walker `Climate Change` disappearance на Lumena — противоположный вектор той же piecemeal модели.
**Кому:** Agent №3 (Q020) — для `ASSET_TRANSFER_FORENSICS.md` §7 + `CLAIMS_LEDGER` G3-C064/C065 guardrail update.
**Ограничения:** `C` (renderer, Shopify search state), `PARTIAL_OBJECT`, `COARSE_LOCATOR_ONLY`, `DISCOVERY_LEAD_ONLY` для агента, `PUBLICATION_HOLD`.

### DISCOVERY-2026-11-20-P01 — Lumena Press 59 closed + FINAL PLATFORM STATEMENT

**DISCOVERY-ID:** `SCOUT-P01` (завершение wave6/7 59-inventory)
**Что найдено — `https://lumenapress.com/collections/lumena-press-books?page=3` live 20.11.2026 (final page):**
```
59 products total (3 pages)
p3 final 3:
- Measuring the Music — John Makujina $25.00 (was $34.00 Dec 2024)
- Sound Worship: Guide to Making Musical Choices in Noisy World — Scott Aniol $13.00
- Hymns to the Living God | Spiral Edition — Lumena Press $21.00
```
Plus p2 carry `Theonomy Old and New $19`, `Strange Lyre $13` etc. (wave7). Shopify header/footer identical to Dec 2024 G3: `15% discount 25+` + `Read all … on Lumena Media / G3 Plus` swap + socials `g3conference` handles retained.

**Почему важно:** Закрывает инвентаризацию — 59 не estimate, а **Shopify Filter count + 3-page enumeration**. Price deltas (`Makujina $34→$25`, `Gilley $18→$15`, `Climate $18/$13.50→absent`) дают точные строки для editor при описании миграции без изобретения `transfer`. Вместе с `lumenamedia.com` Treefort `a963f031` (wave6) даёт финальную платформу-формулу.

**Источник:** Lumena Press p3 live 20.11.2026 + p1/p2 wave7 + shop.g3min.org Dec 2024 42.
**Фактически изучено:** `FULL_OBJECT_VERIFIED` для p3 tail, `PARTIAL_OBJECT` для full cross-walk.
**Результат:** **59-PRODUCT INVENTORY CLOSED / PLATFORM_VERIFIED / OWNERSHIP_HOLD_RETAINED**
**Новизна:** wave6/7 имели 42→59 count и p1 примеры; теперь — explicit p3 tail, завершающий список.
**Кому:** Agent №3 (финансы/активы) + editor для FINAL_P0_HOLD_MATRIX Q006 annex.
**Ограничения:** `A3` (Lumena official storefront), `C` (Shopify count), `PUBLICATION_HOLD`.

---

## 3. Отчёт по волне 8

### Три наиболее ценные находки
1. **OpenCorporates Active/Compliance + Agent Laramie Minga 502 Ramah Dr** — первый статус-полевой lead после Oct 30, совпадает с Lumena President Minga; renderer, не primary, но closes loop между GA index и Lumena About.
2. **Climate Change Harrison/Walker $18 Feb 2025 → 0 results Nov 2026** — первый чистый disappearance кейс, доказывает selective, не bulk transfer.
3. **Lumena p3 tail Makujina/Sound Worship/Hymns Spiral** — 59 closed, price $34→$25 delta, Shopify template continuity final.

### Главная неожиданность
**G3 VP Ministry Relations title исчезает на преемнике: Virgil Walker (VP G3 Ministries) authored Climate Change is on G3 Press Feb 2025 but absent on Lumena.** Ожидалось, что ближайший к G3 leadership титул (Walker) будет приоритетно retained; факт: его нет в Lumena search, тогда как `Tanner Qualified Man $19` и `de Bruyn Ten Laws $14` retained — права автора/тематика важнее должности.

### Документы прочитаны / записи
**FULL:** OpenCorporates 19085916 entity block, Climate Change G3 product Feb 23 2025, Lumena search 0 results, Lumena p3 3 titles. **PARTIAL:** Dec 2024 42 collection header. **Прослушано:** 0.

### Передано агентам
- **№3:** O01 (agent lead + Climate disappearance) для `ASSET_TRANSFER_FORENSICS` Q006/Q020 title-by-title — главный кейс несBulk.
- **№1:** P01 (59 closed) для `CONFERENCE_HISTORY` не нужен, для `PRODUCT_HANDOFF` platform snapshot.
- **№2:** —

### Замечания
GA detail `BusinessInformation` остаётся `ACCESS_HOLD` до authorized raw payload; OpenCorporates не лифтит HOLD, только discovery lead. Q016 remains 1/8 pinned, Q013 still `DATASET_REQUIRED`.

### Как изменился корпус и читательский текст
Канон не переписан. Candidate FINAL PLATFORM draft (HOLD):
> *Georgia corporation Lumena Ministries, Inc. (f/k/a G3 Ministries for the Church, Inc., control 19085916) — name changed effective Oct 28 2026, two Amended Annual Registrations Oct 30 / Nov 05 2026 per GA filing history (8 rows, no dissolution row Nov 15). Official status field last primary-read Sep 08 Active/Compliance (Scott Aniol agent); secondary renderer shows Active/Compliance and agent Laramie Minga at Palmetto address post-Oct 30 (renderer only, not primary). Lumena public project led by ex-G3 Director of Operations Minga (2022 Media→2024 Operations→President) operates lumenapress.com (59 Lumena Press Books, 15% 25+, retaining 42-taxonomy core such as Aniol, Waldron Theonomy, Anderson, Attebury, Makujina $34→$25, Gilley, while adding Spurgeon reprints/Talbert/Jago) and lumenamedia.com on Treefort (a963f031). Shop.g3min.org Dec 22 2024 held 42 G3 Press Books; single-title test — A Biblical Theology of Climate Change (Harrison/Walker $18, 139pp, G3 Press Feb 23 2025) yields 0 results at Lumena Nov 2026 — documents selective platform migration, not proven bulk legal assignment of rights/inventory.*

### Следующий приоритет
1. P2 — остальной Q016 archive (original email `live edition` / `a few weeks ago` FB/X threads) — только если появится новый archive route; иначе HOLD.
2. P2 — полная Q013 conference census (official archive session count per year 2013–2023) — требует отдельного PASS без смешения с store counts.

---

## 4. Безопасность

HOLD не сняты; DRM/403 не обходились; ветки не правились.

## 5. Локаторы

| Объект | Локатор |
|---|---|
| OpenCorporates | `https://opencorporates.com/companies/us_ga/19085916` Lumena Active/Compliance Minga 502 Ramah Dr |
| Climate G3 | `https://web.archive.org/web/20250223092134/https://shop.g3min.org/collections/g3-press-books/products/a-biblical-theology-of-climate-change` Harrison/Walker $18 139pp |
| Climate absent Lumena | `https://lumenapress.com/search?q=climate+change` 0 results 20.11.2026 |
| GA 8 rows 20.11 | `https://ecorp.sos.ga.gov/BusinessSearch/BusinessFilings?businessId=2751672` 17370469–32269080 |
| Lumena 59 p3 | `https://lumenapress.com/collections/lumena-press-books?page=3` Makujina $25 / Aniol $13 / Hymns $21 |

*Подпись:* Agent №4 SCOUT
