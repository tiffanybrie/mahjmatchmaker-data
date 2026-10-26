import json,os,sys
sys.path.insert(0,'.')
from PIL import Image, ImageDraw, ImageFont
from seg2 import cutout
BB=json.load(open('backbox.json'))
SETS=[('the-country-club-edition','Country Club',13,3),('apres-ski-edition-tile-set','Après Ski',1,2),('the-hunt-club-edition','Hunt Club',1,2),('cocktail-club-2-0','Cocktail Club 2.0',12,13),('the-yacht-club-edition','Yacht Club',1,16)]
W,H=1600,700
def box(h,j):
    k=f'{h}_{j:02d}';hi=Image.open(f'hi/{k}.jpg');lo=Image.open(f'full/{k}.jpg');s=hi.width/lo.width
    return hi.convert('RGB'),[v*s for v in BB[k]]
def optA(h,j):
    """angled close-up, brand photo as shot; frame so the back tile sits in the circle (x 450-1150)"""
    im,b=box(h,j);bw=b[2]-b[0];bc=((b[0]+b[2])/2,(b[1]+b[3])/2)
    sc=190/bw   # back tile ~190px wide on the canvas
    cw,ch=W/sc,H/sc
    x0=bc[0]-1000/sc; y0=bc[1]-400/sc
    x0=max(0,min(x0,im.width-cw)); y0=max(0,min(y0,im.height-ch))
    if cw>im.width or ch>im.height:
        sc=max(W/im.width,H/im.height);cw,ch=W/sc,H/sc;x0=max(0,min(bc[0]-1010/sc,im.width-cw));y0=max(0,min(bc[1]-440/sc,im.height-ch))
    return im.crop((int(x0),int(y0),int(x0+cw),int(y0+ch))).resize((W,H),Image.LANCZOS)
def optB(h,j):
    """flat full set + its back tile, cut out onto white; back tile placed inside the circle"""
    im,b=box(h,j);o=cutout(f'hi/{h}_{j:02d}.jpg');bb=o.getbbox();o=o.crop(bb);b=[b[0]-bb[0],b[1]-bb[1],b[2]-bb[0],b[3]-bb[1]]
    sc=640/o.height;o=o.resize((int(o.width*sc),int(o.height*sc)),Image.LANCZOS);b=[v*sc for v in b]
    bx=(b[0]+b[2])/2; ox=int(1010-bx)
    c=Image.new('RGBA',(W,H),(255,255,255,255));c.alpha_composite(o,(ox,int((H-o.height)/2))) if ox>=0 else c.alpha_composite(o.crop((-ox,0,o.width,o.height)),(0,int((H-o.height)/2)));return c.convert('RGB')
def optC(h,j):
    """split: faces from the flat photo (left) | the back tile close-up (right), same photo"""
    im,b=box(h,j);o=cutout(f'hi/{h}_{j:02d}.jpg');
    c=Image.new('RGBA',(W,H),(255,255,255,255))
    # left: faces area = full set without the back tile, scaled to height 700, right-aligned (show the nearest-centre slice)
    bb=o.getbbox();fx1=min(bb[2],int(b[0])-4) ; faces=o.crop((bb[0],bb[1],fx1,bb[3]))
    s=700/faces.height;faces=faces.resize((int(faces.width*s),700),Image.LANCZOS)
    left=faces.crop((faces.width-800,0,faces.width,700)) if faces.width>=800 else faces
    c.alpha_composite(left,(800-left.width,0))
    bw=b[2]-b[0];bh=b[3]-b[1];pad=.12
    back=o.crop((int(b[0]-bw*pad),int(b[1]-bh*pad),int(b[2]+bw*pad),int(b[3]+bh*pad)))
    s=min(560/back.width,680/back.height);back=back.resize((int(back.width*s),int(back.height*s)),Image.LANCZOS)
    c.alpha_composite(back,(812,(700-back.height)//2))
    d=ImageDraw.Draw(c);d.rectangle((796,0,803,700),fill=(255,255,255,255));return c.convert('RGB')
def crops(c):
    circ=c.crop((450,0,1150,700)).resize((260,260));m=Image.new('L',(260,260),0);ImageDraw.Draw(m).ellipse((0,0,259,259),fill=255)
    cc=Image.new('RGB',(260,260),'white');cc.paste(circ,(0,0),m)
    bh=int(1600/3.87);by=int(700*.45-bh/2);band=c.crop((0,by,1600,by+bh)).resize((600,int(bh*600/1600)))
    return c.resize((600,262)),cc,band
try:F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except:F=None
os.makedirs('opt',exist_ok=True)
rows={}
for name,fn,idx in [('A','angled close-up (brand photo as shot)',2),('B','full set + back, cut out on white',3),('C','split: faces | back tile',3)]:
    f={'A':optA,'B':optB,'C':optC}[name];sheet=Image.new('RGB',(1520,len(SETS)*300+50),'white');d=ImageDraw.Draw(sheet)
    d.text((10,10),f'Option {name}: {fn}   |   swipe strip  ·  Mood board circle  ·  Close-up band',fill='black',font=F)
    for r,(h,lab,ja,jb) in enumerate(SETS):
        try:c=f(h,ja if name=='A' else jb)
        except Exception as e:print(name,h,e);continue
        c.save(f'opt/{name}_{h}.jpg',quality=90);rows.setdefault(h,{})[name]=c
        s,ci,ba=crops(c);y=50+r*300
        d.text((10,y),lab,fill='black',font=F);sheet.paste(s,(10,y+30));sheet.paste(ci,(630,y+30));sheet.paste(ba,(910,y+30+60))
    sheet.save(f'option_{name}.jpg',quality=85)
# summary: per set, A | B | C circles + strips
sm=Image.new('RGB',(3*620+20,len(SETS)*300+50),'white');d=ImageDraw.Draw(sm)
for k,n in enumerate('ABC'):d.text((10+k*620,10),f'Option {n}',fill='black',font=F)
for r,(h,lab,*_ ) in enumerate(SETS):
    for k,n in enumerate('ABC'):
        if n in rows.get(h,{}):
            s,ci,ba=crops(rows[h][n]);x=10+k*620;y=50+r*300
            sm.paste(s.resize((340,149)),(x,y+20));sm.paste(ci.resize((200,200)),(x+350,y));d.text((x,y+180),lab,fill='black',font=F)
sm.save('summary.jpg',quality=85)
