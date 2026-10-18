# mat image swaps, new mats, hidden crop mats. Imported by patch_data before her lists.
import io,base64,hashlib
from PIL import Image
from common import *
AM=REPO+'assets/mats/'; CUT='/tmp/sun/alb_cut/'
newMC={}; newIMGm={}
nextf=max(int(m['f'].split('/')[1].split('.')[0]) for m in M.values())+1
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
def load(path):
    im=Image.open(path)
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA'); bb=im.getbbox(); im=im.crop(bb) if bb else im
        bg=Image.new('RGB',im.size,(255,255,255)); bg.paste(im,mask=im.split()[3]); return bg
    return im.convert('RGB')
def setimg(mid,path,recolor=True):
    global nextf
    im=load(path); full=im.copy(); full.thumbnail((900,900))
    b=io.BytesIO(); full.save(b,'WEBP',quality=80); f='m/%d.webp'%nextf; nextf+=1
    newMC[f]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    th=im.copy(); th.thumbnail((180,180)); b=io.BytesIO(); th.save(b,'JPEG',quality=74)
    t='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(); h='mt'+hashlib.md5(t.encode()).hexdigest()[:8]
    newIMGm[h]=t; m=M[mid]; m['f']=f; m['th']=h; m['w'],m['h']=full.size; m['c']=False
    if recolor: m['ms'],mf=colors(im); m['mf']=mf or ['neutral']
    m['src']='clean'
def newmat(mid,n,bn,u,dc,path):
    M[mid]={'n':n,'bn':bn,'b':bn,'u':u,'dc':dc,'pa':bool(dc),'nc':False,'rt':False,'c':False,'ml':True,'hol':False}
    setimg(mid,path); byb[nb(bn)].append(mid); byhandle[mid.split('/')[-1]].append(mid)
    if mid not in D['order']: D['order'].append(mid)
SWAP={'www.ohmymahjong.com/hampton-mat-in-tube':AM+'clean/hampton-omm.jpg',
 'mahjsquadshop.com/pink-chinoiserie-mahjong-mat-pink-floral-neoprene-mahjongg-mat-pink-chintz-mahj-mat-colorful-floral-mahj-ongg-mat-spring-1':AM+'mahj-squad/pink-floral-chinoiserie-flat-closeup-WATERMARKED-no-social.jpg',
 'alb:cypress-forest:Dapper 1':AM+'omm-retired/dapper-1.jpg',
 'alb2:charleston-mahjong-club-club-mat':AM+'charleston-mahjong-club/the-club-mat-pink-white-stripe.jpg',
 'alb2:my-fair-mahjong-confetti-lemon-lime':AM+'my-fair-mahjong/confetti-lemon-lime.jpg',
 'alb2:tigre-de-tartan-domino-faded-carolina':AM+'tigre-de-tartan/domino-faded-carolina.jpg',
 'alb2:tigre-de-tartan-domino-oxblood':AM+'tigre-de-tartan/domino-oxblood.jpg',
 'alb2:ozark-mah-jongg-carson-vintage':CUT+'carson-vintage-mat.png',
 'alb2:splash-of-color-preppy-animal-print':AM+'splash-of-color/preppy-animal-print.jpg',
 'alb2:wren-mats-bright-orangey':AM+'wren-mats/bright-orangey-red-and-blue.jpg',
 'alb2:wren-mats-palm-beach':AM+'wren-mats/palm-beach.jpg'}
for k,p in SWAP.items(): setimg(k,p,recolor=k.startswith('alb'))
REMAP={'alb2:mahj-vine-chinoiserie-songbird-2':'mahjandvine.com/chinoiserie-song-bird','alb2:oh-my-mahjong-lorelei-2':'www.ohmymahjong.com/lorelei-mat',
 'alb2:oh-my-mahjong-serengeti-2':'alb:amara:Serengeti','alb2:oh-my-mahjong-enchanted-2':'alb:amara:Enchanted'}
