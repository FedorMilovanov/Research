#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Закрытие круга — порядок, в котором числа становятся каноническими (круг 64).

Название выбрано соседним с `atonement_close_round.py` и нарочно не совпадающим: под прежним
именем в реестре помянут утраченный счётчик чисел кругов 61–62 (см. §9.3 аудита и шапку
`atonement_reshoot_state.py`), и возвращать его было бы тем же грехом, что и выдать пересъёмщик
за спасённый оригинал — тот файл не восстановлен, а его роль чисел с круга 63 живёт в
пересъёмщике.

Зачем: до этого круга последовательность «писатели → пересъём → реестр локаторов → пересъём →
гейт → батарея» жила в голове автора круга и в прозе §9.3 аудита. Она была описана командами, но
исполнялась руками, и ровно на этом месте круг 62 потерял работу: правка после последнего
пересъёма ломает `--check`, а рука помнит порядок не всегда. Порядок — не знание, а инструмент,
поэтому он здесь код, а не памятка.

Что он делает и чего не делает:
  • пишет только то, что пишут названные им инструменты, и в единственном допустимом порядке;
    сам он не содержит ни одного числа, ни одной даты и ни одной правки реестра;
  • отказывается запускать двух писателей (`atonement_drive_mirror_round63.py --write` и
    `atonement_library_index_round63.py --write`), пока ему явно не разрешат и не назовут круг:
    каждый `--write` дописывает запись в индекс или в `driveMirrors`, то есть двигает ценз,
    который сверяет правило 25, — это событие круга, а не часть сходимости;
  • после каждого витка смотрит на `git status --porcelain` и краснеет, если изменён путь вне
    дозволенного списка: так заметна рука, решившая «попутно» поправить что-нибудь ещё;
  • ничего не публикует: `publicationEligible` ему не принадлежит, и он его не читает как право.

Режимы:
  --plan        напечатать порядок и зачем он такой; ничего не исполняется, ничего не пишется
  --selfcheck   только читающая часть (гейт, `--check` пересъёмщика, `--check` и `--cross`
                реестра локаторов); этим же его гоняет CI
  --run         сходимость: пересъём, реестр локаторов, пересъём, затем читающая часть
  --run --with-battery [--with-proof <ref>]
                то же плюс батарея мутаций и, по желанию, доказательство на чистом клоне
  --allow-appending-writers --confirm-circle N
                дополнительно разрешить двух писателей (по одному вызову каждого)

Коды выхода: 0 — круг закрыт, всё сошлось; 1 — расхождение (печатается дословно, без сглаживания);
2 — отказ: запрошены писатели без подтверждения, или в дереве мусор, который не объясним порядком.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable or "python3"

# пути, которым позволено меняться во время закрытия круга; всё остальное — чужая правка
ALLOWED_DIRTY = (
    "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json",
    "ИСКУПЛЕНИЕ/data/atonement-library-index.json",
    "ИСКУПЛЕНИЕ/18_SERIES_AUDIT_AND_ARCS_2026-10-26.md",
)

RESHOOT = ["scripts/atonement_reshoot_state.py"]
REGISTER = ["scripts/atonement_claim_register.py"]
GATE = "scripts/validate_atonement_corpus_integrity.py"
BATTERY = "scripts/run_atonement_mutation_battery.py"
PROOF = "scripts/atonement_proof_round63.sh"

WRITERS = (
    ("scripts/atonement_drive_mirror_round63.py", "--write",
     "дописывает запись в `driveMirrors` и переснимает перечисление прежней записи"),
    ("scripts/atonement_library_index_round63.py", "--write",
     "дописывает запись в индекс библиотеки и вытесняет прежнюю в `HOLD_superseded`"),
)


