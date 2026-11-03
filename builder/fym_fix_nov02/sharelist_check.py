"""Gate [149]: 'Text or email me this list' always shows something (toast or sheet), in WebKit (iPhone) and Chromium (desktop):
share undefined -> toast + sheet; share throws NotAllowedError -> toast + sheet; share throws AbortError (user cancelled) -> toast;
share succeeds -> toast. Copy happens before any await. Usage: python3 sharelist_check.py <build dir> -> [149] lines, exit 1 on fail."""
import sys, time, subprocess, socket
from playwright.sync_api import sync_playwright
B = sys.argv[1]; s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
F = []
CASES = {'none': "delete Navigator.prototype.share;try{Object.defineProperty(navigator,'share',{value:undefined,configurable:true})}catch(_){}",
         'notallowed': "Object.defineProperty(navigator,'share',{value:()=>Promise.reject(new DOMException('no','NotAllowedError')),configurable:true})",
         'throws': "Object.defineProperty(navigator,'share',{value:()=>{throw new TypeError('bad')},configurable:true})",
         'abort': "Object.defineProperty(navigator,'share',{value:()=>Promise.reject(new DOMException('x','AbortError')),configurable:true})",
         'ok': "Object.defineProperty(navigator,'share',{value:()=>Promise.resolve(),configurable:true})"}
WANT = {'none': (1, 1), 'notallowed': (1, 1), 'throws': (1, 1), 'abort': (1, 0), 'ok': (1, 0)}
try:
    with sync_playwright() as p:
        for eng, ctx in (('webkit', p.devices['iPhone 13']), ('chromium', {'viewport': {'width': 1280, 'height': 800}})):
            br = getattr(p, eng).launch(); pg = br.new_context(**ctx).new_page(); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
            pg.evaluate("()=>{S.set=D.sets.findIndex(s=>s.m&&s.m.length);S.fav=D.sets[S.set].m[0][0];}")
            for c, js in CASES.items():
                pg.evaluate("js=>{(document.getElementById('slsheet')||{remove(){}}).remove();const t=document.getElementById('sltoast');if(t)t.hidden=true;new Function(js)();window.__cp=null;try{navigator.clipboard.writeText=x=>{window.__cp=x;return Promise.resolve()}}catch(_){}}", js)
                pg.evaluate("()=>{const b=document.createElement('button');b.setAttribute('data-shoplist','');document.body.appendChild(b);b.click();b.remove()}"); time.sleep(.4)
                r = pg.evaluate("()=>{const t=document.getElementById('sltoast'),s=document.getElementById('slsheet');const vis=e=>!!e&&!e.hidden&&e.getBoundingClientRect().height>0;return {toast:vis(t)?1:0,sheet:vis(s)?1:0,txt:t?t.textContent:'',links:s?[...s.querySelectorAll('a')].map(a=>a.getAttribute('href').slice(0,9)):[],cp:(window.__cp||'').length}}")
                tw, sw = WANT[c]
                if r['toast'] != tw or r['sheet'] != sw: F.append(f"[149] {eng} share={c}: toast {r['toast']} sheet {r['sheet']} (want toast {tw} sheet {sw})")
                if not (r['toast'] or r['sheet']): F.append(f"[149] {eng} share={c}: the tap shows nothing")
                if sw and r['links'] != ['mailto:?s', 'sms:&body']: F.append(f"[149] {eng} share={c}: sheet links wrong: {r['links']}")
                if r['cp'] < 50: F.append(f"[149] {eng} share={c}: the list was not copied")
            br.close()
finally: srv.kill()
for f in F: print(f)
print('sharelist check', 'FAIL' if F else 'ok'); sys.exit(1 if F else 0)
