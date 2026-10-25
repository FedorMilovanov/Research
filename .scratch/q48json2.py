# -*- coding: utf-8 -*-
"""Круг 48, шаг JSON: индекс библиотеки + реестр корпуса.
Все числа снимаются обходом файлов; факты Drive — из ответов get_file/upload_file этого часа."""
import json, pathlib, re, hashlib

ROOT = pathlib.Path("/home/user/Research")
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IDX = ROOT / "ИСКУПЛЕНИЕ/data/atonement-library-index.json"
REG = ROOT / "docs/research/atonement/35_four_point_authors_mass_registry.md"
REC = ROOT / "ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md"
NOW = "2026-10-25T17:22:00Z"

# ---------------- измерения ----------------
reg_txt = REG.read_text(encoding="utf-8")
REG_BYTES = len(reg_txt.encode())
REG_LINES = len(reg_txt.rstrip("\n").split("\n"))
rows = [ln for ln in reg_txt.split("\n") if re.match(r"^\| FP-\d+ \|", ln)]
cls = {}
for ln in rows:
    head = re.match(r"^\| FP-\d+ \|[^|]*\|[^|]*\|[^|]*\|[^|]*\|", ln).group(0)
    k = re.findall(r"`(A1|A2|B1|B2|C)`", head)[0]
    cls[k] = cls.get(k, 0) + 1
queue = len(set(re.findall(r"^- Q-(\d+) —", reg_txt, re.M)))
dobyt_lines = len([ln for ln in reg_txt.split("\n") if "Добыть:" in ln])
share_floor = cls["A1"] * 100 // len(rows)
share_round = round(100 * cls["A1"] / len(rows))
md5 = hashlib.md5(REG.read_bytes()).hexdigest()
sha = hashlib.sha256(REG.read_bytes()).hexdigest()
h2 = len(re.findall(r"^## ", reg_txt, re.M))
rec_txt = REC.read_text(encoding="utf-8")
rec_bytes, rec_lines = len(rec_txt.encode()), len(rec_txt.rstrip("\n").split("\n"))
h3 = len(re.findall(r"^### ", rec_txt, re.M))
assert (len(rows), queue, dobyt_lines, REG_BYTES, REG_LINES, cls["A1"], cls["C"], md5) == (
    209, 97, 4, 469418, 1447, 37, 97, "f4a7f749a1717271d0a6c69d7f95def1"), (
    len(rows), queue, dobyt_lines, REG_BYTES, REG_LINES, cls, md5)
print("реестр: %d Б / %d строк / рядов %d / %s / очередь %d / «Добыть:» %d строк / доля %d(floor) %d(round) / H2 %d"
      % (REG_BYTES, REG_LINES, len(rows), cls, queue, dobyt_lines, share_floor, share_round, h2))
print("17_: %d Б / %d строк / H3 %d" % (rec_bytes, rec_lines, h3))

# ---------------- факты Drive этого часа ----------------
LIVE = "1rCtYH83FjiVEhl4rzgdOmP500XzUFR8U"          # #37, слепокfinal
P36 = "1l535xSDigBFItXcId9uWmhEE5K9kO7ZO"           # #36, первый снимок круга 48, вытеснен через 12 с
P35 = "1jfEydgDot9ZgGZDjSwA-Ehcq0nK7drf2"           # #35, слепок круга 47
P34 = "1cL8icKDA-Jwrs4xMYj4ICN3SBY4flCoo"            # #34, первые шестнадцать минут круга 47
FOLDER_ID = "13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ"
LIVE_UPLOADED = "2026-10-25T17:18:16.832Z"
LIVE_SIZE, LIVE_MD5 = 469418, "f4a7f749a1717271d0a6c69d7f95def1"
P36_UPLOADED, P36_RETIRED = "2026-10-25T17:13:40.086Z", "2026-10-25T17:18:28.535Z"
P36_SIZE, P36_MD5 = 468549, "f155ec3b34d8eec4c1980d0ebf5ed84c"
P35_RETIRED = "2026-10-25T17:13:53.312Z"
P35_SIZE, P35_MD5 = 448944, "0e6769c315980b98033cce96061fde82"
AUDIT = {"объектовСИменемРеестра": 45, "изНихСУСТАРЕЛО": 44, "объектовВПапке": 56}
LIVE_NAME = ("2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 48: 209 строк, %d B, md5 %s).md"
             % (REG_BYTES, md5))
