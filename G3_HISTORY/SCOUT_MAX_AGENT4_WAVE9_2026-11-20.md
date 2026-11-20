# G3 MAX — Агент №4 (СКАУТ) — Волна 9

**Дата:** 2026-11-20 (ночь, финал итераций)
**Агент:** №4
**Ветка:** `arena/963be9bc-research` — волны 1–8 `26231a3`, без правки чужих веток
**Статус:** `RESEARCH_DRAFT / PUBLICATION_HOLD`
**Вход:** waves 1–8 + `OPEN_QUESTIONS` Q016/Q013/Q019 + `IDEOLOGY_CONTENT_CODING_PROTOCOL.md` + Wayback checks 20.11.2026 (podcast 20210121 pinned, FB Jan 04 / Jan 20 gap, Lumena home/about)

---

## 1. Две выбранные гипотезы волны 9

### Гипотеза Q — P1: Q016 promotion wording — исчерпать оставшийся archive-gap после 2 доп-проверок, зафиксировать STOP

**Вопрос:** Остаётся ли wording `will be sitting down / live edition / refresh for live event` и `a few weeks ago → early October` только в Detwiler reproduction после прямой проверки календарей Facebook G3Conference Jan 07 и g3min.org/podcast Jan 07?
**Ожидаемый результат:** explicit `ARCHIVE_HOLD_RETAINED after 2 addressable calendar checks` + STOP_DISCOVERY для Q016 wording.
**STOP:** после FB Jan 04→Jan 20 gap + podcast Jan 21 list (без promo-banner) — STOP.

### Гипотеза R — P2: Q013 pilot census — дать первую denominator-таблицу для ideology-кодирования без процентов

**Вопрос:** Можно ли построить reproducible conference-session denominator `A. National conference sessions` по официальным archive labels + GNL delivered counts 2013–2023 как базу для будущего `IDEOLOGY_CONTENT_CODING_PROTOCOL`, не делая тренд-вывода?
**Ожидаемый результат:** raw-n table 2013–2023 с source-quality flag, не проценты.
**STOP:** после 1 census-pass по theme sequence + GNL counts — STOP.

---

## 2. Пакет открытий

### DISCOVERY-2026-11-20-Q01 — Q016 promotion wording — archive gap подтверждён

**DISCOVERY-ID:** `SCOUT-Q01` (closure attempt Q016 `2021_MACARTHUR_LIVE_EPISODE.md`)

**Что проверено (2 addressable passes как обещано):**
1. `https://web.archive.org/web/20210107000000*/https://www.facebook.com/G3Conference` → calendar 48 captures 20 Nov 2017–09 Sep 2025: **Jan 04 2021** (16:30 Dec 22 2020 next = Jan 04 14:27) → **Jan 20 2021 23:24** — **нет capture Jan 06–07 2021**. Nearest Jan 04 shows community page `16.290 Me gusta / 17.515 siguen / Creada 02 abril 2012 / www.G3Conference.com` — без поста. Это подтверждает transport-gap для FB promotion wording, не refutation.
2. `https://web.archive.org/web/20210121022916/https://g3min.org/podcast/` re-read + `20210104142628 https://g3min.org/` homepage: podcast list Jan 21 shows `Ep31 Jan 07 2021 50:43` **без `live edition` banner**; homepage Jan 04 shows `G3 2021 Christ Sep 30–Oct 02` + `Trending: Walker Dec 28 / Buice Dec 29` — без MacArthur promo. `g3min.org/podcast` calendar confirms first capture after Jan 07 is Jan 21 — Jan 07 itself not captured.

**Почему важно:** После wave7 pin для `Jan 07 date/duration`, это — **вторая половина Q016**: promotion wording остаётся `PARTIALLY_VERIFIED / ARCHIVE_HOLD` с exact checked routes, а не vague `not found`. Две календарные дыры записаны, третий проход без новой гипотезы (Twitter API, email provider) был бы Tier 4 (repetition).

**Источник:** Wayback FB calendar Jan 07 gap + podcast page Jan 21 + homepage Jan 04.
**Фактически изучено:** `PARTIAL_OBJECT` — calendars read, post bodies not retrievable via fetch_page.
**Результат:** **PROMOTION_WORDING_ARCHIVE_HOLD_RETAINED — STOP_DISCOVERY for this route.** `live` semantics defence + `few weeks` inaccuracy остаются `INTENT_UNPROVED` per master file.
**Новизна:** Q016 теперь имеет split-state: `date/duration ARCHIVE_PINNED (M01)` + `wording ARCHIVE_HOLD (Q01)` — честная атрибуция вместо `all unverified`.
**Кому:** Agent №2 (MEDIA_LEDGER) + owner PR #582 — для Q016 status split.
**Ограничения:** `B1/C` (Detwiler reproduction only for wording), `COARSE_LOCATOR_ONLY`, `PUBLICATION_HOLD` для `lied/cover-up`.

