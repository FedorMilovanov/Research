# 35. Масса носителей позиции: реестр «четырёхпунктников» и гипотетических универсалистов по всем эпохам

**Созд | индекс прочитан частично: 3 страницы каталога из 16; остальные имена того же периода в строки не разведены — измеренное отсутствие, а не забытьё; названия работ в каталоге не приведены, поэтому выдумывать их я не сталаоппонент всегда мог ответить «вы спорите с частным случаем». Здесь собрано **сколько удалось найти** носителей той же схемы по всем эпохам — от III в. до 2023 г., включая древних, очень старых и совсем новых, — с честной отметкой, что именно про каждого из них **доказано**, а что только **приписано**.
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
| FP-04 | Фавст Риёзский (Faustus Regiensis), *De gratia* (ок. 470–480, кн. I–II) | благодать даётся «всем верующим», предосуждения нет | `C` | изд. A. Consolati, *Fausto di Riez: La Grazia* (1976?), CC Series — уточнить; очередь Q-04 |
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
| FP-33 | Кент? — Символы: *Second Helvetic Confession* (1566), гл. ?; *Gallican Confession* (1559) art. ? | «Христос… умер за наши грехи» без ограничения; вопрос объёма не артикулирован | `C` | Шафф *Creeds* I (тексты есть) — нужно: конкретные артикулы; очередь Q-33 |

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
| FP-41 | Дж. Кэмерон (1580–1625), *Theses de triplici Dei cum hominibus foedere* (Bourges 1618 / Saumur?) | «три завета»: природы, письма, благодати — логический приоритет условного (в формулировке Кэмерона речь о *ordo*, а о временном порядке — нет; сверить латынь по изданию) | `C` | лат. изд. (Geneva 1653? *Praelectiones*?) — уточнить; очередь Q-41 |
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
| FP-56 | Дж. Давенант, *Dissertationes duæ*: prima «de morte Christi, quatenus ad omnes extendatur, quatenus ad solos electos restringatur», altera «de prædestinatione & reprobatione» (Cambridge: Ex Officina Rogeri Danielis, 1650, 245 s.; посмертно) | «pretium pro omnibus» при частности применения; собственная формула — «ordained sufficiency» против «mere sufficiency» | `A2` | латинский текст: изд. 1650, 245 с. (крыло Wing, EEBO-серия 593:11); англ. пер. Дж. Оллпорта, 1831 (приложение к комментарию на Колоссян), сс. 424–425; переизд. Banner of Truth 2005 вышло **без** диссертации — отсюда «невидимость» Давенанта. Цитата 424–425 дана по вторичному (FP-173), том не снят |
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
| FP-76 | Дж. Уэсли, *Explanatory Notes Upon the New Testament* (1755) на 1 Тим 2:6, Тит 2:11, Евр 2:9, 1 Ин 2:2; *Hymns on God's Everlasting Love* (1763); письмо к Р. (1763?) | «general redemption» + предвосхищающая благодать; гимнóлогия как носитель учения | `A2` | *The Works of John Wesley* (Jackson 1872; сверять по BICD — Bicentennial Edition): Notes 1755 — нужны страницы; гимны (Bristol 1763) — нужны; нужно: Pinson, «Wesley on the Nature of Atonement» (*evangelicalarminians.org* PDF) как вторичное |
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
| FP-136 | Джон Буньян, *Reprobation Asserted* (1674) и *The Doctrine of the Law and Grace Unfolded* (1659) — приписывание ему «всеобщего искупления» | **картина не та, что в приписывании Прокопенко**: в спорном трактате есть прямое «за всех» — «the death of Christ did extend itself unto them [the reprobate]… the offer of the Gospel cannot… be offered any further then the death of Jesus Christ doth go» (с. 130 сн. 24), но авторство трактата оспаривается (John Brown считал его псевдоэпиграфом), а в несомненных текстах Буньян держит «died for all his Elect» | `C` | первичное исследование: *The Baptist Quarterly* 21:3 (biblicalstudies.org.uk/pdf/bq/21-3_126.pdf), с. 126–130, сн. 21–27; издания трактата — IA (24 с.) / Chapel Library (30 с.), и Offor I (Glasgow 1854) по `22_` №27–28. **Пересъём навигационного «дефекта» (круг 18): он был ложным.** Круг 16 записал, что разбора Буньяна в `15_patristic_and_reformation_misattributions.md` нет: греп по латинскому имени «bunyan» → 0 вхождений по `15_patristic_and_reformation_misattributions.md`, и этого «0» хватило, чтобы объявить отсутствие. По кириллическому имени тот же файл даёт «Буньян» → 17 вхождений по `15_patristic_and_reformation_misattributions.md`, и §6 «Грубейшая историческая ошибка: Джон Буньян…» (строки 107–143) там есть; «Буньян» → 0 вхождений по `ИСКУПЛЕНИЕ/15_CALVIN_III24_AND_DORT_II_LOCATORS.md` — туда и попал прежний обход. Настоящий пробел — печати: «Banner» → 0 вхождений по `15_patristic_and_reformation_misattributions.md`; локаторы внесены в §20.2 (FP-190: *The Works of John Bunyan*, Banner of Truth, 1991, т. 1, сс. 334, 408–409, 416, 432, 526, 561–562 — читаны в транскрипте с напечатанными страницами), и для таких строк написано правило 24 гейта |
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
11. **1562 → 1650 → 2021:** конфессиональный слой гипотетической воли старше Сомюра на 75 лет и старше Дорта на 56 (FP-152: венгерская *Confessio Catholica* 1562 г. учит «общей внешней спасительной воле» и условному декрету), а спор о том, **покрывает ли Вестминстерское исповедание такую позицию**, идёт и сейчас: Крист (2014, сс. 181–183) и Линч (2017, гл. 5; 2021, с. 85) утверждают, что покрывает, и это не «деградация», а чтение того же корпуса символов с другой инструкцией. ⇒ «четыре пункта» нельзя ни вывести из исповеданий, ни опровергнуть исповеданиями: они спорят о **рамке допустимого** в одном и том же символе (§19.1).

10. **Итог для корпуса:** «четыре пункта» — не одна позиция, а **четыре разных** (сомюрская декретная, англиская ломбардистская, хопкинсианская лексическая, шотландско-бартианская онтологическая), которые ссылаются друг на друга как на одну. Разбор статьи Прокопенко потому и требует этой массы: чтобы задать вопрос, *в каком именно из четырёх смыслов* она держит позицию (по `34_` — ближе всего к давенантовскому *pretium pro omnibus* и к хопкинсианской лексике, а не к Сомюру).

## 19. Масса, добавленная кругом 17 (2026-10-23): индекс первичных цитат и то, что он даёт

**Что это за источник и почему ему нельзя верить на слово.** Английский «индекс первичных цитат»
(`calvinandcalvinism.com`, 16 страниц каталога) — это не библиотека, а карточное собрание выписок с напечатанными
страницами; 3 страницы из 16 прочитаны 2026-10-23, остальные — измеренное отсутствие (FP-172). Строки ниже отнесены по
совести: `B1` там, где названа страница напечатанного издания, `C` — где назван только заголовок. Ни одна строка не получила
`A1`/`A2` «по авторитету сайта»; повышение класса возможно только снятием тома (см. очередь §17).

### 19.1 Исповедания и делегации: то, чего «в символических книгах нет»

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-152 | Реформатская церковь Венгрии, *Confessio Catholica* (Debrecen–Eger, 1562; авторы Péter Melius Juhász, 1536–1572, и Gergely Szegedi, 1511–1569) | «общей и внешней спасительной волей» Бог хочет, чтобы жили все — «и хорошие, и худые»; не исполняется она по несовершенству людей («Я хотел, а вы не захотели», Мф 23:37); рядом — условный декрет | `C` | исповедание 1562 г. с гипотетической волей: нужно снять по печатному переводу (очередь Q-152) |
| FP-153 | «The Collegiat Suffrage of the Divines of Great Britaine, Concerning the Five Articles Controverted in the Low Countries» (Дж. Карлтон, Дж. Давенант, С. Уорд, Т. Год, У. Балканкуолл) | вторая статья: Христос «дал Себя как выкуп за грехи всего мира», при этом «цена уплачена за всех, но полезна/применима не всем»; quinta positio — «в Церкви, где по обещанию Евангелия спасение предложено всем, устроение благодати таково, что достаточно обличает всех некающихся» | `A2` | издания установлены: лат. *Suffragium Collegiale…* (London: R. Young, 1626); англ. пер. (London: Robert Milbourne, 1629); критическое изд. A. Milton (ed.), *The British Delegation and the Synod of Dort (1618–1619)*, Church of England Record Society 13 (Woodbridge: Boydell, 2005), сс. 226–293 (внутренние ссылки вторичных работ: 253, 258, 262–263); транскрипт читан с пагинацией [сс. 44–50], печатный лист 1629 г. не сверен |

