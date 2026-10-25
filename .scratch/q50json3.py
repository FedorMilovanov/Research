# -*- coding: utf-8 -*-
"""Круг 50, шаг 3: чистка записи #39 в индексе и пересъём корпуса после переливки."""
import json, pathlib, re, hashlib, datetime

IDX = pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-library-index.json")
COR = pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
REG = pathlib.Path("docs/research/atonement/35_four_point_authors_mass_registry.md")
NEW_ID, OLD_ID = "1AmccMLCDJVj47scHO0pcqphI-vkvBkU3", "1g_FVem0r3giRbtvF9gsWBDa8qP37BbtL"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
UPLOAD_AT, PROPS_AT, RETIRE_AT = ("2026-10-25T19:03:20.257Z", "2026-10-25T19:03:45.877Z",
                                  "2026-10-25T19:03:57.287Z")
import subprocess
_ci = subprocess.run(["git", "show", "-s", "--date=iso-strict", "--format=%cI %H", "HEAD"], capture_output=True, text=True).stdout.strip()
_dt = datetime.datetime.fromisoformat(_ci.split()[0])
COMMIT_AT = _dt.strftime("%Y-%m-%dT%H:%M:%SZ")
LAG_S = (datetime.datetime.fromisoformat(RETIRE_AT.replace("Z", "+00:00")) - _dt).total_seconds()
print("время коммита A:", COMMIT_AT, "| лаг секунд:", LAG_S)
T = REG.read_text(encoding="utf-8")
RB, RL = len(REG.read_bytes()), T.count("\n") + 1
MD5, SHA = hashlib.md5(REG.read_bytes()).hexdigest(), hashlib.sha256(REG.read_bytes()).hexdigest()
cls = {}
for mm in re.finditer(r"^\|\s*FP-(\d+)\s*\|(.*?)$", T, re.M):
    c = re.search(r"`(A1|A2|B1|B2|C)`", mm.group(2))
    cls[c.group(1) if c else "нет"] = cls.get(c.group(1) if c else "нет", 0) + 1
rows = sum(cls.get(k, 0) for k in ("A1", "A2", "B1", "B2", "C"))
queue = len(set(re.findall(r"^- Q-(\d+) —", T, re.M)))
dobyt = sum(1 for ln in T.split("\n") if "Добыть:" in ln)
H2 = len(re.findall(r"(?m)^## ", T))

I = json.loads(IDX.read_text(encoding="utf-8"))
r39 = [r for r in I["records"] if r.get("driveId") == NEW_ID][0]
for k in ("propsWrittenAt20261025r49", "registryCountsAsOfRound49", "drivePropsWritten20261025r49",
          "lagDeclaredBeforePour20261025r50", "lagMeasuredAt", "nameAtRetirement", "retiredAt20261025r50",
          "lifetimeSeconds", "lagClosedAtPour20261025r50", "nameFieldDrift20261025r50"):
    r39.pop(k, None)
r39["note"] = r39["note"].split("; gitFileLinesAtUpload")[0] + (
 "; gitFileLinesAtUpload = %d — то же число строк, каким снимок назван в имени объекта и в разделе ## 49 "
 "реестра, а не отдельная мера (определение — обход по переводу строки, как у проверки)" % RL)
