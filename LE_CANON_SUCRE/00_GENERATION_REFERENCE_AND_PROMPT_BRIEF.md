# LE CANON SUCRÉ — generation reference & prompt brief

**Status:** `VISUAL BRIEF / REFERENCE-ONLY / NO PRODUCT WRITE`  
**Purpose:** define what should be generated for the future Canon experience and what must remain authentic archive material.

## 0. Hard boundary: generated ≠ historical evidence

Generation is allowed for **contemporary editorial food imagery** only.

Never generate or reconstruct as if authentic:

- historical newspaper pages;
- old menus or advertisements;
- recipe-book facsimiles;
- handwritten recipes/letters;
- INPI/trademark/patent records;
- period shop photographs;
- portraits presented as archival photographs;
- fake stamps, signatures, dates, BnF/Gallica marks or institution labels.

Historical-document slots on `/canon/` must use real acquired objects after item-level rights review. If no cleared document exists, show no document rather than an AI imitation.

## 1. Visual DNA

Target feeling:

**Musée des Arts Décoratifs × haute pâtisserie × French editorial still life.**

Not restaurant advertising. Not fantasy luxury. Not a wedding-dessert table.

Core visual rules:

- dark graphite / near-black museum space;
- black stone, charcoal plaster or restrained mineral plinths;
- one controlled warm old-gold key light;
- very subtle cool rim light for separation;
- deep clean shadows, visible material texture, restrained highlights;
- large negative space;
- precise object geometry and physically plausible pastry texture;
- no text baked into image;
- no logos;
- no decorative typography;
- no excessive edible gold leaf;
- no floating ingredients;
- no theatrical smoke;
- no flowers unless a dessert structurally requires a floral ingredient cue;
- no cutlery/hands unless a later article-specific brief explicitly asks for them.

The images are backgrounds/art-directed editorial objects. All titles, metadata and CTA remain real HTML.

## 2. Reference links — use for form, restraint and lighting only

These are **references, not reusable production assets unless rights are separately cleared**.

### Official pastry/form references

**Opéra — Dalloyau**  
https://www.dalloyau.fr/patisseries/658-opera-loriginal-6-a-50-personnes.html

Use for: strict low rectangular geometry, coffee/chocolate/Joconde layer logic.  
Do not clone the exact proprietary photograph or branded presentation.

**Pierre Hermé — signature collection / Ispahan + 2000 Feuilles context**  
https://www.pierreherme.com/fr/patisseries/patisseries-signatures.html

**2000 Feuilles — current official form/composition**  
https://www.pierreherme.com/fr/2000-feuilles-entremets.html

**Pierre Hermé — visual/editorial philosophy reference**  
https://www.pierreherme.com/fr/art-de-la-patisserie

Use for: disciplined form, texture contrast, minimal decorative artifice. Do not duplicate a house product photograph pixel-for-pixel.

**Mont-Blanc — Angelina current signature reference**  
https://www.angelina-paris.fr/notre-savoir-faire

Use for: dome/mountain silhouette, chestnut vermicelli language.  
Research dossier shows the category predates Angelina; this link is a modern house-form reference only.

**Saint-Honoré — real historical architecture reference, Gouffé 1873**  
https://fr.wikisource.org/wiki/Page%3AGouff%C3%A9_-_Le_Livre_de_P%C3%A2tisserie%2C_1873.djvu/278

Use to understand that base + choux crown + small choux is historically documented. Do not turn the generated gateway into a sepia reconstruction.

**Galette des Rois — modern ritual context**  
https://www.elysee.fr/emmanuel-macron/2026/01/05/remise-de-la-galette-de-lepiphanie-1

Use for category context only. The generated galette should be a generic canonical round laminated galette, not a copy of a named chef's proprietary surface motif.

### Composition / lighting mood references

**Mori Yoshida / museum-pedestal pastry presentation**  
https://www.ufu-sweets.jp/patisserie/2412_mori-yoshida_open/

Use for: controlled negative space, object separation, tiered mineral display feeling.

**La Fabrique du Pâtissier**  
https://www.lafabriquedupatissier.fr/

Use for: dark stands, restrained black-background pastry presentation.

**Four Seasons Paris galette editorial**  
https://press.fourseasons.com/fr/paris/hotel-news/2024/king-cake-2

