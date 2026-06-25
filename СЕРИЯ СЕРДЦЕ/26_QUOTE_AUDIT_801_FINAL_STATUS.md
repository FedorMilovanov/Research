# Аудит 801 строк и финальные статусы

> Consolidated in v53 from SERDCE_RESEARCH_PACK v52. Every original file is preserved below under its original path.



---

## ORIGINAL_FILE: `264_V40_PARAPHRASE_PURGE_PLAN_AND_LINT_RULES.md`

# V40 — Paraphrase Purge Plan and Lint Rules

## Что чистим

Все строки старого архива, где есть:

- кавычки вокруг богословской формулы;
- `>` blockquote;
- “говорит”, “пишет”, “утверждает”, “формулирует”, “у него есть мысль”;
- “пуритане говорят”;
- “Charnock/Owen/Edwards/Boston учит...” без точного локатора;
- “цитата” без статуса.

## Как исправлять

### Случай 1: есть точный источник

Оставляем цитату и добавляем:

```text
Status: EXACT_QUOTE
Author:
Work:
Locator:
Source URL / Edition:
Use:
Guardrail:
```

### Случай 2: есть только смысл, но нет точной цитаты

Убираем кавычки и пишем:

```text
Status: ANALYTICAL_SUMMARY_NOT_A_QUOTE
This is our synthesis, not author wording.
Needs quote anchor before article publication.
```

### Случай 3: цитата найдена в modernized source

Помечаем:

```text
Status: EXACT_QUOTE_FROM_MODERNIZED_TEXT
Do not present as original spelling.
For scholarly use, verify against original edition.
```

### Случай 4: источник вторичный

Помечаем:

```text
Status: SECONDARY_LEAD_ONLY
Do not quote in article.
Use to find primary source.
```

## Строгие правила линтера

Линтер не доказывает, что цитата точная. Он только ловит опасные места.

Он должен ругаться на:

- кавычки рядом с именем автора без `Status: EXACT_QUOTE`;
- blockquote без `Source:` в ближайших строках;
- “говорит/пишет/утверждает” без локатора;
- “по словам” без локатора;
- “цитата” без статуса;
- длинные цитаты без причины.

## Editorial red lines

Нельзя публиковать в статье:

- “свободный перевод” как цитату;
- сокращённый пересказ как quote;
- точную цитату без ссылки;
- ссылку без локатора;
- цитату из поиска без открытия страницы;
- цитату из PDF без page-check.

## Минимальный формат цитаты в статье

```markdown
> “Exact short quote.”

— Author, *Work*, chapter/section/page, source edition.
```

Затем отдельно:

```markdown
Наш вывод: ...
Пастырский предохранитель: ...
```


---

## ORIGINAL_FILE: `267_V41_801_QUOTE_AUDIT_BATCH1.md`

# v41 — проверка 801 suspect lines: batch 1 / triage + web anchors

Дата: 2026-06-25.

## Что реально сделано

Проверка v40 дала 801 строку, которые линтер посчитал подозрительными: blockquote, кавычки, либо атрибуция источника. В v41 все 801 строки получили первичный статус в `data/v41_801_triage_full.csv`.

Это **не означает**, что 801 строка вручную сверена по странице как точная цитата. Это означает, что каждая строка теперь не висит как неопределённая: она классифицирована для редакторской работы.

## Ключевой вывод

Большая часть 801 — это не чужие цитаты, а наши русские авторские формулы, оформленные через `>` как выразительные тезисы. Для публикации их нужно переоформлять как авторский текст, а не как цитату.

## Итоги по статусам

| Статус | Кол-во |
|---|---:|
| QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | 357 |
| INTERNAL_AUTHOR_THESIS_REWRITE_NOT_QUOTE | 291 |
| LOW_RISK_INTERNAL_PROSE_OR_TABLE | 109 |
| ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | 22 |
| EDITORIAL_EXAMPLE_QUOTATION_OK_BUT_STYLE_REVIEW | 14 |
| SOURCE_SUMMARY_NOT_A_QUOTE | 8 |

## Самые загруженные файлы

| Файл | Подозрительных строк |
|---|---:|
| 01_SERDCE_RESEARCH_MASTER.md | 57 |
| 166_V22_ANTI_CONFUSION_MAP_DEEP_PATTERNS_RESPONSIBILITY_TRAUMA.md | 38 |
| 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md | 35 |
| 190_V28_PASTORAL_TRIAGE_MAP_SAFETY_AUTHORITY_LIMITS.md | 33 |
| 195_V29_PASTORAL_MAP_HEART_UNDER_AFFLICTION_PROVIDENCE.md | 32 |
| 00_README.md | 27 |
| 165_V22_EXEGETICAL_CHAIN_CUSTOM_HARDENING_DECEITFULNESS.md | 27 |
| 167_V22_READY_ARTICLE_DRAFT_SECOND_NATURE_HEART.md | 25 |
| 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md | 24 |
| 197_V29_CHECKLIST_SUFFERING_LAMENT_PROVIDENCE_SERIES_GUARDRAILS.md | 23 |
| 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md | 22 |
| 193_V29_QUALITY_AUDIT_SUFFERING_PROVIDENCE_LAYER.md | 21 |
| 186_V27_PASTORAL_MAP_CONFESSION_EXHORTATION_DISCIPLINE_RESTORATION.md | 18 |
| 189_V28_SOURCE_VERIFIED_SAFETY_ABUSE_SUICIDE_LIMITS.md | 18 |
| 196_V29_ARTICLE_MODULE_WHEN_SUFFERING_REVEALS_THE_HEART.md | 18 |
| 171_V23_ARTICLE_MODULE_FROM_SECOND_NATURE_TO_NEW_AFFECTION.md | 17 |
| 194_V29_SOURCE_VERIFIED_PROVIDENCE_LAMENT_AFFLICTION.md | 17 |
| 187_V27_ARTICLE_MODULE_THE_HEART_IS_NOT_HEALED_IN_ISOLATION.md | 16 |
| 182_V26_PASTORAL_MAP_CHANGE_WITHOUT_MORALISM_OR_MAGIC.md | 15 |
| 180_V26_QUALITY_AUDIT_CHANGE_LAYER_MORTIFICATION_VIVIFICATION.md | 14 |
| 185_V27_SOURCE_VERIFIED_HEBREWS_1689_COMMUNION_BONHOEFFER_SOCIAL_SUPPORT.md | 14 |
| 183_V26_ARTICLE_MODULE_HOW_DEEP_PATTERNS_CHANGE.md | 13 |
| 181_V26_SOURCE_VERIFIED_OWEN_CALVIN_HEIDELBERG_1689_DORT.md | 12 |
| 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md | 9 |
| 175_V24_ARTICLE_MODULE_HEART_NEGOTIATES_WITH_CONSCIENCE.md | 9 |

