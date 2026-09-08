# G3 ideology/content corpus — reproducible coding protocol

**Status:** ACTIVE / PUBLICATION_HOLD  
**Purpose:** replace impressionistic claims such as `G3 became increasingly culture-war oriented` with a reproducible, auditable content analysis.

## Core rule

Search-engine visibility is **not** a corpus census.

No percentage, prevalence claim or trend line may be published from Google/Bing result counts, current G3 category pages, or a hand-picked list of memorable controversies.

A quantitative claim requires a defined acquisition frame, deduplication, date normalization and a frozen coding dataset.

## 1. Separate content universes

At minimum, do **not** mix these into one denominator:

### A. National conference sessions

Unit = one official main/breakout/panel session.

This is the best surface for answering:

> What did the G3 Conference foreground to attendees each year?

### B. G3 site articles

Unit = one dated article/post published on the G3 web property.

This answers a different question:

> What did the broader G3 media ecosystem publish about over time?

### C. Podcasts / recurring video programs

Unit = one episode.

Keep separate because high-frequency recurring programs can swamp the article denominator.

### D. Institutional products

Books, curricula, workshops, G3+, journal issues and Church Network materials are coded as product/institution milestones, not mixed one-for-one with blog posts.

## 2. Required acquisition fields

Each corpus row must retain:

- canonical URL or archived URL;
- title;
- author/speaker;
- publication/event date;
- content universe (`conference`, `article`, `podcast`, `product`);
- conference/year/series where applicable;
- acquisition source (`official live/crawl`, `Wayback`, `participant archive`, etc.);
- current accessibility state;
- duplicate/canonical status;
- primary topic code;
- optional secondary topic codes;
- coder note;
- source confidence.

## 3. Topic vocabulary

Use a fixed controlled vocabulary.

### Theology / ministry

- `GOSPEL_CHRIST_SALVATION`
- `SCRIPTURE_SUFFICIENCY`
- `CHURCH_ECCLESIOLOGY`
- `PREACHING_PASTORAL_MINISTRY`
- `MISSIONS_EVANGELISM`
- `WORSHIP`
- `TRINITY_DOCTRINE_OF_GOD`
- `REFORMATION_HISTORY`
- `SANCTIFICATION_DISCIPLESHIP`
- `FAMILY_MARRIAGE`
- `ESCHATOLOGY`

### Culture / institutional conflict

- `SOCIAL_JUSTICE_CRT_RACE`
- `GENDER_SEXUALITY_COMPLEMENTARIANISM`
- `ABORTION_PRO_LIFE`
- `POLITICS_ELECTIONS_PARTIES`
- `STATE_CIVIL_AUTHORITY_COVID`
- `CHRISTIAN_NATIONALISM_THEONOMY`
- `SBC_EVANGELICAL_INSTITUTIONS`
- `EDUCATION_CULTURAL_FORMATION`
- `MEDIA_DISCOURSE_WOKEISM`

### Organization

- `G3_ANNOUNCEMENT_GOVERNANCE`
- `G3_PRODUCT_EVENT_PROMOTION`

## 4. Primary-topic rule

Every unit receives **exactly one primary topic** based on its main thesis/purpose, not on isolated keywords.

Example:

- an exposition of 1 Peter that briefly applies to hostile culture remains `SANCTIFICATION_DISCIPLESHIP` if the sermon/article is fundamentally pastoral exposition;
- an article directly arguing how Christians should vote is `POLITICS_ELECTIONS_PARTIES` even if it cites many biblical texts;
- a conference on `The Sovereignty of God` is not reclassified as political merely because one preconference panel discusses Christian Nationalism.

Secondary codes may capture real additional themes.

## 5. No keyword-only coding

Words such as `justice`, `race`, `government`, `church`, `Christ`, `worship` or `nation` are insufficient by themselves.

Each item requires headline + dek/description + enough body/session metadata to identify the actual thesis.

## 6. Periodization to test rather than assume

Freeze these candidate periods before analysis:

- `P1 2011–2017` — conference formation / broad conservative-Reformed coalition;
- `P2 2018–2020` — Dallas Statement / social-justice boundary formation + nonprofit institutionalization;
- `P3 2021–2022` — ecosystem expansion / partnership narrowing;
- `P4 2023–2024` — political-theology/right-flank conflict + financial reversal;
- `P5 2025–2026` — founder crisis / attempted reset / final collapse.

These periods are research hypotheses. If the coded data shows a different breakpoint, revise the periods rather than force the data to fit them.

## 7. Conference analysis

Preferred method: **full census** of surviving official conference archive entries, not a sample.

For each conference year:

- total identifiable sessions;
- count and share by primary topic;
- main-session versus breakout/preconference distinction;
- panel versus sermon distinction;
- conference main theme recorded separately.

This prevents one political preconference from being mistaken for the whole national conference.

## 8. Article analysis

Preferred method if full WordPress/archive export becomes available: full census.

If complete export cannot be lawfully/reliably acquired, use a **stratified sample fixed in advance**, for example:

- equal number of articles per calendar year;
- selection from chronological archive pages, not search relevance;
- deterministic interval sampling after deduplication;
- separately report years with insufficient surviving content.

Do not backfill missing years with hand-picked controversial articles.

## 9. Pilot anchors — qualitative only, not denominator data

The following verified pages prove that multiple content types existed; they **must not** yet be converted into percentages.

### Early political/cultural media before the Dallas Statement

- `When Belief Is Not Conviction` — surviving G3 page from the 2012-era corpus discusses the 2012 presidential vote, Obama, abortion and Christian conviction.
- `James Brown: The Godfather of…Theology?` — 2015-11-27; race/social-justice/cultural discussion.
- `Why I Cannot and Will Not Support Donald Trump for President` — 2016-02-20; direct presidential-politics commentary.

Interpretation allowed now: broader G3 web media was not apolitical before 2018.

Interpretation **not** allowed: political content dominated early G3 output.

### Early conference theological anchors

- 2013 — `The Gospel: Message and Mission`;
- 2014 — church/ecclesiology;
- 2015 — Scripture;
- 2016 — Trinity;
- 2017 — Reformation 500;
- 2018 — Knowing God / discipleship;
- 2019 main conference — Mission of God;
- 2020 — Worship;
- 2021 — Christ;
- 2023 — Sovereignty of God.

Interpretation allowed now: official main-conference themes across this sequence are predominantly theological/ecclesial.

### Boundary-formation anchors

- 2018-06-19 — Buice-organized Dallas meeting;
- 2018-09 — Statement on Social Justice and the Gospel;
- 2019 — dedicated G3 Social Justice preconference;
- 2021 — Challies participant account of Dallas-alignment functioning as platform/partnership boundary.

### 2023 right-flank/political-theology anchors

- Scott Aniol — `The Mixed Blessings of a Christian Nation`;
- Virgil Walker — `The Dangerous Intersection of Christian Nationalism and Ethnocentrism`;
- Scott Aniol — `Christian Faithfulness: The Biblical Alternative to Christian Nationalism`;
- official G3 preconference — Christian Nationalism/theonomy/postmillennialism debate;
- official national-conference main theme — `The Sovereignty of God`.

### Late ordinary-theology/pastoral controls

Do not sample only controversy. Surviving later G3 material includes ordinary doctrinal/pastoral content such as:

- expository preaching;
- election/salvation;
- worship;
- suffering;
- marriage/family;
- church;
- pastoral temperament;
- biblical manhood;
- historical theology.

These controls are essential when testing whether culture-war content became `dominant` rather than merely more visible.

## 10. Quantitative outputs permitted after acquisition

Once the frozen dataset is complete, calculate separately by content universe:

- yearly primary-topic counts;
- yearly shares;
- rolling three-year shares where sample size permits;
- theology/ministry aggregate versus culture/institutional-conflict aggregate;
- social-justice/CRT share;
- political-theology share;
- SBC/institutional-conflict share;
- number/share of multi-label items;
- number of identifiable conference sessions per year.

Report raw `n` alongside every percentage.

## 11. Sensitivity analysis

Before using trend language in the article, test at least:

1. primary-topic only;
2. primary + secondary labels;
3. main conference sessions only;
4. all conference sessions including breakouts/preconferences;
5. articles excluding pure G3 announcements/promotions;
6. articles including organizational posts.

A result that disappears under one reasonable coding choice should not be described as a robust historical trend.

## 12. Inter-coder / auditability rule

Even if one researcher performs the first coding pass, preserve enough source text/locator metadata that a second reviewer can reproduce disputed classifications.

For high-stakes trend claims, independently re-code a random subset and record disagreements.

## 13. Current working hypothesis

Current qualitative evidence suggests:

> G3’s **main conference themes remained heavily theological/ecclesial**, while its broader media and special-program surfaces carried culture/political commentary from early in its history and developed increasingly explicit boundary disputes after 2018. The 2023 Christian Nationalism conflict added a second ideological frontier rather than replacing the theological core.

**State:** `QUALITATIVE_HYPOTHESIS_STRONGLY_SUPPORTED / QUANTITATIVE_LANGUAGE_HOLD`.

Do not publish `X%`, `dominant`, `mostly`, `rare`, `surged by Y` or similar quantitative language until the acquisition and coding gates above are complete.