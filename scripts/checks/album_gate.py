"""album_gate (Album Playbook, Nov 8: "How it's enforced" -> "Every step, start to finish").

An album's review page may only be built once its record shows steps 1-8 done. The record is
config/album-records/<set>.json (see that file's _about); the other inputs are the shared configs.

Checks, in playbook order:
  [1] FYM set ready     config/album-fym-sets.json colorcards.<set> -> an FYM slug, and that slug has walls
                        (a back colour in config/tableview-back-colors.json)
  [2] colour card       config/colorcards.json sets.<set> with backs + faces, and the colour card image exists
  [3] TNT search        config/tnt-recs.json sets.<set> with scanned + source + posts_read > 0 + terms[] + scrolled_to_end (tnt_check.py)
  [3b] other groups     config/tnt-recs.json sets.<set>.other_groups: scanned + groups[] (each with members),
                        or an empty groups list WITH a note
  [0] tile photo        record tile_photo approved_at set (her yes in chat; scripts/checks/tile_photo_check.py)
  [3c] mat discovery   record discovery {at, searches[]} (light Google/Etsy/Amazon search; finds may be empty) + variety warning
  [4] pool              record pool.size > 0 and pool.sources
  [4b] committed pull   record pool.pulled_by = scripts/albumreview/pull.py and pool.no_photo = 0
  [4a] catalog fresh    record catalog_checked.at the same day as pool.pulled_at and not after it
                        (scripts/albumreview/catalog_refresh.py: ShopMy every collection + partner-store sweep)
  [5] by-sight pass     the left-out list exists, has mats, and every mat has a reason
  [6] holiday           the album spec has holiday cards, or record holiday.considered + note (none fit)
  [7] faces pre-picked  record faces.picks = 5 keys, each with a face image
  [8] cards + code band manifest exists, every card file exists, card_code_band_check passes on it
  [8b] card sharpness   no card has a blurry/pixelated mat (card_sharpness.py; Nov 9)

Usage:
  python3 scripts/checks/album_gate.py <set>        PASS / FAIL with the missing steps (exit 1 on FAIL)
  python3 scripts/checks/album_gate.py --in-progress   every album in progress (front door; reads docs/status/live-albums.json)
  python3 scripts/checks/album_gate.py --refresh-live  re-check which colour-card albums are live (network)
  python3 scripts/checks/album_gate.py <set> --golive   GO-LIVE mode (Playbook step 10b, Nov 8 6:02pm): steps 1-8 PLUS
                        [10b] every bring-in in record "bringins" has its paid link (route from config/link-routes.json:
                        ShopMy link for shopmy-*; Amazon also saved in Associates + imported by Ops) AND catalog staging
                        (scripts/albumreview/bringins.py missing()). Run before the album goes live (NEW-ALBUM-CHECKLIST).
Imported by scripts/albumreview/build_review.py (refuses to write the page on FAIL) and scripts/hooks/front_door.py."""
import json, os, sys, glob
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/checks')
from tnt_check import complete as _tnt_complete, why_incomplete as _tnt_why
sys.path.insert(0, R + 'scripts/checks')


def J(p, default=None):
    try: return json.load(open(R + p))
    except Exception: return default


def record(s):
    return J(f'config/album-records/{s}.json')


def variety(s, rec):
    import glob as _g
    tops = {}
    for f in _g.glob(R + 'scripts/albumcard/specs/*.json'):
        try: d = json.load(open(f))
        except Exception: continue
        if not isinstance(d, dict) or not isinstance(d.get('mats'), list): continue
        key = os.path.basename(f).rsplit('_', 1)[0]
        tops[key] = [m.get('name') for m in d['mats'] if isinstance(m, dict) and not m.get('holiday')][:6]
    mine = tops.get(os.path.basename(rec.get('spec', '')).rsplit('_', 1)[0], [])
    if not mine: return None
    common = [n for n in mine if sum(1 for k, v in tops.items() if n in v and k != os.path.basename(rec['spec']).rsplit('_', 1)[0]) >= 5]
    return f'all 6 standouts are in the top 6 of 5+ other albums ({", ".join(common)}): add one rare or special match' if len(common) == len(mine) == 6 else None


