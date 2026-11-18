#!/usr/bin/env python3
"""Отрисовка и проверка матрицы определения прав (2026-11-18).

Матрица перечисляет 22 объекта, которые в §4.7 инвентаря держат только
права/публикацию. Скрипт ничего не закрывает и не меняет `rightsState`:
он проверяет, что матрица не разошлась с реестрами, и перерисовывает
markdown из JSON.

    python3 scripts/render_rights_matrix.py           # перерисовать .md из .json
    python3 scripts/render_rights_matrix.py --check   # только проверить

Проверки (fail-closed):
  1. набор id в матрице совпадает с набором, который даёт тот же фильтр,
     что и `check_decision_only_holds()` в render_hold_inventory.py;
  2. для каждого id записанные rightsState и holds совпадают с реестром;
  3. категория входит в объявленный словарь, а счётчики summary сходятся;
  4. в записях нет полей, которые бы объявляли новое состояние прав
     (newRightsState / rightsState / closesHold и подобных);
  5. markdown на диске совпадает с перерисовкой.
"""

from __future__ import annotations

import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_hold_inventory as inventory  # noqa: E402

DATA = ROOT / "data" / "rights-determination-matrix-2026-11-18.json"
OUT = ROOT / "docs" / "research" / "holds" / "RIGHTS_DETERMINATION_MATRIX_2026-11-18.md"

FORBIDDEN_KEYS = {
    "rightsState",
    "newRightsState",
    "proposedRightsState",
    "closesHold",
    "closes",
    "holdClosed",
}


def expected_ids() -> set[str]:
    """Тот же фильтр, что и в §4.7 инвентаря."""
    nodes_by_file, _ = inventory.scan_json()
    ids = set()
    for _path, nodes in nodes_by_file.items():
        for node in nodes:
            holds = set(node["holds"])
            if not (
                holds
                and holds <= {"RIGHTS_HOLD", "PUBLICATION_HOLD"}
                and node["accessState"] == "FULL_OBJECT_VERIFIED"
                and node["locatorState"] == "EXACT_LOCATOR_VERIFIED"
            ):
                continue
            if node["rightsState"] in {"RIGHTS_UNKNOWN", "PERMISSION_REQUIRED"}:
                ids.add(node["id"] or "(без id)")
    return ids


def registry_index() -> dict[str, dict]:
    nodes_by_file, _ = inventory.scan_json()
    index = {}
    for path, nodes in nodes_by_file.items():
        for node in nodes:
            key = node["id"] or "(без id)"
            index.setdefault(key, []).append(
                {
                    "path": path,
                    "rightsState": node["rightsState"],
                    "holds": sorted(node["holds"]),
                }
            )
    return index


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def validate(matrix: dict) -> list[str]:
    problems: list[str] = []
    entries = matrix["entries"]
    ids = [e["id"] for e in entries]
    dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dupes:
        problems.append(f"повторяющиеся id: {dupes}")

    want = expected_ids()
    got = set(ids)
    if want != got:
        problems.append(
            "набор id разошёлся с фильтром §4.7: "
            f"лишние {sorted(got - want)}, недостающие {sorted(want - got)}"
        )

    index = registry_index()
    for entry in entries:
        known = index.get(entry["id"])
        if not known:
            problems.append(f"{entry['id']}: id отсутствует в реестрах")
            continue
        states = {item["rightsState"] for item in known}
        holds = {tuple(item["holds"]) for item in known}
        if entry["recordedRightsState"] not in states:
            problems.append(
                f"{entry['id']}: rightsState {entry['recordedRightsState']} "
                f"не совпадает с реестром {sorted(states)}"
            )
        if tuple(sorted(entry["recordedHolds"])) not in holds:
            problems.append(
                f"{entry['id']}: holds {sorted(entry['recordedHolds'])} "
                f"не совпадают с реестром {sorted(holds)}"
            )
        if entry["source"] not in {item["path"] for item in known}:
            problems.append(
                f"{entry['id']}: source {entry['source']} не тот файл, где лежит запись"
            )
        bad = FORBIDDEN_KEYS & set(entry)
        if bad:
            problems.append(f"{entry['id']}: поля {sorted(bad)} объявляют правовой эффект")

    categories = matrix["categories"]
    counts = collections.Counter(e["category"] for e in entries)
    unknown = set(counts) - set(categories)
    if unknown:
        problems.append(f"категории вне словаря: {sorted(unknown)}")
    declared = matrix["summary"]["byCategory"]
    if dict(counts) != declared:
        problems.append(f"счётчики категорий разошлись: факт {dict(counts)}, объявлено {declared}")
    if sum(declared.values()) != matrix["summary"]["total"]:
        problems.append("сумма категорий не равна total")
    if len(entries) != matrix["summary"]["total"]:
        problems.append("число записей не равно total")

    needs = sum(1 for e in entries if categories[e["category"]]["needsCorrespondence"])
    if needs != matrix["summary"]["needsCorrespondence"]:
        problems.append(
            f"needsCorrespondence: факт {needs}, объявлено {matrix['summary']['needsCorrespondence']}"
        )
    return problems


