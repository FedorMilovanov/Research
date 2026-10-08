# Карточки: III–IV вв. (пробелы) и латинский Запад

**Дата:** 2026-10-08
**Статус:** `RESEARCH CARDS / NO VERDICT / EVIDENCE_HOLD / PUBLICATION_HOLD`
**Метод:** [`01_METHOD_LOCATORS_GENRE_ANACHRONISM.md`](01_METHOD_LOCATORS_GENRE_ANACHRONISM.md)
**Задача файла:** закрыть дыры, оставшиеся после `02_`–`05_`: Ипполит (был `LOCATOR_HOLD`), Иларий (был `LOCATOR_HOLD`), Амвросий, Иероним, Евсевий, III в. (Григорий Чудотворец, Мефодий, Лактанций), Александр Александрийский.
**Каналы:** CCEL-тома Schaff-сета (ANF05, ANF06, ANF07, NPNF2_01, NPNF2_06, NPNF2_09, NPNF2_10) — локально `…/downloads/<VOL>/<VOL>.txt`; локаторы даны как `VOL.txt:L<line>` (строки файла-источника, не печатные страницы; печатная пагинация — `LOCATOR_HOLD`).

> **Замечание о среде.** В этой волне рабочие копии томов пришлось добывать заново (прежний `/tmp` не сохранился); том-локально: 8 томов. Переносимые материалы под-корпуса лежат в `_src/greek/` (вне git). Потери данных под-корпуса нет: все md-файлы и SSOT — в репозитории.

---

## HIP-1. Ипполит Римский (ок. 170–235)

### (a) «Против Верона и Геликса», фрагмент II — основной локус

**Локатор:** ANF05, раздел *Fragments of Hippolytus* (CCEL `anf05.iii.iv`), внутри — «Against Beron and Helix», **Fragment II**, `ANF05.txt:L23452–23570` (цитата `L23558–23570`).
**Перевод (ANF):** «For with this purpose did the God of all things become man, viz., in order that by suffering in the flesh, which is susceptible of suffering, **He might redeem our whole race, which was sold to death**; and that by working wondrous things by His divinity… He might restore it to that incorruptible and blessed life **from which it fell away by yielding to the devil**; and that He might establish the holy orders of intelligent existences in the heavens… the doing of which is **the recapitulation of all things in himself**.»
**Жанр:** фрагменты полемического слова против еретиков (Berоn/Helix).
**Что утверждает:** (1) Христос **выкупил весь род**, проданный смерти; (2) освобождение — от «уступки диаволу», а не от сделки с ним; (3) «рекапитуляция всего в Нём» — терминология Иринея в III в.
**Что не утверждает:** «кому» уплачен выкуп; ничего о «праве диавола» как юридической величине.
**Осторожно (attribution):** название фрагмента и авторство — традиционные; ANF сам оговаривает заголовок («N.B. Beron = “Vero”», `L23493–23494`), а весь блок «Fragments» включает тексты спорной атрибуции → `LOCATOR_HOLD` по атрибуции, `ORIGINAL_TEXT_HOLD` (греч. не сверен).

### (b) Толкование на Даниила (фрагменты), §45

**Локатор:** ANF05 (блок «On Daniel» начинается `L17841`: «I. Preface by the most holy Hippolytus, (Bishop) of Rome»), §45, `ANF05.txt:L21271`.
**Перевод (ANF):** «He also first preached to those in Hades, becoming a forerunner there when he was put to death by Herod, that there too he might intimate that **the Saviour would descend to ransom the souls of the saints from the hand of death**.»
**Жанр:** экзегетический комментарий (фрагменты).
**Что утверждает:** схождение Христа во ад описано как **выкуп душ святых «из руки смерти»** — «держатель» здесь — смерть/ад, не диавол-кредитор.
**Что не утверждает:** ничего о платеже.
**Пометка:** точное деление работы (§45 внутри «On Daniel» или следующего блока фрагментов) в PD-канале не проверяется без печатного тома → `LOCATOR_HOLD` (книга/раздел), локус-строка верна.

**Живые чтения (B1, по именам):** (a) Ипполит читается как звено между Иринеем (рекапитуляция) и александрийцами (толкование на выкуп-победу); (b) критическое чтение настаивает, что «Fragments» — сборник разной степени достоверности, и на нём нельзя строить «учение Ипполита».
**Анахронизм:** «Ипполит учил выкупу диаволу» — в проверенных текстах этого нет: у него «проданные смерти»/«рука смерти».

