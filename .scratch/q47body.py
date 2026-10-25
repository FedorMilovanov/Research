import json,pathlib,re,subprocess,sys
LIM=262144
ROOT=pathlib.Path("/home/user/Research")
CP=ROOT/"ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
IPth=ROOT/"ИСКУПЛЕНИЕ/data/atonement-library-index.json"
out=subprocess.run(["gh","api","repos/FedorMilovanov/Research/pulls/235","--jq",".body"],capture_output=True,text=True).stdout
assert out.endswith("\n"); b0=out[:-1]
MOLD="69a3f853be807e3de0954af401d53944"; MNEW="0e6769c315980b98033cce96061fde82"
sub=[
("реестр 448 516 B / 1 418 строк, md5 `%s`"%MOLD,"реестр 448 944 B / 1 418 строк, md5 `%s`"%MNEW),
("индекс библиотеки 241 507 B (113 записей, 104 файла, 9 папок, `driveBytesSum` 146 290 654, `registry_linked` 43, `HOLD_superseded` 51); корпус 734 181 B, число помеченных полей доведено до 316 и переснято тем же определением, которым считает проверка.",
 "индекс библиотеки @@INDEX@@ B (114 записей, 105 файла, 9 папок, `driveBytesSum` 146 739 598, `registry_linked` 44, `HOLD_superseded` 52); корпус @@CORPUS@@ B, число помеченных полей 316 → 319 — снято тем же определением, которым считает проверка, и снято дважды: второй раз после починки, о которой ниже."),
("Цепочка имён в папке: 43 объекта с именем реестра, 42 с пометкой «УСТАРЕЛО», 53 всего — живой ровно один. За семь кругов (41…47) папка выросла с 46 до 53 объектов.",
 "Цепочка имён в папке: 44 объекта с именем реестра, 43 с пометкой «УСТАРЕЛО», 54 всего — живой ровно один. За семь кругов (41…47) папка выросла с 46 до 54 объектов, и пометки отстают от имён ровно на один объект: это инвариант цепочки, а не совпадение двух чисел."),
("**Зеркало:** залит 34-й слепок `1cL8icKDA-Jwrs4xMYj4ICN3SBY4flCoo` (448 516 B, md5 совпал с деревом, `lagBehindGit=false`); 33-й переведён в `УСТАРЕЛО … заменён слепком 1cL8icKDA…` / `HOLD_superseded` с отсылкой к 34-му, его поля о строках обнулены, чтобы он не утверждал классы, которых в живом дереве нет.",
 "**Зеркало:** залит 34-й слепок `1cL8icKDA-Jwrs4xMYj4ICN3SBY4flCoo` (448 516 B, md5 совпал с деревом); через шестнадцать минут круг перелил самого себя — живым стал 35-й слепок `1jfEydgDot9ZgGZDjSwA-Ehcq0nK7drf2` (448 944 B), потому что починка числа сдвинула байты реестра, а живое зеркало обязано быть побайтовым. 34-й переведён в `УСТАРЕЛО (круг 47, починка) …` / `HOLD_superseded`: appProperties не тронуты (они описывают его содержимое и остаются правдой о коммите шага 4), поля о строках обнулены, чтобы запись не утверждала классов живого дерева; 33-й вытеснен тем же кругом раньше."),
("0 % отказов доступа при 64.71 % адресов без каталожной записи","0 % отказов доступа при 64.71 % адресов без каталожной записи (по нынешней очереди, после снятия двух адресов, — 66.00 %)"),
("дозуёмкость тела этого сообщения — 94.64 % занято, 5.36 % свободно (числа в последней строке)","дозуёмкость тела этого сообщения — @@OCC@@ % занято, @@FR@@ % свободно (числа в последней строке)"),
]
for a,bb in sub:
    assert b0.count(a)==1, "не нашёл: "+a[:70]
    b0=b0.replace(a,bb)
body=re.sub(r"\*\*Длина этого тела: [^\n]*\*\*","@@LEN@@",b0,flags=re.S)
assert body.count("@@LEN@@")==1
add=pathlib.Path("/tmp/add47b.md").read_text(encoding="utf-8")
tpl=body+add
def fmt_len(n,By,occ,fr):
    return ("**Длина этого тела: %d символов / %d байт — у канала %d байта, значит занято %.2f %% и свободно (%d − %d) байт = %.2f %%; "
    "эта строка называет собственную длину и обязана называть её верно (правило 15zk.5).**")%(n,By,LIM,occ,LIM,By,fr)
