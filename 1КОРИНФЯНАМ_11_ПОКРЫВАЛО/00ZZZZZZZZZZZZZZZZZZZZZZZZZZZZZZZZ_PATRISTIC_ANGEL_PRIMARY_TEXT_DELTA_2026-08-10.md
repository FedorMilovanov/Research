# 1 Коринфянам 11:10 — patristic angel primary-text delta

**Дата:** 2026-08-10  
**Статус:** `PRIMARY-PATRISTIC-TEXT / ATTRIBUTION-CORRECTION / RECEPTION-HISTORY / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

Paczkowski 2023 is an excellent modern map of patristic angelological reception, but modern summaries must be pressure-tested against surviving primary wording where accessible.

This pass asks:

> Does the primary author personally endorse a reading, report that others hold it, or merely provide background later associated with the reading?

```text
MODERN_SUMMARY != PRIMARY_AUTHOR_OWNERSHIP
REPORTS_A_VIEW != ENDORSES_A_VIEW
RECEPTION_EXISTENCE != EXEGETICAL_PROBABILITY
```

---

# 1. Tertullian — fallen-angels / Genesis 6 reading is direct

Primary English routes:

- *On the Veiling of Virgins* (New Advent): https://www.newadvent.org/fathers/0403.htm
- ch.11 parallel transcription: https://en.wikisource.org/wiki/Ante-Nicene_Fathers/Volume_IV/Tertullian:_Part_Fourth/On_the_Veiling_of_Virgins/Chapter_11

Tertullian directly links Paul’s `because of the angels` with the Genesis tradition in which heavenly beings desired the daughters of men. In the larger treatise he explicitly identifies the relevant angels as those who fell from God/heaven through desire for women.

Thus:

```text
TERTULLIAN_WATCHERS/FALLEN_ANGELS_READING = DIRECT_PRIMARY
GEN6_LINK_IN_EARLY_RECEPTION = A_RECEPTION_FACT
WATCHERS_AS_PAULS_ACTUAL_REFERENT = C_SERIOUS_ALTERNATIVE // unchanged
```

The first statement is reception history; the last remains modern exegetical calibration.

---

# 2. John Chrysostom — holy/heavenly angels + immediate v10 backlink

Primary route:

- Homily 26 on First Corinthians: https://www.newadvent.org/fathers/220126.htm

At 1 Cor 11:10 Chrysostom explicitly asks what `for this cause` refers to and answers that it is because of the reasons just stated, **plus** `because of the angels`.

He then urges the woman who might disregard her husband nevertheless to reverence the angels.

Safe result:

```text
CHRYSOSTOM_ANGELS = HEAVENLY/RELIGIOUS_BEINGS_IN_CONTEXT
CHRYSOSTOM_DIA_TOUTO = PRECEDING_REASONS_PLUS_ANGELS
CHRYSOSTOM_ANGELS_AS_PRIESTS_OR_BISHOPS = FALSE_ATTRIBUTION
```

Nothing in this primary passage identifies `angels` as priests or bishops.

---

# 3. Ambrosiaster — bishops reading is direct

The existing primary-Latin branch audit already pinned Ambrosiaster’s wording:

```text
angelos episcopos dicit
```

Primary Latin route:

- https://la.wikisource.org/wiki/Commentaria_in_Epistolam_ad_Corinthios_Primam_(Ambrosiaster)

Therefore:

```text
AMBROSIASTER_ANGELS_AS_BISHOPS = DIRECT_PRIMARY_ENDORSEMENT
```

This remains the strongest directly verified ancient clergy-reading in the current corpus.

---

# 4. Severian of Gabala — crucial attribution correction

## 4.1 Direct surviving fragment

A synchronized primary-text edition exposes the Greek fragment on 1 Cor 11:10:

- https://catholiclibrary.org/library/view?docId=%2FFathers-Synchronized-EN%2FSeverianus__in_epistulam_i_ad_Corinthios.en.html%3Bchunk.id%3D00000035

The relevant wording contains:

```text
τινὲς δὲ ἀγγέλους τοὺς ἱερέας τῆς ἐκκλησίας εἰρῆσθαί φασιν
```

The decisive source-hygiene feature is:

```text
τινὲς ... φασιν = some say
```

Thus the surviving fragment does **not** safely permit:

```text
SEVERIAN_PERSONALLY_IDENTIFIES_ANGELS_AS_PRIESTS = CERTAIN
```

Instead it permits:

```text
SEVERIAN_REPORTS_AN_ANCIENT_PRIESTS_READING = DIRECT_PRIMARY
ANCIENT_PRIESTS_READING_EXISTED_BY_SEVERIANS_RECEPTION_HORIZON = STRONG
SEVERIAN_PERSONAL_ENDORSEMENT_OF_PRIESTS_READING = HOLD/NOT_ESTABLISHED_BY_THIS_FRAGMENT
```

This is a meaningful correction to a stronger modern paraphrase.

## 4.2 What Severian himself says first

Before reporting the priest-reading, the fragment says in substance that the Apostle reminds women that God has appointed angels over us.

Therefore Severian’s own immediate line appears compatible with superhuman angels, after which he records another interpretation held by `some`.

Do not collapse those two sentences.

---

# 5. Theodoret of Cyrrhus — guardian-angel attribution remains source-pinned but direct-text HOLD

Paczkowski 2023 cites:

```text
Theodoretus Cyrensis, Interpretatio epistulae I ad Corinthios XI,
PG 82, 312D–313A
```

and reports a guardian-angel reading tied to Acts 12:15 and Matt 18:10. Older technical commentaries independently attribute a guardian-angel reading to Theodoret.

The PG 82 index directly verifies that Theodoret’s *Interpretatio epistolae I ad Corinthios* occupies the relevant volume/column range, but this pass did not obtain the exact 312D primary Greek bytes in a reliable direct reader.

Therefore:

```text
THEODORET_GUARDIAN_ANGELS = STRONG_SECONDARY/PATRISTIC_SOURCE_ATTESTED
THEODORET_EXACT_312D_PRIMARY_TEXT = LOCATOR_OBJECT_HOLD
GUARDIAN_ANGELS_EXACT_V10_MODEL = C_LOW // current modern grade retained
```

Do not promote `guardian angels` merely because the attribution is ancient.

---

# 6. Updated ancient angel-reception map

| Ancient witness | Reading/status | Ownership confidence |
|---|---|---|
| Tertullian | fallen angels / Gen 6 sexual danger | **direct endorsement** |
| Chrysostom | heavenly angels to be revered; worship context | **direct** |
| Ambrosiaster | bishops | **direct endorsement** |
| Severian of Gabala | reports `some say` angels = priests of church | **direct report of others; personal endorsement not established** |
| Theodoret | guardian angels | **strong attribution; exact primary locator still HOLD** |

This table is deliberately about **reception ownership**, not probability of Paul’s intended referent.

---

# 7. Effect on current modern grades

None.

```text
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
ANGELS_AS_COSMIC_WITNESSES/PRESENT_ASSEMBLY = B_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
HUMAN_MESSENGERS = D_C_LOW_PUBLISHED_ALTERNATIVE
BISHOPS/CLERGY = D_C_LOW_RECEPTION
GUARDIAN_ANGELS = C_LOW
CORE_GRADE_REVERSALS = 0
```

The primary-text delta improves **who actually says what**.

---

# 8. New no-overclaim rules

```text
PACZKOWSKI_SUMMARY_SEVERIAN_IDENTIFIES_BISHOPS != PRIMARY_FRAGMENT_PERSONAL_ENDORSEMENT
SEVERIAN_TINES_PHASIN = REPORT_OF_OTHERS
AMBROSIASTER_BISHOPS = DIRECT_ENDORSEMENT
TERTULLIAN_WATCHERS = DIRECT_RECEPTION_FACT
ANCIENTNESS != PAULINE_PROBABILITY
```

---

## Boundary

```text
RECEPTION_HISTORY != AUTHORIAL_INTENT
SOURCE_OWNERSHIP_MATTERS
DIRECT_PRIMARY_TEXT > MODERN_PARAPHRASE_FOR_ATTRIBUTION
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
