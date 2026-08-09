# LE CANON SUCRÉ — multilingual query and terminology map

**Status:** `ACTIVE / WAVE 2 AUDITED`  
**Rule:** historical spelling, semantic drift, owner-name drift and date-vs-event drift are first-class targets. Modern names are never assumed to be earliest names.

## Français — primary search language

| Object | Core historical/query variants |
|---|---|
| Saint-Honoré | `Saint-Honoré`, `St-Honoré`, `gâteau Saint-Honoré`, `Chiboust`, `Maison Chiboust`, `crème Chiboust`, `Auguste Julien`, `Jullien`, `Flan Suisse`, `Bordeaux`, `1840`, `1847`, `1863`, `Lacam p.44`, `Lacam p.49` |
| Paris-Brest | `Paris-Brest`, `Paris Brest`, `Paris-Brest-Paris`, `Louis Durand`, `Durand pâtissier`, `Maisons-Laffitte`, `Longueil`, `Bauget`, `Gerbet`, `roue`, `praliné`, `1909`, `1910`, `1911`, `annuaire`, `réclame`, `menu`, `pâtisserie` |
| Baba | `baba`, `baba au rhum`, `baba moderne`, `baba polonais`, `kouglof`, `kougelhopf`, `Stanislas`, `Stohrer`, `Tokay`, `Malaga`, `savarin` |
| Tarte citron | `tarte au citron`, `tourte au citron`, `crème citron`, `citron vert`, `basilic`, `Jacques Genin`, `crémeux`, `émulsion`, `meringué`, `2009`, `Acton 1845`, `Common Lemon Tartlets`, `Store Mixture for Lemon Tartlets`, `rdz664vd`, `z22c8gru`, `Gunter's Modern Confectioner`, `Lemon Cheese Cakes`, `Jeanes 227` |
| Opéra | `Opéra`, `gâteau opéra`, `entremets opéra`, `Cyriaque Gavillon`, `Andrée Gavillon`, `Dalloyau`, `1955`, `Grand Hôtel`, `Le Gaulois`, `18 mars 1899` |
| Ispahan | `Ispahan`, `Paradis`, `rose`, `framboise`, `litchi`, `letchi`, `Pierre Hermé`, `Fauchon`, `Ladurée`, `1997` |
| 2000 Feuilles | `2000 Feuilles`, `Deux Mille Feuilles`, `mille-feuille praliné`, `Millefeuille praliné`, `Ladurée`, `praliné feuilleté`, `crêpes dentelles`, `millénaire`, `an 2000`, `catalogue Pierre Hermé`, `1998`, `1999`, `2000`, `2001` |
| Mont-Blanc | `Mont-Blanc`, `Mont Blanc`, `Monte Bianco`, `marrons`, `vermicelles de marrons`, `châtaignes`, `panna montata`, `Rumpelmayer`, `Angelina`, `1891`, `1896`, `1903` |
| Religieuse | `religieuse`, `flan à la religieuse`, `religieuse au café`, `religieuse au chocolat`, `Frascati`, `Café Frascati`, `Maison Frascati`, `Cintract`, `M. A. Cintract`, `Signor Frascati`, `pains à la duchesse`, `choux superposés`, `1856`, `1860`, `1873` |
| Kouign-Amann | `kouign-amann`, `kouign amann`, `Douarnenez`, `Scordia`, `Yves-René Scordia`, `1860`, `beurre`, `sucre`, `Association du véritable Kouign-Amann`, `marque`, `1999` |
| Tatin | `tarte Tatin`, `tarte des demoiselles Tatin`, `Mlle Tatin`, `Fanny Tatin`, `Stéphanie Tatin`, `Caroline Tatin`, `Lamotte-Beuvron`, `Pin d'Or`, `Hôtel Tatin`, `Gabriel Hanotaux`, `Le Journal 18 décembre 1899`, `Société de géographie du Cher 1903`, `Jullemier 1915`, `Contes de Sologne`, `Paul Besnard`, `Blois et le Loir-et-Cher`, `4-LC11-1357`, `Livret d'or 1923 p.85`, `Curnonsky`, `L'Orléanais 1926`, `Paris-Soir 25 août 1929 p.5`, `Horizons d'Argonne 1976 p.97`, `n°30 à 39`, `Lichonneux`, `0413000987`, `W413000745`, `prospectus 1979`, `tourte retournée 1790`, `Urbain Dubois 1894`, `Tarte aux pêches molles` |
| Tropézienne | `Tarte Tropézienne`, `Alexandre Micka`, `Aleksander Micka`, `Saint-Tropez`, `Brigitte Bardot`, `Et Dieu… créa la femme`, `mai 1956`, `juin 1956`, `juillet 1956`, `brevet 1972`, `18 août 1972`, `INPI`, `BOPI` |
| Canelé | `canelé`, `cannelé`, `canaule`, `canaulier`, `canauliers`, `Bordeaux`, `Annonciades`, `Confrérie du Canelé`, `Union départementale des pâtissiers de la Gironde`, `Syndicat des patrons pâtissiers de Bordeaux et de la Gironde`, `781846068`, `Daniel Antoine`, `Marquet`, `24 mars 1985`, `1985`, `marque collective`, `INPI`, `BOPI`, `moule cuivre`, `cire d'abeille` |
| Éclair | `éclair`, `eclair`, `Charles Paul de Kock`, `L'Atelier de demoiselles`, `1848`, `p.4 col.1`, `pains à la duchesse`, `pain à la duchesse`, `cartouche`, `Bailleux`, `Le Pâtissier moderne`, `1856 p.74`, `Carême`, `pâte à choux`, `Vanity Fair 1861`, `1864`, `Gouffé 1873` |
| Galette des Rois | `galette des rois`, `gâteau des rois`, `brioche des rois`, `fève`, `frangipane`, `Pithiviers`, `Épiphanie`, `galette républicaine`, `Élysée 1975` |

