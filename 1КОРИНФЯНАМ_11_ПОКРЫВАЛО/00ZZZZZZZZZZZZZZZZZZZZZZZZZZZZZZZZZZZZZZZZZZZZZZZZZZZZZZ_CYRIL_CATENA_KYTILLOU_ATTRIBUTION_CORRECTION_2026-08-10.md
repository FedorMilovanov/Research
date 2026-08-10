# 1 Коринфянам 11:10 — `Κυτίλλου` catena label → Cyril of Alexandria attribution correction

**Дата:** 2026-08-10  
**Статус:** `CATENA-ATTRIBUTION-CORRECTION / CYRIL-FRAGMENT-PROVENANCE / STRONG-NORMALIZATION / DIRECT-PG74-IMAGE-HOLD / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Supersession target

The Cramer catena firewall deliberately left the digital label:

```text
Κυτίλλου
```

unnormalized, because guessing `Κυρίλλου` (“of Cyril”) from visual similarity alone would have repeated the exact source-attribution error this project is trying to eliminate.

New independent provenance now makes the normalization substantially stronger.

This file supersedes only:

```text
CATENA_KYTILLOU_NORMALIZED_AUTHOR = HOLD
```

with a calibrated Cyril attribution.

---

# 1. The catena fragment itself

Cramer/Scaife’s Vatican-type catena on 1 Corinthians preserves the v10 fragment with the wording:

```text
οὐκοῦν κατακαλυπτέσθω ... διὰ τοὺς ἀγγέλους.
δῆλον δὲ ὅτι τοὺς ταῖς ἐκκλησίαις ἐνιδρυμένους παρὰ Θεοῦ.
```

That is, the woman is to be covered “because of the angels,” understood as those **established by God at/over the churches**.

The digital transcription immediately associated with this author-layer displays:

```text
Κυτίλλου.
```

The same transcription uses `Κυτίλλου` repeatedly elsewhere in the catena, including combined labels such as:

```text
Ὠριγένους ὁμοίως καὶ Κυτίλλου
```

This makes it unlikely that the isolated string is a new author discovered only at 1 Cor 11; it is a systematic edition/transcription form requiring identification.

---

# 2. Independent Cyril fragment tradition

Modern scholarly bibliography independently identifies a substantial surviving fragment corpus:

> Cyril of Alexandria, *Fragmenta in sancti Pauli epistulam I ad Corinthios*.

Controlled edition range:

- P. E. Pusey, *Sancti patris nostri Cyrilli archiepiscopi Alexandrini in D. Joannis evangelium*, vol. 3, pp.249–318;
- corresponding PG 74, cols.856–916.

Independent scholarly controls for this edition/range include:

- Walter J. Burghardt’s study of Cyril, which cites Cyril’s 1 Corinthians fragments as Pusey III 249–319 / PG 74, 856–916;
- Cambridge scholarly bibliography identifying Cyril, *Fragmenta in Epistulam i ad Corinthios*, Pusey vol.3, pp.249–318.

Thus:

```text
CYRIL_1COR_FRAGMENT_CORPUS = INDEPENDENTLY_ESTABLISHED
Pusey_III_249_318 = CYRIL_1COR
PG74_856_916 = CYRIL_1COR
```

---

# 3. Exact thematic/textual convergence at 1 Cor 11

A source explicitly citing Cyril’s 1 Corinthians fragment in **PG 74, 879–883** reproduces the same substantive block:

- woman crowned with her hair;
- female public boldness/propriety language;
- instruction to be covered “because of the angels”;
- angels identified as those appointed/established by God over the churches;
- angels are grieved when the rule of propriety is neglected;
- transition immediately into Paul’s image/glory and male/female argument.

This sequence corresponds to the Cramer/Scaife block, not merely to a generic shared angel doctrine.

Separately, Burghardt cites Cyril’s 1 Corinthians material in this same argumentative neighborhood from Pusey III, including the image/likeness male/female discussion.

The convergence is therefore:

```text
SAME_WORK_CORPUS
+ SAME_1COR11_SEQUENCE
+ SAME_ANGELS_AT_CHURCHES_EXEGESIS
+ SAME_IMAGE/GLORY_TRANSITION
```

not merely:

```text
SIMILAR_THEOLOGY = SAME_AUTHOR
```

---

# 4. Current attribution judgment

The safest current normalization is:

```text
CATENA_KYTILLOU = STRONGLY_IDENTIFIED_AS_CYRIL_OF_ALEXANDRIA
EXPECTED_GREEK_LABEL = ΚΥΡΙΛΛΟΥ
DIGITAL_KYTILLOU = CORRUPT/TRANSCRIPTIONAL_OR_EDITIONAL_FORM
```

Because the printed Cramer page and PG 74, 879–883 page image have not yet been visually inspected in this runtime, retain a final material-control caveat:

```text
CYRIL_ATTRIBUTION = STRONG_MULTI_ROUTE
DIRECT_PG74_PAGE_IMAGE_AUTOPSY = HOLD
DIRECT_CRAMER_PRINT_LABEL_IMAGE_AUTOPSY = HOLD
```

This is stronger than `ATTRIBUTION_HOLD`, but still distinguishes normalization from direct paleographic/print inspection.

---

# 5. Cyril’s angel-function reception can now be named

Source-near formulation:

```text
CYRIL_ANGELS = ANGELS ESTABLISHED BY GOD AT/OVER THE CHURCHES
CYRIL_ANGEL_FUNCTION = GUARD/OBSERVE ECCLESIAL PROPRIETY; GRIEVED BY ITS NEGLECT
```

This is **not identical** to Theodoret’s assigned-over-human-beings / entrusted-with-care model.

It is also not identical to Photius’s later witness/observer-of-subjection formulation.

Current differentiated map:

```text
CHRYSOSTOM = HEAVENLY ANGELS REVERENCED IN WORSHIP
CYRIL = ANGELS ESTABLISHED AT/OVER CHURCHES; ECCLESIAL PROPRIETY
THEODORET = ANGELS ASSIGNED OVER HUMAN BEINGS; CARE/OVERSIGHT
PHOTIUS = ANGELS AS WITNESSES/OBSERVERS OF SUBJECTION
AMBROSIASTER = BISHOPS
SEVERIAN = REPORTS SOME SAY CHURCH PRIESTS
TERTULLIAN = WATCHERS/GEN6
CLEMENT_FRAGMENT = RIGHTEOUS/VIRTUOUS HUMAN OBSERVERS
```

Ancient reception is therefore even more functionally diverse than a simple `holy vs fallen` binary suggests.

---

# 6. Why the earlier firewall was still correct

The earlier file did the right thing by refusing immediate normalization.

Correct research sequence:

```text
1. READ_LITERAL_DIGITAL_LABEL
2. REFUSE_NAME_GUESS
3. SEARCH_INDEPENDENT_WORK/EDITION_PROVENANCE
4. IDENTIFY_MATCHING_FRAGMENT_CORPUS
5. ONLY_THEN_NORMALIZE
```

This should remain the required method for future catena work.

Do not replace the firewall with the opposite shortcut:

```text
ODD_CATENA_LABEL -> OBVIOUS_FAMOUS_FATHER
```

The present Cyril normalization is justified by independent fragment-edition convergence, not by visual resemblance alone.

---

# 7. Effect on project angel grades

No core probability promotion follows merely because a new patristic owner is identified.

```text
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
ANGELS_AS_COSMIC_WITNESSES/PRESENT_ASSEMBLY = B_LEADING
EXACT_ANGELIC_FUNCTION = B_C
CYRIL_CHURCH_ANGELS = C_LOW_RECEPTION_VARIANT / SOURCE_OWNER_NOW_STRONG
```

The source-ownership confidence has increased; the probability that Paul intended Cyril’s exact later function has not automatically increased.

---

# 8. Supersession statement

```text
OLD:
CATENA_KYTILLOU_BLOCK = ANGELS_ESTABLISHED_AT_CHURCHES / NORMALIZED_AUTHOR_HOLD

NEW:
CATENA_KYTILLOU_BLOCK = STRONG_CYRIL_OF_ALEXANDRIA_ATTRIBUTION
CYRIL_FRAGMENT_CORPUS = PUSEY_III_249_318 / PG74_856_916
CYRIL_1COR11_ANGEL_BLOCK = PG74_879_883_STRONGLY_LOCATED
DIRECT_PAGE_IMAGE = HOLD
```

---

# 9. Result

```text
CORE_GRADE_REVERSALS = 0
CYRIL_1COR_FRAGMENT_CORPUS = VERIFIED_BIBLIOGRAPHIC/SCHOLARLY
KYTILLOU_TO_CYRIL_NORMALIZATION = STRONG_MULTI_ROUTE
CYRIL_ANGELS_AT_CHURCHES = STRONG_PAGE_LOCATED_RECEPTION
CYRIL_DIRECT_PG74_PAGE_IMAGE = HOLD
CYRIL_DIRECT_CRAMER_PRINT_LABEL_IMAGE = HOLD
EXACT_ANGELIC_FUNCTION = B_C_UNCHANGED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
