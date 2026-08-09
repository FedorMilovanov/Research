# Итог интеграции параллельных корпусов и канонический индекс

**Дата:** 9 августа 2026
**Статус:** `INTEGRATED / SINGLE-CANONICAL-FOLDER / RESEARCH-ONLY`
**Ветка:** `arena/019fe62b-research`

---

## 1. Что сделано

В ветке параллельно работали несколько агентов. После синхронизации с `origin/arena/019fe62b-research` обнаружились два корпуса по 1 Кор. 11:

1. `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/` — каноническая папка, объявленная в `00A_PARALLEL_FOUNDATION_MERGE_NOTE`.
2. `СЕРИЯ 1 КОРИНФЯНАМ 11/` — параллельный корпус агента Б (17 досье + папка `ИСТОЧНИКИ/` с выверенными цитатами).

Произведена консолидация:

### 1.1. Перенесены уникальные цитаты в `SOURCE_LIBRARY/processed/1COR11_PRIMARY/`

Из `СЕРИЯ 1 КОРИНФЯНАМ 11/ИСТОЧНИКИ/`:

- `КОММЕНТАТОРЫ_ШРЕЙНЕР_RBMW_ГЛАВА5_ЦИТАТЫ.md` → `classical_conservative/` (полная глава RBMW 5, 119 строк проверенных цитат)
- `КОММЕНТАТОРЫ_ЭЛЛИКОТТ_ЦИТАТЫ.md` → `classical_conservative/`

Остальные 10 файлов источников уже были идентичны по md5 с версиями в SOURCE_LIBRARY, их удаление не требуется.

### 1.2. Перенесены уникальные досье агента Б как supplements 19–31

В каноническую папку перенесены:

| Файл агента Б | Канонический файл |
|---|---|
| 00_EVIDENCE_LEVELS... | 19_EVIDENCE_LEVELS_AND_CLAIM_CALIBRATION_STANDARD |
| 00_SCOPE_AND_BOUNDARIES | 20_SCOPE_AND_BOUNDARIES |
| 00_SOURCE_WEIGHT... | 21_SOURCE_WEIGHT_AND_ACQUISITION_PLAN |
| 03_COMMENTATOR_LANDSCAPE | 22_COMMENTATOR_LANDSCAPE |
| 04_QUESTION_MATRIX... | 23_QUESTION_MATRIX_AND_CLAIM_LEDGER |
| 05_ADVERSARIAL... | 24_ADVERSARIAL_AND_LIBERAL_READINGS |
| 06_PATRISTIC_PRIMARY... | 25_PATRISTIC_PRIMARY_SOURCES |
| 07_APPLICATION_DEBATE | 26_APPLICATION_DEBATE |
| 08_LOGIC_AND_RHETORIC | 27_LOGIC_AND_RHETORIC |
| 09_VERSE_BY_VERSE... | 28_VERSE_BY_VERSE_EXEGESIS |
| 10_Q7_11_5_VS_14_34 | 29_WOMEN_PRAYING_VS_1COR14_34 |
| 11_OT_JEWISH_BACKGROUND | 30_OT_AND_JEWISH_BACKGROUND_SUPPLEMENT |
| 00_PARALLEL_CORPUS_COORDINATION | 31_PARALLEL_CORPUS_COORDINATION |

### 1.3. Удалены дубликаты

- Папка `СЕРИЯ 1 КОРИНФЯНАМ 11/` удалена целиком (после переноса всего уникального).
- Удалён мой старый дубль `07_CORINTH_HISTORICAL_CONTEXT_ROMAN_COLONY_VEILING_2026-08-09.md`, который дублировал канонический `09_CORINTH_HISTORICAL_CONTEXT`.
- README обновлён: снят устаревший тег `NO-PUSH`, указан канонический вход, отражены оба корпуса.

### 1.4. Проверены дубли внутри канонической папки

После слияния остались сознательно не слитые пары с разных агентов, которые нужно будет синтезировать в следующей фазе:

| Тема | Канонический файл | Supplement |
|---|---|---|
| Греческий текст | 06_GREEK_TEXT_AND_APPARATUS | (дубль моего файла удалён) |
| Kephale | 07_KEPHALE_LEXICON | (мой дубль удалён) |
| История/Коринф | 09_CORINTH_HISTORICAL_CONTEXT | 07_* удалён, дополнения в 09_PRIMARY |
| ВЗ/еврейский фон | 04_OT_AND_JEWISH_BACKGROUND_DOSSIER | 30_OT_AND_JEWISH_BACKGROUND_SUPPLEMENT |
| Логика/риторика | 08_LOGIC_AND_RHETORIC | 27_LOGIC_AND_RHETORIC (мой дубль удалён) |
| Муж/жена покрытие | 11_COVERING_MEN_WOMEN_HAIR_VEIL_SHAME | 09_* (близкий, требует синтеза) |
| Патристика | 12_PATRISTIC_REFORMATION_HISTORY | 17_PATRISTIC_HISTORY_SUPPLEMENT, 25_PATRISTIC_PRIMARY |
| Адверсариал | 13_ADVERSARIAL_AND_LIBERAL | 24_ADVERSARIAL_AND_LIBERAL |
| Применение | 18_MODERN_APPLICATION | 26_APPLICATION_DEBATE |
| Exousia/ангелы | (отдельный файл агента Б) | 14_EXOUSIA_AND_ANGELS_SUPPLEMENT |
| Physis/волосы | (в каноне нет отдельного) | 15_NATURE_HAIR_PERIBOLAIOS_SUPPLEMENT |
| Матрица комментаторов | 22_COMMENTATOR_LANDSCAPE | 16_COMMENTATORS_MATRIX_SUPPLEMENT |
| 11:5 vs 14:34 | 10_PRAYER_PROPHECY_AND_1COR14_34 | 29_WOMEN_PRAYING_VS_1COR14_34 |

