#!/usr/bin/env python3
"""DESK DROP CHECK (Tiffany Nov 11 3:01pm: "the desk cleanup Claude deleted it... What gave that Claude the right?").

Why: the Nov 7 end-of-day DESK rewrite (commit 90efa799) silently dropped the line
"| Fait à Main code | Main | MAHJMATCH still not applicable at cart. | Watch |". Nothing had been done; the rewrite
regenerated the page and the open item vanished. Rewrites may reorder and condense, but an OPEN item may only leave the
DESK with proof: a DONE/CLOSED line in docs/ANSWERS.md, or the item moved to docs/OVERDUE.md / docs/MATCH-INBOX.md.

How: for every commit that touched docs/DESK.md in the window, take the table rows + bullet lines it removed. A removed
line counts as CARRIED if a distinctive key from it (its first cell / first ~6 words) still appears in the current
DESK, OVERDUE, MATCH-INBOX, or in an ANSWERS line marked DONE/CLOSED/no longer needed. Anything else = DROPPED.
Usage: desk_drop_check.py [--since "3 days ago" | --commit <sha>] [--front]   (the desk cleanup runs it with --commit on its own rewrite BEFORE pushing)
--front: one line per dropped item (scripts/hooks/front_door.py shows them in every chat until restored or proven done).
Exception list: config/desk-drop-ok.json {"<key>": "<proof / reason, date>"} for lines checked by hand."""
import subprocess, re, os, sys, json
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
a = sys.argv; since = a[a.index('--since') + 1] if '--since' in a else '3 days ago'
git = lambda *x: subprocess.run(['git', '-C', R, *x], capture_output=True, text=True).stdout
norm = lambda s: re.sub(r'[^a-z0-9 ]', ' ', s.lower()).split()
def key(line):
    t = line.strip().lstrip('-*').strip()
    if t.startswith('|'):
        cells = [c.strip() for c in t.strip('|').split('|')]
        t = cells[0] if cells else t
    t = re.sub(r'\*\*', '', t)
    w = [x for x in norm(t) if len(x) > 2][:6]
    return ' '.join(w)
here = ' '.join(norm(' '.join(open(R + p).read() for p in ('docs/DESK.md', 'docs/OVERDUE.md', 'docs/MATCH-INBOX.md') if os.path.exists(R + p))))
done_txt = ' '.join(norm(' '.join(l for l in open(R + 'docs/ANSWERS.md') if re.search(r'\b(DONE|CLOSED|no longer needed|not needed)\b', l))))
ok = json.load(open(R + 'config/desk-drop-ok.json')) if os.path.exists(R + 'config/desk-drop-ok.json') else {}
SKIP = re.compile(r'^\s*\|\s*(-{3}|item\b|owner\b)|top priorities|^\s*$', re.I)
# Only OPEN-ITEM lines count: table rows (In progress / waiting) and owner bullets ("- **Main:", "- **OPS", "- **Matches"),
# not narrative, headers or the dated top-5 (those are rewritten every night by design).
ITEM = re.compile(r'^\s*\|(?!\s*-{3})|^\s*-\s*\*\*(Main|OPS|Ops|Matches)', re.I)
dropped = {}
commits = [a[a.index('--commit') + 1]] if '--commit' in a else git('log', f'--since={since}', '--format=%h', '--', 'docs/DESK.md').split()
for c in commits:
    diff = git('show', c, '--format=', '--unified=0', '--', 'docs/DESK.md')
    added = {key(l[1:]) for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')}
    for l in diff.splitlines():
        if not l.startswith('-') or l.startswith('---') or SKIP.search(l[1:]) or not ITEM.search(l[1:]): continue
        k = key(l[1:])
        if len(k.split()) < 2 or k in added or k in ok: continue
        if k in here or k in done_txt: continue
        dropped.setdefault(k, (c, l[1:].strip()[:160]))
if '--front' in a:
    for k, (c, l) in dropped.items():
        print(f"DESK LINE DROPPED WITHOUT PROOF ({c}): {l}  -> put it back on DESK/OVERDUE with owner + date, or log DONE proof in ANSWERS.")
    sys.exit(0)
print(f'DESK DROP CHECK since {since}: {len(dropped)} open line(s) removed with no DONE proof')
for k, (c, l) in dropped.items(): print(f'  {c}: {l}')
sys.exit(1 if dropped else 0)
