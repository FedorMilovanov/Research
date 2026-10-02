# Серия «Отступники» — Research → Product handoff

**Дата:** 2026-10-02  
**Статус:** `READY FOR PRODUCT INTAKE / DO NOT DEPLOY BLINDLY / FIVE-PART ARCHITECTURE`  
**Research authority:** `108_...` → `109_...` → `110_...`  
**Reader architecture authority:** `85_APOSTATES_FIVE_PART_SERIES_ARCHITECTURE_BIBLICAL_HISTORICAL_PASTORAL_2026-10-01.md`  
**Supersedes for Product reader architecture:** `14_PRODUCT_SERIES_BLUEPRINT_V2_2026-09-30.md` multi-hard-text-first model.  
**Product repository:** `FedorMilovanov/gb-is-my-strength`.

---

## 1. Handoff verdict

The Research corpus has completed:

- whole-Bible coverage;
- P0/P1 hard-text closure;
- source trust policy;
- competing-view ledger;
- Puritan practical-theology source map;
- church-history primary-source dossier;
- five reader drafts;
- five source/editorial maps;
- cross-series contradiction/overclaim audit;
- application of all seven required wording patches.

> **Product may now ingest the five-part reader series. Product must not reopen broad theology research or silently improvise claims beyond the frozen reader drafts/maps.**

No Product files are modified by this handoff.

---

# 2. Canonical Product shape

## Series title

# **ОТСТУПНИКИ**

## Hub subtitle

> **От падения Петра и предательства Иуды до отпавших времён гонений: что Библия называет отступничеством, кого можно вернуть и как Бог сохраняет Своих.**

## Required reader order

1. **Part I — Что такое отступничество?**
2. **Part II — Отступники Библии**
3. **Part III — Пётр и Иуда: падение или отступничество?**
4. **Part IV — Падение и возвращение в истории Церкви**
5. **Part V — Как предупреждать, исправлять и возвращать**

### Why this order is frozen

- Part I gives categories before cases.
- Part II displays diverse biblical trajectories without premature final-state judgments.
- Part III is the theological/pastoral center: grievous denial vs final apostasy and recovery.
- Part IV shows visible historical analogues without making history a second canon.
- Part V converts the theology into church/pastoral action.

Do not reorder merely for SEO keyword volume.

---

# 3. Route plan

The following route plan is the recommended canonical Product target.

Before implementation, Product must perform a collision/redirect check against current `main` and live routes. Research code search on 2026-10-02 did not surface existing `apostasy`/`otstupl` route content, but this is not a substitute for Product’s own route manifest/build check.

## Hub

`/apostasy/`

Reader title:

**«Отступники: отступничество, падение, восстановление и стойкость веры»**

## Part I

Preserve the previously proposed stable flagship route where possible:

`/articles/otstuplenie-chto-govorit-bibliya/`

H1:

**«Отступничество: что Библия на самом деле называет отпадением от веры»**

Research source:

`98_PART_I_WHAT_IS_APOSTASY_QUOTATION_FREE_DRAFT_2026-10-01.md`

Editorial map:

`104_PART_I_SOURCE_ANNOTATION_AND_EDITORIAL_FREEZE_MAP_2026-10-02.md`

## Part II

`/articles/otstupniki-biblii-iuda-saul-ierovoam-dimas/`

H1:

**«Отступники Библии: Иуда, Саул, Иеровоам, Димас и разные траектории ухода от Бога»**

Research source:

`99_PART_II_BIBLICAL_APOSTATES_AND_TRAJECTORIES_QUOTATION_FREE_DRAFT_2026-10-01.md`

Editorial map:

`105_PART_II_SOURCE_ANNOTATION_AND_EDITORIAL_FREEZE_MAP_2026-10-02.md`

## Part III

`/articles/petr-i-iuda-padenie-ili-otstuplenie/`

H1:

**«Пётр и Иуда: падение или отступничество?»**

Research source:

`97_PART_III_PETER_JUDAS_FALL_VS_APOSTASY_QUOTATION_FREE_DRAFT_2026-10-01.md`

Editorial map:

`103_PART_III_SOURCE_ANNOTATION_AND_EDITORIAL_FREEZE_MAP_2026-10-01.md`

## Part IV

`/articles/otreklis-ot-hrista-istoriya-cerkvi/`

