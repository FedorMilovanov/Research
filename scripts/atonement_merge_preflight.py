#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Предполётная проверка ветки «Искупления» перед мержем с параллельным агентом.

Зачем. Две сессии агентов пишут в один и тот же корпус: длинный журнал
`ИСКУПЛЕНИЕ/18_SERIES_AUDIT_AND_ARCS_2026-10-26.md` (только дописывается в конец),
сгенерированные скриптами JSON-своды и каталог `scripts/`. Конфликт в JSON или в
хвосте журнала стоит не «красного CI», а разъехавшихся выводов, поэтому проверять
надо ДО мержа, а не после.

Что проверяется (жёсткие проверки — при провале код 1):

  H1  рабочее дерево чистое (снимается ключом --allow-dirty);
  H2  в отслеживаемых файлах нет маркеров конфликта (`<<<<<<<`, `>>>>>>>`, `=======` в начале строки);
  H3  в индексе нет неразрешённых путей (unmerged);
  H4  origin/main — предок HEAD, то есть ветка не отстала от main;
  H5  нумерация разделов журнала `18_…` строго возрастает и не повторяется
      (дубль `### 9.N` — самый частый след ручного разрешения конфликта);
  H6  нет неотслеживаемых файлов, которые попадут в коммит «за компанию»
      (снимается ключом --allow-untracked);

Мягкие отчёты (не влияют на код возврата):

  R1  какие файлы ветка меняла относительно точки отделения от main — по владельцам
      подкорпусов из реестра `parallelAgents` (ot/, nt/, fathers/, synthesis/);
  R2  пересечение «мы меняли» × «main менял» — это и есть будущие конфликты;
  R3  расхождение числа разделов журнала с последним номером (пропуски в нумерации).

Ключи: --with-gates (после предполёта прогнать три гейта в режиме --check),
       --allow-dirty, --allow-untracked, --json.
Код возврата: 0 — можно мержить, 1 — есть жёсткий провал, 2 — не удалось снять состояние.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "ИСКУПЛЕНИЕ" / "18_SERIES_AUDIT_AND_ARCS_2026-10-26.md"
REGISTRY = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-corpus-v1.json"

CONFLICT = re.compile(r"^(<{7}|>{7}|={7})(\s|$)")
SECTION = re.compile(r"^###\s+9\.(\d+)\b")
TEXT_SUFFIXES = {".md", ".py", ".json", ".sh", ".txt", ".yml", ".yaml", ".csv", ".tsv"}
SKIP_DIRS = (".git/", "node_modules/", ".venv/", "dist/", "build/")


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-c", "core.quotepath=false", *args],
                          cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout


def git_ok(*args: str) -> bool:
    return subprocess.run(["git", *args], cwd=ROOT,
                          capture_output=True).returncode == 0


def changed_files() -> list[str]:
    """Файлы, изменённые веткой относительно точки отделения от origin/main."""
    try:
        out = git("diff", "--name-only", "origin/main...HEAD")
    except RuntimeError:
        out = git("diff", "--name-only", "HEAD~1..HEAD")
    return [line for line in out.splitlines() if line.strip()]


def main_changed_files(base: str) -> list[str]:
    try:
        out = git("diff", "--name-only", f"{base}..origin/main")
    except RuntimeError:
        return []
    return [line for line in out.splitlines() if line.strip()]


GENERATED = re.compile(r"/data/[\w.-]*corpus-v1\.json$")


def domain_of(path: str, domains: list[tuple[str, str]]) -> str:
    """Сгенерированные своды — отдельная категория: их не «владеют», их пересобирают."""
    if GENERATED.search(path):
        return "своды подкорпусов (генерируются)"
    for prefix, label in domains:
        if path.startswith(prefix):
            return label
    if path.startswith("ИСКУПЛЕНИЕ/evidence/"):
        return "корень/свидетельства"
    if path.startswith("ИСКУПЛЕНИЕ/data/"):
        return "корень/своды"
    if path.startswith("ИСКУПЛЕНИЕ/"):
        return "корень/журнал и карточки"
    if path.startswith("scripts/"):
        return "скрипты"
    return "вне корпуса"


