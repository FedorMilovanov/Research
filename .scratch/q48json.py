# -*- coding: utf-8 -*-
"""Круг 48, шаг JSON: корпусный реестр + индекс библиотеки.
Числа берутся из файлов, а не из памяти круга; mirror-поля — из ответов Drive этого часа."""
import json, pathlib, re, hashlib, sys

ROOT = pathlib.Path("/home/user/Research")
COR = ROOT / "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IDX = ROOT / "ИСКУПЛЕНИЕ/data/atonement-library-index.json"
REG = ROOT / "docs/research/atonement/35_four_point_authors_mass_registry.md"
REC = ROOT / "ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md"
NOW = "2026-10-25T17:20:00Z"

reg_txt = REG.read_text(encoding="utf-8")
REG_BYTES = len(reg_txt.encode())
REG_LINES = len(reg_txt.rstrip("\n").split("\n"))
rows = [ln for ln in reg_txt.split("\n") if re.match(r"^\| FP-\d+ \|", ln)]
cls = {}
for ln in rows:
    m = re.match(r"^\| FP-\d+ \|[^|]*\|[^|]*\|[^|]*\|[^|]*\|", ln)
    k = re.findall(r"`(A1|A2|B1|B2|C)`", m.group(0))
    cls[k[0]] = cls.get(k[0], 0) + 1
queue = len(set(re.findall(r"^- Q-(\d+) —", reg_txt, re.M)))
share_floor = cls["A1"] * 100 // len(rows)
share_round = round(100 * cls["A1"] / len(rows))
md5 = hashlib.md5(REG.read_bytes()).hexdigest()
sha = hashlib.sha256(REG.read_bytes()).hexdigest()
h2 = len(re.findall(r"^## ", reg_txt, re.M))
dobyt = len(re.findall(r"Добыть:", reg_txt))
rec_txt = REC.read_text(encoding="utf-8")
rec_lines = len(rec_txt.rstrip("\n").split("\n"))
rec_bytes = len(rec_txt.encode())
print("реестр: %d Б / %d строк / рядов %d / %s / очередь %d / доля %d(floor) %d(round) / H2 %d / Добыть %d"
      % (REG_BYTES, REG_LINES, len(rows), cls, queue, share_floor, share_round, h2, dobyt))
print("17_: %d Б / %d строк" % (rec_bytes, rec_lines))
assert (len(rows), queue, dobyt, md5) == (209, 97, 2, "f155ec3b34d8eec4c1980d0ebf5ed84c")

# ---------------- индекс ----------------
idx = json.loads(IDX.read_text(encoding="utf-8"))
recs = idx["records"]
LIVE = "1l535xSDigBFItXcId9uWmhEE5K9kO7ZO"
OLD = "1jfEydgDot9ZgGZDjSwA-Ehcq0nK7drf2"
PREV = "1Otzj3fe-u1QL08sXC3AGsSPhZkWAW4hI"
byid = {r["driveId"]: r for r in recs}
assert LIVE not in byid and OLD in byid and PREV in byid

# 1. прежний живой слепок -> УСТАРЕЛО
r35 = byid[OLD]
r35["name"] = ("УСТАРЕЛО (25.10.2026, круг 48): 35_four_point_authors_mass_registry — заменён слепком "
               "1l535xSDigBFItXcId9uWmhEE5K9kO7ZO")
r35["role"] = "registry-mirror-superseded"
r35["rights"] = "HOLD_superseded"
r35["lagBehindGit"] = True
r35["queueRows"] = ["Q-164"]
r35["supersededBy20261025r48"] = LIVE
r35["retiredAt20261025r48"] = "2026-10-25T17:13:53.312Z"
r35["note"] = (r35.get("note", "") + " Круг 48 перевёл этот слепок в HOLD_superseded и переименовал его в 17:13:53.312Z: "
  "причина — не починка вывода, а новые данные (реестр вырос на раздел ## 47, подняты три строки, сняты три адреса "
  "очереди). Содержимое объекта не менялось с 16:27:27.239Z и остаётся побайтово равным дереву круга 47 (448 944 B, "
  "md5 0e6769c315980b98033cce96061fde82); appProperties намеренно не тронуты — они описывают залитое содержимое. "
  "Список адресов очереди у записи укорочен кругом 48: Q-22 в сегодняшнем дереве нет, а адрес Q-164 в нём живёт и "
  "остаётся открытым.")
