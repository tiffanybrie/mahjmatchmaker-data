"""FYM v92 Bespoke rack fix (Tiffany Oct 25 21:42, second report; first was Oct 23 3:55pm Highlighter Pink).
Bespoke shoots Highlighter Pink (hottie-pink), Peacock Blue (turquoise) and Bright White on a BLACK background.
Our old cutouts keyed that black out badly: jagged dark remnants around the racks (sm) and the HD copies were the raw
black-background photo. Fix: a luminance key made for objects on black (alpha from brightness, colour un-premultiplied),
so translucent acrylic stays see-through with no dark fringe. Source = Bespoke's own listing image 1 (full res).
HD copies are dropped (like v89 PLM Chartreuse) and the new 800px cutout is the card image.
cutout_on_black() is the house method for any future rack shot on black.
Usage: python3 v92_bespokeracks.py <build_dir>"""
import sys, os, io, json, base64
import numpy as np
from PIL import Image
from scipy import ndimage
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'

def cutout_on_black(im):
    a = np.asarray(im.convert('RGB')).astype(float) / 255
    al = np.clip((a.max(2) - 0.06) / 0.55, 0, 1) ** 0.8
    m = ndimage.binary_closing(al > 0.12, iterations=6); lab, n = ndimage.label(m)
    keep = lab == (np.argmax(ndimage.sum(m, lab, range(1, n + 1))) + 1)
    al = al * ndimage.binary_dilation(keep, iterations=4)
    col = np.clip(a / np.maximum(al[..., None], 1e-3), 0, 1)
    o = Image.fromarray((np.dstack([col, al]) * 255).astype(np.uint8), 'RGBA'); return o.crop(o.getbbox())

FIX = {  # rack key -> asset (made with cutout_on_black from bespokemahjong.com/products/<handle> image 1)
    'www.bespokemahjong.com/the-ultimate-rack-hottie-pink': 'assets/racks/v92/bespoke-ultimate-hottie-pink.webp',
    'www.bespokemahjong.com/the-ultimate-rack-turquoise': 'assets/racks/v92/bespoke-ultimate-turquoise.webp',
    'www.bespokemahjong.com/the-ultimate-rack-bright-white': 'assets/racks/v92/bespoke-ultimate-bright-white.webp',
}
if __name__ == '__main__':
    B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
    i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
    IMG = {}; hd = json.load(open(B + '/hd/index.json'))
    for k, path in FIX.items():
        r = D['racks'][k]; nk = r['im'] + 'v92'
        IMG[nk] = 'data:image/webp;base64,' + base64.b64encode(open(REPO + path, 'rb').read()).decode()
        r['im'] = nk; hd['r'].pop(k, None); print('re-cut', r['n'])
    json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
    open(P, 'w').write(h)
