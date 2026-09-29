# Steven J. Lawson — ISBN registrant prefix / micro-publisher block audit

**Snapshot:** 2026-09-29  
**Status:** `OFFICIAL ISBN STRUCTURE VERIFIED / U.S. REGISTRANT = 979-8-9961673 / 10-NUMBER CAPACITY / REGISTRANT NAME STILL UNRESOLVED`

## 1. Executive finding

The ISBN printed across the public retail record for *Mercy in the Wilderness* is:

- `9798996167302`

Using the current range rules distributed from the **International ISBN Agency**, that number parses as:

> **979-8-9961673-0-2**

where:

- `979` = ISBN prefix element;
- `8` = United States registration group;
- `9961673` = seven-digit registrant/publisher element;
- `0` = one-digit publication element;
- `2` = check digit.

The result is important because the International ISBN standard explicitly ties registrant-element length to anticipated publisher output: **larger publishers receive shorter registrant elements; smaller-output publishers receive longer ones.**

A seven-digit U.S. registrant element is therefore at the smallest-output end of the ISBN allocation structure.

Because only one digit remains for the publication element, this particular registrant prefix can structurally identify **10 publication numbers: 0–9**.

That is highly consistent with a very small independent/self-publisher allocation rather than the prefix architecture of a high-output established publishing house.

It does **not** by itself reveal whether the registrant's legal/publisher-of-record name is `Steven Lawson`, `But God Press`, or another entity.

---

## 2. Range-rule source

Current machine-readable ISBN range data:
- https://isbnbarcode.org/api/isbn-ranges.json

The file identifies its own source as:

- `MessageSource: International ISBN Agency`
- `MessageDate: Fri, 24 Jul 2026 05:44:13 BST`

For registration group `979-8`, the file states:

- Agency: **United States**
- range `9960000–9984999`
- registrant `Length: 7`

The Lawson sequence after the `979-8` group begins:

- `9961673...`

which falls squarely inside `9960000–9984999`.

Therefore the seven-digit registrant boundary is not guessed from typography or retailer hyphenation; it follows the current International ISBN Agency range table.

## 3. Formal parse

Raw ISBN:

`9798996167302`

### Prefix element

`979`

### Registration group

`8`

The current range table identifies `979-8` as:

> **United States**

### Registrant element

The remaining sequence begins `9961673...`.

For `979-8`, any value in `9960000–9984999` has a **7-digit registrant element**.

Thus:

> Registrant = `9961673`

Full publisher prefix / first three ISBN components:

> **`979-8-9961673`**

### Publication element

After `979` + `8` + seven-digit registrant, one digit remains before the final check digit:

> Publication element = `0`

### Check digit

> `2`

### Result

> **ISBN 979-8996167302 = 979-8-9961673-0-2**

---

## 4. What the International ISBN Agency says registrant length means

International ISBN Agency publisher guidance states that the range of publication elements assigned to a publisher is based on current and anticipated future publishing output and is **directly related to the length of the registrant element**.

Official source:
- https://www.isbn-international.org/content/publishers/47

The ISBN User Manual is more explicit:

> the registrant element identifies a particular publisher or imprint;
> its length varies directly with anticipated publisher output;
> publishers with the largest expected outputs receive the shortest registrant elements, and vice versa.

Official manual:
- https://www.isbn-international.org/sites/default/files/ISBN%20Manual%202012%20-corr.pdf

Current International ISBN Agency explanation likewise says:

- the registrant element identifies the particular publisher or imprint;
- it may be up to seven digits.

Source:
- https://www.isbn-international.org/index.php/node/10

### Evidentiary conclusion

A **seven-digit registrant** is not neutral noise. It is deliberately the long end of the ISBN publisher-prefix structure and corresponds to low anticipated publishing output.

---

## 5. Why this prefix has 10 publication slots

An ISBN-13 contains exactly 13 digits:

- 3-digit prefix;
- variable registration-group element;
- variable registrant element;
- variable publication element;
- 1-digit check digit.

For this ISBN:

- prefix = 3 digits (`979`)
- group = 1 digit (`8`)
- registrant = 7 digits (`9961673`)
- check digit = 1 digit (`2`)

That consumes 12 of 13 positions, leaving exactly **one digit** for the publication element.

A one-digit decimal publication element has ten possible values:

> `0,1,2,3,4,5,6,7,8,9`

Thus the publisher prefix `979-8-9961673` structurally supports **10 ISBN publication identifiers**.

This follows directly from the official ISBN structure and the official current range boundary.

## 6. Bowker independently confirms the small-block model

ISBN.org / Bowker is the official U.S. ISBN Agency.

Its ISBN-standard page says ISBNs are assigned to publishers and self-publishers in quantities including:

- 1
- **10**
- 100
- 1,000
- 10,000
- 100,000

Source:
- https://www.isbn.org/about_ISBN_standard

Bowker's general FAQ further says:

- the U.S. ISBN Agency database establishes the **publisher of record associated with each prefix**;
- an ISBN publisher prefix identifies a **single publisher**;
- publishers/self-publishers need their own prefix if they want to be correctly identified as publisher of record.

Source:
- https://www.isbn.org/faqs_general_questions

This independently fits the mathematical result above: `979-8-9961673` behaves as a ten-number publisher block.

### Guardrail

