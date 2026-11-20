#!/usr/bin/env python3
"""Render the one-page map of the closure registry, and refuse to let it go stale.

The register grew to eighteen sections and fourteen closures. A reader who wants to
know "what was actually verified today, and what is still open" had to walk the whole
document and assemble the answer by hand - which is how a summary becomes a quotation
of an older state of the file it summarises.

So the summary is generated, not written: this tool reads
``data/hold-closure-registry-v1.json`` and prints the block between

    <!-- closures-summary:begin -->
    <!-- closures-summary:end -->

with ``--write`` into the register, and with ``--check`` it fails when the committed
block differs from the one the registry implies. Every closure's axis, HOLD type,
method and record location come from the registry itself; the open items come from the
registry's own ``notClosed`` list. Nothing here invents a count.

    python3 -B scripts/render_closures_summary.py --check
    python3 -B scripts/render_closures_summary.py --write

``--check`` is gated in CI: a summary that disagrees with the registry is exactly the
"stale counter" this whole register is about.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BEGIN = "<!-- closures-summary:begin -->"
END = "<!-- closures-summary:end -->"
DETAIL_BEGIN = "<!-- closures-detail:begin -->"
PLACE_RE = re.compile(r"^(?P<path>[^\s,]+?\.(?:md|json|py|txt|ya?ml))(?P<rest>.*)$")
DETAIL_END = "<!-- closures-detail:end -->"
DEFAULT_REGISTRY = "data/hold-closure-registry-v1.json"
DEFAULT_REGISTER = "docs/research/HOLDS_REGISTER_2026-11-18.md"
METHOD_NAMES = {
    "raw-download-compare": "скачивание и пересчёт байтов",
    "drive-metadata-read": "чтение метаданных Drive",
    "internal-digest-rehash": "пересчёт внутренних подписей",
    "short-digest-label": "разметка коротких подписей",
    "document-twin-shingles": "сравнение текстов",
    "state-stamp-vs-commit": "дата в заголовке против Git",
    "drive-ledger-join": "реестр против ответа Drive",
    "unclaimed-reason-classification": "классификация строк",
    "relative-link-audit": "проверка относительных ссылок",
    "hold-vocabulary-mapping": "соответствие неканонических значений `holds`",
    "ci-trigger-dependency-audit": "сверка триггеров CI с зависимостями гейтов",
    "self-confirmation-regression": "регрессия на самоподтверждение",
    "confirmation-counter-audit": "счётчики подтверждений против артефактов",
    "pinned-github-locator-readback": "перечитывание закреплённых локаторов",
    "text-integrity-repair": "сверка склеек с историей",
    "register-claims-audit": "счётчики против артефактов",
    "server-checksum-readback": "серверная контрольная сумма",
    "read-only-link-audit": "read-only проверка ссылок",
    "relative-link-audit": "проверка относительных ссылок",
    "hold-vocabulary-mapping": "соответствие неканонических значений `holds`",
    "ci-trigger-dependency-audit": "сверка триггеров CI с зависимостями гейтов",
    "self-confirmation-regression": "регрессия на самоподтверждение",
    "confirmation-counter-audit": "счётчики подтверждений против артефактов",
    "space-restoration-backed-by-file-history": "пробелы по истории файла",
    "internal-digest-rehash": "пересчёт внутренних подписей",
}


def _place(entry: str) -> str:
    """A record location as a link: the path links, the section and prose after it do not."""
    entry = entry.strip()
    match = PLACE_RE.match(entry)
    if not match:
        return f"`{entry}`"
    path, rest = match.group("path"), match.group("rest").strip()
    if not path.startswith(("data/", "docs/", "scripts/", "БИОГРАФИИ/", "ИСКУПЛЕНИЕ/", "СЕРИЯ", "STEVE_LAWSON/", "history/")):
        return f"`{entry}`"
    # the register lives in docs/research/, so a repository path needs two levels up
    link = f"[`{path}`](../../{path})"
    if rest.startswith("§"):
        return f"{link} {rest}"
    return f"{link}{' ' + rest if rest else ''}"


def render_detail(registry: dict) -> str:
    """Per-closure detail, generated: the hand-kept version of this table had lost rows.

    §3 listed eighteen closures while the registry held twenty-five. It was a third copy -
    after §0 and the registry itself - and the only one nobody regenerated.
    """
    closures = registry.get("closures", [])
    lines = [DETAIL_BEGIN, "| Запись | Что закрыто | Метод | Где отражено |", "|---|---|---|---|"]
    for closure in closures:
        ident = f"`{closure.get('id', '')}`"
        scope = (closure.get("closedScope") or closure.get("title") or "").replace("|", "\\|")
        method = closure.get("method", "")
        places = closure.get("recordLocations") or []
        where = ", ".join(_place(p) for p in places[:2]) or "—"
        lines.append(f"| {ident} | {scope} | {METHOD_NAMES.get(method, method)} | {where} |")
    lines.append(DETAIL_END)
    return "\n".join(lines)


class CounterError(Exception):
    """A confirmation counter that cannot be resolved is a broken promise, not a blank."""


def _pick(data: dict, field: str):
    node = data
    for part in field.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def render_counter(counter: dict, root: Path) -> str:
    """``label`` + a value read from an artefact; never from the registry's memory."""
    artefact, field = counter.get("artefact"), counter.get("field")
    if not artefact or not field:
        raise CounterError(f"counter without artefact/field: {counter!r}")
    path = root / artefact
    if not path.is_file():
        raise CounterError(f"counter artefact missing: {artefact}")
    value = _pick(json.loads(path.read_text(encoding="utf-8")), field)
    if not isinstance(value, int):
        raise CounterError(f"counter field is not a number: {artefact} {field}")
    label = counter.get("label") or field
    return f"{label}: {f'{value:,}'.replace(',', chr(0x2009))}"


