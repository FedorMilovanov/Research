# LE CANON SUCRÉ — current Research authority

**Authority ID:** `LE-CANON-SUCRE-WAVE2-AUDITED-2026-08-09`  
**Status:** `ACTIVE RESEARCH / FAIL-CLOSED / NO PRODUCT WRITE`  
**Research snapshot originally examined:** `217fa015b6957c6577e4261bb74055d5e2c1a99c`  
**Working branch:** `agent/le-canon-sucre-research-wave1-20260809`  
**Draft PR:** `#154`

## Governing scope

This authority governs the multilingual evidence corpus for 15 candidate canonical French pâtisseries. It is **Research-only** and does not authorize edits or publication in `Milovi_School`, `gb-is-my-strength`, or any Product repository.

Repository contracts remain authoritative:

- `../AGENT_RULES.md`;
- `../00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md`;
- `../00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md`;
- `../data/repository-evidence-policy-v2.json`;
- `../data/artifact-custody-policy-v2.json`.

Only `A1/A2/A3/B1/C/D` are source classes. `accessState`, `locatorState`, `rightsState`, `publicationState` and typed HOLDs remain independent. `HOLD` is never a source class.

## Core 15

1. Saint-Honoré
2. Paris-Brest
3. Baba au Rhum
4. Tarte au Citron / Jacques Genin
5. Opéra / Dalloyau
6. Ispahan / Pierre Hermé
7. 2000 Feuilles / Pierre Hermé
8. Mont-Blanc / Angelina
9. Religieuse
10. Kouign-Amann
11. Tarte Tatin
12. Tarte Tropézienne
13. Canelé de Bordeaux
14. Éclair
15. Galette des Rois

This list is a research sample, not a predetermined editorial verdict. Reserve candidates remain separate.

## Audit result

The corpus currently contains the governing files, generation/rights brief and all 15 dossiers. The repository authority-integrity workflow was green at audited head `1931d3fbaa10edeea415c788b8946cbe4ae39938`, including `Validate repository control plane` and deterministic corpus validators. Later commits must receive their own completed CI conclusion before being called green.

The substantive audit found **content drift**, not a broken control plane: the master claim ledger and visual ledger lagged behind newer dossier discoveries. They have now been converted to Wave 2 governing state with explicit `SUPERSEDED` decisions rather than silent history rewrites.

## Controlling findings

### Saint-Honoré

- Gouffé 1873 directly documents recognizable base + pâte-à-choux crown + small-choux architecture.
- Lacam/Charabot 1893 full object is identified. The historical Maison Chiboust / Auguste Julien / Bordeaux `Flan Suisse` account is tightly mapped to printed **p.44**; printed **p.49** is a separate technical statement.
- `1840` remains probable through the Lacam line; exact p.44/p.49 scan inspection remains open. Do not collapse Maison Chiboust, Chiboust the proprietor and Julien/Jullien into one inventor claim.

### Éclair

- The earliest **current French pastry locator** is now Charles Paul de Kock **1848**, printed p.4 col.1, with cream-filled `éclairs`; the underlying BnF/Gallica page still requires direct inspection.
- Bailleux 1856 is a verified full professional-book object; `Éclairs` is tightly located to p.74, direct page pending.
- University of Michigan identifies the 1861 New York *Vanity Fair* volume; exact 2 Feb 1861 p.50 col.1 remains to inspect.
- Gouffé 1873 directly links éclairs to `pains à la duchesse` / pâte à choux.
- `Carême invented the éclair` remains `EVIDENCE_HOLD`.

### Religieuse

- Gouffé 1873 remains the earliest **directly verified professional Religieuse recipe/form in this corpus**, and the form is multi-piece rather than the later timeless two-choux stereotype.
- Frascati 1856 is repeatedly claimed by later sources; Bailleux's 1856 provenance confirms a real Maison Frascati professional connection through M. A. Cintract.
- Targeted pre-1873 searches have not yet produced an inspectable Religieuse object. This is negative-search coverage, **not evidence of absence**.

### Paris-Brest

