"""Album card mat photo check (Tiffany Nov 21-22 2026, Sadie Jane review): the mat must fill the card to its corners.
Flags, per card of a BUILT card spec (<work>/spec.json from scripts/albumcard/specs/*_build.py; each card has 'mat' = the cropped mat as a data URI):
  margin  an edge strip (outer 2%) that is mostly blank white/near-white while the mat inside is not: a white border or cut-out edge
  fold    a corner block (14%) that is mostly near-black while the mat is not a dark mat: a folded-over corner showing the backing
It cannot see hands, props or racks covering the key colour: those are still a LOOK at the contact sheet.
Allow list: config/card-mat-edge-ok.json {"ok": {"<card file>": "reason"}}.
Usage: python3 scripts/checks/card_mat_edge_check.py <work>/spec.json [more specs]   (exit 1 on any flag)"""
import sys, json, io, base64, os
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def check(img):
    a = np.asarray(img.convert('RGB').resize((400, 400))).astype(int)
    white = (a.min(axis=2) > 236) & ((a.max(axis=2) - a.min(axis=2)) < 14)
    dark = (a.max(axis=2) < 118) & ((a.max(axis=2) - a.min(axis=2)) < 20)   # black / charcoal backing, no hue
    out = []
    inner_white = white[60:340, 60:340].mean()
    for nm, strip in (('top', white[:8]), ('bottom', white[-8:]), ('left', white[:, :8]), ('right', white[:, -8:])):
        if strip.mean() > .7 and inner_white < .45: out.append(f'margin {nm} ({strip.mean():.0%} blank)')
    blks = {'top-left': dark[:120, :120].mean(), 'top-right': dark[:120, -120:].mean(), 'bottom-left': dark[-120:, :120].mean(), 'bottom-right': dark[-120:, -120:].mean()}
    for nm, v in blks.items():   # one corner charcoal while the other three are not = the backing showing
        if v > .28 and max(x for k, x in blks.items() if k != nm) < .08 and dark.mean() < .2: out.append(f'fold {nm} ({v:.0%} dark)')
    return out


def run(specs):
    okp = os.path.join(REPO, 'config/card-mat-edge-ok.json')
    ok = json.load(open(okp))['ok'] if os.path.exists(okp) else {}
    bad = []
    for sp in specs:
        for c in json.load(open(sp))['cards']:
            m = c.get('mat') or ''
            if not m.startswith('data:'): continue
            f = check(Image.open(io.BytesIO(base64.b64decode(m.split(',', 1)[1]))))
            if f and c['file'] not in ok: bad.append(f"{c['file']}: " + '; '.join(f))
    return bad


if __name__ == '__main__':
    bad = run(sys.argv[1:])
    if bad:
        print(f'CARD MAT EDGE CHECK FAIL ({len(bad)}):'); [print('  ' + b) for b in bad]; sys.exit(1)
    print('CARD MAT EDGE CHECK PASS')
