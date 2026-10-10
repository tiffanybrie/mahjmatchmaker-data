import json,base64,io,subprocess
import numpy as np
from rembg import remove,new_session
SES=new_session('u2netp')
from PIL import Image
import sys; sys.path.insert(0,'/tmp/mb')
from bgcut import bgcut,unroll
sys.path.insert(0,'/tmp/mb')
import bbrack
BLANK=bbrack.make_blank()
PILE=json.load(open('/tmp/mb/pile.json'))
DATA=json.load(open('/home/claude/mahjmatchmaker-data/data.json'))
MF=json.load(open('matfix.json'))
import urllib.request
VAR={'Peace Love Mahjong Oak':'Oak','Bam Bird Boutique Walnut':'Walnut'}
def get(u):return subprocess.run(['curl','-s','-m','25','-L',u],capture_output=True).stdout
def variant_img(domain,handle,vname):
    j=json.loads(get(f'https://{domain}/products/{handle}.json'))['product']
    iid=[v.get('image_id') for v in j['variants'] if v['title'].lower()==vname.lower()]
    for im in j['images']:
        if iid and im['id']==iid[0]:
            s=im['src'];s+=('&' if '?' in s else '?')+'width=700'
            return Image.open(io.BytesIO(get(s))).convert('RGB')
BB={x['name']:x['hex'] for x in json.load(open('/home/claude/mahjmatchmaker-data/work/bbracks.json'))}
def bb_svg(hexc):
    import colorsys
    r,g,b=(int(hexc[i:i+2],16) for i in (1,3,5));dk='#%02x%02x%02x'%(int(r*.78),int(g*.78),int(b*.78));lt='#%02x%02x%02x'%(min(255,int(r*1.12+12)),min(255,int(g*1.12+12)),min(255,int(b*1.12+12)))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 120"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lt}"/><stop offset="1" stop-color="{hexc}"/></linearGradient></defs><rect x="4" y="22" width="632" height="80" rx="14" fill="url(#g)" stroke="{dk}" stroke-width="3"/><rect x="22" y="38" width="596" height="26" rx="8" fill="{dk}" opacity=".35"/><rect x="22" y="40" width="596" height="3" rx="2" fill="#fff" opacity=".35"/><rect x="40" y="76" width="560" height="10" rx="5" fill="{dk}" opacity=".25"/></svg>'
    return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
plan=json.load(open('plan.json'));F=json.load(open('fetched.json'));P=plan['prods']
def b64(im,fmt,q=80):
    b=io.BytesIO();im.save(b,fmt,quality=q);return 'data:image/%s;base64,'%fmt.lower()+base64.b64encode(b.getvalue()).decode()
def clean_alpha(im):
    a=np.asarray(im).copy().astype(float)
    al=a[...,3]; al=np.clip((al-70)*255/(185),0,255); a[...,3]=al
    return Image.fromarray(a.astype('uint8'),'RGBA')
from scipy.ndimage import binary_fill_holes
def fill(im):
    a=np.asarray(im).copy();m=a[...,3]>128;f=binary_fill_holes(m);h=f&~m;a[...,3][h]=255
    return Image.fromarray(a,'RGBA')
def isbad(nm): return any(b in nm.lower() for b in ['gray malin','yotd','hunt club','light blue','iridescent','peace love mahjong oak','viola'])
prods={}
for pid,p in P.items():
    r=F.get(pid)
    if not r or 'cut' not in r: continue
    ok=True
    if p['kind']=='mat':
        fp=MF.get(pid,{}).get('file',r['file'])
        src=Image.open(fp).convert('RGB');src.thumbnail((700,700))
        cut,u=bgcut(src,14,'thresh');cut=unroll(cut)
        w,h=cut.size;fl=(np.asarray(cut)[...,3]>128).sum()/(w*h);asp=min(w,h)/max(w,h)
        rg=np.asarray(cut.convert('RGB')).astype(float).mean(axis=2);a2=np.asarray(cut)[...,3]>128;hh=rg.shape[0];st=rg[int(hh*0.95):][a2[int(hh*0.95):]];roll=bool(st.size and (st<45).mean()>0.5 and rg[a2].mean()>70)
        ok=u>=0.95 and fl>0.9 and asp>0.88 and not roll
        ph=src.copy()
        cut.thumbnail((520,520))
    else:
        src=None
        if p['kind']=='rack' and p['name'] in VAR:
            try: src=variant_img(p['domain'],p['handle'],VAR[p['name']])
            except Exception as ex: print('variant fail',p['name'],ex)
        if src is None: src=Image.open(r['file']).convert('RGB')
        src.thumbnail((700,700))
        c2,u=bgcut(src)
        if c2 is not None and u>=0.95:
            cut=c2
        else:
            cut=clean_alpha(Image.open(r['cut']).convert('RGBA'));ok=False
        bb=cut.getbbox();cut=cut.crop(bb) if bb else cut;cut.thumbnail((420,420))
        ph=src.copy()
    ph.thumbnail((360,360))
    hide=(not ok) and bool(np.asarray(ph.resize((50,50)))[:2].mean()<25)
    prods[pid]=dict(hide=hide,k=p['kind'],n=p['name'],cut=b64(cut,'WEBP',78),photo=b64(ph,'JPEG',72),clean=bool(ok),url='https://'+pid)
