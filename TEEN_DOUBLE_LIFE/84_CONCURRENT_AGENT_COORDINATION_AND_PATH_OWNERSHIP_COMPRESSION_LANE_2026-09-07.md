# Concurrent-Agent Coordination — Compression Lane Ownership

**Status:** WORKFLOW CONTROL / RESEARCH ONLY  
**Date:** 2026-09-07  
**Reason:** multiple agents are actively committing to the same Draft PR branch. This file prevents accidental overwrites/duplicate research.

---

# 1. Observed concurrent state

PR #187 has already experienced:

- CAS movement while shared files were being edited;
- overlapping numeric prefixes `59–65` from independent useful streams;
- later concurrent additions in adult-child/prodigal research (`66–71` observed);
- simultaneous compression work begun at `80+`.

Concurrency is therefore **real**, not hypothetical.

---

# 2. Current lane division

## Adult-child / prodigal / household / admonition lane

Observed active concurrent files include:

- `66_ISRAEL_WARNING_HANDING_OVER_EXILE_RESTORATION_AND_PARENTAL_ANALOGY_GUARDS...`
- `67_ADULT_CHILD_AT_HOME_CORESIDENCE_RULES_SEXUAL_SIN_WORK_SUPPORT_AND_EVICTION_GUARDS...`
- `68_PROVERBS_1_9_PARENTAL_ADMONITION_SON_WISDOM_FOLLY_AND_ADULT_APPLICATION_GUARDS...`
- `69_LIMITS_OF_REPEATED_ADMONITION_SCORNER_QUARRELS_GENTLENESS_AND_MODE_CHANGE...`
- `70_ADULTHOOD_HONOR_OBEDIENCE_HOUSEHOLD_AND_FAMILY_DUTY_1TIM5_EPH6_GEN2_MARK7...`
- `71_POST_DEPARTURE_CONTACT_CADENCE_SAFETY_FACT_FINDING_NONENABLING_AND_OPEN_DOOR_MATRIX...`

**Compression agent must not edit these paths.**

Assume this lane may continue into `72–79` unless current PR inspection proves otherwise.

---

## Compression / architecture lane

Reserved here:

- `80_PUBLICATION_COMPRESSION_CORE_THESIS_MAP_AND_NARRATIVE_SPINE...`
- `81_ARCHITECTURE_OPTIONS_ONE_THREE_FIVE_ARTICLES_COMPARATIVE_AUDIT...`
- `82_KEEP_CUT_APPENDIX_COMPANION_PUBLICATION_PRIORITY_MATRIX...`
- `83_DRAFTING_ORDER_SELECTED_QUOTE_FACT_VERIFICATION_AND_NO_OVERCLAIM_GATES...`
- `84_CONCURRENT_AGENT_COORDINATION_AND_PATH_OWNERSHIP_COMPRESSION_LANE...`

Future compression work should use **`85+`** and should avoid editing adult-child source modules unless explicitly reconciling after the other agent stops.

---

# 3. Shared-file rule

The following are shared/high-collision files:

- `README.md`;
- continuity master/addenda;
- PR body;
- claim/exegesis ledgers;
- any reconciliation index.

### Default

**Do not edit a shared file merely to keep it cosmetically current while another agent is active.**

Instead:

1. create a new lane-local addendum;
2. record the exact filenames/head observed;
3. reconcile shared index later in one CAS-safe pass.

This reduces useless conflicts.

---

# 4. Before every write burst

Check:

1. PR exact head;
2. changed-file list;
3. whether the intended path already exists;
4. whether a new concurrent thematic lane appeared;
5. whether another agent edited the same shared file.

If head moved but intended path is new/unique, creating the new file is normally safe.

If editing an existing file:

- fetch current blob;
- use exact SHA;
- never reuse old SHA after head movement without re-fetching the file;
- on CAS failure, re-read and merge conceptually rather than overwriting.

---

# 5. Numbering rule

Numeric prefixes are for sorting, not identity.

Because duplicates already exist:

- exact filename is authoritative;
- do not rename parallel files merely to make numbers pretty while agents are active;
- renumbering can happen only in a deliberate cleanup after concurrency stops, if useful at all.

For now:

- adult-child lane: `66–79` observed/reserved by convention;
- compression lane: `80+`.

If another agent unexpectedly uses `80+`, choose a higher unused block (`90+`) rather than fighting over numbering.

---

# 6. Topic non-overlap rule

Compression lane may:

- summarize;
- deduplicate;
- compare architectures;
- rank claims;
- set drafting gates;
- create publication source packets;
- design narrative arcs.

Compression lane should **not** independently re-research:

- Luke 15;
- adult-child eviction/co-residence;
- post-departure contact cadence;
- repeated-admonition limits;
- Israel-exile analogy;

while another agent is already actively extending those subjects.

It may later consume the finished results.

---

# 7. Product-repo protection

No agent working in this Research lane should begin writing product prose into `gb-is-my-strength` until:

- research/architecture phase is intentionally handed off;
- product repository current rules are re-read;
- active product PRs are checked;
- a distinct product branch/lane is assigned.

This prevents a second kind of concurrency collision: Research agent vs publication agent.

---

# 8. Merge policy

Do not merge Draft PR #187 merely because one lane finishes.

Before any merge decision:

- all active concurrent agents should stop or be reconciled;
- shared index should be current;
- authority integrity workflow should be green at exact head;
- no unresolved contradictory conclusions should remain;
- user/product workflow should decide whether Research corpus belongs merged as-is or retained as Draft/source branch.

---

# 9. Current coordination verdict

Concurrent work is adding value, not merely noise.

The correct response is **lane isolation + later reconciliation**, not forcing all agents into one shared file.

This file is the compression lane’s ownership marker.