def sh(cmd, why=""):
    """Один шаг: команда, её вывод хвостом, код возврата. Ничего не переписывает и не глушит."""
    printable = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    print(f"  $ {printable}")
    if isinstance(cmd, str):
        r = subprocess.run(["bash", "-c", cmd], cwd=str(ROOT), capture_output=True, text=True)
    else:
        r = subprocess.run([PY] + cmd, cwd=str(ROOT), capture_output=True, text=True)
    out = (r.stdout + (("\n" + r.stderr) if r.stderr.strip() else "")).rstrip()
    tail = out.split("\n")[-3:] if out else ["(пусто)"]
    for line in tail:
        print(f"     │ {line}")
    mark = "ok" if r.returncode == 0 else f"код {r.returncode}"
    print(f"     → {mark}{'' if not why else ' — ' + why}")
    return r.returncode, out


def dirty_paths():
    """Грязь по отслеживаемым файлам. Новые файлы (untracked) сюда не входят намеренно: проверка
    о том, что канон не правят вне порядка, а не о том, что в песочнице лежит черновик.
    Неотслеживаемое видно по обычному `git status` в выводе круга."""
    r = subprocess.run(["git", "-c", "core.quotepath=off", "status", "--porcelain",
                        "--untracked-files=no"], cwd=str(ROOT), capture_output=True, text=True)
    return [ln[3:].strip() for ln in r.stdout.split("\n") if ln.strip()]


def preflight():
    """Среда годна или нет — решается до первой цифры. Новый круг открывается в клоне глубиной в
    один коммит, и в таком клоне вся git-сверка (правило 20, чтение blob'ов зеркал, аудит времени
    коммитов) обязана молчать; пусть она говорит здесь, а не притворяется пройденной внутри круга."""
    shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=str(ROOT),
                             capture_output=True, text=True).stdout.strip()
    base = subprocess.run(["git", "rev-parse", "--verify", "-q", "origin/main"], cwd=str(ROOT),
                           capture_output=True, text=True).stdout.strip()
    problems = []
    if shallow != "false":
        problems.append("клон shallow — история не достана")
    if not base:
        problems.append("нет локального refs/remotes/origin/main")
    if problems:
        print("ОТКАЗ СРЕДЫ: " + "; ".join(problems))
        print("  достать историю и ссылку: git fetch --deepen 2400 origin main && git fetch origin "
              "+refs/heads/main:refs/remotes/origin/main")
        print("  без этого числа правила 20 и сверка зеркал не замер, а догадка; круг с такой средой "
              "не закрывается")
        return 2
    ncommits = subprocess.run(["git", "rev-list", "--count", "origin/main"], cwd=str(ROOT),
                              capture_output=True, text=True).stdout.strip()
    print(f"среда годна: клон не shallow, origin/main = {base[:7]}, истории видно {ncommits} коммитов")
    return 0


def unexpected_dirty(before):
    now = set(dirty_paths())
    fresh = now - before
    return sorted(p for p in fresh if p not in ALLOWED_DIRTY)