### 19.2 Англия и Шотландия XVII в.: новые носители и один сильный анти-ряд

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-154 | Томас Калверт (1606–1679), *Mel Cœli Evangelii: Or, Isaiah's Prophecie of Christ's Passion For Man's Redemption* (London: Tho. Pierrepont, «at the Sun in Pauls Church-yard», 1658), сс. 169–171 | отрицает «aptitudinal, potential, objective, abstracted sufficiency» как ответ: «смотрим субъективно, действительно и формально — с волей и намерением Отца и Сына»; «Христос умер за тех, кто погибнет» — «трудно усвояемо рассудком из Писания»; пометка «Maxime, hypothetica minime est positiva»; внутри ссылки на Voetius, *Disputationes Theologicae*, disp. 2, cap. *De merito Christi* | `B1` | анти-ряд (см. §13): страница указана по индексной перепечатке с помеченной правкой орфографии; том 1658 г. не снят |
| FP-155 | Уильям Лифорд (1598–1653) о достаточности смерти Христа | «индексное заглавие» приписывает ему защиту достаточности смерти «для всех» в рамках ортодоксии; собственного чтения текста у меня нет | `C` | найти работу и сверить по изданию (очередь Q-155) |
| FP-156 | Роберт Эббот (1560–1617) о всеобщности и достаточности искупления Христа | Эббот — автор скандального отказа подписать три статьи о предопределении (1595); индекс приписывает ему «universal and sufficient redemption» | `C` | связать с делом 1595 г. по печатным *Acta* Кембриджа и снять текст (очередь Q-156) |
| FP-157 | Эдвард Лиг (1602–1671), *A Systeme or Body of Divinity*, «Christ died for the reprobate in five ways» | пять способов, которыми Христос «умер за нечестивых»: прокламация (Лк 24:47; Деян 13:38; 10:43), обязательство верить (Мк 1:15) — «you are bound to believe that your sins may be forgiven thee in Christ», запечатление («God has sealed this serious offer in your own Conscience»), общая заслуга (Ин 3:16) и особое намерение «for all that thou knowest» (Деян 8:22); «универсальный» термин 1 Ин 2:2 при этом объяснён как различение народов, а не как спасение всех людей | `B1` | снято 2026-10-23T18:22Z с `calvinandcalvinism.com/?p=13913` (файл-снимок — в Drive `10.9`, см. `driveMirrors.captures20261023b`); в ссылке индексатора — *A Systeme or Body of Divinity* (London: A.M. for William Lee at the Signe of the Turks-head in Fleet-street over against Fetter-lane), 1662, с. 602. **Расхождение, видимое без печати:** тот же отпечаток в EEBO привязан к изданию 1654 (Wing L1008 = ESTC R25452, [28], 873, [19] p., imprimatur Э. Кэламэ 15.06.1653), а 1662 — четвёртое издание по DNB (третье — 1650); лист 602 по титульному развёрсту не сверен, поэтому класс `B1`, а не `A1`. Индексатор отдельно оговаривает, что Лиг не был ни «classic-moderate», ни гипотетическим универсалистом, а пересказывает Феннера (FP-204), — снимать эту строку как английское свидетельство четырёхчленности нельзя |
| FP-204 | Уильям Феннер (1600–1640), о достаточности умилостивления: «Christ died for the reprobate in five ways» — первоисточник лиговой формулы | «Mentiris Cain… Christ died for thy sins, and that in five ways»: те же пять пунктов, что у Лига, но с исходной оговоркой — обязательство верить распространяется на всех без исключения («even reprobate and all, they are bound as well as the Apostles themselves»), общая интенция есть «достаточная цена… even for the reprobate men», но «although I do not say generally, in respect of absolute purpose», особая интенция — «for all that you know»; к этому приложены «Omnia Omnium» Гилария, «сто миров» Экция и ссылка на Фому (I Sent. d.19, q.5, a.1, qu.2, co.) | `B1` | снято 2026-10-23 с `calvinandcalvinism.com/?p=6596` (фрагмент 1 из 3, два других не читаны); ссылка индексатора ведёт на `books.google.com/books?id=RCwJAAAAIAAJ&pg=PA319`, то есть на с. 319 сборника Феннера, а какое именно издание за этим стоит — из перечня его работ (Practicall Divinitie 1650, Hidden Manna 1652, Remains 1657 = EEBO A41123) без титульного листа не выводится. Индексатор называет Феннера «moderate-classic», а Лига — нет, и для §14 это два разных случая: у Феннера формула соединена с различением достаточности и условного приглашения, у Лига она цитируется без исходной оговорки |
| FP-158 | Ричард Мейден (ок. 1591–1677), «The Preface to the Reader» к трактату Уильяма Эмса о подчинённости воли человека воле Божией | предисловие — собственный голос Мейдена, и в нём он (а) отказывается вступать в спор о декрете, (б) утверждает, что обе стороны свободно признают: Бог серьёзно желает спасения всем, кому Евангелие предлагается в служении Слова, и (в) все люди способны к спасению на условиях завета благодати — «if they repent of their sins, and believe in Christ»; различение Дорта об impetration/application он передаёт так: синод отвергает его только в том смысле, где из него выводят равное и безразличное желание Бога | `B1` | снято 2026-10-23 с `calvinandcalvinism.com/?p=14276` (фрагмент 1 из 4); ссылка индексатора — `books.google.com/books?id=FKWOjwhjXsEC&pg=PA428`, то есть с. 428, а издание по титулу не установлено. Заглавие трактата восстановлено по торговой росписи Т. Чайлди (*A catalogue of the most vendible books in England*, London, 1676), где в разделе Эмса стоит «A Treatise, shewing the subordination of the will of man unto the will of God, 8°». **Erratum этого круга:** прежняя строка называла Мейдена «шотландским професором (Абердин/Мерисколл? — не сверено)» — это вывод из сходства фамилий, а не из файла; Мейден — английский пресвитерианский богослов, и шотландская линия (Кэмпбелл, Браун) идёт отдельным прогоном без его имени |
| FP-159 | Стивен Чарнок (1628–1680), семь мест *Works* (тт. 3–5) о смерти Христа | «he hath given him… the world of his elect to redeem» (4:306) лежит рядом с «no creature could pay a sufficient ransom for the sin of man» (4:145), «more value to outweigh the sins of the whole world» (4:251–252), «sufficient bar[ri]ng the sins of the whole world… must have an efficacy for those few that do comply with the terms» (5:96), «the blood shed by the order of God, is able to expiate a world of sins» и «it is a sufficient sacrifice for all, if all would accept of it» (3:425) — пограничный случай: достаточность бесконечна, действенность ограничена «теми, кто принимает условие», а условием является вера, а не декрет; разбор 1 Ин 2:2 у него трёхчастный (верующие всех веков / иудеи и язычники / «whole world in point of the sufficiency of the sacrifice and infinite value of his blood») | `B1` | снято 2026-10-23 с `calvinandcalvinism.com/?p=17` (фрагмент 1 из 16, остальные 15 не читаны — это записано в §21 как остаток, а не как адрес очереди, потому что класс строки уже не `C`); том:страница даны по изданию, которым пользовался индексатор, сверки с титулом не делалось — отсюда `B1`, а не `A1`. Лексика этого места — ближайший предшественник хопкинсианского «пункта 1» (ср. §16 п. 11 о четырёх логических формах) |
| FP-160 | Джон Хамфрей (1621–1719): о смерти Христа; об общей и особой благодати | два трактата, по индексу — защитник всеобщности предложения при частности применения | `A2` | снято начало страницы `?p=4407` (блоки 1 и 2 разобраны, 3–9 не читаны): трактат назван в самой странице под вторым блоком — John Humfrey, *The Middle-Way in One Paper of Election & Redemption, With Indifferency between Arminian & Calvinist* (London: Printed for T. Parkhurst, at the Three Bibles in Cheap-side, 1673), 24–40; тот же отпечаток — в каталоге Folger (№ 488217, собрание *Mediocria*, 1674), где трактат 1673 г. перечислен в составе собрания, — значит, независимое подтверждение есть и класс `A2` по правилу круга 23, а не `B1`. По существу из *Middle-Way*: «I am for a middle Way, as Mr. Baxter was, and Dr. Davenant»; «both universal and special grace together; and the one is Applicatory, not Destructive to the other»; «does make Christ's Redemption a double thing … Salvation for Judas, if he repent … Repentance for Peter»; «there is Gratia universalis simpliciter, which if we maintain not, we must leave our Preaching, and the Gospel»; «The mission or giving of the Spirit … is the fruit or offspring of our Election». По той же странице, под первым блоком, — ссылка на *Free Thoughts* (1710), 8–15, и формулы, которые круг 24 по ошибке записал сюда; они перенесены в `FP-208` (см. §25). Из ловушек этой страницы в строке держатся три: гиперссылка в заголовке ведёт на *Dictionary of National Biography* (Google Books, том 1891 г.), а не на источник цитаты; написание имени книготорговца у индексатора плавает («Parkhust» на одной странице, «Parkhurst» на другой), и сверка по одному написанию даёт ложное «нет совпадений»; поиск по одной фамилии выводит на Пелхэма Хамфрея (1647–1674), придворного композитора-однофамильца |
| FP-208 | Джон Хамфрей (1621–1719), *Free Thoughts upon these heads* (London: T. Parkhurst …; J. Robinson …; sold by J. Morphew, 1710) | то же «среднее» по два фронта, но снятое с другого блока той же страницы и с другим локатором: искупление «одно, но в двойном отношении», и из этого — «все искуплены, и также только избранные»; прощение условное, по аналогии с актом парламента | `A2` | снято с той же страницы `?p=4407`, блок 1, цитата под которым называет *Free Thoughts* (1710), 8–15: «Redemption is but one, though that one may have a double Respect»; «so that in these diverse Respects, all are redeemed, and also the Elect only»; «it is an Inconsistency I cannot fully, but half approve»; «Election takes care that Redemption be not in vain»; «a Universal Conditional Remission … Pardon by an Act of Parliament … The Gospel-Covenant is such an Act of Pardon for all the World; and if you object, then all the World must be saved, I answer, The Act must be read … we find Conditions in it»; «you must not lay it on him, as if he *willed it not*». Отпечаток 1710 г. подтверждён независимо от блога: авторная страница Джона Хамфрея в PRDL (Perry Miller Center) перечисляет *Free thoughts upon these heads* с выходными данными Parkhurst–Robinson–Morphew, 1710, и со ссылкой на скан Internet Archive ⇒ `A2`; `A1` не ставится, потому что листа не читали, а в EEBO-TCP у Хамфрея висит соседний трактат 1679 г., а не этот. Строка заведена кругом 25 для того, чтобы снять эти формулы со строки `FP-160`, где им было не место (см. §25) |
| FP-161 | Джозеф Трумэн (1631–1671), *A Discourse of Natural and Moral Impotency* (London: Robert Clavel, 1675), с. 3, со ссылкой на Твисса | различение естественной и нравственной немощи он называет настолько важным, что без него «учёнейшие отцы и врачи говорят как дети»; саму пару он приписывает «французским протестантским богословам» — то есть сомюрскому ходу, — и указывает, что даже противники в этом пункте прячутся за неё: у Твисса *Vindic. grat.* l. II, *Errat.* 9, *Sect.* 6, p. 211 | `A2` | выходные данные названы индексатором (`calvinandcalvinism.com/?p=14798`, доступ 2026-10-23) и подтверждены двумя независимыми каталожными снятиями одного и того же издания (EEBO A63764: «London: Printed for Robert Clavel, and are to be sold at the sign of the Peacock in St. Pauls Church-yard, 1675») и описанием библиотечного экземпляра; том Трумэна имеет и второе издание с добавками самого автора, поэтому пагинация между оттисками расходится. Отдельная деталь, важная для всякого локатора XVII в.: сам Трумэн свою страницу Твисса пишет как «pag. (_mihi_) 211» — «по моему экземпляру», то есть сверка по листу уже тогда считалась привязанной к конкретному оттиску. Страница 3 самим листом не читана ⇒ не `A1` |
| FP-162 | Джеймс Фрейзер из Бреы (1639–1698): «двойная взыскаемость» как софизм; 2 Пет 2:1 | шотландский пастор, у которого довод «нельзя взыскать дважды» разбирается прямо, и не в пользу пятипунктников | `C` | Fragment 1 из 3 снят 23.10.2026 с `?p=12519`: возражение VIII (Рим 8:32, Ис 53:11) и ответ Фрейзера — аргумент от «inadequate cause», «gave him for us all good and bad… to all elect and reprobate», «you must not say absolutely and merely, because Christ died for a man therefore shall that man be saved»; сама страница печати не называет (последний её фрагмент — только сайдбар), версия *Michod-Kedoshim* не подтверждена, 2 фрагмента не читаны ⇒ очередь Q-162 |