- Race date = **1891**, securely separated from cake date.
- Current Durand Maison = **1910**.
- La Poste + a direct interview with Louis Durand's great-grandson preserve **1909**.
- A weak local chronology gives **1911** and a Bauget signal; this remains `C / DISCOVERY` only.
- Exact cake chronology is therefore unresolved; search window is **1909–1911**. Do not invent `commission 1909 → launch 1910` without a period record.

### Opéra

- Dalloyau 1955 remains the strong canonical modern-form milestone.
- Exact Gallica page route for an older Grand Hôtel `gâteau opéra` name lead is identified: *Le Gaulois*, 18 March 1899, p.3 — `https://gallica.bnf.fr/ark:/12148/bpt6k5305801/f3.image.langFR`.
- Route resolved is not content verified; identity with Dalloyau's 1955 cake is not assumed.

### Ispahan / 2000 Feuilles

- Ispahan **1997** is cross-language official/institutional chronology; earlier rose / `Paradis` genealogy remains separate.
- 2000 Feuilles composition/signature status is directly documented by Hermé material.
- Gault&Millau's Hermé-recollection framing materially supports the **millennium renaming context**; `2000` must not be explained as literal layer count.
- A first-person Hermé author-text points to an earlier Ladurée `Millefeuille praliné` precursor, but the searchable copy is not an authorized publisher surface. Acquire legitimate book/publisher/library custody before promotion.

### Mont-Blanc

- Artusi 1891 directly documents a close chestnut-strand + whipped-cream predecessor construction, under a descriptive title rather than `Monte Bianco`.
- Farmer **1896 first edition** is a verified Internet Archive full object, with printed p.357 headed `Mont Blanc`.
- Therefore a named Mont Blanc is documented before Angelina's 1903 founding. Angelina should be treated as a famous house-signature lineage, not category inventor.
- Earlier named European `Mont-Blanc/Monte Bianco` remains open.

### Canelé

- Nouvelle-Aquitaine's institutional history rejects the convent-origin story as established fact.
- 1985 professional institutionalization / Confrérie / spelling layer is independently corroborated by professional, regional and library sources.
- Exact **1985 INPI collective-mark object** remains `LOCATOR_HOLD`; repetition of the 1985 story is not a substitute for the legal record.

### Tarte Tropézienne

- Maison creation tradition = **1955**.
- Independent film chronology places Saint-Tropez filming of *Et Dieu… créa la femme* at **3 May–7 July 1956**.
- Therefore `Bardot named it in 1955 during filming` is rejected as current wording.
- Secondary legal sources converge on 18 August 1972 for a process/patent filing; exact historical INPI patent/mark objects remain open and `brevet`, `marque`, brand and secret formula stay legally separate.

### Tarte Tatin — documentary history, myth history and technique history are separate

**Documentary fame/network**

- Exact RetroNews route: *Le Journal*, **18 Dec 1899 p.1**; direct page content still pending.
- Independent contemporaneous 1903 witness is tightly located to *Bulletin de la Société de géographie du Cher*, `1re année, 1902-1903`, pp.127–138. Full serial object identified; exact Tatin leaf pending.
- Jullemier correction: **c.1903 = described meal/event; 1915 = publication date of *Contes de Sologne***. Never call Jullemier a 1903 publication.
- Besnard 1921 target is narrowed to BnF serial `Blois et le Loir-et-Cher`, ISSN 0995-8347, cote `4-LC11-1357`; exact issue/page open.
- BnF confirms Curnonsky/Rouff `L'Orléanais` volume, 1926; exact Tatin page open.

**Accident-legend genealogy**

- Current early 1899/1903 documentary network establishes the famous Hôtel Tatin apple-tart specialty, not an accident.
- Leclercq/Delétang report no located Curnonsky passage carrying the famous accident anecdote.
- A vague clumsiness precursor is scholarly-located to *Horizons d'Argonne* **1976, p.97**; exact issue/pagination is unresolved and must not be guessed from a 1976 issue with incompatible pagination.
- A developed promotional legend is associated with the Confrérie around **1979**. The current Confrérie page itself labels the birth narrative a `légende` and states Journal officiel registration on **27 March 1979**.
- Official Journal-officiel guidance confirms that association publications **before 2 January 1985** belong to the older JORF publication stream rather than the later JOAFE stream. The exact 1979 original notice still has to be acquired. Third-party declaration/creation dates (`9 Mar` / `16 Mar`) remain non-controlling until that primary notice/statutes are obtained.

