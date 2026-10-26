#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Батарея мутаций «Искупления» — прогон против рабочего дерева.

С круга 27 батарея лежит в репозитории. До этого она семь кругов жила в /tmp
(/tmp/mutations22.py … /home/user/cap26/mutations26b.py), и дважды — в кругах 26 и
26-после-отката — гибла вместе с песочницей вместе со своим логом: восстановить
«что именно проверялось» тогда было нечем. Результат прогона вносится в
ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json, а способ прогона — вот сюда, чтобы его
можно было повторить в любом клоне.

Три правила, которые вписаны сюда как код, а не как комментарий:

1. Значения якорей читаются из файлов в момент прогона. Литералы гниют за один
   круг: в круге 26 три случая «ловили» сами себя, потому что байты индекса,
   md5 зеркала и текст абзаца `17_` переехали раньше, чем был запущен прогон.
2. Если анкор случая не найден, случай НЕ считается прошедшим: он печатает
   «не проверен» и уводит прогон в ненулевой код. Молчаливый PASS — это ложь
   о покрытии.
3. Мутация обязана оставлять изменяемый файл разбираемым (JSON — валидным,
   markdown — с тем же числом разделов). FAIL по сломанному синтаксису ничего
   не доказывает: он подтверждает только наличие парсера.

Прогон ничего не оставляет в дереве: побайтовый бэкап всех четырёх файлов,
restore() после каждого случая, filecmp по всем четырём и контрольный прогон
гейта в конце.
"""
import argparse
import filecmp
import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG_MD = ROOT / "docs/research/atonement/35_four_point_authors_mass_registry.md"
IDX = ROOT / "ИСКУПЛЕНИЕ/data/atonement-library-index.json"
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
DOC17 = ROOT / "ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md"
# С круга 59 батарея трогает не только главный реестр: реестр доводов лежит в реестре
# своего лана, а ловится он правкой прозы, поэтому в откат входят четыре под-реестра и
# один файл прозы. Молча не откатанный файл — это не проверка, а порча рабочего дерева.
LANE_REG = {lan: ROOT / ("ИСКУПЛЕНИЕ/%s/data/%s-corpus-v1.json" % (lan, lan)) for lan in ("ot", "nt", "fathers", "synthesis")}
FATHERS_DOC = ROOT / "ИСКУПЛЕНИЕ/fathers/09_SILENCES_AND_FALSE_FRIENDS.md"
FILES = [REG_MD, IDX, COR, DOC17, FATHERS_DOC] + [LANE_REG[k] for k in sorted(LANE_REG)]
CLAIMS_BLOCK = "claimRegister20261026"
GATE = [sys.executable, "-B", "scripts/validate_atonement_corpus_integrity.py"]


def gate():
    """Код и вывод гейта на текущем дереве."""
    p = subprocess.run(GATE, cwd=str(ROOT), capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def first_errors(out, n=14):
    return [x.strip()[2:].strip() for x in out.split("\n") if x.strip().startswith("- ")][:n]


def sub(text, old, new, path=""):
    """Ровно одно вхождение — иначе случай не проверен, а подменён."""
    c = text.count(old)
    if c != 1:
        raise AssertionError("не проверен: анкор встречается %d раз (%s)" % (c, path))
    return text.replace(old, new, 1)


def jsub(obj, path, key, value):
    """Правка одного поля по пути-цепочке ключей."""
    node = obj
    for k in path:
        node = node[k]
    if key not in node:
        raise AssertionError("не проверен: поля %s нет" % key)
    old = node[key]
    node[key] = value
    return old


# --- якоря, снятые с дерева в момент прогона ---------------------------------------------
def anchors():
    reg = json.loads(COR.read_text(encoding="utf-8"))
    idx = json.loads(IDX.read_text(encoding="utf-8"))
    mdtxt = REG_MD.read_text(encoding="utf-8")
    recs = idx.get("records") or []
    # то же уточнение, что и в случае 11: снятое зеркало круга 53 помечено ролью, а не именем,
    # и без этого якорь брал первую попавшуюся запись — размер устаревшего слепка
    mir = [r for r in recs if isinstance(r, dict) and "35_four_point_authors_mass_registry" in str(r.get("name", ""))
           and "УСТАРЕЛО" not in str(r.get("name", "")) and "superseded" not in str(r.get("role", ""))]
    sw = reg["libraryIndex20261023"]
    return {
        "reg": reg, "idx": idx, "mdtxt": mdtxt, "recs": recs,
        "rows": len(re.findall(r"^\|\s*FP-\d+\s*\|", mdtxt, re.M)),
        "stamped": reg["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]["корпус"],
        "bytesSum": sw["driveBytesSum"], "records": sw["records"], "mirrorRows": len(mir),
        "liveBytes": (mir[0].get("bytes") if mir else None), "liveRec": (mir[0].get("name") if mir else None),
        "corpusBytes": len(COR.read_bytes()),
        "lines17": len(DOC17.read_text(encoding="utf-8").rstrip("\n").split("\n")),
    }


def md_row_sample(text):
    m = re.search(r"^\|\s*FP-\d+\s*\|[^\n]*$", text, re.M)
    if not m:
        raise AssertionError("не проверен: ни одной строки-носителя в реестре")
    return m.group(0)


def md_row_with_class(text, cls):
    """Строка, у которой одна из колонок — ровно этот класс (в кавычках-бэктиках)."""
    for m in re.finditer(r"(?m)^\|\s*FP-\d+\s*\|.*$", text):
        cells = m.group(0).split("|")
        if any(c.strip().strip("`").strip("*") == cls for c in cells):
            return m.group(0), cells
    raise AssertionError("не проверен: строки с классом %s в реестре нет" % cls)


def jsurgical(path, block_key, field, new_scalar_text):
    """Правка одного поля блока на месте, без пересборки всего файла. Whole-file
    json.dumps переставил бы форму всему реестру, и ловить пришлось бы не то, что
    проверяется, а формат: мутация обязана быть точечной ровно так же, как точечен
    реестр, который она проверяет."""
    import re as _re
    raw = path.read_text(encoding="utf-8")
    if '"%s"' % block_key not in raw:
        raise AssertionError("не проверен: блока %s в %s нет, сеять некуда" % (block_key, path.name))
    i = raw.index('"%s"' % block_key)
    j = raw.index("{", i)
    depth, in_str, esc, end = 0, False, False, None
    for k in range(j, len(raw)):
        ch = raw[k]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = k + 1
                break
    span = raw[j:end]
    m = _re.search(r'"%s": (?:[^,\n]|\\.)+' % field, span)
    if not m:
        raise AssertionError("не проверен: поля %s в блоке %s нет" % (field, block_key))
    if span.count(m.group(0)) != 1:
        raise AssertionError("не проверен: поле встречается в блоке %d раз" % span.count(m.group(0)))
    old_text = m.group(0)
    path.write_text(raw[:j] + span.replace(old_text, '"%s": %s' % (field, new_scalar_text)) + raw[end:],
                    encoding="utf-8")


def jsurgical_first(path, block_key, field, new_scalar_text):
    """То же, но берётся первое вхождение поля — для строк реестра, где поле
    «строка» встречается по разу на запись и править надо ровно одну запись."""
    raw = path.read_text(encoding="utf-8")
    if '"%s"' % block_key not in raw:
        raise AssertionError("не проверен: блока %s в %s нет, сеять некуда" % (block_key, path.name))
    i = raw.index('"%s"' % block_key)
    m = re.search(r'"%s": (?:[^,\n]|\\.)+' % field, raw[i:])
    if not m:
        raise AssertionError("не проверен: поля %s в блоке нет" % field)
    path.write_text(raw[: i + m.start()] + '"%s": %s' % (field, new_scalar_text) + raw[i + m.end():],
                    encoding="utf-8")


# --- случаи ------------------------------------------------------------------------------
def cases():
    """Каждый случай: (имя, ожидаемый вердикт, ожидаемая подстрока, функция правки).

    expected is None → случай обязан дать PASS (это не победа, а дыра; они нужны,
    чтобы открытое место было записано, а не забыто). expected вида "!фраза" →
    случай пройден, если ни одна ошибка гейта эту фразу не содержит: так
    документируется отсутствие ловушки там, где дерево и так краснеет по другой
    причине (правка реестра всегда поднимает правило 25: зеркало названо байтами
    и md5 файла, и это делает реестр защищённым от подмены, но не говорит, что
    именно в нём не так).
    """
    A = anchors()
    out = []

    def add(name, expect, fn, note=""):
        out.append((name, expect, fn, note))

    # 1. Число строк-носителей в реестре.
    def m_rows():
        t = REG_MD.read_text(encoding="utf-8")
        ln = md_row_sample(t)
        REG_MD.write_text(sub(t, ln, ln + "\n" + ln, "реестр"), encoding="utf-8")

    add("registryRowsDoubled", "liveNumbers", m_rows, "строка-носитель удвоена")

    # 2. Класс строки: A2 → A1 без основания.
    def m_class():
        t = REG_MD.read_text(encoding="utf-8")
        line, cells = md_row_with_class(t, "A2")
        new = "|".join(" `A1` " if c.strip().strip("`").strip("*") == "A2" else c for c in cells)
        REG_MD.write_text(sub(t, line, new, "реестр"), encoding="utf-8")

    add("registryClassPromoted", "классы достоверности разошлись", m_class, "A2 поднят до A1 без печатного носителя")

    # 3. Живой счётчик строк реестра в JSON (снимается обходом, литералов нет).
    def m_reglines():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        jsub(raw, ["driveMirrors", "massRegistry20261023"], "fileLines", A["rows"] + 1)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("registryFileLinesClaim", None, m_reglines, "число строк git-файла завышено на 1")

    # 4. Сумма байт индекса.
    def m_bytessum():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        jsub(raw, ["libraryIndex20261023"], "driveBytesSum", int(A["bytesSum"]) + 1)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("indexBytesSumOff", "driveBytesSum", m_bytessum, "сумма байт индекса сдвинута на 1")

    # 5. Число записей индекса (одна запись удалена из файла, счётчик оставлен).
    def m_records():
        raw = json.loads(IDX.read_text(encoding="utf-8"))
        recs = raw["records"]
        if int(A["records"]) != len(recs):
            raise AssertionError("не проверен: записей в файле %d, в сводке %s" % (len(recs), A["records"]))
        raw["records"] = recs[:-1]
        IDX.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("indexRecordDropped", "libraryIndex20261023.records", m_records, "последняя запись индекса удалена, счётчик не тронут")

    # 6. stamped-поле корпуса.
    def m_stamped():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        jsub(raw, ["integrityGate", "scopeOfMeasurementRules", "stampedFieldsPerRegistry"], "корпус",
             int(A["stamped"]) + 2)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("stampedFieldsInflated", "stampedFieldsPerRegistry", m_stamped, "счётчик размеченных полей завышен")

    # 7. Мёртвая sha-ссылка в датированном блоке корпуса (внутри строки, JSON цел).
    def m_deadsha():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        b = raw["sandboxRebuild20261024"]
        old = b["how"] if isinstance(b.get("how"), str) else b["command"]
        key = "how" if isinstance(b.get("how"), str) else "command"
        b[key] = old + " — сверка на deadc0de (такого объекта в этом клоне нет)"
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("deadShaLinkAdded", "deadc0de", m_deadsha, "в датированный блок вписана недостижимая sha")

    # 8. Датированный блок без способа пересъёма.
    def m_nohow():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        b = raw["driveMirrors"]["massRegistry20261023"]
        if "how" not in b:
            raise AssertionError("не проверен: у блока нет поля how")
        del b["how"]
        for k in ("command", "howRule", "measuredBy", "method", "recheckCommand", "verification"):
            b.pop(k, None)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("datedBlockMethodless", "датировано", m_nohow, "из датированного блока изъяты все способы пересъёма")

    # 9. Смешанное письмо в собственном прозовом тексте реестра.
    def m_mixed():
        t = REG_MD.read_text(encoding="utf-8")
        m = re.search(r"(?m)^([А-ЯЁ][^|#`]{40,120}\.)\s*$", t)
        if not m:
            raise AssertionError("не проверен: подходящего прозового предложения в реестре нет")
        s = m.group(1)
        REG_MD.write_text(sub(t, s, s.replace(".", " отката.", 1), "реестр"), encoding="utf-8")

    add("mixedScriptInProseAbsent", "!письм", m_mixed, "в прозу реестра внесено слово с латинской a вместо русской")

    # 10. Размер `17_` в сводке документа.
    def m_doc17():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        jsub(raw, ["reconciliationDocument20261022"], "lines", int(A["lines17"]) + 3)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("doc17LinesClaim", "reconciliationDocument20261022", m_doc17, "число строк `17_` в сводке завышено")

    # 11. Имя живого зеркала: байты в имени не равны git-файлу.
    def m_mirrorname():
        raw = json.loads(IDX.read_text(encoding="utf-8"))
        # живым зеркалом считается единственная запись без пометки в имени и без роли superseded:
        # с круга 53 в индексе появился второй способ помечать снятое (role …-superseded при
        # ненарушенном имени), и старый предикат по одному имени находил два живых
        rec = [r for r in raw["records"] if "35_four_point_authors_mass_registry" in str(r.get("name", ""))
               and "УСТАРЕЛО" not in str(r.get("name", ""))
               and "superseded" not in str(r.get("role", ""))]
        if len(rec) != 1:
            raise AssertionError("не проверен: живых записей о зеркале реестра %d, ожидалась одна" % len(rec))
        rec = rec[0]
        fld = "driveBytesClaimed" if "driveBytesClaimed" in rec else "bytes"
        if int(rec[fld]) != int(A["liveBytes"]):
            raise AssertionError("не проверен: в записи %s = %s, в якорях %s" % (fld, rec[fld], A["liveBytes"]))
        rec[fld] = int(rec[fld]) + 1
        IDX.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("mirrorBytesClaimed", None, m_mirrorname, "размер в записи индекса о живом зеркале сдвинут на 1 байт")

    # 12. Пустая группа мутаций (гейт обязан не дать спрятать расхождение).
    def m_group():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        g = raw["integrityGate"]["rules"]["mutationGroups"]
        g.append({"label": "", "count": 0})
        raw["integrityGate"]["rules"]["mutationGroups"] = g
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("emptyMutationGroup", "пустая группа", m_group, "в разложение добавлена пустая группа")

    # 13. Разложение и итог разошлись.
    def m_total():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        jsub(raw, ["integrityGate", "rules"], "mutationTotal",
             int(raw["integrityGate"]["rules"]["mutationTotal"]) - 16)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("mutationTotalMismatch", "разложение и итог", m_total, "итог уменьшен на 16, разложение не тронуто")

    # 14. Убрать из реестра строку очереди (C-строка), оставив счётчик.
    def m_queue():
        t = REG_MD.read_text(encoding="utf-8")
        line, cells = md_row_with_class(t, "C")
        i = t.index(line + "\n")
        REG_MD.write_text(t[:i] + t[i + len(line) + 1:], encoding="utf-8")

    add("queueRowRemoved", "нумерация строк реестра не непрерывна", m_queue, "строка C удалена — проверка обязана увидеть и счётчики, и строку")

    # 15. ДЫРА, объявленная с круга 25: поле bytes в driveMirrors гейтом не сверяется
    # (размер и md5 читаются из имени зеркала). Случай обязан дать PASS.
    def m_jsonbytes():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        jsub(raw, ["driveMirrors", "massRegistry20261023"], "bytes",
             int(raw["driveMirrors"]["massRegistry20261023"]["bytes"]) + 1)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("corpusMirrorBytesUntouched", None, m_jsonbytes,
        "bytes в driveMirrors сдвинуты: проходил и пройдёт — открытое место записано")

    # 16. ДЫРА: правка прозового числа «семь мест» без правки таблицы снимка гейтом не
    # ловится (сверка прозы с таблицами — читательская). Случай обязан дать PASS.
    def m_prosecount():
        t = REG_MD.read_text(encoding="utf-8")
        m = re.search(r"семь мест", t)
        if not m:
            raise AssertionError("не проверен: в реестре нет строки «семь мест» (она была вписана кругом 26)")
        REG_MD.write_text(t[:m.start()] + "пять мест" + t[m.end():], encoding="utf-8")

    add("proseCountVsTableAbsent", "!семь", m_prosecount, "прозовое число правится без таблицы: не ловится")

    # 17. Имя живого зеркала врёт о md5, при этом запись имеет роль registry-mirror:
    # сверка обязана краснеть. Поймано кругом 30 (до перестановки роли молчало).
    def m_mirrorname_md5():
        raw = json.loads(IDX.read_text(encoding="utf-8"))
        live = [r for r in raw["records"] if r.get("role") == "registry-mirror" and not r.get("lagBehindGit")
                and "35_four_point" in str(r.get("gitFile", ""))]
        if len(live) != 1:
            raise AssertionError("не проверен: живых зеркал с ролью registry-mirror найдено %d, ожидалось одно"
                                 % len(live))
        rec = live[0]
        m = re.search(r"md5 ([0-9a-f]{32})", str(rec["name"]))
        if not m:
            raise AssertionError("не проверен: в имени зеркала нет md5 — подложить ложь некуда")
        rec["name"] = rec["name"].replace(m.group(1), "0" * 32)
        IDX.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("mirrorNameMd5LieCaught", "зеркало в Drive названо md5", m_mirrorname_md5,
        "в имени живого зеркала md5 обнулён: правило 25 обязано увидеть расхождение с деревом")

    # 18. ДЫРА, перенесённая кругом 30: та же ложь в имени, но у записи снята роль
    # registry-mirror — сравнение не запускается, и гейт зеленеет. Классификатор
    # проставляет автор записей, поэтому «зеркало проверено» по-прежнему означает
    # «я завела запись с нужной ролью». Случай обязан дать PASS.
    def m_mirror_role_stripped():
        raw = json.loads(IDX.read_text(encoding="utf-8"))
        live = [r for r in raw["records"] if r.get("role") == "registry-mirror" and not r.get("lagBehindGit")
                and "35_four_point" in str(r.get("gitFile", ""))]
        if len(live) != 1:
            raise AssertionError("не проверен: живых зеркал с ролью registry-mirror найдено %d" % len(live))
        rec = live[0]
        m = re.search(r"md5 ([0-9a-f]{32})", str(rec["name"]))
        if not m:
            raise AssertionError("не проверен: в имени зеркала нет md5")
        rec["name"] = rec["name"].replace(m.group(1), "0" * 32)
        rec["role"] = "mirror-of-git"
        IDX.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("mirrorLieInvisibleWithoutRole", None, m_mirror_role_stripped,
        "та же ложь в имени без роли registry-mirror: не ловится, и это записанное открытое место круга 30")

    # 19. Правило 26, ложь против собственного канала: в команду переписи Тэйлор дописано, что
    # .scratch/q49stamp.py в снимок ceabb56ea не попал, — а снимок его отдаёт. Поймано кругом 58.
    def m_lossclaim_vs_snapshot():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        node = raw["fourPointMassRegistry20261023"]["taylorVolumeCensusRound51Finding20261025"]
        if ".scratch/q49stamp.py" in node["command"]:
            raise AssertionError("не проверен: поле уже говорит о q49stamp.py, сеять ложь некуда")
        jsub(raw, ["fourPointMassRegistry20261023", "taylorVolumeCensusRound51Finding20261025"],
             "command",
             node["command"] + "; и .scratch/q49stamp.py в снимок ceabb56ea не попал (тот же канал)")
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("lossClaimContradictsSnapshot", "а снимок его отдаёт", m_lossclaim_vs_snapshot,
        "объявлено отсутствие файла, который снимок отдаёт: правило 26 обязано краснеть")

    # 20. Правило 26, утрата без канала: у блока сверки корзинок круга 47 способ пересъёма
    # вычищен из обоих полей. Поймано кругом 58.
    def m_lossclaim_no_channel():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        node = raw["fourPointMassRegistry20261023"]["carrierPartitionReconciliation20261025r47"]
        if "command" not in node or "how" not in node:
            raise AssertionError("не проверен: у блока нет пары how+command, сеять некуда")
        node["command"] = ""
        node["how"] = ("сводка корзинок круга 46 по выгрузке .scratch/q46dump.json утрачена "
                       "безвозвратно: файла нет ни в дереве, ни в снимке, ни где-либо ещё")
        for _k, _v in node.items():
            if any(_t in str(_v) for _t in ("git ", "gh api", "curl", "http", "python3")):
                raise AssertionError("не проверен: канал остался в поле %s" % _k)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("lossClaimWithoutChannel", "канала повторения не называет", m_lossclaim_no_channel,
        "«утрачено» без команды, которой это можно переспросить: правило 26 краснеет")

    # 21. ДЫРА офлайна, записанная кругом 58: тот же класс лжи, что и в случае 19, но про
    # живом адресе, объявленном мёртвым. Без флага --net-loss-claims гейт обязан остаться
    # зелёным: ловит только прогон с сетью, а CI сети не имеет. Случай обязан дать PASS.
    def m_stale_claim_offline():
        raw = json.loads(COR.read_text(encoding="utf-8"))
        live = raw["fourPointMassRegistry20261023"]["catalogReshootRound5820261026"]["источник"]["адрес"]
        node26 = raw["fourPointMassRegistry20261023"]["externalIndexRound46Finding20261025"]
        if "contents/TCP.csv" not in live:
            raise AssertionError("не проверен: живой адрес каталога не читается из корпуса")
        if "404" in node26["recheckCommand"]:
            raise AssertionError("не проверен: поле уже объявляет 404, подклад не отличается от правды")
        jsub(raw, ["fourPointMassRegistry20261023", "externalIndexRound46Finding20261025"],
                 "recheckCommand",
                 "источник недоступен навсегда: %s даёт 404, поэтому числа остаются записью о съёме"
                 % live)
        COR.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    add("staleLossClaimInvisibleOffline", None, m_stale_claim_offline,
        "протухшее 404 без флага сети: не ловится, и это записанная граница офлайна (переспрос — "
        "--net-loss-claims)")



    # 22. Реестр доводов, сводка против обхода: в ot-блоке число строк занижено на 1,
    # сами строки не тронуты. Ловится правилом 27, а не md5 файла.
    def m_claim_summary():
        blk = json.loads(LANE_REG["ot"].read_text(encoding="utf-8")).get(CLAIMS_BLOCK) or {}
        if not isinstance(blk.get("строк"), int):
            raise AssertionError("не проверен: в ot-реестре доводов нет сводки «строк»")
        jsurgical(LANE_REG["ot"], CLAIMS_BLOCK, "строк", str(blk["строк"] - 1))

    add("claimsSummaryUnderstated", "сводка «строк» записана", m_claim_summary,
        "реестр доводов говорит о себе на одну строку меньше, чем их в прозе")

    # 23. Локатор строки сдвинут на 1: файл тот, заголовок тот, номер не тот. Ровно та
    # болезнь, от которой в круге 45 страдали чужие реестры, а проверять её было нечем.
    def m_claim_locator():
        blk = json.loads(LANE_REG["nt"].read_text(encoding="utf-8")).get(CLAIMS_BLOCK) or {}
        rows = blk.get("строки") or []
        if not rows or not isinstance(rows[0].get("строка"), int):
            raise AssertionError("не проверен: в nt-реестре нет строк с номером")
        jsurgical_first(LANE_REG["nt"], CLAIMS_BLOCK, "строка", str(rows[0]["строка"] + 1))

    add("claimsLocatorShiftedByOne", "поле «строка» записано", m_claim_locator,
        "номер строки локатора сдвинут: побайтовая сверка обязана это увидеть")

    # 24. Проза выросла, а реестр нет: в файл под-лана дописан раздел уровня ##. Это
    # обратная сторона покрытия — без неё реестр был бы списком того, что удобно считать.
    def m_prose_heading():
        t = FATHERS_DOC.read_text(encoding="utf-8")
        if "\n## TST-99." in t:
            raise AssertionError("не проверен: раздел уже в файле")
        FATHERS_DOC.write_text(t.rstrip("\n") + "\n\n## TST-99. Раздел, заведённый без строки реестра\n\n"
                               "Временная запись: гейт обязан требовать строку реестра на каждый заголовок.\n",
                               encoding="utf-8")

    add("proseHeadingWithoutRegisterRow", "обход лана даёт", m_prose_heading,
        "новый довод в прозе не записан в реестр — покрытие проверяется в обе стороны")

    # 25. Новый вердиктный маркер, которого нет в классификации. Классификация обязана
    # объяснять каждый маркер, иначе «прочее» съедает ровно то, что надо замечать.
    def m_unknown_marker():
        t = FATHERS_DOC.read_text(encoding="utf-8")
        if not re.search(r"(?m)^## ", t):
            raise AssertionError("не проверен: в файле нет ни одного раздела уровня ##")
        # дописываем в конец: строки выше не сдвигаются, и ловиться должно ровно отсутствие
        # класса у маркера, а не массовый разъезд локаторов — иначе случай проверяет не то
        t = t.rstrip("\n") + "\n\nСостояние новой формы: `QUARANTINE_UNTIL_RESHOT`.\n"
        FATHERS_DOC.write_text(t, encoding="utf-8")

    add("undeclaredVerdictMarker", "не отнесено ни к одному классу", m_unknown_marker,
        "в прозе появился вердикт, которого нет в словаре реестра")

    # 26. Блок реестра доводов удалён из под-реестра совсем: проверка обязана краснеть
    # на отсутствии счёта, а не молчать «нарушений нет».
    def m_block_missing():
        import sys as _sys
        _sys.path.insert(0, str(ROOT / "scripts"))
        import atonement_claim_register as _acr
        raw = LANE_REG["synthesis"].read_text(encoding="utf-8")
        if '"%s"' % CLAIMS_BLOCK not in raw:
            raise AssertionError("не проверен: блока и так нет")
        a, b = _acr.block_span(raw, CLAIMS_BLOCK)
        LANE_REG["synthesis"].write_text(raw[:a].rstrip() + "\n" + raw[b:].lstrip("\n"), encoding="utf-8")

    add("claimsBlockMissingEntirely", "нет блока " + CLAIMS_BLOCK, m_block_missing,
        "реестра доводов нет вовсе: ноль обязан быть ошибкой, а не зелёным прогоном")


    # 27. Выдуманная строка реестра: в nt-блок дописан довод, которого в прозе нет, а
    # сводка увеличена так, чтобы счётчик не разошёлся. Обратный ход сверки ловит именно это.
    def m_claim_row_invented():
        raw = LANE_REG["nt"].read_text(encoding="utf-8")
        m = re.search(r'"строк": (\d+)', raw[raw.index('"%s"' % CLAIMS_BLOCK):])
        if not m:
            raise AssertionError("не проверен: сводка «строк» не читается")
        row = ('{"код": "CL-FAKE@00_NT_AUTHORITY_2026-10-07", "лан": "nt", '
               '"файл": "ИСКУПЛЕНИЕ/nt/00_NT_AUTHORITY_2026-10-07.md", "строка": 1, '
               '"срез": "Заголовок, которого в файле нет", "класс": "ЗАКРЫТО", "маркеров": 0, '
               '"токены": [], "машинно": false, "машинноПоФайлу": true}')
        i = raw.index('"строки": [', raw.index('"%s"' % CLAIMS_BLOCK)) + len('"строки": [')
        out = (raw[:i] + "\n            " + row + "," + raw[i:]
               .replace('"строк": %s' % m.group(1), '"строк": %d' % (int(m.group(1)) + 1), 1))
        LANE_REG["nt"].write_text(out, encoding="utf-8")

    add("claimsRowInventedInBlock", "обход прозы её не находит", m_claim_row_invented,
        "в реестр доводов вписана несуществующая строка: обратный ход сверки обязан краснеть")

    # 28. Карточка ot дописывает вердикт, которого проза лана не знает, а реестр доводов
    # не переснят. Сверка двух учётов обязана краснеть на расхождение, а не «ну и ладно».
    def m_card_state_without_reshoot():
        raw = LANE_REG["ot"].read_text(encoding="utf-8")
        start = raw.find('"cards": [')
        if start == -1:
            raise AssertionError("не проверен: в ot-корпусе нет списка cards")
        i = raw.find('"holds": ["EVIDENCE_HOLD"', start)
        if i == -1:
            raise AssertionError("не проверен: у первой карточки нет однострочного holds")
        if "ZZZ_UNSEEN_HOLD" in raw:
            raise AssertionError("не проверен: маркер уже в файле")
        j = i + len('"holds": [')
        LANE_REG["ot"].write_text(raw[:j] + '"ZZZ_UNSEEN_HOLD", ' + raw[j:], encoding="utf-8")

    add("cardStateWithoutRegisterReshoot", "сверка с машинными карточками разошлась", m_card_state_without_reshoot,
        "у карточки появилось состояние, которого нет ни в прозе, ни в пересъёме реестра")

    # 29. Ссылка карточки уехала в несуществующий файл: карточка осталась, а её носителя
    # нет. Так выглядит «учёт, который ничего не описывает», и ловить это должно гейтом.
    def m_card_dangling_file():
        raw = LANE_REG["ot"].read_text(encoding="utf-8")
        needle = '"file": "ИСКУПЛЕНИЕ/ot/01_LEX_KPR_KIPPER_FAMILY.md"'
        if needle not in raw:
            raise AssertionError("не проверен: карточка 01 не ссылается на ожидаемый файл")
        LANE_REG["ot"].write_text(
            raw.replace(needle, '"file": "ИСКУПЛЕНИЕ/ot/99_UNNAMED_CASE_NO_SUCH_FILE.md"', 1), encoding="utf-8")

    add("cardPointsToMissingProseFile", "на несуществующий файл", m_card_dangling_file,
        "машинная запись указывает в пустоту, а её файл прозы остался без записи")

    # 30. Приукрашенное покрытие: в блоке реестра число файлов без карточки задрано с 0
    # до 1 без изменения прозы и карточек. Число обязано читаться из обхода, а не из текста.
    def m_faked_coverage():
        sys.path.insert(0, str(ROOT / "scripts"))
        blk = json.loads(LANE_REG["synthesis"].read_text(encoding="utf-8")).get(CLAIMS_BLOCK) or {}
        if blk.get("файловБезКарточки") != 0:
            raise AssertionError("не проверен: обход и так находит карточки без прозы")
        # поле живёт в блоке дважды (сводка и сверка), поэтому режем по верхнеуровневому
        # вхождению внутри блока, а не по первому встречному: иначе случай бил бы не в то поле
        import atonement_claim_register as _acr
        raw = LANE_REG["synthesis"].read_text(encoding="utf-8")
        a, b = _acr.block_span(raw, CLAIMS_BLOCK)
        needle = '"файловБезКарточки": 0,'
        i = raw.index(needle, a)
        if raw.index('"сверкаСКарточками"', a) < i:
            raise AssertionError("не проверен: верхнеуровневое поле идёт не первым")
        LANE_REG["synthesis"].write_text(raw[:i] + needle.replace(": 0,", ": 1,") + raw[i + len(needle):],
                                         encoding="utf-8")

    add("coverageClaimFakedUpward", "сводка «файловБезКарточки» записана", m_faked_coverage,
        "покрытие приукрасили числом: сверка обязана читать его с дерева, а не с бумаги")

    return out


def run(probe=False):
    cs = cases()
    backups = {p: p.read_bytes() for p in FILES}
    print("батарея: %d случаев; затронуто файлов: %d" % (len(cs), len(FILES)))
    bad, npass, nfail, notchecked = [], 0, 0, []
    for name, expect, fn, note in cs:
        for p, data in backups.items():
            p.write_bytes(data)
        try:
            fn()
        except AssertionError as e:
            notchecked.append((name, str(e)))
            print("%-34s %s" % (name, e))
            continue
        code, out = gate()
        errs = first_errors(out)
        if expect is None:
            ok = code == 0
            verdict = "PASS(ожидаемое: поле не сверяется)" if code == 0 else "FAIL(а ждали, что не сверяется)"
        elif expect.startswith("!"):
            ok = not any(expect[1:] in e for e in errs)
            verdict = "ловушки нет — задокументировано" if ok else "ловушка нашлась"
        else:
            ok = code != 0 and any(expect in e for e in errs)
            verdict = "FAIL(ожидаемое)" if code != 0 else "PASS(неожиданное)"
        if probe:
            print("%-34s code=%d\n    %s" % (name, code, "\n    ".join(errs)))
        else:
            print("%-34s %s %s" % (name, "ok  " if ok else "МИМО",
                                   verdict + (" · " + expect if expect else " · ожидание = PASS")))
            if not ok:
                bad.append((name, verdict, errs[:1]))
        if ok and expect is not None:
            nfail += 1
        elif ok:
            npass += 1
    for p, data in backups.items():
        p.write_bytes(data)
    restored = all(filecmp.cmp(p, p, shallow=False) for p in FILES) and all(
        p.read_bytes() == backups[p] for p in FILES)
    code, out = gate()
    print("\n"); print("откат побайтовый: %s · контрольный прогон гейта: %s" % (restored, "PASS" if code == 0 else "FAIL"))
    print("поймано случаев: %d, подтверждённых PASS-дыр: %d, непопаданий: %d, не проверено: %d"
          % (nfail, npass, len(bad), len(notchecked)))
    for b in bad:
        print("  МИМО:", b[0], "→", str(b[2])[:220])
    for n in notchecked:
        print("  НЕ ПРОВЕРЕНО:", n[0], "→", n[1][:200])
    print("\n"); print("прогонов-мутаций: %d (группа круга 27), непопаданий %d, контрольный прогон %s"
          % (len(cs) - len(notchecked), len(bad), "PASS" if code == 0 else "FAIL"))
    return 1 if (bad or notchecked or not restored or code != 0) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--probe", action="store_true", help="печатать фактические ошибки гейта по каждому случаю")
    sys.exit(run(probe="--probe" in sys.argv[1:]))
