#!/usr/bin/env python3
"""Снимок хранения артефактов CI: что лежит только в Actions и когда исчезнет.

Зачем: репозиторий объявляет часть собранных объектов `EPHEMERAL_ACTION_ARTIFACT`
с `durableReceiptPresent: false`. Это честное объявление, но его никто не
проверяет: нет ни одного места, где видно, сколько байт и до какой даты живёт
только в Actions. Скрипт считает это по API и раскладывает по классам
воспроизводимости.

Только чтение: `gh api` по артефактам и чтение workflow-файлов. Ничего не
скачивается, ни один HOLD не снимается и не ставится.

    python3 scripts/audit_artifact_custody.py            # отчёт в stdout
    python3 scripts/audit_artifact_custody.py --write    # + записать JSON и MD
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = "FedorMilovanov/Research"
OUT_JSON = ROOT / "data" / "artifact-custody-snapshot-2026-11-18.json"
OUT_MD = ROOT / "docs" / "research" / "holds" / "ARTIFACT_CUSTODY_SNAPSHOT_2026-11-18.md"

# Классы воспроизводимости. Это не догадка: класс определяется тем, что
# workflow делает с внешним объектом, и записывается явно для каждой семьи.
DETERMINISM = {
    "link-audit": (
        "REGENERABLE_AUDIT",
        "Проверка ссылок: результат — отчёт о состоянии URL на момент прогона. "
        "Перепрогон даёт новый отчёт, но исходные объекты не теряются.",
    ),
    "1peter-product-handoff": (
        "REGENERABLE_AUDIT",
        "Пакет handoff собирается из файлов репозитория; артефакт — производная сборка.",
    ),
    "baptist-proof-ledger-v2-canonical-view": (
        "REGENERABLE_VIEW",
        "Канонический вид строится из реестра в репозитории.",
    ),
    "total-cross-repo-source-audit": (
        "REGENERABLE_AUDIT",
        "Сводный аудит источников: отчёт о состоянии, а не приобретённый объект.",
    ),
    "baptist-scan-request-package": (
        "REGENERABLE_PACKAGE",
        "Пакет запроса на сканы — заявка, а не сам скан.",
    ),
    "charnock-custody-v3-research-only": (
        "HAS_DURABLE_RECEIPT",
        "Оба V3-архива имеют квитанцию с Drive ID и SHA-256; сумма сверена с Drive 2026-11-18.",
    ),
    "ephemeral-second-editorial-40-pdf": (
        "NON_DETERMINISTIC_ACQUISITION",
        "Сборка PDF из внешних источников; перепрогон даёт актуальное состояние источников, "
        "а не те же байты. Квитанции на хранение нет.",
    ),
    "ephemeral-commons-strict-literary-pdf-40plus": (
        "NON_DETERMINISTIC_ACQUISITION",
        "То же: внешние PDF, перепрогон не воспроизводит прежние байты.",
    ),
    "ephemeral-official-core-acquisition-59-v2": (
        "NON_DETERMINISTIC_ACQUISITION",
        "Приобретение официальных цифровых коллекций; на стороне источника объекты меняются.",
    ),
    "ephemeral-poet-portrait-review-v4": (
        "NON_DETERMINISTIC_ACQUISITION",
        "Отобранные портреты для ревью; источник может измениться.",
    ),
    "ephemeral-ephemera-review-candidates": (
        "NON_DETERMINISTIC_ACQUISITION",
        "Кандидаты эфемерид для ревью.",
    ),
    "ephemeral-approved-ephemera-originals": (
        "NON_DETERMINISTIC_ACQUISITION",
        "Одобренные оригиналы, скачанные из внешнего источника.",
    ),
    "ephemeral-approved-core-poet-portraits": (
        "NON_DETERMINISTIC_ACQUISITION",
        "Одобренные портреты из внешнего источника.",
    ),
    "g3-": (
        "NON_DETERMINISTIC_ACQUISITION",
        "G3: записи IRS, округов, Wayback-снимки. Wayback и опубликованный IRS XML стабильны, "
        "но записи округов и текущие страницы меняются; квитанции на хранение нет.",
    ),
}


def gh_pages() -> list[dict]:
    rows: list[dict] = []
    for page in range(1, 40):
        proc = subprocess.run(
            [
                "gh",
                "api",
                f"repos/{REPO}/actions/artifacts?per_page=100&page={page}",
                "--jq",
                ".artifacts[]|{name,expired,created_at,expires_at,size_in_bytes,branch:.workflow_run.head_branch}",
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise SystemExit(f"gh api failed: {proc.stderr[:300]}")
        chunk = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
        if not chunk:
            break
        rows += chunk
    return rows


def family_of(name: str) -> str:
    base = re.sub(r"-[0-9a-f]{40}$", "", name)
    base = re.sub(r"-\d{8,}-\d+$", "", base)
    base = re.sub(r"-(item-)?\d+$", "", base)
    base = re.sub(r"-\d{8,}$", "", base)
    return base


def classify(family: str) -> tuple[str, str]:
    if family.startswith("g3-"):
        return DETERMINISM["g3-"]
    if family in DETERMINISM:
        return DETERMINISM[family]
    if "link-audit" in family:
        return DETERMINISM["link-audit"]
    return ("UNCLASSIFIED", "Семья не описана в скрипте; требует ручного решения.")


G3_TOKENS = ("g3", "irs"), ("g3", "buck"), ("g3", "wayback"), ("g3", "douglas"), ("g3", "georgia"), ("g3", "content"), ("g3", "archive")


def g3_workflow(family: str) -> str | None:
    """Сопоставить g3-семью с workflow-файлом по первым двум токенам имени."""
    tokens = family.split("-")
    key = tuple(tokens[:2])
    if key not in G3_TOKENS:
        return None
    matches = sorted(
        path
        for path in (ROOT / ".github" / "workflows").glob("g3-*.yml")
        if path.name.split("-")[:2] == list(key)
    )
    return f".github/workflows/{matches[0].name}" if matches else None


def workflow_map() -> dict[str, dict]:
    """Какая workflow-файл производит артефакт и какое retention объявлено."""
    mapping: dict[str, dict] = {}
    for path in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        retention = re.search(r"retention-days:\s*(\d+)", text)
        declares_ephemeral = "EPHEMERAL_ACTION_ARTIFACT" in text
        receipt_false = "durableReceiptPresent': False" in text or 'durableReceiptPresent": false' in text
        receipt_true = "durableReceiptPresent': True" in text or 'durableReceiptPresent": true' in text
        for match in re.finditer(r"^\s*name:\s*([a-z0-9][a-z0-9._-]*)\s*$", text, re.MULTILINE):
            name = match.group(1)
            if not re.search(r"(audit|ephemeral|g3-|handoff|package|ledger|custody)", name):
                continue
            mapping.setdefault(
                name,
                {
                    "workflow": f".github/workflows/{path.name}",
                    "retentionDays": int(retention.group(1)) if retention else None,
                    "declaresEphemeral": declares_ephemeral,
                    "declaresNoDurableReceipt": receipt_false,
                    "declaresDurableReceipt": receipt_true,
                },
            )
    return mapping


def build() -> dict:
    rows = [r for r in gh_pages() if r["name"] != "gitleaks-results.sarif"]
    families: dict[str, dict] = {}
    for row in rows:
        family = family_of(row["name"])
        item = families.setdefault(
            family,
            {
                "family": family,
                "artifacts": 0,
                "bytes": 0,
                "firstCreated": row["created_at"][:10],
                "lastCreated": row["created_at"][:10],
                "earliestExpiry": row["expires_at"][:10] if row["expires_at"] else None,
                "expired": 0,
                "branches": set(),
            },
        )
        item["artifacts"] += 1
        item["bytes"] += row["size_in_bytes"]
        item["firstCreated"] = min(item["firstCreated"], row["created_at"][:10])
        item["lastCreated"] = max(item["lastCreated"], row["created_at"][:10])
        if row["expired"]:
            item["expired"] += 1
        if row["expires_at"]:
            day = row["expires_at"][:10]
            item["earliestExpiry"] = min(item["earliestExpiry"] or day, day)
        if row["branch"]:
            item["branches"].add(row["branch"])

    workflows = workflow_map()
    for item in families.values():
        cls, why = classify(item["family"])
        item["class"] = cls
        item["why"] = why
        meta = workflows.get(item["family"]) or {}
        if not meta and item["family"].startswith("g3-"):
            path = g3_workflow(item["family"])
            if path:
                text = (ROOT / path).read_text(encoding="utf-8")
                retention = re.search(r"retention-days:\s*(\d+)", text)
                meta = {
                    "workflow": path,
                    "retentionDays": int(retention.group(1)) if retention else None,
                    "declaresEphemeral": "EPHEMERAL_ACTION_ARTIFACT" in text,
                    "declaresNoDurableReceipt": "durableReceiptPresent': False" in text
                    or 'durableReceiptPresent": false' in text,
                    "declaresDurableReceipt": False,
                }
        if not meta:
            for candidate_path in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
                candidate_text = candidate_path.read_text(encoding="utf-8")
                if f"name: {item['family']}" not in candidate_text:
                    continue
                retention = re.search(r"retention-days:\s*(\d+)", candidate_text)
                meta = {
                    "workflow": f".github/workflows/{candidate_path.name}",
                    "retentionDays": int(retention.group(1)) if retention else None,
                    "declaresEphemeral": "EPHEMERAL_ACTION_ARTIFACT" in candidate_text,
                    "declaresNoDurableReceipt": "durableReceiptPresent': False" in candidate_text
                    or 'durableReceiptPresent": false' in candidate_text,
                    "declaresDurableReceipt": False,
                }
                break
        if not meta:
            for name, candidate in workflows.items():
                if item["family"].startswith(name) or name.startswith(item["family"]):
                    meta = candidate
                    break
        item["workflow"] = meta.get("workflow")
        item["retentionDays"] = meta.get("retentionDays")
        item["declaresEphemeral"] = meta.get("declaresEphemeral", False)
        item["declaresNoDurableReceipt"] = meta.get("declaresNoDurableReceipt", False)
        item["branches"] = sorted(item["branches"])

    ordered = sorted(families.values(), key=lambda x: -x["bytes"])
    by_class = collections.Counter()
    bytes_by_class = collections.Counter()
    for item in ordered:
        by_class[item["class"]] += item["artifacts"]
        bytes_by_class[item["class"]] += item["bytes"]

    deadline = collections.defaultdict(lambda: {"bytes": 0, "families": []})
    for item in ordered:
        if item["earliestExpiry"]:
            deadline[item["earliestExpiry"]]["bytes"] += item["bytes"]
            deadline[item["earliestExpiry"]]["families"].append(item["family"])

    return {
        "schemaVersion": 1,
        "artifactId": "ARTIFACT-CUSTODY-SNAPSHOT-2026-11-18",
        "role": "DERIVED_READ_ONLY_NOT_AUTHORITY",
        "generatedAt": "2026-11-18",
        "repo": REPO,
        "method": "gh api repos/<repo>/actions/artifacts по всем страницам; gitleaks-отчёты исключены как шум сканера",
        "families": ordered,
        "totals": {
            "artifacts": sum(item["artifacts"] for item in ordered),
            "bytes": sum(item["bytes"] for item in ordered),
            "expired": sum(item["expired"] for item in ordered),
            "families": len(ordered),
            "byClass": dict(by_class),
            "bytesByClass": dict(bytes_by_class),
        },
        "deadlines": {day: {"bytes": v["bytes"], "families": sorted(v["families"])} for day, v in sorted(deadline.items())},
    }


def render(snapshot: dict) -> str:
    totals = snapshot["totals"]
    lines: list[str] = []
    add = lines.append
    add("# Хранение артефактов CI: что живёт только в Actions (2026-11-18)")
    add("")
    add("**Роль:** `DERIVED_READ_ONLY_NOT_AUTHORITY`. Снимок, не решение: ни один HOLD здесь не")
    add("снимается и не ставится.")
    add("")
    add(f"**Метод:** `{snapshot['method']}`.")
    add("")
    add("## 1. Зачем это считать")
    add("")
    add("Часть объектов репозиторий сам объявляет `EPHEMERAL_ACTION_ARTIFACT` с")
    add("`durableReceiptPresent: false`. Объявление честное, но проверять его было нечем: нигде не")
    add("видно, **сколько байт и до какой даты** существует только внутри Actions. Снимок это")
    add("показывает, и делит артефакты по воспроизводимости — потому что «эфемерный» не значит")
    add("«потерянный»: отчёт о ссылках пересобирается, а скачанный из внешнего источника PDF — нет.")
    add("")
    add("## 2. Итог")
    add("")
    add(f"Живых артефактов (без отчётов сканера): **{totals['artifacts']}** в "
        f"**{totals['families']}** семьях, суммарно **{totals['bytes'] / 1e9:.2f} ГБ**.")
    add(f"Просроченных: **{totals['expired']}**. Ноль здесь читается узко: GitHub держит")
    add("просроченные артефакты в списке ещё около 90 дней, поэтому «ноль» означает «ни один из")
    add("живых не истёк», а не «за всё время ничего не пропало».")
    add("")
    add("| Класс | Артефактов | Байт | Что это значит |")
    add("|---|---:|---:|---|")
    meaning = {
        "HAS_DURABLE_RECEIPT": "есть квитанция хранения с Drive ID и SHA-256",
        "REGENERABLE_AUDIT": "пересобирается; потеря артефакта не теряет доказательство",
        "REGENERABLE_VIEW": "производная сборка из реестра репозитория",
        "REGENERABLE_PACKAGE": "заявка/пакет, а не сам объект",
        "NON_DETERMINISTIC_ACQUISITION": "перепрогон даёт другое состояние источника — байты не воспроизводятся",
        "UNCLASSIFIED": "требует ручного решения",
    }
    for cls, count in sorted(totals["byClass"].items(), key=lambda kv: -totals["bytesByClass"][kv[0]]):
        add(f"| `{cls}` | {count} | {totals['bytesByClass'][cls] / 1e9:.2f} ГБ | {meaning.get(cls, '—')} |")
    add("")
    add("## 3. Семьи")
    add("")
    add("| Семья | n | ГБ | Класс | Создано | Истекает | retention | Объявлено |")
    add("|---|---:|---:|---|---|---|---:|---|")
    for item in snapshot["families"]:
        declared = "эфемерно, квитанции нет" if item["declaresNoDurableReceipt"] else (
            "квитанция есть" if item["class"] == "HAS_DURABLE_RECEIPT" else "не объявлено"
        )
        add(
            f"| `{item['family']}` | {item['artifacts']} | {item['bytes'] / 1e9:.2f} | "
            f"`{item['class']}` | {item['firstCreated']}…{item['lastCreated']} | "
            f"{item['earliestExpiry'] or '—'} | "
            f"{item['retentionDays'] if item['retentionDays'] is not None else '—'} | {declared} |"
        )
    add("")
    add("## 4. Ближайший обрыв")
    add("")
    for day, payload in snapshot["deadlines"].items():
        families = ", ".join(f"`{f}`" for f in payload["families"])
        add(f"- **{day}**: {payload['bytes'] / 1e9:.2f} ГБ — {families}")
    add("")
    add("Ближайшая дата — через несколько дней. Это не значит, что доказательства исчезнут: у")
    add("большинства семей перепрогон даёт сопоставимый объект. Но у класса")
    add("`NON_DETERMINISTIC_ACQUISITION` перепрогон даёт **другое состояние источника**, и если")
    add("владелец считает прежние байты доказательством, их нужно забрать до этой даты.")
    add("")
    add("## 5. Что здесь не так, помимо срока")
    add("")
    add("Артефакты сборки PDF висят на прогонах **dependabot-ветвей**: обновление версии")
    add("`upload-artifact` меняет сам workflow-файл, а path-фильтр включает этот файл, поэтому")
    add("каждый dependabot-PR пересобирает архив в гигабайт. Побочный эффект: живой артефакт")
    add("последней сборки может оказаться копией с ветки, которая вот-вот закроется.")
    add("")
    add("## 6. Границы")
    add("")
    add("- Снимок описывает только артефакты Actions. Объекты в Drive и в репозитории он не проверяет.")
    add("- Класс воспроизводимости назначен по тому, что workflow делает с внешним объектом, а не")
    add("  по проверке совпадения байтов двух прогонов: такой проверки не делалось.")
    add("- `HAS_DURABLE_RECEIPT` присвоен только семье Charnock V3, и только потому, что суммы")
    add("  сверены с Drive 2026-11-18 в `docs/research/holds/DRIVE_SHA256_READBACK_CROSSCHECK_2026-11-18.md`.")
    add("- Снимок датирован. Retention и состав семей меняются каждым прогоном, поэтому файл")
    add("  пересобирается, а не правится.")
    add("")
    add("Воспроизводимость: `python3 scripts/audit_artifact_custody.py`.")
    add("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    snapshot = build()
    text = render(snapshot)
    if "--write" in argv:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        OUT_MD.parent.mkdir(parents=True, exist_ok=True)
        OUT_MD.write_text(text, encoding="utf-8")
        print(f"записано: {OUT_JSON.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)}")
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