# --- Bird & Bamboo: one recoloured rack per colour (blank = Tiffany's isolated Canva rack, colours = her swatch hex)
for k in [k for k,v in P.items() if v['name']=='Bird & Bamboo Light Blue']: prods.pop(k,None)
BBL=json.load(open('/home/claude/mahjmatchmaker-data/work/bbracks.json'))
base=BLANK.copy();base.thumbnail((420,80))
for x in BBL:
    rc=bbrack.recolor(base,x['hex'])
    prods['bb:'+x['name']]=dict(hide=False,k='rack',n='Bird & Bamboo '+x['name'],cut=b64(rc,'WEBP',80),photo=b64(rc,'WEBP',80),clean=True,skin=True,url=x['url'])
# --- Miss Mahjong acrylic racks: product photos are tight crops (no clean cutout) -> colour preview on the blank rack
def _mmhex(f):
    a=np.asarray(Image.open(f).convert('RGB').resize((200,140))).astype(float)
    mx=a.max(2);mn=a.min(2);sat=(mx-mn)/(mx+1e-6)
    m=(mx<246)&(mx>60)
    if (sat[m]>0.18).sum()>500: m=m&(sat>0.18)
    c=np.median(a[m],axis=0);return '#%02x%02x%02x'%tuple(int(x) for x in c)
for _pid,_p in P.items():
    if _p['kind']=='rack' and _pid.startswith('missmahjong.com/') and _pid in prods and not prods[_pid]['clean']:
        _hx=_mmhex(F[_pid]['file']);_rc=bbrack.recolor(base,_hx)
        prods[_pid].update(cut=b64(_rc,'WEBP',80),clean=True,skin=True)
# --- Peace Love Mahjong colour variants used in her matches
PLM_ID=[k for k,v in P.items() if v['name']=='Peace Love Mahjong Oak'][0];PLM=P[PLM_ID]
def plm_real(color):
    import os
    f=f'/tmp/mb/plm/r_{color.replace(" ","_")}.png'
    if not os.path.exists(f): return None
    c=Image.open(f).convert('RGBA');c.thumbnail((420,420));return c
def add_plm(color):
    c=plm_real(color)
    if c is not None:
        pid='plm:'+color;prods[pid]=dict(hide=False,k='rack',n='Peace Love Mahjong '+color,cut=b64(c,'WEBP',82),photo=b64(c,'WEBP',82),clean=True,url='https://'+PLM_ID);return pid
    try: src=variant_img(PLM['domain'],PLM['handle'],color)
    except Exception: src=None
    if src is None: return None
    src.thumbnail((700,700));c2,u=bgcut(src);ok=bool(c2 is not None and u>=0.95)
    cut=c2 if ok else src.convert('RGBA')
    if ok:
        bb=cut.getbbox();cut=cut.crop(bb) if bb else cut
    cut.thumbnail((420,420));ph=src.copy();ph.thumbnail((360,360))
    pid='plm:'+color
    prods[pid]=dict(hide=False,k='rack',n='Peace Love Mahjong '+color,cut=b64(cut,'WEBP',78),photo=b64(ph,'JPEG',72),clean=ok,url='https://'+PLM_ID)
    return pid
for _c in ['Chartreuse','Dark Green','Aqua','French Blue','Navy','Purple','Pink','Light Pink','Lilac','Red','Cobalt','Oak','White','Mint']:
    if 'plm:'+_c not in prods and _c!='Oak': add_plm(_c)