## Новые файлы v41

- `267_V41_801_QUOTE_AUDIT_BATCH1.md`
- `268_V41_801_TRIAGE_SUMMARY_AND_COUNTS.md`
- `269_V41_WEB_VERIFIED_EXACT_QUOTE_ANCHORS_BATCH1.md`
- `270_V41_REWRITE_GUIDE_FOR_BLOCKQUOTE_THESES.md`
- `271_V41_NEXT_BATCH_QUEUE_AND_PRIORITIES.md`
- `data/v41_801_triage_full.csv`
- `data/v41_801_summary_counts.csv`
- `data/v41_801_by_file_top.csv`
- `data/v41_verified_quote_anchors_batch1.csv`
- `tools/v41_quote_audit_batch.py`

## Новое правило после v41

1. `>` в рабочих MD больше не использовать для красивого авторского тезиса, если это может быть принято за цитату.
2. Дословная цитата допускается только в формате: автор, труд, раздел/страница/строка, источник, статус.
3. Русские формулы архива переносить в статью как наш авторский текст, а не как quote block.
4. Если нужна русская цитата старого англоязычного автора, сначала ставить оригинал, затем наш перевод как перевод, не как независимую цитату.


---

## ORIGINAL_FILE: `267_V42_801_QUOTE_AUDIT_BATCH2_DEEPENING.md`

# v42 — 801 quote audit, batch 2: углубление и зачистка риска

## Что сделано

В v41 все 801 подозрительных места были разложены по первичным статусам. В v42 закрыт следующий слой: **22 строки с явной атрибуцией / именем автора / названием труда / кавычками**.

Это самые опасные места, потому что читатель может принять их за дословные цитаты. После проверки они разделены на группы:

1. **EXACT_ANCHOR_AVAILABLE** — можно цитировать, но только коротко и с точным локатором.
2. **WORK_TITLE / BIBLIOGRAPHIC_ENTRY** — кавычки были вокруг названия труда, а не вокруг цитаты.
3. **INTERNAL_SUMMARY_NOT_QUOTE** — это наш вывод, нельзя оформлять как цитату.
4. **MODERNIZED / EXTRACT STATUS** — можно использовать как рабочий локатор, но для академической публикации лучше сверить с изданием/сканом.

## Главный редакторский итог

Не всякая строка с кавычками — ошибка. Но всякая строка с кавычками должна иметь ясный статус.

Правило v42:

- название книги можно оставлять в кавычках или лучше переводить в курсив/`backticks`;
- русские тезисы в blockquote — переписать как авторский текст, не как чужую цитату;
- точная цитата должна быть короткой, дословной, с автором, трудом, разделом/главой/линиями/страницей;
- modernized texts помечать как modernized, а не как оригинальную орфографию XVII века.

## Что теперь стало лучше

v42 не просто добавляет цитаты, а очищает метод: теперь у каждого опасного места появляется судьба — цитировать, переписать, оставить как библиографию, или отложить до primary check.

См. файлы:

- `data/v42_22_attributed_resolution_batch2.csv`
- `data/v42_801_triage_after_batch2.csv`
- `data/v42_357_ambiguous_queue_prioritized.csv`
- `data/v42_verified_quote_anchors_batch2.csv`


---

## ORIGINAL_FILE: `267_V43_357_AMBIGUOUS_QUOTES_CLOSED_AUDIT.md`

# v43 — Closing the 357 ambiguous quotation-mark rows

## Purpose

This batch closes the remaining **357 rows** that v42 left under `QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY`.

The key finding is editorial rather than merely bibliographic: these 357 rows were not primarily hidden Puritan quotations. They were mostly Russian diagnostic phrases, internal article titles, examples of inner speech, scare quotes, search queries, and Bible references. They were dangerous only because quotation marks can make internal language look like a source quotation.

## Result

All 357 rows now have a replacement status in:

- `data/v43_357_ambiguous_closed_batch3.csv`
- `data/v43_801_triage_after_closing_357.csv`
- `data/v43_357_closed_status_counts.csv`

## Status breakdown for the 357

| new_status                                                    |   count |
|:--------------------------------------------------------------|--------:|
| RESOLVED_INTERNAL_DIAGNOSTIC_PHRASE_NOT_QUOTE                 |     164 |
| RESOLVED_INTERNAL_CASE_VOICE_NOT_SOURCE_QUOTE                 |     113 |
| RESOLVED_GENERIC_RUSSIAN_STYLE_QUOTES_NOT_SOURCE_QUOTE        |      34 |
| RESOLVED_SCRIPTURE_QUOTE_OR_REFERENCE_NEEDS_BIBLE_EDITION     |      17 |
| RESOLVED_KEYWORD_OR_TERM_NOT_QUOTE                            |      15 |
| RESOLVED_FILE_TITLE_OR_INTERNAL_LABEL_NOT_QUOTE               |       5 |
| RESOLVED_SEARCH_QUERY_OR_MODERN_WORK_TITLE_NOT_QUOTE          |       3 |
| RESOLVED_WORK_TITLE_OR_ARTICLE_TITLE_NOT_QUOTE                |       2 |
| RESOLVED_WORK_TITLE_NOT_QUOTE                                 |       1 |
| RESOLVED_INTERNAL_ARTICLE_TITLE_OR_EDITORIAL_THESIS_NOT_QUOTE |       1 |
| RESOLVED_CONFESSION_TITLE_AND_SUMMARY_NOT_QUOTE               |       1 |
| RESOLVED_CONFESSION_REFERENCE_SUMMARY_NOT_QUOTE               |       1 |

## What this means for writing

### 1. Internal Russian diagnostic phrases are not quotations

Examples such as “если бы ты верил, тебе было бы легко” or “без этого я не выдержу” are not source quotations. They are editorially useful as examples of inner speech, false comfort, pastoral mistakes, or diagnostic language.

**Rule:** these may be kept only as examples, not as attributed quotations.

### 2. Book/article titles are not source claims

Items like `When People Are Big and God Is Small`, `Idols of the Heart and Vanity Fair`, or planned article titles are safe as titles. The title itself may stay in quotation marks or italics depending on style, but any adjacent doctrinal claim must be clearly separated as our summary.

### 3. Scripture quotations need translation/version

Rows containing direct Bible wording are not “bad,” but they are not complete unless the Bible translation/version is named.

**Rule:** exact wording of Scripture requires reference + translation/version. A summary of a passage should not be in quotation marks.

### 4. Search queries should be code, not quotes

