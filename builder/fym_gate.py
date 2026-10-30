"""FYM publish gate. Run before EVERY publish of the Find Your Match artifact:
    python3 builder/fym_gate.py <build_dir> [--release]   (--release: [104] version match artifact = website copy = README pin FAILS instead of warning)
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
 82-90 (Oct 26 evening, v97 = Version 1.1): 82 searched mat cleared on reset/new set (node-run resetFrom), 83 accent-blind search (node-run
    NRM over every accented name), 84 mat-door Add racks, 85 no set hidden by a stale no_tiles flag + Jubilee Midnight Blue, 86 PLM band
    framing, 87 MFM Natural Wood featured + no 404 wood-rack link, 88 PLM painted racks re-cut, 89 mat photos without white bands (warn:
    angled shots), 90 gallery sync (warn)
 100 (Oct 27, v101 = Version 1.5): missing partner mats from the last launch-watch sweep (config/partner-mat-sweep.json; no network)
 91-94 (Oct 26 night, v98 = Version 1.2): 94 PLM rack colours vs reference + locked approved Chartreuse/Dark Green; 95 card title = assigned s.tc; 96 names without stray quotes + Wren logo; 91 match card racks low + tight + equal length, stack photos big, off the mat's left (partner-graphics layout), 92 Mahjong Register single
    racks (no stacks) + Mahj Mood angled scalloped rack, 93 Desert Dreams Up close strip framing; [89] now FAILS if a v98-flattened
    mat loses its flat photo
"""
import struct
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
                 (r'(?i)[>\'"`\s]pass[<\'"`\s,.!]|\bto pass\b|aria-label="Pass"', 'pass'), (r'(?i)save 10%(?! or more)', 'hard-coded 10%')):  # Oct 29 Tiffany 12:11pm: the generic "save 10% or more with code MAHJMATCH" on partner brands is her wording; a bare/brand-specific % is still banned
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
if "const c=f.fam[0];ids=ids.filter(r=>(R[r].rf||[]).includes(c))" not in fn('rackDeck'): F.append("[8] in-deck rack colour filter is not the single-colour filter (Tiffany Oct 25 17:08: one rack colour at a time)")
if 'HASC(id,C)' not in fn('doorMats') or 'CSORT(ids,C)' not in fn('doorMats'): F.append("[8] mat-door colour chips are not AND-filtered / tier-sorted")
if 'CSORT(' not in fn('matDeck'): F.append("[8] in-deck colour filter does not sort primary > also > accent")
if "f.fam=PICK(b.dataset.k,f,b.dataset.fam)" not in UI or "S.dfams=PICK('m',f,b.dataset.dfam)" not in UI or 'C.includes(c)?C.filter(' not in fn('TOG'):
    F.append("[8] colour chips do not toggle (tap again to unselect)")
if 'data-dfam=""' not in UI or 'data-fam="" data-k=' not in UI or "[data-fclear]" not in UI: F.append("[8] clear / All colours control missing")
if 'No mats with all of those yet' not in fn('NOAND') or 'data-fclear' not in fn('deck') or 'NOAND' not in fn('deck'):
    F.append("[8] in-deck zero-result message (No mats with all of those yet) missing")
if UI.count('class="dempty">${NOAND}') < 2: F.append("[8] mat-door zero-result message missing (grid + search reset)")
if "${filters('m')}</div>${deck('m')}" not in fn('renderMats'): F.append("[8] colour chips not rendered right above the mat deck (filter could lock)")
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
# v104 (Tiffany Oct 29 3:31pm): a cleared chip ('') shows the partner brand LOGOS (the full list is one tap away: All A-Z); never a locked/empty view
if "S.tcol==='az'" not in fn('tileGrid') or "if(S.tcol==='')return blogoView();" not in fn('tileGrid'): F.append("[19] cleared tiles-door chips ('') do not render the brand logos / All A-Z list")
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
if "if(S.rpick.length>=2){const old=S.rpick.shift();toast(" not in UI: F.append("[23] a 3rd rack pick does not swap out the older pick (Tiffany Oct 25 20:08; max 2)")
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
        if it_['status'] == 'upgrade' and not str(T[tk_].get('fo') or T[tk_].get('full', '')).startswith('t71/') and not (it_.get('applied') and T[tk_].get('src') == it_.get('proposed')): F.append(f"[30] {it_['name']}: audit upgrade not applied (full {T[tk_].get('full')})")
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
        _lm36 = (_rp_lm or {}).get(e[0]) or []
        if not all(r in cur for r in _lm36): _rp_bad.append(f"{s['slug']} + {M.get(e[0], {}).get('n', e[0])}")   # v90 (Tiffany Oct 25 17:10): her mat picks lead; tile racks moved to D.ltc
if _rp_bad: F.append(f"[36] {len(_rp_bad)} pairings' racks are missing her mat picks (config/mat-racks-picks.json): " + '; '.join(_rp_bad[:8]))
if any((D.get('lm') or {}).get(k) != v for k, v in _rp_lm.items()): F.append("[36] D.lm is missing or differs from config/mat-racks-picks.json")

# 37 rack screen = MIRROR of the mat screen (Tiffany Oct 23 9:13am): chosen mat on top, rack swiper directly under it (same deck(),
# same ✕/♥ acts), rack suitors tray at the bottom; nothing (no slots/picker) between the mat and the swiper; one picks toggle; Back on racks
_rr = fn('renderRacks'); _rm = fn('renderMats'); _rm = _rm[_rm.find("head(2,'Mat-ching'"):]
def _order(src, parts):
    pos = [src.find(x) for x in parts]
    return all(p_ >= 0 for p_ in pos) and pos == sorted(pos)
if not _order(_rm, ["tileView('m')", 'class="tcap"', "filters('m')", "deck('m')", "acts('m')", "tray('m')"]): F.append("[37] mat screen order changed (tiles, caption, filters, deck, ✕/♥, suitors; v91 Tiffany Oct 25 20:03)")
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
if "k==='r'&&S.rpick.length)return rpickView()" in fn('deck'): F.append("[41] picked racks replace the rack deck (it must keep swiping; Tiffany Oct 25 20:08)")
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
# Oct 26 (Tiffany 11:55, Rackin' Rudolph Canva v2): a tile may carry T.cf = a circle crop of the SAME photo as its swipe-screen strip
# (the strip cannot centre the backs). Allowed only for tiles listed in config/fym-tile-circle-crops-oct26.json.
_cf44 = json.load(open(REPO + 'config/fym-tile-circle-crops-oct26.json'))['tiles'] if os.path.exists(REPO + 'config/fym-tile-circle-crops-oct26.json') else {}
_ok44 = ('Promise.resolve(tileFull(s)||pile(s)).then(lk)' in UI) or ('Promise.resolve((T[s.tile].cf&&!T[s.tile].soon?T[s.tile].cf:tileFull(s))||pile(s)).then(lk)' in UI)
if "hdOr('t',s.tile" in UI or not _ok44:
    F.append("[44] match card tile photo is not the swipe-screen photo tileFull(s) (it must never pick a separate HD/listing photo)")
for _k44, _t44 in T.items():
    if _t44.get('cf') and (_k44 not in _cf44 or _cf44[_k44].get('cf') != _t44['cf'] or _cf44[_k44].get('full') != _t44.get('full')):
        F.append(f"[44] {_t44.get('n')}: card circle photo cf={_t44['cf']} is not a listed crop of its swipe-screen photo (config/fym-tile-circle-crops-oct26.json)")
# [45] Oct 25 (Tiffany form Oct 24 9:45pm + 16:36: Boots & Bubbles blue tiles out of frame on the card). The Mood board band (3.87:1,
#      zoom 1.05, anchor [.5,.45]) of every visible set's tile photo must be mostly tiles, not white background / a pouch gap.
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
if "/* v89: Mood board (tri) bar spans the brand line (flame to .com) */" not in UI:
    F.append("[48] Mood board code bar is full width (should span the brand line)")
# [49] Oct 25 (Tiffany 16:55): Start over prompt opened at the bottom of the page on desktop. Every sheet opens via openSheet (at the tap when framed)
if UI.count("className='sheet'") != UI.count('openSheet(d);}') + UI.count('openSheet(el)') or 'function openSheet(' not in UI:
    F.append("[49] a pop-up sheet is appended without openSheet() (it would open at the bottom of the page inside the artifact / website)")
# [50] Oct 25 (Tiffany 16:58: Splash of Color Preppy Animal Print was a far-away living-room render). Mats whose photo shows the mat too
#      small (config/fym-mat-focus-oct25.json, action crop) must show the cropped photo (M.f0 = original); too_far ones stay hidden.
_mfp = os.path.join(REPO, 'config', 'fym-mat-focus-oct25.json')
if os.path.exists(_mfp):
    for k_, fo_ in json.load(open(_mfp)).items():
        m_ = M.get(k_)
        if not m_ or m_.get('hid'): continue
        if fo_.get('action') == 'crop' and not m_.get('f0'): F.append(f"[50] {m_['n']} ({m_.get('bn')}): far-away / room photo not cropped to the mat")
        if fo_.get('action') == 'too_far': F.append(f"[50] {m_['n']} ({m_.get('bn')}): photo too far away but visible (hide it + Questionable list)")
# [51] Oct 25 (Tiffany 17:10: Birdie + Luna led with the tile rack Hot Pink; her Luna album pick is PLM Oak + OMM White Acrylic).
#      Every mat's rack list in FYM = her album 'Rack matches' for that mat, in order; tile racks live in D.ltc and only show when they fit the mat.
_arp = os.path.join(REPO, 'config', 'album-rack-picks.json')
if 'const rackFits=' not in UI or 'D.ltc' not in UI: F.append("[51] herRacks() does not put her per-mat racks first / filter tile racks by the mat's colours")
if os.path.exists(_arp):
    _AR = json.load(open(_arp)); _bad = []
    for s_ in D['sets']:
        al_ = _AR.get(s_['slug']) or {}
        for k_, r_ in s_['m']:
            e_ = al_.get(k_)
            _lm51 = [r for r in (D.get('lm') or {}).get(k_, []) if r in D['racks']]
            if e_ and e_.get('mat') and not e_.get('shown') and r_ != list(dict.fromkeys(e_['mat'] + _lm51)): _bad.append(f"{s_['name']} + {M[k_]['n'] if k_ in M else k_}")
    if _bad: F.append(f"[51] {len(_bad)} mats' rack picks differ from the live album page: " + '; '.join(_bad[:8]))
# [52] Oct 25 (Tiffany 17:08): rack colour chips are single-select; Tortoise leads with Middle & Main Hawksbill Heritage; Mahjong Studios never
#      leads a chip; seasonal / metallic-only racks (Santa Baby, Trust Fund) sit in Metallic, not a colour; '+ Add a colour' combine mode on mats
if "const PICK=(k,f,c)=>" not in UI or "if(k==='r')return f.fam[0]===c?[]:[c];" not in UI or 'data-fmulti' not in UI:
    F.append("[52] colour chips: racks not single-select / mats missing single-select + '+ Add a colour'")
