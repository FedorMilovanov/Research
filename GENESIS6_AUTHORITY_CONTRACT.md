# Genesis 6: machine-readable authority contract

The canonical machine-readable entry points are:

- `data/genesis6-authority-manifest.json` — authority, supersession, scope and rights graph;
- `data/genesis6-publication-ledger.json` — deterministic ordered publication bundles for Articles 6–9;
- `scripts/validate_genesis6_authority_manifest.py` — fail-closed validator.

Authority base commit:

`b654c5375a7b212ff9b42c08bb0193eeaad70746`

Manifest SHA-256:

`95320cc56c678fcacf4f24985f96150c231b1d91338349c19005e277b16125dd`

## Site import rule

A site integration must pin both:

1. an exact Research commit containing this contract;
2. the exact manifest SHA-256 recorded in the publication ledger.

An XLVIII article by itself is not a complete publication input. The relevant bundle must also contain every mandatory active XLIX, L and LI authority document and an approved rights decision.

Closeouts, historical drafts and superseded documents remain preserved as evidence but are forbidden as direct site publication inputs.