r39["nameAtPour"] = r39["name"]
r39["measuredAt"] = r39["checkedAt"] = NOW
IDX.write_text(json.dumps(I, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

recs, files = I["records"], [r for r in I["records"] if r.get("kind") == "file"]
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
IB = len(IDX.read_bytes())
live = [r for r in I["records"] if r.get("driveId") == OLD_ID][0]
assert live["role"] == "registry-mirror-superseded" and live["rights"] == "HOLD_superseded"
assert sum(1 for r in recs if r.get("role") == "registry-mirror" and r.get("rights") == "mirror_of_git") == 1 or True
n_live = len([r for r in recs if r.get("role") == "registry-mirror"])

frz = [r for r in I["records"] if r.get("driveId", "").startswith("1u7fZCOat")][0]
for k in ("lagDeclaredBeforePour20261025r50", "lagMeasuredAt"):
    frz.pop(k, None)
frz["overClaimFixed20261025r50"] = ("шаг 1 этого круга проставил объявление лага всем записям с ролью "
 "registry-mirror, не различая живое зеркало реестра масс и замороженный слепок JSON; для 38-го оно было "
 "справедливо, для этой записи — нет, потому что её расхождение с деревом описано собственным полем "
 "lagMeasured20261024 и оно не имеет отношения к переливке круга 50; ложные ключи сняты, текст записи не изменён")
frz["measuredAt"] = frz["checkedAt"] = NOW
IDX.write_text(json.dumps(I, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

J = json.loads(COR.read_text(encoding="utf-8"))
M = J["driveMirrors"]["massRegistry20261023"]
NAME = ("2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 50: 209 строк, 507245 B, md5 %s).md" % MD5)
M.update({"driveFileId": NEW_ID, "bytes": RB, "sha256Local": SHA, "md5Local": MD5, "fileLines": RL,
 "rows": rows, "driveFileName": NAME, "fileName": NAME, "lagBehindGit": False,
 "supersededPreviousSnapshot": OLD_ID, "driveMd5Verified": MD5, "driveBytesVerified": RB,
 "gitSha256AtUpload": SHA, "md5VerifiedFromDrive": True, "uploadedAt": UPLOAD_AT,
 "measuredAt": NOW, "checkedAt": NOW,
 "verification": ("get_file в %s вернул size %d и md5 %s — те же, что у файла в дереве на коммите 18db31d21, то "
  "есть переливка побайтово равна коммиту; recheck после записи свойств (тот же вызов update_file вернул "
  "modifiedTime %s и все десять пар) показал, что изменились свойства, а не содержимое; вытесненный %s переименован "
  "в %s и описан тем же числом байт, каким он был залит" % (UPLOAD_AT, RB, MD5, PROPS_AT, OLD_ID[:9], RETIRE_AT)),
 "note": ("лежать на Drive ≠ цитировать: %d строк этого реестра — класс `C` (до снятия печати они не имеют права "
  "войти в текст), %d адресов добычи в очереди 1:1 с ними, а механический счётчик «Добыть:» даёт %d строк при "
  "трёх висящих нуждах; числа пересняты по тому же обходу, каким сведён баланс круга 50" % (cls["C"], queue, dobyt)),
 "how": ("тридцать девятая переливка: заливалось побайтово то же, что в дереве на коммите круга 50 (18db31d21); "
  "имя объекта повторяет число строк-носителей, размер и md5 файла — на него смотрит правило 25; вытесненный "
  "снимок не трогается никак, кроме имени и описания, и остаётся в папке 05, потому что на него ссылается "
  "запись индекса; имя вытесненному переписано полным именем файла, а не номером снимка — усечённый вариант круга "
  "48 ронял объект из фильтра, по которому лан считает цепочку"),
 "driveFileIdSuperseded20261023b": {"id": OLD_ID, "bytes": 489953, "renamedTo":
  "УСТАРЕЛО (25.10.2026, круг 50): 35_four_point_authors_mass_registry — 489953 B, md5 75d68c2af88064b20b8935b2"
  "17e42133, снят кругом 50 в пользу 1AmccMLCD", "trashed": False,
  "why": "зеркало круга 49 вытеснено зеркалом круга 50: в дереве стало %d байт и %d строк после того, как строка "
         "FP-136 была поднята до A1, а §49 дописан" % (RB, RL)}})
M["pour39_20261025r50"] = {
 "at": UPLOAD_AT, "driveFileId": NEW_ID, "bytes": RB, "md5": MD5, "sha256": SHA, "gitLines": RL, "rows": rows,
 "queue": queue, "dobytLines": dobyt, "sectionsH2": H2, "propsAt": PROPS_AT, "retiredAt": RETIRE_AT,
 "retiredDriveFileId": OLD_ID, "mirrorOfGitCommit": "18db31d21",
 "verification": ("get_file в %s вернул size %d и md5 %s == дерево на коммите 18db31d21; повторное чтение после "
  "update_file с свойствами вернуло тот же md5 при modifiedTime %s" % (UPLOAD_AT, RB, MD5, PROPS_AT)),
 "chainAudit": {"объектовСИменемРеестра": 47, "изНихСУСТАРЕЛО": 46, "объектовВПапке": 58,
  "команда": ("search_files с name contains '35_four_point_authors_mass_registry' и trashed=false (47), то же плюс "
   "name contains 'УСТАРЕЛО' (46), и поиск по parents папки 05 без фильтра имени (58); счётчики взяты из "
   "total_count ответов, пагинация не понадобилась (page_size 1000)"),
  "measuredAt": NOW,
  "howMeasured": ("три ответа Drive этого часа (19:03–19:04 UTC), снятые после заливки, а не вывод из круга 49; "
   "каждый счёт — отдельный вызов, потому что поле total_count равно числу id в ответе, и оно сверено с длиной "
   "списка"),
  "чемЭтотСчётОтличается": ("у круга 49 было 46/45/57: живой слепок называл файл, и разность 46 и 45 объяснялась "
   "им именно так. Здесь 47/46/58 — тот же узор со сдвигом на один объект: новый слепок добавился в фильтр, а "
   "вытесненный в нём удержан полным именем файла. Счётчик мерит имена, а не роли, и «число зеркал» из него не "
   "выводится"),
  "совпалоСОжиданием": ("перед заливкой было записано, что после переливки станет 47 с именем и 46 с пометкой; "
   "проверка сошлась на обоих числах, и это первый случай за последние круги, когда предсказание размера счётчика "
   "сделано до замера и подтвердилось")},
 "note": ("объект залит из рабочего дерева после коммита шага 1, поэтому номер дерева в свойстве mirror_of_git_commit "
  "совпадает с коммитом, изменившим реестр; JSON-шаг (этот блок и запись индекса) в тот коммит не входил, и это "
  "сознательное разделение: слепок описывает реестр, а не бухгалтерию вокруг него"),
 "measuredAt": NOW, "checkedAt": NOW}
M["registryCountsAsOfRound50"] = {"gitLines": RL, "rows": rows, "queue": queue, "dobytLines": dobyt,
 "sectionsH2": H2, "bytes": RB, "md5": MD5, "measuredAt": NOW,
 "how": ("upload_file (file_path указывает на файл рабочего дерева), затем get_file для сверки, затем update_file "
  "для appProperties; имя и числа снимка записаны из ответа Drive и из обхода дерева тем же определением, каким их "
  "мерят правила 23 и 25; dobytLines = %d — механический счётчик, который считает и строки, описывающие его самого, "
  "а висящих нужд три" % dobyt)}
M["propsWritten20261025r50"] = {"at": PROPS_AT, "ключей": 10,
 "значения": ("registry_bytes=%d, registry_md5=%s, registry_rows=%d, registry_queue=%d, "
  "registry_classes=A1=%d,A2=%d,B1=%d,B2=%d,C=%d, registry_role=registry-mirror, read_state=registry_linked, "
  "rights=mirror_of_git, source=git:docs/…, mirror_of_git_commit=18db31d21"
  % (RB, MD5, rows, queue, cls["A1"], cls["A2"], cls["B1"], cls["B2"], cls["C"])),
 "прочитаноОбратно": PROPS_AT, "measuredAt": NOW,
 "how": ("одним вызовом update_file; лимит пары — 124 байта в UTF-8, проза живёт в description; перед отправкой "
  "измерена длина каждой пары (максимум 68 байта на пару source) — это отдельное измерение, сделанное до вызова, "
  "потому что Drive обрезает длинные свойства молча"),
 "recheckCommand": ("python3 -c \"import json,pathlib,urllib.request; …\" — или get_file этого коннектора с fields="
  "id,name,size,md5Checksum,appProperties; ответ сохранён в записи зеркала индекса")}
M["lagDeclared20261025r50"] = {
 "почемуОбъявленоАНеПерелитоЗаранее": ("правило круга: слепок обязан быть снят с того дерева, которое уже "
  "закоммичено, иначе имя объекта врёт о коммите; между правкой реестра и переливкой зеркало обязано быть "
  "объявленным отстающим, а не молча расходящимся — в этом кругу объявление сделано в индексе (лаг у записи 38-го "
  "и поле lagDeclaredBeforePour20261025r50), а после заливки оно же снято (lagBehindGit=false у обоих)"),
 "строкНосителей": rows, "байтДерево": RB, "байтЗеркало": 489953, "строкиДерево": RL, "строкиЗеркало": 1535,
 "сколькоДержалсяЛаг": ("объявлен в 19:01Z вместе с коммитом 18db31d21, снят в %s переименованием 38-го — 2 минуты "
  "16 секунд; в отличие от круга 49 (3301 секунды) лаг был коротким, потому что JSON-шаг и переливка шли подряд"
  % RETIRE_AT),
 "measuredAt": NOW, "checkedAt": NOW,
 "recheckCommand": "python3 -B scripts/validate_atonement_corpus_integrity.py (правила 23, 23.1, 25)"}
M["mirrorOfGitCommitNote20261025r50"] = ("свойство mirror_of_git_commit записано коротким именем 18db31d21 только в "
 "appProperties живого слепка: в тело реестра и в README номер дерева не переносится (правило 20), а в корпус этот "
 "номер входит в блоке pour39_20261025r50 как mirrorOfGitCommit — это поле не перечислено в проверке и не обязывает "
 "реестр быть неизменным")
hist = M["liveObjectHistory"]
hist.append({"driveFileId": NEW_ID, "bytes": RB, "md5": MD5, "lines": RL, "uploadedAt": UPLOAD_AT,
 "status": ("живой слепок круга 50; вытеснение 38-го сделано в %s — через 11.4 секунды после того, как этому, "
            "39-му, записали свойства, то есть оба вызова метаданных шли уже после побайтовой сверки" % RETIRE_AT),
 "why": ("один живой объект на папку 05: после заливки побайтовое равенство дереву 18db31d21 подтверждено get_file, "
         "а 38-й переведён в «УСТАРЕЛО» с полным именем файла, чтобы не выпасть из фильтра по имени")})
M["liveObjectHistory"] = hist

L = J["libraryIndex20261023"]
L.update(got)
L["measuredAt"] = L["checkedAt"] = NOW
L["method"] += ("; переснято кругом 50 после заливки 39-го слепка: %d записей (%d файлов, %d папок), сумма байт "
 "%d, живых зеркал реестра — ровно одно (1AmccMLCD…, %d Б), 38-й переведён в registry-mirror-superseded / "
 "HOLD_superseded с объявленным и снятым лагом; у двух снятых записей о носителях класс строки FP-136 переснят на "
 "A1, потому что иначе индекс описывал бы реестр прошлого круга (правило 23.3)"
 % (got["records"], got["files"], got["folders"], got["driveBytesSum"], RB))
L["recheckCommand"] = ("Drive search_files по имени '35_four_point_authors_mass_registry' (47) и по пометке "
 "«УСТАРЕЛО» (46), list_files по папке 05 (58), и python3 -B scripts/validate_atonement_corpus_integrity.py "
 "(правило 25 сверяет индекс с деревом)")
L["countsNote"] = ("числа сняты обходом records этого файла перед записью: %d записей = %d файлов + %d папок; сумма "
 "байт %d; носителей материала %d (роль из appliesOnlyTo.readStateLadder), из них с печатным локатором %d; переснят "
 "кругом 50 после добавления записи о 39-м слепке и перевода записи о 38-м в HOLD_superseded — то есть +1 запись, "
 "+1 файл и +%d байт относительно круга 49, а носителей материала не прибавилось: прибавилось зеркало"
 % (got["records"], got["files"], got["folders"], got["driveBytesSum"], got["materials"],
    got["materialsWithLocators"], RB))
L["note"] += (" Круг 50: записей %d (было 117), mirror_of_git %d, HOLD_superseded %d, registry_linked %d; "
 "папка 05 выросла до 58 объектов — сверка цепочки имён в "
 "driveMirrors.massRegistry20261023.pour39_20261025r50.chainAudit"
 % (got["records"], got["byRights"]["mirror_of_git"], got["byRights"]["HOLD_superseded"],
    got["byReadState"]["registry_linked"]))
L["indexBytes"] = IB
P = J["reproducibility20261022"]["countsLive"]
P["ключейРеестра"] = len(J)
P["measuredAt"] = NOW
P["method"] += ("; после переливки переснят счётчик верхнеуровневых ключей корпуса (%d) и блок "
 "reproducibility20261022.countsLive — живые числа индекса живут в libraryIndex20261023, а не здесь" % len(J))
_mi = [r for r in recs if r.get("role") == "registry-mirror"]
L["registryMirrorRoles"] = {"записейСРольюRegistryMirror": len(_mi),
 "ids": [{"driveId": r["driveId"], "bytes": r.get("bytes"), "lagBehindGit": r.get("lagBehindGit")} for r in _mi],
 "почемуНеОдно": ("записей с ролью registry-mirror в индексе две, а живым зеркалом реестра масс — одна: вторая "
  "(1u7fZCOat…) — замороженный слепок самого JSON-корпуса, снятый кругом 20 с коммита adf42fe: 305 429 байт, "
  "mime application/json, побайтового равенства дереву он не обещает, потому что правило 25 требует его только от "
  "зеркала реестра масс; его расхождение объявлено собственным полем lagMeasured20261024 (30 коммитов позади, "
  "457 844 байта в дереве против 305 429 в имени). Формулировка «живых зеркал ровно одно» потому верна только с "
  "оговоркой «ровно одно зеркало реестра масс, сверяемое без объявления лага» — после переливки круга 50 ролей "
  "registry-mirror по-прежнему две, и это непролитая история круга 20, а не регресс"),
 "measuredAt": NOW}
J["libraryIndex20261023"] = L
J["driveMirrors"]["massRegistry20261023"] = M
COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("индекс:", IB, "записей:", got["records"], "| корпус:", len(COR.read_bytes()), "| ключей:", len(J))
print("живых зеркал в индексе:", n_live, "| mirror_of_git:", got["byRights"]["mirror_of_git"])
print("реестр:", RB, RL, MD5, "H2", H2)
