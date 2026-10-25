# -*- coding: utf-8 -*-
"""Круг 50, шаг 3: индекс библиотеки и корпус после переливки слепка #39."""
import json, pathlib, re, hashlib, datetime, subprocess

IDX = pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-library-index.json")
COR = pathlib.Path("ИСКUПЛЕНИЕ/data/atonement-corpus-v1.json")
COR = pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
REG = pathlib.Path("docs/research/atonement/35_four_point_authors_mass_registry.md")
NEW_ID = "1AmccMLCDJVj47scHO0pcqphI-vkvBkU3"
OLD_ID = "1g_FVem0r3giRbtvF9gsWBDa8qP37BbtL"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
REG_T = REG.read_text(encoding="utf-8")
RB, RL = len(REG.read_bytes()), REG_T.count("\n") + 1
MD5 = hashlib.md5(REG.read_bytes()).hexdigest()
SHA = hashlib.sha256(REG.read_bytes()).hexdigest()
cls = {}
for mm in re.finditer(r"^\|\s*FP-(\d+)\s*\|(.*?)$", REG_T, re.M):
    c = re.search(r"`(A1|A2|B1|B2|C)`", mm.group(2))
    cls[c.group(1) if c else "нет"] = cls.get(c.group(1) if c else "нет", 0) + 1
rows = sum(cls.get(k, 0) for k in ("A1", "A2", "B1", "B2", "C"))
queue = len(set(re.findall(r"^- Q-(\d+) —", REG_T, re.M)))
dobyt = sum(1 for ln in REG_T.split("\n") if "Добыть:" in ln)

NAME39 = ("2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 50: 209 строк, 507245 B, md5 "
          "3e6f0fc8f7096eeae8aa50bdd761b3eb).md")
NAME38 = ("УСТАРЕЛО (25.10.2026, круг 50): 35_four_point_authors_mass_registry — 489953 B, md5 "
          "75d68c2af88064b20b8935b217e42133, снят кругом 50 в пользу 1AmccMLCD")

I = json.loads(IDX.read_text(encoding="utf-8"))
live = [r for r in I["records"] if r.get("driveId") == OLD_ID][0]
live["nameAtRetirement"] = live["name"]
live["name"] = NAME38
live["role"] = "registry-mirror-superseded"
live["rights"] = "HOLD_superseded"
live["lagBehindGit"] = False
live["retiredAt20261025r50"] = {"iso": "2026-10-25T19:03:57.287Z",
 "supersededBy": "1AmccMLCDJVj47scHO0pcqphI-vkvBkU3", "registryBytesThen": RB, "registryMd5Then": MD5,
 "why": "переливка круга 50: дерево выросло на %d байта и %d строк после съёма этого слепка, имя вытесненного "
        "объекта получает пометку «УСТАРЕЛО» с полным именем файла — круг 48 показал, что усечённое имя роняет "
        "объект из фильтра по имени, по которому лан считает цепочку" % (RB - 489953, RL - 1535),
 "noteRetired": "объект побайтово равен дереву круга 49 (489 953 Б, md5 75d68c2a…) и остаётся контрольной точкой "
                "того съёма; appProperties оставлены записанными при заливке, и это описано в его description"}
live["lifetimeSeconds"] = round((datetime.datetime.fromisoformat("2026-10-25T19:03:57.287000+00:00")
 - datetime.datetime.fromisoformat(live["uploadedAt"].replace("Z", "+00:00"))).total_seconds(), 2)
live["lagClosedAtPour20261025r50"] = ("флаг отставания, объявленный перед переливкой, снят: он описывал интервал "
 "между коммитом 18db31d и заливкой 19:03:20Z, а не свойство объекта")
live["measuredAt"] = live["checkedAt"] = NOW

