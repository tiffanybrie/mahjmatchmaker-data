"""Petalee (Virora Mahjong) album draft: one card per YES mat in her Petalee swipe book (artifact JMaCDUwEZf528PX13x9mKa,
db 'petalee', 39 yes of 110 votes as of Oct 18 ~7am; she may still be swiping). Deck order (no stars in this book).
Title colour #FBB1D7 = the tile-back pastel pink (her rule). Tile photo assets/tiles/album/petalee-pile.jpg; Virora logo flag.
Tile racks (Claude's pick, needs her OK; no final_lists entry): her layer-colour rule (lavender + pale green layers) plus a
feminine neutral: Miss Mahjong Scalloped Iridescent Opal, Bird & Bamboo Lavender, Peace Love Mahjong Chartreuse (B&B Pistachio rendered khaki).
Photo overrides: Pink Floral Chinoiserie = the registry's flat close-up, crop as the approved Oct 18 PFC cards; Parrotia and Roseveil = Virora's
first listing photo (flat mat, rolled mat at right is cropped off by the lower-left crop); book photos had tiles and a size ruler.
Mat racks: config/mat-racks-picks.json registry when listed, else matpick.py.
Usage: python3 petalee_build.py <workdir>; then gen2.py <workdir>/spec.json <workdir>/cards"""
import json, io, base64, re, os, sys, glob
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
S = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
W = sys.argv[1]
SPEC = json.load(open(S + 'petalee/petalee_spec.json'))
H = open(S + 'petalee/book/index.html').read()
IMG = dict(re.findall(r'\{"id": ?"([^"]+)"[^{}]*?"img": ?"(m/\d+\.jpg)"', H))
LAB = {x['id']: x.get('label', '') for x in SPEC['items']}
LAB.update({k: v for k, v in re.findall(r'\{"id": ?"([^"]+)", ?"label": ?"([^"]*)"', H)})
POOL = {}
for f in glob.glob(S + 'petalee/book/pool*.js'):
    for k, lab, img in re.findall(r'\{"id": ?"([^"]+)", ?"label": ?"([^"]*)", ?"img": ?"(data:image/[^"]+)"', open(f).read()):
        POOL[k.split('?')[0]] = (lab, img)
votes = {}
for f in glob.glob(S + 'petaleedb/petalee/*.json'):
    j = json.load(open(f)); votes[j['i']] = j['v']
deck = [x['id'] for x in SPEC['items']]
deck_ids = [k.split('?')[0] for k in deck] + [k for k in IMG if k.split('?')[0] not in [d.split('?')[0] for d in deck]]
yes = [k for k in dict.fromkeys(deck_ids) if votes.get(k) == 'y'] + [k for k, v in votes.items() if v == 'y' and k not in deck_ids]
TRACKS = ['Miss Mahjong Scalloped Iridescent Opal', 'Bird & Bamboo Lavender', 'Peace Love Mahjong Chartreuse']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
PARTNERS = {b[0] for b in json.load(open(R + 'work/pub/catalog.json'))['B']}
PCT = {'Britt Mills': '15%', 'Amanda Toppe': '20%', 'Royal Mahjong Society': '15%'}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
ALIAS = {'Amanda Toppe': 'Amanda Toppe', 'Bird and Bamboo': 'Bird & Bamboo'}
NAME = {'Botanical Garden Mahjong Mat': 'Botanical Garden', 'Garden Party Mahjong Mat': 'Garden Party', 'The Paradise Mahjong Mat': 'Paradise Blue Bliss',
        'Beautiful Beginnings: A New Mahjong Player’s Mat': 'Beautiful Beginnings', 'A Mahjong Soirée Mahjong Mat': 'A Mahjong Soirée',
        'Posy Pop Watercolor Floral Mahjong Mat': 'Posy Pop Watercolor', 'Hummingbird Hydrangea Mahjong Mat': 'Hummingbird Hydrangea',
        'Roseveil Mahjong Mat': 'Roseveil', 'Hey Baby Mahjong Mat': 'Hey Baby', 'Martha & Mae Vintage Quilt': 'Martha & Mae'}
