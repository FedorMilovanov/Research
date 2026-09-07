# Source Verification Ledger — Primary Puritan / Confessional / Modern Facts

**Status:** RESEARCH CONTROL / PRE-PUBLICATION VERIFICATION  
**Date:** 2026-09-07  
**Purpose:** identify which sources are strong enough for direct quotation, which are safe mainly for paraphrase, and which modern empirical claims remain eligible for main-text use.

> **GLOBAL EVIDENCE POLICY CONTROL (2026-09-08):** repository evidence semantics are governed by `data/repository-evidence-policy-v2.json` and current `AGENT_RULES.md`. Historical labels `P1/P2/C1/M1/S` below are preserved only as **local source-role / verification-provenance labels**. They are **not** repository `evidenceClass` values. Any source actually transferred toward publication must also carry global `evidenceClass`, `accessState`, `locatorState`, `rightsState`, `publicationState`, and applicable HOLDs.

---

## 0. Historical local verification-role labels — not repository evidenceClass

- **P1 — PRIMARY/NEAR-PRIMARY VERIFIED:** original/early text, institutional transcription, scan or authoritative author/archive presentation; suitable for direct quotation after final wording check.
- **P2 — RELIABLE HISTORICAL EDITION/TRANSCRIPTION:** suitable for paraphrase and usually quotation, but final quote should be compared against a scan/critical edition where feasible.
- **C1 — CONFESSIONAL PRIMARY TEXT VERIFIED:** stable text of 1689 LBCF from multiple presentations.
- **M1 — MODERN OFFICIAL PRIMARY DATA:** official institution/report page; strong for exact contemporary factual claim with scope/sample stated.
- **S — SECONDARY:** commentary/orientation; do not prefer over primary text for direct quotation.

### Global transfer rule

For publication-bound sources, use only repository-global values:

- `evidenceClass`: `A1 | A2 | A3 | B1 | C | D`;
- `accessState`: `FULL_OBJECT_VERIFIED | PARTIAL_OBJECT | CATALOG_ONLY | LINK_ONLY | NOT_ACQUIRED`;
- `locatorState`: `EXACT_LOCATOR_VERIFIED | COARSE_LOCATOR_ONLY | LOCATOR_MISSING`;
- `rightsState`: `PUBLICATION_ELIGIBLE | STORAGE_ONLY | PRIVATE_STUDY_ONLY | PERMISSION_REQUIRED | RIGHTS_UNKNOWN`;
- `publicationState`: `PROMOTE | REFERENCE | SUPERSEDED | BLOCKED`;
- HOLDs: `EVIDENCE_HOLD | LOCATOR_HOLD | ARCHIVE_HOLD | RIGHTS_HOLD | PUBLICATION_HOLD`.

A local `P1`, `P2`, `C1`, or `M1` therefore never substitutes for the global fields.

---

# 1. Thomas Watson — *The Doctrine of Repentance*

## Status: P1 VERIFIED

Primary digital text:

- Early English Books Online / University of Michigan Text Creation Partnership
- Title: *The doctrine of repentance, useful for these times by Tho. Watson...*
- Author: Thomas Watson
- Publication: London, 1668
- Stable item: `A65293.0001.001`

Verified URL:
- https://quod.lib.umich.edu/e/eebo/A65293.0001.001/1:7.2?rgn=div2&view=fulltext

Verified textual points in the primary transcription:

- “Sorrow for Sin” is an ingredient of repentance.
- Watson explicitly distinguishes true/godly sorrow from false sorrow.
- He says godly sorrow is more for the **offence** than the punishment.
- He gives the thief-caught illustration: sorrow at being taken/punished is not the same as repentance.
- He explicitly says not all have the same degree/visible expression of sorrow.
- He distinguishes rational/spiritual sorrow from abundance of visible tears.
- He connects godly sorrow in appropriate cases with restitution.
- He says true sorrow is abiding rather than a momentary emotional shower.

### Publication decision

**Direct quote eligible**, but quote from the EEBO transcription and preserve archaic spelling only if desired. For readable modern prose, paraphrase and cite primary text.

### Important guard

Do not reduce Watson’s doctrine of repentance to “must cry enough.” The primary text itself rejects equal degrees of visible tears as a universal criterion.

---

# 2. Richard Baxter — *A Christian Directory*

## Status: P1/P2 VERIFIED

Primary digital source:

- Early English Books Online / University of Michigan
- Item `A26892.0001.001`

Verified URL for duties of children:
- https://quod.lib.umich.edu/e/eebo/A26892.0001.001/1:6.13?rgn=div2&view=fulltext

Verified from the institutional transcription:

