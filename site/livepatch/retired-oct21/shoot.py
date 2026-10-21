import sys, asyncio, os
from playwright.async_api import async_playwright
# usage: shoot.py <mode: after|live> <outprefix>
mode=sys.argv[1]; pre=sys.argv[2] if len(sys.argv)>2 else mode
pages=sorted(f for f in os.listdir('after'))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--disable-dev-shm-usage'])
    for w,h in [(390,844),(1280,800)]:
      ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
      pg=await ctx.new_page()
      for f in pages:
        slug=f[:-5]
        if mode=='after': await pg.goto('file://'+os.path.abspath('after/'+f),wait_until='domcontentloaded',timeout=60000)
        else: await pg.goto('https://www.mahjmatchmaker.com/'+slug+'?v=qa'+str(os.getpid()),wait_until='domcontentloaded',timeout=60000)
        await pg.wait_for_timeout(2500)
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        # header area / first pill
        sel = '.mm3-hero' if pg.url and await pg.query_selector('.mm3-tret') else None
        target = await pg.query_selector('.mm3-hero') if await pg.query_selector('.mm3-tret') else None
        if target:
          await target.scroll_into_view_if_needed(); await pg.wait_for_timeout(1500)
          await target.screenshot(path=f'qa/{pre}-{slug}-hero-{w}.png')
        pills = await pg.query_selector_all('.mm-retpill')
        for n,el in enumerate(pills[:3]):
          card = await el.evaluate_handle('e=>e.closest("a").parentElement')
          await card.scroll_into_view_if_needed(); await pg.wait_for_timeout(1800)
          bb = await card.bounding_box()
          clipH=min(bb['height'], 1100)
          await pg.screenshot(path=f'qa/{pre}-{slug}-covers{n+1}-{w}.png', clip={'x':0,'y':max(0,bb['y']),'width':w,'height':clipH}, full_page=False) if bb['y']>=0 else await card.screenshot(path=f'qa/{pre}-{slug}-covers{n+1}-{w}.png')
        # horizontal overflow check
        ov = await pg.evaluate('document.documentElement.scrollWidth - innerWidth')
        print(w, slug, 'pills', len(pills), 'hero', bool(target), 'overflowX', ov, flush=True)
      await ctx.close()
    await b.close()
asyncio.run(main())
