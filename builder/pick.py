import json,re
d=json.load(open('/home/claude/mahjmatchmaker-data/data.json'))
T,M,X,R=d['T'],d['M'],d['X'],d['R']
want=['amara','gatsby','heritage-2-0','drake','lagoon','seabreeze','talulah','willow','cypress-forest','solara','coquette','emerald','gemma','glow-wild','jasmine','la-fete','luminaire','moonlight','nantucket','osler','palm-royale','pearlescent','pippa','sierra','smith','tortoise','jade','malachite','birdie','dandy','glitterville','limoncello','lola','sorbet','sunset','taylor']
OVR={'jade':'https://missmahjong.com/products/miss-classic-mahjong-tile-set','malachite':'https://missmahjong.com/products/miss-classic-malachite-mahjong-tile-set'}
RET={'birdie','dandy','glitterville','limoncello','lola','sorbet','sunset','taylor'}
out=[];prods={}
def key(url):
    m=re.match(r'https?://([^/]+)/products/([^/?#]+)',url or '')
    return (m.group(1),m.group(2)) if m else None
def add(url,kind,name):
    k=key(url)
    if not k: return None
    pid=k[0]+'/'+k[1]
    prods.setdefault(pid,dict(domain=k[0],handle=k[1],kind=kind,name=name))
    return pid
for slug in want:
    ti=next(i for i,t in enumerate(T) if t[0]==slug)
    t=T[ti]
    tp=('ret:'+slug) if slug in RET else add(OVR.get(slug,t[4]),'tile',t[1])
    xs=sorted([x for x in X if x[0]==ti],key=lambda x:x[5])[:7]
    ms=[]
    for x in xs:
        m=M[x[1]]
        mp=add(m[2],'mat',m[0])
        rp=[add(R[r][1],'rack',R[r][0]) for r in x[4][:3]]
        ms.append(dict(mat=mp,matName=m[0],brand=m[1],retired=m[3],racks=[r for r in rp if r],take=x[3][:240],n=x[5]))
    out.append(dict(slug=slug,name=t[1],maker=t[2],tile=tp,matches=ms))
json.dump(dict(sets=out,prods=prods),open('/tmp/mb/plan.json','w'),indent=1)
print(len(out),'sets',len(prods),'products',sum(1 for p in prods.values() if p['kind']=='mat'),'mats',sum(1 for p in prods.values() if p['kind']=='rack'),'racks')
for s in out: print(s['name'],s['tile'],len(s['matches']))
