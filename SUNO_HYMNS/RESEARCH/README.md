# Historical RESEARCH lane — Dutch Reformed hymnody

## Scope

The Dutch lane was joined on 2026-10-26 by a second lane: **ancient Greek and Latin hymns**, catalogued separately in `ANCIENT_HYMNS_CATALOG.md`. Its first work is PHOS-001 (Φῶς ἱλαρόν); its evidence rules are the same ones below, and its dossier is `DOSSIER_PHOS-001_PHOS_HILARON.md`.

Build a source-grounded history of Dutch Reformed devotional songs and poems used as the basis for modern Russian musical adaptations. Initial authors are Jodocus van Lodenstein, Abraham Rutgers as later reviser, and Jacobus Revius. The wider history of Dutch hymnody and psalmody is a connected research lane, not a synonym for the three current tracks.

Establish original titles and spelling variants, historical genre, composition and publication dates separately, first publication and exact edition, biblical/historical context, author/translator/adapter/reviser roles, melody directions and sources, later hymnbook transmission, exact locators, access and rights boundaries.

## Mandatory repository method

The root Research AGENT_RULES.md and evidence policy are controlling. In every dossier, keep these fields distinct:

- evidenceClass — global A1/A2/A3/B1/C/D, unchanged;
- accessState — FULL_OBJECT_VERIFIED / PARTIAL_OBJECT / CATALOG_ONLY / LINK_ONLY / NOT_ACQUIRED;
- locatorState — EXACT_LOCATOR_VERIFIED / COARSE_LOCATOR_ONLY / LOCATOR_MISSING;
- rightsState — PUBLICATION_ELIGIBLE / STORAGE_ONLY / PRIVATE_STUDY_ONLY / PERMISSION_REQUIRED / RIGHTS_UNKNOWN;
- publicationState — PROMOTE / REFERENCE / SUPERSEDED / BLOCKED;
- global typed HOLDs, when appropriate.

Do not create local meanings for A1, A2 or B1. A B1 source alone cannot support a disputed quote-safe claim. To make a direct quotation quote-safe, identify the edition/version, inspect exact text and surrounding context, and record the exact locator. Do not claim full-object access based only on a catalog or snippet.

## Claim workflow

For each important historical claim:
1. Give it a stable claim ID and state wording actually supported by the evidence.
2. Cite the best primary witness first; add a critical edition and high-quality scholarly study separately.
3. Record the exact page/poem/item/section locator and version consulted.
4. State what the evidence does not establish.
5. Check rights for the underlying work separately from rights in modern transcription, critical apparatus, translation, photograph/scan or published recording.
6. Update the source register and author/track dossier together when a claim changes.

Do not count search results as independent sources. Several pages derived from one edition are not several independent witnesses. Search engines, bibliographic records and reachable URLs are discovery tools until contents and locators are inspected.

## Current source anchors

- Lodenstein 1676 first-edition entrypoint: https://www.dbnl.org/tekst/lode002uyt_01_01/
- Lodenstein critical-edition contents (2005; A. Ros and L. Strengholt): https://www.dbnl.org/tekst/lode002uyt_02_01/index.php
- Revius collection contents, first edition listed as 1630; digital scholarly edition 1930–1935: https://www.dbnl.org/tekst/revi001over01_01/
- Rutgers 1806 Evangelische Gezangen, hymn 68: https://www.dbnl.org/tekst/_eva005evan01_01/_eva005evan01_01_0070.php
- Rutgers attribution: https://www.dbnl.org/tekst/aa__001nieu03_01/aa__001nieu03_01_0176.php
- Missio source chain for Afrikaans Lied 276: https://missio.org.za/songs/lied-276/
- Dutch church-order history, Dordrecht Article 69: https://kerkrecht.nl/node/2149/

- Lodenstein, preface to *Uyt-spanningen* (ed. 1727), the six rules for singing in a house circle, leaves \*3v–\*5r: https://www.dbnl.org/tekst/lode002uyt_03_01/lode002uyt_03_01_0002.php
- The critical edition's introduction (2005), biography and the Zoetermeer singing reform: https://www.dbnl.org/tekst/lode002uyt_02_01/
- Dordrecht 1578 and 1618–19 article 69 on what may be sung: https://kerkrecht.nl/node/2149/

