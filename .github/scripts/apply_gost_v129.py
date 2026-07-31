from pathlib import Path
import csv
import re

ROOT = Path('БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED')
HISTORY = ROOT / 'groups/02_HISTORY_NARRATIVE.md'
PERIODICALS = ROOT / 'groups/03_PERIODICAL_CORPUS.md'
LEDGERS = ROOT / 'groups/06_DATA_AND_PROOF_LEDGERS.md'
README = ROOT / 'README.md'

for path in (HISTORY, PERIODICALS, LEDGERS, README):
    if not path.exists():
        raise SystemExit(f'missing required grouped file: {path}')


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding='utf-8')
    if marker in text:
        print(f'already present: {marker}')
        return
    path.write_text(text.rstrip() + '\n\n' + block.strip() + '\n', encoding='utf-8')
    print(f'appended {marker}')


# Critical person-authority correction.
text = HISTORY.read_text(encoding='utf-8')
old = '| **Р. А. Фетлер** | 1861–1933 (standard reference; *needs primary card*) | 365 | Latvian-born evangelist; Far-East/emigration periodicals |'
new = '''| **В. А. Фетлер (Вильгельм / William)** | 1883–1957 (RSL authority records) | surname pool not yet disambiguated | St Petersburg/Riga evangelist, author, compiler and publishing organizer; `Вера`, `Гость`, legal and devotional booklet network |
| **Р. А. Фетлер (Роберт / Robert)** | 1892–1941 (family archive strong; exact LVA file 1987/1/13296 located, contents pending) | surname pool not yet disambiguated | Omsk/Vladivostok pastor and editor-publisher of `Благовестник`; distinct younger brother of William |'''
if old in text:
    if text.count(old) != 1:
        raise SystemExit('unsafe old Fetler row count')
    HISTORY.write_text(text.replace(old, new), encoding='utf-8')
    print('replaced conflated Fetler authority row')
elif '## v129 — `Гость` и Фетлеры: консолидированный H–L delta' not in text:
    raise SystemExit('expected old Fetler row missing')

append_once(HISTORY, '## v129 — `Гость` и Фетлеры: консолидированный H–L delta', r'''
## v129 — `Гость` и Фетлеры: консолидированный H–L delta

**Дата интеграции:** 2026-07-31  
**Метод:** один no-loss блок вместо последовательного добавления марафонов H–L.  
**Gate:** metadata, text layer и reproduction не повышаются до `quote_ready` без полного оригинала, OCR и визуальной сверки.

### Authority-коррекция

- **Вильгельм Андреевич Фетлер (1883–1957):** Петербург—Рига; `Вера`, `Гость`; автор, составитель и издательский организатор. РГБ закрепляет полную форму имени и годы жизни.
- **Роберт Андреевич Фетлер (1892–1941):** Омск—Владивосток; редактор-издатель `Благовестника`. Точный первичный маршрут — Latvijas Valsts arhīvs, фонд 1987, опись 1 (Rīga), дело 13296; само дело ещё не просмотрено.
- Число **365** означает только `FETLER SURNAME HITS — PERSON DISAMBIGUATION REQUIRED` и не присваивается одному из братьев.

### Юридическая и организационная граница

- Уставное имя сохраняло евангельских христиан и баптистов; после выхода баптистов в 1925 году употреблялось имя без них. Статус: `PARTIALLY RESOLVED — STATUTORY NAME VS POST-SPLIT USAGE`.
- Союз и Общество взаимной помощи оставались самостоятельными организациями; координация 1937 года не доказывает слияния или общего издателя.
- Официальный орган Союза в апреле 1939 года исправляет формулу «группа Фетлера» на легализованное Общество взаимной помощи и называет `ks. L. Jesakow` руководителем.
- Jesakow: `PROBABLE LEONID/LEON — IDENTITY NOT CLOSED`.
- `(Husaruk)`: первичный след ассоциации; редакторская/руководящая роль `HOLD`.
- Неназванное общество из предупреждения 1939 года не отождествляется с Обществом взаимной помощи без прямого документа.

### Роберт Фетлер и `Благовестник`

В публичном семейно-архивном корпусе воспроизведена обложка №1, март 1919, Омск; читается адрес Сенная, 10, а подпись называет Р. А. Фетлера редактором-издателем. Статус: `FACSIMILE REPRODUCTION VISUALLY VERIFIED — ORIGINAL ISSUE FILE NOT HELD`.

Точные маршруты: Wardin AR 915 Box 9 Folders 9.5–9.6; GAPK, май 1921 №5; приложение 8 книги В. А. Прохорова. Сохраняется конфликт `1919–1921` в библиографии против №5 конца 1922 года в повествовании.

### Новый P0-корпус `Гостя`

Музей Вильяма Фетлера / Latvian Biblical Centre сообщает о физической коллекции `Гостя` 1923–1930. Доказан хранитель и диапазон; не доказаны полнота, непрерывность, дубли, приложения и права на оцифровку. Следующий шаг — issue-level inventory и контрольные фото обложек/колофонов.

### Запреты

Не переносить издателя одного журнала на другой; не присваивать 365 одному Фетлеру; не называть музейный диапазон полным комплектом; не назначать Гусарука редактором; не исправлять печатную статистику молча.
''')

