# Q005 / Q006 — Georgia filing delta and dated re-check, 2026-11-15

**Status:** CANONICAL-DELTA OVERLAY / PUBLICATION_HOLD  
**Scope:** strictly Q005 (Georgia legal status) and Q006 (G3+ successor / closing / scope). Nothing else is reopened.  
**Prior authority:** `FINAL_P0_HOLD_MATRIX_2026-09-09.md` (Q005 and Q006 rows), `P0_REFRESH_2026-09-09.md`, `Q006_ASSET_TRANSFER_REFRESH_2026-09-09.md`  
**Observation date for every retrieval below:** 2026-11-15 (UTC)  
**Reopen trigger actually met:** `Later Georgia filing/status change` (matrix Q005) and trigger 9 of `Q006_ASSET_TRANSFER_REFRESH_2026-09-09.md` §6.

This file is a dated overlay. It supersedes the Sep. 9 matrix **only** for the Q005 and Q006 rows and does not rewrite the Sep. 8/9 files, which remain accurate as dated evidence.

## Decisions

| Question | Decision | State after this pass |
|---|---|---|
| Q005 — Georgia legal status | **VERIFIED NEW EVIDENCE** | `NAME_CHANGE_VERIFIED_PRIMARY (effective 2026-10-28) / NO_DISSOLUTION_FILING_IN_HISTORY_AS_OF_2026-11-15 / CURRENT_STATUS_FIELD_AND_FILING_BODIES_ACCESS_HOLD / TIME_SENSITIVE` |
| Q006 — G3+ successor / closing / scope | **EXTERNAL_DOCUMENT_HOLD RETAINED** | `ACQUISITION-OR-TRANSITION-IN-PROGRESS REPRESENTATION VERIFIED / TRANSFEREE, CLOSING AND TERMS EXTERNAL_DOCUMENT_HOLD`; new context recorded, hold not lifted |

## 1. Q005 — what the official registry now shows

### 1.1 Objects read

Official Georgia Secretary of State Corporations Division (eCorp), internal `businessId=2751672` — the identifier already recorded for this entity in `G3-S001` from the Sep. 8 official acquisition:

- filing history: `https://ecorp.sos.ga.gov/BusinessSearch/BusinessFilings?businessId=2751672`
- name change history: `https://ecorp.sos.ga.gov/BusinessSearch/NameChangeHistory?businessId=2751672`

### 1.2 Filing history as rendered (8 of 8 records, one page)

| Filing no. | Filing date/time | Effective | Filing type | Ledger position |
|---|---|---|---|---|
| 17370469 | 6/6/2019 8:26:29 AM | 6/6/2019 | Business Formation | already in `G3-S001` |
| 17449198 | 7/16/2019 3:10:59 PM | 7/16/2019 | Annual Registration (2019) | already in `G3-S001` |
| 18903966 | 3/30/2020 5:05:48 PM | 3/30/2020 | Annual Registration (2020, 2021) | already in `G3-S001` |
| 22250386 | 1/10/2022 8:41:02 PM | 1/10/2022 | Annual Registration (2022, 2023, 2024) | pre-cutoff, index row newly readable |
| 29366217 | 5/14/2025 9:28:16 PM | 5/14/2025 | Annual Registration (2025, 2026) | pre-cutoff, index row newly readable |
| **32257311** | **10/28/2026 2:47:06 PM** | **10/28/2026** | **Business Amendment Name Change** | **new, after the Sep. 8 cutoff** |
| **32260917** | **10/30/2026 1:23:37 PM** | **10/30/2026** | **Amended Annual Registration** | **new, after the Sep. 8 cutoff** |
| **32269080** | **11/5/2026 9:31:29 AM** | **11/5/2026** | **Amended Annual Registration** | **new, after the Sep. 8 cutoff** |

### 1.3 Name change history as rendered (1 of 1 record)

| Filing no. | Old name | New name | Filing date | Effective date |
|---|---|---|---|---|
| 32257311 | `G3 Ministries for the Church, Inc.` | `Lumena Ministries, Inc.` | 11/4/2026 2:29:02 PM | 10/28/2026 |

### 1.4 Entity binding

The eCorp header cells `Business Name` and `Control Number` rendered empty in the retrieval tool, so the binding to G3 is established by three other means rather than by that header:

1. `businessId=2751672` is the internal identifier recorded for control no. `19085916` in `G3-S001`;
2. the first three filing numbers and dates match the three filings already primary-anchored in `G3-S001` exactly;
3. the name-change table itself names `G3 Ministries for the Church, Inc.` as the old name.

### 1.5 Claim states

