#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Пересъём чисел, которые живут в двух местах сразу: реестр корпуса и срез в аудите.

Смысл появления этого файла — авария, описанная в разделе 9.3 аудита: круг 61 носил счётчики
в скрипте `scripts/atonement_close_round.py`, круг 62 его унаследовал, а вместе с незапушенным
коммитом круга 62 скрипт пропал (проверяется двумя командами: `git cat-file -t fe39288` и
`git ls-remote origin | grep ba50183d`). Числа остались — и тут же протухли: в строке
«Индекс библиотеки» документа 18 стояло 123 записи при 124 в дереве.

Значит, «производитель чисел» обязан быть не только в дереве, но и под проверкой. Отсюда две
меры, обе в этом файле:
  • `--check` ничего не пишет и падает с кодом 1 на любом расхождении — он добавлен шаг в
    workflow `atonement-corpus-integrity.yml`, то есть протухшее число теперь блокирует мерж;
  • `--write` переснимает и применяет, сходя к неподвижной точке (документ меняется → размер
    корпуса меняется → числа дерева в корпусе меняются → строка документа про размеры дерева
    меняется снова).

Определения взяты у того, кто проверяет, а не сочинены заново:
  • ценз индекса — правило 25 гейта (записи; уникальные `file`; уникальные `folder`;
    `role == material`; материалы с непустым `locator`; счётчики по `rights` и `readState`;
    сумма `driveBytes`; максимум `driveBytes`; `len(scope.indexedFolders)`);
  • аудит sha-ссылок — правило 20 гейта (токен = `[0-9a-f]{7,40}`, целиком из цифр — не токен;
    достижимость меряется по локальному `origin/main` без сети; при shallow или отсутствии
    ссылки блок пересъёмки молча пропускается, ровно как молчит гейт — но молчание печатается);
  • счётчик штампованных полей — правила (1)+(2b) гейта: поле словаря с ключом
    `at|measuredAt|checkedAt|measuredOn|measuredAtGit`, по всем machine-реестрам;
  • леджер — файл `ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md`: запись = заголовок `## C-NN.`,
    статус = строка `**Status:** X` (8 лексикон, из них машиночитаемых меньше: часть записей
    описана словами);
  • срезы дерева — те же глобы, что печатает таблица §1: `docs/research/atonement/*.md`,
    `ИСКУПЛЕНИЕ/*.md`, `ИСКУПЛЕНИЕ/<лан>/*.md`, `ИСКУПЛЕНИЕ/synthesis/drafts/*.md`,
    `ИСКУПЛЕНИЕ/data/*`, реестр массы `35_` (строка-носитель = строка вида `| FP-NNN |`,
    раздел круга = строка вида `## `).

Размерности, объявленные явно, потому что они менялись: «строк» = сколько в файле переводов
строк (`text.count("\\n")`), «КБ» = байт / 1000 (min до десятой, max до целого) — так строка
документа воспроизводится дословно, а не «уточняется» задним числом.
"""

from __future__ import annotations

import collections
import glob
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-corpus-v1.json"
INDEX = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-library-index.json"
DOC = ROOT / "ИСКУПЛЕНИЕ" / "18_SERIES_AUDIT_AND_ARCS_2026-10-26.md"
LEDGER = ROOT / "ИСКУПЛЕНИЕ" / "synthesis" / "02_CONFLICT_LEDGER.md"
SUBLANES = ("ot", "nt", "fathers", "synthesis")
STAMP = re.compile(r"^(?:at|measuredAt|checkedAt|measuredOn|measuredAtGit)$")
CIRCLE = "64"
# дата в именах блоков этого скрипта — дата круга, а не дата файла: ключ вида reshootCounters…
# обязан говорить, когда его снимали, иначе следующий круг читал бы чужую отметку как свою.
# Имена чужих блоков — `seriesAuditRound58…`, `cardProseCrossCheck…r60` — этим не двигаются:
# они принадлежат своим кругам и своим владельцам. Дата берётся по UTC, потому что штампы `measuredAt` пишет `date -u`: блок, названный одним днём и отмеченный другим,
# лжёт о себе так же, как число, сочинённое вместо снятого. Сверяется это проверкой
# `keydate_audit` ниже, а не внимательностью автора круга.
KEY_DATE = "20261026"


def num(n) -> str:
    """Как в документе: разделитель разрядов — обычный пробел (не `format(n," ")`, который
    печатает ведущий пробел у однозначных и даёт «|  129 085 |» вместо «| 129 085 |»)."""
    return f"{int(n):,}".replace(",", " ")


def plural(n, one, few, many):
    r = n % 100
    k = n % 10
    if 10 <= r <= 20 or k in (0, 5, 6, 7, 8, 9):
        return many
    if k == 1:
        return one
    return few


def git(*args):
    return subprocess.run(("git", "-c", "core.quotepath=off") + args, cwd=str(ROOT),
                          capture_output=True, text=True)


# ------------------------------------------------------------------ определения

def stamped_count(node) -> int:
    """Ровно обход правил (1)+(2b): для каждого словаря — сколько в нём ключей этой формы."""
    if isinstance(node, dict):
        return sum(1 for k in node if STAMP.match(str(k))) + sum(stamped_count(v) for v in node.values())
    if isinstance(node, list):
        return sum(stamped_count(v) for v in node)
    return 0


def index_census(idx: dict) -> dict:
    """Ценз — обход правила 25 гейта, дословно: «файл» = запись с kind == "file", а не
    множество имён; байты берутся из поля `bytes` файловых записей."""
    recs = idx["records"]
    files = [r for r in recs if r.get("kind") == "file"]
    mats = [r for r in recs if r.get("role") == "material"]
    return {
        "records": len(recs),
        "files": len(files),
        "folders": len([r for r in recs if r.get("kind") == "folder"]),
        "materials": len(mats),
        "materialsWithLocators": len([r for r in mats if str(r.get("locator") or "").strip()]),
        "byRights": dict(sorted(collections.Counter(str(r.get("rights")) for r in recs).items())),
        "byReadState": dict(sorted(collections.Counter(str(r.get("readState")) for r in recs).items())),
        "driveBytesSum": sum(int(r.get("bytes") or 0) for r in files),
        "largestBytes": max([int(r.get("bytes") or 0) for r in files] or [0]),
        "scopeFolders": len(set((idx.get("scope") or {}).get("indexedFolders") or [])),
    }


SHA_TOKEN = re.compile(r"\b[0-9a-f]{7,40}\b")


def sha_token_paths(obj) -> dict:
    """{токен: [пути]} — фильтр правила 20: длина ровно 7, 8 или 40, и не все цифры."""
    out = {}

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + "." + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, "%s[%d]" % (p, i))
        elif isinstance(o, str):
            for m in SHA_TOKEN.findall(o):
                if len(m) not in (7, 8, 40) or re.fullmatch(r"[0-9]+", m):
                    continue
                out.setdefault(m, []).append(p)

    walk(obj, "")
    return out



QUOTED_MD = re.compile(r"«[^»]*»|`[^`]*`|\"[^\"]*\"")
QUOTED_JSON = re.compile(r"«[^»]*»")
EXEMPT = "<!-- mixed-script:цитата-дефекта -->"
MASS_FILE = ROOT / "docs" / "research" / "atonement" / "35_four_point_authors_mass_registry.md"
LEDGER_MD = LEDGER
DEPT = ROOT / "ИСКУПЛЕНИЕ"


def mixed_words(text: str):
    """Склеенные кириллица+латиница — токен целиком, цитаты в «ёлочках», `обратных кавычках` и \"\" вырезаны.
    Определение — строка 772 гейта, правится синхронно с ним."""
    bare = QUOTED_MD.sub(" ", text)
    return [w for w in re.findall(r"[^\W\d_]+", bare)
            if re.search(r"[А-Яа-яЁё]", w) and re.search(r"[A-Za-z]", w)]


def json_leaf_scan():
    """Правило 19 (JSON-листья): обход всех JSON отдела, своё и чужое, плюс число прочитанных файлов."""
    own, foreign, scanned = [], [], 0
    for jp in sorted(DEPT.rglob("*.json")):
        try:
            data = json.loads(jp.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 - нечитаемый JSON ловят другие проверки
            continue
        scanned += 1
        hits = []

        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items():
                    walk(v, path + "." + str(k))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, "%s[%d]" % (path, i))
            elif isinstance(o, str):
                hits.extend((path, w) for w in mixed_words(QUOTED_JSON.sub(" ", o)))

        walk(data, "")
        if jp == CORPUS:
            own.extend(hits)
        else:
            foreign.extend(str(jp.relative_to(ROOT)) + q for q, w in hits for _ in [0])
    return {"ownOccurrences": len(own), "scannedFiles": scanned, "foreignOccurrences": len(foreign),
            "own": own[:3], "foreign": foreign[:3]}


def out_of_scope_mixed():
    """mixedScriptCheck.outOfScope: чужой периметр (всё под ИСКУПЛЕНИЕ/, кроме корня отдела)."""
    files, occ = set(), 0
    for md in sorted(DEPT.rglob("*.md")):
        if md.parent == DEPT:
            continue
        for line in md.read_text(encoding="utf-8", errors="replace").split("\n"):
            if EXEMPT in line:
                continue
            w = mixed_words(line)
            if w:
                files.add(str(md.relative_to(ROOT)))
                occ += len(w)
    return {"occurrences": occ, "files": len(files)}


def ledger_svodki():
    """строка сводки = то, что напечатано под «## Итоговая сводка» как строка таблицы (строка 186 гейта)."""
    text = LEDGER_MD.read_text(encoding="utf-8")
    at = text.find("## Итоговая сводка")
    if at < 0:
        return 0
    out, started = [], False
    for line in text[at:].split("\n")[1:]:
        if line.startswith("|"):
            out.append(line.rstrip())
            started = True
        elif started and line.strip() == "":
            break
    return len([x for x in out if x.startswith("| `")])


def mass_counts():
    """Правило 23: строка реестра = `^| FP-NN |`, очередь = `^- Q-NN —`; считаются разные номера."""
    txt = MASS_FILE.read_text(encoding="utf-8", errors="replace")
    rows = {m.group(1) for m in (re.match(r"^\|\s*FP-(\d+)\s*\|", ln) for ln in txt.split("\n")) if m}
    queue = {m.group(1) for m in (re.match(r"^- Q-(\d+) —", ln) for ln in txt.split("\n")) if m}
    return len(rows), len(queue)


def sha_audit(reg: dict):
    """Правило 20 целиком. None — если среда не годна (shallow или нет локального origin/main):
    тогда блок не переснимается, и `--check` об этом говорит вслух вместо тихого совпадения."""
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != "false":
        return None
    base = git("rev-parse", "--verify", "-q", "origin/main").stdout.strip()
    if not base:
        return None
    objs = git("rev-list", "--objects", base).stdout
    full = sorted({line.split(" ")[0] for line in objs.split("\n") if line})
    import bisect

    def reachable(tok):
        k = bisect.bisect_left(full, tok)
        return k < len(full) and full[k].startswith(tok)

    toks = sha_token_paths(reg)
    dead = {t for t in toks if not reachable(t)}
    fields_dead = {}
    for tok in dead:
        for pth in toks[tok]:
            top = pth.lstrip(".").split(".")[0].split("[")[0]
            fields_dead[top] = fields_dead.get(top, 0) + 1
    total = len(toks)
    # число мёртвых полей = сколько путей ведут на мёртвые токены (правило 20: sum(len(toks[t])) for t in dead),
    # а не «сколько блоков»: блок может содержать десять таких путей
    npaths = sum(len(toks[t]) for t in dead)
    return {
        "gitObjectsConsidered": len(full),
        "uniqueShaTokens": total,
        "reachableTokens": total - len(dead),
        "unreachableTokens": len(dead),
        "fieldsWithDeadLinks": npaths,
        "byBlock": fields_dead,
        "note": ("блок integrityGate.shaCitationAudit20261023 переснят scripts/atonement_reshoot_state.py "
                 "тем же обходом, каким его меряет правило 20 гейта: {н} токенов длины 7/8/40, живых {ж}, "
                 "мёртвых {м}, мёртвых полей {ф}. Мёртвые не правятся и не удаляются — они и есть предмет "
                 "проверки: ссылка на объект, переживший только squash-историю, обязана иметь пересъём через "
                 "запись. Достижимость меряется по локальному origin/main без сети: на shallow-клоне блок "
                 "не исполняется, и прогон обязан это напечатать").format(
                    н=total, ж=total - len(dead), м=len(dead), ф=npaths),
    }


