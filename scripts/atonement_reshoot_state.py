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
CIRCLE = "63"


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


def tree_counts() -> dict:
    def stat(paths):
        ps = [Path(p) for p in paths]
        return len(ps), sum(p.stat().st_size for p in ps)

    docs = stat(sorted(glob.glob(str(ROOT / "docs" / "research" / "atonement" / "*.md"))))
    n_num = len([p for p in glob.glob(str(ROOT / "docs" / "research" / "atonement" / "*.md"))
                 if re.search(r"/\d\d_", p)])
    rootmd = stat(sorted(glob.glob(str(ROOT / "ИСКУПЛЕНИЕ" / "*.md"))))
    b17 = (ROOT / "ИСКУПЛЕНИЕ" / "17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md").stat().st_size
    docbytes = DOC.stat().st_size
    doclines = len(DOC.read_text(encoding="utf-8").split("\n")) - 1
    docmd5 = hashlib.md5(DOC.read_bytes()).hexdigest()
    per = {}
    for lan in SUBLANES:
        per[lan] = stat(sorted(glob.glob(str(ROOT / "ИСКУПЛЕНИЕ" / lan / "*.md"))))
    sub = (sum(v[0] for v in per.values()), sum(v[1] for v in per.values()))
    dr_paths = sorted(glob.glob(str(ROOT / "ИСКУПЛЕНИЕ" / "synthesis" / "drafts" / "*.md")))
    dr = stat(dr_paths)
    dr_lines = sum(Path(p).read_text(encoding="utf-8").count("\n") for p in dr_paths)
    dr_lines_split = sum(len(Path(p).read_text(encoding="utf-8").split("\n")) for p in dr_paths)
    dr_sizes = [Path(p).stat().st_size for p in dr_paths]
    data = stat(sorted(glob.glob(str(ROOT / "ИСКУПЛЕНИЕ" / "data" / "*"))))
    corp_bytes = CORPUS.stat().st_size
    idx_bytes = INDEX.stat().st_size
    mass = (ROOT / "docs" / "research" / "atonement" / "35_four_point_authors_mass_registry.md").read_text(encoding="utf-8")
    mass_bytes = (ROOT / "docs" / "research" / "atonement" / "35_four_point_authors_mass_registry.md").stat().st_size
    return {
        "docs": docs, "docsNumbered": n_num, "rootmd": rootmd, "b17": b17,
        "doc": (docbytes, doclines, docmd5), "perLan": per, "sub": sub,
        "drafts": dr, "draftsLines": dr_lines, "draftsLinesSplit": dr_lines_split, "draftsMin": round(min(dr_sizes) / 1000, 1),
        "draftsMax": round(max(dr_sizes) / 1000),
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



PIPELINE_FILES = ("scripts/validate_atonement_corpus_integrity.py", "scripts/atonement_claim_register.py",
                  "scripts/run_atonement_mutation_battery.py", "scripts/atonement_reshoot_state.py",
                  "scripts/atonement_drive_mirror_round63.py", "scripts/atonement_library_index_round63.py")


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
    out["json"] = json_leaf_scan()
    out["out"] = out_of_scope_mixed()
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
    li["countsNote20261026r" + CIRCLE] = (
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
    key = "reshootCounters20261026r" + CIRCLE
    extra = {
        "что": ("числа, которые круг 63 переснимает по своим определениям и которым не место в "
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

    sf = corp["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]
    sf.update(dict(sorted(n["stamp"].items())))
    # поле how — журнал пересъёмов, и оно обязано кончаться этим кругом: иначе следующая рука,
    # которая придёт править число, увидит обрыв на полуслове. Отметки времени здесь не добавляются:
    # строка без measuredAt не двигает тот самый счётчик, который она описывает
    clause = (f"круг {CIRCLE}: {n['stampPrev']} → {n['stamp']['корпус']} (запись о слепке круга 63 в "
              "driveMirrors, поправка перечисления в записи круга 61, метод и countsNote в блоке индекса, "
              "пара отметок в новом блоке seriesAudit и этой строке — отметок не добавляется, иначе "
              "собственный пересъём сдвигал бы число, которое он переснимает)")
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
        sc["gitObjectsConsidered"] = n["sha"]["gitObjectsConsidered"]
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
    blk = corp["reproducibility20261022"].get("pipelineScripts20261026r" + CIRCLE) or {}
    corp["reproducibility20261022"]["pipelineScripts20261026r" + CIRCLE] = {
        "что": ("инструменты, которыми сняты числа этого круга: пересъёмщик, два писателя записей, гейт, "
                "реестр доводов и батарея мутаций. Блок переснимается каждый прогон, потому что md5 файла "
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
    idx_note = ("числа снимает scripts/atonement_reshoot_state.py --write, сверяет --check (шаг гейта); "
                "до этого в строке стоял срез круга 60 (корпус 1 121 533 B)")
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


def check_table_91(corp: dict) -> list:
    """Таблицу §9.1 этот скрипт не порождает (её производитель — утраченный финалайзер круга 61),
    но право её сверить оставляет: каждая ячейка обязана равняться полю реестра."""
    cpr = corp["integrityGate"]["scopeOfMeasurementRules"]["claimsPerRegistry"]
    rows, total = {}, None
    for line in DOC.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `") and "**всего**" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        try:
            vals = [int(c.replace("*", "").replace(" ", "")) for c in cells[1:]]
        except ValueError:
            continue
        if "всего" in cells[0]:
            total = vals
        else:
            rows[cells[0].strip("`")] = vals
    bad = []
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
            "fourPointMassRegistry20261023.cardProseCrossCheck20261026r60.числа"]
    lines = ["этот скрипт переснимает только перечисленное; из разделов 9.1 и 9.2 документа 18 он "
             "проверяет (но не пишет) таблицу §9.1, а остальное — проза, порождённая утраченным "
             "финалайзером круга 61, и живёт до ближайшей ручной правки:", "  реестровые блоки-источник: "
             + ", ".join("`%s`" % k for k in keys), "  поля, которые он намеренно не трогает: "
             "`claimsPerRegistry.всего`, `сверкаСКарточками` (ими заведует atonement_claim_register.py), "
             "`driveMirrors.*`, `libraryIndex20261023.countsNote*`, `shaCitationAudit20261023.note` "
             "в части формулировки"]
    return "\n".join(lines)


# ------------------------------------------------------------------ режимы

def diff_state(corp: dict, idx_file: dict, n: dict):
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
    # jsonLeafScan/outOfScope в apply_corpus, подменил их и в diff_state (replace без count=1
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
        for k in ("uniqueShaTokens", "reachableTokens", "unreachableTokens", "fieldsWithDeadLinks",
                  "gitObjectsConsidered"):
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
    decl = corp["reproducibility20261022"].get("pipelineScripts20261026r" + CIRCLE) or {}
    if decl.get("файлы") != pinv["файлы"] or decl.get("байт") != pinv["байт"]:
        drift.append("pipelineScripts20261026r" + CIRCLE + ": реестр описывает инструменты не этих байт — "
                     "после любой правки скрипта блок обязан быть переснят (declared "
                     f"{decl.get('байт')}, обход {pinv['байт']})")
    if mir["неПрочитано"] and not mir["проверено"]:
        drift.append("зеркала Drive: " + "; ".join(mir["неПрочитано"]) + " — в такой среде поле "
                     "lagBehindGit никем не подтверждено")
    # «ноль расхождений» обязано быть отличимо от «сверять было нечего»: число групп и число
    # сравнений печатается в PASS и в --report, и считается оно из размера тех же обходов
    n["сверок"] = [
        ("ценз индекса по правилу 25", len(n["census"])),
        ("срез дерева: четыре глоба §1, четыре под-лана, файл аудита", 4 + len(SUBLANES) + 1),
        ("штампованные поля по меткам реестра", len(n["stamp"])),
        ("countsLive — закрытый список правила", 8),
        ("jsonLeafScan и outOfScope", 3 + 2),
        ("числа sha-аудита", 5),
        ("зеркала driveMirrors, прочитанные из blob'а", mir["проверено"] + len(mir["gap"] or {})),
        ("строки документа, которые порождает этот скрипт", len(doc_numbers(corp, n))),
        ("ячейки таблицы §9.1 (сверка, не генерация)", 7 * (len(SUBLANES) + 1) + 2),
    ]
    return drift


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode not in ("--check", "--write", "--report"):
        raise SystemExit("употребление: atonement_reshoot_state.py [--check|--write|--report]")
    global now
    now = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()
    corp = json.loads(CORPUS.read_text(encoding="utf-8"))
    idx_file = json.loads(INDEX.read_text(encoding="utf-8"))
    if mode == "--report":
        print(report_not_generated(corp))
        nn = registry_numbers(corp, idx_file)
        drift = diff_state(corp, idx_file, nn)
        print("группы сверок: " + "; ".join("%s — %d" % (g, c) for g, c in nn.get("сверок", [])))
        print("расхождений сейчас: %d" % len(drift))
        return 0
    n = registry_numbers(corp, idx_file)
    if mode == "--check":
        drift = diff_state(corp, idx_file, n)
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
              f"обходом; сверено {sum(c for _g, c in n['сверок'])} чисел в {len(n['сверок'])} группах")
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
        if diff_state(corp, idx_file, new):
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
