# Том 69. Глоссарий серии о Джоне Гилле: определения, падежи, размещение, частота и регрессионный контракт

Дата: 23 июля 2026 года.

## Задача

Проверить не отдельные красивые тултипы, а всю систему терминов серии о Джоне Гилле:

- какие определения отсутствуют;
- насколько определения исторически нейтральны и точны;
- распознаются ли русские падежи и множественные формы;
- где тултипы вообще допустимы;
- как часто один термин может появляться повторно;
- не попадают ли определения в краткие карточки, таблицы, примечания и навигацию;
- разрешается ли каждый `data-term` в каноническую запись словаря;
- не приклеиваются ли скрытые определения к TTS и Pagefind.

---

# I. Текущее поведение runtime

`js/glossary.js` автоматически обходит текстовые узлы внутри `article` и гидратирует словарные термины.

Уже исключены:

- ссылки и существующие `abbr/.gterm`;
- code/pre/kbd/samp;
- nav;
- figcaption/caption;
- th/td;
- article header;
- author card;
- series navigation;
- article TOC;
- summary card;
- footnote/tooltip containers;
- headings;
- quizzes;
- hidden/Pagefind metadata.

TTS уже исключает `.gtip`, поэтому определение не должно приклеиваться к произносимому русскому тексту.

## Найденные системные недостатки

1. `.note-box`, `.context-bridge`, `.ancient-epigraph`, краткие fact cards и часть sidebar-блоков не запрещены.
2. Ручная разметка `.gterm/.gtip` может обойти автоматические запреты.
3. Повтор ограничен разницей в 40 индексированных абзацев. Это не учитывает реальную длину текста.
4. Падежи хранятся как ручной список aliases; нет теста полноты парадигмы.
5. Нет единого CI-теста “каждый термин существует, каждый alias однозначен, каждый tooltip находится в разрешённой зоне”.
6. Словарь общий для сайта, но многие определения написаны в жанре мини-проповеди; для исторической серии нужны более нейтральные brief definitions и отдельный contextual detail.
7. Нет отдельного поля `scope` или `usageNote`, которое различало бы общее значение термина и его использование у Gill.
8. Некоторые английские/латинские формы являются каноническими ключами, а русский текст — alias; заголовок tooltip может получаться неестественным.
9. Нет контроля омонимии: короткие слова вроде “канон”, “призвание”, “завет” могут гидратироваться в нерелевантном контексте.
10. Нет отчёта о терминах, которые встречаются в тексте серии, но отсутствуют в словаре.

---

# II. Новый контракт размещения

## Разрешённые зоны

Тултип разрешён только в основном объяснительном тексте:

- `<p class="reveal">`;
- `<p data-glossary-zone="prose">`;
- специально помеченный длинный абзац внутри обычного article body.

## Запрещённые зоны

Тултип не должен находиться или автоматически создаваться внутри:

- `.summary-card`;
- `.note-box`;
- `.context-bridge`;
- `.ancient-epigraph`;
- `.fact-card`, `.quick-fact`, `.key-point`, `.reading-list-section`;
- table/thead/tbody/tr/th/td/caption;
- figure/figcaption;
- nav, cards and series links;
- author card;
- timeline;
- TOC/rail/mobile navigation;
- hero/header;
- footnotes and citations;
- quiz;
- source lists;
- any `[data-glossary-skip]`.

## Обработка ручной разметки

Runtime должен:

1. найти `.gterm` в запрещённой зоне;
2. заменить оболочку обычным текстом, не удаляя видимое слово;
3. удалить вложенный `.gtip`;
4. записать предупреждение только в development/debug audit, а не в console production;
5. CI должен считать такую разметку ошибкой source-level.

---

# III. Новый контракт повторения

Существующее правило “не чаще чем через 40 абзацев” заменяется гибридным порогом.

Термин появляется:

1. при первом содержательном употреблении на странице;
2. затем только если одновременно прошло:
   - не менее 20 prose-блоков;
   - не менее 1 200 слов основного текста;
3. не более трёх раз на одной длинной статье;
4. для статей короче 3 000 слов — обычно один раз;
5. ручной `data-glossary-force="true"` допускается только для реального изменения значения, но фиксируется аудитом.

Причина: на странице из коротких абзацев 40 блоков могут составлять 600 слов, а на странице из длинных — 4 000–5 000. Гибридный порог лучше соответствует читательской памяти.

---

# IV. Канонические поля словаря

Для Gill-терминов рекомендуется структура:

```json
{
  "канонический термин": {
    "definition": "Краткое нейтральное определение.",
    "detail": "Расширение, история спора и употребление.",
    "usageNote": "Как термин употребляется в серии или у Gill.",
    "aliases": [],
    "category": "История церкви",
    "categorySlug": "church-history",
    "autoHydrate": true,
    "maxPerArticle": 2,
    "minWordGap": 1200,
    "minBlockGap": 20
  }
}
```

`usageNote` не должен подменять определение конфессиональной оценкой. Например, `hyper-Calvinism` сначала определяется историографически, а затем отдельной заметкой объясняется, почему классификация Gill спорна.

---

# V. Термины, необходимые для исторического введения

