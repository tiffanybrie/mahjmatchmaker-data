# Christmas style carousel v3 (Nov 17 pm): v2 + no '1 of 2' labels, real Find Your Mat-ch lockup image, last slide = the real app on a phone
# (Amara tiles by Oh My Mahjong swiping Clara, captured from mahjmatchmaker.com/find-your-match), Comment MATCH instead of link in bio.
import json, re, random, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
R='/home/claude/tiffanybrie/mahjmatchmaker-data/'
OUT=R+'assets/social/christmas-style-nov17/v3/'
import os; os.makedirs(OUT,exist_ok=True)
LOCK=R+'assets/brand/fym-lockup/find-your-mat-ch-lockup.png'
G=R+'assets/mats/gallery/'
FD=R+'scripts/social/tileprofile/fonts/'
CAP=FD+'Caprasimo.ttf'; BIT=R+'scripts/albumcard/woodfix/Bitter-Bold.ttf'; BIT6=FD+'bitter-latin-600-normal.woff2'; PF=FD+'playfair-display-latin-600-italic.woff2'
NAVY=(6,42,85); RED=(179,32,42); GREEN=(31,90,60); MUTED=(70,105,145); GOLD=(233,199,123)
snap=json.load(open(R+'config/partner-products-snapshot.json'))
gal={it[0]:it for it in json.load(open(R+'site/livepatch/matgallery/data/matgallery-v120.json'))}
def price(slug):
    link=gal[slug][3]; u=urllib.parse.urlparse(link); q=urllib.parse.parse_qs(u.query)
    path=urllib.parse.unquote(q.get('redirect',[u.path])[0]); h=re.search(r'/products/([^/?#]+)',path).group(1)
    for dom,v in snap.items():
        if dom.replace('www.','')==u.netloc.replace('www.','') and h in v:
            p=v[h]; assert p['avail'], slug; assert p['min']>0, slug; return p['min']
    raise Exception('noprice '+slug)
def S(brand,name): # find slug by brand + exact gallery name
    m=[k for k,v in gal.items() if v[2]==brand and v[1]==name]; assert len(m)==1,(brand,name,m); return m[0]
