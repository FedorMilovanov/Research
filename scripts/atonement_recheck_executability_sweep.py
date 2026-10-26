#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Съём исполнимости обещаний пересъёма в корпусе ланы ИСКУПЛЕНИЕ (круг 57).

Критерий тот же, что объявлен в fourPointMassRegistry20261023.recheckExecutabilityRound5620261026:
упоминание = вхождение [.]scratch/[A-Za-z0-9_./-]+ в строковое значение; нечитаемое = пути нет ни
в дереве, ни в снимке; поле приказное, если его имя recheckCommand, command, артефакт или how;
объявление утраты, если в том же значении стоит одно из перечисленных ниже слов.

Чем этот инструмент отличается от разового обхода круга 56: число нечитаемых зависит от того,
виден ли в клоне снимок. В клоне глубиной в один коммит `git cat-file -e ceabb56ea:<путь>` падает
на всех путях сразу, и 19 превращаются в 29 — без единого изменения в данных. Такой обход здесь
не выдаёт привычное число молча, а говорит отдельным вердиктом и отдельным кодом выхода.

Второе отличие: утверждения вида «в снимок этого не попало» и «восстанавливается из снимка»
проверяются, а не читаются на веру. Полю, которое обещает пересъём и называет снимок, инструмент
сопоставляет его утверждение с фактом и при разночтении пишет ДЕФЕКТ.

exit 0 — расхождений нет; 1 — найдены дефектные поля или разночтения со снимком;
2 — снимок недоступен в этом клоне (числа несравнимы, молча не проходим).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys

CORPUS_DEFAULT = "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
PROSE_DEFAULT = (
    "docs/research/atonement/35_four_point_authors_mass_registry.md",
    "docs/research/atonement/README.md",
)
RX = re.compile(r"[.]scratch/[A-Za-z0-9_./-]+")
IMPER = ("recheckCommand", "command", "артефакт", "how")
DECL = ("не исполнимы", "не исполнимо", "не ложились", "не попали", "утрачены",
        "не пересъёмно", "не входят", "только из снимка")
SELF = ("mkdir -p", "fetch ")
ABSENT_MARKS = ("не попали", "отсутствуют", "ни q5", "не пересъёмно", "не исполнимо",
                "не исполнимы", "не ложились", "его нет", "там нет")
PRESENT_MARKS = ("git archive", "восстанавли", "прочитан из снимка", "из снимка песочницы",
                 "лежат в снимк", "восстановим")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(("git",) + args, capture_output=True, text=True)


def gh(*args: str) -> subprocess.CompletedProcess:
    """Канал GitHub API: разрешает ref на сервере, поэтому глубина локального клона ему не указ."""
    return subprocess.run(("gh",) + args, capture_output=True, text=True)


def clone_depth() -> tuple[bool, int]:
    shallow = git("rev-parse", "--is-shallow-repository").stdout.strip() == "true"
    out = git("rev-list", "--count", "HEAD")
    try:
        n = int(out.stdout.strip())
    except ValueError:  # noqa: BLE001 - не репозиторий: глубину не узнать, это не ошибка съёма
        n = -1
    return shallow, n


def snapshot_alive(snap: str) -> bool:
    return git("cat-file", "-t", snap).returncode == 0


def ref_in_snapshot(snap: str, ref: str) -> bool:
    return git("cat-file", "-e", f"{snap}:{ref.rstrip('.,;:)')}").returncode == 0


def ref_in_tree(ref: str) -> bool:
    return os.path.exists(ref.rstrip(".,;:)"))


def net_channel_for(val: str, ref: str) -> bool:
    """Исполнимо ли обещание переснять ИМЕННО этот путь вне клона.

    Считать исполнимым только потому, что в тексте встретился api.github.com, нельзя: так любой
    упомянутый URL превратил бы дефект в проход. Требуем, чтобы путь был назван внутри адреса
    содержимого (contents/<путь>) и чтобы рядом стоял ref снимка — тогда команда разрешит именно
    этот объект на сервере, где глубина локального клона ни при чём.
    """
    esc = re.escape(ref)
    if not re.search(r"contents/" + esc + r"(?![A-Za-z0-9_./-])", val):
        return False
    return "?ref=" in val or "ref=" in val


