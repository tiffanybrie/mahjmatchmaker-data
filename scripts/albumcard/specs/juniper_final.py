"""Juniper FINAL album spec (Tiffany's order, Nov 7 11:21pm 'done': config/picks/juniper-final-order-2026-11-07.json, 42 in).
Pulls each card's spec row (photo, crop box, racks, why) from the round-3 / holiday / to-see / OMM-adds specs by mat + brand, in HER
order, and sets the code band:
- Nov 8 HARD RULE (Tiffany 10:11am, docs/ANSWERS.md): every Juniper card has Oh My Mahjong tiles (a partner), so EVERY card carries the
  code band. Non-partner mats (Mahj Tile Haus, Sophie Clima, That Mahjong Moment, Betty June & Jeannette) and Mahjong Register (MAHJMATCH
  not working there yet, cart test Nov 7) get 'SAVE WITH CODE : MAHJMATCH' (no % promise). Never 'NOT A PARTNER : NO CODE' /
  'NO CODE AT THIS TIME' on a card: 'no code' notes live in the page captions only. gen2.py refuses a no-code band
  (scripts/checks/card_code_band_check.py).
- Green Malachite (Mahj Squad): every Mahj Squad photo but one carries MAHJ SQUAD overlay watermarks; card now uses the one clean
  product image (mats-191, the library table shot), cropped to the mat and EDSR x4 (assets/colorcards/juniper/mats/green-malachite-mahj-squad.jpg).
Usage: python3 juniper_final.py  -> writes scripts/albumcard/specs/juniper_final_nov07.json; then
  JUNIPER_SPEC=scripts/albumcard/specs/juniper_final_nov07.json python3 juniper_build.py <work> && gen2.py <work>/spec.json assets/cards/juniper-final"""
import json, re
R = '/home/claude/mahjmatchmaker-data/'
SP = R + 'scripts/albumcard/specs/'
specs = [json.load(open(SP + f + '.json')) for f in ('juniper_round3', 'juniper_holiday_nov07', 'juniper_see_nov07', 'juniper_omm_nov07')]
KEYS = {}
for s in specs: KEYS.update(s['rack_keys'])
ROWS = {}
for s in specs:
    for m in s['mats']: ROWS.setdefault((m['name'], m['brand']), m)
PARTNERS = set(json.load(open(R + 'builder/fym_flags/nonpartner_allow.json'))['partners'])
ORDER = json.load(open(R + 'config/picks/juniper-final-order-2026-11-07.json'))['in']
out = []
for it in ORDER:
    m = re.match(r'^(.*)\(([^()]*)\)\s*$', it); name, brand = m.group(1).strip(), m.group(2).strip()
    row = dict(ROWS[(name, brand)]); row.pop('out', None); row.pop('out_reason', None); row.pop('code', None)
    if brand not in PARTNERS or brand == 'Mahjong Register': row['code'] = 'SAVE WITH CODE : MAHJMATCH'  # Nov 8 rule: band always on
    if name == 'Green Malachite':
        row['img'] = 'assets/colorcards/juniper/mats/green-malachite-mahj-squad.jpg'; row['box'] = [0, 0, 1680, 1728]
        row['photo_src'] = 'mahjsquadshop.com green-malachite-mahjong-mat-mats-191.webp (only image without overlay watermarks), mat crop, EDSR x4'
    out.append(row)
json.dump({'_note': "Juniper FINAL: Tiffany's order Nov 7 11:21pm (42 cards); built by juniper_final.py", 'rack_keys': KEYS, 'mats': out},
          open(SP + 'juniper_final_nov07.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'cards;', sum('code' in r for r in out), 'code overrides:', [(r['name'], r['code']) for r in out if 'code' in r])