### 19.3 Континент: пиетизм, ортодоксия и то, чего не подтвердил поиск

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-163 | Иоганн Бергий (1587–1658) о воле и желании Бога о спасении всех людей | немецкий пиетизм до Шпенера: «желание спасти всех» у Бехмейрова круга | `B1` | *The Pearle of Peace & Concord. Or A Treatise of Pacification Betwixt the dissenting Churches of Christ* (London: Printed by T.C. for John Rothwell, at the Fountain and Bear in Cheap-side; and John Wright, at the Kings Head in the Old Bayly, 1655), 51–55 — вопросы 52–53 катехизического диалога: «no pleasure in the condemnation of any man», **с оговоркой** «that he will also according to his Justice judge those who despite of his invitation will not hear»; четыре способа действия воли (`voluntate approbante / præcipiente et promittente / operante / non tamen necessitante`) при **неделимом** искуплении. Издание и страницы названы индексатором (Х. Э. Скотт; по титульному листу вторая цифра 1655 вычеркнута и исправлена от руки на «54», немецкий оригинал «about 1635» — дата им же не установлена); вторым, независимым от блога, источником не сверено ⇒ `B1`, а не `A2` |
| FP-164 | Иероним Занки (1516–1590), «Of the Love of God» — главы о любви общей и особой, о благодати, о милости и об условной воле Бога | любовь Божия не равна по адресатам: «he loves not all things with an equal love… the godly then the ungodly»; «God loves all things which he has made besides himself», кроме греха; Ин 3:16 разворачивается у него в два слоя — sustaining/governing and enriching the world, и «gave his only begotten Son, that all which believe in him should not perish» | `C` | текст снят (первый из четырёх фрагментов `?p=4461`; четыре страницы индекса: `?p=4461`, `?p=4475`, `?p=4494`, `?p=4544`), но локатора, годного для класса, это не даёт: индексатор в примечании к своей же странице указывает «pages 370-371, the fifth question», не назвав, к какому изданию эти страницы относятся, а печатная основа под ними — то ли латинская *De Natura Dei* (Geneva, 1577; пять книг, книги II–IV об атрибутах), то ли английский перевод Р. Уинертона *The Whole Body of Christian Religion* (London: John Redmayne, 1659 = EEBO A97309). Строка остаётся `C` ровно для того, чтобы класс не отличался от проверки (очередь Q-164) |
| FP-165 | Пётр Маастрихт (1630–1706) о Кэмероне и Амирауте как «реформатских и православных» | утверждение вторичного индекса: Маастрихт упоминает их **внутри** реформатской ортодоксии; в круге 22 независимый поиск этого не подтвердил, в круге 24 текст найден и подтверждён | `A2` | утверждение вторичного индекса подтверждено текстом и изданием: Peter van Mastricht, *A Treatise on Regeneration* (New-Haven: Printed and sold by Thomas and Samuel Green, in the Old-Council-Chamber, 1770), 37–38 и 46–47 — сняты оба места, и в них действительно «**Some of the Reformed, v.g. John Cameron**, and many others», и «but as to the baptism of *infants*, here **the orthodox are divided** … thus the **celebrated Amyraldus**. But he inaccurately confounds *regeneration* … with *conversion*». Издание сверено независимо: скан Принстонской духовной семинарии в Internet Archive (`treatiseonregene00mast`), пагинация «viii, 9–94, [2] p.» по OpenLibrary и каталожным записям Bowdoin и Bates со ссылками на Evans, Trumbull и ESTC, переиздание Morgan: Soli Deo Gloria, 2002 (под ред. B. Withrow) ⇒ `A2`, а не `A1`: листа не читали. Оговорки держатся в строке: у Эванса год 1769 против титульного 1770; «внутри ортодоксии» значит «назван среди разделившихся и поправлен», а не «одобрен»; латинский первоисточник для `A1` — *Theologia theoretico-practica* VI.iii.757–774, «De Redimendorum Regeneratione» (локатор дан по D. Stanton, *Mid-America Journal of Theology* 29 (2018), лист не снят) |
| FP-166 | Герардус Восс (1862–1949) о детях завета и о разнообразии внутри ранней реформатской традиции | у Восса «diversity» — не либеральная уступка, а часть его учения о завете; именно на него потом опираются и «четырёхпунктники», и их оппоненты | `A2` | работа установлена: «The Doctrine of the Covenant in Reformed Theology» (речь 1891 г. в Богословской школе Гран-Рапидса; англ. перепечатка — R. B. Gaffin (ред.), *Redemptive History and Biblical Interpretation*, Phillipsburg: P&R, 1980, 242–267; пагинация названа вторично, по J. Olinger и разбору CBTS). Снят абзац о детях завета с локаторами самого Восса: Беза *Conf. Christ. Fidei* IV.48, Буллингера *Loci Communes* IV.8.7, Полануса *Syntagma* VI.55. Страница **этого** абзаца не заявлена (перепечатки расходятся), листа не читали ⇒ `A2`, а не `A1` |

### 19.4 XIX–XXI вв.: от шотландских лекций до федерал-визионного спора

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-167 | Арчибальд Александр (1808–1884) против «количественной» эквивалентности в смерти Христа, с разбором Оуэна | качественная vs количественная эквивалентность — та же лексическая вилка, что у Шедда, но у шотландского профессора | `C` | сняты 2 фрагмента из 5 (гл. XVI «The Atonement. 2. Principal Theories of the Sacrifice of Christ»): две «радикально различные и даже враждебные» теории, `solutio ejusdem` у гиперкальвинистов, «This opinion cannot be ascribed to Calvin, who expresses himself in a very general manner», длинная выписка из Оуэна. Печать в странице не названа; отпечаток «The Atonement. London: T. Nelson and Sons, 1868», который стоит под именем Александра в «Works Cited» того же блога, принадлежит А. А. Ходжу (`FP-168`), поэтому поднимать класс по нему нельзя ⇒ очередь Q-167 |
| FP-168 | А. А. Ходж (1823–1886), «The Atonement» (London: T. Nelson and Sons, 1868), сс. 328–329 и 333 — ревизия ломбардской формулы «sufficient for all, efficient for the elect» | вопрос не о достаточности: «no man has ever yet perished, or ever will perish, for want of an atonement», «infinite intrinsic value… no need for him to obey or to suffer an iota more… in order to secure, if God so willed, the salvation of every man, woman, and child that ever lived», и так же у Туллиния, Витсиуса и Оуэна; сама школьная формула «sufficienter pro omnibus, efficienter pro electis» названа «inaccurate and inadequate rather than false», причём автор относит её к Кальвину на 1 Ин 2:2 и к ранним реформатам — до «просеивания» темы французскими богословами (Cameron, Amyraldus, Testardus), а итог формулирует как «the actual ends effected are the exact measure of the real ends designed» | `A2` | выходные данные совпали в двух независимых снятиях: ссылка индексатора (`calvinandcalvinism.com/?p=119`, доступ 2026-10-23T18:35Z) и каталожная запись того же издания (402 p., ред. W. H. Goold; известны также издание 1867 г. и перепечатка 1953 г.). Косвенно подтверждена и пагинация: в оглавлении раздела «The Design or Intended Application of the Atonement» глава II начинается с 328, глава III — с 337, то есть названные страницы лежат ровно внутри. Сам абзац со скана не читан, поэтому `A2`, а не `A1`; снимок текста — в Drive `10.9` |
| FP-169 | Альва Хови (1820–1903) о смерти Христа | баптист из Ньютон-семинарии: различение «достаточности/действенности» в баптистском учении второй половины XIX в. | `C` | не снято (очередь Q-169) |
| FP-170 | Джон Браун (1784–1858): о «universal satisfaction» и о Вестминстерском исповедании; о Кальвине и др. о протяжённости умилостивления | шотландская оппозиция с собственным каталогом «кто что говорил» — самый полный список противников до XIX в. | `C` | каталог не сверен (очередь Q-170) |
| FP-171 | Ральф Уордлоу (1779–1853), «On the Calvinistic Views of the Extent of the Atonement» (Discourse XXIV), *Discourses on the Nature and Extent of the Atonement of Christ* (Glasgow: James Maclehose, 1843/1844) | протяжённость умилостивления он разлагает на три модификации — гиперкальвинизм «точных эквивалентистов», обыкновенно державшийся ортодоксальный кальвинизм и «умеренный, или современный» (Фуллер, Э. Уильямс) — и отвергает первую с той же интонацией, что и сомюрцы: «exact equivalent» измеримо, а значит отрицает бесконечную ценность лица; «pitiful process of commercial reckoning, this weight-and-measure system of atonement» ведёт к тому, что вечная гибель всех была бы большим явлением праведности Бога, чем крест | `A2` | заглавие и издание установлены из двух независимых снятий: список цитируемой литературы у Дж. М. Кемпбелла (*The Nature of the Atonement*, 1884) даёт «*Discourses on the Nature and Extent of the Atonement of Christ*. By Ralph Wardlaw, D.D. Fourth Thousand. Glasgow: James Maclehose, 1844», а библиография самого сайта — то же заглавие с годом 1843; ранее тот же текст вышел как *Two Essays: On Assurance and On the Extent of the Atonement* (Glasgow: Archibald Fullarton, 1831). Страницы индексатор не называет, лист не снимался ⇒ не `A1`; снят первый из 15 фрагментов страницы |
| FP-205 | Б. Х. Кэрролл (1843–1914) о смерти Христа — лексика 2 Кор 5:18–20 без издания в ссылке | вопрос «умер ли Христос за всех или только за избранных» он решает через различение двух примирений: «God was reconciled to us through the expiation of Christ… (2) our reconciliation to God through acceptance of Christ tendered in the ministry of the word»; вывод — «universal or limited salvation is not connected with the atonement Godward, but with the ministry of reconciliation», и «no matter in what sense expiation was effective toward God for all men, it cannot result in universal salvation» | `C` | название книги, из которой снято, индексатор не приводит (фрагмент 1 из 3 на `calvinandcalvinism.com/?p=14969`, доступ 2026-10-23); поиск по характерным формулировкам 2026-10-23 книги не назвал, а у Кэрролла несколько экзегетических курсов, где такая лексика уместна. Очередь Q-205. Побочная польза строки: в этом же фрагменте Кэрролл цитирует Джеймса П. Бойса с точной страницей — см. FP-206 |
| FP-206 | Джеймс П. Бойс (1827–1888), *Abstract of Theology* (переработка F. H. Kerfoot), с. 296 — трёхчастная формула умилостивления | «(1) While for the elect he made an actual atonement, by which they are actually reconciled to God… (2) Christ at the same time and in the same work, wrought out a means of reconciliation for all men, which removed every legal obstacle to their salvation, upon their acceptance of the same conditions upon which the salvation is given to the elect» — то есть в южнобаптистском учебнике XIX в. стоит не «четыре пункта», а умилостивление «фактическое для избранных / обеспечивающее условия для всех» | `B1` | локатор вторичный и точный: страницу называет Кэрролл (FP-205), снимая её с *Abstract of Theology*, «revised by F. H. Kerfoot, p. 296»; какое именно издание (первое 1876 г. или переработка Керфута) имеет эту пагинацию — не установлено, лист не читан, поэтому не `A2` и уж верно не `A1` |
| FP-207 | Фома Мэнтон (1620–1677), «Sermons Upon 1 Peter 1:23» о естественной и нравственной немощи | то же различение, на котором позже стоит хопкинсианская пара, — в английской проповеди 1670-х, и с выводом не в сторону ограничения искупления, а в сторону обязанности увещевать | `A2` | Thomas Manton, “Sermons Upon 1 Peter 1:23,” in *The Complete Works of Thomas Manton* (London: James Nisbet & Co., 1873), 21:332 — «Our *non posse* is *non velle*… The impotence is rather moral than natural… to inform the judgment, awaken the conscience, persuade the will… yet the bare means will not do it without God's concurrence». Отпечаток и страница подтверждены независимо: набор из 22 томов датирован 1870–1875 (Logos/Verbum; скан тома 21 в Internet Archive — `completeworksoft21mant`), а оглавления тома 21 ставят «Sermons Upon 1 Peter i.23» на 299 и следующий блок (Psalm 19:13) на 337, то есть названная страница 332 лежит внутри названного блока; год самого тома в каталогах колеблется (1873 против 1874) — оговорка в строке. Транскрипция вторична дважды: индексатор благодарит за находку чужой блог 2008 г., подчёркивание его ⇒ `A2`, а не `A1` |
| FP-172 | Объединённый «индекс первичных цитат» (calvinandcalvinism.com): 7 страниц из 16 прочитаны 2026-10-23 (круг 21 добавил `?p=13913`, `?p=6596`, `?p=17`, `?p=14276`) | измерение остатка: индекс несёт десятки имён (Пэн, Барли, Фирмин, Полхилл, Сеаман, Шарп, Уодделл, Стеббинс, Райс, Пирс, Мускул, Полян, Вермиль, Урсин, Воэций, Валей, Юний, Олевин, Схильдер, Тил, Шпангейм, Уотс, Гилли? — перечислены по именам каталога), не сведённых в строки | `B1` | списки-источники как жанр (ср. §15): полезны как очередь, бесполезны как улики |
| FP-173 | Оливер Крист, «On Hypothetical Universalism and the Westminster Confession», в *Deviant Calvinism: Broadening Reformed Theology* (Minneapolis: Fortress Press, 2014), сс. 181–183 | современная защита тезиса «ломбардская линия не противоречит символу» — с перечнем имён (Ушер, Престон, Давенант) | `B1` | страницы названы вторичной библиографией; книга не снята |
| FP-174 | Майкл М. Дж. Линч, *John Davenant's Hypothetical Universalism: A Defense of Catholic and Reformed Orthodoxy* (Oxford University Press, 2021), с. 85 | монография, на которую сейчас опирается всё чтение Давенанта: «ordained sufficiency» против «mere sufficiency»; там же разбор У. Каннингема | `B1` | издание и год сверены по каталожным записям; страницу 85 я не читала |
| FP-175 | Майкл Линч, «Confessional Orthodoxy and Hypothetical Universalism: Another Look at the Westminster Confession of Faith», в *Beyond Calvin: Essays on the Diversity of the Reformed Tradition*, ed. B. Littlejohn & J. Tomes (The Davenant Trust, 2017), гл. 5 | редакторская формулировка вывода: если кто-то держит «приобретение только для избранных», но верит, что Христос умер за весь мир иным образом, то (1) он внутри Вестминстерского исповедания, (2) исповедание де-факто это допускает, (3) так, вероятно, и понимали составители | `B1` | цитата редакторов; том 2017 г. не снят |
| FP-176 | Ричард Мюллер: три записи (гипотетический универсализм в реформатской традиции; что Дорт утверждает и чего не утверждает; Амираут) | историографический аргумент, которым прикрывают и «Дорт не сказал», и «Дорт сказал»: у Мюллера — различение *sententia* и обязательности | `C` | томов PRRF в руках не было (очередь Q-176) |