- Baxter directly addresses children as responsible moral hearers.
- He tells them to love parental company and not prefer idle playfellows to parents.
- He explicitly acknowledges that parents may “chide,” “restrain,” and “correct” without this cancelling the child’s duty.

Additional historical transcription/edition used in corpus:
- https://classic-literature.net/richard-baxter-1615-1691/a-christian-directory-part-2-christian-economics/

This edition contains the fuller material used in modules `48` and `58` regarding:

- parental love and government;
- avoiding excessive terror/strangeness;
- avoiding overindulgence;
- watching lying, railing/ribald speech and corrupt company.

### Publication decision

Use EEBO **whenever a direct quotation is available there**. Use modern/historical transcription for navigation/paraphrase, then verify exact quote against EEBO or a scan before publication.

---

# 3. John Owen — *Mortification*, *Of Temptation*, *Indwelling Sin*, *Dominion of Sin and Grace*

## Status: P2 VERIFIED / STRONG HISTORICAL TRANSCRIPTION

Primary working source:
- Christian Classics Ethereal Library (CCEL) transcriptions of Owen’s works.

Verified pages include:

- *Mortification of Sin*: https://ccel.org/ccel/owen/mort.i.v.html
- *Of Temptation*: https://www.ccel.org/ccel/owen/temptation.i.xi.html
- additional corpus pages under `temptation.i.vii–x`;
- *Dominion of Sin and Grace*: CCEL pages already recorded in modules `57`.

Verified exact major Owen line suitable for publication after edition check:

> “be killing sin or it will be killing you”

The CCEL text places it inside Owen’s argument that even true believers must make daily mortification their work.

Verified conceptual controls:

- believers must mortify remaining sin continually;
- perseverance doctrine must not be abused as security for a particular temptation;
- self-reasoning and isolated strenuous acts are insufficient if the wider life is negligent;
- Owen’s temptation framework treats particular lusts/occasions and watchfulness as central.

### Publication decision

**Paraphrase freely with citation.** If quoting word-for-word in final article, compare against a standard modern critical/printed edition or page scan where practical.

### Guard

Do not make Owen sound as though he teaches salvation by self-control. His mortification is explicitly Spirit-dependent and addressed to believers.

---

# 4. Thomas Brooks — *Precious Remedies Against Satan’s Devices*

## Status: P2 VERIFIED / SCAN AVAILABLE

Verified sources:

- scanned/public PDF edition: https://www.apuritansmind.com/wp-content/uploads/FREEEBOOKS/PreciousRemediesAgainstSatansDevices-ThomasBrooks.pdf
- Google Books historical edition: https://books.google.com/books/about/Precious_Remedies_Against_Satan_s_Device.html?id=WypMAAAAYAAJ
- Banner of Truth table of contents: https://banneroftruth.org/us/store/christian-living/precious-remedies-against-satans-devices/

Verified title/device structure:

1. presenting the bait and hiding the hook;
2. painting sin with virtue’s colours;
3. extenuating/lessening sin;
4. showing the sins of the best men while hiding their sorrow/repentance;
6. persuading the soul that repentance is easy/later;
8. encouraging boldness near occasions of sin;
9. emphasizing difficulties of the path of holiness;
12. wicked company.

The scanned text explicitly gives the “bait / hide the hook” formulation and contrasts immediate sweetness/profit with hidden wrath/misery.

### Publication decision

This is one of the strongest Puritan sources for direct thematic quotation. Prefer the scanned/historical edition for exact wording; use Banner of Truth mainly for bibliographic/table-of-contents confirmation.

---

# 5. John Flavel — *Keeping the Heart / Saint Indeed*

## Status: P2 VERIFIED

Verified CCEL pages:

- temptation progression: https://ccel.org/ccel/flavel/saintindeed/saintindeed.v.ii.html
- pleasure of sin / keeping heart under temptation: https://www.ccel.org/ccel/flavel/saintindeed.v.iii.ix.html
- PDF edition: https://www.ccel.org/f/flavel/keeping/cache/keeping.pdf

Verified conceptual content:

- an unguarded heart is easily surprised;
- temptation is easier checked in earlier motions than after gaining strength;
- Flavel describes a sequence from object → appetite → mental consultation → choice of will → fuller engagement;
- he openly acknowledges the temptation argument from pleasure and answers it by bringing the full consequences/end into view.

### Publication decision

Excellent for paraphrase and one short direct quote after page/edition check.

### Guard

Do not convert Flavel’s pastoral sequence into a universal scientific five-stage model.

---

# 6. Richard Sibbes — *The Bruised Reed*

## Status: P2 VERIFIED

