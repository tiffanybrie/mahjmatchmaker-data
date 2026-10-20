"""Holiday page /holiday-mahjong-matches, section id="december-1994": replacement grid (31 cards, her order) + the
swap list for the 5 cards already live. Usage: dec1994_snippet.py <sha>"""
import json, sys, re
import common as C, album_block as A
SHA = sys.argv[1]
O = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/owedwork/d94/'
L = {x['mat']: x for x in json.load(open(O + 'list.json'))}
m = json.load(open(C.R + 'assets/cards/december-1994-oct20/manifest.json'))
NM = {'Ski Club Red Sweater': 'Ski Club Red Sweater', 'Bam Bird Holiday': 'Bam Bird Holiday', 'Peace Love Holiday': 'Peace Love Holiday'}
figs = []
for c in m['cards']:
    x = L.get(c['mat']) or next((v for k, v in L.items() if k.lower().startswith(c['mat'].lower()[:10])), {})
    img = A.CDN.format(sha=SHA, folder='december-1994-oct20', file=c['file'])
    figs.append(C.figure(c['order'], img, 'December 1994', 'December 1994', c['mat'], c['brand'], m['tile_racks'], c['mat_racks'],
                         url=x.get('url'), cls='mm3-c mm3-hc'))
out = C.R + 'site/livepatch/december-1994-oct20/'
open(out + 'december-1994-holiday-grid.html', 'w').write(
    '<!-- /holiday-mahjong-matches, <section class="mm3-hol" id="december-1994">: replace EVERYTHING inside its <div class="mm3-grid">...</div> with these 31 figures, and change "5 mat matches" to "31 mat matches" in its mm3-sub line -->\n' + '\n'.join(figs) + '\n')
print(len(figs), 'figures; missing:', C.MISSING_LINKS)
