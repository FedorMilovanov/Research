# 100. Chapter 8 — periodical acquisition and page-control map

Дата прохода: 2026-09-06  
Authority: MASTER `02 Periodicals` + repo acquisition ledgers 80/84 + Book Authority v2  
Статус: **CANONICAL RECEIPT MAP / SELECTED OBJECTS PARTLY CLOSED**

## 0. Главное правило

Для Chapter 8 различаем четыре состояния:

1. `SERIES / ISSUE IDENTITY` — выпуск существует и библиографически определён;
2. `DIRECT EXTERNAL ROUTE` — найден прямой PDF/DJVU URL;
3. `CANONICAL LOCAL RECEIPT` — MASTER `02 Periodicals` содержит local relative path + SHA256;
4. `PAGE VISUAL VERIFIED` — конкретная страница/титул просмотрены и связаны с claim/caption.

`DIRECT URL` не равен `IN DRIVE`.  
`MASTER row + SHA256` не автоматически равен `PAGE VISUAL VERIFIED`.

---

## 1. `Братский листок`, 1906 — acquisition gate существенно закрыт

До этого Chapter 8 ошибочно выглядел так, будто representative 1906 `Братский листок` ещё надо получать снаружи. MASTER показывает обратное: несколько выпусков **физически приняты в canonical corpus и имеют SHA256**.

### 1.1 Row 75 — strongest controlled early object

MASTER `02 Periodicals`, row 75:
- series: `БРАТСКИЙ ЛИСТОК`;
- year: 1906;
- source month field: 5;
- canonical note: `№6 — printed parent; source filename labels May`;
- size: **4.650 MiB**;
- local relative path: `04 — CHANNEL METADATA & EXPORTS\ChatExport_2026-06-27\files\Братский Листок май 1906 года.pdf`;
- SHA256: **`1f2576aeeefdf95f4366b740ecf06a7a1dbd374b82c9575a68d8931021db258b`**.

Crucial title audit from 2026-07-31:
- first page was visually checked;
- it prints the object as an appendix to **`Христианин` №6, 1906**;
- page count: **10 pages**;
- canonical local slot is therefore tied to printed parent №6, while the owner/source filename labels it May.

### Independent page recheck, 27 November 2026

