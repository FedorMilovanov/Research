# БИБЛЕЙСКИЙ АТЛАС — исследовательские гео-досье

**Роль (ATLAS-CONTRACT Р5, `gb-is-my-strength/docs/ATLAS-CONTRACT-2026-07-10.md`):** здесь хранится доказательная база географии Атласа — аргументация локализаций, первоисточники, археология и хронологические таблицы. Код и данные карт живут в `gb-is-my-strength/data/atlas/**`, аудиты — в AuditRepo.

## Authority и терминология

Этот корпус подчиняется [`../AGENT_RULES.md`](../AGENT_RULES.md) и [`../data/repository-evidence-policy-v2.json`](../data/repository-evidence-policy-v2.json).

Глобальные evidence classes используются только в значениях:

- `A1` — первичный археологический, эпиграфический, государственный или юридический объект/отчёт;
- `A2` — официальная публикация раскопок, институциональный отчёт или первичная академическая публикация;
- `A3` — официальное event-specific заявление или решение учреждения;
- `B1` — качественная вторичная академическая опора;
- `C` — контекст/поисковый lead;
- `D` — исключённый источник.

Исторические Atlas-обозначения `Level A/B/C/HOLD` **не используются**. Уверенность локализации (`consensus`, `primary`, `candidate`, `alternative`, `caveat`, `minor`, `rejected`) — отдельная ось и не является классом источника. `primary` в словаре локализации означает основной картографический кандидат, а не evidence class `A1`.

## Правила

1. **Один кейс = один файл-досье.** `GEO-DOSSIER-<place-id>.md` использует ID канонического реестра `gb-is-my-strength/data/atlas/places-draft.json` или `places/*.json`.
2. Каждая опора фиксирует отдельно `evidenceClass`, `accessState`, `locatorState`, `rightsState` и `publicationState`.
3. Географическая уверенность использует только словарь движка: `consensus | primary | candidate | alternative | caveat | minor | rejected`.
4. Досье создаётся для спорной или чувствительной локализации (`identifications > 1` или status ≠ `consensus`).
5. Карта, подпись и визуальный asset проходят отдельный rights/publication gate; исследовательское решение не разрешает автоматический Product write.

## Стандарт структуры досье

```text
# <Название> (<place-id>)
## Суть вопроса
## Кандидаты локализации
## Источники, локаторы и evidence classes
## Анализ и отрицательные данные
## Решение для Атласа
## Rights / publication boundary
## Следующее проверяемое действие
```

## Приоритетная очередь

| Приоритет | Место | Состояние |
|---|---|---|
| P0 | `mount-sinai` — [досье](GEO-DOSSIER-mount-sinai.md) | Джебель-Муса / Джебель-аль-Лавз / Хар-Карком; owner-review |
| P0 | `kadesh-barnea` — [досье](GEO-DOSSIER-kadesh-barnea.md) | Кудейрат как основной кандидат; Петра как историческая альтернатива |
| P1 | `ur` — [досье](GEO-DOSSIER-ur.md) | Tell el-Muqayyar и северная теория разведены |
| P1 | `sodom` + `hammam` — [досье](GEO-DOSSIER-sodom.md) | южный и северный кандидаты; airburst не подаётся как факт |
| P1 | `bethany-beyond-jordan` — [досье](GEO-DOSSIER-bethany-beyond-jordan.md) | Аль-Махтас и текстовый вопрос разведены |
| P2 | `emmaus` — [досье](GEO-DOSSIER-emmaus.md) | четыре кандидата и развилка 60/160 стадий |
| P2 | `cana` — [досье](GEO-DOSSIER-cana.md) | Хирбет-Кана / Кафр-Канна; остаётся Product data debt |
| P2 | `mount-beatitudes` — [досье](GEO-DOSSIER-mount-beatitudes.md) | традиционная и альтернативная локализации разведены |
| P0 active | `pihahiroth` — [досье](GEO-DOSSIER-pihahiroth.md) | owner-review, primary-source strengthening, locator and rights work |
