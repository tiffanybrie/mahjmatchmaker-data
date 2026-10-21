"""Pick the 'It's a match!' card pairs from Tiffany's REAL album picks (Oct 21).

Inputs
  albums_live.json  live album pages parsed (album order = her order; count = cards on the page)
  D.json            the live FYM app data (const D) for the mat keys, photos and hid/hol/rt flags
Rules (brief + CLAUDE.md)
  - only her album cards, in album order; never invent a pairing
  - skip official pairs (mat brand == tile maker; Coquette = LoveShackFancy x OMM, so both are out)
  - mat brand must be a partner (nonpartner_allow.json partners) minus the banned ones; Paige Spearin x TdT out
  - skip retired mats, holiday mats, and mats hidden in FYM (bad photo / locked out)
  - prefer brands with a verified IG handle (config/social/ig-handles.json): first such card in album order wins;
    fall back to the first partner card without a handle
  - pronoun: male list (brief/doc 00) + Heritage 2.0 (Heritage line; album copy says "he"); sets not clearly
    gendered are skipped (UNCLEAR)
Output: picks.json (list of card dicts for render.py) + skipped list.
Usage: python3 pick.py <albums_live.json> <D.json> <out_dir>
"""
import json, re, sys, os
R = '/home/claude/mahjmatchmaker-data'
A = json.load(open(sys.argv[1])); D = json.load(open(sys.argv[2])); OUT = sys.argv[3]
NPA = json.load(open(f'{R}/builder/fym_flags/nonpartner_allow.json'))
IG = {k: v for k, v in json.load(open(f'{R}/config/social/ig-handles.json')).items() if not k.startswith('_')}
nz = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower().replace('&', 'and').replace('+', 'and'))

BANNED = {nz(b) for b in ['Mahjong Studios', 'The Mahjong Line', 'Mahj House Rules', 'Four Winds Social', 'Amore Mahjong', 'Amore']}
PARTNERS = {nz(b): b for b in NPA['partners']}
ALIAS = {'virora': 'Virora Mahjong', 'mahjongrowandco': 'Mahjong Row & Co.', 'macmiller': 'Mac + Miller Mahjong',
         'mahjandmoon': 'Mahj & Moon'}
IGN = {nz(k): v for k, v in IG.items()}
IGN[nz('Virora Mahjong')] = IG['Virora Mahjong']

MALE = {'malachite', 'heritage', 'heritage-2-0', 'smith', 'cypress-forest', 'gatsby', 'drake'}
UNCLEAR = {'dandy': 'Dandy: not on the male list, and the name reads male; album copy uses no pronoun',
           'osler': 'Osler: surname-style name like Smith/Drake, not on the male list, no pronoun in album copy',
           'taylor': 'Taylor: unisex name, not on the male list, no pronoun in album copy',
           'sunday-tile-set': 'Sunday Tile Set: no gender in the name or album copy'}
SETFYM = {'papaya-spritz': 'oh-my-mahjong-papaya-spritz', 'seabreeze': 'seabreeze'}
TILEIMG = json.load(open(f'{R}/assets/tiles/album/index.json'))
TILEFILE = {'tortoise': 'assets/tiles/album/classic-tortoise-zoom.jpg', 'cypress-forest': 'assets/tiles/album/cypress.jpg'}


def canon_brand(b):
    b = re.sub(r'Holiday$', '', b).strip()
    n = nz(b)
    return ALIAS.get(n, b)


def find_mat(card, brand, setkeys):
    """FYM mat key for an album card: same brand, name equal or contained, preferring the set's own list."""
    want = nz(card['mat']); bn = nz(brand)
    def cands(keys):
        out = []
        for k in keys:
            v = D['mats'].get(k)
            if not v or nz(canon_brand(v['bn'])) != bn: continue
            n = nz(v['n'])
            if n == want: out.insert(0, k)
            elif want and (want in n or n in want) and min(len(n), len(want)) >= 4: out.append(k)
        return out
    c = cands(setkeys) or cands(D['mats'].keys())
    return c[0] if c else None


