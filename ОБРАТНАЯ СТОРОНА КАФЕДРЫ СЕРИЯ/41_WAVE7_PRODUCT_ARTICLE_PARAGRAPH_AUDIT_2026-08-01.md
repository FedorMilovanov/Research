# «20 антисоветов пастору» — Wave 7: paragraph-level audit production-статьи

**Дата:** 2026-08-01  
**Статус:** `ACTIVE CURRENT AUTHORITY / WAVE 7 AUDIT CLOSED / PRODUCT FIX NOT YET APPLIED`  
**Authority ID:** `RESEARCH-OSK-AUTHORITY-2026-08-01-W7`  
**Research base:** `49f49f89cceb53f8146de3426ccc71f3c6ad1818`  
**Product snapshot:** `efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3`  
**Canonical product source:** `src/components/article-pilots/antisovetov/AntisovetovBody.astro`  
**Product blob SHA:** `c7d3e1be45bacbb538126c76d50399920aa53ec7`  
**Audit ledger:** `data/osk-wave7-product-article-audit-2026-08-01.json`  
**Source pool:** `data/osk-wave7-article-audit-source-registry-2026-08-01.json`

## Итог

Текущая статья не требует концептуальной перестройки. Все 20 антисоветов получают
статус:

`PRESERVE_WITH_BOUNDARY`

Основной библейско-пастырский каркас остаётся владельцем страницы. Современный
case roster не добавляется, новые прямые цитаты не разрешаются, продукт этой
волной не изменяется.

Аудит выявил:

- **20** point-level preserve records;
- **14** обязательных исправлений;
- из них **1 CRITICAL**, **8 HIGH**, **5 MEDIUM**;
- **12** терминологических/source-note задач;
- **54** контрольных источника:
  - 18 библейско-лексикографических и экзегетических;
  - 18 психологических и организационных;
  - 18 safeguarding, spiritual-abuse и pastoral-governance;
- **0** новых разрешённых direct quotes;
- **0** изменённых product files.

## Что сохраняется

1. Сатирическая форма «антисоветов».
2. Центральный тезис: идолопоклонство перед служением и первое место.
3. Все 20 заголовков и anchors `point-1` — `point-20`.
4. Различение законной власти и властного злоупотребления.
5. Библейские примеры Диотрефа, Саула, Давида, Петра и других фигур — после
   точечных экзегетических уточнений.
6. Практический раздел о совете, свидетелях, внешней помощи и государстве — после
   safeguarding и legal-scope исправлений.
7. Запрет превращать статью в список современных обвиняемых лидеров.

## Единственная CRITICAL-правка

Текущая формула:

> «Коллективное письменное обращение — это 1 Тим. 5:19 в действии»

экзегетически слишком сильна.

1 Тим. 5:19 устанавливает evidentiary safeguard: обвинение против пресвитера не
следует принимать без двух или трёх свидетелей. Стих не предписывает конкретный
формат коллективного письма.

Допустимая новая формула:

> «Совместное письменное обращение может быть одним из разумных способов
> документировать согласующиеся свидетельства. Однако 1 Тим. 5:19 прежде всего
> задаёт evidentiary safeguard, а не обязательную форму обращения».

## HIGH-правки

### 1. Conditional warmth

Фразу о том, что новых людей встречают особой теплотой, нельзя подавать как
универсальную механику церкви. Следует сказать, что **в coercive или spiritually
abusive systems** первоначальная теплота иногда становится условной и зависит от
лояльности.

### 2. «Негласные правила никогда не объявляют»

`Никогда` заменить на bounded pattern. Не всякая неформальная норма является
манипуляцией.

### 3. Две боли и гарантированные результаты

Формула «первая ведёт к покаянию, вторая — к зависимости» детерминистична.
Следует говорить о возможных плодах и диагностических признаках, а не о
гарантированном причинном тесте.

### 4. Learned helplessness

Нужна современная формулировка через uncontrollability и revision Maier–Seligman:
упрощённая фраза «человек выучил, что ничего не зависит» не передаёт нынешнюю
модель полностью.