def plan():
    print("порядок закрытия круга (исполняется именно так, порядок — часть определения чисел):")
    steps = [
        ("шаг −1: годна ли среда",
         f"{PY} -B scripts/atonement_round_close.py --selfcheck (проверка среды внутри)",
         "новый круг открывается в клоне глубиной в один коммит; в нём правило 20 и сверка "
         "зеркал обязаны объявить недоказуемость, а не молча пройти — поэтому среда проверяется "
         "раньше первой цифры"),
        ("писатели, только по явному подтверждению",
         " ".join(f"{PY} -B {s[0]} {s[1]}" for s in WRITERS),
         "каждый вызов дописывает запись; без подтверждения этот шаг отсутствует, и `--plan` его "
         "не выполнит ни при каких обстоятельствах"),
        ("сходимость чисел: пересъём",
         f"{PY} -B {RESHOOT[0]} --write",
         "неподвижная точка корпус ↔ документ; внутри до восьми витков"),
        ("локаторы строк после правки документа",
         f"{PY} -B {REGISTER[0]} --write root",
         "строковые локаторы §9.1 сдвигает любая правка документа, поэтому они пишутся после "
         "пересъёма, а не до него"),
        ("сходимость ещё раз: пересъём обязан сойтись на прогоне #0",
         f"{PY} -B {RESHOOT[0]} --write",
         "второй вызов — не перестраховка, а проверка, что правка реестра локаторов не сдвинула "
         "число, которое пересъёмщик сверяет"),
        ("гейт корпуса",
         f"{PY} -B {GATE}",
         "арбитр содержимого: 27 правил, `publicationEligible=false` на выходе обязано остаться"),
        ("пересъёмщик: только сверка",
         f"{PY} -B {RESHOOT[0]} --check",
         "тот же шаг живёт в workflow `atonement-corpus-integrity` — круг закрыт, только если он "
         "зелёный в чистом дереве"),
        ("реестр локаторов: только сверка",
         f"{PY} -B {REGISTER[0]} --check && {PY} -B {REGISTER[0]} --cross",
         "пять ланов сходятся, и root-ссылки вне обхода лана равны объявленному числу"),
        ("батарея мутаций (по флагу)",
         f"{PY} -B {BATTERY}",
         "ловит ли гейт то, что обещает; ~4 минуты, поэтому только по `--with-battery`"),
        ("доказательство на чистом клоне (по флагу)",
         f"bash {PROOF} <ref>",
         "единственный способ увидеть, что пересъём не зависит от песочницы: после мержа круг "
         "обязан быть доказан на origin/main"),
    ]
    for i, (what, cmd, why) in enumerate(steps, 1):
        print(f" {i}. {what}\n      {cmd}\n      — {why}")
    print("\nсам этот инструмент проверяется так:")
    print(f"      {PY} -B scripts/atonement_round_close.py --selfcheck")
    return 0


def selfcheck():
    if preflight() != 0:
        return 2
    bad = []
    code, _ = sh([GATE], "гейт корпуса")
    bad += [] if code == 0 else ["гейт"]
    code, _ = sh([RESHOOT[0], "--check"], "пересъёмщик, только сверка")
    bad += [] if code == 0 else ["пересъёмщик --check"]
    code, _ = sh([REGISTER[0], "--check"], "реестр локаторов, пять ланов")
    bad += [] if code == 0 else ["register --check"]
    code, _ = sh([REGISTER[0], "--cross"], "root-ссылки вне обхода лана")
    bad += [] if code == 0 else ["register --cross"]
    if bad:
        print("САМОПРОВЕРКА КРУГА: РАСХОЖДЕНИЕ — " + ", ".join(bad))
        return 1
    print("САМОПРОВЕРКА КРУГА: всё зелёное — гейт, пересъёмщик, реестр локаторов, перекрёстная сверка")
    return 0


