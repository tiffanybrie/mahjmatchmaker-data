#!/usr/bin/env python3
"""FB GROUPS DAILY (Tiffany Nov 11 5:28pm: "I want to be asked about Facebook groups every day"). Front door, every message.
Prints one ASK line until today's group post is posted (or she skipped today), and a week line when next week's 7 aren't approved."""
import json, datetime, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
d = json.load(open(R + 'config/fb-groups.json'))
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))); today = now.date().isoformat()
done = {p.get('date') for p in d.get('posted', [])} | set(d.get('skipped_days', []))
plan = {x['date']: x for w in d.get('weeks', []) for x in w.get('days', [])}
appr = {x['date'] for w in d.get('weeks', []) if w.get('approved') for x in w.get('days', [])}
if today not in done:
    x = plan.get(today)
    if not x: print(f"ASK TIFFANY: FACEBOOK GROUP TODAY ({today}): no week planned yet. Build/finish the week's 7 groups + intros (config/fb-groups.json) and ask her to approve the week.")
    elif today in appr: print(f"FACEBOOK GROUP TODAY ({today}): {x['group']} is APPROVED and not posted yet: post it from her Facebook in Chrome now, log it in config/fb-groups.json posted.")
    else: print(f"ASK TIFFANY: FACEBOOK GROUP TODAY ({today}): {x['group']} is waiting on her week approval ({d['weeks'][-1].get('page','')}).")
nxt = (now.date() + datetime.timedelta(days=(7 - now.weekday()) % 7 or 7)).isoformat()
if now.weekday() >= 4 and nxt not in plan: print(f"FACEBOOK GROUPS: next week (from {nxt}) has no 7 groups planned yet: build them before Monday.")
