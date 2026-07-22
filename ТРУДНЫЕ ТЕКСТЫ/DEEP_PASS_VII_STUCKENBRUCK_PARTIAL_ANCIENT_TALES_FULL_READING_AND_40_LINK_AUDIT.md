# Марафон VII: Stuckenbruck 1997, полный сборник *Ancient Tales*, новая критическая редакция 2025/2026 и проход по 40+ академическим страницам

**Дата:** 22 июля 2026 года  
**Статус:** `SOURCE-CORRECTION / PARTIAL-FILE-MAPPED / FULL-COLLECTION-DEEP-READ / 40+ URL AUDIT / NEW-CRITICAL-EDITION-FOUND`  
**Связанный PR:** #5

---

## 1. Главная поправка к предыдущему статусу

Два новых файла подходят, но **по-разному**.

### 1.1. `Ancient Tales of Giants ... (1).pdf`

Это не новая книга и не иное издание, а точный побайтовый дубль уже принятого полного файла:

```text
SHA-256 старого файла:
e681fb764e48856115a747122cab2f9c8746bfb558d46dc9a5f97cb223d81ba2

SHA-256 нового файла:
e681fb764e48856115a747122cab2f9c8746bfb558d46dc9a5f97cb223d81ba2

cmp = IDENTICAL
```

Статус:

```text
RECEIVED-FULL / EXACT-DUPLICATE / NO-NEW-BIBLIOGRAPHIC-ITEM
```

Однако повторная отправка стала основанием не просто зарегистрировать сборник, а провести **углублённое чтение его центральных статей**.

### 1.2. `f603c0c55160e9b66af5facc5bbbc38c.pdf`

Это действительно нужная книга:

> Loren T. Stuckenbruck, *The Book of Giants from Qumran: Texts, Translation, and Commentary*. TSAJ 63. Tübingen: Mohr Siebeck, 1997.

Технический хеш:

```text
SHA-256:
f1f314d83bcde73760bd1d22ccdec50c4e59fd538b84a6db8e69c6e331ff0e61
```

Но файл **не полный**.

Официальный том содержит `xvi + 289` печатных страниц; карточка современного eBook указывает 305 технических страниц. Присланный PDF содержит только 57 технических страниц.

### 1.3. Физическая карта присланного Stuckenbruck

| PDF-страницы | Реальное содержимое |
|---:|---|
| 1–17 | титул, выходные данные, предисловие, оглавление, сокращения |
| 18–27 | начало главы 1, печатные страницы 1–10 |
| 28–54 | индексы, печатные страницы 263–289 |
| 55 | пустая страница |
| 56–57 | издательский каталог серии |

Отсутствуют печатные страницы **11–262**.

Особенно критично, что сам автор называет главным корпусом книги главу 2, печатные страницы **41–224**, где расположены:

- арамейские тексты;
- английские переводы;
- текстологические примечания;
- подробный комментарий;
- разделение вероятных рукописей и спорных атрибуций;
- глоссарий и приложение.

Все эти страницы в присланном PDF отсутствуют.

Исправленный статус:

```text
STUCKENBRUCK 1997
= EXACT BOOK IDENTIFIED
= RECEIVED-PARTIAL
= INTRODUCTION pp. 1–10 + INDICES pp. 263–289
= MAIN BODY pp. 11–262 MISSING
= NOT SUITABLE FOR FINAL LINE-BY-LINE CITATION
```

---

# 2. Почему даже неполный Stuckenbruck полезен

Несмотря на усечённость, сохранившееся начало даёт несколько надёжных методологических контролей.

## 2.1. Это не официальное DJD-издание

Stuckenbruck прямо предупреждает, что его книга не должна смешиваться с официальной публикацией ещё не вышедших тогда материалов в серии *Discoveries in the Judaean Desert*.

Его книга шире по охвату предполагаемых фрагментов, но в ней отсутствуют некоторые элементы официального издания:

- полные пластины;
- размеры каждого фрагмента;
- местами детальная палеография;
- местами полная орфографическая документация.

Следовательно, правильная цепочка для окончательного исследования:

```text
ФОТОГРАФИЯ / ОБЪЕКТ
→ DJD 31 / DJD 36
→ STUCKENBRUCK 1997
→ НОВЫЕ ЧТЕНИЯ
→ СЮЖЕТНАЯ РЕКОНСТРУКЦИЯ
```

## 2.2. Автор различает уровни уверенности

Глава 2 была специально разделена на:

1. рукописи, **вероятно** принадлежавшие Книге Исполинов;
2. материалы, чья принадлежность **сомнительна**.

Это подтверждает ключевой принцип Research:

```text
fragment mentioning Enoch or giants
≠ automatically a Book of Giants witness
```

## 2.3. Старый спор о числе рукописей не закрывается одной формулой

Во введении видно, что Milik, Fitzmyer, Beyer и другие по-разному понимали выражения:

- «третья рукопись из коллекции Starcky»;
- «две группы малых фрагментов»;
- число несомненных и возможных копий.

Поэтому нельзя писать без оговорки: «найдено ровно N рукописей».

Нужно разделять:

```text
CERTAIN / HIGHLY PROBABLE
PROBABLE
POSSIBLE
DISPUTED
REJECTED OR UNDETERMINED
```

---

# 3. Углублённое чтение полного *Ancient Tales of Giants from Qumran and Turfan*

Повторный проход охватил не только введение и статью Goff, но центральный комплекс:

- Joseph L. Angel;
- Amanda M. Davis Bledsoe;
- Ida Fröhlich;
- Matthew Goff;
- Loren Stuckenbruck;
- манихейские разделы Kósa, Morano, Reeves и Wilkens.

## 3.1. 4Q530 2 ii — не цельная физическая колонка

Обозначение `4Q530 2 ii` в литературе часто скрывает сложную реконструкцию. Речь идёт о композиции из нескольких фрагментов:

```text
2 ii + 6 + 7 i + 8 + 9 + 10 + 11 + 12(?)
```

Следовательно, в любой будущей таблице необходимо показывать отдельно:

| Уровень | Что показывать |
|---|---|
| физический объект | конкретный фрагмент и фотографию |
| чтение | реально видимые буквы |
| соединение | физическое или только литературное |
| восстановление | дополненные буквы и слова |
| перевод | зависимость перевода от восстановления |
| рассказ | итоговая сюжетная последовательность |

Нельзя цитировать реконструированную колонку так, будто она целиком сохранилась на одном листе.

## 3.2. Сны Хахии и Охии

Сохранившийся рассказ имеет двойную структуру:

```text
Хахия:
сад / деревья / один ствол с тремя побегами
→ огонь и воды Потопа

Охия:
нисхождение небесного Владыки
→ установление престолов
→ открытие книг
→ письменный приговор
```

После этого исполины боятся и отправляют Махавая к Еноху, «писцу истолкования».

Главное уточнение: содержание истолкования Еноха сохранилось лишь частично. Поэтому формула «Енох подробно объяснил им всё» является сюжетной реконструкцией, а не полным дошедшим текстом.

## 3.3. Книга Исполинов и Даниил

Angel выявляет комплекс параллелей с Дан. 4 и Дан. 5:

- сон сильного и надменного правителя;
- тревога и физическая потеря сна;
- публичный рассказ сна;
- неспособность собственной группы дать истолкование;
- обращение к иудейскому мудрецу;
- объявление суда и унижения;
- дерево и пень;
- «дикий человек»;
- Гильгамеш как побеждённый сверхчеловек.

Но его вывод осторожнее популярной схемы:

```text
DIRECT LITERARY DEPENDENCE
= NOT DEMONSTRATED

SHARED POOL OF ARAMAIC / MESOPOTAMIAN / DANIELIC TRADITIONS
= STRONG
```

То есть Книга Исполинов и Даниил могли работать в близких книжнических кругах и перерабатывать общий резервуар мотивов.

## 3.4. Функция снов — унижение имперской силы

В Дан. 4 царь после суда восстанавливается. В Книге Исполинов наказание выглядит необратимым или, по крайней мере, гораздо более мрачным.