### 19.5 Современный спор, у которого есть адресат, но нет снятой страницы

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-177 | Дуглас Уилсон, «Definite Atonement» (онлайн-статья; интервью в *Christian Renewal*, апр. 2003 — в пересказе той же статьи) | формула: «все православные христиане верят в ограниченное умилостивление: одни ограничивают силу, другие — протяжённость»; «все, за кого Христос умер, спасутся, и Христос умер за мир»; «проблема у тех, кто думает, что обе стороны значат одно и то же слово „за“» | `C` | нужна печатная публикация интервью 2003 г. и страниц (очередь Q-177) |
| FP-178 | Рич Ласк, «The Biblical Plan of Salvation», в E. C. Beisner (ed.), *The Auburn Avenue Theology, Pros and Cons* (Knox Seminary Press, 2004), с. 142 | «пятипунктность как затруднение для „отпадения“» — то же возражение, что у хопкинсианцев 1815 г., в шестом десятилетии XX в. + | `B1` | страница названа двумя независимыми рецензиями; том не снят |
| FP-179 | Стив Вилкинс, Джон Баррах, Стив Шлиссель (Auburn Avenue, 2002–2007) | «вопрос не в том, достаются ли неверующим и осуждённым многие блага от смерти и воскресения Христа; господство Христа всеобщо» — по пересказу интервью 2003 г. | `C` | нет ни одной снятой страницы (очередь Q-179) |
| FP-180 | Сиднейская линия: Брудертон Нокс (1916–1994), «on 'Limited Atonement'» | англиканская лекция, в которой «limited atonement» разбирается как ошибка в формулировке, а не в учении — ближайший современный аналом английской ломбардистской формы (§16.2) | `C` | текста нет (очередь Q-180) |

**Что даёт §19 для §16.** Одна новая линия эволюции: 1562 (венгерский символ, FP-152) → 1618–1619 (английский суфрагий, FP-153) → 1650 (Давенант, FP-56) → 1658 (Калверт как реакция, FP-154) → 1869/1879 (А. А. Ходж о правке формулы, FP-168) → 2002–2007 (федерал-визионный спор, FP-177…FP-179) → 2014/2017/2021 (Крист и Линч, FP-173…FP-175). Это не «деградация» и не «прогресс», а **перенос предмета**: от «за кого умер» к «что покрывает символ». Итог для корпуса прежний: ни один из этих шагов не даёт права ни обвинять Прокопенко в новизне, ни оправдывать его символ — спор идёт в другой рамке.

## 20. Масса, круг 18 (2026-10-23): тот же указатель, снятый целиком, и первичные локаторы XVI–XVII вв.

Круг 17 прочитал 3 части указателя из 16 и вынес из них 29 строк. Круг 18 добирает **саму структуру** указателя
«For Whom Did Christ Die?» (`calvinandcalvinism.com/?page_id=7147`, 4 раздела: I — древняя и средняя церковь, 12 позиций;
II — эпоха Реформации, 36 позиций; III — «вторая Реформация», 33 позиции; IV — постРеформация, 25 позиций; всего **106**)
и шесть страниц, по которым удалось прочитать текст с напечатанным локатором. Классы в этом круге **не повышаются от
том, что цитата красивая**: `B1` здесь означает «ссылка на печатное издание названа вторичным источником, лист не сверен»,
`A2` — «выходные данные совпадают минимум в двух независимых снятиях либо в каталоге издателя», `C` — «печатного текста
нет, есть адрес, куда за ним идти».

### 20.1 XVI век: ломбардистская пара задолго до Сомюра

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-181 | П. М. Вермильи, *Predestination and Justification* (пер. Ф. Э. Джеймса, Kirksville: Sixteenth Century Essays & Studies, назван т. 8, 2003), с. 62; там же с. 16 о значении слова «предопределение» | «Мы охотно это допускаем, если рассматривать только достоинство смерти Христовой: она была **достаточна для грешников всего мира**; но хотя сама по себе её довольно, она не имела, не имеет и не будет иметь действенности во всех людях. Схоластики также признают, что Христос **искупил всех достаточно, но не действенно**» — то есть ломбардистская формула как **собственная** строка одного из учителей второй Реформации, до Сомюра и до Дорта; плюс молиться «о спасении человеческого рода, которое Ты приобрёл милостью Своей» (*Sacred Prayers*, 1994, т. 3, с. 69) и «цена уплачена за весь мир, и если бы она не была дороже всего мира, мир не был бы искуплен» (Philippians-комментарий, *Life, Letters and Sermons*, 1999, т. 5, с. 243) | `B1` | том и серия названы указателем; сверить по титулу (год и нумерация серии расходятся с тем, что я помню о *Sixteenth Century Essays & Studies*), снять печатные страницы |
| FP-182 | Я. Кимедонций (ок. 1550–1596), *The Redemption of Mankind: Three Books*, пер. Х. Инса (London: Imprinted by Felix Kingston, 1598), сс. 4, 7, 12, 13, 14, 26, кн. XI «Who be Redeemed by Christ» | «один Посредник, давший Себя цену искупления **для всех**, как говорит Апостол»; «только Посредник… искупление, умилостивление и спасение **всех людей**»; «Христос по времени умер за нечестивых, но по предопределению — за братьев и друзей» (цитата Бернарда); спор прямо выведен на Лютеранскую конвергенцию в Монбельяре (1586) | `B1` | 1598 г. и печатник названы указателем; латинский оригинал (*De universa hominis redemptione*) и страницы не сверены; читать нужно вместе с FP-41 (Кэмерон) и с §8 |
| FP-183 | Д. Парей, предисловие к четвёртой части Катехизиса, в *Certain learned and excellent discourses…* (London: H.L. for John Royston, 1613), сс. 52–53 | свидетельство современника: Кимедонций «в трактате **о всеобщности искупления**… debating the main question, resolving it very judiciously in his public lectures» — то есть тема «universality of redemption» в английской/немецкой лекционной практике 1590-х уже названа отдельным жанром | `B1` | перевод 1613 г. назван; сверить листы предисловия по экз. (EEBO-копия) |
| FP-184 | В. Музул (1497–1563), *on the Redemption of Mankind* (указатель `?p=237`) и на 1 Ин 2:2 (`?p=260`) | бернский/немецкий слой «за всех» до ломбардистских школ; по заголовку указателя — отдельный разбор «искупления человеческого рода» | `C` | ни названия издания, ни страниц нет (текст указателя не приводит); добыча — по латинским *Opera* (Basel?) |

### 20.2 Англия XVII века: прелат, пролоктор Вестминстера и «грёза» об объёме

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-185 | И. А. Уссер (1581–1656), «The True Intent and Extent of Christ's Death and Satisfaction upon the Cross» и ответ на возражения, в *The Whole Works of the Most Rev. James Ussher*, 17 тт. (Dublin: Hodges, Smith & Co., 1864), т. **12**, сс. **553–560** и **563–571** | различение «satisfaction абсолютно рассмотренная» и «применение к каждому»: «первая совершена за всех, вторая ещё совершается; первая даёт **достаточность, изобилующую на весь долг**, вторая присовокупляет действенность»; «все люди поистине могут быть называющимися имеющими участие в заслугах Христа **как в общем** (as in a common), хотя пользуются плодом не все, потому что не хотят взять»; крайности: «примирение фактически всех до веры» и «никто, кроме избранных, не имеет никакого участия» | `A2` | том, издательство и страницы совпали в двух независимых снятиях (указатель + сноски вторичных обзоров); текст читан в транскрипте, лист 1864 г. не сверен |
| FP-186 | Катехизис Уссера «The Principles of Christian Religion» (1615? по изд.), по изд. А. Митчелла *Catechisms of the Second Reformation* (London: Nisbet, 1886), с. 144 | «Христос… принёс совершенную жертву **за грехи мира**»; «что требуется от человека — принять Христа, **которого Бог свободно предлагает ему**» — катехизический (не трактатный) слой той же позиции, у того же лица | `B1` | Митчелл назван; год и место самого катехизиса (Irish Articles 1615 vs. лат. изд.) не сверены |
| FP-187 | У. Твисс (1578–1646), пролоктор Вестминстерской ассамблеи, *The Doctrine of the Synod of Dort and Arles*, предисловие сс. 15–17; 3.1 сс. 143–144; 3.2 с. 152; 3.3 с. 165 | «мы охотно исповедуем, что Христос имел и полное намерение Своё, и заповедь Отца **совершить умилостивление за грехи всего мира**, чтобы тем приобрести прощение и спасение **всем, кто уверует**, и никому иному в зрелых летах»; «за всех — но не безусловно, а условно, при условии веры»; «Совет Дорта мог это сказать, и всякий слушающий Евангелие обязан верить, что Христос умер за него **в этом смысле**»; «во второй половине — веру и покаяние Он приобрёл не для всех» — то есть **условная** всеобщность из уст того, кто возглавлял Assembly | `B1` | указатель даёт страницы без года издания; снять титул (1630-е?), сверить нумерацию частей |
| FP-188 | Г. Хикман (ум. 1692), *Patro-scholastico-dikaiösis…* (Oxford: Printed by A. Lichfield for J. Adams & E. Forrest, 1659), preface, сс. 40–45 по ручной пагинации транскрипта | **показания очевидца**: «Король Яков понимал эти споры куда лучше, чем мистер П. или я, и именно тогда, когда он посылал своих богословов на Синод в Дорт, чтобы решить против нарождающегося арминианства, **поручил им не отрицать, что Христос умер за всех**, как я сам слышал от епископа Уссера»; Уссер «дал своё суждение доктору Давенанту **за всеобщее искупление**, но прибавил, что есть определённое число тех, кому Бог намерен дать Своего Духа»; «Церковь Англии поддерживает всеобщее искупление всего рода человеческого» + цитата «успокоенного прелата» (с. 103 книги оппонента: примирение «как способные получить прощение в случае веры») | `B1` | 1659 г., печатник и разворот предисловия названы указателем; **у предисловия нет печатной пагинации** — отсылка «40–45» принадлежит транскриптору, и в корпусе её надо цитировать как листы (sig. …), а не как страницы |
| FP-189 | Дж. Оверолл (1559–1619), «суждение о пяти статьях» (указатель `?p=8485`) | то, что Хемптон называет «рукописным мнением Оверолла», которым Давенант пользовался на Дорте и которое перепечатывалось вместе с суфрагием; для корпуса важен сам факт **третьего** английского текста 1618–1629 (помимо суфрагия и диссертаций) | `C` | добыть: латинский и английский листы (1629?) и страницы; в корпусе Оверолла нет ни одной карточки |
| FP-190 | Дж. Буньян (1628–1688), *The Works of John Bunyan* (Banner of Truth, 1991), т. 1: с. 334 («Justification by an Imputed Righteousness»), сс. 408–409, 416, 432 («Light for Them that Sit in Darkness»), с. 526, сс. 561–562 («The Doctrine of Law and Grace Unfolding») | Христос как «**грех мира**», «полное удовлетворение **за грехи мира**», «Тот, кто поверит этому, исповедует Его не так, как квакери» — то есть у Буньяна «за мир» входит в **онтологию замещения**, а не в спор об объёме; ровно то различение, из-за которого ссылка на Буньяна в README лана вела в файл о ложных атрибуциях, где его нет | `B1` | 1991 г. и нумерация томов названы указателем; сверить по экз. Banner of Truth (3 тома, год по титулу); после сверки — кандидат в `A2` |

