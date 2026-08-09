# Заметка о слиянии параллельных фундаментов: 1 Кор. 11

**Дата:** 9 августа 2026 г.
**Статус:** `MERGED / CANONICAL-ENTRYPOINT = 00_README_FOUNDATION_OPEN_2026-08-09.md`

---

## 1. Две параллельные закладки

В рамках одного и того же задания два агента независимо открыли фундамент серии по 1 Кор. 11 в одной и той же ветке `arena/019fe62b-research`:

- **Агент А** (параллельный) создал папку `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/` с 6 файлами (README foundation, source acquisition plan, claim ledger template, product site style contract, source cards/locator registry, anti-duplication guide).
- **Агент Б** (текущий проход) создал папку `1_КОРИНФЯНАМ_11/` с 5 файлами (README, Greek dossier 01, master source ledger 15, book acquisition queue 16, foundation status 00A).

Оба фундамента методологически совместимы:
- TMS/confessional, inerrancy, historico-grammatical method, canonical supremacy;
- консервативный центр тяжести, либералы только как история толкования/стилмэн;
- сильный steelman, а не карикатура оппонента;
- греческий приоритет, уровни уверенности A/B/C/D/X или A/B/C/X по аналогии с Быт. 6;
- без пушей продуктового сайта, research-only на данной стадии;
- серийный уровень как Быт. 6, а не «одна короткая статья про платки».

## 2. Решение по канонической папке

Согласно anti-duplication файлу Агента А (`05_BRANCH_STATE_AND_PARALLEL_AGENT_ANTI_DUPLICATION_2026-08-09.md`), в котором явно сказано «не создавать вторую папку с другим именем» и указан канонический вход:

```text
1КОРИНФЯНАМ_11_ПОКРЫВАЛО/00_README_FOUNDATION_OPEN_2026-08-09.md
```

принимаем его папку как каноническую. Содержимое Агента Б влито в эту папку с суффиксами `_SUPPLEMENT` и под номерами, соответствующими схеме файлов Агента А.

## 3. Слияние содержимого

| Файл Агента Б | Перенос в каноническую папку | Примечание |
|---|---|---|
| `00_1COR11_RESEARCH_README.md` | не копируется как отдельный README; его архитектура 18 досье и доп. методологические замечания интегрируются логически, но не дублируют файл 00 | его содержание покрыто и расширено в 00-файле Агента А |
| `00A_FOUNDATION_STATUS_2026-08-09.md` | → `00A_PARALLEL_FOUNDATION_MERGE_NOTE_2026-08-09.md` (этот файл) | переименован и переписан как заметка о слиянии |
| `01_1COR11_GREEK_TEXT_AND_VARIANTS_DOSSIER.md` | → `06_GREEK_TEXT_AND_APPARATUS_1COR11_2_16.md` (соответствует плану файла 06 у Агента А) | полный стих-за-стихом греческий разбор NA28/SBLGNT, интегрирован с DEEP-PASS-XIX-C |
| `15_1COR11_MASTER_SOURCE_LEDGER.md` | → `04B_MASTER_SOURCE_LEDGER_SUPPLEMENT_2026-08-09.md` | расширенный реестр источников (130+ записей с evidence-классами) дополняет source cards Агента А |
| `16_1COR11_BOOK_ACQUISITION_QUEUE.md` | → `01B_BOOK_ACQUISITION_PRIORITY_QUEUE_SUPPLEMENT_2026-08-09.md` | P0/P1/P2/P3 очередь и порядок чтения шестью слоями дополняет его source acquisition plan |

Папка `1_КОРИНФЯНАМ_11/` удалена после переноса, чтобы не было двух параллельных entrypoint.

Рабочая папка `SOURCE_LIBRARY/processed/1COR11_PRIMARY/` сохранена как есть (пустая структура под первоисточники).

## 4. Дополнительно интегрированные находки Агента Б

1. **Найден и интегрирован существующий прямой греческий анализ** из `ТРУДНЫЕ ТЕКСТЫ/GREEK_NT_DIRECT_TEXT_ANALYSIS_1COR11_1PETER3_4_2PETER2_JUDE.md` (DEEP-PASS-XIX-C, 23 июля 2026); его минимальные выводы A/B/C/X перенесены в досье 06.
2. **Изучена редакционная хартия сайта** (`docs/ARTICLE-STANDARD-CHARTER.md` в продуктовом репозитории): SBL + Chicago/Turabian notes-bibliography, первоисточник выше пересказа, милость к оппоненту, девятиуровневая шкала доказательности, русский читательский слог, догмат vs адиафора, явная атрибуция конфессиональной позиции. Это соответствует site contract Агента А.
3. **Расширен реестр источников** добавлением Preston Massey, David W. J. Gill, Alan Padgett, Murphy-O'Connor, Gary Derickson, Cynthia Westfall, Lucy Peppiatt, David deSilva, и рядом дополнительных работ по сравнению с первоначальным списком.
4. **Push policy уточнена**: владелец разрешил пуш в эту research-ветку; начальный `PUSH_HOLD` снят; коммит с фундаментом запушен на `origin/arena/019fe62b-research`.