### 5. Внутренние процедуры «бесполезны»

Заменить на «могут быть недостаточными или небезопасными». Minority elders,
письменные records, denominational structures и safeguarding officers иногда
сохраняют значение даже при скомпрометированном совете.

### 6. Неанонимность

Подписанное коллективное обращение может быть сильным, но нельзя универсально
требовать раскрытия личности жертвы или whistleblower обвиняемому либо всей
общине. Нужны protected reporting routes.

### 7. Правоохранительные органы

Не всякий финансовый или пастырский конфликт является уголовным делом. Корректная
граница: suspected crime, immediate danger, child/vulnerable-person safeguarding
obligation или иное legally reportable conduct; конкретные обязанности зависят
от юрисдикции.

### 8. `ὑπόκρισις`

В НЗ слово означает hypocrisy/pretence. Театральный фон может объяснять образ,
но нельзя определять слово буквально как «маска».

## MEDIUM-правки

1. `Гомеостаз системы` — явно назвать family-systems/organizational analogy.
2. `Когнитивный диссонанс` — исправить научное определение.
3. `Внешний служитель защитит источники` — добавить competence, conflict и
   confidentiality requirements.
4. `Саул начинал искренне смиренным` — убрать уверенность во внутреннем мотиве;
   говорить о его ранних self-effacing словах.
5. `В здоровой церкви вопросы ничего не стоят` — заменить на отсутствие
   retaliation/spiritual punishment; трудный разговор всё равно может быть
   болезненным.

## Терминологические source notes

Обязательные source/boundary notes нужны для:

- gaslighting;
- sunk-cost effect;
- strategic ambiguity;
- impression management;
- rationalization;
- organizational silence;
- institutional betrayal;
- авторской формулы «негативный отбор старейшин»;
- spiritual abuse / coercive-control analogy;
- psychological safety;
- identified patient;
- secondary trauma.

Особые ограничения:

- disagreement и плохая память сами по себе не gaslighting;
- длительная верность сама по себе не sunk-cost irrationality;
- ordinary pastoral caution не strategic ambiguity;
- забота о репутации не всегда impression management в обманном смысле;
- `негативный отбор старейшин` — авторский analytic term, не диагноз;
- coercive-control legal categories не переносятся автоматически в церковь;
- `secondary trauma` нельзя использовать для обычного семейного напряжения.

## Point-level решение

Все `point-1` — `point-20` сохраняются. Современные case boundaries из Wave 6
остаются обязательными:

- David Platt — только labelled no-merits comparator в пунктах 4 и 19;
- Gray и Guay не используются в пункте 9;
- dark-side кейсы не становятся автоматическим evidence для пункта 20;
- case roster и новые прямые цитаты остаются запрещёнными.

## Source pool

54 источника не являются новой читательской библиографией целиком. Это audit pool.
В product PR следует вывести короткий curated source note, а полный registry
оставить в Research.

В source pool входят:

- SBLGNT, MorphHB, STEP Bible, LSJ, BDAG;
- Kruse, Towner, Mounce и исторические комментарии к 1 Тим. 5;
- Sweet, Seligman/Maier, Arkes/Blumer, Festinger, Jackson, Eisenberg,
  Leary/Kowalski, Morrison/Milliken, Smith/Freyd, Edmondson, Tepper;
- Oakley/Kinmond, Oakley/Humphreys, Langberg, Mullen, DeGroat, Stark;
- Royal Commission, IICSA, Church of England safeguarding guidance,
  Charity Commission и Guidepost.

## Wave 8 product boundary

Следующая волна может изменить продукт, но только отдельным PR:

1. применить ровно 14 mandatory fixes;
2. добавить компактные source notes для 12 терминов;
3. сохранить все 20 headings и anchors;
4. не добавлять case roster;
5. не добавлять direct quotes;
6. не менять route, schema и visual architecture без отдельного решения;
7. пройти production tests и visual/readback review.

**Wave 7 сама product write не выполняет.**