---

## MET-1. Мефодий Олимпийский (ум. ок. 311)

**Локатор:** ANF06, *Three Fragments from the Homily on the Cross and Passion of Christ*, фрагм. I, `ANF06.txt:L37838–37960`.
**Перевод (ANF), ключевое:** «Christ, the Son of God, by the command of the Father, became conversant with the visible creature, in order that, **by overturning the dominion of the tyrants, the demons**, that is, **He might deliver our souls from their dreadful bondage**… until Christ, the Lord, by the flesh in which He lived and appeared, weakened the force of Pleasure's onslaughts… **and freed mankind from all their evils**… For it had not been wonderful if Christ, by the terror of His divinity… had reduced to weakness the adverse nature of the demons… therefore it was that **by a man He procured the safety of the race**… and that the demons, **being conquered by one weaker than they**, and thus brought into contempt, might desist from their over-bold confidence… It was for this mainly that the cross was brought in, being erected as **a trophy against iniquity**… after that he had made up for the defeat which, by his disobedience, he had received, and had lawfully conquered the infernal powers, and **by the gift of God had been set free from every debt**.»
**Жанр:** гомилия (вопросы слушателей: «что нам пользы, что Сын Божий был распят?»), в которой отвечает антиоригенистски настроенный автор.
**Что утверждает:** тиранство демонов сокрушено; освобождение — даром («gift of God»), а не платой; крест — трофей; победа одержана «человеком» (Христом в плоти) — смиряющий демонов способ.
**Что не утверждает:** ни «выкупа диаволу», ни «удовлетворения», ни объёма. **Важно:** Мефодий — главный критик Оригена своего века, но **не** воспроизводит оригеновской гипотезы о выкупе «лукавому»; там, где Ориген строит сделку, Мефодий строит триумф.
**Пометка:** `ORIGINAL_TEXT_HOLD` (греч. не сверен); ANF-фрагменты — перевод XIX в.
**Живые чтения:** (a) Мефодий — свидетель «классической» модели победы в восточной традиции до Никеи; (b) критическое: фрагментарность не позволяет говорить о «системе».

---

## THA-1. Григорий Чудотворец (ок. 213–270) — молчание

**Где искали:** ANF06, раздел *Gregory Thaumaturgus* (`ANF06.txt:L217–7200`: «Похвальное слово Оригену», «Переложение Екклесиаста», «Каноническое послание», «К Феопомпу о страдающем и бесстрастном», «Изложение веры»).
**Результат:** искупительной лексики (ransom/redemption/redeem) в разделе **нет**; «oblation» встречается в значении жертвоприношения/приношения.
**Что не выводить:** молчание фиксируется как результат поиска по каналу, а не как позиция автора.

---

## LAC-1. Лактанций (ок. 250–325) — два ложных друга и одна общая формула

1. **Divine Institutes VI.3** (`ANF07.txt:L15977`): «…because God, who is the guide of that way, **denies immortality to no human being**» — речь о том, что христианский «путь» открыт людям всякого пола и возраста, в отличие от языческих учителей. **Редакторская сноска ANF [1098]** (`L16008`) гласит: «[Universal redemption is lovingly set forth by our author.]» — это **аппарат A. C. Coxe (XIX в.)**, а не текст Лактанция, и «universal redemption» там означает всеобщий доступ к пути, не искупление на кресте → ложный друг.
2. **Divine Institutes VI.12** (`ANF07.txt:L17156`): «The **ransoming of captives** is a great and noble exercise of justice» — **цитата из Цицерона** о милосердии/милостыне. Латинская идиома *redemptio captivorum* = выкуп пленных как социальное дело, и в этом значении она встречается у латинских авторов постоянно (ср. Амвросий, `NPNF2_10.txt:L7650, L7690–7691`) — не «теория искупления».
3. **Epitome** (`ANF07.txt:L24830`): «…unless a man shall have received Christ, whom God has sent, and is about to send **for our redemption**…» — общая формула, без «кому».
**Жанр:** апологетико-этический трактат (VI книга — о справедливости и милосердии).
**Анахронизм:** цитировать епископскую сноску ANF как «учение Лактанция» и опираться на *redemptio captivorum* как на сотериологию.

