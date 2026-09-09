# Bible Quotation / Numbering / Translation / Original-Language Policy — Teen Double Life Series

**Status:** PRE-DRAFT PRODUCT-AWARE SCRIPTURE CONTROL / RESEARCH ONLY / NOT PUBLICATION  
**Date:** 2026-09-07  
**Scope:** Parts I–III + adult-child/prodigal companion.  
**Purpose:** prevent a well-researched English-language source packet from producing wrong Russian Bible references, silent translation mixing, or unnecessary Hebrew/Greek display in the future `gb-is-my-strength` articles.

---

# 0. Why this control became necessary

The Research corpus uses many English-language primary sources (Calvin, Owen, Gill, Edwards, Spurgeon, modern reviews) and often inherits their Bible numbering conventions.

That creates a concrete publication risk in Psalms because Russian Synodal/LXX-style Psalm numbering may differ from the MT/English numbering used in English commentaries.

A critical example was found in Part III source packets:

> English source: `Psalm 50:16–21` — “What right have you to recite my statutes...”

For a Russian Synodal reader this is **not Psalm 50**.

The Russian Synodal reference is:

> **Пс. 49:16–21** — «Грешнику же говорит Бог: что ты проповедуешь уставы Мои и берешь завет Мой в уста твои...»

Russian **Пс. 50** is instead the penitential Psalm beginning:

> «Помилуй меня, Боже, по великой милости Твоей...»

Therefore copying English Psalm numbers into Russian publication is forbidden without cross-check.

---

# 1. P0 correction for Part III

## Incorrect for Russian publication

`Пс. 50:16–21` as the hypocrisy / “recite my statutes” text.

## Correct Russian Synodal reference

> **Пс. 49:16–21**

## Cross-reference when discussing an English source

If necessary in a source note:

> Пс. 49:16–21 по русской Синодальной нумерации (= Ps 50:16–21 MT/English numbering).

Do **not** burden ordinary prose with both numbers every time. The double number belongs in the first scholarly/source clarification where needed.

### Publication consequence

All future Part III drafting packets, article prose, source notes, tooltip references and bibliography comments must normalize this passage to **Пс. 49:16–21** for the Russian reader.

Existing Research files that say `Psalm/Ps. 50` may remain as records of English-source work, but they are **not publication-ready numbering**.

---

# 2. Product repository’s actual Bible-data policy

Read-only audit of `FedorMilovanov/gb-is-my-strength@main` found:

`data/bible/books.json` explicitly defines:

```json
"defaultTranslationByTestament": {
  "OT": "synodal",
  "NT": "kassian"
}
```

with labels:

- OT — **Синодальный перевод**;
- NT — **перевод еп. Кассиана (Безобразова)**.

This is important: the current product Bible tooltip/data layer is **not two parallel complete Bibles**.

It is testament-specific by default:

- Old Testament files resolve to `data/bible/synodal/...`;
- New Testament files resolve to `data/bible/kassian/...`.

The current data corpus is also **selective rather than exhaustive**. For example, current NT files do not necessarily contain every verse required by this series (Eph. 6:1–4, Luke 15, 2 Cor. 7:10–11 may be absent from the current local verse subset).

### Guard

Do not treat the tooltip dataset as the sole textual authority for every quotation merely because it exists in the product repo.

Do not silently add missing Bible-data entries from Research; product-data mutation belongs to a later bounded product lane with its own rules and validation.

---

# 3. Observed current MDX writing practice

Read-only inspection of current native MDX articles shows a stable editorial pattern:

1. reader-facing theological prose remains normal Russian;
2. Scripture is quoted/paraphrased in Russian;
3. Hebrew/Greek appears only where lexical/exegetical precision benefits materially;
4. original-language display does not replace the Russian biblical sentence;
5. application is distinguished from the text’s direct meaning rather than pretending every modern application is the verse’s immediate referent.

Examples inspected:

- `src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx` — Russian Scripture wording plus targeted `לֵב / καρδία` analysis;
- `src/content/articles/cerkovnaya-disciplina-vlast-granicy-zashchita.mdx` — Russian theological prose plus targeted Greek terms (`οἰκονόμος`, `καταρτίζω`) where argument requires them.

This is the model for this series.

---

# 4. Drafting policy for this series

## 4.1 Reader-facing body

Default:

> **Russian Bible wording first.**

The article must read naturally as Russian theological journalism / pastoral exposition, not as an interlinear notebook.

## 4.2 OT passages

Default citation/reference convention should follow the **Russian Synodal numbering and book names** because that is the product’s OT Bible-data default and the natural reference system for the site’s Russian readership.

