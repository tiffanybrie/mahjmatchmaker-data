"""Hand-post wake gate (OVERDUE line 243; from the 2026-11-24 8:05pm miss: the Sadie Jane countdown story was only a
Planoly reminder, and reminders go nowhere now she's stopped using Planoly -- nothing else told her it was time to
post). Rule: every hq/social plan item with status 'needs-you' and a real time must have a matching send_later /
create_trigger wake logged in config/handpost-wakes.json. This gate FAILS any such item with no matching wake, so a
hand-post item can never again depend on a Planoly reminder alone.

Reads:
  docs/status/hq-social-plan.json  -- local snapshot of HQ db doc hq/social's 'plan' field (refresh it whenever
                                       hq/social changes: re-fetch via db_get and overwrite this file)
  config/handpost-wakes.json       -- every wake Main has set, keyed by day+what (log a new entry here the same
                                       turn a send_later/create_trigger wake is set for a needs-you item)

A 'time' of '-', 'any', 'Draft', or empty is not a real clock time (nothing to wake FOR) and is skipped; any
other value counts, including relative ones like 'Tonight or Wed morning'.

Usage: python3 scripts/checks/handpost_wake_check.py [--front]   (--front = one-line summary for front_door.py)"""
import json, re, sys, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
NO_TIME = {'-', '', 'any', 'draft', 'on your go', '—'}

def norm(s):
    return re.sub(r'\s+', ' ', (s or '').strip().lower())

try:
    plan = json.load(open(R + 'docs/status/hq-social-plan.json'))['plan']
except FileNotFoundError:
    print('handpost wake gate: NO SNAPSHOT (docs/status/hq-social-plan.json missing -- fetch hq/social via db_get and write it)')
    sys.exit(1)

try:
    wakes = json.load(open(R + 'config/handpost-wakes.json'))['wakes']
except FileNotFoundError:
    wakes = []

logged = {(norm(w.get('day')), norm(w.get('what'))) for w in wakes}

fails = []
for day_block in plan:
    day = day_block.get('day', '')
    for post in day_block.get('posts', []):
        if post.get('status') != 'needs-you':
            continue
        t = norm(post.get('time'))
        if t in NO_TIME:
            continue
        key = (norm(day), norm(post.get('what')))
        if key not in logged:
            fails.append('%s | %s @ %s (%s)' % (day, post.get('what'), post.get('time'), post.get('where')))

if '--front' in sys.argv:
    if fails:
        print('HAND-POST ITEMS WITH NO WAKE SET (%d): log a send_later/create_trigger wake in config/handpost-wakes.json NOW, or it will rely on a Planoly reminder that no longer reaches her:' % len(fails))
        for f in fails:
            print('  - ' + f)
    sys.exit(0)
else:
    for f in fails:
        print('FAIL no wake:', f)
    print('handpost wake gate: checked %d day-blocks -' % len(plan), 'PASS' if not fails else 'FAIL %d' % len(fails))
sys.exit(1 if fails else 0)
