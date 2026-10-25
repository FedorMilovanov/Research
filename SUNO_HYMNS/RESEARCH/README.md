# Historical RESEARCH lane — Dutch Reformed hymnody

## Scope

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

Two source runs are already assembled and should be extended rather than re-searched from scratch: `DUTCH-005_SOURCE_RUN_50PLUS.md` (75 addresses, hymn and transmission) and `DUTCH-005_SINGING_PRACTICE_SOURCES.md` (88 addresses, church singing, the organ ban, the `voorzanger`, the `gezelschappen`, Lodenstein's singing rules). Both carry an honest status per address: opened and read, found in results only, or still a library lead.

See SOURCE_REGISTER.md for limits of each item.

## Current state

Four works are in `DUTCH_HYMN_CATALOG.md`. DUTCH-001/002/003 have prior research and audio/asset work reported in conversation, but no repository-resident lyrics, no verbatim Suno prompts, no final images and no verified publication receipts. DUTCH-004 (*Den nedrigen christen*, Psalm 131) was researched to a complete source dossier in the third pass and carries only a lyric draft.

Candidates in `DUTCH_HYMN_BACKLOG.md` are unrecorded as produced in the current context — which is not proof that the owner never made them elsewhere. The backlog now also carries activation status: `DUTCH-CAND-002` became DUTCH-004.

## Two method notes learned the hard way

1. **DBNL slug numbers are not page numbers.** In a `lode002uyt_01_01_00NN.php` URL, `00NN` is a sequential chunk index: slug `0036` shows printed pp. 74–75, `0039` shows pp. 82–84, `0084` shows p. 230. The colophon cites printed pages, so always cite the `[pagina N]` bracket and the poem title. See `CLM-DBNL-SLUG-TRAP`.
2. **Read the 1676 print before the critical edition.** Both *Hert-sterckte* poems and *Den nedrigen christen* are in the 1676 first edition at exact locators. The 2005 edition is a check on sense and apparatus, not the necessary route to the text — and it is copyrighted, so it cannot be the source you quote.
