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
    s=(s or "").replace("ſ","s").replace("ﬁ","fi")
    s=unicodedata.normalize("NFKD",s)
    s=re.sub(r"[^a-z0-9 ]+"," ",s.lower()); return re.sub(r"\s+"," ",s).strip()
recs=[]
with open(ROOT/".scratch/TCP.csv",newline="",encoding="utf-8") as f:
    for r in csv.DictReader(f): recs.append(r)
by_author=collections.defaultdict(list)
for r in recs:
    for tok in set(re.findall(r"[a-z]{5,}",norm(r["Author"]))): by_author[tok].append(r)
IT=re.compile(r"\*([^*]{12,})\*")
NAME=re.compile(r"\b([A-Z][a-zA-Z]{4,})\b")
STOP=set("London Oxford Cambridge Edition Works The And With From Being Wherein Without Wherein Concerning Certain Gospel".split())
res={}
for q,txt in q2row.items():
    rid=addr_row.get(q); cells=" ".join(tab[rid]) if rid else ""
    scope=txt+" "+cells
    keys=[norm(x) for x in IT.findall(scope)]
    keys=[k for k in keys if len(k)>=12]
    years=set(int(y) for y in re.findall(r"\b(1[4-7]\d{2})\b",scope))
    surn=set(t.lower() for t in NAME.findall(scope) if t not in STOP and not t.endswith("ing"))
    cand=collections.Counter()
    for sn in surn:
        for r in by_author.get(norm(sn),[]):
            ok = (any(k in norm(r["Title"]) for k in keys)) or (int(r["Date"]) in years if r["Date"].isdigit() and years else False)
            if ok: cand[r["TCP"]]+=1
    res[q]={"keys":len(keys),"surn":sorted(surn)[:6],"years":sorted(years),"hits":sorted(cand)}
u=[q for q,v in res.items() if len(v["hits"])==1]; m=[q for q,v in res.items() if len(v["hits"])>1]; z=[q for q,v in res.items() if not v["hits"]]
print("определение 2 (автор + (заглавие|год)): уникальных %d | нескольких %d | без записи %d"%(len(u),len(m),len(z)))
for q in u:
    tcp=res[q]["hits"][0]; r=[x for x in recs if x["TCP"]==tcp][0]
    print("  %s [%s] → %s | %s | %s | листов %s | %s"%(q,addr_row.get(q),r["TCP"],r["STC"][:30],r["Date"],r["Pages"],r["Author"][:38]))
d1=json.load(open(ROOT/".scratch/q46g.json"))
inter=set(u)&set(d1["уникальных"]); uni=set(u)|set(d1["уникальных"])
print("\nпересечение с определением 1:",len(inter),"| объединение:",len(uni))
print("только опр.2:",sorted(set(u)-set(d1["уникальных"])))
print("только опр.1:",sorted(set(d1["уникальных"])-set(u)))
json.dump({"уникальных2":u,"несколько2":m,"нет2":len(z),"пересечение":sorted(inter),"объединение":sorted(uni),
 "рез":{q:res[q]["hits"] for q in u+m}},open(ROOT/".scratch/q46h.json","w"),ensure_ascii=False,indent=1)
