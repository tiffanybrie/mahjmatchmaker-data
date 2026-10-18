from common import *
import prepatch as PP
import io,base64,hashlib,glob
from PIL import Image,ImageChops
rep=collections.Counter(); notes=collections.defaultdict(list)
H=json.load(open(REPO+'scripts/albumcard/holiday_manifest.json'))
MRJ=json.load(open(REPO+'config/mat-racks-picks.json'))
sets={s['slug']:s for s in D['sets']}
OLD={s['slug']:[list(x) for x in s['m']] for s in D['sets']}
oldrack={(s,x[0]):tuple(x[1]) for s in OLD for x in OLD[s]}
# ---------- tile slug -> FYM slug
T2S={s:s for s in sets}
T2S.update({'sunday':'sunday-mahjong-sunday','december-1994':'sunday-mahjong-december-1994','brownstone-bloom':'anders-ruff-brownstone-bloom',
 'papaya-spritz':'oh-my-mahjong-papaya-spritz','hummingbird':'sunday-mahjong-hummingbird','nature-walk':'sunday-mahjong-nature-walk','sunday-blues':'sunday-mahjong-sunday-blues'})
TILEKEYS=sorted(T2S,key=len,reverse=True)
# ---------- rack images / flags
RI=json.load(open(SP+'rackimg/rackimg_new.json'))
newIMG=dict(RI['img']); newIMG.update(PP.newIMGm)
for k,h in RI['map'].items(): R[k]['im']=h; rep['rack_img_replaced']+=1
ks=list(R)
HIDE=[20,66,95,96,100,108,111,306,328,5]
for i in HIDE: R[ks[i]]['hid']=1
WOODS={'bb:Weathered Oak','bb:Provincial','bb:Red Mahogany','bb:Dark Walnut'}
for w in WOODS:
    if w in R: R[w]['hid']=1
def small(k):
    r=R[k]; n=r['n']; b=r.get('bn','')
    return ('Oh My Mahjong' in b) or ('Mahjong Row' in b) or bool(re.search(r'18(\.5)?\s*(["”]|-?inch|in\b)',n,re.I))
for k in R:
    if small(k): R[k]['sm']=1
D['badges']={'mm:Hawksbill':'Best value in tortoise'}
LEAD=['peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4','vr:My Fair Mahjong:Transparent Clear','mm:Hawksbill']
D['uni']=LEAD+[u for u in D['uni'] if u not in LEAD]
# ---------- mat lookups
HBYF={}
for h in H: HBYF[h['file'].split('-mahjong-tiles-',1)[1]]=h
brands=sorted({M[i]['bn'] for i in M if M[i].get('bn')},key=len,reverse=True)
slug=lambda s: re.sub(r'[^a-z0-9]+','-',s.lower().replace("'",'').replace('’','').replace('&','and')).strip('-')
BSL=sorted([(slug(b),b) for b in brands]+[(slug(b).replace('-and-','-'),b) for b in brands],key=lambda x:-len(x[0]))
def mat_from_hol(h):
    mid=by_handle(h['mat'],h['brand'])
    if not mid: mid=best(re.sub(r'\(.*?\)','',h['matName']),h['brand'])
    return mid
def mat_from_rest(rest):
    rest=re.sub(r'(-v\d+)?\.jpg$','',rest)
    if rest+'.jpg' in HBYF: return mat_from_hol(HBYF[rest+'.jpg'])
    rest=rest.replace('let-s-be-besties','lets-be-besties')
    for bs,b in BSL:
        if rest.startswith(bs+'-'):
            mw=rest[len(bs)+1:]; mw=re.sub(r'-mat$','',mw)
            return best(mw.replace('-',' '),b) or by_handle(mw+'-mahjong-mat',b) or by_handle(mw+'-mat',b)
    return None
def parse_file(fn):
    b=os.path.basename(fn)
    if '-mahjong-tiles-' not in b or b.startswith('00-'): return None,None
    t,rest=b.split('-mahjong-tiles-',1); t=re.sub(r'^\d+-','',t)
    return T2S.get(t), rest
# ---------- rack lock tables
def rlist(names):
    out=[]
    for n in names:
        k=rres(n)
        if k: out.append(k)
        else: notes['rack_unresolved'].append(n)
    return out
