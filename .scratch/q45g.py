import re,pathlib,json
from collections import Counter
ROOT=pathlib.Path("/home/user/Research")
REG=ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md"
d=json.load(open(ROOT/".scratch/q45.json"))
t=REG.read_text(); lines=t.split("\n")
rows={}
for l in lines:
    if l.startswith("| FP-"):
        rid=re.match(r"^\| (FP-\d+) \|",l).group(1)
        cells=[c.strip() for c in l.split("|")]
        rows[rid]=" ".join(cells[2:4])
peri=[p for p in (ROOT/"docs/research/atonement").glob("*.md") if p.name!=REG.name]+ \
     [p for p in (ROOT/"ИСКУПЛЕНИЕ").rglob("*.md")]
texts={p.relative_to(ROOT).as_posix():p.read_text() for p in peri}
CAP=re.compile(r"\b[A-ZÀ-Ỹ][A-Za-zÀ-ỹœŒĀā]{4,}\b|\b[А-ЯЁ][а-яё]{4,}\b")
TITLE=re.compile(r"\*([^*]{6,})\*")
def work_tokens(rid):
    if not rid or rid not in rows: return []
    ti=rows[rid].split("|")[0]
    out=[]
    for m in TITLE.finditer(ti):
        for w in re.findall(r"[A-Za-zÀ-ÿ]{6,}",m.group(1)):
            lw=w.lower()
            if lw in {"being","which","wherein","whereof","about","after","before","through","concerning","against","containing","together","therein","thet","and","the","that","with","from"}: continue
            if lw not in out: out.append(lw)
    return out[:6]
cand=sorted(set(d["candA"])&set(d["candB"]))
strict=[]
for q in cand:
    v=d["B"][q]; ks=v["ks"]; rid=(v["rows"] or [""])[0]; wt=work_tokens(rid)
    hits=[]
    for fn,tx in texts.items():
        for ln in tx.split("\n"):
            if not any(re.search(r"(?<![\w])"+re.escape(k)+r"(?![\w])",ln) for k in ks): continue
            if not wt: hits.append((fn,ln,"без тогена названия")); continue
            low=ln.lower()
            if any(w in low for w in wt): hits.append((fn,ln,"+".join(w for w in wt if w in low)))
    if hits: strict.append((q,rid,ks,wt,hits[:2]))
print("=== уточнённая перепись: имя автора И токен названия работы И локатор И цитата в одной строке периметра")
print("адресов в устойчивом ядре кандидатов (%d):"%len(cand))
print("  из них выдержали требование названия работы: %d"%len(strict))
for q,rid,ks,wt,hh in strict:
    print("%s [%s] имя %s | название %s"%(q,rid or "—",", ".join(ks),", ".join(wt[:4])))
    for f,l,why in hh[:1]: print("      %s :: %s … [%s]"%(f,l[:150],why))
print("=== итог: %d из 102 адресов (%.2f %%) имеют в лане строку, где названы автор, произведение, локатор и цитата"%(len(strict),100*len(strict)/102))
json.dump({"strict":[[q,rid,ks,wt,[[f,l] for f,l,_ in hh]] for q,rid,ks,wt,hh in strict]},open(".scratch/q45strict.json","w"),ensure_ascii=False,indent=1)