### DISCOVERY-2026-11-20-R01 — Q013 pilot conference denominator (без квантификации тренда)

**DISCOVERY-ID:** `SCOUT-R01` (first deliverable for `IDEOLOGY_CONTENT_CODING_PROTOCOL.md` Q013)

**Что построено — Universe A `National conference sessions` pilot census (content universe A, not articles/podcasts/products):**

| Year | Official theme (CONFERENCE_HISTORY) | Official archive anchor | GNL delivered count (verified) | GNL sample titles (evidence of ecclesial focus) |
|---|---|---|---|---|
| 2013 | The Gospel: Message and Mission | `g3min.org/archives/?conf=2013` | 9 episodes (GNL 2013) | Washer, Whitney, Baucham, Beeke, Lawson, Miller, Challies — gospel/mission |
| 2014 | The Doctrine of the Church / Church Biblical Perspective | `g3min.org/2014-g3-conference` + Founders ad Jan 23–25 Pray's Mill | 11 episodes (GNL 2014) | SBTS cross-check `Church: Biblical Perspective` contemporary |
| 2015 | The Bible is the Word of God | `g3min.org/2015-g3-conference-review` | ≥10 (GNL 2015 Lawson 1:11 Washer 1:02 White 53:48 Challies 53:54) | Inerrancy, God-Breathed Word, Two Books |
| 2016 | Trinity | `g3min.org/g3-2016` announcement + archive | 8 episodes (GNL 2016 Ware 1:06 White 55:15 Lawson 1:05) | Trinity in Worship/Salvation/Qur'an apologetics |
| 2017 | Reformation 500 | `g3min.org/archives` `Reformation 500` label | 18 episodes (GNL 2017 Carson x2 58:27+48:42 Washer/Baucham/Mbewe) | Soli Deo Gloria, Reformation Was Recovery, Atonement vs Rome |
| 2018 | Knowing God / Discipleship | archive + promo `Knowing God` | — (GNL not re-fetched) | — |
| 2019 | The Mission of God (+ Social Justice preconference) | `archives/?conf=2019` + G3 Study `based on 2019 sermons` | 17 episodes (GNL 2019 thumbnail) | missions/church planting — preconference separate per protocol §7 |
| 2020 | Worship | `archives/?conf=worship` + Challies Jan 20 report | 14 episodes (GNL 2020 MacArthur 57:46 etc) | Worship + MacArthur/Washer/Baucham Q&A |
| 2021 | Christ | `archives/christ` + FY2021 6,500 claim | — | Christology + BLT session — demonstrates culture dispute inside theology |
| 2023 | Sovereignty of God ( + political-theology panel) | `library-resources/the-sovereignty-of-god-study` + pre-conf `White/Sstrachan/Aniol debate` | 8.2k participant not sessions | Main theme theology, panel = Christian Nationalism/theonomy/postmill |

**Почему важно для Q013:** Это — **первый frozen denominator row set** для content universe A, требуемый `IDEOLOGY_CONTENT_CODING_PROTOCOL` §7 ("full census of surviving official conference archive entries"). Он:
- различает `main sessions vs breakout/preconference` (2019 Social Justice preconference не смешивается с Mission of God main — протокольное правило);
- даёт `total identifiable sessions` per year для будущей кодировки 12 категорий (`GOSPEL_CHRIST_SALVATION`, `TRINITY_DOCTRINE_OF_GOD`, `SOCIAL_JUSTICE_CRT_RACE`, `CHRISTIAN_NATIONALISM_THEONOMY` etc.) с первичным топиком §4;
- пока **не даёт проценты** — pilot anchors §9 уже зафиксированы (early political articles 2012/2015/2016), но `No quantitative ideological percentage may be published until corpus and coding protocol are complete` — соблюдено.

**Источник:** `CONFERENCE_HISTORY.md` Phase 1–4 themes + official archive URLs + GNL title/duration live reads waves 1,5,6,7 + FY2021 6,500 + Prata 8,200 + pre-conf 2023 schedule.
**Фактически изучено:** `PARTIAL_OBJECT` — counts from GNL thumbnails + theme labels; full session catalog per year not yet extracted row-by-row.
**Результат:** **PILOT_CENSUS_TABLE_DELIVERED — DATASET_REQUIRED retained for articles/podcasts (universes B/C), but universe A denominator now starter-kit for coders.**
**Новизна:** Ранее Q013 был `DATASET_REQUIRED` без единой таблицы; теперь есть reproducible starter с exact locators для A-universe.
**Кому:** Agent №1 (IDEOLOGY_AND_COALITION) — для `IDEOLOGY_CONTENT_CODING_PROTOCOL` implementation + editor guardrail `increasingly central` still blocked until B/C census.
**Ограничения:** `A2/A3` for official themes + `A2` GNL counts, `PARTIAL_OBJECT`, `COARSE_LOCATOR_ONLY`, `PRIVATE_STUDY_ONLY`, `PUBLICATION_HOLD` для любого тренд-утверждения.