Historical scans/metadata:

- Google Books edition: https://books.google.com/books/about/The_Bruised_Reed_and_Smoking_Flax.html?id=Hzw3AAAAMAAJ
- alternate digitized edition: https://books.google.com/books/about/The_Bruised_Reed_and_Smoking_Flax.html?id=45W7Se5darAC

The historical table of contents itself verifies the themes used in module `62`:

- grace is little at first;
- Christ will not quench small and weak beginnings;
- tenderness required in ministers toward young beginners;
- governors should be tender toward weak ones;
- infirmities are not sufficient cause of discouragement.

### Publication decision

Use Sibbes chiefly as a counterweight against crushing a weak, bruised, genuinely struggling child/believer. Direct quotations should be checked in the scan, not lifted from a modern summary site.

### Guard

Sibbes’ tenderness is not evidence that persistent defended rebellion should be called mere “weakness.”

---

# 7. John Bunyan — *The Barren Fig-Tree*

## Status: P2 VERIFIED

Verified full-text source:
- https://johnbunyan.org/en/the-barren-fig-tree/

The edition identifies the work as Bunyan’s 1682 treatise and explicitly explains the central image as the fruitless/formal professor in the gospel church/vineyard.

Verified themes:

- visible profession can exist without spiritual fruit;
- religious privilege/proximity does not itself prove grace;
- the treatise repeatedly warns against barren profession and abuse of means.

### Publication decision

Useful for a section on **false/formal profession**, not as a direct policy text for unbaptized children.

### Strong guard

Do not label every church-attending unconverted child Bunyan’s “barren professor.” His image concerns religious profession/visible church placement in his own ecclesial argument.

---

# 8. Charles Spurgeon — “Do Not Sin Against the Child”

## Status: P1/P2 VERIFIED FROM SPURGEON LIBRARY

Authoritative institutional presentation:
- https://www.spurgeon.org/sermons/do-not-sin-against-the-child

Also CCEL:
- https://www.ccel.org/ccel/spurgeon/sermons14.liii.html

Verified points directly in the sermon:

- Spurgeon condemns the policy of leaving children unconverted until later life rather than seeking their conversion now;
- he explicitly tells parents not to be over-angry and cites the parental non-provocation side of the household commands;
- he immediately also warns against over-indulgence;
- he calls for “proper subjection” of children while warning against both too much and too little rebuke;
- he says child professions should not be received without examination;
- he requires the same **real** repentance and faith in kind as for adults, while warning against unnecessary suspicion and adultized expectations;
- he explicitly says mistaking a child’s terror for repentance or religious joy for faith can educate the child in self-deception.

### Publication decision

**High-priority source.** Suitable for direct quotation from Spurgeon Library, within copyright/public-domain constraints and normal quotation length.

---

# 9. 1689 London Baptist Confession

## Status: C1 VERIFIED

Reliable current presentations cross-checked:

- https://baptistconfession.org/
- https://rbs.org/2lbc
- Wikisource historical text: https://en.wikisource.org/wiki/1689_Baptist_Confession_of_Faith

Key verified controls:

### 19.4
Israel’s judicial laws expired with that polity; only general equity remains morally useful.

### 19.5
The moral law binds **all**, justified and others, because of God the Creator’s authority.

### 19.6–7
The law remains useful, including to restrain corruption and reveal duty; these uses sweetly comply with gospel grace.

### 15
Saving repentance is evangelical grace involving Spirit-given sense of sin, faith in Christ, godly sorrow, detestation, prayer for pardon/strength and purposeful endeavor; particular known sins require particular repentance.

### 17
True believers may fall into grievous sins, continue for a time, harden hearts/wound consciences/scandalize others, yet be renewed in repentance and preserved.

### Publication decision

Use as confessional synthesis, not as substitute for biblical exegesis.

---

# 10. Modern empirical facts retained for main-text eligibility

> The historical `M1` wording below is a local role label only. Global source-class/state fields govern publication transfer.

## WHO/HBSC digital contact — local M1 VERIFIED

Official WHO 2024 report/news page:
- https://www.who.int/europe/news-room/25-09-2024-teens--screens-and-mental-health

Scope:
- nearly 280,000 adolescents;
- ages 11, 13, 15;
- 44 countries/regions in Europe, Central Asia and Canada;
- data collected 2022.

Verified:
- 36% reported continuous online contact with friends/others;
- 11% classified problematic social-media users, up from 7% in 2018;
- 15-year-old girls highest continuous-online-contact figure at 44%.

Guard:
- `continuous online contact` is not itself sinful/problematic use.

---

## Pew U.S. teen internet use — local modern survey VERIFIED