## Уже существуют, но требуют проверки/расширения aliases

### `диссентер`

Текущее определение в целом качественное, но формула “сознательно отделившийся” слишком узка: человек мог родиться в dissenting congregation и никогда лично не проходить акт отделения.

Новая краткая формула:

> Протестант в Англии, принадлежавший к церкви или религиозной традиции вне установленной Church of England.

Нужные aliases:

- диссентер;
- диссентеры;
- диссентера;
- диссентеров;
- диссентеру;
- диссентерам;
- диссентером;
- диссентерами;
- диссентерский;
- диссентерская;
- диссентерское;
- диссентерские;
- диссентерского;
- диссентерской;
- диссентерских;
- диссентерскому;
- диссентерским;
- диссентерскую;
- диссентерскими;
- диссентерстве;
- диссентерство;
- диссентерству.

### `нонконформист`

Нужно различать широкое употребление до/после 1662 и юридико-исторический контекст.

Aliases:

- нонконформист;
- нонконформисты;
- нонконформиста;
- нонконформистов;
- нонконформисту;
- нонконформистам;
- нонконформистом;
- нонконформистами;
- нонконформистский;
- нонконформистская;
- нонконформистское;
- нонконформистские;
- нонконформистского;
- нонконформистской;
- нонконформистских;
- нонконформизм;
- нонконформизма;
- нонконформизме.

### `sola scriptura`

Не автоматически гидратировать каждое употребление внутри Latin/English quotation or heading. Добавить русские aliases только если выражение реально переводится в прозе:

- только Писание;
- принцип «только Писание».

## Отсутствуют и должны быть добавлены

1. **установленная церковь / Established Church**
2. **Акт о веротерпимости / Toleration Act**
3. **религиозный тест**
4. **Кларендонский кодекс**
5. **конвентикула / conventicle**
6. **диссентерская академия**
7. **генеральные баптисты**
8. **партикулярные баптисты**
9. **особое искупление / particular redemption**
10. **общее искупление / general redemption**
11. **сепаратист**
12. **собранная церковь / gathered church**
13. **конгрегационализм**
14. **церковная подписка / confessional subscription**
15. **non-subscription / отказ от обязательной подписки**
16. **арианство**
17. **социнианство**
18. **унитарианство**
19. **вечное рождение Сына**
20. **реформатская ортодоксия**
21. **ковенантное богословие / covenant theology**
22. **федеральное богословие**
23. **доктринальный дрейф** — autoHydrate false; слишком оценочное выражение.
24. **методистское пробуждение / Evangelical Revival**
25. **поместная церковь**
26. **церковная ассоциация**
27. **рукоположение / ordination**
28. **раввинистика / rabbinics**
29. **Таргум**
30. **Мидраш**
31. **Мишна**
32. **Талмуд**
33. **Мемра / Memra**
34. **ориентальная литература** — историческое bibliographical usage, not modern geopolitical category.
35. **folio / фолио**
36. **amanuensis / писец-секретарь**

---

# VI. Термины, необходимые по всей серии Gill

1. **гиперкальвинизм**
2. **высокий кальвинизм / High Calvinism**
3. **duty-faith / обязанность спасительной веры**
4. **external call / внешний призыв**
5. **effectual calling / действенное призвание**
6. **free offer / свободное предложение**
7. **well-meant offer / благожелательное предложение**
8. **proclamation / провозглашение Евангелия**
9. **sensible sinner / пробуждённый грешник**
10. **вечное оправдание**
11. **имманентный акт**
12. **representative union / представительное единство во Христе**
13. **оправдание в совести**
14. **супралапсарианство**
15. **инфралапсарианство**
16. **антиномизм**
17. **неономизм**
18. **завет искупления / pactum salutis**
19. **завет благодати**
20. **частное искупление**
21. **ограниченное искупление**
22. **персеверанс / стойкость святых**
23. **отвержение / reprobation**
24. **двойное предопределение**
25. **Gillites**
26. **Fullerites**
27. **Strict Baptists**
28. **Gospel Standard**
29. **тринитарная ортодоксия**
30. **eternal generation**
31. **экономическая Троица**
32. **онтологическая Троица**
33. **экзегетический анахронизм**
34. **типология** — уже существует, проверить aliases.
35. **грамматико-исторический метод** — уже существует.
36. **католичность / catholicity**
37. **историография**
38. **первичный источник**
39. **позднее свидетельство**
40. **конфессиональная память**

---

# VII. Качество определений

## Требования к brief definition

- одно предложение;
- 16–36 слов;
- не повторяет сам термин как пустую тавтологию;
- не выносит спорный богословский приговор;
- объясняет, почему читателю нужно знать слово;
- согласуется с обычным русским синтаксисом после любого alias.

## Требования к detail

- 80–180 слов;
- происхождение или исторический контекст;
- граница термина: что он не означает;
- в спорных случаях — минимум две позиции;
- Scripture only when definition is genuinely theological, not as decorative proof-text;
- no raw long quotations;
- no “очевидно”, “несомненно”, “еретический” unless describing a named historical judgment.

## Проблемные стили текущего словаря

