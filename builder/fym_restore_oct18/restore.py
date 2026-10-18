# Restore Tiffany's matches dropped by the Oct 18 card-crop hide. Base = live FYM index.html.
import json,os,re,io,base64,hashlib,collections,colorsys,sys
from PIL import Image
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
REPO='/home/claude/mahjmatchmaker-data/'
FR=SP+'fymrestore/'; DL=FR+'dl/'; OUT=FR+'build/'
os.makedirs(OUT+'mc',exist_ok=True)
def ldD(p):
    h=open(p).read(); i=h.index('const D=')+8; j=h.index('\n',i); return json.loads(h[i:j].rstrip()[:-1]),h,i,j
D,HTML,I0,J0=ldD(FR+'live/index.html'); M=D['mats']; R=D['racks']; sets={s['slug']:s for s in D['sets']}
OLDD,_,_,_=ldD(SP+'fymaudit/index.bak_pre_fix_oct18_0820.html')
OLD={s['slug']:[list(x) for x in s['m']] for s in OLDD['sets']}
rep=collections.Counter(); log=collections.defaultdict(list)
# ---------------- images
nextf=max(int(m['f'].split('/')[1].split('.')[0]) for m in M.values())+1
newMC={}; newIMG={}
def famof(rgb):
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
def load(path,crop=None):
    im=Image.open(path)
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA'); bb=im.getbbox(); im=im.crop(bb) if bb else im
        bg=Image.new('RGB',im.size,(255,255,255)); bg.paste(im,mask=im.split()[3]); im=bg
    im=im.convert('RGB')
    if crop: im=im.crop(crop)
    return im
def setimg(mid,path,crop=None):
    global nextf
    im=load(path,crop); full=im.copy(); full.thumbnail((900,900))
    b=io.BytesIO(); full.save(b,'WEBP',quality=80); f='m/%d.webp'%nextf; nextf+=1
    newMC[f]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    th=im.copy(); th.thumbnail((180,180)); b=io.BytesIO(); th.save(b,'JPEG',quality=74)
    t='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(); h='mt'+hashlib.md5(t.encode()).hexdigest()[:8]
    newIMG[h]=t; m=M[mid]; m['f']=f; m['th']=h; m['w'],m['h']=full.size; m['c']=False
    m['ms'],mf=colors(im); m['mf']=mf or ['neutral']; m['src']='clean'; m.pop('hid',None)
def setrack(rid,path,crop=None):
    im=load(path,crop); im.thumbnail((640,640)); b=io.BytesIO(); im.save(b,'JPEG',quality=80)
    t='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(); h='rk'+hashlib.md5(t.encode()).hexdigest()[:8]
    newIMG[h]=t; R[rid]['im']=h; R[rid]['c']=False; R[rid].pop('hid',None); rep['rack_restored']+=1; log['racks'].append(R[rid]['n'])
OMMDC='https://mahjmatchmaker.com/oh-my-mahjong-discount-code'
# 1. hidden album-card mats that get a clean brand photo
CLEAN={
 'alb2:bespoke-mahjong-jungle-hot-pink':(DL+'jungle_1.jpg',None,{}),
 'alb2:bespoke-mahjong-cranes-and-clouds':('/tmp/mb/img/www.bespokemahjong.com__cranes-and-clouds.jpg',None,{}),
 'alb2:tigre-de-tartan-strawberry':(DL+'tdtstraw_0.jpg',None,{}),
 'alb2:tigre-de-tartan-coconut-peony':(DL+'tdtcoco_0.jpg',None,{}),
 'alb2:tigre-de-tartan-pop-art-roses':(DL+'tdtpop_1.jpg',None,{}),
 'alb2:oh-my-mahjong-regal-bloom':(DL+'regal_crop.png',None,{}),
 'alb2:mahj-tile-haus-imperial-lotus':(DL+'implotus_0.jpg',None,{'u':'https://mahjtilehaus.com/products/imperial-lotus-mat'}),
 'alb2:sweet-jojo-designs-boho-wildflower':(DL+'boho_0.jpg',(0,60,735,840),{}),
 'alb2:isabel-harte-isabel-harte':(REPO+'assets/mats/other/isabel-harte-bamboo-dragon.jpg',None,{'n':'Bamboo Dragon','u':'https://isabelharte.com/products/cushioned-mahjong-mat-for-card-table'}),
 'alb2:mary-benson-mary-benson':(DL+'mb_mahjong-ma_0.jpg',None,{'n':'Blooming Tulips','u':'https://marybensonart.com/products/mahjong-mat-winter-preorder'}),
}
for mid,(p,crop,upd) in CLEAN.items():
    setimg(mid,p,crop); M[mid].update(upd); rep['mat_clean_photo']+=1; log['mats_clean'].append(M[mid]['n']+' · '+M[mid]['bn'])
