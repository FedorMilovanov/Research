# Чарнок — сводный леджер уже используемого в Research материала

**Объект:** Stephen Charnock, B.D. (1628–1680)
**Том:** 10 отдела «Стивен Чарнок»
**Дата:** 2026-10-25
**Задача:** учесть и связать всё, что Research уже использует от Чарнока, с каноническим
пятитомником Nichol 1864–66, не переписывая authority чужих корпусов.

---

## 1. Проверяемый вопрос

Какие именно Charnock-утверждения Research уже использует в публикуемых корпусах, к каким
дискурсам они относятся, и каков их статус верификации?

**Ответ:** корпуса используют Чарнока в **трёх** функциональных ролях — practical atheism
diagnosis, regeneration anatomy, restraint/reformation distinction. Все они опираются на
**цифровые** редакции (CCEL, Digital Puritan, Monergism) без постраничной сверки с печатным
Nichol 1864. Ниже — полная карта с оценкой.

---

## 2. Функциональные роли Чарнока в Research

| Роль | Где используется | Дискурс (Nichol) | Статус |
|---|---|---|---|
| **Practical atheism** — язык для скрытой безбожности сердца | `СЕРИЯ СЕРДЦЕ/19`, `25`, `27`, `03`, `04`, `07`, `12`, `13` | vol. 1, *A Discourse on Practical Atheism* (Пс. 14:1) | `A2` (Monergism HTML), `locatorState = digital` |
| **Regeneration anatomy** — two states, no middle, grace predominating | `СЕРИЯ СЕРДЦЕ/43`, `62`, `63`, `65`; `TEEN_DOUBLE_LIFE/52` | vol. 3, *Necessity of Regeneration*, *Nature of Regeneration*, *Efficient of Regeneration*, *Word, Instrument of Regeneration* | `A2` (CCEL, Digital Puritan vol. 3), `locatorState = digital` |
| **Restraint vs. reformation** — fear может удерживать действие, не меняя желание | `TEEN_DOUBLE_LIFE/52`, `44`, `90`, `156` | vol. 3, regeneration discourses | `A2`, `locatorState = digital` |

---

## 3. Quote-anchors, уже зафиксированные в Research

### 3.1. `CHARN_PRACT_ATHEISM_001` — «Men may have atheistical hearts without atheistical heads.»

- **Где:** `СЕРИЯ СЕРДЦЕ/25_QUOTE_BANK_EXACT_ANCHORS_AND_CANDIDATES.md` §1 и §139;
  `СЕРИЯ СЕРДЦЕ/27_WEB_VERIFICATION_SOURCES_AND_LEDGER.md` §4 (статус **A**).
- **Указанный источник:** *Discourse on Practical Atheism*, Monergism HTML, **lines 82–84** в web
  extraction, opening Psalm 14:1 exposition.
- **Печатный локатор первого издания:** *Several discourses upon the existence and attributes of
  God* (Lond., 1682), **стр. 47** — афоризм стоит на стр. 47 в exposиции Пс. 14:1, внутри
  «Doct. 2. PRACTICAL Atheism is natural to Man in his depraved state». Установлено 2026-10-25
  прямым чтением `A32723.0001.001`, узел `1:5`.
- **Функция:** показать разрыв между правильной идеей о Боге и практическим отношением сердца.
- **Предохранитель корпуса:** «не использовать это как ярлык для всякой слабости… Устойчивый
  practical atheism — это не единичное согрешение с покаянием, а практическая схема жизни».
  **Усилен 2026-10-25:** в первом издании афоризм непосредственно развивается: «Their reasons may
  defend the Notion of a Deity, while their hearts are empty of affection to the Deity: Jobs
  Children may curse God in their hearts, tho not with their lips.»
- **`evidenceClass`:** `A1` (текст первого издания 1682, прочитан в EEBO-TCP; ранее `A2`).
- **`locatorState`:** **`checked`** для первого издания 1682 (стр. 47). Для Nichol 1864 —
  **`unverified`**: «lines 82–84 in web extraction» печатным локатором не является.