Use for: isolated round geometry and clean surface reading, not for copying the exact chef design.

**La Mercerie**  
https://www.lamercerieny.com/

Use only for low-key dramatic lighting reference. Avoid its more romantic/decorative styling in the final Canon system.

## 3. Mandatory generated set

### G01 — HOME GATEWAY / DESKTOP

**Purpose:** one wide editorial gateway after the four main school directions.

**Master composition:** approximately `3.5:1–3.8:1`; generate with enough source resolution for a production crop around **1600 × 440 px**.

**Layout contract:**

- left **38–42%**: intentionally quiet dark negative space for HTML text;
- right **58–62%**: exactly five pastry silhouettes;
- no object crosses the text-safe left area;
- safe dark margin at all outer edges;
- objects read clearly even at ~400 px block height.

**Five objects, left-to-right inside the object zone:**

1. Saint-Honoré — vertical/choux crown silhouette;
2. Opéra — low precise rectangular slab;
3. Ispahan — refined round macaron/raspberry/rose silhouette;
4. Mont-Blanc — chestnut-vermicelli dome/mountain;
5. Galette des Rois — larger shallow laminated round disk.

The rhythm matters more than literal scale: **tower → rectangle → circle → dome → disk**.

**Prompt — G01**

```text
Ultra-premium French pâtisserie editorial still life for a digital museum exhibition, extremely wide panoramic composition, dark graphite museum interior and black mineral stone plinth, large intentional negative space across the left 40 percent for real HTML typography, all pastry objects arranged only across the right 60 percent. Exactly five distinct canonical pastry silhouettes: a refined Saint-Honoré with a clear pastry base, choux crown and small caramelized choux; a low geometrically precise rectangular Opéra with elegant visible coffee-chocolate layers; a restrained Ispahan-inspired rose-raspberry macaron form with natural raspberry geometry and only a subtle rose cue; a classic Mont-Blanc dome with fine chestnut vermicelli texture; a broad shallow traditional galette des rois with crisp laminated puff pastry and restrained scored surface. Museum-display spacing, each silhouette separated by air, no buffet feeling. One soft old-gold directional key light, very subtle cool rim light, deep clean shadows, realistic pastry textures, premium French editorial realism, understated film grain, high dynamic range without glossy advertising excess, black and charcoal palette with muted warm pastry tones. No typography, no logo, no labels, no plates with branding, no human hands, no cutlery, no floating ingredients, no flowers, no smoke, no excessive gold leaf, no fantasy props. The scene must feel curated, architectural and quiet, not festive and not restaurant-commercial. Preserve dark crop-safe borders and clean negative space.
```

### G02 — HOME GATEWAY / MOBILE ART-DIRECTED VERSION

**Master composition:** `4:5` preferred; acceptable `5:6`. Target source at least **1200 × 1500 px**.

Do **not** crop G01 mechanically. This is a separate composition.

Use only three hero forms to avoid clutter:

- Saint-Honoré;
- Ispahan;
- Mont-Blanc.

Upper **35–40%** should stay quiet enough for HTML label/title/subtitle. Objects occupy lower-middle area with strong depth separation.

**Prompt — G02**

```text
Vertical art-directed companion image to a premium French pâtisserie museum gateway, 4:5 composition, near-black graphite gallery space, upper 38 percent intentionally quiet and dark for real HTML typography, three sculptural pastry objects only in the lower-middle exhibition zone: Saint-Honoré with clearly readable choux architecture, an elegant Ispahan-inspired round rose-raspberry macaron form, and a fine-textured Mont-Blanc chestnut dome. Separate mineral plinth heights, large negative space, subtle depth, one restrained old-gold key light with a faint cool edge light, deep cinematic shadows, realistic pastry texture, French editorial still-life photography, quiet museum atmosphere, no text, no logo, no floating elements, no excessive decoration, no gold-leaf cliché, no flowers as props, no utensils, no hands, no restaurant-table styling. Keep all edges crop-safe.
```

### G03 — `/canon/` HERO / DIGITAL EXHIBITION

**Format:** `16:9`, source ideally **1920 × 1080** or larger.

This should not be the same composition as G01. It is the entrance hall of the exhibition.

Five forms may appear, but each should feel like an individual collection object on a separate subtle plinth. More depth and architectural darkness; central/upper text-safe field for HTML.

**Prompt — G03**