for _c in ['White','Mint']:
    if 'plm:'+_c in prods: prods['plm:'+_c]['skin']=True   # real PLM rack shape recoloured from her swatch photo
_oc=plm_real('Oak')
if _oc is not None: prods[PLM_ID].update(cut=b64(_oc,'WEBP',82),photo=b64(_oc,'WEBP',82),clean=True,hide=False)
# --- Heritage 2.0 racks were mislabelled Blond Tortoise; her cards show OMM's Burl rack
for _k in [k for k,v in prods.items() if v['n']=='Oh My Mahjong Blond Tortoise']: prods.pop(_k)
try:
    _j=json.loads(get('https://www.ohmymahjong.com/products/burlwood-rack.json'))['product']
    _bi=None;_bs=-9
    for _im in _j['images'][:6]:
        _s=Image.open(io.BytesIO(get(_im['src']+'?width=700'))).convert('RGB');_s.thumbnail((700,700));_c,_u=bgcut(_s)
        _sc=-1 if (_c is None or _u<0.95) else _u
        if _sc>_bs:_bs,_bi=_sc,(_s,_c)
    _s,_c=_bi;_ok=_bs>0
    _cut=_c if _ok else _s.convert('RGBA')
    if _ok:
        _bb=_cut.getbbox();_cut=_cut.crop(_bb) if _bb else _cut
    _cut.thumbnail((420,420));_ph=_s.copy();_ph.thumbnail((360,360))
    prods['www.ohmymahjong.com/burlwood-rack']=dict(hide=False,k='rack',n='Oh My Mahjong Burl',cut=b64(_cut,'WEBP',80),photo=b64(_ph,'JPEG',72),clean=bool(_ok),url='https://www.ohmymahjong.com/products/burlwood-rack')
except Exception as _e: print('burl fail',_e)
# --- OMM racks: use the single-rack product shot, cut out, levelled and trimmed to the rack (/tmp/mb/straight.py -> /tmp/mb/rkalt)
import os as _os
for _h in ['tortoise-shell-rack-pusher','white-rack-pusher','hot-pink-rack-pusher','pink-quartz-rack-and-pusher-set','burlwood-rack']:
    _f='/tmp/mb/rkalt/'+_h+'.png';_k='www.ohmymahjong.com/'+_h
    if _os.path.exists(_f) and _k in prods:
        _c=Image.open(_f).convert('RGBA');_c.thumbnail((520,520));prods[_k].update(cut=b64(_c,'WEBP',82),clean=True)
for _f,_k in [('/tmp/mb/rkalt/walnut.png','www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'),('/tmp/mb/rkalt/oak13.png',PLM_ID)]:
    if _os.path.exists(_f) and _k in prods:
        _c=Image.open(_f).convert('RGBA');_c.thumbnail((520,520));prods[_k].update(cut=b64(_c,'WEBP',82),clean=True,hide=False)
# --- My Fair Mahjong acrylic racks: each colour variant has a clean tile-free stack photo on white -> real isolated cutout
import colorsys
def _fam(h,s_,v):
    if v<0.16: return 'black'
    if s_<0.10 or (v>0.93 and s_<0.14): return 'neutral'
    d=h*360
    if (15<=d<50) and (s_<0.5 and v<0.75): return 'neutral'
    if d<12 or d>=345: return 'red' if s_>0.55 and v<0.85 else 'pink'
    if d<40: return 'orange'
    if d<68: return 'yellow'
    if d<160: return 'green'
    if d<195: return 'teal'
    if d<255: return 'blue'
    if d<290: return 'purple'
    return 'pink'
