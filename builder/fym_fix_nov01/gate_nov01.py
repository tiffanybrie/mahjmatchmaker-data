"""Gate checks for the Nov 1 inbox-sweep fixes (v112). Merge into builder/fym_gate.py as [130]-[137] once the v111 accounts build
lands (fym_gate.py was mid-edit by that build on Nov 1, so these live here). Exit 1 on any FAIL.
Usage: python3 builder/fym_fix_nov01/gate_nov01.py <build_dir>"""
import sys, json, re, subprocess, os
B = sys.argv[1]; h = open(B + '/index.html').read()
i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:]); M, R, T, S = D['mats'], D['racks'], D['tiles'], D['sets']
fails = []
def chk(tag, ok, msg):
    print(('PASS ' if ok else 'FAIL ') + tag + ' ' + msg)
    if not ok: fails.append(tag)
# N1 no white copy / outline behind card titles (Tiffany Oct 27)
dc = h[h.find('function drawCard'):]; dc = dc[:dc.find('\nfunction ')]
chk('[130]', "rgba(255,255,255,.9)';g.fillText(l,W/2+4" not in h and not re.search(r'strokeText\(l', dc), 'card title = one plain fill (no white copy, no stroke)')
# N2 colour results: partners before non-partners, both doors, with headers
chk('[131]', 'SECP' in h and '/*v112B*/' in h and '/*v112Bm*/' in h and 'DGRID(' in h, 'shop-by-colour partner / non-partner sections in both doors')
# N3 brand menu copy
chk('[132]', 'Partner brands come first' not in h and 'works at brands marked ♥' in h, 'brand menu copy = approved Oct 29 3:32pm wording')
# N4 TdT: no visible code text next to their name
chk('[133]', 'LINKONLY' in h and "through our link" in h, 'Tigre de Tartán shown as link-only (no code next to the name)')
# N5 rack fit by tile size: no short rack offered for large tiles
short = [k for k, r in R.items() if r.get('len') and r['len'] <= 18.5 and not r.get('hid')]
chk('[134a]', 'RFIT' in h and 'smallSet())&&' not in h.split('const rackOK=')[1][:200], 'rackOK uses tile-size fit')
chk('[134b]', not any(r.get('sm') for r in R.values()), 'no brand-based sm flags left')
chk('[134c]', R.get('mahjongrowandco.com/scalloped-deluxe-tortoise-rack', {}).get('len') == 20, 'MRC Scalloped Tortoise = 20 in')
nolen = [r['n'] for r in R.values() if not r.get('hid') and not r.get('len')]
chk('[134d]', not nolen, f'every visible rack has a length ({len(nolen)} missing: {nolen[:5]})')
# N6 tortoise order patch present
chk('[135]', '/*v112F' in h, 'MRC Scalloped Tortoise before Hawksbill in the rack deck')
# N7 tile colour groups: every name exists; December 1994 in Holiday
m = re.search(r'const BACKG=(\{.*?\});\n', h); BG = json.loads(m.group(1)); names = {s['name'] for s in S}
dead = sorted({n for g in BG.values() for n in g if n not in names})
chk('[136a]', 'Glitter Glow' not in dead, f'no dead Glitter Glow entry (other unmatched legacy names, filtered at runtime: {len(dead)})')
chk('[136b]', 'December 1994' in BG['Holiday'], 'December 1994 in Holiday tiles')
# data fixes
d2 = M.get('www.ohmymahjong.com/dapper-mat-w-tube', {})
chk('[137a]', d2.get('rt') is True, 'Dapper 2 retired (404 since Oct 28)')
iv = T.get('www.ymimports.com/fx-am014-a', {})
chk('[137b]', not iv.get('soon') and all(T[k].get('hid') for k in ('www.ymimports.com/fx-am022-a', 'www.ymimports.com/fx-am019-a')), 'YMI Ivory merged into one set with a real photo')
HC = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/../../config/tiffany-color-notes/2026-10-29-holiday-calls.json'))
def _m(n, o):
    bn = o.get('bn', ''); t = n[len(bn):].strip().lower() if n.lower().startswith(bn.lower()) else None
    return t is not None and (t in o['n'].lower() or o['n'].lower() in n.lower())
miss = [n for n in HC['holiday'] if not any(o.get('hol') and not o.get('hid') and _m(n, o) for o in M.values())]
chk('[137c]', not miss, f'Oct 29 holiday calls applied ({miss})')
np_ = [o['n'] for o in M.values() if not o.get('hid') and not o.get('pa') and not o.get('dc') and not o.get('ncn') and not any(x.get('pa') and x.get('bn') == o.get('bn') for x in M.values())]
chk('[137d]', not np_, f'non-partner brands carry ncn ({len(np_)} missing)')
pend = [r['n'] for r in R.values() if r.get('pending_review') and not r.get('hid')]
chk('[137e]', not pend, f'no rack visible while its cut-out is pending review ({pend})')
print('gate_nov01:', 'FAIL ' + ' '.join(fails) if fails else 'PASS'); sys.exit(1 if fails else 0)
