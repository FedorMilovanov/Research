# Отступничество — reconciliation трёх параллельных research-корпусов

**Дата:** 2026-09-30  
**Статус:** `CURRENT WORKING HANDOFF / RESEARCH-ONLY / PUBLICATION_HOLD`  
**Глобальная рамка:** `00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md` + `data/repository-evidence-policy-v2.json`  
**Цель:** прекратить размножение параллельных досье и продолжать исследование из одного рабочего spine без потери уже добытого материала.

> Этот файл выбирает **рабочий research spine данной темы**, но не является сам по себе publication authority и не разрешает перенос материала в Product. Research presence ≠ publication approval.

---

## 1. Что обнаружено

На `Research/main` одновременно существуют три каталога, посвящённые почти одной и той же теме:

1. `apostasy/` — наиболее полный систематизированный корпус: master research map, biblical corpus/categories, отдельный Judas Iscariot dossier, Hebrews 6, Hebrews warning system/10:29, historical theology, disputed NT texts, publication architecture и source registry 70+.
2. `APOSTASY/` — более поздний/параллельный supporting layer: большой biblical-theology dossier, отдельная матрица warnings в Hebrews и сравнительная case matrix.
3. `ОТСТУПНИЧЕСТВО/` — ещё один параллельный слой с двумя master-файлами, глубоким Heb 6/10 материалом, отдельным 2 Peter deep dive и 2026-09-30 exegetical dossiers.

Проблема не в качестве самих материалов, а в **authority drift**: агент, читающий только один каталог, может заново исследовать уже закрытый узел, дать ему новый parent, создать третью формулировку статуса и затем не знать, какой файл надо переносить в Product.

---

## 2. Решение: единый рабочий spine

До создания отдельного corpus authority по правилам control plane **каноническим рабочим research spine этой темы считается `apostasy/` (lowercase)**.

Причины:

- в истории `main` именно для этой линии существует отдельный commit `research(apostasy): establish canonical master dossier`;
- здесь уже находится самая полная структура evidence → exegesis → historical models → publication architecture → source registry;
- `apostasy/07_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-09-29.md` уже привязан к реальной архитектуре Product;
- `apostasy/08_SOURCE_REGISTRY_70_PLUS_2026-09-29.md` уже является evidence registry, а не просто bibliography;
- `APOSTASY/00_APOSTASY_BIBLICAL_THEOLOGY_DOSSIER.md` сам заявляет, что является `supporting research dossier` и **не является root/corpus authority**;
- `ОТСТУПНИЧЕСТВО/` создан позднее и содержит ценные усиления, но не сопровождается отдельной authority-chain, которая supersede-ит lowercase corpus.

### Нормативная формула

`apostasy/` = **working canonical research spine**.  
`APOSTASY/` = **supporting overlay / comparative matrix lane**.  
`ОТСТУПНИЧЕСТВО/` = **late overlay / deep-dive salvage lane**.

Это не означает, что старшие/параллельные каталоги надо немедленно удалить. Наоборот: до content-completeness diff они сохраняются как forensic/source material.

---

## 3. Что уже считать закрытым как «не надо делать заново»

### 3.1. Иуда Искариот

Canonical working dossier уже существует:

- `apostasy/02_JUDAS_ISCARIOT_EXEGETICAL_DOSSIER_2026-09-29.md`.

Поэтому следующий агент **не должен заново “начинать досье Иуды”**. Следующая работа — source-to-claim hardening, exact locators, counter-reading pass и подготовка publication candidate.

### 3.2. Евр. 6

Canonical deep work уже существует:

- `apostasy/03_HEBREWS_6_EXEGETICAL_DOSSIER_2026-09-29.md`;
- дополнительные/параллельные материалы: `APOSTASY/01_HEBREWS_WARNING_PASSAGES_MATRIX.md`, `ОТСТУПНИЧЕСТВО/01_HEBREWS_6_10_DEEP_DIVE.md`, `ОТСТУПНИЧЕСТВО/01_HEBREWS_6_EXEGETICAL_DOSSIER_2026-09-30.md`.

