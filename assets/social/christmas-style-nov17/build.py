import json, re, sys
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
R='/home/claude/tiffanybrie/mahjmatchmaker-data/'
OUT=R+'assets/social/christmas-style-nov17/'
G=R+'assets/mats/gallery/'
F=R+'scripts/social/tileprofile/fonts/'
CAP=F+'Caprasimo.ttf'; CAV=F+'Caveat-Bold.ttf'; BIT=R+'scripts/albumcard/woodfix/Bitter-Bold.ttf'
NAVY=(6,42,85); PINK=(214,51,108); BLUSH=(247,182,200); CREAM=(250,243,234); WNAVY=(5,70,137)
snap=json.load(open(R+'config/partner-products-snapshot.json'))
gal={it[0]:it for it in json.load(open(R+'site/livepatch/matgallery/data/matgallery-v120.json'))}
import urllib.parse
def price(slug):
    link=gal[slug][3]; u=urllib.parse.urlparse(link); q=urllib.parse.parse_qs(u.query)
    path=urllib.parse.unquote(q.get('redirect',[u.path])[0]); h=re.search(r'/products/([^/?#]+)',path).group(1)
    for dom,v in snap.items():
        if dom.replace('www.','')==u.netloc.replace('www.','') and h in v:
            p=v[h]; assert p['avail'], slug; return p['min']
    raise Exception('noprice '+slug)
SL={
'plaid':[('anders-ruff--tartan-tidings-mahjong-mat','Tartan Tidings'),('oh-my-mahjong--yuletide','Yuletide'),("bam-let-s-mahjong--holly-jolly-christmas-mahjong-mat",'Holly Jolly Christmas'),('my-fair-mahjong--plaid-tidings','Plaid Tidings'),('bam-bird-boutique--plaid-neoprene-green-with-pink','Green Plaid Neoprene'),('anders-ruff--evergreen-tartan-mahjong-mat','Evergreen & Tartan')],
'pink':[('oh-my-mahjong--clara','Clara'),('anders-ruff--very-merry-mahj-mahjong-mat','Very Merry Mahj'),('bam-bird-boutique--plaid-neoprene-pink-on-pink','Pink on Pink Plaid'),('britt-mills--nutcracker-leatherette','Nutcracker'),('peace-love-mahjong--tied-with-a-bow','Tied With A Bow'),('my-fair-mahjong--peppermint-wishes','Peppermint Wishes')],
'green':[('bespoke-mahjong--double-sided-mat-double-the-fun-bespoke-x-corey-paige-holiday-love-mat-red-green','Holiday Love'),('anders-ruff--watercolor-christmas-tree-mahjong-mat','Watercolor Christmas Tree'),('britt-mills--winter-berry-leatherette','Winter Berry'),('peace-love-mahjong--perfectly-wrapped','Perfectly Wrapped'),('mahj-mood--holly-berry-mat','Holly Berry'),('virora-mahjong--hollivia-mahjong-mat','Hollivia')],
'blue':[('oh-my-mahjong--winterberry','Winterberry'),('bespoke-mahjong--double-sided-mat-double-the-fun-bespoke-x-corey-paige-holiday-love-mat-blue','Holiday Love Blue'),('anders-ruff--tartan-toile-no-l-mahjong-mat','Tartan Toile Noël'),('peace-love-mahjong--frosted-flowers','Frosted Flowers'),('virora-mahjong--hiverelle-mahjong-mat','Hiverelle'),('let-s-be-besties--alpine-snowflakes','Alpine Snowflakes')],
}
def trim(im):
    rgb=im.convert('RGB')
    bg=Image.new('RGB',rgb.size,(255,255,255))
    diff=ImageChops.difference(rgb,bg).convert('L').point(lambda v:255 if v>40 else 0)
    bb=diff.getbbox(); im=rgb.crop(bb) if bb else rgb
    # square crop center
    w,h=im.size; k=int(min(w,h)*0.02); im=im.crop((k,k,w-k,h-k)); w,h=im.size; s=min(w,h); return im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))
def rounded(im,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.size[0]-1,im.size[1]-1),r,fill=255); return m
def fit(d,text,font,size,maxw):
    while size>14:
        f=ImageFont.truetype(font,size)
        if d.textlength(text,font=f)<=maxw: return f
        size-=1
    return ImageFont.truetype(font,size)
def ctext(d,y,text,font,fill,cx=540):
    w=d.textlength(text,font=font); d.text((cx-w/2,y),text,font=font,fill=fill)
