import os,sys,json
from playwright.sync_api import sync_playwright
H='/home/claude/mahjmatchmaker-data/site/livepatch/fym-preview-oct21/'
BLOCK=open(H+'page-block.html').read()
SWAP="""(html)=>{const m=document.querySelector('#fymp,#fymx');const box=m.closest('.sqs-block-content');box.innerHTML=html;
box.querySelectorAll('script').forEach(o=>{const n=document.createElement('script');n.textContent=o.textContent;o.replaceWith(n)});return !!document.getElementById('fymx')}"""
with sync_playwright() as p:
  b=p.chromium.launch(proxy={'server':os.environ['HTTPS_PROXY']} if os.environ.get('HTTPS_PROXY') else None,args=['--disable-dev-shm-usage'])
  for w,h in ((390,844),(1440,900)):
    ctx=b.new_context(viewport={'width':w,'height':h},is_mobile=w<500,has_touch=w<500)
    pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
    pg.goto('https://www.mahjmatchmaker.com/find-your-mat-ch-preview',wait_until='load',timeout=120000);pg.wait_for_timeout(3000)
    print(w,'swap',pg.evaluate(SWAP,BLOCK))
    fr=None
    for i in range(60):
      pg.wait_for_timeout(2000)
      for f in pg.frames:
        try:
          if f.evaluate("typeof D!=='undefined'&&typeof S!=='undefined'&&document.title"): fr=f
        except Exception: pass
      if fr: break
    if not fr: print('no app frame');continue
    print(w,'title',fr.evaluate('document.title'))
    r=fr.evaluate("""()=>{const PM=id=>/^mahjongrowandco\\.com\\//.test(id)||/^mahjongco\\.com\\//.test(id);
      const vis=D.sets.filter(VIS);const out={sets:vis.length,mr:vis.filter(s=>/Mahjong Row/.test(s.maker)).length,kal:vis.some(s=>/Kaleidoscope/.test(s.name)),
      visParkMats:Object.keys(M).filter(id=>!M[id].hid&&PM(id)).length,visMR_racks:Object.keys(R).filter(id=>!R[id].hid&&/mahjongrow/.test(id)).length,
      logos:[...document.querySelectorAll('[data-blogo]')].map(e=>e.dataset.blogo).filter(x=>/Mahjong/.test(x))};return out}""")
    print(w,json.dumps(r))
    sk=fr.query_selector('button.sk')
    if sk and sk.is_visible(): sk.click()
    fr.click('[data-door=tiles]');pg.wait_for_timeout(600);fr.fill('#tsq','Gatsby');pg.wait_for_timeout(500);fr.click('[data-tile="2"]');pg.wait_for_timeout(4000)
    fr.locator('[data-z="1"]').first.click();fr.locator('[data-z="1"]').first.click();pg.wait_for_timeout(500)
    fr.locator('.sb.no').first.click();pg.wait_for_timeout(1500);fr.locator('.sb.no').first.click();pg.wait_for_timeout(3000)
    z=fr.evaluate("()=>{const i=document.querySelector('#top-m img');return [S.zs.mz.s,i&&i.naturalWidth,i&&getComputedStyle(i).transform]}")
    print(w,'zoom after 2 swipes',z)
    pg.screenshot(path=f'qa/pageblock-{w}.png')
    print(w,'errs',errs[:5]);ctx.close()
  b.close()
