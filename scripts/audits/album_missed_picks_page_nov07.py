#!/usr/bin/env python3
"""Phone-first yes-only review page for the Nov 7 album missed-mats audit (374 mats, 43 albums).

One card per mat: mat photo full width with the album's tile photo inset bottom-right (match-card style, CLAUDE.md
PICK / REVIEW rule), tap to zoom, full mat name, brand, partner line, the one-line why, a heart (yes-only; unmarked = no).
Holiday mats sit in their own "Holiday" section at the end of each album.

Usage: python3 scripts/audits/album_missed_picks_page_nov07.py <mcmap.json> <fym_site_dir> <out_dir>
Writes <out_dir>/index.html, <out_dir>/files.json, <out_dir>/m/<id>.jpg (900px mats), <out_dir>/t/<album>.jpg (tiles).
"""
import json, os, sys, hashlib, html
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from album_missed_sheets_nov07 import fym_img  # noqa: E402

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
AUD = os.path.join(R, 'docs/audits/album-missed-mats-2026-11-07.json')
SL = os.path.join(R, 'docs/audits/album-missed-nov07-data/shortlist.json')
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'album_missed_picks_page_nov07.html')


def load_mat(img, mcmap, site):
    if '/fym-v' in img:
        return fym_img('m/' + os.path.basename(img), mcmap, site)
    p = os.path.normpath(img)
    return Image.open(p).convert('RGB') if os.path.exists(p) else None


def main(mcmap_p, site, out):
    A = json.load(open(AUD)); S = json.load(open(SL)); mcmap = json.load(open(mcmap_p))
    os.makedirs(os.path.join(out, 'm'), exist_ok=True); os.makedirs(os.path.join(out, 't'), exist_ok=True)
    files, mats, albums, missing = [], {}, [], []
    order = sorted(A['albums'], key=lambda k: (k != 'papaya-spritz', -A['albums'][k]['strong_count'], A['albums'][k]['name']))
    for slug in order:
        a = A['albums'][slug]; s = S[slug]; sm = {x['key']: x for x in s['shortlist']}
        tp = 't/%s.jpg' % slug
        if tp not in files:
            t = Image.open(os.path.join(R, s['tile_img']))
            if t.mode in ('RGBA', 'LA', 'P'):
                t = t.convert('RGBA'); bg = Image.new('RGB', t.size, (255, 255, 255)); bg.paste(t, mask=t.split()[-1]); t = bg
            t = ImageOps.contain(t.convert('RGB'), (520, 520)); t.save(os.path.join(out, tp), quality=82, optimize=True); files.append(tp)
        items = []
        for st in a['strong']:
            x = sm[st['key']]
            mid = hashlib.md5(st['key'].encode()).hexdigest()[:10]
            mp = 'm/%s.jpg' % mid
            if st['key'] not in mats:
                im = load_mat(x['img'], mcmap, site)
                if im is None:
                    missing.append(st['key']); mp = ''
                else:
                    im = ImageOps.contain(im, (900, 900)); im.save(os.path.join(out, mp), quality=80, optimize=True, progressive=True)
                    files.append(mp)
                mats[st['key']] = mp
            mp = mats[st['key']]
            why = st['why'].strip()
            if why.upper().startswith('HOLIDAY:'): why = why[8:].strip()
            head = ' '.join(st['name'].lower().split()[:2])
            if ': ' in why and head in why.split(': ', 1)[0].lower(): why = why.split(': ', 1)[1]
            why = why[:1].upper() + why[1:]
            items.append({'k': st['key'], 'n': st['name'], 'b': st['brand'], 'img': mp, 'url': st['url'],
                          'p': st['partner'].startswith('partner'), 'pl': st['partner'], 'w': why,
                          'h': st['kind'] == 'holiday', 'mo': 'motif' in st['kind']})
        albums.append({'id': slug, 'name': a['name'], 'tile': tp, 'cards': a['live_cards'], 'items': items})
    tpl = open(TEMPLATE).read()
    data = json.dumps({'albums': albums}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('/*__DATA__*/null', data))
    json.dump(files, open(os.path.join(out, 'files.json'), 'w'), indent=0)
    n = sum(len(a['items']) for a in albums); h = sum(i['h'] for a in albums for i in a['items'])
    print('albums', len(albums), 'mats', n, 'holiday', h, 'distinct mat photos', sum(1 for v in mats.values() if v), 'missing', missing)


if __name__ == '__main__':
    main(*sys.argv[1:4])
