# START HERE — Steven J. Lawson research

**Updated:** 2026-09-30  
**Canonical operational handoff:** [`CURRENT.md`](CURRENT.md)

> **Do not resume from the old README file list, the 2026-09-28 queue, or article v4.** The large historical `README.md` preserves the evolution of the corpus but its top-level canonical-draft labels are stale.

## Current reading order

1. [`CURRENT.md`](CURRENT.md) — current status, unresolved P1 targets, live biography-branch protocol.
2. [`62_LOGICAL_SYNTHESIS_AND_RESEARCH_VERDICT_2026-09-29.md`](62_LOGICAL_SYNTHESIS_AND_RESEARCH_VERDICT_2026-09-29.md) — stable research conclusion.
3. [`64_ARTICLE_RU_REFINED_V5_2026-09-29.md`](64_ARTICLE_RU_REFINED_V5_2026-09-29.md) — current full Russian publication draft.
4. [`65_BOOK_SIX_ROOT_PUBLIC_TRANSCRIPTION_AND_ACKNOWLEDGMENTS_P1_PASS_2026-09-29.md`](65_BOOK_SIX_ROOT_PUBLIC_TRANSCRIPTION_AND_ACKNOWLEDGMENTS_P1_PASS_2026-09-29.md) — six-root / book-page P1 status.
5. [`66_TOM_GIBSON_PRESIDENT_CANDIDATE_STRENGTHENED_AND_RESTORATION_SERMON_AUDIT_2026-09-29.md`](66_TOM_GIBSON_PRESIDENT_CANDIDATE_STRENGTHENED_AND_RESTORATION_SERMON_AUDIT_2026-09-29.md) — OnePassion successor candidate, still not directly proven.
6. [`67_ANNE_LAWSON_DIRECT_PUBLIC_STATEMENT_AND_MARITAL_STATUS_P1_NEGATIVE_AUDIT_2026-09-29.md`](67_ANNE_LAWSON_DIRECT_PUBLIC_STATEMENT_AND_MARITAL_STATUS_P1_NEGATIVE_AUDIT_2026-09-29.md) — Anne/marital-status hard guardrail.
7. [`68_BIOGRAPHY_LANE_INTEGRATION_BRIDGE_2026-09-30.md`](68_BIOGRAPHY_LANE_INTEGRATION_BRIDGE_2026-09-30.md) — how the live biography branch changes the historical method without being merged yet.
8. [`69_ARTICLE_RU_V6_BIOGRAPHY_INTEGRATION_PLAN_2026-09-30.md`](69_ARTICLE_RU_V6_BIOGRAPHY_INTEGRATION_PLAN_2026-09-30.md) — one-pass V6 integration plan.
9. [`70_BIOGRAPHY_LANE_IMPACT_TRIAGE_AND_FREEZE_CRITERIA_2026-09-30.md`](70_BIOGRAPHY_LANE_IMPACT_TRIAGE_AND_FREEZE_CRITERIA_2026-09-30.md) — which remaining biography questions can actually change V6.
10. [`71_CANONICAL_STACK_CONSISTENCY_AUDIT_2026-09-30.md`](71_CANONICAL_STACK_CONSISTENCY_AUDIT_2026-09-30.md) — confirms the canonical claims currently align.
11. [`72_TBC_LEGACY_LAWSON_PAGE_STATE_FALSE_CURRENT_TRAP_2026-09-30.md`](72_TBC_LEGACY_LAWSON_PAGE_STATE_FALSE_CURRENT_TRAP_2026-09-30.md) — current Trinity legacy pages are not proof of Lawson's return.
12. [`73_ARTICLE_RU_V6_BIOGRAPHY_INSERT_DRAFTS_2026-09-30.md`](73_ARTICLE_RU_V6_BIOGRAPHY_INSERT_DRAFTS_2026-09-30.md) — polished V6 insertion staging with exact V5 anchors, recovered 2013 marriage baseline, recovered 2020 prayer/work/rest self-diagnosis and final Tier-A-delta guardrails.

## Live biography lane

Branch:
- `arena/01a0ea6e-research`

Last observed HEAD:
- `4768115996a06397af8fd59547bceee102ed67a8`
- commit date: `2026-09-29T18:33:37Z`
- latest observed pass: **21**

Stable branch-delta facts:
- merge base: `8c21307eff34f184759011c29f692b202080ac13`;
- biography branch has **29 commits** after that merge base;
- its own delta touches only six paths:
  1. `STEVEN_LAWSON_2024_2026/README.md`
  2. `STEVE_LAWSON/19_CURRENT_STATUS_AND_ACQUISITION_QUEUE_2026-09-28.md`
  3. `STEVE_LAWSON/28_EARLY_LIFE_AND_FAMILY_DOSSIER_2026-09-28.md`
  4. `STEVE_LAWSON/DURABLE_CUSTODY_MANIFEST.json`
  5. `STEVE_LAWSON/LOG.md`
  6. `STEVE_LAWSON/README.md`

Do **not** use the branch's `behind main` count as a durable handoff datum. `main` is concurrently active in unrelated research lanes, so that number can grow without any change to Lawson evidence. Recompute it only at freeze if needed for mechanics.

Rule:
- **do not blind-merge while the agent is still working**;
- after freeze, inspect only the delta after `4768115996a...` first and classify it under `70_`;
- replay the biography-specific dossier and log, and merge only the biography additions to the custody manifest;
- do **not** overwrite the newer main copies of `19_`, either README, `CURRENT.md`, article files or the canonical handoff;
- then produce one V6 article revision.

### Reconcile trap already identified

