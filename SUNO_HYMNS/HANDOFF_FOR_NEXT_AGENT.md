# Handoff for the next Research / Arena agent

**As of:** 2026-10-26, publication pass (branch `arena/0bdf988d-research`, PR #237)  
**Scope:** continue the SUNO and historical-research workstream without inventing missing assets or disturbing Research root authority.

## Mandatory preflight

Read the repository root files before touching this project:

1. AGENT_RULES.md
2. CURRENT_AUTHORITY.md
3. data/research-authority-registry-v1.json
4. data/repository-evidence-policy-v2.json
5. 00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md
6. SUNO_HYMNS/README.md
7. The specific SUNO or RESEARCH lane README relevant to the task.
8. `SUNO_HYMNS/RESEARCH/LESSONS_AND_GUARDS.md` — the register of errors already made here, with the guard that now catches each. Read it before drafting a lyric, applying a review, or generating artwork, so the same mistakes are not repeated at the owner's expense.
9. `projects/lord-god-strength/RULES.md` — the single rule sheet of this channel: identifiers, markup, description architecture, pins, Telegram, lyric requirements, sources, gates. There is no second rule file and no cross-channel table: the other channel's rules live in its own repository, and mixing them here is how a poetry playlist ends up in a hymn description. `projects/WORKS_LEDGER.md` records what has been made and what has not.
10. `SUNO_HYMNS/SUNO/NEXT_STEPS.md` — the live plan: what is open, who owns it, what blocks what. Start here to see whether your task is already tracked; if it is not, add it instead of inventing a parallel list.
11. `SUNO_HYMNS/SUNO/PUBLICATION_LANE.md` — **before you touch any title, description, pinned comment, Telegram post or tag.** It says which file governs what, where the three copy files are, which five gates must pass, and the eight traps that already cost a release. Note the division of labour: the editorial rules live in `projects/`, split by channel; `video-channel-manager` keeps platform behaviour, exact IDs and anything that reaches a provider. Neither restates the other wholesale, and a contradiction between them stops publication instead of being resolved silently.

Do not promote this scoped project to root authority. Do not change the global evidence vocabulary. Normal repository changes go through a bounded branch and PR.

## Current known works

- DUTCH-001 — *Schepselen niet en Jesus al* / «Всё сотворённое — ничто, Иисус — всё», Jodocus van Lodenstein. One WAV, one 1080p YouTube MP4 and one 320-kbps Telegram MP3 were recorded as prepared in the conversation history.
- DUTCH-002 — *Hert-sterckte in Jehova* / later seven-stanza *Zelfverloochening* (Evangelische Gezangen 1806, no. 68), adapted in Russian as «Блаженно, блаженно — быть ничем». Two exported versions are recorded.
- DUTCH-003 — *Hy droech onse smerten*, Jacobus Revius (first publication 1630), adapted as «Он понёс наши скорби». MP3 filename is known; ID3 readback and the finally selected cover are not confirmed.

The catalog distinguishes asset preparation from public release. Do not mark anything PUBLISHED_VERIFIED unless an actual public URL or direct publication receipt is checked.

## Where the third pass left things

**Resolved or narrowed:**

- Both *Hert-sterckte in Jehova* poems are in the 1676 first edition: **I on pp. 78–81** (28 December 1673) and **II on pp. 82–84** (4 January 1674). II is a **sequel** to I — one week later, sung to I's tune, opening on I's closing image — not a duplicate. Full case: `RESEARCH/DOSSIER_HERT_STERCKTE_I_II.md`.
- `DUTCH_HYMN_CATALOG.md` had cited the **item-34** page as the source of II. Fixed to item 35.
- The second colophon correction `p. 87: 1664→1674` belongs to item **36**, not to II. The date hold therefore covers one poem, not a group.
- DUTCH-004 (*Den nedrigen christen*, Psalm 131) researched from the 1676 print to a full dossier + production package. Tune pointer resolved to printed p. 29; the tune itself is untraced.

**Still open, in priority order:**

1. **Inspect printed p. 84 of the 1676 impression.** This is the only thing standing between the project and an unqualified 4 January 1674. Routes: KB Den Haag **4 B 1** (the copy DBNL photographed), UBA **113: BALIE 250.D12** (the copy transcribed), the DBNL scan bundle `https://www.dbnl.org/arch/lode002uyt_01_01/pag/lode002uyt_01_01.pdf`, or a Delpher/Google Books copy. Direct download from dbnl.org is blocked in the Arena sandbox — use the page-fetch tool for text and a network-permitted environment for binaries.
2. **Acquire the 1674 *Meditatien over eenige van 's Heeren Gods Eygenschappen***. Two modern sources describe it; no copy is held. It is the strongest independent witness for the whole Rees group's dating.
3. **Retry the Nederlandse Liederenbank.** It returns HTTP 403 (KNAW notice, taken offline) as of 2026-10-25. Until it returns, every tune name in this corpus — *Prendete la*, *Onherroepelijke Jeugd*, *Gavotte. A la fronté*, *Rosemont waer gy vliedt* — is untraceable through the normal authority. Do not record "no melody exists" on the strength of a dead link.
4. **Recover the real SUNO prompts for DUTCH-001/002/003.** Still `NOT_CAPTURED`. Nothing was invented to fill the gap, and nothing should be.

**Do not:**

- merge I and II, or use I as the source of DUTCH-002;
- present DUTCH-004's `PROMPT-DUTCH-004-V1` as a recovered prompt — it was authored here and never submitted;
- present the Russian draft as a translation, or as reproducing the *Prendete la* metre, which is unknown;
- copy the 2005 critical edition's text, notes or its editorial expansions of the print's `etc.` abbreviations.

## Where the fourth pass left things (2026-10-25, supplementary brief)

Four things were settled from primary or near-primary sources, and one earlier error was corrected:

1. **DUTCH-002 stanza counts: 14 → 7 → 5.** The 1806 *Evangelische Gezangen* hymn LXVIII has **seven** stanzas (printed pp. 143–144). The **five**-stanza form is the 1938 Hervormde Bundel, **Gezang 205**, which drops 1806 stanzas 4 and 5 but keeps the last couplet of stanza 5 as the close of its own fourth stanza, and replaces `zielverdervend eigen` with `trots, hoogmoedig eigen`. See `RESEARCH/DOSSIER_DUTCH-002_TEXT_HISTORY.md`.
2. **DUTCH-001 read from the 1676 print** (pp. 131–134): eight stanzas, tune line `Rosemont waar gy vliedt`, and eight **different** Christological addresses — no refrain in the source. See `RESEARCH/DOSSIER_DUTCH-001_TRANSLATION_DECISIONS.md`.
3. **DUTCH-003 verified as a sonnet** with the turn at line 9 and six instruments in print order. The Russian text discussed earlier is **not** in the repository and is **not** approved. See `RESEARCH/DOSSIER_DUTCH-003_REVIUS_SONNET.md`.
4. **`Heerlijckheyds Loff` identified** as a distinct ten-stanza poem, 1676 pp. 155–158, 27 August 1665, `Voyse: Un jour &c.`; registered as `DUTCH-CAND-021` with **no** work ID. The notes' `Hoog, omhoog…` is its incipit, not a second title. See `RESEARCH/CANDIDATE_DUTCH-CAND-021_HEERLIJCKHEYDS_LOFF.md`.

**Correction to remember:** the 1806 hymn does **not** have five stanzas. Five is the 1938 count. Do not reintroduce the error.

**The most important thing this pass did not do:** it did not review any Russian lyric, because none is stored here. Do not let a future summary describe the fourth pass as having validated translations.

**Standing text rules** for SUNO work now live in `SUNO/STYLE_AND_PRODUCTION_RULES.md`, with a per-work table that keeps DUTCH-002's 112–120 BPM brief out of the project defaults. **Draft ≠ approved**, and a prompt is not proof of accuracy: see the seven-state table in `SUNO/LYRIC_REGISTER.md`.

## Where the fifth pass left things (2026-10-25, evidence-gap closure)

1. **`heylsaam Niet` located** — 1676, stanza II line 5. It is *not* 1806 wording. The poem qualifies its Nothing three ways: `heylsaam` (II), `eyndeloos` (IV), `grondloos` (VIII).
2. **Gezang 205 collated against the printed 1938 bundel** (Delpher `MMKB06:000000593`, image pp. 724–725) — `RESEARCH/COLLATION_GEZANG205_THREE_WAY.md`. Corrections: the stanza-2 substitution is a pair of changes, not one; the grafted couplet in stanza 4 is 1806 stanza 5 ll. 5–6, and it changes the argument from decree to providence. Melody credit: Johann Christoph Bach. Text credit: Lodenstein, *Bewerking van Abraham Rutgers*. The bundel is a **protected** object.
3. **Access routes worth knowing.** Delpher serves page OCR at `/nl/boeken/view?coll=boeken&identifier=<OBJ>:<IMAGE>`; the image number is not the printed page and items must be bracketed (image 430 = Gezang 18, 640 = 153, 724–725 = 205; image 296 = Psalm 109). In-bundle search and `download/txt` return 404. The WNT at `gtb.ivdnt.org` renders only its JavaScript shell, and Ensie is paywalled — **no dictionary sense has been read in this project**.
4. **`in 't dorre stickt`** narrowed to "stuck fast, choked, in the dry" on rhyme + etymology; still `PENDING_LEXICAL_CHECK`.

## Where the sixth pass left things (2026-10-25, DUTCH-005 activated)

The owner asked for the Dutch hymn with SUNO styles "that we haven't done yet". That is **`DUTCH-005` — *Heerlijckheyds Loff*** (1676, pp. 155–158), the poem previously known as `Heerlijckheyds Loff / Hoog, omhoog…`.

- **What exists now:** `SUNO/DUTCH-005_PRODUCTION_PACKAGE.md` — a ten-stanza literal gloss, a Russian **adaptation** draft v0.1 (`DUTCH-005-RU-DRAFT`), an eight-row deviation table, a per-work musical brief, and **two** SUNO style directions: `PROMPT-DUTCH-005-V1` (epic organ, Georgian-flavoured male monastic choir, one low male lead, ♩≈116) and a documented alternative (organ, low strings, cantor, choir from stanza 4).
- **What does not exist:** any generation, audio, cover, export or publication. The prompt is `AUTHORED_NOT_YET_SUBMITTED`.
- **The text is not print-verified.** All ten stanzas were read in full from the DBNL diplomatic transcription, but the 1676 page images of pp. 155–158 have not been inspected, and the illustration `ill0155` has not been viewed.
- **The tripled word is the spine**, not a chorus: `leven` (III–VI) → `lieven` (VII–IX) → `loven` (X). Do not detach it, and do not add a refrain.
- **Do not reuse the 1938 reworking** (*'t Oog omhoog…*, Bourgeois melody): it is a different, protected object.

**Gate before anything else on this work:** the owner's poetic revision of the Russian draft. It is a draft, not an approved text.

## Validation

`python SUNO_HYMNS/scripts/validate_project_registry.py` is now enforced by `.github/workflows/suno-hymns-registry.yml`. It checks registry state, cross-references, orphan sources, claim-to-work traceability, `EVIDENCE_HOLD` gaps, backlog/catalog Markdown against the JSON, prompt byte-identity with the production package, and read-only behaviour. If you add a source, a claim or a candidate, expect the Markdown/JSON set comparison to fail until both sides agree.

## First work package

0. Read REVIEW_LOG_2026-10-25.md, CLAIM_LEDGER.md, SONGBOOK_REGISTER.md, and GENRE_AND_CLASSIFICATION.md before adding research. Run the read-only project validator: python SUNO_HYMNS/scripts/validate_project_registry.py. Respect the date EVIDENCE_HOLD for II. Hert-sterckte until the original page image is inspected.

1. Locate the exact current lyric file and final prompt for each existing version if they are not available in the active workspace. The Windows paths in ASSET_MANIFEST.md are inventory notes, not GitHub uploads.
2. Record each Suno prompt verbatim, not reconstructed from prose recollection. Store prompt, lyric revision ID, generation date, output filename, duration and cover ID together.
3. For DUTCH-003, read back actual MP3 ID3 tags with ffprobe or a tag reader. A metadata-rewrite command was proposed, but success is unconfirmed. Confirm the final cover after the cool/muted cinematic color pass.
4. For DUTCH-001 and DUTCH-002, revalidate output metadata if the user wants to rely on it; do not overwrite unrelated media.
5. Begin the next historical candidate with the original textual witness, exact bibliographic record, genre classification, biblical anchor if any, and source/rights notes. Prefer one well-closed dossier over many superficial title lists.
6. Update the catalog and source registry together if statuses change. Do not silently delete historical status; record a dated update or supersession.

## Recommended next candidates

1. *'t Cruyce van een christen* (no. 57) or *Genoegen in het cleyne* (no. 47) — short and self-contained; check first whether either collides with an existing release's theme.
2. *Jesus Lijdende Liefde* (no. 41) — Passion theme with a printed tune direction, but it repeats DUTCH-003's subject.
3. *I. Hert-sterckte in Jehova* (pp. 78–81, 28 December 1673) — now fully separated from II and located in the 1676 print; consider only if a paired release with DUTCH-002 is intended.
4. *De algenoegsaamheyd* (item no. 2) — Psalm 73:25 and Luke 10:42 in the title, but theologically close to DUTCH-001.
5. *Niet en al* (no. 54) — still blocked on section count and excerpt policy.
4. *Heil'ge Jesus, wat my lewe* — trace the Dutch source and adaptation chain behind Afrikaans Lied 271 before drafting a Russian version.
6. Conduct a bounded discovery pass through *Hymni ofte Loff-sangen op de Christelijcke feest-dagen ende andersins* (Utrecht tradition, 1615); do not assume the songbook's contents were used uniformly in every congregation.

These are candidates, not approved or completed productions. Re-check the critical-edition table of contents and primary witness before selection.

## Research discipline

- Cite the source that supports each historical claim; exact locators matter.
- Use global Research classes exactly: A1/A2/A3/B1/C/D. Do not invent new meanings.
- A B1 secondary source must not be the sole support for a disputed quote-safe claim.
- Record access, locator, rights and publication state independently.
- Do not reproduce a modern critical edition or songbook in full just because the underlying seventeenth-century work is public domain.
- Separate original title/text, later editor/reviser, translator/adaptor and modern arrangement.
- Keep authorial attribution, publication date, composition date, melody and genre as distinct claims.

## Adjacent work not in the Dutch catalog

The conversation also included a Russian 1 Peter 1 Scripture-song draft with Cantor/organ/monastic-drone section labels, and a separate Passion-confession lyric/visual concept beginning «Не те иудеи, Господь Иисус…». They are recorded as adjacent works only. Their recording/export state and historical attribution are not established here; do not classify them as Dutch historical hymns.

## Where the publication pass left things (2026-10-26)

DUTCH-005 now has a complete publication package for two surfaces, and **nothing is generated, chosen or published**. State is still `LYRIC_DRAFT`.

**New since the sixth pass:**

1. `SUNO/DUTCH-005_YOUTUBE.md` — title options, a 4881-character description (12 bold spans, 5 italic lines), hidden tags, a checklist, and § 0: a verbatim post-mortem of the markup that broke on a live page, so nobody re-runs the same experiment.
2. `SUNO/DUTCH-005_TELEGRAM.md` — the @lordchrist post in Telegram markup, plus an HTML twin.
3. `SUNO/DUTCH-005_PINNED.md` — **two** pinned comments: one on the hymn (date under the last stanza, the meaning of the title, `leven`/`lieven`/`loven`, the edition chain, the missing melody), one on how the Dutch actually sang (psalms only, the 1574 organ ban, the `voorzanger`, the house circles, and Lodenstein's own six singing rules from the preface).
4. `RESEARCH/DUTCH-005_SINGING_PRACTICE_SOURCES.md` — 88 addresses behind the second pinned comment, with honest statuses: 5 opened and read, 74 found in results, 9 still only library leads. Nothing in either закреп rests on a snippet alone.
5. `scripts/check_youtube_markup.py` — the gate, wired into CI together with a check that the copy files carry their fenced bodies.
6. `SUNO/PUBLICATION_LANE.md` — the bridge to the channel standards. Read it first if your task ends in a public post.

**The one thing worth reading before anything else:** Lodenstein's preface to *Uyt-spanningen* (1727 edition, leaves \*3v–\*5r) is not a dedication, it is a manual for singing in a house circle — six rules, including `'t hardste schreeuwen en is het beste singen niet`. That single source carries the second pinned comment and most of the "how they sang" section in the description.

**Do not:**

- deliver marked-up copy to the owner as a block quote — the chat renders `*…*` away and the asterisks never reach the clipboard; always a fenced block;
- "fix" broken markup by deleting it;
- carry Telegram `**bold**` into a YouTube file: there it prints literally;
- call the pinned comments publication, or attach a URL that has not been checked;
- describe the hymn as written for public worship. It was written for a house circle, and that is the fact the copy is built on.

**Still open, in priority order:** the lyric defect at stanza 3.2 («После земных невзгод»); the cover (references live outside the repository); the title separator `✦` or `✝`; a live Studio check of the description and both pinned comments; the 1676 page images of pp. 155–158 (only the text layer has been read).
