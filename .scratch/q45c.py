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
# ключ = собственное имя: заглавная буква в исходнике, длина >=5, вне списка нартопиков и частиц
NAMESTOP={"christ","death","grace","atonement","redemption","faith","works","truth","doctrine","salvation","heaven",
 "cross","sermon","chapter","points","views","extent","discourse","treatise","essay","inquiry","confessions",
 "catholica","centuries","english","reformation","reformed","canons","covenant","justification","sanctification",
 "glory","merit","satisfaction","remedy","mediation","reconciliation","election","decree","purpose","offer","gospel",
 "judicia","acta","opera","works","somnium","tractatus","disputatio","quaestio","regula","institutio","confessio",
 "assertio","vindicatio","animadversio","responsio","commonitorium","collatio","expositio","enarratio","liber",
 "capitula","epistola","sermo","homilia","prologus","praefatio","duplex","totius","magna","novum","testamenti",
 "against","about","after","before","within","upon","being","there","where","which","whose","that","this","these","those",
 "the","and","for","not","but","all","any","with","from","into","over","under","more","most","less","well","also",
 "беседа","письмо","послание","толкование","рассуждение","исследование","верноучение","вероучение","сочинение",
 "указатель","индекс","каталог","издание","перевод","комментарии","примечания","замечания","описание","разбор"}
PART={"of","de","van","der","ди","из","sancti","saint","the","and"}
def name_keys(seg):
    out=set()
    for m in re.finditer(r"\b[A-ZÀ-Ỹ][A-Za-zÀ-ỹœŒĀāÀ-ÿ-]{4,}\b|\b[А-ЯЁ][а-яёА-ЯЁ-]{4,}\b",seg):
        w=m.group(0)
        lw=w.lower()
        if lw in NAMESTOP or lw in PART or w[1:2].isupper(): continue
        out.add(lw)
    return out
def keys_for(rid,addr):
    ks=set()
    if rid:
        cells=[c.strip() for c in rows[rid].split("|")]
        title=re.sub(r"\*","",cells[2] if len(cells)>2 else "")
        ks|=name_keys(title.split(",")[0])          # сегмент автора
        ks|=name_keys(" ".join(re.findall(r"\*([^*]{5,})\*",title)) if False else "")  # (заглавия не используются)
    if not ks:
        m=re.match(r"^- Q-\d+ — ([^,;(.]{3,})",addr)
        if m: ks|=name_keys(m.group(1))
    return ks
LOC=re.compile(r"(?:\bpp?\.\s|\bcols?\.?\s|столбец|столбца|столб\.|лист[ах]?|страниц|стр\.\s|col\.\s|\bleaf\b|cc?\.\s*\d{2,4}|сс\.\s|\bs\.\s*\d{2,4})",re.I)
QUOTE=re.compile(r"«[^»]{25,}»")
cls={};det={}
for q,addr in sorted(qadd.items()):
    rids=rowbyref.get(q,[])
    ks=set()
    for rid in rids: ks|=keys_for(rid,addr)
    ks|=keys_for("",addr) if len(ks)<2 else ks
    namefiles=set(); loc=[]; quot=[]
    for fn,tx in texts.items():
        for ln in tx.split("\n"):
            low=ln.lower()
            if not any(re.search(r"(?<![\w])"+re.escape(k)+r"(?![\w])",low) for k in ks): continue
            namefiles.add(fn)
            if LOC.search(ln):
                loc.append((fn,ln.strip()))
                if QUOTE.search(ln): quot.append((fn,ln.strip()))
    if not namefiles: c="автор не назван в периметре ни разу"
    elif not loc: c="назван, но ни в одной строке с локатором"
    elif not quot: c="назван в строке с локатором, без цитаты"
    else: c="назван в строке с локатором и цитатой"
    cls[q]=c; det[q]={"rows":rids,"keys":sorted(ks),"nfiles":len(namefiles),"files":sorted(namefiles)[:6],
       "quote":[{"file":f,"line":l[:400]} for f,l in quot[:3]]}
cc=Counter(cls.values()); n=len(cls)
print("=== перепись: как автор адреса очереди назван в периметре лана (%d файлов)"%len(texts))
for k in ["автор не назван в периметре ни разу","назван, но ни в одной строке с локатором","назван в строке с локатором, без цитаты","назван в строке с локатором и цитатой"]:
    print("  %-46s %3d  %6.2f %%"%(k,cc[k],100*cc[k]/n))
print("итого:",n,"| адресов без ключа:",sum(1 for v in det.values() if not v["keys"]))
print("=== кандидаты (ручная проверка обязательна)")
for q in sorted(cls):
    if cls[q]=="назван в строке с локатором и цитатой":
        d=det[q]; print("%s [%s] ключи: %s | файлов %d"%(q,",".join(d["rows"]) or "—",", ".join(d["keys"]),d["nfiles"]))
        for it in d["quote"][:1]: print("      %s :: %s"%(it["file"],it["line"][:130]))
json.dump({"cls":cls,"det":det},open(".scratch/q45.json","w"),ensure_ascii=False,indent=1)
