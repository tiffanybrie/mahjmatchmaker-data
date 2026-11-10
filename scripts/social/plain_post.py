#!/usr/bin/env python3
"""Plain album-launch posts, fill-in-the-blank only (Tiffany Nov 10 11:45am, STANDING).

Her words: "really matter-of-fact posts... friendly, but basically facts... all this cute stuff requires me to
monitor it, and I don't have time." So Claude no longer WRITES album-launch captions. This script fills fixed
sentences with facts (set, brand, release time, match count, code %), and nothing else. No one-liners, no
personality copy, no "she's a ...". Rules: docs/social/PLAIN-POSTS.md. Output is linted with content_lint.py.

Usage: plain_post.py --set Juniper --brand "Oh My Mahjong" --release "this Wednesday 11/11 at 10am CT" --count 42 \
         --album https://www.mahjmatchmaker.com/juniper-mahjong-tile-matches --tag ohmymahjong --out <dir>
Writes <dir>/ig-caption.txt (IG + FB Page) and <dir>/group-post.txt (FB group, links typed out)."""
import argparse, json, os, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FYM = 'https://www.mahjmatchmaker.com/find-your-match'

a = argparse.ArgumentParser()
for k in ('set', 'brand', 'release', 'album', 'tag', 'out'):
    a.add_argument('--' + k, required=True)
a.add_argument('--count', type=int, required=True)
a.add_argument('--partner-mat', default='')
a.add_argument('--emoji', default='')
a.add_argument('--every-set', action='store_true', help='we have an album for every set this brand ever made (Tiffany: OMM, Nov 10)')
a.add_argument('--instock', action='store_true', help='set is already for sale: no release line')
x = a.parse_args()

pct = json.load(open(R + '/config/code-truth.json'))['pct'].get(x.brand)
if not pct:
    sys.exit(f'FAIL: no verified code % for {x.brand} in config/code-truth.json')
# Her voice, from her own Nov 9 10:47am line: "The latest Oh My Mahjong set Juniper releases this Wednesday 11/11 at
# 10am CT! As always I have an album for you (link below) and you can also match both Juniper and her new partner mat
# Lotus up in Find-Your-Mat-ch!" Facts + a little excitement in HER words; no invented one-liners.
when = (f"The latest {x.brand} set, {x.set}, is in stock now!" if x.instock
        else f"The latest {x.brand} set, {x.set}, releases {x.release}!")
pm = f" and her new partner mat, {x.partner_mat}," if x.partner_mat else ""
code = f"Use code MAHJMATCH to save {pct}% at {x.brand} 💕"
every = f" (plus an album for every {x.brand} set ever made)" if x.every_set else ""
ig = (f"{when} {x.emoji}\n\nAs always, I have an album for you: {x.count} mats matched to {x.set}{every}, link in bio. "
      f"You can also match {x.set}{pm} in Find Your Mat-ch!\n\n{code}\n\n"
      f"#mahjong #{x.tag} #mahjongtiles #mahjongmat #MahjMatch")
grp = (f"{when} {x.emoji}\n\nAs always, I have an album for you: {x.count} mats matched to {x.set}{every}.\n{x.album}\n\n"
       f"You can also match {x.set}{pm} in Find Your Mat-ch!\n{FYM}\n\n{code}\n\n#MahjMatch")

os.makedirs(x.out, exist_ok=True)
paths = []
for name, txt in (('ig-caption.txt', ig), ('group-post.txt', grp)):
    p = os.path.join(x.out, name); open(p, 'w').write(txt + '\n'); paths.append(p)
L = R + '/scripts/social/content_lint.py'
r1 = subprocess.run([sys.executable, L, paths[0]], capture_output=True, text=True)
r2 = subprocess.run([sys.executable, L, '--codes-list', paths[1]], capture_output=True, text=True)  # group post: typed links, length exempt
print(r1.stdout.strip()); print(r2.stdout.strip()); sys.exit(r1.returncode or r2.returncode)