def render(registry: dict, root: Path | None = None) -> str:
    root = root or Path(".")
    closures = registry.get("closures", [])
    confirmations = registry.get("confirmations", [])
    open_items = registry.get("notClosed", [])
    by_type: dict[str, int] = {}
    for closure in closures:
        key = closure.get("holdType") or "не указан"
        by_type[key] = by_type.get(key, 0) + 1
    lines = [
        BEGIN,
        "## 0. Карта закрытий (генерируется; не редактировать руками)",
        "",
        f"Закрытий: **{len(closures)}**. Подтверждений без закрытия: **{len(confirmations)}**."
        f" Открытых пунктов по существу: **{len(open_items)}**.",
        "",
        "По типу HOLD: " + ", ".join(f"`{k}` — {v}" for k, v in sorted(by_type.items())) + ".",
        "",
        "| № | Ось | HOLD | Чем проверено | Где запись |",
        "|---|---|---|---|---|",
    ]
    for closure in closures:
        number = closure.get("id", "").rsplit("-", 1)[-1]
        title = (closure.get("title") or closure.get("axis") or "").replace("|", "\\|")
        method = closure.get("method", "")
        places = closure.get("recordLocations") or ([closure["evidence"]] if closure.get("evidence") else [])
        where = ", ".join(f"`{p}`" for p in places[:2]) or "—"
        lines.append(
            f"| {number} | {title} | `{closure.get('holdType', '—')}`"
            f" | {METHOD_NAMES.get(method, method)} | {where} |"
        )
    lines += ["", "**Подтверждения (не закрытия):**"]
    # A confirmation used to print its own title, and the titles carried measurements
    # ("17 объектов", "36/36", "8 из 24"). Nothing checked them: by now three of the four
    # were stale. Numbers come from artefacts; the title carries none.
    for confirmation in confirmations:
        ident = (confirmation.get("id") or "").strip()
        title = (confirmation.get("title") or "").strip()
        counters = [render_counter(c, root) for c in confirmation.get("counters", [])]
        detail = f" ({'; '.join(counters)})" if counters else ""
        superseded = (confirmation.get("supersededBy") or "").strip()
        note = f" — значения пересняты в {superseded}" if superseded else ""
        lines.append(f"- `{ident}` — {title}{detail}{note}")
    lines += ["", "**Осталось открытым по существу:**"]
    # An open item's identity is its id, not a sentence. The earlier version rendered the
    # item's display text, which happened to carry two measurements inside the name; the
    # generated map then repeated numbers that nothing checked - and one of them was wrong.
    for item in open_items:
        ident = (item.get("id") or "").strip()
        title = (item.get("title") or "").strip()
        reason = (item.get("reason") or "").strip()
        short = reason.split(".")[0][:180]
        lines.append(f"- `{ident}` — {title}. {short}.")
    lines += [
        "",
        "Строки этой карты не являются проверкой: они перечисляют, где проверка записана.",
        "Перегенерация: `python3 -B scripts/render_closures_summary.py --write`;",
        "расхождение с реестром ловит `--check` (шаг CI).",
        END,
    ]
    return "\n".join(lines)


def replace_block(text: str, block: str, begin: str = BEGIN, end: str = END) -> tuple[str, bool]:
    # The markers are parameters: the first version read the module globals, so a second
    # call replaced the first block with the second block's content. The slice must use the
    # found index, not the marker string - which is how one newline went missing here.
    start, stop = text.find(begin), text.find(end)
    if start == -1 or stop == -1 or stop < start:
        return text, False
    return text[:start] + block + text[stop + len(end):], True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--register", default=DEFAULT_REGISTER)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print", dest="print_only", action="store_true")
    parser.add_argument("--root", default=".", help="where artefacts live (counters are read from there)")
    args = parser.parse_args(argv)

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    try:
        block = render(registry, Path(args.root))
    except CounterError as exc:
        print(f"closure summary: {exc}", file=sys.stderr)
        return 2
    register_path = Path(args.register)
    text = register_path.read_text(encoding="utf-8")
    detail = render_detail(registry)
    updated, found = replace_block(text, block, BEGIN, END)
    updated, detail_found = replace_block(updated, detail, DETAIL_BEGIN, DETAIL_END)
    found = found and detail_found

    if args.print_only or not (args.write or args.check):
        print(block)
        return 0
    if not found:
        print(f"markers {BEGIN} … {END} not found in {args.register}", file=sys.stderr)
        return 1
    if args.write:
        register_path.write_text(updated, encoding="utf-8")
        print(f"wrote {args.register}", file=sys.stderr)
        return 0
    if args.check and updated != text:
        print("closure summary is stale: the registry and the register disagree", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
