# 1 Коринфянам 11:2–16 — MAIN synthesis authority и supersession map

**Дата:** 2026-08-09  
**Статус:** `MAIN-SYNTHESIS-AUTHORITY / MULTI-AGENT-INTEGRATED / 51-URL-VERIFIED / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Цель:** дать одну контролирующую точку входа после сведения всех обнаруженных параллельных агентских веток по 1 Кор. 11:2–16.

## 1. Provenance: что именно сведено

### Agent corpus B

- branch: `arena/019fe62b-research`
- exact imported head: `883593bd3aedb4fbb67d1fb159ab363a847596dd`
- integration PR: `#155`
- основная ценность: `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/`, первичные extracts в `SOURCE_LIBRARY/processed/1COR11_PRIMARY/`, source cards, position sheet, будущая серия `СЕРИЯ ЖЕНЩИНЫ В СЛУЖЕНИИ/`.
- до импорта exact-head CI: `Repository authority integrity` SUCCESS; `Genesis 6 authority manifest` SUCCESS.

### Agent corpus D

- branch: `arena/019fe62d-research`
- exact official remote head: `1ae05904aad93bae59e7b655791c9dea5530758e`
- original transport PR to main: `#156`
- normalized integration PR: `#158`
- основная ценность: `1_КОРИНФЯНАМ_11/` (67 dossiers + 7 site-ready research drafts), `data/1cor11-research-manifest.json`, expanded argument/objection/history/application corpus.
- normalization изменила только transport namespace: исходный generic authority manifest сохранён как `data/1cor11-authority-manifest-arena-d-20260809.json`; конфликтующий generic alias второй ветки не заменяет уже импортированную canonical alias первого корпуса. Root README second-corpus transport был возвращён к base authority до merge. Исследовательские 74 документа не переписывались.
- exact normalized head CI: `Repository authority integrity` SUCCESS.

### Older shared Greek work

- commit `85c5f6a65c249cdcddcac37572ab5103b8a18dc5`
- прямой Greek analysis 1 Cor 11 + 1 Peter/2 Peter/Jude используется как исторический research input, но текущую степень уверенности контролирует этот overlay и `00Z_FINAL_CLAIM_CALIBRATION`.

## 2. Почему оба корпуса сохранены

Не выполняется destructive “choose one folder and delete the other”. Две независимые линии несут разную доказательную ценность:

- `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/` — source/evidence-oriented foundation, primary extracts, claim/position controls;
- `1_КОРИНФЯНАМ_11/` — расширенная аналитическая система и article architecture.

Исторические расхождения не скрываются. Они разрешаются **overlay authority**, так что можно восстановить, что утверждал каждый агент и почему итоговая формулировка изменилась.

## 3. Текущий порядок authority

При противоречии читать в таком порядке:

1. **`00Z_MAIN_SYNTHESIS_AUTHORITY_AND_SUPERSESSION_2026-08-09.md`** — ownership, provenance, publication boundary.
2. **`00Z_FINAL_CLAIM_CALIBRATION_2026-08-09.md`** — controlling confidence/wording и explicit supersessions.
3. **`00Z_51_EXTERNAL_VERIFICATION_LEDGER_2026-08-09.md`** — внешний verification receipt и границы проверок.
4. `1_КОРИНФЯНАМ_11/21_CLAIM_CALIBRATION_AND_FAIL_CLOSED_AUDIT.md` — сильный внутренний correction overlay второй ветки, если не противоречит 00Z.
5. `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/36_POSITION_SHEET_AND_EVIDENCE_BALANCE_2026-08-09.md` — Q1–Q10 synthesis первого корпуса, если не противоречит 00Z.
6. Тематические dossiers/source cards/primary extracts обоих корпусов.
7. Site-ready research drafts ARTICLE_1–7 — **не publication authority**; всегда читаются через overlays выше.
8. Более ранние foundation/agent status files — historical provenance only там, где поздний overlay их исправляет.

## 4. Канонический итог по ключевым узлам

### Текстология

- GNT6 — опубликованная текущая UBS Greek NT edition.
- NA28 — текущая опубликованная Nestle-Aland на 2026-08-09.
- NA29 официально ожидается 2027-02-28; GNT6 сообщает, что его text совпадает с будущим NA29.
- Завершённую ECM Pauline letters не заявлять.
- Перикопа имеет сильную раннюю manuscript attestation; это не заменяет полного apparatus-level census.

