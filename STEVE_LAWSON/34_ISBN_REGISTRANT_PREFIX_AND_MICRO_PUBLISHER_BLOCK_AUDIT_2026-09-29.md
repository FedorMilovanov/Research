# Steven J. Lawson — ISBN registrant prefix / micro-publisher block audit

**Snapshot:** 2026-09-29  
**Status:** `OFFICIAL ISBN STRUCTURE VERIFIED / U.S. REGISTRANT = 979-8-9961673 / 10-NUMBER CAPACITY / PRINT + EBOOK SLOTS 0–1 PRIMARY-CONFIRMED / REGISTRANT NAME STILL UNRESOLVED`

## 1. Executive finding

The print ISBN for *Mercy in the Wilderness* is:

- `9798996167302`

Using the current range rules distributed from the **International ISBN Agency**, that number parses as:

> **979-8-9961673-0-2**

where:

- `979` = ISBN prefix element;
- `8` = United States registration group;
- `9961673` = seven-digit registrant/publisher element;
- `0` = one-digit publication element;
- `2` = check digit.

The International ISBN standard explicitly ties registrant-element length to anticipated publisher output: **larger publishers receive shorter registrant elements; smaller-output publishers receive longer ones.**

A seven-digit U.S. registrant element is therefore at the smallest-output end of the ISBN allocation structure. Because only one digit remains for the publication element, this particular registrant prefix can structurally identify **10 publication numbers: 0–9**.

A later-acquired photograph of the book's copyright page now confirms that the first two slots are actually assigned:

- publication element `0` → print ISBN `979-8-9961673-0-2`;
- publication element `1` → ebook ISBN `979-8-9961673-1-9`.

Primary-object audit:
- `35_BOOK_COPYRIGHT_PAGE_PRIMARY_OBJECT_2026-09-29.md`

Thus this is not merely a theoretical prefix decomposition: the physical book itself uses the prefix consistently across two format-specific ISBNs.

It still does **not** by itself reveal whether the registrant's legal/publisher-of-record name is `Steven Lawson`, `But God Press`, or another entity.

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

Raw print ISBN:

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

### Print publication element

After `979` + `8` + seven-digit registrant, one digit remains before the final check digit:

> Publication element = `0`

### Print check digit

> `2`

### Print result

> **ISBN 979-8996167302 = 979-8-9961673-0-2**

### Ebook result — primary object

The book's own copyright page states:

> **Ebook ISBN: 979-8-9961673-1-9**

Direct photographed object:
- https://pbs.twimg.com/media/HSs94M9XkAAocYE?format=png&name=small

This independently validates the registrant boundary: the same prefix `979-8-9961673` is followed by publication element `1` and its proper check digit `9` for a second format.

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

For this prefix:

- prefix = 3 digits (`979`)
- group = 1 digit (`8`)
- registrant = 7 digits (`9961673`)
- check digit = 1 digit

That leaves exactly **one digit** for the publication element.

A one-digit decimal publication element has ten possible values:

> `0,1,2,3,4,5,6,7,8,9`

Thus the publisher prefix `979-8-9961673` structurally supports **10 ISBN publication identifiers**.

The first two are now primary-object confirmed as print (`0`) and ebook (`1`). Slots `2–9` remain unverified and must not be described as assigned or unused merely from web-search silence.

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

The presence of a 10-number block does not prove Lawson purchased it personally or when it was acquired. It proves the scale and structure of the registrant allocation. The copyright page proves two format ISBNs were assigned under it, not that all ten slots have been or will be used.

---

## 7. Primary copyright page changes the evidentiary model

The acquired copyright page says:

- Copyright © 2026 by **Steven Lawson**;
- **Published by But God Press, 2026**;
- Cover design and layout by **Caleb Faires**;
- Print ISBN `979-8-9961673-0-2`;
- Ebook ISBN `979-8-9961673-1-9`.

Primary-object audit:
- `35_BOOK_COPYRIGHT_PAGE_PRIMARY_OBJECT_2026-09-29.md`

This proves `But God Press` is not merely a downstream retailer-data artifact: it is the publisher/imprint name printed inside the work.

It also proves Steven Lawson is the named copyright holder.

What it still does **not** prove is who Bowker identifies as the publisher-of-record for the prefix or who legally owns/operates the `But God Press` name.

---

## 8. Why this matters for `But God Press` vs. `Steven Lawson`

The evidence stack now has three distinct layers:

### Primary book object
- Copyright holder: **Steven Lawson**
- Published by: **But God Press**

### Amazon current state
- Publisher: **Steven Lawson**

### Broad independent distribution feeds
- Publisher: **But God Press**

### ISBN structure
- a U.S. registrant with only a **10-number block**;
- at least two format-specific numbers already assigned inside the book.

These facts align naturally with an author-controlled micro-imprint/self-publisher model.

But they still do not answer the final bibliographic identity question:

> **Who does Bowker / the Global Register actually name as registrant for `979-8-9961673`?**

