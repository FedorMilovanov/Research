# Buck Item 10 — Titus 2:11–15 original-media gate addendum

**Status:** ACTIVE / PUBLICATION_HOLD  
**Parent item:** `10_TITUS_2_11_15_AUTOBIOGRAPHY_AND_ATTRIBUTION.md`  
**Scope:** supersedes only the parent's former `BUCK_AUDIO_HOLD` acquisition state. It does not alter the Chapell-source or Jennifer-Buck biographical findings.

## Acquisition result

Workflow `G3 Buck Titus original-media acquisition`, run `34254294262`, Research head `f086679ae47a36cb7e99e66beb4a63886449e1dc`, successfully resolved the official FBC Lindale sermon landing page:

`https://fbclindale.com/resources/sermons/titus-211-15/`

The public page exposed an unauthenticated MP3:

`https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2023/08/06124555/2023_08_06_AM.mp3`

No cookies, account, session, password, private URL, or access-control bypass was used.

The lane acquired only `00:32:30–00:36:30` ephemerally:

- duration: 240 seconds;
- segment size: 23,040,104 bytes;
- segment SHA-256: `954041ea7b697ed98c27db8a852c8bb798db14ec44f69ec6e634046a2bd9729a`;
- full audio binary retained: **no**;
- artifact contains research receipt/transcript metadata, not sermon audio;
- machine transcript: **success**;
- `machine_transcript_only = true`;
- `item_verified = false`.

## What the machine transcript establishes diagnostically

The acquired source-window transcript contains the disputed first-person marriage/application passage, including reference to `Jennifer`, Buck's description of early marital coldness/selfishness, increasing awareness of his own insensitivities, and the analogy to Christ's love and holiness.

This is materially stronger than relying on the accusation dossier's STT for **whether the relevant subject matter is actually present in original FBC media**.

However, machine STT is not a human-verified quotation.

No explicit `Chapell`, `Hughes`, or `commentator` token occurs in the machine transcript of this selected four-minute window. That is a diagnostic observation only.

It does not prove that Buck gave no attribution:

- immediately before `00:32:30`;
- immediately after `00:36:30`;
- earlier in the sermon section;
- or in wording the machine model misrecognized.

## Current gate state

| Gate | State |
|---|---|
| Sermon identity/date | `VERIFIED_PRIMARY` |
| Official original-media locator | `VERIFIED_PRIMARY` |
| Relevant original-media segment acquired | `VERIFIED_EPHEMERALLY / HASHED` |
| Machine transcript of relevant window | `ACQUIRED / NOT QUOTE-SAFE` |
| Human original-audio check | `HOLD` |
| Wider attribution context | `HOLD` |
| Chapell source lineage | `VERIFIED / STRONG` |
| Pre-controversy Buck marital-history control | `PRIMARY_ANCHORED` |
| Fabricated-biography allegation | `BLOCKED / REFUTED_AS_UNSUPPORTED` |
| Whole sermon Item 10 | **NOT `ITEM_VERIFIED`** |

## Corrected verdict

`SERMON_IDENTITY_VERIFIED / ORIGINAL_MEDIA_LOCATOR_VERIFIED / RELEVANT_SEGMENT_ACQUIRED_AND_HASHED / MACHINE_TRANSCRIPT_ONLY / CHAPELL_SOURCE_OBJECT_VERIFIED / PRECONTROVERSY_BIOGRAPHY_PRIMARY_ANCHORED / FABRICATED-BIOGRAPHY CLAIM BLOCKED / HUMAN_AUDIO_AND_WIDER_ATTRIBUTION_CONTEXT_HOLD`

The parent item's phrase `BUCK_AUDIO_HOLD` should henceforth be read as superseded by this narrower human/context hold.
