# 35. Масса носителей позиции: реестр «четырёхпунктников» и гипотетических универсалистов по всем эпохам

**Создан:** 2026-10-23 (круг 15). **Статус:** рабочий реестр, не вердикт. **Публикация:** `publicationEligible=false`, `EVIDENCE_HOLD` в силе.
**Зачем.** В корпусе позиция разобрана по одному носителю — статье А. Прокопенко (`01_`, `06_`, `23_`, `34_`). Это делало разбор уязвимым: оппонент всегда мог ответить «вы спорите с частным случаем». Здесь собрано **сколько удалось найти** носителей той же схемы по всем эпохам — от III в. до 2023 г., включая древних, очень старых и совсем новых, — с честной отметкой, что именно про каждого из них **доказано**, а что только **приписано**.
**Главное методологическое правило этого файла:** строка без класса достоверности не имеет права существовать. Класс — не украшение, а обязательное поле; гейт корпуса (`scripts/validate_atonement_corpus_integrity.py`, правило 23) сверяет число строк, распределение классов и то, что каждая строка класса `C` стоит в очереди §17.

## 0. Шкала классов (закрытая)

| Класс | Что значит | Что проверяет гейт |
|---|---|---|
| `A1` | место прочитано по изданию; есть страница / колонка / номер пар.; унаследованные локаторы помечены «по `22_`/`34_`» | обязательны 4-значный год и маркер локатора |
| `A2` | выход­ные данные (автор, заглавие, год, издательство) сверены по проверяемому источнику; само место не читалось | — |
| `B1` | утверждение взято из вторичного исследования с локатором («X пишет, что Y утверждал…») | — |
| `B2` | утверждение из партизанских списков, справочников или из памяти; локатора нет | — |
| `C` | требуется добыча: строка обязана иметь адресата в очереди §17 | 1:1 с очередью |

`B2` — это не «врут», это «я не проверила». Половина историко-догматических списков в этом споре живёт именно на `B2`, и ровно поэтому §14 (ложные друзья) здесь важнее, чем §1–§12.

## 1. Поздняя античность: позиция ещё не сформулирована, тексты уже есть

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-01 | Кассиан, *Conlationes*, кн. XIII (собеседник Germanus; «12 анафематизмов» против предопределения единичных) | 1 Тим 2:4 читается буквально: Бог хочет спасти всех; воля к спасению не делится на «избранных» и «прочих» | `A2` | NPNF II.11 (*The Institutes and Select Conferences*, ed. P. Schaff, 1883/1894), Conference XIII; лат. CSEL 13 (Pichler 1882). Нужно: сверка глав (XIII 7–12 vs 13–19) по CSEL |
| FP-02 | Проспер Аквитанский, *Liber sententiarum ex operibus Augustini* (ок. 435) и *Capitula* | сборник мест Августина, отобранных так, чтобы «все хотят спастись» осталось в тексте; против «единичного» предопределения | `C` | PL 45:179–200? — установить объём и номер главы; очередь Q-02 |
| FP-03 | Геннадий Марсельский, *De dogmatibus ecclesiasticis* (гл. 16–19) | «Бог хочет, чтобы все спаслись… кто не хочет — по своей воле»; труд долго печатался под именем Августина | `B2` | PL 58 (и *Corpus…*, изд. B. de Margerie?); случай **ложной атрибуции авторства** — отдельный сюжет, см. §14 |
| FP-04 |Faust де Riez, *De gratia* (ок. 470–480, кн. I–II) | благодать даётся «всем верующим», предосуждения нет | `C` | изд. A. Consolati, *Fausto di Riez: La Grazia* (1976?), CC Series — уточнить; очередь Q-04 |
| FP-05 | Ориген (в латинских переложениях Руфина/Иеронима) — *Commentariorum series in Ioannem*, in 1 Tim 2:4 | «умер за всех» у Оригена есть, но в связке с апокатастасисом: все и спасутся — иная позиция | `C` | GCS 10 (Boumatter? — Etzold 1905–1908) / *Die griech. christl. Schr.*; очередь Q-05 |
| FP-06 | Анафематизмы против «оригенистского универсализма» (Константинополь 543/544; II К-поль 553) | осуждается **всеобщность спасения**, а не всеобщность предложения: граница, которую обе стороны спора любят стирать | `B1` | сверено в лану: см. `ИСКУПЛЕНИЕ/fathers/08_UNIVERSAL_TEXTS_IN_THE_FATHERS.md`, `ИСКУПЛЕНИЕ/fathers/09_SILENCES_AND_FALSE_FRIENDS.md` и запись круга 2026-10 о «оригеновских анафемах 544 г.»; нужно: изд. Schwartz, *Duae collectiones de novilianis?/ Liber de tribus capitulis* |

**Вывод эпохи (не вердикт):** до VI в. нет ни одного текста, который ставил бы вопрос «за *кого именно* умножена цена» как отдельный. Есть «за всех» без трилеммы и есть «за многих» без частности. Это ровно то, что делает позднейшую апелляцию «так учили все древние» недоказуемой с обеих сторон.

## 2. Каролингский спор (849–860): здесь вопрос впервые назван

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-07 | Готшальк Орбийский, *Defensio prædestinationis* и фрагменты (849–853) | «Кто говорит, что Господь пострадал вообще за всех, для спасения и искупления и избранных, и отверженных, — противоречит Богу Отцу»; 1 Тим 2:4 = «все избранные» | `B1` | фрагменты по изданию: *Gottschalk and a Medieval Predestination Controversy* (см. FP-08); PL 112? / Mauguin 1650 — точность издательских знаков требует сверки |
| FP-08 | Victor Genke, Francis X. Gumerlock (transl. & ed.), *Gottschalk and a Medieval Predestination Controversy: Texts Translated from the Latin* (Mediaeval Philosophical Texts in Translation) | первый полный англ. перевод спора; внутри — аппарат с колонками PL | `A2` | Milwaukee: Marquette University Press, 2010, 247 s., ISBN 978-0-87462-253-9 (в изд. 2019 — Wipf & Stock?); нужно: сверить, какой лист/стр. у нужного фрагмента |
| FP-09 | Гинкмар Реймсский, *De prædestinatione Dei et libero arbitrio* | Бог предопределил только ко благу; «нет такого человека, за которого Христос не пострадал» | `A1` | PL 125:49–474; конкретные колонки 55, 85B–C, 618C — сверены по аппарату FP-08 |
| FP-10 | Серват Луп (Луп Феррьерский), *De tribus quæstionibus* (850) | три вопроса: свободная воля, предопределение и **объём искупления**; Луп держит «за всех» | `B1` | описание вопроса как «the extent of the atonement» — у Шаффа, *History of Christian Church* IV, §119 (CCEL, онлайн-паг. 851 sqq.); нужно: текст по PL 119 / изд. |
| FP-11 | Ратрамний Корбийский, *De prædestinatione* (850) | предопределение только к жизни; гибель — от человека | `C` | PL 121? / *De anima*? — edition uncertain; очередь Q-11 |
| FP-12 | Пруденций Троаский, *Epistola de prædestinatione* / *Contra Ioannem Scotum* | против «двух» предопределений; «Христос желал спасения всех» | `C` | PL 115?; изд. — очередь Q-12 |
| FP-13 | Флор Лионский, *De prædestinatione contra Ioannem Scotum* | держит Готшалька, но не держит «предопределения ко злу» | `C` | PL 119?; Gumerlock (см. FP-08) — очередь Q-13 |
| FP-14 | Иоанн Скот Эриугена, *De divina prædestinatione* (851) | ответ Готшальку; универсальная воля спасения при реальности предосуждения | `A2` | изд.: Mauguin 1650; Floss в PL 122; Lambot (1922?) — год издания по каталогу уточнить |
| FP-15 | **Собор в Квирзи (Quierzy, 853)**, артикулы | 1) Бог хочет спастись всем; 2) Христос пострадал за всех; 3) предосуждения нет; 4) благодать необходима | `B1` | цитируется как источник CCC 605 (см. FP-71) и описан у Gumerlock, *Kerux* 22:3 (2007), 17–34; нужно: *Concilium… Quierciense* — Mansi XIII?; **это ядро всей «древности» позиции** |
| FP-16 | **Тюзей (Tusey, 860)**, компромиссная формула | предопределение — к жизни; воля повреждена, но не потеряна; «Бог хочет всех спасти, Христос умер за всех» | `B1` | изложение у Gumerlock (Kerux 22:3, 2007); нужно: *Concilii Tuziensis acta* — Mansi XIV / Hefele |
| FP-17 | Иаков Ушер как **издатель** спора, *Gottchalci et Prædestinatianæ controversiæ ab eo motæ Historia* (Dublin 1631; Hanover 1662) | четырёхпунктник сам нашёл и издал IX в.: «за всех» — не новинка, а древность | `A2` | зафиксировано у Шаффа, *HCC* IV §119 (список источников); нужно: сверка с *The Whole Works of Ussher*, vol. XXII? (Petrie 1864–66) |

**Вывод эпохи:** тезис, популярный в лагере «за всех» («вопрос об объёме возник только в XVI в.»), — **ошибочен в такой форме**: в 850-х гг. он прямо назван одним из трёх вопросов (FP-10). Одновременно ошибочен и тезис противоположной стороны («IX век на нашей стороне»): Квирзи и Тюзея приняты именно *анти*-готшальковской партией (FP-15, FP-16).

