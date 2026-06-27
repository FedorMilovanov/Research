# v103 TRUE GROUPED — индекс

Архив остаётся компактным: master-группы + CSV-ledgers. Старые мелкие файлы поглощены группами; соответствие старых файлов см. в `data/LEGACY_TO_GROUP_CROSSWALK-v98.csv`.

## Быстрый вход

1. `README.md` — что изменилось и как пользоваться.
2. `ARCHIVE_RULES.md` — правила: не плодить мелкие MD, углублять группы.
3. `groups/04_SAMIZDAT_PERSECUTION.md` — текущие самиздатные закрытия.
4. `data/PROOF_STATUS_LEDGER.csv` — статусы конкретных выпусков.
5. `data/NEXT_MICROBATCH.csv` — следующий список на файл/OCR/quote-card.

## Текущий статус

v103 закрыл ещё блоки `Вестника Спасения` и `Бюллетеня СРУ` до уровня holding/page, но публикационные quote-cards всё ещё требуют локальных файлов/сканов, OCR и визуальной сверки.


## v104

Добавлен verification-pass по `Бюллетень СРУ 1979 №62/64`, master-grid `Вестника Спасения`, master-grid `Бюллетеня СРУ` и OSA-crosscheck `BRATSKII LISTOK`. Архитектура не раздута; quote-ready не добавлялся.


## v105 update

Closed additional samizdat items to holdings/page level: Vestnik Spaseniia 1965 no.1, 1967 no.1, 1968 no.1; BSRU 1979 no.65–73 and 1980 no.74. No quote-ready claims.


## v110 update

Closed additional BSRU 1980 item cards to holdings/page level: no.75–79, 82, 84–86; closed Vestnik Spaseniia 1967 no.3(19) to 54 pp. No quote-ready claims.


## v110 note

Added a focused verification pass for Vestnik Spaseniia and BRATSKII LISTOK. No new mini-MD files; all changes live in master groups and ledgers.


## v110 note

Focused SRU Bulletin pass: 1976 №30–38 and 1977 №39–41 now in proof ledger with page/holding statuses and copy-variant flags.


## v110 update

Closed a dense Toronto Samizdat verification block for Biulleten SRU 1977 no.42–46 and 1978 no.47/49 to holdings/page level. No quote-ready status was assigned; local scan/OCR/visual check remains required.


## v110 note

Focused SRU 1978 batch: №52, 53, 55, 56, 58, 59, 60 and a separate 1978 year-level bundle. No new per-issue MD files.


## v112 summary

Version v112 continues the TRUE GROUPED architecture. It adds a compact verification pass for `Бюллетень СРУ` 1975 №19–23, №25–26, №28 and 1976 №29. All newly added rows are metadata/holding/page-level only; no `quote_ready` status is assigned without local scan, OCR, and visual verification.


## v112 note

Focused SRU early block: 1972 №9–10, 1973 №11–12, 1974 №14–18. No per-issue MD files created.


## v113 percentage snapshot

- Proof-ledger rows: **114**.
- Holdings/file/page metadata level: **100/114 ≈ 87.7%**.
- Rows with page/file metadata evidence: **101/114 ≈ 88.6%**.
- Quote-ready rows: **0/114 = 0%**.

Interpretation: web/catalog verification is now mostly mature for the Toronto SRU segment, but publication-grade citation work is still at the file/OCR/visual-check stage.


## v115 Bratskii Listok verification pass

This pass moves a batch of `BRATSKII LISTOK` items from loose title-level awareness into item-card / holdings-aware status. Most records still lack visible page-counts, so they remain **not quote-ready**. The key additions are: 1971 no.7-8, 1971 no.9-10, 1972 no.1, 1972 no.4, 1972 no.6, 1973 no.4, 1974 no.1, 1975 no.2, 1975 no.4, and 1975 no.5. The strongest warning is 1971 no.9-10: one Baylor/Keston copy row has Pages=0 while other rows show no visible page-count; this must be treated as a catalog anomaly until a local scan is inspected.

Archive rule reaffirmed: do not create one MD per issue. Add rows to `PROOF_STATUS_LEDGER.csv`, add source anchors, and summarize the batch inside the grouped library only.


## v115 update

Focused pass on late-1975 to 1977 `BRATSKII LISTOK` item cards. The pass adds nine proof-ledger rows. Most were upgraded to `holdings_verified_no_page_count`; `1976 no. 1`, `1976 no. 6`, and `1977 no. 3` remain `item_designation_verified` only. No `quote_ready` rows were added.


## v116 summary

Added compact Bratskii Listok 1978–1980 item/holding pass. Working rule unchanged: do not create separate MD files for each issue; update grouped files and CSV ledgers only. Quote-ready remains blocked until local file/scan + OCR + visual check.


## v118 update

Continued compact TRUE GROUPED verification. Added `BRATSKII LISTOK` 1980 no.5-6, 1981 no.1-6, 1982 no.2/3/6, and 1983 no.1-3 to proof/source ledgers. Most are holding/item-level only; no `quote_ready` status was assigned.


## v118 update
BRATSKII LISTOK 1983–1986 pass added to grouped ledgers; still no quote-ready rows.


### v119 update

Added early BRATSKII LISTOK 1965–1966 verification pass. This version keeps the TRUE GROUPED architecture and updates only master-groups plus ledgers. New rows mostly confirm issue existence and selected Baylor/Keston/OSA holdings; no quote_ready status was added.


## v120 update — 1967–1970 BRATSKII LISTOK early block

v120 continues the grouped architecture. It adds an early BRATSKII LISTOK verification pass covering 1967 item-only cards, 1968 page-verified issues, and 1969–1970 holdings-without-page rows. The archive remains non-quote-ready until local file/OCR/visual-check work is completed.


## v125 update — Sinichkin TG export acquired (local periodical corpus)

A full export of the Telegram channel «Синичкин рассказывает» was acquired and mined (`ChatExport_2026-06-27`, 6125 files incl. 143 PDF, 2 125 pages of material). This is the archive's first **local, page-counted** periodical corpus.

- **+98 periodical issues** verified to `page_count_verified` (scans, no OCR): `Баптист` (46), pre-revolutionary `Братский Листок` (22), `Утренняя Звезда` 1915 (16), `Христианин` (6), `Гость` (4), `Слово Истины` (3), `Братский Вестник` 1945 №2 (1).
- **Key distinction:** the Sinichkin *Братский Листок* (1906–1910) is the pre-revolutionary supplement to *Христианин* — **not** the Soviet CCECB samizdat (1965–2000) tracked in the Toronto corpus.
- **Resolved open targets:** P. V. Pavlov «Политические требования баптистов» (Slovo Istiny 1917 №1) — text extracted; Sinichkin Voronin article — text extracted; Baptist/EC unity congress protocols — local files acquired.
- **No `quote_card_verified` rows added.** Scanned issues need OCR; typed documents are queued for quote-cards. See `groups/03_PERIODICAL_CORPUS.md` (v125 section) and `groups/06_DATA_AND_PROOF_LEDGERS.md`.
