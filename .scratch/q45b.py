import re,pathlib,json
from collections import defaultdict
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
FIRST={"james","john","richard","thomas","robert","edward","george","william","charles","henry","francis","daniel",
 "nathanael,""isaac","jacob","petrus","joannes","augustinus","августин","джеймс","джон","томас","роберт","эдвард",
 "чарльз","фрэнсис","даниил","нафанаил","исак","ияков","пётр","петр","иоганн","иоанн","якоб","гергард","эразм",
 "hugh","bobby,""andrew","antonius","lucius","marcus","gaius","vigilius"," prosper"}
PART={"of","de","van","der","ди","из","изд","ed","eds","edn","ed.","sancti","saint","svnt","accursius","aquinas"}
def surname_keys(rowtext,addrtext):
    """ключ = фамилия (или прозвание): слова сегмента до первой запятой в заглавии строки; при отсутствии строки — из адреса"""
    out=set()
    for src in ([c.strip() for c in rowtext.split("|")][2] if rowtext else ""):
        seg=re.split(r"[,;(]",src)[0]
        seg=re.sub(r"\*","",seg)
        for w in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿœŒ-]+|[А-Яа-яЁё][А-Яа-яЁё]+",seg):
            lw=w.lower()
            if len(lw)<5 or lw in FIRST or lw in PART: continue
            out.add(lw)
    if not out and addrtext:
        m=re.match(r"^- Q-\d+ — ([^,;(.]+)",addrtext)
        if m:
            for w in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ]+|[А-Яа-яЁё][А-Яа-яЁё]+",m.group(1)):
                if len(w)>=5 and w.lower() not in FIRST: out.add(w.lower())
    return out
LOC=re.compile(r"(?:\bpp?\.\s|\bcols?\.?\s|столбец|столбца|столб\.|лист[ах]?|страниц|стр\.\s|col\.\s|\bleaf\b|\bleaves\b|s\.\s*\d{2,4}|c\.\s*\d{2,4}|сс\.\s)",re.I)
QUOTE=re.compile(r"«[^»]{25,}»|”\s*«|\*[A-ZÀ-Ỹ][^*]{25,}\*")
cls={}; detail={}
for q,addr in sorted(qadd.items()):
    rids=rowbyref.get(q,[])
    ks=set()
    for rid in rids: ks|=surname_keys(rows[rid],addr)
    if not ks: ks=surname_keys("",addr)
    namehits=[]; lochits=[]; qhits=[]
    for fn,tx in texts.items():
        for ln in tx.split("\n"):
            low=ln.lower()
            if not any(re.search(r"(?<![\w])"+re.escape(k)+r"(?![\w])",low) for k in ks): continue
            namehits.append(fn)
            if LOC.search(ln):
                lochits.append((fn,ln.strip()))
                if QUOTE.search(ln): qhits.append((fn,ln.strip()))
            break_after=False
    cls[q]=("ни разу не назван" if not namehits else "назван без локатора" if not lochits else "назван с локатором и цитатой" if qhits else "назван в строке с локатором")
    detail[q]={"rows":rids,"keys":sorted(ks),"files":sorted(set(namehits)),"nfiles":len(set(namehits)),
       "loc":lochits[:3],"quote":qhits[:3]}
from collections import Counter
cc=Counter(cls.values())
print("=== partition адреса очереди по тому, как автор назван в периметре лана (122 файла)")
for k,v in cc.most_common(): print("  %-34s %3d  (%.2f %%)"%(k,v,100*v/len(cls)))
print("итого адресов:",len(cls))
print("=== адреса, названные в строке с локатором и цитатой (кандидаты на ручной разбор)")
for q in sorted(cls):
    if cls[q]=="назван с локатором и цитатой":
        d=detail[q]; print("%s [%s] ключи %s файлов %d"%(q,",".join(d["rows"]) or "—",", ".join(d["keys"])[:60],d["nfiles"]))
        for fn,ln in d["quote"][:2]: print("      %s :: %s"%(fn,ln[:150]))
json.dump({"cls":cls,"detail":detail},open(".scratch/q45.json","w"),ensure_ascii=False,indent=1)
print("детали: .scratch/q45.json")
