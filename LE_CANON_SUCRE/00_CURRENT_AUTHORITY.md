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

The substantive audit found **content drift**, not a broken control plane. Governing artifacts have been synchronized with explicit `SUPERSEDED` decisions rather than silent history rewrites. Every later source discovery must update the controlling layer as well as its dossier.

Repository authority CI is authoritative only after GitHub reports a completed conclusion for the current head; `queued`, `pending` or `in_progress` is not green.

## Controlling findings

### Saint-Honoré

- Gouffé 1873 directly documents recognizable base + pâte-à-choux crown + small-choux architecture.
- Lacam/Charabot 1893 full object is identified. The historical Maison Chiboust / Auguste Julien / Bordeaux `Flan Suisse` account is tightly mapped to printed **p.44**; printed **p.49** is a separate technical statement.
- `1840` remains probable through the Lacam line; exact p.44/p.49 scan inspection remains open. Do not collapse Maison Chiboust, Chiboust the proprietor and Julien/Jullien into one inventor claim.

### Éclair

- The earliest **current French pastry locator** is Charles Paul de Kock **1848**, printed p.4 col.1, with cream-filled `éclairs`; the underlying BnF/Gallica page still requires direct inspection.
- Bailleux 1856 is a verified full professional-book object; `Éclairs` is tightly located to p.74, direct page pending.
- University of Michigan identifies the 1861 New York *Vanity Fair* volume; exact 2 Feb 1861 p.50 col.1 remains to inspect.
- Gouffé 1873 directly links éclairs to `pains à la duchesse` / pâte à choux.
- `Carême invented the éclair` remains `EVIDENCE_HOLD`.

### Religieuse

- The Saint Petersburg Polytechnic University Electronic Library identifies **Bailleux, *Le Pâtissier moderne*, Paris 1860**, and its institutional machine-readable table of contents lists a dedicated **`Religieuse`** entry inside Chapter V `Gâteaux garnis`.
- Therefore the old corpus statement `Gouffé 1873 = earliest directly verified professional named Religieuse` is **SUPERSEDED**.
- Correct current distinction:
  - **1860 Bailleux** = earliest directly verified **professional named entry/section** in this corpus;
  - **1873 Gouffé** = earliest exact **recipe/form pages directly inspected** in this corpus.
- The 1860 scan is access-restricted for anonymous Internet users, so exact Bailleux page/recipe/form remains `LOCATOR_HOLD / CONTENT_HOLD`; no access controls are bypassed.
- Rare-book bibliography identifies the 1860 book as a **third edition, revised/corrected/enlarged**, while Christie's verifies the first edition as **1856**. It is now a P0 edition-history question whether `Religieuse` was already present in 1856 or added before 1860.
- Frascati 1856 remains a later origin tradition, although Bailleux's genuine first-edition provenance connects him professionally to M. A. Cintract / Maison Frascati. Do not infer the 1856 recipe from that provenance.
- Modern retellings conflict about the alleged 1856 geometry. Do not reconstruct it as historical fact.

### Baba au Rhum / Savarin

- The same SPbPU institutional 1860 Bailleux record exposes professional named entries including **`Petits Savarins`, `Babas parisiens`, `Savarin` and `Baba`** in the openly visible table of contents.
- Therefore the professional named-form chronology does not begin with Gouffé 1873: **Baba/Savarin are directly verified as named professional entries in the 1860 edition**.
- The 1860 scan itself is access-restricted; exact recipe wording, form and soaking liquid remain `ACCESS/LOCATOR_HOLD`. Presence of `Baba` in the TOC does **not** prove rum use.
- Gouffé 1873 remains the earliest **exact rum-specific page directly inspected in the current corpus** through `baba moderne glacé au rhum`, while separately documenting savarin.
- Whether Bailleux's **1856 first edition** already contains the same Baba/Savarin entries remains an edition-delta question.
- Current Stohrer house history attributes baba to Nicolas Stohrer but itself preserves divergent Tokay/Malaga stories and treats rum as later. This participant inconsistency is a reason for caution, not a defect to smooth over.
- Do not write `rum baba first appeared in 1873`; 1873 is only the current earliest exact inspected rum-specific page.

### Tarte au Citron / Jacques Genin

