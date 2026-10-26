#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проб возмущением истории: проверяет, что числа реестра относятся к дереву, а не к клону (круг 65).

Круг 63 опубликовал в реестре число объектов git, видимых при съёме, и оно покраснело на смёрженном
main: верно для своей среды, бесполезно как сверка. Круг 64 закрыл тот же класс правилом по имени поля
(ENV_MARK в пересъёмщике). Имя — слабое место: счётчик, названный иначе, проходит незамеченным. Этот
проб делает то же утверждение поведением, а не лексикой: он собирает три среды над одним и тем же
деревом и требует, чтобы числа вели себя согласно своему объявлению.

Среды (все — отдельные клоны проверяемого репозитория, канон не трогается ни в одном режиме):
  E1 контроль   полная история, origin/main = main, от которого идёт ref. Ожидание: гейт PASS,
                `--check` пересъёмщика PASS.
  E2 возмущение то же дерево, но `origin/main` сдвинут вперёд на один пустой коммит (история выросла,
                файлы проверяемого ref не изменились). Ожидание: обе проверки так же PASS. Любая
                строка расхождения здесь — число, которое зависит от истории, но ведёт себя как число
                дерева: именно оно и есть дефект, и он назван словом, а не угадан по имени поля.
  E3 неполнота  клон глубиной в один коммит, без origin/main. Ожидание обратное: обе проверки обязаны
                ОТКАЗАТЬ и назвать причину словами про shallow/недостающую ссылку. Молчаливый PASS в
                такой среде — тот же грех, что и тихое «совпало» над пустым обходом; шаг и поставлен,
                чтобы молчание не вернулось вместе с починкой.

Употребление: `python3 -B scripts/atonement_history_perturbation_probe.py [ref] [--selftest] [--keep]`.
ref — тот репозиторий, в котором лежит проб (по умолчанию его HEAD), поэтому вызов из чистого клона
проверяет чистый клон, а не песочницу автора круга.

Самопроверка `--selftest` обязана быть у инструмента, который обещает ловить. В E1 вносится намеренный
дефект: число объектов обхода возвращается в реестр, а пересъёмщик этого клона учится его писать и
сверять — под именем, которое правило круга 64 по имени поля не ловит (ни одна метка ENV_MARK в нём не
встречается). Затем E1 закрывается своим `--write`, и число становится честным замером своей среды.
Ожидание: E1 зелёная, а E2 — те же байты скрипта, корпуса и прозы, но `origin/main` на один коммит
длиннее — краснеет ровно этим полем (пустой коммит добавляет ровно один объект). Если ловушка не
сработала, проб не имеет права выдавать зелёный вердикт: он печатает «ловушка не подтверждена» и выходит
с кодом 1. Если E2 покраснеет чем-то ещё — проб так и пишет: «найдено сверх ловушки», и это уже не
самопроверка, а найденный дефект.

Выход: 0 — все ожидания совпали; 1 — есть расхождение ожидания с поведением; 2 — проб не смог
построить среду (нет git, клон упал, ref не разрешается) — это не «проверка пройдена», и код отдельный
ровно для того, чтобы его нельзя было спутать с успехом.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESHOOT = "scripts/atonement_reshoot_state.py"
GATE = "scripts/validate_atonement_corpus_integrity.py"
CORPUS_REL = "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
ENV_TOKEN = re.compile(r"shallow|недоста|нет локального|не видит ни одного коммита|пересъём невозможен",
                       re.I)


def git(cwd, *args, check=True):
    r = subprocess.run(("git", "-c", "core.quotepath=off") + args, cwd=str(cwd),
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} → {r.returncode}: {r.stderr.strip()[:160]}")
    return r.stdout.strip()


def run_tool(cwd, script, *args):
    """Инструмент запускается СВОЙ, из клона: пересъёмщик вычисляет корень по положению файла,
    поэтому запустить канонский скрипт из песочницы в каталоге клона — значит измерить не клон."""
    r = subprocess.run([sys.executable, "-B", str(Path(cwd) / script), *args], cwd=str(cwd),
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + ("\n" + r.stderr if r.stderr.strip() else "")).rstrip()


