«Свет Отрадный» — автор неизвестен

# PHOS-001 — карточка выдачи для SUNO

**Что это:** всё, что нужно, чтобы получить тейк. Ниже пять направлений. В каждом — **два блока**: первый вставляется в поле **Style**, второй в поле **Lyrics**. Больше ничего копировать не надо.

**Как работать (по правилам канала):**

1. Выберите букву — A, B, C, D или E. Они специально разные: греческий певец с исоном, латинская скола, знаменный распев, камера, ренессансная полифония.
2. Скопируйте **оба** блока выбранной буквы: стиль — в Style, текст — в Lyrics.
3. Баттл — одна генерация, два варианта. Раунд — три баттла. Из шести вариантов выбирается один тейк.
4. Если припев покажется навязчивым, есть запасная раскладка без припева — весь гимн дважды подряд; она описана в [`PHOS-001_LYRICS_SUNO.md`](PHOS-001_LYRICS_SUNO.md) § 3.
5. Пришлите мне: букву, дословный промпт, которым генерировали (если правили — присланный текст), длительность, файл. Я запишу это в `PROMPT_AND_VERSION_REGISTER.md` — без этого через месяц никто не вспомнит, чем сделан тейк.

**Ревизия текста:** `PHOS-001-RU v0.4` — звательные «Иисусе Христе» / «Сыне Божий» заменены на именительный «Иисус Христос» / «Сын Божий»: без церковнославянской стилистики, ровный регистр.

**Что важно не менять в тексте.** Текст длиннее, чем был: к шести строкам добавлены **припев и реприза**, сделанные только из слов самого гимна. Припев — это четвёртая строка («воспеваем Отца, Сына и Святого Духа, Бога»), повторённая дословно дважды; в конце возвращается первая строка. Новых слов нет ни одного. Всего поётся девять строк вместо шести — примерно две с половиной минуты.

Если SUNO начнёт повторять строки сверх этого — например зациклит «Бога» — тейк бракуется: повтор в гимне один, и он уже написан.

**Метаданные для файлов:** название `Свет Отрадный`, автор `автор неизвестен` (или `Anonymous`), альбом `Господь Бог — Сила Моя`, жанр `Христианский гимн`.

Подробности и обоснования: стили — [`PHOS-001_STYLE.md`](PHOS-001_STYLE.md), текст — [`PHOS-001_LYRICS.md`](PHOS-001_LYRICS.md), решения перевода — [`../RESEARCH/DOSSIER_PHOS-001_TRANSLATION_DECISIONS.md`](../RESEARCH/DOSSIER_PHOS-001_TRANSLATION_DECISIONS.md).

---

## A. Греческий певец и исон — `STYLE-PHOS-001-A` · основной слот

Самый близкий к тому, как этот гимн поют полторы тысячи лет: один голос ведёт, хор держит низкий исон. Разборчивость высокая, риск провала низкий.

**Style:**

```
ancient Greek Orthodox lamp-lighting hymn, through-composed, a cappella, one male cantor singing a clear modal melody in a Byzantine-flavoured mode on E, a male choir holding a soft ison drone on the tonic beneath him, the drone entering only after the first two lines, strictly syllabic declamation, one syllable per note, no melisma, no vocal runs, no vibrato, natural diction, narrow range, a firm slow pulse rather than free drifting rubato, short two-bar breath of silence as the introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the opening line reprised at the end, no other repeats and no newly written words, then a short held final chord and silence, large but clean stone-church acoustic with an intelligible forward cantor, no percussion, no organ, no strings, no synthesizers
```

**Lyrics:**

```
[Intro]

[Verse 1]
Свет отрадный святой славы бессме́ртного Отца,
небесного, святого, блаженного, Иисус Христос,

[Verse 2]
придя к закату солнца, увидев свет вечерний,
воспева́ем Отца, Сына и Святого Духа, Бога.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Verse 3]
Достоин Ты во все времена быть воспетым голосами благи́ми,
Сын Божий, даю́щий жизнь: потому мир Тебя славит.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Outro]
Свет отрадный святой славы бессме́ртного Отца,
```

---

## B. Унисонная мужская скола — `STYLE-PHOS-001-B`

Западная ветвь того же гимна (лат. *Lumen Hilare*): унисон без гармонии, один колокол в начале и в конце. Звучит старше любой полифонии.

**Style:**

```
early Latin-rite chant, through-composed, a cappella, unison male schola of six voices, modal melody in the Dorian mode on D, no harmony except a bare octave doubling at the final cadence, very even syllabic declamation, one syllable per note, no melisma, no vibrato, crisp consonants and clear Russian diction, a single low bell struck once before the singing and once at the end, short one-phrase introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the opening line reprised at the end, no other repeats and no newly written words, dryish stone acoustic, moderate and steady tempo, no percussion kit, no organ, no strings, no synthesizers
```

**Lyrics:**