**Pre-Tatin inversion-technique genealogy**

- A 1790 professional/mastery `tourte retournée` lead exists through scholarly historical work; exact primary legal/professional object remains open.
- Urbain Dubois, *La pâtisserie d'aujourd'hui*, **2e éd., E. Dentu, 1894**, is now an identified BnF/Gallica historical full object: `https://gallica.bnf.fr/ark:/12148/bpt6k3412588h`.
- The exact `Tarte aux pêches molles` scan leaf and wording about fruit variants remain `LOCATOR_HOLD` because the Gallica viewer/API did not expose the relevant page in the current environment.
- This means the future article must distinguish `pre-existing inversion technique` from `Hôtel Tatin version/name/fame`; it is unsafe to claim the sisters invented the general upside-down-fruit-tart technique.

## Evidence boundary

- `A3` participant/institutional pages prove what that participant/institution currently states; they do not automatically prove an earlier event.
- `B1` can triangulate, expose conflicts and supply tight locators but cannot alone make a disputed historical claim quote-safe.
- **route resolved != content verified**.
- Negative search coverage never proves historical non-existence.
- OCR may navigate a verified full object but direct quotations require page/context verification.
- An unauthorized modern upload can expose an acquisition lead but cannot be promoted merely because its text is searchable.

## Rights boundary

Historical evidence strength and visual publication rights are separate. `viewable`, `downloadable`, `digitized`, `public domain in one jurisdiction`, or `OCR-found` do not automatically produce Product publication approval.

Modern maison photography remains reference-only unless licensed. Generated visuals are modern editorial specimens only and must never masquerade as historical evidence. See `00_VISUAL_ARCHIVE_AND_RIGHTS_LEDGER.md` and `00_GENERATION_REFERENCE_AND_PROMPT_BRIEF.md`.

## Current publication state

All dossiers remain `REFERENCE / PUBLICATION_HOLD` as a corpus. Individual bounded claims may be confirmed while Product transfer remains a later explicit transaction.

No Product repository has been modified by this wave.

## Current P0 acquisition queue

1. Direct page images: de Kock 1848 p.4 col.1; Bailleux 1856 p.74; Michigan *Vanity Fair* 1861 p.50 col.1; Lacam 1893 p.44/p.49; *Le Gaulois* 1899 p.3; *Le Journal* 1899 p.1.
2. Tatin: exact 1903 Bulletin page; Dubois 1894 `Tarte aux pêches molles` leaf; primary 1790 `tourte retournée` object; Jullemier 1915 page; Besnard 1921 issue/page; Curnonsky/Rouff 1926 page.
3. Tatin myth genealogy: exact *Horizons d'Argonne* 1976 p.97 with correct issue/pagination; original 1979 Confrérie prospectus/statutes and old-JORF association notice; search 1926–1975 for earlier accident motifs.
4. Paris-Brest: contemporaneous **1909–1911** advertising/menu/trade/local-directory evidence, including Durand/Bauget.
5. Religieuse: pre-1873 Frascati/Cintract/name sources and first clearly standard two-choux depiction.
6. Legal records: exact INPI canelé 1985 collective mark; Tropézienne historical patent/mark; Kouign-Amann association/mark claims.
7. 2000 Feuilles: authorized Hermé source for Ladurée `Millefeuille praliné` → `2000 Feuilles` recollection; earliest 1998–2001 catalogue/sale evidence.
8. Mont-Blanc: Farmer 1896 p.357 page-image/credit review; earlier named European forms before 1896.
9. Tropézienne: May–July 1956 contemporary Saint-Tropez press + original Bardot testimony provenance + Polish primary biographical/migration records for Micka.
10. Resolve item-level rights before any archive visual enters Product.

## Repository state

Working branch: `agent/le-canon-sucre-research-wave1-20260809`. Draft PR `#154` remains intentionally open while P0 primary-object acquisition continues.

A CI run is authoritative only after GitHub reports a completed conclusion; `queued`, `pending` or `in_progress` is not green.
