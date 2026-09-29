# Серия «Отступничество и стойкость веры» — Product blueprint V2

**Дата:** 2026-09-30  
**Статус:** `PROPOSAL / RESEARCH-ONLY / DO NOT IMPLEMENT / PUBLICATION_HOLD`  
**Развивает, а не заменяет:** `apostasy/07_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-09-29.md`  
**Research spine:** `apostasy/00_MASTER_RESEARCH_MAP_2026-09-29.md`  
**Product checked:** `FedorMilovanov/gb-is-my-strength` `main`, включая текущий `/hard-texts/` series pattern.

> Этот документ решает **где и как** разложить уже накопившееся исследование. Он не разрешает создавать routes в Product до evidence closure и отдельного release witness.

---

## 1. Что подтвердил повторный Product audit

Текущий `/hard-texts/` остаётся хорошим native pattern:

- `page.type = 'series'`;
- JSON-LD `CollectionPage`;
- `hasPart` на дочерние `Article`;
- breadcrumbs;
- series-specific hero/metadata;
- reader/TOC infrastructure уже есть в Product.

Следовательно, **не нужен новый content framework** и не нужен Teletype-first подход. Для этой темы правильна та же модель: hub + самостоятельные статьи.

---

## 2. Главная архитектурная поправка после новых исследований

V1 предполагал 4–5 статей и возможный общий hard-text материал. После отдельных dossier по Jude и особенно 2 Пет. 2 стало ясно:

- **2 Пет. 2 заслуживает собственного deep dive**;
- Послание Иуды содержит достаточно самостоятельной структуры для отдельной статьи, но его route следует открывать только после P0 text-critical closure;
- case matrix не надо превращать в десяток маленьких статей про Димаса/Саула/Ананию — это будет thin-content fragmentation;
- flagship должен владеть **общим вопросом**, а deep dives — конкретными search intents.

Итоговая рекомендуемая серия: **hub + 6 обязательных articles + 1 условный Jude article**.

---

## 3. Search-intent ownership — чтобы статьи не каннибализировали друг друга

| Page | Единственный главный вопрос | Что туда НЕ складывать |
|---|---|---|
| `/apostasy/` | «Что входит в серию и как связаны отступничество/стойкость?» | полный экзегетический спор любого hard text |
| flagship | «Может ли истинно верующий окончательно отпасть / потерять спасение? Как Библия соединяет warnings и preservation?» | длинные Greek word studies Евр. 6/10/2 Пет. 2 |
| Judas Iscariot | «Был ли Иуда когда-либо спасительно верующим?» | Послание Иуды; общий трактат о perseverance |
| Temporary faith | «Что значит “до времени веруют” и как временная вера отличается от спасительной?» | полный Judas dossier; Heb 6 lexical monograph |
| Hebrews 6 | «Кто просвещён, вкусил, стал `μέτοχος` Духа и отпал?» | широкий обзор всех case studies |
| Hebrews 10 | «Кто “освящён кровью завета” и что такое сознательная апостасия?» | 2 Pet atonement debate |
| 2 Peter 2 | «Кого “купил Владыка”; что значат `ἐπίγνωσις`, escape и dog/sow return?» | общий definite-atonement article |
| Jude (conditional) | «Как в Иуде соединены “храните себя” и Бог, Который хранит; что делает Jude 5?» | повтор flagship conclusion без Jude-specific exegesis |

Главное правило: **один search intent — один canonical owner**. Остальные статьи дают краткий crosslink, а не заново переписывают тот же раздел.

---

## 4. Series hub

### Route

`/apostasy/`

### Reader title

**«Отступничество и стойкость веры»**

### Role

Hub должен отвечать не «кто прав?», а «какие вопросы и тексты здесь разбираются, в каком порядке читать».

### Required blocks

1. Hero: 2–3 предложения без конфессионального лозунга.
2. `Canonical tension`: warnings ↔ preservation promises.
3. `Key distinctions`: временная вера / служебные дары / заветные привилегии / тяжёлое падение / окончательная апостасия / стойкость.
4. Article cards с status/read-time.
5. «Как мы работаем с трудными текстами»: text → context → alternatives → synthesis.
6. Research/source policy note.
7. `CollectionPage.hasPart` только для **реально опубликованных** частей; не притворяться, что draft существует публично.

### Visual master

