# Агент 2 — аудит строгой аргументации «Кальвин учил определённому искуплению»: где логический шаг доказан, а где нет

**Дата:** 2026-11-17
**Исполнитель:** Agent 2 (ARENA), режим `ONE_SHARED_GOAL`, координатор MAX.
**Ветка:** `arena/0fbd0e42-research`, база `5fab12abd16246a0ff5fab558f11001304f2e970` (`origin/main`).
**Статус:** `RESEARCH / EVIDENCE DELTA / NOT PUBLICATION-READY`. `RIGHTS_HOLD`, `PUBLICATION_HOLD` и `EXEGETICAL_HOLD` родительского корпуса этим документом не снимаются.
**Владение файлами.** Создан только этот файл. Общие главы, `synthesis/02_CONFLICT_LEDGER.md` (в том числе C-17), `synthesis/drafts/article16_*`, `13_`, `15_`, `fathers/16_`, матрица Agent 6 и `docs/research/atonement/*` **не редактировались**. Поправки к ним вынесены в §7 как предложения для MAX. Перед началом работы я проверил открытые PR: 547, 546, 379 и 287–289 не касаются ИСКУПЛЕНИЕ/, поэтому конфликта владения нет.
**Чего здесь нет.** Пять пунктов не передоказываются, и параллельная систематика не строится. Уже полученные корпусом результаты (достаточность/действенность, hard-text cards, особая импетрация, предложение и применение) принимаются как данность. Проверяются только логические переходы.

---

## 0. Краткий ответ

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
| L1 | Кальвин против Хесхузия, *Dilucida explicatio* (1561) | *Opera omnia*, Amsterdam 1667, т. VIII, `bub_gb_6COCD48cJ90C` | скан с. **759** | A1 |
| L1e | то же, англ. | CTS *Tracts relating to the Reformation*, vol. 2 (Beveridge), `tractsreformatio02calvuoft` | **527** (лист 531) | B1 |
| L2 | *De aeterna Dei praedestinatione* (1552), раздел против Георгия Сицилийского | 1667, т. VIII, тот же скан | скан с. **628** | A1 |
| L2e | то же, англ. | H. Cole, *Calvin's Calvinism* (1856), `calvinscalvinis00colegoog` | **150–151** | B1 |
| L3 | Комм. на Рим. 5:18 | CTS *Romans* (Owen, 1849), `commentariesonth00calvuoft` | **211** (комментарий и лат. сноска 3); примечание «— Ed.» на **212** | B1 + лат. A1 в сноске |
| L4 | Комм. на Рим. 8:34 («who intercedes») | там же | **325** (по указателю: «Intercession… of Christ, how to be understood, 325») | B1 |
| L5 | Комм. на Ин. 17:6, 9 | CTS *John*, vol. 2 (Pringle, 1847), `commentaryongosp02calvuoft` | 17:6 — **170**; 17:9 — **172**; «Christ prays for the elect only» — **173** (лист = индекс, калибровка как у L3) | B1 |
| L6 | Комм. на 1 Ин. 2:2 | CTS 1855, `commentariesonca00calv` | **173** (уже в `13_` §2.2) | B1, лат. CO 55:310 в `fathers/16_` §2.2 |
| L7 | Оуэн, *Death of Death*, кн. I, гл. VII | Goold, *Works* X (1850), `worksofjohnowe185010owen` | заголовок главы — индекс 198 (кн. I = с. 157–199 по `14_`) | A2 (не Кальвин) |

### 2.1. Дословные тексты, на которые опирается матрица

**L1, 1667 с. 759.** Нормализовано: long-s → s, лигатуры раскрыты.
> «…Et quando tam mordicus verbis adhaeret, scire velim quomodo Christi carnem edant impii, pro quibus non est crucifixa, et quomodo sanguinem bibant, qui expiandis eorum peccatis non est effusus. Fateor quod dicit, adesse ut severum judicem… Sed aliud est comedi, aliud esse judicem.»