Search strings like `site:thinkbiblically.org "Thinking Biblically About the Heart"` should be formatted as search queries, not source quotations.

### 5. Source quotes remain strict

Nothing in this v43 closure weakens v39/v40 policy. If the article says “Charnock writes…” or uses blockquote as an external quotation, it must have author, work, locator, exact text, and source status.

## After v43

The original 801 suspicious rows are now editorially triaged. The next stage is not another broad pass over quotation marks; it is direct cleanup of article-ready files:

1. remove quotation marks around internal Russian diagnostic phrases;
2. convert planned article titles to italics/headings;
3. mark Bible quotes with translation/version;
4. keep only verified exact quote anchors from the quote bank;
5. send any new author quotation back through the v39 strict protocol.


---

## ORIGINAL_FILE: `269_V43_WEB_VERIFIED_ANCHORS_FOR_357_CLOSURE.md`

# v43 — Web-verified source anchors for the closed ambiguous batch

This file records which web sources were used while closing the 357 ambiguous quotation-mark rows.

## High-confidence exact anchors

| Author/source | Work | Exact short anchor | Use |
|---|---|---|---|
| Stephen Charnock | Discourse on Practical Atheism | “Actions are a greater discovery of a principle than words.” | Use for heart/practice/practical atheism. |
| John Owen | Of Temptation | “Entertain no parley…” | Use for temptation and consent, with CCEL locator. |
| Jonathan Edwards | Religious Affections | “True grace is not an unactive thing.” | Use for grace and practice, not works-righteousness. |
| Canons of Dort | III/IV | “God infuses new qualities into the will…” | Use for regeneration and renewed will. |

## Source-title anchors, not quote anchors

These sources are now title/locator-safe but not quote-safe without a page/transcript check:

- Edward Welch, `When People Are Big and God Is Small`.
- David Powlison, `Idols of the Heart and Vanity Fair`.
- Greg Gifford, `Thinking Biblically About Habits` / `Heart & Habits`.

## Modernized / edition caution

Sibbes and Goodwin are useful and source-locatable, but when using modernized web editions the article must say so in the research note or use a stable edition/PDF.

## Practical result

The 357 rows were closed because they were mostly not source quotations. The external source material remains governed by exact-quote discipline, not by attractive paraphrase.


---

## ORIGINAL_FILE: `270_V43_ARTICLE_CLEANUP_PLAN_AFTER_CLOSING_357.md`

# v43 — Cleanup plan after closing the 357 ambiguous rows

## The remaining work is cleanup, not discovery

After v43 the ambiguous quotation-mark batch is no longer an unknown pile. It is a set of editorial actions.

## Action map

| status                                                        | example_id   | required_action                                                                                                       |
|:--------------------------------------------------------------|:-------------|:----------------------------------------------------------------------------------------------------------------------|
| RESOLVED_CONFESSION_REFERENCE_SUMMARY_NOT_QUOTE               | V41-LINT-324 | Keep as summary/reference; do not put summary in quotation marks.                                                     |
| RESOLVED_CONFESSION_TITLE_AND_SUMMARY_NOT_QUOTE               | V41-LINT-323 | Treat Russian phrase as article-use label, not a quote; exact confessional wording requires article locator.          |
| RESOLVED_FILE_TITLE_OR_INTERNAL_LABEL_NOT_QUOTE               | V41-LINT-014 | Keep filenames in code; article/module titles may use italics, not blockquote.                                        |
| RESOLVED_GENERIC_RUSSIAN_STYLE_QUOTES_NOT_SOURCE_QUOTE        | V41-LINT-130 | Replace with italics, no quotes, or explicit “так называемый” only if needed; not a citation.                         |
| RESOLVED_INTERNAL_ARTICLE_TITLE_OR_EDITORIAL_THESIS_NOT_QUOTE | V41-LINT-240 | Rewrite as normal author text or heading; no blockquote/quote formatting.                                             |
| RESOLVED_INTERNAL_CASE_VOICE_NOT_SOURCE_QUOTE                 | V41-LINT-132 | Keep only as illustrative inner speech/example; label as “пример внутренней речи”, not as author/source quote.        |
| RESOLVED_INTERNAL_DIAGNOSTIC_PHRASE_NOT_QUOTE                 | V41-LINT-017 | Remove quotation marks or explicitly label as diagnostic paraphrase/example, never as cited source.                   |
| RESOLVED_KEYWORD_OR_TERM_NOT_QUOTE                            | V41-LINT-178 | Use code formatting/italics for term; not quotation marks as source quote.                                            |
| RESOLVED_SCRIPTURE_QUOTE_OR_REFERENCE_NEEDS_BIBLE_EDITION     | V41-LINT-062 | If verse wording is quoted, attach Bible translation/version; if only summary, remove quotation marks around summary. |
| RESOLVED_SEARCH_QUERY_OR_MODERN_WORK_TITLE_NOT_QUOTE          | V41-LINT-094 | Keep as search query/title; do not quote Gifford without page/source.                                                 |
| RESOLVED_WORK_TITLE_NOT_QUOTE                                 | V41-LINT-078 | Keep book title in italics/backticks; do not treat adjacent Russian summary as quote.                                 |
| RESOLVED_WORK_TITLE_OR_ARTICLE_TITLE_NOT_QUOTE                | V41-LINT-193 | Keep title as title only; any doctrinal claim needs exact citation if quoted.                                         |

## Recommended cleanup order

1. **Article-ready modules first**: files with `ARTICLE_MODULE`, `READY`, `BLUEPRINT`, and master notes.
2. **Scripture wording second**: add Bible translation/version wherever exact biblical wording is quoted.
3. **Modern authors third**: Welch/Powlison/Gifford should remain source-title references unless exact page/source text is verified.
4. **Puritan exact quotes last**: only from quote bank or fresh primary check.

## What not to do

Do not mechanically remove all quotation marks. Some are useful as examples of inner speech. The problem is not punctuation itself; the problem is ambiguity between authorial example and source quotation.

## Article-writing policy after v43

When drafting the actual series, every source-bearing paragraph should follow this order:

1. biblical text or theological claim;
2. exact source quote if needed;
3. locator;
4. our interpretation;
5. pastoral guardrail.

If there is no exact source quote, do not imitate one.


---

## ORIGINAL_FILE: `271_V41_NEXT_BATCH_QUEUE_AND_PRIORITIES.md`

# v41 — next batch queue / приоритеты проверки

Следующая ручная пачка должна идти не по порядку файлов, а по риску.

## Приоритет 1

`ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK`: строки, где есть имя автора/труда и кавычки. Их нельзя переносить в статью без точного локатора.

## Приоритет 2