def render(matrix: dict) -> str:
    entries = matrix["entries"]
    categories = matrix["categories"]
    grouped = collections.OrderedDict()
    for entry in entries:
        grouped.setdefault(entry["category"], []).append(entry)

    lines: list[str] = []
    add = lines.append
    add("# Матрица определения прав: 22 объекта (2026-11-18)")
    add("")
    add("**Роль:** `PROPOSAL_NOT_AUTHORITY`, производный документ. Здесь **не снимается ни один HOLD**")
    add("и не меняется ни один `rightsState`: матрица раскладывает 22 объекта запроса по слоям, где")
    add("права действительно возникают, и по цене закрытия. Решение принимает владелец.")
    add("")
    add(f"**Что попало в матрицу:** {matrix['scope']}")
    add("")
    add("**Фильтр отбора:**")
    add("")
    add(f"`{matrix['selectionRule']}`")
    add("")
    add("Это тот же фильтр, что в `render_hold_inventory.py::check_decision_only_holds()`;")
    add("совпадение наборов проверяется скриптом `scripts/render_rights_matrix.py --check`.")
    add("")
    add("## 1. Почему «права неизвестны» — не одно и то же в 22 случаях")
    add("")
    add("Права возникают на четырёх разных слоях, и HOLD стоит на разных:")
    add("")
    add("| Слой | Что это |")
    add("|---|---|")
    for key, value in matrix["layers"].items():
        add(f"| `{key}` | {value} |")
    add("")
    add("Объект XVI–XVII вв. в общественном достоянии и **та же страница** с современным переводом — это")
    add("два разных правовых объекта. Пока слой не назван, «`RIGHTS_UNKNOWN`» читается как")
    add("неизвестность там, где на самом деле известна неполнота записи.")
    add("")
    add("## 2. Итог в цифрах")
    add("")
    summary = matrix["summary"]
    add(f"Всего объектов: **{summary['total']}**. Из них:")
    add("")
    add("| Категория | Объектов | Что требуется |")
    add("|---|---:|---|")
    for key, count in summary["byCategory"].items():
        need = "переписка" if categories[key]["needsCorrespondence"] else "решение владельца"
        if key == "REFUSED_BY_RECORDED_FINDING":
            need = "ничего"
        add(f"| `{key}` | {count} | {need} |")
    add("")
    add(f"- **{summary['ownerDecisionOnly']}** объектов не требуют переписки: им нужен записанный")
    add("  `rightsBasis` или решение о политике цитирования.")
    add(f"- **{summary['needsCorrespondence']}** требуют письма: три правообладателя современных")
    add("  текстов и распорядитель прав РБО (два объекта закрываются одним ответом).")
    add(f"- **{summary['resolvedWithoutWork']}** уже несёт записанный отказ и не должен попадать")
    add("  в очередь запросов.")
    add("")
    add("Практический вывод: очередь переписки — не 21 объект. Пять объектов закрываются")
    add("письмами по **четырём адресам** (два объекта РБО — одно письмо), остальные шестнадцать")
    add("ждут записей в карточках, которых до сих пор не было.")
    add("")
    add("## 3. Объекты по категориям")
    for key, items in grouped.items():
        meta = categories[key]
        add("")
        add(f"### `{key}` — {meta['title']} ({len(items)})")
        add("")
        add(meta["whatItMeans"])
        add("")
        add("| id | Что это | Доказательство в репозитории | Чего не хватает | Действие |")
        add("|---|---|---|---|---|")
        for entry in items:
            evidence = " ".join(entry["evidenceInRepo"])
            add(
                f"| `{entry['id']}` | {entry['what']} | {evidence} | {entry['gap']} | "
                f"{entry['action']} |"
            )
    add("")
    add("## 4. Проверка оцифровщика: почему у восьми узлов Pusey не появилось основания прав")
    add("")
    check = matrix["digitizerCheck"]
    add("Эта часть — единственная, где 2026-11-18 выполнялась внешняя проверка, и она **не** дала")
    add("основания снять HOLD. Наоборот, она объяснила, почему `RIGHTS_UNKNOWN` здесь честен.")
    add("")
    add(f"Репозиторий сканов: `{check['repository']}`. Метод: `{check['method']}`.")
    add("")
    observed = check["observed"]
    add("| Что проверялось | Результат |")
    add("|---|---|")
    add(f"| Поле `license` в GitHub API | `{observed['githubLicenseField']}` |")
    add(f"| Содержимое корня репозитория | {', '.join(observed['rootEntries'])} |")
    add(f"| Файл LICENSE | {'есть' if observed['licenseFilePresent'] else 'отсутствует'} |")
    add(f"| README | {'есть' if observed['readmePresent'] else 'отсутствует'} |")
    add("")
    statement = check["repoStatementOnFile"]
    add(f"В репозитории уже есть запись о лицензии OGL — `{statement['path']}`, ключ")
    add(f"`{statement['key']}`:")
    add("")
    add(f"> {statement['value']}")
    add("")
    add(statement["reading"])
    contrast = check["contrast"]
    add("")
    add(
        f"Контраст: `{contrast['repository']}` действительно заявляет "
        f"`{contrast['githubLicenseField']}`. Переносить эту лицензию на репозиторий сканов было бы"
    )
    add("выдумкой: лицензии там нет вовсе, и отсутствие лицензии не читается ни как разрешение,")
    add("ни как запрет.")
    add("")
    upstream = check.get("upstream")
    if upstream:
        add("### 4.1 Что заявил оцифровщик выше по цепочке")
        add("")
        add(
            f"Проверка GitHub-зеркала смотрит не туда, где возникает заявление. Сам предмет — "
            f"`{upstream['itemId']}` на archive.org; метаданные прочитаны один раз "
            f"(`{upstream['method']}`)."
        )
        add("")
        observed_up = upstream["observed"]
        add("| Поле метаданных | Значение |")
        add("|---|---|")
        add(f"| `possible-copyright-status` | `{observed_up['possibleCopyrightStatus']}` |")
        add(f"| `sponsor` | {observed_up['sponsor']} |")
        add(f"| `contributor` | {observed_up['contributor']} |")
        add(f"| `scanningcenter` | `{observed_up['scanningCenter']}` |")
        add(f"| `collection` | {', '.join(observed_up['collections'])} |")
        add(f"| `date` / `publisher` / `volume` | {observed_up['date']} / {observed_up['publisher']} / {observed_up['volume']} |")
        add(f"| `language` | {', '.join(observed_up['language'])} |")
        add("")
        add(upstream["reading"])
        add("")
        byte = check.get("byteCheck")
        if byte:
            add("### 4.2 Байты и том: что сверено в этом проходе")
            add("")
            add(f"Метод: {byte['method']}.")
            add("")
            add("| id | Файл | Байт | sha256 совпал с записью реестра |")
            add("|---|---|---:|---|")
            for obj in byte["objects"]:
                add(f"| `{obj['id']}` | `{obj['path']}` | {obj['bytes']} | {'да' if obj['sha256Matched'] else 'нет'} |")
            add("")
            add(byte["visualRead"])
            add("")
    corpus = check.get("corpusItems")
    if corpus:
        add("### 4.3 Предметы, на которые опирается корпус: статус заявлен у всех")
        add("")
        add(f"Метод: {corpus['method']}.")
        add("")
        add("| Предмет | Том | Год | `possible-copyright-status` | `copyright-region` | Спонсор / держатель | Кадров | ppi |")
        add("|---|---|---|---|---|---|---:|---:|")
        for it in corpus["items"]:
            add(
                f"| `{it['id']}` | {it['volume']} | {it['year']} | `{it['possibleCopyrightStatus']}` | "
                f"{('`' + it['copyrightRegion'] + '`') if it['copyrightRegion'] else '—'} | "
                f"{it['sponsor']} / {it['contributor']} | {it['imagecount']} | {it['ppi'] or '—'} |"
            )
        add("")
        add(corpus["reading"])
        add("")
        note = next(
            (it.get("qualityNote") for it in corpus["items"] if it.get("qualityNote")), None
        )
        if note:
            add(note)
            add("")
        add("Что это меняет для C-25 и подобных очередей: вопрос не «существуют ли сканы», а «кто "
            "скачает и прочитает». Ни один из шести предметов не открывается из среды, где "
            "собирался этот отчёт, поэтому визуальная сверка страниц остаётся делом человека с "
            "доступом к archive.org.")
        add("")
    add("Отсюда два честных пути закрытия восьми узлов — и оба требуют владельца, а не поиска:")
    add("")
    add("1. **Политика faithful reproduction.** Издание 1872 г. вне охраны (колофон осмотрен визуально),")
    add("   оцифровщик прав не заявляет. Решение о допустимости воспроизведения такой страницы —")
    add("   политика владельца с записанным обоснованием, а не «права установлены».")
    add("2. **Переприобретение из источника, где написано разрешение, а не только статус.** Те же")
    add("   страницы нужно получить там, где сказано, что файлы сканов можно переиспользовать.")
    add("   `NOT_IN_COPYRIGHT` этого не говорит: он про издание, а не про разрешение на копию")
    add("   скана. До тех пор основание прав остаётся рассуждением, а рассуждение — не основание.")
    add("")
    add("## 5. Границы")
    add("")
    for item in matrix["boundaries"]:
        add(f"- {item}")
    add("")
    add("Воспроизводимость: `python3 scripts/render_rights_matrix.py --check`.")
    add("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    matrix = load()
    problems = validate(matrix)
    if problems:
        print("Rights matrix: FAIL")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    rendered = render(matrix)
    if "--check" in argv:
        if not OUT.exists():
            print(f"Rights matrix: FAIL — нет {OUT.relative_to(ROOT)}")
            return 1
        if OUT.read_text(encoding="utf-8") != rendered:
            print("Rights matrix: FAIL — markdown разошёлся с JSON, перерисуйте скриптом")
            return 1
        print("Rights matrix: PASS (файлы соответствуют JSON и реестрам)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered, encoding="utf-8")
    print(f"собрано: {OUT.relative_to(ROOT)} — записей {len(matrix['entries'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
