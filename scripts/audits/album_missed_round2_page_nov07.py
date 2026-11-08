#!/usr/bin/env python3
"""Round-2 missed-mats pick page (Nov 7 2026): MAT-FIRST, one card per mat with EVERY album it fits.

Inputs: round-2 scores (album_missed_round2_nov07.py), the selection kept after the by-eye pass, and her round-1
yeses (config/picks/missed-mats-round1-2026-11-07.txt): those pairs show as locked "Yes from round 1" and are not new.
Card = mat photo full + a row per album (tile photo chip -> zoom = mat full + tiles inset, heart, star), a note box and
"+ add another album" listing every live album. Sorted most versatile first; album filter at the top.
All selections live in ONE state object saved through persist(state) (localStorage by default; window.MM_LOAD()
returns it) so the page can be wired to the artifact database before publishing.

Usage: python3 scripts/audits/album_missed_round2_page_nov07.py <scored.json> <kept.json> <round1.txt> <mcmap.json> <fym_site_dir> <out_dir>
Writes <out>/index.html, files.json (+ files_part1.json / files_part2.json, <=255 each), m/<id>.jpg (900px), t/<album>.jpg (400px).
"""
import json, os, sys, hashlib, collections
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from album_missed_sheets_nov07 import fym_img  # noqa: E402

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'album_missed_round2_page_nov07.html')
R1_AUDIT = os.path.join(R, 'docs/audits/album-missed-mats-2026-11-07.json')


def round1_yes(path, albums, mats):
    by_name = {v['name']: k for k, v in albums.items()}; yes = set()
    for line in open(path, encoding='utf-8').read().splitlines()[1:]:
        if ': ' not in line: continue
        al, rest = line.split(': ', 1); al = al.replace(' (holiday)', '')
        slug = by_name.get(al)
        if not slug: continue
        for k, m in mats.items():
            if f"{m['name']} ({m['brand']})" in rest: yes.add((slug, k))
    return yes


def load_img(m, mcmap, site):
    k = m['img']
    if '/fym-v' in k: return fym_img('m/' + os.path.basename(k), mcmap, site)
    return Image.open(k).convert('RGB') if os.path.exists(k) else None


def main(scored_p, kept_p, r1_p, mcmap_p, site, out):
    S = json.load(open(scored_p)); kept = json.load(open(kept_p)); mcmap = json.load(open(mcmap_p))
    A, M = S['albums'], S['mats']
    yes = round1_yes(r1_p, A, M)
    shown1 = {(s, x['key']) for s, a in json.load(open(R1_AUDIT))['albums'].items() for x in a['strong']}
    pairs = collections.defaultdict(dict)
    for p in kept: pairs[p['key']][p['album']] = p['score']
    for a, k in yes:  # her round-1 yeses stand on every card that is on the page
        if k in pairs: pairs[k].setdefault(a, 0)
    os.makedirs(os.path.join(out, 'm'), exist_ok=True); os.makedirs(os.path.join(out, 't'), exist_ok=True)
    files, mats_out, missing = [], [], []
    used_albums = set()
    for k, ps in pairs.items():
        new = [a for a in ps if (a, k) not in yes]
        if not new: continue
        m = M[k]; mid = hashlib.md5(k.encode()).hexdigest()[:10]; mp = 'm/%s.jpg' % mid
        im = load_img(m, mcmap, site)
        if im is None: missing.append(k); continue
        if not os.path.exists(os.path.join(out, mp)):
            ImageOps.contain(im, (900, 900)).save(os.path.join(out, mp), quality=80, optimize=True, progressive=True)
        files.append(mp)
        pl = sorted(({'a': a, 's': round(s, 2), 'r1': 2 if (a, k) in yes else (1 if (a, k) in shown1 else 0)}
                     for a, s in ps.items()), key=lambda x: (x['r1'] != 2, -x['s']))
        used_albums.update(ps)
        mats_out.append({'id': mid, 'k': k, 'n': m['name'], 'b': m['brand'], 'pa': m['pa'], 'h': m['hol'],
                         'u': m['url'] or '', 'img': mp, 'p': pl, 'best': max(ps.values())})
    mats_out.sort(key=lambda m: (-len(m['p']), -m['best'], m['n']))
    albums_out = []
    for slug, a in sorted(A.items(), key=lambda kv: kv[1]['name']):
        tp = 't/%s.jpg' % slug
        t = Image.open(os.path.join(R, a['tile_img']))
        if t.mode in ('RGBA', 'LA', 'P'):
            t = t.convert('RGBA'); bg = Image.new('RGB', t.size, (255, 255, 255)); bg.paste(t, mask=t.split()[-1]); t = bg
        ImageOps.contain(t.convert('RGB'), (400, 400)).save(os.path.join(out, tp), quality=82, optimize=True)
        files.append(tp); albums_out.append({'id': slug, 'name': a['name'], 'tile': tp})
    for m in mats_out: del m['best']
    data = json.dumps({'albums': albums_out, 'mats': mats_out}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    open(os.path.join(out, 'index.html'), 'w').write(open(TEMPLATE).read().replace('/*__DATA__*/null', data))
    json.dump(files, open(os.path.join(out, 'files.json'), 'w'), indent=0)
    half = (len(files) + 1) // 2
    assert half <= 255
    json.dump(files[:half], open(os.path.join(out, 'files_part1.json'), 'w'), indent=0)
    json.dump(files[half:], open(os.path.join(out, 'files_part2.json'), 'w'), indent=0)
    newp = sum(1 for m in mats_out for p in m['p'] if p['r1'] != 2)
    lock = sum(1 for m in mats_out for p in m['p'] if p['r1'] == 2)
    per = collections.Counter(p['a'] for m in mats_out for p in m['p'] if p['r1'] != 2)
    print('mats', len(mats_out), 'new pairs', newp, 'locked round-1 yes', lock, 'files', len(files), 'missing', missing)
    print(sorted(per.items(), key=lambda x: -x[1]))
    return mats_out


if __name__ == '__main__':
    main(*sys.argv[1:7])
