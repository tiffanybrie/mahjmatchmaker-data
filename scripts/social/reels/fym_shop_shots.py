# FYM "Shop your selections" raws: card screen shop list, one frame before and after each Shop tap (row ticks green).
import asyncio,sys
from playwright.async_api import async_playwright
O='www.ohmymahjong.com/'
OUT='/home/claude/mahjmatchmaker-data/assets/social/sadie-jane-launch/fym-phones/raw/'
MAT,RACK=O+'serendipity-mat-in-tube',O+'pink-quartz-rack-and-pusher-set'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    pg=await ctx.new_page()
    ctx.on('page',lambda np: asyncio.ensure_future(np.close()) if np!=pg else None)
    await pg.goto('file:///home/claude/fymws/r2f/index.html');await pg.wait_for_timeout(6000)
    await pg.add_style_tag(content='.swh,.r2swh,#coach,#tourq,.tourq,.ver{display:none!important}')
    await pg.evaluate("""([k,r])=>{try{TOUR.on=false}catch(e){};try{localStorage.clear()}catch(e){};S.set=D.sets.findIndex(x=>x.slug==='sadie-jane');S.fav=k;S.rpick=[r];S.fmt='story';S.mode='table';S.view='tri';S.made=true;renderAll();}""",[MAT,RACK])
    await pg.wait_for_timeout(8000)
    await pg.evaluate("()=>{document.querySelectorAll('.shop .si.done').forEach(e=>e.classList.remove('done'));const h=document.querySelector('.shop h3');window.scrollTo(0,h.getBoundingClientRect().top+scrollY-90)}")
    await pg.wait_for_timeout(1500)
    n=await pg.evaluate("()=>document.querySelectorAll('.shop .si a.go').length"); print('rows',n)
    await pg.screenshot(path=OUT+'shop-0.png')
    for i in range(n):
      await pg.evaluate("(i)=>document.querySelectorAll('.shop .si a.go')[i].click()",i)
      await pg.wait_for_timeout(1200)
      d=await pg.evaluate("()=>[document.querySelectorAll('.shop .si.done').length,document.getElementById('shc').textContent]"); print(i,d)
      await pg.screenshot(path=OUT+f'shop-{i+1}.png')
    print(await pg.evaluate("()=>[...document.querySelectorAll('.shop .si a.go')].map(a=>{const r=a.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})"))
    await b.close()
asyncio.run(main())
