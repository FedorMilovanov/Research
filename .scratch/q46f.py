import re,pathlib,collections,json
ROOT=pathlib.Path("/home/user/Research")
REGNAME="35_four_point_authors_mass_registry.md"
reg=(ROOT/"docs/research/atonement"/REGNAME).read_text()
SNAP=re.compile(r"`([a-z][a-z0-9]{6,20}\d{2}[a-z]{2,12})`")
DIG=re.compile(r"`([a-z][a-z0-9_\-]{6,}\d[a-z0-9_\-]{0,20})`")
ARCH=re.compile(r"archive\.org|ia\d{3,4}|_djvu\.txt",re.I)
perim=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REGNAME]+[p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
lane_snap=set(); lane_pairs=0
for p in perim:
    x=p.read_text()
    ids=set(SNAP.findall(x))|{m.group(1) for m in DIG.finditer(x) if ARCH.search(x[max(0,m.start()-200):m.end()+200])}
    lane_snap|=ids; lane_pairs+=len(ids)
# что названо самим реестром
reg_ids_strict=set(SNAP.findall(reg))
reg_ids_all=reg_ids_strict|{m.group(1) for m in DIG.finditer(reg) if ARCH.search(reg[max(0,m.start()-200):m.end()+200])}
print("реестр называет id: строгим определением",len(reg_ids_strict),"| с контекстом",len(reg_ids_all))
print("инвентарь лана (объединение двух правил, 122 файла):",len(lane_snap))
print("пересечение (названо реестром И есть в лане):",len(reg_ids_all&lane_snap),"| строгое:",len(reg_ids_strict&lane_snap))
print("реестром названо, в лане отсутствует:",sorted(reg_ids_all-lane_snap)[:10])
# --- классы объекта: два определения и пересечения
q2row={}
for l in reg.split("\n"):
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
tab={}
for l in reg.split("\n"):
    m=re.match(r"^\| (FP-0*(\d+)) \|(.*)\|\s*$",l)
    if m: tab["FP-%02d"%int(m.group(2))]=[x.strip() for x in m.group(3).split("|")]
addr_row={}
for rid,cells in tab.items():
    for x in re.findall(r"Q-(\d+)"," ".join(cells)):
        q="Q-%02d"%int(x)
        if q in q2row and q not in addr_row: addr_row[q]=rid
WEB=re.compile(r"http|\.com|\.org|\?p=|\?page_id=|сайт",re.I)
OLD=re.compile(r"\b(1[4-8]\d{2})\b|PL \d|Migne|mign|Patrolog|EEBO|TCP|Acta|confessio|Opera",re.I)
MOD=re.compile(r"\b(19\d{2}|20[0-2]\d)\b|Crossway|Baker|P&R|IVP|Eerdmans|Press|Kregel",re.I)
def kind(s):
    o,m,w=bool(OLD.search(s)),bool(MOD.search(s)),bool(WEB.search(s))
    if w and not o: return "веб"
    if o and not m: return "ранняя печать"
    if m and not o: return "книга XX–XXI"
    if o and m: return "смешанный"
    return "не выводимо"
pairs={}
for q in sorted(q2row):
    cells=" ".join(tab[addr_row[q]]) if addr_row.get(q) else ""
    pairs[q]=(kind(q2row[q]),kind(q2row[q]+" "+cells))
A=collections.Counter(a for a,b in pairs.values()); B=collections.Counter(b for a,b in pairs.values())
same=sum(1 for a,b in pairs.values() if a==b)
print("\nклассы по адресу:",dict(A)); print("классы по адресу+строке:",dict(B)); print("совпало:",same,"из",len(pairs))
for k in ["ранняя печать","книга XX–XXI","веб","смешанный","не выводимо"]:
    i=sum(1 for a,b in pairs.values() if a==k and b==k); u=sum(1 for a,b in pairs.values() if a==k or b==k)
    print("  %-16s пересечение %3d (%5.2f %% от 102) | объединение %3d"%(k,i,100*i/102,u))
json.dump({"инвентарьЛана":len(lane_snap),"реестрНазвал":len(reg_ids_all),"пересечение":len(reg_ids_all&lane_snap),
 "классыАдрес":dict(A),"классыОба":dict(B),"совпало":same,
 "пересечения":{k:[sum(1 for a,b in pairs.values() if a==k and b==k),sum(1 for a,b in pairs.values() if a==k or b==k)] for k in A.keys()|B.keys()},
 "pairs":pairs},open(ROOT/".scratch/q46f.json","w"),ensure_ascii=False,indent=1)
