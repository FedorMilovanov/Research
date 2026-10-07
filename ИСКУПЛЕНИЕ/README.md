# Искупление — canonical research authority index

**Дата открытия корпуса:** 2026-10-07
**Статус корпуса:** `WAVE-0 / CHARTER + TERMINOLOGY + SOURCE-REGISTRY OPEN / NOT-FOR-PUBLICATION`
**Canonical directory:** `ИСКУПЛЕНИЕ/`
**Machine registry:** [`../data/redemption-corpus-authority-2026-10-07.json`](../data/redemption-corpus-authority-2026-10-07.json)
**Validator:** [`../scripts/validate_redemption_corpus.py`](../scripts/validate_redemption_corpus.py)
**CI gate:** [`.github/workflows/redemption-corpus-integrity.yml`](../.github/workflows/redemption-corpus-integrity.yml)
**Google Drive intake root:** `07 — СЕРИЯ «ИСКУПЛЕНИЕ»` → `1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV`

**Authority rule.** Этот каталог (`ИСКУПЛЕНИЕ/`) — единственная canonical spine темы искупления. Всё, что появляется в других директориях или в Drive по той же теме, является input-ом или зеркалом, а не параллельной authority. Последующая adjudication внутри каталога заменяет более раннюю очередь, если они противоречат друг другу, — но только явной записью, а не молча.

> **Research closure ≠ Product publication approval.** Открытие отдела не означает, что какой-либо материал готов на `gospod-bog.ru`. Ни одна формулировка отсюда не переносится в `FedorMilovanov/gb-is-my-strength`, пока соответствующий dossier не закрыт до уровня `PUBLICATION-CANDIDATE` и пока Product не прошёл собственную проверку на актуальном source anchor.

---

# 1. Что уже сделано (Wave 0)

| # | Документ | Что владеет | Статус |
|---|---|---|---|
| 00 | `00_CURRENT_AUTHORITY_2026-10-07.md` | статусная карточка: кто чем владеет, цифры доказательной базы, действующие HOLD, границы | `CURRENT / STATUS-CARD` |
| 00 | `00_MASTER_RESEARCH_MAP_AND_CHARTER_2026-10-07.md` | вопрос, метод, границы, волны, series plan v1, forbidden claims | `CURRENT / CHARTER` |
| 01 | `01_W0_INTRODUCTION_AND_TERMINOLOGY_2026-10-07.md` | введение и определения терминов; русско-языковой терминологический узел | `CURRENT / DRAFT-INTERNAL` |
| 02 | `02_W0_SCRIPTURE_CORPUS_FOR_WHOM_2026-10-07.md` | канонический корпус текстов «за кого» и инвентарь спорных locus | `CURRENT / INVENTORY` |
| 03 | `03_W0_SOURCE_REGISTRY_2026-10-07.md` | реестр учебников, монографий, первоисточников; классы и права | `CURRENT / REGISTRY` |
| 04 | `04_W0_COMPETING_MODELS_TAXONOMY_2026-10-07.md` | карта позиций и различений (в т. ч. hypothetical universalism) | `CURRENT / TAXONOMY` |
| 05 | `05_W0_ACQUISITION_FAMILIES_AND_DRIVE_INTAKE_2026-10-07.md` | семейства acquisition, критерии приёмки, Drive-разметка | `CURRENT / REQUEST-READY` |
| 06 | `06_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-10-07.md` | архитектурное предложение для сайта (только proposal) | `PROPOSAL / DO-NOT-IMPLEMENT` |
| 07 | `07_W0_DRIVE_MIRROR_RECEIPT_2026-10-07.md` | побайтное зеркало корпуса в Drive 07-дерева: ids, размеры, sha256, что здесь запрещено | `CURRENT / MIRROR-RECEIPT` |
| 10 | `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md` | верифицированный текст Второй главы постановлений Синода в Дордрехте (Arts I–IX) + фрагмент Кальвина на 1 Ин. 2:1–2 | `CURRENT / PRIMARY-TEXT-VERIFIED` |

---

# 1a. Что не входит в эту spine (история, а не удаление)

