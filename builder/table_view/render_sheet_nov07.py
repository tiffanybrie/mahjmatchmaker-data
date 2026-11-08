"""Contact sheet of REAL Table view renders (the app's own window.TVRENDER in Chromium), for the by-eye look every mat gets
before it is marked usable (Nov 7). Each tile: the table as the app shows it (full or corner by D.tv.cls; class C / unclassified
mats are rendered as full tables so they can be judged), label '#i cls brand | name'. Also flags renders where table background
shows (magenta/green probe like gate [147]).
Usage: python3 render_sheet_nov07.py <build dir> <keys.json> <out prefix> [--slug juniper] [--px 300] [--per 30]"""
import sys, time, subprocess, socket, base64, io, json, os
import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
B, KJ, OUT = sys.argv[1:4]
arg = lambda f, d: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else d
SLUG = arg('--slug', 'juniper'); PX = int(arg('--px', 300)); PER = int(arg('--per', 30))
keys = json.load(open(KJ))
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
res = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
        rack = pg.evaluate("s=>TVPICK(s,null)||Object.keys(TVD.rk)[0]", SLUG)
        for i in range(0, len(keys), 20):
            out = pg.evaluate("""async([ks,slug,rack,px])=>{const o={};for(const k of ks){if(!M[k]){o[k]=null;continue}const cl=TVD.cls[k]||'-';const cor=cl==='B';
              try{window.TVPROBE='#ff00ff';const a=await TVRENDER(k,slug,rack,px,cor);window.TVPROBE='#00ff00';const b2=await TVRENDER(k,slug,rack,px,cor);window.TVPROBE=null;
              o[k]=[cl,M[k].bn+' | '+M[k].n,a,b2]}catch(e){window.TVPROBE=null;o[k]=[cl,M[k].bn+' | '+M[k].n,null,null]}}return o}""", [keys[i:i + 20], SLUG, rack, PX])
            for k in keys[i:i + 20]:
                v = out.get(k)
                if not v or not v[2]: res.append((k, '?', k, None, None)); continue
                a = Image.open(io.BytesIO(base64.b64decode(v[2].split(',')[1]))).convert('RGB')
                a2 = Image.open(io.BytesIO(base64.b64decode(v[3].split(',')[1]))).convert('RGB')
                mag = float((np.abs(np.asarray(a).astype(int) - np.asarray(a2).astype(int)).max(2) > 90).mean())
                res.append((k, v[0], v[1], a, mag))
        b.close()
finally: srv.kill()
W = 6; L = 30
for si in range(0, len(res), PER):
    chunk = res[si:si + PER]; o = Image.new('RGB', (W * PX, ((len(chunk) + W - 1) // W) * (PX + L)), 'white'); d = ImageDraw.Draw(o)
    for j, (k, cl, n, im, mag) in enumerate(chunk):
        x, y = (j % W) * PX, (j // W) * (PX + L)
        if im: o.paste(im.resize((PX, PX)), (x, y))
        else: d.rectangle([x, y, x + PX - 1, y + PX - 1], fill='#ccc'); d.text((x + 8, y + 8), 'RENDER FAILED', fill='red')
        t = f'#{si + j} {cl} {n}'; d.text((x + 2, y + PX + 2), t[:46], fill='black'); d.text((x + 2, y + PX + 15), t[46:92], fill='black')
        if mag and mag > .003: d.text((x + 4, y + 4), f'BG {mag * 100:.1f}%', fill='red')
    o.save(f'{OUT}_{si // PER:02d}.jpg', quality=82)
json.dump([[k, cl, n, mag] for k, cl, n, _, mag in res], open(OUT + '.json', 'w'), indent=0)
print('rendered', len(res), 'sheets', (len(res) + PER - 1) // PER, 'bg>0.3%:', sum(1 for r in res if r[4] and r[4] > .003), 'failed:', sum(1 for r in res if r[3] is None))
