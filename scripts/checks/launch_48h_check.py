#!/usr/bin/env python3
"""Partner launches in the next 48h must be ACTED ON, not filed (Tiffany Nov 10 7:52am: Domino Blonde was caught Mon 1:30pm,
filed in brand-watch-curated.json as a 'reshare' note, and nothing was built or told to her before Tue).
Every partner item in brand-watch-curated.json this_week/coming_soon dated today..+2 days needs a line in
config/launch-actions.json: {"<id>": {"status": "posted|drafted|skip", "note": "...", "by": "..."}}.
'drafted' still shows until posted or she says skip. Prints one line per open item; exit 1 if any."""
import json, datetime, re, sys
R = '/home/claude/mahjmatchmaker-data/'
try: d = json.load(open(R + 'config/brand-watch-curated.json'))
except Exception: sys.exit(0)
try: acts = json.load(open(R + 'config/launch-actions.json'))
except Exception: acts = {}
today = datetime.date.today(); soon = today + datetime.timedelta(days=2)
open_ = []
for sec in ('this_week', 'coming_soon', 'just_dropped'):
    for x in d.get(sec, []) or []:
        if not x.get('partner'): continue
        try: dt = datetime.date.fromisoformat(str(x.get('date', ''))[:10])
        except Exception: continue
        if not (today <= dt <= soon): continue
        key = re.sub(r'[^a-z0-9]+', '-', (x.get('brand', '') + ' ' + x.get('what', '')[:40]).lower()).strip('-')[:70]
        st = (acts.get(key) or {}).get('status')
        if st in ('posted', 'skip'): continue
        open_.append(f"  - {x.get('day','')} {x.get('time','')} | {x.get('brand','')}: {x.get('what','')[:90]} | {st or 'NOTHING BUILT'} | key {key}")
if open_:
    print(f"PARTNER LAUNCHES IN 48H NOT YET POSTED ({len(open_)}): draft a group post/story NOW, show Tiffany, post on her yes; mark config/launch-actions.json posted|skip:")
    print('\n'.join(open_)); sys.exit(1)
