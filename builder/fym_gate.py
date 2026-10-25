"""FYM publish gate. Run before EVERY publish of the Find Your Match artifact:
    python3 builder/fym_gate.py <build_dir>
Exits non-zero and prints every failure. Checks (add one for each bug type Tiffany reports):
 1  album / swipe-book sets show their canonical album tile photo (D.tiles[..].src == locked src, file exists, pixels match)
 2  no visible set without an album / swipe book carries a "Tiffany's match" list (m)
 3  no visible set flagged no_tiles (builder/fym_flags/tile_photo_flags.json); no visible mat flagged no_mat/partial_crop/no_flat_photo/duplicate (mat_photo_flags.json); 3b retired mats labelled in mat-door grid + mat search; 3d Questionable list hidden, no Paige Spearin newly in Holiday
 3c cleaned photos pinned in the flags (photo) stay in the build; props/lifestyle photos are OK (ok_fym_props, low bar Oct 21 pm); only locked mats on an unusable photo warn
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
 13h holiday exceptions (Tiffany Oct 21, final definition: Holiday = ONLY Christmas, Hanukkah, winter snowy/ski scenes). The ONLY mats
    allowed in Holiday AND colour sections / single chips are late-calls also_year_round (gallery: colours + 'holiday' last + co-primary;
    FYM: hol + ayr + mf); the ONLY year-round mats shown with Holiday are late-calls works_for_holiday (gallery row field 12, bottom of
    Holiday under the subheading; FYM wfh, setsForMat ok = hol || wfh). Mats she moved OUT of Holiday (late-calls primary = a colour,
    e.g. the pumpkin mats) never come back as holiday in the gallery or FYM.
 14 tile-photo identity (Oct 21 12:10, Heritage 1 photo on the Heritage 2.0 colour card): no FYM tile photo (full or pile) is another
    set's canonical album photo (builder/photo_identity_check.py, SIFT + RANSAC against assets/tiles/album/*)
 15 replaced racks (Oct 21 pm, QA: Papaya Spritz still showed PLM Oak as "Tiffany's match" from D.lt after the Beechwood swap): for every
    rack replacement in builder/fym_flags/rack_replacements.json, the old rack is in neither the set's D.lt nor any of its m rack lists,
    the new rack is in D.lt, and the key is a final_lists set whose list names the new rack (D.uni is not checked)
 16 pick order (Oct 21, Tiffany: Papaya Spritz picks started Greenly, Goldie, Preppy Pink; her live album starts Heiress, Press for
    Mahjong, Greenly): D.ao is recomputed from scripts/social/its_a_match/albums-live-oct21.json (builder/fym_fix_oct21/album_order.py)
    and must equal the build's D.ao; the page's own load-time sort, run in node, must put every album set's picks in live album order
 17 tool name (Oct 21): the start-screen title is "Find <i>Your</i> Mat-ch(TM)", (TM) exactly once in the UI, no "Find Your Match" text,
    and the .ttl headline is not text-transform:uppercase (brand guide: Title Case, never ALL CAPS)
 18 swipe row is X and heart only (Oct 21: an undo/rewind button sat in the row): no data-undo button / rewind glyph in the UI
 19 tiles-door colour chips clear (Oct 21: radio-style, Holiday could not be cleared): tapping the active chip sets S.tcol to '' and
    '' renders the whole list; Holiday may stay the season default (HOLIDAY_SEASON, Oct 14)
 20 phone orphan (Oct 21: "for" alone on its own line in the I have tiles door): door subtitles end in a non-breaking space + last
    word and .door button small has text-wrap:balance
 21 footer feedback link (Oct 21 launch): "Something look off or have an idea? Tell me here" -> find-your-mat-ch-feedback, new tab
 17 (Oct 21 6:30pm) title is plain "Find Your Mat-ch(TM)"; no italic in any headline. 18b labelled Back above the card, not in the X/heart row
 22 node run of the page's own code over Tiffany's Oct 21 paths (builder/fym_matdoor_check.js): mat-door pairing summary with working
    Change mat + Change tiles, See other mats deck swipes, no swipe copy on a locked/1-card deck, picks toggle only when it changes
    something, mock-up only from HER pick, racks tray max 2 with x/swap, Back x5 restores order, logo Start over with confirm
 23 racks tray / one card design in 3 sizes / "to save" code line / Save-Share without press-and-hold   24 zoom-out swipe not sticky
 25 m contains every swipe-book yes (builder/fym_flags/swipe_yeses_map.json)   26 Holiday chip   27 Start over   28 Photo coming soon card
 8b colour-chip order: sh (measured share) lines up with mf; CSORT (single chip) = lead > ONE list by score (share + 20 if primary),
    checked by running CSORT in node over every chip colour
 38 (Oct 22) card formats read Mood board / Close up
 37 (Oct 22) rack screen like the mat screen: picker under the mat, suitors at the bottom, one picks toggle, Back on racks
 36 (Oct 22) rack picks per (set, mat): every pairing = the mat's own picks (config/mat-racks-picks.json) first, then the tile set's
    racks, plus every rack on a structured album card for that pairing; every registry mat/rack resolves; D.lm matches the registry
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
    sp = REPO + lk['src']; fp = os.path.join(B, t.get('fo') or t['full'])  # v89: reframed photos are checked against their original (t.fo)
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
MAT_HIDE_FLAGS = ('no_mat', 'partial_crop', 'no_flat_photo', 'duplicate', 'too_far', 'covered', 'questionable')   # Oct 20 round 2: crops / no flat photo / duplicates stay hidden too
# Oct 21 8:03am (Tiffany, rule 6): too_far (shot from too far away), covered (tiles/racks hide the pattern), questionable (her review list) stay hidden
for mid, f in mflags.items():
    m = M.get(mid)
    if m and f.get('flag') in MAT_HIDE_FLAGS and not m.get('hid'):
        F.append(f"[3] mat {m['n']} ({m.get('bn')}): visible but photo flagged {f.get('flag')}")
# 3c. Oct 21 (QA: room shots / props on the mat / logo tile photos): a cleaned photo pinned in the flags ('photo') must stay in the build
#     while visible (no refresh may bring the old lifestyle shot back); locked mats still on a flagged photo are listed as a warning
for mid, f in mflags.items():
    m = M.get(mid)
    if m and f.get('photo') and not m.get('hid') and m.get('f') != f['photo']:
        F.append(f"[3c] mat {m['n']} ({m.get('bn')}): shows {m.get('f')} but its cleaned photo is {f['photo']} (mat_photo_flags.json)")
for s in D['sets']:
    f = tflags.get(s['slug']); t = T.get(s['tile'], {})
    if f and f.get('photo') and f.get('flag') == 'ok' and vis(s) and (t.get('fo') or t.get('full')) != f['photo']:
        F.append(f"[3c] {s['name']} ({s['maker']}): tile photo {t.get('full')} but its cleaned photo is {f['photo']} (tile_photo_flags.json)")
# Oct 21 pm (Tiffany, CLAUDE.md rule 6): the FYM photo bar is LOW. Props / tiles / racks / a room around the mat are fine
# (flag ok_fym_props, no warning). Only a locked mat whose photo is flagged unusable (wrong product, packaging, corner close-up:
# locked_needs_approval) is still listed while visible; unlocked unusable photos (no_mat / partial_crop / duplicate) FAIL in [3].
_lna = [M[k]['n'] for k, f in mflags.items() if f.get('flag') == 'locked_needs_approval' and k in M and not M[k].get('hid')]
if _lna:
    print(f"FYM GATE WARNING [3c]: {len(_lna)} locked mats show a photo flagged unusable (corner close-up / wrong product / packaging), waiting on Tiffany: " + ', '.join(_lna))
for k, f in mflags.items():
    if f.get('flag') == 'ok_fym_props' and k not in M: F.append(f"[3c] ok_fym_props flag for a mat not in the build: {k}")
# 3d. Oct 21 (Tiffany, rule 6 'when in doubt, pull it'): every mat on her Questionable for FYM list stays hidden until she says keep;
#     Paige Spearin x TdT collabs earn no commission: none may be newly brought into Holiday (Apres Mahj was holiday-tagged before Oct 21)
_qp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fym_flags', 'fym_questionable.json')
if os.path.exists(_qp):
    for it in json.load(open(_qp)).get('items', []):
        m = (D['racks'] if it.get('kind') == 'rack' else M).get(it['key'])   # Oct 25: racks with a bad photo go on the list too
        if m and not m.get('hid'): F.append(f"[3d] {m['n']} ({m.get('bn')}): on the Questionable for FYM list but visible")
for k, m in M.items():
    if 'paige spearin' in m['n'].lower() and (m.get('hol') or m.get('wfh') or m.get('ayr')) and k != 'tigredetartan.com/paige-spearin-mahjong-mat-apres-mahj':
        F.append(f"[3d] {m['n']}: Paige Spearin mat brought into Holiday (no commission, do not promote)")
# 3b. retired mats carry a Retired label in the mat-door grid / door search (matBtn) and the mat search list (#msr) (Oct 20 bug: Liberty)
mb = re.search(r'function matBtn\(id\)\{.*?\n', UI)
if not mb or "M[id].rt?" not in mb.group(0) or 'Retired' not in mb.group(0):
    F.append("[3b] matBtn (mat-door grid + door search) has no Retired label for rt mats")
ms = re.search(r"box\.innerHTML=hits\.length\?hits\.map\(id=>`<button type=\"button\" data-(?:mock|mfront).*?\n", UI)
if not ms or "M[id].rt?" not in ms.group(0) or 'Retired' not in ms.group(0):
    F.append("[3b] mat search list (#msr) has no Retired label for rt mats")

# 4. wording (UI text only; product names inside D, CSS and code comments are exempt)
TXT = re.sub(r'<style>.*?</style>', ' ', UI, flags=re.S); TXT = re.sub(r'/\*.*?\*/', ' ', TXT, flags=re.S)
for pat, why in ((r'(?<!Color )(?<!Pearl )\b[Cc]rush\b', 'crush'), (r'\bCRUSH\b', 'CRUSH'), (r'(?i)\bnope\b', 'nope'), (r'Pick your crush', 'Pick your crush'),
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
    if o.get('hol') and o.get('mf') and not o.get('hid') and not o.get('ayr'): F.append(f"[8] holiday mat {o['n']} is in single-colour chips {o['mf']} (only late-calls also_year_round may be)")

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
_AYR = set(LATE.get('also_year_round', {}).get('mats', {})); _WFH = set(LATE.get('works_for_holiday', {}).get('imgs', []))
_WFHK = {GKEY(i_) for i_ in _WFH} | set(LATE.get('works_for_holiday', {}).get('fym_keys', [])); _AYRK = {GKEY(i_) for i_ in _AYR}
for c in LATE['corrections']:
    r = GR.get(c['img'])
    if c.get('primary') == 'holiday':
        _ayr = c['img'] in _AYR
        if r is not None and (r[5] != ['holiday'] if not _ayr else ('holiday' not in r[5] or r[5][-1] != 'holiday' or 'holiday' not in (r[9] or []))):
            F.append(f"[13] holiday mat {r[1]} sections {r[5]} co-primary {r[9]} (late-calls: Holiday only, or colours + 'holiday' last for also_year_round)")
        k = GKEY(c['img'])
        if k in M and not M[k].get('hid') and ((M[k].get('mf') and not (_ayr and M[k].get('ayr'))) or not M[k].get('hol')): F.append(f"[13] holiday mat {M[k]['n']} in FYM single-colour chips {M[k].get('mf')} / hol={M[k].get('hol')} ayr={M[k].get('ayr')}")
    elif c.get('primary') and r is not None and ('holiday' in r[5] or (r[12] if len(r) > 12 else 0)):
        F.append(f"[13h] {r[1]}: late-calls primary {c['primary']} (moved out of Holiday) but it is back in Holiday {r[5]}")
    elif r is not None:
        for a in c.get('also', []):
            if a not in r[5]: F.append(f"[13] {r[1]}: Tiffany's also-colour {a} missing (sections {r[5]})")
        for a in c.get('remove', []):
            if a in r[5] or a in r[8] or a in (r[10] or []): F.append(f"[13] {r[1]}: colour {a} she removed is back")
        if c.get('floral') is False and 'florals' in r[5]: F.append(f"[13] {r[1]}: in Multicolor Florals (late-calls floral:false)")
if any(k_ != 'note' for k_ in XT.get('holiday_off', {})): F.append("[13] crosstags holiday_off is not empty (Tiffany Oct 20: holiday stays in Holiday)")
# 13h (Oct 21, Tiffany's final holiday definition): the two holiday exceptions are the ONLY mats in Holiday + colours / shown with Holiday
for r in _G:
    if 'holiday' in r[5] and r[5] != ['holiday'] and r[0] not in _AYR: F.append(f"[13h] {r[1]}: in Holiday AND colour sections {r[5]} but not on late-calls also_year_round")
    if (r[12] if len(r) > 12 else 0) and (r[0] not in _WFH or 'holiday' in r[5]): F.append(f"[13h] {r[1]}: shown under 'work for the holidays' but not a year-round late-calls works_for_holiday mat")
    if r[0] in _WFH and not (r[12] if len(r) > 12 else 0): F.append(f"[13h] {r[1]}: late-calls works_for_holiday but not flagged in the gallery row")
    if 'paige spearin' in r[1].lower() and ('holiday' in r[5] or (r[12] if len(r) > 12 else 0)) and 'apr' not in r[1].lower(): F.append(f"[13h] {r[1]}: Paige Spearin mat in Holiday (no commission)")
if 'Year-round mats that work for the holidays' not in _g or "c==='holiday'&&x[12]" not in _g: F.append("[13h] gallery Holiday section has no 'Year-round mats that work for the holidays' subheading / works_for_holiday handling")
for k, o in M.items():
    if o.get('ayr') and (k not in _AYRK or not o.get('hol')): F.append(f"[13h] FYM {o['n']}: ayr flag but not a holiday late-calls also_year_round mat")
    if o.get('wfh') and (k not in _WFHK or o.get('hol')): F.append(f"[13h] FYM {o['n']}: wfh flag but not a year-round late-calls works_for_holiday mat")
for k in _WFHK:
    if k in M and not M[k].get('wfh'): F.append(f"[13h] FYM {M[k]['n']}: late-calls works_for_holiday but no wfh flag")
for k in _AYRK:
    if k in M and not M[k].get('hid') and not (M[k].get('ayr') and M[k].get('hol') and M[k].get('mf')): F.append(f"[13h] FYM {M[k]['n']}: also_year_round but not hol + ayr + single chips")
for c in LATE['corrections']:
    k = GKEY(c.get('img', ''))
    if c.get('primary') and c['primary'] != 'holiday' and k in M and (M[k].get('hol') or M[k].get('wfh')): F.append(f"[13h] FYM {M[k]['n']}: moved out of Holiday (late-calls primary {c['primary']}) but hol/wfh in FYM")
if 'M[id].hol||M[id].wfh||!HOL.has(r.s.name)' not in UI: F.append("[13h] FYM setsForMat does not offer holiday tile sets for works_for_holiday (wfh) mats")
# 13c (Oct 21): measured colours Claude's photo check ruled out (brown/tan read as orange/red, gold as orange; config/mat-accent-photo-fixes.json)
# never come back, in the gallery or the FYM chips, unless it is a Tiffany call (late-calls also / v5 final_sections).
_PF = json.load(open(REPO + 'config/mat-accent-photo-fixes.json'))['mats']
_V5F = json.load(open(REPO + 'config/tiffany-color-notes/2026-10-20-v5-calls.json')).get('final_sections', {})
_LA = {c['img']: c.get('also', []) + ([c['primary']] if c.get('primary') else []) for c in LATE['corrections'] if c.get('img')}
for img_, fx_ in _PF.items():
    gone = (set(fx_.get('move', {})) | set(fx_.get('drop', [])) | set(fx_.get('drop_secs', []))) - set(_LA.get(img_, [])) - set(_V5F.get(img_, []))
    r = GR.get(img_)
    if r is None: continue
    for a in gone:
        if a in r[5] or a in r[8] or a in (r[11] or {}): F.append(f"[13c] {r[1]}: photo-checked colour {a} is back in the gallery (sections {r[5]}, accents {r[8]})")
    k = GKEY(img_)
    if k in M and not M[k].get('hid'):
        for a in gone:
            if a in (M[k].get('mf') or []): F.append(f"[13c] {M[k]['n']}: photo-checked colour {a} is back in FYM chips {M[k]['mf']}")
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

# 14. tile-photo identity (Tiffany Oct 21 12:10: Heritage 1 pictured on the Heritage 2.0 colour card). Every tile photo (full + pile)
# must not be ANOTHER set's canonical album photo (SIFT + RANSAC vs assets/tiles/album/*; builder/photo_identity_check.py).
try:
    from photo_identity_check import check_fym as _pic
    for f_ in _pic(B): F.append('[14] ' + f_)
except Exception as e_:
    F.append(f"[14] photo identity check could not run: {e_}")

# 15. replaced racks (Tiffany Oct 21 pm, rule 8: QA found PLM Oak still in D.lt['oh-my-mahjong-papaya-spritz'] after her Beechwood swap,
# so Oak kept a "Tiffany's match" badge in the her-picks rack deck). A rack she REPLACED in final_lists may not remain in that set's
# lt or m; the new rack must be in lt. D.uni (universal racks) is deliberately not checked.
_rr = json.load(open(REPO + 'builder/fym_flags/rack_replacements.json'))
_fl = json.load(open(REPO + 'config/tile-racks-picks.json'))['final_lists']
_sets_by = {}
for s_ in D['sets']: _sets_by.setdefault(s_['slug'], []).append(s_)
for k_, r_ in _rr.items():
    if k_.startswith('_'): continue
    sl_, old_, new_ = r_['set'], r_['old'], r_['new']
    if k_ not in _fl: F.append(f"[15] {k_}: rack replacement for a set with no final_lists entry"); continue
    if new_ not in D['racks']: F.append(f"[15] {k_}: new rack {new_} not in D.racks"); continue
    if D['racks'][new_]['n'] not in _fl[k_]: F.append(f"[15] {k_}: final_lists does not name the new rack {D['racks'][new_]['n']}")
    if old_ in D['racks'] and D['racks'][old_]['n'] in _fl[k_]: F.append(f"[15] {k_}: final_lists still names the replaced rack {D['racks'][old_]['n']}")
    if sl_ not in _sets_by: F.append(f"[15] {k_}: set {sl_} not in the build"); continue
    lt_ = (D.get('lt') or {}).get(sl_, [])
    if old_ in lt_: F.append(f"[15] {k_}: replaced rack {r_.get('old_name', old_)} still in D.lt['{sl_}'] (shows as Tiffany's match)")
    if new_ not in lt_: F.append(f"[15] {k_}: new rack {r_.get('new_name', new_)} missing from D.lt['{sl_}']")
    _bad = [e[0] for s_ in _sets_by[sl_] for e in s_['m'] if old_ in e[1]]
    if _bad: F.append(f"[15] {k_}: replaced rack {r_.get('old_name', old_)} still in {len(_bad)} m rack lists (e.g. {_bad[0]})")
    _lmb = [m_ for s_ in _sets_by[sl_] for m_ in {e[0] for e in s_['m']} if old_ in (D.get('lm') or {}).get(m_, [])]
    if _lmb: F.append(f"[15] {k_}: replaced rack {r_.get('old_name', old_)} in D.lm for its match-list mats {_lmb[:3]}")

# 16. Tiffany's picks follow her live album order (Oct 21, Papaya Spritz)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fym_fix_oct21'))
import album_order as _AO
_ao, _ = _AO.compute(D)
if (D.get('ao') or {}) != _ao: F.append("[16] D.ao missing or stale vs live album snapshot (run builder/fym_fix_oct21/album_order.py)")
_sortjs = re.search(r"D\.sets\.forEach\(s=>\{const o=\(D\.ao\|\|\{\}\)\[s\.slug\];.*?\}\);", UI)
if not _sortjs: F.append("[16] load-time album-order sort of s.m missing from the page")
else:
    _SS = [{'slug': s_['slug'], 'm': [[e[0], []] for e in s_['m']]} for s_ in D['sets'] if s_['slug'] in _ao]
    _o16, _e16 = _node('const D=' + json.dumps({'sets': _SS, 'ao': _ao}) + ';' + _sortjs.group(0) + 'process.stdout.write(JSON.stringify(Object.fromEntries(D.sets.map(s=>[s.slug,s.m.map(x=>x[0])]))))')
    if _o16 is None: F.append(f"[16] node failed running the page sort: {_e16}")
    else:
        for sl_, ord_ in _ao.items():
            got_ = [k for k in _o16[sl_] if k in set(ord_)]
            if got_ != ord_: F.append(f"[16] {sl_}: picks not in live album order (first: {[M[k]['n'] for k in got_[:3]]} vs {[M[k]['n'] for k in ord_[:3]]})")

# 17. tool name: Find Your Mat-ch(TM), italic Your, TM once (Oct 21)
if '<h1 class="ttl">Find Your Mat-ch\u2122</h1>' not in UI: F.append("[17] start-screen title is not plain 'Find Your Mat-ch\u2122' (Tiffany Oct 21 6:30pm: never italic in display type)")
if re.search(r'<h[12][^>]*>[^<]*<i>', UI) or re.search(r'\.lock \.ttl i\{[^}]*font-style:italic', UI): F.append("[17] italic in a headline (display type is never italic; italics only in running body text)")
_cardtm = TXT.count('Matched with Find Your Mat-ch\u2122')  # v80: the match card image is its own piece; its one full-name use carries the TM (brand guide)
if _cardtm > 1: F.append('[17] the match card carries the TM more than once')
if TXT.count('\u2122') - _cardtm != TXT.count('Find Your Mat-ch\u2122</h1>') or TXT.count('Find Your Mat-ch\u2122</h1>') < 2: F.append(f"[17] \u2122 must sit only on each door's title (both doors), found {TXT.count(chr(8482))}")
if re.search(r'(?i)find\s+(<i>)?your(</i>)?\s+match\b', TXT): F.append("[17] old name 'Find Your Match' still in the UI")
if re.search(r'\.lock \.ttl\{[^}]*text-transform:uppercase', UI): F.append("[17] .lock .ttl is ALL CAPS (brand guide: Title Case)")

# 18. swipe row: X and heart only (Oct 21: undo button)
if re.search(r'<button[^>]*data-undo=', TXT) or '\u21ba' in TXT or '↺' in TXT: F.append("[18] undo / rewind button in the swipe row (X and heart only)")
# 18b (Oct 21 6:37pm, Tiffany: a card she wanted flew by): a labelled "<- Back" just above the card, never in the X/heart row
_acts = fn('acts')
if 'data-back' in _acts: F.append("[18b] Back button inside the X/heart row (it belongs above the card)")
if 'data-back=\\"m\\"' not in UI and 'data-back="m"' not in UI: F.append("[18b] no labelled Back button above the mat card")
if "if(b=q('[data-back]')){undo(b.dataset.back)" not in UI: F.append("[18b] Back button does not undo the last swipe")

# 19. tiles-door colour chips can be cleared (Oct 21)
if "S.tcol=S.tcol===v?'':v" not in UI: F.append("[19] tiles-door colour chip does not toggle off (radio-style lock)")
if "S.tcol==='az'||S.tcol===''" not in fn('tileGrid'): F.append("[19] cleared tiles-door chips ('') do not render the full list")
if 'if(!S.tcol)S.tcol=' in UI: F.append("[19] falsy S.tcol re-selects the default chip (clearing impossible)")

# 20. phone orphan in door subtitles (Oct 21: 'for' alone on a line)
_ds = re.findall(r'data-door="[a-z]+"[^>]*>[^<]*<small>([^<]*)</small>', UI)
if len(_ds) < 2 or any('\u00a0' not in x_ for x_ in _ds): F.append(f"[20] door subtitles missing a non-breaking space before the last word: {_ds}")
if not re.search(r'\.door button small\{[^}]*text-wrap:balance', UI): F.append("[20] .door button small lacks text-wrap:balance")

# 21. feedback link in the footer (Oct 21, launch): opens the feedback page in a new tab
if not re.search(r'<footer class="fb"><a href="https://www\.mahjmatchmaker\.com/find-your-mat-ch-feedback" target="_blank" rel="noopener">', UI): F.append("[21] footer feedback link missing / wrong URL / not a new tab")

# 22 (Oct 21 6:20-6:44pm, Tiffany's phone tests): run the page's own code in node over every mat-door / tiles-door path
import subprocess as _sp
_r = _sp.run(['node', os.path.join(REPO, 'builder', 'fym_matdoor_check.js'), B], capture_output=True, text=True, timeout=300)
try:
    for f_ in json.loads(_r.stdout.strip().splitlines()[-1])['fails']: F.append('[22] ' + f_)
except Exception as e_: F.append(f"[22] mat-door check could not run: {e_} {_r.stderr[-300:]}")
# 23 racks tray (2 slots, x to remove, swap via suitors), one card design in 3 sizes, code line, save/share (no press-and-hold)
_tr = fn('tray')
if 'class="tray rtr"' not in _tr or 'data-rx' not in _tr or 'data-rp' not in _tr or '2 of 2' not in _tr or 'data-make' not in _tr or 'class="slots"' in _tr: F.append("[23] rack suitors tray (bottom, Oct 23): hearted racks with ✓ picks (max 2, unpick + pick to swap) + Make it official; no empty slots")
if "if(S.rpick.length>=2){toast(" not in UI or "S.rpick.shift()" in UI: F.append("[23] a 3rd rack can push one out of the tray without x (max 2, swap via x)")
_rr = fn('renderRacks')
if not (0 <= _rr.find("deck('r')") < _rr.find("tray('r')")) or 'Browsing racks' in UI: F.append("[23] racks step: suitors tray must sit after the rack deck, and no 'Browsing racks' tab (Oct 23 mirror)")
if re.search(r'(?i)press and hold', TXT): F.append("[23] press-and-hold save copy still in the UI (does not work on iPhone)")
if "claude.use('downloads')" not in UI or 'navigator.share' not in UI or 'Save / Share my match card' not in UI: F.append("[23] Save / Share button does not use downloads capability + navigator.share")
if not re.search(r"CARD_SIZES=\{story:\{w:1080,h:1920.*post:\{w:1080,h:1350.*pin:\{w:1000,h:1500", UI) or re.search(r'Facebook post|Pinterest pin', TXT): F.append("[23] card sizes are not Story 9:16 / Post 4:5 / Pin 2:3 (or old FB/Pin variants remain)")
if "' to save'" not in fn('codeLine') and 'to save' not in fn('codeLine'): F.append("[23] card code line does not say 'Use code ... to save'")
# 24 zoom (Oct 21 6:30pm: swiping sticky right after zoom-out): pinch end snaps ~1x to 1x and re-seeds the drag
_z = fn('zoomer')
if 'if(pinch&&pts.size<2){pinch=null;if(z.s<1.15)' not in _z or 'st=rest?' not in _z: F.append("[24] zoom-out does not hand the remaining finger straight back to swiping")
# 25 Tiffany's swipe-book yeses are in her match lists (Oct 21 6:44pm, Tinselle Ruby Red showed 2 of her ~25 yeses)
_ym = os.path.join(REPO, 'builder', 'fym_flags', 'swipe_yeses_map.json')
if os.path.exists(_ym):
    _sb = {s_['slug']: s_ for s_ in D['sets']}
    for sl_, ks_ in json.load(open(_ym)).items():
        s_ = _sb.get(sl_)
        if not s_: continue
        miss_ = [M[k]['n'] for k in ks_ if k in M and not M[k].get('hid') and k not in {e[0] for e in s_['m']}]
        if miss_: F.append(f"[25] {sl_}: {len(miss_)} swipe-book yeses missing from m (e.g. {miss_[:3]})")
        if s_['m'] and vis(s_) and not (s_.get('album') or s_.get('sb')): F.append(f"[25] {sl_}: has yeses but no album/sb flag (runtime guard blanks m)")
else: F.append("[25] builder/fym_flags/swipe_yeses_map.json missing (run builder/fym_fix_oct21/swipe_yeses.py)")
# 26 Holiday chip in the mat colour filters (Oct 21 6:44pm: 'How do I get to just all the holiday mats?')
if 'data-fam="holiday"' not in fn('filters') or 'data-dfam="holiday"' not in fn('doorChips') or 'M[id].hol||M[id].wfh' not in UI: F.append("[26] no Holiday chip (hol || wfh) in the deck / mat-door colour filters")
# 27 Start over from the top logo (confirm with a shortlist) + a Start over link near the top past the doors (Oct 21 6:32pm)
if "q('#logo')||q('[data-startover]')" not in UI or 'Start over?' not in UI or 'data-startover' not in UI: F.append("[27] top logo / Start over link missing or no confirm sheet")
# 28 Photo coming soon tile card (Oct 21 6:44pm) stays selectable
if 'function SOON(' not in UI or 'T[s.tile].soon?SOON(s)' not in UI: F.append("[28] 'Photo coming soon' tile card missing")
for k_, t_ in T.items():
    if t_.get('soon') and t_.get('hid'): F.append(f"[28] {t_.get('n')}: photo-coming-soon tile is hidden (must stay selectable)")

# 29 only full-size tile sets (Tiffany Oct 21 6:55pm: numbered flower packs in the picker): no visible partial / add-on tile product
_PART = re.compile(r'(?i)numbered[- ]flower|flower[- ](pack|tiles? pack|add)|add[- ]?on\b|\bsample\b|\bmini\b|\btravel\b|joker[- ](pack|set)|blank[- ]tiles?|for[- ]decor|\bdecor\b|\bevent\b|tastings?|flyer|tile[- ]takers|novelty|gift card|\bsold as individual')
for s_ in D['sets']:
    if not vis(s_): continue
    t_ = T[s_['tile']]
    if _PART.search(s_['name'] + ' ' + t_.get('n', '') + ' ' + (t_.get('u0') or t_.get('u', ''))) or (isinstance(t_.get('pc'), int) and t_['pc'] < 152):
        F.append(f"[29] {s_['name']} ({s_['maker']}): looks like a partial / add-on tile product (only full-size sets are matched)")
if any(vis(s_) for s_ in D['sets'] if s_['slug'] == 'wren-mats-simply'): F.append("[29] Simply (Wren Mats) visible (Tiffany Oct 21: bad photo, out of stock)")

# 30 tile photo audit (Oct 21, builder/fym_flags/tile_photo_upgrades.json): every upgrade applied; coming_soon only where switched on
_tu = os.path.join(REPO, 'builder', 'fym_flags', 'tile_photo_upgrades.json')
if os.path.exists(_tu):
    _sw = json.load(open(os.path.join(REPO, 'builder', 'fym_flags', 'tile_coming_soon_on.json'))) if os.path.exists(os.path.join(REPO, 'builder', 'fym_flags', 'tile_coming_soon_on.json')) else {}
    _on_all, _on = bool(_sw.get('all')), set(_sw.get('on') or [])
    _bt = {}
    for s_ in D['sets']: _bt.setdefault(s_['tile'], []).append(s_['slug'])
    for k_, it_ in json.load(open(_tu))['sets'].items():
        tk_ = it_.get('tile_key')
        if tk_ not in T or tk_ not in _bt: continue
        if it_['status'] == 'upgrade' and not str(T[tk_].get('fo') or T[tk_].get('full', '')).startswith('t71/'): F.append(f"[30] {it_['name']}: audit upgrade not applied (full {T[tk_].get('full')})")
        want_ = it_['status'] == 'coming_soon' and (_on_all or k_ in _on or any(x in _on for x in _bt[tk_]))
        if bool(T[tk_].get('soon')) != want_: F.append(f"[30] {it_['name']}: Photo coming soon is {'on' if T[tk_].get('soon') else 'off'} but the switch says {'on' if want_ else 'off'}")

# 30b one picker photo per tile (Oct 21 QA: a truncated pile key made 4 Heirloom sets show the same photo)
_pk = {}
for tk_, t_ in T.items():
    if t_.get('hid') or not any(s_['tile'] == tk_ and vis(s_) for s_ in D['sets']): continue
    _pk.setdefault(t_.get('pile'), []).append(t_.get('n') or tk_)
for k_, ns_ in _pk.items():
    if k_ and len(ns_) > 1: F.append(f"[30b] tiles share one picker photo key {k_}: {ns_[:4]}")

# 31 v72 optional tour + one-time hints (Tiffany Oct 21 6:37/6:38pm): offered once, stored, skippable; dock bounce with a reduced-motion glow
for need_, why_ in (("function tourOffer(", "first-run tour offer"), ("Want a quick tour?", "tour prompt copy"), ("data-tq-no", "Skip on the prompt"),
                    ("LS.set('fym_tour'", "tour done/skipped flag"), ("data-tour>Take the tour", "Take the tour link near the top"), ("@keyframes dock", "dock bounce"),
                    ("prefers-reduced-motion:reduce){.bnc", "reduced-motion glow"), ("hint('back'", "Back hint"), ("hint('picks'", "picks hint"), ("hint('colors'", "colours hint"), ("hint('mock'", "mock-up hint"),
                    ("try{return localStorage.getItem(k);}catch(e){return null;}", "guarded storage")):
    if need_ not in UI: F.append(f"[31] tour/hints: {why_} missing")
# 32 fast swipes are queued (QA v71: swipes < 300ms apart were dropped); a swipe is never half of a double-tap zoom
if 'decide(k,yes);requestAnimationFrame(' not in fn('fly') or 'setTimeout(()=>decide' in fn('fly'): F.append("[32] the next card waits for the fly animation (fast swipes get dropped)")
if 'else last=n;' in fn('zoomer') or 'last=(st&&lock===null&&!pinch)?Date.now():0;' not in fn('zoomer'): F.append("[32] a swipe can start a double-tap zoom (double tap must be two taps)")
# 33 deck tab never covers the card pills (QA v71 at 390: 'BROWSING RACKS' over 'Goes with everything')
if '.deck:has(.peekbar) .scard .hb' not in UI: F.append("[33] deck tab can overlap the card pill")
# 34 names / photos from v71 QA
if re.search(r'Editon', h): F.append("[34] typo 'Editon' (Blue Edition)")
if 'class="${T[id]?\'tcv\':\'\'}"' not in UI: F.append("[34] tile photo in Take them home can letterbox (Heritage 1.0)")

# 35 tour bubble never covers its target (QA v72: step 1/2 coach over the heart/X; colour dot off-screen in the chip row; desktop bubble far from target)
for need_, why_ in (("function coachPlace(", "bubble placed next to its target"), ("pointer-events:none;background:var(--navy)", "bubble lets touches through"),
                    ("p.scrollLeft+=", "chip row scrolled so the target dot is visible")):
    if need_ not in UI: F.append(f"[35] tour: {why_} missing")
if os.environ.get('FYM_GATE_SKIP_TOUR') != '1':
    import subprocess as _sp
    _r = _sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fym_tour_place_check.py'), B], capture_output=True, text=True, timeout=900)
    if _r.returncode != 0: F.append("[35] tour bubble covers its target / target off-screen at 390x664, 390x844 or 1280x800: " + ' '.join(l for l in _r.stdout.splitlines() if 'FAIL' in l)[:600])

# 36 rack picks per (set, mat) (Tiffany Oct 22: Amara + Chinoiserie Songbird showed the SET's racks, missing PLM Chartreuse).
# Every pairing = the mat's own picks (config/mat-racks-picks.json) first, then the tile set's racks; every rack on a structured
# album card (manifests/specs) for that pairing is present; every registry mat resolves to an app mat.
sys.path.insert(0, REPO + 'builder/fym_fix_oct22')
from rack_picks import expected as _rp_expected
_rp_lm, _rp_want, _rp_rep = _rp_expected(json.loads(json.dumps(D)))
for _k in ('unresolved_mats', 'unresolved_racks'):
    if _rp_rep[_k]: F.append(f"[36] config/mat-racks-picks.json {_k.replace('_', ' ')}: {json.dumps(_rp_rep[_k])[:300]}")
_rp_bad = []
for s in D['sets']:
    for e in s.get('m', []):
        cur = e[1] if len(e) > 1 else []
        if cur != _rp_want[(s['slug'], e[0])]: _rp_bad.append(f"{s['slug']} + {M.get(e[0], {}).get('n', e[0])}")
if _rp_bad: F.append(f"[36] {len(_rp_bad)} pairings' racks are not mat picks first + tile racks (run builder/fym_fix_oct22/rack_picks.py): " + '; '.join(_rp_bad[:8]))
if any((D.get('lm') or {}).get(k) != v for k, v in _rp_lm.items()): F.append("[36] D.lm is missing or differs from config/mat-racks-picks.json")

# 37 rack screen = MIRROR of the mat screen (Tiffany Oct 23 9:13am): chosen mat on top, rack swiper directly under it (same deck(),
# same ✕/♥ acts), rack suitors tray at the bottom; nothing (no slots/picker) between the mat and the swiper; one picks toggle; Back on racks
_rr = fn('renderRacks'); _rm = fn('renderMats'); _rm = _rm[_rm.find("head(2,'Mat-ching'"):]
def _order(src, parts):
    pos = [src.find(x) for x in parts]
    return all(p_ >= 0 for p_ in pos) and pos == sorted(pos)
if not _order(_rm, ["filters('m')", "tileView('m')", 'class="tcap"', "deck('m')", "acts('m')", "tray('m')"]): F.append("[37] mat screen order changed (filters, tiles, caption, deck, ✕/♥, suitors)")
# Oct 25 (Tiffany 14:36): on racks the Brand/colour row sits BETWEEN the mat picture and the rack cards (her husband never found it above the mat)
if not _order(_rr, ["matBand()", 'class="tcap"', 'class="rfil"', "filters('r')", "deck('r')", "acts('r')", "tray('r')"]): F.append("[37] rack screen order changed (mat, caption, brand/colour row, rack deck, ✕/♥, rack suitors)")
_between = _rr[_rr.find("matBand()"):_rr.find("deck('r')")]
if re.search(r"tray\(|slots|rSuitors|herBar", _between): F.append("[37] something sits between the mat and the rack swiper (no slots/picker there)")
if "herBar('r')" in _rr: F.append("[37] second Tiffany's picks toggle (herBar) still on the rack screen")
if "return kk==='m'&&herUseful(kk)?`<button type=\"button\" class=\"hb\"" not in UI: F.append("[37] the pill over the rack photo is still a picks toggle (keep one toggle on racks)")
if 'data-back="r"' not in UI: F.append("[37] Back button on the rack deck missing")
if 'class="slots"' in UI or 'function rSuitors(' in UI: F.append("[37] old empty rack slots / separate suitors tray still in the app")
# 38 card format names (Tiffany Oct 22 desktop note 6): the spread is "Mood board", the stacked close-ups are "Close up"
if "const VIEWS=[['tri','Mood board'],['stack','Close up']];" not in UI: F.append("[38] card formats must read Mood board / Close up (was Love triangle / Mood board)")

# 40 mat search on the mat screen (Tiffany Oct 23 3:21pm): a searched mat goes to the top of the MAT swiper, never straight to racks
_ms = UI[UI.find("if(e.target.id!=='msq')"):]
_ms = _ms[:_ms.find('\n')+600]
if 'data-mock' in _ms[:_ms.find("No mat by that name")]: F.append("[40] mat-search results jump to the racks (data-mock); they must put the mat on top of the mat swiper")
if 'S.mfront' not in fn('matDeck') or "q('[data-mfront]')" not in UI: F.append("[40] searched mat is not put on top of the mat deck")
# [41] v79 (Tiffany Oct 23 8:35-8:37pm): racks mirror the mats. Hearting never picks a rack; picked racks show on the deck
# (split for 2) and lock swiping; picks OFF = colour ranking with partners ahead of non-partners; a tapped mat suitor
# can go back to the deck or be removed (she got stuck on a suitor preview).
_dc = fn('decide')
if 'S.rpick.push' in _dc: F.append("[41] hearting a rack preselects it (nothing is picked until she taps a rack suitor)")
if "k==='r'&&S.rpick.length)return rpickView()" not in fn('deck') or 'rpv n${' not in UI: F.append("[41] picked racks are not shown on the deck under the mat")
if 'R[r].pa?0:1e5' not in fn('rackPool') or '!S.f.r.her' not in fn('rackPool'): F.append("[41] rack picks OFF does not re-rank by colour with partners first")
if 'data-unlike' not in fn('acts') or "q('[data-unlike]')" not in UI or 'keep swiping' not in fn('acts'): F.append("[41] a tapped mat suitor has no way back to swiping / no Remove from suitors")
if "'Make it a love triangle'" not in UI or 'wingman' in UI: F.append("[41] rack heading is not 'Make it a love triangle'")
# [42] v81 (Tiffany Oct 23 8:24 + 8:54pm): the mat door starts like the tiles door and swipes TILE SETS after the mat
_md = fn('renderMatDoor')
if 'tswipe(el,lock,m,g)' not in _md or 'Swipe on tiles' not in _md or 'data-tour' not in _md: F.append("[42] mat door: no tour link / 'Swipe on tiles' intro / tile-set swiper after picking the mat")
if "pairUp(i);jump('s-racks')" not in UI or 'data-dgrid="1"' not in UI or 'data-dgrid="0"' not in UI: F.append("[42] mat door: Add racks does not go straight to the racks, or no See all / Swipe instead toggle")
# [43] Oct 25 (Tiffany 14:39, website: "Couldn't draw the card here"): card images from another origin (jsDelivr on the website copy)
# must load with crossOrigin, or one photo taints the canvas and the card cannot be drawn/saved.
if "const lk=src=>" in UI and "i.crossOrigin='anonymous'" not in UI[UI.index('const lk=src=>'):UI.index('const lk=src=>') + 400]:
    F.append("[43] card image loader lk() does not set crossOrigin='anonymous' for http(s) images (website card breaks: tainted canvas)")
# [44] Oct 25 (Tiffany 14:43): the card's tile picture must be the SAME photo the shopper matched to on the swipe screen (tileFull), never a separate HD/listing photo.
if "hdOr('t',s.tile" in UI or 'Promise.resolve(tileFull(s)||pile(s)).then(lk)' not in UI:
    F.append("[44] match card tile photo is not the swipe-screen photo tileFull(s) (it must never pick a separate HD/listing photo)")
# [45] Oct 25 (Tiffany form Oct 24 9:45pm + 16:36: Boots & Bubbles blue tiles out of frame on the card). The Mood board band (3.87:1,
#      zoom 1.05, anchor t.bf or [.5,.45]) of every visible set's tile photo must be mostly tiles, not white background / a pouch gap.
if 'cover(tile,x,top,w,hT,22,1.05,...(T[s.tile].bf||[.5,.45]))' not in UI:
    F.append("[45] Mood board tile band does not use the per-photo anchor T[s.tile].bf")
def _band_tiles(path, bf):
    im = Image.open(path).convert('RGB'); Wd, Hd = im.size; k = max(3.87 / Wd, 1 / Hd) * 1.05; cw, ch = 3.87 / k, 1 / k
    x0 = (Wd - cw) * bf[0]; y0 = (Hd - ch) * bf[1]; a = np.asarray(im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((160, 42))).astype(int)
    return float(1 - ((a.min(2) > 225) & ((a.max(2) - a.min(2)) < 18)).mean())
BAND_MIN = 0.12  # white-faced close-ups read low; this catches bands that are basically empty
_b45 = []
for s in D['sets']:
    t = T.get(s['tile']) or {}
    if s.get('hid') or t.get('hid') or t.get('soon') or not t.get('full') or not os.path.exists(os.path.join(B, t['full'])): continue
    v = _band_tiles(os.path.join(B, t['full']), t.get('bf') or [.5, .45])
    if v < BAND_MIN: _b45.append(f"{s['name']} ({s['maker']}) {v:.2f}")
if _b45: F.append(f"[45] {len(_b45)} tile photos show mostly white in the match-card band (reframe in config/fym-tile-focus-oct25.json): " + '; '.join(_b45[:12]))
# [47] Oct 25 (Tiffany 16:51: Mac + Miller 'Heirloom Collection: Fire + Fortune Verdant Fortune' ran off the card). The card title
#      must wrap to two lines instead of overflowing, and no visible set name may be a broken scrape (unbalanced brackets, > 48 chars).
if '/* v89: too long for one line -> two balanced lines */' not in UI:
    F.append("[47] match card title has no two-line fallback (long names run off the card)")
for s in D['sets']:
    if s.get('hid'): continue
    n_ = s['name']
    if n_.count('(') != n_.count(')') or len(n_) > 48: F.append(f"[47] set name looks broken or too long for the card: {n_!r} ({s['maker']})")
# [48] Oct 25 (Tiffany 16:52): Mood board code bar spans only the 'Matched with ... mahjmatchmaker.com' line, not the full width
if "/* v89: bar spans the brand line (flame to .com) */" not in UI:
    F.append("[48] Mood board code bar is full width (should span the brand line)")
# [49] Oct 25 (Tiffany 16:55): Start over prompt opened at the bottom of the page on desktop. Every sheet opens via openSheet (at the tap when framed)
if UI.count("className='sheet'") != UI.count('openSheet(d)') + UI.count('openSheet(el)') or 'function openSheet(' not in UI:
    F.append("[49] a pop-up sheet is appended without openSheet() (it would open at the bottom of the page inside the artifact / website)")
# [46] Oct 25 (Tiffany 16:37): Mood board rack labels sit BELOW the racks (whole rack visible)
if 'racks(x+28,ry+14,w-56,hR-28,{fs:20,maxRow:230,below:true})' not in UI:
    F.append("[46] Mood board rack labels are not below the racks (below:true)")

if W:
    print(f"FYM GATE WARNING [9]: {sum(map(len, W.values()))} unmatched non-partner mats visible, brands pending Tiffany's decision (builder/fym_flags/nonpartner_pending.json):")
    for b, v in sorted(W.items()): print(f"  {b} ({len(v)}): " + ', '.join(v[:8]) + (' ...' if len(v) > 8 else ''))
if F:
    print(f"FYM GATE: FAIL ({len(F)} problems)")
    for f in F: print('  ' + f)
    sys.exit(1)
print(f"FYM GATE: PASS  (album sets checked: {len(seen)}, sets: {len(D['sets'])}, visible: {sum(1 for s in D['sets'] if vis(s))}, locks: tiles {len(locks['tiles'])} sets {len(locks['sets'])} mats {len(locks['mats'])})")
