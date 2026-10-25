# PR №2 — без потерь: восстановление evidence archive и supersession-карта

**Дата восстановления:** 2026-07-24  
**Статус:** `LOSSLESS-RECOVERY / PROVENANCE-PRESERVED / CURRENT-MAIN-NOT-ROLLED-BACK`  
**Объект:** закрытый `FedorMilovanov/Research#2`, ветка `audit/gill-final-master-2026-07-09`, head `aeb7526d5910f26bb98408684463d9f357c508e5`.

---

## 1. Зачем создан этот entrypoint

PR №2 был закрыт как superseded после появления томов 43–73. Повторная проверка показала, что это было верно только для **текущих решений**, но неверно для **полноты provenance**:

- в `main` не находился полный накопительный архив `GILL-CONTENT-001…480`;
- расширенная редакция `AGENT_RULES.md` из PR №2 не находилась в `main`;
- supersession-матрица из редакции тома 31 не находилась в `main`;
- README-снимок PR №2 также не был сохранён как отдельный исторический слой.

Поэтому закрытый PR не переоткрывается и не вливается поверх современного дерева целиком. Вместо этого все четыре его содержательных blob восстанавливаются **byte-for-byte** как provenance, а позднейшие тома и актуальный `main` сохраняют приоритет.

---

## 2. Полный инвентарь PR №2

PR менял ровно четыре файла:

| Исходный путь в PR №2 | Git blob SHA | Что сделано теперь |
|---|---|---|
| `AGENT_RULES.md` | `3c9fc503839335e37a29e5e7bbf46d1738d44a00` | сохранён точный снимок в `incoming/.../pr2-lossless-snapshots/` |
| `Джон Гилл/00_README_AND_NAVIGATION.md` | `e59a297ee6bcea6c10c5fd34de5f76b8e7cc78b8` | сохранён точный снимок в `incoming/.../pr2-lossless-snapshots/` |
| `Джон Гилл/31_GILL_DEPT_MASTER_MAP.md` | `dc0fc2de8885e85c58122f142ae0a945a36e6b3b` | сохранён точный снимок в `incoming/.../pr2-lossless-snapshots/` |
| `incoming/arena-auditor/2026-07-09/GILL_SERIES_EVIDENCE_ARCHIVE_V1_V11_001_480_2026-07-09.md` | `baa3fccb6f67cd05117b2c4f0342867662a3fce0` | восстановлен по исходному пути |

Параметры полного evidence archive из PR №2:

- диапазон: `GILL-CONTENT-001…480`;
- размер: **431 460 bytes**;
- строки: **11 557**;
- SHA-256: `86834ecb1f90775de6876c91cafab054450914b521291ad3dd7522823c612f14`;
- Git blob SHA: `baa3fccb6f67cd05117b2c4f0342867662a3fce0`.

Это означает, что ни одна из 480 накопительных карточек, ранних исправлений, HOLD-пунктов, route observations, source notes или редакционных предупреждений не удалена.

---

## 3. Где лежат восстановленные материалы

### Полный архив 001–480

`../incoming/arena-auditor/2026-07-09/GILL_SERIES_EVIDENCE_ARCHIVE_V1_V11_001_480_2026-07-09.md`

### Точные снимки трёх управляющих файлов PR №2

`../incoming/arena-auditor/2026-07-09/pr2-lossless-snapshots/AGENT_RULES_PR2_2026-07-09.md`

`../incoming/arena-auditor/2026-07-09/pr2-lossless-snapshots/GILL_README_PR2_2026-07-09.md`

`../incoming/arena-auditor/2026-07-09/pr2-lossless-snapshots/GILL_MASTER_MAP_PR2_2026-07-09.md`

Снимки нельзя молча копировать обратно поверх современных файлов: они фиксируют состояние и terminology на 9 июля 2026 года.

---

## 4. Что действительно superseded, а что нельзя терять

### Superseded как текущая инструкция

- snapshot сайта `d00715e9…`;
- инвентарь, ограниченный томами `01–42`;
- старые route paths и ранняя архитектура компонентов;
- ранние P0/P1 totals;
- старые формулировки, позднее исправленные томами 43–73 и production-коммитами;
- внутренняя taxonomy архива, включая исторический `Level D`;
- отдельные provisional hypotheses и неподтверждённые причинные связи.

### Не superseded как provenance

- полный audit trail `001–480`;
- точные ранние цитаты, locators и negative-search results;
- список исторических ошибок и overstatements;
- ранние HOLD и unresolved items;
- route-by-route наблюдения для понимания происхождения исправлений;
- supersession-матрица PR №2;
- правила разделения source class, access host, evidence grade и claim status;
- предупреждения против false-green и самоподтверждения текста сайта.