def tree_counts(root=None) -> dict:
    """Числа дерева — снятые с того корня, который назван.

    `root` нужен ловушке (круг 65, правка 13): чтобы проверить, что сверяемые числа относятся к
    дереву, а не к месту, где скрипт случайно лежал, обход должен уметь пройтись по *другому*
    дереву. Без этого «числа не шевелятся, потому что их берут из кэша» и «числа не шевелятся,
    потому что дерево не менялось» — одно и то же наблюдение, и отличить их было нечем.
    """
    root = ROOT if root is None else Path(root)

    def rel(path: Path) -> Path:
        return root / path.relative_to(ROOT)

    def stat(paths):
        ps = [Path(x) for x in paths]
        return len(ps), sum(x.stat().st_size for x in ps)

    lane_glob = str(rel(ROOT / "docs" / "research" / "atonement")) + "/*.md"
    docs = stat(sorted(glob.glob(lane_glob)))
    n_num = len([x for x in glob.glob(lane_glob) if re.search(r"/\d\d_", x)])
    rootmd = stat(sorted(glob.glob(str(rel(ROOT / "ИСКУПЛЕНИЕ")) + "/*.md")))
    b17 = rel(ROOT / "ИСКУПЛЕНИЕ" / "17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md").stat().st_size
    doc = rel(DOC)
    docbytes = doc.stat().st_size
    doclines = len(doc.read_text(encoding="utf-8").split("\n")) - 1
    docmd5 = hashlib.md5(doc.read_bytes()).hexdigest()
    per = {}
    for lan in SUBLANES:
        per[lan] = stat(sorted(glob.glob(str(rel(ROOT / "ИСКУПЛЕНИЕ" / lan)) + "/*.md")))
    sub = (sum(v[0] for v in per.values()), sum(v[1] for v in per.values()))
    dr_paths = sorted(glob.glob(str(rel(ROOT / "ИСКУПЛЕНИЕ" / "synthesis" / "drafts")) + "/*.md"))
    dr = stat(dr_paths)
    dr_lines = sum(Path(x).read_text(encoding="utf-8").count("\n") for x in dr_paths)
    dr_lines_split = sum(len(Path(x).read_text(encoding="utf-8").split("\n")) for x in dr_paths)
    dr_sizes = [Path(x).stat().st_size for x in dr_paths]
    data = stat(sorted(glob.glob(str(rel(ROOT / "ИСКУПЛЕНИЕ" / "data")) + "/*")))
    corp_bytes = rel(CORPUS).stat().st_size
    idx_bytes = rel(INDEX).stat().st_size
    mass_path = rel(ROOT / "docs" / "research" / "atonement" / "35_four_point_authors_mass_registry.md")
    mass = mass_path.read_text(encoding="utf-8")
    mass_bytes = mass_path.stat().st_size
    return {
        "docs": docs, "docsNumbered": n_num, "rootmd": rootmd, "b17": b17,
        "doc": (docbytes, doclines, docmd5), "perLan": per, "sub": sub,
        "drafts": dr, "draftsLines": dr_lines, "draftsLinesSplit": dr_lines_split,
        "draftsMin": round(min(dr_sizes) / 1000, 1) if dr_sizes else 0,
        "draftsMax": round(max(dr_sizes) / 1000) if dr_sizes else 0,
        "data": data, "corpBytes": corp_bytes, "idxBytes": idx_bytes,
        "massBytes": mass_bytes, "massRows": len(re.findall(r"^\|\s*FP-\d+\s*\|", mass, re.M)),
        "massSections": len(re.findall(r"^## ", mass, re.M)),
    }


def ledger_counts() -> dict:
    """Запись = заголовок `## C-NN.`; машиночитаемый статус = строка вида
    `- **Статус:** \\`OPEN\\`` внутри записи. Порядок разбивки: по убыванию числа, внутри —
    по первому появлению в файле (иначе «8 RESOLVED-BY-TEXT, 6 OPEN …» воспроизводится, а не
    пересобирается алфавитом на глазах)."""
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    entries = sorted({m.group(1) for m in (re.match(r"^## C-(\d+)\.", ln) for ln in lines) if m}, key=int)
    order, cnt = [], collections.Counter()
    for ln in lines:
        m = re.match(r"^- \*\*Статус:\*\* `([A-Z][A-Z-]*)`", ln)
        if m:
            s_ = m.group(1)
            if s_ not in cnt:
                order.append(s_)
            cnt[s_] += 1
    ranked = sorted(cnt.items(), key=lambda kv: (-kv[1], order.index(kv[0])))
    return {"записей": len(entries), "первый": entries[0] if entries else "00",
            "последний": entries[-1] if entries else "00", "статусов": sum(cnt.values()),
            "разбивка": ", ".join("%d `%s`" % (n, s_) for s_, n in ranked)}



def draft_paths() -> list:
    """Полное зеркало каталога черновиков: пути относительно корня, в сортировке обхода.
    Дуга III (п. 3.14): поле `synthesis.drafts` в под-регистре перечисляло один файл из каталога и
    не объявляло назначения — либо отсталое зеркало, либо список «на память». С этого круга его
    пишет и сверяет тем же обходом тот же скрипт, что и леджер-строку документа."""
    return sorted(Path(x).relative_to(ROOT).as_posix() if Path(x).is_absolute() else x
                  for x in glob.glob(str(ROOT / "ИСКУПЛЕНИЕ" / "synthesis" / "drafts") + "/*.md"))


def mirror_audit(corp: dict) -> dict:
    """Записи `driveMirrors.corpusSnapshotRound*` обязаны сходиться со своим blob'ом, а обещанный
    разрыв с деревом — равняться текущему размеру файла минус размер слепка. Это то, что круг 62
    делал внутри утраченного финализатора; здесь оно стало отдельной функцией, потому что
    «зеркало на Drive» — единственный класс записей, который гейт иначе проверяет только
    «по самим себе» (правило 25 сравнивает поля записи между собой, а не с git и не с listing'ом)."""
    out = {"проверено": 0, "неПрочитано": [], "bad": [], "gap": {}, "записей": 0}
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != "false":
        out["неПрочитано"].append("клон shallow — blob'ы снимков не читаются, сверка зеркал не исполнена")
        return out
    for k, v in sorted((corp.get("driveMirrors") or {}).items()):
        if not k.startswith("corpusSnapshotRound") or not isinstance(v, dict):
            continue
        out["записей"] += 1
        ls = v.get("живойСлепок") or {}
        sha, path = ls.get("gitShaAtUpload"), CORPUS.relative_to(ROOT).as_posix()
        if not sha:
            out["bad"].append(f"driveMirrors.{k}: нет gitShaAtUpload — сверять не с чем")
            continue
        r = git("show", f"{sha}:{path}")
        if r.returncode != 0:
            out["неПрочитано"].append(f"driveMirrors.{k}: blob {sha[:7]} не читается в этом клоне "
                                      "(не «расхождение», а отсутствие истории — пропечатать, а не молчать)")
            continue
        raw = r.stdout.encode()
        out["проверено"] += 1
        md5 = hashlib.md5(raw).hexdigest()
        for field, want in (("байт", len(raw)), ("md5Drive", md5), ("md5Git", md5)):
            if field in ls and ls[field] != want:
                out["bad"].append(f"driveMirrors.{k}.живойСлепок.{field} = {ls[field]!r}, blob {sha[:7]} "
                                  f"даёт {want!r}")
        if "gitFileLinesAtUpload" in ls:
            ln = raw.count(b"\n")
            if ls["gitFileLinesAtUpload"] != ln:
                out["bad"].append(f"driveMirrors.{k}.живойСлепок.gitFileLinesAtUpload = "
                                  f"{ls['gitFileLinesAtUpload']}, blob даёт {ln}")
        if "снятПрогоном" in (v.get("разрывСДеревом") or {}):
            gap = CORPUS.stat().st_size - len(raw)
            out["gap"][k] = gap
    return out


# ------------------------------------------------------------------ числа обхода (круг 64)
#
# Класс дефекта, пойманный доказательством круга 63: в реестр попало число, которое меряет не дерево,
# а клон, — сколько объектов git увидел обход. Такое число верно в момент съёма и краснеет после
# всякого мержа, потому что сравнивается с чужой средой. Доказать «это число о дереве» нельзя, а вот
# заставить его назваться — можно: имя поля говорит, что оно считает обход, и тогда ему разрешены три
# места — штамп прогона, объявленный список, или ничто.

ENV_MARK = ("gitobjects", "объектовв", "объектовсъёма", "коммитовв", "revlist", "rev-list",
            "обходоввсего", "файловвобходе", "строквобходе")
ENV_PASS = ("пересняткругом", "удалённыефигуры", "снятпрогоном")
# Периметр правила — не «весь реестр», а ровно те поля, которые пересъёмщик сверяет: покраснеть
# само может только то, что с чем-то сравнивается. Исторические записи, которым сверять не с чем
# (перечисления папок Drive в записях `driveMirrors.massRegistry20261023.*`), сюда не входят — и
# не по снисхождению, а потому, что они не дрейфуют: их никто не перечитывает.
ENV_SCOPES = ("integrityGate.shaCitationAudit20261023.*", "integrityGate.mixedScriptCheck.jsonLeafScan.*",
              "integrityGate.mixedScriptCheck.outOfScope.*",
              "integrityGate.scopeOfMeasurementRules.stampedFieldsPerRegistry.*",
              "libraryIndex20261023.*", "fourPointMassRegistry20261023.seriesAuditRound5820261026.*",
              "reproducibility20261022.countsLive.*", "reproducibility20261022.pipelineScripts*.файлы.*",
              "driveMirrors.*.разрывСДеревом.*")
ENV_DECL_PREFIX = "environmentScopedNumbers"


def path_match(path, pattern):
    """Совпадение пути с шаблоном, где `*` закрывает ровно один сегмент (`[0]` в имя сегмента входит)."""
    p, q = path.split("."), pattern.split(".")
    if len(q) > len(p):
        return False
    for got, want in zip(p, q):
        if want == "*":
            continue
        if want != got.split("[")[0]:
            return False
    return True


def in_env_scope(path):
    return any(path_match(path, pat) for pat in ENV_SCOPES)


def resolve(node, dotted):
    """Путь вида `блок.подблок.поле` → значение или None. Не исключение: мёртвое объявление — тоже
    ответ, и он должен быть виден, а не утонуть в traceback."""
    for part in str(dotted).split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def env_declared(corp):
    """Объявленные числа обхода: путь → записка. Собирается объединением по всем круговым блокам:
    снять чужое объявление этим кругом значило бы поправить чужой блок рукой, а переопределить его
    можно только своим блоком и со своим «почему»."""
    out = {}
    for holder in (corp.get("integrityGate") or {}, corp.get("reproducibility20261022") or {}):
        for key in sorted(holder):
            if key.startswith(ENV_DECL_PREFIX):
                block = holder[key] or {}
                for path, note in sorted((block.get("поля") or {}).items()):
                    out[path] = note
    return out


PIPELINE_FILES = ("scripts/validate_atonement_corpus_integrity.py", "scripts/atonement_claim_register.py",
                  "scripts/run_atonement_mutation_battery.py", "scripts/atonement_reshoot_state.py",
                  "scripts/atonement_drive_mirror_round63.py", "scripts/atonement_library_index_round63.py",
                  "scripts/atonement_round_close.py",
                  "scripts/atonement_history_perturbation_probe.py",
                  "scripts/atonement_drive_mirror_round66.py", "scripts/atonement_library_index_round66.py")


ENV_DECL_BLOCK = ENV_DECL_PREFIX + KEY_DATE + "r" + CIRCLE
# блоки, которые этот скрипт имеет право править; вне них незаконное поле только объявляется,
# а снимает его владелец — снимать чужие поля рукой тот же грех, что и затирать чужой метод
ENV_OWNED = ("integrityGate.", "libraryIndex20261023", "fourPointMassRegistry20261023.seriesAudit",
             "reproducibility20261022.")


def env_scan(corp):
    """Съём чисел обхода: где они стоят и какие объявления о них живы.

    Возвращает незаконные поля (число, названное счётчиком обхода, стоит вне штампа прогона и вне
    объявленного списка), мёртвые объявления (список ссылается на несуществующее поле) и живые
    объявления — тем же словарём, каким их пишет `apply_corpus`, чтобы сверка сравнивала два
    одинаковых обхода, а не обход с памятью автора круга."""
    declared = env_declared(corp)
    leaves, in_pass, illegal, dead, live = [], [], [], [], {}

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                pth = f"{path}.{k}" if path else str(k)
                if isinstance(v, bool):
                    continue
                if isinstance(v, (int, float)):
                    parts = [part.split("[")[0].lower() for part in pth.split(".")]
                    if in_env_scope(pth) and any(m in str(k).lower() for m in ENV_MARK):
                        if any(any(q in part for q in ENV_PASS) for part in parts):
                            in_pass.append((pth, v))
                        else:
                            leaves.append((pth, v))
                else:
                    walk(v, pth)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, "%s[%d]" % (path, i))

    walk(corp, "")
    for pth, _v in leaves:
        if pth not in declared:
            illegal.append(pth)
    for pth in sorted(declared):
        if resolve(corp, pth) is None:
            dead.append(pth)
        else:
            live[pth] = declared[pth]
    return {"обходных": len(leaves) + len(in_pass), "вШтампеПрогона": len(in_pass),
            "объявлено": len(live), "живые": live, "незаконные": illegal,
            "мертвыеОбъявления": dead, "пути": [pth for pth, _v in leaves + in_pass]}


OWNED_BLOCK_RX = re.compile(r"(reshootCounters|pipelineScripts|countsNote|environmentScopedNumbers)"
                              r"(\d{8})r(\d+)$")


