"""Propose one TYPE per visible rack (Tiffany Nov 3 2:48pm): wood (Wood tone: natural wood looks, stained / clear-coat wood,
wood-look and burl acrylic), painted (painted wood: most Bird & Bamboo colours, Bam Bird / Virora / My Fair Mahjong colour woods),
acrylic (solid-colour acrylic), clear (clear / translucent / frosted / lucite), tortoise, pearl (pearl / iridescent / opal), metallic
(metallic / gold / silver / glitter). Proposal only; every rack is then checked by eye on contact sheets and corrected in
config/rack-types-nov03.json (by_eye overrides). Usage: python3 rack_types_propose.py <build dir> <out json>"""
import sys, json, re
B, OUT = sys.argv[1:3]; h = open(B + '/index.html').read(); D, _ = json.JSONDecoder().raw_decode(h[h.index('const D=') + 8:])
STAINS = re.compile(r'Bird & Bamboo (White Wood Stain|Clear Wood Stain|Weathered Oak|Provincial|Dark Walnut|Red Mahogany)$')
WOODW = r'wood|wooden|walnut|oak|pine|beech|maple|mahogany|chestnut|camphor|acacia|bamboo|teak|cherry wood'
COLW = r'pink|blue|green|purple|lilac|lavender|teal|navy|red|yellow|orange|white|black|mint|coral|lagoon|indigo|mulberry|periwinkle|slate|olive|aqua|jade|macaron'
out = {}
for k, r in D['racks'].items():
    if r.get('hid'): continue
    n = r['n']; l = n.lower(); rf = r.get('rf') or []
    if STAINS.search(n): t = 'wood'
    elif n.startswith('Bird & Bamboo'): t = 'metallic' if 'Metallic' in n else 'painted'
    elif re.search(r'tortoise|hawksbill', l): t = 'tortoise'
    elif re.search(r'burl', l): t = 'wood'
    elif re.search(r'pearl|iridescent|opal|mother of|shell', l) or 'pearl' in rf: t = 'pearl'
    elif re.search(r'clear|crystal|translucent|frosted|lucite|transparent', l) or 'clear' in rf: t = 'clear'
    elif re.search(r'metallic|gold|silver|glitter|chrome|brass|sparkle', l) or 'metallic' in rf: t = 'metallic'
    elif re.search(WOODW, l) or 'wood' in rf:
        t = 'painted' if re.search(COLW, l) and not re.search(r'natural|walnut|oak|pine|chestnut|beech|maple|mahogany|cherry wood|acacia', l) else 'wood'
    else: t = 'acrylic'
    out[k] = {'n': n, 'bn': r.get('bn', ''), 'type': t}
json.dump(out, open(OUT, 'w'), indent=0)
import collections; print(len(out), collections.Counter(v['type'] for v in out.values()))
