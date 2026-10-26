import sys
from playwright.sync_api import sync_playwright
TILE,MAT,BRAND,OUT=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
RB=sys.argv[5] if len(sys.argv)>5 else BRAND
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':797},device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    import os,base64
    if os.environ.get('MATFIX'):
        k_,n_=os.environ['MATFIX'].split('|||'); print('matfix',pg.evaluate("([k,n])=>{if(!M[k])return false;M[k].n=n;M[k].dn=n;return true}",[k_,n_]))
    if os.environ.get('MATOV'):  # MATOV0
        mu0='data:image/jpeg;base64,'+base64.b64encode(open(os.environ['MATOV'],'rb').read()).decode()
        print('matov0',pg.evaluate("([m,br,u])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);MC[M[id].f]=u;return id}",[MAT,BRAND,mu0]))
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type(TILE); pg.wait_for_timeout(1200)
    pg.evaluate("(t)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t)).click()",TILE); pg.wait_for_timeout(1200)
    pg.evaluate("([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);S.f.m.her=false;S.f.m.brand=br;S.mfront=id;renderAll();}",[MAT,BRAND]); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-360)}"); pg.wait_for_timeout(3000)
    pg.screenshot(path=OUT+'_swipe.png')
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1500)
    pg.evaluate("(m)=>[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop().click()",MAT); pg.wait_for_timeout(1500)
    pg.evaluate("(br)=>{S.f.r.her=false;S.f.r.brand=br;renderRacks();}",RB); pg.wait_for_timeout(2500)
    RK=sys.argv[6].split(',') if len(sys.argv)>6 else []
    OV=sys.argv[7].split(',') if len(sys.argv)>7 and sys.argv[7] else []
    if OV:
        import base64
        ov={r:'data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode() for r,f in zip(RK,OV) if f}
        pg.evaluate("""async(ov)=>{const ix=await hdIndex();ix.r=ix.r||{};for(const k in ov){ix.r[k]='file:'+ov[k];IMG[R[k].im]=ov[k];R[k].c=true;}}""",ov)
    if RK: pg.evaluate("(r)=>{S.rpick=r;S.rliked=r.slice();renderRacks();}",RK); pg.wait_for_timeout(1500)
    import os
    if not os.environ.get('TCFIX') and not os.environ.get('TCAUTO'): os.environ['TCFIX']=pg.evaluate("()=>{const h=set().tc||'#d6247f';let r=parseInt(h.slice(1,3),16)/255,g=parseInt(h.slice(3,5),16)/255,b=parseInt(h.slice(5,7),16)/255;const mx=Math.max(r,g,b),mn=Math.min(r,g,b);let H=0,S=0,L=(mx+mn)/2;if(mx!==mn){const d=mx-mn;S=L>.5?d/(2-mx-mn):d/(mx+mn);H=(mx===r?(g-b)/d+(g<b?6:0):mx===g?(b-r)/d+2:(r-g)/d+4)/6;}if(L<=.62)return h;/* same hue + saturation, only darker so a pale colour-card colour stays readable */return `hsl(${Math.round(H*360)},${Math.round(Math.max(S,.35)*100)}%,50%)`;}")  # Tiffany Oct 26: use the set's assigned colour-card colour, never the contrast-darkened one
    if os.environ.get('TCFIX'): print('tcfix',pg.evaluate("""(c)=>{const src=drawCard.toString();const i=src.indexOf('const tc=(()=>');const j=src.indexOf('})();',i)+5;const ns=src.slice(0,i)+"const tc='"+c+"';"+src.slice(j);window.drawCard=(0,eval)('('+ns+')');try{drawCard=window.drawCard}catch(e){};return i>0}""",os.environ['TCFIX']))
    if os.environ.get('SRCPATCH'):
        for pr in os.environ['SRCPATCH'].split(';;'):
            o_,n_=pr.split('|||'); print('patch',pg.evaluate("""([o,n])=>{const src=drawCard.toString();if(!src.includes(o))return false;window.drawCard=(0,eval)('('+src.split(o).join(n)+')');try{drawCard=window.drawCard}catch(e){};return true}""",[o_,n_]))
    if os.environ.get('MATOV'):
        import base64
        mu='data:image/jpeg;base64,'+base64.b64encode(open(os.environ['MATOV'],'rb').read()).decode()
        print('matov',pg.evaluate("(u)=>{MC[M[S.fav].f]=u;return !!S.fav}",mu))
    Z=float(os.environ.get('TZOOM','0') or 0)
    if Z>1: pg.evaluate("""async(z)=>{const s=set();const t=T[s.tile];const u=(t.cf&&!t.soon?t.cf:null)||(await tileFull(s))||pile(s);const im=await lk(u);const c=document.createElement('canvas');const w=im.width/z,h=im.height/z;c.width=w;c.height=h;c.getContext('2d').drawImage(im,(im.width-w)/2,(im.height-h)/2,w,h,0,0,w,h);t.cf=c.toDataURL('image/jpeg',.92);}""",Z); pg.wait_for_timeout(800)
    if not os.environ.get('KEEPCODE'): pg.evaluate("()=>{window.codeLine=()=>'';try{codeLine=()=>''}catch(e){}}")
    pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&b.innerText.includes('official')).pop().click()"); pg.wait_for_timeout(4500)
    ok=pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');if(!b)return 0;b.click();return 1}")
    pg.wait_for_timeout(800)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Post'));if(b)b.click();}"); pg.wait_for_timeout(3000)
    if ok: pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');window.scrollTo(0,b.getBoundingClientRect().top+scrollY-75)}"); pg.wait_for_timeout(2500)
    print('card',ok, pg.evaluate("S.rpick"))
    pg.screenshot(path=OUT+'_card.png')
    b.close()