_RR = {k: r for k, r in D['racks'].items() if not r.get('hid')}
for c_ in ('pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'neutral', 'brown', 'black', 'wood', 'tortoise', 'metallic', 'clear'):
    _l = sorted([k for k, r in _RR.items() if c_ in (r.get('rf') or [])], key=lambda k: -(_RR[k].get('rs') or {}).get(c_, 0))
    if _l and 'Mahjong Studios' in (_RR[_l[0]].get('bn') or ''): F.append(f"[52] Mahjong Studios leads the {c_} rack chip ({_RR[_l[0]]['n']})")
    if c_ == 'tortoise' and _l and _l[0] != 'mm:Hawksbill': F.append(f"[52] Tortoise rack chip does not lead with Middle & Main Hawksbill Heritage ({_RR[_l[0]]['n']})")
for k, r in _RR.items():
    if re.search(r'santa baby|trust fund', r['n'], re.I) and set(r.get('rf') or []) - {'metallic', 'clear'}: F.append(f"[52] {r['n']} sits in a colour chip {r.get('rf')} (metallic / seasonal only)")
# [53] Oct 25 (Tiffany 20:03): the mat filter row sits between the tile photo and the mat deck (it filters the mats), like the racks row
if "<div class=\"rfil mfil\">${filters('m')}</div>${deck('m')}" not in UI or "role=\"listbox\"></div></div>`+filters('m')" in UI:
    F.append("[53] mat filter row is not between the tile photo and the mat deck")
# [54] Oct 25 (Tiffany 20:07): the texted / emailed shop list has one block per piece with a blank line between
if "${L.join('\\n\\n')}" not in UI or "${kind} \\u00b7 ${nm} by ${o.bn}\\n${o.u" not in UI:
    F.append("[54] 'Text or email me this list' is not one block per piece with blank lines between")
# [55] Oct 25 (Tiffany 20:02/20:08): the rack deck never locks after picking; a 3rd pick swaps out the older one
if 'class="rlock"' in UI or "function deck(k){if(k==='r'&&S.rpick.length)return rpickView();" in UI or "const old=S.rpick.shift();" not in UI:
    F.append("[55] rack deck locks after a pick / no swap on a third pick")
# [56] Oct 25 (Tiffany 21:42, 2nd report of jagged Bespoke rack cutouts): every rack photo shown must be reviewed 'ok'
#      in builder/fym_flags/rack_image_review.json (contact sheet on white AND navy: builder/fym_rack_images.py --sheet)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fym_rack_images import problems as _rack_img_problems
_rp = _rack_img_problems(B)
if _rp: F.append(f"[56] {len(_rp)} rack photos not reviewed / rejected cutout: " + '; '.join(_rp[:6]))
# [57] Oct 25 (Tiffany 20:24): a brand's coordinated mats come first for its tile set (config/fym-coordinated.json)
_co = {k: v for k, v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-coordinated.json'))).items() if not k.startswith('_')}
for _s in D['sets']:
    if _s['slug'] in _co:
        _want = [m for m in _co[_s['slug']] if m in D['mats'] and not D['mats'][m].get('hid')]
        for _f in ('cr', 'rank'):
            _lst57 = [D['order'][x] for x in _s.get(_f, []) if D['mats'][D['order'][x]].get('side') != 'B' or D['order'][x] in _want]  # Oct 26: Bespoke side B sits next to its twin (v95_bespoke2side)
            if _lst57[:len(_want)] != _want: F.append(f"[57] {_s['name']}: coordinated mats are not first in {_f}")
# [58] Oct 25 (Tiffany 21:43; + Classic/East Meets West Tortoise Oct 26 9:24am, v94_bambirdtortoise.py): Bam Bird tile sets use the uniform faces|backs split photo (config/fym-bambird-splits-oct25.json)
for _k in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-bambird-splits-oct25.json')))['splits']:
    if _k in D['tiles'] and not str(D['tiles'][_k].get('full', '')).startswith('t92/'): F.append(f"[58] Bam Bird tile {_k} is not using its split photo")
# [59] Oct 26 (Tiffany 8:24am): Start with tiles has no default colour chip; every set shows A-Z
if "S.tcol=tileOrder()[0]" in UI: F.append("[59] tile door pre-selects a colour chip (should open on all sets A-Z, nothing selected)")
# [61] Oct 26 (Tiffany 8:25am): 'Photo coming soon' tile sets sort to the bottom of every tile list
if "sort((a,b)=>a[0].name.localeCompare(b[0].name))" in UI or not (".sort((a,b)=>!!T[a[0].tile].soon-!!T[b[0].tile].soon).map(" in UI or ".sort((a,b)=>!!T[a[0].tile].soon-!!T[b[0].tile].soon||(BPA(a[0].maker)?0:1)-(BPA(b[0].maker)?0:1))" in UI):
    F.append("[61] 'Photo coming soon' tile sets are not sorted to the bottom of the tile lists")
# [64] Oct 26 (Tiffany 8:43am): Charleston Mahjong Club tile sets use the approved faces | angled-backs photo (config/fym-cmc-splits-oct26.json)
for _k in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-cmc-splits-oct26.json')))['splits']:
    if _k in D['tiles'] and not str(D['tiles'][_k].get('full', '')).startswith('t94/cmc-'): F.append(f"[64] CMC tile {_k} is not using its approved photo")
# [63] Oct 26 (Tiffany 8:48am): every Yellow Mountain Imports tile set uses its faces|backs split photo (config/fym-ymi-splits-oct26.json)
for _k, _v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-ymi-splits-oct26.json')))['splits'].items():
    if _k in D['tiles'] and D['tiles'][_k].get('full') != 't94/' + os.path.basename(_v['img']): F.append(f"[63] YMI tile {_v['name']} is not using its faces|backs split photo")
for _k in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-ymi-splits-oct26.json'))).get('soon', []):
    if _k in D['tiles'] and not D['tiles'][_k].get('soon'): F.append(f"[63] YMI tile {D['tiles'][_k]['n']} should be Photo coming soon (Ivory sets, Tiffany 8:56am)")
# [65] Oct 26 (Tiffany 8:50am): no visible Bespoke tile photo on a black/dark background (config/fym-bespoke-tiles-oct26.json)
_vt65 = {s['tile'] for s in D['sets'] if VIS_SET(s)} if 'VIS_SET' in globals() else {s['tile'] for s in D['sets'] if not s.get('hid')}
for _k in sorted(_vt65):
    if 'bespokemahjong' not in _k: continue
    _fp = os.path.join(B, str(D['tiles'].get(_k, {}).get('full', '')))
    try:
        _a = np.asarray(Image.open(_fp).convert('L'), dtype=float)
        _bd = np.concatenate([_a[:6].ravel(), _a[-6:].ravel(), _a[:, :6].ravel(), _a[:, -6:].ravel()]).mean()
        if _bd < 60: F.append(f"[65] Bespoke tile {D['tiles'][_k].get('n')} photo has a dark background (border {_bd:.0f})")
    except Exception as _e: F.append(f"[65] Bespoke tile {_k} photo not readable: {_e}")
# [66] Oct 26 (Tiffany 9:03-9:05am): PLM + My Fair Mahjong tile photos fill the match-card circle (no white background
# showing): outer ring of the centred square crop of t.full has <3% pure-white pixels (config/fym-tilezoom-oct26.json)
_zc = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-tilezoom-oct26.json')))['tiles']
_zk = set(_zc) | {s['tile'] for s in D['sets'] if vis(s) and s['tile'].startswith(('peacelovemahjong.com/', 'myfairmahjong.com/'))}
for _k in sorted(_zk):
    _t = T.get(_k)
    if not _t or _t.get('soon') or not _t.get('full'): continue
    try:
        _im = Image.open(os.path.join(B, _t['full'])).convert('RGB'); _s = min(_im.size); _x = (_im.width - _s) // 2; _y = (_im.height - _s) // 2
        _a = np.asarray(_im.crop((_x, _y, _x + _s, _y + _s)).resize((200, 200))).astype(int)
        _yy, _xx = np.mgrid[:200, :200]; _r = np.hypot(_xx - 99.5, _yy - 99.5); _w = (_a.min(2) > 248)[(_r < 100) & (_r > 80)].mean()
        if _w >= .03: F.append(f"[66] {_t.get('n')}: tile photo doesn't fill the match-card circle ({_w:.0%} white at the edge)")
    except Exception as _e: F.append(f"[66] {_k}: could not check ({_e})")
# [68] Oct 26 (QA): zoom snaps to 1 so drag-swipe never dies after zoom in/out (builder/fym_fix_oct25/v94_zoomsnap.py)
if "if(Math.abs(ns-1)<0.02)ns=1;" not in UI: F.append("[68] zoom does not snap back to 1 (drag-swipe can stay dead after zooming in and out)")
# [69] Oct 26 (Tiffany 10:25am): 'Add racks' right under the chosen mat + tapping the chosen mat = Add racks; no rack named
# just "Mahjong Rack & Pusher Set"/"Racks" (builder/fym_fix_oct25/v95_addracks.py)
if 'class="go pkgo" data-mock=' not in UI or 'v95: tap the chosen mat' not in UI: F.append("[69] no 'Add racks' button / tap-to-continue under the chosen mat")
for _k69, _r69 in D['racks'].items():
    if not _r69.get('hid') and _r69.get('n', '').strip() in ('Racks', 'Mahjong Rack & Pusher Set', 'Rack & Pusher Set'): F.append(f"[69] rack with no real name: {_k69}")
# [71] Oct 26 (Tiffany 10:48am): match-card title stays within the mat/button column (builder/fym_fix_oct25/v95_titlewidth.py)
if "TW=Math.min(W-120-2*SW,W*.74)" not in UI: F.append("[71] match-card title can run wider than the mat column (long set names overhang)")
# [70] Oct 26 (Tiffany 10:46am): no visible rack's card photo is portrait (racks standing up mock up tiny on the match
# card); content box (alpha / non-white) h/w must be < 1.3. Let's Mahj On Luxe Pink is a 3D standing shot, allowed.
try:
    import io as _io70, numpy as _np70
    from PIL import Image as _Im70
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fym_rack_images import shown as _shown70
    _ok70 = {'www.letsmahj-on.com/luxe-acrylic-scalloped-mahjong-rack-pink'}
    for _k, _n, _t, _h, _b in _shown70(B):
        if _t != 'sm' or not _b or _k in _ok70: continue
        _a = _np70.asarray(_Im70.open(_io70.BytesIO(_b)).convert('RGBA')).astype(int)
        _m = _a[..., 3] > 40 if _a[..., 3].min() < 250 else _a[..., :3].min(2) < 235
        _ys, _xs = _np70.where(_m)
        if len(_xs) and (_ys.max() - _ys.min() + 1) >= 1.3 * (_xs.max() - _xs.min() + 1): F.append(f"[70] rack photo is portrait (racks standing up): {_n}")
except Exception as _e: F.append(f"[70] portrait rack check did not run: {_e}")
# [72] Oct 26 card sweep (docs/FYM-CARD-SWEEP-oct26.md): title contrast >= 3.5:1 on cream, subtitle fits the mat column (no '…'),
# Photo coming soon text fits the circle, rack label never the generic 'Racks', long mat names have a display name
for _need, _msg in ((("/*v100 title*/" if "/*v100 title*/" in UI else "/* v95 contrast */" if "/*v98 assigned title colour*/" not in UI else "/*v98 assigned title colour*/"), "title colour is not darkened for contrast"), ("/* v95 subtitle fits the mat column */", "subtitle can overrun the mat / be cut with '…'"),
                    ("/* v95 fit circle */", "Photo coming soon text can be clipped by the circle"), ("/* v95 no generic Racks */", "rack label can fall back to just 'Racks'")):
    if _need not in UI: F.append("[72] " + _msg)
for _k, _v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-mat-display-names-oct26.json')))['dn'].items():
    if _k in D['mats'] and D['mats'][_k].get('dn') != _v: F.append(f"[72] mat {_k} is missing its short display name")
for _k, _m in D['mats'].items():
    if not _m.get('hid') and (_m['n'].endswith(' P') or _m['n'].endswith(' LT')): F.append(f"[72] mat name looks cut short: {_m['n']}")
# [73] Oct 26 (card sweep): racks whose photo was a stack drew TINY on cards -> one real rack each (config/fym-rack-size-oct26.json,
# builder/fym_fix_oct25/v95_racksize.py); 'hide' entries stay hidden
_c73 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-rack-size-oct26.json')))
for _k in _c73['racks']:
    if _k in json.load(open(REPO + 'config/fym-rack-split-oct26.json'))['replace'] and str(D['racks'].get(_k, {}).get('im', '')).startswith('rk98'): continue  # v98 single-rack photo (gate [92])
    if _k in D['racks'] and not D['racks'][_k].get('hid') and 's95' not in str(D['racks'][_k].get('im', '')): F.append(f"[73] {D['racks'][_k]['n']}: still shows its stacked-racks photo (draws tiny on cards)")
for _k in _c73.get('hide', {}):
    if _k in D['racks'] and not D['racks'][_k].get('hid'): F.append(f"[73] {D['racks'][_k]['n']}: should be hidden (no usable single-rack photo)")
_v96pq79 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-rack-clean-oct26.json')))['pq']
# [79] Oct 26 (Tiffany 11:35 + 11:39; QA v95): single-rack recuts show (Iridescent Opal = one rack, no white box) and the
# by-eye photo-quality scores are applied (config/fym-rack-recut-oct26.json, config/fym-rack-pq-oct26.json, v95_rackphotos.py)
_c79 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-rack-recut-oct26.json')))['racks']
_q79 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-rack-pq-oct26.json')))['racks']
for _k in _c79:
    if _k in json.load(open(REPO + 'config/fym-rack-split-oct26.json'))['replace'] and str(D['racks'].get(_k, {}).get('im', '')).startswith('rk98'): continue  # v98 newer single-rack photo (gate [92])
    if str(D['racks'].get(_k, {}).get('im', '')).startswith('rk99'): continue  # v99 single horizontal re-cut (gate [97])
    if _k in D['racks'] and not D['racks'][_k].get('hid') and not str(D['racks'][_k].get('im', '')).endswith('q95'): F.append(f"[79] {D['racks'][_k]['n']}: still shows its old rack photo (recut not applied)")
for _k, _v in _q79.items():
    if _k in _v96pq79 and '/*v96 poor photo never leads*/' in open(os.path.join(B, 'index.html')).read(): continue  # v96 re-scored (config/fym-rack-clean-oct26.json, gate [81])
    if _k in D['racks'] and D['racks'][_k].get('pq') != _v['pq']: F.append(f"[79] {D['racks'][_k]['n']}: photo score {D['racks'][_k].get('pq')} != by-eye {_v['pq']}")
# [67] Oct 26 (Tiffany 9:23/9:24am): Mahjong Studios + Splash of Color pulled from FYM; only Splash mats on her own matches stay
_k67 = {x[0] for s_ in D['sets'] for x in s_.get('m', [])}
for s_ in D['sets']:
    if s_.get('maker') in ('Mahjong Studios', 'Splash of Color') and not s_.get('hid'): F.append(f"[67] {s_['maker']} set visible: {s_['name']}")
for k_, m_ in D['mats'].items():
    if m_.get('bn') in ('Mahjong Studios', 'Splash of Color') and not m_.get('hid') and k_ not in _k67: F.append(f"[67] {m_['bn']} mat visible (not one of her matches): {m_['n']}")
for k_, r_ in D['racks'].items():
    if r_.get('bn') in ('Mahjong Studios', 'Splash of Color') and not r_.get('hid'): F.append(f"[67] {r_['bn']} rack visible: {r_['n']}")
_ms_pulled = all(s_.get('hid') for s_ in D['sets'] if s_.get('maker') == 'Mahjong Studios')
# [62] Oct 26 (Tiffany 8:48am, replaces 8:42): Mahjong Studios tile photos follow config/fym-mstudios-oct26.json
# (keep / white_bg / pile_photo / soon / hide; builder/fym_fix_oct25/v94_mstudios.py); brands whose sets are all
# 'Photo coming soon' sort last in Shop by brand
_c62 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-mstudios-oct26.json')))['sets']
_s62 = {s['tile']: s for s in D['sets']}
for _k, _v in _c62.items():
    _t = D['tiles'].get(_k); _do = _v['do']
    if _ms_pulled: break
    if not _t: F.append(f"[62] Mahjong Studios tile missing from the build: {_k}"); continue
    if _do in ('keep', 'white_bg', 'pile_photo') and _t.get('soon'): F.append(f"[62] {_t['n']}: shows Photo coming soon, decided '{_do}'")
    if _do in ('white_bg', 'pile_photo') and _t.get('full') != 't94/ms-' + os.path.basename(_v['img']): F.append(f"[62] {_t['n']}: not using its {_do} photo")
    if _do == 'soon' and not _t.get('soon'): F.append(f"[62] {_t['n']}: should be Photo coming soon")
    if _do == 'hide' and _k in _s62 and not _s62[_k].get('hid'): F.append(f"[62] {_t['n']}: should be hidden")
    if _do != 'hide' and _k in _s62 and _s62[_k].get('hid') and _do != 'soon': F.append(f"[62] {_t['n']}: hidden but decided '{_do}'")
if "so[s.maker]=(so[s.maker]??true)&&!!t.soon" not in UI: F.append("[62] Shop by brand does not sort all-'Photo coming soon' brands last")
# [60] Oct 26 (Tiffany 8:29am): among equally matching racks the best-photographed one leads (config/rack-photo-quality.json,
# builder/fym_fix_oct26/v94_rackquality.py). Default suggestions (picks off, every album pairing) and the white/clear/wood chips:
# the first non-pick rack has photo score >= 4 whenever a 4+ rack is in the same colour band. Every visible rack has a score.
_r60 = subprocess.run(['node', os.path.join(REPO, 'builder', 'fym_rackquality_check.js'), B], capture_output=True, text=True, timeout=600)
try:
    _j60 = json.loads(_r60.stdout)
    for _m in _j60['fails'][:6]: F.append('[60] ' + _m)
    if _j60['nfail'] > 6: F.append(f"[60] ... {_j60['nfail'] - 6} more rack photo-order problems")
except Exception as _e: F.append(f"[60] rack photo-quality check did not run: {_e} {_r60.stderr[:200]}")
# [46] Oct 25 (Tiffany 16:37): Mood board rack labels sit BELOW the racks (whole rack visible)
if 'racks(rx,ry,rw,rh,{fs:STORY?23:19,maxRow:rh,rows:true,back:true,below:true})' not in UI and 'racks(rx,top+110,rw,bot-top-110,{fs:STORY?23:19,rows:true,back:true,below:true,eq:true' not in UI:  # v98 equal-length block keeps below:true
    F.append("[46] Mood board (tri view) rack labels are not below the racks (below:true)")

# [74] Oct 26 (Tiffany 11:16am, builder/fym_fix_oct25/v96_amazon_holiday.py): partner brands keep preferential order over ShopMy
# Amazon mats. On every visible Holiday tile set (BACKG Holiday), the first 6 non-pick mats of the colour ranking (s.cr) hold no
# Amazon mat while a partner holiday mat matches (sits in that set's top 30). Amazon mats carry a go.shopmy.us link, no code claim.
try:
    _bg74 = re.search(r'BACKG=(\{.*?\});', UI) or re.search(r'BACKG=(\{.*?\});', open(os.path.join(B, 'index.html')).read())
    _hol74 = set(json.loads(_bg74.group(1)).get('Holiday', [])) if _bg74 else set()
    _O74 = D['order']
    for _s in D['sets']:
        if _s.get('hid') or _s['name'] not in _hol74 or 'cr' not in _s: continue
        _pk = {e[0] if isinstance(e, list) else e for e in (_s.get('m') or [])}
        _cr = [_O74[j] for j in _s['cr'] if not D['mats'][_O74[j]].get('hid')]
        if not any(D['mats'][k].get('pa') and D['mats'][k].get('hol') for k in _cr[:30]): continue
        _top = [k for k in _cr if k not in _pk][:6]
        _am = [D['mats'][k]['n'] for k in _top if D['mats'][k].get('b') == 'Amazon']
        if _am: F.append(f"[74] {_s['name']}: Amazon mat in the first 6 non-pick places ahead of partner holiday mats: {', '.join(_am)}")
    for _k, _m in D['mats'].items():
        if _m.get('b') == 'Amazon' and _m.get('add') == 'oct26-amazon' and not _m.get('hid'):
            if not str(_m.get('u', '')).startswith('https://go.shopmy.us/') or _m.get('dc') or _m.get('pa'): F.append(f"[74] Amazon mat {_m['n']}: needs her go.shopmy.us link and no code claim")
except Exception as _e: F.append(f"[74] Amazon partner-order check did not run: {_e}")

# [75] Oct 26 (Tiffany 11:35): racks follow the TILE brand first, then the mat brand (Mahj Mood 90s + Anders Ruff mat led with
# Anders Ruff clear racks). builder/fym_fix_oct25/v95_rackbrand.py
_h75 = open(os.path.join(B, 'index.html')).read()
if '/*v95 tile brand first*/' not in _h75 or 'ownW(b)-ownW(a)' not in _h75 or "ownW(r)===2?5:2" not in _h75:
    F.append("[75] rack order does not put the TILE brand's racks ahead of the mat brand's (run v95_rackbrand.py)")

# [77] Oct 26 QA v95: Close up card draws 'Photo coming soon' sets in a band that fits (no text cut off, no TILES pill over the
# name); card pills shrink then wrap long names before '…'; Mood board TILES label wraps (r*1.5). Etsy mats the spec hides
# (e.g. Savannah Soiree, corner close-up) stay hidden. builder/fym_fix_oct25/v95_qafix.py + config/fym-etsy-shopmy-oct26.json
_h77 = open(os.path.join(B, 'index.html')).read()
for _need, _msg in (("/*v95 soon band*/soonBand(x,top,w,hT)", "Close up card crops 'Photo coming soon' into the tiles band"),
                    ("/*v95 pill fit*/", "card pills cut long names with '…' instead of shrinking/wrapping"),
                    ("'TILES',s.name,{up:true,right:true,maxW:r*1.5", "Mood board TILES label runs across the mat")):
    if _need not in _h77: F.append("[77] " + _msg + " (run v95_qafix.py)")
try:
    for _x in json.load(open(os.path.join(REPO, 'config/fym-etsy-shopmy-oct26.json')))['mats']:
        if _x.get('hid') and _x['key'] in D['mats'] and not D['mats'][_x['key']].get('hid'): F.append(f"[77] Etsy mat {_x['name']} should be hidden ({_x.get('reason','')[:60]})")
except Exception as _e: F.append(f"[77] Etsy hidden check did not run: {_e}")

# [76] Oct 26 (Tiffany 11:37: "The back color is a dominant color"): mat ranking weighs the tile BACK (re-measured from the current
# photo), partner-first tie-break, motif hint. Every visible non-holiday faces|backs split set carries bsw (v95_matrank.py ran), and
# Aloha (YMI, white backs with yellow plumeria) has a yellow mat in its first 5 colour-ranked mats. builder/fym_fix_oct25/v95_matrank.py
try:
    import re as _re76
    _hg = _re76.search(r'BACKG=(\{.*?\});', open(os.path.join(B, 'index.html')).read())
    _hol76 = set(json.loads(_hg.group(1)).get('Holiday', [])) if _hg else set()
    _miss = [s['name'] for s in D['sets'] if not s.get('hid') and s['name'] not in _hol76 and (D['tiles'].get(s['tile']) or {}).get('split') and not (D['tiles'].get(s['tile']) or {}).get('soon') and not s.get('bsw')]
    if _miss: F.append(f"[76] {len(_miss)} split tile sets ranked without their back colour (run v95_matrank.py): {', '.join(_miss[:6])}")
    _C76 = json.load(open(os.path.join(REPO, 'config/fym-colour-oct25.json')))['mats']
    def _yel(m):
        from skimage.color import rgb2lab as _r2l
        import numpy as _np
        for hx, w in (_C76.get(m) or {}).get('sw', []):
            L = _r2l(_np.array([[[int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]]]))[0, 0]
            if w >= .12 and L[2] >= 30 and L[0] >= 60 and abs(L[1]) < 25: return True
        return False
    for s in D['sets']:
        if s['slug'] == 'yellow-mountain-imports-aloha' and not s.get('hid') and not s['m']:
            top = [D['order'][j] for j in s.get('cr', [])]; top = [m for m in top if m in D['mats'] and not D['mats'][m].get('hid') and not D['mats'][m].get('rt')][:5]
            if not any(_yel(m) for m in top): F.append("[76] Aloha's first 5 mats have no yellow (its yellow plumeria backs are not weighed): " + ', '.join(D['mats'][m]['n'] for m in top))
except Exception as _e: F.append(f"[76] back-colour ranking check did not run: {_e}")

# [78] Oct 26 (Tiffany 11:41am): Bespoke double-sided mats are listed twice, one entry per side, ONE photo each
# (config/fym-bespoke-2side-oct26.json, builder/fym_fix_oct25/v95_bespoke2side.py). Side B = '<A key>#side-b', same shop link,
# visible whenever side A is, ranked right after side A wherever side A is ranked.
try:
    _S78 = json.load(open(REPO + 'config/fym-bespoke-2side-oct26.json'))['mats']
    _ix78 = {m: j for j, m in enumerate(D['order'])}
    for _ka, _x in _S78.items():
        _A, _B = D['mats'].get(_ka), D['mats'].get(_ka + '#side-b')
        if not _A: continue
        if not _B: F.append(f"[78] {_x['nameA']}: side B entry missing"); continue
        if not _A.get('f') or not _B.get('f') or _A['f'] == _B['f']: F.append(f"[78] {_x['nameA']}: each side needs its own single photo")
        if '(Side A:' not in _A['n'] or '(Side B:' not in _B['n']: F.append(f"[78] {_x['nameA']}: names must say Side A / Side B")
        if bool(_A.get('hid')) != bool(_B.get('hid')): F.append(f"[78] {_x['nameA']}: side B visibility differs from side A")
        if _B.get('u') != _A.get('u') or _B.get('dc') != _A.get('dc'): F.append(f"[78] {_x['nameA']}: side B shop link/code differs from side A")
        if bool(_B.get('hol')) != bool(_x['holB']): F.append(f"[78] {_x['nameA']}: side B holiday flag wrong")
        _ja, _jb = _ix78[_ka], _ix78[_ka + '#side-b']
        for _s in D['sets']:
            _r = _s.get('rank') or []
            if _ja in _r and (_jb not in _r or _r.index(_jb) != _r.index(_ja) + 1): F.append(f"[78] {_x['nameA']}: side B not right after side A in {_s['name']}"); break
except Exception as _e: F.append(f"[78] double-sided check did not run: {_e}")

# [80] Oct 26: every visible mat photo m/<n> must sit in a packed chunk the page loads (chunk n//12 listed in MCB and present
# in <n//12>.webp header). v95_etsy wrote 21 mats into chunk 180 only, so m/2172-2180 fell back to 150px thumbs on cards.
try:
    _h80 = open(os.path.join(B, 'index.html')).read()
    _mcb80 = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', _h80)
    if _mcb80:
        _set80 = {int(v) for v in _mcb80.group(1).split(',')}; _hdr80 = {}
        for _k, _m in D['mats'].items():
            _f = str(_m.get('f', ''))
            _mm = re.match(r'm/(\d+)\.', _f)
            if _m.get('hid') or not _mm: continue
            _c = int(_mm.group(1)) // 12
            if _c not in _set80: continue
            if _c not in _hdr80:
                try:
                    _raw = open(os.path.join(B, 'mc', f'{_c}.webp'), 'rb').read(); _n = struct.unpack('<I', _raw[-4:])[0]
                    _hdr80[_c] = json.loads(_raw[-4 - _n:-4])
                except Exception: _hdr80[_c] = None
            if _hdr80[_c] is not None and _f not in _hdr80[_c]: F.append(f"[80] {_m.get('n')}: {_f} is not inside packed chunk mc/{_c}.webp (card shows a thumbnail)")
except Exception as _e: F.append(f"[80] chunk check did not run: {_e}")

# [81] Oct 26 (QA v95 item 2c, builder/fym_fix_oct25/v96_rackclean.py): a poorly photographed rack (pq<=2) never leads a rack
# list (top 3) unless it is her pick or the TILE brand's own rack; mat-brand lift needs pq>=3; the clean cutouts are in; Bird &
# Bamboo "Clear" (= Clear Wood Stain) is a wood rack, not clear.
try:
    _h81 = open(os.path.join(B, 'index.html')).read(); _v81 = re.search(r'Version (\d+)', _h81)
    if _v81 and int(_v81.group(1)) < 96 and '/*v96 poor photo never leads*/' not in _h81: raise StopIteration  # rule starts with v96
    _c81 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-rack-clean-oct26.json')))
    if '/*v96 poor photo never leads*/' not in _h81 or "(ownW(r)===2||(R[r].pq||3)>=3)" not in _h81: F.append("[81] rack ranking: poor-photo / mat-brand-lift rule missing (run v96_rackclean.py)")
    for _k in _c81['recut']:
        if _k in D['racks'] and not D['racks'][_k].get('hid') and not str(D['racks'][_k].get('im', '')).endswith('c96') and not str(D['racks'][_k].get('im', '')).startswith('rk98'): F.append(f"[81] {D['racks'][_k]['n']}: still shows its boxed/scene photo")
    for _k, _v in _c81['pq'].items():
        if _k in D['racks'] and D['racks'][_k].get('pq') != _v: F.append(f"[81] {D['racks'][_k]['n']}: photo score {D['racks'][_k].get('pq')} != {_v}")
    if 'bb:Clear' in D['racks'] and 'clear' in (D['racks']['bb:Clear'].get('rf') or []): F.append("[81] Bird & Bamboo Clear Wood Stain is tagged clear")
except StopIteration: pass
except Exception as _e: F.append(f"[81] check did not run: {_e}")

# ---- v97 (Version 1.1) checks, Oct 26 evening (docs/MATCH-INBOX.md) ----
W97 = []   # warnings printed at the end (do not fail the gate)
_v97 = re.search(r'Version (\d+)', h); _pre97 = '/*v97 accent-blind search*/' not in UI and _v97 is not None and int(_v97.group(1)) < 97
# [82] Oct 26 5:37pm (Tiffany testing): a searched mat stuck to the front of EVERY later deck (S.mfront never cleared).
# resetFrom(1) is RUN in node on a stub S: mfront/mfset must come back null; tReset clears it; matDeck fronts it only for the set
# it was searched on (S.mfset===S.set); the search sets S.mfset. builder/fym_fix_oct25/v97_ui.py
if not _pre97:
    try:
        _rf = re.search(r'function resetFrom\(level\)\{.*?S\.made=false;\}', UI, re.S).group(0)
        _js82 = _rf + ";const S={mfront:'x',mfset:3,seen:{a:1},f:{m:{},r:{}}};resetFrom(1);console.log(JSON.stringify([S.mfront,S.mfset]));"
        _o82 = subprocess.run(['node', '-e', _js82], capture_output=True, text=True, timeout=60)
        if _o82.stdout.strip() != '[null,null]': F.append(f"[82] resetFrom(1) leaves the searched mat in front (S.mfront/mfset = {_o82.stdout.strip() or _o82.stderr[:120]})")
        if 'const tReset=()=>{S.mfront=null;S.mfset=null;' not in UI: F.append("[82] tReset (mat door / start over) does not clear the searched mat")
        if 'S.mfront&&S.mfset===S.set&&M[S.mfront]' not in UI: F.append("[82] matDeck fronts a searched mat on every set (no S.mfset===S.set guard)")
        if 'S.mfront=id;S.mfset=S.set;' not in UI: F.append("[82] mat search does not remember which set it was searched on")
    except Exception as _e: F.append(f"[82] sticky-search check did not run: {_e}")
# [83] Oct 26 5:53pm: "soiree" found nothing, "soir" found SOIRÉE. Every search box folds accents on BOTH sides (NRM); every
# visible mat / tile set / rack name with an accent is found by its accent-free spelling (run in node with the page's own NRM).
if not _pre97:
    try:
        import unicodedata as _ud
        _nrm = re.search(r"const NRM=(x=>.*?\.toLowerCase\(\));", UI).group(1)
        if UI.count('const v=NRM(e.target.value.trim()),') < 4: F.append("[83] a search box still compares the typed text without folding accents")
        for _need in ("const s=NRM(M[id].n+' '+(M[id].bn||''));", "const h=NRM(s.name+' '+s.maker);", "const s=NRM(R[id].n+' '+(R[id].bn||''));"):
            if _need not in UI: F.append(f"[83] search haystack not accent-folded: {_need[:40]}")
        _fold = lambda x: ''.join(c for c in _ud.normalize('NFD', x) if not _ud.combining(c)).lower()
        _cases = []
        for _o in list(M.values()) + list(D['racks'].values()):
            if _o.get('hid'): continue
            _txt = _o['n'] + ' ' + (_o.get('bn') or '')
            if _fold(_txt) != _txt.lower(): _cases.append([_txt, _fold(_o['n'])])
        for _s in D['sets']:
            if vis(_s) and _fold(_s['name'] + ' ' + _s['maker']) != (_s['name'] + ' ' + _s['maker']).lower(): _cases.append([_s['name'] + ' ' + _s['maker'], _fold(_s['name'])])
        _js83 = f"const NRM={_nrm};const C={json.dumps(_cases, ensure_ascii=False)};const bad=C.filter(([h,q])=>!q.split(/\\s+/).filter(Boolean).every(t=>NRM(h).includes(NRM(t))));console.log(JSON.stringify(bad.map(x=>x[0])));"
        _o83 = subprocess.run(['node', '-e', _js83], capture_output=True, text=True, timeout=60)
        _bad83 = json.loads(_o83.stdout or 'null')
        if _bad83 is None: F.append(f"[83] accent search check did not run: {_o83.stderr[:150]}")
        elif _bad83: F.append(f"[83] {len(_bad83)} accented names not found by their accent-free spelling: " + '; '.join(_bad83[:6]))
        elif not _cases: F.append("[83] no accented product names found to test (check the parser)")
    except Exception as _e: F.append(f"[83] accent search check did not run: {_e}")
# [84] Oct 26: mat door parity: 'Add racks ›' right under the chosen suitor tile set + tapping the chosen tile set = Add racks
if not _pre97:
    if 'class="go pkgo" data-tadd="${pk.i}">Add racks ›</button>' not in UI: F.append("[84] mat door: no 'Add racks' button under the chosen tile set")
    if '/*v97 tap chosen tiles = Add racks*/' not in UI: F.append("[84] mat door: tapping the chosen tile set does not go to racks")
# [85] Oct 26 5:45pm: 5 My Fair Mahjong sets stayed hidden by the no_tiles flag of their OLD photo after the Oct 21 audit gave them a
# good photo. A set whose photo upgrade is ok/upgrade may not stay hidden behind a no_tiles flag, unless the flag note records a
# keep-hidden decision (e.g. OMM Debutantes = travel sets). Jubilee Midnight Blue is in (v97_mfm.py).
try:
    _U85 = json.load(open(REPO + 'builder/fym_flags/tile_photo_upgrades.json'))['sets']
    _S85 = {s_['slug']: s_ for s_ in D['sets']}
    for _sl, _u in _U85.items():
        _s = _S85.get(_sl); _fl = tflags.get(_sl) or {}
        if _s and _s.get('hid') and _u.get('status') in ('ok', 'upgrade') and _fl.get('flag') == 'no_tiles' and not re.search(r'(?i)stay hidden|stays hidden|keep hidden', _fl.get('note', '')):
            F.append(f"[85] {_s['name']} ({_s['maker']}): hidden by a stale no_tiles flag although its photo upgrade is '{_u['status']}'")
    if _pre97: raise StopIteration
    _mb = _S85.get('my-fair-mahjong-the-jubilee-series-midnight-blue')
    if not _mb or not vis(_mb): F.append("[85] My Fair Mahjong The Jubilee Series (Midnight Blue) missing or hidden")
    elif _mb['m']: F.append("[85] Jubilee Midnight Blue carries a Tiffany's-match list (catalog set: m must be [] until her album / swipe book)")
except StopIteration: pass
except Exception as _e: F.append(f"[85] stale tile flag check did not run: {_e}")
# [86] Oct 26 5:40pm: Peace Love Mahjong match-card band framing (config/fym-plm-band-oct26.json): Desert Dreams showed blanks
try:
    for _k, _bf in json.load(open(REPO + 'config/fym-plm-band-oct26.json'))['tiles'].items():
        if _pre97: break
        if T.get(_k, {}).get('bf') != _bf: F.append(f"[86] {T.get(_k, {}).get('n', _k)}: band anchor {T.get(_k, {}).get('bf')} != {_bf}")
except Exception as _e: F.append(f"[86] PLM band check did not run: {_e}")
# [87] Oct 26 5:40pm: My Fair Mahjong Natural Wood rack featured (good single-rack photo, ft lift when it fits the mat colour) and no
# visible rack links the old 404 MFM wooden-painted-mahjong-racks product
try:
    _NW = D['racks'].get('myfairmahjong.com/wooden-racks?v=53371892990263')
    if not _pre97:
        if not _NW or _NW.get('hid') or not _NW.get('ft') or (_NW.get('pq') or 0) < 4: F.append("[87] MFM Natural Wood rack is not featured (visible, ft, photo score >= 4)")
        if '/*v97 featured wood*/' not in UI: F.append("[87] rack pool has no featured-rack lift")
    for _k, _r in D['racks'].items():
        if not _r.get('hid') and any('wooden-painted-mahjong-racks' in str(_r.get(x, '')) for x in ('u', 'u0')): F.append(f"[87] {_r['n']} links the old 404 MFM wood rack product")
except Exception as _e: F.append(f"[87] wood rack check did not run: {_e}")
# [88] Oct 26 5:50pm: Peace Love Mahjong painted racks re-cut whole from the brand's group photo (no chopped crops)
if not _pre97:
    for _c in ['Chartreuse', 'Dark Green', 'Aqua', 'French Blue', 'Navy', 'Purple', 'Pink', 'Light Pink', 'Lilac', 'Red', 'Cobalt']:
        _r = D['racks'].get('plm:' + _c)
        if _r and not _r.get('hid') and not str(_r.get('im', '')).startswith('rk97plm') and not ('plm:' + _c in json.load(open(REPO + 'config/fym-rack-split-oct26.json'))['locked'] and str(_r.get('im', '')).startswith('rk98')): F.append(f"[88] Peace Love Mahjong {_c}: still the chopped rack photo")  # v98: approved whole-rack photos restored (gate [94])
# [89] Oct 26 5:49pm: mat photos fill the frame (white bands on the card + swipe). FAIL: a visible mat photo with a flat white margin
# >= 6% on any side (trim it: config/fym-mat-white-oct26.json + v97_matwhite.py). WARN: angled shots whose corners are white
# (need a perspective flatten like Amahj Blue, Citron + Lilac).
if not _pre97:
    try:
        _imgs89 = {}
        for _fn in os.listdir(os.path.join(B, 'mc')):
            if _fn.endswith('.webp'):
                _raw = open(os.path.join(B, 'mc', _fn), 'rb').read(); _n = struct.unpack('<I', _raw[-4:])[0]
                for _f, (_a, _l) in json.loads(_raw[-4 - _n:-4]).items(): _imgs89[_f] = (_raw, _a, _l)
        _flat89, _ang89 = [], []
        _FL89 = json.load(open(REPO + 'config/fym-mat-flat-oct26.json'))  # v98: flattened angled shots stay fixed; flat-by-design shots skipped
        _on89 = any(_m.get('w98') for _m in M.values())  # the flattening is post-launch WIP: checked only in builds that applied it
        for _k, _fo in (_FL89['mats'].items() if _on89 else []):
            if _k in M and not M[_k].get('hid') and M[_k].get('w98') != _fo['action']: F.append(f"[89] {_fo['brand']} | {_fo['name']}: v98 photo fix ({_fo['action']}) not applied")
        import io as _io89
        for _k, _m in M.items():
            if _m.get('hid') or _m.get('f') not in _imgs89: continue
            _raw, _a, _l = _imgs89[_m['f']]
            _im = Image.open(_io89.BytesIO(_raw[_a:_a + _l])).convert('RGB'); _ar = np.asarray(_im.resize((200, max(1, round(200 * _im.height / _im.width))))).astype(int)
            _wh = (_ar.min(2) > 235) & ((_ar.max(2) - _ar.min(2)) < 16)
            def _run(v):
                n_ = 0
                for x_ in v:
                    if x_ > .97: n_ += 1
                    else: break
                return n_
            _cw, _rw = _wh.mean(0), _wh.mean(1)
            _mg = max(_run(_cw) / _wh.shape[1], _run(_cw[::-1]) / _wh.shape[1], _run(_rw) / _wh.shape[0], _run(_rw[::-1]) / _wh.shape[0])
            if _mg >= .06: _flat89.append(f"{_m.get('bn')} | {_m['n']} ({_mg:.0%})")
            _hh, _ww = _wh.shape; _c = max(2, min(_hh, _ww) // 6)
            if np.mean([_wh[:_c, :_c].mean(), _wh[:_c, -_c:].mean(), _wh[-_c:, :_c].mean(), _wh[-_c:, -_c:].mean()]) >= .45:
                if _on89 and _k in _FL89['mats']: F.append(f"[89] {_m.get('bn')} | {_m['n']}: was flattened in v98 but shows an angled photo with white corners again")
                elif _k not in _FL89['not_angled']: _ang89.append(f"{_m.get('bn')} | {_m['n']}")
        if _flat89: F.append(f"[89] {len(_flat89)} mat photos with white bands (trim in config/fym-mat-white-oct26.json): " + '; '.join(_flat89[:8]))
        if _ang89: W97.append(f"[89] {len(_ang89)} angled mat photos with white corners (need a perspective flatten): " + '; '.join(_ang89))
    except Exception as _e: F.append(f"[89] white-band check did not run: {_e}")
# [90] Oct 26: gallery sync. Every visible FYM mat (not hidden, not a '#side-b' second listing) should have a Mat Gallery row
# (staged site/livepatch/matgallery/matgallery-v5.html rows or config/mat-gallery-extra-rows.json), matched by key, product URL or
# name + brand. WARN for now (lists them); extra rows not yet in the staged page are listed too (that page needs a rebuild + paste).
try:
    import unicodedata as _ud90
    _nz = lambda x: re.sub(r'[^a-z0-9]', '', ''.join(c for c in _ud90.normalize('NFD', str(x or '')) if not _ud90.combining(c)).lower())
    import urllib.parse as _up90
    def _nu(u):  # Oct 26 fix: a /discount/CODE?redirect=/products/x link is keyed by its redirect product (it used to collapse to the brand's discount URL and match any row of that brand)
        u = str(u or '')
        if '/discount/' in u and 'redirect=' in u:
            u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + _up90.unquote(u.split('redirect=', 1)[1].split('&')[0])
        return re.sub(r'^https?://(www\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')
    _XR = json.load(open(REPO + 'config/mat-gallery-extra-rows.json'))['rows']
    _GK = {GKEY(r[0]) for r in _G}; _GU = {_nu(r[3]) for r in _G}; _GN = {_nz(r[1]) + '|' + _nz(r[2]) for r in _G}
    _XK = {a['key'] for a in _XR}; _XU = {_nu(a.get('url') or a.get('u')) for a in _XR if a.get('url') or a.get('u')}
    _miss90, _stale90 = [], []
    for _k, _m in M.items():
        if _m.get('hid') or '#side-b' in _k: continue
        _u = {_nu(_m.get('u0')), _nu(_m.get('u')), _nu(_k)}
        _in_staged = _k in _GK or bool(_u & _GU) or (_nz(_m['n']) + '|' + _nz(_m.get('bn'))) in _GN
        if _in_staged: continue
        if _k in _XK or _u & _XU: _stale90.append(f"{_m.get('bn')} | {_m['n']}"); continue
        _miss90.append(f"{_m.get('bn')} | {_m['n']}")
    if _miss90: W97.append(f"[90] {len(_miss90)} visible FYM mats have no Mat Gallery row: " + '; '.join(_miss90))
    if _stale90: W97.append(f"[90] {len(_stale90)} visible FYM mats are in config/mat-gallery-extra-rows.json but not in the staged gallery page (rebuild + paste): " + '; '.join(_stale90))
except Exception as _e: F.append(f"[90] gallery sync check did not run: {_e}")
# ---- v98 (Version 1.2) checks, Oct 26 night (docs/MATCH-INBOX.md) ----
_pre98 = _v97 is not None and int(_v97.group(1)) < 98 and '/*v98 racks low equal*/' not in UI
if not _pre98:
    # [91] Tiffany 6:19pm: match card racks sat too high on the mat (covered the Heirloom Fire + Fortune horse) with a big gap
    # between two racks. Mood board card rack block = Main's partner-graphics layout (low, tight, equal length, off the mat's left).
    # Tiffany 7:20pm + Main 7:22pm: every rack the same length (rw = W*.40), stack photos (Bespoke) drawn big, x = max(48, mat left - 8.5% W)
    for _need91 in ("const lch=56,rw=W*.40,rx=Math.max(48,mbx.x-W*.085);/*v98 racks low equal*/", "eq:true,stk:W*.26,bottom:bot+8}", "/*v98 equal-length racks*/"):
        if _need91 not in UI: F.append(f"[91] match card rack layout missing: {_need91[:60]}")
    if "Math.max(2*r+40,n*170)" in UI: F.append("[91] old high rack block (n*170, centred on the tile circle) still in drawCard")
    # [92] Tiffany 6:04pm + Main 6:01pm: no Mahjong Register rack image shows a stack / infographic of several racks; Mahj Mood
    # White Wooden Scalloped shows the angled single rack (config/fym-rack-split-oct26.json, v98_racks.py)
    _C92 = json.load(open(REPO + 'config/fym-rack-split-oct26.json')); _hd92 = json.load(open(os.path.join(B, 'hd', 'index.json'))).get('r', {})
    for _k in _C92['hide']:
        if _k in D['racks'] and not D['racks'][_k].get('hid'): F.append(f"[92] {D['racks'][_k]['n']}: stacked-racks entry should be hidden (split into single variants)")
    for _k, _v in list(_C92['add'].items()) + list(_C92['replace'].items()):
        _r = D['racks'].get(_k)
        if not _r or _r.get('hid'): F.append(f"[92] {_v.get('n', _k)}: single-rack entry missing or hidden"); continue
        if not str(_r.get('im', '')).startswith('rk98') or not str(_hd92.get(_k, '')).startswith('file:r98/') or not os.path.exists(os.path.join(B, _hd92.get(_k, 'x')[5:])): F.append(f"[92] {_r['n']}: does not show its v98 single-rack photo")
        if bool(_r.get('c')) != bool(_v['c']): F.append(f"[92] {_r['n']}: cutout flag c should be {_v['c']}")
    for _k in _C92.get('mrc_single', []):  # Tiffany 7:45pm: Mahjong Row & Co. racks regressed to 4-rack stacks
        _r = D['racks'].get(_k)
        if _r and not _r.get('hid') and (not str(_r.get('im', '')).startswith('rk98') or not _r['n'].startswith('Mahjong Row & Co. ')): F.append(f"[92] Mahjong Row & Co. rack {_r['n']}: not its single-rack photo / clean name")
    for _k, _r in D['racks'].items():
        if _r.get('bn', '').startswith('Mahjong Row') and not _r.get('hid') and _k not in _C92.get('mrc_single', []): F.append(f"[92] Mahjong Row & Co. rack {_r['n']}: new entry without a checked single-rack photo")
    for _k, _r in D['racks'].items():
        if _r.get('bn') == 'Mahjong Register' and not _r.get('hid') and not str(_r.get('im', '')).startswith('rk98') and _k not in _C92['single_ok']:
            F.append(f"[92] Mahjong Register rack {_r['n']}: photo not checked as ONE rack (add a single-rack cut or list it in single_ok after looking)")
    # [93] Main 5:40pm + v97 QA: OG Desert Dreams 'Up close' tile strip (set fp/fz) must sit on the jokers + flowers rows, not the
    # winds + BLANK row (config/fym-plm-band-oct26.json 'strip', v98_plmstrip.py)
    for _n, (_fx, _fy, _fz) in json.load(open(REPO + 'config/fym-plm-band-oct26.json'))['strip'].items():
        _s93 = [s_ for s_ in D['sets'] if s_['name'] == _n]
        if not _s93: F.append(f"[93] set {_n} missing"); continue
        if _s93[0].get('fp') != [_fx, _fy] or _s93[0].get('fz') != _fz: F.append(f"[93] {_n}: Up close tile strip framing {_s93[0].get('fp')}/{_s93[0].get('fz')} != {[_fx, _fy]}/{_fz} (shows blank tiles)")
        # the 16:7 strip window must stay below the blank row (ends at y ~.68 in the brand photo)
        if _fy - (7 / 16) / _fz / 2 < .675: F.append(f"[93] {_n}: strip window reaches up into the blank-tile row")
if not _pre98:
    # [94] Tiffany 6:58pm (URGENT): the v97 PLM Chartreuse re-cut read lemon yellow. Locked racks show their approved photo, and
    # every PLM painted rack photo shown (thumbnail + HD) stays within 8 deg hue (RGB distance 30 when low saturation) of its
    # reference colour (config/fym-rack-split-oct26.json plm_ref)
    import colorsys as _cs94, io as _io94, hashlib as _hl94
    _C94 = json.load(open(REPO + 'config/fym-rack-split-oct26.json'))
    for _k in _C94['locked']:
        _r = D['racks'].get(_k); _want = 'rk98' + ''.join(ch for ch in os.path.splitext(os.path.basename(_C94['replace'][_k]['img']))[0] if ch.isalnum())
        if not _r or _r.get('hid') or _r.get('im') != _want: F.append(f"[94] {_k}: does not show its locked, approved rack photo ({_C94['replace'][_k]['img']})")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fym_rack_images import shown as _shown94
    for _k, _n, _t, _h, _b in _shown94(B):
        if _k not in _C94['plm_ref'] or not _b: continue
        _a = np.asarray(Image.open(_io94.BytesIO(_b)).convert('RGBA')).reshape(-1, 4); _a = _a[_a[:, 3] > 200][:, :3]; _a = _a[~(_a.min(1) > 235)] if (_a.min(1) <= 235).sum() > 50 else _a
        _m = np.median(_a, 0); _ref = np.array(_C94['plm_ref'][_k], float)
        _h1, _l1, _s1 = _cs94.rgb_to_hls(*(_m / 255)); _h2, _l2, _s2 = _cs94.rgb_to_hls(*(_ref / 255)); _dh = abs(_h1 - _h2) * 360; _dh = min(_dh, 360 - _dh)
        if (min(_s1, _s2) >= .2 and _l2 < .93 and _dh > 8) or np.linalg.norm(_m - _ref) > (60 if min(_s1, _s2) >= .2 else 30):
            F.append(f"[94] {_n} ({_t}): colour {_m.astype(int).tolist()} drifted from PLM reference {_ref.astype(int).tolist()} (hue {_dh:.0f} deg)")
if not _pre98 and '/*v100 title*/' not in UI:  # v100 replaces [95] with [98] (her Oct 27 12:37am call)
    # [95] Tiffany 6:25pm: the card title uses the ASSIGNED set colour (s.tc), no contrast-loop darkening; light colours only get
    # a white outline
    if "const tc=s.tc||'#d6247f'/*v98 assigned title colour*/" not in UI or "/* v95 contrast */const Hh" in UI: F.append("[95] match card title colour is not the assigned set colour s.tc")
    if "/*v98 white outline for light colours*/" not in UI: F.append("[95] light title colours have no white outline")
if not _pre98:
    # [96] Main 6:25pm + 6:33pm: no visible mat/rack/tile name starts with a straight quote or carries a backslash (Peppi; curly quotes are fine); the Wren Mats
    # logo badge is the visible wordmark, and every brand logo file is not just a blank white square
    for _kind, _bag in (('mat', M), ('rack', D['racks']), ('tile', D['tiles'])):
        for _k, _o in _bag.items():
            if not _o.get('hid') and (str(_o.get('n', '')).startswith(('"', "'")) or '\\' in str(_o.get('n', ''))): F.append(f"[96] {_kind} name has a stray quote/backslash: {_o.get('n')}")
    _C96 = json.load(open(REPO + 'config/fym-names-logos-v98.json')); _hd96 = json.load(open(os.path.join(B, 'hd', 'index.json'))).get('l', {})
    for _b in _C96['logos']:
        if not str(D['logos'].get(_b, '')).startswith('lg98') or not str(_hd96.get(_b, '')).startswith('file:r98/'): F.append(f"[96] {_b} logo badge is not the visible v98 wordmark")
# [99] Tiffany Oct 27 2:06am (iPhone, Shop by brand: last brands unreachable, list sticks then floats mid-page): pop-up sheets
# inside the website frame must fit the phone screen and not chain their scroll into the page (v100c_sheet.py).
if 'function openSheet' in h and ('/*v100c sheet*/' not in h or 'overscroll-behavior:contain' not in h or "setProperty('--sbh'" not in h or '/*v100d visible*/' not in h): F.append('[99] framed pop-up sheets can run below the phone screen / chain scroll (v100c fix missing)')
# [98] Tiffany Oct 27 12:37am ("these cards are hideous now... I didn't tell anybody to do anything to the text"): the match-card
# title keeps the pre-Oct-26 look: solid fill + soft white offset shadow, NO outline (no strokeText on the title), exact s.tc when it
# reads (contrast >= 2.5), v97 same-hue darkening otherwise (builder/fym_fix_oct25/v100_title.py). Title style changes need HER yes.
if 'drawCard' in h and ('tcVL' in h or 'tcLow' in h or 'navy outline when very light' in h): F.append('[98] card title has an outline style (v98/v98b) - title must be solid fill + white offset shadow only (her Oct 27 call)')
if 'drawCard' in h and '/*v100 title*/' not in h: F.append('[98] card title is not the v100 (pre-Oct-26 look + exact assigned colour) version')
if os.path.isdir(os.path.join(B, 'r99')):
    # [97] Tiffany Oct 26 10:07pm ("Have all of the vertical racks been rotated to horizontal? Have backgrounds been removed from
    # racks where possible? Have we isolated a single horizontal rack from every set where it's possible?"): FAIL if a visible
    # rack's CARD image (HD if it has one, else the thumbnail) is portrait (h > w). WARN with the racks whose card image still has
    # an opaque photo background or is a multi-rack / lifestyle photo, so what's left is tracked (config/fym-rack-singles-oct26.json
    # 'left_as_is' gives the reason for each; v99_cut.py + v99_racksingles.py make the single horizontal cut-outs).
    import io as _io97
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fym_rack_images import shown as _shown97
    _C97 = json.load(open(REPO + 'config/fym-rack-singles-oct26.json')); _done97 = {c['key'] for c in _C97['cuts'].values()}
    _card97 = {}
    for _k, _n, _t, _h, _b in _shown97(B):
        if _b and (_t == 'hd' or _k not in _card97): _card97[_k] = (_n, _b)
    _opaque97 = []
    for _k, (_n, _b) in _card97.items():
        _im = Image.open(_io97.BytesIO(_b)); _A = np.asarray(_im.convert('RGBA')).astype(int)
        _m = _A[..., 3] > 40 if _A[..., 3].min() < 250 else _A[..., :3].min(2) < 235  # the rack itself (alpha, or non-white on a white photo)
        _ys, _xs = np.where(_m); _w, _hh = ((_xs.max() - _xs.min() + 1), (_ys.max() - _ys.min() + 1)) if len(_xs) else _im.size
        if _hh > _w: F.append(f"[97] rack card photo is portrait (rack {_w}x{_hh} px): {_n}")
        _a = _A[..., 3]
        if (_a < 20).mean() < 0.02 and _k not in _done97: _opaque97.append(_n)
    for _k, _v in _C97.get('left_as_is', {}).items():
        if _k in D['racks'] and not D['racks'][_k].get('hid') and D['racks'][_k]['n'] not in _opaque97: _opaque97.append(D['racks'][_k]['n'] + ' (' + _v + ')')
    if _opaque97: W97.append(f"[97] {len(_opaque97)} visible racks still show a photo background / several racks / lifestyle shot (left as is): " + '; '.join(sorted(set(_opaque97))))
    for _c in _C97['cuts'].values():  # every v99 cut that is on the card keeps the cut-out flag from the config
        _r = D['racks'].get(_c['key'])
        if _r and not _r.get('hid') and str(_r.get('im', '')).startswith('rk99') and bool(_r.get('c')) != bool(_c['c']): F.append(f"[97] {_r['n']}: cutout flag c should be {_c['c']}")
# [100] Tiffany Oct 27 2:21am ("This is going to get very old, me chasing down mats"; House Print sat 5 days after the watch saw it).
#       Missing partner mats: reads ONLY the last saved sweep (config/partner-mat-sweep.json, written by builder/partner_mat_sweep.py,
#       run by the twice-daily launch watch; Tiffany 2:26am: no scanning per build, no network here). FAIL: a full-size partner mat
#       published > 2 days ago that is in neither this build (key / u / u0 -> domain/handle) nor config/partner-mat-sweep-ignore.json
#       (with a reason). WARN: the sweep file is older than 3 days, or a partner store could not be read.
try:
    import datetime as _dt100, urllib.parse as _up100
    def _nu100(u):
        u = str(u or '')
        if '/discount/' in u and 'redirect=' in u:
            u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + _up100.unquote(u.split('redirect=', 1)[1].split('&')[0])
        u = re.sub(r'^https?://', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')
        return re.sub(r'^(www\.|shop\.)', '', u)
    _sw100p = REPO + 'config/partner-mat-sweep.json'
    if not os.path.exists(_sw100p): F.append("[100] no partner mat sweep on file (config/partner-mat-sweep.json): run python3 builder/partner_mat_sweep.py")
    else:
        _SW = json.load(open(_sw100p)); _IG = json.load(open(REPO + 'config/partner-mat-sweep-ignore.json'))
        _now = _dt100.datetime.now(_dt100.timezone.utc)
        _age = (_now - _dt100.datetime.fromisoformat(_SW['swept_at'])).total_seconds() / 86400
        if _age > 3: W97.append(f"[100] partner mat sweep is {_age:.1f} days old (config/partner-mat-sweep.json, {_SW['swept_at']}): the launch watch should refresh it twice daily")
        _have = set()
        for _k, _m in M.items():
            for _u in (_k, _m.get('u'), _m.get('u0')):
                if _u: _have.add(_nu100(_u))
        _miss100, _err100 = [], []
        for _dom, _v in _SW['stores'].items():
            if str(_v.get('status', '')).startswith('error'): _err100.append(f"{_dom} ({_v['status'][:60]})")
            _sb = (_IG.get('stores_before') or {}).get(re.sub(r'^(www\.|shop\.)', '', _dom))
            for _pub, _t, _hd in _v.get('mats', []):
                _key = _nu100(f'{_dom}/{_hd}')
                if _key in _have or _key in _IG['items']: continue
                try: _pd = _dt100.datetime.fromisoformat(_pub)
                except Exception: _pd = _now
                if (_now - _pd).total_seconds() / 86400 <= 2: continue
                if _sb and _pub[:10] < _sb['before']: continue
                _miss100.append(f"{_v.get('brand', _dom)} | {_t} ({_key}, live {_pub[:10]})")
        if _miss100: F.append(f"[100] {len(_miss100)} full-size partner mats live > 2 days are not in FYM (add them, or list them with a reason in config/partner-mat-sweep-ignore.json): " + '; '.join(_miss100[:12]))
        if _err100: W97.append(f"[100] partner stores the last sweep could not read (not checked): " + '; '.join(_err100))
except Exception as _e: F.append(f"[100] missing partner mat check did not run: {_e}")
# [102] Oct 29 (Tiffany 12:09/12:11pm): Aerial switch sits next to the deck in BOTH doors; the tile photo in Aerial is a
# bottom-right inset (never centred over the mat); Shop by brand in BOTH doors says who takes MAHJMATCH and who has no discount.
try:
    _h102 = open(os.path.join(B, 'index.html')).read()
    if 'const VROW=' not in _h102 or _h102.count('VROW()') < 3: F.append("[102] Up close / Aerial switch is not next to the deck in both doors (VROW missing)")
    _om = re.search(r'\.onmat\{([^}]*)\}', _h102)
    if not _om or 'translate(-50%' in _om.group(1) or 'right:' not in _om.group(1): F.append("[102] Aerial tile photo is centred over the mat (must be a bottom-right inset)")
    if "matSrc(S.dmat)}\" alt=\"${esc(MN(S.dmat))} mat\" class=\"tkm\"" not in _h102: F.append("[102] start-with-a-mat side has no Aerial view (mat full, tiles inset)")
    if 'save 10% or more with code MAHJMATCH' not in _h102 or 'no discount available' not in _h102: F.append("[102] Shop by brand does not label partner (code) vs non-partner (no discount) brands")
    if "bselect('mbr'" not in _h102 or 'matBrandMenu()+' not in _h102: F.append("[102] start-with-a-mat side has no Shop by brand dropdown")
except Exception as _e: F.append(f"[102] aerial/brand check did not run: {_e}")
# [103] Oct 29 (Tiffany 1:31pm): a card TITLE is the tile BACK colour. Sunday Blues showed tan because its stored tc was the
# ivory/tan tile body. Every set with a colour card (config/colorcards.json) and no album title colour must use its first back
# colour (or, for an all-ivory back, the colour card's title colour). Also: the Shop by brand code callout is a pink feature (1:57pm).
try:
    _cc103 = json.load(open(REPO + 'config/colorcards.json'))['sets']
    _h103 = open(os.path.join(B, 'index.html')).read()
    _am = re.search(r'const tc=.*?\(\(\)=>\{const h=\((\{[^}]*\})\)\[s\.name\]', _h103)
    _alb103 = set(json.loads(_am.group(1))) if _am else set()
    _al103 = {'Sunday Tile Set': 'Sunday'}
    def _lum103(x): return sum(w * int(x[i:i+2], 16) / 255 for w, i in ((.2126, 1), (.7152, 3), (.0722, 5)))
    _bad103 = []
    for _k, _v in _cc103.items():
        _nm = _al103.get(_v['name'], _v['name'])
        if _nm in _alb103: continue
        _b0 = _v['backs'][0][1]
        _want = _b0 if _lum103(_b0) < 0.6 else _v.get('col')
        for _s in D['sets']:
            if _s['name'] == _nm and (_s.get('maker') == _v.get('brand') or not _v.get('brand')) and (_s.get('tc') or '').lower() != (_want or '').lower():
                _bad103.append(f"{_nm} title {_s.get('tc')} (should be {_want})")
    if _bad103: F.append("[103] card title is not the tile back colour: " + '; '.join(_bad103))
    if not re.search(r'\.bnote\.gen>span\{[^}]*color:#c8325f', _h103) or '.bnote.gen{background:transparent;color:var(--mute)' in _h103:
        F.append("[103] Shop by brand code callout is not the pink feature (it went back to light gray)")
except Exception as _e: F.append(f"[103] title colour / callout check did not run: {_e}")
# [105] Oct 30 (Tiffany Oct 29 3:29-3:33pm, Oct 30 2:49am): the tiles door must NOT open on the alphabetical tile list
# (Mahj Mood "90s Pool Party", YMI "Aloha"). With no colour / brand / search it shows PARTNER BRAND LOGOS: Oh My Mahjong first,
# partners before non-partners, every partner with a logo; colour results list partner sets before non-partner sets.
try:
    _h105 = open(os.path.join(B, 'index.html')).read()
    if 'function blogoView()' not in _h105 or "if(S.tcol==='')return blogoView();" not in _h105:
        F.append("[105] tiles door opens on the alphabetical tile list, not the partner brand logos")
    if "q('[data-blogo]')" not in _h105: F.append("[105] tapping a brand logo does nothing (no data-blogo handler)")
    _v105 = re.search(r"function blogoView\(\)\{.*?function brandMenu", _h105, re.S)
    if not _v105 or _v105.group(0).find('P.map(one)') < 0 or _v105.group(0).find('P.map(one)') > _v105.group(0).find('NP.map(one)'):
        F.append("[105] brand logos do not put partner brands before non-partners")
    _bl = re.search(r'const BLOGO=(\{.*?\});const BLORD=(\[.*?\]);', _h105)
    if not _bl: F.append("[105] brand logo data (BLOGO/BLORD) missing")
    else:
        _blogo, _blord = json.loads(_bl.group(1)), json.loads(_bl.group(2))
        if not _blord or _blord[0] != 'Oh My Mahjong': F.append("[105] Oh My Mahjong is not the first brand logo")
        _bc = {o.get('bn') for X in (D.get('mats', {}), D.get('racks', {}), D.get('tiles', {})) for o in X.values()
               if isinstance(o, dict) and o.get('bn') and not o.get('hid') and o.get('pa') and not o.get('nc')}
        _miss = sorted({s['maker'] for s in D['sets'] if vis(s) and s['maker'] in _bc and s['maker'] not in _blogo})
        if _miss: F.append("[105] partner brands with no logo on the opening screen: " + ', '.join(_miss))
    if not re.search(r"flatMap\(n=>all\.filter\(x=>x\[0\]\.name===n\)\)\.sort\(\(a,b\)=>!!T\[a\[0\]\.tile\]\.soon-!!T\[b\[0\]\.tile\]\.soon\|\|\(BPA\(a\[0\]\.maker\)", _h105):
        F.append("[105] colour results do not list partner tile sets first")
except Exception as _e: F.append(f"[105] brand logo opening view check did not run: {_e}")
# [104] Oct 30 (rules audit GA4; CLAUDE.md FYM 0 "every publish goes to BOTH places"): the build's public "Version X.Y" label
# == the newest site-app/fym-vNN on the fym-site-preview branch == the page-block pinned at the TOP of
# site/livepatch/fym-preview-oct21/README.md (that pin is what gets pasted on Squarespace). WARNING by default (the README
# pin is often written after the gate runs); with --release (before a publish is called done) it FAILS.
W104 = []
try:
    import subprocess as _sp104
    def _g104(*a):
        return _sp104.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, timeout=60).stdout
    _sp104.run(['git', '-C', REPO, 'fetch', '-q', 'origin', 'fym-site-preview:refs/remotes/origin/fym-site-preview'], capture_output=True, timeout=60)
    _lab104 = re.findall(r'Version (\d+\.\d+)', open(os.path.join(B, 'index.html')).read())
    _lab104 = _lab104[0] if _lab104 else None
    _nn104 = sorted(int(x) for x in re.findall(r'fym-v(\d+)', _g104('ls-tree', '--name-only', 'origin/fym-site-preview', 'site-app/')))
    _site104 = None
    if _nn104:
        _sl = re.findall(r'Version (\d+\.\d+)', _g104('show', f'origin/fym-site-preview:site-app/fym-v{_nn104[-1]}/index.html'))
        _site104 = _sl[0] if _sl else None
        if _site104 != _lab104:
            W104.append(f"build is Version {_lab104} but the newest website copy site-app/fym-v{_nn104[-1]} is Version {_site104}")
    _pin104 = re.search(r'[Pp]in page-block @([0-9a-f]{7,40})', open(REPO + 'site/livepatch/fym-preview-oct21/README.md').read())
    if not _pin104:
        W104.append("no 'Pin page-block @<sha>' line in site/livepatch/fym-preview-oct21/README.md")
    elif _nn104:
        _ref = set(re.findall(r'site-app/fym-v(\d+)', _g104('show', f'{_pin104.group(1)}:site/livepatch/fym-preview-oct21/page-block.html')))
        if str(_nn104[-1]) not in _ref:
            W104.append(f"README 0a pin @{_pin104.group(1)[:8]} loads site-app/fym-v{'/'.join(sorted(_ref)) or '?'}, not the newest fym-v{_nn104[-1]} (update the README pin)")
except Exception as _e:
    W104.append(f"version check did not run: {_e}")
# [106] Oct 30 (Tiffany 2:51am: "you can't just say you don't have a photo and not go to the website, look through all the photos";
#       Anders Ruff Mahj in Bloom had a tile-pile shot and showed 'Photo coming soon'). A visible tile set may show the placeholder
#       (T.soon) ONLY if config/fym-tile-photo-fills-*.json logs it as kind 'none' with photos_checked > 0 (every brand photo looked at).
try:
    import glob as _gl106
    _ok106 = set()
    for _f106 in _gl106.glob(REPO + 'config/fym-tile-photo-fills-*.json'):
        for _e106 in json.load(open(_f106)).get('tiles', []):
            if _e106.get('kind') == 'none' and int(_e106.get('photos_checked') or 0) > 0: _ok106.add(_e106['key'])
    _bad106 = [f"{T[s['tile']].get('bn', '')} {s['name']}" for s in D['sets'] if vis(s) and T.get(s['tile'], {}).get('soon') and s['tile'] not in _ok106]
    if _bad106: F.append(f"[106] {len(_bad106)} visible tile sets show 'Photo coming soon' without a logged check of every brand photo (config/fym-tile-photo-fills-*.json kind 'none', photos_checked > 0): " + '; '.join(_bad106[:15]))
except Exception as _e: F.append(f"[106] placeholder photo check did not run: {_e}")
# [107] Oct 30 (v104 QA E1): new mats were APPENDED to the end of every set's s.rank (and left out of s.cr), so in the mat door
#       (setsForMat sorts sets by s.rank position) all 7 Oct 30 partner mats showed the SAME tile order (non-partner Coquette first)
#       and ~65 earlier adds had the same bug. Fix: builder/fym_fix_oct30/v104rank.py. Fails if a visible mat sits in the last
#       TAIL slots of every set's rank (never ranked), or if 3+ visible mats share an identical mat-door top-8 set order.
try:
    _O107 = D['order']; _pos107 = {}
    for s_ in D['sets']:
        _r = s_.get('rank') or []; _L = len(_r)
        for _p, _j in enumerate(_r): k_ = _O107[_j]; _pos107[k_] = max(_pos107.get(k_, 0), _L - _p)
    _st107 = [f"{M[k_].get('bn', '')} {M[k_]['n']}" for k_, v_ in _pos107.items() if k_ in M and not M[k_].get('hid') and not M[k_].get('hol') and v_ <= 130]
    if _st107: F.append(f"[107] {len(_st107)} visible mats were appended to the tail of every set's ranking instead of colour-ranked (run builder/fym_fix_oct30/v104rank.py): " + '; '.join(_st107[:12]))
    _vs107 = [s_ for s_ in D['sets'] if vis(s_)]; _sig107 = {}
    _OI107 = {k_: j_ for j_, k_ in enumerate(_O107)}
    for k_, m_ in M.items():
        if m_.get('hid') or k_ not in _OI107: continue
        _ix = _OI107[k_]
        _rows = sorted((0 if any(x[0] == k_ for x in s_['m']) else 1, s_['rank'].index(_ix) if _ix in s_['rank'] else 10 ** 9, n_) for n_, s_ in enumerate(_vs107))
        _sig107.setdefault(tuple(r_[2] for r_ in _rows[:8]), []).append(m_['n'])
    _dup107 = [v_ for v_ in _sig107.values() if len(v_) >= 3]
    if _dup107: F.append(f"[107] {len(_dup107)} groups of 3+ mats show an identical mat-door tile order (un-ranked appends): " + '; '.join(', '.join(v_[:4]) for v_ in _dup107[:5]))
except Exception as _e: F.append(f"[107] appended-mat rank check did not run: {_e}")
# [108] Oct 30 (v104 QA: Bespoke XL Mega flat-lays, Round Top Stamped, House of Hydrangea, Lumera did not fill the frame). Gate [45]
#       only measures the wide match-card BAND (>= 12% not-white) of each photo, so a full-set flat-lay with big white margins, a
#       bag shot with tiles in one corner or a blurry close-up all passed it; nothing checked the square swipe photo / round picker
#       thumbnail. New standard for every tile photo added from v104 on (t1NN/ folders, NN >= 104): the centre-square circle may be
#       at most 11% LARGE empty background (border-connected white/black, opened with a 14px square at 200px so gaps between tiles
#       and white faces with line art don't count). Exemptions (white tiles laid flat, one brand photo): config/fym-tile-fill-exempt-oct30.json.
try:
    from scipy import ndimage as _nd108
    _ex108 = json.load(open(REPO + 'config/fym-tile-fill-exempt-oct30.json'))['tiles'] if os.path.exists(REPO + 'config/fym-tile-fill-exempt-oct30.json') else {}
    def _empty108(path, k=14):
        im = Image.open(path).convert('RGB'); S_ = min(im.size)
        im = im.crop(((im.width - S_) // 2, (im.height - S_) // 2, (im.width + S_) // 2, (im.height + S_) // 2)).resize((200, 200))
        a = np.asarray(im).astype(int); flat = ((a.min(2) > 232) & ((a.max(2) - a.min(2)) < 20)) | (a.max(2) < 30)
        big = _nd108.binary_opening(flat, structure=np.ones((k, k))); lab, _ = _nd108.label(big)
        bd = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        bg = np.isin(lab, list(bd)); yy, xx = np.mgrid[:200, :200]; circ = ((yy - 100) ** 2 + (xx - 100) ** 2) <= 100 ** 2
        return float(bg[circ].mean())
    _b108 = []
    for s_ in D['sets']:
        t_ = T.get(s_['tile']) or {}
        f_ = t_.get('full') or ''; mm_ = re.match(r't(\d+)/', f_)
        if not vis(s_) or t_.get('soon') or not mm_ or int(mm_.group(1)) < 104 or s_['tile'] in _ex108 or not os.path.exists(os.path.join(B, f_)): continue
        v_ = _empty108(os.path.join(B, f_))
        if v_ > 0.11: _b108.append(f"{s_['name']} ({s_['maker']}) {v_:.2f}")
    if _b108: F.append(f"[108] {len(_b108)} new tile photos don't fill the frame (large empty background in the swipe photo / picker circle): " + '; '.join(_b108[:12]))
except Exception as _e: F.append(f"[108] tile frame-fill check did not run: {_e}")
if W104:
    if '--release' in sys.argv:
        F.append("[104] artifact / website copy / README pin are not the same version: " + '; '.join(W104))
    else:
        print("FYM GATE WARNING [104] (FAIL with --release): " + '; '.join(W104))
if W97:
    print("FYM GATE WARNINGS (v97):")
    for _w in W97: print('  ' + _w)

if W:
    print(f"FYM GATE WARNING [9]: {sum(map(len, W.values()))} unmatched non-partner mats visible, brands pending Tiffany's decision (builder/fym_flags/nonpartner_pending.json):")
    for b, v in sorted(W.items()): print(f"  {b} ({len(v)}): " + ', '.join(v[:8]) + (' ...' if len(v) > 8 else ''))
if F:
    print(f"FYM GATE: FAIL ({len(F)} problems)")
    for f in F: print('  ' + f)
    sys.exit(1)
print(f"FYM GATE: PASS  (album sets checked: {len(seen)}, sets: {len(D['sets'])}, visible: {sum(1 for s in D['sets'] if vis(s))}, locks: tiles {len(locks['tiles'])} sets {len(locks['sets'])} mats {len(locks['mats'])})")
