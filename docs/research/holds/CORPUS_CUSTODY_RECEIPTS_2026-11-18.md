# Квитанции хранения двух корпусов (2026-11-18)

**Роль:** `DERIVED_READ_ONLY_NOT_AUTHORITY`. Квитанция про **носитель**, а не про права: она
отвечает на вопрос «где лежат байты и сколько их», и не отвечает на вопрос «можно ли это
публиковать».

**Зачем появилась.** Оба корпуса собираются в CI и живут в артефактах с retention 7–30 дней.
В репозитории было записано, что корпуса существуют и что суммы совпали, но не было записано,
где они лежат. Из-за этого первый выпуск `ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md` читался как
«5,7 ГБ под угрозой», хотя для двух семей из трёх байты давно на Drive. Эта квитанция закрывает
именно бухгалтерскую дырку, а не риск.

**Метод:** `list_files` по ID папки, `get_file` по объекту, `read_file_text` по текстовому
контрольному файлу. Только чтение: ни один объект не скачивался, не переименовывался и не
изменялся. Машинная версия — `data/corpus-custody-receipts-2026-11-18.json`.

---

## 1. COMMONS STRICT 40 — корпус 40 PDF по русской литературе

Заявлено в репозитории (`SOURCE_LIBRARY/COMMONS_RUSSIAN_LITERATURE_40PLUS_PDF_PASS_2026-07-30.md`):
40 действительных PDF, 610 183 443 байта, 12 434 страницы, 40/40 SHA-256 совпали, лицензии
39 Public Domain + 1 CC BY-SA 4.0.

На Drive — папка `01 — COMMONS STRICT 40` (`1DSfzT3YJC19iI0YG9IjfOXybVilgnQFJ`), девять
ZIP-шардов, у каждого серверный `sha256Checksum`:

| Шард | Drive ID | Байт | SHA-256 |
|---|---|---:|---|
| `01 — PDF 01-10 — PART A.zip` | `1JcpOMbKwNPWl0KaXQldKP74NgopPwYsJ` | 93 419 267 | `36e94ab7…f084d5` |
| `01 — PDF 01-10 — PART B.zip` | `13k_0dAsEktbR_wB_DjHqapgQX4svc7dd` | 35 560 492 | `88a6cc17…66c0a8c` |
| `02 — PDF 11-20 — PART A.zip` | `1VKlMMB2bMTFqkplVqx4k1WWUwmrEyD7v` | 90 799 683 | `aca6903a…05654454` |
| `02 — PDF 11-20 — PART B.zip` | `1NyDYYVSuPxk-5jjvuPb59SYLK5qPqSdG` | 22 299 138 | `5ff95785…9c55b9a2` |
| `03 — PDF 21-30 — PART A.zip` | `1ybgXXoI2Txfwk37Hl7jP2SfIkp8DwJA4` | 89 990 950 | `0d2c417f…2483b4cf` |
| `03 — PDF 21-30 — PART B.zip` | `16YwcXyvR0iGfUpq4PSSDeaN9l5UWVaBZ` | 62 752 353 | `dc4c148d…31b4244c` |
| `04 — PDF 31-40 — PART A.zip` | `1ErA3Xo8IGfWr42K-rOcGEOlUZwfaavoL` | 84 277 081 | `589049c2…f309e99ebb` |
| `04 — PDF 31-40 — PART B.zip` | `1qnTCG2WCTQXqogN5QYzula2rn4h3rl81` | 87 106 112 | `f026b53c…a12f43d7` |
| `04 — PDF 31-40 — PART C.zip` | `1s45tVKvZMKFJyDzY_5brSm08AfFSWWG_` | 43 987 425 | `565f7d24…2132fc5` |
| **Итого** | 9 объектов | **610 192 501** | |

Разница с заявленными 610 183 443 байтами — **9 058 байт** на весь корпус. Это оверхед zip
(заголовки, имена, структура), а не расхождение объектов: сумма девяти шардов не может быть
меньше суммы сорока PDF внутри них.

Контрольные файлы рядом:

- `commons_strict_sha256_verification.txt` (`1PvXKzW6Oq1U7qP-j0FLIXx_gv19ogez9`, 3 110 Б) —
  прочитан, содержит 40 строк вида `<имя>.pdf: OK`, по одной на каждый PDF;