Два участка земли под одним дождём: один приносит плод, другой — терния (Евр. 6:7–8). Это лучше виноградной лозы как master-image, потому что не заставляет hub заранее принять одно чтение Ин. 15.

---

## 5. Article 1 — flagship synthesis

### Route

Сохранить V1 route:

`/articles/otstuplenie-chto-govorit-bibliya/`

### Рабочий H1

**«Отступничество и стойкость: может ли истинно верующий окончательно отпасть?»**

### Search intent

Broad doctrinal query: «можно ли потерять спасение», «может ли верующий отпасть», но без FAQ-упрощения.

### Article job

- дать taxonomy, не доказывая всё одним стихом;
- wilderness pattern;
- temporary faith;
- service/gifts without saving grace;
- covenant/common operations;
- grievous fall vs final apostasy;
- warning passages as real means;
- preservation promises;
- visible church;
- 1 John 2:19 as retrospective diagnostic control;
- Jude 20–24 as compact synthesis;
- confessional/historical spectrum.

### Must-link deep dives

Judas → temporary faith → Heb 6 → Heb 10 → 2 Pet 2 → Jude (если опубликован).

### Do not say

- «Все отступники просто никогда ничего реального не переживали».
- «Если человек тяжело пал, он доказанно никогда не был верующим».
- «Предупреждения гипотетичны и фактически никому не угрожают».
- «Сильный язык переживаний автоматически = justification/regeneration».

---

## 6. Article 2 — Иуда Искариот

### Route

Сохранить V1:

`/articles/iuda-izbrannyy-apostol-no-ne-spasennyy/`

### Preferred H1

**«Иуда Искариот: апостольское служение без спасительной веры?»**

Вопросительный знак лучше рубленого «но не спасённый» в slug: route может оставаться стабильным, H1 — более экзегетически открытым.

### Must-prove

- real apostolic office/ministry;
- John 6:64/70–71 as internal control;
- John 13:10–11,18 distinction;
- John 12:6 hidden greed;
- Matt 27 `μεταμεληθείς`: remorse ≠ lexical magic proof;
- Acts 1:17 real share in ministry;
- office/election-to-service ≠ election-to-salvation.

### Strong counter-question

Does John 17:12 (“those whom you gave me... son of perdition”) imply Judas belonged to saving “given ones”? Must answer, not skip.

### Pastoral guardrail

Judas is not template for declaring every fallen minister damned; his canonical biography contains unique explicit controls.

---

## 7. Article 3 — временная вера

### Route

`/articles/vremennaya-vera-i-stoykost-svyatyh/`

### H1

**«“До времени веруют”: временная вера, ложная уверенность и стойкость»**

### Corpus ownership

- Luke 8:13 / Synoptic soils;
- Simon Magus Acts 8;
- John 2:23–25;
- John 8:30ff as difficult discourse;
- 1 John 2:19 / 2:24–28;
- 1689 14.3 / Dort temporary faith;
- Owen/Watson/Edwards only as historical explanatory layers.

### Key thesis

Do not deny the reality of `πιστεύουσιν`. Ask what kind of faith the context describes: it lacks root and endurance.

### Do not absorb

Heb 6 must only be compared briefly; its experiential language is stronger and deserves its own article.

---

## 8. Article 4 — Евр. 6

### Route

`/articles/evreyam-6-4-8-vkusili-i-otpali/`

### H1

**«Евреям 6:4–8: кто “вкусил небесного дара” и отпал?»**

### Non-negotiable structure

1. 5:11–6:3 context before 6:4.
2. Each descriptor separately.
3. `γεύομαι`: explicitly reject “merely nibbled” shortcut because Heb 2:9.
4. `μέτοχος`: full Hebrews usage.
5. `παραπεσόντας` / impossibility.
6. land/rain 6:7–8.
7. crucial 6:9 — “better things, belonging to salvation.”
8. 6:10–20 assurance/oath/hope/anchor.
9. major interpretation matrix.
10. relation to entire Hebrews warning trajectory.

### Counter-readings required

- true believers lose salvation;
- covenant/common-operations model;
- warnings-as-means/prospective model;
- hypothetical reading (likely weak, but document why);
- other minority proposals if academically significant.

---

## 9. Article 5 — Евр. 10

### Route

`/articles/evreyam-10-26-31-osvyashchennyy-krovyu-zaveta/`