Where an English/MT source uses a different Psalm number, verify mapping before publication.

## 4.3 NT passages

The product tooltip/data default is Kassian, but that does **not** require every body quotation to be silently represented as Kassian if the final editorial lane selects another clearly identified Russian wording.

Before final direct quotation:

1. choose the Russian wording deliberately;
2. identify translation if wording matters to the argument;
3. do not splice phrases from different Russian translations into quotation marks as though they were one published translation;
4. where article reasoning rests on the Greek rather than on a Russian rendering, say so explicitly.

## 4.4 Literal/editorial rendering

If a standard Russian translation obscures a point that matters materially, a literal rendering may be supplied, but it must be marked:

- `буквально:`;
- `более буквально:`;
- `смысловой перевод:`;
- or an equivalent transparent label.

Never present an agent-authored literal rendering as “the Bible says” in quotation marks without disclosure.

---

# 5. Original languages — when to show them

Use Hebrew/Greek only when at least one of these is true:

1. the semantic range materially changes the argument;
2. a Russian translation might suggest a stronger/weaker claim than the original supports;
3. a grammatical/syntactical issue is central to the disputed interpretation;
4. terminology needs disambiguation across passages.

Do **not** show original-language words merely to create academic atmosphere.

### Likely justified cases in this project

- Eph. 4:19 `ἀπηλγηκότες` — when discussing callousness/loss of sensitivity and explicitly rejecting neurological overreading;
- repentance vocabulary where a precise lexical claim is actually made;
- selected command/discipline vocabulary if the argument depends on force/aspect/semantic range.

### Likely unnecessary cases

- routine quotations from Prov. 9;
- Heb. 11:25 “fleeting pleasure of sin” if no lexical dispute is being argued;
- ordinary references to “flee youthful passions” when the Russian wording is sufficient.

---

# 6. Psalm-numbering gate for ALL selected Psalms

Before drafting any Psalm citation from an English source:

1. identify the MT/English Psalm number used by the source;
2. identify the Russian Synodal number used by the product/readership;
3. verify verse correspondence, not merely Psalm title;
4. store Russian publication number as primary;
5. retain English/MT number only in source notes if needed to make the cited commentary discoverable.

### Known locked mapping for this series

| Theme | English/MT source numbering | Russian Synodal publication numbering |
|---|---|---|
| wicked person recites God’s statutes / hates correction | Psalm 50:16–21 | **Пс. 49:16–21** |
| David’s penitential “Have mercy on me, O God” | Psalm 51 | **Пс. 50** |

This table must be expanded only when another selected Psalm actually enters final prose.

---

# 7. Immediate consequences for current Research packets

The following concept is **GREEN**:

> outward religious speech/song cannot function as cover for defended rebellion; Psalm 49:16–21 is a strong biblical witness in its covenant/worship context.

The following reference form is **RED for Russian publication**:

> `Пс. 50:16–21` for that passage.

English-language Research/source files may continue to mention `Ps 50` when accurately reporting Calvin/English editions, provided downstream drafting uses this `105` normalization control.

---

# 8. Interaction with Part III choir/worship argument

The Psalm correction strengthens rather than weakens the argument.

But the direct text still does **not** legislate a children’s choir policy.

Correct inferential chain:

`Пс. 49:16–21 direct meaning`  
→ God condemns covenantal/religious profession on the lips joined to hatred of correction and defended evil  
→ religious speech cannot morally neutralize rebellion  
→ church leaders may not use “but the child sings Christian songs” as evidence that known serious rebellion is harmless  
→ exact choir participation policy remains ecclesial/pastoral application, not an inspired eligibility list.

This preserves the established `TEXT → PRINCIPLE → PRUDENCE/POLICY` hierarchy.

---

# 9. Product mutation guard

This file is Research guidance only.

Do **not** in this lane:

- edit `gb-is-my-strength/data/bible/**`;
- expand Kassian/Synodal datasets;
- alter Bible-tooltip runtime;
- change product article files;
- declare a site-wide new translation policy.

Any such changes require the product repository’s live preflight, owner lane, overlap check and validation gates.

---

# 10. Final publication rule

> **Quote Scripture in readable Russian; cite according to the Russian reader’s numbering; show original languages only when they do exegetical work; disclose literal/editorial renderings; and never inherit an English Psalm number without verification.**

For this project the first critical correction is locked:

> **Part III central hypocrisy/worship text = Пс. 49:16–21 (Russian Synodal), not Пс. 50:16–21.**
