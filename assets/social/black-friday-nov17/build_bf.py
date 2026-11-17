# Black Friday partner deals carousel (Nov 17 pm). Our snowy holiday style (not Mixit's look).
# Deals from Brand Watch's Black Friday section (updated Tue 11/17 3:50pm ET). Order per brand-tiers.md:
# code works on top first, then check-at-checkout, then sales that replace MAHJMATCH; tiers break ties.
import os
R='/home/claude/tiffanybrie/mahjmatchmaker-data/'
src=open(R+'assets/social/christmas-style-nov17/build_v3.py').read().split('\nrows=[]')[0]
exec(src)  # helpers only: bg, place, mat, fit, ct, pill, fonts, colors (no renders run)
OUT=R+'assets/social/black-friday-nov17/v1/'; os.makedirs(OUT,exist_ok=True)
AMBER=(176,106,18); GRAYB=(92,112,138); LINE=(170,196,222)
GROUPS=[
 ('Code MAHJMATCH works on top',GREEN,[
  ('Charleston Mahjong Club','Buy 2 save 10%, 3 save 15%, 4+ save 20%. Club bundles $425 (reg. $530).','Fri 11/27 to Mon 11/30','Charleston says MAHJMATCH takes 10% more on top'),
  ('Mahj & Vine','Every mat $65 (reg. $70), with free US shipping','On now','MAHJMATCH takes 10% more, so a mat is $58.50'),
  ('The Royal Mahjong Society','20% off sitewide, new Heirloom sets included','On now through Dec 1','Use MAHJMATCH for the full 20% off'),
 ]),
 ('Check at checkout',AMBER,[
  ('Bam Bird Boutique','15% off sitewide, Tortoise Travel tiles included (some exclusions)','Fri 11/20 to Sun 11/22','Not confirmed on top of the sale. MAHJMATCH is 10% otherwise.'),
  ('Mah Jongg Maven','5% off with code HOLIDAY5','On now','One code per order. MAHJMATCH saves the same 5%.'),
 ]),
 ('Their sale replaces our code',GRAYB,[
  ('Bespoke Mahjong','25% off sitewide and 15% off tables, taken off automatically','On now through Sun 11/22','No codes on top of the sale'),
  ('Peace Love Mahjong',"One Day, One Mat: a different mat 30% off each day, with that day's code",'On now, a new mat each day','Daily code replaces ours. MAHJMATCH is 10% on everything else.'),
  ('Mac + Miller Mahjong','Black Friday bundles $350 to $425, Dream Sling $99, Card Clutch $10','Mon 11/23 returning customers, Thu 11/26 everyone','Codes paused 11/23 to 12/1'),
  ('Mahjong Studios','30% off with their own Black Friday code, free US shipping over $49','On now','Their code replaces MAHJMATCH'),
 ],"Use their sale price here. MAHJMATCH won't add on top."),
]

_G=None
def grad():
    # the same light blue snowy gradient as bg(), without snow (snow goes on afterwards, kept off the text)
    global _G
    if _G is None:
        import math
        im=Image.new('RGB',(W,H)); px=im.load(); stops=[(0,(255,255,255)),(.38,(238,246,252)),(.75,(217,234,246)),(1,(198,221,239))]
        cx,cy=W/2,H*.42; rx,ry=W*.75,H*.75
        for y in range(H):
            for x in range(W):
                t=min(1,math.hypot((x-cx)/rx,(y-cy)/ry))
                for i in range(3):
                    a,ca=stops[i]; b,cb=stops[i+1]
                    if t<=b: f=(t-a)/(b-a); px[x,y]=tuple(int(ca[k]+(cb[k]-ca[k])*f) for k in range(3)); break
        _G=im.convert('RGBA')
    return _G.copy()
def snow(base,seed,avoid,n=90):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); ds=ImageDraw.Draw(sh); rnd=random.Random(seed); k=0; tries=0
    while k<n and tries<20000:
        tries+=1; r=rnd.uniform(3,9); x=rnd.uniform(0,W); y=rnd.uniform(0,H)
        if any(x+r+8>a and x-r-8<c and y+r+8>b and y-r-8<e for a,b,c,e in avoid): continue
        a_=int(255*rnd.uniform(.55,1)); k+=1
        ds.ellipse((x-r,y-r+3,x+r,y+r+3),fill=(60,110,160,int(a_*.35)))
        d.ellipse((x-r-2,y-r-2,x+r+2,y+r+2),fill=(120,165,205,int(a_*.55))); d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,a_))
    out=grad(); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3))); out.alpha_composite(lay); out.alpha_composite(base); return out