r35["registryCountsAsOfRound47Correction"] = {"lines": 1418, "fileBytes": 448944, "registryRows": 209,
                                              "queueAddresses": 100, "dobytLines": 2,
                                              "perClass": {"A1": 34, "A2": 35, "B1": 34, "B2": 6, "C": 100},
                                              "shareA1Percent": 16, "mirrorMd5": "0e6769c315980b98033cce96061fde82",
                                              "sectionsH2": 47,
                                              "how": "снято обходом файла круга 47 после починки §46; число живёт здесь "
                                                     "как описание зеркала, а не как живое число реестра",
                                              "measuredAt": NOW}

# 2. запись круга 47 (#34) — снимаем несуществующий адрес
r34 = byid[PREV]
r34["queueRows"] = ["Q-164"]
r34["note"] = (r34.get("note", "") + " Круг 48 убрал из этой записи адрес Q-22: строка FP-22 поднята до `A1` и адрес "
  "снят с очереди, а проверка правила 25 сверяет объявленные адреса с текущим деревом, не с тем, что было в зеркале.")

# 3. новая запись о живом слепке
new_rec = {
 "folder": "05", "driveId": LIVE, "kind": "file", "mime": "text/markdown", "bytes": REG_BYTES,
 "name": ("2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 48: 209 строк, %d B, md5 %s).md"
          % (REG_BYTES, md5)),
 "gitFile": "docs/research/atonement/35_four_point_authors_mass_registry.md",
 "role": "registry-mirror", "rights": "mirror_of_git", "readState": "registry_linked",
 "aboutRows": ["FP-022", "FP-074", "FP-078"], "citedBy": [], "queueRows": [],
 "registryRowClasses": {"FP-022": "A1", "FP-074": "A1", "FP-078": "A1"},
 "locator": ("FP-022: A16626, с. 250 (и с. 242 как цитата Августина); FP-074: A62570, с. 366 и A62579, с. 44; "
             "FP-078: N03743, с. 64"),
 "driveBytesClaimed": REG_BYTES, "driveMd5Claimed": md5,
 "driveBytesVerified": 468549, "driveMd5Verified": "f155ec3b34d8eec4c1980d0ebf5ed84c",
 "gitBytesAtUpload": REG_BYTES, "gitFileLinesAtUpload": REG_LINES, "gitRowsAtUpload": len(rows),
 "gitMd5AtUpload": md5, "gitSha256AtUpload": sha, "md5VerifiedFromDrive": True,
 "uploadedAt": "2026-10-25T17:13:40.086Z", "measuredAt": NOW, "lagBehindGit": False,
 "chainNote": ("тридцать седьмой слепок подряд: … → 1OTWnh6E… (круг 45, шаг 3) → 1Otzj3fe… (круг 46) → 1cL8icKDA… "
  "(круг 47, первые шестнадцать минут) → 1jfEydgDot… (круг 47, после починки) → этот (%d Б); без пометки «УСТАРЕЛО» "
  "ровно он один: поиск по имени реестра в папке 05 дал 45 объектов, из них 44 с пометкой, в папке 55 объектов"
  % REG_BYTES),
 "note": ("живой слепок круга 48: upload_file в 17:13:40.086Z (468 549 Б), состояние прочитано get_file — те же байты "
  "и md5 f155ec3b34d8eec4c1980d0ebf5ed84c, то есть заливка побайтово равна дереву. Переливан потому, что круг поднял "
  "три строки и снял три адреса: правило 25 сверяет имя зеркала с деревом, а слепок, отстающий от дерева на раздел, "
  "был бы носителей, а не копией. appProperties будут дописаны после коммита шага 6 — свойство mirror_of_git_commit "
  "называет то дерево, которым залит слепок"),
 "registryCountsAsOfRound48": {
   "lines": REG_LINES, "fileBytes": REG_BYTES, "registryRows": len(rows), "queueAddresses": queue,
   "dobytLines": dobyt, "perClass": {k: cls[k] for k in ("A1", "A2", "B1", "B2", "C")},
   "shareA1Percent": share_round, "shareA1PercentFloor": share_floor, "mirrorMd5": md5, "sectionsH2": h2,
   "текстыEEBO-TCP": {"опробованоИдентификаторов": 17, "репозиториевНашлось": 17, "прочитаноТранскрипций": 13,
                      "снятоАдресов": 3, "поднятоСтрок": 3, "опознанийТрудаОтозвано": 9, "попаданийЦитатВтеле": 0,
                      "адресовПереписаноПротоколом": 4},
   "how": ("строки и классы — шаблоном по началу строки таблицы и по первому класс-токену; очередь — подсчётом строк "
           "очереди (правило 23); тексты — curl по contents/<id>.xml репозитория textcreationpartnership/<id> с "
           "разбором по маркерам pb n=, поиск по автору в TCP.csv вместо поиска по фрагменту заглавия"),
   "measuredAt": NOW},
}
recs.append(new_rec)

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
idx_path_written = False
IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
IDX_BYTES = len(IDX.read_bytes())
IDX_MD5 = hashlib.md5(IDX.read_bytes()).hexdigest()

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
                                 "reshotBy": "круг 48 (2026-10-25): H2 стал 48, потому что добавлен раздел ## 47; "
                                              "число строк файла переснято тем же обходом, что и баланс круга"}
