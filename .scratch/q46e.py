import re,pathlib,collections,json
ROOT=pathlib.Path("/home/user/Research")
REGNAME="35_four_point_authors_mass_registry.md"
t=(ROOT/"docs/research/atonement"/REGNAME).read_text()
q2row={}
for l in t.split("\n"):
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
SNAP=re.compile(r"`([a-z][a-z0-9]{6,20}\d{2}[a-z]{2,12})`")
DIG=re.compile(r"`([a-z][a-z0-9_\-]{6,}\d[a-z0-9_\-]{0,20})`")
ANY=re.compile(r"`([a-z][a-z0-9_\-]{7,})`")
ARCH=re.compile(r"archive\.org|ia\d{3,4}|_djvu\.txt",re.I)
lane=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REGNAME]
full=lane+[p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
def variants(perim):
    out={}
    txts={p:p.read_text() for p in perim}
    s1=set(); s1p=0
    for p,x in txts.items():
        f=set(SNAP.findall(x)); s1|=f; s1p+=len(f)
    out["SNAP уникальных"]=(len(s1),s1p)
    s2=set(); s2p=0
    for p,x in txts.items():
        f={m.group(1) for m in DIG.finditer(x) if ARCH.search(x[max(0,m.start()-200):m.end()+200])}
        s2|=f; s2p+=len(f)
    out["DIG+ARCH уникальных"]=(len(s2),s2p)
    u=s1|s2; up=sum(len(set(SNAP.findall(x))|set(m.group(1) for m in DIG.finditer(x) if ARCH.search(x[max(0,m.start()-200):m.end()+200]))) for x in txts.values())
    out["объединение уникальных"]=(len(u),up)
    s3=set()
    for p,x in txts.items():
        s3|={m.group(1) for m in ANY.finditer(x) if ARCH.search(x[max(0,m.start()-200):m.end()+200]) and re.search(r"\d",m.group(1))}
    out["ANY+цифра+контекст"]=(len(s3),sum(1 for x in txts.values() for m in ANY.finditer(x) if ARCH.search(x[max(0,m.start()-200):m.end()+200]) and re.search(r"\d",m.group(1))))
    return out
for name,per in [("лан (37 файлов)",lane),("периметр 122",full)]:
    print("==",name)
    for k,v in variants(per).items(): print("   %-24s уникальных %3d | пар объект-файл %3d"%(k,v[0],v[1]))
# --- пересечения классов
d=json.load(open(ROOT/".scratch/q46d.json"))
