#!/usr/bin/env python3
"""Album missed-mats audit (Nov 7 2026; Tiffany 8:28pm: catalog gaps snowball into the albums).

For every LIVE tile-set match album: the mats it never got to consider =
  (a) never-in-catalog mats now staged for FYM 1.18 (config/fym-shopmy-nov07.json + config/fym-amazon-holiday-oct26.json)
  (b) FYM v117 mats whose `add` tag is dated AFTER the album's build date (CUTOFF below; untagged = original catalog = seen)
minus mats already on the live album page (name / product handle) or in the FYM set's match list.
Colour-score each against the set's tile profile (config/tile-tones.json back/signature/layer shades + colorcards faces),
using measured shades (CIEDE2000, scripts/colors/palette.py), the tone gate (doc 76) and the back-colour family rule.
Writes a ranked shortlist (top N per album) to the scratch JSON given; the by-eye pass happens on contact sheets
(scripts/audits/album_missed_sheets_nov07.py).

Usage: python3 scripts/audits/album_missed_mats_nov07.py <albums_html_dir> <fym_index.html> <out.json> [N]
"""
import json, os, re, sys, html
import numpy as np
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(R, 'scripts/colors'))
import palette as P
import families as F

# album slug -> (album index name, tile-tones key, FYM set slug, build cutoff MM-DD)
# Cutoffs: albums built before the FYM catalog grew (Oct 16+) = 10-15; Papaya Spritz staged Oct 18 from the Oct 17 pool;
# the 4 vault albums Oct 21; the 9 thin albums got her hearts from the Oct 23-24 review (pool ~Oct 22);
# Malachite Oct 20; Brownstone Bloom + Sunday Tile Set swipe books rebuilt from the widest pool Oct 29.
ALB = {
 'papaya-spritz': ('Papaya Spritz', 'papayaspritz', 'oh-my-mahjong-papaya-spritz', '10-17'),
 'amara': ('Amara', 'amara', 'amara', '10-15'), 'birdie': ('Birdie', 'birdie', 'birdie', '10-15'),
 'brownstone-bloom': ('Brownstone Bloom', 'brownstonebloom', 'anders-ruff-brownstone-bloom', '10-29'),
 'coquette': ('Coquette', 'coquette', 'coquette', '10-15'), 'dandy': ('Dandy', 'dandy', 'dandy', '10-15'),
 'drake': ('Drake', 'drake', 'drake', '10-15'), 'emerald': ('Emerald', 'emerald', 'emerald', '10-15'),
 'gatsby': ('Gatsby', 'gatsby', 'gatsby', '10-15'), 'gemma': ('Gemma', 'gemma', 'gemma', '10-22'),
 'glitterville': ('Glitterville', 'glitterville', 'glitterville', '10-15'),
 'glow-wild': ('Glow Wild', 'glowwild', 'glow-wild', '10-15'),
 'heritage-2-0': ('Heritage 2.0', 'heritage20', 'heritage-2-0', '10-15'),
 'heritage': ('Heritage', 'heritage', 'heritage', '10-15'), 'jade': ('Jade', 'jade', 'jade', '10-15'),
 'jasmine': ('Jasmine', 'jasmine', 'jasmine', '10-22'), 'la-fete': ('La Fete', 'lafete', 'la-fete', '10-15'),
 'lagoon': ('Lagoon', 'lagoon', 'lagoon', '10-15'),
 'lilac-soiree': ('Lilac Soiree (retired)', 'lilacsoiree', None, '10-21'),
 'limoncello': ('Limoncello', 'limoncello', 'limoncello', '10-22'), 'lola': ('Lola', 'lola', 'lola', '10-15'),
 'luminaire': ('Luminaire', 'luminaire', 'luminaire', '10-15'),
 'malachite': ('Malachite', 'malachite', 'malachite', '10-20'),
 'moonlight': ('Moonlight', 'moonlight', 'moonlight', '10-15'),
 'nantucket': ('Nantucket', 'nantucket', 'nantucket', '10-22'), 'osler': ('Osler', 'osler', 'osler', '10-22'),
 'palm-royale': ('Palm Royale', 'palmroyale', 'palm-royale', '10-15'),
 'pearlescent': ('Pearlescent', 'pearlescent', 'pearlescent', '10-15'), 'pippa': ('Pippa', 'pippa', 'pippa', '10-22'),
 'preppy-soiree': ('Preppy Soiree (retired)', 'preppysoiree', None, '10-21'),
 'seabreeze': ('Seabreeze', 'seabreeze', 'seabreeze', '10-15'),
 'shangri-la': ('Shangri-la (retired)', 'shangrila', None, '10-21'), 'sierra': ('Sierra', 'sierra', 'sierra', '10-15'),
 'smith': ('Smith', 'smith', 'smith', '10-15'), 'solara': ('Solara', 'solara', 'solara', '10-15'),
 'sorbet': ('Sorbet', 'sorbet', 'sorbet', '10-22'),
 'spring-love': ('Spring Love (retired)', 'springlove', None, '10-21'),
 'sunday-tile-set': ('Sunday Tile Set', 'sundaytileset', 'sunday-mahjong-sunday', '10-29'),
 'sunset': ('Sunset', 'sunset', 'sunset', '10-22'), 'talulah': ('Talulah', 'talulah', 'talulah', '10-15'),
 'taylor': ('Taylor', 'taylor', 'taylor', '10-22'), 'tortoise': ('Classic Tortoise', 'classictortoise', 'tortoise', '10-15'),
 'willow': ('Willow', 'willow', 'willow', '10-15'),
}
CC_KEY = {'papaya-spritz': 'papaya-spritz', 'shangri-la': 'shangri-la', 'lilac-soiree': 'lilac-soiree',
          'preppy-soiree': 'preppy-soiree', 'spring-love': 'spring-love', 'sunday-tile-set': 'sunday-tile-set',
          'brownstone-bloom': 'brownstone-bloom'}
