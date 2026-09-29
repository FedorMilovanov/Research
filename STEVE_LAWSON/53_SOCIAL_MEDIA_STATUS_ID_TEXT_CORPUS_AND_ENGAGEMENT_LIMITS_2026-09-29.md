# Steven J. Lawson — archived X/Twitter status-ID text corpus / engagement-limit audit

**Snapshot:** 2026-09-29  
**Status:** `ORIGINAL STATUS IDS RECOVERED / POST DATES RECONSTRUCTABLE / MULTIPLE TEXTS MIRROR-CONFIRMED / OWN ENGAGEMENT METRICS NOT RECOVERED / BOOK CLAIM NOT YET EMPIRICALLY QUANTIFIED`

## 1. Why this audit exists

In *Mercy in the Wilderness*, Lawson reportedly says that provocative social-media posts received far more likes/reposts than pastoral and encouraging posts. That statement matters because it proposes a concrete platform-reinforcement mechanism for his own increasingly combative public posture.

Canonical causal audit:
- `52_LAW_GRACE_RETRIBUTION_RESTORATION_PUBLIC_TONE_SELF_DIAGNOSIS_AUDIT_2026-09-29.md`

The obvious next question is empirical:

> Can the historical X/Twitter record independently verify Lawson's claim?

A first reconstruction pass now shows that **substantial portions of the text/status-ID corpus can be recovered**, even where the original X page is no longer indexed. However, the pass has **not** recovered Lawson's own contemporaneous like/repost counts with sufficient reliability.

Therefore the present result is a **text/provenance corpus**, not a quantitative engagement study.

---

## 2. Methodological rule: mirror engagement is not Lawson engagement

Many Lawson tweets survive because other Facebook, Instagram, Reddit, blog or quote accounts copied them and retained the original Twitter status URL.

Those mirror pages often display their own:

- likes;
- comments;
- shares;
- reactions.

Those numbers belong to the **mirror post**, not to Lawson's original tweet.

### Hard rule

> **NEVER TRANSFER MIRROR ENGAGEMENT COUNTS TO LAWSON'S ORIGINAL STATUS.**

This matters because the research question is specifically whether *Lawson's* provocative tweets outperformed *Lawson's* pastoral tweets.

A mirror going viral years later cannot answer that question.

---

## 3. Original status IDs are still valuable even when X is unavailable

Twitter/X uses Snowflake IDs. The ID itself contains the creation timestamp.

Twitter/X's own engineering announcement explains that Snowflake IDs combine:

- timestamp;
- worker number;
- sequence number.

Official historical source:
- https://blog.x.com/engineering/en_us/a/2010/announcing-snowflake

For production-era Twitter Snowflakes, the timestamp may be reconstructed with:

`timestamp_ms = (snowflake_id >> 22) + 1288834974657`

Independent technical reference:
- https://techconverter.me/twitter-snowflake-id-to-timestamp

Thus when a third-party mirror preserves a full original URL such as:

`twitter.com/drstevenjlawson/status/<ID>`

we can recover the posting time independently of the mirror's own upload date.

This does **not** recover engagement counts.

---

## 4. Control group: pastoral / Christ-centered / encouraging Lawson posts

The current pass recovered multiple original Lawson status IDs through third-party mirrors.

### 4.1. Christ as life's greatest decision/joy/wisdom

Original status ID:
- `1301283422413950978`

Snowflake timestamp:
- **2020-09-02 22:18:39.237 UTC**

Mirror preserves the original English text and source URL:

> “To believe in Christ is life’s greatest decision. To know Him is life’s greatest joy. To obey Him is life’s greatest wisdom.”

Mirror:
- https://www.instagram.com/p/CEzFoBPjbTu/

The Instagram metadata explicitly preserves:
- `https://twitter.com/drstevenjlawson/status/1301283422413950978?s=21`

### Classification

`PASTORAL / CHRIST-CENTERED / ENCOURAGING`

---

### 4.2. Trials mature rather than merely break believers

Original status ID:
- `1251310283617898496`

Snowflake timestamp:
- **2020-04-18 00:43:14.492 UTC**

