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

# Sixth pass — 2026-10-25 (DUTCH-005: *Heerlijckheyds Loff* activated and packaged)

The owner asked for the Dutch hymn with SUNO styles "that we haven't done yet" — the text identified in the fourth pass as *Heerlijckheyds Loff* and left as a candidate. It is now a work.

## 1. Activation, with the catalog checked first

`DUTCH-CAND-021` → **`DUTCH-005`**. No duplicate was created: the research record stays in `CANDIDATE_DUTCH-CAND-021_HEERLIJCKHEYDS_LOFF.md`, and the production record is new. The two claims about this text had been `projectLevel` because no work existed; they now hang off the work, and the flag was removed rather than left as a lie.

## 2. The whole text read, and its shape recorded

All ten stanzas of the 1676 print (pp. 155–158) were read. Structure: four statement lines, a call line and its abbreviated repeat (`etc.` — a repeat instruction, not a lacuna), the tripled word with its object, the call again, a closing line. Stanza I is printed in full and is the metrical model for III–X. The tripled word moves **`leven` (III–VI) → `lieven` (VII–IX) → `loven` (X)** — the poem's architecture, inside the stanzas, not a chorus.

**Still not print-verified:** the page images have not been inspected, and the illustration `ill0155` has not been viewed.

## 3. What was authored, and what was deliberately not

Authored: a literal gloss, a Russian **adaptation** draft v0.1, an eight-row deviation table, a per-work musical brief, and two style directions.

Not authored: any claim that the Russian is a translation; any claim about the melody; any claim about the illustration; any generated audio; any publication. `PROMPT-DUTCH-005-V1` is `AUTHORED_NOT_YET_SUBMITTED`.

**Two uncertainties kept visible instead of smoothed:** I.7 has no expressed negation in the Dutch (elliptical reading adopted, the "costly" pun recorded as a secondary sense), and the tripled device is rendered with a noun in III–IX but an infinitive in X, where Dutch triples infinitives throughout.

## 4. Registry and gate

Three claims added; candidate activated; work added to the track catalog with `workType: DEVOTIONAL_SONG_WITH_TUNE_DIRECTION` and production state `LYRIC_DRAFT`. `validate_project_registry.py` passes: **49 sources, 3 authors, 5 tracks, 38 claims, 9 songbooks**.

## Still open on DUTCH-005

- Owner poetic revision of the Russian draft.
- The 1676 page images of pp. 155–158, and the illustration.
- Choice between the two style directions.
- The Dutch Song Database for *Un jour &c.* — no melody claim until then.

# Seventh pass — 2026-10-25 (artifact separation, lyric revision v0.2)

The owner pointed out that the delivery had mixed lyrics and style into one sheet, against the project's own rule.

## 1. The rule that was broken, quoted

`SUNO/README.md`: *"Keep these artifacts separate: source-language historical text; normalized transcription text; literal translation for analysis; Russian literary adaptation; SUNO-ready lyric with vocal cues and optional stress marks; published/recorded take."*
`SUNO/LYRIC_REGISTER.md`: *"Keep clean public lyric and pronunciation-marked SUNO lyric separate."*

One file holding Dutch text, gloss, Russian lyric, tags and style prompts is exactly what those two lines forbid.

## 2. What replaced it

`DUTCH-005_LYRIC_AND_STYLE_SHEET.md` is **deleted**. In its place, three files, each with one job:

| File | Contains | Does not contain |
|---|---|---|
| `SUNO/DUTCH-005_LYRICS.md` | clean Russian lyric, v0.2, changelog, rhyme/metre statement | tags, prompts, gloss |
| `SUNO/DUTCH-005_LYRICS_SUNO.md` | the same wording with section labels and the minimum stress marks | prompt text, analysis |
| `SUNO/DUTCH-005_STYLE.md` | style prompts only, primary + one option | any lyric |

The Dutch text and the literal gloss stay in the production package §2–§3, where the research lane expects them.

## 3. The lyric itself revised to v0.2

Nine changes, each with a reason in the lyric file's changelog: the stanza-1 clause restored as one sentence; the stanza-2 close given the right subject (`Сердце ставит выше всего` — the Dutch subject is the blood); stanza 3's vocative and `onsigtbaerlijck` restored; stanza 6's participle calque replaced and the call repeated in full rather than half; stanza 8's line shortened; stanza 9's false friend `обаяния` replaced by `отрада`; stanza 10's plural/singular address corrected.

**Rhyme is declared, not faked:** the Dutch rhymes its thrice-repeated call line with the closing line in all eight stanzas that use the device. The Russian reproduces the **device** everywhere and the **rhyme pair** only in stanzas 1, 2 and 10, leaving the rest unrhymed rather than filling them with words the Dutch does not have.

## 4. Registry

