# Агент 2 — аудит строгой аргументации «Кальвин учил определённому искуплению»: где логический шаг доказан, а где нет

**Дата:** 2026-11-17
**Исполнитель:** Agent 2 (ARENA), режим `ONE_SHARED_GOAL`, координатор MAX.
**Ветка:** `arena/0fbd0e42-research`, база `5fab12abd16246a0ff5fab558f11001304f2e970` (`origin/main`).
**Статус:** `RESEARCH / EVIDENCE DELTA / NOT PUBLICATION-READY`. `RIGHTS_HOLD`, `PUBLICATION_HOLD` и `EXEGETICAL_HOLD` родительского корпуса этим документом не снимаются.
**Владение файлами.** Создан только этот файл. Общие главы, `synthesis/02_CONFLICT_LEDGER.md` (в том числе C-17), `synthesis/drafts/article16_*`, `13_`, `15_`, `fathers/16_`, матрица Agent 6 и `docs/research/atonement/*` **не редактировались**. Поправки к ним вынесены в §7 как предложения для MAX. Перед началом работы я проверил открытые PR: 547, 546, 379 и 287–289 не касаются ИСКУПЛЕНИЕ/, поэтому конфликта владения нет.
**Чего здесь нет.** Пять пунктов не передоказываются, и параллельная систематика не строится. Уже полученные корпусом результаты (достаточность/действенность, hard-text cards, особая импетрация, предложение и применение) принимаются как данность. Проверяются только логические переходы.

---

## 0. Краткий ответ

> **Волна 3 (§10, ответ на ревью MAX):** границы каждого `EXPLICIT` сужены. S3-b понижено до `WEAK_INFERENCE` / `TENSION`: в том же трактате на той же странице (CO 9:483) Кальвин говорит, что нечестивые отвергают «victimam, qua expiata sunt mundi peccata». «PRIMARY_VERIFIED» заменено точными осями `evidenceClass` / `accessState` / `locatorState`. Печатная страница 1667 г. — `LOCATOR_HOLD`. Таблица поправок к реестрам — §10.3.
>
> **Волна 2 (§9):** CO 9:484, 9:485 и 8:336 сверены по скану *Corpus Reformatorum*. Моя пометка «Cole sealed… = переводчик» снята: это латынь Кальвина. «solis electis» в CO 9 встречается только об освящении. Добавлено S1-b′: «nec aliud Christi officium… quam ut morte sua in unum congreget Dei filios» — `EXPLICIT`. Главный вывод §0 и §5 не меняется.

1. **Что у Кальвина явно (EXPLICIT).**
   - Спасительное собирание, действенное учение Духом, вера, ходатайство Христа и «наслаждение» Его благом принадлежат только избранным.
   - В одной фразе против Хесхузия, в евхаристическом и полемическом контексте, Кальвин прямо говорит: плоть Христа «не распята» за нечестивых, кровь «не пролита для искупления их грехов» (1667, т. VIII, с. 759).
2. **Что у Кальвина тоже явно, и это нельзя стирать.**
   - Христос «пострадал за грехи всего мира» (Рим. 5:18, его собственная латынь, CO 49:100).
   - «Не подлежит спору, что Христос пришёл для искупления грехов всего мира» (против Георгия Сицилийского, 1667, т. VIII, с. 628).
   - Примирение «предлагается всем» (там же; Рим. 5:18).
3. **Новое в этой волне (NEW_DELTA).**
   - В трактате *De aeterna Dei praedestinatione* Кальвин **сам откладывает** формулу Ломбарда «достаточно за всех, действенно только за избранных»: «Ne valeat in praesens communis illa solutio».
   - Это структурный параллелизм с 1 Ин. 2:2: «verum… nego praesenti loco quadrare».
   - Значит, ни строгая, ни универсалистская сторона не вправе опираться на эту формулу как на собственный довод Кальвина об объёме.
4. **Главная недоказанная посылка строгого вывода.**
   - Строгому выводу нужна посылка: *объём импетрации (за кого принесена жертва) совпадает с объёмом намеренного применения*. У Кальвина её нет.
   - В явном виде эту посылку формулирует Оуэн: *Death of Death*, кн. I, гл. VII, «oblation and intercession… the same personal object».
   - Без неё из «спасение получают избранные» не следует «у смерти Христа нет иного отношения к неизбранным».
5. **Сильнейшая защитимая формулировка.** Кальвин — партикуляр в решении, применении, ходатайстве и действенности. Его тексты **совместимы** со строгим определённым искуплением, а одна фраза против Хесхузия вербально его выражает.
6. **Пока недоказуемо** (по крайней мере на собранной первичной базе):
   - «Кальвин учил оуэновскому определённому искуплению» (импетрация только за избранных, без какого-либо всеобщего отношения смерти);
   - обратное утверждение «Кальвин учил общему искуплению». Это сноска редактора CTS, а не слова Кальвина; см. C-17.

---

## 1. Шкала и правила

| Вердикт | Значение |
|---|---|
| `EXPLICIT` | Утверждение стоит в проверенном тексте Кальвина в нужном смысле и контексте. |
| `STRONG_INFERENCE` | Вывод опирается на явные тексты Кальвина плюс одну посылку, которую Кальвин сам где-то высказывает. |
| `WEAK_INFERENCE` | Нужна посылка, которой у Кальвина нет: её вносят позднейшие авторы (Оуэн, Утрехт 1620) или требует внешняя систематика. |
| `COMPATIBLE` | Текст не противоречит строгому чтению, но и не требует его. |
| `UNDETERMINED` | Собранные первичные тексты допускают оба чтения или молчат. |

Классы свидетельства — по `AGENT_RULES.md`:
- `A1` — первичный текст, проверенный по скану в этой сессии;
- `A2` — первичный документ не Кальвина;
- `B1` — перевод или вторичный источник.

Правило переводчика: английские добавления CTS и Cole, которых нет в латыни, **не являются Кальвином**.

---

## 2. Проверенные первичные локаторы этой волны

Все тексты прочитаны через полнотекстовый поиск Internet Archive (`/fulltext/inside.php`) по сканам. Индекс страницы, который возвращает поиск, совпадает с номером листа (`leafNum`) в `*_page_numbers.json`. Для Romans 1849 это откалибровано так: индекс 216 несёт колонтитул «212 COMMENTARIES ON THE CHAP. V. 19». Для Cole печатные страницы взяты по колонтитулам.

| ID | Текст | Издание (IA id) | Печатная страница | Класс |
|---|---|---|---|---|
| L1 | Кальвин против Хесхузия, *Dilucida explicatio* (1561) | *Opera omnia*, Amsterdam 1667, т. VIII, `bub_gb_6COCD48cJ90C` | скан с. **759** | A1 **Волна 3 (§10.2):** «с. 759» — индекс скана (inside.php), печатная страница 1667 не установлена (`LOCATOR_HOLD`; в томе несколько пагинаций). Основной локатор — CO 9:484. |
| L1e | то же, англ. | CTS *Tracts relating to the Reformation*, vol. 2 (Beveridge), `tractsreformatio02calvuoft` | **527** (лист 531) | B1 |
| L2 | *De aeterna Dei praedestinatione* (1552), раздел против Георгия Сицилийского | 1667, т. VIII, тот же скан | скан с. **628** | A1 **Волна 3 (§10.2):** «с. 628» — индекс скана; основной локатор — CO 8:336. |
| L2e | то же, англ. | H. Cole, *Calvin's Calvinism* (1856), `calvinscalvinis00colegoog` | **150–151** | B1 |
| L3 | Комм. на Рим. 5:18 | CTS *Romans* (Owen, 1849), `commentariesonth00calvuoft` | **211** (комментарий и лат. сноска 3); примечание «— Ed.» на **212** | B1 + лат. A1 в сноске |
| L4 | Комм. на Рим. 8:34 («who intercedes») | там же | **325** (по указателю: «Intercession… of Christ, how to be understood, 325») | B1 |
| L5 | Комм. на Ин. 17:6, 9 | CTS *John*, vol. 2 (Pringle, 1847), `commentaryongosp02calvuoft` | 17:6 — **170**; 17:9 — **172**; «Christ prays for the elect only» — **173** (лист = индекс, калибровка как у L3) | B1 |
| L6 | Комм. на 1 Ин. 2:2 | CTS 1855, `commentariesonca00calv` | **173** (уже в `13_` §2.2) | B1, лат. CO 55:310 в `fathers/16_` §2.2 |
| L7 | Оуэн, *Death of Death*, кн. I, гл. VII | Goold, *Works* X (1850), `worksofjohnowe185010owen` | заголовок главы — индекс 198 (кн. I = с. 157–199 по `14_`) | A2 (не Кальвин) **Волна 3 (§10.2):** класс исправлен на A1 (для позиции *Оуэна*, не Кальвина); прочитаны только синопсис и заголовок главы. |

### 2.1. Дословные тексты, на которые опирается матрица

**L1, 1667 с. 759.** Нормализовано: long-s → s, лигатуры раскрыты.
> «…Et quando tam mordicus verbis adhaeret, scire velim quomodo Christi carnem edant impii, pro quibus non est crucifixa, et quomodo sanguinem bibant, qui expiandis eorum peccatis non est effusus. Fateor quod dicit, adesse ut severum judicem… Sed aliud est comedi, aliud esse judicem.»

- CTS p. 527: «I should like to know how the wicked can eat the flesh of Christ which was not crucified for them? and how they can drink the blood which was not shed to expiate their sins?»
- Несущая аксиома в том же споре (CTS): «Christ, considered as the living bread and the victim immolated on the cross, cannot enter any human body which is devoid of his Spirit».

**L2, 1667 с. 628.** Нормализовано.
> «…Ne valeat in praesens communis illa solutio: Christum sufficienter pro omnibus passum esse, efficaciter tantum pro electis. Magna illa absurditas, ob quam plausum sibi inter suos gregales Monachus quaesivit, apud me nihil habet momenti. Per quascunque mundi plagas dispersi sint fideles, expiationem Christi morte partam ad eos Joannes extendit. Id certe non obstat, quominus reprobi in mundo electis permixti sint. Controversia etiam caret, Christum expiandis totius mundi peccatis venisse. Sed confestim occurrit… Ut quisquis credit… Nec vero qualis sit Christi virtus, vel quid per se valeat, nunc quaeritur: sed quibus se fruendum exhibeat… Quamvis per ipsum offeratur omnibus reconciliatio, peculiare tamen esse electis beneficium, ut in vitae societatem colligantur. Quanquam dum omnibus offerri dico, non ita accipio, quasi ad omnes legatio illa perveniat…»

- Cole p. 150: «we will not permit the common solution… Christ suffered sufficiently for all men; but effectually for his elect alone».
- Cole p. 151: «although reconciliation is offered unto all men, through Him; yet… the great benefit belongs peculiarly to the elect».
- ~~**Добавка переводчика (не Кальвин):** у Cole на с. 151 «but that it is not sealed indiscriminately on the hearts of all… so as to be effectual in them» не имеет соответствия в латыни.~~ **`SUPERSEDED` волной 2 (§9.2):** в CO 8:336 латынь есть: «sed ad quos pervenit, ne eorum quidem cordibus indifferenter obsignatur, ut rata sit». В выписке из 1667 г., сделанной в волне 1, эта фраза была обрезана. Английский Cole здесь передаёт Кальвина, а не переводчика.
- **Локатор CO 8:336** — ~~традиционный, в этой сессии не сверен~~ **сверен в волне 2 (§9.1)**: CR 36 = CO 8, IA `operaquaesupersu0036calv`, лист 210, правая колонка = кол. 336. Цитировать: CO 8:336 + 1667 с. 628 + Cole с. 150–151.

**L3, CTS Romans 1849, с. 211.**
> «He makes this favour common to all, because it is propounded to all, and not because it is in reality extended to all; for though Christ suffered for the sins of the whole world, and is offered through God's benignity indiscriminately to all, yet all do not receive him.»

- Латынь в сноске 3 (OCR): «Nam etsi passus est Christus pro peccatis totius mundi, atque omnibus indifferenter Dei benignitate offertur; non tamen omnes apprehendunt».
- **Примечание редактора, с. 212:** «It appears from this sentence that Calvin held general redemption. — Ed.» Это слова редактора, **не Кальвина**.

**L4, CTS Romans, с. 325.**
> «…as he appears continually, as one who died and rose again, and as his death and resurrection stand in the place of eternal intercession, and have the efficacy of a powerful prayer for reconciling and rendering the Father propitious to us, he is justly said to intercede for us.»

**L5, CTS John vol. 2.**
- с. 172 (17:9): «He openly declares that he does not pray for the world, because he has no solicitude but about his own flock… Christ himself afterwards prayed indiscriminately for all, Father, forgive them… I reply, the prayers which we offer for all are still limited to the elect of God… because we cannot yet distinguish the elect from the reprobate».
- с. 173: «since Christ prays for the elect only, it is necessary for us to believe the doctrine of election».
- с. 170 (17:6): «There was no want of faith or diligence on the part of Christ, to call all men to God, but among the elect only was his labour profitable and efficacious».

**L7, Owen, Works X.** Аргумент кн. I, гл. VII: «reasons to prove the oblation and intercession of Christ to be one entire mean respecting the accomplishment of the same proposed end, and to have the same personal object».

---

## 3. Матрица аргументов