В более ранней сессии проекта по этой теме описывались ещё два файла: `01_VVEDENIE_TERMINY_I_OPREDULENIYA_2026-10-07.md` (введение-досье) и `100_PRODUKT_ARHITEKTURA_I_HANDOFF_2026-10-07.md` (архитектура продукта). В текущем checkout их нет (ни в рабочем дереве, ни в HEAD), и они **не** восстановлены по памяти: их роли явно переназначены — терминология владеет `01_W0_INTRODUCTION_AND_TERMINOLOGY_2026-10-07.md`, архитектура владеет `06_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-10-07.md`, а статусная карточка корпуса — `00_CURRENT_AUTHORITY_2026-10-07.md`. Введения в двух экземплярах в корпусе нет. Если эти файлы появятся извне, они принимаются как input и сверяются со spine, а не становятся второй параллельной authority; расхождение разрешается явной записью, а не молча.

---

# 2. Порядок чтения

1. `00_MASTER_RESEARCH_MAP_AND_CHARTER_2026-10-07.md` — что именно исследуется и чего делать нельзя.
2. `01_W0_INTRODUCTION_AND_TERMINOLOGY_2026-10-07.md` — что такое «искупление» и какие различения обязаны быть зафиксированы до спора.
3. `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md` — первый зафиксированный первичный текст ( hinge-документ всей дискуссии).
4. `02_W0_SCRIPTURE_CORPUS_FOR_WHOM_2026-10-07.md` — текстовая база.
5. `04_W0_COMPETING_MODELS_TAXONOMY_2026-10-07.md` — чью позицию мы описываем и как честно.
6. `03_W0_SOURCE_REGISTRY_2026-10-07.md` + `05_W0_ACQUISITION_FAMILIES_AND_DRIVE_INTAKE_2026-10-07.md` — чем доказываем и что ещё нужно добыть.
7. `06_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-10-07.md` — как это однажды выйдет наружу.

---

# 3. Обязательные правила этого корпуса

1. **Спорная формулировка без A-опоры остаётся ограниченной или удаляется.** Тема по определению спорная; `B1` не может быть единственной опорой quote-safe тезиса.
2. **Текст Писания цитируется только из верифицированного файла корпуса.** Пока `BIBLE_CORPUS` (see [`../BIBLE_CORPUS/00_BIBLE_CORPUS_RIGHTS_PROVENANCE_AUTHORITY_2026-08-06.md`](../BIBLE_CORPUS/00_BIBLE_CORPUS_RIGHTS_PROVENANCE_AUTHORITY_2026-08-06.md)) не закрыл Synodal-модуль, в досье допускается пересказ с ссылкой на место, но не «цитата из Синодального».
3. **Исторический автор цитируется только по странице своего издания.** Конфессиональные и полемические тексты семнадцатого века цитируются по конкретному изданию (латинское/английское, том, страница), а не по пересказу у современного автора.
4. **Позиция противника описывается в её сильнейшей форме.** Арминианская, лютеранская, hypothetical-universalist и remonstrant-side позиции даются по их собственным документам (Remonstrance 1610, Amyraut, Davenant, Baxter, и современные защитники), а не по карикатуре полемиста.
5. **Название доктрины — предмет редакционного решения, а не аргумент.** «Ограниченное искупление», «определённое искупление», «частное искупление», «всеобщее искупление», «общее искупление» фиксируются в `01_...` и `06_...` с явным указанием, кто так называет и почему.
6. **Прямые цитаты авторов XX–XXI вв. не публикуются без полной проверки страницы и прав.** Для них действует `RIGHTS_HOLD + PUBLICATION_HOLD` по умолчанию.

---

# 4. Текущая граница

```text
CHARTER, TERMINOLOGY, INVENTORY, SOURCE REGISTRY, DRIVE SKELETON = OPENED (Wave 0)
PRIMARY TEXTS VERIFIED BY BYTES                     = 1 (Canons of Dort, Head II, Arts I–IX)
QUOTE-SAFE CLAIMS                                   = 0
PD BOOK COPIES PRESENT IN Drive (unhashed, unread)  = 4  (Owen Works, Goodwin, Calvin Institutes, WCF)
READER-READY DRAFTS                                 = 0
PRODUCT IMPLEMENTATION                              = NOT STARTED
```

Ничто в этом корпусе не может быть описано как «исследовано», «доказано» или «готово к публикации», пока не закрыт соответствующий wave в `00_...` §6 с явным exit-критерием.
