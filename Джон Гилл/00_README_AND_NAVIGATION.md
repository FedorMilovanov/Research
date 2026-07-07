# Джон Гилл (1697–1771) — исследовательский отдел

**Дата создания:** 2026-07-06  |  **Режим:** консолидация исследований Гилла из AuditRepo → Research (по указанию владельца; «чтобы не путаться»).
**Canonical home:** это папка — единственное место хранения исследований по Гиллу. Аудит-отчёты (баги/CI) остаются в `FedorMilovanov/AuditRepo` (см. ссылки ниже) — они НЕ перенесены.

Связь с сайтом: результаты ложатся в основу серии `dzhon-gill` на [gb-is-my-strength](https://github.com/FedorMilovanov/gb-is-my-strength) (5 частей + Справочник). План: добавить сфокусированную статью **«Богословие Гилла»** (Часть IV, экзегетический климакс).

---

## 🔎 Уровни верификации источников (по AGENT_RULES.md)

- **Level A — первичные источники, public domain (цитировать можно):** johngill.thekingsbible.com (*Exposition of the Bible*, все цитаты Гилла по 9+ текстам); archive.org (*The Cause of God and Truth*, Tegg 1838, предисловие = первичный якорь структуры); ccel.org/ccel/gill/doctrinal (*A Body of Doctrinal Divinity*, полное оглавление 7 книг); reformedreader.org (Gill's *Declaration of Faith*).
- **Level B — контент сайта (проверен автором):** `src/content/articles/dzhon-gill-*.mdx` (прочитаны заголовки/объёмы для аудита покрытия).
- **Level C / осторожно — вторичная литература:** SBJT 25.1 (2021), TGC, SEBTS Rathel (2017), Nettles (*By His Grace*), George, Ella (*John Gill and the Cause of God and Truth*) — цитируются с пометкой, особенно в споре о гипер-кальвинизме.

---

## 📚 Тома отдела (порядок углубления)

| № | Файл | Суть | Ключевая добыча |
|---|---|---|---|
| 01 | `01_SERIES_GAPS_AND_PRIMARY_SOURCES.md` | Лакуны серии + каталог первоисточников A–G | Главная лакуна: богословие Гилла не выделено в статью; A–G первоисточники на сайте |
| 02 | `02_THEOLOGY_DEEP_DIVE.md` | Позиции Гилла с прямыми цитатами | 5 пунктов кальвинизма; завет благодати; экзегеза 1 Тим 2:4, Ин 3:16; вечное оправдание; сбалансированный гипер-кальвинизм |
| 03 | `03_STRUCTURE_PROPOSAL.md` | Структура серии: добавить Часть IV. Богословие | Серия УЖЕ = «Введение + I + II + III + Справочник»; рекомендация — Часть IV. Богословие (6 документов) |
| 04 | `04_CONTENT_DEEPENING_AUDIT_AND_EXEGESIS_SET.md` | Аудит покрытия 5 MDX + 7-текстовый экзегетический сет | Богословие УЖЕ вшито в Часть II; 7 текстов с цитатами (1 Тим 2:4, Ин 3:16, 2 Петр 3:9, 1 Ин 2:2, Ин 1:29, Рим 8:29, Рим 9); Cause of God and Truth 4 части (из предисловия) |
| 05 | `05_BODY_OF_DIVINITY_TOC_AND_ARTICLE_SKELETON.md` | Полное оглавление *Body of Divinity* (7 книг) + каркас статьи | Book VI.4 «Texts seeming to Favour Universal Redemption» = точная параллель 7-текстовому сету; каркас из 7 разделов |
| 06 | `06_SITE_INDEX_LAW_ANTINOMIANISM_ELECTION.md` | Полный индекс сайта (20 статей) + закон/антиномизм + избрание/вера | Карта ссылок: `rimlyanam-7` (Рим 7→закон), `krajne-li-isporcheno-serdce` (total depravity); Рим 3:31 (закон утверждён), Деян 13:48 (вера = плод декрета); Cause Part III «arguments from reason» |

---

## 🎯 План статьи «Богословие Гилла» (8 разделов, итог)

1. Введение — Гилл-систематик (*Body of Divinity*).
2. Вечный замысел: избрание и завет (Рим 9:11; завет Троицы; Рим 8:29; Деян 13:48).
3. Грех и нужда → `krajne-li-isporcheno-serdce`.
4. Христос и искупление + 7-текстовый сет (particular redemption).
5. Применение спасения: оправдание, рождение свыше (Ин 3:3), призвание, претерпение.
6. Закон и антиномизм (Рим 3:31) → `rimlyanam-7-veruyushchiy-ili-neveruyushchiy`.
7. Спор о «гипер-кальвинизме» (сбалансированно; Cause Part III).
8. Заключение + асайды: герменевтика (`hermenevticheskaya-otsenka-…`), канон (`kod-da-vinchi`), баптистская идентичность (серия `russian-baptism`).

---

## 🔗 Перекрёстные ссылки

- **Сайт (gb-is-my-strength):** серия `dzhon-gill` (`src/content/articles/dzhon-gill-*.mdx`); ключевые статьи для ссылок: `rimlyanam-7-veruyushchiy-ili-neveruyushchiy`, `krajne-li-isporcheno-serdce`, `hermenevticheskaya-otsenka-hristotsentrichnoy-germenevtiki`, `kod-da-vinchi`, серия `russian-baptism`.
- **AuditRepo (аудиты, НЕ перенесены):** `AUDIT_gb-main_36b815c2_2026-07-06_cycle4.md` — D-23 (deploy-блокирующая регрессия Gill play-smoke; код чинит другой агент). Матрица: `verified/MASTER_BUG_MATRIX.md`.
- **Другие отделы Research:** `БАПТИСТЫ РОССИИ` (баптистская идентичность Гилла), `СЕРИЯ СЕРДЦЕ` (антропология/сердце — смежно с total depravity и законом).

> Примечание аудитора: все тома — исследование/каркас. Авторинг статей и правка кода — вне режима аудитора.