assert (LIVE_SIZE, LIVE_MD5) == (REG_BYTES, md5), "слепок обязан равняться дереву"

# ---------------- индекс ----------------
idx = json.loads(IDX.read_text(encoding="utf-8"))
recs = idx["records"]
byid = {r["driveId"]: r for r in recs}
assert LIVE not in byid and P36 not in byid, "слепки уже в индексе — скрипт не идемпотентен"
assert P35 in byid and P34 in byid

live_rows = set(re.findall(r"^\|\s*FP-(\d+)\s*\|", reg_txt, re.M))
live_q = set(re.findall(r"^- Q-(\d+) —", reg_txt, re.M))


def prune(r, why):
    """адреса и строки, которых больше нет в дереве, не имеют права оставаться в записи."""
    gone_q = [x for x in (r.get("queueRows") or []) if str(x).startswith("Q-") and str(x)[2:] not in live_q]
    if gone_q:
        r["queueRows"] = [x for x in r["queueRows"] if x not in gone_q]
        r["queueRowsPrunedByRound48"] = {"снято": gone_q, "почему": why, "measuredAt": NOW}
    gone_a = [x for x in (r.get("aboutRows") or []) if not re.fullmatch(r"FP-(\d+)", str(x))
              or str(x).split("-")[1].lstrip("0") not in live_rows]
    if gone_a:
        r["aboutRows"] = [x for x in r["aboutRows"] if x not in gone_a]
    return gone_q


RETIRE_WHY = ("адрес Q-22 снят с очереди круга 48: строка FP-22 поднята до `A1` по напечатанной странице A16626 "
              "(с. 250), а правило 25 сверяет объявленные адреса с текущим деревом, не с тем, что было в зеркале")

# 1. #35 — прежний живой слепок: в HOLD_superseded
r35 = byid[P35]
r35["role"] = "registry-mirror-superseded"
r35["name"] = ("УСТАРЕЛО (25.10.2026, круг 48): 35_four_point_authors_mass_registry — заменён слепком %s, "
               "который тем же кругом заменён %s" % (P36, LIVE))
r35["rights"] = "HOLD_superseded"
r35["lagBehindGit"] = True
prune(r35, RETIRE_WHY)
r35["supersededBy20261025r48"] = P36
r35["retiredAt20261025r48"] = P35_RETIRED
r35["note"] = (r35.get("note", "") +
               " Круг 48 переименовал этот слепок в 17:13:53.312Z и перевёл в HOLD_superseded: причина — не починка "
               "вывода, а новые данные (реестр вырос на раздел ## 47, подняты три строки, сняты три адреса очереди). "
               "Содержимое объекта с 16:27:27.239Z не менялось и остаётся побайтово равным дереву круга 47 "
               "(%d B, md5 %s); appProperties намеренно не тронуты — они описывают залитое содержимое, а mirror_of_git_commit "
               "называет то дерево, из которого его лили." % (P35_SIZE, P35_MD5))
r35["registryCountsAsOfRound47Correction"] = {
    "lines": 1418, "fileBytes": P35_SIZE, "registryRows": 209, "queueAddresses": 100, "dobytLines": 2,
    "perClass": {"A1": 34, "A2": 35, "B1": 34, "B2": 6, "C": 100}, "shareA1Percent": 16,
    "mirrorMd5": P35_MD5, "sectionsH2": 47,
    "how": ("снято обходом файла круга 47 после починки §46; число живёт здесь как описание зеркала, а не как живое "
            "число реестра; dobytLines = 2 там было числом строк-нужд, с круга 48 тот же ключ значит механический "
            "`grep -c 'Добыть:'` — расхождение названо в §47 реестра"),
    "measuredAt": NOW}

