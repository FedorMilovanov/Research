# LX: статьи 6A–6B — итоговая запись внедрения и аудита claim-level источников

**Дата:** 28 июля 2026 года  
**Статус:** `LX / SITE-IMPLEMENTATION-RECORD / MERGED-TO-MAIN / 53-GROUP-AUDIT-COMPLETE / SIX-ARTICLE-CONTRACT / AUTHORITY-ACCEPTED / DRAFT-NOINDEX / NOT-PUBLICATION-AUTHORITY`  
**Site repository:** `FedorMilovanov/gb-is-my-strength`  
**Merged site PR:** `#465`  
**Accepted site head:** `b315998937e4fdd68e204d01660adb65707cd0e6`  
**Site main merge commit:** `522f0e1cae4fb9ce5a4631cfe856421f1952f4bc`

---

## 1. Назначение

Этот документ фиксирует завершённое внедрение читательского source apparatus для статей 6A и 6B и его принятие действующим Research authority manifest.

Он является implementation record, а не новым исследовательским авторитетом. Он не заменяет LII, LIV, LVI, LIX, критические издания, locus-level version control или каноническую экзегезу.

Корректная производственная последовательность:

```text
LIX CLAIM-LEVEL MAPS
→ ЧИТАТЕЛЬСКАЯ ВСТАВКА ИСТОЧНИКОВ
→ БИБЛИОГРАФИЧЕСКИЙ МИКРОАУДИТ 53 ГРУПП
→ CROSS-ARTICLE И ЭКЗЕГЕТИЧЕСКИЙ АУДИТ
→ SIX-ARTICLE MACHINE CONTRACT
→ CLEAN SITE PR #465
→ EXACT-HEAD CI
→ MERGE В SITE MAIN
→ RESEARCH SITE ACCEPTANCE
```

## 2. История поставки

### 2.1. Промежуточные ветки

Site PR `#457` и `#460` использовались как continuation/audit ветки. PR `#460` разошёлся с меняющимся `main`, был сохранён как историческое audit evidence и закрыт без merge. Его история не переписывалась force push.

### 2.2. Чистая итоговая поставка

Итоговый аппарат был собран одним чистым коммитом от актуального `main` и доставлен через PR `#465`:

- title: `content(genesis6): apply audited reader source apparatus`;
- accepted head: `b315998937e4fdd68e204d01660adb65707cd0e6`;
- merge commit: `522f0e1cae4fb9ce5a4631cfe856421f1952f4bc`;
- изменено ровно шесть site-файлов;
- merge выполнен после зелёного exact-head CI.

Изменённые файлы:

1. `data/genesis6-enoch-footnote-gates.json`;
2. `data/genesis6-research-provenance.json`;
3. `scripts/genesis6-enoch-footnote-gate.mjs`;
4. `scripts/genesis6-research-provenance-contract.mjs`;
5. `src/content/articles/kniga-enoha-kotoroy-ne-bylo-kak-raznye-proizvedeniya-stali-korpusom.mdx`;
6. `src/content/articles/mozhno-li-doveryat-1-enohu-kanonicheskiy-audit.mdx`.

## 3. Точные article blobs

### 3.1. Статья 6A

- slug: `kniga-enoha-kotoroy-ne-bylo-kak-raznye-proizvedeniya-stali-korpusom`;
- blob: `4896a78591538f56a1a5f1db35131d12677d7c70`;
- Research map: `GEN6-ENOCH-6A-FOOTNOTE-MAP-LIX`;
- source groups: 27.

### 3.2. Статья 6B

- slug: `mozhno-li-doveryat-1-enohu-kanonicheskiy-audit`;
- blob: `c57db2e7c8a5140fdf96869794d284128653630c`;
- Research map: `GEN6-ENOCH-6B-SOURCE-PASS-LIX`;
- source groups: 26.

Итого проверено 53 reader-facing source groups.

## 4. Библиографический микроаудит

Каждая группа была сопоставлена с точным inline claim, а не только с тематикой раздела.

### 4.1. Исправления 6A

- удалена внутренняя placeholder-формула `Research dossier`;
- неподтверждённое сильное утверждение об извлечении Астрономической книги в календарные сборники ослаблено до документированной множественности и развивающейся истории геэз-передачи;
- расплывчатая формула о «критических реестрах» заменена публичной OCP-библиографией и разграничением функций каталогов и специальных исследований;
- dating, version и composition `HOLD` сохранены.

### 4.2. Исправления 6B

