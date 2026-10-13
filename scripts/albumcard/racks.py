"""Rack art for album cards, same sources as the live album cards:
- Bird & Bamboo: our painted render (builder/bbrack.py recolor of the full-res blank), any color.
- Other brands: the builder's cut-out product photo, only when it reads as a real rack (long, clean, with depth).
  Flat side-view strips (Miss Mahjong scalloped cut-outs) and square multi-rack photos with halos
  (Middle & Main beechwood, Mahjong Row sets, My Fair) are NOT drawn; they stay in the caption's rack line."""
import json, io, base64, sys
from PIL import Image
sys.path.insert(0, '/home/claude/mahjmatchmaker-data/builder')
from bbrack import recolor
R = '/home/claude/mahjmatchmaker-data/'
P = json.load(open('/tmp/mb/data_embed.json'))['prods']
BBHEX = {x['name']: x['hex'] for x in json.load(open(R + 'work/bbracks.json'))}
BLANK = Image.open('/tmp/mb/bb_blank.png')
BYNAME = {v['n']: k for k, v in P.items() if v.get('k') == 'rack'}
# cut-outs Tiffany's albums already use and that look right on a card
GOOD_PREFIX = ('plm:', 'peacelovemahjong.com/', 'www.ohmymahjong.com/', 'www.bambirdboutique.com/')

def bb(name):
    """name like 'Teal' -> RGBA render"""
    h = BBHEX.get(name)
    return recolor(BLANK, h) if h else None

def photo(key):
    v = P.get(key)
    if not v or not v.get('cut') or not key.startswith(GOOD_PREFIX): return None
    im = Image.open(io.BytesIO(base64.b64decode(v['cut'].split(',', 1)[1]))).convert('RGBA')
    if im.width / im.height < 4: return None
    return im

def by_label(label):
    """'Bird & Bamboo Teal' / 'Peace Love Mahjong Pink' / 'Oh My Mahjong White Acrylic' -> (img, label) or None"""
    if label.startswith('Bird & Bamboo '):
        im = bb(label[len('Bird & Bamboo '):]);
        return (im, label) if im else None
    if label.startswith('Peace Love Mahjong ') and 'plm:' + label[19:] in P:
        im = photo('plm:' + label[19:]); return (im, label) if im else None
    k = BYNAME.get(label)
    im = photo(k) if k else None
    return (im, label) if im else None