def check(s):
    """Returns (problems, proof). proof = what the review page shows for steps 1-8."""
    bad, proof = [], {}
    rec = record(s)
    if rec is None:
        return [f'[0] no album record config/album-records/{s}.json'], proof
    # [0] tile photo approved by her in chat (Playbook step 0, Nov 8 1:37pm)
    from tile_photo_check import problem as tp_problem, tile_photo
    tpp = tp_problem(s)
    if tpp: bad.append('[0] ' + tpp)
    tp = tile_photo(s) or {}
    proof['tile_photo'] = tp
    # [1] FYM set + walls
    afs = J('config/album-fym-sets.json', {})
    slug = (afs.get('colorcards') or {}).get(s)
    walls = J('config/tableview-back-colors.json', {})
    w = walls.get(slug) if slug else None
    if not slug: bad.append(f'[1] tiles not set up in Find Your Mat-ch: config/album-fym-sets.json colorcards.{s} has no FYM set')
    elif not (isinstance(w, dict) and w.get('back')): bad.append(f'[1] FYM set {slug} has no walls (config/tableview-back-colors.json)')
    proof['fym'] = {'slug': slug, 'back': (w or {}).get('back'), 'photo': tp.get('file')}
    for k in ('file', 'inset'):
        if tp.get(k) and not os.path.exists(R + tp[k]): bad.append(f"[1] tile photo file missing: {tp[k]}")
    # [2] colour card
    cc = (J('config/colorcards.json', {}).get('sets') or {}).get(s)
    if not cc or not cc.get('backs') or not cc.get('faces'): bad.append(f'[2] no colour card in config/colorcards.json sets.{s}')
    img = rec.get('colorcard_img')
    if not img or not os.path.exists(R + img): bad.append(f'[2] colour card image missing ({img})')
    proof['colorcard'] = {'img': img, 'wheel': rec.get('wheel_img'), 'backs': (cc or {}).get('backs'), 'faces': (cc or {}).get('faces')}
    # [3] TNT + [3b] other groups
    t = (J('config/tnt-recs.json', {}).get('sets') or {}).get(s)
    if not (isinstance(t, dict) and t.get('scanned') and t.get('source')): bad.append(f'[3] no Tiles & Tablescapes search on record (config/tnt-recs.json sets.{s})')
    elif not _tnt_complete(t): bad.append(f'[3] Tiles & Tablescapes search not proven exhaustive ({_tnt_why(t)}): config/tnt-recs.json sets.{s} needs posts_read > 0, terms[], scrolled_to_end: true (Tiffany Nov 8 6:20pm)')
    og = (t or {}).get('other_groups')
    if not isinstance(og, dict) or not og.get('scanned'): bad.append(f'[3b] other big Facebook groups not searched (config/tnt-recs.json sets.{s}.other_groups)')
    elif not og.get('groups') and not og.get('note'): bad.append('[3b] other_groups has no groups and no note saying why')
    elif any(not g.get('members') for g in og.get('groups', [])): bad.append('[3b] other_groups: every group needs its member count')
    proof['research'] = {'tnt': t, 'other': og}
    # [3c] mat discovery (Playbook step 3b, Tiffany Nov 8 1:59pm): a light targeted web search on record (finds may be empty)
    dsc = rec.get('discovery') or {}
    if not dsc.get('at') or not dsc.get('searches'): bad.append(f'[3c] no mat discovery on record (record discovery {{at, searches, new_finds, misses_added}})')
    # variety (warning only): the top 6 should not all be mats already in the top 6 of 5+ other albums
    proof['variety_warning'] = variety(s, rec)
    # [4] pool
    pool = rec.get('pool') or {}
    if not pool.get('size') or not pool.get('sources'): bad.append('[4] no candidate pool on record (record pool.size + sources)')
    proof['pool'] = pool
    # [4b] the pull is the committed one (Nov 8, after Tiffany caught Britt Mills Scarlett + Flora missing from Deco Lagoon: the
    # scratch pull silently dropped 13 scored mats with no gallery photo and never showed the contrast side)
    if pool and (pool.get('pulled_by') != 'scripts/albumreview/pull.py' or pool.get('no_photo', 1) != 0):
        bad.append(f'[4b] pool not pulled by scripts/albumreview/pull.py (every FYM photo, no silent drops, contrast side on the sheets): run python3 scripts/albumreview/pull.py {s} <out> --record and judge its miss sheets')
    # [4a] catalog up to date before the pull (Tiffany Nov 8 1:33pm): catalog_checked the same day as pool.pulled_at, not after it
    ck = rec.get('catalog_checked') or {}
    import datetime as _dt
    try:
        ca, pa = _dt.datetime.fromisoformat(ck['at']), _dt.datetime.fromisoformat(pool['pulled_at'])
        if ca.date() != pa.date(): bad.append(f"[4a] catalog checked {ca:%b %d} but the pool was pulled {pa:%b %d}: run scripts/albumreview/catalog_refresh.py {s} the day of the pull")
        elif ca > pa: bad.append('[4a] the pool was pulled before the catalog check: re-pull after scripts/albumreview/catalog_refresh.py')
    except Exception:
        bad.append(f'[4a] catalog not checked before the pull (record catalog_checked + pool.pulled_at): run scripts/albumreview/catalog_refresh.py {s}')
    proof['catalog'] = ck
    # [5] by-sight
    lo = rec.get('leftout') or {}
    lst = (J(lo.get('file', ''), {}) or {}).get(lo.get('key')) if lo.get('file') else None
    if not lst: bad.append('[5] no by-sight pass: the left-out list is missing or empty')
    elif any(not (m.get('why') or '').strip() for m in lst): bad.append('[5] left-out mats without a reason: ' + ', '.join(m['name'] for m in lst if not (m.get('why') or '').strip()))
    proof['leftout'] = len(lst or [])
    # [6] holiday
    spec = J(rec.get('spec', ''), {}) or {}
    nh = sum(1 for m in spec.get('mats', []) if m.get('holiday'))
    hol = rec.get('holiday') or {}
    if not nh and not (hol.get('considered') and hol.get('note')): bad.append('[6] no holiday section and no record that holiday mats were considered')
    proof['holiday'] = {'n': nh, 'note': hol.get('note')}
    # [7] faces
    fz = rec.get('faces') or {}
    picks = [p['key'] if isinstance(p, dict) else p for p in fz.get('picks', [])]
    # 5 = Claude's pre-picks; her own picks on the review page are final at any count >= 5 (A YES IS A YES; Deco Lagoon: 7, Nov 8)
    if len(picks) < 5: bad.append(f'[7] faces not pre-picked: need 5, record has {len(picks)}')
    miss = [k for k in picks if not os.path.exists(R + fz.get('dir', '') + k + '.png')]
    if miss: bad.append('[7] face images missing: ' + ', '.join(miss))
    proof['faces'] = picks
    # [8] cards + code band
    cd = rec.get('cards_dir')
    man = J(f'{cd}/manifest.json') if cd else None
    if not man or not man.get('cards'): bad.append(f'[8] no match cards (manifest {cd}/manifest.json)')
    else:
        gone = [c['file'] for c in man['cards'] if not os.path.exists(f'{R}{cd}/{c["file"]}')]
        if gone: bad.append(f'[8] {len(gone)} card image(s) missing, e.g. {gone[0]}')
        from card_code_band_check import check_file
        band = check_file(R + f'{cd}/manifest.json')
        if band: bad.append(f'[8] code band check FAIL: {band[0]}')
        names = {m['name'] for m in spec.get('mats', [])}
        notin = [c['mat'] for c in man['cards'] if c['mat'] not in names]
        if notin: bad.append(f'[8] cards are stale (not in the spec): {", ".join(notin[:3])}; rebuild the cards')
        nspec = [m['name'] for m in spec.get('mats', []) if m['name'] not in {c['mat'] for c in man['cards']}]
        if nspec: bad.append(f'[8] spec mats with no card: {", ".join(nspec[:3])}; rebuild the cards')
        # [8b] Nov 9 (Tiffany: blurry Dec 1994 + Festive Plaid card, white-boxed Virora tiles): every built card's mat must be sharp
        # and its tile inset filled (card_sharpness / tile_fill_check; gen2.py refuses new ones, this catches older builds)
        import card_sharpness as _CS
        from PIL import Image as _I
        _ok = _CS.ok_list(); _soft = []
        for c in man['cards']:
            f = f'{R}{cd}/{c["file"]}'
            if os.path.exists(f) and c['file'] not in _ok and _CS.blurry(_CS.measure(_I.open(f))): _soft.append(c['file'])
        if _soft: bad.append(f'[8b] {len(_soft)} card(s) with a blurry/pixelated mat, e.g. {_soft[0]}: re-render from the brand full-size photo')
        proof['cards'] = {'n': len(man['cards']), 'tnt': sum(1 for c in man['cards'] if c.get('caption_note') == 'TNT rec'), 'band': 'PASS' if not band else 'FAIL'}
    return bad, proof