Mirror/search preservation gives the text:

> “God uses our trials to make us, not break us. We mature more during days of adversity than in days of prosperity.”

Mirror:
- https://www.facebook.com/DefendendoOEvangelhoOficial/posts/boa-tarde-deus-usa-nossas-prova%C3%A7%C3%B5es-para-nos-moldar-n%C3%A3o-para-nos-quebrar-amadure/3173689482670580/

The fetched mirror preserves the original Twitter link for ID `1251310283617898496`.

### Classification

`PASTORAL / SUFFERING / ENCOURAGEMENT`

---

### 4.3. Eternity and God's glory

Original status ID:
- `1221124984250216449`

Snowflake timestamp:
- **2020-01-25 17:37:38.307 UTC**

Mirror preserves:

> “Eternity will not be long enough to give God the glory He deserves.”

Mirror:
- https://www.facebook.com/DefendendoOEvangelhoOficial/posts/bom-dia-a-eternidade-n%C3%A3o-ser%C3%A1-longa-o-suficiente-para-dar-a-deus-a-gl%C3%B3ria-que-el/3003408073032056/

Search result preserves the original status ID.

### Classification

`DOXOLOGICAL / ENCOURAGING`

---

### 4.4. Knowing Christ / making Christ known

Original status ID:
- `1282903671731179520`

Snowflake timestamp:
- **2020-07-14 05:04:05.195 UTC**

A Facebook mirror preserves the original status ID and renders the statement in Portuguese as:

- the greatest joy is knowing Jesus Christ;
- the second greatest joy is making Him known.

Mirror:
- https://www.facebook.com/DefendendoOEvangelhoOficial/photos/boa-noite-a-maior-alegria-%C3%A9-conhecer-jesus-cristo-a-segunda-maior-alegria-%C3%A9-torn/3413184068721119/

### Guardrail

The current fetch/search object does not expose the full original English text cleanly enough to use exact quotation marks in article copy. Preserve the proposition and ID; reacquire the original English wording from another mirror before quote-level use.

### Classification

`EVANGELISTIC / CHRIST-CENTERED / ENCOURAGING`

---

## 5. Sharper / judgment-warning Lawson posts

### 5.1. More false prophets than true teachers

Original status ID:
- **`1353457746671239168`**

Snowflake timestamp:
- **2021-01-24 21:40:47.492 UTC**

A Facebook mirror/search index preserves both the text and the original status ID:

> “There are more false prophets than there are true teachers. Many pulpits are on the wide path, few are on the narrow way.”

Mirror:
- https://www.facebook.com/DefendendoOEvangelhoOficial/posts/bom-dia-existem-mais-falsos-profetas-do-que-verdadeiros-mestres-muitos-p%C3%BAlpitos-/3977378438968343/

Search preservation explicitly shows:
- `twitter.com/drstevenjlawson/status/1353457746671239168`

### Classification

`POLEMICAL / JUDGMENT / FALSE-TEACHER WARNING`

### Guardrail

Calling false teachers dangerous is not by itself sinful provocation. This post is placed in the “sharper” bucket because of tone/content, not because its doctrine is being judged false.

---

### 5.2. Life is short / death / judgment / hell

Original status ID:
- **`1389757632596955136`**

Snowflake timestamp:
- **2021-05-05 01:43:34.716 UTC**

A mirror preserves:

> “Life is short. Death is sure. Judgment is coming. Heaven is glorious. Hell is dreadful. Jesus is Savior.”

Mirror:
- https://www.facebook.com/DefendendoOEvangelhoOficial/posts/boa-noite-a-vida-%C3%A9-curta-a-morte-%C3%A9-certa-o-julgamento-est%C3%A1-chegando-o-c%C3%A9u-%C3%A9-glor/4364286956944154/

Search preservation explicitly exposes the original Twitter status ID.

### Classification

`EVANGELISTIC WARNING / JUDGMENT / GOSPEL`

### Important nuance

This is not easily categorized as “provocative” versus “pastoral.” It combines severe warning and explicit gospel proclamation in one compact tweet.

