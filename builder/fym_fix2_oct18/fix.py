# FYM fix 2 (Oct 18): independent-audit fixes on top of v53. Base = live index.html (v53).
import json,os,re,io,base64,hashlib,collections,colorsys,sys,unicodedata
from PIL import Image,ImageDraw,ImageFont
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
FX=SP+'fymfix2/'; REPO='/home/claude/mahjmatchmaker-data/'; DL=FX+'dl/'; OUT=FX+'build/'
os.makedirs(OUT+'mc',exist_ok=True)
HTML=open(FX+'base.html').read(); I0=HTML.index('const D=')+8; J0=HTML.index('\n',I0)
D=json.loads(HTML[I0:J0].rstrip()[:-1]); M=D['mats']; R=D['racks']
TR=json.load(open(FX+'aud/truth_albums.json'))   # rebuilt against v53 (set index -> ordered cards)
rep=collections.Counter(); log=collections.defaultdict(list)
# ---------------- image helpers (same encoding as restore.py)
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
    im=path if isinstance(path,Image.Image) else Image.open(path)
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA'); bb=im.getbbox(); im=im.crop(bb) if bb else im
        bg=Image.new('RGB',im.size,(255,255,255)); bg.paste(im,mask=im.split()[3]); im=bg
    im=im.convert('RGB')
    if crop: im=im.crop(crop)
    return im
def autotrim(im,thr=245,pad=12):
    g=im.convert('L').point(lambda v:255 if v<thr else 0); bb=g.getbbox()
    if not bb: return im
    return im.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)))
def setimg(mid,path,crop=None,keepcolors=False):
    global nextf
    im=load(path,crop); full=im.copy(); full.thumbnail((900,900))
    b=io.BytesIO(); full.save(b,'WEBP',quality=80); f='m/%d.webp'%nextf; nextf+=1
    newMC[f]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    th=im.copy(); th.thumbnail((180,180)); b=io.BytesIO(); th.save(b,'JPEG',quality=74)
    t='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(); h='mt'+hashlib.md5(t.encode()).hexdigest()[:8]
    newIMG[h]=t; m=M[mid]; m['f']=f; m['th']=h; m['w'],m['h']=full.size; m['c']=False
    if not keepcolors:
        m['ms'],mf=colors(im); m['mf']=mf or ['neutral']
    m['src']='clean'; m.pop('hid',None)
