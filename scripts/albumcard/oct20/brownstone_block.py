"""Full Brownstone Bloom album code block. Template = the Oct 18 staged block
(site/livepatch/oct18c/brownstone-bloom.html, same structure/CSS/lightbox as the Papaya block); figures rebuilt in her order
with Match the tiles / Match the mat captions. Usage: brownstone_block.py <sha> [card folder, default brownstone-bloom-oct31]
Oct 31: reads assets/cards/<folder>/manifest.json (40 cards); shop links = catalog, else the previous block's link for the
same card file, else the manifest's round-2 'shop'. Partner list topped up from config/fym-mats-snapshot.json (pa=true),
since the catalog partner list predates Amanda Toppe / Mahjong Register. Mahjong Row & Co. spelled one way."""
import json, sys, re, os
import common as C, album_block as A
SHA = sys.argv[1]; FOLDER = sys.argv[2] if len(sys.argv) > 2 else 'brownstone-bloom-oct31'
m = json.load(open(C.R + f'assets/cards/{FOLDER}/manifest.json'))
for v in json.load(open(C.R + 'config/fym-mats-snapshot.json'))['mats'].values():
    if v.get('pa') and not v.get('nc'): C.PARTNERS.add(v['bn'])
OUTF = C.R + 'site/livepatch/brownstone-bloom-oct20/brownstone-bloom-codeblock.html'
_old = open(OUTF).read()
ST = {}
for _c in m['cards']:
    _f = re.search(re.escape(_c['file']) + r'.{0,6000}?<a class="mm3-btn" href="(http[^"]+)"', _old, re.S)
    if _f: ST[_c['mat']] = _f.group(1).replace('&amp;', '&')
cards = []
for c in m['cards']:
    b = 'Mahjong Row & Co.' if c['brand'].rstrip('.') == 'Mahjong Row & Co' else c['brand']
    url = C.mat_url(c['mat'], b) or C.mat_url(c['mat'], c['brand']) or ST.get(c['mat']) or c.get('shop')
    cards.append(dict(c, brand=b, url=url))
tpl = open(C.R + 'site/livepatch/oct18c/brownstone-bloom.html').read()
out = A.build(tpl, cards, 'Brownstone Bloom', 'Anders Ruff Brownstone Bloom', SHA, FOLDER)
# Colour card first (doc 86b / NEW-ALBUM-CHECKLIST): same Tile Edit markup as the Papaya block, right before the matches.
CC = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/assets/colorcards/brownstone-bloom/00-brownstone-bloom-mahjong-tiles-'
GUIDE = ('<section class="mm3-guides"><h2>Colors &amp; racks</h2><div class="mm3-gg"><figure class="mm3-g"><picture>'
         f'<source media="(max-width: 640px)" srcset="{CC}color-guide-mobile.jpg"><img src="{CC}tile-edit-moodboard.jpg" data-lb="" '
         'alt="Anders Ruff Brownstone Bloom mahjong tiles color card: ivory backs with lavender butterflies, wine, olive and dusty rose faces, rack and mat matches" loading="lazy">'
         '</picture><figcaption><strong>The Tile Edit</strong><p>Ivory tiles with lavender butterflies on the back and wine, olive and dusty rose faces. '
         'Middle &amp; Main Hawksbill Heritage Tortoise and Bam Bird Boutique Olive racks pick up her browns and greens.</p></figcaption></figure>'
         '<style>.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]){grid-column:1/-1}.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]) figcaption{max-width:860px;margin:0 auto;padding:20px 26px 12px;font-size:16px}</style>'
         '</div></section>')
# Oct 31 night: OMM no longer sells these 3 mats (product pages 404, not in ohmymahjong.com/products.json). Her cards stay in
# her order; only the dead Shop button is left off. Flagged on DESK / MATCH-INBOX for her keep-or-drop call.
GONE = {'Dapper', 'Vanderbilt', 'Cognac'}
for g in GONE:
    out, k = re.subn(r'<a class="mm3-btn" href="[^"]*"[^>]*>Shop the ' + re.escape(g) + r' Mat</a>', '', out)
    assert k == 1, g
_M = '<section><h2>My Brownstone Bloom matches</h2>'
assert out.count(_M) == 1 and 'mm3-guides' not in out
out = out.replace(_M, GUIDE + _M).replace('Mahjong Row &amp; Co..', 'Mahjong Row &amp; Co.').replace('Mahjong Row & Co..', 'Mahjong Row & Co.')
open(OUTF, 'w').write(out)
print(len(re.findall(r'<figure class="mm3-c', out)), 'figures; missing links:', C.MISSING_LINKS)
