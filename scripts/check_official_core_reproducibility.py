#!/usr/bin/env python3
"""Проверить квитанцию воспроизводимости трёх official-core архивов.

Offline-гейт проверяет форму, внутреннюю арифметику квитанции и производный Markdown:

    python3 -B scripts/check_official_core_reproducibility.py --check

Markdown пересобирается только из проверенной machine receipt:

    python3 -B scripts/check_official_core_reproducibility.py --write

Полный сетевой повтор скачивает неизменяемые GitHub archives во временный каталог,
проверяет размер и SHA-256 и ничего не распаковывает/не пишет в Research или Drive:

    python3 -B scripts/check_official_core_reproducibility.py --fetch

Уже скачанные файлы можно проверить без сети (по одному --archive на объект):

    python3 -B scripts/check_official_core_reproducibility.py \
      --archive STEPBible/STEPBible-Data=/tmp/stepbible.zip \
      --archive openscriptures/morphhb=/tmp/morphhb.zip \
      --archive Faithlife/SBLGNT=/tmp/sblgnt.zip

Квитанция подтверждает carrier по pinned commit, не содержание, права или публикацию.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import tempfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "official-core-datasets-reproducibility-2026-11-18.json"
STEP_TERMS = ROOT / "data" / "stepbible-subdataset-terms-2026-11-18.json"
OUT = ROOT / "docs" / "research" / "holds" / "OFFICIAL_CORE_DATASETS_REPRODUCIBILITY_2026-11-18.md"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_ROLE = "DERIVED_READ_ONLY_NOT_AUTHORITY"
EXPECTED_REPOSITORIES = {
    "STEPBible/STEPBible-Data",
    "openscriptures/morphhb",
    "Faithlife/SBLGNT",
}


def display_path(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: pathlib.Path) -> tuple[dict | None, list[str]]:
    if not path.is_file():
        return None, [f"нет {display_path(path)}"]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{display_path(path)} не разбирается: {exc}"]
    if not isinstance(value, dict):
        return None, [f"{display_path(path)}: корень должен быть JSON object"]
    return value, []


def validate(receipt: dict, step_terms: dict | None = None) -> list[str]:
    errors: list[str] = []
    if receipt.get("schemaVersion") != 1:
        errors.append("schemaVersion должен оставаться 1")
    if receipt.get("artifactId") != "OFFICIAL-CORE-DATASETS-REPRODUCIBILITY-2026-11-18":
        errors.append("artifactId вышел за bounded official-core receipt")
    if receipt.get("role") != EXPECTED_ROLE:
        errors.append(f"role должен быть {EXPECTED_ROLE}")
    if receipt.get("checkedAt") != "2026-11-18":
        errors.append("checkedAt должен сохранять исходную дату 2026-11-18")
    for field in ("question", "method"):
        if not isinstance(receipt.get(field), str) or not receipt[field].strip():
            errors.append(f"{field} должен быть непустой строкой")
    if receipt.get("urlPattern") != "https://codeload.github.com/{owner}/{repo}/zip/{commit}":
        errors.append("urlPattern не является закреплённым codeload-маршрутом")

    items = receipt.get("items")
    if not isinstance(items, list):
        return errors + ["items должен быть массивом"]

    repositories: list[str] = []
    bytes_total = 0
    recorded_total = 0
    matched = 0
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] должен быть object")
            continue
        prefix = f"items[{index}]"
        repository = item.get("repository")
        commit = item.get("commit")
        size = item.get("bytes")
        recorded = item.get("recordedBytes")
        digest = item.get("sha256")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip() or "|" in name or "\n" in name:
            errors.append(f"{prefix}.name некорректен для generated view")
        if not isinstance(repository, str) or repository.count("/") != 1:
            errors.append(f"{prefix}.repository некорректен")
        else:
            repositories.append(repository)
        if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
            errors.append(f"{prefix}.commit должен быть полным lowercase Git SHA")
        if not isinstance(size, int) or size <= 0:
            errors.append(f"{prefix}.bytes должен быть положительным числом")
        else:
            bytes_total += size
        if not isinstance(recorded, int) or recorded <= 0:
            errors.append(f"{prefix}.recordedBytes должен быть положительным числом")
        else:
            recorded_total += recorded
        if isinstance(size, int) and size == recorded:
            matched += 1
        else:
            errors.append(f"{prefix}: bytes не совпадает с recordedBytes")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"{prefix}.sha256 должен быть полным lowercase SHA-256")

    if len(repositories) != len(set(repositories)):
        errors.append("repository повторяется в items")
    if set(repositories) != EXPECTED_REPOSITORIES:
        errors.append(
            "набор repository отличается от bounded official-core тройки: "
            f"{sorted(repositories)}"
        )

    result = receipt.get("result")
    if not isinstance(result, dict):
        errors.append("result должен быть object")
    else:
        expected = {
            "matched": matched,
            "total": len(items),
            "bytesTotal": bytes_total,
            "recordedBytesTotal": recorded_total,
        }
        for field, value in expected.items():
            if result.get(field) != value:
                errors.append(f"result.{field}={result.get(field)!r}, вычислено {value}")
        if not isinstance(result.get("verdict"), str) or not result["verdict"].strip():
            errors.append("result.verdict должен быть непустой строкой")

    boundaries = receipt.get("boundaries")
    if not isinstance(boundaries, list) or len(boundaries) < 3 or not all(
        isinstance(line, str) and line.strip() for line in boundaries
    ):
        errors.append("boundaries должен явно фиксировать границы вывода")
    else:
        boundary_text = " ".join(boundaries)
        for required in (
            "не подтверждают права",
            "не распаковывалось и не читалось",
            "на 2026-11-18",
            "на Drive байты не попадали",
        ):
            if required not in boundary_text:
                errors.append(f"boundaries потерял обязательную границу: {required}")

    if step_terms is not None:
        step_item = next(
            (item for item in items if isinstance(item, dict) and item.get("repository") == "STEPBible/STEPBible-Data"),
            None,
        )
        pin = step_terms.get("pin") if isinstance(step_terms, dict) else None
        if not isinstance(step_item, dict) or not isinstance(pin, dict):
            errors.append("невозможно сопоставить STEPBible receipt с картой поднаборов")
        else:
            for field in ("repository", "commit", "bytes", "sha256"):
                if step_item.get(field) != pin.get(field):
                    errors.append(f"STEPBible {field} расходится с картой поднаборов")
    return errors


def receipt_items() -> tuple[list[dict], list[str]]:
    receipt, errors = load_json(RECEIPT)
    if receipt is None:
        return [], errors
    step_terms = None
    if STEP_TERMS.exists():
        step_terms, step_errors = load_json(STEP_TERMS)
        errors.extend(step_errors)
    errors.extend(validate(receipt, step_terms))
    items = receipt.get("items", []) if isinstance(receipt.get("items"), list) else []
    return items, errors


def grouped_int(value: int) -> str:
    return f"{value:,}".replace(",", "\u202f")


def render_markdown(receipt: dict) -> str:
    """Render the bounded human view only from the validated machine receipt."""
    lines = [
        f"# Official core: воспроизводимость закреплённых carrier ({receipt['checkedAt']})",
        "",
        f"**Роль:** `{receipt['role']}`. Это производная квитанция о carrier-байтах, а не",
        "заключение о содержании, правах, custody на Drive или публикации.",
        "",
        "Документ генерируется из",
        "`data/official-core-datasets-reproducibility-2026-11-18.json`; ручная правка запрещена.",
        "",
        "## 1. Датированный вопрос и метод",
        "",
        receipt["question"],
        "",
        f"**Метод:** {receipt['method']}",
        "",
        f"Закреплённый URL-шаблон: `{receipt['urlPattern']}`.",
        "",
        "## 2. Точная квитанция",
        "",
        "| Набор | Репозиторий | Commit | Байт | Записано, байт | SHA-256 |",
        "|---|---|---|---:|---:|---|",
    ]
    for item in receipt["items"]:
        lines.append(
            f"| {item['name']} | `{item['repository']}` | `{item['commit']}` | "
            f"{grouped_int(item['bytes'])} | {grouped_int(item['recordedBytes'])} | "
            f"`{item['sha256']}` |"
        )
    result = receipt["result"]
    lines.extend(
        [
            f"| **Итого** |  |  | **{grouped_int(result['bytesTotal'])}** | "
            f"**{grouped_int(result['recordedBytesTotal'])}** |  |",
            "",
            f"Совпало: **{result['matched']}/{result['total']}**. {result['verdict']}",
            "",
            "Истечение прежнего CI artifact поэтому не уничтожает единственный воспроизводимый",
            "carrier: каждый из трёх ZIP можно заново получить по полному pinned commit и проверить",
            "по размеру и полному SHA-256. Это не означает, что ZIP уже сохранены в независимой",
            "custody-копии.",
            "",
            "## 3. Границы",
            "",
        ]
    )
    lines.extend(f"- {boundary}" for boundary in receipt["boundaries"])
    lines.extend(
        [
            "- Датированная доступность commit на 2026-11-18 не является текущим сетевым ответом.",
            "- `RIGHTS_HOLD`, `PUBLICATION_HOLD`, `EVIDENCE_HOLD`, `ARCHIVE_HOLD` и `PROMOTE=0`",
            "  этим документом не меняются.",
            "",
            "## 4. Воспроизведение",
            "",
            "Offline-проверка JSON, арифметики, STEPBible pin и этого Markdown:",
            "",
            "```bash",
            "python3 -B scripts/check_official_core_reproducibility.py --check",
            "```",
            "",
            "Полный повтор скачивания во временный каталог и сверка трёх carrier:",
            "",
            "```bash",
            "python3 -B scripts/check_official_core_reproducibility.py --fetch",
            "```",
            "",
            "Сетевой режим обращается только к закреплённым `codeload.github.com` URL, не",
            "распаковывает архивы и не пишет в Research или Drive.",
            "",
        ]
    )
    return "\n".join(lines)


def markdown_errors(receipt: dict, out: pathlib.Path = OUT) -> list[str]:
    if not out.is_file():
        return [f"нет производного Markdown {display_path(out)}"]
    if out.read_text(encoding="utf-8") != render_markdown(receipt):
        return [f"{display_path(out)} разошёлся с JSON; выполните --write"]
    return []


def file_digest(path: pathlib.Path) -> tuple[int, str]:
    total = 0
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            total += len(chunk)
            digest.update(chunk)
    return total, digest.hexdigest()


def verify_archive(item: dict, path: pathlib.Path) -> list[str]:
    repository = item["repository"]
    if not path.is_file():
        return [f"{repository}: нет файла {path}"]
    size, digest = file_digest(path)
    errors: list[str] = []
    if size != item["bytes"]:
        errors.append(f"{repository}: размер {size}, ожидалось {item['bytes']}")
    if digest != item["sha256"]:
        errors.append(f"{repository}: SHA-256 {digest}, ожидалось {item['sha256']}")
    if not errors:
        print(f"PASS {repository}: {size} B / {digest}")
    return errors


def archive_url(item: dict) -> str:
    owner, repo = item["repository"].split("/", 1)
    return f"https://codeload.github.com/{owner}/{repo}/zip/{item['commit']}"


def fetch_and_verify(items: list[dict], directory: pathlib.Path) -> list[str]:
    errors: list[str] = []
    directory.mkdir(parents=True, exist_ok=True)
    for item in items:
        repo = item["repository"].split("/", 1)[1]
        path = directory / f"{repo}-{item['commit']}.zip"
        print(f"GET {archive_url(item)}", file=sys.stderr)
        try:
            with urllib.request.urlopen(archive_url(item), timeout=120) as response, path.open("wb") as out:
                while chunk := response.read(1 << 20):
                    out.write(chunk)
        except (OSError, TimeoutError) as exc:
            errors.append(f"{item['repository']}: fetch failed: {exc}")
            continue
        errors.extend(verify_archive(item, path))
    return errors


def parse_archives(values: list[str]) -> tuple[dict[str, pathlib.Path], list[str]]:
    result: dict[str, pathlib.Path] = {}
    errors: list[str] = []
    for value in values:
        repository, separator, raw_path = value.partition("=")
        if not separator or repository not in EXPECTED_REPOSITORIES or not raw_path:
            errors.append(f"неверный --archive {value!r}; нужен owner/repo=/path/file.zip")
            continue
        if repository in result:
            errors.append(f"--archive повторяет {repository}")
            continue
        result[repository] = pathlib.Path(raw_path)
    return result, errors


def report(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="offline-проверка квитанции и Markdown")
    parser.add_argument("--write", action="store_true", help="пересобрать Markdown из квитанции")
    parser.add_argument("--fetch", action="store_true", help="скачать и проверить все три pinned ZIP")
    parser.add_argument(
        "--archive",
        action="append",
        default=[],
        metavar="OWNER/REPO=PATH",
        help="проверить уже скачанный ZIP; повторить для каждого repository",
    )
    parser.add_argument("--cache-dir", type=pathlib.Path, help="оставить --fetch архивы в этом каталоге")
    args = parser.parse_args(argv)
    if sum((args.check, args.write, args.fetch, bool(args.archive))) != 1:
        parser.error("выберите ровно один режим: --check, --write, --fetch или --archive")

    items, errors = receipt_items()
    if errors:
        return report(errors)
    receipt, load_errors = load_json(RECEIPT)
    if receipt is None:
        return report(load_errors)
    if args.check:
        errors.extend(markdown_errors(receipt))
        if errors:
            return report(errors)
        print(f"official-core reproducibility: PASS ({len(items)} pinned receipts and Markdown agree)")
        return 0
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(render_markdown(receipt), encoding="utf-8")
        print(f"wrote {display_path(OUT)}")
        return 0
    if args.archive:
        archives, parse_errors = parse_archives(args.archive)
        errors.extend(parse_errors)
        missing = EXPECTED_REPOSITORIES - set(archives)
        if missing:
            errors.append(f"нет --archive для {sorted(missing)}")
        by_repo = {item["repository"]: item for item in items}
        for repository, path in archives.items():
            errors.extend(verify_archive(by_repo[repository], path))
        return report(errors)

    if args.cache_dir:
        errors.extend(fetch_and_verify(items, args.cache_dir))
    else:
        with tempfile.TemporaryDirectory(prefix="official-core-") as tmp:
            errors.extend(fetch_and_verify(items, pathlib.Path(tmp)))
    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
