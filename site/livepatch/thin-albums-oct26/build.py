"""Thin albums: Tiffany's 41 hearts (thin-album review, artifact UQy4YpGD2RR5Z1WqswJWYM, db 'votes', Oct 23-24) become
match cards appended to 9 live album pages (Tiffany Oct 26 8:01am: "my additional picks for the thin albums ... have not gone
into the match album").
Card = live-album layout (scripts/albumcard/gen2.py): tile photo assets/tiles/album/<set>.jpg, lower-left = the album's tile
racks (config/tile-racks-picks.json final_lists), upper-right = mat racks (config/mat-racks-picks.json when the mat has an entry, else a Claude
matpick kept in the spec as mat_racks), code band 10% OFF USE CODE : MAHJMATCH (OMM tiles).
Mat photo: the cleanest local file (brand flat render) where we have one, else the FYM/gallery photo (assets/mats/thin-oct26).
Shop link = the affiliate link (FYM u: ShopMy / discount / sca_ref); Midori Shadows has no shop link anywhere (no button,
same as the live Malachite card). Fig HTML mirrors the live cards (Kerry pattern, site/livepatch/kerry-oct21).
Usage: python3 build.py            (writes specs, renders cards to assets/cards/thin-oct26, writes <set>.html figure lists)
       python3 build.py <sha>      (only rewrites the figure HTML with jsDelivr URLs at <sha>)"""
import json, os, re, sys, html, subprocess
R = '/home/claude/mahjmatchmaker-data/'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, R + 'scripts/albumcard')
from tdt_policy import card_code, shop_url  # TdT: no visible code on their cards (Oct 30)
P = json.load(open(HERE + '/picks.json'))
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
RU = json.load(open(HERE + '/rackurls.json'))
BBU = {'Bird & Bamboo ' + x['name']: x['url'] for x in json.load(open(R + 'work/bbracks.json'))}
OUT = 'assets/cards/thin-oct26'
SETCOL = {'sorbet': '#e9a926', 'pippa': '#e0478a', 'sunset': '#e8613d', 'limoncello': '#97aa27', 'osler': '#456fbe',
          'jasmine': '#36a272', 'taylor': '#b68ccd', 'gemma': '#40214b', 'nantucket': '#dc282c'}
NOPHOTO = {'Tigre de Tartán Oxblood Scallop'}  # not sold / no photo (scripts/albumcard/real_racks.py)
# better local mat files (clean flat renders) -> (file, crop)
ROT = {k: f'assets/mats/thin-oct26/{v}-r90.jpg' for k, v in {  # Etsy photos with a curled black corner (top right): turned 90 deg so the corner sits under the tile photo
    'www.etsy.com/listing/4506841316/preppy-mahjong-mat-with-white-bag-pink': 'sophie-clima-pink-orchids',
    'www.etsy.com/listing/4530894010/preppy-chinoiserie-elephant-mahjong-mat': 'sophie-clima-chinoiserie-elephant-with-pagodas',
    'www.etsy.com/listing/4497433465/the-katelyn-yellow-mahjong-mat': 'betty-june-jeannette-katelyn-yellow',
    'www.etsy.com/listing/4510347710/the-brooke-mahjong-mat': 'betty-june-jeannette-brooke'}.items()}
LOCAL = {'yolo:pink-tiger': ('assets/mats/yolo-mahjong/pink-tiger-flat-v2.jpg', [8, 8, 732, 732]),
         'goldenpond:midori-shadows': ('assets/mats/golden-pond-mahjong/midori-shadows.jpg', None),
         'splashofcolorco.com/peony-and-parasol': ('assets/mats/splash-of-color/peony-parasol-straight.jpg', None),
         'www.wrenmats.com/watercolor-floral': ('assets/mats/wren-mats/watercolor-floral.jpg', None),
         'ozarkmahjong.com/winslow-1920-rouge-mat': ('assets/mats/ozark-mahjongg/winslow-1920-rouge-mat.jpg', None),
         'ozarkmahjong.com/winslow-1920-original-navy-blue-mat': ('assets/mats/ozark-mahjongg/winslow-1920-original-navy-blue-mat.jpg', None),
         'mahjongco.com/gatsby-mahjong-mat': ('assets/mats/mahjong-by-si/mahjongb-gatsby-mahjong-mat.jpg', None),
         'www.etsy.com/listing/4493549326/the-kerry-mahjong-mat-watercolor-pink': ('assets/mats/etsy/bettyjunejeannette/kerry-2.jpg', [181, 558, 2049, 2429])}
