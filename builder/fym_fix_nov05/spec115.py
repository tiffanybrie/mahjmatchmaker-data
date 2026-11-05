"""Writes config/fym-adds-nov05.json (FYM 1.15 catalog adds) and the mat/tile photos it names (assets/mats/v115, assets/tiles/v115).
Photos chosen by eye on contact sheets Nov 5 (Matches & Catalog): brand flat/whole-mat shots; props on the mat are fine (low bar).
Usage: python3 builder/fym_fix_nov05/spec115.py"""
import json, os, re
from PIL import Image
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
L = R + 'assets/launches/'; os.makedirs(R + 'assets/mats/v115', exist_ok=True); os.makedirs(R + 'assets/tiles/v115', exist_ok=True)
def save(src, out, crop=None, mx=1200):
    im = Image.open(src).convert('RGB')
    if crop: W, H = im.size; im = im.crop((int(crop[0] * W), int(crop[1] * H), int(crop[2] * W), int(crop[3] * H)))
    im.thumbnail((mx, mx)); im.save(R + out, quality=90); return out
LBBR = '12515508.SUyXEjJsqV'; MPR = '12703261.srer4OxWkeRwwDVs'; BMR = '11205153.24gc8ncLZw3'
def lbb(h): return dict(b="Let's Be Besties", bn="Let's Be Besties", u=f'https://letsbebesties.com/discount/MAHJMATCH?redirect=%2Fproducts%2F{h}%3Fsca_ref%3D{LBBR}',
                       u0=f'https://letsbebesties.com/products/{h}?sca_ref={LBBR}', dc='https://mahjmatchmaker.com/lets-be-besties-discount-code', pa=True)
def noli(h): return dict(b='nolijune.com', bn='Noli June', u=f'https://nolijune.com/discount/MAHJMATCH?dt_id=3655694&redirect=%2Fproducts%2F{h}',
                        u0=f'https://nolijune.com/products/{h}', dc='https://mahjmatchmaker.com/noli-june-discount-code', pa=True)
def mp(h): return dict(b='mahjpit.co', bn='Mahj Pit', u=f'https://mahjpit.co/products/{h}?sca_ref={MPR}', u0=f'https://mahjpit.co/products/{h}?sca_ref={MPR}',
                      dc='https://www.mahjmatchmaker.com/mahj-pit-discount-code', pa=True)
mats = []
def add(key, name, link, img, hol=False, **kw): mats.append(dict(key=key, name=name, img=img, hol=hol, hid=False, reason='', **link, **kw))
for h, n, hol in [('electric-zigzag-mahjong-mat', 'Electric ZigZag', False), ('christmas-lights-mahjong-mat', 'Christmas Lights', True),
                  ('tiger-stripes-ohbon-studios-artist-mahjong-mat', 'Tiger Stripes', False), ('spinning-dreidel-ohbon-studios-artist-mahjong-mat', 'Spinning Dreidel', True),
                  ('champange-bubbles-mahjong-mat', 'Champagne Bubbles', False), ('mid-century-floral-mahjong-mat', 'Mid Century Floral', False),
                  ('pink-pizzazz-mahjong-mat', 'Pink Pizzazz', False), ('gatsby-glow-mahjong-mat', 'Gatsby Glow', False),
                  ('mad-for-plaid-mahjong-mat', 'Mad for Plaid', False), ('disco-dot-with-simple-middle-mahjong-mat', 'Disco Dot with Simple Middle', False)]:
    src = sorted(f for f in os.listdir(L + 'letsbebesties-' + h) if f.startswith('01'))[0]
    add('letsbebesties.com/' + h, n, lbb(h), save(L + f'letsbebesties-{h}/{src}', f'assets/mats/v115/lbb-{h}.jpg'), hol, photo_note='LBB flat render', inbox='Nov 1/Nov 3 launch watch')
for h, n, hol in [('marlene-put-out-a-spread-on-the-eighth-night', 'Marlene Put Out a Spread on the Eighth Night', True),  # Hanukkah menorah
                  ('rochelle-didnt-make-it-to-midnight', "Rochelle Didn't Make It to Midnight", False),          # New Year's Eve = not holiday (Oct 21 definition)
                  ('ruth-took-the-last-run-in-the-dark', 'Ruth Took the Last Run in the Dark', True),            # ski / snowy village
                  ('shirley-wore-a-parka-to-the-beach', 'Shirley Wore a Parka to the Beach', True)]:             # snowy beach
    add('nolijune.com/' + h, n, noli(h), save(L + f'noli-june-{h}/0.jpg', f'assets/mats/v115/noli-{h}.jpg'), hol, photo_note='Noli flat render', inbox='Nov 3 HQ yes')