SKIP = {'style-of-your-life'}  # dropped Nov 7 11:47pm (Dillard's exclusive), same as tnt_check


def refresh_live():
    """Writes docs/status/live-albums.json: colour-card sets whose album page answers 200 (profile 'album' URL, else
    /<set>-mahjong-tile-matches). Network; the morning HQ cleanup / any chat runs it. The front door only reads the file."""
    import subprocess, datetime
    cc = J('config/colorcards.json', {}).get('sets', {})
    live = []
    for s in cc:
        u = (J(f'config/profiles/{s}.json', {}) or {}).get('album') or f'https://www.mahjmatchmaker.com/{s}-mahjong-tile-matches'
        c = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-L', '--max-time', '10', u], capture_output=True, text=True).stdout
        if c == '200': live.append(s)
    os.makedirs(R + 'docs/status', exist_ok=True)
    json.dump({'at': datetime.datetime.now().isoformat(timespec='seconds'), 'live': live}, open(R + 'docs/status/live-albums.json', 'w'), indent=1)
    return live


def in_progress():
    """Albums in progress = config/album-fym-sets.json 'upcoming' sets that have a colour card, plus every colour-card set
    with an FYM set whose album is not live (record live:true or docs/status/live-albums.json)."""
    afs = J('config/album-fym-sets.json', {})
    cc = J('config/colorcards.json', {}).get('sets', {})
    fym = afs.get('colorcards') or {}
    slug2set = {v: k for k, v in fym.items() if v}
    live = set(J('docs/status/live-albums.json', {}).get('live', []))
    out = {slug2set[x] for x in (afs.get('upcoming') or {}) if x in slug2set}
    for s in cc:
        if s in SKIP or s in live or not fym.get(s) or (record(s) or {}).get('live'): continue
        out.add(s)
    return sorted(out - SKIP)


