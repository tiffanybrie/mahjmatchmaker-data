"""FYM publish gate. Run before EVERY publish of the Find Your Match artifact:
    python3 builder/fym_gate.py <build_dir>
Exits non-zero and prints every failure. Checks (add one for each bug type Tiffany reports):
 1  album / swipe-book sets show their canonical album tile photo (D.tiles[..].src == locked src, file exists, pixels match)
 2  no visible set without an album / swipe book carries a "Tiffany's match" list (m)
 3  no visible set flagged no_tiles (builder/fym_flags/tile_photo_flags.json); no visible mat flagged no_mat/partial_crop/no_flat_photo/duplicate (mat_photo_flags.json); 3b retired mats labelled in mat-door grid + mat search
 4  UI wording: no crush / nope / pass / "Pick your crush" / hard-coded "save 10%"
 5  colour-dot click selector bug (.dots [data-fam])
 6  locked values (builder/fym_flags/locks.json) unchanged
 7  misc: every T.full file exists, no relative shop URLs, no prototype email box, every <script src> exists
 8  colour chips (Oct 20 r3, multi-select approved): AND logic on mat-door chips + in-deck dots, tap again unselects, clear control,
    zero results show a friendly message and never lock (chips stay rendered); mt tiers line up with mf; holiday mats out of single chips
 9  non-partner lockout (CLAUDE.md): a visible mat of a non-partner brand must be allowed (builder/fym_flags/nonpartner_allow.json: brand,
    mat key, ShopMy link) or in an album / swipe-book set's match list; HARD FAIL for anything else (Oct 20 late: pending no longer warns)
 10 no discount-code claim for non-partner / ShopMy mats (pa false, dc empty)
 11 no set's Tiffany's-match list (m) references a hidden mat or a removed mat (config/mat-gallery-crosstags.json remove_mats imgs/brands),
    except her verified real picks in builder/fym_flags/m_hidden_ok.json (Amore Manor Garden bug, Oct 20)
 12 no Mahjong Studios mat visible in FYM or in the staged Mat Gallery (Tiffany Oct 20 22:31: tiles/racks stay, mats go); no removed
    gallery row back in site/livepatch/matgallery/matgallery-v5.html
 13 staged Mat Gallery (Oct 20 late): non-partner lockout hard FAIL, late-call holiday mats Holiday-only (gallery + FYM), her also/remove/floral
    calls present, holiday_off empty, lead/tail pins match late-calls, section sort = lead > ONE list by score > tail, where
    score = measured share of the colour + 20 if it is the mat's primary (ties: primary first, then name). Checked by RUNNING the page's
    sk + sort in node over every section (Oct 20 late: near-0% primaries sat above Coralia 40% / Pink Tiger 20% in Orange)
 8b colour-chip order: sh (measured share) lines up with mf; CSORT (single chip) = lead > ONE list by score (share + 20 if primary),
    checked by running CSORT in node over every chip colour
"""
import sys, os, json, re
import numpy as np
from PIL import Image, ImageOps
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
sys.path.insert(0, REPO + 'builder')
from fym_apply_locks import diffs

B = sys.argv[1]
h = open(os.path.join(B, 'index.html')).read()
i = h.find('const D=') + 8
D, end = json.JSONDecoder().raw_decode(h, i)
UI = h[:i] + h[end:]
T, M = D['tiles'], D['mats']
locks = json.load(open(REPO + 'builder/fym_flags/locks.json'))
tflags = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
mflags = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
albums = json.load(open(REPO + 'work/albums.json'))
F = []
vis = lambda s: not (s.get('hid') or T.get(s['tile'], {}).get('hid'))

def flat(p):
    im = Image.open(p).convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
def sig(im): return np.asarray(ImageOps.fit(im, (48, 48)).convert('L'), dtype=float)

