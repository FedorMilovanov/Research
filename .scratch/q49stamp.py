# -*- coding: utf-8 -*-
"""Пересъём stampedFieldsPerRegistry['корпус'] обходом правила 2b — вызывать последним."""
import json, pathlib, sys, datetime
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
COR = pathlib.Path("/home/user/Research/ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
KEYS = ("at", "measuredAt", "checkedAt", "measuredOn", "measuredAtGit")
def count(node):
    n = 0
    if isinstance(node, dict):
        for k, v in node.items():
            if k in KEYS and isinstance(v, str):
                n += 1
            n += count(v)
    elif isinstance(node, list):
        for v in node:
            n += count(v)
    return n
J = json.loads(COR.read_text(encoding="utf-8"))
live = count(J)
sm = J["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]
old = sm["корпус"]
sm["корпус"] = live
sm["how"] = ("переснято кругом 49 обходом правила (2b): %d поля формы at|measuredAt|checkedAt|measuredOn|"
 "measuredAtGit — было %d до пересъёма; прирост круга 49 дают пять новых блоков находки с отметками времени, "
 "пересъём measuredAt/checkedAt у laneReadmeConsistency, countsLive, rd и у зеркала, запись contentRevisions-лага и "
 "отметки в списке заявок; число снимается самим гейтом, а не подсчётом в тексте, и расхождение — ошибка"
 % (live, old))
sm["measuredAt"] = NOW
sm["checkedAt"] = NOW
if len(sys.argv) > 1 and sys.argv[1] == "write":
    COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("stampedFields['корпус']: было", old, "стало", live, "байт", len(COR.read_bytes()))