- `COMMONS STRICT 40 — ORIGINAL MANIFEST.zip` (`1qdpO--2fZim1Ui4suCm0hoxppCEhl0kM`, 27 136 Б);
- `COMMONS STRICT 40 — PROCESSED CONTROL PACKAGE.zip` (`1RIA4gU8AkkwQ-JR72Ek5pCJr-5VBnnQC`, 826 936 Б).

## 2. SECOND EDITORIAL 40 — второй редакционный корпус 40 открытых PDF

Заявлено в репозитории (`SOURCE_LIBRARY/SECOND_EDITORIAL_40_PDF_PASS_2026-07-30.md`): независимый
корпус из 40 PDF по шести осям (периодика, авангард, воспоминания, реформатские и пуританские
первоисточники, баптистские документы, Codex Sinaiticus и 1 Енох).

На Drive — папка `02 — SECOND EDITORIAL 40` (`1qba3eUdOo0x4Sp2T1viB_MMdWQf80UtZ`), четыре шарда
по десять PDF:

| Шард | Drive ID | Объектов |
|---|---|---:|
| `01-10` | `1cLg23XvpSxTuJXG14pwsxHACmbbqrah4` | 10 |
| `11-20` | `1fDuFrAOklfmazeC1wvkuIFN_HiuojybM` | 10 |
| `21-30` | `14QR3UlghkWlXABp52feO1Dkpzy_2NYIu` | 10 |
| `31-40` | `1DRavSKBH34HABvRLrovlampMZWTwDwqW` | 10 |
| **Итого** | | **40 PDF** |

У каждого PDF Drive отдаёт серверный `sha256Checksum`. Рядом —
`SECOND EDITORIAL 40 — MANIFEST RIGHTS SHA256.zip` (`1bHbwp7AoS2F645_BZhNVNTjWfKYoHm4g`,
25 419 Б, sha256 `f363ec567be8a40cd5828d251e288572270c4368f5940602c0b29548b4a7e547`): манифест
прав и сумм, который проходил вместе с корпусом.

Пофайловые суммы прочитаны через коннектор, но **в репозиторий не перенесены**. Причина
названа прямо: перенос сорока значений вручную создаёт риск опечатки, который в репозитории
нечем проверить, — а неверная сумма в квитанции хуже отсутствующей. Проверять нужно чтением,
а не копированием.

## 3. APPROVED CORE POET PORTRAITS 45 и APPROVED EPHEMERA 63

Те же два класса объектов, что и выше, но наборы одобренные, а не полные. Оба живут в
артефактах с retention 7–30 дней и оба уже имеют папки на Drive.

**Портреты.** Папка `01 — APPROVED CORE POET PORTRAITS 45` (`1BcHMZEPJtTDbE9zXZnRLtjCBtvGG3S02`):

| Объект | Drive ID | Байт | SHA-256 |
|---|---|---:|---|
| `01 — ESENIN BUNIN SEVERYANIN.zip` | `1p74lMCCL-4jBUoJAkTIMwlNc-Z44o29p` | 5 693 954 | `bbb49e26…a43effeb` |
| `02 — BALMONT TYUTCHEV MAYKOV.zip` | `1npjCwiSvNAGv_uNB7gYmn4Q2TTj-dvRb` | 4 297 804 | `b6e8ffb4…0703609` |
| `03 — BRYUSOV BLOK FET.zip` | `1TUIiE80Kuv0VIzeTGsTYwSYk8hUHfv4b` | 5 615 172 | `ee82a6eb…cf2074c` |
| **Итого** | 3 шарда | **15 606 930** | |

Рядом `PORTRAITS 45 — MANIFEST RIGHTS SHA256.zip` (`1wqrGOW86x_cHPW14Xe_6x9yvaYxJS8sD`, 23 433 Б).
Важно: в самом allowlist-файле статус записан как `CURRENT LICENSE RECHECK REQUIRED` — квитанция
про байты этого не отменяет.

**Эфемериды.** Папка `02 — APPROVED EPHEMERA 63` (`1vfSja20qrEwQNuYDS1dI_WFZYxD18-_C`):

