# G3 durable custody policy

**Status:** `ACTIVE / RESEARCH-ONLY / PUBLICATION_HOLD`  
**Authority:** `DURABLE_CUSTODY_MANIFEST.json`

GitHub Actions artifacts are deliberately **ephemeral acquisition custody**, not the durable evidence archive. For the G3 corpus, durable custody means that Git preserves enough immutable provenance to identify and re-acquire or authenticate an evidence object without pretending that a seven-day Actions artifact is permanent storage.

## Durable layer

For high-value acquired objects, the repository should preserve, where available:

1. canonical source/claim ID;
2. exact object ID or locator;
3. SHA-256 of the acquired bytes or bounded derivative;
4. acquisition workflow/run/head identity;
5. whether raw bytes are retained;
6. publication/rights state.

`DURABLE_CUSTODY_MANIFEST.json` is the machine-readable receipt set for the highest-value cryptographically controlled objects.

## Raw-byte rule

`DURABLE RECEIPT != RAW BYTES IN GIT`.

Government records, archived HTML, sermon audio/video and third-party PDFs have different licensing, privacy, size and republication constraints. Raw bytes must not be copied into Git merely to make custody look stronger.

Before publication, each object actually quoted, reproduced, embedded or relied on for a high-impact allegation needs a separate item-level decision:

`IDENTITY → HUMAN READ/LISTEN → HASH/LOCATOR → RIGHTS → PUBLICATION USE`.

## Runtime reproducibility

The media/content workflows pin direct Python dependencies and pinned GitHub Action commits. Each media/content artifact also records the resolved Python environment; media workflows additionally record the actual `ffmpeg` version because the Ubuntu package is an external runner dependency.

This is reproducible provenance, not a claim of hermetic bit-for-bit media decoding across all future runner images.

## Reopen rule

If a source disappears or materially changes, the durable receipt is sufficient to prove which bytes were acquired previously **only when a full SHA-256 is present**. It is not sufficient to publish copyrighted raw material that was not otherwise cleared.

`PUBLICATION_HOLD` remains independent of custody completeness.