---

## 2. Текущий канонический список файлов

```text
1КОРИНФЯНАМ_11_ПОКРЫВАЛО/
  00_README_FOUNDATION_OPEN_2026-08-09.md             — основной entrypoint
  00A_PARALLEL_FOUNDATION_MERGE_NOTE_2026-08-09.md     — заметка о слиянии агентов
  01_SOURCE_ACQUISITION_PLAN.md                        — базовый план источников
  01B_BOOK_ACQUISITION_PRIORITY_QUEUE_SUPPLEMENT       — очередь книг агента Б
  02_CLAIM_LEDGER_TEMPLATE_AND_POSITIONS.md            — реестр тезисов
  03_PRODUCT_SITE_STYLE_AND_SERIES_CONTRACT             — стиль будущего сайта
  04B_MASTER_SOURCE_LEDGER_SUPPLEMENT                  — master ledger (130+ записей)
  04_OT_AND_JEWISH_BACKGROUND_DOSSIER.md               — ВЗ/еврейский фон
  04_SOURCE_CARDS_AND_LOCATOR_REGISTRY                 — карточки источников
  05_BRANCH_STATE_AND_PARALLEL_AGENT_ANTI_DUPLICATION
  06_GREEK_TEXT_AND_APPARATUS_1COR11_2_16.md           — греческий текст
  07_KEPHALE_LEXICON_THEOLOGY_AND_CHRISTOLOGY.md       — κεφαλή
  08_LOGIC_AND_RHETORIC_OF_1COR11_2_16.md             — логика/риторика
  09_CORINTH_HISTORICAL_CONTEXT_ROMAN_COLONY_VEILING.md — Коринф
  09_PRIMARY_CLASSICAL_AND_JEWISH_SOURCES_ON_VEILING.md — первоисточники
  10_PRAYER_PROPHECY_AND_1COR14_34_RECONCILIATION.md   — 11:5 vs 14:34
  11_COVERING_MEN_WOMEN_HAIR_VEIL_SHAME.md             — ткань/волосы/честь
  12_PATRISTIC_REFORMATION_HISTORY_OF_INTERPRETATION.md — патристика/Реформация
  13_ADVERSARIAL_AND_LIBERAL_READINGS_DOSSIER.md       — контраргументы
  14-31 — supplements (exousia/ангелы, природа, комментаторы, применение и т.д.)
```

Полный текст первоисточников: `SOURCE_LIBRARY/processed/1COR11_PRIMARY/` — 15 файлов (ANF, классика, консервативные цитатники).

---

## 3. Что уже установлено по существу (консервативный центр)

1. **Текст аутентичен** (P46 и все основные свидетели; Walker/Cope отвергаются).
2. **Покрытие реальное**, не только духовное; вероятнее всего шаль/накидка, а не полная чадра; волосы — природный знак, не замена.
3. **`κεφαλή`** в этом контексте = authority/headship с измерением источника; Грудем 2336 примеров; контраргументы Сервина/Фицмайера учтены.
4. **`ἐξουσία` в 11:10** грамматически активна (женщина имеет власть/право покрыть голову), но большинство консерваторов толкует как знак власти мужа; обе позиции требуют честного изложения.
5. **Ангелы** — вероятнее всего святые ангелы-свидетели богослужения; линия падших ангелов Быт. 6 (Тертуллиан, Элликотт) — древняя, но не прямая.
6. **Женщины молятся и пророчествуют** в собрании (11:5 прямо), вопрос с 14:34 решается через различие контекстов.
7. **Природа** (11:14) = врождённое чувство приличия + культурное проявление; не буквально «длина в сантиметрах».
8. **Применение сегодня**: вечный принцип (главенство, различие полов, благопристойность) и культурная форма знака.

---

## 4. Следующие фазы

- **Фаза 2 (синтез):** свести пары дублей (08/27, 12/17/25, 13/24, 18/26, 11/... и 04/30) в единые файлы без потери контента.
- **Фаза 3 (приобретение P0):** Garland BECNT, Thiselton NIGTC, Fee NICNT, Ciampa/Rosner PNTC, Schreiner ESVEC, Winter обе книги, Oster NTS 1988 — точные страницы.
- **Фаза 4 (claim ledger):** пройти по матрице вопросов Q1–Q8 и присвоить каждому уровни уверенности с опорой на имеющиеся цитаты.
- **Фаза 5 (продукт):** lane record в gb-is-my-strength, hub в `/hard-texts/`, статьи в `/articles/` — по образцу серии «Сердце» и «Бытие 6».

Research остаётся research-only; никаких продуктовых мутаций не делается.
