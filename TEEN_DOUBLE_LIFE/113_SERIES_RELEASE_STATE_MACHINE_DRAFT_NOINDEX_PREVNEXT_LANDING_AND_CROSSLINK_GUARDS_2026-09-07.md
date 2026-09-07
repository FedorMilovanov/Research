# Series Release State Machine — Draft / Noindex / Prev-Next / Landing / Cross-Link Guards

**Status:** PRODUCT-RELEASE DESIGN / RESEARCH ONLY / NO PRODUCT MUTATION  
**Date:** 2026-09-07  
**Depends on:** `110_PUBLICATION_TRANSFER_MANIFEST...`, `111_CROSS_PART_DEDUPLICATION...`, `112_READER_FACING_BIBLIOGRAPHY_BUDGET...`  
**Product architecture observed read-only:** `gb-is-my-strength` Astro/MDX content model, `ArticleLayout`, `SERIES_ORDER`, `data/series.json`, existing series landings.

---

# 0. Why this file exists

The series is intended to be written and released one article at a time.

That creates a technical/editorial danger:

- Part I may be public while Part II exists only as a draft;
- series navigation may know about entries that readers should not reach;
- a landing may accidentally link to a `noindex` manuscript;
- `related[]` may point at a future slug that has no public route;
- a progress indicator can claim `1 из 3` while two parts are not actually public;
- search/sitemap/feed can disagree with the visible series state.

The goal is simple:

> **A reader should never discover a publication-state inconsistency merely because the internal roadmap is ahead of the public site.**

---

# 1. Observed product behavior that matters

The standard content schema supports:

- `series`;
- `related[]`;
- `draft`;
- `noindex`;
- publication dates;
- source-required state.

The standard `ArticleLayout` resolves series neighbors from content entries associated with the series and an explicit `SERIES_ORDER`.

Existing product culture also distinguishes:

- public published series material;
- planned/draft roadmap material;
- companion material.

### Consequence

The internal existence of Part II/III must not automatically make them **public series members**.

Publication state and research/manuscript state are separate contracts.

---

# 2. Core invariant

At every public release state:

> **Every clickable series/related link from an indexable page must resolve to an intentionally public destination.**

Allowed exception:

- a clearly non-clickable roadmap/planned card may describe a future article if existing product patterns support it and no fake route is exposed.

Disallowed:

- published Part I → clickable Part II draft/noindex route;
- public landing → dead future slug;
- progress widget counting internal drafts as if published;
- related link to an unpublished companion;
- sitemap/feed entry for a deliberately hidden draft.

---

# 3. State definitions

Use four conceptual states independent of exact implementation names.

## R0 — Research only

No product manuscript/route.

Public state:

- nonexistent.

## R1 — Product manuscript, private publication state

Product manuscript exists for build/review.

Expected intent:

- `draft: true`;
- `noindex: true`;
- no public catalog/series/related wiring that makes it discoverable as released content.

Exact route behavior must follow then-current product architecture.

## R2 — Release candidate

Content/source/theology gates substantially complete.

Still not public until product/static/release gates pass.

Expected:

- remains fail-closed;
- no public navigation promises yet unless release is atomic with those changes.

## R3 — Published

Intentional public route with:

- indexable state according to product policy;
- final source list;
- catalog/search/series metadata as required;
- only valid public cross-links;
- exact-head terminal-green release evidence.

---

# 4. Series-wide release sequence

## Stage A — before Part I publication

Public site should contain **no accidental teen-series shell** merely because Research is complete.

Allowed:

- nothing public;
- or an intentionally designed general editorial/news teaser outside the article system, if separately justified.

Preferred default:

> no series landing until at least Part I is genuinely publishable.

Do not create empty SEO pages to reserve the series slug.

---

## Stage B — Part I published, Parts II–III not public

Public truth:

- exactly one article exists.

### Part I

May carry the intended series identity if current product model safely supports a one-member public series.

### `SERIES_ORDER`

Safest rule under the currently observed architecture:

> include only **publicly released core slugs** in the ordering consumed by public navigation.

Therefore at Stage B:

```text
[podrostok-za-kadrom-taynaya-zhizn]
```

not:

```text
[Part I, future Part II draft, future Part III draft]
```

### Public navigation

No fake “Следующая” to Part II.

### Landing

Two valid options:

#### Option B1 — no dedicated series landing yet

Part I lives in `/articles/` and carries series metadata internally/publicly as appropriate.

This is technically simplest.

#### Option B2 — modest landing exists

Landing shows:

