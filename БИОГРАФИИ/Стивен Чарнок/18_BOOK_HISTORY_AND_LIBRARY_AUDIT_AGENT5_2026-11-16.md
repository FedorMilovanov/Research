# Том 18. История книг Чарнока: библиотеки, каталог 1680 года, издательская цепь и титульный лист 1682

**Тип записи:** рабочий библиографический аудит Агента 5 (историк книги, библиотек и английского книгоиздания XVII века) для досье Стивена Чарнока. Это **не** глава биографии и **не** готовый текст для публикации. Документ фиксирует: (а) что именно говорят свидетели о первой библиотеке и пожаре 1666 года; (б) что реально содержит оригинал *Bibliotheca Charnockiana* 1680 года и что в нём отсутствует; (в) точную издательскую хронологию 1674–1702 и XIX века с локаторами; (г) текстологию посмертных томов — переписчики, редакторы, надзор за печатью, утраченные рукописи; (д) титульный лист 1682 года как предмет исследования (два состояния, конкретные экземпляры, состояние изображения, права); (е) перечень ошибок статьи № 2 (PR #971 `charnock-biography-02-working.md`) и рекомендации для частей «Учёный», «Главная книга», «Другие книги».

**Границы владения.** Том 03 остаётся владельцем библиографии; настоящий том — аудит и аппарат к ней. Том 01 владеет иерархией биографических свидетелей, том 02 — хронологией, том 06 — матрицей доступа, том 08 — эпистолами Адамса и Вила, том 12 — broadside *Sayings*, том 16 — архитектурой серии. Правки в чужих томах в этом проходе минимальны и помечены.

**Дата прохода:** 16 ноября 2026. **Ветка:** `arena/cdc37d9b-research`, HEAD `70defa6`.

---

## 0. Классы источников и рабочие правила

| Класс | Что это | Как используется здесь |
|---|---|---|
| `A1` | Печатный оригинал XVII–XIX в., прочитанный как текст (EEBO-TCP, оцифровка IA, факсимиле) | Основание для утверждений о содержании |
| `A1-scan` | Просмотренное изображение страницы оригинала | Основание для утверждений о титуле, коллации, состоянии |
| `B1` | Современное научное исследование с аппаратом (Pearson 2010, Lawler 1898, BM *List of Catalogues* 1915) | Основание для внешней проверки цифр |
| `B2` | Современный реестр/агрегатор (Book Owners Online, ESTC-запись, каталог библиотеки) | Маршрут и сверка, но не независимое свидетельство |
| `C` | Каталог, OCR-слой, поисковый индекс, сниппет | Только как указатель; не доказательство |

Правила, действующие в этом томе без исключений:

1. **Произведение ≠ издание ≠ титульный лист ≠ экземпляр ≠ каталог ≠ цифровая репродукция.** Одна книга в пяти каталогах — одна книга.
2. **Права на изображение проверяются отдельно от возраста произведения.** 1682 год не делает файл свободным.
3. **OCR — не визуальная колляция.** Даты и номера страниц из OCR не цитируются без проверки по образу; в каталоге 1680 года OCR сильно испорчен (долгая «ſ», «1672» → «1972», разрушенные строки условий).
4. **Отрицательный результат ограничен прочитанным диапазоном.** «В прочитанном тексте нет» ≠ «не существует».
5. **Запрет на реконструкцию погибшего собрания.** Каталог 1680 года описывает **вторую** библиотеку; переносить его состав на 1666 год нельзя.

---

## 1. Первая библиотека и пожар 1666 года

### 1.1. Свидетели: полная таблица (обновлена в этом проходе)

| № | Свидетель | Дата | Что сказано | Класс | Статус |
|---|---|---|---|---|---|
| W1 | Джон Джонсон, *Eklampsis tōn dikaiōn* (Лондон, 1680), с. 33 | 1680, прижизненный круг | О «Deed of Gift, or rather Copy of it, which shewed his title to Heaven»: «**I believe** perished with his Books in Londons flames; and I have forgot the particular places of Scripture» | `A1` (EEBO-TCP A46911, том 09) | прочитано дословно; **единственное современное указание на гибель книг**; ограничено формулой «I believe» и одним конкретным документом |
| W2 | Ричард Адамс и Эдуард Вил, «To the Reader» к *A Treatise of Divine Providence* (Лондон, 1680; перепечатано в 1683 и 1684) | 1680 | «His Library, furnished (though not with a numerous, yet) a curious collection of Books, was his Workhouse, in which he laboured hard all the week» | `A1` (прочитано по набору 1684 г., том 08) | **пожар не упомянут**; фраза описывает библиотеку, которой он пользовался в конце жизни, т. е. **после** 1666 г. |
| W3 | Эдмунд Калами, *A Continuation of the Account…* (Лондон, 1727), **т. I, с. 81** | 1727 | «**His Library was burnt in the Fire of London.**» — отдельным абзацем, под рубрикой «Pag. 56. Mr. Stephen Charnock, B. D.» | `A1` — **текст перечитан 2026-11-16** (IA `continuationofac01cala`, скан с. 159, колонтитул «in London, Westminster and Southwark. 81»; § 1.4) | **первое явное печатное утверждение о пожаре**; на 47 лет позже события. **Исправление прежней записи:** не «т. III», а **том I** — издание пагинировано как два тома, и приписки идут подряд за текстом 1713 г. Размера библиотеки Калами **не** называет |
| W4 | Калами, *An Account…* (1713), т. II, с. 56 | 1713 | пожар **не упомянут** — проверено дважды: по Пирсону (2010, прим. 7) и **прямым поиском по тексту 2026-11-16** (слов «burnt», «burnt in the Fire of London» при статье нет; статья кончается смертью и «Funeral Sermon») | `A1` (текст) + `B1` (Пирсон) | согласуется с W1–W2: между 1680 и 1727 следов рассказа нет. Поиск «not large» по всему тому 1713 — **ноль совпадений** |
| W5 | Энтони Вуд, *Athenae Oxonienses* (1691) | 1691 | «published nothing while he lived» — о книгах, не о библиотеке | `A1` (том 11) | к пожару не относится |
| W6 | Сэмюэл Палмер, *The Nonconformist's Memorial* (Лондон, **1775**), т. I, **с. 161** | 1775 | «in his library, which was furnished with a **curious, tho' not large collection of books, and was burnt in the Fire of London**» | `A1` — **найдено 2026-11-16** (IA `nonconformistsm01cala`, скан с. 181; § 1.4) | **вот здесь и находится «not large»**. Палмер соединил две фразы, ходившие отдельно: «curious… collection» из предисловия Адамса–Вила 1680 г. и «burnt in the Fire of London» из Калами 1727 г. Приписано Калами ошибочно (см. § 1.3) |
| W6a | Производные XIX в. от Палмера: Уильям Саймингтон, Маккош | 1853+ | пожар как установленный факт, часто с риторическим расширением («smouldering ashes», «much valuable manuscript perished») | `B2`/`C` | **расширения XIX века не имеют опоры в XVII в.**; их источник — компиляция Палмера, а не новые документы |
| W7 | Дэвид Пирсон, *The Library* 11 (2010), 139–167, прим. 7 | 2010 | рассказ о пожаре отсутствует в earliest biographical accounts и в Калами 1713; в предисловии 1684 г. библиотека названа «not numerous, yet curious»; предупреждение против вывода о полном уничтожении | `B1` | внешняя проверка, принята |

### 1.2. Что устанавливается

1. **Факт утраты книг в 1666 году** стоит на одном современном свидетельстве (W1), и оно ограничено: Джонсон говорит о конкретном документе («Deed of Gift»), о котором он не помнит точных мест Писания, и выражает **уверенность-мнение** («I believe»), а не наблюдение. Формула «погибли в лондонском огне» относится к бумагам и книгам Чарнока в целом.
2. **Библиотека конца жизни — другая.** W2 (1680) описывает собрание, бывшее его «мастерской» в последние годы; В. Пирсон фиксирует, что 80 % проданных в 1680 году книг напечатаны **до 1660 года**, и на этом основании сам ставит под сомнение рассказ о полном уничтожении: старые книги в продаже 1680 года могли быть остатком первой библиотеки либо куплены на вторичном рынке. Вывод Пирсона («if the story is true…») — образец осторожности, который следует воспроизводить.
3. **Имя утраченной рукописи — ровно одно.** Это собственноручная запись обращения/посвящения себя Богу («Deed of Gift, or rather Copy of it»), о которой говорит Джонсон (W1). Никакого списка погибших рукописей не существует.

### 1.3. Что не устанавливается (и не должно быть заполнено догадкой)

| Вопрос задачи | Состояние источника | Формулировка для текста |
|---|---|---|
| Место хранения библиотеки в 1666 г. | Ни один свидетель не называет адрес, дом, приход или чьё-либо хранилище. Чарнок в Лондоне с 1660 г. без settled call; адрес его жилья в 1666 г. в прочитанных источниках не зафиксирован | «Где именно стояли книги в сентябре 1666 года, неизвестно» |
| Размер первой библиотеки | Нет ни числа томов, ни оценки стоимости. Формула «not large» **найдена и локализована 2026-11-16**: она принадлежит **Палмеру 1775, т. I, с. 161** («a curious, tho' not large collection of books»), а не Калами. Калами 1727 о размере молчит; «not numerous» — из предисловия Адамса–Вила 1680 г. | «Размер первой библиотеки не документирован» |
| Состав (языки, дисциплины, авторы) | Ни одного перечня. Каталог 1680 г. — вторая библиотека; отождествление запрещено | «Состав неизвестен; каталог 1680 года к ней не относится» |
| Погибшие рукописи, кроме Deed of Gift | Нет свидетелей. Косвенно: в 1684 г. редакторы сообщают, что собственные заметки Чарнока к одному из рассуждений «upon stricter search not being found» (см. § 4.2) — но это утрата, зафиксированная **после смерти**, без указания причины | «Кроме записи о посвящении себя Богу, ни одна погибшая рукопись по имени не названа» |

**Ловушка «not large» — РАЗРЕШЕНО 2026-11-16.** А. Гордон (Book Owners Online) пишет: библиотека «described by Calamy as ‘not large’». Проверка по трём оригиналам:

1. **Калами 1713** (т. II, с. 56): статьи о размере библиотеки нет; поиск «not large» по всему тому — ноль.
2. **Калами 1727** (т. I, с. 81): есть только «His Library was burnt in the Fire of London»; поиск «not large» по тому I — **ноль**, по тому II — **ноль**.
3. **Палмер 1775** (т. I, с. 161): «his library, which was furnished with a **curious, tho' not large collection of books, and was burnt in the Fire of London**» — единственное место, где формула существует.

**Вывод.** Атрибуция «Calamy: not large» **неверна**; это **Палмер 1775**, и он в свою очередь склеил две цитаты разных авторов и разных десятилетий: «curious collection» — Адамс и Вил, 1680 (о библиотеке **после** 1666 г.); «burnt in the Fire of London» — Калами, 1727. Палмер писал популярную компиляцию и не различал источники. Статус: `LOCATOR_HOLD` **снят**; вместо него вводится `ATTRIBUTION_CORRECTED`. В тексте допустима только формула: «Палмер (1775, т. I, с. 161) называет собрание «curious, though not large»; это его сводная характеристика, соединяющая предисловие 1680 г. с известием Калами 1727 г.».

### 1.4. Ключевые страницы: что именно прочитано (новое, 2026-11-16)

| Объект | Место | Дословно |
|---|---|---|
| Калами 1727, т. I | с. **81** (скан 159), колонтитул «in London, Westminster and Southwark. 81». Рубрика «Pag. 56. Mr. Stephen Charnock, B. D.» → «Mr. Johnson's Funeral Sermon for him was on Mat. xiii. 43…» → абзац о библиотеке | «His Library was burnt in the Fire of London. It was only in his latter Years, when his Memory began to fail him, that he penn'd and read his Sermons verbatim: But in his younger Days, he us'd no Notes in the Pulpit.» |
| Калами 1727, т. I, с. **81** (там же, абзацем выше) | рубрика «Pag. 56» | «…he never knew a Man in all his Life, that had attaind near unto that Skill that Mr. Charnock had, in the Originals of the Old and New Testament, except Mr. **Thomas Cawton**.» — **не Gataker** |
| Калами 1713, т. II | печатная с. **56** = скан 87 (нумерованная статья «43») | «43 Mr. Stephen Charnock, B. D. first of Emanuel College in Cambridge, and afterwards Fellow of New-College in Oxford. He was Senior Proctor of the University in 1652, and manag'd that Office with great Honour and Reputation; and was much Applauded for his Exercises at the Act.» |
| Палмер 1775, т. I | с. **160** | «in 1652, he was **senior proctor** of the university… **The year following** he was called to constant public employment in **Ireland**» |
| Палмер 1775, т. I | с. **159–160** | «of Eman. Col. Camb. where he was under the tuition of **Dr. Sancroft**, afterwards Abp. of Canterbury. It was there that he first experienced the effectual operations of divine grace upon his heart… He afterwards spent some time in a private family, and then in the exercise of his ministry, in **Southwark**; where **7 or 8 persons** owned him as the instrument of their conversion.» |
| Палмер 1775, т. I | с. **160** | «He had indeed studied **physic**, in which he had acquired considerable skill; but preaching was his peculiar gift.» |
| Палмер 1775, т. I | с. **161** | «**Mr. John Johnson**, who preached his funeral sermon, and had been an intimate friend of his from the time they were fellow students at Cambridge, has, **in the preface to that sermon**, given him a very uncommon character in a number of striking passages **selected from the Greek Fathers**…» |
| Палмер 1775, т. I | с. **161** | «He had entered upon a set of discourses concerning the **attributes of God**, which he **did not live to finish**» |

**Что это меняет.** (а) Локатор «Калами 1727, т. III, с. 81» исправлен на **т. I, с. 81**; (б) «Gataker» — ошибка томов 01/05/09: в 1727 г. стоит **Cawton**, что снимает расхождение между Johnson (Cawton) и Calamy; (в) Палмер 1775 — **первый, кто локализует источник патристического портрета** в предисловии к похоронной проповеди Джонсона, то есть подтверждает вывод тома 09 независимо; (г) Палмер — **первый, кто называет незавершённость рассуждений об атрибутах** обстоятельством смерти, а не редакторской небрежностью (ср. § 4.2); (д) Палмер — **первый и единственный источник** «studied physic», и он согласуется с «neglecting the practice of Physick» Адамса–Вила: **изучал, но не практиковал**; (е) Палмер **не** поддерживает «senior proctor 1652» Калами: он даёт 1652, но при этом ставит Ирландию «the year following», то есть воспроизводит ошибку, уже разрешённую в томе 02 в пользу 1654 (Wood, *Fasti*, с. 783; McCosh).

### 1.5. Урок для аппарата: как возникает «цитата Калами»

Цепочка, восстановленная полностью, стоит того, чтобы её зафиксировать как типовой случай:

1. **1680**, Адамс и Вил: «His Library, furnished (tho not with a numerous, yet) a curious Collection of Books, was his Workhouse» — о собрании **после** 1666 г., без слова «large» и без слова «burnt».
2. **1713**, Калами: о библиотеке ничего.
3. **1727**, Калами: «His Library was burnt in the Fire of London» — **без размера**.
4. **1775**, Палмер: «his library, which was furnished with a curious, tho' **not large** collection of books, **and was burnt in the Fire of London**» — склейка (1) и (3) в одном предложении, причём обе половины относятся к **разным** собраниям.
5. **XXI в.**, Book Owners Online: «described by Calamy as ‘not large’» — цитата приписана Калами, которого в этой точке цепочки нет.

**Правило, которое из этого следует.** Формулу, соединяющую характеристику собрания с известием о его гибели, нельзя принимать на веру даже в академическом реестре: она может быть позднейшей склейкой двух источников. Проверка делается по **двум** признакам одновременно: (а) есть ли это слово в оригинале автора, которому цитата приписана; (б) не составлена ли фраза из двух предложений разных лет. В нашем случае «large» отсутствует у Калами во всех томах, а «curious» принадлежит 1680 году.

**Следствие для биографии.** Характеристика «not large» может быть **употреблена**, но только с точной атрибуцией — «Палмер (1775, т. I, с. 161) называет собрание «curious, though not large»» — и с оговоркой, что это компиляция, а не свидетель эпохи.

---

## 2. Вторая библиотека: *Bibliotheca Charnockiana* (1680)

### 2.1. Объект и его экземпляры

**Полное заглавие** (по транскрипции Folger 533300; стиль оригинала сохранён):
*Bibliotheca Charnockiana, sive catalogus librorum selectissimae bibliothecae clarissimi, doctissimiq; viri domini Steph. Charnock, S.T.B. nuperrime defuncti. Quorum auctio habebitur Londini apud insigne Agni in vico vulgo dicto Cornhill, quarto die Octobris, 1680.*

| Параметр | Значение | Источник |
|---|---|---|
| Автор каталога (в записи) | Edward Millington, c. 1636–1703 | Folger 533300 |
| Место и распространители | Лондон; каталоги раздавались бесплатно «at Sign of the Lamb in Cornhill» (у обойщика) и «at Sign of Three Legs in Poultrey» (у книгопродавца) | Folger 533300 |
| Объём | [4], 31 с. | Folger 533300 |
| Wing | C3707 | Folger 533300; Christie's (Lauderdale set, лот 49) |
| Оригинал репродукции | Британская библиотека, EEBO Tract supplement D8:1[2] | Folger 533300 |
| Экземпляр Британского музея/Библиотеки | **S.-C. 923.(2)** (Sale Catalogues), с пометой «With preface», **без пометы «Priced»** | *List of Catalogues of English Book Sales 1676–1900 now in the British Museum* (1915), раздел 1680 |
| Цифровая копия | IA `bim_early-english-books-1641-1700_bibliotheca-charnockiana_charnock-stephen_1680`: 35 изображений, JP2 84,9 МБ, PDF 24,4 МБ, `djvu.txt` 60 751 байт (MD5 `7be51344ffa42891e2ed9028908f3a77`) | IA metadata |
| Экземпляр в частном собрании | Christie's, Lauderdale set (71 каталог), лот 49; набор частично с рукописными ценами, но **о наличии цен именно в каталоге Чарнока** в описании лота не сказано | Christie's, lot 4458260 |

**Важная текстологическая деталь титула:** каталог титулует Чарнока **S.T.B.** (Sacrae Theologiae Baccalaureus), то есть B.D. Британский музей в 1915 г. внёс его как «Charnock, Stephen, *D.D.*» — это ошибка каталожной шапки, а не издание. При цитировании нельзя воспроизводить «D.D.».

### 2.2. Что содержит оригинал: полное чтение

Прочитан весь текстовый слой оцифровки (chunks 0–7 из 8; последний фрагмент — служебный). Порядок отделов и наблюдённые максимумы нумерации:

| Отдел каталога | Наблюдённый диапазон | Примечание |
|---|---|---|
| Титул | — | латинский, см. § 2.1 |
| Advertisement (на обороте титула) | — | **отдельное объявление о приложении**: распродажа библиотеки Томаса Уотсона, «late Master of Charter-House-School in London»; здесь же сведения о печатании каталогов |
| «To the Reader» | — | Чарнок как «sometime Fellow of New-Colledge in Oxford and Proctor of the University», известный точностью проповеди; анонс: «Excellent Discourses of his, Of Providence, &c. now preparing for publick view» |
| Условия продажи (I–IV) | — | повторное выставление при споре; «perfect unless expressed»; оплата в течение месяца; осмотр за неделю до торга |
| Libri Theologici, Folio | 1–110 | латинское богословие в лист |
| Libri Theologici, Quarto | 1–135 | |
| Libri Theologici, Octavo & Duodecimo | 1–127 | |
| Libri Miscellanei (Folio / Quarto / Octavo) | в пределах отделов | классики, история, право, философия, медицина отдельно |
| Libri Medicinales (Folio / Quarto / Octavo) | — | латинская медицина |
| Книги на французском, итальянском, испанском | — | Пирсон: 75 лотов, «mostly French but including a Spanish Bible and writings by Guicciardini and Machiavelli in Italian» |
| English Divinity | — | |
| English Miscellaneae | — | |
| Латинские и английские памфлеты | — | по Пирсону: латинские 39 в 4°; английские 24 в folio + 225 в 4° + 26 в 8° = 275; латинские помечены «incompacti» (непереплетённые); продавались связками по 15 лотов, в каждом 20 и более единиц |

**Чего в прочитанном тексте нет.** Ни в одном фрагменте — включая титул, Advertisement, «To the Reader» и Conditions — не встречается: общего числа предметов; итоговой суммы выручки; указания на имя аукционера; упоминания пожара 1666 года; каких-либо дат продажи, кроме 4 октября 1680 года. Это отрицательный результат по всему объёму текстового слоя, но **не** визуальная колляция: лист мог содержать рукописные пометы в конкретном экземпляре, которых OCR не передаёт.

### 2.3. Число 1330: происхождение и проверка

| Источник | Что даёт | Класс |
|---|---|---|
| Пирсон 2010, таблица пяти каталогов, строка Charnock | «Nonconformist clergyman, 4 Oct 1680 (London), **1,330**» — то есть число взято в базу из каталога | `B1` |
| Book Owners Online (ред. 20.06.2021) | разбивка: латинское богословие 372; английское богословие 256; латинская медицина 65; латинское разное 192; английское разное 56; европейские языки 75; латинские памфлеты 39 в 2 томах; английские памфлеты 275 в 13 томах | `B2` |
| Пирсон 2010, текст | независимо: латинские памфлеты 39; английские памфлеты 24+225+26 = **275** | `B1` |

**Проверка арифметики, выполненная Агентом 5 (новое):**

- 372 + 256 + 65 + 192 + 56 + 75 + 39 + 275 = **1330** — сумма разбивки точно равна заявленному числу.
- 110 + 135 + 127 = **372** — три богословских латинских отдела (folio / quarto / octavo-duodecimo), максимумы которых я наблюдал при чтении, в точности дают «латинское богословие 372».
- 24 + 225 + 26 = **275** — совпадает с независимым разбором Пирсона.

**Вывод.** Число **1330** — не оценка и не позднейшая реконструкция: это арифметика по разделам самого каталога, и она сходится по двум независимым линиям (Пирсон и внутренняя структура отделов). Однако **прямым чтением оригинала с подсчётом каждого лота Агент 5 это число не подтверждает**: OCR разрушает нумерацию, а сверка по образам не проводилась. Корректная формула: «около 1 330 лотов; цифра получена сложением разделов каталога и подтверждена независимо Пирсоном (2010), но не проверена нами постранично по образам» (`ARCHIVE_HOLD` на постраничный пересчёт).

### 2.4. £366 5s 1d: статус — **одно свидетельство, не подтверждено**

| Проверка | Результат |
|---|---|
| Текст каталога 1680 г. (весь доступный OCR) | суммы нет |
| Пирсон 2010 (chunks 0–9, включая приложения и примечания) | суммы нет; в статье обсуждаются только числа лотов |
| *List of Catalogues… British Museum* (1915) | запись о каталоге **не помечена «Priced»**; помеченные (например, Seaman 1676, Manton 1678) помечены явно |
| Lawler, *Book Auctions in England in the Seventeenth Century* (1898) — главы о Купере и Миллингтоне, хронологический список | каталог Чарнока в разобранных разделах не описан; итогов продажи не приводится |
| Christie's, Lauderdale set (описание 71 каталога) | цена лота аукциона 2005 г., не выручка 1680 г. |
| Book Owners Online | **единственный** источник фразы «The sale made £366 5s 1d» |

**Вывод, обязательный к соблюдению.** £366 5s 1d — цифра **одного современного реестра**, не подтверждённая ни оригиналом, ни научной литературой, ни аукционными исследованиями. Она **не должна** сопровождаться словами «по каталогу», «документировано», «выручка составила». Допустимая формулировка: «в литературе встречается цифра £366 5s 1d (Book Owners Online); первоисточник её не раскрыт, и проверить её можно только по экземпляру с рукописными ценами — такой экземпляр пока не найден». Статус: `SINGLE_SOURCE_UNVERIFIED`.

Если экземпляр с ценами будет найден, порядок проверки: (1) сверить, что цены проставлены современной рукой против каждого лота; (2) просуммировать по отделам; (3) учесть непроданные лоты (ранние каталоги их не отмечают систематически); (4) только затем сопоставлять с £366 5s 1d.

### 2.5. Аукцион 4 октября 1680 года: документированные факты

| Параметр | Установлено | Статус |
|---|---|---|
| Дата | понедельник 4 октября 1680 г. | `A1` (титул) |
| Место | «apud insigne Agni in vico vulgo dicto Cornhill» — у вывески Агнца на Корнхилле | `A1` |
| Что это за дом | дом обойщика (upholsterer), где раздавались каталоги; в том же месте 8 октября 1680 г. Миллингтон продавал библиотеку Томаса Уотсона | `B2` (Folger), `B1` (BM List, Christie's) |
| Второй пункт раздачи каталогов | «Three Legs in the Poultrey» — лавка **Томаса Кокерилла**, издателя почти всех посмертных томов Чарнока | `A1` (титул) + `A1` (импрессы 1680–1699) |
| Аукционер | **на титуле не назван.** Миллингтон выводится только косвенно: (а) запись Folger приписывает ему авторство каталога; (б) тот же дом и тот же агент через четыре дня; (в) Кокерилл как распространитель связывает продажу с издательским кругом | `B2`, `C` — **атрибуция вероятная, не документированная** |
| Часы торгов | в OCR условия содержат испорченные числа; **не цитировать** | `LOCATOR_HOLD` |
| Условия | четыре пункта (повторное выставление при споре; комплектность, «perfect unless expressed»; оплата в течение месяца после окончания; осмотр за неделю) | `A1` |
| Состав | см. § 2.2 | `A1` (текстовый слой) |
| Томас Уотсон | отдельное объявление на обороте титула: библиотека «late Master of Charter-House-School in London» | `A1`; **это не** со-пастырь Чарнока и **не** его душеприказчик |

**Практический вывод для биографии.** Продажа была организована в связке с Кокериллом: каталог раздавался в его лавке, а в самом каталоге уже анонсированы «Excellent Discourses of his, Of Providence, &c. now preparing for publick view». Это единственное прямое документальное звено между распродажей библиотеки и издательской программой 1680–1684 годов, и оно сильнее любой догадки об «аукционере-друге».

### 2.6. Что библиотека говорит и чего не говорит

**Говорит (осторожно):**

- Латинская часть решительно преобладает; по Пирсону соотношение латыни и английского примерно 50/50, а по богословию латынь вдвое больше английского.
- Тематический профиль нонконформистского богослова виден в концентрациях: Эймс (5 названий), Джон Оуэн (13), Уильям Стронг (7), Ричард Бакстер (10). Это **состав**, а не индекс цитирования.
- Есть книги, которых биограф не ожидает: Томас Флэтмен, *Poems and Songs*; Рафаэль Ториус, *Hymnus tabaci*; «Hicks's Collection of Oxford Jests»; «The Noble Birth and Gallant Atchievements of that Remarkable Out-law Robin Hood»; «Mr. Smirke, or the Divine in Mode» Марвелла; из Мильтона — только *Reason of Church-Government Urg'd*.
- Один экземпляр описан с переплётом: еврейская Библия «corio turcico» (турецкая кожа). Пирсон отмечает, что такие пометы в каталогах редки.
- Памфлеты хранились **непереплетёнными** («incompacti») и продавались связками — материальная деталь, объясняющая, почему от таких собраний почти ничего не дошло.

**Не говорит:**

- **65 латинских медицинских книг ≠ доказательство врачебной практики.** Это состав библиотеки. Предисловие 1680 года само говорит, что Чарнок «neglecting the practice of Physick, in which he had arrived at a considerable measure of knowledg» — то есть знание признаётся, практика отрицается как оставленная. Оба свидетельства нужно держать рядом; вывод «практиковал, потому что были медицинские книги» недопустим.
- **Ни одна книга из его собрания не отождествлена.** Пирсон прямо пишет: прослежены книги Бабингтона (2) и Натчбулла (3), но «not of any of Bassett's, Charnock's, or Coga's». Следовательно, на сегодня **нет экземпляра с доказанным происхождением из библиотеки Чарнока**.
- Каталог не доказывает, что вторая библиотека была собрана «взамен погибшей»: он фиксирует состояние на август–октябрь 1680 года.

---

## 3. Библиографическая хронология: 1674–1702 и далее

Ниже — только то, что подтверждено записью или текстом. Колонка «Статус» отражает, **что именно** проверено.

### 3.1. Прижизненная публикация

| Год | Объект | Данные | Локатор | Статус |
|---|---|---|---|---|
| 1674 | *A Supplement to the Morning-Exercise at Cripple-gate…* (1-е изд.), проповедь 19 «The Sinfulness and Cure of Thoughts», Быт 6:5, подпись «Mr. S. C.» | Лондон, Thomas Cockerill; посвящение Сэмюэла Эннсли датировано 19 июня 1674 г.; текст проповеди в издании 1674 г. на с. 422 (по цитатной литературе) | Google Books (полный просмотр) — цитируется по Quote Investigator; **прямого чтения первопечатного листа нет** | `FAM-01 BLOCKED` (не подтверждено нами по образу) |
| 1676 | То же, 2-е изд. | Wing A25478, ESTC; Cockerill «at the Sign of the Atlas in Cornhil»; [6], 778 с.; проповедь 19, с. 471–502 (по Research 03) | EEBO-TCP `A25478.0001.001` | `FULL_OBJECT_VERIFIED` (для 1676 г.) |

Замечание к атрибуции: подпись «S. C.» в 1674 г. сама по себе не доказывает авторства; она подкрепляется (а) включением той же проповеди в *Supplement* 1683 г. под именем Чарнока, (б) указанием Вуда 1691 г. и (в) traditio XIX в. Цепочка косвенная, но непрерывная; в тексте её нужно показывать, а не подразумевать.

### 3.2. 1680 год: шесть печатных объектов

| Объект | Wing / ESTC | Импресс | Объём | Статус |
|---|---|---|---|---|
| *A Treatise of Divine Providence* | C3712 (`A32726`), ESTC R13224 | Cockerill, Three Legs in the Poultry | [16], 397, [4] (8°); Folger 126705: [16], 397, [3] | `A1` прочитан (том 08); экземпляр Folger 257348 с рукописными пометами на первом форзаце |
| *A Sermon… on 2 Cor. V. XIX* | C3710 (`A32722`) | «Printed by Thomas Milbourn, for J.K., and are to be sold by Langley Curtis» | [2], 5–38 | `A1` (EEBO); **не входит в круг изданий, которые Адамс и Вил признают своими** — см. § 4.4 |
| *The Sayings of that Reverend and Great Preacher Mr. S. Charnock* (broadside) | C3709 (`B02133`) | два состояния: [s.n.] (Bodleian; 2740:15) и «Printed for R.J.» (BL; Tract supplement B3:3[7], с дефектом — stained) | 1 лист | `A1` + визуальная коллация (том 12) |
| *New Poems upon the Death…* | N715 (`A52960`) | Thomas Snowden | broadside | `A1` (том 13) |
| *An Elegy on the Death…* | E409 (`A39134`) | J. A. for Thomas Cockerill | broadside | `A1` (том 14) |
| Джон Джонсон, *Eklampsis tōn dikaiōn* | J783 (`A46911`) | «Printed for the author, and are to be sold by Tho. Parkhurst, Will. Miller, and Benj. Alsop» | [6], 40 с. | `A1` полностью (том 09) |
| *Bibliotheca Charnockiana* | C3707 | см. § 2.1 | [4], 31 с. | `A1` (текстовый слой) |

### 3.3. 1682: *Several Discourses upon the Existence and Attributes of God* — **два состояния**

Это важнейшая поправка к текущему Research, где издание описано одной коллацией.

| | Состояние A (C3711) | Состояние B (C3711aA) |
|---|---|---|
| Wing / ESTC | C3711 / ESTC **R15604** | C3711aA / ESTC **R231290** |
| Импресс | «Printed for D. Newman, T. Cockerill, Benj. Griffin, T. Simmons, and Benj. Alsop» | то же + «**And are to be sold by Michael Hide bookseller in Exon**» |
| Пагинация в записи | [10], 827, [28] с. | [10], 552, 551–692, 697–827, [29] с. («text and register continuous despite pagination») |
| Формат | 2° | 2° (fol.) |
| Оригинал репродукции | Bodleian Library (EEBO 21:5, ProQuest docview 2240898110) | Folger Shakespeare Library, шифр **228918** (EEBO 2475:5, image 135203, ProQuest docview 2240933541) |
| Другие экземпляры в ESTC (выборка) | Bristol (Restricted Small Folio BX9318 CHA), Hereford Cathedral 29.C.1 и 25.A.6, National Trust CHA (с надписью «Th. 26. Oct. 1682 fro[m] Mr. Tho. Guy, pretium 1li.2s.6d besides carriage» и гербовым экслибрисом William Lucy of Charlecote), National Trust LAN (спринклед-калф XVII в.), Oxford Exeter College PGW 6S, Oxford Trinity G.17.7, Huntington 432389, Union Theological Seminary 1682 C483, Free Library of Philadelphia C3711, Virginia BT130.C44 1682, Berkeley Bancroft BX9315 .C42 S3 1682, Oxford St Edmund Hall 279 (в записи R231290) | то же издание; Folger 228918 |
| Что читаем как текст | EEBO-TCP `A32723.0001.001`, 866 с., 1 378 961 слово | IA-микрофильм `…charnock-stephen_1682` (871 изображение) и `…_1682_0` (865 изображений) |

**Практические следствия.**

1. Утверждение «827 страниц основного текста» описывает **одно** состояние; в другом пагинация выражена иначе (552, 551–692, 697–827). Это не разные издания, но и не одна коллационная формула. В статьях нужно писать: «[10], 827, [28] с. (в другом состоянии пагинация записана как [10], 552, 551–692, 697–827, [29] с. при непрерывном регистре)».
2. Наличие второго импресса («sold by Michael Hide in Exon») — документальное свидетельство **провинциального распространения** первого тома: книга не осталась в лондонском круге. Это самостоятельный факт книжной истории, которого в Research нет.
3. Запись National Trust CHA с ценой «1li. 2s. 6d. besides carriage» и датой покупки 26 октября 1682 г. — редчайший случай **датированной покупки** первого тома; полезна как свидетельство цены и скорости распространения. Внимание: это провенанс одного экземпляра, не цена издания.

### 3.4. 1683–1702

| Год | Объект | Данные | Локатор | Статус |
|---|---|---|---|---|
| 1683 | *A Supplement to the Several Discourses upon Various Divine Subjects* | Wing C3711C, ESTC R24823; Cockerill; 118, [36] с.; 2°; errata на с. [36] второй группы; **индексы к *Discourse of Divine Providence* и к *Works***; в записи — ссылка на «Works of the late learned divine, Stephen Charnock» | EEBO `A32724.0001.001`; фрагмент `A32724.xml` | `A1` (текст прочитан); связь «Supplement = т. II» не доказана (см. ниже) |
| 1683 | *A Treatise of Divine Providence* — издание/выпуск иного объёма | Wing **C3712 Variant**; [6], 94 с.; экземпляр Huntington | Folger 494834 | `CATALOG_ONLY`; природа выпуска (сокращение? отдельный оттиск части?) не установлена |
| 1683 (титул) | *A Treatise of Divine Providence* внутри составных томов 1684 г. | отдельный титул с датой 1683 г. и пагинацией/регистром | Folger 134068 (Vol. I), 133622 (Vol. II) | `A1` (титул читается в составе томов) |
| 1684 | *Works… Vol. I*: «Several Discourses upon the Existence and Attributes of God… To which is added his Discourse of Divine Providence» | Wing **C3703**, ESTC **R12522**; «Printed for Ben Griffin, and Tho. Cockeril, and are to be sold at the Three Legs in the Poultrey»; [10], 820, [6], 58, 55–94, [34] с., [1] л. портрета; **портрет подписан «R. White sculp:»**; сигнатуры A⁴ chi1 B–5M⁴ 5N–5S², ²A–O⁴; финальный рекламный лист | Folger 134068 (шифр 144-451f Vol. 1; современный тёмный марокен с золотым тиснением и гоффрированными обрезами; провенанс — гербовый экслибрис с девизом «tuum est», куплено у Maggs 3 мая 1954) | `A1` (каталожная запись с полной коллацией) |
| 1684 | *Works… Vol. II*: «Being Several Discourses upon Various Divine Subjects» | Wing **C3705**, ESTC **R11740**; «Printed by A. Maxwell, and R. Roberts, for Tho. Cockerill»; [6], 200, 201–242 (листы), 241–520, 553–592, 597–952, 1073–1220, 1281–1376, [2], 118, [32] с., портрет; *Supplement* 1683 г. с отдельным титулом, пагинацией и регистром; сигнатуры pi1 A² B–2N⁴ 2O², ²2H–3T⁴, 4A–4E⁴ 4F⁶ 4G–6D⁴, 7A–7S⁴ 7T², 8A–8M⁴, ³A–P⁴, ⁴A–H² | Folger 133622 (та же провенанс-линия, что Vol. I) | `A1` |
| 1684 | *A Discourse of Divine Providence* (отдельно, 8°) | Wing **C3708**, ESTC **R232630**; «Printed by R. Roberts for Thomas Cockerill»; [16], 397, [3]; «Originally published in 1680 as: A treatise of divine providence (Wing C3712)» | Folger 148053 (провенанс: Shipdham Church, Norfolk) | `A1` |
| 1685 | *A Discourse of Divine Providence* — переиздание | «Printed for John Harris, at the Harrow, over against the Church in the Poultrey»; [16], 397, [3] | Folger (EEBO `99896919`) | `CATALOG_ONLY` (Wing не зафиксирован) |
| 1699 | *Works… The third edition corrected* (2 т.) | Wing **C3704** (т. I), **C3706** (т. II); «Printed for Ben. Griffin, John Lawrence, Eliz. Harris, John Nicholson, and Tho. Cockerill»; I: [6], 648, [22] + портрет; II: [6], 758, [20] + портрет; **том II помечен «The second edition corrected»**; «To the reader» подписан Edw. Veel и Ri. Adams | Folger (EEBO 653:7 и 653:8) | `A1` (каталожная запись) |
| 1699 | *Two Discourses: Of Man's Enmity to God (Рим 8:7); Of the Salvation of Sinners (1 Тим 1:15)* | Wing **C3713**, ESTC **R035566**; «Printed for Tho. Cockerill, at the Three Legs and Bible in the Poultrey»; [12], 76, 79–254, [2]; 148 с.; 8°; **«Publish'd from his original manuscripts by Mr. Edward Veel»**; «An Advertisement to the reader» подписан Edw. Veel; вторая часть с колонтитулом «Chiefest sinners objects of choicest mercy» | Folger 200087 (Enquiry 348220) | `A1` (каталожная запись); текст `B20167` |
| 1702 | 3-е изд. (?) | в текущем Research значится «1702 3rd ed.» | — | **не подтверждено**; вероятно, смешение с 1699 «third edition»: требует снятия или локатора (`FAM-03`) |
| 1797 | *Discourses upon the Existence and Attributes of God, abridged… by the Rev. Griffith Williams* | ESTC **T73779**; Лондон, 8°; viii, [2], 559 с.; «Price Six Shillings and Six-Pence in Boards» | Folger 846678 | `A1` (запись); **в Research отсутствует** |
| 1815–1816 | *The Works of the Late Rev. Stephen Charnock… with a prefatory dedication and memoir* (Edward Parsons), 9 т. 8° | IA: `worksoflaterevst04char`, `…05char`, `…08char` (1815) | IA | `CATALOG_ONLY` (состав томов не сверен) |
| 1840 / 1853 / 1859 | *The Doctrine of Regeneration… selected from the writings*; *Discourses upon the Existence and Attributes of God*, изд. с «Life and Character» Уильяма Саймингтона (R. Carter, New York, 1859; первое издание 1853) | HathiTrust 100873983; IA `discoursesuponex02char_0` (1854), `discoursesupone01symigoog` (1853) | `B2` |
| 1864–1866 | *The Complete Works* / «With introd. by James M'Cosh», Edinburgh: J. Nichol, 5 т., серия «Nichol's Series of Standard Divines. Puritan Period» | Folger 51421, шифр BX9315.C4A1 1864; IA `completeworksofs03char` | `A1` (запись); вступительная статья Маккоша используется в Research, но её **полный текст не сверен** |

### 3.5. Уточнение по «второму тому» и *Supplement*

В Research (03 §3E и §12.4) уже зафиксировано, что униформный титул «Works of the late learned divine» не доказывает, что *Supplement* 1683 г. равен всему второму тому. Данные этого прохода усиливают осторожность:

- *Supplement* 1683 (C3711C) — самостоятельная единица в 118 + [36] с. с индексами к *Providence* и к *Works*; она входит в Vol. II 1684 г. как блок с собственным титулом, пагинацией и регистром (см. коллацию Folger 133622).
- Vol. II 1684 г. содержит **гораздо больше**, чем *Supplement*: «Discourses upon various divine subjects» на сотни страниц (200–1 376 в прерывистой пагинации).
- Следовательно, отождествление «Supplement = Vol. II» неверно; верно: «*Supplement* — один из блоков внутри Vol. II, сохранивший отдельный титул 1683 года».

---

## 4. Текстология посмертных томов: кто делал текст

### 4.1. Издательская группа

| Лицо | Роль по документам |
|---|---|
| **Thomas Cockerill** | издатель/книгопродавец почти всех посмертных томов 1680–1699: *Providence* 1680 (Three Legs in the Poultry), *Supplement* 1683, *Works* 1684 (с Ben Griffin; печатники A. Maxwell и R. Roberts), *Two Discourses* 1699 (Three Legs and Bible); **его лавка — второй пункт раздачи каталога аукциона 1680 г.** |
| **Richard Adams** (1626?–1698) | со-подписант эпистол «To the Reader» 1680 (Providence), 1682, 1684 (оба тома), 1699 |
| **Edward Veal / Veel** (1632?–1708) | то же; в 1699 г. — единственный названный публикатор *Two Discourses* («publish'd from his original manuscripts»); его «Advertisement to the reader» 1699 г. — последнее прямое редакторское свидетельство |
| **D. Newman, Benj. Griffin, T. Simmons, Benj. Alsop** | консорциум импресса 1682 г.; Newman и Griffin затем в 1684 и 1699 |
| **Michael Hide (Exon)** | провинциальный распространитель состояния B 1682 г. |
| **A. Maxwell, R. Roberts** | печатники *Works* 1684 |
| **Robert White** (1645–1703) | гравёр парадного портрета-фронтисписа в *Works* 1684 (подпись «R. White sculp:») — материальная привязка к иконографии, используемой в PR #971 |
| **J. K.** и **Langley Curtis** | импресс *Sermon on 2 Cor. V. XIX* 1680 — вне круга Адамса–Вила |
| **Thomas Milbourn** | печатник той же проповеди |

### 4.2. Разделение труда переписчиков (дословно, 1684, Vol. II, «To the Reader»)

> «…a considerable part, namely, the Learned and Spiritual Discourses of **Regeneration**, were carefully Copied out by **one** of the former happy Undertakers; and tho **another** who attain'd to the Skill of perfectly reading his Manuscripts, was chiefly employ'd in Transcribing the major part of this Great Work from the Authors own Copy; yet the Transcript hath been diligently compar'd with the Original, by **the other** of the former Transcribers, before we read it each of us separately, and afterwards those passages conjunctly, in consultation together, wherein either of us conceiv'd any little scruple might arise concerning the Authors genuine sense…»

> «…and the vigilant Supervisal of the Press by an **Ingenious person**, who did much honour the Author…»

Что это даёт:

1. **Двухступенчатая работа**: один переписчик копирует «Regeneration», другой — основную массу; затем взаимная сверка переписчика с оригиналом и совместное чтение обоих редакторов. Это не «редактура по вкусу», а заявленная процедура сличения.
2. **Третий участник** — «Ingenious person», наблюдавший за печатью; имя не названо. В сносках 1684 г. (по OCR, ненадёжно) фигурируют инициалы, которые Research передаёт как «Mr. J. Wichens. Mr. Ashton.» — **полные имена не установлены**, и отождествлять их с «Ingenious person» нельзя.
3. Формула «before we read it each of us separately» — свидетельство того, что Адамс и Вил работали как **два независимых корректора**, а не как один редактор.

### 4.3. Пропуски и утраты в рукописях (1684, «To the Reader», дословно)

> «As to that Discourse about *The Spirits convincing the World of sin*, the Authors own Notes **upon stricter search not being found**, two **Skilful short-hand Writers**, who constantly attended his Ministry, have supplied the defect, from what they both took from his own mouth, when they had **compared their Notes**…»

Это ключевой пассаж для всей текстологии Чарнока:

- часть корпуса — **автографы**;
- часть — **стенограмма двух постоянных слушателей**, сведённая сверкой двух записей;
- часть автографов **не найдена** при подготовке издания (причина не указана — пожар здесь не упомянут);
- редакторы сами признают, что «supply» уступает «Accuracy of those other parts Transcrib'd from his own Manuscripts».

### 4.4. Редакторская полемика с «чужими» изданиями

В предисловии 1680 г. (Providence) Адамс и Вил пишут:

> «…whatever any else shall publish, can be but **imperfect Notes** (his own Copies being under our revisal at the request of his Friends) taken from him in the Pulpit; in which, what mistakes do often happen, every one knows, and **we have found by experience in the case of this very Author more than once**».

Что это значит практически:

- Уже в 1680 г. существовали **посторонние публикации** проповедей Чарнока по слушательским записям, и редакторы знали о их дефектности по опыту.
- Кандидаты на статус «imperfect Notes»: *A Sermon… on 2 Cor. V. XIX* (1680, Milbourn для J. K., продавал Langley Curtis) — не входит в круг изданий, подписанных Адамсом и Вилом; и малое издание *Treatise of Divine Providence* 1683 г. в 94 с. (Wing C3712 Variant).
- **Это вывод-гипотеза (`B`), а не установленный факт.** Прямого указания, какое именно издание редакторы имели в виду, нет. В тексте часть «Другие книги» формулировка обязательна: «редакторы предупреждали о дефектных чужих записях, не называя изданий».

### 4.5. Признание несовершенства мелких трактатов

Vol. II 1684: «if in two or three smaller Tracts the Author seem not altogether so elaborate as in his other pieces, it cannot but be granted, that they were some **occasional Sermons composed in great straits of time**». Это редакторская оговорка, которую следует цитировать при любом утверждении о «неровности» корпуса: неровность признана самими издателями и объяснена обстоятельствами, а не небрежностью переписчиков.

---

## 5. Титульный лист 1682 года как предмет исследования

### 5.1. Что должно быть объектом

Обязательный объект — **титульный лист первого издания 1682 г.**, а не титул *Works* 1684 г., не титул 1699 г. и не титул любого переиздания XIX–XXI вв. В PR #971 и в Research 03 до сих пор цитировался титул, восстановленный по каталогизации, а не по образу листа.

### 5.2. Выбор экземпляра

| Кандидат | Плюсы | Минусы | Решение |
|---|---|---|---|
| **Folger 228918** (ESTC R231290, EEBO 2475:5, image 135203) | физически в Folger; полная каталожная коллация; состояние B с импрессом Michael Hide | цифровой файл — микрофильм EEBO; доступ к изображению через ProQuest; в открытом доступе образца нет | **приоритет № 1** для заказа фотосъёмки/скана |
| **Bodleian** (EEBO 21:5, ProQuest docview 2240898110) | оригинал репродукции, на которой построен EEBO-TCP `A32723` | шифр в ESTC не указан («Shelfmark not available»); доступ через EEBO/ProQuest | приоритет № 2 (через EEBO image, если есть институциональный доступ) |
| **National Trust, Charlecote (CHA)** | надпись о покупке 26 октября 1682 г. и цена | частное собрание National Trust, режим доступа не установлен | только как провенанс-свидетельство, не как источник титула |
| **IA `…_1682_0` / `…_1682`** | открытый доступ, полный текст | **микрофильм** (box IA40313010-83 / IA40310615-24), 800 ppi, изображения в этом окружении не загружаются; в текстовом слое титул читается фрагментарно | только для транскрипции, не для публикации образа |

### 5.3. Что уже установлено о титуле

По текстовому слою IA-микрофильма состояния B (chunk 0) читается:

> «SEVERAL | DISCOURSES | UPON THE | EXISTENCE | AND | ATTRIBUTES | OF GOD. | By that late Eminent Minister of Christ, | Mr. STEPHEN CHARNOCKE, B. D. | And sometimes Fellow of New-Colledge in Oxon. | LONDON, | Printed for D. Newman, T. Cockerill, Benj. Griffin, | T. Simmons, and Benj. Alsop. | And are to be Sold by Michael Hide Bookſeller in Exon. | M DC LXXXII.»

По текстовому слою второго микрофильма (состояние A, `…_1682`, chunk 0) тот же титул **без строки о Michael Hide**.

Отсюда два практических требования:

1. **Титул нужно описывать с указанием состояния.** Строка «And are to be sold by Michael Hide bookseller in Exon» присутствует не во всех экземплярах; если в статье её нет, а иллюстрация взята из состояния B, возникает расхождение текста и изображения.
2. **Формула «B.D. and sometimes Fellow of New-Colledge in Oxon»** — часть титула и должна воспроизводиться дословно; в исследовательской литературе встречаются искажения («B.D. and Fellow», «S.T.P.»).

### 5.4. Состояние изображения и права

| Вопрос | Ответ на 16.11.2026 |
|---|---|
| Есть ли готовый свободный образ титула 1682 г.? | **Нет.** EEBO-изображения (ProQuest) — по институциональной подписке; IA-копии — производные микрофильма, качество и правовой статус переиспользования не установлены |
| Права Folger | цифровые изображения Folger в целом — **CC BY-SA 4.0** (требуется указание «Folger Shakespeare Library» и распространение производного под тем же лицензионным типом); на уровне предмета возможны исключения, отмечаемые полем «Copyright information». Для экземпляра 228918 наличие опубликованного цифрового ассета и его лицензионное поле **не подтверждены** |
| Права Bodleian | отдельная заявка на образ; EEBO-файл не свободен |
| Права IA/EEBO-микрофильм | микрофильм — продукт UMI/ProQuest; переиспользование не автоматическое |
| Итог | статус `RIGHTS_HOLD`: публиковать титул 1682 г. сейчас нельзя ни по одному из найденных файлов. Требуется либо заказ у Folger с проверкой CC BY-SA, либо разрешение Bodleian, либо письменное разрешение ProQuest |

### 5.5. Что нужно заказать (формулировки для запроса)

1. Folger: «digital image of the title page, copy 228918 (ESTC R231290, Wing C3711aA), plus the licence status of that specific image».
2. Bodleian: образ титульного листа экземпляра, с которого снят EEBO 21:5 (image 48355), с указанием шифра.
3. При невозможности — указать в статье, что иллюстрация отсутствует по правовым причинам, и дать транскрипцию титула с указанием состояния. **Подмена титула 1684/1699/1864 годов недопустима.**

---

## 6. Перечень доступных подлинников (сводка)

| № | Объект | Год | Доступ | Класс | Ограничение |
|---|---|---|---|---|---|
| 1 | *Supplement* (2-е изд.), EEBO-TCP `A25478` | 1676 | полный текст | `A1` | права TCP: CC0 для транскрипции, изображения отдельно |
| 2 | *Bibliotheca Charnockiana*, IA + EEBO (BL) | 1680 | полный текстовый слой | `A1` | OCR испорчен; **нет экземпляра с ценами** |
| 3 | *Treatise of Divine Providence*, `A32726` | 1680 | полный текст | `A1` | — |
| 4 | *Sermon on 2 Cor. V. XIX*, `A32722` | 1680 | полный текст | `A1` | статус «чужого» издания — гипотеза |
| 5 | *Sayings* broadside, `B02133` | 1680 | полный текст + визуальная коллация | `A1`+`A1-scan` | два состояния |
| 6 | *New Poems*, `A52960`; *Elegy*, `A39134` | 1680 | полный текст | `A1` | — |
| 7 | Johnson, *Eklampsis*, `A46911` | 1680 | полный текст | `A1` | — |
| 8 | *Several Discourses*, `A32723` | 1682 | полный текст (866 с.) | `A1` | **титульный лист по образу не верифицирован** |
| 9 | *Supplement*, `A32724` | 1683 | полный текст | `A1` | — |
| 10 | *Works* Vol. I–II, ESTC R12522 / R11740 | 1684 | каталожные записи с полной коллацией; Vol. II — текстовый слой IA | `A1`/`A1-scan` | титул Vol. I в микрофильме утрачен (по записи EEBO 559:1) |
| 11 | *Two Discourses* | 1699 | запись + текст `B20167` | `A1` | — |
| 12 | Parsons, *Works* 9 т.; Nichol, *Complete Works* 5 т. | 1815–1866 | IA/сканы | `A1-scan` | состав томов и текст Маккоша не сверены |
| 13 | Экземпляры из библиотеки Чарнока | — | **не найдено ни одного** с доказанным провенансом | — | Пирсон 2010: «not … of any of Bassett's, Charnock's, or Coga's» |

---

## 7. Ошибки и неточности статьи № 2 (PR #971, `charnock-biography-02-working.md`)

Оценка по тексту, полученному через `gh api` (файл 183 строки). Формулировки ошибок даны как исправления, готовые к внесению.

| № | Место в статье | Что сказано | Проблема | Исправление |
|---|---|---|---|---|
| E1 | § «1666» | «В передаче позднейших биографов Адамс и Вил называли это собрание его рабочим пространством» | Смешаны два разных предмета: фраза Адамса–Вила относится к библиотеке **конца жизни** (собрание после 1666 г.), а рассказ о пожаре у них **отсутствует** | «Адамс и Вил в предисловии 1680 года называют его библиотеку мастерской, не упоминая пожара; о гибели книг в 1666 году первым печатно говорит Калами в 1727 году» |
| E2 | § «1666» | Пожар подан как установленный факт биографии | Единственное современное свидетельство (Джонсон 1680) ограничено формулой «I believe» и говорит о конкретной бумаге; сводная проверка Пирсона (2010) требует осторожности | Добавить: «ближайшее по времени свидетельство — Джонсон (1680), и оно осторожно сформулировано; явное утверждение о библиотеке появляется только у Калами (1727)» |
| E3 | § «1680, аукцион» | «Каталог включал 31 страницу перечня, помимо вводных листов» | Верно, но без указания, что **число лотов в самом каталоге не напечатано** | Добавить: «общее число лотов в каталоге не проставлено; цифра 1 330 получена сложением разделов и подтверждена Пирсоном (2010)» |
| E4 | там же | Аукцион подан как факт с известным организатором | Аукционер **не назван** на титуле; Миллингтон — вывод по месту и соседней продаже | «Аукционер в каталоге не назван; по месту и по соседней продаже библиотеки Т. Уотсона 8 октября 1680 г. продажу связывают с Эдвардом Миллингтоном» |
| E5 | там же | Не отмечена связь с Кокериллом | Упущен документированный факт: каталог раздавался в лавке Кокерилла «Three Legs in the Poultry», и в самом каталоге анонсированы готовящиеся «Discourses… Of Providence» | Внести как отдельный абзац: распродажа и издательская программа — одно событие |
| E6 | § «1682» | «827 страниц основного текста» | Описано одно состояние из двух; второе состояние (Folger 228918, ESTC R231290) имеет иную коллационную формулу и добавляет импресс Michael Hide в Эксетере | Дать обе формулы и указать, по какому экземпляру цитируется титул |
| E7 | § «1682» | «Следующие издания появились уже в конце XVII века» | Слишком обще; пропущены конкретные ступени | «1684 — *Works* в двух томах in folio; 1699 — „third edition corrected“ (том II — „second edition corrected“)» |
| E8 | прим. 10 | Указаны только Folger 470309 и Google Books | Folger 470309 — воспроизведение **бодлеянского** экземпляра, без строки о Michael Hide; второй линк не идентифицирован | Разделить: бодлеянский оригинал (EEBO 21:5) и фолджеровский экземпляр 228918 (R231290); ссылку Google Books либо идентифицировать, либо снять |
| E9 | прим. 16 | «Перечень отдельных книг пока не прочитан непосредственно» | Устарело: каталог прочитан целиком в текстовом слое | «Текстовый слой оцифровки прочитан полностью; постраничная сверка по образам не проводилась; экземпляр с рукописными ценами не найден» |
| E10 | библиография в целом | Отсутствуют: 1-е изд. *Supplement* 1674 г.; *Supplement* 1683; *Two Discourses* 1699; сокращение Гриффита Уильямса 1797 г.; *Works* 1684 Vol. I и II как отдельные единицы; 1699 «third edition corrected» | Неполная хронология при заявленной задаче «построить точную библиографию» | Внести перечисленные позиции с Wing/ESTC |
| E11 | § «1682», прим. 11 | Предисловие 1680 г. цитируется по переизданию 1864 г. и по современному английскому переводу | Двойная передача; первичный набор доступен (1684, «To the Reader») | Цитировать по набору 1683/1684 гг. с указанием листа; перепечатку 1864 г. оставить как вспомогательную |
| E12 | общее | Нет ни одной оговорки о правах изображений применительно к титулу 1682 г. | Требование задачи «проверять права отдельно от возраста» не выполнено | Внести статус `RIGHTS_HOLD` и объяснение (EEBO/ProQuest; Folger CC BY-SA требует проверки на уровне предмета) |

---

## 8. Рекомендации для будущих частей

### 8.1. «Учёный» (паспорт II, том 16 § 21.1)

Можно:

- показать профиль библиотеки 1680 г. как **рабочего инструмента**: латинское богословие 372 лота против английского 256; 65 медицинских книг; 192 латинских «разных»; 75 континентальных книг (французский, итальянский, испанский), включая испанскую Библию, Гвиччардини и Макиавелли по-итальянски;
- показать **концентрации авторов** (Эймс 5, Оуэн 13, Стронг 7, Бакстер 10) как свидетельство читательского поля, а не как индекс цитирования;
- ввести одну материальную деталь: непереплетённые памфлеты («incompacti»), проданные связками, — объясняет, почему библиотека физически не сохранилась.

Нельзя:

- выводить врачебную практику из наличия медицинских книг (предисловие 1680 г. прямо говорит «neglecting the practice of Physick»);
- выводить «отсутствие» книги в каталоге как «не читал»;
- использовать каталог как доказательство состава библиотеки **до** 1666 года; Пирсон отмечает, что 80 % проданных книг напечатаны до 1660 г., и сам не решает эту проблему;
- утверждать, что хоть одна книга с провенансом Чарнока известна: таких нет.

### 8.2. «Главная книга» (паспорт VI)

Можно:

- опереть рассказ о происхождении текста на два дословных свидетельства: эпистолу 1682 г. («Transcribed out of his own Manuscripts, by the unwearied diligence of those worthy Persons that undertook it») и эпистолу Vol. II 1684 г. (разделение труда, взаимная сверка, «Ingenious person» при печати);
- показать, что сам Чарнок не успел: по эпистоле 1682 г. он работал над этим предметом «about three years before he died», а рассуждение о долготерпении (Наум 1:3, с. 787) осталось незавершённым;
- использовать консорциум импресса как книговедческий факт: пять книгопродавцев + провинциальный распространитель в Эксетере.

Нельзя:

- описывать издание одной коллацией без указания состояния (см. § 3.3);
- публиковать титул 1682 г. без решения вопроса прав (§ 5.4);
- приписывать «незавершённость» небрежности редакторов: она засвидетельствована как обстоятельство смерти автора.

### 8.3. «Другие книги» (паспорт VII)

Можно:

- различать три потока текста: **автографы**, **стенограммы двух постоянных слушателей**, **посторонние слушательские записи**;
- документировать конфликт: предисловие 1680 г. прямо называет чужие публикации «imperfect Notes» и говорит, что дефекты встречались «more than once»;
- дать точную цепочку: 1680 *Providence* (8°, Cockerill) → 1683 отдельный выпуск в 94 с. (Wing C3712 Variant, природа не установлена) → 1684 *Works* I–II (folio, с портретом R. White) → 1684/1685 отдельное 8° *Discourse of Divine Providence* → 1699 *Two Discourses* (Veel, «from his original manuscripts») → 1699 *Works* «third edition corrected»;
- отдельно отметить 1699 год как последний, где рукописи ещё были в руках редактора: через 19 лет после смерти Вил публикует два рассуждения «из оригинальных рукописей», то есть архив сохранялся и был доступен.

Нельзя:

- называть *Supplement* 1683 вторым томом;
- приписывать 1680 проповедь на 2 Кор 5:19 кругу Адамса–Вила без оговорки;
- переносить дату или объём одного выпуска на всё издание (пример: 94-страничный выпуск 1683 г. и 397-страничный 8° — разные объекты).

---

## 9. Реестр HOLD и следующие действия

| ID | Предмет | Статус | Действие |
|---|---|---|---|
| BH-1 | Постраничный пересчёт лотов каталога 1680 по образам | `ARCHIVE_HOLD` | заказать/просмотреть 35 изображений IA либо EEBO Tract supplement D8:1[2]; сверить суммы по отделам |
| BH-2 | Экземпляр каталога с рукописными ценами | `LOCATOR_HOLD` | проверить: BL S.-C. 923.(2) на наличие помет; Lauderdale set (Christie's 2005) — описание лота не указывает цены именно у Чарнока; искать в BL/Бодлеян/Кембридже по «priced» |
| BH-3 | £366 5s 1d | `SINGLE_SOURCE_UNVERIFIED` | не использовать как факт; при находке BH-2 — пересчитать |
| BH-4 | Имя аукционера | вероятностная атрибуция | искать письма/счета Миллингтона 1680 г.; проверить, нет ли имени в других экземплярах титула |
| BH-5 | Титульный лист 1682, образ | `RIGHTS_HOLD` | запрос Folger (228918) и Bodleian (EEBO 21:5) |
| ~~BH-6~~ | ~~Цитата Калами «not large»~~ | **ЗАКРЫТ 2026-11-16** | Источник найден: **Палмер 1775, т. I, с. 161**, а не Калами. Калами 1713 и 1727 (оба тома) оборота «not large» не содержат. Атрибуция Book Owners Online исправлена: `ATTRIBUTION_CORRECTED`. См. § 1.3–1.4 |
| BH-11 | Локатор «Калами 1727, т. III, с. 81» в томах 00/01/03 | **ИСПРАВЛЕНО 2026-11-16** | Верно: **т. I, с. 81** (скан 159, колонтитул «in London, Westminster and Southwark. 81»). Исправлено в 01 §2.9E, 03 §3G, 18 §1.1 |
| BH-12 | «Thomas Gataker» в цитате Калами 1727 | **ИСПРАВЛЕНО 2026-11-16** | В оригинале **Cawton** (сверено по скану). Исправлено в 01, 03, 04; совпадает с Johnson, p. 39. Оценка Джонсона меняет смысл: не «второй после корифея века», а «второй в своём кругу» |
| BH-13 | Палмер 1775 как самостоятельный свидетель | `A1` получен, **не исчерпан** | Т. I, с. 159–162 прочитан. Палмер — первый, кто: называет «studied physic»; локализует патристический портрет в предисловии Джонсона; объясняет незавершённость атрибутов смертью автора. Требуется полная сверка с 1713/1727 на предмет остальных добавлений Палмера (изд. 1802, `nonconformistsme01cala_0`, другое) |
| ~~BH-14~~ | ~~Свидетельство о саутворкском служении «7 or 8 persons»~~ | **ЗАКРЫТ 2026-11-16** | Источник — **Джонсон, p. 37** (том 09, §4.2): «In Southwark, where seven or eight… owned their conversion». Палмер 1775, т. I, с. 159 лишь пересказывает. `A1` уже был в корпусе; проверка не требовалась |
| BH-7 | Природа выпуска 1683 г. в 94 с. (Wing C3712 Variant) | `CATALOG_ONLY` | сравнить с 397-страничным 8° и с блоком *Providence* в *Works* 1684 |
| BH-8 | 1702 «3rd ed.» в Research | подозрение на ошибку | снять или дать локатор; 1699 г. сам себя называет «third edition corrected» |
| BH-9 | Полные имена переписчиков («J. Wichens», «Ashton») и «Ingenious person» | `LOCATOR_HOLD` | читать сноски 1684 г. по образам, не по OCR |
| BH-10 | Состав 9-томного Парсонса и 5-томного Николя | `CATALOG_ONLY` | сверить тома по IA/каталогам, прежде чем говорить о «реальных отличиях редакций» |

---

## 10. Счётчик этого прохода (для журнала запросов)

| Срез | `web_search` | `fetch_page` | Пояснение |
|---|---:|---:|---|
| Продолжение 16.11.2026 (после передачи) | ≈14 | ≈46 | Поиски: «366 5s 1d», цены и итоги аукциона, Калами и пожар, Wing C3711A, ESTC R15604, Michael Hide Exeter, priced copies, Lawler, Supplement 1674, Two Discourses 1699, Folger CC BY-SA. Чтения: Пирсон (chunks 2–9), IA-каталог 1680 (chunk 4 + ранее 0–7), IA-метаданные двух микрофильмов 1682, ESTC R15604 / R231290 / R24823 / R21459(контроль), Folger записи 147608, 470309, 126705, 133622, 134068, 148053, 200087, 846678, 51421, Lawler (chunks 13–19, 30), BM *List of Catalogues* (chunks 0–2), Christie's Lauderdale (chunks 1, 3), Folger CC BY-SA (Folgerpedia) |

| Проход BH-6 (16.11.2026, закрытие HOLD) | 0 | ≈14 | Чтения: IA full-text `continuationofac01cala` (запросы «Library was burnt», «not large», «no Notes in the Pulpit», «Prefatory Epistle»), `continuationofac02calaiala` («Charnock», «not large»), `bim_…1713_2` («Library», «burnt», «Applauded», «Cawton», «Senior Proctor», «not large»), `nonconformistsm01cala` («Charnock», «not large»), плюс `djvu.txt` chunks 41, 43–45, 61–64 (Калами 1727) и 57, 63–64 (Палмер 1775), метаданные двух объектов IA, `advancedsearch` по *Nonconformist's Memorial*. Поисков не было: задача решалась адресными чтениями известных объектов |

Ограничения счёта: числа приблизительны; видимые результаты поиска не равны уникальным URL; часть страниц открывалась повторно для снятия неоднозначности.

---

## 11. Сводка в seven lines

1. Пожар 1666 г. стоит на одном современном свидетельстве, сформулированном как мнение (Джонсон 1680), и на одном позднем — **Калами 1727, т. I, с. 81**; место, размер и состав погибшего собрания не документированы, кроме одного названного документа. Знаменитое «not large» Калами **не принадлежит**: это **Палмер 1775, т. I, с. 161**, склеивший фразу Адамса–Вила 1680 г. с фразой Калами 1727 г.
2. Каталог 1680 г. прочитан целиком: он не содержит ни общего числа лотов, ни суммы выручки, ни имени аукционера, ни упоминания пожара.
3. Число 1 330 — арифметика разделов каталога, сходящаяся по двум независимым линиям (Пирсон; суммы 110+135+127=372 и 24+225+26=275).
4. £366 5s 1d — одно современное свидетельство без раскрытого первоисточника; в BM-экземпляре каталог не помечен как priced.
5. Аукцион документирован по месту и дате; аукционер не назван; каталог раздавался в лавке Кокерилла, и в нём уже анонсированы готовящиеся посмертные «Discourses».
6. Издание 1682 г. существует в двух состояниях (C3711 и C3711aA с импрессом Michael Hide в Эксетере); титульный лист по образу не верифицирован и по правам закрыт.
7. Редакторская цепь 1680–1699 документирована дословно: два переписчика с взаимной сверкой, два корректора-редактора, третий наблюдатель за печатью, стенограммы двух постоянных слушателей и прямые жалобы на «imperfect Notes» посторонних изданий.