SHORT = {'Colony - Chartreuse & Petal Pink': 'Colony', 'Cabana - Pink & Ivory with Citrus Fringe': 'Pink Cabana',
         'Cabana - Seafoam Blue & Ivory with Citrus Fringe': 'Seafoam Cabana', 'Katelyn (Yellow)': 'Katelyn',
         'Caroline (Preppy)': 'Caroline', 'Chinoiserie Citrus Grove': 'Citrus Grove', 'Betty Floral (Monogrammed Neoprene)': 'Betty Floral',
         'The Kerry': 'Kerry', 'Chinoiserie Elephant with Pagodas': 'Chinoiserie Elephant', 'Allie (Purple)': 'Allie',
         'Cheetah in Chinoiserie': 'Chinoiserie Cheetah', 'Whimsical Chinoiserie Meeting in the Pavilion': 'Whimsical Chinoiserie',
         'Peony and Parasol': 'Peony & Parasol', 'Winslow 1920 Navy': 'Winslow Navy', 'Winslow 1920 Rouge': 'Winslow Rouge',
         'The Pavilion - Bamboo Neutral with Blue Fringe': 'Pavilion'}
SHOP = {'splashofcolorco.com/peony-and-parasol': 'https://splashofcolorco.com/products/peony-parasol-mahjong-mat-sleek-surface?sca_ref=10059443.c9rDRhYNIB31oxJN',
        'mahjandvine.com/citrus-grove': 'https://mahjandvine.com/products/citrus-grove?sca_ref=10366165.hDgHZlY4LYtU0W',
        'www.etsy.com/listing/4506841316/preppy-mahjong-mat-with-white-bag-pink': 'https://go.shopmy.us/p-96130981'}