H1:

**«Отреклись от Христа: падение, возвращение и отступничество в истории Церкви»**

Research source:

`100_PART_IV_CHURCH_HISTORY_LAPSE_RECANTATION_RESTORATION_QUOTATION_FREE_DRAFT_2026-10-01.md`

Editorial map:

`106_PART_IV_SOURCE_ANNOTATION_AND_EDITORIAL_FREEZE_MAP_2026-10-02.md`

## Part V

`/articles/kogda-chelovek-uhodit-ot-very/`

H1:

**«Когда человек уходит от веры: как предупреждать, исправлять, возвращать и не давать ложной надежды»**

Research source:

`101_PART_V_PASTORAL_RESPONSE_WARNING_RESTORATION_AND_PERSEVERANCE_QUOTATION_FREE_DRAFT_2026-10-01.md`

Editorial map:

`107_PART_V_SOURCE_ANNOTATION_AND_EDITORIAL_FREEZE_MAP_2026-10-02.md`

---

# 4. Architecture supersession rule

`85_...` supersedes `14_...` **for initial reader-facing architecture**.

Therefore Product must not automatically create seven initial deep-dive routes for:

- Judas standalone;
- Luke 8 standalone;
- Heb 6 standalone;
- Heb 10 standalone;
- 2 Pet 2 standalone;
- Jude standalone.

Those technical dossiers remain high-value evidence owners and can become later deep dives if:

- search intent warrants it;
- internal-link structure benefits;
- content is not thin/duplicative;
- Product receives separate authorization.

Do not delete the old route ideas; classify them `FUTURE-DEEP-DIVE / NOT INITIAL FIVE-PART SERIES`.

---

# 5. Hub requirements

The hub `/apostasy/` should be a `series`-type page using the site’s native series infrastructure rather than a new framework.

Required blocks:

1. Hero/title/subtitle.
2. One-paragraph “why this series exists.”
3. Canonical tension: warnings ↔ preservation promises.
4. Five article cards in frozen reading order.
5. Key distinctions:
   - grievous fall;
   - recoverable wandering;
   - temporary faith;
   - privilege without proven saving union;
   - doctrinal/practical denial;
   - corporate apostasy;
   - hardening;
   - final repudiation;
   - restoration/preservation.
6. Method box:
   `text → context → original-language issue when material → competing readings → whole-canon synthesis → pastoral application`.
7. Source-policy note.
8. `CollectionPage.hasPart` only for routes actually published.

### Visual master

Preferred canonical image concept from earlier blueprint:

> **Two plots of ground under the same rain: one fruitful, one producing thorns (Heb 6:7–8).**

Do not use an image that visually presupposes a disputed reading of John 15 as the series master metaphor.

---

# 6. Internal-link graph

## Hub

Links to all five parts.

## Part I

Must link:

- Part II when moving from categories to cases;
- Part III where Peter/Judas distinction is introduced;
- Part V at warning/restoration application.

Optional contextual links to future technical deep dives should remain disabled until those routes exist.

## Part II

Must link:

- back to Part I for taxonomy;
- forward to Part III as the central “fall vs final apostasy” question;
- Part V where corrective discipline / false teachers / final-state restraint becomes pastoral.

## Part III

Must link:

- Part I for taxonomy;
- Part II for Judas/Saul/false-teacher case context;
- Part IV for historical recantation/restoration analogues;
- Part V for present pastoral response.

## Part IV

Must link:

- Part III for biblical control on denial/restoration;
- Part V for church response.

## Part V

Must link:

- Part I for definitions;
- Part III for Peter/Judas and recoverability;
- Part IV for historical illustrations where used.

### End navigation

Every article should have:

- previous part;
- next part;
- hub.

Part I: no previous, next = II.

Part V: previous = IV, no next, hub CTA.

---

# 7. Source-note conversion requirements

The Research drafts contain `Editorial source notes` with internal Research filenames. These are **not reader-facing Product citations**.

Product intake must convert them into restrained reader/source notes.

## Reader body

Keep quotation-free by default.

Use:

- Scripture references inline;
- Hebrew/Greek only where it prevents a real interpretive error;
- no decorative academic parentheticals every paragraph.

## End/source block

Each article should provide a concise source block with categories such as:

### Biblical/exegetical controls

Major passages and, where needed, technical commentaries/articles.

