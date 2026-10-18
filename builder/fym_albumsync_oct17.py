import json,re,collections,os,io,base64,hashlib,urllib.request
from PIL import Image
D=json.load(open('D.json')); M=D['mats']; R=D['racks']
A=json.load(open('/home/claude/mahjmatchmaker-data/work/albums.json')); L=A if isinstance(A,list) else list(A.values())
REPO='/home/claude/mahjmatchmaker-data/'
STOP={'mat','mahjong','the','and','with','rules','edition','w','playing','american','neoprene','retired','mahj','game','classic','tdt','copy','pre','order','new','premium','a'}
def toks(s): s=re.sub(r'\(.*?\)|\[.*?\]',' ',s.lower()).replace('&',' and ').replace("'",'').replace('’',''); return set(t for t in re.findall(r"[a-z0-9']+",s) if t not in STOP)
def nb(s): return re.sub(r'[^a-z]','',s.lower().replace('holiday','').replace('mahjongg','').replace('mahjong','').replace('mahj','').replace('co.','').replace('&','and'))
byb=collections.defaultdict(list)
for i,m in M.items(): byb[nb(m['bn'])].append(i)
ABB={'lt':'light'}
ALIAS={'birdie g':'Birdie Green','birdie p':'Birdie Pink'}
def T2(x): return set(ABB.get(t,t) for t in toks(x))
def best(mat,brand):
    bt=T2(mat)
    if not bt: return None
    cands=byb.get(nb(brand)) or [i for i in M if nb(brand)[:5] and nb(brand)[:5] in nb(M[i]['bn'])]
    full=[]
    for i in cands:
        nm=T2(M[i]['n']); sg=T2(i.split('/')[-1].split('?')[0].replace('-',' '))
        if bt<=nm: full.append((0,len(nm-bt),' '.join(sorted(nm)),i))
        elif (not nm or nm<=STOP) and bt<=sg: full.append((1,len(sg-bt),i,i))
        elif bt<=(nm|sg) and len(bt)>1: full.append((2,len((nm|sg)-bt),i,i))
    if not full: return None
    full.sort()
    a=full[0]
    if len(full)>1:
        b=full[1]
        if (a[0],a[1])==(b[0],b[1]) and a[2]!=b[2]: return None
        if a[0]==0 and a[1]>0 and len(bt)==1 and b[0]==0: return None
    return a[3]
def rid(url,name):
    u=re.sub(r'^https?://','',url or '').split('?')[0].replace('/products/','/').rstrip('/')
    if u in R: return u
    for k in R:
        if k.split('?')[0]==u: return k
    m=re.match(r'Bird & Bamboo (.+)',name or '')
    if m and 'bb:'+m.group(1) in R: return 'bb:'+m.group(1)
    for k,r in R.items():
        if r['n'].lower()==(name or '').lower(): return k
    return None
# --- new mat entries for album mats missing from FYM
newm={}; newimg={}; nextf=max(int(m['f'].split('/')[1].split('.')[0]) for m in M.values())+1
def famof(rgb):
    import colorsys
    r,g,b=[x/255 for x in rgb]; h,l,s=colorsys.rgb_to_hls(r,g,b); h*=360
    if l<0.22: return 'dark'
    if s<0.18 or (l>0.85 and s<0.4): return 'neutral'
    if h<15 or h>=345: return 'red' if l<0.6 else 'pink'
    if h<40: return 'orange'
    if h<65: return 'yellow'
    if h<170: return 'green'
    if h<255: return 'blue'
    if h<300: return 'purple'
    return 'pink'
def colors(im):
    q=im.convert('RGB').resize((120,120)).quantize(6); pal=q.getpalette(); cnt=sorted(q.getcolors(),reverse=True)
    tot=sum(c for c,_ in cnt); ms=[];fam=[]
    for c,ix in cnt[:5]:
        rgb=pal[ix*3:ix*3+3]; ms.append(['#%02x%02x%02x'%tuple(rgb),round(c/tot,2)])
        f=famof(rgb)
        if f not in fam and c/tot>0.08: fam.append(f)
    return ms,fam[:3]
