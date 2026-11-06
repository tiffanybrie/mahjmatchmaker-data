import json, re
C = json.load(open('/dev/shm/sun/new_cands.json'))
M = json.load(open('/dev/shm/sun/mats.json'))
NOV = re.compile(r"game ?day|gameday|ghoul|spell|turkey|\busa\b|liberty|michigan|ramblin|dawgs|uga\b|bulldog|tiger fans|western boot|"
                 r"pups|rooster|cranberry from a can|corn maze|summerween|halloween|witch|spooky|go blue|cowgirl|boot|football|"
                 r"tailgate|\bhorns?\b|aggie|gator|tide\b|mascot|kristen \(usa\)|neon", re.I)
out = {}
for sid, L in C.items():
    seen = {}; pick = []
    for s, k, n, bn in L:
        m = M[k]
        if NOV.search(n): continue
        if seen.get(bn, 0) >= 2: continue
        seen[bn] = seen.get(bn, 0) + 1
        pick.append({'key': k, 'name': n, 'brand': bn, 'score': s, 'f': m['f'], 'add': m.get('add'), 'w': m.get('w')})
        if len(pick) >= 12: break
    out[sid] = pick
json.dump(out, open('/dev/shm/sun/new_pick12.json', 'w'), indent=1, ensure_ascii=False)
for sid, p in out.items(): print(sid, [(x['name'], x['brand'], x['add']) for x in p])