append_once(PERIODICALS, '## v129 — `Гость`: контрольный корпус, издательская сеть и новые holdings', r'''
## v129 — `Гость`: контрольный корпус, издательская сеть и новые holdings

### Контрольный первичный корпус

JBC хранит официальный орган Союза `Ewangeliczny Chrześcijanin` за 1935–1939 годы. Он используется для юридических имён, решений, адресов и руководства, но не является выпуском или продолжением `Гостя`.

- group: https://jbc.bj.uj.edu.pl/dlibra/publication/678242/ewangeliczny-chrzescijanin
- March 1937 PDF: https://jbc.bj.uj.edu.pl/Content/680472/0001_NDIGCZAS039838_110491185.pdf
- April 1939 PDF: https://jbc.bj.uj.edu.pl/Content/680480/0001_NDIGCZAS039838_110491233.pdf

### Печатная статистика 1939 года

| Показатель | Союз | Общество | Сумма | Напечатано | Статус |
|---|---:|---:|---:|---:|---|
| Члены с детьми | 16 007 | 11 373 | 27 380 | 27 383 | arithmetic conflict |
| Пресвитеры и диаконы | 116 | 40 | 156 | 156 | match |
| Евангелисты и работники | 187 | 213 | 400 | 401 | arithmetic conflict |

Напечатанное и вычисленное хранить раздельно.

### Передача источника

`Kirchenblatt für die reformierte Schweiz` 21–22/1935 → `Zwiastun Ewangeliczny` 51–52/1935 и 1/1936 → `Ewangeliczny Chrześcijanin` 1/1937 → корректирующая статья 1/1939. Это граф передачи, а не независимые свидетельства. Контроль: Eduard Kupsch, `Die Freikirchen in Polen`, 1938, pp.172–182.

### Издательская сеть `Гостя`

РГБ фиксирует брошюры редакции или конторы `Гостя`: `Скрытое сокровище` (https://search.rsl.ru/ru/record/01004213601) и R. A. Torrey, `Потрясающий вопрос` (https://search.rsl.ru/ru/record/01004214188). Модель различает periodical, editorial office, imprint, booklet series, editor, translator, printer и address.

### Holdings

- LBC museum: физическая коллекция `Гостя` 1923–1930; completeness unknown; P0 inventory. https://bible.lv/en/fetler-family-heirlooms/
- Public family compilation: https://drive.google.com/file/d/1CUpNUJKayB3witUEm8bhzVP9VPAC1vv-/view — modern compilation, not original issue.
- AAN 1446 p.70: `Siejatiel Istiny` или `Gost` среди источников; конкретный выпуск не установлен.
- AAN I1082: устав и переписка 1922–1931; P0, без сканов.
- KUL 1927 statute: https://dlibra.kul.pl/publication/1714/edition/1866/ — 8 pages, full stable file/page review pending.
''')