LBB="Let's Be Besties"; PLM='Peace Love Mahjong'; AR='Anders Ruff'; OMM='Oh My Mahjong'; BB='Bam Bird Boutique'
STY={
'plaid':[(AR,'Tartan Tidings',None),(AR,'Evergreen & Tartan',None),(AR,'Candy Cane Lane',None),(AR,'Heritage Tartan',None),(OMM,'Yuletide',None),("Bam! Let's Mahjong",'Holly Jolly Christmas',None),('My Fair Mahjong','Plaid Tidings',None),(BB,'Plaid Neoprene – Green with Pink','Green with Pink Plaid'),(BB,'Plaid Neoprene – Green and Blue','Green and Blue Plaid'),
         (LBB,'Ho Ho Ho! Christmas',None),(LBB,'Grinches',None),(LBB,'Tartan Tweed',None),(LBB,'Olive Plaid',None),(PLM,'Gingham - Red','Red Gingham'),(PLM,'Sugarplum Plaid',None),(LBB,'Holly Jolly Gingham',None),(LBB,'Merry Gnome Mas',None),(BB,'Plaid Neoprene – Pink on Pink','Pink on Pink Plaid')],
'pink':[(AR,'Very Merry Mahj',None),('Britt Mills','Nutcracker Leatherette','Nutcracker'),('My Fair Mahjong','Peppermint Wishes',None),(OMM,'Clara',None),(OMM,'Merriment',None),(PLM,'Tied With A Bow',None),(PLM,'Candy Cane Lane',None),(LBB,'Orange and Pink Christmas',None),(LBB,'Jingle Jungle',None),
        ('Bespoke Mahjong','Gray Malin A Very Merry Getaway (double-sided)','A Very Merry Getaway'),(LBB,'Merry & Bright, Holiday Prism','Merry & Bright'),(LBB,'Bow & Baubles Christmas',None),(LBB,'MOD Merry',None),(PLM,'Poinsettia & Peace',None),('Bespoke Mahjong','The Chalet (Let It Snow / double-sided)','The Chalet'),(LBB,'Fair Isle Pink Snowflakes',None),(PLM,'Merry Mix',None),(PLM,'Vintage Noel',None)],
'green':[('Bespoke Mahjong','Bespoke x Corey Paige - Holiday Love Mat - Red/Green','Holiday Love'),(AR,'Watercolor Christmas Tree',None),('Britt Mills','Winter Berry Leatherette','Winter Berry'),(PLM,'Perfectly Wrapped',None),('Mahj Mood','Holly Berry',None),(LBB,'Christmas Ribbon Rhapsody',None),(BB,'Bandana – Holiday Green/Pink accents','Holiday Green Bandana'),(LBB,'Christmas Lights',None),(LBB,'Christmas Village',None),
         (LBB,'Emerald Night Christmas',None),(LBB,'Festive Frost',None),(LBB,'Garland Christmas',None),(LBB,'Holly Coastal Christmas',None),(PLM,'Spirit of Christmas',None),(PLM,'Peace Love & Mistletoe',None),(LBB,'Candy Cane Christmas',None),(PLM,'Nutcracker Noel - Red & Green','Nutcracker Noel'),('Mahj Squad',"Clara's Dream Christmas",None)],
'blue':[(OMM,'Winterberry',None),('Bespoke Mahjong','Bespoke x Corey Paige - Holiday Love Mat - Blue','Holiday Love Blue'),(AR,'Tartan Toile Noël',None),(PLM,'Frosted Flowers',None),('Virora Mahjong','Hiverelle',None),(LBB,'Alpine Snowflakes',None),(OMM,'Holly Jolly',None),(PLM,'Pretty Little Christmas',None),('Mahj Squad','Blue Christmas',None),
        (LBB,'Snowflake Holiday',None),(LBB,'Whoosh',None),(LBB,'Winter Jewel',None),(LBB,'Apres Skiing in Teal',None),(LBB,'Green Apres Skiing with Skiers','Green Apres Skiing'),(BB,'Holiday Neoprene',None),('Hip Hip Mahjong','Nativity',None),(LBB,'Beachy Wreath Christmas',None),(AR,"Santa's Mahjong Mail",None)],
}
W,H=1080,1350
def bg(seed):
    im=Image.new('RGB',(W,H)); px=im.load()
    import math
    stops=[(0,(255,255,255)),(.38,(238,246,252)),(.75,(217,234,246)),(1,(198,221,239))]
    cx,cy=W/2,H*.42; rx,ry=W*.75,H*.75
    row=[]
    for y in range(H):
        for x in range(W):
            t=min(1,math.hypot((x-cx)/rx,(y-cy)/ry))
            for i in range(3):
                a,ca=stops[i]; b,cb=stops[i+1]
                if t<=b:
                    f=(t-a)/(b-a); px[x,y]=tuple(int(ca[k]+(cb[k]-ca[k])*f) for k in range(3)); break
    # snow
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(lay); ds=ImageDraw.Draw(sh); rnd=random.Random(seed)
    for _ in range(110):
        r=rnd.uniform(3,9); x=rnd.uniform(0,W); y=rnd.uniform(0,H); a=int(255*rnd.uniform(.55,1))
        ds.ellipse((x-r,y-r+3,x+r,y+r+3),fill=(60,110,160,int(a*.35)))
        d.ellipse((x-r-2,y-r-2,x+r+2,y+r+2),fill=(120,165,205,int(a*.55))); d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,a))
    base=im.convert('RGBA'); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3))); base.alpha_composite(lay)
    return base
_BG={}
def getbg(seed):
    if seed not in _BG: _BG[seed]=bg(seed)
    return _BG[seed].copy()
def trim(im):
    rgb=im.convert('RGB'); bgw=Image.new('RGB',rgb.size,(255,255,255))
    diff=ImageChops.difference(rgb,bgw).convert('L').point(lambda v:255 if v>40 else 0)
    bb=diff.getbbox(); im=rgb.crop(bb) if bb else rgb
    w,h=im.size; k=int(min(w,h)*0.02); im=im.crop((k,k,w-k,h-k)); w,h=im.size; s=min(w,h); return im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))
def rmask(size,r):
    m=Image.new('L',size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,size[0]-1,size[1]-1),r,fill=255); return m
