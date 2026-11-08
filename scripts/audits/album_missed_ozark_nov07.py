#!/usr/bin/env python3
"""Ozark Mahjongg album pairs (Nov 7 2026, Tiffany 10:58pm: "that Ozark miss means those mats have to be matched up").
The Ozark line was missed because our links pointed at a parked wrong domain (ozarkmahjong.com); FYM had 4 of 15 mats. This scores
the Ozark mats staged in config/fym-ozark-nov07.json (visible ones; the 4 close-up-only mats are hidden + Questionable and cannot go
on a match card) plus the 4 already in FYM against EVERY live album with round 2's scorer (scripts/audits/album_missed_round2_nov07.py:
no per-album cap, back colour first, hits by count, fit, tone gate), keeps round 2's selection rule (select()), writes
the selected pairs as contact sheets (mat full, album tiles inset bottom-right) for the by-eye pass, and the final file
docs/audits/album-missed-nov07-data/ozark-pairs.json in round2.json's shape, minus the pairs pruned by eye (PRUNE below).
NOTE: every Ozark mat is SOLD OUT on the store (Nov 7); round 2's pool skips sold-out mats, this run does not (her ask), and each
mat carries sold_out so the pick page can say so.
Usage: python3 scripts/audits/album_missed_ozark_nov07.py <albums_html_dir> <fym build dir with the Ozark patch> <sheet_out_dir>
"""
import json, os, sys, collections
from PIL import Image, ImageDraw
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import album_missed_round2_nov07 as R2
from album_missed_mats_nov07 import ALB, CC_KEY, norm, album_cards
from album_missed_sheets_nov07 import font, card

# By-eye pass (pairs LOOKED at on the contact sheets and pulled as clear misses): {album: [mat key, ...]}
PRUNE = json.load(open(os.path.join(R, 'docs/audits/album-missed-nov07-data/ozark-by-eye.json')))['pruned'] \
    if os.path.exists(os.path.join(R, 'docs/audits/album-missed-nov07-data/ozark-by-eye.json')) else {}