m["fileBytesAsOfRound48"] = REG_BYTES
m["fileMd5AsOfRound48"] = md5
m["fileSha256AsOfRound48"] = sha
m["linesAsOfRound48"] = REG_LINES
m["foundThisRound"] = ("круг 48 (2026-10-25, вечер после круга 47): перепись каталога по автору вместо переписи по "
 "фрагменту заглавия. Из десяти адресов, намеченных кругом 47 как цитируемые, правильную работу держит один (Q-22 → "
 "A16626); девять опознаний отозваны с названным механизмом подмены. Три строки подняты до `A1` по напечатанным "
 "страницам: FP-22 (A16626, с. 250 — «non possunt… orare absolutè pro omnibus ut salventur», и «oportet quod tacitè "
 "saltem intelligant de omnibus prædestinatis ad vitam»), FP-74 (A62570, с. 366 — «would have all men to be saved»; "
 "A62579, с. 44 — благорасположение «common to all Men» при условии «Duty and Obedience»), FP-78 (N03743, с. 64 — "
 "«I seem to assert universal Redemption, which I now absolutely deny»). Очередь 100 → 97. Реальных попаданий цитат "
 "в теле напечатанного текста из десяти намеченных — ноль; два найденных «попадания» сидели на титульной странице и "
 "были эхом слов самой очереди")
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
 "прочитанныеТома": {"A62570": "Tillotson, Of sincerity and constancy, 1695, 618205 Б",
                     "A62579": "Tillotson, The remaining discourses on the attributes of God, 1700, 574737 Б",
                     "N03743": "Whitefield, The Querists — Whitefield's answer, Garden's letters, Evans 4588, 1740, 261865 Б",
                     "N03645": "Whitefield, answer to the Bishop of London's last pastoral letter, Evans 4457, 1739, 49812 Б",
                     "A09997": "Preston, Remaines, 1634, 639823 Б",
                     "A09990": "Preston, The nevv covenant, 1629, 1240898 Б",
                     "A09950": "Preston, The breast-plate of faith and love, 1630, 1180974 Б",
                     "A12183": "Sibbes/Goodwin/Nye, The excellencie of the Gospell above the law, 1639, 582478 Б",
                     "A15859": "Zanchi, Speculum Christianum (пер. H. Nelson), 1614, 726340 Б"},
 "команда": ("python-обход TCP.csv: сличение подстрочника фамилии со столбцом Author; чтение TEI через "
             "curl -H 'Accept: application/vnd.github.raw' api.github.com/repos/textcreationpartnership/<id>/contents/"
             "<id>.xml; поиск по страницам через разметку pb n="),
 "measuredAt": NOW, "checkedAt": NOW,
 "recheckCommand": "python3 -B scripts/validate_atonement_corpus_integrity.py (правило 23 переснимает классы и очередь; перепись каталога — вне дерева, её следы в строках очереди и в разделе ## 47)"}
