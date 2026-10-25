# -*- coding: utf-8 -*-
"""Круг 48, шаг JSON-b: четыре починки, которые показал гейт (латинские command в трёх блоках, счётчик дат)."""
import json, pathlib, hashlib

ROOT = pathlib.Path("/home/user/Research")
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IDX = ROOT / "ИСКУПЛЕНИЕ/data/atonement-library-index.json"
NOW = "2026-10-25T17:24:00Z"

d = json.loads(COR.read_text(encoding="utf-8"))
m = d["fourPointMassRegistry20261023"]
dm = d["driveMirrors"]["massRegistry20261023"]

ca = dm["pour37_20261025r48"]["chainAudit"]
ca["command"] = ("google-drive list_files с q \"'13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ' in parents and trashed = false\" и "
                 "двумя вариантами фильтра name contains (по файлу реестра; по файлу реестра и по «УСТАРЕЛО»); счёт "
                 "берётся из поля total_count ответа, пагинация не понадобилась")
ca["howMeasured"] = "перепись ответов Drive этого часа (17:18–17:20 UTC), а не вывод из прошлого круга"
ca["recheckCommand"] = ca["command"]

qc = m["quoteIdentificationCensus20261025r48"]
qc["command"] = ("python-обход `.scratch/q48*.py`: сверка опознанного TCP-id с трудом, названным в строке реестра; "
                 "поиск формул строки по телу TEI с разметкой pb n= (попадания на странице pre не считаются); "
                 "поровну делит на десять адресов, намеченных кругом 47 — масштаб назван полем «шкала»")
qc["recheckCommand"] = qc["command"]

qm = m["queueClosures20261025r48"]
qm["command"] = ("grep -c '^| FP-' по реестру для числа строк; подсчёт уникальных '^- Q-NN —' для очереди; класс "
                 "строки — первый класс-токен строки таблицы (правило 23 переснимает те же два числа)")
qm["recheckCommand"] = qm["command"]

st = d["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]
st["корпус"] = 332
st["measuredAt"] = NOW
st["checkedAt"] = NOW
st["how"] = ("переснято кругом 48 обходом правила (2b): 332 поля формы at|measuredAt|checkedAt|measuredOn|"
             "measuredAtGit — было 319 до этого круга, прирост 13 от четырёх новых блоков находки и от полей "
             "записей о слепках; число снимается самим гейтом, а не подсчётом в тексте, и расхождение — ошибка")

COR.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
IDX_MD5 = hashlib.md5(IDX.read_bytes()).hexdigest()
print("корпус: %d Б / ключей %d | индекс: %d Б md5 %s"
      % (len(COR.read_bytes()), len(d), len(IDX.read_bytes()), IDX_MD5))
