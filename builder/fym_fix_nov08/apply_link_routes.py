"""Apply the staged link-route fixes (config/link-route-fixes.json, Tiffany Nov 8 6:02pm: close the ShopMy gap) to an FYM build.

Each item "<group>|<key>" -> {u: corrected paid link, ...}. Sets D[group][key].u (and u0, kept for the old store link in u_store).
The discount-code page link (dc) and the MAHJMATCH code on the card stay: e.g. Charleston Mahjong Club takes MAHJMATCH at checkout
after a ShopMy click too. Items with u = null (link not made yet) are skipped and listed. Idempotent.
The Mat Gallery takes the new links from the same build (builder/fym_fix_nov06/gallery_sync.py + build_v6.py).
Check afterwards: python3 scripts/checks/link_route_check.py <build> --gate   (FYM gate [172]).
Usage: python3 builder/fym_fix_nov08/apply_link_routes.py <build_dir> [--dry-run]"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; DRY = '--dry-run' in sys.argv
P = os.path.join(B, 'index.html'); h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
FX = json.load(open(REPO + 'config/link-route-fixes.json'))['items']
done, same, todo, gone = [], 0, [], []
for fk, x in FX.items():
    g, k = fk.split('|', 1)
    o = (D.get(g) or {}).get(k)
    if o is None: gone.append(fk); continue
    if not x.get('u'): todo.append(f"{x.get('name')} ({x.get('brand')})"); continue
    if o.get('u') == x['u']: same += 1; continue
    o.setdefault('u_store', o.get('u0') or o.get('u'))
    o['u'] = x['u']; o['u0'] = x['u']
    done.append(f"{g} {o.get('n')} ({o.get('bn')})")
print(f'link routes: {len(done)} links switched, {same} already right, {len(todo)} waiting for a link, {len(gone)} not in this build')
for d in done: print('  switched ' + d)
for t in todo: print('  NO LINK YET ' + t)
for t in gone: print('  not in build ' + t)
if not DRY and done:
    open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:])