m["quoteIdentificationCensus20261025r48"] = {
 "шкала": "из десяти адресов, помеченных кругом 47 как цитируемые: совпадает ли найденная каталогом запись с трудом строки",
 "верно": 1, "авторВеренТрудНеТот": 2, "записьЛожная": 7,
 "доляВерныхОпознанийПроцент": round(1 * 100 / 10, 2),
 "попаданийЦитатВТеле": 0, "доляПопаданийПроцент": 0.0,
 "попаданияНаТитуле": 2,
 "механизмыПодмены": {"Q-02": "«Capitula» → кентерберийский синод 1597 (A00075)",
  "Q-12": "Пруденцию приписан Flacius, *Wonderfull newes of the death of Paule the iii.* (A00402, 1552)",
  "Q-58": "Престону приписаны *Quodlibets* Robert Hayman (A02836, 1628)",
  "Q-64": "«interest of the kingdome» — фраза, вписанная в адрес кругом 46, ловит ответ «G. G.» о речи Чэлонера (A85742)",
  "Q-74": "год 1752 ловит *The Rambler* Джонсона (K008295.001)",
  "Q-78": "верный автор, чужой труд: *Christmas well kept* (N03638)",
  "Q-81": "«Balances» ловит *God and the world weighted in the balances* Роуорта (A58146, 1656)",
  "Q-164": "верный автор и переводчик, не тот трактат (A97309)",
  "Q-167": "чужой век: *The repentance of Iohn Haren* (A02641, 1610)"},
 "почемуНеГрадациz": ("ни одно опознание не стало основанием для повышения класса: подняты те три строки, место "
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
 "круга из 102 адресов закрыто 5, то есть %.2f %%, остаток %.2f %%" % (5 * 100 / 102, queue * 100 / 102))
dm = d["driveMirrors"]["massRegistry20261023"]
dm.update({"driveFileId": LIVE, "bytes": REG_BYTES, "md5Local": md5, "sha256Local": sha,
 "fileLines": REG_LINES, "rows": len(rows), "lagBehindGit": False,
 "driveFileName": ("2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 48: 209 строк, %d B, md5 %s).md"
                   % (REG_BYTES, md5)),
 "fileName": "2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 48: 209 строк, %d B, md5 %s).md" % (REG_BYTES, md5),
 "uploadedAt": "2026-10-25T17:13:40.086Z", "driveMd5Verified": md5, "driveBytesVerified": 468549,
 "gitSha256AtUpload": sha, "md5VerifiedFromDrive": True, "measuredAt": NOW, "checkedAt": NOW,
 "supersededPreviousSnapshot": OLD,
 "verification": ("get_file вернул size 468549 и md5 f155ec3b34d8eec4c1980d0ebf5ed84c — те же, что у файла в дереве; "
                  "вытесненный 1jfEydgDot9ZgGZDjSwA-Ehcq0nK7drf2 переименован в 17:13:53.312Z в «УСТАРЕЛО (25.10.2026, "
                  "круг 48)» и переведён в HOLD_superseded с сохранением своих чисел (448 944 B, md5 "
                  "0e6769c315980b98033cce96061fde82); его appProperties тронуты не были"),
 "how": ("тридцать седьмая переливка: заливалось побайтово то же, что в рабочем дереве, имя объекта повторяет размер "
         "и md5 файла, сверка читалась get_file, имя вытесненного объекта поменял update_file"),
 "pour36_20261025": {"at": "2026-10-25T17:13:40.086Z", "driveFileId": LIVE, "bytes": 468549, "md5": md5,
   "gitLines": REG_LINES, "rows": len(rows), "queue": queue, "dobyt": dobyt,
   "verification": ("get_file в 17:13:4xZ вернул size 468549 и md5 f155ec3b34d8eec4c1980d0ebf5ed84c; файл не менялся "
                    "с момента заливки — реестр больше не правился в этом кругу"),
   "chainAudit": {"объектовСИменемРеестра": 45, "изНихСУСТАРЕЛО": 44, "объектовВПапке": 55,
     "команда": ("list_files с q \"'13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ' in parents and trashed = false and name "
                 "contains '35_four_point_authors_mass_registry'\" (45) и то же с 'name contains УСТАРЕЛО' (44), "
                 "list_files по папке целиком (55)"), "measuredAt": NOW},
   "measuredAt": NOW, "how": "upload_file (file_path указывает на файл рабочего дерева), затем get_file для чтения состояния"},
 "mirrorChainNameAudit20261025r48": {"объектовСИменемРеестра": 45, "изНихСУСТАРЕЛО": 44, "объектовВПапке": 55,
   "команда": ("list_files по папке 05 с двумя фильтрами имени и без них; живой слепок ровно один — это #36 "
               "(1l535xSDigBFItXcId9uWmhEE5K9kO7ZO)"), "measuredAt": NOW},
 "mirrorOfGitCommitNote20261025r48": ("свойство mirror_of_git_commit будет дописано в appProperties живого слепка "
   "после коммита шага 6; короткое имя коммита в тело реестра не переносится (правило 20 читает семи- и "
   "восьмизначный шестнадцатеричный токен как ссылку на объект git и требует живого git show)"),
 "propsNote20261025r48": ("свойства объекта будут перечислены после записи: ожидается десять ключей (registry_bytes, "
   "registry_rows, registry_md5, registry_classes, registry_queue, registry_role, registry_read_state, source, rights, "
   "mirror_of_git_commit); байты и md5 описывают залитое содержимое, а не позднее дерево")})
li = d["libraryIndex20261023"]
li.update(got)
li["measuredAt"] = NOW
li["checkedAt"] = NOW
li["method"] = (li.get("method", "") + "; переснято кругом 48 тем же обходом: добавлена запись о 37-м слепке (468 549 Б), "
 "запись 36-го переведена в registry-mirror-superseded/HOLD_superseded с lagBehindGit, у обеих записей убран адрес "
 "Q-22, которого в дереве больше нет")
li["countsNote"] = ("числа сняты обходом records этого файла перед записью: %d записей = %d файлов + %d папок; сумма "
 "байт %d; пересъём — круг 48, шаг записи зеркала" % (got["records"], got["files"], got["folders"], got["driveBytesSum"]))
li["fileBytes"] = IDX_BYTES
li["fileMd5"] = IDX_MD5
d["reproducibility20261022"]["countsLive"]["очередейДобычиМассы"] = queue
d["reproducibility20261022"]["countsLive"]["строкРеестраМассы"] = len(rows)
d["reproducibility20261022"]["countsLive"]["measuredAt"] = NOW
d["reproducibility20261022"]["countsLive"]["method"] = (
 d["reproducibility20261022"]["countsLive"].get("method", "") +
 "; переснято кругом 48 (очередь 100 → 97 по снятым Q-22, Q-74 и Q-78; классов A1 стало 37; ключей реестра осталось "
 "%d — находка круга записана вложенными блоками fourPointMassRegistry20261023, верхнеуровневых ключей не добавлено)"
 % len(d))
rd = d["reconciliationDocument20261022"]
rd["lines"] = rec_lines
rd["fileBytes"] = rec_bytes
rd["sectionsH3"] = len(re.findall(r"^### ", rec_txt, re.M))
rd["measuredAt"] = NOW
rd["checkedAt"] = NOW
rd["history"].append({"at": NOW, "round": "48",
 "что": ("блок 15zm. из четырёх правил: труд опознаётся по автору, а фрагмент заглавия — улика; попадание на титуле "
         "не есть попадание; прочитанная страница важнее формулы, с которой в неё пришли; наследовать номер книги или "
         "проповеди — то же, что наследовать цитату"),
 "lines": rec_lines, "sectionsH2": rd["sectionsH2"], "sectionsH3": rd["sectionsH3"], "fileBytes": rec_bytes,
 "measuredAt": NOW,
 "how": "снято определением проверки: len(text.rstrip('\\n').split('\\n')); newline-счёт даёт на единицу больше из-за пустой строки в конце",
 "command": "python3 -B scripts/validate_atonement_corpus_integrity.py"})
st = d["integrityGate"]["scopeOfMeasurementRules"]["stampedFieldsPerRegistry"]
st["measuredAt"] = NOW
st["checkedAt"] = NOW
COR.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус: %d Б | индекс: %d Б" % (len(COR.read_bytes()), IDX_BYTES))
print("заявленные счётчики индекса:", {k: v for k, v in got.items() if k not in ("byRights", "byReadState")})
