"""FYM 1.18: Tiffany's 28 Amazon holiday picks (Oct 26 11:16, never shipped) WITHOUT v96's colour-ranking step.
builder/fym_fix_oct25/v96_amazon_holiday.py was written for v96; run on today's build its part 2 (ShopMy placement into s.cr) drops
every earlier oct26-etsy placement, re-places them with a stale score (Christmas mats landed in Aloha's / Brownstone's / Juniper's
first 5) and cuts s.cr to 300 (gate [57] / [76] failed on the 1.18 candidate, Nov 7). So: keep v96 part 1 (the adds: photo, chunk,
thumb, colours, Holiday only, ShopMy link), put every set's s.cr back exactly as it was, give the new non-partner mats ncn=1
('No code available at this time', gate [137d]); builder/fym_fix_oct30/v104rank.py then colour-ranks them (gate [107]).
Idempotent. Usage: python3 builder/fym_fix_nov07/amazon118.py <build dir>"""
import sys, os, json, subprocess, re, struct
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'
def load():
    h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return h, i, i + e, D
_, _, _, D0 = load(); cr0 = {s['slug']: list(s['cr']) for s in D0['sets'] if 'cr' in s}
r = subprocess.run([sys.executable, R + 'builder/fym_fix_oct25/v96_amazon_holiday.py', B], capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '', r.stderr[-500:] if r.returncode else '')
assert r.returncode == 0
h, i, e, D = load(); n = 0
# v96 packs all 28 photos into ONE chunk file, but the page loads photo m/N from chunk N // MCN (12): m/3060.. would be looked up in
# chunks 255/256, which did not exist (no photo in the app, gallery_sync 'no FYM photo'). Re-pack per chunk + list every chunk in MCB.
MCN = int(re.search(r'MCN=(\d+)', h).group(1)); mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); have = [int(v) for v in mcb.group(1).split(',')]
amz = sorted({o['f'] for o in D['mats'].values() if o.get('add') == 'oct26-amazon'}, key=lambda f: int(f[2:-5]))
src_c = sorted({c for c in have if os.path.exists(f'{B}/mc/{c}.webp') and amz and amz[0] in json.loads((lambda r: r[-4 - struct.unpack('<I', r[-4:])[0]:-4])(open(f'{B}/mc/{c}.webp', 'rb').read()))})
if src_c:
    raw = open(f'{B}/mc/{src_c[0]}.webp', 'rb').read(); hn = struct.unpack('<I', raw[-4:])[0]; hdr = json.loads(raw[-4 - hn:-4])
    groups = {}
    for f_, (a_, l_) in hdr.items(): groups.setdefault(int(f_[2:-5]) // MCN, {})[f_] = raw[a_:a_ + l_]
    for c_, fs in groups.items():
        body, hd = b'', {}
        for f_, b_ in sorted(fs.items(), key=lambda kv: int(kv[0][2:-5])): hd[f_] = [len(body), len(b_)]; body += b_
        hj = json.dumps(hd, separators=(',', ':')).encode()
        if os.path.exists(f'{B}/mc/{c_}.webp'): os.remove(f'{B}/mc/{c_}.webp')  # never write through a hardlink
        open(f'{B}/mc/{c_}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
    new = sorted(set(groups) - set(have))
    if new: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c_}' for c_ in new) + ']);', 1)
    print('amazon118: Amazon photos re-packed into chunks', sorted(groups))
    i = h.index('const D=') + 8; e = i + json.JSONDecoder().raw_decode(h[i:])[1]
for s in D['sets']:
    if s['slug'] in cr0: s['cr'] = cr0[s['slug']]
for k, o in D['mats'].items():
    if o.get('add') == 'oct26-amazon' and not o.get('pa') and not o.get('ncn'): o['ncn'] = 1; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:]; open(P, 'w').write(h)
print('amazon118: s.cr restored on', len(cr0), 'sets; ncn set on', n, 'Amazon mats;', sum(1 for o in D['mats'].values() if o.get('add') == 'oct26-amazon'), 'Amazon mats in build')
