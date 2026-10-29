import json,re,sys,math
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/colors'); import matcolors as mc
R='/home/claude/mahjmatchmaker-data/'
M=json.load(open('mats.json'))
CC=json.load(open(R+'config/colorcards.json'))['sets']
SK=json.load(open(R+'tiffany-skip-list.json'))['mats']; skh={x.get('handle') for x in SK}
EXCL=re.compile(r"travel|\bmini\b|mini-|starter|\bkit\b|bundle|caddy|desk mat|desk\b|table cover|foldable|solo play|\bpool\b|logo mat|art print|\btube only|\bbag\b|pet mat|bath mat|needlepoint|\bcanvas\b|coaster|placemat",re.I)
HOL=re.compile(r"christmas|xmas|holly|yuletide|merriment|winterberry|nutcracker|sugarplum|\bclara\b|santa|noel|jingle|candy cane|\bcane mat|winter wonderland|mistletoe|reindeer|snowflake|halloween|o-ween|\bween\b|spooky|pumpkin|witch|valentine|easter|hanukkah",re.I)
def lab(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: ((c+0.055)/1.055)**2.4 if c>0.04045 else c/12.92
    r,g,b=f(r),f(g),f(b); X=(r*.4124+g*.3576+b*.1805)/.95047; Y=r*.2126+g*.7152+b*.0722; Z=(r*.0193+g*.1192+b*.9505)/1.08883
    t=lambda v: v**(1/3) if v>0.008856 else 7.787*v+16/116
    return (116*t(Y)-16, 500*(t(X)-t(Y)), 200*(t(Y)-t(Z)))
dE=lambda a,b: math.dist(a,b)
TONE={'nature-walk':'earthy','sunday-blues':'transitional','plum-panda':'transitional','hummingbird':'transitional'}
def ok(k,m):
    if m.get('hid') or m.get('hol') or m.get('rt'): return False
    if k.startswith(('alb:','alb2:','md-')): return False
    if m['bn'] in ('Mahjong Studios','Splash of Color'): return False
    if re.search('paige spearin',m['n']+k,re.I): return False
    if EXCL.search(m['n']) or HOL.search(m['n']): return False
    if k.split('/')[-1].split('?')[0] in skh: return False
    return True
def score(setid,k,m):
    c=CC[setid]; back=[lab(x[1]) for x in c['backs'] if 'IVORY' not in x[0]]; ivory=[lab(x[1]) for x in c['backs'] if 'IVORY' in x[0]]
    faces=[lab(x[1]) for x in c['faces']]; P=[(p,1.0) for p in back]+[(p,0.85) for p in faces]+[(p,0.55) for p in ivory]
    sc=0; bk=0; off=0; cov={}
    for h,sh in m.get('ms') or []:
        L=lab(h); sims=[(max(0,1-dE(L,p)/38)*w,j) for j,(p,w) in enumerate(P)]; best,j=max(sims); sc+=sh*best
        if best>0.45 and j<len(back)+len(faces): cov[j]=cov.get(j,0)+sh
        if back and min(dE(L,p) for p in back)<22: bk+=sh
        if best<0.15 and (abs(L[1])+abs(L[2]))>25: off+=sh   # strong colour the set doesn't have
    rec=mc.get(k) or {}; tone=rec.get('tone')
    if TONE[setid]=='earthy' and tone in ('bright','pastel'): return None
    nc=sum(1 for v in cov.values() if v>=0.04); s=sc+0.6*min(bk,0.4)-0.5*off+0.12*max(0,nc-1)+(0.04 if tone=='blend' else 0)
    solid=max([sh for h,sh in (m.get('ms') or [])]+[0])>0.6
    return (round(s,4),solid)
if __name__=='__main__':
    out={}
    for sid in CC:
        if sid not in TONE: continue
        L=[(score(sid,k,m),k) for k,m in M.items() if ok(k,m)]
        L=sorted([(x[0][0],x[0][1],x[1]) for x in L if x[0] is not None],reverse=True)
        sol=0;LL=[]
        for sc_,so,k in L:
            if so:
                sol+=1
                if sol>8: continue
            LL.append((sc_,k))
        L=LL
        out[sid]=L[:160]
        print(sid,len(L),[ (s,M[k]['n'],M[k]['bn']) for s,k in L[:12]])
    json.dump(out,open('ranked.json','w'))
