"""Re-draw the RACK MATCHES panel on finished Mat Edit cards with REAL rack photos (Tiffany, Oct 15).
Everything else on the card stays pixel-identical: only the cream rack box is replaced.
- Bird & Bamboo picks stay painted colour bars (B&B is the one rack we generate, doc 48).
- Any other brand's pick shows its real rack photo (assets/racks/card/index.json, see scripts/albumcard/real_racks.py).
Usage: python3 scripts/matcard/rackpanel.py config/matcard/<mat>.json <in_dir> <out_dir>
  spec racks: [[label, hex, dark, photo_rack_name_or_empty, ...]]; spec panel_boxes: {"fb":[x0,y0,x1,y1],"pin":[...]}
  (the story size has no rack panel, so story PNGs are copied unchanged)."""
import json, sys, os, io, base64, shutil, subprocess, glob
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.environ.get('MATCARD_FONTS', '/tmp/cc/f/')
IDX = json.load(open(ROOT + '/assets/racks/card/index.json'))['racks']
spec, src, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True); tmp = out + '/_tmp'; os.makedirs(tmp, exist_ok=True)

def b64(im):
    b = io.BytesIO(); im.save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def panel_html(w, h):
    rows, missing = [], []
    for r in spec['racks']:
        name, hx, dark = r[0], r[1], r[2]
        real = r[3] if len(r) > 3 else ''
        if real:
            if real not in IDX: missing.append(real); continue
            im = Image.open(ROOT + '/' + IDX[real]['file']).convert('RGBA'); im.thumbnail((520, 120))
            rows.append(f"<div class=rp><img src='{b64(im)}'><span>{name}</span></div>")
        else:
            rows.append(f"<div class=rk style='background:{hx};color:{'#fff' if dark else '#2a2036'}'>{name}</div>")
    return f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:'Bitter';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-400-normal.woff2)}}
@font-face{{font-family:'BitterB';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-700-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#f6e9df}}
.rks{{width:{w}px;height:{h}px;display:flex;flex-direction:column;justify-content:center;gap:6px;background:#fff8f2;border-radius:18px;padding:12px 16px}}
.rk{{font-family:BitterB;font-size:17px;padding:6px 12px;border-radius:6px;box-shadow:inset 0 -4px 0 rgba(0,0,0,.12)}}
.rp{{display:flex;align-items:center;gap:10px;height:42px;padding:0 4px;border-radius:6px;background:#f3e6da}}
.rp img{{height:38px;width:168px;object-fit:contain;object-position:left center;filter:drop-shadow(0 2px 2px rgba(0,0,0,.25))}}
.rp span{{font-family:BitterB;font-size:17px;color:#2a2036;line-height:1.1}}
small{{font-family:Bitter;font-size:13px;color:#6b5a77;text-align:center;line-height:1.3}}
</style></head><body><div class=rks>{''.join(rows)}<small>{spec.get('rackNote', '')}</small></div></body></html>""", missing

NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
JS = """const {chromium}=require('playwright');(async()=>{const a=process.argv.slice(2);const b=await chromium.launch();
for(let i=0;i<a.length;i+=4){const p=await b.newPage({viewport:{width:+a[i+2],height:+a[i+3]}});await p.goto('file://'+a[i]);
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);await p.screenshot({path:a[i+1]});await p.close()}await b.close()})();"""
open(tmp + '/shot.js', 'w').write(JS)
allmiss = set()
for f in sorted(glob.glob(src + '/*.png')):
    base = os.path.basename(f); size = base.rsplit('-', 1)[-1][:-4]
    box = spec.get('panel_boxes', {}).get(size)
    if not box: shutil.copy(f, out + '/' + base); continue
    x0, y0, x1, y1 = box; w, h = x1 - x0 + 1, y1 - y0 + 1
    html, miss = panel_html(w, h); allmiss |= set(miss)
    hf = f'{tmp}/{base}.html'; pf = f'{tmp}/{base}.panel.png'; open(hf, 'w').write(html)
    subprocess.run(['node', tmp + '/shot.js', hf, pf, str(w), str(h)], check=True, env={**os.environ, 'NODE_PATH': NP})
    card = Image.open(f).convert('RGB'); card.paste(Image.open(pf).convert('RGB'), (x0, y0)); card.save(out + '/' + base, optimize=True)
shutil.rmtree(tmp)
print('done ->', out, '| no real photo:', sorted(allmiss) or 'none')