CLEANOK={'alb2:mahjong-moxie-duck-camp','alb2:birdsong-mahjong-heaven-scent','alb2:that-mahjong-moment-evergreen','alb2:ozark-mah-jongg-winslow-1920'}|set(SWAP)
HIDDEN_CROP=[i for i in M if i.startswith('alb2:') and i not in CLEANOK]
for i in HIDDEN_CROP: M[i]['hid']=1
NEW=[('mahjongco.com/mahjong-mat-vintage-oxblood-leather-sclp','Vintage Oxblood Leather','Mahjong by SI','https://mahjongco.com/products/mahjong-mat-vintage-oxblood-leather-sclp','',CUT+'mahjongb-mahjong-mat-vintage-oxblood-leather-sclp.png'),
 ('mahjongco.com/gatsby-mahjong-mat','Gatsby','Mahjong by SI','https://mahjongco.com/products/gatsby-mahjong-mat','',CUT+'mahjongb-gatsby-mahjong-mat.png'),
 ('mahjongco.com/mahjong-by-si-highland-house-mahjong-mat','Highland Heritage Plaid','Mahjong by SI','https://mahjongco.com/products/mahjong-by-si-highland-house-mahjong-mat','',CUT+'mahjongb-mahjong-by-si-highland-house-mahjong-mat.png'),
 ('mahjongco.com/mahjong-by-si-the-hunt-club-mahjong-mat','The Hunt Club','Mahjong by SI','https://mahjongco.com/products/mahjong-by-si-the-hunt-club-mahjong-mat','',CUT+'mahjongb-mahjong-by-si-the-hunt-club-mahjong-mat.png'),
 ('mahjongco.com/mahjong-by-si-tracing-the-tides-mahjong-mat','Tracing the Tides','Mahjong by SI','https://mahjongco.com/products/mahjong-by-si-tracing-the-tides-mahjong-mat','',CUT+'mahjongb-mahjong-by-si-tracing-the-tides-mahjong-mat.png'),
 ('mahjongco.com/the-lodge-mahjong-mat','The Lodge','Mahjong by SI','https://mahjongco.com/products/the-lodge-mahjong-mat','',CUT+'mahjongb-the-lodge-mahjong-mat.png'),
 ('luckydaughters.com/astor-place-mat','Astor Place','Lucky Daughters','https://luckydaughters.com/products/astor-place-mat','',CUT+'ld_astor.png'),
 ('ozarkmahjong.com/winslow-1920-original-navy-blue-mat','Winslow 1920 Navy','Ozark Mahjongg','https://ozarkmahjong.com/products/winslow-1920-original-navy-blue-mat','',CUT+'winslow-1920-original-navy-blue-mat.png'),
 ('ozarkmahjong.com/winslow-1920-rouge-mat','Winslow 1920 Rouge','Ozark Mahjongg','https://ozarkmahjong.com/products/winslow-1920-rouge-mat','',CUT+'winslow-1920-rouge-mat.png'),
 ('ozarkmahjong.com/winslow-1920-noir-mat','Winslow 1920 Noir','Ozark Mahjongg','https://ozarkmahjong.com/products/winslow-1920-noir-mat','',CUT+'winslow-1920-noir-mat.png'),
 ('lbb:fall-flowers','Fall Flowers',"Let's Be Besties",'','https://mahjmatchmaker.com/lets-be-besties-discount-code',CUT+'letsbebe-fall-flowers-mahjong-mat.png'),
 ('lbb:tartan-tweed','Tartan Tweed',"Let's Be Besties",'','https://mahjmatchmaker.com/lets-be-besties-discount-code',CUT+'letsbebe-tartan-tweed-mahjong-mat.png'),
 ('rebecca:rainbow-row','Rainbow Row','Rebecca Illustrated','','',AM+'rebecca-illustrated/rainbow-row.jpg'),
 ('splashofcolorco.com/peony-and-parasol','Peony and Parasol','Splash of Color','','',AM+'splash-of-color/peony-parasol-straight.jpg'),
 ('amore:manor-garden','Manor Garden','Amore Mahjong','','',AM+'amore-mahjong/manor-garden-WATERMARKED-no-social-colorfix.jpg'),
 ('goldenpond:midori-shadows','Midori Shadows','Golden Pond Mahjong','','',AM+'golden-pond-mahjong/midori-shadows.jpg')]
EXIST_BY_NAME={}
for mid,n,bn,u,dc,p in NEW:
    ex=[i for i in M if nb(M[i]['bn'])==nb(bn) and toks(n)==toks(M[i]['n'])]
    if ex: EXIST_BY_NAME[(n,bn)]=ex[0]; continue
    newmat(mid,n,bn,u,dc,p)
MALIAS={('carson vintage','ozark mahjongg'):'alb2:ozark-mah-jongg-carson-vintage',('dapper','oh my mahjong'):'www.ohmymahjong.com/dapper-mat-w-tube',('winslow 1920 navy','ozark mahjongg'):'ozarkmahjong.com/winslow-1920-original-navy-blue-mat'}
AUTO={'amahj/round-top-mahjong-game-mat.jpg','bam-lets-mahjong/cottage-bloom.jpg','bam-lets-mahjong/palm-court.jpg','bam-lets-mahjong/posy-pop-watercolor.jpg','bam-lets-mahjong/secret-garden.jpg','bespoke-mahjong/preppy-pink-garden.jpg','bespoke-mahjong/year-of-the-dragon-plum.jpg','bird-bamboo/paradise-pink.jpg','charleston-mahjong-club/the-club-mat-blue-green-stripe.jpg','mahj-mood/rally-in-pink.jpg','mahj-squad/blue-christmas-mahjong-mat.jpg','mahj-vine/chinoiserie-elephant.jpg','miss-mahjong/garden-party-deep-green-flat.jpg','miss-mahjong/garden-party-lavender-flat.jpg','miss-mahjong/garden-party-powder-blue-flat.jpg','royal-mahjong-society/hydrangea-mahjong-mat.jpg','wren-mats/dancing-poppies.jpg','wren-mats/green-gingham.jpg'}
_bs={}
for b in {M[i]['bn'] for i in M}: _bs.setdefault(re.sub(r'[^a-z0-9]+','-',b.lower().replace('&','').replace("'",'')).strip('-').replace('--','-'),b)
AUTO_DONE=[]
for rel in sorted(AUTO):
    d,fn=rel.split('/'); b=_bs.get(d) or next((v for k,v in _bs.items() if k.startswith(d[:8])),None)
    name=re.sub(r'\.(jpg|png)$','',fn).replace('-mahjong-mat','').replace('-mat','').replace('-flat','').replace('-straight','').replace('-',' ')
    mid=best(name,b)
    if mid and not mid.startswith('alb') and mid not in SWAP: setimg(mid,AM+rel,recolor=False); AUTO_DONE.append(mid)
