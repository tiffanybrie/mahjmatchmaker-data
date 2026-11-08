"""Apply Tiffany's saved review-page answers to the album (Album Playbook step 10: "Claude applies every keep, remove, add,
note and face swap without asking again").

1. Read her answers:   ArtifactData get  url=<review page>  collection=review  doc_id=<set>  out_dir=<dir>
                       -> <dir>/review/<set>.json  (a bare doc or {data: doc, version})
2. python3 scripts/albumreview/read_review.py <set> <dir>/review/<set>.json [--dry-run]
   Changes, all written back to the album's own files:
   - X'd cards           -> removed from the spec, moved to Left out with "You took it out (round N)" + her note
   - hearted cards       -> spec mat her_keep: true
   - notes               -> spec mat her_note (shown on the next round's card)
   - order (unless "Not ordering yet") -> spec mats re-ordered: main section, then holiday
   - "Put it in"         -> left-out mat moves into the spec (group 'yours')
   - "Missed one?" adds  -> new spec mats (group 'yours'; photo from Find Your Mat-ch, holiday if FYM says so)
   - faces               -> record faces.picks = her picks (pre-selected next round) + config/profiles/<set>.json best_features_her
   - cover               -> record covers.default + covers.chosen
   - Bring it in (finds) -> album pool + spec + record bringins[] tracker (scripts/albumreview/bringins.py) + DESK lines
   - anything else / done -> record rounds[-1].anything / done
   Appends record rounds[] {round, applied_at, changes[], answers} -> the next page shows "Round N+1: what changed".
3. Rebuild the cards with the record's card_build commands (gen2 still enforces the code band, TNT and tile-photo gates),
   then python3 scripts/albumreview/build_review.py <set> and republish to the SAME artifact url (record review_url)."""
import json, os, re, sys, io, datetime
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumreview')
SET, SRC = sys.argv[1], sys.argv[2]
DRY = '--dry-run' in sys.argv
J = lambda p: json.load(open(R + p))
rec_p = f'config/album-records/{SET}.json'; rec = J(rec_p)
spec = J(rec['spec']); man = J(rec['cards_dir'] + '/manifest.json')
lo_file = J(rec['leftout']['file']); lo = lo_file[rec['leftout']['key']]
raw = json.load(open(SRC)); A = raw.get('data') if isinstance(raw.get('data'), dict) else raw
rnd = len(rec.get('rounds', [])) + 1
if A.get('round') not in (None, rnd): sys.exit(f"These answers are for round {A.get('round')}, the album is on round {rnd}. Nothing applied.")


def cid(fn): return re.sub(r'-mat\.jpg$', '', fn.replace(f'{SET}-mahjong-tiles-', ''))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', (s or '').lower().replace('&', 'and').replace("'", '')).strip('-')


card2mat = {cid(c['file']): c['mat'] for c in man['cards']}
byname = {m['name']: m for m in spec['mats']}
ch = []
# notes + keeps
for i, n in (A.get('notes') or {}).items():
    m = byname.get(card2mat.get(i))
    if m and n.strip(): m['her_note'] = n.strip(); ch.append(f"Note on {m['name']}: “{n.strip()}”")
for i, v in (A.get('v') or {}).items():
    m = byname.get(card2mat.get(i))
    if m and v == 'keep': m['her_keep'] = True
kept = sum(1 for v in (A.get('v') or {}).values() if v == 'keep')
if kept: ch.append(f'{kept} cards hearted (kept)')
# order
if not A.get('ordering_off') and A.get('order'):
    seq = [card2mat.get(i) for i in (A['order'].get('main', []) + A['order'].get('hol', []))]
    seq = [s for s in seq if s in byname]
    before = [m['name'] for m in spec['mats']]
    rest = [n for n in before if n not in seq]
    after = seq + rest
    if after != before:
        spec['mats'] = [byname[n] for n in after]; moved = sum(1 for a, b in zip(before, after) if a != b)
        ch.append(f'Order updated ({moved} positions changed); new top 3: ' + ', '.join([n for n in after if A.get('v', {}).get(next((i for i, x in card2mat.items() if x == n), ''), '') != 'remove'][:3]))