- Genin's **2009 citron-basilic** version is strongly documented by later French journalism and should be treated as a modern authored reinterpretation, not the invention of tarte au citron as a genre.
- A 2026 Relais Desserts professional historical synthesis remains an explicit **falsification/locator source**: it challenges a timeless purely French modern-tart genealogy and points toward a wider English/transnational lemon-cream history. The synthesis itself is not primary origin proof.
- **Eliza Acton 1845 materially changes the governing boundary.** Wellcome/University of Leeds identifies a digitized 1845 *Modern Cookery* object with 679 images and a Public Domain Mark; the same Leeds scan is preserved on Wikimedia Commons. Separately, a transcription explicitly based on the 1845 first edition maps `Common Lemon Tartlets` to printed **p.431** and `Store Mixture for Lemon Tartlets` to **p.434**.
- The mapped Acton text describes a recognizable pastry-shell + lemon-filling architecture: thin puff-paste shells receive an egg/sugar/butter/lemon filling and are baked; the store mixture is cooked until cream-thick before later filling and baking in thin puff-paste shells.
- Evidence remains deliberately split: **1845 object identity and rights lane are institutionally verified; recipe text/page mapping is strong; the exact original p.431/p.434 facsimile leaves have not yet been directly visually inspected.** Therefore `PAGE_IMAGE_HOLD` remains for verbatim quotation/facsimile Product use.
- Additional bounded nodes remain useful but are no longer the earliest architecture evidence:
  - **1855 Webster** = directly readable `Lemon Cream`, served as a cream rather than shown in a tart shell;
  - **1870 Jeanes** = professional *Gunter's Modern Confectioner* TOC directly lists `Lemon Cheese Cakes`, p.227; exact recipe/form remains `CONTENT_HOLD`;
  - **1877 Charles Gérard** = direct French-language/Alsatian inventory witness listing `la tourte au citron`; nomenclature, not recipe architecture.
- Dumas's **1873** *Grand dictionnaire de cuisine* is directly identified as a full historical object. Targeted direct searches have not yet surfaced a modern-style lemon-tart entry; this is **negative search coverage only**, never proof of absence.
- The high-value unresolved question is now specifically **French codification and later convergence**: when comparable shell + lemon filling appears in directly inspectable French professional recipes; when meringue enters; when the familiar pâte-sucrée + smooth/emulsified lemon-cream architecture becomes established.
- Prohibited shortcuts include `Jacques Genin invented tarte au citron`, `Acton invented the modern tart`, `Gérard 1877 is the modern tarte au citron`, and any simple national-invention claim unsupported by the transmission chain.

### Paris-Brest

- Race date = **1891**, securely separated from cake date.
- Current Durand Maison = **1910**.
- La Poste + a direct interview with Louis Durand's great-grandson preserve **1909**.
- A weak local chronology gives **1911** and a Bauget signal; this remains `C / DISCOVERY` only.
- Exact cake chronology is unresolved; search window is **1909–1911**. Do not invent `commission 1909 → launch 1910` without a period record.

### Opéra

- Dalloyau 1955 remains the strong canonical modern-form milestone.
- Exact Gallica page route for an older Grand Hôtel `gâteau opéra` name lead is identified: *Le Gaulois*, 18 March 1899, p.3 — `https://gallica.bnf.fr/ark:/12148/bpt6k5305801/f3.image.langFR`.
- Route resolved is not content verified; identity with Dalloyau's 1955 cake is not assumed.

### Ispahan / 2000 Feuilles

- Ispahan **1997** is cross-language official/institutional chronology; earlier rose / `Paradis` genealogy remains separate.
- 2000 Feuilles composition/signature status is directly documented by Hermé material.
- Gault&Millau's Hermé-recollection framing materially supports the **millennium renaming context**; `2000` must not be explained as literal layer count.
- A first-person Hermé author-text points to an earlier Ladurée `Millefeuille praliné` precursor. The relevant authorized editions are now cleanly identified through Pierre Hermé's own Maison: *Toutes les saveurs de la vie* (Buchet-Chastel, 2022) and *Dictionnaire amoureux de la pâtisserie* (Plon, 2025).
- Exact precursor wording/page still requires authorized publisher/library custody. Searchable user-upload copies remain locator leads only.

### Mont-Blanc