# 1. album photos
alb_names = {a['tile'].lower() for a in albums}
ALIAS = {'heritage 1.0': 'heritage', 'miss classic jade': 'jade', 'miss classic malachite': 'malachite', 'classic tortoise': 'tortoise'}
seen = set()
for s in D['sets']:
    has_album = bool(s.get('album')) or bool(s.get('sb')) or ALIAS.get(s['name'].lower(), s['name'].lower()) in alb_names and not s.get('cat')
    if not has_album or s['slug'] in seen: continue
    seen.add(s['slug'])
    t = T[s['tile']]; lk = locks['tiles'].get(s['tile'])
    if not lk: F.append(f"[1] {s['name']}: album set has no locked album photo in locks.json"); continue
    if t.get('src') != lk['src']: F.append(f"[1] {s['name']}: tile src {t.get('src')!r} != album photo {lk['src']!r}"); continue
    sp = REPO + lk['src']; fp = os.path.join(B, t['full'])
    if not os.path.exists(sp): F.append(f"[1] {s['name']}: album photo missing {lk['src']}"); continue
    if not os.path.exists(fp): F.append(f"[1] {s['name']}: FYM photo file missing {t['full']}"); continue
    a, o = flat(sp), flat(fp)
    d = float(np.abs(sig(a) - sig(o)).mean())
    if d > 3 or abs(a.size[0] / a.size[1] - o.size[0] / o.size[1]) > 0.03:
        F.append(f"[1] {s['name']}: FYM photo {t['full']} is not the album photo {lk['src']} (pixel diff {d:.1f})")

# 2. her lists only on album / swipe-book sets
for s in D['sets']:
    if vis(s) and s['m'] and not (s.get('album') or s.get('sb')):
        F.append(f"[2] {s['name']} ({s['maker']}): has a Tiffany's-match list ({len(s['m'])}) but no album / swipe book")
if "D.sets.forEach(s=>{if(!(s.album||s.sb))s.m=[];})" not in UI:
    F.append("[2] runtime guard (album||sb) missing from the app script")

# 3. photo flags
for s in D['sets']:
    f = tflags.get(s['slug'])
    if f and f.get('flag') == 'no_tiles' and vis(s):
        F.append(f"[3] {s['name']} ({s['maker']}): visible but tile photo flagged no_tiles ({f.get('note','')})")
MAT_HIDE_FLAGS = ('no_mat', 'partial_crop', 'no_flat_photo', 'duplicate')   # Oct 20 round 2: crops / no flat photo / duplicates stay hidden too
for mid, f in mflags.items():
    m = M.get(mid)
    if m and f.get('flag') in MAT_HIDE_FLAGS and not m.get('hid'):
        F.append(f"[3] mat {m['n']} ({m.get('bn')}): visible but photo flagged {f.get('flag')}")
# 3b. retired mats carry a Retired label in the mat-door grid / door search (matBtn) and the mat search list (#msr) (Oct 20 bug: Liberty)
mb = re.search(r'function matBtn\(id\)\{.*?\n', UI)
if not mb or "M[id].rt?" not in mb.group(0) or 'Retired' not in mb.group(0):
    F.append("[3b] matBtn (mat-door grid + door search) has no Retired label for rt mats")
ms = re.search(r"box\.innerHTML=hits\.length\?hits\.map\(id=>`<button type=\"button\" data-mock.*?\n", UI)
if not ms or "M[id].rt?" not in ms.group(0) or 'Retired' not in ms.group(0):
    F.append("[3b] mat search list (#msr) has no Retired label for rt mats")

# 4. wording (UI text only; product names inside D, CSS and code comments are exempt)
TXT = re.sub(r'<style>.*?</style>', ' ', UI, flags=re.S); TXT = re.sub(r'/\*.*?\*/', ' ', TXT, flags=re.S)
for pat, why in ((r'(?<!Color )\b[Cc]rush\b', 'crush'), (r'\bCRUSH\b', 'CRUSH'), (r'(?i)\bnope\b', 'nope'), (r'Pick your crush', 'Pick your crush'),
                 (r'(?i)[>\'"`\s]pass[<\'"`\s,.!]|\bto pass\b|aria-label="Pass"', 'pass'), (r'(?i)save 10%', 'hard-coded 10%')):
    for m in re.finditer(pat, TXT):
        F.append(f"[4] UI text contains {why!r}: ...{TXT[max(0, m.start()-50):m.end()+30]!r}")
# 5. colour-dot selector
if ".dots [data-fam]" in UI: F.append("[5] colour-dot click selector '.dots [data-fam]' (dots live in .frow; filter can't switch)")

