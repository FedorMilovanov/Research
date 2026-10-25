import re,pathlib,collections,json
ROOT=pathlib.Path("/home/user/Research")
REG=pathlib.Path("docs/research/atonement/35_four_point_authors_mass_registry.md")
t=(ROOT/REG).read_text(); lines=t.split("\n")
rows={}; q2row={}
for l in lines:
    m=re.match(r"^\| (FP-\d+) \|(.*)\|\s*$",l)
    if m: rows["FP-%02d"%int(m.group(1).split("-")[1])]=[x.strip() for x in m.group(2).split("|")]
for l in lines:
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
addr_row={}
for rid,cells in rows.items():
    for x in re.findall(r"Q-(\d+)"," ".join(cells)):
        q="Q-%02d"%int(x)
        if q in q2row and q not in addr_row: addr_row[q]=rid
    m=re.search(r"^- Q-%s —"%rid.split("-")[1].lstrip("0"),t,re.M)
# --- инвентарь снимков: определение круга 44 (строга часть) 
SNAP=re.compile(r"`([a-z][a-z0-9]{6,20}\d{2}[a-z]{2,12})`")
perim=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+[p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
inv=collections.Counter()
for p in perim:
    for m in SNAP.finditer(p.read_text()): inv[m.group(1)]+=1
print("периметр файлов:",len(perim),"| снимков строгим определением:",len(inv))
ARCH=re.compile(r"archive\.org|ia\d{3,4}|_djvu\.txt",re.I); CTX=re.compile(r"`([a-z][a-z0-9_\-]{7,})`")
inv2=set(inv)|{m.group(1) for p in perim for m in CTX.finditer(p.read_text()) if ARCH.search(p.read_text()[max(0,m.start()-200):m.end()+200]) and not m.group(1).endswith((".md",".json",".txt",".py",".csv"))}
print("снимков с контекстным правилом:",len(inv2))
# --- классы
CAT=re.compile(r"установить|определить|выяснить|уточнить|атрибуц|какому сочинени|принадлежит|заглавие|год\b|издание|изд\.",re.I)
PAG=re.compile(r"страниц|пагинац|сдвиг|столбец|столбца|колонк|pp?\.\s*\d|номер главы|гл\.",re.I)
READ=re.compile(r"прочитать|снять|разобраться|дочитать|пробежать|выписат|цитат|место",re.I)
PL=re.compile(r"\bPL\s*(\d{2,3})\b|Migne|mign|patrologi",re.I)
YEAR=re.compile(r"\b(1[5-8]\d{2}|19\d{2})\b")
EEBO=re.compile(r"EEBO|TCP\s*[A-Z]\d+|A\d{5}",re.I)
res={}
for q in sorted(q2row):
    txt=q2row[q]; rid=addr_row.get(q); cells=" ".join(rows[rid]) if rid else ""
    scope=txt+" "+cells
    ids_in=sorted(set(x for x in re.findall(r"`([a-z][a-z0-9_\-]{7,})`",scope) if x in inv2))
    ids_any=sorted(set(re.findall(r"`([a-z][a-z0-9_\-]{7,})`",scope)))
    pl=re.search(r"\bPL\s*(\d{2,3})\b",scope)
    cand=[]
    if ids_in: cand.append("скан из инвентаря лана: "+", ".join(ids_in[:3]))
    if pl: cand.append("том Migne: PL %s"%pl.group(1))
    if EEBO.search(scope): cand.append("идентификатор EEBO/TCP")
    if YEAR.search(scope): cand.append("год издания в строке: "+", ".join(sorted(set(YEAR.findall(scope)))[:3]))
    if not cand: cand.append("нет кандидата")
    act=("каталог" if CAT.search(txt) else "пагинация" if PAG.search(txt) else "чтение" if READ.search(txt) else "иначе")
    res[q]={"row":rid,"act":act,"idsIn":ids_in,"idsAny":ids_any,"cand":cand}
c1=collections.Counter(v["act"] for v in res.values())
print("\nкласс действия по тексту адреса:",dict(c1))
print("адресов, где в адресе+строке назван скан из инвентаря лана:",sum(1 for v in res.values() if v["idsIn"]))
print("назван любой обратнокотированный id:",sum(1 for v in res.values() if v["idsAny"]))
cc=collections.Counter()
for v in res.values():
    if v["idsIn"]: cc["скан лана"]+=1
    elif any(x.startswith("том Migne") for x in v["cand"]): cc["том Migne (id известен из соседних кругов)"]+=1
    elif any(x.startswith("идентификатор EEBO") for x in v["cand"]): cc["EEBO/TCP-идентификатор"]+=1
    elif any(x.startswith("год издания") for x in v["cand"]): cc["только год/издание (нужен каталог)"]+=1
    else: cc["нет кандидата вовсе"]+=1
print("\nкандидат носителя:",dict(cc))
pl=collections.Counter()
for v in res.values():
    m=[x for x in v["cand"] if x.startswith("том Migne")]
    if m: pl[m[0]]+=1
print("пакеты по томам Migne:",pl.most_common(8))
noid=[q for q,v in res.items() if v["cand"]==["нет кандидата"]]
print("\nадресов без кандидата:",len(noid))
print("примеры:",", ".join(noid[:14]))
json.dump({"классы":dict(c1),"кандидат":dict(cc),"migne":dict(pl),"безКандидата":noid,
  "инвентарьСтрогий":len(inv),"инвентарьСКонтекстом":len(inv2),
  "res":{k:{"row":v["row"],"act":v["act"],"idsIn":v["idsIn"],"idsAny":v["idsAny"],"cand":v["cand"]} for k,v in res.items()}},
  open(ROOT/".scratch/q46b.json","w"),ensure_ascii=False,indent=1)
