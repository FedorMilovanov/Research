# Исследование: структура серии «Джон Гилл» — добавляем Часть IV. Богословие

> Часть 3 контентного досье Гилла (arena-auditor, 2026-07-06). Режим:研究/рекомендация, НЕ авторинг.
> Ответ на вопрос владельца: *«добавим ещё одну статью? Четвёртую? Будет введение и 1-2-3-4 и справочник?»*

---

## 1. Текущая структура серии (доказательство)

Источник: `data/series.json` → ключ `dzhon-gill` + метки из `gillSeriesData.ts` (проверено `gill:series:data:consistency:audit`).

| n | slug | title | series-mark | rt |
|---|---|---|---|---|
| 1 | `dzhon-gill-istoricheskiy-kontekst` | Исторический контекст | **Введение** (label) | 16 |
| 2 | `dzhon-gill-chast-1-chelovek` | Часть I. Человек | **I** (roman) | 32 |
| 3 | `dzhon-gill-chast-2-uchenyi` | Часть II. Учёный | **II** | 39 |
| 4 | `dzhon-gill-chast-3-nasledie` | Часть III. Наследие | **III** | 54 |
| 5 | `dzhon-gill-spravochnik` | Справочник по Гиллу | **Справ.** (label) | 8 (самая маленькая) |

**Ответ:** серия УЖЕ построена ровно как **«Введение + I + II + III + Справочник»** — то есть твоя интуиция «введение и 1-2-3-4 и справочник» уже реализована (без «4»). Серия поддерживает и roman-метки (I/II/III), и label-метки (Введение/Справ.) — значит добавить roman «IV» технически тривиально.

---

## 2. Рекомендация: да, добавить «Часть IV. Богословие»

**Итоговая структура (6 документов):**
```
Введение (Исторический контекст)
  ├─ I.  Человек      (биография)
  ├─ II. Учёный       (биография)
  ├─ III. Наследие    (биография)
  ├─ IV. Богословие   (ДОКТРИНА)   ← НОВОЕ, «недостающее золото»
  └─ Справочник       (факт-аппендикс)
```

**Почему именно «Богословие» — единственная логичная «Четвёртая»:**
- I–III — **биографичны** (Человек/Учёный/Наследие). Справочник — факт-аппендикс.
- Реальная значимость Гилла — **доктринальная**: particular redemption, вечное оправдание, завет благодати, спор о «гипер-кальвинизме». Без «Богословия» серия описывает *жизнь*, но не *учение* — самое ценное для читателя gospod-bog.ru остаётся за кадром.
- Это закрывает главную лакуну, отмеченную в ч.1 досье (`RESEARCH_gill-series-gaps-primary-sources`): «богословие Гилла не выделено в статью».

**Где вставить (data-shape):** как `n=5` (Часть IV. Богословие, roman-метка `IV`), сдвинув Справочник на `n=6`. Консистентность `series.json` ↔ `gillSeriesData.ts` ↔ MDX ↔ search-manifest проверяется `gill:series:data:consistency:audit` (сейчас зелёный) — после добавления прогнать этот гейт.

---

## 3. Конкретный план «Богословие Гилла» (материал готов в ч.2)

Готовый материал с прямыми цитатами из первоисточников уже собран в `RESEARCH_gill-theology-deep-dive_2026-07-06.md`. Адаптация под одну статью (8 разделов):

1. **Введение:** кто такой Гилл и почему его богословие актуально (связать с Введением и III. Наследие).
2. **Метод и завет благодати:** завет как вечный завет Троицы (две администрации, Агарь/Сарра) — цитата из *Body of Divinity* Book IV.
3. **Сотериология (5 пунктов):** избрание/отвержение, particular redemption, действенная благодать, претерпение святых, total depravity.
4. **Экзегеза спорных текстов (ЗАВЕРШЕНА цитатами):**
   - **1 Тим 2:4** — «все» = всякие роды людей (цари/бедные/язычники), не каждый индивид → `johngill.thekingsbible.com/CommentaryVerse/54/2/4`.
   - **Ин 3:16** — «мир» = язычники/избранные среди них, не каждый человек → `CommentaryVerse/43/3/16`.
   - **2 Петр 3:9** — «us/any» = избранные; «не желая, чтобы кто погиб» = избранные во Христе; долготерпение ради них → `CommentaryVerse/61/3/9` (цитата получена в cycle 4: «the persons intended by us are manifestly distinguished from 'some men'... nor is it true of all men, that God is not willing that any of them should perish»).
   - **Рим 9** — избрание по Рим 9:11 → *Body of Divinity* Book II (ccel.org/ccel/gill/doctrinal).
5. **Вечное оправдание:** *Body of Divinity* Book II, «Of Other Eternal and Immanent Acts in God, Particularly Adoption and Justification».
6. **Церковь и ординации:** кредобаптизм (крещение — prerequisite для Вечери; *Declaration of Faith* art. XI), ординации.
7. **Спор о «гипер-кальвинизме» (сбалансированно):** Rathel 2017 (был) · Toon (был) · Nettles/George (нет) · Ella (защита, остерегаться quote-mining p.156); нюанс: free offer Евангелия без duty-faith.
8. **Заключение:** Гилл между «высоким» кальвинизмом и евангельским предложением; связь с современностью.

---

## 4. Первоисточники для цитирования (A–G, из ч.1)

- **A.** *The Cause of God and Truth* (4 т., 1735–38) — archive.org, 1838, public domain.
- **B.** *A Body of Doctrinal Divinity* (1769–73, 3 т.) — archive.org т.1 / т.3.
- **C.** *An Exposition of the Old and New Testaments* (9 т., 1746–63) — johngill.thekingsbible.com.
- **D.** Rippon, *Brief Memoir* (1838) — archive.org.
- **E.** *The Doctrine of the Trinity* (1731) — archive.org.
- **F.** *A Dissertation Concerning the Antiquity of the Hebrew Language* (1767) — archive.org.
- **G.** Gill's *Declaration of Faith* — reformedreader.org (art.VI particular redemption, VIII irresistible grace, IX perseverance, XI baptism).
- PRDL (113 works) · CCEL (gill).

---

## 5. Перекрёстные ссылки

- Ч.1 (лакуны + первоисточники): `RESEARCH_gill-series-gaps-primary-sources_2026-07-06.md`
- Ч.2 (глубокая теология + цитаты): `RESEARCH_gill-theology-deep-dive_2026-07-06.md`
- Матрица: `verified/MASTER_BUG_MATRIX.md` (cycle-4 блок, pointer D-«Gill-structure»)
- Данные серии: `data/series.json` (`dzhon-gill`), `src/pages/articles/dzhon-gill-*/`, `src/components/article-pilots/gill-series/`
- Аудит cycle 4 (D-23 и пр.): `AUDIT_gb-main_36b815c2_2026-07-06_cycle4.md`

> Примечание аудитора: рекомендация только по структуре/контенту. Написание статьи — вне режима аудитора (нужен switch в author/fix mode).