BAN = re.compile(r'mahjong studios|paige spearin', re.I)
EXCL = re.compile(r"travel|\bmini\b|starter|\bkit\b|bundle|caddy|desk mat|table cover|foldable|solo play|\bpool\b(?! pawty)|"
                  r"logo mat|\bbag\b|pet mat|bath mat|gift card|sample", re.I)
MON = {'oct': 10, 'nov': 11}
# tile-tones profile fixes found by LOOKING at the album tile photo (Nov 7): Malachite's backs are dark green malachite
# (#445344, measured 21%); tile-tones had the blush faces/layer as the back, which pulled pink mats.
FIX = {'malachite': {'back_hex': '#445344', 'back_colors': ['green'], 'signature': ['#445344', '#7b3e43', '#d0b1b9'],
                     'layer_hex': ['#7b3e43'], 'tone': 'transitional'}}


def add_date(tag):
    if not tag: return None
    m = re.search(r'(oct|nov)(\d{2})', tag)
    return '%02d-%02d' % (MON[m.group(1)], int(m.group(2))) if m else None


def norm(s):
    s = html.unescape(s or '').lower().replace('é', 'e').replace('&', 'and')
    s = re.sub(r'\b(mahjong|mahjongg|mahj|mat|mats|double[- ]sided|neoprene|vegan leather|the)\b', ' ', s)
    return re.sub(r'[^a-z0-9]', '', s)


def album_cards(path):
    t = open(path, encoding='utf-8', errors='ignore').read()
    out = []
    for fig in re.findall(r'<figure class="mm3-c.*?</figure>', t, re.S):
        h3 = re.search(r'<h3>(.*?)</h3>', fig, re.S); by = re.search(r'mm3-by">(?:Mat by )?(.*?)</span>', fig, re.S)
        href = re.search(r'class="mm3-btn" href="([^"]+)"', fig)
        name = html.unescape(re.sub('<[^>]+>', '', h3.group(1))).split(' + ', 1)[-1].strip() if h3 else ''
        brand = html.unescape(re.sub('<[^>]+>', '', by.group(1))).strip() if by else ''
        u = href.group(1) if href else ''
        hm = re.search(r'/products/([^/?%"]+)', html.unescape(u)) or re.search(r'redirect=%2Fproducts%2F([^%&"]+)', u) \
            or re.search(r'/listing/(\d+)', u) or re.search(r'/dp/([A-Z0-9]{10})', u)
        out.append({'name': name, 'brand': brand, 'handle': hm.group(1) if hm else '', 'u': u})
    return out


