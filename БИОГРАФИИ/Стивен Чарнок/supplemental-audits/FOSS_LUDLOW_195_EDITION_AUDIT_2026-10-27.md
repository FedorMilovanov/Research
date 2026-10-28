# Foss, “Ludlow, 195”: edition and locator audit

**Checked:** 27 October 2026<br>
**Question:** Which edition/volume of Edmund Ludlow’s *Memoirs* is meant by Foss’s short reference “Ludlow, 195”?<br>
**Result:** the strongest page-level match found is the **1771 edition, p. 195**, but Foss does not name an edition and the page image has not yet been visually inspected. Do not present the 1771 witness as Foss’s proven source or assign it a volume number.

## Findings

1. **Foss’s own locator.** Edward Foss, *The Judges of England*, vol. VI (London, 1857), pp. 422–423; p. 423 attaches “Ludlow, 195” to the account of the confrontation dated 20 April 1653. The OCR also shows Foss’s separate reference to Whitelocke, p. 565; that note concerns the Lancaster County Palatine jurisdiction Act, not the Chester/Northwich ordinance or a refusal to issue a Chester commission. Foss OCR (`B1 / checked text layer`; print page image not visually collated): https://dn760001.eu.archive.org/0/items/judgesofenglandw06fossuoft/judgesofenglandw06fossuoft_djvu.txt .

2. **Positive match: Ludlow, 1771.** The Internet Archive page-number JSON maps scan leaf 207 to printed p. 195 at confidence 100; the OCR for that leaf contains the exchange/confrontation described by Foss. The independent Bayerische Staatsbibliothek OCR for scan 247 labels the page “195” and contains the same passage. These are strong, mutually consistent text-layer locators (`A1 / checked OCR and page metadata`), not visual collation:
   - IA item and reader: https://archive.org/details/bim_eighteenth-century_memoirs-of-edmund-ludlow_ludlow-edmund_1771 ; https://archive.org/details/bim_eighteenth-century_memoirs-of-edmund-ludlow_ludlow-edmund_1771/page/197/mode/2up
   - IA page-number JSON: https://archive.org/download/bim_eighteenth-century_memoirs-of-edmund-ludlow_ludlow-edmund_1771/bim_eighteenth-century_memoirs-of-edmund-ludlow_ludlow-edmund_1771_page_numbers.json
   - BSB OCR and image metadata: https://api.digitale-sammlungen.de/ocr/bsb10722812/247 ; https://api.digitale-sammlungen.de/iiif/image/v2/bsb10722812_00247/info.json
   - BSB image route (not retrieved/visually inspected): https://api.digitale-sammlungen.de/iiif/image/v2/bsb10722812_00247/full/full/0/default.jpg

3. **Volume is not established.** Yale describes its 1771 witness as a quarto (`xii, 558, 19, [31] p.`), but its catalogue record says that this particular extra-illustrated copy is physically expanded into two volumes; it does not assign printed p. 195 to either physical volume. Therefore use “1771 ed., p. 195” only as a page-level candidate, not “vol. I” or “vol. II.” Yale record (`C / checked catalogue`): https://search.library.yale.edu/catalog/99166416283408651 .

## Other editions checked

| Witness | Result | Status / locator |
|---|---|---|
| 1698, vol. I | Printed p. 195 concerns 1647 material, not the 20 April 1653 exchange. Vol. II begins at p. 435. | EEBO-TCP full text checked: https://quod.lib.umich.edu/e/eebo/A49445.0001.001/1:4?rgn=div1;view=fulltext ; vol. II: https://quod.lib.umich.edu/e/eebo2/B26328.0001.001/1:2?rgn=div1;view=fulltext |
| 1751, London folio witness | IA leaf labelled p. 195 has unrelated OCR; page-number confidence is null. This does not amount to a visual exclusion. A separate Google Books OCR snippet places the exchange at p. 23, not p. 195. | IA item: https://archive.org/details/bim_eighteenth-century_memoirs-of-edmund-ludlow_ludlow-edmund_1751 ; GB id `WRJcAAAAcAAJ` (bibliographic/search locator only). |
| 1720, vol. II | No verified printed-p.195 locator. The `/page/n195` scan leaf is not proved to be printed p. 195. | IA item: https://archive.org/details/bim_eighteenth-century_memoirs-of-edmund-ludlow_ludlow-edmund_1720_2 ; `LOCATOR_HOLD`. |
| 1771 quarto | Printed p. 195 text-layer match is positive; edition/volume intended by Foss remains unproven. | `A1 / checked` OCR and page metadata; `ARCHIVE_HOLD` for raster; `LOCATOR_HOLD` for Foss’s edition attribution. |

## Conservative citation rule

- Safe statement: **“Foss, vol. VI, p. 423, cites ‘Ludlow, 195’ for the 20 April 1653 confrontation; a matching text-layer witness is Ludlow, 1771 ed., p. 195.”**
- Unsafe until a page image or other edition-specific evidence is checked: **“Foss used the 1771 edition”**, or any volume number for that page.
- The IA/BSB OCR and page-number services returned text/metadata only; image requests failed (HTTP 500 in the prior access attempt). Keep the 1771 raster `ARCHIVE_HOLD`; OCR is not a substitute for visual inspection.