Pew 2024:
- https://www.pewresearch.org/internet/2024/12/12/teens-social-media-and-technology-2024/

Scope:
- 1,391 U.S. teens ages 13–17;
- survey Sept.–Oct. 2024;
- probability-based panel, weighted to U.S. teens living with parents.

Verified:
- 96% use internet daily;
- nearly half say they are online almost constantly;
- 95% report smartphone access.

Guard:
- U.S.-specific; do not universalize globally.

Global transfer state when retained:
- `evidenceClass`: `B1`;
- `accessState`: `FULL_OBJECT_VERIFIED`;
- `locatorState`: `COARSE_LOCATOR_ONLY` pending exact table/method locator for a retained numerical claim;
- `rightsState`: `PUBLICATION_ELIGIBLE` for factual paraphrase/citation subject to product policy;
- `publicationState`: `REFERENCE`;
- `holds`: `[LOCATOR_HOLD]` until selected exact statistic is pinned.

---

## UNICEF 2026 tech-facilitated sexual exploitation/abuse — local M1 VERIFIED

Official report/press release:
- https://www.unicef.org/innocenti/reports/through-childrens-eyes
- https://www.unicef.org/press-releases/1-5-children-across-21-countries-have-experienced-tech-facilitated-sexual

Publication: September 2026.

Scope:
- approximately 21,000 internet-using children ages 12–17;
- 21 countries;
- survey data largely collected 2020–2025.

Verified:
- estimated 20 million, almost 1 in 5, experienced at least one form of technology-facilitated sexual exploitation/abuse in one year across those countries;
- more than half occurred on mainstream social media platforms;
- less than 1% were reported to police/social worker/helpline;
- more than 4 in 10 disclosed to no one.

Critical guard:
- this is **victimization/exploitation**, not “1 in 5 children committed sexual sin.”
- result applies to the covered countries/sample/model, not automatically the entire world.

---

## NCMEC financial sextortion — local M1 VERIFIED

Official NCMEC:
- https://www.ncmec.org/blog/2026/ncmec-releases-new-sextortion-data-2025
- https://ncmec.org/gethelpnow/cybertipline/cybertiplinedata

Verified for 2025:
- more than 50,000 reports of financially motivated sextortion;
- average 137 reports per day;
- NCMEC states many reports involve teenage boys targeted with fake social-media accounts;
- at least three dozen U.S. teenage boys known by NCMEC to have died by suicide in connection with this crime.

Critical guard:
- reports ≠ population prevalence;
- association with suicide cases must not be used as inevitability rhetoric.

---

## Children’s Commissioner for England — pornography exposure — local M1 VERIFIED

Official report pages:
- https://www.childrenscommissioner.gov.uk/resource/a-lot-of-it-is-actually-just-abuse-young-people-and-pornography/
- https://www.childrenscommissioner.gov.uk/resource/pornography-and-harmful-sexual-behaviour/

Original survey/report scope:
- over 1,000 young people ages 16–21 plus teen focus groups in England/UK context.

Verified findings reported by Commissioner:
- average reported first exposure age 13;
- 27% by age 11;
- 10% by age 9;
- mainstream social platforms were important exposure pathways, not only adult sites.

Guard:
- retrospective national sample; not universal global prevalence.
- avoid causal overstatement from observational links.

---

## Australian eSafety Commissioner 2026 — AI assistants/companions

Official regulator research:
- https://www.esafety.gov.au/research/talking-to-machines-childrens-experiences-with-ai-assistants-and-companions
- https://www.esafety.gov.au/industry/basic-online-safety-expectations/ai-services/findings-october-2025

Verified scope/results recorded in module `18`:
- demographically representative survey of 1,950 Australian children ages 10–17;
- 79% had ever used an AI assistant or AI companion;
- 8% had ever used an AI companion specifically;
- 54% of users reported at least one companion-type purpose;
- 22% reported chatting about feelings/challenges;
- 20% sought mental-health/wellbeing advice;
- 20% reported at least one potentially inappropriate/harmful interaction;
- 32% had shared personal or potentially sensitive information;
- prior eSafety transparency findings for teen users 13–17 included 4% reporting chat about kissing/sex and 3% sexual image/video output.

### Global evidence state

- `evidenceClass`: `A2`;
- `accessState`: `FULL_OBJECT_VERIFIED`;
- `locatorState`: `COARSE_LOCATOR_ONLY`;
- `rightsState`: `PUBLICATION_ELIGIBLE` for factual paraphrase/citation subject to product policy;
- `publicationState`: `REFERENCE`;
- `holds`: `[LOCATOR_HOLD]` for any exact quotation/table-level claim until the final retained claim is pinned.