### H1

**«Евреям 10:26–31: кто “освящён кровью завета” и почему ему грозит суд?»**

### Must-prove

- 10:19–25 before 10:26: drawing near, confession, assembly, mutual exhortation;
- deliberate ongoing rejection is not “every consciously committed sin”;
- triple insult in 10:29;
- `ἐν ᾧ ἡγιάσθη` competing referents/readings;
- Christ-referent (Owen/Gill) must not be presented as grammar-proven;
- apostate/covenantal-sanctification reading;
- saving-sanctification/loss reading;
- 10:32–39 and explicit ending 10:39;
- relation to 6 and 12.

### Pastoral box

«Что этот текст НЕ говорит человеку, который боится, что случайно потерял спасение» — only after exegesis, not sentimental override.

---

## 10. Article 6 — 2 Петра 2

### Route recommendation

Prefer a shorter stable route than the first research candidate:

`/articles/2-petra-2-vladyka-kupil-ih/`

### H1

**«2 Петра 2:1, 20–22: кого “купил Владыка” и что означает их возвращение?»**

### Why standalone now

Research crossed the threshold: the passage simultaneously raises perseverance and atonement questions, and contains independent lexical nodes (`δεσπότης`, `ἀγοράζω`, `ἐπίγνωσις`, `ἀποφεύγω`). Folding it into a generic hard-text roundup would either flatten it or make flagship bloated.

### Required view matrix

A. covenantal/nonsoteriological purchase;  
B. phenomenological/professional purchase;  
C. actual atoning purchase without automatic saving application;  
D. actual saving redemption + final apostasy.

### Guardrails

- same strong `ἐπίγνωσις` also occurs positively in ch.1;
- `ἀποφεύγω` marks real escape;
- washed sow means real cleaning occurred at some level;
- dog/sow still strongly contributes a nature/reversion argument;
- `bought` alone does not prove prior justification;
- do not let definite-attempt doctrine decide lexicon before exegesis.

---

## 11. Article 7 — Jude (conditional but now likely warranted)

### Route candidate

`/articles/poslanie-iudy-otstuplenie-i-stoykost/`

### H1

**«Послание Иуды: “храните себя” — и Бог, Который может сохранить»**

### Why still conditional

The dossier is sufficiently rich, but two text-critical P0 nodes remain:

- Jude 5 (`Ἰησοῦς / κύριος / θεός`);
- Jude 22–23 variants.

Do not open the route until apparatus-level closure is recorded.

### Unique value

Jude alone compresses:

- kept/called people;
- intruders without Spirit;
- wilderness judgment;
- `τηρέω` wordplay;
- self-keeping command;
- ecclesial rescue;
- divine keeping doxology.

### Lexical quality-control box

Explicitly note: v.21 `τηρέω`, v.24 `φυλάσσω`; theological parallel, **not identical verb**.

---

## 12. What NOT to turn into standalone pages

Do **not** create individual short articles at this stage for:

- Demas;
- Hymenaeus/Alexander;
- Hymenaeus/Philetus;
- Saul;
- Balaam;
- Ananias/Sapphira;
- Esau.

They belong in flagship comparative-case section unless one later acquires independent search demand + enough primary exegetical material.

This avoids:

- thin content;
- duplicated doctrine;
- internal-link noise;
- maintenance drift;
- article count masquerading as research depth.

---

## 13. Romans 11, John 15, Gal 5, Rev 2–3 — placement decision

These texts are important but **do not need separate routes yet**.

### Phase 1

Flagship contains compact sections with honest unresolved flags.

### Phase 2 trigger for standalone article

Create a new deep dive only if all three conditions hold:

1. research dossier > substantial independent argument;
2. distinct user/search question not already owned by flagship;
3. source-to-claim closure strong enough to justify maintenance cost.

Likely candidates later:

- John 15 branches;
- Romans 11 branches/cutting off.

Gal 5:4 and Rev 2–3 more naturally remain sections until corpus proves otherwise.

---

## 14. Internal-link graph

### Hub

Links to every published article, ordered pedagogically.

### Flagship

Links to all deep dives at first substantive mention of their hard text.

### Every deep dive

Must link:

- up to `/apostasy/`;
- to flagship;
- to **only 2–3 closest sibling articles** contextually, not every article mechanically.

Suggested semantic links:

