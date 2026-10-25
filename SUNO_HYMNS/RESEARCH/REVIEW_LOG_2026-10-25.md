# Review log — SUNO_HYMNS project bootstrap

Date: 2026-10-25  
Branch: arena/dutch-hymns-suno-research-20261025  
Base snapshot originally inspected: f38b194a99fdc6cc66b86fcc4c1b217da7e945a0

## Changes identified by the second audit

1. **Two poems called Hert-sterckte in Jehova.** The critical edition distinguishes item 34 (I, dated 28 December 1673 with its own melody directions) and item 35 (II). The current Russian track follows the later Rutgers hymnbook chain for II; I has been added as a separate candidate.
2. **Date emendation for II.** The digital material reads 4 January 1674, but records that the original print erroneously says 1664 and the online colophon records a 1664→1674 correction. The specific date claim now carries EVIDENCE_HOLD until the original page image is checked.
3. **First edition versus critical edition.** The 1676 book is a primary historical witness and DBNL marks the underlying work Auteursrechtvrij; the digital rendering is diplomatic, with omissions and explicit editorial corrections. The 2005 critical edition by Ros and Strengholt is explicitly copyright-protected. The source registry now separates historical evidence class, access state and reproduction rights.
4. **Utrecht Hymni 1615 access layer.** The accessible DBNL item is the 1967 facsimile edited by Jan van Biezen and Marie Veldhuyzen, not an independent direct scan of the 1615 original. The facsimile is copyright-protected.
5. **Revius distinction.** The 1630 first-edition object has not been independently acquired; the exact sonnet page currently used comes from W.A.P. Smit's 1930–1935 scholarly edition. Composition date and original melody remain unverified.
6. **Status hygiene.** Production asset preparation, exact prompt capture, actual metadata readback, rights and public publication are recorded separately.
7. **Broader backlog.** Added directly locatable first-edition candidates with tune directions and a separate discovery queue for the broader Uyt-spanningen contents. Discovery items remain candidates; not all are necessarily hymns or appropriate for a full-length SUNO adaptation.
8. **Machine checks.** Added author, claim and songbook registries plus a read-only cross-reference/state validator. These are project-local tooling; they do not alter root authority or global evidence policy.

## Still open after this commit

- Inspect the actual 1676 page image for the 1664 misprint and resolve the date HOLD only with recorded visual evidence.
- Acquire / inspect the 1630 Revius leaf if a claim requires original punctuation, physical layout or edition variants.
- Recover exact lyric versions and verbatim SUNO prompts from an authoritative record.
- Read actual media metadata and identify the final Revius cover.
- Verify YouTube/Telegram publication URLs before any publication-status change.
- Continue rights review before redistributing a modern critical edition, facsimile, translation or recording.


The follow-up state pass removed source- and book-level EVIDENCE_HOLD where the uncertainty was narrower than the whole object. The 1664→1674 dispute remains on the specific claim CLM-HERT-II-DATE-1674. The DUTCH-001 tune/date and Revius 1630 first-edition claims are marked as needing primary-witness collation where the exact accessed text is a later scholarly edition.

---

# Third pass — 2026-10-25 (branch `arena/0bdf988d-research`)

Continuation of PR #236's lane, merged into the session branch. This pass read the historical witnesses directly instead of relying on the previous summaries.

## 1. Both *Hert-sterckte in Jehova* poems are in the 1676 first edition

Earlier records implied the two poems were known chiefly through the 2005 critical edition (item 34/35) and the 1971 anthology. They stand in the 1676 print itself: **I on pp. 78–81** (15 stanzas, 28 December 1673) and **II on pp. 82–84** (14 stanzas, 4 January 1674). Correction: `DUTCH_HYMN_CATALOG.md` had cited the item-34 page `…_02_01_0039.php` as the source of **II**; the correct item is 35, `…_02_01_0040.php`.

## 2. The relation between the two poems is textual, not merely titular

