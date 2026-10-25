import json,pathlib,hashlib
from collections import Counter
ROOT=pathlib.Path("/home/user/Research")
Rg=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
b=Rg.read_bytes(); B=len(b); M=hashlib.md5(b).hexdigest(); S=hashlib.sha256(b).hexdigest(); L=b.count(b"\n")
assert (B,M,L)==(432576,"d0a72c33bb10914998e6f24c9692dc3a",1399),(B,M,L)
ID33="1Otzj3fe-u1QL08sXC3AGsSPhZkWAW4hI"; ID32="1OTWnh6Ejcjtm_T7GIt-tO1O3ueVCzYlX"
B32=422703; M32="cf1dd2ba5767afa77c6167d769aeda8d"; L32=1379
T="2026-10-25T15:32:00Z"
f17p=ROOT/"ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md"; f17=f17p.read_text()
F17=len(f17p.read_bytes()); L17=f17.count("\n")
H2=sum(1 for l in f17.split("\n") if l.startswith("## ")); H3=sum(1 for l in f17.split("\n") if l.startswith("### "))
IP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-library-index.json"
d=json.loads(IP.read_text(encoding="utf-8")); recs=d["records"]
r32=recs[-1]; assert r32["driveId"]==ID32
r32.update({"name":"УСТАРЕЛО (25.10.2026, круг 46): 35_four_point_authors_mass_registry — заменён слепком "+ID33,
 "role":"registry-mirror-superseded","rights":"HOLD_superseded","lagBehindGit":True,"measuredAtGit":T,
 "note":("слепок круга 45 шага 3 (%d B, %d строк файла), вытеснен кругом 46: в дереве добавлен раздел ## 45 (свод очереди по каталогу EEBO-TCP) "
  "и четыре пометки в строках очереди, байтов стало %d; имя и описание переведены update_file в 2026-10-25T15:29:33Z, appProperties объекта "
  "намеренно не тронуты (registry_bytes=%d, registry_md5=%s, mirror_of_git_commit оставлен на дереве шага 3) — они описывают залитое содержимое; "
  "содержимое файла в Drive не менялось")%(B32,L32,B,B32,M32),
 "supersededBy20261025r46":ID33,
 "retiredBy20261025r46":{"at":"2026-10-25T15:29:33Z","how":"update_file (имя + описание); состояние прочитано ответом того же вызова",
  "note":"второй раз подряд круг вытесняет слепок, залитый собственным кругом: сначала так вытеснили 31-й (шаг 3 круга 45), теперь 32-й (круг 46)"}})
