# SUNO prompt and version register

## Non-negotiable rule

The exact prompt must be stored verbatim from the submitted prompt text or recovered from the owner's authoritative record. A style description reconstructed from memory is not the original prompt. When the exact text is not available, state NOT CAPTURED.

## Required version fields

- work ID and version ID;
- historical source ID and lyric revision ID;
- exact prompt text and prompt revision/hash;
- generation date/time when known;
- model / mode only when the owner records it;
- vocal assignment, section tags and pronunciation notes;
- output filename, format, duration and file hash after actual readback;
- cover ID and approval state;
- export settings and metadata readback;
- QA state, open defects and release URL/receipt.

## Current capture

| Version | Audio export reported | Exact prompt | Exact lyric revision | Actual file metadata readback | Public URL |
|---|---|---|---|---|---|
| DUTCH-001-V1 | Yes, local WAV/MP4/MP3 paths reported | NOT CAPTURED | NOT IN REPOSITORY | Prior properties reported; re-read actual files before relying on them | NOT VERIFIED |
| DUTCH-002-V1 | Yes, local WAV/MP4/MP3 paths reported | NOT CAPTURED | NOT IN REPOSITORY | Prior properties reported; re-read actual files before relying on them | NOT VERIFIED |
| DUTCH-002-V2 | Yes, local WAV/MP4/MP3 paths reported | NOT CAPTURED | NOT IN REPOSITORY | Prior properties reported; re-read actual files before relying on them | NOT VERIFIED |
| DUTCH-003-V1-REPORTED | MP3 filename reported; QA incomplete | NOT CAPTURED | NOT IN REPOSITORY | ID3 tag readback and cover state unconfirmed | NOT VERIFIED |
| DUTCH-004-RU-DRAFT-v0.1 | **None — nothing generated** | `PROMPT-DUTCH-004-V1`, authored in this repository, never submitted | v0.1 draft in the production package | NOT APPLICABLE | NONE |
| DUTCH-005-RU-DRAFT-v0.1 | **None — nothing generated** | `PROMPT-DUTCH-005-V1`, authored in this repository, never submitted; a second style direction recorded as an option only | v0.1 draft in the production package | NOT APPLICABLE | NONE |

## Authored versus recovered prompts

Two different objects are recorded here and must not be confused:

- **Recovered prompt** — the exact text that was actually submitted to SUNO in an earlier session. For DUTCH-001, DUTCH-002 and DUTCH-003 no such text is held: `NOT_CAPTURED`. It must be recovered from the owner, never reconstructed.
- **Authored prompt** — a prompt written in this repository for a work that has not been generated. DUTCH-004's `PROMPT-DUTCH-004-V1` and DUTCH-005's `PROMPT-DUTCH-005-V1` are of this kind and carries `promptState: AUTHORED_NOT_YET_SUBMITTED`. The validator requires its `promptText` to appear byte-identically in the production package, so the registry and the document cannot drift.

## Style selection

Choose style from the text's literary type and rhetorical arc. The owner's general preference is a restrained, dark, acoustic sacred sound; strings, cello and contrabass may fit. Avoid harsh or “smoker-like” bass. These preferences are not a replacement for a per-track prompt, nor evidence that the historical poet used those instruments.

For a text with a verified tune instruction, the prompt may explicitly say “modern setting inspired by the source's devotional context”; do not claim historical authenticity unless separately proven.
