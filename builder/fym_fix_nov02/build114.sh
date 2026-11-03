#!/bin/bash
# FYM v114 = public "Version 1.14" (overnight Nov 1-2): b113 + Table view (third view: Up close / Aerial / Table, from the QA-passed
# preview v14 + the held tablet sheet fix) + price filter on the app's own decks (mat deck, mat-door tile deck, rack deck).
# Usage: build114.sh <b113 dir> <b114 dir>. Out = hardlinks to b113 + a NEW index.html (b113 is never modified).
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $R/builder/table_view/preview_nov01.py "$D/index.html" "$D" --release 1.14   # Table view as a real build (no preview title)
python3 $H/price114.py "$D"
python3 $H/ui114.py "$D"   # rack filter singles + Table tour step (Tiffany Nov 1 11:33pm)
python3 $H/ui114b.py "$D"   # rack filters below the rack deck (Tiffany Nov 3 2:27pm)
