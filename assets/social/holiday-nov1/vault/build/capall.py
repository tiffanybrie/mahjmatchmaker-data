import sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
O='/dev/shm/vault-tour/cap/'
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
def warm(pg,h):
    y=0
    while y<h:
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(180); y+=500
    pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(1200)
def strip(pg,y0,y1,name):
    parts=[];y=y0
    while y<y1:
        h=min(2000,y1-y); f=f'{O}_seg.png'
        pg.screenshot(path=f,full_page=True,clip={'x':0,'y':y,'width':390,'height':h})
        parts.append(Image.open(f).convert('RGB')); y+=h
    W=parts[0].width; H=sum(p.height for p in parts); im=Image.new('RGB',(W,H)); yy=0
    for p in parts: im.paste(p,(0,yy)); yy+=p.height
    im.save(O+name+'.jpg',quality=90); print(name,im.size)
meta={}
targets=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,user_agent=UA)
    def go(u,warmh=None):
        pg=ctx.new_page(); pg.goto(u,wait_until='networkidle',timeout=90000)
        h=pg.evaluate('document.body.scrollHeight'); warm(pg,warmh or h); return pg
    if 'xmas' in targets:
        pg=go('https://www.mahjmatchmaker.com/christmas-mahjong-mats'); h=pg.evaluate('document.body.scrollHeight')
        meta['xmas_h']=h; strip(pg,0,min(h,8800),'xmas'); pg.close()
    if 'hol' in targets:
        pg=go('https://www.mahjmatchmaker.com/holiday-mahjong-matches',12000)
        meta['hol']=pg.evaluate("""(()=>{const r=s=>{const e=document.querySelector(s);return e?e.getBoundingClientRect().top+scrollY:null};return {nh:r('#new-holiday-sets'),hm:r('#holiday-matches')}})()""")
        strip(pg,0,11000,'hol'); pg.close()
    if 'albums' in targets:
        for a in ['nantucket','jade','malachite','heritage-2-0','moonlight','birdie','osler','smith','gatsby']:
            pg=ctx.new_page(); pg.goto(f'https://www.mahjmatchmaker.com/{a}-mahjong-tile-matches',wait_until='networkidle',timeout=90000)
            y=pg.evaluate("(()=>{const a=[...document.querySelectorAll('[id=holiday]')].map(e=>e.getBoundingClientRect().top+scrollY);return a.length?Math.max(...a):-1})()")
            if y<0: print('no holiday',a); pg.close(); continue
            yy=int(y)
            for k in range(0,2600,400): pg.evaluate(f'window.scrollTo(0,{yy+k})'); pg.wait_for_timeout(250)
            pg.wait_for_timeout(1000); strip(pg,max(0,yy-40),yy+1800,'alb_'+a); meta['alb_'+a]=yy; pg.close()
    if 'fym' in targets:
        ctx2=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,user_agent=UA)
        pg=ctx2.new_page(); pg.goto('https://www.mahjmatchmaker.com/find-your-match',wait_until='networkidle',timeout=90000); pg.wait_for_timeout(2500)
        fr=[f for f in pg.frames if f.url=='about:srcdoc'][0]
        fr.get_by_text('No thanks').click(); pg.wait_for_timeout(500)
        fr.locator('button:has-text("Start with a mat")').click(); pg.wait_for_timeout(1000)
        fr.evaluate("window.scrollTo(0,1000)"); pg.wait_for_timeout(300)
        pg.screenshot(path=O+'fym_before.png')
        fr.locator('[data-dfam="holiday"]').first.click(); pg.wait_for_timeout(2000)
        pg.screenshot(path=O+'fym_after.png')
        for i in range(4):
            try: fr.get_by_text('Show more mats').click(timeout=3000); pg.wait_for_timeout(1500)
            except Exception: break
        H=fr.evaluate('document.documentElement.scrollHeight'); meta['fym_h']=H
        n=fr.evaluate("document.body.innerText.split('☆').length-1"); meta['fym_cards']=n
        # tall viewport to capture the frame content
        pg.set_viewport_size({'width':390,'height':min(H,9000)}); pg.wait_for_timeout(2500)
        for k in range(0,H,500): fr.evaluate(f'window.scrollTo(0,{k})'); pg.wait_for_timeout(150)
        fr.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(2500)
        pg.screenshot(path=O+'fym_tall.png'); print('fym',H,n)
    b.close()
json.dump(meta,open(O+'meta_'+'_'.join(targets)+'.json','w')); print(meta)