MPM = {'mahjong-mat-domino-oxblood': ('Domino Oxblood', '01', False, None), 'mahjong-mat-french-mural': ('French Mural', '01', False, None),
       'mahjong-mat-ditsy-christmas-maraschino-w-rules': ('Ditsy Christmas Maraschino', '01', True, None), 'savannah': ('Savannah', '01', False, None),
       'inky-mat': ('The Blue Hole', '01', False, None), 'the-butterfly-dolly-mat': ('The Butterfly Dolly', '01', False, None),
       'pixel-pusher-mat': ('Pixel Pusher', '01', False, None), 'paint-party-mat': ('Paint Party', '02', False, (0, 0, 0.82, 1)), 'turkey-dinner-mat': ('Turkey Dinner', '01', False, (0, 0.2, 1, 0.78)),
       'the-line-mat-copy': ('The Calling Card', '01', False, None), 'the-line-mat': ('The Line', '01', False, None), 'the-quigley-mat': ('The Quigley', '01', False, None),
       'poppylicious-mat': ('Poppylicious', '01', False, None), 'acid-in-the-library-may': ('Acid in the Library', '02', False, None), 'flower-shop': ('Flower Shop', '04', False, (0, 0.22, 1, 0.78)),
       'primary-on-broughton-game-mat-copy': ('Zinnia Jockeys', '01', False, None), 'primary-on-broughton': ('Primary on Broughton', '03', False, None),
       'seaside-game-mat': ('Seaside', '01', False, None), 'mahjong-gaming-mat-el-tigre-rules-edition': ('El Tigre (Rules Edition)', '01', False, None),
       'deep-blue-mat': ('Deep Blue', '03', False, (0.12, 0, 0.79, 0.76)), 'all-vibes-mat': ('All Vibes', '01', False, None)}
CAT = {x['handle']: x for x in json.load(open(R + 'data/brands/mahj-pit-catalog-2026-11-04.json'))['items']}
for h, (n, f, hol, crop) in MPM.items():
    add('mahjpit.co/' + h, n, mp(h), save(L + f'mahjpit-{h}/{f}.jpg', f'assets/mats/v115/mahjpit-{h}.jpg', crop), hol, oos=0 if CAT[h]['available'] else 1,
        price=CAT[h]['price'], photo_note=f'brand photo {f} (whole mat; racks/tiles on it are fine)', inbox='Nov 4 3:40pm NEW PARTNER')
add('www.ohmymahjong.com/lotus-cove-mat-in-tube', 'Lotus Cove', dict(b='Oh My Mahjong', bn='Oh My Mahjong', u='https://ohmymahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Flotus-cove-mat-in-tube',
    u0='https://www.ohmymahjong.com/products/lotus-cove-mat-in-tube', dc='https://mahjmatchmaker.com/oh-my-mahjong-discount-code', pa=True),
    save(R + 'config/matcard/lotuscove_mat.jpg', 'assets/mats/v115/omm-lotus-cove.jpg'), False, photo_note='OMM overhead flat, cropped mat card', inbox='Nov 3 HQ: all new OMM into FYM', price=90)
add('brittmillsdesign.com/isla-neoprene-mahjong-mat-arriving-late-november', 'Isla', dict(b='brittmillsdesign.com', bn='Britt Mills',
    u=f'https://brittmillsdesign.com/products/isla-neoprene-mahjong-mat-arriving-late-november?sca_ref={BMR}', u0=f'https://brittmillsdesign.com/products/isla-neoprene-mahjong-mat-arriving-late-november?sca_ref={BMR}',
    dc='https://mahjmatchmaker.com/britt-mills-discount-code', pa=True), 'assets/mats/v115/britt-mills-isla.jpg', False,
    alt='Also available in leatherette', altu=f'https://brittmillsdesign.com/products/isla-leatherette-mahjong-mat?sca_ref={BMR}', photo_note='brand render cropped to the mat', inbox='Nov 2 launch watch')
add('splashofcolorco.com/santa-baby-s-cocktail-hour-mahjong-mat-sleek-surface', "Santa Baby's Cocktail Hour", dict(b='splashofcolorco.com', bn='Splash of Color',
    u='https://splashofcolorco.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fsanta-baby-s-cocktail-hour-mahjong-mat-sleek-surface',
    u0='https://splashofcolorco.com/products/santa-baby-s-cocktail-hour-mahjong-mat-sleek-surface', dc='https://mahjmatchmaker.com/splash-of-color-discount-code', pa=True),
    save(L + 'splashofcolor-santa-baby-s-cocktail-hour-mahjong-mat-sleek-surface/1.jpg', 'assets/mats/v115/splash-santa-babys-cocktail-hour.jpg', (0.05, 0.19, 0.98, 0.98)), True,
    photo_note='table render cropped to the mat', inbox='her 12 swipe-book yeses (santababy)')