# 2. #36 — первый снимок круга 48, вытеснен через двенадцать секунд
r36 = {
 "schema": "2026-10-25-drive-mirror-v1", "folder": "05", "driveId": P36, "kind": "file", "mime": "text/markdown",
 "bytes": P36_SIZE,
 "name": ("УСТАРЕЛО (25.10.2026, круг 48): 36_four_point_authors_mass_registry — заменён слепком %s" % LIVE),
 "gitFile": "docs/research/atonement/35_four_point_authors_mass_registry.md",
 "role": "registry-mirror-superseded", "rights": "HOLD_superseded", "readState": "registry_linked",
 "aboutRows": ["FP-022", "FP-074", "FP-078"], "citedBy": [], "queueRows": [],
 "registryRowClasses": {"FP-022": "A1", "FP-074": "A1", "FP-078": "A1"},
 "locator": ("FP-022: A16626, с. 250; FP-074: A62570, с. 366 и A62579, с. 44; FP-078: N03743, с. 64"),
 "driveBytesClaimed": P36_SIZE, "driveMd5Claimed": P36_MD5, "driveBytesVerified": P36_SIZE,
 "driveMd5Verified": P36_MD5, "gitBytesAtUpload": P36_SIZE, "gitFileLinesAtUpload": 1447, "gitRowsAtUpload": 209,
 "gitMd5AtUpload": P36_MD5, "md5VerifiedFromDrive": True, "uploadedAt": P36_UPLOADED, "retiredAt20261025r48": P36_RETIRED,
 "measuredAt": NOW, "checkedAt": NOW, "lagBehindGit": True, "supersededBy20261025r48": LIVE,
 "registryCountsAsOfRound48FirstPour": {
   "lines": 1447, "fileBytes": P36_SIZE, "registryRows": 209, "queueAddresses": 97, "dobytLines": 2,
   "perClass": {"A1": 37, "A2": 35, "B1": 34, "B2": 6, "C": 97}, "shareA1Percent": 18,
   "mirrorMd5": P36_MD5, "sectionsH2": 48,
   "how": ("числа этого снимка сняты тем же обходом, что и баланс круга 48; dobytLines = 2 — счётчик, унаследованный "
           "от круга 42, который этот же круг 48 и починил: механический `grep -c 'Добыть:'` даёт 4 строки, а 2 — "
           "число висящих нужд (REQ-7, REQ-8). Разница между этим объектом и живым слепком — ровно две правки: "
           "оговорка к старому счётчику в §43 и снятие причинного утверждения о годе 1752 в 17_.(1)"),
   "measuredAt": NOW},
 "note": ("первый слепок круга 48: залит в 17:13:40.086Z, сверен get_file (468 549 Б, md5 %s == дерево того "
          "минуты); вытеснен в 17:18:28.535Z, когда тот же круг нашёл в реестре ложное утверждение о счётчике и в "
          "17_ — причинное утверждение, которого доказательства не держат. Сохранён в индексе, чтобы пара «ошибка — "
          "починка» читалась по байтам, а не по описанию: разница файлов %d Б (причина — оговорка в §43 и смягчение "
          "в 17_, ни одна строка-носитель позиции не изменена)." % (P36_MD5, REG_BYTES - P36_SIZE))}
recs.append(r36)

# 3. #34 — снимаем несуществующий адрес
r34 = byid[P34]
prune(r34, RETIRE_WHY)
r34["note"] = (r34.get("note", "") + " Круг 48 убрал из этой записи адрес Q-22 (строка FP-22 поднята до `A1`), "
               "адрес Q-164 в дереве живёт и остаётся открытым.")

