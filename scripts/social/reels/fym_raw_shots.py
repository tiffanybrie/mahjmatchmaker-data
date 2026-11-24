# FYM phone raws for reels: (name, mat key, [ONE rack], mode table|close|aerial). Asserts a single rack style.
# Also: --card name matkey rack  -> saves the story match card PNG.
import asyncio,sys,base64,json
from playwright.async_api import async_playwright
O='www.ohmymahjong.com/'
PQ,WH,CL,HP,BLA=O+'pink-quartz-rack-and-pusher-set',O+'white-rack-pusher',O+'clear-acrylic-rack-and-pusher-set',O+'hot-pink-rack-pusher',O+'blue-lace-agate-rack-and-pusher-set'
OUT='/home/claude/mahjmatchmaker-data/assets/social/sadie-jane-launch/fym-phones/raw/'
SHOTS=[('heron',O+'heron-mat-in-tube',WH,'table'),('peri-twinkle','alb:coquette:Peri-twinkle',CL,'table'),('anastasia',O+'anastasia-mat-in-tube',BLA,'table'),
('vivara-close',O+'vivara-mat-w-tube',HP,'close'),('vivara-aerial',O+'vivara-mat-w-tube',HP,'aerial'),
('jade-pq',O+'jade-mat-in-tube',PQ,'table'),('jade-hp',O+'jade-mat-in-tube',HP,'table'),('jade-cl',O+'jade-mat-in-tube',CL,'table'),('anastasia-clear',O+'anastasia-mat-in-tube',CL,'table')]
CARDS2=[('sticker-serendipity',O+'serendipity-mat-in-tube',[PQ],'phone|sticker'),('card-serendipity-2r',O+'serendipity-mat-in-tube',[PQ,WH],'tri'),('card-serendipity-v-stack-2r',O+'serendipity-mat-in-tube',[PQ,WH],'stack')]
CARDS=[('card-serendipity',O+'serendipity-mat-in-tube',PQ,'tri'),('card-lotus-cove',O+'lotus-cove-mat-in-tube',WH,'tri'),('card-serendipity-v-table',O+'serendipity-mat-in-tube',PQ,'table'),('card-serendipity-v-phone',O+'serendipity-mat-in-tube',PQ,'phone'),('card-serendipity-v-stack',O+'serendipity-mat-in-tube',PQ,'stack')]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    pg=await ctx.new_page()
    await pg.goto('file:///home/claude/fymws/r2f/index.html');await pg.wait_for_timeout(6000)
    await pg.add_style_tag(content='.swh,.r2swh,#coach,#tourq,.tourq{display:none!important}.r2dot{animation:none!important}')
    for n,k,r,mode in SHOTS:
      await pg.evaluate("""([k,r,m])=>{try{TOUR.on=false}catch(e){};S.set=D.sets.findIndex(x=>x.slug==='sadie-jane');S.tilesOpen=false;S.mode=m;S.fav=k;S.rstage=true;S.rpick=[r];S.mfront=k;S.mfset=S.set;S.peek=null;delete S.seen[k];renderAll();}""",[k,r,mode])
      await pg.wait_for_timeout(5000)
      # Up close = tiles photo + mat TOGETHER in frame (Tiffany Nov 24): scroll so the tile band sits right under the nav
      await pg.evaluate("(m)=>{const c=document.querySelector('#s-mats .scard[id^=top-]');let y=c.getBoundingClientRect().top+scrollY-78;if(m==='close'){const t=[...document.querySelectorAll('#s-mats *')].filter(e=>/Sadie Jane tiles/.test(e.textContent)&&e.children.length<4&&e.getBoundingClientRect().height>0).pop();let el=t;while(el&&el.getBoundingClientRect().height<120)el=el.parentElement;y=el.getBoundingClientRect().top+scrollY-92;}window.scrollTo(0,y)}",mode)
      await pg.wait_for_timeout(4000)
      x=await pg.evaluate("()=>{const c=document.querySelector('#s-mats .scard[id^=top-]');const x=window.R2CTX(c);return [c.dataset.id,x.rack,x.rack2,S.mode]}")
      assert not x[2], f'MIXED RACKS {n} {x}'
      if mode=='close':
        tb=await pg.evaluate("()=>{const t=[...document.querySelectorAll('#s-mats *')].filter(e=>/Sadie Jane tiles/.test(e.textContent)&&e.children.length<4&&e.getBoundingClientRect().height>0).pop();let el=t;while(el&&el.getBoundingClientRect().height<120)el=el.parentElement;const r=el.getBoundingClientRect();return [r.top,r.height]}")
        print('  tiles band',tb); assert tb[0]>=86, f'UP CLOSE without the tiles in frame: {n} {tb}'
      await pg.screenshot(path=OUT+f'table-{n}.png'); print(n,x)
    for n,k,r,md in CARDS:
      await pg.evaluate("""([k,r,md])=>{S.set=D.sets.findIndex(x=>x.slug==='sadie-jane');S.fav=k;S.rpick=Array.isArray(r)?r:[r];S.fmt=md.includes('|')?md.split('|')[1]:'story';S.mode='table';S.view=md.split('|')[0];S.made=true;renderCard();}""",[k,r,md])
      await pg.wait_for_timeout(9000)
      u=await pg.evaluate("()=>cardURL")
      open(OUT+f'{n}.'+('png' if u.startswith('data:image/png') else 'jpg'),'wb').write(base64.b64decode(u.split(',',1)[1])); print(n,len(u))
    await b.close()
if len(sys.argv)>1 and sys.argv[1]=='--only':
  keep=sys.argv[2:]; SHOTS=[x for x in SHOTS if x[0] in keep]; CARDS=[x for x in CARDS+CARDS2 if x[0] in keep]
asyncio.run(main())
