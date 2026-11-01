"""Table view wall-color check (Nov 1, after Brownstone Bloom walls were drawn in the match-card TITLE color).
Fails if any Table view tile set draws walls with a color that is not a recorded back color, if a recorded back's
source is the title color / missing, or if a recorded back equals the set's match-card title color (s.tc) without a
real-back source. Usage: python3 scripts/tableview_back_check.py [built sample index.html]"""
import sys, json, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
BACK = json.load(open(R / 'config/tableview-back-colors.json'))
page = sys.argv[1] if len(sys.argv) > 1 else str(R / 'site/livepatch/tableview-sample-nov01/index.html')
t = open(page).read(); i = t.index('const DATA=') + 11; D, _ = json.JSONDecoder().raw_decode(t[i:])
bad = []
for slug, v in BACK.items():
    if slug.startswith('_'): continue
    src = (v.get('src') or '').lower()
    if not v.get('back') or not src: bad.append(f'{slug}: recorded back has no color or no source')
    if 'title' in src or 'tc' == src.strip(): bad.append(f'{slug}: back source is the title color')
    if v.get('type') == 'pattern' and not v.get('patch'): bad.append(f'{slug}: pattern back without a photo patch')
    # Nov 1 5:12pm (Dear Santa drawn ivory from a COLOR-GROUP note while its photo clearly shows dark green backs):
    # a back color must be MEASURED from a real back in a photo. Notes/groups/'her call' records never count on their own;
    # the only exceptions are ivory-back sets Tiffany explicitly confirmed as ivory backs (listed here).
    IVORY_OK = {'anders-ruff-brownstone-bloom', 'sunday-mahjong-hummingbird'}
    if not src.startswith('back photo measured') and slug not in IVORY_OK:
        bad.append(f'{slug}: back color not measured from a real back photo (source: {v.get("src")})')
for slug, tl in D['tiles'].items():
    if tl.get('walls'):
        b = BACK.get(slug)
        if not b: bad.append(f'{slug}: walls drawn but no recorded back color'); continue
        if (tl.get('back_hex') or '').lower() != b['back'].lower(): bad.append(f"{slug}: wall color {tl.get('back_hex')} is not the recorded back {b['back']}")
    elif not tl.get('why'): bad.append(f'{slug}: walls off with no reason shown')
    if 'tc' in tl: bad.append(f'{slug}: sample still ships the title color (tc) in tile data')
print('TABLE VIEW BACK CHECK:', 'FAIL' if bad else 'PASS', f'({sum(1 for x in D["tiles"].values() if x.get("walls"))} sets with walls, {len(D["tiles"])} sets)')
for b in bad: print('  ', b)
sys.exit(1 if bad else 0)
