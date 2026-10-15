# W0 — Source registry: учебники, монографии, первоисточники, лексикография

**Дата:** 2026-10-07
**Владелец:** библиографический SSOT корпуса
**Статус:** `CURRENT / REGISTRY / БИБЛИОГРАФИЧЕСКАЯ ЗАПИСЬ ≠ ДОСТУП ≠ ПРАВА ≠ ЦИТАТА`
**Machine mirror:** [`../data/redemption-corpus-authority-2026-10-07.json`](../data/redemption-corpus-authority-2026-10-07.json) → `sourceRegistry`

---

## 0. Как читать реестр

Каждая запись имеет пять полей состояния. Они независимы и не смешиваются (AGENT_RULES §1).

```text
CLASS      A1 A2 A3 B1 C D            (класс источника)
ACCESS     FULL = полный объект получен и прочитан
           PART = часть прочитана (preview, index, глава)
           NONE = только библиографическая запись
LOCATOR    YES = страница/раздел/статья проверены по объекту
           NO  = локатора нет
RIGHTS     PD / PD-TRANSLATION-CHECK / OWNER-ONLY / UNKNOWN
PUB        ALLOWED / HOLD
```

Пустое или неполное состояние **не** означает «можно процитировать». Строки с `ACCESS: NONE` — это очередь acquisition, а не источники.

**Что уже верифицировано в этой волне (2026-10-07, поисковые проверки).** Проверены библиографические описания и оглавления: Мюррей (Eerdmans, 1955; часть I, главы I–V; часть II, главы I–X; в издании Banner of Truth 2014 оглавление даёт стр. 51 для главы «The Extent of the Atonement»); Gibson & Gibson (P&R, 2013, 704 pp, полные оглавление и список авторов глав); том 10 «Works» Оуэна (состав по издательскому оглавлению Banner of Truth); текст Второй главы постановлений Дортского синода в переводе 1840 г. (первичная страница, сохранена в `10_...`); фрагмент комментария Кальвина на 1 Ин. 2:1–2 (CCEL, страница комментария, проверена). Всё остальное — `ACCESS: NONE` или `PART`.

## 1. Слой P — первоисточники спора (конфессиональные и соборные акты)

> **Правило резервирования строки.** «Известное имя» не попадает в реестр, пока не подтверждено, что данный конкретный текст говорит об extent. Пустые строки-памятники в этом реестре запрещены: ниже нет ни одной записи, добавленной «для веса списка».

