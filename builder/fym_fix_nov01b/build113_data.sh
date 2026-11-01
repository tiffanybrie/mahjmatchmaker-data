#!/bin/bash
# FYM v113 = public "Version 1.13" (Nov 1, Tiffany 4:50am): Sunday Ruby + Forrest, Let's Be Besties full catalog, per-brand cap,
# Dapper explainer hook (off), Dapper 1/2 + Polo Club wfh. Usage: build113_data.sh <b112 dir> <b113 dir>. Out = hardlinks + NEW files.
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $H/adds113.py "$D"
python3 $R/builder/fym_fix_oct30/v104rank.py "$D"
python3 $H/cr113.py "$S/index.html" "$D"
python3 $H/ui113.py "$D"
python3 $H/answers113.py "$D"                            # Tiffany Nov 1 3:27pm: Estate Sale wfh, Queen Bee corner crop visible (tvc)
python3 $H/pearl113.py "$D"                              # Tiffany Nov 1 3:43pm: Pearl rack finish chip + finish words in rack search
python3 $H/ui113b.py "$D"                               # QA Nov 1 round 1: cap over album+catalog, hidden racks out of search, preview height + tour wait, finish row, Dapper in holiday decks
python3 $H/photos113.py "$D"                            # QA round 2: Sky Blue Florals flat render; 3 angled Oct-16 LBB mats hidden
python3 $H/ui113c.py "$D"                               # QA round 2: card links open with a mouse; Also available links to the variant