- `The Georgia corporate entity formerly registered as G3 Ministries for the Church, Inc. changed its registered name to Lumena Ministries, Inc., effective 2026-10-28 (filing 32257311)` — **VERIFIED_PRIMARY** at the registry-index level.
- `Two Amended Annual Registrations were filed after the name change (2026-10-30 and 2026-11-05)` — **VERIFIED_PRIMARY** at the registry-index level. Their contents are **not acquired**.
- `No dissolution-type filing (notice of intent to dissolve, articles of dissolution, administrative dissolution) appears in the eight-row filing history on 2026-11-15` — **VERIFIED_PRIMARY as a dated registry-index observation**.
- `G3 was formally dissolved under Georgia law` (`G3-C029`) — stays **REFUTED** for the Sep. 8 acquisition and is not supported by anything in the Nov. 15 filing history. A rename plus amended registrations is the conduct of a corporation that continues to exist on the register; it is not a liquidation event.

### 1.6 Preserved internal tension

Filing 32257311 carries two different registry date fields: `10/28/2026 2:47:06 PM` in the filing history and `11/4/2026 2:29:02 PM` in the name change history, both with effective date `10/28/2026`. The registry does not label the difference. Both values are preserved as displayed. Publication-safe wording is `effective October 28, 2026`; do not narrate a submission/approval sequence that the registry does not state.

### 1.7 What was not acquired

- **Current status field** (`Active/Compliance` or otherwise), current registered agent, principal office and officer list on the official `BusinessInformation` detail page. Every GET form of that route redirected to the blank search form. The last official reading of the status field remains the Sep. 8 `Active/Compliance` acquisition.
- **Document bodies** of filings 32257311, 32260917 and 32269080 (articles of amendment, amended registration contents, signatory, officers). The guessed document route returned HTTP 404.
- **Raw bytes / hashes.** The retrievals are rendered readbacks through the session fetch tool. The research sandbox has no network route to `ecorp.sos.ga.gov`; the repository workflow `g3-georgia-entity-acquisition` was last classified `ACCESS_HOLD` (run `42331190745`), and manual dispatch was refused to this session (HTTP 403). The filing-history table was read three times and returned identical rows each time.

Access failure on the detail page is not evidence about what that page says.

### 1.8 Secondary renderer — discovery only

OpenCorporates (`https://opencorporates.com/companies/us_ga/19085916`), a third-party renderer of the same Georgia registry and therefore **not** an independent source, displayed on 2026-11-15:

- status `Active/Compliance`;
- the old name, alongside a filing list that already includes the Oct. 28 name-change filing and the Oct. 30 amended registration but not the Nov. 5 one;
- registered agent `Laramie Minga` at a Winston, Georgia address (street locator deliberately not reproduced here), where the Sep. 8 official acquisition named Scott Aniol;
- `5 officers`, names behind a login.

Use: a lead that the status field was still `Active/Compliance` at a snapshot taken after Oct. 30 and that the registered agent changed. Neither point is promoted until the official detail page or the amended-registration bodies are read. The agent's identity must not be read as naming the organization's leadership or a transferee.

## 2. Q006 — what was checked and what it shows

### 2.1 Official current sources, one pass

| Surface | Reading on 2026-11-15 | Change from the Sep. 9 ledger |
|---|---|---|
| `https://g3min.org/` | `This Site Is Offline` notice: `G3 Ministries is concluding its operations. G3 Plus and G3 Press are continuing in a new form, under new leadership, and full details will be shared once the transition is complete.` Links to G3 Plus and G3 Press. | **New first-party text.** The root body was unread (HTTP 503) on Sep. 7/9. Promoted as `G3-S142`. |
| G3+ iOS App Store listing (`id1192776791`) | developer and seller `G3 Ministries For The Church, Inc.`; latest version `37.1.7`, dated `Sep 4`; copyright `© 2023 G3 Ministries` | none; no later release |
| `https://plus.g3min.org/legal/terms-of-service` | provider named `G3`; `Last Updated: April 03, 2025`; contact `admin@g3min.org` | none; no post-transfer legal-provider change |
| `https://shop.g3min.org/` | G3 Press storefront, G3 branding and G3 social links; `/policies/terms-of-service` returns the store 404 page | none |
| Georgia registry | see §1 | **new** |
| Web search for `Lumena Ministries` | no site, announcement, storefront or press mention located | first search for this name |

No final-transition subscriber notice, recipient-ministry announcement, board or corporate transaction notice, or agreement/assignment/closing instrument was found. Searches across the secondary reporters already in the ledger surfaced no later statement identifying a transferee; those pages were checked through search results, not re-read in full.

### 2.2 What the new first-party notice adds

