import sys,re,json
sys.path.insert(0,"/home/user/Research/.scratch")
from q48lib import pages,ctx
CASES={
 "A16626":[r"constat deum nolle omnes salvari",r"pro omnibus vt saluentur",r"de omnibus pr[aæ]destinatis ad vitam",r"liber (primus|secundus|tertius|tertius)",r"caput \d+"],
 "A62570":[r"universal redemption",r"sincerity of god",r"offer to all",r"all men"],
 "A62579":[r"universal redemption",r"died for all",r"mercy of god",r"sufficien"],
 "N03645":[r"bishop of london",r"answer",r"all men",r"redemption"],
 "N03743":[r"christ died for all",r"universal redemption",r"all mankind",r"querists"],
 "A09997":[r"condition",r"all men",r"would have all",r"covenant"],
 "A15859":[r"equal love",r"love of god",r"all things which he has made",r"universal redemption"],
 "A12183":[r"all men",r"condition",r"promise",r"gospel"],
}
res={}
for tid,pats in CASES.items():
    P=pages(tid)
    print("\n=========",tid,"| страниц:",len(P))
    rr={}
    for p in pats:
        rx=re.compile(p,re.I); n=0; ex=[]
        for pg,(raw,nx,idx) in P.items():
            for m in rx.finditer(nx):
                n+=1
                if len(ex)<3: ex.append((pg,ctx(raw,idx,nx,m.start(),m.end(),pad=200)))
        rr[p]={"n":n,"ex":[{"page":a,"ctx":b} for a,b in ex]}
        print("  /%s/ → %d %s" % (p,n,("первые страницы: "+", ".join(a for a,_ in ex[:6])) if ex else ""))
    res[tid]=rr
pathlib=json.dumps
open("/home/user/Research/.scratch/q48scan.json","w",encoding="utf-8").write(json.dumps(res,ensure_ascii=False,indent=1))
