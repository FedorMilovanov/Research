# 1 Коринфянам 11:2–16 — третий аудит: open-web exhaustion, latest editions и provenance крайних моделей

**Дата:** 2026-08-10  
**Статус:** `THIRD-AUDIT / OPEN-WEB-EXHAUSTION / LATEST-EDITION-CONTROL / EDGE-PROVENANCE / CONSERVATIVE-WEIGHTED / FAIL-CLOSED / RESEARCH-ONLY / PUBLICATION-HOLD`  
**База:** `main@a353b6d2b83553a60548bf2f9d625c54ab2d5f88`

## 1. Зачем нужен третий проход

Второй аудит уже расширил карту до 45 commentary/reception nodes + 25 специализированных scholarly nodes. Третий проход не считает новые URL как новые «голоса». Его задача — сделать три вещи, которые влияют на качество дальнейшего исследования:

1. **исчерпать открытый web до просьбы пользователю о книге**;
2. **проверить latest edition**, чтобы не просить устаревшее издание как главный источник;
3. **привязать редкие/экзотические версии к точным авторам и академическим loci**, чтобы не пересказывать карикатуры.

Жёсткое правило:

```text
OPEN-WEB-SUFFICIENT => USER_ACQUISITION = NO
FULL-PAGE-CONTEXT_STILL_CLOSED => USER_ACQUISITION = OPTIONAL/PRIORITISED
EXOTIC_MODEL_FOUND => HISTORY/DEBATE NODE, NOT EQUAL-WEIGHT THEOLOGY
```

## 2. Latest-edition correction: Garland

Предыдущая очередь ставила David E. Garland, *1 Corinthians* (BECNT, 2003), pp. 505–532, как P0. Это библиографически уже не оптимально.

### Исправление

- **David E. Garland, *1 Corinthians*, 2nd ed., BECNT, Baker Academic, 2025** — теперь **основной P0 Garland witness**.
- 2003 edition сохраняется только для **edition-delta comparison**: что Garland изменил за два десятилетия.
- Официальные/книжные метаданные 2025 edition подтверждают отдельный раздел `VII. Headdress in Public Worship (11:2–16)`.
- Старые locator `pp. 505–532` относятся к первой редакции и **не должны автоматически переноситься** на 2025 edition.

**Policy:** если пользователь имеет новую 2nd edition, нужен именно полный section 11:2–16 + footnotes. Старую 2003 просить только если нужно сравнить revisions.

## 3. Новый current-control commentary: Michael J. Gorman 2025

- Michael J. Gorman, *1 Corinthians: A Theological, Pastoral, and Missional Commentary* (Eerdmans, 2025).
- Это **не замена** Thiselton/Fee/Garland/Ciampa-Rosner по technical Greek.
- Роль: свежий post-2024 theological/pastoral control, особенно для contemporary application и ecclesiology.
- Пока позиция Gorman по каждому спорному узлу 11:2–16 не прочитана page-level, нельзя приписывать ему конкретное решение.

Калибровка: `BIBLIOGRAPHICALLY VERIFIED / CURRENT CONTROL / PAGE-LEVEL HOLD`.

## 4. Open-web exhaustion: что больше НЕ надо просить у пользователя первым

### 4.1 Ambrosiaster — узел «ангелы = епископы» уже доступен

Для конкретного historical claim v.10 достаточно прямого атрибутированного open-web excerpt:

- Ambrosiaster: veil signifies power; `angels` interpreted as bishops.
- Этот exact claim уже можно фиксировать как late-antique reception node без просьбы о полном IVP томе.

**Следствие:** Ambrosiaster/Bray full volume больше не P1 user-acquisition target для самого тезиса `angels=bishops`. Full volume нужен лишь при желании сделать полную late-antique page-level катену или публикационную цитату с контролем контекста.

### 4.2 Lucy Peppiatt — core thesis доступен достаточно для map-level критики

Google Books/издательские preview дают:

- тезис о dialogue/quotation-rhetorical reading;
- структуру книги;
- explicit proposal, что Corinthian male leadership навязывал женщинам coverings и что Paul в значимой части спорит с их позицией.