Не создавать новый Heb 6 dossier. Переносить только **уникальные** аргументы/локаторы/контраргументы.

### 3.3. Евр. 10

Canonical parent:

- `apostasy/04_HEBREWS_WARNING_SYSTEM_AND_10_29_2026-09-29.md`.

Сильный поздний overlay:

- `ОТСТУПНИЧЕСТВО/02_HEBREWS_10_EXEGETICAL_DOSSIER_2026-09-30.md`.

В overlay особенно сохранить три конкурирующих чтения `ἐν ᾧ ἡγιάσθη`, запрет решать вопрос одной грамматической формулой, связь 10:24–25 с warning как ecclesial means и 10:39 как pastoral-confidence ending.

### 3.4. 2 Петра 2

Наиболее ценный поздний deep dive:

- `ОТСТУПНИЧЕСТВО/02_2_PETER_DEEP_DIVE.md`.

Его нельзя потерять. Ключевые salvage points:

- `ἐπίγνωσις` во 2:20 нельзя автоматически редуцировать к «голому интеллектуальному знанию», поскольку термин положительно употреблён в 1:2–3,8;
- `ἀποφεύγω` связывает 1:4 и 2:20: описано **реальное escape/change** на некотором уровне;
- собака/вымытая свинья позволяют одновременно признать реальную перемену и финальное проявление устойчивой природы;
- 2:1 `τὸν ἀγοράσαντα αὐτοὺς δεσπότην` — отдельный hard case, который нельзя поглотить пословицами 2:22;
- вопрос 2 Пет. 2:1 затрагивает и perseverance, и extent/intent of atonement; их нельзя склеивать в один аргумент.

Следующий 2 Peter pass должен быть **canonical supplement**, а не новым competing dossier.

---

## 4. Что взять из `APOSTASY/`

### `APOSTASY/00_APOSTASY_BIBLICAL_THEOLOGY_DOSSIER.md`

Использовать как зрелый synthesis overlay. Особенно сохранить:

- таксономию temporary faith / service gifts / common operations / final apostasy / grievous fall / covenant cutting-off;
- wilderness matrix (1 Cor 10 + Heb 3–4);
- distinction Judas/Peter;
- историко-богословскую связку Calvin → Owen → Edwards → confessions → Schreiner;
- принцип: предупреждения не театральны, но являются назначенными средствами стойкости;
- список формулировок, которые **можно** и **нельзя пока** публиковать.

### `APOSTASY/01_HEBREWS_WARNING_PASSAGES_MATRIX.md`

Использовать как structural control для последовательности warning passages. Не переписывать Hebrews по разрозненным proof-texts.

### `APOSTASY/02_COMPARATIVE_CASES_AND_CANONICAL_WARNINGS_MATRIX.md`

Использовать как base для расширенной case matrix. Уже закрыты минимум rocky soil, Simon Magus, Judas, Heb 6, 2 Pet 2, Peter. Следующий pass должен добавлять новые случаи, а не создавать новую таблицу с теми же шестью строками.

---

## 5. Следующая волна исследования — порядок

### Wave A — Jude (Послание Иуды, не Иуда Искариот)

Создать отдельный canonical supplement в lowercase `apostasy/`:

- Jude 1: `called / beloved / kept`;
- Jude 4: intruders, denial of Master/Lord;
- Jude 5: Exodus deliverance → later destruction of unbelievers; textual variant `Ἰησοῦς / κύριος / θεός`;
- Jude 6–7: angels + Sodom as judgment analogies, без превращения их в прямую схему human regeneration-loss;
- Jude 11: Cain/Balaam/Korah;
- Jude 12–13: terminal metaphors, включая `twice dead, uprooted`;
- Jude 17–19: mockers/dividers, `not having the Spirit`;
- Jude 20–23: build/pray/keep/wait + rescue of wavering/endangered;
- Jude 24–25: God able to keep from stumbling and present blameless.

