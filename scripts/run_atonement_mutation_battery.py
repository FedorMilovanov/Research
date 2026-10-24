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
FILES = [REG_MD, IDX, COR, DOC17]
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
    mir = [r for r in recs if isinstance(r, dict) and "35_four_point_authors_mass_registry" in str(r.get("name", ""))
           and "УСТАРЕЛО" not in str(r.get("name", ""))]
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
        rec = [r for r in raw["records"] if "35_four_point_authors_mass_registry" in str(r.get("name", ""))
               and "УСТАРЕЛО" not in str(r.get("name", ""))]
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