- CTS p. 527: «I should like to know how the wicked can eat the flesh of Christ which was not crucified for them? and how they can drink the blood which was not shed to expiate their sins?»
- Несущая аксиома в том же споре (CTS): «Christ, considered as the living bread and the victim immolated on the cross, cannot enter any human body which is devoid of his Spirit».

**L2, 1667 с. 628.** Нормализовано.
> «…Ne valeat in praesens communis illa solutio: Christum sufficienter pro omnibus passum esse, efficaciter tantum pro electis. Magna illa absurditas, ob quam plausum sibi inter suos gregales Monachus quaesivit, apud me nihil habet momenti. Per quascunque mundi plagas dispersi sint fideles, expiationem Christi morte partam ad eos Joannes extendit. Id certe non obstat, quominus reprobi in mundo electis permixti sint. Controversia etiam caret, Christum expiandis totius mundi peccatis venisse. Sed confestim occurrit… Ut quisquis credit… Nec vero qualis sit Christi virtus, vel quid per se valeat, nunc quaeritur: sed quibus se fruendum exhibeat… Quamvis per ipsum offeratur omnibus reconciliatio, peculiare tamen esse electis beneficium, ut in vitae societatem colligantur. Quanquam dum omnibus offerri dico, non ita accipio, quasi ad omnes legatio illa perveniat…»

