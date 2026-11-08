"""album_gate (Album Playbook, Nov 8: "How it's enforced" -> "Every step, start to finish").

An album's review page may only be built once its record shows steps 1-8 done. The record is
config/album-records/<set>.json (see that file's _about); the other inputs are the shared configs.

Checks, in playbook order:
  [1] FYM set ready     config/album-fym-sets.json colorcards.<set> -> an FYM slug, and that slug has walls
                        (a back colour in config/tableview-back-colors.json)
  [2] colour card       config/colorcards.json sets.<set> with backs + faces, and the colour card image exists
  [3] TNT search        config/tnt-recs.json sets.<set> with scanned + source (scripts/checks/tnt_check.py)
  [3b] other groups     config/tnt-recs.json sets.<set>.other_groups: scanned + groups[] (each with members),
                        or an empty groups list WITH a note
  [4] pool              record pool.size > 0 and pool.sources
  [5] by-sight pass     the left-out list exists, has mats, and every mat has a reason
  [6] holiday           the album spec has holiday cards, or record holiday.considered + note (none fit)
  [7] faces pre-picked  record faces.picks = 5 keys, each with a face image
  [8] cards + code band manifest exists, every card file exists, card_code_band_check passes on it

Usage:
  python3 scripts/checks/album_gate.py <set>        PASS / FAIL with the missing steps (exit 1 on FAIL)
  python3 scripts/checks/album_gate.py --in-progress   every album in progress (front door; reads docs/status/live-albums.json)
  python3 scripts/checks/album_gate.py --refresh-live  re-check which colour-card albums are live (network)
Imported by scripts/albumreview/build_review.py (refuses to write the page on FAIL) and scripts/hooks/front_door.py."""
import json, os, sys, glob
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/checks')


def J(p, default=None):
    try: return json.load(open(R + p))
    except Exception: return default


def record(s):
    return J(f'config/album-records/{s}.json')


def check(s):
    """Returns (problems, proof). proof = what the review page shows for steps 1-8."""
    bad, proof = [], {}
    rec = record(s)
    if rec is None:
        return [f'[0] no album record config/album-records/{s}.json'], proof
    # [1] FYM set + walls
    afs = J('config/album-fym-sets.json', {})
    slug = (afs.get('colorcards') or {}).get(s)
    walls = J('config/tableview-back-colors.json', {})
    w = walls.get(slug) if slug else None
    if not slug: bad.append(f'[1] tiles not set up in Find Your Mat-ch: config/album-fym-sets.json colorcards.{s} has no FYM set')
    elif not (isinstance(w, dict) and w.get('back')): bad.append(f'[1] FYM set {slug} has no walls (config/tableview-back-colors.json)')
    proof['fym'] = {'slug': slug, 'back': (w or {}).get('back'), 'photo': rec.get('tile_photo')}
    if rec.get('tile_photo') and not os.path.exists(R + rec['tile_photo']): bad.append(f"[1] tile photo missing: {rec['tile_photo']}")
    # [2] colour card
    cc = (J('config/colorcards.json', {}).get('sets') or {}).get(s)
    if not cc or not cc.get('backs') or not cc.get('faces'): bad.append(f'[2] no colour card in config/colorcards.json sets.{s}')
    img = rec.get('colorcard_img')
    if not img or not os.path.exists(R + img): bad.append(f'[2] colour card image missing ({img})')
    proof['colorcard'] = {'img': img, 'wheel': rec.get('wheel_img'), 'backs': (cc or {}).get('backs'), 'faces': (cc or {}).get('faces')}
    # [3] TNT + [3b] other groups
    t = (J('config/tnt-recs.json', {}).get('sets') or {}).get(s)
    if not (isinstance(t, dict) and t.get('scanned') and t.get('source')): bad.append(f'[3] no Tiles & Tablescapes search on record (config/tnt-recs.json sets.{s})')
    og = (t or {}).get('other_groups')
    if not isinstance(og, dict) or not og.get('scanned'): bad.append(f'[3b] other big Facebook groups not searched (config/tnt-recs.json sets.{s}.other_groups)')
    elif not og.get('groups') and not og.get('note'): bad.append('[3b] other_groups has no groups and no note saying why')
    elif any(not g.get('members') for g in og.get('groups', [])): bad.append('[3b] other_groups: every group needs its member count')
    proof['research'] = {'tnt': t, 'other': og}
    # [4] pool
    pool = rec.get('pool') or {}
    if not pool.get('size') or not pool.get('sources'): bad.append('[4] no candidate pool on record (record pool.size + sources)')
    proof['pool'] = pool
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
    if len(picks) != 5: bad.append(f'[7] faces not pre-picked: need 5, record has {len(picks)}')
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
    bad, _ = check(a[0])
    if bad:
        print(f'ALBUM GATE FAIL {a[0]} ({len(bad)}):'); [print('  ' + b) for b in bad]; return 1
    print(f'ALBUM GATE PASS {a[0]}: steps 1-8 on record'); return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
