# Искупление — corpus-specific current authority (статусная карточка)

**Дата:** 2026-10-07
**Область действия:** только `ИСКУПЛЕНИЕ/` (тема: искупление/умилостивление, particular vs universal atonement)
**Статус:** `WAVE-0 / CLOSED_WITH_HOLDS / publicationEligible = false`

Этот файл — **не** введение и **не** досье. Он владеет только ответом на вопрос «что сейчас является действующим внутри корпуса и на какой границе всё стоит». Содержание владеют файлы, перечисленные ниже.

---

## 1. Кто чем владеет

| Вопрос | Владелец | Статус владельца |
|---|---|---|
| Что исследуется, метод, волны, границы, запрещённые тезисы, план серии | `00_MASTER_RESEARCH_MAP_AND_CHARTER_2026-10-07.md` | `CURRENT / CHARTER` |
| Индекс и обязательные правила корпуса | `README.md` | `CURRENT / INDEX` |
| Термины: искупление / умилостивление / замещение / примирение; различения 4.1–4.8 | `01_W0_INTRODUCTION_AND_TERMINOLOGY_2026-10-07.md` | `CURRENT / TERMINOLOGY` |
| Корпус текстов «за кого» (A/B/C/D/TC) и допуск к экзегезе | `02_W0_SCRIPTURE_CORPUS_FOR_WHOM_2026-10-07.md` | `CURRENT / INVENTORY` |
| Реестр учебников, монографий, первоисточников, лексикон; классы и права | `03_W0_SOURCE_REGISTRY_2026-10-07.md` | `CURRENT / REGISTRY` |
| Карта конкурирующих позиций и осей спора | `04_W0_COMPETING_MODELS_TAXONOMY_2026-10-07.md` | `CURRENT / TAXONOMY` |
| Семейства acquisition, критерии приёмки, Drive-политика | `05_W0_ACQUISITION_FAMILIES_AND_DRIVE_INTAKE_2026-10-07.md` | `CURRENT / REQUEST-READY` |
| Архитектура публикации на gospod-bog.ru | `06_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-10-07.md` | `PROPOSAL / DO-NOT-IMPLEMENT` |
| Первый проверенный первичный текст (Дорт, Head II, Arts I–IX; Кальвин на 1 Ин. 2:1–2) | `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md` | `CURRENT / PRIMARY-TEXT-VERIFIED` |
| Machine mirror | `../data/redemption-corpus-authority-2026-10-07.json` | `CURRENT` |
| Gate | `../scripts/validate_redemption_corpus.py`, `../.github/workflows/redemption-corpus-integrity.yml` | `ENFORCED` |

## 2. Состояние доказательной базы (цифры, а не настроение)

```text
scripture loci in inventory            = 71  (A 22 / B 23 / C 12 / D 7 / TC 7)
source records in registry             = 113
acquisition families                   = 13
original-language strings verified     = 0
quotations page-verified               = 0
verified primary texts                 = 2   (Dort Head II Arts I–IX; Calvin on 1 Jn 2:1–2)
reader-ready drafts                    = 0
publication-eligible                   = false
```

## 3. Действующие HOLD

- `EVIDENCE_HOLD` — любая атрибуция позиции (Amyraut, Davenant, Arminius, Оуэн, Мюррей) до чтения первичного текста; любое лексическое утверждение до словарной страницы (W1).
- `LOCATOR_HOLD` — печатная пагинация переводов (каноны Дорта, комментарий Кальвина); страницы в современных книгах.
- `ARCHIVE_HOLD` — полнотекстовые издания через проверенный канал; русско-язычный слой.
- `RIGHTS_HOLD` — все книги XX–XXI вв.; русские переводы PD-оригиналов; библейские переводы (Синодальный не ingested, Кассиановский — `PERMISSION_REQUIRED`).
- `PUBLICATION_HOLD` — весь корпус.

## 4. Границы

1. `BIBLE_CORPUS`-зависимость открыта: **ни одной цитаты из Синодального перевода** в досье, только место + пересказ.
2. Product (`FedorMilovanov/gb-is-my-strength`) не трогается: предложение архитектуры в `06_...` реализуется только через owner-PR после `W6`.
3. Drive: `07 — СЕРИЯ «ИСКУПЛЕНИЕ»` (`1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV`) — единственная приёмная структура корпуса; полные тексты защищённых книг туда не загружаются.
4. Корпус не конкурирует с корневой `CURRENT_AUTHORITY.md` за root-authority; он владеет только своим evidence graph.

## 5. Что здесь никогда не появится

Здесь никогда не появятся формулировки «исследовано», «доказано», «готово к публикации» и заявления о закрытии цитатного корпуса — до тех пор, пока соответствующий wave в `00_...` не закрыт по своему exit-критерию и gate не прошёл зелёным.