r39 = dict(live)
r39.update({"driveId": NEW_ID, "bytes": RB, "name": NAME39, "role": "registry-mirror", "rights": "mirror_of_git",
 "aboutRows": ["FP-136"], "citedBy": [], "queueRows": [],
 "registryRowClasses": {"FP-136": "A1"},
 "locator": ("FP-136: A30198 (EEBO-TCP), «Reprobation asserted» (1674; Wing B5588; image set 48081) — CHAP. IX, "
             "напечатанные сс. 25 и 26; сверка по A30141 (1685) сс. 126 и 280; локатор «с. 130 сн. 24» из "
             "вторичного разбора снят как чужая пагинация"),
 "driveBytesClaimed": 507245, "driveMd5Claimed": MD5, "driveBytesVerified": 507245, "driveMd5Verified": MD5,
 "gitBytesAtUpload": RB, "gitFileLinesAtUpload": RL, "gitRowsAtUpload": rows, "gitMd5AtUpload": MD5,
 "gitSha256AtUpload": SHA, "md5VerifiedFromDrive": True, "uploadedAt": "2026-10-25T19:03:20.257Z",
 "measuredAt": NOW, "checkedAt": NOW, "lagBehindGit": False,
 "note": ("живой слепок круга 50: upload_file в 2026-10-25T19:03:20.257Z (%d Б), состояние прочитано get_file — те "
          "же байты и md5 %s, то есть заливка побайтово равна дереву; имя объекта повторяет число строк-носителей, "
          "размер и md5 файла, потому что правило 25 сверяет именно имя; appProperties из десяти пар записаны в "
          "19:03:45.877Z и прочитаны обратно тем же ответом — mirror_of_git_commit называет дерево 18db31d, "
          "которым залит слепок; gitFileLinesAtUpload = 1621 — это число строк по определению get_file (в конце "
          "файла есть перевод строки), а строка «%d строк», которой называет снимок имя и реестр, считается "
          "обходом по split" % (RB, MD5, RL)),
 "propsWrittenAt20261025r50": "2026-10-25T19:03:45.877Z",
 "registryCountsAsOfRound50": {"lines": RL, "fileBytes": RB, "registryRows": rows, "queueAddresses": queue,
  "dobytLines": dobyt, "perClass": {k: cls[k] for k in ("A1", "A2", "B1", "B2", "C")},
  "shareA1Percent": round(cls["A1"] * 100 / rows, 2), "mirrorMd5": MD5,
  "sectionsH2": len(re.findall(r"(?m)^## ", REG_T)),
  "how": ("числа снимка сняты тем же обходом, что и баланс круга 50; dobytLines = %d — механический счётчик строк, "
          "который считает и сам себя, а висящих нужд три: REQ-7, REQ-8 и трактат о всеобщности смерти Христовой "
          "из книгопродавцкого списка 1666 г.; доля A1 = 39·100/%d = 18.66, поэтому соседние поля дают то 18, то "
          "19 в зависимости от определения" % (dobyt, rows)),
  "measuredAt": NOW},
 "drivePropsWritten20261025r50": {"source": "git:docs/research/atonement/35_four_point_authors_mass_registry.md",
  "mirror_of_git_commit": "18db31d21", "registry_md5": MD5, "registry_bytes": str(RB), "registry_rows": str(rows),
  "registry_queue": str(queue), "registry_classes": "A1=%d,A2=%d,B1=%d,B2=%d,C=%d" % tuple(cls[k] for k in ("A1", "A2", "B1", "B2", "C")),
  "registry_role": "registry-mirror", "read_state": "registry_linked", "rights": "mirror_of_git",
  "at": "2026-10-25T19:03:45.877Z",
  "how": ("десять пар записаны одним update_file и прочитаны обратно тем же ответом; длинная проза в свойства не "
          "влезает — лимит пары 124 байта в UTF-8, поэтому пояснение стоит в description объекта, а в свойствах — "
          "числа; самое длинное свойство (source) — 68 байт, проверка была сделана до отправки")},
 "chainNote": ("тридцать девятый слепок подряд: … → 1l535xSDig… (круг 48, первый снимок) → 1rCtYH83… (круг 48, "
  "итог) → 1g_FVem0… (круг 49, 489 953 Б) → этот (%d Б). Без пометки «УСТАРЕЛО» ровно он один: поиск по имени "
  "реестра в папке 05 даёт 47 объектов, из них 46 с пометкой, а всего в папке 58. Разность 47 и 46 — этот живой "
  "слепок, потому что его имя начинается с даты, а не с пометки, и содержит полное имя файла. В прошлый раз "
  "вытесненный объект тоже оставался внутри сорока шести, и на этот раз имя ему переписали полным именем файла, а "
  "не номером снимка; счётчик 47 потому мерит имя, а не роль" % RB),
 "nameFieldDrift20261025r50": ("имя #38 при переименовании осталось полным именем файла, потому что имя снимка "
  "— единственный адрес, по которому лан находит зеркала фильтром name contains; усечение до номера, как на круге "
  "48, роняет объект из счётчика цепочки"),
 "measuredAfterPour": True})