MX=72; TW=W-2*MX
fKick=ImageFont.truetype(BIT,26); fSec=ImageFont.truetype(CAP,50); fBrand=ImageFont.truetype(CAP,37)
fOff=ImageFont.truetype(BIT6,28); fWhen=ImageFont.truetype(BIT,26); fChip=ImageFont.truetype(BIT,23); fFoot=ImageFont.truetype(BIT6,24)
def wrap(d,t,f,w):
    lines=['']
    for x in t.split():
        c=(lines[-1]+' '+x).strip()
        if d.textlength(c,font=f)<=w: lines[-1]=c
        else: lines.append(x)
    return lines
def kicker(d):
    t='BLACK FRIDAY MAHJONG DEALS'; sp=4; w=sum(d.textlength(ch,font=fKick) for ch in t)+sp*(len(t)-1); x=W/2-w/2
    for ch in t: d.text((x,44),ch,font=fKick,fill=RED); x+=d.textlength(ch,font=fKick)+sp
def item_h(d,it):
    return 47+len(wrap(d,it[1],fOff,TW))*36+38+48
BOX=[]
def tx(d,xy,t,f,fill):
    d.text(xy,t,font=f,fill=fill); BOX.append(d.textbbox(xy,t,font=f))
def draw_item(base,d,y,it,col):
    brand,off,when,chip=it
    tx(d,(MX,y),brand,fBrand,NAVY); y+=47
    for l in wrap(d,off,fOff,TW): tx(d,(MX,y),l,fOff,NAVY); y+=36
    tx(d,(MX,y),when,fWhen,RED); assert d.textlength(when,font=fWhen)<=TW; y+=38
    cw=d.textlength(chip,font=fChip)+40; assert cw<=TW,(chip,cw); ch=42; BOX.append((MX,y+4,MX+cw,y+4+ch))
    d.rounded_rectangle((MX,y+4,MX+cw,y+4+ch),ch/2,fill=col); bb=fChip.getbbox(chip); d.text((MX+20,y+4+(ch-(bb[3]-bb[1]))/2-bb[1]),chip,font=fChip,fill=(255,255,255))
def deal_slide(n,groups):
    BOX.clear(); base=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(base); kicker(d); BOX.append((60,36,W-60,80))
    blocks=[]
    for gi,grp in enumerate(groups):
        title,col,items=grp[:3]; sub=grp[3] if len(grp)>3 else None
        blocks.append(('sec',title,col,66+(50 if sub else 0),sub))
        for j,it in enumerate(items): blocks.append(('item',it,col,item_h(d,it)))
    top,bot=94,1266; need=sum(b[3] for b in blocks); gaps=len(blocks)-1
    g=(bot-top-need)/gaps; assert g>=16,(n,g)
    g=min(g,72); y=top+(bot-top-need-g*gaps)/2
    prev=None
    for b in blocks:
        if b[0]=='sec':
            if prev=='item': y+=10
            ct(d,y,b[1],fSec,b[2] if b[2]!=GRAYB else NAVY); tw_=d.textlength(b[1],font=fSec); BOX.append(d.textbbox((W/2-tw_/2,y),b[1],font=fSec))
            if b[4]: fsb=ImageFont.truetype(PF,36); ct(d,y+70,b[4],fsb,RED); tw_=d.textlength(b[4],font=fsb); BOX.append(d.textbbox((W/2-tw_/2,y+70),b[4],font=fsb))
            y+=b[3]
        else:
            draw_item(base,d,y,b[1],b[2]); y+=b[3]
            if b is not blocks[-1] and blocks[blocks.index(b)+1][0]=='item': d.line((MX,y+g/2,W-MX,y+g/2),fill=LINE,width=2); BOX.append((MX,y+g/2-2,W-MX,y+g/2+2))
        y+=g; prev=b[0]
    t="Deals from each brand's own site, checked Tue 11/17"; ct(d,1290,t,fFoot,MUTED); tw_=d.textlength(t,font=fFoot); BOX.append(d.textbbox((W/2-tw_/2,1290),t,font=fFoot))
    base=snow(base,40+n,BOX)
    base.convert('RGB').save(OUT+f'slide{n:02d}-deals.jpg',quality=92)
def ctb(d,y,t,f,fill,cx=W/2):
    ct(d,y,t,f,fill,cx); w_=d.textlength(t,font=f); BOX.append(d.textbbox((cx-w_/2,y),t,font=f))