### 20.3 Континент и делегаты Дорта: то, что обычно забывают

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-191 | У. Цвингли, «on the Unlimited Expiation and Unlimited Redemption» (указатель `?p=52`) | цюрихский слой «неограниченного» до Кальвина; для §16 важно, что рамка «умилостивление/искупление» разделяется и там, где о Сомюре не слыхали | `C` | лат. *Opera* (Schuler/Scrinzer), том/страницы — добыть |
| FP-192 | И. Эколомпидий (1482–1531), «on the Death of Christ» (указатель `?p=23`) | базельский слой; предшественник Кэмеронова круга (никакой связи с Гонди я не утверждаю: текст не снят) | `C` | лат./нем. издания *Opera*; страницы добыть |
| FP-193 | И. Г. Альстед (1588–1638), **делегат от Веттерау к Дорту**, «on the Death of Christ» (указатель `?p=14458`) | оккультно-энциклопедист Альстед как носитель позиции на Дорте — единственная строка этого круга, где «четыре пункта» упираются в **присутствующего** на синоде, а не в его комментаторов | `C` | *Compendium theologicum* (Herborn 1623–1627?) и *Trace the extent* — не снято; добыча обязательна до любого цитирования |
| FP-194 | Р. Роллок (1555–1599), «on the Death of Christ and Related Issues» (указатель `?p=148`) | шотландская школа до Кемпбелла: «related issues» у Роллока = завет и объём, то есть онтологическая форма (§16.4) уже в Эдинбурге | `C` | *Opera* (1618? 1620-е), том/страницы добыть |

### 20.4 Новая Англия и Шотландия XVIII–XIX вв.: «достаточность» как отдельный жанр

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-195 | Э. Калверуэлл (1553/4–1631), «Christ as the Deed of Gift to All Mankind» (указатель `?p=14959`) | «дарственная записка всем людям» — язык **законного основания** дара, а не гипотетического декрета; ближайший английский аналог того, что позже назовут «sufficiency of the deed» | `C` | *A Looking-Glass for sinners*? — название не снято, добыть по каталогу |
| FP-196 | Дж. Престон (1587–1628), «Go Tell Every Man, Christ is Dead For You» (указатель `?p=15421`) | императив проповеди как аргумент об объёме — та же связка, что у Чарнока и у поздней литературы «free offer» | `C` | *Works* (1670-е? 1840-е?), страницы добыть |
| FP-197 | Дж. Хау (1630–1705), «on the Redemption of Christ» (указатель `?p=102`) | неконформистский слой: искупление как «redemption of…», с различением достоинства и применения | `C` | *The Redemption of Christ*? — название/год добыть |
| FP-198 | М. Генри (1662–1714), «on the Universal Redemption of Mankind» (указатель `?p=10733`) | популярнейший комментарий как **носитель** формулы «за всех» вне богословской литературы — то, что в §15 названо roll-call эффектом, работающим наоборот | `C` | *Commentary* (1710-е?), том/страницы на 1 Тим 2:6, Евр 2:9 добыть |
| FP-199 | Дж. Смолли (1734–1820), «on the All-Sufficient Satisfaction of Christ» (указатель `?p=11627`) | «all-sufficient satisfaction» в новоанглийской богословской школе — прямой предшественник лексической пары Хопкинса (§10), и по теме, и по языку | `C` | *Tracts and Essays*? (Хартфорд, 1790-е?) — страницы добыть |
| FP-200 | Р. Балмер (1787–1844), «Mediating Between Two Extremes» (указатель `?p=9595`) | шотландская медиация между «всеобщностью» и «ограниченностью» в 1820-х — локально тот же жест, что у Чалмерса (FP-136?) и за полвека до «неограниченного искупления» у пресвитерианских диссидентов | `C` | *Remarks on the extent of the atonement*? — название/год/страницы добыть |

### 20.5 Агрегаты: что осталось неразведённым, измеренное, а не забытое

| id | носитель | что утверждает ровно | класс | локатор / что нужно добыть |
|---|---|---|---|---|
| FP-201 | Указатель «For Whom Did Christ Die?» (`?page_id=7147`) как **закрытый список**: I — 12, II — 36, III — 33, IV — 25 = 106 позиций | из 106 позиций указателя в реестре стоят 23 строки §20 (из них прочитаны с локатором 6); остальные 83 не разведены — это измеренное отсутствие, а не «мы всё видели». Число **106** взято из самой нумерации разделов (последние номера: 12, 36, 33, 25), а не из подсчёта по экрану | `C` | снять нумерацию по всем четырём разделам и сверить со счётчиком строк реестра (очередь Q-201) |
| FP-202 | Кластер «вестминстерские богословы» указателя: Дж. Уокер `?p=8760`, Р. Вайнс `?p=24`, Г. Скуддер `?p=151`, Т. Форд `?p=8647`, Ф. Раус (мирской ассессор) `?p=…` | у партии Assembly есть **множественные** носители «условной всеобщности», а не один Твисс; ни один из них не снят — поэтому «Вестминстер сказал то-то» в чужих спорах остаётся утверждением без инвентаря | `C` | адресат Рауса в указателе не дочитан (13 частей не просмотрены): добывать адресатом через `?page_id=7147` |
| FP-203 | Кластер 1 Ин 2:2 (`?page_id=7309`): Кальвин с замечаниями Белла `?p=3340`, Н. Харди `?p=1485`, Т. Джайкомб `?p=2204`, У. Беркитт `?p=3024`, Т. Кроуфорд `?p=167`, «1 John 2:2 and the Argument for Limited Atonement» `?p=15807` | стих, на котором держится аргумент «умилостивление не только за наши, но и за всего мира» (1 Ин 2:2), имеет в указателе **12 разборов**, включая анти-ряд; в корпусе локаторов по 1 Ин 2:2 нет ни одного снятого | `C` | снимать постранично; до снятия — не цитировать стих «как аргумент четырёхпунктников» |

**Что круг 18 даёт для §16.** Кривая, которая была в §19 (1562 → 1618 → 1650 → 1658 → 1869 → 2002–2007 → 2014–2021), удлиняется назад и вбок: Вермильи (1562 г. смерти) с **явной** ломбардистской парой, Кимедонций (1598) с трактатом «о всеобщности искупления», Парей (1613) с отзывом о его лекциях, Оверолл и суфрагий (1618–1629), Твисс (1630-е) как пролоктор Вестминстера, Хикман (1659) с показаниями об Уссере и о королевском поручении, Уссер (т. 12, 553–571) с различением «satisfaction/applicatio». Это не «истина постепенно открывалась», а **один и тот же спор в разных институциях**: где-то его ведёт символ (1562), где-то делегация (1619), где-то предисловие к полемике (1659), где-то собрание сочинений (1864).

## 17. Очередь добычи (Q-…) — закрытый список, синхронный с классом `C`

Каждая строка класса `C` обязана иметь адресата здесь, и каждый адресат обязан вести в строку класса `C`: связь 1:1 по номеру,
её сверяет правило 23 (`python3 -B scripts/validate_atonement_corpus_integrity.py`). Порядок — по номерам эпох, а не по срочности:
срочность меняет очередь, а очередь не меняет класса. Круг 18 снял три строки из очереди (FP-153 перешла в `A2` после
установления изданий 1626/1629 и CERS 13) и внёс пятнадцать новых адресов (Q-184, Q-189…Q-203).
Круг 21 снял ещё три адреса (Q-157, Q-158, Q-159 — строки FP-157, FP-158, FP-159 переведены в `B1` после съёма
текстов с `?p=13913`, `?p=6596`, `?p=17`, `?p=14276`), новых адресов не внёс ни одного, потому что ни одна строка
не опустилась в `C`: очередь стала 116.

