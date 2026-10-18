"""Sync in-use web images from mahjmatchmaker-data to mahjmatchmaker-assets (GitHub Pages).

Usage:
  python3 scripts/assets/sync_assets.py [--push] DIR [DIR ...]
DIRs hold .html/.js/.json that reference jsDelivr URLs
(https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@<commit>/<path>), e.g.
saved live pages, site/livepatch, FYM builds. Nested text files are followed.

For each referenced path, the NEWEST pinned version is staged into the assets repo at the
same relative path. No files are copied to disk: the assets clone uses the data repo's
objects via .git/objects/info/alternates and updates its index directly (skip-worktree).
Writes url_map.json: jsDelivr URL -> https://tiffanybrie.github.io/mahjmatchmaker-assets/<path>
Note: Pages serves the latest version per path (no commit pin), so when an image changes
in place, the Pages URL changes content too.
"""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.environ.get('ASSETS_REPO', '/home/claude/mahjmatchmaker-assets')
BASE = 'https://tiffanybrie.github.io/mahjmatchmaker-assets/'
args = sys.argv[1:]; push = '--push' in args; dirs = [a for a in args if a != '--push']
if not dirs: sys.exit(__doc__)
alt = os.path.join(ASSETS, '.git/objects/info/alternates')
want = os.path.join(DATA, '.git/objects')
if not os.path.exists(alt) or want not in open(alt).read():
    open(alt, 'a').write(want + '\n')
tmp = tempfile.mktemp(suffix='.json')
subprocess.run([sys.executable, os.path.join(HERE, 'collect_inuse.py'), tmp, *dirs], check=True)
inuse = json.load(open(tmp))
def git(repo, *a, **k):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, **k)
cur = {}
for line in git(ASSETS, 'ls-files', '-s').stdout.splitlines():
    meta, path = line.split('\t', 1); cur[path] = meta.split()[1]
lines, changed, urlmap = [], [], {}
for p, c in sorted(inuse.items()):
    sha = git(DATA, 'rev-parse', f'{c}:{p}').stdout.strip()
    if not sha: continue
    urlmap[f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{c}/{p}'] = BASE + p
    if cur.get(p) != sha:
        lines.append(f'100644 {sha}\t{p}\n'); changed.append(p)
json.dump(urlmap, open(os.path.join(os.getcwd(), 'url_map.json'), 'w'), indent=1)
print(len(inuse), 'in use;', len(changed), 'new/changed; url_map.json written')
if changed:
    git(ASSETS, 'update-index', '--add', '--index-info', input=''.join(lines))
    for i in range(0, len(changed), 200):
        git(ASSETS, 'update-index', '--skip-worktree', *changed[i:i+200])
    git(ASSETS, 'commit', '-q', '-m', f'Sync {len(changed)} web images\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_014aKoC1ZMdZPjGkZ9kHhnLk')
    if push:
        git(ASSETS, 'fetch', '-q', 'origin', 'main')
        r = git(ASSETS, 'push', '-q', 'origin', 'HEAD:main')
        print('pushed' if r.returncode == 0 else 'PUSH FAILED: ' + r.stderr[-300:])
    else:
        print('committed locally; rerun with --push (keep each push under ~50 MB)')
