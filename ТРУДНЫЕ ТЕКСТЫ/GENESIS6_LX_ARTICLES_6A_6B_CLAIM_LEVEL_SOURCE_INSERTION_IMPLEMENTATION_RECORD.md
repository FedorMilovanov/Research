# LX: статьи 6A–6B — итоговая запись внедрения и аудита claim-level источников

**Дата:** 28 июля 2026 года  
**Статус:** `LX / SITE-IMPLEMENTATION-RECORD / MERGED-TO-MAIN / 53-GROUP-AUDIT-COMPLETE / SIX-ARTICLE-CONTRACT / DRAFT-NOINDEX / NOT-PUBLICATION-AUTHORITY`  
**Site repository:** `FedorMilovanov/gb-is-my-strength`  
**Merged site PR:** `#465`  
**Merged site head:** `b315998937e4fdd68e204d01660adb65707cd0e6`  
**Site main after merge:** `522f0e1cae4fb9ce5a4631cfe856421f1952f4bc`

---

## 1. Назначение записи

Этот документ фиксирует фактическое завершение читательского source-apparatus прохода для статей 6A и 6B и его внедрение в site `main`.

Он является implementation record и не создаёт новый исследовательский авторитет. Он не заменяет LII, LIV, LVI, LIX, критические издания, locus-level version control или каноническую экзегезу.

Корректная последовательность выполненной работы:

```text
LIX CLAIM-LEVEL MAPS
→ ЧИТАТЕЛЬСКАЯ ВСТАВКА ИСТОЧНИКОВ
→ БИБЛИОГРАФИЧЕСКИЙ МИКРОАУДИТ 53 ГРУПП
→ CROSS-ARTICLE И ЭКЗЕГЕТИЧЕСКИЙ АУДИТ
→ SIX-ARTICLE MACHINE CONTRACT
→ CLEAN SITE PR #465
→ EXACT-HEAD CI
→ MERGE В SITE MAIN
```

## 2. История веток и PR

### 2.1. Ранние continuation PR

Site PR `#457` и позднее PR `#460` использовались как промежуточные continuation/audit ветки.

PR `#460` разошёлся с меняющимся `main`, был сохранён как историческое audit evidence и закрыт без merge. Его история не переписывалась force push.

### 2.2. Чистая итоговая поставка

Итоговый читательский аппарат был заново собран одним чистым коммитом от актуального `main` и доставлен через PR `#465`:

- title: `content(genesis6): apply audited reader source apparatus`;
- exact head: `b315998937e4fdd68e204d01660adb65707cd0e6`;
- merge commit: `522f0e1cae4fb9ce5a4631cfe856421f1952f4bc`;
- changed files: ровно шесть;
- merge выполнен после зелёного exact-head CI.

Изменённые site-файлы:

1. `data/genesis6-enoch-footnote-gates.json`;
2. `data/genesis6-research-provenance.json`;
3. `scripts/genesis6-enoch-footnote-gate.mjs`;
4. `scripts/genesis6-research-provenance-contract.mjs`;
5. `src/content/articles/kniga-enoha-kotoroy-ne-bylo-kak-raznye-proizvedeniya-stali-korpusom.mdx`;
6. `src/content/articles/mozhno-li-doveryat-1-enohu-kanonicheskiy-audit.mdx`.

## 3. Точные article blobs

### 3.1. Статья 6A

**Slug:** `kniga-enoha-kotoroy-ne-bylo-kak-raznye-proizvedeniya-stali-korpusom`  
**Blob:** `4896a78591538f56a1a5f1db35131d12677d7c70`  
**Research map:** `GEN6-ENOCH-6A-FOOTNOTE-MAP-LIX`  
**Source groups:** 27

### 3.2. Статья 6B

**Slug:** `mozhno-li-doveryat-1-enohu-kanonicheskiy-audit`  
**Blob:** `c57db2e7c8a5140fdf96869794d284128653630c`  
**Research map:** `GEN6-ENOCH-6B-SOURCE-PASS-LIX`  
**Source groups:** 26

Итого проверено 53 reader-facing source groups.

## 4. Выполненный библиографический микроаудит

Каждая из 53 групп была сопоставлена с точным inline claim, а не только с тематикой раздела.

### 4.1. Исправления 6A

- удалена внутренняя placeholder-формула `Research dossier`;
- неподтверждённое сильное утверждение об извлечении Астрономической книги в календарные сборники ослаблено до документированной множественности и развивающейся истории геэз-передачи;
- расплывчатая формула о «критических реестрах» заменена публичной OCP-библиографией и явным разграничением функций каталогов и специальных исследований;
- сохранены все dating, version, composition и rights `HOLD`.

### 4.2. Исправления 6B