# 2. hidden album-card mats that are the same product as a catalog mat already in FYM
REMAP={'alb2:bam-bird-boutique-classic-neoprene-in-pink':'www.bambirdboutique.com/classic-neoprene-mahjong-mat-copy',
 'alb2:mahj-moon-pink-citrus-chinoiserie':'mahjandmoon.com/pink-lemon-blossom-mahjong-mat',
 'alb2:bespoke-mahjong-yotd-purple':'www.bespokemahjong.com/year-of-the-dragon-mat-plum',
 'alb2:mahj-vine-chinoiserie':'mahjandvine.com/chinoiserie-song-bird',
 'alb2:mahj-vine-chinoiserie-songbird-2':'mahjandvine.com/chinoiserie-song-bird','alb2:oh-my-mahjong-lorelei-2':'www.ohmymahjong.com/lorelei-mat',
 'alb2:oh-my-mahjong-serengeti-2':'alb:amara:Serengeti','alb2:oh-my-mahjong-enchanted-2':'alb:amara:Enchanted'}
# 3. new mats
def newmat(mid,n,bn,u,dc,path,hol=False,crop=None):
    M[mid]={'n':n,'bn':bn,'b':bn,'u':u,'dc':dc,'pa':bool(dc),'nc':False,'rt':False,'c':False,'ml':False,'hol':hol}
    setimg(mid,path,crop)
    if mid not in D['order']: D['order'].append(mid)
    rep['mat_new']+=1; log['mats_new'].append(n+' · '+bn)
newmat('omm:holly-jolly','Holly Jolly (retired)','Oh My Mahjong','',OMMDC,'/tmp/vault3/m/omm-hol-holly-jolly.jpg',hol=True)
newmat('yolo:pink-tiger','Pink Tiger','YOLO Mahjong','https://www.yolomahjong.com/products/pink-tiger-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch','',REPO+'assets/mats/yolo-mahjong/pink-tiger-flat-v2.jpg',crop=(8,8,732,732))
# racks
setrack('www.hiphipmahjong.com/trust-fund-racks',DL+'rk_trust-fund-rac_0.jpg')
# TdT Tortoise Scalloped stays hidden: every Tigre listing photo is a lifestyle shot with tiles (no clean product photo)
# ---------------- rack filters (same rules as the Oct 18 fix)
WOODS={'bb:Weathered Oak','bb:Provincial','bb:Red Mahogany','bb:Dark Walnut'}
OMMSET=lambda s:'Oh My Mahjong' in sets[s]['maker'] or 'Mahjong Row' in sets[s]['maker']
def clean_racks(s,racks):
    out=[]
    for r in racks:
        if r not in R or R[r].get('hid') or r in WOODS: continue
        if 'Oh My Mahjong' in R[r].get('bn','') and 'Oh My Mahjong' not in sets[s]['maker']: continue
        if R[r].get('sm') and not OMMSET(s): continue
        if r not in out: out.append(r)
    return out
sys.path.insert(0,SP+'fymfix')
from common import rres
def rlist(names):
    o=[]
    for n in names:
        k=rres(n)
        if k: o.append(k)
    return o
H=json.load(open(REPO+'scripts/albumcard/holiday_manifest.json'))
T2S={s:s for s in sets}
T2S.update({'sunday':'sunday-mahjong-sunday','december-1994':'sunday-mahjong-december-1994','brownstone-bloom':'anders-ruff-brownstone-bloom','papaya-spritz':'oh-my-mahjong-papaya-spritz','hummingbird':'sunday-mahjong-hummingbird'})
TILE_LOCK={}
for h in H:
    s=T2S.get(h['tile'])
    if s and s not in TILE_LOCK: TILE_LOCK[s]=rlist(h['racks'])
RESTORED=[]
def canon(mid): return REMAP.get(mid,mid)
def present(s,mid): return any(x[0]==mid for x in sets[s]['m'])
def insert(s,mid,racks,anchor_order,src):
    """insert mid into sets[s]['m'] after the nearest earlier item of anchor_order that is already in the list"""
    if s not in sets or mid not in M or M[mid].get('hid'): log['skipped_hidden'].append((s,mid)); return
    if present(s,mid): rep['already_there']+=1; return
    L=sets[s]['m']; pos=None
    if anchor_order and mid in anchor_order:
        k=anchor_order.index(mid)
        for prev in reversed(anchor_order[:k]):
            ix=next((i for i,x in enumerate(L) if x[0]==prev),None)
            if ix is not None: pos=ix+1; break
        if pos is None: pos=0
    if pos is None: pos=len(L)
    L.insert(pos,[mid,clean_racks(s,racks)]); RESTORED.append((s,mid)); rep['pairing_restored']+=1; log['pairings'].append((s,M[mid]['n'],M[mid]['bn'],src))
