"""Swap list for the 4 Osler cards re-rendered without the bamboo background (assets/cards/bamboo-v1 @ PIN).
Each entry: exact old <img src> and old rack caption div on the live Osler block -> new src + caption that matches the new card."""
import json, re, html, sys, glob
R = '/home/claude/mahjmatchmaker-data/'
PIN = sys.argv[1]; LIVE = sys.argv[2]
e = lambda s: html.escape(s, quote=True)
U = {n: u for n, u in json.load(open(R + 'data.json'))['R']}
for f in glob.glob(R + 'site/livepatch/codefooter/*.html'):
    for u, n in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', open(f).read()):
        n = html.unescape(n).strip()
        if n.startswith(('Bird & Bamboo', 'Middle & Main', 'Bam Bird')): U.setdefault(n, html.unescape(u))
U['Middle & Main Hawksbill Heritage Tortoise'] = 'https://www.middleandmainmahjong.com/products/hawksbill-heritage-mahjong-rack-and-pusher-set-of-4?sca_ref=10574197.BKiJ48vXYfYfD31E'
def link(n):
    u = U.get(n)
    return f'<a href="{e(u)}" target="_blank" rel="sponsored noopener">{e(n)}</a>' if u else e(n)
spec = json.load(open(R + 'scripts/albumcard/specs/bamboo_oct18/osler_spec_nomat.json'))
s = open(LIVE).read(); out = []
for c in spec['cards']:
    f = c['file']; i = s.find(f)
    a = s.rfind('<figure', 0, i); b = s.find('</figure>', i) + 9; fig = s[a:b]
    old_src = re.search(r'<img src="([^"]+)"', fig).group(1)
    old_rk = re.search(r'<div class="mm3-rk"[^>]*>.*?</div>', fig, re.S).group(0)
    tiles = ' · '.join(link(n) for n in c['racks'] if n != 'Tigre de Tartán Oxblood Scallop')
    mat = ' · '.join(link(n) for n in c['mat_racks'])
    new_rk = f'<div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">Match the tiles: {tiles}<br>Match the mat: {mat}</div>'
    new_src = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{PIN}/assets/cards/bamboo-v1/{f}'
    out.append({'title': c['title'], 'old_src': old_src, 'new_src': new_src, 'old_caption': old_rk, 'new_caption': new_rk,
                'missing_links': [n for n in c['racks'] + c['mat_racks'] if n not in U and n != 'Tigre de Tartán Oxblood Scallop']})
json.dump({'page': '/osler-mahjong-tile-matches', 'swaps': out}, open(R + 'site/livepatch/bamboo/osler.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps([[o['title'], o['missing_links']] for o in out]))
