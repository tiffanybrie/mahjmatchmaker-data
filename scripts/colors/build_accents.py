"""Accent colors for the Mat Gallery v5 multi-select (AND) filter. by: claude-measured (Oct 20).
Source: config/mat-color-measured.json all_clusters (k-means in Lab, flat bg + near white/black removed) for the catalog mats;
for mats added after Oct 19 (new53 + retired additions) the same family rules (families.fam_arr) per pixel, white/black dropped.
A color is an accent when it covers >= THRESH % of the measured (non white/black) area; Neutral needs NEUTRAL_THRESH (a real
ivory/linen field, not a pale tint), Dark needs DARK_THRESH; low-saturation 'orange' clusters
(tan, beige, peach cream) count as Earthy/Neutral; Black & White is never an accent. Accents are only used when 2+ chips are selected; build_v5.py drops any accent that Tiffany
removed from a mat (her v5 final_sections) and any accent already in the mat's primary/also tags.
Usage: python3 scripts/colors/build_accents.py  -> config/mat-accent-colors.json"""
import json, os, sys
import numpy as np
from PIL import Image
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
P = lambda *a: os.path.join(ROOT, *a)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from families import fam_arr
MAJOR = 15.0  # v5: a color covering >= 15% is a major part of the mat -> promoted to an also-color by build_v5.py (mats Tiffany hasn't called)
THRESH, NEUTRAL_THRESH, DARK_THRESH, TEAL_THRESH = 12.0, 45.0, 20.0, 15.0  # v5 accents also show as tier 3 in single-color sections: real visible color only
MAP = {'gold': 'yellow', 'brown': 'earthy'}
OK = {'pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'neutral', 'earthy', 'dark'}  # B&W is a graphic call, never an accent


def refam(fam, sat, light, hue=None):
    # eye checks (60-mat sample + teal/yellow accent sheets): tan/beige/peach-cream read 'orange', cream/tan read 'yellow'/'gold',
    # jade/emerald reads 'teal' (Tiffany: hue under ~180 is green). Move them before counting.
    if fam in ('orange', 'yellow', 'gold') and sat < (0.45 if fam == 'orange' else 0.5):
        return 'neutral' if light >= 0.75 else 'earthy'
    if fam == 'gold':
        return 'earthy' if light < 0.45 else 'yellow'
    if fam == 'teal' and hue is not None and hue < 180:
        return 'green'
    return fam


def pick(shares):
    tot = {}
    for fam, pct in shares:
        f = MAP.get(fam, fam)
        if f in OK: tot[f] = tot.get(f, 0) + pct
    return sorted([f for f, v in tot.items() if v >= {'neutral': NEUTRAL_THRESH, 'dark': DARK_THRESH, 'teal': TEAL_THRESH}.get(f, THRESH)], key=lambda f: -tot[f]), {f: round(v, 1) for f, v in tot.items()}


COLORS = ('pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple')


def major(sh):
    return [f for f in sorted(sh, key=lambda f: -sh[f]) if f in COLORS and sh[f] >= MAJOR]


def measure(path, N=96):
    a = np.asarray(Image.open(path).convert('RGB').resize((N, N))).astype(float) / 255
    f, h, l, s = fam_arr(a)
    low = ((f == 'orange') & (s < 0.45)) | (np.isin(f, ['yellow', 'gold']) & (s < 0.5))
    f = np.where(low, np.where(l >= 0.75, 'neutral', 'earthy'), f)
    f = np.where(f == 'gold', np.where(l < 0.45, 'earthy', 'yellow'), f)
    f = np.where((f == 'teal') & (h < 180), 'green', f)
    f = f.ravel(); keep = ~np.isin(f, ['white', 'black'])
    vals, cnt = np.unique(f[keep], return_counts=True)
    t = cnt.sum() or 1
    return [(str(v), 100.0 * c / t) for v, c in zip(vals, cnt)]


out = {'by': 'claude-measured', 'date': '2026-10-20', 'thresh_pct': THRESH, 'neutral_thresh_pct': NEUTRAL_THRESH, 'dark_thresh_pct': DARK_THRESH, 'teal_thresh_pct': TEAL_THRESH, 'major_pct': MAJOR,
       'about': __doc__.split('\n')[0] + ' Keyed by gallery img id. accents = colors >= threshold; shares = measured % per family.', 'mats': {}}
M = json.load(open(P('config/mat-color-measured.json')))['mats']
for k, v in M.items():
    img = v.get('image')
    if not img: continue
    acc, sh = pick([(refam(c['family'], c.get('sat', 1), c.get('light', 0.5), c.get('hue')), c['pct']) for c in v.get('all_clusters', [])])
    out['mats'][img] = {'accents': acc, 'major': major(sh), 'shares': sh, 'src': 'mat-color-measured'}
gal = P('assets/mats/gallery')
extra = [r[0] for r in json.load(open(P('site/livepatch/matgallery/new53_rows.json')))['rows']] + ['tigre-de-tartan--holy-mahj-retired', 'tigre-de-tartan--queen-bee-retired', 'mahj-tile-haus--imperial-lotus']  # Imperial Lotus: Tiffany allowed Oct 20 late (her Talulah album)
extra += [a['img'] for a in json.load(open(P('config/mat-gallery-extra-rows.json')))['rows'] if a.get('added') == '2026-10-26-sync']  # Oct 26 gallery sync rows (FYM b97 photos)
for img in extra:
    acc, sh = pick(measure(os.path.join(gal, img + '.webp')))
    out['mats'][img] = {'accents': acc, 'major': major(sh), 'shares': sh, 'src': 'pixel-families'}
json.dump(out, open(P('config/mat-accent-colors.json'), 'w'), indent=1, ensure_ascii=False)
print(len(out['mats']), 'mats;', sum(len(v['accents']) for v in out['mats'].values()), 'accent tags')
