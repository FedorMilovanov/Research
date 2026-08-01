# Archive branch index

This directory is the only current-main entry point for non-current branch history.

## Authority rule

- `main` is the only current Research authority.
- Archive branches are recovery containers, not alternate working authorities.
- Files found only on an archive branch must not be cited as current decisions until deliberately promoted to `main` with a new authority record.

## Permanent forensic archive

| Branch | Archive anchor / relationship | Purpose | Current authority |
|---|---|---|---|
| `archive/legacy-diverged-heads-20260801` | diverged from `f50b21ad6af5dd7aaa53c5be381929b353b26d58`; contains additional-parent preservation commits and forensic ledgers | recovery of unique pre-cleanup histories | **NO** |

Recovery:

```bash
git fetch origin archive/legacy-diverged-heads-20260801
git show origin/archive/legacy-diverged-heads-20260801:archive-ledgers/branch-cleanup-summary-20260801.md
```

Recover individual files to a temporary path. Never merge the forensic archive wholesale into `main`.

## Neutralized aliases

On 2026-08-02 the following obsolete working refs were force-aligned to exact `main` commit `96935a825a38cdd24fac028c8d2a51358dd55abd` after their unique histories had already been preserved in the forensic archive or GitHub PR history:

- `agent/osk-source-authority-20260801`;
- `agent/osk-wave2-money-power-20260801`;
- `agent/osk-wave5-adelaja-20260801`;
- `archive/poet-portrait-review-refresh-20260731`;
- `archive/second-editorial-40-pdf-refresh-20260731`;
- `arena/019fb9cf-research`;
- `docs/source-library-94-collections-navigation-2026-07-30`;
- accidental ref `tmp-do-not-use`.

These refs contain no commits ahead of or behind that recorded `main` point and therefore no alternate authority. They should be deleted when a delete-ref operation is available; until then they are inert aliases.

## Expected long-term ref set

1. `main`;
2. `archive/legacy-diverged-heads-20260801`.

Any additional branch must have an explicit active owner, expiration date and authority purpose.

## Integrity boundary

The repository-wide validator requires this index so that non-main history cannot exist without a visible warning and recovery contract on `main`.