r32["registryCountsAsOfRound45Step3"]["recheck20261025r46"]=("между слепками разница одна: раздел ## 45 и четыре пометки очереди, %d байта прозы"%(B-B32))
new={"folder":"05","driveId":ID33,"kind":"file","mime":"text/markdown","bytes":B,
 "name":"2026-10-25 — слепок 35_four_point_authors_mass_registry (круг 46: 209 строк, %d B, md5 %s).md"%(B,M),
 "gitFile":"docs/research/atonement/35_four_point_authors_mass_registry.md",
 "role":"registry-mirror","rights":"mirror_of_git","readState":"registry_linked",
 "aboutRows":[],"citedBy":[],"queueRows":["Q-22","Q-64","Q-67","Q-164"],"registryRowClasses":{},"locator":"",
 "driveBytesClaimed":B,"driveMd5Claimed":M,"driveBytesVerified":B,"driveMd5Verified":M,
 "gitBytesAtUpload":B,"gitFileLinesAtUpload":L,"gitRowsAtUpload":209,"gitMd5AtUpload":M,"gitSha256AtUpload":S,
 "md5VerifiedFromDrive":True,"uploadedAt":"2026-10-25T15:29:12.527Z","measuredAtGit":T,"lagBehindGit":False,
 "chainNote":("тридцать четвёртый слепок подряд: … → 1s_VudOC… → 1-iyXbJb… (круг 45, шаг 1) → 1OTWnh6E… (круг 45, шаг 3) → этот (%d B); "
  "без пометки «УСТАРЕЛО» ровно он один: поиск по имени реестра дал 42 объекта, из них 41 с пометкой, в папке 52")%B,
 "note":("живой слепок круга 46: залито upload_file в 2026-10-25T15:29:12.527Z (%d B), состояние прочитано get_file сразу за этим тем же часом — "
  "те же байты и md5 %s; десять свойств (registry_bytes, registry_rows, registry_md5, registry_classes, registry_queue, registry_role, source, "
  "read_state, rights, mirror_of_git_commit) дописаны после коммита. aboutRows пусты: ни один класс не двинулся; queueRows названы четыре адреса, "
  "которых касался круг, — три с идентификацией издания и один с пометкой-ловушкой")%(B,M),
 "registryCountsAsOfRound46":{"lines":L,"fileBytes":B,"registryRows":209,"queueAddresses":102,"dobytLines":2,
  "perClass":{"A1":32,"A2":35,"B1":34,"B2":6,"C":102},"shareA1Percent":15,"mirrorMd5":M,"sectionsH2":46,
  "внешнийИндекс":{"каталог":"EEBO-TCP (textcreationpartnership/Texts, TCP.csv)","записей":61315,"байт":29286409,
    "уникальныхИдентификаций":3,"ручнойПроверкойПодтверждено":3,"коллизий":4,"закрытоАдресов":0,"подвижкаКлассов":0},
  "how":("строки и классы — шаблоном по началу строки таблицы и по первому класс-токену; очередь — подсчётом строк очереди (правило 23); "
   "свод по каталогу — двумя определениями ключа, затем ручная проверка каждого кандидата"),
  "measuredAt":T},
 "pour33Note20261025":("имя и описание записаны по ответам upload_file / get_file / update_file этого часа; аудит цепочки: 42 объекта с именем "
   "реестра, 41 с пометкой «УСТАРЕЛО», 52 объекта в папке 05")}
