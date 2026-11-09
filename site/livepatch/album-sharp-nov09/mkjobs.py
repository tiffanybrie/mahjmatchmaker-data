"""album-sharp-nov09: rerender jobs for the album-page cards the tighter blur gate failed (docs/status/card-sharpness.json).
Each job copies the LIVE figure (title, tile set, tile + mat rack captions); only the mat photo changes.
Usage: python3 mkjobs.py <dir of live page curls> <cards.json from the scan parse> jobs.json"""
import sys, json
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'site/livepatch/missed-album-picks-nov07')
import build as B
PH = {'Peace Love Mahjong': 'plm_sugarplum_1512.jpg',            # PLM holiday variant 1512px (HolidayMat-SugarplumPlaid_1.jpg)
      'Holiday Love Red & Green': 'bespoke_rg_706.jpg',          # Bespoke screenshot 706px, Side A (the Tinselle source)
      'Holiday Love Blue': 'blue_s1.png'}                        # Bespoke Screenshot2026-06-28at9.43.38AM.png 732x722, Side A
TB = {}
for p in json.load(open(R + 'site/livepatch/missed-album-picks-nov07/pairs.json')): TB.setdefault(p['page'], p['tile_brand'])
srcdir = sys.argv[1]; cards = json.load(open(sys.argv[2])); jobs = []
for x in cards:
    mat = x['h3'].split(' + ', 1)[1]
    ph = PH.get(mat) or PH.get(x['brand']) if x['brand'] in ('Peace Love Mahjong', 'Bespoke Mahjong') else None
    if not ph: continue
    t = x['page'].replace('-mahjong-tile-matches', '')
    jobs.append({'page': x['page'], 'idx': x['idx'], 'img': x['img'], 'h3': x['h3'], 'brand': x['brand'], 'hol': x['hol'], 'tile': t,
                 'tile_file': None, 'tile_brand': TB[t], 'tile_racks': x['tile_racks'], 'mat_racks': x['mat_racks'],
                 'file': x['img'].split('/')[-1].split('?')[0], 'crop': None, 'photo': srcdir + '/' + ph})
json.dump(jobs, open(sys.argv[3], 'w'), indent=1)
print(len(jobs), 'jobs')