- It is G3's own text and it couples **G3 Plus and G3 Press** in one statement. The Sep. 9 state had Press inclusion only at a recipient/secondary layer. That sub-point moves to: `G3 PRESS INCLUDED IN THE ANNOUNCED TRANSITION = FIRST-PARTY REPRESENTATION VERIFIED`.
- On its face it describes the transition as **not yet complete** (`once the transition is complete`). The notice is undated, and the date on which this sentence first appeared is unknown; it is not shown to post-date Sep. 8. Its presence on Nov. 15 is a dated surface state, not proof that the transition was still legally open on that day.
- It does not use the Aug. 27 wording `acquired by another ministry`. It says `a new form, under new leadership`.

### 2.3 Unreconciled first-party formulations

Three first-party or official objects now describe the same subject in different terms:

1. Aug. 27 subscriber email: G3 Plus `is being acquired by another ministry`;
2. site notice: G3 Plus and G3 Press `are continuing in a new form, under new leadership`;
3. Georgia registry: the same corporation, same control number, renamed `Lumena Ministries, Inc.`.

These are compatible with more than one legal structure — a transfer of assets to a distinct legal entity, a change of governance inside the same renamed corporation, or a combination. No acquired document selects among them. None is asserted.

### 2.4 Blocked inferences

All of the following remain blocked:

- `Lumena Ministries, Inc. is the ministry that acquired G3+` — the registry proves a rename of the G3 corporation, not an acquisition and not which assets the renamed corporation holds;
- `G3+ and G3 Press now belong to Lumena Ministries, Inc.`;
- `the acquisition was abandoned and replaced by a rebrand`;
- `the Aug. 27 email was inaccurate`, or any motive for the difference in wording;
- `the transition has closed` or `the transition has not closed`;
- `the registered agent shown by a secondary renderer is the new leadership`;
- any reading of the rename as concealment, evasion or wrongdoing. A name amendment is an ordinary corporate filing and carries no such meaning by itself.

Earlier guardrails are unchanged: `Living Heritage = successor` unverified, `Treefort = successor` blocked, app-store and storefront state is dated platform state only.

### 2.5 Answer to the three Q006 sub-questions

| Sub-question | Answer | State |
|---|---|---|
| Primary evidence of completed legal closing? | No | `COMPLETED_CLOSING = UNVERIFIED / EXTERNAL_DOCUMENT_HOLD` |
| Primary evidence naming a specific successor/transferee? | No | `TRANSFEREE = UNVERIFIED / EXTERNAL_DOCUMENT_HOLD`; `Lumena Ministries, Inc.` is recorded as the renamed G3 entity and as a lead only |
| Primary evidence of the scope of the transfer? | Partly, as representation only | Both Plus and Press are named in G3's own notice; assets, rights, inventory, consideration and liabilities remain `EXTERNAL_DOCUMENT_HOLD` |

## 3. Publication-safe formulations

Subject to the corpus-wide `PUBLICATION_HOLD`:

> Georgia Secretary of State records show that the nonprofit corporation registered in 2019 as G3 Ministries for the Church, Inc. amended its name to Lumena Ministries, Inc., effective October 28, 2026, and filed two amended annual registrations in the following days. As of November 15, 2026, its filing history showed no dissolution filing. The end of G3's operations therefore still cannot be described as a completed legal dissolution.

> G3's website states that G3 Plus and G3 Press "are continuing in a new form, under new leadership," with details to follow once the transition is complete. No public document reviewed identifies who now controls those services, whether a transfer has closed, or on what terms.

Not publication-safe: any sentence naming Lumena Ministries, Inc. as the acquirer, owner or operator of G3+ or G3 Press.

## 4. Narrowed reopen triggers

Do not repeat this pass against unchanged surfaces. Reopen only on:

1. the official `BusinessInformation` detail page for control no. `19085916` (status field, registered agent, officers) by any route that returns the record;
2. the document body of filing 32257311, 32260917 or 32269080;
3. a later filing on the same record, in particular any dissolution, merger or conversion filing;
4. a public surface that uses the name `Lumena Ministries` and connects it to G3 Plus or G3 Press;
5. a change of seller, developer, legal provider or merchant identity on the G3+ or G3 Press surfaces;
6. the instruments already listed in `Q006_ASSET_TRANSFER_REFRESH_2026-09-09.md` §6, items 1–8.

Custody follow-up for the owner: a hashed raw acquisition of the two readable eCorp GET routes in §1.1 through an authorized workflow run would upgrade the §1 objects from rendered readback to hashed payloads. The acquisition tool does not currently request those routes.

## 5. Out-of-scope pointer, not adjudicated here

The filing-history route that `G3-S001` recorded as HTTP 403 on Sep. 8 is now readable as an index. It shows annual registration `29366217`, filed 5/14/2025 9:28:16 PM for registration years 2025–2026, six days after the board accepted Josh Buice's resignation as president. Its contents were not acquired. This is relevant to the broader Q004 hold (`accessible Georgia filing-history object`) and is left to that question's owner. Q004 state is unchanged by this file.

`PUBLICATION_HOLD = true`.
