import re,pathlib,csv,json,collections,unicodedata
ROOT=pathlib.Path("/home/user/Research")
reg=(ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md").read_text()
q2row={}; tab={}
for l in reg.split("\n"):
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
    m=re.match(r"^\| (FP-0*(\d+)) \|(.*)\|\s*$",l)
    if m: tab["FP-%02d"%int(m.group(2))]=[x.strip() for x in m.group(3).split("|")]
addr_row={}
for rid,cells in tab.items():
    for x in re.findall(r"Q-(\d+)"," ".join(cells)):
        q="Q-%02d"%int(x)
        if q in q2row and q not in addr_row: addr_row[q]=rid
def norm(s):
    s=s.replace("ſ","s").replace("ﬁ","fi").replace("ﬀ","ff")
    s=unicodedata.normalize("NFKD",s)
    s=re.sub(r"[^a-z0-9 ]+"," ",s.lower())
    return re.sub(r"\s+"," ",s).strip()
# индекс каталога
rows=[]
with open(ROOT/".scratch/TCP.csv",newline="",encoding="utf-8") as f:
    for r in csv.DictReader(f): rows.append(r)
print("записей каталога:",len(rows))
idx=[(norm(r["Title"]),norm(r["Author"]),r) for r in rows]
# для каждого адреса: курсивные латинские фрагменты >= 8 букв из текста адреса и ячеек строки
IT=re.compile(r"\*([^*]{8,})\*")
res={}
CACHE={}
for q,txt in q2row.items():
    rid=addr_row.get(q); cells=" ".join(tab[rid]) if rid else ""
    spans=IT.findall(txt)+IT.findall(cells)
    spans=[s for s in spans if re.search(r"[A-Za-zſ]{8,}",s)]
    hits={}
    for sp in spans:
        key=norm(sp)
        if len(key)<8: continue
        if key not in CACHE:
            CACHE[key]=[r for tn,ta,r in idx if key in tn]
        for r in CACHE[key]: hits.setdefault(r["TCP"],(r,sp))
    res[q]={"spans":sorted(set(spans))[:6],"hits":{k:v[1] for k,v in hits.items()},"n":len(hits)}
uniq=[q for q,v in res.items() if v["n"]==1]; multi=[q for q,v in res.items() if v["n"]>1]; none=[q for q,v in res.items() if v["n"]==0]
print("адресов с уникальной записью каталога:",len(uniq))
print("адресов с несколькими записями:",len(multi),"| без записи (или без латинского заглавия):",len(none))
for q in uniq[:12]:
    r0=[x for x in idx if x[2]["TCP"]==list(res[q]["hits"])[0]][0][2]
    print("  %s [%s] → %s | %s | %s | стр. %s | %s"%(q,addr_row.get(q),r0["TCP"],r0["STC"],r0["Date"],r0["Pages"],r0["Author"][:44]))
json.dump({"уникальных":uniq,"несколько":multi,"нет":none,
 "хиты":{q:res[q]["hits"] for q in uniq+multi},
 "строк":len(rows)},open(ROOT/".scratch/q46g.json","w"),ensure_ascii=False,indent=1)
