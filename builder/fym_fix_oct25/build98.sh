#!/bin/bash
# FYM v98 = public "Version 1.2" (docs/FYM-VERSIONS.md) = v97 (Version 1.1, built by build97.sh) + docs/MATCH-INBOX.md Oct 26 night:
# match card racks lower + tighter (v98_card), Mahjong Register single racks + Mahj Mood angled scalloped rack + MFM Natural Wood
# screw holes (v98_racks), angled mat photos flattened + Benjamin edge line (v98_matflat), OG Desert Dreams Up close strip +
# Jubilee Midnight Blue card band (v98_plmstrip). Usage: build98.sh <b97 dir> <out dir>
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0")
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v98_card.py "$D" | tail -1
python3 $H/v98_racks.py "$D" | tail -1
python3 $H/v98_matflat.py "$D" | tail -1
python3 $H/v98_plmstrip.py "$D" | tail -1
python3 $H/strip_inline_img.py "$D/index.html" write
sed -i "s/(Version 1.1)/(Version 1.2)/g; s/Version 1.1/Version 1.2/g" "$D/index.html"; grep -c "Version 1.2" "$D/index.html"
ls -la "$D/index.html"