That ambiguity is itself important for any future quantitative coding protocol.

---

### 5.3. Coronavirus / eternal-destiny warning

Original status ID:
- **`1239239636842668033`**

Snowflake timestamp:
- **2020-03-15 17:18:48.039 UTC**

A Portuguese Facebook mirror/search result preserves the original Lawson status URL and enough text to establish that the post framed the coronavirus tragedy in relation to death and hell.

Mirror:
- https://www.facebook.com/DefendendoOEvangelhoOficial/photos/bom-dia-a-verdadeira-trag%C3%A9dia-com-o-coronav%C3%ADrus-n%C3%A3o-%C3%A9-que-muitos-tenham-morrido-/3095971603775702/?locale=pt_BR

Original status:
- `twitter.com/drstevenjlawson/status/1239239636842668033`

### Evidence guardrail

The current retrieval does **not** expose the complete English sentence with sufficient confidence for exact quotation.

Use this object as:

- a confirmed Lawson status ID;
- a confirmed March 15, 2020 warning post about coronavirus/death/hell;
- a reacquisition target for exact text.

Do not reconstruct missing wording from translation fragments.

### Classification

`JUDGMENT / ETERNAL-DESTINY WARNING / HIGH-RHETORICAL-SEVERITY`

---

## 6. A category problem: “hard” is not the same as “provocative”

Several recovered Lawson statements are severe but biblically ordinary within conservative evangelical preaching.

Examples include:

- false teachers;
- judgment;
- hell;
- narrow/wide way;
- telling sinners the truth.

The book's self-critique appears to concern something more specific than merely preaching unpleasant doctrines.

The critical distinction for future coding must be:

### Category A — necessary theological warning

Examples:
- hell is real;
- false teachers exist;
- judgment is coming;
- sinners need truth;
- church discipline may be required.

### Category B — performative/provocative platform style

Possible markers:
- phrasing optimized for reaction rather than clarity;
- unnecessary personal attack;
- inflammatory framing beyond the biblical claim;
- repetitive outrage-content selection;
- rejoicing in punishment or humiliation;
- posts whose primary rhetorical function appears to be confrontation.

The current pass has **not** reconstructed enough Lawson statuses to make this Category B judgment reliably at scale.

That prevents confirmation bias.

---

## 7. Why simple engagement comparison is not currently possible

The mirrors preserve some combination of:

- tweet text;
- original status URL/ID;
- mirror publication date;
- mirror likes/comments/shares.

They generally do **not** preserve:

- Lawson's original like count;
- Lawson's original retweet/repost count;
- Lawson's original quote count;
- count snapshot time;
- impression count.

Current X pages for these old IDs are not reliably indexed/fetchable through the available public retrieval paths.

### Therefore

It would be methodologically false to write:

> “Our data confirm Lawson's provocative tweets received N times more engagement.”

The current data do not support that.

Safe:

> “The historical text corpus can be partially reconstructed, including original status IDs and dates, but the original engagement counts have not yet been recovered. Lawson's claim that provocative posts outperformed pastoral ones therefore remains a first-person claim rather than an independently quantified finding.”

---

## 8. Early qualitative finding: the surviving corpus is not one-note

The currently recovered material already includes both:

### Warm / pastoral / Christ-centered

- believing, knowing and obeying Christ;
- maturity through trials;
- God's glory;
- knowing Christ and making Him known.

### Severe / warning-oriented

- more false prophets than true teachers;
- many pulpits on the broad road;
- death/judgment/heaven/hell;
- coronavirus framed through eternal destiny.

This supports the methodological conclusion from `52_`:

> **Lawson's public corpus was not simply “grace” or simply “judgment.” Both existed.**

The 2026 book's self-diagnosis is therefore best tested by **relative frequency, rhetorical style and engagement incentives**, not by cherry-picking one severe quote and declaring the case closed.

---

## 9. Status-ID ledger acquired so far