## 5. Канонический список файлов на текущий момент

```text
1КОРИНФЯНАМ_11_ПОКРЫВАЛО/
  00_README_FOUNDATION_OPEN_2026-08-09.md             — основной entrypoint
  00A_PARALLEL_FOUNDATION_MERGE_NOTE_2026-08-09.md     — эта заметка
  01_SOURCE_ACQUISITION_PLAN.md                        — базовый план приобретения
  01B_BOOK_ACQUISITION_PRIORITY_QUEUE_SUPPLEMENT_...   — детальная P0/P1 очередь и порядок чтения слоями
  02_CLAIM_LEDGER_TEMPLATE_AND_POSITIONS.md            — каркас тезисов
  03_PRODUCT_SITE_STYLE_AND_SERIES_CONTRACT_...        — продуктовый стандарт
  04_SOURCE_CARDS_AND_LOCATOR_REGISTRY_...             — карточки отдельных ключевых источников
  04B_MASTER_SOURCE_LEDGER_SUPPLEMENT_...              — общий реестр 130+ источников
  05_BRANCH_STATE_AND_PARALLEL_AGENT_ANTI_DUPLICATION  — статус и правила для следующих агентов
  06_GREEK_TEXT_AND_APPARATUS_1COR11_2_16.md           — первый контентный досье (греческий текст, разбор стих за стихом, минимальные выводы)
```

## 6. Следующие файлы (по плану Агента А, не создаются сразу)

Нумерация дана по `05_BRANCH_STATE_AND_PARALLEL_AGENT_ANTI_DUPLICATION`:

```text
07_CORINTH_ROMAN_COLONY_CONTEXT.md
08_KEPHALE_AUTHORITY_SOURCE_CHRISTOLOGY.md
09_COVERING_MEN_WOMEN_HAIR_VEIL.md
10_EXOUSIA_AND_ANGELS_VERSE_10.md
11_NATURE_HAIR_PERIBOLAIOS_AND_MARTIN_GOODACRE.md
12_PATRISTIC_HISTORY_OF_INTERPRETATION.md
13_COMMENTATORS_MATRIX.md
14_MODERN_APPLICATION_HERMENEUTICS.md
15_RUSSIAN_ORTHODOX_AND_EVANGELICAL_INTERPRETATION.md
```

Дополнительно могут понадобиться в будущем (номера продолжать с 16):

- древние версии текста (Vg, Peshitta, Old Latin, CS) — при необходимости внутри 06;
- визуальные источники (монеты, статуи, фрески, коропластика Corinth);
- русский баптистский архив по покрывалу (можно в 15 или отдельно).

## 6.5. Третий параллельный корпус (Агент В)

Третий агент параллельно построил рабочий корпус в папке

```text
СЕРИЯ 1 КОРИНФЯНАМ 11/
```

с собственной нумерацией 00–07 (evidence levels, master index, scope/source weight plan, historical context draft, Greek analysis v2, commentator landscape, question matrix, adversarial readings, patristic primary sources, application debate) и, что особенно ценно, уже физически загрузил первоисточники в подпапку `ИСТОЧНИКИ/`:

- полный текст Климента Александрийского *Paedagogus* (ANF 2);
- полный текст Тертуллиана *On Prayer* (ANF 3);
- полный текст Тертуллиана *On the Veiling of Virgins* (ANF 4);
- свёрстанный файл цитат Златоуста (Беседа 26);
- сводка цитат Тертуллиана/Климента;
- цитаты Кальвина, Гилла, Ходжа;
- цитаты Феофилакта Болгарского и Феофана Затворника (русская патристика);
- служебные скрипты извлечения.

Эти источники уже скопированы в общую библиотеку `SOURCE_LIBRARY/processed/1COR11_PRIMARY/patristics/` и доступны для цитирования с должной сверкой. Досье 01–07 в папке `СЕРИЯ 1 КОРИНФЯНАМ 11/` остаются как параллельная рабочая поверхность и используются как сырьё при построении канонических досье 07–15 в этой папке.

## 7. Не дублировать

Следующим агентам запрещается:

1. Создавать новую папку под серию (другое имя, в корне или в подпапках).
2. Переписывать файл 00 с нуля — вносить правки и дополнения в существующий.
3. Начинать публикационные файлы для сайта без отдельного продуктового лейна в gb-is-my-strength репозитории.
4. Заявлять выводы по спорным узлам до построения соответствующих досье.
5. Сливать русский баптистский контекст поверх греческого разбора; сначала слой 1–3 по файлу 01B, потом патристика, потом русская практика.

---

Итог: серия открыта, фундаменты слиты в единую папку, греческое досье 06 готово, очередь источников и книг оформлена. Дальше — глубокое копание по досье.