# 4. живой слепок
recs.append({
 "schema": "2026-10-25-drive-mirror-v1", "folder": "05", "driveId": LIVE, "kind": "file", "mime": "text/markdown",
 "bytes": REG_BYTES, "name": LIVE_NAME,
 "gitFile": "docs/research/atonement/35_four_point_authors_mass_registry.md",
 "role": "registry-mirror", "rights": "mirror_of_git", "readState": "registry_linked",
 "aboutRows": ["FP-022", "FP-074", "FP-078"], "citedBy": [], "queueRows": [],
 "registryRowClasses": {"FP-022": "A1", "FP-074": "A1", "FP-078": "A1"},
 "locator": ("FP-022: A16626, с. 250 (и с. 242 как цитата Августина); FP-074: A62570, с. 366 и A62579, с. 44; "
             "FP-078: N03743, с. 64"),
 "driveBytesClaimed": REG_BYTES, "driveMd5Claimed": md5, "driveBytesVerified": LIVE_SIZE,
 "driveMd5Verified": LIVE_MD5, "gitBytesAtUpload": REG_BYTES, "gitFileLinesAtUpload": REG_LINES,
 "gitRowsAtUpload": len(rows), "gitMd5AtUpload": md5, "gitSha256AtUpload": sha, "md5VerifiedFromDrive": True,
 "uploadedAt": LIVE_UPLOADED, "measuredAt": NOW, "checkedAt": NOW, "lagBehindGit": False,
 "chainNote": ("тридцать восьмой слепок подряд: … → 1Otzj3fe… (круг 46) → 1cL8icKDA… (круг 47, первые шестнадцать "
               "минут) → 1jfEydgDot… (круг 47, после починки) → 1l535xSDig… (круг 48, первый снимок) → этот "
               "(%d Б). Без пометки «УСТАРЕЛО» ровно он один: обход папки 05 дал %d объектов, в имени которых назван "
               "файл реестра, из них %d с пометкой; всего в папке %d объектов. Разница между %d и %d объясняется "
               "полностью: вытесненный за минуту до этого 1l535xSDig… при переименовании стал называть номер слепка, "
               "а не файл, и в фильтр по имени не попадает — счётчик 45 потому и нельзя читать как «все зеркала»"
               % (REG_BYTES, AUDIT["объектовСИменемРеестра"], AUDIT["изНихСУСТАРЕЛО"], AUDIT["объектовВПапке"],
                  AUDIT["объектовВПапке"], AUDIT["объектовСИменемРеестра"])),
 "note": ("живой слепок круга 48: upload_file в 17:18:16.832Z (%d Б), состояние прочитано get_file — те же байты и "
          "md5 %s, то есть заливка побайтово равна дереву; имя объекта повторяет число строк-носителей, размер и md5 "
          "файла, потому что правило 25 сверяет именно имя. appProperties будут дописаны после коммита — свойство "
          "mirror_of_git_commit называет то дерево, которым залит слепок" % (REG_BYTES, md5)),
 "registryCountsAsOfRound48": {
   "lines": REG_LINES, "fileBytes": REG_BYTES, "registryRows": len(rows), "queueAddresses": queue,
   "dobytLines": dobyt_lines, "perClass": {k: cls[k] for k in ("A1", "A2", "B1", "B2", "C")},
   "shareA1Percent": share_round, "shareA1PercentFloor": share_floor, "mirrorMd5": md5, "mirrorSha256": sha,
   "sectionsH2": h2,
   "текстыEEBO-TCP": {"опробованоИдентификаторов": 17, "репозиториевНашлось": 17, "томовПрочитано": 9,
                      "адресовНамечено": 10, "снятоАдресов": 3, "поднятоСтрок": 3, "опознанийТрудаОтозвано": 9,
                      "попаданийЦитатВтеле": 0, "адресовПереписаноПротоколом": 4,
                      "почемуДевятьАНеТринадцать": ("круг 48 считал прочитанными те TEI-записи, чьё содержимо вошло "
                        "в реестр или в отрицательный протокол: девять томов из перечня в fourPointMassRegistry20261023; "
                        "число 13, встречавшееся в черновиках круга, считало ещё четыре попытки, кончившиеся "
                        "отсутствием репозитория, и в реестр не внесено")},
   "how": ("строки и классы — шаблоном по началу строки таблицы и по первому класс-токену; очередь — подсчётом "
           "уникальных адресов вида `- Q-NN —` (правило 23); «Добыть:» — числом строк файла, содержащих токен "
           "(механический счётчик, не число нужд); доля — целочисленным делением (floor) и отдельно округлением, "
           "расхождение названо; тексты — curl по contents/<id>.xml репозитория textcreationpartnership/<id> с "
           "разбором по маркерам pb n=, поиск по автору в TCP.csv вместо поиска по фрагменту заглавия"),
   "measuredAt": NOW, "checkedAt": NOW}})

files = [r for r in recs if r.get("kind") == "file"]
mats = [r for r in recs if r.get("role") == "material"]
cnt = lambda seq: dict(sorted({x: seq.count(x) for x in set(seq)}.items()))
got = {
 "records": len(recs), "files": len(files), "folders": len([r for r in recs if r.get("kind") == "folder"]),
 "materials": len(mats), "materialsWithLocators": len([r for r in mats if str(r.get("locator") or "").strip()]),
 "byRights": cnt([str(r.get("rights")) for r in recs]),
 "byReadState": cnt([str(r.get("readState")) for r in recs]),
 "driveBytesSum": sum(int(r.get("bytes") or 0) for r in files),
 "largestBytes": max(int(r.get("bytes") or 0) for r in files),
 "scopeFolders": len((idx.get("scope") or {}).get("indexedFolders") or []),
}
print("индекс после правки:", {k: v for k, v in got.items() if k not in ("byRights", "byReadState")})
idx["records"] = recs
IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
IDX_BYTES, IDX_MD5 = len(IDX.read_bytes()), hashlib.md5(IDX.read_bytes()).hexdigest()