# removes
rm = [card2mat[i] for i, v in (A.get('v') or {}).items() if v == 'remove' and i in card2mat]
for n in rm:
    m = byname[n]; spec['mats'].remove(m)
    lo.append({'name': n, 'brand': m['brand'], 'img': m['img'], 'why': f'You took it out (round {rnd})' + (f': {m["her_note"]}' if m.get('her_note') else '.'),
               'retired': m.get('retired', False), 'holiday': bool(m.get('holiday')), 'fym': m.get('fym'), 'removed_by_her': rnd})
if rm: ch.append('Taken out: ' + ', '.join(rm))
# put it in
spec['groups'].setdefault('yours', 'Your adds')
def lid(m): return f"lo-{slug(m['brand'])}-{slug(m['name'])}"
put = [m for m in lo if lid(m) in set(A.get('putin') or [])]
for m in put:
    lo.remove(m)
    spec['mats'].append({'group': 'holiday' if m.get('holiday') else 'yours', 'name': m['name'], 'brand': m['brand'], 'img': m['img'],
                         'why': f"Your pick from Left out (round {rnd}). Claude had said: {m['why']}", 'retired': m.get('retired', False),
                         'fym': m.get('fym'), 'lowres': False, 'holiday': bool(m.get('holiday')), 'her_pick': True})
if put: ch.append('Put back in: ' + ', '.join(m['name'] for m in put))
# catalog adds
adds = [a for a in (A.get('adds') or []) if a.get('k') and a.get('n') not in byname]
if adds:
    snap = J('config/fym-mats-snapshot.json')['mats']
    from fym_images import image_bytes
    from PIL import Image
    got = image_bytes([snap[a['k']]['f'] for a in adds if a['k'] in snap]) if not DRY else {}
    os.makedirs(R + f'assets/albums/{SET}/adds', exist_ok=True)
    for a in adds:
        m = snap.get(a['k'], {}); f = m.get('f'); p = f"assets/albums/{SET}/adds/{slug(a['b'])}-{slug(a['n'])}.jpg"
        if f in got:
            im = Image.open(io.BytesIO(got[f])).convert('RGB'); im.save(R + p, quality=92); low = max(im.size) < 800
        else: low = True
        hol = bool(m.get('hol'))
        spec['mats'].append({'group': 'holiday' if hol else 'yours', 'name': a['n'], 'brand': a['b'], 'img': p, 'why': f'Your add from the catalog search (round {rnd}).',
                             'retired': False, 'fym': a['k'], 'lowres': low, 'holiday': hol, 'her_pick': True})
    ch.append('Added from the catalog: ' + ', '.join(a['n'] for a in adds))
# faces
fz = rec['faces']; old = [p['key'] if isinstance(p, dict) else p for p in fz['picks']]
new = A.get('faces') or old
if new != old:
    why = {p['key']: p.get('why', '') for p in fz['picks'] if isinstance(p, dict)}
    fz['picks'] = [{'key': k, 'why': why.get(k, 'Your pick.')} for k in new]
    fz['her'] = {'round': rnd, 'keys': new}
    ch.append(f"Faces: {', '.join(new)} ({len(new)})")
    pp = R + f'config/profiles/{SET}.json'
    if os.path.exists(pp) and not DRY:
        prof = json.load(open(pp)); prof['best_features_her'] = {'keys': new, 'round': rnd, '_note': "Tiffany's face picks from the review page; rebuild best_features from these"}
        json.dump(prof, open(pp, 'w'), indent=1, ensure_ascii=False)
