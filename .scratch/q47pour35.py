import json,pathlib,hashlib,re
from collections import Counter
ROOT=pathlib.Path("/home/user/Research")
Rg=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
b=Rg.read_bytes(); B=len(b); M=hashlib.md5(b).hexdigest(); S=hashlib.sha256(b).hexdigest()
L=len(Rg.read_text(encoding="utf-8").rstrip("\n").split("\n"))
ID35="1jfEydgDot9ZgGZDjSwA-Ehcq0nK7drf2"; ID34="1cL8icKDA-Jwrs4xMYj4ICN3SBY4flCoo"
B34,M34,L34=448516,"69a3f853be807e3de0954af401d53944",1418
NAME="2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 47, починка: 209 строк, %d B, md5 %s).md"%(B,M)
assert (B,M)==(448944,"0e6769c315980b98033cce96061fde82"),(B,M)
NSHA=hashlib.sha256(NAME.encode("utf-8")).hexdigest()
T="2026-10-25T16:30:00Z"
# ---------- индекс ----------
IP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-library-index.json"
d=json.loads(IP.read_text(encoding="utf-8")); recs=d["records"]
r34=recs[-1]; assert r34["driveId"]==ID34
r34.update({"name":"УСТАРЕЛО (25.10.2026, круг 47, починка): 35_four_point_authors_mass_registry — заменён слепком "+ID35,
 "role":"registry-mirror-superseded","rights":"HOLD_superseded","lagBehindGit":True,"measuredAtGit":T,
 "aboutRows":[],"registryRowClasses":{},
 "supersededBy20261025r47":ID35,
 "retiredBy20261025r47":{"at":"2026-10-25T16:27:40.460Z","how":"update_file (имя + описание); состояние прочитано ответом того же вызова",
   "propsLeftAlone":True,
   "note":("свойства оставлены его собственными (registry_bytes=448516, registry_md5 69a3f853…, classes A1=34…C=100, queue=100, "
     "mirror_of_git_commit на том коммите, где реестр и был равен этим байтам) — это правда о нём, а не отставание; строки и классы "
     "в записи обнулены, чтобы она не описывала живое дерево; очередьLeft названной: адреса Q-22 и Q-164 открыты и в живом дереве")
     .replace("очередьLeft названной","очередь оставлена названной")},
 "note":("слепок круга 47, пролежавший живым шестнадцать минут: %d B, залит в 16:11:42.769Z, вытеснен в "
   "16:27:40.460Z слепком %s — первое за круги 41…47 вытеснение, причиной которому не новые данные, а исправление числа в уже "
   "записанном выводе (§46 приписывал 2.78 %% долю строк с цитатой, а это доля попаданий; строк с цитатой 12 из 36 = 33.33 %%). "
   "Починка добавила в реестр 428 байт, и правило «слепок следует за байтами» сработало без исключения для правок текста")%(B34,ID35)})
new={"folder":"05","driveId":ID35,"kind":"file","mime":"text/markdown","bytes":B,"name":NAME,
 "gitFile":"docs/research/atonement/35_four_point_authors_mass_registry.md",
 "role":"registry-mirror","rights":"mirror_of_git","readState":"registry_linked",
 "aboutRows":["FP-065","FP-067"],"citedBy":[],"queueRows":["Q-22","Q-164"],
 "registryRowClasses":{"FP-065":"A1","FP-067":"A1"},
 "locator":"FP-065: A18610, с. 405; FP-067: A66344, с. 17",
 "driveBytesClaimed":B,"driveMd5Claimed":M,"driveBytesVerified":B,"driveMd5Verified":M,
 "gitBytesAtUpload":B,"gitFileLinesAtUpload":L,"gitRowsAtUpload":209,"gitMd5AtUpload":M,"gitSha256AtUpload":S,
 "md5VerifiedFromDrive":True,"uploadedAt":"2026-10-25T16:27:27.239Z","measuredAt":T,"lagBehindGit":False,
 "chainNote":("тридцать шестой слепок подряд: … → 1Otzj3fe… (круг 46) → 1cL8icKDA… (круг 47, первые шестнадцать минут) → этот (%d B); "
  "без пометки «УСТАРЕЛО» ровно он один: поиск по имени реестра дал 44 объекта, из них 43 с пометкой, в папке 54")%B,
 "note":("живой слепок круга 47 после починки его же вывода: upload_file в 16:27:27.239Z (%d B), состояние прочитано get_file — те же "
  "байты и md5 %s; причина переливки — не новые данные, а исправленное число в §46; десять свойств будут дописаны после коммита")%(B,M),
 "registryCountsAsOfRound47":{"lines":L,"fileBytes":B,"registryRows":209,"queueAddresses":100,"dobytLines":2,
  "perClass":{"A1":34,"A2":35,"B1":34,"B2":6,"C":100},"shareA1Percent":16,"mirrorMd5":M,"sectionsH2":47,
  "текстыEEBO-TCP":{"опробованоИдентификаторов":37,"репозиториевНашлось":37,"прочитаноТранскрипций":4,"снятоАдресов":2,
    "поднятоСтрок":2,"отозваноПодтверждений":1,"адресовСКаталогомОсталось":34,"строкСЦитатойОсталось":10,"попаданийОсталось":0},
  "how":("строки и классы — шаблоном по началу строки таблицы и по первому класс-токену; очередь — подсчётом строк очереди (правило 23); "
   "тексты — curl по contents/<id>.xml репозитория textcreationpartnership/<id> с разбором по pb n="),"measuredAt":T}}