The live biography dossier was forked before several Sept. 29 main-corpus upgrades. Therefore some of its statements about what the main corpus lacks are now stale even though the biography evidence itself remains useful.

The clearest known example:

- the branch dossier still says the 2020 Ask Ligonier / Anne node lacks a checked primary-audit object and treats the old missing `08_ASK_LIGONIER...` path as a live evidentiary weakness;
- current main now contains [`37_ASK_LIGONIER_2020_ANNE_MARRIAGE_SELF_WITNESS_2026-09-29.md`](37_ASK_LIGONIER_2020_ANNE_MARRIAGE_SELF_WITNESS_2026-09-29.md), which establishes the official-event provenance and recovers the searchable Ligonier-channel transcript through a derivative carrier, with explicit publication guardrails.

At final reconcile, preserve the historical broken-link observation if useful, but **remove the stale inference that the Anne/Ligonier evidentiary node remains unacquired**. Main's newer `37_` governs that question.

This is the model for the whole merge: biography facts move forward; stale fork-era assessments of the newer main corpus do not.

## Historical Lawson branch archaeology — completed 2026-09-30

Several branch names can look like unmerged Lawson work but are **not** additional live research lanes:

- `tmp/lawson-biography-integration-20260930`
- `tmp/lawson-biography-integration-20260930-2`

Both point to exactly the same commit, `7b0979c7f2acdad0c4c279929e97277b5d16706a`. That commit is a direct ancestor of current `main`; the two temporary refs contain **zero unique commits**. Do not merge or replay them.

Older branches:

- `lawson-bundle-bootstrap-20260928` (`b7cd8a8...`) is an ancestor of the finalized Lawson line;
- `lawson-finalize-20260928` (`dff6e36...`) is a direct ancestor of current `main`;
- `lawson-final-import-20260928` (`f30ff8b...`) is a divergent historical import-runner branch, not a second canonical research line. Its five post-bootstrap commits are the import-runner sequence and bot import used during the Sept. 28 reconstruction.

Semantic salvage was checked rather than relying on Git ancestry alone:

- the 2022 `Should I Marry Her?` object from the old lead/source files is **already preserved in current main** at [`08_QA_TRANSCRIPT_AND_LIGONIER_STATE_2026-09-27.md`](08_QA_TRANSCRIPT_AND_LIGONIER_STATE_2026-09-27.md), including carrier metadata, audio hash, machine-transcript locators and publication limitations;
- the old 2020 Ask Ligonier / Anne material is superseded and strengthened by `37_`;
- the same July 2020 Ask Ligonier session also contained a stronger workaholism lead that had fallen out of the newer synthesis: Lawson publicly said he should have prayed more, had been too driven in work, and should have taken more vacation and rest. This has now been restored to the canonical workaholism evidence file [`39_...`](39_PERSONAL_LIFE_OF_PREACHER_VS_MINISTRY_WORKAHOLISM_SELF_WITNESS_2026-09-29.md) and staged as `MICRO-EDIT A2` in [`73_...`](73_ARTICLE_RU_V6_BIOGRAPHY_INSERT_DRAFTS_2026-09-30.md);
- one useful pre-fall marriage baseline had likewise fallen out of the newer canonical synthesis: Lawson's March 2013 *Tabletalk* article `His Heart Trusts in Her` / later `The Blessing of an Excellent Wife`. Its publication is independently traceable through *Tabletalk* and Ligonier indexes and surviving text carriers. It has now been restored, conservatively paraphrased, into `73_` for V6;
- weaker historical leads (for example title-only sermon leads or later commentator applications) remain available in Git history / `lawson-final-import-20260928`, but they do not outrank the stronger evidence already in the current canonical corpus and are not V6 blockers.

Therefore **none of these legacy branches should be merged into `main`**. Keep them as provenance/history unless branch cleanup is undertaken separately.

## Core thesis

> Lawson's pre-fall ministry already contained most of the theological categories that his 2026 book uses to diagnose his collapse. The central documented contradiction is therefore not ignorance versus later enlightenment but known doctrine/warning versus lived obedience. Post-fall, a real counseling/pastoral/accountability process existed; however, the public record still does not transparently disclose the finished-book external review/approval chain. Because the scandal itself was a prolonged disparity between public theological competence and private life, renewed public spiritual credibility cannot be established by theological fluency or autobiographical eloquence alone. It must rest on durable observable fruit and meaningful external pastoral judgment.

## Hard guardrails

Do not state as fact that:

- Lawson is unregenerate;
- Lawson is divorced;
- Anne supports/opposes the book;
- King Counts counseled Lawson;
- Terry Warren was on the accountability team or reviewed the manuscript;
- Tom Gibson is definitively the post-Lawson OnePassion president;
- Lawson bypassed his counselors/elders;
- TBC/SVC/OnePassion/family approved or opposed the book without a direct source;
- the book was AI-written;
- the book was a money grab;
- old live Trinity ministry pages prove Lawson has returned to current teaching;
- numerical differences in old autobiographical recollections prove intentional dishonesty.

## Endgame

The project is no longer searching for a missing grand theory.

Remaining work is:

1. let/finalize the biography lane;
2. inspect only the post-`4768115...` Tier-A delta;
3. reconcile the three biography-bearing payloads (`28_EARLY...`, `LOG.md`, manifest additions) without replaying stale shared control files;
4. correct any fork-era statements invalidated by newer main evidence (known example: Ask Ligonier 2020 → `37_`);
5. execute V6 using `69_` + polished `73_`;
6. final claim/source audit;
7. update `CURRENT.md` and this handoff once;
8. publish.

Do not create parallel V6-beta drafts while the biography lane is live.