II has no tune of its own: it prints `Te singen als boven pag.78. Soet Geselschap dat met my, &c.`, and the 2005 apparatus states that the direction refers to the preceding text. The same apparatus cross-references I's line 89 (*In dien Ocean*) for II's opening *daar*. Together with the one-week interval and the shared place, II is a deliberate sequel. It is not a recension of I.

## 3. The date hold is narrowed, not lifted

- The DBNL colophon lists `p. 84: 1664 → 1674`, so the transcription's `1674` is an **emendation**.
- The **1727 ninth edition** independently prints `4 in Loumaand 1674`. This is the only *printed* witness in the project that actually reads 1674, and it was not previously recorded.
- The 1971 anthology prints 1674 and footnotes `Er staat abusievelijk: 1664`.
- The second listed correction, `p. 87: 1664 → 1674`, belongs to item **36**, *'t Verheven Herte* (11 January 1674) — **not** to II. A related correction at p. 7 (`1565 → 1665`) shows a recurring compositor-level digit fault.
- Chronological corroboration: in December 1673 Lodenstein was a French hostage; the group was printed in **1674** as *Meditatien over eenige van 's Heeren Gods Eygenschappen*.

`CLM-HERT-II-DATE-1674` therefore stays on `EVIDENCE_HOLD` — the 1676 leaf has still not been inspected — but the hold now covers only the literal reading of that impression. What is missing and where to look are recorded in the claim's `evidenceGap` / `nextCheck`.

## 4. New candidate researched: `DUTCH-004` — *Den nedrigen christen, Op Psalm 131*

Activated from `DUTCH-CAND-002`. Full text read on printed pp. 74–75 and collated against the 1727 edition; tune pointer resolved to printed p. 29; rights separated by layer; a Russian adaptation draft and a production package prepared. No melody was invented, no composition date inferred, and no generation was attempted.

## 5. Locator defect found and recorded

The numeric slug of a DBNL `lode002uyt_01_01_00NN.php` URL is a **chunk index, not a printed page**: slug `0036` shows pp. 74–75, `0039` shows pp. 82–84, `0084` shows p. 230. The colophon cites printed pages, so reading `p. 84` as `…_0084.php` lands on an unrelated poem. Recorded as `CLM-DBNL-SLUG-TRAP` and in the dossier.

## 6. Validator and CI

- The validator gained: globally unique version IDs; prompt text must be **byte-identical** to the published production package; `claimIds` cross-references with every claim either work-linked or explicitly `projectLevel`; `EVIDENCE_HOLD` must carry `evidenceGap` and `nextCheck`; orphan-source detection; backlog/catalog Markdown must equal the JSON ID sets; `PERMISSION_REQUIRED` must retain `RIGHTS_HOLD`; registries must agree on `asOf`.
- Each new rule was tested by deliberately breaking the data in a scratch copy and confirming a non-zero exit.
- Added `.github/workflows/suno-hymns-registry.yml` — path-scoped to `SUNO_HYMNS/**`, read-only, with an assertion that the validator does not modify the working tree and a duplicate-JSON-key check. It duplicates no existing workflow; no other workflow inspects `SUNO_HYMNS/`.

## Still open after this pass

- Inspect printed p. 84 of the 1676 impression (KB 4 B 1 / UBA 113: BALIE 250.D12 / the DBNL scan bundle) and record the reading.
- Acquire the 1674 *Meditatien* pamphlet and collate its four poems.
- Retry the Nederlandse Liederenbank when it returns online (offline since at least 2026-10-25, HTTP 403).
- Inspect the 1676 page images of pp. 74–75 to close the DUTCH-004 typography `LOCATOR_HOLD`.
- Recover the exact submitted SUNO prompts for DUTCH-001/002/003 — still `NOT_CAPTURED`; nothing was invented here to fill the gap.

# Fourth pass — 2026-10-25 (supplementary brief)

Scope: check the four works against a set of working notes from earlier sessions, without treating those notes as facts. Nothing in this pass changed any Russian lyric, because **no Russian lyric is stored in the repository**.

## 1. The 1806 hymn has seven stanzas, not five

