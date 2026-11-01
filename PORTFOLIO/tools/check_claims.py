#!/usr/bin/env python3
"""Гейт портфолио: сверяет утверждения из CLAIMS.csv с данными и структуру каталога.

Что проверяется:

1. **Считаемое.** Утверждения с `computable=metrics_sum:*` / `metrics_field:*`
   пересчитываются из `METRICS.csv`; с `computable=media_value:*` — из
   `MEDIA_METRICS.csv`. Расхождение = провал.
2. **Реестр.** Уникальные id, допустимые статусы (`CONFIRMED`, `DERIVED`,
   `UNPROVEN`), заполненные `source`, `checked`, `status`.
3. **Индекс.** Каждый markdown-файл верхнего уровня `PORTFOLIO/` (кроме `README.md`)
   обязан быть указан в `README.md`.
4. **Ссылки.** Каждая относительная markdown-ссылка внутри `PORTFOLIO/` ведёт
   в существующий файл.
5. **Устаревшие числа.** В документах текущего состояния не должно быть
   опровергнутых значений (они остаются только в журнале и в протоколе
   перепроверки, где описано «было → стало»).
6. **Паритет RU/EN.** Ключевые числа обязаны совпадать в русской и английской
   версиях портфолио с учётом формата разделителей.

Запуск: `python3 PORTFOLIO/tools/check_claims.py` (только стандартная библиотека).
Выход 0 — реестр согласован, 1 — есть расхождения.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

PORTFOLIO = Path(__file__).resolve().parents[1]
REPO_ROOT = PORTFOLIO.parent

STATUSES = {"CONFIRMED", "DERIVED", "UNPROVEN"}
REQUIRED_COLUMNS = ["id", "category", "claim_ru", "value", "unit", "scope", "source", "method", "computable", "status", "checked"]
# Документы, описывающие текущее состояние. Журнал проверки и протокол
# перепроверки сюда не входят: в них опровергнутые числа хранятся намеренно.
CURRENT_STATE_DOCS = [
    "README.md",
    "AUDIT_RU.md",
    "PORTFOLIO_RU.md",
    "PORTFOLIO_EN.md",
    "PROFILE_README.md",
    "DEEP_SWEEP.md",
    "HISTORY_AND_PRINCIPLES.md",
    "DEFECT_CLASSES.md",
    "DEFINITION_OF_DONE.md",
]
STALE_TOKENS = ["17 831", "576/576", "658/658", "183 из 183", "239/239"]
# Ключевые числа: (русская запись, английская запись). EN-файл использует
# запятую как разделитель разрядов, поэтому пары проверяются как есть.
PARITY = [
    ("824 453", "824,453"),
    ("766 175", "766,175"),
    ("512 322", "512,322"),
    ("119 919", "119,919"),
    ("2 877", "2,877"),
    ("3 834", "3,834"),
    ("754/754", "754/754"),
    ("241", "241"),
]

problems: list[str] = []
notes: list[str] = []


def fail(message: str) -> None:
    problems.append(message)


def load_csv(path: Path, delimiter: str = ";") -> list[dict[str, str]]:
    with io.open(path, encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def to_int(raw: str) -> int:
    text = (raw or "").strip().replace(" ", "").replace("\u00a0", "")
    return int(text)


def metrics_value(rows: list[dict[str, str]], spec: str) -> int | None:
    """spec: `<колонка>:all` | `<колонка>:not=<repo>` | `<колонка>:kind~<префикс>`."""
    column, _, selector = spec.partition(":")
    if not selector:
        return None
    if selector == "all":
        selected = rows
    elif selector.startswith("not="):
        excluded = selector.split("=", 1)[1]
        selected = [row for row in rows if row["repository"] != excluded]
    elif selector.startswith("kind~"):
        prefix = selector.split("~", 1)[1]
        selected = [row for row in rows if row["kind"].startswith(prefix)]
    else:
        return None
    total = 0
    for row in selected:
        raw = (row.get(column) or "").strip()
        if raw.isdigit():
            total += int(raw)
        elif raw:
            return None
    return total


def metrics_field(rows: list[dict[str, str]], spec: str) -> int | None:
    """spec: `<repository>:<колонка>`."""
    repository, _, column = spec.partition(":")
    for row in rows:
        if row["repository"] == repository:
            raw = (row.get(column) or "").strip()
            return int(raw) if raw.isdigit() else None
    return None


def media_value(rows: list[dict[str, str]], spec: str) -> int | None:
    """spec: `<surface>:<metric>` — первая строка с такой парой."""
    surface, _, metric = spec.partition(":")
    for row in rows:
        if row["surface"] == surface and row["metric"] == metric:
            raw = (row.get("value") or "").strip()
            return int(raw) if raw.isdigit() else None
    return None


def check_claims() -> tuple[int, int, int]:
    path = PORTFOLIO / "CLAIMS.csv"
    if not path.is_file():
        fail("CLAIMS.csv отсутствует")
        return 0, 0, 0
    with io.open(path, encoding="utf-8-sig") as handle:
        header = handle.readline().strip().split(";")
    missing = [column for column in REQUIRED_COLUMNS if column not in header]
    if missing:
        fail(f"CLAIMS.csv: нет колонок {', '.join(missing)}")

    claims = load_csv(path)
    metrics = load_csv(PORTFOLIO / "METRICS.csv")
    media: list[dict[str, str]] = []  # счётчики аудитории сняты из портфолио по решению владельца

    seen: set[str] = set()
    counts = {"CONFIRMED": 0, "DERIVED": 0, "UNPROVEN": 0}
    for row in claims:
        claim_id = (row.get("id") or "").strip()
        if not claim_id:
            fail("CLAIMS.csv: строка без id")
            continue
        if claim_id in seen:
            fail(f"{claim_id}: повторяющийся id")
        seen.add(claim_id)

        status = (row.get("status") or "").strip()
        if status not in STATUSES:
            fail(f"{claim_id}: недопустимый статус {status!r}")
            continue
        counts[status] += 1
        for column in ("source", "checked", "method"):
            if not (row.get(column) or "").strip():
                fail(f"{claim_id}: пустое поле {column}")

        computable = (row.get("computable") or "").strip()
        if not computable or computable in {"none", "measured"}:
            continue
        raw_value = (row.get("value") or "").strip()
        if not raw_value.replace(" ", "").isdigit():
            fail(f"{claim_id}: считаемое утверждение с нечисловым значением {raw_value!r}")
            continue
        expected = to_int(raw_value)

        if computable.startswith("metrics_sum:"):
            actual = metrics_value(metrics, computable.split(":", 1)[1])
        elif computable.startswith("metrics_field:"):
            actual = metrics_field(metrics, computable.split(":", 1)[1])
        elif computable.startswith("media_value:"):
            actual = media_value(media, computable.split(":", 1)[1])
        else:
            fail(f"{claim_id}: неизвестное правило {computable!r}")
            continue

        if actual is None:
            fail(f"{claim_id}: правило {computable!r} не дало значения")
        elif actual != expected:
            fail(f"{claim_id}: в реестре {expected}, пересчёт даёт {actual} ({computable})")
    return counts["CONFIRMED"], counts["DERIVED"], counts["UNPROVEN"]


def check_index() -> None:
    index = (PORTFOLIO / "README.md").read_text(encoding="utf-8")
    for path in sorted(PORTFOLIO.glob("*.md")):
        if path.name == "README.md":
            continue
        if path.name not in index:
            fail(f"README.md: не указан {path.name}")
    for extra in ("CLAIMS.csv", "DEFINITION_OF_DONE.md", "tools/check_claims.py", "tools/measure_defense.py"):
        if extra not in index:
            fail(f"README.md: не указан {extra}")


LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")


def check_links() -> None:
    for document in sorted(PORTFOLIO.rglob("*.md")):
        text = document.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for match in LINK.finditer(text):
            target = match.group("target").strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            resolved = (document.parent / target).resolve()
            if not resolved.exists():
                fail(f"{document.relative_to(REPO_ROOT)}: битая ссылка {match.group('target')}")


def check_stale() -> None:
    for name in CURRENT_STATE_DOCS:
        path = PORTFOLIO / name
        if not path.is_file():
            fail(f"нет документа текущего состояния {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in STALE_TOKENS:
            if token in text:
                fail(f"{name}: опровергнутое значение {token!r} всё ещё в документе текущего состояния")


def check_parity() -> None:
    ru = (PORTFOLIO / "PORTFOLIO_RU.md").read_text(encoding="utf-8")
    en = (PORTFOLIO / "PORTFOLIO_EN.md").read_text(encoding="utf-8")
    for ru_form, en_form in PARITY:
        if ru_form not in ru:
            fail(f"PORTFOLIO_RU.md: нет ключевого числа {ru_form}")
        if en_form not in en:
            fail(f"PORTFOLIO_EN.md: нет ключевого числа {en_form}")


def main() -> int:
    confirmed, derived, unproven = check_claims()
    check_index()
    check_links()
    check_stale()
    check_parity()

    print(f"утверждений: {confirmed + derived + unproven}  "
          f"CONFIRMED {confirmed}  DERIVED {derived}  UNPROVEN {unproven}")
    if problems:
        print(f"\nрасхождений: {len(problems)}")
        for item in problems:
            print("  - " + item)
        return 1
    print("OK: реестр согласован с данными, индекс, ссылки и паритет RU/EN в порядке")
    print("    непроверяемыми остаются только утверждения со статусом UNPROVEN — их список в DEFINITION_OF_DONE.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
