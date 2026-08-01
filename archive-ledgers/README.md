# Archive branch index

This directory is the only current-main entry point for non-current branch history.

## Authority rule

- `main` is the only current Research authority.
- Archive branches are recovery containers, not alternate working authorities.
- Files found only on an archive branch must not be cited as current decisions until they are deliberately promoted to `main` with a new authority record.
- GitHub search results from non-main branches are historical evidence only.

## Durable archive ref

| Branch | Archive anchor / relationship | Purpose | Current authority |
|---|---|---|---|
| `archive/legacy-diverged-heads-20260801` | diverged from `f50b21ad6af5dd7aaa53c5be381929b353b26d58`; forensic archive contains preserved legacy heads and cleanup receipts | recovery of unique pre-cleanup branch histories | **NO** |

The archive branch is intentionally retained because it stores additional-parent preservation commits and forensic ledgers. It must remain clearly separated from current corpus authority.

## Recovery procedure

```bash
git fetch origin archive/legacy-diverged-heads-20260801
git show origin/archive/legacy-diverged-heads-20260801:archive-ledgers/branch-cleanup-summary-20260801.md
```

Recover a file to a temporary path first. Do not merge the archive branch into `main` wholesale.

## Stale working refs

Historical `agent/*`, `arena/*`, `docs/*` and temporary `archive/*-refresh-*` refs may still exist until repository ref deletion is completed. Their commits were already integrated or preserved; they carry no current authority. The expected permanent ref set is:

1. `main`;
2. `archive/legacy-diverged-heads-20260801`.

Any additional branch must have an explicit active owner, expiration date and authority purpose, otherwise it is stale.

## Integrity boundary

The repository-wide validator requires this index so that a hidden archive layer cannot exist without a visible warning on `main`.