---

## 3. Отчёт по волне 9

### Три наиболее ценные находки
1. **Q016 split-state pinned:** date/duration `ARCHIVE_PINNED` (wave7) + promotion wording `ARCHIVE_HOLD after FB Jan 04→20 gap + podcast Jan 21 no-banner` — честный источник-сплит.
2. **Q013 pilot census A-universe 2013–2023:** 9/11/≥10/8/18/17/14 episodes mapped to official themes, с явным отделением 2019 preconference — первый denominator для coding protocol.
3. **Lumena final snapshot stability:** `lumenaministries.com` 20.11.2026 `Preserve/Equip/Pass on` + Psalm 43:3, без упоминания G3+ closing terms — reinforces platform≠ownership guardrail для FINAL H0LD.

### Главная неожиданность
**Facebook G3Conference имеет непрерывную страницу с 2012 (Creada 02 abril 2012) и даже Jan 04 2021 snapshot жив, но именно Jan 07 2021 — дыра.** Ожидался хотя бы `live edition` promo capture; факт: ближайший Jan 20 capture через 13 дней — FB archive transport-gap, не опровержение.

### Документы прочитаны / записи
**FULL:** FB calendar Jan 07 gap + G3Conference creation date, Lumena home Preserve/Equip/Pass on. **PARTIAL:** podcast Jan 21 re-read + census table 10 rows. **Прослушано:** 0.

### Передано агентам
- **№1:** R01 census table для `IDEOLOGY_AND_COALITION.md` Q013 stepwise coding — A-universe ready, B/C pending.
- **№2:** Q01 split-state для `MEDIA_LEDGER` Q016 — wording hold retained.
- **№3:** —

### Замечания
Седьмая волна (42→59) + восьмая (Climate disappearance) + девятая (census pilot) вместе дают требуемый `QUANTIFICATION_STILL_REQUIRED → DATASET_BUILDING` transition без нарушения HOLD.

### Как изменился корпус и читательский текст
Канон не переписан. Candidate Q016 split draft (HOLD):
> *Podcast Episode 31 with John MacArthur published Jan 07, 2021, 50:43 — pinned via contemporaneous Wayback g3min.org/podcast Jan 21, 2021; Facebook G3Conference page (est. Apr 02, 2012) shows no capture Jan 06–07, with nearest Jan 04 and Jan 20 — promotional `live edition`/`a few weeks` wording remains attested only via secondary reproduction.*
Census draft (HOLD):
> *National conference main themes 2013 Gospel → 2014 Church → 2015 Bible → 2016 Trinity → 2017 Reformation 500 → 2018 Knowing God → 2019 Mission of God (with separate Social Justice preconference) → 2020 Worship → 2021 Christ → 2023 Sovereignty of God — pilot denominator 9/11/≥10/8/18/17/14 sessions per GNL-official cross-check; no ideological share published pending article/podcast coding.*

### Следующий приоритет
1. P1 — завершить Q013 B-universe (dated article sample per IDEOLOGY protocol §8) — equal-n per year, deterministic interval, not search relevance.
2. P2 — Q016 email source (original G3 Jan 07 2021 email) — только если появится mail-archive route; FB/X wording остаётся HOLD.

---

## 4. Безопасность

HOLD не сняты; DRM/403 не обходились; ветки не правились.

## 5. Локаторы

| Объект | Локатор |
|---|---|
| Q016 date pinned | `https://web.archive.org/web/20210121022916/https://g3min.org/podcast/` Ep31 Jan 07 2021 50:43 |
| Q016 FB gap | `https://web.archive.org/web/20210107000000*/https://www.facebook.com/G3Conference` Jan 04→Jan 20 gap, Creada 02 abr 2012 |
| Q016 home context | `https://web.archive.org/web/20210104142628/https://g3min.org/` Christ Sep 30–Oct 02 + Trending Walker/Buice Dec 2020 |
| Q013 census | `g3min.org/archives/?conf=2013` + 2014 + 2015 review + g3-2016 + GNL 2013/14/15/16/17/19/20 counts |
| Lumena mission | `https://lumenaministries.com/` Preserve/Equip/Pass on Psalm 43:3 |
| Final platform Q006 | `Q005_Q006_GEORGIA_FILING_DELTA_2026-11-15.md` + OpenCorporates 19085916 Minga / Lumena Press 59 |

*Подпись:* Agent №4 SCOUT
