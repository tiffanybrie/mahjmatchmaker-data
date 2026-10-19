"""Turn Tiffany's Mat Color Tagger taps into config/mat-color-overrides.json (her tags win everywhere).

Pull step (from a Claude session; the tagger's db can only be read through the ArtifactData tool):
  ArtifactData action=list url=https://claude.ai/artifact/RoHrY1LHAj8bgZx2aL4bLW collection=matcolors
               query={"limit":1000} out_dir=<DIR>
  -> writes <DIR>/matcolors/<doc_id>.json (one per mat she touched; page through next_cursor if >1000)
Then:  python3 scripts/colors/apply_matcolors.py <DIR>/matcolors
Also refreshes config/mat-color-guesses.json from scratchpad guesses when --guesses PATH is given.
Doc ids are gallery image names; each doc carries the catalog key in `key`."""
import json, os, sys, glob, datetime
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
args = sys.argv[1:]
if '--guesses' in args:
    i = args.index('--guesses'); gpath = args[i + 1]; del args[i:i + 2]
    G = json.load(open(gpath))
    out = {g['k']: {'primary': g['p'], 'secondary': g['s'], 'tone': g['t'], 'holiday': g['hol'], 'skip': False, 'image': n}
           for n, g in G.items()}
    json.dump({'about': 'Computer photo read (scripts/colors/families.py). Tiffany overrides win: config/mat-color-overrides.json',
               'updated': datetime.date.today().isoformat(), 'mats': out}, open(os.path.join(R, 'config/mat-color-guesses.json'), 'w'), indent=0)
    print('guesses', len(out))
if args:
    p = os.path.join(R, 'config/mat-color-overrides.json')
    cur = json.load(open(p)) if os.path.exists(p) else {'mats': {}}
    n = 0
    for f in glob.glob(os.path.join(args[0], '*.json')):
        d = json.load(open(f)); d = d.get('data', d)
        if not d.get('key') or d.get('by') == 'claude-probe': continue
        cur['mats'][d['key']] = {k: d.get(k) for k in ('primary', 'secondary', 'tone', 'holiday', 'skip')} | {'image': os.path.basename(f)[:-5], 'at': d.get('at')}
        n += 1
    cur['about'] = "Tiffany's Mat Color Tagger taps (artifact RoHrY1LHAj8bgZx2aL4bLW, db matcolors). These win over every computer color."
    cur['updated'] = datetime.date.today().isoformat()
    json.dump(cur, open(p, 'w'), indent=1)
    print('overrides', n, 'total', len(cur['mats']))
