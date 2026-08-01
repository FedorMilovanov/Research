# «Обратная сторона кафедры» — Wave 6: publication ledger и site-transfer boundary

**Дата:** 2026-08-01  
**Статус:** `ACTIVE CURRENT AUTHORITY / WAVE 6 LEDGER READY / NO PRODUCT WRITE`  
**Authority ID:** `RESEARCH-OSK-AUTHORITY-2026-08-01-W6`  
**Research base:** `446a83932d4ec446b4c87e2c7b2fb02aeeee49eb`  
**Product snapshot:** `efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3`  
**Machine ledger:** `data/osk-wave6-site-transfer-ledger-2026-08-01.json`  
**Projection overlay:** `data/public-projection-osk-wave6-overlay-2026-08-01.json`

## Решение

Пять evidence-волн закрыли маршрутизацию всех 33 кейсов:

- **21** `ANTISOVETY_CORE`;
- **1** `ANTISOVETY_CONDITIONAL`;
- **7** `DARK_SIDE_SERIES`;
- **4** `STANDALONE`;
- **0** generic case-level `HOLD`.

Корпус контролирует **290 источников**, включая **216 A-класса**, **197 точных URL**
и **105 quote-safe records**.

Это закрывает Research, но не даёт автоматического права переписать сайт.

## Текущая статья

Текущий production-source:

`src/components/article-pilots/antisovetov/AntisovetovBody.astro`

Маршрут:

`/articles/20-antisovetov-pastoru/`

Статья уже построена правильно как библейско-пастырский и концептуальный текст.
Wave 6 не превращает её в перечень известных падений и обвинений.

Управляющее решение:

`PRESERVE_BODY_NO_CASE_ROSTER`

Для каждого из 20 антисоветов ledger фиксирует:

- точный anchor;
- primary core cases;
- supporting core cases;
- отдельно именованный conditional comparator;
- допустимое место evidence;
- claim boundary;
- запрет на новую прямую цитату без отдельной проверки.

Ни один современный кейс не получает автоматическую вставку в body.

## Допустимые способы использования evidence

1. `source-note` — короткое нейтральное подтверждение механизма.
2. `editorial-footnote` — только с точным source/claim boundary.
3. `separate-case-article` — предпочтительный формат для сложных правовых и
   институциональных кейсов.

Запрещено:

- создавать обвинительный roster внутри основной статьи;
- использовать dark-side или standalone case как доказательство Диотрефа;
- вставлять direct quote только потому, что среди 290 записей существует источник;
- смешивать allegation, denial, settlement, dismissal, conviction,
  scientific probability и institutional finding;
- переносить преступление одного человека на другого лидера или институт.

## Карта 20 пунктов

Machine ledger содержит **20 point records**. Все они имеют:

- `siteAction = PRESERVE_CONCEPTUAL_CORE`;
- `bodyCaseInsertionApproved = false`;
- `quoteMode = NO_NEW_DIRECT_QUOTES`;
- primary/supporting IDs только из эффективного `ANTISOVETY_CORE`;
- David Platt только как явно помеченный `ANTISOVETY_CONDITIONAL`
  no-merits comparator в пунктах 4 и 19.

Dark-side и standalone маршруты исключены из evidence-set основной статьи.

## Будущие отдельные статьи

Wave 6 создаёт 10 editorial bundles, но не создаёт product routes:

1. **«Диотрефы нашего времени»** — 21 core case.
2. **Дисквалификация, покаяние и пригодность к служению** — Lawson, Allberry.
3. **Неполное признание и преждевременное восстановление** — Tchividjian, Noble.
4. **Когда «моральная ошибка» скрывает зло** — Savage.
5. **Звёздная платформа и оспариваемое злоупотребление властью** — Lentz.
6. **Мировое соглашение — не приговор** — Long.
7. **Душепопечение, дисциплина и домашнее насилие** — Gray.
8. **Обязательное сообщение и конфликт свидетельств** — Guay.
9. **Институциональная память и научная переоценка** — Hengsbach.
10. **Церковный авторитет и финансовые проекты** — Adelaja.

Каждый bundle сохраняет собственную evidence и legal boundary.

## A06 projection

Старый A06 record `osk-power-dark-side-standalone` имел статус:

`BLOCKED / EVIDENCE_HOLD + PUBLICATION_HOLD`

Он superseded только для OSK новым overlay.

Текущий effective A06 status:

- disposition: `REFERENCE`;
- research status:
  `WAVES_1_TO_5_EVIDENCE_CLOSED_290_SOURCES_WAVE6_LEDGER_READY`;
- hold: только `PUBLICATION_HOLD`;
- automatic promotion: запрещён;
- product write: отсутствует.

Эффективный projection dashboard после overlay:

- `PROMOTE = 0`;
- `REFERENCE = 4`;
- `BLOCKED = 6`;
- `SUPERSEDED = 0`.

## Что нужно перед первым product PR

1. Выбрать один bounded target:
   - terminology/source audit существующей статьи;
   - один source-note;
   - один новый case article.
2. Проверить current product exact head и active overlapping lanes.
3. Привязать каждое новое предложение к case boundary.
4. Не вводить новую direct quote без quote-safe source и locator.
5. Сохранить основную статью как conceptual owner.
6. Открыть отдельную product branch и пройти production-like CI.

## Финальный статус Wave 6

- Research evidence closure: **closed**;
- case routing: **closed**;
- site-transfer ledger: **ready**;
- A06 evidence hold: **removed by overlay**;
- product wording fidelity: **not yet verified**;
- product change: **none**;
- production claim: **none**.
