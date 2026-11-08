#!/usr/bin/env python3
"""UserPromptSubmit hook (Tiffany Nov 6 2026): before EVERY reply in EVERY chat, show what is broken or overdue.
- pulls the repo (quiet, 10s cap)
- live code/date check (scripts/checks/live_codes_check.py), re-run if the cached result is older than 3 hours
- docs/OVERDUE.md lines + DESK 'Blocked, approved' items
- coverage GAP lines (top 8) from docs/status/coverage.json (scripts/checks/coverage_check.py; file read only)
Prints nothing when all is clear. Output becomes context for the chat, which must deal with it FIRST."""
import subprocess, json, os, re, sys, datetime
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(R)
def run(cmd,t):
    try: return subprocess.run(cmd,shell=True,capture_output=True,text=True,timeout=t).stdout
    except Exception: return ''
run('git pull -q --rebase --autostash',10)
out=[]
st='docs/status/live-check.json'
try:
    age=(datetime.datetime.now()-datetime.datetime.fromisoformat(json.load(open(st))['at'])).total_seconds()/3600
except Exception: age=99
if age>3: run('python3 scripts/checks/live_codes_check.py',45)
try:
    j=json.load(open(st))
    if j['fails']: out.append(f"LIVE SITE IS WRONG ({len(j['fails'])}, checked {j['at']}): fix in Squarespace NOW if Chrome is up, then re-run scripts/checks/live_codes_check.py until PASS:"); out+= ['  - '+f for f in j['fails'][:15]]
except Exception: pass
try:
    od=[l.strip() for l in open('docs/OVERDUE.md') if l.startswith('- ')]
    if od: out.append(f'OVERDUE ({len(od)}), no owner, do it now if you can, delete the line when done:'); out+=['  '+l for l in od]
except Exception: pass
try:
    d=open('docs/DESK.md').read(); m=re.search(r'## Blocked, approved[^\n]*\n(.*?)\n## ',d,re.S)
    items=[l.strip() for l in (m.group(1).splitlines() if m else []) if l.strip().startswith(('-','1','2','3','4','5','6','7','8','9'))]
    if items: out.append(f'BLOCKED BUT APPROVED ({len(items)}): raise at the top of your reply ("These approved tasks are blocked: ... Can I do them now?") and do any you can:'); out+=['  '+l[:220] for l in items[:8]]
except Exception: pass
# Coverage gaps (Tiffany Nov 7: "where do we have other gaps"): read docs/status/coverage.json ONLY (no network, no rebuild here).
# Written by scripts/checks/coverage_check.py (morning HQ cleanup runs it with --refresh).
try:
    cj=json.load(open('docs/status/coverage.json'))
    cage=(datetime.datetime.now()-datetime.datetime.fromisoformat(cj['at'])).total_seconds()/3600
    g=cj.get('gaps',[])+cj.get('unknown',[])
    if g or cage>30:
        out.append(f"COVERAGE GAPS ({len(cj.get('gaps',[]))} GAP, {len(cj.get('unknown',[]))} unknown; checked {cj['at'][:16]}"+(', STALE: run python3 scripts/checks/coverage_check.py --refresh' if cage>30 else '')+'). Not done until X of N = target:')
        out+=['  - '+l.split(' | missing:')[0][:170] for l in g[:8]]
        if len(g)>8: out.append(f'  ... +{len(g)-8} more: python3 scripts/checks/coverage_check.py')
except Exception: pass
# Nov 8 12:57pm (Tiffany: TNT recs "get missed every single time"): every album set needs a Tiles & Tablescapes search on record.
try:
    r=subprocess.run(['python3','scripts/checks/tnt_check.py'],capture_output=True,text=True,timeout=20)
    if r.returncode: out+=[l for l in r.stdout.splitlines() if l.strip()]
except Exception: pass
if out:
    print('=== FRONT DOOR (automatic, every message) ===\n'+'\n'.join(out)+'\nRule: if you tell Tiffany you will fix something, fix it BEFORE you reply, or add it to docs/OVERDUE.md in the same turn and tell her who/when.')
