"""Thin-album shortlists (Oct 21). Pool = mats new to FYM since the Oct 18 7:37am snapshot (Oct 20 ShopMy/Etsy/Tala/Mahj & Vine adds +
new partner mats), visible in FYM (partner/allowed, photo flags passed), not holiday, not already in the set's match list.
Ranked by the FYM colour rank, then Claude looked at every candidate next to the album tile photo and dropped weak ones (doc 76 clean vs earthy).
Kerry excluded where she already matched it (Sorbet, Taylor) or dropped it (Jasmine)."""
import json, re, sys
R = '/home/claude/mahjmatchmaker-data/'
P = {
 'sorbet': ['Colony - Chartreuse & Petal Pink', 'Cabana - Pink & Ivory with Citrus Fringe', 'Peony and Parasol', 'Katelyn (Yellow)',
            'Cabana - Seafoam Blue & Ivory with Citrus Fringe', 'Caroline (Preppy)', 'Nora', 'Chinoiserie Citrus Grove', 'Brinkley'],
 'sunset': ['Pink Tiger', 'Brooke', 'Fall Flowers', 'Betty Floral (Monogrammed Neoprene)', 'Elizabeth', 'Cheeky Cockatoo',
            'Watercolor Floral', 'Pink Orchids', 'Chinoiserie Elephant with Pagodas', 'Dogs Playing Mahjong'],
 'limoncello': ['Colony - Chartreuse & Petal Pink', 'Cabana - Seafoam Blue & Ivory with Citrus Fringe', 'Cabana - Pink & Ivory with Citrus Fringe',
            'Pink Orchids', 'Katelyn (Yellow)', 'The Kerry', 'Brinkley', 'Chinoiserie Elephant with Pagodas'],
 'gemma': ['Cheetah in Chinoiserie', 'Livy', 'Allie (Purple)', 'Midori Shadows', 'Pink Orchids', 'Chinoiserie Elephant with Pagodas',
            'Preppy Monkeys', 'Whimsical Chinoiserie Meeting in the Pavilion', 'Nichole'],
 'taylor': ['Livy', 'Nora', 'Caroline (Preppy)', 'Cabana - Sage & Ivory with Cantaloupe Fringe', 'Watercolor Floral', 'Nichole',
            'Elizabeth', 'Peony and Parasol', 'Brinkley', 'Whimsical Chinoiserie Meeting in the Pavilion'],
 'jasmine': ['Cheetah in Chinoiserie', 'Allie (Purple)', 'Midori Shadows', 'Pink Orchids', 'Whimsical Chinoiserie Meeting in the Pavilion',
            'Tracing the Tides', 'Chinoiserie Citrus Grove', 'Nichole', 'Benjamin'],
 'nantucket': ['Winslow 1920 Rouge', 'Midori Shadows', 'Pink Orchids', 'Chinoiserie Elephant with Pagodas',
            'Whimsical Chinoiserie Meeting in the Pavilion', 'Nichole'],
 'pippa': ['Peony and Parasol', 'Katelyn (Yellow)', 'Cabana - Seafoam Blue & Ivory with Citrus Fringe', 'Colony - Chartreuse & Petal Pink',
            'Cabana - Pink & Ivory with Citrus Fringe', 'Nora', 'Caroline (Preppy)', 'Pink Peonies', 'Watercolor Floral', 'Brinkley',
            'Chinoiserie Citrus Grove'],
 'osler': ['Winslow 1920 Navy', 'Winslow 1920 Rouge', 'Gatsby', 'The Pavilion - Bamboo Neutral with Blue Fringe', 'The Montecito - Wildflowers',
            'Preppy Monkeys', 'Whimsical Chinoiserie Meeting in the Pavilion', 'Chinoiserie Citrus Grove'],
}
D = json.load(open(sys.argv[1])); V = set(json.load(open(sys.argv[2])))
G = {}
for rid, n, b, u in re.findall(r'\["([a-z0-9-]+--[a-z0-9-]+)","((?:[^"\\]|\\.)*)","((?:[^"\\]|\\.)*)","([^"]*)"', open(R + 'site/livepatch/matgallery/matgallery-v5.html').read()):
    G.setdefault(n, []).append((rid, b, u))
out = {}
for s, names in P.items():
    S = next(x for x in D['sets'] if x['slug'] == s); inm = {e[0] for e in S['m']}
    rows = []
    for n in names:
        ks = [k for k in V if D['mats'][k]['n'] == n]
        assert len(ks) == 1, (s, n, ks)
        k = ks[0]; m = D['mats'][k]
        assert not m.get('hid') and not m.get('hol'), (s, n)
        if k in inm: print('  already her match, skipped:', s, n); continue
        g = [r for r in G.get(n, []) if r[1].lower()[:4] in (m['b'] + m['bn']).lower() or True]
        assert g, ('no gallery row', n)
        rid, b, u = g[0]
        rows.append({'key': k, 'name': n, 'brand': m['bn'] if m['bn'] != 'mahjandvine.com' else 'Mahj & Vine', 'url': u, 'img': f'assets/mats/gallery/{rid}.webp'})
    out[s] = {'name': S['name'], 'maker': S['maker'], 'tc': S['tc'], 'album': S['album'], 'live_count': None, 'mats': rows}
json.dump(out, open('shortlist.json', 'w'), indent=1, ensure_ascii=False)
for s, v in out.items(): print(s, len(v['mats']), [r['brand'] for r in v['mats']][:3])