def setrack(rid,img):
    im=load(img); im.thumbnail((640,640)); b=io.BytesIO(); im.save(b,'JPEG',quality=82)
    t='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(); h='rk'+hashlib.md5(t.encode()).hexdigest()[:8]
    newIMG[h]=t; R[rid]['im']=h; R[rid]['c']=False; R[rid].pop('hid',None); R[rid].pop('lo',None); rep['rack_photo']+=1; log['rack_photos'].append(R[rid]['n'])
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; FONT2='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def placeholder(mid):
    m=M[mid]; W=900; im=Image.new('RGB',(W,W),(248,242,233)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((40,40,W-40,W-40),radius=36,outline=(31,58,107),width=6)
    d.rounded_rectangle((70,70,W-70,W-70),radius=26,outline=(232,180,196),width=3)
    def ctext(y,t,f,fill):
        w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
    nm=re.sub(r'\s*\(retired\)$','',m['n'])
    fs=64
    while fs>30 and d.textlength(nm,font=ImageFont.truetype(FONT,fs))>W-200: fs-=4
    ctext(330,nm,ImageFont.truetype(FONT,fs),(31,58,107))
    ctext(330+fs+24,m.get('bn',''),ImageFont.truetype(FONT2,38),(90,90,110))
    ctext(560,'Photo coming soon',ImageFont.truetype(FONT2,40),(200,110,140))
    ctext(230,'♥',ImageFont.truetype(FONT2,70),(232,120,150))
    ms,mf=m.get('ms'),m.get('mf')   # keep colors measured from her card crop (pattern colors)
    setimg(mid,im,keepcolors=True); m['ph']=True
    if ms: m['ms']=ms
    if mf: m['mf']=mf
    rep['placeholder']+=1; log['placeholders'].append(m['n']+' · '+m.get('bn',''))
def newmat(mid,n,bn,u,dc,path,hol=False,crop=None,tmpl=None):
    base=dict(M[tmpl]) if tmpl else {}
    base.update({'n':n,'bn':bn,'b':bn,'u':u,'dc':dc,'pa':bool(dc),'nc':False,'rt':False,'c':False,'ml':False,'hol':hol})
    for k in ('alt','src','hid','ph'): base.pop(k,None)
    M[mid]=base; setimg(mid,path,crop)
    if mid not in D['order']: D['order'].append(mid)
    rep['mat_new']+=1; log['mats_new'].append(n+' · '+bn)
# ---------------- 1. catalog: new mats + photo fixes
SPLASH_T='splashofcolorco.com/peony-and-parasol' if 'splashofcolorco.com/peony-and-parasol' in M else None
newmat('splashofcolorco.com/alpine-ski-lodge-mahjong-winter-play-mat','Alpine Ski Lodge Winter','Splash of Color',
       'https://splashofcolorco.com/products/alpine-ski-lodge-mahjong-winter-play-mat',M[SPLASH_T]['dc'] if SPLASH_T else '',
       REPO+'assets/mats/holiday/hd/alpine-ski-lodge-mahjong-winter-play-mat.jpg',hol=True,tmpl=SPLASH_T)
newmat('maisonmahj.com/the-chalet-mat','The Chalet','Maison Mahj','https://maisonmahj.com/products/the-chalet-mat','',
       REPO+'assets/mats/holiday/hd/maison-chalet.jpg',hol=True,tmpl='maisonmahj.com/the-afternoon-tea-mat')
BUT='www.wrenmats.com/watercolor-floral-wz34m'
newmat('www.wrenmats.com/watercolor-floral','Watercolor Floral','Wren Mats','https://www.wrenmats.com/mats/p/watercolor-floral',M[BUT]['dc'],
       REPO+'assets/mats/wren-mats/watercolor-floral.jpg',tmpl=BUT)
SUG='peacelovemahjong.com/mahjong-mats-holiday?v=67570557321508'; MMX='peacelovemahjong.com/mahjong-mats-holiday?v=67570521276708'
setimg(SUG,REPO+'assets/mats/holiday/hd/plm-holiday-sugarplum-plaid.jpg'); log['mat_photos'].append('PLM Sugarplum Plaid (Peace Love Holiday)')
setimg(MMX,autotrim(Image.open(DL+'plmhol/5.jpg').convert('RGB'))); log['mat_photos'].append('PLM Merry Mix (flat mat, not the box)')
# Jardín de Los Jefes: no flat photo exists; use the clean pattern close-up (no racks, no tiles)
JAR='tigredetartan.com/third-shipment-mahjong-mat-jardin-de-los-jefes'
im=Image.open(DL+'jardin/3.jpg').convert('RGB'); w,h=im.size; s=min(w,h); setimg(JAR,im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))); log['mat_photos'].append('Jardín de Los Jefes (pattern close-up; brand has no flat photo)')
# Savannah Leatherette: crop the mat out of the brand's marketing graphic
SAV='brittmillsdesign.com/savannah-leatherette-mahjong-mat'
im=Image.open(DL+'savannah/0.jpg').convert('RGB'); px=im.load(); W_,H_=im.size
bg=px[10,H_//2]
def isbg(p): return sum(abs(a-b) for a,b in zip(p,bg))<60
xs=[x for x in range(W_) if sum(1 for y in range(H_//3,2*H_//3,6) if not isbg(px[x,y]))>8]
ys=[y for y in range(H_) if sum(1 for x in range(W_//3,2*W_//3,6) if not isbg(px[x,y]))>8]
# keep the largest contiguous run (the mat), skipping title/text lines
def run(v):
    best=(0,0);st=v[0];pr=v[0]
    for a in v[1:]+[10**9]:
        if a!=pr+1:
            if pr-st>best[1]-best[0]: best=(st,pr)
            st=a
        pr=a
    return best
x0,x1=run(xs); y0,y1=run(ys)
setimg(SAV,im.crop((x0,y0,x1,y1))); log['mat_photos'].append('Savannah Leatherette (mat cropped from brand graphic, %dx%d)'%(x1-x0,y1-y0))
# ---------------- 2. aliases (duplicates / wrong products) applied to truth + every set
HUNT_W='www.charlestonmahjongclub.com/the-hunt-club-neoprene-mat-toile-w-carrying-bag'; HUNT='charlestonmahjongclub.com/the-hunt-club-neoprene-mat-toile-w-carrying-bag'
LUNA_V='mahjongstudios.com/mahjong-mat?v=50645970682093'; LUNA='mahjongstudios.com/lunaflor-mahjong-mat'
VP_V='www.bambirdboutique.com/neoprene-mat?v=51290364313909'; VP='www.bambirdboutique.com/vintage-plum-neoprene-mahjong-mat'
WHOLE='peacelovemahjong.com/mahjong-mats-holiday-1'
ALIAS={HUNT_W:HUNT,LUNA_V:LUNA,VP_V:VP,MMX:SUG,WHOLE:SUG,
 'alb2:bam-bird-boutique-classic-neoprene-in-pink':'www.bambirdboutique.com/classic-neoprene-mahjong-mat-copy',
 'alb2:mahj-moon-pink-citrus-chinoiserie':'mahjandmoon.com/pink-lemon-blossom-mahjong-mat',
 'alb2:bespoke-mahjong-yotd-purple':'www.bespokemahjong.com/year-of-the-dragon-mat-plum',
 'alb2:mahj-vine-chinoiserie':'mahjandvine.com/chinoiserie-song-bird','alb2:mahj-vine-chinoiserie-songbird-2':'mahjandvine.com/chinoiserie-song-bird',
 'alb2:ozark-mah-jongg-winslow-1920':'ozarkmahjong.com/winslow-1920-original-navy-blue-mat',
 'alb2:oh-my-mahjong-lorelei-2':'www.ohmymahjong.com/lorelei-mat','alb2:oh-my-mahjong-serengeti-2':'alb:amara:Serengeti','alb2:oh-my-mahjong-enchanted-2':'alb:amara:Enchanted'}
for a,b in ALIAS.items(): assert b in M,(a,b)
# merged duplicates leave the catalog (door search shows one entry)
for a in (HUNT_W,LUNA_V,VP_V,WHOLE,'alb2:ozark-mah-jongg-winslow-1920'): M[a]['hid']=1; log['dups_hidden'].append(M[a]['n']+' -> '+M[ALIAS[a]]['n'])
if not M[HUNT].get('n','').startswith('The'): M[HUNT]['n']='The Hunt Club'
A=lambda mid: ALIAS.get(mid,mid)
# ---------------- 3. unmapped album cards -> mat (checked against the card images)
CARDMAP={'Birdie':'alb:coquette:Birdie Green','Alpine Ski Lodge Winter':'splashofcolorco.com/alpine-ski-lodge-mahjong-winter-play-mat',
 'The Chalet':'maisonmahj.com/the-chalet-mat','Isabel Harte':'alb2:isabel-harte-isabel-harte','Watercolor Floral':'www.wrenmats.com/watercolor-floral',
 'Blue Cowboy Boot':'hutchandnook.com/mahjong-mat-blue-cowboy-boot','The Club Blue Green Stripe':'www.charlestonmahjongclub.com/the-club-mat-2-color-options-copy',
 'Songbird Bloom':'hutchandnook.com/mahjong-mat-moody-mat-songbird-bloom','Mary Benson':'alb2:mary-benson-mary-benson',
 'Pink Citrus Chinoiserie':'mahjandmoon.com/pink-lemon-blossom-mahjong-mat','Chinoiserie':'mahjandvine.com/chinoiserie-song-bird',
 'Amazon':'alb2:amazon-amazon','Amazon 2':'alb2:amazon-amazon-2','Nantucket Rope':'tigredetartan.com/mahjong-mat-nantucket-basket-1'}
for si,L in TR.items():
    for x in L:
        if not x['mat']:
            k=x['title'].split(' + ',1)[1]
            if k in CARDMAP: x['mat']=CARDMAP[k]; rep['card_mapped']+=1
            else: log['card_unmapped'].append((D['sets'][int(si)]['name'],x['title']))
        if x['mat']: x['mat']=A(x['mat'])
# ---------------- 4. racks: bans, photos, low-priority, universal
WOODS=['bb:Weathered Oak','bb:Provincial','bb:Red Mahogany','bb:Dark Walnut','bb:Almond','bb:Tudor']
for w in WOODS: R[w]['hid']=1
log['woods_hidden']=WOODS
# Mahjong Register pearl racks: crop each variant's own row out of the brand's 6-up photo
mr=Image.open(DL+'mreg/0.jpg').convert('RGB'); g=mr.convert('L'); Wm,Hm=mr.size
rows=[y for y in range(Hm) if sum(1 for x in range(0,Wm,8) if g.getpixel((x,y))<240)>Wm//8*0.35]
bands=[];st=rows[0];pr=rows[0]
for y in rows[1:]+[10**9]:
    if y!=pr+1:
        if pr-st>40: bands.append((st,pr))
        st=y
    pr=y
mb=[]
for b in bands:
    if mb and b[0]-mb[-1][1]<12: mb[-1]=(mb[-1][0],b[1])
    else: mb.append(b)
bands=mb
assert len(bands)==6,bands
MRV=['Navy','Capri Blue','Emerald','Sea Glass','Peony Blush','Ivory Oyster']
for (y0,y1),v in zip(bands,MRV):
    rid=next(k for k,r in R.items() if r['n']=='Mahjong Register %s Pearl Scalloped'%v)
    setrack(rid,autotrim(mr.crop((0,max(0,y0-14),Wm,min(Hm,y1+14)))))
# My Fair premium acrylic variants: the brand's single-variant photo (top half; the label text below is cut off)
MFV={'myfairmahjong.com/acrylic-mahjong-racks':40,'myfairmahjong.com/acrylic-mahjong-racks?v=52896917750071':39,'myfairmahjong.com/acrylic-mahjong-racks?v=52896919322935':36,
     'myfairmahjong.com/acrylic-mahjong-racks?v=52896919519543':23,'myfairmahjong.com/acrylic-mahjong-racks?v=52896919683383':37,'myfairmahjong.com/acrylic-mahjong-racks?v=52896920207671':38}
for rid,k in MFV.items():
    im=Image.open(DL+'mfp/%d.jpg'%k).convert('RGB'); w,h=im.size
    top=im.crop((0,0,w,int(h*0.56)))
    setrack(rid,autotrim(top))
# racks whose only photos show tiles, bags or several variants: never in the first cards
LO=['www.hiphipmahjong.com/hostess-with-the-mostest-racks','www.bamletsmahjong.com/white-acrylic-racks-set-4',
    'mahjongregister.com/signature-collection-acrylic-mahjong-racks-set-of-4-20-luxury-tile-holders','sundaymahjong.com/clear-mahjong-rack-set']
for k,r in R.items():
    if r.get('bn')=='Royal Mahjong Society' and 'White' in r['n']: LO.append(k)
for k in LO:
    if k in R: R[k]['lo']=1; log['racks_lo'].append(R[k]['n'])
D['uni']=D['uni'][:3]   # L1: PLM Oak, My Fair Clear, M&M Hawksbill only
# ---------------- 5. rebuild her match lists
SL={'Miss Classic Jade':'jade','Miss Classic Malachite':'malachite','Classic Tortoise':'tortoise','Heritage 1.0':'heritage','Heritage 2.0':'heritage-2-0','Cypress':'cypress-forest','Sunday':'sunday','Petalée':'petalee','La Fete':'la-fete'}
def slug(s): s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower(); return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def nk(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
IDA={'Miss Mahjong Scalloped Iridescent Opal':'missmahjong.com/iridescent-opal-scalloped-acrylic-racks','Middle & Main Hawksbill Heritage Tortoise':'mm:Hawksbill','Middle & Main Hawksbill Tortoise':'mm:Hawksbill',
 'Peace Love Mahjong Acrylic Burl':'peacelovemahjong.com/acrylic-burlwood-mahjong-racks-pushers-set-of-4','Middle & Main White Lace Acrylic':'www.middleandmainmahjong.com/blue-and-white-chinoiserie-mahjong-rack-and-pusher-set-of-4-copy',
 'Middle & Main White Lace':'www.middleandmainmahjong.com/blue-and-white-chinoiserie-mahjong-rack-and-pusher-set-of-4-copy',
 'Middle & Main Milk Glass':'www.middleandmainmahjong.com/milk-glass-collection-mahjong-rack-and-pusher-set-of-4','Sunday Mahjong Cola':'sundaymahjong.com/sunday-cola-mahjong-rack-set','Mahj Mood Scalloped White':'mahjmood.com/pure-white-acrylic-racks-and-pushers',
 'Mahjong Row & Co. Scalloped Tortoise':'mahjongrowandco.com/scalloped-deluxe-tortoise-rack','Miss Mahjong Brass & Tortoise':'missmahjong.com/blonde-tortoise-and-brass-acrylic-racks','My Fair Mahjong Clear':'vr:My Fair Mahjong:Transparent Clear',
 'Middle & Main Scalloped Milk Glass':'www.middleandmainmahjong.com/milk-glass-collection-mahjong-rack-and-pusher-set-of-4','Middle & Main Scalloped Milk Glass Acrylic':'www.middleandmainmahjong.com/milk-glass-collection-mahjong-rack-and-pusher-set-of-4'}
RN={}
for k,r in R.items(): RN.setdefault(nk(r['n']),k)
def rid(name):
    if name in IDA: return IDA[name]
    n=nk(name)
    if n in RN: return RN[n]
    c=[k for k,r in R.items() if r.get('bn') and n.startswith(nk(r['bn'])) and nk(r['n'].replace(r['bn'],''))==n[len(nk(r['bn'])):]]
    if c: return c[0]
    c=[k for k,r in R.items() if r.get('bn') and n.startswith(nk(r['bn'])) and n[len(nk(r['bn'])):] and n[len(nk(r['bn'])):] in nk(r['n'])]
    return c[0] if len(c)==1 else None
trp=json.load(open(REPO+'config/tile-racks-picks.json')); mrp=json.load(open(REPO+'config/mat-racks-picks.json'))
unres=collections.Counter()
def ids(names):
    o=[]
    for n in names:
        k=rid(n)
        if k and k not in o: o.append(k)
        elif not k: unres[n]+=1
    return o
def toks(s): return [t for t in slug(s).split('-') if t and t not in ('the','mat','mahjong','mahj')]
LT={}
for s in D['sets']:
    k=SL.get(s['name'],slug(s['name']))
    L=trp.get('final_lists',{}).get(k,[])+trp.get('fym_more',{}).get(k,[])
    if L: LT[s['slug']]=ids(L)
LM={}
for mid,m in M.items():
    for k,v in mrp.items():
        if k.startswith('_'): continue
        files=' '.join(v.get('files',[])); key=slug(m['n'])
        if k in slug(m['n']+' '+m.get('bn','')) or (key and key in files) or (set(toks(v['mat']))>=set(toks(m['n'])) and set(toks(m['n'])) and slug(m.get('bn','')).split('-')[0] in slug(v['mat'])):
            LM[mid]=ids(v['racks']); break
D['lt']=LT; D['lm']=LM
WOODSET=set(WOODS)
def okr(s,r):
    if r not in R or R[r].get('hid') or r in WOODSET: return False
    if 'Oh My Mahjong' in R[r].get('bn','') and 'Oh My Mahjong' not in s['maker']: return False
    if R[r].get('sm') and not re.search('Oh My Mahjong|Mahjong Row',s['maker']): return False
    return True
HOL=set(json.load(open(REPO+'config/tile-back-colors.json')).get('Holiday',[]))
# FYM pairs that no album card supports (audit rule 2) -> dropped
DROP={('Gatsby','www.charlestonmahjongclub.com/the-ski-club-mat-in-toile-w-matching-bag'),('Nantucket','www.charlestonmahjongclub.com/the-ski-club-mat-in-toile-w-matching-bag'),
      ('Solara',BUT),('Classic Tortoise',BUT),('Miss Classic Jade',BUT),('Miss Classic Jade','www.bespokemahjong.com/year-of-the-dragon-mat-raspberry'),
      ('Miss Classic Malachite',JAR),('Brownstone Bloom',JAR),('Pearlescent','www.bamletsmahjong.com/secret-garden-mahjong-mat-watercolor-floral-mahjong-mat'),
      ('Brownstone Bloom','brittmillsdesign.com/eden-neoprene-mahjong-mat')}
for k,r in R.items(): pass
YR=[k for k,m in M.items() if m['n']=='YOTD Raspberry']; MOCHA=[k for k,m in M.items() if m['n'].startswith('Mocha Bloom')]
for k in YR: DROP.add(('Miss Classic Jade',k))
for k in MOCHA: DROP.add(('Brownstone Bloom',k))
# December 1994: her saved album order (ship db) -> mat ids; Periwinkle there is really the Red Sweater card
DEC=[os.path.basename(x) for x in json.load(open(SP+'shipdb/ship/c5-dec1994.json'))['order'] if 'cover' not in x]
RED='www.charlestonmahjongclub.com/new-ski-mat-with-red-sweater-border-and-toilet-pattern'; PERI='www.charlestonmahjongclub.com/the-ski-club-mat-in-toile-w-matching-bag'
changed=0
for si,s in enumerate(D['sets']):
    old=[[A(x[0]),list(x[1])] for x in s['m']]
    seen=set(); oldm=[]
    for mid,rk in old:
        if mid in seen:   # merge racks of aliased duplicates
            nx=next(y for y in oldm if y[0]==mid); nx[1]+= [r for r in rk if r not in nx[1]]; continue
        seen.add(mid); oldm.append([mid,rk])
    oldr={mid:rk for mid,rk in oldm}
    truth=TR.get(str(si))
    if s['name']=='December 1994':
        oldm=[[RED if mid==PERI else mid,rk] for mid,rk in oldm]; oldr={mid:rk for mid,rk in oldm}
        order=[]
        for f in DEC:
            rest=f.split('-mahjong-tiles-',1)[1][:-8]   # drop -mat.jpg
            FOV={'anders-ruff-tartan-toile-no-l':next((k for k,_ in oldm if M[k]['n'].startswith('Tartan Toile')),None),'charleston-mahjong-club-ski-club-red-sweater':RED,'peace-love-mahjong-peace-love-holiday':SUG}
            if FOV.get(rest) in oldr:
                if FOV[rest] not in order: order.append(FOV[rest])
                continue
            hit=None; rt=set(t for t in rest.split('-') if t)
            STOP={'premium','mahjong','mat','neoprene','the','retired','mahj','s','l','no'}
            best=0
            for mid,_ in oldm:
                m=M[mid]; mt=set(t for t in slug(re.sub(r'\s*\(retired\)$','',m['n'])).split('-') if t and t not in STOP)
                bt=set(slug(m.get('bn','')).split('-'))
                if mt and mt<=rt and bt<=rt|{'co','and'}:
                    if len(mt)>best: best=len(mt); hit=mid
            if not hit:
                for mid,_ in oldm:
                    m=M[mid]; mt=set(t for t in slug(m['n']).split('-') if t and t not in STOP)
                    if mt and len(mt&rt)>=max(1,len(mt)-1) and set(slug(m.get('bn','')).split('-'))&rt: hit=mid; break
            if hit and hit not in order: order.append(hit)
        new=order+[mid for mid,_ in oldm if mid not in order]
        log['dec1994_unplaced']=[M[m]['n'] for m in new[len(order):]]
        s['m']=[[mid,[r for r in oldr[mid] if okr(s,r)]] for mid in new]; changed+=1; continue
    if not truth:
        s['m']=[[mid,[r for r in rk if okr(s,r)]] for mid,rk in oldm if (s['name'],mid) not in DROP]; continue
    tmats=[];tr_r={}
    for x in truth:
        mid=x['mat']
        if not mid or mid not in M: continue
        if mid not in tmats: tmats.append(mid); tr_r[mid]=[r for r in x['rackids'] if r]
        else: tr_r[mid]+= [r for r in x['rackids'] if r and r not in tr_r[mid]]
    extras=[mid for mid,_ in oldm if mid not in tmats and (s['name'],mid) not in DROP]
    order=tmats+extras
    if s['name'] in HOL and order:
        # holiday rule (kept): the set's own pair mat leads
        pair=next((mid for mid,_ in oldm[:1] if M[mid].get('bn')==s['maker']),None) or next((mid for mid in tmats if M[mid].get('bn')==s['maker']),None)
        if pair: order=[pair]+[m for m in order if m!=pair]
    newm=[]
    for mid in order:
        rk=oldr.get(mid) or []
        if not rk: rk=tr_r.get(mid,[])          # H11: empty pair -> racks printed on her card
        rk=[r for r in rk if okr(s,r)]
        newm.append([mid,rk])
    if [x[0] for x in newm]!=[x[0] for x in s['m']]: changed+=1
    s['m']=newm
    log['extras_kept'].extend((s['name'],M[m]['n']) for m in extras)
rep['sets_reordered']=changed
# unhide every mat that is now one of her matches; card-crop photos become a neutral placeholder
used=collections.Counter(x[0] for s in D['sets'] for x in s['m'])
for mid in used:
    m=M[mid]
    if m.get('src')=='album-card' or (m.get('hid') and m.get('src')!='clean'):
        placeholder(mid)
    m.pop('hid',None)
for mid,m in M.items():
    if m.get('src')=='album-card' and not used[mid] and not m.get('hid'): m['hid']=1
# ---------------- 6. names / catalog cleanup
for k,m in M.items():
    if m.get('bn')=='Hutch & Nook' and m['n']=='Mahjong Mat':
        sl=k.split('/',1)[1].replace('mahjong-mat-','')
        nm={'moody-mat-songbird-bloom':'Songbird Bloom','moody-mat':'Moody'}.get(sl,sl.replace('-',' ').title().replace('White','White'))
        m['n']=nm; log['hutch_named'].append(nm)
M[BUT]['n']='Butterfly'
DROPSETS={'Mahjong Tile Takers (Set of 4)','Giant Mahjong Tile (for decor)- sold as individual','Mischief Mahj'}
D['sets']=[s for s in D['sets'] if s['name'] not in DROPSETS]
for s in D['sets']:
    if s['name']=='Tile Sets' and s['maker']=='Mahjong Studios': s['name']='Tiles Only'; T_=D['tiles'][s['tile']]; T_['n']='Tiles Only'
# Nature Walk: her approved crop (no sundaymahjong.com banner)
NW=next(s for s in D['sets'] if s['name']=='Nature Walk')
D['tiles'][NW['tile']]['full']='t14/0.jpg'
os.makedirs(OUT+'t14',exist_ok=True)
nwim=load(REPO+'assets/tiles/album/nature-walk.png'); nwim.save(OUT+'t14/0.jpg','JPEG',quality=88)
th=nwim.copy(); th.thumbnail((240,240)); b=io.BytesIO(); th.save(b,'JPEG',quality=78)
t='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(); h='tp'+hashlib.md5(t.encode()).hexdigest()[:8]; newIMG[h]=t; D['tiles'][NW['tile']]['pile']=h
# ranks: her mats first, in list order
oi={m:i for i,m in enumerate(D['order'])}
for S_ in D['sets']:
    herix=[oi[x[0]] for x in S_['m'] if x[0] in oi]; hs=set(herix)
    S_['rank']=herix+[i for i in S_['rank'] if i not in hs]
# ---------------- 7. JS fixes
h=HTML[:I0]+json.dumps(D,separators=(',',':'),ensure_ascii=False)+';'+HTML[J0:]
def sub(old,new,cnt=1):
    global h
    assert h.count(old)==cnt,(old[:80],h.count(old)); h=h.replace(old,new)
# racks: her card racks + locked tile racks + locked mat racks (all filtered by the rack rules); low-photo racks last
sub("const herRacks=()=>{const x=set().m.find(x=>x[0]===S.fav);return x?x[1]:[];};",
    "const herRacks=()=>{const x=set().m.find(x=>x[0]===S.fav);const a=[...(x?x[1]:[]),...((D.lt||{})[set().slug]||[]),...((D.lm||{})[S.fav]||[])];return [...new Set(a)].filter(r=>typeof rackOK==='function'?rackOK(r):!!R[r]);};")
sub("const U=uni();const rest=Object.keys(R).filter(r=>!hr.includes(r)&&!U.includes(r)&&rackOK(r)).map(r=>[sc(r),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);",
    "const U=uni();const rest=Object.keys(R).filter(r=>!hr.includes(r)&&!U.includes(r)&&rackOK(r)).map(r=>[sc(r)+(R[r].lo?1e4:0),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);")
# M9: undoing the mocked mat clears it (and its racks) from step 3
sub("function undo(k){if(k==='m'){const id=S.hist.pop();if(!id)return;delete S.seen[id];S.liked=S.liked.filter(x=>x!==id);renderMats();}",
    "function undo(k){if(k==='m'){const id=S.hist.pop();if(!id)return;delete S.seen[id];S.liked=S.liked.filter(x=>x!==id);if(S.peek===id)S.peek=null;if(S.fav===id){Object.assign(S,{fav:null,rseen:{},rliked:[],rhist:[],rpick:[]});S.f.r={fam:'',brand:'',her:false};S.made=false;renderAll();return;}renderMats();}")
# M10: the full-screen button on the swipe card must not be swallowed by the swipe's pointer capture
sub("host.querySelectorAll('[data-z],[data-tz]').forEach(b=>{",
    "host.querySelectorAll('.xz[data-lbx]').forEach(b=>{b.addEventListener('pointerdown',e=>e.stopPropagation());b.addEventListener('click',e=>{e.stopPropagation();openLbx(b.dataset.lbx);});});host.querySelectorAll('[data-z],[data-tz]').forEach(b=>{")
sub("const toks=v.split(/\\s+/);const hits=Object.keys(M).filter(id=>{const s=(M[id].n+' '+(M[id].bn||'')).toLowerCase();return toks.every(k=>s.includes(k));}).slice(0,60);",
    "const toks=v.split(/\\s+/);const hits=Object.keys(M).filter(id=>{if(M[id].hid)return false;const s=(M[id].n+' '+(M[id].bn||'')).toLowerCase();return toks.every(k=>s.includes(k));}).slice(0,60);")
sub("const toks=v.split(/\\s+/);const hits=Object.keys(M).filter(id=>{const s=(M[id].n+' '+(M[id].bn||'')).toLowerCase();return toks.every(t=>s.includes(t));})",
    "const toks=v.split(/\\s+/);const hits=Object.keys(M).filter(id=>{if(M[id].hid)return false;const s=(M[id].n+' '+(M[id].bn||'')).toLowerCase();return toks.every(t=>s.includes(t));})")
assert '<script src="b12v1.js"></script>' in h and 'b13v1.js' not in h
h=h.replace('<script src="b12v1.js"></script>','<script src="b12v1.js"></script><script src="b13v1.js"></script>',1)
open(OUT+'index.html','w').write(h)
open(OUT+'b13v1.js','w').write('window.IMG=Object.assign(window.IMG||{},'+json.dumps(newIMG,separators=(',',':'))+');')
ch={}
for f,u in newMC.items():
    c=int(f.split('/')[1].split('.')[0])//12; ch.setdefault(c,{})[f]=u
for c,o in ch.items():
    p=FX+'site/mc/%d.json'%c; base=json.load(open(p)) if os.path.exists(p) else {}
    base.update(o); json.dump(base,open(OUT+'mc/%d.json'%c,'w'),separators=(',',':'))
json.dump({'rep':rep,'log':log,'mc':sorted(ch),'unresolved_rack_names':unres,'lt':len(LT),'lm':len(LM)},open(FX+'report.json','w'),indent=1,default=list,ensure_ascii=False)
print(dict(rep)); print('mc chunks',sorted(ch)); print('unresolved racks',unres.most_common(12)); print('card_unmapped',log['card_unmapped'])