### Участие женщин

- 11:5 прямо предполагает женщину, которая молится/пророчествует.
- Это нельзя стереть интерпретацией 14:34–35.
- Но 11:5 также нельзя использовать как единственный proof-text для окончательного решения office/pastorate/ordination.

### `κεφαλή`

- Leading synthesis: headship/authority/predominance **B / probable**, с реальным origin/source dimension в argument flow.
- Source-only reading = **C / viable alternative**, не “refuted”.

### Покрытие и волосы

- Material head covering = **B-high / probable**.
- Hair/hairstyle-only = **C / serious alternative**.
- Конкретная современная форма предмета из текста с A-certainty не восстанавливается.

### 11:10 `ἐξουσία`

- A-level core: женщина — grammatical subject `ἔχειν`; `ἐξουσία` означает authority/right/power.
- “Sign of husband’s authority” — традиционное/контекстуальное interpretation, но не lexical replacement слова.

### Ангелы

- A-level minimum: angels are invoked; identity/function are unstated.
- Holy/liturgical angels = **B / leading probable reading**.
- Watchers/fallen angels = **C / ancient but weaker Tertullian line**.

### Roman Corinth

- Male head-covered Roman cult practice = **A historical background**.
- Identification of v.4’s actual Corinthian problem specifically with that practice = **B reconstruction**.
- Portraiture/status/new-woman models are useful, but background data must not replace textual argument.

### Wives vs all women

- `γυνή` scope across 11:2–16 is **OPEN** at the all-women-vs-wives boundary; contemporary scholarship explicitly lacks consensus.

## 5. Что было исправлено при синтезе

- `NA29 current` → corrected to future release 2027-02-28.
- `Pauline ECM complete` → corrected to not completed/published as full Pauline ECM.
- “75 strictly verified sources” → recast as mixed verification registry; no source-count inflation.
- exact P46 folio/page → HOLD unless directly acquired/inspected.
- `kephale source refuted` → superseded.
- `hair-only refuted` → superseded.
- `holy angels certain` → B.
- `Watchers direct Pauline meaning` → C.
- `capite velato proves Corinthian Christian action` → B reconstruction.
- all-women/unmarried scope settled → OPEN.
- “Schreiner wrote ESV Expository Commentary on 1 Corinthians” → corrected: **Andrew David Naselli** wrote the 1 Corinthians contribution in the Romans–Galatians ESVEC volume.

## 6. External verification receipt

`00Z_51_EXTERNAL_VERIFICATION_LEDGER_2026-08-09.md` records **51 URL checks** across:

- official text-critical publishers/institutes;
- manuscript/institutional archives;
- Greco-Roman/Jewish primary texts;
- Qumran objects and scholarship;
- patristic texts;
- peer-reviewed lexical/exegetical debates;
- archaeology/material-culture studies;
- 1 Cor 14 manuscript debate;
- official publisher bibliographic verification for major commentaries.

Count discipline:

```text
51 URL CHECKS
≠ 51 FULL BOOKS READ
≠ 51 PAGE-LEVEL CLAIM CLOSURES
```

## 7. Research-main vs publication

После успешного final exact-head CI этот corpus может быть **merged into Research `main`** как consolidated research authority.

Это **не** означает:

- Product write;
- публикацию ARTICLE_1–7;
- снятие rights/quote/page holds;
- превращение B/C claims в A;
- закрытие отдельной серии о женщинах в служении.

Контролирующий state:

```text
RESEARCH_MAIN_READY = true (after final CI)
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
DIRECT_QUOTE_PROMOTION = false unless separately verified
```

## 8. Следующий отдельный gate после MAIN

Если серия пойдёт на сайт, нужен отдельный publication transaction:

1. page-level acquisition для ключевых закрытых комментариев (Thiselton, Fee, Ciampa/Rosner, Garland и др.);
2. direct-quote/rights audit;
3. отдельная редактура ARTICLE_1–7 через 00Z calibration;
4. Product lane record и exact pinned Research commit;
5. Product CI/QA.

Ни один из этих этапов не следует молча из Research merge.