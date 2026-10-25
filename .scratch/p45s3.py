import json,pathlib,hashlib
from collections import Counter
ROOT=pathlib.Path("/home/user/Research")
Rg=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
b=Rg.read_bytes(); B=len(b); M=hashlib.md5(b).hexdigest(); S=hashlib.sha256(b).hexdigest(); L=b.count(b"\n")
assert (B,M,L)==(422703,"cf1dd2ba5767afa77c6167d769aeda8d",1379),(B,M,L)
ID32="1OTWnh6Ejcjtm_T7GIt-tO1O3ueVCzYlX"; ID31="1-iyXbJbUw9ncpOwaOudU8woaa-8sR17q"
B31=422440; M31="1fc7b00018c0d484eea641796e213b58"; L31=1379
T="2026-10-25T14:56:00Z"
IP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-library-index.json"
d=json.loads(IP.read_text(encoding="utf-8")); recs=d["records"]
r31=recs[-1]; assert r31["driveId"]==ID31
r31.update({"name":"УСТАРЕЛО (25.10.2026, круг 45 шаг 3): 35_four_point_authors_mass_registry — заменён слепком "+ID32,
 "role":"registry-mirror-superseded","rights":"HOLD_superseded","lagBehindGit":True,"measuredAtGit":T,
 "note":("слепок круга 45 шага 1 (%d B, %d строк файла), вытеснен шагом 3 того же круга: в реестре переснят один ряд таблицы остатка — «адреса "
   "очереди, закрытые ланом» 2 → 0, байтов стало %d; имя и описание переведены update_file в 2026-10-25T14:55:39Z, appProperties объекта "
   "намеренно не тронуты (registry_bytes=%d, registry_md5=%s, mirror_of_git_commit оставлен на дереве шага 1) — они описывают залитое содержимое, "
   "а не текущий вывод реестра; содержимое файла в Drive не менялось")%(B31,L31,B,B31,M31),
 "supersededBy20261025r45step3":ID32,
 "retiredBy20261025r45step3":{"at":"2026-10-25T14:55:39Z","how":"update_file (имя + описание); состояние прочитано ответом того же вызова",
  "note":"единственный случай за круг, когда слепок вытеснен собственным кругом: правка нашлась после заливки, а не до неё"}})
r31["registryCountsAsOfRound45"]["recheck20261025r45step3"]=("между шагом 1 и шагом 3 разница одна: переснят ряд таблицы остатка (2 кандидата → 0) "
  "и %d байта прозы"%(B-B31))
new={"folder":"05","driveId":ID32,"kind":"file","mime":"text/markdown","bytes":B,
 "name":"2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 45 шаг 3: 209 строк, %d B, md5 %s).md"%(B,M),
 "gitFile":"docs/research/atonement/35_four_point_authors_mass_registry.md",
 "role":"registry-mirror","rights":"mirror_of_git","readState":"registry_linked",
 "aboutRows":[],"citedBy":[],"queueRows":[],"registryRowClasses":{},"locator":"",
 "driveBytesClaimed":B,"driveMd5Claimed":M,"driveBytesVerified":B,"driveMd5Verified":M,
 "gitBytesAtUpload":B,"gitFileLinesAtUpload":L,"gitRowsAtUpload":209,"gitMd5AtUpload":M,"gitSha256AtUpload":S,
 "md5VerifiedFromDrive":True,"uploadedAt":"2026-10-25T14:55:26.998Z","measuredAtGit":T,"lagBehindGit":False,
 "chainNote":("тридцать второй слепок подряд: … → 1T6gNz8O… → 1BFrPIKM… → 1s_VudOC… (все три круга 44) → 1-iyXbJb… (круг 45, шаг 1) → этот "
   "(%d B); без пометки «УСТАРЕЛО» ровно он один: поиск по имени реестра дал 41 объект, из них 40 с пометкой, в папке 51")%B,
 "note":("живой слепок круга 45 шага 3: залито upload_file в 2026-10-25T14:55:26.998Z (%d B), состояние прочитано get_file тем же ответом — те же "
   "байты и md5 %s; десять свойств дописаны после коммита шага 3. aboutRows и queueRows пусты: шаг 3 не двинул ни одного класса и ни одного адреса, "
   "он переснял число в таблице остатка")%(B,M),
 "registryCountsAsOfRound45Step3":{"lines":L,"fileBytes":B,"registryRows":209,"queueAddresses":102,"dobytLines":2,
  "perClass":{"A1":32,"A2":35,"B1":34,"B2":6,"C":102},"shareA1Percent":15,"mirrorMd5":M,"sectionsH2":45,
  "очередьЗакрытаИзЛана":{"было":2,"стало":0,"остатокПроцент":100},
  "how":"строки и классы шаблоном по началу строки таблицы; очередь подсчётом строк (правило 23); ряд таблицы остатка — перечитыванием строки ## 43",
  "measuredAt":T},
 "pour32Note20261025":("имя и описание записаны по ответам upload_file / get_file / update_file этого часа; аудит цепочки: 41 объект с именем реестра, "
   "40 с пометкой «УСТАРЕЛО», 51 объект в папке 05")}