def make_clone(src, dest, *, depth=None, want_main=True):
    """Клон из песочницы обязан принести и `origin/main`: если песочница сама была неполной или
    клонирована по HEAD, ссылки на main в ней не будет, и E1 станет не контрольной средой, а
    поломанной — с молчаливой пропущенной проверкой правила 20."""
    cmd = ["clone", "-q", "--no-local"]
    if depth:
        cmd += [f"--depth={depth}"]
    cmd += [f"file://{src}", str(dest)]
    git(src, *cmd)
    if want_main and not git(dest, "rev-parse", "--verify", "-q", "origin/main", check=False):
        git(dest, "fetch", "-q", "origin", "+refs/heads/main:refs/remotes/origin/main", check=False)
    if want_main and not git(dest, "rev-parse", "--verify", "-q", "origin/main", check=False):
        # источник может знать main только как remote-tracking (клон по HEAD, как в песочнице этого
        # круга, или чистый клон, где local `main` не создаётся); тогда указатель переносится явно —
        # объект в клоне с полной историей уже есть, а отказать здесь означало бы назвать неполной
        # среду, в которой проб просто не угадал способ хранения ссылки
        src_main = (git(src, "rev-parse", "--verify", "-q", "refs/remotes/origin/main", check=False) or "").strip()
        # "-e" ничего не печатает и потому неразличима через git(..., check=False): проверяем тип
        if src_main and git(dest, "cat-file", "-t", src_main, check=False) != "commit":
            src_main = ""
        if src_main:
            git(dest, "update-ref", "refs/remotes/origin/main", src_main, check=False)
    if want_main and not git(dest, "rev-parse", "--verify", "-q", "origin/main", check=False):
        raise RuntimeError(f"в клоне {Path(dest).name} нет refs/remotes/origin/main — среда не собрана "
                           "(источник не знает main никак; в песочнице: git fetch -q origin "
                           "+refs/heads/main:refs/remotes/origin/main, предварительно --deepen)")


class Env:
    def __init__(self, name, path, note):
        self.name, self.path, self.note = name, Path(path), note

    def verdict(self):
        gcode, gout = run_tool(self.path, GATE)
        rcode, rout = run_tool(self.path, RESHOOT, "--check")
        return {"среда": self.name, "гейт": gcode, "пересъём": rcode,
                "строки": [l.strip() for l in (gout + "\n" + rout).split("\n")
                           if l.lstrip().startswith("- ") or "PASS" in l or "FAIL" in l],
                "вывод": gout + "\n" + rout}

    def snapshot_objects(self):
        out = git(self.path, "rev-list", "--objects", "origin/main")
        return len([l for l in out.split("\n") if l])


def build(src, work):
    """E1 → E2 → E3. Все три — независимые клоны одного источника: среды обязаны различаться ровно
    тем, что объявлено (полнота истории и наличие `origin/main`), а не тем, откуда их клонировали."""
    e1 = Path(work) / "e1"
    make_clone(src, e1)
    head = git(src, "rev-parse", "HEAD")
    git(e1, "checkout", "-q", head)
    e2 = Path(work) / "e2"
    # E2 собирается клоном из того же источника, а не из E1: клон переносит только refs/heads/*, а `main` в E1
    # живёт как remote-tracking — из E1 вторая среда получила бы иную картину ссылок, чем первая, и
    # сравнение меряло бы разницу клонирования, а не задуманное возмущение истории
    make_clone(src, e2)
    base = git(e2, "rev-parse", "--verify", "origin/main")
    git(e2, "branch", "-f", "probe-main", base)
    git(e2, "checkout", "-q", "probe-main")
    git(e2, "-c", "user.name=probe", "-c", "user.email=probe@invalid", "commit", "-q", "--allow-empty",
        "-m", "проб круга 65: main вырос на коммит, дерево проверяемого ref не изменилось")
    new = git(e2, "rev-parse", "HEAD")
    git(e2, "update-ref", "refs/remotes/origin/main", new)
    git(e2, "checkout", "-q", head)
    e3 = Path(work) / "e3"
    make_clone(src, e3, depth=1, want_main=False)
    git(e3, "checkout", "-q", head)
    return (Env("E1 контроль", e1, "полная история, origin/main = base"),
            Env("E2 возмущение", e2, f"origin/main сдвинут на 1 коммит ({base[:7]} → {new[:7]})"),
            Env("E3 неполнота", e3, "клон глубины 1, origin/main отсутствует"))


