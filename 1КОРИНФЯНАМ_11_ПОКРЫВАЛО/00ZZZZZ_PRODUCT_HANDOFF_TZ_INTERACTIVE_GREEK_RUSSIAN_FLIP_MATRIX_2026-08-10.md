# ТЗ / Product handoff — интерактивная греко-русская матрица 1 Кор. 11:2–16

**Дата:** 2026-08-10  
**Статус:** `PRODUCT-HANDOFF-SPEC / RESEARCH-DERIVED / NOT-IMPLEMENTATION / DO-NOT-BUILD-IN-RESEARCH`  
**Источник идеи:** пользовательский UX-концепт: русский текст первым слоем, греческий оригинал на «перевороте» как на начальной странице «Господь Бог — сила моя»; компактное окно, раскрывающееся в большой аналитический режим; визуально показывать, что к чему относится.

## 1. Граница этой работы

Этот файл **не является UI-разработкой** и не разрешает Product write. Его задача — сохранить идею и необходимые research-contracts так, чтобы отдельный Product/UX агент позднее мог спроектировать реализацию без повторного изобретения исследовательской модели.

```text
RESEARCH_NOW = true
UI_IMPLEMENTATION_NOW = false
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
```

---

## 2. Смысл продукта

Нужен не декоративный chart, а **интерактивный исследовательский инструмент**, позволяющий человеку визуально увидеть структуру 1 Кор. 11:2–16:

- какие слова и фразы составляют аргумент;
- какие элементы зависят друг от друга;
- где текст говорит прямо, а где начинается интерпретация;
- какие альтернативные прочтения относятся именно к конкретному греческому узлу;
- где Павел вводит creation-order аргумент, где его балансирует взаимозависимостью, где появляется `ἐξουσία`, где `ангелы`, где `φύσις`, где финальный `συνήθεια`;
- как русский перевод соотносится с греческим текстом, не маскируя неоднозначность оригинала.

---

## 3. Базовая UX-идея, которую надо сохранить

### 3.1 Первый слой — русский

По умолчанию пользователь видит качественный русский исследовательский перевод/сегментацию. Русский слой — основной для чтения.

### 3.2 Flip / разворот — греческий

Каждый стих или смысловой сегмент должен уметь **переворачиваться** тем же типом взаимодействия, который уже используется/задуман на начальной странице проекта «Господь Бог — сила моя»:

- front: русский;
- back: греческий оригинал;
- не заменять flip обычным tooltip, если Product-дизайн позволяет сохранить знакомый эффект бренда;
- при развороте структура соответствий должна оставаться понятной: пользователь должен видеть, какой русский сегмент соответствует какому греческому.

### 3.3 Компактный и расширенный режим

На основной странице инструмент может быть небольшим компактным окном/виджетом, чтобы не захватывать весь экран.

По действию пользователя он раскрывается в **большой аналитический режим** (modal/fullscreen/expanded panel — конкретная реализация решается отдельным Product агентом).

В большом режиме должно быть достаточно пространства для:

- текста;
- связей между фразами;
- competing interpretations;
- confidence labels;
- source/evidence drill-down.

---

## 4. Что должно быть наглядно, а не просто перечислено

Главный критерий качества: **видно, что к чему относится**.

Например:

- `κεφαλή` в 11:3 связано с тремя парами отношений, но значение слова нельзя визуально подменять заранее русским «начальник» или «источник»;
- `κατὰ κεφαλῆς ἔχων` / `ἀκατακαλύπτῳ τῇ κεφαλῇ` в 11:4–5 связаны с covering/hair debate;
- vv.7–9 должны быть визуально связаны с Genesis reasoning;
- `διὰ τοῦτο` в 11:10 должно показывать, к какому аргументу оно возвращается;
- `ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς` должно быть отдельным disputed node;
- `διὰ τοὺς ἀγγέλους` — отдельный unresolved semantic/referential node;
- `πλὴν ... ἐν κυρίῳ` vv.11–12 должен визуально показывать counterbalance/interdependence;
- `ἡ φύσις αὐτή` vv.13–15 — отдельный node с biological/custom/naturalized-propriety debate;
- `τοιαύτην συνήθειαν` v.16 — отдельный node: что именно обозначает «такой обычай».

