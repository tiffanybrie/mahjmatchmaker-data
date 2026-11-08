#!/usr/bin/env python3
"""Round-2 contact sheets for the by-eye pass: per album, every selected mat FULL with the album tiles inset
bottom-right (match-card style), numbered; 24 per sheet.
Usage: python3 scripts/audits/album_missed_round2_sheets_nov07.py <scored.json> <selected.json> <mcmap.json> <fym_site_dir> <out_dir>
"""
import json, os, sys, collections
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from album_missed_sheets_nov07 import fym_img, font, card  # noqa: E402

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
_C = {}


def mat_img(m, mcmap, site):
    k = m['img']
    if k not in _C:
        im = fym_img('m/' + os.path.basename(k), mcmap, site) if '/fym-v' in k else (
            Image.open(k).convert('RGB') if os.path.exists(k) else None)
        if im is not None: im.thumbnail((600, 600))
        _C[k] = im
    return _C[k]


def main(scored, selected, mcmap_p, site, out):
    d = json.load(open(scored)); sel = json.load(open(selected)); mcmap = json.load(open(mcmap_p))
    os.makedirs(out, exist_ok=True); M = d['mats']; A = d['albums']
    by = collections.defaultdict(list)
    for p in sel: by[p['album']].append(p)
    f1, f2 = font(15, True), font(13); W = 290; cols = 6; per = 24
    only = os.environ.get('ONLY', '').split(',') if os.environ.get('ONLY') else None
    for slug, ps in by.items():
        if only and slug not in only: continue
        ps.sort(key=lambda p: -p['score'])
        tile = Image.open(os.path.join(R, A[slug]['tile_img'])).convert('RGB')
        for part in range(0, len(ps), per):
            chunk = ps[part:part + per]; rows = (len(chunk) + cols - 1) // cols
            sh = Image.new('RGB', (cols * (W + 8) + 8, 40 + rows * (W + 46)), (240, 238, 232)); dr = ImageDraw.Draw(sh)
            dr.text((10, 10), f"{A[slug]['name']}  {part + 1}-{part + len(chunk)} of {len(ps)}", fill=(0, 0, 0), font=font(20, True))
            for i, p in enumerate(chunk):
                m = M[p['key']]; im = mat_img(m, mcmap, site) or Image.new('RGB', (300, 300), (200, 60, 60))
                x = 8 + (i % cols) * (W + 8); y = 40 + (i // cols) * (W + 46)
                sh.paste(card(im, tile, W), (x, y))
                dr.text((x + 2, y + W + 2), f"{part + i + 1}. {m['name']}"[:34], fill=(0, 0, 0), font=f1)
                dr.text((x + 2, y + W + 22), f"{m['brand'][:20]} {p['score']:.1f}{' H' if m['hol'] else ''}", fill=(80, 80, 80), font=f2)
            sh.save(os.path.join(out, f'{slug}-{part // per + 1}.jpg'), quality=78)
        print(slug, len(ps))


if __name__ == '__main__':
    main(*sys.argv[1:6])