```
[Intro]

[Verse 1]
Свет отрадный святой славы бессме́ртного Отца,
небесного, святого, блаженного, Иисус Христос,

[Verse 2]
придя к закату солнца, увидев свет вечерний,
воспева́ем Отца, Сына и Святого Духа, Бога.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Verse 3]
Достоин Ты во все времена быть воспетым голосами благи́ми,
Сын Божий, даю́щий жизнь: потому мир Тебя славит.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Outro]
Свет отрадный святой славы бессме́ртного Отца,
```

---

## C. Знаменный распев, низкий мужской хор — `STYLE-PHOS-001-C`

Русский древний язык — на русский же текст. Самый соборный из пяти и самый опасный: здесь легче всего получить тягучую низкую декламацию, которую проект уже получал.

**Style:**

```
Russian Znamenny chant style, through-composed, a cappella male choir of eight low voices, monophonic melody with a soft under-voice on the final phrase, very slow and steady pulse, strictly syllabic, one syllable per note, no melisma, no vibrato, deep but not growling basses, clear intelligible diction, a long quiet breath of silence as the introduction, the whole six-line Russian text sung once with no repeats and no chorus, a single held final chord then silence, very large cathedral acoustic, no percussion, no organ, no strings, no synthesizers
```

**Lyrics:**

```
[Intro]

[Verse 1]
Свет отрадный святой славы бессме́ртного Отца,
небесного, святого, блаженного, Иисус Христос,

[Verse 2]
придя к закату солнца, увидев свет вечерний,
воспева́ем Отца, Сына и Святого Духа, Бога.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Verse 3]
Достоин Ты во все времена быть воспетым голосами благи́ми,
Сын Божий, даю́щий жизнь: потому мир Тебя славит.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Outro]
Свет отрадный святой славы бессме́ртного Отца,
```

---

## D. Камерный тенор-баритон — `STYLE-PHOS-001-D`

Сдержанная тёмная акустика, как вы любите: виолончель, контрабас, малый орган, один голос вблизи. Самый короткий и самый «домашний» из пяти.

**Style:**

```
restrained dark chamber sacred song, through-composed, 3/4, about 72 bpm, minor mode on A, one close-miked male tenor-baritone with natural diction and no vibrato, gut-string cello pedal tones, arco contrabass on the bass line, a small chamber organ with a stopped 8-foot flute, a second voice joining only on the last two lines, strictly syllabic, one syllable per note, no melisma, short four-bar instrumental introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the opening line reprised at the end, no other repeats and no newly written words, quiet dynamics, close natural room reverb, no percussion, no drums, no electric instruments, no synthesizers
```

**Lyrics:**

```
[Intro]

[Verse 1]
Свет отрадный святой славы бессме́ртного Отца,
небесного, святого, блаженного, Иисус Христос,

[Verse 2]
придя к закату солнца, увидев свет вечерний,
воспева́ем Отца, Сына и Святого Духа, Бога.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Verse 3]
Достоин Ты во все времена быть воспетым голосами благи́ми,
Сын Божий, даю́щий жизнь: потому мир Тебя славит.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Outro]
Свет отрадный святой славы бессме́ртного Отца,
```

---

## E. Ренессансная полифония — `STYLE-PHOS-001-E`

Тот же текст как мотет: строки вступают по очереди, четыре голоса. Сильнейший контраст к A и C, но и самый большой риск для разборчивости.

**Style:**

```
Renaissance sacred polyphony, through-composed, a cappella four-part male choir, imitative entries one line at a time, modal harmony in the Mixolydian mode on G, strictly syllabic, one syllable per note, no melisma, no vocal runs, no vibrato, even and transparent texture, words always intelligible, short one-phrase choral introduction, all six lines sung in order, the Trinitarian line repeated verbatim as the refrain after the second and the third verse, the opening line reprised at the end, no other repeats and no newly written words, a bare open fifth on the final chord, dry-ish chapel acoustic, no percussion, no organ, no strings, no synthesizers
```

**Lyrics:**

```
[Intro]

[Verse 1]
Свет отрадный святой славы бессме́ртного Отца,
небесного, святого, блаженного, Иисус Христос,

[Verse 2]
придя к закату солнца, увидев свет вечерний,
воспева́ем Отца, Сына и Святого Духа, Бога.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Verse 3]
Достоин Ты во все времена быть воспетым голосами благи́ми,
Сын Божий, даю́щий жизнь: потому мир Тебя славит.

[Refrain]
воспева́ем Отца, Сына и Святого Духа, Бога.

[Outro]
Свет отрадный святой славы бессме́ртного Отца,
```

---

## Что прислать обратно

| Поле | Обязательно |
|---|---|
| Буква направления (A–E) | да |
| Дословный текст промпта, который ушёл в Style | да — если правили, пришлите правленый |
| Файл или ссылка на тейк | да |
| Длительность | желательно |
| Что услышали не так: строка повторена, «Иисусе» спето в три слога, «благими» с ударением на «бла» и т. п. | желательно |

Правило проекта: промпт, которого нет в реестре дословно, считается неснятым (`NOT_CAPTURED`). Это не формальность — три прежних гимна так и остались без записи того, чем они сделаны.