That remains the key missing primary object.

---

## 9. Global Register of Publishers: the exact lookup we still need

The International ISBN Agency's Global Register of Publishers says anyone can perform simple searches by:

- ISBN prefix;
- complete ISBN;
- publisher name.

Official search guidance:
- https://grp.isbn-international.org/node/357

The target queries are:

- complete print ISBN: `9798996167302`
- complete ebook ISBN: `9798996167319`
- prefix: `979-8-9961673`
- publisher: `But God Press`
- publisher: `Steven Lawson`

At the time of this audit the GRP endpoint was returning HTTP 503 through available noninteractive retrieval paths, and the connected interactive browser automation could not run because its wallet had no balance.

Therefore the **registrant name remains unresolved**, not guessed.

## 10. Publisher-of-record implications

Bowker says the U.S. ISBN Agency database establishes the publisher of record associated with each prefix.

Possible outcomes remain:

### A. Registrant = Steven Lawson

This would directly support the current Amazon field and strongly indicate `But God Press` is an imprint/label under Lawson's publisher identity.

### B. Registrant = But God Press

This would establish the imprint itself as Bowker's publisher-of-record name; the remaining question would be who legally owns or operates it.

### C. Registrant = another person/entity

That would materially change the publishing-chain hypothesis and require tracing that registrant.

Until the actual record is acquired, the corpus must not choose among A/B/C.

---

## 11. Ebook status: assigned ISBN ≠ demonstrated public release

The copyright page assigns the ebook ISBN `9798996167319`, but targeted current searches do not locate an actual Lawson ebook storefront/catalog object on Kobo, Apple Books, Google Play Books, Barnes & Noble ebook, or ordinary indexed web results.

Sept. 21 reporting likewise observed that only the paperback appeared publicly available at that time.

Source:
- https://evangelicaldarkweb.org/2026/09/21/steve-lawson-returns-with-new-book/

Therefore the precise status is:

> **EBOOK ISBN ASSIGNED IN PRIMARY BOOK OBJECT / PUBLIC EBOOK RELEASE NOT YET LOCATED.**

Possible explanations — planned edition, delayed edition, withdrawn edition, private metadata, or unindexed distribution — remain hypotheses only.

---

## 12. Scale conclusion

The allocation architecture is established:

> **U.S. registrant prefix `979-8-9961673` / seven-digit registrant / one-digit publication element / ten-number capacity.**

Primary evidence also establishes at least two assigned formats:

- `...0-2` print;
- `...1-9` ebook.

This is an **ultra-small publisher allocation** in structural terms.

Safe article wording:

> Current International ISBN Agency range rules parse Lawson's print ISBN as `979-8-9961673-0-2`: a U.S. publisher prefix with a seven-digit registrant element, leaving only a one-digit publication element and therefore ten possible publication numbers. The book's own copyright page confirms the next number in that same block as its ebook ISBN. The standard assigns longer registrant elements to lower-output publishers, which independently supports the picture of a very small author-controlled/micro-publisher operation. The unresolved question is whether Bowker names the registrant as Steven Lawson, But God Press, or another entity.

Unsafe:

- “The ISBN proves Lawson owns But God Press.”
- “But God Press has published exactly ten books.”
- “Lawson bought ten ISBNs.”
- “All ten numbers have been used.”
- “Slots 2–9 are unused.”

None of those follows from the evidence currently acquired.

---

## 13. Next acquisition targets

1. Obtain the Global Register / Bowker publisher record for `9798996167302`, `9798996167319`, or prefix `979-8-9961673`.
2. Search publication elements `2–9` only as discovery leads, with a positive-control catalog before interpreting silence.
3. Continue U.S. Copyright Office CPRS lookup by title/ISBN/author; a direct API endpoint has now been identified but its JSON body still needs extraction through a compatible client.
4. Search Library of Congress / library catalog records for publisher/copyright statements.
5. Determine whether the assigned ebook was ever actually released.
6. Correlate any registrant name with state DBA/corporate records only after the name is known.

## Research conclusion

> **THE ISBN AND PRIMARY COPYRIGHT PAGE NOW REINFORCE EACH OTHER. *MERCY IN THE WILDERNESS* USES THE TINY U.S. PUBLISHER PREFIX `979-8-9961673`; ITS PRINT FORMAT OCCUPIES PUBLICATION ELEMENT `0`, AND THE BOOK ITSELF ASSIGNS ELEMENT `1` TO AN EBOOK. THE SAME PRIMARY PAGE NAMES STEVEN LAWSON AS COPYRIGHT HOLDER AND BUT GOD PRESS AS PUBLISHER. THIS STRONGLY SUPPORTS AN AUTHOR-CONTROLLED MICRO-IMPRINT/SELF-PUBLISHING STRUCTURE, WHILE THE BOWKER/GRP REGISTRANT NAME AND LEGAL OWNERSHIP OF THE IMPRINT REMAIN UNRESOLVED.**