CODEPAGE = {'Mahj & Vine': '/mahj-and-vine-discount-code', 'Wren Mats': '/wren-mats-discount-code', 'Splash of Color': '/splash-of-color-discount-code'}
RETIRED = {'sorbet', 'taylor'}  # retired OMM sets (kerry-oct21/build.py): the code no longer applies to the tiles themselves
TAKE = {  # one line per card: why the mat goes with the tiles
 ('sorbet', 'Colony'): "Sorbet's lemon and blush in one soft stripe.",
 ('sorbet', 'Pink Cabana'): "Blush stripes and a citrus fringe for Sorbet's sherbet colors.",
 ('sorbet', 'Katelyn'): "Katelyn's shells in pink and lemon on a sunny yellow border.",
 ('sorbet', 'Seafoam Cabana'): "Seafoam stripes cool down Sorbet's yellows, with a citrus fringe to tie them together.",
 ('sorbet', 'Caroline'): "Pastel blossoms in Sorbet's pink, peach and mint.",
 ('sorbet', 'Nora'): "Nora's aqua and coral florals pick up Sorbet's minty and peachy tiles.",
 ('sorbet', 'Citrus Grove'): "Lemons and oranges in a chinoiserie border, right in Sorbet's citrus palette.",
 ('sorbet', 'Brinkley'): "A poolside scene in pink, aqua and lemon, as playful as Sorbet.",
 ('sunset', 'Pink Tiger'): "Coral pink and a golden tiger for Sunset's warm glow.",
 ('sunset', 'Brooke'): "Brooke's coral, peach and pink florals are a Sunset sky.",
 ('sunset', 'Betty Floral'): "Hot pink and coral florals for Sunset's brightest tiles.",
 ('sunset', 'Elizabeth'): "Soft rose and coral, made for Sunset's pink and orange.",
 ('sunset', 'Cheeky Cockatoo'): "A pink cockatoo with tangerine strokes, Sunset's colors exactly.",
 ('limoncello', 'Seafoam Cabana'): "Seafoam stripes with a lemon fringe, a fresh partner for Limoncello.",
 ('limoncello', 'Pink Cabana'): "Pink stripes and a lemon fringe pick up Limoncello's pink and yellow.",
 ('limoncello', 'Kerry'): "The Kerry's leafy greens and blush suit Limoncello's lime and pink.",
 ('limoncello', 'Brinkley'): "Lemon, pink and aqua poolside, as zesty as Limoncello.",
 ('limoncello', 'Chinoiserie Elephant'): "A bright chinoiserie elephant in lime, pink and turquoise.",
 ('gemma', 'Livy'): "Lavender and pink florals for Gemma's jewel-toned purple.",
 ('gemma', 'Allie'): "Purple orchids and hummingbirds over a mint lattice, Gemma's purple and teal.",
 ('gemma', 'Pink Orchids'): "Orchids in magenta and violet with a blue-and-white vase, rich like Gemma.",
 ('taylor', 'Livy'): "Lavender and pink, made for Taylor's lilac tiles.",
 ('taylor', 'Nora'): "Nora's soft florals bring out Taylor's pastel lilac and blush.",
 ('taylor', 'Caroline'): "Pastel blossoms on cream for Taylor's soft palette.",
 ('taylor', 'Elizabeth'): "Elizabeth's rose and lilac pattern is Taylor's colors in a mat.",
 ('jasmine', 'Chinoiserie Cheetah'): "A cheetah in a jungle pavilion, with Jasmine's greens and raspberry pink.",
 ('jasmine', 'Whimsical Chinoiserie'): "A garden pavilion in jade green and pink, Jasmine's two colors.",
 ('jasmine', 'Citrus Grove'): "Leafy greens and bright citrus around a pale center, fresh with Jasmine.",
 ('jasmine', 'Nichole'): "Ginger jars and pink blossoms on green, a chinoiserie mate for Jasmine.",
 ('nantucket', 'Midori Shadows'): "Deep green with cranes and red blossoms, a moody match for Nantucket's red.",
 ('pippa', 'Peony & Parasol'): "Pink peonies and parasols in Pippa's pink, yellow and green.",
 ('pippa', 'Colony'): "Chartreuse and blush stripes, Pippa's sunny yellow and pink.",
 ('pippa', 'Pink Cabana'): "Blush stripes with a citrus fringe for Pippa's pink and yellow.",
 ('pippa', 'Nora'): "Nora's florals in coral, aqua and yellow suit Pippa's brights.",
 ('pippa', 'Caroline'): "Pastel blossoms in Pippa's pink, yellow and green.",
 ('pippa', 'Watercolor Floral'): "Soft watercolor roses in pink and yellow around a calm center.",
 ('pippa', 'Citrus Grove'): "Lemons, oranges and greenery, as sunny as Pippa.",
 ('osler', 'Winslow Navy'): "Navy toile with ivory birds for Osler's deep blues.",
 ('osler', 'Winslow Rouge'): "Rouge toile picks up Osler's burgundy and tan.",
 ('osler', 'Gatsby'): "Denim blue and caning with a green frame, classic like Osler.",
 ('osler', 'Pavilion'): "Bamboo lattice on ivory with a blue fringe, Osler's tan and navy."}


def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def build_cards():
    from matpick import pick
    from PIL import Image
    MF = json.load(open(HERE + '/matfiles.json'))  # key -> slug of the FYM photo in assets/mats/thin-oct26
    MR = json.load(open(R + 'config/mat-racks-picks.json'))
    bymat = {}
    for p in P: bymat.setdefault(p['key'], []).append(p)
    for key, ps in bymat.items():
        f, crop = LOCAL.get(key, (ROT.get(key, f'assets/mats/thin-oct26/{MF[key]}.jpg'), None))
        im = Image.open(R + f).convert('RGB')
        if crop is None: crop = [0, 0, im.width, im.height]
        b0 = ps[0]; mslug = slug(b0['brand'] + ' ' + b0['name'])
        mk = next((k for k, v in MR.items() if isinstance(v, dict) and f in v.get('files', [])), None)
        # no registry entry -> Claude matpick goes in the SPEC (mat_racks), never into config/mat-racks-picks.json (it feeds FYM D.lm)
        mr = None if mk else pick(im.crop(tuple(crop)))
        cards = []
        for p in ps:
            s = p['set']; short = SHORT.get(p['name'], p['name'])
            cards.append({'slug': f'{s}-{mslug}', 'set': s, 'title': f"{p['setname']} + {short}", 'col': SETCOL[s],
                          'tile_file': f'assets/tiles/album/{s}.jpg', 'tilefit': 'cover',
                          'racks': [r for r in F[s] if r not in NOPHOTO],
                          'file': f'{s}-mahjong-tiles-{mslug}-mat.jpg'})
        spec = {'_note': f'thin albums Oct 26: {b0["brand"]} {b0["name"]}', 'mat_file': f, 'mat_crop': crop,
                **({'mat_key': mk} if mk else {'mat_racks': mr}), 'max_racks': 4, 'cards': cards}
        sp = HERE + f'/specs/{mslug}.json'; os.makedirs(HERE + '/specs', exist_ok=True)
        json.dump(spec, open(sp, 'w'), indent=1, ensure_ascii=False)
        subprocess.run(['python3', R + 'scripts/albumcard/gen2.py', sp, R + OUT], check=True)