def keydate_audit(corp):
    """Имя блока против его же штампа: дату в имени нельзя ставить задним числом.

    Возвращает (проверено, расхождения) — и то и другое идёт в сверку: круг, который переименовал
    блок, но не переставил отметку, обязан быть пойман машиной. Круг 65 смягчил формулировку с
    равенства на порядок: первая версия требовала совпадения дат, из-за чего корпус краснел в 00:00
    UTC — всякая ночная пересъёмка ставила в `measuredAt` новые сутки под блоком, названным вчера,
    и единственной починкой было бы переименование ключей с осиротевшими предками (круг 64 потерял
    так четыре блока). Обман эта версия ловит тот же: блок, названный датой *позже* его штампа,
    значит, что дату придумали для числа, которое так ещё не снимали."""
    bad, checked = [], 0

    def walk(node, path):
        nonlocal checked
        if isinstance(node, dict):
            m = OWNED_BLOCK_RX.search(str(path).split(".")[-1])
            if m:
                checked += 1
                stamp = str(node.get("measuredAt") or "")[:10].replace("-", "")
                # сравнение порядка, а не равенства: переснять блок позже, чем его назвали, законно
                # (для свежей даты есть `переснятоПрогоном`), а вот назвать его датой, которой он ещё
                # не был снят, — ровно тот жест, против которого правило и заводилось
                if stamp and int(stamp) < int(m.group(2)):
                    bad.append(f"{path}: имя блока датировано {m.group(2)}, а штамп — {stamp}: дату "
                               "в имени нельзя ставить задним числом (блок назван свежее, чем снят); "
                               "обратный порядок законен — пересъёмка позже имени обновляет только штамп)")
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    walk(v, f"{path}.{k}" if path else str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                if isinstance(v, (dict, list)):
                    walk(v, "%s[%d]" % (path, i))

    walk(corp, "")
    return checked, bad


# Реестр стражей сверок (круг 65, правка 9). Каждая функция-сверка этого файла обязаналибо быть
# объявленной с названным местом, где её кусают посаженным нарушением,либо быть объявленной дырой с
# причиной. Смысл не в том, чтобы вести список, а в том, чтобы список нельзя было забыться: новая
# сверка без стража поднимает ловушку, старый страж, которого в названном файле уже нет, — тоже.
PLANT_SOURCES = {
    "сам": Path(__file__),
    "гейт": ROOT / "scripts" / "validate_atonement_corpus_integrity.py",
    "проб истории": ROOT / "scripts" / "atonement_history_perturbation_probe.py",
    "доказательство": ROOT / "scripts" / "atonement_proof_round63.sh",
    "батарея": ROOT / "scripts" / "run_atonement_mutation_battery.py",
}
# имя сверки -> (источник стража, маркер в нём) либо ("нет", причина, по которой дыра терпима)
PLANTED_GUARDS = {
    "keydate_audit": ("сам", "ЛОВУШКА ПРАВИЛА ДАТ"),
    "env_scan": ("проб истории", "ПРОБ ИСТОРИИ"),
    "sha_audit": ("проб истории", "недостижим"),
    "json_leaf_scan": ("доказательство", "ловит внедрённое число среды"),
    "index_census": ("доказательство", "ценз индекса"),
    "pipeline_inventory": ("доказательство", "инвентарь инструментов"),
    "mirror_audit": ("гейт", "правило 25"),
    "mass_counts": ("гейт", "правило 23"),
    "ledger_svodki": ("гейт", "statusVocabulary"),
    "ledger_counts": ("гейт", "conflict ledger"),
    "tree_counts": ("сам", "ЛОВУШКА ДЕРЕВА"),
    "check_table_91": ("сам", "ЛОВУШКА ТАБЛИЦЫ 9.1"),
    # Найдена правкой 17: сверка, которая называлась вне соглашения и десять кругов обходила
    # реестр. Посаженного отделения под неё нет — почему это дыра, а не упущение, написано в
    # самой причине: она обязана называться, а не выглядеть как «всё объявлено».
    "diff_state_scan": ("нет", "сверка закрытия без собственного посадочного отделения: ослепить её — "
                        "краснеют независимые обходы (доказательство: инвентарь канона, разрыв зеркала, "
                        "байты аудита; гейт: правила 27/28 своим съёмом), но поломки, посаженной "
                        "именно в ней, не существует — дыра объявлена и видна по счётчику"),
}
SCAN_SUFFIXES = ("_audit", "_counts", "_census", "_scan", "_svodki", "_inventory")
SCAN_PREFIXES = ("check_",)

# Вне соглашения — только поимённо и с причиной (правка 17). Три ведра делят все вызываемые
# имена модуля: сверка (совпало с соглашением → PLANTED_GUARDS), ловушка (`_trap`, их форма
# собственная: исполняются `--rule-trap` и грепами workflow) и это — объявленные несверки.
# Никакого четвёртого «тихого» ведра нет: имя вне всех трёх поднимает `plant_registry_trap`.
# Причина у каждой своя и с измеримым якорем (правка 18): названная в ней функция обязана
# существовать в этом файле и звать это имя в своём теле — иначе ловушка краснеет словами
# о ложной причине, а не ждёт ревьюера.
SCAN_EXEMPT = {
    "num": "помощник: форматирование числа (неразрывные разряды) внутри строк вердикта; якорь `doc_numbers`",
    "plural": "помощник: русская плюрализация счётчиков в сообщениях и вердиктах; якорь `doc_numbers`",
    "git": "обёртка: чтение git через subprocess; сравнивает ничего, результат отдаёт вызывающему; якорь `sha_audit`",
    "stamped_count": "измеритель: сколько штампованных полей в узле; сравнение — в diff_state_scan и дока-якорях; якорь `registry_numbers`",
    "draft_paths": "измеритель: полное зеркало каталога synthesis/drafts (дуга III, п. 3.14); число берёт агрегатор, "
                   "сверка — в diff_state_scan, запись — в apply_corpus; якорь `registry_numbers`",
    "sha_token_paths": "измеритель: фильтр токенов правила 20; сравнение — в sha_audit; якорь `sha_audit`",
    "mixed_words": "измеритель: строки смешанного письма с вырезанными цитатами; ловит их проверка вызывающего; якорь `out_of_scope_mixed`",
    "out_of_scope_mixed": "измеритель: то же для чужого периметра (поле outOfScope); сравнение — в diff_state_scan; якорь `registry_numbers`",
    "path_match": "помощник: совпадение пути с шаблоном под-лана при обходе; якорь `in_env_scope`",
    "in_env_scope": "помощник: попадание пути в периметр правила среды; решение — в env_scan; якорь `env_scan`",
    "resolve": "помощник: точка-путь → значение (мёртвое объявление резолвится тоже); сверка — в вызывающем; якорь `env_scan`",
    "env_declared": "читатель: объявленные числа обхода по круговым блокам; сравнение — в env_scan; якорь `env_scan`",
    "scan_functions": "обход имён для самого реестра стражей: счётчик для plant_registry_trap, не сверка двух учётов; якорь `plant_registry_trap`",
    "registry_numbers": "агрегатор: собирает числа сверок в один снимок; сравнивает его diff_state_scan; якорь `main`",
    "apply_corpus": "писатель: подставляет измеренные числа в корпус; читает и сравнивает — другие; якорь `main`",
    "doc_numbers": "генератор: (регулярка, строка) для документа; сверка результата — в петле apply/check; якорь `diff_state_scan`",
    "apply_doc": "писатель: применяет сгенерированные строки к документу, отказывается при двух якорях; якорь `main`",
    "report_not_generated": "служебная фраза отчёта о блоках, которые генератор не создаёт; сравнивает ничего; якорь `main`",
    "main": "разбор флагов и вызов шагов; сверок в теле не определено; корневой якорь `main` — его никто не зовёт",
}


def scan_functions():
    """Сверки, которые определяет этот файл, — найденные обходом, а не списком.

    Список руками отстаёт от изобретательности ровно так же, как список запрещённых имён полей
    (круг 64 запретил числа среды по имени — круг 65 запретил их поведением). Здесь обход идёт по
    `globals()`: имя функции кончается на суффикс сверки или начинается на `check_`, и функция
    определена в этом модуле (вложенные `walk` в подсчёт не попадают).

    Предел имени снят правкой 17 — не изобретением более умного имени, а полным разбором: всё
    вызываемое имя модуля обязано попасть в одно из трёх ведёр — сверка (совпало с соглашением,
    значит объявление в PLANTED_GUARDS), ловушка (`_trap`) или SCAN_EXEMPT с причиной. Сверка,
    названная как `audit_claims` или `itog`, отныне не «промолчит», а поднимет реестр словами
    «вне соглашения и вне списка исключений»: раньше этот реестр был назван реестром, а не
    доказательством, и отнимал у забвения только возможность забыть объявить уже названное сверкой;
    теперь он отнимает и возможность просто не назвать. Пределом оставалась ложная причина в
    SCAN_EXEMPT — правка 18 сняла и его измерением: каждая причина обязана назвать якорь (имя
    функции этого файла в обратных кавычках), а ловушка сверяет, что якорь существует, что имя
    действительно зовётся в его теле, а для корневого якоря — что сверок в теле не определено
    и самого корня никто не зовёт. Остаётся предел меры, а не предел имени: якорь доказывает
    присутствие имени в названном теле, но не то, что это присутствие и есть та сверка, о
    которой говорит причина, — эту долю по-прежнему различает читатель diff'а, и строки списка
    написаны с расчётом на него.
    """
    here = globals().get("__name__")
    found = []
    for name, fn in list(globals().items()):
        if not callable(fn) or getattr(fn, "__module__", None) != here:
            continue
        if name == "keydate_trap" or name.endswith(("_trap",)):
            continue    # сами ловушки — не сверки
        if name.startswith(SCAN_PREFIXES) or name.endswith(SCAN_SUFFIXES):
            found.append(name)
    return sorted(found)


def plant_registry_trap():
    """Сверка реестра стражей с тем, что определено в файле: ни дыры без причины, ни стража
    без тела, ни причины без якоря."""
    found = set(scan_functions())
    declared = set(PLANTED_GUARDS)
    if found - declared:
        print("РЕЕСТР СТРАЖЕЙ РАСХОДИТСЯ: определено и не объявлено — %s. Новая сверка обязана "
              "объявить, где её кусают, или быть записанной дырой с причиной"
              % ", ".join(sorted(found - declared)))
        return 1
    if declared - found:
        print("РЕЕСТР СТРАЖЕЙ РАСХОДИТСЯ: объявлено и не найдено обходом — %s. Страж висит на "
              "несуществующей функции: либо свёрка переименована, либо она тихо умерла вместе с "
              "телом, и объявление надо снять руками"
              % ", ".join(sorted(declared - found)))
        return 2
    # Правка 17: три ведра обязаны разбить все вызываемые имена модуля без остатка.
    # D — мёртвое исключение (имени больше нет вне соглашения): тот же хвост, что мёртвый страж,
    # и первым — потому что «исключение для исчезнувшей функции» и «новое имя без ведра» часто
    # рождаются одной правкой, и читать надо сначала ту причину, которую автор видел в прошлом.
    here = globals().get("__name__")
    outsiders = {name for name, fn in list(globals().items())
                 if callable(fn) and getattr(fn, "__module__", None) == here
                 and not (name == "keydate_trap" or name.endswith("_trap"))
                 and not (name.startswith(SCAN_PREFIXES) or name.endswith(SCAN_SUFFIXES))}
    stale_ex = set(SCAN_EXEMPT) - outsiders
    if stale_ex:
        print("РЕЕСТР СТРАЖЕЙ РАСХОДИТСЯ: исключение висит на имени, которого нет вне соглашения — %s. "
              "Либо функции больше нет, либо она переименована в сверку и обязана объявить страж; "
              "мёртвое исключение — тот же хвост, что мёртвый страж, и снять его надо руками"
              % ", ".join(sorted(stale_ex)))
        return 1
    # C — имя вне соглашения и вне исключений: замолчать больше нечем. Новая функция объявляет
    # себя ровно двумя способами, и третий (просто не попасть в список) отныне красный.
    unex = outsiders - set(SCAN_EXEMPT)
    if unex:
        print("РЕЕСТР СТРАЖЕЙ РАСХОДИТСЯ: вне соглашения и вне списка исключений — %s. Новая функция "
              "объявляет себя двумя способами: сверка входит в соглашение и получает страж в "
              "PLANTED_GUARDS, несверка вносится в SCAN_EXEMPT с причиной; третьего молчания нет"
              % ", ".join(sorted(unex)))
        return 1
    # Правка 18: у причины в исключении обязан быть измеримый якорь. Причина обязана назвать
    # хотя бы одну функцию этого файла (имя в обратных кавычках); для каждого названного якоря
    # сверяется, что якорь существует и что исключённое имя действительно зовётся в его теле,
    # а для корневого якоря (имя ссылается на себя) — что сверок в теле не определено и самого
    # корня никто не зовёт. Так ложная причина перестаёт быть уделом одного ревьюера: призрак
    # якоря, якорь без имени и ложный корень краснеют здесь же, с названной причиной.
    def _code_names(code):
        names = set(getattr(code, "co_names", ()))
        for const in getattr(code, "co_consts", ()):
            if hasattr(const, "co_names"):
                names |= _code_names(const)
        return names

    def _nested_scans(code):
        hits = []
        for const in getattr(code, "co_consts", ()):
            if hasattr(const, "co_names"):
                nm = const.co_name
                if (nm.startswith(SCAN_PREFIXES) or nm.endswith(SCAN_SUFFIXES)) and not nm.endswith("_trap"):
                    hits.append(nm)
                hits += _nested_scans(const)
        return hits

    anchors_seen = 0
    anchor_faults = []
    for exempt_name in sorted(SCAN_EXEMPT):
        ids = re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", SCAN_EXEMPT[exempt_name])
        if not ids:
            anchor_faults.append("%s: причина без якоря — не названо ни одной функции-носителя"
                                 % exempt_name)
            continue
        anchors_seen += len(ids)
        own = globals().get(exempt_name)
        for anchor in ids:
            afn = globals().get(anchor)
            if not (callable(afn) and getattr(afn, "__module__", None) == here):
                anchor_faults.append("%s: якорь-призрак — `%s` не найден среди функций этого файла"
                                     % (exempt_name, anchor))
                continue
            if anchor == exempt_name:
                nested = _nested_scans(getattr(own, "__code__", None))
                if nested:
                    anchor_faults.append("%s: сверка определена в теле корня — %s"
                                         % (exempt_name, ", ".join(nested)))
                callers = [g for g, gf in list(globals().items())
                           if hasattr(gf, "__code__") and getattr(gf, "__module__", None) == here
                           and g != exempt_name and exempt_name in _code_names(gf.__code__)]
                if callers:
                    anchor_faults.append("%s: корень зовётся извне — %s"
                                         % (exempt_name, ", ".join(sorted(callers))))
                continue
            if exempt_name not in _code_names(getattr(afn, "__code__", None)):
                anchor_faults.append("%s: имя не зовётся в теле якоря `%s`" % (exempt_name, anchor))
    if anchor_faults:
        print("РЕЕСТР СТРАЖЕЙ РАСХОДИТСЯ: причина без измеримого якоря — " + "; ".join(anchor_faults))
        return 1
    missing, stale, holes = [], [], []
    for name in sorted(declared):
        src, marker = PLANTED_GUARDS[name]
        if src == "нет":
            if not str(marker).strip():
                missing.append("%s: дыра объявлена без причины — молчаливая дыра хуже объявленной" % name)
            holes.append(name)
            continue
        path = PLANT_SOURCES.get(src)
        if path is None or not path.exists():
            stale.append("%s: источник стража %r не найден (%s)" % (name, src, path))
            continue
        if marker not in path.read_text(encoding="utf-8", errors="replace"):
            missing.append("%s: страж назван в %r, но строки «%s» там нет — проверка, на которую "
                           "ссылается объявление, оттуда исчезла" % (name, src, marker))
    if stale:
        print("РЕЕСТР СТРАЖЕЙ НЕИСПОЛНИМ — " + "; ".join(stale))
        return 2
    if missing:
        print("РЕЕСТР СТРАЖЕЙ РАСХОДИТСЯ — " + "; ".join(missing))
        return 1
    print("РЕЕСТР СТРАЖЕЙ: сверок %d, с посаженным нарушением %d, без него %d%s, вне соглашения "
          "объявлено %d, якорей %d — причины названы и зовутся в телах якорей, обход `globals()`, "
          "список исключений и объявления сошлись"
          % (len(found), len(found) - len(holes), len(holes),
             (" (" + ", ".join(holes) + ")") if holes else "", len(SCAN_EXEMPT), anchors_seen))
    return 0


# Поломки, которые обязана поймать ловушка (круг 65, правка 10). Каждая строка — текстовая мутация
# исходника этого файла, исполняемая на месте: компиляция и вызов нужного отделения. Прогон
# ничего не пишет и не трогает дерево, поэтому его можно позволить себе и в CI, и в `--selfcheck`.
# Смысл именно в исполняемости: утверждение «мы проверили, что ловушка кусает», записанное прозой
# или скриптом в песочнице, через круг уже невоспроизводимо, а это ровно та иллюзия покрытия, против
# которой весь этот реестр и заведён.
SELF_MUTATIONS = (
    # (что сломано, иголка в исходнике, на что меняем, отделение, чем обязан отозваться)
    #
    # Иглы пишутся разорванными литералами («…m.group» + «(2)):…») намеренно: таблица, которая
    # цитирует носитель целиком, саму себя и находит — первая версия этого шага вставляла новую
    # функцию перед `def pipeline_inventory():` и попала в собственную строку описания. Разрыв
    # литерала — не шифр, а способ сказать «это ссылка на код, а не код».
    ("правило дат заглушено (никогда не срабатывает)",
     "if stamp and int(stamp) < int(m.group" + "(2)):", "if stamp and False:",
     "keydate_trap", "правило не поймало незаконный порядок"),
    ("обход дат ослеплён (regex не находит ни одного имени)",
     'OWNED_BLOCK_RX = re.compile(r"(reshootCounters|pipelineScripts|countsNote'
     '|environmentScopedNumbers)"',
     'OWNED_BLOCK_RX = re.compile(r"(ZZZтакогоблоканет)"',
     "keydate_trap", "не нашёл ни одного блока"),
    ("вернулись к равенству дат (краснеет и на законном порядке)",
     "if stamp and int(stamp) < int(m.group" + "(2)):", "if stamp and int(stamp) != int(m.group(2)):",
     "keydate_trap", "ловушка сработала на законном порядке"),
    ("объявление стража снято (сверка осталась без реестра)",
     '    "mirror_audit": ("гейт", "правило ' + '25"),\n', "",
     "plant_registry_trap", "определено и не объявлено"),
    ("завелась сверка без объявления",
     "\ndef tree_counts(root=None) -> dict:",
     "\ndef claims_rollup_audit(corp):\n    return 0\n\n\n"
     "def tree_counts(root=None) -> dict:",
     "plant_registry_trap", "Новая сверка обязана объявить"),
    ("сверка переименована, объявление висит на пустом месте",
     "\ndef env_scan(corp):", "\ndef env_scanX(corp):",
     "plant_registry_trap", "объявлено и не найдено"),
    ("чужая проверка исчезла, а ссылка на неё осталась",
     '    "mirror_audit": ("гейт", "правило ' + '25"),',
     '    "mirror_audit": ("гейт", "правило ' + '99"),',
     "plant_registry_trap", "там нет"),
    ("съём дерева игнорирует названный корень (всегда мерит живое дерево)",
     "    root = ROOT if root is None else Path(" + "root)", "    root = ROOT",
     "tree_counts_trap", "ЛОВУШКА ДЕРЕВА НЕ ПОДТВЕРЖДЕНА"),
    ("обход ланов разучился ходить по подкаталогам (всегда ноль)",
     "    per = {}\n    for lan in SUBLANES:", "    per = {}\n    for lan in ():",
     "tree_counts_trap", "ЛОВУШКА ДЕРЕВА НЕ ПОДТВЕРЖДЕНА"),
    ("файл-страж исчез",
     '    "гейт": ROOT / "scripts" / "validate_atonement_corpus_integrity' + '.py",',
     '    "гейт": ROOT / "scripts" / "туда-не-смотри.py",',
     "plant_registry_trap", "НЕИСПОЛНИМ"),
    ("сверка таблицы §9.1 обезврежена (строки сверяются, но не сравниваются)",
     'elif rows[lan] != ' + 'want:', "elif False:",
     "table91_trap", "ЛОВУШКА ТАБЛИЦЫ 9.1"),
    ("глава 9.1 для обхода переименована (сверка осталась без таблицы)",
     '    start = next((i for i, l in enumerate(raw) if l.startswith("' + '### 9.1")), None)',
     '    start = next((i for i, l in enumerate(raw) if l.startswith("' + '### 9.7")), None)',
     "table91_trap", "НЕ ИСПОЛНИМА"),
    ("сверка завелась вне соглашения и без списка исключений (имя молчало бы десять кругов)",
     "\ndef " + "num(",
     "\ndef itog():\n    return 0\n\n\ndef " + "num(",
     "plant_registry_trap", "вне соглашения и вне списка исключений"),
    ("исключение унаследовано от исчезнувшей функции (мёртвый хвост в списке)",
     "\ndef " + "main() -> int:",
     "\ndef " + "mainX() -> int:",
     "plant_registry_trap", "исключение висит на имени"),
    # Правка 18: мера причины получает те же исполняемые опровержения, что и всё в списке:
    # безымянная причина, призрак якоря, якорь без имени в теле и ложный корень.
    ("причина в исключении осталась без якоря — мера снова проза одного читателя",
     "фильтр токенов правила 20; сравнение — в sha_audit; якорь " + "`sha_audit`",
     "; фильтр токенов правила 20; сравнение — в sha_audit; якорь не назначен",
     "plant_registry_trap", "причина без якоря"),
    ("якорь в причине указывает на несуществующую функцию",
     "дока-якорях; якорь " + "`registry_numbers`",
     "; якорь `registry_numbersX`",
     "plant_registry_trap", "якорь-призрак"),
    ("якорь существует, но исключённое имя в его теле не зовётся",
     "дока-якорях; якорь " + "`registry_numbers`",
     "; якорь `tree_counts`",
     "plant_registry_trap", "не зовётся в теле якоря"),
    ("в тело корня посажена сверка — корневой якорь врёт, что сверок в теле нет",
     "\ndef " + "main() -> int:",
     "\ndef main() -> int:\n    def root_lie_audit():\n        return 0",
     "plant_registry_trap", "сверка определена в теле корня"),
)


def self_mutation_trap():
    """Ломает собственный исходник всеми способами, перечисленными в таблице выше, и требует,
    чтобы каждый был пойман с причиной.

    Вердикт мутанта не печатается в общий вывод — он захватывается и сверяется по подстроке:
    «красно» недостаточно, краснота обязана быть про ту поломку, которую посадили.

    Проверено и обратное: если отделение реестра заглушить (`return 0` в начале тела), шаг краснеет
    словами «поломка прошла зелёной» — то есть сам шаг не может выродиться в молчание незамеченным.
    """
    import contextlib
    import io
    src = Path(__file__).read_text(encoding="utf-8")
    missed, caught = [], 0
    for i, (what, needle, repl, dept, why) in enumerate(SELF_MUTATIONS):
        # ровно одно место: первая версия этого шага подставила новую функцию перед `def
        # pipeline_inventory():` — и попала в собственную таблицу, потому что та же строка читается
        # в ней как иголка. Однократность якоря проверяется здесь, а не подразумевается: так же
        # отказывается писать пересъёмщик, когда его якорь в документе находит две строки.
        if src.count(needle) != 1:
            missed.append("%s: носитель встречается %d раза — мутация обязана указывать ровно на одно "
                          "место (иначе она правит не инструмент, а эту таблицу)"
                          % (what, src.count(needle)))
            continue
        ns = {"__name__": "reshoot_mutant_%d" % i, "__file__": str(Path(__file__))}
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src.replace(needle, repl, 1), "<мутация %d>" % i, "exec"), ns)
                rc = ns[dept]()
            text = buf.getvalue().strip()
        except Exception as exc:            # падение мутанта — тоже поимка, но названная
            rc, text = 1, "%s: %s" % (type(exc).__name__, exc)
        if rc == 0:
            missed.append("%s: поломка прошла зелёной" % what)
        elif why not in text:
            tail = text.splitlines()[-1][:110] if text else "вердикта нет вовсе"
            missed.append("%s: код %d, но причины «%s» в вердикте нет; последняя строка: %s"
                          % (what, rc, why, tail))
        else:
            caught += 1
    if missed:
        print("ЛОМКА ИСХОДНИКА НЕ ПОЙМАНА полностью — %d из %d: %s"
              % (len(missed), len(SELF_MUTATIONS), "; ".join(missed)))
        return 1
    print("ЛОМКА ИСХОДНИКА: %d поломок, все пойманы с названной причиной — ловушка кусает себя сама"
          % len(SELF_MUTATIONS))
    return 0


