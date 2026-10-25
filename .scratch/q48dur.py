# -*- coding: utf-8 -*-
"""Круг 48, починка длительностей: две фразы о времени жизни #36 были написаны по памяти и неверны."""
import json, pathlib, datetime as dt


def must(txt, a, b):
    assert a in txt, "не найдено: " + a[:60]
    return txt.replace(a, b, 1)

ROOT = pathlib.Path("/home/user/Research")
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IDX = ROOT / "ИСКУПЛЕНИЕ/data/atonement-library-index.json"
P36_UP = "2026-10-25T17:13:40.086Z"
P36_OFF = "2026-10-25T17:18:28.535Z"
P37_UP = "2026-10-25T17:18:16.832Z"
T = lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
LIFE = round((T(P36_OFF) - T(P36_UP)).total_seconds(), 3)
GAP = round((T(P36_OFF) - T(P37_UP)).total_seconds(), 3)
print("жизнь #36: %s с | разрыв #37→переименование #36: %s с" % (LIFE, GAP))
assert LIFE == 288.449 and GAP == 11.703

d = json.loads(COR.read_text(encoding="utf-8"))
li = d["libraryIndex20261023"]
li["method"] = must(li["method"],
 "добавлена запись о вытесненном 37-м (468 549 Б, прожил двенадцать минут и пятьдесят две секунды)",
 "добавлена запись о вытесненном 37-м (468 549 Б; прожил 288,449 с — залит в 17:13:40.086Z, переименован в "
 "17:18:28.535Z; вторая фраза этого метода, говорившая про «двенадцать минут», была написана по памяти и снята: "
 "двенадцать с лишним секунд — это не жизнь слепка, а промежуток между заливкой 38-го и переименованием 37-го)")
p36 = d["driveMirrors"]["massRegistry20261023"]["pour36_20261025"]
p36["livedForSeconds"] = LIFE
p36["livedNote"] = ("от заливки (upload_file, 17:13:40.086Z) до переименования, которым круг перевёл объект в "
                    "«УСТАРЕЛО» (update_file, 17:18:28.535Z); отсчёт снят по полям createdTime/modifiedTime самих "
                    "объектов, а не по часам круга; до этого в этом поле стояло 12 — это не длительность жизни, а "
                    "промежуток 38-й заливка → 37-е переименование, и он записан отдельно числом %s с" % GAP)
p36["gapToRetirementAfterNextPourSeconds"] = GAP
COR.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

i = json.loads(IDX.read_text(encoding="utf-8"))
byid = {r["driveId"]: r for r in i["records"]}
r36 = byid["1l535xSDigBFItXcId9uWmhEE5K9kO7ZO"]
r36["note"] = must(r36["note"],
 "сверен get_file (468 549 Б, md5 f155ec3b34d8eec4c1980d0ebf5ed84c == дерево того минуты)",
 "сверен get_file (468 549 Б, md5 f155ec3b34d8eec4c1980d0ebf5ed84c == дерево того часа)")
r36["note"] = must(r36["note"], "вытеснен в 17:18:28.535Z, когда тот же круг нашёл",
             "прожил 288,449 с и вытеснен в 17:18:28.535Z, когда тот же круг нашёл")
r36["lifetimeSeconds"] = LIFE
r37 = byid["1rCtYH83FjiVEhl4rzgdOmP500XzUFR8U"]
r37["chainNote"] = must(r37["chainNote"],
 "вытесненный за минуту до этого 1l535xSDig…",
 "вытесненный через 11,703 с после этой заливки 1l535xSDig… (переименование в 17:18:28.535Z)")
IDX.write_text(json.dumps(i, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус: %d Б | индекс: %d Б" % (len(COR.read_bytes()), len(IDX.read_bytes())))