---

## HIL-1. Иларий Пиктавийский (ок. 310–367), *De Trinitate* — закрытие `LOCATOR_HOLD`

| Локус | Локатор | Текст |
|---|---|---|
| **X (о человечестве Христа)** | `NPNF2_09.txt:L22458` | «…unless (God the Word being able of Himself to take flesh from the Virgin and to give that flesh a soul, **for the redemption of our soul and body**), the Man Christ Jesus was born perfect…» |
| **XII.18** | `NPNF2_09.txt:L27208` | «…thanks to **the redemption wrought by the tree of Life, that is, by the Passion of the Lord**, all that happens to us is eternal…» |
| **VI** | `NPNF2_09.txt:L16397` | полемический аргумент против ариан: если Сын — творение, то Бог дал «одно из ничего воздвигнутое **за искупление** другого из ничего воздвигнутого» — «эта дешёвая и ничтожная жертва плохое ручательство Его любви» |

**Жанр:** догматический трактат (антиарианская полемика).
**Что утверждает:** крест — «Passio Domini» как средство искупления; достоинство Жертвы доказывает, что Сын не творение (христологический аргумент, в котором искупление — часть посылки).
**Что не утверждает:** ни объёма, ни «кому».
**Анахронизм:** вырывать «redemption of our soul and body» как сотериологический тезис вне аргумента о природах Сына.
**Статус:** `LOCATOR_HOLD` снят по этим трём локам (NPNF2_09); греческого/латинского оригинала нет → `ORIGINAL_TEXT_HOLD` (лат. De Trinitate в проверенном канале отсутствует).

---

## AMB-1. Амвросий Медиоланский (ок. 340–397)

| Локус | Локатор | Текст |
|---|---|---|
| *De officiis* III.19 (кн. III, гл. III = §19; гл. III с `L8192`, гл. IV с `L8336`) | `NPNF2_10.txt:L8263–8264` | «…the whole community of the human race [is] disturbed in one man… **Christ the Lord, also, Who died for all, will grieve that the price of His blood was paid in vain.**» |
| *De Spiritu Sancto* I.12.126 | `NPNF2_10.txt:L11952–11954` | «The peace and grace of the Father, the Son, and the Holy Spirit are one, so also is Their charity one, **which showed itself chiefly in the redemption of man**.» |
| *De officiis* (о выкупе пленных) | `NPNF2_10.txt:L7650, L7690–7694` | «the redemption of captives» — милостыня, а не учение о кресте (лат. идиома, см. LAC-1) |

**Жанр:** этико-пастырский трактат (De officiis) и догматический трактат (De Spiritu Sancto).
**Что утверждает:** «умер за всех» и «цена крови» — в пастырском рассуждении о вреде, который один человек наносит целому; при «единстве любви» Трёх — «искупление человека».
**Что не утверждает:** не разбирает объём; не «удовлетворение правосудия».
**Анахронизм:** «Амвросий о выкупе пленных = учение об искуплении» — ложный друг латинской идиомы.

---

## JER-1. Иероним (ок. 347–420), *Против Иовиниана* I.11

**Локатор:** `NPNF2_06.txt:L39287` (книга I трактата начинается `L38619`).
**Перевод (NPNF):** «…“Ye were bought with a price, become not servants of men.” **We have been redeemed with the most precious blood of Christ: the Lamb was slain for us**, and having been sprinkled with hyssop and the warm drops of His blood, we have rejected poisonous pleasure.»
**Жанр:** полемический трактат об аскезе/браке/девстве (против Иовиниана).
**Что утверждает:** искупление «драгоценнейшей кровью» как основание свободы от «рабства людей» — аргумент аскетической этики, подкреплённый Писанием.
**Что не утверждает:** ничего об объёме; ничего о «кому».
**Анахронизм:** использовать как «свидетельство об ограниченном/всеобщем искуплении» — текст этического спора.

---

## EUS-1. Евсевий Кесарийский (ок. 260–339), *Похвальное слово Константину* (Tricennial Oration), гл. XV