- **HOLD:** `LOCATOR_HOLD` в отношении Nichol 1864. `RIGHTS_HOLD` для `A32723` (каталог TCP:
  Restricted; страница Michigan: CC0 — расхождение не разрешено).
- **Требуемое действие:** найти страницу в Nichol 1864 vol. 1 и сверить формулировку; при
  цитировании по первому изданию восстановить капитализацию («Atheistical … Atheistical») либо
  оговорить нормализацию.

**Добавление 2026-10-25 (том 14, элегия 1680, сноска d).** Элегия *An Elegy on the death of the
truly reverend, learned and pious, Mr. Stephen Charnock, July 27, 1680* (EEBO-TCP
`A39134.0001.001`, CC0 1.0) содержит сноску **«Upon Psal. 14.1»**, привязанную к строкам «On what
firm grounds did he God's Being lay, / And leave the Atheist nothing more to say». То есть
**sermon на Пс. 14:1 — тот самый текст, на котором построен *Discourse on Practical Atheism* —
аттрибуцирован Чарноку contemporaneous печатным источником 1680 года**. Это поднимает обоснование
`CHARN_PRACT_ATHEISM_001` с уровня `A2` (цифровая копия без аппарата) до уровня **`A1`-обоснованной
цитаты**: текст sermon'а подтверждён contemporaneous аттрибуцией, независимой от репринта 1844 и от
Monergism. `evidenceClass` цитаты остаётся `A2` (текст взят из цифровой копии), но
`locatorState` получает **contemporaneous якорь**: «sermon на Пс. 14:1, аттрибуцирован в 1680».
Требуемое действие остаётся: привести к странице Nichol 1864 vol. 1.

**Добавление 2026-10-25 (том 03 §3D): печатный локатор получен — в первом издании.** Оглавление
фолианта 1682 (`A32723.0001.001`, узел `1:3`) даёт: «Page 1. & 47. THE Existence of God, and
Practical Atheism; **from Psal. 14.1**.» То есть дискурс, являющийся источником
`CHARN_PRACT_ATHEISM_001`, напечатан в **первом издании** на страницах **1 и 47**.

**Добавление 2026-10-25 (том 10 §3.1): точная страница цитаты установлена — стр. 47.** Дискурс
«A DISCOURSE UPON PRACTICAL ATHEISM» (узел `1:5`) открывается на стр. 47 заголовком, текстом
Пс. 14:1 и «Doct. 2.», и афоризм стоит **на самой стр. 47**, в exposиции текста (не в «use»):

> **Page 47.** A DISCOURSE UPON PRACTICAL ATHEISM. > Psalm 14.1. Doct. 2. PRACTICAL Atheism is
> natural to Man in his depraved state, and very frequent in the hearts and lives of Men. The Fool
> hath said in his heart there is no God. He regards him as little as if he had no being… He could
> not rase out the Notion of a Deity in his mind, but he neglected the fixing the sence of God in
> his heart, and made it too much his business to de∣face and blot out those Characters of God in
> his Soul, which had been left under the ruines of original nature.
>
> **Men may have Atheistical hearts without Atheistical heads.** Their reasons may defend the Notion
> of a Deity, while their hearts are empty of affection to the Deity: Jobs Children may curse God in
> their hearts, tho not with their lips.

**Цитируемый локатор:** *Several discourses upon the existence and attributes of God*, London:
Printed for D. Newman, T. Cockerill, Benj. Griffin, T. Simmons, and Benj. Alsop, **1682**, **p. 47**
(EEBO-TCP `A32723.0001.001`, узел `1:5`; Wing **C3711**).

**Текстологическая оговорка.** В первом издании оба слова даны с заглавной: «**A**theistical hearts
without **A**theistical heads». Формулировка, зафиксированная в Research
(«atheistical hearts without atheistical heads»), — **нормализованная по капитализации**. При
цитировании по первому изданию капитализации следует восстановить либо оговорить нормализацию.

