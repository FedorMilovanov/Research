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

P0 target remains official `Христианин` 1906 №1.

---

## 4. `Баптист`, 1907 — first issue identity closed, canonical receipt not established

Repo ledger 84 records official routes for 1907 №1–6. №1 is verified as a 22-page PDF externally; Commons also exposes exact first-issue visual objects with a public-domain path.

MASTER `02 Periodicals` search for `1907` surfaced received `Братский листок` issues but **no received `Баптист` 1907 row**.

Therefore:
- first issue identity: CLOSED;
- official/public facsimile route: CLOSED;
- preliminary rights route: CLOSED / PD candidate;
- canonical local receipt + our SHA256: OPEN;
- page visual verification after controlled receipt: OPEN.

Do not call first `Баптист` `IN DRIVE` yet.

---

## 5. `Утренняя звезда`, 1910 — official corpus exists, canonical receipt for 1910 not found

Repo ledger 80 stores 47 direct PDF routes for the 1910 annual run; №36 was the explicit hole in that pass.

MASTER `02 Periodicals` query by series surfaced local receipts only for **1915**, not 1910.

Therefore target `Утренняя звезда` 1910 №4 remains:
- issue/article identity: CLOSED;
- official route: CLOSED;
- canonical receipt: OPEN;
- SHA256: OPEN;
- page visual: OPEN.

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
