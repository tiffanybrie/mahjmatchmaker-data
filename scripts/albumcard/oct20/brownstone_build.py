"""Brownstone Bloom (Anders Ruff) album, Oct 20 rebuild from her Ready to Ship notes:
- c5-brownstone (Oct 18 12:20pm): her saved order (41 = cover + 40 mats); "Check resolution of all cards, some are not great.
  Missing AR logo and missing racks for both tiles and mat".
- l-final-brownstone (Oct 18 12:20pm): cancel Jardin, Sedona, Fall Fling, Saddles & Silk, Handbook Plaid, Nantucket Basket,
  Nantucket Rope, Harvest Plaid, Midnight Garden  -> 31 cards.
Resolution: higher-res brand photos where the brand's Shopify page has the same photo bigger (hd_fetch.py), else EDSR x4
super-resolution (<S>EDSR_x4.pb) for the sources whose card crop was under ~830px (4 Anders Ruff mats at 745px, Chinoiserie Round,
and the lower-left crops of Rattan, YOTD White, The Hunt Club).
Logo: tile_brand Anders Ruff (assets/brand/partner-logos/ar.png) instead of the default OMM flag.
Racks (PROPOSAL, needs her OK; no final_lists entry): tile racks = PLM Oak + the face colours (B&B Lilac butterflies,
B&B Moss olive leaves, B&B Wine protea); mat racks = config/mat-racks-picks.json registry when listed, else matpick.py.
Usage: python3 brownstone_build.py <workdir>; then gen2.py <workdir>/spec.json assets/cards/brownstone-bloom-oct20"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'; W = sys.argv[1]; os.makedirs(W, exist_ok=True)
S = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
SRC = '/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/brownstone_v1/src/'
HD = S + 'owedwork/bbhd/img/'
V1 = json.load(open(SRC + '../manifest.json'))
BYNAME = {c['mat']: c for c in V1['cards']}
ORDER = ['Brownstone Bloom', 'Autumn Saffron', 'Mocha Bloom Light', 'Scarlett', 'Rattan', 'Walk in the Park', 'Burgundy Grove', 'Dapper',
         'Moss Grove', 'Marigold', 'Ivy Reverie', 'Flourish', 'Hawthorne', 'Chinoiserie Round', 'Toile de los Muertos', 'Neutre Blanc',
         'Plum Peony', 'Tova', 'The Hunt Club', 'Palomino', 'Regency Scalloped', 'Vanderbilt', 'YOTD Black', 'YOTD Periwinkle', 'YOTD White',
         'Eden', 'Radiance', 'Nantucket Basket', 'Nantucket Rope', 'Cognac', 'Pineapple Palms', 'Hydrangea', 'Harvest Plaid',
         'Midnight Garden', 'Fall Fling', 'Autumn Bloom', 'Jardin de Los Jefes', 'Sedona', 'Saddles & Silk', 'Handbook Plaid']  # = c5-brownstone order
CANCEL = {'Jardin de Los Jefes', 'Sedona', 'Fall Fling', 'Saddles & Silk', 'Handbook Plaid', 'Nantucket Basket', 'Nantucket Rope', 'Harvest Plaid', 'Midnight Garden'}
TRACKS = ['Peace Love Mahjong Oak', 'Bird & Bamboo Lilac', 'Bird & Bamboo Moss', 'Bird & Bamboo Wine']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
CLOSEUP = {'a38d0c3d6c', '9c5f1f84f2', '9df40a7c15', 'f371dd8b2e'}
PCT = {'Britt Mills': '15%', 'Amanda Toppe': '20%', 'Royal Mahjong Society': '15%'}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
NOCODE = {'Sunday Mahjong', 'Luxe Mahjong', 'Lucky Daughters', 'Mahjong Studios', 'I Love Mahj', 'Mahjong by SI', "Let's Be Besties", 'Mahj Tile Haus', 'Ozark Mahjongg', ''}
def footer(b):
    if b in NOCODE or b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return f"{PCT.get(b, '10%')} OFF  USE CODE : MAHJMATCH"
def uri(im, maxs=1600):
    im = im.copy(); im.thumbnail((maxs, maxs), Image.LANCZOS); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im, closeup=False):
    im = im.convert('RGB'); Wd, H = im.size
    if closeup:
        cw = min(Wd, int(H * 0.973)); ch = int(cw / 0.973); x0 = (Wd - cw) // 2; y0 = (H - ch) // 2
        return im.crop((x0, y0, x0 + cw, y0 + ch))
    z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H))
def source(k, orig_w):
    """-> (cropped PIL image, how)"""
    if os.path.exists(HD + k + '-crop.jpg'): return Image.open(HD + k + '-crop.jpg').convert('RGB'), 'EDSR x4 of the album crop'
    if os.path.exists(HD + k + '.jpg'):
        im = Image.open(HD + k + '.jpg').convert('RGB')
        if k in CLOSEUP: return crop(im, True), f'hi-res {im.size[0]}px'
        if im.width >= 2 * orig_w and orig_w < 900:  # super-resolved small photo: keep the full-photo framing she saw (z=1.0)
            Wd, H = im.size; cw = min(Wd, int(H * .973)); ch = int(cw / .973); return im.crop((0, H - ch, cw, H)), f'EDSR x4 ({orig_w}->{Wd}px)'
        return crop(im), f'brand hi-res {im.size[0]}px'
    im = Image.open(SRC + k + '.jpg'); return crop(im, k in CLOSEUP), f'original {im.size[0]}px'
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and')).strip('-')
TILE = 'assets/tiles/anders_ruff_brownstone_bloom_tilebox_CARD-ONLY-edited.jpg'; COL = '#7b2d3b'
cards, man = [], []
for nm in ORDER:
    if nm in CANCEL: continue
    v = BYNAME[nm]; k = v['vote_id']; brand = v['brand']
    m, how = source(k, v['src_size'][0])
    rk = next((kk for kk in REG if kk in (slug(nm), slug(brand) + '-' + slug(nm))), None)
    mr = REG[rk]['racks'] if rk else pick(m, exclude=TRACKS)
    fn = f"brownstone-bloom-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"; n = len(cards) + 1
    cards.append({'slug': f'bb{n:02d}', 'title': f'Brownstone Bloom + {nm}', 'col': COL, 'tile_file': TILE, 'racks': TRACKS, 'mat_racks': mr,
                  'file': fn, 'code': footer(brand), 'mat': uri(m)})
    man.append({'order': n, 'vote_id': k, 'mat': nm, 'brand': brand, 'file': fn, 'code': footer(brand), 'photo': how, 'crop_px': m.size[0],
                'racks': TRACKS, 'mat_racks': mr, 'mat_reg': rk})
json.dump({'_note': 'Brownstone Bloom album Oct 20', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Anders Ruff'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Brownstone Bloom', 'cards': man, 'cancelled': sorted(CANCEL), 'tile': TILE, 'title_color': COL,
           'racks_note': 'PROPOSAL pending her OK: tile racks PLM Oak + B&B Lilac/Moss/Wine; mat racks registry else matpick'}, open(W + '/manifest.json', 'w'), indent=1)
print(len(cards), 'cards'); [print(c['order'], c['mat'], c['photo'], c['crop_px'], c['mat_racks']) for c in man]