**Контекст, который должен сопровождать цитату.** Афоризм стоит внутри exposиции Пс. 14:1 и
непосредственно развивается двумя предложениями: «Their reasons may defend the Notion of a Deity,
while their hearts are empty of affection to the Deity: Jobs Children may curse God in their
hearts, tho not with their lips.» Это **усиливает** предохранитель корпуса: Чарнок говорит не о
случайной слабости, а о **естественном для падшего состояния практическом атеизме**, при котором
разум защищает понятие о Божестве, а сердце пусто к Нему.

**Статус после этой проверки.** `evidenceClass` цитаты — `A1` (текст первого издания 1682, прочитан
в EEBO-TCP); `locatorState` — **`checked`** (стр. 47 первого издания). `LOCATOR_HOLD` в отношении
Nichol 1864 **сохраняется**: цифровая копия, из которой цитата попала в Research, — репринт XIX
века, и страница Nichol до сих пор неизвестна. `RIGHTS_HOLD` для `A32723` сохраняется (каталог TCP:
Restricted; страница Michigan: CC0 — расхождение не разрешено).

### 3.2. Two-state diagnostic — prevalency of corrupt habit vs. predominancy of gracious habit

- **Где:** `СЕРИЯ СЕРДЦЕ/43_V67_MANTON_CHARNOCK_VINCENT_CONFESSIONAL_DEEPENING.md` §5.
- **Формулировка корпуса:** «the state of nature consists in the prevalency of the corrupt habit,
  while the state of grace consists in the predominancy of the gracious habit, which spreads over the
  whole soul while striving with the powerful opposite that still partly resides there».
- **Источник корпуса:** Digital Puritan, *The Complete Works of Stephen Charnock* (vol. 3).txt.html.
- **Противопоставление корпуса:** Boston's four states включают creation и eternity; Charnock's
  two-state diagnostic действует внутри истории после падения.
- **`evidenceClass`:** `A2`.
- **`locatorState`:** **`unverified`** — нет страницы Nichol vol. 3.
- **HOLD:** `LOCATOR_HOLD`.
- **Дополнительное требование:** необходимо установить, в каком из четырёх regeneration discourses
  vol. 3 находится эта формулировка. По оглавлению — вероятно, *Nature of Regeneration* (2 Кор. 5:17)
  или *Efficient of Regeneration* (Ин. 1:13), но Nichol vol. 3 pagination не сверена.

### 3.3. «Regeneration before conversion»

- **Где:** `СЕРИЯ СЕРДЦЕ/43` §5, таблица §300.
- **Функция:** отделить regenerate status от conversion как act.
- **Статус:** paraphrase, не цитата. `A2`. `LOCATOR_HOLD`.

### 3.4. «Custom can deepen nature's disorder»

- **Где:** `СЕРИЯ СЕРДЦЕ/43` §5.
- **Формулировка корпуса:** «he argues that custom can deepen nature's disorder; a person does not
  cure sinful habit by mere self-accustoming, because the heart itself needs overruling grace».
- **Функция:** связка с concern пользователя о patterns, childhood formation, deeply rooted attachments.
- **Статус:** paraphrase. `A2`. `LOCATOR_HOLD`.

### 3.5. Regeneration / restraint cluster (`TEEN_DOUBLE_LIFE/52`)

| Утверждение | Источник корпуса | Статус |
|---|---|---|
| Regeneration — real inward change, не новая религиозная внешность | CCEL `nec_regen.ii.html` | `A2`, `locatorState = digital` |
| Outward reformation insufficient but «of excellent use» | CCEL `nec_regen.ii.html` | `A2` |
| Fear может restrain action without changing desire | CCEL `nec_regen.ii.html` | `A2` |
| Convictions ≠ regeneration | CCEL `nec_regen.ii.html`, `nat_regen.i.html` | `A2` |
| Christian parents ищут regeneration детей, не merely worldly success | CCEL `nec_regen.ii.html` | `A2` |
| Inability/perversity не отменяет справедливость заповеди | CCEL `efficient_regeneration.ii.html` | `A2` |
| «Rhetorical application, not Charnock quote» — явная пометка корпуса | — | **образцовая практика** |

