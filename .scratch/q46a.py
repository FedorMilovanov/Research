import re,pathlib,collections,json
ROOT=pathlib.Path("/home/user/Research")
REG=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
t=REG.read_text()
lines=t.split("\n")
# --- строки реестра: q -> cells
rows={}
for l in lines:
    m=re.match(r"^\| (FP-\d+) \|(.*)\|\s*$",l)
    if m: rows[m.group(1)]=[x.strip() for x in m.group(2).split("|")]
q2row={}
for l in lines:
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
def qkey(s):
    m=re.search(r"\bQ-(\d+)\b",s);  return m
# адрес -> FP: по строке очереди ищем FP, иначе по строке реестра с тем же номером
addr_row={}
for q,txt in q2row.items():
    m=re.search(r"FP-(\d+)",txt)
    if m: addr_row[q]="FP-%02d"%int(m.group(1)); continue
n=0
for rid,cells in rows.items():
    joined=" ".join(cells)
    mm=re.findall(r"Q-(\d+)",joined)
    for x in mm:
        q="Q-%02d"%int(x)
        if q in q2row and q not in addr_row: addr_row[q]=rid
print("адресов:",len(q2row),"| сопоставлено со строкой:",len(addr_row))
# --- определение снимка по кругу 44
SNAP=re.compile(r"`([a-z][a-z0-9]{6,20}\d{2}[a-z]{2,12})`")
CTX=re.compile(r"`([a-z][a-z0-9_\-]{7,})`")
ARCH=re.compile(r"archive\.org|ia\d{3,4}|_djvu\.txt|\.us\.archive",re.I)
perim=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+ \
      [p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md") if "17_RECONCILIATION" in p.name or True]
perim=[p for p in perim if p.exists()]
inv=collections.Counter(); where=collections.defaultdict(set)
for p in perim:
    s=p.read_text()
    for m in SNAP.finditer(s):
        inv[m.group(1)]+=1; where[m.group(1)].add(p.name)
    for m in CTX.finditer(s):
        a,b=max(0,m.start()-200),min(len(s),m.end()+200)
        if ARCH.search(s[a:b]) and not m.group(1).endswith((".md",".json",".txt",".py")):
            inv[m.group(1)]+=1; where[m.group(1)].add(p.name)
print("уникальных снимков в периметре (122+ файла):",len(inv))
# --- классы действия
CAT=re.compile(r"установить|определить|выяснить|уточнить|атрибуц|какому сочинени|принадлежит|заглавие|год|издание|том\b|изд\.",re.I)
PAG=re.compile(r"страниц|пагинац|сдвиг|лист[ах] |столбец|столбца|колонк|pp?\.|колон",re.I)
READ=re.compile(r"прочитать|снять|разобраться|дочитать|пробежать|выписат|привесть|место|цитат",re.I)
res={}
for q in sorted(q2row):
    txt=q2row[q]; rid=addr_row.get(q)
    scope=txt+(" || "+" ".join(rows[rid]) if rid else "")
    ids=set(m.group(1) for m in CTX.finditer(scope) if m.group(1) in inv)
    all_named=set(m.group(1) for m in CTX.finditer(scope))
    if ids: act="носитель назван и он в инвентаре лана"
    elif all_named: act="id назван, но его нет в инвентаре лана"
    elif CAT.search(txt): act="каталожная задача"
    elif PAG.search(txt): act="нужна пагинация/локатор"
    elif READ.search(txt): act="нужно чтение места"
    else: act="иначе"
    res[q]={"row":rid,"ids":sorted(ids),"named":sorted(all_named),"act":act}
cnt=collections.Counter(v["act"] for v in res.values())
print("\nклассы действия:")
for k,c in cnt.most_common(): print(f"  {c:4d}  {k}")
batches=collections.Counter()
for v in res.values():
    for i in v["ids"]: batches[i]+=1
print("\nпакеты (адресов на один названный снимок):",len(batches))
for i,c in batches.most_common(10): print(f"   {c}  {i}  (в файлах: {len(where[i])})")
print("\nадресов с носителем из инвентаря:",sum(1 for v in res.values() if v["ids"]))
print("адресов с id вне инвентаря:",sum(1 for v in res.values() if v["named"] and not v["ids"]))
print("адресов без всякого id:",sum(1 for v in res.values() if not v["named"]))
json.dump({"res":{k:{"row":v["row"],"ids":v["ids"],"named":v["named"],"act":v["act"]} for k,v in res.items()},
 "классы":dict(cnt),"пакеты":dict(batches),"инвентарь":len(inv)},open(".scratch/q46.json","w"),ensure_ascii=False,indent=1)
