"""Live card sharpness + tile-fill scan (Tiffany Nov 9 1:39-1:43am: blurry Dec 1994 + Festive Plaid card; Virora tile insets in a
white box). Scans every card image on /holiday-mahjong-matches and every *-mahjong-tile-matches page in the sitemap:
  - mat area soft/pixelated (scripts/checks/card_sharpness.py: e2 >= 0.6 and r < 0.2), unless listed in config/card-sharpness-ok.json
  - tile inset (card2 #tile, x667-1080 y592-1106) with a near-white border band > 5% (the white box around shrunk tiles:
    Tinselle 3x3 was 20%). Live tolerance 5% because a scattered pile shot on white (Dear Santa, ~3.5%) is a photo, not a box;
    new builds are held to 3% by tile_fill_check in gen2.py. Only card2-layout cards (1080x1350 or 750x938) are measured.
Images pinned to this repo (jsDelivr @sha) are read from git (git show sha:path); others are downloaded once into
/tmp/card_sharpness_cache. Writes docs/status/card-sharpness.json; front_door.py shows the FAIL lines on every message.
Usage: python3 scripts/checks/card_sharpness_check.py [slug ...]   (exit 1 on any FAIL)
Runs in the morning HQ cleanup (docs/HQ-CLEANUP.md) and after every album/holiday paste."""
import re, sys, os, io, json, random, subprocess, hashlib, datetime
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/checks')
import card_sharpness as CS
SITE = 'https://www.mahjmatchmaker.com/'
CACHE = '/tmp/card_sharpness_cache/'
def get(u): return subprocess.run(['curl', '-sL', '--max-time', '60', f'{u}?nc={random.randint(1, 10**9)}'], capture_output=True, text=True).stdout
def load(u):
    m = re.match(r'https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@([0-9a-f]+)/(.+)$', u)
    if m:
        b = subprocess.run(['git', '-C', R, 'show', f'{m.group(1)}:{m.group(2)}'], capture_output=True).stdout
        if b: return Image.open(io.BytesIO(b))
    os.makedirs(CACHE, exist_ok=True)
    uu = ('https:' + u) if u.startswith('//') else u
    if 'squarespace-cdn' in uu and 'format=' not in uu: uu += ('&' if '?' in uu else '?') + 'format=1500w'
    f = CACHE + hashlib.md5(uu.encode()).hexdigest()
    if not os.path.exists(f): subprocess.run(['curl', '-sL', '--max-time', '60', uu, '-o', f])
    return Image.open(f)
def tile_band(im):
    im = im.convert('RGB').resize((1080, 1350)) if im.size != (1080, 1350) else im.convert('RGB')
    a = np.asarray(im.crop((667, 592, 1080, 1106)), dtype=np.int16)
    wht = (a.min(axis=2) >= 232) & ((a.max(axis=2) - a.min(axis=2)) <= 14)
    def run(fl):
        n = 0
        for f in fl:
            if not f: break
            n += 1
        return n
    rows = wht.mean(axis=1) >= 0.97; cols = wht.mean(axis=0) >= 0.97
    return max(run(rows) / rows.size, run(cols) / cols.size)
def cards(t):
    for m in re.finditer(r'<figure class="mm3-c[^"]*">(.*?)</figure>', t, re.S):
        im = re.search(r'<img src="([^"]+)"', m.group(1)); h = re.search(r'<h3>(.*?)</h3>', m.group(1), re.S)
        if im: yield im.group(1), re.sub('<[^>]+>', '', h.group(1)) if h else ''
def check(page, u, h3, ok):
    try: im = load(u)
    except Exception as e: return (page, h3, u, f'unreadable ({e})')
    if im.size not in ((1080, 1350), (750, 938)): return None
    fn = u.split('/')[-1].split('?')[0]
    out = []
    m = CS.measure(im)
    if CS.blurry(m) and fn not in ok: out.append(f'blurry mat r={m["r"]} e2={m["e2"]}')
    b = tile_band(im)
    if b > 0.05 and fn not in ok: out.append(f'white band around tile inset {b*100:.0f}%')
    return (page, h3, u, '; '.join(out)) if out else None
def main():
    pages = sys.argv[1:]
    if not pages:
        sm = get(SITE + 'sitemap.xml')
        pages = ['holiday-mahjong-matches'] + sorted(set(re.findall(r'mahjmatchmaker\.com/([a-z0-9-]+-mahjong-tile-matches)<', sm)))
    ok = CS.ok_list(); jobs = []
    for p in pages:
        for u, h3 in cards(get(SITE + p)): jobs.append((p, u, h3))
    with ThreadPoolExecutor(8) as ex: res = [r for r in ex.map(lambda j: check(j[0], j[1], j[2], ok), jobs) if r]
    os.makedirs(R + 'docs/status', exist_ok=True)
    json.dump({'at': datetime.datetime.now().isoformat(timespec='minutes'), 'cards': len(jobs), 'pages': len(pages),
               'fails': [{'page': a, 'card': b, 'img': c, 'why': d} for a, b, c, d in res]}, open(R + 'docs/status/card-sharpness.json', 'w'), indent=1, ensure_ascii=False)
    print(f'CARD SHARPNESS {"FAIL" if res else "PASS"}: {len(jobs)} cards on {len(pages)} pages, {len(res)} failing')
    for a, b, c, d in res: print(f'  FAIL {a} | {b} | {d} | {c.split("/")[-1][:90]}')
    sys.exit(1 if res else 0)
if __name__ == '__main__': main()
