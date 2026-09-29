# Серия об отступничестве — архитектура публикации для gospod-bog.ru

**Статус:** PROPOSAL / DO NOT IMPLEMENT UNTIL RESEARCH CLOSES  
**Дата:** 2026-09-29  
**Product inspected:** `FedorMilovanov/gb-is-my-strength` `main`

## 1. Вывод после аудита текущего сайта

Сайт уже имеет **два уровня публикации**, идеально подходящие для этой темы:

1. отдельные длинные статьи в `articles/<slug>/index.html`;
2. отдельные **series hubs** верхнего уровня, которые собирают связанные статьи.

Это не теория. В текущем Product уже есть:

- `/hard-texts/` — `page.type = 'series'`, JSON-LD `CollectionPage`, `hasPart` со ссылками на статьи;
- `/nagornaya/seriya/` — серия Нагорной проповеди;
- `articles/index.html` выводит series banner рядом с отдельными article cards.

Поэтому для отступничества **не стоит помещать всё в один гигантский article HTML** и не стоит прятать всё только в Teletype. Тема уже по объёму естественно является серией.

## 2. Рекомендуемая публичная структура

### Series hub

**Route:** `/apostasy/`  
**Рабочее название:** «Отступничество и стойкость веры»  
**Тип:** `CollectionPage` / `page.type='series'`

Почему английский slug `apostasy`:

- короткий и стабильный;
- точно описывает corpus;
- не привязан к одной спорной формулировке статьи;
- соответствует уже существующему pattern коротких тематических routes (`/hard-texts/`).

Русский пользователь не видит slug как заголовок, поэтому reader-facing title остаётся полностью русским.

### Часть 1 — флагманская карта всей темы

**Route:** `/articles/otstuplenie-chto-govorit-bibliya/`

**Рабочий title:**  
«Отступничество: что Библия говорит о тех, кто был среди народа Божьего и отошёл»

**Роль:** не исчерпывать каждый hard case, а дать читателю категории и карту:

- что такое окончательная апостасия;
- временная вера;
- дары/служение без спасительной благодати;
- реальные заветные привилегии без saving union;
- тяжёлое падение истинного верующего;
- warning texts как средства постоянства;
- assurance/preservation.

Флагманская статья должна ссылаться на каждый deep dive и наоборот.

### Часть 2 — Иуда

**Route:** `/articles/iuda-izbrannyy-apostol-no-ne-spasennyy/`

Рабочий reader-facing title лучше не делать слишком рубленым. Возможные варианты после research:

- «Иуда Искариот: апостольское служение без спасительной веры»;
- «Иуда Искариот: избран в число Двенадцати — но был ли он спасён?»;
- «Иуда: как далеко можно зайти рядом со Христом без спасительной веры».

Предпочтение на данный момент: **«Иуда Искариот: апостольское служение без спасительной веры»** — самый точный и наименее сенсационный.

### Часть 3 — Евр. 6

**Route:** `/articles/evreyam-6-4-8-vkusili-i-otpali/`

**Title:**  
«Евреям 6:4–8: кто “вкусил небесного дара” и отпал?»

Это должен быть полноценный exegetical article с Greek detail, land analogy 6:7–8, 6:9–20, warning-system context и major interpretive views.

### Часть 4 — Евр. 10

**Route:** `/articles/evreyam-10-26-31-osvyashchennyy-krovyu-zaveta/`

**Title:**  
«Евреям 10:26–31: кто “освящён кровью завета” и почему ему грозит суд?»

Отдельный материал оправдан потому, что 10:29 имеет самостоятельную grammatical/theological проблему и не должен быть сноской в статье о Евр. 6.

### Часть 5 — временная вера

**Route:** `/articles/vremennaya-vera-i-stoykost-svyatyh/`

**Title:**  
«“До времени веруют”: временная вера и стойкость святых»

Corpus:
- Luke 8/Matt 13/Mark 4;
- Acts 8 Simon;
- John 2/8;
- 1 John 2:19;
- 1689 14.3/18.1;
- Owen/Watson.

### Возможная часть 6 — трудные тексты о «потере спасения»

Не создавать, пока Parts 1–5 не готовы. Если hard-case corpus окажется слишком большим, сделать:

**Route:** `/articles/mozhno-li-poteryat-spasenie-trudnye-teksty/`

Содержание:
John 15; Rom 11; Gal 5:4; 1 Cor 9–10; 2 Pet 2; Rev 3:5.

Но есть риск, что такой title превратит серьёзную библейскую теологию в FAQ/proof-text polemic. Лучше использовать его лишь при реальной необходимости.

## 3. Почему series hub лучше одной мегастатьи

### Читатель

Иуда и Евр. 6 — разные exegetical задачи. Если соединить Greek word studies, patristics, Reformed/Arminian debate, biblical theology и pastoral application в один HTML, материал станет труден для чтения и навигации.

### Поиск/SEO

Каждый hard text имеет собственный search intent:

- «Иуда был спасён?»
- «Евреям 6:4–6 можно потерять спасение?»
- «Евреям 10:29 освящён кровью»
- «временная вера Лука 8:13»

Отдельные canonical pages позволяют отвечать точно, а hub собирает authority тематически.

### Внутренняя архитектура

Existing `/hard-texts/` уже показывает нужную модель: `CollectionPage` + `hasPart` + отдельные Article routes. Не надо изобретать новый content framework.

