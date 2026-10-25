import json,pathlib,re,sys
LIM=262144
b0=pathlib.Path("/tmp/body47_old.md").read_text(encoding="utf-8")
assert b0.endswith("\n"); b0=b0[:-1]
old=json.loads(pathlib.Path("/tmp/pr47.json").read_text(encoding="utf-8"))["body"]
add=old[len(b0):]                      # аддендум круга 47 из прошлой попытки, с устаревшими числами
add=re.sub(r"\*\*Длина этого тела: [^\n]*\*\*","@@LEN@@",add)
add=re.sub(r"дозуёмкость тела этого сообщения — [^\n]*?\(числа в последней строке\)",
           "дозуёмкость тела этого сообщения — @@PROC@@ (числа в последней строке)",add)
assert add.count("@@LEN@@")==1 and add.count("@@PROC@@")==1, (add.count("@@LEN@@"),add.count("@@PROC@@"))

def fmt_len(n,L,occ,fr):
    return ("**Длина этого тела: %d символов / %d байт — у канала %d байта, значит занято %.2f %% и свободно (%d − %d) "
            "байт = %.2f %%; эта строка называет собственную длину и обязана называть её верно (правило 15zk.5).**")%(n,L,LIM,occ,LIM,L,fr)

def build(line,proc):
    a=add.replace("@@LEN@@",line).replace("@@PROC@@",proc)
    body=b0+a
    L=len(body.encode()); n=len(body)
    occ=L*100.0/LIM; fr=(LIM-L)*100.0/LIM
    return body,a,L,n,occ,fr

line,proc="0"*60,"0"*30
for it in range(30):
    body,a,L,n,occ,fr=build(line,proc)
    nl=fmt_len(n,L,occ,fr); np="%.2f %% занято, %.2f %% свободно"%(occ,fr)
    if nl==line and np==proc:
        break
    line,proc=nl,np
else:
    sys.exit("неподвижная точка не найдена")
body,a,L,n,occ,fr=build(line,proc)
m=re.search(r"Длина этого тела: (\d+) символов / (\d+) байт — у канала %d байта, значит занято ([\d.]+) %% и свободно \(%d − (\d+)\) байт = ([\d.]+) %%"%(LIM,LIM),a)
assert m, a[-600:]
assert int(m.group(1))==n and int(m.group(2))==L and int(m.group(4))==L, m.groups()
assert abs(float(m.group(3))-round(occ,2))<1e-9 and abs(float(m.group(5))-round(fr,2))<1e-9
assert "%.2f %% занято"%occ in a and "%.2f %% свободно"%fr in a
assert L<=LIM, L
assert "залив" not in a and not re.search(r"[\u4e00-\u9fff]",a), "смешанными символами/иероглифами"
pathlib.Path("/tmp/body47.md").write_text(body,encoding="utf-8")
pathlib.Path("/tmp/pr47.json").write_text(json.dumps({"body":body},ensure_ascii=False),encoding="utf-8")
print("символов:",n,"| байт:",L,"=",("%.2f %% занято, %.2f %% свободно"%(occ,fr)),"| строк в аддендуме:",len(a.split("\n")))
print(a.rstrip().split("\n")[-1])
