#!/usr/bin/env python3
"""Contact sheets for the album missed-mats audit (Nov 7): one sheet per album, each shortlisted mat shown FULL with the
album tile photo inset bottom-right (match-card style, CLAUDE.md pick/review rule), numbered for the by-eye pass.

FYM mat photos come from the FYM v117 image bundles (mc/<c>.webp: webp blobs + JSON footer {f: [offset, len]}), resolved
with the bundle map the app itself uses (mcmap.json, evaluated from fym-v117 loadMC) against the fym-site-preview worktree.
Usage: python3 scripts/audits/album_missed_sheets_nov07.py <shortlist.json> <mcmap.json> <fym_site_dir> <out_dir>
"""
import json, os, re, sys, io, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
MCN = 12
_B = {}


def bundle(c, mcmap, site):
    if c in _B: return _B[c]
    url = mcmap.get(str(c)); data = None
    if url:
        m = re.search(r'@([0-9a-f]{40})/(site-app/[^/]+/)', url)
        p = m.group(2) + 'mc/%d.webp' % c
        lp = os.path.join(site, p)
        if os.path.exists(lp): data = open(lp, 'rb').read()
        else:
            data = subprocess.run(['git', '-C', site, 'show', '%s:%s' % (m.group(1), p)], capture_output=True).stdout or None
    else:
        cands = sorted([d for d in os.listdir(os.path.join(site, 'site-app')) if os.path.exists(os.path.join(site, 'site-app', d, 'mc', '%d.webp' % c))],
                       key=lambda d: (int(re.sub(r'\D', '', d) or 0)))
        if cands: data = open(os.path.join(site, 'site-app', cands[-1], 'mc', '%d.webp' % c), 'rb').read()
    idx = None
    if data:
        n = int.from_bytes(data[-4:], 'little'); idx = json.loads(data[-4 - n:-4].decode())
    _B[c] = (data, idx); return _B[c]


def fym_img(f, mcmap, site):
    c = int(f.split('/')[1].split('.')[0]) // MCN
    data, idx = bundle(c, mcmap, site)
    if not data or f not in idx: return None
    a, l = idx[f]; return Image.open(io.BytesIO(data[a:a + l])).convert('RGB')


def font(sz, bold=False):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else '')]:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def card(mat, tile, W=420):
    m = ImageOps.contain(mat, (W, W)); cv = Image.new('RGB', (W, W), (255, 255, 255))
    cv.paste(m, ((W - m.width) // 2, (W - m.height) // 2))
    t = ImageOps.contain(tile, (int(W * .42), int(W * .42)))
    x, y = W - t.width - 8, W - t.height - 8
    ImageDraw.Draw(cv).rectangle([x - 3, y - 3, x + t.width + 2, y + t.height + 2], fill=(255, 255, 255))
    cv.paste(t, (x, y)); return cv


def main(sl, mcmap_p, site, out):
    S = json.load(open(sl)); mcmap = json.load(open(mcmap_p)); os.makedirs(out, exist_ok=True)
    f1, f2 = font(17, True), font(14)
    for slug, a in S.items():
        if os.environ.get('ONLY') and slug not in os.environ['ONLY'].split(','): continue
        tile = Image.open(os.path.join(R, a['tile_img'])).convert('RGB')
        items = a['shortlist']; cols = 4; W = 420; H = W + 58
        rows = (len(items) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * W + (cols + 1) * 10, 70 + rows * (H + 10)), (240, 238, 232))
        d = ImageDraw.Draw(sheet)
        d.text((12, 12), f"{a['name']} - missed-mat shortlist (album built ~{a['cutoff']}; {a['album_cards']} cards live)", fill=(20, 20, 20), font=font(24, True))
        d.text((12, 44), "mat full, album tiles inset bottom-right; H = holiday", fill=(80, 80, 80), font=f2)
        for i, r in enumerate(items):
            if r['img'].startswith(os.path.join(site, '')) or '/fym-v' in r['img']:
                f = os.path.relpath(r['img'], os.path.dirname(r['img']).rsplit('/m', 1)[0]) if False else 'm/' + os.path.basename(r['img'])
                im = fym_img(f, mcmap, site)
            else:
                im = Image.open(r['img']).convert('RGB') if os.path.exists(r['img']) else None
            if im is None: im = Image.new('RGB', (400, 400), (200, 60, 60))
            x = 10 + (i % cols) * (W + 10); y = 70 + (i // cols) * (H + 10)
            sheet.paste(card(im, tile, W), (x, y))
            lab = f"{i + 1}. {r['name']}"[:40]
            d.text((x + 4, y + W + 4), lab, fill=(0, 0, 0), font=f1)
            d.text((x + 4, y + W + 26), f"{r['brand'][:22]} · {r['score']}{' · H' if r['hol'] else ''}{'' if r['pa'] else ' · np'}", fill=(70, 70, 70), font=f2)
        sheet.save(os.path.join(out, f'{slug}.jpg'), quality=82)
        print(slug, len(items))


if __name__ == '__main__':
    main(*sys.argv[1:5])