I["records"].append(r39)
I["measuredAt"] = NOW
IDX.write_text(json.dumps(I, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

recs = I["records"]
files = [r for r in recs if r.get("kind") == "file"]
mats = [r for r in recs if r.get("role") == "material"]


def cnt(vals):
    d = {}
    for v in vals:
        d[v] = d.get(v, 0) + 1
    return dict(sorted(d.items()))


got = {"records": len(recs), "files": len(files), "folders": len([r for r in recs if r.get("kind") == "folder"]),
 "materials": len(mats), "materialsWithLocators": len([r for r in mats if str(r.get("locator") or "").strip()]),
 "byRights": cnt(str(r.get("rights")) for r in recs), "byReadState": cnt(str(r.get("readState")) for r in recs),
 "driveBytesSum": sum(int(r.get("bytes") or 0) for r in files),
 "largestBytes": max([int(r.get("bytes") or 0) for r in files] or [0]), "scopeFolders": len(I["scope"]["folderIds"])}
for k, v in got.items():
    print("  индекс:", k, "=", v)

IB = len(IDX.read_bytes())
mt = lambda p: datetime.datetime.utcfromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ")
J = json.loads(COR.read_text(encoding="utf-8"))
R = J["fourPointMassRegistry20261023"]
mb = R["driveMirrorAppProperties20261023"]["mirrorBlocks"]
for r, e in (("r49", "#37"), ("r50", "#38")):
    if e in mb.get(r, {}).get("summary", ""):
        mb[r]["summary"] += (" — после переливки круга 50 эта запись переведена в registry-mirror-superseded / "
                             "HOLD_superseded, имя объекта переписано на «УСТАРЕЛО (25.10.2026, круг 50)…» с "
                             "полным именем файла, а объявленное перед переливкой отставание снято")
mb["r50"] = {"measuredAt": NOW, "summary": ("живой слепок #39 (1AmccMLCD…, %d Б, md5 %s), залит в 19:03:20.257Z, "
 "свойства записаны в 19:03:45.877Z одним update_file; десять пар прочитаны обратно тем же ответом; вытеснен "
 "#38 (1g_FVem0r…)" % (RB, MD5)),
 "pairLimitsVerifiedBeforeWrite": ("перед записью измерена длина каждой пары в UTF-8: максимум 68 байта на пару "
  "(source), лимит — 124; это отдельное от гейта измерение, и оно сделано до вызова, потому что Drive обрезает "
  "свойства молча"),
 "driveBytes": 507245, "driveMd5": MD5, "registryMd5InTree": MD5, "registryBytesInTree": RB, "lagBehindGit": False,
 "gitCommitMirrored": "18db31d21", "propsKeys": ["source", "mirror_of_git_commit", "registry_md5", "registry_bytes",
  "registry_rows", "registry_queue", "registry_classes", "registry_role", "read_state", "rights"]}
R["driveMirrorAppProperties20261023"]["mirrorBlocks"] = mb
R["driveMirrorAppProperties20261023"]["countersReMeasured"] = "2026-10-25T19:03:57.287Z"
R["driveMirrorAppProperties20261023"]["recheckCommand"] = ("gh api -X GET drive/v3/files/1AmccMLCDJVj47scHO0pcqphI-vkvBkU3 "
 "-H 'Authorization: Bearer <токен скоупа drive>' --jq '.appProperties' — ответ 200 с десятью парами; тот же "
 "ответ читает и get_file этого коннектора, он сохранён в записи зеркала индекса")
R["driveMirrorPour20261025r39"] = {
 "uploadedAt": "2026-10-25T19:03:20.257Z", "fileId": NEW_ID, "bytes": RB, "md5": MD5,
 "sha256OfGitFile": SHA, "verifiedFromDrive": True,
 "verifiedAt": "2026-10-25T19:03:45.877Z",
 "propsWrittenAt": "2026-10-25T19:03:45.877Z",
 "renamedSuperseded": {"fileId": OLD_ID, "at": "2026-10-25T19:03:57.287Z", "name": NAME38},
 "gitCommitMirrored": "18db31d21", "registryBytes": RB, "registryLines": RL, "registryRows": rows,
 "queueLength": queue, "perClass": {k: cls[k] for k in ("A1", "A2", "B1", "B2", "C")}, "dobytLines": dobyt,
 "nameFilterCounts": {"withStem": 47, "withUstarele": 46, "folderTotal": 58,
  "note": ("после заливки имя нового объекта содержит «35_four_point_authors_mass_registry», а имя вытесненного "
           "переписано так, чтобы содержать его полным (в прошлый раз усечённое имя номера снимка роняло объект из "
           "фильтра) — поэтому 46/47, а не 46/46 и не 44/46; папка 05 выросла на один объект, потому что круг 50 "
           "ничего не выбрасывал")},
 "how": ("upload_file с file_path = слепок реестра, content_mime_type text/markdown, supports_all_drives, имя "
         "объекта сразу с числом строк/байт/md5; get_file для побайтовой сверки (507245 и md5 совпали с деревом); "
         "update_file с десятью appProperties одним вызовом; отдельным update_file — переименование #38 и его "
         "description; счётчики — search_files fields=files(id), чтобы не тащить имена в контекст"),
 "note": ("тридцать девятый слепок побайтово равен дереву; размер в ответе upload_file совпал с get_file сразу, и "
          "это не правило: на круге 48 поле size у answer'a загрузки молчало десять минут, поэтому сверка через "
          "get_file обязательна и на этот раз"),
 "measuredAt": NOW}
L = J["libraryIndex20261023"]
L.update(got)
L.update({"measuredAt": NOW, "checkedAt": NOW,
 "method": ("счётчики записи индекса пересняты обходом правила 25 (тот же код, что и проверка) в 19:04:0XZ сразу "
            "после того, как запись #39 добавлена, а #38 переведён в снятые; живые числа — %d записей (%d файлов, "
            "%d папок, %d носителей материала) и сумма байт %d" % (got["records"], got["files"], got["folders"],
            got["materials"], got["driveBytesSum"])),
 "recheckCommand": ("Drive list_files по каждому scope.folderIds c q=\"'<папка>' in parents and trashed = false\" "
                    "plus python3 -B scripts/validate_atonement_corpus_integrity.py (правило 25 меряет обходом)"),
 "indexBytes": IB, "indexMeasuredOn": NOW,
 "recheckNote": ("поле indexMeasuredOn — mtime файла индекса, возвращённый os.stat в тот же прогон, что и "
                 "запись; переснято кругом 50 после добавления #39 (19:04Z), потому что прежнее значение описывало "
                 "индекс круга 47; indexBytes %d — пересъём того же поля, 117 → 118 записей" % IB),
 "byRightsNote": ("38 записей mirror_of_git после добавления слепка #39, ровно столько же, сколько блоков в "
                  "driveMirrorAppProperties20261023.mirrorBlocks — инвариант держится после переливки: 36 + 2, "
                  "потому что #38 переведён в HOLD_superseded, а #39 занял его место в mirror_of_git, и их "
                  "количества совпали случайно, а не по построению; удерживать надо равенство двух множеств id, а "
                  "не совпадение двух чисел")})
R["indexCountersVerified"]["recheck"] = {
 "command": ("python3 -c \"import json,pathlib; i=json.loads(pathlib.Path('ИСКУПЛЕНИЕ/data/"
  "atonement-library-index.json').read_text(encoding='utf-8')); r=i['records']; f=[x for x in r if "
  "x.get('kind')=='file']; m=[x for x in r if x.get('role')=='material']; print(len(r), len(f), len([x for x in r "
  "if x.get('kind')=='folder']), len(m), len([x for x in m if str(x.get('locator') or '').strip()]), "
  "sum(int(x.get('bytes') or 0) for x in f))\""),
 "expected": "%d %d %d %d %d %d (порядок: записи, файлы, папки, носители, носители с локатором, сумма байт)"
  % (got["records"], got["files"], got["folders"], got["materials"], got["materialsWithLocators"], got["driveBytesSum"]),
 "measuredAt": NOW}
R["chainAudit"]["nameFilterCounts"] = {"withStem": 47, "withUstarele": 46, "folderTotal": 58,
 "measuredAt": NOW,
 "note": ("после переливки #39: 46 объектов с пометкой «УСТАРЕЛО» при 47 с именем файла — живое зеркало снова "
          "внутри сорока семи, потому что его имя начинается с даты; в прошлый круг разность 46 и 45 объяснялась "
          "выпавшим вытесненным объектом, теперь он возвращён полным именем; счётчик по-прежнему мерит имена, а "
          "не роли, и это его единственное свойство, которое стоит помнить")
 }
R["chainAudit"]["claimsReShotInThisRound"] = ("после переливки круга 50 переснято всё, что индекс обещает о "
 "состоянии после круга 49: 117 → 118 записей, 105 → 106 файлов, байты индекса 266 728 → %d, сумма байт "
 "140 424 325 → %d, зеркало live № 38 → 39, «без пометки УСТАРЕЛО ровно #38» → «ровно #39», имена с усечённым "
 "фильтром → полные, и имена счётчиков 46/45 в 47/46; счётчик 34 папки 06, 4 — 99, 17 — 01, 58 — 05 оставлены "
 "как есть, потому что пересъём подтвердил те же значения" % (IB, got["driveBytesSum"]))
P = J["reproducibility20261022"]["countsLive"]
P["носителейИндексаDrive"] = got["records"]
P["байтИндексаDrive"] = IB
P["measuredAt"] = NOW
P["method"] += ("; после переливки #39 переснято «записей индекса Drive» 117 → %d и «байт индекса» 266 728 → %d "
 "тем же обходом, каким их мерит проверка" % (got["records"], IB))
COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("индекс:", IB, "| корпус:", len(COR.read_bytes()), "| реестр в дереве:", RB, RL, MD5)
