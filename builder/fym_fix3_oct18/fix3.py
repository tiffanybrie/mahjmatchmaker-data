# FYM fix 3 (Oct 18 afternoon): full-quality mat + catalog tile images, mat-image rules, wrong-image fixes.
# Applies on top of the CURRENT scratchpad/fymfix2/build/index.html (re-read at write time), then the caller runs
# builder/fym_mated_oct18/patch.py again.
import json,os,re,io,base64,hashlib,sys,shutil,collections
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
Image.MAX_IMAGE_PIXELS=None
FX='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/'
REPO='/home/claude/mahjmatchmaker-data/'
OUT=FX+'build/'
sys.path.insert(0,FX+'f3')
P=json.load(open(FX+'f3/proc.json'))
LONG=int(os.environ.get('LONG','1200')); Q=int(os.environ.get('Q','85'))
log=collections.defaultdict(list)

h=open(OUT+'index.html').read(); I0=h.index('const D=')+8; J0=h.index('\n',I0)
D=json.loads(h[I0:J0].rstrip()[:-1]); M=D['mats']; T=D['tiles']

def famof(rgb):
    import colorsys
    r,g,b=[x/255 for x in rgb]; hh,l,s=colorsys.rgb_to_hls(r,g,b); hh*=360
    if l<0.22: return 'dark'
    if s<0.18 or (l>0.85 and s<0.4): return 'neutral'
    if hh<15 or hh>=345: return 'red' if l<0.6 else 'pink'
    if hh<40: return 'orange'
    if hh<65: return 'yellow'
    if hh<170: return 'green'
    if hh<255: return 'blue'
    if hh<300: return 'purple'
    return 'pink'
def colors(im):
    q=im.convert('RGB').resize((120,120)).quantize(6); pal=q.getpalette(); cnt=sorted(q.getcolors(),reverse=True)
    tot=sum(c for c,_ in cnt); ms=[];fam=[]
    for c,ix in cnt[:5]:
        rgb=pal[ix*3:ix*3+3]; ms.append(['#%02x%02x%02x'%tuple(rgb),round(c/tot,2)])
        f=famof(rgb)
        if f not in fam and c/tot>0.08: fam.append(f)
    return ms,fam[:3]