**Отметка отдела:** `TEEN_DOUBLE_LIFE/52` line 86 содержит явную пометку «Rhetorical application,
not Charnock quote». Это ровно та дисциплина, которую требует `AGENT_RULES.md`, и она должна
служить образцом для всех будущих Charnock quote-card в отделе.

---

## 4. Карта цифровых источников, используемых корпусами

| Источник | Что даёт | evidenceClass | locatorState |
|---|---|---|---|
| CCEL `ccel.org/c/charnock/nec_regen` + `.ii.html` + PDF | *Necessity of Regeneration* | `A2` | digital |
| CCEL `ccel.org/ccel/charnock/nat_regen/nat_regen.i.html` | *Nature of Regeneration* | `A2` | digital |
| CCEL `ccel.org/ccel/charnock/efficient_regeneration/efficient_regeneration.{ii,iii}.html` | *Efficient of Regeneration* | `A2` | digital |
| CCEL `ccel.org/ccel/charnock/instr_regen/instr_regen.html` | *Word, Instrument of Regeneration* | `A2` | digital |
| CCEL `ccel.org/ccel/charnock/reconcil.html` | *God the Author of Reconciliation* | `A2` | digital |
| CCEL `ccel.org/ccel/charnock/cleansing.html` | *Cleansing Virtue of Christ's Blood* | `A2` | digital |
| Digital Puritan vol. 1–5 (txt.html / epub / pdf) | Полные тома | `A2` | digital |
| Digital Puritan vol. 1 Ind Titles `[SC] A Discourse Upon Spiritual Worship.pdf` | *Spiritual Worship* | `A2` | digital |
| Digital Puritan vol. 1 Ind Titles `[SC] Practical Atheism.pdf` | *Practical Atheism* | `A2` | digital |
| Monergism `A Treatise on Divine Providence` (pdf/epub) | *Providence* + epistol Adams & Veal | `A2` | digital |
| grace-ebooks `SC-Discourses-On-The-Existence-and-Attributes-of-God-Vol-1.pdf` | *Attributes* vol. 1 | `A2` | digital |

**Все эти источники — `A2`.** `СЕРИЯ СЕРДЦЕ/27` §4 явно ставит Charnock в класс **A** со
статусом «доступен и проверяем», но оговаривает: «для точной цитаты проверять контекст».
Отдел «БИОГРАФИИ/Стивен Чарнок» **подтверждает** эту классификацию и добавляет требование:
для quote-safe необходима постраничная сверка с Nichol 1864.

---

## 5. Что отдел добавляет к уже используемому

