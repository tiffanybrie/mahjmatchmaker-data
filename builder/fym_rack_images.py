"""Every rack photo shown in FYM must be LOOKED AT before it can go out (Tiffany Oct 23 3:55pm + Oct 25 21:42:
"It's supposed to be checked for every image that we don't have this kind of a horrible cutout going on").
Review list: builder/fym_flags/rack_image_review.json  {sha1: {key, name, verdict: ok|bad, date, note}}
Gate [56] fails if a visible rack shows an image that is not reviewed 'ok'.
  python3 builder/fym_rack_images.py <build_dir> --sheet out.jpg   contact sheet of UNREVIEWED images (on white AND navy, so
                                                                  dark fringes and white halos both show) -> look at it
  python3 builder/fym_rack_images.py <build_dir> --approve         mark every currently unreviewed image ok (ONLY after looking)
"""
import sys, os, re, json, glob, base64, hashlib, io
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
REV = REPO + 'builder/fym_flags/rack_image_review.json'

def shown(B):
    s = open(B + '/index.html').read(); i = s.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(s[i:])
    want = {r['im'] for r in D['racks'].values() if not r.get('hid')}; IMG = {}
    for f in sorted(glob.glob(B + '/b*.js')) + [B + '/index.html']:
        for m in re.finditer(r'"([A-Za-z0-9_]+)":"data:image/[a-z]+;base64,([^"]+)"', open(f, errors='ignore').read()):
            if m.group(1) in want: IMG[m.group(1)] = m.group(2)
    hd = json.load(open(B + '/hd/index.json')).get('r', {}); cache = {}; out = []
    for k, r in D['racks'].items():
        if r.get('hid'): continue
        srcs = []
        if r.get('im') in IMG: srcs.append(('sm', base64.b64decode(IMG[r['im']])))
        v = hd.get(k)
        if v:
            if v.startswith('file:'): srcs.append(('hd', open(B + '/' + v[5:], 'rb').read()))
            else:
                cache.setdefault(v, json.load(open(B + '/hd/' + v))); du = cache[v].get(k)
                if du: srcs.append(('hd', base64.b64decode(du.split(',', 1)[1])))
        if not srcs: out.append((k, r['n'], 'none', None, None)); continue
        for t, b in srcs: out.append((k, r['n'], t, hashlib.sha1(b).hexdigest(), b))
    return out

def problems(B):
    rev = json.load(open(REV)) if os.path.exists(REV) else {}; bad = []
    for k, n, t, h, _ in shown(B):
        v = rev.get(h, {}).get('verdict') if h else None
        if v != 'ok': bad.append(f"{n} ({t}) {'REJECTED cutout' if v == 'bad' else 'no image' if not h else 'not reviewed'}")
    return bad

if __name__ == '__main__':
    B = sys.argv[1]; rev = json.load(open(REV)) if os.path.exists(REV) else {}
    todo = [x for x in shown(B) if x[3] and x[3] not in rev]
    if '--sheet' in sys.argv:
        from PIL import Image, ImageDraw
        out = sys.argv[sys.argv.index('--sheet') + 1]; S = 300; W = 4
        sh = Image.new('RGB', (W * S * 2, max(1, (len(todo) + W - 1) // W) * (S // 2 + 18)), 'white'); d = ImageDraw.Draw(sh)
        for j, (k, n, t, h, b) in enumerate(todo):
            im = Image.open(io.BytesIO(b)).convert('RGBA'); im.thumbnail((S - 8, S // 2 - 8)); x = (j % W) * 2 * S; y = (j // W) * (S // 2 + 18)
            for dx, bg in ((0, (255, 255, 255, 255)), (S, (25, 45, 85, 255))):
                c = Image.new('RGBA', im.size, bg); c.alpha_composite(im); sh.paste(c.convert('RGB'), (x + dx, y + 16))
            d.text((x, y), f'{n[:40]} [{t}]', fill='black')
        sh.save(out); print(len(todo), 'unreviewed ->', out)
    elif '--approve' in sys.argv:
        import datetime
        for k, n, t, h, _ in todo: rev[h] = {'key': k, 'name': n, 'tag': t, 'verdict': 'ok', 'date': str(datetime.date.today())}
        json.dump(rev, open(REV, 'w'), indent=0); print('approved', len(todo))
    else:
        p = problems(B); print('\n'.join(p) or 'all rack images reviewed ok')