def slot_check(s):
    """[10c] ONE ALBUM A WEEK (Tiffany Nov 10): a go-live date in config/album-launch-slots.json,
    not before it, and no other album in the same Mon-Sun week."""
    import datetime as dt
    sl = J('config/album-launch-slots.json', {}).get('slots', {})
    slug = s.lower().replace(' ', '-').replace('(', '').replace(')', '')
    keys = [k for k in sl if k == slug or k == s]
    if not keys:
        return [f"[10c] {s}: no go-live slot. Pick its week in config/album-launch-slots.json (one album a week; stage it hidden until then)"]
    d = dt.date.fromisoformat(sl[keys[0]]); bad = []
    if dt.date.today() < d: bad.append(f"[10c] {s}: slot is {d}, not yet. Keep the page hidden until then")
    wk = d.isocalendar()[:2]
    others = [k for k, v in sl.items() if k != keys[0] and dt.date.fromisoformat(v).isocalendar()[:2] == wk]
    if others: bad.append(f"[10c] {s}: week of {d} already has {', '.join(others)}. One album a week: move it")
    return bad


def golive(s):
    """[10b] bring-in loop: every bring-in closed (paid link + catalog staging)."""
    sys.path.insert(0, R + 'scripts/albumreview')
    import bringins as BI
    bad = []
    for e in (record(s) or {}).get('bringins', []):
        m = BI.missing(e)
        if m: bad.append(f"[10b] bring-in {e.get('mat')} ({e.get('brand')}, route {e.get('route')}) still needs: " + ', '.join(m))
    return bad


def main(a):
    if a and a[0] == '--refresh-live':
        print('live albums:', ', '.join(refresh_live())); return 0
    if a and a[0] == '--in-progress':
        fails = 0
        for s in in_progress():
            bad, _ = check(s)
            if bad:
                fails += 1
                print(f'ALBUM GATE FAIL {s} ({len(bad)} missing): ' + bad[0][:150])
        if not fails: print('ALBUM GATE PASS: every album in progress has steps 1-8 on record')
        return 1 if fails else 0
    if not a: sys.exit(__doc__)
    bad, proof = check(a[0])
    if '--golive' in a: bad += golive(a[0]) + slot_check(a[0])
    if bad:
        print(f'ALBUM GATE FAIL {a[0]} ({len(bad)}):'); [print('  ' + b) for b in bad]; return 1
    if proof.get('variety_warning'): print('WARNING (variety): ' + proof['variety_warning'])
    print(f'ALBUM GATE PASS {a[0]}: steps 1-8 on record' + (f", {len((record(a[0]) or {}).get('bringins', []))} bring-ins closed (go-live)" if '--golive' in a else '')); return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
