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
