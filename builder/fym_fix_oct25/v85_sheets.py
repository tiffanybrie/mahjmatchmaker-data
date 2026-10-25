"""Contact sheets for the colour-ranking audit: per tile set, the tile photo + the first 6 mats the app shows (picks off).
Usage: python3 v85_sheets.py <build_dir> <out_dir> [only_unmatched=1]"""
import sys, os, json, re
from PIL import Image, ImageDraw, ImageFont
B, OUT = sys.argv[1], sys.argv[2]; only = (sys.argv[3] if len(sys.argv) > 3 else '1') == '1'
os.makedirs(OUT, exist_ok=True)
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
M = D['mats']; order = D['order']
fn = lambda k: '/tmp/v85img/' + re.sub(r'[^a-z0-9]+', '_', k.lower())[:90] + '.png'
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except Exception: F = ImageFont.load_default()
SZ, PER = 150, 8
sets = [(j, s) for j, s in enumerate(D['sets']) if (not s['m'] or not only) and s.get('cr')]
idx = []
for b0 in range(0, len(sets), PER):
    chunk = sets[b0:b0 + PER]; W = SZ * 7 + 10; Hh = (SZ + 34) * len(chunk)
    sh = Image.new('RGB', (W, Hh), 'white'); d = ImageDraw.Draw(sh)
    for r, (j, s) in enumerate(chunk):
        y = r * (SZ + 34); t = D['tiles'].get(s['tile']) or {}
        try:
            im = Image.open(B + '/' + t['full']).convert('RGB'); im.thumbnail((SZ, SZ)); sh.paste(im, (0, y + 16))
        except Exception: pass
        d.text((2, y), f"#{j} {s['name']} ({s['maker']})"[:60], fill='black', font=F)
        for c, oi in enumerate(s['cr'][:6]):
            m = order[oi]
            try:
                im = Image.open(fn(m)).convert('RGB'); im.thumbnail((SZ - 6, SZ - 6)); sh.paste(im, (SZ * (c + 1) + 10, y + 16))
            except Exception: pass
            d.text((SZ * (c + 1) + 10, y + SZ + 16), f"{c+1} {M[m]['n']}"[:22], fill='black', font=F)
    p = f'{OUT}/sheet{b0 // PER:02d}.jpg'; sh.save(p, quality=80); idx.append(p)
print(len(sets), 'sets,', len(idx), 'sheets in', OUT)
