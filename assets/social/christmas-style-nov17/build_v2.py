# Christmas style carousel v2 (Nov 17 pm): light snowy Find Your Mat-ch holiday look, 72 partner mats.
import json, re, random, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
R='/home/claude/tiffanybrie/mahjmatchmaker-data/'
OUT=R+'assets/social/christmas-style-nov17/v2/'
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
        tw=d.textlength(title,font=fT); sub=f'{part+1} of 2'; sw=d.textlength(sub,font=fP)
        x0=W/2-(tw+22+sw)/2; d.text((x0,92),title,font=fT,fill=NAVY); d.text((x0+tw+22,140),sub,font=fP,fill=RED)
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
picks=[STY['plaid'][0],STY['pink'][3],STY['green'][0],STY['blue'][0]]
S_=314; gap=60; x0=(W-2*S_-gap)//2; y0=380
for i,(brand,gname,_) in enumerate(picks):
    x=x0+(i%2)*(S_+gap); y=y0+(i//2)*(S_+72)
    place(base,mat(S(brand,gname),S_),x,y,r=26)
    ct(d,y+S_+16,['PLAID','PINK','GREEN','BLUE'][i],ImageFont.truetype(BIT,34),RED,x+S_/2)
ct(d,1182,f"{len(rows)} holiday mats from our partner brands",ImageFont.truetype(BIT,36),NAVY)
ct(d,1240,"Swipe to find yours",ImageFont.truetype(PF,50),RED)
base.convert('RGB').save(OUT+'slide01-cover.jpg',quality=92)
# closing
base=getbg(99); d=ImageDraw.Draw(base)
ct(d,64,"Picked your style?",ImageFont.truetype(CAP,88),NAVY)
ct(d,172,"Now see it with your tiles.",ImageFont.truetype(PF,56),RED)
fan=[STY['pink'][3],STY['plaid'][0],STY['blue'][0]]
for i,(brand,gname,_) in enumerate(fan):
    m=mat(S(brand,gname),380).convert('RGBA'); m.putalpha(rmask(m.size,28)); ang=[9,0,-9][i]
    sh=Image.new('RGBA',(m.size[0]+80,m.size[1]+80),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((40,52,40+m.size[0],52+m.size[1]),28,fill=(30,70,120,110)); sh=sh.filter(ImageFilter.GaussianBlur(16))
    rs=sh.rotate(ang,expand=True,resample=Image.BICUBIC); rm=m.rotate(ang,expand=True,resample=Image.BICUBIC)
    x=[150,350,550][i]; y=[300,268,300][i]
    base.alpha_composite(rs,(x-40-(rs.size[0]-sh.size[0])//2,y-40-(rs.size[1]-sh.size[1])//2)); base.alpha_composite(rm,(x-(rm.size[0]-m.size[0])//2,y-(rm.size[1]-m.size[1])//2))
fl=Image.open(R+'assets/brand/flame-heart-holiday.png').convert('RGBA'); fl=fl.resize((111,120),Image.LANCZOS); base.alpha_composite(fl,((W-111)//2,750))
fT=ImageFont.truetype(CAP,92); fY=ImageFont.truetype(PF,96); a="Find "; b="Your"; c=" Mat-ch"
wa,wb,wc=[d.textlength(t,font=f) for t,f in ((a,fT),(b,fY),(c,fT))]; x=W/2-(wa+wb+wc+30)/2; y=880
d.text((x,y),a,font=fT,fill=NAVY); d.text((x+wa,y-4),b,font=fY,fill=RED); d.text((x+wa+wb,y),c,font=fT,fill=NAVY); d.text((x+wa+wb+wc+2,y+8),"™",font=ImageFont.truetype(BIT,30),fill=NAVY)
fD=ImageFont.truetype(BIT6,36)
ct(d,1010,"Pick your tile set, then swipe the mats",fD,NAVY); ct(d,1056,"that bring out its best colors.",fD,NAVY)
pill(base,1140,"Link in bio  ·  Code MAHJMATCH",ImageFont.truetype(BIT,38),h=74,padx=44)
ct(d,1252,"Prices from each brand's site on Nov 17",ImageFont.truetype(BIT6,26),MUTED)
base.convert('RGB').save(OUT+'slide10-find-your-match.jpg',quality=92)
json.dump(rows,open(OUT+'mats.json','w'),indent=1)
print(len(rows), sorted({r['brand'] for r in rows}))