- Q-2 — Проспер, *Liber sententiarum*: PL 45, столбцы и номер главы о «voluntas omnium».
- Q-4 — Faustus of Riez, *De gratia*: изд. Consolati (CC?), кн. I–II, о всеобщности благодати.
- Q-5 — Ориген, *Commentariorum series in Ioannem* / in 1 Tim: GCS 10 (Etzold 1905–08) + лат. Руфин (CCL 29?).
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
- Q-136 — Джон Буньян, *Reprobation Asserted* (1674) и *The Doctrine of the Law and Grace Unfolded* (1659) — приписывание ему «всеобщего искупления»: установить издание и страницы места; до этого строка не имеет права повышаться до `A1` (строка реестра FP-136) — добавить сверку по *The Works* (Banner of Truth, 1991), т. 1 (FP-190) и переснять греп в обеих азбуках (правило 24): 
- Q-152 — снять *Confessio Catholica* 1562 по: *Reformed Confessions of the 16th and 17th Centuries in English Translation*, vol. 2: 1552–1566 (Grand Rapids: RHB / PTMS, 2013) — документ занимает свыше 200 страниц, нужен трактат о воле Божией с пагинацией; критический текст — *Reformierte Bekenntnisschriften*, Bd. II/2 (Neukirchen-Vluyn: Neukirchener Verlag, 2009). Reception: вытеснена II Гельветическим 1566 (подписана в Дебрецене 1567) — Schaff, *Encyclopaedia of Religious Knowledge*, s.v. «Hungary» (`ccel.org/ccel/schaff/encyc05/htm/iii.xiv.xv.htm`). Пока страница не снята, цитата ходит как вторичная.
- Q-155 — установить, о каком именно сочинении Лифорда идёт речь (индекс: `calvinandcalvinism.com/?p=11907`), снять по EEBO-TCP или по печатному изданию 1650-х, дать страницы.
- Q-156 — сверить с документами Кембриджа 1595 г. (дело Тревора/Эббота: отказ произносить три статьи), затем с его трактатами; индексная запись: `calvinandcalvinism.com/?p=6871`. Класс поднимать только по напечатанному тексту Эббота, не по репутации «первого четырёхпунктника».
- Q-162 — индексы: `calvinandcalvinism.com/?p=12382`, `?p=12406`, `?p=12519`. Снято с `?p=12519` (Fragment 1 из 3, 23.10.2026): возражение VIII с Ис 53:11 и Рим 8:32 и ответ Фрейзера; фрагменты 2–3 не читаны, издания страница не называет. Осталось: установить печать (версия *Michod-Kedoshim* не подтверждена), прочитать остальное, снять по изданию места о 2 Пет 2:1 и о «double payment»; сопоставить с `18_` (двойная оплата) и с ответом Оуэна 1650 г.
- Q-164 — индексы Занки: `calvinandcalvinism.com/?p=4461` (о любви Божией), `?p=4475`, `?p=4494`, `?p=4544`. Снять по *Operum theologicum* (Geneva) тома об атрибутах и о предопределении; индексатор называет страницы 370–371 для пятого вопроса, не называя издания: установить печатную основу (*De Natura Dei*, Geneva 1577, кн. II–IV, или перевод Уинертона *The Whole Body of Christian Religion*, London: John Redmayne, 1659 = EEBO A97309) и снять главы по страницам; только тогда класс `A2`/`A1`, и до этого строка не поднимается, несмотря на наличие текста.
- Q-205 — индекс: `calvinandcalvinism.com/?p=14969` (Кэрролл, фрагмент 1 из 3). Установить, из какой книги снято: у Кэрролла несколько экзегетических курсов и два объёма по искуплению; поиск по формулировкам 2026-10-23 результата не дал. Отдельно — сверка цитаты Бойса (FP-206) по тому изданию *Abstract of Theology*, пагинация которого даёт 296.
- Q-167 — индекс: `calvinandcalvinism.com/?p=12084` (Fragment 1 из 5; прочитаны 0 и 4). Установить название, год и издательство по каталогу: правдоподобный кандидат *The Redemption* (Edinburgh: T. & T. Clark, 1870) **не** подтверждён, а отпечаток «The Atonement, London: T. Nelson and Sons, 1868» из «Works Cited» той же сети страниц принадлежит А. А. Ходжу, не Александру (ср. `FP-168`) — значит ссылка «The Atonement (1868)» без автора в этом корпусе неоднозначна. Прочитать фрагменты 1–3; сверить с `34_` §4.36–4.39 (Шедд).
- Q-169 — индекс: `calvinandcalvinism.com/?p=13542`. Установить название и год по каталогу (индекс их не приводит), дать страницы; в корпусе у Хови нет ни одной карточки.
- Q-170 — индексы: `calvinandcalvinism.com/?p=6438`, `?p=15205`. Снять по *Essays and Characteristic Sermons of John Brown of Haddington*? — установить, где именно напечатаны оба разбора; сверить список «Calvin et al.» с `15_` и с `34_` — это тот редкий случай, когда оппонент даёт нам инвентарь атрибуций.
- Q-176 — индексы: `?p=10963`, `?p=4805`, `?p=139`. Снять по *Post-Reformation Reformed Dogmatics*, vol. III и IV (2nd ed., Baker 2003) и по *Christ's Faith*? — нет: только по PRRF и по *Unsprung Well*, страницы; сравнить с §16.2 и с `27_`.
- Q-177 — тексты: monergism.com «definite_wilson.html»; цитата интервью *Christian Renewal* (апр. 2003) — по вторичному сайту (доступ 2026-10-23), номер/страницы не сняты. Требуется: (1) сам выпуск *Christian Renewal*; (2) печатный том Beisner (ed.), *The Auburn Avenue Theology, Pros and Cons* (Fort Lauderdale: Knox Seminary Press, 2004), 331 с.: ответ Уилсона — сс. 224–232, статья Тревборста — сс. 187–205; (3) решение PCA *Ad Interim Committee on Federal Vision* (2007) о том, что именно вменялось.
- Q-179 — снять: (1) RPCUS «Public Call to Repentance» (июнь 2002) по пункту об умилостивлении; (2) интервью *Christian Renewal*, апрель 2003; (3) том Beisner 2004 целиком по статьям Шлисселя и Барраха; (4) *The Federal Vision*, ed. S. Wilkins & D. Garner (Athanasius Press; год по издательскому листу — сверить): заметка Шлисселя с критикой TULIP — с. 238. Ни один из этих текстов не цитируется в корпусе как улика до снятия.
- Q-180 — индекс: `calvinandcalvinism.com/?p=7623`. Установить, где печаталось (собрание статей Нокса, изданное после 1994 г. (какое именно — установить по каталогу)), снять страницы. Важно: эта строка единственная, где «четыре пункта» возможны в **англиканском** языке XX в. без всякого Сомюра.
- Q-184 — индекс: `calvinandcalvinism.com/?p=237` (о «Redemption of Mankind») и `?p=260` (на 1 Ин 2:2). Установить латинское издание *Opera* Музула (том, год) и страницы; класс поднимать только после чтения листа.
- Q-189 — индекс: `calvinandcalvinism.com/?p=8485`. Добыть латинский и английский тексты «suffragium» Оверолла (1619? / 1629?) с листами; сверить с изданием суфрагия 1626/1629 (FP-153) и с *Grace and Conformity* Стефена Хемптона (OUP, гл. 2), где это «manuscript opinion» названо.
- Q-191 — индекс: `calvinandcalvinism.com/?p=52`. Латинские *Opera* Цвингли (Schuler, 1828–1844; Scrinzer), том и страницы на тему «unlimited expiation»; без этого любая ссылка на Цвингли остаётся ссылкой на заголовок.
- Q-192 — индекс: `calvinandcalvinism.com/?p=23`. *Opera* Эколомпидия (Basel), том/страницы.
- Q-193 — индекс: `calvinandcalvinism.com/?p=14458`. Альстед: *Compendium theologicum* (Herborn, 1623–1627?) и, отдельно, его роль делегата Веттерау на Дорте — добывать по актам синода и по каталогу, не по названию страницы.
- Q-194 — индекс: `calvinandcalvinism.com/?p=148`. *Opera* Роллока (1618? 1620-е?), том/страницы; сверить с §7 и с §16.4 (онтологическая форма).
- Q-195 — индекс: `calvinandcalvinism.com/?p=14959`. Установить название и год (по каталогам ESTC), снять страницы о «deed of gift».
- Q-196 — индекс: `calvinandcalvinism.com/?p=15421`. *Works* Престона (1670-е? 1840-е?), страницы проповеди «Christ is dead for you».
- Q-197 — индекс: `calvinandcalvinism.com/?p=102`. Установить название/год текста Хау, снять страницы.
- Q-198 — индекс: `calvinandcalvinism.com/?p=10733`. *Commentary* Мэттью Генри на 1 Тим 2:6, Тит 2:11, Евр 2:9, 1 Ин 2:2 — том/столбцы по изданию (1710-е; перепечатки расходятся).
- Q-199 — индекс: `calvinandcalvinism.com/?p=11627`. Смолли: установить, где печаталось («Tracts on important subjects of doctrine and duty», Hartford?), снять страницы.
- Q-200 — индекс: `calvinandcalvinism.com/?p=9595`. Балмер: название/год по каталогу (1820-е–1830-е), страницы о «двух крайностях».
- Q-201 — снять нумерацию всех четырёх разделов указателя `?page_id=7147` (последние номера: 12, 36, 33, 25) и развести 106 позиций по строкам реестра; до этого число «106» в FP-201 — по нумерации разделов, а не по перечёту.
- Q-202 — разобрать постранично кластер «вестминстерские богословы» (Уокер `?p=8760`, Вайнс `?p=24`, Скуддер `?p=151`, Форд `?p=8647`, Раус — адресат не дочитан); Рауса id взять из `?page_id=7147`.
- Q-203 — снять постранично кластер 1 Ин 2:2 (`?page_id=7309`: Кальвин/Белл `?p=3340`, Харди `?p=1485`, Джайкомб `?p=2204`, Беркитт `?p=3024`, Кроуфорд `?p=167`, разбор аргумента `?p=15807`).

## 18. Что этот реестр меняет в корпусе

- Позиция перестаёт быть «статьёй одного автора»: реестр даёт **203 строк** — носители позиции, обязательная оппозиция, ложные друзья и сами партизанские списки как жанр, по 13 эпохам и слоям (III в. — 2026 г., включая §19 круга 17).
- Распределение по классам достоверности: `A1` 25 (место прочитано по изданию), `A2` 26 (сверены выходные данные), `B1` 27 (вторичное с локатором), `B2` 6 (приписано, не сверено), `C` 119 (печатного текста нет, есть адрес), а не моя аккуратность.
- Доля прочитанного по первичному изданию — 12%. Масса выросла на 52 строки за круги 17–18, и доля **упала**: это и есть цена «максимальной объективности» — новые имена из индекса первичных цитат пока не тексты, а очередь.
- `C`-строки и очередь §17 связаны 1:1 по номеру (119 = 119): заявить «массу собрали» нельзя, не закрыв добычу или не сняв строку.
- Три результата, готовых к опровержению оппонентом: (1) тезис «вопрос об объёме возник в XVI в.» не выдерживает IX в. (FP-07…FP-17) и теперь не выдерживает и 1562 г. (FP-152: гипотетическая воля в **символе**); (2) у позиции **четыре различные логические формы** (§16.1–16.10), и «четырёхпунктность» Прокопенко ближе к давенантовской и хопкинсианской, чем к Сомюру; (3) из 12 приписываний в §14 и §19 шесть опровергнуты ланом, четыре не подтверждены (Маастрихт FP-165, Лиг FP-157, Эббот FP-156, Чарнок FP-159) — и все они остаются в реестре, а не вычёркнуты.
- Переснять всё: `python3 -B scripts/validate_atonement_corpus_integrity.py` (правило 23 меряет этот файл обходом; числа выше: 203 / 25 / 26 / 27 / 6 / 119).
- Классы в этом реестре теперь отвечает не только за «достоверность цитаты», но и за чистоту самого файла: правило 23 сканирует реестр и корпус на прилипшие CJK-глифы (в круге 16 их было шесть, и ни одно прежнее правило их не видело, потому что склейка кириллицы с латиницей — не то же самое, что иероглиф). Заявленные нули сверяются обходом; ноль — это тоже число, и `x or -1` его съедает.
- Круг 18 (этот заход) измерим тремя числами: **106** позиций указателя «For Whom Did Christ Die?» (по нумерации четырёх разделов: 12 + 36 + 33 + 25) против **23** новые разведённые строки, **6** страниц, по которым текст прочитан с печатным локатором (Вермильи, Кимедонций с отзывом Паррея, Твисс, Уссер, Хикман, Буньян), и **13** частей индекса, которые остаются непрочитанными — они записаны в очередь, а не «забыты». Из них ровно одна строка поднята в `A2` (суфрагий 1626/1629 + CERS 13), потому что там совпали два независимых снятия; повышения «по красоте цитаты» не делалось.
## 21. Масса, круг 21 (2026-10-23): четыре куска указателя, три строки подняты из `C`, одна добавлена, одно обвинение снято с себя

Круг добирает четвёрку страниц указателя «For Whom did Christ Die?», которые круги 18–20 оставляли недочитанными:
`?p=13913` (Лиг), `?p=6596` (Феннер), `?p=17` (Чарнок), `?p=14276` (Мейден); доступ 2026-10-23T18:20–18:21Z. Из них
полностью снята одна (у Лига), у Феннера — 1 фрагмент из 3, у Чарнока — 1 из 16, у Мейдена — 1 из 4.

Ни одна из четырёх страниц не является съёмом с печати, поэтому класс поднят **ровно до `B1`** («вторичное с
локатором»): `A2` требует сверки выходных данных, а её сделать было нельзя — сеть песочницы отдаёт только
каталожные описания, и те из них, что получены, записаны ниже отдельными словами, а не «красивой ссылкой».
Измерение после круга 21, снятое обходом файла, а не памятью: **204** строк-носителей; `A1` 25, `A2` 26, `B1` 31,
`B2` 6, `C` 116; адресатов очереди **116**, связь 1:1 с классом `C` держится (правило 23); доля прочитанного по
первичному — **12 %**.

**Что это меняет в содержании, а не в счёте.** Формула «пяти способов» оказывается не английским изобретением
четырёхчленных, а высказыванием Феннера о *достаточности*, которое Лиг пересказал через сорок лет без исходной
оговорки («although I do not say generally, in respect of absolute purpose»). У Чарнока та же лексика
достаточности собрана в условное приглашение («a sufficient sacrifice for all, if all would accept of it»), а не в
пункт о декрете. Это ровно тот слой, который §16 п. 11 называет «ломбардистской» и «хопкинсианской» формами:
ни одна из трёх строк не говорит, что Христос умер за всех в смысле намерения спасти каждого, и ни одна не
отрицает этого — они держат различение, из которого четыре пункта вырастают позже.

**Erratum круга (против себя).** Строка FP-158 до этого круга приписывала Мейдену «шотландского професора
(Абердин/Мерисколл?)» — вывод из сходства фамилий, а не из файла. Прочитанный текст показывает обратное:
речь об английском пресвитерианском богослове, пишущем предисловие к трактату Эмса, и он сам открещивается от
спора о декрете. Шотландская линия (Кэмпбелл 1856, Браун) остаётся отдельным прогоном, и её строки не должны
ссылаться на Мейдена. Побочный вывод того же съёма: заглавие эмсовского трактата установлено по торговой росписи
Чайлди (London, 1676), а не по титулу, — значит и оно `B1`, а не `A2`.