# cover
cv = A.get('cover')
if isinstance(cv, int) and cv != rec['covers'].get('default', 0) and cv < len(rec['covers']['options']):
    rec['covers']['default'] = cv; rec['covers']['chosen'] = cv; ch.append(f"Cover: {rec['covers']['options'][cv]['label']}")
elif isinstance(cv, int): rec['covers']['chosen'] = cv
# new finds (Playbook step 3b + 10b): Bring it in -> album pool + a bring-in tracker entry + DESK line(s) (Claude makes the paid link
# by the brand's route in config/link-routes.json and stages the catalog/FYM entry; Amazon: Associates save, then Ops imports to ShopMy)
fi = {f['id']: f for f in (rec.get('discovery') or {}).get('new_finds', [])}
brought = [fi[k] for k, v in (A.get('finds') or {}).items() if v == 'in' and k in fi]
_have = {m.get('new_find') for m in spec['mats']}
brought_new = [f for f in brought if f['url'] not in _have]  # a bring-in recorded earlier (e.g. by hand) is not added twice
for f in brought_new:
    rec.setdefault('pool', {}).setdefault('new_candidates', []).append({'name': f['name'], 'brand': f['seller'], 'img': f['img'], 'source': 'discovery: her Bring it in', 'link': f['url'], 'her_pick': True})
    spec['mats'].append({'group': 'yours', 'name': f['name'], 'brand': f['seller'].split(' (')[0], 'img': f['img'], 'why': f"Your pick from New finds (round {rnd}). {f.get('why', '')}",
                         'retired': False, 'fym': None, 'lowres': True, 'her_pick': True, 'new_find': f['url']})
if brought:
    ch.append('New finds brought in: ' + ', '.join(f['name'] for f in brought))
    # Playbook step 10b (Nov 8 6:02pm): every bring-in gets a tracker entry (record "bringins": paid link + catalog staging, Amazon
    # Associates save + Ops import); album_gate.py --golive FAILS until each loop is closed. docs/LINK-ROUTES.md
    import bringins as BI
    lines = []
    for f in brought:
        e, is_new = BI.add(rec, f, rnd)
        if is_new: lines += BI.desk_lines(rec, e)
        ch.append(f"Bring-in {e['mat']}: route {e['route']} ({BI.status(e)})")
    if lines and not DRY:
        dp = R + 'docs/DESK.md'; d = open(dp).read()
        d = d.replace('## Handoffs (do first)\n', '## Handoffs (do first)\n' + ''.join(lines), 1) if '## Handoffs (do first)\n' in d else d + '\n' + ''.join(lines)
        open(dp, 'w').write(d)
skipped = [fi[k]['name'] for k, v in (A.get('finds') or {}).items() if v == 'skip' and k in fi]
if skipped: ch.append('New finds skipped: ' + ', '.join(skipped))
if (A.get('anything') or '').strip(): ch.append('Your note: “' + A['anything'].strip()[:300] + '”')
rec.setdefault('rounds', []).append({'round': rnd, 'applied_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                                     'changes': ch or ['No changes: every card stays as it was'], 'anything': A.get('anything', ''), 'done': bool(A.get('done')), 'answers': A})
print(f'{SET} round {rnd}:'); [print('  - ' + c) for c in ch or ['no changes']]
if DRY: sys.exit(0)
json.dump(spec, open(R + rec['spec'], 'w'), indent=1, ensure_ascii=False)
lo_file[rec['leftout']['key']] = lo; json.dump(lo_file, open(R + rec['leftout']['file'], 'w'), indent=1, ensure_ascii=False)
json.dump(rec, open(R + rec_p, 'w'), indent=1, ensure_ascii=False)
print('Next: rebuild the cards:'); [print('  ' + c.format(work=f'/tmp/albumbuild-{SET}')) for c in rec.get('card_build', [])]
print(f'  python3 scripts/albumreview/build_review.py {SET}   then republish to {rec.get("review_url", "<review_url>")}')