[Recorded reviewer verification in PR #547](https://github.com/FedorMilovanov/Research/pull/547#issuecomment-7068396651): the reviewer downloaded Drive object `1M_jJBvfs5FFCqpQ-TpOgsQ_ewskYZrnH` (4,875,926 bytes) and reported a locally recomputed SHA256 identical to MASTER row 75. This is a modern 2025 compilation of ten raster page images, without a text layer, not a born-digital archival original. The reviewer visually checked pages 1 and 10: page 1 names the parent `Христианин` №6 (1906) and contains May chronology (5, 13 and 16 May); page 10 includes the editorial signature `Редакторъ-Издатель И. С. Прохановъ`. This establishes the printed parent, internal May evidence and the editor-publisher on the inspected pages. It does not establish that this was the first issue, independently prove free distribution, or clear scan provenance/rights. MAX W04 transfers this attributed reviewer receipt; no new local PDF download or image inspection is claimed.

### Status
- binary receipt: CLOSED;
- SHA256: CLOSED;
- first-page / printed-parent visual verification: CLOSED;
- exact month-normalization beyond printed parent: preserve conflict note;
- rights/provenance for web republication: OPEN;
- derivative/web path: OPEN.

This is already a serious Book Authority object, not merely a lead.

### 1.2 Other received 1906 issues

MASTER rows:

| Row | Slot | Size MiB | SHA256 |
|---:|---|---:|---|
| 44 | Aug 1906 | 6.432 | `48d8611d27ad9d26329e713e4405ae6d11719f9b42704b88ca68f506f26c45b9` |
| 50 | Jul 1906 | 3.917 | `09fee235887ae29dd60060e277b7208dae3e6baa6c25e95fca7f26269355f333` |
| 54 | Nov 1906 | 3.511 | `fb9030ad4a1309ab578374731c07180b885488406e46ead566b13d7b837a6554` |
| 60 | Sep 1906 | 4.522 | `a90c76e0375ac8ac49177ed5d369891123c42f76748519a4f1db88aeb3af5130` |
| 76 | second Nov-labelled receipt | 3.511 | `67c1de40d68ea200c4cc1ea80fa61db6697437d84ad3a9365bad01db1de2bc25` |

Row 54 and row 76 are **not assumed duplicates solely from date/size** because SHA256 differs. Deduplication requires binary/content comparison, not guesswork.

### 1.3 Start-date gate remains open

MASTER photo caption says `Братский листок` began from March 1906, while the earliest canonical received object currently surfaced here is the printed-parent №6 object.

Therefore:
- representative early-series binary: CLOSED;
- claim `first issue = March 1906`: still requires exact first-issue facsimile / series bibliography.

---

## 2. `Братский листок`, 1907–1910 — local corpus is already substantial

Examples with canonical SHA256:

- Dec 1907, row 47: `750b92b27612fac2025b9af2ab94f5c2ea50c19bf199f2c02779d4ea75bac2db`;
- Nov 1907, row 55: `255ecccbac553ceb6e8b22595eaa6791130d033c7ed5685f67e0a5793248d624`;
- Sep 1907, row 61: `c0299138c65e775870092427b6c48f8a873ce8627d506fb1cb9dd1bd8a4ee0c4`;
- May 1908, row 49: `ed2899b8957158f5638ccd2557ef68467b7f8d408ce63f7f23b1251089c26683`;
- Oct 1908 special RES supplement, row 58: `0ee01385271aa83d5464465271319c1a27753fa609cab7a3cdc566974daac6fe`;
- Jul 1909, row 51: `1fbc119781a19e74d7b94a8672968e270fcc1017cd2f76a55fed4d0c94819bef`;
- Oct 1909, row 59: `19679a242c3872a970d0cf560850d8e9b20feb22684a4954bd33d76d0376d389`;
- Jun 1910, row 53: `64161aac155ee77d84985758807fb8ea3ec0f082df35094d714a068ab9c0c8a6`;
- Jul 1910, row 52: `775cd42c3f9656c641de8f913b594716308718743fdf67373640b89757f4c577`;
- Aug 1910, row 46: `f259338653848c00a26df3f291806115bf7a604f88ce5b59acec30382ca8227a`;
- Nov 1910, row 57: `4f61f13d34bc5c85eea4d2433d89652cbfc808c626bdc503224925f6a2fd8f3c`;
- Dec 1910, row 48: `4a00b37b5518e8c1d447e00c0efdc4daff4462f3d51c19fb460af239829870ba`.

### Editorial consequence

Chapter 8 does **not** have a general `Братский листок bytes missing` blocker. The remaining work is narrower:
- choose representative pages;
- verify exact page/masthead/caption;
- rights/provenance;
- derivatives/media ledger.

---

## 3. `Христианин`, 1906 — external corpus strong, canonical receipt still open

Repo ledger 84 records direct official routes for 1906 №1, 4, 5, 6, 8, 9, 10, 11, 12; №3 is bibliographically confirmed but the direct binary route remained unresolved in that pass.

MASTER `02 Periodicals` search for `1906` surfaced **only `Братский листок` rows**, not a canonical `Христианин` 1906 receipt.

Therefore:
- series identity: CLOSED;
- official direct routes for representative issues: CLOSED;
- canonical local receipt for `Христианин` 1906 №1: OPEN;
- SHA256 for received canonical 1906 `Христианин`: OPEN;
- page visual/quote gate: OPEN.

### W31 — selected first-issue visual reading

[Commons copy of №1, January 1906](https://commons.wikimedia.org/wiki/File:Журнал_«Христианин»,_СПб.,_1906,_№01.pdf), 57 digital pages, 23.77 MiB; upload history attributes transfer to the former official RS ECB PDF URL in 2018. [Current official index](https://baptist.org.ru/izdaniya/hristianin/) links [the same-named official PDF](https://baptist.org.ru/wp-content/uploads/2026/02/khristianin-1_1906.pdf). Both full-PDF fetches rejected at 24,922,934 B; container download failed DNS. No current byte equality or new SHA256. Two 960px per-page Commons images actually inspected.

- Digital page 1: illustrated cover, №1, January 1906, first year. Christ speaking from a boat to listeners by the shore (artist not identified); 1 Cor. 1:22–23, unity/freedom/love maxim, and wording of Phil. 1:27. Printed reference appears as «Филипп 1,17», not the correct biblical locator 1:27; distinguish historical printing from editorial normalization.
- [Digital page 2](https://commons.wikimedia.org/w/index.php?page=2&title=File:Журнал_«Христианин»,_СПб.,_1906,_№01.pdf): title leaf independently dated January 1906, №1; imprint at bottom **1905**, St Petersburg, typography A. Lashinsky, Kirpichny lane, house 3. This is the January 1906 numbered issue with a 1905 imprint, not proof that the November trial number has been recovered. Do not equate imprint year with actual day of circulation. Contents identify Spurgeon's sermon «Как воскрешать мертвых», p.13; «Христос распятый», signed И. С. П., p.39; «Вера (для юных читателей)», p.47; appendix «Оправдание Христом». Contents locators only, not claims that articles were read.
- [Братский вестник 1947 №5](https://mbchurch.ru/publications/brotherly_journal/1628/): retrospective narrative describes two earlier manuscript/multiplication-apparatus issues and Zhidkov's handwriting, then regular typography from 1906. Not an image of those earlier issues; precise machine remains open. Commons provides PD-scan candidate, not final media approval.

Proposed reader paragraph: «Январский номер 1906 года имел на титуле дату выпуска, но в типографских выходных данных стоял ещё 1905 год. На обложке помещены евангельские слова о распятом Христе и единстве веры. Оглавление показывает, что редакция с самого начала соединяла проповедь, богословие и наставление молодёжи: в первом номере были заявлены беседа Сперджена, статья о распятом Христе и приложение об оправдании Христом». Selected external page visual VERIFIED; full original receipt, rights, reading of articles and full issue remain OPEN.

P0 target remains controlled receipt of official `Христианин` 1906 №1.

---

## 4. `Баптист`, 1907 — first issue identity closed, canonical receipt not established

Repo ledger 84 records official routes for 1907 №1–6. №1 is verified as a 22-page PDF externally; Commons also exposes exact first-issue visual objects with a public-domain path.

MASTER `02 Periodicals` search for `1907` surfaced received `Братский листок` issues but **no received `Баптист` 1907 row**.

Therefore:
- first issue identity: CLOSED;
- official/public facsimile route: CLOSED;
- preliminary rights route: CLOSED / PD candidate;
- canonical local receipt + our SHA256: OPEN;
- selected external page visual verification: VERIFIED (W30, PDF indices 0–4 and 21); full 22-page inspection and verification against a controlled local receipt: OPEN.

### W30 — first-issue page images and exact editorial evidence (28 November 2026)

[Official RS ECB PDF, 1907 №1, 22 digital pages](https://baptist.org.ru/wp-content/uploads/2026/02/baptist1907_01.pdf), linked from [the official periodicals index](https://baptist.org.ru/izdaniya/baptist/). Six images directly inspected, not OCR; no download/hash or Drive receipt claimed. The issue's existence and route were known in ledger 84; the new evidence is selected page-level reading.

- PDF index 0, unnumbered first/title page (conventionally p. 1): №1, June 1907, spiritual-moral journal, organ of Russian Baptists; Matthew 28:19–20 and a captioned illustration of Christ's baptism by John in the Jordan. The inaugural editorial statement presents service to Christ's church through reporting Baptist faith, doctrine and life in Russia and abroad; sermons and scriptural exposition, news of worldwide Christian life from a Baptist viewpoint, defence of the gospel and Christian unity are explicit aims. No author signature visible on this page; do not identify the illustration's artist from appearance.
- Printed p. 2 / PDF index 1: Apostles' Creed introduced as recognized by Baptists and read at the London world congress, followed by Article I of the Brief Baptist Confession, on the Word of God: enumerated canonical books, divine inspiration and Scripture as the sole rule of faith and life. This is the periodical's own doctrinal and editorial witness, not independent proof of universal subscription by every Baptist or of congress proceedings.
- Printed pp. 2–4 / indices 1–3, complete article «Название „Баптисты“»: acknowledges discomfort with the non-Russian name, explains believer's baptism by immersion and the international link to churches outside Russia; retains the name while extending fellowship to believers who believe and are baptized regardless of their name. It also explicitly distinguishes Baptist baptism from infant baptism. Attribute this to the article (no visible author signature at its end), not automatically to Mazaev personally. Do not equate unity in Christ with the abolition of confessional differences.
- Printed pp. 4–5 / indices 3–4: beginning of «Вера Божия» on Acts 16:16–40; the exposition emphasizes salvation through faith in Christ. Only these two pages read, not the complete sermon.
- Printed p. 22 / index 21: colophon identifies responsible editor-publisher D. I. Mazaev, Nakhichevan-on-Don, 2nd Voznesenskaya Street, own house no. 23, printer F. P. Pavlov, Rostov-on-Don. Distinguish editorial address from printing location; neither should be silently normalized into the other. The same page prints an attributed letter report about English Christians deciding to discontinue financial assistance on the assumption that persecution had ended in Russia; it is a report, not independent proof of actual freedom or a financial transaction.
- [Commons 1907 category](https://commons.wikimedia.org/wiki/Category:Baptist_(Russian_magazine),_1907) lists all six 1907 DjVu issues. No independence or byte equality with the official PDF established. The official index also assigns the same link to both 1907 №1 and 1909 №1; do not infer correct 1909 identity from anchor labels. The 1907 PDF itself confirms the correct 1907 identity.
- Secondary comparison: I. P. Plett, *История евангельских христиан-баптистов 1905–1944* (2009), p. 23, explicitly locates the inaugural programme at 1907 №1 p. 1 ([text](https://djvu.online/file/gUelaYOtdwn1E)); its generic Rostov location is refined by the actual colophon. The visual original is stronger for the exact wording and editorial address. No reliance on a later reproduction for these readings.

Reader-ready passage for #547: «Первый номер „Баптиста“, вышедший в июне 1907 года, открывался изображением крещения Христа в Иордане и словами Великого поручения. За редакционным обращением следовали Апостольский символ веры и первый раздел краткого баптистского вероучения — о Слове Божьем. В статье о названии „баптисты“ автор объяснял, почему русские верующие сохраняли это имя: оно связывало их понимание крещения с братством за пределами России. При этом он не считал само название важнее церковного мира. Редакция находилась в доме Дея Мазаева в Нахичевани-на-Дону, а печатался журнал в Ростове-на-Дону». Sources: first page, pp. 2–4, 22; editorial programme and theology are direct page evidence. No claim that Mazaev wrote the unsigned article, or that its particular fellowship formula represented every evangelical group.

Do not call first `Баптист` `IN DRIVE` yet. Physical provenance, exact binary identity, remaining pages, image rights and publication approval remain open.

---

## 5. `Утренняя звезда`, 1910 — official corpus exists, canonical receipt for 1910 not found

Repo ledger 80 stores 47 direct PDF routes for the 1910 annual run; №36 was the explicit hole in that pass.

MASTER `02 Periodicals` query by series surfaced local receipts only for **1915**, not 1910.

Therefore target `Утренняя звезда` 1910 №4 remains:
- issue/article identity: CLOSED;
- official route: CLOSED;
- canonical receipt: OPEN;
- SHA256: OPEN;
- page visual: OPEN (1910 №4 not inspected this wave).


### W31 — earliest issue chronology and holder locator

[RNB, *Газеты дореволюционной России 1703–1917: каталог*, СПб., 2007](https://militera.org/books/pdf/enc/biblio_gazety-dorrev-rossii.pdf#page=407), printed p.407, entry 5219, PDF index 406 and title page index 0 visually checked: first issue explicitly `1909, №1 (19 дек.)`; holdings 1909 №1, 1910–1916, 1917 №1 (24 March); shelfmark **Газ.1-П/1-217**. Record identifies a break August 1916–23 March 1917 and supplements; this is holder bibliography, not inspection of newspaper pages.

[Проханов, *В котле России*, online Russian translation](https://krashve.ru/wp-content/uploads/2021/01/ivan_prohanov_-_v_kotle_rossii.pdf#page=66), p.66, PDF index 65 visually checked: remembers first printed number on 1 January 1910 and distinguishes six periodical functions (spiritual, church needs, youth, children, music and broader public life). Edition/translator and English original not verified here. **19 December 1909 Julian = 1 January 1910 Gregorian**, so these two witnesses may refer to precisely the same day. Do not invent a December trial issue separate from the January first number, or declare the memoir date erroneous. Calendar convention of translated memoir and original masthead require confirmation. [RNB online index](https://nlr.ru/res/inv/ukazat55/cat_show.php?p=3&rid=7957) indexed record corroborates the 1909 start but direct access timed out; [RS ECB periodicals index](https://baptist.org.ru/izdaniya/) describes 1910 start and linked newspaper archive returned 404. These failures do not negate ledger 80.

Reader wording: «На рубеже 1909–1910 годов Проханов начал выпускать еженедельную „Утреннюю звезду“». Note with RNB p.407/entry 5219 and memoir p.66: likely old/new-style equivalence, not separate issue proof. Next bounded action: original RNB №1, 19.12.1909, Газ.1-П/1-217. No original newspaper page, full object, new checksum or rights claimed.


### W32 — directly inspected 1910 first-page witness, №41

[Commons archival image, №41](https://commons.wikimedia.org/wiki/File:Газета_Утренняя_Звезда_1910-41.png), permanent revision 855280429: original PNG 3299 × 5109, 29 MB, uploaded 15 July 2017, author unknown; Commons PD-old-70 and PD-US tags, repository's rights gate unchanged. Direct visual read of 1920 × 2973 derivative, not OCR, not whole issue. [Exact image route](https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f7/Газета_Утренняя_Звезда_1910-41.png/1920px-Газета_Утренняя_Звезда_1910-41.png).

- Masthead: «Утренняя звезда», №41, first year, St Petersburg, Friday 8 October 1910 (printed date), weekly on Fridays, separate number 5 kopecks. Self-description concerns the religious awakening of the Russian people; the five named domains are religion, politics, public life, science and literature. This is a direct visual confirmation for that number, not an extrapolation to the inaugural issue. Do not infer the first issue date solely from issue numbering or weekday.
- Left column: editorial communications directed to I. S. Prokhanov, Chernyshev lane, house 12, flat 53; subscription money and advertisements routed through publishing partnership Raduga, Voznesensky prospect, house 40 (also repeated in the foot-of-page banner). Petersburg subscription 2 r. 50 k. per year; separate regional tariff is printed. Do not equate advertised prices with actual revenue or subscriber numbers.
- Actual juxtaposition of articles: «О безпорядкахъ въ семинаріяхъ» addresses students and religious education; «При дверяхъ» offers spiritual exhortation; «За недѣлю» presents domestic and foreign news, including reports on the imperial funds and the monarchy in England. Reader notices address subscription arrears and correspondence with the office. Exact column headers and placement are visible; no claim to have fully transcribed these articles or to verify the news reports themselves.
- Dossier 80 was reread: the already recorded direct routes for [1910 №1](https://baptist.org.ru/_service/33957/download/id/246321/name/Utrennyaya-zvezda%2B1910_1.pdf) returned oversized response (28,331,217 B), [№4](https://baptist.org.ru/_service/33957/download/id/295211/name/Utrennyaya-zvezda%2B1910_4.pdf) inaccessible. No new acquisition, checksum, complete issue or №4 article reading. The external visual evidence for №41 is separate from the still-open №4 target and first issue RNB locator. No independence of this image from official series copies established.
- Reader-ready evidence: «Осенью 1910 года „Утренняя звезда“ уже выходила каждую пятницу. На первой полосе номера от 8 октября рядом с духовным наставлением обсуждались события в семинариях и новости политики, а в заголовке газета прямо объявляла своим предметом не только религию, но и общественную жизнь, науку и литературу. Статьи направляли в редакцию Проханова, а подписку обслуживало товарищество „Радуга“». Cite first page №41; do not identify it as №4 or use this as a witness to the exact opening date.

External first-page visual locator for №41 VERIFIED; canonical full receipt, issue №1/№4 page controls, provenance, item-level rights and publication HOLD remain. STOP_DISCOVERY on the same legacy PDF routes absent a genuinely different access path.

---

## 6. `Утренняя звезда`, 1915 — verified wartime press and legal/community evidence

MASTER row 97:
- series: `УТРЕННЯЯ ЗВЕЗДА`;
- date: **30 Oct 1915**;
- filename: `Утренняя_Звезда_30_октября_1915_года_.pdf`;
- size: **7.632 MiB**;
- local relative path recorded in canonical corpus;
- SHA256: **`95751678e4e943de85a2648e79f5e2fa88cb4a55295d0254d1a15e83211c38f7`**.

MASTER annotation explicitly records:

> white unprinted strips indicate material removed by censorship.

Contents include:
- tenth anniversary of `Христианин`;
- `Еще о журналах`;
- war/current affairs;
- religious/community questions.

### Why this is a P0 Chapter 8 visual

This one object can show, physically and without reconstruction:
- weekly evangelical current-affairs press;
- the wartime public sphere;
- the visible blank column and contemporary reports of administrative restrictions (the cause of the blank space itself remains unverified);
- the mature relationship between `Утренняя звезда` and the wider Prokhanov print ecosystem.

### W23 — actual binary and eight-page visual inspection, 28 November 2026

[Drive object](https://drive.google.com/file/d/1ilzW_kOr2tfSAjmIdqbhukvnUj0GaG2n/view): received through the authorized Drive connector, 8,002,892 bytes, independently recomputed SHA256 exactly equal to MASTER row 97 above. PDF has eight raster pages and no extractable text layer; metadata dates the modern JPEG-to-PDF compilation to 30.10.2024 (not a historical digital original). All eight page images were opened; targeted crops on pp. 1 and 5 were read directly, without OCR. Printed numbers 2–8 match PDF pages 2–8; first page has the masthead. Not a complete transcription.

- **p. 1, masthead and «Десятилетие „Христианина“»:** №44, VI year, Petrograd, Friday 30 October 1915; weekly on Fridays, single issue 5 kopecks, editorial correspondence addressed to I. S. Prokhanov, subscription/advertising to «Радуга», Стремянная 11. The anniversary article explicitly dates the Main Administration for Press Affairs' permission for Prokhanov to print, publish and edit the monthly spiritual magazine to **3 November 1905** (date as printed, old style). The article distinguishes the permission anniversary from the anniversary of actual publication and announces a planned celebration on 6 December 1915. This is contemporary retrospective editorial testimony, not the administrative permit itself, and the announcement does not prove that the celebration occurred.
- **p. 5, «О метрической записи детей»:** printed copies of the First Kharkov community's application and Kharkov provincial administration's reply, 5 May 1915, department I, desk I, addressed to the bailiff of Kharkov precinct 6. The reply concerns children from marriages conducted in the Orthodox rite who were not entered in the Orthodox registers in time; entry in sectarian registers is to follow the procedure for correction/addition under competent supervision. Scope is this case, not a general abolition of registration restrictions.
- **p. 5, «О закрытии общины»:** printed complaint addressed to the First Department of the Governing Senate, by members of the council of the Temryuk–Anapa community of Russian Christians-Baptists of evangelical confession, Anapa, 20 October 1915. According to the complainants, the funeral procession on 17 April took a different street because of mud; judicial proceedings were discontinued, then the authorities administratively closed the registered community and prohibited prayer gatherings on 1 June. The council says it had not received the closure order and asks the Senate to overturn it; it invokes point 6 of section II of the decree of 17 October 1906 (not the 1905 Manifesto). A1 participant testimony as reproduced in the periodical, not the original signed petition, closure order or Senate judgment. A dark blot obscures a small part of the complaint; no restoration of obscured words asserted.
- **p. 7:** printed editorial imprint I. S. Prokhanov; large visibly blank area in the right column below the continuation marker, with show-through of reverse-side printing. No legible explicit censorship attribution in this area. Physical blank space is confirmed; MASTER's interpretation that censorship removed material is **not established by the blank space alone**. Do not label it as a proven censor's cut without another edition, editor's note or archival evidence.
- **p. 8:** advertisements of publishing partnership «Радуга», Стремянная 11, books and hymn collections; offers annual sets of «Христианин» for 1908–1910, 1 rouble 50 kopecks per set compared with subscription price 3 roubles 60 kopecks. Useful direct evidence of periodical/book distribution, not proof of actual sales or circulation.

### Current status

- canonical binary receipt and SHA256: CLOSED, independently reverified;
- issue/date identity and eight-page visual inspection: CLOSED;
- exact page locators pp. 1, 5, 7, 8: VERIFIED for the specific observations above;
- censorship interpretation: MASTER-ANNOTATED / EVIDENCE_HOLD (blank area physically verified, causal attribution not established);
- rights/provenance: OPEN; derivative/web path: OPEN; publication eligibility unchanged.
- Earlier connector filename-search limitation: SUPERSEDED by the exact-ID receipt; no new permanent Drive copy created.

---

## 7. `Беседа` — largest remaining acquisition gap

Unlike `Братский листок`, current canonical receipt pass did not surface representative `Беседа` binaries with SHA256.

This matters because `Беседа` is the intended opening documentary scene.

P0:
1. identify representative 1889/1890 early object;
2. identify later Stockholm/foreign phase object;
3. controlled receipt;
4. SHA256;
5. masthead/date/page visual verification;
6. rights/provenance.

Until this closes, do not generate a fake `Беседа` cover or reconstruct the clandestine newsroom.

### W33 — contemporary external witnesses to the contents and circulation of «Беседа»

This closes a limited textual witness gap, not the original-issue acquisition gate. The chapter manuscript (#547 exact HEAD ee035041) still gives predominantly a generic description of the journal; the following documented scene can replace some abstraction.

1. **Lesia Ukrainka, «Беседа», часопись баптистів (штундистів)**, first published in «Народ», 1895, №5, pp.64–69; subsequently separate offprint «Українські баптисти і їх часопись “Бесѣда” за 1894 р.», Lviv: Ivan Franko, 1895, 29 pp., series book 31. [Full web text](https://www.l-ukrainka.name/uk/Publicistics/Beseda.html) read in relevant opening, theological discussion, visit to Tolstoy and conclusion. Author states she had nearly all the 1894 issues, monthly Russian-language publication from Stockholm, fourth publication year, distribution address Blombergs bokhandel, Folkungagatan 14. She reports an editorial appeal for common evangelical work, short practical articles, and clarification of the Old Testament's obligations for Christians. Her review discusses spiritual new birth and grace, Sunday school materials translated from Swedish, hymns, reports of persecution and disagreements about nonresistance. She describes the dialogue «Несколько часов у Л. Н. Толстого» as a shortened Ukrainian translation from a contribution about a visit in 1893, not her own interview. She distinguishes the journal's tolerance in engaging opponents from her own criticism of Calvinistic salvation by grace and her preference for practical social work. **A1 as contemporary evidence of her reading and reception; mediated witness for the original journal's contents, not exact original pages.** Do not generalize her characterizations (including the movement's ethnic distribution, pacifism and Calvinism) into uncontested facts about all communities.
2. **L. N. Tolstoy, letter 129 to I. S. Prokhanov**, editorially dated second half September 1896, Yasnaya Polyana, *Complete Works*, vol.69, printed pp.155–156, [official Tolstoy corpus](https://tolstoy.ru/online/90/69/), full letter and notes read. Tolstoy explicitly acknowledges receipt of «Беседа» and a promised book on persecution, then disputes the possibility of unity on the basis of Christ's divinity. Editorial note says the letter responds to Prokhanov's 5/17 September 1896 letter and is printed from a typescript copy; note places the journal in London and identifies the earlier 1893 visit with Stavtsev. **A1 for Tolstoy's acknowledgment and position as transmitted by the edition; not an autograph, not direct proof of which issue was sent, not proof the promised book was delivered.** The writer's reply and Ukrainka's account independently corroborate circulation and the earlier visit; they do not prove verbatim identity of the 1893 conversation.
3. **Additional mediated historical locators:** [Tambov diocesan gazette, 1915 digitized PDF](https://pravoslavnoe-duhovenstvo.ru/media/priestdb/materialattachment/attachment/4b/d0/4bd09866-aaec-4119-9c3e-6bb0f86928e5.pdf), text layer pp.425–427, notes 24–28, includes January 1895 p.13 (Stockholm), May 1895 «Слово защиты», and a contribution on the need to organize overseas help for persecuted believers. The text quotes an appeal for detailed reports of exile and addresses of people in need. The missionary author interprets such activity polemically; do not adopt the author's justification of repression or treat embedded quotations as visually collated journal pages. Two screenshot attempts returned DisabledError; article author and precise issue number not checked. Bibliographic route to the earlier administrative compilation [V. A. Valkevich, 1900, RSL record](https://search.rsl.ru/ru/record/01003550121); the separate appendix 3 referenced by the missionary text is still not read.
4. **Edition/locator QA:** [academic collected works 2021, vol.7 contents](https://chtyvo.shron.org/authors/Ukrainka/Povne_akademichne_zibrannia_tvoriv_Tom_07_Literaturno-krytychni_ta_publitsystychni_statti/) locates the article starting p.381, commentary p.617; the web edition's concluding metadata instead says pp.162–164 and has an anomalous 1884 Geneva date inconsistent with its own 1889–1898 chronology. Do not copy these values as authority. PDF download redirected to inaccessible DSpace; no visual verification of the 2021 pages or 1895 first print. Retain the securely identified first-publication range as bibliographic locator; do not use long verbatim quotations from modern editions. The offprint is corroborated by [Ivan Franko research site](https://franko.live/prychynky-do-biografiyi/pryyateli-svyatoyi-poeziyi-ivan-franko-ta-4/).

**Reader-ready proposed passage:** «В 1895 году о “Беседе” написала Леся Украинка, в руки которой попала почти вся подшивка за предыдущий год. Она увидела в ней источник сведений о верующих, которых читатели обычно знали по официальной печати. В журнале обсуждали благодать и новое рождение, помещали материалы для воскресных школ и сообщения о преследованиях. Сама писательница не разделяла всех богословских убеждений авторов и предпочитала более деятельное общественное христианство. Год спустя Лев Толстой в письме Проханову поблагодарил его за присланную “Беседу”, но не согласился с тем основанием единства, которое предполагало исповедание божественности Христа. Подпольная печать становилась не только связью между общинами, но и пространством разговора с людьми за их пределами — разговора, не стиравшего разногласий».

Original representative issue images, SHA256, exact underlying article pages, original offprint and rights remain OPEN. Do not replace these missing objects with a reconstructed cover. STOP_DISCOVERY on repetitive generic searches: precise next target is Stockholm 1894 monthly run or January 1895 p.13; if unavailable, keep the attributed reception evidence and advance the manuscript.


---

## 8. Revised Book Authority media status for Chapter 8

### Already meaningful local objects

**Object A — `Братский листок`, 1906 / printed parent `Христианин` №6**
- bytes: YES;
- SHA256: YES;
- first-page/title audit: YES;
- rights: OPEN;
- derivative: OPEN.

**Object B — `Утренняя звезда`, 30 Oct 1915**
- bytes: YES, W23 independent exact-ID receipt;
- SHA256: YES, independently reproduced;
- page visual: YES, all eight images opened; targeted pp. 1, 5, 7, 8; censorship causation remains HOLD;
- rights: OPEN;
- derivative: OPEN.

This means Chapter 8 is **closer to the minimum 2-object media gate than originally assessed**. It is still not BOOK-READY because rights, provenance, causal attribution of the blank area and derivatives/media-ledger publication fields remain open.

### External-but-not-local priority

- `Христианин` 1906 №1;
- `Баптист` 1907 №1;
- `Утренняя звезда` 1910 №4;
- representative `Беседа`.

---

## 9. Immediate production queue

1. MASTER row75: page 1 / printed parent and page 10 / editorial signature verified by the attributed PR #547 reviewer. Select any further illustration only against its exact visual locator; rights and provenance remain open.
2. MASTER row97: binary/hash and all page images checked W23; use pp. 1, 5, 7, 8 for the bounded observations above. Do not infer censor removal from the blank column; pursue an independent causal witness only if the caption requires it.
3. Resolve rights/provenance for both local objects.
4. Receive/hash official `Христианин` 1906 №1.
5. Receive/hash `Баптист` 1907 №1.
6. Receive/hash `Утренняя звезда` 1910 №4.
7. Continue hardest acquisition: `Беседа`.

Current verdict: **NARRATIVE DRAFT-READY / TWO STRONG LOCAL MEDIA RECEIPTS WITH PAGE CONTROL / RIGHTS + PROVENANCE + DERIVATIVES OPEN / NOT BOOK-READY**.