# 6. locks
for x in diffs(D, locks):
    F.append(f"[6] locked value changed: {x[0]} {x[1]} {x[2]} build={json.dumps(x[3], ensure_ascii=False)[:60]} locked={json.dumps(x[4], ensure_ascii=False)[:60]}")

# 7. misc
for k, t in T.items():
    if not os.path.exists(os.path.join(B, t['full'])): F.append(f"[7] tile photo file missing: {t['full']} ({t.get('n')})")
for kind in ('tiles', 'mats', 'racks'):
    for k, o in D[kind].items():
        if o.get('u', '').startswith('/'): F.append(f"[7] relative shop URL {kind} {k}: {o['u']}")
if 'class="mailbox"' in UI or 'function mail(' in UI: F.append("[7] prototype email box still present")
for src in re.findall(r'<script src="([^"]+)"', UI) + json.loads((re.search(r'window\.__LAZY=(\[[^\]]*\])', UI) or [None, '[]'])[1]):
    if not os.path.exists(os.path.join(B, src)): F.append(f"[7] script missing: {src}")

# 8. colour chips: multi-select AND, never locks (Oct 20 round 3)
def fn(name):
    m = re.search(r'(?:function ' + name + r'\(|const ' + name + r'=).*?(?=\n(?:function |const |let |document\.|/\*)|\Z)', UI, re.S)
    return m.group(0) if m else ''
if 'C.every(c=>MTI(id,c)<9)' not in fn('HASC'): F.append("[8] HASC (AND over selected colours) missing")
if 'HASC(id,C)' not in fn('matDeck'): F.append("[8] in-deck mat colour filter is not the multi-select AND filter")
if 'f.fam.every(' not in fn('rackDeck'): F.append("[8] in-deck rack colour filter is not the multi-select AND filter")
if 'HASC(id,C)' not in fn('doorMats') or 'CSORT(ids,C)' not in fn('doorMats'): F.append("[8] mat-door colour chips are not AND-filtered / tier-sorted")
if 'CSORT(' not in fn('matDeck'): F.append("[8] in-deck colour filter does not sort primary > also > accent")
if "f.fam=TOG(f.fam,b.dataset.fam)" not in UI or "S.dfams=TOG(S.dfams||[],b.dataset.dfam)" not in UI or 'C.includes(c)?C.filter(' not in fn('TOG'):
    F.append("[8] colour chips do not toggle (tap again to unselect)")
if 'data-dfam=""' not in UI or 'data-fam="" data-k=' not in UI or "[data-fclear]" not in UI: F.append("[8] clear / All colours control missing")
if 'No mats with all of those yet' not in fn('NOAND') or 'data-fclear' not in fn('deck') or 'NOAND' not in fn('deck'):
    F.append("[8] in-deck zero-result message (No mats with all of those yet) missing")
if UI.count('class="dempty">${NOAND}') < 2: F.append("[8] mat-door zero-result message missing (grid + search reset)")
if "filters('m')+" not in fn('renderMats'): F.append("[8] colour chips not rendered above the deck (filter could lock)")
if "fam:''" in UI or 'S.dfam=' in UI: F.append("[8] single-colour filter state left over (fam:'' / S.dfam)")
if 'D.lead' not in fn('CSORT') or '-(SHR(id,C[0])+20*p)' not in fn('CSORT') or 'Mahjong Studios' in fn('CSORT'):
    F.append("[8b] colour chips not sorted lead > ONE list by score (share + 20 if primary) (CSORT/SHR)")
import subprocess
def _node(js):
    r = subprocess.run(['node', '-'], input=js, capture_output=True, text=True)
    if r.returncode: return None, [l_ for l_ in r.stderr.splitlines() if 'Error' in l_][:1] or r.stderr[-200:]
    return json.loads(r.stdout), ''
def _score_order_bad(seq, score, prim):  # one list, high to low; equal score -> primary first
    for a_, b_ in zip(seq, seq[1:]):
        if score(a_) < score(b_) - 1e-9 or (abs(score(a_) - score(b_)) < 1e-9 and prim(a_) < prim(b_)): return (a_, b_)
    return None