TILE_LOCK={}
for h in H:
    s=T2S.get(h['tile'])
    if s and s not in TILE_LOCK: TILE_LOCK[s]=rlist(h['racks'])
MATLOCK={}
for k,v in MRJ.items():
    if isinstance(v,dict) and 'racks' in v and str(v.get('approved','')).startswith('2026'):
        bn=next((b for _,b in BSL if v['mat'].startswith(b)),None)
        mid=best(v['mat'][len(bn):] if bn else v['mat'],bn or '') if bn else None
        if not mid: mid=by_handle(k)
        if mid: MATLOCK[mid]=rlist(v['racks'])
        else: notes['registry_mat_unresolved'].append(v['mat'])
hp=collections.defaultdict(collections.Counter)
for h in H:
    mid=mat_from_hol(h)
    if mid and h.get('mat_picks'): hp[mid][tuple(h['mat_picks'])]+=1
for mid,c in hp.items():
    if mid not in MATLOCK: MATLOCK[mid]=rlist(c.most_common(1)[0][0])
# ---------- build her lists
HER=collections.defaultdict(list)   # slug -> [(mid, card_racks or None, src)]
def canon(s,mid):
    if not mid: return None
    mid=PP.REMAP.get(mid,mid)
    if M[mid].get('hid'): rep['her_dropped_crop_img']+=1; notes['her_dropped_crop_img'].append((s,M[mid]['n'],M[mid]['bn'])); return None
    hd=mid.split('/')[-1].split('?')[0]
    for o,_ in OLD.get(s,[]):
        oh=o.split('/')[-1].split('?')[0]
        if o!=mid and nb(M[o]['bn'])==nb(M[mid]['bn']) and (oh.startswith(hd) or hd.startswith(oh)) and len(min(oh,hd,key=len))>8: return o
    return mid
def add(s,mid,racks,src):
    mid=canon(s,mid)
    if not s or not mid: return
    if any(x[0]==mid for x in HER[s]): return
    HER[s].append((mid,racks,src))
HOLSETS={T2S[h['tile']] for h in H if h['hol'] and h['tile'] in T2S and T2S[h['tile']] in sets}-{'sunday-mahjong-december-1994'}
# 1a live albums: keep existing album order (from albums.json sync)
for s in sets:
    if s in HOLSETS: continue
    if sets[s].get('album') and OLD[s]:
        for mid,_ in OLD[s]: add(s,mid,None,'album')
# 1b holiday tile sets: holiday manifest order
for h in sorted(H,key=lambda h:h['order']):
    s=T2S.get(h['tile'])
    if s in HOLSETS: add(s,mat_from_hol(h),rlist(h['racks']+h.get('mat_picks',[])),'holiday')
# 1c almost-live albums
def man(p):
    m=json.load(open(REPO+f'assets/cards/{p}/manifest.json')); return m['cards'] if isinstance(m,dict) else m
def card_mid(c):
    a=PP.MALIAS.get((c['mat'].lower(),c['brand'].lower()))
    if a: return a
    hd=re.sub(r'^(shop|cc)-','',c.get('vote_id') or '')
    return by_handle(hd,c['brand']) or best(c['mat'],c['brand']) or mat_from_rest(c['file'].split('-mahjong-tiles-',1)[1])
for c in sorted(man('brownstone-bloom'),key=lambda c:c['order']):
    if 'el-tigre' in c['file']: continue
    mid=card_mid(c); 
    if not mid: notes['unmatched'].append(('brownstone',c['mat'],c['brand']))
    add('anders-ruff-brownstone-bloom',mid,rlist(c.get('racks') or [])+rlist(c.get('mat_racks') or []) or None,'almost-live')
sv=[os.path.basename(x) for x in json.load(open(SP+'shipdb/ship/c5-sunday.json'))['order']]
sun=man('sunday-tile-set'); pos={f:i for i,f in enumerate(sv)}
for c in sorted(sun,key=lambda c:pos.get(c['file'],500+c['order'])):
    mid=card_mid(c)
    if not mid: notes['unmatched'].append(('sunday',c['mat'],c['brand']))
    add('sunday-mahjong-sunday',mid,rlist((c.get('racks') or [])+(c.get('mat_racks') or [])),'almost-live')