def add_variant_racks(domain,handle,brand):
    try: j=json.loads(get(f'https://{domain}/products/{handle}.json'))['product']
    except Exception as ex: print('vr fail',brand,ex);return 0
    ims={i['id']:i for i in j['images']};n=0
    for v in j['variants']:
        im=ims.get(v.get('image_id'))
        if not im or any(w in v['title'] for w in ('Pearl','Malachite','Ribbon','Transparent')): continue   # those variant photos carry text overlays / tiles
        try:
            src=Image.open(io.BytesIO(get(im['src']+('&' if '?' in im['src'] else '?')+'width=700'))).convert('RGB')
        except Exception: continue
        c2,u=bgcut(src)
        if c2 is None or u<0.95: continue
        bb=c2.getbbox();c2=c2.crop(bb) if bb else c2;c2.thumbnail((420,420));ph=src.copy();ph.thumbnail((360,360))
        nm=brand+' '+v['title'].replace('Solid ','').replace(' / Chartreuse','')
        pid='vr:'+brand+':'+v['title']
        prods[pid]=dict(hide=False,k='rack',n=nm,cut=b64(c2,'WEBP',80),photo=b64(ph,'JPEG',72),clean=True,url=f'https://{domain}/products/{handle}?variant={v["id"]}')
        a=np.asarray(c2).astype(float);m=a[...,3]>200;r,g,b_=np.median(a[...,:3][m],axis=0)/255
        prods[pid]['f']=_fam(*colorsys.rgb_to_hsv(r,g,b_));n+=1
    return n
print('myfair racks',add_variant_racks('myfairmahjong.com','acrylic-mahjong-racks','My Fair Mahjong'))
# --- universal "goes with everything" racks (Tiffany: first rack you ever buy)
import os as _os
UNI=[]
def _uni(pid,name,url,src,mult_ok=True):
    src=src.convert('RGB');src.thumbnail((700,700));ph=src.copy();ph.thumbnail((360,360))
    c2,u=bgcut(src);mult=False
    if c2 is not None and u>=0.95:
        bb=c2.getbbox();cut=c2.crop(bb) if bb else c2;cut.thumbnail((420,420));cuts=b64(cut,'WEBP',80)
    else:
        mult=True;t=src.copy();t.thumbnail((420,420));cuts=b64(t,'JPEG',80)
    prods[pid]=dict(hide=False,k='rack',n=name,cut=cuts,photo=b64(ph,'JPEG',72),clean=True,url=url,uni=True)
    if mult:prods[pid]['mult']=True
    UNI.append(pid)
try:
    _uni(PLM_ID,'Peace Love Mahjong Oak','https://peacelovemahjong.com/products/mahjong-racks-racks-pushers-set-of-4?variant=46833181557028&ref=Mahjmatch',variant_img(PLM['domain'],PLM['handle'],'Oak'))
except Exception as ex: print('uni oak',ex)
if _os.path.exists('/tmp/mb/rkalt/oak13.png'):
    _c=Image.open('/tmp/mb/rkalt/oak13.png').convert('RGBA');_c.thumbnail((520,520));prods[PLM_ID]['cut']=b64(_c,'WEBP',82)
try:
    _q=json.loads(get('https://myfairmahjong.com/products/acrylic-mahjong-racks.json'))['product']
    _vid=[v for v in _q['variants'] if v['title']=='Transparent Clear'][0]
    _im=[i for i in _q['images'] if i['id']==_vid['image_id']][0]
    _uni('vr:My Fair Mahjong:Transparent Clear','My Fair Mahjong Clear','https://myfairmahjong.com/products/acrylic-mahjong-racks?variant=%s'%_vid['id'],Image.open(io.BytesIO(get(_im['src']+'?width=700'))))
except Exception as ex: print('uni mfm',ex)
try:
    _h=json.loads(get('https://www.middleandmainmahjong.com/products/hawksbill-heritage-mahjong-rack-and-pusher-set-of-4.json'))['product']
    _uni('mm:Hawksbill','Middle & Main Hawksbill Heritage (tortoise)','https://www.middleandmainmahjong.com/products/hawksbill-heritage-mahjong-rack-and-pusher-set-of-4?sca_ref=10574197.BKiJ48vXYfYfD31E',Image.open(io.BytesIO(get(_h['images'][4]['src']+'?width=700'))))
except Exception as ex: print('uni mm',ex)
for _p in UNI:print('uni',_p,prods[_p]['n'],'mult' if prods[_p].get('mult') else 'cut')
# --- rebuild each set's matches from her real data (every rack colour she matched, in her order)
T,M,X,R=DATA['T'],DATA['M'],DATA['X'],DATA['R']
byname={v['n']:k for k,v in prods.items() if v['k']=='rack'}
LEAD={(0,'Chinoiserie Songbird'):[11,12,9]}  # her lead racks per match (Amara + Songbird: B&B Hot Pink, PLM Chartreuse, B&B Teal)
def rack_id(nm):
    if nm.startswith('Bird & Bamboo '):
        k='bb:'+nm[len('Bird & Bamboo '):];return k if k in prods else None
    if nm.startswith('Peace Love Mahjong ') and nm!='Peace Love Mahjong Oak':
        k='plm:'+nm[len('Peace Love Mahjong '):]
        return k if (k in prods) else add_plm(nm[len('Peace Love Mahjong '):])
    return byname.get(nm)