Не делать линейные стрелки там, где связь спорна. Спорная связь должна быть визуально отличима от прямой синтаксической связи.

---

## 5. Research authority contract для будущего Product

Product не должен выбирать «самый новый по имени файл» или хранить snapshot grades внутри этого ТЗ.

```text
00_CURRENT_INDEX_1COR11.md = NAVIGATION_AUTHORITY
CURRENT_CLAIM_REGISTRY = GRADE_AUTHORITY
SEGMENT_LEVEL_RELATION_MAP = RELATION_TYPE_AUTHORITY
VERSE_BY_VERSE_ADVERSARIAL_AUDIT = EXPLANATORY_PROSE_OWNER
THEMATIC_CANONICAL_AUDIT_OR_EVERGREEN_DOSSIER = EVIDENCE_OWNER
PRODUCT_HANDOFF_SPEC = UX_AND_DATA_CONTRACT_ONLY
```

```text
PRODUCT_HANDOFF_SPEC != GRADE_AUTHORITY
FILENAME_RECENCY != AUTHORITY
MORE_Z_CHARACTERS != MORE_CURRENT
DEPRECATED_POINTER != CURRENT_GRADE_SOURCE
```

При будущей реализации grades и relation types должны считываться/переноситься из **актуальных controlling owners**, а не из старого примера в ТЗ.

---

## 6. Research data contract для будущего Product

Каждый стих/сегмент должен иметь машинно-пригодные поля примерно следующего класса:

```text
verse_id
segment_id
greek_text_authority
greek_segment
russian_research_rendering
morphology
syntax_relation
relation_type
semantic_node
cross_reference
leading_reading
strongest_alternative
edge_readings[]
exact_research_grade
grade_authority
relation_authority
historical_background
source_ids[]
source_provenance_class
body_status
page_image_status
negative_boundaries[]
publication_caution
```

Ключевое разделение:

```text
RELATION_TYPE != CLAIM_GRADE
SOURCE_IDENTITY_CLOSED != BODY_READ
PDF_TEXT_LAYER_READ != PAGE_IMAGE_AUTOPSY
BACKGROUND_FACT_GRADE != EXACT_EXEGETICAL_TRIGGER_GRADE
```

Например, Roman `capite velato` может быть **A-level historical background**, тогда как связь этого фона с точным смыслом v4 остаётся **B_C**, а конкретный Corinthian trigger — reconstruction-layer. Product не должен сводить эти три уровня в одну стрелку с одним цветом.

Конкретный JSON/schema проектируется позднее; Research сейчас должен производить информацию так, чтобы её можно было перенести без ручного пересобирания смыслов.

---

## 7. Текстовая база оригинала

Для будущего Product слоя использовать **актуальную критическую текстовую authority**, а не случайную web-копию.

На 2026-08-10:

- GNT6 официально опубликован и издатель называет его самым актуальным текстом греческого NT;
- текст GNT6 идентичен тексту будущего NA29;
- NA29 официально заявлен к выпуску 2027-02-28;
- перечисленные издателем новые ECM-driven изменения GNT6 относятся к Acts (2017), Mark (2021), Revelation (2025); не заявлять отдельную завершённую Pauline ECM.

Источники:
- https://shop.die-bibel.de/Greek-New-Testament-GNT6.-Standardausgabe/5310
- https://shop.die-bibel.de/Novum-Testamentum-Graece-NA29./5320

**Важно:** Product должен отдельно решить licensing/display rights для выбранного критического текста. Research не даёт автоматического права публиковать редакционный apparatus или большие защищённые издательские фрагменты.

---

## 8. Перевод