## 3. Средневековье: различение, из которого потом вырастет вся позиция

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-18 | Пётр Ломбардский, *Sententiæ* III, d. 20? и d. 1? | формула «достаточно для всех, эффективно для избранных» (*sufficienter… principaliter?*) — источник всей будущей двусмысленности | `C` | *Libri sententiarum*, ed. Collegii S. Bonaventuræ (Quaracchi 1916), I–II; точный различь — d.20 c.1–3?; очередь Q-18. У Crisp/Bird (FP-69) назван основанием «английского гипотетического универсализма» |
| FP-19 | Фома Аквинский, *ST* III, q. 48 a. 2 ad 2; *In I ad Timotheum*, c. 2 lect. 2 | цена «бесконечна и потому достаточна за всех», спасительно же действует для многих | `C` | изд. Leonina (1888–1906) / Parma (1871) — страницы сверить; очередь Q-19 |
| FP-20 | Бонавентура, *In III Sent.* d. 15–16? | обсуждает, «за кого» и «сколько» | `C` | Quaracchi ed. Opera omnia IX (1885); очередь Q-20 |
| FP-21 | Г. Биель (via moderna), *Collectorium circa IV Sent.* III, d. ?? q. ? | «сделавшему, что в его силах, Бог не отказывает в благодати»: условие ставится тварью, а не отменяет предложение | `C` | изд. Heiko A. Oberman, *The Harvest of Medieval Theology* (1963; Grand Rapids: Baker 2001) — нужно: страницы трактата; очередь Q-21 |
| FP-22 | Брэдвардин, *De causa Dei contra Pelagium* III | противоположный полюс: необходимость, предопределение, «за своих» | `C` | изд. Henry George? (London 1715?; *Opera*, Basel 1571? — уточнить); очередь Q-22 |
| FP-23 | Григорий Риминийский, *In I Sent.* prol. q. 1? | «гипотетическое» чтение «за всех» отвергнуто | `C` | изд. Benets? (Venice 1579–81?) / Modern edition (Brib? ) — уточнить; очередь Q-23 |

## 4. Реформация и Lutheran «универсальная благодать»: конфессиональный слой позиции

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-24 | Erasmus, *Annotationes in Novum Instrumentum* (1516/1519) и *Paraphrasis* в 1 Тим 2 | «за всех» как plain sense; предопределение — не догмат | `C` | *Opera omnia* ed. Le Clerc (Lugd. Bat. 1703–1706), Tom. VI; очередь Q-24 |
| FP-25 | М. Лютер, *In Galatas* (1535; WA 26/40 II) | «pro me» — но для каждого верующего: универсальность в *доверии*, а не в декрете | `C` | Weim. Ausg.: *Vorlesungen Galater* = WA 40 II (1937?); нужно: конкретный лист; очередь Q-25 |
| FP-26 | Ф. Меланхтон, *Loci communes* (1521 → ред. 1559) и *Sententiæ ex Scriptura passim collectæ* (1539/1543) | отрицание предосуждения; «заслуга Христа применяется ко всем» — ядро позиции | `C` | св. свод: *A Melanchthonian Perspective on Predestination* (modernreformation.org, 2018?) — вторичное; нужно: *Corpus Reformatorum* (Halle 1834–60), Bd. 9?; очередь Q-26 |
| FP-27 | **Formula of Concord (1577), Solid Declaration II, §§ 27–28** | «обетование Евангелия *universalis*, то есть относится ко всем людям… Бог возлюбил мир и отдал Сына» | `A1` | *Concordia Triglotta* (Bente, St. Louis 1921) / *Book of Concord* (Tappert 1977), SD II 27–28 — раздел и номер § устойчивы во всех изданиях; цитата прочитана в двух онлайн-зеркалах |
| FP-28 | D. Scaer, *The Nature and Extent of the Atonement in Lutheran Theology* | современный лютеранский взгляд: «за всех» без гипотетического декрета | `A2` | *BETS* 10:4, 179–187 (PDF на etsjets.org); нужно: подтвердить год (2007 vs 2010) |
| FP-29 | И. Г. Бренц, Я. Андреэ (и «филипписты») | спор о том, «универсальна» ли благодать *по существу*; против них — Calov, *Consensus repetitus* (1664) | `C` | Шафф, *Creeds* I §61 (сн. 916, «p. 851») указывает сравнение; нужны собственные тексты; очередь Q-29 |
| FP-30 | М. Хемниц, *Examen Concilii Tridentini* (1565–1573), tractatio de iustificatione | удовлетворение «за всех», применение — верой | `C` | изд. Decker (Berlin 1867?; *Opera theologica* ed. Rudelbach?) — уточнить; очередь Q-30 |
| FP-31 | И. Герхард, *Loci Theologici* (1639–1643) | Бог желает спасения всех **и даёт всем возможность** | `C` | указано у Шаффа, *Creeds* I §45 (сн. 655: «John Gerhard… *Loci Theologici*»); нужно: изд. (Berolini 1879–1883, ed. H. W. Harms?) —Loc. de prædestinatione; очередь Q-31 |
| FP-32 | Гейдельбергский катехизис (1563), в.о. 37–39 | вопрос об объёме **не ставится**: «за всех» в ответах, но без трилеммы | `A2` | текст читается; см. также `ИСКУПЛЕНИЕ/13_DORT_II_CALVIN_OWEN_EXTENT.md` — «молчание исповеданий» как класс улик |
| FP-33 | Кент? — Символы: *Second Helvetic Confession* (1566), гл. ?; *Gallican Confession* (1559) art. ? | «Xристос… умер за наши грехи» без ограничения; вопрос объёма не артикулирован | `C` | Шафф *Creeds* I (тексты есть) — нужно: конкретные артикулы; очередь Q-33 |

## 5. Ремонстранты и арминиане: не «четыре пункта», но общий корень лексики

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-34 | Я. Арминий, *Declaração de sententiis* (1608; лат. 1629) + articles 1609? | «нет человека, исключённого декретом» — при предвосхищающей благодати | `C` | *The Writings of Jacob Arminius*, tr. W. R. Bagnall (1853/1875, 2 vol.; repr. Baker 1960? with Nichols ed.) — нужно: страницы; очередь Q-34 |
| FP-35 | Ремонстрация 1610, Артикул II | «Христос умер за всех и за каждого; верующие *не* спасаются своей волей» | `C` | **ловушка цитирования:** формулировки 1610 г. и пересказы Дорта расходятся; сверить по *Acta* (ed.?; лат. текст в *Judicium*? / C. C. ? — у Шаффа, *Creeds* III: Dordt-контекст) — очередь Q-35 |
| FP-36 | Г. Гроций, *Defensio fidei catholicæ de satisfactione Christi, adversus Faustum Socinum* (Paris 1617) | правительство/довод-«за всех»: *satisfactio* как honoraria, не как idem | `A1` | по лану: `22_` 42bk/42bo (издания сверены в раундах 23–24, 2026-10-16/17) |
| FP-37 | С. Эпископий, *Confessio* (1627) / *Apollonius?/Voorredeneke* (1629) и *Disputatio* | защита «за всех» против Дорта; ключевой для «что именно осудил Дорт» | `C` | *Opera in quo profligatur* (1627); нужно: изд. (van den Berg? / *Oeuvres*?) — очередь Q-37 |
| FP-38 | И. Крелл (Келлиус), *Responsio?/«De satisfactione»* (1629) | полемика о природе зачтения | `C` | сочинение (Amst.?) — уточнить название и год; очередь Q-38 |
| FP-39 | Дж. Лимборх, *Christen Godgeleerdheid* (Amst. 1686; англ. *Christian Theology*, 1692/1713?) | «umoe? » — всеобщность удовлетворения при условном применении | `C` | англ. пер. (London 1693? 1713?), кн. IV? гл. о искуплении — сверить; очередь Q-39 |
| FP-40 | Ф. Соц (Социниане: *Opera quae reperiri potuere omnia*, 1656; катехизис *Racovian Catechism*, 1609) | отрицание замещения вообще — граница, от которой позиция отграничивает себя | `A2` | изд.: *Bibliotheca Fr. Pol.*? Raców?; англ. пер. (London 1791?, tr. W. Chambers?) — нужно: страницы; **в корпусе нужно как контрастный полюс** |