for pid,f in PILE.items():
    if pid in prods:
        pi=Image.open(f).convert('RGB');pi.thumbnail((520,520));prods[pid]['pile']=b64(pi,'JPEG',74)
PNAME={b[1].replace('www.',''):b[0] for b in json.load(open('/home/claude/mahjmatchmaker-data/catalog.json'))['B']}
PDIS={b[1].replace('www.',''):b[3] for b in json.load(open('/home/claude/mahjmatchmaker-data/catalog.json'))['B']}
PARTNER={b[1].replace('www.','') for b in json.load(open('/home/claude/mahjmatchmaker-data/catalog.json'))['B']}
SC=json.load(open('/tmp/mb/scatter.json'))
from PIL import ImageFilter
for pid,f in SC.items():
    if pid not in prods: continue
    si=Image.open(f).convert('RGB');si.thumbnail((600,600))
    if np.asarray(si)[:6].mean()<45: continue          # black-backdrop grid, not a scatter
    o,u=bgcut(si,24)
    if o is None or u<0.95: continue
    al=o.getchannel('A').filter(ImageFilter.MinFilter(3))
    o.putalpha(al);bb=o.getbbox();o=o.crop(bb) if bb else o;o.thumbnail((520,520))
    prods[pid]['scatter']=b64(o,'WEBP',80);prods[pid]['scatterCut']=True
# --- real shop links (with her affiliate refs). Never build URLs from the internal key (that dropped /products/ -> 404)
import re as _re
def _host(u):return u.split('//')[1].split('/')[0].replace('www.','')
LK={}
for t in T:LK[('tile',t[1],_host(t[4]) if t[4] else '')]=t[4]
for m in M:
    if m[2]:LK[('mat',m[0],_host(m[2]))]=m[2]
for r in R:LK[('rack',r[0],'')]=r[1]
for pid,v in prods.items():
    host=_host(v['url']);u=None
    if v['k']=='rack':u=LK.get(('rack',v['n'],''))
    else:u=LK.get((v['k'],v['n'],host))
    if not u:
        u=v['url']
        if '/products/' not in u and '/collections/' not in u:
            h,_,rest=u.split('//')[1].partition('/');u='https://'+h+'/products/'+rest
    v['url']=u
BR={'ohmymahjong.com':'Oh My Mahjong','sundaymahjong.com':'Sunday Mahjong','peacelovemahjong.com':'Peace Love Mahjong','birdandbamboo.com':'Bird & Bamboo','missmahjong.com':'Miss Mahjong','bambirdboutique.com':'Bam Bird Boutique','mahjongrowandco.com':'Mahjong Row & Co.'}
FAM={('Bird & Bamboo '+x['name']):x['fam'] for x in BBL}
# --- retired tile sets: no shop page; use the tile photo from Tiffany's album color card, link to her album
import os as _os2
_AU=open('/home/claude/mahjmatchmaker-data/config/album-urls.txt').read().split()
for _s in plan['sets']:
    if _s['tile'].startswith('ret:'):
        _slug=_s['slug'];_f='/tmp/mb/ret/'+_slug+'.jpg'
        if not _os2.path.exists(_f): continue
        _im=Image.open(_f).convert('RGB');_im.thumbnail((520,520))
        _u=[u for u in _AU if u.rstrip('/').endswith('/'+_slug+'-mahjong-tile-matches')]
        prods[_s['tile']]=dict(hide=False,k='tile',n=_s['name'],cut=b64(_im,'JPEG',80),photo=b64(_im,'JPEG',80),pile=b64(_im,'JPEG',80),clean=True,url=(_u[0] if _u else 'https://www.mahjmatchmaker.com'),retired=True)
for pid,v in prods.items():
    host=v['url'].split('//')[1].split('/')[0].replace('www.','')
    v['b']=BR.get(host,host);v['p']=host in PARTNER
    if v['p'] and PDIS.get(host):v['d']='https://mahjmatchmaker.com'+PDIS[host]
    v['nc']=(host=='ymimports.com')
    if host in PNAME:v['bn']=PNAME[host]
    if v['n'] in FAM: v['f']=FAM[v['n']]