## 4. Что должно быть на `/apostasy/`

Hub не должен быть пустым menu page. Минимум:

1. **Hero:** название серии + 2–3 предложения, что именно исследуется.
2. **Короткий doctrinal orientation:** различить тяжёлое падение и окончательное отступничество; указать, что серия исследует тексты до систематического вывода.
3. **Series map:** 4–5 карточек с status/read time.
4. **Ключевые определения:** saving faith, temporary faith, apostasy, perseverance, visible church/covenant privilege — кратко и без жаргона либо с tooltip.
5. **Canonical tension panel:** две колонки/группы текстов: warning texts и preservation promises; цель серии — не отменить ни одну группу.
6. **Research note:** исторические цитаты проверяются по первичным источникам; русские переводы редакционные, где нет установленного русского издания.
7. **Related materials:** «Тайны человеческого сердца» / Рим. 7 при наличии действительно полезного мостика, но не превращать hub в рекламный каталог.

## 5. Внутренняя навигация статьи

Каждый deep dive:

- breadcrumb: Главная → Статьи → Отступничество и стойкость → текущая статья;
- вверху small series badge;
- сразу после intro — краткий thesis box, но не conclusion-before-exegesis;
- sticky/normal TOC на desktop и existing reader TOC на mobile;
- в конце «В серии» с предыдущей/следующей частью;
- references/source notes;
- «Что этот текст НЕ говорит» как небольшой guardrail section у hard passages;
- crosslinks не только внизу, но и semantic links внутри текста.

## 6. Порядок публикации

Не обязательно публиковать в логическом номере исследования.

Лучший release order:

1. **Иуда** — понятный narrative entry point, уже хорошо исследован.
2. **Временная вера** — создаёт категории.
3. **Евр. 6** — самый известный hard text.
4. **Евр. 10** — углубляет covenant/sanctification issue.
5. **Флагманская статья + hub finalized** — после deep dives можно написать synthesis без обещаний, которые потом придётся переписывать.

Технически hub можно создать раньше и показывать «в работе», но Product-standard лучше не индексировать полупустую серию. Оптимально открыть hub, когда готовы минимум 2 материала.

## 7. Teletype / Telegram

### Teletype

Teletype — **не canonical source**. Если он доступен и нужен для распространения, туда лучше отправить adaptation флагманской статьи или отдельный popularized essay с canonical link на `gospod-bog.ru`.

Не держать две независимые «полные версии», иначе неизбежен editorial drift.

### Telegram

Telegram-версии должны быть:

- одна мысль / один hard text;
- 3500–4000 символов;
- ссылка на canonical article;
- не пытаться переносить весь source apparatus;
- при цитировании исторического автора оставлять максимум 1–2 проверенных золотых цитаты.

Например, по Иуде Telegram может быть entry post, а сайт — полный dossier.

## 8. SEO/metadata plan

### Hub `/apostasy/`

`title`: «Отступничество и стойкость веры — библейское исследование | Господь Бог — Сила Моя»  
`description`: «Иуда, временная вера, Евреям 6 и 10, предупреждения об отпадении и Божие сохранение святых: экзегеза трудных текстов и библейский синтез.»

JSON-LD:
- `CollectionPage`
- `hasPart` Articles
- `BreadcrumbList`
- `ImageObject`
- canonical and OG

### Individual articles

Use `Article`/`ScholarlyArticle` only if existing site standard supports it consistently. Do not invent schema type that breaks validators. Better clone the current strongest Article implementation and change content-specific metadata.

Keywords are secondary; titles, headings, descriptions, internal links and actual content matter more.

## 9. Visual concept

Series should not look like horror/sensational “fall from grace” content.

Possible visual language:

- narrow path / wilderness under darkening sky;
- vine with fruitful and dry branches, but avoid oversimplifying John 15 as series master image;
- rain falling equally over two fields, one fruitful and one thorny — probably the strongest biblical image from Heb. 6:7–8;
- distant light/anchor behind veil for preservation/hope side.

**Best series master:** two plots of earth under the same rain, one bearing grain/green growth, the other thorns, restrained cinematic palette, no text in source image. It visually states the exact Heb. 6 distinction without depicting God.

Judas article could have a separate non-kitsch image: empty place at a table / dropped coins / receding figure, but avoid treating unverified Supper chronology as doctrinal evidence.

## 10. Release gate before touching Product

No Product implementation until:

- Research dossiers reach at least `PUBLICATION-CANDIDATE`;
- Heb 10:29 lexical/grammatical pass closes or is explicitly represented as disputed;
- major commentary matrix is complete;
- each historical quote has exact primary locator;
- source-to-claim ledger exists;
- final article text passes site `ARTICLE-STANDARD-CHARTER.md`;
- new route is registered wherever current Product requires: articles index, search/index data, sitemap/feed if applicable, tests/validators;
- no live release until exact Product CI and release witness are green.

## 11. Decision

**Recommended architecture now:** reserve conceptually `/apostasy/` as a top-level series hub, but do not implement it yet. Store all evidence in Research. Publish later as 4–5 linked `articles/<slug>/` deep dives plus the hub, using the already established `/hard-texts/` series pattern.

Это лучше, чем Teletype-first и лучше, чем одна мегастатья: Research остаётся единым доказательным слоем, `gospod-bog.ru` — canonical publication layer, Telegram/Teletype — производные distribution layers.