def load_domains() -> list[tuple[str, str]]:
    """Владельцы подкорпусов берутся из реестра, а не из головы."""
    fallback = [
        ("ИСКУПЛЕНИЕ/ot/", "агент 1 · Ветхий Завет"),
        ("ИСКУПЛЕНИЕ/nt/", "агент 2 · Новый Завет"),
        ("ИСКУПЛЕНИЕ/fathers/", "агент 3 · Отцы"),
        ("ИСКУПЛЕНИЕ/synthesis/", "агент 4 · синтез"),
    ]
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        block = data.get("parallelAgents") or {}
        out = []
        for item in block.get("domains") or []:
            sub = str(item.get("subCorpus") or "").strip()
            if sub:
                short = sub.rstrip("/").rsplit("/", 1)[-1]
                out.append((sub if sub.endswith("/") else sub + "/",
                            f"агент {item.get('agent', '?')} · {short}"))
        return out or fallback
    except (OSError, ValueError, AttributeError):
        return fallback


def scan_conflicts() -> list[str]:
    bad: list[str] = []
    try:
        listed = git("ls-files", "-z").split("\0")
    except RuntimeError:
        return ["<не удалось получить список файлов>"]
    for rel in listed:
        if not rel or rel.startswith(SKIP_DIRS):
            continue
        if Path(rel).suffix.lower() not in TEXT_SUFFIXES:
            continue
        p = ROOT / rel
        try:
            if p.stat().st_size > 4_000_000:
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if CONFLICT.match(line):
                bad.append(f"{rel}:{lineno}: {line[:40]}")
                break
    return bad


def scan_sections() -> tuple[list[str], list[str], dict]:
    """Дубли и невозрастающая нумерация разделов журнала."""
    problems: list[str] = []
    notes: list[str] = []
    info = {"разделов": 0, "первый": None, "последний": None}
    if not AUDIT.is_file():
        return ["журнал 18_… не найден"], [], info
    seen: dict[int, int] = {}
    last = None
    for lineno, line in enumerate(AUDIT.read_text(encoding="utf-8").splitlines(), 1):
        m = SECTION.match(line)
        if not m:
            continue
        num = int(m.group(1))
        info["разделов"] += 1
        if info["первый"] is None:
            info["первый"] = num
        if num in seen:
            problems.append(f"дубль раздела §9.{num}: строки {seen[num]} и {lineno}")
        else:
            seen[num] = lineno
        if last is not None and num <= last:
            problems.append(f"нумерация не возрастает: §9.{num} (стр. {lineno}) после §9.{last}")
        last = num
        info["последний"] = num
    if info["первый"] is not None and info["последний"] is not None:
        span = info["последний"] - info["первый"] + 1
        if span > info["разделов"]:
            notes.append(f"в диапазоне §9.{info['первый']}–§9.{info['последний']} "
                         f"пропущено {span - info['разделов']} номеров (это нормально, "
                         f"если номера заняты разделами других сессий; дублей быть не должно)")
    return problems, notes, info


