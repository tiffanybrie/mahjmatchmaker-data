#!/bin/bash
# FYM v116 = public "Version 1.16" (Nov 6): b115 +
#  1. auto-apply discount links (gate [159])            5. Mahj Pit White Beech Wood rack (rule 6b reviewed; other 5 left out)
#  2. 17 dead shop links: no shop button, not Retired   6. Mahjong Row & Co. parked out (Tiffany Nov 6 1:19pm, gate [160])
#     (config/fym-dead-links.json, gate [162])          7. Juniper: Palm Royale, Garden Glow, Lotus Cove (pair mat in top 3, gate [57])
#  8. MATCH-INBOX build items (inbox116.py) + her 41 thin-album hearts (v94_thinpicks.py)
#  9. Mahjong Co. mats hidden + parked (Tiffany Nov 6 3:56pm; Kaleidoscope tiles stay)
#  3. colour fixes from the Mat Gallery v6 work (cream read as orange/yellow, magenta read as purple; locked colours untouched)
# Usage: build116.sh <b115 dir> <b116 dir>. Out = hardlinks to b115 + NEW index.html (b115 is never modified).
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $R/builder/fym_fix_oct26/v94_thinpicks.py "$D"                # her 41 thin-album hearts (live on 9 albums since Nov 1) join m
python3 $H/inbox116.py "$D"                                          # MATCH-INBOX: LBB relinks, Domino Blonde rules link, 2 sold out, Brownstone album link
python3 $H/autoapply_links.py "$D" --write | tail -2
python3 $H/deadlinks116.py "$D"
python3 $H/mr_out.py "$D"
python3 $H/mco_out.py "$D"                                             # Mahjong Co. mats hidden (Tiffany Nov 6 3:56pm; gate [161])
python3 $H/colour116.py "$D"
python3 $H/racks116.py "$D"
python3 $R/builder/fym_fix_oct25/v92_coordinated.py "$D" | grep -i juniper
python3 $H/sideb116.py "$D"                                          # Bespoke side B after side A again (gate [78])
python3 $H/release116.py "$D"
python3 $R/builder/fym_apply_locks.py "$D"
