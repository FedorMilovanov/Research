# LX: статьи 6A–6B — итоговая запись внедрения claim-level источников после решения 10:8

**Дата:** 28 июля 2026 года  
**Статус:** `LX / SITE-IMPLEMENTATION-RECORD / MERGED-TO-MAIN / 53-GROUP-AUDIT-COMPLETE / AUTHORITY-ACCEPTED / 10-8-TEXT-RESOLVED / THREE-BLOCKERS-REMAIN / DRAFT-NOINDEX / NOT-PUBLICATION-AUTHORITY`  
**Site repository:** `FedorMilovanov/gb-is-my-strength`  
**Merged site PR:** `#465`  
**Accepted site head:** `b315998937e4fdd68e204d01660adb65707cd0e6`  
**Site merge commit:** `522f0e1cae4fb9ce5a4631cfe856421f1952f4bc`  
**Research authority main:** `4881aca169e76e60fb76e5574a38d360835822f4`

---

## 1. Назначение

Этот документ фиксирует завершённое внедрение reader-facing source apparatus для статей 6A и 6B, его техническое принятие сайтом и последующее authority-решение по 1 Енох 10:8.

Он является implementation record, а не самостоятельным исследовательским authority. Он не заменяет:

- extension authority manifest;
- `GEN6-ENOCH-10-8-DECISION-LX`;
- LII, LIV, LVI и LIX;
- critical editions;
- locus-level review оставшихся blockers;
- отдельную publication transaction.

## 2. Итоговая site delivery

Чистая поставка выполнена через site PR `#465`:

- accepted head: `b315998937e4fdd68e204d01660adb65707cd0e6`;
- merge commit: `522f0e1cae4fb9ce5a4631cfe856421f1952f4bc`;
- изменено ровно шесть файлов;
- exact-head CI полностью зелёный;
- статьи оставлены `draft/noindex`;
- публикация не авторизована.

Промежуточные PR `#457` и `#460` не являются текущей поставкой. `#460` закрыт без merge и сохранён как историческое audit evidence.

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

### 4.1. 6A

Исправлено:

- внутренняя placeholder-формула `Research dossier` удалена;
- неподтверждённая сильная формула об извлечении Астрономической книги в календарные сборники заменена документированной множественностью и развивающейся историей геэз-передачи;
- расплывчатые «критические реестры» заменены публичной OCP-библиографией и source-role boundary;
- version, dating и composition uncertainty сохранены.

### 4.2. 6B

Исправлено:

- варианты чтения 10:8 обозначены как hypothesis map, а не consensus;
- неопределённые «древние версии» удалены;
- внутренние Research filenames удалены;
- текстологическое установление отделено от конфессионального канонического verdict;
- `DIRECT-CONFLICT` не присвоен до authority review.

## 5. Six-article consistency

Проверен reader order:

```text
6 → 6A → 6B → 7 → 8 → 9
```

Проверено:

- статья 6 не канонизирует весь 1 Енох из-за Иуд. 14–15;
- 6A остаётся corpus/manuscript/version history;
- 6B сохраняет qualified canonical audit;
- статья 7 не переносит Еноховы имена, число Стражей, Ермон, запрещённые искусства или происхождение бесов в Иуду и 2 Петра;
- статья 8 не утверждает доказанную зависимость 1 Пет. 3:19 от конкретной редакции 1 Еноха;
- статья 9 не объединяет 1 Пет. 3:19 и 4:6 через 1 Енох 22.

Статьи 7–9 прошли отдельный экзегетический аудит без необходимости изменения текста.

## 6. Machine contracts

Site provenance contract защищает:

- reader order;
- slug, section, author, series;
- canonical override;
- related-link graph;
- forward link между соседними статьями;
- `draft: true`;
- `noindex: true`;
- `sourcesRequired: true`;
- pinned Research commit и manifest digests;
- `releaseState: blocked`.

Draft site PR `#466` отдельно усиливает exact footnote identity:

- IDs `1–27` для 6A;
- IDs `1–26` для 6B;
- отсутствие неожиданных definitions;
- использование каждого definition;
- claim reference для каждого required ID;
- release state меняется только отдельной publication transaction.

`#466` не меняет article blobs и не является публикационной операцией.

## 7. Exact-head CI

На accepted site head успешно завершены:

- Genesis 6 Research provenance;
- Glossary Contract;
- Native Source Contract;
- Shared Files Guard;
- Route Registry Validators;
- Visual Parity Guard — pixel-diff.

