"""Top-5 countdown reel from an album's first five cards.
Usage: python3 build.py <album-slug> <tile name> <title color> <heart1 mat color> <heart2 tile color> <out.mp4>"""
import json, sys, subprocess, base64, os
R = '/home/claude/mahjmatchmaker-data/'
slug, tile, col, h1, h2, out = sys.argv[1:7]
a = {x['slug']: x for x in json.load(open(R + 'work/albums.json'))}[slug]
cards = [c for c in a['cards'] if not c.get('retired')][:5]
wd = f'/tmp/cd_{slug}'; os.makedirs(wd, exist_ok=True)
C = []
for i, c in enumerate(cards):
    f = f'{wd}/c{i}.jpg'
    if not os.path.exists(f): subprocess.run(['curl', '-s', '-o', f, c['img'] + '?format=1500w'], check=True)
    C.append({'rank': i + 1, 'mat': c['mat'], 'brand': c['brand'], 'img': 'data:image/jpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode()})
C = C[::-1]  # count down 5 -> 1
wm = 'data:image/png;base64,' + base64.b64encode(open(R + 'assets/brand/mahjmatchmaker-wordmark.png', 'rb').read()).decode()
h = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'countdown.html')).read()
h = (h.replace('__CARDS__', json.dumps(C)).replace('__COL__', col).replace('__H1__', h1).replace('__H2__', h2)
     .replace('__TILE__', tile.upper()).replace('__N__', str(len(a['cards']))).replace('__WORDMARK__', wm))
open(f'{wd}/r.html', 'w').write(h)
dur = 2.4 + 3.6 * len(C) + 3.6
json.dump({'dur': dur}, open(f'{wd}/meta.json', 'w'))
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
subprocess.run(['node', R + 'scripts/reel/swipe/render.js', f'{wd}/r.html', f'{wd}/meta.json', out, '30'], check=True, env={**os.environ, 'NODE_PATH': NP})
print(out, dur)