def run(args):
    if preflight() != 0:
        return 2
    before = set(dirty_paths())
    if args.allow_appending_writers and not args.confirm_circle:
        print("ОТКАЗ: писатели разрешены флагом, но круг не назван. Каждый `--write` дописывает "
              "запись в индекс или в `driveMirrors` и двигает ценз правила 25 — это событие круга, "
              "а не часть сходимости. Повторите с --confirm-circle <номер>.")
        return 2
    if args.allow_appending_writers:
        print(f"--- шаг 0: писатели (подтверждено кругом {args.confirm_circle}) ---")
        for script, flag, why in WRITERS:
            code, _ = sh([script, flag], why)
            if code != 0:
                print(f"НЕ ЗАКРЫТО: писатель {script} вернул код {code} — дальше идти нельзя, "
                      "половина записи в бухгалтерии означает расхождение ценза")
                return 1
    print("--- шаг 1: сходимость чисел ---")
    for i in range(3):
        code, _ = sh([RESHOOT[0], "--write"], f"виток {i + 1}: числа корпуса и прозы документа")
        if code != 0:
            print("НЕ ЗАКРЫТО: пересъёмщик не сошёлся за восемь своих прогонов — он сам это печатает, "
                  "чинить молча нельзя")
            return 1
        code, _ = sh([REGISTER[0], "--write", "root"], "локаторы §9.1 после правки документа")
        if code != 0:
            print("НЕ ЗАКРЫТО: реестр локаторов не записался")
            return 1
        code, out = sh([RESHOOT[0], "--write"], "второй пересъём обязан сказать «прогон #0»")
        # критерий неподвижности — не «вывод похож», а ровно то слово, которым пересъёмщик
        # называется первый удачный виток; если он снова пишет байты, порядок не закрыт
        if code == 0 and "сошлось на прогоне #0" in out:
            break
        print("     · ещё не неподвижная точка — повторяю виток")
    else:
        print("НЕ ЗАКРЫТО: за три витка порядок не сошёлся — определение где-то читает то, что само "
              "же меняет; это ищут руками, а не ещё одним прогоном")
        return 1
    print("--- шаг 2: читающая часть ---")
    if selfcheck() != 0:
        return 1
    if args.with_battery:
        print("--- шаг 3: батарея мутаций ---")
        code, out = sh([BATTERY], "ловит ли гейт то, что обещает")
        good = "непопаданий: 0" in out and "не проверено: 0" in out
        if code != 0 or not good:
            print("НЕ ЗАКРЫТО: батарея не подтвердила ловлю — последние строки её вывода напечатаны "
                  "выше дословно")
            return 1
    if args.with_proof:
        print(f"--- шаг 4: доказательство на чистом клоне {args.with_proof} ---")
        code, _ = sh(f"bash {PROOF} {args.with_proof}", "18+ проверок в дереве из remote")
        if code != 0:
            print("НЕ ЗАКРЫТО: доказательство отказало — оно краснее, чем закрытый круг, и это тот "
                  "случай, когда красный вывод лучше зелёного")
            return 1
    stray = unexpected_dirty(before)
    if stray:
        print("НЕ ЗАКРЫТО: вне дозволенного списка изменены пути — " + ", ".join(stray[:6])
              + " ; порядок круга не трогает ничего, кроме корпуса, индекса и документа аудита")
        return 2
    print(f"ЗАКРЫТО: порядок отработан, пересъёмщик и реестр сходятся, изменены только пути "
          f"{', '.join(ALLOWED_DIRTY)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="atonement_round_close.py", add_help=True,
                                 description="порядок закрытия круга ланы ИСКУПЛЕНИЕ")
    ap.add_argument("--plan", action="store_true", help="напечатать порядок, ничего не исполняя")
    ap.add_argument("--selfcheck", action="store_true", help="только читающая часть")
    ap.add_argument("--run", action="store_true", help="отработать порядок целиком")
    ap.add_argument("--with-battery", action="store_true", help="внутри --run добавить батарею мутаций")
    ap.add_argument("--with-proof", metavar="REF", default="",
                    help="внутри --run добавить доказательство на чистом клоне ref")
    ap.add_argument("--allow-appending-writers", action="store_true",
                    help="разрешить двух писателей, дописывающих записи")
    ap.add_argument("--confirm-circle", metavar="N", default="",
                    help="номер круга, которым подтверждается разрешение писателей")
    args = ap.parse_args()
    if args.plan:
        if args.run or args.selfcheck:
            print("ОТКАЗ: --plan не совмещается с исполняющими режимами: план обязан быть безвредным")
            return 2
        return plan()
    if args.selfcheck:
        return selfcheck()
    if args.run:
        return run(args)
    print("употребление: atonement_round_close.py [--plan | --selfcheck | --run [--with-battery] "
          "[--with-proof REF]] [--allow-appending-writers --confirm-circle N]")
    return 2


if __name__ == "__main__":
    sys.exit(main())
