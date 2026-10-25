# -*- coding: utf-8 -*-
"""Круг 48, шаг JSON-c: свойства appProperties прочитаны — записываем их как факт, а не как обещание."""
import json, pathlib

ROOT = pathlib.Path("/home/user/Research")
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IDX = ROOT / "ИСКУПЛЕНИЕ/data/atonement-library-index.json"
NOW = "2026-10-25T17:25:00Z"
LIVE = "1rCtYH83FjiVEhl4rzgdOmP500XzUFR8U"
P36 = "1l535xSDigBFItXcId9uWmhEE5K9kO7ZO"

PROPS37 = {"rights": "mirror_of_git", "registry_role": "registry-mirror",
           "source": "git:docs/research/atonement/35_four_point_authors_mass_registry.md",
           "registry_md5": "f4a7f749a1717271d0a6c69d7f95def1", "registry_bytes": "469418",
           "mirror_of_git_commit": "3825e71", "registry_queue": "97",
           "registry_classes": "A1=37,A2=35,B1=34,B2=6,C=97", "read_state": "registry_linked",
           "registry_rows": "209"}
PROPS36 = {"source": "git:docs/research/atonement/35_four_point_authors_mass_registry.md",
           "mirror_of_git_commit": "pre-3825e71", "registry_md5": "f155ec3b34d8eec4c1980d0ebf5ed84c",
           "rights": "HOLD_superseded", "read_state": "registry_linked", "registry_role": "superseded-r48",
           "registry_bytes": "468549", "registry_queue": "97",
           "registry_classes": "A1=37,A2=35,B1=34,B2=6,C=97", "registry_rows": "209"}

d = json.loads(COR.read_text(encoding="utf-8"))
m = d["fourPointMassRegistry20261023"]
dm = d["driveMirrors"]["massRegistry20261023"]

dm["propsNote20261025r48"] = (
 "свойства живого слепка #37 записаны и прочитаны обратно тем же вызовом update_file (fields=id,name,size,"
 "md5Checksum,appProperties,modifiedTime): десять ключей — registry_bytes, registry_rows, registry_md5, "
 "registry_classes, registry_queue, registry_role, read_state, source, rights, mirror_of_git_commit; значения "
 "перечислены в propsWritten20261025r48. Отдельный факт канала, найтый этим кругом: пара «ключ + значение» в "
 "appProperties ограничена 124 байтами в UTF-8 (кириллица стоит два байта на символ), поэтому первая попытка "
 "записать в #36 длинное пояснение получила отказ Google Drive и не была повторена дословно; вместо прозы в "
 "свойстве пояснение осталось в description объекта, а в свойствах #36 стоит короткая метка pre-3825e71")
dm["propsWritten20261025r48"] = {
 "live37": dict(PROPS37, driveId=LIVE, writtenAt="2026-10-25T17:23:47.270Z",
                readBack=("ответ update_file вернул те же десять пар, size 469418 и md5 "
                          "f4a7f749a1717271d0a6c69d7f95def1 — запись свойств не тронула содержимое")),
 "retired36": dict(PROPS36, driveId=P36, writtenAt="2026-10-25T17:24:11.190Z",
                   readBack=("ответ update_file вернул те же десять пар при неизменных size 468549 и md5 "
                             "f155ec3b34d8eec4c1980d0ebf5ed84c; note: mirror_of_git_commit у вытесненного слепка "
                             "не называет коммита, потому что залитого им дерева в истории нет — оно было рабочим "
                             "и через четыре минуты стало деревом 3825e71 с двумя дополнительными правками")),
 "how": "google_drive.update_file с app_properties как JSON-строкой, затем чтение fields=appProperties из того же ответа",
 "measuredAt": NOW, "checkedAt": NOW}
dm["registryCountsAsOfRound48"] = dm.get("registryCountsAsOfRound48", {}) | {
 "lines": 1447, "fileBytes": 469418, "registryRows": 209, "queueAddresses": 97, "dobytLines": 4,
 "perClass": {"A1": 37, "A2": 35, "B1": 34, "B2": 6, "C": 97}, "shareA1Percent": 18, "shareA1PercentFloor": 17,
 "sectionsH2": 48, "mirrorMd5": "f4a7f749a1717271d0a6c69d7f95def1",
 "how": ("снято обходом файла реестра в рабочем дереве тем же определением, которым мерит правило 23; dobytLines — "
         "механический счётчик строк, содержащих токен «Добыть:»"), "measuredAt": NOW, "checkedAt": NOW}
m["mirrorPropsRound4820261025"] = {
 "что": "свойства appProperties двух объектов папки `05` после круга 48 (живой #37 и вытесненный #36)",
 "ключей": 10, "лимитПарыБайт": 124,
 "отказ": ("первая запись #36 с пояснением в 300+ байт отклонена Drive (403, «Properties and app properties are "
           "limited to 124 bytes in UTF-8»); повторен не дословный вызов, а другой: короткая метка в свойствах, "
           "проза в description"),
 "measuredAt": NOW, "checkedAt": NOW,
 "command": "google_drive.update_file (app_properties как JSON-строка) + чтение fields=appProperties из ответа"}

idx = json.loads(IDX.read_text(encoding="utf-8"))
byid = {r["driveId"]: r for r in idx["records"]}
byid[P36]["drivePropsWritten20261025r48"] = dict(PROPS36, at="2026-10-25T17:24:11.190Z",
    how=("записаны тем же кругом, что его вытеснил, и прочитаны обратно из ответа update_file; длинная проза в "
         "свойства не влезает — лимит пары 124 байта в UTF-8, поэтому в свойствах метка pre-3825e71, а "
         "пояснение стоит в description объекта"))
byid[LIVE]["drivePropsWritten20261025r48"] = dict(PROPS37, at="2026-10-25T17:23:47.270Z",
    how="десять пар записаны и прочитаны обратно тем же ответом update_file; содержимое объекта при этом не изменилось")
IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
COR.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус: %d Б / ключей %d | индекс: %d Б" % (len(COR.read_bytes()), len(d), len(IDX.read_bytes())))
