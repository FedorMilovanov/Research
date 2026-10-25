# Handoff for the next Research / Arena agent

**As of:** 2026-10-25  
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

## First work package

1. Locate the exact current lyric file and final prompt for each existing version if they are not available in the active workspace. The Windows paths in ASSET_MANIFEST.md are inventory notes, not GitHub uploads.
2. Record each Suno prompt verbatim, not reconstructed from prose recollection. Store prompt, lyric revision ID, generation date, output filename, duration and cover ID together.
3. For DUTCH-003, read back actual MP3 ID3 tags with ffprobe or a tag reader. A metadata-rewrite command was proposed, but success is unconfirmed. Confirm the final cover after the cool/muted cinematic color pass.
4. For DUTCH-001 and DUTCH-002, revalidate output metadata if the user wants to rely on it; do not overwrite unrelated media.
5. Begin the next historical candidate with the original textual witness, exact bibliographic record, genre classification, biblical anchor if any, and source/rights notes. Prefer one well-closed dossier over many superficial title lists.
6. Update the catalog and source registry together if statuses change. Do not silently delete historical status; record a dated update or supersession.

## Recommended next candidates

1. *Niet en al, Dat is: Des werelds ydelheyd en Gods Al-genoegsaamheyd* (Lodenstein, no. 54 in the critical-edition contents) — a thematic companion to the existing “creature nothing / Jesus all” track; avoid merely repeating the same Russian lyric.
2. *Den nedrigen christen, Op Psalm 131* (Lodenstein, no. 32) — a clear biblical anchor and distinct theme.
3. *De algenoegsaamheyd* (Lodenstein, item no. 2), associated in the contents with Psalm 73:25 and Luke 10:42; verify exact title and references in the critical text.
4. *Heil'ge Jesus, wat my lewe* — trace the Dutch source and adaptation chain behind Afrikaans Lied 271 before drafting a Russian version.
5. *Jesus lijdende liefde* (Lodenstein, no. 41) or a Revius Passion-cycle candidate after checking its primary source and textual status.
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
