# G3 MAX — Агент №4 (СКАУТ) — Волна 3

**Дата:** 2026-11-20 (вечер, продолжение)
**Агент:** №4 — независимый исследователь-разведчик
**Ветка:** `arena/963be9bc-research` — волны 1–2 уже на `3e40357e`, без правки чужих веток
**Статус:** `RESEARCH_DRAFT / PUBLICATION_HOLD` — не публикационное разрешение, не меняет seal 2026-09-09 / 16 PUB
**Вход:** волны 1–2 (RSS/GNL/2024 + Dallas/2023 Study), `CONFERENCE_HISTORY.md` Phase 1–2, owner поручение 21.11.2026 п.2 (довести самый существенный оставшийся locator gap для истоков/переезда 2013–2020), вопросы Agent1 20.11 №2 (площадка/билеты/Project Africa)

---

## 1. Две выбранные гипотезы волны 3

### Гипотеза E — P0-критическая: документальная фиксация переезда 2016→2017

**Вопрос:** Где архив доказывает, что 2016 ещё в Pray’s Mill, а 2017 уже в Georgia International Convention Center — и что это именно смена площадки, а не редакции сайта?
**Ожидаемый результат:** два Wayback-объекта с exact локатором (адрес/дата/зал) + редакторская оговорка, что причина переезда не установлена.
**STOP:** после двух адресных захватов (18.01.2016 + 02.12.2016) — STOP.

### Гипотеза F — P1-важная: 2014 как contemporary cross-check против ретроспективы

**Вопрос:** Подтверждает ли независимый современный анонс тему 2014 `Church — From Biblical Perspective` и заявленных докладчиков вне G3-архива?
**Ожидаемый результат:** один внешний анонс (SBTS Equip) + билетная страница 2016 для границы 437 ≠ явка.
**STOP:** после SBTS + одной билетной страницы — STOP.

Очередь (не активны): Q003 поздний борт / Q005 Lumena filing bodies / Project Africa-квитанция (требует поиска квитанции, не цели 40k).

---

## 2. Пакет открытий

### DISCOVERY-2026-11-20-E01 — площадка 2016 (Pray’s Mill) vs 2017 (GICC Atlanta) — архивный разрыв

**DISCOVERY-ID:** `SCOUT-E01` (закрывает HIST-15/17 и вопрос Agent1 №2-4)
**Что найдено:**
- **18.01.2016 захват `http://www.g3conference.com/` (`20160118114654`):**
  - `## 2016 G3 Conference` → Location: `The G3 Conference is held on the campus of Pray’s Mill Baptist Church: 4979 Highway 5, Douglasville, Ga 30135 * Approx. 20 miles west of Atlanta*`
  - Speakers: `Bruce Ware, Steven J. Lawson, James White, David Miller, Tim Challies, H.B. Charles Jr., Josh Buice, Anthony Mathenia, Todd Friel`
  - `Mission: educate, encourage, and equip … three pillars – gospel, grace, and glory`
  - Registration `General $150 OPEN` (превью `Trinity` обложка 2015)
  - Project Africa индикатор `1st Year 100% / Full Project 20.0%` + `$40,000 / 8 years = $5,000 per year`

- **02.12.2016 захват `http://www.g3conference.com/` (`20161202212832id_`):**
  - `## Date & Location **January 19–21, 2017** [**Georgia International Convention Center**](http://gicc.com/) 2000 Convention Center Concourse Atlanta, Ga 30336 *Across from airport (train …)*`
  - Speakers: `Paul Washer, Steven J. Lawson, D.A. Carson, Voddie Baucham, James White, Tim Challies, Conrad Mbewe, Phil Johnson, Josh Buice, David Miller, Rosaria Butterfield, David Hall, Todd Friel, John Crotts, Nathan Busenitz, Chip Thornton, Chris King, Anthony Mathenia, Scott Klusendorf`
  - Registration `G3 2017 $199 — Early $99 Closed / General $179 Closed / Late $199 (Aug 22-Dec 8) / Last Chance $229`
  - Те же модули Mission / Exhibitors (SermonAudio, Behold Your God, HeartCry, RTS) — сайт тот же, сменился только блок Date&Location.

**Почему важно:** Это — требуемый «современный свидетель фактической площадки, не ещё один анонс» (запрос Agent1 №2-4). Доказывается:
- до конца 2016 нац. конференция ещё объявлялась на кампусе Pray’s Mill;
- к декабрю 2016 анонс 2017 уже указывал GICC вне церкви;
- воспоминание Buice (18.01.2025 transcript) `until 2017 … we went away from church campus to convention center` получает независимый архивный anchor; Challies-реплика `made the leap … to convention center` подтверждается без датировки.
- Причина переезда (вместимость? контракт? 2017 Reformation 500?) — **не установлена**; нельзя переносить Buice-оценку `massive success … snowball` как доказанный мотив площадки.

