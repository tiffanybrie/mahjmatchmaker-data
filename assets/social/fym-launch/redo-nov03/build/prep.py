"""Rebuild every /dev/shm input for the launch reel redo (Nov 3) from scratch, then render + finish.
  python3 prep.py            -> inputs only
  python3 prep.py --render   -> inputs + reel.py frames + finish.py (all outputs in assets/social/fym-launch/redo-nov03/)
Steps: holiday v5_prep data+logos (app v113 copy, D.json, 38 code-partner logos) -> cards_pick.json -> cap.py all (2x screen
recordings rec0/recA/recP/recB + Story match card) -> cards.py (15 cross-brand match cards) -> dwall.py (48 everyday mats)."""
import subprocess, sys, os, shutil
B = os.path.dirname(os.path.abspath(__file__)); H = '/home/claude/mahjmatchmaker-data/assets/social/holiday-nov1/intro/build'
def run(*a, cwd=B): print('>', ' '.join(a)); subprocess.run(a, check=True, cwd=cwd)
for d in ['/dev/shm/lr', '/dev/shm/lr/dbg', '/dev/shm/lr/mtmp', '/dev/shm/introv2/tmp']: os.makedirs(d, exist_ok=True)
os.environ['MAGICK_TMPDIR'] = '/dev/shm/lr/mtmp'
run('python3', 'v5_prep.py', 'data', cwd=H); run('python3', 'v5_prep.py', 'logos', cwd=H)
shutil.copy(f'{B}/cards_pick.json', '/dev/shm/lr/cards_pick.json')
run('python3', 'cap.py', 'all'); run('python3', 'cards.py'); run('python3', 'dwall.py')
if '--render' in sys.argv: run('python3', 'reel.py', 'frames'); run('python3', 'finish.py')
