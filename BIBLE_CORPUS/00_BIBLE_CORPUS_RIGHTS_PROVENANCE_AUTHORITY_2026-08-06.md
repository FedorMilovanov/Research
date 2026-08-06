# Bible corpus rights and provenance authority

**Date:** 2026-08-06  
**Status:** `VERIFIED DECISION / ARCHIVE_HOLD + RIGHTS_HOLD + PUBLICATION_HOLD`  
**Case:** `SEARCH-P2-07`  
**Research base:** `c3f7ea27bfc8a10f2369ae90a89107faea8257bf`  
**Product evidence anchor:** `76737eefe16a0feb2fdf729c805d17b5cdcdc376`  
**Machine ledger:** [`../data/bible-corpus-rights-provenance-2026-08-06.json`](../data/bible-corpus-rights-provenance-2026-08-06.json)

## Проверяемый вопрос

Можно ли честно и законно превратить текущий разреженный `data/bible/**` в полный публичный 66-книжный корпус для поиска и библейских всплывающих ссылок?

Краткий ответ: **пока нет**. Текущий Product не содержит достаточной provenance/rights-цепочки. При этом найден один конкретный сильный кандидат — точный модуль CrossWire `RusSynodal` 1.9.1, который официальный реестр CrossWire обозначает как `Public Domain`. Кандидат ещё не получен побайтно, не хеширован и не сопоставлен с 66-книжной схемой Product. Кассиановский Новый Завет остаётся `PERMISSION_REQUIRED`.

Research closure этого вопроса не является Product publication approval.

## Текущий Product-факт

Текущий Product реестр:

- содержит 66 протестантских книг;
- назначает `synodal` по умолчанию для Ветхого Завета;
- назначает `kassian` по умолчанию для Нового Завета;
- требует для канонических записей отдельные `translation`, `source`, `sourceUrl` и `rights`.

Exact Product owners:

| Owner | Blob | Current evidence |
|---|---|---|
| `data/bible/books.json` | `1df1830241657e13efba43ebd27397dbdc46bbc7` | 66-book registry; OT=`synodal`, NT=`kassian` |
| `scripts/bible-reference-contract.mjs` | `5b5d3cb368990b7069dd657ef563a8af3491954f` | source/sourceUrl/rights metadata contract |
| `data/bible/synodal/bytie.json` | `4f0e2a6e6b7481442bfb12b39934e3e93be66eea` | source label exists; `sourceUrl` and `rights` absent |
| `data/bible/kassian/matfeya.json` | `02ca5a53cc0036f06f425456914fb6eba36b0391` | source is only “open web publications”; `sourceUrl` and `rights` absent |

The current corpus therefore has operational text records but not a publication-grade rights chain.

## Первичные источники и локаторы

### 1. CrossWire `RusSynodal` 1.9.1

- Module record: <https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=RusSynodal>
- Copyright record: <https://www.crosswire.org/sword/copyright/ModInfoCopyright.jsp?modName=RusSynodal>
- Resolved raw-package endpoint: <https://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/RusSynodal.zip>
- Evidence class: `A3`
- Locator: exact module/copyright records verified
- Rights state: `PUBLICATION_ELIGIBLE` for the exact identified module
- Publication state: `REFERENCE`
- Holds: `ARCHIVE_HOLD`, `PUBLICATION_HOLD`

The module record identifies version `1.9.1 (2020-12-21)`, language `ru`, and `Distribution License: Public Domain`. The independent CrossWire copyright record repeats `Public Domain`.

The raw ZIP endpoint was resolved from the official module download flow, but the current execution environment could not acquire the archive. Therefore this wave asserts **no archive SHA-256, no embedded configuration bytes and no book manifest**.

### 2. CrossWire `RusSynodalLIO` 1.0.3

- Module record: <https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=RusSynodalLIO>
- Copyright record: <https://www.crosswire.org/sword/copyright/ModInfoCopyright.jsp?modName=RusSynodalLIO>
- Evidence class: `A3`
- Rights state: `PERMISSION_REQUIRED`
- Publication state: `BLOCKED`
- Holds: `RIGHTS_HOLD`, `PUBLICATION_HOLD`

CrossWire labels this modified Licht im Osten edition as copyrighted and says permission to distribute was granted to CrossWire. That statement is not a general downstream licence. This module is rejected as an unlicensed Product corpus source.

### 3. Кассиановский Новый Завет

- Official RBO catalog record: <https://biblia.ru/catalog/Portions/2039/>
- Corroborating permitted web publication: <https://only.bible/bible/cas/>
- Evidence classes: `A3` for RBO; `B1` for the downstream permission notice
- Rights state: `PERMISSION_REQUIRED`
- Publication state: `BLOCKED`
- Holds: `RIGHTS_HOLD`, `PUBLICATION_HOLD`

