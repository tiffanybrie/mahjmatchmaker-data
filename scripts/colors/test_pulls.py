"""Test pulls for doc 76/77 rules -> site/colortagger/pull-test.jpg (top 10 per set + layer picks) and printed counts."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matcolors as M
from PIL import Image, ImageDraw, ImageFont
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SCR = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
D = json.load(open(SCR + 'matgal/D.json'))['mats']; man = json.load(open(SCR + 'matgal/manifest.json'))
img_of = {v: k for k, v in man.items()}
GATE = ('mahjong studios', 'splash of color', 'mahjong by si')  # doc 55 match-pool brand gate
keys = [k for k in img_of if k in D and not D[k].get('hol')
        and not any(g in (D[k].get('bn') or '').lower() for g in GATE)]
SETS = ['Papaya Spritz', 'Sorbet', 'Dandy', 'La Fete', 'Drake', 'Sierra', 'Lagoon']
try: F = ImageFont.truetype(os.path.join(R, 'assets/fonts/bitter-latin-700-normal.woff2'), 15)
except Exception: F = ImageFont.load_default()
W, TH = 120, 120; rows = []; rep = {}
for sn in SETS:
    got = M.pull(sn, keys); lp = M.layer_picks(sn, keys, exclude=got)
    names = [D[k]['n'] for k in got]
    multi = sum(1 for k in got if M.is_multi(M.get(k), k))
    rep[sn] = {'count': len(got), 'multis': multi, 'top10': names[:10], 'layer_picks': [D[x['key']]['n'] for x in lp],
               'spring_fling_rank': next((i + 1 for i, k in enumerate(got) if 'spring fling' in D[k]['n'].lower()), None),
               'greenly_rank': next((i + 1 for i, k in enumerate(got) if 'greenly' in D[k]['n'].lower()), None)}
    rows.append((sn, got[:10], [x['key'] for x in lp][:4]))
sheet = Image.new('RGB', (150 + 14 * (W + 6), len(rows) * (TH + 44) + 10), 'white'); d = ImageDraw.Draw(sheet)
y = 6
for sn, top, lp in rows:
    d.text((6, y + TH // 2), sn, fill=(20, 48, 95), font=F)
    for i, k in enumerate(top + lp):
        x = 150 + i * (W + 6) + (20 if i >= len(top) else 0)
        try:
            t = Image.open(os.path.join(R, 'assets/mats/gallery', img_of[k] + '.webp')).convert('RGB'); t.thumbnail((W, TH)); sheet.paste(t, (x, y))
        except Exception: pass
        d.text((x, y + TH + 2), D[k]['n'][:16], fill=(200, 40, 100) if i >= len(top) else (60, 60, 60), font=ImageFont.load_default())
    y += TH + 44
sheet.save(os.path.join(R, 'site/colortagger/pull-test.jpg'), quality=82)
json.dump(rep, open(os.path.join(R, 'site/colortagger/pull-test.json'), 'w'), indent=1)
for k, v in rep.items(): print(k, v['count'], 'multis', v['multis'], 'SF', v['spring_fling_rank'], 'Greenly', v['greenly_rank'], '|', ', '.join(v['top10'][:6]), '| layer:', ', '.join(v['layer_picks'][:4]))
print('pool', len(keys))
