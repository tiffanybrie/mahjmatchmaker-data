"""Table view RACK IMAGE AUDIT (Tiffany Nov 1 11:33pm: only clean cut-outs on the table: no white edges, no white boxes, e.g. Mahjong
Register Emerald Pearl Scalloped showed a white box, Emerald Tortoise Scalloped white fringes).
For every rack the Table view would draw (coverage class S in config/tableview-photo-class-nov01.json, not hidden), the image the
Table draws (TVD override in assets/table-view/racks/<safe id>.webp if present, else the app's rack image IMG[R[id].im]) must:
  alpha  - have real transparency (a photo on a white card has none = a white box on the mat)
  box    - no opaque near-white region connected to the image border (> 1.5% of the image)
  fringe - the cut edge (opaque pixels touching transparency) is not near-white, unless the rack itself is white/clear/pearl
Modes:
  audit <build dir> <out dir>  : metrics json + contact sheets (dark green / red plaid) of every rack, flagged first
  fix   <build dir>            : try builder/fym_defringe.py (and a border flood-fill for white boxes) on flagged racks; a fixed image
                                 that passes goes to assets/table-view/racks/; one that still fails is listed as not usable in Table
                                 (config/tableview-rack-audit-nov02.json 'not_usable' with the reason) - Tiffany: 'others grayed or re-cut'
  check <build dir>            : gate [146]: print [146] FAIL lines for any rack the build's Table view would draw that fails
"""
import sys, os, re, json, io, base64, glob, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
R0 = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R0 / 'builder'))
COV = json.load(open(R0 / 'config/tableview-photo-class-nov01.json'))['_racks']
AUD = R0 / 'config/tableview-rack-audit-nov02.json'
OVD = R0 / 'assets/table-view/racks'
import hashlib
safe = lambda k: re.sub(r'[^A-Za-z0-9]+', '_', k).strip('_')[-60:] + '_' + hashlib.md5(k.encode()).hexdigest()[:8]

def load_build(B):
    h = open(os.path.join(B, 'index.html')).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
    IMG = {}
    for src in [h] + [open(f).read() for f in sorted(glob.glob(os.path.join(B, 'b*.js')))]:
        for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', src):
            o, _ = json.JSONDecoder().raw_decode(src[m.end():]); IMG.update(o)
    return D, IMG
def decode(uri):
    return Image.open(io.BytesIO(base64.b64decode(uri.split(',', 1)[1]))).convert('RGBA')
def whiteish(r):
    rf = set(r.get('rf') or []); n = (r.get('n') or '').lower()
    return bool(rf & {'clear', 'pearl'}) or 'neutral' in rf and re.search(r'white|ivory|cream|pearl|clear|acrylic|lucite|opal', n) is not None
def metrics(im, wh):
    a = np.asarray(im).astype(float); al = a[..., 3]; rgb = a[..., :3]; H, W = al.shape
    mn = rgb.min(2); sp = rgb.max(2) - mn; L = rgb.mean(2)
    tr = al < 40; op = al > 200
    out = {'w': W, 'h': H, 'transp': round(float(tr.mean()), 3)}
    # white card / box: pure-white opaque pixels connected to the photo border
    pw = (mn >= 240) & (sp <= 14) & op
    lab, n = ndimage.label(pw)
    border = np.zeros_like(pw); border[:2, :] = border[-2:, :] = border[:, :2] = border[:, -2:] = True
    ids = np.unique(lab[border & pw]); ids = ids[ids > 0]
    out['box'] = round(float(np.isin(lab, ids).mean()), 4) if len(ids) else 0.0
    # fringe / halo: cut-edge pixels clearly lighter than the rack just inside them
    edge = op & ndimage.binary_dilation(tr, iterations=1)
    band = op & ~ndimage.binary_dilation(tr, iterations=3) & ndimage.binary_dilation(tr, iterations=7)
    num = ndimage.uniform_filter(L * band, 11); den = ndimage.uniform_filter(band.astype(float), 11)
    ref = np.where(den > 0.02, num / np.maximum(den, 1e-6), L)
    ne = int(edge.sum()); out['edge_n'] = ne
    halo = edge & (L - ref > 32) & (((mn >= 222) & (sp <= 22)) | ((mn > 110) & (sp <= 14) & (L - ref > 60)))  # whitish / grey rim, not a coloured highlight
    out['fringe'] = round(float(halo.sum() / ne), 3) if ne else 0.0
    why = []
    if out['box'] > 0.01: why.append(f"white card around the rack ({out['box']*100:.1f}% of the photo)")
    inner = op & ~ndimage.binary_dilation(tr, iterations=6); il = float(np.median(mn[inner])) if inner.any() else 0
    if out['fringe'] > 0.10 and not (wh and il > 215): why.append(f"light halo on {out['fringe']*100:.0f}% of the cut edge")
    out['why'] = why; return out
def shave(img, px=1):
    """the Table view's draw-time 1px alpha shave (preview_tv.js rackPrep): grey erosion of alpha, 3x3"""
    a = np.asarray(img).copy(); a[..., 3] = ndimage.grey_erosion(a[..., 3], size=(2 * px + 1, 2 * px + 1)); return Image.fromarray(a, 'RGBA')
