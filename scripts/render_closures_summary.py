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
import sys
from pathlib import Path

BEGIN = "<!-- closures-summary:begin -->"
END = "<!-- closures-summary:end -->"
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
    "pinned-github-locator-readback": "перечитывание закреплённых локаторов",
    "text-integrity-repair": "сверка склеек с историей",
    "register-claims-audit": "счётчики против артефактов",
    "server-checksum-readback": "серверная контрольная сумма",
    "read-only-link-audit": "read-only проверка ссылок",
    "relative-link-audit": "проверка относительных ссылок",
    "hold-vocabulary-mapping": "соответствие неканонических значений `holds`",
    "space-restoration-backed-by-file-history": "пробелы по истории файла",
    "internal-digest-rehash": "пересчёт внутренних подписей",
}


def render(registry: dict) -> str:
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
    for confirmation in confirmations:
        lines.append(
            f"- `{confirmation.get('id', '')}` — {(confirmation.get('title') or '').strip()}"
        )
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


def replace_block(text: str, block: str) -> tuple[str, bool]:
    start = text.find(BEGIN)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        return text, False
    return text[:start] + block + text[end + len(END):], True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--register", default=DEFAULT_REGISTER)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print", dest="print_only", action="store_true")
    args = parser.parse_args(argv)

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    block = render(registry)
    register_path = Path(args.register)
    text = register_path.read_text(encoding="utf-8")
    updated, found = replace_block(text, block)

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
