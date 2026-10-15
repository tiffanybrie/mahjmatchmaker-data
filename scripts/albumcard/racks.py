"""Rack art for album cards (Tiffany, Oct 15: real rack photos only, no rendered OMM racks).
- Every non-B&B rack = its REAL photo from assets/racks/card/index.json (built by real_racks.py from OMM's
  single-rack product photos, PLM's real per-colour cut-outs, Bam Bird's photo and Tiffany's own rack cut-outs).
  A rack with no real photo returns None and is reported as missing; it is never replaced by a render or
  another colour.
- Bird & Bamboo = the one rack we generate (doc 48): builder/bbrack.py recolor of the real B&B blank."""
import json, sys
from PIL import Image
sys.path.insert(0, '/home/claude/mahjmatchmaker-data/builder')
from bbrack import recolor
R = '/home/claude/mahjmatchmaker-data/'
IDX = json.load(open(R + 'assets/racks/card/index.json'))
BBHEX = {x['name']: x['hex'] for x in json.load(open(R + 'work/bbracks.json'))}
BLANK = Image.open(R + 'assets/racks/card/bb-blank.png').convert('RGBA')
MISSING = set()

def bb(name):
    h = BBHEX.get(name)
    return recolor(BLANK, h) if h else None

try:  # builder product keys (gen_hol.py passes these); only used to look up the rack's name
    P = json.load(open('/tmp/mb/data_embed.json'))['prods']
except Exception:
    P = {}

def photo(label):
    """approved rack name (or a builder product key) -> real photo, else None"""
    if label not in IDX['racks'] and label in P: label = P[label].get('n', label)
    r = IDX['racks'].get(label)
    return Image.open(R + r['file']).convert('RGBA') if r else None

def by_label(label):
    """'Bird & Bamboo Teal' / 'Peace Love Mahjong Pink' / 'Oh My Mahjong White Acrylic' -> (img, label) or None"""
    im = bb(label[len('Bird & Bamboo '):]) if label.startswith('Bird & Bamboo ') else photo(label)
    if im is None: MISSING.add(label); return None
    return (im, label)

def frac(label):
    """share of the image height that is the rack itself (OMM photos also show the pusher above it)"""
    if label not in IDX['racks'] and label in P: label = P[label].get('n', label)
    return IDX['racks'].get(label, {}).get('rack_frac', 1.0)
