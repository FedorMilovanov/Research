# -*- coding: utf-8 -*-
"""Круг 49, шаг 3 (после переливки #38): зеркало в корпусе, запись в индексе, счётчики индекса."""
import json, pathlib, hashlib, re, datetime

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
ROOT = pathlib.Path("/home/user/Research")
REG = ROOT / "docs/research/atonement/35_four_point_authors_mass_registry.md"
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IDX = ROOT / "ИСКУПЛЕНИЕ/data/atonement-library-index.json"

txt = REG.read_text(encoding="utf-8")
raw = REG.read_bytes()
B, L = len(raw), len(txt.rstrip("\n").split("\n"))
MD5, SHA = hashlib.md5(raw).hexdigest(), hashlib.sha256(raw).hexdigest()
ROWS = len([x for x in txt.split("\n") if re.match(r"^\| FP-\d+ \|", x)])
CLS = {}
for ln in [x for x in txt.split("\n") if re.match(r"^\| FP-\d+ \|", x)]:
    head = re.match(r"^\| FP-\d+ \|[^|]*\|[^|]*\|[^|]*\|[^|]*\|", ln).group(0)
    k = re.findall(r"`(A1|A2|B1|B2|C)`", head)[0]
    CLS[k] = CLS.get(k, 0) + 1
QUEUE = len(set(re.findall(r"^- Q-(\d+) —", txt, re.M)))
DOBYT = len([x for x in txt.split("\n") if "Добыть:" in x])
H2 = len(re.findall(r"(?m)^## ", txt))
assert (B, L, ROWS, QUEUE, DOBYT, CLS["A1"], CLS["C"]) == (489953, 1535, 209, 96, 4, 38, 96), (B, L, ROWS, QUEUE, DOBYT, CLS)

NAME38 = ("2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 49: 209 строк, %d B, md5 %s).md" % (B, MD5))
ID38 = "1g_FVem0r3giRbtvF9gsWBDa8qP37BbtL"
ID37 = "1rCtYH83FjiVEhl4rzgdOmP500XzUFR8U"
UP38, PROP38, RET37 = "2026-10-25T18:09:05.444Z", "2026-10-25T18:09:35.440Z", "2026-10-25T18:09:41.499Z"
NAME37NEW = "УСТАРЕЛО (25.10.2026, круг 49): 35_four_point_authors_mass_registry — заменён слепком " + ID38

# ---------------- индекс библиотеки ----------------
I = json.loads(IDX.read_text(encoding="utf-8"))
recs = I["records"]
have38 = any(r.get("driveId") == ID38 for r in I["records"])
if have38:
    print('запись #38 уже в индексе — секция индекса пропущена (идемпотентный повтор)')