for c in sorted(man('papaya-spritz'),key=lambda c:c['order']):
    mid=card_mid(c)
    if not mid: notes['unmatched'].append(('papaya',c['mat'],c['brand']))
    add('oh-my-mahjong-papaya-spritz',mid,rlist((c.get('racks') or [])+(c.get('mat_racks') or [])),'almost-live')
dec=[os.path.basename(x) for x in json.load(open(SP+'shipdb/ship/c5-dec1994.json'))['order'] if 'cover' not in x]
DECT=rlist(next(h['racks'] for h in H if h['tile']=='december-1994'))
for f in dec:
    rest=f.split('-mahjong-tiles-',1)[1]; h=HBYF.get(rest)
    mid=mat_from_rest(rest)
    if not mid: notes['unmatched'].append(('dec1994',rest))
    add('sunday-mahjong-december-1994',mid,DECT+(rlist(h.get('mat_picks',[])) if h else []),'holiday-album')
# 2 mat-specific / new card sets
EXTRA=['larkspur-v6','new-oct18','peony-and-parasol','malachite-new','polofix-v1','logofix-v2','spirit-of-christmas']
lk=[os.path.basename(x) for x in json.load(open(SP+'shipdb/ship/c5-larkspur.json'))['order']]
for d in EXTRA:
    fs=sorted(glob.glob(REPO+f'assets/cards/{d}/*.jpg'))
    for fn in fs:
        s,rest=parse_file(fn)
        if not s: rep['extra_no_set']+=1; continue
        mid=mat_from_rest(rest)
        if not mid: notes['unmatched'].append((d,os.path.basename(fn))); continue
        add(s,mid,None,d)
# 3 holiday album cards for non-holiday tile sets
for h in sorted(H,key=lambda h:h['order']):
    s=T2S.get(h['tile'])
    if s and s not in HOLSETS: add(s,mat_from_hol(h),rlist(h['racks']+h.get('mat_picks',[])),'holiday-album')
# ---------- pair-first
def pair(s,mid):
    S_=sets[s]; st=toks(S_['name'].split('(')[0]); mt=toks(M[mid]['n'])
    return st and st<=mt and nb(S_['maker'].split(' x ')[-1])==nb(M[mid]['bn'])
# ---------- racks + purge
OMMSET=lambda s: 'Oh My Mahjong' in sets[s]['maker'] or 'Mahjong Row' in sets[s]['maker']
removed=collections.Counter()
for s in sets:
    lst=HER.get(s,[])
    if s in HOLSETS: lst=[x for x in lst if pair(s,x[0])]+[x for x in lst if not pair(s,x[0])]
    newm=[]
    for mid,cr,src in lst:
        racks=list(dict.fromkeys((cr or [])+TILE_LOCK.get(s,[])+MATLOCK.get(mid,[])))
        keep=[]
        for r in racks:
            if r in WOODS: removed['bb_wood']+=1; continue
            if 'Oh My Mahjong' in R[r].get('bn','') and 'Oh My Mahjong' not in sets[s]['maker']: removed['omm_on_non_omm']+=1; continue
            if R[r].get('sm') and not OMMSET(s): removed['small_on_large']+=1; continue
            keep.append(r)
        newm.append([mid,keep])
    old=oldrack; 
    for mid,keep in newm:
        if (s,mid) in old and tuple(old[(s,mid)])!=tuple(keep): rep['combo_racks_changed']+=1
        if (s,mid) not in old: rep['her_added']+=1
    for mid,_ in OLD[s]:
        if mid not in [x[0] for x in newm]: rep['her_removed']+=1; notes['her_removed'].append((s,mid))
    sets[s]['m']=newm
    if newm and sets[s].get('cat'): sets[s].pop('cat',None); rep['cat_cleared']+=1
rep.update({'rack_'+k:v for k,v in removed.items()})
# ---------- ranks
oi={m:i for i,m in enumerate(D['order'])}
for s in D['sets']:
    herix=[oi[x[0]] for x in s['m'] if x[0] in oi]
    hs=set(herix); s['rank']=herix+[i for i in s['rank'] if i not in hs]
json.dump(D,open('D_patched.json','w')); json.dump(newIMG,open('newIMG.json','w')); json.dump(PP.newMC,open('newMC.json','w'))
json.dump({'rep':rep,'notes':notes},open('report_data.json','w'),indent=1,default=list)
print(dict(rep)); 
for k,v in notes.items(): print(k,len(v),v[:40])