def place(base,img,x,y,r=22,blur=14,off=10,alpha=95):
    sh=Image.new('RGBA',base.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((x,y+off,x+img.size[0],y+img.size[1]+off),r,fill=(30,70,120,alpha))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    base.paste(img,(x,y),rmask(img.size,r))
def mat(slug,s): return trim(Image.open(G+slug+'.webp')).resize((s,s),Image.LANCZOS)
def fit(d,text,font,size,maxw):
    while size>12:
        f=ImageFont.truetype(font,size)
        if d.textlength(text,font=f)<=maxw: return f
        size-=1
    return f
def ct(d,y,text,font,fill,cx=W/2):
    d.text((cx-d.textlength(text,font=font)/2,y),text,font=font,fill=fill)
def pill(base,cy,text,font,fill=RED,fg=(255,255,255),padx=34,h=58):
    d=ImageDraw.Draw(base); w=d.textlength(text,font=font)+2*padx; x=(W-w)/2
    sh=Image.new('RGBA',base.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((x,cy+6,x+w,cy+h+6),h/2,fill=(30,70,120,70)); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d.rounded_rectangle((x,cy,x+w,cy+h),h/2,fill=fill); bb=font.getbbox(text); d.text((x+padx,cy+(h-(bb[3]-bb[1]))/2-bb[1]),text,font=font,fill=fg)
rows=[]; order=['plaid','pink','green','blue']; NAME={'plaid':'Plaid','pink':'Pink','green':'Green','blue':'Blue'}
fK=ImageFont.truetype(BIT,27)
n=2
for key in order:
    items=STY[key]
    for part in range(2):
        base=getbg(n); d=ImageDraw.Draw(base)
        # style row
        labels=[NAME[k].upper() for k in order]; sp=56
        tw=sum(d.textlength(l,font=fK) for l in labels)+3*sp; x=W/2-tw/2; y=46
        for i,l in enumerate(labels):
            c=RED if order[i]==key else (120,150,185); d.text((x,y),l,font=fK,fill=c); lw=d.textlength(l,font=fK)
            if order[i]==key: d.rounded_rectangle((x,y+38,x+lw,y+43),2,fill=RED)
            x+=lw
            if i<3: d.ellipse((x+sp/2-4,y+12,x+sp/2+4,y+20),fill=(150,180,210)); x+=sp
        title=NAME[key]; fT=ImageFont.truetype(CAP,96); fP=ImageFont.truetype(PF,40)
        ct(d,92,title,fT,NAVY)
        S_=266; gx=46; M=(W-3*S_-2*gx)//2; top=214; rowh=S_+84
        for i,(brand,gname,short) in enumerate(items[part*9:part*9+9]):
            slug=S(brand,gname); p=price(slug); nm=short or gname
            rows.append(dict(style=key,name=nm,brand=brand,price=p,slug=slug))
            cx=M+(i%3)*(S_+gx); cy=top+(i//3)*rowh
            place(base,mat(slug,S_),cx,cy)
            fn=fit(d,nm,BIT,26,S_+gx-6); ct(d,cy+S_+12,nm,fn,NAVY,cx+S_/2)
            bl=f"{brand} · ${p:.0f}"; fb=fit(d,bl,BIT6,22,S_+gx-6); ct(d,cy+S_+44,bl,fb,MUTED,cx+S_/2)
        pill(base,1272,"Code MAHJMATCH works at every brand here",ImageFont.truetype(BIT,26),h=54)
        base.convert('RGB').save(OUT+f'slide{n:02d}-{key}-{part+1}.jpg',quality=92); n+=1
# cover
base=getbg(1); d=ImageDraw.Draw(base)
wm=Image.open(R+'assets/brand/mahjmatchmaker-wordmark-holiday-notag.png').convert('RGBA'); wm=wm.resize((420,int(420*wm.size[1]/wm.size[0])),Image.LANCZOS)
base.alpha_composite(wm,((W-420)//2,52))
ct(d,128,"What's your",ImageFont.truetype(CAP,100),NAVY)
fT=ImageFont.truetype(CAP,100); t1="Christmas"; t2=" style?"; w1=d.textlength(t1,font=fT); w2=d.textlength(t2,font=fT); x=W/2-(w1+w2)/2
d.text((x,236),t1,font=fT,fill=RED); d.text((x+w1,236),t2,font=fT,fill=NAVY)
picks=[STY['plaid'][0],STY['pink'][0],STY['green'][0],STY['blue'][0]]
S_=314; gap=60; x0=(W-2*S_-gap)//2; y0=380
for i,(brand,gname,_) in enumerate(picks):
    x=x0+(i%2)*(S_+gap); y=y0+(i//2)*(S_+72)
    place(base,mat(S(brand,gname),S_),x,y,r=26)
    ct(d,y+S_+16,['PLAID','PINK','GREEN','BLUE'][i],ImageFont.truetype(BIT,34),RED,x+S_/2)
ct(d,1182,f"{len(rows)} holiday mats from our partner brands",ImageFont.truetype(BIT,36),NAVY)
ct(d,1240,"Swipe to find yours",ImageFont.truetype(PF,50),RED)
base.convert('RGB').save(OUT+'slide01-cover.jpg',quality=92)
# closing: the real app on a phone
base=getbg(99); d=ImageDraw.Draw(base)
lk=Image.open(LOCK); lw=760; lh=round(lk.height*lw/lk.width); base.alpha_composite(lk.resize((lw,lh),Image.LANCZOS),((W-lw)//2,64))
fH=ImageFont.truetype(BIT,38); ct(d,64+lh+30,"Your tiles, matched to every holiday mat",fH,NAVY)
# phone: screenshot of the live app (scrollbar column cropped off)
shot=Image.open(R+'assets/social/christmas-style-nov17/fym-amara-clara-phone.png').convert('RGB').crop((0,0,492,992))
SW=420; SH=round(992*SW/492); scr=shot.resize((SW,SH),Image.LANCZOS)
bz=16; PW,PH=SW+2*bz,SH+2*bz; px,py=86,248
sh=Image.new('RGBA',base.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((px,py+18,px+PW,py+PH+18),62,fill=(20,50,90,110)); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
ph=Image.new('RGBA',(PW,PH),(0,0,0,0)); ImageDraw.Draw(ph).rounded_rectangle((0,0,PW-1,PH-1),62,fill=(22,24,30,255))
ph.paste(scr,(bz,bz),rmask(scr.size,48)); base.alpha_composite(ph,(px,py))
assert py+PH<=1150, py+PH
# three steps beside the phone
sx=px+PW+52; maxw=W-60-sx; fS=ImageFont.truetype(CAP,44); fs=ImageFont.truetype(BIT6,30)
steps=[("Pick your tiles","Amara by Oh My Mahjong"),("Swipe holiday mats","Heart the ones you love, skip the rest"),("Add racks","Save your match card and shop it")]
y=py+120
for i,(t,sub) in enumerate(steps):
    d.ellipse((sx,y,sx+60,y+60),fill=RED); n=str(i+1); f=ImageFont.truetype(BIT,34); bb=f.getbbox(n); d.text((sx+30-(bb[2]-bb[0])/2-bb[0],y+30-(bb[3]-bb[1])/2-bb[1]),n,font=f,fill=(255,255,255))
    tx=sx; ty=y+78
    ft=fit(d,t,CAP,44,maxw); d.text((tx,ty),t,font=ft,fill=NAVY); assert d.textlength(t,font=ft)<=maxw
    # wrap sub
    words=sub.split(); lines=['']
    for w_ in words:
        cand=(lines[-1]+' '+w_).strip()
        if d.textlength(cand,font=fs)<=maxw: lines[-1]=cand
        else: lines.append(w_)
    for j,l in enumerate(lines): d.text((tx,ty+62+j*38),l,font=fs,fill=MUTED)
    y=ty+62+len(lines)*38+56
assert y<=1150, y
pill(base,1176,"Comment MATCH and we'll send you the link",ImageFont.truetype(BIT,36),h=72,padx=40)
ct(d,1272,"Code MAHJMATCH at every brand here \u00b7 prices from each brand's site Nov 17",ImageFont.truetype(BIT6,24),MUTED)
base.convert('RGB').save(OUT+'slide10-find-your-match.jpg',quality=92)
json.dump(rows,open(OUT+'mats.json','w'),indent=1)
print(len(rows), sorted({r['brand'] for r in rows}))