| ID | Текст Кальвина | Строгое утверждение | Необходимая посылка | Лучшее возражение | Вердикт |
|---|---|---|---|---|---|
| **S1-a** | Ин. 17:6 (L5, с. 170); Inst III.1.1 («extra nos… inutile»); Рим. 5:18 (L3, «non tamen omnes apprehendunt») | Спасение действительно получают только избранные | — | Нет | `EXPLICIT` (это никто не оспаривает) |
| **S1-b** | те же | Значит, у смерти Христа **нет иной** спасительной цели или отношения к неизбранным | **P-coext**: объём импетрации (за кого принесена жертва) = объём намеренного применения. Иначе: что не применено, то и не было приобретено/предназначено | Кальвин сам разделяет «quid per se valeat» и «quibus se fruendum exhibeat» (L2) и говорит «passus pro peccatis totius mundi» (L3). P-coext у него не высказана; в явном виде она у Оуэна (L7) | `WEAK_INFERENCE` (уточнено в §9.4: «нет иного *officium*» — у Кальвина явно, «нет иного отношения» — нет) |
| **S1-c** | Inst II.17.4 («cursed… righteousness»; Battles 1:532 — не II.16.5–6, как иногда цитируют) | Удовлетворение есть реальная замена, поэтому оно не может быть «впустую» за неспасённых | P-coext + **P-noDouble**: реальная замена исключает вторичное, обусловленное отношение | Строка доказывает реальность замены для «нас» (верующих), но не говорит, что «нас» исчерпывает возможный объём | `WEAK_INFERENCE` |
| **S2-a** | Ин. 17:9 (L5, с. 172–173) | Ходатайство Христа — только за избранных | — | Лк. 23:34. Кальвин отвечает сам: даже молитва «за всех» в конечном счёте «limited to the elect» | `EXPLICIT` |
| **S2-b** | Рим. 8:34 (L4, с. 325) | Ходатайство есть непрерывно предъявляемая сила смерти и воскресения | — | Нет | `EXPLICIT` (**NEW_DELTA** для S2) |
| **S2-c** | S2-a + S2-b | Значит, предъявляемая действенность смерти ограничена избранными | S2-a, S2-b | Это вывод о **действенности/применении**, а не об объёме жертвы как такового | `STRONG_INFERENCE` (собран из двух явных мест Кальвина) |
| **S2-d** | S2-c + L2/L3 | Кальвин **исключает** различение «всеобщее основание призыва (жертва за весь мир, предложение всем) + особое ходатайство» | **P-same-object** (Оуэн, L7) или отказ от «двойного ходатайства» (Утрехт 1620, Acta pp. 122–123, A2, матрица Agent 6, A.2) | Кальвин явно держит оба полюса: «offertur omnibus reconciliatio» / «peculiare electis beneficium» (L2), «propounded to all / not extended to all» (L3). Тезиса «жертва и ходатайство коэкстенсивны» в его проверенных текстах нет. Цитата «Inst 2.16.16» в `32_` — склейка (`QUOTE_RISK`, уже отмечено там) | `WEAK_INFERENCE` → `UNDETERMINED`. Различение `COMPATIBLE` с Кальвиным, но им **не сформулировано**. Кальвин также не постулирует второе, общее ходатайство за отверженных |
| **S3-a** | Хесхузий (L1, с. 759) | Плоть Христа не распята за нечестивых, кровь не пролита для искупления их грехов | — | — | `EXPLICIT` (в этой ограниченной формулировке). **PRIMARY_VERIFIED** Волна 3: «PRIMARY_VERIFIED» заменено на точные оси (§10.2). |
| **S3-b** | L1 + аксиома о Духе | Это утверждение Кальвина об **объёме** жертвы, в оуэновском смысле | **P-ctx**: евхаристический вопрос («как едят…») переносим на учение об объёме. Плюс **P-sincere**: фраза — не довод ad hominem | (1) Контекст — manducatio impiorum; Христос взят «как духовная пища». (2) Рамка ad hominem: «quando tam mordicus verbis adhaeret». (3) Та же лексика «expiandis… peccatis» утверждается о «totius mundi» в L2 того же тома. (4) Довод работает и при чтении «не распята за них **действенно / как пища**» | `STRONG_INFERENCE` в лучшем случае; спорно. Не `EXPLICIT` для оуэновского объёма **Волна 3 (§10.1, E1): понижено до `WEAK_INFERENCE` / `TENSION`** — на той же странице CO 9:483 нечестивые отвергают «victimam, qua expiata sunt mundi peccata». |
| **S3-c** | «Christum solis electis passum esse» (`01_`:890); «pro solis electis passus est», CO 9:524 (`22_` #11/#998) | Кальвин дословно говорил «только за избранных» | Наличие фразы в тексте | В 1667, т. VIII, по OCR не найдено: «solis electis», «folis electis», «femper dixi» — 0 совпадений. В CTS Tracts II: «always said» — 0; «elect alone» — только о вере (лист 136). Два целевых прохода безрезультатны → `STOP_DISCOVERY` | `INVALID` как verbatim (до предъявления скана). Отсутствие в OCR — не доказательство отсутствия в тексте, но метка «Verified» в `22_` не обоснована Волна 2: в CO 9 единственное «solis electis» — о *освящении*, кол. 485 (§9.3) |
| **S4-a** | 1 Ин. 2:2 (L6; CO 55:310) | «Весь мир» здесь — верующие по всему миру, без отверженных | — | — | `EXPLICIT` |
| **S4-b** | то же | Кальвин выводит партикулярный объём **через** формулу «достаточно/действенно» | Что формула — его аргумент здесь | Он называет формулу «истинной», но «не подходящей к этому месту». В L2 он её «in praesens» откладывает | `INVALID` (формулу нельзя вменять как его довод) Волна 2: «nego praesenti loco quadrare» — устойчивая экзегетическая формула Кальвина (ещё Евр. 5:6, CO 55; §9.5) |
| **S4-c** | то же | Кальвин **отверг** формулу «достаточно/действенно» | Что «nego… quadrare» / «ne valeat» = доктринальное отрицание | «verum esse… fateor» (L6); «in praesens» (L2). «Magna illa absurditas» относится к доводу Георгия, а не к формуле | `INVALID` |
| **S4-d** | L6 + L2 | Из толкования 1 Ин. 2:2 следует, что жертва вообще не относится к отверженным | P-coext + распространение экзегезы одного стиха на учение | В L2 на той же странице Кальвин сначала даёт ту же экзегезу («ad fideles… Joannes extendit»), а затем признаёт «controversia caret… totius mundi peccatis». То есть экзегеза стиха у него **не** исчерпывает вопроса | `WEAK_INFERENCE` |
| **S5-a** | Рим. 5:18 (L3) | Благо «общее всем» лишь по предложению, а не по действительному распространению | — | — | `EXPLICIT` (лучший партикулярный ответ из самого Кальвина) |
| **S5-b** | то же | «passus pro peccatis totius mundi» означает только «за всякого рода людей» | Перечтение «totius mundi» как родового, против прямого смысла | Кальвин сам противопоставляет «весь мир» и «не все принимают», то есть мыслит широкий круг, а не только тех, кто принимает | `WEAK_INFERENCE`. Строгое прочтение обязано **оставить** универсальные слова и объяснять их через различение «exposita / re ipsa extendatur», а не через их удаление |
| **S5-c** | Сноска «held general redemption — Ed.» (с. 212) | «Кальвин учил общему искуплению» | Редактор = автор | Это примечание редактора CTS (`C-08`, `C-17`) | `INVALID` как атрибуция Кальвину |
| **N-1** | L2 | В этом месте Кальвин признаёт искупление за весь мир бесспорным и переносит вопрос на «кому Христос даёт Себя вкусить» | — | Строгие читатели скажут: «totius mundi» = верующие, рассеянные по миру (так он только что толковал Иоанна) | `EXPLICIT` как текст; смысл «totius mundi» — `UNDETERMINED` (оба чтения в одном абзаце) |
| **N-2** | L1 vs L2 (тот же т. VIII; оба «expiandis… peccatis») | Кальвин противоречит сам себе | Обе фразы — в одном и том же отношении | Различение отношений, которое Кальвин сам называет в L2: «quid per se valeat» / «quibus se fruendum exhibeat». L1 говорит о Христе «как пище», вкушаемой только с Духом | Не противоречие, а **ядро напряжения**. Разрешимо через различение, которое Кальвин называет сам, но не через P-coext |

---

## 4. Недоказанные посылки, которые на самом деле несут строгий вывод

1. **P-coext.** Объём импетрации = объём намеренного применения.
   - Где явно: Оуэн, *Death of Death*, кн. I, гл. VII (L7); затем Утрехт 1620 против «double intercession» (A2).
   - У Кальвина: в проверенных текстах не найдено.
   - Куда вписывается: шаги S1-b, S1-c, S2-d, S4-d.
2. **P-same-object.** Жертва и ходатайство имеют один и тот же личный объект.
   - Кальвин даёт **половину** этой посылки (S2-b: ходатайство есть сила смерти) и **отдельно** ограничение ходатайства (S2-a).
   - Обратной импликации «за кого не ходатайствует, за того не умер» он не формулирует.
   - Его ответ на Лк. 23:34 касается молитвы, а не жертвы.
3. **P-ctx.** Евхаристическую фразу против Хесхузия можно переносить на учение об объёме. Не доказано: см. S3-b, возражения (1)–(4).
4. **P-formula.** Формула Ломбарда — довод Кальвина (неважно, «за» или «против»).
   - Ложна для 1 Ин. 2:2 и для L2: оба раза формула выведена из игры для данного места.
   - Положительного доктринального использования формулы Кальвином в этих loci нет.

---

## 5. Сильнейший защитимый вывод и то, что пока недоказуемо

### 5.1. Защитимо сейчас (класс A1/B1 по проверенным сканам)

> У Кальвина Бог по Своему решению собирает в жизнь только избранных. Вера, учение Духом, ходатайство Христа (которое есть предъявление силы Его смерти, Рим. 8:34) и вкушение Христа принадлежат только им (L1, L4, L5, L6). Всеобщность у Кальвина — это всеобщность **предложения** (L2, L3), а не действительного распространения блага (L3, «non… re ipsa»). В одной полемической фразе (L1) он прямо отрицает, что плоть Христа распята, а кровь пролита для искупления грехов нечестивых, вкушающих без Духа. Поэтому строгое определённое искупление **совместимо** с Кальвином и имеет у него текстовую опору. Связать его объём с объёмом решения позволяет сочетание S2-a + S2-b (`STRONG_INFERENCE` для действенности).

### 5.2. Пока недоказуемо

- **(a) Строгая сторона.** «Кальвин учил, что смерть Христа импетрировала искупление исключительно для избранных и не имеет никакого всеобщего отношения». Препятствия:
  - этому нужна P-coext;
  - против стоят собственные слова Кальвина в L2 («controversia caret… totius mundi») и L3 («passus pro peccatis totius mundi»).
- **(b) Противоположная сторона.** «Кальвин учил общему искуплению (в смысле Амиро / гипотетического универсализма)». Препятствия:
  - L1 — явная обратная формулировка;
  - в L2 и L6 Кальвин отказывается строить довод на формуле «достаточно за всех»;
  - примечание «— Ed.» — не Кальвин.
- **Итог.** На собранной первичной базе вопрос об **объёме импетрации у Кальвина** остаётся `UNDETERMINED`. Это совпадает со статусом `TENSION` в C-17 и уточняет его: напряжение лежит **внутри одного тома** (т. VIII, с. 628 и 759).

---

## 6. Фаза 2 — исследователи

| Автор | Работа | Состояние в корпусе | Вердикт |
|---|---|---|---|
| R. Nicole | «John Calvin's View of the Extent of the Atonement», *WTJ* 47.2 (1985): 197–225 | Не прочитана. Библиографию подтвердил web-поиск; в корпусе только упоминания | `HOLD`. По пересказам (Allen и др.) Nicole сам формулирует вывод как «definite atonement **fits better**», то есть как `STRONG/WEAK_INFERENCE`, а не `EXPLICIT`. Через рецензию не верифицировано |
| J. H. Rainbow | *The Will of God and the Cross* (Pickwick, 1990; Princeton Theol. Monograph 22) | Не прочитана; есть только каталожная запись | `HOLD` |
| P. Helm | *Calvin and the Calvinists* (1982) | Только упоминания в `01_` и `05_` | `HOLD` |
| P. Archbald | дисс. WTS 1998 | Не в рабочем пространстве. Тезис о коэкстенсивности жертвы и ходатайства в `32_` опирается на склейку из Inst 2.16.16 | `HOLD`. Не повышать без чтения |
| R. Muller, R. Blacketer | — | Только `fathers/16_` §4 | Новых первичных свидетельств в этой волне не дают; `REVIEW_DEFERRED` |

Новых проверяемых первичных свидетельств из исследовательской литературы в этой волне **не добавлено**. Ни одна книга не считается прочитанной по рецензии.

---

## 7. Предлагаемые поправки (только предложения; файлы не редактировались)

| Цель | Сейчас | Предложение |
|---|---|---|
| `docs/research/atonement/22_…registry…md` п. 11 (стр. ~48–50) и таблица #11 (стр. ~998) | «CO 9:524 … *Christus pro solis electis passus est* … Verified» | Пометить `SUPERSEDED/HOLD`: verbatim не найден в 1667, т. VIII (два прохода OCR); верный locus и формулировка — L1 (1667 с. 759; CTS Tracts II p. 527). Исторические строки не удалять |
| `docs/research/atonement/01_prokopenko_article_review.md:890` | «Nihil aliud dico quam quod semper dixi: Christum solis electis passum esse» | `QUOTE_HOLD` → заменить на L1 с оговорками S3-b |
| `ИСКУПЛЕНИЕ/evidence/AGENT6_…` §4.5 и пункт 7 списка HOLD (`HESHUSIUS_VERBATIM_HOLD`) | «quae non pro ipsis crucifixa est… qui non pro ipsorum peccatis effusus est» (по транскрипциям) | Снять `HESHUSIUS_VERBATIM_HOLD` в части смысла и локатора; исправить wording на «pro quibus non est crucifixa… qui expiandis eorum peccatis non est effusus» (L1). Часть HOLD о «solis electis» сохранить |
| `docs/research/atonement/02_…controversies.md` #17 | «qui non est effusus in peccatorum eorum expiationem», CO 9:484 | Исправить вторую половину по L1; CO 9:484 — ~~`LOCATOR_UNVERIFIED`~~ **сверен в волне 2 (§9.1)**; добавить 1667 с. 759 |
| `ИСКУПЛЕНИЕ/13_` §2.2, `fathers/16_` §2.2, рамка достаточности | Формула «достаточно/действенно» и Кальвин | Добавить параллель L2: Кальвин и в *De aeterna praed.* откладывает формулу «in praesens»; не приписывать её ему как довод об объёме и не утверждать, что он её отверг |
| `docs/research/atonement/32_…` §3, ошибка 3 | Коэкстенсивность жертвы и ходатайства как позиция Кальвина | Уже есть `QUOTE_RISK`. Добавить: ближайшая проверенная опора — Рим. 8:34 (L4) + Ин. 17:9 (L5); результат — `STRONG_INFERENCE` для действенности, `WEAK` для объёма (S2-c/S2-d) |
| C-17 (`synthesis/02_CONFLICT_LEDGER.md`) | `TENSION` | **Не редактировалось.** Для MAX: L2 даёт второе место (помимо Рим. 5:18) с той же структурой. Статус `TENSION` подтверждён, а не снят |

---

## 8. Передача MAX

**ALREADY_PROVEN** — в корпусе до этой волны; принято, не передоказывалось:
- 1 Ин. 2:2: «весь мир» = верующие по миру; формула «верна, но не к месту» (`13_` §2.2, C-06);
- Рим. 5:18: «— Ed.» не Кальвин (C-08, C-17);
- 1 Тим. 2:4: «de hominum generibus»;
- Ин. 17:9: ходатайство за избранных;
- Inst III.1.1: «extra nos inutile»;
- различение предложения и применения;
- Утрехт 1620 против двойного ходатайства — это A2, а не Кальвин.

**NEW_DELTA** (две содержательные позиции волны):
1. **Хесхузий — ~~PRIMARY_VERIFIED~~ (`SUPERSEDED` волной 3: см. оси в §10.2; вердикт S3-b понижен в §10.1).** 1667, т. VIII, скан-индекс 759; CTS Tracts II p. 527. Wording исправлен. Вердикт: `EXPLICIT` в ограниченной формулировке и не более чем `STRONG_INFERENCE` для оуэновского объёма.
2. ***De aeterna Dei praed.*, против Георгия (1667 с. 628; Cole 150–151).**
   - Кальвин откладывает формулу Ломбарда «in praesens».
   - Он признаёт «controversia caret» об искуплении грехов всего мира.
   - Вопрос он переносит на «quibus se fruendum exhibeat»: предложено всем, собирание — особое благо избранных.
   - Сопутствующее: Рим. 8:34 (CTS Romans с. 325) даёт Кальвинову половину посылки о единстве жертвы и ходатайства (S2-b, S2-c).

**INVALID_INFERENCES:**
- S1-b и S1-c без P-coext;
- S2-d как «явное учение Кальвина»;
- S3-c: «solis electis passum» как verbatim;
- S4-b и S4-c: формула как довод Кальвина «за» или «против»;
- S5-b: удаление «totius mundi»;
- S5-c: редактор = Кальвин;
- ~~английское «sealed… effectual» у Cole с. 151 как слова Кальвина~~ — `SUPERSEDED`: это слова Кальвина (CO 8:336, «obsignatur, ut rata sit»; §9.2). Ошибочным был мой вывод волны 1, а не корпус.

**EXACT_LOCATORS:** см. §2 (L1–L7) и §9.1. В волне 2 по скану CO сверены CO 9:484, CO 9:485 и CO 8:336. CO 9:524 как locus «solis electis passus» не подтверждён (§9.3). CO 49:100 по скану CO не сверен (CR 77 в IA не найден); латынь Рим. 5:18 сверена только по сноске CTS. *[Раунд 69, §20: CO 52:268 и CO 55:310 сверены по скану; CO 45:711 подтверждено вторым экземпляром; CO 9:523–524 прочитаны — фразы «pro solis electis passus est» нет; CO 49 на IA нет.]*

**PR/HEAD/TESTS:**
- ветка `arena/0fbd0e42-research`, база `5fab12a`; PR — Draft, номер в описании PR;
- проверки в этой ветке (после `git fetch --unshallow`, иначе commitTimeChecks честно падает):
  - `python -B scripts/validate_research_root_authority.py` — PASS;
  - `python -B scripts/validate_atonement_corpus_integrity.py` — PASS.

**HOLD:**
- `QUOTE_HOLD` — «solis electis» (01_, 22_);
- `LOCATOR_UNVERIFIED` — CO-номера выше;
- `HOLD` — Nicole, Rainbow, Helm, Archbald (не прочитаны);
- `EXEGETICAL_HOLD` по F16-02 сохраняется;
- `REVIEW_DEFERRED` — реального пересечения с открытыми объектами Agent 1/3/6 нет; поправки к матрице Agent 6 вынесены в §7, а не внесены.

**OWN_TASK_DONE:**
- S1–S5 закрыты как аудит;
- Фаза 2 — `STOP_DISCOVERY` (два безрезультатных целевых прохода по «solis electis»; исследовательская литература без первичного чтения не повышена).

---

## 9. Волна 2 (2026-11-17, продолжение): сверка по *Corpus Reformatorum* (CO) и две поправки

Источник: *Ioannis Calvini Opera quae supersunt omnia* (Baum, Cunitz, Reuss; Brunsvigae, 1863–1900; репринт Johnson). Сканы Claremont в IA; нумерация томов IA — по CR, то есть CO *n* = CR *n*+28. Номера колонок получены так: лист IA → `*_page_numbers.json` (соседние листы с распознанными колонтитулами, по две колонки на страницу) → положение абзаца на листе (левая или правая колонка). Это вычисленные локаторы, не прочитанные глазом колонтитулы; погрешность ±1 колонка оговорена ниже.

### 9.1. Сверенные локаторы CO

| ID | Текст | IA id, лист | Колонка CO | Опора вычисления | Класс |
|---|---|---|---|---|---|
| CO-1 | Против Хесхузия, «scire velim… edant impii…» | `operaquaesupersu0037calv` (CR 37 = CO 9), лист 320, правая колонка | **CO 9:484** | лист 319 = кол. 481(–482), лист 321 = кол. (485–)486 → лист 320 = 483–484 | A1 |
| CO-2 | Там же, «sanctificationem, quae solis electis… propria est» + аксиома | тот же том, лист 321, левая колонка | **CO 9:485** | то же | A1 |
| CO-3 | *De aeterna Dei praed.*, против Георгия | `operaquaesupersu0036calv` (CR 36 = CO 8), лист 210, правая колонка | **CO 8:336** | лист 209 = кол. 333(–334), лист 211 = кол. (337–)338 → лист 210 = 335–336 | A1 |
| CO-4 | 1 Ин. 2:2, «Ego quamquam verum… nego tamen praesenti loco quadrare» | `operaquaesupersu0083calv` (CR 83 = CO 55), лист 167, правая колонка | традиционно **CO 55:310**; текст сверен, колонка **не откалибрована** (номера страниц в json этого тома интерполированы) *[раунд 69, §20: откалибрована — «310» над правой колонкой, OCR-обёртка 166; `LOCATOR_APPROX` снят]* | — | A1 (текст) / `LOCATOR_APPROX` (колонка) |

**Выводы по локаторам:**
- Традиционные CO 9:484 и CO 8:336 **подтверждены**.
- Текст CO-1 совпадает с изданием 1667 г. (с. 759) дословно, включая «expiandis eorum peccatis».
- Wording в матрице Agent 6 §4.5 и в `02_` #17 по-прежнему расходится с CO (предложение §7 остаётся в силе).

### 9.2. Поправка к моей волне 1: «obsignatur, ut rata sit» — это Кальвин

CO 8:336 (полный абзац, нормализовано):
> «…Ne valeat in praesens communis illa solutio: Christum sufficienter pro omnibus passum esse, efficaciter tantum pro electis. … Controversia etiam caret, Christum expiandis totius mundi peccatis venisse. Sed confestim occurrit illa solutio: Ut quisquis credit in eum non pereat… (Ioann. 3, 15). Nec vero qualis sit Christi virtus, vel quid per se valeat, nunc quaeritur: sed quibus se fruendum exhibeat. Quod si in fide consistit possessio, et fides ex spiritu adoptionis manat, restat, ut in numerum filiorum is duntaxat ascitus sit, qui futurus est Christi particeps. **Nec vero aliud Christi officium commendat evangelista Ioannes, quam ut morte sua in unum congreget Dei filios (Ioann. 11, 52).** Unde colligimus quamvis per ipsum offeratur [pag. 156] omnibus reconciliatio, peculiare tamen esse electis beneficium, ut in vitae societatem colligantur. Quanquam dum omnibus offerri dico, non ita accipio, quasi ad omnes legatio illa perveniat, qua mundum sibi reconciliat Deus (2 Cor. 5, 18): **sed ad quos pervenit, ne eorum quidem cordibus indifferenter obsignatur, ut rata sit.**»

- В волне 1 я пометил английское «sealed… effectual» у Cole (с. 151) как добавку переводчика. Это **ошибка**: в латыни CO есть «obsignatur, ut rata sit». Моя выписка из 1667 г. обрывалась на «…legatio illa perveniat». Строки §2.1 и §8 помечены `SUPERSEDED`, не удалены.
- Правило переводчика остаётся в силе, но к этому месту не применимо.

### 9.3. Откуда «solis electis»: единственное вхождение в CO 9 — об освящении

Поиск по OCR CO 9 (весь том, включая *Dilucida explicatio* против Хесхузия):

| Запрос | Результат |
|---|---|
| «solis electis» | **1** совпадение, CO 9:485: «…ut aliquando sanctificationem, [pag. 40] quae solis electis et filiis Dei propria est, discernere a generali potentia discat, quae ad reprobos quoque pertinet» |
| «electis passum» | 0 |
| «electis passus» | 0 |
| «semper dixi» | 0 |

Сразу за этим (CO 9:485) стоит латинский оригинал аксиомы: «…ne minimum quidem apicem labefactat mei axiomatis: Non posse Christum, quatenus est panis vivificus, et victima in cruce immolata, spiritu suo vacuum in corpus hominis intrare».

**Вывод:**
- В CO 9 нет ни «Christum solis electis passum esse» (`01_`:890), ни «pro solis electis passus est» (`22_` #11/#998, «CO 9:524»).
- Единственное «solis electis» в этом споре говорит об **освящении**, а не о страдании Христа, и стоит на кол. 485, а не 524.
- С учётом трёх независимых сканов (1667, CTS, CO) классификация `INVALID` для verbatim-атрибуции **усиливается** до `MISATTRIBUTION_PROBABLE`: вероятное смешение с CO 9:485 или позднейший пересказ. Строки `01_`/`22_` — по §7 в `SUPERSEDED/HOLD`, не удалять.
- OCR-поиск не заменяет чтения тома глазами, поэтому это `PROBABLE`, а не `PROVEN`.

**Контекст CO 9:484, усиливающий оговорку S3-b.** Непосредственно перед вопросом стоит: «Sed in primis hoc probandum est, quomodo adsit Christus incredulis, quatenus est spiritualis animarum cibus, **vita denique et salus mundi**». То есть Кальвин сам ставит рамку «quatenus» (поскольку Христос есть пища, жизнь и *спасение мира*). Вопрос о распятии «pro impiis» задан внутри этой рамки. Это поддерживает чтение «в отношении духовного вкушения», но не опровергает строгое чтение.

### 9.4. Уточнение S1: «нет иного *officium*» явно у Кальвина

CO 8:336: «Nec vero aliud Christi officium commendat evangelista Ioannes, quam ut morte sua in unum congreget Dei filios (Ioann. 11, 52)».

| ID | Строгое утверждение | Вердикт после волны 2 |
|---|---|---|
| S1-b′ | Спасительная функция (*officium*) смерти Христа, о которой говорит Иоанн, есть собирание чад Божиих, и иной Иоанн не называет | `EXPLICIT` (CO 8:336) — **NEW_DELTA** в пользу строгой стороны |
| S1-b″ | Значит, у смерти нет **никакого** отношения к неизбранным (ни «quid per se valeat», ни «expiandis totius mundi peccatis») | По-прежнему `WEAK_INFERENCE`: в **том же абзаце** Кальвин различает «quid per se valeat» и «quibus se fruendum exhibeat», признаёт «controversia caret… totius mundi peccatis» и «offeratur omnibus reconciliatio». Фраза об *officium* ограничена рамкой «commendat evangelista Ioannes» (Ин. 11:52) |

**Чистый итог для S1.** Кальвин явно отождествляет намеренный спасительный результат смерти с собиранием избранных; недостающая посылка уже не «цель = собирание» (это есть), а только P-coext в узком смысле: что «quid per se valeat» не создаёт никакого реального отношения к миру. Этой посылки в CO 8:336 нет, а её отрицание по меньшей мере совместимо с текстом.

### 9.5. S4: «nego praesenti loco quadrare» — стоковая экзегетическая формула

В том же томе CO 55 (Евр. 5:6, лист 42) Кальвин употребляет ту же формулу о другом предмете: «Si excipiant, כהנים interdum vocari principes: fateor id quidem, sed nego praesenti loco quadrare». Модель «признаю общее утверждение — отрицаю, что оно подходит этому месту» — его обычный экзегетический приём. Это **подкрепляет** S4-b/S4-c: в 1 Ин. 2:2 формула Ломбарда не отвергнута и не использована как аргумент, а признана верной и признана неприменимой к стиху.

### 9.6. Фаза 2 — добавка

Nicole (*WTJ* 47 [1985]) в переводных и вторичных выдержках (golgothaministry.org; Nicole, *Standing Forth*, гл. 13) называет фразу против Хесхузия «a categorical denial of universal atonement». Сама статья **не прочитана**; через выдержку не верифицировано (`HOLD`). По существу: в свете §9.3 (рамка «quatenus… salus mundi», CO 9:484) квалификация «categorical» требует P-ctx (§4.3) — это шаг, который статья должна защищать, а не предполагать.

### 9.7. Передача MAX (дельта волны 2)

- **NEW_DELTA (две позиции):**
  1. Сверка CO: 9:484, 9:485, 8:336 подтверждены по скану CO. Поправка к моей волне 1: «obsignatur, ut rata sit» — слова Кальвина.
  2. «solis electis» в CO 9 встречается только об освящении (CO 9:485) → `MISATTRIBUTION_PROBABLE` для `01_`:890 и `22_` #11/#998. S1-b′: «nec aliud Christi officium… quam ut morte sua in unum congreget Dei filios» (CO 8:336) — `EXPLICIT`.
- **INVALID_INFERENCES (добавка):** моя собственная пометка волны 1 «Cole sealed… = переводчик» — снята.
- **HOLD:**
  - CO 49:100 (Рим. 5:18) по скану CO не сверен (CR 77 в IA не найден);
  - колонка CO 55:310 не откалибрована;
  - Nicole/Rainbow/Helm/Archbald не прочитаны.
- **STOP_DISCOVERY:** по «solis electis» — закрыто окончательно (три издания).
- **REVIEW_DEFERRED:** без изменений; общие файлы и C-17 не трогались.

---

## 10. Волна 3 (2026-11-17): адресный ответ на ревью MAX в PR #554

Ревью MAX (комментарий в Conversation PR #554, 2026-11-17 11:56 UTC) — пять пунктов. Широкого поиска в этой волне нет: прочитаны только страницы, уже названные в §2 и §9, и их непосредственный контекст. Для полного текста одной страницы использовался текстовый слой IA BookReader (`BookReaderGetTextWrapper.php`, страница *n* = лист *n*+1).

### 10.1. Пункт 1: что именно доказывает каждый новый `EXPLICIT`

| ID | Цитата и локатор | Что доказано (`EXPLICIT`) | Что **не** доказано | Ближайший контекст, проверенный в этой волне |
|---|---|---|---|---|
| **E1** | Хесхузий: «scire velim quomodo Christi carnem edant impii, pro quibus non est crucifixa…» — CO 9:484 | В евхаристическом споре Кальвин утверждает: нечестивые не могут «есть» плоть, которая не распята за них, и «пить» кровь, не пролитую для искупления их грехов. Вопрос стоит в рамке «quatenus est spiritualis animarum cibus, vita denique et salus mundi» и в условной ad hominem конструкции «quando tam mordicus verbis adhaeret» | Общее учение об объёме *impetratio*. Это не трактат об объёме, а довод о вкушении; нужна P-ctx (§4.3) | **CO 9:483, левая колонка той же страницы**: «Christum enim tam reprobis quam fidelibus corpus suum in coena porrigere sic asserimus…»; и о нечестивых, отвергающих дар: «merito profani et bruti contemptus damnantur: quia **victimam, qua expiata sunt mundi peccata**, et homines Deo reconciliati, pro nihilo ducunt». То есть в одном трактате и на одной странице стоят «не распята за нечестивых» (484) и «нечестивые презирают жертву, которой искуплены грехи мира» (483). **S3-b понижено: `WEAK_INFERENCE` / `TENSION`** (было «STRONG_INFERENCE в лучшем случае»). Строка Agent 6 «9. … Resp. Heshusius — EXPLICIT» (PR #555) — см. §10.4 |
| **E2** | «Nec vero aliud Christi officium commendat evangelista Ioannes, quam ut morte sua in unum congreget Dei filios (Ioann. 11, 52)» — CO 8:336 | Подлежащее — *evangelista Ioannes*, глагол *commendat*. Кальвин говорит: Иоанн (в Ин. 11:52) указывает служение Христа как собирание чад Божиих Его смертью. Фраза служит посылкой для вывода «Unde colligimus… peculiare tamen esse electis beneficium» | Что у смерти Христа вообще нет иной цели или отношения. Фраза — о том, что *Иоанн* «рекомендует» в этом месте, и стоит **между** «Controversia etiam caret… totius mundi peccatis» и «offeratur omnibus reconciliatio». Моя формулировка S1-b′ в §9.4 («`EXPLICIT` — NEW_DELTA в пользу строгой стороны») **сужается**: `EXPLICIT` только для иоанновского *officium* в аргументе об особом благе | Предшествует: «Quod si in fide consistit possessio, et fides ex spiritu adoptionis manat, restat, ut in numerum filiorum is duntaxat ascitus sit, qui futurus est Christi particeps». Следует: вывод об особом благе избранных и оговорка «obsignatur, ut rata sit» |
| **E3** | «Ne valeat in praesens communis illa solutio…» — CO 8:336 | В этом месте Кальвин не строит ответ на формуле Ломбарда | Ни принятия формулы как довода об объёме, ни её доктринального отвержения | См. §10.2 (границы фраз) |
| **E4** | «Controversia etiam caret, Christum expiandis totius mundi peccatis venisse» — CO 8:336 | Кальвин признаёт это утверждение бесспорным в споре с Георгием | Что «totius mundi» здесь распределительно = каждый человек. Предыдущая фраза глоссирует Иоанна как «fideles… per quascunque mundi plagas dispersi», и сразу следует «Sed confestim occurrit illa solutio: Ut quisquis credit…» | Смысл «totius mundi» — `UNDETERMINED` (как в N-1) |
| **E5** | «sed ad quos pervenit, ne eorum quidem cordibus indifferenter obsignatur, ut rata sit» — CO 8:336 | Действенное запечатление — не у всех, до кого дошло послание | — | Авторская оговорка; в волне 1 была обрезана (§9.2) |
| **E6** | Рим. 8:34, CTS Romans с. 325; Ин. 17:9, CTS John II с. 172–173 | Ходатайство = непрерывно предъявляемая сила смерти и воскресения; Христос молится только за избранных | Объём жертвы как таковой (S2-c/S2-d без изменений) | — |

### 10.2. Пункты 2–3: границы фраз *De aeterna* и оси классификации

**(a) Выравнивание CO 8:336 / 1667 (скан-индекс 628) / Cole с. 150–151 по смысловым единицам.**

| № | CO 8:336 (OCR-слой скана CO) | 1667, скан-индекс 628 (OCR) | Cole 1856, с. 150–151 | Замечание |
|---|---|---|---|---|
| 0 | «Atqui ego sic universalem Dei gratiam esse fateor, ut in hoc tamen situm esse discrimen addam: quod non omnes secundum Dei propositum vocantur.²)» (сн. 2: франц. добавка «dont parle sainct Paul, qui emporte un mouvement certain du sainct esprit») | не извлекалось | не извлекалось | **Авторская рамка перед абзацем**: всеобщая благодать признаётся с различением |
| 1 | «Argute se ratiocinari putat, quum dicit: Christus propitiatio est pro peccatis totius mundi. Ergo extra mundum reprobos constituant oportet qui a Christi participatione arcere eos volunt.» | Начало в выписке волны 1 было реконструировано в скобках; дальше «…mundum reprobos constitu[…] oportet…» | «Georgius imagines himself to argue very cleverly… must, of necessity, place them somewhere out of the world.» | Довод Георгия. Чтение «constituere» в §2.1 — моя нормализация; следовать CO: «constituant» |
| 2 | «Ne valeat **in praesens** communis illa solutio: Christum sufficienter pro omnibus passum esse, efficaciter tantum pro electis.» | совпадает (OCR «fufficienter») | «Now we will not permit the common solution of this question to avail, **on the present occasion**; which would have it, that Christ suffered sufficiently for all men; but effectually for his elect alone.» | Граница «in praesens» сохранена во всех трёх |
| 3 | «Magna illa absurditas, ob quam plausum sibi inter suos gregales monachus quaesivit, apud me nihil habet momenti.³)» (сн. 3: «Hoc comma om. in versione») | совпадает | «This great absurdity, by which our monk has procured for himself so much applause… has no weight whatever with me.» | **На кого указывает «magna illa absurditas».** В CO 8:335 Кальвин передаёт довод Георгия «Verum sequetur, solos electos destitui gloria Dei». Сноска 3 там цитирует французскую версию: «il obiecte qu'il s'ensuyvroit une grande absurdité». Значит, «magna absurditas» — это вывод, которым Георгий грозит, а не формула Ломбарда. Английский Cole ставит фразу сразу после формулы, и читатель может отнести её к формуле: это риск перевода. Во французской версии фраза опущена |
| 4 | «Per quascunque mundi plagas dispersi sint **fideles**, expiationem Christi morte partam ad eos Ioannes extendit.» | совпадает | «John does indeed extend the benefits of the atonement… to **all the elect of God**, throughout what climes…» | **Сдвиг перевода**: *fideles* → «the elect of God». Цитировать по латыни |
| 5 | «Id certe non obstat, quominus reprobi in mundo electis permixti sint.» | совпадает | «…it by no means alters the fact, that the reprobate are mingled with the elect in the world.» | — |
| 6 | «**Controversia etiam caret**, Christum expiandis totius mundi peccatis venisse.» | совпадает | «It is also a fact, without controversy, that Christ came to atone for the sins "of the whole world."» | Cole берёт «of the whole world» в кавычки (как цитату Писания); в латыни кавычек нет. Граница фразы сохранена |
| 7 | «Sed confestim occurrit illa **solutio**: Ut quisquis credit in eum non pereat… (Ioann. 3, 15).» | совпадает | «But the solution of all difficulty is immediately at hand…» | Кальвин отвечает Георгию «решением» из Ин. 3:15, а не схоластическим |
| 8 | «Nec vero qualis sit Christi virtus, vel quid per se valeat, nunc quaeritur: sed quibus se fruendum exhibeat.» | совпадает | «…not what the power or virtue of Christ is, nor what efficacy it has in itself; but, who those are, to whom He gives himself to be enjoyed.» | — |
| 9 | «…Nec vero aliud Christi officium commendat evangelista Ioannes… Unde colligimus quamvis per ipsum offeratur omnibus reconciliatio, peculiare tamen esse electis beneficium…» | совпадает | Cole с. 151 | E2 |
| 10 | «Quanquam dum omnibus offerri dico, non ita accipio, quasi ad omnes legatio illa perveniat…: sed ad quos pervenit, ne eorum quidem cordibus indifferenter obsignatur, ut rata sit.⁴)» (сн. 4: продолжение «на целую страницу» отсутствует во французской версии) | в выписке волны 1 обрезано после «perveniat» | «…not sealed indiscriminately on the hearts of all… so as to be effectual in them» | Авторская оговорка **не обрезана** в расширенном фрагменте (исправлено в §9.2) |

**Вывод по пункту 2.** Обе границы — «in praesens» (ед. 2) и «Controversia etiam caret» (ед. 6) — одинаковы в CO, в 1667 г. и у Cole. Авторские ограничения стоят до абзаца (ед. 0) и в его конце (ед. 10). Расширенный фрагмент их не обрезает. Два риска перевода у Cole — ед. 3 (отнесение «absurditas») и ед. 4 (*fideles* → «elect») — зафиксированы. Цитировать по латыни CO.

**(b) Оси по `data/repository-evidence-policy-v2.json` и `AGENT_RULES.md` §1.** В этом под-корпусе латинский текст автора — `A1` (участник-автор); английский перевод CTS — `B1` (`ИСКУПЛЕНИЕ/00_CURRENT_AUTHORITY_2026-10-07.md`, раунд 61: «Класс остаётся B1: везде английский перевод CTS»).

| Источник | evidenceClass | accessState (что реально прочитано) | locatorState | Quote-safe? |
|---|---|---|---|---|
| CO 9 (CR 37), *Dilucida explicatio* | A1 | OCR-слой скана: полный текст страницы кол. 483–484 и абзац кол. 485. **Изображение страницы глазами не проверено** | **кол. 484** — колонтитул «DE VERA PARTICIPATIONE 484» в OCR-слое той же страницы; **483** — левая колонка той же страницы; **485** — вычислено по листу (±1) | Нет: `LOCATOR_HOLD(visual)`. Совпадение 1667 = CO = CTS — сильный индикатор, но не замена визуальной сверки |
| CO 8 (CR 36), *De aeterna* | A1 | OCR-слой: полный текст кол. 335–336 со сносками | **кол. 336** — колонтитул «DE AETERNA DEI 336» в OCR-слое; кол. 335 — левая колонка | Нет: `LOCATOR_HOLD(visual)` |
| CO 55 (CR 83), 1 Ин. 2:2 и Евр. 5:6 | A1 | OCR-абзацы | 55:310 — традиционный; колонка **не откалибрована** | Нет: `LOCATOR_HOLD` **Волна 4 (§11.1):** кол. 310 подтверждена колонтитулом «310» в OCR-слое; 1 Ин. 2:1 — кол. 309. `LOCATOR_HOLD(visual)` |
| 1667 *Opera* т. VIII | A1 (раннее собрание; издание идентифицировано) | OCR-абзацы | «с. 628 / 759» — **индексы скана**, не печатные страницы; в томе несколько пагинаций (с листа 742 счёт начинается заново) | Нет: `LOCATOR_HOLD` |
| CTS *Tracts* II | B1 | абзац | p. 527 — по автоматическому `page_numbers.json` IA; колонтитула в OCR-слое нет | Не единственная опора |
| CTS *Romans* 1849 | B1 (латинская сноска — A1-текст, но в B1-носителе; издание латыни не названо) | абзацы p. 211, 212, 325 | p. 212 — колонтитул «212 COMMENTARIES… V. 19» в OCR; 211 — предыдущий лист; 325 — по указателю книги | Не единственная опора; CO 49:100 `LOCATOR_HOLD` |
| CTS *John* II 1847 | B1 | абзацы p. 170–173 | по `page_numbers.json` IA; колонтитула в OCR нет | Не единственная опора |
| Cole 1856 | B1 | абзацы pp. 150–151 + отдельные совпадения | колонтитулы найдены поиском по номерам | Не единственная опора; риски перевода: ед. 3, 4, 6 |
| Owen, *Works* X | **A1 для позиции Оуэна** (исправлено: в §2 стояло «A2») | только синопсис и заголовок кн. I, гл. VII | печатная страница не установлена | Только как свидетельство *формулировки Оуэна* |
| Утрехт 1620, Acta pp. 122–123 | A2 (по матрице Agent 6) | **мною не читано** | по Agent 6 | Ссылка транзитивная |

**Понижения статуса.** «PRIMARY_VERIFIED» (S3, §0/§8) и «сверен» (§9.1) означали: текст найден в OCR-слое идентифицированного издания, а колонка подтверждена колонтитулом в том же OCR-слое. По оси `locatorState` это **не** визуальная сверка, поэтому статус по этой оси — `LOCATOR_HOLD(visual)`. Класс `A1` остаётся (это класс источника, а не степень проверки).

### 10.3. Пункт 4: короткая адресная таблица исправлений к существующим реестрам (не применены)

| # | Файл : строка (на `origin/main` 5fab12a) | Сейчас | Исправление | Основание | Флаг |
|---|---|---|---|---|---|
| R1 | `docs/research/atonement/22_master_source_registry_50_plus_primary_citations.md` : 48–50 (п. 11) | «CO 9:524 … *Christus pro solis electis passus est*» | `SUPERSEDED` → «*Dilucida explicatio* (1561), CO 9:484: "…pro quibus non est crucifixa… qui expiandis eorum peccatis non est effusus" (евхаристический контекст)» | §9.3: в OCR CO 9 «electis passus/passum» — 0; «solis electis» только о *освящении*, CO 9:485 | `MISATTRIBUTION_PROBABLE`, `LOCATOR_HOLD(visual)` |
| R2 | там же : 998 (табл. #11) | «*Contra Heshus.* \| Verified \| «pro solis electis passus est»» | «Verified» → `QUOTE_HOLD`; цитату заменить по R1 | то же | то же |
| R3 | `docs/research/atonement/01_prokopenko_article_review.md` : 890 | «Nihil aliud dico quam quod semper dixi: Christum solis electis passum esse» | `SUPERSEDED/QUOTE_HOLD` → цитата по R1 с оговоркой E1 (CO 9:483 vs 484) | §9.3: «semper dixi» — 0 в CO 9 и в 1667 | `MISATTRIBUTION_PROBABLE` |
| R4 | `docs/research/atonement/02_history_of_atonement_controversies.md` : 30 (#17) | «…qui non est effusus in peccatorum eorum expiationem», CO 9:484 | вторую половину заменить на «qui expiandis eorum peccatis non est effusus»; локатор CO 9:484 — верен | CO 9:484 = 1667 | wording |
| R5 | `ИСКУПЛЕНИЕ/evidence/AGENT6_HISTORICAL_EXTENT_MATRIX_2026_11_15.md` : 137 (§4.5) и 951 (HOLD #7) | «quae non pro ipsis crucifixa est… qui non pro ipsorum peccatis effusus est»; `HESHUSIUS_VERBATIM_HOLD` | wording по R4; HOLD сузить до `LOCATOR_HOLD(visual)`; часть о «solis electis» сохранить и дополнить ссылкой на §9.3 | CO 9:484 | файл Agent 6 — правит владелец/MAX |
| R6 | `docs/research/atonement/32_archbald_dissertation_calvin_boundaries_vs_prokopenko.md` : 80 | цитата Хесхузия | **без изменений** — совпадает с CO 9:484 дословно. Добавить контекст CO 9:483 («victimam, qua expiata sunt mundi peccata») к выводу «твёрдая аксиома» | E1 | context |
| R7 | `ИСКУПЛЕНИЕ/13_` §2.2; `fathers/16_` §2.2 | формула «достаточно/действенно» у Кальвина | добавить параллель CO 8:336 «Ne valeat in praesens…» и ед. 3 (§10.2: «magna absurditas» = довод Георгия, по CO 8:335 сн. 3) | §10.2 | framing |
| R8 | `ИСКУПЛЕНИЕ/00_CURRENT_AUTHORITY_2026-10-07.md` : 132 (открытый пункт «латинский Кальвин (*De aeterna*) — нужен CR/OS, а не OCR-перебор») | открыто | для MAX: текст CO 8:335–336 найден и выровнен (§10.2), но через OCR-слой скана CR; пункт остаётся `LOCATOR_HOLD(visual)` и закрывается только визуальной сверкой страницы | §10.2(b) | не закрывать |
| R9 | `synthesis/02_CONFLICT_LEDGER.md` C-17 | `TENSION` | **не редактировалось**. Для MAX: E1 (CO 9:483/484) и E4 (CO 8:336) — две внутритомные пары «за мир / не за нечестивых», статус `TENSION` подтверждается | §10.1 | — |

### 10.4. Пункт 5: пересечение с AGENT 3/6

- **AGENT 6, PR #555** (`arena/c5802a5f-research`, HEAD `f9a4ba2c341934e25dcca4c62e13fd6dfe578305`, файл `ИСКУПЛЕНИЕ/evidence/AGENT6_CALVIN_DORT_DOGMATIC_CROSSWALK_2026-11-17.md`) — **реальное пересечение**:
  - строка 9: «Resp. Heshusius … **EXPLICIT**»;
  - строка 1: Рим. 5:18 и 1 Ин. 2:2 как опора «бесконечной достаточности»;
  - строка 8: Inst II.16.16.
  Оставлен **один** предметный review (id 5938088668). Во время написания HEAD #555 сменился на `ec8cb0d49a60562fb8f0d69b7fe7261e018599d0`, и GitHub привязал ревью к нему. Сверка с новым HEAD дана отдельным комментарием в #555:
  - строка 1 переформулирована как «признание истинности формулы» — `EXPLICIT` допустимо, п. 2 ревью снят;
  - строка 9 по-прежнему `EXPLICIT`, а новый локатор «CO 47:64» **неверен** (верно: CO 9:484; противовес CO 9:483);
  - строка 8 — без изменений.
  Файлы Agent 6 не редактировались.
  - **Закрыто владельцем (AGENT 6, коммит `bd3338ba91ba6509e1f26c7c888c071c47b4982d`, проверено по диффу #555):**
    - локатор «CO 47:64» заменён на CO 9:484, вхождений «CO 47:64» в диффе больше нет;
    - противовес CO 9:483 внесён;
    - строка 9 понижена с `EXPLICIT` до `INFERRED (TENSION)`, `LOCATOR_HOLD(visual)` сохранён.
    Предметные замечания этого ревью **закрыты**; повторного ревью не будет. Приёмку #555 ведёт MAX.
- **AGENT 3:** открытого PR с объектом пересечения нет → `REVIEW_DEFERRED`.
- **AGENT 4 (#557), AGENT 5 (#558):** по диффу совпадений с Хесхузием, *De aeterna* и «solis electis» нет → без review.

### 10.5. Финальная передача MAX

- **PR/HEAD/CI:** PR #554 (Draft), ветка `arena/0fbd0e42-research`. HEAD и CI — в последнем комментарии PR.
- **ALREADY_PROVEN:** без изменений (§8).
- **NEW_DELTA волны 3** (две позиции):
  1. CO 9:483 — контекстный противовес E1 на той же странице; S3-b → `WEAK_INFERENCE` / `TENSION`.
  2. Выравнивание *De aeterna* по 10 единицам: «magna absurditas» = довод Георгия (CO 8:335 сн. 3); риск Cole *fideles* → «elect».
- **INVALID_INFERENCES (добавка):**
  - «Хесхузий = EXPLICIT отвержение всеобщего удовлетворения» (PR #555, строка 9);
  - «magna absurditas = формула Ломбарда» (по английскому Cole);
  - моя S1-b′ в широкой формулировке (сужено, E2).
- **HOLD:**
  - `LOCATOR_HOLD(visual)` — для всех CO-локаторов;
  - `LOCATOR_HOLD` — печатные страницы 1667 г., CO 49:100, CO 55:310;
  - Nicole, Rainbow, Helm, Archbald не прочитаны;
  - `PUBLICATION_HOLD` / `RIGHTS_HOLD` не снимались.
- **OWN_TASK_DONE:** S1–S5 и Фаза 2 закрыты в границах задания. Дальнейшая активность без нового адресного запроса MAX не планируется.


---

## 11. Волна 4 (2026-11-17): закрытие одного HOLD из списка §10.5 и одна текстовая дельта к S2

Без нового запроса MAX широкого поиска нет. Проверены только два HOLD-локатора, уже названные в §10.5 (CO 55:310 и CO 49:100), каждый не более чем двумя целевыми проходами.

### 11.1. CO 55:310 (1 Ин. 2:2) — колонка подтверждена; на той же странице текст к S2

Страница скана `operaquaesupersu0083calv` (CR 83 = CO 55), текстовый слой BookReader, страница 166 (= лист 167). Правая колонка начинается с колонтитула **«310»**, перед ним стоит «CAPUT II.» в конце левой колонки. Значит, левая колонка — **кол. 309**.

- **Кол. 310, 1 Ин. 2:2:** «Qui hanc absurditatem volebant effugere, dixerunt, sufficienter pro toto mundo passum esse Christum: sed pro electis tantum efficaciter. Vulgo haec solutio in scholis obtinuit. Ego quamquam verum esse illud dictum fateor: nego tamen praesenti loco quadrare. Neque enim aliud fuit consilium Iohannis, quam toti ecclesiae commune facere hoc bonum. Ergo sub omnibus, reprobos non comprehendit…». Это совпадает с `fathers/16_` §2.2 и `13_` §2.2. Традиционный локатор CO 55:310 **подтверждён** по колонтитулу в OCR-слое, глазами не проверен.
- **Кол. 309, 1 Ин. 2:1 (новое для S2):**
  > «Porro dum ostendere vult quomodo redeamus cum Deo in gratiam, dicit Christum esse nobis advocatum. Nam in hoc apparet coram facie Dei, ut sacrificii sui vim et efficaciam erga nos exserat. Quo melius hoc possit intelligi, crassius loquar. **Intercessio Christi continua est mortis eius applicatio in salutem nostram.** Quod ergo Deus peccata nobis non imputat, hoc fit quia Christum deprecatorem respicit.»

| ID | Утверждение | Вердикт |
|---|---|---|
| S2-b′ | Для Кальвина ходатайство Христа есть **постоянное применение (*applicatio*)** Его смерти ко спасению «нас» | `EXPLICIT` (CO 55:309). Подкрепляет S2-b (Рим. 8:34, CTS p. 325) латинским A1-текстом |
| S2-c′ | Значит, ограничение ходатайства избранными (Ин. 17:9) — это ограничение **применения** смерти | `STRONG_INFERENCE` (S2-a + S2-b′, оба места — Кальвин) |
| S2-d′ | Значит, Кальвин ограничивает избранными и **импетрацию** (объём жертвы) | По-прежнему `WEAK_INFERENCE` / `UNDETERMINED`. Собственное определение Кальвина помещает ходатайство на сторону *applicatio*. Поэтому из ограничения ходатайства выводится ограничение применения, а не объёма жертвы, пока не добавлена P-coext (Оуэн, *Death of Death* I.vii) |

**Значение.** Это самый точный текст Кальвина по узлу S2 из найденных. Он не решает спор: строгая сторона прочтёт его так, что применяется именно то, что приобретено для тех же лиц. Но он фиксирует, на какой стороне различения Кальвин сам ставит ходатайство. Тезис `32_` / Archbald «жертва и ходатайство коэкстенсивны» по-прежнему опирается на P-same-object (§4.2), которой в этом тексте нет.

### 11.2. CO 49:100 (Рим. 5:18) — `STOP_DISCOVERY`

| Проход | Запрос | Результат |
|---|---|---|
| 1 | advancedsearch IA: «calvini opera» AND (volume 49 / 77 / «vol XLIX» / «romanos») | 0 |
| 2 | advancedsearch IA по фразе «Communem omnium gratiam facit» | 0 |

Два целевых прохода безрезультатны → `STOP_DISCOVERY`. CO 49:100 остаётся `LOCATOR_HOLD`. Латынь Рим. 5:18 по-прежнему опирается только на сноску CTS 1849, p. 211 (B1-носитель) и на `fathers/16_` §2.2.

### 11.3. Обновлённые HOLD

- `LOCATOR_HOLD(visual)` — CO 8:335–336, CO 9:483–485, CO 55:309–310: найдены по OCR-слою, колонки подтверждены колонтитулами (кроме 9:485 — вычислено по листу);
- `LOCATOR_HOLD` — CO 49:100; печатные страницы 1667 г.;
- Nicole, Rainbow, Helm, Archbald — `HOLD` (не прочитаны);
- `PUBLICATION_HOLD` / `RIGHTS_HOLD` — не снимались.

**OWN_TASK_DONE** сохраняется. Список HOLD из §10.5 сокращён на CO 55:310 (по OCR-колонтитулу).

---

## 12. Review receipt: научное ревью PR #555 (AGENT 6) по заданию MAX

**Задание:** MAX в #554, issuecomment-6948763867 (выдано на HEAD #555 `c530c89a`).
**Ревью:** [#555, review 5939105630](https://github.com/FedorMilovanov/Research/pull/555#pullrequestreview-5939105630), по HEAD **`f6d27e9ea6b8bcfeb94d95b56a78fe25df0698ac`** (HEAD сдвинулся до начала ревью).
**Границы:** чужой файл не редактировался, ledger и C-17 тоже. Нового PR нет. Retest — один, после ответа AGENT 6.

### 12.1. Итог по узлам MAX

| Узел | Статус на `f6d27e9e` | Суть |
|---|---|---|
| A. Ин. 3:16 `propitium` | PASS | `reconciliatum` снят в `f6d27e9e`; независимо подтверждено OCR CO 47 (§12.2). Остаток MINOR: пересказ «без различия звания и племени» |
| B. §4.3 блок 3 | PARTIAL / BLOCKER | Часть «Кальвин» → `TENSION` исправлена. Часть «Дорт ПРЯМО ОТВЕРГАЕТ (Rej. V, VI)» противоречит тексту Rej. V/VI, `01_` R24, `04_` §6 и собственному §7.3 файла (Девенант подписал Каноны) |
| C. Девять строк | строки 1, 2, 3, 5 PASS по вердиктам; 4, 8 MAJOR (латынь и атрибуция, вердикт верен); 6, 7 MAJOR (вердикт и шаг); 9 MAJOR (латынь) | Дорт II.8 — `acquisivit`, а не `impetravit`. Каноны II.8–9 о ходатайстве молчат. Строка 6 — Дорт `NOT_ADDRESSED` → `COMPATIBLE`. Строка 7 — текстуальная зависимость II.5 от Кальвина не установлена |
| D. Прокопенко / история / систематики | BLOCKER + MAJOR | «Вера не приобретена смертью» — пробел аргумента (`01_` R24, :281, :499), а не авторский тезис. Датировка гибрида «лишь с конца XVIII в.» противоречит самому файлу. Амиро в п. 3 противоречит `AGENT6_HISTORICAL_EXTENT_MATRIX` §6.3. SYS-11 / SYS-20 / SYS-24 → `secondary/unverified` |
| Системно | BLOCKER | 10 латинских «цитат» (L1–L10) не совпадают с засвидетельствованным текстом (обратный перевод или контаминация); в L10 стоит ложная пометка «сверено по OCR» |

### 12.2. Новые первичные чтения (OCR-слой CR; `LOCATOR_HOLD(visual)`)

| ID | Место | Свидетель | Чтение |
|---|---|---|---|
| CO-2a | *Inst.* III.24.17 (1559), **CO 2:727** | `operaquaesupersu0030calv`, wrapper page 375; колонтитул «INSTITUTIO REL. CHRIST. 1559 … 728» (правая колонка = 728) | «…et quod salutem omnibus **indiscriminatim denuntiat**. Equidem dico optime convenire. Sic enim promittendo nihil aliud vult, quam omnibus expositam esse suam misericordiam… Ergo quum utrisque Dei misericordia per evangelium **offeratur**, fides est, hoc est Dei illuminatio, quae inter pios et impios distinguit» |
| CO-2b | *Inst.* III.24.17, **CO 2:728** | там же, правая колонка | «Addunt, non esse discrimen Iudaei et gentilis, ideoque **indiscriminatim omnibus proponi Dei gratiam**: nempe modo admittant… Deum pro suo beneplacito vocare» — это **возражение оппонентов**, а не тезис Кальвина. Там же: «Deum ita solem suum producere super bonos et malos (Matth. 5, 45)» |
| CO-2c | *Inst.* III.1.1 | `operaquaesupersu0030calv`, inside.php page 209 (номер колонки не установлен) | «quamdiu **extra nos est Christus** et ab eo sumus separati, quidquid in salutem humani generis passus est ac fecit, nobis esse inutile nulliusque momenti… ne salus per hunc parta nobis effluat» |
| CO-47 | Ин. 3:16, традиционно **CO 47:64** | `operaquaesupersu0075calv`, wrapper page 52 (скан-лист 53); колонтитула в OCR нет, карта страниц confidence 29 | «Et universalem notam apposuit, tum ut **promiscue** omnes ad vitae participationem invitet, tum ut praecidat excusationem incredulis. … se tamen toti mundo **propitium** ostendit, quum sine exceptione omnes ad fidem Christi vocat… Patet enim omnibus Christus ac expositus est, solis tamen electis oculos Deus aperit, ut fide ipsum quaerant». Подтверждает `fathers/21_` §8.1 (F-51) третьим свидетелем; номер колонки остаётся `LOCATOR_HOLD` |

**Следствия для моих узлов (без изменения вердиктов §0–§11):**
- Английское «indiscriminately» в CTS передаёт у Кальвина разные слова: *indiscriminatim* (III.24.17), *promiscue* (Ин. 3:16) и *indifferenter* (Рим. 5:18).
- Дорт II.5 по Schaff — «promiscue et indiscriminatim», по *Acta* 1620 — «promiscue & indifferenter» (`34_` S61 / S110).
- Лексический аргумент о зависимости канона от Кальвина на этом материале не проходит.

**HOLD без изменений** (§11.3); CO 2 и CO 47 добавлены в `LOCATOR_HOLD(visual)`. C-17 `TENSION` сохраняется.

## 13. Review receipt: peer review PR #557 (AGENT 4) и перехват верификации после заморозки #555

**Основание.** MAX, #554, 13:50:39Z (адресное peer review #557); MAX, #555, 13:50:37Z (`PROBATION FAILED / FREEZE`). Пользователь: AGENT 6 закрыт, проверки продолжаются силами AGENT 2. Файлы AGENT 4 и AGENT 6, ledger, C-17 и reader-главы **не редактировались**.

### 13.1. #557 @ `c7707700` — вердикт `CONDITIONAL / HOLD`

Комментарий: `issuecomment-6950270026`.
- **BLOCKER D1.** rev6 §2 («у Strong III.778 ровно два компонента; хвост Ин. 3:16 — веб-расширение») опровергается печатным OCR p. 778. Стронг сшивает **три** локуса — Рим. 5:18 + Мф. 26:28 + Ин. 3:16 — и приписывает их Comm. 1 Jn 2:2.
- **MAJOR:**
  - D2 — блог-транскрипция ≠ A1; пагинация блога не совпадает со сканом;
  - D4 — «вербатим» → переводческая эквивалентность;
  - D5 — противоречие Fuller ↔ Рим. 5:18; роль Richards сузить до элемента Мф. 26:28 (Ин. 3:16 — вероятно);
  - D6 — усечение 1 Ин. 2:2 происходит уже у Уоттса p. 153.
- **D3** (Рим. 5:18 у Ричардса отсутствует) подтверждён и усилен: постраничный OCR вместо индексного отсутствия.
- **Цепочка по уровням:**
  - (b) доказано: Watts p. 153 → Richards pp. 308–310 и Richards → Strong (только для Мф. 26:28); *(вторая половина снята в §16.1: совпадение по Мф. 26:28 не диагностично)*
  - (c) гипотеза: Watts → Strong для Рим. 5:18 (H1); формула «without distinction» как стандартная передача *indifferenter* (Дорт 1619, англ., II.5) (H2); посредник до 1907 г. (H3).

### 13.2. Новые чтения (OCR текстового слоя; `PRINT_IMAGE_HOLD`)

| ID | Свидетель | Пагинация | Существенное |
|---|---|---|---|
| ST-778 | Strong III, `cu31924092368236`, лист 17 | p. 778 (S39) | полный текст цитаты с хвостом «…for although in the world nothing is found worthy of the favor of God, yet he holds out the propitiation to the whole world, since without exception he summons all to the faith of Christ, which is nothing else than the door unto hope» |
| RI-306–311 | Richards 1846, `lecturesonmental00richrich`, листы 318–323 (wrapper 315–320) | лист = стр. + 12 (S50) | раздел о Кальвине целиком: p. 308 — «distinctly asserted by Dr. Watts» и Мф. 26:28; p. 309 — Ин. 3:16, 1 Кор. 8:11–12, Евр. 10:26; p. 310 — 1 Ин. 2:2 (до «agrees to this place»), 2 Пет. 2:1; p. 311 — Иуд. 4. Рим. 5:18 нет; `"indifferently"` и `"suffered for the sins of the whole world"` → 0 |
| WA-152–153 | Watts, *Works* VI (1811), `worksofreverendl06watt`, листы 166–167 | лист = стр. + 14 (якоря 149/161, интерполяция) | p. 152: сноска «See the end of this Fifth Consideration». p. 153: катена с латынью — Мф. 26:28, **Рим. 5:18** («…atque omnibus indifferenter Dei benignitate offertur…» / «offered indifferently to all by the bounty of God»), 1 Кор. 8:11–12, 1 Ин. 2:2 (обрыв после «quadrare»), 2 Пет. 2:1. Сноска «Comments… labours of his riper years» |

Следствие для моих узлов: латынь Рим. 5:18, на которую опирается S5 (§0), теперь засвидетельствована печатью 1811 г., а не только вторичными носителями. **CO 49:100 остаётся `LOCATOR_HOLD(visual)`.** Вердикты §0–§12 не меняются.

### 13.3. Перехват после заморозки #555: эталон засвидетельствованного текста вместо L1–L10

Файл AGENT 6 заморожен и не редактируется. Для будущего ревьюера, который будет заменять или снимать L1–L10, здесь фиксируется только засвидетельствованный текст (источники — ревью `5939105630` и §12). **В reader-главы не копировать.**

| # | Не использовать (#555) | Засвидетельствовано | Опора |
|---|---|---|---|
| L1 | II.3 `infinitae virtutis` | `infiniti valoris` | `34_` S110 (*Acta* 1620) |
| L2 | II.2 `aut nostro loco` | `seu vice nostra` | S110 |
| L3 | II.8 `impetravit` | `acquisivit` | S110 |
| L4 | Rej. VI `aequaliter` | `ex aequo` | S110 |
| L5 | II.5 `indiscriminatim` (Schaff) | `promiscue & indifferenter` (*Acta*) | S61 / S110 |
| L6 | 1 Ин. 2:2, пересказ с `fateor` | «verum esse illud dictum fateor: nego tamen praesenti loco quadrare» | CO 55:310 (OCR) + Watts 1811 p. 153 |
| L7 | CO 8:336 с `in scholis jactata` | контаминация; в тексте — `pro omnibus` | ревью 5939105630 |
| L8 | *Inst.* III.1.1 | «quamdiu extra nos est Christus… nobis esse inutile nulliusque momenti» | §12.2 CO-2c |
| L9 | III.24.17 `offert` | `indiscriminatim denuntiat` (727); `proponi` — слова оппонентов (728) | §12.2 CO-2a/b |
| L10 | CO 9:484, пересказ с пометкой «OCR-verified» | текст в рамке «quatenus est spiritualis animarum cibus» | ревью 5939105630 |

Сохраняется исправленная формулировка узла B-1: Дорт II.8 — `EXPLICIT` (действенное искупление избранных); несовместимость с гипотетическим универсализмом — `INFERRED`, а не «прямое отвержение» (Rej. V/VI о другом; Девенант подписал Каноны). Строки матрицы 4/6/7/8 — по ревью `5939105630`.

**HOLD без изменений.** Публикационный HOLD; `LOCATOR_HOLD(visual)` для CO 2, 8, 9, 45, 47, 55; `LOCATOR_HOLD` для CO 49:100; C-17 `TENSION`.

## 14. Ретест #557 @ `7f0dbbd` (rev7) и локатор CO 47 для Ин. 3:16

### 14.1. Ретест (единственный; `issuecomment-6951818068`) — `CONDITIONAL / HOLD`

| Дефект §13.1 | На `7f0dbbd` |
|---|---|
| D1 BLOCKER (Strong III.778: три компонента) | **не исправлен.** Стр. 33 (rev6 §2) и стр. 42 (rev7 §3) говорят «два компонента», стр. 28 и комментарий rev7 — «три». Возникло внутреннее противоречие |
| D2 (блог ≠ A1) | исправлен |
| D3 (негатив Рим. 5:18 у Ричардса) | приемлемо |
| D4 («вербатим») | частично: дословна только первая клауза |
| D5 (Fuller) | исправлен (кандидат `B1`, путь `HOLD`) |
| D6 (усечение 1 Ин. 2:2 — уже у Уоттса p. 153) | не исправлен (стр. 66, 78) |
| D7 / D8 | не исправлены (MINOR: S46 `VERIFY`; «Dr. Watts» — p. 308, не 307) |

Предъявлен точный минимальный diff (п. 1–6). После п. 1–4 позиция AGENT 2 по #557 — `PASS with bounds`. Повторных ретестов не будет.

### 14.2. CO 47: колонка толкования на Ин. 3:16 (OCR + карта листов; `PRINT_IMAGE_HOLD`)

- `operaquaesupersu0075calv`: подписные колонтитулы «Calvini opera. Vol. XLVII.» стоят на листах 21, 29, 37, 45, 53, … (шаг 8). Лист 21 — начало комментария (Ин. 1:1).
- Детектированные номера колонок в `_page_numbers.json`: лист 27 → 14, 28 → 15, 40 → 40, 41 → 41, 43 → 45. Отсюда **лист L = кол. 2(L−21)+1 и 2(L−21)+2**.
- Перикопа Ин. 3:13–16 — внизу листа 51 (кол. 61). Лист 53 = кол. 65–66.
- Фраза «Eodem etiam pertinet nomen mundi… se tamen toti mundo **propitium** ostendit, quum sine exceptione omnes ad fidem Christi vocat, quae nihil aliud est quam ingressus in vitam» стоит в **кол. 65**.
- **Предложение владельцам** (файлы не правились): `fathers/21_` §8.1, `fathers/10_`:333, `fathers/data/fathers-corpus-v1.json`:1668/:2040, `docs/research/atonement/08_`:169 — `CO 47:64` → `CO 47:64–65` (цитируемая фраза — кол. 65).
- Моя запись §12.2 CO-47 («традиционно CO 47:64; колонка не установлена») уточняется: **кол. 65** (OCR / карта листов). `LOCATOR_HOLD(visual)` для CO 47 понижается до `PRINT_IMAGE_HOLD`.

### 14.3. Сводка остаточных HOLD AGENT 2 (что закрыть в этой среде нельзя)

| HOLD | Почему не закрывается | Что нужно |
|---|---|---|
| `LOCATOR_HOLD` CO 49:100 (Рим. 5:18) | тома CR 77 (= CO 49) на archive.org нет; 4 прохода — `STOP_DISCOVERY`. Латынь засвидетельствована печатью трижды (Goodwin 1651; Cox/Beman — `fathers/21_` §8.2; Watts 1811 p. 153 — §13.2); колонка — по корпусу | скан CO 49 (e-rara / Google Books) вне allowlist песочницы |
| `LOCATOR_HOLD` по колонке CO 45:706 (Мф. 26:28) | тома CR 73 (= CO 45) на archive.org нет. Латынь — Watts 1811 p. 153 (OCR) | то же |
| `PRINT_IMAGE_HOLD` для CO 2:727–728, 8:335–336, 9:483–485, 47:65, 55:309–310 | изображения archive.org недоступны (TLS, HTTP 500); текст и колонки — по OCR-слою | ручная визуальная сверка по URL из §12 |
| Nicole, Rainbow, Helm, Archbald | современные защищённые издания; текста в рабочей области нет | легальная копия; без неё — `LOCATOR_HOLD` |
| S2-d / S2-d′ `UNDETERMINED`; S3-c `MISATTRIBUTION_PROBABLE` | исчерпаны тексты CO 9:483–485 и OCR 1667 (§9–§11); новый источник не появился | — (вердикты окончательны при данной доказательной базе) |

Публикационный HOLD и C-17 `TENSION` не затрагиваются.

## 15. Раунд 64 (2026-11-17): исправление ложной информации в корпусе и закрытие `34_` п. 46

После ухода остальных агентов владелец передал AGENT 2 право править корпус (без мерджа). Принцип тот же: прежние строки не удаляются, исправления — датированными пометками «испр. 2026-11-17 / раунд 64»; классы не повышаются.

### 15.1. Новые чтения (OCR-слой IA; `PRINT_IMAGE_HOLD`)

| ID | Свидетель | Локатор | Результат |
|---|---|---|---|
| CTS-R | Calvin, *Romans*, tr. Owen (CTS 1849), `commentariesonep00calv` | лист 225 = **p. 211** (`_page_numbers.json`, confidence 100) | Рим. 5:18: «for though Christ suffered for the sins of the whole world, and is offered through God's benignity indiscriminately to all, yet all do not receive him» |
| WA-152–154 | Watts, *Works* VI (1811), `worksofreverendl06watt` | wrapper 165–167 (pp. 152–154); заглавие «Ruin and Recovery of Mankind» — листы 61/71; «Question XIII» — лист 162, «Question XIV» — лист 176 | p. 152: «Calvin himself has frequently intimated, in his Comments on Scripture, that Christ did in some sense die for all men»; p. 153 Мф. 26:28 — «all mankind» (не «whole human race»); p. 154 Иуд. 4 и вывод «in some sense he died for all». `"without distinction"` по тому — только листы 92, 93, 169 (вне катены) |
| RI-312 | Richards 1846 | wrapper 321 = p. 312 | «First. As to the first position…» — раздел о Кальвине кончился на p. 311 |

### 15.2. Закрыто

- **`34_` §8 п. 46 — CLOSED.** Первая половина пастиша Strong III.778 — Кальвин на **Рим. 5:18** (CTS p. 211; латынь — Watts p. 153). Пастиш трёхчастный: Рим. 5:18 + Мф. 26:28 + Ин. 3:16, все три ложно отнесены к Comm. 1 John 2:2. Звенья Watts → Richards и Richards → Strong (Мф. 26:28) — A2 по тексту; путь Рим. 5:18 → Strong (через Уоттса или напрямую из CTS) — `HOLD`. *(Звено «Richards → Strong (Мф. 26:28)» снято в §16.1; п. 46 остаётся CLOSED по составу цитаты, путь передачи — `OPEN`.)* Фуллер p. 712 — параллель, не звено.
- **`34_` S46 «по памяти, `VERIFY`»** для Рим. 5:18 снят (CTS p. 211). Вторая часть — Мф. 26:28, а не Мк. 14:24.
- **CO 47:64 → CO 47:64–65** (фраза `propitium` — кол. 65; `LOCATOR_HOLD(visual)`).

### 15.3. Исправленная ложная информация (файлы и характер правки)

| Файл | Было | Исправление |
|---|---|---|
| `docs/research/atonement/34_…shedd_distinction.md` | Richards pp. 303–310 — «источник пастиша»; две части; первая — источник открыт; обрыв 1 Ин. 2:2 «у Ричардса»; Фуллер — «кандидат в родословную» | новый **§4.148 (Q144)**, источники **S158** (Watts) и **S159** (CTS Romans); пометки в S39, S46, S50, §4.31 п. 4, §4.33 п. 4 (г), §5 (3 строки), §6 (3 строки хронологии), §8 пп. 33, 46; дополнение к указателю (4.146–4.148); журнал «раунд 64» |
| `docs/research/atonement/22_…registry…md` | 42a «провенанс `VERIFY`»; 42e «источник пастиша», pp. 303–310 | **42a/42e не трогаются** (входят в исторический блок контроля S40 `synchronization_2026-11-02.json`); добавлены 42du (Watts), 42dv (CTS Romans), 42dw (поправка к 42a/42e) |
| `docs/research/atonement/01_prokopenko_article_review.md` §14.1 п. 4 | «Источник пастиша — Richards 1846» | пометка: верно лишь для одной из трёх частей |
| `docs/research/atonement/35_…registry.md` FP-138 | «Richards 1846 = источник пастиша» | пометка: Watts → Richards → Strong, три локуса |
| `08_`, `THEMATIC_TAXONOMY…`, `fathers/00_`, `09_`, `10_`, `21_`, `fathers-corpus-v1.json` | «CO 47:64»; «скан CO 47:64 — `LOCATOR_HOLD`» | «CO 47:64–65»; в `08_` и `21_` — пометка: скан CO 47 прочитан по OCR, фраза — кол. 65, `LOCATOR_HOLD(visual)` |
| `ИСКУПЛЕНИЕ/evidence/AGENT6_HISTORICAL_EXTENT_MATRIX_2026_11_15.md` (Приложение, Rej. II) | «Дорт классифицирует Strong-линию… как пелагианское отравление»; «доктрина Прокопенко — переоткрытие заблуждения, отвергнутого Rej. II.3 и II.6» | поправка **`INVALID`**: Rej. II.6 — о различии *по свободной воле*, Rej. II.3 — о «nullis certo meruisse… fidem»; Strong III.779 и PDF Прокопенко (с. 25, 30–31; `34_` §4.146) учат обратному |
| `01_` §VII (строка «История вопроса»), `README.md` (§34, раунд 8), `THEMATIC_TAXONOMY…` (§34), `synthesis/00_SYNTHESIS_AUTHORITY…` | «источник пастиша Стронга — Richards pp. 303/308–310» | краткая пометка: Ричардс — источник лишь части о Мф. 26:28; пастиш трёхчастный, цепочка Watts → Richards → Strong |

Блок `claimRegister20261026` в `fathers-corpus-v1.json` и таблица ценза пересняты штатными `--write` (новый маркер `LOCATOR_HOLD(visual)` в `fathers/21_`).

### 15.4. Самопроверка (что исправлено в моих собственных черновиках до коммита)

- Латинская цитата Ин. 3:16 в первом черновике §4.148 была дана по памяти («…quae vere ingressus est in vitam») — заменена на прочитанную по CO 47 («quum sine exceptione omnes ad fidem Christi vocat, quae nihil aliud est quam ingressus in vitam», §14.2).
- Удалены непроверенные детали первого черновика: список всех упоминаний «Calvin» у Ричардса, «confidence 100» для якорей Уоттса, ложная ссылка «с. 211 — по `01_` §14.1» (номер страницы взят из `_page_numbers.json`). «Question XIII» и заглавие трактата оставлены только после кавычечной проверки `inside.php`.
- «Не Гал. 5:12» смягчено: Гал. 5:12 тоже содержит «suffered for the sins of the whole world»; к Рим. 5:18 указывает именно пара с «offered… indifferenter».

### 15.5. Не правилось (вне ветки) — предложение владельцам `main`

- *(Выполнено после слияния `origin/main` в ветку, коммит `b188d850`: в конец файла AGENT 5 добавлена датированная поправка; строки не правились.)* `ИСКУПЛЕНИЕ/evidence/AGENT5_CALVIN_EXEGETICAL_DELTA_AUDIT_2026-11-17.md`, стр. 86, 95, 99: «CO 47:64» и «печатный скан CO 47:64 всё ещё `LOCATOR_HOLD`» → «CO 47:64–65; OCR скана прочитан (кол. 65), `LOCATOR_HOLD(visual)`».
- PR #556 (round 58 §4.124 в `02_CONFLICT_LEDGER.md`): та же формула «скан CO 47:64 ещё не сверен»; заявленное в описании ограничение C-17 в диффе отдельной правкой не видно.
- `docs/research/arena/AGENT4_*` — журналы агента; «CO 47:64» там — историческая запись, не правится.

**HOLD без изменений:** колонки CO 49:100 и CO 45:706; `PRINT_IMAGE_HOLD`; права Nicole/Rainbow/Helm/Archbald; публикационный HOLD; C-17 `TENSION`.

## 16. Раунд 65 (2026-11-17): самопоправка по пастишу Стронга, новые чтения и ревью PR #562 (AGENT 7)

### 16.1. Самопоправка: «Richards → Strong по формулировке Мф. 26:28» снято

В раунде 64 (§13.1 (b), §15.2 и пометки в шести файлах) я утверждал: формулировка «not a part of the world only, but **the whole human race**» в Strong III.778 — ричардсовская (у Уоттса — «all mankind»), значит, звено Richards → Strong доказано текстом. **Это неверно.**

- **CTS Harmony III** (пер. W. Pringle, Edinburgh 1846; IA `harmonyofevangel03calvuoft`, лист 220 = **p. 214**; OCR-обёртка 219, кавычечный `inside.php`), под «Mark XIV. 24»: «Which is shed for many. By the word many he means not a part of the world only, but the whole human race; for he contrasts many with one; as if he had said, that he will not be the Redeemer of one man only, but will die in order to deliver many from the condemnation of the curse».
- Ричардс (p. 308) переводит то же место иначе: «designates… opposes many to one… liberate many from the guilt of the curse». Совпадает только буквальный перевод «non partem mundi tantum… sed totum humanum genus».
- Следовательно, совпадение формулировки **не диагностично**: оно не различает каналы «Ричардс», «CTS» и «собственный перевод с латыни».

Вторая и третья части цитаты Стронга тоже не совпадают дословно ни с одним свидетелем: Рим. 5:18 — «goodness / without distinction» ≠ Watts «bounty / indifferently» ≠ CTS «benignity / indiscriminately»; Ин. 3:16 — «holds out the propitiation… summons… door unto hope» ≠ Richards p. 309 «shows himself propitious… calls… an entrance into life».

**Что остаётся доказанным (A2, OCR-слой печати, `PRINT_IMAGE_HOLD`):**

1. Состав пастиша — три места Кальвина (Рим. 5:18 + Мф. 26:28 + Ин. 3:16) под ложным локатором 1 Ин. 2:2; `34_` §8 п. 46 остаётся CLOSED по составу.
2. Звено Watts → Richards: явная ссылка (p. 308), почти дословный английский для 1 Ин. 2:2 и 2 Пет. 2:1, тот же обрыв 1 Ин. 2:2.
3. Стронг пользовался Ричардсом для **тезиса** «Институты избегают определённости, Комментарии принимают всеобщее искупление»: Strong III, p. 777 (лист 16), петит — «Richards, Theology, 303-307, shows that Calvin, while in his early work, the Institutes, he avoided definite statements… yet in his latter works, the Commentaries, acceded to the theory of universal atonement». Указатель Стронга (лист 371): «Richards, James, 555, 644, 773, 777». Сетевой текст godrules.net даёт «302-307» — расхождение изданий или OCR, не сверялось. Указанный Стронгом диапазон кончается на p. 307, т. е. *перед* ричардсовской подборкой цитат (pp. 308–311); при возможном сдвиге пагинации между изданиями из этого ничего не следует.

**Что теперь `OPEN`:** путь самой цитаты в Strong. Сочетание Мф. 26:28 + Ин. 3:16 (рядом у Ричардса, pp. 308–309) и Рим. 5:18 (у Уоттса, на которого ссылается Ричардс) совместимо с работой Стронга по Ричардсу и Уоттсу с собственным переводом с латыни, но это `INFERRED`, не доказано.

Позиция AGENT 7 в #562 («близкая параллель; передача в Strong не установлена») по этому пункту **ближе к верной**, чем моя формула раунда 64.

**Исправлено в файлах этого раунда:**

| Файл | Было (раунд 64) | Стало |
|---|---|---|
| `34_` §4.148 | «родословная Watts → Richards → Strong»; «от Ричардса у Стронга доказуемо взята формулировка Мф. 26:28» | раздел переписан (мой собственный, ещё не слитый): таблица свидетелей с Strong p. 777, Richards p. 309 (Ин. 3:16) и CTS Harmony; колонка «совпадение формулировки»; вывод в шести пунктах; путь в Strong — `OPEN` |
| `34_` §3 | — | новый источник **S160** (CTS Harmony III, p. 214) |
| `34_` S46, §4.31 п. 4 (пометка), §6 строка 1907, §8 п. 33 (пометка), п. 46 (закрывающая пометка), указатель 4.148, журнал | «в передаче Richards p. 308»; «цепочка… документирована»; «доказуемо взята» | «формулировка совпадает с Richards и CTS — канал не устанавливает»; «звено Watts → Richards доказано; путь в Strong — `OPEN`» |
| `22_` 42dw | «Ричардс — источник одной части (Мф. 26:28)» | «Ричардс — не доказанный источник цитаты»; Strong p. 777 — ссылка для тезиса |
| `22_` 42du | «первоисточник подборки Richards» | «источник части подборки Richards» (1 Ин. 2:2, 2 Пет. 2:1) |
| `01_` §14.1 п. 4 и строка «История вопроса», `README.md`, `THEMATIC_TAXONOMY…`, `synthesis/00_…`, `35_` FP-138 | «Ричардс — источник лишь части о Мф. 26:28; цепочка Watts → Richards → Strong» | «Ричардс — не доказанный источник цитаты… путь в Strong — `OPEN`» |

`22_` 42a/42e (блок S40) не правились.

### 16.2. Новые чтения раунда 65

| Код | Свидетель | Локатор | Результат |
|---|---|---|---|
| CTS-H-214 | CTS Harmony III (1846) | лист 220 = p. 214 (`_page_numbers.json`: листы 219 = p. 213 и 221 = p. 215, уверенность 100) | см. §16.1; дата тома 1846 — по метаданным IA («stated date is 1846») |
| ST-777 | Strong III | лист 16 (p. 777) | ссылка «Richards, Theology, 303-307» |
| RI-312–314 | Richards 1846 | листы 324–326 (OCR-обёртка 321–323) | «First / Second / Third position»; p. 313 — заместительство (Мэги); p. 314 — «restoration of the whole human family to the favor of God». **Кальвина и Рим. 5:18 нет**; пункт «pp. 311–314 не читались» в `34_` §8 п. 46 снят |
| RI-map | Richards 1846, `_page_numbers.json`, чанк 6 | — | лист = p + 12 (p. 308 = лист 320); OCR-обёртка = лист − 3. Мои «wrapper = p + 9» и «лист = p + 12» у AGENT 7 **согласуются**: это две системы нумерации |
| ACTA-78–83 | *Acta* 1620, IA `actasynodination00syno` | OCR-обёртка 483 (p. 78) и 488 (p. 83) | британская «Sententia Theologorum Magnae Britanniae, De Articulo secundo» — **pp. 78–83**, а не 78–81, как в `34_` S111, §4.54 и §6 (строка 1620) (исправлено пометками); на p. 83 «Subscripserant» и пять имён — Georgius Landavensis, Joannes Davenantius, Samuel Wardus, Thomas Goad, Gualterus Balcanqual, — затем сразу «Iudicium Theologorum Palatinorum» |
| ACTA-ark | метаданные IA | `identifier-ark` = `ark:/13960/t9g455x02` | HathiTrust `ia.ark:/13960/t9g455x02`, на который опираются досье AGENT 7 о band R и F15-08 в статье 15, — **тот же** Princeton-скан, что и корпусные S110/S111. Это не независимый свидетель (AGENT 7 это предполагал; теперь подтверждено). HathiTrust seq = OCR-обёртка IA + 1 |

### 16.3. Ревью PR #562 (AGENT 7, Draft, `9d9ddef8`): только чтение, ветка не правилась

1. **Пастиш Стронга (`34_` §4.31/Q144, §8 пп. 33, 46; `22_` 42e).** Суть («близкая параллель; передача не установлена») — верна и после §16.1. Недочёты:
   - (а) не учтена ссылка Стронга на Ричардса (p. 777) — единственная документированная связь Strong ↔ Richards;
   - (б) третья часть пастиша (Ин. 3:16, «door unto hope») не названа; у #562 композит фактически двухчастный (Мф. 26:28 + Рим. 5:18);
   - (в) смешение языков в тексте 42e («Matthew 26:28 clause», «1 John 2:2 context», «Calvin-attributed варианты»);
   - (г) «Richards pp. 303–310, 315, 320, 403 — `EXACT_LOCATOR_VERIFIED`» не сопровождается указанием на чтения pp. 311–314 (прочитаны здесь, §16.2).
2. **Коллизия нумерации.** В #562 и в #554 одновременно появились `34_` §4.148 / Q144 и S158 (Watts), с близким, но не тождественным содержанием. При слиянии обоих PR конфликт неизбежен. Предложение MAX: оставить одну §4.148 (в формулировке §16.1: состав — A2, звено Watts → Richards — A2, путь в Strong — `OPEN`), добавить ссылку Strong p. 777 и S160 (CTS Harmony); S158 объединить.
3. **42e и S40.** Правка 42e внутри охраняемого блока S40 сделана через новый механизм `historicalRevisions` в `scripts/atonement_sync_check.py`: явная пара old/new с основанием и тестом `test_s40_retains_the_preimage_with_only_its_reviewed_exact_revision`. Это прозрачный и проверяемый путь, а не обход контроля; ретест до правки задокументирован (`preCorrectionRetest20261117`). Возражение одно: текст ревизии (см. п. 1 (а)–(в)) стоит уточнить до слияния, иначе в охраняемый блок попадёт неполная формула.
4. **Досье band R / *Acta* 1620 и статья 15 (F15-08).**
   - Локаторы *Acta* pp. 78–83 и пять имён на p. 83 **подтверждены** независимым чтением OCR IA (§16.2).
   - Ограничения сформулированы корректно: печатный список имён — не автограф; band R ↔ inv.nr. 128 — кандидат, не подтверждено; Lynch, гл. 4 — не прочитан.
   - Поправка: HathiTrust t9g455x02 — тот же скан, что IA `actasynodination00syno` (ark совпадает). Как второй физический экземпляр годится только KB `ned-kbn-all-00001297-001`.
5. **Сообщение в HUA** отправлено по согласию пользователя (по записи AGENT 7); ответ не поступил — проверять не мне.

### 16.4. Статус

**HOLD без изменений:** колонки CO 49:100 и CO 45:706; `PRINT_IMAGE_HOLD`; права Nicole/Rainbow/Helm/Archbald; публикационный HOLD; C-17 `TENSION`. **Новый `OPEN`:** путь цитаты Strong III.778 (канал не установлен; состав установлен).

## 17. Раунд 66 (2026-11-17): датировка и источник пастиша Strong III.778

Полная запись — `34_` §4.149 (Q145), S161–S163, `22_` 42dx.

### 17.1. Что установлено

| # | Утверждение | Основание | Класс |
|---|---|---|---|
| 1 | Примечание «Richards, Theology, 303-307… he acceded to the theory of universal atonement» уже есть в Strong 1886 (p. 426), в той же формулировке | IA `systematictheolo00strouoft`, лист 450, `inside.php` q=acceded + полное чтение OCR-обёртки 449 | A2 (OCR) |
| 2 | Пастиша «In later days Calvin wrote…» в издании 1886 г. нет | `inside.php`: «door unto hope» — 0; «without distinction» — только в указателе | `STRONG` (отрицательный поиск по OCR одного экземпляра) |
| 3 | В изданиях 1889 и 1902 гг. пастиша тоже нет; впервые он появляется в 1907 г. | Полнотекстовый поиск HathiTrust: фраза о «hyper-Calvinistic» — в 1886/1889/1902/1907/1909, «door unto hope» + Calvin + Richards — только в 1907/1909 | `STRONG` (поиск, без прямого чтения 1889/1902) |
| 4 | Часть «Ин. 3:16» пастиша дословно совпадает с переводом в письме «A Side Light», *New-York Evangelist*, 23.07.1891 (вплоть до ошибки *propitium ostendit* → «holds out the propitiation»); расходится только последнее слово («life» → «hope») | IA FTS (единственное попадание до 1907 г.) + чтение OCR | A2 (OCR); зависимость — `STRONG`; прямое заимствование Стронгом — `OPEN` |
| 5 | Graham 1857 (pp. 86–87) цитирует латынь Кальвина на Рим. 5:18 в толковании 1 Ин. 2:2 («through the goodness of God, is offered equally to all») | IA `spiritofloveorpr00grahuoft`, лист 123 | A2 (OCR); как звено — `PARALLEL`, не доказано |
| 6 | Richards p. 309 (Ин. 3:16) в §4.148 и §16.1 процитирован верно («shows himself propitious… calls all men without exception… an entrance into life») | `inside.php` q=propitious, лист 321 | A2 (OCR); пункт 4 «следующих шагов» раунда 65 закрыт |
| 7 | Рецепция пастиша после 1907 г.: Topical Excerpt Library 1908, Poe 1938, **Thiessen 1949**, Sword of the Lord 1958, McComas 1975, Baker 1994, Towns 1995 | Только сниппеты IA FTS | `LEAD` |

### 17.2. Что не найдено (отрицательные результаты)

- «offered unto all men without distinction» и «not for a part of the world only» (часть «Рим. 5:18») — в IA FTS до 1907 г. 0 попаданий. *[Поправка раунда 69 (§20): «not for a part of the world only» относится к части «Мф. 26:28», а не «Рим. 5:18». Отрицательный результат верен только для точной формы с «for». Форма без «for» — «not a part of the world only» — засвидетельствована с 1740 г.: [J. Wesley], *Serious Considerations concerning the Doctrines of Election and Reprobation. Extracted from a late author* (1740; извлечение из Уоттса; IA `bim_eighteenth-century_serious-considerations-c_watts-isaac_1740`, лист 7 по `inside.php`): «Sub multorum nomine non partem mundi tantum designat, sed totum humanum genus, Under the Name of Many, he signifies not a Part of the World only, but all Mankind» к «Matt. xxvi. v. 8» [sic, = 28]. Далее — Watts, *Works* VI, p. 153 (S158), Richards 1846, CTS Harmony 1846, Bacon 1855 (`34_` §4.148, §4.150, §4.152).]*
- В IA FTS «door unto hope» до 1907 г. не встречается.

### 17.3. Значение для корпуса

- Гипотеза «Стронг взял пастиш у Ричардса» ослаблена ещё больше: ссылка на Ричардса появилась в 1886 г., пастиш — только в 1907 г., и формулировка Ин. 3:16 у них разная.
- Вероятный фон появления пастиша — американский пресвитерианский спор 1889–1893 гг. о пересмотре Вестминстерского исповедания (формулы с «propitiation» по 1 Ин. 2:2). Это `INFERRED`.
- Для `01_` (линия Strong → Chafer/Thiessen) Thiessen 1949 отмечен как воспроизводящий пастиш (`LEAD`, `VERIFY` по книге: книга доступна только через выдачу).

### 17.4. Статус

HOLD без изменений: CO 49:100, CO 45:706, `PRINT_IMAGE_HOLD`, права, публикационный HOLD, C-17 `TENSION`. Путь пастиша: часть «Ин. 3:16» → *New-York Evangelist* 1891 (`STRONG`); части «Рим. 5:18» и «Мф. 26:28» и прямой источник Стронга — `OPEN`. Доступ к HathiTrust заблокирован с адреса песочницы, поэтому прямое чтение изданий 1889 и 1902 гг. отложено.

## 18. Раунд 67 (2026-11-17): часть «Рим. 5:18» пастиша Стронга

Полная запись — `34_` §4.150 (Q146), S164–S165, добавление к S83(b), `22_` 42dy.

| # | Утверждение | Основание | Класс |
|---|---|---|---|
| 1 | Strong III.778, Рим. 5:18: «Christ suffered for the sins of the whole world, and in the goodness of God is offered unto all men without distinction» | `inside.php` по `cu31924092368236`, лист 17 | A2 (OCR) |
| 2 | Th. Scott 1786: «suffered for the sins of the whole world; and is offered indiscriminately to all men, by the goodness of God»; следом — 1 Ин. 2:2 | `inside.php`, лист 13 | A2 (OCR) |
| 3 | R. Anderson 1837: «…by the mercy of God, is offered to all without distinction»; «In this passage Calvin speaks as an interpreter of Scripture; in the Institutes, as the advocate of a system» | `inside.php`, лист 36 | A2 (OCR) |
| 4 | W. Bacon 1855 (= S83b): катена Мф. 26:28 → Рим. 5:18 («offered to all, without distinction») → 1 Кор. 8:11 → 2 Пет. 2:1 → 1 Ин. 2:2 | полный OCR-текст `_djvu.txt`, листы 65–66 | A2 (OCR) |
| 5 | Ни один свидетель не даёт формулировку Стронга целиком; все элементы — буквальные переводы одной латыни; общей ошибки нет | сравнение 1–4 с Watts (S158) и Graham (S162) | вывод: `PARALLEL`, недиагностично |
| 6 | Тезис «Кальвин-экзегет против „Наставления“» в англоязычной литературе — по меньшей мере с 1837 г. (до Ричардса 1846) | п. 3 | A2; связь Anderson → Richards **не** установлена |
| 7 | Ложный локатор «1 John 2:2» у Стронга может происходить из катен, где Рим. 5:18 соседствует с 1 Ин. 2:2 (Scott, Bacon, Graham) | структурное наблюдение | `INFERRED` |

**Статус пути пастиша:** часть «Ин. 3:16» — `STRONG` (общая ошибка, *New-York Evangelist* 1891); части «Рим. 5:18» и «Мф. 26:28» — `PARALLEL`, недиагностично; прямой источник Стронга — `OPEN`. HOLD без изменений.

## 19. Раунд 68 (2026-11-17): CO 45 найден — локатор Мф. 26:28 исправлен с 706 на 711

Полная запись — `34_` §4.151 (Q147), S166, `22_` 42dz.

**Поправка к §14 (строка о `LOCATOR_HOLD` по CO 45:706) и к «Статусу» §16.4, §17.4, §18.** Утверждение «тома CR 73 (= CO 45) на archive.org нет» было **ложным**: том лежит под идентификатором `ioanniscalviniop0045vari` (CO vol. 45, Brunsvigae 1891; загружен в 2025 г.), который не совпадает со схемой `00NNcalv`, по которой я искал раньше. Сами записи §14–§18 оставлены как история; действует эта поправка.

| # | Утверждение | Основание | Класс |
|---|---|---|---|
| 1 | Толкование Кальвина на Мф. 26:28 стоит под леммой «Marc. 24. Hic est sanguis meus» и начинается внизу CO 45:710 | OCR-обёртка 378, chunk 1 | A2 (OCR) |
| 2 | «Caeterum sub multorum nomine non partem mundi tantum designat, sed totum humanum genus…» и «Notandum tamen simul est, quod apud Lucam (pro vobis)…» — **CO 45:711** | `inside.php` q="partem mundi" (лист 380) и OCR-обёртка 379; колонцифры 706/710/712/714 на обёртках 376/378/379/380 согласованы | A2; колонка — `LOCATOR_HOLD(visual)` |
| 3 | «CO 45:706» во всём корпусе — ошибка: кол. 706 = Мф. 26:26 «Hoc est corpus meum» | OCR-обёртка 376 | A2 |
| 4 | Вывод F-29 (вторая «цитата» Кальвина на Мф. 26:28 в старом `15_` §3.2 сфабрикована) подтверждён по латыни CO | п. 2 | A2 |
| 5 | Том CO 49 (Рим. 5:18) на IA не найден; CO 49:100 остаётся `HOLD` | IA advancedsearch + FTS «Communem omnium gratiam facit» | отрицательный поиск |

**Исправлено в файлах:** `15_` §3.2; `fathers/09_` F-29; `fathers/10_`; `fathers/16_` (3 места); `arena/AGENT4_DOGMATICS_*` и `arena/AGENT4_EDITORIAL_*` (пометка «→ 711»); `34_` (абзац HOLD в §4.148). Сгенерированный `fathers-corpus-v1.json` пересобран.

**HOLD после раунда 68:** CO 49:100; `LOCATOR_HOLD(visual)` для CO 45:711 и CO 47:64–65; `PRINT_IMAGE_HOLD`; права; публикационный HOLD; C-17 `TENSION`.

## 20. Раунд 69 (2026-11-17): остальные колонки CO; «CO 9:524» опровергнут

Полная запись — `34_` §4.152 (Q148), S167, `22_` 42ea.

| # | Утверждение | Основание | Класс |
|---|---|---|---|
| 1 | 1 Тим. 2:4 — **CO 52:268**: «nullum mundi vel populum, vel ordinem a salute excludi… At de hominum generibus, non singulis personis, sermo est» | `operaquaesupersu0080calv` (CR 80 = CO 52), OCR-обёртка 145; «268» над правой колонкой | A2 (OCR) |
| 2 | 1 Ин. 2:2 — **CO 55:310** (всё толкование 2:2 в правой колонке; 2:1 — кол. 309) | `operaquaesupersu0083calv`, обёртка 166; «310» над правой колонкой | A2; `LOCATOR_APPROX` CO-4 снят |
| 3 | Мф. 26:28 — **CO 45:711** по второму, независимому экземпляру | `operaquaesupersu0000calv` (том в метаданных не указан; по тексту — CO 45), обёртка 375; «112» = 712 справа, фраза — в левой колонке | A2; `LOCATOR_HOLD(visual)` |
| 4 | `operaquaesupersu0050calv_c6j3` — это CO 50 («Vol. L», Гал. 1); тома CO 49 на IA нет | обёртка 100 | CO 49:100 — `HOLD` |
| 5 | В CO 9:523–524 фразы «pro solis electis passus est» **нет**; там: «Christum omnibus generaliter corpus suum et sanguinem offerre: sed quia infideles ianuam claudunt eius liberalitati, non recipere quod offertur» | `operaquaesupersu0037calv`, обёртка 339 (колонтитул «… 524») | A2 |
| 6 | Во всём томе CO 9 «electis passus» — 0 совпадений; «solis electis» — 1 (CO 9:485, об освящении) | `inside.php` по тому | отрицательный OCR-поиск (точные формы) |
| 7 | Заголовок `22_` п. 11 (*Defensio sanae et orthodoxae doctrinae de sacramentis… contra Heshusii*) смешивает *Defensio* 1555 (Цюрихское соглашение) и *Dilucida explicatio… ad discutiendas Heshusii nebulas* (Genevae: Badius, 1561) | титулы в CO 9, `inside.php` листы 19 и 46 | A2 |
| 8 | Поправка к §17.2: «not for a part of the world only» — часть «Мф. 26:28», не «Рим. 5:18»; ноль только для формы с «for». Форма без «for» — с 1740 г. ([Wesley], *Serious Considerations… Extracted from a late author*, лист 7: «not a Part of the World only, but all Mankind») | `inside.php` q="part of the world" | A2 (OCR) |

**Вердикты.** S3-c — `MISATTRIBUTION_PROBABLE` без изменений; основание усилено прямым чтением кол. 523–524. Повышения классов нет.

**Исправлено в файлах:** `22_` п. 11 (поправка), строка № 11 таблицы (`~~Verified~~ → MISATTRIBUTION_PROBABLE`), 42ea; `01_` п. 3 о Хесхузии (`SUPERSEDED`); AGENT6 HOLD № 7 (пометка); в этом файле — CO-4, строка `EXACT_LOCATORS` и §17.2.

**HOLD после раунда 69:** CO 49:100; `LOCATOR_HOLD(visual)` для CO 45:711 и CO 47:64–65; `PRINT_IMAGE_HOLD`; права; публикационный HOLD; C-17 `TENSION`.

## 21. Раунд 70 (2026-11-17): ревизия верхних пунктов `22_` и итоговой матрицы

**Задача.** Снять ложные «Verified» в `22_` §VII и исправить пункты реестра, которые расходятся с первичным текстом или с исправленными файлами корпуса. Подробности — `34_` §4.153 (Q149), S168.

| # | Место | Проверка | Итог |
|---|---|---|---|
| 1 | Афанасий, *De Inc.* | First1KGreek (Robertson 1893): 8.4, 9.1–2, 20.2, 20.6, 37.7 — ἀντὶ/ὑπὲρ πάντων, τὸ ὀφειλόμενον | `PARTIAL` (реестр опускал язык долга «за всех») |
| 2 | Августин, *De corr.* 7 | `augustinus.it`: 7.12, 7.14, 13.40, 14.44 | `PARTIAL`; ограничения крови нет; `01_` п. 2 помечен |
| 3 | Готшалк | IA FTS — 0; Ussher IV, с. 44 (Гинкмар) | `QUOTE_UNVERIFIED`; суть — A2 через оппонента |
| 4 | Гейдельберг, в. 37 | Schaff III, лист 335 (≈ с. 319) | `PARTIAL`: «the sin of the whole human race» |
| 5 | Турретин | оглавление t. II (1847), лист 13 | `LOCATOR_ERROR`: необходимость — Q. X (p. 368), объект — Q. XIV (p. 400) |
| 6 | Оуэн, «трилемма несокрушима» | — | `EVALUATIVE` |
| 7 | Буньян | TCP A30198, с. 25; `15_` §6; FP-136 | `SUPERSEDED` |
| 8 | Русские баптисты, пп. 34–37 | `14_` (Волна 17) | нумерация, инициалы, 1928 г. — исправлены; Павлов 1906 (место) — `HOLD` |
| 9 | Сперджен | `17_` | № 566, не #564 |
| 10 | TMS, Гибсоны | `09_` §1; `17_` | `SECONDARY` |

**Вердикты по S1–S5 не меняются.** Ни одна правка раунда 70 не касается локаторов Кальвина и не повышает классы. Готшалк и Августин — фон, а не доказательство тезиса о Кальвине. Снятие «Verified» с этих строк убирает лишь ложную опору, на которую мог бы сослаться довод S3-c / C-17.

**Исправлено в файлах:** `22_` (пп. 1, 3, 7, 14, 21, 27, 34–37; матрица; итоговая фраза; 42eb); `01_` п. 2; `02_` пп. 8, 10; `21_` (CO 55:310); `34_` (§4.153, S168, журнал, индекс).

**HOLD после раунда 70:** CO 49:100; `LOCATOR_HOLD(visual)` для CO 45:711 и CO 47:64–65; `PRINT_IMAGE_HOLD`; критические издания (Lambot 1945, PL 121, CSEL 92, SC 199) не открывались; права; публикационный HOLD; C-17 `TENSION`.

## 22. Раунд 71 (2026-11-17): библиографическая ревизия `22_`, пп. 4, 5, 16, 22, 24, строка № 39

Подробности — `34_` §4.154 (Q150), S169.

| # | Место | Итог |
|---|---|---|
| 1 | *Enchiridion* 103 (п. 4) | `PARAPHRASE`: «omnes homines, omne genus hominum… per quascumque differentias distributos»; второе из двух толкований |
| 2 | Проспер, возражение I (п. 5) | сверено: Hurter 35 (1877), с. 186 — «recte omnes dicantur redempti… redemptionis proprietas… penes illos»; `02_` п. 5 — `PARTIAL` |
| 3 | 39 статей (п. 16) | `PARTIAL`: ст. XXXI «for all the sins of the whole world» (Schaff III ≈ с. 507) |
| 4 | *Formula Consensus Helvetica* (п. 22) | `LOCATOR_ERROR`: в Schaff III нет (сс. 437–485 — шотландские исповедания); Schaff I, указатель «478»; текст — Niemeyer, pp. 729–739 |
| 5 | Ussher, *True Intent and Extent* (п. 24) | `LOCATOR_ERROR`: Works XII, сс. 551–571, не 559–596; с. 565 — против «only for the elect, and for others nullo modo» |
| 6 | Ходж, строка № 39 | `PARTIAL` (вывод): II, 558 «Augustinians do not deny that Christ died for all men…» |

**Вердикты S1–S5 не меняются.** Правки касаются фона (патристика, исповедания, XVII в.), а не локаторов Кальвина.

**HOLD после раунда 71:** без изменений (см. §21).

## 23. Раунд 72 (2026-11-17): библиографическая ревизия `22_`, пп. 15, 23, 31, 32

Подробности — `34_` §4.155 (Q151), S170.

| # | Место | Итог |
|---|---|---|
| 1 | Второе Гельветическое (п. 15) | `LOCATOR_ERROR` (незначительная): Schaff III, сс. 233–306, а не 237–306 |
| 2 | Davenant / Allport (п. 23) | Allport, т. II — 1832 (титул); издание in folio 1650 г. подтверждено; «1627» — `DATE_HOLD` |
| 3 | Эдвардс, *Freedom of the Will* (п. 31) | `LOCATOR_ERROR`: цитата «in some sense… for all» — в «Conclusion» (Andover 1840, ≈ с. 405), а не в ч. IV, разд. XII |
| 4 | Эдвардс, «Satisfaction for Sin» (п. 32) | `ATTRIBUTION_ERROR`: *Remarks* (1796), гл. VI, а не *Misc. Observations* (1793); «Фокус» — `QUOTE_RISK` |
| 5 | `01_` §2.3 (Эдвардс) | `INACCURATE`: это не «гипотетический аргумент оппонента», а собственная оговорка Эдвардса |
| 6 | `17_` §2.1, пометка волны 18 | п. 4 добавлен: «Sect. XII» → «Conclusion»; гл. V → гл. VI *Remarks* |
| 7 | AGENT 6, матрица (строка 8) | та же неточность («гипотетический аргумент оппонента»); файл заморожен, расхождение зафиксировано здесь |

**Вердикты S1–S5 не меняются.** Правки касаются фона (исповедания, XVII–XVIII вв.), а не локаторов Кальвина.

**HOLD после раунда 72:** как в §21. Добавлены `DATE_HOLD` (Davenant «1627») и `LOCATOR_HOLD` (страница гл. VI *Remarks*).

## 24. Раунд 73 (2026-11-17): библиографическая ревизия `22_`, пп. 8, 12, 13, 19, 20, 30

Подробности — `34_` §4.156 (Q152), S171.

| # | Место | Итог |
|---|---|---|
| 1 | Ансельм, *Cur Deus homo* (п. 8) | локаторы II.14 и II.18 подтверждены: «pro peccatis totius mundi… et plus in infinitum»; «dignitas infinita» — `PARAPHRASE`; «Фокус» — `PARTIAL` |
| 2 | Беза, 1570 (п. 12) | `IMPRINT_ERROR_PROBABLE`: Креспен (Gilmont № 70/1), а не Виньон |
| 3 | Урсин, в. 37 (п. 13) | `PARTIAL`: «Christ satisfied for all, as it respects the sufficiency… but not as it respects the application» (Williard 1851, с. 215); «Heidelberg, 1591» — `IMPRINT_HOLD` |
| 4 | Du Moulin, *Examen* (п. 19) | `IMPRINT_ERROR_PROBABLE`: Амстердам (Gass 1857; Roehrich 1867; van de Schoor 1995), а не Седан |
| 5 | Spanheim (п. 20) | подтверждено (A3): Лейден, 1646, 3 тома |
| 6 | 2LBC 8.8 (п. 30) | `INACCURATE`: «obtained Eternal Redemption… uniting them to himself» вместо «purchased redemption» в WCF VIII.8 |

**Вердикты S1–S5 не меняются.** Урсин и Ансельм говорят о достаточности; это фон, а не локатор Кальвина.

**HOLD после раунда 73:** как в §21–§23; добавлено `IMPRINT_HOLD` (Урсин).

## 25. Раунд 74 (2026-11-17): `22_`, пп. 2 (Кирилл) и 6 (Оранж)

Подробности — `34_` §4.157 (Q153), S172.

| # | Место | Итог |
|---|---|---|
| 1 | Кирилл, *Огл.* 13.4 (п. 2) | текст подтверждён (в т. ч. по скану PG 33, лист 386; колонка — `LOCATOR_HOLD`); контекст антидокетический, «против языческих богов» — ошибка; «достаточность» — `INFERRED`; итог — `PARTIAL` |
| 2 | Оранж II (п. 6) | Mansi 8:712 сл. подтверждено по скану (кан. 5 — кол. 713; заключение — кол. 717–718); «Фокус» верен; объёма искупления в прочитанных колонках нет; DH — A3 |
| 3 | `22_`, 42ee | исправлено размещение (раунд 73 вставил 42ee внутрь 42ed); текст не изменён |

**Вердикты S1–S5 не меняются.** Кирилл и Оранж к локаторам Кальвина отношения не имеют.

**HOLD после раунда 74:** как в §21–§24; добавлено `LOCATOR_HOLD` (колонка PG 33 для XIII.4).

## 26. Раунд 75 (2026-11-17): `01_` §2.3 — Ходж и Сперджен; `22_` п. 39

Подробности — `34_` §4.158 (Q154), S173.

| # | Место | Итог |
|---|---|---|
| 1 | `01_` §2.3, Ходж | `PARTIAL`: Амиро подробно разобран в ST II, гл. I §4 (321–324), а не в гл. VIII; опущены «There is a sense… He died for all» (546) и «Augustinians do not deny that Christ died for all men» (558) |
| 2 | `01_` §2.3, Сперджен | `CONFLATION`: «смерть за людей в аду… monstrous iniquity» — «A Defense of Calvinism» (*Autobiography*, т. 1), а не № 566; в № 566 — «in that other sense… a propitiation for the sins of the whole world» |
| 3 | `22_` п. 39 | `PARTIAL` («Фокус»: подробный разбор Амиро — не в гл. VIII) |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 75:** как в §25; факсимиле *Autobiography* т. 1 / MTP 10 — A2.

## 27. Раунд 76 (2026-11-17): `01_` §2.2 п. 4 — «Миф о вине Безы»

Подробности — `34_` §4.159 (Q155), S174.

| # | Место | Итог |
|---|---|---|
| 1 | `01_` §2.2 п. 4, Мюллер | `PARTIAL`: *After Calvin*, с. 15 — непрерывность в ограничении *действенности*; гипотетический универсализм включён в «полную картину»; Буцер и Вермильи не названы |
| 2 | `01_` §2.2 п. 4, Мускулус | противоречит первоисточнику: *Common places* (1578) — «vniuersall redemption… for all the whole worlde… redy for all men» |
| 3 | `01_` §2.2 п. 4, Вермильи | `PARTIAL`: ломбардская формула и 1 Тим. 2:4 = «some of all kindes», без формулы ограниченного объёма |
| 4 | `01_` §2.2 п. 4, Буцер / Труман | Буцер не сверен; Труман — `SOURCE_UNSPECIFIED` |
| 5 | `15_` §5 пп. 1–2 | поправка рядом с текстом (`PARTIAL`) |
| 6 | Матрица AGENT 6, §9 строка 2 (заморожена) | та же ошибка («Буцер, Мускулус, Вермильи — партикуляристы»; «Trthen» — опечатка); не редактируется |

**Вердикты S1–S5 не меняются.** S3 (Кальвин в ряду реформатов) не опирается на Мускулуса.

**HOLD после раунда 76:** как в §26; латинские *Loci* Мускулуса и Вермильи, Буцер (Рим., 1536), печатная пагинация сканов — A2/HOLD.

## 28. Раунд 77 (2026-11-17): А. А. Ходж, *Outlines of Theology* (1879), гл. XXV

Подробности — `34_` §4.160 (Q156), S175.

| # | Место | Итог |
|---|---|---|
| 1 | `17_` §6.4 (HOLD страницы) | снят: место Прокопенко — 1879, с. 416, вопр. 17 I.5; пересказ подлинный |
| 2 | `22_` п. 40, глава | верно (гл. XXV, сс. 401–425) |
| 3 | `22_` п. 40, «Фокус» | `PARTIAL`: «part of the purchase of Christ’s blood», «impetrate temporal blessings for all»; опущены «removed all legal obstacles from the salvation of any and every man» и «applied… if God so wills it» |
| 4 | Ходж о Кальвине на 1 Ин. 2:2 (с. 417) | `PARTIAL`: CO 55:310 — «verum esse illud dictum fateor, nego tamen praesenti loco quadrare» |

**Вердикты S1–S5 не меняются.** К S2 (1 Ин. 2:2, CO 55:310): популярная форма «Кальвин учил sufficienter/efficaciter на 1 Ин. 2:2» неточна и у Ходжа; верно — «признавал истинность формулы, но отвергал её как толкование этого стиха».

**HOLD после раунда 77:** как в §27; факсимиле *Outlines* — A2.

## 29. Раунд 78 (2026-11-17): Дэвенант, *Dissertatio de Morte Christi* — дата «1627»

Подробности — `34_` §4.161 (Q157), S176.

| # | Место | Итог |
|---|---|---|
| 1 | `22_` п. 23, «1627» | `DATE_ERROR_PROBABLE`: 1627 — *Expositio ad Colossenses* (Allport, «Life», т. I) |
| 2 | `23_`, «написан в 1627 г.» | то же; поправка рядом с текстом |
| 3 | Матрица AGENT 3, оговорка по Дэвенанту («1627 — сочинение») | то же; файл не правится |
| 4 | Датировка по предисловию 1650 г. | лекции до или сразу после Дорта; отделка после Колоссянам и *Praelectiones*; издание задержано королевским запретом |

**Вердикты S1–S5 не меняются.** HOLD раунда 72 по дате п. 23 снят и заменён на `DATE_ERROR_PROBABLE`.

**HOLD после раунда 78:** как в §28; место печати 1650 г.; римская пагинация «Life».

## 30. Раунд 79 (2026-11-17): `01_` §2.4 — 2 Пет. 2:1 и 1 Ин. 2:2

Подробности — `34_` §4.162 (Q158), S177.

| # | Место | Итог |
|---|---|---|
| 1 | `01_` §2.4 п. 1: δεσπότης «нигде» не имя Христа | `FALSE`: Иуд. 4 (SBLGNT); всего 10 случаев в НЗ |
| 2 | `01_` §2.4 п. 1: «прямая аллюзия» на Втор. 32:5–6 | LXX `ἐκτήσατο` (`κτάομαι`), не `ἀγοράζω`; эхо — гипотеза |
| 3 | `01_` §2.4 п. 1: подача довода | `OMITS_AUTHOR_ENGAGEMENT`: Прокопенко сам цитирует Мак-Артура (сн. 58) и отвечает |
| 4 | `01_` §2.4 п. 2: «мир = все неверующие» | `TRUNCATION`: у Прокопенко «или, по крайней мере, всё человечество без разбора» |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 79:** как в §29; страницы PDF Прокопенко по факсимиле; аппарат NA28 к Иуд. 4 — только по SBLGNT.

## 31. Раунд 80 (2026-11-17): `01_` §§2.5–2.6 — двойная уплата и лапсарианские схемы

Подробности — `34_` §4.163 (Q159), S178.

| # | Место | Итог |
|---|---|---|
| 1 | §2.5: «трилемма Оуэна» | `MISIDENTIFIED_TARGET`: в статье Беттнер (сн. 70) и Грудем (сн. 71) |
| 2 | §2.5: «смешивает приобретение и применение» | `MISREPRESENTATION`: автор их различает и цитирует Дорт II.8 о приобретении веры |
| 3 | §2.5: «приговор снят Голгофой» | `TENSION_WITH_WCF_XI.4` |
| 4 | §2.5: «крест недостаточен» | `TENSION_WITH_DORT_II.3/II.6` (Шафф III, листы 575–576, 600–601) |
| 5 | §2.6: описание схемы | `ACCURATE`; опущена оговорка сн. 95 |
| 6 | §2.6: «Тринитарный коллапс», «4 цели» | `CONTESTED`; стр. 31–36 — HOLD |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 80:** как в §30; стр. 31–36 PDF Прокопенко; печатные номера Шаффа III.

## 32. Раунд 81 (2026-11-17): `01_` §2.1 и §2.2 п. 1 — Томас, вероучение TMS, Афанасий

Подробности — `34_` §4.164 (Q160), S179.

| # | Место | Итог |
|---|---|---|
| 1 | `01_` §2.1: Томас — «традиция Чейфера» | учёба в DTS подтверждена; взгляд на объём — `UNVERIFIED` |
| 2 | `01_` §2.1: *Biblical Doctrine* «pp. 544–555» | расходится с `09_` (pp. 543–558) |
| 3 | `01_` §2.1: «ясный конфессиональный стандарт» | `ANACHRONISM` для 2019 г.: статьи `Atonement` в снимках до 23.04.2024 нет |
| 4 | `09_` п. 3, `10_` п. 6, `THEMATIC_TAXONOMY`: «в 2023 г.» | `DATE_ERROR`: между 23.04 и 25.07.2024 (Wayback) |
| 5 | `01_` §2.1: «иллюзия нейтралитета» | `MISREPRESENTATION` подачи (R01; с. 8, 19) |
| 6 | `01_` §2.2 п. 1: Афанасий «не об уплате» | `PARTIAL`: *De Inc.* 9.2, 20.2 |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 81:** как в §31; печатный каталог TMS 2023–2024; страницы *Biblical Doctrine*; локатор сн. 3 Прокопенко.

## 33. Раунд 82 (2026-11-17): `01_` — шапка, §1, §3 раннего обзора; цели креста по веб-изданию

Подробности — `34_` §4.165 (Q161), S180. Новый носитель: веб-издание статьи на prokopenkobooks.ru (2023) — полный текст, включая разделы «Цели жертвы Христовой» и «Заключение», недоступные в PDF через инструмент чтения.

| # | Место | Итог |
|---|---|---|
| 1 | шапка: ярлык «4-пунктный / гипотетический универсализм» | `LABEL_IMPOSED`: самоназвание — «сублапсарианство», «неограниченное искупление с ограниченным применением» |
| 2 | §1: «крайности новоначальных»; «отвергает действенное искупление» | `PARAPHRASE_IN_QUOTES`; `IMPRECISE` |
| 3 | §2.6: «умилостивительной» | слово подтверждено; смысл — временная милость; вывод рецензии — `MISREPRESENTATION` |
| 4 | §2.6: «4 цели» | у автора «три, возможно четыре»; четвёртая гипотетична |
| 5 | §3 п. 1: «амиральдианство», «популярно в США» | `OVERSTATED`; `UNSOURCED` |
| 6 | §3 п. 2: «гипотетическая возможность» | `CONTRADICTED_BY_SOURCE` |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 82:** как в §32, кроме «стр. 31–36 PDF» — снят по тексту; страницы PDF для этих разделов и их сноски не сверены.

## 34. Раунд 83 (2026-11-17): полный PDF статьи — ярлыки, сноски, страницы

Подробности — `34_` §4.166 (Q162), S181. Источник: полный 40-страничный PDF от пользователя (создан 11.06.2019; в репозиторий не добавлен).

| # | Место | Итог |
|---|---|---|
| 1 | `01_` шапка: «4-пунктный / гипотетический универсализм» | `LABEL_IMPOSED` подтверждён: 0 совпадений в тексте |
| 2 | `01_` §2.1: *Biblical Doctrine* p. 544 | автор сам ссылается на учебник: сн. 91 (с. 28), p. 544 |
| 3 | `01_` §2.2 п. 1: сн. 3 | «Гл. 4 § 20» = *De Inc.* 20; HOLD снят |
| 4 | `01_` §2.6: страницы целей | с. 31–36 установлены; HOLD снят |
| 5 | `01_` R03: Шафф III (сн. 6, 15, 16) | `ACCURATE` (англ. орфография ст. XXXI = Шафф, редакция 1571 г.); в XI.16 многоточие опускает «per fidem» |

**Вердикты S1–S5 не меняются.**

**Отменено:** правка «`09_` 1986 → 1987» — источника нет; «1986» там — год основания TMS (`34_` §4.166).

**HOLD после раунда 83:** как в §33, кроме снятых «стр. 31–36» и «сн. 3»; Лютер (*LW* 26), Цвингли (рус. изд.) — не сверены.

## 35. Раунд 84 (2026-11-17): «цитирует» ≠ «разделяет позицию» — повторный объективный проход

Подробности — `34_` §4.167 (Q163), S182; полный разбор — `ИСКУПЛЕНИЕ/evidence/AGENT2_PROKOPENKO_CITED_VS_HELD_REPASS_2026-11-17.md` (новый файл; «Владение файлами» в шапке этого аудита относится к раунду его создания). Источник — тот же полный PDF (S181). Метод — четыре уровня: текст статьи → подача цитируемого → его собственная позиция → вывод автора.

| # | Место | Итог |
|---|---|---|
| 1 | §34 п. 1 «`LABEL_IMPOSED` подтверждён» | **уточнено**: верно только для самоназвания; по существу классификация «умеренный / четырёхпунктный, гипотетический универсализм» обоснована (с. 18, 30, 36; Уорфилд 1915; Ходж *ST* II §4) |
| 2 | заключение статьи (с. 36): «это признают… те, кто исповедует ограниченное искупление» | `CONFLATION_AT_CONCLUSION`: формулу «заплатил за всех, не вменяется до веры» в статье даёт Гангел (всеобщий лагерь); частный лагерь объясняет тексты благами, временным умилостивлением или аналогией |
| 3 | Спроул (сн. 91) | `CONJECTURE_MISREADS_SOURCE`: у Спроула ограничение в замысле при неограниченной ценности (Ligonier 2021) |
| 4 | Ч. Ходж (сн. 36) | цитата точна; `SELECTIVE_CITATION` на уровне вывода: *ST* II §4, pp. 321–324, отвергает порядок «redemption precedes election» (= с. 30, столбец 3) |
| 5 | Хиберт (с. 16–17) | `AFFILIATION_ERROR`: BJU Press был только издателем; Southern Baptist Seminary, Tabor College, MBBS |
| 6 | МакАртур, Сперджен | ярлыки и подача на уровне «подача» честные (Сперджен: «особый замысел», сн. 45); расхождение — в выводе «заплатил за всех» |
| 7 | `13_` (Дэниел) | «страница за страницей» — `UNVERIFIED` (частично расходится с текстом); «специалист по Коттону» — `FACT_ERROR` (Gill, Edinburgh 1983); цитата p. 363 — `UNVERIFIED_QUOTE`; «сдвиг» — `PARTIAL` |
| 8 | `34_` §4.39 и п. «(раунд 16)» в §5: «Бакстера нет в библиографии» | `FACT_ERROR`: *Catholik Theologie* в сн. 34 и в библиографии; «структурно совпадает» остаётся |
| 9 | `34_` §4.28 и `01_`: «Talbot» как школа Прокопенко | `UNSUPPORTED`: в Талботе учился МакАртур (с. 1–2) |
| 10 | `01_`, строка 974: «Источник таблицы — Strong → …» | прямые источники — Эриксон и Тиссен (автор их называет сам); Стронг — `LINEAGE_NOT_CITATION`; синонимию «инфра-» и «суб-» автор признаёт сам (сн. 95) |
| 11 | зависимость структур от учебников | разделы истории, «баланса» и таблицы опираются на названные самим автором вторичные работы; композиция всей статьи по учебнику **не доказана** |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 84:** как в §34; добавлены: Daniel, *History and Theology of Calvinism* pp. 360–363 (книга не получена); взгляды МакАртура и Беркхофа на порядок решений; кальвинизм Хиберта (не установлен ни в одну сторону).

## 36. Раунд 85 (2026-11-17): собственные тексты цитируемых — хирургическая сверка

Подробности — `34_` §4.168 (Q164), S183; полный разбор — `ИСКУПЛЕНИЕ/evidence/AGENT2_PROKOPENKO_CITED_VS_HELD_REPASS_2026-11-17.md`, §8.

| # | Место | Итог |
|---|---|---|
| 1 | МакАртур — «Неверный аргумент» (с. 19–20) | `OMITTED_COUNTERPOSITION`: в GTY 90-277 (2004) МакАртур сам пользуется доводом «double jeopardy»; статья называет носителями только Беттнера и Грудема | *(Раунд 125, §76: позиция МакАртура менялась — в 1990 г. он отказывался от ярлыка «limited atonement»; вердикт прежний.)*
| 2 | МакАртур — MSB к 1 Ин. 2:2 (сн. 69) | цитата точна; рядом прямое отрицание уплаты за осуждённых → дополнительная опора для `CONFLATION_AT_CONCLUSION` (с. 36) |
| 3 | Гангел (с. 13): «флагманская кальвинистская школа» | `FRAMING_AS_CONCESSION` (мягко): Чейфер, основатель DTS, — «unlimited redemptionist» |
| 4 | Тиссен (сн. 95–96) | ошибки нет: Доэрксен 1979 назван; поправка к `01_` (Тиссен 1949 — арминианин; S41) |
| 5 | Стронг в родословной | уточнение §35 п. 10: `LINEAGE_VIA_CITED_TEXTBOOK` (Erickson *CT*², p. 852) |
| 6 | Бакстер (сн. 34) | точно; мягкий `SELECTIVE_CITATION` (опущено «resolved into that of Predestination») |
| 7 | Демарест / Lewis & Demarest | открытая опора на учебники одной школы; «страница за страницей» — `UNVERIFIED` |
| 8 | Написание | «Мак-Артур» → «МакАртур» в собственном тексте раунда 84 (в цитатах из статьи — как у автора) |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 85:** как в §35; добавлены: место многоточия в MSB 1997, с. 1965; рев. Тиссен, с. 104–105; русско-английское соответствие страниц Эриксона.

## 37. Раунд 86 (2026-11-17): только первоисточники — сканы раздела «баланса»

Подробности — `34_` §4.169 (Q165), S184; REPASS-документ, §9. Правило: без текста скана — «проверить».

| # | Место | Итог |
|---|---|---|
| 1 | Куйпер (с. 12, сн. 49) | `ELLIPSIS_REMOVES_QUALIFIER`: опущено «in the place of… accurate enough… will not themselves have to suffer that penalty» (1959, с. 78); чьё многоточие (Дэниел или автор) — HOLD |
| 2 | Беркхоф (с. 11–12) | `OMITTED_COUNTERPOSITION`: «Extent», п. 2 — «This dubious and very unsatisfactory view» о двойном декрете (= столбец 3, с. 30) |
| 3 | А. А. Ходж (сн. 37) | `TRANSLATION_SHIFT` (reference → применение); опущен п. II о порядке декретов |
| 4 | Ашшер, Эдвардс, Шедд | `ACCURATE` (Ашшер p. 567; Эдвардс II.179; Шедд II.470/475; у Шедда снято «well») |
| 5 | Лютер (сн. 5) | смысл подтверждён по переводу 1575 г.; *LW* 26 — проверить |
| 6 | Характеристики авторов | Ашшер «английский», Беркхоф «пресвитерианский» (также `17_`, стр. 532), Куйпер «систематического богословия» — `DESIGNATION_IMPRECISE` |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 86:** как в §36; добавлены: имя Амвросия на Ussher p. 567 (OCR); Gomes 2003, p. 741–743; страницы Банер-издания Беркхофа; должности Куйпера до 1959 г.

## 38. Раунд 87 (2026-11-17): оставшиеся сноски истории и «баланса»

Подробности — `34_` §4.170 (Q166), S185; REPASS-документ, §10.

| # | Место | Итог |
|---|---|---|
| 1 | Сперджен, сн. 45 (вторая цитата) | `LOCATOR_ERROR`: № 3331, MTP 58:583–584 (по Мюррею), а не MTP 7:26; опущено «may believe what is not true»; Мюррей использует цитату против всеобщего искупления |
| 2 | Ч. Ходж, сн. 36 | локатор верен (p. 546); `ATTRIBUTION_SHIFT` «Augustinians» → «Августин»; опущено «merely incidental» |
| 3 | Амвросий, сн. 33 | `ACCURATE` (*in Luc.* VI.25) |
| 4 | Цвингли, сн. 8 | `ACCURATE` (Z II, л. 130; формула повторяется); `CONTEXT_NOTE` (тезис 18 — «aller gleubigen») |
| 5 | Алансон 1637 | факты верны (Quick II, pp. 352–356); `TRANSLATION_ERROR` «завет» ≠ «Decree» |
| 6 | Даути, сн. 50 | HOLD (книга недоступна); `FRAMING` (мягко) |

**Вердикты S1–S5 не меняются.**

**HOLD после раунда 87:** как в §37, кроме снятого «Цвингли, с. 76» (текст подтверждён по Z II; русская страница — проверить); добавлены: Мюррей (рус. изд., с. 84); нумерация Амвросия «V.7» в бременском эпиграфе; Джабаллах (сн. 23).

## 39. Раунд 88 (2026-11-17): Кол. 1:20, сноски 102–112

Подробности — `34_` §4.171 (Q167), S186; REPASS-документ, §11.

| # | Место | Итог |
|---|---|---|
| 1 | Винсент, сн. 106 | цитата и p. 475 точны; `QUALIFIER_OMITTED_NONDISTORTING` (опущено «ultimate fate of evil men and angels… full weight») |
| 2 | Винсент, датировка «нач. XIX в.» | `DATE_ERROR` (сама статья датирует т. 3 1887 г.); годы жизни — проверить |
| 3 | Сн. 102 (Винсент, Лайтфут) | `SOURCE_BROADER_THAN_CLAIM`: «the whole universe, material and spiritual», а не «люди + ангелы»; Лайтфут — изд. 1879, pp. 159–160 (8-е изд. не прочитано) |
| 4 | «Генри», сн. 105 | пересказ точен (л. 598); `AUTHORSHIP_NOTE`: Колоссянам «Completed by Dr. W. Harris» (л. 593) |
| 5 | Вюст, Баркли (Феодорит/Эразм), Кинер, MSB, BDAG, Мелик, Гайслер | HOLD (авторское право) |

**Вердикты S1–S5 не меняются.** Раздел гипотетичен и к масштабу искупления людей прямо не относится. Закономерность §37–§38 (умолчания против лагеря Б) здесь не проявляется.

**HOLD после раунда 88:** как в §38; из кластера Кол. 1:20 сняты Винсент III, p. 475 и английский «Генри»; остаются Вюст VI, p. 188; Баркли, p. 124; Мелик, p. 225; Гайслер, p. 674; Лайтфут 8-е изд., p. 158; русский Генри, т. 6, с. 113.

## 40. Раунд 89 (2026-11-17): Шарантон и Лудён по актам

Подробности — `34_` §4.172 (Q168), S187; REPASS-документ, §12.

| # | Место | Итог |
|---|---|---|
| 1 | Лудён 1659 (с. 7) | `FACT_ERROR`: жалобы на «Daille and Amyrald», оба защищались сами (Quick II, p. 554); итог «признаны» передан верно |
| 2 | Шарантон 1644–45 | `MISCHARACTERIZATION` (мягко): «мягкое порицание» ≠ «very well satisfied… dismissed… with honour» (p. 455); мораторий для всех сторон |
| 3 | «обвинение в ереси» | `SIMPLIFIED` (мягко): язык противников (pp. 405–406), а не синодальных жалоб |
| 4 | Винсент «нач. XIX в.» | `DATE_ERROR` подкреплён каталогом IA (публикации 1863–1899) |

**Вердикты S1–S5 не меняются.** Сняты из HOLD: Шарантон/Лудён. Остаются: Джабаллах, pp. 165–199; ректорство Амиро с 1641 г.; прочее — как в §39.

## 41. Раунд 90 (2026-11-17): с. 7–8 — Гельветическая формула, 1706, Павлов, GCC

Подробности — `34_` §4.173 (Q169), S188; REPASS-документ, §13.

| # | Место | Итог |
|---|---|---|
| 1 | Канон XIII (сн. 25) | ACCURATE (перевод Клаубера) |
| 2 | «как минимум инфралапсарианский» | `IMPRECISE_QUALIFIER` (мягко): кан. IV прямо инфралапсарианский; Schaff I — Формула «within the limits of infralapsarianism» |
| 3 | Хайдеггер, «братья во Христе» | ACCURATE (Schaff I, p. 486) |
| 4 | Местреза и Троншен (сн. 26) | содержание согласуется (класс C); `CONTEXT_OMITTED` (мягко): оба — сторонники Сомюра; Klauber p. 113 — HOLD |
| 5 | 1706, Ж.-А. Турретин (сн. 27) | роль и год подтверждены (речь к Совету XXV, июнь 1706; Chandler 1748); «отменена в Швейцарии» — `SIMPLIFIED` (отменена подписка в Женеве) |
| 6 | Павлов 1906 / Одинцов 1928 | `OMITTED_RELEVANT_TEXT` (мягко): ст. V 1847 «für welche er sein Leben lassen wollte»; корпус `13_` — `OVERSTATED_REFUTATION` |
| 7 | GCC (сн. 28) | `TIME_BOUND`: в 2015 г. статьи нет; ныне (правка 06.05.2024) — «Atonement… for all those the Father has given to Him»; MSB 1997 — HOLD |
| 8 | Корпус `09_` §4 | `QUOTE_NOT_VERBATIM` (избрание); `UNSOURCED_CLAIM` (пп. 1–3) |

**Вердикты S1–S5 не меняются.** Сняты из HOLD: Хайдеггер (по Шаффу); 1706 для Женевы. Остаются: Klauber, pp. 113, 118; текст GCC на 2019 г.; MSB 1997; русские тексты Павлова; прочее — как в §40.

## 42. Раунд 91 (2026-11-17): сноски 6, 9, 16, 19, 85 — Аллен (ETS 2017) и Шафф III

Подробности — `34_` §4.174 (Q170), S189; REPASS-документ, §14.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 19 (Allen, p. 4) | ACCURATE; рядом «введена Безой» — `SIMPLIFIED` (Аллен: «no one suggested that Beza single-handedly…») |
| 2 | Сн. 9, Хесхузий | ACCURATE как передача Аллена и Рувендаля (pp. 7–8) |
| 3 | Сн. 9, «переписка» | `IMPRECISE_TERM` (трактат; LCC 22, p. 285) |
| 4 | С. 3–4, «ещё более очевидна» | `CONTEXT_OMITTED` (мягко): вывод Рувендаля «do not prove positively…»; четыре группы по Хартогу |
| 5 | Сн. 85 (Schaff III, p. 738) | ACCURATE; `SOURCE_SAYS_MORE`: Савойская декларация как второй образец, гл. XX (p. 741) |
| 6 | Сн. 6 (латынь ст. XXXI, p. 507) | ACCURATE (пометка раунда 83 снята) |
| 7 | Сн. 16 (II Helv. XI.17, p. 258) | ACCURATE (пометка раунда 83 снята) |

**Вердикты S1–S5 не меняются.** Остаются в HOLD: Lewis & Demarest II, pp. 380–381; White, p. 255; Шнукер; печать Гейдельбергского катехизиса 1563 г.; прочее — как в §41.

## 43. Раунд 92 (2026-11-17): логика и факты статьи от начала до конца; остаток непроверенных источников

Подробности — `34_` §4.175 (Q171), S190; REPASS-документ, §15 (таблица по страницам: тезис, логическая форма, состоятельность, факты).

| # | Место | Итог |
|---|---|---|
| 1 | С. 14, сн. 57 («Там же» = Green, p. 118): ἀγοράζω «по отношению к исходу» | `FACT_ERROR`, шире известного: в LXX Ральфса 24 глагольные словоформы ἀγοράζω (*испр. раунд 172:* стояло «24»; *испр. раунд 182, REPASS §105: верно 24 — пропущено 2 Езд. 20:32*), ни одна не об исходе (исход — λυτρόω, κτάομαι). Кто ошибся, Грин или статья, — HOLD |
| 2 | Сн. 12 «(4.7). Т. 4» | `LOCATOR_ERROR`: *Inst.* 4.14.7; «Т. 4» при трёхтомнике. Контекст таинств передан верно |
| 3 | Сн. 79 (Дорт II.6, Schaff III, pp. 562 и 586) | ACCURATE (латынь, л. 576; англ., л. 600) |
| 4 | С. 25: II.6 → «не была принесена за них» | `NON_SEQUITUR`: II.6 говорит о достаточности, «pro illis» нет. II.5 — `SIMPLIFIED`; «может каждый» — `AMBIGUOUS_MODAL` |
| 5 | С. 5 ↔ 26: «неограниченное искупление» | `INTERNAL_TENSION` (смена регистра «достаточность / замещение»); «преобладало до XVII в.» — `OVERGENERALIZATION`. Урсин к в. 37 (Obj. 4): «sufficiency… not… application» |
| 6 | С. 5, в. 37 | Локатор p. 319 ACCURATE; многоточие обрывает придаточное цели («redeem our body and soul») — `ELLIPSIS_CONTEXT` (мягко) |
| 7 | С. 3–4 (2.12.3) и с. 4 (4.14.7) | Цитаты точны; общая природа → замещение всех и предложение → объём — `NON_SEQUITUR` (смягчено) |
| 8 | С. 19–23 | (1)–(2) верны, но их принимает и Оуэн (`34_` §4.39); временное → вечное — `NON_SEQUITUR`; Августин (5.9.16, латынь сверена) → объём — `INFERENCE_GAP` |
| 9 | С. 14–16, 1 Ин. | «Шестнадцати» — ACCURATE (SBLGNT: 17 стихов); критерий непоследователен (новое: 4:5 «ἐκ τοῦ κόσμου»), вывод не затронут; метод «за скобки» состоятелен |
| 10 | С. 6 WCF «(1648)»; с. 24 даты Дорта | ACCURATE (Schaff I, лл. 782, 536) |
| 11 | С. 26–27, WCF | В WCF нет оговорки о достаточности (5 мест с «sufficien*», ни одно не о жертве); гармонизация с. 26 для WCF — довод от умолчания |
| 12 | Корпус: `15_` §4.1, в. 20 | `NON_SEQUITUR` на стороне корпуса: в. 20 ограничивает спасение, а не объём искупления |

**Вердикты S1–S5 не меняются.** Остаются в HOLD: Lewis & Demarest; White, p. 255; Шнукер (поиск по Диску, Gmail и Google Books — без результата); Green, p. 118; Berkhof, p. 125; описание супралапсарианства на с. 29–30 (проверено только по памяти); латынь Урсина; лист II Helv. XI.15.

## 44. Раунд 93 (2026-11-17): лапсарианские схемы (с. 29–30, сн. 93); латынь Урсина; II Helv. XI.15

Подробности — `34_` §4.176 (Q172), S191; REPASS-документ, §16.

| # | Место | Итог |
|---|---|---|
| 1 | С. 29–30: супралапсарианство избирает «невиновных… к погибели», «делает Бога причиной гибели невинных» | `SOURCE_SAYS_OPPOSITE` (частично) + `NON_SEQUITUR`. Беркхоф (источник сн. 93) называет это представление искажением: «It is sometimes represented as if…», «abhor the idea of a tyrannical God». Оговорка Беркхофа: «may be true of some» |
| 2 | С. 30, супралапсарианский столбец таблицы | Расходится с источником (мягко): у Беркхофа сотворение идёт после избрания и отвержения, осуждение — отдельный шаг после падения |
| 3 | С. 29: «не приобрела большого количества последователей» | `SOURCE_SAYS_MORE`: у Беркхофа 12 имён, включая Урсина; председатели Дорта и Вестминстера — супралапсарии |
| 4 | Сн. 93: исповедания не супралапсарианские | ACCURATE по содержанию (Беркхоф: «always adopted the infralapsarian position… always tolerated, the other view»); p. 125 не проверена |
| 5 | С. 29–30: инфралапсарианское отвержение «условное, основанное на предузнании греховности» | Смешение оставления и осуждения; внутренне несостоятельно — предвиденный грех общий для всех падших. Дорт I.15 (Schaff III, p. 555): оставление «ex liberrimo… beneplacito», осуждение «propter… peccata»; WCF III.7 |
| 6 | Урсин, латынь (1587, л. 475) | «Satisfecit pro omnibus… non quoad applica[tionem]» — формула подтверждена; дословная латынь — HOLD (OCR) |
| 7 | II Helv. XI.15 (p. 257) | «reconciliavit omnibus fidelibus» перед цитируемыми XI.16–17 — `CONTEXT_OMITTED` (мягко) |
| 8 | Корпус: `16_` §4, пп. 1 и 3 | `OVERSTATED`: кванторы «никогда» и «всегда» при оговорке Беркхофа «at least some» |

**Вердикты S1–S5 не меняются.** Остаются в HOLD: Berkhof, p. 125 по изданию статьи; Тиссен; Эриксон; дословная латынь Урсина; Lewis & Demarest; White; Шнукер; Green, p. 118.

## 45. Раунд 94 (2026-11-17): Кальвин на Гал. 5:12 по латыни; заключение статьи против основной части

Подробности — `34_` §4.177 (Q173), S192; REPASS-документ, §17.

| # | Место | Итог |
|---|---|---|
| 1 | С. 4, сн. 14: Кальвин на Гал. 5:12 | ACCURATE по латыни (*Opera* 1667, t. VII, p. 311): «omnium salus sine exceptione nobis a Deo commendatur; quemadmodum pro peccatis totius mundi passus est Christus» |
| 2 | Там же, рамка | «Respondeo, id verum esse dum homines respicimus» и «sed fit interdum…» опущены — `CONTEXT_OMITTED` (мягко); всеобщая формула остаётся |
| 3 | С. 4: «в более поздних комментариях» | `CHRONOLOGY_UNSUPPORTED` (мягко): Галатам — 1548 г., цитируемое «Наставление» — редакция 1559 г. |
| 4 | Рим. 5:18 (`01_` R05) | Подтверждено по латыни; рядом, к ст. 17: «non ad omnes homines pervenit Christi beneficium» |
| 5 | С. 36: «ключевые исповедания подчёркивают неограниченный размер заплаченной цены» | `CONCLUSION_EXCEEDS_BODY`: в основной части — только Дорт II.3; для WCF — довод от умолчания; WCF VIII.5, 8 относят покупку к данным Отцом |

**Вердикты S1–S5 не меняются.** HOLD: CO 50; с. 525 русского перевода; датировка IV.14.7.

## 46. Раунд 95 (2026-11-17): Бёттнер, *The Reformed Faith* (сн. 70) — мишень раздела «Неверный аргумент»

Подробности — `34_` §4.178 (Q174), S193; REPASS-документ, §18.

| # | Место | Итог |
|---|---|---|
| 1 | С. 19: пересказ довода «за один грех не платят дважды» | ACCURATE по существу: «punishing their sins twice, once in Christ, and then again in them… unjust»; «If we had both we would have universal salvation». «Неудачник» — слово статьи |
| 2 | С. 19: «слабая форма» (потоп, Содом) | `STRAWMAN` (мягко): у Бёттнера «twice» — это наказание в Заместителе и затем в грешнике, а не любое временное наказание |
| 3 | С. 19–20: «усиленная форма» (бесконечная ценность) | Уже у Бёттнера: «a just equivalent for all that His people would have suffered in an eternity in hell» |
| 4 | С. 20–23: ответ через вменение при обращении | Не задевает форму Бёттнера («the Holy Spirit would invariably bring them to faith and repentance») — `MISIDENTIFIED_TARGET` (р. 80) распространён на сн. 70 |
| 5 | Перекрёстно: с. 25–26, 36; с. 29–30 | Бёттнер признаёт бесконечную достаточность («amply sufficient to save all men») и пишет об оставлении «for their willing continuance in sin» |

**Вердикты S1–S5 не меняются.** HOLD: Грудем, с. 672 (легальной копии нет).

## 47. Раунд 96 (2026-11-17): «Наставление» IV.14.7 по латыни 1559 и 1536 гг.; поправка к §45, п. 3

Подробности — `34_` §4.179 (Q175), S194; REPASS-документ, §19.

| # | Место | Итог |
|---|---|---|
| 1 | С. 4, сн. 12: IV.14.7 | ACCURATE по смыслу. CO 2, col. 946–947: «Qualiter omnibus in salutem oblatus a patre ac propositus Christus, non tamen ab omnibus agnitus exceptusque est». В русском переводе «oblatus» опущено, «exceptus» передано как «узнан», сравнение превращено в самостоятельное утверждение (особенности перевода, не автора) |
| 2 | Датировка фразы | Уже в *Institutio* 1536 г. (OS I, пагинация 1536 г. [103]–[104]) |
| 3 | **Поправка к §45, п. 3** | `CHRONOLOGY_UNSUPPORTED` **снят**: комментарий на Галатам (1548) позднее текста IV.14.7 (1536). Ошибка проверяющего: сравнивались годы изданий, а не слои текста |

**Вердикты S1–S5 не меняются.** HOLD: датировка II.12.3; русский том РГГУ.

## 48. Раунд 97 (2026-11-17): «Наставление» II.12.3 (сн. 11) по латыни; слой 1559 г. по курсиву CO 2

Подробности — `34_` §4.180 (Q176), S195; REPASS-документ, §20.

| # | Место | Итог |
|---|---|---|
| 1 | С. 3–4, сн. 11: II.12.3 | ACCURATE по смыслу (CO 2, col. 342–343). В русском переводе «carnem nostram» передано как «своё тело» — особенность перевода. Перевод здесь ослабляет довод статьи: в латыни плоть прямо названа «нашей», и акцент статьи на общей природе латынь поддерживает сильнее перевода |
| 2 | Слой текста | По предисловию CO 2 курсив = добавления 1559 г. Вторая часть цитаты («carnem quam a nobis accepit, obtulisse in sacrificium») — вероятно 1559 г. (признак курсива по OCR; визуально не проверено) |
| 3 | С. 4: «в более поздних комментариях» | `CHRONOLOGY_PARTIAL` (мягко, PROBABLE): верно для сн. 12 (1536 г.), вероятно неверно для ключевой фразы сн. 11 (1559 г. позже 1548 г.) |

**Вердикты S1–S5 не меняются.** HOLD: визуальная проверка курсива; текст 1539–1554 гг.

## 49. Раунд 98 (2026-11-17): II.12.3 (сн. 11) по CO 1; слой ключевой фразы — 1559 г. (установлено)

Подробности — `34_` §4.181 (Q177), S196; REPASS-документ, §21.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 11, первая часть | Слой 1539 г. по существу (CO 1, col. 518, §10: «ut carnem nostram in satisfactionem iusto Dei iudicio statueret ac sisteret»), формулировки переписаны в 1559 г.; русский перевод идёт по 1559 г. |
| 2 | Сн. 11, вторая часть («плоть, которую принял от нас») | **1559 г. — SUPPORTED**: в тексте 1539–1554 гг. (слои 1539, 1543, 1550–1554) её нет; за §10 сразу идёт §11 о манихеях |
| 3 | С. 4: «в более поздних комментариях» | `CHRONOLOGY_PARTIAL` повышен с PROBABLE до SUPPORTED (мягкий по весу): верно для сн. 12, обратно для ключевой фразы сн. 11 |
| 4 | Метод | Правило «курсив CO 2 = 1559 г.» подтверждено предисловием (CO 1, л. 54) и сличением: искажённые как курсив места CO 2 совпали с формулировками, которых нет в CO 1 |

**Вердикты S1–S5 не меняются.** Снято из HOLD: CO 1. HOLD: русский том РГГУ.

## 50. Раунд 99 (2026-11-17): печатные страницы Беркхофа — сн. 93 и сн. 46–48

Подробности — `34_` §4.182 (Q178), S197; REPASS-документ, §22.

| # | Место | Итог |
|---|---|---|
| 1 | С. 29, сн. 93 (Berkhof, p. 125) | ACCURATE; **локатор EXACT**. На p. 125: «Our confessional standards embody the infralapsarian position, but do not condemn Supralapsarianism. It was felt that this view was not necessarily inconsistent with Reformed theology» + выводы Утрехта 1908 г. |
| 2 | То же — объём | `CONTEXT_OMITTED` (мягко): оговорка о терпимости стоит на той же странице и в статье не приведена. Прямого противоречия нет: статья сама относит все три схемы к кальвинизму (с. 30) |
| 3 | Сн. 46–48 (с. 11–12) | Локаторы pp. 393, 398–399, 399 — EXACT; они же служат калибровкой пагинации. Пропущенный п. 2 («dubious and very unsatisfactory») — p. 394, внутри цитируемого диапазона |
| 4 | §16 / аудит §44 | Листы скана переведены в печатные страницы: pp. 118, 119, 122, 123, 124. Вердикты не меняются |

**Вердикты S1–S5 не меняются.** Снято из HOLD: Berkhof, p. 125; страницы сн. 46–48. HOLD: Lewis & Demarest (IA, доступ ограничен); Тиссен; Эриксон.

## 51. Раунд 100 (2026-11-17): Эриксон (сн. 95–97) по 3-му изд.; происхождение рамки сн. 13

Подробности — `34_` §4.183 (Q179), S198; REPASS-документ, §23.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 96–97 | ACCURATE: четыре шага; «Sublapsarianism (unlimited atonement with a limited application)» (Erickson 3rd ed., гл. 43). Русская с. 779 — HOLD |
| 2 | Сн. 95: «в последнее время… более чёткое разграничение» | `SIMPLIFIED` (мягко): источник Эриксона для сублапсарианской схемы — Strong 1907, pp. 778–79 (прим. 1600) |
| 3 | С. 30, таблица (супра-столбец) | Расходится также с Эриксоном (мягко): решение о спасении и осуждении у него первое, до сотворения |
| 4 | Генеалогия таблицы | Эриксон: супра/инфра — Warfield, *Plan of Salvation*, p. 31 (прим. 1599); «sub» — Strong (прим. 1600). Звено Strong → Erickson — A2 (было C) |
| 5 | Сн. 13: «в более поздних комментариях» | Рамка «Institutes — ранняя работа, Commentaries — поздние» прослежена: Richards → Strong 1907, p. 777 (A1) → Erickson, прим. 1398 (A2). Путь к статье не утверждается (сн. 13 — Lewis & Demarest, HOLD). Для текста 1559 г. рамка анахронична (§20–§21) |

**Вердикты S1–S5 не меняются.** HOLD: Эриксон, рус. с. 779; Тиссен; Lewis & Demarest.

## 52. Раунд 101 (2026-11-17): Стюарт, *SBET* 2008 (сн. 80, 86–92)

Подробности — `34_` §4.184 (Q180), S199; REPASS-документ, §24.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 86, 87, 88 | ACCURATE, страницы EXACT (pp. 189, 196 прим. 35, 189) |
| 2 | «Авторы XVII–XIX веков» | `SCOPE_EXCEEDED` (мягко): обзор Стюарта начинается с 1707 г. |
| 3 | Сн. 89: Топлади — «единственный… до XX века» | Страницы EXACT (p. 194; прим. 41, p. 198); `OVERGENERALIZATION` (мягко): у Стюарта — XVIII–XIX века и рассмотренная литература. По существу опровергнуто в корпусе (`34_` §4.5, П7) |
| 4 | Сн. 90: «большинство… богословов XVII–XIX веков» | `OVERGENERALIZATION` (мягко): у Стюарта «writers surveyed here», выборка |
| 5 | Сн. 91: «см. p. 196» | Содержание ACCURATE; `LOCATOR_ERROR` (вероятно): таблица на pp. 201–203 |
| 6 | Сн. 92 | Страница EXACT (p. 199); `TRANSLATION_SHIFT` (мягко): «There is no pretending here» — о Сперджене, а не общий тезис; `CONTEXT_OMITTED` (мягко): у Стюарта «universal benefits in that particular redemption» (p. 198) |
| 7 | С. 28: «надо полагать… акцент на результате» | Не согласуется с причиной, которую называет сам Стюарт («adequacy and capaciousness»); догадка помечена в статье как догадка |
| 8 | CO 1, «accepit», части 1–2 | «a nobis accepit» нет; вывод раунда 98 подтверждён |

**Вердикты S1–S5 не меняются.** Снято из HOLD: Стюарт. HOLD: Lewis & Demarest; MacArthur & Mayhue, p. 544; Green, p. 118; White; Шнукер; Грудем.

## 53. Раунд 102 (2026-11-17): Лютер, сн. 5, по WA 40/I

Подробности — `34_` §4.185 (Q181), S200; REPASS-документ, §25.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 5: «несет грехи всех людей в Своем теле» | ACCURATE, дословно: WA 40/I, 433 «qui habet et portat omnia omnium peccata in corpore suo» |
| 2 | Сн. 5: «понес грехи всего мира» | ACCURATE: WA 40/I, 443 «gestaret in nostra larva peccatum totius mundi» |
| 3 | Сн. 5: «от первого человека и до последнего дня… на плечах одного, родившегося от Марии» | По смыслу подтверждено (439: «praeterita, praesentia et futura»; 442: «in humeros suos»); словесная форма не найдена — `WORDING_NOT_LOCATED` (мягко) |
| 4 | Локатор *LW* 26, pp. 285, 277 | `PLAUSIBLE` (*LW* недоступен; WA 433 ≈ *LW* 26:277) |
| 5 | Контекст (444: «Quatenus igitur hoc credis, eatenus habes») | Совпадает со схемой статьи «обеспечение — всем, применение — по вере»; `CONTEXT_OMITTED` не ставится |
| 6 | Green, сн. 56–57 | IA: только экземпляры с ограниченным доступом — HOLD |

**Вердикты S1–S5 не меняются.** HOLD: *LW* 26 (страницы); Green; Lewis & Demarest; MacArthur & Mayhue; White; Шнукер; Грудем.

## 54. Раунд 103 (2026-11-17): Кол. 1:20 — Златоуст (сн. 103), Феодорит и Эразм (сн. 104)

Подробности — `34_` §4.186 (Q182), S201; REPASS-документ, §26.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 103: цитата Златоуста | ACCURATE: NPNF¹ 13, p. 272, «the Angels were become enemies to men, through seeing the Lord insulted»; локатор EXACT |
| 2 | Сн. 103: выходные данные | Точно: перевод J. Ashworth (p. 176), ред. J. A. Broadus (p. 173) |
| 3 | Сн. 104: Феодорит | Подтверждено по PG 82, ad Col. 1:20 (IA л. 323): «συνῆψε τοῖς ἐπιγείοις τὰ ἐπουράνια· ἀπεστρέφοντο γὰρ ἡμᾶς καὶ τῶν ἀγγέλων οἱ δῆμοι»; колонка PG не прочитана |
| 4 | Сн. 104: Эразм | NOT_LOCATED (OCR *Paraphrasis*, 1540); HOLD |
| 4a | *Уточнение раунда 108 (§59)* | Найден: *Paraphrases* (Basel, 1521), IA `ARes14515` — «omnia sibi reconciliaret» и мир небесных с земными; у статьи — `OVERSTATEMENT` (мягко) |
| 5 | С. 34–35: логика раздела | Златоуст («Was war and battle there also?») и Феодорит толкуют примирение «небесного» как мир ангелов с людьми; вывод статьи — «творение примирилось с Богом» (по Мелику). Разные толкования поданы как иллюстрация одного тезиса — `INTERNAL_TENSION` (мягко) |

**Вердикты S1–S5 не меняются.** HOLD (§11): Вюст; Баркли; Эразм; Кинер; MSB; BDAG; Мелик; Гайслер; Лайтфут 8-е изд.; Генри рус. с. 113.

## 55. Раунд 104 (2026-11-17): хвосты Кол. 1:20 — Лайтфут, Винсент, «Генри»

Подробности — `34_` §4.187 (Q183), S202; REPASS-документ, §27.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 102: Лайтфут, p. 158 | EXACT по оттиску Macmillan 1890 г. (`ed9saintpaulsepis00ligh`): ст. 20 — pp. 157–158; τὰ πάντα — p. 158, «material as well as spiritual» |
| 2 | Сн. 102: «8th ed., 1886» | Точно по счёту оттисков: 1886 — восьмой оттиск (Reprinted) 3-го изд. марта 1879 г.; та же печатная форма, что 1890 г. |
| 3 | §11, страницы перепечатки «1880» | Расходятся на 1–2 страницы с оттиском 1890 г. — HISTORICAL |
| 4 | С. 34: Винсент «нач. XIX в.» | `DATE_ERROR` подтверждён: 1834–1922 (каталожная запись Cornell) |
| 5 | Сн. 105: «Генри» на Кол. 1:20 | Предисловие продолжателей: работа по стенограммам устных толкований Генри — `AUTHORSHIP_NOTE` смягчён |

**Вердикты S1–S5 не меняются.** HOLD (§11): Вюст; Баркли; Эразм; Кинер; MSB; BDAG; Мелик; Гайслер; Генри рус. с. 113; колонки PG 82 и PG 62.

## 56. Раунд 105 (2026-11-17): «MTP 7, p. 26» (сн. 45) и немецкий текст в. 37 1563 г. (сн. 15)

Подробности — `34_` §4.188 (Q184), S203; REPASS-документ, §28.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 45: «MTP 7, p. 26» | Вторая страница № 351 *Plenteous Redemption* (MTP 7, pp. 25–32; указатель archive.spurgeon.org, Passmore 1862). Цитаты нет — `LOCATOR_ERROR` подтверждён положительно |
| 2 | Содержание MTP 7:25–26 | Начало раздела I: «I cannot for one moment give any credence whatever to that doctrine which tells us that all men are redeemed». Граница страниц оценена по объёму текста, по скану не сверена |
| 3 | Происхождение ошибки | У Мюррея (англ., прим. 17) — «Sermons, Volume 58, pages 583–4»; «7, 26» в открытом отрывке гл. 3 нет. Механизм не установлен; рус. с. 84 — HOLD |
| 4 | Сн. 15: немецкий в. 37 | Текст 1563 г. по Lang 1907 (л. 137) и Müller 1903 (л. 770): «wider die sünde des gantzen menschlichen geschlechts» — ACCURATE; HOLD REPASS §14 снят |
| 5 | С. 5: «включённый Дортским синодом» | `PLAUSIBLE`; акт Дорта не открыт |
| 5a | *Уточнение раунда 106 (§57)* | ACCURATE по *Acta* 1620, сессия CXLVIII |

**Вердикты S1–S5 не меняются.** HOLD: Цвингли, рус. с. 76; Дэниел, pp. 360–363; Мюррей, рус. с. 84; Даути; Льюис и Демарест; Грудем; White; Шнукер.

## 57. Раунд 106 (2026-11-17): Дорт и Гейдельбергский катехизис (с. 5) по актам 1620 г.

Подробности — `34_` §4.189 (Q185), S204; REPASS-документ, §29.

| # | Место | Итог |
|---|---|---|
| 1 | С. 5: «позднее включённый Дортским синодом» | ACCURATE: *Acta* 1620 (`actasynodination00syno`), л. 364 ≈ p. 318, сессия CXLVIII — «consentientibus omnium tam Exterorum, quam Belgicorum Theologorum suffragiis… Verbo Dei in omnibus esse consentientem… omnino retineri debere» |
| 2 | Дата | Накануне 2 мая 1619 г., после полудня (по всей вероятности 1 мая) |
| 2a | *Уточнение раунда 109 (§60)* | **1 мая 1619 г. (среда), после полудня**: *Acta*, p. 317 — сессия CXLVII «Calendis Maij, Die Mercurij ante meridiem»; p. 318 — CXLVIII «Eodem Die post meridiem» |
| 3 | Слово «включённый» | Катехизис уже был формулой единства («hactenus hic usitatam», л. 12) и синодом подтверждён — `IMPRECISE_TERM` (минимально) |
| 4 | Логика | Синод, принявший II.8, признал в. 37 согласным со Словом «in omnibus»; значит, в. 37 не различает позиции спора — `EVIDENCE_UNDERDETERMINES` (мягко); внутреннего противоречия в статье нет |

**Вердикты S1–S5 не меняются.**

## 58. Раунд 107 (2026-11-17): Томас Скотт (сн. 80) по первоисточникам

Подробности — `34_` §4.190 (Q186), S205; REPASS-документ, §30.

| # | Место | Итог |
|---|---|---|
| 1 | С. 26: Скотт «верил в общее искупление… признавал более узкий взгляд» | ACCURATE — Стюарт и *Remarks* II (1817), л. 115: «General redemption is also clearly declared» |
| 2 | «в 1804 г. опубликовал их перевод» | `DATE_ERROR` подтверждён по первоисточникам: 1804 — оксфордская *Sylloge Confessionum*; перевод — 1817 (*Remarks*, 2-е изд.), отдельно 1818 (титул; *Life*, л. 484) |
| 3 | «продвигал богословие Дортских канонов» | `CHRONOLOGY_PARTIAL` (мягко): в 1811 г. Скотт сам принял сокращение Тиленуса–Хейлина за подлинные каноны |
| 4 | Логика | «General redemption» Скотта = всеобщая достаточность при ограниченной действенности; поддерживает с. 25–26, но не с. 36 — `EVIDENCE_UNDERDETERMINES` (мягко) |

**Вердикты S1–S5 не меняются.**

## 59. Раунд 108 (2026-11-17): Стюарт (сн. 80, 92), Скотт 1817, Эразм (сн. 104)

Подробности — `34_` §4.191 (Q187), S206; REPASS-документ, §31.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 80, «P. 193–194» | EXACT: «General Redemption… narrower view» — конец p. 193; сноска 23 и *Sylloge* 1804 — p. 194 |
| 2 | Сн. 92, «P. 199» | Локатор EXACT; `TRANSLATION_SHIFT` и `CONTEXT_OMITTED` (§24) остаются |
| 3 | Перевод Скотта | Впервые — *Remarks*, 2-е изд. (London, 1817), p. 725 (IA `a608278200scotuoft`, л. 749); «ibid. p. 725» у Стюарта — EXACT |
| 4 | Стюарт, прим. 22–24 | `EDITION_MISLABEL` (мягко, у Стюарта): «London: 1811», а страницы — по 2-му изд. 1817 г. |
| 5 | Сн. 104: Эразм «не с Богом, а с людьми» | `OVERSTATEMENT` (мягко): в *Paraphrases* (1521) — «omnia sibi reconciliaret» и «concordiam et pacem coelestium ac terrestrium»; NOT_LOCATED §54 снят |

**Вердикты S1–S5 не меняются.** HOLD: *Annotationes* Эразма; *Remarks* 1811.

> *Уточнено (раунд 110, 2026-11-17; §61):* *Annotationes* (1535) и т. I *Remarks* (1811) прочитаны; остаётся т. II 1811 г.

## 60. Раунд 109 (2026-11-17): дата сессии CXLVIII; корпусные формулы о Скотте и лапсарианской терминологии

Подробности — `34_` §4.192 (Q188), S207; REPASS-документ, §32.

| # | Место | Итог |
|---|---|---|
| 1 | Дата одобрения катехизиса (§57) | 1 мая 1619 г. (среда), после полудня — *Acta*, p. 317–318; ср. Schaff, *Creeds* I, л. 573 |
| 2 | `16_` §1: «употребляет «сублапсарианство» как синоним инфралапсарианства» | `CORPUS_MISREAD` (мягко): статья различает три схемы; о прежней синонимии сообщает в сн. 95 |
| 3 | `11_`, `06_` §40, `01_` §4.31: «Reply 1811, с. 725» | Наследуют `EDITION_MISLABEL` Стюарта; p. 725 — 2-е изд. 1817 г. Примечания внесены |
| 4 | `12_` `T-10` (`EDITION_HOLD`) | Снят |
| 5 | Лапсарианский раздел (с. 29–30) | Повторная сверка по Дорту I.15 подтверждает §16 и §22; новых вердиктов нет |

**Вердикты S1–S5 не меняются.**

## 61. Раунд 110 (2026-11-17): Скотт 1811/1817; локаторы Стюарта; *Annotationes* Эразма

Подробности — `34_` §4.193 (Q189), S208; REPASS-документ, §33.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 80, «продвигал» | `CHRONOLOGY_PARTIAL` подтверждён: *Remarks* (1811), предисловие, p. xiii — «Much less are we answerable for the Lambeth articles, or those of the Synod of Dort» |
| 2 | Мотив перевода (1817, p. 747) | Исправить своё «false witness against this Synod» и «check Antinomian Calvinism»; отдельное издание с отвержением заблуждений обещано — прим. 24 Стюарта («enlarged edition 1818») EXACT |
| 3 | Стюарт, прим. 22–23 | «xiv» = p. xiv изд. 1817 г. («sweep away at once the labours of his whole life»); заголовки и страницы прим. 23 — по 1817 г.; `EDITION_MISLABEL` (мягко, у Стюарта) подтверждён |
| 4 | Сн. 104, Эразм, *Annotationes* (1535), p. 635 | Толкования «ангелы с людьми» нет; εἰς αὐτόν — «erga se» (к Себе). `OVERSTATEMENT` подтверждён обоими текстами Эразма |

**Вердикты S1–S5 не меняются.**

## 62. Раунд 111 (2026-11-17): сн. 78 — Каннингем; сн. 76 — Коллинз

Подробности — `34_` §4.194 (Q190), S209; REPASS-документ, §34.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 78, «под руководством Арминия и Гомара» | Каннингем (1863), p. 373: Гомар — «a learned and zealous defender of Calvinism», Арминий умер в 1609 г., Ремонстрацию 1610 г. подали «the followers of Arminius»; p. 435: «Gomarus, the colleague and opponent of Arminius». Источник статьи опровергает связку — `SOURCE_CONTRADICTS_CLAIM`; `FACT_ERROR` (V5) усилен |
| 2 | Сн. 78, локатор pp. 379–380 | По пагинации 1863 г. — начало раздела «Synod of Dort», общая оценка синода, без дат и имён. `LOCATOR_IMPRECISE` (мягко); при иной пагинации изд. 1882 г. — HOLD |
| 3 | Сн. 76, Коллинз | Цитата и этимология «at onement» — EXACT. Но значение 2a той же статьи — «reconciliation of humankind with God», а *redemption* — «a buying back» и «atonement for guilt». Пара «atonement = цена, redemption = результат» источником не поддержана — `SELECTIVE_CITATION` (мягко) |

**Вердикты S1–S5 не меняются.**

## 63. Раунд 112 (2026-11-17): сноски ↔ библиография; электронные издания

Подробности — `34_` §4.195 (Q191), S210; REPASS-документ, §35.

| # | Место | Итог |
|---|---|---|
| 1 | Аппарат статьи | 112 сносок; все 69 позиций библиографии (61 печатная + 8 электронных) процитированы; не внесены в библиографию: сн. 11 (Calvin, *Sermons on the Saving Work of Christ*, 2011), сн. 76 (Коллинз), сн. 1 (URL) — `BIBLIOGRAPHY_INCOMPLETE` (мягко) |
| 2 | Бокэм 1998, Смолли 1989, Вюст 1997 (вероятно TWOT 1999, Кинер, Робертсон) | Выходные данные электронных изданий Logos (печатные WBC 50/51 — 1983/1984) — `ELECTRONIC_EDITION_UNMARKED` (мягко); не `DATE_ERROR`. Лайтфут «8th ed., 1886» — реальная перепечатка; из Logos только название серии |
| 3 | Сн. 75 ↔ 76 | *expiation*: «удаление вины» и «компенсация» — `INTERNAL_INCONSISTENCY` (мягко) |
| 4 | Пробел «сн. 114–120» | Артефакт поиска: таких сносок нет |

**Вердикты S1–S5 не меняются.**

## 64. Раунд 113 (2026-11-17): карта покрытия; сн. 20

Подробности — `34_` §4.196 (Q192), S211; REPASS-документ, §36.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 1–112 | Без упоминаний в корпусе оставались 20, 29, 38, 63, 100; теперь у каждой есть статус (сн. 63 и 100 — HOLD) |
| 2 | Сн. 20 | «Почти дословно» — верно для 90 из 160 параграфов (≥ 0.80; совпадающих слов ≥ 69.6 %). «Кроме баптистских особенностей» — `SIMPLIFIED` (мягко): изменены III.3 («left to act in their sin to their just condemnation» вместо «fore-ordained to everlasting death»), VIII.8 («without any condition foreseen in them»), VIII.9–10, XVII.1; гл. XV и XX — из Савойской декларации. Скан 1688 г. (перепечатка, IA), лл. 13, 19, 21, 50 |

**Вердикты S1–S5 не меняются.**

## 65. Раунд 114 (2026-11-17): WCF по печатному скану

Подробности — `34_` §4.197 (Q193), S212; REPASS-документ, §37.

| # | Место | Итог |
|---|---|---|
| 1 | WCF III.3, II.3, VIII.1, VIII.5, VIII.8, конец гл. VIII | Сверены по скану изд. 1946 г. (Google Drive, pp. 6, 9, 10). «Foreordained to everlasting death»; «purchased, not only reconciliation»; «purchased redemption» без оговорки о благодати; гл. VIII кончается §8 |
| 2 | `12_` T-13, REPASS §36 | Расхождения теперь подтверждены сканами обеих сторон (вторая — перепечатка изд. 1688 г., лл. 13, 19, 20, 21). Вердикты прежние |
| 3 | Google Drive | Книг из списка HOLD нет |

**Вердикты S1–S5 не меняются.**

## 66. Раунд 115 (2026-11-17): счёт слов WCF по печатному скану

Подробности — `34_` §4.198 (Q194), S213; REPASS-документ, §38.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 82 / V1 | По OCR скана изд. 1946 г. с визуальной проверкой: *redemption* 5, *redeemed* 3, *atone-* 0, *propitiation* 1 (XXIX.2 «for all the sins of His elect»), *purchased* 4, *satisf-* 7, *reconcil-* 2 — **совпадает с S32**; V1 как арифметика — ACCURATE |
| 2 | S32, *sacrifice* | 5 в ед. ч.; с VII.5 «sacrifices» — 6 (уточнение, на вывод не влияет) |

**Вердикты S1–S5 не меняются.**

## 67. Раунд 116 (2026-11-17): Ж.-А. Турретин — «преемник на богословской кафедре» (сн. 27)

Подробности — `34_` §4.199 (Q195), S214; REPASS-документ, §39.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8, сн. 27: «его преемник на богословской кафедре» | `FACT_ERROR` (мягко). По Боржо (1900): кафедру Франсуа Турретина в 1686 г. принял Б. Пикте (л. 560, 749); Ж.-А. Турретин — профессор церковной истории с 1697 г., с 1705 г. — на кафедре догматики после Луи Троншена (л. 627). HOLD раунда 90 снят |
| 2 | Ректорство в 1706 г. (Чандлер) | Подтверждено: ректор до 1711 г. (л. 582) |
| 3 | Обещание «не учить вопреки Формуле» (оппонент Чандлера) | `SOURCES_CONFLICT`: DeYoung/Клаубер (класс C) — компромисс не принят; протоколы Совета 1706 г. — HOLD |
| 4 | Корпус `27_` §4.4: «в сторону теологического деизма» | `OVERSTATEMENT` (мягко): Боржо подтверждает рационалистический поворот, но с сохранением «foi» и «révélation» |

**Вердикты S1–S5 не меняются.**

## 68. Раунд 117 (2026-11-17): Женева, 1706 — текст формуляра (Боржо)

Подробности — `34_` §4.200 (Q196), S215; REPASS-документ, §40.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8, сн. 27: «отменена в 1706 г.» | `SIMPLIFIED` (без изменений), теперь с актами. В Женеве Компания (27.08.1706) и Совет (20.09.1706) отменили подпись под Формулой. П. 3 нового формуляра — увещание не учить против Дорта и «règlements… des Églises de Suisse», ответ «Je le promets». Всякий формуляр отменён 01.06.1725 |
| 2 | Конфликт §67 п. 3 | `RESOLVED_PARTIAL`: обещание было, но без названия Формулы; дата Совета — `DATE_DISCREPANCY` (Боржо 20.09 ↔ DeYoung 06.09) |
| 3 | «Преемник на кафедре» (§67 п. 1) | Усилено: у Боржо — «le jeune successeur de Louis Tronchin» (л. 630, с. 538) |

**Вердикты S1–S5 не меняются.**

## 69. Раунд 118 (2026-11-17): сн. 26 — Местреза и Троншен (Боржо)

Подробности — `34_` §4.201 (Q197), S216; REPASS-документ, §41.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8, сн. 26: возражение Местреза и Троншена | Согласуется (класс B): оба противились обязательному отвержению сомюрских мнений с 1669 г. (л. 417–418). Формулировка о Кальвине/Безе/II Гельв. — класс C; Klauber p. 113 — HOLD |
| 2 | `CONTEXT_OMITTED` (мягко) | Прежний; для Троншена — класс B: «disciple» Камерона, «ami» Каппеля (л. 415–416). Для Местреза «амиральдист» — по-прежнему класс C |
| 3 | `06_` §15, идентификация | Подтверждена: Филипп Местреза (1618–1690), Луи Троншен I (1629–1705) — л. 748–749 |

**Вердикты S1–S5 не меняются.**

## 70. Раунд 119 (2026-11-17): сн. 27, 1706 — Чандлер (л. 181–182) и J. Clarke 1749

Подробности — `34_` §4.202 (Q198), S217; REPASS-документ, §42.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8, сн. 27: «отменена в 1706 г.» | `SIMPLIFIED` прежний, опора расширена. Послесловие Чандлера (л. 182), сторонника отмены: после 1706 г. требовалось обещание не учить «contrary to the Consensus Helveticus… pour le Bien de la Paix» |
| 2 | «Оппонент Чандлера» (§67, п. 3; §68, п. 2) | Это J. Clarke, 1749 (каталог IA). Его фраза пересказывает Чандлера (л. 182) и **не является независимым свидетельством**. `RESOLVED_PARTIAL` прежний: в тексте акта (Боржо) Формула не названа, у Чандлера — названа (`PARAPHRASE_NOT_ACT`) |
| 3 | Дата речи | «Tuesday, the 2[?]th of June, 1706»: 22 или 29 (григ.) либо 25 (юл.) — не установлено. Речь — от имени Компании, до решения Советов (л. 181) |

**Вердикты S1–S5 не меняются.**

## 71. Раунд 120 (2026-11-17): сн. 27, 1706 — решение Компании 25.06.1706 (Бюде 1880)

Подробности — `34_` §4.203 (Q199), S218; REPASS-документ, §43.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8, сн. 27: «отменена в 1706 г.» | `SIMPLIFIED` прежний. Решение Компании 25.06.1706 принято «sans toucher à la doctrine contenue dans les règlements de 1649»: отменена подпись, сохранено увещание «à ne rien enseigner contre les règlements» (л. 139) |
| 2 | Дата речи Турретина (§70, п. 3) | Скорее всего, 29.06.1706 (`DATE_INFERRED`): заседание 25.06 (пятница), делегаты выступили позже, а вторник после 25-го — только 29-е (григ.) |
| 3 | «Преемник» (§67, п. 1) | Бюде, л. 80: «en remplacement de Louis Tronchin», 29.09.1705 — подтверждено независимо |
| 4 | `27_`: Цюрих | Регистр 1706 г.: «on ne signe point à Zurich» ↔ Schaff-Herzog (до 1725–1740) — `SOURCE_TENSION` | *(Раунд 121, §72: Schaff-Herzog V, p. 218 — «Zurich and Bern retained it»; дат 1725–1740 там нет.)*

**Вердикты S1–S5 не меняются.**

## 72. Раунд 121 (2026-11-17): «не продержалась долго даже в Швейцарии» — Шафф и *New Schaff-Herzog*

Подробности — `34_` §4.204 (Q200), S219; REPASS-документ, §44.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8, сн. 26–27: «не продержалась долго даже в Швейцарии» | По смыслу совпадает с Schaff, *Creeds* I, p. 486 («about half a century») и *New Schaff-Herzog* V, p. 218 («could not long hold its position»). Заимствование не утверждается |
| 2 | «…и была отменена в 1706 г.» | `SIMPLIFIED` прежний: 1706 — Женева, «Zurich and Bern retained it», «never formally abolished» (SH V, p. 218) |
| 3 | `27_`: «к 1725–1740 гг.… (Schaff-Herzog V:218)» | На p. 218 дат нет — `LOCATOR_DOES_NOT_SUPPORT_DATES` (поправка к корпусу, мягко) |
| 4 | Цюрих (§71, п. 4) | `SOURCE_TENSION` прежний: регистр Компании 1706 г. ↔ SH «Zurich and Bern retained it» |

**Вердикты S1–S5 не меняются.**

## 73. Раунд 122 (2026-11-17): локатор `27_` «Schaff I:478 fn. 914»; триумвират (Бюде)

Подробности — `34_` §4.205 (Q201), S220; REPASS-документ, §45.

| # | Место | Итог |
|---|---|---|
| 1 | `27_`, п. 3 пометки Волны 18: Турретин, Веренфельс, Остервальд «тяготевшие к арминианству… и раннему Просвещению» (Schaff I:478) | На p. 478 — только Ж.-А. Турретин: «inclined to Arminianism, and advocated toleration». `LOCATOR_OVEREXTENDED` (поправка к корпусу, мягко) |
| 2 | Связь трёх лиц | Бюде, л. 75: «le triumvirat» (класс B). Л. 152: Веренфельс считал отмену формуляра «dangereuse» (контекст 1719–1725 гг.) | *(Раунд 124, §75: л. 152 перепроверен дословно; год для л. 152 у Бюде не указан, ближайшая дата — 23.03.1721.)*
| 3 | `27_`, п. 1 (Гернлер, p. 478) | Подтверждено |
| 4 | Сн. 27, «преемник» | Шафф: «Professor of Church History» — `FACT_ERROR` (мягко) прежний |

**Вердикты S1–S5 не меняются.**

## 74. Раунд 123 (2026-11-17): Шафф, pp. 486–489 — предисловие, кан. XIII/XVI, инфралапсарианство

Подробности — `34_` §4.206 (Q202), S221; REPASS-документ, §46.

| # | Место | Итог |
|---|---|---|
| 1 | С. 7–8: «как минимум инфралапсарианский» | Шафф, p. 487: «This is clearly the Augustinian infralapsarianism». Главная мысль подкреплена; `IMPRECISE_QUALIFIER` (мягко) прежний |
| 2 | С. 7, сн. 25: кан. XIII | Перевод согласуется с латынью Шаффа (p. 488): «pro solis electis… solos illos… solos». ACCURATE |
| 3 | `27_`: «487 fn. 932» / «488 fn. 936» / «pp. 487–489» | Сноска к предисловию начинается на p. 486 (`LOCATOR_IMPRECISE`, мелко); остальное подтверждено |
| 4 | Контекст | Шафф, p. 488: «The infinite value and inherent sufficiency of Christ's satisfaction is not denied, but the divine intention and the practical efficiency are limited» |

**Вердикты S1–S5 не меняются.**

## 75. Раунд 124 (2026-11-17): Бюде, л. 146–152 — Веренфельс, письмо Уэйка, Давенант

Подробности — `34_` §4.207 (Q203), S222; REPASS-документ, §47.

| # | Место | Итог |
|---|---|---|
| 1 | §73 / §4.205: Веренфельс, «l'abrogation du formulaire lui paraît dangereuse» (л. 152) | Подтверждено дословно. Это пересказ Бюде («il semble plutôt qu'il soit opportuniste»); в кавычках от Веренфельса только совет «d'irriter les Confédérés» не надо. Вывод раунда 122 прежний |
| 2 | «Контекст 1719–1725 гг.» | Года у л. 152 нет; ближайшая дата — письмо Уэйка 23.03.1721 (л. 150–151). Диапазон — вывод (`DATE_INFERRED`) |
| 3 | `27_`, п. 3: письма королей «в 1722–1723 гг.» | Бюде: 23 марта 1721 г. письмо короля Англии «en chemin pour Berne». Вероятно, старый стиль (год с 25 марта) = апрель 1722 г. н. ст.; согласуется с Schaff-Herzog V:218 (`DATE_STYLE_PROBABLE`) |
| 4 | Контекст | По Бюде, Турретин прислал Уэйку план королевского письма. Турретин со ссылкой на Давенанта пишет, что Формулу не подписали бы «presque tous nos réformateurs» (полемическое мнение, не факт) |

**Вердикты S1–S5 не меняются.**

## 76. Раунд 125 (2026-11-17): МакАртур по GTY 1990/2004/2008; формула IFCA

Подробности — `34_` §4.208 (Q204), S223; REPASS-документ, §48.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8: «собственная убеждённость в ограниченном искуплении» | Верно для 2004 г. и позже. 01.04.1990 (GTY 70-11) МакАртур говорил о «a strong case for a general atonement» и отказывался от ярлыка «limited atonement or particular redemption». Позиция менялась; статья (2019, MSB 1997) не ошибается |
| 2 | Сн. 58: MSB к 2 Пет. 2:1 | 20.01.2008 (GTY 70-26) МакАртур зачитывает заметку: «more analogical than theological, speaking of a human master over a household». Перевод ACCURATE; с. 1955 — HOLD |
| 3 | Корпус: §8 строка 3 / `34_` §4.168 «позже стало иным» | `CORPUS_OVERSTATEMENT` (мягко): в 2008 г. аналогическое чтение снова «the best response» |
| 4 | IFCA Art. IV, 1.3.b | «died on the cross for all mankind as a representative, vicarious, substitutionary sacrifice» — подтверждено (класс B) |

**Вердикты S1–S5 не меняются.**

## 77. Раунд 126 (2026-11-17): вероучение GCC на 2019 г. (сн. 28); дата статьи «Atonement»

Подробности — `34_` §4.209 (Q205), S224; REPASS-документ, §49.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8, сн. 28: вероучение GCC не выносит вопрос об объёме в исповедуемые принципы | Wayback 02.11.2019 (`id_`): статьи об объёме нет; «accomplished our redemption». **ACCURATE для 2019 г.**; HOLD снят |
| 2 | `TIME_BOUND` | Статья «Atonement» («for all those the Father has given to Him») появилась между 02.05.2024 и 01.06.2024 |
| 3 | `09_` §4, цитата об избрании | `QUOTE_NOT_VERBATIM` прежний: не совпадает ни с одной редакцией 2015–2024 гг. |

**Вердикты S1–S5 не меняются.**

## 78. Раунд 127 (2026-11-17): Одинцов 1928 по-русски (с. 8)

Подробности — `34_` §4.210 (Q206), S225; REPASS-документ, §50.

| # | Место | Итог |
|---|---|---|
| 1 | С. 8: исповедание «не формулирует четкой позиции» по объёму | Русский текст 1928 г. (две перепечатки, класс C), ст. V: «как овцы Его стада, за которых Он положит Свою жизнь (Ин. 10:15-16, 26-27)». «За всех» нет, исключительной формулы тоже нет. `OMITTED_RELEVANT_TEXT` (мягко) — как для немецкого текста 1847 г. |
| 2 | `13_` §II.2, Член IV | «страдательно… душу и Своё тело» в текстах 1928 г. нет («тело и Свою душу»): `QUOTE_NOT_VERBATIM` (мягко); пометки «[1906: …]» — `UNVERIFIED` |
| 3 | Павлов 1906 | Издание не найдено — HOLD |

**Вердикты S1–S5 не меняются.**

## 79. Раунд 128 (2026-11-17): русские вероучения 1911/1913/1985 — сверка формул корпуса

Подробности — `34_` §4.211 (Q207), S226; REPASS-документ, §51.

| # | Место | Итог |
|---|---|---|
| 1 | `13_`/`14_`, Чл. IV, «[1906]»: «действительное… страдательно… Свою душу и Своё тело» | Есть в тексте до 1911 г. (Кунцевич, Харьков, 1911). `13_` смешивает издания — `CONFLATED_EDITIONS` (мягко) |
| 2 | «Дословное переиздание 1928 г.» | По Чл. IV пара активного и пассивного послушания в 1928 г. сглажена — `OVERSTATEMENT` (мягко); Чл. V совпадает по смыслу |
| 3 | Каргель 1913 в `14_`/`20_` | «Господь предлагает… прощение всех грехов»; вторая фраза иная — `QUOTE_NOT_VERBATIM` (мягко); «за всех человеков» подтверждено |
| 4 | «Вероучение 1985: …предназначена для всего мира… Христос умер за всех» (`14_`, `20_`, `D6_`) | Это тезис 3 «Мы верим» (Совет Союза ЕХБ Белоруссии, 2001) — `MISATTRIBUTION` |
| 5 | ПЭ «БАПТИСТЫ»: «искупление всех людей» | Сводный пересказ современного вероучения, не исповедания Павлова |

**Вердикты S1–S5 не меняются.**

## 80. Раунд 129 (2026-11-17): Шафф, *Creeds* I, p. 635

Подробности — `34_` §4.212 (Q208), S227; REPASS-документ, §52.

| # | Место | Итог |
|---|---|---|
| 1 | Лист 659 (цитата «all the Reformed Confessions… infralapsarianism») | **p. 635** — сверено по разметке страниц IA. `LOCATOR_VERIFIED` |
| 2 | С. 5, сн. 15–16: Гейдельберг, в. 37 и II Helv. как «неограниченное искупление» | Шафф на той же странице: «God's promises and Christ's redemption are general» (со ссылкой на в. 37 и II Helv. X). `SCHOLARLY_PRECEDENT` — контекст в пользу статьи. Наши вердикты (V\*, `OVERGENERALIZATION`, `INTERNAL_TENSION`) не меняются: у Шаффа «general» — в регистре предложения, а Дорт и WCF он ставит в те же рамки |

**Вердикты S1–S5 не меняются.**

## 81. Раунд 130 (2026-11-17): Ломбард, *Sent.* III, dist. XX, PL 192:799

Подробности — `34_` §4.213 (Q209), S228; REPASS-документ, §53.

| # | Место | Итог |
|---|---|---|
| 1 | С. 36, сн. 36: формула «sufficienter / efficaciter» как «утверждение Августина» | Дословно — у Ломбарда, PL 192:799 (Sent. III, dist. XX, § 3 по PL). `ATTRIBUTION_SHIFT` прежний |
| 2 | `02_` п. 12: «cap. 3; PL 192:799» против `fathers/13_` «c. 5» | Нумерация разных изданий — `LOCATOR_EDITION_DEPENDENT` |
| 3 | `02_` п. 12: «qui pro omnibus oblatus est…» | В PL: «qui se… obtulit pro omnibus…» — `QUOTE_NOT_VERBATIM` (мягко) |
| 4 | Ломбард на Евр. 5:3: «Christus enim non nisi pro suis membris obtulit» | Противопоставление «за Себя / за других», не довод об объёме — `CONTEXT_REQUIRED` |

**Вердикты S1–S5 не меняются.**

## 82. Раунд 131 (2026-11-17): *Formula Consensus Helvetica*, канон XIII, латынь по Нимейеру и Августи

Подробности — `34_` §4.214 (Q210), S229; REPASS-документ, §54.

| # | Место | Итог |
|---|---|---|
| 1 | С. 7, сн. 25: канон XIII по Клауберу («dreadful death» / «мучительную смерть») | Латынь «diram mortem oppetiit» — Августи 1846, p. 450; Шафф I, p. 488. ACCURATE прежний |
| 2 | `AGENT6` A.10: «duram mortem» | В Августи OCR «diram», «duram» — 0 попаданий: `QUOTE_NOT_VERBATIM` (мягко) |
| 3 | `fathers/10_`: «Niemeyer 1840, pp. 733–735, сверено в Волне 18» | В скане Нимейера (IA) нет одной страницы (вероятно, p. 731); по реконструкции XIII начинается на p. 732, XVI — p. 734. `LOCATOR_IMPRECISE` (мягко). `AGENT6` A.10 прямо пишет, что Нимейер не открывался |
| 4 | Предисловие Формулы («Salvum… fundamentum fidei») | Есть у Нимейера, p. 729 |

**Вердикты S1–S5 не меняются.**

## 83. Раунд 132 (2026-11-17): Каннингем, *Historical Theology* II — пагинация в четырёх печатях

Подробности — `34_` §4.215 (Q211), S230; REPASS-документ, §55.

| # | Место | Итог |
|---|---|---|
| 1 | С. 24, сн. 78: «vol. 2, pp. 379–380» | Разрыв pp. 378/379 и колонтитул «SYNOD OF DORT. 379» одинаковы в печатях 1863, 1870 (*Works* III), 1960 и 1969 гг. (Banner of Truth). `LOCATOR_IMPRECISE` (мягко) больше не зависит от издания |
| 2 | HOLD «изд. 1882 / SWRB 1991» | Сужен: само издание 1882 г. не видено |
| 3 | «Арминий и Гомар» | `SOURCE_CONTRADICTS_CLAIM` прежний: фраза о Гомаре («learned and zealous defender of Calvinism») во всех четырёх печатях одна и та же |

**Вердикты S1–S5 не меняются.**

## 84. Раунд 133 (2026-11-17): Lewis & Demarest, *Integrative Theology* II, pp. 380–381

Подробности — `34_` §4.216 (Q212), S231; REPASS-документ, §56.

| # | Место | Итог |
|---|---|---|
| 1 | С. 5, сн. 18 (Л. и Д. II, p. 381) | «Scholastic Calvinism, however, narrowed the intent of the atonement…». `LOCATOR_VERIFIED`; ACCURATE для слов при сноске («схоластический кальвинизм») |
| 2 | С. 5: Беза «ввёл» ограниченное искупление вместе с супралапсарианской схемой | Своей сноски нет; в OCR т. 2 слова «Beza» нет. `UNSOURCED_CLAIM` (мягко); прежний `SIMPLIFIED` остаётся |
| 3 | С. 4, сн. 13 | «In his later commentaries Calvin more clearly postulates an unlimited atonement. With regard to Galatians…» — ACCURATE, `SCHOLARLY_PRECEDENT` |
| 4 | С. 11, сн. 45 | «Spurgeon, Charles Haddon, 380» в указателе — `LOCATOR_VERIFIED` |
| 5 | REPASS §2, строка 7 | «через Lewis & Demarest (сн. 18)» — `CORPUS_MISREAD` (мягко) |

**Вердикты S1–S5 не меняются.**

## 85. Раунд 134 (2026-11-17): Lewis & Demarest, *Integrative Theology* II, p. 381 — сноска 83

Подробности — `34_` §4.217 (Q213), S232; REPASS-документ, §57.

| # | Место | Итог |
|---|---|---|
| 1 | С. 26, сн. 83 — локатор | Отрывок о «scholastic / high Calvinism» — p. 381 (между Блёшем и Тюрретином по указателю). `LOCATOR_VERIFIED` |
| 2 | «Эффективность» как парадигма; «не просто возможным – действительным и надежным» | «the design of the cross was not merely to provide salvation but to secure the salvation of those persons the Father gave to the Son». ACCURATE по существу |
| 3 | «Ранние авторы фокусировались на достаточности» | В отрывке нет «sufficiency». У Л. и Д. ранний Кальвин — «unlimited atonement» (p. 380), схоласты — «narrowed the intent». `SIMPLIFIED` (мягко): контраст источника смягчён |
| 4 | Связь с WCF | Л. и Д. сами ссылаются на WCF гл. III (декрет раньше дела Христа). Лексический довод статьи (*redemption*) — её собственный |

**Вердикты S1–S5 не меняются.**

## 86. Раунд 135 (2026-11-17): White, *The Potter's Freedom*, p. 255 — сноска 9

Подробности — `34_` §4.218 (Q214), S233; REPASS-документ, §58.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 9 — локатор p. 255 | Отрывок о Гессгусене и 1 Ин. 2:2 стоит перед колонтитулом «256 THE POTTER'S FREEDOM». `LOCATOR_VERIFIED` (печать 2000 г.) |
| 2 | Ответ Гессгусену | «Calvin's statement in response to Heshusius is especially telling: „I should like to know how the wicked can eat the flesh of Christ which was not crucified for them…“» — ACCURATE |
| 3 | 1 Ин. 2:2 | «under the world ‚all‘ [in 1 John 2:2] he does not include the reprobate…» — ACCURATE |
| 4 | 1 Тим. 2:4 | По указателю Писания — с. 169, 257, 259; на p. 255 не видно. «Напр.» смягчает |
| 5 | «Основные доводы» | Уайт добавляет термины («reconciliation», «redemption», «propitiation»), избрание, мёртвость в грехе, ходатайство и отсылает к Николю (*WTJ* 1985). `SOURCE_SAYS_MORE` (мягко) |

**Вердикты S1–S5 не меняются.**

## 87. Раунд 136 (2026-11-17): Шнукер, «Helvetic Confessions» (словарь Элвелла) — сноска 17

Подробности — `34_` §4.219 (Q215), S234; REPASS-документ, §59.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 17 — содержание | Элвелл (1984), pp. 506–507: «The Heidelberg Catechism and the Second Helvetic Confession are the two most widely adopted and authoritative of the Reformed statements of faith. R. V. Schnucker». ACCURATE |
| 2 | Сн. 17 — атрибуция | Подпись Шнукера в изданиях 1984, 2001 и 2017 гг. ACCURATE |
| 3 | Сн. 17 — «С. 312» | Страница русского перевода 2003 г. не видена. HOLD |
| 4 | «Оба они содержат исповедание неограниченного искупления» | Собственный вывод статьи (сн. 15–16), Шнукеру не приписан |

**Вердикты S1–S5 не меняются.**

## 88. Раунд 137 (2026-11-17): Лютер, сн. 5 — страницы *LW* 26

Подробности — `34_` §4.220 (Q216), S235; REPASS-документ, §60.

| # | Место | Итог |
|---|---|---|
| 1 | *LW* 26:277 | = WA 40/I, 433 («qui habet et portat omnia omnium peccata in corpore suo»); Ryken (2005) и Schroeder (2016) дают ту же цитату с «26:277». `LOCATOR_VERIFIED` |
| 2 | *LW* 26:285 | = WA 40/I, 444b–445 («Luther Refracted», 2015, дважды); WA 445: «Christus in quem Pater coniecit peccata totius mundi». `LOCATOR_VERIFIED` (класс B) |
| 3 | Третья фраза | Ближайший смысл — *LW* 26:281 = WA 439. `WORDING_NOT_LOCATED` (мягко) — без изменений |
| 4 | Контекст | «Quatenus credis, eatenus habes» — та же *LW* 26:285; `CONTEXT_OMITTED` не ставится (как в §25) |

**Вердикты S1–S5 не меняются.**

## 89. Раунд 138 (2026-11-17): Смолли, WBC 51, p. 40 — сноска 62

Подробности — `34_` §4.221 (Q217), S236; REPASS-документ, §61.

| # | Место | Итог |
|---|---|---|
| 1 | Локатор p. 40 | Shultz (2013) даёт дословную фразу Смолли с «40»; Peterson (2012, по изд. 1984 г.) — p. 40 к 1 Ин. 2:2. `LOCATOR_VERIFIED` (класс B) |
| 2 | Вывод о масштабе | Смолли: жертва «embraces the sins of the whole world», не только «наши». ACCURATE |
| 3 | Посылка «мы = все верующие» | У Смолли «наши» — «those of John’s immediate circle». `SOURCE_TENSION` (мягко); сноска стоит при выводе, не при посылке |
| 4 | «Dallas: Word, 1989» | Пагинация совпадает с печатью 1984 г.; тот же адрес есть и в печатной библиографии 2015 г. `ELECTRONIC_EDITION_UNMARKED` остаётся мягким |
| 5 | Попутно | Устаревшие пометки о II Helv. XI.15 (REPASS §15) отосланы к §16.3 |

**Вердикты S1–S5 не меняются.**

## 90. Раунд 139 (2026-11-17): Бокэм, WBC 50, p. 240 — сноска 52

Подробности — `34_` §4.222 (Q218), S237; REPASS-документ, §62.

| # | Место | Итог |
|---|---|---|
| 1 | Локатор p. 240 | Watson (2012): «Bauckham 1983, 240» в толковании 2 Пет. 2:1; Shultz (2013): три ссылки на p. 240 в разборе «Master who bought them». `LOCATOR_VERIFIED` (класс B) |
| 2 | Лексический тезис (ἀγοράζω = покупать/выкупать) | Слова Бокэма не видны; Shultz относит его к сторонникам сотериологического прочтения, но анкер сноски не установлен. Содержание — HOLD |
| 3 | «Ср.» BDAG, p. 14 | Алфавитно правдоподобно (класс C); не открыто. HOLD |
| 4 | «Dallas: Word, 1998» | Оригинал 1983 г.; пагинация совпадает. `ELECTRONIC_EDITION_UNMARKED` остаётся мягким |

**Вердикты S1–S5 не меняются.**

## 91. Раунд 140 (2026-11-17): Шрайнер, NAC 37, p. 329 — сноска 54

Подробности — `34_` §4.223 (Q219), S238; REPASS-документ, §63.

| # | Место | Итог |
|---|---|---|
| 1 | Локатор p. 329 | В OCR NAC 2003 видно толкование 2:1 (перевод → обзорный абзац → разбор kai/despotēs → конец страницы); печатный номер не виден. `LOCATOR_PLAUSIBLE` (класс C) |
| 2 | Фраза 1 («как Господин купил их… в рабы… цена искупительной смерти») | Ядро есть: «as their master he bought them and made them his servants». Вторая половина не найдена. `WORDING_PARTIAL` |
| 3 | Фразы 2–4 (не язычники; часть церкви, исповедовали веру; верные слуги, пролил кровь) | Страницы после разбора despotēs в индекс не попали (пять выражений из pp. 331–332 тоже дают 0). `WORDING_NOT_LOCATED` (мягко) |
| 4 | Вывод Шрайнера pp. 331–332 | Эскобедо (2002/2004) дословно: «phenomenological language… did not truly belong to God… bought… in the sense that they gave every indication initially of genuine faith». `CONTEXT_OMITTED` — класс B для NAC 2003 |
| 5 | Многоточие во фразе 3 | Скрывает ли оно оговорку «did not truly belong to God» — `OPEN`, не утверждается. *Снято в раунде 141 (§92): многоточия в статье нет* |

**Вердикты S1–S5 не меняются.**

## 92. Раунд 141 (2026-11-17): Гангел, BKC II, p. 870 — сноски 51 и 55; поправка к §91

Подробности — `34_` §4.224 (Q220), S239; REPASS-документ, §64.

| # | Место | Итог |
|---|---|---|
| 1 | Поправка к §91, п. 5 | Во фразе 3 Шрайнера в статье многоточия нет («…частью церкви, которой Петр адресовал свое послание…»). Открытый вопрос снят |
| 2 | Локатор p. 870 | Swindoll (1990): BKC p. 869 — это 2 Пет. 1:21; 2:1 — на следующей странице. `LOCATOR_CONSISTENT` (класс B для соседней страницы) |
| 3 | Сн. 55: перевод | Совпадает с текстом BKC в цитате Эскобедо (2002/2004). ACCURATE (класс C) |
| 4 | Сн. 51: три варианта | Это варианты (1)–(3) Гангела с его опровержениями; (4) — «наиболее вероятно» статьи. Атрибуция верна; «seems to read into» стало «слишком много вчитывает» — `HEDGE_DROPPED` (мягко) |
| 5 | Шрайнер в схеме Гангела | Приведён в поддержку (4); его собственный вывод (pp. 331–332, феноменологический) ближе к отвергнутому (3). Усиление `CONTEXT_OMITTED` |

**Вердикты S1–S5 не меняются.**

## 93. Раунд 142 (2026-11-17): Грин, TNTC, p. 118 — сноски 56 и 57

Подробности — `34_` §4.225 (Q221), S240; REPASS-документ, §65.

| # | Место | Итог |
|---|---|---|
| 1 | Цитата сн. 56 | Тематическая параллель «крест — исход», цель — «народ для Себя» (2 Цар. 7:23). Утверждения о греческом слове нет; стих употреблён верно |
| 2 | Фраза со сн. 57 («Там же») | Лексическое утверждение (ἀγοράζω об исходе) — собственная фраза статьи; `FACT_ERROR` из §15 в силе |
| 3 | Чья ошибка | HOLD: книга не открыта. Правдоподобнее, что статья превратила тематическую параллель в лексическую, но это не доказано |
| 4 | Следующий довод («избавлены все… итог различен») | Принадлежит статье, за слова Грина не выдан; цитата его не подкрепляет |
| 5 | Поправка | В REPASS §15 фраза статьи была процитирована как «агоразо»; в статье — «агорадзо» |

**Вердикты S1–S5 не меняются.**

## 94. Раунд 143 (2026-11-17): Хиберт, сн. 63 — цитата Бенгеля внутри цитаты

Подробности — `34_` §4.226 (Q222), S241; REPASS-документ, §66.

| # | Место | Итог |
|---|---|---|
| 1 | «Умилостивление настолько же широко, насколько широк грех» (во внутренних кавычках) | Изречение Бенгеля, *Gnomon* (1742), на 1 Ин. 2:2: «Quam late patet peccatum, tam late propitiatio»; англ. пер. 1859, vol. V, pp. 115–116 |
| 2 | Русская передача | Точна; совпадает с английской формой «The propitiation is as wide as the sin» (Бриггс 1895, Вуэст 1954 — с пометой «Bengel») |
| 3 | Атрибуция в статье | Статья фразу никому не приписывает — ошибки нет |
| 4 | Называет ли Бенгеля сам Хиберт; p. 97 | HOLD: ни русское, ни английское издание не открыто |
| 5 | Ярлык «кальвинист» | `AFFILIATION_ERROR` (раунд 84) в силе; изречение лютеранина Бенгеля его не подкрепляет |

**Вердикты S1–S5 не меняются.**

## 95. Раунд 144 (2026-11-17): Ходжес, BKC II, p. 887 — сноски 66 и 67

Подробности — `34_` §4.227 (Q223), S242; REPASS-документ, §67.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 66 («Христос действительно умер за каждого… *может* спастись, если пожелает») | Перевод точен (класс C: два посредника совпадают дословно); ссылки на стихи и курсив сохранены |
| 2 | Сн. 66: опущенная фраза | «In context, however, John’s point is…» — главная мысль стиха, по Ходжесу, уверенность верующих. Ошибкой не считается |
| 3 | Сн. 67 («Крест действительно умилостивил Бога…») | Перевод точен; фраза взята через абзац, статья отделяет её словами «И еще:» — склейки нет |
| 4 | p. 887 | `LOCATOR_PLAUSIBLE`: введение Ходжеса — p. 882 (Hanna 2015, класс B) |
| 5 | «2 vols., 1985, vol. 2» | Новозаветный том — 1983 г.; мягкая оговорка, как для Гангела (§92) |

**Вердикты S1–S5 не меняются.**

## 96. Раунд 145 (2026-11-17): Робертсон, *Word Pictures*, т. VI, p. 210 — сноска 68

Подробности — `34_` §4.228 (Q224), S243; REPASS-документ, §68.

| # | Место | Итог |
|---|---|---|
| 1 | Цитата сн. 68 | Есть в печатном т. VI (1933), p. 210 — последняя фраза толкования 1 Ин. 2:2 (IA `generalepistlesr0000arch`, класс A) |
| 2 | Перевод | Точен; «provides for» передано как «обеспечило все, что нужно», время изменено — на смысл не влияет |
| 3 | Контекст | Опущено предшествующее толкование «весь мир» как «масса греха» (5:19); тезис цитаты не меняется |
| 4 | Сноска | Год верен; тома и страницы нет — `BIBLIOGRAPHY_INCOMPLETE` (мягко) |

**Вердикты S1–S5 не меняются.**

## 97. Раунд 146 (2026-11-17): Мак-Артур, MSB 1997, с. 1965 — сноска 69, многоточие

Подробности — `34_` §4.229 (Q225), S244; REPASS-документ, §69.

| # | Место | Итог |
|---|---|---|
| 1 | Многоточие в цитате сн. 69 | Заменяет только «(see note on 1 Tim. 4:10)» — OCR издания NKJV 1997 г. (IA `macarthurstudybi0000unse_n6a5`) и изданий 2006–2010 гг. (класс B). Содержательных слов не опущено |
| 2 | Перевод | Точен; «actually satisfied fully» передано страдательным оборотом без «actually» — смысл сохранён |
| 3 | Соседние фразы заметки | Отрицание уплаты за неверующих — `FRAMING` из §8 в силе |
| 4 | с. 1965 | HOLD: индекс даёт только общее число страниц скана |

**Вердикты S1–S5 не меняются.**

## 98. Раунд 147 (2026-11-17): Грудем — сноски 71 (с. 672) и 77 (с. 680)

Подробности — `34_` §4.230 (Q226), S245; REPASS-документ, §70.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 71, «усиленная форма» довода | У Грудема 1994 г. дословно: «could not condemn to eternal punishment anyone whose sins are already paid for: that would be demanding double payment» (OCR IA `systematictheolo00grud_0`, класс B). «Ср.» уместно; «бесконечной ценности» — добавка статьи |
| 2 | «Слабая форма» с любым наказанием | Нет ни в сн. 70, ни в сн. 71: `STRAWMAN` (мягко) подкреплён |
| 3 | Ответ через вменение | У Грудема уплата связана с неизбежным применением Духом: `MISIDENTIFIED_TARGET` распространён на сн. 71 |
| 4 | Сн. 77, предлог «for» | Атрибуция верна (ACCURATE); Грудем выводит из различения частное искупление: `SOURCE_SAYS_MORE` (мягко) |
| 5 | Страницы | Русские с. 672 и 680 — HOLD; английские — pp. 594–603 только по вторичным ссылкам |

**Вердикты S1–S5 не меняются.**

## 99. Раунд 148 (2026-11-17): Хукема — сноска 100 (с. 360)

Подробности — `34_` §4.231 (Q227), S246; REPASS-документ, §71.

| # | Место | Итог |
|---|---|---|
| 1 | Опорная фраза сн. 100 | PDF статьи, с. 33 (класс A1): Павел «увязывает освобождение материального творения от смерти с тем искуплением, которое совершено через жертву Христову» |
| 2 | Выходные данные | «Мн.: Полиграфкомбинат им. Я. Коласа, 2019», 400 с. — совпадают с карточкой книги (класс C) |
| 3 | Довод | «Ср.» поддерживает бесспорный тезис о восстановлении творения; на объём искупления не влияет (`20_` C32.05, C33.01) |
| 4 | Страница | Содержание с. 360 и место в *Created in God’s Image* (1986) — HOLD |

**Вердикты S1–S5 не меняются.**

## 100. Раунд 149 (2026-11-17): сноска 101 — TWOT 1023 (Харрис), HALOT, Swanson

Подробности — `34_` §4.232 (Q228), S247; REPASS-документ, §72.

| # | Место | Итог |
|---|---|---|
| 1 | «выкупа путем замещения» (с. 33) | TWOT 1980, ст. 1023: от kōper «ransom»… «It means “to atone by offering a substitute.”» (OCR, класс B). По существу верно; в кавычках — сжатый пересказ: `QUOTE_NOT_VERBATIM` (мягко) |
| 2 | Вывод о «неживой материи» | Замещение предполагает лицо, за которое дают замену; статья сама называет святилище «не нравственным существом»: `NON_SEQUITUR` (мягко), как `20_` C33.05 |
| 3 | HALOT p. 494, Swanson #4105, печатная страница TWOT | HOLD |

**Вердикты S1–S5 не меняются.**

## 101. Раунд 150 (2026-11-17): сноска 98 — Демарест, *The Cross and Salvation*, p. 193

Подробности — `34_` §4.233 (Q229), S248; REPASS-документ, §73.

| # | Место | Итог |
|---|---|---|
| 1 | Цитата Демареста (с. 31), английские вставки | «universal in its provision and particular in its application» и p. 193 подтверждены двумя независимыми посредниками (Тиссен; Шульц 2008; класс C). Перевод верен по смыслу; без флага |
| 2 | «Описывая последнюю точку зрения» | Демарест излагает собственный взгляд («Наш взгляд»). Ярлык «сублапсарианство» дан через Эриксона (сн. 97); по существу правдоподобен; называет ли так взгляд сам Демарест — HOLD |
| 3 | Выходные данные | Crossway, 1997 — верно |
| 4 | Корпус | Исправлены `23_` §7 (номера сносок) и `35_` FP-109 (издательство); `16_` §6 — примечание о пересказах в кавычках |

**Вердикты S1–S5 не меняются.**

## 102. Раунд 151 (2026-11-17): сноска 112 — Гайслер, BKC II (Кол. 1:20)

Подробности — `34_` §4.234 (Q230), S249; REPASS-документ, §74.

| # | Место | Итог |
|---|---|---|
| 1 | Цитата Гайслера (с. 35) | BKC: «The phrase “all things” is limited to good angels and redeemed people since only things on earth and things in heaven are mentioned. Things “under the earth” (Philippians 2:10) are not reconciled» (два посредника, класс C). Перевод точен |
| 2 | Гайслер ↔ Мелик | Гайслер сужает сам объём «всего» до лиц; Мелик и «восстановительная» цель статьи включают материальное творение: `INTERNAL_TENSION` (мягко) подтверждён по источнику |
| 3 | Контекст | В *When Critics Ask* (1992) Гайслер читает стих как «universal sovereignty» — близко к толкованию через подчинение, отвергнутому в сн. 107–108; без флага |
| 4 | Печатная p. 674 | Соседние ст. 15–18 — pp. 672–673; HOLD |

**Вердикты S1–S5 не меняются.**

## 103. Раунд 152 (2026-11-17): сноски 109–111 — Мелик, NAC 32, p. 225 (Кол. 1:20)

Подробности — `34_` §4.235 (Q231), S250; REPASS-документ, §75.

| # | Место | Итог |
|---|---|---|
| 1 | Цитаты Мелика (с. 35, сн. 109–110) и пересказ о трёх сферах | Совпадают с текстом NAC 32 (посредники, класс C); p. 225 подтверждена. «Должен простираться» вместо «extends» — мелочь |
| 2 | «Наиболее вероятное объяснение» вместо толкования через подчинение (сн. 107–108) | Мелик: «reconciliation may be effected by voluntary submission… or by involuntary submission, being conquered… Everyone and everything will be subordinated to Christ». `SOURCE_SAYS_MORE` (существенно): опущенное определение снимает противопоставление статьи |
| 3 | Для объёма искупления | Всеобщее «примирение» у Мелика для противящихся означает покорение. Всеобщность заместительной платы из Кол. 1:20 через Мелика не следует. Довод `06_` и вывод `20_` C35.02 подтверждены |
| 4 | Прим. 106 Мелика (сн. 111) | HOLD |

**Вердикты S1–S5 не меняются.**

## 104. Раунд 153 (2026-11-17): сноски 107–108 — Кинер, MSB p. 1833, BDAG p. 112 (Кол. 1:20)

Подробности — `34_` §4.236 (Q232), S251; REPASS-документ, §76.

| # | Место | Итог |
|---|---|---|
| 1 | Кинер (сн. 107) | 2-е изд. (2014, p. 572; класс B): «The reconciling even of the invisible powers (1:16) refers to their subordination rather than their salvation (2:15), “peace” being an end to hostilities». Подчинение — только для властей. Текст 1993 г. — HOLD |
| 2 | MSB, p. 1833 (сн. 107) | NKJV 1997 (OCR, класс B): «total and complete reconciliation of believers… This text does not teach that, as a result, all will believe; rather it teaches that all will ultimately submit… God and those He saved are no longer at enmity». Печатная страница — HOLD |
| 3 | «Некоторые авторы считают, что «примирение»… означает подчинение земного и небесного» | Оба источника, как и Мелик (§103), различают примирение верующих и покорение враждебных. `STRAWMAN` (умеренно) |
| 4 | BDAG, p. 112 (сн. 108) | Страница правдоподобна (класс C); глосса — HOLD. Значение слова Кинер не оспаривает, так что довод его тезиса не касается: `NON_SEQUITUR` (мягко) |
| 5 | Для объёма искупления | Ни один из трёх комментариев не выводит из Кол. 1:20 всеобщую заместительную плату |

**Вердикты S1–S5 не меняются.**

## 105. Раунд 154 (2026-11-17): сноска 104 — Баркли, DSB, p. 124 (Феодорит и Эразм)

Подробности — `34_` §4.237 (Q233), S252; REPASS-документ, §77.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 104: Феодорит и Эразм — примирение ангелов «не с Богом, а с людьми» | Баркли: «The most interesting suggestion was made by Theodoret and followed by Erasmus… not that the heavenly angels were reconciled to God, but that they were reconciled to men». Пересказ точен (текст — класс C; фраза — OCR изданий 1975 г., класс B) |
| 2 | `OVERSTATEMENT` р. 108 (Эразм) | Формула принадлежит Баркли; статья её точно передала |
| 3 | «Westminster John Knox Press, 1975» | В 1975 г. — Westminster Press (Philadelphia): `EDITION_MISLABEL` (мягко) |
| 4 | P. 124 | Правдоподобно; печатная страница — HOLD |

**Вердикты S1–S5 не меняются.**

## 106. Раунд 155 (2026-11-17): сноска 102 — Вюст, *Word Studies* VI, p. 188 (Кол. 1:20)

Подробности — `34_` §4.238 (Q234), S253; REPASS-документ, §78.

| # | Место | Итог |
|---|---|---|
| 1 | Сн. 102: «ср.» Вюст к «небесное = ангелы» | Вюст к Кол. 1:20 (OCR, класс B): Бог и человек; «the curse placed upon the material universe… will one day be removed through that same precious Blood». Тезиса об ангелах в прочитанных фрагментах нет: `SOURCE_BROADER_THAN_CLAIM` (мягко) |
| 2 | Сн. 102 в целом | Теперь у всех трёх источников «ср.» (Винсент, Лайтфут, Вюст) — тот же мягкий флаг |
| 3 | «Vol. 6. P. 188» | В издании Logos т. 6 — Колоссянам (класс C); p. 188 — `LOCATOR_PLAUSIBLE`, HOLD |

**Вердикты S1–S5 не меняются.**

## 107. Раунд 156 (2026-11-17): самопроверка раунда 155 (сн. 102, Вюст)

Подробности — `34_` §4.239 (Q235), S254; REPASS-документ, §79.

| # | Место | Итог |
|---|---|---|
| 1 | Фразы Вюста из р. 155 | Все запрошены заново (OCR, класс B) — **подтверждены** |
| 2 | «Вероятно, к Кол. 1:16» | Уточнено: перечень «thrones, dominions, principalities, and powers» — значит, Кол. 1:16 |
| 3 | «Место не установлено» (суд у Великого белого престола) | Уточнено: комментарий к Еф. 1:10; падшие ангелы — под судом, о примирении ангелов нет |
| 4 | «Vol. 6» | Подкреплено: vol. 6 pp. 199–200 = Кол. 2:8 (класс C); p. 188 — `LOCATOR_PLAUSIBLE`, HOLD |
| 5 | REPASS §11, «в IA его нет» | Поправка: в IA есть, доступ ограничен |

**Вердикт сн. 102 и вердикты S1–S5 не меняются.**

## 108. Раунд 157 (2026-11-17): самопроверка раунда 154 (Баркли) и списков HOLD

Подробности — `34_` §4.240 (Q236), S255; REPASS-документ, §80.

| # | Место | Итог |
|---|---|---|
| 1 | Фраза Баркли о Феодорите и Эразме (р. 154) | Подтверждена по OCR трёх изданий 1975 г. (класс B) |
| 2 | HOLD «*Annotationes* Эразма к Кол. 1:20» в REPASS §77.5, §78.5 | Ошибочный возврат: снято ещё в р. 110 (§33). Исправлено; остаётся визуальная сверка p. 635 |
| 3 | Ранние сводки «Баркли — HOLD» | Помечены: после р. 154 HOLD — только печатная p. 124 |

**Вердикты S1–S5 не меняются.**

## 109. Раунд 158 (2026-11-17): самопроверка раунда 153 (Кинер, MSB, BDAG)

Подробности — `34_` §4.241 (Q237), S256; REPASS-документ, §81.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи и сн. 107–108 | Совпадает с PDF |
| 2 | Заметка MSB к Кол. 1:20 | Дополнено: «The Gr. word for “reconcile” means “to change”…» (три издания, вкл. NKJV 1997) |
| 3 | `STRAWMAN` (умеренно) для сн. 107; `NON_SEQUITUR` (мягко) для сн. 108 | Остаются в силе |

**Вердикты S1–S5 не меняются.**

## 110. Раунд 159 (2026-11-17): самопроверка раунда 152 (Мелик)

Подробности — `34_` §4.242 (Q238), S257; REPASS-документ, §82.

| # | Место | Итог |
|---|---|---|
| 1 | Посредник (а) — коллаж пяти комментариев | Фраза о «voluntary / involuntary submission» лежит внутри блока Мелика; атрибуция подтверждена |
| 2 | URL посредников | Внесены (REPASS §75.2, `34_` S250) |
| 3 | Печатная страница фразы о подчинении | Не установлена (не p. 225 по умолчанию) |

**Вердикты S1–S5 не меняются.**

## 111. Раунд 160 (2026-11-17): самопроверка раунда 151 (Гайслер)

Подробности — `34_` §4.243 (Q239), S258; REPASS-документ, §83.

| # | Место | Итог |
|---|---|---|
| 1 | Формулировка Гайслера к Кол. 1:20 | Подтверждена повторно по двум посредникам (класс C) и одному пересказу (класс D) |
| 2 | p. 674 | HOLD в силе: последние видимые примечания посредника ведут к p. 673 |
| 3 | `INTERNAL_TENSION` (мягко) | В силе |

**Вердикты S1–S5 не меняются.**

## 112. Раунд 161 (2026-11-17): CO 9:484 — сверка по изданию и по корпусу

Подробности — `34_` §4.244 (Q240), S259; REPASS-документ, §84.

| # | Место | Итог |
|---|---|---|
| 1 | E1 / строка 78 этого аудита | Дословно совпадает с OCR CO 9, кол. 484 (A2) |
| 2 | `02_` п. 17 | Окончание цитаты было неточным; исправлено, прежнее помечено HISTORICAL |
| 3 | `AGENT6_…` строка 137 | Неточно; остаётся за владельцем (R5) |
| 4 | Баланс того же разворота | Кол. 483: «victimam, qua expiata sunt mundi peccata»; кол. 485: «solis electis» — об освящении |

**Вердикты S1–S5 не меняются.**

## 113. Раунд 162 (2026-11-17): самопроверка раунда 150 (Демарест)

Подробности — `34_` §4.245 (Q241), S260; REPASS-документ, §85.

| # | Место | Итог |
|---|---|---|
| 1 | Формулы «universal in its provision… particular in its application», p. 193 | Подтверждены повторно (класс C); URL посредника внесён |
| 2 | Выходные данные сн. 98 | Crossway 1997, серия Фейнберга — подтверждено (класс C) |
| 3 | Ярлык «сублапсарианство» у самого Демареста | HOLD |
| 4 | Правки `23_` §7 / `35_` FP-109 | Верны по PDF статьи |

**Вердикты S1–S5 не меняются.**

## 114. Раунд 163 (2026-11-17): самопроверка раунда 149 (сн. 101, TWOT 1023)

Подробности — `34_` §4.246 (Q242), S261; REPASS-документ, §86.

| # | Место | Итог |
|---|---|---|
| 1 | Текст сн. 101 и фраза к ней (PDF статьи, с. 33–34) | Совпадает с §72.1 |
| 2 | Глосса TWOT «to atone by offering a substitute» | Подтверждена в трёх сканах (класс B); `QUOTE_NOT_VERBATIM` (мягко) в силе |
| 3 | Значение «purge» в заголовке TWOT 1023; «for the worshipper» | Уточняет `NON_SEQUITUR` (мягко): словарь сам даёт значение для очищения места |
| 4 | `page_num` Open Library как номер листа | Поправка формулировки §72.2 (в) |
| 5 | HALOT p. 494, Swanson #4105, печатная p. 453 | HOLD |

**Вердикты S1–S5 не меняются.**

## 115. Раунд 164 (2026-11-17): самопроверка раунда 148 (сн. 100, Хукема)

Подробности — `34_` §4.247 (Q243), S262; REPASS-документ, §87.

| # | Место | Итог |
|---|---|---|
| 1 | Фраза статьи и сн. 100 (PDF, с. 33) | Совпадает с §71.1; sha256 тот же |
| 2 | Выходные данные (Минск, 2019, 400 с., ISBN 978-985-7101-27-6) | Подтверждены карточками (класс C) |
| 3 | equalibra.org: 380 с., 2018 г. | Мягкая заметка; ошибки в сноске нет |
| 4 | Отрывок гл. 12 (без страниц) | Тема близка; с с. 360 не отождествляется |
| 5 | Содержание с. 360 | HOLD |

**Вердикты S1–S5 не меняются.**

## 116. Раунд 165 (2026-11-17): самопроверка раунда 147 (сн. 71 и 77, Грудем)

Подробности — `34_` §4.248 (Q244), S263; REPASS-документ, §88.

| # | Место | Итог |
|---|---|---|
| 1 | Текст сн. 71 и 77 (PDF, с. 19 и 24) | Совпадает с §70.1 |
| 2 | Русский текст к сн. 71 («вечные муки… повторной платы») | `STRAWMAN` (мягко) в силе и подкреплён |
| 3 | «Бесконечная ценность» | Поправка формулировки §70.3: «неизмеримая ценность» — общее положение того же раздела |
| 4 | Русский текст к сн. 77 (предлог «за») | ACCURATE; `SOURCE_SAYS_MORE` (мягко) в силе |
| 5 | Грудем против постановки вопроса через цель (Беркхоф) | Наблюдение, вердикты не меняет |
| 6 | Печатные с. 672 и 680 | HOLD (оценка 673 / 682) |

**Вердикты S1–S5 не меняются.**

## 117. Раунд 166 (2026-11-17): самопроверка раунда 146 (сн. 69, MSB к 1 Ин. 2:2)

Подробности — `34_` §4.249 (Q245), S264; REPASS-документ, §89.

| # | Место | Итог |
|---|---|---|
| 1 | Текст сн. 69 (PDF, с. 19) | Совпадает с §69.1 |
| 2 | Многоточие = «(see note on 1 Tim. 4:10)» | В силе; повторный поиск в сканах 1997, 2008 и 2010 гг. |
| 3 | Фразы цитаты | Точно (фраза 1), точно по смыслу (фразы 2–3) — в силе |
| 4 | Контекст после цитаты: «actual satisfaction and atonement was made only for those who believe» | Дополнение к `FRAMING` |
| 5 | Печатная с. 1965 | HOLD (`page_num` 2182–2264 — страницы скана) |

**Вердикты S1–S5 не меняются.**

## 118. Раунд 167 (2026-11-17): самопроверка отзыва раунда 157 на #618 (Чарнок, Lingendes, 1699)

Подробности — `34_` §4.250 (Q246), S265; REPASS-документ, §90.

| # | Место | Итог |
|---|---|---|
| 1 | Маргиналия «Lingend.» — leaf 520 | Печатная с. 521 (колонтитулы: leaf 515 = 516; после пассажа — 522) |
| 2 | Ориентир #627 «p. 513» | Неверен: `page_numbers.json` не учитывает пропуск 337–344 |
| 3 | Цифры в OCR | Не прочитаны («**3») — отзыв р. 157 в силе |
| 4 | «p. 185» в 1699 г. | Только машинное чтение #627; Nichol IV OCR — «p. 185». Изображение не открылось (HTTP 500) |
| 5 | HOLD ED-02 | В силе |

**Вердикты S1–S5 не меняются.**

## 119. Раунд 168 (2026-11-17): самопроверка раунда 145 (сн. 68, Робертсон, *Word Pictures* VI)

Подробности — `34_` §4.251 (Q247), S266; REPASS-документ, §91.

| # | Место | Итог |
|---|---|---|
| 1 | Страница статьи | Поправка: с. 18 (не 18–19); §68.1 исправлен |
| 2 | Цитата, т. VI p. 210 | В силе (leaf 228 → p. 210, confidence 98) |
| 3 | Перевод, контекст, год 1933 | В силе |
| 4 | Сноска без тома и страницы | `BIBLIOGRAPHY_INCOMPLETE` (мягко) — в силе |
| 5 | «Более 1400 страниц» *Grammar* | Верно для изд. 1923 г. (для 1919 г. — только по числу листов скана; 1923 г.: 1453 с.); изд. 1914 г. — 1360 с. |

**Вердикты S1–S5 не меняются.**

## 120. Раунд 169 (2026-11-17): чистка и подготовка ветки к слиянию

Подробности — `34_` §4.252 (Q248), S267; REPASS-документ, §92.

| # | Место | Итог |
|---|---|---|
| 1 | Слияние с main `389de7b1` | Без конфликтов; разница — 45 файлов корпуса, мусора нет |
| 2 | Подсчёт разделов `34_` | Исправлен: расхождение 3 с раундов 66–68; теперь 248 с `Q`, 250 §4.x |
| 3 | Строки S153–S156 | Добавлены в таблицу §3 |
| 4 | Формулировка р. 168 о *Grammar* «1919 г. и позже» | Сужена до издания 1923 г.; 1919 г. — только по числу листов |

**Вердикты S1–S5 не меняются.**

## 121. Раунд 170 (2026-11-17): самопроверка раунда 144 (Ходжес, BKC) и проверка ссылок ветки

Подробности — `34_` §4.253 (Q249), S268; REPASS-документ, §93.

| # | Место | Итог |
|---|---|---|
| 1 | Внутренние ссылки (§4.x, REPASS §N, S-номера, Markdown-ссылки) | Битых нет; «§5.0» в REPASS §88 уточнено до `34_` §5.0 |
| 2 | Тексты сн. 66–67 | В силе (класс C) |
| 3 | p. 887 | HOLD: сканы BKC в IA закрыты, в индексе нет |
| 4 | «НЗ — т. 2 двухтомника 1985» | Моё непроверенное допущение; LC: [1] NT, [2] OT. Помечено в пяти местах |

**Вердикты S1–S5 не меняются.**

## 122. Раунд 171 (2026-11-17): самопроверка раунда 143 (Хиберт, сн. 63 — изречение Бенгеля) и чистка ветки

Подробности — `34_` §4.254 (Q250), S269; REPASS-документ, §94.

| # | Место | Итог |
|---|---|---|
| 1 | Текст сн. 63 (PDF, с. 17) | Совпадает; Бенгель в статье не назван |
| 2 | *Gnomon* 1742 и перевод 1859 | Совпадают (OCR IA); перевод — p. 116 |
| 3 | Английская форма «The propitiation is as wide as the sin» | Раньше всех найденных — Винсент (1887); Вуэст повторяет его ряд ссылок. Мягкое уточнение в REPASS §66.2 и `34_` S241 |
| 4 | Хиберт p. 97 | HOLD: в индексе Open Library его нет |
| 5 | `git diff --check` против main | Чисто |

**Вердикты S1–S5 не меняются.**

## 123. Раунд 172 (2026-11-17): самопроверка раунда 142 (Грин, сн. 56–57) и опоры раунда 92 (ἀγοράζω в LXX)

Подробности — `34_` §4.255 (Q251), S270; REPASS-документ, §95.

| # | Место | Итог |
|---|---|---|
| 1 | Текст сн. 56–57 (PDF, с. 14) | Совпадает |
| 2 | 2 Цар. 7:23 (MT, LXX) | לִפְדּוֹת / λυτρώσασθαι — в силе |
| 3 | ἀγοράζω в LXX об исходе | Ни одного места — `FACT_ERROR` в силе |
| 4 | «24 словоформы ἀγοράζω» | Моя ошибка счёта: 23 места (перечень не менялся). Исправлено в пяти местах |
| 5 | Локаторы «с. 13–14» | Шрайнер — с. 13, Грин — с. 14 |
| 6 | Чья ошибка в сн. 57 | HOLD (Грин p. 118 не открыт) |

**Вердикты S1–S5 не меняются.**

## 124. Раунд 173 (2026-11-17): самопроверка раунда 141 (Гангел, сн. 51 и 55)

Подробности — `34_` §4.256 (Q252), S271; REPASS-документ, §96.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи (с. 12–13) | Совпадает |
| 2 | Цитата BKC у Эскобедо (2002, ред. 2004) | Совпадает; курсив варианта (4) — его («emphasis mine») |
| 3 | Swindoll, p. 24, n. 3 → BKC p. 869 = 2 Пет. 1:21 | Совпадает; p. 870 — `LOCATOR_CONSISTENT` |
| 4 | Перевод сн. 55 | ACCURATE (класс C) |
| 5 | Пересказ вариантов 1–3 | Расширен пояснениями статьи — мягко, в рамках `HEDGE_DROPPED` |
| 6 | p. 870 | HOLD |

**Вердикты S1–S5 не меняются.**

## 125. Раунд 174 (2026-11-17): самопроверка раунда 140 (Шрайнер, сн. 54)

Подробности — `34_` §4.257 (Q253), S272; REPASS-документ, §97.

| # | Место | Итог |
|---|---|---|
| 1 | Фраза 1 в OCR NAC 2003 | Найдена снова — `WORDING_PARTIAL` |
| 2 | Фразы 2–4, p. 329 | В экземпляре IA, по метаданным, нет страниц начиная с p. 329 («Inherent missing pages 329-534»): проверить нельзя; HOLD |
| 3 | Вывод pp. 331–332 (Эскобедо, прим. 39) | Совпадает — `CONTEXT_OMITTED` в силе |
| 4 | Слова Чанга | Не Шрайнер — в силе |

**Вердикты S1–S5 не меняются.**

## 126. Раунд 175 (2026-11-17): самопроверка раунда 138 (Смолли, сн. 62)

Подробности — `34_` §4.258 (Q254), S273; REPASS-документ, §98.

| # | Место | Итог |
|---|---|---|
| 1 | Фрагменты WBC 51 к 1 Ин. 2:2 | Найдены снова — в силе |
| 2 | p. 40 | Shultz и Peterson; локатор теперь подтверждён для обеих ключевых фраз — `LOCATOR_VERIFIED` в силе |
| 3 | «Смолли p. 41» в HOLD | Заявка корпуса («WBC 40–41»), не сн. 62 — не расхождение; помечено в REPASS §80.4 |
| 4 | Посылка «мы» | `SOURCE_TENSION` (мягко) в силе |

**Вердикты S1–S5 не меняются.**

## 127. Раунд 176 (2026-11-17): самопроверка раунда 139 (Бокэм, сн. 52)

Подробности — `34_` §4.259 (Q255), S274; REPASS-документ, §99.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи, с. 13, сн. 52 | Совпадает — в силе |
| 2 | p. 240 | Watson, Shultz, Schreiner найдены снова — `LOCATOR_VERIFIED` в силе |
| 3 | IA `jude2peter0000bauc` | *Word Biblical Themes* (1990, 114 с.); в OL сведён в одну «работу» с WBC 50 — вывод «другая книга» в силе |
| 4 | Содержание p. 240 | HOLD |

**Вердикты S1–S5 не меняются.**

## 128. Раунд 177 (2026-11-17): самопроверка раунда 137 (Лютер, сн. 5)

Подробности — `34_` §4.260 (Q256), S275; REPASS-документ, §100.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи, с. 3, сн. 5 | Совпадает — в силе |
| 2 | *LW* 26:277 = WA 433 | В силе |
| 3 | *LW* 26:285 = WA 444b–445 | В силе; третий свидетель — Kim 2014 |
| 4 | «coniecit… delevit» (WA 445.30) | Может быть уже на *LW* 286; опора первой фразы — «sustulit» на *LW* 285 |
| 5 | «Concordia, 1976» | Каталог знает т. 26 только 1963 г.; не подтверждено, ошибкой не считается |

**Вердикты S1–S5 не меняются.**

## 129. Раунд 178 (2026-11-17): самопроверка раунда 136 (Шнукер, сн. 17)

Подробности — `34_` §4.261 (Q257), S276; REPASS-документ, §101.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи, с. 5, сн. 17 | Совпадает — в силе |
| 2 | Английский оригинал (1984, 2001, 2017) | ACCURATE — в силе |
| 3 | Русский перевод (ВикиЧтение) | Фраза и подпись найдены; статья следует переводу почти дословно |
| 4 | «Оба они содержат исповедание неограниченного искупления» | По полному тексту Шнукер о масштабе искупления не пишет — собственный вывод статьи |
| 5 | Рус. с. 312 | HOLD без изменений |

**Вердикты S1–S5 не меняются.**

## 130. Раунд 179 (2026-11-17): самопроверка раунда 135 (White, сн. 9)

Подробности — `34_` §4.262 (Q258), S277; REPASS-документ, §102.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи, с. 3, сн. 9 | Совпадает — в силе |
| 2 | Гессгусен на p. 255 | `LOCATOR_VERIFIED`, ACCURATE — в силе |
| 3 | 1 Ин. 2:2 «непосредственно перед» (REPASS §58) | **Поправка:** между ними блок текста; разбор может быть на p. 254 |
| 4 | Мф. 1:21 / Ин. 15:13 / Тит. 2:14 у Уайта | Не упомянуты в статье — `SOURCE_SAYS_MORE` (мягко) подкреплён |
| 5 | Печать 2005 г. | В каталогах нет; вероятно, допечатка |

**Вердикты S1–S5 не меняются.**

## 131. Раунд 180 (2026-11-17): самопроверка раунда 134 (Lewis & Demarest, сн. 83)

Подробности — `34_` §4.263 (Q259), S278; REPASS-документ, §103.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи, с. 26, сн. 83 | Совпадает — в силе |
| 2 | «design of the cross… to secure», p. 381 | `LOCATOR_VERIFIED`, ACCURATE — в силе |
| 3 | «Sufficiency» — «рамка самой статьи» (REPASS §57) | **Поправка:** «sufficient for all» у Л. и Д. есть — умеренные кальвинисты, прим. 57, p. 380 или раньше |
| 4 | «Более ранние авторы — достаточность» | `SIMPLIFIED` (мягко) — в силе, сужен |
| 5 | IA `integrativetheol0000dema_t1r1` | Сам т. 2, © 1990: текст печати 1990 г. виден (OCR) |

**Вердикты S1–S5 не меняются.**

## 132. Раунд 181 (2026-11-17): самопроверка раунда 141 (Гангел, сн. 51 и 55)

Подробности — `34_` §4.264 (Q260), S279; REPASS-документ, §104.

| # | Место | Итог |
|---|---|---|
| 1 | Текст статьи, с. 12–13 | Совпадает — в силе |
| 2 | BKC p. 870 | `LOCATOR_CONSISTENT` подкреплён: у Свиндолла p. 859, 867 (1:10), 869 (1:21) |
| 3 | Перевод сн. 55; вариант 3 | ACCURATE (класс C); `HEDGE_DROPPED` (мягко) — в силе |
| 4 | «Без акта вменения» | Новое: `IMPRECISE_TERM` (мягко) — у Гангела «did not apply it to themselves» |

**Вердикты S1–S5 не меняются.**

## 133. Раунд 182 (2026-11-17): самопроверка раунда 142 (Грин, сн. 56–57) и раунда 172

Подробности — `34_` §4.265 (Q261), S280; REPASS-документ, §105.

| # | Место | Итог |
|---|---|---|
| 1 | Текст сн. 56–58 (PDF, с. 14) | Совпадает |
| 2 | ἀγοράζω в LXX об исходе | Ни одного из 24 мест — `FACT_ERROR` в силе |
| 3 | «24 → 23» (раунд 172) | Моя ошибка: верно 24 (пропущено 2 Езд. 20:32). Исправлено, в том числе в §43 этого документа |
| 4 | Чья ошибка в сн. 57 | HOLD (Green p. 118 не открыт) |

**Вердикты S1–S5 не меняются.**
