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
# Nov 8 6:55pm (Tiffany, HARD: "If the Google report ever doesn't run, it's the very first thing that you should prompt me for"):
# goes FIRST in the output. Report runs 12:13pm ET daily and commits docs/reports/google-revenue/<date>.md.
try:
    now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))
    want=now.date() if now.hour>=13 else now.date()-datetime.timedelta(days=1)
    ds=sorted(f[:10] for f in os.listdir('docs/reports/google-revenue') if re.match(r'\d{4}-\d\d-\d\d\.md$',f))
    last=ds[-1] if ds else 'never'
    if last<str(want):
        out.insert(0,f"GOOGLE REPORT DIDN'T RUN (last full report {last}, expected {want}). SAY THIS FIRST to Tiffany, before anything else: 'The Google report didn't run (last one {last}). Want me to run it now?' and IN THE SAME REPLY call mcp__claude-code-remote__fire_trigger trig_01LZjGfVneN3vKwweVXwbzub so she only has to tap Approve (if it is disabled, update_trigger enabled:true first). Never wait for her to notice.")
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
# Nov 9 (Tiffany 1:39-1:43am: blurry Dec 1994 + Festive Plaid card; Virora tile insets in a white box): live card sharpness +
# tile-fill scan. Reads docs/status/card-sharpness.json ONLY (written by scripts/checks/card_sharpness_check.py in the morning
# HQ cleanup and after every album/holiday paste). Fix = re-render with the brand's full-size photo (gen2.py refuses blurry/too-small).
try:
    cs=json.load(open('docs/status/card-sharpness.json'))
    cage=(datetime.datetime.now()-datetime.datetime.fromisoformat(cs['at'])).total_seconds()/3600
    if cs.get('fails') or cage>30:
        out.append(f"BLURRY / WHITE-BOXED CARDS LIVE ({len(cs.get('fails',[]))} of {cs.get('cards')} cards; checked {cs['at'][:16]}"+(', STALE: run python3 scripts/checks/card_sharpness_check.py' if cage>30 else '')+'):')
        out+=['  - '+f"{f['page']} | {f['card']} | {f['why']}" for f in cs.get('fails',[])[:8]]
        if len(cs.get('fails',[]))>8: out.append(f"  ... +{len(cs['fails'])-8} more: docs/status/card-sharpness.json")
except Exception: pass
# Nov 8 12:57pm (Tiffany: TNT recs "get missed every single time"): every album set needs a Tiles & Tablescapes search on record.
try:
    r=subprocess.run(['python3','scripts/checks/tnt_check.py'],capture_output=True,text=True,timeout=20)
    if r.returncode: out+=[l for l in r.stdout.splitlines() if l.strip()]
except Exception: pass
# Nov 8 (Album Playbook "How it's enforced"): album_gate for every album in progress (upcoming + colour cards with no live album).
# Reads docs/status/live-albums.json only (refresh: python3 scripts/checks/album_gate.py --refresh-live).
try:
    r=subprocess.run(['python3','scripts/checks/album_gate.py','--in-progress'],capture_output=True,text=True,timeout=20)
    if r.returncode:
        ls=[l for l in r.stdout.splitlines() if l.strip()]
        out.append(f'ALBUMS IN PROGRESS MISSING PLAYBOOK STEPS ({len(ls)}): the review page refuses to build until album_gate passes (config/album-records/<set>.json, Album Playbook steps 1-8):')
        out+=['  - '+l for l in ls[:8]]
except Exception: pass
# Nov 8 1:37pm (Tiffany, Album Playbook step 0): an album tile photo sent for her yes and not answered goes FIRST, every message,
# until she answers (no card is built before it: gen2.py refuses).
try:
    r=subprocess.run(['python3','scripts/checks/tile_photo_check.py'],capture_output=True,text=True,timeout=20)
    if r.returncode: out[0:0]=[l for l in r.stdout.splitlines() if l.startswith('ASK TIFFANY NOW')]
except Exception: pass
# Nov 10 7:52am (Tiffany: Domino Blonde caught Monday, filed, never acted on): partner launches in the next 48h.
try:
    r=subprocess.run(['python3','scripts/checks/launch_48h_check.py'],capture_output=True,text=True,timeout=20)
    if r.returncode: out[0:0]=[l for l in r.stdout.splitlines() if l.strip()]
except Exception: pass
# Nov 10 10:40pm (Tiffany: the hidden Brand Watch page must keep up with every find; she checks it against what she sees).
try:
    import hashlib
    _bw=json.load(open('site/livepatch/brand-watch/published.json'))
    if hashlib.sha256(open('config/brand-watch-curated.json','rb').read()).hexdigest()!=_bw['curated_sha256']:
        out.insert(0,'BRAND WATCH PAGE IS BEHIND the latest finds: run scripts/site_brand_watch.py + scripts/site_brand_watch_preview.py, publish site/livepatch/brand-watch/brand-watch-preview.html to '+_bw['artifact']+', then update site/livepatch/brand-watch/published.json (curated_sha256). Do it this turn.')
except Exception: pass
# Nov 10 10:33pm (Tiffany: new affiliates get forgotten and left out of everything): new partners with open onboarding steps.
try:
    r=subprocess.run(['python3','scripts/checks/partner_checklist.py','--front'],capture_output=True,text=True,timeout=30)
    out[0:0]=[l for l in r.stdout.splitlines() if l.startswith('NEW PARTNER')]
except Exception: pass
# Nov 11 2:19pm (Tiffany: Fait à Main + Maison Mahj half set up; "no gap between what we say and what happens"):
# every partner, in ANY of our partner lists, checked against the codes page AND the app (tile sets + mats).
try:
    r=subprocess.run(['python3','scripts/checks/partner_coverage.py','--front'],capture_output=True,text=True,timeout=40)
    out[0:0]=[l for l in r.stdout.splitlines() if l.startswith('PARTNER HALF SET UP')]
except Exception: pass
# Nov 11 5:28pm (Tiffany: one FB group a day, approve the week in one place, "I want to be asked about Facebook groups every day").
try:
    r=subprocess.run(['python3','scripts/checks/fb_groups_check.py'],capture_output=True,text=True,timeout=10)
    out[0:0]=[l for l in r.stdout.splitlines() if l.strip()]
except Exception: pass
if out:
    print('=== FRONT DOOR (automatic, every message) ===\n'+'\n'.join(out)+'\nRule: if you tell Tiffany you will fix something, fix it BEFORE you reply, or add it to docs/OVERDUE.md in the same turn and tell her who/when.')
