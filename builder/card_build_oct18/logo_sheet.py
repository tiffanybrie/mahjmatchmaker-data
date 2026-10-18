import asyncio,os,json,glob,io,base64,re
from PIL import Image,ImageDraw
from playwright.async_api import async_playwright
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad';F=SP+'/hd_logos/fetched'
async def svg2png():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(device_scale_factor=1)
        for f in glob.glob(F+'/*.svg'):
            svg=open(f).read();await pg.set_content(f'<html><body style="margin:0;background:transparent"><img id=i src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}" style="width:1200px;height:auto"></body></html>')
            await pg.wait_for_timeout(300);el=await pg.query_selector('#i');await el.screenshot(path=f[:-4]+'.png',omit_background=True)
        await b.close()
asyncio.run(svg2png())
import sys;sys.argv=[sys.argv[0],'__none__']
import hd_tiles as H
D=H.D;rows=[]
fet=json.load(open(F+'/report.json'));hd=json.load(open(SP+'/hd_logos/report.json'))
names=sorted(set(list(fet.keys())+[k for k,v in hd.items() if v]))
W=1500;rh=150;sheet=Image.new('RGB',(W,rh*len(names)),'white');d=ImageDraw.Draw(sheet)
def paste(im,x,y,w,h):
    im=im.convert('RGBA');im.thumbnail((w,h));bg=Image.new('RGBA',im.size,(235,235,235,255));bg.alpha_composite(im);sheet.paste(bg.convert('RGB'),(x,y))
for i,b in enumerate(names):
    y=i*rh;d.text((5,y+5),b,fill='black')
    if b in D['logos'] and D['logos'][b] in H.IMG:
        im=H.dec(H.IMG[D['logos'][b]]) if False else Image.open(io.BytesIO(base64.b64decode(H.IMG[D['logos'][b]].split(',',1)[1])));paste(im,200,y+10,380,rh-20);d.text((200,y+rh-14),'bundled %s'%(im.size,),fill='red')
    if hd.get(b):im=Image.open(SP+'/hd_logos/'+hd[b]['file']);paste(im,620,y+10,380,rh-20);d.text((620,y+rh-14),'repo %s'%(im.size,),fill='red')
    fn=re.sub(r'\W','',b)
    for ext in ('.png',):
        p=F+'/'+fn+ext
        if os.path.exists(p):im=Image.open(p);paste(im,1060,y+10,420,rh-20);d.text((1060,y+rh-14),'site %s'%(im.size,),fill='red')
sheet.save(SP+'/hd_logos/sheet.jpg',quality=80);print(len(names))