tiles = []
def tadd(key, slug, name, bn, link, img, tc, group, oos=0, **kw): tiles.append(dict(key=key, slug=slug, name=name, bn=bn, img=img, tc=tc, group=group, oos=oos, **link, **kw))
OMMT = dict(u='https://ohmymahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fjuniper-mahjong-tiles', u0='https://www.ohmymahjong.com/products/juniper-mahjong-tiles',
            dc='https://mahjmatchmaker.com/oh-my-mahjong-discount-code', pa=True)
tadd('www.ohmymahjong.com/juniper-mahjong-tiles', 'juniper', 'Juniper', 'Oh My Mahjong', OMMT, 'assets/tiles/album/juniper.jpg', '#225d36', 'Green', price=475,
     photo_note='album photo (assets/tiles/album/juniper.jpg); catalog set m=[] (Claude picks are not hers)')
BSR = '10217561.eoZg0pKJHSf8IQSE'
def bsp(h): return dict(u=f'https://bespokemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2F{h}%3Fsca_ref%3D{BSR}', u0=f'https://www.bespokemahjong.com/products/{h}?sca_ref={BSR}',
                       dc='https://mahjmatchmaker.com/bespoke-mahjong-discount-code', pa=True)
tadd('www.bespokemahjong.com/sunshineglow', 'bespoke-mahjong-garden-glow-sunshine-glow', 'Garden Glow (Sunshine Glow)', 'Bespoke Mahjong', bsp('sunshineglow'),
     save(L + 'bespokemahjong-sunshineglow/02.png', 'assets/tiles/v115/bespoke-sunshine-glow.jpg', (0.0, 0.0, 1, 0.78)), '#e8c547', 'Yellow & Orange', price=495, photo_note='brand flat-lay of the faces')
tadd('www.bespokemahjong.com/coming-this-november-mahjong-its-a-vibe-glitter-glow-green', 'bespoke-mahjong-its-a-vibe-glitter-glow-green', "It's a Vibe (Glitter Glow Green)", 'Bespoke Mahjong',
     bsp('coming-this-november-mahjong-its-a-vibe-glitter-glow-green'), save(L + 'bespoke-coming-this-november-mahjong-its-a-vibe-glitter-glow-green/02-53521055187227.png',
     'assets/tiles/v115/bespoke-glitter-glow-green.jpg'), '#8fd19e', 'Holiday', price=495, photo_note='brand pile of faces (green pearl backs)')
def mpt(h): return dict(u=f'https://mahjpit.co/products/{h}?sca_ref={MPR}', u0=f'https://mahjpit.co/products/{h}?sca_ref={MPR}', dc='https://www.mahjmatchmaker.com/mahj-pit-discount-code', pa=True)
for h, slug, n, f, tc, g, crop in [('the-original-confetti-tiles-small', 'mahj-pit-original-confetti-small', 'The Original Confetti (Small)', '02', '#1d3f9a', 'Blue', None),
                                   ('large-confetti-tiles', 'mahj-pit-original-confetti-large', 'The Original Confetti (Large)', '01', '#1d3f9a', 'Blue', (0.05, 0.1, 0.95, 0.9)),
                                   ('the-martha-tiles', 'mahj-pit-martha', 'The Martha', '02', '#e9e3d6', 'Ivory', (0.0, 0.0, 1, 0.62)),
                                   ('merry-merry-holiday-tiles-limited-edition', 'mahj-pit-merry-merry', 'Merry Merry Holiday', '02', '#b5172b', 'Holiday', (0.1, 0.2, 0.89, 0.75)),
                                   ('the-commuter-skinny-tiles-only', 'mahj-pit-commuter-skinny-midnights', 'Commuter Skinny (Midnights)', '03', '#16161d', 'Blue', (0.0, 0.15, 1, 0.85))]:
    tadd('mahjpit.co/' + h, slug, n, 'Mahj Pit', mpt(h), save(L + f'mahjpit-{h}/{f}.jpg', f'assets/tiles/v115/mahjpit-{h}.jpg', crop), tc, g,
         oos=0 if CAT[h]['available'] else 1, price=CAT[h]['price'], photo_note=f'brand photo {f}')
json.dump({'_about': 'FYM 1.15 (v115) catalog adds, Nov 5 (DESK item 2b). Photos chosen by eye on contact sheets. Holiday = Christmas/Hanukkah/winter snow only (Rochelle NYE = year-round). '
           'Mahj Pit racks NOT here (rule 6b white+navy review first). Read by builder/fym_fix_nov05/adds115.py.', 'made': '2026-11-05', 'mats': mats, 'tiles': tiles},
          open(R + 'config/fym-adds-nov05.json', 'w'), indent=1, ensure_ascii=False)
print('mats', len(mats), 'tiles', len(tiles))
