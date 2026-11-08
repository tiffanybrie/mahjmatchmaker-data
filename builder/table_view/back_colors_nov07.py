"""Table view walls for every set we can confirm (Nov 7 2026, Tiffany 8:13pm: every album set fully built in Find Your Mat-ch,
walls included, BEFORE she reviews the album; Juniper showed "Walls off: back color not confirmed yet").

Reads config/tableview-back-boxes-nov07.json (a box inside ONE real tile back per set, picked by eye on gridded contact sheets and
checked as back photo | wall swatch) and ADDS each set to config/tableview-back-colors.json:
  solid   -> median colour of the box (light glare and dark seams trimmed)
  pattern -> texture patch assets/table-view/backs/<slug>.webp (walls cut random 60% windows from it) + its median colour
  sprite  -> one whole back tile assets/table-view/backs/<slug>-sprite.webp, drawn as every wall tile (printed backs: Bam Bird
             Deco / MCM / Origami / East Meets West, YMI Toucan / Panda / God of Fortune / Peony / Koi, PLM Spirit of Christmas)
The Nov 1 entries (back_colors_nov01.py) are never overwritten. Sets in `_needs_eye` get NO walls (shown grayed "not confirmed")
until Tiffany confirms; never guess. preview_nov01.py --release carries the file into the build as D.tv.backs (b / p / s).

Usage: python3 builder/table_view/back_colors_nov07.py <fym build dir>   (the build's tile photos are used where img is null)
Check: python3 builder/table_view/back_colors_nov07.py <build> --sheet out.jpg   (contact sheet: photo with box | crop | wall)"""
import sys, json, io, struct, glob, pathlib, random
import numpy as np
from PIL import Image, ImageDraw
R = pathlib.Path(__file__).resolve().parents[2]
B = sys.argv[1]
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
MC = {}
for f in glob.glob(B + '/mc/*.webp'):
    ab = open(f, 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]
    try: hh = json.loads(ab[-4 - n:-4])
    except Exception: continue
    for k, (a, l) in hh.items(): MC[k] = (f, a, l)
SETS = {s['slug']: s for s in D['sets']}
def photo(slug, img):
    if img: im = Image.open(R / img)
    else:
        p = D['tiles'][SETS[slug]['tile']]['full']
        if p in MC: f, a, l = MC[p]; im = Image.open(io.BytesIO(open(f, 'rb').read()[a:a + l]))
        else: im = Image.open(B + '/' + p)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); im = bg
    return im.convert('RGB')
def med(crop):
    c = np.asarray(crop).reshape(-1, 3).astype(float); v = c.max(1)
    k = (v <= np.percentile(v, 92)) & (v >= np.percentile(v, 5)); c = c[k] if k.sum() > 20 else c
    return '#%02x%02x%02x' % tuple(int(x) for x in np.median(c, 0))
BOX = json.load(open(R / 'config/tableview-back-boxes-nov07.json'))
OUT = json.load(open(R / 'config/tableview-back-colors.json'))
added, kept, rows = [], [], []
for slug, v in BOX['sets'].items():
    if slug not in SETS: print('not in this build:', slug); continue
    if slug in OUT and 'nov07' not in (OUT[slug].get('src') or ''): kept.append(slug); continue
    im = photo(slug, v.get('img')); w, hh_ = im.size; x0, y0, x1, y1 = v['box']
    crop = im.crop((int(x0 * w), int(y0 * hh_), int(x1 * w), int(y1 * hh_)))
    where = v.get('img') or 'FYM tile photo'
    e = dict(back=med(crop), type='solid', src=f'back photo measured (nov07 box inside one back, {where}; checked by eye as back | wall swatch)')
    if v['kind'] in ('pattern', 'sprite'):
        pp = R / f"assets/table-view/backs/{slug}{'-sprite' if v['kind'] == 'sprite' else ''}.webp"
        c2 = crop.copy(); c2.thumbnail((160, 160) if v['kind'] == 'pattern' else (140, 200)); c2.save(pp, 'WEBP', quality=82)
        if v['kind'] == 'pattern': e.update(type='pattern', patch=str(pp.relative_to(R)))
        else: e.update(sprite=str(pp.relative_to(R)))
    OUT[slug] = e; added.append(slug); rows.append((slug, im, (x0, y0, x1, y1), crop, e, v['kind']))
OUT['_about'] = OUT.get('_about', '').split(' Nov 7:')[0] + ' Nov 7: + sets from builder/table_view/back_colors_nov07.py (config/tableview-back-boxes-nov07.json; its _needs_eye sets stay without walls until Tiffany confirms).'
json.dump(OUT, open(R / 'config/tableview-back-colors.json', 'w'), indent=1, ensure_ascii=False)
print(f'nov07: added/refreshed {len(added)}, kept nov01 {len(kept)}, total with walls {sum(1 for k in OUT if not k.startswith("_"))}, needs her eye {len(BOX["_needs_eye"])}')
if '--sheet' in sys.argv:
    out = sys.argv[sys.argv.index('--sheet') + 1]; P, cols = 220, 5; CW = P * 2 + 12
    def shade(hx, f): return tuple(max(0, min(255, int(int(hx[j:j + 2], 16) * f))) for j in (1, 3, 5))
    def wall(e, crop, kind, n=5, W=36):
        H = int(W * 1.45); im = Image.new('RGB', (n * W + (n + 1) * 3, H + 8), (228, 220, 210)); d = ImageDraw.Draw(im); rnd = random.Random(7)
        for j in range(n):
            x = 3 + j * (W + 3)
            if kind == 'sprite': t = crop.resize((W, H))
            elif kind == 'pattern':
                pw, ph = crop.size; sw, sh = max(1, int(pw * .6)), max(1, int(ph * .6)); ox = rnd.randint(0, pw - sw); oy = rnd.randint(0, ph - sh); t = crop.crop((ox, oy, ox + sw, oy + sh)).resize((W, H))
            else:
                t = Image.new('RGB', (W, H)); td = ImageDraw.Draw(t)
                for yy in range(H): td.line([(0, yy), (W, yy)], fill=shade(e['back'], 1.14 - .30 * yy / H))
            im.paste(t, (x, 4)); d.rectangle([x, 4, x + W - 1, 4 + H - 1], outline=(70, 60, 60))
        return im
    rws = (len(rows) + cols - 1) // cols; sh = Image.new('RGB', (cols * CW, rws * (P + 34)), 'white'); d = ImageDraw.Draw(sh)
    for j, (slug, im, b, crop, e, kind) in enumerate(rows):
        t = im.copy(); t.thumbnail((P, P)); s = t.size[0] / im.size[0]; g = ImageDraw.Draw(t); w, hh_ = im.size
        g.rectangle([b[0] * w * s, b[1] * hh_ * s, b[2] * w * s, b[3] * hh_ * s], outline=(255, 0, 255), width=3)
        x = (j % cols) * CW; y = (j // cols) * (P + 34); sh.paste(t, (x, y))
        c2 = crop.copy(); c2.thumbnail((100, 100)); sh.paste(c2, (x + P + 6, y))
        wl = wall(e, crop, kind); wl.thumbnail((P - 6, 110)); sh.paste(wl, (x + P + 6, y + 106))
        d.rectangle([x + P + 6, y + 178, x + P + 70, y + 200], fill=e['back'])
        d.text((x + 2, y + P + 2), SETS[slug]['name'][:44] + ' · ' + SETS[slug]['maker'][:20], fill='black'); d.text((x + 2, y + P + 16), f"{e['back']} {kind}", fill='black')
    sh.save(out, quality=84); print('sheet', out, sh.size)