Закрытие PR не должно означать удаление этих оснований.

---

## 5. Канонический порядок чтения после восстановления

1. `00_README_AND_NAVIGATION.md` — современная карта томов 01–73 и текущая архитектура серии.
2. `72_PRIMARY_SOURCE_40_PLUS_DIRECT_LINK_LEDGER_AND_CLOSURE.md` — строгий реестр 56 A1/A2-точек.
3. `73_PRIMARY_LINK_HEALTH_60_UNIQUE_URL_ACCEPTANCE.md` — двухпроходная приёмка прямых URL.
4. `70_FINAL_50_PLUS_SOURCE_REVERIFICATION_AND_PUBLICATION_LEDGER.md` и `71_POST_MERGE_40_PLUS_SOURCE_COVERAGE_AND_EXPANSION_DECISION.md` — publication gate и решение по объёму.
5. Томá 43–69 — тематическая проверка, PDF-аудит, корпусные синтезы и implementation ledgers.
6. Этот файл — lossless crosswalk закрытого PR №2.
7. Полный archive `001–480` и три snapshot-файла — историческое доказательство и источник для повторной проверки, но не автоматическая current truth.

Если формулировка в archive конфликтует с поздним томом, применяется поздний том при сохранении ранней записи как provenance.

---

## 6. Тематический охват архива 001–480

Архив сохраняет, среди прочего:

- биографическую хронологию, семью, обращение, служение и образование;
- печатные труды, даты, edition mapping, объёмы и библиографию;
- Hebrew/Judaica, раввинистические источники и риски анахронизма;
- Троицу, христологию, пневматологию, завет и eternal justification;
- *The Cause of God and Truth*, universal texts, duty-faith, offer/proclamation и external call;
- Gill–Whitefield, Spurgeon, Brown, Gillites/Fullerites и спор о баптистском упадке;
- закон, добрые дела, Practical Divinity, церковь, государство, worship и ethics;
- legal/dissent context, academies, coffeehouses и локальную историю;
- image provenance, captions, glossary, tooltips, quiz/SEO/body drift и route-level risks;
- точные ошибки, осторожные формулировки, HOLD, negative results и необходимые источники.

Поэтому архив нельзя считать «дубликатом поздних томов»: поздние тома дают более надёжные решения, а архив сохраняет полный путь к ним и длинный хвост наблюдений.

---

## 7. Почему активные файлы не заменены версиями PR №2

### Корневой `AGENT_RULES.md`

Версия PR №2 существенно сильнее старого файла по source taxonomy и parallel-work safety, но это корневой документ всего Research, а не только Gill-lane. Его точный blob сохранён; отдельное глобальное принятие должно проходить без скрытого влияния на параллельные отделы.

Для Gill-lane актуальные уровни `A1/A2/A3/B1/B2/B3/C1/C2/X` уже закреплены в современном `00_README_AND_NAVIGATION.md` и поздних source ledgers.

### `00_README_AND_NAVIGATION.md`

Современный файл содержит тома 43–73 и текущую шестичастную архитектуру сайта. Замена его снимком 9 июля откатила бы позднюю работу.

### Том 31

Современный том 31 остаётся исторической картой `01–30`; README прямо так его маркирует. Улучшенная supersession-матрица PR №2 сохранена точным snapshot-файлом и не теряется.

---

## 8. Acceptance gates

Восстановление считается корректным только если одновременно выполнено всё:

- [x] все четыре blob SHA PR №2 перечислены;
- [x] archive `001–480` возвращён по исходному пути;
- [x] три управляющих файла сохранены byte-for-byte как snapshots;
- [x] актуальные `AGENT_RULES.md`, README и том 31 не откатились;
- [x] тома 43–73 не изменены и не удалены;
- [x] production-код сайта не затронут;
- [x] закрытый PR №2 остаётся закрытым и не может случайно перезаписать современный `main`;
- [x] precedence между современными решениями и историческим archive описан явно.

---

## 9. Итоговый verdict

```text
PR #2 UNIQUE CONTENT
→ NOT LOST
→ PRESERVED BYTE-FOR-BYTE
→ HISTORICAL PROVENANCE RETAINED

CURRENT GILL RESEARCH
→ VOLUMES 01–73 RETAINED
→ LATE SOURCE LEDGERS GOVERN
→ NO ROLLBACK TO JULY 9 SNAPSHOT

CLOSED PR #2
→ REMAINS CLOSED
→ SAFE FROM ACCIDENTAL MERGE
→ ALL FOUR CONTENT BLOBS REACHABLE FROM CURRENT MAIN AFTER MERGE
```

Гилл-lane может считаться lossless только после проверки, что перечисленные blob SHA действительно доступны из итогового `main`.