def run_gates() -> list[tuple[str, bool, str]]:
    steps = [
        ("реестр доводов", ["scripts/atonement_claim_register.py", "--check"]),
        ("пересъём", ["scripts/atonement_reshoot_state.py", "--check"]),
        ("целостность", ["scripts/validate_atonement_corpus_integrity.py"]),
    ]
    out = []
    for label, argv in steps:
        proc = subprocess.run([sys.executable, "-B", *argv], cwd=ROOT,
                              capture_output=True, text=True)
        tail = (proc.stdout or proc.stderr).strip().splitlines()
        out.append((label, proc.returncode == 0, tail[-1] if tail else "(нет вывода)"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--allow-untracked", action="store_true")
    ap.add_argument("--with-gates", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    hard: list[str] = []
    soft: list[str] = []
    report: dict = {}

    try:
        branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
        head = git("rev-parse", "--short", "HEAD").strip()
        porcelain = git("status", "--porcelain").splitlines()
    except RuntimeError as exc:
        print(f"MERGE PREFLIGHT: не удалось снять состояние — {exc}")
        return 2

    report["ветка"], report["head"] = branch, head

    # H1/H6: дерево и неотслеживаемые файлы
    dirty = [ln for ln in porcelain if not ln.startswith("??")]
    untracked = [ln[3:] for ln in porcelain if ln.startswith("??")]
    if dirty and not args.allow_dirty:
        hard.append(f"рабочее дерево не чистое: изменено/удалено {len(dirty)} путей")
    if untracked and not args.allow_untracked:
        hard.append(f"неотслеживаемых файлов {len(untracked)} — они уедут в коммит "
                    f"«за компанию»: {', '.join(untracked[:5])}"
                    + (" …" if len(untracked) > 5 else ""))

    # H2: маркеры конфликта
    conflicts = scan_conflicts()
    if conflicts:
        hard.append(f"маркеры конфликта в {len(conflicts)} файлах: " + "; ".join(conflicts[:3]))

    # H3: неразрешённые пути
    unmerged = [ln for ln in git("ls-files", "-u").splitlines() if ln.strip()]
    if unmerged:
        hard.append(f"в индексе {len(unmerged)} неразрешённых путей")

    # H4: не отстали ли от main
    try:
        base = git("merge-base", "HEAD", "origin/main").strip()
        behind = git("rev-list", "--count", f"HEAD..origin/main").strip()
        ahead = git("rev-list", "--count", f"origin/main..HEAD").strip()
    except RuntimeError as exc:
        hard.append(f"origin/main недоступен: {exc}")
        base, behind, ahead = "", "?", "?"
    if behind.isdigit() and int(behind):
        hard.append(f"ветка отстала от origin/main на {behind} коммит(ов) — "
                    f"перед мержем слить main в ветку")
    report["отставание_от_main"] = behind
    report["опережение_main"] = ahead

    # H5/R3: журнал
    sec_problems, sec_notes, sec_info = scan_sections()
    hard.extend(sec_problems)
    soft.extend(sec_notes)
    report["журнал"] = sec_info

    # R1/R2: владельцы файлов и пересечение с main
    domains = load_domains()
    ours = changed_files()
    theirs = main_changed_files(base) if base else []
    by_domain: dict[str, list[str]] = {}
    for path in ours:
        by_domain.setdefault(domain_of(path, domains), []).append(path)
    report["наши_файлы"] = {k: len(v) for k, v in sorted(by_domain.items())}
    overlap = sorted(set(ours) & set(theirs))
    if overlap:
        soft.append(f"main тоже менял {len(overlap)} из наших файлов — это будущие конфликты: "
                    + "; ".join(overlap[:5]) + (" …" if len(overlap) > 5 else ""))
    foreign = [k for k in by_domain if k.startswith("агент")]
    if foreign:
        soft.append("ветка трогает подкорпуса других владельцев: "
                    + ", ".join(f"{k} ({len(by_domain[k])})" for k in foreign)
                    + " — правится только по договорённости с владельцем домена")
    if "своды подкорпусов (генерируются)" in by_domain:
        soft.append("сгенерированные своды (" + str(len(by_domain["своды подкорпусов (генерируются)"]))
                    + " файлов) при конфликте не сливаются руками: берём любую сторону "
                      "и пересобираем `--write`, затем `--check`")

    gates = run_gates() if args.with_gates else []
    if gates:
        report["гейты"] = {label: ok for label, ok, _ in gates}
        for label, ok, tail in gates:
            if not ok:
                hard.append(f"гейт «{label}» красный: {tail}")

    if args.json:
        report["жёсткие"] = hard
        report["мягкие"] = soft
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"MERGE PREFLIGHT: ветка {branch} @ {head}; "
              f"отставание от main {report['отставание_от_main']}, "
              f"опережение {report['опережение_main']}")
        if report.get("наши_файлы"):
            print("  файлы ветки по владельцам: " + ", ".join(
                f"{k} — {v}" for k, v in report["наши_файлы"].items()))
        if report["журнал"].get("последний") is not None:
            print(f"  журнал: разделов {report['журнал']['разделов']}, "
                  f"последний §9.{report['журнал']['последний']}")
        for label, ok, tail in gates:
            print(f"  гейт «{label}»: {'PASS' if ok else 'FAIL'} — {tail[:120]}")
        for line in soft:
            print(f"  замечание: {line}")

    if hard:
        print("MERGE PREFLIGHT: FAIL")
        for line in hard:
            print(f"  - {line}")
        return 1
    print("MERGE PREFLIGHT: PASS — ветку можно мержить")
    return 0


if __name__ == "__main__":
    sys.exit(main())