**Локатор:** NPNF2_01 (под-том: «Life of Constantine, together with the Oration of Constantine to the Assembly of the Saints, and the Oration of Eusebius in Praise of Constantine», см. `L51085–51087`), **глава XV** — `NPNF2_01.txt:L68280` (начало главы), цитата `L68399–68407`.
**Перевод (NPNF), ключевое:** «For as soon as the one holy and mighty sacrifice, **the sacred body of our Saviour, had been slain for man, to be as a ransom for all nations**, heretofore involved in the guilt of impious superstition, thenceforward the power of impure and unholy spirits was utterly abolished, and every earth-born and delusive error was at once weakened and destroyed.»
**Жанр:** **панегирик** (праздничное слово; в том же томе отдельно стоит «Орация Константина к собранию святых» — имперская риторика).
**Что утверждает:** жертва Христа — «выкуп за все народы»; устранение демонической власти; язык победы в триумфальном регистре.
**Что не утверждает:** это не догматическое рассуждение; объём и «кому» не обсуждаются.
**Анахронизм:** цитировать панегирик как вероучительный документ; смешивать с *Demonstratio Evangelica* (DE), которая в PD-канале отсутствует → DE — `ARCHIVE_HOLD` (Ferrar 1920).

---

## ALX-1. Александр Александрийский (ум. 328), Послания (ANF06), «V. О душе и теле и страдании Господа»

**Локатор:** ANF06, *Epistles of Alexander of Alexandria*, V (`ANF06.txt:L28392` — начало), цитаты: `L28416–28418`, `L28630–28643`.
**Перевод (ANF), ключевое:**
- «…the Lord Himself hath shown His charity towards us, not only in words but also in deeds, since **He hath given Himself up as the price of our salvation**.» (`L28416–28418`)
- «Who compelled God to come down to earth… to be nailed to the tree… in the cause of redemption **to give life for life, blood for blood, to undergo death for death? For Christ, by dying, hath discharged the debt of death to which man was obnoxious.** Oh, the new and ineffable mystery! **the Judge was judged**… He died who gives life.» (`L28630–28643`)
**Жанр:** послание-слово (в ANF — среди посланий Александра, в том числе против Ария; по ANF-пометке [2472] фрагментарность подчёркнута самим редактором).
**Что утверждает:** «жизнь за жизнь, кровь за кровь, смерть за смерть»; Христос **«уплатил долг смерти»**, которому подлежал человек; судья был судим.
**Что не утверждает:** долг — **смерти**, а не «чести Бога»; объём не обсуждается.
**Анахронизм (важно):** слово «долг» здесь ≠ анзельмов *debitum* чести, которое человек не может уплатить; это «долг смерти» из Рим 5–6 и Быт 2:17. Прямое смешение двух «долгов» — грубая ошибка (см. `09_`, F-19).
**Пометка:** `ORIGINAL_TEXT_HOLD` (греч. не сверен); атрибуция и состав посланий — по печатному тому ANF06 (`LOCATOR_HOLD` по [2472]-примечанию и по печатной странице).

---

## Сверка с оригиналом (добавлено в этой волне)

**Августин, *De Trinitate* XIII — латинский текст (VERIFIED_ORIGINAL).** Источник: `thelatinlibrary.com/augustine/trin13.shtml` (транскрипция; аппарата нет).
- **XIII.12.16**: «Si ergo **commissio peccatorum per iram dei iustam hominem subdidit diabolo, profecto remissio peccatorum per reconciliationem dei benignam eruit hominem a diabolo**.»
- **XIII.13.17**: «**Non autem diabolus potentia dei sed iustitia superandus fuit.** … placuit deo ut **propter eruendum hominem de diaboli potestate non potentia diabolus sed iustitia uinceretur**, atque ita et homines imitantes Christum iustitia quaererent diabolum uincere non potentia.»
  (Осторожно с чтением: в транскрипции «non potentia diabolus sed iustitia uinceretur»; NPNF-перевод даёт «не силой Бога, но Его праведностью» — см. [`05_`](05_FIFTH_CENTURY_AND_BOUNDARY_CARDS.md), AUG-1.)
**Что это меняет:** центральная формула AUG-1 («праведностью, не властью») теперь подтверждена по латыни, а не только по переводу XIX в.

### Ириней, *Adv. haer.* III.18.1 — латынь найдена (2-я волна, 2026-10-08)