### Historical/confessional controls

Only where relevant.

### Primary historical documents

Part IV especially.

### Further technical reading

Optional; should point to high-quality conservative/technical sources rather than TGC brand pages by default.

## Do not expose

Do not publish internal Research filenames or status labels to ordinary readers.

---

# 8. Source hierarchy Product must preserve

## 1. Scripture / original languages / textual apparatus

Highest authority.

## 2. Technical conservative exegesis

Claim-dependent examples:

- Thomas Schreiner;
- Douglas Moo;
- D. A. Carson;
- Darrell Bock;
- David Peterson;
- Eckhard Schnabel;
- William Mounce;
- George Knight;
- Abner Chou;
- Iosif Zhakevich.

Gordon Fee may be used for technical grammatical/exegetical contribution where useful without automatic adoption of confessional conclusions.

## 3. TMS / Shepherds / GTY

Strong conservative canonical/pastoral controls; not substitutes for primary exegesis.

## 4. Reformed/confessional synthesis

Sproul, Ferguson, Reformed Baptist confessions and major Reformed sources claim-by-claim.

## 5. Puritan practical theology

- Owen;
- Watson;
- Brooks;
- Flavel;
- Sibbes;
- Charnock.

Frozen rule:

> **Scripture establishes the exegetical claim; Puritan practical theology traces the anatomy of the soul under that truth.**

---

# 9. TGC rule — Product lock

Do not use “The Gospel Coalition says…” as a doctrinal warrant.

If a useful article is hosted by TGC:

- identify the actual author;
- evaluate that author’s claim;
- prefer/confirm with the author’s technical work or the primary text where available;
- do not infer compatibility with site theology merely from TGC hosting.

The same claim-by-claim discipline applies to friendly platforms; platform brand never replaces exegesis.

---

# 10. Final-state confidence lock

Product copy must preserve the Research confidence ladder.

## Explicit/high-confidence terminal

Judas Iscariot and texts where Scripture itself supplies corresponding finality.

## Severe / hard warning texts with disputed prior-saving status

Heb 6; Heb 10; 2 Pet 2 and related nodes according to dedicated dossiers.

## Severe trajectory, final eternal state not narrated

- Saul;
- Solomon;
- Demas;
- several historical cases.

## Corporate/institutional judgment

- Jeroboam system;
- Israel / 2 Kings 17.

### Hard lock

> **Narrator strength sets editorial strength.**

Product editors/agents must not make titles, SEO descriptions, summaries, cards or FAQ answers stronger than the article body on final-state certainty.

This specifically prohibits reintroducing the patched phrase “дороги к погибели” into Part II metadata.

---

# 11. Hard-text locks

## Luke 8:13

Do not rewrite “believe for a time” as “never believed in any sense.”

Do not make `πιστεύω` alone settle saving faith.

## Heb 6

Do not trivialize experiences; retain 6:9 control.

## Heb 10:29

Do not hide `ἡγιάσθη`; preserve referent dispute.

## 2 Pet 2

Keep bought / knowledge / escape / defeat / dog-sow nodes distinct.

## Jude

Remain variant-safe in 5 and 22–23.

## Revelation

- Rev 3:5: do not invert negative promise into automatic erasure narrative;
- Rev 22:14: disclose material variant if exact wording is used argumentatively;
- Rev 22:19: critical wording = tree of life / holy city, not `book of life` as doctrinal proof.

---

# 12. Pastoral locks

Product must preserve:

- no false assurance to settled repudiation;
- no premature final judgment where Scripture commands restoration;
- gentleness without doctrinal vagueness;
- protection of flock from destructive teachers;
- discipline ≠ infallible declaration of eternal decree;
- forgiveness/fellowship/trust/office qualification are distinct;
- weak/bruised believers ≠ final apostates;
- presumption and despair are opposite errors;
- perseverance = divine preservation through living faith and appointed means, not carnal security.

Do not add universal office-restoration timelines or family-case rules without a separate evidence dossier.

---

# 13. Historical locks — Part IV

Primary documents own historical facts wherever possible.

Must preserve:

