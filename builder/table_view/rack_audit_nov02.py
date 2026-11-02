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
safe = lambda k: re.sub(r'[^A-Za-z0-9]+', '_', k).strip('_')[:90]

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
    mn = rgb.min(2); sp = rgb.max(2) - mn
    tr = al < 40; op = al > 200
    out = {'w': W, 'h': H, 'transp': round(float(tr.mean()), 3)}
    near = (mn >= 228) & (sp <= 22) & op
    # white box: near-white opaque pixels connected to the border
    lab, n = ndimage.label(near)
    border = np.zeros_like(near); border[:2, :] = border[-2:, :] = border[:, :2] = border[:, -2:] = True
    ids = np.unique(lab[border & near]); ids = ids[ids > 0]
    out['box'] = round(float(np.isin(lab, ids).mean()), 4) if len(ids) else 0.0
    # fringe: opaque pixels within 2px of transparency
    edge = op & ndimage.binary_dilation(tr, iterations=2)
    ne = int(edge.sum()); out['edge_n'] = ne
    fw = (mn >= 215) & (sp <= 30)
    out['fringe'] = round(float((edge & fw).sum() / ne), 3) if ne else 0.0
    inner = op & ~ndimage.binary_dilation(tr, iterations=6)
    out['inner_light'] = round(float(np.median(mn[inner])) if inner.any() else 0, 1)
    why = []
    if out['transp'] < 0.02: why.append('no transparency (white card behind the rack)')
    if out['box'] > 0.015: why.append(f"white box touching the photo edge ({out['box']*100:.1f}% of the image)")
    if not wh and out['fringe'] > 0.12 and out['inner_light'] < 200: why.append(f"white fringe on {out['fringe']*100:.0f}% of the cut edge")
    out['why'] = why; return out
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
            m = metrics(im, whiteish(D['racks'][k])); m['src'] = src; res[k] = m
            items.append((k, im, f"{D['racks'][k]['n']} | " + ('; '.join(m['why']) or f"ok (fringe {m['fringe']}, box {m['box']})"), bool(m['why'])))
        items.sort(key=lambda x: (not x[3], x[2]))
        for n0 in range(0, len(items), 36): sheet(items[n0:n0 + 36], f'{OUT}/racks_{n0 // 36:02d}.jpg')
        json.dump(res, open(f'{OUT}/rack_audit.json', 'w'), indent=1)
        bad = {k: v['why'] for k, v in res.items() if v['why']}
        print('audit: table racks', len(ks), 'flagged', len(bad)); [print(' ', D['racks'][k]['n'], '|', '; '.join(w)) for k, w in bad.items()]
    elif mode == 'fix':
        from fym_defringe import defringe
        OVD.mkdir(parents=True, exist_ok=True); done, nu = {}, {}
        for k in ks:
            if (OVD / (safe(k) + '.webp')).exists(): continue
            uri = IMG.get(D['racks'][k].get('im'));
            if not uri: nu[k] = 'no rack photo'; continue
            im = decode(uri); wh = whiteish(D['racks'][k]); m = metrics(im, wh)
            if not m['why']: continue
            a = np.asarray(im).copy()
            if m['transp'] < 0.02 or m['box'] > 0.015:  # flood the white background in from the border
                rgb = a[..., :3].astype(int); mn = rgb.min(2); sp = rgb.max(2) - mn
                bgm = (mn >= (240 if wh else 225)) & (sp <= (14 if wh else 26))
                lab, _ = ndimage.label(bgm); bd = np.zeros_like(bgm); bd[:2, :] = bd[-2:, :] = bd[:, :2] = bd[:, -2:] = True
                ids = np.unique(lab[bd & bgm]); ids = ids[ids > 0]; kill = np.isin(lab, ids)
                a[..., 3] = np.where(kill, 0, a[..., 3])
            fx = defringe(Image.fromarray(a, 'RGBA'), whiteish_rack=wh)
            al = np.asarray(fx)[..., 3]; ys, xs = np.where(al > 20)
            if len(xs): fx = fx.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
            m2 = metrics(fx, wh)
            if m2['why']: nu[k] = 'Our photo of these racks still has a white edge after cleaning; not on the table yet.'; continue
            p = OVD / (safe(k) + '.webp'); fx.save(p, 'WEBP', quality=90, method=6); done[k] = {'file': str(p.relative_to(R0)), 'was': m['why']}
        aud['fixed'].update(done); aud['not_usable'].update(nu)
        json.dump(aud, open(AUD, 'w'), indent=1)
        print('fix: re-cut', len(done), 'not usable', len(nu))
    elif mode == 'check':
        h = open(os.path.join(B, 'index.html')).read(); i = h.index('const D=') + 8; D2, _ = json.JSONDecoder().raw_decode(h[i:]); tv = D2.get('tv') or {}
        rk, ro = tv.get('rk', {}), tv.get('ro', {})
        bad = 0
        for k in rk:
            uri = ro.get(k) or IMG.get(D['racks'].get(k, {}).get('im'))
            if not uri: print(f"[146] Table rack {k}: no image"); bad += 1; continue
            m = metrics(decode(uri), whiteish(D['racks'][k]))
            if m['why']: print(f"[146] Table rack {D['racks'][k]['n']}: {'; '.join(m['why'])}"); bad += 1
        sys.exit(1 if bad else 0)