**Источник:** Irenaeus, *Libros quinque adversus haereses*, ed. W. W. Harvey, vol. 2 (Cantabrigiae 1857) — archive.org item `sanctiirenaeiep00harvgoog`; текст получен **полнотекстовым поиском внутри скана** (`…/fulltext/inside.php?item_id=…&q=…`), скан-страница 106.
**Цитата (лат.):** «…sed quando incarnatus est, et homo factus, **longam hominum expositionem in seipso recapitulavit**, in compendio nobis salutem praestans, ut quod perdideramus in Adam, id est, secundum imaginem et similitudinem esse Dei, hoc in Christo Jesu reciperemus.»
**Аппарат:** скан-стр. 452 (дополнения тома): «longam hominum expositionem **denuo instauravit** (*Int.* ?in seipso recapitulavit])» — сирийское чтение «начал заново» против латинского «recapitulavit»; ср. ANF01, сноска [3633] («So the Syriac. The Latin has, 'in seipso recapitulavit'»).
**Итог:** вторая половина F-16 закрыта — латинское `recapitulavit` в III.18.1 подтверждено по печатному изданию (скан), а не по переводу. Ограничение: латынь *Adv. haer.* — древний перевод; греческий оригинал книги III в PD-каналах отсутствует.

### Ириней, кн. V — проверка F-4 (частично)

Индекс тома Harvey vol. 2: «Suadela — 6, 7, 301; **ii. 315**» (без префикса = vol. I; «ii.» = vol. II), т.е. интересующая формулировка «не насилием, но убеждением» стоит в vol. II ок. p. 315 (кн. V). Полнотекстовый поиск по телу тома совпадений не дал (OCR/индексные страницы) → F-4 сохраняет оговорку «локус требует отдельной сверки». См. [`09_…`](09_SILENCES_AND_FALSE_FRIENDS.md).

### Что сверилось и что нет (2-я волна)

- **Сверилось:** Ириней III.18.1 (лат., Harvey vol. 2, p. 106); Августин *De Trin.* XIII.12.16/13.17 (Latin Library).
- **Не сверилось (осталось на переводе ANF/NPNF):** HIP-1, METH-1, ALX-1 (греч.), LAC-1, HIL-1, JER-1, AMB-1, EUS-1 (оригиналы) — см. [`10_…`](10_ORIGINAL_LANGUAGE_VERIFICATION.md), дополнение 2-й волны.
- **Ловушки этой волны:** F-17 (редакторская вставка ANF у Лактанция), F-18 (*redemptio captivorum* = милостыня), «долг смерти» у Александра Александрийского ≠ *debitum* Анзельма, `redemption` в Еф. 1:14 у Златоуста (F-20).

---

## Что закрыто и что осталось

| Было | Стало |
|---|---|
| H-1 Ипполит — `LOCATOR_HOLD` | **HIP-1** (2 лока; атрибуция фрагмента и деление «On Daniel» — `LOCATOR_HOLD`) |
| Иларий — `LOCATOR_HOLD` | **HIL-1** (3 лока: De Trin. VI, X, XII.18) |
| Амвросий — `LOCATOR_HOLD` | **AMB-1** (De officiis III.3; De Spiritu Sancto I.12.126) |
| Иероним — `ARCHIVE_HOLD` (том не выгружен) | **JER-1** (Adv. Jovinianum I.11) |
| Евсевий — не начат | **EUS-1** (Oration XV) + *DE* = `ARCHIVE_HOLD` |
| III в.: Григорий Чудотворец, Мефодий, Лактанций | **THA-1** (молчание), **MET-1**, **LAC-1** |
| Александр Александрийский — не заявлен | **ALX-1** |
| Августин De Trin. XIII — только перевод | **латынь сверена** (XIII.12.16; XIII.13.17) |

**Остаётся открытым:** печатные локаторы (ANF/NPNF том + страница; PG/PL) для всех карточек этого файла; греческие оригиналы Мефодия, Ипполита, Александра; Кирилл Алекс. (`Contra Nestorium`, `In Ioannem`) — `ARCHIVE_HOLD`; Григорий Великий (*Moralia*, Bliss) — `ARCHIVE_HOLD`; Феофилакт, Фотий — `RIGHTS_HOLD`; Анзельм (Deane 1903) — `ARCHIVE_HOLD`.