Angel предлагает политико-апокалиптическое чтение:

```text
допотопные исполины
= символический образ насильственных имперских властей

их сон о гибели
= откровение о конце имперской гордыни
```

Это сильная историческая модель, но автор сам предупреждает, что невозможно уверенно привязать текст к одной конкретной сирийской войне или одному царю.

Статус:

```text
ANTI-IMPERIAL READING
= PLAUSIBLE / STRONG CONTEXTUAL MODEL
≠ IDENTIFICATION OF ONE HISTORICAL RULER
```

## 3.5. Bledsoe: три престольных видения выполняют разные функции

Bledsoe сравнивает:

- Дан. 7;
- 1 Енох 14;
- 4Q530.

Она считает, что данных недостаточно, чтобы уверенно построить линейную цепь прямого заимствования.

Различия принципиальны:

| Текст | Место | Провидец | Функция |
|---|---|---|---|
| 1 Енох 14 | небесный храм | праведный Енох | посвящение и откровение |
| Дан. 7 | спорно: небо или земля | праведный Даниил | суд над царствами и утешение святых |
| 4Q530 | Бог нисходит на землю | виновный исполин Охия | обвинительный приговор самому сновидцу |

Главная литературная инновация Книги Исполинов:

> престольное видение дано не праведному провидцу, а виновному существу, которому показывают собственный суд.

## 3.6. Гильгамеш — не просто объект пародии

Сборник подтверждает более сложную картину:

- имя Гильгамеша действительно входит в арамейский рассказ;
- он говорит о своей силе и поражении от небесных противников;
- его можно читать как «дикого человека»;
- связь с месопотамским эпосом реальна;
- но не все детали объясняются одной полемической инверсией.

Правильная формула:

```text
DE-HEROIZATION
+
CREATIVE LITERARY APPROPRIATION
+
ANTI-IMPERIAL RESEMANTIZATION
```

## 3.7. «Молитесь» и возможность покаяния

Вторая табличка Еноха в 4Q203 8 заканчивается императивом «молитесь», после которого идёт большой пустой участок.

Goff предлагает читать это не обязательно как издёвку, а как реальную возможность обращения. В поддержку он привлекает:

- страх некоторых персонажей;
- фрагменты молитвы;
- манихейские версии;
- поздний Мидраш Шемихазы и Азаэля.

Но доказательная граница остаётся жёсткой:

```text
QUMRAN TEXT:
prayer / fear / judgment = attested or partly attested

repentance of a subgroup = possible
forgiveness = not explicitly preserved
survival of repentant giants = not established by the Aramaic fragments alone
```

Поздние манихейские и раввинистические формы могут сохранять старый материал, но не имеют права механически заполнять каждую лакуну Кумрана.

## 3.8. Махавай и крылья

Арамейский текст 4Q530 7 ii содержит чтение, связанное с полётом Махавая; уйгурская версия прямо говорит о его крыльях.

Статус:

```text
MAHAWAY AS FLYING / WINGED
= TEXTUALLY SERIOUS

exact iconographic equation with Pazuzu / Shedu / Lamaštu
= COMPARATIVE HYPOTHESIS
```

Нельзя превращать сравнительное сходство в доказанное тождество персонажей.

---

# 4. Главная новая находка: Iñaki Marro Sánchez, 2025/2026

В ходе дополнительного веб-прохода обнаружена открытая диссертация LMU:

> Iñaki Marro Sánchez, *The Book of Giants: A Critical Edition of the Aramaic Fragments in their Ancient Scribal and Tradition-Historical Context*.

Метаданные:

```text
Institution: Ludwig-Maximilians-Universität München
Referee: Loren T. Stuckenbruck
Oral examination: 13 February 2025
Repository deposit: 20 February 2026
DOI: 10.5282/edoc.36601
PDF: 675 pages
Language: English
Access: OPEN-FULL
```

Официальная карточка LMU называет труд самой современной и полной редакцией фрагментов Книги Исполинов.

## 4.1. Почему это меняет приоритеты