LENRE=re.compile(r"\*\*Длина этого тела: \d+ символов / \d+ байт — у канала 262144 байта, значит занято [\d.]+ % и свободно \(262144 − \d+\) байт = [\d.]+ %;[^\n]*\*\*")
PROCRE=re.compile(r"дозуёмкость тела этого сообщения — [\d.]+ % занято, [\d.]+ % свободно")
CORTPL=re.compile(r"Корпус после этой правки: \d+ байт, индекс библиотеки: \d+ байт")
CORIN=re.compile(r"индекс библиотеки \d+ B \(114 записей, 105 файла, 9 папок, `driveBytesSum` 146 739 598, `registry_linked` 44, `HOLD_superseded` 52\); корпус \d+ B,")
def fmt_len(n,By,occ,fr):
    return ("**Длина этого тела: %d символов / %d байт — у канала %d байта, значит занято %.2f %% и свободно (%d − %d) байт = %.2f %%; "
    "эта строка называет собственную длину и обязана называть её верно (правило 15zk.5).**")%(n,By,LIM,occ,LIM,By,fr)
def sizes():
    return len(CP.read_bytes()), len(IPth.read_bytes())
def apply_corpus_numbers(full):
    cp,ip=sizes()
    full=CORTPL.sub("Корпус после этой правки: %d байт, индекс библиотеки: %d байт"%(cp,ip),full,count=1)
    full=CORIN.sub("индекс библиотеки %d B (114 записей, 105 файла, 9 папок, `driveBytesSum` 146 739 598, `registry_linked` 44, "
                   "`HOLD_superseded` 52); корпус %d B,"%(ip,cp),full,count=1)
    return full
full=tpl.replace("@@CORPUS@@","0").replace("@@INDEX@@","0").replace("@@OCC@@","0").replace("@@FR@@","0")
full=full.replace("@@LEN@@",fmt_len(0,0,0.0,0.0))
full=apply_corpus_numbers(full)
hist=[]
for it in range(14):
    n=len(full); L=len(full.encode()); occ=L*100.0/LIM; fr=(LIM-L)*100.0/LIM
    new=LENRE.sub(fmt_len(n,L,occ,fr),full,count=1)
    new=PROCRE.sub("дозуёмкость тела этого сообщения — %.2f %% занято, %.2f %% свободно"%(occ,fr),new,count=1)
    c=json.loads(CP.read_text(encoding="utf-8"))
    p=c["driveMirrors"]["massRegistry20261023"]["pour35_20261025"]
    p["prBodyChars20261025r47"]=n; p["prBodyBytes20261025r47"]=L
    p["prBodyNote"]=("числа тела записаны из той же неподвижной точки, что и корпус: тело цитирует размер корпуса, а корпус — длину тела; "
      "цифры шестизначные в обе стороны, поэтому итерация, на которой обе длины совпали, не двигает ни байты корпуса, ни байты тела")
    CP.write_text(json.dumps(c,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
    new=apply_corpus_numbers(new)
    if new==full and len(hist)>=2 and hist[-1]==hist[-2]:
        break
    hist.append((L,n,len(CP.read_bytes())))
    full=new
else:
    sys.exit("совместная точка не найдена: "+str(hist))
cp,ip=sizes()
assert LENRE.search(full) and PROCRE.search(full) and CORTPL.search(full) and CORIN.search(full)
m=re.search(r"\*\*Длина этого тела: (\d+) символов / (\d+) байт",full)
assert int(m.group(1))==len(full) and int(m.group(2))==len(full.encode())
assert "корпус %d B"%cp in full and "индекс библиотеки %d B"%ip in full
assert cp==len(CP.read_bytes()) and "@@" not in full
mine=add+"".join(x[1] for x in sub)
assert not re.search(r"[\u3000-\u9fff\uff00-\uffef]",mine) and "заливкиProperties" not in mine
assert len(re.findall(r"[\u3000-\u9fff]",full))==4, "чужих CJK-цитат в теле должно остаться ровно четыре (поправка круга 46)"
assert len(full.encode())<=LIM, len(full.encode())
pathlib.Path("/tmp/body47f.md").write_text(full,encoding="utf-8")
pathlib.Path("/tmp/pr47f.json").write_text(json.dumps({"body":full},ensure_ascii=False),encoding="utf-8")
print("итераций:",it,"| тело:",len(full),"символов /",len(full.encode()),"байт = %.2f %%"%(len(full.encode())*100.0/LIM),
      "| свободно",LIM-len(full.encode()),"| корпус:",cp,"| индекс:",ip)