**Расхождение в библиографии, записанное как расхождение.** Ссылка индексатора на Лига сочетает отпечаток
издания 1654 г. (Wing L1008 = ESTC R25452) с годом 1662 (четвёртое издание по DNB). Пока это не снято с
титульного развёрста, строка не может быть `A2`, и номер страницы 602 в ней читается как «страница того издания,
которое держал в руках индексатор».

**Что осталось от этих четырёх страниц.** У Чарнока 15 из 16 фрагментов, у Феннера 2 из 3, у Мейдена 3 из 4 —
это продолжение съёма того же куска указателя (строки уже `B1`, поэтому в очередь `Q-…` не записывается:
очередь по правилу 23 синхронна классу `C` и служит только для «печатного текста нет»); от Феннера отдельно
остаётся незакрытым издание под с. 319. Снятые тексты лежат файлами в Drive-папке `10.9` (4 штуки, имена с датой
съёма), их id, байты и md5 — в `driveMirrors.captures20261023b`, записи о них — в индексе библиотеки
(`ИСКУПЛЕНИЕ/data/atonement-library-index.json`), и правило 25 сверяет индекс с обходом Drive.

### 21.1. Ходж: XIX век не хранит ломбардскую пару, а перерабатывает её

Та же волна сняла со дна очереди строку FP-168: А. А. Ходж, «The Atonement» (London: T. Nelson and Sons, 1868),
сс. 328–329 и 333. Это единственный случай круга, где класс поднят до `A2`, а не до `B1`: выходные данные
совпали в двух независимых снятиях (ссылка индексатора и каталожная запись тома, 402 p., ред. W. H. Goold), а
пагинация подтверждена структурой оглавления — глава II раздела о намерении и применении умилостивления
начинается ровно с 328.

Смысл находки для §16 и для «эволюции/деградации» в том, что Ходж формулу не повторяет, а чинит: школьная пара
«sufficienter pro omnibus, efficienter pro electis» для него «inaccurate and inadequate rather than false», а
положительное утверждение — «the actual ends effected are the exact measure of the real ends designed». То есть в
американском пресвитерианстве 1868 г. различение ещё держится как слово, но его смысл уже перенесён с
достаточности на число достигнутых целей. Рядом стоит признание, что формулу принял сам Кальвин на 1 Ин 2:2 —
для §13 («что говорят оппоненты») это годная цитата в обе стороны, и её надо давать целиком, а не половинками.

Отдельная зацепка, которая стоит дороже самой строки: в перечне «французских богословов», чьи спекуляции
вызвали просеивание темы, у Ходжа назван Testard (Даниэль Тестар) наряду с Кэмероном и Amyraldus. Это имя в
корпусе раньше не встречалось ни в одном лане, и для сомюрского слоя (§13, §16) оно означает, что перечень
участников меньшею, чем «Сомюр = три имени». Заносить его в очередь строк реестра нельзя (класса `C` у строки
нет), поэтому он записан здесь словом и повторён в тексте PR: следующий круг обязан проверить, есть ли у
Тестара печатное высказывание об объёме удовлетворения.

## 22. Масса, круг 22 (2026-10-23): Уордлоу и Трумэн закрыты по изданию, Кэрролл выделен в отдельную строку, Занки остался `C`

Круг снял четыре страницы указателя: `?p=14798` (Трумэн), `?p=11751` (Уордлоу, фрагмент 1 из 15), `?p=14969`
(Кэрролл, фрагмент 1 из 3) и `?p=4461` (Занки, фрагмент 1 из 4), плюс два каталожных поиска для сверки выходных.

Измерение после круга (обход файла): **206** строк-носителей; `A1` 25, `A2` 29, `B1` 32, `B2` 6, `C` 114;
адресов очереди **114**; доля прочитанного по первичному — **12 %**. Строка FP-171 была разделена: Уордлоу остался
в ней и получил `A2`, а Кэрролл вынесен в новую строку FP-205 с классом `C` и адресом Q-205. Разделение сделано не
для красоты, а потому, что в одной строке нельзя держать два разных уровня доказательности: у Уордлоу издание
названо и подтверждено, у Кэрролла — нет. Третья новая строка, FP-206, — Джеймс П. Бойс с точной страницей
(*Abstract of Theology*, изд. с переработкой Керфута, с. 296), снятой не с листа Бойса, а из цитаты Кэрролла,
поэтому `B1`.

**Что нашли по существу.**

1. *Трумэн, 1675.* Различение естественной и нравственной немощи он прямо приписывает «французским протестантским
   богословам» — то есть сомюрскому ходу — и утверждает, что без него учёнейшие «говорят как дети». Это ещё одно
   свидетельство (§13, §16 п. 11) того, что лексика, на которой позже стоит хопкинсианская пара, в Англии XVII в.
   заимствовалась именно у французов, а не вырастала из собственного грунта. Второе наблюдение — техническое и для
   всего корпуса обязательное: свою ссылку на Твисса Трумэн пишет как «pag. (*mihi*) 211», «по моему экземпляру».
   Семнадцатый век сам признавал, что номер страницы принадлежит оттиску, а не тексту; наш корпус обязан держать то
   же правило, и потому страницы без названного издания у нас не поднимают класс (см. пункт 3).
2. *Уордлоу, 1843/44.* Внутри кальвинизма он различает уже три позиции: гиперкальвинизм «точных эквивалентистов»,
   обыкновенно державшийся ортодоксальный кальвинизм и «умеренный, или современный» — тот, что держат Фуллер и
   Эдвард Уильямс. Отказ от «коммерческого исчисления» («this weight-and-measure system of atonement») у него
   построен на том же основании, что у ломбардистов и у Баркли: ценность умилостивления бесконечна из-за лица
   Страдающего, а значит не измеряется числом должников. Для §16 это значит, что к 1843 г. «четырёхпунктность» уже
   не внешнее обвинение, а классификация внутри самого кальвинизма, и Уордлоу её называет сам.
3. *Занки остался `C`, хотя текст снят, а страницы названы.* Индексатор в комментарии к своей странице указывает
   «pages 370-371, the fifth question» — но не говорит, к какому изданию они относятся, а кандидатов два: латинская
   *De Natura Dei* (Geneva, 1577) и английский перевод Уинертона *The Whole Body of Christian Religion* (London:
   John Redmayne, 1659 = EEBO A97309). Локатор без издания — это адрес, а не доказательство; класс обязан
   отличаться от проверки, иначе `A2` начинает означать «мне поверили на слово».
4. *Кэрролл и Бойс — самое неприятное для рядовой схемы.* Южнобаптистский учебник XIX в. формулирует так: «для
   избранных Христос совершил фактическое умилостивление… и одновременно, в том же деле, приобрёл средство
   примирения для всех людей, устраняющее всякое законное препятствие их спасению при принятии тех же условий».
   Это не четыре пункта в сомюрском смысле и не пять: это протяжённость под условием, встроенная в американский
   баптистский учебник задолго до XX в. Сам Кэрролл при этом переносит вопрос с «умилостивления пред Богом» на
   «служение примирения» — ровно тот же жест, что у Чарнока («if all would accept of it», круг 21) и у Феннера
   («five ways» как способы предложения). Семья условного приглашения, таким образом, тянется от 1640-х через
   1675-е и 1840-е прямо в 1900-е, и её нельзя описать как «отклонение от Дорта»: она держится на различении
   достаточности и применения, которое Дорт сам отверг лишь в одной формулировке (ср. §13 и §18).

**Не закрыто этим кругом:** Занки (4 страницы, издания нет), Восс `?p=14037`, Александр `?p=12084`, Маастрихт
`?p=12944`, Фрейзер `?p=12382`/`?p=12406`/`?p=12519`, Хамфрей `?p=4407`/`?p=4031`, Бергий `?p=5835`, Мэнтон
`?p=12583`. Снятые тексты — четырьмя файлами в Drive-папке `10.9` (записи о них в индексе библиотеки, id — в
`driveMirrors.captures20261023c`).

## 23. Масса, круг 23 (2026-10-23): Бергий и Восс подняты, Александр и Фрейзер остались `C`, найден библиографический «ложный друг»

**Что взято.** Прочитаны и записаны снимками в Drive (папка `10.9`, четыре объекта; байты, md5 и привязка к
строкам — в индексе библиотеки) четыре страницы указателя `calvinandcalvinism.com`: `?p=5835` (Бергий,
вопросы 52–53 — вместе с титульными данными издания), `?p=14037` (Восс, Fragment 1 из 1), `?p=12084`
(Александр, Fragment 1 из 5, прочитаны 0 и 4), `?p=12519` (Фрейзер, Fragment 1 из 3). Итог по классам:
`A2` +1 (Восс), `B1` +1 (Бергий); две строки остаются `C` с переписанными адресами очереди; два адреса
очереди (Q-163, Q-166) сняты вместе с переходом строк в прочитанное, и очередь снова 1:1 с `C` — 112
адресов, и все 112 *уникальны*: дубль `Q-164`, живший в файле с круга 19, слит (см. «Правила», п. 4).

**Что нашли по существу.**

1. *Бергий, 1655.* Лютеранский пиетик середины XVII в. даёт **четырёхчастную** схему действия воли
   (`approbante / præcipiente et promittente / operante / non tamen necessitante`) — и при этом не делит само
   искупление: множится число способов предложения, а не частей цены. Это ровно та конфигурация, которую §16
   называет выводом корпуса, и стоит она вне реформатского спора: к Дорту автор отношения не имеет, а схема
   уже есть.
2. *Восс, 1891/1980.* «Diversity» у Восса — не либеральная уступка, а часть его учения о завете: старая
   теология «proceeded more fearlessly than the later ones in the individualization and general application of
   the promises». Для корпуса ценность двойная: Восс даёт готовую **цепочку первичных адресов** (Беза
   *Conf. Christ. Fidei* IV.48; Буллингера *Loci Communes* IV.8.7; Полануса *Syntagma* VI.55) — по ним реестр
   и обязан идти дальше, — и показывает, что «дети завета куплены кровью Христа» есть тезис, общий для обеих
   сторон спора о числе.
3. *Фрейзер, печать не установлена.* Он принимает силу довода «нельзя взыскать дважды» и ограничивает его
   **условием состояния**: «you must not say absolutely and merely, because Christ died for a man therefore
   shall that man be saved», с эмфазой на «*us*». В том же абзаце — «gave him for us all good and bad… to all
   elect and reprobate». Правило, записанное отсюда: **лозунг без различения способа предикации
   классификационной силы не имеет** — ни «for all», ни «for his people» сами по себе строку между классами
   не двигают.
4. *Александр, книга не установлена.* Глава XVI даёт ту же вилку `solutio ejusdem` / `tantundem`, что и Шедд
   (ср. `34_` §4.36–4.39), и прямо отказывает гиперкальвинизму в авторстве Кальвина. Класс не поднят:
   страница не называет издания, а поиск точной фразы по корпусу ничего не даёт — индексатор модернизирует
   орфографию, и проверять транскрипцию такой фразой бессмысленно.

**Правила, которые ввёл этот круг.**

1. *Каталожное подтверждение обязано быть независимым от транскриптора.* У Бергия есть и титул, и страницы
   51–55, но круг берёт их из одного источника, который цитирует сам себя: в «Works Cited» и «Further
   Reading» того же блога стоит та же строка. `A2` значит «сверены выходные данные», а не «выходные данные
   названы», — поэтому `B1`, и это сказано в самой строке реестра, а не в сноске к ней.
2. *Библиографический «ложный друг».* Отпечаток чужой книги, приписанный нашему автору, — тот же дефект, что
   доктринальный «ложный друг» из §14, только на уровне описания издания, и опасен он именно тем, что
   выглядит как подтверждение. Отсюда обязательная проверка для любого `A2`, взятого из чужого списка
   литературы: **сверять, чьё имя стоит у этого отпечатка в каталоге**, а не то, что строка в списке есть.
3. *Страница статьи не равна странице абзаца.* Локатор «242–267» у Восса относится к статье целиком: он
   поднимает строку до `A2` и не даёт `A1`, потому что `A1` требует прочитанной страницы, на которой стоит
   снятая фраза.