Stuckenbruck 1997 остаётся фундаментальным историческим комментарием. Но для актуального чтения рукописей теперь необходимо начинать с Marro и возвращаться к Stuckenbruck для сравнения истории чтений.

Новая иерархия:

```text
1. PHOTOGRAPHS: IAA / PAM / B-series / SQE
2. OFFICIAL EDITIONS: DJD 31 / DJD 36
3. MARRO 2025/2026: newest comprehensive critical edition
4. STUCKENBRUCK 1997: foundational reconstruction and commentary
5. LATER ARTICLES: Perrin–Machiela, Goff, Angel, Bledsoe, etc.
6. MANICHAEAN / MIDRASHIC RECEPTION
```

## 4.2. Структура новой редакции

Marro даёт отдельные крупные разделы:

| Свидетель | Начальная страница диссертации |
|---|---:|
| 1Q23 | 143 |
| 1Q24 | 175 |
| 2Q26 | 183 |
| 4Q203 | 189 |
| 4Q206 | 225 |
| 4Q530 | 233 |
| 4Q531 | 321 |
| 4Q532 | 458 |
| 4Q533 | 469 |
| 6Q8 | 485 |
| иранские/манихейские фрагменты | 523 |
| Мидраш Шемихазы и Азаэля | 585 |
| выводы | 601 |
| арамейский словарь | 607 |

Это именно тот посвидетельный формат, который планировался для Research.

## 4.3. Метод Marro

Особенно ценен порядок:

```text
отдельные физические фрагменты
→ чтения букв
→ фотографии и каталожные номера
→ соединения
→ реконструированная последовательность
→ перевод
→ комментарий
```

Автор также сообщает об ошибках и путанице в отдельных онлайн-записях IAA и SQE. Эти заявления нужно проверять по каждому объекту, но они подтверждают, что цифровая карточка не заменяет непосредственного контроля фотографии.

## 4.4. Смелые тезисы Marro требуют отдельной проверки

В первом целевом проходе выявлены несколько сильных предложений автора:

1. Махавай как крылатый исполин и сопоставление с месопотамскими демоническими фигурами.
2. `Nephilim` как отрицательный квалификатор, применимый к ангелам, исполинам или людям.
3. Сны как призыв к обращению.
4. Возможность спасения отдельных исполинов.
5. Индивидуальная ответственность каждого исполина.
6. Более тесное использование манихейских текстов для заполнения арамейского рассказа.

Рабочий статус:

```text
MARRO READINGS
= PRIMARY MODERN EDITORIAL PROPOSALS
= MUST BE COMPARED FRAGMENT BY FRAGMENT
≠ AUTOMATIC NEW CONSENSUS
```

Особенно вывод о спасении нельзя перенести в статью без отдельной матрицы:

```text
арамейская буква
→ восстановление
→ перевод
→ манихейская параллель
→ поздний мидраш
→ степень уверенности
```

---

# 5. Проход по 40+ академическим страницам и цифровым объектам

Ниже зафиксирован не список случайных результатов, а карта реально проверенных узлов.

## A. Полные и критические издания

1. LMU — карточка Marro: https://edoc.ub.uni-muenchen.de/36601/
2. LMU — полный PDF Marro: https://edoc.ub.uni-muenchen.de/36601/1/Marro_Inaki.pdf
3. DOI Marro: https://doi.org/10.5282/edoc.36601
4. Mohr Siebeck — Stuckenbruck eBook: https://www.mohrsiebeck.com/en/book/the-book-of-giants-from-qumran-9783161587887/
5. DOI Stuckenbruck: https://doi.org/10.1628/978-3-16-158788-7
6. JTS review Stuckenbruck: https://academic.oup.com/jts/article-abstract/50/2/648/1676465
7. JSS review Stuckenbruck: https://academic.oup.com/jss/article/XLV/1/172/1639756
8. Brill — *A Handbook of the Aramaic Scrolls*: https://brill.com/display/book/9789004513815/9789004513815_webready_content_text.pdf
9. JTS review of Puech, DJD 31: https://academic.oup.com/jts/article/55/2/625/1706247
10. Mohr Siebeck — *The Myth of Rebellious Angels*: https://www.mohrsiebeck.com/en/book/the-myth-of-rebellious-angels-9783161532818/