Read in full: *Evangelische Gezangen* (1806), **LXVIII Zelfverloochening**, printed pp. 143–144. Seven numbered stanzas. The "five" figure belongs to the **1938** Hervormde Bundel, Gezang 205. The error is corrected in the track catalog, the source register and the new DUTCH-002 dossier.

## 2. The exact omissions in the 1938 form

Gezang 205 keeps 1806 stanzas 1, 2, 3, 6 and 7; **omits stanzas 4 and 5** (`Niets met al, niets zijn wij waardig…`; `U te danken zijn wij schuldig…`), while keeping the **last couplet of stanza 5** as the close of its own fourth stanza — a deletion plus a graft. It also replaces `zielverdervend eigen` with `trots, hoogmoedig eigen`, weakening a spiritual diagnosis into a moral one. Known only from two agreeing web transcriptions: `EVIDENCE_HOLD` until the printed bundel is collated.

## 3. DUTCH-001 read from the print, and the tune line corrected

The 1676 print, pp. 131–134, gives eight stanzas and the tune line **`Rosemont waar gy vliedt`** (the registry had the critical edition's `waer`). The eight Christological addresses were checked one by one and do differ — which is why a single universal refrain would be an adaptation, not a translation.

## 4. `Heerlijckheyds Loff` identified

A distinct ten-stanza poem, 1676 pp. 155–158, incipit `HOog! om hoog! mijn siel, na boven!`, tune line `Voyse: Un jour &c.`, dated 27 August 1665, item 56. The notes' `Heerlijckheyds Loff / Hoog, omhoog…` was one text, not two: the second element is the incipit. Registered as candidate `DUTCH-CAND-021` — **no work ID, no lyric, no prompt, no track**. The 1938 bundel's *'t Oog omhoog, het hart naar boven!* is a modernised reworking to a Bourgeois melody and must not be quoted as the 1665 poem; note that the 1938 bundel therefore holds **two** different Lodenstein hymns.

## 5. DUTCH-003 confirmed as a sonnet, and the discussed Russian line flagged

The 14-line text was checked line by line: octave of negations, turn at **line 9** with a doubled self-identification, six instruments in the order tree/cross → rope → nail → spear → scourge → bloodied crown, causal close. The discussed Russian turn («…я — виновник мук Твоих») converts an **agentive** claim into a claim of causation; that is a deviation to record if adopted, not an equivalent. The earlier Russian text is **not approved**.

## 6. Statuses separated, and no prompt invented

`SUNO/LYRIC_REGISTER.md` now carries a seven-state table (source text / verified translation / working draft / prompt / generation output / user-approved / unverified history) and states plainly that no work in the catalog has a verified translation. `SUNO/STYLE_AND_PRODUCTION_RULES.md` now carries the eight standing text rules, with a precedence note and a per-work table separating DUTCH-002's 112–120 BPM brief from project defaults.

## 7. Registry and gate

Six sources and eight claims added; candidate `DUTCH-CAND-021` mirrored in the backlog Markdown. `validate_project_registry.py` passes: 44 sources, 3 authors, 4 tracks, 33 claims, 9 songbooks.

## Still open after this pass

- Collate the printed 1938 Hervormde Bundel (Delpher `MMKB06:000000593`) for Gezang 205 and for *'t Oog omhoog*.
- WNT checks for the eight DUTCH-001 expressions; `in 't dorre stickt` and `Geven op de hand` remain low-confidence.
- Locate `heylsaam Niet`: **not present** in the 1806 text checked, so it belongs to the 1676 poem — the 1676 stanza has not been re-read for it in this pass.
- Acquire the 1630 Revius leaf.
- Recover the Russian drafts and the verbatim SUNO prompts for DUTCH-001/002/003.

# Fifth pass — 2026-10-25 (closing the evidence gaps that the fourth pass left)

Scope: take the four items the fourth-pass audit listed as "still open" and see which were actually reachable. Two closed, one moved, two are now documented dead ends with the reason.

## 1. `heylsaam Niet` — found

The phrase is in the **1676** poem, stanza **II, line 5** (`Sig tot 't heylsaam Niet te neygen`), read in full this pass at printed pp. 82–84. It is **not** in the 1806 hymn, which replaces the clause with `Om zich tot dien wil te neigen`. The open question is closed, and the phrase must never be quoted as 1806 wording.

The same reading turned up a related fact: the poem qualifies its "Nothing" three different ways — `heylsaam Niet` (II), `'t eyndeloos Niet` (IV), `'t grondloos Niet` (VIII). None is nihilism, and no translation should reduce them to one word.

## 2. Gezang 205 (1938) — collated against the printed book

The printed bundel was reached through Delpher page images (`MMKB06:000000593`, image pp. 724–725). Result: the five-stanza count and the composition are **print-verified**, and two fourth-pass details needed correcting.

- The stanza-2 change is a **pair**: `zielverdervend` → `trots, hoogmoedig` in line 1 **and** `Werp die trotsheid dan` → `werp dien hoogmoed dan` in line 5. The word for pride moves out of the prayer into the diagnosis.
- The couplet closing the 1938 fourth stanza is 1806 **stanza 5, lines 5–6**, grafted onto 1806 **stanza 6, lines 1–4**. It replaces 1806's own couplet, which asserted that what God decides *is* wisdom. The 1938 couplet asserts that God knows what would harm us. **The two hymnals therefore explain `Voor 't geloof is alles goed` differently** — decree in 1806, providence in 1938.
- Printed credits: melody `Johann Christoph Bach (1642—1703)`, text `Jodocus van Lodenstein … Bewerking van Abraham Rutgers (1751—1809)`. The Rutgers chain is now attested at the 1938 end too, and the 1938 tune is not the 1674 tune.
- **Rights:** Delpher marks the object *"Auteursrechtelijk beschermd"*. The 1938 bundel is protected, whatever the status of the 1676 poem.

New file: `COLLATION_GEZANG205_THREE_WAY.md`. Remaining gap: **stanza 1** of Gezang 205 was dropped by the page OCR and still rests on web transcriptions.

## 3. DUTCH-001 lexis — narrowed on internal evidence, still not dictionary-verified

`in 't dorre stickt` rhymes with `verquickt`, and the etymological record makes the "smother" sense of *stikken* the same word as *stikken* "to stitch", an intensivum of *steken*, glossed *"blijven steken, niet verder kunnen"*. The narrowed gloss is **stuck fast, choked, in the dry**. Confidence rises from low to medium; the status stays `PENDING_LEXICAL_CHECK`.

The WNT itself was **not** consultable: the Geïntegreerde Taalbank serves only a JavaScript shell, and Ensie's Van Dale 1898 is paywalled. Both are recorded as sources with their access limits, so no future pass can mistake an attempt for a lookup.

## 4. Two dead ends, now documented

- **Revius 1630.** DBNL's title record for the 1630 collection lists only the 1930–35 Smit edition as an *edition*; there is no transcription of the 1630 print. The leaf is still `NOT_ACQUIRED`.
- **`'t Oog omhoog` in the 1938 bundel.** Not located. What was established is the mechanism: the bundel prints the composer above an item and the author below (Gezang 204: `Louis Bourgeois` above, `Johannes Helder` below), which is how a 16th-century tune name attaches to a 20th-century item. The Bourgeois claim therefore stays `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`.

## 5. Registry and gate

Five sources and two claims added; four claims revised. `validate_project_registry.py` passes: **49 sources, 3 authors, 4 tracks, 35 claims, 9 songbooks**.

## Still open after this pass

- 1938 stanza 1 (page image, not OCR).
- The 1630 Revius leaf.
- WNT for the eight DUTCH-001 expressions and `wilt gy my`.
- Printed p. 84 of the 1676 impression (the 1674 hold).
- `'t Oog omhoog` in the 1938 bundel.
- The Russian drafts and verbatim SUNO prompts — unchanged, still absent.
