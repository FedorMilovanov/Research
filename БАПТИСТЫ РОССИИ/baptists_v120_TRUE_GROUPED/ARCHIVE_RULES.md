# ARCHIVE RULES v98 — NO MORE FILE SPRAWL

## Главный принцип
Не создавать новые numbered `.md` файлы (`159-...`, `160-...`, `new-pass-...`) для отдельных находок.

## Куда писать новые данные
- Метод / протокол / правила агентов → `groups/01_METHOD_AND_WORKFLOW.md`
- Исторический нарратив → `groups/02_HISTORY_NARRATIVE.md`
- Периодика → `groups/03_PERIODICAL_CORPUS.md`
- Самиздат / гонения / СРУ / СЦ ЕХБ → `groups/04_SAMIZDAT_PERSECUTION.md`
- GitHub / публикация / медиа → `groups/05_REPO_AND_PUBLICATION.md`
- Таблицы / статусы / OCR / proof-cards → `groups/06_DATA_AND_PROOF_LEDGERS.md`

## Когда можно создать новый файл
Только если появляется новая большая группа уровня раздела книги. Не номер журнала, не один архив, не одна цитата.

## Proof ladder
`lead` → `catalog_verified` → `item_card_verified` → `file_access_verified` → `page_count_verified` → `ocr_done` → `quote_card_verified`.

Прямая цитата в текст серии допускается только после `quote_card_verified`.


## v101 rule update

Use stable filenames (`MASTER_CORPUS_LEDGER.csv`, `PROOF_STATUS_LEDGER.csv`) instead of versioned delta-sprawl when possible. Keep changelog versioned, but ledgers should be current working ledgers.


## v104 strict rule

Do not create per-issue MD files for ordinary verification passes. Add rows to `data/PROOF_STATUS_LEDGER.csv`, source anchors to `data/SOURCE_ANCHORS.csv`, and narrative synthesis to `groups/04_SAMIZDAT_PERSECUTION.md` / `groups/06_DATA_AND_PROOF_LEDGERS.md`. Only create a new standalone file for a genuinely new large corpus or a publication-ready chapter.


## v108 reinforcement

Do not create per-issue MD files for every verified issue. Record issue status in data/PROOF_STATUS_LEDGER.csv and summarize only the meaningful deltas in groups/04_SAMIZDAT_PERSECUTION.md.


## v108 reinforcement

When a batch has many issues, add rows to PROOF_STATUS_LEDGER and summarize the batch in groups/04; do not create one MD per issue.


## v110 reinforcement

If a year-level or unnumbered item appears, keep it separate until title-page/file check. Do not merge with numbered issues by assumption.


## v112 reinforcement

If a copy-row has a zero or missing page count, record it as a catalog anomaly / unresolved copy, not as an absence of text.


## v117 reaffirmation

Continue grouped-library only. Add issue evidence to CSV ledgers and group summaries. Do not create one MD file per issue.