4. *Очередь — множество, а не список, и это теперь проверяется.* Снимая адреса Q-163 и Q-166, круг нашёл,
   что `Q-164` написан в файле **дважды**: короткая строка круга 19 и полная строка круга 22 живут рядом, и
   ни одно число этого не ловило, потому что правило 23 сверяет *множество* номеров очереди с *множеством*
   `C`-строк. Две строки слиты в одну, и в гейт введено **правило 23.2**: у одного номера обязана быть ровно
   одна строка очереди. По-другому «снять адрес, не сняв строку» остаётся невидимым — а именно так и теряются
   улики в длинных списках.

**Правка против себя.** В строке `FP-33` с круга 16 стояло «Xристос» с латинской иксом — тот же дефект, что
«Соumur» в `17_` и что «приоритет条件的ного» в описании лана: при наборе по памяти латинская буква садится на
кириллическое место, и глазами это не видно, потому что слово читается правильно. Исправлено здесь же, где
найдено; скан лана на смешанное письмо пока покрывает `ИСКУПЛЕНИЕ/*.md`, а не `docs/research/atonement/*.md`,
и круг фиксирует это как открытую дыру в проверке, а не как мелочь. **[Поправка круга 25.]** Это утверждение неверно: лан `docs/research/atonement/**` сканируется тем же гейтом как ошибка с круга 22 (правило 22, `_adj22`), а `ИСКУПЛЕНИЕ/*.md` — правилом 23.3. В лане на момент поправки найдено два написания («Xристос» и «Соumur»), оба стоят внутри «ёлочек», то есть легальны по правилу цитат, и блокировать нечего. Ложная строчка убрана и из гл. 07, где она была написана; причины записаны как ошибка проверяющего, а не как снятая угроза: периметр собственной проверки был описан по памяти, а не по коду гейта.

**Не закрыто этим кругом:** Фрейзер (2 фрагмента из 3, печати нет), Александр (3 фрагмента из 5, книги нет),
Маастрихт `?p=12944`, Мэнтон `?p=12583`, Хамфрей `?p=4407`/`?p=4031`, повтор Рим 8:32 `?p=12483`, датировка
немецкого оригинала Бергия и каталожная сверка *Pearle of Peace* (напечатанное 1655 против руки «54» на
титульном листе), и вся латинская линия локаторов Восса (Беза, Буллингера, Поланус) — она следующая. Снятые
тексты — четырьмя файлами в Drive-папке `10.9` (записи о них в индексе библиотеки, id — в
`driveMirrors.captures20261023d`).

## 24. Масса, круг 24 (2026-10-23): два повышения из резерва, одна новая строка и ссылка, которая ведёт не туда

**Что это за круг.** Круг 23 поставил правило: строка поднимается из `C` тогда, когда независимый источник
подтверждает наличие текста в названном издании и на названной странице. Здесь это правило применено к двум
кандидатам, которых круг 23 оставил в очереди, и к одному автору, которого в реестре раньше не было.

**1. Маастрихт, `FP-165`: `C` → `A2`.** Круг 22 закрыл строку отрицательным результатом поиска, круг 23
приказал снять латинский оригинал. Вместо латинского оригинала найден английский: трактат о regeneration в
американском издании (New-Haven: Thomas and Samuel Green, 1770), и в нём стоят оба названных места — «Some of
the Reformed, v.g. John Cameron» (37–38) и «here the orthodox are divided … thus the celebrated Amyraldus. But
he inaccurately confounds regeneration … with conversion» (46–47). Отпечаток подтверждён сканом Принстонской
духовной семинарии и каталожными записями (OpenLibrary, Bowdoin, Bates, со ссылками на Evans, Trumbull и ESTC),
то есть цепочка «страница → книга → экземпляр» замкнута ⇒ `A2`. Выше — нельзя: листа не читали, а сам трактат
есть выписка из «Theologia theoretico-practica» (VI.iii.757–774, «De Redimendorum Regeneratione»); локатор
известен по вторичной статье, и он записан в строку как будущий адрес `A1`. Утверждение, из-за которого строка
вообще появилась, при этом остаётся ровно тем, чем было: Маастрихт называет Кэмерона и Амираута *среди
разделившихся и поправленных*, а не одобрительно; колонка «почему на четыре» теперь говорит это прямо.

**2. Хамфрей, `FP-160`: `C` → `B1`.** Страница `?p=4407` называет трактат целиком, с выходными данными и
пагинацией (John Humfrey, *The Middle-Way in One Paper of Election & Redemption*, London: for T. Parkhust,
1673, 24–40) — по правилу круга 23 этого довольно для `B1`; независимой каталожной записи на это издание найти
не удалось, поэтому `A2` строке не положено. По существу строка получает именно то, что обещала: одно
искупление в двух «respect'ах», «all are redeemed, and also the Elect only», самопризнание «it is an
Inconsistency I cannot fully, but half approve» и встречный упрёк: «Redemption Special does indeed» разрушить
свободу благодати. Держать в памяти: снят Fragment 1 из 9, дальше по странице текст может сказать и
противоположное.

**3. Мэнтон, новая строка `FP-207`: сразу `A2`.** Различение «нравственная немощь вместо естественной» («Our
non posse is non velle … The impotence is rather moral than natural») — ровно то ядро, из-за которого в реестре
держатся строки о Хопкинсе и о формуле «не может ⇒ не хочет». Строка вводится отдельной, а не приписывается
указателю вслепую: проповедь названы том и страница, набор из 22 томов датирован 1870–1875 по каталогам, а
страница 332 проверена *по оглавлению тома*: блок «Sermons Upon 1 Peter i.23» начинается на 299, следующий
блок — на 337, значит названная страница лежит внутри названного блока. Это слабее, чем снятый лист, и сильнее,
чем голое заглавие: отсюда `A2`, но не `A1`. Год самого тома в каталогах расходится (1873 против 1874) —
оговорка записана в строку.

**Ловушка, ради которой этот круг стоит запомнить.** В заголовке страницы Хамфрея висит гиперссылка на
Google Books — и ведёт она не на трактат, а на словарь биографий 1891 года, где Хамфрей просто помянут.
Открой её невнимательно — и в реестр попадёт «подтверждение издания», которого нет. Вторая мелочь того же
рода: книготорговец в странице напечатан «Parkhust», в каталогах — «Parkhurst»; сверка по одному написанию
даёт ложное «подтверждений нет».

**Правила, которые ввёл этот круг.**

1. До `A2` дорастает не только подтверждение отпечатка, но и подтверждение *объёма* названной страницы — когда
   страница попадает в названный блок по оглавлению тома; при одном только названном заглавии это ещё `B1`.
2. Гиперссылка, висящая на единице разбора, — отдельный объект проверки: она ничего не подтверждает, пока её
   адресат не опознан (то же, что правило круга 19 про чужие каталоги, применённое к собственным ссылкам).
3. Имена издателей и годы сверяются во всех написаниях, которые встречаются в источнике; «совпадений нет» при
   одном написании — это результат поиска, а не факт об издании.

**Ревизия круга 23 на этих же основаниях.** §23 обещал снять адрес очереди у `FP-165`, если подтверждение
будет найдено, — снято здесь, задним числом ничего не переписывается: строка §23 остаётся в файле как
отчёт о том круге. Из трёх позиций, которые §23 назвал незакрытыми, закрыты две (Маастрихт и Мэнтон);
остались второй трактат Хамфрея (`?p=4031`), повтор Рим 8:32 (`?p=12483`), латинская линия локаторов Восса,
страницы Фрейзер и Александра и датировка немецкого оригинала Бергия.

**Что в реестре после круга 24.** Строк: 207 (было 206). Распределение: A1 25, A2 32, B1 34,
B2 6, C 110 (было 25/30/33/6/112). Строк с адресом очереди: 110 (было 112); `C` стало меньше на две,
а адресов — ровно на два, так что один-к-одному держится и после снятия. Доля `A1` — 12 %. Снятые тексты —
тремя файлами в Drive-папке `10.9` от 2026-10-23 (их байты и md5 — в `driveMirrors.captures20261023e`, записи о
них — в индексе библиотеки).

**Не закрыто этим кругом.** Fragments 2–9 страницы Хамфрея и его второй трактат; латинские листы Маастрихта
(будущее `A1`); сама страница 332 у Мэнтон снята не напрямую; локаторы Восса по Amandus и Turretin; страницы
Фрейзер и Александра; год и ISBN «The Hampton Court Conference»; письма Кэмерона.

## 25. Круг 25: цитата обязана читать локатор под собой, а не под страницей

Круг 24 поднял Хамфрея из «непрочитанного» и вписал в `FP-160` (*Middle-Way*, 1673) пять формул. Три из них принадлежат другому сочинению того же автора — *Free Thoughts* (1710), 8–15, — а «double Respect» и «in these diverse Respects…» стоят у индексатора в блоке с совсем другими выходными данными. Дефект был не в снимке (снято всё, что страница отдавала) и не в поиске (по каталогам искали), а в разборе: страница указателя содержит несколько блоков, у каждого своя цитатная строка, а я прочитала её как один текст с одной ссылкой внизу.

Что сделано в этом круге:

1. **Строка `FP-160`**: формулы *Free Thoughts* из неё сняты, возвращены те, что в самом деле стоят под локатором 1673 г. («both universal and special grace together; and the one is Applicatory…», «a double thing … Salvation for Judas … Repentance for Peter», «Gratia universalis simpliciter…», «the fruit or offspring of our Election»). Отпечаток 1673 г. подтверждён каталожной записью Folger 488217, где *Middle-Way* перечислен в составе собрания *Mediocria* (London: T. Parkhurst, 1674), то есть назван библиотекой независимо от блога ⇒ `B1` → `A2`. Выше не поднимать: страницы 24–40 и 36–37 принадлежат одному только индексатору, листа не читали.
2. **Новая строка `FP-208`** — *Free Thoughts* (1710), 8–15: перенесённые формулы («double Respect», «diverse Respects», «an Inconsistency I cannot fully, but half approve», «Election takes care that Redemption be not in vain», «Universal Conditional Remission… The Act must be read… we find Conditions in it») плюс та же оговорка о Христе как «Executor of his Father's Election»; отпечаток стоит в PRDL вместе со ссылкой на скан Internet Archive ⇒ `A2`. Всего строк в реестре **208**: `A1` 25, `A2` 34, `B1` 33, `B2` 6, `C` 110; очередь пересъёма не изменилась (110) — ни одна строка из `C` в этом круге не поднималась.
3. **Поправка к собственному утверждению о периметре смешанного письма** (§23 выше, гл. 07): лан документов сканируется блокирующе с круга 22, «открытой дыры» в том виде, как она была описана, нет.
4. **Проверяемая часть этого круга — процедурная, и то, что остальное не проверяемо, надо называть.** Машинной проверки «цитата приписана не тому сочинению на той же странице» в гейте нет, и в этом круге её не добавлено: год отпечатка в строке совпадал с годом в локаторе, слова цитат в снятом тексте присутствовали, все счётчики сходились — всё, что гейт умеет считать, было в порядке, и он прав: он считает, а не читает. Что добавлено в данные: `note` записей о снятом носителе обязана называть **блок страницы**, а не только «фрагмент N из M», и `whatNotChecked` обязана перечислять блоки, не разобранные до локатора. Остальное — обязанность читающего: локатор читается под цитатой, а не под страницей, и страница не считается прочитанной, пока не дошла до последней своей цитатной строки.

Что круг не закрыл: блоки 3–9 страницы `?p=4407` не читаны; *Mediocria* 1674 как собрание (единственный путь Хамфрея к `A1`) не снималась; «Pracedanea» в снятом латинском и «he first head» у индексатора не сверены ни со сканом, ни с оригинальным набором. Файл-снимок — `cap25_humfrey_attribution.md` в папке `10.9`.
