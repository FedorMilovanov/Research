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

**EXACT_LOCATORS:** см. §2 (L1–L7) и §9.1. В волне 2 по скану CO сверены CO 9:484, CO 9:485 и CO 8:336. CO 9:524 как locus «solis electis passus» не подтверждён (§9.3). CO 49:100 по скану CO не сверен (CR 77 в IA не найден); латынь Рим. 5:18 сверена только по сноске CTS.

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
| CO-4 | 1 Ин. 2:2, «Ego quamquam verum… nego tamen praesenti loco quadrare» | `operaquaesupersu0083calv` (CR 83 = CO 55), лист 167, правая колонка | традиционно **CO 55:310**; текст сверен, колонка **не откалибрована** (номера страниц в json этого тома интерполированы) | — | A1 (текст) / `LOCATOR_APPROX` (колонка) |

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