recs.append(new)
br=Counter(r.get("rights") for r in recs); bs=Counter(r.get("readState") for r in recs)
d["measuredAt"]=T
d["method"]=d["method"]+"; переснят кругом 45 шагом 3: добавлен тридцать второй слепок (%d B), тридцать первый переведён в registry-mirror-superseded / HOLD_superseded"%B
IP.write_text(json.dumps(d,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
CP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
c=json.loads(CP.read_text(encoding="utf-8"))
reg=c["fourPointMassRegistry20261023"]
reg["fileBytesAsOfRound45"]=B; reg["fileMd5AsOfRound45"]=M; reg["fileSha256AsOfRound45"]=S; reg["linesAsOfRound45"]=L
fs=reg["queueSweepRound45Finding20261025"]
fs["поправкаШага3"]={"что":("ряд таблицы остатка круга 44 «адреса очереди, закрытые тем, что уже лежит в лане» переснят этим же кругом: два адреса, "
  "посчитанные кругом 43 закрытыми, держались на общем слове в строке, а при строгом своде (имя + название + локатор + цитата) их не осталось — "
  "0 из 102, остаток шкалы 98.04 % → 100 %. В реестре ряд оставлен с обеими цифрами (2 → 0), чтобы было видно, что мера менялась; в корпусе "
  "шкала перевычислена"),
 "measuredAt":T,"how":"перечитывание строки таблицы в разделе ## 43 после свода ## 44"}
rwm=reg["remainingWorkMeasures20261025"]
rwm["шкалы"]["очередьЗакрытаИзЛана"]=0.0
rwm["округлённыеОстатки"]["очередьПоЛану"]=100
rwm["переснятКругом45Шаг3"]={"ряд":"очередьЗакрытаИзЛана","значения":{"закрыто":"2 → 0","остаток":"98.04 % → 100 %"},
 "почему":"два адреса круга 43 были полуготовностью по общему слову; строгий свод того же круга не оставил в них ни локатора, ни цитаты по требуемому изданию",
 "чтоНеИзменилось":"остальные шесть шкал, классы (A1 32 / A2 35 / B1 34 / B2 6 / C 102), очередь 102 и число висящих нужд 2",
 "measuredAt":T,"how":"обход реестра тем же определением, которым мерил круг 44 (round44Finding20261025), плюс свод ## 44"}
lrc=reg["laneReadmeConsistency20261023"]
lrc["note20261025r45step3"]=("README лана не тронут и шагом 3: переснят ряд таблицы остатка внутри реестра, а README держит классы и очередь — "
  "они стояли (A1 32, C 102, очередь 102, доля 15)")
g=c["integrityGate"]
dm=g["driveMirrors"]["massRegistry20261023"] if "driveMirrors" in g else c["driveMirrors"]["massRegistry20261023"]
dm["driveFileId"]=ID32; dm["bytes"]=B; dm["md5Local"]=M; dm["fileLines"]=L
dm["driveMd5Verified"]=M; dm["driveBytesVerified"]=B; dm["gitSha256AtUpload"]=S; dm["rows"]=209; dm["lagBehindGit"]=False
dm["contentRevisions"].append({"asOf":T,"bytes":B,"lines":L,"md5":M,"rows":209,
 "perClass":{"A1":32,"A2":35,"B1":34,"B2":6,"C":102},"queue":102,"dobytLines":2,"driveFileId":ID32,"uploadedAt":"2026-10-25T14:55:26.998Z",
 "measuredAt":T,"how":"upload_file → get_file этого часа; ответы записаны в pour32_20261025",
 "command":"python3 -B scripts/validate_atonement_corpus_integrity.py (правила 23, 25) плюс md5sum файла в дереве",
 "note":("шаг 3 того же круга: в разделе ## 43 переснят ряд таблицы остатка (очередь, закрытая ланом: 2 → 0 кандидата, 98.04 % → 100 %); байтов "
   "422 440 → 422 703; классы, очередь и число «Добыть:» не двигались")})
dm["liveObjectHistory"].append({"driveFileId":ID31,"bytes":B31,"md5":M31,"lines":L31,"uploadedAt":"2026-10-25T14:46:03.665Z",
 "status":"вытеснено шагом 3 круга 45 в 2026-10-25T14:55:39Z (имя + описание одного вызова, appProperties оставлены своими)",
 "why":"он зеркалит реестра шага 1; в дереве шага 3 лежит %d B, и живой объект в папке обязан быть ровно один"%B})
dm["pour32_20261025"]={"at":"2026-10-25T14:55:26.998Z","driveFileId":ID32,"bytes":B,"md5":M,"gitLines":L,"rows":209,"queue":102,"dobyt":2,
 "verification":("get_file вернул size %d и md5 %s — те же, что у файла в дереве; вытесненный %s помечен «круг 45 шаг 3» и сохранил свои числа "
   "(%d B, %s)")%(B,M,ID31,B31,M31),
 "countMove":("второй за вечер случай, когда слепок переливает не новый вывод, а поправку к старому: правило «слепок следует за байтами, а не за "
   "выводом» работает и в обратную сторону — правка одного числа в таблице обязана тянуть за собой объект в Drive"),
 "measuredAt":T,"how":"upload_file → get_file → update_file на вытесненном объекте → два поиска по имени и листинг папки",
 "mirrorChainNameAudit":{"объектовСИменемРеестра":41,"изНихСУСТАРЕЛО":40,"объектовВПапке":51}}
dm["mirrorChainNameAudit20261025r45step3"]={"объектовСИменемРеестра":41,"изНихСУСТАРЕЛО":40,"объектовВПапке":51,
 "команда":("search_files 'name contains 35_four_point_authors_mass_registry' в папке 13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ (41), search_files с обоими "
  "условиями имени разом (40), list_files по папке (51)"),
 "почему40":"живой слепок шага 3 — единственный без пометки; пометку получил и 31-й, залитый часом ранее тем же кругом",
 "наблюдение":("за девять минут круг залил, проверил, пометил и перелил объект заново: цепочка выдерживает вытеснение слепка его же кругом, "
  "и это единственная защита от того, чтобы поправка числа осталась не отзеркаленной"),
 "measuredAt":T,"how":"ответы двух поисков и листинга этого часа"}
dm["mirrorOfGitCommitNote20261025r45step3"]=("свойство mirror_of_git_commit дописано после коммита шага 3 у живого слепка (32-го); у 31-го оно "
 "осталось на дереве шага 1 — семантика не меняется: слепок называет то дерево, которым он залит")
q=c["acquisitionRequests20261024"]
q["round45Step3Note20261025"]={"что":("список заявок не изменён; шаг 3 уточняет его основание: шкала «очередь, закрытая ланом» переснята с 2 на 0, "
  "то есть доля очереди, снимаемой без внешнего доступа, равна нулю, а не двум процентам"),
 "зачем":"чтобы отказ от механических сводов не выглядел недоработкой: он опирается на ноль, полученный двумя определениями ключа и ручной проверкой",
 "measuredAt":T,"how":"обход 102 адресов по 122 файлам периметра (определения в queueSweepRound45Finding20261025) и перечитывание ряда таблицы ## 43"}
li=d["records"]  # noqa
li2=c["libraryIndex20261023"]
li2["records"]=len(recs); li2["files"]=sum(1 for r in recs if r.get("kind")=="file"); li2["folders"]=sum(1 for r in recs if r.get("kind")=="folder")
li2["byRights"]={k:v for k,v in br.items() if v}; li2["byReadState"]={k:v for k,v in bs.items() if v}
li2["driveBytesSum"]=sum(r.get("bytes",0) for r in recs if r.get("kind")=="file")
li2["largestBytes"]=max(r.get("bytes",0) for r in recs if r.get("kind")=="file")
li2["measuredAt"]=T; li2["checkedAt"]=T
li2["method"]=li2["method"]+"; переснято кругом 45 шагом 3: %d записей, %d файлов, тридцать первый слепок вытеснен и тридцать второй добавлен, сумма байт выросла на %d"%(li2["records"],li2["files"],B)
CP.write_text(json.dumps(c,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
print("корпус:",len(CP.read_bytes()),"индекс:",len(IP.read_bytes()))
print("счётчики:",li2["records"],li2["files"],li2["folders"],dict(br),dict(bs),li2["driveBytesSum"])
