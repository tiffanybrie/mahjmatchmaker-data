"""Measure exact colors: config/mat-palettes.json (pattern-area palette per mat) and measured back/layer/signature colors
added to config/tile-tones.json (doc 76 'Named hues', doc 77 'Exact shades'). Run: python3 scripts/colors/build_palettes.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import palette as P
import families as F
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SCR = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
man = json.load(open(SCR + 'matgal/manifest.json'))  # gallery image name -> mat key
out = {}
for name, key in man.items():
    p = os.path.join(R, 'assets/mats/gallery', name + '.webp')
    if os.path.exists(p): out[key] = {'img': name, 'pal': P.mat_palette(p)}
json.dump({'about': 'Measured pattern-area palette per mat: [hex, weight]; compare with palette.dE (CIEDE2000). doc 77.', 'mats': out},
          open(os.path.join(R, 'config/mat-palettes.json'), 'w'), separators=(',', ':'))
print('mats', len(out))
import numpy as np
def fam(h):
    f, *_ = F.fam_arr(P.hex2rgb(h).reshape(1, 1, 3)); return str(f.ravel()[0])
TP = os.path.join(R, 'config/tile-tones.json'); TT = json.load(open(TP))
# Her words where the photo can't tell (doc 76): Lagoon's signature includes berry.
SIG_ADD = {'lagoon': ('#8e2f5c', 'berry (Tiffany: teal + berry)')}
n = 0
for k, r in TT['sets'].items():
    im = r.get('img'); pth = None
    if im: pth = os.path.join(R, im) if im.startswith('assets') else SCR + 'fymfix2/build/' + im[4:]
    if not pth or not os.path.exists(pth): continue
    pal = P.tile_palette(pth)
    if not pal: continue
    backf = set(r.get('back_colors') or r.get('colors') or [])
    # back = biggest cluster whose family is a back color (else the biggest cluster)
    bi = next((i for i, (h, w) in enumerate(pal) if fam(h) in backf), 0)
    back = pal[bi][0]
    rest = [(h, w) for i, (h, w) in enumerate(pal) if i != bi and P.dE(h, back) > 12]
    layf = set(r.get('layer_colors') or [])
    lay = [h for h, w in rest if (not layf or fam(h) in layf) and w >= 0.03][:2]
    if layf and not lay:  # her named layer family not separated by k-means: nearest cluster by family hue
        lay = [h for h, w in rest if fam(h) in layf or (('green' in layf) and fam(h) in ('yellow', 'gold', 'brown'))][:1]
    r['back_hex'] = back; r['layer_hex'] = lay; r['palette'] = pal
    sig = [back] + [h for h, w in rest if w >= 0.08][:2]
    if k in SIG_ADD and all(P.dE(SIG_ADD[k][0], s) > 15 for s in sig): sig = sig[:2] + [SIG_ADD[k][0]]
    r['signature'] = sig[:3]; n += 1
# Her words override what the photo clusters suggest (doc 76): Drake's back is olive; Dandy has an olive layer; La Fete has
# olive + deep teal layers. Pick the measured cluster nearest the named reference (dE < 25), else use the reference itself.
HAND = {'drake': {'back': '#5b5a24'}, 'dandy': {'layers': ['#6f6a2c']}, 'lafete': {'layers': ['#6f6a2c', '#2f6970']}}
for k, h in HAND.items():
    r = TT['sets'].get(k)
    if not r or not r.get('palette'): continue
    pal = r['palette']
    def near(ref):
        best = min(pal, key=lambda x: P.dE(ref, x[0])); return best[0] if P.dE(ref, best[0]) < 25 else ref
    if 'back' in h: r['back_hex'] = near(h['back'])
    if 'layers' in h: r['layer_hex'] = [near(x) for x in h['layers']]
    r['layer_hex'] = [x for x in r.get('layer_hex', []) if x != r['back_hex']]
    r['signature'] = [r['back_hex']] + [x for x in r['layer_hex'] if x != r['back_hex']][:2]
    r['measured_src'] = 'photo, named by Tiffany (doc 76)'
PASTEL = {'pearlescent', 'luminaire', 'taylor', 'limoncello', 'sorbet', 'moonlight', 'amara'}
for k in TT['sets']: TT['sets'][k]['pastel_family'] = k in PASTEL
TT['about'] += (' | Oct 19 overnight: back_hex/layer_hex/palette/signature = MEASURED colors from the album tile photo (white faces '
                'dropped; back = biggest cluster in a back family). Layer picks and the color finder use these exact shades, never color '
                'names (doc 77). pastel_family (doc 76): Pearlescent, Luminaire, Taylor, Limoncello, Sorbet, Moonlight, Amara.')
json.dump(TT, open(TP, 'w'), indent=1, ensure_ascii=False)
print('tiles measured', n)