TRAP_FIELD = "обход" + "Видел" + "Объектов"
DOC_REL = "ИСКУПЛЕНИЕ/18_SERIES_AUDIT_AND_ARCS_2026-10-26.md"


def trap(e1, e2):
    """Ловушка для самого проба.

    В клон E1 возвращается число объектов обхода: пересъёмщик этого клона учится его писать и
    сверять, а имя поля выбрано так, чтобы правило по имени (ENV_MARK, круг 64) его не поймало —
    ни одна метка в нём не встречается. Затем E1 закрывается своим же `--write`, и число становится
    честным замером своей среды: `--check` обязан остаться зелёным. E2 получает ровно те же байты
    скрипта, корпуса и прозы, но другой `origin/main` — на один коммит больше. Ожидание: E2 краснеет
    этим полем и ничем больше. Если покраснеет чем-то ещё — это уже не ловушка, а найденный дефект:
    число, объявленное деревом, оказалось числом истории.

    Канон ловушка не трогает: всё живёт во временных клонах и после прогона удаляется.
    """
    n = e1.snapshot_objects()
    sp = Path(e1.path) / RESHOOT
    src = sp.read_text(encoding="utf-8")
    cmp_anchor = '        if sc.get("byBlock") != n["sha"]["byBlock"]:'
    wrt_anchor = '        sc["byBlock"] = n["sha"]["byBlock"]'
    if src.count(cmp_anchor) != 1 or src.count(wrt_anchor) != 1:
        return ("ловушка не установлена: якоря сверки и записи найдены как "
                + str(src.count(cmp_anchor)) + " и " + str(src.count(wrt_anchor))
                + " — структуру пересъёмщика надо читать заново")
    inj = [
        '        _g = sc.get("' + TRAP_FIELD + '")',
        "        if _g != n['sha']['gitObjectsConsidered']:",
        "            drift.append('shaCitationAudit20261023." + TRAP_FIELD + ": ' + repr(_g)",
        "                         + ' против обхода ' + repr(n['sha']['gitObjectsConsidered']))",
    ]
    patched = src.replace(cmp_anchor, "\n".join(inj) + "\n" + cmp_anchor)
    patched = patched.replace(wrt_anchor,
                              wrt_anchor + '\n        sc["' + TRAP_FIELD + '"] = n["sha"]["gitObjectsConsidered"]')
    try:
        compile(patched, str(sp), "exec")
    except SyntaxError as exc:
        return "ловушка не установлена: сгенерированная правка не компилируется (" + str(exc) + ")"
    sp.write_text(patched, encoding="utf-8")
    wcode, _wout = run_tool(e1.path, RESHOOT, "--write")
    if wcode != 0:
        return "ловушка не установлена: `--write` пропатченного клона не сошёлся (код " + str(wcode) + ")"
    if TRAP_FIELD not in (Path(e1.path) / CORPUS_REL).read_text(encoding="utf-8"):
        return "ловушка не установлена: `--write` пропатченного клона не записал поле в реестр"
    for rel in (RESHOOT, CORPUS_REL, DOC_REL):
        shutil.copy2(Path(e1.path) / rel, Path(e2.path) / rel)
    a, aout = run_tool(e1.path, RESHOOT, "--check")
    b, bout = run_tool(e2.path, RESHOOT, "--check")
    d1 = [l.strip() for l in aout.split("\n") if l.lstrip().startswith("- ")]
    d2 = [l.strip() for l in bout.split("\n") if l.lstrip().startswith("- ")]
    if a != 0:
        return "ловушка не подтверждена: E1 красная (код %d): %s" % (a, " / ".join(d1)[:170] or "пусто")
    if b == 0 or not any(TRAP_FIELD in l for l in d2):
        return ("ЛОВУШКА НЕ ПОДТВЕРЖДЕНА: в E2 поле истории не вызвало расхождения (код %d, "
                "расхождения: %s) — зелёный вердикт проб выдавать не вправе" % (b, d2[:2]))
    extra = [l for l in d2 if TRAP_FIELD not in l]
    if extra:
        return "найдено сверх ловушки: в E2 покраснели ещё и эти числа — " + " / ".join(extra)[:200]
    return None


