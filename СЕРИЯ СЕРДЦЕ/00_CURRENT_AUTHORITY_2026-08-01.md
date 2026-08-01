# CURRENT AUTHORITY — «СЕРИЯ СЕРДЦЕ»

**Дата:** 2026-08-01  
**Статус:** текущая точка входа для Research, source-verification и Site-closure.  
**Research authority:** `FedorMilovanov/Research@35403816164af8d400c8d0e0b811b5e230d2d7c1` — PR `#77`.  
**Site implementation:** `FedorMilovanov/gb-is-my-strength@49ad224145957325559d50286579a9c032b19629` — PR `#510`.  
**Exact Site PR head:** `c9af888684ad9ee919422ad31ad1a351546d73e6`, все `15/15` triggered workflows успешны.  
**Verified production ancestry:** Site merge `49ad2241…` является предком exact source/production authority `abf1edba190280e554dfda085bef9fb6594c896d`.

---

## 1. Правило чтения корпуса

Этот файл является **текущей status-authority**. Он не переписывает исторические исследования и не отменяет их содержательные выводы.

- `72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md` — точный исторический snapshot после ранних merge, но **до** окончательного Site cleanup PR `#510` и Research PR `#77`.
- `73_OPEN_VERIFICATION_BACKLOG_2026-07-31.md` — хронологический audit/closure ledger. Ранние секции сохраняют состояние на момент соответствующего прохода; их нельзя читать как текущий backlog без сверки с §8, §13 и этим документом.
- `61_BOOK_ARCHITECTURE_V2_CHAPTERS_AND_RESEARCH_TASKS.md` — архитектурный план. Его последовательные owner-revisions сохраняются; текущие незакрытые решения перечислены ниже.
- `62_R1…`–`71_R9…` — substantive research dossiers. Их локальные исторические caveats сохраняются, но текущий статус определяется последними safe-closure записями и правилами этого файла.

**Supersession распространяется только на изменяемые факты:** open/closed, merge state, Site implementation, source-lock и evidence-boundary. Исторические даты, доказательства и ограничения источников остаются неизменными.

---

## 2. Что реально закрыто в Research

Research PR `#77` не превратил каждый источник в печатное A+ издание. Он сделал более важную вещь: для каждого существенного кандидата установил честный допустимый режим использования.

### R1 — рождение свыше

- Gill, Bavinck excerpt, Boston и официальный Sproul source-layer закрыты на уровне доступного первичного/open или official текста.
- Whitefield anecdote заблокирован как документированный факт.
- Carson / Schreiner / Kruse разрешены только как position-locator / paraphrase, пока книга не открыта напрямую.
- Остаток: optional print-page/edition policy, а не blocker для богословского каркаса.

### R2 — возрождение и обитание Духа в ВЗ

- Hamilton Themelios и TrinJ spectrum, Calvin, Augustine, Gill, Warfield и Owen закрыты на уровне доступных текстов/локаторов.
- Ferguson book и Hamilton monograph direct quotes остаются book-page hold / optional.
- Остаток не должен ошибочно называться незакрытой основной экзегезой.

### R3 — борьба без возрождения

- Calvin и латинский locus Augustine `Contra Julianum IV.3.25` закрыты.
- `splendida vitia` остаётся reception-label, а не прямой цитатой Августина.
- Watson aphorism и апокрифический Spurgeon заблокированы для direct quote.

### R4 — четыре почвы

- Calvin, Thomas Taylor open text, официальный Spurgeon и Ryle закрыты.
- Whitefield остаётся attributed-only.
- France / Carson — no-direct-quote / paraphrase-only.
- Досье является content-ready при соблюдении этих границ.

### R5 — две борьбы

- Owen `Mortification`, Mead step VII / Agrippa / false peace, Augustine VIII.9.21, Spurgeon Luke 18:13 и Edwards heading locators закрыты.
- Остаток: optional broader Mead QII–V и body-level Edwards extraction только при необходимости прямой цитаты.

### R7a — сердце и Слово

- Calvin, Gill, Manton и open-reference Hebrews 4:2 layer закрыты.
- Metzger exact rating намеренно снят с обязательного использования: `NO-DIRECT-METZGER-QUOTE`.
- Lane / O’Brien / Schreiner / Ellingworth / Attridge — not-checked / no-direct-quote, не blocker.
- Owen “burn our Bibles” — secondary attribution only, не цитировать как Owen.

### R7b — фарисей и ученик

- Gill Acts 17:11, официальный Spurgeon, Whitefield и Ryle закрыты на открытых/официальных текстах.
- Carson, Lloyd-Jones и snippet-only Ryle extra не цитируются напрямую.
- Остаток: optional translation/editorial refinement, а не source-risk ядра.

### R8 — созерцание славы Христа

- Ключевые Owen `Glory of Christ` quote-cards получили CCEL chapter locators.
- Calvin, Chalmers, M’Cheyne letter page и официальный Spurgeon support locator закрыты в своих evidence classes.
- Hughes wording заблокирован как direct quote.
- MLJ official sermon page можно использовать только как metadata/description; direct sermon quote не заявляется.
- Остаток: editorial placement грамматического экскурса, optional print pagination и возможный dedicated-sermon search.

