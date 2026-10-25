import re,pathlib,json
from collections import defaultdict
ROOT=pathlib.Path("/home/user/Research")
REG=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
t=REG.read_text(); lines=t.split("\n")
qlines=[l for l in lines if re.match(r"^- Q-\d+",l)]
def norm_id(x):
    m=re.match(r"Q-0*(\d+)$",x.strip()); return "Q-%02d"%int(m.group(1)) if m else None
qadd={norm_id(re.match(r"^- (Q-\d+)",l).group(1)):l for l in qlines}
rows={}
for l in lines:
    if l.startswith("| FP-"):
        rid=re.match(r"^\| (FP-\d+) \|",l).group(1); rows[rid]=l
rowbyref=defaultdict(list)
for rid,l in rows.items():
    for m in re.finditer(r"\bQ-\d+\b",l): rowbyref[norm_id(m.group(0))].append(rid)
peri=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+ \
     [p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
texts={p.relative_to(ROOT).as_posix():p.read_text() for p in peri}
LATSTOP={"liber","de","et","in","ad","contra","super","secundum","quaestio","epistola","capitula","caput",
 "opusculum","tractatus","sententia","sententiae","sententiarum","excerptiones","confessio","enarratio",
 "expositionum","expositionem","expositio","commentariorum","commentarius","commentii","quae","quod","qui",
 "que","atque","vel","nec","non","ut","sicut","item","libri","libro","versio","editio","notae","nota",
 "prologus","praefatio","disputatio","disputationes","theologia","theologica","doctrina","assertio",
 "assertiones","vindicatio","animadversio","animadversiones","inquiry","inquiryes","treatise","discourse",
 "discourses","sermo","sermones","homilia","homiliae","regula","regulae","annotata","annotatio","responsio",
 "responsiones","defensio","commonitorium","collatio","collationes","confutatio","duplex","totius","opus",
 "opera","operibus","magna","magnus","novum","testamenti","vetus","librum","contra","adversus","tractatio",
 "animadversionum","iudicium","judicium","tractatibus","disputationem","questiones","quaestiones"}
CYRSTOP=set("""круг очередь строка адрес издание издательство том глава лист страница колонка ссылка реестр
указатель индекс класс периметр носитель оцифровка проба номер цифра разобрать установить уточнить решить
перевод переводчик предисловие заглавие заглавный универсалист универсалисты четырёхпунктник четырёхпунктники
позиция позиции сочинение сочинения свидетель свидетельство вторичный первичный библиограф библиография
отсылка вычитка сверка цитата цитаты фрагмент фрагменты извлечение извлечения версия версии рукопись рукописи
кодекс кодексы название названия список списка разбор разборы замечание замечания рассуждение рассуждения
исследование исследования трактат трактата беседа беседе письмо письма послание послания толкование толкования
вопрос вопросы глава главы article articles book books volume volumes""".split())
def keys_for(rowtext):
    cells=[c.strip() for c in rowtext.split("|")]
    title=cells[2] if len(cells)>2 else rowtext
    ks=set()
    for m in re.finditer(r"\b[А-ЯЁ][а-яё]{4,}\b",title):
        w=m.group(0).lower()
        if w not in CYRSTOP: ks.add(w)
    for m in re.finditer(r"\b[A-ZÀ-Ỹa-zà-ỹ][A-Za-zÀ-ỹœŒĀā]{4,}\b",title):
        w=m.group(0).lower()
        if w in LATSTOP or w.rstrip("ys") in {s.rstrip("ys") for s in LATSTOP}: continue
        ks.add(w)
    return ks
LOC=re.compile(r"(?:\bp\.|\bpp\.|\bcol\.|\bcols\.|\bcolumn|столбец|столбца|столб\.|лист|листа|leaf|leaves|страниц|стр\.|\sс\.\s*\d|\bc\.\s*\d)",re.I)
QUOTE=re.compile(r"«[^»]{25,}»")
res={}
for q,addr in sorted(qadd.items()):
    rids=rowbyref.get(q,[])
    ks=set(); src=addr
    for rid in rids: ks|=keys_for(rows[rid]); src=rows[rid]
    if not ks: ks=keys_for(addr)
    hits=[]
    for fn,tx in texts.items():
        for ln in tx.split("\n"):
            if not LOC.search(ln) or not QUOTE.search(ln): continue
            low=ln.lower()
            g=[k for k in ks if re.search(r"(?<![\w])"+re.escape(k)+r"(?![\w])",low)]
            if g: hits.append((fn,ln.strip()[:220],g)); break
    res[q]={"rows":rids,"nkeys":len(ks),"keys":sorted(ks),"nfiles":len(hits),"sample":hits[:4]}
cand=[k for k,v in res.items() if v["nfiles"]]
print("адресов:",len(res),"| с кандидатом в периметре:",len(cand),"| без:",len(res)-len(cand))
print("адресов без строки-носителя (ключ из строки очереди):",sum(1 for v in res.values() if not v["rows"]))
for k in sorted(cand,key=lambda x:-res[x]["nfiles"]):
    v=res[k]; print("%s [%s] файлов %d | ключи: %s"%(k,",".join(v["rows"]) or "—",v["nfiles"],", ".join(v["keys"][:7])))
    for fn,ln,g in v["sample"][:2]: print("      %s :: %s"%(fn,ln[:170]))
json.dump(res,open("/home/user/Research/.scratch/q45.json","w"),ensure_ascii=False,indent=1)
print("детали: .scratch/q45.json")