- Part I as published/clickable;
- Parts II–III only as explicitly planned, **non-clickable** cards/titles if product precedent/policy allows;
- no reading-time/source-count claims for unfinished manuscripts unless already locked;
- no fake publication dates.

Existing `pastor-series` demonstrates the concept of visible planned/non-clickable roadmap material, but exact component reuse must be evaluated in a product lane rather than copied blindly.

---

## Stage C — Part II release candidate while Part I public

Part II may exist in product as R1/R2.

Public Part I must still behave exactly as Stage B.

Do **not** add Part II to public `SERIES_ORDER` early just to test navigation on production.

Test draft navigation in a build/review context without making the public site claim Part II is released.

### Atomic release bundle for Part II

When Part II actually releases, the minimal public-state mutation should make these consistent together:

- Part II route becomes public;
- series ordering becomes `[Part I, Part II]`;
- Part I gains valid next link;
- Part II gains valid previous link;
- landing/catalog shows Part II as published;
- search/feed/sitemap/derived registries update as current product tooling requires;
- any `related[]` links activated in the same release resolve publicly.

Do not split these across independent merges if doing so creates a temporarily false public state.

---

## Stage D — Part I + II public, Part III private

Public truth:

- series has two released parts.

Public navigation:

`Part I → Part II`

No clickable Part III.

Landing may show Part III as planned/non-clickable.

Part II conclusion may say:

> в следующей части мы рассмотрим ответственность церкви

but should avoid linking to a nonexistent URL.

A future title may be named as provisional only if editorially useful; avoid overpromising exact scope before final manuscript.

---

## Stage E — Part III release

Atomic public series state becomes:

`Part I ↔ Part II ↔ Part III`

At this point:

- series progression is complete;
- landing can present `3 части` as complete core;
- Part III may link to adult companion only if the companion is already public;
- otherwise adult companion remains an editorially described future related material without dead link.

---

# 5. Adult companion release sequence

The adult-child article is not part of numbered core progression by default.

Therefore its release should not mutate core `SERIES_ORDER` merely to gain visibility.

## Before companion is public

Do not place its future slug in public `related[]` if the renderer creates a link.

Part II/III prose may say generally:

> отдельный материал о взрослом ребёнке будет рассматривать изменившуюся родительскую юрисдикцию

without a dead URL.

## At companion release

Atomic relationship changes may include:

- companion route becomes public;
- companion `related[]` points to Part II/III as appropriate;
- Part II gains companion in `related[]`;
- Part III gains it only if the relation is genuinely useful;
- landing gains a clearly separate **Сопутствующий материал** card rather than `Часть IV`.

---

# 6. Draft/noindex invariant

`noindex` is not a substitute for non-discoverability.

A noindex page can still be:

- linked from public pages;
- visited by readers;
- shared;
- cached;
- mistaken for released material.

Therefore:

> **Do not knowingly link from released navigation to a draft merely because the draft says `noindex`.**

`draft` / `noindex` are fail-closed metadata, not permission to expose unfinished content.

---

# 7. Prev/next invariant

Public prev/next must describe **published sequence**, not editorial roadmap.

At release time verify from the rendered artifact, not merely source intent:

- Part I has no `prev`;
- Part I `next` exists only when Part II public;
- Part II `prev` points Part I;
- Part II `next` exists only when Part III public;
- Part III `prev` points Part II;
- Part III has no core `next` after core completion.

Adult companion is not the automatic `next` after Part III.

It belongs in related/companion UX.

---

# 8. Progress-language invariant

Do not claim completion against unpublished roadmap unless the UI explicitly distinguishes roadmap from publication.

Potentially misleading at Stage B:

> `1 из 3 опубликовано` displayed inside a generic reader progress component that normally means three navigable parts exist.

Safer depending existing component semantics:

- `Серия · часть 1`;
- or only show progress when two or more public series entries exist;
- or a landing can explicitly say `Запланировано 3 части · опубликована 1`.

Exact UX decision belongs to product-design lane.

Research principle:

> **publication progress and reading progress must not be conflated.**

---

# 9. Landing-page state machine

## L0 — absent

Before Part I.

## L1 — one published part

If landing exists:

- clear series thesis;
- Part I clickable;
- Parts II–III planned/non-clickable;
- no companion unless its plan is useful and clearly labeled.

## L2 — two published parts

- Parts I–II clickable;
- Part III planned/non-clickable;
- status language accurate.

## L3 — core complete

- Parts I–III clickable;
- core completion visible;
- companion area separated.

## L4 — core + companion

- core remains visually numbered 1–3;
- companion is visibly unnumbered;
- no design implying Part IV.

---

# 10. Cross-link state machine

## Part I → Part II