# ---------------- корпус ----------------
d = json.loads(COR.read_text(encoding="utf-8"))
m = d["fourPointMassRegistry20261023"]
m["perClass"] = {k: cls[k] for k in ("A1", "A2", "B1", "B2", "C")}
m["queueLength"] = queue
m["shareA1Percent"] = share_round
m["entries"] = len(rows)
m["measuredAt"] = NOW
m["checkedAt"] = NOW
m["registrySectionsMeasured"] = {"H2": h2, "H3": m["registrySectionsMeasured"].get("H3"), "lines": REG_LINES,
                                 "reshotBy": ("круг 48 (2026-10-25): H2 стал 48, потому что добавлен раздел ## 47; "
                                              "число строк файла переснято тем же обходом, что и баланс круга")}
m["fileBytesAsOfRound48"] = REG_BYTES
m["fileMd5AsOfRound48"] = md5
m["fileSha256AsOfRound48"] = sha
m["linesAsOfRound48"] = REG_LINES
m["dobytLinesAsOfRound48"] = dobyt_lines
m["foundThisRound"] = ("круг 48 (2026-10-25, вечер после круга 47): перепись каталога по автору вместо переписи по "
 "фрагменту заглавия. Из десяти адресов, намеченных кругом 47 как цитируемые, правильную работу держит один (Q-22 → "
 "A16626); девять опознаний отозваны с названным механизмом подмены. Три строки подняты до `A1` по напечатанным "
 "страницам: FP-22 (A16626, с. 250 — «non possunt… orare absolutè pro omnibus ut salventur», и «oportet quod tacitè "
 "saltem intelligant de omnibus prædestinatis ad vitam»), FP-74 (A62570, с. 366 — «would have all men to be saved»; "
 "A62579, с. 44 — благорасположение «common to all Men» при условии «Duty and Obedience»), FP-78 (N03743, с. 64 — "
 "«I seem to assert universal Redemption, which I now absolutely deny»). Очередь 100 → 97. Реальных попаданий цитат "
 "в теле напечатанного текста из десяти намеченных — ноль; два найденных «попадания» сидели на титульной странице и "
 "были эхом слов самой очереди. Отдельно починен счётчик «Добыть:»: механический grep даёт 4 строки при двух висящих "
 "нуждах, и поле dobytLines с этого круга значит именно счётчик строк")
m["laneReadmeConsistency20261023"]["liveNumbers"] = {"rows": len(rows), "A1": cls["A1"], "A2": cls["A2"],
    "B1": cls["B1"], "B2": cls["B2"], "C": cls["C"], "queue": queue, "share": share_floor}
m["laneReadmeConsistency20261023"]["measuredAt"] = NOW
m["laneReadmeConsistency20261023"]["checkedAt"] = NOW
m["laneReadmeConsistency20261023"]["method"] = (m["laneReadmeConsistency20261023"].get("method", "") +
 "; переснято кругом 48: восемь чисел README сняты теми же шаблонами, что и обход реестра; расхождений ноль, и "
 "отдельно записано, что с круга 48 два определения доли снова расходятся (17 при целочисленном делении, 18 при "
 "округлении), потому что 37·100/209 = 17.70")