```text
Entrance image for a digital museum exhibition about the canon of French pâtisserie, 16:9, monumental but restrained dark gallery, five pastry forms displayed like collected design objects on separate low black-stone plinths with generous spacing: Saint-Honoré, Opéra, an Ispahan-inspired rose-raspberry macaron form, Mont-Blanc, and galette des rois. Deep architectural perspective, large calm text-safe area through the center-upper field, restrained warm museum key lights with subtle cool separation, graphite, black mineral surfaces, muted old gold only in illumination, realistic edible material, precise geometry, soft film grain, editorial photographic realism. No words, no labels, no brand marks, no velvet ropes, no people, no plates with logos, no fake historical documents, no excessive gold, no dramatic smoke, no surrealism. The feeling is a curated design collection rather than a dessert buffet.
```

### G04 — ACT I / ARCHITECTURE

Objects:

`Saint-Honoré · Paris-Brest · Religieuse · Éclair · Opéra`

Visual temperature: colder graphite / mineral / slight metal cue.

Important: the generated Religieuse is a **modern canonical specimen**, while the article can separately show the real Gouffé 1873 historical form. Do not fake the 1873 drawing photographically.

**Prompt — G04**

```text
Curated French pâtisserie architecture study, 16:9 editorial museum still life, five distinct specimens with strong silhouette spacing: Saint-Honoré, Paris-Brest wheel, modern two-tier Religieuse, elongated Éclair, low rectangular Opéra. Cool graphite and black mineral exhibition surfaces, subtle brushed-metal undertone, restrained warm highlights only on pastry edges, quiet museum lighting, precise geometry, highly realistic pâte à choux, laminated and glazed textures, no decorative buffet clutter, no plates with branding, no text, no labels, no chef hands, no floating crumbs, no excessive gold leaf. Each dessert must read as a different architectural typology.
```

### G05 — ACT II / MAISONS & SIGNATURES

Objects:

`Baba au Rhum · Tarte au Citron · Ispahan · 2000 Feuilles · Mont-Blanc`

Visual temperature: warmer old-gold key, still dark and restrained.

Do not copy proprietary house photographs exactly. Preserve recognizable category/signature geometry while changing staging, camera, background and presentation.

**Prompt — G05**

```text
French haute-pâtisserie signatures presented as five museum collection objects, 16:9 dark editorial still life: a restrained baba au rhum, a clean modern tarte au citron, an Ispahan-inspired rose-raspberry macaron form, a tall precisely layered praline mille-feuille inspired by the 2000 Feuilles texture concept, and a classic Mont-Blanc chestnut-vermicelli dome. Warm old-gold directional light slightly softer than the Architecture chapter, deep charcoal background, black stone plinths, luxurious texture without ostentation, generous negative space, realistic creams, laminated pastry and fruit, subtle cool rim light, premium French magazine photography. No text, no logos, no exact recreation of any branded product photograph, no gold-leaf overload, no flowers as set decoration, no hands, no cutlery, no smoke.
```

### G06 — ACT III / TERRITOIRE & RITUEL

Objects:

`Kouign-Amann · Tarte Tatin · Tarte Tropézienne · Canelé · Galette des Rois`

Visual temperature/materials: dark stone with restrained natural wood/craft note; slightly more tactile, never rustic-kitsch.

**Prompt — G06**

```text
French regional pâtisserie and ritual as a sophisticated museum still life, 16:9, five distinct objects with generous spacing: deeply laminated caramelized kouign-amann, inverted apple tarte Tatin with controlled caramelized fruit geometry, restrained brioche-and-cream Tarte Tropézienne, small deeply baked fluted canelé, and a broad classic galette des rois with crisp laminated layers and subtle scored top. Dark charcoal stone with one understated natural craft surface, elegant museum lighting, old-gold warmth from baked pastry rather than decorative gold, highly realistic texture, sophisticated editorial photography, large negative space, no folkloric props, no Provençal souvenir styling, no flags, no fake vintage signs, no brand logos, no text, no utensils, no hands, no excessive crumbs or flour clouds.
```

## 4. Optional specimen system — G07–G21

If existing article imagery is inconsistent, generate one standardized editorial specimen per Canon object.

**Recommended format:** `4:5`, source `1200 × 1500` or larger.

Common contract:

- one pastry only;
- 10–14% empty margin around silhouette;
- three-quarter view or slight eye-level depending on form;
- same graphite/mineral background family;
- same light direction across the set;
- realistic scale;
- no text/logos;
- do not reproduce a proprietary current maison photograph exactly;
- article can pair the generated modern specimen with a real historical facsimile where rights permit.

Suggested IDs:

- `G07_SAINT_HONORE`
- `G08_PARIS_BREST`
- `G09_BABA`
- `G10_TARTE_CITRON`
- `G11_OPERA`
- `G12_ISPAHAN`
- `G13_2000_FEUILLES`
- `G14_MONT_BLANC`
- `G15_RELIGIEUSE`
- `G16_KOUIGN_AMANN`
- `G17_TATIN`
- `G18_TROPEZIENNE`
- `G19_CANELE`
- `G20_ECLAIR`
- `G21_GALETTE`

## 5. Universal negative prompt

```text
text, letters, captions, logo, watermark, menu, fake newspaper, fake archive, fake vintage document, fake handwriting, fake stamp, fake museum label, brand packaging, excessive edible gold leaf, gold flakes everywhere, glitter, luxury cliché, baroque ornament, rococo props, flowers used as unrelated decoration, floating ingredients, levitating pastry, smoke, fog machine, sparks, magical glow, neon, cyberpunk, oversaturated colors, glossy restaurant commercial look, buffet, crowded table, duplicate pastries, extra desserts, cutlery, hands, people, chef, plates with logos, deformed pastry geometry, melted impossible cream, plastic texture, waxy fruit, impossible shadows, mirrored symmetry, tilted horizon, cropped pastry, busy background
```

## 6. Consistency contract for all generated images

Before accepting an image, check:

1. correct number of pastries;
2. recognizable geometry for every named form;
3. no invented text or branding;
4. no historical fakery;
5. no gold-leaf AI cliché;
6. no unintended extra objects;
7. no impossible pastry structure;
8. dark negative-space zone remains usable for HTML;
9. all essential objects survive intended desktop/mobile crop;
10. visual language matches the other Canon images.

Reject a visually beautiful generation if it breaks collection consistency.

## 7. Proposed production filenames — planning only

Research does not write Product assets. If/when Product transfer is explicitly authorized, a clean naming family could be:

```text
canon-gateway-desktop.webp
canon-gateway-mobile.webp
canon-hero.webp
canon-act-01-architecture.webp
canon-act-02-signatures.webp
canon-act-03-territory-ritual.webp
canon-01-saint-honore.webp
...
canon-15-galette.webp
```

Final Product paths, codecs, sizes and responsive variants must be decided in the Product repository at transfer time.

## 8. What should NOT be generated because real objects are being acquired

Do not spend image-generation credits on these. Research should obtain the authentic item instead:

- *Le Gaulois*, 18 March 1899, p. 3 — reported Grand Hôtel `gâteau opéra`; exact Gallica route already identified: https://gallica.bnf.fr/ark:/12148/bpt6k5305801/f3.image.langFR
- *Le Journal*, 18 December 1899, p. 1 — early Tatin route identified: https://www.retronews.fr/journal/le-journal/18-decembre-1899/129/238489/1
- Fannie Farmer, 1896, printed p. 357 `Mont Blanc` — primary full object: https://archive.org/details/bostoncookingsc00collgoog
- Bailleux, 1856, printed p. 74 `Éclairs` — primary book identified: https://books.google.com/books/about/Le_Patissier_moderne_ou_trait%C3%A9_%C3%A9l%C3%A9men.html?id=BljqJaHy8eoC
- Gouffé 1873 Saint-Honoré / Religieuse / Éclair / Baba pages — use the real facsimiles already in the visual ledger;
- Lacam/Charabot 1893 Saint-Honoré history — inspect the real identified volume/page rather than fabricating a period page;
- INPI canelé/Tropézienne/Kouign-Amann records — acquire actual legal records;
- Bardot/Micka period photographs or letters — acquire authentic archive objects and rights.

## 9. Acceptance philosophy

The generated layer should supply **modern visual coherence**. The archive layer supplies **historical truth**.

The strongest Canon page will deliberately let those two layers look different: clean contemporary dark editorial specimens beside visibly real historical paper/scans with proper source captions. Do not blur the boundary by asking AI to manufacture “convincing old evidence.”