Before Part II release:

- prose teaser only, no dead link.

After Part II:

- series next navigation is canonical;
- optional in-prose link only if reader benefit exceeds duplication.

## Part II → Part III

Same rule.

## Part II → adult companion

Activate only when companion public.

## Part III → adult companion

Activate only when public and relevant.

## Companion → core

At companion publication, strongest backlinks:

- Part II for parent/adult jurisdiction transition;
- Part III for church-discipline/family-duty intersection.

Avoid four reciprocal links in every page footer if existing series/related UI already provides them.

---

# 11. Search / sitemap / feed consistency

Exact tooling must be re-derived at product head, but publication invariant is stable:

A route should not be simultaneously:

- presented as published in series landing;
- absent from intended discovery surfaces;
- or present in feed/sitemap while explicitly private/draft.

For each release candidate check the generated artifact for:

- sitemap inclusion/exclusion;
- RSS/feed inclusion/exclusion;
- search/Pagefind inclusion/exclusion;
- article catalog card;
- series landing card;
- canonical URL;
- robots state.

Do not assume one metadata toggle controls all of these.

---

# 12. Publication-date invariant

Do not preassign public `publishedAt` dates to Parts II–III merely to stabilize ordering.

Ordering belongs to explicit series order, not fabricated chronology.

Use actual release date at release.

If a manuscript requires a date field during draft build, current product convention must determine how that draft date is represented and later corrected without creating false publication history.

---

# 13. Source-state invariant

A part can be editorially written while its final source gate remains incomplete.

That does not make it public.

Release requires:

- used factual sources selected;
- exact historical quotations rechecked;
- biblical quotation/numbering policy applied;
- bibliography pruned to used sources under `112`;
- source-required validator satisfied.

Do not let complete prose outrun source state.

---

# 14. Theological continuity state

Before releasing Part II after Part I, check not only Part II internally but the **interface**:

- Part I did not imply parents can diagnose regeneration infallibly;
- Part II does not contradict Part I’s false-profession/grievous-fall guard.

Before Part III:

- Part II’s family authority does not become church authority;
- Part III’s discipline does not retroactively imply every unbaptized child was a member discipline case.

Before companion:

- Part II child-level authority is explicitly not carried into adulthood;
- Part III church discipline does not erase family relation.

This interface review is part of release state, not optional copyedit.

---

# 15. Minimal shared-file mutation principle

Shared product surfaces are collision-prone.

Possible examples:

- series registry/order;
- route ownership manifest;
- article catalog metadata;
- sitemap/feed/search derived registries;
- landing components.

Therefore each release lane should ask:

> What is the smallest shared-file change required to make **this already-ready article** publicly coherent?

Not:

> What files can we prepare now for all future parts?

Do not prewire Part III during Part I release.

---

# 16. Atomicity matrix

## Article-local changes

Can usually be developed before public release:

- MDX manuscript;
- article-local source block;
- article-local image metadata;
- local route component if required;
- draft/noindex metadata.

## Public-state shared changes

Prefer atomic with release:

- public series order;
- published landing card;
- public related links;
- public route ownership changes;
- generated discovery surfaces where not automatic.

## Never prewire blindly

- next link to future draft;
- related link to future companion;
- sitemap entry for private manuscript;
- published card with future date;
- public source count before source pruning is final.

---

# 17. Per-release verification checklist

For every Part I/II/III/companion release candidate:

1. live `main` SHA captured;
2. active PRs and overlapping files rechecked;
3. exact candidate head captured;
4. article route intentional;
5. `draft/noindex` state intentional;
6. every public series link resolves;
7. every public related link resolves;
8. no hidden draft is linked from published content;
9. landing status matches reality;
10. prev/next matches published order only;
11. search/sitemap/feed state matches release state;
12. publishedAt/updatedAt truthful;
13. current source policy passes;
14. current validation/audit passes;
15. exact-head CI terminal-green;
16. rendered artifact inspected for state drift;
17. no undeclared shared-file overlap.

---

# 18. Recommended release strategy

Default:

### Release Part I by itself.

Do not wait for all three manuscripts merely to avoid incremental metadata work.

But do not expose unfinished Part II/III routes.

### Then Part II.

At that point enable real two-part sequence.

### Then Part III.

Complete numbered core.

### Then adult companion when ready.

Keep it separate from core prev/next.

This gives the project both editorial velocity and public-state integrity.

---

# 19. Final state-machine verdict

The internal roadmap may always be ahead of the site.

The site must never pretend the roadmap is already publication.

> **Draft state is private intent. Series navigation is a public promise. Only released articles belong in that promise.**