picks, skipped, seconds_pool = [], [], {}
for a in A:
    slug = a['slug']
    if slug in UNCLEAR:
        skipped.append((slug, UNCLEAR[slug])); continue
    fs = next((s for s in D['sets'] if s['slug'] == SETFYM.get(slug, slug)), None)
    setkeys = [m[0] for m in (fs or {}).get('m', [])]
    makers = {nz(x) for x in re.split(r'\s+x\s+', re.sub(r'Retired tile set', '', a['maker']).strip())}
    ok, why = [], []
    for c in a['cards']:
        raw = c['brand']; brand = canon_brand(raw); bn = nz(brand)
        tag = f"{c['n']} {c['mat']} ({raw})"
        if raw.endswith('Holiday'): why.append(tag + ': holiday'); continue
        if bn in makers: why.append(tag + ': official pair'); continue
        if bn in BANNED or 'paigespearin' in nz(c['mat']): why.append(tag + ': banned brand / no-commission collab'); continue
        if bn not in PARTNERS: why.append(tag + ': not a partner'); continue
        if c['retired']: why.append(tag + ': retired'); continue
        k = find_mat(c, brand, setkeys)
        if not k: why.append(tag + ': no FYM mat photo found'); continue
        v = D['mats'][k]
        if v.get('hid'): why.append(tag + ': hidden in FYM'); continue
        if v.get('hol'): why.append(tag + ': holiday in FYM'); continue
        if v.get('rt'): why.append(tag + ': retired in FYM'); continue
        ok.append(dict(order=int(c['n']), mat=c['mat'], mat_brand=PARTNERS[bn], key=k, f=v['f'], ig=IGN.get(bn),
                       album_img=c['img']))
    if not ok:
        skipped.append((slug, 'no partner non-official match: ' + '; '.join(why[:6]))); continue
    with_ig = [o for o in ok if o['ig']]
    first = (with_ig or ok)[0]
    tile_img = TILEFILE.get(slug) or TILEIMG.get(a['tile'], {}).get('file') or f'assets/tiles/album/{slug}.jpg'
    base = dict(set=slug, tile=a['tile'], tile_brand='Oh My Mahjong' if 'Oh My Mahjong' in a['maker'] and ' x ' not in a['maker'] else re.sub(r'\s*Retired tile set', '', a['maker']),
                tile_ig=IGN.get(nz(re.sub(r'\s*Retired tile set', '', a['maker']).split(' x ')[-1])),
                tile_img=tile_img, count=a['n'], pron='his' if slug in MALE else 'her',
                maker=a['maker'], retired_set='Retired' in a['maker'])
    picks.append({**base, **first, 'rank': 1})
    rest = [o for o in (with_ig or ok) if o['key'] != first['key']]
    seconds_pool[slug] = (base, rest, first)

# second cards: the 10 OMM sets with the most album matches (different mat brand first, still her order)
omm = sorted([s for s in seconds_pool if 'Oh My Mahjong' in A[[x['slug'] for x in A].index(s)]['maker']],
             key=lambda s: -seconds_pool[s][0]['count'])[:10]
for s in omm:
    base, rest, first = seconds_pool[s]
    alt = [o for o in rest if o['mat_brand'] != first['mat_brand']] or rest
    if alt: picks.append({**base, **alt[0], 'rank': 2})
    else: skipped.append((s + ' (2nd card)', 'no second partner match'))

os.makedirs(OUT, exist_ok=True)
json.dump(picks, open(f'{OUT}/picks.json', 'w'), indent=1)
json.dump(skipped, open(f'{OUT}/skipped.json', 'w'), indent=1)
for p in picks: print(p['rank'], p['set'], p['count'], p['pron'], '|', p['order'], p['mat'], '|', p['mat_brand'], '@' + str(p['ig']), '| tile@', p['tile_ig'])
print('cards', len(picks)); [print('SKIP', *s) for s in skipped]
