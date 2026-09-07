# Product-Repo Architecture Fit Audit — Trilogy vs Hybrid

**Status:** READ-ONLY PRODUCT ARCHITECTURE AUDIT / RESEARCH ONLY / NOT PUBLICATION  
**Date:** 2026-09-07  
**Research lane:** `80+` compression/architecture.  
**Product repo inspected read-only:** `FedorMilovanov/gb-is-my-strength@main`.  
**Concurrency:** adult-child/prodigal agent remains active in `66–79`; this file does not edit or reinterpret its source files.

---

# 0. Question

Modules `81`, `85`, and `86` left two leading publication architectures:

1. **three-part core series + separate adult-child companion**;
2. **one flagship + church companion + adult-child companion**.

Content alone did not decisively choose between them.

This audit asks what the existing product repository can support **natively**, without inventing a new content engine or creating a one-off architecture.

---

# 1. Product policy/architecture facts

`gb-is-my-strength` is already an Astro 6 + MDX/content-collections production site.

Relevant product rules observed in `AGENTS-REFERENCE.md`:

- production comes from Astro/MDX source and generated `dist/`;
- new work must respect existing route/content architecture;
- no casual parallel architectural expansion;
- article/series mutation must run repository validations and obey current source/editorial policy;
- product mutations require a bounded owner lane and overlap check.

### Consequence

Research markdown must **not** be copied directly into product paths.

A publication lane must later:

- re-read current product rules at exact product head;
- check active product PRs;
- create article MDX under the established content model;
- update only the canonical series/route registries required by that model;
- run product validation/CI.

---

# 2. Native article schema already supports both series and companions

`src/content.config.ts` defines article fields including:

- `series?: string`;
- `related: string[]`;
- tags;
- reading time;
- source mode;
- publication/draft/noindex states.

Therefore the product already has the two relationships this project needs:

1. **ordered series membership**;
2. **non-series related/companion references**.

No new frontmatter concept is required merely to express:

> three numbered core articles + one related adult-child companion.

---

# 3. Existing series registry is flexible

`data/series.json` already contains series of very different lengths/shapes:

- `pastor-series` — currently 2 published entries in registry;
- `nagornaya` — 5 parts;
- `dzhon-gill` — 6 entries including a reference work;
- `hard-texts` — 6 entries;
- `russian-baptism` — 10 entries;
- `genesis-6` — mixed numbering such as `6A` / `6B`.

### Implication

The product does **not** impose a fixed series length.

A three-part series is fully consistent with the existing registry model.

A companion does not need to be forcibly labeled “Part IV” merely to fit the data model.

---

# 4. Standard ArticleLayout already has native series progression

`src/layouts/ArticleLayout.astro`:

- reads `data.series`;
- uses `SERIES_ORDER`;
- resolves all articles belonging to the series;
- computes current `N из M` position;
- renders previous/next series navigation;
- renders a visual progress track.

This matters greatly.

The teen project does **not** need the specialized heavy `SeriesArticleLayout` or a new runtime to achieve a coherent trilogy.

### Required later product changes for a new ordinary series

Likely minimal structural set:

- MDX articles with the same `series` slug;
- add ordered slugs to `SERIES_ORDER`;
- add/update `data/series.json` if the registry/landing ecosystem requires it;
- route/landing work only to the extent current product policy requires or editorial strategy chooses.

Exact mutation list must be re-derived from then-current product head, not frozen here.

---

# 5. Specialized SeriesArticleLayout is not necessary for this project

The repository also contains `SeriesArticleLayout.astro` with:

- full sidebar rail;
- progress ring;
- all-series part navigation;
- previous/next cards;
- timeline/era presentation.

But it is currently heavily shaped around the historical `Баптисты России` experience.

The adolescent series does not need:

- historical era timeline;
- custom rail;
- 3D-map affordance;
- a parallel specialized visual world.

### Architecture principle

> **Do not turn a content decision into a new frontend subsystem.**

Use the normal article architecture unless a later UX audit proves a real missing capability.

---

# 6. Strongest existing precedent: pastor-series

The current `/pastor-series/` implementation contains an explicit architecture rule in source comments:

> numbered biblical/pastoral core + unnumbered documentary dossiers/field guides as companion materials.

Its landing page already distinguishes:

- published materials;
- numbered canonical core;
- accompanying tools / dossiers;
- materials that exist in research/manuscript state but are not yet public routes.

This is remarkably close to the teen-project need.

### Direct architectural analogy

For this project:

## Numbered core

1. **Hidden life / sinful desire / digital world / hardening**
2. **Parents / means / boundaries / truth / discovery / repentance**
3. **Church / children / worship / choir / youth access / holiness**

## Unnumbered companion

- **Adult child / prodigal / changed jurisdiction / contact / non-enabling / return**

Potential future tools/sidebars may remain unnumbered rather than inflating the core series.

---

# 7. Why the three-part core now beats one flagship + companions

Before product audit, hybrid and trilogy were nearly tied.

The product architecture changes the score.

## A. Native sequential navigation exists

Readers can receive:

- part number;
- series label;
- previous/next article;
- progress.

Thus the trilogy is not just editorial labeling; the site can actually carry the sequence.

## B. Existing site culture already understands numbered theological series

Examples:

- Nagornaya;
- John Gill;
- hard-texts;
- Russian baptism;
- pastor-series roadmap.

A three-part theological/pastoral sequence therefore fits reader expectations.

## C. Companion model also already exists conceptually

`pastor-series` proves the site can distinguish core from dossier/tool material.

The adult-child article does not have to be forced into the main sequence.

## D. One giant flagship would underuse the existing series capability

The original adolescent corpus contains at least three distinct but sequential questions:

`what forms the hidden life?`  
`what should parents do?`  
`what should church do?`

Trying to collapse them into one 10k–15k+ word page creates avoidable narrative density when the site already has a native sequence solution.

---

# 8. Why not five core parts

The product can technically support five.

But technical ability is not editorial necessity.

Five core pieces would likely separate:

- heart/temptation;
- digital world;
- parents;
- church;
- adult child.

Problems:

1. digital mechanics would risk becoming an autonomous technology-panic article separated from fallen-heart anthropology;
2. adult-child material changes jurisdiction and life stage enough to deserve companion status rather than mandatory continuation;
3. five numbered parts increase reader attrition;
4. the research structure would begin dictating publication structure.

### Verdict

**Do not use five merely because Research has enough material for five.**

---

# 9. Why adult-child/prodigal should be companion, not Part IV

This is now the most stable architecture conclusion.

Adolescent core assumes substantial parental shepherding jurisdiction.

Adult-child lane asks what happens **after that jurisdiction changes**.

It introduces new primary questions:

- honor vs obedience after adulthood;
- independent residence;
- contact cadence;
- no-contact requests;
- non-enabling aid;
- co-residence of adults;
- household property/resources;
- protection of younger siblings;
- church discipline vs enduring family duties;
- Luke 15 misuse;
- Romans 12 / James 5 after departure.

That is a new pastoral situation, not simply the next adolescent chapter.

### Strong editorial line

> **The series should explain how a hidden adolescent life is formed and shepherded. The companion should explain what love and truth look like when the parents can no longer shepherd by child-level authority.**

---

# 10. Why church material should remain Part III, not separate companion

Unlike adulthood, church is already part of the adolescent formation system.

The original project explicitly asks:

- what happens when church knows;
- whether unregenerate children are treated as exempt;
- whether openly rebellious children remain in choir;
- whether small-group/youth access can corrupt others;
- what tolerated hypocrisy teaches.

Therefore Part III is not an optional tangent.

It completes the progression:

`heart` → `home` → `church`.

Removing it into a companion would weaken the original thesis that adults/institutions around the child also bear real responsibilities.

---

# 11. Recommended publication architecture after product audit

## SERIES CORE — 3 numbered parts

### Part I — Hidden life

Working subject:

> sinful desire, temporary sweetness, secret peer world, smartphone/internet/pornography, lying, hardening, false profession vs grievous fall.

### Part II — Parents

Working subject:

> sovereignty + means, no moral neutral zone, formation, individual weakness, radical boundaries, non-provocation, trust, voluntary accountability, discovery and repentance.

### Part III — Church

Working subject:

> child responsibility, worship/hypocrisy, public Word vs trusted roles, choir/youth/small groups, corrupting influence, discipline, safeguarding, restoration.

## UNNUMBERED COMPANION — Adult child / prodigal

Working subject:

> adulthood changes jurisdiction, not morality; release control without releasing relationship; Luke 15 guard; contact; non-enabling; household conditions; younger siblings; restoration; Romans 12 / James 5; sovereign hope.

---

# 12. Optional future companion materials

Do not create now merely because possible.

Potentially useful only if future reader need is demonstrated:

- practical parent/pastor `first response after discovery` guide;
- sextortion/safeguarding emergency guide;
- church children’s-choir/youth-access policy appendix;
- parent self-audit / conversation guide.

These should remain **tools**, not numbered theological core.

---

# 13. Landing-page recommendation

The product already has precedent for a dedicated series landing.

A later product lane should evaluate a modest teen-series landing that:

- states the core question;
- shows Parts I–III;
- lists adult-child companion separately;
- clearly labels publication/draft state;
- avoids pretending research manuscripts are already public;
- links source/editorial methodology if useful.

### Guard

Do not build a new bespoke frontend theme merely for this series.

Reuse existing cards/layout patterns unless a product-design audit demonstrates a gap.

---

# 14. Related-field note

The content schema already contains `related[]`.

Even if its current rendered use is incomplete or indirect in some routes, the data model is already prepared for companion relationships.

Therefore the adult-child article should likely be related to:

- Part II strongly;
- Part III where church discipline/family duties intersect;
- Part I only where hidden adolescent history is necessary context.

Do not duplicate the adult-child material into all three core articles merely for discoverability.

---

# 15. Product mutation guard

This audit is **read-only**.

No product file was changed.

Before actual product authoring:

1. inspect current `gb-is-my-strength` head again;
2. read current `AGENTS.md` + relevant `AGENTS-REFERENCE` article/series/source sections;
3. inspect active product PRs and shared-file overlap;
4. claim an explicit owner lane;
5. decide article slugs/series slug;
6. create a publication source packet;
7. draft one part at a time;
8. update series registries only in that product lane;
9. run required validation/audit gates;
10. merge only on exact-head evidence.

Concurrent Research work is not permission to mutate product repo concurrently without that check.

---

# 16. Updated architecture score

| Architecture | Before product audit | After product audit |
|---|---:|---:|
| 3-part core + adult companion | 9.1/10 | **9.7/10** |
| flagship + church/adult companions | 9.0/10 | **8.8/10** |
| 5-part series | 8.1/10 | **8.0/10** |
| one all-inclusive flagship | 7.3/10 | **6.8/10** |

Scores are editorial heuristics, not empirical measurements.

---

# 17. Final architecture verdict

> **Recommended: three numbered core articles plus an unnumbered adult-child/prodigal companion.**

This is not merely the cleanest editorial theory.

It is also the architecture that best matches the product repository’s existing native capabilities and established series/companion precedent **without requiring a new frontend subsystem**.

The next Research task should therefore be compression into a **selected-source packet for Part I**, not more uncontrolled thematic expansion.