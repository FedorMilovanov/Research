# -*- coding: utf-8 -*-
"""Круг 49, шаг 1b: countsLive без checkedAt, how в reshotByRound49, lag на записи живого зеркала в индексе."""
import json, pathlib, datetime, hashlib, re

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
COR = pathlib.Path("/home/user/Research/ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
IDX = pathlib.Path("/home/user/Research/ИСКУПЛЕНИЕ/data/atonement-library-index.json")
REG = pathlib.Path("/home/user/Research/docs/research/atonement/35_four_point_authors_mass_registry.md")

J = json.loads(COR.read_text(encoding="utf-8"))
reg = REG.read_text(encoding="utf-8")
cl = J["reproducibility20261022"]["countsLive"]
cl.pop("checkedAt", None)
rd = J["reconciliationDocument20261022"]["reshotByRound49"]
rd["how"] = rd.pop("как", rd.get("how"))
rd["command"] = "python3 -B scripts/validate_atonement_corpus_integrity.py (правило сверки 17_ — блок reconciliationDocument20261022)"
COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус: байт", len(COR.read_bytes()), "ключи countsLive", sorted(cl))

regb = REG.read_bytes()
I = json.loads(IDX.read_text(encoding="utf-8"))
n = 0
for r in I["records"]:
    if r.get("role") == "registry-mirror" and r.get("driveId") == "1rCtYH83FjiVEhl4rzgdOmP500XzUFR8U":
        r["lagBehindGit"] = ("слепок #37 = дерево круга 48 (469418 B, md5 f4a7f749a1717271d0a6c69d7f95def1, 1447 "
 "строк, 209 строк-носителей); в дереве после круга 49 — 488865 B, md5 941b134f3831c613252863410758d262, 1528 строк "
 "при тех же 209 строках-носителях; имена и числа снимка не правятся (это история съёма), расхождение объявлено "
 "здесь, а переливка 38-го слепка — долг этого же круга")
        r["lagMeasured20261025r49"] = {"treeBytes": len(regb),
            "treeMd5": hashlib.md5(regb).hexdigest(),
            "treeLines": len(reg.rstrip("\n").split("\n")),
            "treeRowsCarriers": len([x for x in reg.split("\n")
                                     if re.match(r"^\| FP-\d+ \|", x)]),
            "mirrorBytesInName": 469418, "mirrorMd5InName": "f4a7f749a1717271d0a6c69d7f95def1",
            "measuredAt": NOW,
            "how": "wc -c и md5sum на файле реестра в рабочем дереве; имя зеркала не тронуто — оно описывает "
            "состояние круга 48, и менять его значит подделать историю",
            "recheckCommand": "python3 -B scripts/validate_atonement_corpus_integrity.py (правило 25)"}
        r["checkedAt"] = NOW
        n += 1
assert n == 1, n
I["measuredAt"] = NOW
IDX.write_text(json.dumps(I, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("индекс: байт", len(IDX.read_bytes()), "записей", len(I["records"]), "lag проставлен на", n)