- Cole p. 150: «we will not permit the common solution… Christ suffered sufficiently for all men; but effectually for his elect alone».
- Cole p. 151: «although reconciliation is offered unto all men, through Him; yet… the great benefit belongs peculiarly to the elect».
- **Добавка переводчика (не Кальвин):** у Cole на с. 151 стоит «but that it is not sealed indiscriminately on the hearts of all… so as to be effectual in them». В процитированной латыни соответствия нет.
- **Локатор CO 8:336** — традиционный, в этой сессии **не сверен**. Цитировать: 1667 с. 628 + Cole с. 150–151.

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
| **S1-b** | те же | Значит, у смерти Христа **нет иной** спасительной цели или отношения к неизбранным | **P-coext**: объём импетрации (за кого принесена жертва) = объём намеренного применения. Иначе: что не применено, то и не было приобретено/предназначено | Кальвин сам разделяет «quid per se valeat» и «quibus se fruendum exhibeat» (L2) и говорит «passus pro peccatis totius mundi» (L3). P-coext у него не высказана; в явном виде она у Оуэна (L7) | `WEAK_INFERENCE` |
| **S1-c** | Inst II.17.4 («cursed… righteousness»; Battles 1:532 — не II.16.5–6, как иногда цитируют) | Удовлетворение есть реальная замена, поэтому оно не может быть «впустую» за неспасённых | P-coext + **P-noDouble**: реальная замена исключает вторичное, обусловленное отношение | Строка доказывает реальность замены для «нас» (верующих), но не говорит, что «нас» исчерпывает возможный объём | `WEAK_INFERENCE` |
| **S2-a** | Ин. 17:9 (L5, с. 172–173) | Ходатайство Христа — только за избранных | — | Лк. 23:34. Кальвин отвечает сам: даже молитва «за всех» в конечном счёте «limited to the elect» | `EXPLICIT` |
| **S2-b** | Рим. 8:34 (L4, с. 325) | Ходатайство есть непрерывно предъявляемая сила смерти и воскресения | — | Нет | `EXPLICIT` (**NEW_DELTA** для S2) |
| **S2-c** | S2-a + S2-b | Значит, предъявляемая действенность смерти ограничена избранными | S2-a, S2-b | Это вывод о **действенности/применении**, а не об объёме жертвы как такового | `STRONG_INFERENCE` (собран из двух явных мест Кальвина) |
| **S2-d** | S2-c + L2/L3 | Кальвин **исключает** различение «всеобщее основание призыва (жертва за весь мир, предложение всем) + особое ходатайство» | **P-same-object** (Оуэн, L7) или отказ от «двойного ходатайства» (Утрехт 1620, Acta pp. 122–123, A2, матрица Agent 6, A.2) | Кальвин явно держит оба полюса: «offertur omnibus reconciliatio» / «peculiare electis beneficium» (L2), «propounded to all / not extended to all» (L3). Тезиса «жертва и ходатайство коэкстенсивны» в его проверенных текстах нет. Цитата «Inst 2.16.16» в `32_` — склейка (`QUOTE_RISK`, уже отмечено там) | `WEAK_INFERENCE` → `UNDETERMINED`. Различение `COMPATIBLE` с Кальвиным, но им **не сформулировано**. Кальвин также не постулирует второе, общее ходатайство за отверженных |
| **S3-a** | Хесхузий (L1, с. 759) | Плоть Христа не распята за нечестивых, кровь не пролита для искупления их грехов | — | — | `EXPLICIT` (в этой ограниченной формулировке). **PRIMARY_VERIFIED** |
| **S3-b** | L1 + аксиома о Духе | Это утверждение Кальвина об **объёме** жертвы, в оуэновском смысле | **P-ctx**: евхаристический вопрос («как едят…») переносим на учение об объёме. Плюс **P-sincere**: фраза — не довод ad hominem | (1) Контекст — manducatio impiorum; Христос взят «как духовная пища». (2) Рамка ad hominem: «quando tam mordicus verbis adhaeret». (3) Та же лексика «expiandis… peccatis» утверждается о «totius mundi» в L2 того же тома. (4) Довод работает и при чтении «не распята за них **действенно / как пища**» | `STRONG_INFERENCE` в лучшем случае; спорно. Не `EXPLICIT` для оуэновского объёма |
| **S3-c** | «Christum solis electis passum esse» (`01_`:890); «pro solis electis passus est», CO 9:524 (`22_` #11/#998) | Кальвин дословно говорил «только за избранных» | Наличие фразы в тексте | В 1667, т. VIII, по OCR не найдено: «solis electis», «folis electis», «femper dixi» — 0 совпадений. В CTS Tracts II: «always said» — 0; «elect alone» — только о вере (лист 136). Два целевых прохода безрезультатны → `STOP_DISCOVERY` | `INVALID` как verbatim (до предъявления скана). Отсутствие в OCR — не доказательство отсутствия в тексте, но метка «Verified» в `22_` не обоснована |
| **S4-a** | 1 Ин. 2:2 (L6; CO 55:310) | «Весь мир» здесь — верующие по всему миру, без отверженных | — | — | `EXPLICIT` |
| **S4-b** | то же | Кальвин выводит партикулярный объём **через** формулу «достаточно/действенно» | Что формула — его аргумент здесь | Он называет формулу «истинной», но «не подходящей к этому месту». В L2 он её «in praesens» откладывает | `INVALID` (формулу нельзя вменять как его довод) |
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
| `docs/research/atonement/02_…controversies.md` #17 | «qui non est effusus in peccatorum eorum expiationem», CO 9:484 | Исправить вторую половину по L1; CO 9:484 — `LOCATOR_UNVERIFIED`, добавить 1667 с. 759 |
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
1. **Хесхузий — PRIMARY_VERIFIED.** 1667, т. VIII, с. 759; CTS Tracts II p. 527. Wording исправлен. Вердикт: `EXPLICIT` в ограниченной формулировке и не более чем `STRONG_INFERENCE` для оуэновского объёма.
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
- английское «sealed… effectual» у Cole с. 151 как слова Кальвина.

**EXACT_LOCATORS:** см. §2 (L1–L7). Не сверены: CO 8:336, CO 9:484, CO 9:524, CO 49:100 по скану CO; латынь Рим. 5:18 сверена только по сноске CTS.

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
