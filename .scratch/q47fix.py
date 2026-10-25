import pathlib,re,sys,hashlib
f=pathlib.Path("/home/user/Research/docs/research/atonement/35_four_point_authors_mass_registry.md")
t=f.read_text(encoding="utf-8")
# 1) исправление ложного числа в §46: 2.78 % — доля попаданий, а не доля строк с цитатой
old=("Из этих 36 строк **одна** держит цитату на латинице или английском, по которой место можно искать механически (2.78 %): "
     "о остальных носителях реестр пишет по-русски, и поиску не за что зацепиться.")
assert t.count(old)==1, t.count(old)
new=("Из этих 36 строк **12** держат цитату на латыни или английском, по которой место можно искать механически (33.33 %), а "
     "**попаданием** кончилась одна (2.78 %); об остальных 24 реестр пишет по-русски, и поиску не за что зацепиться. "
     "Первая формулировка этого абзаца приписывала числу 2.78 % не его шкалу (оно считает попадания, а не строки с цитатой) — "
     "починено в том же круге, до переливки зеркала, и переливка из-за починки есть: 35-й слепок.")
t=t.replace(old,new)
t=t.replace("1 418(числа сняты после дописки этого предложения и сходятся итерацией)","1 418 (числа сняты после дописки этого предложения и сходятся итерацией)",1)
assert "1 418 (числа сняты" in t or "(числа сняты" not in t
# 2) неподвижная точка в балансовой строке: байты и строки файла после правки
sep=re.search(r"байт в реестре 432 576 → 448(.)516, строк файла 1399 → 1(.)418",t)
assert sep, "нет якоря баланса"
s=sep.group(1); assert sep.group(2)==s
pat=re.compile(r"байт в реестре 432 576 → 448%s516, строк файла 1399 → 1%s418"%(s,s))
def fmt(n,sep):
    a=str(n); return a[:-3]+sep+a[-3:] if len(a)>3 else a
B=None
for it in range(12):
    b0=len(t.encode()); L=len(t.split("\n"))-(1 if t.endswith("\n") else 0)
    # длина строки не зависит от записываемых чисел (цифры те же по количеству), но проверяем итерацией
    cand=pat.sub("байт в реестре 432 576 → %s, строк файла 1399 → %s"%(fmt(b0,s),fmt(L,s)),t,count=1)
    if cand==t:
        break
    t=cand
else:
    sys.exit("баланс не сошёлся")
b=len(t.encode()); L=len(t.split("\n"))-(1 if t.endswith("\n") else 0)
sub="→ %s,"%fmt(b,s)
assert sub in t and re.search(r"строк файла 1399 → %s[ ]?\("%re.escape(fmt(L,s)),t), (b,L)
assert "条件的" in t
f.write_text(t,encoding="utf-8")
m=hashlib.md5(f.read_bytes()).hexdigest(); sh=hashlib.sha256(f.read_bytes()).hexdigest()
print("байт:",b,"строк(gate):",L,"md5:",m,"sha256:",sh[:12])
print("баланс:",pat.search(t).group(0)[:160])