### Publication guard

Use to establish a **new private conversational pathway**, not to claim that most teens have AI romantic partners or that AI use itself is sinful.

---

## Pew Research Center 2026 — teen chatbot use

Source:
- https://www.pewresearch.org/internet/2026/02/24/how-teens-use-and-view-ai/

Verified scope/results recorded in module `18`:
- U.S. teens ages 13–17, survey Sept.–Oct. 2025;
- 64% had used AI chatbots;
- 16% reported casual-conversation use;
- 12% reported emotional-support/advice use.

### Global evidence state

- `evidenceClass`: `B1`;
- `accessState`: `FULL_OBJECT_VERIFIED`;
- `locatorState`: `COARSE_LOCATOR_ONLY`;
- `rightsState`: `PUBLICATION_ELIGIBLE` for factual paraphrase/citation subject to product policy;
- `publicationState`: `REFERENCE`;
- `holds`: `[LOCATOR_HOLD]` for exact table-level publication use.

### Publication guard

Do not infer emotional dependence, romantic attachment, or sexual use from the 12% emotional-support/advice figure.

---

## Cyber dating violence systematic review/meta-analysis — publication-eligible reference with locator hold

Source:
- https://pubmed.ncbi.nlm.nih.gov/39283366/

Verified at abstract/metadata level:
- systematic review/meta-analysis;
- 49 studies;
- cyber dating violence perpetration/victimization associated with multiple offline dating-violence factors and mental-health symptoms.

### Global evidence state

- `evidenceClass`: `B1`;
- `accessState`: `PARTIAL_OBJECT`;
- `locatorState`: `COARSE_LOCATOR_ONLY`;
- `rightsState`: `PUBLICATION_ELIGIBLE` for ordinary paraphrase/citation subject to product policy;
- `publicationState`: `REFERENCE`;
- `holds`: `[LOCATOR_HOLD]` for exact effect-size claims.

### Publication guard

Use the category-level finding only unless full-text tables/effect sizes are reopened and pinned.

---

## 2026 U.S. national teen sexting / nonconsensual sharing / sextortion study

Source:
- https://pubmed.ncbi.nlm.nih.gov/41653178/

Verified at abstract/metadata level:
- national U.S. sample;
- N=3,466 adolescents ages 13–17;
- examines sexting and harms including nonconsensual sharing and sextortion.

### Global evidence state

- `evidenceClass`: `B1`;
- `accessState`: `PARTIAL_OBJECT`;
- `locatorState`: `COARSE_LOCATOR_ONLY`;
- `rightsState`: `PUBLICATION_ELIGIBLE` for ordinary paraphrase/citation subject to product policy;
- `publicationState`: `REFERENCE`;
- `holds`: `[LOCATOR_HOLD]` until exact prevalence/denominator tables are retrieved if numerical claims beyond the sample size are retained.

### Publication guard

Use it to support the existence of the coercive/nonconsensual layer; do not invent prevalence beyond the verified abstract/metadata.

---

# 11. Publication quote/source policy after verification

### Direct-quote preferred sources

1. Scripture.
2. 1689 text.
3. Watson EEBO.
4. Baxter EEBO where exact section available.
5. Spurgeon Library.
6. historical/scan editions of Brooks/Sibbes/Bunyan/Flavel/Owen after final wording check.

### Paraphrase preferred

- Puritan argument when wording varies by edition;
- modern commentary summaries;
- empirical studies unless exact statistic is the point.

### Never quote as primary authority

- blog summaries when original source is available;
- modern paraphrase editions if historical text is readily accessible;
- AI-generated summaries;
- psychology terminology as doctrinal authority.

### Mandatory global transfer gate

Before any retained source crosses into `gb-is-my-strength`, record/check its current global evidence state. A source being present in Research or labeled locally `P1/P2/M1` is not itself publication authorization.

---

# 12. Final source-quality conclusion

The core theological/pastoral thesis no longer depends on fragile modern psychology.

It is independently supported by:

- Scripture in context;
- 1689 confessional synthesis;
- multiple independent Puritan/Reformed pastoral witnesses across the seventeenth–nineteenth centuries;
- modern official/high-quality data only where contemporary scale, digital pathways and safeguarding claims require it.

The 2026 delta adds two narrow contemporary pathways without reopening the governing framework:

1. AI assistants/companions as a private conversational environment;
2. coercive sexting/cyber dating violence as a distinct layer between voluntary sexting and stranger sextortion.

Remaining source work before publication should be **selected-claim locator/quote precision**, not a search for a new governing framework.
