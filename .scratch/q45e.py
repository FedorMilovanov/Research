import re,pathlib,json
from collections import defaultdict,Counter
ROOT=pathlib.Path("/home/user/Research")
REG=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
t=REG.read_text(); lines=t.split("\n")
qadd={}
for l in lines:
    m=re.match(r"^- (Q-0*\d+)\b",l)
    if m: qadd["Q-%02d"%int(m.group(1).split("-")[1])]=l
rows={}; titles={}
for l in lines:
    if l.startswith("| FP-"):
        rid=re.match(r"^\| (FP-\d+) \|",l).group(1); rows[rid]=l
        cells=[c.strip() for c in l.split("|")]
        titles[rid]=re.sub(r"[*`]","",cells[2] if len(cells)>2 else "")
rowbyref=defaultdict(list)
for rid,l in rows.items():
    for m in re.finditer(r"\bQ-\d+\b",l): rowbyref["Q-%02d"%int(m.group(0).split("-")[1])].append(rid)
CAP=re.compile(r"\b[A-ZÀ-Ỹ][A-Za-zÀ-ỹœŒĀā]{4,}\b|\b[А-ЯЁ][а-яё]{4,}\b")
# df = в скольких заглавиях строк и скольких адресах очереди встречается токен с такой буквы
df=defaultdict(set)
for rid,ti in titles.items():
    for m in CAP.finditer(ti): df[m.group(0)].add(("row",rid))
for q,l in qadd.items():
    for m in CAP.finditer(re.sub(r"[*`]","",l)): df[m.group(0)].add(("q",q))
GEN={k for k,v in df.items() if len({y for x,y in v})>2}   # нарицательное: в >2 разных строках/адресах
PART={"of","de","van","der","the","and","из","ди","sancti","saint"}
def keys_for(rid,addr):
    out=[]
    src=[]
    if rid: src.append(re.split(r"[,;(]",titles[rid])[0])
    if addr:
        m=re.match(r"^- Q-\d+ — (.*)",addr,re.S)
        if m: src.append(re.split(r"[,;(<]",re.sub(r"[*`]","",m.group(1)))[0])
    for s in src:
        for m in CAP.finditer(s):
            w=m.group(0)
            if w in PART or w in GEN or w[1:2].isupper(): continue
            if w not in out: out.append(w)
        if out: break
    return out
peri=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+ \
     [p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
texts={p.relative_to(ROOT).as_posix():p.read_text() for p in peri}
LOC=re.compile(r"(?:\bpp?\.\s|\bcols?\.?\s|столбец|столбца|столб\.|лист[ах]?\s*\d|страниц|стр\.\s*\d|col\.\s|leaf|cc?\.\s*\d{2,4}|сс\.\s*\d|\bs\.\s*\d{2,4})",re.I)
QUOTE=re.compile(r"«[^»]{25,}»")
NAMES=["автор не назван в периметре ни разу","назван, но ни в одной строке с локатором",
 "назван в строке с локатором, без цитаты","назван в строке с локатором и цитатой"]
cls={};det={}
for q,addr in sorted(qadd.items()):
    rids=rowbyref.get(q,[])
    ks=keys_for(rids[0],addr) if rids else keys_for(None,addr)
    if not ks and rids: ks=keys_for(None,addr)
    files=set(); loc=[]; quot=[]
    for fn,tx in texts.items():
        for ln in tx.split("\n"):
            if ks and not any(re.search(r"(?<![\w])"+re.escape(k)+r"(?![\w])",ln) for k in ks): continue
            if not ks: files=set(); break
            files.add(fn)
            if LOC.search(ln):
                loc.append((fn,ln.strip()))
                if QUOTE.search(ln): quot.append((fn,ln.strip()))
    c=1 if not ks or not files else 2 if not loc else 3 if not quot else 4
    cls[q]=NAMES[c-1]
    det[q]={"rows":rids,"keys":ks,"nfiles":len(files),"files":sorted(files)[:8],"nloc":len(loc),"nquote":len(quot),
      "quote":[{"file":f,"line":l[:300]} for f,l in quot[:5]],"nokey":not ks}
cc=Counter(cls.values()); n=len(cls)
print("=== перепись очереди по авторскому имени (ключ: собственное имя из сегмента автора, отброшены нарицательные токены — те, что встречаются более чем в двух заглавиях/адресах)")
print("периметр: %d файлов, адресов: %d, адресов без ключа: %d"%(len(texts),n,sum(1 for v in det.values() if v["nokey"])))
for k in NAMES: print("  %-46s %3d  %6.2f %%"%(k,cc[k],100*cc[k]/n))
print("=== кандидаты на ручной разбор (%d)"%cc[NAMES[3]])
for q in sorted(cls):
    if cls[q]==NAMES[3]:
        d=det[q]; print("%s [%s] ключи %s | файлов %d, с локатором %d, с цитатой %d"%(q,",".join(d["rows"]) or "—",", ".join(d["keys"]),d["nfiles"],d["nloc"],d["nquote"]))
json.dump({"cls":cls,"det":det},open(".scratch/q45.json","w"),ensure_ascii=False,indent=1)
print("детали: .scratch/q45.json")
