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
PROBE = "scripts/atonement_history_perturbation_probe.py"

WRITERS = (
    # Кто в паре — называет круг, а не вечность: писатель чужого круга переснимал бы чужую
    # запись своими штампами и своим listing'ом, а у listing'а папки с момента переаливки
    # другое живое лицо. Прежняя пара (round63) уходит вместе со своим кругом: её числа
    # держит пересъёмщик (разрыв), а её listing остаётся транскрипцией своего часа.
    ("scripts/atonement_drive_mirror_round66.py", "--write",
     "дописывает запись `driveMirrors.corpusSnapshotRound66_20261027` и вытеснение прежней записи"),
    ("scripts/atonement_library_index_round66.py", "--write",
     "дописывает строку индекса нового слепка и снимает у прежней права `mirror_of_git`"),
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
    if branch_parity() != 0:
        return 2
    if canon_parity() != 0:
        print("  пока канона в индексе нет, числа не снимаются: сверка будет описывать то, чего "
              "дерево не содержит")
        return 2
    return 0


def plural_ru(n: int, one: str = "коммит", few: str = "коммита", many: str = "коммитов") -> str:
    """Число с формой — чтобы в отказе не было «на 1 коммитов»."""
    d, dd = n % 10, n % 100
    form = one if d == 1 and dd != 11 else (few if 2 <= d <= 4 and not 11 <= dd <= 14 else many)
    return f"{n} {form}"


def canon_tool_paths():
    """Список инструментов канона — один на всех: `PIPELINE_FILES` пересъёмщика."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("reshoot_for_preflight", str(ROOT / RESHOOT[0]))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.PIPELINE_FILES) + [PROOF]


def canon_parity():
    """Каждый инструмент канона обязан быть не только на диске, но и в индексе.

    Третий откат снапшота за этот круг был тише первых двух: файлы полосы остались на диске, а
    индекс перестал их знать, и `git status` смолчал — неотслеженный файл для него не расхождение,
    а просто чужой. Коммит в таком состоянии собрал бы дерево, в котором нет половины круга, а
    описывал бы он инструменты, которых в этом дереве нет: реестр знает их байты, и это знание
    ничего не проверяет, пока проверяющий сам лежит вне git.

    Отличие от «дерево изменилось» принципиально: незакоммиченная правка инструмента — обычное
    состояние середины круга, её и ловить нечего (пересъём инвентаря её оформляет), а вот
    *отсутствие в индексе* — это уже не работа, а потеря: следующее восстановление среды унесёт
    файл, и ни одна сверка об этом не скажет.
    """
    idx = set(subprocess.run(["git", "ls-files", "--"], cwd=str(ROOT), capture_output=True,
                             text=True).stdout.split("\n"))
    head = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.split("\n")
    headset = set(head)
    paths = canon_tool_paths()
    missing = [f for f in paths if f not in idx]
    if missing:
        print("ОТКАЗ СРЕДЫ: инструментов канона нет в индексе — %s. Файл на диске без индекса "
              "переживёт ближайший `git add -A` и не переживёт восстановления снапшота"
              % ", ".join(missing))
        print("  вернуть в индекс: git add %s" % " ".join(missing))
        print("  если файл чужой и не должен был появиться: удалить с диска, а не оставлять "
              "неотслеженным — реестр описывает инструменты, которые круг собирается закоммитить")
        return 1
    fresh = [f for f in paths if f not in headset]
    if fresh:
        print("  %s в индексе, но ещё не в HEAD — новый инструмент круга, это законно до коммита"
              % ", ".join(fresh))
    changed = 0
    for f in paths:
        if f in headset:
            a = subprocess.run(["git", "rev-parse", "HEAD:" + f], cwd=str(ROOT),
                              capture_output=True, text=True).stdout.strip()
            b = subprocess.run(["git", "hash-object", f], cwd=str(ROOT),
                              capture_output=True, text=True).stdout.strip()
            if a and b and a != b:
                changed += 1
    print("  канон цел: %d инструмента в индексе, из них %d отличаются от HEAD (незакоммиченная "
          "правка круга, инвентарь переснимет)" % (len(paths), changed))
    return 0


def branch_parity():
    """Локальная ветка не имеет права отставать от того, что лежит на удалённом имени круга.

    Пустой `git status` значит только согласие индекса с рабочим деревом — он молчит и в том
    состоянии, в котором этот круг застал песочницу вторично за ночь: указатель ветки откатился
    на коммит предыдущего круга вместе с восстановлением снапшота, файлы круга остались на диске,
    но для git стали неотслеженными, а `--run` закоммитил бы дерево, в котором нет ни проба, ни
    ловушек, — и был бы собой доволен, потому что сверяется он с локальным HEAD. Значит, сравнивать
    надо не с HEAD, а с удалённым именем ветки: опережать его можно (незапушенный коммит — обычное
    состояние середины круга), отставать нельзя, расхождение тоже отказ: два разных ответа на один
    вопрос круг не закрывает.
    """
    def gitout(*args):
        return subprocess.run(["git"] + list(args), cwd=str(ROOT), capture_output=True,
                              text=True).stdout.strip()
    branch = gitout("rev-parse", "--abbrev-ref", "HEAD")
    if branch in ("", "HEAD"):
        print("  HEAD отвязан (проверка идёт на merge-ref pull request) — сверка с именем ветки "
              "пропущена: сверяется содержимое, а не указатель")
        return 0
    ls = gitout("ls-remote", "origin", "refs/heads/" + branch).split()
    rsha = ls[0] if ls else ""
    if not rsha:
        # Отсутствие имени на origin — две причины, и называть второй первую ложная подпись:
        # (а) ветку не пушили; (б) её слили — GitHub удаляет head-ref при мерже, а локальный
        # указатель спокойно лежит в main. Отказ в обоих случаях один и тот же (сверять не с
        # чем), но причина рисуется сверкой с origin/main, а не памятью о круге.
        lsha0 = gitout("rev-parse", "HEAD")
        merged = bool(lsha0) and subprocess.run(
            ["git", "merge-base", "--is-ancestor", lsha0, "refs/remotes/origin/main"],
            cwd=str(ROOT), capture_output=True).returncode == 0
        if merged:
            # Правка 17: первая формулировка этого случая («после мержа») сама оказалась догадкой —
            # свежая ветка, вырезанная от main и ещё не запущенная, даёт тот же ref-слепок. По
            # одному ref git не различает эти причины, поэтому печатаются обе, а не та, что
            # вчера казалась единственной.
            print(f"  на origin нет refs/heads/{branch}: локальная ветка ({lsha0[:7]}) целиком лежит в "
                  "origin/main — причин две и по ref не отличить: либо ветка слита и GitHub удалил "
                  "head-ref при мерже, либо она свежа и ещё не запушена; обе законны, сверять не с чем")
            return 0
        print(f"  на origin нет refs/heads/{branch} — круг ещё не пушил ветку, сверять не с чем")
        return 0
    lsha = gitout("rev-parse", "HEAD")
    if rsha == lsha:
        print(f"  ветка {branch} совпадает с origin ({lsha[:7]}) — указатель там, где и обещал")
        return 0
    if subprocess.run(["git", "cat-file", "-e", rsha + "^{commit}"], cwd=str(ROOT),
                      capture_output=True).returncode != 0:
        print(f"ОТКАЗ СРЕДЫ: на origin/{branch} лежит {rsha[:7]}, а в локальном репозитории такого "
              "коммита нет — история не достана, и снятые числа относятся не к этому дереву")
        print(f"  достать: git -c gc.auto=0 fetch --deepen 3000 origin {branch} && git fetch origin "
              f"+refs/heads/{branch}:refs/sandbox/head && git reset --hard {rsha[:7]} && "
              "git update-ref -d refs/sandbox/head")
        return 1
    if subprocess.run(["git", "merge-base", "--is-ancestor", rsha, "HEAD"], cwd=str(ROOT),
                      capture_output=True).returncode != 0:
        behind = int(gitout("rev-list", "--count", "HEAD.." + rsha) or 0)
        ahead = int(gitout("rev-list", "--count", rsha + "..HEAD") or 0)
        if ahead == 0:
            print(f"ОТКАЗ СРЕДЫ: локальная {branch} отстаёт от origin/{branch} на {plural_ru(behind)} — "
                  "указатель сдвинулся под кругом, и снятые в таком дереве числа относились бы к "
                  "прошлому кругу, хотя файлы этого лежат на диске и для git выглядят лишними")
            print(f"  вернуть ветку к залитому: git fetch origin +refs/heads/{branch}:refs/sandbox/head "
                  f"&& git reset --hard {rsha[:7]} && git update-ref -d refs/sandbox/head")
        else:
            print(f"ОТКАЗ СРЕДЫ: локальная {branch} разошлась с origin/{branch}: назад на "
                  f"{plural_ru(behind)} и вперёд на {plural_ru(ahead)}")
            print(f"  разобрать руками: git log --oneline HEAD..{rsha[:7]} и git log --oneline "
                  f"{rsha[:7]}..HEAD — потом решить, какое дерево считать кругом")
        return 1
    print(f"  локальная {branch} опережает origin/{branch} ({lsha[:7]} против {rsha[:7]}) — "
          "незапушенный коммит середины круга, это законно")
    return 0


def unexpected_dirty(before):
    now = set(dirty_paths())
    fresh = now - before
    return sorted(p for p in fresh if p not in ALLOWED_DIRTY)


def plan():
    print("порядок закрытия круга (исполняется именно так, порядок — часть определения чисел):")
    steps = [
        ("шаг −1: годна ли среда",
         f"{PY} -B scripts/atonement_round_close.py --preflight, затем --selfcheck",
         "новый круг открывается в клоне глубиной в один коммит; в нём правило 20 и сверка зеркал "
         "обязаны объявить недоказуемость, а не молча пройти. `--preflight` — то же самое, но "
         "без десяти секунд чтения корпуса: им открывается круг, потому что за ночь песочница "
         "успевает откатиться, а `git status` об этом молчит (круг 65, правка 11)"),
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
        ("проб истории (внутри --verify, или вручную)",
         f"{PY} -B {PROBE} HEAD --selftest",
         "сверяемые числа не должны реагировать на рост истории; в неполном клоне — отказ словами, "
         "а не молчание; ловушка проба подтверждается на каждом запуске, ~30 секунд; способ отчёта "
         "сверяется отдельно и дёшево: `--verdicts` (коды 0/1/2 не должны путаться между собой)"),
        ("сверка пост-фактум после мержа",
         f"{PY} -B scripts/atonement_round_close.py --verify origin/main",
         "после слияния `--run` краснеет законно: реестр описывает прежнее дерево. Для слитого среза "
         "этот режим зовёт доказательство и проб истории одними читающими шагами и ничего не пишет"),
    ]
    for i, (what, cmd, why) in enumerate(steps, 1):
        print(f" {i}. {what}\n      {cmd}\n      — {why}")
    print("\nсам этот инструмент проверяется так:")
    print(f"      {PY} -B scripts/atonement_round_close.py --selfcheck")
    print(f"      {PY} -B {PROBE} HEAD --selftest""  — проб истории зовётся и здесь: замкнутый на себе "
          "инструмент, который никто не вызывает, перестанет ловить незаметно")
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
    # ловушка правила дат — шаг самопроверки, а не факультатив: смягчённое правило без посадочного
    # места тихо вырождается в молчание, и «0 расхождений из 0» тогда выглядит успехом
    code, _ = sh([RESHOOT[0], "--rule-trap"], "ловушка правила дат, реестр стражей сверок, "
                                             "ловушка таблицы 9.1, ловушка съёмки дерева и "
                                             "ломка собственного исходника: "
                                             "незаконный порядок пойман, законный молчит, каждая "
                                             "сверка объявлена со стражем или с причиной дыры, "
                                             "посаженная ячейка, ослеплённый обход и чужой корень "
                                             "пойманы, каждая поломка названа текстом")
    bad += [] if code == 0 else ["ловушка правил и реестр стражей"]
    if bad:
        print("САМОПРОВЕРКА КРУГА: РАСХОЖДЕНИЕ — " + ", ".join(bad))
        return 1
    print("САМОПРОВЕРКА КРУГА: всё зелёное — гейт, пересъёмщик, реестр локаторов, перекрёстная "
          "сверка, ловушка правил пересъёмщика (дат, реестр стражей, таблица 9.1, дерево, ломка исходника)")
    return 0


def verify(ref: str) -> int:
    """Сверка пост-фактум, которой не нужен слепой шаг 4 (круг 65).

    После слияния `--run` краснеет законно: реестр описывает дерево *до* мержа, а не после. Честная
    проверка слитого состояния — только читающими шагами по удалённому указателю. До сих пор для этого
    приходилось помнить, что доказательство вызывается вручную, а проб истории не вызывался нигде:
    он молодой инструмент, а инструмент, который CI не зовёт, живёт до первого удобного рефакторинга.
    Эта ветка собирает читающие шаги в один и ничего не пишет. Разница с `--run` видна в имени: здесь
    нечего подтверждать, здесь есть на что посмотреть."""
    print(f"--- сверка пост-фактум на {ref}: ничего не пишется ---")
    if preflight() != 0:
        return 2
    print("--- шаг 1: читающая часть на рабочем дереве ---")
    if selfcheck() != 0:
        return 1
    print(f"--- шаг 2: доказательство на чистом клоне {ref} ---")
    code, _ = sh(f"bash {PROOF} {ref}", "полное доказательство в дереве из remote; сколько шагов — "
                                      "печатает сам отчёт, здесь числа не держат")
    if code != 0:
        print("СВЕРКА ОТКАЗАЛА: доказательство красное — на слитом срезе это дефект круга, а не шум")
        return 1
    print(f"--- шаг 3: проб истории на том же срезе {ref} ---")
    code, _ = sh([PROBE, ref, "--selftest"], "среды из одного дерева: дрейфа сверяемых чисел нет, "
                                             "отказ назван словами")
    if code == 2:
        print("СВЕРКА ОТКАЗАЛА: проб не смог собрать среды — это не «всё хорошо», это «не проверено»")
        return 2
    if code != 0:
        print("СВЕРКА ОТКАЗАЛА: проб истории увидел реакцию сверяемых чисел на рост истории — "
              "список лежит в выводе шага 3 дословно")
        return 1
    print(f"ПОСЛЕ СЛИЯНИЯ: {ref} сверен читающими шагами — гейт, пересъёмщик, реестр локаторов, "
          "доказательство, проб истории; реестр не тронут, слепой шаг 4 для этого среза не требуется")
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
            # Правка 19: отказ измеряется, а не додумывается. Круг 68 упёрся в мёртвую петлю:
            # таблица §9.1 отредактирована руками вперёд блока claimsPerRegistry, пересъёмщик
            # сверяет таблицу с блоком и отказывает общими словами о дрейфе — а лечение есть и
            # оно одно: блок регистрируется до пересъёма. Диагноз читает ту же сверку, что
            # отказала, и печатает готовую команду, как preflight печатает лечение для shallow.
            _, chk = sh([RESHOOT[0], "--check"], "диагноз: какая именно сверка красная")
            if "- §9.1" in chk:
                print("  измеренная причина: таблица §9.1 разошлась с блоком claimsPerRegistry — "
                      "блок отстаёт от прозы, а сверка читает блок. Блок регистрируется до "
                      "пересъёма: python3 -B scripts/atonement_claim_register.py --write root "
                      "— затем повторите --run. Если после неё §9.1 всё ещё красная, красна "
                      "сама таблица, и эту правку смотрят руками; если красное в другом месте — "
                      "это дрейф, и его ищут так же, как иск до правки 19")
            return 1
        code, rout = sh([REGISTER[0], "--write", "root"], "локаторы §9.1 после правки документа")
        # у реестра список служебных маркеров сверяется *до* записи, поэтому виток, на котором проза
        # назвала новый жаргон, обязан быть красным и одновременно записать свежий список: судить
        # должна следующая читающая сверка (шаг 8), а не этот код. Проглотить же отказ что-либо
        # писать — значит закрыть круг с чужим списком в реестре, поэтому условие именно «записал»
        if code != 0 and ("записан в atonement-corpus-v1.json" not in rout or "Traceback" in rout):
            print("НЕ ЗАКРЫТО: реестр локаторов отказался писать или сломался (код %d) — он не "
                  "переснял блок; это чинится не вторым прогоном" % code)
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
        code, _ = sh(f"bash {PROOF} {args.with_proof}", "полное доказательство в дереве из remote")
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
    ap.add_argument("--preflight", action="store_true",
                    help="только годность среды: shallow, origin/main и совпадение ветки с залитым "
                         "указателем — дешёвая проверка, с которой круг обязан начинаться")
    ap.add_argument("--selfcheck", action="store_true", help="только читающая часть")
    ap.add_argument("--run", action="store_true", help="отработать порядок целиком")
    ap.add_argument("--with-battery", action="store_true", help="внутри --run добавить батарею мутаций")
    ap.add_argument("--with-proof", metavar="REF", default="",
                    help="внутри --run добавить доказательство на чистом клоне ref")
    ap.add_argument("--verify", metavar="REF", nargs="?", const="origin/main", default="",
                    help="сверка пост-фактум на залитом срезе: только читающие шаги, зовёт и "
                         "доказательство, и проб истории; единственный честный режим сразу после мержа")
    ap.add_argument("--allow-appending-writers", action="store_true",
                    help="разрешить двух писателей, дописывающих записи")
    ap.add_argument("--confirm-circle", metavar="N", default="",
                    help="номер круга, которым подтверждается разрешение писателей")
    args = ap.parse_args()
    if args.preflight:
        return preflight()
    if args.verify:
        return verify(args.verify)
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
          "[--with-proof REF]] | --verify [REF] [--allow-appending-writers --confirm-circle N]")
    return 2


if __name__ == "__main__":
    sys.exit(main())