def fam_shares(pal):
    """[(hex,w)] -> {family: share} using the same family wheel as the catalog (families.fam_arr)."""
    out = {}
    for h, w in pal:
        L = P.lab(h)
        if float(np.hypot(L[1], L[2])) < 18:  # greys, creams, beiges, near-blacks = neutral, never a colour family
            f = 'dark' if L[0] < 30 else 'neutral'; out[f] = out.get(f, 0) + w; continue
        f = str(F.fam_arr(P.hex2rgb(h).reshape(1, 3))[0][0])
        f = {'gold': 'yellow', 'white': 'neutral', 'black': 'dark'}.get(f, f)
        out[f] = out.get(f, 0) + w
    return out


def cover(target, pal, near=11, far=19):
    c = 0.0
    for h, w in pal:
        d = P.dE(target, h)
        c += w if d < near else (w * 0.5 if d < far else 0)
    return c


def chroma(pal):
    num = den = 0
    for h, w in pal:
        L = P.lab(h); c = float(np.hypot(L[1], L[2]))
        if c > 8: num += c * w; den += w
    return num / den if den else 0


def score(prof, pal, mf):
    if not pal: return 0, {}
    back = prof['back_hex']; sig = [h for h in prof['signature'] if h != back]
    lay = prof['layer_hex']; faces = prof['faces']
    cb = cover(back, pal) if back else 0
    fs = fam_shares(pal)
    backfam = prof['back_colors']
    if 'neutral' in backfam: backfam = backfam + ['neutral']
    fam_share = sum(fs.get(c if c != 'teal' else 'teal', 0) for c in backfam)
    prim = (mf or [None])[0]
    qualifies = cb >= 0.1 or (prim in backfam and fam_share >= 0.2) or fam_share >= 0.3
    if not qualifies: return 0, {'cb': round(cb, 2), 'fam': round(fam_share, 2)}
    s = 2.0 * min(cb, 0.45) / 0.45 + 1.0 * min(fam_share, 0.5) / 0.5
    s += 0.6 * sum(min(cover(h, pal), 0.25) / 0.25 for h in sig[:2])
    s += 0.5 * sum(min(cover(h, pal), 0.2) / 0.2 for h in lay[:2])
    s += 0.25 * sum(min(cover(h, pal, 12, 18), 0.15) / 0.15 for h in faces[:4])
    # tone gate (doc 76): clean tile never on an earthy/muted mat, earthy tile never on a bright/clean mat
    ch = chroma(pal); tone = prof['tone']; t = 1.0
    if tone == 'clean' and ch < 16 and 'neutral' not in prof['back_colors']: t = 0.35
    if tone == 'earthy' and ch > 48: t = 0.4
    # clash: a big share of a colour family that is nowhere in the tile (back/layers/faces)
    tile_fams = set(backfam) | set(prof['fams_all']) | {'neutral', 'dark'}
    clash = sum(v for f, v in fs.items() if f not in tile_fams)
    s -= 2.5 * max(0, clash - 0.12)
    return round(max(0, s) * t, 3), {'cb': round(cb, 2), 'fam': round(fam_share, 2), 'ch': round(ch), 'clash': round(clash, 2)}


