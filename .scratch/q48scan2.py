import sys,re,json
sys.path.insert(0,"/home/user/Research/.scratch")
from q48lib import pages,ctx
def flex(s):
    out=[]
    for ch in s.lower():
        if ch in "uv": out.append("[uv]")
        elif ch.isalnum(): out.append(re.escape(ch))
        else:
            if out and out[-1]=="\\W*": continue
            out.append("\\W*")
    s="".join(out)
    return re.sub(r"^(\W\*)+","",s)
CASES={
 "N03743":["universal redemption","all mankind","died for all","sufficient","election"],
 "A09997":["all men","condition","could not choose","believe","covenant"],
 "A62570":["sincerity","offer to all","will have all men","1 tim","all men to be sa"],
 "A62579":["mercy of god","died for all","all men","sufficien","reward"],
 "A15859":["love of god","equal love","all things","redemption","predestin"],
 "A12183":["all men","condition","promise","free"],
}
res={}
for tid,ps in CASES.items():
    P=pages(tid)
    print("\n=========",tid)
    for p in ps:
        rx=re.compile(flex(p),re.I); n=0; ex=[]
        for pg,(raw,nx,idx) in P.items():
            for m in rx.finditer(nx):
                n+=1
                if len(ex)<4: ex.append((pg,ctx(raw,idx,nx,m.start(),m.end(),pad=230)))
        print("  /%s/ → %d" % (p,n))
        for pg,c in ex[:2]:
            print("      с. %s : %s" % (pg,re.sub(r"\s+"," ",c)[:430]))
        res.setdefault(tid,{})[p]={"n":n,"ex":[{"page":a,"ctx":b} for a,b in ex]}
json.dump(res,open("/home/user/Research/.scratch/q48scan2.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
