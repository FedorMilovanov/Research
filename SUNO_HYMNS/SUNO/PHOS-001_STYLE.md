# PHOS-001 — стили

**«Свет Отрадный»** — Φῶς ἱλαρόν, древний гимн вечерни, автор неизвестен.
*Греческий текст — принятый литургический; русский — `PHOS-001-RU v0.5`; название «Свет Отрадный» утверждено владельцем 2026-10-26.*

**Состояние:** пять направлений написаны в этом проходе, ни одно не отправлено в SUNO и ни одно не выбрано владельцем. `STYLE-PHOS-001-A` стоит в первичном слоте только потому, что реестр обязан нести один `promptText`, а не потому, что он лучше.

Только стиль; текста здесь нет. Текст: [`PHOS-001_LYRICS.md`](PHOS-001_LYRICS.md) · сценический: [`PHOS-001_LYRICS_SUNO.md`](PHOS-001_LYRICS_SUNO.md).

У всех пяти один пол: **строго силлабически**, один слог на ноту, без мелизмов и растянутых гласных; **повторы только те, что прописаны в раскладке** `PHOS-001-ARR-R1` — припев из четвёртой строки после второй и третьей строфы и реприза шестой строки в конце; новых слов и добавленных строк нет; ясный, разборчивый ведущий голос, без хрипа, шёпота и нарочито низкого баса; короткое вступление и короткое заключение, без длинных инструментальных проигрышей. Продолжительность при R1 — порядка двух с половиной минут; запасная раскладка R2 (весь гимн дважды) не длиннее трёх.

**Почему форма сквозная, а не строфическая.** У греческого текста нет ни метра, ни рифмы; строки русского перевода — от четырнадцати до двадцати слогов. Строфическая мелодия потребовала бы выравнивания, то есть правки слов. Поэтому все пять промптов просят through-composed: фраза идёт за словами.

---

## A. Греческий певец и исон — `STYLE-PHOS-001-A` · первичный слот

```
ancient Greek Orthodox lamp-lighting hymn, through-composed, a cappella, one male cantor singing a clear modal melody in a Byzantine-flavoured mode on E, a male choir holding a soft ison drone on the tonic beneath him, the drone entering only after the first two lines, strictly syllabic declamation, one syllable per note, no melisma, no vocal runs, no vibrato, natural diction, narrow range, a firm slow pulse rather than free drifting rubato, short two-bar breath of silence as the introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the closing line reprised at the end, no other repeats and no newly written words, then a short held final chord and silence, large but clean stone-church acoustic with an intelligible forward cantor, no percussion, no organ, no strings, no synthesizers
```

**Исключить:** мелизмы, распевы, вибрато, шёпот, хрип, слишком низкий бас, ударные, орган, струнные, синтезаторы, длинные проигрыши, повторы сверх припева и репризы.

**Зачем:** это ровно та среда, в которой гимн живёт полторы тысячи лет; исон даёт «опору», на которой триадологическая строка звучит как удар.

**Риск:** свободный ритм — уже случавшаяся здесь авария (медленно, тягуче, полушёпотом). Отсюда «firm slow pulse» в промпте, а не rubato; если тейк поплыл, лечится темпом и вступлением, а не сокращением текста.

## B. Унисонная мужская скола в староримском духе — `STYLE-PHOS-001-B`

```
early Latin-rite chant, through-composed, a cappella, unison male schola of six voices, modal melody in the Dorian mode on D, no harmony except a bare octave doubling at the final cadence, very even syllabic declamation, one syllable per note, no melisma, no vibrato, crisp Latin-school consonants and clear Russian diction, a single low bell struck once before the singing and once at the end, short one-phrase introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the closing line reprised at the end, no other repeats and no newly written words, dryish stone acoustic, moderate and steady tempo, no percussion kit, no organ, no strings, no synthesizers
```

**Исключить:** многоголосие, мелизмы, вибрато, ударные, орган, струнные, синтезаторы, повторы сверх припева и репризы, длинные проигрыши.

**Зачем:** западная ветвь того же гимна — латинское *Lumen Hilare*; унисон без гармонии звучит старше любой полифонии и не спорит с текстом.

**Риск:** унисон при долгом звучании монотонен; держится тем, что вступление и колокол дают две опорные точки, а темп не опускается ниже разговорного.