- Artusi 1891 directly documents a close chestnut-strand + whipped-cream predecessor construction, under a descriptive title rather than `Monte Bianco`.
- Farmer **1896 first edition** is a verified Internet Archive full object, with printed p.357 headed `Mont Blanc`.
- Therefore a named Mont Blanc is documented before Angelina's 1903 founding. Angelina should be treated as a famous house-signature lineage, not category inventor.
- Earlier named European `Mont-Blanc/Monte Bianco` remains open.

### Kouign-Amann

- Douarnenez official/regional heritage preserves Yves-René Scordia / c.1860 as the strong local creation tradition.
- Independent *Le Monde* reporting in 2001, while describing the Douarnenez association founder's historical research, explicitly notes the absence of an incontestable written trace for the reconstruction then being advanced.
- The same 2001 report independently states that **two years earlier** eighteen of Douarnenez's twenty-two pâtissiers had formed an association for the `véritable kouign-amann de Douarnenez` and **had filed the mark with INPI**. Thus the bounded existence of association/protection activity around **1999** is no longer participant-only.
- A current artisan/association participant supplies the more precise **November 1999** association date and **15 December 1999** filing date. Those exact dates, plus mark number, historical holder/applicant wording, classes, publication/registration and status, remain `LOCATOR_HOLD` until the INPI register object is acquired.
- Do not silently reconcile the 2001 count of eighteen pâtissiers with the current artisan page's seventeen-member account; preserve the source-level variance.
- The independent modern-protection evidence does not strengthen the unclosed **c.1860 invention event**.

### Canelé

- Nouvelle-Aquitaine's institutional history rejects the convent-origin story as established fact.
- Professional Gironde pastry testimony says that in 1985 the departmental pastry organization created the Confrérie, removed one `n` from `cannelé`, and filed the one-`n` name with INPI; regional/library sources independently report the collective-mark step.
- INPI's own historical coverage includes French marks, valid or expired, from **1976**, and BOPI pages for French marks from **1982**. A genuine 1985 French filing is therefore within the official historical search horizon.
- Exact mark number, historical holder/deposant, filing/publication dates, classes and BOPI page remain `LOCATOR_HOLD`.
- Holder search must include the historical professional-union line, not only the modern Confrérie title; current owner/predecessor hypotheses remain leads until the register object is found.

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
- 1923 *Livret d'or* Tatin recipe is tightly located to printed **p.85**; direct page-context review remains open.
- BnF confirms Curnonsky/Rouff `L'Orléanais` volume, 1926; exact Tatin page open.
- Exact RetroNews route is identified for *Paris-Soir*, **25 Aug 1929 p.5**, plus *La Dépêche du Berry*, **11 Sep 1931 p.2**.

**Accident-legend genealogy**

- Current early 1899/1903 documentary network establishes the famous Hôtel Tatin apple-tart specialty, not an accident.
- Leclercq/Delétang report no located Curnonsky passage carrying the famous accident anecdote.
- Preserve the scholarly citation exactly as ***Horizons d'Argonne*, `n°30 à 39, 1976, p.97`** for a vague clumsiness precursor; original page/bound-run mapping remains open. Do not silently rewrite it to `n°30–31`.
- A developed promotional legend is associated with the Confrérie around **1979**. The current Confrérie page itself labels the birth narrative a `légende` and states Journal officiel publication/registration on **27 March 1979**.
- Official Journal-officiel guidance confirms that association publications **before 2 January 1985** belong to the older JORF stream rather than later JOAFE. The exact 1979 original notice/prospectus remains open; third-party March creation/declaration dates remain non-controlling.

**Pre-Tatin inversion-technique genealogy**

- A 1790 professional/mastery `tourte retournée` lead exists through scholarly historical work; exact primary legal/professional object remains open.
- Urbain Dubois, *La pâtisserie d'aujourd'hui*, **2e éd., E. Dentu, 1894**, is an identified BnF/Gallica historical full object: `https://gallica.bnf.fr/ark:/12148/bpt6k3412588h`.
- The exact `Tarte aux pêches molles` scan leaf and wording about fruit variants remain `LOCATOR_HOLD` because the Gallica viewer/API did not expose the relevant page in the current environment.
- The future article must distinguish `pre-existing inversion technique` from `Hôtel Tatin version/name/fame`; it is unsafe to claim the sisters invented the general upside-down-fruit-tart technique.

## Evidence boundary

