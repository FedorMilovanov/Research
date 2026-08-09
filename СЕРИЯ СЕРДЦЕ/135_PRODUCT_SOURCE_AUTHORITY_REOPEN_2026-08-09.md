# Heart Product source authority correction — 2026-08-09

**Authority:** `HEART-PRODUCT-SOURCE-AUTHORITY-PARITY-2026-08-09`  
**Corrected current state:** `HEART-ENTRY-CITATION-PASS-CURRENT-V11-2026-08-09`  
**Pinned Product snapshot:** `0fbe7d1ead9ebd1bea867418e254da438ec63329`  
**Calibration manifest SHA-256:** `df4fd39e73c031083d8fad145263281c3be10ededa0a20d14f89b78e64a3b576`

## Почему потребовалась коррекция

Исторический whole-book citation inventory был построен по `src/content/articles/*.mdx`. Текущие Product route profiles для проверенных Heart-страниц уже объявляют эти MDX `reference-only`, а действующим содержательным владельцем — `astro-native-entry` / strict-native route с реально рендеримым `*Body.astro`.

Red-first calibration автоматически взял все Product owner-specs из существующего Heart inventory, разрешил каждый из них через Product route profile и сравнил reference MDX с нативным Body на одном и том же pinned Product snapshot.

Результат: **10 / 10 owner-specs расходятся**, охватывая **9 уникальных native routes**.

Расхождение нельзя списать только на оболочку Astro. Да, в native source появляются служебные URL вроде `schema.org`, Telegram и SVG namespace, но одновременно расходятся реальные citation-bearing surfaces: наборы Scripture references, внутренние article-targets и/или нормализованные quotation manifests.

Поэтому reference-only MDX остаётся допустимым историческим witness, но больше не может считаться текущим citation authority.

## Какие завершённые pass пришлось reopen

Следующие семь entries имели исторически завершённый citation pass, но их Product-backed evidence был проверен не против текущего native source authority:

- `HEART-BOOK-I1`;
- `HEART-BOOK-I3`;
- `HEART-BOOK-I4`;
- `HEART-BOOK-III1`;
- `HEART-BOOK-III4`;
- `HEART-BOOK-X2`;
- `HEART-BOOK-X3`.

Их старые receipts не удаляются и не переписываются. Они остаются immutable historical evidence и требуют отдельной native-authority reconciliation.

Part V и VII также затронуты source-authority divergence, но citation-complete до этой коррекции не были, поэтому их не надо «открывать заново» — они уже были open.

## Исправленная текущая цифра

**CURRENT NATIVE-AUTHORITY CITATION PASSES COMPLETE = 6 / 18**  
**CURRENT CITATION PASSES OPEN = 12 / 18**  
**ASSEMBLED READERS = 14 / 18**  
**MISSING STANDALONE READERS = 4**  
**ASSEMBLED READERS CURRENTLY VALIDATED AGAINST CURRENT AUTHORITY = 6**

Без source-authority разрыва остаются завершёнными:

- `HEART-BOOK-I2`;
- `HEART-BOOK-II`;
- `HEART-BOOK-III2`;
- `HEART-BOOK-III3`;
- `HEART-BOOK-IV`;
- `HEART-BOOK-X1`.

Это не потеря проделанной работы. Это исправление уровня доказательства: прежние citation reviews сохраняются как forensic history, но текущий счётчик больше не выдаёт reference-only MDX за production content authority.

## Что не было тихо закрыто

Остаются открытыми:

- historical Product source repairs: **4**;
- dossier URL HOLDs: **55**;
- dossier source URL repairs: **2**;
- unresolved internal paths: **1**;
- native-source reconciliation для reopened entries: **7**;
- new direct quotes approved: **0**.

Reader assembly Part V остаётся валидным как отдельная транзакция: он изначально был собран и pinned непосредственно к `Rimlyanam7Body.astro`, то есть к текущему native content authority. Его citation pass всё ещё открыт.

## Следующая bounded transaction

**NEXT = HEART-BOOK-V NATIVE-AUTHORITY ENTRY CITATION PASS**

Part V — удобная и честная следующая граница: reader уже существует на native source, но citation pass ещё никогда не заявлялся. Его review должен работать по `Rimlyanam7Body.astro` как primary Product authority и по bounded R3/R4/R5 support owners; reference-only MDX может использоваться только как исторический witness, не как источник текущей полноты.

После этого отдельными транзакциями должны пройти семь reopened entries. Whole-book citation completeness, manuscript bundle и Product release по-прежнему не заявляются.
