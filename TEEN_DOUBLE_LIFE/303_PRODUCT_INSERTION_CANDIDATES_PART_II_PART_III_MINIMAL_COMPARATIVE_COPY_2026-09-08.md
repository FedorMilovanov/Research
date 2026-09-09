# Product Insertion Candidates — Part II / Part III
## Minimal comparative copy after Research closure

**Status:** EDITORIAL TRANSFER CANDIDATES / RESEARCH ONLY / NOT AUTOMATIC PRODUCT PATCH  
**Date:** 2026-09-08  
**Depends on:** `301–302`  
**Rule:** these blocks are deliberately short. If the Product owner cannot insert them without harming pace, drop Part III first. Do not expand them into new subsections merely because more Research exists.

---

# 1. Part II — RECOMMENDED

Target Product PR: `#1895`  
Target file: `src/content/articles/podrostok-za-kadrom-roditelyam-posle-razoblacheniya.mdx`

## Best insertion anchor

Preferred: after the early section `Нет моральной комнаты ожидания для необращённого ребёнка`, before or near `Воспитание начинается не в день скандала`.

Reason: the manuscript has just established that unregenerate status does not suspend duty; the historical paragraph then shows that this is not a modern Baptist improvisation.

## Candidate reader-facing copy

### Вариант A — recommended compact paragraph

Исторически это не чужая для баптистов логика. Геркулес Коллинз, один из лондонских Particular Baptists XVII века, спорил против крещения младенцев и одновременно называл благочестивых родителей большой милостью для детей — из-за доброго воспитания, молитвы и примера. В предисловии к своему катехизису он призывал родителей молиться за детей, наставлять их и заботиться об их вечном благе. Позднее Джон Гилл столь же серьёзно говорил о детском послушании, родительской молитве, Писании, исправлении греховных привычек и приведении детей под обычные средства благодати. Но Гилл же предостерегал от другого перекоса: нельзя учить ребёнка произносить религиозное «я верую» так, будто выученная форма уже является самой верой.

**Баптистская граница у крещения не означает паузы в воспитании до крещения.** Ребёнка нужно сейчас учить, исправлять, приводить под Слово и звать ко Христу — и одновременно нельзя превращать семейную религиозность или правильные ответы в свидетельство нового рождения.

Approximate size: ~130–150 Russian words depending tokenizer/punctuation.

## Optional shorter variant

### Вариант B — if article is too long

Это не современная попытка сделать баптизм «строже». Геркулес Коллинз, отвергая крещение младенцев, всё же называл благочестивых родителей большой милостью для детей — из-за воспитания, молитвы и примера. Джон Гилл соединял детское послушание и серьёзное родительское наставление с предупреждением не приучать ребёнка изображать веру, которой у него ещё нет. **Баптистская граница у крещения не требует паузы в воспитании:** учите, исправляйте, приводите под Слово и зовите ко Христу сейчас — но не превращайте семейную религиозность в сертификат нового рождения.

Approximate size: ~80–100 Russian words.

## Source-list additions if imported

Add only sources actually used:

- Hercules Collins, *Believers-baptism from heaven, and of divine institution*, pp. 47–48 — University of Michigan / EEBO2: `https://quod.lib.umich.edu/e/eebo2/B20542.0001.001/1:5.5?rgn=div2;view=fulltext`.
- Hercules Collins, *An Orthodox Catechism* (1680), Preface, printed p. 6 / accessible reprint PDF p. 11: `https://www.thecalvinist.net/etc/1680%20Orthodox%20Catechism%20(Hercules%20Collins).pdf`.
- John Gill, *A Body of Practical Divinity*, `Of the Respective Duties of Parents and Children`: `https://ccel.org/ccel/gill/practical/practical.v.ii.html`.

### Source compression option

If the Product source list should remain shorter, use Collins *Believers-baptism* + Gill only. The *Orthodox Catechism* Preface deepens the same claim but is not required to prove the core sentence.

## Forbidden edits around this insertion

Do not:

- imply Collins/Gill considered unbaptized children quasi-members;
- say their pastoral model proves credobaptism;
- present Gill’s `1 Cor 7:14 = legitimacy` reading as the article’s necessary exegesis;
- call outward obedience regeneration;
- remove the manuscript’s existing Spurgeon balance.

---

# 2. Part III — OPTIONAL / DROP-FIRST

Target Product PR: `#1921`  
Target file: `src/content/articles/podrostok-za-kadrom-chto-delat-tserkvi.mdx`

## Best insertion anchor

Inside or immediately after the existing section whose controlling point is:

> `Нельзя отлучить от церковного членства человека, который к нему не принадлежит`;

followed by ordinary pastoral responsibility toward a nonmember.

Reason: the comparison answers one narrow institutional question — why intentional pre-membership pastoral ownership matters — without interrupting the article’s choir/safeguarding/discipline architecture.

