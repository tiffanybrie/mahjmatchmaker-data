"""Rose Ceremony reel from an album's first five cards.
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
C = C[::-1]  # 5th pick first, top pick gets the final rose
for i, c in enumerate(C):
    c['q'] = f'Rose #{i+1}' if i < len(C) - 1 else 'The final rose'
    c['last'] = i == len(C) - 1
ROSE = '<path d="M50 60 C48 85 52 105 50 128" stroke="#2f7a3e" stroke-width="5" fill="none"/><path d="M50 92 C35 80 22 84 18 92 C30 98 42 98 50 92Z" fill="#3f8f4e"/><path d="M51 102 C64 92 78 95 82 102 C70 108 58 108 51 102Z" fill="#3f8f4e"/><path d="M50 8 C30 8 20 24 22 40 C24 56 38 64 50 64 C62 64 76 56 78 40 C80 24 70 8 50 8Z" fill="#c8102e"/><path d="M50 18 C38 20 34 32 38 42 C42 50 58 50 62 42 C66 32 60 20 50 18Z" fill="#9e0b23"/><path d="M44 30 C46 24 56 24 58 32 C56 38 48 40 44 30Z" fill="#e23a52"/><path d="M22 40 C30 52 40 58 50 58 C40 62 26 58 22 40Z" fill="#a50d26"/>'
wm = 'data:image/png;base64,' + base64.b64encode(open(R + 'assets/brand/mahjmatchmaker-wordmark.png', 'rb').read()).decode()
h = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rose.html')).read()
h = (h.replace('__CARDS__', json.dumps(C)).replace('__COL__', col).replace('__H1__', h1).replace('__H2__', h2)
     .replace('__TILE__', tile.upper()).replace('__TILE_T__', tile).replace('__ROSE__', ROSE).replace('__N__', str(len(a['cards']))).replace('__WORDMARK__', wm))
open(f'{wd}/r.html', 'w').write(h)
dur = 2.4 + 3.6 * len(C) + 3.6
json.dump({'dur': dur}, open(f'{wd}/meta.json', 'w'))
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
subprocess.run(['node', R + 'scripts/reel/swipe/render.js', f'{wd}/r.html', f'{wd}/meta.json', out, '30'], check=True, env={**os.environ, 'NODE_PATH': NP})
print(out, dur)
