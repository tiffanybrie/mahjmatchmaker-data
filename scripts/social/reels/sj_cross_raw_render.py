# Cross-brand Sadie Jane FYM Table raws. RULE: ONE rack style x4 per table (asserts).
import asyncio
from playwright.async_api import async_playwright
OUT='/home/claude/mahjmatchmaker-data/assets/social/sadie-jane-launch/cross/raw/'
MATS=[('serendipity','www.ohmymahjong.com/serendipity-mat-in-tube','www.ohmymahjong.com/pink-quartz-rack-and-pusher-set'),
('petalwing','www.viroramahjong.com/petalwing','ballet pink'),
('lattice','missmahjong.com/lattice-mahjong-playing-mat-pre-order','cornflower blue scalloped'),
('hamptons-hydrangea','shop.andersruff.com/hamptons-hydrangea-mahjong-mat','french blue|bird'),
('color-wave','myfairmahjong.com/standard-mahjong-mats?v=49809801937207','iridescent opal'),
('blue-blooms','peacelovemahjong.com/mahjong-mats-hanukkah?v=67570489557284','wavy.*french blue'),
('pink-lemonade','mahjmood.com/pink-lemonade-mat','www.ohmymahjong.com/pink-quartz-rack-and-pusher-set'),
('paradise','birdandbamboo.com/the-paradise-mahjong-mat-tropical-teal','ballet pink'),
('cmc-reversible','www.charlestonmahjongclub.com/vegan-leather-reversible-game-mat?v=50377156264241','french blue|bird'),
('royal-hydrangea','theroyalmahjongsociety.com/hydrangea-mahjong-mat','iridescent opal')]
async def main():
  import os,sys; os.makedirs(OUT,exist_ok=True); only=sys.argv[1:]
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    pg=await ctx.new_page()
    await pg.goto('file:///home/claude/fymws/r2f/index.html');await pg.wait_for_timeout(6000)
    await pg.add_style_tag(content='.swh,.r2swh,#coach,#tourq,.tourq{display:none!important}.r2dot{animation:none!important}')
    for slug,k,rq in MATS:
      if only and slug not in only: continue
      rk=rq if rq in ('www.ohmymahjong.com/pink-quartz-rack-and-pusher-set',) else await pg.evaluate("""([k,q])=>{if(!M[k])return 'NOMAT';const re=new RegExp(q.split('|')[0],'i');const re2=q.includes('|')?new RegExp(q.split('|')[1],'i'):null;const c=Object.keys(R).filter(r=>!R[r].hid&&re.test((R[r].n||'')+' '+r)&&(!re2||re2.test(r+' '+(R[r].b||''))));return c[0]||'NORACK'}""",[k,rq])
      print(slug,rk)
      if rk.startswith('NO'): continue
      await pg.evaluate("""([k,rp])=>{try{TOUR.on=false}catch(e){};S.set=D.sets.findIndex(x=>x.slug==='sadie-jane');S.tilesOpen=false;S.mode='table';S.fav=k;S.rstage=true;S.rpick=rp;S.mfront=k;S.mfset=S.set;S.peek=null;delete S.seen[k];renderAll();}""",[k,[rk]])
      await pg.wait_for_timeout(5000)
      await pg.evaluate("()=>{const c=document.querySelector('#s-mats .scard[id^=top-]');window.scrollTo(0,c.getBoundingClientRect().top+scrollY-78)}")
      await pg.wait_for_timeout(4000)
      r2=await pg.evaluate("()=>{const c=document.querySelector('#s-mats .scard[id^=top-]');const x=window.R2CTX(c);return [c.dataset.id,x.rack,x.rack2]}")
      assert not r2[2] and r2[0]==k, f'bad {slug} {r2}'
      await pg.screenshot(path=OUT+f'table-{slug}.png'); print('  ok',r2)
    await b.close()
asyncio.run(main())