m["authorCensusRound48Finding20261025"] = {
 "что": ("перепись `TCP.csv` (61 315 записей) по подстрочнику фамилии в столбце Author — вместо поиска по фрагменту "
         "заглавия, которым работал круг 47"),
 "записейНаФамилию": {"Whitefield": 64, "Tillotson": 62, "Preston": 33, "Nye": 33, "Chillingworth": 16,
                      "Williams (Daniel, 1643?-1716)": 14, "Ratramnus": 4, "Zanchi": 4, "Bradwardine": 1,
                      "Wardlaw": 0, "Alexander": 0, "Prudentius": 0, "Haymo": 0, "Paschasius": 0, "Godescalcus": 0},
 "ложныйСчёт": ("12 записей дают нулевой смысл: подстрочник «prosper» ловит «vnhappy prosperitie» и «a prosper fall», "
                "а не Проспера Аквитанского — подстрочник фамилии так же опасен, как подстрочник заглавия"),
 "следствие": ("число 66 «адресов без записи» из свода круга 47 есть артефакт способа поиска, а не состояние "
               "источниковой базы; у шести адресов из десяти записи нашлись, и две строки закрыты напечатанной "
               "страницей, а три прочитаны с отрицательным протоколом (Престон, Нее, Занки)"),
 "прочитанныеТома": {"A62570": "Tillotson, Of sincerity and constancy, Chiswell 1695, 618205 Б",
                     "A62579": "Tillotson, The remaining discourses on the attributes of God, Chiswell 1700, 574737 Б",
                     "N03743": ("Whitefield, The Querists — Whitefield's answer, Garden's letters, Zenger, New York "
                                "1740 (Evans 4588), 261865 Б"),
                     "N03645": "Whitefield, answer to the Bishop of London's last pastoral letter, 1739, 49812 Б",
                     "A09997": "Preston, Remaines, 1634, 639823 Б",
                     "A09990": "Preston, The nevv covenant, 1629, 1240898 Б",
                     "A09950": "Preston, The breast-plate of faith and love, 1630, 1180974 Б",
                     "A12183": "Sibbes/Goodwin/Nye, The excellencie of the Gospell above the law, 1639, 582478 Б",
                     "A15859": "Zanchi, Speculum Christianum (пер. H. Nelson), Eld 1614, 726340 Б"},
 "томовПрочитано": 9,
 "команда": ("python-обход TCP.csv: сличение подстрочника фамилии со столбцом Author; чтение TEI через "
             "curl -H 'Accept: application/vnd.github.raw' api.github.com/repos/textcreationpartnership/<id>/contents/"
             "<id>.xml; поиск по страницам через разметку pb n="),
 "measuredAt": NOW, "checkedAt": NOW,
 "recheckCommand": "python3 -B scripts/validate_atonement_corpus_integrity.py (правило 23 переснимает классы и "
                   "очередь; перепись каталога вне дерева, её следы — в строках очереди и в разделе ## 47)"}
m["quoteIdentificationCensus20261025r48"] = {
 "шкала": ("из десяти адресов, помеченных кругом 47 как цитируемые: совпадает ли найденная каталогом запись с трудом "
           "строки (это доля верных опознаний, а не покрытие реестра цитатами)"),
 "верно": 1, "авторВеренТрудНеТот": 2, "записьЛожная": 7,
 "доляВерныхОпознанийПроцент": round(1 * 100 / 10, 2),
 "попаданийЦитатВТеле": 0, "доляПопаданийПроцент": 0.0, "попаданияНаТитуле": 2,
 "механизмыПодмены": {"Q-02": "«Capitula» → кентерберийский синод 1597 (A00075)",
  "Q-12": "Пруденцию приписан Flacius, *Wonderfull newes of the death of Paule the iii.* (A00402, 1552)",
  "Q-58": "Престону приписаны *Quodlibets* Robert Hayman (A02836, 1628)",
  "Q-64": "«interest of the kingdome» — фраза, вписанная в адрес кругом 46, ловит ответ «G. G.» о речи Чэлонера (A85742)",
  "Q-74": ("K008295.001 *The Rambler* Джонсона; между адресом и книгой только совпадение по году 1752, большая "
           "причина подмены документально не установлена"),
  "Q-78": "верный автор, чужой труд: *Christmas well kept* (N03638)",
  "Q-81": "«Balances» ловит *God and the world weighted in the balances* Роуорта (A58146, 1656)",
  "Q-164": "верный автор и переводчик, не тот трактат (A97309)",
  "Q-167": "чужой век: *The repentance of Iohn Haren* (A02641, 1610)"},
 "почемуНеГрадация": ("ни одно опознание не стало основанием для повышения класса: подняты те три строки, место "
                      "которых найдено по смысловому якорю и прочитано глазами, — правило 15zm.3"),
 "measuredAt": NOW, "checkedAt": NOW}
