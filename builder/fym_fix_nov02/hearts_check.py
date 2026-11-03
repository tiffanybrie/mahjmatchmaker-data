"""Gate [153] (Tiffany Nov 3 2:58pm): stars became hearts. No star glyph in the app UI; every mat and rack hearted while swiping
is saved to My hearts (deduped); each My hearts item has an x that removes it; the match card shows the account prompt
(signed out: sign-in button; signed in: 'Saved to your account'). Runs the page's own code (WebKit, iPhone 13).
Usage: python3 hearts_check.py <build dir> -> [153] lines, exit 1 on failure."""
import sys, time, subprocess, socket, json
from playwright.sync_api import sync_playwright
B = sys.argv[1]; s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
F = []; r = {}
try:
    with sync_playwright() as p:
        br = p.webkit.launch(); pg = br.new_context(**p.devices['iPhone 13']).new_page(); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
        r = pg.evaluate("""async()=>{const out={};const w=ms=>new Promise(r=>setTimeout(r,ms));LS.set(STAR.k,'[]');STAR.mem=null;
          const ia=D.sets.findIndex(s=>s.m&&s.m.length&&VIS(s));S.set=ia;renderAll();await w(50);
          const qm=queue('m');out.qm=qm.length;const m1=qm[0];decide('m',true);decide('m',true);out.m=STAR.has('m:'+m1);
          S.fav=m1;renderAll();await w(50);const qr=queue('r');out.qr=qr.length;const r1=qr[0];decide('r',true);out.r=STAR.has('r:'+r1);
          out.dupe=STAR.get().filter(x=>x==='m:'+m1).length;HSAVE('m:'+m1);out.dupe2=STAR.get().filter(x=>x==='m:'+m1).length;
          ACCT.tab='stars';openStars();await w(20);const ov=document.getElementById('starsov');out.items=ov.querySelectorAll('.stb[data-star]').length;out.x=ov.querySelectorAll('.stb.hrm').length;
          out.title=(ov.querySelector('h2')||{}).textContent;const n0=STAR.get().length;ov.querySelector('.stb.hrm').click();await w(50);out.rm=n0-STAR.get().length;
          out.items2=document.querySelectorAll('#starsov .stb[data-star]').length;out.sheetText=document.getElementById('starsov').innerText;closeStars();
          S.rpick=[r1];S.made=true;try{renderCard();}catch(e){out.cerr=String(e);}await w(20);const a=document.querySelector('#s-card .acp');out.acp=a?a.innerText:'';out.acpBtn=!!(a&&a.querySelector('[data-acct]'));
          ACCT.user={email:'qa@example.com'};acctTop();out.acp2=a?a.innerText:'';ACCT.user=null;acctTop();
          out.top=(document.querySelector('.tbb[data-mystars]')||{}).textContent;out.body=/[★☆]/.test(document.body.innerText);return out}""")
        br.close()
finally: srv.kill()
UI = open(B.rstrip('/') + '/index.html' if not B.endswith('.html') else B).read()
i = UI.index('const D=') + 8; _, e = json.JSONDecoder().raw_decode(UI, i); UIc = UI[:i] + UI[e:]
if '★' in UIc or '☆' in UIc: F.append('[153] a star glyph is still in the app UI (stars became hearts, hearts114.py)')
if 'My stars' in UIc: F.append("[153] 'My stars' is still in the app UI (now 'My hearts')")
if not r.get('qm') or not r.get('qr'): F.append(f"[153] check could not reach the mat/rack swipe ({r})")
else:
    if not r['m']: F.append('[153] a mat hearted while swiping was not saved to My hearts')
    if not r['r']: F.append('[153] a rack hearted while swiping was not saved to My hearts')
    if r['dupe'] != 1 or r['dupe2'] != 1: F.append('[153] My hearts saves the same mat twice')
    if not r['items'] or r['x'] != r['items']: F.append(f"[153] not every My hearts item has an x to remove it ({r['x']} of {r['items']})")
    if r['rm'] != 1 or r['items2'] != r['items'] - 1: F.append(f"[153] the x did not remove the item from My hearts ({r['rm']}, {r['items']}->{r['items2']})")
    if 'My hearts' not in (r['title'] or ''): F.append(f"[153] the sheet is not titled My hearts ({r['title']})")
    if r.get('cerr'): F.append('[153] match card did not render: ' + r['cerr'])
    if not r['acpBtn'] or 'sign in with your email' not in r['acp']: F.append(f"[153] signed out, the match card has no 'sign in with your email' prompt ({r['acp']!r})")
    if 'Saved to your account' not in r['acp2']: F.append(f"[153] signed in, the match card does not say 'Saved to your account' ({r['acp2']!r})")
    if r['body']: F.append('[153] a star glyph shows on the page')
for f in F: print(f)
print('hearts check', 'FAIL' if F else 'ok', json.dumps({k: v for k, v in r.items() if k != 'sheetText'})); sys.exit(1 if F else 0)
