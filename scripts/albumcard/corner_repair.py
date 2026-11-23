"""Corner repair for album card mat photos (Tiffany Nov 23 2026: 'you have to do corner repairs. You cannot do this on our
mock-ups... put that in your rules'). A product render with a curled / folded top-right corner (dark underside) is repaired by
mirroring the mat left<->right inside the peel polygon (same method as FYM Table view, builder/table_view/peel_nov02.py).
Usage: python3 scripts/albumcard/corner_repair.py <mat photo> [out.jpg]  -> writes <name>-repaired.jpg (the mat square, corner filled).
gen2.py REFUSES to build a card whose mat photo still shows a fold (see the mat-edge check there)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'builder', 'table_view'))
from PIL import Image
from peel_nov02 import analyse, fill
def repair(src, out=None, poly=None):
    """poly: optional manual peel polygon [[x,y],...] in 0..1 of the mat square, for a big fold the detector refuses."""
    im = Image.open(src).convert('RGB'); r = analyse(im)
    if poly:
        from peel_nov02 import square_box
        import numpy as np
        a = np.asarray(im).astype(int); H, W = a.shape[:2]; bg = (a.min(2) > 238) & (a.max(2) - a.min(2) < 12)
        rows = np.where((~bg)[:, :W // 2].mean(1) > .3)[0]; cols = np.where((~bg)[H // 2:].mean(0) > .3)[0]
        r = {'b': [cols.min() / W, rows.min() / H, (cols.max() + 1) / W, (rows.max() + 1) / H], 'p': poly, 'area': 0}
    if not r or 'p' not in r: raise SystemExit(f'no repair possible for {src}: {r}')
    out = out or os.path.splitext(src)[0] + '-repaired.jpg'; fill(im, r).save(out, quality=95); return out, r
if __name__ == '__main__':
    import json
    a = sys.argv[1:]; poly = json.loads(a[-1]) if a[-1].startswith('[') else None
    o, r = repair(a[0], a[1] if len(a) > 1 and not a[1].startswith('[') else None, poly); print(o, r['b'])