The presence of a 10-number block does not prove Lawson purchased it personally or when it was acquired. It proves only the scale and structure of the registrant allocation.

---

## 7. Why this matters for `But God Press` vs. `Steven Lawson`

The prior publishing-chain audit established a metadata split for exactly the same ISBN:

### Amazon current state

Current Amazon product details say:

> Publisher: **Steven Lawson**

### Broad independent distribution feeds

Multiple retailers/catalogs say:

> Publisher: **But God Press**

### ISBN structure

The prefix now independently shows:

> a U.S. registrant with only a **10-number block**.

These three facts align naturally with an author-controlled micro-imprint/self-publisher model:

1. very small U.S. ISBN allocation;
2. author shown directly as publisher on Amazon;
3. a one-title public imprint shown in downstream distribution feeds.

This is much more consistent with a micro-publisher or author-created imprint than with a traditional high-output Christian publishing house.

But it still does not answer the final legal/bibliographic identity question:

> **Who does Bowker / the Global Register actually name as registrant for `979-8-9961673`?**

That remains the key missing primary object.

---

## 8. Global Register of Publishers: the exact lookup we still need

The International ISBN Agency's Global Register of Publishers says anyone can perform simple searches by:

- ISBN prefix;
- complete ISBN;
- publisher name.

It explicitly notes that some small publishers may receive single ISBNs rather than full blocks.

Official search guidance:
- https://grp.isbn-international.org/node/357

The target queries are therefore:

- complete ISBN: `9798996167302`
- prefix: `979-8-9961673`
- publisher: `But God Press`
- publisher: `Steven Lawson`

At the time of this audit the GRP endpoint was not reliably returning an actionable result through the available noninteractive retrieval paths, and the interactive browser route was unavailable because the connected browser-automation wallet had no balance.

Therefore the **registrant name remains unresolved**, not guessed.

## 9. Publisher-of-record implications

Bowker says the U.S. ISBN Agency database establishes the publisher of record associated with each prefix.

That makes the eventual GRP/Bowker registrant result highly probative.

Possible outcomes:

### A. Registrant = Steven Lawson

This would provide direct publisher-of-record support for the current Amazon field and strongly indicate `But God Press` is an imprint/label under Lawson's publisher identity.

### B. Registrant = But God Press

This would establish the imprint itself as Bowker's publisher-of-record name; the remaining question would then be who legally owns or operates it.

### C. Registrant = another person/entity

That would materially change the publishing-chain hypothesis and require tracing that registrant.

Until the actual record is acquired, the corpus must not choose among A/B/C.

---

## 10. Scale conclusion

The allocation architecture itself is now established:

> **U.S. registrant prefix `979-8-9961673` / seven-digit registrant / one-digit publication element / ten-number capacity.**

This is an **ultra-small publisher allocation** in structural terms.

Safe article wording:

> The book's ISBN is not merely a generic retail identifier. Current International ISBN Agency range rules parse it as `979-8-9961673-0-2`: a U.S. publisher prefix with a seven-digit registrant element, leaving only a one-digit publication element. The ISBN standard assigns longer registrant elements to lower-output publishers, and this prefix structurally allows ten publication numbers. That independently supports the picture of a very small/self-publishing-style operation. It does not yet tell us whether Bowker names the registrant as Steven Lawson, But God Press, or another entity.

Unsafe:

- “The ISBN proves Lawson owns But God Press.”
- “But God Press has published exactly ten books.”
- “Lawson bought ten ISBNs.”
- “All ten numbers have been used.”

None of those follows from the prefix alone.

---

## 11. Next acquisition targets

1. Obtain the Global Register / Bowker publisher record for `9798996167302` or `979-8-9961673`.
2. Search the other nine possible publication elements under the prefix for assigned/live titles, without assuming every slot is or will be used.
3. Acquire the physical copyright page, where ISBN.org says ISBN and publisher information are normally printed.
4. Search U.S. Copyright Office records for the title/author/claimant.
5. Search Library of Congress / library catalog records for publisher and copyright statement.
6. Correlate any registrant name with state DBA/corporate records only after the name is known.

## Research conclusion

> **THE ISBN ITSELF NOW PROVIDES INDEPENDENT STRUCTURAL EVIDENCE THAT *MERCY IN THE WILDERNESS* COMES FROM A VERY SMALL U.S. PUBLISHER ALLOCATION. CURRENT INTERNATIONAL ISBN RANGE RULES PARSE `9798996167302` AS `979-8-9961673-0-2`: A SEVEN-DIGIT REGISTRANT ELEMENT WITH ONLY A ONE-DIGIT PUBLICATION ELEMENT, I.E. TEN POSSIBLE PUBLICATION IDENTIFIERS IN THAT BLOCK. INTERNATIONAL ISBN GUIDANCE EXPLICITLY STATES THAT LONGER REGISTRANT ELEMENTS CORRESPOND TO LOWER ANTICIPATED PUBLISHER OUTPUT. THIS STRONGLY REINFORCES THE AUTHOR-CONTROLLED/MICRO-PUBLISHER MODEL ALREADY SUGGESTED BY AMAZON'S `PUBLISHER: STEVEN LAWSON` FIELD AND DOWNSTREAM `BUT GOD PRESS` METADATA. THE REGISTRANT'S ACTUAL NAME REMAINS THE CRITICAL UNRESOLVED PRIMARY RECORD.**
