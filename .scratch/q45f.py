import re,pathlib,json
from collections import defaultdict,Counter
ROOT=pathlib.Path("/home/user/Research")
REG=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
t=REG.read_text(); lines=t.split("\n")
qadd={}
for l in lines:
    m=re.match(r"^- (Q-0*\d+)\b",l)
    if m: qadd["Q-%02d"%int(m.group(1).split("-")[1])]=l
rows={};titles={}
for l in lines:
    if l.startswith("| FP-"):
        rid=re.match(r"^\| (FP-\d+) \|",l).group(1); rows[rid]=l
        cells=[c.strip() for c in l.split("|")]
        titles[rid]=re.sub(r"[*`]","",cells[2] if len(cells)>2 else "")
rowbyref=defaultdict(list)
for rid,l in rows.items():
    for m in re.finditer(r"\bQ-\d+\b",l): rowbyref["Q-%02d"%int(m.group(0).split("-")[1])].append(rid)
CAP=re.compile(r"\b[A-ZÀ-Ỹ][A-Za-zÀ-ỹœŒĀā]{4,}\b|\b[А-ЯЁ][а-яё]{4,}\b")
df=defaultdict(set)
for rid,ti in titles.items():
    for m in CAP.finditer(ti): df[m.group(0)].add(rid)
PART={"of","de","van","der","the","and","из","ди","sancti","saint"}
MANUAL={"индекс","страницы","страница","глава","главы","заглавие","установить","уточнить","сверить","снять",
 "разобрать","постранично","кластер","тексты","текста","опровержение","неопубликованное","трактат","вменении",
 "опосредованном","записи","линия","оппоненты","журнал","богословы","вестминстерские","реформатская","церковь",
 "венгрии","сиднейская","латинский","английский","добыть","оппонентов","перевод","издание","тома","том","книга",
 "сочинения","письма","проповеди","комментарии","примечания","рукопись","редакция","предисловие","указатель"}
peri=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+ \
     [p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
texts={p.relative_to(ROOT).as_posix():p.read_text() for p in peri}
LOC=re.compile(r"(?:\bpp?\.\s|\bcols?\.?\s|столбец|столбца|столб\.|лист[ах]?\s*\d|страниц|стр\.\s*\d|col\.\s|leaf|cc?\.\s*\d{2,4}|сс\.\s*\d|\bs\.\s*\d{2,4})",re.I)
QUOTE=re.compile(r"«[^»]{25,}»")
def keys_for(rid,addr,variant):
    src=[]
    if rid: src.append(re.split(r"[,;(<]",titles[rid])[0])
    m=re.match(r"^- Q-\d+ — (.*)",addr,re.S)
    if m: src.append(re.split(r"[,;(<]",re.sub(r"[*`]","",m.group(1)))[0])
    out=[]
    for s in src:
        for mm in CAP.finditer(s):
            w=mm.group(0); lw=w.lower()
            if w in PART or w[1:2].isupper(): continue
            if variant==1 and len(df[w])>2: continue          # авто-genericity
            if variant==2 and lw in MANUAL: continue          # ручной стоп-лист
            if w not in out: out.append(w)
        if out: break
    return out
def census(variant):
    res={}
    for q,addr in sorted(qadd.items()):
        rids=rowbyref.get(q,[])
        ks=keys_for(rids[0],addr,variant) if rids else keys_for(None,addr,variant)
        if not ks: res[q]={"c":0,"ks":[]}; continue
        files=set(); loc=[]; quot=[]
        for fn,tx in texts.items():
            for ln in tx.split("\n"):
                if not any(re.search(r"(?<![\w])"+re.escape(k)+r"(?![\w])",ln) for k in ks): continue
                files.add(fn)
                if LOC.search(ln):
                    loc.append((fn,ln.strip()))
                    if QUOTE.search(ln): quot.append((fn,ln.strip()))
        c=1 if not files else 2 if not loc else 3 if not quot else 4
        res[q]={"c":c,"ks":ks,"nfiles":len(files),"nloc":len(loc),"nquote":len(quot),
                "rows":rids,"quote":[{"file":f,"line":l} for f,l in quot[:6]]}
    return res
A=census(1); B=census(2)
LAB={0:"имя не извлекается",1:"автор не назван в периметре ни разу",2:"назван без локатора",3:"назван с локатором, без цитаты",4:"назван с локатором и цитатой"}
for name,R in (("вариант 1 (авто: токен в >2 заглавиях — нарицательный)",A),("вариант 2 (ручной стоп-лист служебных слов)",B)):
    cc=Counter(v["c"] for v in R.values())
    print("===",name)
    for k in range(5): print("   %-42s %3d  %6.2f %%"%(LAB[k],cc[k],100*cc[k]/102))
candA={q for q,v in A.items() if v["c"]==4}; candB={q for q,v in B.items() if v["c"]==4}
print("кандидаты: A=%d B=%d | пересечение=%d | объединение=%d"%(len(candA),len(candB),len(candA&candB),len(candA|candB)))
print("=== ручная выборка: адреса из пересечения")
for q in sorted(candA&candB):
    v=B[q]; print("%s [%s] ключи %s | цитат %d"%(q,",".join(v["rows"]) or "—",", ".join(v["ks"]),v["nquote"]))
    for it in v["quote"][:2]: print("      %s :: %s"%(it["file"],it["line"][:190]))
json.dump({"A":A,"B":B,"candA":sorted(candA),"candB":sorted(candB)},open(".scratch/q45.json","w"),ensure_ascii=False,indent=1)