## C. Знаменный распев, низкий мужской хор — `STYLE-PHOS-001-C`

```
Russian Znamenny chant style, through-composed, a cappella male choir of eight low voices, monophonic melody with a soft under-voice on the final phrase, very slow and steady pulse, strictly syllabic, one syllable per note, no melisma, no vibrato, deep but not growling basses, clear intelligible diction, a long quiet breath of silence as the introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the closing line reprised at the end, no other repeats and no newly written words, a single held final chord then silence, very large cathedral acoustic, no percussion, no organ, no strings, no synthesizers
```

**Исключить:** мелизмы, распевы, вибрато, рычащий бас, ударные, орган, струнные, синтезаторы, повторы сверх припева и репризы, длинные проигрыши.

**Зачем:** русская традиция поёт этот гимн как «Свете тихий»; знаменный распев — её собственный древний язык, и он честно отделён от греческого исона.

**Риск:** самый большой соблазн скатиться в тягучую низкую декламацию, которую проект уже получал. Спасает «steady pulse» и требование разборчивости; проверять на слух, а не на глаз.

## D. Камерный тенор-баритон, виолончель и орган — `STYLE-PHOS-001-D`

```
restrained dark chamber sacred song, through-composed, 3/4, about 72 bpm, minor mode on A, one close-miked male tenor-baritone with natural diction and no vibrato, gut-string cello pedal tones, arco contrabass on the bass line, a small chamber organ with a stopped 8-foot flute, a second voice joining only on the last two lines, strictly syllabic, one syllable per note, no melisma, short four-bar instrumental introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the closing line reprised at the end, no other repeats and no newly written words, quiet dynamics, close natural room reverb, no percussion, no drums, no electric instruments, no synthesizers
```

**Исключить:** ударные, электробас, синтезаторы, кинематографические струнные нарастания, белтинг, шёпот, хрип, мелизмы, повторы сверх припева и репризы, длинные проигрыши.

**Зачем:** известное предпочтение владельца — сдержанная тёмная акустика; здесь оно применено к самому короткому тексту в проекте.

**Риск:** камерный состав при шести строках даёт самую короткую вещь из пяти; если она выходит короче полутора минут, это не повод добавлять строки — это повод не гнать темп.

## E. Полифония четырёх голосов — `STYLE-PHOS-001-E`

```
Renaissance sacred polyphony, through-composed, a cappella four-part male choir, imitative entries one line at a time, modal harmony in the Mixolydian mode on G, strictly syllabic, one syllable per note, no melisma, no vocal runs, no vibrato, even and transparent texture, words always intelligible, short one-phrase choral introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the closing line reprised at the end, no other repeats and no newly written words, a bare open fifth on the final chord, dry-ish chapel acoustic, no percussion, no organ, no strings, no synthesizers
```

**Исключить:** мелизмы, распевы, вибрато, ударные, орган, струнные, синтезаторы, повторы сверх припева и репризы, длинные проигрыши, густую педальную гармонию.

**Зачем:** сильнейший контраст к A и C: тот же текст как многоголосная мотетная ткань, где каждая строка вступает по очереди.

**Риск:** полифония и разборчивость враждуют; при шести строках это главная опасность. Если слова плывут, направление не спасается — оно меняется на A.

---

## Сравнение

| | A | B | C | D | E |
|---|---|---|---|---|---|
| Состав | певец + исон | унисонная скола | низкий мужской хор | тенор-баритон, виолончель, контрабас, орган | мужской хор, 4 голоса |
| Лад | византийский на E | дорийский на D | знаменный | минор на A | миксолидийский на G |
| Темп | медленный, ровный | умеренный, ровный | очень медленный | 72, 3/4 | ровный, прозрачный |
| Аккомпанемент | нет | колокол | нет | виолончель, контрабас, орган | нет |
| Риск разборчивости | низкий | низкий | средний | низкий | высокий |
| Характер | греческий, древний | латинский, аскетичный | русский, соборный | камерный, тёмный | ренессансный, прозрачный |

## Что решает владелец

Одно из пяти — и только тогда появляется тейк. Выбранный стиль вместе с дословным промптом фиксируется в `PROMPT_AND_VERSION_REGISTER.md`; до этого все пять остаются `AUTHORED_NOT_YET_SUBMITTED`.