def rack_links(labels):
    out = []
    for r in labels:
        u = RU.get(r) or BBU.get(r)
        out.append(f'<a href="{html.escape(u)}" target="_blank" rel="sponsored noopener">{html.escape(r)}</a>' if u else html.escape(r))
    return ' · '.join(out)


def figures(sha):
    MR = json.load(open(R + 'config/mat-racks-picks.json'))
    res = {}
    for p in P:
        s = p['set']; short = SHORT.get(p['name'], p['name']); mslug = slug(p['brand'] + ' ' + p['name'])
        spec = json.load(open(HERE + f'/specs/{mslug}.json')); mr = spec.get('mat_racks') or MR[spec['mat_key']]['racks']
        file = f'{s}-mahjong-tiles-{mslug}-mat.jpg'
        shop = shop_url(SHOP.get(p['key']) or p.get('fym_u') or p['url'], p['brand'])
        b = html.escape(p['brand']); by = f'<a href="{CODEPAGE[p["brand"]]}">{b}</a>' if p['brand'] in CODEPAGE else b
        code = card_code(p['brand']) if p['brand'] in CODEPAGE else ''
        tiles = "Oh My Mahjong's current tiles and mats." if s in RETIRED else f"{p['setname']} tiles."
        take = TAKE[(s, short)] + ('' if p['brand'] in CODEPAGE else f" We do not have a code for {p['brand']}; code MAHJMATCH works on {tiles}")
        btn = (f'<a class="mm3-btn" href="{html.escape(shop)}" target="_blank" rel="sponsored noopener">Shop the {html.escape(short)} Mat</a>'
               if shop else '')
        racks = [r for r in F[s] if r not in NOPHOTO]
        racks += [r for r in mr if r not in racks]
        alt = f'Oh My Mahjong {p["setname"]} mahjong tiles with {b} {html.escape(p["name"])} mahjong mat'
        fig = (f'<figure class="mm3-c"><div class="mm3-im"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/{OUT}/{file}" data-lb="" '
               f'alt="{alt}" loading="lazy" width="750" height="938"><a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div>'
               f'<figcaption><span class="mm3-n">NN</span><h3>{html.escape(p["setname"])} + {html.escape(short)}</h3><span class="mm3-by">Mat by {by}</span>'
               f'<div class="mm3-take"><p>{html.escape(take)}</p></div><div class="mm3-l">{btn}{code}</div>'
               f'<div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">Rack matches: {rack_links(racks)}</div></figcaption></figure>')
        res.setdefault(s, {'name': p['setname'], 'album': p['album'], 'figs': [], 'brands': []})
        res[s]['figs'].append(fig); res[s]['brands'].append(p['brand'])
    for s, v in res.items():
        open(HERE + f'/{s}-cards.html', 'w').write(''.join(v['figs']))
    json.dump({s: {'name': v['name'], 'album': v['album'], 'n': len(v['figs']), 'brands': sorted(set(v['brands'])), 'file': f'{s}-cards.html'}
               for s, v in res.items()}, open(HERE + '/manifest.json', 'w'), indent=1)
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1: figures(sys.argv[1])
    else: build_cards()
