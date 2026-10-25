import re,pathlib,json
from collections import defaultdict,Counter
ROOT=pathlib.Path("/home/user/Research")
REG=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
t=REG.read_text(); lines=t.split("\n")
qadd={}
for l in lines:
    m=re.match(r"^- (Q-0*\d+)\b",l)
    if m: qadd["Q-%02d"%int(m.group(1).split("-")[1])]=l
rows={}
for l in lines:
    if l.startswith("| FP-"): rows[re.match(r"^\| (FP-\d+) \|",l).group(1)]=l
rowbyref=defaultdict(list)
for rid,l in rows.items():
    for m in re.finditer(r"\bQ-\d+\b",l): rowbyref["Q-%02d"%int(m.group(0).split("-")[1])].append(rid)
peri=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+ \
     [p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
texts={p.relative_to(ROOT).as_posix():p.read_text() for p in peri}
NAMESTOP={"christ","death","grace","atonement","redemption","faith","works","truth","doctrine","salvation","heaven",
 "cross","sermon","chapter","points","views","extent","discourse","treatise","essay","inquiry","confessions",
 "catholica","centuries","english","reformation","reformed","canons","covenant","justification","glory",
 "against","about","after","before","within","upon","being","there","where","which","whose","that","this","these",
 "the","and","for","not","but","all","any","with","from","into","over","under","more","most","less","well","also",
 "Institutio","Opera","Works","Acta","Judicia","Canons","Confessio","Turretin"}
PART={"of","de","van","der","the","and","из","ди","sancti","saint"}
CAP=re.compile(r"\b[A-ZÀ-Ỹ][A-Za-zÀ-ỹœŒĀā]{4,}\b|\b[А-ЯЁ][а-яё]{4,}\b")
def keys_for(rid,addr):
    srcs=[]
    if rid:
        cells=[c.strip() for c in rows[rid].split("|")]
        title=re.sub(r"[*`]",'',cells[2] if len(cells)>2 else "")
        srcs.append(re.split(r"[,;(]",title)[0])
    m=re.match(r"^- Q-\d+ — ([^,;(.]{3,})",addr)
    if m: srcs.append(m.group(1))
    out=[]
    for s in srcs:
        for mm in CAP.finditer(s):
            w=mm.group(0)
            if w in NAMESTOP or w.lower() in NAMESTOP or w in PART: continue
            if w[1:2].isupper(): continue
            if w not in out: out.append(w)
        if out: break
    return out
LOC=re.compile(r"(?:\bpp?\.\s|\bcols?\.?\s|столбец|столбца|столб\.|лист[ах]?\s*\d|страниц|стр\.\s*\d|col\.\s|leaf|cc?\.\s*\d{2,4}|сс\.\s*\d|\bs\.\s*\d{2,4})",re.I)
QUOTE=re.compile(r"«[^»]{25,}»")
cls={};det={}
for q,addr in sorted(qadd.items()):
    rids=rowbyref.get(q,[])
    ks=[]
    for rid in rids:
        ks=keys_for(rid,addr)
        if ks: break
    if not ks: ks=keys_for(None,addr)
    files=set(); loc=[]; quot=[]
    for fn,tx in texts.items():
        for ln in tx.split("\n"):
            if not any(re.search(r"(?<![\w])"+re.escape(k)+r"(?![\w])",ln) for k in ks): continue
            files.add(fn)
            if LOC.search(ln):
                loc.append((fn,ln.strip()))
                if QUOTE.search(ln): quot.append((fn,ln.strip()))
            if len(quot)>40: break
    if not files: c=1
    elif not loc: c=2
    elif not quot: c=3
    else: c=4
    NAMES={1:"автор не назван в периметре ни разу",2:"назван, но ни в одной строке с локатором",
      3:"назван в строке с локатором, без цитаты",4:"назван в строке с локатором и цитатой"}
    cls[q]=NAMES[c]; det[q]={"rows":rids,"keys":ks,"nfiles":len(files),"files":sorted(files)[:8],
      "nloc":len(loc),"nquote":len(quot),"quote":[{"file":f,"line":l[:300]} for f,l in quot[:4]]}
NAMES=["автор не назван в периметре ни разу","назван, но ни в одной строке с локатором",
 "назван в строке с локатором, без цитаты","назван в строке с локатором и цитатой"]
cc=Counter(cls.values()); n=len(cls)
print("=== перепись очереди по именованной форме автора (периметр: %d файлов, %d адресов)"%(len(texts),n))
for k in NAMES: print("  %-46s %3d  %6.2f %%"%(k,cc[k],100*cc[k]/n))
print("адресов без извлечённого ключа:",sum(1 for v in det.values() if not v["keys"]))
print("=== кандидаты на ручной разбор (%d)"%cc[NAMES[3]])
for q in sorted(cls):
    if cls[q]==NAMES[3]:
        d=det[q]; print("%s [%s] ключи %s | файлов %d, строк с локатором %d, с цитатой %d"%(q,",".join(d["rows"]) or "—",", ".join(d["keys"]),d["nfiles"],d["nloc"],d["nquote"]))
json.dump({"cls":cls,"det":det},open(".scratch/q45.json","w"),ensure_ascii=False,indent=1)