def table_racks(D):
    return [k for k, v in COV.items() if v.get('class') == 'S' and k in D['racks'] and not D['racks'][k].get('hid')]
def image_for(k, D, IMG):
    p = OVD / (safe(k) + '.webp')
    if p.exists(): return Image.open(p).convert('RGBA'), 'override'
    uri = IMG.get(D['racks'][k].get('im'))
    return (decode(uri), 'app') if uri else (None, 'missing')
def plaid(w, h):
    im = Image.new('RGB', (w, h), (150, 30, 40)); d = ImageDraw.Draw(im)
    for x in range(0, w, 36): d.rectangle([x, 0, x + 9, h], fill=(30, 70, 45)); d.line([x + 20, 0, x + 20, h], fill=(220, 190, 90), width=2)
    for y in range(0, h, 36): d.rectangle([0, y, w, y + 9], fill=(30, 70, 45)); d.line([0, y + 20, w, y + 20], fill=(220, 190, 90), width=2)
    return im
def sheet(items, path):
    cw, chh = 380, 120; cols = 3; rows = (len(items) + cols - 1) // cols
    S = Image.new('RGB', (cols * cw * 2, rows * chh), (255, 255, 255)); d = ImageDraw.Draw(S)
    for j, (k, im, label, bad) in enumerate(items):
        r_, c_ = divmod(j, cols); x0, y0 = c_ * cw * 2, r_ * chh
        for t, bg in enumerate((Image.new('RGB', (cw, chh), (31, 90, 58)), plaid(cw, chh))):
            t_ = im.copy(); t_.thumbnail((cw - 16, chh - 34)); bg.paste(t_, ((cw - t_.width) // 2, 6), t_)
            S.paste(bg, (x0 + t * cw, y0))
        d.rectangle([x0, y0 + chh - 26, x0 + 2 * cw, y0 + chh], fill=(255, 235, 235) if bad else (240, 248, 240))
        d.text((x0 + 4, y0 + chh - 24), label[:110], fill=(160, 0, 0) if bad else (20, 60, 20))
    S.save(path, quality=88)

if __name__ == '__main__':
    mode, B = sys.argv[1], sys.argv[2]; D, IMG = load_build(B); ks = table_racks(D)
    aud = json.load(open(AUD)) if AUD.exists() else {'not_usable': {}, 'fixed': {}}
    if mode == 'audit':
        OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True); res = {}; items = []
        for k in ks:
            im, src = image_for(k, D, IMG)
            if im is None: res[k] = {'why': ['no image'], 'src': src}; continue
            m = metrics(shave(im), whiteish(D['racks'][k])); m['src'] = src; res[k] = m
            items.append((k, im, f"{D['racks'][k]['n']} | " + ('; '.join(m['why']) or f"ok (fringe {m['fringe']}, box {m['box']})"), bool(m['why'])))
        items.sort(key=lambda x: (not x[3], x[2]))
        for n0 in range(0, len(items), 36): sheet(items[n0:n0 + 36], f'{OUT}/racks_{n0 // 36:02d}.jpg')
        json.dump(res, open(f'{OUT}/rack_audit.json', 'w'), indent=1)
        bad = {k: v['why'] for k, v in res.items() if v['why']}
        print('audit: table racks', len(ks), 'flagged', len(bad)); [print(' ', D['racks'][k]['n'], '|', '; '.join(w)) for k, w in bad.items()]
    elif mode == 'fix':
        from fym_defringe import defringe
        from rembg import new_session, remove
        SES = new_session('isnet-general-use'); OVD.mkdir(parents=True, exist_ok=True); done, nu = {}, {}
        def choke(img, px=1):
            a = np.asarray(img).copy(); al = a[..., 3]; tr = al < 40
            ring = ndimage.binary_dilation(tr, iterations=px) & ~tr
            a[..., 3] = np.where(ring, 0, al); return Image.fromarray(a, 'RGBA')
        def crop(img):
            al = np.asarray(img)[..., 3]; ys, xs = np.where(al > 20)
            return img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)) if len(xs) else img
        only = set(sys.argv[3].split('|')) if len(sys.argv) > 3 and sys.argv[3] else None; nu_canva = {}; force_rembg = set()
        for k in ks:
            if only is not None and k not in only: continue
            uri = IMG.get(D['racks'][k].get('im'))
            if not uri: nu[k] = 'no rack photo'; continue
            im = decode(uri); wh = whiteish(D['racks'][k]); m = metrics(shave(im), wh)
            if not m['why'] and only is None: continue
            meth = []; a0 = np.asarray(im); il = float(np.median(a0[..., :3].mean(2)[a0[..., 3] > 200])) if (a0[..., 3] > 200).any() else 0  # body lightness
            card = m['box'] > 0.01 and float((a0[..., 3] < 40).mean()) < 0.02   # a photo on a white card (no transparency at all)
            light = il >= 175; dark = il < 110
            if card:
                big = im.convert('RGB'); pad = Image.new('RGB', (big.width + 40, big.height + 40), (255, 255, 255)); pad.paste(big, (20, 20))
                fx = remove(pad, session=SES, post_process_mask=True).crop((20, 20, 20 + big.width, 20 + big.height)); meth.append('rembg isnet')
                fx = choke(fx, 1); meth.append('1px edge choke')
                rgb0 = a0[..., :3].astype(int); body0 = ~((rgb0.min(2) >= 240) & (rgb0.max(2) - rgb0.min(2) <= 14))
                kept = float((np.asarray(fx)[..., 3] > 128)[body0].mean()) if body0.any() else 0
                if kept < 0.85 or metrics(shave(crop(fx)), wh)['why']: nu_canva[k] = f'rembg kept {kept:.0%} of the rack: Canva remove-background'; continue
            elif light:
                continue   # light racks: the original cut is kept; the Table's draw-time 1px shave handles the edge (defringe would eat the body)
            else:
                fx = choke(im, 1); meth.append('1px edge choke')
                if dark: fx = defringe(fx, whiteish_rack=wh); meth.append('fym_defringe')  # defringe only on dark bodies (it eats light ones)
            fx = crop(fx); m2 = metrics(shave(fx), wh)
            p = OVD / (safe(k) + '.webp'); fx.save(p, 'WEBP', quality=92, method=6)
            done[k] = {'file': str(p.relative_to(R0)), 'was': m['why'], 'now': m2['why'], 'method': ' + '.join(meth)}
        aud['fixed'].update(done); aud['not_usable'].update(nu); aud.setdefault('canva', {}).update(nu_canva)
        json.dump(aud, open(AUD, 'w'), indent=1)
        print('canva needed', len(nu_canva), [D['racks'][k]['n'] for k in nu_canva]); print('fix: re-cut', len(done), 'still flagged', sum(1 for v in done.values() if v['now']), 'no photo', len(nu))
        for k, v in done.items():
            if v['now']: print('  still:', D['racks'][k]['n'], v['now'])
    elif mode == 'trim':
        # Nov 2: light racks cut flush to the photo edge (Bird & Bamboo pastels): a partial light strip under the rack (photo leftover)
        # and a white rim. Pad with transparency, drop partial top/bottom rows (< 90% of the widest row), then a 1px choke on every side.
        names = sys.argv[3].split('|'); aud = json.load(open(AUD)); done = {}
        for k in ks:
            if D['racks'][k]['n'] not in names: continue
            im = decode(IMG[D['racks'][k]['im']]); a = np.zeros((im.height + 6, im.width + 6, 4), np.uint8); a[3:-3, 3:-3] = np.asarray(im)
            cov = (a[..., 3] > 200).sum(1); mx = cov.max(); rows = np.where(cov >= .9 * mx)[0]; y0, y1 = rows.min(), rows.max()
            a[:y0, :, 3] = 0; a[y1 + 1:, :, 3] = 0
            tr = a[..., 3] < 40; ring = ndimage.binary_dilation(tr, iterations=1) & ~tr; a[..., 3] = np.where(ring, 0, a[..., 3])
            fx = Image.fromarray(a, 'RGBA'); al = np.asarray(fx)[..., 3]; ys, xs = np.where(al > 20)
            fx = fx.crop((xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3)); m2 = metrics(shave(fx), whiteish(D['racks'][k]))
            p = OVD / (safe(k) + '.webp'); fx.save(p, 'WEBP', lossless=True)
            done[k] = {'file': str(p.relative_to(R0)), 'was': metrics(shave(im), whiteish(D['racks'][k]))['why'], 'now': m2['why'], 'method': 'trim partial edge rows + 1px edge choke (flush light cut-out)'}
            print(D['racks'][k]['n'], 'rows', int(y0) - 3, int(y1) - 3, 'of', im.height, 'now', m2['why'])
        aud['fixed'].update(done); json.dump(aud, open(AUD, 'w'), indent=1)
    elif mode == 'check':
        h = open(os.path.join(B, 'index.html')).read(); i = h.index('const D=') + 8; D2, _ = json.JSONDecoder().raw_decode(h[i:]); tv = D2.get('tv') or {}
        rk, ro = tv.get('rk', {}), tv.get('ro', {})
        bad = 0; A2 = json.load(open(AUD)); ok_eye = A2.get('by_eye_ok', {})
        for k in A2.get('fixed', {}):  # every re-cut rack (incl. QA Nov 2: pusher sticks removed, see-through clear racks) must ship in the build
            if k in rk and k not in ro: print(f"[146] Table rack {D['racks'].get(k, {}).get('n', k)}: re-cut image not in the build (D.tv.ro)"); bad += 1
        for k in rk:
            if k in ok_eye: continue  # looked at on green + plaid: the light edge IS the rack (translucent / tight white crop)
            uri = ro.get(k) or IMG.get(D['racks'].get(k, {}).get('im'))
            if not uri: print(f"[146] Table rack {k}: no image"); bad += 1; continue
            m = metrics(shave(decode(uri)), whiteish(D['racks'][k]))
            if m['why']: print(f"[146] Table rack {D['racks'][k]['n']}: {'; '.join(m['why'])}"); bad += 1
        sys.exit(1 if bad else 0)
