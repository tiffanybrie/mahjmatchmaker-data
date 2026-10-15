"""From the Vault albums (retired OMM sets): Lilac Soiree, Preppy Soiree, Shangri-la, Spring Love.
One card per YES mat from her vault swipe book (artifact SyWK3cDMvUiUf691PBAKb9, db omvault; Done Oct 15,
57 yes), live-album layout (gen2.py). Her stars (omvault_notes) lead each album, then deck order;
holiday mats she said yes to go last as holiday cards (gen2 'hol' layout = her "B tinted" pick).

Mat photos: retired OMM = repo assets/mats/omm-retired/ (Goldie = goldie-color-corrected.jpg, made after her
"Goldie coloring is wrong" note; Spring Fling = spring-fling.png, Tiffany's photo, doc 53); current OMM and
OMM holiday mats = the flat studio shots the book used (<workdir>/book/m/<id>.jpg).
Tile photos: assets/tiles/album/<set>.jpg (Spring Love's source is only ~210px, upscaled: needs a bigger one).
Racks: config/tile-racks-picks.json final_lists has none of the four sets. Lilac Soiree and Spring Love keep
the rack their live Larkspur cards use (Peace Love Mahjong Oak, scripts/albumcard/specs/larkspur.json);
Preppy Soiree and Shangri-la get no racks.
Footer: current OMM mats 10% code; retired mats (not sold) SHOP THE MATCH.
Usage: python3 vault_build.py <workdir>  (needs <workdir>/yes.json, stars.json, order.json, items.json, book/m/)
then per set: gen2.py <workdir>/<set>/spec.json <workdir>/<set>/cards"""
import json, io, base64, re, os, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
W = sys.argv[1]
Y = json.load(open(W + '/yes.json')); ST = json.load(open(W + '/stars.json')); OR = json.load(open(W + '/order.json'))
IT = json.load(open(W + '/items.json'))
SETS = {'lilac-soiree': ('Lilac Soiree', '#8a6fb5', ['Peace Love Mahjong Oak']),
        'preppy-soiree': ('Preppy Soiree', '#5a7f9e', []),
        'shangri-la': ('Shangri-la', '#1a7f63', []),
        'spring-love': ('Spring Love', '#e0789c', ['Peace Love Mahjong Oak'])}
RET = {'amethyst', 'birdie-green', 'birdie-pink', 'camellia', 'enchanted', 'goldie', 'mirage', 'peri-twinkle',
       'serengeti', 'soho', 'spring-fling', 'sweet-marie', 'zen-glow'}
RETFILE = {'goldie': 'goldie-color-corrected.jpg', 'spring-fling': 'spring-fling.png'}
NAME = {'peri-twinkle': 'Peri-twinkle', 'soho': 'SoHo', 'hol-miracle': 'Miracle', 'birdie-green': 'Birdie Green', 'birdie-pink': 'Birdie Pink'}
FLAME = 'data:image/png;base64,' + base64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def crop(im):
    im = flat(im); Wd, H = im.size
    z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and')).strip('-')
for g, (tname, col, racks) in SETS.items():
    yes = Y[g]; stars = [k for k in ST.get(g, []) if k in yes]
    order = stars + [k for k in OR[g] if k in yes and k not in stars]; order += [k for k in yes if k not in order]
    hol = [k for k in order if k.startswith('omm-hol-')]; order = [k for k in order if k not in hol] + hol
    cards, man = [], []
    for k in order:
        mid = k[4:]; is_hol = mid.startswith('hol-')
        nm = NAME.get(mid) or re.sub(r'\s*\(.*', '', IT[k]['label'].split(' · ')[0])
        if mid in RET: src = Image.open(R + 'assets/mats/omm-retired/' + RETFILE.get(mid, mid + '.jpg')); srcn = 'assets/mats/omm-retired/' + RETFILE.get(mid, mid + '.jpg')
        else: src = Image.open(f'{W}/book/m/{k}.jpg'); srcn = f'vault book m/{k}.jpg'
        retired = mid in RET or mid == 'hol-miracle'
        code = 'SHOP THE MATCH : MAHJMATCHMAKER.COM' if retired else '10% OFF  USE CODE : MAHJMATCH'
        fn = f"{g}-mahjong-tiles-oh-my-mahjong-{slug(nm)}-mat.jpg"
        c = {'slug': f'{g[:4]}{len(cards)+1:02d}', 'title': f'{tname} + {nm}', 'col': col, 'tile_file': f'assets/tiles/album/{g}.jpg',
             'racks': racks, 'file': fn, 'code': code, 'mat': uri(crop(src))}
        if is_hol: c.update(hol=True, flame=FLAME)
        cards.append(c)
        man.append({'order': len(cards), 'vote_id': k, 'star': k in stars, 'mat': nm, 'retired_mat': retired, 'holiday': is_hol,
                    'file': fn, 'code': code, 'src': srcn, 'src_size': list(src.size), 'racks': racks})
    os.makedirs(f'{W}/{g}', exist_ok=True)
    json.dump({'_note': f'From the Vault: {tname} v1', 'cards': cards, 'max_racks': 3}, open(f'{W}/{g}/spec.json', 'w'))
    json.dump({'set': tname, 'cards': man, 'title_color': col,
               'racks_note': 'no final_lists entry; ' + ('Peace Love Mahjong Oak as on the live Larkspur card' if racks else 'no racks')},
              open(f'{W}/{g}/manifest.json', 'w'), indent=1)
    print(g, len(cards), 'cards', len(hol), 'holiday')
