# 16. Подпольная печать — Bulletin №44 (1977) PDF verification

**Текущее решение:** изображения выбранных страниц рабочего PDF уже прочитаны по [записи от 18.11.2026 в досье 14](14-podpolnaya-pechat-golden-chapter-source-to-claim-2026-09-06.md#визуальная-проверка-контрольных-pdf); историческое факсимиле и публикационный допуск **не проверены**. [Точный объём и оставшиеся задачи](#working-pdf-scope).

> **HISTORICAL:** исходная запись ниже (включая проверку байтов 12.09.2026) сохранена до раздела «Актуальная граница проверки». Её общий статус `FACSIMILE VISUAL PENDING` и задача повторно увидеть титул/«Христианин» **SUPERSEDED только для выбранных изображений современной рабочей вёрстки**. Старое условие «достаточно успешного рендера» не удостоверяет историческое факсимиле. Утверждения о live source и Product `main` — исторический срез, не новая удалённая проверка.

**Дата:** 2026-09-06  
**Lane:** `book/podpolnaya-pechat-golden-chapter` / PR #1794  
**Status:** `PDF/TEXT VERIFIED`; `LOCAL BINARY PRESENT`; `SHA256 VERIFIED`; `FACSIMILE VISUAL PENDING`.

## Source

Public corpus URL:

`https://propovednik.com/media/mp3/Литература/Бюллетени совета родственников и узников 1970-1987/1971-1977 Синька/044-1977.pdf`

The live source resolves as an 87-page PDF. This closes the earlier ambiguity between a merely catalogued URL and an actually reachable issue.

A controlled local binary already exists in the Product repository on `main`:

- path: `baptisty-rossii/research/raw-sources/bulletin-council-relatives-044-1977.pdf`;
- size: **1,171,788 bytes**;
- Git blob SHA: `66f54198e369f836387a18b40c203468c662a4eb`;
- SHA256: `79e9fab61164ffd2c881ac641402e8b8bd9806bad8cf9b1360aa8b35568ce55c`.

Important: the Git blob SHA is repository object identity, **not SHA256 of the PDF bytes**. Both are now recorded independently. On 2026-09-12 the exact file in the primary local clone (`C:\\Users\\Fedor\\Documents\\GitHub\\gb-is-my-strength`) was checked with `Get-FileHash -Algorithm SHA256` and `git hash-object`; its byte length was 1,171,788, its Git blob SHA matched the GitHub repository object exactly, and its SHA256 was fixed as shown above.

## Page-level text anchors

### PDF page 1 / source page P0

The title page identifies:

- issue **44**;
- **Москва, 1977 г.**;
- `БЮЛЛЕТЕНЬ СОВЕТА РОДСТВЕННИКОВ УЗНИКОВ ЕВАНГЕЛЬСКИХ ХРИСТИАН-БАПТИСТОВ В СССР`.

This is sufficient to identify the object as Bulletin no. 44, 1977. It is not yet a visually verified facsimile because the current web screenshot renderer returned a cache-miss error.

### PDF page 7 / source page P6

The issue asks readers to continue prayer and petitions for arrested workers of the underground publisher `Христианин` and names:

- И. И. Левен;
- Д. И. Кооп;
- Людмила Зайцева;
- Лариса Зайцева.

The text states that they were still under investigation in a Leningrad prison. This directly supports the current source-to-claim ledger's 1977 printing/publisher layer.

Adjacent pages also contain contemporaneous notices about G. P. Vins in the Tabaga camp, Ya. P. Volf, military-service cases and petitions to Soviet authorities. These may be used as issue context but should not be expanded into quantitative repression claims without a separate corpus-wide inventory.

## Production classification

What may now be treated as verified:

- Bulletin no. 44 is a real, reachable 1977 PDF object;
- the exact PDF binary is already stored in the repository's controlled `raw-sources` corpus;
- repository object identity and byte size are known;
- the issue itself identifies the series and issue number;
- the named `Христианин` workers appear in the issue-level text;
- the 1977 source can serve as a primary-document anchor for the underground-printing chapter.

What remains open:

1. run visual page verification on the title page and the relevant `Христианин` page;
2. create a publication derivative only from that verified local binary;
3. record rights/provenance/caption before web use.

## Important guard

Do **not** mark this issue `FACSIMILE VERIFIED` yet. The web PDF text layer is available and the local binary is present, but the screenshot renderer failed with a cache miss. The correct state is `PDF/TEXT VERIFIED + LOCAL BINARY PRESENT + SHA256 VERIFIED`, while `FACSIMILE VISUAL PENDING` remains in force until a visual page read succeeds from the exact repository binary or another deterministic renderer.

<a id="working-pdf-scope"></a>

## Актуальная граница проверки

Это согласование с уже существующей [визуальной записью досье 14 от 18.11.2026](14-podpolnaya-pechat-golden-chapter-source-to-claim-2026-09-06.md#визуальная-проверка-контрольных-pdf), **не новое чтение PDF**. При этой сверке заново проверены только байты уже хранящегося [рабочего файла в Research](raw-sources/bulletin-council-relatives-044-1977.pdf): размер **1 171 788**, Git blob `66f54198e369f836387a18b40c203468c662a4eb` и SHA-256 `79e9fab61164ffd2c881ac641402e8b8bd9806bad8cf9b1360aa8b35568ce55c` совпали с файлом в текущем HEAD и неизменённой [ведомостью переноса](SOURCE_CUSTODY_MANIFEST.json). Ведомость — историческая квитанция, не реестр нового чтения. Новых загрузки, рендера, подсчёта страниц или live-проверки каталога не было.

| Объём | Что уже зафиксировано 18 ноября | Чего это не доказывает |
|---|---|---|
| PDF **1** | По изображению прочитаны номер **44**, «Москва, 1977 г.» | Идентичность конкретному историческому экземпляру, его обложке или архивной единице |
| PDF **7**, с. **4** этой вёрстки, п. **4** | Просьба Совета ходатайствовать за работников «Христианина»: Левена И. И., Коопа Д. И., Людмилу и Ларису Зайцевых; по словам Совета, они под следствием в Ленинграде | Судебный приговор, независимое подтверждение обстоятельств ареста или атрибуцию фотографии Ивангорода |
| PDF **6** и **8**, с. **3** и **5** этой вёрстки | Сообщение Совета о Винсе в Табаге и примечание о получении двух писем в конце июля | Независимый медицинский диагноз; остальные страницы не входят в визуальное чтение |

Прежние `P0` / `P6` — нулевые индексы PDF, не исторические страницы; здесь им соответствуют PDF **1** / **7**. Задача увидеть титул и страницу о «Христианине» выполнена **только в указанном объёме**. Это не полное чтение выпуска и не сверка всей современной транскрипции с оригиналом.

**Современный рабочий PDF ≠ историческое факсимиле.** В досье 14 зафиксированы Adobe InDesign CS5, создание в 2015 г., изменение в 2016 г., современный набор и навигация на просмотренных страницах. Нельзя выводить из них исторические оформление, пагинацию или способ печати. Упоминание `primary-document anchor` в историческом блоке выше не повышает эту вёрстку до проверенного оригинального свидетеля: допустимая формула здесь — «Совет сообщает / просит, в доступной рабочей версии № 44», с указанным локатором и оговорённой передачей текста.

**Разница 88/87 остаётся открытой.** Существующие CSV-записи `biulleten_sru_1977_44` и `toronto_sru_1977_44` описывают 88-страничные экземпляры Baylor/Keston; прежняя проверка рабочего PDF в досье 14 — 87 страниц. [Граница каталоговой идентификации](14-podpolnaya-pechat-golden-chapter-source-to-claim-2026-09-06.md#copy44-catalog-boundary) не позволяет объявить эти объекты тождественными или заключить, что в PDF потеряна страница. Ни экземпляр, ни box/folder, ни соответствие исторической пагинации не установлены. CSV-статус `holdings_page_verified` и `next_action` `Acquire local scan/OCR/visual check` не изменены.

**Следующее проверяемое действие для [FIG-02](15-podpolnaya-pechat-visual-dossier-2026-09-06.md#fig-02--primary-bulletin-facsimile):** получить законным путём снимок идентифицированного исторического экземпляра, сопоставить нужную страницу и происхождение; отдельно проверить права, подпись и публикационное решение. Повторный рендер современной вёрстки не заменяет этого шага. Производная для сайта не создана; старый пункт о ней остаётся условным, а не разрешением использовать текущий PDF как историческую иллюстрацию. Реестры, evidence/access/locator/rights/publication-состояния и HOLD не повышались. Общий `FACSIMILE VERIFIED` не присвоен.
