#!/bin/bash
# FYM v98 = public "Version 1.2" (docs/FYM-VERSIONS.md) = v97 (Version 1.1, built by build97.sh) + docs/MATCH-INBOX.md Oct 26 night:
# match card racks low + tight + equal length, stack photos big (v98_card), Mahjong Register single racks + Mahj Mood angled scalloped
# rack + PLM Chartreuse/Dark Green restored (v98_racks), card title = assigned set colour (v98_title),
# Peppi name + Wren logo (v98_names), Mahjong Row & Co. single racks (v98_racks), OG Desert Dreams Up close strip + Jubilee
# Midnight Blue card band (v98_plmstrip). The angled-mat flattening (v98_matflat.py, config/fym-mat-flat-oct26.json) is POST-LAUNCH
# WIP and NOT in this build (Tiffany Oct 26 7:49pm). Usage: build98.sh <b97 dir> <out dir>
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0")
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v98_card.py "$D" | tail -1
python3 $H/v98_racks.py "$D" | tail -1
python3 $H/v98_plmstrip.py "$D" | tail -1
python3 $H/v98_title.py "$D" | tail -1
python3 $H/v98_names.py "$D" | tail -1
python3 $H/strip_inline_img.py "$D/index.html" write
sed -i "s/(Version 1.1)/(Version 1.2)/g; s/Version 1.1/Version 1.2/g" "$D/index.html"; grep -c "Version 1.2" "$D/index.html"
ls -la "$D/index.html"
python3 $H/v98b_fix.py "$D" | tail -1  # QA fixes: navy title outline for very light colours, Mahjong Register Pearl racks cut out (Oct 26 ~9:20pm)