## 6. Сомюр (1618–1664): «четыре пункта» как партия

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-41 | Дж. Кэмерон (1580–1625), *Theses de triplici Dei cum hominibus foedere* (Bourges 1618 / Saumur?) | «три завета»: природы, письма, благодати — логический приоритет条件的ного? | `C` | лат. изд. (Geneva 1653? *Praelectiones*?) — уточнить; очередь Q-41 |
| FP-42 | М. Амираут, *Brief traicté de la prédestination et de ses principales dépendances* (Saumur: Jean Lesnier, 1634; изд. 1658) | условный (гипотетический) декрет спасения через веру; затем — избрание к вере | `A1` | по лану: `22_` №18 и запись с IA `brieftraitdela00amyr` (Saumur: Isaac Desbordes, 1658; 398 с.); страницы абзацев — `34_` §§4.36–4.40 |
| FP-43 | М. Амираут, *Echantillon de la doctrine de Calvin sur la prédestination* (1637) | «я не изменяю учение, а учу порядку» — апеляция к Кальвину | `C` | список сочинений у Шаффа, *Creeds* I §61 сн. 919; нужно: изд. (Saumur 1637; переизд.?) — очередь Q-43 |
| FP-44 | М. Амираут, *Traicté de la justification* (1638) и *De la providence de Dieu? * | оправдание «для всех, кто верит»; провидение и зло | `C` | тот же список Шаффа (PD-первичка!); нужно: экземпляр (BNF/Gallica) — очередь Q-44 |
| FP-45 | Ж. де ла Плас (Placeus, 1596–1655) | **опосредованное** вменение Адама — второй сомюрский тезис; осуждён на Шанторане 1645, смягчён на Лудуне 1659 | `C` | даты/события: Roger Nicole, *Brief Survey on the Controversy on Universal Grace (1634–1661)*; *Tracts*? (в *CTJ*?); нужно: сочинение Placeus *De veritate mediationis?*; очередь Q-45 |
| FP-46 | Л. Каппель (1585–1658) | текстовая критика ВЗ → подрыв «вербального» основания ортодоксии; союзник Амираута | `C` | Шафф, *Creeds* I §61 (стр. 479); нужно: *Arcanum punctationis revelatum* (1624) — дата сверена по описанию; страница — очередь Q-46 |
| FP-47 | Ж. Дайе (1596–1663), *? — поддержка* и трактат *De? /Responsio* | союзник Сомюра (ср. «Daillé favorable») | `C` | Шафф §61 перечисляет его среди друзей; собственные сочинения (в т. ч. *Responsio ad?*) — нужны; очередь Q-47 |
| FP-48 | П. дю Мулен, *Examen de la doctrine de Messieurs Amyraut et Testard* (Sedan 1638) | опровержение: «условный декрет» | `A2` | по лану: `22_` №19 |
| FP-49 | А. Риве (1572–1651) | опровержение Амираута и Тестара (неопубликованное, послано на синод) | `C` | Nicole (FP-52); нужно: рукописный/«Responsum» — очередь Q-49 |
| FP-50 | П. Тестар (Paul Testard) | второй обвиняемый 1637 г. | `C` | имя и роль — Nicole/Шафф; собственные труды? — очередь Q-50 |
| FP-51 | Синоды: Alençon 1637 (осуждены выражения «décrets conditionnels», «Christ est mort également pour tous», «velleity»), Charenton 1645, Loudun 1659 | позиция *допущена*, но лексически запрещена: редкий случай, когда история спора даёт **датированный список точных слов** | `A2` | Roger Nicole, *Brief Survey on the Controversy on Universal Grace (1634–1661)*; также *Tracts*? (перевод 2014 — monergism.com) и цитата Nicole у HeidelBlog 13.11.2015; нужно: *Aymon, Tous les synodes nationaux* (La Haye 1710), II, pp. 183, 298 (указаны Шаффом) |
| FP-52 | *Formula Consensus Helvetica* (1675) — кан. de decreto universali?/ о «volente omnes» | прямой анти-сомюрский канон; лат./нем. тексты, Niemeyer *Collectio* pp. 729–739, Böckel pp. 348–360 | `A2` | Шафф, *Creeds* I §61 (там же вся литература: Hottinger 1723, Pfaff 1723, Salchli 1723, Barnaud 1726, Walch 1733, Hagenbach 1827, Schweizer 1856/1860, Trechsel, Frank 1865, Ebrard 1866) — **готовая библиография добычи** |
| FP-53 | М. Амираут, *Le moyen de concorder l'alliance des œuvres avec celle de la grâce*? (Amst. 1676?) / *De la disposition de l'homme à la conversion?* | поздняя редакция | `C` | посмертные издания (Amsterdam?; *Opuscules?*); сверить — очередь Q-53 |

## 7. Англия и Шотландия 1618–1690: «классические четырёхпунктники»

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-54 | Дж. Ушер, *The True Intent and Extent of Christ's Death and Satisfaction upon the Cross* (1617) | « Satisfaction* для всех, эффективность — для верующих | `A2` | по лану: `22_` №24 (*Whole Works*, Vol. 12, Dublin 1864, pp. 559–596) |
| FP-55 | Дж. Ушер, *The Judgment of the late Arch-bishop of Armagh… of the extent of Christ's death* (лат. *? *, 1634/1655?) | самозащита от обвинения в «новизне»: ссылка на Квирзи и «вселенскую церковь» | `A2` | по лану: `22_` 41g |
| FP-56 | Дж. Давенант, *Dissertatio de Morte Christi, qua declaratur intentio, actio, effectus et extentio* (1627/1630; publ. 1650/1651?) | «pretium pro omnibus» при частности применения | `A1` | по лану: `22_` №23 и `23_` раунды 12–17 (с сверкой по *Collegii Suffragium* 1619, *Opera omnia* 1678/1679?) |
| FP-57 | Дж. Давенант, *Tractatus de arbitrio Dei et hominis* (posth. 1650/1659?) | воля Божия «antecedens/Consequens? » — гипотетический декрет | `C` | по лану: `03_`/`22_`; нужно: изд. (London 1659; *Operum* vol.?) — страница в очереди Q-57 |
| FP-58 | Дж. Престон (Fen Ditton, 1587–1628) | «English Hypothetical Universalism» до Амираута (по Crisp) | `C` | *Works* (London 1634?; *Golden? — «Medulla», «Church-porch?*) — нужно: установить труд и место; очередь Q-58 |
| FP-59 | Дж. Холл (Joseph Hall, 1574–1656) | «смягчённый» объём; эпизод 1619 («Suffrage»?) | `C` | *Works* (Oxford 1837, ed. Whittie?; *Residences?* ) — очередь Q-59 |
| FP-60 | У. Твикл? (W. Twisse, *The Riches of Gods Love*), 1653 | первоисточник для «double contingency»; у него же гипотетическая необходимость удовлетворения | `A1` | по лану: `34_` §4.46 (EEBO-TCP A64002: с. 66, 193) |
| FP-61 | Р. Бакстер, *Aphorismes of Justification* (1649; Appendix 1655, pp. 292–318) | «всеобщая цена + условное освобождение + несомненное исполнение условия» | `A1` | по лану: `34_` §4.39 (TCP A26862) |
| FP-62 | Р. Бакстер, *Universal Redemption of Mankind, by the Lord Jesus Christ* (1694; диспутации ≤1657) | развёрнутое: «никто не примирён фактически, пока не уверует»; довод «дважды» — к Твиссу | `A1` | по лану: `34_` §4.40 (TCP A27064, с. 377, 387, 389, 400–404) |
| FP-63 | Дж. Гудвин, *Redemption Redeemed* (1651) — против Оуэна | «price of redemption is… for all» в споре | `C` | *Works*, London? 1675–1681 (4 vol.) / Oliver David (18??) — нужно: изд. + страницы; очередь Q-63 |
| FP-64 | П. Нее (Philip Nye, пресвитер-независимец) | возражение «за всех» на Вестминстерской ассамблее | `C` | *The Interest of the Kingdom…?* / Mitchell–Struthers, *Minutes of the Sessions of the Westminster Assembly* (Edinburgh: Blackwood, 1874) — в лану уже есть `22_` 41b; нужно: конкретная страница — очередь Q-64 |
| FP-65 | У. Чиллингворт, *The Religion of Protestants* (1637) | аргумент «Бог хочет всех спасти, значит Христос за всех» против идентичности «Церковь = Писание» | `C` | изд. (London 1637; ed. P. Gadue, Oxford 1845? / 1853?) — очередь Q-65 |
| FP-66 | Дж. Тэйлор (Jeremy Taylor), *Liberty of Prophesying* (1647/1652) и *Ductor*? + *Works* (Heber 1828–30?) | англиканская линия «за всех» | `C` | изд. (London 1647; *Works*, 10 vol., 1828? — W. Doolittle?); очередь Q-66 |
| FP-67 | **Дэвид Уильямс / Фома Чонси и «the General Redemption controversy» 1690-х**: Williams, *A Defence of Gospel-truth* (London: John Dunton, 1693; EEBO-TCP **A66344**) | документ с обеих сторон; сам Уильямс — пятипунктник: «for absolute certain Election, for Christ's not dying alike for all» (p. 17) | `C` | EEBO-TCP A66344, стр. 17 прочитана в выдаче; цитата — **против** позиции, важна как датированный *ex officio* ярлык «general redemption»; **нужно**: текст Чонси (*Answer/ Vindication?*) — очередь Q-67 |
| FP-68 | *The Agreement in Doctrine among the Dissenting Ministers in London* (1693, 4°) + Д. Уильямс, *An End of Discord* (1699; EEBO-TCP A66345) | попытка загнать «general redemption» в рамки диссентерского согласия: статьи, добавленные к *Heads of Agreement* в декабре 1692 | `A2` | DNB-статья (Wikisource, *DNB* 1885–1900, s.v. Williams) + prdl.org (17 заглавий); текст A66345 в EEBO — **для A1 не хватает чтение нужного §** |
| FP-69 | С. Уэсли (отец Методистов): переписка/донос на Taunton Academy 1693 | свидетельство, что в диссентерских академиях «general redemption» преподавалась открыто | `C` | *The Life and Times of the Rev. Samuel Wesley* (написана Дж. и Ч. Уэсли; Project Gutenberg 67980 — PD) — нужно: страница эпизода; очередь Q-69 |
| FP-70 | Э. Калами, *A Continuation of an Account of the Ministers… (Abridgement)* 1709/1713 + *Historical Account of my Own Life* | «умеренный» пятипунктник? — классический источник по списку «кто держал всеобщность» | `C` | изд. (London 1709–13; *Select Works*, 1815/1823?) — очередь Q-70 |
| FP-71 | **Катехизис Католической Церкви (1992), п. 605** (+ 616, 1260) | «The Church, following the apostles, teaches that Christ died for all men without exception»: в сн. 411 — **Квирзи 853** | `A1` | vatican.va (ENG0015/__P1O.HTM), пар. 605 прочитан 2026-10-23; рус. пер. (ruscath.ru, ccconline.ru) — тот же пар. **Это самый сильный «всеобщий» авторитет в споре, и он опирается на IX в.** |
| FP-72 | Критика этого шага: «Quierzy говорит о *страдании* по аналогии с воплощением, а не о смерти, и сам держит предосуждение» | зеркальный аргумент | `B1` | vaticanfiles.org (1999-09-02), «The Cross and the Eucharist according to the CCC» |

