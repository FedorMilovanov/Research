# ED-02 · независимое визуальное чтение Чарнока 1699 года: leaf n520 = печатная p. 521

**Дата проверки:** 23 ноября 2026. **Тип:** отдельный первоисточниковый визуальный свидетель, а не автоматически доверенная OCR-метка.

## Первичный источник

Стивен Чарнок, *The Works*, том II (1699), проповедь *Of the Lord's Supper*, цифровой экземпляр Internet Archive `bim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0`, **изображение leaf n520**.

- [Непосредственно страница n520](https://archive.org/details/bim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0/page/n520/mode/1up)
- [IIIF: верхняя четверть того же кадра, без интерпретации метаданных](https://iiif.archive.org/image/iiif/3/bim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0%2Fbim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0_jp2.zip%2Fbim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0_jp2%2Fbim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0_0520.jp2/pct:0,0,100,25/1600,/0/default.jpg)
- [IIIF: правая нижняя часть того же кадра — маргиналия](https://iiif.archive.org/image/iiif/3/bim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0%2Fbim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0_jp2.zip%2Fbim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0_jp2%2Fbim_early-english-books-1641-1700_the-works-of-_charnock-stephen_1699_0_0520.jp2/pct:65,42,35,48/1800,/0/default.jpg)

Обе части получены как реальные JPEG-данные IIIF через сетевой fetch и просмотрены непосредственно; один и тот же суффикс исходного листа `_0520.jp2` проверен в обоих URL.

## Визуальные наблюдения — узкий точный статус VERIFIED

**Колонтитул:** вверху листа чётко напечатаны «Vol. II:», «of the Lord's Supper.» и номер **«521»** справа. Таким образом, на **leaf n520 печатная страница 521**, а не 513. Связь `page_numbers.json` `n520 → p.513` имела `confidence=null` и сейчас **опровергнута изображением**. Это подтверждает ранее высказанную в обсуждении PR #629 гипотезу `p.521`.

**Маргиналия:** на правом нижнем поле именно того же n520 рядом с пассажем «Let then the bounty of Christ engage us» напечатана трёхстрочная сноска `* Lingend. / de Eucha- / rist. / p. 185.` (перенос внутри `Eucharist.`); источник прямо содержит указание **«Lingend. de Eucharist. p. 185.»**. Ранее значение `p.185` было подкреплено машинным чтением; **наличие и номер теперь лично проверены по графическому оригиналу**, без вывода из OCR.

## Что такое исправление не доказывает

1. **Не смешивать источники:** ранняя маргиналия из *Works* 1682 года на печатной p.621 ссылается на Lingendes **p.84,85**. Издание 1699 года на p.521 ссылается на **p.185**. Это **два разных редакционно-исторических свидетельства**, а не исправление p.84–85 на p.87 или p.185.
2. Экземпляр/вариант 1684 года остаётся не сверен по изображению и контексту; атрибуция авторства маргиналий самому Чарноку **не устанавливается** печатным текстом 1699 года.
3. Эта визуальная проверка не является `ED-06` независимой филологической рецензией 12 переводов, проверкой прав на русский текст или разрешением публикации. **DRAFT / RESEARCH_ONLY / PUBLICATION_HOLD** сохраняются.
4. Старый custody snapshot 17/17 на SHA `7adf6d1c...` остаётся достоверным **для своих неизменённых байтов**; новое чтение оформлено отдельным supplemental witness и не может задним числом менять содержание или хэши старого архива.

**Вердикт:** `ED02_N520_PRINTED_P521 = VERIFIED_BY_IMAGE`; `ED02_N520_LINGENDES_P185 = VERIFIED_BY_IMAGE`; `ED02_OTHER_EDITION_VARIANTS = NOT_COLLATION_COMPLETE`; `ED06 / RIGHTS / PUBLICATION = HOLD`. Не писать «весь ED-02 закрыт», пока остальные границы не приняты.