| Объект | Drive ID | Байт | SHA-256 |
|---|---|---:|---|
| `01 — ORIGINALS 01-16.zip` | `14DsRdBd3zvEvR9JiF_2yAOL-agZfE7GU` | 3 942 853 | `12d846f9…8ab30341` |
| `02 — ORIGINALS 17-32.zip` | `1yi5Vzi7DbTFVhJ5IaIAmTsXjDvFdm72C` | 30 333 112 | `b3e71942…e2093807` |
| `03 — ORIGINALS 33-48.zip` | `1fVWuckOkgxHRTmdxyLqvfSJR35mjkRsi` | 60 674 985 | `7c2ca45b…b75ec8c29d` |
| `04 — ORIGINALS 49-63.zip` | `1-JY6zCDgDp0I38oqXLZaQCbEfL20wef-` | 11 570 623 | `b216b40d…94f8234c` |
| `90 — REVIEW CONTACT SHEETS AND CANDIDATES.zip` | `13JOBCx_Pu5FfIPOshYYEOMPBkPCRQndl` | 26 686 822 | `2b311c37…415e27a27` |
| **Итого** | 5 объектов | **133 208 395** | |

Рядом `EPHEMERA 63 — MANIFEST RIGHTS SHA256.zip` (`1XVd-P7ttZrWnvmow0A0s2Bb3KVN-Srp3`, 27 553 Б).

**Честная оговорка по обоим наборам:** объёмы артефактов не сходятся с суммами шардов, и
расхождение не объяснено. Для портретов артефакт 63 239 012 Б на два прогона (≈31,6 МБ на
прогон) против 15,6 МБ на Drive — артефакт больше. Для эфемерид 213 327 748 Б на два прогона
против 133,2 МБ на Drive — тоже больше. Возможные причины (в артефакт попадают промежуточные
файлы, контрольные листы, несколько версий одного объекта) не проверялись. Поэтому здесь
записано только то, что подтверждено: **папки и суммы существуют**, а не «байты совпадают».

**Материал ревью** (`ephemeral-poet-portrait-review-v4` 316,2 МБ и
`ephemeral-ephemera-review-candidates` 282,5 МБ) отдельной квитанции не имеет и не должен:
на Drive лежит его итог — контрольные листы, `ephemera-candidates.csv` (1,2 МБ) и
`ephemera-candidates.json` (1,7 МБ), то есть то, по чему принималось решение. Скачанные
изображения кандидатов — расходный материал ревью, а не доказательство.

## 4. Чего эти квитанции не доказывают

- **Не доказывают права.** Оба корпуса собраны из открытых источников, но квитанция про байты.
  `RIGHTS_HOLD` и `PUBLICATION_HOLD` остаются как были.
- **Не доказывают содержимое.** Шарды не распаковывались, пофайловые суммы внутри шардов против
  списка «OK» не сверялись. Совпадение объёма и наличие контрольного файла — это не тождество.
- **Не покрывают третий корпус.** `official-core 59` сюда не входит и не может входить: на Drive
  у него только манифест 19 137 Б и документ статуса, а объекты на 123 МБ живут в артефакте,
  который истекает 2026-11-24. Это единственный настоящий риск из трёх, и он описан в
  `OFFICIAL_CORE_59_AND_LEDGER_GAPS_2026-11-18.md`.
- **Не вечны.** Значения сняты 2026-11-18. Перезапись объекта на Drive изменит сумму; квитанцию
  тогда пересобирают заново, а не «подправляют».

## 5. Воспроизводимость

```text
list_files(q="'1DSfzT3YJC19iI0YG9IjfOXybVilgnQFJ' in parents and trashed = false",
           fields="files(id,name,size,sha256Checksum)")
read_file_text(file_id="1PvXKzW6Oq1U7qP-j0FLIXx_gv19ogez9")
list_files(q="'1qba3eUdOo0x4Sp2T1viB_MMdWQf80UtZ' in parents and trashed = false", ...)
get_file(file_id="1bHbwp7AoS2F645_BZhNVNTjWfKYoHm4g", fields="sha256Checksum,size")
```

Сводка по артефактам, из которой эти семьи вышли, — `ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md` §5.