m["queueClosures20261025r48"] = {
 "снято": 3, "добавлено": 0, "остаток": queue,
 "как": ("строки FP-22, FP-74 и FP-78 переведены в `A1` по напечатанной странице тома (A16626, с. 250; A62570, "
         "с. 366 и A62579, с. 44; N03743, с. 64); у FP-22 снят номер книги, унаследованный от индекса, у FP-74 снято "
         "требование *Works* 1752 г. и приписанная строке фраза «universal redemption», у FP-78 снято ожидание "
         "издания Тайлера 1871 г."),
 "переписаноПротоколом": ["Q-58", "Q-64", "Q-164", "Q-11"],
 "остатокОчередиШкалаПроцент": round(queue * 100 / 102, 2),
 "measuredAt": NOW, "checkedAt": NOW}
m["queueNote20261025r48"] = ("очередь 97 = 97 адресов и 97 строк класса `C` (правило 23 держит биекцию); за два "
 "круга из 102 адресов закрыто 5, то есть %.2f %% по шкале очереди, остаток %.2f %%" % (5 * 100 / 102, queue * 100 / 102))
dm = d["driveMirrors"]["massRegistry20261023"]
dm.update({"driveFileId": LIVE, "bytes": REG_BYTES, "md5Local": md5, "sha256Local": sha,
 "fileLines": REG_LINES, "rows": len(rows), "lagBehindGit": False, "driveFileName": LIVE_NAME, "fileName": LIVE_NAME,
 "uploadedAt": LIVE_UPLOADED, "driveMd5Verified": LIVE_MD5, "driveBytesVerified": LIVE_SIZE,
 "gitSha256AtUpload": sha, "md5VerifiedFromDrive": True, "measuredAt": NOW, "checkedAt": NOW,
 "supersededPreviousSnapshot": P36,
 "verification": ("get_file вернул size %d и md5 %s — те же, что у файла в дереве; вытесненные объекты переименованы "
                  "и переведены в HOLD_superseded с сохранением своего содержимого: %s — в 17:18:28.535Z (468 549 Б, "
                  "md5 %s), %s — в 17:13:53.312Z (448 944 Б, md5 %s); appProperties ни у того, ни у другого не "
                  "тронуты, потому что они описывают залитое содержимое"
                  % (LIVE_SIZE, LIVE_MD5, P36, P36_MD5, P35, P35_MD5)),
 "how": ("тридцать восьмая переливка: заливалось побайтово то же, что в рабочем дереве; имя объекта повторяет число "
         "строк-носителей, размер и md5 файла — на него смотрит правило 25; сверка читалась get_file; имена "
         "вытесненных объектов поменял update_file"),
 "pour37_20261025r48": {"at": LIVE_UPLOADED, "driveFileId": LIVE, "bytes": REG_BYTES, "md5": md5, "sha256": sha,
   "gitLines": REG_LINES, "rows": len(rows), "queue": queue, "dobytLines": dobyt_lines, "sectionsH2": h2,
   "verification": ("get_file в 17:18:1xZ вернул size %d и md5 %s; после заливки реестр больше не правился — файл "
                    "заморожен тем же кругом, что и зеркалирован" % (LIVE_SIZE, LIVE_MD5)),
   "chainAudit": dict(AUDIT, команда=("list_files по папке 05 с фильтром имени '35_four_point_authors_mass_registry' "
                                      "(45), то же плюс 'УСТАРЕЛО' (44), и обход папки без фильтров (56); пагинация "
                                      "не сработала ни разу — одна страница закрывает выборку"), measuredAt=NOW),
   "measuredAt": NOW,
   "how": "upload_file (file_path указывает на файл рабочего дерева), затем get_file для чтения состояния"},
 "pour36_20261025": {"at": P36_UPLOADED, "driveFileId": P36, "bytes": P36_SIZE, "md5": P36_MD5,
   "gitLines": 1447, "rows": 209, "queue": 97, "dobytLinesRecorded": 2, "dobytLinesMechanical": 4,
   "livedForSeconds": 12,
   "verification": ("get_file вернул size 468549 и md5 f155ec3b34d8eec4c1980d0ebf5ed84c — слепок был равен дереву "
                    "того часа; вытеснен, потому что дерево с тех пор изменилось на две правки (оговорка к "
                    "наследованному счётчику в §43 и снятие причинного утверждения о годе 1752 в 17_.(1)), а слепок "
                    "обязан равенству побайтно, иначе он становится второй копией вместо зеркала"),
   "measuredAt": NOW, "retiredAt": P36_RETIRED,
   "how": "upload_file, get_file, затем update_file (имя + описание) для пометки «УСТАРЕЛО»"},
 "mirrorOfGitCommitNote20261025r48": ("свойство mirror_of_git_commit будет дописано в appProperties живого слепка "
   "после коммита; короткое имя коммита в тело реестра не переносится — правило 20 читает семи- и восьмизначный "
   "шестнадцатеричный токен как ссылку на объект git и требует живого git show"),
 "propsNote20261025r48": ("свойства живого слепка будут перечислены после записи: ожидается десять ключей "
   "(registry_bytes, registry_rows, registry_md5, registry_classes, registry_queue, registry_dobyt, registry_role, "
   "source, rights, mirror_of_git_commit); байты, md5 и счётчики описывают залитое содержимое, а не позднее дерево")})
