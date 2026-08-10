# 1 Коринфянам 11:2–16 — current Greek text base and textual-risk audit

**Дата:** 2026-08-10  
**Статус:** `CURRENT-GREEK-BASE / TEXTUAL-RISK / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Why this file exists

The project now performs very fine semantic work on individual Greek expressions. That creates a new failure mode:

> a future agent/UI may call a Greek string “the latest original” without specifying which current critical edition is controlling, or may imply that a completed Pauline ECM/NA29 apparatus already exists.

This file sets a fail-closed text-base contract for 1 Cor 11:2–16.

---

# 1. Current published base

The German Bible Society’s current official description of **The Greek New Testament, Sixth Edition (GNT6)** states that:

- GNT6 was published in 2025;
- it uses the most current text available from the Editio Critica Maior work;
- its text is **identical to that of the future Nestle-Aland 29th edition**;
- new ECM-based text changes incorporated into GNT6 specifically include **Mark, Acts, and Revelation**;
- apparatus witness selection was comprehensively revised, including Pauline letters.

Therefore for this project:

```text
CURRENT_PUBLISHED_GREEK_BASE = GNT6
GNT6_PUBLICATION_YEAR = 2025
FUTURE_NA29_TEXT_IDENTICAL_TO_GNT6 = A_OFFICIAL_PUBLISHER
```

This is the correct basis for describing the Greek layer as current **as of 2026-08-10**.

---

# 2. NA29 status

Official Deutsche Bibelgesellschaft catalog data gives the planned publication date for the standard NA29 edition as:

```text
2027-02-28
```

Therefore on 2026-08-10:

```text
NA29_IS_PUBLISHED = false
NA29_SCHEDULED_PUBLICATION = 2027-02-28
```

Do not call a physical/currently published NA29 the source edition before that date.

But because the publisher explicitly states that GNT6 and future NA29 share the same **text**, it is legitimate to say:

> the current GNT6 Greek text is the text planned for NA29.

It is **not** legitimate to say:

> we have already consulted the full published NA29 apparatus.

```text
GNT6_TEXT_EQUALS_FUTURE_NA29_TEXT = true
GNT6_APPARATUS_EQUALS_FUTURE_NA29_APPARATUS = false / DO_NOT_ASSUME
```

---

# 3. Pauline ECM status — crucial boundary

The INTF ECM project is being published book-group by book-group.

The current official GNT6 description highlights new ECM text incorporated from:

- Mark;
- Acts;
- Revelation.

It does **not** claim that a completed ECM volume for the Pauline letters has supplied a new full Pauline text.

The official NA29 description likewise says the edition incorporates the **latest results** of ECM work, not that every NT corpus now has a completed ECM.

Therefore:

```text
COMPLETED_PAULINE_ECM_FOR_1COR = false
CLAIM_NEW_ECM_PAULINE_TEXT_1COR11 = prohibited
```

A future agent must not write:

> “NA29/ECM changed the text of 1 Cor 11...”

unless a specific official critical source demonstrates that exact change.

---

# 4. What GNT6 does change for Pauline textual work

Even where the base text itself is not newly replaced by a completed Pauline ECM, GNT6’s official description says the **apparatus witness selection** was thoroughly revised, with adjustments including Pauline letters.

This matters for Research:

```text
SAME_OR_STABLE_BASE_TEXT != SAME_APPARATUS_INFORMATION
```

A future text-critical pass on a disputed word should therefore prefer:

1. GNT6/current official apparatus;
2. INTF/NTVMR manuscript/transcription data where resolvable;
3. future NA29 apparatus once actually published;
4. older NA28/UBS5 apparatus as historical controls, not automatically final current apparatus.

---

# 5. Passage-level textual-risk classification

The exegetical controversies in 1 Cor 11:2–16 are dominated by **semantic, syntactic, historical and discourse questions**, not by a known wholesale textual instability of the entire pericope.

The project already separately grades the theory that 11:3b–15 is an interpolation as:

```text
INTERPOLATION_11_3B_15 = D_C_LOW
```

That remains unchanged.

Why the current text-base audit does not promote interpolation:

- there is no established manuscript omission-base for the whole unit comparable to a genuine absent passage tradition;
- current critical editions retain the unit;
- later structural/quotation theories do not become textual variants merely because they propose another speaker or an interpolation.

Thus:

```text
PERICOPE_PRESENT_IN_CURRENT_CRITICAL_TEXT = A_EDITIONAL_FACT
WHOLE_UNIT_TEXTUAL_INSTABILITY = LOW_RELATIVE_TO_EXEGETICAL_INSTABILITY
```

This statement does **not** mean every word has zero variants. It means no identified variant presently overturns the project’s core semantic nodes by itself.

---

# 6. Variant-risk contract for each analytical node

For the future Greek/Russian analytical matrix, every disputed node should carry a separate field:

```text
textual_variant_risk
```

Allowed values:

```text
NONE_KNOWN_MATERIAL
LOW
MEDIUM
HIGH
HOLD_APPARATUS
```

Do not use semantic uncertainty as if it were textual uncertainty.

Examples:

```text
κεφαλή semantic debate != manuscript uncertainty
ἐξουσία referent debate != manuscript uncertainty
διὰ τοὺς ἀγγέλους referent debate != manuscript uncertainty
φύσις semantic debate != manuscript uncertainty
τοιαύτην συνήθειαν referent debate != manuscript uncertainty
```

Unless apparatus evidence says otherwise, these are **interpretive** disputes over a critically printed text.

---

# 7. Copyright / text-reproduction boundary for future Product work

The project may use a current critical edition as the research authority without assuming unlimited redistribution rights for the full edition text.

Therefore the Product handoff must distinguish:

```text
TEXT_AUTHORITY = GNT6
TEXT_REPRODUCTION_RIGHTS = separate question
```

The Research repository should preserve:

- verse/segment identifiers;
- lemma references;
- short disputed Greek expressions needed for analysis;
- edition metadata;
- variant-risk flags.

A future public Product agent must verify edition licensing/quotation conditions before embedding the complete GNT6 passage as distributable page content.

This is not a theological issue; it is a publication/legal boundary.

---

# 8. Current research-text contract

For all new 1 Cor 11 work:

```text
GREEK_BASE_EDITION = GNT6_2025
GREEK_BASE_STATUS = CURRENT_PUBLISHED
FUTURE_NA29_TEXT_STATUS = IDENTICAL_TO_GNT6_BY_OFFICIAL_PUBLISHER
NA29_PHYSICAL_EDITION_STATUS_2026_08_10 = NOT_YET_PUBLISHED
PAULINE_ECM_STATUS = NOT_COMPLETE_FOR_1COR
```

If an older file says “NA28 base,” interpret it as a historical work-state unless the exact word/reading is rechecked against current GNT6.

Do **not** silently rewrite old research citations from NA28 to GNT6.

Instead use:

```text
HISTORICAL_BASE_EDITION = preserved
CURRENT_TEXT_AUTHORITY = GNT6
```

---

# 9. Claims prohibited after this audit

```text
“NA29 is already the currently published edition.”
“1 Cor 11 is based on a completed Pauline ECM.”
“GNT6 introduced a new Pauline ECM text for 1 Cor 11.”
“Because the passage is difficult, its Greek text is textually unstable.”
“Quotation/refutation theory is itself a manuscript variant.”
“Interpolation theory is established by current critical editions.”
“GNT6 and future NA29 necessarily have identical apparatuses because their texts are identical.”
```

---

# 10. Claims allowed

```text
“GNT6 is the current published Greek base used by this Research.”
“Deutsche Bibelgesellschaft states that GNT6’s text is identical to the text of the future NA29.”
“NA29 is scheduled for publication on 2027-02-28.”
“Current ECM-driven text changes highlighted for GNT6 include Mark, Acts and Revelation.”
“Pauline witness selection/apparatus work has been revised, but a completed Pauline ECM for 1 Corinthians is not claimed.”
“The major disputes in 1 Cor 11:2–16 are primarily interpretive unless a specific apparatus variant is identified.”
```

---

# 11. Next apparatus-level work

A future dedicated apparatus pass should be **variant-led**, not theory-led:

1. obtain the current GNT6 apparatus for 1 Cor 11:2–16 or official digital equivalent;
2. list every variant that materially affects translation/syntax;
3. identify manuscript support via INTF/NTVMR where resolvable;
4. classify whether the variant can affect an existing claim grade;
5. do not inflate spelling/word-order noise into theological variants;
6. create a `TEXTUAL_VARIANT_LEDGER` only after direct apparatus access.

Until that pass:

```text
CLAIM_SPECIFIC_VARIANT_PROMOTION = HOLD_APPARATUS
```

The current base itself, however, is no longer ambiguous.

---

# 12. Boundary

```text
DO_NOT_REQUEST_FROM_USER_IF_AGENT_CAN_ACCESS = true
PRODUCT_WRITE = false
UI_IMPLEMENTATION = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
```
