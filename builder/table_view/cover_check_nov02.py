"""Gate [147] (Tiffany Nov 2 8:15am: 'a corner view must FILL THE WHOLE SQUARE'): render EVERY mat Table view can show (full and
Corner class) the way the app shows it, with the table background painted magenta (window.TVPROBE), and fail any render where
background shows: each mat is rendered twice, background magenta then green, and any pixel that changes is
uncovered background (> 0.3% of the square fails; a mat that is itself magenta or green can't fool it). Also writes a contact sheet of every Corner render for a by-eye look.
Usage: python3 cover_check_nov02.py <build dir> [sheet.jpg]  -> [147] FAIL lines, exit 1 on failure."""
import sys, time, subprocess, socket, base64, io, json
import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
B = sys.argv[1]; SHEET = sys.argv[2] if len(sys.argv) > 2 else None
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
F = []; corners = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
        G = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..', 'config', 'tableview-gray-nov02.json')))['mats']
        for k, n in G.items():  # QA Nov 2: no clean top-down photo -> must be grayed in Table view
            if pg.evaluate("k=>!!M[k]&&TVD.cls[k]!=='C'", k): F.append(f"[147] {n}: should be grayed in Table view (config/tableview-gray-nov02.json)")
        ks = pg.evaluate("Object.keys(M).filter(k=>!M[k].hid&&TVD.cls[k]&&TVD.cls[k]!=='C')"); 
        slug = 'oh-my-mahjong-papaya-spritz'; rack = pg.evaluate("Object.keys(TVD.rk)[0]")
        for i in range(0, len(ks), 25):
            out = pg.evaluate("""async([ks,slug,rack])=>{const o={};for(const k of ks){try{window.TVPROBE='#ff00ff';const a=await TVRENDER(k,slug,rack,240);window.TVPROBE='#00ff00';const b=await TVRENDER(k,slug,rack,240);window.TVPROBE=null;o[k]=[TVD.cls[k],a,b]}catch(e){window.TVPROBE=null;o[k]=[TVD.cls[k],null,null]}}return o}""", [ks[i:i + 25], slug, rack])
            for k, (cl, u, u2) in out.items():
                if not u or not u2: F.append(f"[147] {k}: Table render failed"); continue
                im = Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'); a = np.asarray(im).astype(int)
                a2 = np.asarray(Image.open(io.BytesIO(base64.b64decode(u2.split(',')[1]))).convert('RGB')).astype(int)
                mag = (np.abs(a - a2).max(2) > 90).mean()
                if mag > .003: F.append(f"[147] {pg.evaluate('k=>M[k].n+\" | \"+M[k].bn', k)} ({'Corner' if cl == 'B' else 'Full'} view): {mag * 100:.1f}% of the square shows no mat")
                if cl == 'B': corners.append((k, im))
        names = pg.evaluate("ks=>ks.map(k=>M[k].bn+' | '+M[k].n)", [k for k, _ in corners]); b.close()
finally: srv.kill()
if SHEET and corners:
    S = 240; W = 8; o = Image.new('RGB', (W * S, ((len(corners) + W - 1) // W) * (S + 14)), 'white'); d = ImageDraw.Draw(o)
    for i, ((k, im), n) in enumerate(zip(corners, names)): x, y = (i % W) * S, (i // W) * (S + 14); o.paste(im.resize((S, S)), (x, y)); d.text((x + 2, y + S), n[:40], fill='black')
    o.save(SHEET, quality=84)
print(f"checked {len(ks)} mats, corner renders {len(corners)}")
for f in F[:40]: print(f)
sys.exit(1 if F else 0)
