"""v112 (prepared Nov 1 by the MATCH-INBOX sweep): catalog adds that pass the gates (no OK needed, CLAUDE.md standing authority).
Runs builder/fym_fix_oct31/partneradds109.py UNCHANGED in logic, with spec config/fym-adds-nov01.json and ADD 'nov01-v112'
(16 mats: LBB Tropicana / Butterscotch Floral (+Simple Middle) / Vibrant Vortex (+Simple Middle), Britt Mills 5 leatherette +
Emerald Mirage neoprene twins, Sunday Green Gingham / Blue Gingham / Blue Rattan, Fait a Main Texas Mon Amour Chocolate Blue,
Fait a Main Round Top Mon Amour (HIDDEN + Questionable: close-up photos only)). Then, in the same build dir:
  - 'Also available in leatherette/neoprene' on the Britt Mills twins (spec alt_on_twin)
  - Sunday Vegan Leather relink (old listing 404s) (spec relink)
  - ncn=1 on the new non-partner mats (shop list says 'No code available at this time')
  - 12 racks from config/fym-rack-adds-nov01.json, HIDDEN + pending_review until a single-rack cut-out is approved on
    white + navy (rule 6b, gate [56]); see README step 3b.
Idempotent. Usage: python3 builder/fym_fix_nov01/adds112.py <build_dir>"""
import sys, os, json, hashlib
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
SRC = REPO + 'builder/fym_fix_oct31/partneradds109.py'
src = open(SRC).read()
for a, b in [("config/fym-nonpartner-adds-oct31b.json", "config/fym-adds-nov01.json"),
             ("ADD = 'oct31-v109'", "ADD = 'nov01-v112'"),
             ("src='nonpartner-adds-oct31b'", "src='adds-nov01'"),
             ("'Oct 31 non-partner Etsy brand add (v109, Tiffany Brands to Bring In = now): '", "'Nov 1 inbox sweep add (v112): '")]:
    assert a in src, 'partneradds109 changed, re-check anchor: ' + a
    src = src.replace(a, b)
g = {'__name__': '__main__', '__file__': SRC}
exec(compile(src, SRC, 'exec'), g)

# --- post steps on the written build ---
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, R = D['mats'], D['racks']
SPEC = json.load(open(REPO + 'config/fym-adds-nov01.json'))
log = []
for k, t in SPEC['alt_on_twin'].items():
    if k in M and M[k].get('alt') != t: M[k]['alt'] = t; log.append(('alt', M[k]['n'], t))
for k, x in SPEC['relink'].items():
    if k in M:
        o = M[k]
        if o.get('u') != x['u']: o.update(n=x['n'], u=x['u'], u0=x['u0']); log.append(('relink', k, x['n']))
for x in SPEC['mats']:
    if x.get('ncn') and x['key'] in M and not M[x['key']].get('ncn'): M[x['key']]['ncn'] = 1
RS = json.load(open(REPO + 'config/fym-rack-adds-nov01.json'))
HX = {'Light Pink': '#f3c6d3', 'Pink': '#e88aaa', 'Peach': '#f2b48f', 'Purple': '#8a6bb8', 'Navy': '#1f2a52', 'Sky Blue': '#9cc8ea',
      'Mint': '#a8dcc4', 'Green': '#2f7a4a', 'Black': '#1a1a1a', 'White': '#f3f1ec', 'Crystal Palace': '#e9eef0'}
RF = {'Light Pink': ['pink'], 'Pink': ['pink'], 'Peach': ['orange'], 'Purple': ['purple'], 'Navy': ['blue'], 'Sky Blue': ['blue'],
      'Mint': ['green'], 'Green': ['green'], 'Black': ['dark'], 'White': ['neutral'], 'Crystal Palace': ['neutral']}
for x in RS['racks']:
    k = x['key']
    if k in R: continue
    o = {f: x[f] for f in ('n', 'bn', 'b', 'u', 'u0', 'dc', 'pa', 'len') if f in x}
    col = next((c for c in HX if c in x['n']), None)
    o.update(nc=False, rt=False, c=False, ml=False, sk=False, hx=x.get('hx') or HX.get(col, '#cccccc'), rf=x.get('rf') or RF.get(col, []),
             im='', pq=3, hid=True, pending_review=1, add='nov01-v112', src_img=x.get('local_img') or x['src_img'])
    R[k] = o; log.append(('rack (hidden, pending cut-out review)', o['n']))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
for l in log: print(*l)
print('adds112 post steps:', len(log))
