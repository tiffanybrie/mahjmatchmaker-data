# ShopMy product pin test (Oct 21): 1000x1500 single-product pins. Usage: python3 scripts/pinterest/shopmy_product_pins.py
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='/home/claude/mahjmatchmaker-data/'
TMP='/tmp/claude-0/pp/'
OUT=R+'assets/social/pinterest/shopmy-test/'
CAP=R+'scripts/social/tileprofile/fonts/Caprasimo.ttf'
BIT=R+'scripts/social/tileprofile/fonts/bitter-latin-700-normal.woff2'
LOGO=R+'assets/brand/mahjmatchmaker-wordmark.png'
BG=(250,243,234); NAVY=(5,70,137); PINK=(214,51,108)
G=R+'assets/mats/gallery-new/'
PINS=[ # slug, source, headline lines, brand
 ('livy',G+'betty-june-jeannette--livy.jpg',['Lavender pink','floral mahjong mat'],'Betty June & Jeannette'),
 ('kerry',R+'assets/mats/etsy/bettyjunejeannette/kerry-2.jpg',['Pink watercolor','floral mahjong mat'],'Betty June & Jeannette'),
 ('allie',G+'betty-june-jeannette--allie-purple.jpg',['Orchid hummingbird','mahjong mat'],'Betty June & Jeannette'),
 ('brinkley',G+'betty-june-jeannette--brinkley.jpg',['Pink poolside','mahjong mat'],'Betty June & Jeannette'),
 ('nichole',G+'betty-june-jeannette--nichole.jpg',['Blue chinoiserie','mahjong mat'],'Betty June & Jeannette'),
 ('tala-midnight',TMP+'tala_midnight.jpg',['Midnight wildflower','mahjong mat'],'Tala Mahj'),
 ('tala-pink',G+'tala-mahj--cabana-pink-ivory-with-citrus-fringe.jpg',['Pink striped','mahjong mat'],'Tala Mahj'),
 ('tala-blue',G+'tala-mahj--cabana-seafoam-blue-ivory-with-citrus-fringe.jpg',['Blue striped','mahjong mat'],'Tala Mahj'),
 ('tala-carlyle',TMP+'tala_carlyle.jpg',['Holiday plaid','mahjong mat'],'Tala Mahj'),
 ('omm-heritage',TMP+'heritage.jpg',['Heritage','mahjong tile set'],'Oh My Mahjong'),
]
def f(p,s): return ImageFont.truetype(p,s)
def build(slug,src,lines,brand):
    im=Image.open(src).convert('RGB')
    W,H=1000,1500; S=940; X=(W-S)//2; Y=60
    pin=Image.new('RGB',(W,H),BG)
    if slug=='omm-heritage':
        w,h=im.size; im=im.crop((int(.04*w),int(.255*h),int(.96*w),int(.745*h)))
        card=Image.new('RGB',(S,S),(255,255,255))
        t=im.resize((S-40,int((S-40)*im.size[1]/im.size[0])),Image.LANCZOS)
        card.paste(t,(20,(S-t.size[1])//2))
    else:
        w,h=im.size
        if slug=='kerry':
            im=im.crop((int(.04*w),int(.14*h),int(.69*w),int(.86*h)))
            bgc=Image.open(src).convert('RGB').getpixel((20,20))
            w,h=im.size; m=max(w,h); sq=Image.new('RGB',(m,m),bgc); sq.paste(im,((m-w)//2,(m-h)//2)); im=sq
        else:
            if slug in('livy','nichole'):
                box={'livy':(.12,.03,.945,.955),'nichole':(0,0,.95,.95)}[slug]
                im=im.crop((int(box[0]*w),int(box[1]*h),int(box[2]*w),int(box[3]*h))); w,h=im.size
                m=max(w,h); sq=Image.new('RGB',(m,m),(255,255,255)); sq.paste(im,((m-w)//2,(m-h)//2)); im=sq
            else:
                m=min(w,h); im=im.crop(((w-m)//2,(h-m)//2,(w-m)//2+m,(h-m)//2+m))
        card=im.resize((S,S),Image.LANCZOS)
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle((X,Y+10,X+S,Y+S+10),fill=(5,70,137,50))
    sh=sh.filter(ImageFilter.GaussianBlur(16)); pin.paste(sh,(0,0),sh)
    pin.paste(card,(X,Y))
    d=ImageDraw.Draw(pin)
    d.rectangle((X,Y,X+S,Y+S),outline=(255,255,255),width=6)
    y=Y+S+50
    for ln in lines:
        d.text((W//2,y),ln,font=f(CAP,88 if max(len(x) for x in lines)<=16 else 78),fill=NAVY,anchor='mt'); y+=104
    y+=14
    d.text((W//2,y),brand.upper(),font=f(BIT,34),fill=PINK,anchor='mt')
    lg=Image.open(LOGO).convert('RGBA'); lg=lg.resize((300,int(300*lg.size[1]/lg.size[0])),Image.LANCZOS)
    pin.paste(lg,((W-300)//2,H-lg.size[1]-34),lg)
    pin.save(OUT+f'{slug}-1000x1500.jpg',quality=92)
for p in PINS: build(*p)
# contact sheet
sh=Image.new('RGB',(5*300,2*450),'white')
for i,p in enumerate(PINS):
    t=Image.open(OUT+f'{p[0]}-1000x1500.jpg').resize((300,450)); sh.paste(t,((i%5)*300,(i//5)*450))
sh.save('/tmp/claude-0/pp/pinsheet.jpg')