- Judas ↔ temporary faith;
- temporary faith ↔ Heb 6;
- Heb 6 ↔ Heb 10;
- Heb 10 ↔ 2 Peter 2;
- 2 Peter 2 ↔ Jude;
- Jude ↔ flagship.

At article end: compact “В серии” navigator can expose all parts without stuffing prose links.

---

## 15. Release order V2

### Recommended order

1. **Judas Iscariot** — most narratively accessible, dossier mature.
2. **Temporary faith** — establishes categories readers need.
3. **Hebrews 6** — famous hard text, categories now in place.
4. **Hebrews 10** — deeper covenant/sanctification node.
5. **2 Peter 2** — requires more atonement/source closure but now standalone-worthy.
6. **Flagship + `/apostasy/` hub** — synthesize only after deep dives stabilize wording.
7. **Jude** — either before flagship if P0 text criticism closes early, or immediately after flagship.

### Why flagship is not first

Writing synthesis before hard texts close creates downstream rewrite pressure. Better let deep dives determine the exact boundaries of the flagship claims.

---

## 16. Standard article evidence contract

Every article needs a local claim ledger before Product transfer:

| Field | Required |
|---|---|
| Reader-facing claim | exact sentence or atomic proposition |
| Biblical locus | verse/context |
| Text-critical state | stable / variant / disputed |
| Exegetical confidence | high / medium / open |
| Primary historical locator | if historical attribution used |
| Strongest contrary reading | named and represented fairly |
| Why rejected/limited | actual argument, not label |
| Rights/translation state | especially long quotations |
| Publication status | HOLD / CANDIDATE / PROMOTE |

No article can become `PUBLICATION-CANDIDATE` merely because prose sounds finished.

---

## 17. Reader-facing structure shared by all deep dives

1. **Question**, not confessional verdict.
2. **Text in context**.
3. **What the wording actually says**.
4. **Why the text is difficult**.
5. **Major readings**.
6. **Evaluation**.
7. **Canonical synthesis**.
8. **What the passage does NOT prove**.
9. **Pastoral implication**.
10. **Sources / further reading**.
11. **Series navigation**.

This structure matches the site’s serious-seminary-but-readable goal better than polemical “5 reasons Calvinists are right.”

---

## 18. Distribution layers

### gospod-bog.ru

**Canonical**. Full apparatus, updates, internal links.

### Telegram

Derivative entry post:

- one hard question;
- one central exegetical insight;
- one or at most two verified historical quotations;
- canonical link;
- no 70-link apparatus.

### Teletype

Optional readable adaptation, never independent research master. Must point to canonical site article and not silently drift when canonical article changes.

---

## 19. Visual system by article

- **Series hub / flagship:** two fields under one rain (Heb 6:7–8).
- **Judas:** abandoned place / coins / receding figure; no speculative face-of-Judas “portrait.”
- **Temporary faith:** young growth over shallow stone/rock with sun/heat, restrained and non-cartoonish.
- **Heb 6:** rain, fruitful land vs thorns — tighter symbolic frame than hub.
- **Heb 10:** approach to sanctuary/light vs deliberate turning away; avoid depicting God.
- **2 Peter 2:** clean water/washed surface leading back toward mire; avoid literal gross dog-vomit cover.
- **Jude:** storm-dark sea / wandering light / guarded path; visual should hold judgment + preservation tension.

No text baked into source art; title remains HTML.

---

## 20. Product implementation gate

**Do not touch Product now.** Before route creation:

- article-specific research reaches `PUBLICATION-CANDIDATE`;
- P0 text-critical/lexical gaps close;
- source-to-claim ledger exists;
- exact historical quote locators close;
- Russian translations labelled editorial where necessary;
- current Product article/series standards are re-read from the then-current `main`;
- route/search/sitemap/feed/index registrations are enumerated;
- exact-head validators/CI pass;
- release witness explicitly authorizes publication.

Research file/green check ≠ live release.

---

## 21. V2 decision

**Recommended final architecture:**

- 1 hub `/apostasy/`;
- 6 mandatory deep/synthesis articles;
- Jude as a seventh article once its two textual P0 nodes close;
- no micro-articles for every biblical character;
- flagship written late, after hard-text articles fix the doctrinal boundaries;
- Product untouched until publication gate.

This is now a sufficiently precise information architecture to guide article drafting without creating duplicate routes or theological drift.