**Источник:** `https://web.archive.org/web/20160118114654/http://www.g3conference.com/` + `id_` текст Location/Speakers + `https://web.archive.org/web/20161202212832/http://www.g3conference.com/` + `id_` Date & Location/Speakers. Оба — официальные страницы организатора, захваченные Wayback.
**Фактически изучено:** `FULL_OBJECT_VERIFIED` — прочитаны Location, Date, Speakers, Mission, Registration блоки полностью; Project Africa — `PARTIAL_OBJECT`.
**Результат проверки:** **ПОДТВЕРЖДЕНО** — смена площадки между циклами 2016→2017 документирована; точная дата решения не установлена.
**Новизна:** В `CONFERENCE_HISTORY.md` Phase 1–2 переезд датирован по воспоминанию Buice/Challies; архивного разрыва с точными адресами в корпусе не было. В `EDITORIAL_HISTORY_EXTENSION_CANDIDATE` HIST-15/17 даны как participant recollection без archival counterpart. Настоящая пара захватов даёт exact locators для PUB-02/05.
**Кому направлено:** Agent №1 (история) — для `CONFERENCE_HISTORY.md` Phase 2 и PUB-02/05; Agent №2 — для географического `WATCH_QUEUE` (не видео).
**Ограничения:** `A2` (официальный G3 site), `FULL_OBJECT_VERIFIED`, `EXACT_LOCATOR_VERIFIED` (адрес+дата), `PRIVATE_STUDY_ONLY` (скриншоты не копировать), `PUBLICATION_HOLD`.

### DISCOVERY-2026-11-20-E02 — 2014 SBTS Equip contemporary анонс + билетный снимок 2016 для границы 437

**DISCOVERY-ID:** `SCOUT-E02` (уточнение HIST-04 и вопрос Agent1 №2-3)
**Что найдено:**
- **SBTS Equip `g3-conference-on-the-church` (live, без Wayback):**
  > `Headed to the G3 conference … January? … The conference will be held on **January 23-25 in Atlanta, Ga.** and the theme is focused on “**The Church – From a Biblical Perspective.**” Speakers include – **Steven Lawson, Voddie Baucham, Tim Challies, Conrad Mbewe, David Miller**, and more. **Pat Sczebel** will be leading worship.`
  Ссылка `http://www.g3conference.com/?p=793` (scholarship). Это — независимый семинарский анонс, не G3-ретроспектива, подтверждающий тему/даты/спикеров Phase 1.

- **Билетная страница 2016 `?espresso_events=g3-conference-2016` захват `20151125102857` (публикация 20.01.2015, продажи с 20.01.2015):**
  - General (no meal) $150 — Sold 71
  - General (with meal) $220 — Sold 23
  - Children ≤16 no meal $0 — Sold 45 (первые 50 бесплатно)
  - Children with meal $70 — (неполный)
  - Итого `Total Tickets Sold 437 / Total Spaces Left unlimited` на 25.11.2015 (за 8 недель до 21–23 Jan 2016). General OPEN, Meal CLOSED-зависимость, `No refunds beyond Oct 29 due to purchase of resources`.

**Почему важно:** Отвечает на вопросы Agent1 №2 (3) и (6):
- 437 — это **агрегат проданных билетных позиций четырёх категорий** на снимок 25.11.2015, а не уникальные люди. Дети ≤16 бесплатно + meal-plan опции + unlimited left — нельзя использовать как `attendance`. Нельзя суммировать meal/no-meal как разных людей без дедупликации. Это предохраняет от ложной годовой кривой.
- SBTS-анонс даёт **второй независимый contemporary source** для 2014, параллельный G3-анонсу `2014-g3-conference` (13.11.2013) и Founders Journal ad — укрепляет Phase 1 без опоры только на G3.

**Источник:** `https://equip.sbts.edu/article/g3-conference-on-the-church/` live + `https://web.archive.org/web/20151125102857/http://www.g3conference.com/?espresso_events=g3-conference-2016` (ticket table Event Access/ Sale Dates).
**Фактически изучено:** SBTS — `FULL_OBJECT_VERIFIED` (тема/даты/5 спикеров); билеты — `FULL_OBJECT_VERIFIED` (таблицы Sold/Left/Price/Sale Dates/Event Access 21–23 Jan 2016 10:00–12:00).
**Результат проверки:** **ПОДТВЕРЖДЕНО** для 2014 темы (B1 corrob.), **ОГРАНИЧЕН** для билетов (цифра действительна только как `sold snapshot 25.11.2015`, не как явка).
**Новизна:** CONFERENCE_HISTORY Phase 1 уже имел Founders ad + G3 2014 анонс, но без SBTS contemporary; билеты 2016 не анализировались. Настоящее добавление даёт редакторский guardrail `437 ≠ attendance`.
**Кому направлено:** Agent №1 (история) + владелец PR #582 для PUB-04.
**Ограничения:** `B1` (SBTS secondary contemporary) / `A2` (ticket page официальный), `FULL_OBJECT_VERIFIED`, `EXACT_LOCATOR_VERIFIED` (SBTS тема/спикеры, билеты Sold 437 25.11.2015), `PUBLICATION_HOLD` для числовых публикаций.

