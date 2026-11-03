"""Gate [154] (Tiffany Nov 3, QA r9: 'driving me crazy'): every WOOD TONE rack shows real grain / texture, never a flat fill, on every
render path. All rack pictures in the app (deck card, suitor tray, selected rack, match card, My hearts) go through rackSrc(id);
Table view draws TVD.ro[id] or rackSrc(id). This runs the page (Chromium), takes both images for every visible Wood tone rack, and
measures the fine texture inside the rack (luminance minus a 2px blur, std over opaque pixels). A flat colour render measures ~1-3;
real wood grain measures well above. Also checks no other code path reads R[id].im directly.
Usage: python3 wood_check.py <build dir> [sheet.jpg] -> [154] lines, exit 1 on failure."""
import sys, time, subprocess, socket, json, base64, io, re
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from playwright.sync_api import sync_playwright
SIG = 6.0
B = sys.argv[1].rstrip('/'); SHEET = sys.argv[2] if len(sys.argv) > 2 else None; MIN = 0.7
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
F = []
try:
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 390, 'height': 844}); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
        rows = pg.evaluate("""async()=>{const tv=D.tv||{},rt=tv.rt||{},out=[];const ids=Object.keys(rt).filter(k=>rt[k]==='wood'&&R[k]&&!R[k].hid);
          const get=async u=>{if(!u)return '';if(u.startsWith('data:'))return u;try{const b=await (await fetch(u)).blob();return await new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(b);});}catch(e){return ''}};
          for(const k of ids){const d=rackSrc(k),t=(tv.ro&&tv.ro[k])||d;out.push({k,n:R[k].n,deck:await get(d),table:await get(t)});}return out;}""")
        br.close()
finally: srv.kill()
def tex(uri):
    """Grain runs along the rack, so a real wood photo varies ALONG each row; a flat render is ~constant along a row (only its
    lip / shadow lines change row to row). Per row (interior pixels, 4px in from the outline): robust spread (1.4826 MAD) of the
    luminance minus its own smooth trend along the row; the metric is the median over rows."""
    if not uri: return None, None
    from scipy import ndimage
    im = Image.open(io.BytesIO(base64.b64decode(uri.split(',', 1)[1]))).convert('RGBA'); im.thumbnail((600, 600))
    a = np.asarray(im).astype(float); m = a[..., 3] > 200
    if m.all() or m.sum() < 200:  # photo on a white background (no cut-out): the rack = the non-white pixels
        c = a[..., :3]; m = ((c.max(2) - c.min(2)) > 14) | (c.mean(2) < 215)
    small = min(a.shape[:2]) < 60 or m.sum() < 6000; m = ndimage.binary_erosion(m, iterations=1 if small else 4); L = a[..., :3].mean(2); vals = []
    for y in range(L.shape[0]):
        xs = np.where(m[y])[0]
        if len(xs) < (12 if small else 60): continue
        row = L[y, xs]; d = row - ndimage.gaussian_filter1d(row, SIG, mode="nearest"); vals.append(1.4826 * np.median(np.abs(d - np.median(d))))
    return (round(float(np.median(vals)), 2) if vals else 0.0), im
res = []
for r in rows:
    for path in ('deck', 'table'):
        v, im = tex(r[path]); res.append((r['n'], path, v, im))
        if v is None: F.append(f"[154] {r['n']}: no {path} image")
        elif v < MIN: F.append(f"[154] Wood tone rack shows a flat fill, no grain ({path} view, texture {v} < {MIN}): {r['n']}")
UI = open(B + '/index.html').read(); i = UI.index('const D=') + 8; _, e = json.JSONDecoder().raw_decode(UI, i)
if len(re.findall(r'R\[[^\]]{1,12}\]\.im\b(?!=)', UI[e:])) > 1: F.append('[154] some code reads a rack picture without rackSrc (wood fix would not reach it)')
if SHEET:
    W = 560; S = Image.new('RGB', (W * 2, 70 * len(res) // 2 + 70), 'white'); dr = ImageDraw.Draw(S)
    for j, (n, path, v, im) in enumerate(res):
        x, y = (j % 2) * W, (j // 2) * 70
        if im is not None:
            t = im.copy(); t.thumbnail((360, 52)); bg = Image.new('RGB', t.size, '#ffffff' if j % 4 < 2 else '#1f2a44'); bg.paste(t, (0, 0), t); S.paste(bg, (x + 4, y + 4))
        dr.text((x + 370, y + 8), f'{n[:30]}\n{path}  tex {v}', fill='red' if (v or 0) < MIN else 'black')
    S.save(SHEET)
for f in F: print(f)
print('wood check', 'FAIL' if F else 'ok', json.dumps([(n, p_, v) for n, p_, v, _ in res])); sys.exit(1 if F else 0)