- Pliny = visible former-Christian/public repudiation evidence, not proof of former regeneration;
- Quintus = fall under fear, final state unknown;
- Cyprian/lapsi = gravity + penitential/restoration category;
- Ninus/Clementianus/Florus = confession → torture → lapse → prolonged repentance/restoration consideration;
- Julian = public Christian-identity-to-pagan/anti-Christian trajectory; disputed formation details attributed;
- Cranmer = documented recantation + public repudiation of recantation; do not make archives prove regeneration;
- Spira = recantation/despair/reception-history case, not inspired proof of unforgivable sin or reprobation.

Do not use Foxe, Gregory or later Spira retellings as neutral sole witnesses where the claim can be primary-source controlled.

---

# 14. Puritan deployment lock

Use Puritans where they are strongest:

- Owen — apostasy/decay/common operations/preservation means;
- Watson — repentance/false peace/presumption;
- Brooks — temptation masks/small tolerated sins/despair;
- Flavel — first declensions/backsliding/recovery;
- Sibbes — bruised/weak grace and anti-despair;
- Charnock — practical denial / profession contradicted by life.

Do not add Puritan names for density.

Direct quotes require exact work/section/page custody. Paraphrase from frozen primary sections is safer for initial publication.

---

# 15. SEO/meta do-not-improvise rules

Metadata must not simplify the theology beyond the article.

Forbidden SEO formulations:

- “Все отступники никогда не верили вообще.”
- “Любой истинный христианин может потерять спасение.”
- “Евр. 6 окончательно доказывает X” without model/context qualification.
- “Саул потерял спасение.”
- “Димас погиб.”
- “Публично отрёкшийся автоматически не может вернуться.”
- “Настоящий верующий никогда серьёзно не падает.”

SEO title/description may ask strong questions; answer snippets must retain the article’s distinctions.

---

# 16. Product implementation gates

Before merge/deploy Product must verify:

1. route collision / redirects;
2. article schema and series hub schema;
3. breadcrumbs;
4. `CollectionPage.hasPart` only for published items;
5. previous/next/hub links;
6. mobile reader layout;
7. TOC anchors;
8. source-note rendering;
9. Greek/Hebrew glyph rendering;
10. no broken internal links to unpublished future deep dives;
11. metadata does not exceed final-state/source certainty;
12. build / lint / relevant tests;
13. release witness on live route after deployment.

---

# 17. What Product must NOT copy verbatim

Do not copy these Research-only artifacts into public body content:

- `Status:` labels;
- `Evidence owners:` filenames;
- `Editorial source notes — remove/convert before publication` headings;
- internal P0/P1 terminology unless pedagogically useful;
- Research commit SHAs;
- internal source-trust tiers as bureaucratic labels.

Translate research controls into clean reader prose/source notes.

---

# 18. Product content source of truth

For prose:

- Part I → `98_...` at/after commit `54015ad1d81da360f77f2db90e52ddcf5372c470`.
- Part II → `99_...` at/after commit `bc7e47eed80e9d1c2929fe7031ba08c799f6edcb`.
- Part III → `97_...` at/after commit `7b6d372252f2503d1f7a5ed2ce63e6c4f54d3791`.
- Part IV → `100_...` at/after commit `2d5913faf55afb578137604254c5962e41cf72fc`.
- Part V → `101_...` at/after commit `194fba4aaf87e67e2555990f2560c20f4404d468`.

For guardrails:

- maps `103–107`;
- `108` final source/editorial gate;
- `109` contradiction audit;
- `110` merge check.

For difficult claims:

- use dedicated dossier, not memory or generic web summary.

---

# 19. Handoff stop rule

Once Product begins intake:

- do not let a Product agent rewrite theology from scratch;
- do not let it browse for a “better” simplified answer and replace Research conclusions;
- do not reopen broad Research because wording feels long;
- shorten only by preserving thesis + evidence + nearest guardrail;
- if a Product edit creates a new theological claim, route that exact claim back to Research for adjudication.

---

# 20. Exact next action

> **Product intake may now begin from the five source-of-truth drafts above. First create/verify the `/apostasy/` series hub and five routes without publishing, map each route to its source draft, convert Research source notes into reader-facing notes, preserve all locks in this handoff, run Product build/accessibility/internal-link checks, then obtain a release witness before live publication. Technical Heb 6 / Heb 10 / 2 Pet 2 / Jude dossiers remain evidence backbone and are not mandatory initial public routes.**

**Research → Product status: `HANDOFF READY / NO PRODUCT WRITE PERFORMED`.**