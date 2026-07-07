# ИССЛЕДОВАНИЕ: серия «Джон Гилл» — лакуны контента + первоисточники

> **Статус:** исследовательское досье аудитора (НЕ баг-репорт, НЕ правка кода).
> **Дата:** 2026-07-06. **Объект:** `main` @ `14a49be8` (gb-is-my-strength).
> **Место:** `incoming/arena-auditor/2026-07-06/`. См. перекрёстные ссылки в конце.
> **Лицензия первоисточников:** издание *The Cause of God and Truth* (Tegg, 1838) на archive.org помечено `NOT_IN_COPYRIGHT` — общественное достояние, допустимо цитировать/выдерживать.

---

## 1. Инвентарь серии (источник: `data/series.json` → `"dzhon-gill"`, 5 частей, все `published`)

| n | slug | title | rt | проза (слов)* |
|---|---|---|---|---|
| 1 | `dzhon-gill-istoricheskiy-kontekst` | Исторический контекст | 16 | ~3834 |
| 2 | `dzhon-gill-chast-1-chelovek` | Часть I. Человек | 32 | ~7759 |
| 3 | `dzhon-gill-chast-2-uchenyi` | Часть II. Учёный | 39 | ~8745 |
| 4 | `dzhon-gill-chast-3-nasledie` | Часть III. Наследие | 54 | ~11834 |
| 5 | `dzhon-gill-spravochnik` | Справочник по Гиллу | 8 | ~2705 |

\* проза = `cat src/components/article-pilots/gill-*/Gill*Section*.astro | sed 's/<[^>]*>//g' | wc -w` (грубо).

**Самая маленькая:** Справочник (2705 сл / rt 8). **Средняя:** Исторический контекст (3834 / rt 16). Части I–III крупные.

---

## 2. Лакуны контента (что НЕ хватает)

Серия **биографическая**; собственное **богословие Гилла** не выделено в статью. Приоритет лакун:

1. **★★★ «Богословие Джона Гилла»** (синтез из *Body of Doctrinal Divinity*): избрание, завет благодати, particular redemption, непреодолимая благодать, претерпение святых, Троица, закон/благодать. Естественная «Часть IV/VI». → СМ. первичный источник **B**.
2. **★★★ «The Cause of God and Truth»** — его главный полемический труд (кальвинизм vs арминианство Уитбя). Нет посвящённой статьи. Критично для рус. реформ./бапт. аудитории. → СМ. **A**.
3. **★★ «Exposition» (комментарий)** — magnum opus (9 тт). Не представлен; можно обогащать существующие статьи его экзегезой (Рим 9, 2 Петра, Ин). → СМ. **C**.
4. **★★ Крещение / экклесиология (baptist catholicity)** — Particular Baptist distinctive; на сайте есть ссылка на TGC, но, вероятно, тонко. → СМ. **G** (Gill's Confession, арт. XI) + вторичный TGC.
5. **★ Иврит / Троица** — *Dissertation on Hebrew* (1767) и *Doctrine of Trinity* (1731) упомянуты ссылками, но не раскрыты (Часть II «Учёный» могла бы углубить). → СМ. **E**, **F**.

**Маленькие статьи (кандидаты на расширение):** Справочник (добавить entries по трудам/терминам/таймлайну), Исторический контекст (углубить фон диссентерства).

---

## 3. Первоисточники (извлечены из `src/components/article-pilots/gill-*` → внешние `href`)

### A. The Cause of God and Truth (4 ч., 1735–1738) — ★★★
- **Ссылка на сайте:** `https://archive.org/details/causeofgodtruthi00gill` (изд. Tegg, 1838; 632 с.; `NOT_IN_COPYRIGHT`).
- **Что это:** ответ на *Discourse on the Five Points* англиканского арминианина Daniel Whitby. Структура:
  - **Part I (1735):** экзегеза ~60 мест Писания, которые арминиане использовали «за универсальную схему» (предопределение, искупление, первородный грех, действенная благодать, претерпение, язычники).
  - **Part II (1736):** защита мест в пользу particular/special grace.
  - **Part III (1737):** опровержение рациональных аргументов (Гоббс, стоики); защита кальвинизма разумом.
  - **Part IV (1738):** свидетельства ранних отцов (до Августина) — Гилл показывает, что «пять пунктов» не новшество.
- **Читать для:** аргументация по 1 Тим 2:4, 2 Пет 3:9, Ин 3:16, Рим 9, Иак 2:19 и др. (список мест есть у baptists.net).
- **Заметка:** Ратхел называет это (наряду с Owen, *Death of Death*) «лучшей учёной защитой кальвинизма».

### B. A Body of Doctrinal Divinity (1769–1773, 3 книги) — ★★★
- **Ссылки на сайте:** `archive.org/.../a-body-of-doctrinal-divi_gill-john_1769_1` (т.1) и `_1770_3` (т.3).
- **Структура (по Monergism/Logos):** Кн.I Бог, Его слово, имена, природа, совершенства, Лица (Троица); Кн.II вечные декреты (избрание, отвержение), вечный союз избранных, вечный завет благодати (Отец/Сын/Дух); Кн.III вечные дела, творение (ангелы/человек), грехопадение, заражённость, импутация Адамова греха; Кн.IV явление завета благодати во времени (патриархи/Моисей/Давид/НЗ); Кн.V благодать Христа (воплощение, уничижение, активное/пассивное послушание, смерть); Кн.VI благословения благодати (искупление).
- **Важно:** Гилл — **первый баптист, написавший полную систематическую теологию**. Пастор New Park Street (позже — Метрополитен-тэбернакл Спёрджена) 51 год. Поч. D.D. Абердина (1748).
- **Дополнение:** *A Body of Practical Divinity* (1770) — проповеди на катехизис/десять заповедей.

### C. An Exposition of the Old and New Testaments (9 тт, 1746–1763) — ★★
- **Ссылка на сайте:** `https://johngill.thekingsbible.com/` (полный текст экзегезы по стихам).
- **Что это:** magnum opus, **крупнейший библейский комментарий одного автора** (6 тт ВЗ + 3 тт НЗ, ~7370 с.). Спёрджен: «лучший комментатор ВЗ». Подход: summary книги → главы → verse-by-verse, с упором на еврейскую учёность и раввинические источники.
- **Читать выборочно:** Рим 9 (избрание: цитирует Рим 9:11, 9:29, Еф 2:8-10, Рим 11:5-6), 2 Петра (детальная экзегеза, см. christianity.com/commentary/john-gill/2-peter), Ин.

### D. Rippon, *Brief Memoir of the Life and Writings of John Gill* (1838) — ★★
- **Ссылки на сайте:** `archive.org/details/briefmemoiroflif00ripp` (+ `_djvu.txt` для машинного извлечения).
- **Что это:** базовое биографическое свидетельство (для сверки дат/фактов Частей I и III).

### E. The Doctrine of the Trinity Stated and Vindicated (1731) — ★
- **Ссылка на сайте:** `archive.org/.../the-doctrine-of-the-trin_gill-john_1731`.
- **Что это:** защита Троицы, включая аутентичность 1 Ин 5:7 (Comma Johanneum). Для углубления раздела о Троице.

### F. A Dissertation Concerning the Antiquity of the Hebrew Language… (1767) — ★
- **Ссылка на сайте:** `archive.org/.../a-dissertation-concernin_gill-john_1767`.
- **Что это:** защита божественного происхождения/древности огласовок иврита (против тех, кто считал точки поздней масоретской вставкой). Для углубления Части II («Учёный»).

### G. Собственное «Confession of Faith» Гилла — первичный источник
- **Ссылка:** `https://www.reformedreader.org/ccc/johngilldeclarationoffaith.htm` (не на сайте, но первично).
- **Что это:** его исповедание. Ключевое: арт.VI particular redemption; арт.VIII непреодолимая благодать; арт.IX претерпение; арт.XI крещение — необходимое условие Вечери (credobaptism). Прямая опора для статей о богословии и крещении.

### Каталоги / агрегаторы
- **PRDL** (113 назв., 148 тт): `https://www.prdl.org/author_view.php?a_id=1996` — навигация/библиография.
- **CCEL / The John Gill Archive**: `https://www.ccel.org/ccel/gill` — собрание сочинений.

### Вторичные / академические (для контекста и точности)
- **SBJT 25.1 (2021)** спецвыпуск о Гилле — на сайте (`cf.sbts.edu/equip/uploads/2021/10/SBJT-25.1-Complete.pdf`): Scheiderer «John Gill and the Continuing Baptist» (eternal covenant), Rathel «John Gill and the Rule of Faith».
- **TGC**: «Baptist Catholicity in the Ecclesiology of John Gill» — `thegospelcoalition.org/themelios/...`.
- **SEBTS**: «John Gill and the Rule of Faith» — `sebts.edu/.../4-John-Gill-and-the-Rule-of-Faith-David-Rathel.pdf`.
- **Queen Mary Dissenting Academies Project**; **British History Online** (statutes); **legislation.gov.uk** (Act of Uniformity 1662, Conventicle 1664, Five Mile 1665, Test 1673).

---

## 4. Научный нюанс: спор о «гипер-кальвинизме» (обязателен для статьи о богословии)

Идентичность Гилла как «гипер-кальвиниста» — предмет дебатов:
- **David Rathel**, «Was John Gill A Hyper-Calvinist?» (*Baptist Quarterly* 48:1, 2017, DOI 10.1080/0005576X.2016.1255421): аргументирует, что Гилл **был** гипер-кальвинистом — отвергал «Gospel offer» и «duty-faith», минимизировал человеческую ответственность в принятии спасения.
- **Peter Toon** (*The Emergence of Hyper-Calvinism…*, 1967): Гилл — отец баптистского гипер-кальвинизма.
- **Tom Nettles** (*By His Grace and for His Glory*, 1986) и **Timothy George**: Гилл **не** был гипер-кальвинистом.
- **George Ella**, *John Gill and the Cause of God and Truth* (Go-Publications, 1995/2009): защитительная биография; предостерегает от вырывания цитат из контекста (с. 156 — фраза, которую приписывают Гиллу, на деле им опровергается).

**Рекомендация:** любая статья о богословии Гилла должна прямо адресовать этот спор (particular redemption + отказ от «duty-faith» ≠ «Гилл не проповедовал Евангелие»). Без баланса статья будет односторонней.

---

## 5. Биография — сверка фактов (cross-check: Theopedia / Wikipedia / CCEL / Britannica / Grokipedia)

| Факт | Значение | Примечание к сайту |
|---|---|---|
| Род. | 23.11.1697, Kettering, Northamptonshire | — |
| Языки | греч. к 11 годам; иврит самоучкой (Buxtorf) | Часть II «Учёный» |
| Обращение | ~12 лет (проповедь W. Wallis, Быт 3:9) | — |
| Крещение | погружением 1.11.1716 (≈19 лет), Kettering | — |
| Пасторство | **1719** — Goat Yard Chapel, Horsleydown, Southwark; 51 год | сайт верно: «Декларация 1729» = подтверждение 1689 Исповедания (отдельно от начала пасторства) |
| Лектор | 1729–1756, среда-вечерний лектор, Great Eastcheap (оттуда проповеди → *Cause of God and Truth*) | — |
| D.D. | 1748, поч. доктор Абердинского ун-та | — |
| Переезд | 1757 → Carter Lane (позже Метрополитен-тэбернакл Спёрджена); поддерживал Уайтфилда на Kennington Common | — |
| Смерть | 14.10.1771, Camberwell | — |

---

## 6. Рекомендованный порядок чтения первоисточников (для будущей статьи)
1. **A** *Cause of God and Truth* (Parts I–II) — аргументация по спорным текстам.
2. **B** *Body of Doctrinal Divinity* (Кн.I–VI) — систематика.
3. **C** *Exposition* (выборочно Рим/Ин/2 Петра) — экзегеза.
4. **D** Rippon *Memoir* — сверка дат.
5. **G** собственное Confession — particular redemption + крещение.
6. Вторичные: SBJT 25.1, Ella, Rathel (для нюанса гипер-кальвинизма).

---

## 7. Перекрёстные ссылки
- **Циклы аудита (этот же каталог):** [cycle1](../AUDIT_gb-main_e044908e_2026-07-05.md) · [cycle2](./AUDIT_gb-main_14a49be8_2026-07-06_cycle2.md) · [cycle3](./AUDIT_gb-main_14a49be8_2026-07-06_cycle3.md)
- **Матрица багов:** [../verified/MASTER_BUG_MATRIX.md](../verified/MASTER_BUG_MATRIX.md) (раздел «AUDITOR / ARENA — 2026-07-06»)
- **Серия в репо:** `data/series.json` → ключ `"dzhon-gill"`; страницы в `src/pages/articles/dzhon-gill-*`
- **Первоисточники (внешние):** A `archive.org/details/causeofgodtruthi00gill` · B `archive.org/.../a-body-of-doctrinal-divi_gill-john_1769_1` + `_1770_3` · C `johngill.thekingsbible.com` · D `archive.org/details/briefmemoiroflif00ripp` · E `archive.org/.../the-doctrine-of-the-trin_gill-john_1731` · F `archive.org/.../a-dissertation-concernin_gill-john_1767` · G `reformedreader.org/ccc/johngilldeclarationoffaith.htm` · PRDL `prdl.org/author_view.php?a_id=1996` · CCEL `ccel.org/ccel/gill`
- **Вторичные:** SBJT 25.1 `cf.sbts.edu/equip/uploads/2021/10/SBJT-25.1-Complete.pdf` · TGC themelios · SEBTS Rathel PDF · Rathel 2017 DOI `10.1080/0005576X.2016.1255421` · Ella 1995 · Toon 1967 · Nettles 1986