LANE_OF_91 = "корпус"


def table91_trap():
    """Ловушка на живом разборе §9.1: посадить расхождение, не трогая документ.

    Три состояния, а не одно: на живом дереве сверка обязана молчать, посаженная ячейка — быть
    пойманной именно про тот лан, куда посажено, и пустой текст — быть пойманным как ослепление.
    Третье отделение здесь главное: сверка, не нашедшая таблицы, не имеет права вернуться пустым
    списком, потому что пустой список у неё означает «всё сходится».
    """
    corp = json.loads(CORPUS.read_text(encoding="utf-8"))
    text = DOC.read_text(encoding="utf-8")
    clean = check_table_91(corp, text)
    if clean:
        print("ЛОВУШКА ТАБЛИЦЫ 9.1 НЕ ИСПОЛНИМА: на живом дереве сверка уже красна — сначала "
              "почините таблицу, потом проверяйте ловушку: " + clean[0][:100])
        return 2
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("### 9.1")), None)
    stop = next((i for i in range(start + 1, len(lines)) if lines[i].startswith(("### ", "## "))),
                len(lines)) if start is not None else 0
    hits = []
    for i in range(start if start is not None else 0, stop):
        line = lines[i]
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8 or cells[0].strip("`") != LANE_OF_91:
            continue
        try:
            hits.append((i, int(cells[1].replace("*", "").replace(" ", ""))))
        except ValueError:
            continue
    planted_at = None
    if len(hits) == 1:
        i, first = hits[0]
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        cells[1] = str(first + 1)
        lines[i] = "| " + " | ".join(cells) + " |"
        planted_at = i
    if planted_at is None:
        print("ЛОВУШКА ТАБЛИЦЫ 9.1 НЕ ИСПОЛНИМА: строка `%s` не найдена в главе ровно один раз "
              "(найдено %d) — сажать нарушение некуда или не в ту строку"
              % (LANE_OF_91, len(hits)))
        return 2
    red = check_table_91(corp, "\n".join(lines))
    blind = check_table_91(corp, "")
    problems = []
    if not red:
        problems.append("посаженное расхождение (ячейка «+1» в строке `%s`) прошло молча" % LANE_OF_91)
    elif not any(LANE_OF_91 in r for r in red):
        problems.append("покраснело не про посаженный лан: " + red[0][:90])
    if not blind:
        problems.append("пустой текст вернулся без единого расхождения — сверка ослепла и назвала "
                        "это совпадением")
    if problems:
        print("ЛОВУШКА ТАБЛИЦЫ 9.1 НЕ ПОДТВЕРЖДЕНА — " + "; ".join(problems))
        return 1
    print("ЛОВУШКА ТАБЛИЦЫ 9.1: живое дерево молчит, посаженная ячейка поймана (%d расхождений, "
          "первое — про `%s`), ослеплённый обход пойман (%d расхождений на пустом тексте) — дыра, "
          "объявленная правкой 9, закрыта"
          % (len(red), LANE_OF_91, len(blind)))
    return 0


