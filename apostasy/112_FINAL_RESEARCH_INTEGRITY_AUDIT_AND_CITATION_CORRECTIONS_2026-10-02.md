# Серия «Отступники» — final Research integrity audit и citation corrections

**Дата:** 2026-10-02  
**Статус:** `FINAL INTEGRITY AUDIT COMPLETE / TWO READER-FACING CITATION DEFECT CLASSES CORRECTED / RESEARCH-SIDE CLOSED`  
**Audited HEAD:** `9da9c2615c563f20fffda6bd4bca851d86cc2c71` (== `origin/main`, session branch base)  
**Authority chain checked:** `README.md` → `111_...` → `110_...` → `109_...` → `108_...` → maps `103–107` → drafts `97–101` → `102_...`, `49A_...`  
**Correction commit:** `ded80da14a66f8d42a984e22213ef4e8cc81d398`

---

## 1. Executive verdict

Пост-фризовый integrity audit пяти частей выполнен полностью: authority chain, five-part integrity, final-state language, hard-text conformance, source policy, historical custody и pastoral locks.

> **RED research blocker не найден. Найдены и исправлены два класса reader-facing citation defects (Parts I/II/V) и один класс spelling defects. Ни один theological claim, wording lock, variant-control или source-annotation status не изменён.**

`111_...` остаётся authoritative Research → Product handoff. Единственное operational-изменение: Product обязан брать drafts `98`, `99`, `101` на/после коммита `ded80da14a66f8d42a984e22213ef4e8cc81d398` (указатели `111_...` сформулированы как “at/after commit”, поэтому остаются валидными).

---

## 2. Authority integrity (Block A) — PASS

| Проверка | Результат |
|---|---|
| HEAD / git status | `9da9c26…`; working tree clean на входе в audit |
| Более новые commits в любых refs | Отсутствуют (`git fetch --all`; `git log --all`) |
| README → handoff | README указывает на `111_...`; цепочка `111 → 110 → 109 → 108 → 103–107 → 97–101` подтверждена чтением файлов |
| Supersession chain | `85_...` supersedes `14_...` для initial reader architecture — зафиксировано в `111_...` §4; старые P0/missing-owner очереди явно superseded в `108_...` §1 |
| Возрождение старых очередей | Не выполнялось и не требуется: новый конфликт не обнаружен |
| Architecture | Пять частей в каноническом порядке; изменения архитектуры не производились |

---

## 3. Five-part integrity (Block B)

## 3.1. Семь wording patches — 7/7 подтверждены построчно

| # | Файл / строка | Фактический текст |
|---|---|---|
| 1 | `99_...`:1 | «…и разные траектории ухода от Бога» |
| 2 | `101_...`:554 | «…по одному текущему эпизоду самовольно объявлять окончательный Божий приговор…» |
| 3 | `97_...`:19 | «Иуда **испытал реальное мучительное сожаление о содеянном**» |
| 4 | `98_...`:87 | `## 10. Окончательное отвержение и самые крайние предупреждения` |
| 5 | `100_...`:15 | «На реальной истории Церкви видно, насколько практичны эти библейские различия.» |
| 6 | `100_...`:271 | «зрелый церковный лидер с многолетней христианской профессией…» |
| 7 | `101_...`:484, 488 | «обычными назначенными Богом средствами и практиками сохранения» / «…средствам и практикам» |

Ранее отмеченный «missing» Patch 7 был артефактом exact-string grep: фраза стоит в творительном падеже. Дефекта в корпусе не было.

## 3.2. Statuses, map pointers, titles

- Все пять drafts несут `PUBLICATION-CANDIDATE / SOURCE-ANNOTATED` и точный pointer на свою map (`97→103`, `98→104`, `99→105`, `100→106`, `101→107`).
- H1 всех пяти частей == route titles в `111_...` §3.
- Title/meta Parts I–V не сильнее body claim; запрещённая фраза «дороги к погибели» отсутствует.

## 3.3. Morphology / quotation discipline

Полный инвентарь не-русских лексем в reader-теле (без editorial notes):

| Draft | Greek / Hebrew |
|---|---|
| `97` | `μεταμεληθείς` |
| `98` | `πάλιν`, `ἐπιστρέφω`, `ἡγιάσθη`, `שוב` |
| `99` | `ἐπίγνωσις`, `מעל` |
| `100` | — |
| `101` | — |

Оригинальные формы — единичные, функциональные, на зафиксированных hard nodes. Формы проверены и корректны.

- Прямых цитат современных комментаторов и пуритан в drafts нет (quotation-free статус сохранён).
- TGC упоминается только в разделах `Editorial source notes — remove/convert before publication` (`98`:328, 336; `99`:601) — и только как запрет на platform-authority use.

