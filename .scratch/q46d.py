import re,pathlib,collections,json
ROOT=pathlib.Path("/home/user/Research")
REGNAME="35_four_point_authors_mass_registry.md"
t=(ROOT/"docs/research/atonement"/REGNAME).read_text()
q2row={}; tab={}; rowQ={}
for l in t.split("\n"):
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
    m=re.match(r"^\| (FP-0*(\d+)) \|(.*)\|\s*$",l)
    if m:
        cells=[x.strip() for x in m.group(3).split("|")]; tab["FP-%02d"%int(m.group(2))]=cells
addr_row={}
for rid,cells in tab.items():
    for x in re.findall(r"Q-(\d+)"," ".join(cells)):
        q="Q-%02d"%int(x)
        if q in q2row and q not in addr_row: addr_row[q]=rid
# --- 1. воспроизвести 108 снимков круга 44
SNAP=re.compile(r"`([a-z][a-z0-9]{6,20}\d{2}[a-z]{2,12})`")
DIG=re.compile(r"`([a-z][a-z0-9_\-]{6,}\d[a-z0-9_\-]{0,20})`")
ARCH=re.compile(r"archive\.org|ia\d{3,4}|_djvu\.txt",re.I)
perim=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REGNAME]+[p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
s1=set(); s2=set()
for p in perim:
    x=p.read_text(); s1|=set(SNAP.findall(x))
    for m in DIG.finditer(x):
        if ARCH.search(x[max(0,m.start()-200):m.end()+200]) and not m.group(1).endswith((".md",".json",".txt",".py")): s2.add(m.group(1))
print("периметр:",len(perim),"| строгие:",len(s1),"| цифра+контекст:",len(s2),"| объединение:",len(s1|s2))
# --- 2. типы объектов очереди
WEB=re.compile(r"http|\.com|\.org|\.io|\?p=|\?page_id=|сайт|страниц[аы] сайта|index\.php|PDF",re.I)
OLD=re.compile(r"\b(1[4-8]\d{2})\b|\b190[0-5]\b|PL \d|Migne|mign|Patrolog|EEBO|TCP|Acta|Синод|доксолог|confessio|Opera",re.I)
MOD=re.compile(r"\b(19\d{2}|20[0-2]\d)\b|Crossway|Baker|P&R|IVP|Eerdmans|Press|Regular Baptist|Kregel|patmos|Reformed Fellowship",re.I)
PER=None
def kind(scope):
    old=bool(OLD.search(scope)); mod=bool(MOD.search(scope)); web=bool(WEB.search(scope))
    if web and not old: return "веб-страница (вторичный сайт)"
    if old and not mod: return "ранняя печать (оцифровка возможна)"
    if mod and not old: return "книга XX–XXI в. (нужна покупка или библиотека)"
    if old and mod: return "смешанный адрес (старое издание +modernая литература)"
    return "не выводимо из текста адреса"
c_addr=collections.Counter(); c_scope=collections.Counter(); both=0
for q in sorted(q2row):
    a=q2row[q]; rid=addr_row.get(q); cells=" ".join(tab[rid]) if rid else ""
    ka=kind(a); kb=kind(a+" "+cells)
    c_addr[ka]+=1; c_scope[kb]+=1
    if ka==kb: both+=1
print("\nклассы по одному тексту адреса:")
for k,v in c_addr.most_common(): print("  %4d  %s"%(v,k))
print("классы по адресу+строке:")
for k,v in c_scope.most_common(): print("  %4d  %s"%(v,k))
print("совпало в обоих определениях:",both,"из",len(q2row))
mixed=[q for q in sorted(q2row) if kind(q2row[q])!=kind(q2row[q]+" "+(" ".join(tab[addr_row[q]]) if addr_row.get(q) else ""))]
print("расходятся:",len(mixed),mixed[:12])
json.dump({"инвентарь":{"строгие":len(s1),"цифраКонтекст":len(s2),"объединение":len(s1|s2),"файлов":len(perim)},
 "классыАдрес":dict(c_addr),"классыОба":dict(c_scope),"совпало":both,"расходятся":mixed,
 "расходитсяПоАдресу":{q:{"адрес":kind(q2row[q]),"сЯчейками":kind(q2row[q]+" "+(" ".join(tab[addr_row[q]]) if addr_row.get(q) else ""))} for q in mixed}},
 open(ROOT/".scratch/q46d.json","w"),ensure_ascii=False,indent=1)