def leaves(node, path=""):
    if isinstance(node, dict):
        for key, val in node.items():
            yield from leaves(val, path + "/" + str(key))
    elif isinstance(node, list):
        for i, val in enumerate(node):
            yield from leaves(val, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", default=CORPUS_DEFAULT)
    ap.add_argument("--prose", nargs="*", default=list(PROSE_DEFAULT))
    ap.add_argument("--snapshot", default="ceabb56ea",
                    help="снимок, из которого когда-то восстанавливалась песочница")
    ap.add_argument("--allow-unreachable", action="store_true",
                    help="не считать недоступный снимок ошибкой (тогда числа помечаются как несравнимые)")
    ap.add_argument("--repo", default="FedorMilovanov/Research", help="владелец/репозиторий для канала api")
    ap.add_argument("--list", action="store_true", help="перечислить пути и их класс")
    ap.add_argument("--cross-check", action="store_true",
                    help="для каждого пути сверить два канала: клон (git cat-file по снимку) и "
                         "api.github.com (contents по тому же ref); расхождением считается только "
                         "несовпадение каналов, а не мелкий клон сам по себе")
    ap.add_argument("--json", action="store_true", help="машинный вывод одной строкой")
    args = ap.parse_args()

    if not os.path.isfile(args.corpus):
        print(f"съём не исполним: корпуса нет по пути {args.corpus}", file=sys.stderr)
        return 1
    data = json.loads(io.open(args.corpus, encoding="utf-8").read())
    lv = dict(leaves(data, "корпус"))

    corp_m = [m for v in lv.values() for m in RX.findall(v)]
    prose_m = []
    for f in args.prose:
        if os.path.isfile(f):
            prose_m += [m for line in io.open(f, encoding="utf-8") for m in RX.findall(line)]
    strip = lambda xs: [x.rstrip(".,;:)") for x in xs]  # noqa: E731
    paths = sorted(set(strip(corp_m + prose_m)))

    shallow, depth = clone_depth()
    alive = snapshot_alive(args.snapshot)
    unreadable = [p for p in paths if not ref_in_tree(p) and not (alive and ref_in_snapshot(args.snapshot, p))]
    recoverable = [p for p in paths if alive and ref_in_snapshot(args.snapshot, p)]

    imper = []
    for path, val in sorted(lv.items()):
        if path.rsplit("/", 1)[-1] not in IMPER:
            continue
        for ref in sorted({m.rstrip(".,;:)") for m in RX.findall(val)}):
            if ref in unreadable:
                if net_channel_for(val, ref):
                    kind = "сетевойКанал"
                elif any(k in val for k in DECL):
                    kind = "объявление"
                elif any(k in val for k in SELF):
                    kind = "самоготовится"
                else:
                    kind = "ДЕФЕКТ"
                imper.append((ref, path, kind))
    bykind: dict[str, int] = {}
    for _r, _p, k in imper:
        bykind[k] = bykind.get(k, 0) + 1
    def_fields = sorted({p for _r, p, k in imper if k == "ДЕФЕКТ"})

    # утверждения о снимке: проверяем полярность там, где поле её явно называет
    claims = []
    for path, val in sorted(lv.items()):
        if args.snapshot not in val:
            continue
        says_absent = any(k in val for k in ABSENT_MARKS)
        says_present = any(k in val for k in PRESENT_MARKS)
        if says_absent == says_present:
            verdict = "не разобрано (полярность не названа явно)" if says_absent else "нет явного утверждения"
            claims.append((path, verdict, None))
            continue
        for ref in sorted({m.rstrip(".,;:)") for m in RX.findall(val)}):
            if not alive:
                claims.append((path, "не проверено: снимок недоступен", ref))
                continue
            have = ref_in_snapshot(args.snapshot, ref)
            ok = (not have) if says_absent else have
            claims.append((path, "совпало" if ok else "РАСХОЖДЕНИЕ", ref, ok))
    bad_claims = [c for c in claims if len(c) == 4 and not c[3]]
    unchecked = [c for c in claims if c[1].startswith("не проверено")]

    cross = None
    if args.cross_check:
        rows = []
        for p_ in paths:
            in_clone = alive and ref_in_snapshot(args.snapshot, p_)
            api = gh("api", f"repos/{args.repo}/contents/{p_}?ref={args.snapshot}", "--jq", ".size")
            in_api = api.returncode == 0
            api_size = int(api.stdout.strip()) if in_api and api.stdout.strip().isdigit() else None
            clone_size = None
            if in_clone:
                cs = git("cat-file", "-s", f"{args.snapshot}:{p_}")
                clone_size = int(cs.stdout.strip()) if cs.returncode == 0 else None
            agree = (in_clone == in_api) and (not in_clone or clone_size == api_size)
            rows.append({"путь": p_, "вКлоне": in_clone, "вApi": in_api,
                         "байтКлон": clone_size, "байтApi": api_size, "совпало": agree})
        both = sum(1 for r in rows if r["вКлоне"] and r["вApi"])
        gone = sum(1 for r in rows if not r["вКлоне"] and not r["вApi"])
        mism = [r for r in rows if not r["совпало"]]
        cross = {"путей": len(rows), "вобоихКаналах": both, "ниводном": gone, "расхождений": len(mism),
                 "строки": mism[:6]}

    res = {
        "клон": {"shallow": shallow, "глубина": depth},
        "снимок": {"id": args.snapshot, "доступен": alive},
        "корпус": {"упоминаний": len(strip(corp_m)), "различныхпутей": len(set(strip(corp_m))),
                   "нечитаемых": len([p for p in unreadable if p in set(strip(corp_m))])},
        "корпусИПроза": {"упоминаний": len(strip(corp_m + prose_m)), "различныхпутей": len(paths),
                        "нечитаемых": len(unreadable), "возвратимыхИзСнимка": len(recoverable)},
        "приказныеВхождения": len(imper), "разбивка": bykind,
        "дефектныхПолей": len(def_fields), "поля": def_fields,
        "утвержденияОСнимке": {"всего": len(claims), "незадокументированныхСверок": len(unchecked),
                              "расхождений": len(bad_claims)},
        "сверкаКаналов": cross,
    }
    if args.json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(f"клон: shallow={shallow} глубина={depth} | снимок {args.snapshot}: "
              f"{'доступен' if alive else 'НЕДОСТУПЕН'}")
        k = res["корпус"]
        print(f"корпус: упоминаний {k['упоминаний']} | различных путей {k['различныхпутей']} | "
              f"нечитаемых {k['нечитаемых']}")
        a = res["корпусИПроза"]
        print(f"корпус+проза: упоминаний {a['упоминаний']} | путей {a['различныхпутей']} | "
              f"нечитаемых {a['нечитаемых']} | возвратимых из снимка {a['возвратимыхИзСнимка']}")
        print(f"приказные вхождения: {res['приказныеВхождения']} {bykind or {}} | "
              f"ДЕФЕКТНЫХ ПОЛЕЙ: {res['дефектныхПолей']}")
        if cross:
            print(f"сверка двух каналов: путей {cross['путей']} | в обоих (размер совпал) "
                  f"{cross['вобоихКаналах']} | ни в одном (утрачено подтверждённо) {cross['ниводном']} | "
                  f"РАСХОЖДЕНИЙ каналов {cross['расхождений']}")
            for r in cross["строки"]:
                print("   РАСХОЖДЕНИЕ КАНАЛОВ:", r)
        u = res["утвержденияОСнимке"]
        print(f"утверждений о снимке: {u['всего']} | не проверено (снимок недоступен): "
              f"{u['незадокументированныхСверок']} | РАСХОЖДЕНИЙ: {u['расхождений']}")
        for c in bad_claims:
            print("   РАСХОЖДЕНИЕ:", c[1], "по", c[2], "в", c[0].replace("корпус/", ""))
        for d in def_fields:
            print("   ДЕФЕКТНОЕ ПОЛЕ:", d.replace("корпус/", ""))
        if args.list:
            for p in paths:
                mark = "нечитаем" if p in unreadable else ("в снимке" if p in recoverable else "в дереве")
                print(f"   {mark:10} {p}")
        if not alive and not args.allow_unreachable:
            print(f"\nВЕРДИКТ: снимок {args.snapshot} в этом клоне не найден (глубина {depth}, "
                  f"shallow={shallow}); обход по этому критерию считает нечитаемым каждый путь сразу "
                  f"({a['нечитаемых']} вместо меньшего числа: расхождение равно ровно количеству путей, "
                  "которые живут в снимке). Числа несравнимы с записанными, и притворяться сравнимыми не "
                  "будут: разверните клон (git fetch --unshallow) либо переснимайте утверждения о снимке "
                  "через api.github.com (git/trees и blobs по ref) — этот канал работает из клона любой "
                  "глубины. Для прогона вслепую: --allow-unreachable.")

    if bad_claims or def_fields:
        return 1
    if not alive and not args.allow_unreachable:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
