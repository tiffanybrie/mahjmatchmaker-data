import json,math,sys
L=json.load(open('trim/list.json'))
BX0,BY0,BW,BH=56,222,968,996
GX,GY=24,22
EXP=0.42
BOOST={"The Royal Mahjong Society":1.5,"Soirée All Day":1.4,"Noli June":1.2,"Amanda Toppe":1.3,"Wren Mats":1.1,"Bespoke Mahjong":1.3,
"Mahj & Vine":1.1,"I Love Mahj":0.8,"Middle & Main Mahjong":1.05,"Mahjong Studios":0.9,"Miss Mahjong":1.15,"Peace Love Mahjong":1.35,"Splash of Color":1.1,"Hip Hip Mahjong":1.05,
"Bird & Bamboo":1.2,"Mahj Mood":1.2,"Mahjong Co.":1.15,"Virora Mahjong":1.05}
def nat(e,base):
    ar=e['w']/e['h']; h=base*e['weight']*BOOST.get(e['brand'],1)/(ar**EXP); return h*ar,h
def layout(base):
    n=len(L); W=[nat(e,base) for e in L]
    # DP over breakpoints: cost = (BW - rowwidth)^2, rows overfull allowed up to 8% (they get scaled down)
    INF=1e18; best=[INF]*(n+1); prev=[0]*(n+1); best[0]=0
    for j in range(1,n+1):
        for i in range(j-1,-1,-1):
            k=j-i; w=sum(W[t][0] for t in range(i,j))+GX*(k-1)
            if w>BW*1.12 and k>1: break
            c=(BW-w)**2
            if j==n and w<BW: c*=0.15
            if best[i]+c<best[j]: best[j]=best[i]+c; prev[j]=i
    if best[n]>=INF: return [],1e9,0
    br=[];j=n
    while j>0: br.append((prev[j],j)); j=prev[j]
    br.reverse()
    out=[];y=0
    for (i,j) in br:
        r=[[L[t],*W[t]] for t in range(i,j)]
        gaps=GX*(len(r)-1); ws=sum(x[1] for x in r)
        sc=min((BW-gaps)/ws,1.7)
        for x in r: x[1]*=sc;x[2]*=sc
        rh=max(x[2] for x in r); tw=sum(x[1] for x in r)+gaps
        xx=(BW-tw)/2
        for e,w,h in r: out.append((e,xx,y+(rh-h)/2,w,h)); xx+=w+GX
        y+=rh+GY
    return out,y-GY,len(br)
best=None
for ex in [0.32,0.36,0.40,0.44,0.48,0.52]:
  EXP=ex
  b=40.0
  while b<200:
    it,H,nr_=layout(b)
    if H<=BH and it:
        # score: smallest logo matters most (readability), then total area
        mn=sorted(math.sqrt(w*h) for e,x,y,w,h in it)[:6]
        score=sum(mn)*3+math.sqrt(sum(w*h for e,x,y,w,h in it))
        if not best or score>best[0]: best=(score,b,it,H,nr_,ex)
    b+=0.25
_,lo,items,H,nr,EXP=best
print('EXP',EXP)
nrows=len(set(round(y) for e,x,y,w,h in items))
off=(BH-H)/2
# group rows by row index via y-top of row band: recompute bands
rows={}
for it in items:
    e,x,y,w,h=it; rows.setdefault(round(y+h/2),[]).append(it)
keys=sorted(rows); nb=len(keys)
extra=(BH-H)/(nb+1) if nb>0 else 0
new=[]
for i,k in enumerate(keys):
    for e,x,y,w,h in rows[k]: new.append((e,x,y+extra*(i+1)-(BH-H)/2,w,h))
items=new
json.dump([{'file':e['file'],'brand':e['brand'],'x':BX0+x,'y':BY0+off+y,'w':w,'h':h} for e,x,y,w,h in items],open('placed.json','w'))
print('base',round(lo,1),'H',round(H),'rows',nr, 'minh',round(min(h for *_,h in items)), 'minw',round(min(w for e,x,y,w,h in items)))