- devotional close (“Сердце всей темы…”) unsuitable for neutral historical terms;
- confessional judgments presented as dictionary facts;
- excessive proof-texting;
- canonical title in English while Russian inflection is clicked;
- detail repeats article content instead of orienting the reader;
- category sometimes too broad (“Богословие”) when “История церкви”, “Сотериология”, “Троица”, “Языки и иудаика” would be better.

---

# VIII. Падежный аудит

Для русского языка aliases must include not every mechanically possible word, but all forms actually used in production.

New audit script should:

1. scan Gill Astro components and rendered HTML;
2. normalize `ё/е`, punctuation and Unicode dashes;
3. collect visible word forms surrounding known lemmas;
4. report likely unmatched inflections;
5. report alias collisions;
6. report aliases shorter than four characters unless explicitly allowed;
7. verify longest-match precedence;
8. reject alias that crosses HTML boundaries or matches inside another word.

Examples:

- `диссентерской` is absent in current list though likely in prose;
- `нонконформизма`, `нонконформистской` need aliases;
- `партикулярно-баптистской` requires hyphen variants;
- `раввинистических`, `раввинистикой`, `раввинистике`;
- `гиперкальвинистской`, `гиперкальвинистами`, `гиперкальвинизма`;
- `ковенантного`, `ковенантной`, `ковенантную`;
- English hyphen variants `well-meant`, `well meant`, `free-offer`, `free offer`.

---

# IX. Регрессионные тесты

## `scripts/gill-glossary-contract-test.js`

Must fail when:

1. `.gterm` appears in a forbidden container;
2. `.gtip` is visible in static rendered HTML;
3. a `data-term` key does not exist;
4. an alias maps to multiple canonical entries;
5. a term repeats before both cadence thresholds;
6. a term exceeds `maxPerArticle`;
7. an explicit static tooltip conflicts with dictionary brief definition;
8. a tooltip exists in summary, table, source list or navigation;
9. a Gill component contains a likely technical term from the required registry but no dictionary entry exists;
10. TTS extraction includes `.gtip` text;
11. Pagefind includes detail text as article prose;
12. keyboard role/tabindex/aria attributes are missing after hydration.

## Browser test

On each of six Gill routes:

- hover/focus opens;
- Escape closes;
- click outside closes;
- “Подробнее” expands without jump;
- mobile touch opens once and does not activate neighbouring links;
- popover remains inside viewport;
- repeated occurrence follows the same canonical title;
- no tooltip inside quick summary, note box, table, footer or rail.

---

# X. Внедрение

Because `js/glossary.js`, `data/glossary.json` and shared tests affect the whole site, they should not be mixed into the content-only Gill PR.

Create a separate branch/PR:

`agent/gill-glossary-system`

Scope:

- readable source module or generated runtime for glossary hydration;
- dictionary entries and aliases;
- source-level contract test;
- browser regression test;
- package script and active CI linkage;
- no article rewrites except removal of manual `.gterm/.gtip` from forbidden Gill blocks.

The content PR may add `data-glossary-skip` markers or remove manual tooltips in Gill-only components, but shared runtime belongs in the dedicated system PR.

---

# XI. Definition examples

## `диссентер`

**Brief:**

> Английский протестант, принадлежавший к церкви или традиции вне установленной Church of England.

**Detail core:**

> Термин описывает положение относительно государственной церкви, а не одну деноминацию. Presbyterians, Congregationalists, Baptists and other Protestant groups could all be called Dissenters. After the Toleration Act of 1689 registered worship became lawful under conditions, but civil offices, university privileges and public trust remained separate questions. A person could be born into a dissenting congregation and never personally “separate” from Anglicanism.

## `нонконформист`

**Brief:**

> Протестант, не подчинившийся установленным требованиям богослужения, рукоположения или церковного управления Church of England.

**Usage note:**

> In post-1662 English history the word often focuses on refusal to conform to the restored settlement; it overlaps with “Dissenter” but is not a perfectly interchangeable legal term in every document.

## `партикулярные баптисты`

**Brief:**

> Английская баптистская традиция, соединявшая крещение верующих с реформатским учением об избрании и particular redemption.

**Boundary:**

> This was a network of congregations and confessional relationships, not a centralized denomination with one governing office.

## `non-subscription`

**Brief:**

> Отказ делать обязательную подпись под внебиблейской догматической формулой условием церковного доверия или совместного действия.

**Boundary:**

> At Salters’ Hall non-subscription did not by itself prove Arianism; orthodox non-subscribers existed.

## `well-meant offer`

**Brief:**

> Учение о том, что в евангельской проповеди Бог искренне предлагает Христа и спасение всем слушателям без исключения.

**Usage note:**

> Gill distinguished universal proclamation from this stronger claim and generally rejected offer-language while still directing hearers to Christ and assuring that believers will be saved.

---

# XII. Итог

The glossary should become a sparse reading aid, not a decorative layer. A reader needs a definition at the first difficult occurrence and perhaps once much later—not in every card, table and note. The system must treat morphology, source context and interface placement as one contract. Manual tooltip markup without dictionary and CI control is no longer acceptable for the Gill series.