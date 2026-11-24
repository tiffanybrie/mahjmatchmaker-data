# Renders FYM Table-view phone raws for social. RULE (Tiffany Nov 23-24): ONE rack style x4 per table, never mixed.
# Fails if any table renders with a second rack.
import asyncio
from playwright.async_api import async_playwright
O='www.ohmymahjong.com/'
PQ,WH,CL,HP,AG,BLA,CA=O+'pink-quartz-rack-and-pusher-set',O+'white-rack-pusher',O+'clear-acrylic-rack-and-pusher-set',O+'hot-pink-rack-pusher',O+'agate-rack-and-pusher-set',O+'blue-lace-agate-rack-and-pusher-set',O+'carrara-rack-pusher-set'
MATS=[('serendipity',O+'serendipity-mat-in-tube',[PQ]),('heron',O+'heron-mat-in-tube',[BLA]),('vivara',O+'vivara-mat-w-tube',[HP]),('jade',O+'jade-mat-in-tube',[WH]),('chantilly',O+'chantilly-mat',[PQ]),('anastasia',O+'anastasia-mat-in-tube',[CL]),('peri-twinkle','alb:coquette:Peri-twinkle',[BLA]),('lotus-cove',O+'lotus-cove-mat-in-tube',[WH]),('year-of-the-horse',O+'year-of-the-horse-mat',[HP])]
OUT='/home/claude/mahjmatchmaker-data/assets/social/sadie-jane-launch/fym-phones/raw/'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    pg=await ctx.new_page()
    await pg.goto('file:///home/claude/fymws/r2f/index.html');await pg.wait_for_timeout(6000)
    await pg.add_style_tag(content='.swh,.r2swh,#coach,#tourq,.tourq{display:none!important}.r2dot{animation:none!important}')
    await pg.evaluate("()=>{sessionStorage.setItem('r2swh','1')}")
    for slug,k,rp in MATS:
      await pg.evaluate("""([k,rp])=>{try{TOUR.on=false}catch(e){};S.set=D.sets.findIndex(x=>x.slug==='sadie-jane');S.tilesOpen=false;S.mode='table';S.fav=k;S.rstage=true;S.rpick=rp;S.mfront=k;S.mfset=S.set;S.peek=null;delete S.seen[k];renderAll();}""",[k,rp])
      await pg.wait_for_timeout(5000)
      await pg.evaluate("()=>{const c=document.querySelector('#s-mats .scard[id^=top-]');window.scrollTo(0,c.getBoundingClientRect().top+scrollY-78)}")
      await pg.wait_for_timeout(4000)
      await pg.screenshot(path=OUT+f'table-{slug}.png')
      r2=await pg.evaluate("()=>{const c=document.querySelector('#s-mats .scard[id^=top-]');return window.R2CTX(c).rack2}")
      assert len(rp)==1 and not r2, f'MIXED RACKS on {slug}: {rp} rack2={r2}'
      print(slug,'single rack ok')
    await b.close()
asyncio.run(main())