## 8. XVIII век: методисты, унитарии?, англикане, «британская линия»

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-73 | Д. Уитби, *A Discourse on the Five Points*? / *Points of Calvinism*? (1710; посм. изд. 1720?) | систематическое отвержение 5-го пункта; «general redemption» как статья | `C` | заглавие и год — уточнить (упоминается 1 раз в лану: `22_`?/`03_`); очередь Q-73 |
| FP-74 | Дж. Тиллотсон, *Works*, sermon(s) o «efficacy of faith? / universal redemption?» | «the sincerity of God… offer to all» линия | `C` | изд. (London 1752; *Works* with Life by S. Johnson? — needed) — очередь Q-74 |
| FP-75 | Дж. Локк, *The Reasonableness of Christianity* (1695) + *Paraphrase and Notes on the Epistles of St Paul* (1707) | евангелие = закон веры для всех; без «частного намерения» | `C` | изд.: *Works* (ed. P. Yolton? / *Clarendon Edition*: Reasonableness ed. I. C. Thomas, 1997) — страница; очередь Q-75 |
| FP-76 | Дж. Уэсли, *Explanatory Notes Upon the New Testament* (1755) на 1 Тим 2:6, Тит 2:11, Евр 2:9, 1 Ин 2:2; *Hymns on God's Everlasting Love* (1763); письмо к Р. (1763?) | «general redemption» + предвосхищающая благодать; гимнóлогия как носитель учения | `A2` | *The Works of John Wesley* (Jackson 1872;新方法 BICD): Notes 1755 — нужны страницы; гимны (Bristol 1763) — нужны; нужно: Pinson, «Wesley on the Nature of Atonement» (*evangelicalarminians.org* PDF) как вторичное |
| FP-77 | Дж. Уэсли и «two sorts of Methodists» (particular vs general redemption) | раскол по 5-му пункту внутри пробуждения | `B1` | Шафф, *Encyclopedia of Religious Knowledge* (CCEL, encyc07 ii.xi.ii) — цитата прочитана онлайн |
| FP-78 | Г. Уитфилд, *Letters* (1770s) и ответ на «Letter to Mr. W.? » | противоположная сторона, обязательна для объективности | `C` | *Works* (ed. S. J. Tyler 1871?; *Journal*, 1739–44); очередь Q-78 |
| FP-79 | Дж. Мильтон, *De Doctrina Christiana* (написано 1640-е?, опубл. 1825) кн. VI | декрет «спасти всех верующих»; анти-Троица рядом | `C` | *Complete Prose Works* VI (Columbia UP, 1953–59, ed. M. Y. Hughes) — страницы; очередь Q-79 |
| FP-80 | Дж. Эрквин (John Erskine of Linlathen, 1721–1803), *The Unconditional Freeness of the Gospel*? (1795?/1828) | «безусловная щедрость» предложения — предтеча Кемпбелла | `C` | изд. (Edinburgh 1795?, перераб. 1828?; *Works* 1847?) — установить; очередь Q-80 |
| FP-81 | Р. Уордлоу / оппоненты Эрквина в SEC (Glasgow–Edinburgh, 1805–1817) | шотландский «disruption debate» до 1843 | `C` | *Balances? / «An Apology for…?»*, Glasgow 1817? — уточнить; очередь Q-81 |

## 9. Континентальное Просвещение и либерализм (для полноты «эволюции/деградации»)

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-82 | А. Ричль, *Die christliche Lehre von der Rechtfertigung und Versöhnung* (3 т., 1874/1882-88; англ. *The Christian Doctrine of Justification and Reconciliation*, Edinburgh 1900–03) | искупление как «ценность для всех»; снятие юридической частности | `C` | англ. пер. (tr. H. R. Mackintosh, 3 vol.) — том/страницы; очередь Q-82 |
| FP-83 | А. Гарнак, *Das Wesen des Christentums* (1900) | Иисус проповедует Отца, а не «цену за избранных» | `C` | *GCS* N.F. 1? / англ. 1891 — очередь Q-83 |
| FP-84 | К. Барт, *Kirchliche Dogmatik* IV/1 §§ 59–60; II/2 §34 | «во Христе избран весь род человеческий» — универсализм без гипотетического декрета: иная, чем у Амираута, логика | `C` | ET: *Church Dogmatics* IV/1 (T&T Clark, 1956) — страницы; **обязательно отличать от «четырёхпунктников»**: иначе список превращается в мешанину |

## 10. США: хопкинсианская лексическая пара (уже разобрана в лану) + «неограниченное искупление» в евангельском лагерé

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-85 | Новоанглийская линия 1785–1820: Edwards Jr., Smalley, Hopkins, Emmons,anon. *Theological Magazine* 1795, Whelpley 1816, *Brief View* 1817, Weeks 1820-25, Janeway 1826-27, Bacon 1855, Park 1859 | **не** четырёхпунктники: «atonement неограничен → redemption ограничен» — лексическая, а не декретная схема; самоназвание — «limited redemption» при «atonement sufficient for all» | `A1` | всё по лану: `34_` S66–S85 (страницы указаны в §4.36–4.39), сводка в `01_` §3.1.5–3.1.6 — **самый надёжный блок реестра** |
| FP-86 | А. Барнс, *Notes* на Рим 3:25, Евр 2:9, 1 Тим 2:6 | popular unlimited-atonement exegesis | `C` | *Notes, Critical and Practical, on the… Epistles* (NY: Leavitt? 1837–?) — очередь Q-86 |
| FP-87 | Д. Л. Муди, проповеди («The Way to be Saved»?) | «whosoever» как богословие, не как полемическая лекция | `C` | *Sermons* (1881/1883?; *Gospel Trumpet?*) — страница; очередь Q-87 |
| FP-88 | Р. А. Торрей, *What the Bible Teacheth* (London: Marshall Brothers, 1898/1899) | глава об искуплении | `C` | нужно: изд. и страницы главы; очередь Q-88 |
| FP-89 | Л. С. Чафер, *Systematic Theology* (8 vol., 1947–48) | «unlimited provision, limited application»; «unofficial stance at Dallas» | `C` | атрибуция по обзору/форуму; нужно: vol. VI *The Work of Christ* (Moody? / Galaxie 1993?) — страницы; очередь Q-89 |
| FP-90 | Ч. Р. Смит?/Д. П. Уолворд, *The extent of the? — и Р. Лайтнер | см. FP-91, 92; Walvoord (BST 1982?) | `C` | установить: Walvoord article title/journal/year; очередь Q-90 |
| FP-91 | Р. Лайтнер, *The Death Christ Died: A Case for Unlimited Atonement* (Des Plaines: Regular Baptist Press, 1967, 151 s.) → изд. перераб. *…: A Biblical Case for Unlimited Atonement* (Grand Rapids: Kregel, 1998, 176 s., ISBN 978-0-8254-3155-5) | «объём искупления был малоспорен до Реформации XVI в. и после неё оспаривался только частными» — **тезис, который §2 этого файла опровергает по форме** | `C` | цитаты по с. 9 (перераб. изд.) и с. 33 (изд. 1967) — сверены по цитатам в SES-статье и Crossway-статье; нужно: чтение с. 9 полностью (очередь Q-91) |
| FP-92 | Дж. Уолворд? / У. Н. Нььюэлл, *Hebrews: Verse by Verse* (1938?/1957?) | Евр 2:9 «for every man» | `C` | изд. (Chicago: Moody?; *Verse by Verse*, 1938) — страницы; очередь Q-92 |
| FP-93 | Р. Л. Дабни, *Syllabus* (2-е изд. 1878), лекция XLIII «Christ's Satisfaction not Commercial» | оппонент, но **сам** отрицает «коммерческую» форму — важно для границ спора | `A1` | по лану: `34_` §4.41 (S96), стр. 504, 521 |
| FP-94 | Ч. Ходж, *Systematic Theology* II (1871–73) и А. А. Ходж, *The Atonement* (1867) | «no injustice… punished twice over»; частность «solely from the purpose» | `A1` | по лану: `34_` §4.40 (II.472, 557–558; pp. 31, 369) |
| FP-95 | Шедд, *Dogmatic Theology* (II.469–470) | «Atonement is unlimited, redemption is limited» — **не** четырёхпунктник, а носитель пары | `A1` | по лану: `34_` §4.36–4.39 (Шедд II.469–470) |
| FP-96 | А. Г. Стронг, *Systematic Theology* (1907) | список «кто держал всеобщность» — проверен ланом: у Стронга *limited atonement* в лагере противников? (см. `01_` §3.1.1–3.1.2) | `A1` | по лану: `01_` §3.1.1 (раунд 7), 3.1.2 (раунд 8): Griffin 1819, Fuller 1803, Richards 1846 |
| FP-97 | Генри Смит, *God's Method of Salvation* (London? 1908; изд. 1914?) | «ролл» из ~25 имён «веривших, что Христос умер за всех» (с. 361) + формула «sincerity of God is at stake» | `B2` | список перепечатан у D. L. Allen? и на e-журналах (scottthong 2020) — нужно: экземпляр 1908 г.; **этот ролл — предмет §14** |
| FP-98 | IFCA Statement of Faith (Независимые фундаментальные церкви США) | «unlimited atonement» — догматически закреплённая всеобщность | `C` | текст исповедания (ifca.org) — дата редакции; очередь Q-98 |