## B. Официальные изображения рукописей IAA

11. 1Q23: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/1Q23-1?locale=en_US
12. 1Q24: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/1Q24-1?locale=en_US
13. 2Q26: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/2Q26-1?locale=en_US
14. 4Q203: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q203-1?locale=en_US
15. 4Q206: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q206-3
16. 4Q530: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q530-1?locale=en_US
17. 4Q531: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q531-1?locale=en_US
18. 4Q532: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q532-1?locale=en_US
19. 4Q533: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q533-1?locale=en_US
20. 6Q8: https://www.deadseascrolls.org.il/explore-the-archive/manuscript/6Q8-1?locale=en_US

## C. Цифровые текстовые и библиографические корпуса

21. Scripta Qumranica Electronica: https://sqe.deadseascrolls.org.il/
22. Comprehensive Aramaic Lexicon — описание проекта: https://cal.huc.edu/info.html
23. CAL bibliography for 4Q530: https://cal.huc.edu/getbibsigla.php?myauthor=4Q530
24. CAL bibliography for 2QEnGiants: https://cal.huc.edu/getbibsigla.php?myauthor=2QEnGiants
25. Orion Center bibliography: https://orion-bibliography.huji.ac.il/

## D. Реконструкция, Даниил и престольные видения

26. Stuckenbruck, “The Sequencing of Fragments”: https://journals.sagepub.com/doi/pdf/10.1177/095182079700001601
27. Brill DSD 15.3, Stokes: https://brill.com/view/journals/dsd/15/3/dsd.15.issue-3.xml
28. JSTOR DSD 15.3: https://www.jstor.org/stable/i40017260
29. Trotter, throne vision article record: https://www.jstor.org/stable/24672225
30. Angel, “Reading the Book of Giants”: https://doi.org/10.1163/15685179-12341330
31. Angel, article metadata: https://openurl.ebsco.com/contentitem/doi%3A10.1163/15685179-12341330
32. Goff–Stuckenbruck–Morano official book page: https://www.mohrsiebeck.com/en/book/ancient-tales-of-giants-from-qumran-and-turfan-9783161545320/

## E. Гильгамеш, Книга Стражей и литературное присвоение

33. Goff, “Gilgamesh the Giant” DOI: https://doi.org/10.1163/156851709X395740
34. DSD 16.2 issue: https://www.jstor.org/stable/10.2307/i40017263
35. Goff author repository/profile: https://fsu.academia.edu/MatthewGoff
36. Goff, “When Giants Dreamed about the Flood” record: https://librarycatalog.austinseminary.edu/cgi-bin/koha/opac-detail.pl?biblionumber=162575
37. Peeters volume record: https://www.peeters-leuven.be/detail.php?search_key=9789042931282
38. Henning, “The Book of the Giants”: https://www.cambridge.org/core/journals/bulletin-of-the-school-of-oriental-and-african-studies/article/book-of-the-giants/F09AF3F19C427A250B9D562F82640944

## F. История енохического корпуса и рецепции

39. Milik, HTR article: https://www.cambridge.org/core/journals/harvard-theological-review/article/abs/problemes-de-la-litterature-henochique-a-la-lumiere-des-fragments-arameens-de-qumran/6F6DA65BF3AB6C433F1ED4D65F503FF6
40. Greenfield–Stone, “Enochic Pentateuch”: https://www.cambridge.org/core/journals/harvard-theological-review/article/abs/enochic-pentateuch-and-the-date-of-the-similitudes/D4118AF45448314D0BE4EEB863749E14
41. Review of Reeves: https://www.cambridge.org/core/journals/ajs-review/article/john-c-reeves-jewish-lore-in-manichean-cosmogony-studies-in-the-book-of-giants-traditions-monographs-of-the-hebrew-union-college-14-cincinnati-hebrew-union-college-press-1992-xi-260-pp/43EF7B1B8CBE3A95B38956515AF05A1F
42. Brill 2024, fragmentary traditions: https://brill.com/view/journals/dsd/31/2/article-p143_2.xml
43. Full PDF of the 2024 article: https://brill.com/downloadpdf/view/journals/dsd/31/2/article-p143_2.pdf
44. Brill index of BG witnesses in Aramaic priesthood study: https://brill.com/display/book/9789004546165/back-3.xml