## Candidate reader-facing copy

### Вариант A — recommended if comparison is retained

Здесь полезно увидеть силу вопроса, который по-другому решают пресвитерианские и некоторые реформатские церкви. В их церковном устройстве крещёный ребёнок верующих уже имеет формальный церковный адрес до собственного публичного исповедания: он числится некомуницирующим или крещёным членом и находится под названным надзором церкви. В разных союзах конкретные дисциплинарные процедуры различаются, поэтому нельзя сводить их к одной схеме. Но институциональный эффект понятен: ребёнок не исчезает из пастырской карты только потому, что ещё не стал причастником или публично исповедующим членом.

Баптист может не соглашаться с самой предпосылкой крещения младенцев и наследственного членства. Однако вопрос остаётся полезным и для нас: **если мы говорим «членом церкви он станет после личного исповедания», кто пастырски знает и ведёт его сейчас?** Ответ не должен быть «никто». Граница членства может остаться баптистской; пастырская безадресность — не обязана. При этом пастырская забота о нечлене не превращается в церковные ключи и не создаёт скрытого квазичленства.

Approximate size: ~155–185 Russian words.

## Shorter variant

### Вариант B — preferred if pace is tight

Пресвитерианские и некоторые реформатские церкви решают один практический вопрос очень определённо: крещёный ребёнок верующих уже имеет формальный церковный адрес и находится под названным надзором до собственного публичного исповедания. Баптист может отвергать крещение младенцев и наследственное членство, но сам вопрос ему полезен: **если членом ребёнок станет после личного исповедания, кто пастырски знает и ведёт его сейчас?** Ответ не должен быть «никто». Граница членства может остаться баптистской; пастырская безадресность — не обязана. И наоборот: пастырская забота о нечлене не создаёт квазичленства и не даёт церкви ключей, которых в отношении него нет.

Approximate size: ~90–110 Russian words.

## Source-list additions if imported

Do not flood the source list. Two official polity sources are sufficient to establish the comparative sentence; a third is optional.

### PCA

Official 2026 Book of Church Order:

`https://www.pcaac.org/book-of-church-order/`

Use the current digital BCO controls around:

- children/non-communing members;
- oversight/instruction/government;
- discipline;
- Chapter 28 non-communing members.

### OPC

Official Form of Government / Book of Discipline:

`https://www.opc.org/BCO/FG.html`  
`https://www.opc.org/BCO/BD.html`

Use communicant/noncommunicant membership and baptism-only member discipline controls.

### URCNA — optional third source

Current official publications page / Church Order:

`https://www.urcna.org/pubsarts/`

Use mature baptized-member Article 59 only if the Product text needs an example of a formal exclusion path. The compact variants above do not require this detail.

## Mandatory wording guards

Do not say:

- `all Reformed churches discipline unprofessing children identically`;
- `PCA technical judicial process is identical for every non-communing child`;
- `formal baptized membership means presumed regeneration`;
- `institutional clarity proves infant baptism`;
- `Baptists have no category at all for children before conversion`.

### Preferred generic wording

Use:

> `пресвитерианские и некоторые реформатские церкви`

rather than naming three denominations in the reader-facing paragraph unless names are genuinely helpful.

---

# 3. If only one delta survives editorial compression

Choose **Part II historical Baptist recovery**.

Why:

1. it directly strengthens the article’s own confessional identity;
2. it answers a plausible objection without opening the baptism controversy;
3. it is closed by primary historical sources;
4. it supports the manuscript’s existing argument rather than changing its architecture;
5. Part III already states the important pastoral-ownership conclusion without needing comparative proof in the body.

Therefore priority:

`PART II COLLINS/GILL > PART III PAEDOBAPTIST COMPARISON`.

---

# 4. If Part III comparison is omitted

No theological defect remains.

Keep the comparative material in Research and perhaps a future deliberately chosen theological companion.

The existing Part III statement:

`never-member cannot be excommunicated`  
+
`nonmembership does not eliminate pastoral stewardship`

is already sufficient for the core Baptist article.

### Locked

`OPTIONAL COMPARISON OMITTED ≠ RESEARCH LOST`.

Research can remain evidence beneath editorial restraint.

---

# 5. Exact transfer sequence

For either Product mutation:

1. re-fetch live PR head;
2. confirm current Product main and `behind=0`;
3. fetch exact owned MDX blob SHA;
4. make one bounded content edit;
5. add only sources used by the added copy;
6. update internal Research authority comment to the exact comparative handoff/head used;
7. verify one-file permanent scope still holds;
8. rerun exact-head CI;
9. preserve Draft/noindex;
10. re-red-team the inserted paragraph for confessional overclaim.

No other Product owner should move in the same transaction.