| ID | Запись | CLASS | ACCESS | LOCATOR | RIGHTS | PUB | Для чего |
|---|---|---|---|---|---|---|---|
| `RED-SRC-0001` | **Canons of the Synod of Dort (1618–1619), Head of Doctrine II «Of the death of Christ, and the redemption of men thereby»**, Art. I–IX. Англ. пер. в издании: *The Constitution of the Reformed Dutch Church of North America* (1840) | A3 | FULL (Arts I–IX Head II, прочитаны на источнике) | YES (глава/статьи; перевод 1840) | PD (перевод 1840 — проверить статус редакторского аппарата) | HOLD | hinge-документ: ценность/достаточность (III–IV), всеобщее предложение (V), вменение вины неверия (VI), действенность и замысел (VIII–IX). Сохранён в `10_...` |
| `RED-SRC-0002` | Те же постановления, **Rejection of Errors по Второй главе** + «Errors of the Remonstrants» | A3 | NONE | NO | PD (вероятно) | HOLD | без них Дорт читается наполовину; обязательны для честного описания того, *что именно* осуждено |
| `RED-SRC-0003` | **The Remonstrance of 1610** (пять статей, лат. «Actio»/«Exhibitio articulorum»), в проверяемом издании (акты коллоквиума в Гааге 1610 / латинский текст + англ. пер.) | A2 | NONE | NO | PD | HOLD | позиция противника в её собственных словах; обязательна до любого пересказа «арминиане учат…» |
| `RED-SRC-0004` | **Acts of the Synod of Dort** (session minutes, дела о Remonstrants, подписания) | A2 | NONE | NO | PD | HOLD | кто, что и в какой формулировке принял; разница между «canons» и «acts» |
| `RED-SRC-0005` | **Westminster Confession of Faith**, гл. VIII «Of Christ the Mediator», XI «Of Justification», XXV? (только по проверке), + Larger/Shorter Catechism (вопросы об умилостивлении? — уточнить по тексту) | A3 | NONE | NO | PD | HOLD | что реально говорит символ о простирании (известно, что WCF не использует слово «limited»); обязательно к полному чтению VIII |
| `RED-SRC-0006` | **Savoy Declaration (1658)** и **Second London Baptist Confession (1689)**, гл. VIII; 1689 гл. XI | A3 | NONE | NO | PD | HOLD | баптистско-реформатская рецепция: важно для сайта (наш контекст — евангельский баптизм) |
| `RED-SRC-0007` | **Belgic Confession (1561), Arts. XX–XXI**; **Heidelberg Catechism (1563)** — вопросы о жертве, умилостивлении и посреднике (номера вопросов и Lord's Days уточнить по тексту издания) | A3 | NONE | NO | PD | HOLD | до-Дордрехтская формулировка; «of the same eternal and infinite essence» и «for our sins» |
| `RED-SRC-0008` | **Formula Consensus Helvetica (1675)** — анти-Амиралдское соглашение | A3 | NONE | NO | PD | HOLD | показывает, что спор о простирании внутри реформатства был живым и институциональным; важная «тонкость» |
| `RED-SRC-0009` | **Акты французских национальных синодов** по делу Amyraut (Alençon? Charenton? Loudun?) — точные года и решения уточнить по изданиям актов | A2 | NONE | NO | PD | HOLD | без них «Saumur controversy» — городская легенда |

## 2. Слой O — первоисточники: Писание и его версии

| ID | Запись | CLASS | ACCESS | LOCATOR | RIGHTS | PUB | Для чего |
|---|---|---|---|---|---|---|---|
| `RED-SRC-0101` | **NT греческий текст: NA28/ECM Catholic Epistles & Pauline** (издание фиксируется) | A1 | NONE | NO | UNKNOWN | HOLD | оригинал для 1 Ин. 2:2; 2 Кор. 5; Рим. 3, 5; 1 Тим. 2; Тит. 2; аппарат |
| `RED-SRC-0102` | **BHS / OT еврейский текст** (издание фиксируется) | A1 | NONE | NO | UNKNOWN | HOLD | Ис. 53; Лев 16–17; Втор. 7; Иез. 18; Пс. 49, 130 |
| `RED-SRC-0103` | **LXX (Göttingen или Rahlfs — выбрать и записать)** | A1 | NONE | NO | UNKNOWN | HOLD | `ἱλάσ*`-ряд; «умилостивилище»; для связи NT-языка с греко-еврейским культом |
| `RED-SRC-0104` | **Синодальный перевод** — через верифицированный модуль `../BIBLE_CORPUS/` (кандидат CrossWire `RusSynodal` 1.9.1, PD по официальному реестру CrossWire; побайтно ещё не получен) | A1 | NONE (зависимость) | NO | PD-CLAIM-UNVERIFIED | HOLD | все библейские цитаты; без закрытия этой зависимости ни одной цитаты Писания в статьях |
| `RED-SRC-0105` | **Кассиановский Новый Завет** | A1 | NONE | NO | `PERMISSION_REQUIRED` (см. `../BIBLE_CORPUS/00_...`) | HOLD | как переданы `ἱλασμός`/`ἀγοράζω` в русской евангельской традиции |
| `RED-SRC-0106` | **Церковнославянский НЗ (для термина «искꙋплєнїе»/«умилостивлєнїе»)** | A1 | NONE | NO | PD (текст) | HOLD | история русско-язычного термина |

## 3. Слой L — лексикография (без неё спор о «все» и «умилостивление» не решается)

| ID | Запись | CLASS | ACCESS | LOCATOR | RIGHTS | PUB | Для чего |
|---|---|---|---|---|---|---|---|
| `RED-SRC-0201` | BDAG 3rd ed., статьи: `λύτρον`, `ἀντίλυτρον`, `ἀπολύτρωσις`, `ἀγοράζω`, `ἐξαγοράζω`, `ἱλάσκομαι`, `ἱλασμός`, `ἱλαστήριος/ἱλαστήριον`, `καταλλαγή`, уточнить полный список ряда | B1 | NONE | NO | UNKNOWN | HOLD | основной греко-английский лексикон; каждая статья — с точной страницей |
| `RED-SRC-0202` | TDNT (англ.) / KITTEL — статьи `λύτρον`-ряда, `ἱλάσ*`-ряда, `καταλλαγή` | B1 | NONE | NO | UNKNOWN | HOLD | history-of-religions слой, с которым спорил Dodd; цитировать только по страницам |
| `RED-SRC-0203` | NIDNTTE (4 vol.) | B1 | NONE | NO | UNKNOWN | HOLD | современная замена TDNT-упоминаний |
| `RED-SRC-0204` | HALOT (2nd ed.) — `כָּפַר`, `גָּאַל`, `פָּדָה`, `רָבִים`, `כֹּל` | B1 | NONE | NO | UNKNOWN | HOLD | еврейский ряд; `pi'el` `כפר` «покрыть/очистить»; семитская идиома `רַבִּים` |
| `RED-SRC-0205` | NIDOTTE / TLOT (Harris–Taylor) — `גָּאַל`, `פָּדָה` | B1 | NONE | NO | UNKNOWN | HOLD | кин-редимер и искупление в ВЗ |
| `RED-SRC-0206` | Girdlestone, *Synonyms of the Old Testament* (1897) | B1 | FULL? NONE | NO | PD (проверить перепечатку и редакторский аппарат) | HOLD | доступная PD-лексикография: `redeem` vs `atonement` |
| `RED-SRC-0207` | Trench, *Synonyms of the New Testament* (1864) | B1 | NONE | NO | PD | HOLD | классический разбор `ἀγοράζω`/`ἀπολύτροω`/`λύτρον`; полезно для «что русское слово теряет» |
| `RED-SRC-0208` | Moisés Silva (ed.), *NIDNTTE2? / New International Dictionary of NT Theology*, 2nd ed. — статьи по ряду | B1 | NONE | NO | UNKNOWN | HOLD | сверка с BDAG |
| `RED-SRC-0209` | Wallace, работа о семантическом диапазоне `πᾶς`, используемая в споре об extent (обычно указывают как богословскую диссертацию 1982 г., Dallas Theological Seminary) — **библиографическое описание НЕ подтверждено; найти и подтвердить или исключить** | C | NONE | NO | UNKNOWN | HOLD | ровно тот тип «известной ссылки», который чаще всего цитируют не читая |
| `RED-SRC-0210` | Конкорданс Нового Завета (точное издание фиксируется при использовании) — для usage-подсчётов `πᾶς + gen.`, `ὑπέρ + gen.` | A1 | NONE | NO | UNKNOWN | HOLD | количественная база вместо интуиций |

## 4. Слой C — комментарии по ключевым locus

| ID | Запись (место в комментарии) | CLASS | ACCESS | LOCATOR | RIGHTS | PUB |
|---|---|---|---|---|---|---|
| `RED-SRC-0301` | Calvin, *Commentaries on the Catholic Epistles*, на 1 Ин. 2:1–2 (англ. пер.; CCEL-страница проверена в этой волне) | A1 | FULL (фрагмент прочитан) | YES | PD (перевод 19 в. — проверить статус) | HOLD (нужен русский/англ. цитатник постранично) |
| `RED-SRC-0302` | Calvin, на 2 Пет. 2:1; на Евр. 2:9, 9–10; на Рим. 3:25, 5:6–21; на Ин. 6, 10, 17 | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0303` | Calvin, *Institutes*, III.21–24 (об election и «all») | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0304` | **Owen, *The Death of Death in the Death of Christ*** (1645), Books I–IV; Book IV — ответы на аргументы за universal redemption (в оглавлении Banner-издания: «An unfolding of the remaining texts of Scripture produced for the confirmation of the first general argument for universal redemption») | A1 | NONE | NO | PD (текст 17 в.; редакторский аппарат и предисловие Packer — нет) | HOLD |
| `RED-SRC-0305` | Owen, *A Display of Arminianism* (1643) — том 10 Works | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0306` | Owen, *Of the Death of Christ* (в т. 10 Works, направленное против Baxter) | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0307` | Owen, комментарии к Евреям (Works, тома с экспозицией Евр. 2 и 9–10) — точные тома и страницы уточнить | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0308` | **Thomas Goodwin**, Works (в т. ч. трактаты об искуплении/применении) — томизация по изданию 1663/1861–65 уточняется | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0309` | **John Bunyan**, *A Discourse of the Sufferings of Christ* (17 в.) | A1 | NONE | NO | PD | HOLD | пастырский слой, доступный и русскому читателю |
| `RED-SRC-0310` | **John Gill**, Commentary on Isa 53, на 1 Ин. 2:2, на 2 Пет. 2:1; *Body of Divinity* | A1 | NONE | NO | PD | HOLD | **владелец цитат — `../Джон Гилл/`**; наш корпус только заказывает claims |
| `RED-SRC-0311` | **Baxter**, *Aphorismes of Justification* + его учение о «universal redemption» (точное издание и приложение уточнить) | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0312` | **Manton**, ответы Baxter'у (уточнить трактат/том) | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0313` | **Davenant**, *De Morte Christi, Dissertatio Dubia* (1650) и англ. перевод (год и место уточнить) | A1 | NONE | NO | PD | HOLD | различение «sufficiency of redemption / of acceptance» |
| `RED-SRC-0314` | **Amyraut**, *Brief Traicté de la prédestination* (1634?) и *Traicté de la prédestination et de ses dépendances* (1658) — лат. и фр. издания | A1 | NONE | NO | PD | HOLD | гипотетический универсализм по первоисточнику |
| `RED-SRC-0315` | **Socinus**, *De Iesu Christo Servatore* (1578) | A1 | NONE | NO | PD | HOLD | то, против чего писал Grotius и что Дорт не называет прямо |
| `RED-SRC-0316` | **Grotius**, *Defensio fidei catholicae de satisfactione Christi adversus Faustum Socinum* (1617) | A1 | NONE | NO | PD | HOLD | рождение «governmental»-логики; важно для §4 модели `M-07` в `04_...` |
| `RED-SRC-0317` | **Anselm**, *Cur Deus Homo* (1099), кн. I–II | A1 | NONE | NO | PD | HOLD | satisfactio; «honestas» vs «merit» |
| `RED-SRC-0318` | **Aquinas**, *ST* III, qq. 46–52 (особенно q. 48, a. 6? — уточнить по тексту) | A1 | NONE | NO | PD | HOLD | средневековый корень различения sufficiency/efficiency |
| `RED-SRC-0319` | **Peter Lombard**, *Sentences* III, dd. 12–23 | A1 | NONE | NO | PD | HOLD | откуда различение пошло в схоластику |
| `RED-SRC-0320` | **Turretin**, *Institutes of Elenctic Theology*, locus о смерти Христа и о простирании (номер вопроса уточнить) | A1 | NONE | NO | PD | HOLD | реформатская ортодоксия: «sufficiens/efficax», полемика с Amyraut и Socinus |
| `RED-SRC-0321` | **Voetius**, *Selectarum theologicarum disputationum* (частично о простирании) | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0322` | **Mastricht**, *Theoretico-practica theologia* — soteriologia | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0323` | **Cocceius**, *Summa doctrinae de foedere et testamento* — для «covenant of redemption» | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0324` | **Brakel** (Wilhelmus à Brakel), *Redelijke Godsdienst* — soteriologia | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0325` | **Hodge, Charles**, *Systematic Theology* (1871–73), том о «The Mediatorial Work of Redemption» — глава об extent | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0326` | **A. A. Hodge**, *Outlines of Theology* — глава об extent | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0327` | **Shedd, W. G. T.**, *Dogmatic Theology* (1863?/1874? — уточнить) | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0328` | **Warfield**, статьи о примирении/умилостивлении ( exact essay titles уточнить в Warfield Works) | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0329` | **Dabney**, *Discussions* (том и эссе об extent уточнить) | A1 | NONE | NO | PD | HOLD |
| `RED-SRC-0330` | **McLeod Campbell**, *The Nature of the Atonement* (1856) | A1 | NONE | NO | PD | HOLD | классика возражения «universal Fatherhood» против satisfaction-extent |
| `RED-SRC-0331` | **Finney**, *Systematic Theology* (1851/1878), главы об atonement | A1 | NONE | NO | PD | HOLD | governmental/moral-government view изнутри |
| `RED-SRC-0332` | **Ritschl**, *The Christian Doctrine of Justification and Reconciliation* | A1 | NONE | NO | PD (перевод проверить) | HOLD | модернизм-слой для полноты карты |

## 5. Слой M — современные монографии и учебники (защищённые правами; в Drive — только запись + легальный канал)

| ID | Запись | CLASS | ACCESS | LOCATOR | RIGHTS | PUB | Примечание |
|---|---|---|---|---|---|---|---|
| `RED-SRC-0401` | **John Murray, *Redemption Accomplished and Applied***, Eerdmans, 1955; перепечатки: Banner of Truth (2014, 200 pp; с предисл. Trueman в издании 2015 — уточнить, какое именно) | B1 | NONE | PART (оглавление проверено: I. Necessity, II. Nature, III. Perfection, **IV. Extent (стр. 51 в изд. Banner)**, V. Conclusion; часть II — ordo applicationis) | COPYRIGHT | HOLD | **центральный учебник серии.** Оглавление подтверждено издательскими данными; текст глав ещё не читан в этой волне |
| `RED-SRC-0402` | **David J. Gibson & Jonathan M. Gibson (eds.), *From Heaven He Came and Sought Her: Definite Atonement in Historical, Biblical, Theological, and Pastoral Perspective***, P&R, 2013, 704 pp | B1 | NONE | PART (полное оглавление + авторы глав подтверждены; страницы начал глав: ch.5 → 121, ch.6 → 143, ch.7 → 165, ch.12 → 289, ch.13 → 331, ch.14 → 375, ch.15 → 401, ch.16 → 437, ch.17 → 461, ch.18 → 483, ch.19 → 517 — по издательскому оглавлению) | COPYRIGHT | HOLD | самый полный современный корпус защитников; 23 главы |
| `RED-SRC-0403` | Henri A. Blocher, «Jesus Christ the Man: Toward a Theology of Definite Atonement» (гл. 20 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | богословская «тонкость»: почему «человек Христос» |
| `RED-SRC-0404` | Thomas R. Schreiner, «“Problematic Texts” for Definite Atonement in the Pastoral and General Epistles» (гл. 14 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | методологически лучший образец: защитник честно перечивает трудные тексты |
| `RED-SRC-0405` | Jonathan Gibson, «For Whom Did Christ Die? Particularism and Universalism in the Pauline Epistles» + гл. 13 (оба в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | Павлова exegesis |
| `RED-SRC-0406` | Garry J. Williams, «The Definite Intent of Penal Substitutionary Atonement» и «Punishment God Cannot Twice Inflict: The Double Payment Argument Redivivus» (гл. 17–18 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | double-payment-аргумент: защита |
| `RED-SRC-0407` | Lee Gatiss, «The Synod of Dort and Definite Atonement» (гл. 6 в `0402`) + его издание/перевод самих канонов (уточнить) | B1 | NONE | NO | COPYRIGHT | HOLD | исторический слой Дорта |
| `RED-SRC-0408` | Amar Djaballah, «“Controversy on Universal Grace”: An Historical Survey of Moïse Amyraut’s *Brief Traitté de la Predestination*» (гл. 7 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | Amyraut по его собственному трактату |
| `RED-SRC-0409` | Carl R. Trueman, «Atonement and the Covenant of Redemption: John Owen on the Nature of Christ’s Satisfaction» (гл. 8 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0410` | David S. Hogg, «“Sufficient for All, Efficient for Some”: Definite Atonement in the Medieval Church» (гл. 3 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | генезис различения §4.1 в `01_...` |
| `RED-SRC-0411` | Michael A. G. Haykin, «“We Trust in the Saving Blood”: Definite Atonement in the Ancient Church» (гл. 2 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0412` | Raymond A. Blacketer, «Blaming Beza: The Development of Definite Atonement in the Reformed Tradition» (гл. 5 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | тезис о «двойной предестинации → double extent» — обязателен к спору |
| `RED-SRC-0413` | Paul Helm, «Calvin, Indefinite Language, and Definite Atonement» (гл. 4 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0414` | J. Alec Motyer, «“Stricken for the Transgression of My People”: The Atoning Work of Isaiah’s Suffering Servant» (гл. 10 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | Ис. 53 (наш `A-19/B-14/C-08`) |
| `RED-SRC-0415` | Paul R. Williamson, «“Because He Loved Your Forefathers”: Election, Atonement, and Intercession in the Pentateuch» (гл. 9 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0416` | Matthew S. Harmon, «Definite Atonement in the Synoptics and Johannine Literature» (гл. 11 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0417` | Donald MacLeod, «Definite Atonement and the Divine Decree» (гл. 15 в `0402`); Robert Letham, «The Triune God, Incarnation, and Definite Atonement» (гл. 16) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0418` | Stephen J. Wellum, «The New Covenant Work of Christ: Priesthood, Atonement, and Intercession» (гл. 19 в `0402`) и его книга *The New Covenant Work of Christ* (издание/год уточнить) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0419` | Daniel Strange, «Slain for the World? The “Uncomfortability” of the “Unevangelized” for a Universal Atonement» (гл. 21 в `0402`) | B1 | NONE | NO | COPYRIGHT | HOLD | миссиологический аргумент |
| `RED-SRC-0420` | Sinclair B. Ferguson, «“Blessèd Assurance, Jesus Is Mine”? Definite Atonement and the Cure of Souls» (гл. 22 в `0402`); John Piper, «“My Glory I Will Not Give to Another”» (гл. 23) | B1 | NONE | NO | COPYRIGHT | HOLD | пастырский слой `RQ-5` |
| `RED-SRC-0421` | J. I. Packer, предисловие/введение к переизданию Owen, *The Death of Death* | B1 | NONE | NO | COPYRIGHT | HOLD | важно: именно переиздание вернуло тему в англо-американский евангельский оборот |
| `RED-SRC-0422` | **Leon Morris, *The Apostolic Preaching of the Cross*** (1944; переиздания IVP) — главы о `lytron`-ряду и `hilaros`-ряду | B1 | NONE | NO | COPYRIGHT | HOLD | лексический ответ Dodd'у |
| `RED-SRC-0423` | **Leon Morris, *The Cross in the New Testament*** (1965) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0424` | **John R. W. Stott, *The Cross of Christ*** (IVP, 1986) — раздел о «широте» креста | B1 | NONE | NO | COPYRIGHT | HOLD | умеренный реформатский автор, читающий extent иначе, чем Owen; обязателен для честной карты |
| `RED-SRC-0425` | **Gustaf Aulén, *Christus Victor*** (шв. 1931; англ. пер. — уточнить год/изд.) | B1 | NONE | NO | UNKNOWN (перевод) | HOLD | «victory»-модель `M-06` |
| `RED-SRC-0426` | **Clark H. Pinnock, *The Grace of God and the Will of Man*** | B1 | NONE | NO | COPYRIGHT | HOLD | сильнейшая арминианская защита неограниченного искупления |
| `RED-SRC-0427` | **Stephen J. Amyx, *The Death of Definite Atonement*** (год/издательство уточнить; ранее — его диссертация) | B1 | NONE | NO | COPYRIGHT | HOLD | современный calvinist-критик; обязателен, чтобы серия не была односторонней |
| `RED-SRC-0428` | **David L. Mathers, *The Design of the Atonement: A Historical and Lexical Study*** | B1 | NONE | NO | COPYRIGHT | HOLD | монография именно о «design/extent» |
| `RED-SRC-0429` | Сборник «о намерении искупления» (multiple-views; в англ. лит-ре известен как *The Intent of the Atonement: Which Way Do Evangelicals Argue?*) — **издателя, серию, год подтвердить до внесения в список литературы** | B1 | NONE | NO | COPYRIGHT | HOLD | не включать в публичную библиографию до подтверждения |
| `RED-SRC-0430` | **Jack Cottrell**, *The Faith Once for All* + его soteriological works | B1 | NONE | NO | COPYRIGHT | HOLD | классический арминианский аргумент |
| `RED-SRC-0431` | **Oliver Crisp, *Deviant Calvinism: Broadening Reformed Theology*** — гл. о hypothetical universalism | B1 | NONE | NO | COPYRIGHT | HOLD | современный аргумент за «шотландский»/универсалистский вариант |
| `RED-SRC-0432` | **Colin Gunton, *The Actuality of the Atonement*** | B1 | NONE | NO | COPYRIGHT | HOLD | критик удовлетворения; нужен для честной карты |
| `RED-SRC-0433` | **Gerhard Forde** (о кресте) — точное издание уточнить | B1 | NONE | NO | COPYRIGHT | HOLD | лютеранский слой |
| `RED-SRC-0434` | **R. T. Kendall**, работы об искуплении и о кальвинизме (какие именно — уточнить) | B1 | NONE | NO | COPYRIGHT | HOLD | пример пересмотра позиции внутри reformed-традиции |
| `RED-SRC-0435` | **D. A. Carson, *The Difficult Doctrine of the Love of God*** | B1 | NONE | NO | COPYRIGHT | HOLD | «любовь» — обязательный слой для пастырской части |
| `RED-SRC-0436` | **A. W. Pink** о примирении/искуплении (какой именно трактат — уточнить) | B1 | NONE | NO | UNKNOWN | HOLD | популярен у русскоязычного читателя; требует критической проверки |
| `RED-SRC-0437` | **Spurgeon**, проповеди об искуплении (New Park Street Pulpit / Metropolitan Tabernacle Pulpit — точные номера проповедей и тома уточнить) | B1 | NONE | NO | PD (проверить переводы) | HOLD | пастырский авторитет для русско-евангельской аудитории |
| `RED-SRC-0438` | **Herman Bavinck, *Reformed Dogmatics***, т. 3 (and *Gereformeerde Dogmatiek*, 2nd ed.) — главы о примирении/умилостивлении | B1 | NONE | NO | COPYRIGHT | HOLD | «тонкости» о sufficiency и о «value» |
| `RED-SRC-0439` | **Geerhardus Vos** — о царстве/победе и об искуплении (статьи уточнить) | B1 | NONE | NO | COPYRIGHT | HOLD | библейское богословие |
| `RED-SRC-0440` | **Louis Berkhof, *Systematic Theology*** — глава о примирении, умилостивлении, удовлетворении | B1 | NONE | NO | PD? (уточнить; перепечатки защищёны) | HOLD | стандартный учебник, которым пользуется наш читатель |
| `RED-SRC-0441` | **Robert Letham** и **Donald MacLeod** — их отдельные книги об искуплении/спасении (точные названия подтвердить) | B1 | NONE | NO | COPYRIGHT | HOLD |
| `RED-SRC-0442` | **Steve Chalke & Alan Mann, *The Lost Message of the Cross*** + том-ответ (точный название ответного тома уточнить) | B1 | NONE | NO | COPYRIGHT | HOLD | современная атака на penal substitution; обязана быть в серии, чтобы не выяснилось, что мы её не знаем |

## 6. Слой R — русско-язычная рецепция (самый недоисследованный пласт)

| ID | Запись | CLASS | ACCESS | LOCATOR | RIGHTS | PUB | Зачем |
|---|---|---|---|---|---|---|---|
| `RED-SRC-0501` | **Толковая Библия** под ред. А. П. Лопухина (конец XIX — нач. XX вв.), тома с толкованиями на Послание к Евреям, Соборные послания, 2 Петра | B1 | NONE | NO | PD (проверить перепечатку) | HOLD | единственный широкий русский экзегетический комментарий; важно: составлен в православном институте, требует конфессионального фильтра |
| `RED-SRC-0502` | **Лопухин, *Библейская история Ветхого Завета*** — о первосвященнике, жертвах, Ис. 53 | B1 | NONE | NO | PD | HOLD |
| `RED-SRC-0503` | **Митрополит Макарий (Булгаков)**, *Православное догматическое богословие* (томы; о «искуплении»/«удовлетворении») и *Введение в православное богословие* | B1 | NONE | NO | PD | HOLD | сравнительный слой: как «искупление» строится в восточной традиции (упор на побеждение смерти), и почему русскому читателю близка «victory»-оптика |
| `RED-SRC-0504` | **Протестантская энциклопедия** (СПб., нач. XX в.) — статьи «умилостивление», «искупление», «Кальвинизм», «Арминианство»; точные выходные данные подтверждать по библиотечному каталогу | A2 | NONE | NO | PD (вероятно) | HOLD | как тема называлась по-русски до советского периода |
| `RED-SRC-0505` | **Дореволюционные баптистские/штундистские исповедания и катехизисы** (в т. ч. материалы `../RUSSIAN_BAPTISTS_ARCHIVE/`, `../БАПТИСТЫ РОССИИ/`) | A1 | NONE | NO | см. права архива | HOLD | что пели и исповедовали русские баптисты об «искуплении» — reader-relevant |
| `RED-SRC-0506` | **Пашковское движение**: «Свет и жизнь»?/«Духовная борьба»? (точные названия периодик и годы уточнить по `../RUSSIAN_BAPTISTS_ARCHIVE/`) | A2 | NONE | NO | см. архив | HOLD | кальвинистский слой в российском евангельском движении |
| `RED-SRC-0507` | **«Вопросы богословия»** и материалы евангельских семинарий РФ (точные выпуски и статьи об искуплении — установить) | B1 | NONE | NO | UNKNOWN | HOLD | современная русско-язычная рефлексия; критично, чтобы серия не была переводом англо-спора |
| `RED-SRC-0508` | **Русские переводы Кальвина, Оуэна, Бавинка, Пиппа** — по изданию (права переводчика!): переводы защищены, даже если оригинал PD | B1 | NONE | NO | `TRANSLATION-CHECK` | HOLD | разрешает/запрещает цитировать «по-русски» |
| `RED-SRC-0509` | **Гимнология**: русские евангельские гимны об искуплении/крови (сборники; тексты и права уточнить) | C | NONE | NO | UNKNOWN | HOLD | пастырский слой и «как это уже поётся» |

## 7. Слой X — вторичные обзоры, которые помогают, но не являются доказательством

| ID | Запись | CLASS | ACCESS | RIGHTS | PUB | Роль |
|---|---|---|---|---|---|---|
| `RED-SRC-0601` | Любые энциклопедические/справочные статьи о «limited atonement» (Wikipedia в т. ч.) | C | NONE | — | FORBIDDEN-as-evidence | только discovery; никогда не локатор |
| `RED-SRC-0602` | Монизмы полемических сайтов (обе стороны) | C | NONE | — | FORBIDDEN-as-evidence | discovery + выявление «что реально говорят» |
| `RED-SRC-0603` | TGC/Themelios, «For Whom Did Christ Die?»--type articles | B1 | NONE | COPYRIGHT | HOLD | по правилу `../apostasy/README.md` §7: платформа — не авторитетный слой; заменять на авторскую техническую работу |
| `RED-SRC-0604` | Roger Nicole, «For Whom Did Christ Die?» (эссе; точное издание и страницы подтвердить) | B1 | NONE | COPYRIGHT | HOLD | классический краткий аргумент «многоуровневой» логики extent |
| `RED-SRC-0605` | John Owen, *Death of Death* — историко-текстологические обзоры (Parker? Flood? «A Quest for God's Glory»?) — точные данные подтверждать | B1 | NONE | COPYRIGHT | HOLD | рецепция Оуэна |

## 7a. Поступление объектов в Drive (2026-10-07)

В `07 — СЕРИЯ «ИСКУПЛЕНИЕ» / 01 — PUBLIC DOMAIN LIBRARY` и `/ 04 — CONFESSIONS & HISTORICAL THEOLOGY` находятся четыре PDF-копии (Оуэн, Гудвин, Кальвин «Institutes», Вестминстерское исповедание), принадлежащие владельцу аккаунта. Их наличие меняет статус строк `RED-SRC-0005`, `RED-SRC-0303`, `RED-SRC-0304…0306`, `RED-SRC-0308` с `ACCESS: NONE` на `ACCESS: OBJECT-PRESENT-UNREAD`, и **ничего больше**: `LOCATOR` остаётся `NO`, `RIGHTS` — `PD-CLAIM-UNVERIFIED` (название файла «PD copy» не доказывает, что конкретный набор/вёрстка не защищены), `PUB` — `HOLD`. Побайтный контроль (sha256) этих объектов ещё не выполнялся, поэтому formal `RECEIVED`-state им не присваивается; учёт лежит в `07_W0_DRIVE_MIRROR_RECEIPT_2026-10-07.md` §0a.

## 8. Правила, которые защищают этот реестр от превращения в «много ссылок»

1. **Количество записей не является прогрессом.** Прогресс = закрытые строки `ACCESS: FULL + LOCATOR: YES` для *конкретного claim* (см. claim-регистр в `05_...` и machine JSON).
2. `B1` не может быть единственной опорой quote-safe спорного тезиса (AGENT_RULES §2). Для этой темы это не формальность: почти вся публицистика об extent — `B1`-вторичные пересказы.
3. **Не «у нас есть Пакер», а «мы проверили, что Пакер сказал, на стр. X»**.
4. Все строки в `ACCESS: NONE` — это очередь acquisition, управляемая `05_W0_ACQUISITION_FAMILIES_AND_DRIVE_INTAKE_2026-10-07.md`.
5. **Ни одна строка реестра не даёт права скачать книгу.** Права проверяются отдельно (`RIGHTS`), и «книга есть в open-access на чьём-то сайте» ≠ «её можно хранить и перепубликовать».
6. Русские переводы трактуются как **производные объекты**: оригинал PD, перевод может быть защищён.
7. Реестр не содержит «резервных» и «памятных» строк: запись либо описывает проверяемый объект, либо отсутствует.

## 9. Минимальный состав библиотеки до первой публикации

Чтобы серия была честной, до `W6` надо реально прочитать (а не иметь в списке) минимум:

1. Дорт, Вторая глава (уже есть: `10_...`) + Rejection of Errors (`0002`);
2. Remonstrance 1610 (`0003`);
3. Мюррей, часть I полностью (`0401`);
4. Owen, *Death of Death*, кн. I + хотя бы один полный разбор «всеобщих текстов» (кн. IV) (`0304`);
5. Amyraut-фрагменты по вторичной *и* первичной проверке (`0314` + `0408`);
6. Davenant, ключевое различение (`0313`);
7. один сильный арминианский текст целиком (`0426` или `0430`);
8. один «против satisfaction»-текст (`0432`/`0442`/`0330`);
9. лексические статьи по 6 леммам (`0201`–`0205`).

Только тогда серия получает право называться «заложенной на серьёзные учебники богословия», а не «собравшей список учебников».
