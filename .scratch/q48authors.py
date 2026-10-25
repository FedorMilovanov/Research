import csv,re,json,pathlib,collections
SRC=pathlib.Path("/home/user/Research/.scratch/TCP.csv")
rows=list(csv.DictReader(SRC.open(encoding="utf-8-sig")))
print("записей в каталоге:",len(rows))
NAMES=["Preston, John","Tillotson, John","Whitefield, George","Wardlaw, Ralph","Nye, Philip",
       "Bradwardine","Zanchi, Girolamo","Alexander, Archibald","Prudentius","Prosper","Ratramnus","Haymo","Chillingworth","Williams, Daniel"]
def show(name):
    key=name.lower()
    hits=[r for r in rows if key in (r.get("Author") or "").lower()]
    print("\n### %s — записей по автору: %d" % (name,len(hits)))
    for r in hits[:14]:
        print("   %-9s %-8s %-6s %-14s %s" % (r["TCP"],r.get("EEBO"),r.get("Status"),(r.get("Date") or "")[:14],(r.get("Title") or "")[:110]))
    return hits
out={}
for n in NAMES:
    h=show(n)
    out[n]=[{"tcp":r["TCP"],"status":r.get("Status"),"date":r.get("Date"),"title":(r.get("Title") or "")[:200],"pages":r.get("Pages")} for r in h]
pathlib.Path("/home/user/Research/.scratch/q48authors.json").write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding="utf-8")