else:
    i37 = [n for n, r in enumerate(recs) if r.get("driveId") == ID37 and r.get("role") == "registry-mirror"]
    assert len(i37) == 1
    old37 = recs[i37[0]]
    t_up = datetime.datetime.strptime("2026-10-25T17:18:16.832Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    t_re = datetime.datetime.strptime(RET37, "%Y-%m-%dT%H:%M:%S.%fZ")
    LIFE = round((t_re - t_up).total_seconds(), 3)
    old37.update({
     "name": NAME37NEW,
     "nameAtPour": "2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 48: 209 строк, 469 418 B, md5 "
     "f4a7f749a1717271d0a6c69d7f95def1).md",
     "role": "registry-mirror-superseded",
     "rights": "HOLD_superseded",
     "retiredAt20261025r49": RET37,
     "supersededBy20261025r49": ID38,
     "lagBehindGit": True,
     "lifetimeSeconds": LIFE,
     "nameFieldDrift20261025r49": ("в имени объекта Drive число байт стояло с разрядным пробелом («469 418 B»), а поле "
      "name этой записи индекса хранило его без пробела («469418 B»); правило 25 мерит регэкспом, который терпит оба "
      "написания, поэтому расхождение не кричало. Починено так: name = текущее имя, nameAtPour = снятое с ответа Drive "
      "имя на момент заливки, и то и другое — дословные копии ответа, а не пересказ"),
     "note": (old37.get("note", "") + " Круг 49 вытеснил этот слепок через %s с после заливки: реестр был правится после "
      "зеркала (469418 → 489953 Б при тех же 209 строках-носителях), и переливка — единственный честный исход, потому "
      "что имя снимка обещает байты и md5 дерева, а не его собственные." % LIFE),
     "measuredAt": NOW, "checkedAt": NOW,
    })
    old37.pop("lagMeasured20261025r49", None)
    old37["lagDeclaredBeforePour20261025r49"] = {
     "зачем": "между правкой реестра и переливкой зеркало обязано быть объявленным отстающим, а не молча расходящимся — "
     "флаг lagBehindGit стоял на этой записи с числами дерева, и по нему правило 25 не блокировало первый коммит круга",
     "treeBytesAtLagDeclaration": B, "treeMd5AtLagDeclaration": MD5,
     "measuredAt": "2026-10-25T18:07:20Z",
     "how": "wc -c и md5sum на файле реестра; закрывается переливкой #38 в этом же круге"}

    rec = dict(old37)
    for k in ("nameFieldDrift20261025r49", "retiredAt20261025r49", "supersededBy20261025r49", "lifetimeSeconds",
              "lagDeclaredBeforePour20261025r49", "nameAtPour", "registryCountsAsOfRound48FirstPour",
              "registryCountsAsOfRound48", "drivePropsWritten20261025r48", "chainNote"):
        rec.pop(k, None)
    rec.update({
     "name": NAME38,
     "bytes": B,
     "role": "registry-mirror",
     "rights": "mirror_of_git",
     "readState": "registry_linked",
     "aboutRows": ["FP-024"],
     "citedBy": [], "queueRows": [],
     "registryRowClasses": {"FP-024": "A1"},
     "locator": ("FP-024: A68942 (EEBO-TCP), «The seconde tome … of the Paraphrase of Erasmus», London: Whitchurche, "
      "1549 — 1 Тим 2, напечатанные страницы vi, vij и viiij отдела парафразы (счётчик набран римской цифрой на recto и "
      "перезапускается по отделам, поэтому назван отдел)"),
     "driveId": ID38,
     "driveBytesClaimed": B, "driveMd5Claimed": MD5,
     "driveBytesVerified": B, "driveMd5Verified": MD5,
     "gitBytesAtUpload": B, "gitFileLinesAtUpload": L, "gitRowsAtUpload": ROWS,
     "gitMd5AtUpload": MD5, "gitSha256AtUpload": SHA,
     "md5VerifiedFromDrive": True,
     "uploadedAt": UP38, "propsWrittenAt20261025r49": PROP38,
     "lagBehindGit": False,
     "measuredAt": NOW, "checkedAt": NOW,
     "registryCountsAsOfRound49": {"lines": L, "fileBytes": B, "registryRows": ROWS, "queueAddresses": QUEUE,
      "dobytLines": DOBYT, "perClass": dict(sorted(CLS.items())),
      "shareA1Percent": round(CLS["A1"] * 100 / ROWS, 2), "mirrorMd5": MD5, "sectionsH2": H2,
      "how": "числа этого снимка сняты тем же обходом, что и баланс круга 49; dobytLines = %d — механический счётчик "
      "строк, который считает и сам себя (строки, описывающие счётчик), а висящих нужд две: REQ-7 и REQ-8" % DOBYT,
      "measuredAt": NOW},
     "drivePropsWritten20261025r49": {"source": "git:docs/research/atonement/35_four_point_authors_mass_registry.md",
      "mirror_of_git_commit": "0370ece", "registry_md5": MD5, "registry_bytes": str(B), "registry_rows": str(ROWS),
      "registry_queue": str(QUEUE), "registry_classes": "A1=38,A2=35,B1=34,B2=6,C=96",
      "registry_role": "registry-mirror", "read_state": "registry_linked", "rights": "mirror_of_git",
      "at": PROP38,
      "how": "десять пар записаны одним update_file и прочитаны обратно тем же ответом; длинная проза в свойства не "
      "влезает — лимит пары 124 байта в UTF-8, поэтому пояснение стоит в description объекта, а в свойствах — числа"},
     "chainNote": ("тридцать восьмой слепок подряд: … → 1cL8icKDA… (круг 47, первые 16 минут) → 1jfEydgDot… (круг 47, "
      "после починки) → 1l535xSDig… (круг 48, первый снимок) → 1rCtYH83… (круг 48, итог, 469418 Б) → этот (%d Б). "
      "Без пометки «УСТАРЕЛО» ровно он один: поиск по имени реестра в папке 05 даёт 46 объектов, из них 45 с пометкой, "
      "а всего в папке 57. Разность 46 и 45 — этот живой слепок; вытесненный им 1rCtYH83… остался внутри сорока шести, "
      "потому что новое имя по-прежнему называет файл реестра, — в отличие от 1l535xSDig… круга 48, который при "
      "переименовании стал называть номер слепка и из фильтра выпал. Счётчик 46 потому нельзя читать как «все зеркала»: "
      "он мерит имя, а не роль" % B),
     "note": ("живой слепок круга 49: upload_file в %s (%d Б), состояние прочитано get_file — те же байты и md5 %s, то "
      "есть заливка побайтово равна дереву; имя объекта повторяет число строк-носителей, размер и md5 файла, потому что "
      "правило 25 сверяет именно имя; appProperties из десяти пар записаны в %s и прочитаны обратно тем же ответом — "
      "свойство mirror_of_git_commit называет дерево 0370ece, которым залит слепок" % (UP38, B, MD5, PROP38)),
    })
    recs = [r for r in recs if r.get("driveId") != ID38] + []
    I["records"] = recs
    recs.append(rec)
    I["records"] = recs
    recs = I["records"]
    I["measuredAt"] = NOW
    IDX.write_text(json.dumps(I, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

# --- пересъём счётчиков индекса тем же определением, что у правила 25 ---
def cnt(seq):
    out = {}
    for x in seq:
        out[x] = out.get(x, 0) + 1
    return dict(sorted(out.items()))
recs2 = I["records"]
files = [r for r in recs2 if r.get("kind") == "file"]
mats = [r for r in recs2 if r.get("role") == "material"]  # ровно определение правила 25
newcount = {"records": len(recs2), "files": len(files), "folders": len([r for r in recs2 if r.get("kind") == "folder"]),
 "byRights": cnt(r.get("rights") for r in recs2), "byReadState": cnt(r.get("readState") for r in recs2),
 "driveBytesSum": sum(int(r["bytes"]) for r in files), "largestBytes": max(int(r["bytes"]) for r in files),
 "materials": len(mats), "scopeFolders": len((I.get("scope") or {}).get("indexedFolders") or [])}
print("новое состояние индекса:", {k: v for k, v in newcount.items() if k not in ("byRights", "byReadState")})

# ---------------- корпус ----------------
J = json.loads(COR.read_text(encoding="utf-8"))
LI = J["libraryIndex20261023"]
print("было:", {k: LI[k] for k in ("records", "files", "folders", "driveBytesSum", "largestBytes")})
liq = J["integrityGate"].get("libraryIndexQueueCounts20261023")
dm = J["driveMirrors"]["massRegistry20261023"]
POUR38 = {"at": UP38, "driveFileId": ID38, "bytes": B, "md5": MD5, "sha256": SHA,
 "gitLines": L, "rows": ROWS, "queue": QUEUE, "dobytLines": DOBYT, "sectionsH2": H2,
 "propsAt": PROP38, "retiredAt": RET37, "retiredDriveFileId": ID37, "mirrorOfGitCommit": "0370ece",
 "verification": ("get_file в %s вернул size %d и md5 %s == дерево; recheck после записи свойств: тот же md5, "
  "modifiedTime %s (изменились свойства, не содержимое)" % (UP38, B, MD5, PROP38)),
 "chainAudit": {"объектовСИменемРеестра": 46, "изНихСУСТАРЕЛО": 45, "объектовВПапке": 57,
  "команда": "search_files с name contains '35_four_point_authors_mass_registry' по папке 05 (46), то же плюс "
  "name contains 'УСТАРЕЛО' (45), и list_files по папке без фильтра имени (57); счёт взят из total_count ответа, "
  "пагинация не понадобилась (page_size 100)",
  "measuredAt": NOW,
  "howMeasured": "три ответа Drive этого часа (18:09–18:11 UTC), а не вывод из круга 48",
  "чемЭтотСчётОтличается": "у круга 48 было 45/44/56: живой слепок называл файл, и разница в единицу объяснялась "
  "одним объектом (1l535xSDig…, выпавшим при переименовании). Здесь вытесненный 1rCtYH83… остался в фильтре, потому "
  "что я сохранила в его новом имени имя файла, — 46 на одно больше «числа зеркал» и ровно на одно больше счётчика "
  "помеченных; читать его как «все зеркала» нельзя: он мерит имя, а не роль",
  "recheckCommand": "google-drive list_files с q \"'13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ' in parents and trashed = "
  "false\" и двумя вариантами фильтра name contains"},
 "measuredAt": NOW,
 "how": "upload_file (file_path указывает на файл рабочего дерева), затем get_file для сверки, затем update_file для "
 "appProperties; имя и числа снимка записаны из ответа Drive, а не из памяти о правке"}

dm.update({
 "driveFileId": ID38, "driveFileName": NAME38, "fileName": NAME38,
 "bytes": B, "md5Local": MD5, "sha256Local": SHA, "uploadedAt": UP38,
 "fileLines": L, "rows": ROWS, "lagBehindGit": False,
 "driveMd5Verified": MD5, "driveBytesVerified": B, "gitSha256AtUpload": SHA, "md5VerifiedFromDrive": True,
 "supersededPreviousSnapshot": ID37,
 "verification": ("get_file сразу после заливки вернул size %d и md5 %s — те же, что у файла в дереве, то есть "
  "переливка побайтово равна коммиту 0370ece; вытесненный %s переименован в %s и переведён в HOLD_superseded одним "
  "вызовом update_file в %s, его байты и md5 остались своими (469418 Б, f4a7f749…)"
  % (B, MD5, ID37, NAME37NEW, RET37)),
 "measuredAt": NOW, "checkedAt": NOW,
 "how": ("тридцать девятая переливка: заливалось побайтово то же, что в дереве на коммите круга; имя объекта "
  "повторяет число строк-носителей, размер и md5 файла — на него смотрит правило 25; вытесненный снимок не трогается "
  "никак, кроме имени и описания, и остаётся в папке 05 (не в 99), потому что на него ссылается реестр"),
 "note": ("лежать на Drive ≠ цитировать: %d строк этого реестра — класс `C` (до снятия печати они не имеют права "
  "войти в текст), %d адресов добычи в очереди 1:1 с ними; числа пересняты по тому же обходу, каким сведён баланс "
  "круга 49" % (CLS["C"], QUEUE)),
 "pour38_20261025r49": POUR38,
 "mirrorOfGitCommitNote20261025r49": ("свойство mirror_of_git_commit записано коротким именем 0370ece только в "
  "appProperties живого слепка: в тело реестра и корпуса оно не переносится, потому что правило 20 читает семи- и "
  "восьмизначный шестнадцатеричный токен как ссылку на объект и требует его достижимости из origin/main"),
 "propsWritten20261025r49": {"at": PROP38, "ключей": 10,
  "значения": "registry_bytes=489953, registry_md5=%s, registry_rows=209, registry_queue=96, "
  "registry_classes=A1=38,A2=35,B1=34,B2=6,C=96, registry_role=registry-mirror, read_state=registry_linked, "
  "rights=mirror_of_git, source=git:docs/…, mirror_of_git_commit=0370ece" % MD5,
  "прочитаноОбратно": PROP38, "measuredAt": NOW,
  "how": "одним вызовом update_file с fields=id,name,size,md5Checksum,appProperties,createdTime,modifiedTime; "
  "лимит пары — 124 байта в UTF-8, проза живёт в description"},
 "registryCountsAsOfRound49": {k: POUR38[k] for k in ("gitLines", "rows", "queue", "dobytLines",
  "sectionsH2", "bytes", "md5", "measuredAt", "how")},
})
dm["contentRevisions"] = (dm.get("contentRevisions") or []) + [{
 "asOf": UP38, "bytes": B, "lines": L, "md5": MD5, "rows": ROWS,
 "perClass": dict(sorted(CLS.items())), "queue": QUEUE, "dobytLines": DOBYT, "measuredAt": NOW,
 "how": "числа сняты с файла в дереве перед заливкой 38-го слепка",
 "note": ("круг 49: поднят FP-24 (Эразм, парафраза к 1 Тим), снят адрес очереди; классы сдвинулись на один ряд "
  "вверх, очередь сократилась на один адрес — и то, и другое держится одним чтением")}],
dm["liveObjectHistory"] = (dm.get("liveObjectHistory") or []) + [
 {"driveFileId": ID38, "bytes": B, "md5": MD5, "lines": L, "uploadedAt": UP38,
  "status": "живой слепок круга 49; вытеснил 1rCtYH83… в %s (имя + описание одного вызова, appProperties вытесненного "
  "остались своими)" % RET37,
  "why": "реестр правился после зеркала круга 48, и правило 25 требует, чтобы живой объект побайтово равнялся "
  "дереву, а не описывал его со слов"}]

R = J["fourPointMassRegistry20261023"]
R["mirrorPropsRound4920261025"] = {
 "объект": ID38, "имя": NAME38, "папка": "05 — SOURCE LEDGERS & CLAIM MAPS (13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ)",
 "заливка": UP38, "свойства": PROP38, "вытеснение": {ID37: RET37},
 "байт": B, "строк": L, "строкНосителей": ROWS, "md5": MD5,
 "почемуПереливкаАНеLag": ("расхождение было объявлено флагом в первом коммите круга и закрыто переливкой во "
  "втором: правило круга — не «имя имеет право врать, пока флаг стоит», а «флаг стоит ровно до переливки», потому "
  "что имя снимка обещает md5 конкретного дерева"),
 "чтоЭтоДалоДляРеестра": "ничего содержательного: зеркала нужны читающему вне редактора, а счётчики реестра "
 "переснимает гейт; названо, чтобы переливка не выглядела самоцелью",
 "measuredAt": NOW, "checkedAt": NOW,
 "recheckCommand": "python3 -B scripts/validate_atonement_corpus_integrity.py (правило 25)"}

LI.update(newcount)
LI["materialsWithLocators"] = len([r for r in mats if str(r.get("locator") or "").strip()])
LI["measuredAt"] = NOW
LI["checkedAt"] = NOW
LI["countsNote"] = ("числа сняты обходом records этого файла перед записью: %d записей = %d файлов + %d папок; сумма "
 "байт %d; носителей материала %d (роль из appliesOnlyTo.readStateLadder), из них с печатным локатором %d; переснят "
 "кругом 49 после добавления записи о 38-м слепке и перевода записи о 37-м в HOLD_superseded"
 % (len(recs2), newcount["files"], newcount["folders"], newcount["driveBytesSum"], newcount["materials"],
    LI["materialsWithLocators"]))
LI["note"] = (LI.get("note", "") + " Круг 49: +1 запись (живой слепок #38), 37-й переведён в "
 "registry-mirror-superseded с правами HOLD_superseded; папка 05 выросла до 57 объектов — сверка цепочки имён в "
 "driveMirrors.massRegistry20261023.pour38_20261025r49.chainAudit")

COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус: байт", len(COR.read_bytes()), "| индекс: байт", len(IDX.read_bytes()), "| записи", len(recs2))
print("по rights:", newcount["byRights"])
print("по readState:", newcount["byReadState"])