## 11. XX–XXI вв.: шотландская линия, реформатские «четырёхпунктники», современная академия

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-99 | Дж. Маклеод Кемпбелл, *The Nature of the Atonement and its Relation to Remission of Sins and Eternal Life* (Cambridge: Macmillan, 1856, xxi+382?; 2-е изд. 1867 с предисловием) | «atonement» без частности: «That cannot be the true conception of the nature of the atonement which implies that Christ died for an election from among men»; осуждён 1831 (обвинения: универсальное искупление, всеобщее прощение, уверенность как сущность веры) | `C` | текст в CCEL (`ccel.org/ccel/c/campbell/atonement/`), 1-е изд. = Macmillan & Co., Cambridge, 1856 (1000 экз.), пагинация 1–382 + «List of Books» — **сверено по репринту Handsel Press 1996 с вступлением J. B. Torrance**; нужно: страницы по 1856 г. (очередь Q-99) |
| FP-100 | Дж. Б. Торренс, *Introduction* к репринту Кемпбелла (Edinburgh: Handsel Press, 1996) + докторская диссертация *The Doctrine of Grace as Expounded in the Light of the Teaching of John McLeod Campbell and Edward Irving* | шотландское чтение Кемпбелла в XX в. | `C` | PDF вступления найден (afkimel, 2024) — читать по нему; очередь Q-100 |
| FP-101 | Дж. Денни, *The Death of Christ* (The Baird Lecture, Edinburgh 1902) и *Studies in Theology* (1894) | «ransom for all» при отрицании «коммерческой» схемы; «the atonement… of universal reference» | `C` | изд. (T&T Clark 1894; 1902; Banner? 1951?) — страницы глав; очередь Q-101 |
| FP-102 | П. Т. Форсайт, *The Cruciality of the Cross* (1897?; изд. 1901/1909) | «It is finished» для всех — без частности | `C` | изд. (Hodder & Stoughton?; Fortress 1988?) — очередь Q-102 |
| FP-103 | Т. Ф. Торренс, *The Mediation of Christ* (1983; 2-е изд. Edinburgh: T&T Clark, 1992), *Theology in Reconciliation* (1974/1996) | всеобщность искупления в онто-присутствии Христа; «не гипотетический декрет» — позиция иного типа | `C` | нужно: страницы («the atonement is… of universal reference» не подтверждено цитатой) — очередь Q-103 |
| FP-104 | О. Крайсп, глава «Anglican Hypothetical Universalism» (в FP-105) | «Ломбардское различение sufficiency/efficiency → гипотетический универсализм»; имя: Ушер, Престон, Давенант как независимая «английская» линия | `B1` | прочитано по Google Books / рецензии (spoiledmilks 24.10.2023, стр. 17 цит.) — нужно: экземпляр, страницы |
| FP-105 | M. F. Bird, S. Harrower (eds.), *Unlimited Atonement: Amyraldism and Reformed Theology* (Grand Rapids: Kregel Academic, 23.05.2023, 240 s., ISBN 978-0-8254-4641-2) | самое полное современное исследование позиции; главы: Amyraut as Exegete; Amyraldism and Penal Substitution; The Doctrine of God and Unlimited Atonement; Unlimited Atonement and the Nature of Forgiveness; Amyraldism in History and Theology; Baptist theological tradition; preaching | `A2` | выходные сверены (Kregel.com, Amazon, Google Books, aut.edu.au) + оглавление; **это — первоочередная покупка** (copyright, не PD) |
| FP-106 | Р. Муллер / А. Мур (историография термина) | «Amyraldism» — misnomer для более широкого «hypothetical universalism» | `C` | указано у Crisp (FP-104): «historians of doctrine like Andrew Moore and Richard Muller»; нужно: Muller, *PRRD* III (2003), index «hypothetical universalism»; Moore — установить работу (очередь Q-106) |
| FP-107 | Б. А. Уорр, *Extent of the Atonement: Outline of the Issue, Positions, Key Texts* (EPM PDF, 2016?) | изложение обеих позиций с классификацией «Classic Arminian / Unlimited» | `C` | epm.org static PDF; нужно: сверка, держит ли сам Уорр всеобщность (внешние списки ставят его как «четырёхпунктника») — очередь Q-107 |
| FP-108 | М. Дж. Эриксон, *Christian Theology* (2-е изд., Grand Rapids: Baker, 1998), с. 846, 852 + *How God Works? / The? * | довод по Ис 53:6 («объём греха и объём возложенного параллельны») | `A2` | страницы засвидетельствованы сноской в диссертации (Shultz, SBTS 2008: «Erickson, *Christian Theology*, 2nd ed. (Baker, 1998), 846… 852»); 3-е изд. 2013 — перенумеровано, нужно сверить |
| FP-109 | Б. Демарест, *The Cross and Salvation* (Word 1997; 2-е изд. B&H 2006) | глава об объёме в пользу всеобщности | `C` | изд./страницы — очередь Q-109 |
| FP-110 | Д. Л. Аллен, *The Extent of the Atonement: A Historical and Critical Review* (Nashville: B&H Academic, 2016, xxviii+820/848 s., ISBN 978-1-4336-4392-7) | «исторически всеобщность — преобладающее мнение; среди кальвинистов — значительный диапазон»; гл. «The Intent, Extent, and Application of the Atonement» (149–186); «Special Issues» (215–239) | `A2` | выходные сверены по 4 независимым описаниям + рецензиям (Engelsma, *CTJ*; DTS Voice 27.08.2020, стр. 534–42, 606 n. 195, 754–62; Founders 2018; Lifeway 2017) |
| FP-111 | Д. Л. Аллен (ed.), *Exploring the Extent of the Atonement: Four Views* (Nashville: B&H Academic, 2016) | четырёхсторонний спор в одном томе — лучший «объективатор» | `C` | установить участников и страницы (очередь Q-111) |
| FP-112 | С. У. Лемке | баптистская «unlimited» линия | `C` | *Theology for the Community of God*? / статьи — установить (очередь Q-112) |
| FP-113 | Д. Nettleton, *Chosen to Salvation* | «the position of the GARBC (Regular Baptists)» | `C` | издательство/год (Regular Baptist Press?) — очередь Q-113 |
| FP-114 | Д. Аллен и оппоненты: К. Дэниел, «The Reformed Faith?» — русскоязычный контекст | см. `13_`, `14_` лана | `A1` | по лану |
| FP-115 | Д. А. Карсон (ed.), *The Glory of the Atonement*?; D. Carson, «The Scope of the Atonement» (in *From Heaven He Came and Sought Her*, 2013) | пятипунктный «ответ»: обязателен, чтобы реестр не стал эхом | `C` | Crossway 2013, ed. D. J. Tidball//? — установить точных редакторов/страницы; **покупка** (очередь Q-115) |
| FP-116 | Ф. Ф. Брюс, *The Epistle to the Hebrews* (NICNT, Grand Rapids: Eerdmans, 1964), на Евр 2:9 | «τῷ θανάτῳ γεύσεται ὑπὲρ παντός» читается без ограничения — экзегеза, на которую опирается всеобщность, у автора вне лагеря | `C` | установить страницы заметки к 2:9; очередь Q-116 |
| FP-117 | Л. Моррис, *The Apostolic Preaching of the Cross* (1944; 3-е изд., London: Tyndale Press, 1965) | обязательный контрастный разбор λύτρον/ἱλαστήριον: у Морриса «за всех» — не объём намерения | `C` | страницы глав о λύτρον и о 1 Ин 2:2 (изд. 1965, переизд. IVP 1996); очередь Q-117 |
| FP-118 | глава в *From Heaven He Came and Sought Her* (2013), посвящённая пуританской/«гипотетической» линии (Бакстер и др.; автора установить по оглавлению) | коллективный пятипунктный ответ: именно там оппоненты сами формулируют, что они отвергают у четырёхпунктников | `C` | получить оглавление и страницы; **покупка**; очередь Q-118 |
| FP-119 | «Современные»: Ken Keathley, *Salvation and Sovereignty: A Molinist Approach* (Nashville: B&H Academic, 2010) | «middle knowledge» — **четвёртый** путь в вопросе объёма, отсутствующий у Прокопенко | `C` | заглавие/изд-во сверены (упоминание в списках SEA); страницы — очередь Q-119 |
| FP-120 | Г. Р. Аллисон, *The Christian Faith: A Systematic Theology* (Grand Rapids: Zondervan, 2021), гл. об искуплении | «unlimited atonement» в современной баптистской систематике | `C` | установить страницы; очередь Q-120 |

## 12. Русскоязычный слой: что реально есть на русском