## Query bundles for current P0 acquisition

### Éclair 1848 / 1856 / 1861

Use exact object-oriented queries rather than generic history pages:

- `"L'Atelier de demoiselles" éclairs 1848`
- `"Charles Paul de Kock" éclairs p. 4`
- `"Le Pâtissier moderne" Éclairs 74 Bailleux`
- `"The Primpenny Family" éclairs 2 February 1861`

### Tarte au Citron — Acton edition custody / Jeanes page

Treat **edition identity as a search field**, not incidental metadata:

- `"Modern Cookery" Acton 1845 "first edition" 683`
- `"z22c8gru" edition`
- `"rdz664vd" "Third edition"`
- `"Common Lemon Tartlets" 431 Acton`
- `"Store Mixture for Lemon Tartlets" 434 Acton`
- `"Gunter's Modern Confectioner" "Lemon Cheese Cakes" 227`
- `"b20405881" "Lemon Cheese Cakes"`

Do not map printed p.431/p.434 to a scan frame until the scan's edition and pagination continuity are directly verified. Do not use the 1873 Jeanes scan as a substitute for the 1870 p.227 object without edition comparison.

### Paris-Brest 1909–1911

Search contemporaneous local/business language:

- `"Paris-Brest" pâtissier Maisons-Laffitte 1909`
- `"Paris-Brest" Durand 1910 réclame`
- `"Paris-Brest" Bauget 1911`
- `Louis Durand pâtissier Longueil annuaire`
- `Maisons-Laffitte pâtisserie Durand menu`

Do not search only `qui a inventé Paris-Brest`.

### Tatin documentary network

- `"tarte de Mlle Tatin" "18 décembre 1899"`
- `"Hôtel Tatin" "Société de géographie du Cher"`
- `"La Tarte des Demoiselles Tatin" Paul Besnard 1921`
- `"Recette solognote" "Tatin" 1923`
- `"Tarte des Demoiselles Tatin" "L'Orléanais" 1926`
- `"Tarte Tatin" "Paris-Soir" "25 août 1929"`

### Tatin myth genealogy

Search **transmission of the legend**, not an imaginary nineteenth-century accident record:

- `"Horizons d'Argonne" "1976" "Tatin"`
- `"Horizons d'Argonne" "p. 97" Tatin`
- `"n°30 à 39" "Horizons d'Argonne"`
- `"Confrérie des Lichonneux" prospectus 1979`
- `"0413000987"`
- `"W413000745"`
- `"27 mars 1979" Lichonneux`

### Tatin technique genealogy