def plural(n: int, one: str, few: str, many: str) -> str:
    """Русская форма после числа — не косметика: отчёт, который пишет «в 1 случаях», читается как
    вывод, снятый с чужого шаблона, а шаблон здесь и есть то, чему доверяют."""
    n %= 100
    if 11 <= n <= 14:
        return many
    return one if n == 1 else (few if 2 <= n <= 4 else many)


def decide(broken: bool, bad: int, nchecks: int) -> tuple:
    """Итог проба — чистая функция, и `--verdicts` проверяет именно её.

    Три выхода обязаны различаться словами. Первая версия кодировала «среда не годна» тем же
    счётчиком, что и найденные расхождения (bad = 2), из-за чего два законных находки печатались как
    «среду использовать нельзя» — найденный дефект прятался за шумом и просил ещё один прогон вместо
    правки. Режим `--verdicts` дёшев именно потому, что обязан запускаться всегда: способ отчёта
    отучается быстрее, чем успеваешь заметить."""
    if broken:
        return 2, "ПРОБ ИСТОРИИ: СРЕДА НЕГОДНА — это не проверка"
    if bad:
        return 1, (f"ПРОБ ИСТОРИИ: {plural(bad, 'расхождение', 'расхождения', 'расхождений')} {bad} "
                   f"из {nchecks} {plural(nchecks, 'проверки', 'проверок', 'проверок')} — "
                   "среда собрана, вывод читается выше дословно")
    return 0, ("ПРОБ ИСТОРИИ: PASS — ни одно сверяемое число не отреагировало на рост истории; "
               "в неполном клоне отказ назван словами")


def verdicts() -> int:
    cases = (
        ((True, 2, 6), (2, "СРЕДА НЕГОДНА"), "отказ среды не притворяется находкой"),
        ((False, 2, 6), (1, "расхождения 2 из 6"), "две находки не притворяются отказом среды"),
        ((False, 1, 5), (1, "расхождение 1 из 5 проверок"), "одна находка названа одним"),
        ((False, 0, 5), (0, "ПРОБ ИСТОРИИ: PASS"), "тишина — это успех, а не молчание"),
    )
    bad = 0
    for args, (want_code, want_phrase), name in cases:
        code, text = decide(*args)
        ok = code == want_code and want_phrase in text and (("СРЕДА НЕГОДНА" in text) == (code == 2))
        bad += check(name, ok, "" if ok else f"код {code} (ждался {want_code}): {text[:70]}")
    print("ПРОБ ИСТОРИИ: ВЕРДИКТЫ — " + ("способ отчёта различает находку, успех и непригодную среду"
                                        if bad == 0 else f"отчёт сломан в {bad} случаях"))
    return 0 if bad == 0 else 1