**Следствие:** для честного описания модели книгу у пользователя просить не надо. Full book остаётся optional только если нужен **strongest-form page-by-page rebuttal с footnotes**.

### 4.3 Fee 1987 first edition

Open Library / Internet Archive catalog routes и публичные preview делают первую редакцию широко отслеживаемой. Но **Fee Revised 2014** остаётся отдельным P0, потому что именно revision должна контролировать его финальную позицию.

### 4.4 Garland 2003

Open Library/Google Books preview и подробные ToC/loci позволяют самостоятельно контролировать bibliographic layout первой редакции. Просить старый том как основной больше не нужно.

## 5. Что после open-web sweep всё ещё реально закрыто и ценно

Следующие позиции остаются честными acquisition targets, потому что open web даёт metadata/snippets/TOC, но не полный нужный section + footnotes:

1. **Anthony C. Thiselton, NIGTC (2000), 11:2–16** — P0.
2. **Gordon D. Fee, NICNT Revised (2014), full 11:2–16 + notes** — P0.
3. **David E. Garland, BECNT 2nd ed. (2025), full 11:2–16 + notes** — P0 latest-edition.
4. **Roy E. Ciampa & Brian S. Rosner, PNTC (2010), full 11:2–16 + notes** — P0.
5. **Joseph A. Fitzmyer, Anchor Yale Bible (2008), full 11:2–16 + notes** — P0 pericope-level integration.
6. **Bruce W. Winter, *Roman Wives, Roman Widows* (2003), ch. 5, pp. 77ff** — P0 historical thesis in strongest full-book form.
7. **Gregory J. Lockwood, Concordia Commentary (2000), full 11:2–16** — P1 conservative-confessional technical control.
8. **Wolfgang Schrage, EKK VII/2, 11:2–16** — P1 German critical adversarial control.
9. **Judith L. Kovacs, *The Church's Bible: 1 Corinthians*, 11:2–16** — P1 patristic breadth beyond already-open excerpts.
10. **Michael J. Gorman 2025, 11:2–16** — P1 current application/theological control if available, not technical P0.

## 6. Exact provenance крайних/неведущих моделей

Ниже модели фиксируются потому, что они реально опубликованы. Их включение **не означает**, что они равновероятны консервативному синтезу.

### 6.1 Jerome Murphy-O'Connor — hairstyle + sexual-role thesis

**Source:** `Sex and Logic in 1 Corinthians 11:2–16`, later collected in *Keys to First Corinthians* (OUP, 2009), pp. 142–158.

Позиция в abstract:

- отрывок якобы не о женском veiling;
- мужские длинные волосы трактуются как знак active male homosexual role;
- женская неправильная причёска / короткие волосы связываются с masculine/lesbian presentation;
- creation argument защищает sexual differentiation;
- vv.11–12 используются для affirming equality.

**Калибровка:** `D/C-low / PUBLISHED EDGE MODEL`. Нельзя превращать древние данные о hairstyle/sexual signalling в универсальный lexical equation для 1 Cor 11.

### 6.2 Murphy-O'Connor — human messengers in v.10

**Source:** `1 Corinthians 11:2–16 Once Again`, *Keys to First Corinthians* (2009), pp. 159–181.

В revised proposal:

- `ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς` читается как woman exercising control over her head / arranging hair;
- `angels` предлагается понимать как human messengers from other churches;
- chapter separately weighs `κεφαλή` as ruler/source/person etc.

**Калибровка:** human-messenger reading = `D/C-low history/debate`; полезна именно как реальный академический вариант.

### 6.3 Kirk R. MacGregor — homosexuality-prohibition thesis

**Source:** `Is 1 Corinthians 11:2–16 a Prohibition of Homosexuality?`, *Bibliotheca Sacra* 166:662 (2009), 201ff.

Позиция:

- `κατὰ κεφαλῆς ἔχων` понимается как long hair, не garment;
- мужчинам запрещаются long hair, женщинам short hair;
- gender-crossing appearance связывается с homosexuality.

**Калибровка:** `D/C-low`. Исторически интересная консервативная попытка, но далеко не leading material-covering reading.

### 6.4 Quotation/refutation внутри 11:3–16