| id | носитель | что утверждает ровно | класс | локатор / что нужно для повышения |
|---|---|---|---|---|
| FP-121 | А. Прокопенко, «За кого умер Христос?» (статья; PDF на Drive: `1ZlmUe1PfCeZFAB2aZjjLcx7R7s3stWQo`, 919 808 байт) | четыре пункта + пара atonement/redemption + «неверный аргумент» | `A1` | разобрана в `01_`, `06_`, `16_`, `18_`, `19_`, `23_`; постраничные привязки с. 23–26, 28–31, 32–36 — в лану |
| FP-122 | К. Дэниел, *Curt Daniel's?* («Кёрт Дэниел», анализ источников статьи) + «Павловская исповедная формулировка»? | русскоязычный пятипунктный разбор | `A2` | по лану: `13_curt_daniel_source_analysis_and_pavlov_confession.md` |
| FP-123 | В. Дж. Ситон, «Пять пунктов кальвинизма» (рус. пер., reformed.org.ua) | русскоязычная апология 5-го пункта: «универсальное спасение… только в потенциальном смысле» | `B1` | URL прочитан (2009-02-10) — нужно: печатное изд. (Seaton, *A Token for Children*? / *The Five Points of Calvinism*?) |
| FP-124 | Джон Оуэн, «Жизнь через Его смерть» (Мирт, 1999?, 96 с., ISBN 978-5-88698-349-0? — в карточке 978-5-88869-349-0) | **сокращённый пересказ** «Смерть смерти»: русскоязычный читатель получает *обезвреженный* первоисточник оппонента | `A2` | equalibra.org + gracetime.ru + legere.ru (описания совпали); нужно: сверка с Goold X и с полным переводом, если он существует — **это сюжет «деградации» позиции, а не только «спора»** |
| FP-125 | Дж. Мюррей, *Redemption Accomplished and Applied* (1955; рус. перевод в корпусе — права и публикация под HOLD) | противоположная сторона: «искупление совершено определённо и применено ко всем избранным» | `A1` | по корпусу: `ИСКУПЛЕНИЕ/08_MURRAY_RAA_SOURCE_CARD.md`, `ИСКУПЛЕНИЕ/09_MURRAY_RAA_INTAKE_AND_COMPLETENESS.md`, `ИСКУПЛЕНИЕ/10_MURRAY_RAA_ARGUMENT_MAP_PRIVATE_STUDY.md` (RIGHTS_HOLD + PUBLICATION_HOLD) |
| FP-126 | Русские баптисты 1917–1929 (вопросы об искуплении) | линия «всеобщности» без кальвинистской рамки | `A2` | по лану: `14_russian_baptist_historical_theology.md` + `ИСКУПЛЕНИЕ/nt`,`ot`? — нужно: указатели |
| FP-127 | **Поиск «кто ещё в русскоязычье держит четыре пункта» (2026-10-23, две поисковые сессии)** | дополнительных авторов не найдено: полемика в Рунете ведётся на английском первоисточнике (TMS/Принстон) и на статье FP-121 | `B1` | зафиксировано как **измерение отсутствия**, а не как «их нет»; пересъём: `web_search` с тем же запросом + расширение на украинский/польский |

## 13. Обязательная оппозиция (без неё «масса» — агитка)

| id | носитель | что утверждает ровно | класс | локатор |
|---|---|---|---|---|
| FP-128 | Дж. Оуэн, *The Death of Death in the Death of Christ* (1647; Goold X (1850), лист = стр. + 16) | трилемма; «уплата → освобождение» | `A1` | по корпусу `14_` (CCEL TXT chunks 70–90; 1 Тим 2:4 = с. 343; 2 Пет 2:1 = 362–363) |
| FP-129 | Кан. Дорта II + *Rejectio* (Scott 1841, с. 282–292; англ. 1840; латынь у Шаффа, chunk 165) | «достаточно для всего мира; намерение — спасти только избранных» | `A1` | по корпусу `13_`, `15_`, `16_` |
| FP-130 | Р. Nicole, «The eternality of the atonement?» / *Brief Survey on the Controversy on Universal Grace (1634–1661)* | лучшее пятипунктное изложение Сомюра (и потому — обязательный свидетель) | `A2` | monergism.com (текст доступен); нужно: печатное (in *Tracts*, P&R 2002?) |
| FP-131 | R. C. Sproul? — *Chosen by God*? / «four-point is impossible» (по рус. пер. Шаффа: «должен верить в ограниченное искупление») | критерий «логическая убедительность» | `C` | зафиксировано в рус. пер. статьи о кальвинизме (frwiki mirror) — нужно: Sproul, *Chosen by God* (Tyndale 1986), глава; очередь Q-131 |
| FP-132 | Дж. Пакер, А. В. Вуд (внешние списки четырёхпунктников называют их без полного объекта) | не проверено по их текстам: у Пакера нет места, где «четыре пункта» названы его позицией | `C` | очередь Q-132 |
| FP-133 | Г. Уинс? / W. Cunningham, *The Theology of the Old and New Testories condensed*? (2 vol., Edinburgh 1855/1862?; *Historical Theology*) | «the doctrine of the extent… not to be denied» — пятипунктный историк, чей список цитируют обе стороны | `C` | установить издание и том; **важно**: у него есть разбор Сомюра; очередь Q-133 |
| FP-134 | Boettner, *The Reformed Doctrine of Predestination* (1928/1949?; глава «Limited Atonement») | сам признаёт: «The meaning might be brought out more clearly if we used the phrase *Limited Redemption* rather than *Limited Atonement*» | `B1` | перепечатка главы: the-highway.com/atonement_Boettner.html — нужно: страницы изд. P&R 1962?, с. 199? |
| FP-135 | *From Heaven He Came and Sought Her: Definite Atonement in Historical, Biblical, Theological, and Pastoral Perspective* (Wheaton: Crossway, 2013; ed. D. J. Tidball, T. S. Schreiner, M. A. Thomas) | коллективный ответ «четыём пунктам» (в т. ч. гл. Г. Уильямса о Бакстере/Оуэне) | `A2` | заглавие/изд-во — по `22_` 41m? и по упоминаниям в лану (`reformedbaptistblog` цитирует полемический ответ на с. 235/265? — нет, это Аллен); нужно: том целиком (покупка) |

## 14. «Ложные друзья»: списки, которые не выдерживают проверки

Здесь собрано то, что **приписано** позиции партизанскими роллами, но либо опровергнуто, либо не подтверждается. Это и есть ответ на «максимально объективно»: не список героев, а аудит списка.

