# V84I — POST-MERGE TOTAL AUDIT AND CLOSURE GATES

**Date:** 2026-07-30  
**Status:** CURRENT CROSS-REPO AUTHORITY / MERGES CONFIRMED / SITE CLEANUP OPEN / LIVE RELEASE WITNESS PENDING  
**Supersedes for current state:** V84H status, embedded PR-state counters and every earlier `KEEP DRAFT / NO MERGE` disposition.  
**Preserves:** all substantive source, theological, medical-safety and evidence-class findings from V81–V84H.

---

## 1. Why V84I exists

V84H was accurate as a final pre-merge authority. It became stale after the owner explicitly authorized merge and all three pull requests were merged. Its substantive findings remain valid, but its workflow statements (`draft`, `no merge`, `production not claimed`) are now historical, not current.

This file is the first authority written from the post-merge state. Older files remain an audit trail and must not be silently rewritten as though their historical timestamps occurred after merge.

---

## 2. Confirmed merges

### Research

- Repository: `FedorMilovanov/Research`
- PR: `#38`
- Audited head: `3418a0b227a93e7b9a8b714ecc94692874674b8f`
- Merge commit on `main`: `a6aea00e719f93c7697c695386d81c858ff19201`
- Result: research corpus is in `main`.

### AuditRepo

- Repository: `FedorMilovanov/AuditRepo`
- PR: `#101`
- Audited head: `dfdb6b2adc1e0bf2f7f3090d2890ef39e5bba20f`
- Merge commit on `main`: `e98c594093b5979141d1a582c5b26507659607b1`
- Result: governed intake is in `main`.

### Site

- Repository: `FedorMilovanov/gb-is-my-strength`
- PR: `#498`
- Audited article head: `54b90c60cba945aec71de02d8aa6279f65fbab1e`
- Merge commit on `main`: `e344329096c61a9f01ab5e91b379861a5e15badf`
- Result: the two reader-facing article files are in `main`.

The merge order was Research → AuditRepo → Site.

---

## 3. Material text-base verdict

The material text base is complete for the present publication stage.

Confirmed reader-facing strengths:

1. depression is located within creation, Fall, embodied human nature and life before God before clinical classification;
2. grief, occupational burn-out, depressive disorder, bodily illness, real guilt, false guilt, temptation and crisis are not collapsed;
3. no biblical person is retrospectively assigned a modern diagnosis;
4. diagnosis is neither a moral verdict nor a certificate of innocence;
5. urgent safety intervention and continuing church care are held together;
6. John 9 is corrected: Christ answers His disciples, not imagined friends of the blind man;
7. David supplies the real-guilt case without universalizing guilt to every sufferer;
8. Rogers direct translations carry explicit historical-language and locator boundaries;
9. Goodwin, Gurnall and MLJ are represented according to their actual evidence class;
10. the final cross section preserves one Trinitarian saving work, real judgment and substitution, one Person of the Son, two natures and the limit of revealed metaphysical claims.

No new material-theology rewrite is required before closure. Remaining work is repository/governance/navigation/deployment and source-provenance cleanup.

---

## 4. Post-merge total-audit findings

### PM-001 — stale current-authority disposition

**Severity:** high governance drift  
**Confirmed:** V84H still labels itself current while ending with `KEEP ALL THREE PRS DRAFT / NO MERGE / NO PRODUCTION CLAIM`.

**Resolution:** V84I supersedes those current-state statements. V84H remains the historical pre-merge snapshot.

### PM-002 — AuditRepo has the same stale current-state problem

**Severity:** high governance drift  
**Confirmed:** the final AuditRepo authority still describes all three PRs as draft and unmerged.

**Resolution path:** AuditRepo PR `#102` adds the post-merge governed authority without erasing the historical audit.

### PM-003 — Site article TOC drift

**Severity:** medium reader-navigation defect  
**Confirmed source mismatch:** the common heart-series config omits two current H2 sections from `tma-na-serdce`:

- `#pered-bogom` — «Сначала — человек перед Богом»;
- `#kogda-vina-realna` — «Когда тьма связана с реальной виной: Давид».

It also retains two stale labels:

- `#ne-odin-diagnoz` is no longer «Не один диагноз, а много»;
- `#kogda-tma-bolezn` is no longer «Когда тьма — это болезнь тела».

**Required:** repair the source-of-truth TOC, not a DOM/runtime patch. Governed implementation task: Site issue `#509`.

### PM-004 — tma reading-time and series-progress drift

**Severity:** medium metadata/reader-state defect  
**Confirmed:** article metadata says `34` minutes while the common series config stores `26`.

The book-shaped series calculation also gives every extra article of a chapter the same `doneMin` and uses the core-only `HEART_TOTAL_MIN`, excluding the extra articles from the total. This is structurally wrong now that extras are declared full chapter articles.

**Required:** calculate ordered cumulative progress from all actual book articles and one canonical reading-time source. Correct full-book total after `tma=34`: `727` minutes. Governed implementation task: Site issue `#509`.

### PM-005 — `/hard-texts/` landing is behind the current architecture

**Severity:** medium discoverability/schema drift  
**Confirmed in source and live output:** cards, stats, map and structured-data prose retain the earlier three-part model and stale reading times even though the active series config is a four-chapter book with chapter articles.

Examples include:

- Romans 7 shown as `12` minutes instead of `45`;
- stale `3 parts / 2 published / 53 minutes` counters;
- a three-node series map;
- static JSON-LD `hasPart` that does not represent the current published book structure.