def main(adir, build, out_sheets):
    s = open(os.path.join(build, 'index.html')).read(); i = s.find('const D='); D, _ = json.JSONDecoder().raw_decode(s[i + 8:])
    SP = json.load(open(os.path.join(R, 'config/fym-ozark-nov07.json')))
    keys = [m['key'] for m in SP['mats'] if not m['hid']] + list(SP['existing'])
    img = {m['key']: os.path.join(R, m['img']) for m in SP['mats']}
    img.update({k: os.path.join(R, 'assets/mats/ozark-mahjongg', sl + '.jpg') for k, sl in SP['existing'].items()})
    cands = []
    for k in keys:
        m = D['mats'][k]
        if m.get('hid'): continue
        cands.append({'key': k, 'name': m['n'], 'brand': m['bn'], 'pal': m.get('ms') or [], 'url': m.get('u0') or m.get('u'),
                      'img': img[k], 'new': k in {x['key'] for x in SP['mats']}})
    T = json.load(open(os.path.join(R, 'config/tile-tones.json')))['sets']
    CC = json.load(open(os.path.join(R, 'config/colorcards.json')))['sets']
    IDX = json.load(open(os.path.join(R, 'assets/tiles/album/index.json')))
    SETS = {x['slug']: x for x in D['sets']}
    profs = {slug: R2.profile(slug, T, CC, tk) for slug, (_, tk, _, _) in ALB.items()}
    R2.prefill([h for c in cands for h, _ in c['pal']], [h for p in profs.values() for h in p['back'] + p['keys']])
    albums, pairs = {}, []
    for slug, (iname, tkey, fslug, cut) in ALB.items():
        cards = album_cards(os.path.join(adir, slug + '.html'))
        have_n = {norm(c['name']) for c in cards}
        fm = {x[0] for x in (SETS.get(fslug) or {}).get('m', [])} if fslug else set()
        albums[slug] = {'name': iname, 'tile_img': IDX[iname]['file']}
        for c in cands:
            if c['key'] in fm or norm(c['name']) in have_n: continue  # already on the album / her FYM list
            sc, why = R2.score(profs[slug], c['pal'])
            if sc > 0: pairs.append({'album': slug, 'key': c['key'], 'score': sc, 'why': why})
    sel = R2.select({'pairs': pairs})
    # contact sheets per album (mat full, tiles inset), numbered as in ozark-by-eye.json
    os.makedirs(out_sheets, exist_ok=True); C = {c['key']: c for c in cands}
    by = collections.defaultdict(list)
    for p in sel: by[p['album']].append(p)
    W, cols = 300, 5
    for slug, ps in sorted(by.items()):
        ps.sort(key=lambda p: -p['score']); rows = (len(ps) + cols - 1) // cols
        tile = Image.open(os.path.join(R, albums[slug]['tile_img'])).convert('RGB')
        sh = Image.new('RGB', (cols * (W + 8) + 8, 40 + rows * (W + 40)), (240, 238, 232)); dr = ImageDraw.Draw(sh)
        dr.text((10, 10), albums[slug]['name'], fill=(0, 0, 0), font=font(20, True))
        for n, p in enumerate(ps):
            x, y = 8 + (n % cols) * (W + 8), 40 + (n // cols) * (W + 40)
            sh.paste(card(Image.open(C[p['key']]['img']).convert('RGB'), tile, W), (x, y + 34))
            dr.text((x, y + 2), f"{C[p['key']]['name']} {p['score']:.2f} ({p['sel']})", fill=(0, 0, 0), font=font(14, True))
        sh.save(os.path.join(out_sheets, slug + '.jpg'), quality=80)
    keep = [p for p in sel if p['key'] not in set(PRUNE.get(p['album'], []))]
    mats = []
    for c in cands:
        al = [{'album': p['album'], 'album_name': albums[p['album']]['name'], 'score': p['score'], 'round1': 'new', 'why': p['why']}
              for p in sorted(keep, key=lambda p: -p['score']) if p['key'] == c['key']]
        if al: mats.append({'key': c['key'], 'name': c['name'], 'brand': c['brand'], 'partner': False, 'holiday': False, 'url': c['url'],
                            'sold_out': True, 'new_in_fym': c['new'], 'img': os.path.relpath(c['img'], R), 'albums': al})
    per = collections.Counter(p['album'] for p in keep)
    outj = {'date': '2026-11-07', 'round': 'ozark',
            'method': ("Ozark Mahjongg line (missed: our links used the parked ozarkmahjong.com). 7 newly staged visible mats "
                       "(config/fym-ozark-nov07.json) + the 4 already in FYM, scored against all 43 live albums with round 2's scorer and "
                       "selection (scripts/audits/album_missed_ozark_nov07.py; score>=4.3, or within 85% of the mat's best album (>=3.7), "
                       "or top-12 per album (>=3.0)); pairs already on the live album or her FYM list skipped; then a by-eye pass on "
                       "contact sheets (mat full, album tiles inset; assets/qa/ozark-nov07/albums/) pulled clear misses "
                       "(ozark-by-eye.json). Every Ozark mat is SOLD OUT on the store (Nov 7): sold_out true."),
            'summary': {'mats': len(mats), 'new_pairs': len(keep), 'scored_selected': len(sel), 'pruned_by_eye': len(sel) - len(keep),
                        'pairs_per_album': dict(per.most_common())},
            'mats': mats}
    json.dump(outj, open(os.path.join(R, 'docs/audits/album-missed-nov07-data/ozark-pairs.json'), 'w'), indent=1, ensure_ascii=False)
    print('cands', len(cands), 'scored pairs', len(pairs), 'selected', len(sel), 'kept', len(keep))
    for slug, ps in sorted(by.items()): print(slug, [(n, C[p['key']]['name'], p['score']) for n, p in enumerate(ps)])


if __name__ == '__main__':
    main(*sys.argv[1:4])