- список возможных чтений 10:8 обозначен как редакторская карта гипотез, а не научный консенсус;
- удалена расплывчатая ссылка на неопределённые «древние версии» в 15:8–12;
- внутренние Research filenames удалены из reader-facing примечания;
- установление текста отделено от жанровой и конфессиональной канонической оценки;
- `DIRECT-CONFLICT` не присвоен version-sensitive locus.

## 5. Six-article consistency pass

Проверен порядок серии:

```text
6 → 6A → 6B → 7 → 8 → 9
```

Проверено, что:

- статья 6 не канонизирует весь корпус из-за Иуд. 14–15;
- 6A остаётся историей состава, рукописей и версий;
- 6B сохраняет текстологическую и каноническую квалификацию;
- статья 7 не вставляет Еноховы имена, число Стражей, Ермон, запрещённые искусства или происхождение бесов в Иуду и 2 Петра;
- статья 8 не утверждает доказанную зависимость 1 Пет. 3:19 от конкретной редакции 1 Еноха;
- статья 9 не объединяет автоматически 1 Пет. 3:19 и 4:6 через 1 Енох 22.

Отдельный экзегетический аудит статей 7, 8 и 9 не потребовал содержательных правок.

## 6. Исполняемый release/provenance contract

В site provenance contract закреплены все шесть статей, а не только 6A–6B.

Машинно защищаются:

- точный порядок `6 → 6A → 6B → 7 → 8 → 9`;
- точные slug, section, author и series;
- `draft: true`;
- `noindex: true`;
- `sourcesRequired: true`;
- точные canonical override;
- точный related-link graph;
- прямой forward link между каждой соседней парой серии;
- pinned Research commit и manifest digests;
- `releaseState: blocked` до отдельной publication transaction.

Контракт проверен также отрицательными мутациями: снятие draft, неправильный canonical, разрыв related graph и смена release state приводят к ожидаемому падению.

## 7. Exact-head CI итоговой поставки

На site head `b315998937e4fdd68e204d01660adb65707cd0e6` успешно завершены:

- Genesis 6 Research provenance;
- Glossary Contract;
- Native Source Contract;
- Shared Files Guard;
- Route Registry Validators;
- Visual Parity Guard — pixel-diff.

Зелёный CI подтверждает целостность технического контракта, но не является доказательством богословской истинности или закрытия textual HOLD.

## 8. Follow-up machine hardening

После merge обнаружено, что параллельный промежуточный проход временно вводил 28/27 определений за счёт двух повторных overview-ссылок сверх утверждённых LIX-целей 27/26.

Эти дополнительные номера не закрывали новые уникальные claims. Поэтому текущие reader articles не раздуваются ради числа.

Отдельный draft site PR `#466` усиливает только machine identity contract:

- exact IDs `1–27` для 6A;
- exact IDs `1–26` для 6B;
- отсутствие неожиданных definitions;
- обязательное использование каждого definition;
- обязательная claim-reference для каждого ID;
- отдельная publication transaction.

PR `#466` не меняет article blobs и не является публикационной операцией.

## 9. Следующий узкий Research layer

Отдельный draft Research PR `#22` не меняет сайт и не повышает authority status.

Он содержит:

1. locus-level closure protocol для 1 Енох 10:8 и 15:8–12;
2. первую инвентаризацию публично доступных witness-данных.

Первичный узкий результат:

- спорная формула 10:8 непосредственно присутствует в публичной греческой традиции;
- основная Енохова модель 15:8–12 непосредственно присутствует в публичном греческом тексте;
- семантический объём, арамейский контроль, полный геэз-аппарат и окончательная каноническая классификация остаются `HOLD`.

Этот слой не включён в site wording и не снимает `draft/noindex`.

## 10. Сохранённые блокировки

`NOT CLOSED`:

- 1 Енох 10:8 — семантический объём и межверсионный контроль;
- 1 Енох 15:8–12 — полный арамейский/геэз version control и масштаб модели;
- дата и текстовая форма Притчей;
- 70–71 и возможное отождествление Еноха;
- точная модель Астрономической книги;
- декомпозиция Animal Apocalypse(s);
- первоначальная связь главы 108;
- редакторское намерение Codex Panopolitanus;
- права на manuscript images и защищённый аппарат;
- снятие `draft/noindex`;
- публикационный выпуск серии.

## 11. Запрещённое толкование результата

Нельзя писать:

- «53 сноски решили все вопросы 1 Еноха»;
- «зелёный CI разрешает публикацию»;
- «греческое свидетельство снимает необходимость арамейского и геэз-контроля»;
- «Енохова модель 15:8–12 является апостольской демонологией»;
- «10:8 уже доказан как прямое противоречие Писанию»;
- «Research implementation record является новым магистериальным authority».

Корректно:

> Claim-level source apparatus для 6A–6B прошёл читательский, межстатейный и машинный аудит и внедрён в site main. Все named textual, version, composition, rights и publication HOLD сохраняются; следующий Research pass ограничен точными loci 10:8 и 15:8–12.