- `"tourte retournée" 1790 boulanger maîtrise`
- `règlement maîtrise boulanger 1790 tourte retournée`
- `"Tarte aux pêches molles" Urbain Dubois`
- `"La pâtisserie d'aujourd'hui" "Tarte aux pêches molles"`
- object: `https://gallica.bnf.fr/ark:/12148/bpt6k3412588h`

Do not infer recipe identity merely because an older tart is inverted.

### Canelé 1985 legal record

Search deposant/holder variants, not only Confrérie title:

- `CANELE marque collective 1985 INPI`
- `CANELE DE BORDEAUX marque 1985 BOPI`
- `"Union départementale des pâtissiers de la Gironde" CANELE`
- `"Syndicat des patrons pâtissiers de Bordeaux et de la Gironde" CANELE`
- `781846068 CANELE`
- `Daniel Antoine CANELE INPI`
- `24 mars 1985 canelé confrérie`

Do **not** assume `24 March 1985 founding = trademark filing date`.

## Japanese / 日本語

Priority because official French maisons often preserve structured Japanese history pages.

- `ピエール・エルメ イスパハン 1997 歴史`
- `ピエール・エルメ 2000 フィーユ ミルフィーユ`
- `ダロワイヨ オペラ 1955 歴史`
- `アンジェリーナ モンブラン 歴史 1903`
- `フランス 菓子 歴史 パリブレスト`
- `ルリジューズ フランス菓子 歴史`

Verified official anchors:

- Pierre Hermé Japan: https://www.pierreherme.co.jp/our_brand/history.html
- Dalloyau Japan: https://www.dalloyau.co.jp/produits/opera/

Future targets: National Diet Library full-object historical translations and Japanese professional pastry interviews where they preserve direct chef testimony.

## Italiano

Priority: pre-Angelina named chestnut-dessert lineage.

- `Monte Bianco dolce castagne ricetta ottocento`
- `Mont Blanc dolce castagne vermicelli storia`
- `Montebianco marroni ricettario 1800`
- `Rumpelmayer Mont Blanc dolce`

Artusi 1891 already closes a **construction** precursor but not the earliest Italian `Monte Bianco` name.

## Deutsch / Österreich / Schweiz

- `Mont Blanc Kastanien Dessert Kochbuch 19. Jahrhundert`
- `Baba Rum Savarin Konditorei 19. Jahrhundert`
- `Kouglof Baba Stanislaus Stohrer`
- `französische Konditorei Religieuse 19. Jahrhundert`

Goal: independent transmission evidence, not source-count inflation.

## Polski

Priority: Alexandre/Aleksander Micka.

- `Aleksander Micka cukiernik Saint-Tropez`
- `Alexandre Micka Polska cukiernik`
- `Micka Tarte Tropézienne 1955`
- surname variants + migration/naturalization/residence records.

## English / American archive lane

- `"Saint-Honoré" pastry 19th century cookbook`
- `"religieuse" pastry Frascati 1856`
- `"Mont Blanc" chestnut dessert before 1896`
- `"éclairs" "Vanity Fair" 1861`
- `French pastry menu Paris 1900`

Priority institutions:

- Library of Congress;
- University of Michigan periodicals;
- NYPL Buttolph Menu Collection;
- Internet Archive when provenance is identifiable;
- HathiTrust as full-object route when access permits.

## Breton / regional terminology

For Kouign-Amann:

- `kouign` = cake in Breton context;
- `amann` = butter;
- query both Breton orthography and French regional records;
- prioritize Douarnenez municipal/departemental archives and newspapers over modern etymology pages.

## OCR strategy

For historical French corpora search:

- hyphenated/non-hyphenated forms;
- accents omitted: `eclair`, `opera`;
- OCR confusions and broken line wraps;
- surname variants: `Julien/Jullien`, `Anton/Antoine Rumpelmayer`, `Micka/Mika`, `letchi/litchi`;
- corporate/legal owner variants rather than only modern brand names;
- exact neighbor recipes/section headings when page number is missing.

For Gallica use full-text + date filters + proximity search when the object supports it:
https://gallica.bnf.fr/accueil/fr/html/aide-a-la-recherche

## Query evidence rule

A successful query is discovery, not evidence. Every promoted result must resolve to a stable object/page/issue/legal-record locator and receive its own evidence/access/locator/rights/publication state.
