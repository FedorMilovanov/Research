# ED-08 — Подготовка материалов для новой квитации (передача новой редакции)

**Статус:** проект ED-08, требует координатора MAX и独立 серверной проверки на Google Drive  
**Источник:** том 16 §21.3 (ED-08 OPEN), `data/charnock-handoff-receipt-v1.json` (wave40)  
**Ограничение:** новая квитация не снимает PUBLICATION_HOLD. Публикация остаётся заблокированной.

---

## 1. Что изменилось с момента wave40 (2026-10-26)

| Файл | Хеш в квитации wave40 | Текущий хеш | Статус |
|------|----------------------|-------------|--------|
| `AGENT_RULES.md` | `19f9f24d41a09e9883e4d1620f7f6d6c4094cb2a5d3cab3314025780dd34f8aa` | `7e4b4685178838b2b5d68e3091ee733f8a04fb1921aa4317f523bd3892bc22e4` | Изменён мержем PR #520 (2026-11-16) |
| `БИОГРАФИИ/Стивен Чарнок/00_README_AND_NAVIGATION.md` | `21a2e1af6fe409c788b1af1b11f30ac913e8488484a10529236193fa72c2a863` | `bce8d38772c7debf86ea032027da920f9f2da4e56e5092cb9998224cff13b646` | Изменён (добавлены новые разделы) |
| `БИОГРАФИИ/Стивен Чарнок/16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN.md` | `41d98132f96eb62703b8803ecc89d28a87e96b2ae03f870c056472275116f313` | `273278778733bd5d7d2e72e897ea87d39583ff37cd6464620f01646b815f4d3b` | Изменён (добавлены новые разделы) |
| `ЧARNOK_art2_deepening_proposals.md` | — (новый) | `9ce76deaa4ad37aac1faba70bf9ceebb5146d5d19c7b118cea63d60ca31513f0` | Новый файл (deliverable d) |
| `ЧARNOK_theology_map_primary_locators.md` | — (новый) | `d3f5348f78a571b312fc32e7eb00ce62988f7887c181fe108f0124d751da9cb6` | Новый файл (deliverable a) |
| `ЧARNOK_new_findings.md` | — (новый) | `5e53c9666b10b2f9edabd6012ec09f3b1dde631c8e74a77fc018b8fca2010877` | Новый файл (deliverable b) |
| `ЧARNOK_audit_10_article_plan.md` | — (новый) | `d3e846ff2ffd97d232d36300a745934f08059bb692486e54708eeb4ec3667bef` | Новый файл (deliverable c) |
| `ЧARNOK_series_assembly_plan.md` | — (новый) | `387e6c13acd732b34e41f3bcd420af1e5497e5db941c638a7e9977acf5444e56` | Новый файл (deliverable e) |

**Корневая причина блокировки аудита:** `AGENT_RULES.md` имеет другой хеш, чем записан в квитации wave40. Скрипт `audit_charnock_handoff.py --require-receipt` сравнивает текущие файлы с манифестом квитации и отказывает при расхождении.

---

## 2. Шаги для новой квитации (координатор MAX)

### Шаг 1: Подтвердить изменение AGENT_RULES.md

Мерж PR #520 (2026-11-16) изменил `AGENT_RULES.md`. Это изменение было сделано в репозитории, не в рамках исследования ЧARNОКа. Координатор MAX должен подтвердить, что это изменение не затрагивает границы исследования ЧARNОКа и что новая квитация может использовать текущий хеш `7e4b4685…`.

### Шаг 2: Создать новый ZIP-пакет research-пакета

Включить в ZIP:
- Все 46 файлов из манифеста wave40 (с обновлёнными хешами для трёх изменённых файлов)
- 5 новых файлов ЧARNOK_*.md (deliverable a–e)
- Обновлённые `data/charnock-biographical-anchors-v1.json` (если изменения в quotationPlan или receptionReview)

### Шаг 3: Загрузить на Google Drive

Загрузить ZIP на Google Drive в папку, указанную в квитации wave40:
- `destinationParentIds`: `["15iNGKO8rN3vJKPbJuXfPVx4rXHER5Xq2"]`
- Получить `destinationObjectId`, `destinationBytes`, `destinationSha256`

### Шаг 4: Независимый destinationSHA256 readback

Выполнить `get_file` на загруженный объект, получить SHA256 readback. Сравнить с хешем ZIP.

### Шаг 5: Создать новую квитацию

Создать `data/charnock-handoff-receipt-v1.json` с:
- `sourceArchiveSha256` = хеш ZIP
- `destinationSha256Readback` = результат readback
- `verifiedAtUtc` = текущее UTC время
- `sourceManifestSha256` = SHA256 от канонического JSON манифеста
- `manifest.counts` = обновлённые счётчики (с учётом 5 новых файлов)

### Шаг 6: Проверить аудитом

Запустить `python scripts/audit_charnock_handoff.py --require-receipt`. Ожидаемый результат: `BOUNDED_RESEARCH_COMPLETE`, `publicationState: BLOCKED`.

---

## 3. Обновлённые счётчики манифеста (ожидаемые)

| Поле | Текущее (wave40) | Ожидаемое (с 5 новыми файлами) |
|------|-----------------|-------------------------------|
| tcpAnchors | 79 | 79 (без изменений) |
| xmlObjects | 11 | 11 (без изменений) |
| manualAnchors | 28 | 28 (без изменений) |
| biographicalDecisions | 40 | 40 (без изменений) |
| receptionCases | 5 | 5 (без изменений) |
| selectionSlots | 44 | 44 (без изменений) |
| selectionIds | 40 | 40 (без изменений) |
| plannedDocuments | 10 | 10 (без изменений) |
| dossierOwners | 18 | 18 (без изменений) |
| textCandidates | 16 | 16 (без изменений) |
| researchOnlyQuotes | 7 | 7 (без изменений) |
| illustrations | 1 | 1 (без изменений) |

5 новых файлов — это исследовательские артефакты, не входы в TCP-регистр или quotationPlan. Счётчики не меняются, но файлы добавляются в `manifest.files`.

---

## 4. Границы новой квитации

- Новая квитация **не снимает** PUBLICATION_HOLD
- Новая квитация **не делает** цитаты разрешёнными
- Новая квитация **не делает** AGENT_RULES.md корневым autoridad для ЧARNОКа
- Новая квитация **не архивирует** page images или автографы
- Новая квитация **не проверяет** внешние HTTP-URL

---

## 5. Ожидаемый результат после успешной квитации

```
{
  "state": "BOUNDED_RESEARCH_COMPLETE",
  "criteria": 6,
  "publicationState": "BLOCKED",
  "receiptObject": "<новый Google Drive ObjectId>",
  "counts": { ...те же 12 счётчиков... },
  "nextAction": "SEPARATE_USER_REQUEST_FOR_AUTHORING_OR_SCOPE_EXTENSION"
}
```

После этого авторство может начаться только по отдельному заданию пользователя.

---

**Готово к передаче координатору MAX.** Все материалы для новой квитации подготовлены; остаётся выполнить шаги 1–6 с участием Google Drive.