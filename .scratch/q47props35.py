import json,pathlib
ROOT=pathlib.Path("/home/user/Research")
CP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-library-index.json"
c=json.loads(CP.read_text(encoding="utf-8"))
dm=c["driveMirrors"]["massRegistry20261023"]
p=dm["pour35_20261025"]
p["propsNote20261025r47"]=("десять свойств живого слепка (registry_bytes=448944, registry_rows=209, registry_md5, registry_classes="
 "A1=34,A2=35,B1=34,B2=6,C=100, registry_queue=100, registry_role, source, read_state, rights и mirror_of_git_commit) дописаны одним вызовом "
 "update_file с app_properties в виде JSON-строки в 2026-10-25T16:37:04.263Z и прочитаны обратно тем же ответом; имя коммита — шаг 7 этого круга, "
 "на его дереве реестр равен 448944 байтам (проверено git show HEAD:файл | md5sum до отправки свойств); у 34-го свойства не переписывались, "
 "и его поле про коммит тоже остаётся правдой — оно указывает на шаг 4, где реестр был равен 448516 байтам")
dm["mirrorOfGitCommitNote20261025r47"]=("свойство mirror_of_git_commit записано коротким именем и только в свойства объекта — в корпус оно не "
 "переносится (правило 20 читает семи- и восьмизначный шестнадцатеричный токен как ссылку на объект git и требует живого git show, а шаг круга "
 "ещё не влит в main); способ прочесть: get_file fields=appProperties по id зеркала")
d=json.loads(IP.read_text(encoding="utf-8"))
r=d["records"][-1]
assert r["driveId"]=="1jfEydgDot9ZgGZDjSwA-Ehcq0nK7drf2"
r["note"]=r["note"]+("; десять свойств (включая mirror_of_git_commit на коммит шага 7) дописаны и прочитаны обратно в 2026-10-25T16:37:04.263Z")
CP.write_text(json.dumps(c,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
IP.write_text(json.dumps(d,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
cp=len(CP.read_bytes()); ip=len(IP.read_bytes())
print("корпус:",cp,"индекс:",ip)