li = d["libraryIndex20261023"]
li.update(got)
li["measuredAt"] = NOW
li["checkedAt"] = NOW
li["method"] = (li.get("method", "") + "; переснято кругом 48 тем же обходом: добавлена запись о 38-м слепке "
 "(%d Б), добавлена запись о вытесненном 37-м (468 549 Б, прожил двенадцать минут и пятьдесят две секунды), запись "
 "36-го переведена в registry-mirror-superseded/HOLD_superseded с lagBehindGit; у записей 34-го и 36-го убран адрес "
 "Q-22, которого в дереве больше нет" % REG_BYTES)
li["countsNote"] = ("числа сняты обходом records этого файла перед записью: %d записей = %d файлов + %d папок; сумма "
 "байт %d (в неё входят и вытесненные слепки — индекс описывает папку, а не только живое); пересъём — круг 48, шаг "
 "записи зеркала" % (got["records"], got["files"], got["folders"], got["driveBytesSum"]))
li["note"] = (li.get("note", "") + "; круг 48: записей %d, файлов %d, сумма байт %d. Живых зеркал реестра в "
 "папке `05` осталось одно (#37); устаревших с пометкой — 44 из 45 объектов, в чьём имени назван файл реестра "
 "(всего в папке %d объектов). В эти 45 не попадает #36, переименованный за минуту до этого: его имя стало "
 "называть номер слепка, а не файл, — счётчик по имени не то же самое, что перепись папки"
 % (got["records"], got["files"], got["driveBytesSum"], AUDIT["объектовВПапке"]))
d["reproducibility20261022"]["countsLive"]["очередейДобычиМассы"] = queue
d["reproducibility20261022"]["countsLive"]["строкРеестраМассы"] = len(rows)
d["reproducibility20261022"]["countsLive"]["measuredAt"] = NOW
d["reproducibility20261022"]["countsLive"]["method"] = (
 d["reproducibility20261022"]["countsLive"].get("method", "") +
 "; переснято кругом 48 (очередь 100 → 97 по снятым Q-22, Q-74 и Q-78; классов `A1` стало 37; находка круга "
 "записана вложенными блоками fourPointMassRegistry20261023, верхнеуровневых ключей не добавлено — их число "
 "сверяется правилом 21)")
rd = d["reconciliationDocument20261022"]
rd["lines"] = rec_lines
rd["fileBytes"] = rec_bytes
rd["sectionsH3"] = h3
rd["measuredAt"] = NOW
rd["checkedAt"] = NOW
rd["history"].append({"at": NOW, "round": "48",
 "что": ("блок 15zm. из четырёх правил: труд опознаётся по автору, а фрагмент заглавия — улика; попадание на титуле "
         "не есть попадание; прочитанная страница важнее формулы, с которой в неё пришли; наследовать номер книги или "
         "проповеди — то же, что наследовать цитату. Тем же кругом из правила 15zm.1 снято причинное утверждение о "
         "годе 1752: между адресом Q-74 и *The Rambler* только совпадение годов, большая причина подмены "
         "документально не установлена"),
 "lines": rec_lines, "sectionsH2": rd["sectionsH2"], "sectionsH3": h3, "fileBytes": rec_bytes,
 "measuredAt": NOW,
 "how": ("снято определением проверки: len(text.rstrip('\\n').split('\\n')); newline-счёт даёт на единицу больше "
         "из-за пустой строки в конце"),
 "command": "python3 -B scripts/validate_atonement_corpus_integrity.py"})
COR.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус: %d Б / %d верхнеуровневых ключей | индекс: %d Б md5 %s"
      % (len(COR.read_bytes()), len(d), IDX_BYTES, IDX_MD5))
