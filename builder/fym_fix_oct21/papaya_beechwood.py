"""Papaya Spritz tile-rack swap in FYM (Tiffany, Oct 21): Peace Love Mahjong Oak -> Middle & Main Scalloped Beechwood.
Her approved change (config/tile-racks-picks.json final_lists papaya-spritz, commit 306d7f5; album cards fbf7ec9).
In every Papaya match-list entry (set oh-my-mahjong-papaya-spritz, field m) whose rack list contains the PLM Oak key,
that key is replaced IN PLACE by the M&M Scalloped Beechwood key. Nothing else changes.
Also updates builder/fym_flags/locks.json (sets.oh-my-mahjong-papaya-spritz.m) and records the change in locks '_changes'.
Oct 21 pm (independent QA): D.lt['oh-my-mahjong-papaya-spritz'] (her tile-rack list, merged into the her-picks rack deck by herRacks)
still listed PLM Oak, so Oak kept a "Tiffany's match" badge. D.lt for Papaya is now set to her final list IN final_lists ORDER
(Lavender, Chartreuse, M&M Scalloped Beechwood), Oak dropped; any extra lt racks stay after them. D.lm (per-mat racks) is checked for
a Papaya-specific Oak (none as of Oct 21). D.uni is NOT touched: Oak as the universal rack for every set is fine (Tiffany).
lt is not locked (locks.json has no lt section); gate [15] (builder/fym_flags/rack_replacements.json) keeps Oak out of Papaya lt + m.
Idempotent; src == out patches the build in place.
Usage: python3 builder/fym_fix_oct21/papaya_beechwood.py <src_build_dir> <out_build_dir>"""
import sys, os, json, shutil
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
SLUG = 'oh-my-mahjong-papaya-spritz'
OAK = 'peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'
BW = 'www.middleandmainmahjong.com/golden-grain-beechwood-mahjong-rack-and-pusher-set-of-4'
src, out = sys.argv[1], sys.argv[2]
if os.path.abspath(src) != os.path.abspath(out):
    if os.path.exists(out): shutil.rmtree(out)
    shutil.copytree(src, out, ignore=shutil.ignore_patterns('gate_output.txt'))
p = os.path.join(out, 'index.html'); h = open(p).read(); i = h.find('const D=') + 8
D, end = json.JSONDecoder().raw_decode(h, i)
assert D['racks'][OAK]['n'] == 'Peace Love Mahjong Oak', D['racks'][OAK]['n']
assert D['racks'][BW]['n'] == 'Middle & Main Scalloped Beechwood', D['racks'][BW]['n']
assert not D['racks'][BW].get('rt'), 'Beechwood rack is retired'

def swap(m):
    n = 0
    for e in m:
        rl = e[1]
        if OAK in rl:
            assert BW not in rl, e
            rl[rl.index(OAK)] = BW; n += 1
    return n

sets = [s for s in D['sets'] if s['slug'] == SLUG]
assert len(sets) == 1
n_build = swap(sets[0]['m'])

# D.lt: her tile-rack list for the set, in final_lists order (config/tile-racks-picks.json final_lists['papaya-spritz'])
FINAL_KEYS = ['bb:Lavender', 'plm:Chartreuse', BW]
FL = json.load(open(REPO + 'config/tile-racks-picks.json'))['final_lists']['papaya-spritz']
assert [D['racks'][k]['n'] for k in FINAL_KEYS] == FL, (FL, [D['racks'][k]['n'] for k in FINAL_KEYS])
lt_old = list(D['lt'].get(SLUG, []))
lt_new = FINAL_KEYS + [r for r in lt_old if r not in FINAL_KEYS and r != OAK]
D['lt'][SLUG] = lt_new
n_lt = int(lt_old != lt_new)
# D.lm: per-mat rack lists are shared across sets; report any Oak in a mat that is in Papaya's match list
pap_mats = {e[0] for e in sets[0]['m']}
lm_oak = [k for k, v in (D.get('lm') or {}).items() if OAK in v and k in pap_mats]
assert not lm_oak, f'Papaya match-list mats with Oak in D.lm (decide per mat): {lm_oak}'
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(p, 'w').write(h)

LP = REPO + 'builder/fym_flags/locks.json'
L = json.load(open(LP))
n_lock = swap(L['sets'][SLUG]['m'])
if n_lock: L.setdefault('_changes', []).append({
    'date': '2026-10-21', 'set': SLUG, 'field': 'm',
    'change': f'tile rack Peace Love Mahjong Oak ({OAK}) -> Middle & Main Scalloped Beechwood ({BW}) in {n_lock} match-list entries',
    'approval': "Tiffany's decision (Oct 21): Papaya Spritz racks = B&B Lavender, PLM Chartreuse, M&M Scalloped Beechwood "
                '(config/tile-racks-picks.json final_lists, commit 306d7f5). Approved change, not a refresh.'})
if n_lock:
    json.dump(L, open(LP, 'w'), indent=1, ensure_ascii=False)
assert sets[0]['m'] == L['sets'][SLUG]['m'], 'build m != locked m after swap'
print(f'build m entries swapped: {n_build}; lt: {lt_old} -> {lt_new} (changed: {n_lt}); lm Papaya Oak: {len(lm_oak)}; locks entries swapped: {n_lock}; out: {out}')