# ---- new image slots: mat files are separate webp files (mf/N.webp); mc chunks hold their URL
nextf=max(int(m['f'].split('/')[1].split('.')[0]) for m in M.values())+1
newMC={}; newIMG={}
def setmat(mid,im,keepcolors=False,src='clean',newthumb=True):
    global nextf
    im=im.convert('RGB'); full=im.copy(); full.thumbnail((LONG,LONG),Image.LANCZOS)
    n=nextf; nextf+=1; f='m/%d.webp'%n
    b=io.BytesIO(); full.save(b,'WEBP',quality=Q,method=6)
    newMC[f]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    m=M[mid]
    if newthumb or not m.get('th'):
        th=im.copy(); th.thumbnail((140,140)); b=io.BytesIO(); th.save(b,'JPEG',quality=70)
        t='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(); hh='mt'+hashlib.md5(t.encode()).hexdigest()[:8]
        newIMG[hh]=t; m['th']=hh
    m['f']=f; m['w'],m['h']=full.size; m['c']=False
    if not keepcolors: m['ms'],mf=colors(im); m['mf']=mf or ['neutral']
    m['src']=src
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; FONT2='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def placeholder(mid,why):
    m=M[mid]; W=900; im=Image.new('RGB',(W,W),(248,242,233)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((40,40,W-40,W-40),radius=36,outline=(31,58,107),width=6)
    d.rounded_rectangle((70,70,W-70,W-70),radius=26,outline=(232,180,196),width=3)
    def ctext(y,t,f,fill):
        w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
    nm=re.sub(r'\s*\(retired\)$','',m['n']); fs=64
    while fs>30 and d.textlength(nm,font=ImageFont.truetype(FONT,fs))>W-200: fs-=4
    ctext(330,nm,ImageFont.truetype(FONT,fs),(31,58,107))
    ctext(330+fs+24,m.get('bn',''),ImageFont.truetype(FONT2,38),(90,90,110))
    ctext(560,'Photo coming soon',ImageFont.truetype(FONT2,40),(200,110,140))
    ctext(230,'♥',ImageFont.truetype(FONT2,70),(232,120,150))
    setmat(mid,im,keepcolors=True,src='placeholder'); m['ph']=True
    log['placeholder'].append(f"{m['n']} · {m['bn']} ({why})")

album={r[0] for r in json.load(open(FX+'f3/cmp.json'))}
# album mats per set (her lists) live in D['sets'][i]['m']; a mat is "hers" if it is in any set's list
hers=set(x[0] for s in D['sets'] for x in s.get('m',[]))

# ---------- 1. full-quality images from the quality pass
SKIP=set(m for m in M if M[m].get('ph'))
OVK=set(k.split('|',1)[1] for k in json.load(open(FX+'f3/overrides.json')))
for k,v in P.items():
    kind,key=k.split('|',1)
    if kind!='m' or 'file' not in v or key not in M or key in SKIP or M[key].get('hid'): continue
    im=Image.open(FX+v['file']) if not v['file'].startswith('/') else Image.open(v['file'])
    if v['src']=='current' and max(im.size)<=max(M[key].get('w',0),M[key].get('h',0))+4 and not v.get('graphic') and not v.get('bamboo'):
        # only trimmed: still re-store so the mat fills the frame
        pass
    changed=v['src']!='current' or v.get('graphic') or v.get('bamboo') or key in OVK
    setmat(key,im,keepcolors=not changed,src='hq',newthumb=bool(changed))
    log['mat_hq'].append((M[key]['bn'],max(v['before']),max(im.size) if v['src']=='current' else min(max(im.size),LONG)))

# ---------- 2. specific fixes
def first(pred):
    for m in M:
        if pred(m): return m
BL=first(lambda m:'bandana-neoprene' in m and 'Blue/Pink' in M[m]['n']); OL=first(lambda m:'bandana-neoprene' in m and 'Olive' in M[m]['n'])
FF=first(lambda m:'mahjong-mats-hanukkah' in m and M[m]['n']=='Frosted Flowers'); BS=first(lambda m:'mahjong-mats-hanukkah' in m and M[m]['n']=='Blue Stripes')
# Caroline in Peacock (the card's mat; the catalog only had Caroline in Navy)
CN='mahjandvine.com/caroline-in-navy'; CP='mahjandvine.com/caroline-in-peacock'
if CP not in M:
    M[CP]=dict(M[CN]); M[CP].update({'n':'Caroline in Peacock','u':M[CN]['u'].replace('caroline-in-navy','caroline-in-peacock')})
    for kk in ('hid','ph','alt'): M[CP].pop(kk,None)
    D['order'].append(CP)
cp=Image.open(FX+'f3/dl2/caroline_peacock_mat.png'); setmat(CP,cp); log['mat_new'].append('Caroline in Peacock · Mahj & Vine')
M[CN]['n']='Caroline in Navy'
def remap(old,new,why):
    c=0
    for s in D['sets']:
        for x in s.get('m',[]):
            if x[0]==old: x[0]=new; c+=1
    oi=D['order'].index(old) if old in D['order'] else None; ni=D['order'].index(new) if new in D['order'] else None
    if oi is not None and ni is not None:
        for s in D['sets']:
            if oi in s['rank'] and any(x[0]==new for x in s.get('m',[])):
                r=[ni if q==oi else q for q in s['rank']]; seen=set(); s['rank']=[q for q in r if not (q in seen or seen.add(q))]
    for kk in ('lm',):
        if old in D.get(kk,{}) and new not in D[kk]: D[kk][new]=D[kk][old]
    log['remap'].append(f"{M[old]['n']} -> {M[new]['n']} ({why}, {c} lists)")
remap(OL,BL,'Coquette + Bandana card is the blue/pink colorway')
remap(BS,FF,'PLM Hanukkah cards show Frosted Flowers')
remap(CN,CP,'Glow Wild + Caroline card is the peacock colorway')
# tube photos: mirror the clean half (symmetrical mats) - Chinoiserie Elephant, Chinoiserie Blue and Green
for mid,fn in (('mahjandvine.com/porcelain-bloom-copy','elephant'),('mahjandvine.com/chinoiserie-song-bird-copy','bluegreen')):
    p=FX+'f3/dl2/%s_mat.png'%fn
    if mid in M and os.path.exists(p): setmat(mid,Image.open(p)); log['tube_fixed'].append(M[mid]['n'])
# Limoncea + Painted Water Florentine: the brand's flat photo (no tube / racks)
for mid,p in json.load(open(FX+'f3/manual_src.json')).items():
    if mid in M: setmat(mid,Image.open(p)); log['manual_photo'].append(M[mid]['n'])
# Origami Berry is retired (only Midnight Gray is sold); her card shows Berry
OB='www.bambirdboutique.com/origami-neoprene-mat'
M[OB]['n']='Origami Berry'; M[OB]['rt']=True; placeholder(OB,'retired colorway; the store only shows Midnight Gray')
# Petalwing: cut the "Mat only" caption off the bottom
PW='www.viroramahjong.com/petalwing'
if PW in M:
    from matimg import matimg
    k='m|'+PW; im=Image.open(FX+P[k]['file']) if k in P and 'file' in P[k] else None
    if im is not None:
        im=im.crop((0,0,im.width,int(im.height*0.955))); setmat(PW,im); log['caption_cut'].append('Petalwing')
# ---------- 3. no text / graphics in a mat image (Tiffany, Oct 18)
TEXTRULE={'www.macandmillermahjong.com/sweet-dreams-collection-mahjong-mat':'©Mac and Miller watermark on every photo',
 'www.macandmillermahjong.com/heirloom-collection-white-chinoiserie-round-mahjong-mat':'©Mac and Miller watermark on every photo',
 'www.macandmillermahjong.com/mg-flower-mat-name-tbd':'watermark','www.macandmillermahjong.com/let-the-good-times-toile-mat':'watermark',
 'www.macandmillermahjong.com/heirloom-collection-navy-chinoiserie-mahjong-mat':'watermark','www.macandmillermahjong.com/heirloom-collection-white-chinoiserie-scalloped-mahjong-mat':'watermark',
 'www.macandmillermahjong.com/heirloom-fire-fortune-mahjong-mat':'watermark','www.macandmillermahjong.com/laissez-les-bons-temps-rouler-mahjong-mat-pre-order-ships-march-2026':'watermark',
 'alb2:mahj-tile-haus-imperial-lotus':'"Tile Haus" watermark on every photo',
 'www.middleandmainmahjong.com/painted-water-mat':'every photo has racks and tiles on the mat',
 'mahjmood.com/the-bow-and-bloom-mat-collab-with-four-winds-social-pre-order-estimated':'logo graphic + tiles on every photo',
 'fourwindssocial.com/the-bow-and-bloom-mat-collab-with-four-winds-social-pre-order-ships-end-of-september':'logo graphic + tiles on every photo'}
for m,why in TEXTRULE.items():
    if m not in M: continue
    if m in hers: placeholder(m,why)
    else: M[m]['hid']=1; log['hidden_text_rule'].append(f"{M[m]['n']} · {M[m]['bn']} ({why})")
for m in M:
    if 'coral-coast' in m or 'coral-and-coast' in m:
        if m in hers: placeholder(m,'"Tile Haus" watermark')
        else: M[m]['hid']=1; log['hidden_text_rule'].append(M[m]['n'])
# ---------- 4. retired mats
LIB='www.ohmymahjong.com/liberty-mat-w-tube'; HJ='omm:holly-jolly'
for m in (LIB,HJ):
    if m in M: M[m]['rt']=True; M[m]['n']=re.sub(r'\s*\(retired\)$','',M[m]['n']); log['retired'].append(M[m]['n'])
# ---------- 5. tiles
os.makedirs(OUT+'t15',exist_ok=True); tn=0
TOV={'charlestonmahjongclub.com/the-country-club-edition':FX+'f3/dl/c1.img','mahjmood.com/90s-tile-set?v=58077240361263':FX+'f3/dl/c3.img','myfairmahjong.com/park-series':FX+'f3/dl/c6.img'}
albumtiles={s['tile'] for s in D['sets'] if s.get('album')}
for k,v in P.items():
    kind,key=k.split('|',1)
    if kind!='t' or 'file' not in v or key not in T or key in albumtiles or key in TOV: continue
    im=Image.open(FX+v['file']).convert('RGB'); im.thumbnail((1400,1400)); f='t15/%d.jpg'%tn; tn+=1
    im.save(OUT+f,'JPEG',quality=86); T[key]['full']=f; log['tile_hq'].append(T[key]['n'])
for key,p in TOV.items():
    if key in T:
        im=Image.open(p).convert('RGB'); im.thumbnail((1400,1400)); f='t15/%d.jpg'%tn; tn+=1; im.save(OUT+f,'JPEG',quality=86); T[key]['full']=f; log['tile_photo_fixed'].append(T[key]['n'])
GG='www.bespokemahjong.com/holiday-mahjong-its-a-vibe-glitter-glow-tiles'
n0=len(D['sets']); D['sets']=[s for s in D['sets'] if s['tile']!=GG]
if GG in T: T[GG]['hid']=1
log['tile_hidden'].append(f'Glitter Glow (Bespoke teaser, no tile design released; {n0-len(D["sets"])} set removed)')

# ---------- write (re-read the page so concurrent JS edits are kept)
h=open(OUT+'index.html').read(); I0=h.index('const D=')+8; J0=h.index('\n',I0)
line=h[I0:J0].rstrip(); tail=line[-1]
h=h[:I0]+json.dumps(D,separators=(',',':'),ensure_ascii=False)+tail+h[J0:]
if 'b14v1.js' not in h:
    h=h.replace('<script src="b13v1.js"></script>','<script src="b13v1.js"></script><script src="b14v1.js"></script>',1)
    assert 'b14v1.js' in h
open(OUT+'index.html','w').write(h)
open(OUT+'b14v1.js','w').write('window.IMG=Object.assign(window.IMG||{},'+json.dumps(newIMG,separators=(',',':'))+');')
ch={}
for f,u in newMC.items():
    c=int(f.split('/')[1].split('.')[0])//12; ch.setdefault(c,{})[f]=u
for c,o in ch.items():
    p=OUT+'mc/%d.json'%c
    base=json.load(open(p)) if os.path.exists(p) else (json.load(open(FX+'site/mc/%d.json'%c)) if os.path.exists(FX+'site/mc/%d.json'%c) else {})
    base.update(o); json.dump(base,open(p,'w'),separators=(',',':'))
json.dump({k:(v if k!='mat_hq' else len(v)) for k,v in log.items()},open(FX+'f3/fix3_report.json','w'),indent=1,ensure_ascii=False)
json.dump(log['mat_hq'],open(FX+'f3/fix3_res.json','w'))
print({k:len(v) for k,v in log.items()}); print('mc chunks',sorted(ch)[:3],'..',len(ch),'nextf',nextf)