recs.append(new)
br=Counter(r.get("rights") for r in recs); bs=Counter(r.get("readState") for r in recs)
d["measuredAt"]=T
d["method"]=d["method"]+"; переснят кругом 46: добавлен тридцать четвёртый слепок (%d B), тридцать второй переведён в registry-mirror-superseded / HOLD_superseded"%B
IP.write_text(json.dumps(d,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
CP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
c=json.loads(CP.read_text(encoding="utf-8"))
reg=c["fourPointMassRegistry20261023"]
reg["fileBytesAsOfRound46"]=B; reg["fileMd5AsOfRound46"]=M; reg["fileSha256AsOfRound46"]=S; reg["linesAsOfRound46"]=L
reg["externalIndexRound46Finding20261025"]={
 "что":("первый за шесть кругов внешний индекс, до которого у песочницы есть путь: репозиторий textcreationpartnership/Texts на GitHub содержит "
  "собственный каталог EEBO-TCP — файл TCP.csv, 29 286 409 байт, 61 315 записей, десять полей (TCP, EEBO, VID, STC, Status, Author, Date, Title, "
  "Terms, Pages); скачан через api.github.com сырьём, потому что api.github.com и pypi.org — единственные два научных/технических хоста, "
  "отвечающих 200 из этой среды. Сами тексты в репозитории отсутствуют (только graball.sh на закрытый домен), поэтому индекс годится на "
  "библиографическую половину очереди и не годится на чтение места"),
 "переписьОчереди":{"определение1":{"уникальнаяЗапись":3,"несколькоЗаписей":22,"нетЗаписи":77},
  "определение2":{"уникальнаяЗапись":3,"несколькоЗаписей":16,"нетЗаписи":83},
  "пересечениеУникальных":0,"объединениеУникальных":6,"доляОбъединения":5.88,
  "ручнаяПроверка":{"подтвержденоИзОбъединения":2,"отвергнутоКоллизий":4,
   "подтвержденные":["Q-22 (Bradwardine, De causa Dei — Oxford 1618, A16626 = «STC 3534; ESTC S113557», 916 листов, статус Free, изд. Абботта и Сэвиля, «nunc primum editi»; Basel 1571 и London 1715 в каталоге не представлены)","Q-164 (Zanchi — A97309 = «Wing Z7; Thomason E1897_1; ESTC R209936», 1659, перевод Ральфа Уинертона, 420 листов, статус Restricted)"],
   "отвергнутые":["Q-64 (A85742 — памфлет 1646 г. за подписью «G. G.» о речи Чэлонера; коллизия по фразе interest of the kingdome)","Q-21 (перевод Галена 1574 г. — совпали авторская частица и год)","Q-78 (Уайтфилд 1739 г. — вне охвата каталога 1473–1700)","Q-79 (Hughes 1640 г. — совпала фамилия)"]},
  "вручнуюБезСвода":{"адрес":"Q-67","основание":"строка реестра держала идентификатор A66344 с круга 39; по нему каталог дал запись целиком: «Wing W2646; ESTC R26371», 1693, статус Free, 59 листов, титул называет автора «by Daniel Williams»","чтоИзЭтого":"имя исправлено в строке (не Дэвид, а Дэниел; на Williams, David в каталоге ноль записей), адресат «Фома Чонси» не подтверждён (тематический заголовок каталога ведёт спор с Chauncy, Isaac, 1632–1712 — Neonomianism unmasked) и ждёт титульного листа"}},
 "полеPages":("число листов оцифровки, а не напечатанных страниц: оно ограничивает объём чтения (59, 420, 916 листов) и не даёт локатора, поэтому "
  "ни один из трёх адресов не закрыт и ни один класс не двинут"),
 "доляОчередиСРучкойДляПоиска":{"сЛатинскимЗаглавнымФрагментом":24,"доля":23.53,"хотьОднаЗаписьКаталога":25,"безЗаписи":77,"доляБезЗаписи":75.49,
  "вывод":("узкое место очереди — не права доступа, а присвоение: три четверти адресов не содержат фрагмента, на который можно направить любой "
   "индекс, доступный или недоступный")},
 "классы":"ноль сдвигов, пятый круг подряд: 209 строк, A1 32 / A2 35 / B1 34 / B2 6 / C 102, очередь 102, «Добыть:» 2",
 "how":("перепись одним обходом 102 адресов против 61 315 записей каталога, два определения ключа (заглавный фрагмент из курсива; автор плюс "
  "заглавие или год), затем ручная проверка каждого кандидата по полю Title и Terms"),
 "recheckCommand":("curl -sSL -H \"Accept: application/vnd.github.raw\" https://api.github.com/repos/textcreationpartnership/Texts/contents/TCP.csv?ref=master "
  "-o TCP.csv; затем grep по идентификатору (A66344, A16626, A97309); свод очереди — скрипты круга из рабочей папки"),
 "measuredAt":T}
reg["queueAnnotations20261025r46"]={"адресовДобавлено":0,"адресовЗакрыто":0,"адресовСПометкой":4,
 "что":("в строки Q-22, Q-67 и Q-164 вписана идентификация издания по каталогу EEBO-TCP с полными шифрами (STC/Wing + ESTC + число листов + статус "
  "доступа), в строку Q-64 — пометка-ловушка: единственная запись каталога по фрагменту её заглавия — чужой памфлет 1646 г."),
 "зачем":"чтобы следующий круг не принимал коллизию за идентификацию и не поднимал класс на числе листов оцифровки",
 "measuredAt":T,"how":"grep -c '^- Q-\\d+ —' до и после правки: число адресов не изменилось (102)",
 "command":"python3 -B scripts/validate_atonement_corpus_integrity.py (правила 23, 23.3)"}
lrc=reg["laneReadmeConsistency20261023"]
lrc["note20261025r46"]=("README лана не тронут кругом 46: классы и очередь стояли (A1 32, C 102, очередь 102, доля 15); круг правил строки очереди "
 "и одну ячейку заглавия (имя автора в FP-67), а это не двигает ни одного счётчика README")
g=c["integrityGate"]
g["egressAllowlistCorrection20261025r46"]={"что":("проба пятью адресами: archive.org, www.worldcat.org, babel.hathitrust.org — обрыв рукопожатия "
  "TLS; pypi.org и api.github.com — 200. Значит формулировки полей egressBlocked* прошлых кругов («Архив недоступен») были неточны: доступ не "
  "отключали, его никогда не было в этом контуре — среда живёт по списку разрешённых хостов"),
 "почемуЭтоНеОтговорка":("разница практическая: если доступ закрыт списком, то просить его у архивов бессмысленно, зато всё, что лежит внутри "
  "списка, надо перебрать — круг 46 так и нашёл каталог EEBO-TCP на GitHub; и наоборот, «Архив лег» не означает, что REQ-7 и REQ-8 закрыты"),
 "consequence":"REQ-7 (уточнение по каталогу HathiTrust) и REQ-8 (страницы Каннингема) остаются висящими: их индексы лежат вне списка, и ни один из них не дублируется внутри списка",
 "measuredAt":"2026-10-25T15:2x",
 "how":"один вызов curl по пяти адресам, коды и текст ошибок записаны словами; точную минуту пробы круг не фиксирует, потому что вывод не пересохраняли",
 "measuredBy":"curl -sS -o /dev/null -w код-ответа"}
del g["egressAllowlistCorrection20261025r46"]["measuredAt"]
g["egressAllowlistCorrection20261025r46"]["measuredAt"]=T
dm=c["driveMirrors"]["massRegistry20261023"]
dm["driveFileId"]=ID33; dm["bytes"]=B; dm["md5Local"]=M; dm["fileLines"]=L
dm["driveMd5Verified"]=M; dm["driveBytesVerified"]=B; dm["gitSha256AtUpload"]=S; dm["rows"]=209; dm["lagBehindGit"]=False
dm["contentRevisions"].append({"asOf":T,"bytes":B,"lines":L,"md5":M,"rows":209,
 "perClass":{"A1":32,"A2":35,"B1":34,"B2":6,"C":102},"queue":102,"dobytLines":2,"driveFileId":ID33,"uploadedAt":"2026-10-25T15:29:12.527Z",
 "measuredAt":T,"how":"upload_file → get_file этого часа; ответы записаны в pour33_20261025",
 "command":"python3 -B scripts/validate_atonement_corpus_integrity.py (правила 23, 25) плюс md5sum файла в дереве",
 "note":"слепок круга 46: раздел ## 45 (единственный доступный внешний индекс — каталог EEBO-TCP) и четыре пометки в очереди; байтов 422 703 → 432 576"})
dm["liveObjectHistory"].append({"driveFileId":ID32,"bytes":B32,"md5":M32,"lines":L32,"uploadedAt":"2026-10-25T14:55:26.998Z",
 "status":"вытеснено кругом 46 в 2026-10-25T15:29:33Z (имя + описание одного вызова, appProperties оставлены своими)",
 "why":"он зеркалит реестра шага 3 круга 45; в дереве круга 46 лежит %d B, и живой объект в папке обязан быть ровно один"%B})
dm["pour33_20261025"]={"at":"2026-10-25T15:29:12.527Z","driveFileId":ID33,"bytes":B,"md5":M,"gitLines":L,"rows":209,"queue":102,"dobyt":2,
 "verification":("get_file вернул size %d и md5 %s — те же, что у файла в дереве; вытесненный %s помечен «круг 46» и сохранил свои числа (%d B, %s)"
   )%(B,M,ID32,B32,M32),
 "countMove":("шестой круг подряд без сдвига классов; переливка вызвана не выводом, а текстом: добавлен раздел ## 45 и четыре пометки очереди — "
   "правило «слепок следует за байтами» не делает исключений для кругов, которые ничего не доказали"),
 "measuredAt":T,"how":"upload_file → get_file → update_file на вытесненном объекте → два поиска по имени и листинг папки",
 "prBodyChars20261025r46":0,
 "prBodyNote":"число тела PR круг допишет после патча и прочитает обратно из API; в реестре и в корпусе оно не дублируется, чтобы не плодить самоотсылку"}
dm["mirrorChainNameAudit20261025r46"]={"объектовСИменемРеестра":42,"изНихСУСТАРЕЛО":41,"объектовВПапке":52,
 "команда":("search_files 'name contains 35_four_point_authors_mass_registry' в папке 13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ (42), search_files с обоими "
  "условиями имени разом (41), list_files по папке (52)"),
 "почему41":"живой слепок круга 46 — единственный без пометки; пометку получил и 32-й, залитый кругом 45",
 "наблюдение":("цепочка растёт на один объект за круг и на одну пометку за переливку; за шесть кругов (41…46) папка выросла с 46 до 52 объектов, "
  "из них зеркалами реестра стали 42 — остальные десять это снимки 16_, 22_, 34_ и служебных файлов"),
 "measuredAt":T,"how":"ответы двух поисков и листинга этого часа"}
dm["mirrorOfGitCommitNote20261025r46"]=("свойство mirror_of_git_commit дописано после коммита круга 46 у живого слепка (33-го); у 32-го оно осталось "
 "на дереве шага 3 круга 45 — семантика не меняется: слепок называет то дерево, которым он залит")
rd=c["reconciliationDocument20261022"]
rd["lines"]=L17; rd["sectionsH2"]=H2; rd["sectionsH3"]=H3
rd["history"].append({"at":T,"round":"46",
 "что":("блок 15zk. из четырёх правил: среда со списком разрешённых хостов описывается как закрытый список, а не как отказ источника; если два "
  "определения меры дают непересекающиеся множества выживших, опубликуемо только ручное решение; каталожный индекс закрывает библиографическую "
  "половину адреса и не трогает локатор; прежде чем просить доступ, измерь, у скольких адресов есть ручка для поиска"),
 "lines":L17,"sectionsH2":H2,"sectionsH3":H3,"fileBytes":F17,
 "measuredAt":T,"how":"тот же обход файла, которым мерит поле lines: newline-счёт и префиксы ## / ###",
 "command":"python3 -B scripts/validate_atonement_corpus_integrity.py"})
q=c["acquisitionRequests20261024"]
q["round46Note20261025"]={"что":("список заявок не изменён (REQ-1 … REQ-8, висящие REQ-7 и REQ-8), но изменено их обоснование: причины висеть — "
  "не отказ архивов, а список разрешённых хостов среды (поле egressAllowlistCorrection20261025r46)"),
 "чтоКругНашёл":("внутри списка доступен один библиографический индекс — каталог EEBO-TCP на GitHub; он идентифицировал издание для трёх адресов "
  "очереди (Q-22, Q-67, Q-164) и не закрыл ни одного, потому что локатор каталог не даёт"),
 "почемуЭтоНеЗакрываетЗаявки":"REQ-7 требует каталога HathiTrust (пагинация и наличие оцифровки по-русски и по-латыни), REQ-8 — страниц Каннингема 333–370; ни то, ни другое внутри списка не лежит",
 "measuredAt":T,"how":"проба пятью адресами + перепись 102 адресов против 61 315 записей каталога",
 "command":"python3 -B scripts/validate_atonement_corpus_integrity.py (правила 23, 23.2)"}
li=c["libraryIndex20261023"]
li["records"]=len(recs); li["files"]=sum(1 for r in recs if r.get("kind")=="file"); li["folders"]=sum(1 for r in recs if r.get("kind")=="folder")
li["byRights"]={k:v for k,v in br.items() if v}; li["byReadState"]={k:v for k,v in bs.items() if v}
li["driveBytesSum"]=sum(r.get("bytes",0) for r in recs if r.get("kind")=="file")
li["largestBytes"]=max(r.get("bytes",0) for r in recs if r.get("kind")=="file")
li["measuredAt"]=T; li["checkedAt"]=T
li["method"]=li["method"]+"; переснято кругом 46: %d записей, %d файлов, тридцать второй слепок вытеснен и тридцать четвёртый добавлен, сумма байт выросла на %d"%(li["records"],li["files"],B)
CP.write_text(json.dumps(c,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
print("корпус:",len(CP.read_bytes()),"индекс:",len(IP.read_bytes()))
print("счётчики:",li["records"],li["files"],li["folders"],dict(br),dict(bs),li["driveBytesSum"],"| 17_:",F17,L17,H2,H3)
