"""Oct 17: wide share image (1200x630) with the brand tagline from the wordmark,
replacing the unconfirmed 'Hooking up' line. Usage: python3 share_tagline.py"""
from PIL import Image, ImageDraw, ImageFont
src='assets/brand/share-wide-1200x630.png'; out='assets/brand/share-wide-1200x630-v2.png'
im=Image.open(src).convert('RGB'); W,H=im.size
bg=im.getpixel((600,600-110)) if False else im.getpixel((200,520))
bar=im.getpixel((390,527))
d=ImageDraw.Draw(im)
d.rectangle([360,498,840,560],fill=bg)  # clear old bar
f=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',22)
txt='MATCHING MAHJONG TILES, MATS & RACKS'; tr=3
widths=[d.textlength(c,font=f) for c in txt]; tw=sum(widths)+tr*(len(txt)-1)
pad=22; x0=int(600-tw/2-pad); x1=int(600+tw/2+pad); y0,y1=506,550
d.rounded_rectangle([x0,y0,x1,y1],radius=4,fill=bar)
x=600-tw/2; cy=(y0+y1)/2
for c,w in zip(txt,widths):
    d.text((x,cy),c,font=f,fill='white',anchor='lm'); x+=w+tr
im.save(out); print(out,bar,bg,x0,x1)
