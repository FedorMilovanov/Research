import re,pathlib,collections,json
ROOT=pathlib.Path("/home/user/Research")
REG=pathlib.Path("docs/research/atonement/35_four_point_authors_mass_registry.md")
t=(ROOT/REG).read_text(); lines=t.split("\n")
rows={}; q2row={}; row_of={}
for l in lines:
    m=re.match(r"^\| (FP-0*(\d+)) \|(.*)\|\s*$",l)
    if m: rows["Q-%02d"%int(m.group(2))]=None  # placeholder, ниже свяжем по ссылке Q-в-строке
for l in lines:
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
tab={}
for l in lines:
    m=re.match(r"^\| (FP-0*(\d+)) \|(.*)\|\s*$",l)
    if m: tab["FP-%02d"%int(m.group(2))]=[x.strip() for x in m.group(3).split("|")]
addr_row={}
for rid,cells in tab.items():
    for x in re.findall(r"Q-(\d+)"," ".join(cells)):
        q="Q-%02d"%int(x)
        if q in q2row and q not in addr_row: addr_row[q]=rid
print("адресов:",len(q2row),"| со строкой связано:",len(addr_row))
# --- круг 44: строгое + «с цифрой» в 200 знаках от archive.org
SNAP=re.compile(r"`([a-z][a-z0-9]{6,20}\d{2}[a-z]{2,12})`")
DIG=re.compile(r"`([a-z][a-z0-9_\-]{6,}\d[a-z0-9_\-]*)`")
ARCH=re.compile(r"archive\.org|ia\d{3,4}|_djvu\.txt",re.I)
perim=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+[p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
s1=set(); s2=set()
for p in perim:
    txt=p.read_text()
    s1|=set(SNAP.findall(txt))
    for m in DIG.finditer(txt):
        if ARCH.search(txt[max(0,m.start()-200):m.end()+200]): s2.add(m.group(1))
print("строгие:",len(s1),"| с цифрой+контекст:",len(s2),"| объединение:",len(s1|s2),"| пересечение:",len(s1&s2))
# --- 22 без кандидата: что в их строках
no cand=None
