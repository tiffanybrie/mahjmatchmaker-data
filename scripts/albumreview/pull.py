"""Album Playbook step 4: THE candidate pull, committed (Nov 8 2:35pm, after Tiffany caught Britt Mills Scarlett + Flora
missing from Deco (Lagoon)).

Why it exists: the Nov 7 Deco pull was a scratch script. It scored the FYM catalog, then built the by-eye contact sheets
from Mat Gallery images only and SILENTLY dropped every pool mat with no gallery image (13 of them, incl. Britt Mills
Scarlett Neoprene, scored into both the Lagoon and Mulberry pools). Its score was also tonal: share of pixels near the
set's palette, which the back colour dominates, so a berry mat for teal backs (Scarlett, Flora) ranked 150-190th.

This pull:
 1. Pool = every visible FYM mat (config/fym-mats-snapshot.json) + the record's pool.new_candidates (catalog_refresh).
 2. Photos = the FYM photo itself (scripts/albumreview/fym_images.py, read from git), never a gallery-only lookup.
    A mat with no photo is a HARD FAIL listed by name (nothing is ever dropped silently).
 3. Two scores per mat, from config/colorcards.json sets.<set>:
      tonal = share of mat pixels near the BACK colour (plus faces within dE 25 of it)
      comp  = share near the CONTRAST face colours (faces > dE 25 from the back: e.g. mulberry, rose, gold for Lagoon)
      both  = min(tonal, comp) * 2 + 0.5 * max(tonal, comp)  (a mat carrying both sides of the set wins)
    The by-eye shortlist = top N by tonal UNION top N by comp UNION top N by both, so the complementary side is always seen.
 4. Misses = shortlisted mats that are in neither the album spec nor its Left out list (incl. More from <brand>).
Writes <out>/pull.json (rankings + misses) and contact sheets <out>/miss-*.jpg (mat + the album's tile inset, match-card
style) and records pool.pulled_at / pulled_by / no_photo / shortlist in the album record (--record).

Usage: python3 scripts/albumreview/pull.py <set> <outdir> [--top 60] [--record]"""
import json, os, re, sys, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumreview')
from fym_images import image_bytes
a = sys.argv[1:]
SET, OUT = a[0], a[1]
TOP = int(a[a.index('--top') + 1]) if '--top' in a else 60
os.makedirs(OUT, exist_ok=True)
J = lambda p: json.load(open(R + p))
rec = J(f'config/album-records/{SET}.json')
cc = J('config/colorcards.json')['sets'][SET]
snap = J('config/fym-mats-snapshot.json')
spec = J(rec['spec'])
lo = J(rec['leftout']['file'])[rec['leftout']['key']]


def lab(rgb):
    c = rgb / 255.0; c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.9505, 1.0, 1.089]); f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def hx(h): return lab(np.array([[int(h[1 + i:3 + i], 16) for i in (0, 2, 4)]], float))[0]


BACK = hx(cc['backs'][0][1])
FACES = [(n, hx(h)) for n, h in cc['faces']]
hue = lambda l: np.degrees(np.arctan2(l[2], l[1])) % 360
def hdiff(l):
    d = abs(hue(l) - hue(BACK)); return min(d, 360 - d)
# Tonal side = the back + faces within 30 deg of its hue; contrast side = faces 90+ deg away (Lagoon: mulberry, rose, gold).
# A record may name its contrast colours (record pull.contrast), e.g. Indigo's berry at 67 deg.
_force = set((rec.get('pull') or {}).get('contrast') or [])
TONAL = [('BACK', BACK)] + [(n, l) for n, l in FACES if hdiff(l) <= 30 and n not in _force]
COMP = [(n, l) for n, l in FACES if (hdiff(l) >= 90 or n in _force)]


def score(im):
    im = im.convert('RGB'); im.thumbnail((96, 96))
    p = np.asarray(im).reshape(-1, 3).astype(float)
    p = p[p.min(1) < 240]  # white background out
    if len(p) < 50: return None
    L = lab(p); chroma = np.hypot(L[:, 1], L[:, 2])
    d = lambda pal: np.min(np.stack([np.linalg.norm(L - c, axis=1) for _, c in pal]), 0) if pal else np.full(len(L), 999.)
    dt = d(TONAL)
    col = chroma > 12  # greys/creams never count as a palette hit
    t = float(np.mean((dt < 18) & col))
    # Contrast side by HUE BAND (+-25 deg, chroma > 25, any lightness): berry reads as berry whether it is plum or hot pink.
    # The first contrast face on the colour card (most tiles) counts fully, the others half (rose/gold also catch tan leather).
    ph = np.degrees(np.arctan2(L[:, 2], L[:, 1])) % 360
    per, c = {}, 0.0
    for i, (n, l) in enumerate(COMP):
        dh = np.abs(ph - hue(l)); dh = np.minimum(dh, 360 - dh)
        sh = float(np.mean((dh < 25) & (chroma > 25) & (dt >= 18))); per[n] = round(sh, 3); c += sh * (1 if i == 0 else .5)
    c = min(c, 1.0)
    return {'tonal': round(t, 3), 'comp': round(c, 3), 'both': round(min(t, c) * 2 + .5 * max(t, c), 3), 'comp_by': per}


# ---- pool
pool = {}
for k, m in snap['mats'].items():
    if m.get('hid'): continue
    pool[k] = {'key': k, 'name': m['n'], 'brand': m['bn'], 'hol': bool(m.get('hol')), 'f': m['f'], 'src': 'fym'}
for c in (rec.get('pool') or {}).get('new_candidates', []):
    k = 'new:' + c['brand'] + '|' + c['name']
    pool[k] = {'key': k, 'name': c['name'], 'brand': c['brand'], 'hol': bool(c.get('holiday_guess')), 'img': c['img'], 'src': 'new'}