`BLOCKQUOTE_REQUIRES_SOURCE_CHECK`: английские blockquote, которые могут быть настоящими цитатами.

## Приоритет 3

`QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY`: кавычки без явного автора; чаще это примеры внутренней речи, но перед публикацией лучше снять двусмысленность.

## Первые 120 строк очереди

| ID | Место | Статус | Фрагмент |
|---|---|---|---|
| V41-LINT-014 | 00_README.md:395 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | v29 лучше ставить после v28 или как отдельную статью после блока о церковной помощи и границах. Он нужен, чтобы серия не звучала как “только |
| V41-LINT-017 | 00_README.md:481 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | **Режим:** качество, не количество: после диагностики v21–v25 добавлен слой о том, как глубокие паттерны реально меняются — без морализма “п |
| V41-LINT-022 | 00_README.md:663 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | - John Flavel, `On Keeping the Heart` — сердце как “whole soul / inner man”, хранение сердца как постоянное духовное дело, но сила от Христа |
| V41-LINT-027 | 00_README.md:780 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - готовая структура для будущей статьи “Сердце как поклоняющийся центр человека”. |
| V41-LINT-028 | 01_SERDCE_RESEARCH_MASTER.md:5 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | V40 фиксирует редакционный стандарт для всей серии: **exact quote first**. Любой материал v13–v38, где есть кавычки, blockquote, “X говорит/ |
| V41-LINT-030 | 01_SERDCE_RESEARCH_MASTER.md:44 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Старые файлы v1–v38 не выбрасываются, но перед статьёй каждая цитата и каждое “по словам автора” должны пройти v39 quote bank или новую свер |
| V41-LINT-032 | 01_SERDCE_RESEARCH_MASTER.md:59 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | Главный практический вывод: будущую серию нужно писать source-weighted: не просто “пуритане говорили”, а “этот автор закрывает этот конкретн |
| V41-LINT-044 | 01_SERDCE_RESEARCH_MASTER.md:344 | EDITORIAL_EXAMPLE_QUOTATION_OK_BUT_STYLE_REVIEW | Этот слой добавляет после v26 недостающий общинный контекст перемены. Если v26 отвечал на вопрос “как глубокий паттерн меняется через покаян |
| V41-LINT-049 | 01_SERDCE_RESEARCH_MASTER.md:402 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Практический вывод v24: статья должна избегать двух провалов: **наивности** (“человек просто не понял”) и **пастырской жестокости** (“всякая |
| V41-LINT-051 | 01_SERDCE_RESEARCH_MASTER.md:419 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - `171_V23_ARTICLE_MODULE_FROM_SECOND_NATURE_TO_NEW_AFFECTION.md` — готовый статейный модуль, соединяющий “вторую природу” с “новой привязан |
| V41-LINT-052 | 01_SERDCE_RESEARCH_MASTER.md:422 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Практический вывод v23: будущая статья должна идти не по линии “привычка сильная, значит нужна техника посильнее”, а по линии **привычка дер |
| V41-LINT-054 | 01_SERDCE_RESEARCH_MASTER.md:441 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Практический вывод v22: статья должна идти не по линии “плохая привычка → техника исправления”, а по линии **сердце → ложное благо → повторе |
| V41-LINT-056 | 01_SERDCE_RESEARCH_MASTER.md:472 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Практический вывод v28: будущая статья должна избегать двух провалов: **самоуверенной духовной редукции** (“всё решим обличением сердца”) и  |
| V41-LINT-058 | 01_SERDCE_RESEARCH_MASTER.md:491 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Практический вывод v26: будущая статья должна идти не по линии “плохая привычка → техника замены”, а по линии **свет → исповедание → вера →  |
| V41-LINT-062 | 01_SERDCE_RESEARCH_MASTER.md:561 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Рим. 1 показывает помрачённое сердце и идолопоклонство. Рим. 6:17 говорит о послушании от сердца. Рим. 7 раскрывает внутреннюю войну верующе |
| V41-LINT-073 | 01_SERDCE_RESEARCH_MASTER.md:1051 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Сердце в Писании не просто “внутренний орган выбора” и не только “место эмоций”. Оно является поклоняющимся центром человека: оно любит, бои |
| V41-LINT-074 | 01_SERDCE_RESEARCH_MASTER.md:1055 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Без этого слоя серия может стать слишком диагностической: “сердце испорчено, воля связана, грех глубок”. Это верно, но неполно. Библейское л |
| V41-LINT-075 | 01_SERDCE_RESEARCH_MASTER.md:1069 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | - Thomas Chalmers — “The Expulsive Power of a New Affection”: старую любовь нельзя просто выгнать пустотой; её вытесняет новая, более сильна |
| V41-LINT-076 | 01_SERDCE_RESEARCH_MASTER.md:1070 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | - Jonathan Edwards — “Religious Affections”: истинная религия имеет святые аффекты, но не всякое сильное религиозное чувство является благод |
| V41-LINT-077 | 01_SERDCE_RESEARCH_MASTER.md:1071 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | - John Owen — “Spiritual Mindedness”: Рим. 8:6 раскрывает различие между помышлением плоти и помышлением Духа. |
| V41-LINT-078 | 01_SERDCE_RESEARCH_MASTER.md:1075 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Edward Welch — “When People Are Big and God Is Small”: страх человека — поклонническая деформация сердца, где люди становятся “большими”,  |
| V41-LINT-094 | 07_READING_PLAN_AND_SEARCH_QUERIES.md:78 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | site:thinkbiblically.org "Thinking Biblically About the Heart" |
| V41-LINT-095 | 07_READING_PLAN_AND_SEARCH_QUERIES.md:160 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | site:thinkbiblically.org "Thinking Biblically About the Heart" Greg Gifford |
| V41-LINT-106 | 104_V15_HEART_AS_WORSHIP_LOVE_TREASURE.md:5 | EDITORIAL_EXAMPLE_QUOTATION_OK_BUT_STYLE_REVIEW | Библейское сердце не является нейтральным внутренним механизмом. Оно всегда направлено: любит, боится, доверяет, ищет, радуется, надеется, з |
| V41-LINT-109 | 104_V15_HEART_AS_WORSHIP_LOVE_TREASURE.md:43 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Для борющегося: не только “откажись”, но “увидь лучшее, живи новым сокровищем”. |
| V41-LINT-110 | 105_V15_EXPULSIVE_POWER_NEW_AFFECTION_CHALMERS.md:1 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | # v15 — Thomas Chalmers: “The Expulsive Power of a New Affection” |
| V41-LINT-111 | 105_V15_EXPULSIVE_POWER_NEW_AFFECTION_CHALMERS.md:26 | EDITORIAL_EXAMPLE_QUOTATION_OK_BUT_STYLE_REVIEW | Нельзя сказать: “просто найди новую эмоцию”. Речь не о психологической замене настроения. Речь о духовном пересоздании любви, когда Дух чере |
| V41-LINT-113 | 105_V15_EXPULSIVE_POWER_NEW_AFFECTION_CHALMERS.md:34 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | - Thomas Chalmers, “The Expulsive Power of a New Affection”, Monergism PDF. |
| V41-LINT-114 | 106_V15_EDWARDS_AFFECTIONS_NOT_EMOTIONALISM.md:5 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | Edwards важен не потому, что “он сильный кальвинист”, а потому что он тонко различает: |
| V41-LINT-115 | 106_V15_EDWARDS_AFFECTIONS_NOT_EMOTIONALISM.md:15 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Это прямо служит теме “одинаковая внешность — разная внутренность”. |
| V41-LINT-117 | 107_V15_FEAR_OF_MAN_WELCH_POWLISON_HEART_IDOLS.md:5 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Многие грехи сердца выглядят как “просто характер”, “просто тревожность”, “просто застенчивость”, “просто конфликтность”. Но Писание часто в |
| V41-LINT-120 | 108_V15_HEART_OF_CHRIST_AS_GOSPEL_ANTIDOTE.md:31 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - В конце статьи “Что Библия называет сердцем?” |
| V41-LINT-121 | 109_V15_AFFECTION_REPLACEMENT_NOT_MORALISM.md:5 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Морализм говорит: “перестань делать плохое, делай хорошее”. Библейская перемена сердца глубже: Бог меняет то, что сердце считает красивым, б |
| V41-LINT-123 | 111_V15_RESEARCH_TO_ARTICLE_BLUEPRINT_WORSHIPPING_HEART.md:1 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | # v15 — Blueprint статьи: “Сердце как поклоняющийся центр человека” |
| V41-LINT-127 | 122_V17_HEART_PATTERNS_BODY_MEMORY_ENVIRONMENT.md:9 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Библейски это не нужно описывать как автономную психологическую машину, будто человек — жертва механизма. Но и нельзя упрощать до “просто ре |
| V41-LINT-128 | 122_V17_HEART_PATTERNS_BODY_MEMORY_ENVIRONMENT.md:13 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Не всегда. Многие реакции сердца сначала переживаются как “просто так получилось”, “я не подумал”, “оно само”. Но неосознанность не равна не |
| V41-LINT-129 | 122_V17_HEART_PATTERNS_BODY_MEMORY_ENVIRONMENT.md:17 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Пс. 18:13 — “Кто усмотрит погрешности свои? От тайных моих очисти меня”. |
| V41-LINT-130 | 122_V17_HEART_PATTERNS_BODY_MEMORY_ENVIRONMENT.md:49 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Сложность: человек может помнить грех не как отвращение, а как “сладкий кадр”. Поэтому борьба — не только “не делай”, но “переучивай память  |
| V41-LINT-131 | 123_V17_ATTACHMENTS_CAN_LAST_BUT_NOT_RULE.md:3 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | ## 1. Привязанность как “любовь + утешение + идентичность” |
| V41-LINT-132 | 123_V17_ATTACHMENTS_CAN_LAST_BUT_NOT_RULE.md:8 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “это даёт мне контроль”; |
| V41-LINT-133 | 123_V17_ATTACHMENTS_CAN_LAST_BUT_NOT_RULE.md:10 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “это доказывает, что я значим”; |
| V41-LINT-134 | 123_V17_ATTACHMENTS_CAN_LAST_BUT_NOT_RULE.md:11 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “это мстит за мою боль”; |
| V41-LINT-135 | 123_V17_ATTACHMENTS_CAN_LAST_BUT_NOT_RULE.md:13 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “без этого я не выдержу”. |
| V41-LINT-136 | 123_V17_ATTACHMENTS_CAN_LAST_BUT_NOT_RULE.md:50 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | ### Крайность 1: “Если это долго со мной, значит это моя настоящая сущность” |
| V41-LINT-137 | 123_V17_ATTACHMENTS_CAN_LAST_BUT_NOT_RULE.md:54 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | ### Крайность 2: “Если я во Христе, значит глубокие привязанности должны исчезнуть быстро” |
| V41-LINT-140 | 124_V17_HABIT_LOOP_BIBLICAL_COUNSELING_WITH_GUARDRAILS.md:27 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Gifford полезен тем, что соединяет тему привычек с библейским сердцем и ответственностью верующего. Его подход помогает не сказать “измени с |
| V41-LINT-142 | 125_V17_CHILDHOOD_FORMATION_NO_DETERMINISM_NO_NAIVETY.md:16 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Библия не даёт человеку сказать: “меня сформировали, поэтому я не отвечаю”. Адам обвиняет Еву, Ева — змея; падшее сердце ищет внешнего винов |
| V41-LINT-143 | 125_V17_CHILDHOOD_FORMATION_NO_DETERMINISM_NO_NAIVETY.md:47 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Нельзя жестоко говорить человеку: “просто перестань, детство не важно”. Это пастырски слепо. |
| V41-LINT-144 | 125_V17_CHILDHOOD_FORMATION_NO_DETERMINISM_NO_NAIVETY.md:49 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Нельзя и говорить: “твоя история навсегда определила тебя”. Это евангельски неверно. |
| V41-LINT-146 | 126_V17_RESIDUAL_SIN_LIFELONG_WARFARE_NOT_DESPAIR.md:11 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Иногда человек думает: “если я всё ещё борюсь, значит ничего не изменилось”. Это неверно. В невозрождённом состоянии грех может жить без нас |
| V41-LINT-147 | 126_V17_RESIDUAL_SIN_LIFELONG_WARFARE_NOT_DESPAIR.md:22 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Опасная фраза: “это моя lifelong struggle, поэтому я просто принимаю”. Библия не даёт права заключать мир с грехом. Долгая война — не капиту |
| V41-LINT-148 | 126_V17_RESIDUAL_SIN_LIFELONG_WARFARE_NOT_DESPAIR.md:26 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | 1. **Перфекционизм:** “если я истинно верующий, этот грех исчезнет полностью сейчас”. |
| V41-LINT-149 | 126_V17_RESIDUAL_SIN_LIFELONG_WARFARE_NOT_DESPAIR.md:27 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | 2. **Отчаяние:** “если он не исчез, Христос меня не меняет”. |
| V41-LINT-150 | 126_V17_RESIDUAL_SIN_LIFELONG_WARFARE_NOT_DESPAIR.md:28 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | 3. **Примирение:** “раз он долго со мной, значит это не так страшно”. |
| V41-LINT-151 | 126_V17_RESIDUAL_SIN_LIFELONG_WARFARE_NOT_DESPAIR.md:40 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - молиться не только “убери”, но “покажи Христа большим”;  |
| V41-LINT-153 | 127_V17_PATTERNS_SCRIPTURE_CHAIN_AND_CASES.md:55 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Откр. 3:17: “я богат” — а Христос говорит: “ты несчастен, жалок, нищ, слеп и наг”. Сердце может иметь уверенность, которая не является верой |
| V41-LINT-154 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:9 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Это просто привычка, поменяй технику”. |
| V41-LINT-155 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:10 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Это просто травма, ты не отвечаешь”. |
| V41-LINT-156 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:11 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если бы ты верил, тебе было бы легко”. |
| V41-LINT-157 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:12 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Раз это с детства, ничего не поделаешь”. |
| V41-LINT-158 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:13 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Раз ты снова пал, значит покаяния не было”. |
| V41-LINT-159 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:14 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Просто перестань думать об этом”. |
| V41-LINT-160 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:31 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Не общо: “я плохой”, а конкретно: “когда я чувствую отвержение, я ищу контроль через гнев/изоляцию/угождение/фантазии”. |
| V41-LINT-161 | 128_V17_PASTORAL_CARE_FOR_LONG_TERM_PATTERNS.md:47 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Не “ты справишься”, а “Христос не холоден к сокрушённому, Дух живёт в тебе, Отец не отрёкся от сына”. |
| V41-LINT-163 | 129_V17_ARTICLE_BLUEPRINT_HEART_PATTERNS_ATTACHMENTS.md:13 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | ### 1. Почему одного “я больше так не буду” часто недостаточно |
| V41-LINT-164 | 129_V17_ARTICLE_BLUEPRINT_HEART_PATTERNS_ATTACHMENTS.md:22 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Я должен доказать ценность” → ревность/сравнение. |
| V41-LINT-165 | 129_V17_ARTICLE_BLUEPRINT_HEART_PATTERNS_ATTACHMENTS.md:23 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Мне нужно утешение сейчас” → бегство к идолу. |
| V41-LINT-166 | 129_V17_ARTICLE_BLUEPRINT_HEART_PATTERNS_ATTACHMENTS.md:24 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если я откроюсь, меня уничтожат” → скрытность. |
| V41-LINT-172 | 130_V17_RESEARCH_BACKLOG_PATTERNS_MEMORY_BODY.md:10 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “desire / lust / covet”; |
| V41-LINT-173 | 130_V17_RESEARCH_BACKLOG_PATTERNS_MEMORY_BODY.md:12 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “mind / mindset / phroneo” в Рим. 8 и Флп.; |
| V41-LINT-174 | 130_V17_RESEARCH_BACKLOG_PATTERNS_MEMORY_BODY.md:14 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “train / discipline / practice” в 1 Тим. 4, Евр. 5, 12. |
| V41-LINT-175 | 130_V17_RESEARCH_BACKLOG_PATTERNS_MEMORY_BODY.md:59 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | **“Сердце, тело и страдание: как боль, травма, усталость, болезнь, депрессия и страх взаимодействуют с духовной борьбой без редукционизма”.* |
| V41-LINT-178 | 131_V18_SECOND_NATURE_HEART_PATTERNS_AUTOMATICITY.md:75 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Источник: Phillippa Lally et al., “How are habits formed: Modelling habit formation in the real world,” European Journal of Social Psycholog |
| V41-LINT-193 | 135_V18_FALSE_COMFORTS_SUBSTITUTE_ATTACHMENTS.md:60 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Источник: David Powlison, “Idols of the Heart and Vanity Fair” — https://www.ccef.org/idols-heart-and-vanity-fair/ |
| V41-LINT-194 | 135_V18_FALSE_COMFORTS_SUBSTITUTE_ATTACHMENTS.md:66 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | Источник: Thomas Chalmers, “The Expulsive Power of a New Affection” — https://www.monergism.com/thethreshold/sdg/Chalmers%2C%20Thomas%20-%20 |
| V41-LINT-238 | 160_V21_QUALITY_AUDIT_AND_CONSOLIDATION_PLAN.md:82 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не говорить “автоматично значит невиновно”. |
| V41-LINT-239 | 160_V21_QUALITY_AUDIT_AND_CONSOLIDATION_PLAN.md:83 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не говорить “если долго борешься, значит не возрождён”. |
| V41-LINT-240 | 160_V21_QUALITY_AUDIT_AND_CONSOLIDATION_PLAN.md:97 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Следующий лучший шаг — не “ещё исследование вообще”, а **написание первой сильной статьи из v17–v21**. Архив уже имеет достаточно материала. |
| V41-LINT-241 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:30 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | В `Indwelling Sin` Owen разбирает Рим. 7:21 и показывает, что Павел говорит о “law” греха как о действенном внутреннем принципе в верующем.  |
| V41-LINT-242 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:39 | EDITORIAL_EXAMPLE_QUOTATION_OK_BUT_STYLE_REVIEW | Не писать: “Owen учит habit loop”. Он этого не делает. |
| V41-LINT-245 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:63 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | Flavel должен стоять рядом с темой “осторожности к своему сердцу”. Он помогает сказать: |
| V41-LINT-247 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:85 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “это помогает мне выжить”; |
| V41-LINT-248 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:86 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “без этого я развалюсь”. |
| V41-LINT-253 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:135 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - не только “перестань искать утешение там”; |
| V41-LINT-254 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:136 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - но “увидь, что Христос даёт большее и истинное благо”. |
| V41-LINT-260 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:212 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - почему “я же решил больше так не делать” не всегда разрушает автоматическую реакцию; |
| V41-LINT-261 | 161_V21_SOURCE_VERIFIED_DEEPENING_PATTERNS_HEART.md:217 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Нельзя делать из этого основание учения о сердце. Нельзя говорить: “грех — просто автоматический cue-response”. Библейски грех — это не толь |
| V41-LINT-265 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:23 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если сердце лукаво, значит мне нельзя доверять вообще ничему в себе”. |
| V41-LINT-266 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:24 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если я во Христе, почему старое не исчезло?” |
| V41-LINT-267 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:25 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если реакция запускается быстрее, чем я успеваю подумать, виноват ли я?” |
| V41-LINT-268 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:26 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если это тянется с детства, есть ли надежда?” |
| V41-LINT-269 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:27 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если я борюсь десять лет, не доказывает ли это, что я лицемер?” |
| V41-LINT-273 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:66 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | 1. **Ложное благо:** “это даст мне мир / безопасность / контроль / удовольствие / признание”. |
| V41-LINT-277 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:113 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не говорить жертве: “твоя боль — просто твой грех”. |
| V41-LINT-278 | 162_V21_ARTICLE_CORE_PATTERNS_NOT_ALWAYS_CONSCIOUS.md:114 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не говорить грешнику: “твоё прошлое всё оправдывает”. |
| V41-LINT-287 | 163_V21_PASTORAL_DIAGNOSTIC_GRID_DEEP_PATTERNS.md:49 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | Не надо ломать человека фразой “это просто твой выбор”. Но и нельзя оставлять его под ложной идентичностью “я такой навсегда”. |
| V41-LINT-288 | 163_V21_PASTORAL_DIAGNOSTIC_GRID_DEEP_PATTERNS.md:116 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - говорит “я слабый”, но не хочет бдительности; |
| V41-LINT-289 | 163_V21_PASTORAL_DIAGNOSTIC_GRID_DEEP_PATTERNS.md:145 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | / Человек говорит “я такой” / ложная идентичность / фатализм / новая идентичность во Христе / |
| V41-LINT-290 | 163_V21_PASTORAL_DIAGNOSTIC_GRID_DEEP_PATTERNS.md:149 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не звучит ли мой текст как “всё объясняется детством”? |
| V41-LINT-291 | 163_V21_PASTORAL_DIAGNOSTIC_GRID_DEEP_PATTERNS.md:150 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не звучит ли мой текст как “детство не имеет значения”? |
| V41-LINT-292 | 163_V21_PASTORAL_DIAGNOSTIC_GRID_DEEP_PATTERNS.md:151 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не звучит ли мой текст как “если реакция автоматическая, человек не отвечает”? |
| V41-LINT-293 | 163_V21_PASTORAL_DIAGNOSTIC_GRID_DEEP_PATTERNS.md:152 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - Не звучит ли мой текст как “если человек долго борется, он точно лицемер”? |
| V41-LINT-295 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:43 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | “Я так устроен, значит ничего нельзя сделать” не понимает, что цепь привычного греха не является богом, судьбой или сущностью человека. |
| V41-LINT-300 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:114 | EDITORIAL_EXAMPLE_QUOTATION_OK_BUT_STYLE_REVIEW | Когда человек говорит: “Если я всё ещё борюсь, значит я не изменился”, статья должна ответить: |
| V41-LINT-303 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:130 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - сердце в тексте берётся не узко как орган или эмоции, а как “whole soul / inner man”; |
| V41-LINT-304 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:137 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | v21 уже сказал: “сердце не только выбирает; сердце привыкает”. Flavel добавляет: |
| V41-LINT-307 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:170 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Да, это плохо, но сейчас особый случай”. |
| V41-LINT-308 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:171 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Я не грешу, я просто восстанавливаюсь”. |
| V41-LINT-309 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:172 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Мне нужно это, иначе я сорвусь ещё хуже”. |
| V41-LINT-310 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:173 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Бог понимает, через что я прошёл”. |
| V41-LINT-311 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:174 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Это не похоть/контроль/гордость, это просто потребность”. |
| V41-LINT-312 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:175 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Я уже столько страдал, мне можно”. |
| V41-LINT-314 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:185 | EDITORIAL_EXAMPLE_QUOTATION_OK_BUT_STYLE_REVIEW | При душепопечении нельзя спрашивать только: “Ты понимаешь, что это грех?” Иногда человек понимает. Нужны более глубокие вопросы: |
| V41-LINT-316 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:205 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - почему место, время, усталость, экран, одиночество, музыка, маршрут, запах, переписка, конкретный человек или конфликт запускают старую ре |
| V41-LINT-317 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:214 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Грех — это автоматический механизм”. |
| V41-LINT-318 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:215 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Если реакция контекстно запускается, вина исчезает”. |
| V41-LINT-319 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:216 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Главное — перепрошить привычку”. |
| V41-LINT-320 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:217 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | - “Духовная борьба равна habit redesign”. |
| V41-LINT-322 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:229 | ATTRIBUTED_QUOTATION_REQUIRES_PRIMARY_CHECK | / Augustine, `Confessions VIII` / цепь воли, желания, привычки, рабства / “как сердце становится второй природой” / романтизировать опыт или |
| V41-LINT-323 | 164_V22_SOURCE_VERIFIED_AUGUSTINE_DORT_AMES_HABIT.md:230 | QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY | / Canons of Dort III/IV / новое сердце, действенная благодать, обновлённая воля / “почему техника не спасает” / перегрузить статью догматико |


---

## ORIGINAL_FILE: `271_V42_NEXT_BATCH_QUEUE_357_AMBIGUOUS_QUOTES.md`

# v42 — очередь следующей проверки: 357 ambiguous quotation marks

После закрытия 22 attributed lines остаётся самая большая группа: **357 строк `QUOTATION_MARKS_REVIEW_FOR_AMBIGUITY`**.

## Что это такое

Это строки, где есть кавычки, но пока не ясно, что именно они обозначают:

- название труда;
- термин;
- русскую разговорную формулу;
- внутренний авторский тезис;
- реальную цитату;
- пример речи/пастырского диалога.

## Приоритеты batch 3

1. Все ambiguous строки, где рядом есть имена: Owen, Charnock, Edwards, Flavel, Boston, Sibbes, Brooks, Watson, Perkins, Calvin, Chalmers, Augustine, Baxter.
2. Все строки с blockquote `>` в source-files, где читатель может подумать, что это цитата автора.
3. Все русские формулы с кавычками: “сердце говорит”, “я просто такой”, “это не грех” и т. п. Их надо помечать как illustrative speech, not quote.
4. Все строки, где кавычки вокруг английских терминов. Их можно оставить как terms, но не как citations.

## Предлагаемое правило переписывания

Плохо:

> “Сердце редко говорит: я выбираю зло как зло...”

Лучше:

**Авторский тезис:** сердце чаще оправдывает зло, чем называет его злом.

Плохо:

Owen говорит, что сердце “ведёт переговоры”.

Лучше:

Owen предупреждает: **"Entertain no parley, no dispute with it"** — и уже после этого мы можем объяснить по-русски: не вступай с искушением в переговоры.

Полная очередь: `data/v42_357_ambiguous_queue_prioritized.csv`.


---

## ORIGINAL_FILE: `276_V45_HIGH_RISK_19_CLOSED_AND_NEXT_QUEUE.md`

# v45 — HIGH-RISK 19 CLOSED AND NEXT QUEUE

This layer follows v44 and closes the remaining **19 HIGH priority** items from `v44_remaining_editorial_risk_queue.csv`.

## Result

- HIGH priority before v45: **19**.
- HIGH priority after v45: **0 unresolved HIGH**.
- Most HIGH rows were Scripture references or Scripture-like Russian wording. They are now governed by a strict Bible-edition policy.
- Two non-Scripture rows were source summaries:
  - John Owen, `Indwelling Sin`: keep as analytical summary unless exact locator and edition are supplied.
  - Thomas Watson, `All Things for Good / A Divine Cordial`: quote only from a chosen source/edition.

## New working rule

A biblical or Puritan phrase may enter the final article in only three ways:

1. **Exact quote** — author/work/edition/location/source URL are present.
2. **Reference only** — verse, chapter, article, or section is named, but no quotation marks are used.
3. **Analytical summary** — clearly our own words, no quotation marks, no blockquote styling.

## Files added in v45

- `data/v45_high_priority_19_closed.csv`
- `data/v45_801_queue_with_high_closed.csv`
- `data/v45_risk_priority_counts_after_high_closure.csv`
- `data/v45_deepened_quote_anchors.csv`
- `data/v45_web_verification_sources.csv`
- `data/v45_scripture_translation_policy.csv`
- `276_V45_HIGH_RISK_19_CLOSED_AND_NEXT_QUEUE.md`
- `277_V45_SCRIPTURE_QUOTE_EDITION_POLICY.md`
- `278_V45_DEEPENED_PRIMARY_LOCATORS_PURITANS.md`
- `279_V45_ARTICLE_READY_EXACT_QUOTE_PROTOCOL.md`
- `280_V45_NEXT_DEEPENING_QUEUE_AFTER_HIGH_CLOSURE.md`
- `tools/v45_quote_guard.py`


---

## ORIGINAL_FILE: `280_V45_NEXT_DEEPENING_QUEUE_AFTER_HIGH_CLOSURE.md`

# v45 — Next deepening queue after HIGH closure

After closing the 19 HIGH rows, the next useful work is not another broad topic but targeted source work.

## Priority 1 — convert MEDIUM internal blockquotes

Many MEDIUM rows are authorial Russian theses in blockquotes. They should be rewritten as normal prose or explicitly labelled `Авторский тезис`, not left as pseudo-citations.

## Priority 2 — section-level Perkins and Baxter

Open and extract exact section locators for:

- Perkins on assurance / distressed conscience / good conscience.
- Baxter on temptation / speech / senses / recreation / self-examination.

## Priority 3 — Goodwin edition check

For `The Heart of Christ`, choose one edition/source and build a small exact quote bank with OCR cautions.

## Priority 4 — Boston page-level check

Boston is highly valuable for four states and corrupted faculties, but final article quotes need page/section locator.

## Priority 5 — Scripture edition unification

Pick the default Russian Bible edition for the site. Until then, prefer references over exact wording.


---

## ORIGINAL_FILE: `281_V46_MEDIUM_QUEUE_CLOSED_AND_WEB_DEEPENING.md`

# V46 — Medium Queue Closed / Web Verification Deepening

Date: 2026-06-25

## Purpose

V45 closed the 19 HIGH-risk rows. V46 closes the 590 MEDIUM-risk rows by editorial function and deepens the source layer with web-verified locator anchors.

The point is not to pretend that every line became a usable external quotation. The point is to stop treating internal Russian formulations as quotations and to reserve quotation styling for exact, source-located text.

## Result

- HIGH already closed in v45: 19.
- MEDIUM closed in v46: 590.
- LOW remaining for final style pass: 192.

## Medium closure logic

1. Internal author theses are not quotations.
2. Internal diagnostic phrases are not quotations.
3. Internal case voices are not quotations.
4. Editorial examples may retain quotation marks only as examples, not as attributed source quotations.
5. Source summaries remain summaries unless replaced by exact source text.

## Core editorial rule

Do not make a sentence look like a quote unless it is an exact quote with author, work, source, locator, and edition/translation status.



---

## ORIGINAL_FILE: `285_V46_REMAINING_LOW_RISK_QUEUE_AND_NEXT_STEP.md`

# V46 — Remaining Low-Risk Queue

After v46 the remaining 192 rows are LOW-risk.

They are not priority source-verification problems. They are final editorial cleanup issues:

- table prose,
- internal labels,
- file titles,
- obvious internal summaries,
- non-attributed style quotations,
- low-risk formatting remnants.

## Next recommended batch

V47 should not keep digging randomly. It should either:

1. do a final low-risk cleanup pass, or
2. start building the first real article draft using only verified source anchors.

Best next move for quality: begin an article module and enforce the v46 quote protocol while writing.


---

## ORIGINAL_FILE: `286_V47_FULL_801_QUOTE_QUEUE_CLOSED.md`

# V47 — Full Quote Queue Closed: 801/801

Date: 2026-06-25

## Purpose

This is the final closeout of the 801 quote-lint queue that began in v40/v41.

V45 closed the HIGH-risk rows, v46 closed the MEDIUM-risk rows, and v47 closes the remaining LOW-risk rows.

## Final count

| Queue | Count | Final status |
|---|---:|---|
| HIGH-risk | 19 | CLOSED in v45 |
| MEDIUM-risk | 590 | CLOSED in v46 |
| LOW-risk | 192 | CLOSED in v47 |
| Total | 801 | CLOSED |

## What “closed” means

Closed does not mean every line is an external quotation. It means every line now has a safe editorial classification:

- exact quotation anchor,
- Bible quote/reference requiring edition if quoted,
- internal author thesis,
- diagnostic phrase,
- case voice,
- source summary,
- filename/title/label,
- style-only row.

## Publication rule

No line from the archive may be published as a quotation unless it has exact wording, author, work, source, locator, and edition/translation status.



---

## ORIGINAL_FILE: `287_V47_LOW_RISK_192_CLOSED_AUDIT.md`

# V47 — Low-Risk 192 Closed Audit

The remaining 192 LOW-risk rows were not unresolved source problems. They were style-only or low-risk editorial items.

## Main categories

- Internal prose/table lines.
- File titles and internal labels.
- Exact anchors already available.
- Editorial meta-rules.
- Bible references that require an edition only if quoted directly.
- Keywords/search queries/terms.
- Confession references that need chapter/paragraph if quoted.

## Required article handling

1. Internal prose must not be formatted as blockquote.
2. Titles and filenames should be in code or italics, not source-quote formatting.
3. Bible quotations must specify the translation/edition.
4. Confessional quotations must specify chapter/paragraph and edition.
5. Existing exact anchors may be used only in their short verified form.
6. Search queries and keywords are not citations.

## Conclusion

The 192 LOW rows are closed as source-risk. They remain only as final editorial polish before article publication.