Русский front-layer не должен просто копировать один современный перевод там, где это скрывает спор.

Нужны два уровня:

1. читабельная русская формулировка;
2. исследовательская помета/альтернативный rendering для узлов, где перевод уже является интерпретацией (`κεφαλή`, `ἐξουσία`, covering constructions, `φύσις`, `συνήθεια`).

Product-слой не должен вставлять в основной перевод слово/объект, которого Greek node прямо не называет, без маркировки интерпретационного шага.

---

## 9. Confidence visualization

Research использует не только грубые `A/B/C/D`, но и точные подклассы (`B_HIGH`, `B_HIGH_LEADING`, `B_C`, `C_SERIOUS_ALTERNATIVE`, `C_LOW`, `D_C_LOW`, `HOLD` и т.п.).

```text
DATA_LAYER_MUST_PRESERVE_EXACT_RESEARCH_GRADE = true
UI_MAY_GROUP_GRADES_FOR_READABILITY = true
UI_GROUPING_MUST_NOT_OVERWRITE_STORED_EXACT_GRADE = true
```

Визуально Product может группировать их в понятные семейства:

- A — direct/high;
- B — probable/leading;
- C — possible/serious alternative;
- D — speculative/history-of-interpretation;
- HOLD — требуется прямой источник/locator.

Но интерфейс **не должен превращать A/B/C/D в рейтинг богословских лагерей**. Grade относится к конкретному claim, а не к человеку/конфессии.

Также нельзя визуально присваивать grade самой связи, если grade относится к **claim node**, а relation type описывает другой аспект данных.

---

## 10. Обязательные interaction-сценарии для отдельного Product агента

Зафиксировать как требования, не как текущую реализацию:

- flip русский ↔ греческий;
- компактный вид ↔ expanded analytical view;
- клик по disputed word/phrase → только относящиеся к нему readings/evidence;
- возможность подсветить связи одного аргументного слоя (headship / covering / creation / authority / angels / nature / custom);
- возможность увидеть strongest alternative без ухода на другую страницу;
- source drill-down без захламления основного текста;
- отдельное отображение `direct source body`, `metadata/locator`, `page-image HOLD` там, где это важно для provenance;
- negative boundary должен быть доступен рядом с tempting-but-invalid inference;
- mobile-first readability и отдельная desktop matrix;
- accessibility: flip не должен быть единственным способом получить обратную сторону; keyboard/screen-reader equivalent обязателен.

---

## 11. Анти-требования

Не делать:

- красивый граф без exegetical semantics;
- автоматические стрелки, которые выдают спорную интерпретацию за синтаксический факт;
- один «правильный перевод» спорных слов без возможности увидеть original node;
- перегруженную богословскую mind-map на первом экране;
- анимацию ради анимации;
- Product реализацию из Research-ветки;
- перенос grades из PR body, старого pointer-файла или этого ТЗ вместо controlling registry;
- превращение `source exists` в `source body read`;
- превращение `historical background = A` в `exact Pauline trigger = A`.

---

## 12. Current Research prerequisite state

Постиховый adversarial audit и segment-level relation map уже существуют как текущий Research baseline. Они **не делают исследование publication-ready** и могут обновляться при новых direct sources.

```text
VERSE_AUDIT_BASELINE = COMPLETE
SEGMENT_RELATION_MAP_BASELINE = COMPLETE
CURRENT_CLAIM_REGISTRY = LIVE_GRADE_AUTHORITY
PUBLICATION_READY = false
PUBLICATION_HOLD = true
```

Перед отдельным Product-design этапом Product-агент обязан:

1. прочитать `00_CURRENT_INDEX_1COR11.md`;
2. получить current claim registry;
3. получить current segment relation map;
4. разрешить source owners для спорных nodes;
5. проверить, что Research branch/authority contract не был superseded.

Именно **актуальные controlling Research owners**, а не визуальная фантазия дизайнера и не snapshot этого handoff-файла, должны стать semantic source of truth для будущей матрицы.