# cover: photos follow the text order (Royal and Maven have none in our gallery; Mahjong Studios is text only)
BOX.clear(); base=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(base)
wm=Image.open(R+'assets/brand/mahjmatchmaker-wordmark-holiday-notag.png').convert('RGBA'); wm=wm.resize((400,int(400*wm.size[1]/wm.size[0])),Image.LANCZOS)
base.alpha_composite(wm,((W-400)//2,48)); BOX.append(((W-400)//2,48,(W+400)//2,48+wm.size[1]))
ctb(d,112,'Black Friday',ImageFont.truetype(CAP,138),RED)
ctb(d,272,'mahjong deals',ImageFont.truetype(CAP,84),NAVY)
ctb(d,392,'9 partner sales, and which ones still take code MAHJMATCH',fit(d,'9 partner sales, and which ones still take code MAHJMATCH',BIT,34,W-180),NAVY)
picks=[('Charleston Mahjong Club','Ski Club Mat- Red Sweater Border','Charleston'),('Mahj & Vine','Chinoiserie Elephant','Mahj & Vine'),('Bam Bird Boutique','Bandana – Holiday Green/Pink accents','Bam Bird'),
       ('Bespoke Mahjong','Bespoke x Corey Paige - Holiday Love Mat - Red/Green','Bespoke'),('Peace Love Mahjong','Merry & Striped','Peace Love'),('Mac + Miller Mahjong','Heirloom Collection: Fire + Fortune Year of the Horse','Mac + Miller')]
S_=270; gx=48; x0=(W-3*S_-2*gx)//2; y0=468; rowh=S_+70
for i,(b,nm,lab) in enumerate(picks):
    x=x0+(i%3)*(S_+gx); y=y0+(i//3)*rowh
    place(base,mat(S(b,nm),S_),x,y,r=24)
    ctb(d,y+S_+14,lab,ImageFont.truetype(BIT,30),NAVY,x+S_/2)
assert y0+2*rowh<=1170
ctb(d,1176,'Swipe for the deals',ImageFont.truetype(PF,58),RED)
base=snow(base,31,BOX,110); base.convert('RGB').save(OUT+'slide01-cover.jpg',quality=92)
deal_slide(2,GROUPS[:2]); deal_slide(3,GROUPS[2:])
# closing: the real app on a phone (same as the approved Christmas style slide, BF wording)
BOX.clear(); base=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(base)
lk=Image.open(LOCK); lw=760; lh=round(lk.height*lw/lk.width); base.alpha_composite(lk.resize((lw,lh),Image.LANCZOS),((W-lw)//2,64)); BOX.append(((W-lw)//2,64,(W+lw)//2,64+lh))
fH=ImageFont.truetype(BIT,38); ctb(d,64+lh+30,"Match your tiles before you check out",fH,NAVY)
shot=Image.open(R+'assets/social/christmas-style-nov17/fym-amara-clara-phone.png').convert('RGB').crop((0,0,492,992))
SW=420; SH=round(992*SW/492); scr=shot.resize((SW,SH),Image.LANCZOS)
bz=16; PW,PH=SW+2*bz,SH+2*bz; px,py=86,248
sh=Image.new('RGBA',base.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((px,py+18,px+PW,py+PH+18),62,fill=(20,50,90,110)); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
ph=Image.new('RGBA',(PW,PH),(0,0,0,0)); ImageDraw.Draw(ph).rounded_rectangle((0,0,PW-1,PH-1),62,fill=(22,24,30,255))
ph.paste(scr,(bz,bz),rmask(scr.size,48)); base.alpha_composite(ph,(px,py))
sx=px+PW+52; maxw=W-60-sx; fs=ImageFont.truetype(BIT6,30)
steps=[("Pick your tiles","Amara by Oh My Mahjong"),("Swipe the mats","Heart the ones you love, skip the rest"),("Add racks","Save your match card and shop it")]
y=py+120
for i,(t,sub) in enumerate(steps):
    d.ellipse((sx,y,sx+60,y+60),fill=RED); BOX.append((sx,y,sx+60,y+60)); nn=str(i+1); f=ImageFont.truetype(BIT,34); bb=f.getbbox(nn); d.text((sx+30-(bb[2]-bb[0])/2-bb[0],y+30-(bb[3]-bb[1])/2-bb[1]),nn,font=f,fill=(255,255,255))
    ty=y+78; ft=fit(d,t,CAP,44,maxw); d.text((sx,ty),t,font=ft,fill=NAVY); BOX.append(d.textbbox((sx,ty),t,font=ft))
    lines=wrap(d,sub,fs,maxw)
    for j,l in enumerate(lines): d.text((sx,ty+62+j*38),l,font=fs,fill=MUTED); BOX.append(d.textbbox((sx,ty+62+j*38),l,font=fs))
    y=ty+62+len(lines)*38+56
assert y<=1150, y
BOX.append((100,1170,W-100,1260)); pill(base,1176,"Comment MATCH and we'll send you the link",ImageFont.truetype(BIT,36),h=72,padx=40)
ctb(d,1272,"Find Your Mat-ch™ is on mahjmatchmaker.com",ImageFont.truetype(BIT6,24),MUTED)
base=snow(base,99,BOX,110); base.convert('RGB').save(OUT+'slide04-find-your-match.jpg',quality=92)
print('ok',sorted(os.listdir(OUT)))