- `A3` participant/institutional pages prove what that participant/institution currently states; they do not automatically prove an earlier event.
- `B1` can triangulate, expose conflicts and supply tight locators but cannot alone make a disputed historical claim quote-safe.
- **route resolved != content verified**.
- A verified TOC/structural entry is stronger than vague discovery but does not substitute for an inspected recipe page.
- A transcription explicitly mapped to a historical edition can close a bounded text/locator layer when corroborated by institutional object identity, but it does not become an inspected facsimile page. Acton 1845 p.431/p.434 currently follows this rule.
- Negative search coverage never proves historical non-existence and must be revised when a new object is found.
- OCR may navigate a verified full object but direct quotations require page/context verification.
- An unauthorized modern upload can expose an acquisition lead but cannot be promoted merely because its text is searchable.

## Rights boundary

Historical evidence strength and visual publication rights are separate. `viewable`, `downloadable`, `digitized`, `public domain in one jurisdiction`, or `OCR-found` do not automatically produce Product publication approval.

Acton 1845 has an unusually strong visual-rights lane because Wellcome marks the digitized object with a Public Domain Mark and supplies a credit line, but Product facsimile use still requires exact-leaf inspection, credit capture and durable byte provenance.

Modern maison photography remains reference-only unless licensed. Generated visuals are modern editorial specimens only and must never masquerade as historical evidence. See `00_VISUAL_ARCHIVE_AND_RIGHTS_LEDGER.md` and `00_GENERATION_REFERENCE_AND_PROMPT_BRIEF.md`.

## Current publication state

All dossiers remain `REFERENCE / PUBLICATION_HOLD` as a corpus. Individual bounded claims may be confirmed while Product transfer remains a later explicit transaction.

No Product repository has been modified by this wave.

## Current P0 acquisition queue

1. Direct page images: de Kock 1848 p.4 col.1; Bailleux 1856 Éclairs p.74; Michigan *Vanity Fair* 1861 p.50 col.1; Lacam 1893 p.44/p.49; *Le Gaulois* 1899 p.3; *Le Journal* 1899 p.1.
2. Bailleux edition history: lawfully acquire **1860 Religieuse/Baba/Savarin pages** and determine whether the **1856 first edition** already contains the named Religieuse/Baba/Savarin entries.
3. Baba: continue pre-1873 rum-specific search; distinguish first named Baba/Savarin from first directly inspectable rum-soaked formulation.
4. Tarte au Citron: pin and visually inspect Acton 1845 printed p.431/p.434 facsimile leaves; direct Genin 2009 participant source; complete bounded Dumas 1873 lemon-entry review; inspect Jeanes 1870 p.227; acquire the earliest comparable **French professional recipe architecture** and later meringue/emulsified-cream transitions.
5. Tatin: exact 1903 Bulletin page; Dubois 1894 `Tarte aux pêches molles` leaf; primary 1790 `tourte retournée` object; Jullemier 1915 page; Besnard 1921 issue/page; Curnonsky/Rouff 1926 page; 1923 p.85 / 1929 p.5 / 1931 p.2 direct page reviews.
6. Tatin myth genealogy: original *Horizons d'Argonne* 1976 p.97 under the exact `n°30 à 39` citation; original 1979 Confrérie prospectus/statutes and old-JORF notice; search 1926–1975 for earlier accident motifs.
7. Paris-Brest: contemporaneous **1909–1911** advertising/menu/trade/local-directory evidence, including Durand/Bauget.
8. Legal records: exact INPI canelé 1985 collective mark; Tropézienne historical patent/mark; exact `Véritable Kouign-Amann de Douarnenez` register object to test the participant-reported 15 Dec 1999 date and capture holder/number/classes/publication/status.
9. 2000 Feuilles: authorized Hermé page for Ladurée `Millefeuille praliné` → `2000 Feuilles` recollection; earliest 1998–2001 catalogue/sale evidence.
10. Mont-Blanc: Farmer 1896 p.357 page-image/credit review; earlier named European forms before 1896.
11. Tropézienne: May–July 1956 contemporary Saint-Tropez press + original Bardot testimony provenance + Polish primary biographical/migration records for Micka.
12. Resolve item-level rights before any archive visual enters Product.

## Repository state

Working branch: `agent/le-canon-sucre-research-wave1-20260809`. Draft PR `#154` remains intentionally open while P0 primary-object acquisition continues.

A CI run is authoritative only after GitHub reports a completed conclusion; `queued`, `pending` or `in_progress` is not green.