| id | приписываемый носитель | на каком основании приписан | состояние проверки | класс |
|---|---|---|---|---|
| FP-136 | Джон Буньян, *Reprobation Asserted* (1674) и *The Doctrine of the Law and Grace Unfolded* (1659) — приписывание ему «всеобщего искупления» | **картина не та, что в README**: в спорном трактате есть прямое «за всех» — «the death of Christ did extend itself unto them [the reprobate]… the offer of the Gospel cannot… be offered any further then the death of Jesus Christ doth go» (с. 130 сн. 24), но авторство трактата оспаривается (John Brown считал его псевдоэпиграфом), а в несомненных текстах Буньян держит «died for all his Elect» | `C` | первичное исследование: *The Baptist Quarterly* 21:3 (biblicalstudies.org.uk/pdf/bq/21-3_126.pdf), с. 126–130, сн. 21–27; издания трактата — IA (24 с.) / Chapel Library (30 с.), и Offor I (Glasgow 1854) по `22_` №27–28. **Отдельный дефект, который надо закрыть**: README лана (п. 15) обещает опровержение «грубейшей ошибки о всеобщем искуплении у Буньяна» в `15_patristic_and_reformation_misattributions.md`, а имени Буньяна в этом файле нет (проверено grep'ом 2026-10-23) |
| FP-137 | Джонатан Эдвардс, Эндрю Фуллер, С. Чарнок, Дж. Хау, Г. Суиннок, И. Уоттс | тот же ролл (FP-97) | для Фуллера ланом проверено обратное: частность в намерении (`01_` §3.1.2, раунд 8; `34_` S57 p. 710). Остальные — **не сверены** | `B2` (Чарнок/Хау/Суиннок/Уоттс — очередь Q-137) |
| FP-138 | Кальвин | ролл + `15_`/`13_` | лан показывает: у Кальвина «за всех» в *другой* связке; «четырёхпунктность» Кальвина — позднейшая конструкция (`01_` §3.1.2 раунд 8: Richards 1846 = источник пастиша) | `A1` |
| FP-139 | М. Лютер, У. Цвингли, З. Урсин | ролл (FP-97) | конфессиональный слой (FP-27: Formula of Concord) не равен «гипотетическому декрету»; нужно разбирать по локаторам | `B2` |
| FP-140 | Дж. Э. Мейхью, Дэвид Брейнерд, «Erskine Mason», Дж. Престон | ролл | Престон — единственный, кого подтверждает современная историография (FP-104); остальные — не проверялись | `B2` |
| FP-141 | К. Барт (как «четырёхпунктник») | внешние списки | **неверная рамка**: у Барта универсализм онтологический, без гипотетического декрета (FP-84) | `B1` |
| FP-142 | Шедд как «четырёхпунктник» | внешние списки (из-за пары atonement/redemption) | ланом показано: Шедд — пятипунктник с лексической парой (FP-95); сам Шедд: *Dogmatic Theology* II.469–470 — по лану: `34_` §4.36–4.39 | `A1` |
| FP-143 | Топлэди как носитель «limited atonement» | сноска Стьюарта в статье | проверено: «limited **redemption**» (1769), `34_` §4.37 | `A1` |
| FP-144 | «Дорт осудил новоанглийскую школу» | популярный ход | анахронизм; `34_` §4.38–4.39 | `A1` |
| FP-145 | «Все “умеренные кальвинисты” держат безусловное избрание» | роллы | опровергнуто: Thiessen 1949, Geisler — избрание по предведению; Аллен — некальвинистская позиция SBC (по лану: `34_` §5, список «Недопустимо», запись раунда 5 с отметкой `LOCATOR_HOLD`) | `A1` |
| FP-146 | «Объём искупления — вопрос не издревле спорный» (Lightner, FP-91) | авторитетная монография | **опровергнуто по форме** §2 этого файла: 850-е гг. — спор с тремя вопросами (FP-10), Квирзи 853/Тюзея 860 (FP-15, FP-16), и на Квирзи опирается CCC 605 (FP-71) | `B1` |

## 15. Списки-источники (roll-call как жанр): что с ними делать

| id | список | где напечатан | как использовать | класс |
|---|---|---|---|---|
| FP-147 | Ролл Генри Смита (≈25 имён) | *God's Method of Salvation* (1908), с. 361; перепечатки | как **свидетельство о самосознании партии**, а не об учении; каждый номер — отдельно в §14/§16 | `B2` |
| FP-148 | Ролл А. Г. Стронга | Strong, *Systematic Theology* (1907) — проверен ланом в раунде 8 (`01_` §3.1.2) | уже частично опровергнут: Griffin 1819, Fuller 1803, Richards 1846 | `A1` |
| FP-149 | «Список Стронга» в пересказе у Прокопенко | `01_` §3.1.1–3.1.2 (раунды 7–8) | сверен с текстом: у Стронга *limited atonement* отнесено к лагерю противников | `A1` |
| FP-150 | Списки современных агрегаторов (Wikipedia *Unlimited atonement*; SEA-category «Four-Point Calvinism»; bible-fundamentalist «Men Who Believed…») | онлайн-страницы, зафиксированы 2026-10-23 | как **навигация** для очереди §17, не как улики | `B1` |
| FP-151 | Четырёхсторонник (Four Views, FP-111) + Bird/Harrower (FP-105) | 2016, 2023 | лучший «объективатор»: там оппоненты представлены сами за себя | `A2` |

## 16. Эволюция или деградация: что видно из массы (не вердикт, а описание)

1. **III–VI вв.:** вопроса нет; есть «за всех» без юридической механики (FP-01…FP-06).
2. **849–860:** вопрос появляется **в связи с предосуждением**, а не с искуплением: «Квирзи» даёт формулу, которая через 1130 лет станет цитатой ККЦ (FP-15, FP-16, FP-71). Это колыбель позиции.
3. **Средневековье:** изобретается *различение*, на котором позиция будет жить (Lombard, FP-18) и которое уже у Фомы работает на «достаточность без эффективности» (FP-19).
4. **1618–1661:** Сомюр превращает различение в **декрет** (FP-41…FP-53) и за это получает лексический запрет (FP-51) и канон (FP-52). Здесь — точка, после которой «четыре пункта» становятся партией.
5. **1617–1690:** английская линия (Ушер, Давенант, Престон, Холл, Бакстер, Goodwin; и академический «general redemption» 1690-х, FP-54…FP-70) — **независимое** рождение той же схемы; современная историография требует называть её «английский гипотетический универсализм», а не «амирольдианством» (FP-104, FP-106). Это и есть ответ «не только Прокопенко»: у позиции есть *две* родословные, континентальная и британская.
6. **1785–1826:** в Америке схема превращается в **словесную пару** (atonement/redemption) при сохранении пяти пунктов, с самоназванием «limited redemption» (FP-85). Это деградация *в риторике* и одновременно рождение *терминологии*, которую статья XX в. унаследует без истории.
7. **1831–1996:** Шотландия переносит вопрос из декрета в **природу искупления** (Кемпбелл, FP-99), XX в. — в **онтологию** (Торренсы, FP-100, FP-103) и в **бартианство** (FP-84), где «всеобщность» уже не нуждается в гипотетическом декрете. То есть позиция трижды меняла критерий, сохраняя лозунг.
8. **1908–2023:** евангельско-фундаменталистский и баптистский лагеря переводят спор в **экзегетический** (Лайтнер FP-91, Аллен FP-110, Эриксон FP-108, Аллисон FP-120) и в **апологетический** («евангелизация невозможна без всеобщности», FP-91, FP-110), а современная реформатская академия — обратно в историко-догматический (FP-105, FP-106).
9. **Русскоязычная среда (2000-е — 2020-е):** носитель позиции — почти исключительно *одна статья* (FP-121), оппоненты — переводы (FP-123…FP-126). Отсутствие массовости в Рунете — не аргумент, а данные о состоянии среды (FP-127).
10. **Итог для корпуса:** «четыре пункта» — не одна позиция, а **четыре разных** (сомюрская декретная, англиская ломбардистская, хопкинсианская лексическая, шотландско-бартианская онтологическая), которые ссылаются друг на друга как на одну. Разбор статьи Прокопенко потому и требует этой массы: чтобы задать вопрос, *в каком именно из четырёх смыслов* она держит позицию (по `34_` — ближе всего к давенантовскому *pretium pro omnibus* и к хопкинсианской лексике, а не к Сомюру).

## 17. Очередь добычи (Q-…) — закрытый список, синхронный с классом `C`

**Связь жёсткая: `Q-nn` существует тогда и только тогда, когда `FP-nn` имеет класс `C`; номера совпадают. Проверяет это гейт (правило 23), а не моя аккуратность.**

- Q-02 — Проспер, *Liber sententiarum*: PL 45, столбцы и номер главы о «voluntas omnium».
- Q-04 — Faustus of Riez, *De gratia*: изд. Consolati (CC?), кн. I–II, о всеобщности благодати.
- Q-05 — Ориген, *Commentariorum series in Ioannem* / in 1 Tim: GCS 10 (Etzold 1905–08) + лат. Руфин (CCL 29?).
- Q-11 — Ратрамний, *De prædestinatione*: точное издание (PL 121?; *Corpus Christianarium*? / Marot 1655?).
- Q-12 — Пруденций Троаский: *Epistola*/*Contra Ioannem Scotum*, PL 115? / изд. (MGH?).
- Q-13 — Флор Лионский: *De prædestinatione*, PL 119?; сверить с Gumerlock-аппаратом (FP-08).
- Q-18 — Пётр Ломбардский, *Sententiæ* III: Quaracchi 1916, различь d.20 — где именно «sufficiens/efficax».
- Q-19 — Фома Аквинский: Leonina, *ST* III q.48; *In I ad Tim.* c. 2 lect. 2 (страницы).
- Q-20 — Бонавентура, *In III Sent.*: Quaracchi IX (1885), d.15–16.
- Q-21 — Г. Биель, *Collectorium* III: изд. (Heide? 1570/1574?) + Oberman (2001) страницы.
- Q-22 — Брэдвардин, *De causa Dei* III: изд. (Basel 1571?; London 1715?) — локатор о предопределении и объёме.
- Q-23 — Григорий Риминийский, *In I Sent.*: Venice 1579–81 — различь о «hypothetical necessity? ».
- Q-24 — Эразм, *Annotationes*/*Paraphrasis* в 1 Тим: *Opera omnia* Le Clerc VI (1705), страницы.
- Q-25 — Лютер, *In Galatas* 1535: WA 40 II, лист/строка о «pro me / pro omnibus».
- Q-26 — Меланхтон, *Sententiæ* 1539/1543 и *Loci* 1559: *Corpus Reformatorum* (Bd. 9? / 2?), колонки.
- Q-29 — Бренц/Андреэ: *Judicium de…?*, *De iustitia fidei*? — изд. и страницы о всеобщности.
- Q-30 — Хемниц, *Examen* (tract. de iustificatione): изд. Decker/Rudelbach, колонки.
- Q-31 — Герхард, *Loci* (locus de prædestinatione): Harms-изд. (Berolini 1879–83), том/колонка.
- Q-33 — Confessio Gallicana / II Helvetica: артикулы о всеобщности; изд. Шафф, *Creeds* III (страницы).
- Q-34 — Арминий, *Declaration of Sentiments*: Bagnall-перевод (1853; Baker repr.) — страницы 19-й тезисной статьи.
- Q-35 — Ремонстрация 1610, Артикул II: лат. оригинал (изд. *Acta*? / van der Vorst?) — сверить точную формулировку.
- Q-37 — Эпископий: *Confessio* 1627/1629 + *Voorredeneke* — изд. и страницы.
- Q-38 — Крелл: *Responsio*/*De satisfactione* — название, год, страницы.
- Q-39 — Лимборх, *Christian Theology* (англ. 1693/1713?) — книга/глава о искуплении.
- Q-41 — Кэмерон: *Theses de triplici foedere* (1618) + *Praelectiones* — изд., страницы.
- Q-43 — Амираут, *Echantillon* 1637 — экземпляр (BNF/Gallica), страницы с «за всех».
- Q-44 — Амираут, *Traicté de la justification* 1638 — экземпляр + страницы.
- Q-45 — де ла Плас: его трактат об опосредованном вменении — установить заглавие (Nicole сн.) + *Acta* Charenton 1645 / Loudun 1659 (Aymon II, pp. 183, 298).
- Q-46 — Каппель, *Arcanum punctationis revelatum* (1624) — страницы,relevant для «вербального» основания.
- Q-47 — Дайе: *Responsio*/*Tractatus de…?* — установить заглавие/год.
- Q-49 — Риве: неопубликованное опровержение (Библиотека Лейдена? *Epistolæ*? / изд. Nicole) — страницы.
- Q-50 — Тестар: сочинения? — установить (Nicole, Aymon).
- Q-53 — Амираут, посмертные трактаты (Amst. 1670-е) — библиография (Шафф сн. 919).
- Q-57 — Давенант, *Tractatus de arbitrio Dei et hominis*: изд. (London 1659?; *Opera omnia* 1678/1679) — страницы.
- Q-58 — Престон: *Works* (London 1634?), где «all / condition» — установить труд.
- Q-59 — Дж. Холл: *Works* (Oxford 1837; ed. Whittie) —Disputation? / *Residences* — страницы.
- Q-63 — Гудвин, *Redemption Redeemed* (1651) + *Works* — страницы о цене за всех.
- Q-64 — Нее: *Minutes of the Westminster Assembly* (Mitchell–Struthers 1874) — страницы возражений о всеобщности.
- Q-65 — Чиллингворт, *The Religion of Protestants*: изд. (London 1637; ed. Gadue 1853?) — страницы.
- Q-66 — Дж. Тэйлор: *Liberty of Prophesying* + *Works* (Heber, 1828–30) — страницы.
- Q-67 — Дэвид Уильямс / Фома Чонси и «the General Redemption controversy» 1690-х: Williams, *A Defence of Gospel-truth* (London: John Dunton, 1693; EEBO-TCP A66344): установить издание и страницы места; до этого строка не имеет права повышаться до `A1` (строка реестра FP-67).
- Q-69 — С. Уэсли: *Life and Times* (Project Gutenberg 67980) — глава/страница эпизода 1693 г.
- Q-70 — Калами: *Abridgement* (London 1709/1713) — страницы по «general redemption» и *Heads of Agreement*.
- Q-73 — Уитби: точное заглавие и год (*A Discourse on the Five Points*? 1710/1720?) + страницы.
- Q-74 — Тиллотсон: *Works* (1752; Life by Johnson) — страница «universal redemption».
- Q-75 — Локк: *Reasonableness* (ed. Yolton? / Thomas 1997) + *Paraphrase on Romans* — страницы.
- Q-78 — Уитфилд: *Works* / *Journal* — страницы ответа.
- Q-79 — Мильтонова *Doctrina Christiana* кн. VI: CPW VI (Columbia UP 1953–59) — страницы.
- Q-80 — Эрквин: заглавие/год/изд-во *Unconditional Freeness* + страницы.
- Q-81 — Уордлоу: *Balances?* (Glasgow 1817?) — страницы о Кемпбелле? (уточнить, что именно он ему отвечал).
- Q-82 — Ричль: англ. пер. (Edinburgh 1900–03), том/страницы о всеобщности.
- Q-83 — Гарнак: *GCS N.F. 1*? / англ. 1891 — страницы.
- Q-84 — Барт: *KD* IV/1 (§§59–60), *CD* ET (T&T Clark 1956) — страницы.
- Q-86 — Барнс: *Notes* (1837–?) на Рим 3:25, Евр 2:9 — страницы.
- Q-87 — Муди: *Sermons* (1881/1883?) — проповедь о «whosoever», страницы.
- Q-88 — Торрей: *What the Bible Teacheth* (1898/99) — глава об искуплении, страницы.
- Q-89 — Чафер: *Systematic Theology* vol. VI (*The Work of Christ*?) — страницы о «provision for all».
- Q-90 — Уолворд: установить заглавие/журнал/год статьи об объёме.
- Q-91 — Р. Лайтнер, *The Death Christ Died: A Case for Unlimited Atonement* (Des Plaines: Regular Baptist Press, 1967, 151 s.) → изд. перераб. *…: A Biblical Case for Unlimited A: установить издание и страницы места; до этого строка не имеет права повышаться до `A1` (строка реестра FP-91).
- Q-92 — Нььюэлл: *Hebrews: Verse by Verse* (1938/1957) — страницы к Евр 2:9.
- Q-98 — IFCA Doctrinal Statement: дата редакции, где зафиксировано «unlimited atonement».
- Q-99 — Кемпбелл: 1856 Macmillan — страницы гл. I–IV (CCEL HTML по главам; печатные страницы нужны для `LOCATOR_FULL`).
- Q-100 — Дж. Б. Торренс: PDF вступления (afkimel) + библиографические данные диссертации (Princeton, год?).
- Q-101 — Денни: *The Death of Christ* (1902) — глава/страницы; *Studies in Theology* (1894) — глава об искуплении.
- Q-102 — Форсайт: *The Cruciality of the Cross* — страницы.
- Q-103 — Т. Ф. Торренс: *The Mediation of Christ* (1992) — страницы; **без них «всеобщность» Торренса — городская легенда**.
- Q-106 — Муллер: *PRRD* III (2003) — указатель; Мур: установить работу о гипотетическом универсализме.
- Q-107 — Уорр: *Outline* (EPM PDF) + его систематика — держит ли всеобщность сам.
- Q-109 — Демарест: *The Cross and Salvation* — страницы главы.
- Q-111 — *Exploring the Extent of the Atonement: Four Views* (2016) — участники и страницы.
- Q-112 — Лемке: где именно у него разбор объёма.
- Q-113 — Nettleton, *Chosen to Salvation* — изд-во/год/страницы.
- Q-115 — *From Heaven He Came and Sought Her* (Crossway 2013) — редакторы (уточнить), страницы гл. о Сомюре/Бакстере.
- Q-116 — Ф. Ф. Брюс, *The Epistle to the Hebrews* (NICNT, Grand Rapids: Eerdmans, 1964), на Евр 2:9: установить издание и страницы места; без этого строка не имеет права повышаться до `A1` (сформулировано по тексту строки реестра FP-116).
- Q-117 — Л. Моррис, *The Apostolic Preaching of the Cross* (1944; 3-е изд., London: Tyndale Press, 1965): установить издание и страницы места; без этого строка не имеет права повышаться до `A1` (сформулировано по тексту строки реестра FP-117).
- Q-118 — глава в *From Heaven He Came and Sought Her* (2013), посвящённая пуританской/«гипотетической» линии (Бакстер и др.; автора установить по оглавлению): установить издание и страницы места; без этого строка не имеет права повышаться до `A1` (сформулировано по тексту строки реестра FP-118).
- Q-119 — Китли: *Salvation and Sovereignty* (2010) — страницы о middle knowledge и объёме.
- Q-120 — Аллисон: *The Christian Faith* (2021) — страницы главы.
- Q-131 — Спраул: *Chosen by God* (1986) — глава о «четырёх пунктах невозможно».
- Q-132 — Пакер/Гибсон/Моррис/Скотт/Летэм/Беркхоф/Бавинк — уже в `ИСКУПЛЕНИЕ/00_CURRENT_AUTHORITY_2026-10-07.md` §2 («без полного объекта»), сюда только для синхронизации.
- Q-133 — Каннингем: *The Theology of the Old and New Testaments* (2 vol., Edinburgh 1855/1862?) — том/страницы разбора Сомюра.
- Q-136 — Джон Буньян, *Reprobation Asserted* (1674) и *The Doctrine of the Law and Grace Unfolded* (1659) — приписывание ему «всеобщего искупления»: установить издание и страницы места; до этого строка не имеет права повышаться до `A1` (строка реестра FP-136).

## 18. Что этот реестр меняет в корпусе

- Позиция перестаёт быть «статьёй одного автора»: реестр даёт **151 строк** — носители позиции, обязательная оппозиция, ложные друзья и сами партизанские списки как жанр — по 12 эпохам, от III в. до 2023 г.
- Распределение по классам достоверности: `A1` 26 (место прочитано по изданию), `A2` 23 (сверены выходные данные), `B1` 14 (взято из вторичного исследования с локатором), `B2` 6 (приписано, не сверено), `C` 82 (требуется добыча). Числа переснимает обходом гейт (правило 23); расхождение с файлом роняет прогон — приписать себе больше проверенного, чем есть, не выйдет.
- Доля прочитанного по первичному изданию — 17%. Это и есть честный ответ на «максимально объективно»: масса собрана, но 82 позиций из 151 ещё требуют руки и тома.
- `C`-строки и очередь §17 связаны 1:1 по номеру: заявить «массу собрали» нельзя, не закрыв добычу или не сняв строку.
- Три результата, готовых к опровержению оппонентом: (1) тезис «вопрос об объёме возник в XVI в.» не выдерживает IX в. (FP-07…FP-17); (2) у позиции **четыре различные логические формы** (§16) — сомюрская декретная, английская ломбардистская, новоанглийская лексическая и шотландско-бартианская онтологическая, — и упрёк «вы просто четыре пункта» их не различает; (3) найден дефект самого лана: README (п. 15) обещает опровержение атрибуции Буньяна в `15_patristic_and_reformation_misattributions.md`, а имени Буньяна в этом файле нет (проверено grep'ом 2026-10-23), тогда как первичный свидетель (*The Baptist Quarterly* 21:3, с. 126–130) показывает, что «за всех» в *Reprobation Asserted* напечатано — при оспариваемом авторстве трактата. Зафиксировано как FP-136 / Q-136 и в `ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md` §15n.
