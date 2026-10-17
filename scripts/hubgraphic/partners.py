"""Discount Codes page partner-logo graphic (1080x1350), rebuilt Oct 17 2026 from Tiffany's 'Partner Brands Oct 2026'
graphic: same pink header/footer + coral frame, current tagline (no 'Mahjong Social Club'), all 35 code partners."""
from PIL import Image, ImageDraw, ImageFont, ImageChops
import sys
R='/home/claude/mahjmatchmaker-data/'
SRC=sys.argv[1]; OUT=sys.argv[2]
base=Image.open(SRC).convert('RGB').resize((1080,1350))
PINK=base.getpixel((60,60)); CREAM=base.getpixel((540,190)); CORAL=(232,128,112)
c=base.copy(); d=ImageDraw.Draw(c)
# header tagline swap
d.rectangle((300,122,760,166),fill=PINK)
f=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',19)
txt='MATCHING MAHJONG TILES, MATS & RACKS'; sp=4
w=sum(d.textlength(ch,font=f)+sp for ch in txt)-sp; x=(1080-w)/2-40
for ch in txt: d.text((x,132),ch,font=f,fill=(255,255,255)); x+=d.textlength(ch,font=f)+sp
# body
d.rectangle((0,178,1080,1252),fill=CREAM)
for o in (28,40):
    d.rectangle((o,195+o-28,1080-o,1240-(o-28)),outline=CORAL,width=3)
for (x0,y0) in [(22,189),(1018,189),(22,1194),(1018,1194)]:
    d.rectangle((x0,y0,x0+40,y0+40),fill=CREAM); d.rectangle((x0+6,y0+6,x0+34,y0+34),outline=CORAL,width=3); d.rectangle((x0+14,y0+14,x0+26,y0+26),outline=CORAL,width=3)
def knock(im):
    import numpy as np
    a=np.array(im.convert('RGBA')).astype(int)
    if a[...,3].min()<250: return im.convert('RGBA')
    wht=(a[...,:3].min(-1)>238)
    a[...,3]=np.where(wht,0,255); return Image.fromarray(a.astype('uint8'),'RGBA')
def trim(im,bg):
    im=knock(im) if bg==(255,255,255) else im.convert('RGBA'); a=im.split()[3]
    if a.getextrema()[0]==255:
        diff=ImageChops.difference(im.convert('RGB'),Image.new('RGB',im.size,bg)).convert('L').point(lambda v:255 if v>28 else 0)
        bb=diff.getbbox()
    else: bb=a.getbbox()
    return im.crop(bb) if bb else im
def crop_src(box): return trim(base.crop(box),CREAM)
L=R+'builder/logos/'; P=R+'assets/brand/partner-logos/'; W2=R+'work/logos/'
logos=[('Oh My Mahjong',L+'n_ohmymahjong.png'),('Mahjong Row & Co.',L+'n_mahjongrowco.png'),('Miss Mahjong',(58,306,294,404)),('My Fair Mahjong',L+'n_myfairmahjong.png'),('Middle & Main',L+'n_middlemainmahjong.png'),
 ('Bird & Bamboo',L+'n_birdbamboo.png'),('Bam Bird Boutique',L+'n_bambirdboutique.png'),('Mahj Squad',L+'n_mahjsquad.png'),('Tigre de Tartan',(540,295,730,428)),('Britt Mills',(268,842,518,938)),
 ('Peace Love Mahjong',L+'n_peacelovemahjong.png'),('Charleston Mahjong Club',L+'n_charlestonmahjongclub.png'),('Bespoke Mahjong',L+'n_bespokemahjong.png'),('Virora',P+'virora.png'),('Anders Ruff',L+'n_andersruff.png'),
 ('Mahj Mood',(530,850,782,912)),('Mini Mahjer',L+'n_minimahjer.png'),('Mac + Miller',L+'n_macmillermahjong.png'),('Amanda Toppe',(15,462,238,632)),('Amahj',L+'n_amahj.png'),
 ("Let's Mahj On",L+'n_letsmahjon.png'),('Mahj & Vine',L+'n_mahjvine.png'),('Hip Hip Mahjong',L+'n_hiphipmahjong.png'),('Bam! Let\'s Mahjong',L+'n_bamletsmahjong.png'),('Yellow Mountain',L+'n_yellowmountainimports.png'),
 ('Mahjong Co.',L+'n_mahjongco.png'),('Mahjong Studios',L+'n_mahjongstudios.png'),('I Love Mahj',(358,208,722,268)),('Splash of Color',(292,462,462,612)),('Wren Mats',(315,658,470,812)),
 ('The Mahjong Press',W2+'the-mahjong-press-logo.png'),('Royal Mahjong Society',W2+'royal-mahjong-society-logo.png'),('Soiree All Day',W2+'soiree-all-day-logo.png'),('Mahjong Register',sys.argv[3]),("Let's Be Besties",P+'lets-be-besties.png')]
cols,rows=5,7; x0,y0,x1,y1=78,222,1002,1222; cw=(x1-x0)/cols; ch=(y1-y0)/rows
for i,(n,src) in enumerate(logos):
    im=crop_src(src) if isinstance(src,tuple) else trim(Image.open(src),(255,255,255))
    bw,bh=cw-26,ch-30
    s=min(bw/im.width,bh/im.height); im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)
    cx=x0+(i%cols)*cw+cw/2; cy=y0+(i//cols)*ch+ch/2
    c.paste(im,(int(cx-im.width/2),int(cy-im.height/2)),im)
c.save(OUT,quality=92)
print('ok',len(logos))
