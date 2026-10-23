"""STANDING CHECK (Tiffany Oct 23 2:58pm: "every single tile set from every single partner brand is in here... why aren't
you checking your work?"). Compares every partner store's catalog (Shopify /products.json) with the tiles in the live
Find Your Mat-ch build and lists what is missing, hidden, or not split by colorway.

Rules (hers): a tile set = a full playable mahjong tile set. Each colorway is its own row. Never add travel sets,
replacement/single tiles, mini sets, bags/cases, decor (giant tiles), events/classes, gift cards, stickers.
Usage: python3 builder/fym_tile_audit.py <build_dir> <feeds_dir> [report.md]
 feeds_dir holds <domain>.p1, .p2 ... (raw products.json pages). Exit 0 always; read the report."""
import sys, os, re, json, glob, collections
B, FD = sys.argv[1], sys.argv[2]; OUT = sys.argv[3] if len(sys.argv) > 3 else None
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
T = D['tiles']; S = {s['tile']: s for s in D['sets']}
nd = lambda d: d.replace('www.', '')
app = collections.defaultdict(dict)  # domain -> handle -> [(key, visible)]
for k, t in T.items():
    if '/' not in k: continue
    dom, rest = k.split('/', 1); hnd = rest.split('?')[0]
    s = S.get(k); vis = bool(s) and not s.get('hid') and not t.get('hid')
    app[nd(dom)].setdefault(hnd, []).append((k, vis, t.get('n')))
TILE = re.compile(r'\b(tiles?|tile set|mahjong set|mah ?jongg? set|american mahjong)\b', re.I)
NOT = re.compile(r'\b(travel|mini|replacement|single|extra|spare|bag|pouch|case|tote|sticker|decal|mat|mats|rack|racks|pusher|coaster|card|cards|charm|earring|necklace|bracelet|shirt|tee|sweatshirt|hat|ornament|gift ?card|blank|sample|towel|napkin|decor|giant|event|tasting|class|lesson|book|dice|display box|tray|riichi|chinese|rummy|domino|keychain|magnet|candle|scarf|twilly|coaster|playing|score|pin|bundle add|add-on|upgrade|deposit|wholesale|gift wrap|insurance|joker set|wind set|flower set|flower tiles|shufflers?|guide|kids|little mahj|cabinet|credenza|sideboard|dresser|mug|cup|runner|pants|dress|muumuu|wallet|satchel|handbag|clutch|chair|plate|pajama|sleepwear|invitation|community night|needle|canvas|coasters?|tassel|acrylic|box|traveler)\b', re.I)
COLOPT = re.compile(r'colou?r|style|colorway|design|edition|tile', re.I)
BOXISH = re.compile(r'box|bag|velvet|lucite|case|pouch|acrylic|without|with |no box|size|qty|quantity', re.I)
rows = []; summary = []
for f in sorted(glob.glob(FD + '/*.p1')):
    dom = os.path.basename(f)[:-3]; prods = []
    for pf in sorted(glob.glob(os.path.join(FD, dom + '.p*'))):
        try: prods += json.load(open(pf)).get('products', [])
        except Exception: pass
    have = app.get(nd(dom), {}); miss = hid = split = 0
    for p in prods:
        title = p['title']; pt = p.get('product_type') or ''
        if not (TILE.search(title) or re.search(r'tile', pt, re.I)) or NOT.search(title): continue
        if not any(v.get('available', True) for v in p['variants']): continue  # sold out everywhere: still listed? keep simple: skip unavailable
        cols = []
        for o in p.get('options', []):
            if COLOPT.search(o['name']) and len(o['values']) > 1 and not all(BOXISH.search(v) for v in o['values']):
                cols = [v for v in o['values'] if not BOXISH.search(v)]; break
        got = have.get(p['handle'], [])
        if not got:  # same set under another handle/key (e.g. album keys): match on name words
            words = lambda x: set(re.findall(r'[a-z]{3,}', x.lower())) - {'mahjong', 'american', 'tile', 'tiles', 'set', 'the', 'series', 'with', 'and', 'mahj', 'that'}
            tw = words(title)
            for hd2, lst in have.items():
                for k2, v2, n2 in lst:
                    nw = words(n2 or '')
                    if nw and nw <= tw: got = got + [(k2, v2, n2)]
        if not got: rows.append((dom, 'MISSING', title, ', '.join(cols) or '-', p['handle'])); miss += 1; continue
        if not any(v for _, v, _ in got): rows.append((dom, 'HIDDEN', title, ', '.join(cols) or '-', p['handle'])); hid += 1
        if len(cols) > 1 and len(got) < len(cols): rows.append((dom, f'COLORWAYS {len(got)}/{len(cols)}', title, ', '.join(cols), p['handle'])); split += 1
    summary.append((dom, len(prods), miss, hid, split))
lines = ['# Tile set audit: partner stores vs Find Your Mat-ch', '', '| Brand site | products | missing | hidden | colorways not split |', '|---|---|---|---|---|']
lines += [f'| {d} | {n} | {m} | {hh} | {sp} |' for d, n, m, hh, sp in summary]
lines += ['', '| Brand site | Problem | Store title | Colorways | handle |', '|---|---|---|---|---|'] + [f'| {d} | {k} | {t} | {c} | {hd} |' for d, k, t, c, hd in rows]
rep = '\n'.join(lines); print(rep)
if OUT: open(OUT, 'w').write(rep + '\n')
