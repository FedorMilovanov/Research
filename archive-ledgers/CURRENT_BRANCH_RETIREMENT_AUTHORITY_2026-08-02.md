# CURRENT BRANCH RETIREMENT AUTHORITY — 2026-08-02

**Authority ID:** `RESEARCH-BRANCH-RETIREMENT-AUTHORITY-2026-08-02`  
**Status:** `ABSORBED_REFS_RETIRED_FORENSIC_ARCHIVE_RETAINED`

## 1. Current remote branch set

После ancestry-проверки и удаления полностью поглощённых refs в `FedorMilovanov/Research` должны оставаться только:

1. `main` — единственная current authority branch;
2. `archive/legacy-diverged-heads-20260801` — retained forensic history, **не** current authority.

Machine authority: [`../data/branch-retirement-authority-2026-08-02.json`](../data/branch-retirement-authority-2026-08-02.json).

## 2. Retired refs

Удалены восемь refs, которые перед удалением были проверены по двум обязательным условиям:

- exact branch head являлся предком свежего `origin/main`;
- `origin/main..branch-head` содержал `0` уникальных commits.

| Retired ref | Result |
|---|---|
| `agent/osk-source-authority-20260801` | fully absorbed; retired |
| `agent/osk-wave2-money-power-20260801` | fully absorbed; retired |
| `agent/osk-wave5-adelaja-20260801` | fully absorbed; retired |
| `archive/poet-portrait-review-refresh-20260731` | fully absorbed; retired |
| `archive/second-editorial-40-pdf-refresh-20260731` | fully absorbed; retired |
| `arena/019fb9cf-research` | fully absorbed; retired |
| `docs/source-library-94-collections-navigation-2026-07-30` | fully absorbed; retired |
| `tmp-do-not-use` | fully absorbed; retired |

### Receipt limitation

Первый retirement-run удалил refs после runtime ancestry checks, но его receipt-step не экспортировал shell variables перед Python. Поэтому exact deleted-head SHA не были сохранены в repository evidence. Они **не реконструируются и не выдумываются** в текущей authority.

Закрыт факт существования лишних remote refs и факт их полного поглощения на момент удаления. Не заявляется наличие полного post-hoc SHA-ledger для удалённых голов.

## 3. Retained forensic archive

| Поле | Значение |
|---|---|
| Branch | `archive/legacy-diverged-heads-20260801` |
| Exact head at receipt | `979fdc748c5f7097618c126eb75176152ac98d69` |
| Merge base with main | `f50b21ad6af5dd7aaa53c5be381929b353b26d58` |
| Unique commits at receipt | `50` |
| Behind main at receipt | `138` |
| Status | `RETAIN_FORENSIC_HISTORY_NOT_CURRENT_AUTHORITY` |

Архив сохраняет шесть уникальных forensic-ledger файлов:

- `archive-ledgers/branch-cleanup-summary-20260801.md`;
- `archive-ledgers/branch-forensic-retirement-receipt-20260801.json`;
- `archive-ledgers/legacy-diverged-heads-20260801.json`;
- `archive-ledgers/legacy-diverged-heads-20260801.md`;
- `archive-ledgers/source-library-ref-consolidation-20260801.json`;
- `archive-ledgers/source-library-ref-consolidation-20260801.md`.

Эта branch не должна использоваться как публикационная, статусная или source authority. Её нельзя удалять, пока уникальные ledgers не мигрированы намеренно либо не заменены эквивалентным immutable archive.

## 4. Recovery

```bash
git fetch origin archive/legacy-diverged-heads-20260801
git log --graph --oneline origin/archive/legacy-diverged-heads-20260801
git show origin/archive/legacy-diverged-heads-20260801:archive-ledgers/branch-cleanup-summary-20260801.md
```

## 5. CI contract

Read-only validator обязан проверить:

- machine authority schema/status;
- exact retired-ref set из восьми имён;
- отсутствие этих refs на remote;
- remote branch set ровно `{main, archive/legacy-diverged-heads-20260801}`;
- exact forensic archive head;
- наличие 50 unique commits относительно recorded merge-base/main snapshot boundary;
- запрет `archiveIsCurrentAuthority` и `archiveMayBeDeleted`;
- честное сохранение ограничения `deletedHeadShasPersisted=false`;
- отсутствие active one-time branch-deletion workflow.

## 6. Итог

```text
CURRENT AUTHORITY BRANCHES: 1 (main)
RETAINED FORENSIC BRANCHES: 1
ABSORBED REFS RETIRED: 8
UNIQUE COMMITS IN FORENSIC ARCHIVE AT RECEIPT: 50
FORENSIC ARCHIVE IS CURRENT AUTHORITY: NO
FORENSIC ARCHIVE DELETION AUTHORIZED: NO
DELETED HEAD SHAS PERSISTED: NO — LIMITATION EXPLICITLY RECORDED
ONE-TIME BRANCH WRITER: REMOVED
```