## 3.4. Findings

| ID | Severity | Существо | Статус |
|---|---|---|---|
| F1 | `P1-READER-CITATION` | Part II: падение Соломона было привязано к «1 Цар. 11» — при русской (Синодальной) нумерации это 1 Самуила; должно быть «3 Цар. 11» | `FIXED` (`ded80da`) |
| F2 | `P1-READER-CITATION` | Parts I и V: псалмы цитировались только по масоретской нумерации («Пс. 78 и 106», «Пс. 78/106»), что уводит читателя Синодальной Библии к другим псалмам | `FIXED` (`ded80da`) |
| F3 | `P2-SPELLING` | «perseverence» → «perseverance» (98 ×2, 99 ×1, 101 ×3) | `FIXED` (`ded80da`) |
| F4 | `P2-DOCUMENTATION` | Map `107` использует §-метки, дрейфующие относительно нумерации draft `101` (например, map §16 = office restoration, тогда как draft §16 = settled repudiation) | `DOCUMENTED / NO REWRITE` |

### F1 — детализация

В том же draft `99` статьи «1 Цар. 13» и «1 Цар. 15» обозначают 1 Самуила, «4 Цар. 17» — 2 Царств. Следовательно «1 Цар. 11» для Соломона было внутренне противоречивой ссылкой и указателем на чужой эпизод. Исправлено на «3 Цар. 11» — согласовано с русской конвенцией dossier `84_...` («3 Цар. 11:26–40»). Исправлены оба вхождения (строки 238 и 264).

### F2 — детализация

Русский Синодальный Псалтирь использует LXX-нумерацию, поэтому масоретские Пс. 78 и 106 = Синодальные Пс. 77 и 105. Использована уже принятая в русскоязычных документах корпуса двойная нотация (`19_...`, `23_...`): «Пс. 77(78) и 105(106)». Исправлены `98`:101 и `101`:429. Тождество псалмов проверено по содержанию («соединяют забывание с неверием»: Пс. 78:11; 106:13).

### F4 — детализация

Содержательные freeze-claims map `107` присутствуют в draft `101` (проверено по разделам); дрейфуют только внутренние §-метки. Как «claim inventory» map остаётся пригодной guardrail; переписывание замороженного артефакта ради номеров не выполнялось, чтобы не создавать churn. Зафиксировано здесь явно.

---

## 4. Final-state audit (Block C) — PASS

| Персона / группа | Найдено в drafts | Вердикт |
|---|---|---|
| Иуда Искариот | `98` «погибает»; `99` «terminal case с высокой уверенностью»; `97` «уходит в погибель» | `OK` — narrator/canonical finality (Мф. 26:24; Ин. 17:12; Деян. 1:25) |
| Пётр | восстановлен; «падение не стало последней главой» | `OK` |
| Саул | «тяжёлый retrospective», отказ от «безоговорочного prooftext final individual damnation» | `OK` — final state not narrated |
| Соломон | «финал вечной судьбы не проговаривается» | `OK` (F1 исправлен) |
| Димас | «не говорит, что Димас умер в этом состоянии» | `OK` |
| Иеровоам / 4 Цар. 17 | corporate/institutional judgment; «не раскрывает автоматически вечное состояние каждого» | `OK` |
| Именей, Александр, Филит | severe discipline с corrective purpose; doctrinal contagion | `OK` — no eternal verdict invented |
| Лжеучители 2 Пет. 2 / Иуды | сильный язык сохранён; Иуд. 19 «Духа не имеющие» | `OK` — по тексту послания |
| Валаам | дар и корысть; «дар не является моральным иммунитетом» | `OK` |
| Исторические кейсы (Плиний, Квинт, Нин/Клементиан/Флор, Юлиан, Кранмер, Спира) | везде epistemic guardrails: profession/denial/repentance ≠ regeneration/decree | `OK` |
| Обратимые блуждающие (Иак. 5; Гал. 6; 2 Тим. 2) | явно отнесены к recoverable | `OK` |

---

## 5. Hard-text audit (Block D) — PASS