CLEAN={'heaven scent':'assets/mats/clean/heaven-scent-2-birdsong.png','duck camp':'assets/mats/clean/duck-camp-mahjong-moxie.png','evergreen':'assets/mats/clean/evergreen-that-mahjong-moment.png'}
def card_img(url):
    fn='cardcache/'+hashlib.md5(url.encode()).hexdigest()+'.jpg'
    os.makedirs('cardcache',exist_ok=True)
    if not os.path.exists(fn): urllib.request.urlretrieve(url+'?format=1000w',fn)
    return Image.open(fn)
def make_mat(c,set_slug):
    key=(c['mat'].lower(),nb(c['brand']))
    if key in newm: return newm[key]
    src=CLEAN.get(c['mat'].lower())
    if src: im=Image.open(REPO+src).convert('RGB')
    else:
        im=card_img(c['img']).convert('RGB'); W,H=im.size; s=int(W*0.5); y0=int(H*0.09)
        im=im.crop((0,y0,s,y0+s))
    full=im.copy(); full.thumbnail((640,640))
    b=io.BytesIO(); full.save(b,'WEBP',quality=80); fdata='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    th=im.copy(); th.thumbnail((180,180)); b=io.BytesIO(); th.save(b,'JPEG',quality=72); tdata='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    global nextf
    f='m/%d.webp'%nextf; nextf+=1; h=hashlib.md5(tdata.encode()).hexdigest()[:10]
    ms,mf=colors(im)
    mid='alb2:'+re.sub(r'[^a-z0-9]+','-',(c['brand']+' '+c['mat']).lower()).strip('-')
    M[mid]={'n':c['mat']+(' (retired)' if c.get('retired') else ''),'bn':c['brand'],'b':c['brand'],'u':c.get('shop') or '','dc':'','pa':False,'nc':False,'rt':False,'c':False,'ml':True,'f':f,'th':h,'w':full.size[0],'h':full.size[1],'mf':mf or ['neutral'],'ms':ms,'hol':False,'src':'album-card' if not src else 'clean'}
    newimg[f]=fdata; newimg['TH:'+h]=tdata; newm[key]=mid; return mid
sets={s['slug']:s for s in D['sets']}
report=collections.Counter(); order_add=[]
for a in L:
    sl=a['slug'].replace('-mahjong-tile-matches','')
    s=sets.get(sl)
    if not s: report['album_without_set']+=1; continue
    oldm={x[0]:x[1] for x in s['m']}
    newlist=[]; seen=set()
    for c in a['cards']:
        c=dict(c,mat=ALIAS.get(c['mat'].lower(),c['mat']))
        mid=best(c['mat'],c['brand'])
        if not mid:
            bt=T2(c['mat'])
            for k in oldm:
                if nb(M[k]['bn'])==nb(c['brand']) and bt and bt<=(T2(M[k]['n'])|T2(k.split('/')[-1].replace('-',' '))): mid=k; report['reused_old']+=1; break
        if not mid: mid=make_mat(c,sl); report['new_mat_cards']+=1
        if mid in seen: continue
        seen.add(mid)
        racks=oldm.get(mid)
        if racks is None:
            racks=[r for r in (rid(u,n) for u,n in (c.get('racks') or [])) if r]
            report['added_pairs']+=1
        newlist.append([mid,racks])
    report['removed_pairs']+=len([k for k in oldm if k not in seen])
    s['m']=newlist
# order + ranks
for mid in M:
    if mid not in D['order']: D['order'].append(mid)
oi={m:i for i,m in enumerate(D['order'])}
for s in D['sets']:
    herix=[oi[x[0]] for x in s['m']]
    rest=[i for i in s['rank'] if i not in set(herix)]
    allix=set(herix)|set(rest)
    rest+= [i for i in range(len(D['order'])) if i not in allix]
    s['rank']=herix+rest
json.dump(D,open('D_new.json','w'))
json.dump(newimg,open('newimg.json','w'))
print(dict(report)); print('new mats',len(newm)); print(sorted(newm.values()))