def tree_counts_trap():
    """Ловушка на съёме чисел дерева: другой корень — другие числа.

    Строит во временном каталоге миниатюру того же периметра (те же имена, та же форма таблиц) и
    требует трёх вещей, а не одной: обход обязан увидеть фикстуру целиком (иначе «ноль файлов»
    снова был бы успехом); правка в файле обязан сдвинуть ровно те поля, которые обязана; пустой
    корень не имеет права вернуть живые числа — иначе у съёмки есть тайная дорожка к тому месту,
    где скрипт лежит, и вся история про «число относится к дереву» обнуляется.

    Проверка абсолютных чисел фикстуры честна именно потому, что фикстуру пишет этот код: байты и
    строки здесь не вторая реализация обхода, а условие задачи.
    """
    import shutil
    import tempfile
    doc_text = "шапка\n\n| a | b |\n\nхвост\n"
    mass_text = "## Масса\n\n| FP-1 | 10 |\n| FP-2 | 20 |\n\n"
    files = {
        "docs/research/atonement/01_a.md": "одна строка\nвторая\n",
        "docs/research/atonement/12_b.md": "x\n",
        "docs/research/atonement/x.md": "не нумерованный\n",
        "docs/research/atonement/35_four_point_authors_mass_registry.md": mass_text,
        "ИСКУПЛЕНИЕ/18_SERIES_AUDIT_AND_ARCS_2026-10-26.md": doc_text,
        "ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md": "17\n",
        "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json": "{}\n",
        "ИСКУПЛЕНИЕ/data/atonement-library-index.json": "{}\n",
        "ИСКУПЛЕНИЕ/ot/a.md": "ot\n",
        "ИСКУПЛЕНИЕ/nt/a.md": "nt\n",
        "ИСКУПЛЕНИЕ/fathers/a.md": "fathers\n",
        "ИСКУПЛЕНИЕ/synthesis/a.md": "synthesis\n",
        "ИСКУПЛЕНИЕ/synthesis/drafts/d1.md": "d1\nd2\n",
        "ИСКУПЛЕНИЕ/synthesis/drafts/d2.md": "d3\n",
    }
    tmp = tempfile.mkdtemp(prefix="atonement-tree-trap-")
    try:
        for relpath, content in files.items():
            dst = Path(tmp) / relpath
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(content, encoding="utf-8")
        t = tree_counts(Path(tmp))
        problems = []
        if (t["docs"][0], t["docsNumbered"]) != (4, 3) or t["rootmd"][0] != 2:
            problems.append("фикстура прочитана не целиком: файлов полосы %d (ожидалось 4), "
                            "нумерованных %d (3), в корне отдела %d (2) — обход видит не то, что "
                            "написано" % (t["docs"][0], t["docsNumbered"], t["rootmd"][0]))
        if t["doc"][:2] != (len(doc_text.encode("utf-8")), len(doc_text.split("\n")) - 1):
            problems.append("байты и строки документа съёмнуты не по фикстуре: %r, ожидалось %r"
                            % (t["doc"][:2], (len(doc_text.encode("utf-8")), len(doc_text.split("\n")) - 1)))
        if (t["massRows"], t["massSections"], t["sub"][0]) != (2, 1, 4):
            problems.append("строки массы и ланы съёмнуты неверно: рядов %d (2), разделов %d (1), "
                            "файлов по ланам %d (4)" % (t["massRows"], t["massSections"], t["sub"][0]))
        # посадка: правка в файле обязана двигать числа
        (Path(tmp) / "docs/research/atonement/01_a.md").write_text("одна\nвторая\nтретья\n",
                                                                    encoding="utf-8")
        (Path(tmp) / "docs/research/atonement/35_four_point_authors_mass_registry.md").write_text(
            mass_text + "| FP-3 | 30 |\n", encoding="utf-8")
        (Path(tmp) / "ИСКУПЛЕНИЕ/nt/a.md").unlink()
        t2 = tree_counts(Path(tmp))
        moved = []
        if t2["docs"][1] > t["docs"][1]:
            moved.append("байты полосы")
        if t2["massRows"] == 3:
            moved.append("рядов массы")
        if t2["sub"][0] == 3 and t2["sub"][1] < t["sub"][1]:
            moved.append("файлов по ланам")
        if len(moved) < 3:
            problems.append("правка сдвинула только %s — часть чисел снимается не с дерева, а с "
                            "того, что уже было посчитано" % (", ".join(moved) or "ничего"))
        # ослепление: пустой корень не имеет права вернуть живые числа
        empty = tempfile.mkdtemp(prefix="atonement-tree-trap-empty-")
        try:
            try:
                t3 = tree_counts(Path(empty))
            except OSError as exc:
                t3 = {"отказ": str(exc)[:60]}
            live = tree_counts()
            if "отказ" not in t3 and t3.get("corpBytes") == live["corpBytes"]:
                problems.append("пустой корень вернул живые числа корпуса — у съёмки есть тайная "
                                "дорожка к ROOT, и «число относится к дереву» тогда неправда")
        finally:
            shutil.rmtree(empty, ignore_errors=True)
        if problems:
            print("ЛОВУШКА ДЕРЕВА НЕ ПОДТВЕРЖДЕНА — " + "; ".join(problems))
            return 1
        print("ЛОВУШКА ДЕРЕВА: фикстура прочитана целиком, правка сдвинула 3 поля из 3, пустой "
              "корень живых чисел не вернул — число относится к дереву, а не к месту, где лежит "
              "скрипт")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def keydate_trap():
    """Ловушка на живом определении: правило обязано краснеть и молчать по очереди.

    Смягчение круга 65 (равенство дат -> порядок) оставило `keydate_audit` с одной запрещённой
    стороной, и у этой стороны до сих пор не было ни одного посадочного места: ни батарея (она
    про гейт), ни проб (он про положение main) не высаживают в корпус блок, названный свежее, чем
    снят. Значит, правило могло выродиться в молчание незаметно: сломанный обход не находит блоков,
    `bad` пуст, `checked` ноль — и сверка печатает «0 расхождений из 0», что неотличимо от успеха.
    Поэтому ловушка проверяет три вещи, а не одну: незаконный порядок пойман, законный не пойман,
    и обход действительно видел блоки (иначе первые два пункта ничего не значат).

    Синтетика живёт в памяти: дерево при этом не меняется, писанины нет, повторение безопасно.
    """
    def block(name_date, stamp):
        return {"pipelineScripts%sr99" % name_date: {"measuredAt": stamp}}

    legal = block("20261026", "2026-10-28T00:00:00Z")   # названо вчера, снято позже — законно
    illegal = block("20261028", "2026-10-26T00:00:00Z")  # названо завтра, снято вчера — обман
    checked_l, bad_l = keydate_audit(legal)
    checked_i, bad_i = keydate_audit(illegal)
    verdicts = []
    if checked_l == 0 or checked_i == 0:
        print("ЛОВУШКА НЕ ПОДТВЕРЖДЕНА: обход `keydate_audit` не нашёл ни одного блока в синтетике "
              "(законно: %d, незаконно: %d) — правило молчит не потому, что порядок верен, а потому, "
              "что не видит ключей" % (checked_l, checked_i))
        return 2
    if bad_l:
        verdicts.append("ловушка сработала на законном порядке (так краснел круг 64): "
                      + bad_l[0][:110])
    if not bad_i:
        verdicts.append("правило не поймало незаконный порядок (имя блока позже его штамма)")
    if verdicts:
        print("ЛОВУШКА НЕ ПОДТВЕРЖДЕНА — " + "; ".join(verdicts))
        return 1
    print("ЛОВУШКА ПРАВИЛА ДАТ: ловит незаконный порядок (1 из 1), молчит на законном "
          "(0 из 1), блоков увидено %d — смягчение круга 65 не есть заглушка"
          % (checked_l + checked_i))
    return 0


def pipeline_inventory():
    """Съём инструментов, которыми снимаются числа. Блок живёт в реестре ровно затем, чтобы
    «скрипт есть в дереве» отличалось от «скрипт есть в main и в PR круга»: перечисление
    переснимается каждый прогон, и md5 файла в нём — тот же, что увидит CI."""
    out, total = {}, 0
    for rel in PIPELINE_FILES:
        f = ROOT / rel
        if not f.is_file():
            out[rel] = "нет файла"
            continue
        raw = f.read_bytes()
        total += len(raw)
        out[rel] = {"байт": len(raw), "строк": raw.count(b"\n"), "md5": hashlib.md5(raw).hexdigest()}
    return {"файлов": len([v for v in out.values() if isinstance(v, dict)]), "байт": total, "файлы": out}


# ------------------------------------------------------------------ числа реестра

def registry_numbers(corp: dict, idx_file: dict):
    t = tree_counts()
    lc = ledger_counts()
    cens = index_census(idx_file)
    stamp = {"корпус": stamped_count(corp)}
    for lan in SUBLANES:
        for p in sorted((ROOT / "ИСКУПЛЕНИЕ" / lan / "data").glob("*corpus*.json")):
            stamp[lan] = stamp.get(lan, 0) + stamped_count(json.loads(p.read_text(encoding="utf-8")))
    out = {"tree": t, "ledger": lc, "census": cens, "stamp": stamp,
           "ключейРеестра": len(corp), "правилГейта": len(corp["integrityGate"]["rules"]["list"])}
    sha = sha_audit(corp)
    out["sha"] = sha
    out["mirror"] = mirror_audit(corp)
    out["draftPaths"] = draft_paths()
    out["json"] = json_leaf_scan()
    out["out"] = out_of_scope_mixed()
    out["env"] = env_scan(corp)
    out["keydate"] = keydate_audit(corp)
    out["stampPrev"] = (((corp.get("integrityGate") or {}).get("scopeOfMeasurementRules") or {})
                        .get("stampedFieldsPerRegistry") or {}).get("корпус")
    return out


