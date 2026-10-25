import json,pathlib
CP=pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
IP=pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-library-index.json")
c=json.loads(CP.read_text(encoding="utf-8"))
dm=c["driveMirrors"]["massRegistry20261023"]
dm["mirrorOfGitCommitNote20261025r47"]=("свойство mirror_of_git_commit дописано после коммита круга 47 у живого слепка (34-го) вместе с девятью "
 "другими свойствами (registry_bytes=448516, registry_rows=209, registry_md5, registry_classes=A1=34,A2=35,B1=34,B2=6,C=100, registry_queue=100, "
 "registry_role, source, read_state, rights); десять свойств прочитаны обратно fields=appProperties того же вызова в 2026-10-25T16:19:11.825Z, и тот "
 "же ответ подтвердил size 448516 и md5 69a3f853be807e3de0954af401d53944 — то есть дерево коммита, на который указывает свойство, побайтово равно "
 "зеркалу (git show HEAD:файл | md5sum совпал до отправки свойств). Короткое имя коммита в корпус не переносится по той же причине, что и в кругу 46 "
 "(правило 20 требует достижимости из main, а шаг круга ещё не влит); способ прочесть: get_file fields=appProperties по id зеркала")
p=dm["pour34_20261025"]
p["propsNote20261025r47"]=("свойства дописаны одним вызовом update_file с app_properties в виде JSON-строки; у вытесненного 33-го свойства не "
 "переписывались — они описывают его собственное содержимое (круг 46), и расхождение между его реестром свойств и живым деревом есть состояние "
 "вытесненности, а не ошибка зеркала")
p["verification"]=p["verification"]+"; в 2026-10-25T16:19:11.825Z к слепку дописаны десять свойств, включая mirror_of_git_commit, и прочитаны обратно"
d=json.loads(IP.read_text(encoding="utf-8"))
r=d["records"][-1]
assert r["driveId"]=="1cL8icKDA-Jwrs4xMYj4ICN3SBY4flCoo"
r["note"]=r["note"]+("; десять свойств объекта (включая mirror_of_git_commit на коммит круга 47) дописаны и прочитаны обратно в 2026-10-25T16:19:11.825Z")
CP.write_text(json.dumps(c,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
IP.write_text(json.dumps(d,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
print("корпус:",len(CP.read_bytes()),"индекс:",len(IP.read_bytes()))