Three source registers exist and should be extended rather than re-searched from scratch. `DUTCH-005_SOURCE_LEDGER_FULL.md` consolidates the hymn and transmission work into one table with a status per record; the two older runs are kept because they hold the order in which things were found. `DUTCH-005_SOURCE_RUN_50PLUS.md` (75 addresses, hymn and transmission) and `DUTCH-005_SINGING_PRACTICE_SOURCES.md` (88 addresses, church singing, the organ ban, the `voorzanger`, the `gezelschappen`, Lodenstein's singing rules). Both carry an honest status per address: opened and read, found in results only, or still a library lead.

See SOURCE_REGISTER.md for limits of each item.

## Current state

Four works are in `DUTCH_HYMN_CATALOG.md`. DUTCH-001/002/003 have prior research and audio/asset work reported in conversation, but no repository-resident lyrics, no verbatim Suno prompts, no final images and no verified publication receipts. DUTCH-004 (*Den nedrigen christen*, Psalm 131) was researched to a complete source dossier in the third pass and carries only a lyric draft.

Candidates in `DUTCH_HYMN_BACKLOG.md` are unrecorded as produced in the current context — which is not proof that the owner never made them elsewhere. The backlog now also carries activation status: `DUTCH-CAND-002` became DUTCH-004.

## File index — what to open for what

| File | Use it for |
|---|---|
| `TRANSCRIPTION_DUTCH-005_1676.md` | the working transcription against which every lyric edit is checked |
| `COLLATION_DUTCH-005_THREE_WAY.md` | 1676 vs 1727 vs 2005: five substantive variants, and which reading to adopt |
| `DUTCH-005_TRANSMISSION_AND_TUNE.md` | the chain 1676 → 1681 → 1718 → 1806 → 1938, and why "Bourgeois" and "psalm 42" are one melody |
| `DUTCH-005_STANZA_3_2_OPTIONS.md` | the open defect in stanza 3 line 2, with three counted options |
| `DUTCH-005_SOURCE_LEDGER_FULL.md` | **the consolidated register**: 64 records for this hymn, 15 opened, 24 found in results, 20 catalogue-only, 5 recorded as unusable — the one place that says what was looked at and what came of it |
| `DUTCH-005_SOURCE_RUN_50PLUS.md` | hymn and transmission addresses with an honest status each |
| `DUTCH-005_SINGING_PRACTICE_SOURCES.md` | church singing, the organ ban, the `voorzanger`, the `gezelschappen` |
| `RHYME_PLAN_DUTCH-005.md` | what the Dutch rhyme does and what a rhymed Russian costs |
| `CLAIM_LEDGER.md` | every historical claim, its status, its sources, its limits |
| `SOURCE_REGISTER.md` | what each source is and what it cannot support |
| `DOSSIER_DUTCH-001…`, `DOSSIER_DUTCH-002…`, `DOSSIER_DUTCH-003…`, `DOSSIER_HERT_STERCKTE_I_II.md` | per-work dossiers |
| `CANDIDATE_DUTCH-004_…`, `CANDIDATE_DUTCH-CAND-021_…` | activation dossiers for works that became DUTCH-004 and DUTCH-005 |
| `AUTHOR_JODOCUS_VAN_LODENSTEIN.md`, `AUTHOR_ABRAHAM_RUTGERS.md`, `AUTHOR_JACOBUS_REVIUS.md` | author files: dates, roles, what is and is not known |
| `DUTCH_HYMN_CATALOG.md`, `DUTCH_HYMN_BACKLOG.md` | what is active and what is only a candidate |
| `DUTCH_REFORMED_HYMNODY.md`, `GENRE_AND_CLASSIFICATION.md` | the wider history and the genre vocabulary |
| `COLLATION_GEZANG205_THREE_WAY.md` | the three-way collation behind DUTCH-002 |
| `AUDIT_2026-10-25_PASS4.md` | what the fourth pass audited and what it could not close |
| `REVIEW_LOG_2026-10-25.md` | what I got wrong, pass by pass |
| `LESSONS_AND_GUARDS.md` | the rules that came out of those failures |

## Two method notes learned the hard way

1. **DBNL slug numbers are not page numbers.** In a `lode002uyt_01_01_00NN.php` URL, `00NN` is a sequential chunk index: slug `0036` shows printed pp. 74–75, `0039` shows pp. 82–84, `0084` shows p. 230. The colophon cites printed pages, so always cite the `[pagina N]` bracket and the poem title. See `CLM-DBNL-SLUG-TRAP`.
2. **Read the 1676 print before the critical edition.** Both *Hert-sterckte* poems and *Den nedrigen christen* are in the 1676 first edition at exact locators. The 2005 edition is a check on sense and apparatus, not the necessary route to the text — and it is copyrighted, so it cannot be the source you quote.

## Открытые HOLD-ы

`OPEN_HOLDS.md` — собранная скриптом `scripts/render_hold_ledger.py` сводка всех незакрытых HOLD-ов реестров: что именно не прочитано, не локализовано или не очищено по правам. Пересобирать после каждого изменения реестров.
