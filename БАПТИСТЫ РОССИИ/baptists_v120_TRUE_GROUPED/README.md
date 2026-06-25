# Baptists Russia Research Archive — v103 TRUE GROUPED

v103 продолжает TRUE GROUPED-линию: новые проверки не создают россыпь MD, а входят в существующие master-группы и CSV-ledgers.

## Главный статус

Архитектура и карта корпусов уже сильные. Дальше ключевая работа не в расширении списка названий, а в закрытии выпусков по лестнице: `item/card → holding/page → local file/scan → OCR → visual check → quote-card`.

В v103 подняты несколько самиздатных выпусков до `holdings_page_verified` или `holdings_page_verified_with_variant`, но **ни одна строка не помечена `quote_ready`**, потому что нет полного цикла локальный файл/скан + OCR + визуальная сверка.

## Рабочие группы

- `groups/01_METHOD_AND_WORKFLOW.md` — метод, статусы, доказательная лестница.
- `groups/02_HISTORY_NARRATIVE.md` — исторический каркас.
- `groups/03_PERIODICAL_CORPUS.md` — дореволюционная/межвоенная/официальная периодика.
- `groups/04_SAMIZDAT_PERSECUTION.md` — СЦ ЕХБ, СРУ, самиздат, гонения.
- `groups/05_REPO_AND_PUBLICATION.md` — интеграция в repo и будущую серию.
- `groups/06_DATA_AND_PROOF_LEDGERS.md` — сводные таблицы и рабочие ledgers.

## v103 delta

- Закрыты до `holdings_page_verified`: `Вестник Спасения` 1964 №1, 1972 №1(37), 1974 №1-2(45-46).
- Закрыты/уточнены до `holdings_page_verified`: `Бюллетень СРУ` 1972 №6, 1975 №27, 1979 №61.
- `Бюллетень СРУ 1975 №24` закрыт с вариантом страниц: 44 в item field, 40 в copy-row.
- `BRATSKII LISTOK 1971 №1` поднят до `holdings_verified_no_page_count`, но не выше.
- Обновлены `PROOF_STATUS_LEDGER.csv`, `NEXT_MICROBATCH.csv`, `SOURCE_ANCHORS.csv`.


## v104 update

v104 продолжает TRUE GROUPED-архитектуру: новые сведения добавлены в существующие master-группы и CSV-ledgers. В этом проходе закрыты/уточнены `Бюллетень СРУ 1979 №62`, `Бюллетень СРУ 1979 №64`, master-grid `Вестника Спасения`, master-grid `Бюллетеня СРУ` и OSA-crosscheck для `BRATSKII LISTOK`. Новых `quote_ready` строк нет.


### v105 summary

Продолжен grouped-подход: закрыты дополнительные выпуски Toronto Samizdat до `holdings_page_verified`; новых мелких MD не создано; `quote_ready` не выставлялся.


### v108 summary

Продолжен grouped-подход: закрыт блок `Бюллетень СРУ 1980` по карточкам №75–79, №82, №84–86 и `Вестник Спасения 1967 №3(19)` до уровня `holdings/page`; `quote_ready` не выставлен.


## v108

Focused pass: more issue rows moved to holdings/page verified, but quote-ready remains blocked by lack of local scans/OCR/visual check.


## v108

Added a dense SRU Bulletin verification batch. The archive remains grouped; no per-issue MD files were created.


## v110 update

Closed a dense Toronto Samizdat verification block for Biulleten SRU 1977 no.42–46 and 1978 no.47/49 to holdings/page level. No quote-ready status was assigned; local scan/OCR/visual check remains required.


## v110

Added a SRU 1978 verification batch while preserving grouped architecture. №60 page-count variant 28/66 flagged; №58 has no visible page-count.


## v112 summary

Version v112 continues the TRUE GROUPED architecture. It adds a compact verification pass for `Бюллетень СРУ` 1975 №19–23, №25–26, №28 and 1976 №29. All newly added rows are metadata/holding/page-level only; no `quote_ready` status is assigned without local scan, OCR, and visual verification.


## v112

Added SRU 1972–1974 verification batch while preserving grouped architecture. Page-count variants are preserved, not normalized.


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


## v118 summary
This version extends BRATSKII LISTOK verification into 1983–1986 while preserving TRUE GROUPED architecture. Most new rows are item-designation or holdings without page-count; no OCR/quote-ready status was added.


### v119 update

Added early BRATSKII LISTOK 1965–1966 verification pass. This version keeps the TRUE GROUPED architecture and updates only master-groups plus ledgers. New rows mostly confirm issue existence and selected Baylor/Keston/OSA holdings; no quote_ready status was added.


## v120 update — 1967–1970 BRATSKII LISTOK early block

v120 continues the grouped architecture. It adds an early BRATSKII LISTOK verification pass covering 1967 item-only cards, 1968 page-verified issues, and 1969–1970 holdings-without-page rows. The archive remains non-quote-ready until local file/OCR/visual-check work is completed.
