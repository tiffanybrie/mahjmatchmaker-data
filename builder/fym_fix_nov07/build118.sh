#!/bin/bash
# FYM v118 = public "Version 1.18" (Nov 7 night) = b117 (the 1.17 build, = website fym-v117 except tile photo paths) +
#  a. adds118.sh: 25 ShopMy mats + 28 Amazon holiday picks (amazon118.py: v96 adds without its stale cr placement), Luna Hummingbird
#     Mint hidden + Questionable (gate [3]/[3d]), ShopMy links for Blue Pastel Palm Beach + Rainbow Row
#  +  partner_adds118.py: Mahj Mood Playing For Keeps + Fait a Main Texas Mon Amour Green (gate [100])
#  +  fixes118.py: LSF Fleur ShopMy link (MATCH-INBOX), Deco titles = back colour (gate [103]), Mac + Miller seconds on the sweep ignore list
#  d. revive_links.py: dead-link items whose store product is live again get their shop button back (OMM Pearlescent, $475)
#  -  autoapply_links + v104rank (new mats colour-ranked, gate [107]) + v92_coordinated (gate [57]) + colour116 + locks
#  b. tv118.py: Table view walls from config/tableview-back-colors.json (BACKS = a committed snapshot) + prices refreshed
#  e. price118.py: no-price items shown last with 'Price not listed' instead of hidden (gate [166])
#  c. zoomswipe_v118.py (after the data patches), then release118.py (Version 1.18 + tracking)
# Usage: build118.sh <b117 dir> <b118 dir> <backs json>. Out = hardlinks to b117 + NEW index.html (b117 is never modified; new mc
# chunks are new files).
set -eo pipefail; S=$1; D=$2; BK=$3; H=$(cd "$(dirname "$0")" && pwd); R=$(cd "$H/../.." && pwd)
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
"$H/adds118.sh" "$D"
python3 "$H/partner_adds118.py" "$D" | tail -3
python3 "$H/fixes118.py" "$D"
python3 "$H/revive_links.py" "$D" | tail -2
python3 "$R/builder/fym_fix_nov06/autoapply_links.py" "$D" --write | tail -2
python3 "$R/builder/fym_fix_oct30/v104rank.py" "$D" | tail -2
python3 "$R/builder/fym_fix_oct25/v92_coordinated.py" "$D" | tail -2
python3 "$R/builder/fym_fix_nov06/colour116.py" "$D" | tail -2
python3 - "$R" <<'PY'                                                 # colour116 rewrites 'changed' with only this run's changes: keep the earlier record (gate [163] reads it)
import json, sys, subprocess; R = sys.argv[1]; p = R + '/config/fym-colour-fixes-v116.json'; C = json.load(open(p))
old = json.loads(subprocess.run(['git', '-C', R, 'show', 'HEAD:config/fym-colour-fixes-v116.json'], capture_output=True, text=True).stdout)
for sec in ('changed', 'skipped'):
    if isinstance(old.get(sec), dict) and isinstance(C.get(sec), dict): C[sec] = {**old[sec], **C[sec]}
json.dump(C, open(p, 'w'), indent=1, ensure_ascii=False); print('colour116 record kept:', len(C['changed']), 'changed')
PY
python3 "$R/builder/fym_fix_nov06/sideb116.py" "$D" | tail -1
python3 "$R/builder/fym_apply_locks.py" "$D" | tail -2
python3 "$H/tv118.py" "$D" --backs "$BK"
python3 "$H/price118.py" "$D"
python3 "$H/zoomswipe_v118.py" "$D" | tail -1
python3 "$H/release118.py" "$D"