_MS = {k: {f: o.get(f) for f in ('mf', 'mt', 'sh', 'ha', 'n')} for k, o in M.items() if not o.get('hid')}
_chips = sorted({c for o in _MS.values() for c in (o['mf'] or [])})
_js = ('const M=' + json.dumps(_MS) + ',D={lead:' + json.dumps(D.get('lead') or {}) + '};' + ';'.join(dict.fromkeys(x_ for x_ in (fn('SHR'), fn('MTI'), fn('CTIER'), fn('CSORT')) if not any(x_ != y_ and x_ in y_ for y_ in (fn('SHR'), fn('MTI'), fn('CTIER'), fn('CSORT'))))) +
       ';const o={};' + json.dumps(_chips) + '.forEach(c=>{o[c]=CSORT(Object.keys(M).filter(k=>(M[k].mf||[]).includes(c)).sort(),[c])});console.log(JSON.stringify(o))')
_out, _err = _node(_js)
if _out is None: F.append(f"[8b] could not run FYM CSORT in node: {_err}")
else:
    for c_, seq in _out.items():
        ld_ = [k for k in (D.get('lead') or {}).get(c_, []) if k in seq]
        if seq[:len(ld_)] != ld_: F.append(f"[8b] chip {c_}: lead mats not first in her order"); continue
        mid = seq[len(ld_):]; ix = lambda k: _MS[k]['mf'].index(c_)
        prim = lambda k: 1 if (_MS[k].get('mt') or [0] + [1] * 9)[ix(k)] == 0 else 0
        sc = lambda k: ((_MS[k].get('sh') or [])[ix(k)] if ix(k) < len(_MS[k].get('sh') or []) else 0) + 20 * prim(k)
        bad = _score_order_bad(mid, sc, prim)
        if bad: F.append(f"[8b] chip {c_}: {_MS[bad[0]]['n']} (score {sc(bad[0]):.1f}) sits above {_MS[bad[1]]['n']} (score {sc(bad[1]):.1f}); rule = share + 20 if primary, high to low")
for c_, ks_ in (D.get('lead') or {}).items():
    for k_ in ks_:
        if k_ not in M or M[k_].get('hid') or (M[k_].get('mf') or [None])[0] != c_: F.append(f"[8b] lead mat {k_} for {c_} missing, hidden or not {c_} primary")
for k, o in M.items():
    if len(o.get('sh') or []) != len(o.get('mf') or []): F.append(f"[8b] mat {o['n']}: sh shares {o.get('sh')} do not line up with mf {o.get('mf')}")
for k, o in M.items():
    if len(o.get('mt') or []) != len(o.get('mf') or []): F.append(f"[8] mat {o['n']}: mt tiers {o.get('mt')} do not line up with mf {o.get('mf')}")
    if o.get('hol') and o.get('mf') and not o.get('hid'): F.append(f"[8] holiday mat {o['n']} is in single-colour chips {o['mf']}")

# 9. non-partner lockout (warn for pending brands, fail otherwise)
NPA = json.load(open(REPO + 'builder/fym_flags/nonpartner_allow.json'))
NPP = json.load(open(REPO + 'builder/fym_flags/nonpartner_pending.json'))
nz = lambda s: re.sub(r'[^a-z0-9]', '', re.sub(r'^the\s+', '', (s or '').lower().replace('&', 'and')))
PARTNERS = {nz(b) for b in NPA['partners']}
matched = {x[0] for s in D['sets'] if (s.get('album') or s.get('sb')) and vis(s) for x in s['m']}
W = {}
for k, o in M.items():
    if o.get('hid') or nz(o.get('bn')) in PARTNERS: continue
    if o.get('bn') in NPA['brands'] or k in NPA['mats'] or o.get('u', '').startswith(NPA['shopmy_prefix']) or k in matched: continue
    F.append(f"[9] non-partner mat visible without Tiffany's OK: {o['n']} ({o.get('bn')}) {k}")
# 10. no code claim on non-partner / ShopMy mats
for k, o in M.items():
    if o.get('hid'): continue
    if (o.get('u', '').startswith(NPA['shopmy_prefix']) or nz(o.get('bn')) not in PARTNERS) and (o.get('pa') or o.get('dc')):
        F.append(f"[10] non-partner / ShopMy mat {o['n']} ({o.get('bn')}) claims a partner code (pa={o.get('pa')}, dc={o.get('dc')!r})")

