# Каноны Дорта (1619), Вторая глава — исторический контроль

**Дата:** 2026-10-13. **Ось:** `offer` + `extent` (обе).

**Статус:** **исторический контроль, не свидетельство первого порядка.** Бриф
относит Дорт к тому же классу, что и Кальвина (`15_`/`16_` верхнего корпуса):
он показывает, как традиция читала эти тексты, и **не является экзегезой**.
Вердикта нет. `EVIDENCE_HOLD` не снят.

---

## 13.0 Локация и права

| Параметр | Значение |
|---|---|
| Документ | Каноны Дорта, Национальный синод в Дордрехте, 1618–1619; Вторая глава «О смерти Христа и искуплении людей ею» |
| Перевод | **received English translation** — английский перевод, находящийся в общественном достоянии |
| Откуда прочитано | https://www.covenantlondon.org/canons-of-dort-1619 (2026-10-13); текст II.5 сверен по трём независимым публикациям одного перевода |
| `evidenceClass` | **`B1`** — вторичный исторический документ. **Не `A1`**: это не греческий текст и не перевод Писания |
| `accessState` | `acquired-quotation` — процитированы II.1–II.9 и Rejection II.1–II.5 |
| `locatorState` | **`secondary-only`** — PD-статус перевода подтверждён только вторичными публикациями, а не библиографической записью первого порядка |
| `rightsState` | текст перевода — PD. **Ссылки на Писание на странице даны в ESV и не цитируются** (ESV под правами) |
| `publicationState` | `NOT-APPROVED` |

**Чего здесь нет.** Полный текст Канонов в Git не кладётся: нужен был один
раздел как контроль, а не копия исповедания. Перевод 1986 года (CRC, с латыни)
**не использован** — он современный и под правами; использован только PD-перевод.
Дорт II.5 в переводе 1986 года звучит иначе («without differentiation or
discrimination») — расхождение переводов здесь содержательное, и подменять их
нельзя.

## 13.1 Четыре статьи, которые образуют структуру

Цитаты — received English translation.

**II.3 — ценность.** «The death of the Son of God is the only and most perfect
sacrifice and satisfaction for sin, and is of infinite worth and value,
**abundantly sufficient to expiate the sins of the whole world**.»

**II.5 — опубликование.** «Moreover, the promise of the gospel is, that
whosoever believeth in Christ crucified, shall not perish, but have everlasting
life. This promise, together with the command to repent and believe, ought to be
declared and published **to all nations, and to all persons promiscuously and
without distinction**, to whom God out of His good pleasure sends the gospel.»

**II.6 — отказ.** «And whereas many who are called by the gospel do not repent
nor believe in Christ, but perish in unbelief, this is **not owing to any defect
or insufficiency in the sacrifice** offered by Christ upon the cross, but is
wholly to be imputed to themselves.»

**II.8 — действенность.** «…the quickening and saving efficacy of the most
precious death of His Son **should extend to all the elect**… that Christ by the
blood of the cross… should effectually redeem out of every people, tribe,
nation, and language, **all those, and those only, who were from eternity chosen
to salvation** and given to Him by the Father…»

**Rejection II.5** отвергает учение, «that all men have been accepted unto the
state of reconciliation and unto the grace of the covenant», со ссылкой на
Еф 2:3 («we are by nature children of wrath»).

## 13.2 Сопоставление с тем, что под-корпус вывел из греческого

Карточка `10_NT_OFFER_AXIS_CARDS.md` строилась **независимо**, по греческому
тексту, без обращения к Дорту. Структуры совпали по четырём пунктам:

| Вывод `nt/10_` из греческого | Статья Дорта |
|---|---|
| Объём приглашения ≠ объём покупки (Мф 22:3 против 22:14; Лк 14:17 против 14:24) | II.5 против II.8 |
| Отказ приписан адресату, никогда не предложению | **II.6 дословно** |
| Круг адресата задан меткой, а не списком | II.8 «out of every people, tribe, nation, and language» |
| Достаточность ≠ действенность (природа дара против объёма) | **II.3 против II.8** |

**Что это даёт.** Совпадение не подтверждает греческий разбор — Дорт не
свидетель первого порядка. Оно даёт другое: **структура, к которой пришёл
разбор, не является изобретением разбирающего**. Она уже была сформулирована
в 1619 году и именно в таком виде — достаточность / опубликование / отказ /
действенность как четыре разных утверждения, а не как одно.

**Rejection II.5 особенно важен для §8.3.** Верхний корпус перечисляет
двенадцать локусов, работающих **против обоих лозунгов сразу**. Дорт делает то
же самое на уровне исповедания: II.5 утверждает всеобщее опубликование,
Rejection II.5 отвергает всеобщее примирение. Оба утверждения держатся вместе,
и ни одно не сводится к другому.

## 13.3 Расхождение переводов — его нельзя замазывать

| | received English (PD, использован) | CRC 1986 (не использован) |
|---|---|---|
| II.5 | «to all nations, and to all persons **promiscuously and without distinction**» | «**without differentiation or discrimination** to all nations and people» |

«Promiscuously» — термин XVII века, означающий «без разбора, всем подряд»;
в переводе 1986 года он заменён нейтральным. Для истории доктрины это
существенно: старый перевод сохраняет спорный термин, новый его сглаживает.
Под-корпус цитирует только PD-перевод и помечает это явно.

## 13.4 Что карточка не доказывает

Не доказывает ограниченного искупления — Дорт **утверждает** его, а утверждение
исповедания не является экзегезой; `EVIDENCE_HOLD` остаётся. Не доказывает и
обратного. Не доказывает, что Павел, Иоанн или автор Евреям читали эти тексты
так же: Дорт — 1619 год, а не первый век. Не заменяет собой OPC 1948 (доклад
Мюррея о свободном предложении), который **по-прежнему не получен** и остаётся
открытым пунктом в `05_SOURCE_REGISTRY`. И главное: Дорт здесь полезен именно
тем, что **не решает вопрос за нас** — он показывает форму, в которой вопрос
можно держать открытым, не сваливаясь ни в один из двух лозунгов.
