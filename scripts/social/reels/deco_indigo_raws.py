# Deco Indigo reel raws (Sadie Jane v7 format, Nov 26). One rack style x4 per table (asserted).
import asyncio,base64
from playwright.async_api import async_playwright
SET='bam-bird-boutique-deco-indigo'; B='www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'
IND,MUL,WAL,TEAL,LAG=B+'?v=52307844137269',B+'?v=52307844202805',B,B+'?v=52307844235573',B+'?v=53275469938997'
OUT='/home/claude/mahjmatchmaker-data/assets/social/deco-indigo-launch/fym-phones/raw/'
DDM='www.bambirdboutique.com/deco-neoprene-mahjong-mat-copy-2?v=67663098347829'
SHOTS=[('deco-dragon-mulberry',DDM,IND,'table'),('trent-midnight','ozarkmahjong.com/trent-midnight-mahjong-mat',MUL,'table'),
('bamboo-dragon','alb2:isabel-harte-isabel-harte',IND,'table'),('caroline-peacock','mahjandvine.com/caroline-in-peacock',MUL,'table'),
('hawthorne','www.ohmymahjong.com/hawthorne-mat-in-tube',WAL,'table'),('emw-magenta','www.bambirdboutique.com/east-meets-west-neoprene-mat?v=49857170735413',IND,'table'),
('flourish','brittmillsdesign.com/flourish-neoprene-mahjong-mat',MUL,'table'),('gilded-peacock','bougiemahjong.com/gilded-peacock-mahjong-mat',WAL,'table'),
('deco-neoprene','www.bambirdboutique.com/deco-neoprene-mahjong-mat',MUL,'table'),
('view-close',DDM,IND,'close'),('view-aerial',DDM,IND,'aerial'),
('rack-ind',DDM,IND,'table'),('rack-mul',DDM,MUL,'table'),('rack-wal',DDM,WAL,'table'),('rack-teal',DDM,TEAL,'table')]
CARDS=[('card-0',DDM,[IND,MUL],'phone|sticker'),('card-1',DDM,[IND,MUL],'tri'),('card-2','mahjandvine.com/caroline-in-peacock',[MUL,IND],'tri'),('card-3',DDM,[IND],'table@aerial')]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    pg=await ctx.new_page(); ctx.on('page',lambda np: asyncio.ensure_future(np.close()) if np!=pg else None)
    await pg.goto('file:///home/claude/fymws/r2f/index.html');await pg.wait_for_timeout(6000)
    await pg.add_style_tag(content='.swh,.r2swh,#coach,#tourq,.tourq,.ver{display:none!important}.r2dot{animation:none!important}')
    await pg.evaluate("()=>{sessionStorage.setItem('r2swh','1')}")
    for n,k,r,mode in SHOTS:
      await pg.evaluate("""([k,r,m,s])=>{try{TOUR.on=false}catch(e){};S.set=D.sets.findIndex(x=>x.slug===s);S.tilesOpen=false;S.mode=m;S.fav=k;S.rstage=true;S.rpick=[r];S.mfront=k;S.mfset=S.set;S.peek=null;delete S.seen[k];renderAll();}""",[k,r,mode,SET])
      await pg.wait_for_timeout(4500)
      await pg.evaluate("(m)=>{const c=document.querySelector('#s-mats .scard[id^=top-]');let y=c.getBoundingClientRect().top+scrollY-78;if(m==='close'){const t=[...document.querySelectorAll('#s-mats *')].filter(e=>/Deco Indigo tiles|Indigo tiles/.test(e.textContent)&&e.children.length<4&&e.getBoundingClientRect().height>0).pop();if(t){let el=t;while(el&&el.getBoundingClientRect().height<120)el=el.parentElement;y=el.getBoundingClientRect().top+scrollY-92;}else{y=c.getBoundingClientRect().top+scrollY-78-150;}}window.scrollTo(0,y)}",mode)
      await pg.wait_for_timeout(3500)
      x=await pg.evaluate("()=>{const c=document.querySelector('#s-mats .scard[id^=top-]');const x=window.R2CTX(c);return [c.dataset.id,x.rack,x.rack2,S.mode]}")
      assert not x[2], f'MIXED RACKS {n} {x}'
      await pg.screenshot(path=OUT+f'{n}.png'); print(n,x[0][:40],x[1][-12:] if x[1] else x[1],x[3])
    for n,k,r,md in CARDS:
      await pg.evaluate("""([k,r,md,s])=>{S.set=D.sets.findIndex(x=>x.slug===s);S.fav=k;S.rpick=r;S.fmt=md.includes('|')?md.split('|')[1]:'story';S.mode=md.includes('@')?md.split('@')[1]:'table';S.view=md.split('|')[0].split('@')[0];S.made=true;renderCard();}""",[k,r,md,SET])
      await pg.wait_for_timeout(8000)
      u=await pg.evaluate("()=>cardURL")
      open(OUT+f'{n}.png','wb').write(base64.b64decode(u.split(',',1)[1])); print(n,len(u))
    # shop
    await pg.evaluate("""([k,r,s])=>{try{localStorage.clear()}catch(e){};S.set=D.sets.findIndex(x=>x.slug===s);S.fav=k;S.rpick=[r];S.fmt='story';S.mode='table';S.view='tri';S.made=true;renderAll();}""",[DDM,IND,SET])
    await pg.wait_for_timeout(7000)
    await pg.evaluate("()=>{document.querySelectorAll('.shop .si.done').forEach(e=>e.classList.remove('done'));const h=document.querySelector('.shop h3');window.scrollTo(0,h.getBoundingClientRect().top+scrollY-90)}")
    await pg.wait_for_timeout(1500); await pg.screenshot(path=OUT+'shop-0.png')
    nn=await pg.evaluate("()=>document.querySelectorAll('.shop .si a.go').length")
    for i in range(nn):
      await pg.evaluate("(i)=>document.querySelectorAll('.shop .si a.go')[i].click()",i); await pg.wait_for_timeout(1200)
      await pg.screenshot(path=OUT+f'shop-{i+1}.png')
    print('shop rows',nn)
    await b.close()
import sys
if len(sys.argv)>1: SHOTS=[x for x in SHOTS if x[0] in sys.argv[1:]]; CARDS=[]
asyncio.run(main())