`DUTCH-005-RU-v0.2` with three `lyricFiles` paths; the claims ledger states why the artifacts are separate and quotes the rule. Validator passes: **49 sources, 3 authors, 5 tracks, 38 claims, 9 songbooks**.

# Eighth pass — 2026-10-25 (review response: tags, metre, diction, two-printing collation)

The owner reviewed the delivery and found six defects. Five were real and are fixed; one is a process failure that this pass records rather than argues about.

## 1. The delivered block was not Suno-ready

The lyric was shown with stanza numbers `1`–`10` and no structural tags. Numbers are editorial, not performance structure, and a model may read them as text. `SUNO/DUTCH-005_LYRICS_SUNO.md` now carries `[Intro]`, `[Verse 1]`…`[Verse 10]`, `[Outro]`, with three deliberate accents: verse 7 (lead alone, organ thins — the poem's turn), verse 8 (choir rejoins, building), verse 10 (full choir, one inline echo). **No `[Chorus]`** — the source has no refrain, and its repetitions are already inside the stanzas.

## 2. The metre claim was false

v0.2 asserted "7–8 syllables" while containing lines of 11, 12 and 13. The claim is withdrawn. Actual counts are now tabulated per stanza: statement 6–10, call 6–9, tripled 9–11, close 7–9. The honest conclusion is stated: that is sufficient for **syllabic declamation**, not for a fixed melodic setting, and a strictly metrical version would be a separate, larger revision.

## 3. Seven lines rewired

Stanzas 1, 2, 3, 6, 7, 8, 9 and 10 changed, each with a reason in the lyric's changelog: the invented "свет" removed; the blood restored as the subject in stanza 2; the vocative unambiguously marked in stanza 3; the sentence no longer broken across lines in stanza 6 and `в лоне` (comic in Russian) replaced; the subject of «готовая / находит» made explicit in stanza 7; `если что любить` replaced by `коль что любить` in 8 and 9; `кто здесь прах` given a parsable predicate in 10.

## 4. The style asked for the wrong voice

`one strong low male lead` became `one clear tenor-baritone lead`, with `no melisma, no stretched vowels, strictly syllabic, one syllable per note`, `short two-bar organ introduction`, `all ten verses sung in order with no cuts`, and prohibitions on a husky or excessively low lead and on long instrumental interludes. Tempo 116 → 118.

## 5. The source text is now collated across two printings

`Heerlyckheyds Loff` was fetched from the **1727 ninth edition**, which prints it at **the same pages 155–158** with the same title, tune line, stanza count and date. Four variants were found and recorded (`CLM-DUTCH-005-VARIANTS`), including the resolution of the `dat`/`dan` question at VII.8 in favour of `dan`.

## 6. The process failure

The `DUTCH-005` ID was assigned in the same pass that resolved the identity, on the strength of a transcription. That is what the record now states in `identityStatus: CONFIRMED_BY_TWO_PRINTINGS_TYPOGRAPHY_UNVERIFIED`, with the note that the ID was assigned before any page image was checked. **A green validator proves none of this**; it proves only that the repository's cross-references are consistent.

## 7. Validator

Extended so that a prompt may live in a dedicated style document: `version.promptDocuments` is now accepted, and the prompt must appear verbatim in at least one listed document. This follows the artifact split the lane already required; it does not weaken the drift check.

`validate_project_registry.py` passes: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.

# Ninth pass — 2026-10-25 (delivery format and five styles)

Two owner requirements, both now rules rather than habits of one work.

## 1. The header line

`SUNO/README.md` now specifies a **single line**, title first, author second, no labels:

```
«Слава Господня» — Йодокус ван Лоденстейн
```

The earlier wording of the rule (separate `Название:` and `Автор:` rows) was replaced, because the owner prefers the one-line form. The historical title, the source and the status follow underneath — never above.

## 2. Five style directions per work

`SUNO/STYLE_AND_PRODUCTION_RULES.md` now requires **five genuinely distinct directions**, not one, with a shared floor: syllabic declamation, one syllable per note, no melisma, no stretched vowels, intelligible lead, all stanzas in order, no invented chorus, short intro. Instrumentarium, region and era of the idiom, tempo, metre and the point of ensemble entry are free to differ.

`DUTCH-005_STYLE.md` was rewritten accordingly: A epic organ + Georgian monastic choir (118, D minor); B Renaissance wind consort — cornetto, sackbuts, shawm — with four male voices (112, D dorian); C viol consort + chamber organ + solo tenor, ensemble growing verse by verse (100, G minor); D Byzantine-style ison under a baritone cantor (free); E metrical chorale, unison male voices and organ (126, A minor). Each carries an exclude list, a purpose and its risk; the comparison table states completeness risk per direction, D highest and E lowest.

**A holds the primary slot only because the registry must carry one `promptText`.** No direction is preferred, and the choice is recorded as an open check.

## 3. Registry

`styleVariants` (five IDs) added to `DUTCH-005-RU-v0.3`, with a note that the primary slot is a registry necessity, not a preference. Validator passes: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.

# Tenth pass — 2026-10-25 (stanza 8, lines 3–4: "куда уйдёт?")

The owner asked where the beauty "goes". It goes nowhere: the Dutch verb is `verdwijnt`, **vanishes**, and there is no destination in it. The Russian `уйдёт` in v0.3 imported one.

Two defects in one line, both fixed in v0.4:

1. **Direction invented.** `уйдёт` → `пропадёт` (ceases to be, is gone), with no "where".
2. **Consequence invented.** The Dutch pairs two alternatives — `Min vermaackt, **of oyt** verdwijnt`, "pleases less **or ever** vanishes". v0.3 made the second a result of the first ("меньше радует — и уйдёт"). v0.4 restores the disjunction: `Меньше радует иль пропадёт`.

A third thing is now recorded as an **interpretation, not a settled reading**: the antecedent of `Die`. It may agree grammatically with `Schoonheyd` itself, which would make the addressed Beauty capable of vanishing — contradicting stanza IX and the poem's argument. The earthly-beauties reading is adopted for that reason and flagged as a choice.

Verse 8 in both lyric files, the changelog, the measured syllable table (line 4: 8 → 9) and `DUTCH-005-RU-v0.4` in the registry were updated together. Validator re-run.

# Eleventh pass — 2026-10-25 (full re-read of all ten stanzas; stress)

The owner asked for the whole text to be re-read line by line, not for reassurance, and reported two words the model had stressed wrongly: **драго́е** sung as *дра́гое*, **тре́пета** sung as *трепе́та*. Both were written correctly and unmarked — which is the defect: an unmarked word is a word the model guesses.

## 1. What was wrong in the wording

Twelve defects in v0.4, all in lines I had already passed:

- **I.4** — `maar` dropped: "there where one sees Jesus" instead of "**only** there". The stanza's whole argument rides on that word.
- **I.7** — the line could be read as a claim about ownership ("this is not your life") rather than about direction. Rewritten.
- **II.3** — **an image that was not in the text.** v0.4 read «как туман», a fog. The Dutch is `Lusten met 't gebruyck verdwijnen`: pleasures vanish *with the use of them*. Fog is mine, not Lodenstein's.
- **IV.5** — the vocative was lost (`O! yd'le siel`): «О, праздная» addressed nobody in particular.
- **IV.9** — `goedig schenckt` is "kindly bestows", not "grants mercy".
- **V.1** — «Жизнь добродетелей святых» said "the life **of the saints'** virtues": a possessive the Dutch does not have, plus saints who are not in the line.
- **VI.1** — singular relative with plural verb; `не знаете` had no agreeing subject.
- **VI.9** — "to begin virtue" is not Russian and loses `het deugdsaam leven`.
- **VII.1** — a comma split a single predicate.
- **VIII.2–4** — `wat hier schoon schijnt` = what **seems** beautiful here; the old line asserted beauty and left `Die` without a Russian antecedent.
- **X.5** — `mond` is the mouth, not speech.
- **X.8** — `кто` cannot refer to dust; `hier is stoff` needs `что`.

## 2. Stress

Every polysyllabic word in the SUNO-ready file now carries a combining acute after its stressed vowel; monosyllables and words whose `ё` already carries the stress are left bare. Two-layer rule kept: the accents are in `DUTCH-005_LYRICS_SUNO.md` only, and the clean lyric stays unmarked for reading and for any published text.

Checked mechanically after the edit: **90 lyric lines in both files, identical once the marks, the tags and the one echo are stripped**; **226 polysyllabic word tokens, 218 marked**, the eight unmarked being forms whose `ё` already sets the stress (влечёт, даёт, крадёт, моё, пойдёт, пропадёт); **no word carries two accents**. `Эта` → `Э́та` was caught by that check and fixed.

The project rule was the cause and has been rewritten: `STYLE_AND_PRODUCTION_RULES.md` now requires full marking, and says why — partial marking leaves every other word to the model.

## 3. Metre, re-counted

The syllable table was re-measured by machine rather than by eye and corrected in four places (V.1 11 → 10, V.2 6 → 5, VIII.1 8 → 9, X's close 8 → 11). Ranges as measured: statement 5–10, call 6–9, tripled 9–11, close 6–11. **No regular metre is claimed**; two short lines and one long line are declared with their reasons.

## 4. Registry

`DUTCH-005-RU-v0.5`; `lyricRevisionNote`, `researchViews.note`, `DUTCH_HYMN_CATALOG.md`, `PROMPT_AND_VERSION_REGISTER.md`, `STATUS_LEDGER.md`, `LYRIC_REGISTER.md` and `DUTCH-005_PRODUCTION_PACKAGE.md` (v0.5, deviations D-09…D-12) updated together. Two of those files still said v0.2 and v0.3 — stale, now fixed. Validator: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.
