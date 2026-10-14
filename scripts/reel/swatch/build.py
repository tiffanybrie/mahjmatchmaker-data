"""Color Story (paint chip) reel: colors pulled from the tiles, each revealed with the album card that brings it out.
Usage: python3 build.py <album-slug> <tile name> <title color> <heart1> <heart2> <picks.json> <pile.jpg> <out.mp4>
picks.json: [{"mat": "<exact album mat name>", "chip": "Walnut", "hex": "#8a4a26"}, ...]"""
import json, sys, subprocess, base64, os
R = '/home/claude/mahjmatchmaker-data/'
slug, tile, col, h1, h2, picks, pile, out = sys.argv[1:9]
a = {x['slug']: x for x in json.load(open(R + 'work/albums.json'))}[slug]
by = {c['mat']: c for c in a['cards'] if not c.get('retired')}
wd = f'/tmp/sw_{slug}'; os.makedirs(wd, exist_ok=True)
b64 = lambda f, m: f'data:{m};base64,' + base64.b64encode(open(f, 'rb').read()).decode()
C = []
for i, p in enumerate(json.load(open(picks))):
    c = by[p['mat']]; f = f'{wd}/' + ''.join(ch if ch.isalnum() else '-' for ch in p['mat']) + '.jpg'
    if not os.path.exists(f): subprocess.run(['curl', '-s', '-o', f, c['img'] + '?format=1500w'], check=True)
    C.append({**p, 'brand': c['brand'], 'img': b64(f, 'image/jpeg')})
h = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swatch.html')).read()
for k, v in {'__CARDS__': json.dumps(C), '__COL__': col, '__H1__': h1, '__H2__': h2, '__TILE__': tile.upper(), '__TILE_T__': tile,
             '__N__': str(len(a['cards'])), '__NC__': {3:'Three',4:'Four',5:'Five'}.get(len(C), str(len(C))),
             '__PILE__': b64(pile, 'image/jpeg'), '__WORDMARK__': b64(R + 'assets/brand/mahjmatchmaker-wordmark.png', 'image/png')}.items():
    h = h.replace(k, v)
open(f'{wd}/r.html', 'w').write(h)
dur = 3.2 + 3.8 * len(C) + 3.6
json.dump({'dur': dur}, open(f'{wd}/meta.json', 'w'))
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
if os.environ.get("NORENDER")!="1": subprocess.run(["node", R + "scripts/reel/swipe/render.js", f"{wd}/r.html", f"{wd}/meta.json", out, "30"], check=True, env={**os.environ, "NODE_PATH": NP})
print(out, dur)