# 11. no hidden / removed mat in any m list (except verified real picks)
XT = json.load(open(REPO + 'config/mat-gallery-crosstags.json'))
MAN = json.load(open(REPO + 'site/livepatch/matgallery/manifest.json'))
RMK = {MAN[i_] for i_ in XT['remove_mats'].get('imgs', []) if i_ in MAN}
RMB = set(XT['remove_mats'].get('brands', []))
MOK = {(a['set'], a['key']) for a in json.load(open(REPO + 'builder/fym_flags/m_hidden_ok.json'))['allowed']}
for s in D['sets']:
    for x in s['m']:
        o = M.get(x[0])
        if o is None: F.append(f"[11] {s['slug']}: m references unknown mat {x[0]}"); continue
        if (o.get('hid') or x[0] in RMK or o.get('bn') in RMB) and (s['slug'], x[0]) not in MOK:
            F.append(f"[11] {s['slug']}: Tiffany's-match list has hidden/removed mat {o['n']} ({o.get('bn')}) {x[0]}")
# 12. no Mahjong Studios mats (FYM + staged gallery); removed gallery rows stay out
for k, o in M.items():
    if not o.get('hid') and (o.get('bn') in RMB or k in RMK): F.append(f"[12] removed mat visible in FYM: {o['n']} ({o.get('bn')}) {k}")
_g = open(REPO + 'site/livepatch/matgallery/matgallery-v5.html').read()
_G = json.loads(re.search(r'<script type="application/json">(.*?)</script>', _g, re.S).group(1).replace('<\\/', '</'))
for r in _G:
    if r[2] in RMB or r[0] in set(XT['remove_mats'].get('imgs', [])): F.append(f"[12] removed mat in staged Mat Gallery: {r[1]} ({r[2]}) {r[0]}")

# 13. staged Mat Gallery: non-partner lockout (hard FAIL), late-call holiday mats Holiday-only, lead/tail pins + sort rule (Oct 20 late)
LATE = json.load(open(REPO + 'config/tiffany-color-notes/2026-10-20-late-calls.json'))
_N53 = json.load(open(REPO + 'site/livepatch/matgallery/new53_rows.json'))['manifest']
_RA = {a['gallery_id']: a['fym_key'] for a in json.load(open(REPO + 'site/livepatch/matgallery/retired_additions_oct20.json'))}
_RA.update({a['img']: a['key'] for a in json.load(open(REPO + 'config/mat-gallery-extra-rows.json'))['rows']})
GKEY = lambda img: MAN.get(img) or _N53.get(img) or _RA.get(img)
for r in _G:
    k = GKEY(r[0])
    if nz(r[2]) in PARTNERS or r[2] in NPA['brands'] or k in NPA['mats'] or (r[3] or '').startswith(NPA['shopmy_prefix']) or k in matched: continue
    if r[4] and k in M and M[k].get('rt'): pass
    F.append(f"[13] non-partner mat in staged Mat Gallery without Tiffany's OK: {r[1]} ({r[2]}) {r[0]}")
GR = {r[0]: r for r in _G}
for c in LATE['corrections']:
    r = GR.get(c['img'])
    if c.get('primary') == 'holiday':
        if r is not None and r[5] != ['holiday']: F.append(f"[13] holiday mat {r[1]} is in colour sections {r[5]} (late-calls: Holiday only)")
        k = GKEY(c['img'])
        if k in M and not M[k].get('hid') and (M[k].get('mf') or not M[k].get('hol')): F.append(f"[13] holiday mat {M[k]['n']} in FYM single-colour chips {M[k].get('mf')} / hol={M[k].get('hol')}")
    elif r is not None:
        for a in c.get('also', []):
            if a not in r[5]: F.append(f"[13] {r[1]}: Tiffany's also-colour {a} missing (sections {r[5]})")
        for a in c.get('remove', []):
            if a in r[5] or a in r[8] or a in (r[10] or []): F.append(f"[13] {r[1]}: colour {a} she removed is back")
        if c.get('floral') is False and 'florals' in r[5]: F.append(f"[13] {r[1]}: in Multicolor Florals (late-calls floral:false)")
