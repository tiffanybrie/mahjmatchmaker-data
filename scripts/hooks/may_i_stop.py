#!/usr/bin/env python3
"""Stop hook: 'Am I allowed to stop working?' (Tiffany Nov 21 2026 5:10pm: "After you complete a task... am I allowed to
stop working? Couldn't someone just ask you that? And you would be like, actually, no, I'm not. I better grab something else.")
Runs every time Claude is about to end a turn. If docs/OVERDUE.md still has lines, it refuses the stop ONCE and puts the
question and the next lines in front of Claude. The second time (stop_hook_active) it lets the turn end, so it can never loop.
Rule: CLAUDE.md NEVER STOP WORKING."""
import json, os, sys
try: d = json.load(sys.stdin)
except Exception: d = {}
if d.get('stop_hook_active'): sys.exit(0)
R = os.environ.get('CLAUDE_PROJECT_DIR') or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try: lines = [l for l in open(os.path.join(R, 'docs/OVERDUE.md'), encoding='utf-8').read().split('\n') if l.startswith('- since ')]
except Exception: sys.exit(0)
if not lines: sys.exit(0)
msg = ["AM I ALLOWED TO STOP WORKING? (CLAUDE.md NEVER STOP WORKING, Tiffany Nov 21 2026)",
       f"docs/OVERDUE.md still has {len(lines)} open lines. A deadline is the latest date, not the start date.",
       "You may end this turn ONLY if one of these is true:",
       " (a) Tiffany asked a direct question and this reply answers it, AND a wake-up (send_later) naming the next line is already set; or",
       " (b) every line left needs something you cannot reach right now (her Chrome, her yes), AND the hourly Chrome re-test wake is set.",
       "Otherwise do not stop: start the next doable line now. The last 6 lines on the list:"]
msg += ['  ' + l[:260] for l in lines[-6:]]
print('\n'.join(msg), file=sys.stderr)
sys.exit(2)
