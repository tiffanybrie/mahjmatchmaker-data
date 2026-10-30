#!/bin/bash
# FYM v105 = public "Version 1.9" (Oct 30 pm) = v104 + step-2 layout (pictures touching, controls below) + search at every step
# + Bespoke double-sided fixes (Gray Malin Getaway Dogs Side A/B; Jungle Hot Pink album entry gets the partner link)
# + 3 Let's Be Besties Christmas mats (gate [100]). Usage: build105.sh <b104 dir> <out dir>.
# Out = hardlinks of b104 + NEW files only (never writes through a hardlink).
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"
python3 $H/patch105.py "$S/index.html" "$D/index.html"
python3 $H/patch105b.py "$D/index.html"   # QA fixes: US spelling, search scroll, (retired), rack side buttons
python3 $H/partneradds105.py "$D"   # gate [100]: 3 Let's Be Besties Christmas mats live Oct 28
python3 $H/v105data.py "$D"
python3 $H/v104rank.py "$D"
python3 $H/v105so.py "$D"   # side B of double-sided mats: own mat-door tile order
python3 $R/builder/fym_fix_oct25/strip_inline_img.py "$D/index.html" write
python3 $H/v105_imgout.py "$D"   # artifact limit: inline IMG blocks -> appended to a NEW b24v1.js (index <= 15.5MB)
grep -c "Version 1.9" "$D/index.html"