if any(k_ != 'note' for k_ in XT.get('holiday_off', {})): F.append("[13] crosstags holiday_off is not empty (Tiffany Oct 20: holiday stays in Holiday)")
_lt = re.search(r'LD=(\{.*?\}),TL=(\{.*?\}),IB=', _g)
if not _lt or json.loads(_lt.group(1)) != LATE.get('lead', {}) or json.loads(_lt.group(2)) != LATE.get('tail', {}):
    F.append("[13] gallery lead/tail pins differ from late-calls lead/tail")
for sec_, imgs_ in list(LATE.get('lead', {}).items()) + list(LATE.get('tail', {}).items()):
    for img_ in imgs_:
        r = GR.get(img_)
        if r is not None and sec_ not in r[5] and sec_ not in r[8]: F.append(f"[13] pinned mat {r[1]} is not in section {sec_}")
# sort rule (Oct 20 late, final): lead pins > ONE list by score (share + 20 if primary; ties primary first, then name) > tail pins.
# Runs the page's own sk/has/sort in node over every section, then checks the order in Python.
_sk = re.search(r'function sk\(x,c\)\{.*?\}(?=/\*)', _g); _has = re.search(r'function has\(x,c,m\)\{.*?\}(?=function tier)', _g)
_srt = re.search(r'L\.sort\(function\(a,b\)\{function k\(i\).*?\}\);', _g)
_secs = [c_ for c_ in re.findall(r'class="mmg-sec" data-c="([^"]+)"', _g) if c_ != 'retired']
if not (_sk and _has and _srt and _lt) or 'Mahjong Studios' in _sk.group(0):
    F.append("[13] gallery section sort (sk / sort) not found or still has a brand rule")
else:
    _js = ('const R=' + json.dumps(_G) + ',LD=' + _lt.group(1) + ',TL=' + _lt.group(2) + ';' + _sk.group(0) + _has.group(0) +
           ';const o={};' + json.dumps(_secs) + '.forEach(c=>{var L=[];R.forEach(function(x,i){if(has(x,c))L.push(i)});' + _srt.group(0) +
           'o[c]=L});console.log(JSON.stringify(o))')
    _out, _err = _node(_js)
    if _out is None: F.append(f"[13] could not run gallery sort in node: {_err}")
    else:
        for c_, seq in _out.items():
            rows = [_G[i] for i in seq]; ids = [r[0] for r in rows]
            ld_ = [i for i in LATE.get('lead', {}).get(c_, []) if i in ids]; tl_ = [i for i in LATE.get('tail', {}).get(c_, []) if i in ids]
            if ids[:len(ld_)] != ld_ or (tl_ and ids[-len(tl_):] != tl_): F.append(f"[13] section {c_}: lead/tail pins not at top/bottom in her order"); continue
            mid = rows[len(ld_):len(rows) - len(tl_)]
            prim = lambda r: 1 if (c_ in [r[5][0]] + (r[9] or []) and c_ in r[5]) else 0
            sc = lambda r: (r[11] or {}).get(c_, 0) + 20 * prim(r)
            bad = _score_order_bad(mid, sc, prim)
            if bad: F.append(f"[13] section {c_}: {bad[0][1]} (score {sc(bad[0]):.1f}) sits above {bad[1][1]} (score {sc(bad[1]):.1f}); rule = share + 20 if primary, high to low")
if D.get('lead', {}).get('green') != [GKEY(i) for i in LATE['lead']['green']]: F.append("[13] FYM D.lead.green differs from late-calls lead.green")

if W:
    print(f"FYM GATE WARNING [9]: {sum(map(len, W.values()))} unmatched non-partner mats visible, brands pending Tiffany's decision (builder/fym_flags/nonpartner_pending.json):")
    for b, v in sorted(W.items()): print(f"  {b} ({len(v)}): " + ', '.join(v[:8]) + (' ...' if len(v) > 8 else ''))
if F:
    print(f"FYM GATE: FAIL ({len(F)} problems)")
    for f in F: print('  ' + f)
    sys.exit(1)
print(f"FYM GATE: PASS  (album sets checked: {len(seen)}, sets: {len(D['sets'])}, visible: {sum(1 for s in D['sets'] if vis(s))}, locks: tiles {len(locks['tiles'])} sets {len(locks['sets'])} mats {len(locks['mats'])})")