# A. album pairings dropped because the mat only had a card crop
for s,lst in OLD.items():
    if s not in sets: continue
    order=[canon(x[0]) for x in lst]
    for oid,oracks in lst:
        if not oid.startswith('alb2:'): continue
        mid=canon(oid)
        if M.get(mid,{}).get('hid'): continue
        insert(s,mid,oracks+TILE_LOCK.get(s,[]),order,'album')
# B. holiday manifest: OMM Holly Jolly cards (mat page gone, so these never resolved)
for h in sorted(H,key=lambda h:h['order']):
    if h['mat']!='holly-jolly-mat-in-tube': continue
    s=T2S.get(h['tile'])
    if s=='sunday-mahjong-december-1994': continue
    insert(s,'omm:holly-jolly',rlist(h['racks']+h.get('mat_picks',[])),None,'holiday-album')
# C. December 1994 album: Vegan Leather (Caramel) + Holly Jolly in her saved order
dec=[os.path.basename(x) for x in json.load(open(SP+'shipdb/ship/c5-dec1994.json'))['order'] if 'cover' not in x]
DECT=rlist(next(h['racks'] for h in H if h['tile']=='december-1994'))
FILE2MID={'bam-bird-boutique-vegan-leather-mat.jpg':'www.bambirdboutique.com/origami-leather-mat?v=51114566746421','oh-my-mahjong-holly-jolly-mat.jpg':'omm:holly-jolly'}
s='sunday-mahjong-december-1994'; cur={x[0] for x in sets[s]['m']}
# build anchor order from the album file order, mapping files to mids already in the list via the card rest-name
from common import best,by_handle
anchor=[]
for f in dec:
    rest=f.split('-mahjong-tiles-',1)[1]
    if rest in FILE2MID: anchor.append(FILE2MID[rest]); continue
    hit=next((m for m in cur if M[m]['n'].lower().replace(' ','-').replace("'",'') in rest),None)
    anchor.append(hit or rest)
for rest,mid in FILE2MID.items():
    insert(s,mid,DECT,anchor,'holiday-album')
# D. single new cards
insert('malachite','yolo:pink-tiger',rlist(['Peace Love Mahjong Oak','Miss Mahjong Jade & Brass','Miss Mahjong Brass & Tortoise','Bird & Bamboo Carrot','Bird & Bamboo Dark Teal']),None,'malachite-new')
insert('seabreeze','www.macandmillermahjong.com/sweet-dreams-collection-mahjong-mat',TILE_LOCK.get('seabreeze',[]),None,'logofix-v2')
insert('talulah','www.viroramahjong.com/parrotia',TILE_LOCK.get('talulah',[]),None,'logofix-v2')
# empty rack lists on RESTORED pairings only: fall back to the tile set's locked racks
for (s_,mid) in RESTORED:
    x=next(y for y in sets[s_]['m'] if y[0]==mid)
    if not x[1]:
        x[1]=clean_racks(s_,TILE_LOCK.get(s_,[]))
        if not x[1]:
            c=collections.Counter(r for y in sets[s_]['m'] for r in y[1][:3]); x[1]=[r for r,_ in c.most_common(3)]
        rep['restored_racks_filled']+=1
EMPTY_EXISTING=sum(1 for S_ in D['sets'] for y in S_['m'] if not y[1])
# ranks: her mats first, in list order
oi={m:i for i,m in enumerate(D['order'])}
for S_ in D['sets']:
    herix=[oi[x[0]] for x in S_['m'] if x[0] in oi]; hs=set(herix)
    S_['rank']=herix+[i for i in S_['rank'] if i not in hs]
still=[(i,M[i]['n'],M[i]['bn']) for i in M if M[i].get('hid')]
# ---------------- write
h=HTML[:I0]+json.dumps(D,separators=(',',':'),ensure_ascii=False)+';'+HTML[J0:]
assert '<script src="b11v1.js"></script>' in h and 'b12v1.js' not in h
h=h.replace('<script src="b11v1.js"></script>','<script src="b11v1.js"></script><script src="b12v1.js"></script>',1)
open(OUT+'index.html','w').write(h)
open(OUT+'b12v1.js','w').write('window.IMG=Object.assign(window.IMG||{},'+json.dumps(newIMG,separators=(',',':'))+');')
ch={}
for f,u in newMC.items():
    c=int(f.split('/')[1].split('.')[0])//12; ch.setdefault(c,{})[f]=u
for c,o in ch.items():
    base={}
    if c<=84: base=json.load(open(SP+'fymbuild/mc/%d.json'%c))
    base.update(o); json.dump(base,open(OUT+'mc/%d.json'%c,'w'),separators=(',',':'))
json.dump({'empty_existing':EMPTY_EXISTING,'rep':rep,'log':log,'still_hidden':still,'mc':sorted(ch)},open(FR+'report.json','w'),indent=1,default=list)
print(dict(rep)); print('mc chunks',sorted(ch)); print('still hidden',len(still))
for k,v in log.items(): print(k,len(v))
