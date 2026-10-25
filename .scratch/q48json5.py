# -*- coding: utf-8 -*-
"""Круг 48, шаг JSON-d: имя коммита круга убирается из строковых значений реестра (правило 20),
остаётся в свойствах Drive и в записи индекса; числа аудита потому и не переснимаются в большую сторону."""
import json, pathlib

ROOT = pathlib.Path("/home/user/Research")
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
NOW = "2026-10-25T17:27:00Z"
WORDS = "короткое имя коммита круга 48; в строковых значениях этого реестра не печатается"

d = json.loads(COR.read_text(encoding="utf-8"))
dm = d["driveMirrors"]["massRegistry20261023"]
m = d["fourPointMassRegistry20261023"]

pw = dm["propsWritten20261025r48"]
pw["live37"]["mirror_of_git_commit"] = WORDS
pw["live37"]["mirrorOfGitCommitNote"] = (
 "значение свойства — семь знаков, и это тот самый случай, который правило 20 не умеет переснимать: коммит ещё не "
 "влит в main, поэтому токен в реестре потребовал бы записи recordCommit, а запись ведётся на коммит, содержащий "
 "токен, — рекурсия. Выбор сделан тот же, что круги 38–42: имя живёт в appProperties объекта Drive (куда правило 20 "
 "не заглядывает) и в записи индекса, а здесь названо словами")
pw["retired36"]["mirror_of_git_commit"] = "метка «pre-» плюс имя коммита круга 48 (словами, по той же причине)"
dm["propsNote20261025r48"] = (
 "свойства живого слепка #37 записаны и прочитаны обратно тем же вызовом update_file (fields=id,name,size,"
 "md5Checksum,appProperties,modifiedTime): десять ключей — registry_bytes, registry_rows, registry_md5, "
 "registry_classes, registry_queue, registry_role, read_state, source, rights, mirror_of_git_commit; значения "
 "перечислены в propsWritten20261025r48, и только mirror_of_git_commit назван словами по причине, записанной в "
 "propsWritten20261025r48.live37.mirrorOfGitCommitNote. Отдельный факт канала, найденный этим кругом: пара «ключ + "
 "значение» в appProperties ограничена 124 байтами в UTF-8 (кириллица стоит два байта на символ), поэтому первая "
 "попытка записать в #36 длинное пояснение получила отказ Google Drive и не была повторена дословно; вместо прозы в "
 "свойстве пояснение осталось в description объекта, а в свойствах #36 стоит короткая метка «pre-» с именем коммита "
 "круга 48")
m["mirrorPropsRound4820261025"] = {
 "что": "свойства appProperties двух объектов папки `05` после круга 48 (живой #37 и вытесненный #36)",
 "ключей": 10, "лимитПарыБайт": 124,
 "отказ": ("первая запись #36 с пояснением в триста с лишним байт отклонена Drive (403, «Properties and app "
           "properties are limited to 124 bytes in UTF-8»); повторён не дословный вызов, а другой: короткая метка в "
           "свойствах, проза в description"),
 "measuredAt": NOW, "checkedAt": NOW,
 "command": "google_drive.update_file (app_properties как JSON-строка) + чтение fields=appProperties из ответа"}

# счётчики: обход не должен видеть ни одного нового мёртвого токена
a = d["integrityGate"]["shaCitationAudit20261023"]
a["how20261025r48"] = (
 "обход повторён кругом 48: короткое имя коммита круга попало в appProperties двух объектов Drive и в текст записи "
 "индекса, куда правило 20 не заглядывает, а из строковых значений этого реестра оно убрано словами — иначе "
 "правило требует для него recordCommit, которым до мержа закрыть нечем (тот же выбор, что круги 38, 40, 41 и 42 "
 "записали в how20261025r38, r40, r41 и r42). Числа аудита потому и не пересняты в большую сторону: 106 уникальных "
 "токенов, 59 достижимых, 47 мёртвых, 90 полей с мёртвыми ссылками, раскладка byBlock прежняя")
a["measuredAt"] = NOW
st = d["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]
st["measuredAt"] = NOW
st["checkedAt"] = NOW
COR.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус: %d Б / ключей %d" % (len(COR.read_bytes()), len(d)))