def footer(b, retired):
    if retired or (b not in PARTNERS and b not in PCT): return 'SHOP THE MATCH : MAHJMATCHMAKER.COM'
    if b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return f"{PCT.get(b, '10%')} OFF  USE CODE : MAHJMATCH"
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im):
    im = flat(im); Wd, Hh = im.size; z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / .973)
    if ch > Hh: ch = Hh; cw = int(ch * .973)
    return im.crop((0, Hh - ch, cw, Hh))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '')).strip('-')
OVR = {'tt-mahjsquad-pink-floral-chinoiserie': R + 'assets/mats/mahj-squad/pink-floral-chinoiserie-flat-closeup-WATERMARKED-no-social.jpg',
       'cc-parrotia': R + 'assets/mats/virora-mahjong/parrotia.jpg', 'cc-roseveil': R + 'assets/mats/virora-mahjong/roseveil.jpg'}
def find_img(k):
    if k in OVR: return Image.open(OVR[k]), OVR[k].replace(R, '')
    for kk, p in IMG.items():
        if kk.split('?')[0] == k: return Image.open(S + 'petalee/book/' + p), 'book/' + p
    if k in POOL: return Image.open(io.BytesIO(base64.b64decode(POOL[k][1].split(',', 1)[1]))), 'pool'
    return None, None
def label(k):
    for kk, l in LAB.items():
        if kk.split('?')[0] == k and l: return l
    return POOL.get(k, ('',))[0]
cards, man, held = [], [], []
for k in yes:
    src, sp = find_img(k)
    lab = label(k).replace('From Tiles & Tablescapes · ', '')
    parts = [p.strip() for p in lab.split(' · ')]
    nm = parts[0] if parts else k; brand = ALIAS.get(parts[-1], parts[-1]) if len(parts) > 1 else ''
    nm = re.sub(r'\s*[–-]\s*.*$', '', nm) if len(nm) > 40 else nm
    nm = NAME.get(nm, re.sub(r'\s+Mahjong Mat$', '', nm)); brand = re.sub(r'\s*\(.*\)$', '', brand)
    retired = '(retired)' in nm or k.startswith('ret-'); clean = re.sub(r'\s*\(.*', '', nm).strip()
    if src is None: held.append({'vote_id': k, 'why': 'no photo found'}); continue
    m = crop(src) if k != 'tt-mahjsquad-pink-floral-chinoiserie' else flat(src).crop((0, 0, 838, 861))
    rk = next((kk for kk, v in REG.items() if slug(clean) == kk), None)
    mr = REG[rk]['racks'] if rk else pick(m, exclude=TRACKS)
    fn = f"petalee-mahjong-tiles-{slug(brand)}-{slug(clean)}-mat.jpg"; code = footer(brand, retired); n = len(cards) + 1
    cards.append({'slug': f'pet{n:02d}', 'title': f'Petalée + {clean}', 'col': '#FBB1D7', 'tile_file': 'assets/tiles/album/petalee-pile.jpg',
                  'tile_brand': 'Virora Mahjong', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m)})
    man.append({'order': n, 'vote_id': k, 'mat': clean, 'brand': brand, 'retired_mat': retired, 'holiday': False, 'file': fn, 'code': code,
                'src': sp, 'racks': TRACKS, 'mat_racks': mr, 'mat_reg': rk})
json.dump({'_note': 'Petalee album draft v1 (Oct 18)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Virora Mahjong'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Petalée', 'cards': man, 'held': held, 'title_color': '#FBB1D7', 'tile': 'assets/tiles/album/petalee-pile.jpg',
           'racks_note': 'tile racks = Claude pick pending her OK'}, open(W + '/manifest.json', 'w'), indent=1)
print(len(cards), 'cards', len(held), 'held'); print([ (c['mat'], c['brand']) for c in man])