**Итого:** проверено более 40 отдельных академических страниц, издательских карточек, репозиторных записей, журнальных страниц и официальных цифровых объектов.

---

# 6. Исправленный реестр источников

## 6.1. Stuckenbruck 1997

Старый статус:

```text
NEED-FULL
```

Новый статус:

```text
RECEIVED-PARTIAL
EXACT TITLE CONFIRMED
57 PDF PAGES
PRINTED pp. 1–10 + 263–289 ONLY
MAIN TEXT MISSING
FULL EBOOK STILL DESIRABLE FOR HISTORICAL CONTROL
```

## 6.2. *Ancient Tales*

Статус остаётся:

```text
RECEIVED-FULL
270 PDF PAGES
DEEP TARGETED READING EXPANDED
```

Новый файл не создаёт дополнительную библиографическую позицию, потому что является точным дублем.

## 6.3. Marro 2025/2026

Добавляется самостоятельная позиция:

```text
OPEN-FULL
675 PDF PAGES
LATEST COMPREHENSIVE CRITICAL EDITION
HIGHEST PRIORITY FOR MANUSCRIPT MATRIX
CAUTION: AUTHOR'S NEW RECONSTRUCTIONS REQUIRE INDEPENDENT CHECK
```

Общее число самостоятельных зарегистрированных источников увеличивается:

```text
46 → 47
```

---

# 7. Что изменяется в исследовательской архитектуре

Ранее планировалось сначала найти полный Stuckenbruck 1997, а затем строить посвидетельную матрицу.

Теперь порядок меняется:

```text
MARRO 2025/2026
→ IAA / SQE object verification
→ DJD 31 / DJD 36
→ STUCKENBRUCK 1997 historical comparison
→ Goff / Angel / Bledsoe literary synthesis
→ Turfan witnesses
→ Midrashic reception
```

Полный Stuckenbruck по-прежнему нужен, но он больше не является единственным блокером современной критической работы.

---

# 8. Следующий рабочий модуль

## 8.1. Посвидетельная матрица

Создать отдельные карточки:

```text
1Q23
1Q24
2Q26
4Q203
4Q206 2–3
4Q530
4Q531
4Q532
4Q533
6Q8
```

Для каждого:

| Поле | Содержание |
|---|---|
| физический объект | пещера, материал, рука, период |
| фотографии | PAM / B / IAA / SQE |
| границы | отдельные фрагменты |
| старое чтение | Milik / Baillet / Puech / Stuckenbruck |
| новое чтение | Marro и позднейшие статьи |
| соединение | физическое / вероятное / литературное |
| перевод | буквальный и восстановленный |
| сюжетная функция | только после текстового контроля |
| уверенность | high / medium / low / speculative |

## 8.2. Отдельная матрица спасения исполинов

```text
4Q203 8 — «молитесь»
4Q203 9 — возможная молитва
4Q203 13 — поклон / падение ниц
4Q530 — страх, сны и поиск истолкования
KawI — «не умрут»
Mainz 344 — покаяние и просьба о прощении
U 222 — поклонение Богу
M 813/I — смерть некоторых исполинов
Midrash — поздняя трансформация
```

Главный вопрос:

> Что физически читается в арамейском тексте, а что появляется только в манихейской или средневековой рецепции?

---

# 9. Итог марафона VII

```text
Ancient Tales duplicate recognized
Stuckenbruck exact title recognized
Stuckenbruck file proven incomplete
missing core pp. 11–262 mapped
central Ancient Tales essays deeply reread
40+ academic URLs audited
675-page open Marro critical edition discovered
source registry raised to 47
research sequence corrected
no automatic merge performed
```