| Было в Research | Стало после отдела |
|---|---|
| Charnock = «пуританский пресвитерианин», 1628–1680 | Уточнено: эдикторы называют его «a true Son of the Church of England» (том 08) |
| Все цитаты — `A2`, `locatorState = digital` | Цитаты из funeral sermon Johnson 1680 и эпистола Adams & Veal 1684 — `A1`, `locatorState = checked` (томы 08, 09) |
| Портрет Чарнока — «характеристика Джонсона» | Портрет — patristic compilation, не свидетельство Johnson (том 09 §3) |
| proctor 1652 или 1654 — не решено | **1654**, решено документально (том 08) |
| *Attributes* «1681-2» или «1682» — не решено | Обе части существуют; диапазон = две даты титула (том 03) |
| Смерть 27 июля 1680 | 27 июля, но зафиксирован `CONFLICT-10`. За 27 июля: Wood 1691, Calamy 1727, DNB 1887, Symington, McCosh, ODNB, элегия 1680 (не получена) и *New Poems* 1680 (EEBO-TCP `A52960.0001.001`, **получен полностью**) — **8 свидетелей**. За 28 июля: broadside *The sayings…* 1680 (`B02133.0001.001`, **получен полностью**) — 1 свидетель. Сноска Wood на дату — только «1680.». Проверка дня недели: 28 июля 1680 = среда (юлианский), 27 июля = вторник (тома 03, 11, 12, 13) |
| Биография Чарнока — «скудна инцидентами» | Добавлено: тема **последней проповеди** («To anger he was slow for our sins past / Upon which subject Charnock preacht the last»), причина ухода из Ирландии («not for any crimes, / But by an alteration of the times»), указание на **предшественника** («To Fowler's place God call'd him to succeed»), и отрицательный факт о рождении («His Birth and his Beginning scarcely known») — всё из анонимной элегии 1680 (том 13). Заголовок: четыре новых сведения, ни одного нового цитируемого текста Чарнока |
| Последняя должность Чарнока — Crosby Hall с Watson'ом | Зафиксирована **коллизия** `CONFLICT-14`: поэт 1680, обращающийся «To you his hearers», последней должностью называет «Fowler's place» и **не упоминает ни Crosby Hall, ни Watson**. Гипотеза отдела: Fowler = Christopher Fowler (1610–1678), изгнанный саутуаркский проповедник, соавтор *The Morning Exercise at Cripplegate* 1674–6 — того сборника, где напечатан sermon 19 Чарнока (том 13 §4.1, том 02) |
| Архивный материал Чарнока — «скуден» | Конкретный перечень 10 первоисточников и 4 утраченных свидетельств (том 01) |
| Биографический нарратив эдикторов датируется 1684 | Эпистол «TO THE READER» существует **с 1680 года**: издание `A32726.0001.001` даёт тот же текст, что и 1684-е (`A79420.0001.001`); эдикторы не переписывали нарратив. Все биографические утверждения эпистола — с 1680 года (том 08 §4A) |
| Сэнкрофт как наставник — эксклюзив Wood 1691 | **Снят**: эпистол 1680 называет «the present Arch-Bishop of Canterbury»; в 1680 году это William Sancroft (1678–1691) |
| *Attributes* — «1681–82 или 1682» | **1682**: титульный лист первого издания `A32723.0001.001` датирован M DC LXXXII. Диапазон «1681–82» = две части с разной датой титула |
| Contemporaneous печатных объектов 1680 года — один (funeral sermon Johnson) | **Три**: funeral sermon Johnson (`A46911.0001.001`), broadside *The sayings…* (`B02133.0001.001`), памфлет *New poems…* (`A52960.0001.001`). Два из трёх **получены полностью**, оба с CC0 1.0; третий — funeral sermon. Элегия 1680 (WorldCat 606749756) — четвёртый, не получен |

---

## 6. Следующее проверяемое действие для связки

1. **Привести `CHARN_PRACT_ATHEISM_001` к странице Nichol 1864 vol. 1.** Это единственный
   quote-anchor корпуса, претендующий на точную цитату.
2. **Установить Nichol vol. 3 pagination** для two-state diagnostic и всех regeneration claims
   `TEEN_DOUBLE_LIFE/52`.
3. **Сверить CCEL-тексты с Nichol vol. 3**: убедиться, что CCEL *Necessity/Nature/Efficient/Word*
   — это действительно дискурсы vol. 3, а не другая редакция.
4. **Проверить, что Digital Puritan vol. 3 txt.html** содержит те же дискурсы, что и Nichol vol. 3,
   и в каком порядке.
5. **Создать в отделе tom 11** — quote-card ledger, если после шагов 1–4 наберётся достаточно
   verified локаторов. До тех пор не создавать: дельта интегрируется в существующие тома.
6. **Не переписывать** `СЕРИЯ СЕРДЦЕ/27` §4: её классификация верна. Отдел дополняет, не заменяет.

---

## 7. Права, архив и публикационные HOLD

- Все quote-anchors корпусов: `A2`, `locatorState = digital`. `LOCATOR_HOLD` сохраняется.
- Новые `A1` quote-safe источники (томы 08, 09): CC0 1.0 для TCP-текста; `PUBLICATION_HOLD`
  сохраняется до постраничной сверки со снимком.
- Перенос в Product: `PUBLICATION_HOLD` по всему отделу.