**Resolution path:** Site PR `#510` derives the landing inventory/metadata from the active book config, migrates `/hard-texts/` to `surface=series / seriesShape=book`, updates the four-chapter map and ratchets the route/visual registry contracts.

### PM-006 — live production was not yet a post-merge witness at audit time

**Severity:** release closure gate  
**Observed:** live `/hard-texts/` and live Romans 7 still rendered the old three-part/12-minute version while `main` contained the new book-shaped/45-minute source.

**Important timing fact:** after the Site merge, an accidental one-line `tmp` commit was pushed and then removed. The deploy workflow uses `concurrency: group: pages` with `cancel-in-progress: true`; therefore those pushes restart/cancel the preceding deployment. The old live output proves absence of a completed witness, not by itself a failed pipeline.

**Required closure evidence:** after final cleanup merges, the exact latest `main` release must finish deployment and the live release contract must prove the promoted SHA/candidate.

### PM-007 — deployment workflow itself is structurally sound

**Confirmed source:** `.github/workflows/deploy.yml` triggers on every push to `main`, builds one immutable candidate, promotes the same bytes to GitHub Pages and runs generic live-release plus TTS live contracts.

No emergency manual upload or bypass is justified. The professional action is to use the controlled pipeline and inspect its exact run evidence.

### PM-008 — accidental probe residue

**Severity:** resolved  
**Confirmed:** commit `eb8f337827b2a621a2cdc3e90d6825a503276869` added a one-line `tmp` file; commit `97f5da7122b96d6cdedd55e4717234ac700233f4` removed it.

No file residue remains. The only effect relevant here is deploy restart/cancellation under the pages concurrency policy.

### PM-009 — Rogers translations need scan-first rights/provenance closure

**Severity:** medium source-governance / rights-cleanup gate  
**Confirmed:** the University of Michigan EEBO-TCP item correctly identifies Rogers 1691, exposes the Preface structure and supports locator navigation. The same item also carries an explicit notice restricting subsequent redistribution of its keyboarded/encoded edition.

The underlying 1691 book is historical, and Google Books indexes a full-view British Library scan of the 1691 edition. Therefore the professional provenance model is:

1. visually verify Preface advices `1`, `5` and `6` against the open page images of the 1691 scan;
2. record scan/image and printed-page/signature locators where visible;
3. make the scan the primary basis for the three Russian direct translations;
4. retain Michigan EEBO-TCP only as a structural TOC/search aid with its rights boundary respected;
5. do not import large English transcription passages.

**Governed implementation task:** Site issue `#513`.

This finding does not refute the current Russian translations. It prevents claiming full source-clean closure before scan-image verification and provenance correction.

---

## 5. Evidence gates that remain intentionally open

These are not hidden defects and do not block the current article wording:

- `BOOK-FULLTEXT-HOLD` remains for the full MLJ book edition;
- parsed PDF text is not page-image verification;
- new direct PDF quotations remain `PAGE-IMAGE-HOLD` until visual pagination is available;
- Adams historical psychiatric generalizations remain `DO-NOT-IMPORT`;
- organic/mixed/referral observations remain `LIMITED IMPORT` with current verification;
- no prescribing, deprescribing, dose or taper instruction is authorized;
- no self-diagnosis or retrospective diagnosis of biblical persons is authorized;
- no confident internal-metaphysical mechanism of Trinitarian dereliction is claimed beyond revelation.

A HOLD is an evidence boundary, not an unfinished promise to import the held material.

---

## 6. Required closure sequence

1. Merge Research PR `#39` and AuditRepo PR `#102` after owner approval.
2. Complete and merge Site PR `#510` after all exact-head checks and artifact readback pass.
3. Implement Site issue `#509`:
   - exact tma TOC parity;
   - canonical `34` minutes;
   - cumulative progress over all book pages;
   - full total `727`;
   - automated parity/progress contract.
4. Implement Site issue `#513`:
   - scan-first verification of Rogers Preface advices `1`, `5`, `6`;
   - page-image locators;
   - reader-facing source provenance correction.
5. Run exact-head checks for the final Site cleanup head.
6. Merge the final Site cleanup only after those checks pass.
7. Obtain deployment evidence for the then-current `main` SHA.
8. Read the live-release artifact and verify at minimum:
   - promoted SHA equals intended `main`;
   - `/articles/tma-na-serdce/` resolves;
   - title, canonical, modified date and article body are current;
   - tma reader TOC contains the repaired sections;
   - article/series reading times agree at `34`;
   - full-book progress total is `727` and cumulative positions increase;
   - `/hard-texts/` exposes the current four-chapter book architecture;
   - Pagefind and sitemap include the route;
   - no old three-part chrome remains on Romans 7;
   - Rogers source block points direct translations to scan-first locators.
9. Delete obsolete merged feature/maintenance branches through the owner UI or an authorized branch-ref cleanup tool after all dependent PRs are closed.

---

## 7. Final disposition

`MATERIAL TEXT BASE COMPLETE`

`THEOLOGICAL AND SAFETY BOUNDARIES COMPLETE FOR CURRENT PUBLICATION`

`ALL THREE ORIGINAL PRS MERGED`

`STALE PRE-MERGE AUTHORITY SUPERSEDED BY V84I`

`LANDING CLEANUP IN PR #510`

`TOC / READING-TIME / PROGRESS CLEANUP REQUIRED IN ISSUE #509`

`ROGERS SCAN-FIRST PROVENANCE REQUIRED IN ISSUE #513`

`LIVE RELEASE WITNESS REQUIRED`

`NOT YET FULLY CLOSED`