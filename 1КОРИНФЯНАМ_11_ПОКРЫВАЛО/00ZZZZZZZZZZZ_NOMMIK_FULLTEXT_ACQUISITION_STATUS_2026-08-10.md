# Nõmmik full-text acquisition status

**Дата:** 2026-08-10  
**Статус:** `OPEN-ACCESS-CONFIRMED / BYTES-NOT-YET-RESOLVED / DO-NOT-ASK-USER`

## Institutional proof of availability

University College Stockholm / Enskilda Högskolan Stockholm directly lists:

**Aldar Nõmmik, _Robes, Romans, and Rituals in First Corinthians: Paul and the Conflict over Head-Coverings_, DTH 9**

with the label:

`Fulltext i DiVA`

The official dissertation-defense page supplies the exact persistent identifier:

```text
urn:nbn:se:ths:diva-2600
```

and links it through the Swedish national URN resolver.

Therefore:

```text
OPEN_ACCESS_EXISTENCE = A_INSTITUTIONAL
PERSISTENT_IDENTIFIER = A
USER_NEEDS_TO_SUPPLY_COPY = false
```

## Current route result

This audit attempted:

1. exact URN resolver route;
2. title + URN search-engine discovery;
3. title + `FULLTEXT01.pdf` search;
4. likely DiVA host/index discovery;
5. Google Books current and dissertation-edition routes.

The current web harness can verify the institutional statement and identifier, but does not currently resolve the underlying DiVA record/PDF endpoint into readable bytes.

No direct `FULLTEXT01.pdf` URL for **this exact record** was discovered in indexed results.

## Anti-kostyl rule

Do **not** guess a DiVA `diva2:` PID from the URN suffix.

DiVA examples show that:

```text
urn:*:diva-2600
```

is **not** equivalent to:

```text
diva2:2600
```

The `diva2:` record identifier is a separate global/portal record ID and must be obtained from the actual resolved record.

Therefore these are forbidden:

```text
INVENT_RECORD_PID = false
INVENT_FULLTEXT_URL = false
CLAIM_PDF_READ_FROM_GUESSED_ENDPOINT = false
```

## Available substitute routes while resolver is blocked

Directly usable:

- official EHS defense page with author interview and detailed abstract;
- official EHS DTH listing;
- Wipf & Stock current edition description;
- Google Books limited preview, TOC and indexed terms;
- independent Oster/Gill/Massey/Finney evidence;
- Berglund 2025 bibliography citing Nõmmik pp.81–150.

These suffice for a **pre-fulltext adversarial audit**, but not for page-level promotion of Nõmmik’s distinctive causal claims.

## Full-text priority sections once route resolves

```text
pp. 81–150   capite velato / garment evidence corpus
pp. ~205–206 cognition and group dynamics
pp. ~230+    exegesis / hierarchy of heads / 11:3–6
v10 section  exousia + angels
vv14–15      physis / hair
p. ~289      Women as Scapegoats
p. ~317      conclusions
p. ~347      index of ancient literature for primary-source spot checks
```

## User burden rule

```text
NOMMIK_USER_ACQUISITION = PROHIBITED_FOR_NOW
DO_NOT_REQUEST_FROM_USER_IF_AGENT_CAN_ACCESS = true
```

The source remains an agent-side open-access acquisition task.