W,H=1080,1350
STY={'plaid':('Plaid',PINK),'pink':('Pink',PINK),'green':('Green',PINK),'blue':('Blue',PINK)}
order=['plaid','pink','green','blue']
rows=[]
def color_slide(key,n):
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    ctext(d,60,"WHAT'S YOUR CHRISTMAS STYLE?",ImageFont.truetype(BIT,34),BLUSH)
    ctext(d,104,STY[key][0],ImageFont.truetype(CAP,120),(255,255,255))
    # progress dots row: Plaid Pink Green Blue
    f=ImageFont.truetype(BIT,26); labels=[s.upper() for s in ['Plaid','Pink','Green','Blue']]
    tw=sum(d.textlength(l,font=f) for l in labels)+3*70; x=540-tw/2; y=262
    for i,l in enumerate(labels):
        c=PINK if order[i]==key else (120,150,190); d.text((x,y),l,font=f,fill=c); x+=d.textlength(l,font=f)
        if i<3:
            d.ellipse((x+31,y+12,x+39,y+20),fill=(120,150,190)); x+=70
    M=48; gap=36; S=(W-2*M-2*gap)//3; top=330; rowh=S+118
    for i,(slug,name) in enumerate(SL[key]):
        brand=gal[slug][2]; p=price(slug)
        rows.append((key,name,brand,p,slug))
        mat=trim(Image.open(G+slug+'.webp')).resize((S,S),Image.LANCZOS)
        cx=M+(i%3)*(S+gap); cy=top+(i//3)*rowh
        im.paste(mat,(cx,cy),rounded(mat,26))
        fn=fit(d,name,BIT,30,S); bl=f"{brand} · ${p:.0f}"
        fb=fit(d,bl,BIT,24,S)
        ctext(d,cy+S+16,name,fn,(255,255,255),cx+S/2)
        ctext(d,cy+S+56,bl,fb,BLUSH,cx+S/2)
    ctext(d,H-120,"Code MAHJMATCH works at every brand here",ImageFont.truetype(BIT,32),(255,255,255))
    ctext(d,H-74,"Prices on each brand's site Nov 17",ImageFont.truetype(BIT,22),(140,165,200))
    im.save(OUT+f'slide{n}-{key}.jpg',quality=90)
for n,k in enumerate(order,2): color_slide(k,n)
# cover
im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
ctext(d,92,"What's your",ImageFont.truetype(CAP,104),(255,255,255))
ctext(d,206,"Christmas style?",ImageFont.truetype(CAP,104),(255,255,255))
picks=[SL['plaid'][0],SL['pink'][0],SL['green'][0],SL['blue'][0]]
S=360; gap=48; x0=(W-2*S-gap)//2; y0=360
for i,(slug,name) in enumerate(picks):
    mat=trim(Image.open(G+slug+'.webp')).resize((S,S),Image.LANCZOS)
    x=x0+(i%2)*(S+gap); y=y0+(i//2)*(S+80)
    im.paste(mat,(x,y),rounded(mat,28))
    ctext(d,y+S+12,['PLAID','PINK','GREEN','BLUE'][i],ImageFont.truetype(BIT,34),BLUSH,x+S/2)
ctext(d,H-120,"24 holiday mats from our partner brands",ImageFont.truetype(BIT,34),(255,255,255))
ctext(d,H-72,"Swipe to find yours",ImageFont.truetype(CAV,46),BLUSH)
im.save(OUT+'slide1-cover.jpg',quality=90)
# closing
im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
ctext(d,130,"Picked your style?",ImageFont.truetype(CAP,92),(255,255,255))
ctext(d,250,"Now see it with your tiles.",ImageFont.truetype(CAV,78),BLUSH)
fan=[SL['pink'][1],SL['plaid'][0],SL['blue'][0]]
S=380
for i,(slug,_) in enumerate(fan):
    mat=trim(Image.open(G+slug+'.webp')).resize((S,S),Image.LANCZOS).convert('RGBA')
    mat.putalpha(rounded(mat,28)); ang=[10,0,-10][i]
    r=mat.rotate(ang,expand=True,resample=Image.BICUBIC)
    x=[140,350,560][i]; y=[440,400,440][i]
    im.paste(r,(x,y),r)
ctext(d,900,"Find Your Mat-ch™",ImageFont.truetype(CAP,84),(255,255,255))
ctext(d,1010,"Pick your tile set, then swipe the mats",ImageFont.truetype(BIT,34),(255,255,255))
ctext(d,1056,"that bring out its best colors.",ImageFont.truetype(BIT,34),(255,255,255))
ctext(d,1160,"Link in bio  ·  Code MAHJMATCH",ImageFont.truetype(BIT,38),PINK)
im.save(OUT+'slide6-find-your-match.jpg',quality=90)
json.dump(rows,open(OUT+'mats.json','w'),indent=1)
print(rows)
