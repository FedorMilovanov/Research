# Серия Джона Гилла — FINAL MASTER content / research audit


> **Финальный статус:** этот файл полностью включает V1–V11 и заменяет их как рабочий master-документ.  
> **Диапазон находок:** `GILL-CONTENT-001` — `GILL-CONTENT-480`.  
> **Объекты:** текущая серия `gb-is-my-strength` + отдел `FedorMilovanov/Research/Джон Гилл`.  
> **Production-код не изменялся.**


**Дата:** 2026-07-08  
**Repo:** `FedorMilovanov/gb-is-my-strength`  
**HEAD:** `d00715e95b45a32872aae7e00a3030b4c0bf5c12`  
**Фокус FINAL MASTER:** не chrome-меню, а текст статей, тултипы, глоссарий, research, источники, богословско-исторические риски.  
**Production-код не изменялся.**

---

# 0. Исправление предыдущего диагноза по A− / A+

Предыдущая формулировка была неточной:

> “A− и A+ — два самостоятельных элемента без общего блока, из-за чего они распадаются.”

Правильная формулировка:

> A− и A+ могут оставаться двумя самостоятельными кнопками. Ошибка не в том, что у них нет общего блока, а в возможном версточном разлёте / распределении расстояний / неудачной геометрии в конкретном viewport.

Этот UI-пункт **понижен** и не является предметом текущего content-audit. Дальше его не развиваем, чтобы не создавать путаницу.

---

# 1. Главная проблема content-аудита

Серия Гилла сейчас выглядит как сильный исследовательский материал, но часть текста живёт в промежуточном состоянии:

- местами академическая точность;
- местами популярно-эссеистические усиления;
- местами неподписанные “сильные” исторические утверждения;
- местами research claims стоят прямо в основном тексте без сноски;
- тултипы и глоссарий дают богословские определения, но не всегда связаны с источниками;
- часть тезисов подтверждается списком литературы внизу, но не конкретной inline-сноской рядом с утверждением.

Для публичного баптистского / реформатского сайта это особенно важно: Гилл — спорная фигура, и серия должна выдерживать не только визуальную, но и академическую атаку.

---

# 2. Структурная картина статей

## Part I

`GillPart1ArticleBody.astro` уже разбит на множество native-section компонентов: birth prophecy, education, conversion, pastor, family, Goatyard Declaration, daughter sermon, sources и т. д. Это хорошо для поддержки, но требует section-level audit, потому что каждый компонент теперь является отдельным носителем фактов.

Ключевой риск: `ArticleBody` просто импортирует sections подряд. Нет общего content-schema, которое задаёт:

- где нужен источник;
- где нужен tooltip;
- какие утверждения идут в quiz;
- какие утверждения идут в глоссарий;
- какие утверждения требуют primary-source strength.

## Part II

`GillPart2ArticleBody.astro` пока выглядит менее разрезанным: большой file содержит много крупных блоков подряд, включая Trinitarian controversy, rabbinic material, Song of Songs, Whitefield, covenant, degree, systematics, hyper-Calvinism и Habakkuk bridge.

Это повышает риск:

- дублей;
- слабых переходов;
- нелинейного TOC;
- повторения будущей Part IV;
- смешения “учёный” и “богословская система”.

## Part III

Part III особенно насыщена спорными тезисами: hyper-Calvinism, Spurgeon, Brown University, Bunhill, discipline over eternal generation, five definitions. Именно она требует самого жёсткого research-audit.

---

# 3. Source strength taxonomy

Для серии нужно ввести уровни доказательности.

## Level A — первичный / ранний источник

Примеры:

- Rippon, *A Brief Memoir*.
- Gill, конкретный трактат / sermon / commentary.
- Goat Yard Declaration 1729.
- Bunhill Memorials, если цитируется эпитафия.
- Brown institutional record, если утверждается donation.

Требование: рядом с сильным утверждением должна быть inline-сноска или source note.

## Level B — академическое исследование

Примеры:

- B. R. White.
- Haykin.
- Muller.
- Willis.
- Nettles.
- Clary.
- Glasgow PhD thesis 2025.

Требование: можно использовать для интерпретации, но не подменять первичное свидетельство, если утверждение фактическое.

## Level C — обзор / secondary popular

Примеры:

- London Lyceum overview.
- Baptist History Homepage.
- modern blog/essay.

Требование: не использовать как единственную опору для уникальных фактов.

## Level D — риторическое усиление

Фразы вроде:

- “никогда прежде и никогда после”;
- “единственный”;
- “безусловно крупнейшее”;
- “первое системное”;
- “главное историческое достижение”.

Требование: либо Level A/B source, либо смягчить.

---

# 4. Research findings

## GILL-CONTENT-001 — Glasgow thesis 2025 подтверждена официально

Part III ссылается на Ruth Macritchie, 2025, Glasgow thesis по Joseph Hussey, John Skepp, John Gill, John Brine.

Это подтверждается official Glasgow Enlighten page:

- автор: Ruth Macritchie;
- год: 2025;
- title: *A theological study of hyper-Calvinism in the writings of Joseph Hussey, John Skepp, John Gill, and John Brine*;
- PhD thesis, University of Glasgow;
- supervisor: Scott Spurlock;
- deposited 17 Jun 2025;
- DOI указан.

**Статус:** OK / подтверждено.

**Но:** если серия использует выводы диссертации, а не только факт её существования, нужно читать PDF и ссылаться на page/chapter, а не просто на карточку thesis.

---

## GILL-CONTENT-002 — Part III table по hyper-Calvinism требует footnote на каждую позицию

В таблице Part III перечислены Toon, Nettles, George, Haykin, Muller, Willis, Murray, Engelsma, Rathel, Macritchie. Это хороший формат, но сейчас выглядит как итоговая академическая карта без видимых inline references рядом с каждой строкой.

Риск:

- читатель не видит, где именно Toon сказал “главный архитектор”;
- где Rathel прямо связывает eternal justification и duty-faith;
- где Engelsma квалифицирует Gill;
- какие из формулировок — точные цитаты, а какие пересказ.

**Решение:** сделать колонку или tooltip “source” для каждой строки:

```text
Toon 1967, chapter/page
Nettles 1986, page
Haykin 2021, page
Muller 2003, page
Macritchie 2025, chapter/page
```

---

## GILL-CONTENT-003 — Part III использует свежий источник 2025 без статуса прочтения

Текст говорит:

> “Это первое системное сравнительное исследование всей четвёрки.”

Это сильное утверждение. Сам факт thesis подтверждён, но утверждение “первое системное” требует:

- либо авторского abstract/introduction;
- либо сравнения с Toon, Rathel, Murray и другими;
- либо смягчения.

**Исправить:**

```text
Новейшее доступное системное исследование ...
```

или:

```text
одно из первых специальных сравнительных исследований ...
```

Пока PDF не прочитан.

---

## GILL-CONTENT-004 — “Гилл стал единственным христианским гебраистом без университетского образования...” слишком сильное

Part II:

> “Гилл стал единственным христианским гебраистом без университетского образования, читавшим Талмуд как исследователь, а не как полемист.”

Это очень сильная формула. Она требует широкого сравнительного доказательства по всей европейской христианской гебраистике XVIII века.

**Риск:** почти наверняка слишком категорично.

**Лучше:**

```text
Гилл стал редким для английской баптистской среды примером самоучки-гебраиста, систематически работавшего с раввинистическими источниками не только полемически, но и экзегетически.
```

---

## GILL-CONTENT-005 — “беспрецедентно” по раввинистике требует смягчения

Part II:

> “Для христианина XVIII века это было беспрецедентно.”

Контекст реальный: Gill действительно необычен среди Particular Baptists, но христианская гебраистика до него уже имела Buxtorf, Lightfoot, Pococke, Schoettgen и др.

**Исправить:**

```text
Для баптистского пастора без университетского образования это было чрезвычайно необычно.
```

Так точнее и не вызывает ненужной атаки.

---

## GILL-CONTENT-006 — таблица раввинистических источников смешивает corpus и использование

Part II table:

```text
Талмуд Вавилонский — сопоставление цитат ВЗ с масоретским текстом
Талмуд Иерусалимский — исторический контекст апостольской эпохи
Мишна — еврейские обычаи новозаветного времени
Таргумы — идиомы Нового Завета
Мидраш — раввинистические методы
Зоар — критическое ознакомление
```

Проблема: это выглядит как точная карта Gill usage, но без examples/pages.

**Решение:** добавить 1 пример на каждую строку или перевести в “потенциальная функция источника”, не “использование Гиллом”.

---

## GILL-CONTENT-007 — “мистик” о Gill Song of Songs может вызвать неверную ассоциацию

Part II:

> “открывает его как мистика”

Для баптистско-реформатского сайта слово “мистик” может звучать как католико-созерцательная традиция или неопределённая духовность.

**Лучше:**

```text
открывает его как автора опытно-благочестивого, насыщенного брачной образностью толкования
```

или:

```text
как богослова духовного опыта, а не только полемиста и систематика.
```

---

## GILL-CONTENT-008 — “еврейская традиция признаёт это толкование” требует нюанса

Part II по Матф. 21:42:

> “еврейская традиция признаёт это толкование.”

Если речь о Rashi/Kimchi, лучше:

```text
некоторые авторитетные средневековые еврейские толкователи допускали мессианское прочтение этого места.
```

Иначе звучит так, будто вся “еврейская традиция” признаёт христианский аргумент.

---

## GILL-CONTENT-009 — “главное историческое достижение” Haykin нуждается в точной citation

Part II:

> “Это его главное историческое достижение — по оценке самого Хайкина — превосходящее даже богословские трактаты.”

Очень сильный тезис. Нужно проверить, сказал ли Haykin именно это или это авторская интерпретация его оценки.

**Статус:** NEEDS SOURCE EXACTNESS.

**Решение:**

- если это цитата/точный тезис Haykin — дать сноску;
- если авторский вывод — написать “в этом свете можно говорить...”.

---

## GILL-CONTENT-010 — “Арминианство и пелагианство есть жизнь и душа папства” требует pastoral framing

Part II цитирует Gill:

> “арминианство и пелагианство есть самая жизнь и душа папства”

Исторически важно, но для современного читателя нужно объяснить:

- это polemical 18th-century Protestant idiom;
- это не современный стиль сайта;
- это не разрешение на грубость.

**Решение:** добавить короткий editorial note.

---

## GILL-CONTENT-011 — “первое систематическое богословие, созданное баптистом” требует аккуратного scope

Part II:

> “первое систематическое богословие, созданное баптистом.”

Это распространённый тезис, но безопаснее:

```text
одно из первых, а в англоязычной баптистской традиции — классически называемое первым полным систематическим богословием...
```

Если оставлять “первое”, нужна footnote к библиографу/исследователю.

---

## GILL-CONTENT-012 — structure Body of Divinity дана противоречиво

Part II одновременно говорит:

- “11 книг, 156 глав”;
- “7 книг догматических, 4 практических”;
- “догматическая часть вышла 1767–1769”;
- “в 1769 ... in two volumes quarto”;
- таблица затем даёт 4 крупные категории I–IV с приблизительными страницами.

Проблема: таблица I–IV визуально выглядит как структура самого Gill Body, хотя это авторская агрегированная схема.

**Решение:** подписать:

```text
Схематическое тематическое резюме, не оглавление издания
```

или дать реальную book structure.

---

## GILL-CONTENT-013 — “Гилл строил иначе: оправдание → возрождение → вера” требует осторожности

Part III:

> “Гилл строил иначе: оправдание → возрождение → вера.”

Это очень спорный богословский тезис. Даже если Haykin говорит о “трёх стадиях”, формула может создать впечатление, будто Gill полностью переставляет ordo salutis в простом виде.

**Исправить:**

```text
В интерпретации Хайкина у Гилла возникает порядок, где вечный и виртуальный аспект оправдания предшествует переживаемому во времени акту веры; однако это не означает, что верующий субъективно осознаёт оправдание до веры.
```

---

## GILL-CONTENT-014 — tooltip pactum salutis и справочник противоречат друг другу

Part II tooltip:

> “pactum salutis — вечный совет Отца, Сына и Святого Духа... важный нюанс Гилла — явное включение Святого Духа...”

Spravochnik terms:

> “Pactum Salutis — предвечный завет между Отцом и Сыном...”

Там же добавляется, что Gill различал pactum salutis и covenant of grace, хотя “часто рассматривал их как единое целое”.

Риск: читатель получает две модели:

1. pactum salutis как триадный совет;
2. pactum salutis как договор Отца и Сына с добавленным нюансом.

**Решение:** единое определение:

```text
В классической реформатской схеме pactum salutis часто описывали как предвечное соглашение Отца и Сына; особенность Гилла, по ряду исследователей, — более явное включение Святого Духа как согласующей и применяющей Личности.
```

И использовать это во всех местах.

---

## GILL-CONTENT-015 — glossary “Free Offer” слишком уверенно приписывает позицию “Gill and followers”

Spravochnik:

> “Гилл и его последователи отрицали универсальные предложения...”

Лучше различить:

- Gill;
- Brine;
- Hussey/Skepp;
- later high Calvinists;
- Fullerite critique.

**Исправить:**

```text
Гилл отрицал язык универсальных “предложений” благодати, но поддерживал публичное провозглашение Евангелия. Его последователи и критики по-разному развивали этот тезис.
```

---

## GILL-CONTENT-016 — glossary “Arminianism / Unitarianism” смешивает типы угроз

Spravochnik:

> “Две главные угрозы, против которых сражался Гилл.”

Это допустимо как популярное резюме, но исторически это разные фронты:

- Unitarianism — Trinitarian orthodoxy / Christology.
- Arminianism — soteriology / election / grace.
- “через Wesley” — уже later public polemic.

**Решение:** разделить на две cards или явно указать разные сферы.

---

## GILL-CONTENT-017 — Part III “никогда прежде и никогда после” почти наверняка требует смягчения

Part III про mourning after Gill:

> “никогда прежде и никогда после не поднималось такого плача в англоязычном мире...”

Даже если Rippon употребляет высокий стиль, в русском тексте это звучит как объективная историческая метрика.

**Исправить:**

```text
Риппон гиперболически подчёркивал масштаб скорби...
```

или:

```text
по оценке Риппона, ...
```

---

## GILL-CONTENT-018 — Brown University donation claim требует Level A source

Part III:

> “полный комплект своих сочинений и 52 фолиантных тома трудов отцов Церкви... крупнейшее пожертвование... труды до сих пор хранятся в библиотеке Брауна.”

Это яркий и ценный факт, но он должен иметь сильную опору:

- will / bequest record;
- Brown library catalogue;
- Manning correspondence;
- early college history.

Быстрый внешний поиск не дал очевидного подтверждения по ключевым словам “John Gill 52 folio volumes Brown University”.

**Статус:** NEEDS PRIMARY VERIFICATION.

Пока лучше:

```text
Согласно [конкретный источник], ...
```

или понизить:

```text
в традиции Brown/Rhode Island College с Гиллом связывают пожертвование...
```

---

## GILL-CONTENT-019 — “works still stored at Brown” требует catalogue link

Если утверждать “до сих пор хранятся”, нужно:

- shelf/call number;
- collection page;
- catalogue search;
- archival note.

Без этого это наиболее уязвимый факт раздела.

---

## GILL-CONTENT-020 — “единственный / крупнейший / первый” повторяются слишком часто

В серии много сильных слов:

```text
беспрецедентный
единственный
первый
главное достижение
безусловно крупнейший
никогда прежде и никогда после
не имеет себе равных
```

Часть принадлежит цитатам, часть — авторскому голосу.

**Решение:** маркировать:

- “по словам X”;
- “по оценке Y”;
- “в баптистской среде”;
- “один из”;
- “редкий пример”;
- “классически считается”.

---

# 5. Tooltip / glossary findings

## GILL-CONTENT-021 — tooltip definitions не имеют единого glossary source

Сейчас:

- inline tooltip pactum salutis в Part II;
- inline tooltip hyper-Calvinism в Part III;
- standalone dictionary in Spravochnik.

Они не связаны как единая модель. Если определение правится в одном месте, другое устареет.

**Решение:**

```ts
gillTerms = {
  pactumSalutis: {
    short,
    full,
    sources,
    relatedSections
  }
}
```

Из него рендерить:

- inline tooltip;
- glossary card;
- Pagefind index;
- print glossary.

---

## GILL-CONTENT-022 — tooltip text должен быть print-safe и TTS-safe

Inline pattern:

```html
<span class="gterm">
  термин
  <span class="gtip">длинное определение...</span>
</span>
```

Риск:

- TTS может прочитать tooltip вместе с sentence;
- Pagefind может индексировать скрытый текст как часть body;
- print может скрыть или неудачно раскрыть tooltip;
- screen reader может получить неочевидный nested text.

**Решение:** terms should use `aria-describedby` + hidden definition outside flow or generated popover, not nested text if it pollutes projections.

---

## GILL-CONTENT-023 — tooltip “hyper-Calvinism” хороший, но требует distinction “label vs doctrine”

Part III tooltip уже правильно говорит, что термин спорный. Нужно усилить:

```text
термин часто использовался полемически; применительно к Гиллу оценка зависит от определения.
```

И привязать к Part III table.

---

## GILL-CONTENT-024 — glossary card “Antinomianism” нуждается в softer “часто ложно обвиняли”

Spravochnik пишет, что Gill often falsely accused. Это богословски защитная позиция, но research-wise надо указать:

- кто обвинял;
- кто защищал;
- какие тексты Gill о law/rule of life.

Иначе это apologetic assertion.

---

## GILL-CONTENT-025 — Hebrew inscription uses Wisdom 3:1

Part III uses:

```text
Премудрость 3:1
```

For Baptist/Reformed audience, deuterocanonical citation needs editorial framing:

```text
как эпитафическая/историческая формула, не как канонический proof-text
```

Без этого часть читателей может воспринять как каноническое употребление.

---

# 6. Footnotes / source apparatus findings

## GILL-CONTENT-026 — Part I section facts часто без inline footnotes

Examples:

- Goat Yard Declaration details;
- Stinton / Lorimers Hall;
- exact 1800 membership practice;
- daughter funeral timing;
- sermon text;
- Rippon quotes.

Sources are listed at bottom, but individual high-value claims need inline notes.

## GILL-CONTENT-027 — Part II has long quotations without precise page references

Examples:

- Gill Trinity preface;
- Whiston memoir;
- Hervey quote;
- Gill on Song 7:10;
- Body of Divinity opening sentence;
- sermons and tracts quote.

Need page/edition where possible.

## GILL-CONTENT-028 — Part III quote density is high but citation density is uneven

Examples requiring precise source:

- Spurgeon portrait “smell of free will”;
- Mary Bayly elegy;
- Benjamin Francis poetry;
- Brown donation;
- Spurgeon 1859 “not my Rabbi”;
- reviewer claim no commentary can compare.

These are memorable and likely to be quoted by readers. They must be robust.

---

# 7. Text / editorial findings

## GILL-CONTENT-029 — Part II starts as “Trilogy” despite planned Part IV

Part II and Part III still say:

```text
Трилогия о Джоне Гилле
три самостоятельных текста
```

This is now stale if Part IV is intended.

**Fix:** “серия” / “цикл”.

## GILL-CONTENT-030 — Part II begins at “III. Богословские труды” although page is Part II

This can confuse:

```text
Часть II. Учёный
H2: III. Богословские труды...
```

If Roman numerals are internal macro-parts, fine, but explain. Otherwise reader thinks Part II starts at III.

## GILL-CONTENT-031 — Part III begins at “V. Историческое влияние” without earlier I–IV on same page

Same problem. The macro-numbering crosses pages, but user inside page may not understand.

**Fix:** either visible “сквозная структура серии” note, or page-local heading numbering.

## GILL-CONTENT-032 — Part III has multiple endings

Part III contains:

- death scene;
- epitaph;
- discipline;
- hyper-Calvinism deep;
- legacy;
- Brown;
- Spurgeon.

The emotional climax occurs before many research addenda, so narrative energy resets several times.

**Fix:** move death/epitaph closer to final conclusion OR mark later blocks as “Дополнительные исследовательские справки”.

## GILL-CONTENT-033 — source sections should be outside searchable narrative

Sources are important but should not pollute Pagefind/TTS as if they are main article.

Use:

```html
<section class="reading-list-section" data-pagefind-ignore data-tts-ignore>
```

Then create searchable source page separately if needed.

## GILL-CONTENT-034 — inline style debt inside article text harms future content editing

Part II/III have many inline styles around note-box, quotes, headings, images.

Content editor should not edit style while editing research.

Move to classes.

---

# 8. Priority fix list

## Immediate content/research fixes

1. Replace “три самостоятельных текста / трилогия” → “серия / цикл”.
2. Add source precision to Part III hyper-Calvinism table.
3. Smoothe “единственный / беспрецедентный / никогда прежде” claims.
4. Add inline source notes to Goat Yard Declaration and daughter sermon.
5. Verify Brown donation claim from primary/institutional source.
6. Unify pactum salutis definition across tooltip and Spravochnik.
7. Add deuterocanonical framing for Wisdom 3:1.
8. Mark sources/reading-list sections as non-TTS/non-Pagefind if desired.
9. Split “Arminianism / Unitarianism” glossary card.
10. Move Part III research addenda into clearly marked “research notes” if keeping after death climax.

## Research verification tasks

- Rippon 1838: exact pages for birth prophecy, daughter, wife, final words, mourning scale.
- Goat Yard Declaration: exact text and Article XI/XII.
- Brown/Rhode Island College: institutional catalogue or early history.
- Spurgeon 1859 sermon: exact wording and sermon reference.
- Spurgeon portrait/free-will smell: source and wording.
- Mary Bayly elegy: bibliographic record.
- Haykin SBJT 2021: exact claims on trinitarian preservation and justification.
- Macritchie 2025 PDF: exact chapters/pages on Gill vs Hussey/Skepp/Brine.

---

# 9. Acceptance criteria

Content audit is not complete until every “memorable” claim has one of:

```text
inline footnote
source tooltip
bibliographic page reference
explicit “по оценке/по словам”
or softened wording
```

No claim should remain in the dangerous middle zone:

```text
sounds exact
sounds dramatic
likely to be repeated
but has no visible evidence nearby
```

---

# 10. Correction to previous master

The previous V2 had an over-broad UI interpretation about A−/A+. This V3 supersedes that part:

- Do not force A−/A+ into a common visual block as a design requirement.
- Treat only excessive spacing / layout geometry as possible bug.
- Focus further passes on content, footnotes, glossary, tooltips, Pagefind/TTS projections, sources, and research integrity.

---

# 11. Второй содержательный проход: сверка с Риппоном и cross-page consistency

**Основной первоисточник прохода:** John Rippon, *A Brief Memoir of the Life and Writings of the Late Reverend John Gill, D.D.*  
Проверялся полный OCR экземпляра 1838 года на Internet Archive. Для каждого пункта ниже отдельно указано, что подтверждено самим текстом Риппона, а что пока требует другого источника.

## Обновлённый уровень критичности

### P0 — исправлять до следующей публичной редакции

1. Quiz Part I закрепляет неверную причину семилетней задержки крещения.
2. Хронология 1 / 4 / 11 ноября 1716 года расходится внутри Part I и справочника.
3. Возраст / год рождения дочери Элизабет внутренне несовместимы.
4. Утверждение о Декларации и 1800 годе, вероятно, возникло из неверно прочитанной сноски Риппона.
5. Возраст Гилла при смерти указан неверно.
6. Координата его могилы переписана неверно.
7. Структура *Practical Divinity* дана одновременно как четыре и пять книг.
8. Полная линия пасторов искусственно сокращена до Гилл → Риппон → Сперджен.

### P1 — источниковая и редакционная надёжность

- точные цитаты без страниц;
- дублирование рассказа о степени D.D.;
- Brown University без институционального подтверждения;
- “таинства” вместо устойчивого баптистского “установления”;
- абсолютные superlatives вместо атрибутированных оценок;
- расходящиеся определения в inline tooltip, Part III glossary и справочнике.

---

# 12. Подтверждённые хронологические ошибки

## GILL-CONTENT-035 — Quiz Part I даёт исторически неподтверждённый “правильный” ответ  
**Статус:** CONFIRMED PRIMARY-SOURCE CONFLICT  
**Severity:** P0

Quiz спрашивает, почему Гилл ждал семь лет до публичного исповедания и крещения. Правильным назначен ответ:

> он придерживался осторожного, библейского подхода, глубоко исследуя своё сердце.

В полном объяснении это превращается почти в психологический портрет: он “семь лет испытывал сердце”.

Риппон называет две более конкретные причины:

1. сначала — молодость Гилла и серьёзность публичного исповедания;
2. позднее — понимание, что после вступления в членство церковь намерена как можно скорее призвать его к служению, тогда как он не спешил принимать этот призыв.

Это не отменяет осторожность Гилла, но quiz превращает редакционную интерпретацию в единственный исторический факт.

### Исправление

Вариант правильного ответа:

```text
Сначала из-за молодости и серьёзности публичного исповедания,
а затем потому, что ожидал скорого призвания к служению после вступления в церковь.
```

Пастырский вывод об осторожности можно оставить в пояснении, но явно как интерпретацию.

---

## GILL-CONTENT-036 — Ис. 53 прочитан не вечером крещения, а 4 ноября  
**Статус:** CONFIRMED PRIMARY-SOURCE ERROR  
**Severity:** P0

Part I говорит:

> “Вечером дня крещения ... Гилл прочитал Исаию 53”.

Риппон даёт последовательность:

```text
1 ноября 1716 — исповедание и крещение;
4 ноября, следующее воскресенье — принятие в членство и Вечеря;
вечером 4 ноября — чтение и толкование Ис. 53.
```

Следовательно, “вечером дня крещения” — фактическая ошибка.

---

## GILL-CONTENT-037 — первая проповедь была 11 ноября, не в декабре  
**Статус:** CONFIRMED PRIMARY-SOURCE ERROR  
**Severity:** P0

После толкования Ис. 53 вечером 4 ноября Риппон пишет:

> “the next Lord’s Day evening” Гилл произнёс речь на 1 Кор. 2:2.

Это означает **11 ноября 1716 года**.

В Part I timeline сейчас:

```text
1716, декабрь — первая проповедь
```

Нужно заменить на:

```text
11 ноября 1716 — первая проповедь на 1 Кор. 2:2.
```

Справочник должен получать эту дату из того же chronology manifest.

---

## GILL-CONTENT-038 — возраст дочери и дата рождения не могут быть верны одновременно  
**Статус:** CONFIRMED INTERNAL CONTRADICTION  
**Severity:** P0

Part I утверждает:

```text
родилась 14 марта 1725;
умерла 30 мая 1738;
возраст — 12 лет 2 месяца 16 дней;
“вступила в тринадцатый год жизни”.
```

При дате рождения 14 марта **1725** года 30 мая 1738 года ей было бы 13 лет 2 месяца 16 дней.

Риппон подтверждает:

- смерть 30 мая 1738 года;
- “in the thirteenth year of her age”.

Последняя формула обычно означает, что двенадцать лет исполнилось и шёл тринадцатый год. Поэтому наиболее вероятно, что добавленный сайтом год рождения должен быть **1726**, но менять его без проверки издания *Choice Experiences* / записи о рождении нельзя.

### Правильное действие

1. найти первичный источник даты рождения;
2. до этого удалить “14 марта 1725” либо пометить как требующее проверки;
3. не вычислять точный возраст на основании несовместимых данных;
4. обновить quiz, статью и timeline одновременно.

---

## GILL-CONTENT-039 — quiz повторяет неразрешённую ошибку возраста дочери  
**Статус:** CONFIRMED DEPENDENT ERROR  
**Severity:** P0

Quiz называет Элизабет “двенадцатилетней”. Это может оказаться верным, но только если год рождения 1725 на странице неверен.

Quiz нельзя считать независимым доказательством: он копирует narrative data.

Нужен единый biographical fact:

```ts
daughterElizabeth: {
  born: verifiedDate,
  died: "1738-05-30",
  ageDisplay: generatedFromDates,
  source: ...
}
```

---

## GILL-CONTENT-040 — Old Style → New Style в справочнике, вероятно, сдвинут на один день  
**Статус:** HIGH-CONFIDENCE CALENDAR ERROR; FINAL ARCHIVAL VERIFY  
**Severity:** P1

Справочник пишет:

```text
23 ноября 1697 ст. ст. → 4 декабря по новому стилю.
```

В 1697 году разница между юлианским и григорианским календарями составляла 10 дней. Поэтому 23 ноября OS соответствует **3 декабря NS**, не 4 декабря.

Здесь нет мартовской проблемы двойного года, потому что дата приходится на ноябрь.

### Рекомендация

Либо:

```text
23 ноября 1697 года по действовавшему в Англии календарю
```

без ненужной конвертации, либо после окончательной проверки:

```text
3 декабря по пролептическому григорианскому календарю.
```

---

# 13. Декларация 1729 года: источник и арифметика

## GILL-CONTENT-041 — “почти сто лет после смерти Гилла” арифметически невозможно  
**Статус:** CONFIRMED  
**Severity:** P0

Сайт пишет:

> ещё в 1800 году новые члены принимались ...  
> декларация служила живым уставом почти сто лет после его смерти.

Гилл умер в 1771 году. Между 1771 и 1800 — **29 лет**, не почти сто.

---

## GILL-CONTENT-042 — сноска “Written in 1800” у Риппона относится не к приёму членов  
**Статус:** CONFIRMED PRIMARY-SOURCE MISREAD RISK  
**Severity:** P0

В OCR Риппона фраза:

```text
* Written in 1800.
```

стоит после определения Particular Baptists из **Rules and Orders of the Particular Baptist Fund**.

Она не сообщает, что в 1800 году церковь Гилла принимала членов только при полном согласии с Декларацией 1729 года.

В проверенном фрагменте самой Декларации Риппон после текста лишь говорит, что Гилл сохранял этот creed до конца жизни. Утверждение о процедуре приёма в 1800 году нуждается в отдельном церковном источнике.

### Действие

До обнаружения church-book / later constitution:

- убрать привязку к Риппону;
- либо дать точный источник;
- не строить из сноски 1800 года столетний narrative.

---

## GILL-CONTENT-043 — “определила облик общины на следующие полтора века” не доказано  
**Статус:** NEEDS LONGITUDINAL SOURCE  
**Severity:** P1

Это может быть исторически правдоподобно, но требует:

- позднейших church constitutions;
- records Rippon / Carter Lane / New Park Street;
- данных о том, когда declaration перестала быть membership standard.

Без такой цепочки формула должна быть смягчена:

```text
она надолго закрепила богословский профиль общины
```

---

# 14. Смерть, могила и финальные слова

## GILL-CONTENT-044 — возраст Гилла при смерти указан неверно  
**Статус:** CONFIRMED PRIMARY-SOURCE ERROR  
**Severity:** P0

Part III:

```text
73 года, 10 месяцев и 21 день.
```

Риппон:

```text
seventy-three years, ten months, and ten days.
```

Исправить на **73 года 10 месяцев 10 дней**, если сохраняется календарная система Риппона.

---

## GILL-CONTENT-045 — координата могилы переписана неверно  
**Статус:** CONFIRMED PRIMARY-SOURCE ERROR  
**Severity:** P0

Part III сообщает:

```text
восточно-западный ряд 20–21;
северо-южный 65–66.
```

Риппон сообщает:

```text
19 east and west;
65 and 66 north and south.
```

Следовательно, первая координата должна быть **19**, если используется именно система Риппона.

Нужно дополнительно проверить современную карту Bunhill Fields, прежде чем превращать старую coordinate note в современную инструкцию поиска могилы.

---

## GILL-CONTENT-046 — сайт убрал важное “probably” из оценки масштаба скорби  
**Статус:** CONFIRMED SOURCE AMPLIFICATION  
**Severity:** P1

Риппон пишет, что число memorial sermons:

```text
exceeded, probably, all that had ever been known before or since
```

То есть это:

- похвальная биографическая риторика;
- с явным словом **probably**.

Сайт превращает её в:

> никогда прежде и никогда после не поднималось такого плача в англоязычном мире.

Проблемы:

1. исчезло “вероятно”;
2. “numbers of sermons” превращены в измерение общего плача;
3. “Great Britain and various parts of America” расширено до всего англоязычного мира.

### Исправление

```text
Риппон, говоря в явно панегирическом ключе, полагал, что число
поминальных проповедей могло превосходить всё известное ему прежде и после.
```

---

## GILL-CONTENT-047 — последние слова жены собраны в одну последовательность без source layering  
**Статус:** NEEDS PRIMARY TEXT OF FUNERAL SERMON  
**Severity:** P1

Статья одновременно называет:

- “И для меня тоже”;
- “Господи, Господи”;
- “Завет непоколебим”

последними / итоговыми словами Элизабет.

Это могут быть три разных уровня:

1. слова за несколько воскресений до смерти;
2. последние различимые слова в момент смерти;
3. формула из найденной рукописи или авторский итог Гилла.

Но сейчас reader получает впечатление трёх конкурирующих “последних слов”.

### Исправление

Разнести labels:

```text
Последнее известное исповедание за несколько недель до смерти...
Последние слышимые слова...
Фраза из посмертно найденной записи Гилла...
```

И дать страницу funeral sermon / note.

---

# 15. Первичный источник против редакционной психологии

## GILL-CONTENT-048 — “семилетие испытания сердца” подменяет документированную мотивацию  
**Статус:** CONFIRMED INTERPRETIVE OVERWRITE  
**Severity:** P1

Помимо quiz, narrative утверждает, что семь лет были почти исключительно “испытанием сердца”.

Риппон действительно описывает серьёзность Гилла, но прямо сообщает институциональный фактор: ожидание призвания к служению после membership.

Нельзя убирать этот фактор, потому что он важен для понимания:

- раннего recognition gifts;
- осторожности перед ministry;
- устройства Particular Baptist church.

---

## GILL-CONTENT-049 — “три пророчества” не перечислены как три независимых свидетельства  
**Статус:** EDITORIAL CLARITY / SOURCE VERIFY  
**Severity:** P2

Section heading обещает “три пророчества”, но текст содержит:

- убеждение отца, что родится сын;
- ожидание его служения баптистскому делу / служения Слова;
- реплику незнакомца о будущей учёности.

Возможно, именно эти три элемента имелись в виду, но они не пронумерованы и смешаны с поздней биографической рамкой.

### Исправление

Либо явно показать три пункта, либо переименовать:

```text
Предание об утре рождения
```

---

## GILL-CONTENT-050 — “оксфордские профессора снимали шляпу” не привязано к источнику  
**Статус:** NEEDS SOURCE  
**Severity:** P1

Заключение birth-prophecy section говорит о человеке:

> “перед которым снимали шляпу оксфордские профессора.”

В данном section source — Rippon — такой факт рядом не указан.

Нужно:

- назвать профессора / эпизод / письмо;
- либо убрать образное утверждение.

---

# 16. Образование и источники

## GILL-CONTENT-051 — таблица образования использует неаудируемые source labels  
**Статус:** CONFIRMED  
**Severity:** P1

В table:

```text
10 лет — Rippon
11 лет — “церковные записи Кеттеринга”
~14 — “автобиографические заметки”
19 — “свидетельства учеников”
```

Но доступный narrative Rippon:

- сообщает школу и её оставление;
- сообщает Buxtorf grammar/lexicon;
- не даёт в проверенном месте эти четыре source buckets в такой форме.

“Автобиографические заметки” и “свидетельства учеников” без названия, места хранения и страницы невозможно проверить.

### Исправление

Каждая строка:

```text
author / title / edition / page
```

Если source неизвестен — удалить колонку “Источник”, а не создавать видимость архивной точности.

---

## GILL-CONTENT-052 — “в девятнадцать выучил еврейский” слишком точно датировано  
**Статус:** SOURCE DOES NOT SUPPORT EXACT MILESTONE  
**Severity:** P1

Риппон пишет, что Gill учил Hebrew самостоятельно с Buxtorf и продолжал занятия до примерно девятнадцатого года жизни. Он не фиксирует в проверенном фрагменте отдельное событие:

```text
в 19 лет впервые начал читать Hebrew Bible без помощи.
```

Это может быть поздняя традиция, но тогда нужен отдельный источник.

---

## GILL-CONTENT-053 — хороший caveat Baptist Encyclopedia должен стать моделью всей серии  
**Статус:** POSITIVE PATTERN

Education section корректно поясняет, что:

> “no man in the eighteenth century...” — высокая оценка Baptist Encyclopedia, а не измеримая статистика.

Именно такую форму нужно применить к:

- “нигде больше в протестантизме”;
- “единственный гебраист”;
- “крупнейшее пожертвование”;
- “первое systematic theology”;
- “никогда прежде и после”.

---

# 17. Пасторская преемственность

## GILL-CONTENT-054 — chain Keach → Stinton → Gill → Rippon → Spurgeon не является полной succession  
**Статус:** CONFIRMED HISTORICAL OMISSION  
**Severity:** P0/P1

Статья называет это “линией преемства”:

```text
Benjamin Keach → Benjamin Stinton → John Gill → John Rippon → Charles Spurgeon
```

Между Rippon и Spurgeon в этой общине служили другие пасторы, включая:

```text
Joseph Angus
James Smith
William Walters
```

Поэтому current chain допустима только как:

```text
линия наиболее известных пасторов
```

но не как полная последовательность.

### Исправление

Либо показать всех pastors, либо подписать:

```text
избранная линия наиболее известных преемников кафедры
```

---

## GILL-CONTENT-055 — “четыре последовательных пастора — более двухсот лет” построено на сокращённой линии  
**Статус:** CONFIRMED LOGICAL ERROR  
**Severity:** P1

Part III складывает сроки Keach, Gill, Rippon, Spurgeon и затем утверждает:

> четыре последовательных пастора...

Они не были четырьмя непосредственно последовательными пасторами: пропущены Stinton и post-Rippon ministers.

Также тезис:

> “Нигде больше в истории протестантизма такого нет”

требует глобального сравнительного исследования и сейчас является недоказуемым superlative.

---

## GILL-CONTENT-056 — современный Peter Masters не должен быть бесконечно hardcoded  
**Статус:** TEMPORALLY UNSTABLE CONTENT  
**Severity:** P2

Part I сообщает:

```text
служит с 1970 года; по состоянию на 2026 — 56 лет.
```

Для исторической статьи это быстро устаревающий live fact.

Решение:

- либо дата последней проверки рядом;
- либо генерировать продолжительность;
- либо просто “с 1970 года” без постоянно устаревающего вычисления.

---

# 18. Part II: дубли, терминология и bibliography

## GILL-CONTENT-057 — рассказ о степени D.D. повторён почти трижды подряд  
**Статус:** CONFIRMED  
**Severity:** P1

Section сначала подробно говорит:

- proposal accepted;
- professor paid fees;
- wording of diploma;
- famous answer.

Затем следующий абзац снова:

- 1748;
- honorary D.D.;
- wording of diploma;
- professor’s explanation.

Потом отдельная quote-card в третий раз повторяет:

> “Я об этом не думал, не покупал и не искал.”

### Исправление

Оставить:

1. один narrative paragraph;
2. одну primary-source quote;
3. короткую source note.

Остальное убрать.

---

## GILL-CONTENT-058 — знаменитая фраза переведена неточно по порядку  
**Статус:** MINOR QUOTE ACCURACY  
**Severity:** P2

Риппон:

```text
I neither thought it, nor bought it, nor sought it.
```

Сайт:

```text
Я её не искал, не думал о ней, не покупал.
```

Смысл сохранён, но исчезла ритмическая последовательность thought / bought / sought.

Лучше:

```text
Я о ней не думал, не покупал её и не искал её.
```

Можно дать английский оригинал рядом.

---

## GILL-CONTENT-059 — “таинства” расходятся с баптистским и первичным словоупотреблением  
**Статус:** CONFIRMED TERMINOLOGY DRIFT  
**Severity:** P1

Part II heading:

```text
Таинства и церковные установления
```

и текст:

```text
два таинства
```

Риппон и Declaration используют **ordinances**.

Для русского баптистского сайта нормальный основной термин:

```text
установления
```

Возможная форма:

```text
два установления Христа — крещение и Вечеря Господня
```

Если “таинство” оставляется как широкий исторический перевод, нужна единая terminology policy, иначе сайт звучит конфессионально смешанно.

---

## GILL-CONTENT-060 — Part II не имеет полноценного списка источников  
**Статус:** CONFIRMED  
**Severity:** P1

`GillPart2PostArticle` содержит только SDG.

При этом Part II включает:

- длинные прямые цитаты;
- Whiston;
- Hervey;
- Haykin;
- Muller;
- Scheiderer;
- Kennicott;
- Spurgeon;
- detailed bibliography claims.

Это наиболее research-heavy статья, но без отдельного source apparatus.

### Исправление

Добавить:

```text
Primary sources
Academic studies
Edition/translation notes
Unverified popular anecdotes
```

---

## GILL-CONTENT-061 — structure Practical Divinity: четыре книги или пять  
**Статус:** CONFIRMED CROSS-PAGE CONTRADICTION  
**Severity:** P0

Part II:

```text
7 doctrinal books + 4 practical books + separate appendix on Jewish proselyte baptism.
```

Spravochnik:

```text
Practical Divinity — 5 books;
fifth = Jewish proselyte baptism.
```

Риппон описывает dissertation as appearing in the *Body of Divinity*, но это само по себе не делает её пятой книгой.

Нужно сверить **table of contents конкретного издания** и зафиксировать:

```text
4 books + appendix/dissertation
```

или иную реальную структуру. Пока один из двух блоков неверен.

---

## GILL-CONTENT-062 — даты Old Testament Exposition расходятся  
**Статус:** CONFIRMED CROSS-PAGE CONTRADICTION  
**Severity:** P1

Part II говорит, что публикация OT commentary началась с Pentateuch в 1748–1750.

Spravochnik ставит:

```text
1763–1766 — Exposition of the Old Testament.
```

Это может отражать даты отдельных поздних volumes / completion, но как дата всего труда вводит в заблуждение.

Нужно показывать range публикации всего корпуса и отдельно completion:

```text
publication began 1748;
completed in the 1760s.
```

---

## GILL-CONTENT-063 — Body of Doctrinal Divinity: 1767 или 1769  
**Статус:** EDITION/DATING AMBIGUITY  
**Severity:** P1

В разных частях серии появляются 1767 и 1769. Справочник ставит 1769; распространённые bibliographies часто дают 1767; Internet Archive scan может относиться к 1769 volume/issue.

Нельзя выбрать год по одному digit без bibliographic note.

Нужно различать:

```text
first publication / issue in parts;
title-page date of consulted edition;
completion / second volume.
```

---

## GILL-CONTENT-064 — eschatological “prediction” превращена в teleological praise  
**Статус:** NEEDS SOURCE + EDITORIAL OVERREACH  
**Severity:** P1

Part II говорит, что Gill placed a latter-day period between 1866 and 1913, затем:

> “поразительно точное предвидение экуменического миссионерского движения конца XIX века.”

Даже если dates верны, совпадение с missionary movement:

- является современной интерпретацией;
- не доказывает исполнение Gill’s eschatology;
- слово “экуменический” может быть анахроничным и богословски двусмысленным.

### Исправление

Либо убрать оценку, либо:

```text
Позднейшие авторы сопоставляли этот диапазон с расширением
протестантских миссий XIX века; такое сопоставление остаётся интерпретацией.
```

---

# 19. Part III и справочник: definition drift

## GILL-CONTENT-065 — Sandemanianism одновременно назван продолжением Gill и его противником  
**Статус:** CONFIRMED INTERNAL CONFLICT  
**Severity:** P1

Part III говорит, что последователи Gill, особенно “в духе Robert Sandeman”, развили его идеи до крайностей.

Позднее glossary утверждает:

```text
Gill and his successors fought Sandemanianism.
```

Эти формулы нельзя оставлять вместе без объяснения.

Исторически нужно различить:

- Gill’s high Calvinism;
- Sandeman’s definition of saving faith;
- возможные пересечения / разные networks;
- later polemical conflation.

---

## GILL-CONTENT-066 — inline glossary, Part III flip glossary и Spravochnik не имеют одного owner  
**Статус:** CONFIRMED  
**Severity:** P1

Термины существуют минимум в трёх местах:

1. `.gterm > .gtip`;
2. Part III flip cards;
3. Spravochnik term cards.

Следствия:

- pactum salutis уже расходится;
- hyper-Calvinism может получить разные definitions;
- eternal justification может измениться только в одном месте;
- search/TTS/print получают разные тексты.

Нужен один glossary data file с short/full/source variants.

---

## GILL-CONTENT-067 — “миссионерская спячка в церквях, следовавших Gill” слишком широко  
**Статус:** NEEDS QUANTIFIED HISTORICAL SOURCE  
**Severity:** P1

Part III:

> “В церквях, следовавших Гиллу, наступала миссионерская спячка.”

Это классическая criticism narrative, но она:

- обобщает множество congregations;
- не определяет период;
- не отделяет Gill от Brine/Hussey/later developments;
- не показывает counterexamples.

Нужно атрибутировать конкретному historiographical camp или заменить аналитическим параграфом.

---

## GILL-CONTENT-068 — “искренне приглашать” нуждается в точной source distinction  
**Статус:** NEEDS TEXTUAL PROOF  
**Severity:** P1

Part III одновременно утверждает:

- Gill отрицал universal offers;
- проповедник должен “искренне приглашать”.

Для темы free offer критично различить:

```text
proclamation
command to repent/believe
indiscriminate address
offer
well-meant offer
assurance of Christ’s willingness
```

Нужны точные Gill passages, а не только rehabilitating summary.

---

## GILL-CONTENT-069 — Spravochnik “Top-10” ошибочно называет сборник consensus  
**Статус:** CONFIRMED EDITORIAL OVERSTATEMENT  
**Severity:** P2

SBJT 25.1 называется:

> “современный консенсус о Гилле.”

Но special issue — это collection of scholarly arguments, а не consensus statement.

Лучше:

```text
один из главных современных сборников исследований, представляющий несколько оценок.
```

---

## GILL-CONTENT-070 — Top-10 source hierarchy несбалансирована  
**Статус:** CONFIRMED  
**Severity:** P1/P2

В “десяти текстах, без которых нельзя серьёзно говорить” есть pastoral overview London Lyceum, но нет ряда foundational critical works, постоянно используемых в статье:

- Peter Toon;
- Thomas Nettles;
- B. R. White;
- Gregory Wills / Willis;
- Curt Daniel;
- точного primary corpus Gill on free offer.

Это не означает, что London Lyceum нужно удалить. Но label “must-read top-10” должен отражать research hierarchy.

---

## GILL-CONTENT-071 — Macritchie conclusion пересказывается без pages  
**Статус:** SOURCE EXISTS; INTERPRETATION NEEDS PAGE  
**Severity:** P1

Справочник уже утверждает, что thesis показывает:

> Gill shared assumptions of the school but not its radical conclusions.

Official thesis record confirms the dissertation exists. Но этот итог должен иметь:

```text
chapter / page / conclusion section
```

Иначе summary выглядит как авторский verdict, прикрытый ссылкой на целый PDF.

---

## GILL-CONTENT-072 — undefined “Seymour” в disputes table  
**Статус:** CONFIRMED  
**Severity:** P2

Справочник советует сравнивать:

```text
Сеймура, Туна, Неттлза, Ратела, Макритчи
```

Но:

- full name/title Seymour отсутствует;
- transliteration Rathel / Рэтел / Рател расходится по серии.

Нужен canonical researchers registry.

---

## GILL-CONTENT-073 — `esse / bene esse` введены без определения  
**Статус:** CONFIRMED  
**Severity:** P2

Для справочника, предназначенного помогать читателю, нельзя вводить ещё два латинских термина внутри объяснения без gloss.

---

# 20. Цитаты, переводы и визуальные реконструкции

## GILL-CONTENT-074 — русские переводы первоисточников не имеют translator metadata  
**Статус:** CONFIRMED  
**Severity:** P1

Большинство длинных Gill/Rippon/Spurgeon quotes представлены по-русски как точные цитаты, но неясно:

- чей перевод;
- literal или adaptive;
- какое издание;
- page;
- модернизирована ли пунктуация;
- сокращён ли текст.

Нужен единый format:

```text
Перевод проекта по: Author, Title, edition, page.
Сокращения отмечены многоточием.
```

---

## GILL-CONTENT-075 — крещальный hymn translation должен быть назван поэтическим переложением, если он не literal  
**Статус:** TRANSLATION QA REQUIRED  
**Severity:** P2

Русская версия меняет meter и местами расширяет theological wording. Это допустимо для поэтического перевода, но label:

```text
Русский перевод
```

может обещать literal equivalence.

Лучше:

```text
Поэтический перевод проекта
```

и отдельно предоставить подстрочник, если текст используется как historical evidence.

---

## GILL-CONTENT-076 — художественные изображения подписаны как документальные сцены  
**Статус:** PROVENANCE GAP  
**Severity:** P1

Examples:

- “Погребальная проповедь Гилла в капелле XVIII века”;
- “часовня Хорслидаун ... где Гилл служил”;
- baptism and study scenes.

Если изображения сгенерированы / реконструированы, captions должны говорить:

```text
Художественная реконструкция
```

а не создавать впечатление archival illustration.

---

## GILL-CONTENT-077 — “Charles Spurgeon, G3 Ministries” смешивает автора цитаты и современного посредника  
**Статус:** CONFIRMED ATTRIBUTION ERROR  
**Severity:** P1

Source line:

```text
— Чарльз Сперджен, G3 Ministries
```

G3 Ministries — не первичный источник и не соавтор Spurgeon.

Нужно:

```text
Charles Spurgeon, original sermon/book, volume/page;
цитируется по [secondary page], если оригинал пока не найден.
```

---

## GILL-CONTENT-078 — “один ведущий обозреватель XIX века” должен быть назван  
**Статус:** CONFIRMED SOURCE OPACITY  
**Severity:** P1

Анонимная authority formula недопустима рядом с maximal claim:

> ни один комментарий ни на одном языке нельзя сравнить...

Нужно назвать:

```text
author
periodical/book
year
page
```

или удалить.

---

# 21. Обновлённая таблица первоисточниковой сверки

| Тема | Текст сайта | Риппон / первичный материал | Вердикт |
|---|---|---|---|
| Крещение | 1 ноября 1716 | 1 ноября 1716 | OK |
| Принятие и Вечеря | 4 ноября | 4 ноября | OK |
| Ис. 53 | вечер дня крещения | вечер 4 ноября | Ошибка |
| Первая проповедь | декабрь | следующее воскресенье после 4 ноября = 11 ноября | Ошибка |
| Причина задержки | испытание сердца | молодость/серьёзность + ожидание ministry call | Quiz/narrative искажены |
| Дочь | 14.03.1725, 12 лет | умерла 30.05.1738, “в тринадцатом году” | Год рождения конфликтует |
| Declaration / 1800 | membership standard in 1800 | “Written in 1800” относится к Baptist Fund definition | Вероятная misread |
| Gill age at death | 73y10m21d | 73y10m10d | Ошибка |
| Grave coordinate | 20–21 / 65–66 | 19 / 65–66 | Ошибка |
| Mourning | absolute “never before/after” | “probably” about number of sermons | Усиление источника |
| D.D. phrase | repeated variants | thought / bought / sought | Сократить и уточнить |

---

# 22. Исправление источникового контракта

Каждое содержательное утверждение должно иметь machine-readable provenance:

```ts
interface ClaimSource {
  claimId: string
  sourceLevel: "A-primary" | "B-academic" | "C-overview" | "D-tradition"
  author: string
  title: string
  edition?: string
  year: number
  page?: string
  url?: string
  quoteMode: "verbatim" | "translated" | "paraphrase" | "inference"
  translator?: string
  confidence: "verified" | "probable" | "needs-verification"
}
```

Особенно обязательно для:

- exact dates;
- last words;
- unique / first / greatest claims;
- denominational succession;
- doctrinal classifications;
- quiz correct answers;
- glossary definitions.

---

# 23. Обновлённый immediate-fix пакет

## Блок A — фактические ошибки

1. Исправить Ис. 53 на 4 ноября 1716.
2. Исправить первую проповедь на 11 ноября 1716.
3. Исправить quiz Q2 о задержке крещения.
4. Разрешить дату рождения/возраст дочери; затем обновить quiz Q4.
5. Удалить неподтверждённый 1800 membership claim.
6. Исправить “почти сто лет”.
7. Исправить возраст Gill при смерти: 10 дней, не 21.
8. Исправить grave coordinate: 19, не 20–21.
9. Исправить succession label / добавить пропущенных pastors.
10. Разрешить 4 vs 5 books Practical Divinity.

## Блок B — research integrity

1. Добавить bibliography Part II.
2. Дать pages к hyper-Calvinism table.
3. Проверить Brown donation институционально.
4. Дать page Macritchie conclusion.
5. Назвать unnamed reviewer.
6. Найти original Spurgeon source вместо “G3 Ministries”.
7. Унифицировать glossary.
8. Ввести translator/quote-mode metadata.

## Блок C — редактура

1. Убрать stale “трилогия”.
2. Смягчить superlatives.
3. Развести last confession / last audible words / manuscript phrase жены.
4. Подписать AI/художественные изображения как реконструкции.
5. Перейти на “установления” как основной баптистский термин.

---

# 24. Новые browser/content audit assertions

Помимо visual checks нужны текстовые guards:

```text
Part I contains "11 ноября 1716"
Part I does not contain "1716, декабрь" for first sermon
Isaiah 53 event is tied to 4 Nov
quiz Q2 sourceRef matches documented reasons
daughter dates form a valid age interval
no claim "почти сто лет после смерти" when evidence date is 1800
Gill death duration equals canonical fact record
grave coordinate generated from one fact record
all Gill pages use one glossary JSON
all direct quotes carry source + quoteMode
no “G3 Ministries” as author of Spurgeon quotation
no “leading reviewer” without name
```

---

# 25. Общий вывод V4

Серия сильнее большинства популярных биографий Гилла по объёму и диапазону источников. Основная опасность сейчас — не отсутствие research, а переход:

```text
источник
→ редакционное усиление
→ повтор в справочнике
→ закрепление в quiz
→ восприятие как бесспорного факта
```

Самые опасные баги возникают именно на последних двух шагах. Поэтому приоритет — не добавлять ещё материал, а построить единый provenance graph и устранить уже обнаруженные cross-page contradictions.

---

# 26. Пятый проход: богословские утверждения, quiz, glossary и первичные тексты Part II–III

**Фокус:** Part II «Учёный», Part III «Наследие», их PageHead/quiz, inline glossary, справочник и source apparatus.

**Метод:**

1. Сопоставление утверждений внутри одной статьи.
2. Сопоставление Part II ↔ Part III ↔ Справочник.
3. Проверка того, что quiz ведёт к правильному источнику и не превращает редакционную интерпретацию в факт.
4. Разделение:
   - собственных формулировок Гилла;
   - поздней исследовательской классификации;
   - авторского богословского вывода сайта.
5. Внешняя проверка только там, где найден доступный источник; отсутствие найденного точного первоисточника помечается `NEEDS EXACT SOURCE`, а не восполняется догадкой.

---

# 27. Quiz Part II: неверные anchors и закрепление интерпретаций

## GILL-CONTENT-079 — вопрос о степени D.D. ведёт не к разделу степени  
**Статус:** CONFIRMED  
**Severity:** P1 functional/content navigation

Quiz Part II Q2 посвящён докторской степени, но `sourceRef.href`:

```text
#sec-commentary
```

Специальный раздел степени имеет:

```text
#sec-dd
```

Читатель после ошибки или проверки ответа попадает не к доказательству, а к более позднему разделу о комментарии.

### Исправление

```json
"href": "#sec-dd"
```

После исправления удалить дубли рассказа о степени, иначе anchor всё равно ведёт к перегруженному повторениями блоку.

---

## GILL-CONTENT-080 — вопрос о `pactum salutis` ведёт к общей систематике, а не к специальному разделу  
**Статус:** CONFIRMED  
**Severity:** P1

Quiz Q3:

```text
anchor / sourceRef → #sec-systematics
```

Но специальный подробный раздел:

```text
#sec-pactum
```

Кроме того, похожий материал уже присутствует раньше в `#sec-covenant`.

### Исправление

Сначала устранить дублирование `sec-covenant` / `sec-pactum`, затем оставить один canonical anchor:

```text
#sec-pactum
```

---

## GILL-CONTENT-081 — Q1 приписывает Уистону мотив “недостойно серьёзного богослова”  
**Статус:** EDITORIAL INFERENCE PRESENTED AS EXPLANATION  
**Severity:** P1

Primary anecdote сообщает, что Уистон отказался идти слушать Гилла, узнав о folio на Песнь Песней.

Quiz explanation добавляет:

> “Для Уистона это было чем-то недостойным серьёзного богослова.”

Это возможная интерпретация, но не цитата и не необходимый вывод. Причина могла быть связана с его неприятием каноничности / аллегорического прочтения Песни, а не с общей оценкой “серьёзности богослова”.

### Исправление

```text
Уистон не объяснил мотив подробнее; Риппон иронически отозвался о таком основании отказа.
```

---

## GILL-CONTENT-082 — Q4 hardcodes конкретные Таргумы без ссылки на место в издании  
**Статус:** NEEDS PRIMARY COMMENTARY CHECK  
**Severity:** P1

Quiz делает фактологическим правильным ответом:

```text
Таргум Онкелоса и Иерусалимский Таргум
```

Article body повторяет это, но не даёт edition/page или точную ссылку на Gill’s Genesis 1:2 note.

Поскольку quiz превращает формулировку в проверяемый факт, нужен первичный apparatus:

```text
Gill, Exposition, Genesis 1:2, edition/volume/page.
```

До этого вопрос нельзя считать research-verified.

---

## GILL-CONTENT-083 — quiz Q3 называет вывод Мюллера “оригинальным вкладом” без страницы  
**Статус:** SOURCE EXISTS; EXACT CLAIM NEEDS PAGE  
**Severity:** P1

Статья Мюллера названа, но quiz требует от читателя принять конкретную формулу:

```text
Holy Spirit = interested party
```

Нужны:

- страница Мюллера;
- точная цитата или ясно отмеченный paraphrase;
- место у Гилла, на котором строится вывод.

Иначе quiz проверяет вторичный пересказ сайта.

---

# 28. Part II: дублирование доктрины и ложная структура

## GILL-CONTENT-084 — `pactum salutis` изложен дважды почти одним текстом  
**Статус:** CONFIRMED  
**Severity:** P1 editorial/content architecture

Первое изложение находится в разделе о covenant:

- Дух как “заинтересованная сторона”;
- Мюллер и Scheiderer;
- Мф. 1; Мф. 12; Евр. 9:14;
- длинная цитата Гилла.

Позже специальный `#sec-pactum` снова содержит:

- прежние реформаты якобы ограничивали совет Отцом и Сыном;
- Дух как “заинтересованная сторона”;
- те же три доказательства;
- практически ту же цитату;
- снова Мюллер.

Это не полезное повторение, а две конкурирующие canonical версии одной доктрины.

### Решение

Оставить один раздел:

```text
#sec-pactum
```

В более раннем covenant section — одна короткая ссылка:

```text
Особенность триадной формы совета разобрана ниже.
```

---

## GILL-CONTENT-085 — “все прежние реформаты оставляли Духа наблюдателем” слишком широко  
**Статус:** NEEDS COMPARATIVE SOURCE  
**Severity:** P1

Текст перечисляет Оуэна, Витсиуса, Гейдеггера, Коккеюса, Луи де Дьё и фактически объединяет их в одну модель.

Даже если Мюллер показывает особенность Гилла, сайт должен различать:

```text
не был формальной договаривающейся стороной;
не участвовал в осуществлении;
был свидетелем;
был послан Отцом и Сыном;
не был достаточно эксплицитно включён.
```

Это разные тезисы.

### Безопасная формула

```text
По интерпретации Мюллера, Гилл эксплицировал участие Духа в вечном совете заметнее, чем многие предшественники.
```

---

## GILL-CONTENT-086 — таблица “Книга I–IV” не является структурой *Body of Divinity*  
**Статус:** CONFIRMED INTERNAL MISREPRESENTATION  
**Severity:** P0/P1

Перед таблицей сайт говорит:

```text
11 книг: 7 догматических + 4 практических.
```

Сразу после этого таблица показывает:

```text
I. Теология
II. Антропология
III. Сотериология
IV. Экклесиология
```

Это выглядит как реальные четыре книги Гилла, но является современной тематической агрегацией.

### Проблемы

- numbering конфликтует с реальными 11 books;
- категории не совпадают с original table of contents;
- “экклесиология” включает эсхатологию;
- читатель не предупреждён, что это редакционная схема.

### Исправление

Либо показать реальное оглавление, либо заголовок:

```text
Современная тематическая карта содержания — не структура оригинального издания
```

и убрать римские “Книга I–IV”.

---

## GILL-CONTENT-087 — приблизительные страницы таблицы не имеют проверяемого основания  
**Статус:** CONFIRMED  
**Severity:** P1

Числа:

```text
650 + 580 + 720 + 440 = 2390 страниц
```

не привязаны к изданию и не следуют из четырёх искусственных категорий.

Рядом приводится оценка догматической части как **1091 страницы**. Это может относиться к другому формату / изданию, но сайт не объясняет:

- формат;
- edition;
- pagination;
- входят ли Practical Divinity и appendix;
- почему авторские категории имеют точные page totals.

### Решение

Удалить page column до bibliographic reconstruction конкретного edition.

---

## GILL-CONTENT-088 — “книга 5, глава 14” конфликтует с моделью четырёх practical books  
**Статус:** CONFIRMED CROSS-PAGE/IN-PAGE CONFLICT  
**Severity:** P0

Цитата об эсхатологии подписана:

```text
Practical Divinity, book 5, chapter 14
```

Но тот же Part II утверждает:

```text
4 practical books + appendix.
```

Справочник отдельно называет Practical Divinity пяти-книжной.

Нужно сверить оригинальное оглавление. Пока citation locator нельзя считать надёжным.

---

## GILL-CONTENT-089 — “первое систематическое богословие баптиста” размножено как SEO-факт  
**Статус:** NEEDS DEFINED SCOPE  
**Severity:** P1

Тезис повторён в:

- body;
- heading;
- share text;
- quiz source label;
- metadata.

Даже если он традиционно употребляется, требуется scope:

```text
первое полное англоязычное баптистское систематическое богословие;
первое опубликованное;
первое, объединяющее doctrinal + practical;
первое среди Particular Baptists?
```

Без scope superlative становится уязвимым во всех поверхностях сразу.

---

# 29. Part II: богословские редукции

## GILL-CONTENT-090 — “оправдание → возрождение → вера” не описывает систему без дополнительных уровней  
**Статус:** CONFIRMED OVERSIMPLIFICATION  
**Severity:** P0/P1 theology

Part III переводит три аспекта оправдания у Гилла в простую стрелку порядка спасения.

Но сама статья признаёт:

```text
вечный аспект;
оправдание в воскресении Христа;
“суд совести” верующего;
первые два virtual, не actual.
```

Следовательно, одна цепочка смешивает:

- immanent act/decree;
- representative/virtual accomplishment;
- subjective reception/knowledge;
- faith as instrument/evidence.

### Требуемая формула

```text
У Гилла вечный и репрезентативный аспекты логически предшествуют вере;
субъективное получение и сознание оправдания связаны с верой во времени.
```

Даже эту формулу нужно сверить по первичному тексту и современным исследованиям.

Публичные справочные источники подтверждают, что “justification from eternity” действительно приписывается Гиллу и является спорным отклонением от обычной Westminster-formulation; значит, здесь особенно опасна упрощающая реабилитация.

---

## GILL-CONTENT-091 — eternal justification представлен то как “основание”, то как состоявшееся оправдание  
**Статус:** CONFIRMED TERMINOLOGY DRIFT  
**Severity:** P1

В разных местах:

```text
оправданы в вечном замысле;
вечное основание оправдания;
вечный акт Божьего ума;
оправдание от вечности;
virtual, not actual.
```

Это не взаимозаменяемые формулы.

Нужен glossary record с полями:

```text
Gill’s term
primary quotation
site paraphrase
critical objection
relation to 1689/WCF
subjective realization
```

---

## GILL-CONTENT-092 — free offer, proclamation, invitation и command используются как синонимы  
**Статус:** CONFIRMED CONCEPTUAL COLLAPSE  
**Severity:** P0/P1

Part II приводит Гилла:

> всеобщих предложений благодати и спасения нет, даже избранным; благодать возвещается и применяется.

Part III затем утверждает:

> проповедник должен искренне приглашать.

Spravochnik говорит:

> Gill denied offers but supported public proclamation.

Это может быть согласуемо, но только если точно определить:

```text
offer
well-meant offer
proclamation
indiscriminate preaching
command to repent
duty-faith
invitation addressed to qualified hearers
promise to all believers
```

Сейчас сайт сначала подчёркивает жёсткое отрицание, затем без текстового моста использует современную evangelical формулу “искренне приглашать”.

### Решение

Создать отдельную сравнительную таблицу терминов с первичными цитатами Гилла.

---

## GILL-CONTENT-093 — “миссионерская спячка в церквях, следовавших Гиллу” — причинное обобщение  
**Статус:** NEEDS QUANTIFIED HISTORIOGRAPHY  
**Severity:** P1

Фраза:

```text
если Бог всё предопределил, зачем трудиться для обращений?
```

звучит как авторское объяснение мотива церквей, а не исторически доказанный механизм.

Необходимо различать:

- демографический спад;
- doctrinal high Calvinism;
- lack of ministerial supply;
- social/legal context;
- later anti-mission rhetoric;
- Gill’s own congregation and publishing activity.

### Исправление

Атрибутировать конкретным историкам и показать контраргументы.

---

## GILL-CONTENT-094 — современная millennial taxonomy выдана за собственную схему Гилла  
**Статус:** CONFIRMED ANALYTICAL LAYER NOT LABELLED  
**Severity:** P1

Текст одновременно применяет:

- амилленаристское понимание;
- постмилленаризм;
- исторический премилленаризм;
- прогрессивный диспенсационализм.

Это современные классификационные линзы. Они могут быть полезны, но Gill не строил систему этими поздними labels.

### Исправление

```text
Современные исследователи по-разному классифицируют элементы его схемы...
```

Не писать “это буквальный премилленаризм” без source and definition.

---

## GILL-CONTENT-095 — “предсказал миссионерское движение” превращает дату в исполненное пророчество  
**Статус:** CONFIRMED EDITORIAL OVERREACH  
**Severity:** P1

Даже если у Гилла есть расчёт 1866–1913, вывод:

> “поразительно точное предвидение экуменического миссионерского движения”

не следует автоматически.

Проблемы:

- “экуменическое” может быть анахронично;
- missionary expansion начался раньше;
- Gill ожидал конкретные eschatological events, а не просто рост миссий;
- совпадение диапазона не равно исполнению модели.

Нужно вынести как позднейшую интерпретацию или удалить.

---

## GILL-CONTENT-096 — “единственный пастор” не следует из признания двух церковных должностей  
**Статус:** CONFIRMED INVALID INFERENCE  
**Severity:** P1 theology/polity

Gill мог учить, что ordinary offices — pastors and deacons. Из этого не следует:

```text
в каждой церкви должен быть численно один пастор.
```

Одна должность может иметь нескольких носителей.

Статья превращает биографический факт отсутствия второго пастора в doctrinal prohibition без точной цитаты.

### Требование

Найти место, где Gill прямо отвергает plurality of pastors in one congregation. Если такого текста нет:

```text
Gill served as sole pastor; this was consistent with, but not necessarily demanded by, his polity.
```

---

## GILL-CONTENT-097 — утверждение, что Гилл принял Риппона помощником, требует немедленной проверки  
**Статус:** HIGH-RISK CHRONOLOGY  
**Severity:** P0/P1

Part II говорит:

> в конце жизни Гилл принял Джона Риппона фактически как помощника.

При этом series timeline сообщает:

```text
Rippon ordained 11 Nov 1773
```

после смерти Gill в 1771.

Это не исключает краткого знакомства или проповеднической помощи молодого Rippon, но утверждение требует прямого source. Без него оно выглядит как попытка заполнить разрыв succession.

---

# 30. Part II: research rhetoric и source apparatus

## GILL-CONTENT-098 — “сопоставил все цитаты ВЗ” — абсолютное утверждение  
**Статус:** NEEDS PRIMARY DESCRIPTION  
**Severity:** P1

“Все цитаты” в Mishnah, двух Talmuds и Midrash corpus — огромный measurable claim.

Нужно знать:

- какие именно corpora имел Gill;
- считал ли он variants или excerpts;
- было ли это полным индексом;
- как Kennicott описал вклад.

До этого:

```text
собрал и сопоставил множество цитат...
```

---

## GILL-CONTENT-099 — “равен и, возможно, превосходил университетских профессоров” не research claim  
**Статус:** EDITORIAL PANEGYRIC  
**Severity:** P2

Фраза допустима в авторском эссе, но рядом с точной историей Kennicott она маскируется под вывод из источника.

Либо атрибутировать, либо заменить:

```text
получил признание университетских гебраистов, несмотря на отсутствие университетского образования.
```

---

## GILL-CONTENT-100 — таблица “метод Гилла” является современной реконструкцией  
**Статус:** CONFIRMED  
**Severity:** P1/P2

Категории:

```text
textual criticism
linguistics
historical context
Scripture interprets Scripture
Fathers
rabbinics
dogmatic integration
```

могут быть хорошим аналитическим summary, но не подписаны как synthesis и не имеют methodology/source.

### Исправление

```text
Редакционная аналитическая карта метода, составленная по выборке комментария.
```

И дать sample passages, на которых она построена.

---

## GILL-CONTENT-101 — Part II остаётся без bibliography, хотя это самая цитатная статья  
**Статус:** CONFIRMED  
**Severity:** P0/P1 research integrity

Part II включает:

- direct quotations Gill;
- Whiston;
- Hervey;
- Wesley;
- Spurgeon;
- Muller;
- Haykin;
- Kennicott;
- Baptist Encyclopedia;
- modern eschatology classification.

Но `PostArticle` содержит только SDG.

Наличие отдельного справочника не заменяет bibliography конкретной статьи: читатель не понимает, какие источники поддерживают какие sections.

---

# 31. Part III: таблица исследователей смешивает несовместимые категории

## GILL-CONTENT-102 — колонка “Позиция” содержит не позиции одного типа  
**Статус:** CONFIRMED  
**Severity:** P1

В одной колонке стоят:

```text
Гиперкальвинист
Не гиперкальвинист
Умеренно критичен
Защитник
Реформатский ортодокс
Нюансированная
Новейшее исследование
```

Это смешивает:

- классификацию Gill;
- отношение автора;
- historiographical method;
- жанр/новизну работы.

### Решение

Разделить:

```text
Классификация Gill
Определение hyper-Calvinism
Главный аргумент
Тип источника
Год/страница
```

---

## GILL-CONTENT-103 — строка Macritchie не сообщает её вывода  
**Статус:** CONFIRMED  
**Severity:** P1

В “позиции” стоит:

```text
Новейшее исследование
```

а в аргументе — только предмет thesis.

Это не позволяет читателю понять, поддерживает ли dissertation Toon, Nettles или третью модель.

Нужна страница conclusion и точный qualified verdict.

---

## GILL-CONTENT-104 — Richard Muller 2003 не имеет понятного supporting work  
**Статус:** NEEDS BIBLIOGRAPHIC CORRECTION  
**Severity:** P1

В source list есть конкретная статья Мюллера 1981 года о Spirit and Covenant.

В таблице hyper-Calvinism появляется:

```text
Richard Muller (2003) — Reformed orthodox
```

но title/page не указан. Доступная библиографическая информация за 2003 год включает review Gill’s collected works, что не доказывает именно такую classification.

Нужно указать конкретную публикацию или удалить год/строку.

---

## GILL-CONTENT-105 — Gregory Willis / Wills требует canonical identity  
**Статус:** NEEDS BIBLIOGRAPHIC NORMALIZATION  
**Severity:** P2

Имя встречается без title/page и может быть передано с ошибкой в surname.

В researcher registry должны быть:

```text
canonical Latin spelling
Russian transliteration
work
year
pages
position summary
```

---

## GILL-CONTENT-106 — David Engelsma row может смешивать его определение с вердиктом о Gill  
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P1

Engelsma известен прежде всего спором о well-meant offer и собственным определением hyper-Calvinism. Строка таблицы должна показать:

- где он прямо классифицирует Gill;
- какое определение использует;
- не проецирует ли сайт его general framework на Gill самостоятельно.

---

## GILL-CONTENT-107 — “Haykin rehabilitates Gill” задаёт verdict до анализа  
**Статус:** CONFIRMED FRAMING BIAS  
**Severity:** P1

“Реабилитирует” предполагает, что критическая сторона изначально ошибочна.

Для академической статьи лучше:

```text
Haykin предлагает ревизионистское / более защитительное прочтение...
```

и рядом Toon/Murray/Macritchie.

---

## GILL-CONTENT-108 — “Гилл учил долгу всех веровать” нельзя оставлять без Gill text  
**Статус:** NEEDS PRIMARY TEXT  
**Severity:** P0/P1

Это центральный критерий в споре о hyper-Calvinism.

Таблица приписывает тезис Nettles, а narrative затем использует его почти как установленный факт.

Нужно привести:

- exact Gill passage;
- context;
- distinction between natural duty, evangelical faith, special faith;
- competing interpretation.

---

# 32. Part III quiz: source mismatch и латинская эпитафия

## GILL-CONTENT-109 — Q1 о Wesley ведёт в раздел пяти определений hyper-Calvinism  
**Статус:** CONFIRMED  
**Severity:** P1

Claim:

```text
Haykin: Gill decisively shaped Wesley’s view of Calvinism
```

Source link:

```text
#sec-hypercalv-deep
```

Anchor label обещает пять определений hyper-Calvinism, а не Wesley/Gill polemic.

Нужен отдельный anchor для Wesley impact и точная citation Haykin page.

---

## GILL-CONTENT-110 — Q1 добавляет counterfactual, который может не принадлежать Haykin  
**Статус:** NEEDS QUOTE EXACTNESS  
**Severity:** P1

Вариант ответа:

> без Гилла антикальвинизм Уэсли мог принять другую форму.

Это сильное counterfactual conclusion. Нужна точная цитата; иначе quiz должен спрашивать только то, что автор действительно написал.

---

## GILL-CONTENT-111 — Q4 об эпитафии ведёт к богословским источникам  
**Статус:** CONFIRMED  
**Severity:** P1

`sourceRef.href`:

```text
#sec-sources-gil-theology
```

Вопрос относится к могиле и death section.

Нужен anchor:

```text
#sec-death
```

или отдельный:

```text
#sec-epitaph
```

---

## GILL-CONTENT-112 — “два латинских эпитета” — редакционная конструкция  
**Статус:** CONFIRMED  
**Severity:** P1

`semper invictus` и `fervore perpetuo ardenti` — части более длинного синтаксического периода, а не обязательно два официально выделенных эпитета.

Quiz превращает авторский literary reading в единственный факт.

### Безопасный вопрос

```text
Какие образы автор статьи выделяет в эпитафии?
```

Но academic quiz лучше спрашивать факт, а не интерпретацию.

---

## GILL-CONTENT-113 — латинская транскрипция содержит грамматически подозрительные формы  
**Статус:** NEEDS DIPLOMATIC SOURCE CHECK  
**Severity:** P0/P1 text integrity

В current text:

```text
preconis evangelii insignia
defensoris ... strenni
laboribusque per magnis
```

Формы выглядят как transcription/OCR errors:

- `insignia` не согласуется с genitive chain;
- `strenni` подозрительно вместо `strenui`;
- `per magnis` может быть ошибочно разделённым `permagnis`.

Нельзя строить quiz и русский перевод на невыверенной латинской строке.

### Требование

Сверить:

1. фотографию/доступную запись надписи;
2. Rippon;
3. *Bunhill Memorials*;
4. нормализованный Latin text;
5. дословный перевод.

---

## GILL-CONTENT-114 — перевод “непобедимый” может менять грамматику надписи  
**Статус:** NEEDS LATIN RE-TRANSLATION  
**Severity:** P1

Возможный смысл оборота — не “человек всегда непобедимый” как титул, а:

```text
не сломленный величайшими трудами
```

До исправления Latin quiz Q4 следует отключить.

---

## GILL-CONTENT-115 — Q3 о Spurgeon проверяет не факт, а нравственную оценку сайта  
**Статус:** CONFIRMED  
**Severity:** P2

Explanation:

```text
зрелая формула преемственности без культа личности
```

Это хорошая проповедническая оценка, но не research datum.

Quiz лучше проверять конкретное:

```text
Spurgeon praised Gill yet said he was not his Rabbi / did not bind himself to every detail.
```

После нахождения precise primary source.

---

# 33. Glossary: исторические термины и doctrinal conflation

## GILL-CONTENT-116 — “Партикулярные баптисты” определены через неполный современный TULIP  
**Статус:** CONFIRMED  
**Severity:** P1

Flip card перечисляет:

- unconditional election;
- particular redemption;
- irresistible grace;
- perseverance.

Но опускает total depravity и одновременно создаёт впечатление, что историческое название является просто синонимом поздней пяти-пунктной схемы.

Исторически “Particular” прежде всего указывает на particular redemption в отличие от General Baptists, при более широком confessional context.

### Исправление

```text
английские кальвинистские баптисты, получившие название прежде всего
из-за учения об особом искуплении; их исповедальная система была шире поздней схемы TULIP.
```

---

## GILL-CONTENT-117 — “вечное сыновство” и “вечное рождение” используются как одно и то же  
**Статус:** CONFIRMED THEOLOGICAL CONFLATION  
**Severity:** P1

Статья о discipline говорит о:

```text
eternal generation of the Son
```

Glossary card — о:

```text
eternal Sonship
```

Эти учения тесно связаны, но не полностью тождественны:

- eternal Sonship отвечает, был ли Он Сыном от вечности;
- eternal generation описывает relation of origin.

Некоторые богословы могли защищать первое и по-разному формулировать второе.

Нужно две связанные entries либо одно определение с явным различением.

---

## GILL-CONTENT-118 — Sandemanianism одновременно продолжает Gill и является тем, с чем Gill боролся  
**Статус:** CONFIRMED INTERNAL CONTRADICTION  
**Severity:** P1

Ранний Part III:

```text
последователи, особенно в духе Robert Sandeman, развили Gill до крайностей.
```

Glossary:

```text
Gill and his successors fought Sandemanianism.
```

Возможны сложные отношения, но current reader получает два противоположных тезиса.

### Решение

Отдельный historical paragraph:

- Gill’s relation to Hervey;
- Sandeman’s critique of Hervey;
- chronology;
- whether Gill directly answered Sandeman;
- what later successors opposed.

---

## GILL-CONTENT-119 — glossary definitions не имеют source note  
**Статус:** CONFIRMED  
**Severity:** P1

Особенно нуждаются в источнике:

- Sandemanian saving faith;
- eternal generation;
- hyper-Calvinism;
- supralapsarian logical order;
- free offer;
- eternal justification.

Glossary — не декоративный UI; он формирует doctrinal vocabulary читателя.

---

# 34. Source apparatus Part III расположен до окончания статьи

## GILL-CONTENT-120 — “Итоговая” bibliography стоит в середине substantive narrative  
**Статус:** CONFIRMED  
**Severity:** P0/P1

После section “Первоисточники и научная литература” статья продолжает:

- Spurgeon portrait;
- Whiston;
- Mary Bayly;
- Brown donation;
- Spurgeon 1859;
- Muller / van Asselt;
- unnamed reviewer;
- additional images and legacy material.

Следовательно, source section:

- не является итоговым;
- визуально сообщает ложное завершение;
- неясно, покрывает ли следующие claims;
- разрывает narrative;
- может быть прочитан TTS/Pagefind до последующего основного текста.

### Исправление

Перенести source apparatus в настоящий конец, после последнего research claim и до quiz/SDG.

---

## GILL-CONTENT-121 — bibliography не покрывает самые сильные поздние claims  
**Статус:** CONFIRMED  
**Severity:** P1

После bibliography появляются claims, для которых нет ясной записи:

- Mary Bayly bibliographic record;
- Gill bequest to Brown;
- exact Brown holdings;
- Spurgeon foundation-stone sermon;
- van Asselt quotation;
- unnamed nineteenth-century reviewer;
- portrait/free-will smell quotation.

Нужны отдельные items and page locators.

---

## GILL-CONTENT-122 — `Commenting and Commentaries` не заменяет source исторической речи 1859 года  
**Статус:** CONFIRMED SOURCE MISMATCH RISK  
**Severity:** P1

Source list указывает Spurgeon’s *Commenting and Commentaries*.

Но later section использует:

- foundation-stone historical address/sermon;
- “not my Rabbi”;
- adoption sermon;
- portrait anecdote.

Это разные works. Нужны exact sermons/volumes.

---

## GILL-CONTENT-123 — “Spurgeon, G3 Ministries” является неправильной атрибуцией  
**Статус:** CONFIRMED  
**Severity:** P1

G3 Ministries может быть secondary host/article, но не источник слов Spurgeon.

Формат должен быть:

```text
Charles H. Spurgeon, original work/sermon, volume/page;
quoted via G3 only if original not yet located.
```

---

## GILL-CONTENT-124 — Part III source list содержит неполную запись Nettles  
**Статус:** CONFIRMED  
**Severity:** P2

```text
Tom J. Nettles. Исследования о Гилле...
```

без title/year/pages не соответствует уровню остальных entries и не позволяет проверить central claim duty-faith.

---

# 35. TOC как content integrity problem

## GILL-CONTENT-125 — Part II скрывает большую часть research из собственного TOC  
**Статус:** CONFIRMED  
**Severity:** P1

В комментарии `gillSeriesData` прямо сказано, что article вырос с 6 до 29 sections.

Но Part II TOC показывает только:

- Hebrew;
- Canticles;
- ordinances;
- eschatology;
- systematics;
- quiz.

Не представлены:

- Trinity;
- Whitefield;
- Wesley;
- covenant;
- eternal justification;
- D.D.;
- Hebrew dissertation;
- Kennicott;
- commentary;
- Habakkuk;
- pactum;
- ecclesiology;
- Whitby;
- pastoral portrait;
- deism;
- catholicity.

Для 39-минутной research-статьи TOC перестаёт быть картой текста.

---

## GILL-CONTENT-126 — Part II TOC делает H3 визуально top-level без реального H2 parent  
**Статус:** CONFIRMED STRUCTURE DRIFT  
**Severity:** P1

`sec-hebrew` — H3, но TOC делает его first/current level 2.

Это показывает, что current content hierarchy и navigation hierarchy существуют отдельно.

Нужна реальная H2/H3 reconstruction до дальнейшего research expansion.

---

## GILL-CONTENT-127 — Part III TOC не приводит читателя к death/epitaph для quiz  
**Статус:** CONFIRMED  
**Severity:** P1

Quiz спрашивает эпитафию, но mobile TOC не предлагает obvious death/epitaph row, а sourceRef отправляет к theology sources.

Это системный провал content graph: heading, TOC, quiz и sourceRef не знают друг о друге.

---

# 36. Внешняя проверка: что удалось и чего не удалось подтвердить

## Подтверждено на уровне доступных публичных справочных источников

1. Doctrine of justification from eternity действительно приписывается Gill и является предметом серьёзной критики внутри Reformed tradition.
2. Применение термина “hyper-Calvinism” к Gill реально спорно; разные определения акцентируют duty-faith, indiscriminate call и offer.
3. Между Rippon и Spurgeon действительно были Joseph Angus, James Smith и William Walters; сокращённая succession не полна.
4. Современные public summaries датируют *Doctrinal Divinity* 1767, тогда как сайт использует 1767–1769/1769; это подтверждает необходимость edition note, а не одного безоговорочного года.

## Не найден точный доступный первоисточник в этом проходе

- exact “not my Rabbi” locator;
- exact “first magnitude” locator;
- Brown 52 folios and current holdings;
- precise Chip Lambert quotation;
- exact Haykin page for three stages / Wesley shaping;
- precise Muller 2003 source;
- diplomatic Latin epitaph.

Эти пункты не объявлены ложными; они остаются `NEEDS EXACT SOURCE`.

---

# 37. P0-пакет после пятого прохода

## Отключить или исправить немедленно

1. Quiz Part II Q2/Q3 wrong anchors.
2. Quiz Part III Q1/Q4 wrong anchors.
3. Quiz Part III epitaph question до проверки Latin.
4. 4 vs 5 practical books.
5. Artificial “Book I–IV” table.
6. Simple arrow `justification → regeneration → faith`.
7. Unsupported “Rippon as Gill’s assistant”.
8. Source section в середине Part III.
9. “One pastor” как doctrinal necessity.
10. Free offer/proclamation/invitation terminology collapse.

## Затем

1. Deduplicate pactum salutis.
2. Build primary quotation table for free offer.
3. Rebuild glossary from one data source.
4. Add actual Part II bibliography.
5. Rebuild Part II TOC from real headings.
6. Verify Spurgeon and Brown claims.
7. Diplomatic-check epitaph.
8. Normalize researcher registry.

---

# 38. Новые автоматические content guards

```text
quiz sourceRef target exists
quiz sourceRef target contains relevant claim keywords
degree question → sec-dd
pactum question → canonical pactum anchor
epitaph question → epitaph/death anchor
no quiz question sourced to an unrelated bibliography section

Body of Divinity structure has one canonical book count
no synthetic table uses “Книга” unless it matches original TOC
all approximate page counts carry edition ID
no “book 5” locator if canonical model says four books

freeOffer glossary contains distinct fields:
  proclamation
  command
  invitation
  offer
  wellMeantOffer
  dutyFaith

all direct quotations:
  source author
  work
  year
  page/section
  quoteMode
  translator

bibliography appears after last substantive heading
all post-bibliography content limited to quiz/end matter
Latin strings pass approved diplomatic fixture
```

---

# 39. Итог V5

После пятого прохода главная проблема Part II–III формулируется точнее:

> Сайт собрал много реального research, но не имеет единого механизма,
> который отделяет первичную цитату от исследовательского вывода и от
> авторской богословской интерпретации.

Из-за этого один и тот же тезис проходит цепочку:

```text
сложная позиция Gill
→ короткий пересказ исследователя
→ усиленный narrative сайта
→ glossary definition
→ единственный правильный quiz answer
```

На последнем шаге исчезает вся спорность.

Следующая правильная работа — не наращивать ещё один слой текста, а построить:

```text
Claim Registry
Quotation Registry
Glossary Registry
Quiz Evidence Map
```

и только затем редактировать Part II–III.

---

# 40. Шестой проход: официальные PDF, Macritchie 2025, SBJT 25.1 и структура трудов

**Фокус:** проверка самых спорных выводов серии не по обзорным страницам, а по официальным академическим публикациям:

- *The Southern Baptist Journal of Theology* 25.1 (2021), специальный выпуск о Джоне Гилле;
- Ruth Macritchie, PhD thesis, University of Glasgow (2025);
- Christopher Green, *Themelios* 49.3 (2024);
- библиографические сведения о *Body of Doctrinal and Practical Divinity*.

**Ограничение:** официальные PDF были доступны в распознанном текстовом слое. Попытки снять screenshot страниц завершились cache miss, поэтому формулировки и страницы проверены по parsed text, но визуальная верстка PDF в этом проходе не подтверждалась.

---

# 41. SBJT 25.1 — это не “современный консенсус”

## GILL-CONTENT-128 — Spravochnik ошибочно называет SBJT 25.1 “современным консенсусом”  
**Статус:** CONFIRMED SOURCE MISCHARACTERIZATION  
**Severity:** P1

Справочник описывает специальный выпуск SBJT 25.1 как:

```text
современный консенсус о Гилле
```

Но сам выпуск содержит разные и местами противоположные оценки:

- редакционная статья прямо отвергает eternal justification Гилла и его последствия для безразличного / indiscriminate preaching;
- Michael Haykin одновременно высоко оценивает тринитаризм и благочестие Гилла, но критикует отрицание free offer;
- David Rathel делает вывод, что сотериология Гилла вела к отрицанию gospel offers и duty-faith и что попытки доказать обратное неубедительны;
- другие статьи рассматривают позитивные стороны его доктрины Завета, Троицы, экклесиологии и влияния.

Это symposium, а не consensus statement.

### Исправление

```text
Один из главных современных академических сборников о Гилле,
представляющий как защитительные, так и критические оценки.
```

---

## GILL-CONTENT-129 — Haykin ошибочно сведен к роли “защитника”  
**Статус:** CONFIRMED NUANCE LOSS  
**Severity:** P1

В таблице Part III:

```text
Michael Haykin — Защитник
обвинение в гиперкальвинизме преувеличено
```

Но в статье Haykin 2021 одновременно утверждает, что:

- Gill отрицал free offer;
- его система в этой точке вышла за пределы Писания;
- такой дисбаланс мешал страстной евангелизации и outreach;
- длительная историографическая традиция называла Gill одним из главных представителей hyper-Calvinism.

При этом Haykin действительно защищает:

- тринитарную ортодоксию Гилла;
- его пастырское благочестие;
- значение для Particular Baptists;
- полноценное участие Святого Духа в pactum salutis.

Следовательно, “защитник” — слишком грубая категория.

### Правильнее

```text
Нюансированная ревизия: высоко оценивает тринитаризм и благочестие,
но критически оценивает free-offer theology и её евангелизационные последствия.
```

---

## GILL-CONTENT-130 — “современная наука реабилитирует Гилла” не отражает официальный выпуск 2021 года  
**Статус:** CONFIRMED FRAMING ERROR  
**Severity:** P1

Текущий narrative:

```text
Современная наука, особенно Haykin, во многом реабилитирует Gill.
```

Создаёт линейную схему:

```text
старые критики ошибались
→ новые исследователи оправдали Gill
```

Официальный выпуск SBJT показывает другую картину:

```text
переоценка отдельных обвинений
+ признание pastoral/Trinitarian strengths
+ сохранение серьёзной критики eternal justification,
  denial of offers and duty-faith.
```

### Исправление

```text
Современные исследователи пересматривают карикатурные оценки Гилла,
но не пришли к единому оправдательному выводу. Многие по-прежнему считают
его позиции по eternal justification, duty-faith и gospel offers
существенно проблематичными.
```

---

# 42. Macritchie 2025: current summary переворачивает вывод диссертации

## GILL-CONTENT-131 — Spravochnik даёт противоположный вывод Macritchie  
**Статус:** CONFIRMED MAJOR RESEARCH ERROR  
**Severity:** P0

Справочник говорит, что Macritchie:

```text
показывает, что Гилл разделял предпосылки школы,
но не её радикальные выводы.
```

Официальная PhD thesis утверждает существенно обратное:

- Hussey, Skepp, Gill и Brine рассматриваются как original hyper-Calvinists;
- Gill придал hyper-Calvinism систематическую связность;
- evidence помещает Gill в central stream of hyper-Calvinistic theology;
- все четыре автора соответствуют принятым критериям hyper-Calvinism;
- Gill отрицал duty-faith;
- Gill систематизировал vigorous denial of general offers and duty of faith/repentance;
- попытки Nettles вывести Gill из этой классификации Macritchie считает неубедительными и основанными на принятии собственных distinctions Gill.

Это не нюанс формулировки, а инверсия вывода источника.

### Немедленное исправление

```text
Macritchie относит Гилла к центральной линии раннего гиперкальвинизма:
по её выводу, он систематизировал отрицание общего предложения Евангелия
и обязанности невозрождённых к евангельской вере и покаянию.
```

Рядом обязательно указать, что это **её исследовательский вывод**, а не бесспорный consensus.

---

## GILL-CONTENT-132 — строка Macritchie в таблице скрывает её реальную позицию  
**Статус:** CONFIRMED  
**Severity:** P1

Таблица Part III ставит:

```text
Позиция: Новейшее исследование
Аргумент: Сопоставительный анализ Hussey, Skepp, Gill, Brine
```

Это сообщает только дату и тему, но не вывод.

### Исправленная строка

```text
Классификация:
Гилл принадлежит центральной линии раннего hyper-Calvinism.

Ключевой аргумент:
он систематизировал отрицание general gospel offers и duty-faith,
развивая distinctions между natural и evangelical faith/repentance.
```

Добавить chapter/page conclusion.

---

## GILL-CONTENT-133 — Macritchie прямо оспаривает Nettles, чего таблица не показывает  
**Статус:** CONFIRMED  
**Severity:** P1

Текущая строка Nettles:

```text
Не гиперкальвинист;
Gill учил о долге всех веровать.
```

Диссертация Macritchie:

- прямо разбирает Nettles;
- считает, что он принимает различения Gill без достаточной критики;
- утверждает, что Nettles неверно представляет позицию Gill;
- заключает, что Gill отрицал duty-faith в собственно евангельском смысле.

### Требование к таблице

Нельзя оставлять отдельные строки как независимые мнения. Нужна колонка:

```text
Кто непосредственно оспаривает этот вывод
```

Для Nettles:

```text
Rathel; Macritchie
```

---

## GILL-CONTENT-134 — thesis label “первое системное исследование всей четвёрки” требует точной авторской формулы  
**Статус:** NEEDS INTRODUCTION WORDING  
**Severity:** P2

Thesis действительно посвящена сопоставлению Hussey, Skepp, Gill и Brine. Но superlative “первое” следует оставлять только если Macritchie сама формулирует novelty claim в introduction.

Без прямого locator безопаснее:

```text
новейшее специальное сравнительное исследование четырёх авторов
```

---

# 43. Practical Divinity: структура установлена официальным академическим источником

## GILL-CONTENT-135 — Practical Divinity состоит из четырёх книг  
**Статус:** CONFIRMED  
**Severity:** P0 factual correction

Официальная статья SBJT, подробно излагающая структуру *Body of Divinity*, указывает:

```text
Doctrinal Divinity — 7 books
Practical Divinity — 4 books
```

Содержание Practical Divinity:

1. внутреннее поклонение и благочестие;
2. церковь, служители и публичное поклонение;
3. установления и public worship;
4. частные, домашние и гражданские обязанности.

Следовательно, Spravochnik:

```text
Practical Divinity — 5 books
```

фактически неверен.

---

## GILL-CONTENT-136 — “Practical Divinity, book 5, chapter 14” невозможно  
**Статус:** CONFIRMED INVALID LOCATOR  
**Severity:** P0

Эсхатологическая цитата подписана:

```text
Practical Divinity, книга 5, глава 14
```

Но у Practical Divinity нет пятой книги.

Тема “Of the Spiritual Reign of Christ” относится к эсхатологической части Doctrinal Divinity. По структуре SBJT эсхатология находится в **Doctrinal Divinity, book 7**.

Вероятный правильный locator:

```text
A Body of Doctrinal Divinity, Book VII, chapter XIV
```

Но перед production patch нужно сверить конкретное издание и заголовок главы.

---

## GILL-CONTENT-137 — приложение о крещении прозелитов не нужно превращать в пятую книгу  
**Статус:** CONFIRMED CLASSIFICATION ERROR  
**Severity:** P1

Отдельная dissertation о Jewish proselyte baptism могла печататься вместе с *Body of Divinity* или в том же томе. Это не делает её пятой книгой *Practical Divinity*.

Нужно различать:

```text
основная структура произведения
приложение / dissertation
физический состав тома конкретного издания
```

---

## GILL-CONTENT-138 — artificial Book I–IV table подтверждённо не совпадает с оригиналом  
**Статус:** CONFIRMED  
**Severity:** P0/P1

Официальное описание оригинальной структуры даёт:

```text
7 doctrinal books + 4 practical books
```

Современная таблица сайта:

```text
I. Theology
II. Anthropology
III. Soteriology
IV. Ecclesiology
```

не является структурой Gill.

Следовательно, её нельзя подписывать колонкой “Книга”.

### Варианты

1. удалить;
2. переименовать в “Тематическая карта редакции”;
3. заменить настоящим 11-book outline.

---

# 44. Какие “первые” claims теперь подтверждены, но только с точным scope

## GILL-CONTENT-139 — “первая баптистская систематика” подтверждается при уточнённой формуле  
**Статус:** UPGRADED TO CONFIRMED WITH SCOPE  
**Severity:** P2 wording

Christopher Green, ссылаясь на Timothy George, называет труд Gill:

```text
the first complete systematic exposition of Christian doctrine
written by a Baptist
```

Поэтому корректная русская формула:

> первое полное систематическое изложение христианского учения, написанное баптистом.

Не расширять до:

- первого баптистского богословия вообще;
- первой систематики без слова “полное”;
- первой систематики во всех языках и традициях без source scope.

---

## GILL-CONTENT-140 — полный verse-by-verse комментарий также подтверждён с scope  
**Статус:** UPGRADED TO CONFIRMED WITH SCOPE  
**Severity:** P2

Green также называет Gill автором:

```text
первого написанного баптистом построчного комментария на всю Библию
```

Текущий тезис можно сохранить, если:

- “построчный” соответствует `verse-by-verse`;
- “на всю Библию” не смешивается с числом volumes конкретного edition;
- источник указан рядом.

---

## GILL-CONTENT-141 — Green поддерживает core claim о Church of England Articles, но не военную метафору  
**Статус:** PARTLY CONFIRMED / RHETORIC OVERSTATED  
**Severity:** P2

Green действительно показывает, что Gill творчески использовал 39 Articles:

- для regenerate church membership;
- для congregational polity;
- утверждая, что Baptist practice реализует declared principles Англиканской церкви последовательнее.

Но фраза сайта:

```text
атаковал оппонента его же оружием
```

сильнее академической формулировки Green.

### Лучше

```text
творчески использовал формулировки Англиканской церкви,
чтобы утверждать, что баптистская практика последовательнее реализует
её собственное определение видимой церкви.
```

---

# 45. Muller, dates и bibliographic normalization

## GILL-CONTENT-142 — “Richard Muller (2003)” вероятно ошибочный год  
**Статус:** HIGH-CONFIDENCE BIBLIOGRAPHIC ERROR  
**Severity:** P1

Ключевой essay:

```text
Richard A. Muller, “John Gill and the Reformed Tradition”
```

публиковался в сборнике Haykin о Gill в **1997 году**.

Именно эта работа обычно используется для размещения Gill внутри Reformed scholastic tradition.

Таблица Part III указывает “Muller (2003)” без названия работы.

### Действие

- либо заменить на 1997 и дать полную запись;
- либо найти конкретную публикацию Muller 2003, из которой взят verdict;
- не оставлять год без supporting work.

---

## GILL-CONTENT-143 — степень D.D. имеет конфликт 1747/1748 в современных источниках  
**Статус:** NEEDS INSTITUTIONAL ARCHIVE  
**Severity:** P1

Сайт и Baptist Encyclopedia дают 1748.

Одна из статей официального SBJT issue указывает 1747.

Это может быть связано с:

- датой решения;
- датой diploma;
- old/new dating;
- ошибкой вторичного источника.

До проверки Marischal College / Aberdeen archive не следует объявлять один год окончательно установленным.

---

## GILL-CONTENT-144 — chronology commentary смешивает original publication, completion и later editions  
**Статус:** CONFIRMED BIBLIOGRAPHIC MODEL PROBLEM  
**Severity:** P1

В серии встречаются модели:

```text
NT 1746–1748
OT начинается 1748
OT 1763–1766
9 folio volumes
6-volume reprint
```

Они могут все относиться к разным bibliographic layers:

- first issue in parts;
- original folio volumes;
- completion dates;
- later collected edition/reprint.

Нужна edition-aware таблица:

```text
work
part
first publication
completion
original number of volumes
consulted edition
later reprint pagination
```

Иначе каждая страница считает volume/date по своей логике.

---

# 46. Free offer и eternal justification: официальный issue опровергает мягкую редакцию сайта

## GILL-CONTENT-145 — “Gill искренне приглашал всех” не подтверждён проверенными academic sources  
**Статус:** CONFIRMED SOURCE CONFLICT  
**Severity:** P0/P1

Part III утверждает:

```text
проповедник должен искренне приглашать
```

Но проверенные статьи SBJT:

- описывают Gill как отрицающего free offer;
- Rathel заключает, что Gill отрицал gospel offers и duty-faith;
- Haykin критикует отрицание offers и его практические последствия;
- Macritchie также относит Gill к отрицанию general offers and duty-faith.

Это не доказывает, что Gill никогда не использовал invitational language в любой форме. Но current categorical sentence не имеет достаточного textual basis.

### До первичной цитаты Gill

Удалить или заменить:

```text
Гилл поддерживал публичное и безразличное по аудитории провозглашение Евангелия,
но вопрос о том, признавал ли он обязанность каждого невозрождённого
к евангельской вере и искреннее предложение Христа каждому слушателю,
остаётся предметом прямого спора.
```

---

## GILL-CONTENT-146 — “Nettles доказал duty-faith Gill” нельзя подавать как итог  
**Статус:** CONFIRMED ACTIVE SCHOLARLY DISPUTE  
**Severity:** P1

Rathel и Macritchie не просто предлагают другую классификацию. Они прямо считают аргументы защиты неубедительными.

Поэтому формула таблицы:

```text
Gill учил долгу всех веровать
```

должна быть:

```text
Nettles считает, что Gill признавал duty-faith в достаточном смысле;
Rathel и Macritchie утверждают, что Gill’s distinctions фактически
исключают обязанность невозрождённых к saving/evangelical faith.
```

---

## GILL-CONTENT-147 — схема “первые два оправдания virtual, не actual” не найдена в проверенной статье Haykin 2021  
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P1

Проверенные статьи issue чаще описывают Gill через:

- active / passive justification;
- esse / bene esse;
- eternal act;
- representative justification in resurrection;
- knowledge and comfort in conscience.

До нахождения точного Haykin source формулу:

```text
первые два — virtual, not actual
```

нельзя уверенно приписывать Haykin 2021.

---

## GILL-CONTENT-148 — Rathel даёт более точную схему, чем стрелка сайта  
**Статус:** CONFIRMED  
**Severity:** P1

В проверенном тексте Rathel:

- active justification logically precedes conversion, regeneration and faith;
- faith не сообщает justification its being (`esse`);
- faith сообщает knowledge, comfort, enjoyment (`bene esse`).

Это всё ещё спорное чтение Gill, но оно точнее, чем:

```text
justification → regeneration → faith
```

### Рекомендуемая аналитическая схема

```text
вечный active act / decree
→ representative accomplishment in Christ
→ regeneration and faith in time
→ passive/subjective knowledge and enjoyment in conscience
```

Каждый уровень снабдить primary Gill locator и opposing critique.

---

## GILL-CONTENT-149 — 1689 Confession conflict должен быть раскрыт, а не спрятан  
**Статус:** CONFIRMED IMPORTANT THEOLOGICAL CONTEXT  
**Severity:** P1

Официальный SBJT issue обращает внимание, что 1689 Confession отрицает personal justification до применения Христом во времени.

Если сайт защищает Gill как Particular Baptist, он обязан показать tension:

```text
Gill’s formulation
vs.
confessional wording traditionally received by Particular Baptists
```

Без этого читатель получает впечатление полной тождественности Gill и 1689 tradition.

---

# 47. Primary locator package, который нужно встроить в статьи

## Part II

### Pactum salutis

Добавить:

```text
Michael A. G. Haykin, SBJT 25.1 (2021), section on Gill and the Spirit;
Richard A. Muller, “The Spirit and the Covenant...”, Foundations 24 (1981).
```

Указать страницы после final PDF page reconciliation.

### Body structure

Добавить academic outline:

```text
Doctrinal Divinity: 7 books
Practical Divinity: 4 books
```

### Free offer

Добавить:

```text
Gill quotation in Sermons and Tracts, vol. III;
Haykin 2021 analysis;
Rathel 2021 counter-analysis;
Macritchie 2025 chapter/conclusion.
```

## Part III

### Hyper-Calvinism table

Для каждой строки:

```text
exact work
year
page
definition used
verdict
direct opponent
```

### Eternal justification

Отдельно:

```text
Gill primary chapter
1689 Confession wording
Rathel analysis
Walden 2024 revision
Macritchie conclusion
```

---

# 48. Source correction matrix V6

| Current formulation | Official source finding | Required status |
|---|---|---|
| SBJT = modern consensus | issue contains conflicting verdicts | Rewrite |
| Haykin = defender | praise + explicit criticism of free offer and evangelism | Rewrite |
| Macritchie softens hyper-Calvinism | she places Gill in central hyper-Calvinist stream | Factual correction |
| Gill shared premises but not conclusions | thesis says he systematized denial of offers/duty-faith | Factual correction |
| Practical Divinity = 5 books | official academic outline = 4 books | Factual correction |
| Practical Book 5, ch. 14 | impossible locator; eschatology belongs doctrinal Book 7 | Factual correction |
| First Baptist systematic theology | confirmed only as first complete systematic exposition | Keep with scope |
| First Baptist whole-Bible commentary | confirmed as first Baptist verse-by-verse whole-Bible commentary | Keep with scope |
| Muller 2003 | canonical essay appears in 1997 collection | Correct/verify |
| Gill sincerely invited all | conflicts with Rathel/Macritchie/Haykin | Remove or qualify |
| modern scholarship rehabilitates | modern scholarship remains divided | Rewrite |

---

# 49. Updated P0 queue after V6

1. Correct Macritchie summary in Spravochnik.
2. Correct Practical Divinity book count.
3. Remove invalid `Practical Divinity, Book 5, chapter 14`.
4. Disable or rewrite quiz items built on unstable research conclusions.
5. Rewrite “modern scholarship rehabilitates Gill.”
6. Rewrite Haykin row.
7. Rebuild Macritchie and Nettles rows as a direct dispute.
8. Remove unsupported “sincere invitation” statement.
9. Replace synthetic Book I–IV table.
10. Add bibliography to Part II.
11. Move Part III bibliography to actual end.
12. Add 1689 Confession tension to eternal-justification section.
13. Normalize Muller citation/year.
14. Build edition-aware works chronology.

---

# 50. Что в этом проходе не было подтверждено

Остаются без точного primary/institutional locator:

- Gill’s Brown donation: 52 folio volumes and present holdings;
- exact wording/location of Spurgeon’s “not my Rabbi”;
- exact “star of the first magnitude” locator;
- exact Chip Lambert wording;
- diplomatic Latin epitaph;
- exact Aberdeen diploma date;
- exact Haykin source for “three stages / virtual not actual.”

Эти claims не удаляются автоматически, но не должны использоваться:

- как quiz correct answer;
- как SEO/share superlative;
- как безусловная прямая цитата;
- без `needs-verification` marker в Claim Registry.

---

# 51. Итог шестого прохода

Наиболее серьёзная новая находка — **не отдельная дата и не отдельная цитата**, а исследовательская инверсия:

```text
Macritchie 2025:
Gill систематизировал central hyper-Calvinist theology
и отрицал general offers / duty-faith

Справочник:
Gill разделял предпосылки,
но не радикальные выводы
```

Это меняет смысл источника на противоположный.

Вторая по важности проблема — официальный источник окончательно подтверждает:

```text
Practical Divinity = 4 books
```

Следовательно, сразу несколько элементов сайта — справочник, locator эсхатологии и synthetic structure — требуют фактического исправления.

Дальнейшая работа должна идти по principle:

```text
никакой “реабилитации” или “осуждения” заранее;
каждая позиция — через собственное определение,
первичную цитату и прямой академический спор.
```

---

# 52. Седьмой проход: page-level evidence map и закрытие спорных классификаций

**Фокус:** точные страницы официальных PDF, на которых основаны выводы о:

- Macritchie 2025;
- споре Macritchie / Rathel / Nettles;
- free offer;
- eternal justification;
- 1689 Confession;
- структуре Doctrinal / Practical Divinity;
- статусе пока не найденных утверждений о Spurgeon, Brown и Aberdeen.

**PDF visual note:** была предпринята обязательная попытка screenshot страниц официальных PDF. Веб-инструмент вернул `cache miss` для обеих публикаций. Поэтому этот проход основан на полном parsed-text слое официальных PDF с номерами PDF-страниц; визуальное соответствие строк печатной странице остаётся отдельной проверкой.

---

# 53. Macritchie: точная карта страниц

## GILL-CONTENT-150 — thesis сама называет Gill одним из четырёх original hyper-Calvinists  
**Статус:** CONFIRMED PRIMARY ACADEMIC SOURCE  
**Severity:** P0 correction

Введение диссертации, PDF p. 10:

```text
The objective of this thesis is to analyse the writings
of four original hyper-Calvinists...
```

Далее Gill и Brine прямо описаны как авторы, через которых theology была:

```text
consolidated and disseminated
```

И ещё сильнее:

```text
It was in John Gill that hyper-Calvinism “found its cohesion”.
```

### Вывод для сайта

Формула справочника:

```text
Gill shared premises but not radical conclusions
```

не может использовать Macritchie как поддержку. Она выражает противоположный тезис.

---

## GILL-CONTENT-151 — Macritchie ограничивает предмет исследования, что сайт обязан сообщать  
**Статус:** CONFIRMED IMPORTANT CAVEAT  
**Severity:** P1

На PDF pp. 10–11 автор объясняет:

- thesis изучает именно hyper-Calvinism внутри первичных текстов;
- не пытается охватить все остальные области огромного корпуса Gill;
- концентрация на спорной сотериологии не должна приниматься за общую оценку всего его богословия;
- задача — максимально внимательно учитывать Gill’s own vocabulary and classifications.

### Почему это важно

Сайт не должен превращать вывод:

```text
Gill belongs to hyper-Calvinist stream in the studied soteriological questions
```

в тотальную характеристику:

```text
всё богословие Гилла сводится к гиперкальвинизму.
```

Но также нельзя использовать широту его трудов, чтобы отменить конкретный вывод thesis.

---

## GILL-CONTENT-152 — Macritchie прямо утверждает, что Nettles misrepresents Gill  
**Статус:** CONFIRMED  
**Severity:** P0/P1 table correction

PDF p. 259:

```text
Nettles misrepresents Gill by claiming that he believed
the opposite of these three points.
```

Три пункта, которые Macritchie выводит из Gill:

1. Бог не требует от всех людей веры во Христа в saving/special sense;
2. служители не имеют права и силы “предлагать” Христа в universal-offer sense;
3. люди не осуждаются за отсутствие special faith, которую не способны произвести и которой Бог им не дал.

Затем Macritchie заключает:

```text
According to Nettles’ own parameters Gill hereby puts himself
undeniably in the hyper-Calvinist camp.
```

### Исправление таблицы

Строка Nettles должна содержать warning:

```text
Этот вывод прямо оспаривают Rathel и Macritchie;
Macritchie считает его неверным представлением Gill.
```

---

## GILL-CONTENT-153 — Rathel criticism of Nettles имеет точный locator  
**Статус:** CONFIRMED  
**Severity:** P1

PDF pp. 259–260 диссертации пересказывает Rathel:

- Nettles недостаточно исследует Gill’s soteriology;
- не учитывает eternal justification как key component;
- смешивает external/internal calling;
- из-за этого неверно представляет Gill в вопросе duty-faith.

Для research table это важнее общей метки:

```text
Rathel — гиперкальвинист
```

Нужно показывать **конкретный предмет разногласия**.

---

## GILL-CONTENT-154 — Macritchie фиксирует внутреннее изменение позиции Nettles  
**Статус:** CONFIRMED  
**Severity:** P1

PDF p. 261:

- в поздней статье Nettles признаёт “central point”, на котором Gill выглядит как hyper-Calvinist;
- допускает “compelling evidence”;
- при этом сохраняет прежние оговорки и не отказывается от утверждения duty-faith;
- Rathel называет результат противоречивым portrayal.

### Следствие

Таблица не может давать одну неподвижную строку:

```text
Nettles 1986 — not hyper-Calvinist
```

Нужны минимум две стадии:

```text
ранняя защита;
позднейшее частичное признание compelling evidence.
```

---

## GILL-CONTENT-155 — conclusion Macritchie даёт безусловный verdict внутри её methodology  
**Статус:** CONFIRMED  
**Severity:** P0

PDF p. 281:

```text
they met the criteria of hyper-Calvinism
according to its accepted definitions
```

О Gill:

```text
gave this theology coherence
```

и:

```text
The result was a vigorous denial of general offers of grace
and the duty of faith and repentance.
```

### Правильная русская передача

> По выводу Macritchie, Гилл придал раннему гиперкальвинизму систематическую связность; результатом стало последовательное отрицание общего предложения благодати и обязанности невозрождённых к евангельской вере и покаянию.

Обязательная маркировка:

```text
по выводу Macritchie
```

---

## GILL-CONTENT-156 — thesis подтверждает, что термин anachronistic, но считает его необходимым  
**Статус:** CONFIRMED  
**Severity:** P1 glossary nuance

PDF p. 9:

- `hyper-Calvinism` не был широко употребителен до времени Fuller;
- применительно к раннему XVIII веку он в некотором смысле анахроничен;
- автор всё же использует его для сформировавшейся distinctive theology с узнаваемыми чертами.

### Tooltip correction

Current tooltip должен добавить:

```text
Термин возник позднее описываемого периода и применяется ретроспективно.
```

Это не отменяет классификацию, но предупреждает анахроничное чтение.

---

# 54. SBJT: точная карта страниц

## GILL-CONTENT-157 — 1689 Confession quotation имеет точный locator  
**Статус:** CONFIRMED  
**Severity:** P1 source upgrade

SBJT PDF p. 16 цитирует Second London Confession 11.4:

```text
God did from all eternity decree to justify all the elect...
nevertheless, they are not justified personally,
until the Holy Spirit doth in time due actually apply Christ unto them.
```

### Для статьи

Нужно привести рядом:

- Gill’s formulation of eternal justification;
- 1689 Confession 11.4;
- объяснение различия между decree to justify и personal justification.

Это позволяет уйти от расплывчатой фразы “критическое расхождение”.

---

## GILL-CONTENT-158 — Haykin article прямо связывает eternal justification и rejection of free offer  
**Статус:** CONFIRMED  
**Severity:** P1

SBJT pp. 16–17:

```text
Gill’s development of everlasting covenant
+ eternal justification
→ rejection of free offer
```

Далее приведена собственная формула Gill:

```text
that there are universal offers of grace and salvation
made to all men, I utterly deny
```

и уточнение, что он не описывает спасение как offer даже избранным, а как:

```text
provided, procured, published/revealed, applied
```

### Следствие

Part II правильно показывает denial of universal offers, но Part III не может без отдельной первичной цитаты добавлять противоположное:

```text
Gill insisted the preacher sincerely invite all.
```

---

## GILL-CONTENT-159 — distinction proclamation / offer подтверждён первичным Gill через Haykin  
**Статус:** CONFIRMED  
**Severity:** P1 glossary architecture

SBJT p. 17 предоставляет точную основу:

```text
preached / published / revealed
≠
offered
```

Следовательно, glossary registry должен иметь отдельные поля:

```text
proclamation
offer
invitation
command
application
```

Current prose смешивает их.

---

## GILL-CONTENT-160 — `esse / bene esse` имеет точную страницу и точный смысл  
**Статус:** CONFIRMED  
**Severity:** P1 source upgrade

SBJT p. 45:

```text
Faith adds nothing to the esse,
only to the bene esse of justification.
```

В анализе Rathel:

- active justification — eternal, in foro Dei;
- passive justification — declarative in conscience, in time;
- faith относится к knowledge and comfort;
- faith не является prerequisite к being of justification.

### Исправление Spravochnik

Нельзя оставлять:

```text
различать esse / bene esse
```

без определения.

Нужно:

```text
esse — само бытие/наличие оправдания;
bene esse — его осознанное благополучие, знание, утешение и переживание в совести.
```

При этом отметить, что это изложение спорной схемы Gill, а не нейтральный confessional consensus.

---

## GILL-CONTENT-161 — простая стрелка сайта частично отражает Rathel, но теряет active/passive distinction  
**Статус:** REFINED  
**Severity:** P1

SBJT p. 45 действительно говорит:

```text
active justification precedes conversion, regeneration and faith
```

То есть текущая стрелка не полностью выдумана.

Но она всё равно дефектна, потому что:

- не говорит “active justification”;
- не показывает passive justification in conscience;
- смешивает eternal act и experienced order;
- создаёт впечатление, будто Gill учил переживаемому оправданию до веры.

### Корректная короткая схема

```text
active justification (eternal, in foro Dei)
→ regeneration and faith in time
→ passive/declarative justification in conscience
```

И сразу рядом — критика 1689 Confession / Rathel / Haykin.

---

## GILL-CONTENT-162 — структура 7+4 зафиксирована на SBJT pp. 94–95  
**Статус:** CONFIRMED  
**Severity:** P0 source upgrade

SBJT:

```text
Doctrinal Divinity:
Book 1 — God
Book 2 — acts ad intra / covenant
Book 3 — acts ad extra / creation / fall
Book 4 — covenant of grace / law and gospel
Book 5 — Christology
Book 6 — atonement and application
Book 7 — eschatology

Practical Divinity:
4 books
```

Это позволяет заменить synthetic four-category table на настоящий outline.

---

## GILL-CONTENT-163 — ordinances находятся в Practical Book Three  
**Статус:** CONFIRMED  
**Severity:** P1

SBJT p. 95:

```text
Book Three:
baptism
Lord’s Supper
preaching
public prayer
singing
```

Это подтверждает важное различение:

- Gill группирует не только baptism/Supper;
- public ordinances/work of worship включают более широкий набор.

Current heading “два таинства” сужает его практическую taxonomy.

---

## GILL-CONTENT-164 — private worship / family section находится в Practical Book Four  
**Статус:** CONFIRMED  
**Severity:** P1

SBJT p. 95:

```text
marriage
childrearing
master/servant relations
civil magistrates
good works
Ten Commandments
```

Это можно использовать для реального content map вместо вымышленных page totals.

---

# 55. Новые выводы для hyper-Calvinism table

## GILL-CONTENT-165 — таблица должна различать “denial of offer” и “denial of duty-faith”  
**Статус:** CONFIRMED  
**Severity:** P1

Из точных страниц видно:

- все стороны признают, что Gill отрицал offer-language;
- главный спор — означает ли его система отрицание duty-faith;
- Nettles говорит “нет”;
- Rathel и Macritchie говорят “да”;
- часть защитников сужает definition hyper-Calvinism;
- критики используют более широкую историческую definition.

Текущая таблица скрывает core dispute.

### Новые колонки

```text
Отрицание offer?
Отрицание duty-faith?
Определение hyper-Calvinism
Вердикт о Gill
Primary passages
Direct critics
```

---

## GILL-CONTENT-166 — таблица должна показывать methodological bias thesis  
**Статус:** CONFIRMED  
**Severity:** P2 fairness

Macritchie:

- открыто считает four authors original hyper-Calvinists;
- thesis защищает пригодность самого термина;
- оценивает их по выбранной taxonomy;
- одновременно заявляет об extensive primary-source engagement.

Для честности table должна отражать не только conclusion, но и methodological starting point.

Это не дисквалифицирует thesis, но предотвращает превращение её в нейтральный арбитраж без предпосылок.

---

## GILL-CONTENT-167 — current phrase “пять конкурирующих определений” не соответствует реальному количеству позиций  
**Статус:** CONFIRMED  
**Severity:** P2

Part III содержит около десяти исследователей, а deeper section/quiz label продолжает говорить о “пяти определениях”.

Нужно различить:

```text
определения термина
исследовательские verdicts о Gill
```

Это разные наборы и разное количество элементов.

---

# 56. Claims, которые targeted search не смог подтвердить

## GILL-CONTENT-168 — Spurgeon “he is not my Rabbi” остаётся без exact locator  
**Статус:** NEEDS EXACT PRIMARY SOURCE  
**Severity:** P1

Проведён поиск:

- exact phrase;
- variants `Gill / Rabbi / predecessor`;
- foundation-stone event;
- New Park Street Pulpit;
- Spurgeon archive/CCEL domain queries.

Точная searchable primary record в доступном индексе не найдена.

### Политика до верификации

Можно оставить только с формулой:

```text
цитата, приписываемая Сперджену; exact sermon locator требует проверки
```

Не использовать в quiz как безусловно проверенный факт.

---

## GILL-CONTENT-169 — “star of the first magnitude” не найдено в проверенных searchable texts  
**Статус:** NEEDS EXACT PRIMARY SOURCE  
**Severity:** P1

Targeted exact-phrase search и поиск в Macritchie не дали совпадения.

Это может быть:

- другой перевод;
- вариант wording;
- secondary paraphrase;
- речь, плохо индексируемая OCR.

До locator:

- убрать номер sermon XLV, если он не проверен;
- не ставить кавычки вокруг русского текста как точной цитаты.

---

## GILL-CONTENT-170 — событие foundation stone 16 августа 1859 подтверждается, содержание Gill speech — нет  
**Статус:** EVENT CONFIRMED / QUOTATIONS UNVERIFIED  
**Severity:** P1

Само событие laying of first stone 16 August 1859 подтверждается историческими источниками.

Но current Part III объединяет в одном абзаце:

- дату события;
- “star of first magnitude”;
- “not my Rabbi”;
- оценку Body of Divinity;
- Adoption sermon.

Нельзя считать весь paragraph подтверждённым только потому, что дата церемонии верна.

### Разделить на claim records

```text
event date
speech title/edition
Gill description
Rabbi phrase
adoption sermon
```

---

## GILL-CONTENT-171 — Brown donation не подтверждён доступным официальным каталогом  
**Статус:** STILL NEEDS INSTITUTIONAL VERIFICATION  
**Severity:** P0/P1

Targeted searches по:

- brown.edu;
- Brown library/repository catalog;
- Rhode Island College;
- exact “52 folio volumes”;
- Manning;

не вернули официальной catalog/archive записи.

Это не доказывает, что donation не было. Но current claim включает сразу пять independently verifiable statements:

1. Gill был одним из первых donors;
2. передал complete set of works;
3. передал 52 folio patristic volumes;
4. Manning назвал gift largest;
5. книги до сих пор хранятся в Brown.

Каждый пункт требует отдельного locator.

### До подтверждения

Не публиковать весь package как единый установленный факт.

---

## GILL-CONTENT-172 — source list Brown опирается на secondary historical overviews  
**Статус:** CONFIRMED  
**Severity:** P1

Part III bibliography указывает:

- J. T. Christian;
- David Spencer;
- London Lyceum overview.

Ни одна запись в current source block не является:

- Brown accession record;
- Manning letter;
- will/probate record;
- modern special-collections catalog.

Нужен Level A institutional source.

---

## GILL-CONTENT-173 — Aberdeen year remains 1747/1748 conflict  
**Статус:** UNRESOLVED  
**Severity:** P1

Большинство accessible summaries используют 1748.

Один academic source in SBJT uses 1747.

Targeted search не обнаружил accessible official Aberdeen archival record.

### Правильная editorial form

```text
Степень была присуждена в 1747/1748 году;
большинство поздних биографий указывает 1748.
Точная дата диплома требует архивной проверки.
```

Либо временно оставить 1748 со сноской:

```text
по Rippon / Baptist Encyclopedia
```

не называя вопрос окончательно закрытым.

---

# 57. Source status badges, необходимые для серии

Каждый research-rich claim должен иметь один из статусов:

```text
PRIMARY VERIFIED
ACADEMIC VERIFIED
CONTESTED
SECONDARY TRADITION
NEEDS EXACT LOCATOR
INTERNAL CONTRADICTION
EDITORIAL INFERENCE
```

Примеры:

```text
Macritchie conclusion — ACADEMIC VERIFIED
Gill hyper-Calvinist classification — CONTESTED
Practical Divinity = 4 books — ACADEMIC VERIFIED
Brown 52 folios — NEEDS EXACT LOCATOR
Spurgeon “not my Rabbi” — NEEDS EXACT LOCATOR
“modern scholarship rehabilitates” — EDITORIAL INFERENCE / misleading
```

---

# 58. Page-level replacement package

## Spravochnik Macritchie card

```text
Ruth Macritchie (PhD, University of Glasgow, 2025) относит Гилла
к центральной линии раннего гиперкальвинизма. По её выводу,
он придал системе связность и последовательно отрицал общее
предложение благодати и duty-faith. Диссертация сосредоточена
именно на этой области его богословия и не претендует на полную
оценку всего корпуса Гилла.
```

Sources:

```text
Introduction, PDF pp. 10–11
Debate over Gill, pp. 258–263
Conclusion, pp. 281–282
```

## Part III research framing

```text
Современная дискуссия не завершилась “реабилитацией” Гилла.
Nettles, George и ряд защитительных авторов ограничивают или
отвергают ярлык; Rathel, Macritchie, Oliver и Murray считают,
что denial of offers, duty-faith and eternal justification
поддерживают традиционную классификацию.
```

## Body structure

```text
Doctrinal Divinity — 7 books
Practical Divinity — 4 books
Appendix/dissertation — отдельно
```

---

# 59. P0 queue after V7

1. Replace inverted Macritchie summary.
2. Replace “modern consensus” label for SBJT.
3. Rewrite Haykin row.
4. Rebuild Nettles row with later caveat and direct critics.
5. Correct 5 → 4 books.
6. Correct invalid Book 5 eschatology locator.
7. Replace synthetic Book I–IV table.
8. Add exact 1689 Confession comparison.
9. Rewrite free-offer paragraph.
10. Add definitions for `esse / bene esse`.
11. Disable epitaph quiz pending diplomatic Latin.
12. Disable/qualify Spurgeon quote quiz/claims pending locator.
13. Demote Brown package pending institutional record.
14. Add source-status badges/registry.

---

# 60. Итог V7

Седьмой проход усилил два вывода.

## Первый

Проблема Macritchie теперь доказана на трёх независимых уровнях самой thesis:

```text
Introduction:
four original hyper-Calvinists; in Gill the system found cohesion

Debate:
Nettles misrepresents Gill

Conclusion:
Gill gave the system coherence;
vigorous denial of general offers and duty-faith
```

Поэтому current summary нельзя исправить косметически — его надо переписать полностью.

## Второй

Часть нерешённых ярких claims не удалось подтвердить даже targeted exact-phrase search:

```text
Spurgeon “not my Rabbi”
star of first magnitude
Brown 52 folios / current holdings
exact Aberdeen year
```

Это не повод объявить их ложными. Это повод перестать смешивать:

```text
яркое предание
+
частично подтверждённое событие
+
непроверенную точную цитату
```

в один безусловный narrative paragraph.

---

# 61. Восьмой проход: Сперджен 1861 и полный аудит исторического контекста

**Фокус:**

- разграничение церемонии закладки камня 1859 года и первой проповеди в готовом Metropolitan Tabernacle 1861 года;
- поиск проверяемой замены неподтверждённым формулам “не мой Равви” и “звезда первой величины”;
- content/research audit статьи «Исторический контекст»;
- проверка того, поддерживает ли её bibliography конкретные сильные утверждения;
- отделение закона, деноминационной структуры, богословской интерпретации и литературной реконструкции.

---

# 62. Сперджен: два события были склеены в один narrative

## GILL-CONTENT-174 — найдена проверяемая первичная формула богословской независимости Сперджена  
**Статус:** PRIMARY SERMON LOCATOR IDENTIFIED  
**Severity:** P1 source replacement

Дословная формула:

```text
he is not my Rabbi
```

по-прежнему не найдена в доступном searchable corpus.

Но найден более сильный и проверяемый смысловой эквивалент из первой проповеди Сперджена в Metropolitan Tabernacle:

```text
My venerable predecessor, Dr. Gill, has left a body of divinity
admirable and excellent in its way; but the body of divinity to which
I would pin and bind myself for ever ... is not his system of divinity
or any other human treatise, but Christ Jesus.
```

Locator:

```text
C. H. Spurgeon,
“The First Sermon at the Metropolitan Tabernacle,”
sermon no. 369,
preached Monday, 25 March 1861.
```

### Вывод

Смысл current paragraph верен:

```text
глубокое уважение + отказ считать Gill непогрешимым стандартом
```

Но неподтверждённое “he is not my Rabbi” лучше заменить проверенной цитатой.

---

## GILL-CONTENT-175 — current paragraph смешивает 16 августа 1859 и 25 марта 1861  
**Статус:** CONFIRMED EVENT CONFLATION  
**Severity:** P0/P1

Part III утверждает, что при закладке первого камня 16 августа 1859 года прозвучали:

- оценка Body of Divinity;
- “звезда первой величины”;
- “he is not my Rabbi”.

Проверяемая цитата о Gill’s Body of Divinity относится к:

```text
первой проповеди в уже открытом Metropolitan Tabernacle,
25 марта 1861 года,
sermon no. 369.
```

Следовательно, один абзац склеивает минимум два разных события:

```text
1859 — laying of foundation stone;
1861 — first sermon in completed Tabernacle.
```

### Исправление

Разделить на два блока с разными source records.

---

## GILL-CONTENT-176 — “sermon XLV” не соответствует найденному primary locator  
**Статус:** HIGH-CONFIDENCE CITATION ERROR  
**Severity:** P1

Current text:

```text
Spurgeon, Sermons, vol. 5, sermon XLV
```

Проверяемая первая проповедь в Скинии имеет номер:

```text
369
```

Это не доказывает, что иной historical address не печатался как XLV, но нынешний paragraph соединяет номер с несколькими цитатами без разделения.

### Действие

Для каждой фразы дать отдельный locator; не использовать один номер на весь paragraph.

---

## GILL-CONTENT-177 — “not my Rabbi” можно сохранить только как поздний paraphrase  
**Статус:** NEEDS EXACT LOCATOR  
**Severity:** P1

Если exact phrase всё же важна для литературного эффекта:

```text
поздняя формула, передающая позицию Сперджена;
точный первичный locator не найден.
```

Но для research article лучше использовать sermon 369 verbatim.

---

## GILL-CONTENT-178 — “star of the first magnitude” остаётся неподтверждённой точной цитатой  
**Статус:** NEEDS EXACT LOCATOR  
**Severity:** P1

Exact-phrase searches:

```text
John Gill + star of the first magnitude
Dr Gill + first magnitude
Spurgeon + Gill + first magnitude
```

не дали первичного текста.

Возможны:

- иной wording;
- secondary paraphrase;
- OCR gap;
- другая речь/книга.

До проверки:

- убрать кавычки;
- не указывать точный sermon number;
- либо пометить как позднюю характеристику.

---

## GILL-CONTENT-179 — source list Part III не содержит sermon 369  
**Статус:** CONFIRMED SOURCE GAP  
**Severity:** P1

Bibliography содержит:

```text
Commenting and Commentaries
```

Но narrative использует:

- first Tabernacle sermon;
- foundation-stone event;
- Adoption sermon;
- portrait anecdote.

Это разные источники.

Добавить минимум:

```text
C. H. Spurgeon, sermon no. 369,
“The First Sermon at the Metropolitan Tabernacle,” 25 March 1861.
```

---

# 63. Исторический контекст: происхождение английских баптистов

## GILL-CONTENT-180 — Elizabethan Settlement не “учредил Англиканскую церковь” с нуля  
**Статус:** HISTORICAL OVERCOMPRESSION  
**Severity:** P1

Timeline:

```text
1559 — учреждена государственная Англиканская церковь
```

Church of England уже имела предшествующую историю при Henry VIII и Edward VI, затем Marian restoration.

1559 корректнее описывать как:

```text
Elizabethan Religious Settlement восстановил и заново урегулировал
протестантскую государственную Church of England.
```

---

## GILL-CONTENT-181 — 1608–1612 объединяет разные события Baptist origins  
**Статус:** CONFIRMED CHRONOLOGY COMPRESSION  
**Severity:** P1

В таблице:

```text
1608–1612 — Smyth и Helwys создают первую английскую баптистскую общину.
```

Нужно различить:

```text
ок. 1609 — congregation Smyth/Helwys в Amsterdam принимает believers’ baptism;
1612 — Helwys возвращает часть общины в London,
создавая первую устойчивую Baptist church на английской земле.
```

“Первая английская” может означать:

- English-speaking congregation abroad;
- первая в England;
- начало General Baptist tradition.

Без различения фраза двусмысленна.

---

## GILL-CONTENT-182 — корни General Baptists через Dutch Mennonites упрощены  
**Статус:** CONFIRMED NUANCE LOSS  
**Severity:** P1

Table:

```text
English separatism + Dutch Mennonites
```

Smyth действительно сблизился с Waterlander Mennonites и стремился к объединению.

Но Helwys:

- не поддержал это движение;
- отделился от Smyth;
- вернулся в England;
- сохранял собственную Baptist identity.

### Исправление

```text
English Separatism; Amsterdam contact with Mennonites strongly influenced Smyth,
while Helwys rejected full Mennonite union and returned to England.
```

---

## GILL-CONTENT-183 — “две почти не пересекающиеся ветви” слишком абсолютно  
**Статус:** EDITORIAL OVERSTATEMENT  
**Severity:** P2

Particular и General Baptists имели разные confessional networks, associations и atonement theology.

Но они:

- существовали в одном dissenting environment;
- участвовали в общих controversies;
- представлены вместе в Salters’ Hall data;
- могли взаимодействовать институционально и полемически.

Лучше:

```text
две отчётливо различавшиеся и в основном раздельно организованные ветви.
```

---

## GILL-CONTENT-184 — “дрейф в унитарианство после 1719” создаёт ложную монокаузальность  
**Статус:** HISTORIOGRAPHIC OVERSIMPLIFICATION  
**Severity:** P1

Salters’ Hall был важным marker, но:

- антитринитарные процессы начались раньше;
- not all non-subscribers были Arians/Unitarians;
- regional and congregational trajectories различались;
- голосование не “создало” drift автоматически.

Формула должна говорить о символическом и институциональном marker, а не одном causal switch.

---

## GILL-CONTENT-185 — “General Baptist denomination almost disappeared” фактически неверно  
**Статус:** CONFIRMED FACTUAL ERROR  
**Severity:** P0

Table:

```text
к концу века деноминация почти исчезла.
```

В 1770 году Daniel Taylor организовал **New Connexion of General Baptists**:

- evangelical and orthodox renewal;
- active expansion in industrial Midlands;
- around 70 chapels by 1817;
- eventual union with Baptist Union in 1891.

Следовательно, старые General Baptist structures переживали серьёзный doctrinal crisis, но General Baptist tradition не “почти исчезла”.

### Исправление

```text
Старое General Baptist establishment во многих местах дрейфовало к heterodoxy;
одновременно evangelical renewal породило New Connexion в 1770 году.
```

---

## GILL-CONTENT-186 — Particular Baptist “стабильность и рост” также идеализированы  
**Статус:** NEEDS BALANCED HISTORIOGRAPHY  
**Severity:** P1

Table рисует:

```text
Particular — doctrinal stability and growth;
General — drift and near disappearance.
```

Но Particular Baptists тоже переживали:

- stagnation;
- ministerial shortages;
- high/hyper-Calvinist controversies;
- uneven local decline;
- later evangelical and missionary renewal associated with Fuller/Carey.

Нужна симметричная история обеих branches.

---

# 64. 1662 и Clarendon Code: смешение разных законов

## GILL-CONTENT-187 — “духовная родина Гилла родилась в 1662” стирает более раннюю Baptist history  
**Статус:** EDITORIAL OVERSTATEMENT  
**Severity:** P1

Particular Baptist churches and confessions existed before 1662.

Great Ejection radically enlarged and reshaped Nonconformity, но не создал:

- English separatism;
- General Baptists;
- Particular Baptists;
- Gill’s denominational lineage с нуля.

Правильнее:

```text
1662 превратил English Nonconformity в массовое и долговременное общественное явление.
```

---

## GILL-CONTENT-188 — Act of Uniformity и Five Mile Act объединены в одно последствие  
**Статус:** CONFIRMED LEGAL CONFLATION  
**Severity:** P0/P1

Section сначала описывает 24 August 1662, затем говорит, что ejected ministers потеряли:

- кафедры;
- право учить;
- право жить ближе пяти миль.

Но five-mile restriction — это **Five Mile Act 1665**, не Act of Uniformity 1662.

### Исправление

Развести chronology:

```text
1662 — ejection and conformity requirements;
1664 — conventicle restrictions;
1665 — five-mile residence/teaching restrictions unless oath taken.
```

---

## GILL-CONTENT-189 — “Act of Uniformity created Nonconformity” нуждается в caveat  
**Статус:** HISTORICAL OVERSTATEMENT  
**Severity:** P1

Nonconformity and separatism existed earlier.

Act 1662:

- institutionalized;
- enlarged;
- legally defined;
- made it a permanent mass phenomenon.

Не “создал” его абсолютно.

---

## GILL-CONTENT-190 — перечисление Baxter/Flavel/Watson как библиотеки Gill не доказано  
**Статус:** NEEDS LIBRARY CATALOGUE  
**Severity:** P1

Text says their works:

```text
войдут в библиотеку Гилла
```

Нужен:

- sale catalogue;
- surviving library list;
- citation in Gill;
- Rippon inventory.

Без этого можно сказать:

```text
стали частью dissenting reading culture, знакомой поколению Gill.
```

---

## GILL-CONTENT-191 — memory narrative о стариках, подвалах и сараях является reconstruction  
**Статус:** EDITORIAL INFERENCE  
**Severity:** P2

Фраза:

```text
старики общины помнили, как их собирали по подвалам и сараям
```

может быть правдоподобна, но не названы:

- Kettering church records;
- конкретные witnesses;
- local persecution episodes.

Пометить как historical reconstruction либо убрать документальный тон.

---

## GILL-CONTENT-192 — Gill не был просто “первым поколением без угрозы тюрьмы”  
**Статус:** OVERSTATED TOLERATION  
**Severity:** P1

Toleration Act:

- разрешал worship только при условиях;
- требовал oath/licensing/registration;
- не охватывал Catholics, nontrinitarians и других;
- не снимал civil and educational disabilities;
- enforcement мог различаться.

Лучше:

```text
первое поколение, выросшее после ограниченной легализации зарегистрированного Protestant dissent.
```

---

## GILL-CONTENT-193 — “prestigious invitations to Bristol or London” требует проверки  
**Статус:** INTERNAL/FACTUAL RISK  
**Severity:** P1

Gill сам служил в London с 1720 года.

Фраза:

```text
откажется от престижных приглашений в Bristol или London
```

поэтому как минимум сформулирована странно.

Нужно установить:

- о каком периоде;
- какая церковь/академия;
- источник;
- что именно означал “компромисс с государственной церковью”.

---

# 65. Термины Dissenter / Nonconformist / Baptist

## GILL-CONTENT-194 — предложенная трёхступенчатая система слишком жёсткая  
**Статус:** HISTORICAL TERMINOLOGY ISSUE  
**Severity:** P1

Text defines:

```text
Nonconformist — personal and broad;
Dissenter — institutional separation;
Baptist — concrete subset.
```

Историческое словоупотребление не всегда следует такой taxonomy:

- Nonconformist часто означает institutional Protestant bodies outside established church;
- Dissenter и Nonconformist во многих contexts являются почти взаимозаменяемыми;
- “separatist” — отдельная и важная категория;
- legal usage менялось по периодам.

### Исправление

Дать flexible note:

```text
термины перекрываются; смысл зависит от периода и жанра источника.
Baptist — denominational identity внутри более широкого Protestant Dissent.
```

---

# 66. Правовые ограничения и университеты

## GILL-CONTENT-195 — Test/Corporation Acts не являются единственной причиной university exclusion  
**Статус:** CONFIRMED LEGAL CAUSATION ERROR  
**Severity:** P1

Context connects:

```text
Corporation/Test Acts
→ Gill could not study/profess at Oxford or Cambridge.
```

Civil office tests and university religious tests were related but distinct legal/institutional systems.

Нужно различать:

- municipal/crown office restrictions;
- matriculation subscriptions;
- degree tests;
- fellowships and university offices;
- college statutes.

---

## GILL-CONTENT-196 — repeal in 1828 did not fully open Oxbridge  
**Статус:** CONFIRMED  
**Severity:** P1

Corporation and Test Acts were repealed in 1828.

Но university restrictions continued and were removed in stages:

```text
Oxford reforms — 1854;
Cambridge reforms — 1856;
Universities Tests Act — 1871 for remaining non-theological degrees/offices.
```

Therefore paragraph structure must not imply:

```text
1828 = end of all educational disability.
```

---

## GILL-CONTENT-197 — “could not be diplomat, officer, professor” is too categorical  
**Статус:** NEEDS OFFICE-BY-OFFICE SCOPE  
**Severity:** P2

Legal eligibility varied by:

- office;
- oath;
- communion test;
- date;
- crown/municipal/university jurisdiction.

Use:

```text
was excluded from many municipal, crown and university offices
```

instead of universal list unless each office is sourced.

---

## GILL-CONTENT-198 — “this is why Gill could not attend Oxford/Cambridge” is monocausal  
**Статус:** NEEDS BIOGRAPHICAL PRECISION  
**Severity:** P1

Dissenting status was a major structural barrier.

But actual biography also includes:

- family finances;
- ending grammar school at eleven;
- no subsequent academy route;
- age and patronage;
- subscription/admission requirements.

Correct formulation:

```text
As a Dissenter Gill faced institutional religious barriers;
his family’s limited means and early end of schooling made an Oxbridge path still less realistic.
```

---

## GILL-CONTENT-199 — `Suo Marte` literal gloss is presented as “more accurate” than idiom  
**Статус:** TRANSLATION ERROR  
**Severity:** P2

Text:

```text
“собственными силами”, или, как точнее, “своим Марсом”.
```

`Suo Marte` is an idiom:

```text
by his own efforts / on his own initiative / unaided.
```

“Своим Марсом” is etymologically literal, not a more accurate Russian translation.

### Исправление

```text
латинская идиома suo Marte — “собственными силами, без наставника”.
```

---

# 67. Dissenting academies and Baptist institutions

## GILL-CONTENT-200 — “universities for the expelled” is a metaphor, not uniform institutional status  
**Статус:** EDITORIAL LABEL  
**Severity:** P2

Dissenting academies varied greatly in:

- duration;
- curriculum;
- size;
- legal status;
- level;
- stability.

The article partly acknowledges this, but heading may suggest uniform universities.

Keep as literary heading, but clarify in first sentence:

```text
не университеты юридически, а varied private institutions,
часто дававшие university-level curriculum.
```

---

## GILL-CONTENT-201 — Gill support application needs exact Rippon locator  
**Статус:** NEEDS PRIMARY PAGE  
**Severity:** P1

Claim:

```text
London trustees rejected support because he was too young.
```

This is precise and should have:

```text
Rippon edition/page/quotation.
```

---

## GILL-CONTENT-202 — Particular Baptist Fund 1717 is not supported by current bibliography  
**Статус:** SOURCE COVERAGE GAP  
**Severity:** P1

The source list contains no dedicated history or primary rules of Particular Baptist Fund.

Need:

- foundation document;
- Rules and Orders;
- Baptist Quarterly study;
- exact date and purpose.

The earlier Rippon footnote “Written in 1800” also showed how easily Fund material can be misread; this section needs direct citation.

---

## GILL-CONTENT-203 — Bristol Academy chronology/lineage needs institutional source  
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P1

Claim package:

```text
Broadmead/Terrill/Bodenham line;
work began 1720;
separate from Particular Baptist Fund.
```

Plausible, but bibliography has no Bristol Academy institutional history.

---

## GILL-CONTENT-204 — Stepney/Regent’s Park connection is too compressed  
**Статус:** NEEDS GENEALOGICAL INSTITUTION MAP  
**Severity:** P1

The phrase:

```text
PBF line later especially associated with Stepney and Regent’s Park
```

may collapse multiple trusts, colleges, relocations and mergers.

Need a dated chain:

```text
fund/trust
→ academy
→ Stepney institution
→ Regent’s Park College
```

or remove.

---

# 68. Coffee-house section: law, geography and evidence

## GILL-CONTENT-205 — Dissenters were not legally prohibited from having synods or central structures in the stated sense  
**Статус:** CONFIRMED CATEGORY ERROR  
**Severity:** P0/P1

Opening sentence:

```text
Поскольку диссентеры по закону не могли иметь епископата, синодов
или официальных центральных структур...
```

This conflates:

- state recognition;
- Anglican establishment;
- Baptist congregational polity;
- voluntary associations;
- legal restrictions on worship.

Dissenting denominations did form:

- associations;
- assemblies;
- funds;
- ministerial networks.

Their lack of episcopacy was often theological, not simply statutory.

### Rewrite

```text
Не имея государственной церковной структуры и будучи организованы
через добровольные associations, dissenting ministers relied heavily
on informal London networks and meeting places.
```

---

## GILL-CONTENT-206 — “about 500 coffeehouses by the 1720s” needs named quantitative source  
**Статус:** NEEDS SOURCE  
**Severity:** P2

Historical estimates vary by:

- date;
- definition coffeehouse;
- London/Westminster;
- licensed/unlicensed premises.

Add a city-history source or soften:

```text
hundreds of coffeehouses.
```

---

## GILL-CONTENT-207 — `British Coffee House` identification may be wrong or ambiguous  
**Статус:** HIGH-RISK GEOGRAPHIC ERROR  
**Severity:** P1

The well-documented British Coffee House:

```text
27 Cockspur Street;
especially associated with Scots.
```

The article names British Coffee House as a Particular Baptist meeting place without address.

There were similarly named premises, including a British Coffee House in/near Fullwood’s Rents.

### Requirement

Identify:

```text
exact address;
years;
proprietor;
Baptist meeting record.
```

Do not assume every “British Coffee House” is the same place.

---

## GILL-CONTENT-208 — Hanover Coffee House Baptist role lacks primary/academic support  
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P1

Current bibliography has no:

- minute book;
- Baptist Fund record;
- ordination record;
- Baptist Quarterly article

supporting the detailed institutional role attributed to Hanover Coffee House.

---

## GILL-CONTENT-209 — George Ella cannot be sole authority for “Coffee House Association”  
**Статус:** SOURCE QUALITY ISSUE  
**Severity:** P1

George Ella may be used as a secondary interpretive author.

But a coined organizational label needs corroboration through:

- contemporary records;
- B. R. White;
- Baptist Quarterly;
- association minutes.

---

## GILL-CONTENT-210 — Gill’s suspicion of coffee-house hierarchy is inferred, not demonstrated  
**Статус:** EDITORIAL INFERENCE  
**Severity:** P1

Article moves from Gill’s congregational polity to:

```text
he viewed this informal hierarchy warily
```

without a letter, sermon or church record.

The inference may be reasonable but should be marked:

```text
his polity suggests...
```

not stated as documented attitude.

---

## GILL-CONTENT-211 — ordination by senior ministers does not prove the proposed authority theory  
**Статус:** INVALID INFERENCE  
**Severity:** P2

From the fact that senior pastors participated in ordination, article concludes:

```text
Gill accepted fellowship but did not submit to its authority.
```

The event alone cannot establish inner attitude or jurisdictional theory.

Need Gill’s explicit ecclesiological text.

---

# 69. Southwark and Whitefield

## GILL-CONTENT-212 — Southwark industrial atmosphere needs local-history sourcing  
**Статус:** SOURCE COVERAGE GAP  
**Severity:** P2

Specifics include:

- tanners;
- tanning pits;
- brewers;
- coal smoke;
- Thames fog;
- exact occupational environment of Horsleydown.

Current source list provides Kennington material but no dedicated Southwark/Horsleydown social history.

---

## GILL-CONTENT-213 — images and captions remain documentary-looking reconstructions  
**Статус:** PROVENANCE/EDITORIAL  
**Severity:** P1

Examples:

```text
underground puritan meeting;
Clarendon persecution scene;
Whitefield at Kennington;
young Gill in bookshop;
street preaching in Southwark.
```

If AI-generated or newly illustrated:

```text
Художественная реконструкция
```

must appear in caption/metadata.

---

## GILL-CONTENT-214 — “three times average dissenting congregation” needs dataset  
**Статус:** NEEDS QUANTITATIVE SOURCE  
**Severity:** P1

Claim requires:

- Gill congregation membership/attendance;
- definition of average;
- London date/sample;
- source.

Without those, remove exact multiplier.

---

## GILL-CONTENT-215 — “through two changes of pastors” before Spurgeon is false  
**Статус:** CONFIRMED FACTUAL ERROR  
**Severity:** P0

From Gill to Spurgeon the congregation passed through:

```text
John Rippon
Joseph Angus
James Smith
William Walters
Charles Spurgeon
```

And moved:

```text
Carter Lane
→ New Park Street Chapel
→ Metropolitan Tabernacle
```

Current sentence:

```text
через две смены пасторов вырастет Metropolitan Tabernacle
```

must be corrected.

---

## GILL-CONTENT-216 — Whitefield’s 30,000 is an estimate, not measured attendance  
**Статус:** SOURCE NUANCE  
**Severity:** P2

Caption already says “diary and early biographical estimates,” which is good.

Body reverts to:

```text
собирал толпы по тридцать тысяч
```

Use:

```text
по собственным/ранним оценкам — до примерно 30,000.
```

---

## GILL-CONTENT-217 — “they almost certainly heard of each other every week” is invented frequency  
**Статус:** EDITORIAL SPECULATION  
**Severity:** P2

No weekly correspondence/news source is cited.

Replace with:

```text
их ministries overlapped in London’s evangelical public sphere.
```

---

## GILL-CONTENT-218 — “Gill preferred speaking of Gospel rather than Methodists” lacks evidence  
**Статус:** UNSUPPORTED PSYCHOLOGICAL CLAIM  
**Severity:** P1/P2

This sounds like documentary characterization but no:

- sermon sample;
- diary;
- letter;
- publication analysis

is offered.

Remove or source.

---

# 70. Kettering bookshop: narrative inflation

## GILL-CONTENT-219 — opening only on two market days needs source  
**Статус:** NEEDS LOCAL/PRIMARY SOURCE  
**Severity:** P1

Rippon supports the famous bookseller proverb.

It does not automatically support:

```text
shop opened only twice a week.
```

Need Kettering market/book-trade history or exact biography page.

---

## GILL-CONTENT-220 — “bargained for Buxtorf grammar” is an invented scene unless sourced  
**Статус:** NARRATIVE RECONSTRUCTION  
**Severity:** P1

Current wording:

```text
торговался за грамматику Буксторфа;
выпрашивал разрешение посмотреть редкие тома.
```

This is cinematic but presented as fact.

Either source it or label as reconstruction; preferably remove.

---

## GILL-CONTENT-221 — father’s “own fulling mill” conflicts with other descriptions  
**Статус:** INTERNAL BIOGRAPHICAL CONTRADICTION  
**Severity:** P1

Elsewhere Edward Gill is described as:

- wool merchant;
- hosiery/wool trade figure.

Context gives:

```text
собственная сукновальня / станок.
```

Need one canonical occupation record.

---

## GILL-CONTENT-222 — Hebrew proficiency at fifteen conflicts with checked sources  
**Статус:** P0/P1 CHRONOLOGY CONFLICT

Context:

```text
к пятнадцати годам читал на Hebrew, Greek and Latin.
```

Elsewhere:

- at ~14 begins Hebrew;
- at 19 reads Hebrew Bible;
- Haykin: by 19 well on the way to proficiency;
- Rippon describes unaided study but not the current age-15 milestone.

Do not publish age fifteen without primary locator.

---

## GILL-CONTENT-223 — “ordinary for Oxford graduate” is rhetorical, not measurable  
**Статус:** EDITORIAL PANEGYRIC  
**Severity:** P2

Language competence among Oxford graduates varied by faculty, period and proficiency.

Replace with direct comparison only if sourced.

---

## GILL-CONTENT-224 — own library and research programme by age 21 unsupported  
**Статус:** NEEDS SOURCE  
**Severity:** P1

The article states:

```text
у него уже была собственная библиотека и собственная программа исследования.
```

“Program of research” is modern interpretive language.

Need evidence for library size/content at this date.

---

## GILL-CONTENT-225 — absence of university curriculum as intellectual advantage is romanticized causation  
**Статус:** EDITORIAL INFERENCE  
**Severity:** P2

Claim:

```text
не имел университетского курса → не имел его шор.
```

This is an essayistic judgment, not historical finding.

Could remain as explicitly authorial reflection, not as causal fact.

---

## GILL-CONTENT-226 — “one of London’s largest private libraries” needs catalogue comparison  
**Статус:** NEEDS QUANTITATIVE SOURCE  
**Severity:** P1

Requires:

- Gill library catalogue/inventory;
- volume count;
- comparison sample of private libraries.

Without it:

```text
a substantial scholarly library
```

is safer.

---

## GILL-CONTENT-227 — “hundreds of direct citations where contemporaries cited second-hand” needs corpus study  
**Статус:** NEEDS METHODOLOGICAL SUPPORT  
**Severity:** P1

This is a comparative research conclusion requiring:

- citation count;
- sample of contemporaries;
- source-language verification;
- distinction direct/mediated.

Do not state without study.

---

# 71. Source apparatus of the context article

## GILL-CONTENT-228 — bibliography claims greater coverage than it provides  
**Статус:** CONFIRMED  
**Severity:** P1

Intro says:

```text
popular retellings are not the basis of the argument.
```

But source list does not directly cover:

- General Baptist decline/New Connexion;
- Baptist coffeehouses;
- Particular Baptist Fund foundation;
- Bristol Academy lineage;
- Southwark occupations;
- congregation three-times-average;
- Kettering market/bookshop details;
- Gill’s library size;
- Gill’s attitude to coffeehouse authority.

This is a major claim-to-source mismatch.

---

## GILL-CONTENT-229 — legal sources do not support all educational conclusions  
**Статус:** SOURCE SCOPE ERROR  
**Severity:** P1

Acts in source list support specific civil/religious restrictions.

They do not by themselves establish:

- Oxford matriculation rules;
- Cambridge degree tests;
- professorship exclusions;
- actual biography of Gill’s educational choices.

Add dedicated university-history sources.

---

## GILL-CONTENT-230 — Kennington source cannot support all Southwark claims  
**Статус:** SOURCE SCOPE ERROR  
**Severity:** P1

British History Online Stockwell/Kennington supports:

- local history;
- Whitefield;
- crowd estimates.

It does not automatically support:

- Goat Yard size;
- tanning atmosphere at chapel;
- Gill/Whitefield relationship;
- weekly awareness;
- Gill’s public silence about Methodists.

---

## GILL-CONTENT-231 — automated source availability check produced mixed results  
**Статус:** LINK QA NOTE  
**Severity:** P2

During audit:

- PRDL opened successfully and confirmed 113 titles / 148 volumes;
- SBJT PDF opened in parsed-text mode;
- legislation.gov.uk required JS/bot verification in the web reader;
- British History Online returned 403/502 in automated fetches;
- QMUL direct URLs required search-origin navigation and could not be opened directly by the tool.

This does **not** prove links are dead for normal browsers.

It does mean automated link checking should distinguish:

```text
HTTP dead
bot-blocked
JS-required
temporarily unavailable
verified
```

---

## GILL-CONTENT-232 — PRDL count is correctly stated but not an authored bibliography  
**Статус:** SOURCE NUANCE  
**Severity:** P2

PRDL confirms:

```text
113 titles, 148 vols.
```

But it is a collaborative catalogue/aggregator.

Use it for discovery, then cite original scans/editions for claims.

---

# 72. Series timeline is not chronologically truthful

## GILL-CONTENT-233 — “Context 1697–1719” contradicts the actual article  
**Статус:** CONFIRMED  
**Severity:** P1

Context article covers:

```text
1559–1720s and later retrospective repeal dates.
```

Timeline labels it:

```text
1697–1719.
```

This makes the timeline appear to date the content rather than Gill’s life stage.

---

## GILL-CONTENT-234 — Part II “1729–1748” excludes most of its own contents  
**Статус:** CONFIRMED  
**Severity:** P1

Part II includes:

- publications to 1770;
- Kennicott 1767;
- Doctrinal/Practical Divinity 1760s–1770;
- final theological system;
- later reception.

The 1729–1748 label is materially misleading.

---

## GILL-CONTENT-235 — Part III “1748–1771” also excludes its afterlife subject  
**Статус:** CONFIRMED  
**Severity:** P1

Part III covers:

- death;
- nineteenth-century Spurgeon;
- twentieth/twenty-first-century scholarship;
- Brown legacy;
- 2025 dissertation.

Therefore it is not merely 1748–1771.

### Better timeline categories

```text
Контекст — XVI–начало XVIII века
Человек — 1697–1729
Учёный — труды 1720-е–1770
Наследие — 1771–сегодня
Справочник — вся серия
```

---

# 73. Updated P0/P1 queue after V8

## P0 factual/source corrections

1. Separate Spurgeon 1859 and 1861 events.
2. Replace “not my Rabbi” with sermon 369 unless exact locator found.
3. Correct General Baptists “almost disappeared.”
4. Separate Act 1662 from Five Mile Act 1665.
5. Correct Carter Lane → Spurgeon pastor count.
6. Remove age-15 Hebrew claim pending source.
7. Remove legal claim that dissenters could not have synods.
8. Correct Macritchie inversion and Practical Divinity count from prior passes.

## P1 research integrity

1. Rebuild historical context bibliography by section.
2. Add General Baptist/New Connexion source.
3. Add university religious-tests source.
4. Add Particular Baptist Fund primary/history source.
5. Verify Baptist coffeehouse addresses.
6. Add Southwark social-history source.
7. Remove/relabel bookshop reconstructions.
8. Add image provenance labels.
9. Rebuild chronological series map.
10. Build claim registry shared across context/Part I/II/III/spravochnik.

---

# 74. Context-page source map required

```ts
contextClaims = {
  baptistOrigins: {
    sources: [SmythPrimary, HelwysPrimary, modernBaptistHistory],
    status: "contested-details"
  },
  greatEjection: {
    sources: [Act1662, FiveMile1665, Calamy],
    status: "verified"
  },
  universityTests: {
    sources: [OxfordHistory, CambridgeHistory, UniversitiesTests1871],
    status: "verified-by-period"
  },
  generalBaptists: {
    sources: [GeneralAssemblyHistory, NewConnexionHistory],
    status: "needs-balanced-rewrite"
  },
  coffeehouses: {
    sources: [minutes, fundRecords, BaptistQuarterly],
    status: "not-yet-verified"
  },
  southwark: {
    sources: [localHistory, churchRecords],
    status: "partially-verified"
  },
  bookshop: {
    sources: [Rippon, KetteringLocalHistory],
    status: "narrative-inflation"
  }
}
```

---

# 75. Итог восьмого прохода

Восьмой проход закрыл одну важную проблему и открыл другую.

## Закрыто

Позицию Сперджена можно доказать без неподтверждённого афоризма:

```text
Gill’s Body of Divinity — admirable and excellent in its way;
but Spurgeon would bind himself not to Gill’s system
or any human treatise, but to Christ.
```

Это точнее, сильнее и источниково честнее, чем “he is not my Rabbi”.

## Открыто системно

Статья исторического контекста выглядит осторожнее основных частей, но в действительности содержит много **narrative inflation**:

```text
правдоподобная общая история
→ живописная конкретная сцена
→ точная психологическая мотивация
→ отсутствие соответствующего источника
```

Особенно это видно в разделах:

- coffeehouses;
- Southwark;
- Kettering bookshop;
- Gill’s education;
- denominational fate.

Следующий этап должен превратить context bibliography из общего списка в **section-by-section evidence map**.

---

# 76. Девятый проход: Part I, Солтерс-Холл, евангелизация, цитаты и provenance

**Фокус:**

- блоки Part I, которые не были полностью разобраны в предыдущих проходах;
- `Intro`, `Pastor`, `Evangelism`, `Ordination 1720`, `Personal Credo`, локальный Southwark context;
- Salters’ Hall 1719;
- quiz Part I;
- реальное соответствие bibliography использованным источникам;
- происхождение и статус иллюстраций.

**Основное различение этого прохода:**

```text
документированный факт
≠
правдоподобная реконструкция
≠
поздний апологетический пересказ
≠
авторская духовная интерпретация
```

---

# 77. Part I Intro: биография превращается в предзаданную героическую схему

## GILL-CONTENT-236 — заголовок “гении без университетов” заранее навязывает итог  
**Статус:** EDITORIAL / HAGIOGRAPHIC FRAMING  
**Severity:** P2

Заголовок:

```text
Откуда рождаются гении без университетов
```

до предъявления источников уже определяет Gill как “гения” и строит биографию вокруг triumph narrative.

Для исследовательской статьи лучше:

```text
Самообразование вне университетской системы
```

или сохранить яркий заголовок, но не превращать последующие догадки в доказательства “гениальности”.

---

## GILL-CONTENT-237 — описание матери и “избрания как воздуха” не имеет источника  
**Статус:** UNSUPPORTED FAMILY PSYCHOLOGY  
**Severity:** P1/P2

Text:

```text
Мать, Elizabeth Walker, воспитывала детей в духе строгого
пуританского кальвинизма, где избрание было воздухом.
```

Это конкретное утверждение:

- о роли матери;
- о методе воспитания;
- о семейной эмоциональной атмосфере.

Нужен family memoir, church record или early biography.

Без него:

```text
семья принадлежала к кальвинистской баптистской среде
```

— допустимо; подробная психология матери — нет.

---

## GILL-CONTENT-238 — состав смешанной кеттерингской общины и её разделение нуждаются в локальном источнике  
**Статус:** NEEDS CHURCH HISTORY  
**Severity:** P1

Current claim:

```text
община состояла из Presbyterians, Independents and Baptists;
Edward Gill и William Wallis основали отдельную Particular Baptist church.
```

Нужны:

- название и даты исходной общины;
- церковная книга;
- дата отделения;
- роль Edward Gill;
- статус William Wallis.

Rippon может быть отправной точкой, но нужен page locator.

---

## GILL-CONTENT-239 — богословская атмосфера Кеттеринга выводится из Hussey и Richard Davis без доказанной цепочки  
**Статус:** NEEDS INFLUENCE EVIDENCE  
**Severity:** P1

Text утверждает:

```text
Kettering atmosphere was saturated with Hussey and Davis;
Gill received his lifelong theology not from books but grew in it.
```

Для intellectual influence нужны:

- присутствие их трудов в общине;
- использование гимнов Davis;
- цитаты Gill;
- correspondence;
- testimony of pastor/biographer.

Географическая и конфессиональная близость сама по себе не доказывает formative dominance.

---

## GILL-CONTENT-240 — “оба были людьми великого благочестия и учёности” требует точного объекта и места  
**Статус:** NEEDS EXACT PRIMARY LOCATOR  
**Severity:** P1

Сайт сообщает, что Gill одной фразой защищал Hussey и Tobias Crisp.

Нужно установить:

- work;
- edition/page;
- относится ли `both` именно к ним;
- говорил ли Gill о богословской правоте или только о личных качествах.

Положительная оценка благочестия не доказывает согласия со всей системой.

---

## GILL-CONTENT-241 — “наблюдение биографа” фактически является неназванной авторской цитатой  
**Статус:** PSEUDO-ATTRIBUTION  
**Severity:** P0/P1

Manuscript quote:

```text
Секрет гениальности Гилла...
```

Source:

```text
Наблюдение биографа над методом самообразования
```

Не указаны:

- имя;
- книга;
- страница;
- язык оригинала.

По форме это прямая цитата, по содержанию — редакционная авторская формула сайта.

### Исправление

Либо:

```text
Редакционное наблюдение
```

без кавычек и source-style блока, либо реальный биографический источник.

---

## GILL-CONTENT-242 — “первоисточники вместо пересказов профессоров” — ложная дихотомия  
**Статус:** EDITORIAL ROMANTICIZATION  
**Severity:** P2

Университетское обучение XVIII века также включало чтение классических и богословских текстов.

Нет доказательства, что Gill:

- принципиально избегал вторичной литературы;
- противопоставлял себя профессорам;
- выстроил именно такой conscious method.

Допустимо говорить о самостоятельном чтении оригинальных языков, но не о превосходстве отсутствия образования как установленном факте.

---

# 78. Pastor: anachronisms, succession and documentary appearance

## GILL-CONTENT-243 — Higham Ferrers назван “практикой” и “пробным годом”  
**Статус:** ANACHRONISTIC VOCABULARY  
**Severity:** P2

`Internship`, “практика”, “пробный год” создают современную institutional model.

Если источник говорит, что Gill:

```text
assisted John Davis / preached with the church
```

так и следует писать.

---

## GILL-CONTENT-244 — “значительное число обращённых уже тогда” опирается на Baptist Encyclopedia 1881  
**Статус:** LATE SECONDARY CLAIM  
**Severity:** P1

Для measurable conversion claim нужен:

- early memoir;
- church membership records;
- exact wording Cathcart;
- caveat, что речь о поздней биографической традиции.

Иначе поздняя энциклопедическая похвала становится статистическим фактом.

---

## GILL-CONTENT-245 — “получил наставление не от людей, а от Писания” неверно описывает ординационную проповедь  
**Статус:** RHETORICAL FALSE CONTRAST  
**Severity:** P2

Acts 20:28 был текстом charge/exhortation, произнесённой конкретным служителем.

Правильнее:

```text
наставление было построено на Деян. 20:28
```

а не:

```text
не от людей, а от Писания.
```

---

## GILL-CONTENT-246 — Elias Keach подтверждён как основатель первой Baptist church Pennsylvania, но “прародительница всех” чрезмерно  
**Статус:** PARTLY VERIFIED / OVERSTATED  
**Severity:** P1

Pennepack/Lower Dublin congregation:

- founded 1688 by Elias Keach;
- commonly described as first Baptist church in Pennsylvania;
- congregation still exists.

Но:

```text
прародительница всех баптистских церквей Philadelphia
```

неверно без строгого genealogical definition.

First Baptist Church of Philadelphia была организована отдельно в 1698 году, хотя региональные связи и association history важны.

---

## GILL-CONTENT-247 — текущее служение Peter Masters подтверждается, но “56 лет” нельзя хранить в body  
**Статус:** EXISTING GILL-CONTENT-056 UPDATED  
**Severity:** P1 maintenance

На июль 2026 года current sources продолжают называть Peter Masters пастором с 1970 года.

Но duration:

```text
56 years
```

становится stale ежегодно.

Хранить:

```text
since 1970
```

или вычислять автоматически из structured data.

---

## GILL-CONTENT-248 — chapel/pulpit images выглядят как документальные изображения  
**Статус:** PROVENANCE GAP  
**Severity:** P1

Captions:

```text
Часовня Horsleydown...
Кафедра Gill...
```

не сообщают:

- это historical engraving;
- реконструкция;
- AI image;
- modern visualization;
- actual surviving object.

Если likeness/layout не основаны на источнике, captions должны говорить:

```text
Художественная реконструкция
```

---

## GILL-CONTENT-249 — союз Gill–Whitefield и различие по призыву изложены без первичных текстов  
**Статус:** NEEDS TWO-SIDED SOURCE  
**Severity:** P1

Claim включает:

- church support for Whitefield;
- theological alliance;
- disagreement over free call.

Нужны отдельно:

- Gill/Whitefield correspondence or testimony;
- church record;
- texts defining each position.

Общая кальвинистская идентичность не доказывает личный alliance.

---

## GILL-CONTENT-250 — “у самых стен прихода Gill” географически и экклесиологически неточно  
**Статус:** EDITORIAL EXAGGERATION  
**Severity:** P2

Baptist congregation did not have an Anglican territorial parish in the same sense.

Kennington Common was nearby in South London, but not literally “at the walls” of the chapel.

---

# 79. Evangelism section: single-source apologetic narrative

## GILL-CONTENT-251 — главный рассказ идёт через George Ella → The Baptist Particular → сайт  
**Статус:** LONG SECONDARY SOURCE CHAIN  
**Severity:** P1

Displayed source:

```text
George Ella, p. 184
через The Baptist Particular
```

Это означает, что сайт, вероятно, не проверял cited edition/page directly.

Для центрального контраргумента против image of “cabinet theologian” нужен:

- книга Ella;
- scan/page;
- источники Ella;
- church minutes or early biography.

---

## GILL-CONTENT-252 — blockquote может быть пересказом, а оформлен как прямая цитата  
**Статус:** QUOTE-MODE UNCLEAR  
**Severity:** P0/P1

Русский текст звучит как связный современный summary:

```text
район разделён на четыре части;
по два брата;
труд распространился;
служители всех деноминаций поддержали.
```

Нужно хранить:

```text
quoteMode: exact | translated | paraphrase | synthesis
```

Если это paraphrase Ella, убрать quotation styling.

---

## GILL-CONTENT-253 — “восстановил церковь на библейском основании” является конфессиональной оценкой  
**Статус:** EDITORIAL / POLEMICAL  
**Severity:** P2

Что именно было “небиблейским” до Gill:

- polity;
- preaching;
- discipline;
- doctrine;
- membership?

Без определения фраза неисторична и рисует predecessors как doctrinal failure.

---

## GILL-CONTENT-254 — four districts / two brothers требует church-record verification  
**Статус:** NEEDS PRIMARY RECORD  
**Severity:** P1

Это очень конкретная operational claim.

Нужны:

- date;
- Horselydown minutes;
- names or offices;
- target population;
- duration;
- whether work was pastoral visitation of members or general evangelism.

---

## GILL-CONTENT-255 — “еженедельно достигал более тысячи” не является числом уникальных людей  
**Статус:** QUANTITATIVE MISLEADINGNESS  
**Severity:** P1

Если Ella складывает:

```text
church attendance
+ lectures
+ other meetings
```

это aggregate weekly audiences, potentially with repeated listeners.

`Reached with the Gospel` звучит как:

- unique persons;
- evangelistic contacts;
- conversions.

Нужно указать methodology или убрать число.

---

## GILL-CONTENT-256 — invitation from Whitefield needs exact source  
**Статус:** NEEDS PRIMARY/ACADEMIC LOCATOR  
**Severity:** P1

Current article states:

```text
Whitefield invited Gill to share the pulpit.
```

Нужны:

- letter;
- diary;
- Rippon;
- Whitefield journal;
- church minutes.

---

## GILL-CONTENT-257 — support by “evangelical ministers of all denominations” is too broad  
**Статус:** NEEDS NAMES AND SCOPE  
**Severity:** P1

Who supported:

- visitation scheme;
- open-air preaching;
- funding;
- theological cooperation?

“All denominations” is a superlative-style claim.

---

## GILL-CONTENT-258 — transatlantic pamphlet story and rarity explanation need bibliographic evidence  
**Статус:** NEEDS EDITION/PROVENANCE RECORD  
**Severity:** P1

Claims:

1. New England Baptists requested copies;
2. Baptist Fund sent remaining print run;
3. therefore pamphlets are rare in British libraries.

The third is a causal bibliographical conclusion requiring:

- print run;
- shipment quantity;
- surviving-copy census;
- library catalog comparison.

---

## GILL-CONTENT-259 — `gigantic WALL` переведено как буквальная “стена-исполин”  
**Статус:** HIGH-CONFIDENCE TRANSLATION ERROR  
**Severity:** P0/P1

Original capitalizes:

```text
WALL
```

alongside:

```text
STENNETT
GALE
GILL
```

This strongly indicates a surname/polemical opponent, likely William Wall, with a secondary pun on a wall.

Current translation:

```text
церковного дракона — стену исполина
```

erases the historical person and the wordplay.

### Better draft

```text
поверг церковного дракона — исполина Уолла
```

with footnote explaining the pun.

---

## GILL-CONTENT-260 — `Cleanly compell’d` does not mean “чистым словом”  
**Статус:** TRANSLATION ERROR  
**Severity:** P1

Original sense:

```text
neatly / cleanly / decisively forced him into swift retreat
```

Current:

```text
чистым словом обратил её в бегство
```

adds “word” and changes pronoun/object.

---

## GILL-CONTENT-261 — poem contains a chain of name-puns not explained  
**Статус:** TRANSLATION/COMMENTARY GAP  
**Severity:** P1

Likely wordplay:

```text
Gale → mighty blast
Wall → made fall
Gill → Gale alive in Gill
```

The commentary explains only Gale/Gill and misses Wall/fall.

---

## GILL-CONTENT-262 — “ability to take a city he besieges” does not come from the poem  
**Статус:** SOURCE CONTAMINATION  
**Severity:** P1

Final explanation imports siege imagery associated elsewhere with Toplady’s praise of Gill.

The anonymous poem is about polemical predecessors and wordplay, not conquering a city.

---

# 80. Ordination section: “full protocol” and later accretions

## GILL-CONTENT-263 — title “полный протокол” exceeds the evidence shown  
**Статус:** EDITORIAL OVERCLAIM  
**Severity:** P1

The section provides a reconstructed sequence, not:

- full minutes;
- complete transcript;
- all participants;
- every prayer/hymn;
- documentary facsimile.

Use:

```text
реконструкция порядка рукоположения по Crosby/Rippon
```

---

## GILL-CONTENT-264 — church founding date varies across the series  
**Статус:** INTERNAL CHRONOLOGY CONFLICT  
**Severity:** P1

Current files use:

```text
1650
1652
ок. 1653
```

These may represent:

- first gathering;
- first pastor;
- organizational transition;
- later denominational identity.

Need an event model, not one floating “foundation date”.

---

## GILL-CONTENT-265 — Noble’s introduction of Gill to Particular Baptist Fund in 1718 needs exact record  
**Статус:** NEEDS FUND MINUTES / BIOGRAPHY PAGE  
**Severity:** P1

The section states this as fact but bibliography lacks Fund records.

---

## GILL-CONTENT-266 — sequence of laying on hands and Gill’s role with deacons requires documentary wording  
**Статус:** NEEDS PRIMARY TEXT  
**Severity:** P1

Potential questions:

- Were Gill and deacons ordained in one service?
- Did already-ordained ministers lay hands on all?
- Did Gill participate after his own ordination?
- Were these the congregation’s “first” deacons or newly appointed deacons?

Current concise sentence may overinterpret the sequence.

---

## GILL-CONTENT-267 — grant for Skepp library and “foundation of nine-volume commentary” are two separate claims  
**Статус:** SOURCE + CAUSATION ISSUE  
**Severity:** P1

Even if the Fund financed a purchase:

```text
library significantly aided Gill’s rabbinic studies
```

does not automatically equal:

```text
these books formed the foundation of the nine-volume commentary.
```

The commentary drew on a much wider lifetime library and decades of acquisition.

---

## GILL-CONTENT-268 — “first attempt to create an educational society in 1752” is unnamed  
**Статус:** NEEDS INSTITUTIONAL IDENTIFICATION  
**Severity:** P1

Need:

- society/fund name;
- founders;
- document;
- relation to Bristol, Baptist Fund or later academy structures;
- whether it was truly “first”.

---

## GILL-CONTENT-269 — quote about Baptists’ ignorance of learning lacks speaker and context  
**Статус:** NEEDS EXACT QUOTE LOCATOR  
**Severity:** P1

Was Gill:

- directly quoted in minutes;
- paraphrased by a later historian;
- speaking of ministers, churches or trustees?

The Russian formulation currently sounds verbatim.

---

## GILL-CONTENT-270 — John Martin’s move to hear Gill is broadly supported; later “chief defender against Fuller” needs source  
**Статус:** PARTLY VERIFIED  
**Severity:** P2

Biographical tradition supports:

```text
in 1760 Martin moved to London to sit under Gill.
```

But:

```text
one of the chief defenders of Gill’s tradition against Fuller
```

requires works, controversy dates and comparative assessment.

---

## GILL-CONTENT-271 — conversions under Gill do not settle the hyper-Calvinism classification  
**Статус:** INVALID APOLOGETIC INFERENCE  
**Severity:** P1

Statement:

```text
Brine was converted through Gill,
which people forget when labeling both hyper-Calvinists.
```

Historical conversions may challenge a caricature of total pastoral sterility.

They do not determine:

- duty-faith;
- offer terminology;
- theological definition of hyper-Calvinism.

---

# 81. Personal Credo: attractive quotations without primary apparatus

## GILL-CONTENT-272 — Colton Strother is a tertiary collector, not final source  
**Статус:** SOURCE HIERARCHY ISSUE  
**Severity:** P1

The section begins:

```text
Strother collected three sayings.
```

Each saying should then be traced to Gill/Rippon/Spurgeon rather than cited through a modern overview.

---

## GILL-CONTENT-273 — “prayer is the breath of a regenerate man” needs book/chapter/page  
**Статус:** NEEDS PRIMARY LOCATOR  
**Severity:** P1

`Practical Divinity` is a multi-book work.

Add:

```text
book, chapter, edition, page
```

and translator.

---

## GILL-CONTENT-274 — poverty/conscience saying exists in competing forms inside the series  
**Статус:** INTERNAL QUOTE VARIANCE  
**Severity:** P0/P1

Part I:

```text
I value nothing in comparison with gospel truths.
I am not afraid to be poor.
```

Part II:

```text
I can afford to be poor,
but cannot afford to injure my conscience.
```

These may be:

- two different sentences;
- paraphrase and exact quote;
- merged anecdote;
- translation variants.

Need one canonical English text and provenance.

---

## GILL-CONTENT-275 — “I am a Baptist…” needs exact polemical work  
**Статус:** NEEDS PRIMARY LOCATOR  
**Severity:** P1

The labels:

```text
new Baptist
old Calvinistic
Antinomian
```

belong to a specific controversy.

Without work and opponent, the quote loses its meaning and can be misread as indifference to doctrinal precision.

---

## GILL-CONTENT-276 — “three personal statements” mixes different genres  
**Статус:** EDITORIAL CATEGORY ERROR  
**Severity:** P2

The set combines:

- doctrinal aphorism;
- biographical anecdote;
- polemical self-identification.

It is not a coherent personal creed.

---

## GILL-CONTENT-277 — translations have no translator or quote mode  
**Статус:** CONFIRMED  
**Severity:** P1

All three need:

```text
original English
translation by project / published translator
exact or adapted
```

---

# 82. Part I Southwark context: factual background and speculative bridges

## GILL-CONTENT-278 — Kettering fires are precise but uncited and weakly connected  
**Статус:** NEEDS LOCAL HISTORY SOURCE  
**Severity:** P2

Dates:

```text
1744 and 1766
```

need a municipal/local-history source.

Their relevance to Gill must be shown:

- family affected?
- church records destroyed?
- property loss?
- visit/response?

Otherwise they are decorative chronology.

---

## GILL-CONTENT-279 — “Gill and Carey came from the same soil” is literary, not genealogical  
**Статус:** EDITORIAL  
**Severity:** P2

Baptist Missionary Society was founded in Kettering in 1792.

But shared town/region does not establish:

- direct institutional continuity;
- theological continuity;
- causal influence.

---

## GILL-CONTENT-280 — bridges are mentioned as context for Carter Lane move without evidence  
**Статус:** URBAN CAUSATION SPECULATION  
**Severity:** P2

Footnote says the link is cautious, but the paragraph still suggests urban bridge development helps explain the move.

Need:

- church minutes;
- property/capacity reason;
- transport/access source.

Otherwise list bridge openings separately as background.

---

## GILL-CONTENT-281 — 1720–1757 is not uniformly the “peak” of Gin Craze  
**Статус:** PERIODIZATION OVERSTATEMENT  
**Severity:** P1

The crisis is usually associated especially with the 1720s–1740s, with the 1751 Act marking a major regulatory turning point.

Better:

```text
much of Gill’s early and middle pastorate overlapped the Gin Craze.
```

---

## GILL-CONTENT-282 — Gin Acts chronology should cite legislation, not only two popular histories  
**Статус:** SOURCE-TYPE GAP  
**Severity:** P1

The monographs are useful social history.

Exact Acts and years should be tied to:

- statute titles;
- parliamentary records;
- legislation database.

---

## GILL-CONTENT-283 — “Kennington Common in direct line of sight” is a geospatial claim without proof  
**Статус:** NEEDS HISTORICAL MAP / VIEW-SHED  
**Severity:** P1

Direct visibility depends on:

- exact Goat Yard/Carter Lane position;
- eighteenth-century buildings;
- elevation;
- church window/roof point.

Proximity is enough; line-of-sight should be removed unless mapped.

---

## GILL-CONTENT-284 — exact number of at least 141 executions needs source and date range  
**Статус:** NEEDS QUANTITATIVE SOURCE  
**Severity:** P1

Specify:

- executions at Kennington Common;
- beginning/end dates;
- data source;
- whether military/political/common-law executions all included.

---

## GILL-CONTENT-285 — Whitefield 29 April 1739 quotation needs journal edition/page  
**Статус:** NEEDS PRIMARY LOCATOR  
**Severity:** P1

The crowd estimate is already a self/early estimate, not measured attendance.

Add diary edition and avoid silently converting estimate into census.

---

## GILL-CONTENT-286 — Marischal degree was not simply “unavailable” because English universities were closed  
**Статус:** CAUSAL OVERSTATEMENT  
**Severity:** P1

A Scottish honorary DD and admission to an English degree course are different institutional events.

Correct:

```text
Scottish universities could recognize a Dissenter whom Oxford/Cambridge’s
subscription system excluded from ordinary English university pathways.
```

Do not imply Gill applied for the same honorary degree in England and was legally refused.

---

## GILL-CONTENT-287 — Bunhill Fields “pantheon” paragraph mixes burial history and university exclusion  
**Статус:** RHETORICAL CONFLATION  
**Severity:** P2

Burial among Bunyan, Watts and later Blake is a retrospective memory frame.

It does not itself signify opposition to university privilege.

Separate:

```text
nonconformist burial culture
```

from:

```text
educational disabilities.
```

---

## GILL-CONTENT-288 — `Dissenting Praise` appears mismatched as an education source  
**Статус:** BIBLIOGRAPHIC SCOPE RISK  
**Severity:** P1

The tooltip names:

```text
Isabel Rivers, David L. Wykes, eds., Dissenting Praise
```

as support for dissenting academies/education.

Title/scope must be checked; it appears connected to hymnody/worship rather than a general institutional history of university tests.

Use the actual Dissenting Academies Project, McLachlan, Parker or university histories.

---

## GILL-CONTENT-289 — Southwark context exists in two independently maintained versions  
**Статус:** DUPLICATE CLAIM OWNERSHIP  
**Severity:** P1

Context article and Part I repeat:

- Gin Craze;
- bridges;
- legal disability;
- Kennington;
- Southwark occupations.

They already differ in tone and specifics.

Create one shared data/source module and let each article render a different-length view.

---

# 83. Salters’ Hall: what the vote actually established

## GILL-CONTENT-290 — 53/57 vote is broadly supported, but the procedural object is simplified  
**Статус:** CORE FACT VERIFIED / DESCRIPTION NEEDS REWRITE  
**Severity:** P1

The famous 57–53 vote concerned adding a doctrinal declaration/preamble, drawn from confessional or catechetical language, to the advice sent in the Exeter controversy.

Current question:

```text
must every dissenting minister sign a declaration before he is accused or defended?
```

is broader than the actual motion.

---

## GILL-CONTENT-291 — the Exeter ministers should be named  
**Статус:** CONTEXT GAP  
**Severity:** P1

“Two young Presbyterian pastors” obscures:

- James Peirce;
- Joseph Hallet;
- nature and chronology of Exeter dispute;
- trustees’ actions.

“Young” also needs age/source.

---

## GILL-CONTENT-292 — denominational 14/2 and 1/14 counts lack a cited source  
**Статус:** NEEDS EXACT ROLL/VOTE SOURCE  
**Severity:** P1

The context bibliography contains no dedicated Salters’ Hall primary record or scholarly study.

A precise table requires:

- participant roll;
- denominational classification;
- vote list;
- treatment of uncertain affiliations.

---

## GILL-CONTENT-293 — “Bible carried it by four” should be attributed to Sir Joseph Jekyll tradition  
**Статус:** SOURCE ATTRIBUTION CORRECTION  
**Severity:** P1

Accessible historical summaries attribute the remark to Sir Joseph Jekyll, who witnessed the scene.

The current caveat that it is not a stenographic exit quote is useful.

But it should not be left as an anonymous “later story”.

---

## GILL-CONTENT-294 — non-subscription did not itself constitute Arianism  
**Статус:** POSITIVE NUANCE, RETAIN  
**Severity:** P2

The current article correctly notes that orthodox ministers could oppose mandatory human subscription.

This caveat must remain when the section is rewritten.

---

## GILL-CONTENT-295 — subsequent Unitarian drift is not proof that every non-subscriber’s principle caused it  
**Статус:** CAUSALITY WARNING  
**Severity:** P1

Need distinguish:

- theological heterodoxy;
- anti-subscription conscience;
- institutional enforcement;
- academy networks;
- property/trust structures;
- later generational change.

---

## GILL-CONTENT-296 — “Particular Baptists preserved orthodoxy: 14 to 2” overgeneralizes a delegate sample  
**Статус:** INVALID GENERALIZATION  
**Severity:** P1

Even if the breakdown is correct, it describes ministers present/voting.

It does not by itself prove:

```text
all Particular Baptists remained orthodox
```

through the century.

---

## GILL-CONTENT-297 — Gill’s 1731 Trinity book was not simply a direct response to Salters’ Hall  
**Статус:** CONFIRMED CAUSAL OVERREACH  
**Severity:** P0/P1

Elsewhere the series identifies the immediate occasion as a Baptist physician, Mr Davis, whose tract had Sabellian tendencies.

Salters’ Hall is important background.

Correct formulation:

```text
The 1719 controversy formed part of the confessional climate;
the immediate occasion for Gill’s 1731 work was the Davis controversy.
```

---

## GILL-CONTENT-298 — “without Salters’ Hall it is impossible to understand Gill” is rhetorical totalization  
**Статус:** EDITORIAL  
**Severity:** P2

Gill’s trinitarianism also arose from:

- Scripture;
- Particular Baptist confession;
- patristic reading;
- Davis controversy;
- wider anti-Trinitarian debate.

---

## GILL-CONTENT-299 — context bibliography lacks a dedicated Salters’ Hall source  
**Статус:** SOURCE COVERAGE GAP  
**Severity:** P1

Add at least:

- contemporary advices/pamphlets;
- participant/vote study;
- modern academic history of English Dissent and the Exeter controversy.

SBJT’s broad Gill issue is not sufficient for every number in the table.

---

# 84. Part I quiz: folklore and unsupported connections become scored facts

## GILL-CONTENT-300 — Q1 should explicitly test “Rippon’s reported anecdote,” not the historical event  
**Статус:** QUIZ EPISTEMIC FRAMING  
**Severity:** P1

The question partly does this well by mentioning Chambers and Rippon.

The explanation should retain:

```text
according to the reported recollection
```

throughout, not transition to “the stranger said” as established event.

---

## GILL-CONTENT-301 — Q1 translation needs original wording and translator  
**Статус:** NEEDS EXACT QUOTE  
**Severity:** P1

Phrase:

```text
Учёным станет, и всему миру не остановить его
```

is striking enough to require:

- English original;
- Rippon page;
- whether Chambers quoted exact speech decades later;
- project translation.

---

## GILL-CONTENT-302 — Q3 introduces Isaac Watts although the body section does not establish that target  
**Статус:** QUIZ ADDS UNSOURCED FACT  
**Severity:** P1

Quiz explanation:

```text
в том числе связано с Isaac Watts
```

Body only says “those who taught pre-existence”.

Need a source linking Article V specifically to Watts or remove his name from the scored explanation.

---

## GILL-CONTENT-303 — Q2 and Q4 continue propagating already identified source problems  
**Статус:** CROSS-REFERENCE  
**Severity:** P0/P1

- Q2 repeats unsupported psychological reason for seven-year delay: see `GILL-CONTENT-035`, `048`.
- Q4 hardcodes daughter as twelve and repeats chronology issue: see `GILL-CONTENT-038`, `039`.

Quiz repair must follow body repair, not precede it.

---

# 85. Part I bibliography contradicts its own source policy

## GILL-CONTENT-304 — several sources actually used in body are absent  
**Статус:** CONFIRMED  
**Severity:** P1

Body explicitly relies on:

- George Ella;
- The Baptist Particular;
- Colton Strother;
- Baptist Encyclopedia 1881;
- Reformed Reader;
- unnamed local/urban histories;
- Whitefield diary;
- Kettering fire history.

They are not fully listed in `Sources Part I`.

---

## GILL-CONTENT-305 — “encyclopedic pages were not the basis” conflicts with repeated Cathcart dependence  
**Статус:** CONFIRMED SOURCE-POLICY CONTRADICTION  
**Severity:** P1

Baptist Encyclopedia is used for:

- father’s character;
- Higham Ferrers conversions;
- education/superlatives;
- physical description elsewhere.

If retained, classify it honestly as a late denominational reference work and corroborate high-risk claims.

---

## GILL-CONTENT-306 — vague bibliography entries are not checkable records  
**Статус:** CONFIRMED  
**Severity:** P1

Examples:

```text
История Southwark и мостов...
Dr Williams’s Centre materials...
Corporation Act and Test Acts...
```

Need:

- author/institution;
- title;
- year;
- URL/identifier;
- pages/sections;
- claim coverage.

---

## GILL-CONTENT-307 — legislation entries do not cover university and honorary-degree conclusions  
**Статус:** SOURCE SCOPE ERROR  
**Severity:** P1

Civil office statutes cannot alone prove:

- Oxford admission rules;
- Cambridge degree tests;
- Aberdeen honorary-degree process;
- Gill’s personal educational counterfactual.

---

## GILL-CONTENT-308 — sources are article-level, not claim-level  
**Статус:** SYSTEMIC  
**Severity:** P1

A reader cannot tell which source supports:

- a date;
- a quotation;
- an interpretation;
- a reconstruction.

Need footnotes/claim registry.

---

# 86. Image provenance across Gill series

## GILL-CONTENT-309 — inspected Gill captions contain no reconstruction disclosure  
**Статус:** CONFIRMED MARKUP FACT  
**Severity:** P1

No `Художественная реконструкция` label was found in inspected Gill component captions.

This does not prove every image is synthetic.

It proves the rendered article does not tell readers which visual category they are seeing.

---

## GILL-CONTENT-310 — captions use documentary grammar  
**Статус:** PROVENANCE RISK  
**Severity:** P1

Examples:

```text
Часовня Horsleydown...
Кафедра Gill...
Whitefield проповедует...
Юный Gill в книжной лавке...
подпольное собрание puritans...
```

Readers naturally infer historical depiction.

---

## GILL-CONTENT-311 — alt text also asserts specificity  
**Статус:** ACCESSIBILITY + HISTORICAL INTEGRITY  
**Severity:** P1

Screen-reader users receive the same documentary certainty even if the image is artistic.

Alt should describe the image and disclose:

```text
illustration / reconstruction
```

where applicable.

---

## GILL-CONTENT-312 — visual source registry is required  
**Статус:** SYSTEMIC  
**Severity:** P1

Suggested fields:

```ts
{
  file,
  type: "historical-original" | "licensed-reproduction" |
        "modern-photo" | "artistic-reconstruction" | "ai-assisted",
  subject,
  historicalBasis,
  creator,
  date,
  sourceUrl,
  license,
  captionDisclosure
}
```

---

# 87. Navigation and source discoverability

## GILL-CONTENT-313 — Part I TOC omits its source section  
**Статус:** CONFIRMED  
**Severity:** P2

`partToc` ends with quiz and has no:

```text
#sec-sources-part1
```

For a 32-minute research article, sources should be directly reachable.

---

## GILL-CONTENT-314 — source section exists but quiz `sourceRef` links only back to prose  
**Статус:** EVIDENCE GRAPH GAP  
**Severity:** P2

Ideal quiz flow:

```text
question
→ relevant prose
→ exact source note
```

Current flow stops at prose.

---

# 88. Updated source/evidence architecture after V9

## For every blockquote

```ts
{
  originalText,
  translatedText,
  author,
  work,
  edition,
  pageOrSection,
  quoteMode,
  translator,
  confidence
}
```

## For every historical reconstruction

```ts
{
  claim,
  evidence,
  inferenceLevel:
    "direct" | "probable" | "possible" | "literary",
  wordingAllowed
}
```

## For every image

```ts
{
  imageType,
  documentaryStatus,
  historicalBasis,
  requiredCaptionPrefix
}
```

---

# 89. P0/P1 queue after V9

## P0/P1 immediate

1. Correct `WALL` translation and poem commentary.
2. Remove “clean word” mistranslation.
3. Relabel pseudo-quote “observation of biographer.”
4. Rewrite Salters’ Hall → Gill causation.
5. Add Mr Davis as immediate Trinity controversy.
6. Remove unsupported delay psychology from quiz.
7. Remove daughter age certainty from quiz.
8. Resolve competing poverty/conscience quotations.
9. Reclassify evangelism blockquote as quote/paraphrase.
10. Add exact source for four-district visitation.
11. Remove line-of-sight Kennington claim.
12. Correct 1650/1652/1653 foundation model.
13. Add image reconstruction disclosures.
14. Rebuild Part I bibliography around actual sources used.

## P1 next

1. Verify Personal Credo quotations.
2. Verify Whitefield invitation.
3. Verify Fund grant for Skepp library.
4. Identify 1752 education initiative.
5. Add Salters’ Hall participant/vote source.
6. Add local Kettering/Southwark histories.
7. Add sources row to TOC.
8. Create shared Southwark context module.

---

# 90. Итог девятого прохода

Part I has a different problem from Part II–III.

Part II–III often overstate a scholarly conclusion.

Part I often overstates a **story**:

```text
late biography / denominational tradition
→ vivid reconstructed scene
→ direct quotation styling
→ scored quiz fact
```

The strongest examples are:

- mother’s spiritual atmosphere;
- bookshop scenes;
- evangelism districts;
- complete ordination protocol;
- Personal Credo quotations;
- Salters’ Hall as direct cause;
- documentary-looking illustrations.

The next pass should prioritize **primary quotation recovery** and **visual/source provenance**, not additional narrative expansion.

---

# 91. Десятый проход: reconciliation с репозиторием `FedorMilovanov/Research`

**Новый обязательный источник аудита:** публичный репозиторий `FedorMilovanov/Research`, папка:

```text
Джон Гилл/
```

На 9 июля 2026 года отдел содержит навигационный файл и **42 тематических досье**:

```text
00_README_AND_NAVIGATION.md
01 … 42
31_GILL_DEPT_MASTER_MAP.md
```

Этот проход не повторяет содержание V1–V9. Его задача:

1. Сопоставить уже найденные ошибки сайта с исследованиями 00–42.
2. Повысить статус тех ошибок, которые подтверждены первичными выемками Research.
3. Снять или уточнить прежние выводы, если Research предоставляет лучший первичный материал.
4. Зафиксировать ошибки и внутренние противоречия самого Research.
5. Построить единый маршрут:

```text
Research claim
→ primary quotation
→ current Astro component
→ glossary / quiz / metadata
```

---

# 92. Что Research представляет собой фактически

## GILL-CONTENT-315 — Research уже является полноценным отдельным отделом, а не набором заметок  
**Статус:** CONFIRMED  
**Severity:** architectural

`00_README_AND_NAVIGATION.md` фиксирует:

- canonical home исследований по Гиллу;
- 42 досье;
- тематические кластеры;
- первичные источники;
- будущую статью «Богословие Гилла»;
- связь с сайтом.

Следовательно, дальнейший аудит сайта без сверки с Research действительно был бы неполным.

---

## GILL-CONTENT-316 — Research нарушает собственное правило против фрагментации  
**Статус:** CONFIRMED REPOSITORY-GOVERNANCE CONFLICT  
**Severity:** P1 process

Root `AGENT_RULES.md` говорит:

```text
ЗАПРЕЩЕНО плодить мелкие файлы.
Один кейс = один большой файл-досье.
```

Отдел Гилла состоит из 42 перекрывающихся файлов:

- несколько досье об eternal justification;
- несколько об offer/duty-faith;
- несколько о Body of Divinity;
- несколько о singing/worship;
- несколько о biography;
- несколько о legacy.

`31_GILL_DEPT_MASTER_MAP.md` сам признаёт дублирование.

### Следствие

Research нуждается не в новых `43`, `44`, `45`, а в:

```text
CLAIM_REGISTRY
SOURCE_REGISTRY
CANONICAL_FACTS
SUPERSEDED_CLAIMS
```

---

## GILL-CONTENT-317 — Research проверял старый MDX-слой, а текущая серия уже Astro  
**Статус:** CONFIRMED STALENESS  
**Severity:** P0/P1 integration

`00_README` определяет Level B site content как:

```text
src/content/articles/dzhon-gill-*.mdx
```

Многие досье описывают grep по этим MDX.

Но текущий production content находится в:

```text
src/components/article-pilots/gill-*
*.astro
```

Именно эти Astro-компоненты анализировались в V1–V9.

### Следствие

Утверждения Research:

```text
на сайте уже есть
на сайте отсутствует
сайт содержит только...
```

могут относиться к устаревшему слою и требуют повторной проверки по current `main`.

---

## GILL-CONTENT-318 — уровни источников определены в Research по-разному  
**Статус:** CONFIRMED SYSTEMIC CONFLICT  
**Severity:** P1

Root `AGENT_RULES.md`:

```text
Level A — originals / official records / court decisions
Level B — reputable media / verified biographies
Level C — blogs / social media / rumors
```

Gill `00_README`:

```text
Level A — primary public-domain sources
Level B — site content checked by author
Level C — secondary academic literature
```

Individual Gill dossiers:

```text
Level B — academic secondary sources
Level C — blogs / denominational summaries
```

### Problem

The same label can mean:

- current site text;
- peer-reviewed research;
- respectable media;
- denominational biography.

No automated or human reviewer can infer evidentiary weight consistently.

---

## GILL-CONTENT-319 — “Level A” is often assigned to text accessed through a secondary host  
**Статус:** CONFIRMED PROVENANCE COLLAPSE  
**Severity:** P1

Examples:

- Gill text through `bibleportal`;
- Declaration through `pristinegrace`;
- biography through `reformedreader`;
- primary quotation copied by a blog.

The underlying work may be public domain, but:

```text
primary work
≠
primary scan
≠
secondary transcription
≠
modern excerpt
```

### Required fields

```text
sourceWorkClass
accessHost
edition
scanOrTranscription
verifiedAgainstScan
```

---

## GILL-CONTENT-320 — corrected errors remain in summaries of the same file  
**Статус:** CONFIRMED  
**Severity:** P0/P1

Example `07_VVEDENIE_DEEP.md`:

At the top:

```text
Greek by 11
Hebrew by 12
```

Later, after primary verification:

```text
Hebrew learned without living assistance via Buxtorf;
earlier chronology corrected.
```

The obsolete claim was not removed from the summary or article skeleton.

This makes “latest paragraph wins” impossible for downstream agents.

---

## GILL-CONTENT-321 — the master map is a historical snapshot, not a current canonical index  
**Статус:** CONFIRMED  
**Severity:** P2

`31_GILL_DEPT_MASTER_MAP.md` still says the department grew to 30 dossiers, while appended sections extend it through 42.

This is understandable historically, but downstream automation may treat the opening summary as current.

---

## GILL-CONTENT-322 — “all key doctrines verified” exceeds what the files actually prove  
**Статус:** CONFIRMED EPISTEMIC OVERCLAIM  
**Severity:** P1

Research has verified many quotations.

It has not thereby verified:

- the correct interpretation of those quotations;
- their relation to confessions;
- historical classification;
- causal influence;
- representative use across Gill’s whole corpus.

Primary-text verification answers:

```text
Did Gill write this?
```

It does not automatically answer:

```text
What doctrinal category follows?
Was it orthodox?
Did it cause a movement?
```

---

# 93. Biography reconciliation: Research confirms some V9 findings and repeats others

## GILL-CONTENT-323 — Research confirms the conversion/baptism chronology established in V4  
**Status:** CONFIRMED BY RESEARCH PRIMARY DOSSIER  
**Severity:** source upgrade

`17_BIOGRAPHICAL...` confirms from Rippon:

```text
~12 — Genesis 3:9
1 Nov 1716 — profession + baptism
4 Nov — membership / Lord’s Supper / Isaiah 53
next Sunday — first sermon, 1 Corinthians 2:2
```

This independently confirms:

- `GILL-CONTENT-036`;
- `GILL-CONTENT-037`;
- the error in Part I quiz Q2.

---

## GILL-CONTENT-324 — Research’s own Spravochnik dossier retains the discarded John 6:37 chronology  
**Статус:** CONFIRMED INTERNAL RESEARCH ERROR  
**Severity:** P0

`09_SPRAVOCHNIK_DEEP_RESEARCH.md` says:

```text
1 Nov 1716 — spiritual conversion under William Wallis
on John 6:37
```

`07` and `17` explicitly state:

```text
John 6:37 is absent from Rippon;
Genesis 3:9 occurred around age twelve;
1 Nov was profession/baptism.
```

### Action

Mark the `09` timeline entry `SUPERSEDED` and update the website only from `17`.

---

## GILL-CONTENT-325 — Research repeats the daughter-age error rather than resolving it  
**Статус:** CONFIRMED  
**Severity:** P0/P1

`17` summarizes Elizabeth as:

```text
died 30 May 1738, 13 years old
```

Rippon’s phrase is:

```text
in the thirteenth year
```

That normally means age twelve, not thirteen.

Research therefore copied the same interpretive error present in site narrative/quiz.

### Correct data model

```text
sourceAgePhrase: "in the thirteenth year"
normalizedAge: 12
confidence: high
```

Birth date remains to be independently confirmed.

---

## GILL-CONTENT-326 — Research confirms the seven-year delay was not simply “heart examination”  
**Статус:** CONFIRMED  
**Severity:** source upgrade

`17` gives Rippon’s stated reasons:

- youth;
- solemnity of profession;
- church expectation of ministerial calling.

This confirms earlier audit findings `035` and `048`.

---

## GILL-CONTENT-327 — school withdrawal is incorrectly elevated to the sole cause of no university education  
**Статус:** CONFIRMED RESEARCH OVERREACH  
**Severity:** P1

`17` says:

```text
This is the cause of absence of university education.
```

The source establishes why Gill left grammar school.

It does not by itself prove the whole later counterfactual:

```text
without this event he would have attended Oxford/Cambridge.
```

Other relevant factors:

- dissenting subscription barriers;
- finances;
- patronage;
- absence of academy placement;
- family trade;
- later personal choices.

---

## GILL-CONTENT-328 — Research contains competing D.D. quotations  
**Статус:** CONFIRMED QUOTE VARIANCE  
**Severity:** P1

Research uses:

```text
I neither sought it, nor thought it, nor bought it.
```

The primary Rippon passage previously verified in V4 has a different order:

```text
I neither thought it, nor bought it, nor sought it.
```

The aphorism is often modernized/reordered.

### Requirement

Use the exact wording of the consulted edition and label modernization.

---

## GILL-CONTENT-329 — “University of Aberdeen” and “Marischal College” need one institutional record  
**Статус:** NEEDS NORMALIZATION  
**Severity:** P1

Research uses:

```text
University of Aberdeen
```

Site uses:

```text
Marischal College, Aberdeen
```

Historically Marischal College was a separate institution before the 1860 union forming the modern University of Aberdeen.

Use period-correct wording:

```text
Marischal College, Aberdeen
```

with archival confirmation of date.

---

## GILL-CONTENT-330 — Research correctly identifies “ten thousand” as sheets, then continues asserting ten million words  
**Статус:** CONFIRMED INTERNAL CONTRADICTION  
**Severity:** P1

`17` correctly says:

```text
ten thousand = sheets of letterpress;
ten million words = modern extrapolation.
```

`07` later says:

```text
Rippon testifies that Gill wrote more than ten million words.
```

Rippon does not testify to that word count.

### Correct wording

```text
Rippon recorded more than ten thousand printed sheets;
modern authors sometimes extrapolate this to roughly ten million words.
```

The calculation needs a defined sheet format and average word density.

---

## GILL-CONTENT-331 — Research adds an “ivory tower” routine without page-level proof  
**Статус:** NEEDS EXACT RIP PON LOCATOR  
**Severity:** P1

`07` claims:

- study called an ivory tower;
- daily Talmud reading;
- three sermons weekly;
- no secretaries;
- strict pre-dawn routine.

Some elements may be biographical traditions, but the current paragraph provides no page-level quotations.

Do not render as a single documentary routine until decomposed.

---

## GILL-CONTENT-332 — Declaration articles and Sabellian revision are overstated  
**Статус:** NEEDS TEXTUAL PRECISION  
**Severity:** P1

`17` says articles IV–V were inserted later because of Sabellian heresy.

Its quoted source says:

```text
those especially in Article IV
```

were introduced due to the Sabellian problem.

The site separately associates Article V with pre-existence of Christ’s human soul and Isaac Watts.

These may be separate controversies.

Do not merge:

```text
Sabellian revision
human-soul pre-existence
Watts
```

without document chronology.

---

# 94. Practical Divinity: Research contains the source of the site’s book-count conflict

## GILL-CONTENT-333 — Research has both “four books” and “five books” as canonical facts  
**Статус:** CONFIRMED INTERNAL CONFLICT  
**Severity:** P0

Files `05` and `09`:

```text
Practical Divinity — four books.
```

File `29`:

```text
Practical Divinity — five books;
Book V = Dissertation Concerning Jewish Proselyte Baptism.
```

### Resolution

The body proper has four books.

The dissertation may appear as an appended fifth navigation unit or be bound in the same volume.

Therefore store:

```text
coreBooks: 4
boundAppendices: 1
```

not a single overloaded `bookCount`.

---

## GILL-CONTENT-334 — Research’s own CCEL-derived outlines disagree on chapter placement  
**Статус:** CONFIRMED  
**Severity:** P0/P1

`05` maps:

```text
Book I — internal worship
Book II — external/public worship
Book III/IV — ordinances/government in expanded editions
```

`29` maps:

```text
Book III — ordinances
Book IV — private/civil duties
```

`34` maps prayer and preaching to:

```text
Book III chs. 3/5/6
```

There is no edition identifier explaining these mappings.

### Consequence

All locators of form:

```text
Practical Divinity Book X, chapter Y
```

are unsafe until a canonical edition/TOC is fixed.

---

## GILL-CONTENT-335 — “expanded editions” is used to explain away structure conflict without evidence  
**Статус:** CONFIRMED  
**Severity:** P1

`05` says ordinances and government are split into Books III–IV “in expanded editions.”

No editions are named.

Need an edition table:

```text
1770 original
1810/1839/etc. reprint
CCEL navigation
modern Accordance structure
```

---

## GILL-CONTENT-336 — calling the proselyte dissertation “Book V” cannot validate the site’s eschatology citation  
**Статус:** CONFIRMED  
**Severity:** P0

Even if a digital TOC labels the appendix “Book V,” it contains a dissertation on proselyte baptism.

It cannot contain:

```text
chapter 14 on the spiritual reign of Christ.
```

Thus the site locator remains invalid.

Eschatology belongs to *Doctrinal Divinity*, Book VII.

---

## GILL-CONTENT-337 — Research’s 514-page figure is edition-specific  
**Статус:** NEEDS EDITION ID  
**Severity:** P2

Page totals must include:

- edition;
- format;
- whether dissertation included;
- pagination type.

---

# 95. Offer, proclamation and duty-faith: primary text found, interpretation still disputed

## GILL-CONTENT-338 — Research provides strong primary anchors for `proclamation ≠ offer`  
**Статус:** CONFIRMED POSITIVE FINDING  
**Severity:** source upgrade

Dossiers `12`, `19`, `21` correctly locate:

- *Cause*, Part I, Section XL, 2 Cor. 5:19;
- *Sermons and Tracts*, sermon 95.

Gill explicitly distinguishes:

```text
proclamation/declaration of accomplished peace
from
conditional offer.
```

This should replace vague secondary paraphrases in the site.

---

## GILL-CONTENT-339 — Research correctly discovered a misattribution of the “heralds” quotation  
**Статус:** CONFIRMED  
**Severity:** P1

The “heralds/kerukas” passage is not from the cited chapter of *Cause of God and Truth*.

It belongs to:

```text
Sermon 95, “An Answer to the Birmingham Dialogue-Writer.”
```

Any website attribution to *Cause*, Part III, must be corrected.

---

## GILL-CONTENT-340 — Research converts “external duty” into “external gospel call to all” without sufficient proof  
**Статус:** INTERPRETIVE OVERREACH  
**Severity:** P1

The primary text distinguishes:

- command;
- national/external reformation;
- historical assent;
- saving/evangelical faith;
- internal call.

A command that reprobates can perform externally does not establish:

```text
a sincere saving invitation to every hearer.
```

---

## GILL-CONTENT-341 — Research interprets the John 1:7 passage in the opposite direction from Macritchie  
**Статус:** MAJOR INTERPRETIVE CONFLICT  
**Severity:** P0/P1

Research quotes Gill:

```text
men may be bound to believe,
yet not to the saving of their souls,
or that Christ died for them.
```

Then concludes:

```text
This is against the hyper-Calvinism accusation.
```

Macritchie’s 2025 thesis argues that this very distinction:

- concedes only non-saving/historical belief;
- denies universal duty to saving/evangelical faith;
- places Gill within the hyper-Calvinist camp under accepted definitions.

### Correct presentation

```text
Primary text verified.
Interpretation contested:
Nettles/defenders vs Rathel/Macritchie.
```

Do not encode one interpretation as `Level A`.

---

## GILL-CONTENT-342 — Declaration articles VII–VIII do not prove duty-faith  
**Статус:** INVALID INFERENCE IN RESEARCH  
**Severity:** P1

`10_ORDINANCES...` argues:

```text
imputed righteousness + irresistible grace
refute the claim that Gill denied duty-faith.
```

Those doctrines establish:

- the ground of justification;
- the divine cause of regeneration and faith.

They do not answer:

```text
Is every unregenerate hearer commanded to exercise saving faith?
```

---

## GILL-CONTENT-343 — “critics quote-mined Gill” is an editorial verdict  
**Статус:** NEEDS EVIDENCE  
**Severity:** P1

Research repeatedly says critics extracted offer quotations unfairly.

But Rathel and Macritchie analyze:

- eternal justification;
- active/passive distinction;
- natural vs evangelical repentance;
- offer language;
- duty-faith.

Disagreement is interpretive, not automatically quote-mining.

---

## GILL-CONTENT-344 — Research’s own files describe Gill’s position inconsistently  
**Статус:** CONFIRMED  
**Severity:** P0/P1

`07` says:

```text
Gill affirmed a sincere free offer
but denied duty-faith.
```

`12/19/21` quote Gill denying offer-language.

`27` says he affirmed duty-faith, though only non-saving belief.

`35` identifies Gillites by rejection of duty-faith and promiscuous offer.

No single coherent position is stored.

---

## GILL-CONTENT-345 — a six-term soteriological glossary is now mandatory  
**Статус:** SYSTEMIC  
**Severity:** P1

Research and site must distinguish:

```text
historical belief
natural duty
external reform
evangelical repentance
saving faith
well-meant gospel offer
```

Without this, every side appears to contradict itself.

---

# 96. Eternal justification: primary quotation is good; apologetic framing is not

## GILL-CONTENT-346 — Research correctly verifies active/passive justification  
**Статус:** CONFIRMED POSITIVE FINDING  
**Severity:** source upgrade

Dossiers `08` and `23` provide primary text:

```text
active — internal and eternal act in divine mind;
passive — act terminating on believer’s conscience.
```

This should replace the site’s simple arrow.

---

## GILL-CONTENT-347 — “justification from eternity” versus “eternal justification” is not an established neutral distinction  
**Статус:** PARTISAN TERMINOLOGY  
**Severity:** P1

Research derives this contrast through baptists.net / Ella apologetics.

In ordinary scholarly usage, Gill is routinely discussed under:

```text
eternal justification / justification from eternity.
```

The proposed distinction should be attributed to that defensive tradition, not presented as universal terminology.

---

## GILL-CONTENT-348 — Research conflates declaration in conscience with juridical application through faith  
**Статус:** THEOLOGICAL PRECISION ISSUE  
**Severity:** P1

Gill’s passive justification is described as terminating on the conscience.

Research repeatedly says:

```text
justification is applied/received through faith in time.
```

This wording may make Gill sound closer to standard confessional instrumental justification than his text warrants.

Use:

```text
faith brings knowledge, comfort and conscious enjoyment of justification
```

unless Gill explicitly uses “application” in the juridical sense.

---

## GILL-CONTENT-349 — historical precedents do not settle the orthodoxy of Gill’s exact formulation  
**Статус:** INVALID HISTORIOGRAPHIC INFERENCE  
**Severity:** P1

Research lists:

- Ames;
- Goodwin;
- Twisse;
- Maccovius;
- Witsius.

From this it concludes Gill was not an extremist but an orthodox heir.

A shared vocabulary does not prove identical doctrine.

Need comparative context and confessional reception.

---

## GILL-CONTENT-350 — Research largely omits the 1689 Confession 11.4 tension  
**Статус:** CONFIRMED OMISSION  
**Severity:** P1

The official SBJT material quoted in V7 distinguishes:

```text
eternal decree to justify
from
personal justification in time.
```

That is essential for assessing Gill as a Particular Baptist.

---

## GILL-CONTENT-351 — “active/passive distinction saves Gill from the label” is not a source finding  
**Статус:** EDITORIAL VERDICT  
**Severity:** P1

The primary quotation establishes the distinction.

Whether that distinction removes or confirms hyper-Calvinist classification is the disputed question.

---

# 97. Church and state: Research contains a direct theological contradiction

## GILL-CONTENT-352 — dossier 10 says “complete separation”; dossier 38 says establishmentarian  
**Статус:** CONFIRMED INTERNAL CONTRADICTION  
**Severity:** P0/P1

`10_ORDINANCES...` concludes:

```text
complete separation of church from state,
with civic loyalty.
```

`38_POLITICAL_THEOLOGY` demonstrates from Gill:

- magistrates should suppress impiety;
- encourage religion;
- guard both tables;
- punish blasphemy, idolatry and profanation.

These are not the modern doctrine of complete separation.

### Canonical formulation

```text
Gill rejected Anglican ecclesiastical establishment and civil control
of the gathered church, yet assigned Christian magistrates
a positive coercive duty toward public religion.
```

---

## GILL-CONTENT-353 — `Dissenters’ Reasons` does not prove modern separationism  
**Статус:** CONFIRMED  
**Severity:** P1

Separation from the Church of England means:

- rejecting its polity, worship and membership basis.

It does not necessarily mean:

- religiously neutral government;
- no civil enforcement of first-table duties.

---

## GILL-CONTENT-354 — political theology must be integrated into the site’s legal-context narrative  
**Статус:** CONTENT GAP  
**Severity:** P1

The context article presents Gill mainly as a victim of state religious tests.

That is true but incomplete.

Gill also held stronger views of Christian magistracy than many later Baptists.

This tension is historically valuable and should not be hidden.

---

# 98. Whitefield and the Awakening: Research confirms the source weakness

## GILL-CONTENT-355 — dossier 30 is not primary verification  
**Статус:** CONFIRMED  
**Severity:** P1

Its central claims rely on:

- George Ella;
- baptists.net;
- pristinegrace;
- CCEL/Theopedia summaries;
- Credo/Helm;
- Banner of Truth.

No Whitefield diary/letter or Gill church minute is quoted for:

- shared platform;
- direct invitation;
- congregational support.

---

## GILL-CONTENT-356 — label “white facts” is inappropriate  
**Статус:** EPISTEMIC LABEL ERROR  
**Severity:** P1

The file calls claims “белые факты” while its own source list identifies them as Level C/secondary.

Use:

```text
reported by Ella
secondary tradition
needs primary verification
```

---

## GILL-CONTENT-357 — active ministry does not determine the duty-faith classification  
**Статус:** INVALID APOLOGETIC INFERENCE  
**Severity:** P1

Gill could:

- preach frequently;
- pastor effectively;
- see conversions;
- cooperate with revivalists;

and still deny the universal duty to saving faith under a particular theological definition.

Biography and doctrinal classification answer different questions.

---

## GILL-CONTENT-358 — Research’s Great Awakening dossier is the likely source of site overstatement  
**Статус:** CONFIRMED PROVENANCE  
**Severity:** P1

Site claims mirror dossier 30:

- church strongly supported Whitefield;
- Whitefield invited Gill;
- they preached together;
- Gill was a pioneer of the Awakening.

Therefore the site should not cite these as independent confirmations.

They derive from the same Ella-based chain.

---

# 99. Brown University and American influence

## GILL-CONTENT-359 — Research confirms Brown claims remain secondary  
**Статус:** CONFIRMED  
**Severity:** P1

Dossier 36 explicitly admits:

```text
Morgan Edwards / Brown connections are documented secondarily;
primary letters and records were not checked.
```

This confirms V7/V8 findings.

---

## GILL-CONTENT-360 — Research does not verify 52 folios or current holdings  
**Статус:** CONFIRMED ABSENCE  
**Severity:** P0/P1

No Research file supplies:

- accession catalogue;
- Manning letter;
- probate record;
- Brown special-collections record;
- current shelfmarks.

The site’s expanded package remains unsupported.

---

## GILL-CONTENT-361 — recommendation, donation and financial support are bundled from one modern overview  
**Статус:** SOURCE-CONCENTRATION RISK  
**Severity:** P1

These are three distinct claims and require distinct evidence.

---

## GILL-CONTENT-362 — period name should be Rhode Island College  
**Статус:** HISTORICAL WORDING  
**Severity:** P2

Use:

```text
College in the English Colony of Rhode Island and Providence Plantations
(later Brown University)
```

or a shorter period-accurate equivalent.

---

## GILL-CONTENT-363 — Edwards citations are one of the best verified new contributions in Research  
**Статус:** CONFIRMED POSITIVE FINDING  
**Severity:** P2

Dossier 36 carefully distinguishes:

```text
citation / acquaintance
from
systemic influence.
```

This methodological pattern should be copied elsewhere.

---

# 100. Spurgeon reconciliation

## GILL-CONTENT-364 — Research misdates the Body of Divinity quotation to 1859  
**Статус:** CONFIRMED  
**Severity:** P0/P1

`07` attributes:

```text
His Body of Divinity ... has no rival
```

to the foundation-stone event in 1859.

V8 identified the verified source:

```text
sermon no. 369,
first sermon in completed Metropolitan Tabernacle,
25 March 1861.
```

Research must be corrected before its text is reused.

---

## GILL-CONTENT-365 — Research’s Spurgeon corpus remains mostly secondary  
**Статус:** CONFIRMED  
**Severity:** P1

Claims still needing exact primary locators include:

- “Coryphaeus of hyper-Calvinism”;
- three-star markings;
- “The very best”;
- “not my Rabbi”;
- 1855 revival quotation.

---

## GILL-CONTENT-366 — sermon 369 should become the canonical Spurgeon evidence  
**Статус:** RECOMMENDATION  
**Severity:** P1

It directly proves:

- high regard for Gill;
- praise of *Body of Divinity*;
- refusal to bind himself to Gill’s system;
- Christ as final doctrinal authority.

---

# 101. Eschatology reconciliation

## GILL-CONTENT-367 — Research confirms eschatology belongs to Doctrinal Book VII  
**Статус:** CONFIRMED  
**Severity:** P0 source upgrade

Dossier 11 supplies the chapter map:

```text
Book VII, chapter 8 — Millennium / personal reign.
```

This definitively contradicts the site’s:

```text
Practical Divinity, Book 5, chapter 14.
```

---

## GILL-CONTENT-368 — “two-phase premillennialism” is a modern synthesis  
**Статус:** NEEDS ATTRIBUTION  
**Severity:** P1

The primary text distinguishes spiritual and personal reigns.

The classification:

```text
hybrid postmillennial + premillennial
```

comes from modern researchers and should be labeled as such.

---

## GILL-CONTENT-369 — Research does not substantiate the site’s 1866–1913 “prediction fulfilled” narrative  
**Статус:** CONFIRMED ABSENCE  
**Severity:** P1

Dossier 11 discusses no verified missionary prediction window.

The site’s claim remains unsupported and should not be treated as inherited Research evidence.

---

# 102. Research source-policy and link problems

## GILL-CONTENT-370 — site content cannot be an evidentiary Level B for itself  
**Статус:** CIRCULAR VERIFICATION  
**Severity:** P1

Gill README treats checked website copy as a source tier.

For auditing that same website, this is circular:

```text
site claim
verified by
site claim.
```

Site content should be `TARGET`, not a source level.

---

## GILL-CONTENT-371 — dead links are known but remain embedded across dossiers  
**Статус:** CONFIRMED  
**Severity:** P1

Dossier 17 identifies the dead Reformed Reader memoir link.

Other files continue naming Reformed Reader or derivative pages as primary access points.

A central link registry should replace links globally.

---

## GILL-CONTENT-372 — source status and claim status are conflated  
**Статус:** SYSTEMIC  
**Severity:** P1

A Level A source can still be:

- mistranscribed;
- quoted out of context;
- interpreted incorrectly;
- insufficient for a causal claim.

Research needs separate fields:

```text
sourceLevel
transcriptionStatus
claimSupport
interpretiveStatus
```

---

## GILL-CONTENT-373 — no canonical supersession mechanism exists  
**Статус:** CONFIRMED  
**Severity:** P0/P1

Corrections are written as paragraphs such as:

```text
earlier version was wrong
```

but the earlier version remains elsewhere.

Needed:

```yaml
claim_id: GILL-BIO-CONVERSION
canonical_value: ...
supersedes:
  - dossier09.timeline.1716
  - dossier07.G4
```

---

## GILL-CONTENT-374 — duplicate source chains create false corroboration  
**Статус:** SYSTEMIC  
**Severity:** P1

Example:

```text
Ella book
→ baptists.net
→ pristinegrace
→ Research dossier
→ website
```

Multiple URLs do not equal multiple independent witnesses.

---

# 103. Research-to-site reconciliation matrix

| Existing audit issue | Research evidence | Result |
|---|---|---|
| Isaiah 53 placed on baptism day | dossier 17 gives 4 Nov | Confirm site bug |
| First sermon in December | dossier 17 gives next Sunday after 4 Nov | Confirm site bug |
| Delay explained as heart-testing | dossier 17 gives youth + church expectation | Confirm site/quiz bug |
| Daughter age | dossier 17 repeats “13,” primary wording still problematic | Research does not resolve |
| D.D. wording | Research has reordered popular form | Use primary edition |
| Practical Divinity count | 05/09 = 4; 29 = 5 | Research internally conflicted |
| Eschatology locator | dossier 11 = Doctrinal VII.8 | Site locator definitely wrong |
| Offer/proclamation | dossiers 12/19/21 primary | Strongly confirmed |
| Duty-faith verdict | dossier 27 vs Macritchie | Interpretation contested |
| Eternal justification | dossiers 08/23 primary active/passive | Text confirmed; verdict contested |
| Whitefield cooperation | dossier 30 secondary/Ella | Not independently verified |
| Brown donation | dossier 36 admits secondary only | Remains unverified |
| Spurgeon independence | Research secondary; sermon 369 primary | Replace with sermon 369 |
| Church/state | dossier 10 vs 38 direct conflict | Needs integrated rewrite |
| Image provenance | no Research visual registry | V9 issue remains |
| Latin epitaph | only authorship confirmed | diplomatic text remains unresolved |

---

# 104. Priority corrections inside Research itself

## P0

1. Mark `09` John 6:37 chronology superseded.
2. Correct daughter “13” normalization.
3. Resolve Practical Divinity `4 + appendix` versus `5`.
4. Correct Spurgeon 1859/1861 conflation.
5. Remove “free offer affirmed” from `07` unless sourced.
6. Reclassify John 1:7 duty-faith interpretation as contested.
7. Reconcile `10` separationism with `38` establishmentarianism.
8. Remove ten-million-word attribution to Rippon.

## P1

1. Standardize levels across root and Gill department.
2. Replace MDX target paths with current Astro components.
3. Create canonical claim registry.
4. Create edition registry for Gill’s works.
5. Create direct/secondary source-chain graph.
6. Add Macritchie 2025 to the academic debate.
7. Replace Ella-derived “white facts” with status badges.
8. Add Brown institutional verification queue.
9. Add exact Spurgeon sermon registry.
10. Mark obsolete summary text, not just add corrections below.

---

# 105. What Research newly contributes to the website audit

Research contains substantial material that should be reused after correction:

1. Full primary mapping of *Cause of God and Truth* sections.
2. Exact reattribution of the heralds quotation.
3. Primary active/passive justification quotation.
4. Exact Book VII eschatology structure.
5. Verified Jonathan Edwards references to Gill.
6. Precise ordination participants from Rippon/Crosby.
7. Primary structure of Gill’s covenant theology.
8. Direct political-theology quotations on magistrates.
9. Strong source for the four-book Practical Divinity model.
10. Dead-link detection and public-domain access map.

The problem is not lack of research.

The problem is lack of **canonical consolidation**.

---

# 106. Final conclusion of V10

After reconciling V9 with Research 00–42, the project’s content problem can be stated precisely:

```text
The website contains strong material.
Research contains even stronger primary extraction.
But neither has a canonical claim layer.
```

As a result:

```text
primary quotation
→ agent interpretation
→ defensive framing
→ duplicated dossier
→ stale site paragraph
→ quiz answer
```

may occur even after a later agent has already found the correction.

The next correct deliverable is not dossier 43.

It is:

```text
GILL_CANONICAL_CLAIMS.md
GILL_SOURCE_REGISTRY.yml
GILL_EDITION_REGISTRY.yml
GILL_QUOTE_REGISTRY.yml
GILL_RESEARCH_TO_SITE_CROSSWALK.md
```

These should replace the current “latest paragraph somewhere in 42 files” model.

---

# 107. Одиннадцатый проход: недочитанные досье Research, CCEL-локаторы и перенос ошибок в Part II

**Проверено дополнительно:**

```text
Research/Джон Гилл/
15, 16, 18, 20, 22, 24, 25, 26, 28,
32, 33, 37, 39, 40, 41, 42
```

а также текущий:

```text
gb-is-my-strength/main
src/components/article-pilots/gill-part2/GillPart2ArticleBody.astro
```

**Главный метод этого прохода:**

```text
ошибка Research
≠
ошибка production
```

Каждый пункт ниже помечает, относится ли проблема только к исследовательскому досье, к источниковому регистру или уже к текущему Astro-тексту.

---

# 108. Системная ошибка CCEL: URL-сегмент принят за номер книги

## GILL-CONTENT-375 — CCEL route segment не является надёжным номером печатной книги
**Статус:** CONFIRMED SYSTEMIC LOCATOR BUG  
**Severity:** P0

Research регулярно использует адреса вида:

```text
doctrinal.iv.iii
doctrinal.vi.i
doctrinal.vii.xiv
```

и автоматически читает:

```text
iv = Book IV
vi = Book VI
vii = Book VII
```

Но собственное оглавление Research показывает, что цифровая иерархия CCEL включает дополнительные уровни и не совпадает один к одному с печатной нумерацией Gill.

### Следствие

URL должен храниться отдельно от библиографического locator:

```yaml
web_route: doctrinal.vii.xiv
print_work: A Body of Doctrinal Divinity
print_book: VI
chapter: Of Sanctification
```

---

## GILL-CONTENT-376 — творение, невинность и провидение ошибочно названы Book IV
**Статус:** CONFIRMED RESEARCH ERROR  
**Severity:** P0

Досье `42_THE_CREATION_IMAGE_OF_GOD_AND_PROVIDENCE.md` называет:

```text
creation / innocence / providence = Book IV
```

Но мастер-TOC досье `05` помещает:

```text
creation
providence
state of innocence
fall
```

в **Book III, Of the External Works of God**.

Ошибка возникла из route `doctrinal.iv.iii`, а не из печатного оглавления.

---

## GILL-CONTENT-377 — христология ошибочно названа Book VI
**Статус:** CONFIRMED RESEARCH ERROR  
**Severity:** P0

Досье `40` пишет:

```text
Body of Doctrinal Divinity, Book VI:
communicatio idiomatum / burial / exaltation
```

Но мастер-TOC `05` относит incarnation, humiliation, obedience, death, burial, resurrection, ascension и offices к **Book V, Of the Grace of Christ**.

`doctrinal.vi.*` — route group, не доказательство Book VI.

---

## GILL-CONTENT-378 — пневматология применения названа одновременно Book III и Book VII
**Статус:** CONFIRMED INTERNAL CONTRADICTION  
**Severity:** P0

Досье `39` говорит:

```text
Ordo salutis Gill — Book III BDD
```

а затем трактует:

```text
doctrinal.vii.xiv = Book VII chapter 14
```

Собственный TOC Research помещает regeneration, calling, conversion, sanctification и perseverance в **Book VI, Of the Blessings of Grace**.

---

## GILL-CONTENT-379 — “Of Sanctification, ch. 14” можно считать подтверждённым только после edition mapping
**Статус:** NEEDS EDITION REGISTRY  
**Severity:** P1

Номер главы внутри книги может быть верен. Но locator должен выглядеть так:

```text
Gill, Doctrinal Divinity,
Book VI, chapter 14, “Of Sanctification”
```

с указанием конкретного издания.

---

## GILL-CONTENT-380 — primitivebaptist.net TOC нельзя использовать как Level A edition authority
**Статус:** SOURCE-CLASS ERROR  
**Severity:** P1

Это современная републикация/навигационный слой. Она помогает найти текст, но не заменяет title page, original table of contents, printed pagination и facsimile edition.

---

## GILL-CONTENT-381 — ошибка book mapping подрывает заявления “все ключевые доктрины верифицированы”
**Статус:** CONFIRMED  
**Severity:** P1

Содержание цитат может быть подлинным. Но библиографическая верификация не завершена, если читателю сообщается неправильная книга.

---

## GILL-CONTENT-382 — нужен canonical edition map для Doctrinal и Practical Divinity
**Статус:** SYSTEMIC REQUIREMENT  
**Severity:** P0/P1

```yaml
work:
edition:
volume:
internal_book:
chapter:
printed_page:
digital_host:
digital_route:
scan_verified:
```

---

# 109. Hermeneutics: primary material versus modern synthesis

## GILL-CONTENT-383 — правило веры по Рим. 12:6 не проверено в полном первичном контексте
**Статус:** RESEARCH-ONLY / PARTIAL  
**Severity:** P1

Досье `37` опирается главным образом на Rathel, TGC и Center for Baptist Renewal и признаёт, что полный verbatim-пассаж из Gill не извлечён.

Нельзя маркировать весь вывод `Gill used creeds as external interpretive standard` как полностью Level A.

---

## GILL-CONTENT-384 — “external standard = Creed” может преувеличить роль символов
**Статус:** THEOLOGICAL PRECISION ISSUE  
**Severity:** P1

Gill мог использовать Apostles’ Creed, Nicene language и inherited articles of faith как orthodox summary. Но Scripture остаётся supreme rule.

Правильнее:

```text
creedal regula fidei functioned as a subordinate doctrinal summary,
not as an authority independent of Scripture.
```

---

## GILL-CONTENT-385 — historicist interpretation is not simple “literal-historical exegesis”
**Статус:** CATEGORY ERROR  
**Severity:** P1

Reading seven historical churches as seven future church ages is symbolic, typological and historicist. It is not literal in the same sense as lexical interpretation of Isaiah or Genesis.

---

## GILL-CONTENT-386 — “Catholic in spirit” is a modern editorial characterization
**Статус:** EDITORIAL  
**Severity:** P2

It may describe Gill’s use of Fathers, Reformed paedobaptists and creeds, but should be attributed to a modern scholar or marked as site synthesis.

---

## GILL-CONTENT-387 — “Lightfoot of the Baptists” is a secondary nickname
**Статус:** NEEDS EXACT ATTRIBUTION  
**Severity:** P2

Research cites a biographical website. Need the first identifiable author and date before using it as historical reception.

---

## GILL-CONTENT-388 — rabbinic literature is repeatedly mislabeled “Second Temple literature”
**Статус:** CONFIRMED CATEGORY ERROR  
**Severity:** P1

Mishnah, Babylonian Talmud, Jerusalem Talmud, Zohar, Rashi, Ibn Ezra, Kimhi and many extant Targum forms are mostly late antique or medieval. They can preserve earlier traditions, but are not automatically Second Temple documents.

---

# 110. Current Part II: rabbinic sources and first-reader claims

## GILL-CONTENT-389 — Jerusalem Talmud is presented as direct apostolic-era context
**Статус:** CONFIRMED PRODUCTION CLAIM  
**Severity:** P1

Current table says:

```text
Jerusalem Talmud
→ historical context of the apostolic era.
```

Use:

```text
late-antique rabbinic traditions that may preserve earlier material
```

rather than direct witness language.

---

## GILL-CONTENT-390 — “hear the text as its first readers heard it” is anachronistic
**Статус:** CONFIRMED PRODUCTION CLAIM  
**Severity:** P1

Part II applies this sentence to Onkelos, Jerusalem Targum, Targum Jonathan and Mishnah/Talmud. These witnesses are textually and chronologically diverse.

---

## GILL-CONTENT-391 — Onkelos / Jerusalem Targum references on Genesis 1:2 need exact wording
**Статус:** NEEDS PRIMARY LOCATOR  
**Severity:** P1

Required:

```text
Gill work + verse
exact targum wording
targum identification
edition
translation
what inference Gill draws
```

This was already converted into a quiz answer, increasing priority.

---

## GILL-CONTENT-392 — “Targum Jonathan on Exodus” requires name normalization
**Статус:** NEEDS TEXTUAL IDENTIFICATION  
**Severity:** P1

`Targum Jonathan` properly designates the Prophets. A Pentateuchal text historically called “Jonathan” is usually Pseudo-Jonathan. The site must specify which Targum is meant.

---

## GILL-CONTENT-393 — Zohar “critical acquaintance” has no evidence
**Статус:** CONFIRMED PRODUCTION UNSOURCED CLAIM  
**Severity:** P1

The table tells readers how Gill used Zohar but gives no citation, example or distinction between quotation, agreement and polemic.

---

## GILL-CONTENT-394 — “only Christian Hebraist without university education…” is an unsupported absolute
**Статус:** CONFIRMED PRODUCTION SUPERLATIVE  
**Severity:** P0/P1

Current sentence requires a census of Christian Hebraists and an operational definition of `researcher`, `polemicist` and `university education`. Gill himself repeatedly used rabbinic materials apologetically and polemically.

---

## GILL-CONTENT-395 — “unprecedented for an eighteenth-century Christian” is likewise unbounded
**Статус:** CONFIRMED PRODUCTION SUPERLATIVE  
**Severity:** P1

Christian Hebraism already had Lightfoot, the Buxtorfs, Wagenseil, Surenhusius and other scholars. Gill may have been extraordinary among English Baptists. That is the defensible scope.

---

## GILL-CONTENT-396 — the rabbinic table is a modern reconstruction
**Статус:** CONFIRMED  
**Severity:** P1

The columns look like a documented research inventory, but no corpus search, frequency data or page locators are supplied. Label as editorial summary until verified.

---

# 111. Scripture/canon dossier: access copy is not critical edition

## GILL-CONTENT-397 — dossier 41 calls a modern transcription Level A while admitting no scan check
**Статус:** CONFIRMED INTERNAL CONTRADICTION  
**Severity:** P1

It uses `christianbeliefs.org` and later admits the direct CCEL chapter could not be located. Correct status:

```text
primary text through unverified modern transcription
```

---

## GILL-CONTENT-398 — “66 books” is a normalized count, not Gill’s quoted label
**Статус:** NEEDS PRECISION  
**Severity:** P2

Unless Gill explicitly says “sixty-six,” write:

```text
the Protestant canon conventionally counted as 66 books.
```

---

## GILL-CONTENT-399 — “always received by the Church” must be presented as Gill’s claim
**Статус:** HISTORIOGRAPHIC QUALIFICATION  
**Severity:** P1

Reception of several New Testament antilegomena was historically disputed. Do not convert Gill’s apologetic formulation into neutral modern canon history.

---

## GILL-CONTENT-400 — church testimony is corroborative, not the final ground of authority
**Статус:** THEOLOGICAL PRECISION  
**Severity:** P1

Better:

```text
divine inspiration and internal authority,
corroborated by Jewish and Christian reception.
```

---

## GILL-CONTENT-401 — bridge to Nicaea risks repeating a popular canon myth
**Статус:** CONTENT-RISK  
**Severity:** P0/P1

The Council of Nicaea did not establish the Protestant 66-book canon. Any cross-link must explicitly prevent that misunderstanding.

---

## GILL-CONTENT-402 — bracketed historical names inside a “verbatim quote” need audit
**Статус:** QUOTE-INTEGRITY  
**Severity:** P1

Need identify Gill’s original wording, editor’s expansion and translator/editor responsible.

---

## GILL-CONTENT-403 — the inspiration nuance is valuable and should be preserved
**Статус:** CONFIRMED POSITIVE FINDING  
**Severity:** P2

Gill distinguishes truthful inspired recording from truthfulness of every quoted speaker.

---

# 112. Hebrew dissertation: historical importance versus modern philology

## GILL-CONTENT-404 — Louis Cappel is wrongly labeled a rationalist critic
**Статус:** CONFIRMED HISTORICAL ERROR IN RESEARCH  
**Severity:** P1

Cappel was a French Protestant/Huguenot churchman, professor of Hebrew and theology, and major early textual critic.

---

## GILL-CONTENT-405 — Brian Walton likewise cannot be reduced to “rationalist”
**Статус:** HISTORICAL OVERFRAMING  
**Severity:** P1

Walton was an Anglican bishop and orientalist associated with the London Polyglot. Research turns an intra-Christian textual debate into “orthodoxy versus rationalist enemies.”

---

## GILL-CONTENT-406 — Gill’s antiquity-of-vowel-points thesis is not current scholarly consensus
**Статус:** CONFIRMED HISTORIOGRAPHIC REQUIREMENT  
**Severity:** P0/P1

Ancient Hebrew manuscripts, including the Dead Sea Scrolls, do not use the full Tiberian vowel-point system.

Gill’s dissertation is important for history of Protestant bibliology, eighteenth-century Hebraism and defense of textual certainty. It should not be presented as a currently established philological conclusion.

---

## GILL-CONTENT-407 — oral vocalization tradition does not prove ancient written vowel signs
**Статус:** INVALID INFERENCE  
**Severity:** P1

Talmudic evidence for traditional reading, pronunciation, accents or qere traditions does not establish that present graphic points were written in Mosaic or Ezraic manuscripts.

---

## GILL-CONTENT-408 — Ezra and the Great Synagogue claim is Gill’s theory
**Статус:** NEEDS ATTRIBUTION  
**Severity:** P1

Research states as historical fact that Ezra’s circle, under inspiration, fixed written vowel marks. Introduce it as Gill’s argument.

---

## GILL-CONTENT-409 — accents as inspired punctuation are confessional argument, not neutral linguistics
**Статус:** NEEDS ATTRIBUTION  
**Severity:** P1

Distinguish Gill’s doctrine of preservation from modern history of the Tiberian Masorah.

---

## GILL-CONTENT-410 — “academic proof” and “no assumptions” are false-green labels
**Статус:** EPISTEMIC LANGUAGE ERROR  
**Severity:** P1

A dossier can accurately reconstruct Gill’s argument without endorsing its present-day factual correctness.

---

# 113. Messianic prophecy dossier: chronology and lexical overstatement

## GILL-CONTENT-411 — Pseudo-Jonathan cannot prove a unanimous pre-Christian reading of Genesis 3:15
**Статус:** CONFIRMED HISTORICAL ERROR  
**Severity:** P0/P1

Modern scholarship dates the extant Targum Pseudo-Jonathan broadly in late antiquity or the medieval period; many place its final form after the Islamic conquests.

---

## GILL-CONTENT-412 — Targum evidence can show reception, not necessarily original audience meaning
**Статус:** METHODOLOGICAL  
**Severity:** P1

Correct formulation:

```text
Gill appealed to later Jewish interpretive traditions
as corroboration of a messianic reading.
```

---

## GILL-CONTENT-413 — Isaiah 53 evidence does not establish unanimous Jewish interpretation
**Статус:** HISTORIOGRAPHIC OVERCLAIM  
**Severity:** P1

Targum Jonathan and Sanhedrin 98b attest messianic strands. Jewish interpretation of Isaiah 53 has been diverse.

---

## GILL-CONTENT-414 — `almah` does not lexically mean “virgin” in an uncontested exclusive sense
**Статус:** CONFIRMED LEXICAL OVERSTATEMENT  
**Severity:** P1

Modern lexical discussion generally treats the word as a young woman of marriageable age whose virginity may be implied by context but is not encoded exclusively.

The Christian argument can include Septuagint `parthenos`, context of the sign and Matthew’s inspired use without overstating lexical unanimity.

---

## GILL-CONTENT-415 — “seven uses” needs morphology note
**Статус:** PRECISION  
**Severity:** P2

Depending on whether plural and title-like forms are counted, modern lexical inventories often report nine occurrences/forms. Identify the exact seven passages Gill examined.

---

## GILL-CONTENT-416 — “scientifically proved” is anachronistic
**Статус:** EDITORIAL  
**Severity:** P2

Use `argued philologically and historically`.

---

## GILL-CONTENT-417 — motives of Collins are presented as intention to destroy the Gospel
**Статус:** POLEMICAL MIND-READING  
**Severity:** P2

Describe Collins’s argument, historical consequences and Gill’s response without claiming private motive.

---

# 114. Revelation dossier: synthesis presented as primary quotation

## GILL-CONTENT-418 — dossier number is internally inconsistent
**Статус:** CONFIRMED  
**Severity:** P2

File name says 24; body says part 23 and volume 23.

---

## GILL-CONTENT-419 — exact seven-period dates need verse-level Gill locators
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P1

The dossier gives Ephesus 33–100, Smyrna 100–313, Pergamum 313–600 and Thyatira 600–1517 without quoting Gill for each boundary.

---

## GILL-CONTENT-420 — “ten imperial persecutions” is traditional Protestant schema
**Статус:** NEEDS ATTRIBUTION  
**Severity:** P2

It should not be presented as a modern uncontested count.

---

## GILL-CONTENT-421 — “one of Gill’s most influential models” is unsupported
**Статус:** NEEDS RECEPTION EVIDENCE  
**Severity:** P2

Influence requires later citations and reception evidence.

---

## GILL-CONTENT-422 — two witnesses narrative needs direct Exposition citation
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P1

Claims about 1260 years, faithful communities, Europe-wide suppression and final revival need exact Revelation locators.

---

## GILL-CONTENT-423 — Research still does not validate 1866–1913
**Статус:** CONFIRMED ABSENCE  
**Severity:** P1

No exact Gill passage in dossier 24 supports the current site’s “fulfilled prediction” chronology.

---

# 115. Sabbath dossier: useful primary text, unstable label

## GILL-CONTENT-424 — “first-day Sabbatarian” may mislead
**Статус:** TERMINOLOGY ISSUE  
**Severity:** P1

Gill is quoted as rejecting creation ordinance, perpetual moral force of the fourth commandment and continued Jewish Sabbath.

Safer:

```text
observer of the Lord’s Day as apostolic worship practice,
without classical confessional Sabbatarian foundation.
```

---

## GILL-CONTENT-425 — “Christian Sabbath” needs an exact Gill quotation
**Статус:** NEEDS PRIMARY LOCATOR  
**Severity:** P1

The dossier title uses the term more strongly than the quoted passage.

---

## GILL-CONTENT-426 — Practical Divinity locator remains edition-dependent
**Статус:** CROSS-REFERENCE TO 333–335  
**Severity:** P0/P1

`Book III ch.8` cannot be stabilized until the four-book/five-navigation-unit conflict is resolved.

---

## GILL-CONTENT-427 — tension with 1689 does not prove the Goat Yard congregation subscribed every 1689 clause
**Статус:** HISTORICAL PRECISION  
**Severity:** P1

Compare Gill with 1689. Do not call it his congregation’s formal standard without evidence of subscription.

---

## GILL-CONTENT-428 — Hebrews 4 → Gill’s two-stage millennium is editorial bridge
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P2

The dossier supplies no Gill quotation making this connection.

---

# 116. Song of Songs, baptism and singing

## GILL-CONTENT-429 — “the congregation needed consolation” is invented narrative psychology
**Статус:** RESEARCH-ONLY UNSOURCED  
**Severity:** P2

Need church minutes, preface or Gill’s statement.

---

## GILL-CONTENT-430 — 122 sermons and 1724–1728 sequence require primary locator
**Статус:** PARTLY IN PRODUCTION / NEEDS SOURCE  
**Severity:** P1

Current Part II states 122 Sunday morning sermons, begun 1724 and completed before 1728 publication. Add Rippon/page or Gill preface.

---

## GILL-CONTENT-431 — “first complete English translation of the Targum” is an unsupported superlative
**Статус:** RESEARCH-ONLY  
**Severity:** P1

Current production merely says a translation was included. Do not import the stronger claim without bibliography.

---

## GILL-CONTENT-432 — calling Gill a “mystic” needs definition
**Статус:** CONFIRMED PRODUCTION FRAMING  
**Severity:** P1/P2

Better `experiential and devotional theologian` unless the article defines `mystic`.

---

## GILL-CONTENT-433 — the Spurgeon evaluation of Song is not properly sourced
**Статус:** CONFIRMED PRODUCTION CLAIM  
**Severity:** P1

Need exact English wording and edition/page of *Commenting and Commentaries* or another primary Spurgeon work.

---

## GILL-CONTENT-434 — degree awarded “precisely for refuting Whiston” is unsupported causation
**Статус:** CONFIRMED PRODUCTION CLAIM  
**Severity:** P1

Need Marischal College record or diploma wording.

---

## GILL-CONTENT-435 — early baptism history is overstated as “exclusively confessing believers by immersion”
**Статус:** RESEARCH-ONLY HISTORICAL ERROR  
**Severity:** P0/P1

Immersion was an early normal mode. But the Didache permits pouring when water is insufficient, Tertullian discusses delaying baptism of children around the early third century, and infant baptism is not merely a medieval invention.

---

## GILL-CONTENT-436 — immersion and believer-only subjects are separate historical questions
**Статус:** METHODOLOGICAL  
**Severity:** P1

Evidence for immersion does not itself prove all recipients were adults or professing believers.

---

## GILL-CONTENT-437 — Abraham Taylor’s “health objection” needs exact work and quotation
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P2

---

## GILL-CONTENT-438 — singing dossiers contradict each other
**Статус:** CONFIRMED RESEARCH CONFLICT  
**Severity:** P1

Dossier 20 says psalms, hymns and spiritual songs include Davidic psalms and New Testament evangelical hymns. Dossier 29 quotes Gill saying “hymns” principally means another designation of the Psalter, while uninspired hymns may be used conditionally.

The second is more nuanced and should be canonical.

---

## GILL-CONTENT-439 — Gill’s contribution to “hymnographic tradition” is overstated
**Статус:** EDITORIAL  
**Severity:** P2

Gill defended congregational singing. Rippon later expanded hymnody. These are not identical contributions.

---

## GILL-CONTENT-440 — Egyptian Hallel numbering needs translation-system note
**Статус:** PRECISION  
**Severity:** P2

Use Psalms 113–118 in Hebrew/modern numbering and 112–117 in Septuagint/Church Slavonic numbering.

---

# 117. Good Works dossier: wrong archive item used as primary verification

## GILL-CONTENT-441 — `dissertationconc00gill` is the Hebrew dissertation, not Good Works
**Статус:** CONFIRMED WRONG-SOURCE LINK  
**Severity:** P0

Dossier 26 links the same Internet Archive identifier used for *A Dissertation Concerning the Antiquity of the Hebrew Language, Letters, Vowel-Points, and Accents* (London, 1767). It does not verify *A Dissertation Concerning Good Works*.

---

## GILL-CONTENT-442 — Level A verification of Good Works therefore did not occur
**Статус:** CONFIRMED FALSE-GREEN  
**Severity:** P0

The theological summary may still be accurate, but the cited file cannot support it.

---

## GILL-CONTENT-443 — exact bibliography of Good Works must be rebuilt
**Статус:** NEEDS EXACT SOURCE  
**Severity:** P0/P1

Required:

```text
full title
first publication date
edition used
placement in Sermons and Tracts
printed pages
stable scan
```

---

## GILL-CONTENT-444 — “four biblical supports” may be agent synthesis
**Статус:** NEEDS STRUCTURAL VERIFICATION  
**Severity:** P1

Check whether Gill himself divides the work into spring/principle, rule, end and necessity.

---

## GILL-CONTENT-445 — “absolute necessity” needs exact wording
**Статус:** NEEDS QUOTE  
**Severity:** P1

---

## GILL-CONTENT-446 — Russian typo changes the doctrinal sentence
**Статус:** CONFIRMED EDITORIAL BUG IN RESEARCH  
**Severity:** P2

`по мистии Божьей` must be `по милости Божьей`.

---

# 118. Miracles dossier: apologetic expansion beyond Gill’s text

## GILL-CONTENT-447 — commentary on miracles is not automatically a direct response to Woolston
**Статус:** NEEDS AUTHORIAL EVIDENCE  
**Severity:** P1

Chronological context and thematic overlap are insufficient. Need Gill naming Woolston or a preface identifying him as target.

---

## GILL-CONTENT-448 — Cana guests’ “absolute sobriety and holiness” is unsupported
**Статус:** RESEARCH-ONLY OVERCLAIM  
**Severity:** P1

---

## GILL-CONTENT-449 — “water carriers” are introduced into John 2 without textual basis
**Статус:** RESEARCH-ONLY TEXTUAL ERROR  
**Severity:** P1

The Gospel refers to servants.

---

## GILL-CONTENT-450 — John 11 does not identify all mourners as Pharisees and Sadducees
**Статус:** RESEARCH-ONLY TEXTUAL OVERREACH  
**Severity:** P1

It speaks of Jews who came to console the sisters.

---

## GILL-CONTENT-451 — “professional Roman armed detachment” is a harmonized inference
**Статус:** NEEDS QUALIFICATION  
**Severity:** P1

---

## GILL-CONTENT-452 — “hundreds of eyewitnesses” imports 1 Corinthians 15 into Matthew 28
**Статус:** SOURCE-MIXING  
**Severity:** P1

A cumulative resurrection argument can use both passages, but must identify each source.

---

## GILL-CONTENT-453 — “legally destroys the lie” is rhetorical, not analytical
**Статус:** EDITORIAL  
**Severity:** P2

Use `Gill argues that the report is internally inconsistent`.

---

# 119. Covenant dossier: genuine primary gains and new factual errors

## GILL-CONTENT-454 — Witsius was not a Westminster Assembly delegate
**Статус:** CONFIRMED FACTUAL ERROR  
**Severity:** P0/P1

Thomas Goodwin participated and William Twisse was prolocutor. Herman Witsius belonged to a later Dutch generation and was not a delegate.

---

## GILL-CONTENT-455 — Maccovius and Ames citations do not make Gill’s formulation confessional consensus
**Статус:** HISTORIOGRAPHIC OVERREACH  
**Severity:** P1

Precedents establish genealogy, not identical doctrine.

---

## GILL-CONTENT-456 — Gill did not “refute” the modern distinction as such
**Статус:** WORDING  
**Severity:** P1

He rejected making covenant of redemption and covenant of grace two separate eternal covenants. Use `Gill rejected the two-covenant formulation`.

---

## GILL-CONTENT-457 — Hebrew etymologies of `berit` need modern lexical caution
**Статус:** HISTORICAL PHILOLOGY  
**Severity:** P2

Gill’s proposed derivations are evidence of his method, not automatically current Hebrew etymology.

---

## GILL-CONTENT-458 — GAP-1 is only partially closed
**Статус:** CONFIRMED STATUS ERROR  
**Severity:** P1

Research found a supporting concept from Romans 8:1 but did not locate the exact quoted Adam/Christ sentence.

---

## GILL-CONTENT-459 — “faith because justified” must be included in the controversy section
**Статус:** CONTENT-BALANCE  
**Severity:** P1

Gill’s statement is highly relevant to eternal justification, temporal application, duty-faith and hyper-Calvinism classification.

---

# 120. Marrow/neonomian dossier: structural analogy becomes historical linkage

## GILL-CONTENT-460 — Gill did not participate in the Scottish Marrow controversy
**Статус:** POSITIVE CAVEAT, MUST CONTROL THE WHOLE DOSSIER  
**Severity:** P1

The dossier admits this but repeatedly describes both as two wings of one front. That is a modern comparative framework, not a documented historical network.

---

## GILL-CONTENT-461 — primary quotations accessed through London Lyceum remain secondary transmission
**Статус:** SOURCE-CLASS  
**Severity:** P1

Exact page references are helpful, but the actual scan should still be checked.

---

## GILL-CONTENT-462 — Baxter’s doctrine is presented as settled “new legal ground”
**Статус:** NEEDS ACADEMIC BALANCE  
**Severity:** P1

Baxter’s justification doctrine is disputed in scholarship. A confessional critique should be identified as such.

---

## GILL-CONTENT-463 — Stinton and twelve churches claim rests on a partisan source chain
**Статус:** NEEDS PRIMARY MINUTES  
**Severity:** P1

The 1704 Lorimers’ Hall episode needs meeting record, participants, adopted wording and academic study.

---

## GILL-CONTENT-464 — the two justification-work titles and publication histories remain unstable
**Статус:** NEEDS BIBLIOGRAPHIC NORMALIZATION  
**Severity:** P0/P1

Research distinguishes `Righteousness of Christ` and `Righteousness of Faith`, but dates, editions, sermon origin and reprints need a canonical catalogue.

---

## GILL-CONTENT-465 — corrupted mixed-language text remains in Research
**Статус:** CONFIRMED EDITORIAL BUG  
**Severity:** P2

`接收ающий` must be corrected to Russian.

---

# 121. Older Research dossiers still contain superseded doctrinal errors

## GILL-CONTENT-466 — dossier 04 gives the wrong content for Cause Part IV
**Статус:** CONFIRMED SUPERSEDED ERROR  
**Severity:** P0/P1

It describes Part IV as a vindication against Henry Heywood and divine illumination. Later primary verification in dossiers 12/19 establishes Part IV as patristic testimony before Augustine on the disputed doctrines.

---

## GILL-CONTENT-467 — dossier 04 places the eternal covenant in Book IV
**Статус:** CONFIRMED BOOK ERROR  
**Severity:** P0

The eternal covenant is Book II, chapter 7. Book IV concerns temporal administrations.

---

## GILL-CONTENT-468 — dossier 01 calls Doctrinal Divinity “three books”
**Статус:** CONFIRMED VOLUME/BOOK CONFUSION  
**Severity:** P0

It mixes three printed volumes with seven internal doctrinal books.

---

## GILL-CONTENT-469 — dossier 06 calls Body of Divinity “nine volumes / seven books”
**Статус:** CONFIRMED CORPUS CONFLATION  
**Severity:** P0

Nine volumes belong to the biblical *Exposition*, not the *Body of Divinity*.

---

## GILL-CONTENT-470 — Research’s Cause and theology article plans are superseded but not marked
**Статус:** CONFIRMED  
**Severity:** P1

Dossier 03 recommends broad Part IV; dossier 04 revises it to an exegetical focus; later dossiers expand again. No plan is marked canonical or superseded.

---

# 122. Current Astro Part II: new production findings from Research crosswalk

## GILL-CONTENT-471 — the Marischal degree is causally tied to Whiston without institutional evidence
**Статус:** CONFIRMED PRODUCTION CLAIM  
**Severity:** P1

Current text says Gill received the degree precisely for what refuted Whiston’s arguments. This is stronger than Rippon’s evidence.

---

## GILL-CONTENT-472 — Spurgeon’s Song evaluation needs primary recovery
**Статус:** CONFIRMED PRODUCTION CLAIM  
**Severity:** P1

See `GILL-CONTENT-433`.

---

## GILL-CONTENT-473 — “Gill as mystic” should not be a hidden classification
**Статус:** CONFIRMED PRODUCTION FRAMING  
**Severity:** P1/P2

See `GILL-CONTENT-432`.

---

## GILL-CONTENT-474 — Eastcheap duration is internally expressed as 26 and 27 years
**Статус:** NEEDS DATE ARITHMETIC / SOURCE  
**Severity:** P1

Heading says twenty-six years; body says 1729–1756 and twenty-seven years. Use exact dates rather than competing rounded durations.

---

## GILL-CONTENT-475 — farewell quotation is sourced through `Bunhill Memorials`, not Gill edition
**Статус:** SOURCE HIERARCHY  
**Severity:** P1

Need determine whether exact sermon text survives, whether Memorials paraphrases, and original title/edition/page.

---

## GILL-CONTENT-476 — “Baptists, Anglicans and Independents united to rent halls” needs names and source
**Статус:** CONFIRMED PRODUCTION CLAIM  
**Severity:** P1

---

## GILL-CONTENT-477 — Hervey is called member of Wesley’s Holy Club without source
**Статус:** NEEDS BIOGRAPHICAL CHECK  
**Severity:** P1

---

## GILL-CONTENT-478 — Hervey quotation is translated without work/page
**Статус:** CONFIRMED PRODUCTION QUOTE GAP  
**Severity:** P1

The source line says only `James Hervey, friend of Gill`.

---

## GILL-CONTENT-479 — Crisp is called a “martyr of grace doctrine” as Gill’s settled view
**Статус:** NEEDS EXACT SOURCE / EDITORIAL  
**Severity:** P1

Separate Gill’s editing, Gill’s defense, later classification and the site’s metaphorical verdict.

---

## GILL-CONTENT-480 — Part II currently inherits Research’s Ella-centred Whitefield narrative
**Статус:** CONFIRMED PROVENANCE CHAIN  
**Severity:** P1

The exact claims and rhetoric in the Astro file mirror dossier 30. They are not independent corroboration.

---

# 123. Updated P0/P1 queue after V11

## P0 — bibliographic and factual

1. Fix CCEL route/book-number mapping in dossiers 39, 40 and 42.
2. Correct Good Works archive identifier.
3. Correct Witsius/Westminster delegate claim.
4. Mark dossier 04 Cause Part IV description superseded.
5. Resolve Body volume/book conflations in dossiers 01 and 06.
6. Remove “only Christian Hebraist” from production.
7. Remove causal “degree precisely for refuting Whiston.”
8. Replace pre-Christian-unanimous Targum claims.
9. Reclassify vowel-point dissertation as historical position, not current proof.

## P1 — current Part II

1. Add dates/status to rabbinic-source table.
2. Replace “first readers” language.
3. Verify Genesis 1:2 and Exodus 19:9 Targum citations.
4. Source Spurgeon on Song.
5. Define or replace “mystic.”
6. Resolve Eastcheap 26/27 duration.
7. Source hall-rental denominational cooperation.
8. Source Hervey quotation.
9. Separate Whitefield evidence from Ella’s verdict.
10. Add direct source apparatus to the whole Part II research layer.

---

# 124. Итог одиннадцатого прохода

Research contains real primary discoveries, but its strongest hidden defect is now clear:

```text
digital route
was treated as
printed bibliography.
```

This generated false book numbers across several dossiers.

A second defect is historical:

```text
Gill’s eighteenth-century apologetic argument
was often rewritten as
present-day scholarly conclusion.
```

This is especially serious for antiquity of Hebrew vowel points, dating and authority of Targums, lexical meaning of `almah`, early baptismal history and historicist chronology of Revelation.

The site can preserve all of this as valuable intellectual history if it consistently says:

```text
Gill argued...
Gill appealed to...
Gill understood...
```

rather than:

```text
research has proved...
ancient Judaism unanimously believed...
the first readers heard...
```

---

# 125. FINAL MASTER STATUS

Этот документ является **единственным итоговым cumulative-аудитом** серии о Джоне Гилле и соответствующего отдела `FedorMilovanov/Research`.

Он:

- полностью включает все материалы V1–V11;
- содержит все находки `GILL-CONTENT-001` — `GILL-CONTENT-480`;
- не удаляет ранние наблюдения, даже если позднее они были уточнены;
- помечает уточнения, подтверждения и конфликты через перекрёстные ссылки;
- разделяет production-проблемы сайта и проблемы исследовательского репозитория;
- включает итоговые очереди P0/P1/P2, требования к источникам и полный индекс.

## Статус целостности

```text
Findings parsed: 480
Unique IDs: 480
Range: 001–480
Missing IDs: none
Duplicate canonical headings: none
```

Ссылочные упоминания старых ID внутри поздних разделов не являются дублями самих находок.

---

# 126. Как использовать итоговый файл

## Для редактора сайта

Начинать с разделов:

1. `127. Статистика и тяжесть`;
2. `128. Канонически подтверждённые факты`;
3. `129. Единый аварийный P0-реестр`;
4. `131. Route-by-route план`;
5. затем открывать полный блок соответствующего `GILL-CONTENT-*`.

## Для исследовательского агента

Перед новым поиском:

1. найти claim в полном индексе;
2. проверить, нет ли уже `NEEDS EXACT SOURCE`;
3. проверить Research-досье и current Astro;
4. не создавать новое досье, если claim уже существует;
5. обновить canonical registry и пометить старое значение `SUPERSEDED`.

## Для разработчика

Не переносить исправления только в prose body. Одновременно проверять:

```text
article body
page head / SEO
quiz
glossary
timeline
TOC
share text
series data
tooltips
image captions / alt
source list
```

---

# 127. Итоговая статистика находок

| Категория | Количество |
|---|---:|
| P0 / P0–P1 | 75 |
| P1 | 294 |
| P2 | 70 |
| Source upgrade | 4 |
| Ненормализованные / архитектурные | 37 |
| **Всего** | **480** |

Дополнительно:

```text
P0-containing findings: 75
Findings explicitly requiring source / verification: 101
```

Тяжесть отражает риск для содержания, а не сложность технического исправления.

---

# 128. Канонически подтверждённые факты, которые можно использовать при исправлении

Ниже собраны не все факты о Гилле, а только те, которые в ходе аудита получили устойчивую опору.

## Биография

```text
23 November 1697 Old Style — дата рождения по Риппону.
Около двенадцати лет — воздействие Быт. 3:9.
1 November 1716 — исповедание веры и крещение.
4 November 1716 — принятие в общину, Вечеря и Ис. 53.
Следующее воскресенье — первая проповедь на 1 Кор. 2:2.
1748 — степень D.D. от Marischal College, Aberdeen.
14 October 1771 — смерть.
Возраст по Риппону: 73 года, 10 месяцев, 10 дней.
```

## Семья

```text
Rippon: дочь умерла “in the thirteenth year”.
Это означает двенадцать лет, если выражение употреблено стандартно.
Точная дата рождения требует отдельной документальной сверки.
```

## Труды

```text
Exposition — 9 printed volumes: 6 Old Testament + 3 New Testament.
Doctrinal Divinity — 7 internal books.
Practical Divinity — 4 core books;
proselyte-baptism dissertation может быть присоединённой пятой навигационной единицей.
Eschatology / millennium — Doctrinal Divinity, Book VII, а не Practical Book V.
```

## Завет и оправдание

```text
Gill distinguishes eternal council and eternal covenant.
He treats covenant of redemption and covenant of grace as one covenant,
not two separate eternal covenants.
He distinguishes active eternal justification from passive manifestation
or termination upon the believer’s conscience.
Gill explicitly says faith is not the reason for justification;
faith is bestowed because of justification.
```

## Проповедь Евангелия

```text
Gill explicitly distinguishes proclamation/declaration from conditional offer.
The “heralds” passage belongs to Sermon 95,
not to the previously cited section of Cause of God and Truth.
Whether Gill affirmed universal duty to saving faith remains an interpretive dispute.
```

## Сперджен

```text
The verified Body of Divinity statement belongs to sermon no. 369,
25 March 1861, first sermon in the completed Metropolitan Tabernacle.
It should not be merged with the 1859 foundation-stone event.
```

## Церковь и государство

```text
Gill rejected Anglican ecclesiastical control and state-church polity.
He nevertheless assigned Christian magistrates positive coercive duties
toward public religion.
Therefore “complete modern separation of church and state” is inaccurate.
```

## Источниковая дисциплина

```text
A digital URL segment is not a printed book number.
A primary work accessed through a blog remains a secondary transcription channel.
A verified quotation does not automatically verify the interpretation built upon it.
```

---

# 129. Единый аварийный P0 / P0–P1 реестр

Все пункты ниже подробно раскрыты в основном корпусе документа.

| ID | Находка | Статус | Severity |
|---|---|---|---|
| GILL-CONTENT-035 | Quiz Part I даёт исторически неподтверждённый “правильный” ответ | CONFIRMED PRIMARY-SOURCE CONFLICT | P0 |
| GILL-CONTENT-036 | Ис. 53 прочитан не вечером крещения, а 4 ноября | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-037 | первая проповедь была 11 ноября, не в декабре | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-038 | возраст дочери и дата рождения не могут быть верны одновременно | CONFIRMED INTERNAL CONTRADICTION | P0 |
| GILL-CONTENT-039 | quiz повторяет неразрешённую ошибку возраста дочери | CONFIRMED DEPENDENT ERROR | P0 |
| GILL-CONTENT-041 | “почти сто лет после смерти Гилла” арифметически невозможно | CONFIRMED | P0 |
| GILL-CONTENT-042 | сноска “Written in 1800” у Риппона относится не к приёму членов | CONFIRMED PRIMARY-SOURCE MISREAD RISK | P0 |
| GILL-CONTENT-044 | возраст Гилла при смерти указан неверно | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-045 | координата могилы переписана неверно | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-054 | chain Keach → Stinton → Gill → Rippon → Spurgeon не является полной succession | CONFIRMED HISTORICAL OMISSION | P0/P1 |
| GILL-CONTENT-061 | structure Practical Divinity: четыре книги или пять | CONFIRMED CROSS-PAGE CONTRADICTION | P0 |
| GILL-CONTENT-086 | таблица “Книга I–IV” не является структурой *Body of Divinity* | CONFIRMED INTERNAL MISREPRESENTATION | P0/P1 |
| GILL-CONTENT-088 | “книга 5, глава 14” конфликтует с моделью четырёх practical books | CONFIRMED CROSS-PAGE/IN-PAGE CONFLICT | P0 |
| GILL-CONTENT-090 | “оправдание → возрождение → вера” не описывает систему без дополнительных уровней | CONFIRMED OVERSIMPLIFICATION | P0/P1 theology |
| GILL-CONTENT-092 | free offer, proclamation, invitation и command используются как синонимы | CONFIRMED CONCEPTUAL COLLAPSE | P0/P1 |
| GILL-CONTENT-097 | утверждение, что Гилл принял Риппона помощником, требует немедленной проверки | HIGH-RISK CHRONOLOGY | P0/P1 |
| GILL-CONTENT-101 | Part II остаётся без bibliography, хотя это самая цитатная статья | CONFIRMED | P0/P1 research integrity |
| GILL-CONTENT-108 | “Гилл учил долгу всех веровать” нельзя оставлять без Gill text | NEEDS PRIMARY TEXT | P0/P1 |
| GILL-CONTENT-113 | латинская транскрипция содержит грамматически подозрительные формы | NEEDS DIPLOMATIC SOURCE CHECK | P0/P1 text integrity |
| GILL-CONTENT-120 | “Итоговая” bibliography стоит в середине substantive narrative | CONFIRMED | P0/P1 |
| GILL-CONTENT-131 | Spravochnik даёт противоположный вывод Macritchie | CONFIRMED MAJOR RESEARCH ERROR | P0 |
| GILL-CONTENT-135 | Practical Divinity состоит из четырёх книг | CONFIRMED | P0 factual correction |
| GILL-CONTENT-136 | “Practical Divinity, book 5, chapter 14” невозможно | CONFIRMED INVALID LOCATOR | P0 |
| GILL-CONTENT-138 | artificial Book I–IV table подтверждённо не совпадает с оригиналом | CONFIRMED | P0/P1 |
| GILL-CONTENT-145 | “Gill искренне приглашал всех” не подтверждён проверенными academic sources | CONFIRMED SOURCE CONFLICT | P0/P1 |
| GILL-CONTENT-150 | thesis сама называет Gill одним из четырёх original hyper-Calvinists | CONFIRMED PRIMARY ACADEMIC SOURCE | P0 correction |
| GILL-CONTENT-152 | Macritchie прямо утверждает, что Nettles misrepresents Gill | CONFIRMED | P0/P1 table correction |
| GILL-CONTENT-155 | conclusion Macritchie даёт безусловный verdict внутри её methodology | CONFIRMED | P0 |
| GILL-CONTENT-162 | структура 7+4 зафиксирована на SBJT pp. 94–95 | CONFIRMED | P0 source upgrade |
| GILL-CONTENT-171 | Brown donation не подтверждён доступным официальным каталогом | STILL NEEDS INSTITUTIONAL VERIFICATION | P0/P1 |
| GILL-CONTENT-175 | current paragraph смешивает 16 августа 1859 и 25 марта 1861 | CONFIRMED EVENT CONFLATION | P0/P1 |
| GILL-CONTENT-185 | “General Baptist denomination almost disappeared” фактически неверно | CONFIRMED FACTUAL ERROR | P0 |
| GILL-CONTENT-188 | Act of Uniformity и Five Mile Act объединены в одно последствие | CONFIRMED LEGAL CONFLATION | P0/P1 |
| GILL-CONTENT-205 | Dissenters were not legally prohibited from having synods or central structures in the stated sense | CONFIRMED CATEGORY ERROR | P0/P1 |
| GILL-CONTENT-215 | “through two changes of pastors” before Spurgeon is false | CONFIRMED FACTUAL ERROR | P0 |
| GILL-CONTENT-241 | “наблюдение биографа” фактически является неназванной авторской цитатой | PSEUDO-ATTRIBUTION | P0/P1 |
| GILL-CONTENT-252 | blockquote может быть пересказом, а оформлен как прямая цитата | QUOTE-MODE UNCLEAR | P0/P1 |
| GILL-CONTENT-259 | `gigantic WALL` переведено как буквальная “стена-исполин” | HIGH-CONFIDENCE TRANSLATION ERROR | P0/P1 |
| GILL-CONTENT-274 | poverty/conscience saying exists in competing forms inside the series | INTERNAL QUOTE VARIANCE | P0/P1 |
| GILL-CONTENT-297 | Gill’s 1731 Trinity book was not simply a direct response to Salters’ Hall | CONFIRMED CAUSAL OVERREACH | P0/P1 |
| GILL-CONTENT-303 | Q2 and Q4 continue propagating already identified source problems | CROSS-REFERENCE | P0/P1 |
| GILL-CONTENT-317 | Research проверял старый MDX-слой, а текущая серия уже Astro | CONFIRMED STALENESS | P0/P1 integration |
| GILL-CONTENT-320 | corrected errors remain in summaries of the same file | CONFIRMED | P0/P1 |
| GILL-CONTENT-324 | Research’s own Spravochnik dossier retains the discarded John 6:37 chronology | CONFIRMED INTERNAL RESEARCH ERROR | P0 |
| GILL-CONTENT-325 | Research repeats the daughter-age error rather than resolving it | CONFIRMED | P0/P1 |
| GILL-CONTENT-333 | Research has both “four books” and “five books” as canonical facts | CONFIRMED INTERNAL CONFLICT | P0 |
| GILL-CONTENT-334 | Research’s own CCEL-derived outlines disagree on chapter placement | CONFIRMED | P0/P1 |
| GILL-CONTENT-336 | calling the proselyte dissertation “Book V” cannot validate the site’s eschatology citation | CONFIRMED | P0 |
| GILL-CONTENT-341 | Research interprets the John 1:7 passage in the opposite direction from Macritchie | MAJOR INTERPRETIVE CONFLICT | P0/P1 |
| GILL-CONTENT-344 | Research’s own files describe Gill’s position inconsistently | CONFIRMED | P0/P1 |
| GILL-CONTENT-352 | dossier 10 says “complete separation”; dossier 38 says establishmentarian | CONFIRMED INTERNAL CONTRADICTION | P0/P1 |
| GILL-CONTENT-360 | Research does not verify 52 folios or current holdings | CONFIRMED ABSENCE | P0/P1 |
| GILL-CONTENT-364 | Research misdates the Body of Divinity quotation to 1859 | CONFIRMED | P0/P1 |
| GILL-CONTENT-367 | Research confirms eschatology belongs to Doctrinal Book VII | CONFIRMED | P0 source upgrade |
| GILL-CONTENT-373 | no canonical supersession mechanism exists | CONFIRMED | P0/P1 |
| GILL-CONTENT-375 | CCEL route segment не является надёжным номером печатной книги | CONFIRMED SYSTEMIC LOCATOR BUG | P0 |
| GILL-CONTENT-376 | творение, невинность и провидение ошибочно названы Book IV | CONFIRMED RESEARCH ERROR | P0 |
| GILL-CONTENT-377 | христология ошибочно названа Book VI | CONFIRMED RESEARCH ERROR | P0 |
| GILL-CONTENT-378 | пневматология применения названа одновременно Book III и Book VII | CONFIRMED INTERNAL CONTRADICTION | P0 |
| GILL-CONTENT-382 | нужен canonical edition map для Doctrinal и Practical Divinity | SYSTEMIC REQUIREMENT | P0/P1 |
| GILL-CONTENT-394 | “only Christian Hebraist without university education…” is an unsupported absolute | CONFIRMED PRODUCTION SUPERLATIVE | P0/P1 |
| GILL-CONTENT-401 | bridge to Nicaea risks repeating a popular canon myth | CONTENT-RISK | P0/P1 |
| GILL-CONTENT-406 | Gill’s antiquity-of-vowel-points thesis is not current scholarly consensus | CONFIRMED HISTORIOGRAPHIC REQUIREMENT | P0/P1 |
| GILL-CONTENT-411 | Pseudo-Jonathan cannot prove a unanimous pre-Christian reading of Genesis 3:15 | CONFIRMED HISTORICAL ERROR | P0/P1 |
| GILL-CONTENT-426 | Practical Divinity locator remains edition-dependent | CROSS-REFERENCE TO 333–335 | P0/P1 |
| GILL-CONTENT-435 | early baptism history is overstated as “exclusively confessing believers by immersion” | RESEARCH-ONLY HISTORICAL ERROR | P0/P1 |
| GILL-CONTENT-441 | `dissertationconc00gill` is the Hebrew dissertation, not Good Works | CONFIRMED WRONG-SOURCE LINK | P0 |
| GILL-CONTENT-442 | Level A verification of Good Works therefore did not occur | CONFIRMED FALSE-GREEN | P0 |
| GILL-CONTENT-443 | exact bibliography of Good Works must be rebuilt | NEEDS EXACT SOURCE | P0/P1 |
| GILL-CONTENT-454 | Witsius was not a Westminster Assembly delegate | CONFIRMED FACTUAL ERROR | P0/P1 |
| GILL-CONTENT-464 | the two justification-work titles and publication histories remain unstable | NEEDS BIBLIOGRAPHIC NORMALIZATION | P0/P1 |
| GILL-CONTENT-466 | dossier 04 gives the wrong content for Cause Part IV | CONFIRMED SUPERSEDED ERROR | P0/P1 |
| GILL-CONTENT-467 | dossier 04 places the eternal covenant in Book IV | CONFIRMED BOOK ERROR | P0 |
| GILL-CONTENT-468 | dossier 01 calls Doctrinal Divinity “three books” | CONFIRMED VOLUME/BOOK CONFUSION | P0 |
| GILL-CONTENT-469 | dossier 06 calls Body of Divinity “nine volumes / seven books” | CONFIRMED CORPUS CONFLATION | P0 |

---

# 130. Единая очередь непроверенных источников и locator’ов

В таблицу включены находки, статус которых прямо содержит `NEEDS`, `UNVERIFIED`, `UNSUPPORTED` или `UNRESOLVED`.

| ID | Непроверенное или требующее источника утверждение | Статус |
|---|---|---|
| GILL-CONTENT-009 | “главное историческое достижение” Haykin нуждается в точной citation | NEEDS SOURCE EXACTNESS. |
| GILL-CONTENT-018 | Brown University donation claim требует Level A source | NEEDS PRIMARY VERIFICATION. |
| GILL-CONTENT-043 | “определила облик общины на следующие полтора века” не доказано | NEEDS LONGITUDINAL SOURCE |
| GILL-CONTENT-047 | последние слова жены собраны в одну последовательность без source layering | NEEDS PRIMARY TEXT OF FUNERAL SERMON |
| GILL-CONTENT-050 | “оксфордские профессора снимали шляпу” не привязано к источнику | NEEDS SOURCE |
| GILL-CONTENT-064 | eschatological “prediction” превращена в teleological praise | NEEDS SOURCE + EDITORIAL OVERREACH |
| GILL-CONTENT-067 | “миссионерская спячка в церквях, следовавших Gill” слишком широко | NEEDS QUANTIFIED HISTORICAL SOURCE |
| GILL-CONTENT-068 | “искренне приглашать” нуждается в точной source distinction | NEEDS TEXTUAL PROOF |
| GILL-CONTENT-071 | Macritchie conclusion пересказывается без pages | SOURCE EXISTS; INTERPRETATION NEEDS PAGE |
| GILL-CONTENT-082 | Q4 hardcodes конкретные Таргумы без ссылки на место в издании | NEEDS PRIMARY COMMENTARY CHECK |
| GILL-CONTENT-083 | quiz Q3 называет вывод Мюллера “оригинальным вкладом” без страницы | SOURCE EXISTS; EXACT CLAIM NEEDS PAGE |
| GILL-CONTENT-085 | “все прежние реформаты оставляли Духа наблюдателем” слишком широко | NEEDS COMPARATIVE SOURCE |
| GILL-CONTENT-089 | “первое систематическое богословие баптиста” размножено как SEO-факт | NEEDS DEFINED SCOPE |
| GILL-CONTENT-093 | “миссионерская спячка в церквях, следовавших Гиллу” — причинное обобщение | NEEDS QUANTIFIED HISTORIOGRAPHY |
| GILL-CONTENT-098 | “сопоставил все цитаты ВЗ” — абсолютное утверждение | NEEDS PRIMARY DESCRIPTION |
| GILL-CONTENT-104 | Richard Muller 2003 не имеет понятного supporting work | NEEDS BIBLIOGRAPHIC CORRECTION |
| GILL-CONTENT-105 | Gregory Willis / Wills требует canonical identity | NEEDS BIBLIOGRAPHIC NORMALIZATION |
| GILL-CONTENT-106 | David Engelsma row может смешивать его определение с вердиктом о Gill | NEEDS EXACT SOURCE |
| GILL-CONTENT-108 | “Гилл учил долгу всех веровать” нельзя оставлять без Gill text | NEEDS PRIMARY TEXT |
| GILL-CONTENT-110 | Q1 добавляет counterfactual, который может не принадлежать Haykin | NEEDS QUOTE EXACTNESS |
| GILL-CONTENT-113 | латинская транскрипция содержит грамматически подозрительные формы | NEEDS DIPLOMATIC SOURCE CHECK |
| GILL-CONTENT-114 | перевод “непобедимый” может менять грамматику надписи | NEEDS LATIN RE-TRANSLATION |
| GILL-CONTENT-134 | thesis label “первое системное исследование всей четвёрки” требует точной авторской формулы | NEEDS INTRODUCTION WORDING |
| GILL-CONTENT-143 | степень D.D. имеет конфликт 1747/1748 в современных источниках | NEEDS INSTITUTIONAL ARCHIVE |
| GILL-CONTENT-147 | схема “первые два оправдания virtual, не actual” не найдена в проверенной статье Haykin 2021 | NEEDS EXACT SOURCE |
| GILL-CONTENT-168 | Spurgeon “he is not my Rabbi” остаётся без exact locator | NEEDS EXACT PRIMARY SOURCE |
| GILL-CONTENT-169 | “star of the first magnitude” не найдено в проверенных searchable texts | NEEDS EXACT PRIMARY SOURCE |
| GILL-CONTENT-170 | событие foundation stone 16 августа 1859 подтверждается, содержание Gill speech — нет | EVENT CONFIRMED / QUOTATIONS UNVERIFIED |
| GILL-CONTENT-171 | Brown donation не подтверждён доступным официальным каталогом | STILL NEEDS INSTITUTIONAL VERIFICATION |
| GILL-CONTENT-173 | Aberdeen year remains 1747/1748 conflict | UNRESOLVED |
| GILL-CONTENT-177 | “not my Rabbi” можно сохранить только как поздний paraphrase | NEEDS EXACT LOCATOR |
| GILL-CONTENT-178 | “star of the first magnitude” остаётся неподтверждённой точной цитатой | NEEDS EXACT LOCATOR |
| GILL-CONTENT-186 | Particular Baptist “стабильность и рост” также идеализированы | NEEDS BALANCED HISTORIOGRAPHY |
| GILL-CONTENT-190 | перечисление Baxter/Flavel/Watson как библиотеки Gill не доказано | NEEDS LIBRARY CATALOGUE |
| GILL-CONTENT-197 | “could not be diplomat, officer, professor” is too categorical | NEEDS OFFICE-BY-OFFICE SCOPE |
| GILL-CONTENT-198 | “this is why Gill could not attend Oxford/Cambridge” is monocausal | NEEDS BIOGRAPHICAL PRECISION |
| GILL-CONTENT-201 | Gill support application needs exact Rippon locator | NEEDS PRIMARY PAGE |
| GILL-CONTENT-203 | Bristol Academy chronology/lineage needs institutional source | NEEDS EXACT SOURCE |
| GILL-CONTENT-204 | Stepney/Regent’s Park connection is too compressed | NEEDS GENEALOGICAL INSTITUTION MAP |
| GILL-CONTENT-206 | “about 500 coffeehouses by the 1720s” needs named quantitative source | NEEDS SOURCE |
| GILL-CONTENT-208 | Hanover Coffee House Baptist role lacks primary/academic support | NEEDS EXACT SOURCE |
| GILL-CONTENT-214 | “three times average dissenting congregation” needs dataset | NEEDS QUANTITATIVE SOURCE |
| GILL-CONTENT-218 | “Gill preferred speaking of Gospel rather than Methodists” lacks evidence | UNSUPPORTED PSYCHOLOGICAL CLAIM |
| GILL-CONTENT-219 | opening only on two market days needs source | NEEDS LOCAL/PRIMARY SOURCE |
| GILL-CONTENT-224 | own library and research programme by age 21 unsupported | NEEDS SOURCE |
| GILL-CONTENT-226 | “one of London’s largest private libraries” needs catalogue comparison | NEEDS QUANTITATIVE SOURCE |
| GILL-CONTENT-227 | “hundreds of direct citations where contemporaries cited second-hand” needs corpus study | NEEDS METHODOLOGICAL SUPPORT |
| GILL-CONTENT-237 | описание матери и “избрания как воздуха” не имеет источника | UNSUPPORTED FAMILY PSYCHOLOGY |
| GILL-CONTENT-238 | состав смешанной кеттерингской общины и её разделение нуждаются в локальном источнике | NEEDS CHURCH HISTORY |
| GILL-CONTENT-239 | богословская атмосфера Кеттеринга выводится из Hussey и Richard Davis без доказанной цепочки | NEEDS INFLUENCE EVIDENCE |
| GILL-CONTENT-240 | “оба были людьми великого благочестия и учёности” требует точного объекта и места | NEEDS EXACT PRIMARY LOCATOR |
| GILL-CONTENT-249 | союз Gill–Whitefield и различие по призыву изложены без первичных текстов | NEEDS TWO-SIDED SOURCE |
| GILL-CONTENT-254 | four districts / two brothers требует church-record verification | NEEDS PRIMARY RECORD |
| GILL-CONTENT-256 | invitation from Whitefield needs exact source | NEEDS PRIMARY/ACADEMIC LOCATOR |
| GILL-CONTENT-257 | support by “evangelical ministers of all denominations” is too broad | NEEDS NAMES AND SCOPE |
| GILL-CONTENT-258 | transatlantic pamphlet story and rarity explanation need bibliographic evidence | NEEDS EDITION/PROVENANCE RECORD |
| GILL-CONTENT-265 | Noble’s introduction of Gill to Particular Baptist Fund in 1718 needs exact record | NEEDS FUND MINUTES / BIOGRAPHY PAGE |
| GILL-CONTENT-266 | sequence of laying on hands and Gill’s role with deacons requires documentary wording | NEEDS PRIMARY TEXT |
| GILL-CONTENT-268 | “first attempt to create an educational society in 1752” is unnamed | NEEDS INSTITUTIONAL IDENTIFICATION |
| GILL-CONTENT-269 | quote about Baptists’ ignorance of learning lacks speaker and context | NEEDS EXACT QUOTE LOCATOR |
| GILL-CONTENT-273 | “prayer is the breath of a regenerate man” needs book/chapter/page | NEEDS PRIMARY LOCATOR |
| GILL-CONTENT-275 | “I am a Baptist…” needs exact polemical work | NEEDS PRIMARY LOCATOR |
| GILL-CONTENT-278 | Kettering fires are precise but uncited and weakly connected | NEEDS LOCAL HISTORY SOURCE |
| GILL-CONTENT-283 | “Kennington Common in direct line of sight” is a geospatial claim without proof | NEEDS HISTORICAL MAP / VIEW-SHED |
| GILL-CONTENT-284 | exact number of at least 141 executions needs source and date range | NEEDS QUANTITATIVE SOURCE |
| GILL-CONTENT-285 | Whitefield 29 April 1739 quotation needs journal edition/page | NEEDS PRIMARY LOCATOR |
| GILL-CONTENT-290 | 53/57 vote is broadly supported, but the procedural object is simplified | CORE FACT VERIFIED / DESCRIPTION NEEDS REWRITE |
| GILL-CONTENT-292 | denominational 14/2 and 1/14 counts lack a cited source | NEEDS EXACT ROLL/VOTE SOURCE |
| GILL-CONTENT-301 | Q1 translation needs original wording and translator | NEEDS EXACT QUOTE |
| GILL-CONTENT-329 | “University of Aberdeen” and “Marischal College” need one institutional record | NEEDS NORMALIZATION |
| GILL-CONTENT-331 | Research adds an “ivory tower” routine without page-level proof | NEEDS EXACT RIP PON LOCATOR |
| GILL-CONTENT-332 | Declaration articles and Sabellian revision are overstated | NEEDS TEXTUAL PRECISION |
| GILL-CONTENT-337 | Research’s 514-page figure is edition-specific | NEEDS EDITION ID |
| GILL-CONTENT-343 | “critics quote-mined Gill” is an editorial verdict | NEEDS EVIDENCE |
| GILL-CONTENT-368 | “two-phase premillennialism” is a modern synthesis | NEEDS ATTRIBUTION |
| GILL-CONTENT-379 | “Of Sanctification, ch. 14” можно считать подтверждённым только после edition mapping | NEEDS EDITION REGISTRY |
| GILL-CONTENT-387 | “Lightfoot of the Baptists” is a secondary nickname | NEEDS EXACT ATTRIBUTION |
| GILL-CONTENT-391 | Onkelos / Jerusalem Targum references on Genesis 1:2 need exact wording | NEEDS PRIMARY LOCATOR |
| GILL-CONTENT-392 | “Targum Jonathan on Exodus” requires name normalization | NEEDS TEXTUAL IDENTIFICATION |
| GILL-CONTENT-398 | “66 books” is a normalized count, not Gill’s quoted label | NEEDS PRECISION |
| GILL-CONTENT-408 | Ezra and the Great Synagogue claim is Gill’s theory | NEEDS ATTRIBUTION |
| GILL-CONTENT-409 | accents as inspired punctuation are confessional argument, not neutral linguistics | NEEDS ATTRIBUTION |
| GILL-CONTENT-419 | exact seven-period dates need verse-level Gill locators | NEEDS EXACT SOURCE |
| GILL-CONTENT-420 | “ten imperial persecutions” is traditional Protestant schema | NEEDS ATTRIBUTION |
| GILL-CONTENT-421 | “one of Gill’s most influential models” is unsupported | NEEDS RECEPTION EVIDENCE |
| GILL-CONTENT-422 | two witnesses narrative needs direct Exposition citation | NEEDS EXACT SOURCE |
| GILL-CONTENT-425 | “Christian Sabbath” needs an exact Gill quotation | NEEDS PRIMARY LOCATOR |
| GILL-CONTENT-428 | Hebrews 4 → Gill’s two-stage millennium is editorial bridge | NEEDS EXACT SOURCE |
| GILL-CONTENT-430 | 122 sermons and 1724–1728 sequence require primary locator | PARTLY IN PRODUCTION / NEEDS SOURCE |
| GILL-CONTENT-437 | Abraham Taylor’s “health objection” needs exact work and quotation | NEEDS EXACT SOURCE |
| GILL-CONTENT-443 | exact bibliography of Good Works must be rebuilt | NEEDS EXACT SOURCE |
| GILL-CONTENT-444 | “four biblical supports” may be agent synthesis | NEEDS STRUCTURAL VERIFICATION |
| GILL-CONTENT-445 | “absolute necessity” needs exact wording | NEEDS QUOTE |
| GILL-CONTENT-447 | commentary on miracles is not automatically a direct response to Woolston | NEEDS AUTHORIAL EVIDENCE |
| GILL-CONTENT-451 | “professional Roman armed detachment” is a harmonized inference | NEEDS QUALIFICATION |
| GILL-CONTENT-462 | Baxter’s doctrine is presented as settled “new legal ground” | NEEDS ACADEMIC BALANCE |
| GILL-CONTENT-463 | Stinton and twelve churches claim rests on a partisan source chain | NEEDS PRIMARY MINUTES |
| GILL-CONTENT-464 | the two justification-work titles and publication histories remain unstable | NEEDS BIBLIOGRAPHIC NORMALIZATION |
| GILL-CONTENT-474 | Eastcheap duration is internally expressed as 26 and 27 years | NEEDS DATE ARITHMETIC / SOURCE |
| GILL-CONTENT-477 | Hervey is called member of Wesley’s Holy Club without source | NEEDS BIOGRAPHICAL CHECK |
| GILL-CONTENT-479 | Crisp is called a “martyr of grace doctrine” as Gill’s settled view | NEEDS EXACT SOURCE / EDITORIAL |

---

# 131. Route-by-route итоговый план исправления

## A. Исторический контекст

Приоритеты:

1. разделить Act of Uniformity 1662, Conventicle Act 1664 и Five Mile Act 1665;
2. уточнить ограниченный характер Toleration Act;
3. разделить Test/Corporation Acts и университетские тесты;
4. переписать историю General Baptists с New Connexion 1770;
5. восстановить точный предмет голосования Salters’ Hall;
6. назвать James Peirce и Joseph Hallet;
7. убрать причинную прямую `Salters’ Hall → Gill’s Trinity treatise`;
8. проверить coffee-house network и Particular Baptist Fund;
9. синхронизировать Southwark context с Part I.

## B. Part I — Человек

Приоритеты:

1. исправить крещение, Ис. 53 и первую проповедь;
2. исправить quiz;
3. исправить возраст дочери;
4. убрать неподтверждённую психологию матери и семьи;
5. пометить birth prophecy как позднее свидетельство;
6. проверить ординационный “полный протокол”;
7. восстановить источники Personal Credo;
8. исправить перевод `WALL` и `Cleanly compell’d`;
9. отделить реконструкции от цитат;
10. добавить provenance всех изображений.

## C. Part II — Учёный

Приоритеты:

1. исправить структуру Doctrinal и Practical Divinity;
2. исправить eschatology locator;
3. создать нормальную bibliography;
4. удалить или сузить суперлативы о гебраистике;
5. переработать таблицу раввинистических источников;
6. проверить Targum Onkelos / Jerusalem / Pseudo-Jonathan;
7. не выдавать поздние традиции за голос первых читателей;
8. исправить степень/Whiston causation;
9. проверить Spurgeon и Hervey quotations;
10. разрешить Eastcheap 26/27;
11. не считать Ella независимым подтверждением Whitefield narrative;
12. различить Gill’s historical arguments и современный scholarly consensus.

## D. Part III — Наследие

Приоритеты:

1. определить единый словарь hyper-Calvinism / duty-faith / offer;
2. показать Rathel, Macritchie, Nettles, George и Ella раздельно;
3. не превращать active/passive justification в автоматическое оправдание Gill;
4. проверить Latin epitaph по дипломатической транскрипции;
5. исправить Spurgeon 1859/1861;
6. нормализовать Willis/Wills, Muller и другие библиографические имена;
7. проверить Brown University institutional records;
8. отделить history of Gillites от оценочного языка;
9. переставить bibliography в реальный конец;
10. привязать quiz к источникам смерти и эпитафии.

## E. Справочник

Приоритеты:

1. заменить все устаревшие timeline facts;
2. исправить 3 volumes / 7 books / 9 volumes;
3. нормализовать даты и издания;
4. создать canonical work catalogue;
5. добавить edition-specific locators;
6. исправить definition of Particular Baptists;
7. разделить eternal Sonship и eternal generation;
8. устранить конфликт Sandemanianism;
9. добавить источник к каждому glossary term;
10. не считать Top-10 editorial list историческим фактом.

## F. Shared series layer

Проверить:

```text
gillSeriesData.ts
TOC
reading times
series chronology
SEO
share text
quiz sourceRef
glossary ownership
source tooltips
image captions and alt
```

Особые дефекты:

- Part II TOC скрывает большинство секций;
- Part I TOC не ведёт к источникам;
- chronological labels do not match actual date coverage;
- quiz often freezes disputed claims as correct answers.

## G. Research repository

Не создавать dossier 43 до появления canonical layer.

Обязательные сущности:

```text
GILL_CANONICAL_CLAIMS.md
GILL_SOURCE_REGISTRY.yml
GILL_EDITION_REGISTRY.yml
GILL_QUOTE_REGISTRY.yml
GILL_RESEARCH_TO_SITE_CROSSWALK.md
GILL_SUPERSEDED_CLAIMS.yml
GILL_IMAGE_PROVENANCE.yml
```

Немедленно исправить:

1. MDX → current Astro target paths;
2. source-level definitions;
3. CCEL route/book mapping;
4. Good Works wrong Archive item;
5. John 6:37 conversion entry;
6. daughter age;
7. Cause Part IV;
8. Witsius/Westminster;
9. ten thousand sheets / ten million words;
10. church-state contradiction;
11. free-offer/duty-faith contradiction;
12. Spurgeon 1859/1861.

---

# 132. Каноническая модель доказательства

Каждый claim должен хранить четыре независимых статуса:

```yaml
claim_id:
canonical_wording:
claim_type:
  - date
  - quotation
  - interpretation
  - causal_claim
  - superlative
  - reconstruction

source:
  work:
  author:
  edition:
  volume:
  book:
  chapter:
  page:
  scan_url:
  access_host:

verification:
  transcription: exact | normalized | OCR | unchecked
  translation: project | published | adapted | none
  support: direct | partial | contextual | none
  interpretation: consensus | disputed | confessional | editorial
  confidence: high | medium | low

deployment:
  site_locations:
  research_locations:
  quiz_locations:
  glossary_locations:
  image_locations:

supersession:
  replaces:
  replaced_by:
```

Ключевой принцип:

```text
source quality
≠
transcription quality
≠
claim support
≠
interpretive certainty
```

---

# 133. Финальные acceptance gates

## Content integrity

- [ ] Все P0 закрыты или явно приняты как unresolved.
- [ ] Нет внутренних противоречий по датам.
- [ ] Нет `quote` без quote mode.
- [ ] Нет перевода цитаты без translator metadata.
- [ ] Нет суперлатива без определённого scope.
- [ ] Нет причинного вывода из одной временной близости.
- [ ] Нет современного scholarly verdict, приписанного Gill.

## Bibliography integrity

- [ ] Каждый work имеет edition registry.
- [ ] Volume/book/chapter/page не смешиваются.
- [ ] Digital route хранится отдельно.
- [ ] Archive identifier открыт и проверен.
- [ ] Secondary host не маркируется direct scan.
- [ ] Dead links заменены централизованно.

## Research integrity

- [ ] Каждый claim имеет canonical owner.
- [ ] Старые формулировки помечены superseded.
- [ ] Один source chain не считается несколькими свидетелями.
- [ ] Academic disagreement хранится как disagreement.
- [ ] Confessional judgment не маскируется под neutral history.

## Site integrity

- [ ] Body, quiz, glossary, SEO, share and TOC synchronized.
- [ ] Sources reachable from TOC.
- [ ] Image provenance visible to reader.
- [ ] Artistic reconstruction explicitly labeled.
- [ ] Current-person durations are computed or phrased “since YEAR.”

---

# 134. Полный компактный индекс всех 480 находок

Этот индекс предназначен для поиска и навигации. Полное обоснование каждого пункта находится выше в соответствующем блоке.

| ID | Заголовок находки | Статус | Severity |
|---|---|---|---|
| GILL-CONTENT-001 | Glasgow thesis 2025 подтверждена официально | OK / подтверждено. | — |
| GILL-CONTENT-002 | Part III table по hyper-Calvinism требует footnote на каждую позицию | — | — |
| GILL-CONTENT-003 | Part III использует свежий источник 2025 без статуса прочтения | — | — |
| GILL-CONTENT-004 | “Гилл стал единственным христианским гебраистом без университетского образования...” слишком сильное | — | — |
| GILL-CONTENT-005 | “беспрецедентно” по раввинистике требует смягчения | — | — |
| GILL-CONTENT-006 | таблица раввинистических источников смешивает corpus и использование | — | — |
| GILL-CONTENT-007 | “мистик” о Gill Song of Songs может вызвать неверную ассоциацию | — | — |
| GILL-CONTENT-008 | “еврейская традиция признаёт это толкование” требует нюанса | — | — |
| GILL-CONTENT-009 | “главное историческое достижение” Haykin нуждается в точной citation | NEEDS SOURCE EXACTNESS. | — |
| GILL-CONTENT-010 | “Арминианство и пелагианство есть жизнь и душа папства” требует pastoral framing | — | — |
| GILL-CONTENT-011 | “первое систематическое богословие, созданное баптистом” требует аккуратного scope | — | — |
| GILL-CONTENT-012 | structure Body of Divinity дана противоречиво | — | — |
| GILL-CONTENT-013 | “Гилл строил иначе: оправдание → возрождение → вера” требует осторожности | — | — |
| GILL-CONTENT-014 | tooltip pactum salutis и справочник противоречат друг другу | — | — |
| GILL-CONTENT-015 | glossary “Free Offer” слишком уверенно приписывает позицию “Gill and followers” | — | — |
| GILL-CONTENT-016 | glossary “Arminianism / Unitarianism” смешивает типы угроз | — | — |
| GILL-CONTENT-017 | Part III “никогда прежде и никогда после” почти наверняка требует смягчения | — | — |
| GILL-CONTENT-018 | Brown University donation claim требует Level A source | NEEDS PRIMARY VERIFICATION. | — |
| GILL-CONTENT-019 | “works still stored at Brown” требует catalogue link | — | — |
| GILL-CONTENT-020 | “единственный / крупнейший / первый” повторяются слишком часто | — | — |
| GILL-CONTENT-021 | tooltip definitions не имеют единого glossary source | — | — |
| GILL-CONTENT-022 | tooltip text должен быть print-safe и TTS-safe | — | — |
| GILL-CONTENT-023 | tooltip “hyper-Calvinism” хороший, но требует distinction “label vs doctrine” | — | — |
| GILL-CONTENT-024 | glossary card “Antinomianism” нуждается в softer “часто ложно обвиняли” | — | — |
| GILL-CONTENT-025 | Hebrew inscription uses Wisdom 3:1 | — | — |
| GILL-CONTENT-026 | Part I section facts часто без inline footnotes | — | — |
| GILL-CONTENT-027 | Part II has long quotations without precise page references | — | — |
| GILL-CONTENT-028 | Part III quote density is high but citation density is uneven | — | — |
| GILL-CONTENT-029 | Part II starts as “Trilogy” despite planned Part IV | — | — |
| GILL-CONTENT-030 | Part II begins at “III. Богословские труды” although page is Part II | — | — |
| GILL-CONTENT-031 | Part III begins at “V. Историческое влияние” without earlier I–IV on same page | — | — |
| GILL-CONTENT-032 | Part III has multiple endings | — | — |
| GILL-CONTENT-033 | source sections should be outside searchable narrative | — | — |
| GILL-CONTENT-034 | inline style debt inside article text harms future content editing | — | — |
| GILL-CONTENT-035 | Quiz Part I даёт исторически неподтверждённый “правильный” ответ | CONFIRMED PRIMARY-SOURCE CONFLICT | P0 |
| GILL-CONTENT-036 | Ис. 53 прочитан не вечером крещения, а 4 ноября | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-037 | первая проповедь была 11 ноября, не в декабре | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-038 | возраст дочери и дата рождения не могут быть верны одновременно | CONFIRMED INTERNAL CONTRADICTION | P0 |
| GILL-CONTENT-039 | quiz повторяет неразрешённую ошибку возраста дочери | CONFIRMED DEPENDENT ERROR | P0 |
| GILL-CONTENT-040 | Old Style → New Style в справочнике, вероятно, сдвинут на один день | HIGH-CONFIDENCE CALENDAR ERROR; FINAL ARCHIVAL VERIFY | P1 |
| GILL-CONTENT-041 | “почти сто лет после смерти Гилла” арифметически невозможно | CONFIRMED | P0 |
| GILL-CONTENT-042 | сноска “Written in 1800” у Риппона относится не к приёму членов | CONFIRMED PRIMARY-SOURCE MISREAD RISK | P0 |
| GILL-CONTENT-043 | “определила облик общины на следующие полтора века” не доказано | NEEDS LONGITUDINAL SOURCE | P1 |
| GILL-CONTENT-044 | возраст Гилла при смерти указан неверно | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-045 | координата могилы переписана неверно | CONFIRMED PRIMARY-SOURCE ERROR | P0 |
| GILL-CONTENT-046 | сайт убрал важное “probably” из оценки масштаба скорби | CONFIRMED SOURCE AMPLIFICATION | P1 |
| GILL-CONTENT-047 | последние слова жены собраны в одну последовательность без source layering | NEEDS PRIMARY TEXT OF FUNERAL SERMON | P1 |
| GILL-CONTENT-048 | “семилетие испытания сердца” подменяет документированную мотивацию | CONFIRMED INTERPRETIVE OVERWRITE | P1 |
| GILL-CONTENT-049 | “три пророчества” не перечислены как три независимых свидетельства | EDITORIAL CLARITY / SOURCE VERIFY | P2 |
| GILL-CONTENT-050 | “оксфордские профессора снимали шляпу” не привязано к источнику | NEEDS SOURCE | P1 |
| GILL-CONTENT-051 | таблица образования использует неаудируемые source labels | CONFIRMED | P1 |
| GILL-CONTENT-052 | “в девятнадцать выучил еврейский” слишком точно датировано | SOURCE DOES NOT SUPPORT EXACT MILESTONE | P1 |
| GILL-CONTENT-053 | хороший caveat Baptist Encyclopedia должен стать моделью всей серии | POSITIVE PATTERN | — |
| GILL-CONTENT-054 | chain Keach → Stinton → Gill → Rippon → Spurgeon не является полной succession | CONFIRMED HISTORICAL OMISSION | P0/P1 |
| GILL-CONTENT-055 | “четыре последовательных пастора — более двухсот лет” построено на сокращённой линии | CONFIRMED LOGICAL ERROR | P1 |
| GILL-CONTENT-056 | современный Peter Masters не должен быть бесконечно hardcoded | TEMPORALLY UNSTABLE CONTENT | P2 |
| GILL-CONTENT-057 | рассказ о степени D.D. повторён почти трижды подряд | CONFIRMED | P1 |
| GILL-CONTENT-058 | знаменитая фраза переведена неточно по порядку | MINOR QUOTE ACCURACY | P2 |
| GILL-CONTENT-059 | “таинства” расходятся с баптистским и первичным словоупотреблением | CONFIRMED TERMINOLOGY DRIFT | P1 |
| GILL-CONTENT-060 | Part II не имеет полноценного списка источников | CONFIRMED | P1 |
| GILL-CONTENT-061 | structure Practical Divinity: четыре книги или пять | CONFIRMED CROSS-PAGE CONTRADICTION | P0 |
| GILL-CONTENT-062 | даты Old Testament Exposition расходятся | CONFIRMED CROSS-PAGE CONTRADICTION | P1 |
| GILL-CONTENT-063 | Body of Doctrinal Divinity: 1767 или 1769 | EDITION/DATING AMBIGUITY | P1 |
| GILL-CONTENT-064 | eschatological “prediction” превращена в teleological praise | NEEDS SOURCE + EDITORIAL OVERREACH | P1 |
| GILL-CONTENT-065 | Sandemanianism одновременно назван продолжением Gill и его противником | CONFIRMED INTERNAL CONFLICT | P1 |
| GILL-CONTENT-066 | inline glossary, Part III flip glossary и Spravochnik не имеют одного owner | CONFIRMED | P1 |
| GILL-CONTENT-067 | “миссионерская спячка в церквях, следовавших Gill” слишком широко | NEEDS QUANTIFIED HISTORICAL SOURCE | P1 |
| GILL-CONTENT-068 | “искренне приглашать” нуждается в точной source distinction | NEEDS TEXTUAL PROOF | P1 |
| GILL-CONTENT-069 | Spravochnik “Top-10” ошибочно называет сборник consensus | CONFIRMED EDITORIAL OVERSTATEMENT | P2 |
| GILL-CONTENT-070 | Top-10 source hierarchy несбалансирована | CONFIRMED | P1/P2 |
| GILL-CONTENT-071 | Macritchie conclusion пересказывается без pages | SOURCE EXISTS; INTERPRETATION NEEDS PAGE | P1 |
| GILL-CONTENT-072 | undefined “Seymour” в disputes table | CONFIRMED | P2 |
| GILL-CONTENT-073 | `esse / bene esse` введены без определения | CONFIRMED | P2 |
| GILL-CONTENT-074 | русские переводы первоисточников не имеют translator metadata | CONFIRMED | P1 |
| GILL-CONTENT-075 | крещальный hymn translation должен быть назван поэтическим переложением, если он не literal | TRANSLATION QA REQUIRED | P2 |
| GILL-CONTENT-076 | художественные изображения подписаны как документальные сцены | PROVENANCE GAP | P1 |
| GILL-CONTENT-077 | “Charles Spurgeon, G3 Ministries” смешивает автора цитаты и современного посредника | CONFIRMED ATTRIBUTION ERROR | P1 |
| GILL-CONTENT-078 | “один ведущий обозреватель XIX века” должен быть назван | CONFIRMED SOURCE OPACITY | P1 |
| GILL-CONTENT-079 | вопрос о степени D.D. ведёт не к разделу степени | CONFIRMED | P1 functional/content navigation |
| GILL-CONTENT-080 | вопрос о `pactum salutis` ведёт к общей систематике, а не к специальному разделу | CONFIRMED | P1 |
| GILL-CONTENT-081 | Q1 приписывает Уистону мотив “недостойно серьёзного богослова” | EDITORIAL INFERENCE PRESENTED AS EXPLANATION | P1 |
| GILL-CONTENT-082 | Q4 hardcodes конкретные Таргумы без ссылки на место в издании | NEEDS PRIMARY COMMENTARY CHECK | P1 |
| GILL-CONTENT-083 | quiz Q3 называет вывод Мюллера “оригинальным вкладом” без страницы | SOURCE EXISTS; EXACT CLAIM NEEDS PAGE | P1 |
| GILL-CONTENT-084 | `pactum salutis` изложен дважды почти одним текстом | CONFIRMED | P1 editorial/content architecture |
| GILL-CONTENT-085 | “все прежние реформаты оставляли Духа наблюдателем” слишком широко | NEEDS COMPARATIVE SOURCE | P1 |
| GILL-CONTENT-086 | таблица “Книга I–IV” не является структурой *Body of Divinity* | CONFIRMED INTERNAL MISREPRESENTATION | P0/P1 |
| GILL-CONTENT-087 | приблизительные страницы таблицы не имеют проверяемого основания | CONFIRMED | P1 |
| GILL-CONTENT-088 | “книга 5, глава 14” конфликтует с моделью четырёх practical books | CONFIRMED CROSS-PAGE/IN-PAGE CONFLICT | P0 |
| GILL-CONTENT-089 | “первое систематическое богословие баптиста” размножено как SEO-факт | NEEDS DEFINED SCOPE | P1 |
| GILL-CONTENT-090 | “оправдание → возрождение → вера” не описывает систему без дополнительных уровней | CONFIRMED OVERSIMPLIFICATION | P0/P1 theology |
| GILL-CONTENT-091 | eternal justification представлен то как “основание”, то как состоявшееся оправдание | CONFIRMED TERMINOLOGY DRIFT | P1 |
| GILL-CONTENT-092 | free offer, proclamation, invitation и command используются как синонимы | CONFIRMED CONCEPTUAL COLLAPSE | P0/P1 |
| GILL-CONTENT-093 | “миссионерская спячка в церквях, следовавших Гиллу” — причинное обобщение | NEEDS QUANTIFIED HISTORIOGRAPHY | P1 |
| GILL-CONTENT-094 | современная millennial taxonomy выдана за собственную схему Гилла | CONFIRMED ANALYTICAL LAYER NOT LABELLED | P1 |
| GILL-CONTENT-095 | “предсказал миссионерское движение” превращает дату в исполненное пророчество | CONFIRMED EDITORIAL OVERREACH | P1 |
| GILL-CONTENT-096 | “единственный пастор” не следует из признания двух церковных должностей | CONFIRMED INVALID INFERENCE | P1 theology/polity |
| GILL-CONTENT-097 | утверждение, что Гилл принял Риппона помощником, требует немедленной проверки | HIGH-RISK CHRONOLOGY | P0/P1 |
| GILL-CONTENT-098 | “сопоставил все цитаты ВЗ” — абсолютное утверждение | NEEDS PRIMARY DESCRIPTION | P1 |
| GILL-CONTENT-099 | “равен и, возможно, превосходил университетских профессоров” не research claim | EDITORIAL PANEGYRIC | P2 |
| GILL-CONTENT-100 | таблица “метод Гилла” является современной реконструкцией | CONFIRMED | P1/P2 |
| GILL-CONTENT-101 | Part II остаётся без bibliography, хотя это самая цитатная статья | CONFIRMED | P0/P1 research integrity |
| GILL-CONTENT-102 | колонка “Позиция” содержит не позиции одного типа | CONFIRMED | P1 |
| GILL-CONTENT-103 | строка Macritchie не сообщает её вывода | CONFIRMED | P1 |
| GILL-CONTENT-104 | Richard Muller 2003 не имеет понятного supporting work | NEEDS BIBLIOGRAPHIC CORRECTION | P1 |
| GILL-CONTENT-105 | Gregory Willis / Wills требует canonical identity | NEEDS BIBLIOGRAPHIC NORMALIZATION | P2 |
| GILL-CONTENT-106 | David Engelsma row может смешивать его определение с вердиктом о Gill | NEEDS EXACT SOURCE | P1 |
| GILL-CONTENT-107 | “Haykin rehabilitates Gill” задаёт verdict до анализа | CONFIRMED FRAMING BIAS | P1 |
| GILL-CONTENT-108 | “Гилл учил долгу всех веровать” нельзя оставлять без Gill text | NEEDS PRIMARY TEXT | P0/P1 |
| GILL-CONTENT-109 | Q1 о Wesley ведёт в раздел пяти определений hyper-Calvinism | CONFIRMED | P1 |
| GILL-CONTENT-110 | Q1 добавляет counterfactual, который может не принадлежать Haykin | NEEDS QUOTE EXACTNESS | P1 |
| GILL-CONTENT-111 | Q4 об эпитафии ведёт к богословским источникам | CONFIRMED | P1 |
| GILL-CONTENT-112 | “два латинских эпитета” — редакционная конструкция | CONFIRMED | P1 |
| GILL-CONTENT-113 | латинская транскрипция содержит грамматически подозрительные формы | NEEDS DIPLOMATIC SOURCE CHECK | P0/P1 text integrity |
| GILL-CONTENT-114 | перевод “непобедимый” может менять грамматику надписи | NEEDS LATIN RE-TRANSLATION | P1 |
| GILL-CONTENT-115 | Q3 о Spurgeon проверяет не факт, а нравственную оценку сайта | CONFIRMED | P2 |
| GILL-CONTENT-116 | “Партикулярные баптисты” определены через неполный современный TULIP | CONFIRMED | P1 |
| GILL-CONTENT-117 | “вечное сыновство” и “вечное рождение” используются как одно и то же | CONFIRMED THEOLOGICAL CONFLATION | P1 |
| GILL-CONTENT-118 | Sandemanianism одновременно продолжает Gill и является тем, с чем Gill боролся | CONFIRMED INTERNAL CONTRADICTION | P1 |
| GILL-CONTENT-119 | glossary definitions не имеют source note | CONFIRMED | P1 |
| GILL-CONTENT-120 | “Итоговая” bibliography стоит в середине substantive narrative | CONFIRMED | P0/P1 |
| GILL-CONTENT-121 | bibliography не покрывает самые сильные поздние claims | CONFIRMED | P1 |
| GILL-CONTENT-122 | `Commenting and Commentaries` не заменяет source исторической речи 1859 года | CONFIRMED SOURCE MISMATCH RISK | P1 |
| GILL-CONTENT-123 | “Spurgeon, G3 Ministries” является неправильной атрибуцией | CONFIRMED | P1 |
| GILL-CONTENT-124 | Part III source list содержит неполную запись Nettles | CONFIRMED | P2 |
| GILL-CONTENT-125 | Part II скрывает большую часть research из собственного TOC | CONFIRMED | P1 |
| GILL-CONTENT-126 | Part II TOC делает H3 визуально top-level без реального H2 parent | CONFIRMED STRUCTURE DRIFT | P1 |
| GILL-CONTENT-127 | Part III TOC не приводит читателя к death/epitaph для quiz | CONFIRMED | P1 |
| GILL-CONTENT-128 | Spravochnik ошибочно называет SBJT 25.1 “современным консенсусом” | CONFIRMED SOURCE MISCHARACTERIZATION | P1 |
| GILL-CONTENT-129 | Haykin ошибочно сведен к роли “защитника” | CONFIRMED NUANCE LOSS | P1 |
| GILL-CONTENT-130 | “современная наука реабилитирует Гилла” не отражает официальный выпуск 2021 года | CONFIRMED FRAMING ERROR | P1 |
| GILL-CONTENT-131 | Spravochnik даёт противоположный вывод Macritchie | CONFIRMED MAJOR RESEARCH ERROR | P0 |
| GILL-CONTENT-132 | строка Macritchie в таблице скрывает её реальную позицию | CONFIRMED | P1 |
| GILL-CONTENT-133 | Macritchie прямо оспаривает Nettles, чего таблица не показывает | CONFIRMED | P1 |
| GILL-CONTENT-134 | thesis label “первое системное исследование всей четвёрки” требует точной авторской формулы | NEEDS INTRODUCTION WORDING | P2 |
| GILL-CONTENT-135 | Practical Divinity состоит из четырёх книг | CONFIRMED | P0 factual correction |
| GILL-CONTENT-136 | “Practical Divinity, book 5, chapter 14” невозможно | CONFIRMED INVALID LOCATOR | P0 |
| GILL-CONTENT-137 | приложение о крещении прозелитов не нужно превращать в пятую книгу | CONFIRMED CLASSIFICATION ERROR | P1 |
| GILL-CONTENT-138 | artificial Book I–IV table подтверждённо не совпадает с оригиналом | CONFIRMED | P0/P1 |
| GILL-CONTENT-139 | “первая баптистская систематика” подтверждается при уточнённой формуле | UPGRADED TO CONFIRMED WITH SCOPE | P2 wording |
| GILL-CONTENT-140 | полный verse-by-verse комментарий также подтверждён с scope | UPGRADED TO CONFIRMED WITH SCOPE | P2 |
| GILL-CONTENT-141 | Green поддерживает core claim о Church of England Articles, но не военную метафору | PARTLY CONFIRMED / RHETORIC OVERSTATED | P2 |
| GILL-CONTENT-142 | “Richard Muller (2003)” вероятно ошибочный год | HIGH-CONFIDENCE BIBLIOGRAPHIC ERROR | P1 |
| GILL-CONTENT-143 | степень D.D. имеет конфликт 1747/1748 в современных источниках | NEEDS INSTITUTIONAL ARCHIVE | P1 |
| GILL-CONTENT-144 | chronology commentary смешивает original publication, completion и later editions | CONFIRMED BIBLIOGRAPHIC MODEL PROBLEM | P1 |
| GILL-CONTENT-145 | “Gill искренне приглашал всех” не подтверждён проверенными academic sources | CONFIRMED SOURCE CONFLICT | P0/P1 |
| GILL-CONTENT-146 | “Nettles доказал duty-faith Gill” нельзя подавать как итог | CONFIRMED ACTIVE SCHOLARLY DISPUTE | P1 |
| GILL-CONTENT-147 | схема “первые два оправдания virtual, не actual” не найдена в проверенной статье Haykin 2021 | NEEDS EXACT SOURCE | P1 |
| GILL-CONTENT-148 | Rathel даёт более точную схему, чем стрелка сайта | CONFIRMED | P1 |
| GILL-CONTENT-149 | 1689 Confession conflict должен быть раскрыт, а не спрятан | CONFIRMED IMPORTANT THEOLOGICAL CONTEXT | P1 |
| GILL-CONTENT-150 | thesis сама называет Gill одним из четырёх original hyper-Calvinists | CONFIRMED PRIMARY ACADEMIC SOURCE | P0 correction |
| GILL-CONTENT-151 | Macritchie ограничивает предмет исследования, что сайт обязан сообщать | CONFIRMED IMPORTANT CAVEAT | P1 |
| GILL-CONTENT-152 | Macritchie прямо утверждает, что Nettles misrepresents Gill | CONFIRMED | P0/P1 table correction |
| GILL-CONTENT-153 | Rathel criticism of Nettles имеет точный locator | CONFIRMED | P1 |
| GILL-CONTENT-154 | Macritchie фиксирует внутреннее изменение позиции Nettles | CONFIRMED | P1 |
| GILL-CONTENT-155 | conclusion Macritchie даёт безусловный verdict внутри её methodology | CONFIRMED | P0 |
| GILL-CONTENT-156 | thesis подтверждает, что термин anachronistic, но считает его необходимым | CONFIRMED | P1 glossary nuance |
| GILL-CONTENT-157 | 1689 Confession quotation имеет точный locator | CONFIRMED | P1 source upgrade |
| GILL-CONTENT-158 | Haykin article прямо связывает eternal justification и rejection of free offer | CONFIRMED | P1 |
| GILL-CONTENT-159 | distinction proclamation / offer подтверждён первичным Gill через Haykin | CONFIRMED | P1 glossary architecture |
| GILL-CONTENT-160 | `esse / bene esse` имеет точную страницу и точный смысл | CONFIRMED | P1 source upgrade |
| GILL-CONTENT-161 | простая стрелка сайта частично отражает Rathel, но теряет active/passive distinction | REFINED | P1 |
| GILL-CONTENT-162 | структура 7+4 зафиксирована на SBJT pp. 94–95 | CONFIRMED | P0 source upgrade |
| GILL-CONTENT-163 | ordinances находятся в Practical Book Three | CONFIRMED | P1 |
| GILL-CONTENT-164 | private worship / family section находится в Practical Book Four | CONFIRMED | P1 |
| GILL-CONTENT-165 | таблица должна различать “denial of offer” и “denial of duty-faith” | CONFIRMED | P1 |
| GILL-CONTENT-166 | таблица должна показывать methodological bias thesis | CONFIRMED | P2 fairness |
| GILL-CONTENT-167 | current phrase “пять конкурирующих определений” не соответствует реальному количеству позиций | CONFIRMED | P2 |
| GILL-CONTENT-168 | Spurgeon “he is not my Rabbi” остаётся без exact locator | NEEDS EXACT PRIMARY SOURCE | P1 |
| GILL-CONTENT-169 | “star of the first magnitude” не найдено в проверенных searchable texts | NEEDS EXACT PRIMARY SOURCE | P1 |
| GILL-CONTENT-170 | событие foundation stone 16 августа 1859 подтверждается, содержание Gill speech — нет | EVENT CONFIRMED / QUOTATIONS UNVERIFIED | P1 |
| GILL-CONTENT-171 | Brown donation не подтверждён доступным официальным каталогом | STILL NEEDS INSTITUTIONAL VERIFICATION | P0/P1 |
| GILL-CONTENT-172 | source list Brown опирается на secondary historical overviews | CONFIRMED | P1 |
| GILL-CONTENT-173 | Aberdeen year remains 1747/1748 conflict | UNRESOLVED | P1 |
| GILL-CONTENT-174 | найдена проверяемая первичная формула богословской независимости Сперджена | PRIMARY SERMON LOCATOR IDENTIFIED | P1 source replacement |
| GILL-CONTENT-175 | current paragraph смешивает 16 августа 1859 и 25 марта 1861 | CONFIRMED EVENT CONFLATION | P0/P1 |
| GILL-CONTENT-176 | “sermon XLV” не соответствует найденному primary locator | HIGH-CONFIDENCE CITATION ERROR | P1 |
| GILL-CONTENT-177 | “not my Rabbi” можно сохранить только как поздний paraphrase | NEEDS EXACT LOCATOR | P1 |
| GILL-CONTENT-178 | “star of the first magnitude” остаётся неподтверждённой точной цитатой | NEEDS EXACT LOCATOR | P1 |
| GILL-CONTENT-179 | source list Part III не содержит sermon 369 | CONFIRMED SOURCE GAP | P1 |
| GILL-CONTENT-180 | Elizabethan Settlement не “учредил Англиканскую церковь” с нуля | HISTORICAL OVERCOMPRESSION | P1 |
| GILL-CONTENT-181 | 1608–1612 объединяет разные события Baptist origins | CONFIRMED CHRONOLOGY COMPRESSION | P1 |
| GILL-CONTENT-182 | корни General Baptists через Dutch Mennonites упрощены | CONFIRMED NUANCE LOSS | P1 |
| GILL-CONTENT-183 | “две почти не пересекающиеся ветви” слишком абсолютно | EDITORIAL OVERSTATEMENT | P2 |
| GILL-CONTENT-184 | “дрейф в унитарианство после 1719” создаёт ложную монокаузальность | HISTORIOGRAPHIC OVERSIMPLIFICATION | P1 |
| GILL-CONTENT-185 | “General Baptist denomination almost disappeared” фактически неверно | CONFIRMED FACTUAL ERROR | P0 |
| GILL-CONTENT-186 | Particular Baptist “стабильность и рост” также идеализированы | NEEDS BALANCED HISTORIOGRAPHY | P1 |
| GILL-CONTENT-187 | “духовная родина Гилла родилась в 1662” стирает более раннюю Baptist history | EDITORIAL OVERSTATEMENT | P1 |
| GILL-CONTENT-188 | Act of Uniformity и Five Mile Act объединены в одно последствие | CONFIRMED LEGAL CONFLATION | P0/P1 |
| GILL-CONTENT-189 | “Act of Uniformity created Nonconformity” нуждается в caveat | HISTORICAL OVERSTATEMENT | P1 |
| GILL-CONTENT-190 | перечисление Baxter/Flavel/Watson как библиотеки Gill не доказано | NEEDS LIBRARY CATALOGUE | P1 |
| GILL-CONTENT-191 | memory narrative о стариках, подвалах и сараях является reconstruction | EDITORIAL INFERENCE | P2 |
| GILL-CONTENT-192 | Gill не был просто “первым поколением без угрозы тюрьмы” | OVERSTATED TOLERATION | P1 |
| GILL-CONTENT-193 | “prestigious invitations to Bristol or London” требует проверки | INTERNAL/FACTUAL RISK | P1 |
| GILL-CONTENT-194 | предложенная трёхступенчатая система слишком жёсткая | HISTORICAL TERMINOLOGY ISSUE | P1 |
| GILL-CONTENT-195 | Test/Corporation Acts не являются единственной причиной university exclusion | CONFIRMED LEGAL CAUSATION ERROR | P1 |
| GILL-CONTENT-196 | repeal in 1828 did not fully open Oxbridge | CONFIRMED | P1 |
| GILL-CONTENT-197 | “could not be diplomat, officer, professor” is too categorical | NEEDS OFFICE-BY-OFFICE SCOPE | P2 |
| GILL-CONTENT-198 | “this is why Gill could not attend Oxford/Cambridge” is monocausal | NEEDS BIOGRAPHICAL PRECISION | P1 |
| GILL-CONTENT-199 | `Suo Marte` literal gloss is presented as “more accurate” than idiom | TRANSLATION ERROR | P2 |
| GILL-CONTENT-200 | “universities for the expelled” is a metaphor, not uniform institutional status | EDITORIAL LABEL | P2 |
| GILL-CONTENT-201 | Gill support application needs exact Rippon locator | NEEDS PRIMARY PAGE | P1 |
| GILL-CONTENT-202 | Particular Baptist Fund 1717 is not supported by current bibliography | SOURCE COVERAGE GAP | P1 |
| GILL-CONTENT-203 | Bristol Academy chronology/lineage needs institutional source | NEEDS EXACT SOURCE | P1 |
| GILL-CONTENT-204 | Stepney/Regent’s Park connection is too compressed | NEEDS GENEALOGICAL INSTITUTION MAP | P1 |
| GILL-CONTENT-205 | Dissenters were not legally prohibited from having synods or central structures in the stated sense | CONFIRMED CATEGORY ERROR | P0/P1 |
| GILL-CONTENT-206 | “about 500 coffeehouses by the 1720s” needs named quantitative source | NEEDS SOURCE | P2 |
| GILL-CONTENT-207 | `British Coffee House` identification may be wrong or ambiguous | HIGH-RISK GEOGRAPHIC ERROR | P1 |
| GILL-CONTENT-208 | Hanover Coffee House Baptist role lacks primary/academic support | NEEDS EXACT SOURCE | P1 |
| GILL-CONTENT-209 | George Ella cannot be sole authority for “Coffee House Association” | SOURCE QUALITY ISSUE | P1 |
| GILL-CONTENT-210 | Gill’s suspicion of coffee-house hierarchy is inferred, not demonstrated | EDITORIAL INFERENCE | P1 |
| GILL-CONTENT-211 | ordination by senior ministers does not prove the proposed authority theory | INVALID INFERENCE | P2 |
| GILL-CONTENT-212 | Southwark industrial atmosphere needs local-history sourcing | SOURCE COVERAGE GAP | P2 |
| GILL-CONTENT-213 | images and captions remain documentary-looking reconstructions | PROVENANCE/EDITORIAL | P1 |
| GILL-CONTENT-214 | “three times average dissenting congregation” needs dataset | NEEDS QUANTITATIVE SOURCE | P1 |
| GILL-CONTENT-215 | “through two changes of pastors” before Spurgeon is false | CONFIRMED FACTUAL ERROR | P0 |
| GILL-CONTENT-216 | Whitefield’s 30,000 is an estimate, not measured attendance | SOURCE NUANCE | P2 |
| GILL-CONTENT-217 | “they almost certainly heard of each other every week” is invented frequency | EDITORIAL SPECULATION | P2 |
| GILL-CONTENT-218 | “Gill preferred speaking of Gospel rather than Methodists” lacks evidence | UNSUPPORTED PSYCHOLOGICAL CLAIM | P1/P2 |
| GILL-CONTENT-219 | opening only on two market days needs source | NEEDS LOCAL/PRIMARY SOURCE | P1 |
| GILL-CONTENT-220 | “bargained for Buxtorf grammar” is an invented scene unless sourced | NARRATIVE RECONSTRUCTION | P1 |
| GILL-CONTENT-221 | father’s “own fulling mill” conflicts with other descriptions | INTERNAL BIOGRAPHICAL CONTRADICTION | P1 |
| GILL-CONTENT-222 | Hebrew proficiency at fifteen conflicts with checked sources | P0/P1 CHRONOLOGY CONFLICT | — |
| GILL-CONTENT-223 | “ordinary for Oxford graduate” is rhetorical, not measurable | EDITORIAL PANEGYRIC | P2 |
| GILL-CONTENT-224 | own library and research programme by age 21 unsupported | NEEDS SOURCE | P1 |
| GILL-CONTENT-225 | absence of university curriculum as intellectual advantage is romanticized causation | EDITORIAL INFERENCE | P2 |
| GILL-CONTENT-226 | “one of London’s largest private libraries” needs catalogue comparison | NEEDS QUANTITATIVE SOURCE | P1 |
| GILL-CONTENT-227 | “hundreds of direct citations where contemporaries cited second-hand” needs corpus study | NEEDS METHODOLOGICAL SUPPORT | P1 |
| GILL-CONTENT-228 | bibliography claims greater coverage than it provides | CONFIRMED | P1 |
| GILL-CONTENT-229 | legal sources do not support all educational conclusions | SOURCE SCOPE ERROR | P1 |
| GILL-CONTENT-230 | Kennington source cannot support all Southwark claims | SOURCE SCOPE ERROR | P1 |
| GILL-CONTENT-231 | automated source availability check produced mixed results | LINK QA NOTE | P2 |
| GILL-CONTENT-232 | PRDL count is correctly stated but not an authored bibliography | SOURCE NUANCE | P2 |
| GILL-CONTENT-233 | “Context 1697–1719” contradicts the actual article | CONFIRMED | P1 |
| GILL-CONTENT-234 | Part II “1729–1748” excludes most of its own contents | CONFIRMED | P1 |
| GILL-CONTENT-235 | Part III “1748–1771” also excludes its afterlife subject | CONFIRMED | P1 |
| GILL-CONTENT-236 | заголовок “гении без университетов” заранее навязывает итог | EDITORIAL / HAGIOGRAPHIC FRAMING | P2 |
| GILL-CONTENT-237 | описание матери и “избрания как воздуха” не имеет источника | UNSUPPORTED FAMILY PSYCHOLOGY | P1/P2 |
| GILL-CONTENT-238 | состав смешанной кеттерингской общины и её разделение нуждаются в локальном источнике | NEEDS CHURCH HISTORY | P1 |
| GILL-CONTENT-239 | богословская атмосфера Кеттеринга выводится из Hussey и Richard Davis без доказанной цепочки | NEEDS INFLUENCE EVIDENCE | P1 |
| GILL-CONTENT-240 | “оба были людьми великого благочестия и учёности” требует точного объекта и места | NEEDS EXACT PRIMARY LOCATOR | P1 |
| GILL-CONTENT-241 | “наблюдение биографа” фактически является неназванной авторской цитатой | PSEUDO-ATTRIBUTION | P0/P1 |
| GILL-CONTENT-242 | “первоисточники вместо пересказов профессоров” — ложная дихотомия | EDITORIAL ROMANTICIZATION | P2 |
| GILL-CONTENT-243 | Higham Ferrers назван “практикой” и “пробным годом” | ANACHRONISTIC VOCABULARY | P2 |
| GILL-CONTENT-244 | “значительное число обращённых уже тогда” опирается на Baptist Encyclopedia 1881 | LATE SECONDARY CLAIM | P1 |
| GILL-CONTENT-245 | “получил наставление не от людей, а от Писания” неверно описывает ординационную проповедь | RHETORICAL FALSE CONTRAST | P2 |
| GILL-CONTENT-246 | Elias Keach подтверждён как основатель первой Baptist church Pennsylvania, но “прародительница всех” чрезмерно | PARTLY VERIFIED / OVERSTATED | P1 |
| GILL-CONTENT-247 | текущее служение Peter Masters подтверждается, но “56 лет” нельзя хранить в body | EXISTING GILL-CONTENT-056 UPDATED | P1 maintenance |
| GILL-CONTENT-248 | chapel/pulpit images выглядят как документальные изображения | PROVENANCE GAP | P1 |
| GILL-CONTENT-249 | союз Gill–Whitefield и различие по призыву изложены без первичных текстов | NEEDS TWO-SIDED SOURCE | P1 |
| GILL-CONTENT-250 | “у самых стен прихода Gill” географически и экклесиологически неточно | EDITORIAL EXAGGERATION | P2 |
| GILL-CONTENT-251 | главный рассказ идёт через George Ella → The Baptist Particular → сайт | LONG SECONDARY SOURCE CHAIN | P1 |
| GILL-CONTENT-252 | blockquote может быть пересказом, а оформлен как прямая цитата | QUOTE-MODE UNCLEAR | P0/P1 |
| GILL-CONTENT-253 | “восстановил церковь на библейском основании” является конфессиональной оценкой | EDITORIAL / POLEMICAL | P2 |
| GILL-CONTENT-254 | four districts / two brothers требует church-record verification | NEEDS PRIMARY RECORD | P1 |
| GILL-CONTENT-255 | “еженедельно достигал более тысячи” не является числом уникальных людей | QUANTITATIVE MISLEADINGNESS | P1 |
| GILL-CONTENT-256 | invitation from Whitefield needs exact source | NEEDS PRIMARY/ACADEMIC LOCATOR | P1 |
| GILL-CONTENT-257 | support by “evangelical ministers of all denominations” is too broad | NEEDS NAMES AND SCOPE | P1 |
| GILL-CONTENT-258 | transatlantic pamphlet story and rarity explanation need bibliographic evidence | NEEDS EDITION/PROVENANCE RECORD | P1 |
| GILL-CONTENT-259 | `gigantic WALL` переведено как буквальная “стена-исполин” | HIGH-CONFIDENCE TRANSLATION ERROR | P0/P1 |
| GILL-CONTENT-260 | `Cleanly compell’d` does not mean “чистым словом” | TRANSLATION ERROR | P1 |
| GILL-CONTENT-261 | poem contains a chain of name-puns not explained | TRANSLATION/COMMENTARY GAP | P1 |
| GILL-CONTENT-262 | “ability to take a city he besieges” does not come from the poem | SOURCE CONTAMINATION | P1 |
| GILL-CONTENT-263 | title “полный протокол” exceeds the evidence shown | EDITORIAL OVERCLAIM | P1 |
| GILL-CONTENT-264 | church founding date varies across the series | INTERNAL CHRONOLOGY CONFLICT | P1 |
| GILL-CONTENT-265 | Noble’s introduction of Gill to Particular Baptist Fund in 1718 needs exact record | NEEDS FUND MINUTES / BIOGRAPHY PAGE | P1 |
| GILL-CONTENT-266 | sequence of laying on hands and Gill’s role with deacons requires documentary wording | NEEDS PRIMARY TEXT | P1 |
| GILL-CONTENT-267 | grant for Skepp library and “foundation of nine-volume commentary” are two separate claims | SOURCE + CAUSATION ISSUE | P1 |
| GILL-CONTENT-268 | “first attempt to create an educational society in 1752” is unnamed | NEEDS INSTITUTIONAL IDENTIFICATION | P1 |
| GILL-CONTENT-269 | quote about Baptists’ ignorance of learning lacks speaker and context | NEEDS EXACT QUOTE LOCATOR | P1 |
| GILL-CONTENT-270 | John Martin’s move to hear Gill is broadly supported; later “chief defender against Fuller” needs source | PARTLY VERIFIED | P2 |
| GILL-CONTENT-271 | conversions under Gill do not settle the hyper-Calvinism classification | INVALID APOLOGETIC INFERENCE | P1 |
| GILL-CONTENT-272 | Colton Strother is a tertiary collector, not final source | SOURCE HIERARCHY ISSUE | P1 |
| GILL-CONTENT-273 | “prayer is the breath of a regenerate man” needs book/chapter/page | NEEDS PRIMARY LOCATOR | P1 |
| GILL-CONTENT-274 | poverty/conscience saying exists in competing forms inside the series | INTERNAL QUOTE VARIANCE | P0/P1 |
| GILL-CONTENT-275 | “I am a Baptist…” needs exact polemical work | NEEDS PRIMARY LOCATOR | P1 |
| GILL-CONTENT-276 | “three personal statements” mixes different genres | EDITORIAL CATEGORY ERROR | P2 |
| GILL-CONTENT-277 | translations have no translator or quote mode | CONFIRMED | P1 |
| GILL-CONTENT-278 | Kettering fires are precise but uncited and weakly connected | NEEDS LOCAL HISTORY SOURCE | P2 |
| GILL-CONTENT-279 | “Gill and Carey came from the same soil” is literary, not genealogical | EDITORIAL | P2 |
| GILL-CONTENT-280 | bridges are mentioned as context for Carter Lane move without evidence | URBAN CAUSATION SPECULATION | P2 |
| GILL-CONTENT-281 | 1720–1757 is not uniformly the “peak” of Gin Craze | PERIODIZATION OVERSTATEMENT | P1 |
| GILL-CONTENT-282 | Gin Acts chronology should cite legislation, not only two popular histories | SOURCE-TYPE GAP | P1 |
| GILL-CONTENT-283 | “Kennington Common in direct line of sight” is a geospatial claim without proof | NEEDS HISTORICAL MAP / VIEW-SHED | P1 |
| GILL-CONTENT-284 | exact number of at least 141 executions needs source and date range | NEEDS QUANTITATIVE SOURCE | P1 |
| GILL-CONTENT-285 | Whitefield 29 April 1739 quotation needs journal edition/page | NEEDS PRIMARY LOCATOR | P1 |
| GILL-CONTENT-286 | Marischal degree was not simply “unavailable” because English universities were closed | CAUSAL OVERSTATEMENT | P1 |
| GILL-CONTENT-287 | Bunhill Fields “pantheon” paragraph mixes burial history and university exclusion | RHETORICAL CONFLATION | P2 |
| GILL-CONTENT-288 | `Dissenting Praise` appears mismatched as an education source | BIBLIOGRAPHIC SCOPE RISK | P1 |
| GILL-CONTENT-289 | Southwark context exists in two independently maintained versions | DUPLICATE CLAIM OWNERSHIP | P1 |
| GILL-CONTENT-290 | 53/57 vote is broadly supported, but the procedural object is simplified | CORE FACT VERIFIED / DESCRIPTION NEEDS REWRITE | P1 |
| GILL-CONTENT-291 | the Exeter ministers should be named | CONTEXT GAP | P1 |
| GILL-CONTENT-292 | denominational 14/2 and 1/14 counts lack a cited source | NEEDS EXACT ROLL/VOTE SOURCE | P1 |
| GILL-CONTENT-293 | “Bible carried it by four” should be attributed to Sir Joseph Jekyll tradition | SOURCE ATTRIBUTION CORRECTION | P1 |
| GILL-CONTENT-294 | non-subscription did not itself constitute Arianism | POSITIVE NUANCE, RETAIN | P2 |
| GILL-CONTENT-295 | subsequent Unitarian drift is not proof that every non-subscriber’s principle caused it | CAUSALITY WARNING | P1 |
| GILL-CONTENT-296 | “Particular Baptists preserved orthodoxy: 14 to 2” overgeneralizes a delegate sample | INVALID GENERALIZATION | P1 |
| GILL-CONTENT-297 | Gill’s 1731 Trinity book was not simply a direct response to Salters’ Hall | CONFIRMED CAUSAL OVERREACH | P0/P1 |
| GILL-CONTENT-298 | “without Salters’ Hall it is impossible to understand Gill” is rhetorical totalization | EDITORIAL | P2 |
| GILL-CONTENT-299 | context bibliography lacks a dedicated Salters’ Hall source | SOURCE COVERAGE GAP | P1 |
| GILL-CONTENT-300 | Q1 should explicitly test “Rippon’s reported anecdote,” not the historical event | QUIZ EPISTEMIC FRAMING | P1 |
| GILL-CONTENT-301 | Q1 translation needs original wording and translator | NEEDS EXACT QUOTE | P1 |
| GILL-CONTENT-302 | Q3 introduces Isaac Watts although the body section does not establish that target | QUIZ ADDS UNSOURCED FACT | P1 |
| GILL-CONTENT-303 | Q2 and Q4 continue propagating already identified source problems | CROSS-REFERENCE | P0/P1 |
| GILL-CONTENT-304 | several sources actually used in body are absent | CONFIRMED | P1 |
| GILL-CONTENT-305 | “encyclopedic pages were not the basis” conflicts with repeated Cathcart dependence | CONFIRMED SOURCE-POLICY CONTRADICTION | P1 |
| GILL-CONTENT-306 | vague bibliography entries are not checkable records | CONFIRMED | P1 |
| GILL-CONTENT-307 | legislation entries do not cover university and honorary-degree conclusions | SOURCE SCOPE ERROR | P1 |
| GILL-CONTENT-308 | sources are article-level, not claim-level | SYSTEMIC | P1 |
| GILL-CONTENT-309 | inspected Gill captions contain no reconstruction disclosure | CONFIRMED MARKUP FACT | P1 |
| GILL-CONTENT-310 | captions use documentary grammar | PROVENANCE RISK | P1 |
| GILL-CONTENT-311 | alt text also asserts specificity | ACCESSIBILITY + HISTORICAL INTEGRITY | P1 |
| GILL-CONTENT-312 | visual source registry is required | SYSTEMIC | P1 |
| GILL-CONTENT-313 | Part I TOC omits its source section | CONFIRMED | P2 |
| GILL-CONTENT-314 | source section exists but quiz `sourceRef` links only back to prose | EVIDENCE GRAPH GAP | P2 |
| GILL-CONTENT-315 | Research уже является полноценным отдельным отделом, а не набором заметок | CONFIRMED | architectural |
| GILL-CONTENT-316 | Research нарушает собственное правило против фрагментации | CONFIRMED REPOSITORY-GOVERNANCE CONFLICT | P1 process |
| GILL-CONTENT-317 | Research проверял старый MDX-слой, а текущая серия уже Astro | CONFIRMED STALENESS | P0/P1 integration |
| GILL-CONTENT-318 | уровни источников определены в Research по-разному | CONFIRMED SYSTEMIC CONFLICT | P1 |
| GILL-CONTENT-319 | “Level A” is often assigned to text accessed through a secondary host | CONFIRMED PROVENANCE COLLAPSE | P1 |
| GILL-CONTENT-320 | corrected errors remain in summaries of the same file | CONFIRMED | P0/P1 |
| GILL-CONTENT-321 | the master map is a historical snapshot, not a current canonical index | CONFIRMED | P2 |
| GILL-CONTENT-322 | “all key doctrines verified” exceeds what the files actually prove | CONFIRMED EPISTEMIC OVERCLAIM | P1 |
| GILL-CONTENT-323 | Research confirms the conversion/baptism chronology established in V4 | CONFIRMED BY RESEARCH PRIMARY DOSSIER | source upgrade |
| GILL-CONTENT-324 | Research’s own Spravochnik dossier retains the discarded John 6:37 chronology | CONFIRMED INTERNAL RESEARCH ERROR | P0 |
| GILL-CONTENT-325 | Research repeats the daughter-age error rather than resolving it | CONFIRMED | P0/P1 |
| GILL-CONTENT-326 | Research confirms the seven-year delay was not simply “heart examination” | CONFIRMED | source upgrade |
| GILL-CONTENT-327 | school withdrawal is incorrectly elevated to the sole cause of no university education | CONFIRMED RESEARCH OVERREACH | P1 |
| GILL-CONTENT-328 | Research contains competing D.D. quotations | CONFIRMED QUOTE VARIANCE | P1 |
| GILL-CONTENT-329 | “University of Aberdeen” and “Marischal College” need one institutional record | NEEDS NORMALIZATION | P1 |
| GILL-CONTENT-330 | Research correctly identifies “ten thousand” as sheets, then continues asserting ten million words | CONFIRMED INTERNAL CONTRADICTION | P1 |
| GILL-CONTENT-331 | Research adds an “ivory tower” routine without page-level proof | NEEDS EXACT RIP PON LOCATOR | P1 |
| GILL-CONTENT-332 | Declaration articles and Sabellian revision are overstated | NEEDS TEXTUAL PRECISION | P1 |
| GILL-CONTENT-333 | Research has both “four books” and “five books” as canonical facts | CONFIRMED INTERNAL CONFLICT | P0 |
| GILL-CONTENT-334 | Research’s own CCEL-derived outlines disagree on chapter placement | CONFIRMED | P0/P1 |
| GILL-CONTENT-335 | “expanded editions” is used to explain away structure conflict without evidence | CONFIRMED | P1 |
| GILL-CONTENT-336 | calling the proselyte dissertation “Book V” cannot validate the site’s eschatology citation | CONFIRMED | P0 |
| GILL-CONTENT-337 | Research’s 514-page figure is edition-specific | NEEDS EDITION ID | P2 |
| GILL-CONTENT-338 | Research provides strong primary anchors for `proclamation ≠ offer` | CONFIRMED POSITIVE FINDING | source upgrade |
| GILL-CONTENT-339 | Research correctly discovered a misattribution of the “heralds” quotation | CONFIRMED | P1 |
| GILL-CONTENT-340 | Research converts “external duty” into “external gospel call to all” without sufficient proof | INTERPRETIVE OVERREACH | P1 |
| GILL-CONTENT-341 | Research interprets the John 1:7 passage in the opposite direction from Macritchie | MAJOR INTERPRETIVE CONFLICT | P0/P1 |
| GILL-CONTENT-342 | Declaration articles VII–VIII do not prove duty-faith | INVALID INFERENCE IN RESEARCH | P1 |
| GILL-CONTENT-343 | “critics quote-mined Gill” is an editorial verdict | NEEDS EVIDENCE | P1 |
| GILL-CONTENT-344 | Research’s own files describe Gill’s position inconsistently | CONFIRMED | P0/P1 |
| GILL-CONTENT-345 | a six-term soteriological glossary is now mandatory | SYSTEMIC | P1 |
| GILL-CONTENT-346 | Research correctly verifies active/passive justification | CONFIRMED POSITIVE FINDING | source upgrade |
| GILL-CONTENT-347 | “justification from eternity” versus “eternal justification” is not an established neutral distinction | PARTISAN TERMINOLOGY | P1 |
| GILL-CONTENT-348 | Research conflates declaration in conscience with juridical application through faith | THEOLOGICAL PRECISION ISSUE | P1 |
| GILL-CONTENT-349 | historical precedents do not settle the orthodoxy of Gill’s exact formulation | INVALID HISTORIOGRAPHIC INFERENCE | P1 |
| GILL-CONTENT-350 | Research largely omits the 1689 Confession 11.4 tension | CONFIRMED OMISSION | P1 |
| GILL-CONTENT-351 | “active/passive distinction saves Gill from the label” is not a source finding | EDITORIAL VERDICT | P1 |
| GILL-CONTENT-352 | dossier 10 says “complete separation”; dossier 38 says establishmentarian | CONFIRMED INTERNAL CONTRADICTION | P0/P1 |
| GILL-CONTENT-353 | `Dissenters’ Reasons` does not prove modern separationism | CONFIRMED | P1 |
| GILL-CONTENT-354 | political theology must be integrated into the site’s legal-context narrative | CONTENT GAP | P1 |
| GILL-CONTENT-355 | dossier 30 is not primary verification | CONFIRMED | P1 |
| GILL-CONTENT-356 | label “white facts” is inappropriate | EPISTEMIC LABEL ERROR | P1 |
| GILL-CONTENT-357 | active ministry does not determine the duty-faith classification | INVALID APOLOGETIC INFERENCE | P1 |
| GILL-CONTENT-358 | Research’s Great Awakening dossier is the likely source of site overstatement | CONFIRMED PROVENANCE | P1 |
| GILL-CONTENT-359 | Research confirms Brown claims remain secondary | CONFIRMED | P1 |
| GILL-CONTENT-360 | Research does not verify 52 folios or current holdings | CONFIRMED ABSENCE | P0/P1 |
| GILL-CONTENT-361 | recommendation, donation and financial support are bundled from one modern overview | SOURCE-CONCENTRATION RISK | P1 |
| GILL-CONTENT-362 | period name should be Rhode Island College | HISTORICAL WORDING | P2 |
| GILL-CONTENT-363 | Edwards citations are one of the best verified new contributions in Research | CONFIRMED POSITIVE FINDING | P2 |
| GILL-CONTENT-364 | Research misdates the Body of Divinity quotation to 1859 | CONFIRMED | P0/P1 |
| GILL-CONTENT-365 | Research’s Spurgeon corpus remains mostly secondary | CONFIRMED | P1 |
| GILL-CONTENT-366 | sermon 369 should become the canonical Spurgeon evidence | RECOMMENDATION | P1 |
| GILL-CONTENT-367 | Research confirms eschatology belongs to Doctrinal Book VII | CONFIRMED | P0 source upgrade |
| GILL-CONTENT-368 | “two-phase premillennialism” is a modern synthesis | NEEDS ATTRIBUTION | P1 |
| GILL-CONTENT-369 | Research does not substantiate the site’s 1866–1913 “prediction fulfilled” narrative | CONFIRMED ABSENCE | P1 |
| GILL-CONTENT-370 | site content cannot be an evidentiary Level B for itself | CIRCULAR VERIFICATION | P1 |
| GILL-CONTENT-371 | dead links are known but remain embedded across dossiers | CONFIRMED | P1 |
| GILL-CONTENT-372 | source status and claim status are conflated | SYSTEMIC | P1 |
| GILL-CONTENT-373 | no canonical supersession mechanism exists | CONFIRMED | P0/P1 |
| GILL-CONTENT-374 | duplicate source chains create false corroboration | SYSTEMIC | P1 |
| GILL-CONTENT-375 | CCEL route segment не является надёжным номером печатной книги | CONFIRMED SYSTEMIC LOCATOR BUG | P0 |
| GILL-CONTENT-376 | творение, невинность и провидение ошибочно названы Book IV | CONFIRMED RESEARCH ERROR | P0 |
| GILL-CONTENT-377 | христология ошибочно названа Book VI | CONFIRMED RESEARCH ERROR | P0 |
| GILL-CONTENT-378 | пневматология применения названа одновременно Book III и Book VII | CONFIRMED INTERNAL CONTRADICTION | P0 |
| GILL-CONTENT-379 | “Of Sanctification, ch. 14” можно считать подтверждённым только после edition mapping | NEEDS EDITION REGISTRY | P1 |
| GILL-CONTENT-380 | primitivebaptist.net TOC нельзя использовать как Level A edition authority | SOURCE-CLASS ERROR | P1 |
| GILL-CONTENT-381 | ошибка book mapping подрывает заявления “все ключевые доктрины верифицированы” | CONFIRMED | P1 |
| GILL-CONTENT-382 | нужен canonical edition map для Doctrinal и Practical Divinity | SYSTEMIC REQUIREMENT | P0/P1 |
| GILL-CONTENT-383 | правило веры по Рим. 12:6 не проверено в полном первичном контексте | RESEARCH-ONLY / PARTIAL | P1 |
| GILL-CONTENT-384 | “external standard = Creed” может преувеличить роль символов | THEOLOGICAL PRECISION ISSUE | P1 |
| GILL-CONTENT-385 | historicist interpretation is not simple “literal-historical exegesis” | CATEGORY ERROR | P1 |
| GILL-CONTENT-386 | “Catholic in spirit” is a modern editorial characterization | EDITORIAL | P2 |
| GILL-CONTENT-387 | “Lightfoot of the Baptists” is a secondary nickname | NEEDS EXACT ATTRIBUTION | P2 |
| GILL-CONTENT-388 | rabbinic literature is repeatedly mislabeled “Second Temple literature” | CONFIRMED CATEGORY ERROR | P1 |
| GILL-CONTENT-389 | Jerusalem Talmud is presented as direct apostolic-era context | CONFIRMED PRODUCTION CLAIM | P1 |
| GILL-CONTENT-390 | “hear the text as its first readers heard it” is anachronistic | CONFIRMED PRODUCTION CLAIM | P1 |
| GILL-CONTENT-391 | Onkelos / Jerusalem Targum references on Genesis 1:2 need exact wording | NEEDS PRIMARY LOCATOR | P1 |
| GILL-CONTENT-392 | “Targum Jonathan on Exodus” requires name normalization | NEEDS TEXTUAL IDENTIFICATION | P1 |
| GILL-CONTENT-393 | Zohar “critical acquaintance” has no evidence | CONFIRMED PRODUCTION UNSOURCED CLAIM | P1 |
| GILL-CONTENT-394 | “only Christian Hebraist without university education…” is an unsupported absolute | CONFIRMED PRODUCTION SUPERLATIVE | P0/P1 |
| GILL-CONTENT-395 | “unprecedented for an eighteenth-century Christian” is likewise unbounded | CONFIRMED PRODUCTION SUPERLATIVE | P1 |
| GILL-CONTENT-396 | the rabbinic table is a modern reconstruction | CONFIRMED | P1 |
| GILL-CONTENT-397 | dossier 41 calls a modern transcription Level A while admitting no scan check | CONFIRMED INTERNAL CONTRADICTION | P1 |
| GILL-CONTENT-398 | “66 books” is a normalized count, not Gill’s quoted label | NEEDS PRECISION | P2 |
| GILL-CONTENT-399 | “always received by the Church” must be presented as Gill’s claim | HISTORIOGRAPHIC QUALIFICATION | P1 |
| GILL-CONTENT-400 | church testimony is corroborative, not the final ground of authority | THEOLOGICAL PRECISION | P1 |
| GILL-CONTENT-401 | bridge to Nicaea risks repeating a popular canon myth | CONTENT-RISK | P0/P1 |
| GILL-CONTENT-402 | bracketed historical names inside a “verbatim quote” need audit | QUOTE-INTEGRITY | P1 |
| GILL-CONTENT-403 | the inspiration nuance is valuable and should be preserved | CONFIRMED POSITIVE FINDING | P2 |
| GILL-CONTENT-404 | Louis Cappel is wrongly labeled a rationalist critic | CONFIRMED HISTORICAL ERROR IN RESEARCH | P1 |
| GILL-CONTENT-405 | Brian Walton likewise cannot be reduced to “rationalist” | HISTORICAL OVERFRAMING | P1 |
| GILL-CONTENT-406 | Gill’s antiquity-of-vowel-points thesis is not current scholarly consensus | CONFIRMED HISTORIOGRAPHIC REQUIREMENT | P0/P1 |
| GILL-CONTENT-407 | oral vocalization tradition does not prove ancient written vowel signs | INVALID INFERENCE | P1 |
| GILL-CONTENT-408 | Ezra and the Great Synagogue claim is Gill’s theory | NEEDS ATTRIBUTION | P1 |
| GILL-CONTENT-409 | accents as inspired punctuation are confessional argument, not neutral linguistics | NEEDS ATTRIBUTION | P1 |
| GILL-CONTENT-410 | “academic proof” and “no assumptions” are false-green labels | EPISTEMIC LANGUAGE ERROR | P1 |
| GILL-CONTENT-411 | Pseudo-Jonathan cannot prove a unanimous pre-Christian reading of Genesis 3:15 | CONFIRMED HISTORICAL ERROR | P0/P1 |
| GILL-CONTENT-412 | Targum evidence can show reception, not necessarily original audience meaning | METHODOLOGICAL | P1 |
| GILL-CONTENT-413 | Isaiah 53 evidence does not establish unanimous Jewish interpretation | HISTORIOGRAPHIC OVERCLAIM | P1 |
| GILL-CONTENT-414 | `almah` does not lexically mean “virgin” in an uncontested exclusive sense | CONFIRMED LEXICAL OVERSTATEMENT | P1 |
| GILL-CONTENT-415 | “seven uses” needs morphology note | PRECISION | P2 |
| GILL-CONTENT-416 | “scientifically proved” is anachronistic | EDITORIAL | P2 |
| GILL-CONTENT-417 | motives of Collins are presented as intention to destroy the Gospel | POLEMICAL MIND-READING | P2 |
| GILL-CONTENT-418 | dossier number is internally inconsistent | CONFIRMED | P2 |
| GILL-CONTENT-419 | exact seven-period dates need verse-level Gill locators | NEEDS EXACT SOURCE | P1 |
| GILL-CONTENT-420 | “ten imperial persecutions” is traditional Protestant schema | NEEDS ATTRIBUTION | P2 |
| GILL-CONTENT-421 | “one of Gill’s most influential models” is unsupported | NEEDS RECEPTION EVIDENCE | P2 |
| GILL-CONTENT-422 | two witnesses narrative needs direct Exposition citation | NEEDS EXACT SOURCE | P1 |
| GILL-CONTENT-423 | Research still does not validate 1866–1913 | CONFIRMED ABSENCE | P1 |
| GILL-CONTENT-424 | “first-day Sabbatarian” may mislead | TERMINOLOGY ISSUE | P1 |
| GILL-CONTENT-425 | “Christian Sabbath” needs an exact Gill quotation | NEEDS PRIMARY LOCATOR | P1 |
| GILL-CONTENT-426 | Practical Divinity locator remains edition-dependent | CROSS-REFERENCE TO 333–335 | P0/P1 |
| GILL-CONTENT-427 | tension with 1689 does not prove the Goat Yard congregation subscribed every 1689 clause | HISTORICAL PRECISION | P1 |
| GILL-CONTENT-428 | Hebrews 4 → Gill’s two-stage millennium is editorial bridge | NEEDS EXACT SOURCE | P2 |
| GILL-CONTENT-429 | “the congregation needed consolation” is invented narrative psychology | RESEARCH-ONLY UNSOURCED | P2 |
| GILL-CONTENT-430 | 122 sermons and 1724–1728 sequence require primary locator | PARTLY IN PRODUCTION / NEEDS SOURCE | P1 |
| GILL-CONTENT-431 | “first complete English translation of the Targum” is an unsupported superlative | RESEARCH-ONLY | P1 |
| GILL-CONTENT-432 | calling Gill a “mystic” needs definition | CONFIRMED PRODUCTION FRAMING | P1/P2 |
| GILL-CONTENT-433 | the Spurgeon evaluation of Song is not properly sourced | CONFIRMED PRODUCTION CLAIM | P1 |
| GILL-CONTENT-434 | degree awarded “precisely for refuting Whiston” is unsupported causation | CONFIRMED PRODUCTION CLAIM | P1 |
| GILL-CONTENT-435 | early baptism history is overstated as “exclusively confessing believers by immersion” | RESEARCH-ONLY HISTORICAL ERROR | P0/P1 |
| GILL-CONTENT-436 | immersion and believer-only subjects are separate historical questions | METHODOLOGICAL | P1 |
| GILL-CONTENT-437 | Abraham Taylor’s “health objection” needs exact work and quotation | NEEDS EXACT SOURCE | P2 |
| GILL-CONTENT-438 | singing dossiers contradict each other | CONFIRMED RESEARCH CONFLICT | P1 |
| GILL-CONTENT-439 | Gill’s contribution to “hymnographic tradition” is overstated | EDITORIAL | P2 |
| GILL-CONTENT-440 | Egyptian Hallel numbering needs translation-system note | PRECISION | P2 |
| GILL-CONTENT-441 | `dissertationconc00gill` is the Hebrew dissertation, not Good Works | CONFIRMED WRONG-SOURCE LINK | P0 |
| GILL-CONTENT-442 | Level A verification of Good Works therefore did not occur | CONFIRMED FALSE-GREEN | P0 |
| GILL-CONTENT-443 | exact bibliography of Good Works must be rebuilt | NEEDS EXACT SOURCE | P0/P1 |
| GILL-CONTENT-444 | “four biblical supports” may be agent synthesis | NEEDS STRUCTURAL VERIFICATION | P1 |
| GILL-CONTENT-445 | “absolute necessity” needs exact wording | NEEDS QUOTE | P1 |
| GILL-CONTENT-446 | Russian typo changes the doctrinal sentence | CONFIRMED EDITORIAL BUG IN RESEARCH | P2 |
| GILL-CONTENT-447 | commentary on miracles is not automatically a direct response to Woolston | NEEDS AUTHORIAL EVIDENCE | P1 |
| GILL-CONTENT-448 | Cana guests’ “absolute sobriety and holiness” is unsupported | RESEARCH-ONLY OVERCLAIM | P1 |
| GILL-CONTENT-449 | “water carriers” are introduced into John 2 without textual basis | RESEARCH-ONLY TEXTUAL ERROR | P1 |
| GILL-CONTENT-450 | John 11 does not identify all mourners as Pharisees and Sadducees | RESEARCH-ONLY TEXTUAL OVERREACH | P1 |
| GILL-CONTENT-451 | “professional Roman armed detachment” is a harmonized inference | NEEDS QUALIFICATION | P1 |
| GILL-CONTENT-452 | “hundreds of eyewitnesses” imports 1 Corinthians 15 into Matthew 28 | SOURCE-MIXING | P1 |
| GILL-CONTENT-453 | “legally destroys the lie” is rhetorical, not analytical | EDITORIAL | P2 |
| GILL-CONTENT-454 | Witsius was not a Westminster Assembly delegate | CONFIRMED FACTUAL ERROR | P0/P1 |
| GILL-CONTENT-455 | Maccovius and Ames citations do not make Gill’s formulation confessional consensus | HISTORIOGRAPHIC OVERREACH | P1 |
| GILL-CONTENT-456 | Gill did not “refute” the modern distinction as such | WORDING | P1 |
| GILL-CONTENT-457 | Hebrew etymologies of `berit` need modern lexical caution | HISTORICAL PHILOLOGY | P2 |
| GILL-CONTENT-458 | GAP-1 is only partially closed | CONFIRMED STATUS ERROR | P1 |
| GILL-CONTENT-459 | “faith because justified” must be included in the controversy section | CONTENT-BALANCE | P1 |
| GILL-CONTENT-460 | Gill did not participate in the Scottish Marrow controversy | POSITIVE CAVEAT, MUST CONTROL THE WHOLE DOSSIER | P1 |
| GILL-CONTENT-461 | primary quotations accessed through London Lyceum remain secondary transmission | SOURCE-CLASS | P1 |
| GILL-CONTENT-462 | Baxter’s doctrine is presented as settled “new legal ground” | NEEDS ACADEMIC BALANCE | P1 |
| GILL-CONTENT-463 | Stinton and twelve churches claim rests on a partisan source chain | NEEDS PRIMARY MINUTES | P1 |
| GILL-CONTENT-464 | the two justification-work titles and publication histories remain unstable | NEEDS BIBLIOGRAPHIC NORMALIZATION | P0/P1 |
| GILL-CONTENT-465 | corrupted mixed-language text remains in Research | CONFIRMED EDITORIAL BUG | P2 |
| GILL-CONTENT-466 | dossier 04 gives the wrong content for Cause Part IV | CONFIRMED SUPERSEDED ERROR | P0/P1 |
| GILL-CONTENT-467 | dossier 04 places the eternal covenant in Book IV | CONFIRMED BOOK ERROR | P0 |
| GILL-CONTENT-468 | dossier 01 calls Doctrinal Divinity “three books” | CONFIRMED VOLUME/BOOK CONFUSION | P0 |
| GILL-CONTENT-469 | dossier 06 calls Body of Divinity “nine volumes / seven books” | CONFIRMED CORPUS CONFLATION | P0 |
| GILL-CONTENT-470 | Research’s Cause and theology article plans are superseded but not marked | CONFIRMED | P1 |
| GILL-CONTENT-471 | the Marischal degree is causally tied to Whiston without institutional evidence | CONFIRMED PRODUCTION CLAIM | P1 |
| GILL-CONTENT-472 | Spurgeon’s Song evaluation needs primary recovery | CONFIRMED PRODUCTION CLAIM | P1 |
| GILL-CONTENT-473 | “Gill as mystic” should not be a hidden classification | CONFIRMED PRODUCTION FRAMING | P1/P2 |
| GILL-CONTENT-474 | Eastcheap duration is internally expressed as 26 and 27 years | NEEDS DATE ARITHMETIC / SOURCE | P1 |
| GILL-CONTENT-475 | farewell quotation is sourced through `Bunhill Memorials`, not Gill edition | SOURCE HIERARCHY | P1 |
| GILL-CONTENT-476 | “Baptists, Anglicans and Independents united to rent halls” needs names and source | CONFIRMED PRODUCTION CLAIM | P1 |
| GILL-CONTENT-477 | Hervey is called member of Wesley’s Holy Club without source | NEEDS BIOGRAPHICAL CHECK | P1 |
| GILL-CONTENT-478 | Hervey quotation is translated without work/page | CONFIRMED PRODUCTION QUOTE GAP | P1 |
| GILL-CONTENT-479 | Crisp is called a “martyr of grace doctrine” as Gill’s settled view | NEEDS EXACT SOURCE / EDITORIAL | P1 |
| GILL-CONTENT-480 | Part II currently inherits Research’s Ella-centred Whitefield narrative | CONFIRMED PROVENANCE CHAIN | P1 |

---

# 135. Финальный вывод

Серия о Джоне Гилле уже содержит редкий по объёму и качеству материал. Основная проблема не в нехватке сведений, а в том, что сильная первичная работа и апологетическая редактура не разделены технически.

Текущая цепочка слишком часто выглядит так:

```text
primary source
→ secondary transcription
→ agent paraphrase
→ apologetic conclusion
→ duplicated Research dossier
→ Astro prose
→ tooltip / quiz
```

После этого позднее исправление не вытесняет старое утверждение.

Финальная задача проекта поэтому состоит не только в переписывании отдельных абзацев. Нужен единый слой данных, где каждая дата, цитата, интерпретация и иллюстрация имеет:

```text
одного владельца
один canonical wording
один source chain
явную степень уверенности
полный deployment map
историю supersession
```

Настоящий документ сохраняет весь аудит от `GILL-CONTENT-001` до `GILL-CONTENT-480` и должен использоваться как единственный master-input для будущего исправления сайта и Research.
