import sys,pathlib,re
sys.path.insert(0,"/home/user/Research/.scratch")
from q48lib import pages,ctx
CASES=[("A97309",[r"l[ou]es not all things",r"with an equal l[ou]e",r"l[ou]es all things which he has made",r"equal l[ou]e",r"of the l[ou]e of god",r"l[ou]e of god"]),
       ("A16626",[r"pro c[ou]mbus omnibus",r"mort[uu]s est pro",r"pro multis",r"dedit semetipsum"])]
for tid,pats in CASES:
    P=pages(tid)
    print("\n===",tid,"| страниц в карте:",len(P))
    for p in pats:
        r=re.compile(p,re.I); n=0; where=[]
        for pg,(raw,nx,idx) in P.items():
            for m in r.finditer(nx):
                n+=1
                if len(where)<5: where.append((pg,ctx(raw,idx,nx,m.start(),m.end())))
        print("  /%s/ → %d" % (p,n))
        for pg,c in where[:3]:
            print("      с. %s : %s" % (pg,c[:300].replace("\n"," ")))
