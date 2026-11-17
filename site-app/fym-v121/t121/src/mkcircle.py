import sys
from PIL import Image, ImageDraw, ImageFilter
SRC='/home/claude/tiffanybrie/mahjmatchmaker-data/assets/tiles/v95/bambird-scatter/samples/src/'
TW,TH,G=150,210,8
def rmask(w,h,r=16):
    m=Image.new('L',(w,h),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),r,fill=255);return m
def face(n):
    im=Image.open(SRC+f'u_bootsb_f{n:02d}.png').convert('RGBA').resize((TW,TH),Image.LANCZOS)
    a=im.split()[3];m=rmask(TW,TH)
    from PIL import ImageChops
    im.putalpha(ImageChops.multiply(a,m));return im
def backs(color):
    if color=='blue':
        return [Image.open(SRC+f'u_bootsb_b{n:02d}.png').convert('RGBA').resize((TW,TH),Image.LANCZOS) for n in (1,4,6,8,9,11)]
    sp=Image.open('bam-bird-boots-pink-split.jpg').convert('RGB')
    xs=[883,1014,1146,1277,1410,1541];ys=[186,369,552];out=[]
    for (r,c) in [(0,1),(0,3),(1,0),(1,2),(1,4),(0,4)]:
        box=(xs[c]+3,ys[r]+3,xs[c+1]-2,ys[r+1]-2)
        im=sp.crop(box).resize((TW,TH),Image.LANCZOS).convert('RGBA');im.putalpha(rmask(TW,TH));out.append(im)
    return out
def build(color,out):
    S=700;bg=Image.new('RGBA',(S,S),(236,233,238,255))
    faces=[face(6),face(9),face(16),face(17),face(12),face(13)]
    bk=backs(color)
    x0=(S-(4*TW+3*G))//2;y0=(S-(3*TH+2*G))//2
    sh=Image.new('RGBA',(S,S),(0,0,0,0));lay=Image.new('RGBA',(S,S),(0,0,0,0))
    for r in range(3):
        for c in range(4):
            t=faces[r*2+c] if c<2 else bk[r*2+(c-2)]
            x=x0+c*(TW+G);y=y0+r*(TH+G)
            s=Image.new('RGBA',(TW,TH),(60,40,60,90));s.putalpha(Image.eval(t.split()[3],lambda v:v*90//255))
            sh.alpha_composite(s,(x+2,y+5));lay.alpha_composite(t,(x,y))
    sh=sh.filter(ImageFilter.GaussianBlur(5))
    bg.alpha_composite(sh);bg.alpha_composite(lay)
    bg.convert('RGB').save(out,quality=90)
build('blue','bam-bird-boots-blue-circle.jpg');build('pink','bam-bird-boots-pink-circle.jpg')
# preview: as the card circle (zoom 1.08)
for c in ['blue','pink']:
    im=Image.open(f'bam-bird-boots-{c}-circle.jpg');S=im.size[0];k=1.08;cw=int(S/k);o=(S-cw)//2
    cr=im.crop((o,o,o+cw,o+cw)).resize((500,500),Image.LANCZOS)
    m=Image.new('L',(500,500),0);ImageDraw.Draw(m).ellipse((0,0,499,499),fill=255)
    p=Image.new('RGB',(520,520),(247,236,227));p.paste(cr,(10,10),m);p.save(f'prev-{c}.jpg')
