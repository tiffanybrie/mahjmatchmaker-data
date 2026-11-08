"""My Fair Mahjong The Style of Your Life Series (Pearl Green) album match cards, DRAFT (Nov 7, round 1 = Claude's picks).
Same pipeline as Juniper (juniper_build.py -> gen2.py, card2.html layout): tile PILE photo assets/tiles/album/style-of-your-life.jpg
(MFM listing image StyleofYourLifeSeries_11), current flame-heart wordmark (card_navy_logo_v3.png), racks at TRUE length.
Tile racks (MATCH THE TILES) = config/colorcards.json sets.style-of-your-life racks: My Fair Mahjong Indigo Blue + Magenta
(same solid acrylic shape, both 20in). Mat racks (MATCH THE MAT) = matpick (nearest B&B colours), registry wins when listed.
Usage: python3 style_of_your_life_build.py <workdir>; then python3 scripts/albumcard/gen2.py <workdir>/spec.json assets/cards/style-of-your-life"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
A = json.load(open(os.environ.get('SOYL_SPEC', R + 'scripts/albumcard/specs/style_of_your_life_round1.json')))
CC = json.load(open(R + 'config/colorcards.json'))['sets']['style-of-your-life']
TRACKS = CC['racks']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im):  # Juniper/Papaya default framing: whole mat for small photos, a 72% bottom-left zoom for big ones
    im = flat(im); Wd, H = im.size; z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / .973)
    if ch > H: ch = H; cw = int(ch * .973)
    return im.crop((0, H - ch, cw, H))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '').replace('–', '-')).strip('-')
def reg_for(path, name):
    for k, v in REG.items():
        if path in v.get('files', []) or slug(name) == k: return k, v['racks']
    return None, None
CODE = '10% OFF  USE CODE : MAHJMATCH'  # My Fair Mahjong: 10% with MAHJMATCH (config/code-truth.json)
cards, man = [], []
for c in A['mats']:
    nm, brand, retired = c['name'], c['brand'], c['retired']
    src = Image.open(R + c['img'])
    m = flat(src).crop(tuple(c['box'])) if c.get('box') else crop(src)
    rk, mr = reg_for(c['img'], nm)
    mr = [x for x in (mr or []) if x not in TRACKS]
    if len(mr) < 2:
        for l in pick(m, exclude=TRACKS + mr):
            if l not in mr and len(mr) < 2: mr.append(l)
    fn = f"style-of-your-life-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"
    n = len(cards) + 1
    cards.append({'slug': f'soyl{n:02d}', 'title': f'Style of Your Life + {nm}', 'col': CC['col'], 'tile_file': CC['tile'],
                  'tilefit': 'cover', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': CODE, 'mat': uri(m)})
    man.append({'order': n, 'group': c['group'], 'mat': nm, 'brand': brand, 'retired_mat': retired, 'holiday': False,
                'file': fn, 'code': CODE, 'src': c['img'], 'racks': TRACKS, 'mat_racks': mr, 'mat_reg': rk, 'why': c['why'],
                'caption_note': 'Pair mat' if nm == 'Parquet Petal' else ('Also in Juniper' if c['group'] == 'shared' else None)})
json.dump({'_note': 'Style of Your Life album DRAFT (Nov 7 round 1)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'My Fair Mahjong',
           'navy': 'assets/brand/card_navy_logo_v3.png', 'true_len': True}, open(W + '/spec.json', 'w'))
json.dump({'set': 'The Style of Your Life Series (Pearl Green)', 'brand': 'My Fair Mahjong', 'status': "DRAFT: round 1 = Claude's picks, pending her order",
           'cards': man, 'title_color': CC['col'], 'tile': CC['tile'],
           'racks_note': 'tile racks = colorcards style-of-your-life racks (My Fair Mahjong Indigo Blue + Magenta); mat racks = registry or matpick'},
          open(W + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