The official RBO catalog states that a 2023 Cassian edition was published with permission of the Russian Bible Society. A downstream online publisher separately states that its placement is by permission and identifies RBO as the Russian rights administrator. Neither source grants this Product repository permission.

The current Product wording “сверено по открытым публикациям перевода через веб-поиск” proves neither provenance nor publication rights.

## Ответы, отрицания и альтернативы

### Accepted candidate

`CrossWire RusSynodal 1.9.1` is the only candidate promoted by this wave to `CANDIDATE_ONLY`.

This means:

- exact institutional identity is known;
- exact version is known;
- CrossWire's distribution record says Public Domain;
- acquisition, hashing, extraction and Product mapping remain mandatory.

### Rejected alternatives

- `RusSynodalLIO`: rejected without a separate downstream licence.
- Current Cassian web-derived records: blocked from expansion or corpus publication without explicit permission.
- Generic GitHub datasets, scraped Bible sites and unattributed JSON mirrors: not evaluated and not approved. URL accessibility is not rights evidence.
- Reconstructing a “full Bible” by mixing translations or silently copying visible web text: prohibited.

### Not decided here

This dossier does not decide whether Product should ultimately use:

- the exact `RusSynodal` text for both Testaments;
- another independently licensed complete Russian translation;
- a deliberately mixed corpus with separate per-book licences.

Any mixed strategy would require an explicit per-translation rights and reader-disclosure design.

## Анализ и границы допустимой формулировки

Allowed statement:

> CrossWire's official records identify the exact `RusSynodal` 1.9.1 module as Public Domain, making it a concrete acquisition candidate. Product publication remains blocked until the official archive is acquired, hashed, inspected and mapped.

Forbidden statements:

- “Любой Синодальный текст в интернете находится в public domain.”
- “CrossWire разрешил использовать `RusSynodalLIO` где угодно.”
- “Кассиан свободен, потому что текст доступен на сайте.”
- “SEARCH-P2-07 закрыт.”
- “Полный корпус уже получен.”
- “Research approval equals Product publication approval.”

The exact module identity matters. CrossWire explicitly publishes modules under different licence states; a generic translation name is not enough.

## Хронология

1. Product created a canonical 66-book registry and a governed `data/bible/**` authority.
2. Conflicting legacy `data/verses.json` authority was removed in the earlier Product wave.
3. `SEARCH-P2-07` remained open because corpus completeness and rights/provenance were not established.
4. This wave verified the current Product metadata gap.
5. This wave identified CrossWire `RusSynodal` 1.9.1 as a concrete Public Domain candidate.
6. The official ZIP endpoint was resolved, but archive acquisition failed in the current environment.
7. Cassian and `RusSynodalLIO` remain permission-controlled for this Product.

## Права, архив и публикационные HOLD

### Current Product corpus

- `rightsState`: `RIGHTS_UNKNOWN` for current Synodal records; `PERMISSION_REQUIRED` for Cassian records
- `publicationState`: `BLOCKED`
- Holds: `RIGHTS_HOLD`, `PUBLICATION_HOLD`

### `RusSynodal` candidate

- Institutional licence record: verified
- Archive bytes: not acquired
- SHA-256: not available
- Book manifest: not verified
- Versification mapping: not verified
- Product import manifest: absent
- Holds: `ARCHIVE_HOLD`, `PUBLICATION_HOLD`

### Cassian

- Explicit Product permission: absent
- Rights state: `PERMISSION_REQUIRED`
- Publication state: `BLOCKED`
- Holds: `RIGHTS_HOLD`, `PUBLICATION_HOLD`

## Следующее проверяемое действие

A later acquisition/implementation wave must:

1. acquire the exact official `RusSynodal.zip`;
2. record byte length and SHA-256 before extraction;
3. verify embedded module version, `DistributionLicense`, `TextSource` and complete book manifest;
4. map only the 66 Product books and document any `Synodal` / `SynodalProt` versification conversion;
5. generate a verse-level import receipt;
6. compare every existing canonical Product record and explicitly disposition translation changes;
7. populate exact `sourceUrl` and `rights` metadata;
8. run source, corpus, search, production-like dist and browser witnesses;
9. keep Cassian out of the public corpus unless written permission is obtained.

## Disposition

- `SEARCH-P2-07`: **remains open**.
- Current Product corpus: `BLOCKED` for full-corpus publication.
- CrossWire `RusSynodal` 1.9.1: `CANDIDATE_ONLY`.
- CrossWire `RusSynodalLIO`: `REJECT_UNLICENSED_DOWNSTREAM_USE`.
- Cassian: `DO_NOT_EXPAND_OR_REPUBLISH_WITHOUT_PERMISSION`.
- Product writes: none.
- AuditRepo matrix movement: none.
- Production/live claim: none.
