# G3 engineering hardening checkpoint — 2026-09-08

**State:** `IMPLEMENTED IN HARDENING LANE / PUBLICATION_HOLD UNAFFECTED`  
**Research merge:** PR #188 → `main` merge commit `d88b146e6ebbf3182f9d16ff59f4ae0f97aa70e2`  
**Historical research head:** `02e4a191c87884771158afc38846d09a98ae6422`

This checkpoint records engineering closure after the evidence corpus itself was merged.

## Implemented controls

1. Legacy G3 Buck/content acquisition workflows are no longer tied to the retired `research/g3-history-20260907` branch.
2. Those workflows now support `pull_request`, `workflow_dispatch`, and path-scoped `push` on `main`.
3. Superseded runs use PR/ref-scoped `concurrency` with `cancel-in-progress: true`.
4. GitHub Actions are pinned to immutable commit SHAs.
5. Direct Python acquisition dependencies are version-pinned; resolved environments are recorded in artifacts, and media artifacts record the actual ffmpeg version.
6. `G3 corpus integrity` performs network-free cross-ledger, Buck-registry, workflow and publication-firewall validation on PRs and `main`.
7. Repository-global `Repository authority integrity` now compiles every G3 Python tool and runs the G3 corpus validator.
8. `G3 main governance audit` makes a direct single-parent G3 mutation on `main` terminal-red after the fact.
9. Durable cryptographic receipts are preserved in `DURABLE_CUSTODY_MANIFEST.json`; seven-day Actions artifacts remain explicitly ephemeral and are not misrepresented as permanent storage.

## Administrative protection boundary

At the start of this hardening pass GitHub reported:

- `main.protected = false`;
- repository rulesets = `[]`.

The connected GitHub App exposes content/workflow/PR writes but not repository-administration writes for branch protection/rulesets. Therefore this lane can **detect** an unprotected direct G3 push but cannot install the one control that must exist before the write: GitHub branch/ruleset protection.

Required repository-admin configuration remains:

- PR-only changes to `main`;
- required `Repository authority integrity` and `G3 corpus integrity` checks;
- disallow force pushes and deletion of `main`;
- retain merge-commit workflow for G3 changes while the governance detector requires two-parent provenance.

This is an account/repository administration boundary, not an evidence or code defect that should be hidden by a workflow workaround.

## Publication boundary

Nothing in this engineering hardening changes claim grades or evidence states. `PUBLICATION_HOLD` remains in force. Human Buck audio/source/attribution review, rights decisions, and genuinely new primary evidence remain separate publication gates.