nophoto, imgs, missing_fym = [], {}, []
def _thumb(im):
    im = im.convert('RGB'); im.thumbnail((260, 260)); return im
fk = [k for k, p in pool.items() if p.get('f')]
for i in range(0, len(fk), 150):  # batches: decoded photos are kept only as 260px thumbnails (memory)
    fb = image_bytes([pool[k]['f'] for k in fk[i:i + 150]])
    for k in fk[i:i + 150]:
        try: imgs[k] = _thumb(Image.open(io.BytesIO(fb[pool[k]['f']])))
        except Exception: missing_fym.append(k)
    del fb
GAL = os.listdir(R + 'assets/mats/gallery')
sl = lambda x: re.sub(r'[^a-z0-9]+', '-', x.lower().replace('&', '').replace("'", '')).strip('-')
gal_fallback = []
for k in missing_fym:  # FYM photo not found in the packed chunks: the Mat Gallery copy of the same mat, logged
    p = pool[k]; hit = [g for g in GAL if g.split('--', 1)[-1].rsplit('.', 1)[0] == sl(p['name']) and sl(p['brand']).replace('-', '')[:6] in g.replace('-', '')]
    try: imgs[k] = _thumb(Image.open(R + 'assets/mats/gallery/' + hit[0])); gal_fallback.append(f"{p['brand']} · {p['name']} ({p['f']})")
    except Exception: nophoto.append(f"{p['brand']} · {p['name']}")
for k, p in pool.items():
    if p.get('f'): continue
    try: imgs[k] = _thumb(Image.open(R + p['img']))
    except Exception: nophoto.append(f"{p['brand']} · {p['name']}")
if nophoto:
    sys.exit(f'PULL FAIL {SET}: {len(nophoto)} pool mats have no photo (nothing is dropped silently): ' + '; '.join(nophoto[:20]))
for k, p in pool.items():
    s = score(imgs[k])
    if s is None: sys.exit(f"PULL FAIL {SET}: {p['brand']} · {p['name']} photo is blank after the white-background cut")
    p.update(s)

# ---- shortlist + misses
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower().replace('neoprene', '').replace('leatherette', ''))
have = {(norm(m['name']), norm(m['brand'])) for m in spec['mats']} | {(norm(m['name']), norm(m['brand'])) for m in lo}
short = {}
for kind in ('tonal', 'comp', 'both'):
    for p in sorted(pool.values(), key=lambda p: -p[kind])[:TOP]: short.setdefault(p['key'], set()).add(kind)
misses = []
for k, kinds in short.items():
    p = pool[k]
    if (norm(p['name']), norm(p['brand'])) in have: continue
    misses.append({**{x: p[x] for x in ('key', 'name', 'brand', 'hol', 'tonal', 'comp', 'both', 'comp_by', 'src')}, 'by': sorted(kinds)})
misses.sort(key=lambda m: -m['both'])
rank = {kind: {p['key']: i + 1 for i, p in enumerate(sorted(pool.values(), key=lambda p: -p[kind]))} for kind in ('tonal', 'comp', 'both')}
res = {'set': SET, 'pool': len(pool), 'no_photo': 0, 'gallery_fallback': gal_fallback, 'tonal_colours': [n for n, _ in TONAL], 'comp_colours': [n for n, _ in COMP],
       'shortlist': len(short), 'misses': misses, 'rank': {k: {kind: rank[kind][k] for kind in rank} for k in short}}
json.dump(res, open(os.path.join(OUT, 'pull.json'), 'w'), indent=1, ensure_ascii=False)

# ---- contact sheets of the misses: mat full + the album tile inset bottom-right (match-card style)
ins = Image.open(R + rec['tile_photo']['inset']).convert('RGB'); ins.thumbnail((90, 90))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
T, C, RW = 260, 6, 5
for si in range(0, len(misses), C * RW):
    sh = Image.new('RGB', (C * T, RW * (T + 36)), 'white'); d = ImageDraw.Draw(sh)
    for j, m in enumerate(misses[si:si + C * RW]):
        x, y = (j % C) * T, (j // C) * (T + 36)
        im = imgs[m['key']].convert('RGB'); im.thumbnail((T - 8, T - 8)); sh.paste(im, (x + 4, y + 4))
        sh.paste(ins, (x + T - 96, y + T - 96))
        d.text((x + 4, y + T - 2), f"{si + j} {m['name'][:30]}", fill='black', font=F)
        d.text((x + 4, y + T + 14), f"{m['brand'][:20]} c{m['comp']:.2f} t{m['tonal']:.2f}{' HOL' if m['hol'] else ''}", fill='gray', font=F)
    sh.save(os.path.join(OUT, f'miss-{si // (C * RW):02d}.jpg'), quality=84)
print(f"PULL {SET}: pool {len(pool)} (0 without a photo; {len(gal_fallback)} from the Mat Gallery copy: {gal_fallback}), tonal {[n for n, _ in TONAL]}, contrast {[n for n, _ in COMP]}; "
      f"shortlist {len(short)}; {len(misses)} not in the album or Left out -> {OUT}/pull.json + miss-*.jpg")
if '--record' in a:
    import datetime
    rp = R + f'config/album-records/{SET}.json'; r2 = json.load(open(rp))
    r2['pool'].update({'pulled_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'pulled_by': 'scripts/albumreview/pull.py',
                       'no_photo': 0, 'shortlist': len(short), 'contrast_colours': res['comp_colours'], 'size_fym': sum(1 for p in pool.values() if p['src'] == 'fym')})
    json.dump(r2, open(rp, 'w'), indent=1, ensure_ascii=False)