**Source:** Alessandra Castilho da Costa, `Identifying Quotations in 1 Corinthians 11:3-16` (recent linguistic argumentative-analysis article).

Proposal:

- vv.4–9 могут представлять Corinthian viewpoint/quotation, который Paul затем refutes.

**Калибровка:** `D/C-low / RECENT LINGUISTIC EDGE MODEL`. Нужна отдельная проверка Greek discourse markers; не читать как установленную структуру письма.

### 6.5 Interpolation of 11:3b–15

Timothy Milinovich proposed interpolation of 11:3b–15 (parallel to his approach to 14:34–35). Sławomir Torbus published a direct critique arguing that the passage belongs organically to the performative/concentric structure of 1 Corinthians.

**Калибровка:** interpolation = `D/C-low`, потому что:

- нет достаточного manuscript omission-base для удаления 11:3b–15;
- модель зависит прежде всего от literary/theological reconstruction;
- она должна быть известна как scholarly edge case, но не включена в publication-level alternatives как равновесная.

### 6.6 Mark Finney — honour/status male-covering reconstruction

**Source:** `Honour, Head-coverings and Headship: 1 Corinthians 11.2-16 in its Social Context`, JSNT 33.1 (2010).

Proposal:

- higher-status male Corinthians могли использовать head attire для сохранения status distinctions;
- female covering защищает communal honour в потенциальном присутствии outsiders.

**Калибровка:** `B/C historical reconstruction` — сильнее чистой экзотики, но всё равно реконструкция local trigger, а не A-level текстовый факт.

## 7. Rare `angels` map — provenance tightened

Теперь можно удерживать по крайней мере следующие исторические чтения, не смешивая их:

1. holy/liturgical angels present in worship — `B leading`;
2. fallen angels / Watchers — Tertullian line — `C`;
3. guardian angels — patristic/classic variant — `D/C-low`;
4. bishops/church leaders — Ambrosiaster — `D history`;
5. Christian prophets — Beza/classic catalogue — `D history`;
6. betrothal messengers — Lightfoot/Gill reception — `D history`;
7. hostile/visiting observers or messengers from churches — classic + Murphy-O'Connor variant — `D/C-low`;
8. angelic imitation / covered heavenly worshippers — classic homiletical variant — `D history`.

A-level minimum remains unchanged: Paul says `because of the angels`; text itself does not identify their exact function.

## 8. Conservative synthesis after third audit

Third pass **does not overturn** the controlling synthesis:

- material/textile covering — `B-high / leading`;
- hair/hairstyle-only — `C / serious alternative`, with sexual-role variants lower (`D/C-low`);
- `κεφαλή` headship/authority/predominance — `B / leading`; source/origin-only — `C`;
- `ἐξουσίαν ἔχειν`: woman is grammatical subject — `A`; exact symbolic referent — `B/C`;
- holy/liturgical angels — `B / leading`; Watchers — `C`; human/clergy variants — lower;
- Roman male covered worship — `A historical background`; exact Corinth trigger — `B reconstruction`;
- wives vs all women — `OPEN B/C`;
- women praying/prophesying in 11:5 — `A`;
- interpolation of 11:3b–15 — `D/C-low`;
- quotation/refutation of substantial vv.4–9 — `D/C-low` pending stronger discourse/textual evidence.

## 9. Tightened publication cautions

Не писать как установленный факт:

- что Garland 2003 — его latest/current commentary;
- что Fee 1987 автоматически отражает Revised 2014;
- что `angels=bishops` — нормальное Pauline lexical meaning, хотя Ambrosiaster так толковал;
- что homosexual/lesbian hairstyle reconstruction является «значением греческих слов»;
- что vv.4–9 demonstrably quote Corinthians merely because a rhetorical model can be constructed;
- что 11:3b–15 имеет manuscript evidence of omission sufficient for interpolation;
- что Roman status, Dionysiac ecstasy, prostitution, homosexuality или Judaizing являются доказанным single local trigger.

## 10. Boundary

```text
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
DO_NOT_REQUEST_OPEN_WEB_MATERIAL = true
LATEST_EDITION_CHECK_REQUIRED = true
EDGE_MODEL != EQUAL_WEIGHT_MODEL
```