Особая canonical payoff: **в одном коротком послании стоят рядом “храните себя” (v.21) и “Могущему соблюсти вас” (v.24)**. Это один из лучших миниатюрных текстов для synthesis divine preservation + commanded perseverance.

### Wave B — expanded biblical case matrix

Добавить отдельными строками, с жёстким distinction `text says / text does not say`:

- wilderness generation (1 Cor 10; Heb 3–4);
- Hymenaeus + Alexander (1 Tim 1:18–20);
- Hymenaeus + Philetus (2 Tim 2:16–19);
- Demas (2 Tim 4:10) — **не** объявлять его окончательно погибшим: канонический endpoint не дан;
- Gal 5:2–4;
- Col 1:21–23;
- 1 Cor 15:1–2;
- Esau (Heb 12:16–17) — не превращать автоматически `place of repentance` в тезис «Бог отказался простить личный грех»;
- Saul — service/anointing ≠ автоматическое NT regeneration;
- Balaam;
- Ananias/Sapphira — церковный суд не даёт автоматически final-soteriology verdict;
- Rev 2–3 warnings — различить corporate lampstand/covenant discipline и индивидуальную эсхатологию.

### Wave C — article series V2

Расширить уже существующую архитектуру `apostasy/07_...` без создания конкурирующего плана:

- series hub `/apostasy/`;
- flagship;
- Judas Iscariot;
- temporary faith;
- Heb 6;
- Heb 10;
- **добавить отдельный 2 Peter 2 deep dive**, если source-to-claim closure подтвердит объём;
- **Jude** либо самостоятельный deep dive, либо крупный раздел flagship — решить после full dossier;
- Teletype/Telegram только derivative distribution после canonical site article.

### Wave D — evidence hardening

Source registry расширять не числом ссылок, а claim coverage:

- Jude textual criticism;
- confessional perseverance;
- strongest Arminian/Wesleyan readings;
- Lutheran distinctions;
- Free Grace alternative;
- 2 Peter 2 atonement/referent readings;
- exact-locator pass для Owen/Calvin/Augustine/Watson/Schreiner.

---

## 6. Запреты против повторного drift

1. Не создавать четвёртый каталог (`APOSTASY2`, `ОТПАДЕНИЕ`, `perseverance/` и т. п.).
2. Новые canonical supplements писать в `apostasy/` lowercase.
3. Не переименовывать и не удалять parallel lanes до завершения salvage ledger.
4. Не считать длинный URL-list evidence closure.
5. Не превращать `QUOTE_SAFE` в характеристику автора/сайта вообще: quote-safety относится к **конкретному claim + exact locator + edition/context**.
6. Не ослаблять warning-texts ради системы (`γεύομαι = “чуть попробовали”`, `ἐπίγνωσις = “просто знали факты”`, и т. п.).
7. Не делать обратную ошибку: сильный experiential language сам по себе ещё не доказывает regeneration/justification/adoption, если текст этого не утверждает.
8. Не смешивать grievous fall и final apostasy.
9. Не смешивать corporate covenant cutting-off и individual loss of justification без отдельного аргумента.
10. Не touching Product routes до отдельного publication/release witness.

---

## 7. Definition of done для research corpus

Тема может перейти из `PUBLICATION_HOLD` в `PUBLICATION-CANDIDATE` только когда одновременно выполнено:

- закрыта whole-Bible case matrix;
- Heb 6 / Heb 10 / 2 Pet 2 hard nodes имеют честную competing-view matrix;
- Jude dossier закрыт;
- historical/confessional spectrum покрывает Reformed, Arminian/Wesleyan, Lutheran и Free Grace альтернативы без карикатуры;
- все reader-facing исторические цитаты имеют exact locator/version/context;
- source-to-claim ledger показывает, какой источник держит какой тезис;
- article-series blueprint не создаёт search-intent cannibalization;
- final reader-facing формулировки отделяют `text explicitly says` от `theological inference`;
- Product implementation остаётся отдельной стадией и проходит собственные validators/release witness.

До этого статус всей темы: **`RESEARCH-ONLY / PUBLICATION_HOLD`**.
