import json,re,collections,os
REPO='/home/claude/mahjmatchmaker-data/'
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
def loadD(path=SP+'fymaudit/index.html'):
    h=open(path).read(); i=h.index('const D=')+8; j=h.index('\n',i)
    s=h[i:j].rstrip(); assert s.endswith(';'); return json.loads(s[:-1]),h,i,j
D,HTML,I0,J0=loadD(); M=D['mats']; R=D['racks']
STOP={'mat','mahjong','the','and','with','rules','edition','w','playing','american','neoprene','retired','mahj','game','classic','tdt','copy','pre','order','new','premium','a'}
def toks(s): s=re.sub(r'\(.*?\)|\[.*?\]',' ',s.lower()).replace('&',' and ').replace("'",'').replace('’',''); return set(t for t in re.findall(r"[a-z0-9']+",s) if t not in STOP)
def nb(s): return re.sub(r'[^a-z]','',s.lower().replace('holiday','').replace('mahjongg','').replace('mahjong','').replace('mahj','').replace('co.','').replace('&','and'))
byb=collections.defaultdict(list)
for i,m in M.items(): byb[nb(m['bn'])].append(i)
def best(mat,brand):
    bt=toks(mat)
    if not bt: return None
    cands=byb.get(nb(brand)) or [i for i in M if nb(brand)[:5] and nb(brand)[:5] in nb(M[i]['bn'])]
    full=[]
    for i in cands:
        nm=toks(M[i]['n']); sg=toks(i.split('/')[-1].split('?')[0].replace('-',' '))
        if bt<=nm: full.append((0,len(nm-bt),' '.join(sorted(nm)),i))
        elif (not nm or nm<=STOP) and bt<=sg: full.append((1,len(sg-bt),i,i))
        elif bt<=(nm|sg) and len(bt)>1: full.append((2,len((nm|sg)-bt),i,i))
    if not full: return None
    full.sort(); a=full[0]
    if len(full)>1:
        b=full[1]
        if (a[0],a[1])==(b[0],b[1]) and a[2]!=b[2]: return None
        if a[0]==0 and a[1]>0 and len(bt)==1 and b[0]==0: return None
    return a[3]
byhandle=collections.defaultdict(list)
for i in M: byhandle[i.split('/')[-1].split('?')[0]].append(i)
def by_handle(hd,brand=None):
    c=byhandle.get(hd,[])
    if brand and len(c)>1: c=[i for i in c if nb(M[i]['bn'])==nb(brand)] or c
    return c[0] if c else None
RALIAS={'middle & main milk glass scalloped acrylic':'www.middleandmainmahjong.com/milk-glass-collection-mahjong-rack-and-pusher-set-of-4',
 'middle & main hawksbill heritage tortoise':'mm:Hawksbill','middle & main hawksbill tortoise':'mm:Hawksbill',
 'mahjong row & co. scalloped tortoise':'mahjongrowandco.com/scalloped-deluxe-tortoise-rack',
 'sunday mahjong cola':'sundaymahjong.com/sunday-cola-mahjong-rack-set',
 'peace love mahjong acrylic burl':'peace love mahjong acrylic burlwood',
 'miss mahjong scalloped iridescent opal':'missmahjong.com/iridescent-opal-scalloped-acrylic-racks',
 'miss mahjong blonde tortoise & brass':'missmahjong.com/blonde-tortoise-and-brass-acrylic-racks',
 'middle & main white lace':'www.middleandmainmahjong.com/blue-and-white-chinoiserie-mahjong-rack-and-pusher-set-of-4-copy',
 'middle & main white lace acrylic':'www.middleandmainmahjong.com/blue-and-white-chinoiserie-mahjong-rack-and-pusher-set-of-4-copy',
 'miss mahjong brass & tortoise':'missmahjong.com/dark-tortoise-and-brass-acrylic-racks',
 'oh my mahjong white':'www.ohmymahjong.com/white-rack-pusher','oh my mahjong white acrylic':'www.ohmymahjong.com/white-rack-pusher',
}
byname={v['n'].lower():k for k,v in R.items()}
def rres(n):
    if n in R: return n
    m=re.match(r'Bird & Bamboo (.+)',n)
    if m and 'bb:'+m.group(1) in R: return 'bb:'+m.group(1)
    a=RALIAS.get(n.lower(),n.lower())
    if a in R: return a
    return byname.get(a)