def apply_corpus(corp: dict, n: dict) -> dict:
    """Только поле → значение; ключи создаёт этот код, а не правка текста."""
    t, lc, cens = n["tree"], n["ledger"], n["census"]
    li = corp["libraryIndex20261023"]
    for k, v in cens.items():
        li[k] = v
    li["measuredAt"] = li["checkedAt"] = now
    # method и recheckCommand дописываются, а не заменяются: в них живёт описание того, как счёт
    # снимали круги 25..61, и затирать его «улучшением формата» — тот же дефект, что и потерянное число
    add = ("; с круга 63 числа строит scripts/atonement_reshoot_state.py --write тем же обходом, каким их "
           "сверяет правило 25 гейта, а шаг «Read-only re-shoot check» в workflow "
           "atonement-corpus-integrity.yml гоняет тот же файл на --check: расхождение блокирует мерж")
    if "atonement_reshoot_state.py" not in str(li.get("method", "")):
        li["method"] = f"{li.get('method', '')}{add}"
    addcmd = " || python3 -B scripts/atonement_reshoot_state.py --check"
    if "atonement_reshoot_state.py" not in str(li.get("recheckCommand", "")):
        li["recheckCommand"] = f"{li.get('recheckCommand', '')}{addcmd}"
    li["countsNote" + KEY_DATE + "r" + CIRCLE] = (
        f"Круг {CIRCLE}: ценз переснят после того, как в индекс легла ещё одна запись (живой слепок) и одна "
        f"перестала быть живой (её носитель помечен «УСТАРЕЛО»): записей {cens['records']}, файлов "
        f"{cens['files']}, папок {cens['folders']}, носителей материала {cens['materials']}, с локатором "
        f"{cens['materialsWithLocators']}, байт по Drive {num(cens['driveBytesSum'])}, крупнейший "
        f"{num(cens['largestBytes'])}. Изменение бухгалтерии, а не периметра: прирост ровно один объект."
    )
    li["indexBytes"] = n["tree"]["idxBytes"]

    bta = corp.get("branchTopologyAudit20261022") or {}
    nrows, nqueue = mass_counts()
    cl = corp["reproducibility20261022"]["countsLive"]
    # блок закрыт списком правила (см. комментарий в гейте строки 1041..1070): любое новое поле там
    # — ошибка, поэтому сюда пишутся ровно те восемь чисел, которые переснимает сам гейт
    live = {"ключейРеестра": n["ключейРеестра"], "правилГейта": n["правилГейта"],
            "shaВсверкеВремен": len(bta.get("commitTimeChecks") or {}),
            "строкВАудитеТопологии": len(bta.get("rows") or []),
            "записейЛеджера": lc["записей"], "строкСводки": ledger_svodki(),
            "строкРеестраМассы": nrows, "очередейДобычиМассы": nqueue}
    for k, v in live.items():
        if k in cl:
            cl[k] = v
    cl["measuredAt"] = now

    rn = corp["reproducibility20261022"]
    key = "reshootCounters" + KEY_DATE + "r" + CIRCLE
    extra = {
        "что": (f"числа, которые круг {CIRCLE} переснимает по своим определениям и которым не место в "
                "countsLive: тот блок закрыт восемью проверяемыми счётчиками, а про это число гейт "
                "ничего не знает — значит ему нужен собственный метод и команда"),
        "байтКорпуса": t["corpBytes"], "байтИндекса": t["idxBytes"],
        "байтВсегоДанных": t["data"][1],
        "байтДоковПолосы": t["docs"][1], "доковПолосы": t["docs"][0],
        "байтКорняОтдела": t["rootmd"][1], "файловКорняОтдела": t["rootmd"][0],
        "байтПодЛанов": t["sub"][1], "файловПодЛанов": t["sub"][0],
        "байтПоЛанам": {lan: t["perLan"][lan][1] for lan in SUBLANES},
        "черновиковФайлов": t["drafts"][0], "черновиковБайт": t["drafts"][1],
        "черновиковСтрок": t["draftsLines"],
        "реестрМассыБайт": t["massBytes"], "разделовКруговВРеестреМассы": t["massSections"],
        "документБайт": t["doc"][0], "документСтрок": t["doc"][1], "документMd5": t["doc"][2],
        "подЛанШтампы": {lan: n["stamp"][lan] for lan in SUBLANES},
        "индекс": {"записей": cens["records"], "файлов": cens["files"],
                   "носителей": cens["materials"], "папокПериметра": cens["scopeFolders"]},
        "зеркалаDrive": {"записей": n["mirror"]["записей"], "свереноСBlob": n["mirror"]["проверено"],
                         "неПрочитано": n["mirror"]["неПрочитано"]},
        "measuredAt": now, "checkedAt": now,
        "method": ("scripts/atonement_reshoot_state.py — глобы среза, обход правила 25, обход правила 19 "
                   "по JSON-листьям, сводка леджера и строки реестра массы — определения продублированы из "
                   "гейта, арбитром остаётся гейт: он проверяет свои числа своим обходом в том же прогоне"),
        "recheckCommand": "python3 -B scripts/atonement_reshoot_state.py --check && python3 -B "
                          "scripts/validate_atonement_corpus_integrity.py",
    }
    if key in rn:
        extra["переснятоПрогоном"] = now
    rn[key] = extra

    # дуга III (п. 3.10/3.14): два поля под-регистра, которые аудит нашёл снятыми «по памяти»,
    # теперь пишет и сверяет этот обход. Запись идёт сюда несмотря на ENV_OWNED: поля не новые
    # счётчики, а существующие числа леджера — дуга III подключает их к обходу; авторство
    # расширения — §6 дуги III, владелец подтверждает этим заказом.
    syn = corp["synthesis"]
    cr = syn["conflictRange"]
    cr["ledgerEntries"] = lc["записей"]
    cr["ledgerMaxIndex"] = int(lc["последний"])
    cr["measuredAt"] = now
    if "atonement_reshoot_state.py" not in str(cr.get("method", "")):
        cr["method"] = (f"{cr.get('method', '')}; с круга {CIRCLE} (дуга III) ledgerEntries/ledgerMaxIndex "
                        "переснимает scripts/atonement_reshoot_state.py --write тем же обходом леджера, "
                        "каким их сверяет шаг --check; прежний ручной съём 2026-10-22 сохранён выше как "
                        "история метода")
    syn["drafts"] = n["draftPaths"]
    syn["draftsPurpose"] = ("назначение: полное зеркало каталога synthesis/drafts (п. 3.14: прежнее значение "
                            "перечисляло один файл из каталога и не называло себя) — список и сверка снимаем "
                            "обходом scripts/atonement_reshoot_state.py, читает и требует --check")
    syn["draftsMeasuredAt"] = now

    sf = corp["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]
    sf.update(dict(sorted(n["stamp"].items())))
    # поле how — журнал пересъёмов, и оно обязано кончаться этим кругом: иначе следующая рука,
    # которая придёт править число, увидит обрыв на полуслове. Отметки времени здесь не добавляются:
    # строка без measuredAt не двигает тот самый счётчик, который она описывает
    clause = (f"круг {CIRCLE}: {n['stampPrev']} → {n['stamp']['корпус']} (прирост дают отметки времени "
              "в тех блоках, которые круг трогает, — по measuredAt и checkedAt на блок; перечень таких "
              "блоков — метод этого скрипта, а не память автора круга; самих чисел правка не двигает, "
              "иначе собственный пересъём сдвигал бы число, которое он переснимает)")
    if clause not in str(sf.get("how", "")):
        sf["how"] = f"{sf.get('how', '')}; {clause}"

    if n["sha"] is not None:
        sc = corp["integrityGate"].get("shaCitationAudit20261023") or {}
        # только числа и отметки. В блоке живёт recordCommit — карта «мёртвая ссылка → коммит,
        # через который её переснимают»; правило 20 без неё падает, а замена блока целиком
        # (первый вариант этого скрипта) её и съела: −15 КБ прозы и 47 потерянных пересъёмов
        for k in ("uniqueShaTokens", "reachableTokens", "unreachableTokens", "fieldsWithDeadLinks"):
            sc[k] = n["sha"][k]
        sc["byBlock"] = n["sha"]["byBlock"]
        # gitObjectsConsidered в реестр не пишется: это свойство клона, а не дерева. Объявленное
        # кругом 63, оно покраснело на прогоне того же круга против уже смёрженного main (14661
        # против 14690: мерж добавил в историю 29 объектов) — то есть врало бы в каждом круге,
        # ничего не утверждая о корпусе. Объём обхода печатается в отчёте прогона и живёт в штампе
        # круга как запись о съёме; если поле ещё встречлось в каноне — снимаем его и объявляем.
        removed = sc.pop("gitObjectsConsidered", None)
        note = sc.get("удалённыеФигуры")
        # пишется и когда поле только что снято, и когда записка оказалась неполной (первый вариант
        # этого блока вышел без how/command и гейт его обоснованно не принял); полностью записанный
        if removed is not None or not isinstance(note, dict) or not {"how", "command"} <= set(note):
            sc["удалённыеФигуры"] = {
                "gitObjectsConsidered": "введён и снят кругом 63: число объектов git в среде съёма, "
                                        "свойство клона а не дерева; в отчёте прогона печатается, в "
                                        "реестре не сверяется",
                "measuredAt": now, "checkedAt": now,
                "how": "решение круга 63: поле о размере обхода клона не переснимается против "
                        "другого клона, поэтому оно снято с сверки; причина живёт в §9.3 аудита",
                "command": "python3 -B scripts/atonement_reshoot_state.py --report",
            }
        sc["measuredAt"] = sc["checkedAt"] = now
        sc["переснятКругом" + CIRCLE] = {
            "чем": "scripts/atonement_reshoot_state.py", "обходом": "правило 20 гейта, определение 7/8/40 hex",
            "gitОбъектовВсего": n["sha"]["gitObjectsConsidered"], "measuredAt": now, "checkedAt": now,
            "method": "тот же обход, что и у сверки: --check в workflow atonement-corpus-integrity",
            "recheckCommand": "python3 -B scripts/atonement_reshoot_state.py --check",
        }

    jls = n["json"]
    msc = corp["integrityGate"]["mixedScriptCheck"]
    if "jsonLeafScan" in msc:
        for k in ("ownOccurrences", "scannedFiles", "foreignOccurrences"):
            msc["jsonLeafScan"][k] = jls[k]
        msc["jsonLeafScan"]["переснятКругом" + CIRCLE] = {"measuredAt": now,
                                                          "чем": "scripts/atonement_reshoot_state.py",
                                                          "method": "тот же обход JSON-листьев, что и у правила 19",
                                                          "recheckCommand": "python3 -B scripts/atonement_reshoot_state.py --check"}
    if "outOfScope" in msc:
        for k in ("occurrences", "files"):
            msc["outOfScope"][k] = n["out"][k]
        msc["outOfScope"]["measuredAt"] = msc["outOfScope"]["checkedAt"] = now
        # правило (2) гейта: датированное поле обязано объявить способ пересъёма, иначе отметка
        # времени стоит над мнением; у этого блока способа не было, пока его не стал переснимать круг 63
        if not ({"method", "how", "recheckCommand", "command"} & set(msc["outOfScope"])):
            msc["outOfScope"]["method"] = ("обход всех `ИСКУПЛЕНИЕ/**.md`, кроме корня отдела: "
                                           "mixed_words по строкам, помеченные EXEMPT-строки пропускаются")
            msc["outOfScope"]["recheckCommand"] = "python3 -B scripts/atonement_reshoot_state.py --check"
    for k, gap in sorted((n["mirror"]["gap"] or {}).items()):
        blk = corp["driveMirrors"][k]["разрывСДеревом"]
        blk["байт"] = gap
        blk["снятПрогоном"] = now
        blk["measuredAt"] = now

    pinv = pipeline_inventory()
    blk = corp["reproducibility20261022"].get("pipelineScripts" + KEY_DATE + "r" + CIRCLE) or {}
    corp["reproducibility20261022"]["pipelineScripts" + KEY_DATE + "r" + CIRCLE] = {
        "что": ("инструменты, которыми сняты числа этого круга: пересъёмщик, два писателя записей, гейт, "
                "реестр доводов, батарея мутаций и — с круга 64 — сам порядок закрытия круга "
                "`scripts/atonement_round_close.py`; в списке он потому, что вырезанный порядок "
                "обнуляет смысл чисел ровно так же, как вырезанный пересъёмщик. Блок переснимается каждый прогон, потому что md5 файла "
                "из памяти автора круга — это не замер, а обещание"),
        "файлов": pinv["файлов"], "байт": pinv["байт"], "файлы": pinv["файлы"],
        "зачемВДереве": ("круг 62 перенёс скрипты из песочницы в `scripts/`, но не запушил коммит — "
                         "инструменты и записи погибли вместе с веткой; с этого круга и файл в каноне, "
                         "и его контрольная сумма под проверкой CI"),
        "measuredAt": now, "checkedAt": now,
        "method": "read_bytes + md5 + число переводов строки по списку PIPELINE_FILES этого же скрипта",
        "recheckCommand": ("python3 -B scripts/atonement_reshoot_state.py --check   # сверит реестр с "
                           "файлами; руками: md5sum scripts/atonement_*.py"),
        "байтДоЭтогоПрогона": (blk.get("байт") if blk else None),
    }

    # числа обхода (круг 64). То, что меряет не дерево, а среду съёма, обязано назваться: живёт в
    # штампе прогона — не сверяется, объявлено в списке — сверяется как запись о среде, стоит молча
    # в сверяемом блоке — снимается сюда. Иначе следующий прогон краснеет на числе, верном по
    # определению: ровно так доказательство круга 63 поймало gitObjectsConsidered на main.
    env = n["env"]
    stripped, foreign = {}, {}
    for pth in env["незаконные"]:
        parts = pth.split(".")
        parent = resolve(corp, ".".join(parts[:-1]))
        if isinstance(parent, dict) and parts[-1] in parent and any(pth.startswith(o) for o in ENV_OWNED):
            val = parent.pop(parts[-1])
            stripped[pth] = {"значение": val, "чемСнято": "scripts/atonement_reshoot_state.py --write",
                             "почему": ("поле названо как счётчик обхода и стоит вне штампа прогона: "
                                        "оно меряет среду съёма, а не дерево; в сверке ему места нет")}
        else:
            foreign[pth] = {"что": ("число обхода в блоке, который этот скрипт не правит; снимает его "
                                    "владелец блока, а пересъёмщик только не даёт ему притвориться "
                                    "числом дерева"),
                            "можноИначе": ("объявить в " + ENV_DECL_BLOCK + ".поля с причиной и способом "
                                           "пересъёма")}
    prev_decl = (corp["integrityGate"].get(ENV_DECL_BLOCK) or {}).get("снятоКакМёртвое") or []
    corp["integrityGate"][ENV_DECL_BLOCK] = {
        "что": ("объявленные числа обхода: сколько объектов, коммитов, файлов или строк увидел чей-то "
                "обход. Такое число относится к клону, а не к дереву: оно верно в своей среде и "
                "расходится в чужой. Живёт в штампе прогона — не сверяется; объявлено здесь — сверяется "
                "как запись о среде; молча стоит в сверяемом блоке — снимается в снятоЭтимКругом"),
        "поля": env["живые"],
        "пуст": len(env["живые"]) == 0,
        "снятоЭтимКругом": stripped,
        "ждётВладельца": foreign,
        "снятоКакМёртвое": sorted(set(prev_decl) | set(env["мертвыеОбъявления"])),
        "measuredAt": now, "checkedAt": now,
        "how": ("числовой обход вселенной пересъёмщика по меткам имён полей (ENV_MARK этого скрипта) и "
                "классификация по пути: штамп прогона против объявленного списка; список перечитывается "
                "каждый прогон, потому что мёртвое объявление — это разрешение на будущее число"),
        "method": "env_scan() в scripts/atonement_reshoot_state.py — определения, чем меряется обход",
        "recheckCommand": ("python3 -B scripts/atonement_reshoot_state.py --check && python3 -B "
                           "scripts/atonement_round_close.py --selfcheck"),
    }

    sa = corp["fourPointMassRegistry20261023"]["seriesAuditRound5820261026"]
    sa["файлАудита"] = {"байт": t["doc"][0], "строк": t["doc"][1], "md5": t["doc"][2]}
    sa["срезДерева"] = {
        "доки полосы": {"файлов": t["docs"][0], "байт": t["docs"][1]},
        "корень отдела": {"файлов": t["rootmd"][0], "байт": t["rootmd"][1]},
        "черновики статей": {"файлов": t["drafts"][0], "байт": t["drafts"][1]},
        "данные отдела": {"файлов": t["data"][0], "байт": t["data"][1]},
        **{f"под-лан {lan}": {"файлов": t["perLan"][lan][0], "байт": t["perLan"][lan][1]} for lan in SUBLANES},
    }
    sa["переснятКругом" + CIRCLE] = {
        "номерКруга": int(CIRCLE), "что": ("байты и строки среза и файла аудита пересняты "
                                           "scripts/atonement_reshoot_state.py после записи снимка круга "
                                           + CIRCLE),
        "measuredAt": now, "checkedAt": now,
        "method": "срез строится теми же глобами, что печатает таблица §1; сверка — шагом --check",
        "recheckCommand": "python3 -B scripts/atonement_reshoot_state.py --check",
    }
    return corp


# ------------------------------------------------------------------ строки документа

def doc_numbers(corp: dict, n: dict) -> list:
    """Каждая строка — (регулярка старого текста, новый текст). Регулярки якорены по началу
    строки, а не по старому значению, поэтому генератор находит собственный вывод."""
    t, lc, cens = n["tree"], n["ledger"], n["census"]
    sub = " / ".join(str(n["tree"]["perLan"][lan][0]) for lan in ("ot", "nt", "fathers", "synthesis"))
    stamps = n["stamp"]
    same = len({stamps[l] for l in SUBLANES}) == 1
    под = (f"**{stamps[SUBLANES[0]]}** таких полей в каждом из четырёх содержательных под-ланов"
           if same else "**" + " / ".join(str(stamps[l]) for l in SUBLANES) + "** таких полей по под-ланам (")
    if not same:
        под += "ot / nt / fathers / synthesis)"
    ndonot = len(corp.get("doNot") or [])
    holds = list(corp.get("holds") or [])
    num_hold = {5: "пять", 4: "четыре", 6: "шесть"}.get(len(holds), str(len(holds)))
    # «до этого стоял срез круга N» обязано браться из реестра, а не из памяти круга: строка
    # переживает авторов, и вчерашняя правда в ней сегодня уже ложь (круг 64 поймал это сам: строка
    # ещё звала прежний срез «кругом 60», хотя предыдущим был круг 63)
    repro = corp.get("reproducibility20261022") or {}
    prev = [(k.rsplit("r", 1)[1], (repro[k] or {}).get("байтКорпуса"))
            for k in sorted(k for k in repro if k.startswith("reshootCounters") and not k.endswith("r" + CIRCLE))
            if isinstance((repro[k] or {}).get("байтКорпуса"), int)]
    if prev:
        idx_note = ("числа снимает scripts/atonement_reshoot_state.py --write, сверяет --check (шаг гейта); "
                    f"до этого в строке стоял срез круга {prev[-1][0]} ({num(prev[-1][1])} B)")
    else:
        idx_note = ("числа снимает scripts/atonement_reshoot_state.py --write, сверяет --check (шаг гейта); "
                    "прежнего переснятого среза в реестре нет — строка ведётся с круга 63")
    return [
        (r"^\| `docs/research/atonement/`.*\|$",
         f"| `docs/research/atonement/` — читательско-исследовательская полоса | {t['docs'][0]} | "
         f"{num(t['docs'][1])} | {t['docsNumbered']} нумерованных разборов + `README.md` + таксономия |"),
        (r"^\| `ИСКУПЛЕНИЕ/\*\.md`.*\|$",
         f"| `ИСКУПЛЕНИЕ/*.md` — корень отдела | {t['rootmd'][0]} | {num(t['rootmd'][1])} | "
         f"от `00_CURRENT_AUTHORITY` до `18_SERIES_AUDIT`; `17_` один занимает {num(t['b17'])}, "
         f"этот документ — {num(t['doc'][0])} |"),
        (r"^\| под-ланы `ot`.*\|$",
         f"| под-ланы `ot` `nt` `fathers` `synthesis` | {t['sub'][0]} | {num(t['sub'][1])} | {sub} файлов |"),
        (r"^\| `ИСКУПЛЕНИЕ/synthesis/drafts/`.*\|$",
         f"| `ИСКУПЛЕНИЕ/synthesis/drafts/` — читательские черновики | {t['drafts'][0]} | "
         f"{num(t['drafts'][1])} | {t['draftsLines']} переводов строки суммарно — прежнее определение "
         f"(строки через split) давало {t['draftsLinesSplit']}, разница по одному на файл без финального "
         f"перевода; каждый {str(t['draftsMin']).replace('.', ',')}–{t['draftsMax']} КБ (1 КБ = 1000 B) |"),
        (r"^\| `ИСКУПЛЕНИЕ/data/`.*\|$",
         f"| `ИСКУПЛЕНИЕ/data/` — корпус и индекс библиотеки | {t['data'][0]} | {num(t['data'][1])} | "
         f"корпус {num(t['corpBytes'])} B, индекс {num(t['idxBytes'])} B; {idx_note} |"),
        (r"^\| реестр массы цитат.*\|$",
         f"| реестр массы цитат (`35_`) | 1 | {num(t['massBytes'])} | {t['massRows']} "
         f"{plural(t['massRows'], 'строка-носитель', 'строки-носителя', 'строк-носителей')}, {t['massSections']} "
         f"{plural(t['massSections'], 'раздел', 'раздела', 'разделов')} кругов |"),
        (r"(?ms)^Машина состояния .*?(?=\n\n)",
         "\n".join([
             f"Машина состояния (эти числа переснимает `scripts/atonement_reshoot_state.py`, а `--check`-шаг "
             f"гейта не даёт им разойтись; переписать их рукой — тот же грех, из-за которого круг 59 и завёл "
             f"правило 27): **{n['ключейРеестра']}** ключей верхнего уровня в корпусе, **{n['правилГейта']}** "
             f"правил гейта, **{stamps['корпус']}** штампованных (датированных и пересъёмных) полей корпуса, {под}.",
             f"Леджер конфликтов: **{lc['записей']}** {plural(lc['записей'], 'запись', 'записи', 'записей')} "
             f"`C-{lc['первый']} … C-{lc['последний']}`; машиночитаемых статусов **{lc['статусов']}** "
             f"({lc['разбивка']}).",
             f"Индекс библиотеки: **{cens['records']}** {plural(cens['records'], 'запись', 'записи', 'записей')}, "
             f"**{cens['files']}** {plural(cens['files'], 'файл', 'файла', 'файлов')}, **{cens['materials']}** "
             f"{plural(cens['materials'], 'носитель', 'носителя', 'носителей')} материала, периметр "
             f"**{cens['scopeFolders']}** {plural(cens['scopeFolders'], 'папка', 'папки', 'папок')} — и папка "
             f"`99` с вытесненными зеркалами вне периметра под `HOLD` (её состав переснимается командой из "
             f"`scope.excluded`, это число не из локального обхода).",
             # `publicationEligible=false` — не число и не обход, а Boundary, который печатает гейт
             # строкой; перечисление классов удержания и счётчик запретов — из реестра
             "Права и публикация: `publicationEligible=false`; "
             + f"{num_hold} {plural(len(holds), 'класс', 'класса', 'классов')} удержания — "
             + "`" + "`, `".join(holds) + "`; "
             + f"**{ndonot}** "
             + f"{plural(ndonot, 'исследовательский запрет', 'исследовательских запрета', 'исследовательских запретов')} "
             + "в `doNot`.",
         ])),
    ]


def apply_doc(corp: dict, n: dict) -> str:
    text = DOC.read_text(encoding="utf-8")
    for pat, new in doc_numbers(corp, n):
        hits = re.findall(pat, text, re.M)
        if len(hits) != 1:
            raise SystemExit(f"якорь {pat!r} нашёл {len(hits)} строк вместо одной — генератор "
                             "остановлен, чтобы не писать в две строки или не пропустить свою")
        text = re.sub(pat, lambda _m, s=new: s, text, count=1, flags=re.M)
    return text


def check_table_91(corp: dict, text: str = None) -> list:
    """Таблицу §9.1 этот скрипт не порождает (её производитель — утраченный финалайзер круга 61),
    но право её сверить оставляет: каждая ячейка обязана равняться полю реестра.

    `text` — тот же обход, но по поданному тексту: он нужен ловушке, чтобы посадить расхождение в
    строку, не трогая документ (круг 65, правка 12). Без этой опции сверка была непроверяема:
    доказать, что она кусает, можно было бы только испортив прозу, а порча прозы ради проверки —
    тот самый способ, которым круг 64 потерял четыре блока.
    """
    cpr = corp["integrityGate"]["scopeOfMeasurementRules"]["claimsPerRegistry"]
    raw = (DOC.read_text(encoding="utf-8") if text is None else text).splitlines()
    # Сверять надо с строкой *из §9.1*, а не с первой строкой с таким именем по всему документу:
    # имя `корпус` встречается и в §1, и в §5, и прошлая версия обхода молча переписывала rows
    # последней найденной строкой — то есть первая попавшаяся правка чужой таблицы могла сделать
    # §9.1 невидимым, и ничего бы не покраснело. Ограничение главой — единственное, чем это
    # отличается от «списока имён», который круги этого репозитория как раз и запретили.
    start = next((i for i, l in enumerate(raw) if l.startswith("### 9.1")), None)
    if start is None:
        return ["§9.1: глава не найдена — сверять таблицу не с чего (переименована или удалена)"]
    stop = next((i for i in range(start + 1, len(raw)) if raw[i].startswith(("### ", "## "))), len(raw))
    rows, total, dupes = {}, None, {}
    for line in raw[start:stop]:
        if not line.startswith("| `") and "**всего**" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        try:
            vals = [int(c.replace("*", "").replace(" ", "")) for c in cells[1:]]
        except ValueError:
            continue
        key = cells[0].strip("`")
        if "всего" in cells[0]:
            if total is not None:
                dupes["всего"] = dupes.get("всего", 1) + 1
            total = vals
        else:
            if key in rows:
                dupes[key] = dupes.get(key, 1) + 1
            rows[key] = vals
    bad = ["§9.1: строка `%s` в главе не одна — сверка по имени больше не однозначна" % k
           for k in sorted(dupes)]
    for lan in list(SUBLANES) + ["корпус"]:
        s_ = cpr["сверкаСКарточками"][lan]
        want = [s_["строк"], s_["покрытоПоФайлу"], s_["файлов"], s_["карточекБезСостояния"],
                s_["неОтраженоВКарточке"], s_["терминовКарточкиВнеПрозы"], s_["ссылокВнеОбходаЛана"]]
        if lan not in rows:
            bad.append(f"§9.1: строки `{lan}` в таблице нет")
        elif rows[lan] != want:
            bad.append(f"§9.1 `{lan}`: в таблице {rows[lan]}, реестр говорит {want}")
    sums = [sum(rows[l][i] for l in rows) for i in range(7)] if len(rows) == 5 else None
    if sums is not None and total is not None and sums != total:
        bad.append(f"§9.1: строка «всего» {total}, а сумма строк ланов {sums}")
    if cpr["всего"] not in (total or [None] * 7):
        bad.append(f"§9.1: суммы claimsPerRegistry.всего = {cpr['всего']} нет среди ячеек «всего» ({total})")
    return bad


def report_not_generated(corp: dict) -> str:
    keys = ["integrityGate.shaCitationAudit20261023", "libraryIndex20261023",
            "fourPointMassRegistry20261023.seriesAuditRound5820261026",
            "reproducibility20261022.countsLive",
            "integrityGate.scopeOfMeasurementRules.stampedFieldsPerRegistry",
            "driveSourceAudit20261016.переснят20261025r45",
            "reproducibility20261022.indexBytesNote20261026r53",
            "fourPointMassRegistry20261023.cardProseCrossCheck20261026r60.числа",
            "integrityGate." + ENV_DECL_BLOCK]
    lines = ["этот скрипт переснимает только перечисленное; из разделов 9.1 и 9.2 документа 18 он "
             "проверяет (но не пишет) таблицу §9.1, а остальное — проза, порождённая утраченным "
             "финалайзером круга 61, и живёт до ближайшей ручной правки:", "  реестровые блоки-источник: "
             + ", ".join("`%s`" % k for k in keys), "  поля, которые он намеренно не трогает: "
             "`claimsPerRegistry` целиком — с круга 65 у сводки есть свой производитель: "
             "atonement_claim_register.py (`--write` переснимает, `--check` и `--rollup` сверяют; "
             "до того правила 27 и 28 сравнивали число, которое не переснимал никто), "
             "`driveMirrors.*`, `libraryIndex20261023.countsNote*`, `shaCitationAudit20261023.note` "
             "в части формулировки"]
    return "\n".join(lines)


# ------------------------------------------------------------------ режимы

def diff_state_scan(corp: dict, idx_file: dict, n: dict):
    """Сверка. Только сравнения и сбор расхождений — ничего не записывает в данные: прошлый вариант
    этой функции содержал присваивания, попавшие туда ошибочной заменой, и «проверка» начинала
    чинить реестр у себя в кармане перед сравнением. Так выглядит самоподтверждающаяся бухгалтерия."""
    drift = []
    li = corp["libraryIndex20261023"]
    for k, v in n["census"].items():
        if li.get(k) != v:
            drift.append(f"libraryIndex20261023.{k}: реестр {li.get(k)!r}, обход {v!r}")
    t = n["tree"]
    # здесь только сравнения. Присваиваний быть не должно: патч, который вставлял пересъём
    # jsonLeafScan/outOfScope в apply_corpus, подменил их и в diff_state_scan (replace без count=1
    # нашёл два одинаковых якоря), и «проверка» начала чинить данные перед сравнением — ровно тот
    # вид самоподтверждения, из-за которого правило 25 и ловит internally consistent stale data
    sa = corp["fourPointMassRegistry20261023"]["seriesAuditRound5820261026"]
    for label, (nf, nb) in (("доки полосы", t["docs"]), ("корень отдела", t["rootmd"]),
                            ("черновики статей", t["drafts"]), ("данные отдела", t["data"])):
        if sa["срезДерева"].get(label) != {"файлов": nf, "байт": nb}:
            drift.append(f"seriesAuditRound5820261026.срезДерева.{label}: {sa['срезДерева'].get(label)!r}, "
                         f"обход {{'файлов': {nf}, 'байт': {nb}}}")
    for lan in SUBLANES:
        lab = f"под-лан {lan}"
        if sa["срезДерева"].get(lab) != {"файлов": t["perLan"][lan][0], "байт": t["perLan"][lan][1]}:
            drift.append(f"seriesAuditRound5820261026.срезДерева.{lab}: {sa['срезДерева'].get(lab)!r}, обход "
                         f"{{'файлов': {t['perLan'][lan][0]}, 'байт': {t['perLan'][lan][1]}}}")
    if sa["файлАудита"] != {"байт": t["doc"][0], "строк": t["doc"][1], "md5": t["doc"][2]}:
        drift.append(f"seriesAuditRound5820261026.файлАудита: {sa['файлАудита']!r}, обход "
                     f"{{'байт': {t['doc'][0]}, 'строк': {t['doc'][1]}, 'md5': {t['doc'][2]!r}}}")
    decl = corp["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]
    for _lab, _got in sorted(n["stamp"].items()):
        if decl.get(_lab) != _got:
            drift.append(f"stampedFieldsPerRegistry[{_lab!r}]: реестр {decl.get(_lab)!r}, обход {_got} "
                         "(блок хранит рядом method/note/how — их сравнивать нельзя, только числа)")
    cl = corp["reproducibility20261022"]["countsLive"]
    bta = corp.get("branchTopologyAudit20261022") or {}
    nr, nq = mass_counts()
    for k, v in (("ключейРеестра", n["ключейРеестра"]), ("правилГейта", n["правилГейта"]),
                 ("shaВсверкеВремен", len(bta.get("commitTimeChecks") or {})),
                 ("строкВАудитеТопологии", len(bta.get("rows") or [])),
                 ("записейЛеджера", n["ledger"]["записей"]), ("строкСводки", ledger_svodki()),
                 ("строкРеестраМассы", nr), ("очередейДобычиМассы", nq)):
        if k in cl and int(cl[k]) != v:
            drift.append(f"countsLive.{k}: {cl[k]!r}, обход {v}")
    # дуга III: поля под-регистра, подключённые к обходу, сверяются здесь же — сравнение, не запись
    _syn = corp.get("synthesis") or {}
    _cr = _syn.get("conflictRange") or {}
    if _cr.get("ledgerEntries") != n["ledger"]["записей"]:
        drift.append(f"synthesis.conflictRange.ledgerEntries: реестр {_cr.get('ledgerEntries')!r}, обход "
                     f"{n['ledger']['записей']} (поле переснимается apply_corpus — писать через "
                     "scripts/atonement_reshoot_state.py --write)")
    if _cr.get("ledgerMaxIndex") != int(n["ledger"]["последний"]):
        drift.append(f"synthesis.conflictRange.ledgerMaxIndex: реестр {_cr.get('ledgerMaxIndex')!r}, обход "
                     f"{int(n['ledger']['последний'])} (тот же путь записи, что у ledgerEntries)")
    if _syn.get("drafts") != n.get("draftPaths"):
        drift.append(f"synthesis.drafts: в реестре {len(_syn.get('drafts') or [])} путей, обход даёт "
                     f"{len(n.get('draftPaths') or [])} — поле обязано зеркалить каталог (п. 3.14; "
                     "переснимается apply_corpus тем же обходом)")
    msc = corp["integrityGate"]["mixedScriptCheck"]
    for k in ("ownOccurrences", "scannedFiles", "foreignOccurrences"):
        if msc["jsonLeafScan"].get(k) != n["json"][k]:
            drift.append(f"mixedScriptCheck.jsonLeafScan.{k}: {msc['jsonLeafScan'].get(k)!r}, обход {n['json'][k]}")
    if "outOfScope" in msc:
        for k in ("occurrences", "files"):
            if msc["outOfScope"].get(k) != n["out"][k]:
                drift.append(f"mixedScriptCheck.outOfScope.{k}: {msc['outOfScope'].get(k)!r}, обход {n['out'][k]}")
    if n["sha"] is None:
        drift.append("sha-аудит: пересъём невозможен (shallow-клон или нет локального origin/main) — "
                     "в такой среде блок остаётся недоказанным, и это надо пропечатать, а не промолчать")
    else:
        sc = corp["integrityGate"]["shaCitationAudit20261023"]
        for k in ("uniqueShaTokens", "reachableTokens", "unreachableTokens", "fieldsWithDeadLinks"):
            if sc.get(k) != n["sha"][k]:
                drift.append(f"shaCitationAudit20261023.{k}: {sc.get(k)!r}, обход {n['sha'][k]!r}")
        if sc.get("byBlock") != n["sha"]["byBlock"]:
            drift.append(f"shaCitationAudit20261023.byBlock: {sc.get('byBlock')!r}, обход "
                         f"{n['sha']['byBlock']!r}")
    doc = DOC.read_text(encoding="utf-8")
    want = {re.compile(p, re.M): s for p, s in doc_numbers(corp, n)}
    for pat, s in want.items():
        got = pat.findall(doc)
        if len(got) != 1:
            drift.append(f"документ 18: якорь {pat.pattern!r} нашёл {len(got)} строк вместо одной")
        elif got[0] != s:
            drift.append(f"документ 18 устарел: строка\n  {got[0][:160]}\nдолжна быть\n  {s[:160]}")
    for msg in check_table_91(corp):
        drift.append(msg)
    mir = n["mirror"]
    for msg in mir["bad"]:
        drift.append(msg)
    for k, gap in sorted((mir["gap"] or {}).items()):
        decl = corp["driveMirrors"][k]["разрывСДеревом"]["байт"]
        if decl != gap:
            drift.append(f"driveMirrors.{k}.разрывСДеревом.байт: реестр {decl}, обход {gap} "
                         "(поле объявлено пересъёмным на каждый прогон)")
    pinv = pipeline_inventory()
    decl = corp["reproducibility20261022"].get("pipelineScripts" + KEY_DATE + "r" + CIRCLE) or {}
    if decl.get("файлы") != pinv["файлы"] or decl.get("байт") != pinv["байт"]:
        drift.append("pipelineScripts" + KEY_DATE + "r" + CIRCLE + ": реестр описывает инструменты не этих байт — "
                     "после любой правки скрипта блок обязан быть переснят (declared "
                     f"{decl.get('байт')}, обход {pinv['байт']})")
    if mir["неПрочитано"] and not mir["проверено"]:
        drift.append("зеркала Drive: " + "; ".join(mir["неПрочитано"]) + " — в такой среде поле "
                     "lagBehindGit никем не подтверждено")
    for msg in n["keydate"][1]:
        drift.append(msg)
    env = n["env"]
    edecl = corp["integrityGate"].get(ENV_DECL_BLOCK) or {}
    forgiven = set((edecl.get("снятоЭтимКругом") or {})) | set((edecl.get("снятоКакМёртвое") or {}))
    for pth in env["незаконные"]:
        if pth not in forgiven:
            drift.append(f"число обхода в сверяемом поле: {pth} — оно меряет среду съёма, а не дерево; "
                         "место ему в штампе прогона или в integrityGate." + ENV_DECL_BLOCK + ".поля")
    for pth in env["мертвыеОбъявления"]:
        if pth not in set(edecl.get("снятоКакМёртвое") or []):
            drift.append(f"integrityGate.{ENV_DECL_BLOCK}: объявленное число обхода {pth} не найдено в "
                         "реестре — список объявлений становится разрешением на любое будущее число")
    if edecl.get("поля") != env["живые"]:
        drift.append(f"integrityGate.{ENV_DECL_BLOCK}.поля: реестр объявил {sorted(edecl.get('поля') or {})},"
                     f" обход видит живыми {sorted(env['живые'])} — блок списков тоже обязан пересниматься")

    # «ноль расхождений» обязано быть отличимо от «сверять было нечего»: число групп и число
    # сравнений печатается в PASS и в --report, и считается оно из размера тех же обходов
    n["сверок"] = [
        ("ценз индекса по правилу 25", len(n["census"])),
        ("срез дерева: четыре глоба §1, четыре под-лана, файл аудита", 4 + len(SUBLANES) + 1),
        ("штампованные поля по меткам реестра", len(n["stamp"])),
        ("countsLive — закрытый список правила", 8),
        ("jsonLeafScan и outOfScope", 3 + 2),
        ("числа sha-аудита", 4),
        ("зеркала driveMirrors, прочитанные из blob'а", mir["проверено"] + len(mir["gap"] or {})),
        ("строки документа, которые порождает этот скрипт", len(doc_numbers(corp, n))),
        ("ячейки таблицы §9.1 (сверка, не генерация)", 7 * (len(SUBLANES) + 1) + 2),
        ("числа обхода: где им место (круг 64)", len(n["env"]["пути"]) + n["env"]["объявлено"] + 1),
        ("имена блоков против их штампов (имя не может быть позже штампа)", n["keydate"][0]),
    ]
    return drift


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode == "--rule-trap":
        # ловушка не читает ни реестр, ни дерево: ей довольно собственного определения и текстов
        # соседних инструментов, поэтому она годится и в песочнице с грязным деревом, и в CI до
        # любых тяжёлых шагов. Код — максимум по обоим отделениям: 2 значит «не проверено»,
        # 1 — «проверено и найдено расхождение», 0 — «всё объявлено и всё на месте»
        rc1 = keydate_trap()
        rc2 = plant_registry_trap()
        rc3 = table91_trap()
        rc4 = tree_counts_trap()
        rc5 = self_mutation_trap()
        return max(rc1, rc2, rc3, rc4, rc5)
    if mode not in ("--check", "--write", "--report"):
        raise SystemExit("употребление: atonement_reshoot_state.py "
                         "[--check|--write|--report|--rule-trap]")
    global now
    now = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()
    corp = json.loads(CORPUS.read_text(encoding="utf-8"))
    idx_file = json.loads(INDEX.read_text(encoding="utf-8"))
    if mode == "--report":
        print(report_not_generated(corp))
        nn = registry_numbers(corp, idx_file)
        drift = diff_state_scan(corp, idx_file, nn)
        print("группы сверок: " + "; ".join("%s — %d" % (g, c) for g, c in nn.get("сверок", [])))
        print("расхождений сейчас: %d" % len(drift))
        return 0
    n = registry_numbers(corp, idx_file)
    if mode == "--check":
        drift = diff_state_scan(corp, idx_file, n)
        if drift:
            print("ATONEMENT RE-SHOOT: расхождение —")
            for d in drift:
                print("  -", d)
            return 1
        cens, sha, st, lc = n["census"], (n["sha"] or {}), n["stamp"], n["ledger"]
        print(f"ATONEMENT RE-SHOOT: PASS — {cens['records']} записей / {cens['files']} файлов в индексе, "
              f"{sha.get('uniqueShaTokens', -1)} токенов sha ({sha.get('reachableTokens', -1)} живых, "
              f"{sha.get('unreachableTokens', -1)} мёртвых), {st['корпус']} штампованных полей корпуса, "
              f"леджер {lc['записей']}/{lc['статусов']}, срез дерева и строки документа пересняты тем же "
              f"обходом; сверено {sum(c for _g, c in n['сверок'])} "
              f"{plural(sum(c for _g, c in n['сверок']), 'число', 'числа', 'чисел')} в "
              f"{len(n['сверок'])} {plural(len(n['сверок']), 'группе', 'группах', 'группах')}, "
              f"чисел обхода {n['env']['обходных']} (в штампах прогона {n['env']['вШтампеПрогона']}, "
              f"объявлено {n['env']['объявлено']})")
        return 0
    prev_keys = {k: len(json.dumps(v, ensure_ascii=False, indent=1).encode())
                 for k, v in corp.items()}
    for i in range(8):
        corp = apply_corpus(corp, n)
        # писать надо оба файла на каждом витке: байты корпуса входят в строку документа, а байты
        # документа — в реестр; пока хоть один не записан, следующий виток считает по чужим байтам
        CORPUS.write_text(json.dumps(corp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        DOC.write_text(apply_doc(corp, n), encoding="utf-8")
        corp = json.loads(CORPUS.read_text(encoding="utf-8"))
        idx_file = json.loads(INDEX.read_text(encoding="utf-8"))
        new = registry_numbers(corp, idx_file)
        if diff_state_scan(corp, idx_file, new):
            n = new
            continue
        for k, sz in sorted(((k, len(json.dumps(v, ensure_ascii=False, indent=1).encode()))
                              for k, v in corp.items()), key=lambda kv: kv[1] - prev_keys.get(kv[0], 0)):
            d = sz - prev_keys.get(k, 0)
            if d:
                print(f"   дельта блока {k}: {prev_keys.get(k, 0)} → {sz} ({d:+d})")
        prev_keys = {k: len(json.dumps(v, ensure_ascii=False, indent=1).encode()) for k, v in corp.items()}
        print(f"ATONEMENT RE-SHOOT: сошлось на прогоне #{i} — ценз {n['census']['records']}/"
              f"{n['census']['files']}, штампов {n['stamp']['корпус']}, байт корпуса {num(n['tree']['corpBytes'])}, "
              f"байт индекса {num(n['tree']['idxBytes'])}, документ {n['tree']['doc'][0]} B / "
              f"{n['tree']['doc'][1]} строк")
        break
    else:
        raise SystemExit("ATONEMENT RE-SHOOT: за 8 прогонов не сошлось — определение где-то читает "
                         "то, что само же меняет; искать руками")
    return 0


now = None
if __name__ == "__main__":
    sys.exit(main())