| Lock | Где в drafts | Соответствие |
|---|---|---|
| Luke 8:13 | `98` §2.4, §12 | «временем верует» не переписано; модели раскрыты; `πιστεύω` не объявлен решающим |
| Hebrews 6 | `98` §2.5, §7, §10 | опыты не тривиализованы; контроль 6:9 удержан; prior-saving статус назван спорным |
| Hebrews 10:29 | `98` §7, §10 | `ἡγιάσθη` назван и не спрятан; referent dispute признан |
| 2 Peter 2 | `98` §7; `99` §12 | bought / knowledge / escape / defeat / dog-sow — разведены; «купленный Владыкой» вынесен в отдельный вопрос |
| Jude | `98` §9; `97` §10; `101` §1 | variant-safe; «ровно три класса» отвергнуты как догма |
| Revelation 3:5 / 22:14 / 22:19 | `98` §10 | 3:5 — text-stable, спор экзегетический; 22:14 — вариант раскрыт; 22:19 — tree of life / holy city |
| 1 Peter 2:25 | `98` §1 | «возвратились» не превращено в схему «спасён → потерян → снова спасён» |
| Galatians 4:9 | `98` §1 | «снова» = возврат к структуре рабства |
| John 6:64 (Judas) | `97` §4; `99` §1; `98` §2.5 | согласовано с `02_...` и `103_...` §4: контроль pre-betrayal статуса |
| 1 John 2:19 / James 5 | `98` §8; `97` §8; `101` §1, §8 | обе категории разведены и удержаны |
| 2 Tim 2:11–19, 24–26 | `97` §7, §9; `99` §8; `101` §1, §4, §7 | и warning, и divine faithfulness, и corrective hope |
| 1 Cor 10; Rev 2–3 | `98` §§3, 12; `101` §§12, 13, 19 | warning-as-means без карнавальной безопасности |

Hard-text прозы, противоречащей dossiers `60–69`, `91–92`, не найдено.

---

## 6. Source-policy audit (Block E) — PASS

- TGC не используется как authority; упоминания только как правило «не использовать».
- Слабых aggregator-источников в reader-прозе нет (проза вообще без внешних ссылок; source-note конверсия — задача Product по `111_...` §7).
- Direct quotes отсутствуют; следовательно, нет quote-without-locator дефектов.
- Puritan claims `101` §10, §14 прослежены до разделов `89_...`: Watson — false peace (`A Body of Divinity`, CCEL locator); Owen — gradual decay и preservation через appointed means (ch. XII–XIII); Brooks — bait/hook и anti-despair; Sibbes — weak grace / bruised reed. Misattribution не найдено.
- Platform-brand замены экзегезы не обнаружено.

## 7. Historical audit (Block F) — PASS

Part IV сверен с `94_...` по каждому кейсу: Плиний (c. AD 112; `fuisse … desisse`), Квинт (`Martyrdom of Polycarp` 4; final state unknown), Деций/lapsi (Киприан, `De Lapsis`; две крайности), Нин/Клементиан/Флор (ANF Epistle 52; три года покаяния; conciliar consideration), Новациан (severity без культа безнадёжности), Юлиан (собственные тексты + Аммиан; крещение/чтец — атрибутированные детали), Кранмер (1556 printed recantations + финальный reversal; MacCulloch), Спира (Gribaldi 1549; Overell/MacDonald source criticism). Ни один кейс не превращает архив в доказательство regeneration/election; Foxe/Gregory/поздние Spiera-retellings не выступают единственным нейтральным свидетелем.

## 8. Pastoral audit (Block G) — PASS

Part V удерживает: сильное предупреждение; реальное восстановление; отсутствие ложной уверенности; отсутствие преждевременного отчаяния; дисциплина ≠ безошибочное объявление декрета; прощение/общение/доверие/должность разведены; слабый/сокрушённый ≠ final apostate; защита стада от разрушительных учителей; clinical mental-health кризис не сведён к моральной схеме; универсальные сроки восстановления в должности не изобретены.

---

## 9. Residual AMBER (не RED, не блокирует handoff)

1. Точная политика русского библейского перевода и терминологическая нормализация англицизмов reader-прозы (`saving union`, `final state`, `terminal case` и т. п.) — Product/editorial уровень; map `103` §5.1 частично не мигрирована сознательно, поскольку bulk-переписывание terminology = style rewrite.
2. Формат reader-facing source/endnotes — Product конвертирует по `111_...` §7.
3. Direct quotations — только при edition/page freeze; для v1 не требуются.
4. Office-restoration procedures и family appendix — отдельное исследование, если понадобится.

## 10. Operational consequences

- Product content source of truth: `98`, `99`, `101` — на/после `ded80da14a66f8d42a984e22213ef4e8cc81d398`; `97`, `100` — без изменений (их freeze-коммиты остаются в силе).
- Все locks `111_...` (§10–§15) действуют без изменений.
- Product write не выполнялся; `FedorMilovanov/gb-is-my-strength` не изменялся.

## 11. Closure

> **Research-side работа закрыта: authority chain проверена на реальном HEAD, пять частей согласованы с maps и technical dossiers, выявленные reader-facing citation defects исправлены, final-state/variant/source/pastoral locks подтверждены. `111_...` остаётся authoritative Research → Product handoff.**

**Research status: `CLOSED / HANDOFF READY / NO RED BLOCKER`.** Следующий этап — Product intake в `gb-is-my-strength`, не новый Research.
