#!/usr/bin/env python3
"""Publish the Brand Watch page with a push, no Chrome (Tiffany Nov 20 2026 9:10am: 'make the page load from the repo the way
Find Your Mat-ch does, so Duet publishes without my laptop').
The live /brand-watch page block reads site/livepatch/brand-watch/live.json on branch partner-catalogs-sqsp (5-minute cache) and
swaps in the block it names. This script: checks site/livepatch/brand-watch/block.html, commits it, points live.json at that
commit (pinned jsDelivr URL), commits and pushes.
usage: edit site/livepatch/brand-watch/block.html (set the 'Last updated' line), then  python3 scripts/site_brand_watch_publish.py
After ~5 minutes read https://www.mahjmatchmaker.com/brand-watch in a real browser (the swap happens in the browser; curl shows
the last PASTED block, which is the fallback Google also reads: an attended chat re-pastes page-block-loader.html about weekly)."""
import json, re, subprocess, sys, datetime, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
B = 'site/livepatch/brand-watch/block.html'; J = 'site/livepatch/brand-watch/live.json'
h = open(B).read()
bad = []
if h.count('<div') != h.count('</div>'): bad.append('unbalanced <div>')
if h.count('<section') != h.count('</section>'): bad.append('unbalanced <section>')
if h.count('<article') != h.count('</article>') or h.count('<article') < 40: bad.append('article count')
if 'class="bw"' not in h or 'bw-updated' not in h or len(h) < 20000: bad.append('not a Brand Watch block')
if re.search(r'claude\.ai|sca_ref=[^"&]*["&][^>]*>Shop[^<]*</a>\s*<div class="bw-save">[^<]*Tested at checkout', h) and 'claude.ai' in h: bad.append('claude.ai link')
if re.search(r'Yellow Mountain', h): bad.append('Yellow Mountain Imports is never featured')
if bad: sys.exit('NOT PUBLISHED: ' + '; '.join(bad))
run = lambda *a: subprocess.run(a, check=True, capture_output=True, text=True).stdout.strip()
run('git', 'add', B)
if run('git', 'diff', '--cached', '--name-only'):
    run('git', 'commit', '-q', '-m', 'Brand Watch block ' + (re.search(r'Last updated[^<]*', h) or [''])[0])
sha = run('git', 'log', '-1', '--format=%H', '--', B)
j = json.load(open(J)); now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))
j['block'] = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/{B}'; j['version'] = now.strftime('%Y-%m-%dT%H:%M'); j['published'] = now.isoformat(timespec='seconds')
open(J, 'w').write(json.dumps(j, indent=2) + '\n')
run('git', 'add', J); run('git', 'commit', '-q', '-m', 'Brand Watch live.json -> ' + sha[:8])
subprocess.run('git pull -q --rebase origin partner-catalogs-sqsp && git push -q origin HEAD:partner-catalogs-sqsp', shell=True, check=True)
print('PUBLISHED', j['version'], sha[:8], '(live within about 5 minutes)')