def check(name, ok, detail=""):
    print(f"  {'OK ' if ok else '!! '}{name}{'' if not detail else ' — ' + detail}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="atonement_history_perturbation_probe.py")
    # ref — позиционный: проб вызывают и из замыкающего порядка, и из доказательства, и руками;
    # в двух из этих мест он пишется внутри строки команды, где `--ref` только путает
    ap.add_argument("ref", nargs="?", default="HEAD",
                    help="что проверять: sha или имя (по умолчанию HEAD — тот репозиторий, "
                         "в котором лежит проб)")
    ap.add_argument("--verdicts", action="store_true",
                    help="проверить только способ отчёта (коды 0/1/2 и их формулировки), клонов не "
                         "строить; дёшево, поэтому вызывается вместе с остальными шагами")
    ap.add_argument("--selftest", action="store_true",
                    help="установить в клоны намеренный дефект и потребовать, чтобы ловушка сработала")
    ap.add_argument("--keep", action="store_true", help="не удалять рабочие клоны (для разбора вывода)")
    args = ap.parse_args()
    if args.verdicts:
        return verdicts()
    try:
        src = Path(REPO).resolve()
        head = git(src, "rev-parse", args.ref)
    except Exception as exc:  # noqa: BLE001 - среда непригодна, это отдельный код выхода
        print(f"СРЕДА НЕГОДНА: {exc}")
        return 2
    work = Path(tempfile.mkdtemp(prefix="atonement-probe65."))
    bad = 0
    # «не годна среда» и «найдено два расхождения» — разные слова и разные коды; см. decide()
    broken = False
    try:
        e1, e2, e3 = build(src, work)
        nchecks = 6 if args.selftest else 5
        print(f"проб истории: ref {head[:7]}, три среды в {work.name}")
        v1, v2, v3 = e1.verdict(), e2.verdict(), e3.verdict()
        bad += check("E1 — контроль: гейт и пересъём зелёные",
                     v1["гейт"] == 0 and v1["пересъём"] == 0,
                     f"гейт {v1['гейт']}, пересъём {v1['пересъём']}")
        drift2 = [l for l in v2["строки"] if l.startswith("- ")]
        bad += check("E2 — то же дерево при выросшей истории остаётся зелёным",
                     v2["гейт"] == 0 and v2["пересъём"] == 0,
                     "расхождения: " + ("; ".join(drift2)[:180] if drift2 else "нет"))
        print("     · E1: " + (" | ".join(v1["строки"])[:190] or "тишина"))
        print("     · E2: " + (" | ".join(v2["строки"])[:190] or "тишина"))
        print("     · E3: " + (" | ".join(v3["строки"])[:190] or "тишина"))
        silent = not ENV_TOKEN.search(v3["вывод"])
        bad += check("E3 — неполный клон обязан отказать и назвать среду словами",
                     (v3["гейт"] != 0 or v3["пересъём"] != 0) and not silent,
                     f"гейт {v3['гейт']}, пересъём {v3['пересъём']}, "
                     + ("молчит — это дефект" if silent else "причина названа"))
        n1, n2 = e1.snapshot_objects(), e2.snapshot_objects()
        bad += check("обход E2 действительно видит больше объектов (возмущение настоящее)", n2 > n1,
                     f"{n1} → {n2}")
        if args.selftest:
            # собственный сбой проба не имеет права притворяться «средой, в которой нельзя проверить»:
            # у него свой вердикт и свой код, иначе сломанный инструмент переживёт ещё один круг
            try:
                why = trap(e1, e2)
            except Exception as exc:  # noqa: BLE001
                print(f"  !! ПРОБ СЛОМАН внутри ловушки: {type(exc).__name__}: {exc}")
                bad += 1
            else:
                bad += check("ловушка: невидимая правилу по имени история ловится поведением E2",
                             why is None, why or "")
        v1num = re.findall(r"\d+", " ".join(v1["строки"]))
        v2num = re.findall(r"\d+", " ".join(v2["строки"]))
        bad += check("набор чисел в PASS-строках совпал между E1 и E2", v1num == v2num,
                     "" if v1num == v2num else f"{v1num[:6]}… против {v2num[:6]}…")
    except Exception as exc:  # noqa: BLE001
        print(f"СРЕДА НЕГОДНА: {type(exc).__name__}: {exc}")
        broken = True
    finally:
        if args.keep:
            print(f"клоны оставлены: {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)
    code, text = decide(broken, bad, nchecks)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