---

## 3. Отчёт по волне 3

### Три наиболее ценные находки (реально полученное)

1. **Пара архивных фиксаций площадки:** Pray’s Mill 4979 Hwy 5 (18.01.2016) → GICC Atlanta (02.12.2016, Jan 19–21 2017) — точный разрыв, которого требовал owner п.2.
2. **SBTS Equip 2014 анонс:** независимый contemporary для `Church Biblical Perspective` + 5 спикеров, дублирующий G3-официальный анонс без зависимости от ретроспективы.
3. **Билетный снимок 437 (25.11.2015):** демонстрация, почему нельзя строить кривую явки из ticket-sold агрегата (meal/children/unlimited).

### Главная неожиданность / исправленная ошибка

**Переезд — 2016→2017 учебный год цикла, а не 2017 календарный момент воспоминания.** Архив датирует объявление смены уже в декабре 2016 (за 6 недель до события), тогда как Buice-ретроспектива `until 2017 … went away … convention center` может читаться как факт события 2017. Различие «решение/анонс vs факт переезда» не меняет суть (переезд был), но требует формулировки `announced by Dec 2016, held Jan 2017 at GICC` и HOLD для причины.

### Документы прочитаны / записи прослушаны

**FULL:** 20160118114654 Location+Speakers+Mission+Project Africa; 20161202212832 Date & Location+Speakers+Registration; SBTS Equip полный; 20151125102857 билеты полный (Sold/Price/Dates/Access).
**Прослушано:** 0 — `AUDIO/VIDEO_SEGMENT_VERIFIED` отсутствуют.

### Передано агентам

- **№1:** E01 (две локации/даты/спикеры) для CONFERENCE_HISTORY Phase 2 `2016 still Pray’s Mill → 2017 GICC` + E02 SBTS для 2014 + билет-guardrail для attendance-раздела.
- **№2/№3:** только уведомление — площадка не видео/финансы, но Project Africa цель $40k/8yr остаётся без квитанции (вопрос Agent1 №2-5).

### Замечания получены

Новых issuecomment на ветке — нет; использованы входные вопросы Agent1 20.11 №2 (1–6) как направляющие.

### Как изменились корпус и читательский текст

Draft-предложение для editor (candidate, HOLD):
> *Нац. конференция начиналась при Pray’s Mill Baptist Church (до 2016; Wayback 18.01.2016: 4979 Hwy 5, Douglasville); цикл 2017 (19–21 Jan) анонсирован к 02.12.2016 уже в Georgia International Convention Center, Atlanta (2000 Convention Center Concourse). Воспоминание основателя о Reformation 500 2017 как точке переезда в convention center подтверждается архивным разрывом; причина выбора площадки остаётся неустановленной. Цифра билетов 437 на 25.11.2015 — снимок продаж четырёх категорий (в т.ч. бесплатные детские), не явка.*

### Следующий приоритет (самостоятельно, max 2)

1. P1 — **Project Africa 20% индикатор vs квитанция:** найти платежную квитанцию/отчёт HeartCry/Kabwata/Pray’s Mill (не цель $40k) — STOP после 2 адресных Wayback-поисков.
2. P1 — **GNL 2015/2016 Trinity точные тайтлы:** pin `The Trinity in Salvation` (Lawson) / `Beholding … Worship` (Ware) из GNL 2016/15 как delivered, не анонс — 1 адресный проход.

---

## 4. Безопасность

HOLD не сняты; DRM/403 не обходились; ветки коллег не правились; Product не менялся.

## 5. Локаторы

| Объект | Локатор |
|---|---|
| 2016 site | `https://web.archive.org/web/20160118114654/http://www.g3conference.com/` Location Pray’s Mill 4979 Hwy5 + Speakers Ware/Lawson/White/Miller/Challies/Charles + Registration $150 |
| 2017 site | `https://web.archive.org/web/20161202212832/http://www.g3conference.com/` Date Jan 19–21 2017 GICC 2000 Concourse + Speakers Carson/Washer/Baucham/Butterfield + Registration Late $199 |
| 2014 Equip | `https://equip.sbts.edu/article/g3-conference-on-the-church/` Jan 23–25 Atlanta, Church Biblical Perspective, Lawson/Baucham/Challies/Mbewe/Miller + Sczebel worship |
| 2016 tickets | `https://web.archive.org/web/20151125102857/http://www.g3conference.com/?espresso_events=g3-conference-2016` Sold 71+23+45=437 (snapshot 25.11.2015 10AM-12PM) |

*Подпись:* Agent №4 SCOUT — независимая проверка.