| Status ID | UTC time from Snowflake | Evidence state | Working class |
|---|---|---|---|
| `1221124984250216449` | 2020-01-25 17:37:38.307 | text + mirror + ID | doxological |
| `1239239636842668033` | 2020-03-15 17:18:48.039 | partial text + mirror + ID | severe warning |
| `1251310283617898496` | 2020-04-18 00:43:14.492 | text + mirror + ID | pastoral/trials |
| `1282903671731179520` | 2020-07-14 05:04:05.195 | translated mirror + ID | Christ-centered |
| `1301283422413950978` | 2020-09-02 22:18:39.237 | exact English + mirror + ID | Christ-centered |
| `1353457746671239168` | 2021-01-24 21:40:47.492 | exact text + mirror + ID | polemical/false teachers |
| `1389757632596955136` | 2021-05-05 01:43:34.716 | exact text + mirror + ID | gospel/judgment warning |

Additional status ID already preserved elsewhere and requiring full text reacquisition:
- `1135723374901112832` — Snowflake time **2019-06-04 01:42:07.953 UTC**; Reddit discussion identifies it as Lawson's abbreviated tweet on knowing God, but the current fetch did not expose the original tweet text sufficiently for quote-level custody.

---

## 10. Social-media evidence hierarchy

### A1 — strongest
- live/archived original X object;
- text;
- timestamp;
- original engagement snapshot.

### A2
- third-party embed that preserves original status ID + exact tweet text + timestamp/date.

### B
- mirror preserving status ID + exact/near-exact text, but no original engagement.

### C
- attributed quote without original status ID.

### D
- post-scandal paraphrase of what Lawson “used to post.”

Current corpus is mostly **A2/B**, not A1.

Therefore it is already useful for rhetoric/text analysis but not yet for engagement statistics.

---

## 11. Next acquisition targets

### P1 — more status IDs from archived embeds

Search:
- Ligonier social-media highlight posts;
- conference live-blog pages;
- old blogs embedding `@DrStevenJLawson` tweets;
- Facebook/Instagram translations that preserve source URLs;
- Reddit quote posts;
- cached tweet aggregators.

### P1 — build a balanced sample

Target at least:
- 25 pastoral/encouraging statuses;
- 25 doctrinal-neutral statuses;
- 25 severe/polemical statuses.

Do not select only viral or scandal-relevant examples.

### P1 — original engagement snapshots

Search specifically for:
- screenshots;
- embedded tweet HTML preserving counts;
- Internet Archive captures of status pages;
- quote articles mentioning virality/counts;
- data archives if lawfully/publicly available.

### P2 — coding protocol

Before comparing groups, define blind-ish categories:
- pastoral/encouraging;
- evangelistic warning;
- doctrinal proposition;
- polemical/boundary;
- personal/institutional attack;
- promotional.

A hard doctrine should not automatically be coded “provocative.”

---

## Research conclusion

> **THE FIRST X/TWITTER RECONSTRUCTION PASS RECOVERS A REAL HISTORICAL LAWSON CORPUS RATHER THAN A COLLECTION OF UNSOURCED QUOTES. MULTIPLE THIRD-PARTY MIRRORS PRESERVE HIS ORIGINAL STATUS IDS, ALLOWING EXACT PUBLICATION TIMES TO BE RECONSTRUCTED FROM TWITTER SNOWFLAKE TIMESTAMPS. THE SURVIVING SAMPLE ALREADY CONTAINS BOTH WARM CHRIST-CENTERED/PASTORAL POSTS AND SHARP JUDGMENT/FALSE-TEACHER POSTS. HOWEVER, THE MIRRORS GENERALLY PRESERVE THEIR OWN ENGAGEMENT COUNTS, NOT LAWSON'S ORIGINAL COUNTS. THEREFORE THE 2026 BOOK CLAIM THAT PROVOCATIVE POSTS RECEIVED MORE LIKES/REPOSTS CANNOT YET BE INDEPENDENTLY QUANTIFIED. THE CORRECT NEXT STEP IS A BALANCED STATUS-ID CORPUS PLUS ORIGINAL ENGAGEMENT SNAPSHOTS — NOT BORROWING METRICS FROM MIRROR ACCOUNTS OR CHERRY-PICKING HARSH QUOTES.**
