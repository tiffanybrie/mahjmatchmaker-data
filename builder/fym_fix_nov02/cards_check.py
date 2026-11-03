"""Gate [150] (Tiffany Nov 3 2:43pm): My match cards = ONE card per tile set (a new mat for the same tiles replaces it), newest
first, old duplicates collapse on read, x remove + Undo work, the card button says 'Save image'. Runs the page's own code (WebKit).
Usage: python3 cards_check.py <build dir> -> [150] lines, exit 1 on failure."""
import sys, time, subprocess, socket, json
from playwright.sync_api import sync_playwright
B = sys.argv[1]; s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
F = []
try:
    with sync_playwright() as p:
        br = p.webkit.launch(); pg = br.new_context(**p.devices['iPhone 13']).new_page(); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
        r = pg.evaluate("""async()=>{const out={};const ss=D.sets.map((s,i)=>[s,i]).filter(([s])=>s.m&&s.m.length>1).slice(0,2);if(ss.length<2)return {err:'no test sets'};
          const [[a,ia],[b,ib]]=ss;const rk=Object.keys(R).filter(k=>!R[k].hid).slice(0,2);MCH.put([]);const save=(i,m,r)=>{S.set=i;S.fav=m;S.rpick=r;acctSaveMatch();};
          save(ia,a.m[0][0],[rk[0]]);await new Promise(r=>setTimeout(r,5));save(ia,a.m[1][0],[rk[0]]);await new Promise(r=>setTimeout(r,5));save(ib,b.m[0][0],[rk[1]]);
          let g=MCH.get();out.n=g.length;out.order=g.map(x=>x.t);out.aMat=(g.find(x=>x.t===a.slug)||{}).m===a.m[1][0];out.first=g[0].t===b.slug;
          // legacy duplicates on this device collapse on read
          LS.set(MCH.k,JSON.stringify([{t:a.slug,m:a.m[0][0],r:[],at:1},{t:a.slug,m:a.m[1][0],r:[],at:2},{t:b.slug,m:b.m[0][0],r:[],at:3}]));MCH.mem=null;g=MCH.get();out.legacyN=g.length;out.legacyNewest=(g.find(x=>x.t===a.slug)||{}).at===2&&g[0].t===b.slug;
          // remove + undo through the UI
          ACCT.tab='matches';openStars();const x=document.querySelector('#starsov [data-mrm]');out.btns=document.querySelectorAll('#starsov [data-mrm]').length;out.cards=document.querySelectorAll('#starsov [data-mopen]').length;
          x.click();out.afterRm=MCH.get().length;const t=document.getElementById('mctoast');out.toast=!!t&&!t.hidden&&/Undo/.test(t.textContent);
          document.querySelector('#mctoast [data-mundo]').click();out.afterUndo=MCH.get().length;closeStars();
          out.label=document.body.innerHTML.includes('Save image')||String(renderCard).includes('Save image')||document.documentElement.outerHTML.includes('Save image / Share');return out}""")
        br.close()
finally: srv.kill()
if r.get('err'): F.append('[150] ' + r['err'])
else:
    if r['n'] != 2: F.append(f"[150] a second mat for the same tile set added a card ({r['n']} cards, want 2)")
    if not r['aMat']: F.append("[150] the newer mat did not replace the tile set's card")
    if not r['first']: F.append("[150] newest card is not first")
    if r['legacyN'] != 2 or not r['legacyNewest']: F.append(f"[150] old duplicate cards on this device do not collapse to the newest per tile set ({r['legacyN']})")
    if r['btns'] != r['cards'] or not r['cards']: F.append(f"[150] not every match card has a remove button ({r['btns']} of {r['cards']})")
    if r['afterRm'] != 1 or not r['toast']: F.append(f"[150] remove did not remove the card or show the Undo toast ({r})")
    if r['afterUndo'] != 2: F.append("[150] Undo did not bring the card back")
    if not r['label']: F.append("[150] the card's save button does not say 'Save image'")
for f in F: print(f)
print('cards check', 'FAIL' if F else 'ok', json.dumps(r)); sys.exit(1 if F else 0)