def main(adir, fym_html, out, N=12):
    T = json.load(open(os.path.join(R, 'config/tile-tones.json')))['sets']
    CC = json.load(open(os.path.join(R, 'config/colorcards.json')))['sets']
    IDX = json.load(open(os.path.join(R, 'assets/tiles/album/index.json')))
    s = open(fym_html).read(); i = s.find('const D='); D, _ = json.JSONDecoder().raw_decode(s[i + 8:])
    M = D['mats']; SETS = {x['slug']: x for x in D['sets']}
    fym_dir = os.path.dirname(fym_html)
    cands = []
    for k, m in M.items():
        ad = add_date(m.get('add'))
        if not ad: continue
        if m.get('hid') or m.get('rt') or m.get('oos') or m.get('so') or m.get('parked') or m.get('u_dead'): continue
        if BAN.search(m.get('bn', '') + ' ' + m.get('n', '')) or EXCL.search(m.get('n', '') + ' ' + k): continue
        if m.get('bn') == 'Splash of Color': continue  # Oct 26: only her album-match Splash mats stay
        cands.append({'key': k, 'name': m['n'], 'brand': m['bn'], 'src': 'FYM ' + m.get('add'), 'add': ad,
                      'pa': bool(m.get('pa')), 'hol': bool(m.get('hol')) and not m.get('ayr'),
                      'img': os.path.join(fym_dir, m['f']), 'pal': m.get('ms') or [], 'mf': m.get('mf') or [],
                      'url': m.get('u0') or m.get('u')})
    pal_cache_p = os.path.join(os.path.dirname(out), 'staged_palettes.json')
    pc = json.load(open(pal_cache_p)) if os.path.exists(pal_cache_p) else {}
    for f, tag in (('config/fym-shopmy-nov07.json', 'staged ShopMy (never in catalog)'),
                   ('config/fym-amazon-holiday-oct26.json', 'staged Amazon holiday pick (never in catalog)')):
        for m in json.load(open(os.path.join(R, f)))['mats']:
            if m.get('hid'): continue
            img = os.path.join(R, m['img'])
            if m['key'] not in pc: pc[m['key']] = P.mat_palette(img, k=7, keep=7)
            pal = pc[m['key']]; fs = fam_shares(pal)
            mf = [x for x, _ in sorted(fs.items(), key=lambda kv: -kv[1]) if x not in ('neutral', 'dark')]
            cands.append({'key': m['key'], 'name': m['name'], 'brand': m['brand'], 'src': tag, 'add': '11-07',
                          'pa': False, 'hol': bool(m.get('hol')), 'img': img, 'pal': pal, 'mf': mf, 'url': m.get('u')})
    json.dump(pc, open(pal_cache_p, 'w'))
    res = {}
    for slug, (iname, tkey, fslug, cut) in ALB.items():
        if os.environ.get('ONLY') and slug not in os.environ['ONLY'].split(','): continue
        t = dict(T[tkey], **FIX.get(slug, {})); cc = CC.get(CC_KEY.get(slug, ''), {})
        faces = [h for _, h in cc.get('faces', [])] or []
        lay = list(t.get('layer_hex') or []) + [h for _, h, kind in cc.get('backs', []) if kind != 'solid back']
        fams_all = list(t.get('layer_colors') or []) + list(t.get('face_colors') or [])
        for h in faces + lay:
            f = str(F.fam_arr(P.hex2rgb(h).reshape(1, 3))[0][0]); fams_all.append({'gold': 'yellow'}.get(f, f))
        prof = {'back_hex': t.get('back_hex'), 'signature': t.get('signature') or [], 'layer_hex': lay[:3], 'faces': faces,
                'back_colors': list(t.get('back_colors') or []), 'tone': t.get('tone'), 'fams_all': fams_all}
        cards = album_cards(os.path.join(adir, slug + '.html'))
        have_n = {norm(c['name']) for c in cards}; have_h = {c['handle'].lower() for c in cards if c['handle']}
        fm = {x[0] for x in (SETS.get(fslug) or {}).get('m', [])} if fslug else set()
        rows = []
        for c in cands:
            if c['add'] <= cut: continue
            h = c['key'].split('/')[-1].lower()
            hid = re.search(r'/listing/(\d+)', c['key']); asin = re.search(r'/dp/([A-Z0-9]{10})', c['key'])
            if c['key'] in fm or norm(c['name']) in have_n or h in have_h or (hid and hid.group(1) in have_h) \
                    or (asin and asin.group(1).lower() in have_h):
                continue
            sc, why = score(prof, c['pal'], c['mf'])
            if sc <= 0: continue
            rows.append(dict(c, score=sc, why=why))
        rows.sort(key=lambda r: -r['score'])
        reg = [r for r in rows if not r['hol']][:N]; hol = [r for r in rows if r['hol']][:4]
        res[slug] = {'name': iname, 'tile_img': IDX[iname]['file'], 'cutoff': '2026-' + cut, 'album_cards': len(cards),
                     'never_seen_pool': sum(1 for c in cands if c['add'] > cut), 'qualified': len(rows),
                     'profile': prof, 'shortlist': reg + hol}
        print(f"{slug:18} cards={len(cards):3} pool={res[slug]['never_seen_pool']:4} qualified={len(rows):4}")
    if os.environ.get('ONLY') and os.path.exists(out):
        old = json.load(open(out)); old.update(res); res = old
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 12)
