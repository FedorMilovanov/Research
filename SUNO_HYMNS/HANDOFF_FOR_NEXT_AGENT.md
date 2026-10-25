# Handoff for the next Research / Arena agent

**As of:** 2026-10-25, third pass (branch `arena/0bdf988d-research`, continuing PR #236's lane)  
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