for _k,_v in prods.items():
    if _v.get('retired'):_v.update(b='Oh My Mahjong',bn='Oh My Mahjong',p=False,nc=False)
sets=[]
for s in plan['sets']:
    if s['tile'] not in prods: continue
    ti=[n for n,t in enumerate(T) if t[0]==s['slug']]
    ms=[]
    for m in s['matches']:
        if m['mat'] not in prods: continue
        racks=[]
        if ti:
            for x in X:
                if x[0]==ti[0] and M[x[1]][0]==m['matName']:
                    rr=LEAD.get((ti[0],M[x[1]][0]),[]);rr=rr+[r for r in x[4] if r not in rr];racks=[rack_id(R[r][0]) for r in rr];racks=[r for r in dict.fromkeys(racks) if r];break
        if not racks: racks=[r for r in m['racks'] if r in prods]
        ms.append(dict(mat=m['mat'],racks=racks,n=m['n'],take=m['take']))
    _au=[u for u in open('/home/claude/mahjmatchmaker-data/config/album-urls.txt').read().split() if u.rstrip('/').endswith('/'+s['slug']+'-mahjong-tile-matches')]
    sets.append(dict(slug=s['slug'],name=s['name'],maker=s['maker'],tile=s['tile'],matches=ms,album=(_au[0] if _au else '')))
def _hx(uri):
    try:
        im=Image.open(io.BytesIO(base64.b64decode(uri.split(',',1)[1]))).convert('RGBA');a=np.asarray(im).astype(float);m=a[...,3]>200
        c=np.median(a[...,:3][m],axis=0);return '#%02x%02x%02x'%tuple(int(x) for x in c)
    except Exception: return '#cccccc'
for _k,_v in prods.items():
    if _v['k']=='rack':
        _v['hx']=_hx(_v['cut'])
        if not _v.get('f') and _v['hx']!='#cccccc':
            _r,_g,_b2=[int(_v['hx'][i:i+2],16)/255 for i in (1,3,5)];_v['f']=_fam(*colorsys.rgb_to_hsv(_r,_g,_b2))
_FAMOF={t[0]:(t[5][0] if t[5] else 'neutral') for t in DATA['T']}
TAGS={'amara':'The Lilly Pulitzer of tiles: preppy pink & kelly green'}   # her own lines; add more as she gives them
for _s in sets:_s['fam']=_FAMOF.get(_s['slug'],'neutral');_s['tag']=TAGS.get(_s['slug'],'')
for _s in sets:
    if _s['tile'] in prods: prods[_s['tile']]['f']=_s['fam']
import colorsys as _cs
_BC=json.load(open('/tmp/mb/backcol.json'))
_TC=json.load(open('/tmp/mb/edit/titlecol.json'))
for _s in sets:
    if _s['slug'] in _TC:
        _s['tc']=_TC[_s['slug']];continue  # her color card title color wins when an album exists
    c=_BC.get(_s['tile'])
    if c:
        h,l,sa=_cs.rgb_to_hls(*[x/255 for x in c])
        if l>.55:l=.55
        if l<.2:l=.2
        r,g,b2=_cs.hls_to_rgb(h,l,sa);_s['tc']='#%02x%02x%02x'%(int(r*255),int(g*255),int(b2*255))
LG=json.load(open('/tmp/mb/logos/map.json'))
LOGOS={}
for n,f in LG.items():
    li=Image.open('/tmp/mb/logos/'+f).convert('RGBA');LOGOS[n]=b64(li,'PNG',90) if False else 'data:image/png;base64,'+base64.b64encode((lambda bio:(li.save(bio,'PNG',optimize=True),bio.getvalue())[1])(io.BytesIO())).decode()
json.dump(dict(prods=prods,sets=sets,logos=LOGOS,uni=UNI),open('data_embed.json','w'),separators=(',',':'))
t=open('tpl.html').read()
if '<meta charset' not in t: t='<meta charset="utf-8">\n'+t
open('tpl.html','w').write(t)
open('/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/match-builder-prototype.html','w').write(t.replace('__DATA__',open('data_embed.json').read()))
print('ok',len(prods))