append_once(LEDGERS, '## v129 — `Гость` / Фетлеры: consolidated proof ledger', r'''
## v129 — `Гость` / Фетлеры: consolidated proof ledger

| ID | Тезис / объект | Финальный статус | Разрешено | Заблокировано |
|---|---|---|---|---|
| GOST-129-001 | statutory name / post-split usage | partially_resolved | различать wording и usage | AAN I1082 pending |
| GOST-129-002 | Union / Mutual Aid Society | primary_boundary_confirmed | cooperation with autonomy | общий издатель |
| GOST-129-003 | Fetler group / L. Jesakow | primary_text_visual_pending | организация и роль с атрибуцией | facsimile-exact wording |
| GOST-129-004 | unnamed rival society | counterpart_unknown | сообщение Союза | назвать Mutual Aid Society |
| GOST-129-005 | Husaruk parenthesis | semantic_role_hold | association trace | editor/head role |
| GOST-129-006 | 27 380 / 27 383 | arithmetic_conflict | хранить оба | silent correction |
| GOST-129-007 | 400 / 401 | arithmetic_conflict | хранить оба | silent correction |
| GOST-129-008 | William / Robert conflation | critical_correction_applied | separate persons | restore old row |
| GOST-129-009 | 365 hits | surname_pool | contextual recount | person attribution |
| GOST-129-010 | Blagovestnik no.1/1919 reproduction | facsimile_reproduction_verified | cite provenance | original acquired |
| GOST-129-011 | Robert 1892–1941 | family_archive_strong_primary_file_pending | use with qualifier | primary-card verified |
| GOST-129-012 | LBC `Гость` 1923–1930 | holding_confirmed_completeness_unknown | request inventory | call complete run |
| GOST-129-013 | AAN 1446 p.70 | source_family_confirmed | source-family statement | specific issue/table |
| GOST-129-014 | family PDF | reference_verified_no_repo_binary | link, SHA and provenance | duplicate upload |

### Superseded

1. `Р. А. Фетлер, 1861–1933, 365` → deprecated conflation.
2. `15 February should be March 1905` → rejected; February sequence valid.
3. `1937 cooperation = merger` → rejected.
4. `Husaruk = editor/head` → unsupported HOLD.
5. Printed totals may be silently normalized → rejected.

### P0/P1 request queue — not sent

AAN I1082; AAN 1446 p.70; APL 35/413/0/9/644; LVA 1987/1/13296; Wardin AR915 Box9/9.5–9.6; LBC issue inventory; GAPK 1921 №5; Prokhorov Appendix8; Kupsch pp.172–182; GCAH Jesakow. Every request remains `READY TO REQUEST — NOT SENT`.

### Stable links

- https://czasopisma.ipn.gov.pl/index.php/pis/article/download/2522/2386/3538
- https://dlibra.kul.pl/publication/1714/edition/1866/
- https://jbc.bj.uj.edu.pl/dlibra/publication/678242/ewangeliczny-chrzescijanin
- https://search.rsl.ru/ru/record/01000371468
- https://search.rsl.ru/ru/record/01006754154
- https://www.prlib.ru/history/619208
- https://bible.lv/en/fetler-family-heirlooms/
- https://drive.google.com/file/d/1CUpNUJKayB3witUEm8bhzVP9VPAC1vv-/view
''')

append_once(README, '## v129 update — `Гость` / Фетлеры, no-loss H–L integration', r'''
## v129 update — `Гость` / Фетлеры, no-loss H–L integration

- Исправлена склейка Вильгельма и Роберта Фетлеров; `365` перенесено в surname-disambiguation pool.
- Интегрированы юридическая граница Союза/Общества, JBC-корпус, статистические конфликты, HOLD по Husaruk и authority-route Jesakow.
- Зарегистрированы LVA 1987/1/13296, Wardin AR915 Box9/9.5–9.6, `Благовестник` и музейная коллекция `Гостя` 1923–1930.
- Новых scattered MD и тяжёлых бинарников не создано; `quote_ready` не повышался.
''')


def norm(value: str) -> str:
    return re.sub(r'[^a-z0-9а-я]+', '_', (value or '').strip().lower()).strip('_')


def pick(fields, aliases):
    mapping = {norm(field): field for field in fields}
    for alias in aliases:
        if norm(alias) in mapping:
            return mapping[norm(alias)]
    return None