recs.append(new)
d["measuredAt"]=T
d["method"]=d["method"]+"; круг 47 вторично: добавлен 35-й слепок (%d B) и вытеснен 34-й — переливка из-за починки числа в §46, а не из-за новых данных"%B
IP.write_text(json.dumps(d,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
# ---------- корпус ----------
CP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
c=json.loads(CP.read_text(encoding="utf-8"))
fp=c["fourPointMassRegistry20261023"]
for k,v in (("fileBytesAsOfRound47Correction",B),("linesAsOfRound47Correction",L),("fileMd5AsOfRound47Correction",M),
            ("fileSha256AsOfRound47Correction",S)):
    fp[k]=v
fp["fileBytesNote20261025r47Correction"]=("круг 47 перелил свой же слепок, ничего не изменив в очередях и классах: в §46 число 2.78 %% было "
 "подписано не своей шкалой. Строк с цитатой на латыни или английском — 12 из 36 (33.33 %%), а механических попаданий — одно (2.78 %%). "
 "Правка держится внутри двух абзацев: байт 448516 → %d при тех же 1418 строках. Числа шага 4 круга 47 (448516, 69a3f853…) оставлены как снятые на "
 "шаге 4, а ключи Correction — текущие.")%B
blk=fp["primaryTextsReachableRound47Finding20261025"]
po=blk["переопределениеОчереди"]
po["изНихСЦитатойНаЛатиницеИлиАнглийском"]=12
po["доляСтрокСЦитатой"]=33.33
po["попаданийКавыВТекст"]=1
po["доляМеханическиИщущих"]=2.78
po["оговоркаПроШкалу"]=("число 2.78 % считает не строки с цитатой, а попадания: из 36 носителей с каталожной записью цитату (≥15 букв на латыни "
 "или английском) держат 12 — 33.33 %, а механически она отыскалась ровно в одном тексте; первая редакция этого поля приписывала 2.78 % долю "
 "строк с цитатой, и правка попала в тот же круг, что и запись")
blk["остатокПослеСнятияАдресов"]={"очередь":100,"сЗаписьюКаталога":34,"безЗаписиКаталога":66,"сЦитатой":10,"безЦитаты":24,
 "попаданийОсталось":0,
 "смысл":("после снятия Q-65 и Q-67 узкое место выглядит так: 66 адресов (66.00 %) вообще не имеют записи в этом каталоге — им нужен Evans, а не "
  "этот канал; 10 адресов (10.00 %) читаются и имеют цитату, то есть закрываемы следующим же приёмом; 24 (24.00 %) читаются, но строкy надо "
  "сначала переформулировать цитируемо")}
blk["остатокПослеСнятияАдресов"]["смысл"]=blk["остатокПослеСнятияАдресов"]["смысл"].replace("строкy","строку")
dm=c["driveMirrors"]["massRegistry20261023"]
for k,v in (("driveFileId",ID35),("bytes",B),("md5Local",M),("sha256Local",S),("gitSha256AtUpload",S),("fileLines",L),
            ("driveBytesVerified",B),("driveMd5Verified",M),("uploadedAt","2026-10-25T16:27:27.239Z"),("driveFileName",NAME),
            ("fileName",NAME),("driveFileNameSha256",NSHA),("supersededPreviousSnapshot",ID34),("lagBehindGit",False),("rows",209)):
    dm[k]=v
dm["verification"]=("get_file вернул size %d и md5 %s — те же, что у файла в дереве (проверено до отправки: git show HEAD:файл | md5sum); "
  "вытесненный %s помечен «круг 47, починка» и сохранил свои числа (%d B, md5 %s), lagBehindGit=true")%(B,M,ID34,B34,M34)
dm["how"]=("двадцать шестая переливка, и первая, для которой поводом стала не новая находка, а починка собственного вывода: число снято с файла, "
  "заливка побайтово из рабочего дерева, get_file, update_file на вытесненном, свойства на живом — после коммита")
dm["mirrorChainNameAudit20261025r47b"]={"объектовСИменемРеестра":44,"изНихСУСТАРЕЛО":43,"объектовВПапке":54,
 "команда":("search_files 'name contains 35_four_point_authors_mass_registry' в папке 13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ (44), search_files с "
  "обоими условиями имени (43), list_files по папке (54) — тот же набор, что в кругах 41…46"),
 "почему43":"живой слепок после починки — единственный без пометки; пометку получил и 34-й, залитый этим же кругом 16 минутами раньше",
 "наблюдение":("за семь кругов (41…47) папка выросла с 46 до 54 объектов, зеркалами реестра стали 44, и пометки отстают от имён ровно на один "
  "объект — на живой; отношение 43 к 44 есть инвариант цепочки, а не совпадение двух чисел")}
dm["contentRevisions"].append({"asOf":T,"bytes":B,"lines":L,"md5":M,"rows":209,
 "perClass":{"A1":34,"A2":35,"B1":34,"B2":6,"C":100},"queue":100,"dobytLines":2,"measuredAt":T,
 "how":"числа сняты с файла в дереве после починки §46, до переливки 35-го слепка",
 "note":"круг 47, починка: классы и очередь не двинулись, байт 448516 → %d при тех же 1418 строках"%B})
dm["liveObjectHistory"].append({"driveFileId":ID34,"bytes":B34,"md5":M34,"lines":L34,"uploadedAt":"2026-10-25T16:11:42.769Z",
 "status":"вытеснено в том же кругу в 2026-10-25T16:27:40.460Z (имя + описание одного вызова, appProperties оставлены своими)",
 "why":"после починки §46 в дереве лежит %d B, а живой объект в папке обязан быть ровно один и побайтово ему равен"%B})
dm["pour34_20261025"]["supersededWithinCircle20261025r47"]=("слепком %s в 16:27:40.460Z; запись сохранена как есть, потому что её числа — про её "
  "собственное содержимое, а mirror_of_git_commit 8e44a6b остаётся правдой: на том дереве реестр и был равен 448516 байтам")%ID35
dm["pour35_20261025"]={"at":"2026-10-25T16:27:27.239Z","driveFileId":ID35,"bytes":B,"md5":M,"gitLines":L,"rows":209,"queue":100,"dobyt":2,
 "measuredAt":T,"how":"upload_file → get_file → update_file на вытесненном → два поиска по имени и листинг папки → свойства после коммита",
 "reason":("в абзаце «Что это меняет в очереди» число 2.78 % было приписано не своей шкале: оно считает механические попадания кавы в текст "
  "(1 из 36), а строк с цитатой 12 (33.33 %). Реестр правится, зеркало переливается, вытесненное зеркало сохраняет прежние числа как свои — "
  "так ошибка становится видимой в обеих копиях, а не заметкой поверх"),
 "countMove":("классы и очередь не двинулись (A1 34, C 100, 100 адресов, доля 16 %%); двинулись только байты: 448516 → %d — первый за круги "
  "41…47 случай, когда переливка не несёт новых чисел")%B,
 "verification":("get_file вернул size %d и md5 %s; имя объекта содержит и байты, и md5 — они прочитаны из того же файла, а не из памяти о нём")%(B,M),
 "mirrorChainNameAudit20261025r47b":dm["mirrorChainNameAudit20261025r47b"],
 "prBodyChars20261025r47":0,"prBodyBytes20261025r47":0,
 "prBodyNote":"числа тела пишутся после финального патча и читаются обратно из API; подстановка равной длины не двигает ни тело, ни корпус"}
li=c["libraryIndex20261023"]
br=Counter(r.get("rights") for r in recs); bs=Counter(r.get("readState") for r in recs)
li["records"]=len(recs); li["files"]=sum(1 for r in recs if r.get("kind")=="file"); li["folders"]=sum(1 for r in recs if r.get("kind")=="folder")
li["byRights"]={k:v for k,v in br.items() if v}; li["byReadState"]={k:v for k,v in bs.items() if v}
files=[r for r in recs if r.get("kind")=="file"]
li["driveBytesSum"]=sum(r.get("bytes",0) for r in files)
li["largestBytes"]=max(r.get("bytes",0) for r in files)
li["measuredAt"]=T; li["checkedAt"]=T
li["method"]=li["method"]+("; круг 47, второй проход тем же обходом: %d записей, %d файлов, сумма байт %d"%(li["records"],li["files"],li["driveBytesSum"]))
li["countsNote"]=(li.get("countsNote","")+"; 34-й слепок вытеснен внутри круга 47 через 16 минут (починка числа в §46), 35-й добавлен; "
 "зеркалами реестра с пометкой «УСТАРЕЛО» стали 43 из 44 именованных объектов папки `05`").lstrip("; ")
CP.write_text(json.dumps(c,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
print("корпус:",len(CP.read_bytes()),"индекс:",len(IP.read_bytes()),"| реестр:",B,L,M[:8],"| сумма:",li["driveBytesSum"],"записей:",li["records"])