Зелёный CI подтверждает технический контракт, но не богословскую истинность.

## 8. Authority-решение по 1 Енох 10:8

Research authority document `GEN6-ENOCH-10-8-DECISION-LX` установил:

- `4Q202 / 4QEnᵇ`, frg. 1 iv является физическим частичным и реконструируемым арамейским свидетелем locus;
- греческая версия сохраняет полную формулу о развращении земли через учение Асаэла и записи на нём всех грехов;
- геэз сохраняет согласующуюся двухчастную конструкцию;
- глаголы означают запись/судебную регистрацию, а не сотворение сущности греха;
- формула не утверждает прямо невиновность людей или отмену Адамова падения;
- 98:4 сохраняет внутренний акцент человеческой ответственности.

Authority status:

`TEXT-ESTABLISHED / INTERPRETATION-QUALIFIED`

### 8.1. Resolved by evidence

Закрыто:

`1-enoch-10-8-version-control`

### 8.2. Preserved uncertainty

Сохраняется:

`1-enoch-10-8-interpretive-scope`

Допустимый итоговый verdict:

`DIFFICULT-TO-HARMONIZE / INTERNAL-TENSION / TEXT-ESTABLISHED / INTERPRETATION-QUALIFIED`

`DIRECT-CONFLICT` не требуется, если locus не превращается в отрицание человеческой ответственности.

## 9. Три оставшихся blocking HOLD

После решения 10:8 publication remains blocked тремя authority blockers:

1. `1-enoch-15-8-12-demon-origin`;
2. `1-enoch-70-71-son-of-man`;
3. `astronomical-book-version-plurality`.

## 10. Текущие чистые evidence paths

### 10.1. 15:8–12

Draft Research PR `#31`:

- exact branch based on current authority main;
- Greek model presence established;
- Aramaic exact locus, multi-MS Geʽez and category scale remain open;
- `DIRECT-CONFLICT` not established;
- no site impact.

### 10.2. 70–71

Draft Research PR `#29`:

- public translation divergence documented;
- Charles 1912 emendation separated from manuscript fact;
- Charles 1906 historical variation located in OCR sequence;
- false printed-page precision removed;
- multi-MS syntax/composition control remains open;
- no site impact.

### 10.3. Astronomical Book

Draft Research PR `#30`:

- physical plurality 4Q208–211 registered;
- continuity plus textual plurality strongly supported;
- Geʽez diversity established;
- false OCR page precision removed;
- direction of development and full apparatus remain open;
- no site impact.

## 11. Rights status

`manuscript-image-rights` resolved by policy means only:

```text
NO MANUSCRIPT IMAGE REPRODUCTION
→ TEXT-ONLY DELIVERY IS NOT BLOCKED BY IMAGE RIGHTS
```

Это не разрешает:

- manuscript images;
- protected plates;
- long apparatus reproduction;
- cropping or recoloring as a rights workaround.

## 12. Preserved uncertainty outside blockers

Authority separately preserves:

- Parables date and witness form;
- Animal Apocalypse decomposition;
- chapter 108 relation to the Epistle;
- Codex Panopolitanus editorial intention;
- interpretive scope of 10:8.

Эти вопросы не должны исчезать из wording, даже когда они не являются текущими publication blockers.

## 13. Publication state

Сохраняются:

- `draft: true`;
- `noindex: true`;
- `sourcesRequired: true`;
- `publicationAuthorized: false`;
- `releaseState: blocked`.

Никакой merge evidence PR не является автоматической командой на публикацию.

## 14. Запрещённое толкование

Нельзя писать:

- «10:8 больше не содержит богословского напряжения»;
- «закрытие version control доказало максимальное толкование»;
- «три оставшихся PR автоматически разрешат выпуск»;
- «Greek model 15:8–12 является апостольской демонологией»;
- «71:14 точно отождествляет или точно не отождествляет Еноха»;
- «Астрономическая книга имеет один простой арамейский original»;
- «no-image policy разрешает брать изображения»;
- «зелёный CI является богословским доказательством».

Корректно:

> Claim-level apparatus 6A–6B внедрён и принят authority. Текст 10:8 установлен при сохранении interpretive qualification. Publication остаётся заблокирован тремя locus/version blockers; каждый имеет отдельный чистый evidence path, а сайт сохраняет draft/noindex.