def append_csv(path: Path, records) -> None:
    if not path.exists():
        print(f'optional CSV absent: {path}')
        return
    source = path.read_text(encoding='utf-8-sig')
    reader = csv.DictReader(source.splitlines())
    fields = reader.fieldnames or []
    rows = list(reader)
    searchable = source.lower()
    aliases = {
        'id': ['id', 'record_id', 'source_id', 'proof_id', 'item_id'],
        'series': ['series', 'corpus', 'periodical'],
        'year': ['year', 'date', 'period'],
        'issue': ['issue', 'issues', 'number', 'no'],
        'title': ['title', 'item', 'source_title', 'claim'],
        'url': ['url', 'source_url', 'link', 'evidence_url'],
        'status': ['status', 'proof_status', 'current_status'],
        'evidence': ['evidence', 'evidence_class', 'source_type', 'confidence'],
        'notes': ['notes', 'note', 'caution', 'use_caution', 'comment'],
        'next': ['next_action', 'next_step', 'required_output', 'action'],
        'priority': ['priority'],
    }
    added = 0
    for record in records:
        key = record['id'].lower()
        if key in searchable:
            continue
        row = {field: '' for field in fields}
        for key_name, alias_list in aliases.items():
            field = pick(fields, alias_list)
            if field and key_name in record:
                row[field] = record[key_name]
        if not any(row.values()):
            print(f'unknown CSV schema; skipped: {path}')
            return
        rows.append(row)
        searchable += '\n' + ' '.join(row.values()).lower()
        added += 1
    if added:
        with path.open('w', encoding='utf-8-sig', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        print(f'added {added} rows to {path}')


csvs = {path.name: path for path in ROOT.rglob('*.csv')}
append_csv(csvs.get('SOURCE_ANCHORS.csv', Path('/missing')), [
    {'id': 'GOST-129-SRC-JBC1939', 'series': 'Ewangeliczny Chrześcijanin', 'year': '1939', 'issue': '1', 'title': 'organization/statistics control', 'url': 'https://jbc.bj.uj.edu.pl/dlibra/publication/718058/edition/680480', 'status': 'primary_text_visual_pending', 'evidence': 'A', 'notes': 'not Gost'},
    {'id': 'GOST-129-SRC-LBC', 'series': 'Гость', 'year': '1923-1930', 'title': 'LBC museum holding', 'url': 'https://bible.lv/en/fetler-family-heirlooms/', 'status': 'holding_completeness_unknown', 'evidence': 'A-metadata', 'notes': 'P0 inventory'},
    {'id': 'GOST-129-SRC-FAMILY', 'series': 'Fetler family', 'year': '2026', 'title': 'FETLER BROTHERS compilation', 'url': 'https://drive.google.com/file/d/1CUpNUJKayB3witUEm8bhzVP9VPAC1vv-/view', 'status': 'reference_verified', 'evidence': 'family archive', 'notes': 'no repo binary'},
])
append_csv(csvs.get('PROOF_STATUS_LEDGER.csv', Path('/missing')), [
    {'id': 'GOST-129-008', 'series': 'Authority', 'title': 'William/Robert split', 'status': 'critical_correction_applied', 'evidence': 'RSL/archive/family', 'notes': '365 surname pool'},
    {'id': 'GOST-129-010', 'series': 'Благовестник', 'year': '1919', 'issue': '1', 'title': 'Omsk cover reproduction', 'status': 'facsimile_reproduction_verified', 'evidence': 'reproduced primary image', 'notes': 'original not held'},
    {'id': 'GOST-129-012', 'series': 'Гость', 'year': '1923-1930', 'title': 'LBC holding', 'status': 'holding_completeness_unknown', 'evidence': 'museum statement', 'notes': 'inventory required'},
])
append_csv(csvs.get('NEXT_MICROBATCH.csv', Path('/missing')), [
    {'id': 'GOST-129-TASK-LBC', 'series': 'Гость', 'year': '1923-1930', 'title': 'Museum issue inventory', 'status': 'ready_not_sent', 'priority': 'P0', 'next': 'issues/gaps/covers/colophons/rights'},
    {'id': 'GOST-129-TASK-AAN-I1082', 'series': 'AAN', 'year': '1922-1931', 'title': 'Review I1082', 'status': 'ready_not_sent', 'priority': 'P0', 'next': 'statutes/decisions/names/seals'},
    {'id': 'GOST-129-TASK-LVA', 'series': 'Robert Fetler', 'year': '1941', 'title': 'Request LVA 1987/1/13296', 'status': 'ready_not_sent', 'priority': 'P0', 'next': 'biography/deportation/death'},
    {'id': 'GOST-129-TASK-WARDIN', 'series': 'Благовестник', 'year': '1919-1920', 'title': 'Wardin Box9 folders9.5-9.6', 'status': 'ready_not_sent', 'priority': 'P0', 'next': 'inventory/scans'},
])

print('Gost/Fetler v129 integration prepared successfully.')