### R9 — Христос Откровения

- Gill Revelation subset, Ryle, ключевые GTY transcripts, официальный Ligonier Sproul subset, официальный Crossway Ortlund balance, Goodwin short PDF-text anchors, Calvin Isaiah 63 и подтверждённые Spurgeon locators закрыты в явно названных evidence classes.
- Ortlund book-page wording, aggregator-only Sproul lines, Baucham claim и апокрифические Spurgeon snippets заблокированы.
- Главный остаток — архитектурная роль R9 и optional commentary depth по Откр. 19:13, а не общая непроверенность досье.

---

## 3. Что закрыто на Site

### Issue `#509` — TOC / reading time / progress

Закрыто Site PR `#510`:

- TOC parity: `12/12` H2;
- reading time: `34` минуты;
- ordered reading sequence: `24` страницы;
- total series minutes: `727`;
- source-of-truth config используется вместо runtime DOM patch;
- exact PR head прошёл `15/15` workflows.

Следовательно, строки V84I/backlog, называющие PM-003/PM-004 открытыми, являются историческими.

### Issue `#513` — Timothy Rogers scan-first provenance

Закрыто Site PR `#510` визуальной проверкой скана 1691 года:

- Advice 1 — printed page `ii`, PDF page `17`;
- Advice 5 — printed page `xii`, PDF page `27`;
- Advice 6 — printed page `xiv`, PDF page `29`.

В Site сохранены provenance/locator records и минимальные snippets; scan binaries не коммитились. Поэтому прежний Research-only отрицательный boundary был корректен для sandbox-состояния, но больше не является текущим Site blocker.

### `/hard-texts/` landing

PR `#510` завершил book-shaped landing cleanup и связанный reader/source contract. Старое обозначение PM-005 как open cleanup path является историческим.

### Production boundary

Site merge `49ad2241…` находится в ancestry exact source/production authority `abf1edba…`. Это позволяет считать PR `#510` не только source-merged, но и присутствующим в подтверждённой production ancestry. Более поздние source-коммиты требуют собственных production witnesses и не меняют этот факт об immutable release ancestry.

---

## 4. Текущий настоящий backlog

### Архитектура P0

Отдельного законченного R-досье пока нет для:

1. I.2 `Сердце в Эдеме`;
2. III.3 `Сокрушённое сердце: покаяние`;
3. X.1 `Суд сердца: два воскресения`.

Это **content-architecture gaps**, а не незакрытые цитатные ошибки существующих R1–R9.

### Архитектурные решения

- определить роль R9: standalone article, support block R8 или support для X.1;
- решить объём `κατοπτριζόμενοι` excursus в R8: main text, note/dropdown или сокращение;
- нормализовать окончательную chapter table, если owner изменит утверждённую структуру ещё раз.

### Optional evidence upgrades

Не являются blocker по умолчанию:

- печатные страницы при уже закрытом HTML/chapter locator;
- legal owned edition для MLJ/Ferguson/Hamilton/других book-only sources;
- page-image pass для длинных новых PDF quotations;
- дополнительные современные комментарии, если статья уже несёт аргумент Писанием и закрытыми первичными источниками.

### Hard blocks — не использовать без нового первичного доказательства

- Baucham “sissified/needy Jesus”;
- апокрифические Spurgeon lion/lamb и free-will aphorisms;
- Hughes “expulsive force” как цитата Hughes;
- Owen “burn our Bibles” как прямая цитата Owen;
- `splendida vitia` как дословная формула Августина;
- secondary/aggregator wording, которое в dossier помечено `DO-NOT-DIRECT-QUOTE`.

---

## 5. Текущий порядок работы

1. Этот файл — current mutable status authority.
2. `61_BOOK_ARCHITECTURE…` — план статей и приоритетов.
3. Нужный R-досье — substantive evidence и article material.
4. `73_OPEN_VERIFICATION…` §8 и §13 — подробный closure ledger, но с учётом Site PR `#510` и этого supersession.
5. V81–V84I — историческая цепочка решений и evidence boundaries.
6. Любая новая прямая цитата проходит правило: точный текст, автор, работа, locator, context и явно названный evidence class.

---

## 6. Короткий итог

```text
RESEARCH PR #77: MERGED / SOURCE-BOUNDARIES NORMALIZED
SITE PR #510: MERGED / 15 OF 15 WORKFLOWS
SITE ISSUES #509 AND #513: CLOSED COMPLETED
PR #510 MERGE: INCLUDED IN VERIFIED PRODUCTION ANCESTRY
R1–R9: MOSTLY SOURCE-LOCKED OR HONESTLY BOUNDED, NOT GENERICALLY OPEN
TRUE REMAINDER: THREE P0 DOSSIER GAPS + EDITORIAL/ARCHITECTURE DECISIONS + OPTIONAL EDITION UPGRADES
```
