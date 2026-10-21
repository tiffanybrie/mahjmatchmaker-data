"""Full Brownstone Bloom album code block from the Oct 20 cards. Template = the Oct 18 staged block
(site/livepatch/oct18c/brownstone-bloom.html, same structure/CSS/lightbox as the Papaya block); figures rebuilt in her order
with Match the tiles / Match the mat captions. Usage: brownstone_block.py <sha>"""
import json, sys, re
import common as C, album_block as A
SHA = sys.argv[1]
m = json.load(open(C.R + 'assets/cards/brownstone-bloom-oct20/manifest.json'))
_STP = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/owedwork/bbhd/staged_urls.json'
import os
ST = json.load(open(_STP)) if os.path.exists(_STP) else {}  # Oct 21: scratch file is gone; fall back to the links in the last staged block
if not ST:
    _old = open(C.R + 'site/livepatch/brownstone-bloom-oct20/brownstone-bloom-codeblock.html').read()
    for _c in m['cards']:
        _f = re.search(re.escape(_c['file']) + r'.{0,6000}?<a class="mm3-btn" href="(http[^"]+)"', _old, re.S)
        if _f: ST[_c['mat']] = {'url': _f.group(1)}
BR = {'Mahjong Row & Co': 'Mahjong Row & Co.', 'Mac + Miller Mahjong': 'Mac + Miller Mahjong'}
cards = []
for c in m['cards']:
    url = C.mat_url(c['mat'], c['brand']) or C.mat_url(c['mat'], BR.get(c['brand'], c['brand'])) or ST.get(c['mat'], {}).get('url')
    b = c['brand']
    if b not in C.BRANDPG and ST.get(c['mat'], {}).get('brandpage'): C.BRANDPG[b] = ST[c['mat']]['brandpage']
    if b == 'Mahjong Row & Co' and 'Mahjong Row & Co.' in C.PARTNERS: C.PARTNERS.add(b)
    cards.append(dict(c, url=url))
tpl = open(C.R + 'site/livepatch/oct18c/brownstone-bloom.html').read()
out = A.build(tpl, cards, 'Brownstone Bloom', 'Anders Ruff Brownstone Bloom', SHA, 'brownstone-bloom-oct20')
open(C.R + 'site/livepatch/brownstone-bloom-oct20/brownstone-bloom-codeblock.html', 'w').write(out)
print(len(re.findall(r'<figure class="mm3-c', out)), 'figures; missing links:', C.MISSING_LINKS)