- список возможных чтений 10:8 обозначен как редакторская карта гипотез, а не научный консенсус;
- удалена расплывчатая ссылка на неопределённые «древние версии» в 15:8–12;
- внутренние Research filenames удалены из reader-facing примечания;
- установление текста отделено от жанровой и конфессиональной канонической оценки;
- `DIRECT-CONFLICT` не присвоен version-sensitive locus.

## 5. Six-article consistency pass

Проверен порядок:

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

Машинно защищаются:

- порядок `6 → 6A → 6B → 7 → 8 → 9`;
- slug, section, author и series;
- `draft: true`;
- `noindex: true`;
- `sourcesRequired: true`;
- canonical override;
- related-link graph;
- прямой forward link между соседними статьями;
- pinned Research commit и manifest digests;
- `releaseState: blocked` до отдельной publication transaction.

Контракт проверен отрицательными мутациями: снятие draft, неправильный canonical, разрыв related graph и смена release state приводят к ожидаемому падению.

## 7. Exact-head CI

На accepted head `b315998937e4fdd68e204d01660adb65707cd0e6` успешно завершены:

- Genesis 6 Research provenance;
- Glossary Contract;
- Native Source Contract;
- Shared Files Guard;
- Route Registry Validators;
- Visual Parity Guard — pixel-diff.

Зелёный CI подтверждает техническую целостность, но не является доказательством богословской истинности или закрытия textual HOLD.

## 8. Research authority acceptance

Extension authority manifest schema 2 фиксирует:

- accepted site head `b315998937e4fdd68e204d01660adb65707cd0e6`;
- merge commit `522f0e1cae4fb9ce5a4631cfe856421f1952f4bc`;
- 27 групп для 6A и 26 для 6B;
- закрытие claim-level apparatus, bibliography microaudit, site provenance и exact-head technical CI;
- `publicationAuthorized: false`.

### 8.1. Blocking HOLD

Текстовый выпуск остаётся заблокирован четырьмя authority blockers:

1. `1-enoch-10-8-version-control`;
2. `1-enoch-15-8-12-demon-origin`;
3. `1-enoch-70-71-son-of-man`;
4. `astronomical-book-version-plurality`.

### 8.2. Preserved uncertainty

Следующие вопросы должны оставаться явно квалифицированными, но authority manifest отделяет их от четырёх blocking HOLD:

- `parables-date-and-witness-form`;
- `animal-apocalypse-decomposition`;
- `chapter-108-relation-to-epistle`;
- `codex-panopolitanus-editorial-intention`.

### 8.3. Rights gate

`manuscript-image-rights` закрыт политикой:

```text
NO MANUSCRIPT IMAGE REPRODUCTION
→ RIGHTS GATE RESOLVED FOR TEXT-ONLY DELIVERY
```

Это не разрешает использовать изображения. Это означает, что текстовый выпуск не блокируется правами на изображения, пока сайт не воспроизводит manuscript images или защищённый длинный apparatus.

## 9. Follow-up machine hardening

Draft site PR `#466` меняет только два gate-файла и закрепляет:

- exact IDs `1–27` для 6A;
- exact IDs `1–26` для 6B;
- отсутствие неожиданных definitions;
- использование каждого definition;
- claim-reference для каждого ID;
- отдельную publication transaction.

PR `#466` не меняет article blobs и не является публикационной операцией.

## 10. Controlled Research continuation

Draft Research PR `#22` содержит:

1. locus-level closure protocol для 10:8 и 15:8–12;
2. public-witness evidence inventory;
3. lawful full-text acquisition gate.

Установлено:

- формула 10:8 присутствует в публичной греческой традиции;
- модель 15:8–12 присутствует в публичном греческом тексте;
- OCP не закрывает арамейский контроль после главы 8 и полный геэз-apparatus;
- exact modern apparatus/pages Knibb, Black–Denis, Nickelsburg и Milik не получены в проверяемом открытом режиме;
- действует `FULL-TEXT-ACCESS-HOLD` без site wording upgrade.

## 11. Запрещённое толкование

Нельзя писать:

- «53 сноски решили все вопросы 1 Еноха»;
- «зелёный CI разрешает публикацию»;
- «греческое свидетельство снимает необходимость арамейского и геэз-контроля»;
- «Енохова модель 15:8–12 является апостольской демонологией»;
- «10:8 уже доказан как прямое противоречие Писанию»;
- «rights gate разрешает брать изображения рукописей»;
- «implementation record является новым authority».

Корректно:

> Claim-level source apparatus для 6A–6B прошёл читательский, межстатейный и машинный аудит, внедрён в site main и принят Research authority. Текстовый выпуск остаётся заблокирован четырьмя named blockers; uncertainty по другим вопросам сохраняется явно, а image-rights gate закрыт только решением не воспроизводить manuscript images.
